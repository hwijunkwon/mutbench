#!/usr/bin/env python3
"""Rebuild feature matrices with 10 features and recompute per-feature AUC + RF importance.

10 features:
  Original 6: freq, entropy, rare_freq, homoplasy, esm2_llr, plddt
  New 4: sasa (RSA), grantham, dnds_proxy, semantic_change
"""

import os
import sys
import warnings
warnings.filterwarnings("ignore")

import numpy as np
import pandas as pd
from scipy.stats import spearmanr
from sklearn.metrics import roc_auc_score
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import StratifiedKFold

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from tools.mutbench.ground_truth.multilayer_gt import get_gt_adaptive

BASE = os.path.join(os.path.dirname(__file__), "..")
OUT_DIR = os.path.join(BASE, "results/mutbench/feature_analysis")
STRUCT_DIR = os.path.join(BASE, "results/mutbench/structural_features")

PATHOGENS = [
    "SARS-CoV-2", "H3N2", "Norovirus", "HIV-1", "Dengue",
    "RSV", "Influenza_B", "MERS", "HCV"
]

SASA_NAME_MAP = {
    "SARS-CoV-2": "sars2", "H3N2": "influenza_h3n2", "Norovirus": "norovirus",
    "HIV-1": "hiv", "Dengue": "dengue", "RSV": "rsv",
    "Influenza_B": "influenza_b", "MERS": "mers", "HCV": "hcv",
}

FEATURE_NAMES = [
    "freq", "entropy", "rare_freq", "homoplasy", "esm2_llr", "plddt",
    "sasa", "grantham", "dnds_proxy", "semantic_change"
]

FEATURE_LABELS = {
    "freq": "Frequency",
    "entropy": "Entropy",
    "rare_freq": "Rare variant",
    "homoplasy": "Homoplasy",
    "esm2_llr": "ESM-2 LLR",
    "plddt": "pLDDT",
    "sasa": "SASA (RSA)",
    "grantham": "Grantham dist.",
    "dnds_proxy": "dN/dS proxy",
    "semantic_change": "Semantic change",
}


def load_old_feature_matrix(pathogen):
    """Load existing 6-feature matrix."""
    path = os.path.join(OUT_DIR, f"feature_matrix_{pathogen}.csv")
    return pd.read_csv(path)


def load_new_feature(pathogen, feature_name):
    """Load a new feature CSV and return array."""
    if feature_name == "sasa":
        sasa_name = SASA_NAME_MAP[pathogen]
        path = os.path.join(STRUCT_DIR, f"{sasa_name}_sasa.csv")
        df = pd.read_csv(path)
        return df["RSA"].values
    elif feature_name == "grantham":
        path = os.path.join(OUT_DIR, f"{pathogen}_grantham.csv")
        df = pd.read_csv(path)
        return df["grantham"].values
    elif feature_name == "dnds_proxy":
        path = os.path.join(OUT_DIR, f"{pathogen}_dnds.csv")
        df = pd.read_csv(path)
        return df["dnds_proxy"].values
    elif feature_name == "semantic_change":
        path = os.path.join(OUT_DIR, f"{pathogen}_semantic_change.csv")
        df = pd.read_csv(path)
        return df["semantic_change"].values


def build_10feature_matrix(pathogen):
    """Build 10-feature matrix by merging old and new features."""
    df = load_old_feature_matrix(pathogen)
    n_old = len(df)

    for feat in ["sasa", "grantham", "dnds_proxy", "semantic_change"]:
        arr = load_new_feature(pathogen, feat)
        min_len = min(n_old, len(arr))
        padded = np.full(n_old, np.nan)
        padded[:min_len] = arr[:min_len]
        df[feat] = padded

    return df


def compute_auc_stats(df, pathogen):
    """Compute per-feature AUC and Spearman rho."""
    features = [c for c in FEATURE_NAMES if c in df.columns]
    y = df["layer_a"].values
    n_pos = int(y.sum())

    if n_pos == 0 or n_pos == len(y):
        return []

    results = []
    for feat in features:
        x = df[feat].values
        mask = ~np.isnan(x)
        x_clean = x[mask]
        y_clean = y[mask]

        if len(np.unique(y_clean)) < 2:
            continue

        try:
            auc = roc_auc_score(y_clean, x_clean)
        except ValueError:
            auc = np.nan

        rho, p_val = spearmanr(x_clean, y_clean)

        results.append({
            "pathogen": pathogen,
            "feature": feat,
            "auc": round(auc, 4),
            "spearman_rho": round(rho, 4),
            "p_value": round(p_val, 6) if p_val is not None else np.nan,
            "n_positions": len(y_clean),
            "n_layer_a": int(y_clean.sum()),
        })

    return results


