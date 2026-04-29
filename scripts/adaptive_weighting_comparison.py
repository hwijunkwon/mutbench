#!/usr/bin/env python3
"""Comprehensive adaptive-weighting comparison (Cycle 7B).

Pre-registered hypotheses: each method tested against EqualWeight-4core baseline
(LOPO mean MCC = 0.078) under paired Wilcoxon one-sided greater. Pre-registered
prior on each method beating EQ-4: 15-30%.

Methods tested:
  M1  XGBoost stacked (gradient boosting; non-parametric, non-linear)
  M2  Random Forest stacked (parallel sanity check)
  M3  Logistic Regression L1 (simple linear baseline)
  M4  Algorithm Selection Classifier (pathogen meta-features -> best feature)
  M5  HBFWS-phylo (HBFWS but pooling by genome polarity instead of ICTV)
  M6  Per-pathogen feature ranking aggregation (training-fold rank ensemble)

Baselines:
  B0  EqualWeight 4-core (homoplasy, plddt, entropy, freq) -- canonical
  B1  EqualWeight 10-feat (all features)
  B2  HBFWS (v171 result, archived in hbfws_lopo_results.csv)

12-pathogen nested-LOPO; same threshold (top-10%); same folds.

Usage: python3 scripts/adaptive_weighting_comparison.py
"""

from __future__ import annotations

import warnings
from pathlib import Path

import numpy as np
import pandas as pd
from sklearn.metrics import matthews_corrcoef
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from scipy.stats import wilcoxon

try:
    from xgboost import XGBClassifier
    HAS_XGB = True
except ImportError:
    HAS_XGB = False
    print("[warn] xgboost not available — skipping M1")

warnings.filterwarnings("ignore")

PROJECT_ROOT = Path(__file__).resolve().parent.parent
FEATURE_DIR = PROJECT_ROOT / "results" / "mutbench" / "feature_analysis"
OUT_DIR = PROJECT_ROOT / "results" / "mutbench"

ALL_PATHOGENS = [
    "SARS-CoV-2", "H3N2", "Norovirus", "HIV-1", "Dengue",
    "RSV", "Influenza_B", "MERS", "HCV",
    "Zika", "Rabies", "EV-A71",
]

# ICTV families (also used for HBFWS-phylo grouping below)
PATHOGEN_TO_FAMILY = {
    "SARS-CoV-2": "Coronaviridae",
    "MERS": "Coronaviridae",
    "H3N2": "Orthomyxoviridae",
    "Influenza_B": "Orthomyxoviridae",
    "HCV": "Flaviviridae",
    "Dengue": "Flaviviridae",
    "Zika": "Flaviviridae",
    "Norovirus": "Caliciviridae",
    "HIV-1": "Retroviridae",
    "RSV": "Pneumoviridae",
    "Rabies": "Rhabdoviridae",
    "EV-A71": "Picornaviridae",
}

# Pathogen-level meta-features (for Algorithm Selection Classifier M4 + HBFWS-phylo M5)
# Manually curated from public taxonomy; ssrna_polarity = +1 for ssRNA(+), -1 for ssRNA(-)
# enveloped: 1 if lipid-enveloped virion, 0 otherwise
# genome_size: nominal kb; surface_protein_type: gp=glycoprotein, cap=capsid
PATHOGEN_META = {
    "SARS-CoV-2":  {"ssrna_pol": +1, "enveloped": 1, "genome_kb": 30, "surface": "gp"},
    "MERS":        {"ssrna_pol": +1, "enveloped": 1, "genome_kb": 30, "surface": "gp"},
    "H3N2":        {"ssrna_pol": -1, "enveloped": 1, "genome_kb": 14, "surface": "gp"},
    "Influenza_B": {"ssrna_pol": -1, "enveloped": 1, "genome_kb": 14, "surface": "gp"},
    "HCV":         {"ssrna_pol": +1, "enveloped": 1, "genome_kb":  9, "surface": "gp"},
    "Dengue":      {"ssrna_pol": +1, "enveloped": 1, "genome_kb": 11, "surface": "gp"},
    "Zika":        {"ssrna_pol": +1, "enveloped": 1, "genome_kb": 11, "surface": "gp"},
    "Norovirus":   {"ssrna_pol": +1, "enveloped": 0, "genome_kb":  7, "surface": "cap"},
    "HIV-1":       {"ssrna_pol": +1, "enveloped": 1, "genome_kb": 10, "surface": "gp"},
    "RSV":         {"ssrna_pol": -1, "enveloped": 1, "genome_kb": 15, "surface": "gp"},
    "Rabies":      {"ssrna_pol": -1, "enveloped": 1, "genome_kb": 12, "surface": "gp"},
    "EV-A71":      {"ssrna_pol": +1, "enveloped": 0, "genome_kb":  7, "surface": "cap"},
}

