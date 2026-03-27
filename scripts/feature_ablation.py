#!/usr/bin/env python3
"""Feature ablation study for MutBench-Adapt.

Three ablation analyses:
1. Leave-one-feature-out: remove each of 10 features, measure MCC impact
2. Feature group ablation: test thematic feature subsets
3. Cumulative addition: add features one by one in AUC rank order

All evaluations use EqualWeight ensemble with LOPO and top-10% threshold.
"""

from __future__ import annotations

import sys
import warnings
from pathlib import Path

import numpy as np
import pandas as pd
from sklearn.metrics import matthews_corrcoef

warnings.filterwarnings("ignore", category=RuntimeWarning)

PROJECT_ROOT = Path(__file__).resolve().parent.parent
FEATURE_DIR = PROJECT_ROOT / "results" / "mutbench" / "feature_analysis"
RESULTS_DIR = PROJECT_ROOT / "results" / "mutbench"

sys.path.insert(0, str(PROJECT_ROOT / "tools"))
from mutbench.ground_truth.multilayer_gt import get_gt_adaptive  # noqa: E402

ALL_PATHOGENS = [
    "SARS-CoV-2", "H3N2", "Norovirus", "HIV-1", "Dengue",
    "RSV", "Influenza_B", "MERS", "HCV",
    "Zika", "Rabies", "EV-A71",
]

FEATURE_NAMES = [
    "freq", "entropy", "rare_freq", "homoplasy", "esm2_llr",
    "plddt", "sasa", "grantham", "dnds_proxy", "semantic_change",
]

THRESHOLD_CONFIG = {"type": "topk", "frac": 0.10}

# Feature groups for group ablation
FEATURE_GROUPS = {
    "Frequency-only": ["freq", "entropy", "rare_freq"],
    "Freq + Phylogeny": ["freq", "entropy", "rare_freq", "homoplasy"],
    "Freq + Structure": ["freq", "entropy", "rare_freq", "plddt", "sasa"],
    "Freq + DL": ["freq", "entropy", "rare_freq", "esm2_llr", "semantic_change"],
    "All 10": list(FEATURE_NAMES),
}


def load_feature_matrix(pathogen: str) -> pd.DataFrame:
    path = FEATURE_DIR / f"feature_matrix_{pathogen}.csv"
    if not path.exists():
        raise FileNotFoundError(f"Feature matrix not found: {path}")
    return pd.read_csv(path)


def safe_mcc(y_true: np.ndarray, y_pred: np.ndarray) -> float:
    y_true = np.asarray(y_true, dtype=int)
    y_pred = np.asarray(y_pred, dtype=int)
    if y_pred.sum() == 0 or y_pred.sum() == len(y_pred):
        return 0.0
    if y_true.sum() == 0 or y_true.sum() == len(y_true):
        return 0.0
    return matthews_corrcoef(y_true, y_pred)


def compute_equalweight_mcc(df: pd.DataFrame, y_true: np.ndarray,
                            feature_subset: list[str]) -> float:
    """Compute MCC using equal-weight z-score ensemble on a feature subset."""
    if len(feature_subset) == 0:
        return 0.0

    F = np.nan_to_num(
        df[feature_subset].values.copy(), nan=0.0, posinf=0.0, neginf=0.0
    )
    n_feat = F.shape[1]

    # Z-score normalize each feature
    Z = np.zeros_like(F)
    w = np.zeros(n_feat)
    for j in range(n_feat):
        std_j = np.std(F[:, j])
        if std_j > 1e-10:
            Z[:, j] = (F[:, j] - np.mean(F[:, j])) / std_j
            w[j] = 1.0 / n_feat
        # else: weight stays 0

    if w.sum() < 1e-10:
        return 0.0
    w /= w.sum()

    scores = Z @ w
    thr = np.percentile(scores, 100 * (1 - THRESHOLD_CONFIG["frac"]))
    pred = (scores >= thr).astype(int)
    return safe_mcc(y_true, pred)


def load_all_data() -> dict:
    """Load feature matrices and ground truth for all pathogens."""
    data = {}
    for p in ALL_PATHOGENS:
        try:
            df = load_feature_matrix(p)
            n_positions = len(df)
            if "layer_a" in df.columns:
                y_true = df["layer_a"].values.astype(int)
            else:
                gt_set = get_gt_adaptive(p, max_len=n_positions)
                y_true = np.zeros(n_positions, dtype=int)
                for pos in gt_set:
                    if pos < n_positions:
                        y_true[pos] = 1
            if y_true.sum() > 0:
                data[p] = {"df": df, "y_true": y_true}
        except FileNotFoundError:
            print(f"  [WARN] Skipping {p}: no feature matrix")
    return data


