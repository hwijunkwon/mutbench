#!/usr/bin/env python3
"""P1: 100k-permutation null calibration of Algorithm 1 4-core (and 3-core).

Four null types per pathogen:
  1. iid prevalence-preserving: random permutation of the label vector.
  2. circular_shift:             shift labels by random offset (wraparound).
  3. protein_block_shuffle:      within each fixed 50-residue block, shuffle
                                  labels (preserves within-block prevalence).
  4. local_burden_preserving:    stratify positions into 5 quintiles by local
                                  burden = mean(freq + entropy) over +/-5
                                  window, then shuffle labels within stratum.

For each null type, generate N permutations of y, compute (batched in numpy):
  - exact MCC at top-10% (against the fixed Algorithm 1 prediction)
  - +/-10-window MCC (window-dilated TP/FP)
  - top-20 precision (fixed-count, independent of threshold)
  - enrichment at top-10%

Report observed value, null mean, null SD, observed percentile,
ONE-SIDED above-null p (primary, per codex review Q7), TWO-SIDED p
(sensitivity), Stouffer-aggregated global one-sided p across the
12 pathogens (using one-sided z = norm.ppf(1 - p_one_sided)).

Args:
  --n-perm    integer (default 100000)
  --workers   integer (default 1; multiprocessing pool size if >1)
  --pathogen  optional name to restrict to one pathogen (smoke test)
  --smoke     reduce permutations to 1000 (quick smoke test)

Outputs (under results/mutbench/codex_wave1/):
  p1_null_per_pathogen.csv    (pathogen × null × method × statistics)
  p1_null_summary.csv         (Stouffer-aggregated global p across 12)
  p1_null_distribution.png    (12-facet histogram of null MCC w/ observed marker)
"""
from __future__ import annotations

import argparse
import math
import warnings
from multiprocessing import Pool
from pathlib import Path

import numpy as np
import pandas as pd
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from scipy import stats

warnings.filterwarnings("ignore", category=RuntimeWarning)

PROJECT_ROOT = Path(__file__).resolve().parent.parent
FEATURE_DIR = PROJECT_ROOT / "results" / "mutbench" / "feature_analysis"
OUT_DIR = PROJECT_ROOT / "results" / "mutbench" / "codex_wave1"

ALL_PATHOGENS = [
    "SARS-CoV-2", "H3N2", "Norovirus", "HIV-1", "Dengue",
    "RSV", "Influenza_B", "MERS", "HCV",
    "Zika", "Rabies", "EV-A71",
]
FEATURES = [
    "freq", "entropy", "rare_freq", "homoplasy", "esm2_llr",
    "plddt", "sasa", "grantham", "dnds_proxy", "semantic_change",
]
CORE_4 = ("freq", "entropy", "homoplasy", "plddt")
CORE_3 = ("freq", "entropy", "homoplasy")
TOP10_FRAC = 0.10
PRECISION_K = 20
WINDOW_RADIUS = 10
BLOCK_SIZE = 50
N_BURDEN_BINS = 5
RANDOM_SEED = 42
NULL_TYPES = ["iid", "circular_shift", "protein_block_shuffle", "local_burden_preserving"]


def load_data():
    data = {}
    for p in ALL_PATHOGENS:
        path = FEATURE_DIR / f"feature_matrix_{p}.csv"
        if not path.exists():
            continue
        df = pd.read_csv(path)
        if "layer_a" not in df.columns:
            continue
        y = df["layer_a"].values.astype(int)
        if y.sum() == 0 or y.sum() == len(y):
            continue
        data[p] = {"df": df, "y": y, "n": len(y), "base_rate": float(y.mean())}
    return data


def fit_signs_loo(data: dict, held_p: str, features: list[str]) -> dict[str, float]:
    """LOO sign fitting (held-out pathogen excluded)."""
    signs = {}
    for f in features:
        xs, ys = [], []
        for p, d in data.items():
            if p == held_p:
                continue
            x = np.nan_to_num(d["df"][f].values.astype(float), nan=0.0, posinf=0.0, neginf=0.0)
            y = d["y"].astype(float)
            xs.append(x)
            ys.append(y)
        x_all = np.concatenate(xs)
        y_all = np.concatenate(ys)
        if x_all.std() < 1e-12:
            signs[f] = 1.0
        else:
            r = np.corrcoef(x_all, y_all)[0, 1]
            signs[f] = -1.0 if (np.isfinite(r) and r < 0) else 1.0
    return signs