# HBFWS-phylo grouping: 4 groups instead of 8 ICTV families
#   group_A: ssRNA(+) enveloped gp viruses (SARS, MERS, HCV, Dengue, Zika, HIV-1)
#   group_B: ssRNA(-) enveloped gp viruses (H3N2, InfB, RSV, Rabies)
#   group_C: ssRNA(+) non-enveloped capsid viruses (Norovirus, EV-A71)
#   group_D: empty (placeholder for symmetry)
def phylo_group(p):
    m = PATHOGEN_META[p]
    if m["enveloped"] == 1 and m["ssrna_pol"] == +1: return 0
    if m["enveloped"] == 1 and m["ssrna_pol"] == -1: return 1
    if m["enveloped"] == 0:                          return 2
    return 3

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
    if y_pred.sum() == 0 or y_pred.sum() == len(y_pred): return 0.0
    if y_true.sum() == 0 or y_true.sum() == len(y_true): return 0.0
    return matthews_corrcoef(y_true, y_pred)


def threshold_top_k(scores, frac=THRESHOLD_FRAC):
    if len(scores) == 0: return np.array([], dtype=int)
    threshold = np.quantile(scores, 1 - frac)
    return (scores > threshold).astype(int)


def load_pathogen(p):
    path = FEATURE_DIR / f"feature_matrix_{p}.csv"
    if not path.exists(): return None
    df = pd.read_csv(path)
    if "layer_a" not in df.columns: return None
    y = df["layer_a"].values.astype(int)
    if y.sum() == 0 or y.sum() == len(y): return None
    feats = []
    for f in FEATURE_NAMES:
        feats.append(df[f].values if f in df.columns else np.zeros(len(df)))
    X = np.array(feats).T
    X = np.nan_to_num(X, nan=0.0, posinf=0.0, neginf=0.0)
    return {"X": X, "y": y, "n": len(df)}


def equal_weight_baseline(X_test, core_indices):
    Xz = StandardScaler().fit_transform(X_test)
    return Xz[:, core_indices].sum(axis=1)


def stack_data(pathogen_data, exclude=None):
    X_list, y_list, p_list = [], [], []
    pathogens_used = []
    for p, d in pathogen_data.items():
        if p == exclude: continue
        X_list.append(d["X"])
        y_list.append(d["y"])
        p_list.append(np.full(d["n"], p, dtype=object))
        pathogens_used.append(p)
    X = np.vstack(X_list)
    y = np.concatenate(y_list)
    p = np.concatenate(p_list)
    return X, y, p, pathogens_used


# ============================================================
# M1 XGBoost stacked
# ============================================================
def m1_xgboost(X_train, y_train, X_test, scaler):
    if not HAS_XGB: return None
    Xz = scaler.transform(X_test)
    Xtz = scaler.transform(X_train)
    clf = XGBClassifier(
        n_estimators=200, max_depth=4, learning_rate=0.05,
        subsample=0.8, colsample_bytree=0.8,
        reg_lambda=1.0, scale_pos_weight=(y_train == 0).sum() / max(y_train.sum(), 1),
        random_state=RANDOM_SEED, n_jobs=-1, eval_metric="logloss",
    )
    clf.fit(Xtz, y_train)
    return clf.predict_proba(Xz)[:, 1]


# ============================================================
# M2 Random Forest stacked
# ============================================================
def m2_random_forest(X_train, y_train, X_test, scaler):
    Xz = scaler.transform(X_test)
    Xtz = scaler.transform(X_train)
    clf = RandomForestClassifier(
        n_estimators=300, max_depth=8, min_samples_leaf=20,
        class_weight="balanced", n_jobs=-1, random_state=RANDOM_SEED,
    )
    clf.fit(Xtz, y_train)
    return clf.predict_proba(Xz)[:, 1]


