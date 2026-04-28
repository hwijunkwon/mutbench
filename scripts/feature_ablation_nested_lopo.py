#!/usr/bin/env python3
"""Nested Leave-One-Pathogen-Out (LOPO) feature ablation for MutBench.

Replaces the in-sample protocol of feature_ablation.py for the
4-feature core retention claim. For each fold k:
  - held-out pathogen P_k
  - training pathogens = the other 11
  - on training: fit per-feature directional sign s_f and feature
    ranking by mean |AUC - 0.5|
  - on held-out: apply training sign + ranking, z-score within the
    held-out positions only, uniform-weight average, top-10% threshold,
    MCC against Layer A.

Reports for each k in {1..10} and the explicit 4-feature core
(homoplasy, pLDDT, entropy, frequency) the LOPO mean MCC, fold-level
paired delta vs the 10-feature ensemble, and a paired bootstrap CI
(1,000 resamples over the 12 folds).

Outputs:
  results/mutbench/feature_analysis/feature_ablation_nested_lopo.csv
  results/mutbench/feature_analysis/feature_ablation_nested_lopo_summary.csv
"""

from __future__ import annotations

import sys
import warnings
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

CORE_4 = ["homoplasy", "plddt", "entropy", "freq"]

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


def fit_signs(training_data, features):
    """Per-feature directional sign s_f in {-1, +1}, fit on training pathogens.

    Sign chosen to maximize positive Pearson correlation between feature
    and Layer A membership across the union of training pathogen positions
    (concatenated).
    """
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


def fit_feature_ranking(training_data, features):
    """Rank features by mean |AUC - 0.5| across training pathogens, descending."""
    means = {}
    for f in features:
        eff_aucs = []
        for p, d in training_data.items():
            x = np.nan_to_num(d["df"][f].values.astype(float), nan=0.0, posinf=0.0, neginf=0.0)
            y = d["y"].astype(int)
            if x.std() < 1e-12 or y.sum() == 0 or y.sum() == len(y):
                continue
            try:
                a = roc_auc_score(y, x)
                eff_aucs.append(abs(a - 0.5))
            except ValueError:
                continue
        means[f] = float(np.mean(eff_aucs)) if eff_aucs else 0.0
    return sorted(features, key=lambda f: -means[f])