def compute_rf_importance(df, pathogen):
    """Compute Random Forest feature importance with cross-validation."""
    features = [c for c in FEATURE_NAMES if c in df.columns]
    y = df["layer_a"].values
    n_pos = int(y.sum())

    if n_pos < 5:
        return None, None

    X = df[features].values
    # Fill NaN with column medians
    for j in range(X.shape[1]):
        col = X[:, j]
        mask = np.isnan(col)
        if mask.any():
            X[mask, j] = np.nanmedian(col)

    # Cross-validated importance
    n_splits = min(5, n_pos)
    if n_splits < 2:
        return None, None

    skf = StratifiedKFold(n_splits=n_splits, shuffle=True, random_state=42)
    importances_all = []
    aucs = []

    for train_idx, test_idx in skf.split(X, y):
        rf = RandomForestClassifier(
            n_estimators=200, max_depth=5, random_state=42,
            class_weight="balanced"
        )
        rf.fit(X[train_idx], y[train_idx])
        importances_all.append(rf.feature_importances_)

        try:
            proba = rf.predict_proba(X[test_idx])[:, 1]
            if len(np.unique(y[test_idx])) >= 2:
                aucs.append(roc_auc_score(y[test_idx], proba))
        except:
            pass

    mean_imp = np.mean(importances_all, axis=0)
    mean_auc = np.mean(aucs) if aucs else np.nan

    imp_dict = {feat: round(imp, 4) for feat, imp in zip(features, mean_imp)}
    imp_dict["pathogen"] = pathogen

    return imp_dict, mean_auc


def compute_feature_correlation(df, pathogen):
    """Compute pairwise Spearman correlation between features."""
    features = [c for c in FEATURE_NAMES if c in df.columns]
    X = df[features].values

    n_feat = len(features)
    corr_matrix = np.full((n_feat, n_feat), np.nan)

    for i in range(n_feat):
        for j in range(n_feat):
            mask = ~np.isnan(X[:, i]) & ~np.isnan(X[:, j])
            if mask.sum() > 10:
                rho, _ = spearmanr(X[mask, i], X[mask, j])
                corr_matrix[i, j] = rho

    return pd.DataFrame(corr_matrix, index=features, columns=features)


def main():
    print("=" * 70)
    print("FEATURE ANALYSIS v2: 10 features × 9 pathogens")
    print("=" * 70)

    all_auc = []
    all_imp = []
    all_cv_auc = []
    all_corr = {}

    for pathogen in PATHOGENS:
        print(f"\n{'='*50}")
        print(f"  {pathogen}")
        print(f"{'='*50}")

        df = build_10feature_matrix(pathogen)

        # Save updated matrix
        out_path = os.path.join(OUT_DIR, f"feature_matrix_{pathogen}.csv")
        df.to_csv(out_path, index=False)
        print(f"  Saved: {out_path} ({len(df)} positions, {int(df['layer_a'].sum())} Layer A)")

        # AUC
        auc_results = compute_auc_stats(df, pathogen)
        all_auc.extend(auc_results)

        # RF importance
        imp_dict, cv_auc = compute_rf_importance(df, pathogen)
        if imp_dict:
            all_imp.append(imp_dict)
            all_cv_auc.append({"pathogen": pathogen, "rf_cv_auc": round(cv_auc, 4)})
            print(f"  RF CV AUC: {cv_auc:.4f}")

        # Feature correlation
        corr_df = compute_feature_correlation(df, pathogen)
        all_corr[pathogen] = corr_df

    # ── Save results ──────────────────────────────────────────────────
    # AUC summary
    auc_df = pd.DataFrame(all_auc)
    auc_df.to_csv(os.path.join(OUT_DIR, "per_feature_auc_v2.csv"), index=False)

    # Print AUC pivot
    pivot = auc_df.pivot_table(index="pathogen", columns="feature", values="auc")
    feat_order = [f for f in FEATURE_NAMES if f in pivot.columns]
    pivot = pivot[feat_order]
    print("\n" + "=" * 100)
    print("PER-FEATURE AUC (v2, 10 features)")
    print("=" * 100)
    print(pivot.to_string(float_format=lambda x: f"{x:.3f}"))

    # Best feature per pathogen
    print("\n" + "=" * 70)
    print("BEST FEATURE PER PATHOGEN")
    print("=" * 70)
    for pathogen in PATHOGENS:
        row = pivot.loc[pathogen] if pathogen in pivot.index else None
        if row is not None:
            best = row.idxmax()
            print(f"  {pathogen:15s}: {FEATURE_LABELS.get(best, best):20s} (AUC={row[best]:.3f})")

    # RF importance
    if all_imp:
        imp_df = pd.DataFrame(all_imp)
        imp_df.to_csv(os.path.join(OUT_DIR, "rf_importance_v2.csv"), index=False)
        print("\n" + "=" * 100)
        print("RF FEATURE IMPORTANCE (v2)")
        print("=" * 100)
        cols = ["pathogen"] + [f for f in FEATURE_NAMES if f in imp_df.columns]
        print(imp_df[cols].to_string(index=False, float_format=lambda x: f"{x:.3f}"))

    # CV AUC
    if all_cv_auc:
        cv_df = pd.DataFrame(all_cv_auc)
        cv_df.to_csv(os.path.join(OUT_DIR, "rf_cv_auc_v2.csv"), index=False)

    # Feature correlation (save mean across pathogens)
    if all_corr:
        mean_corr = sum(all_corr.values()) / len(all_corr)
        mean_corr.to_csv(os.path.join(OUT_DIR, "feature_correlation_mean.csv"))
        print("\n" + "=" * 100)
        print("MEAN FEATURE CORRELATION (across 9 pathogens)")
        print("=" * 100)
        print(mean_corr.to_string(float_format=lambda x: f"{x:.2f}"))

    print("\n\nDone! All results saved to", OUT_DIR)


if __name__ == "__main__":
    main()