# ============================================================
# M3 Logistic Regression L1
# ============================================================
def m3_logistic_l1(X_train, y_train, X_test, scaler):
    Xz = scaler.transform(X_test)
    Xtz = scaler.transform(X_train)
    clf = LogisticRegression(
        penalty="l1", solver="liblinear", C=1.0,
        class_weight="balanced", random_state=RANDOM_SEED, max_iter=1000,
    )
    clf.fit(Xtz, y_train)
    return clf.predict_proba(Xz)[:, 1]


# ============================================================
# M4 Algorithm Selection Classifier
#   Train: each pathogen -> best single feature (by training fold MCC)
#          plus pathogen meta-features as input
#   Predict: held-out pathogen meta -> predicted best feature -> use that scoring
# ============================================================
def m4_algorithm_selection(pathogen_data, train_pathogens, test_pathogen, scaler_dict):
    """For each training pathogen, find best single feature (training MCC).
    Build meta-classifier (pathogen meta-features -> best feature index).
    Use it to pick best feature for test pathogen."""
    # Step 1: per training pathogen, find best single feature index
    train_meta = []
    train_best = []
    for p in train_pathogens:
        d = pathogen_data[p]
        best_f, best_mcc = -1, -np.inf
        for f_idx in range(len(FEATURE_NAMES)):
            scores = d["X"][:, f_idx]
            for sign in (-1, +1):
                y_pred = threshold_top_k(sign * scores)
                m = safe_mcc(d["y"], y_pred)
                if m > best_mcc:
                    best_mcc = m
                    best_f = f_idx
        train_best.append(best_f)
        meta = PATHOGEN_META[p]
        train_meta.append([meta["ssrna_pol"], meta["enveloped"], meta["genome_kb"],
                           1 if meta["surface"] == "gp" else 0])
    train_meta = np.array(train_meta, dtype=float)
    train_best = np.array(train_best)

    # Step 2: meta-classifier (multi-class)
    # With n=11 training pathogens, just use 1-NN on meta-features (simplest)
    test_meta_p = PATHOGEN_META[test_pathogen]
    test_meta = np.array([test_meta_p["ssrna_pol"], test_meta_p["enveloped"],
                          test_meta_p["genome_kb"], 1 if test_meta_p["surface"] == "gp" else 0])
    # Standardize meta-features (genome_kb has different scale)
    meta_mean = train_meta.mean(axis=0)
    meta_std = train_meta.std(axis=0)
    meta_std[meta_std == 0] = 1.0
    train_meta_z = (train_meta - meta_mean) / meta_std
    test_meta_z = (test_meta - meta_mean) / meta_std
    # 1-NN by Euclidean distance
    dists = np.linalg.norm(train_meta_z - test_meta_z, axis=1)
    nearest_idx = np.argmin(dists)
    predicted_feature = train_best[nearest_idx]

    # Step 3: apply predicted feature to test pathogen
    d_test = pathogen_data[test_pathogen]
    feat_scores = d_test["X"][:, predicted_feature]
    # Determine sign from training pathogen
    d_nearest = pathogen_data[train_pathogens[nearest_idx]]
    sign_pos = safe_mcc(d_nearest["y"], threshold_top_k(d_nearest["X"][:, predicted_feature]))
    sign_neg = safe_mcc(d_nearest["y"], threshold_top_k(-d_nearest["X"][:, predicted_feature]))
    sign = +1 if sign_pos >= sign_neg else -1
    return sign * feat_scores, predicted_feature, FEATURE_NAMES[predicted_feature]


# ============================================================
# M5 HBFWS-phylo (pooling by polarity/envelope group instead of ICTV)
# ============================================================
def m5_hbfws_phylo(X_train, y_train, group_idx_train, X_test, group_idx_test_p, scaler, n_features=10, n_groups=3):
    try:
        import pymc as pm
    except ImportError:
        return None
    Xtz = scaler.transform(X_train)
    Xz = scaler.transform(X_test)
    with pm.Model() as model:
        sigma_feature = pm.HalfNormal("sigma_feature", sigma=0.3)
        sigma_group = pm.HalfNormal("sigma_group", sigma=0.3)
        mu = pm.Normal("mu", mu=0.0, sigma=0.5)
        w_raw = pm.Normal("w_raw", mu=0.0, sigma=1.0, shape=n_features)
        w = pm.Deterministic("w", sigma_feature * w_raw)
        gamma_raw = pm.Normal("gamma_raw", mu=0.0, sigma=1.0, shape=n_groups)
        gamma = pm.Deterministic("gamma", sigma_group * gamma_raw)
        eta = mu + gamma[group_idx_train] + pm.math.dot(Xtz, w)
        pm.Bernoulli("y_obs", logit_p=eta, observed=y_train)
        trace = pm.sample(draws=600, tune=600, chains=2, random_seed=RANDOM_SEED,
                         target_accept=0.95, progressbar=False, return_inferencedata=True)
    w_post = trace.posterior["w"].values.reshape(-1, n_features).mean(axis=0)
    gamma_post = trace.posterior["gamma"].values.reshape(-1, n_groups)
    mu_post = float(trace.posterior["mu"].values.mean())
    gamma_test = float(gamma_post[:, group_idx_test_p].mean())
    return mu_post + gamma_test + Xz @ w_post


