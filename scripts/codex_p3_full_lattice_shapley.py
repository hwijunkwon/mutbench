#!/usr/bin/env python3
"""P3: Full 2^10 - 1 = 1023 subset lattice + formal Shapley decomposition.

Extends subset_selection_robustness_210combos.csv (4-of-10 only) to all
non-empty subsets of the 10 features. Uses the SAME nested-LOPO
mechanics as feature_ablation_nested_lopo.py (sign by training-set
Pearson, z-score within held-out, top-X% threshold, safe_mcc).

Per-subset metrics (each as fold-mean):
  - mean_mcc            (top-10% MCC, headline)
  - mean_mcc_top20      (top-20% MCC)
  - mean_mcc_window10   (+/-10-window MCC at top-10%)
  - mean_precision20    (precision@top-20 fixed-count calls)
  - mean_enrichment     (precision / pathogen base rate at top-10%)
  - wins_vs_full10      (count of folds where subset MCC >= full-10 MCC)

Formal Shapley:
  phi_f = (1/n) * sum_{k=0..n-1} (1/C(n-1,k)) * mean_{|S|=k, S not in f}[v(SU{f}) - v(S)]
  with v(empty) = 0. Computed for both MCC and enrichment via frozenset
  lookup (NOT the unweighted-mean-marginal proxy).

Outputs (under results/mutbench/codex_wave1/):
  p3_full_lattice_1023.csv
  p3_shapley.csv
  p3_per_pathogen_wins.csv
  p3_pareto_frontier.png
"""
from __future__ import annotations

import itertools
import math
import sys
import warnings
from pathlib import Path

import numpy as np
import pandas as pd
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from sklearn.metrics import matthews_corrcoef

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
CORE_4 = ("freq", "entropy", "homoplasy", "plddt")  # canonical 4-core (matches existing CSVs)
TOP10_FRAC = 0.10
TOP20_FRAC = 0.20
PRECISION_K = 20
WINDOW_RADIUS = 10
RANDOM_SEED = 42


def safe_mcc(y_true: np.ndarray, y_pred: np.ndarray) -> float:
    y_true = np.asarray(y_true, dtype=int)
    y_pred = np.asarray(y_pred, dtype=int)
    if y_pred.sum() == 0 or y_pred.sum() == len(y_pred):
        return 0.0
    if y_true.sum() == 0 or y_true.sum() == len(y_true):
        return 0.0
    return float(matthews_corrcoef(y_true, y_pred))


def window_mcc(y_true: np.ndarray, y_pred: np.ndarray, radius: int) -> float:
    """+/-radius-window MCC: a predicted positive at i counts as TP if any
    true positive lies within +/-radius of i, and a true positive counts as
    detected if any predicted positive lies within +/-radius of it."""
    y_true = np.asarray(y_true, dtype=int)
    y_pred = np.asarray(y_pred, dtype=int)
    n = len(y_true)
    if y_pred.sum() == 0 or y_pred.sum() == n or y_true.sum() == 0 or y_true.sum() == n:
        return 0.0
    # build dilated indicators
    def dilate(v: np.ndarray) -> np.ndarray:
        idx = np.where(v == 1)[0]
        out = np.zeros(n, dtype=int)
        for i in idx:
            lo = max(0, i - radius)
            hi = min(n, i + radius + 1)
            out[lo:hi] = 1
        return out
    pred_window = dilate(y_pred)
    true_window = dilate(y_true)
    tp = int(((y_pred == 1) & (true_window == 1)).sum())
    fp = int(((y_pred == 1) & (true_window == 0)).sum())
    fn = int(((y_true == 1) & (pred_window == 0)).sum())
    tn = int(((y_pred == 0) & (y_true == 0)).sum())
    denom = math.sqrt(float(tp + fp) * float(tp + fn) * float(tn + fp) * float(tn + fn))
    if denom < 1e-12:
        return 0.0
    return float((tp * tn - fp * fn) / denom)


