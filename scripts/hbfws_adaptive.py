#!/usr/bin/env python3
"""Hierarchical Bayesian Feature-Weight Shrinkage (HBFWS) for MutBench.

Pre-registered hypothesis (cycle 7 algorithm experiment):
  H0: HBFWS mean nested-LOPO MCC <= EqualWeight (~0.07-0.083 baseline)
  H1: HBFWS > EqualWeight with paired Wilcoxon p < 0.05
  Prior P(reject H0): 15-25%

Design rationale (vs PAHD-R failures kNN 0.020 / Top-3 0.049 / Correlation 0.043):
  PAHD-R: per-pathogen MLE weights from 11-point 13-dim ill-conditioned space
  HBFWS: hierarchical partial pooling with explicit shrinkage strength
         learned from data; James-Stein dominance under squared loss
         worst case = global mean = EqualWeight (collapse if weak family signal)

Hierarchy:
  y_{i,p} ~ Bernoulli(sigmoid(mu + gamma_F(p) + sum_f w_f * z(x_{i,f})))
  w_f ~ Normal(0, sigma_feature)
  gamma_F ~ Normal(0, sigma_family)  -- 8 ICTV families
  mu ~ Normal(0, 0.5)
  sigma_* ~ HalfNormal(0.3)  -- HYPERPRIORS LEARN SHRINKAGE STRENGTH

Singleton families (Caliciviridae, Pneumoviridae, Retroviridae, Rhabdoviridae,
Picornaviridae) collapse gamma_F to global mean (no information to pool toward) ->
worst case = EqualWeight.

Paired families (Coronaviridae {SARS-CoV-2, MERS}; Orthomyxoviridae {H3N2,
Influenza B}; Flaviviridae {HCV, Dengue, Zika}) provide partial-pooling signal.

Usage: python3 scripts/hbfws_adaptive.py
"""

from __future__ import annotations

import warnings
from pathlib import Path

import numpy as np
import pandas as pd
import pymc as pm
import arviz as az
from sklearn.metrics import matthews_corrcoef
from sklearn.preprocessing import StandardScaler
from scipy.stats import wilcoxon

warnings.filterwarnings("ignore", category=FutureWarning)
warnings.filterwarnings("ignore", category=UserWarning)

PROJECT_ROOT = Path(__file__).resolve().parent.parent
FEATURE_DIR = PROJECT_ROOT / "results" / "mutbench" / "feature_analysis"
OUT_DIR = PROJECT_ROOT / "results" / "mutbench"

# 12-pathogen Stage 3 panel (matches feature_ablation_nested_lopo.py)
ALL_PATHOGENS = [
    "SARS-CoV-2", "H3N2", "Norovirus", "HIV-1", "Dengue",
    "RSV", "Influenza_B", "MERS", "HCV",
    "Zika", "Rabies", "EV-A71",
]

# ICTV family mapping
PATHOGEN_TO_FAMILY = {
    "SARS-CoV-2": "Coronaviridae",
    "MERS": "Coronaviridae",
    "H3N2": "Orthomyxoviridae",
    "Influenza_B": "Orthomyxoviridae",
    "HCV": "Flaviviridae",
    "Dengue": "Flaviviridae",
    "Zika": "Flaviviridae",
    "Norovirus": "Caliciviridae",     # singleton
    "HIV-1": "Retroviridae",          # singleton
    "RSV": "Pneumoviridae",            # singleton
    "Rabies": "Rhabdoviridae",         # singleton
    "EV-A71": "Picornaviridae",        # singleton
}

ALL_FAMILIES = sorted(set(PATHOGEN_TO_FAMILY.values()))
FAMILY_TO_IDX = {f: i for i, f in enumerate(ALL_FAMILIES)}

FEATURE_NAMES = [
    "freq", "entropy", "rare_freq", "homoplasy", "esm2_llr",
    "plddt", "sasa", "grantham", "dnds_proxy", "semantic_change",
]
CORE_4 = ["homoplasy", "plddt", "entropy", "freq"]

THRESHOLD_FRAC = 0.10  # top-10% threshold (matches nested-LOPO baseline)
RANDOM_SEED = 42
N_DRAWS = 1000          # per chain
N_TUNE = 1000
N_CHAINS = 4


