#!/usr/bin/env python3
"""Exhaustive 4-of-10 feature subset selection robustness for MutBench.

For every C(10,4) = 210 combination, run the same nested-LOPO protocol
used in `feature_ablation_nested_lopo.py` and report:
  - LOPO mean MCC across 12 held-out pathogens
  - paired delta vs full-10 ensemble
  - retention ratio vs full-10
  - rank of the dissertation's 4-feature core (homoplasy, pLDDT,
    entropy, freq) within the 210 subsets

Outputs:
  results/mutbench/feature_analysis/subset_selection_robustness_210combos.csv
  results/mutbench/feature_analysis/subset_selection_robustness_top10.csv
  results/mutbench/feature_analysis/subset_selection_robustness_summary.csv
"""

from __future__ import annotations

import sys
import warnings
from itertools import combinations
from pathlib import Path

import numpy as np
import pandas as pd
from sklearn.metrics import matthews_corrcoef, roc_auc_score

warnings.filterwarnings("ignore", category=RuntimeWarning)

PROJECT_ROOT = Path(__file__).resolve().parent.parent
FEATURE_DIR = PROJECT_ROOT / "results" / "mutbench" / "feature_analysis"

ALL_PATHOGENS = [
    "SARS-CoV-2", "H3N2", "Norovirus", "HIV-1", "Dengue",
    "RSV", "Influenza_B", "MERS", "HCV",
    "Zika", "Rabies", "EV-A71",
]

FEATURE_NAMES = [
    "freq", "entropy", "rare_freq", "homoplasy", "esm2_llr",
    "plddt", "sasa", "grantham", "dnds_proxy", "semantic_change",
]

CORE_4 = ("homoplasy", "plddt", "entropy", "freq")  # dissertation choice

THRESHOLD_FRAC = 0.10
RANDOM_SEED = 42


def safe_mcc(y_true, y_pred):
    y_true = np.asarray(y_true, dtype=int)
    y_pred = np.asarray(y_pred, dtype=int)
    if y_pred.sum() == 0 or y_pred.sum() == len(y_pred):
        return 0.0
    if y_true.sum() == 0 or y_true.sum() == len(y_true):
        return 0.0
    return matthews_corrcoef(y_true, y_pred)


def load_data():
    data = {}
    for p in ALL_PATHOGENS:
        path = FEATURE_DIR / f"feature_matrix_{p}.csv"
        df = pd.read_csv(path)
        if "layer_a" not in df.columns:
            print(f"  [WARN] {p}: no layer_a column, skip")
            continue
        y = df["layer_a"].values.astype(int)
        if y.sum() == 0 or y.sum() == len(y):
            print(f"  [WARN] {p}: degenerate Layer A (sum={y.sum()}, n={len(y)}), skip")
            continue
        data[p] = {"df": df, "y": y}
    print(f"Loaded {len(data)} pathogens with valid Layer A: {list(data.keys())}")
    return data


def precompute_pathogen_arrays(data):
    """Cache per-pathogen feature arrays as float matrices for speed."""
    cache = {}
    for p, d in data.items():
        F = np.zeros((len(d["y"]), len(FEATURE_NAMES)), dtype=float)
        for j, f in enumerate(FEATURE_NAMES):
            F[:, j] = np.nan_to_num(
                d["df"][f].values.astype(float),
                nan=0.0, posinf=0.0, neginf=0.0,
            )
        cache[p] = {"F": F, "y": d["y"].astype(int)}
    return cache


def fit_signs_cached(cache, training_pathogens, feature_idx_subset):
    """Fit per-feature sign on training pathogens (concatenated positions)."""
    signs = np.ones(len(feature_idx_subset), dtype=float)
    # concatenate
    xs_all = [cache[p]["F"] for p in training_pathogens]
    ys_all = [cache[p]["y"].astype(float) for p in training_pathogens]
    F_all = np.concatenate(xs_all, axis=0)
    y_all = np.concatenate(ys_all)
    if y_all.std() < 1e-12:
        return signs
    for k, j in enumerate(feature_idx_subset):
        col = F_all[:, j]
        if col.std() < 1e-12:
            signs[k] = 1.0
            continue
        # pearson
        r = np.corrcoef(col, y_all)[0, 1]
        signs[k] = -1.0 if (np.isfinite(r) and r < 0) else 1.0
    return signs


def equalweight_mcc_held_out(F_held, y_held, feat_idx, signs):
    F = F_held[:, list(feat_idx)] * signs[None, :]
    n_feat = F.shape[1]
    Z = np.zeros_like(F)
    w = np.zeros(n_feat)
    for j in range(n_feat):
        col = F[:, j]
        s = col.std()
        if s > 1e-10:
            Z[:, j] = (col - col.mean()) / s
            w[j] = 1.0 / n_feat
    if w.sum() < 1e-10:
        return 0.0
    w /= w.sum()
    scores = Z @ w
    thr = np.percentile(scores, 100 * (1 - THRESHOLD_FRAC))
    pred = (scores >= thr).astype(int)
    return safe_mcc(y_held, pred)


def lopo_eval_subset(cache, feat_idx):
    """Run nested LOPO on a fixed feature index subset; return per-fold MCC dict."""
    fold_mcc = {}
    pathogens = list(cache.keys())
    for held_p in pathogens:
        training = [p for p in pathogens if p != held_p]
        signs = fit_signs_cached(cache, training, feat_idx)
        held = cache[held_p]
        mcc = equalweight_mcc_held_out(held["F"], held["y"], feat_idx, signs)
        fold_mcc[held_p] = mcc
    return fold_mcc