def load_data():
    data = {}
    for p in ALL_PATHOGENS:
        path = FEATURE_DIR / f"feature_matrix_{p}.csv"
        if not path.exists():
            print(f"  [WARN] {p}: no feature matrix at {path}, skip")
            continue
        df = pd.read_csv(path)
        if "layer_a" not in df.columns:
            print(f"  [WARN] {p}: no layer_a column, skip")
            continue
        y = df["layer_a"].values.astype(int)
        if y.sum() == 0 or y.sum() == len(y):
            print(f"  [WARN] {p}: degenerate Layer A (sum={y.sum()}, n={len(y)}), skip")
            continue
        data[p] = {"df": df, "y": y, "n": len(y), "base_rate": y.mean()}
    print(f"Loaded {len(data)} pathogens with valid Layer A: {list(data.keys())}")
    return data


def fit_signs(training_data: dict, features: list[str]) -> dict[str, float]:
    """Per-feature directional sign s_f in {-1, +1}, fit by Pearson correlation
    on concatenated training data. Identical to feature_ablation_nested_lopo.py."""
    signs = {}
    for f in features:
        xs, ys = [], []
        for p, d in training_data.items():
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
    """Apply training-fit signs, z-score per feature within held-out, uniform mean.
    Returns the per-position score array."""
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


def evaluate_subset(scores: np.ndarray, y: np.ndarray, base_rate: float):
    """Compute (mcc_top10, mcc_top20, mcc_window10, precision20, enrichment)."""
    n = len(scores)
    # top-10%
    thr10 = np.percentile(scores, 100 * (1 - TOP10_FRAC))
    pred10 = (scores >= thr10).astype(int)
    mcc10 = safe_mcc(y, pred10)
    # top-20%
    thr20 = np.percentile(scores, 100 * (1 - TOP20_FRAC))
    pred20 = (scores >= thr20).astype(int)
    mcc20 = safe_mcc(y, pred20)
    # window-10 MCC at top-10%
    mcc_w = window_mcc(y, pred10, WINDOW_RADIUS)
    # precision@K (fixed count)
    k = min(PRECISION_K, n)
    top_k_idx = np.argsort(-scores)[:k]
    precision_k = float(y[top_k_idx].mean()) if k > 0 else 0.0
    # enrichment at top-10% = precision / base_rate
    if pred10.sum() > 0:
        precision10 = float(y[pred10 == 1].mean())
        enrichment = precision10 / base_rate if base_rate > 1e-12 else 0.0
    else:
        enrichment = 0.0
    return mcc10, mcc20, mcc_w, precision_k, enrichment


def aggregate_subset(data: dict, subset: tuple[str, ...],
                      signs_per_fold: dict[str, dict[str, float]]) -> dict:
    """LOPO over all pathogens; aggregate per-fold metrics."""
    fold_metrics = {p: {} for p in data}
    for held in data:
        signs = signs_per_fold[held]
        d = data[held]
        scores = equalweight_score(d["df"], subset, signs)
        m10, m20, mw, p20, enr = evaluate_subset(scores, d["y"], d["base_rate"])
        fold_metrics[held] = {
            "mcc": m10, "mcc20": m20, "mcc_window10": mw,
            "precision20": p20, "enrichment": enr,
        }
    return fold_metrics