def safe_mcc(y_true, y_pred):
    y_true = np.asarray(y_true, dtype=int)
    y_pred = np.asarray(y_pred, dtype=int)
    if y_pred.sum() == 0 or y_pred.sum() == len(y_pred):
        return 0.0
    if y_true.sum() == 0 or y_true.sum() == len(y_true):
        return 0.0
    return matthews_corrcoef(y_true, y_pred)


def load_pathogen(pathogen):
    """Load feature matrix + layer_a labels."""
    path = FEATURE_DIR / f"feature_matrix_{pathogen}.csv"
    if not path.exists():
        return None
    df = pd.read_csv(path)
    if "layer_a" not in df.columns:
        return None
    y = df["layer_a"].values.astype(int)
    if y.sum() == 0 or y.sum() == len(y):
        return None
    # Build feature matrix with all 10 features (NaN -> 0)
    feats = []
    for f in FEATURE_NAMES:
        if f in df.columns:
            feats.append(df[f].values)
        else:
            feats.append(np.zeros(len(df)))
    X = np.array(feats).T
    X = np.nan_to_num(X, nan=0.0, posinf=0.0, neginf=0.0)
    return {"X": X, "y": y, "n": len(df)}


def build_stacked_data(pathogen_data, exclude=None):
    """Stack X, y, and pathogen/family indices for training pathogens."""
    X_list, y_list, p_idx_list, f_idx_list = [], [], [], []
    pathogens_used = []
    p_to_idx = {}
    for p, data in pathogen_data.items():
        if p == exclude:
            continue
        if p not in PATHOGEN_TO_FAMILY:
            continue
        if p not in p_to_idx:
            p_to_idx[p] = len(p_to_idx)
        X_list.append(data["X"])
        y_list.append(data["y"])
        p_idx_list.append(np.full(data["n"], p_to_idx[p], dtype=int))
        f_idx_list.append(np.full(data["n"], FAMILY_TO_IDX[PATHOGEN_TO_FAMILY[p]], dtype=int))
        pathogens_used.append(p)
    X = np.vstack(X_list)
    y = np.concatenate(y_list)
    p_idx = np.concatenate(p_idx_list)
    f_idx = np.concatenate(f_idx_list)
    return X, y, p_idx, f_idx, pathogens_used


def fit_hbfws(X_train, y_train, f_idx_train, n_features=10, n_families=8):
    """Fit hierarchical Bayesian model with partial pooling."""
    with pm.Model() as model:
        # Hyperpriors learn shrinkage strength
        sigma_feature = pm.HalfNormal("sigma_feature", sigma=0.3)
        sigma_family = pm.HalfNormal("sigma_family", sigma=0.3)

        # Global intercept
        mu = pm.Normal("mu", mu=0.0, sigma=0.5)

        # Feature weights (non-centered)
        w_raw = pm.Normal("w_raw", mu=0.0, sigma=1.0, shape=n_features)
        w = pm.Deterministic("w", sigma_feature * w_raw)

        # Family random intercepts (non-centered) — partial pooling
        gamma_raw = pm.Normal("gamma_raw", mu=0.0, sigma=1.0, shape=n_families)
        gamma = pm.Deterministic("gamma", sigma_family * gamma_raw)

        # Linear predictor: per position
        eta = mu + gamma[f_idx_train] + pm.math.dot(X_train, w)

        # Bernoulli likelihood
        pm.Bernoulli("y_obs", logit_p=eta, observed=y_train)

        # Sample
        trace = pm.sample(
            draws=N_DRAWS,
            tune=N_TUNE,
            chains=N_CHAINS,
            random_seed=RANDOM_SEED,
            target_accept=0.95,
            progressbar=False,
            return_inferencedata=True,
        )

    return trace


