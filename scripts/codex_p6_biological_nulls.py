#!/usr/bin/env python3
"""P6: Biologically-realistic local nulls extending P1.

Reuses P1's vectorized batched-numpy MCC, +/-10-window MCC, top-20
precision, and enrichment helpers. Adds four new null types that
shuffle Layer A labels within strata defined by biological structure:

  P6.1 SASA-stratified:        5 quintiles of `sasa` column
  P6.2 pLDDT-stratified:       5 quintiles of `plddt` column
  P6.3 SASA x freq joint:      3 x 3 = 9 cells
  P6.4 pLDDT x entropy joint:  3 x 3 = 9 cells

Per codex Wave 3 review §Q3: zero-positive cells are NOT failures.
Stratum-preserving shuffling means: shuffle labels WITHIN each cell;
cells with no labels to move (e.g., all 0s) just stay as-is. A
(pathogen, null) pair is DEGENERATE iff:
  (a) <2 strata contain BOTH positives AND negatives, OR
  (b) <5 total movable positives, OR
  (c) near-zero null variance (numerical degeneracy)
Degenerate pairs are reported with `degenerate_null=True`,
`skip_reason=<diag>`, and excluded from Stouffer aggregation.

p-values use (b+1)/(n_perm+1) smoothing per codex Q8.

Outputs:
  results/mutbench/codex_wave3/p6_null_per_pathogen.csv
  results/mutbench/codex_wave3/p6_null_summary.csv
  results/mutbench/codex_wave3/p6_null_distribution.png
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
from scipy.signal import fftconvolve

warnings.filterwarnings("ignore", category=RuntimeWarning)

PROJECT_ROOT = Path(__file__).resolve().parent.parent
FEATURE_DIR = PROJECT_ROOT / "results" / "mutbench" / "feature_analysis"
OUT_DIR = PROJECT_ROOT / "results" / "mutbench" / "codex_wave3"

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
RANDOM_SEED = 42
NULL_TYPES = ["sasa_strat", "plddt_strat", "sasa_freq_joint", "plddt_ent_joint"]
N_QUINTILES = 5
N_TERTILES = 3
DEGEN_MIN_BOTH_POS_NEG_STRATA = 2
DEGEN_MIN_MOVABLE_POS = 5
DEGEN_NULL_SD_FLOOR = 1e-8


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


def fit_signs_loo(data, held_p, features):
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


def equalweight_score(held_df, feature_subset, signs):
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


def make_prediction(scores):
    thr = np.percentile(scores, 100 * (1 - TOP10_FRAC))
    return (scores >= thr).astype(int)


def make_top_k_indicator(scores, k):
    n = len(scores)
    k = min(k, n)
    out = np.zeros(n, dtype=int)
    out[np.argsort(-scores)[:k]] = 1
    return out


def window_dilate(y, radius):
    n = len(y)
    out = np.zeros(n, dtype=int)
    idx = np.where(y == 1)[0]
    for i in idx:
        lo = max(0, i - radius)
        hi = min(n, i + radius + 1)
        out[lo:hi] = 1
    return out


def vectorized_mcc(Y_batch, pred):
    Y_batch = Y_batch.astype(np.int8)
    pred = pred.astype(np.int8)
    B, n = Y_batch.shape
    pred_pos = pred.sum()
    tp = Y_batch @ pred
    fn_plus_tp = Y_batch.sum(axis=1)
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


def vectorized_window_mcc(Y_batch, pred, radius):
    B, n = Y_batch.shape
    out = np.zeros(B, dtype=np.float64)
    pred_dilated = window_dilate(pred, radius)
    kernel = np.ones(2 * radius + 1, dtype=np.int8)
    Y_dil = fftconvolve(Y_batch.astype(np.float32), kernel.astype(np.float32)[None, :], mode="same")
    Y_dilated = (Y_dil >= 0.5).astype(np.int8)
    pred_pos_w = pred.sum()
    tp = (Y_dilated * pred[None, :]).sum(axis=1)
    fp = pred_pos_w - tp
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


def vectorized_precision_k(Y_batch, top_k_indicator):
    k = int(top_k_indicator.sum())
    if k == 0:
        return np.zeros(Y_batch.shape[0])
    return (Y_batch @ top_k_indicator) / k


def vectorized_enrichment(Y_batch, pred):
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


def quintile_bins(values, n_bins):
    """Return integer bin indices 0..n_bins-1 by equal-frequency quantile."""
    valid = np.isfinite(values)
    if valid.sum() < n_bins:
        return np.zeros(len(values), dtype=int)
    quantiles = np.percentile(values[valid], np.linspace(0, 100, n_bins + 1))
    bins = np.digitize(values, quantiles[1:-1])
    bins = np.clip(bins, 0, n_bins - 1)
    return bins


def compute_strata(df, null_type):
    """Return per-position stratum index for a given null type."""
    if null_type == "sasa_strat":
        sasa = np.nan_to_num(df["sasa"].values.astype(float), nan=0.0)
        return quintile_bins(sasa, N_QUINTILES)
    if null_type == "plddt_strat":
        plddt = np.nan_to_num(df["plddt"].values.astype(float), nan=0.0)
        return quintile_bins(plddt, N_QUINTILES)
    if null_type == "sasa_freq_joint":
        sasa = np.nan_to_num(df["sasa"].values.astype(float), nan=0.0)
        freq = np.nan_to_num(df["freq"].values.astype(float), nan=0.0)
        s_bin = quintile_bins(sasa, N_TERTILES)
        f_bin = quintile_bins(freq, N_TERTILES)
        return s_bin * N_TERTILES + f_bin  # 0..8
    if null_type == "plddt_ent_joint":
        plddt = np.nan_to_num(df["plddt"].values.astype(float), nan=0.0)
        ent = np.nan_to_num(df["entropy"].values.astype(float), nan=0.0)
        p_bin = quintile_bins(plddt, N_TERTILES)
        e_bin = quintile_bins(ent, N_TERTILES)
        return p_bin * N_TERTILES + e_bin
    raise ValueError(null_type)


def check_degenerate(y, strata):
    """Returns (is_degenerate: bool, reason: str)."""
    unique_strata = np.unique(strata)
    n_with_both = 0
    n_movable_pos = 0
    for s in unique_strata:
        mask = strata == s
        n_pos = int(y[mask].sum())
        n_neg = int(mask.sum() - n_pos)
        if n_pos > 0 and n_neg > 0:
            n_with_both += 1
            n_movable_pos += n_pos
    if n_with_both < DEGEN_MIN_BOTH_POS_NEG_STRATA:
        return True, f"<{DEGEN_MIN_BOTH_POS_NEG_STRATA} strata with both pos and neg ({n_with_both} found)"
    if n_movable_pos < DEGEN_MIN_MOVABLE_POS:
        return True, f"<{DEGEN_MIN_MOVABLE_POS} movable positives ({n_movable_pos} found)"
    return False, ""


def shuffle_within_strata(y, strata, n_perm, rng):
    """Shuffle labels within each stratum cell. Cells with all-same labels are
    naturally invariant under shuffling. Returns shape (n_perm, n) array."""
    n = len(y)
    Y = np.tile(y, (n_perm, 1))
    unique_strata = np.unique(strata)
    cell_indices = {s: np.where(strata == s)[0] for s in unique_strata}
    for i in range(n_perm):
        for s in unique_strata:
            idx = cell_indices[s]
            if len(idx) > 1:
                sub = Y[i, idx].copy()
                rng.shuffle(sub)
                Y[i, idx] = sub
    return Y


def smoothed_p(observed, null_arr, n_perm, side="upper"):
    """(b+1)/(n_perm+1) smoothed p-value."""
    if side == "upper":
        b = int((null_arr >= observed).sum())
    elif side == "two":
        null_mean = null_arr.mean()
        b = int((np.abs(null_arr - null_mean) >= abs(observed - null_mean)).sum())
    else:
        raise ValueError(side)
    return (b + 1) / (n_perm + 1)


def run_pathogen_null(args):
    pathogen, null_type, method, p_data, n_perm, seed = args
    y = p_data["y"]
    pred = p_data["pred"]
    top20 = p_data["top20"]
    rng = np.random.default_rng(seed)
    strata = p_data[f"strata_{null_type}"]
    is_degen, reason = check_degenerate(y, strata)
    if is_degen:
        return {
            "pathogen": pathogen, "null_type": null_type, "method": method,
            "degenerate_null": True, "skip_reason": reason,
            "null_mcc": np.array([]), "null_window_mcc": np.array([]),
            "null_p20": np.array([]), "null_enr": np.array([]),
        }
    Y = shuffle_within_strata(y, strata, n_perm, rng)
    null_mcc = vectorized_mcc(Y, pred)
    null_window_mcc = vectorized_window_mcc(Y, pred, WINDOW_RADIUS)
    null_p20 = vectorized_precision_k(Y, top20)
    null_enr = vectorized_enrichment(Y, pred)
    if null_mcc.std() < DEGEN_NULL_SD_FLOOR:
        return {
            "pathogen": pathogen, "null_type": null_type, "method": method,
            "degenerate_null": True, "skip_reason": f"near-zero null SD ({null_mcc.std():.2e})",
            "null_mcc": null_mcc, "null_window_mcc": null_window_mcc,
            "null_p20": null_p20, "null_enr": null_enr,
        }
    return {
        "pathogen": pathogen, "null_type": null_type, "method": method,
        "degenerate_null": False, "skip_reason": "",
        "null_mcc": null_mcc, "null_window_mcc": null_window_mcc,
        "null_p20": null_p20, "null_enr": null_enr,
    }


def stouffer_one_sided(p_values):
    """Stouffer combined one-sided p across pathogens."""
    if len(p_values) == 0:
        return float("nan"), float("nan")
    p = np.clip(p_values, 1e-300, 1 - 1e-300)
    z = stats.norm.isf(p)
    z_combined = z.sum() / math.sqrt(len(z))
    return float(z_combined), float(stats.norm.sf(z_combined))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--n-perm", type=int, default=100000)
    ap.add_argument("--workers", type=int, default=1)
    ap.add_argument("--pathogen", type=str, default=None)
    ap.add_argument("--smoke", action="store_true")
    args = ap.parse_args()
    n_perm = 1000 if args.smoke else args.n_perm
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    print(f"P6 biological-realistic local nulls: n_perm={n_perm}, workers={args.workers}")
    print("=" * 66)
    data = load_data()
    pathogens = list(data.keys()) if args.pathogen is None else [args.pathogen]
    print(f"Pathogens: {pathogens}")

    p_data_cache = {}
    obs_rows = []
    for p in pathogens:
        d = data[p]
        signs = fit_signs_loo(data, p, FEATURES)
        for method, subset in [("4-core", CORE_4), ("3-core", CORE_3)]:
            scores = equalweight_score(d["df"], subset, signs)
            pred = make_prediction(scores)
            top20 = make_top_k_indicator(scores, PRECISION_K)
            cache = {
                "y": d["y"], "df": d["df"], "pred": pred, "top20": top20,
                "base_rate": d["base_rate"],
            }
            for nt in NULL_TYPES:
                cache[f"strata_{nt}"] = compute_strata(d["df"], nt)
            p_data_cache[(p, method)] = cache
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

    jobs = []
    for p in pathogens:
        for method in ["4-core", "3-core"]:
            for null_type in NULL_TYPES:
                seed = abs(hash((p, method, null_type, RANDOM_SEED))) % (2**32)
                jobs.append((p, null_type, method, p_data_cache[(p, method)], n_perm, seed))
    print(f"\nRunning {len(jobs)} jobs (n_perm={n_perm})...")

    if args.workers <= 1:
        results = [run_pathogen_null(j) for j in jobs]
    else:
        with Pool(args.workers) as pool:
            results = pool.map(run_pathogen_null, jobs)

    rows = []
    for r in results:
        p, null_type, method = r["pathogen"], r["null_type"], r["method"]
        obs = obs_df[(obs_df["pathogen"] == p) & (obs_df["method"] == method)].iloc[0]
        if r["degenerate_null"] and len(r["null_mcc"]) == 0:
            for metric_key, obs_val in [("mcc", obs["obs_mcc"]), ("window_mcc", obs["obs_window_mcc"]),
                                          ("p20", obs["obs_p20"]), ("enrichment", obs["obs_enrichment"])]:
                rows.append({
                    "pathogen": p, "null_type": null_type, "method": method,
                    "metric": metric_key, "observed": obs_val,
                    "null_mean": float("nan"), "null_sd": float("nan"),
                    "observed_percentile": float("nan"),
                    "p_one_sided_primary": float("nan"),
                    "p_two_sided_sensitivity": float("nan"),
                    "n_perm": n_perm, "n_valid": 0,
                    "degenerate_null": True, "skip_reason": r["skip_reason"],
                })
            continue
        for metric_key, null_arr, obs_val in [
            ("mcc", r["null_mcc"], obs["obs_mcc"]),
            ("window_mcc", r["null_window_mcc"], obs["obs_window_mcc"]),
            ("p20", r["null_p20"], obs["obs_p20"]),
            ("enrichment", r["null_enr"], obs["obs_enrichment"]),
        ]:
            if r["degenerate_null"]:
                p_one = float("nan")
                p_two = float("nan")
                percentile = float("nan")
                null_mean = float(np.mean(null_arr))
                null_sd = float(np.std(null_arr))
                rows.append({
                    "pathogen": p, "null_type": null_type, "method": method,
                    "metric": metric_key, "observed": obs_val,
                    "null_mean": null_mean, "null_sd": null_sd,
                    "observed_percentile": percentile,
                    "p_one_sided_primary": p_one,
                    "p_two_sided_sensitivity": p_two,
                    "n_perm": n_perm, "n_valid": 0,
                    "degenerate_null": True, "skip_reason": r["skip_reason"],
                })
                continue
            null_mean = float(np.mean(null_arr))
            null_sd = float(np.std(null_arr))
            p_one = smoothed_p(obs_val, null_arr, n_perm, side="upper")
            p_two = smoothed_p(obs_val, null_arr, n_perm, side="two")
            percentile = float((null_arr <= obs_val).mean() * 100)
            rows.append({
                "pathogen": p, "null_type": null_type, "method": method,
                "metric": metric_key, "observed": obs_val,
                "null_mean": null_mean, "null_sd": null_sd,
                "observed_percentile": percentile,
                "p_one_sided_primary": p_one,
                "p_two_sided_sensitivity": p_two,
                "n_perm": n_perm, "n_valid": 1,
                "degenerate_null": False, "skip_reason": "",
            })
    per_path_df = pd.DataFrame(rows)
    per_path_df.to_csv(OUT_DIR / "p6_null_per_pathogen.csv", index=False)

    # Stouffer aggregation
    summary_rows = []
    for method in per_path_df["method"].unique():
        for null_type in NULL_TYPES:
            for metric in ["mcc", "window_mcc", "p20", "enrichment"]:
                sub = per_path_df[
                    (per_path_df["null_type"] == null_type)
                    & (per_path_df["method"] == method)
                    & (per_path_df["metric"] == metric)
                    & (~per_path_df["degenerate_null"])
                ]
                if sub.empty:
                    continue
                p_vals = sub["p_one_sided_primary"].values
                z_combined, p_combined = stouffer_one_sided(p_vals)
                n_above = int((p_vals < 0.05).sum())
                summary_rows.append({
                    "method": method, "null_type": null_type, "metric": metric,
                    "n_pathogens_valid": len(p_vals),
                    "n_pathogens_total": 12,
                    "n_significant_at_0.05_one_sided": n_above,
                    "stouffer_z_one_sided": z_combined,
                    "stouffer_p_one_sided": p_combined,
                    "min_p_one_sided": float(p_vals.min()) if len(p_vals) else float("nan"),
                    "max_p_one_sided": float(p_vals.max()) if len(p_vals) else float("nan"),
                })
    summary_df = pd.DataFrame(summary_rows)
    summary_df.to_csv(OUT_DIR / "p6_null_summary.csv", index=False)

    # Headlines per codex Q5
    print("\n=== Per-null counts of individually significant pathogens (4-core MCC, p<0.05 one-sided) ===")
    for nt in NULL_TYPES:
        sub = per_path_df[
            (per_path_df["null_type"] == nt) & (per_path_df["method"] == "4-core")
            & (per_path_df["metric"] == "mcc") & (~per_path_df["degenerate_null"])
        ]
        n_sig = int((sub["p_one_sided_primary"] < 0.05).sum())
        n_valid = len(sub)
        sig_paths = sub[sub["p_one_sided_primary"] < 0.05]["pathogen"].tolist()
        print(f"  {nt:25s}: {n_sig}/{n_valid} valid (12 total) — {sig_paths}")

    print("\n=== Per-null counts (3-core MCC, p<0.05 one-sided) ===")
    for nt in NULL_TYPES:
        sub = per_path_df[
            (per_path_df["null_type"] == nt) & (per_path_df["method"] == "3-core")
            & (per_path_df["metric"] == "mcc") & (~per_path_df["degenerate_null"])
        ]
        n_sig = int((sub["p_one_sided_primary"] < 0.05).sum())
        n_valid = len(sub)
        sig_paths = sub[sub["p_one_sided_primary"] < 0.05]["pathogen"].tolist()
        print(f"  {nt:25s}: {n_sig}/{n_valid} valid (12 total) — {sig_paths}")

    print("\n=== Norovirus survival across all four P6 nulls (4-core MCC, p<0.05 one-sided) ===")
    nor4 = per_path_df[(per_path_df["pathogen"] == "Norovirus") & (per_path_df["method"] == "4-core")
                        & (per_path_df["metric"] == "mcc")]
    surv4 = int((nor4["p_one_sided_primary"] < 0.05).sum())
    print(f"  4-core MCC: {surv4}/4 nulls passed")
    for _, r in nor4.iterrows():
        flag = "*" if r["p_one_sided_primary"] < 0.05 else " "
        print(f"    {flag} {r['null_type']:25s} p={r['p_one_sided_primary']:.5f} (degen={r['degenerate_null']})")

    nor3 = per_path_df[(per_path_df["pathogen"] == "Norovirus") & (per_path_df["method"] == "3-core")
                        & (per_path_df["metric"] == "mcc")]
    surv3 = int((nor3["p_one_sided_primary"] < 0.05).sum())
    print(f"  3-core MCC: {surv3}/4 nulls passed")

    # Distribution figure
    fig, axes = plt.subplots(3, 4, figsize=(16, 10), sharex=False)
    for ax, p in zip(axes.flat, pathogens):
        for nt, color in [("sasa_strat", "lightcoral"), ("plddt_strat", "lightblue"),
                           ("sasa_freq_joint", "lightgreen"), ("plddt_ent_joint", "khaki")]:
            j = next((j for j in results if j["pathogen"] == p
                      and j["null_type"] == nt and j["method"] == "4-core"), None)
            if j is None or j.get("degenerate_null") and len(j["null_mcc"]) == 0:
                continue
            ax.hist(j["null_mcc"], bins=40, alpha=0.45, color=color, label=nt)
        obs = obs_df[(obs_df["pathogen"] == p) & (obs_df["method"] == "4-core")]["obs_mcc"].iloc[0]
        ax.axvline(obs, color="red", lw=2, label=f"obs={obs:.3f}")
        ax.set_title(p, fontsize=10)
    axes[0, 0].legend(fontsize=7, loc="upper left")
    fig.suptitle("P6: 4-core MCC under biologically-realistic local nulls vs observed (red)", fontsize=12)
    fig.tight_layout()
    fig.savefig(OUT_DIR / "p6_null_distribution.png", dpi=150)
    print(f"\nDone. Outputs: {OUT_DIR}/p6_null_*")


if __name__ == "__main__":
    main()