def equalweight_score(held_df: pd.DataFrame, feature_subset: tuple[str, ...],
                       signs: dict[str, float]) -> np.ndarray:
    if not feature_subset:
        return np.zeros(len(held_df))
    F = np.nan_to_num(
        held_df[list(feature_subset)].values.astype(float),
        nan=0.0, posinf=0.0, neginf=0.0,
    )
    n_feat = F.shape[1]
    Z = np.zeros_like(F)
    w = np.zeros(n_feat)
    for j, fname in enumerate(feature_subset):
        col = F[:, j] * signs.get(fname, 1.0)
        s = col.std()
        if s > 1e-10:
            Z[:, j] = (col - col.mean()) / s
            w[j] = 1.0 / n_feat
    if w.sum() < 1e-10:
        return np.zeros(len(held_df))
    w /= w.sum()
    return Z @ w


def make_prediction(scores: np.ndarray) -> np.ndarray:
    thr = np.percentile(scores, 100 * (1 - TOP10_FRAC))
    return (scores >= thr).astype(int)


def make_top_k_indicator(scores: np.ndarray, k: int) -> np.ndarray:
    n = len(scores)
    k = min(k, n)
    top_k_idx = np.argsort(-scores)[:k]
    out = np.zeros(n, dtype=int)
    out[top_k_idx] = 1
    return out


def window_dilate(y: np.ndarray, radius: int) -> np.ndarray:
    n = len(y)
    out = np.zeros(n, dtype=int)
    idx = np.where(y == 1)[0]
    for i in idx:
        lo = max(0, i - radius)
        hi = min(n, i + radius + 1)
        out[lo:hi] = 1
    return out


def vectorized_mcc(Y_batch: np.ndarray, pred: np.ndarray) -> np.ndarray:
    """Y_batch shape (B, n), pred shape (n,). Returns MCC array shape (B,)."""
    Y_batch = Y_batch.astype(np.int8)
    pred = pred.astype(np.int8)
    B, n = Y_batch.shape
    pred_pos = pred.sum()
    pred_neg = n - pred_pos
    tp = Y_batch @ pred  # shape (B,)
    fn_plus_tp = Y_batch.sum(axis=1)  # total positives per row
    tn_plus_fp = n - fn_plus_tp
    fp = pred_pos - tp
    fn = fn_plus_tp - tp
    tn = tn_plus_fp - fp
    num = tp.astype(np.float64) * tn - fp.astype(np.float64) * fn
    denom2 = (
        (tp + fp).astype(np.float64)
        * (tp + fn).astype(np.float64)
        * (tn + fp).astype(np.float64)
        * (tn + fn).astype(np.float64)
    )
    out = np.zeros(B, dtype=np.float64)
    valid = denom2 > 0
    out[valid] = num[valid] / np.sqrt(denom2[valid])
    return out


def vectorized_window_mcc(Y_batch: np.ndarray, pred: np.ndarray, radius: int) -> np.ndarray:
    """Window MCC: a TP is counted if a true positive lies within +/- radius of a
    predicted positive (and vice-versa for a true positive being detected).
    Implemented via dilated indicators per row."""
    B, n = Y_batch.shape
    out = np.zeros(B, dtype=np.float64)
    pred_dilated = window_dilate(pred, radius)
    # We need per-row dilation of Y_batch — pre-compute via cumulative-sum convolution
    kernel = np.ones(2 * radius + 1, dtype=np.int8)
    # For each row: dilate by convolution with kernel, clipped to {0,1}
    # Use scipy if available, fallback to per-row
    from scipy.signal import fftconvolve
    Y_dil = fftconvolve(Y_batch.astype(np.float32), kernel.astype(np.float32)[None, :],
                        mode="same")
    Y_dilated = (Y_dil >= 0.5).astype(np.int8)
    # Now compute window MCC:
    pred_pos_w = pred.sum()
    # tp_w = pred AND y_dilated -> count over row
    tp = (Y_dilated * pred[None, :]).sum(axis=1)
    # fp = pred AND NOT y_dilated
    fp = pred_pos_w - tp
    # fn = y AND NOT pred_dilated
    fn = (Y_batch * (1 - pred_dilated[None, :])).sum(axis=1)
    tn = n - tp - fp - fn
    num = tp.astype(np.float64) * tn - fp.astype(np.float64) * fn
    denom2 = (
        (tp + fp).astype(np.float64)
        * (tp + fn).astype(np.float64)
        * (tn + fp).astype(np.float64)
        * (tn + fn).astype(np.float64)
    )
    valid = denom2 > 0
    out[valid] = num[valid] / np.sqrt(denom2[valid])
    return out