def predict_held_out(trace, X_test, family_held_out_idx, n_features=10):
    """Posterior predictive: top-10% threshold MCC on held-out pathogen."""
    # Extract posterior means
    w_post = trace.posterior["w"].values.reshape(-1, n_features)  # (n_chains*n_draws, n_features)
    gamma_post = trace.posterior["gamma"].values.reshape(-1, len(ALL_FAMILIES))
    mu_post = trace.posterior["mu"].values.reshape(-1)

    # Posterior mean prediction
    w_mean = w_post.mean(axis=0)
    gamma_F_mean = gamma_post[:, family_held_out_idx].mean()
    mu_mean = mu_post.mean()

    # Score = mu + gamma_F + X @ w (logit space)
    scores = mu_mean + gamma_F_mean + X_test @ w_mean
    return scores


def equal_weight_baseline(X_test, core_indices=None):
    """EqualWeight baseline: uniform z-score average over selected features."""
    Xz = StandardScaler().fit_transform(X_test)
    if core_indices is None:
        # Use 4-feature core
        core_indices = [FEATURE_NAMES.index(f) for f in CORE_4]
    # Apply pre-defined directional signs (homoplasy +, plddt - via inversion is in raw data; entropy +, freq +)
    # For simplicity, use raw z-score sum
    return Xz[:, core_indices].sum(axis=1)


def threshold_top_k(scores, k_frac=THRESHOLD_FRAC):
    """Convert continuous scores to binary via top-k% threshold."""
    threshold = np.quantile(scores, 1 - k_frac)
    return (scores > threshold).astype(int)