def run_leave_one_out(data: dict) -> pd.DataFrame:
    """Leave-one-feature-out ablation."""
    print("\n=== Leave-One-Feature-Out Ablation ===")
    rows = []

    # Full model baseline per pathogen
    full_mccs = {}
    for p, d in data.items():
        full_mccs[p] = compute_equalweight_mcc(d["df"], d["y_true"], FEATURE_NAMES)

    mean_full = np.mean(list(full_mccs.values()))
    print(f"Full model (all 10 features): mean MCC = {mean_full:.4f}")

    for feat in FEATURE_NAMES:
        subset = [f for f in FEATURE_NAMES if f != feat]
        mccs = {}
        for p, d in data.items():
            mccs[p] = compute_equalweight_mcc(d["df"], d["y_true"], subset)

        mean_mcc = np.mean(list(mccs.values()))
        delta = mean_mcc - mean_full
        print(f"  w/o {feat:<18s}: mean MCC = {mean_mcc:.4f}  (delta = {delta:+.4f})")

        for p in data:
            rows.append({
                "ablation_type": "leave_one_out",
                "configuration": f"w/o {feat}",
                "removed_feature": feat,
                "pathogen": p,
                "mcc": mccs[p],
                "mcc_full": full_mccs[p],
                "delta_mcc": mccs[p] - full_mccs[p],
            })

    # Add full model rows
    for p in data:
        rows.append({
            "ablation_type": "leave_one_out",
            "configuration": "all_10",
            "removed_feature": "none",
            "pathogen": p,
            "mcc": full_mccs[p],
            "mcc_full": full_mccs[p],
            "delta_mcc": 0.0,
        })

    return pd.DataFrame(rows)


def run_group_ablation(data: dict) -> pd.DataFrame:
    """Feature group ablation."""
    print("\n=== Feature Group Ablation ===")
    rows = []

    for group_name, features in FEATURE_GROUPS.items():
        mccs = {}
        for p, d in data.items():
            mccs[p] = compute_equalweight_mcc(d["df"], d["y_true"], features)

        mean_mcc = np.mean(list(mccs.values()))
        print(f"  {group_name:<22s} ({len(features)} features): mean MCC = {mean_mcc:.4f}")

        for p in data:
            rows.append({
                "ablation_type": "group",
                "configuration": group_name,
                "n_features": len(features),
                "features": ",".join(features),
                "pathogen": p,
                "mcc": mccs[p],
            })

    return pd.DataFrame(rows)


def run_cumulative_addition(data: dict) -> pd.DataFrame:
    """Cumulative feature addition in order of mean AUC across pathogens."""
    print("\n=== Cumulative Feature Addition ===")

    # Load per-feature AUC and compute mean |AUC - 0.5| per feature
    auc_df = pd.read_csv(FEATURE_DIR / "per_feature_auc_v2.csv")
    auc_df["eff_auc"] = (auc_df["auc"] - 0.5).abs()
    mean_eff = auc_df.groupby("feature")["eff_auc"].mean().sort_values(ascending=False)

    feature_order = [f for f in mean_eff.index if f in FEATURE_NAMES]
    print(f"  Feature order by mean |AUC-0.5|: {feature_order}")

    rows = []
    for k in range(1, len(feature_order) + 1):
        subset = feature_order[:k]
        mccs = {}
        for p, d in data.items():
            mccs[p] = compute_equalweight_mcc(d["df"], d["y_true"], subset)

        mean_mcc = np.mean(list(mccs.values()))
        added = feature_order[k - 1]
        print(f"  +{added:<18s} (k={k:2d}): mean MCC = {mean_mcc:.4f}")

        for p in data:
            rows.append({
                "ablation_type": "cumulative",
                "configuration": f"top_{k}",
                "k_features": k,
                "added_feature": added,
                "features": ",".join(subset),
                "pathogen": p,
                "mcc": mccs[p],
            })

    return pd.DataFrame(rows)


def main():
    print("MutBench-Adapt Feature Ablation Study")
    print("=" * 60)

    data = load_all_data()
    print(f"Loaded {len(data)} pathogens: {list(data.keys())}")

    df_loo = run_leave_one_out(data)
    df_group = run_group_ablation(data)
    df_cumul = run_cumulative_addition(data)

    # Combine and save
    all_results = pd.concat([df_loo, df_group, df_cumul], ignore_index=True)
    out_path = RESULTS_DIR / "feature_ablation_results.csv"
    all_results.to_csv(out_path, index=False)
    print(f"\nSaved {len(all_results)} rows to {out_path}")

    # Print summary table
    print("\n" + "=" * 70)
    print("SUMMARY: Leave-One-Feature-Out (mean MCC across pathogens)")
    print("=" * 70)
    loo_summary = (
        df_loo[df_loo["ablation_type"] == "leave_one_out"]
        .groupby("configuration")
        .agg(mean_mcc=("mcc", "mean"), mean_delta=("delta_mcc", "mean"))
        .sort_values("mean_delta")
    )
    print(loo_summary.to_string())

    print("\nSUMMARY: Feature Group Ablation")
    print("-" * 50)
    group_summary = (
        df_group.groupby("configuration")
        .agg(mean_mcc=("mcc", "mean"), n_features=("n_features", "first"))
        .sort_values("n_features")
    )
    print(group_summary.to_string())

    print("\nSUMMARY: Cumulative Addition")
    print("-" * 50)
    cumul_summary = (
        df_cumul.groupby(["k_features", "added_feature"])
        .agg(mean_mcc=("mcc", "mean"))
        .reset_index()
        .sort_values("k_features")
    )
    print(cumul_summary.to_string(index=False))


if __name__ == "__main__":
    main()