def vectorized_precision_k(Y_batch: np.ndarray, top_k_indicator: np.ndarray) -> np.ndarray:
    """Precision@K: fraction of top-K positions that are positive in shuffled y."""
    k = int(top_k_indicator.sum())
    if k == 0:
        return np.zeros(Y_batch.shape[0])
    return (Y_batch @ top_k_indicator) / k


def vectorized_enrichment(Y_batch: np.ndarray, pred: np.ndarray) -> np.ndarray:
    """Enrichment = precision@top-10% / base_rate."""
    pred_pos = pred.sum()
    if pred_pos == 0:
        return np.zeros(Y_batch.shape[0])
    n_pos_total = Y_batch.sum(axis=1)
    base_rates = n_pos_total / Y_batch.shape[1]
    precision = (Y_batch @ pred) / pred_pos
    out = np.zeros_like(precision, dtype=np.float64)
    valid = base_rates > 1e-12
    out[valid] = precision[valid] / base_rates[valid]
    return out


def shuffle_iid(y: np.ndarray, n_perm: int, rng: np.random.Generator) -> np.ndarray:
    """Returns shape (n_perm, n) of label permutations."""
    n = len(y)
    Y = np.tile(y, (n_perm, 1))
    for i in range(n_perm):
        rng.shuffle(Y[i])
    return Y


def shuffle_circular(y: np.ndarray, n_perm: int, rng: np.random.Generator) -> np.ndarray:
    n = len(y)
    Y = np.empty((n_perm, n), dtype=y.dtype)
    offsets = rng.integers(1, n, size=n_perm)
    for i in range(n_perm):
        Y[i] = np.roll(y, offsets[i])
    return Y


def shuffle_block(y: np.ndarray, n_perm: int, rng: np.random.Generator,
                   block_size: int = BLOCK_SIZE) -> np.ndarray:
    n = len(y)
    Y = np.tile(y, (n_perm, 1))
    n_blocks = (n + block_size - 1) // block_size
    for i in range(n_perm):
        for b in range(n_blocks):
            lo = b * block_size
            hi = min(n, lo + block_size)
            block = Y[i, lo:hi].copy()
            rng.shuffle(block)
            Y[i, lo:hi] = block
    return Y


def burden_quintiles(df: pd.DataFrame, n_bins: int = N_BURDEN_BINS,
                      window: int = 5) -> np.ndarray:
    """Stratify positions into n_bins quintiles by local burden = mean(freq + entropy)
    over +/- window."""
    f = np.nan_to_num(df["freq"].values.astype(float))
    e = np.nan_to_num(df["entropy"].values.astype(float))
    burden = f + e
    n = len(burden)
    # Local mean over +/-window
    kernel = np.ones(2 * window + 1) / (2 * window + 1)
    from scipy.signal import fftconvolve
    smoothed = fftconvolve(burden, kernel, mode="same")
    # Quintile bins
    quantiles = np.percentile(smoothed, np.linspace(0, 100, n_bins + 1))
    bins = np.digitize(smoothed, quantiles[1:-1])  # 0..n_bins-1
    return bins


def shuffle_local_burden(y: np.ndarray, bins: np.ndarray, n_perm: int,
                          rng: np.random.Generator) -> np.ndarray:
    n = len(y)
    Y = np.tile(y, (n_perm, 1))
    unique_bins = np.unique(bins)
    for i in range(n_perm):
        for b in unique_bins:
            mask = bins == b
            sub = Y[i, mask].copy()
            rng.shuffle(sub)
            Y[i, mask] = sub
    return Y


def run_pathogen_null(args):
    """Worker: returns list of result dicts for one (pathogen, null_type, method) combo."""
    pathogen, null_type, method, p_data, n_perm, seed = args
    y = p_data["y"]
    df = p_data["df"]
    pred = p_data["pred"]
    top20 = p_data["top20"]
    base_rate = p_data["base_rate"]
    rng = np.random.default_rng(seed)
    if null_type == "iid":
        Y = shuffle_iid(y, n_perm, rng)
    elif null_type == "circular_shift":
        Y = shuffle_circular(y, n_perm, rng)
    elif null_type == "protein_block_shuffle":
        Y = shuffle_block(y, n_perm, rng)
    elif null_type == "local_burden_preserving":
        bins = p_data["burden_bins"]
        Y = shuffle_local_burden(y, bins, n_perm, rng)
    else:
        raise ValueError(null_type)
    null_mcc = vectorized_mcc(Y, pred)
    null_window_mcc = vectorized_window_mcc(Y, pred, WINDOW_RADIUS)
    null_p20 = vectorized_precision_k(Y, top20)
    null_enr = vectorized_enrichment(Y, pred)
    return {
        "pathogen": pathogen,
        "null_type": null_type,
        "method": method,
        "null_mcc": null_mcc,
        "null_window_mcc": null_window_mcc,
        "null_p20": null_p20,
        "null_enr": null_enr,
    }