def main():
    print("=" * 70)
    print("HBFWS — Hierarchical Bayesian Feature-Weight Shrinkage")
    print("=" * 70)
    print(f"Pathogens: {len(ALL_PATHOGENS)}")
    print(f"Families: {len(ALL_FAMILIES)} ({ALL_FAMILIES})")
    print(f"Singletons: 5/8 ({sum(1 for f in ALL_FAMILIES if sum(1 for p in PATHOGEN_TO_FAMILY.values() if p == f) == 1)} families)")
    print()

    # Load all pathogens
    pathogen_data = {}
    for p in ALL_PATHOGENS:
        d = load_pathogen(p)
        if d is None:
            print(f"  [SKIP] {p}: no data or degenerate Layer A")
            continue
        pathogen_data[p] = d
    print(f"Loaded {len(pathogen_data)} pathogens with valid Layer A")
    print()

    # Standardize features globally (fit on all pathogens, will refit per fold below)
    # Track per-pathogen MCC for HBFWS, EqualWeight 4-core, fixed-4 baseline
    fold_results = []

    for fold_idx, held_out in enumerate(pathogen_data.keys()):
        print(f"  Fold {fold_idx+1}/{len(pathogen_data)}: held-out = {held_out}")

        # Stack training data
        X_train, y_train, _, f_idx_train, train_pathogens = build_stacked_data(
            pathogen_data, exclude=held_out
        )
        # Held-out
        X_test = pathogen_data[held_out]["X"]
        y_test = pathogen_data[held_out]["y"]
        family_held_out = PATHOGEN_TO_FAMILY[held_out]
        f_idx_held_out = FAMILY_TO_IDX[family_held_out]

        # Standardize features (fit on training, apply to both)
        scaler = StandardScaler()
        X_train_z = scaler.fit_transform(X_train)
        X_test_z = scaler.transform(X_test)

        # ---- Fit HBFWS ----
        try:
            trace = fit_hbfws(X_train_z, y_train, f_idx_train, n_features=10, n_families=8)
            scores_hbfws = predict_held_out(trace, X_test_z, f_idx_held_out, n_features=10)
            y_pred_hbfws = threshold_top_k(scores_hbfws, THRESHOLD_FRAC)
            mcc_hbfws = safe_mcc(y_test, y_pred_hbfws)
        except Exception as e:
            print(f"    [HBFWS FIT/PREDICT ERROR] {e}")
            mcc_hbfws = np.nan
            trace = None

        # Diagnostics in separate try so failure doesn't wipe MCC
        rhat_max = np.nan
        ess_min = np.nan
        if trace is not None:
            try:
                rhat_max = float(az.rhat(trace).to_array().max().values)
            except Exception as e:
                print(f"    [rhat warn] {e}")
            try:
                ess_min = float(az.ess(trace).to_array().min().values)
            except Exception as e:
                print(f"    [ess warn] {e}")

        # ---- EqualWeight 4-core baseline (raw, no sign fitting) ----
        scores_eq4 = equal_weight_baseline(X_test, core_indices=[FEATURE_NAMES.index(f) for f in CORE_4])
        y_pred_eq4 = threshold_top_k(scores_eq4, THRESHOLD_FRAC)
        mcc_eq4 = safe_mcc(y_test, y_pred_eq4)

        # ---- EqualWeight 10-feature ----
        scores_eq10 = equal_weight_baseline(X_test, core_indices=list(range(10)))
        y_pred_eq10 = threshold_top_k(scores_eq10, THRESHOLD_FRAC)
        mcc_eq10 = safe_mcc(y_test, y_pred_eq10)

        n_test = len(y_test)
        n_pos = int(y_test.sum())
        is_singleton = sum(1 for q in PATHOGEN_TO_FAMILY.values() if q == family_held_out) == 1

        fold_results.append({
            "fold": fold_idx,
            "pathogen": held_out,
            "family": family_held_out,
            "is_singleton_family": is_singleton,
            "n_test": n_test,
            "n_positive": n_pos,
            "mcc_hbfws": mcc_hbfws,
            "mcc_eq4": mcc_eq4,
            "mcc_eq10": mcc_eq10,
            "delta_hbfws_vs_eq4": mcc_hbfws - mcc_eq4 if not np.isnan(mcc_hbfws) else np.nan,
            "rhat_max": rhat_max,
            "ess_bulk_min": ess_min,
        })
        print(f"    HBFWS: {mcc_hbfws:+.4f}  EqualWeight-4core: {mcc_eq4:+.4f}  delta: {mcc_hbfws - mcc_eq4:+.4f}  R-hat: {rhat_max:.3f}  singleton: {is_singleton}")

    # Aggregate
    df = pd.DataFrame(fold_results)
    out_csv = OUT_DIR / "hbfws_lopo_results.csv"
    df.to_csv(out_csv, index=False)
    print()
    print("=" * 70)
    print("HBFWS LOPO Results Summary")
    print("=" * 70)
    print(f"  HBFWS mean MCC:       {df['mcc_hbfws'].mean():.4f} (sd {df['mcc_hbfws'].std():.4f})")
    print(f"  EqualWeight-4core:    {df['mcc_eq4'].mean():.4f} (sd {df['mcc_eq4'].std():.4f})")
    print(f"  EqualWeight-10feat:   {df['mcc_eq10'].mean():.4f} (sd {df['mcc_eq10'].std():.4f})")
    print(f"  Mean delta (HBFWS - EQ-4): {df['delta_hbfws_vs_eq4'].mean():+.4f}")
    print()
    print("By family-membership:")
    print(f"  Paired families ({(~df['is_singleton_family']).sum()} folds): HBFWS {df.loc[~df['is_singleton_family'], 'mcc_hbfws'].mean():.4f}, delta {df.loc[~df['is_singleton_family'], 'delta_hbfws_vs_eq4'].mean():+.4f}")
    print(f"  Singletons      ({df['is_singleton_family'].sum()} folds): HBFWS {df.loc[df['is_singleton_family'], 'mcc_hbfws'].mean():.4f}, delta {df.loc[df['is_singleton_family'], 'delta_hbfws_vs_eq4'].mean():+.4f}")
    print()
    # Paired Wilcoxon vs EqualWeight-4core (the primary baseline)
    deltas = df["delta_hbfws_vs_eq4"].dropna()
    if len(deltas) > 0:
        try:
            stat, pval = wilcoxon(deltas, alternative="greater")
            print(f"Paired Wilcoxon (HBFWS > EqualWeight-4core, one-sided):")
            print(f"  W = {stat:.2f}, p = {pval:.4f}")
            if pval < 0.05:
                print(f"  ✓ Reject H0: HBFWS beats EqualWeight (p < 0.05)")
            else:
                print(f"  ✗ Fail to reject H0: HBFWS does not beat EqualWeight (pre-registered prior 15-25%)")
        except ValueError as e:
            print(f"  Wilcoxon test failed: {e}")
    print()
    print(f"Results saved to: {out_csv}")
    return df


if __name__ == "__main__":
    df = main()