def lopo_eval_full(cache):
    """Full 10-feature LOPO (baseline)."""
    return lopo_eval_subset(cache, tuple(range(len(FEATURE_NAMES))))


def main():
    print("MutBench: 4-of-10 Exhaustive Subset Selection (210 combos)")
    print("=" * 60)
    data = load_data()
    if not data:
        print("No usable pathogens; aborting.")
        sys.exit(1)
    cache = precompute_pathogen_arrays(data)
    pathogens = list(cache.keys())

    # Full 10-feature reference
    full_mcc = lopo_eval_full(cache)
    full_mean = float(np.mean(list(full_mcc.values())))
    print(f"\nFull 10-feature LOPO mean MCC: {full_mean:.4f}")

    # Enumerate all 4-of-10 subsets
    feat_to_idx = {f: i for i, f in enumerate(FEATURE_NAMES)}
    core4_idx = tuple(sorted(feat_to_idx[f] for f in CORE_4))

    rows = []
    all_combos = list(combinations(range(len(FEATURE_NAMES)), 4))
    print(f"Enumerating {len(all_combos)} 4-of-10 subsets ...")
    for cid, combo in enumerate(all_combos):
        fold_mcc = lopo_eval_subset(cache, combo)
        per_fold = [fold_mcc[p] for p in pathogens]
        m = float(np.mean(per_fold))
        deltas = [fold_mcc[p] - full_mcc[p] for p in pathogens]
        feats = ",".join(FEATURE_NAMES[i] for i in combo)
        rows.append({
            "combo_id": cid,
            "features": feats,
            "f1": FEATURE_NAMES[combo[0]],
            "f2": FEATURE_NAMES[combo[1]],
            "f3": FEATURE_NAMES[combo[2]],
            "f4": FEATURE_NAMES[combo[3]],
            "lopo_mean_mcc": m,
            "paired_delta_vs_full10": float(np.mean(deltas)),
            "retention_ratio_vs_full10": (m / full_mean) if abs(full_mean) > 1e-10 else float('nan'),
            "is_core_4": tuple(sorted(combo)) == core4_idx,
        })
        if (cid + 1) % 30 == 0:
            print(f"  ...{cid + 1}/{len(all_combos)}")

    df = pd.DataFrame(rows)
    df = df.sort_values("lopo_mean_mcc", ascending=False).reset_index(drop=True)
    df["rank"] = df.index + 1
    # rebuild column order
    df = df[[
        "rank", "combo_id", "features", "f1", "f2", "f3", "f4",
        "lopo_mean_mcc", "paired_delta_vs_full10",
        "retention_ratio_vs_full10", "is_core_4",
    ]]

    out_full = FEATURE_DIR / "subset_selection_robustness_210combos.csv"
    df.to_csv(out_full, index=False)
    print(f"\nSaved 210-combination ranking: {out_full}")

    top10 = df.head(10).copy()
    out_top10 = FEATURE_DIR / "subset_selection_robustness_top10.csv"
    top10.to_csv(out_top10, index=False)

    core_row = df[df["is_core_4"]].iloc[0]
    core_rank = int(core_row["rank"])
    core_mcc = float(core_row["lopo_mean_mcc"])
    best_mcc = float(df.iloc[0]["lopo_mean_mcc"])
    best_features = df.iloc[0]["features"]

    median_mcc = float(df["lopo_mean_mcc"].median())
    p25 = float(df["lopo_mean_mcc"].quantile(0.25))
    p75 = float(df["lopo_mean_mcc"].quantile(0.75))

    pct = 100.0 * core_rank / len(df)
    print("\n=== Subset selection robustness summary ===")
    print(f"  Total subsets evaluated: {len(df)}")
    print(f"  Best 4-feature subset: {best_features}  (mean MCC = {best_mcc:.4f})")
    print(f"  Dissertation 4-core ({','.join(CORE_4)}): rank {core_rank}/{len(df)}  ({pct:.1f}%-tile)")
    print(f"    mean MCC = {core_mcc:.4f}  vs best = {best_mcc:.4f}  (gap = {best_mcc - core_mcc:+.4f})")
    print(f"  Distribution: median = {median_mcc:.4f}, IQR = [{p25:.4f}, {p75:.4f}]")
    print(f"  Full-10 reference MCC = {full_mean:.4f}")

    summary = pd.DataFrame([
        {"metric": "n_subsets", "value": len(df)},
        {"metric": "full10_lopo_mean_mcc", "value": full_mean},
        {"metric": "best_subset_mcc", "value": best_mcc},
        {"metric": "best_subset_features", "value": best_features},
        {"metric": "core4_features", "value": ",".join(CORE_4)},
        {"metric": "core4_rank", "value": core_rank},
        {"metric": "core4_total", "value": len(df)},
        {"metric": "core4_percentile", "value": pct},
        {"metric": "core4_mcc", "value": core_mcc},
        {"metric": "core4_gap_vs_best", "value": best_mcc - core_mcc},
        {"metric": "median_subset_mcc", "value": median_mcc},
        {"metric": "iqr_lo", "value": p25},
        {"metric": "iqr_hi", "value": p75},
    ])
    out_sum = FEATURE_DIR / "subset_selection_robustness_summary.csv"
    summary.to_csv(out_sum, index=False)
    print(f"  Summary: {out_sum}")
    print(f"  Top-10: {out_top10}")


if __name__ == "__main__":
    main()