def stouffer_one_sided(p_values: np.ndarray) -> tuple[float, float]:
    """Stouffer's combined one-sided p across pathogens (equal weights).
    Returns (combined_z, combined_p)."""
    p = np.clip(p_values, 1e-300, 1 - 1e-300)
    z = stats.norm.isf(p)  # one-sided z given p_one_sided
    z_combined = z.sum() / math.sqrt(len(z))
    p_combined = float(stats.norm.sf(z_combined))
    return float(z_combined), p_combined


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--n-perm", type=int, default=100000)
    ap.add_argument("--workers", type=int, default=1)
    ap.add_argument("--pathogen", type=str, default=None)
    ap.add_argument("--smoke", action="store_true")
    args = ap.parse_args()
    n_perm = 1000 if args.smoke else args.n_perm
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    print(f"P1 null calibration: n_perm={n_perm}, workers={args.workers}")
    print("=" * 60)
    data = load_data()
    pathogens = list(data.keys()) if args.pathogen is None else [args.pathogen]
    if args.pathogen and args.pathogen not in data:
        raise SystemExit(f"Unknown pathogen {args.pathogen}")
    print(f"Pathogens: {pathogens}")

    # Pre-compute per-pathogen scores, predictions, observed metrics, burden bins
    p_data_cache = {}
    obs_rows = []
    for p in pathogens:
        d = data[p]
        signs = fit_signs_loo(data, p, FEATURES)
        for method, subset in [("4-core", CORE_4), ("3-core", CORE_3)]:
            scores = equalweight_score(d["df"], subset, signs)
            pred = make_prediction(scores)
            top20 = make_top_k_indicator(scores, PRECISION_K)
            burden_bins = burden_quintiles(d["df"])
            cache_key = (p, method)
            p_data_cache[cache_key] = {
                "y": d["y"], "df": d["df"], "pred": pred, "top20": top20,
                "base_rate": d["base_rate"], "burden_bins": burden_bins,
            }
            # Observed metrics
            obs_mcc = float(vectorized_mcc(d["y"][None, :], pred)[0])
            obs_wmcc = float(vectorized_window_mcc(d["y"][None, :], pred, WINDOW_RADIUS)[0])
            obs_p20 = float(vectorized_precision_k(d["y"][None, :], top20)[0])
            obs_enr = float(vectorized_enrichment(d["y"][None, :], pred)[0])
            obs_rows.append({
                "pathogen": p, "method": method,
                "obs_mcc": obs_mcc, "obs_window_mcc": obs_wmcc,
                "obs_p20": obs_p20, "obs_enrichment": obs_enr,
                "n": d["n"], "base_rate": d["base_rate"], "n_pos": int(d["y"].sum()),
            })
    obs_df = pd.DataFrame(obs_rows)
    print("\nObserved metrics:")
    print(obs_df.to_string(index=False))

    # Build worker args
    jobs = []
    for p in pathogens:
        for method in ["4-core", "3-core"]:
            for null_type in NULL_TYPES:
                seed = abs(hash((p, method, null_type, RANDOM_SEED))) % (2**32)
                jobs.append((p, null_type, method, p_data_cache[(p, method)], n_perm, seed))

    print(f"\nRunning {len(jobs)} (pathogen × null × method) jobs with n_perm={n_perm}...")
    if args.workers <= 1:
        results = [run_pathogen_null(j) for j in jobs]
    else:
        with Pool(args.workers) as pool:
            results = pool.map(run_pathogen_null, jobs)

    # Aggregate per-pathogen rows
    rows = []
    for r in results:
        p, null_type, method = r["pathogen"], r["null_type"], r["method"]
        obs = obs_df[(obs_df["pathogen"] == p) & (obs_df["method"] == method)].iloc[0]
        for metric_key, null_arr, obs_val in [
            ("mcc", r["null_mcc"], obs["obs_mcc"]),
            ("window_mcc", r["null_window_mcc"], obs["obs_window_mcc"]),
            ("p20", r["null_p20"], obs["obs_p20"]),
            ("enrichment", r["null_enr"], obs["obs_enrichment"]),
        ]:
            null_mean = float(np.mean(null_arr))
            null_sd = float(np.std(null_arr))
            # one-sided above-null p
            p_one = float((null_arr >= obs_val).mean())
            p_one = max(p_one, 1.0 / (n_perm + 1))  # avoid 0 for Stouffer
            # two-sided sensitivity
            abs_obs = abs(obs_val - null_mean)
            p_two = float((np.abs(null_arr - null_mean) >= abs_obs).mean())
            p_two = max(p_two, 1.0 / (n_perm + 1))
            percentile = float((null_arr <= obs_val).mean() * 100)
            rows.append({
                "pathogen": p,
                "null_type": null_type,
                "method": method,
                "metric": metric_key,
                "observed": obs_val,
                "null_mean": null_mean,
                "null_sd": null_sd,
                "observed_percentile": percentile,
                "p_one_sided_primary": p_one,
                "p_two_sided_sensitivity": p_two,
                "n_perm": n_perm,
            })

    per_path_df = pd.DataFrame(rows)
    per_path_df.to_csv(OUT_DIR / "p1_null_per_pathogen.csv", index=False)

    # Stouffer aggregation across pathogens (one-sided primary)
    summary_rows = []
    for method in per_path_df["method"].unique():
        for null_type in NULL_TYPES:
            for metric in ["mcc", "window_mcc", "p20", "enrichment"]:
                sub = per_path_df[(per_path_df["null_type"] == null_type) &
                                  (per_path_df["method"] == method) &
                                  (per_path_df["metric"] == metric)]
                if sub.empty:
                    continue
                p_vals = sub["p_one_sided_primary"].values
                z_combined, p_combined = stouffer_one_sided(p_vals)
                n_above = int((p_vals < 0.05).sum())
                summary_rows.append({
                    "method": method,
                    "null_type": null_type,
                    "metric": metric,
                    "n_pathogens": len(p_vals),
                    "n_significant_at_0.05_one_sided": n_above,
                    "stouffer_z_one_sided": z_combined,
                    "stouffer_p_one_sided": p_combined,
                    "min_p_one_sided": float(p_vals.min()),
                    "max_p_one_sided": float(p_vals.max()),
                })
    summary_df = pd.DataFrame(summary_rows)
    summary_df.to_csv(OUT_DIR / "p1_null_summary.csv", index=False)

    # Print headline
    print("\n=== P1 Stouffer one-sided p (primary) for MCC ===")
    headline = summary_df[summary_df["metric"] == "mcc"].copy()
    print(headline.to_string(index=False))

    # HARD STOP gate check (codex review Q5): iid Stouffer one-sided p > 0.05 globally
    iid_4core_mcc = summary_df[(summary_df["method"] == "4-core") &
                                (summary_df["null_type"] == "iid") &
                                (summary_df["metric"] == "mcc")].iloc[0]
    print(f"\n=== HARD STOP gate: 4-core MCC iid one-sided Stouffer p ===")
    print(f"  Stouffer p = {iid_4core_mcc['stouffer_p_one_sided']:.4f}")
    if iid_4core_mcc["stouffer_p_one_sided"] > 0.05:
        print("  TRIGGER: HARD STOP — apply P1 failure-mode branch before Task 5.")
    else:
        print("  PASS — Wave 1 may proceed to Task 5 (P4 detector consensus).")

    # Distribution figure
    print("\nGenerating null distribution figure (4-core MCC)...")
    fig, axes = plt.subplots(3, 4, figsize=(15, 9), sharex=False)
    for ax, p in zip(axes.flat, pathogens):
        for null_type, color in [("iid", "lightcoral"),
                                   ("circular_shift", "lightblue"),
                                   ("protein_block_shuffle", "lightgreen"),
                                   ("local_burden_preserving", "khaki")]:
            j = next((j for j in results if j["pathogen"] == p
                      and j["null_type"] == null_type and j["method"] == "4-core"), None)
            if j is None:
                continue
            ax.hist(j["null_mcc"], bins=40, alpha=0.45, color=color, label=null_type)
        obs = obs_df[(obs_df["pathogen"] == p) & (obs_df["method"] == "4-core")]["obs_mcc"].iloc[0]
        ax.axvline(obs, color="red", lw=2, label=f"observed={obs:.3f}")
        ax.set_title(p, fontsize=10)
    axes[0, 0].legend(fontsize=7, loc="upper left")
    fig.suptitle("P1: 4-core MCC null distributions vs observed (red)", fontsize=12)
    fig.tight_layout()
    fig.savefig(OUT_DIR / "p1_null_distribution.png", dpi=150)
    print(f"\nDone. Outputs: {OUT_DIR}/p1_null_*")


if __name__ == "__main__":
    main()