# ============================================================
# M6 Per-pathogen feature ranking aggregation
#   For each training pathogen, rank features by training MCC.
#   Average ranks across training pathogens.
#   Use top-3 features as uniform z-ensemble on test.
# ============================================================
def m6_rank_aggregation(pathogen_data, train_pathogens, X_test, scaler, top_k=3):
    feat_ranks = []
    for p in train_pathogens:
        d = pathogen_data[p]
        per_feat_mcc = []
        for f_idx in range(len(FEATURE_NAMES)):
            scores = d["X"][:, f_idx]
            best_sign_mcc = max(
                safe_mcc(d["y"], threshold_top_k(scores)),
                safe_mcc(d["y"], threshold_top_k(-scores)),
            )
            per_feat_mcc.append(best_sign_mcc)
        # Rank: best = 1, worst = 10
        ranks = pd.Series(per_feat_mcc).rank(ascending=False, method="min").values
        feat_ranks.append(ranks)
    avg_ranks = np.mean(feat_ranks, axis=0)
    top_features = np.argsort(avg_ranks)[:top_k]
    Xz = scaler.transform(X_test)
    # Determine signs from training average
    signs = []
    for f_idx in top_features:
        sign_score = 0.0
        for p in train_pathogens:
            d = pathogen_data[p]
            s = d["X"][:, f_idx]
            mcc_pos = safe_mcc(d["y"], threshold_top_k(s))
            mcc_neg = safe_mcc(d["y"], threshold_top_k(-s))
            sign_score += (1 if mcc_pos >= mcc_neg else -1)
        signs.append(+1 if sign_score >= 0 else -1)
    return Xz[:, top_features] @ np.array(signs), [FEATURE_NAMES[i] for i in top_features]