def equalweight_mcc_held_out(held_df, held_y, feature_subset, signs):
    """Apply training-fit signs, z-score within held-out, uniform mean, top-10% MCC."""
    if not feature_subset:
        return 0.0
    F = np.nan_to_num(
        held_df[feature_subset].values.astype(float),
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
        return 0.0
    w /= w.sum()
    scores = Z @ w
    thr = np.percentile(scores, 100 * (1 - THRESHOLD_FRAC))
    pred = (scores >= thr).astype(int)
    return safe_mcc(held_y, pred)


def lopo_eval(data, feature_selector):
    """Run nested LOPO; feature_selector(training_data, features_in_order) -> selected list."""
    fold_mcc = {}
    for held_p in data:
        training = {k: v for k, v in data.items() if k != held_p}
        signs = fit_signs(training, FEATURE_NAMES)
        ranking = fit_feature_ranking(training, FEATURE_NAMES)
        subset = feature_selector(training, ranking)
        held_d = data[held_p]
        mcc = equalweight_mcc_held_out(held_d["df"], held_d["y"], subset, signs)
        fold_mcc[held_p] = mcc
    return fold_mcc


def main():
    rng = np.random.default_rng(RANDOM_SEED)
    print("MutBench Nested LOPO Feature Ablation")
    print("=" * 60)
    data = load_data()
    if not data:
        print("No usable pathogens; aborting.")
        sys.exit(1)

    # --- 1. 10-feature ensemble (full) ---
    full_mcc = lopo_eval(data, lambda training, ranking: list(FEATURE_NAMES))
    full_mean = np.mean(list(full_mcc.values()))
    print(f"\nFull 10-feature LOPO mean MCC: {full_mean:.4f}")
    for p, m in full_mcc.items():
        print(f"  {p:<14s} held-out MCC = {m:+.4f}")

    # --- 2. Cumulative top-K (training-determined per fold) ---
    print("\nCumulative top-K (fold-specific ranking):")
    cum_results = {}
    for k in range(1, len(FEATURE_NAMES) + 1):
        m = lopo_eval(data, lambda training, ranking, K=k: ranking[:K])
        cum_results[k] = m
        print(f"  top-{k:2d}: mean LOPO MCC = {np.mean(list(m.values())):.4f}")

    # --- 3. Fixed 4-feature core (per the dissertation: homoplasy, pLDDT, entropy, freq) ---
    fixed_mcc = lopo_eval(data, lambda training, ranking: CORE_4)
    fixed_mean = np.mean(list(fixed_mcc.values()))
    print(f"\nFixed 4-feature core ({', '.join(CORE_4)}) LOPO mean MCC: {fixed_mean:.4f}")
    for p, m in fixed_mcc.items():
        print(f"  {p:<14s} held-out MCC = {m:+.4f}")

    # --- 4. Paired bootstrap fixed-4 vs full-10 over folds ---
    pathogens = list(data.keys())
    deltas = np.array([fixed_mcc[p] - full_mcc[p] for p in pathogens])
    full_arr = np.array([full_mcc[p] for p in pathogens])
    fixed_arr = np.array([fixed_mcc[p] for p in pathogens])

    n_boot = 1000
    n = len(pathogens)
    boot_full, boot_fixed, boot_ratio, boot_delta = [], [], [], []
    for _ in range(n_boot):
        idx = rng.integers(0, n, size=n)
        f_b = full_arr[idx].mean()
        x_b = fixed_arr[idx].mean()
        boot_full.append(f_b)
        boot_fixed.append(x_b)
        boot_delta.append(x_b - f_b)
        if abs(f_b) > 1e-10:
            boot_ratio.append(x_b / f_b)
    boot_full = np.array(boot_full)
    boot_fixed = np.array(boot_fixed)
    boot_delta = np.array(boot_delta)
    boot_ratio = np.array(boot_ratio) if boot_ratio else np.array([np.nan])

    print("\n=== Paired bootstrap (1,000 resamples over 12 folds) ===")
    print(f"  Full-10 LOPO mean MCC: {full_mean:.4f}  (95% CI [{np.percentile(boot_full, 2.5):.4f}, {np.percentile(boot_full, 97.5):.4f}])")
    print(f"  Fixed-4 LOPO mean MCC: {fixed_mean:.4f}  (95% CI [{np.percentile(boot_fixed, 2.5):.4f}, {np.percentile(boot_fixed, 97.5):.4f}])")
    print(f"  Paired delta (fixed - full): {deltas.mean():+.4f}  (95% CI [{np.percentile(boot_delta, 2.5):+.4f}, {np.percentile(boot_delta, 97.5):+.4f}])")
    if np.isfinite(boot_ratio).any():
        print(f"  Retention ratio fixed/full: {fixed_mean/full_mean:.3f}  (95% CI [{np.percentile(boot_ratio, 2.5):.3f}, {np.percentile(boot_ratio, 97.5):.3f}])")
    # one-sided permutation: probability that fixed ≥ full under null sign permutation
    n_perm = 5000
    rng2 = np.random.default_rng(RANDOM_SEED + 1)
    pair = np.column_stack([full_arr, fixed_arr])
    abs_diff = np.abs(deltas).mean()
    diffs_under_null = []
    for _ in range(n_perm):
        flip = rng2.integers(0, 2, size=n) * 2 - 1
        diffs_under_null.append((flip * deltas).mean())
    diffs_under_null = np.array(diffs_under_null)
    p_two_sided = (np.abs(diffs_under_null) >= abs(deltas.mean())).mean()
    print(f"  Two-sided sign-flip permutation p (paired): {p_two_sided:.4f}")

    # --- 5. Save artifacts ---
    rows = []
    for p in pathogens:
        rows.append({
            "fold_held_out": p,
            "full10_mcc": full_mcc[p],
            "fixed4_mcc": fixed_mcc[p],
            "delta_fixed4_minus_full10": fixed_mcc[p] - full_mcc[p],
        })
    for k, mp in cum_results.items():
        for p in pathogens:
            rows.append({
                "fold_held_out": p,
                "configuration": f"cumulative_top_{k}",
                "k_features": k,
                "mcc": mp[p],
            })
    pd.DataFrame(rows).to_csv(FEATURE_DIR / "feature_ablation_nested_lopo.csv", index=False)

    summary = pd.DataFrame([
        {"protocol": "full_10_feature_LOPO",
         "lopo_mean_mcc": full_mean,
         "boot_ci_lo": np.percentile(boot_full, 2.5),
         "boot_ci_hi": np.percentile(boot_full, 97.5)},
        {"protocol": "fixed_4_core_LOPO",
         "lopo_mean_mcc": fixed_mean,
         "boot_ci_lo": np.percentile(boot_fixed, 2.5),
         "boot_ci_hi": np.percentile(boot_fixed, 97.5)},
        {"protocol": "paired_delta_fixed4_minus_full10",
         "lopo_mean_mcc": deltas.mean(),
         "boot_ci_lo": np.percentile(boot_delta, 2.5),
         "boot_ci_hi": np.percentile(boot_delta, 97.5)},
        {"protocol": "retention_ratio_fixed4_over_full10",
         "lopo_mean_mcc": fixed_mean / full_mean if abs(full_mean) > 1e-10 else float('nan'),
         "boot_ci_lo": np.percentile(boot_ratio, 2.5) if np.isfinite(boot_ratio).any() else float('nan'),
         "boot_ci_hi": np.percentile(boot_ratio, 97.5) if np.isfinite(boot_ratio).any() else float('nan')},
    ])
    summary.to_csv(FEATURE_DIR / "feature_ablation_nested_lopo_summary.csv", index=False)
    print(f"\nSaved CSVs to {FEATURE_DIR}")
    print(f"\nFinal: 4-core retains {100*fixed_mean/full_mean:.1f}% of full-10 mean MCC under nested-LOPO; permutation p={p_two_sided:.4f}")


if __name__ == "__main__":
    main()