def main():
    print("MutBench P3: Full 2^10 lattice + formal Shapley")
    print("=" * 60)
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    data = load_data()
    if not data:
        print("No usable pathogens.")
        sys.exit(1)
    pathogens = list(data.keys())

    # Pre-compute signs once per fold (depends only on training set, not subset)
    print("\nFitting signs per fold (10 features × 12 folds = 120)...")
    signs_per_fold: dict[str, dict[str, float]] = {}
    for held in pathogens:
        training = {k: v for k, v in data.items() if k != held}
        signs_per_fold[held] = fit_signs(training, FEATURES)

    # Full-10 baseline
    print("\nComputing full-10 baseline...")
    full10_folds = aggregate_subset(data, tuple(FEATURES), signs_per_fold)
    full10_mcc_per_fold = {p: full10_folds[p]["mcc"] for p in pathogens}
    full10_mean_mcc = float(np.mean([full10_mcc_per_fold[p] for p in pathogens]))
    full10_mean_enr = float(np.mean([full10_folds[p]["enrichment"] for p in pathogens]))
    print(f"  Full-10 mean MCC: {full10_mean_mcc:.6f}")
    print(f"  Full-10 mean enrichment: {full10_mean_enr:.6f}")

    # Enumerate all 2^10 - 1 = 1023 non-empty subsets
    n_total = sum(math.comb(10, k) for k in range(1, 11))
    assert n_total == 1023
    print(f"\nEnumerating {n_total} subsets...")

    rows = []
    per_pathogen_wins_rows = []
    lookup: dict[frozenset, dict] = {}  # for Shapley

    idx = 0
    for k in range(1, 11):
        for combo in itertools.combinations(FEATURES, k):
            idx += 1
            fold_metrics = aggregate_subset(data, combo, signs_per_fold)
            mcc_arr = np.array([fold_metrics[p]["mcc"] for p in pathogens])
            mcc20_arr = np.array([fold_metrics[p]["mcc20"] for p in pathogens])
            mw_arr = np.array([fold_metrics[p]["mcc_window10"] for p in pathogens])
            p20_arr = np.array([fold_metrics[p]["precision20"] for p in pathogens])
            enr_arr = np.array([fold_metrics[p]["enrichment"] for p in pathogens])
            # wins vs full-10 (per fold)
            wins = int(sum(1 for p in pathogens if fold_metrics[p]["mcc"] >= full10_mcc_per_fold[p]))
            row = {
                "combo_id": idx,
                "k": k,
                "features": ",".join(combo),  # combo is in FEATURES order
                "mean_mcc": float(mcc_arr.mean()),
                "mean_mcc_top20": float(mcc20_arr.mean()),
                "mean_mcc_window10": float(mw_arr.mean()),
                "mean_precision20": float(p20_arr.mean()),
                "mean_enrichment": float(enr_arr.mean()),
                "wins_vs_full10": wins,
                "delta_mcc_vs_full10": float(mcc_arr.mean()) - full10_mean_mcc,
                "is_core_4": frozenset(combo) == frozenset(CORE_4),
            }
            rows.append(row)
            lookup[frozenset(combo)] = row
            # per-pathogen wins for diagnostic
            for p in pathogens:
                per_pathogen_wins_rows.append({
                    "combo_id": idx, "k": k, "features": ",".join(combo),
                    "pathogen": p,
                    "mcc": fold_metrics[p]["mcc"],
                    "full10_mcc": full10_mcc_per_fold[p],
                    "win": int(fold_metrics[p]["mcc"] >= full10_mcc_per_fold[p]),
                })
            if idx % 100 == 0:
                print(f"  {idx}/{n_total} ...")

    df = pd.DataFrame(rows)
    df.to_csv(OUT_DIR / "p3_full_lattice_1023.csv", index=False)
    pp_df = pd.DataFrame(per_pathogen_wins_rows)
    pp_df.to_csv(OUT_DIR / "p3_per_pathogen_wins.csv", index=False)

    # Formal Shapley with binomial weights
    n = len(FEATURES)
    print(f"\nComputing formal Shapley over {n} features (v(empty)=0)...")

    def shapley_for(metric_key: str, full_metric_value: float) -> dict[str, float]:
        """Formal Shapley: phi_f = (1/n) * sum_k mean_{|S|=k, S not in f}[v(SU{f}) - v(S)]
        (C(n-1,k) subsets per stratum so 1/C(n-1,k) cancels with the stratum size in the mean.)
        v(empty) = 0 by convention."""
        v_empty = 0.0
        shapley = {}
        for f in FEATURES:
            others = [x for x in FEATURES if x != f]
            phi = 0.0
            for k_size in range(0, n):  # |S| = k_size where S subset of others
                deltas = []
                for combo in itertools.combinations(others, k_size):
                    s_with = frozenset(combo + (f,))
                    s_without = frozenset(combo)
                    v_with = lookup[s_with][metric_key]
                    v_without = lookup[s_without][metric_key] if s_without else v_empty
                    deltas.append(v_with - v_without)
                if deltas:
                    phi += float(np.mean(deltas))
            shapley[f] = phi / n
        # efficiency check: sum of phi should approx = v(N) - v(empty)
        total = sum(shapley.values())
        print(f"  [{metric_key}] sum(phi) = {total:.6f}, v(N) = {full_metric_value:.6f}, "
              f"diff = {abs(total - full_metric_value):.2e}")
        return shapley

    sh_mcc = shapley_for("mean_mcc", full10_mean_mcc)
    sh_enr = shapley_for("mean_enrichment", full10_mean_enr)
    sh_df = pd.DataFrame([
        {"feature": f, "shapley_mcc": sh_mcc[f], "shapley_enrichment": sh_enr[f]}
        for f in FEATURES
    ]).sort_values("shapley_mcc", ascending=False)
    sh_df.to_csv(OUT_DIR / "p3_shapley.csv", index=False)
    print("\nShapley table (sorted by MCC contribution):")
    print(sh_df.to_string(index=False))

    # Cross-check: 4-core row matches existing artifacts exactly
    core_row = df[df["is_core_4"]].iloc[0]
    print(f"\n4-core ({','.join(sorted(CORE_4))}):")
    print(f"  mean_mcc = {core_row['mean_mcc']:.10f}")
    print(f"  k = {core_row['k']}, features = {core_row['features']}")
    expected = 0.0808818486287735  # from subset_selection_robustness_210combos.csv combo_id=13
    diff = abs(core_row['mean_mcc'] - expected)
    print(f"  Expected (existing 210-combo CSV): {expected:.10f}")
    print(f"  |diff| = {diff:.2e}")
    if diff > 1e-9:
        print("  WARN: 4-core MCC does not exactly match existing artifact")
    else:
        print("  OK: exact match.")

    # 4-core lattice rank
    df_sorted = df.sort_values("mean_mcc", ascending=False).reset_index(drop=True)
    core_rank = int(df_sorted.index[df_sorted["is_core_4"]].tolist()[0]) + 1
    print(f"\n4-core lattice rank: {core_rank} / {len(df)} (sorted by mean_mcc desc)")

    # Pareto frontier
    best_per_k = df.groupby("k")["mean_mcc"].max().reset_index()
    fig, ax = plt.subplots(figsize=(7, 4.5))
    ax.plot(best_per_k["k"], best_per_k["mean_mcc"], "o-", color="steelblue",
            label="Best subset of size k")
    ax.axhline(full10_mean_mcc, ls="--", color="gray",
               label=f"Full-10 ({full10_mean_mcc:.3f})")
    core4_mcc = float(core_row["mean_mcc"])
    ax.scatter([4], [core4_mcc], s=160, marker="*", color="red", zorder=5,
               label=f"4-core ({core4_mcc:.3f}, rank {core_rank}/1023)")
    ax.set_xlabel("Subset size |S|")
    ax.set_ylabel("LOPO mean MCC")
    ax.set_title("P3: Pareto frontier of feature subsets (12-pathogen nested LOPO)")
    ax.legend(loc="lower right")
    ax.grid(alpha=0.3)
    fig.tight_layout()
    fig.savefig(OUT_DIR / "p3_pareto_frontier.png", dpi=150)
    print(f"\nWrote {OUT_DIR}/p3_pareto_frontier.png")
    print(f"\nDone. Lattice CSV: {OUT_DIR}/p3_full_lattice_1023.csv ({len(df)} rows)")


if __name__ == "__main__":
    main()