# ============================================================
# Main
# ============================================================
def main():
    print("=" * 78)
    print("Adaptive Weighting Comprehensive Comparison (Cycle 7B)")
    print("=" * 78)
    pathogen_data = {}
    for p in ALL_PATHOGENS:
        d = load_pathogen(p)
        if d is None:
            print(f"  [SKIP] {p}")
            continue
        pathogen_data[p] = d
    print(f"Loaded {len(pathogen_data)} pathogens")

    fold_results = []
    for fold_idx, held_out in enumerate(pathogen_data.keys()):
        print(f"\n  Fold {fold_idx+1}/{len(pathogen_data)}: held-out = {held_out}")
        X_train, y_train, p_train, train_paths = stack_data(pathogen_data, exclude=held_out)
        X_test = pathogen_data[held_out]["X"]
        y_test = pathogen_data[held_out]["y"]

        scaler = StandardScaler()
        scaler.fit(X_train)

        # B0 EQ-4
        scores_eq4 = equal_weight_baseline(X_test, [FEATURE_NAMES.index(f) for f in CORE_4])
        mcc_eq4 = safe_mcc(y_test, threshold_top_k(scores_eq4))

        # B1 EQ-10
        scores_eq10 = equal_weight_baseline(X_test, list(range(10)))
        mcc_eq10 = safe_mcc(y_test, threshold_top_k(scores_eq10))

        # M1 XGBoost
        try:
            scores_xgb = m1_xgboost(X_train, y_train, X_test, scaler)
            mcc_xgb = safe_mcc(y_test, threshold_top_k(scores_xgb)) if scores_xgb is not None else np.nan
        except Exception as e:
            print(f"    [M1 err] {e}")
            mcc_xgb = np.nan

        # M2 RF
        try:
            scores_rf = m2_random_forest(X_train, y_train, X_test, scaler)
            mcc_rf = safe_mcc(y_test, threshold_top_k(scores_rf))
        except Exception as e:
            print(f"    [M2 err] {e}")
            mcc_rf = np.nan

        # M3 Logistic L1
        try:
            scores_lr = m3_logistic_l1(X_train, y_train, X_test, scaler)
            mcc_lr = safe_mcc(y_test, threshold_top_k(scores_lr))
        except Exception as e:
            print(f"    [M3 err] {e}")
            mcc_lr = np.nan

        # M4 Algorithm Selection
        try:
            scores_as, pred_feat_idx, pred_feat_name = m4_algorithm_selection(
                pathogen_data, train_paths, held_out, None
            )
            mcc_as = safe_mcc(y_test, threshold_top_k(scores_as))
        except Exception as e:
            print(f"    [M4 err] {e}")
            mcc_as = np.nan
            pred_feat_name = "?"

        # M5 HBFWS-phylo
        try:
            group_idx_train = np.array([phylo_group(p) for p in p_train], dtype=int)
            group_idx_test = phylo_group(held_out)
            scores_hbfwsp = m5_hbfws_phylo(X_train, y_train, group_idx_train,
                                            X_test, group_idx_test, scaler)
            mcc_hbfwsp = safe_mcc(y_test, threshold_top_k(scores_hbfwsp)) if scores_hbfwsp is not None else np.nan
        except Exception as e:
            print(f"    [M5 err] {e}")
            mcc_hbfwsp = np.nan

        # M6 Rank aggregation
        try:
            scores_rank, top_feats = m6_rank_aggregation(pathogen_data, train_paths, X_test, scaler)
            mcc_rank = safe_mcc(y_test, threshold_top_k(scores_rank))
        except Exception as e:
            print(f"    [M6 err] {e}")
            mcc_rank = np.nan
            top_feats = []

        print(f"    EQ-4 {mcc_eq4:+.3f}  EQ-10 {mcc_eq10:+.3f}  XGB {mcc_xgb:+.3f}  RF {mcc_rf:+.3f}  LR {mcc_lr:+.3f}  AS({pred_feat_name}) {mcc_as:+.3f}  HBFWSp {mcc_hbfwsp:+.3f}  Rank({','.join(top_feats[:3])}) {mcc_rank:+.3f}")

        fold_results.append({
            "fold": fold_idx, "pathogen": held_out,
            "mcc_eq4": mcc_eq4, "mcc_eq10": mcc_eq10,
            "mcc_xgb": mcc_xgb, "mcc_rf": mcc_rf, "mcc_lr": mcc_lr,
            "mcc_alg_select": mcc_as, "alg_select_feature": pred_feat_name,
            "mcc_hbfws_phylo": mcc_hbfwsp,
            "mcc_rank_agg": mcc_rank, "rank_top_features": ",".join(top_feats),
        })

    df = pd.DataFrame(fold_results)
    out = OUT_DIR / "adaptive_weighting_comparison.csv"
    df.to_csv(out, index=False)

    print("\n" + "=" * 78)
    print("Summary")
    print("=" * 78)
    print(f"{'Method':<24} {'mean MCC':>10} {'sd':>8} {'Δ vs EQ4':>10} {'Wilcoxon p':>12}")
    methods = [
        ("EQ-4 (baseline)",       "mcc_eq4"),
        ("EQ-10",                 "mcc_eq10"),
        ("XGBoost",               "mcc_xgb"),
        ("Random Forest",         "mcc_rf"),
        ("Logistic L1",           "mcc_lr"),
        ("Algorithm Selection",   "mcc_alg_select"),
        ("HBFWS-phylo",           "mcc_hbfws_phylo"),
        ("Rank Aggregation",      "mcc_rank_agg"),
    ]
    eq4 = df["mcc_eq4"].dropna()
    for name, col in methods:
        x = df[col].dropna()
        delta = x - df["mcc_eq4"].loc[x.index]
        if col == "mcc_eq4":
            print(f"{name:<24} {x.mean():+.4f}    {x.std():.4f}     ----        ----")
        else:
            try:
                w_stat, w_p = wilcoxon(delta.values, alternative="greater")
                print(f"{name:<24} {x.mean():+.4f}    {x.std():.4f}   {delta.mean():+.4f}     {w_p:.4f}")
            except ValueError:
                print(f"{name:<24} {x.mean():+.4f}    {x.std():.4f}   {delta.mean():+.4f}     n/a")
    print(f"\nResults: {out}")
    return df


if __name__ == "__main__":
    main()
