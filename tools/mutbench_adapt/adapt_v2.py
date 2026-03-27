#!/usr/bin/env python3
"""MutBench-Adapt v2: Multi-strategy pathogen-adaptive hotspot detection.

Improvements over v1:
  1. Multiple strategies (kNN-cosine, per-feature AUC, correlation-aware, oracle)
  2. Multiple threshold strategies (top-3%, 5%, 10%, adaptive MAD)
  3. Robust MCC computation via sklearn

Usage:
    python tools/mutbench_adapt/adapt_v2.py
"""

from __future__ import annotations

import sys
import warnings
from pathlib import Path

import numpy as np
import pandas as pd
from scipy.spatial.distance import cosine as cosine_dist
from scipy.stats import median_abs_deviation, skew
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import matthews_corrcoef, roc_auc_score

warnings.filterwarnings("ignore", category=RuntimeWarning)

# ---------------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------------
PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
FEATURE_DIR = PROJECT_ROOT / "results" / "mutbench" / "feature_analysis"
RESULTS_DIR = PROJECT_ROOT / "results" / "mutbench"

sys.path.insert(0, str(PROJECT_ROOT / "tools"))
from mutbench.ground_truth.multilayer_gt import get_gt_adaptive  # noqa: E402

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------
ALL_PATHOGENS = [
    "SARS-CoV-2", "H3N2", "Norovirus", "HIV-1", "Dengue",
    "RSV", "Influenza_B", "MERS", "HCV",
    "Zika", "Rabies", "EV-A71",
]

FEATURE_NAMES = [
    "freq", "entropy", "rare_freq", "homoplasy", "esm2_llr",
    "plddt", "sasa", "grantham", "dnds_proxy", "semantic_change",
]

# Feature groups for Strategy C
FEATURE_GROUPS = {
    "frequency": ["freq", "entropy", "dnds_proxy"],
    "structural_ml": ["esm2_llr", "semantic_change"],
    "structural_phys": ["plddt", "sasa"],
    "homoplasy": ["homoplasy"],
    "biochem": ["grantham"],
}

# Threshold configurations
THRESHOLD_CONFIGS = {
    "top3": {"type": "topk", "frac": 0.03},
    "top5": {"type": "topk", "frac": 0.05},
    "top10": {"type": "topk", "frac": 0.10},
    "mad2": {"type": "mad", "multiplier": 2.0},
}

STRATEGY_NAMES = ["knn_cosine", "top3_auc", "corr_ensemble", "oracle"]


# ---------------------------------------------------------------------------
# Data loading
# ---------------------------------------------------------------------------
def load_feature_matrix(pathogen: str) -> pd.DataFrame:
    path = FEATURE_DIR / f"feature_matrix_{pathogen}.csv"
    if not path.exists():
        raise FileNotFoundError(f"Feature matrix not found: {path}")
    return pd.read_csv(path)


def extract_profile(df: pd.DataFrame) -> np.ndarray:
    freq = df["freq"].values
    entropy = df["entropy"].values
    n_positions = len(df)
    return np.array([
        n_positions, n_positions,
        np.mean(freq), np.mean(entropy),
        np.mean(freq > 0.01), np.mean(freq == 0.0),
        np.max(freq),
        skew(freq) if np.std(freq) > 0 else 0.0,
    ])


# ---------------------------------------------------------------------------
# RF importance (cached)
# ---------------------------------------------------------------------------
_rf_cache: dict[str, np.ndarray] = {}


def compute_rf_importance(df: pd.DataFrame, pathogen: str = "",
                          n_estimators: int = 500) -> np.ndarray:
    if pathogen and pathogen in _rf_cache:
        return _rf_cache[pathogen]

    X = np.nan_to_num(df[FEATURE_NAMES].values.copy(), nan=0.0, posinf=0.0, neginf=0.0)
    y = df["layer_a"].values.astype(int)
    if y.sum() < 2:
        return np.ones(10) / 10.0

    rf = RandomForestClassifier(
        n_estimators=n_estimators, max_depth=None, min_samples_leaf=3,
        class_weight="balanced", random_state=42, n_jobs=-1,
    )
    rf.fit(X, y)
    imp = rf.feature_importances_
    if pathogen:
        _rf_cache[pathogen] = imp
    return imp


def compute_feature_aucs(df: pd.DataFrame) -> np.ndarray:
    """Compute per-feature AUC for a pathogen. Returns (10,) array."""
    y = df["layer_a"].values.astype(int)
    aucs = np.full(10, 0.5)
    if y.sum() < 2 or (len(y) - y.sum()) < 2:
        return aucs
    for i, feat in enumerate(FEATURE_NAMES):
        x = np.nan_to_num(df[feat].values.copy(), nan=0.0)
        try:
            aucs[i] = roc_auc_score(y, x)
        except ValueError:
            aucs[i] = 0.5
    return aucs


def compute_feature_signs(df: pd.DataFrame) -> np.ndarray:
    aucs = compute_feature_aucs(df)
    signs = np.ones(10)
    for i in range(10):
        if aucs[i] < 0.5:
            signs[i] = -1.0
    return signs


# ---------------------------------------------------------------------------
# Scoring & thresholding
# ---------------------------------------------------------------------------
def compute_scores(df: pd.DataFrame, w: np.ndarray, s: np.ndarray) -> np.ndarray:
    """Compute weighted z-score combination. Returns raw scores array."""
    F = np.nan_to_num(df[FEATURE_NAMES].values.copy(), nan=0.0, posinf=0.0, neginf=0.0)
    available = np.std(F, axis=0) > 1e-10

    w_adj = w.copy()
    w_adj[~available] = 0.0
    if w_adj.sum() > 0:
        w_adj /= w_adj.sum()

    # Z-score normalize
    Z = np.zeros_like(F)
    for f_idx in range(10):
        if available[f_idx]:
            mu_f, std_f = np.mean(F[:, f_idx]), np.std(F[:, f_idx])
            if std_f > 0:
                Z[:, f_idx] = (F[:, f_idx] - mu_f) / std_f

    # Apply sign and weight
    return (Z * np.sign(s)) @ w_adj


def apply_threshold(scores: np.ndarray, config: dict) -> np.ndarray:
    """Apply threshold to scores, return boolean prediction."""
    if config["type"] == "topk":
        thr = np.percentile(scores, 100 * (1 - config["frac"]))
        return scores >= thr
    elif config["type"] == "mad":
        med = np.median(scores)
        mad = median_abs_deviation(scores, nan_policy="omit")
        if mad < 1e-10:
            mad = np.std(scores)
        thr = med + config["multiplier"] * mad
        return scores >= thr
    else:
        raise ValueError(f"Unknown threshold type: {config['type']}")


def safe_mcc(y_true: np.ndarray, y_pred: np.ndarray) -> float:
    """Compute MCC with edge-case handling."""
    y_true = np.asarray(y_true, dtype=int)
    y_pred = np.asarray(y_pred, dtype=int)
    if y_pred.sum() == 0 or y_pred.sum() == len(y_pred):
        return 0.0
    if y_true.sum() == 0 or y_true.sum() == len(y_true):
        return 0.0
    return matthews_corrcoef(y_true, y_pred)


# ---------------------------------------------------------------------------
# Strategy A: kNN-cosine (k=2, similarity^2 weighting)
# ---------------------------------------------------------------------------
def strategy_knn_cosine(
    target_profile: np.ndarray,
    P_ref: np.ndarray,
    W_ref: np.ndarray,
    S_ref: np.ndarray,
    mu_sigma: np.ndarray,
    k: int = 2,
) -> tuple[np.ndarray, np.ndarray, list[tuple[str, float]]]:
    """kNN with cosine similarity and squared-similarity weighting."""
    mu, sigma = mu_sigma[0], mu_sigma[1]
    q_std = (target_profile - mu) / sigma
    P_std = (P_ref - mu) / sigma

    n_ref = len(P_ref)
    # Cosine similarity (1 - cosine distance)
    similarities = np.array([
        1.0 - cosine_dist(q_std, P_std[j]) if np.linalg.norm(P_std[j]) > 0 else 0.0
        for j in range(n_ref)
    ])
    # Clamp negatives
    similarities = np.maximum(similarities, 0.0)

    k_actual = min(k, n_ref)
    nn_idx = np.argsort(-similarities)[:k_actual]  # highest similarity first
    nn_sim = similarities[nn_idx]

    # Similarity^2 weighting
    sim_sq = nn_sim ** 2
    total = sim_sq.sum()
    if total < 1e-12:
        alpha = np.ones(k_actual) / k_actual
    else:
        alpha = sim_sq / total

    w = sum(alpha[i] * W_ref[nn_idx[i]] for i in range(k_actual))
    s = sum(alpha[i] * S_ref[nn_idx[i]] for i in range(k_actual))

    return w, s, [(int(nn_idx[i]), float(nn_sim[i])) for i in range(k_actual)]


# ---------------------------------------------------------------------------
# Strategy B: Per-feature AUC top-3 from training set
# ---------------------------------------------------------------------------
def strategy_top3_auc(
    auc_matrix: np.ndarray,  # (n_train, 10) per-feature AUC for training pathogens
    sign_matrix: np.ndarray,  # (n_train, 10) signs
) -> tuple[np.ndarray, np.ndarray]:
    """Pick top-3 features by mean |AUC - 0.5| across training pathogens."""
    # Mean effective AUC (distance from 0.5)
    eff_auc = np.abs(auc_matrix - 0.5).mean(axis=0)
    top3_idx = np.argsort(-eff_auc)[:3]

    w = np.zeros(10)
    w[top3_idx] = 1.0 / 3.0

    # Sign: majority vote from training
    s = np.sign(sign_matrix.mean(axis=0))
    s[s == 0] = 1.0

    return w, s


# ---------------------------------------------------------------------------
# Strategy C: Correlation-aware group ensemble
# ---------------------------------------------------------------------------
def strategy_corr_ensemble(
    auc_matrix: np.ndarray,  # (n_train, 10) AUCs
    sign_matrix: np.ndarray,  # (n_train, 10) signs
) -> tuple[np.ndarray, np.ndarray]:
    """Pick best feature per group, weight groups equally."""
    mean_eff_auc = np.abs(auc_matrix - 0.5).mean(axis=0)
    n_groups = len(FEATURE_GROUPS)

    w = np.zeros(10)
    s = np.sign(sign_matrix.mean(axis=0))
    s[s == 0] = 1.0

    for group_name, feats in FEATURE_GROUPS.items():
        idxs = [FEATURE_NAMES.index(f) for f in feats]
        best_idx = idxs[np.argmax(mean_eff_auc[idxs])]
        w[best_idx] = 1.0 / n_groups

    return w, s


# ---------------------------------------------------------------------------
# Strategy D: Oracle (uses held-out pathogen's own RF importance)
# ---------------------------------------------------------------------------
def strategy_oracle(df_target: pd.DataFrame, pathogen: str) -> tuple[np.ndarray, np.ndarray]:
    """Oracle: use the held-out pathogen's own RF importance and signs."""
    w = compute_rf_importance(df_target, pathogen=f"oracle_{pathogen}")
    s = compute_feature_signs(df_target)
    return w, s


# ---------------------------------------------------------------------------
# Baselines
# ---------------------------------------------------------------------------
def baseline_freq(df: pd.DataFrame, config: dict) -> np.ndarray:
    scores = df["freq"].values.copy()
    return apply_threshold(scores, config)


def baseline_entropy(df: pd.DataFrame, config: dict) -> np.ndarray:
    scores = df["entropy"].values.copy()
    return apply_threshold(scores, config)


def baseline_equal_weight(df: pd.DataFrame, config: dict) -> np.ndarray:
    w = np.ones(10) / 10.0
    s = np.ones(10)
    scores = compute_scores(df, w, s)
    return apply_threshold(scores, config)


def baseline_best_single(df: pd.DataFrame, config: dict) -> np.ndarray:
    """Oracle: best single feature (uses labels)."""
    y = df["layer_a"].values.astype(int)
    if y.sum() < 2:
        return np.zeros(len(df), dtype=bool)

    best_auc = -1
    best_scores = None
    for feat in FEATURE_NAMES:
        x = np.nan_to_num(df[feat].values.copy(), nan=0.0)
        try:
            auc = roc_auc_score(y, x)
        except ValueError:
            continue
        eff_auc = max(auc, 1 - auc)
        if eff_auc > best_auc:
            best_auc = eff_auc
            best_scores = x if auc >= 0.5 else -x

    if best_scores is None:
        return np.zeros(len(df), dtype=bool)
    return apply_threshold(best_scores, config)


def baseline_random(n: int, config: dict, n_trials: int = 100) -> float:
    """Average MCC over random trials. Returns mean MCC (not prediction)."""
    # For random baseline, we use topk frac as the probability
    if config["type"] == "topk":
        frac = config["frac"]
    else:
        frac = 0.05  # fallback
    return frac  # used externally with proper y_true


# ---------------------------------------------------------------------------
# LOPO evaluation
# ---------------------------------------------------------------------------
def run_full_lopo() -> pd.DataFrame:
    """Run LOPO for all strategies x thresholds."""
    # Preload all feature matrices and compute AUCs/signs/importances
    data = {}
    for p in ALL_PATHOGENS:
        try:
            df = load_feature_matrix(p)
            aucs = compute_feature_aucs(df)
            signs = compute_feature_signs(df)
            imp = compute_rf_importance(df, pathogen=p)
            profile = extract_profile(df)
            data[p] = {
                "df": df, "aucs": aucs, "signs": signs,
                "importance": imp, "profile": profile,
            }
        except FileNotFoundError:
            print(f"  [WARN] Skipping {p}: no feature matrix")

    available_pathogens = list(data.keys())
    print(f"Loaded {len(available_pathogens)} pathogens: {available_pathogens}")

    results = []

    for target in available_pathogens:
        print(f"\n{'='*60}")
        print(f"  LOPO target: {target}")
        print(f"{'='*60}")

        df_target = data[target]["df"]
        n_positions = len(df_target)

        # Ground truth
        gt_set = get_gt_adaptive(target, max_len=n_positions)
        y_true = np.zeros(n_positions, dtype=int)
        for pos in gt_set:
            if pos < n_positions:
                y_true[pos] = 1

        # Use layer_a from df if available
        if "layer_a" in df_target.columns:
            y_true = df_target["layer_a"].values.astype(int)

        n_gt = y_true.sum()
        if n_gt == 0:
            print(f"  [SKIP] No ground truth")
            continue

        print(f"  Positions: {n_positions}, Layer A: {n_gt}")

        # Training set
        train_pathogens = [p for p in available_pathogens if p != target]

        # Build reference matrices for kNN
        profiles = np.array([data[p]["profile"] for p in train_pathogens])
        W_ref = np.array([data[p]["importance"] for p in train_pathogens])
        S_ref = np.array([data[p]["signs"] for p in train_pathogens])
        auc_matrix = np.array([data[p]["aucs"] for p in train_pathogens])

        mu = profiles.mean(axis=0)
        sigma = profiles.std(axis=0)
        sigma[sigma == 0] = 1.0
        mu_sigma = np.stack([mu, sigma])

        target_profile = data[target]["profile"]

        # --- Compute weights for each strategy ---
        strategies = {}

        # A: kNN-cosine
        w_knn, s_knn, nn_info = strategy_knn_cosine(
            target_profile, profiles, W_ref, S_ref, mu_sigma, k=2
        )
        nn_names = [train_pathogens[idx] for idx, _ in nn_info]
        nn_sims = [sim for _, sim in nn_info]
        strategies["knn_cosine"] = (w_knn, s_knn)
        print(f"  kNN-cosine NN: {list(zip(nn_names, [f'{s:.3f}' for s in nn_sims]))}")

        # B: Top-3 AUC
        w_top3, s_top3 = strategy_top3_auc(auc_matrix, S_ref)
        top3_feats = [FEATURE_NAMES[i] for i in np.argsort(-w_top3)[:3] if w_top3[i] > 0]
        strategies["top3_auc"] = (w_top3, s_top3)
        print(f"  Top-3 AUC features: {top3_feats}")

        # C: Correlation-aware ensemble
        w_corr, s_corr = strategy_corr_ensemble(auc_matrix, S_ref)
        corr_feats = [FEATURE_NAMES[i] for i in range(10) if w_corr[i] > 0]
        strategies["corr_ensemble"] = (w_corr, s_corr)
        print(f"  Corr-ensemble features: {corr_feats}")

        # D: Oracle
        w_oracle, s_oracle = strategy_oracle(df_target, target)
        strategies["oracle"] = (w_oracle, s_oracle)

        # --- Evaluate each strategy x threshold ---
        for strat_name, (w, s) in strategies.items():
            scores = compute_scores(df_target, w, s)

            for thr_name, thr_config in THRESHOLD_CONFIGS.items():
                pred = apply_threshold(scores, thr_config)
                mcc = safe_mcc(y_true, pred)

                try:
                    auroc = roc_auc_score(y_true, scores)
                except ValueError:
                    auroc = np.nan

                row = {
                    "pathogen": target,
                    "strategy": strat_name,
                    "threshold": thr_name,
                    "n_positions": n_positions,
                    "n_layer_a": n_gt,
                    "n_predicted": int(pred.sum()),
                    "mcc": mcc,
                    "auroc": auroc,
                }

                # Add weights for inspection
                for i, feat in enumerate(FEATURE_NAMES):
                    row[f"w_{feat}"] = w[i] if np.std(df_target[feat].values) > 1e-10 else 0.0

                results.append(row)

        # --- Baselines (per threshold) ---
        for thr_name, thr_config in THRESHOLD_CONFIGS.items():
            # Freq
            pred_freq = baseline_freq(df_target, thr_config)
            mcc_freq = safe_mcc(y_true, pred_freq)

            # Entropy
            pred_ent = baseline_entropy(df_target, thr_config)
            mcc_ent = safe_mcc(y_true, pred_ent)

            # Equal weight
            pred_eq = baseline_equal_weight(df_target, thr_config)
            mcc_eq = safe_mcc(y_true, pred_eq)

            # Best single (oracle)
            pred_best = baseline_best_single(df_target, thr_config)
            mcc_best = safe_mcc(y_true, pred_best)

            # Random
            frac = thr_config.get("frac", 0.05)
            random_mccs = []
            for trial in range(100):
                rng = np.random.RandomState(trial)
                rand_pred = rng.random(n_positions) < frac
                random_mccs.append(safe_mcc(y_true, rand_pred))
            mcc_rand = np.mean(random_mccs)

            for bl_name, bl_mcc, bl_pred in [
                ("baseline_freq", mcc_freq, pred_freq),
                ("baseline_entropy", mcc_ent, pred_ent),
                ("baseline_equal", mcc_eq, pred_eq),
                ("baseline_best_single", mcc_best, pred_best),
                ("baseline_random", mcc_rand, None),
            ]:
                n_pred = int(bl_pred.sum()) if bl_pred is not None else -1
                results.append({
                    "pathogen": target,
                    "strategy": bl_name,
                    "threshold": thr_name,
                    "n_positions": n_positions,
                    "n_layer_a": n_gt,
                    "n_predicted": n_pred,
                    "mcc": bl_mcc,
                    "auroc": np.nan,
                })

    return pd.DataFrame(results)


# ---------------------------------------------------------------------------
# Summary & reporting
# ---------------------------------------------------------------------------
def make_summary(results_df: pd.DataFrame) -> pd.DataFrame:
    """Create summary: mean MCC per strategy x threshold."""
    rows = []
    for (strat, thr), group in results_df.groupby(["strategy", "threshold"]):
        mccs = group["mcc"].values
        rows.append({
            "strategy": strat,
            "threshold": thr,
            "mean_mcc": np.mean(mccs),
            "median_mcc": np.median(mccs),
            "std_mcc": np.std(mccs),
            "min_mcc": np.min(mccs),
            "max_mcc": np.max(mccs),
            "n_pathogens": len(mccs),
            "n_positive": int(np.sum(mccs > 0)),
        })

    summary = pd.DataFrame(rows)
    summary = summary.sort_values("mean_mcc", ascending=False).reset_index(drop=True)
    return summary


def print_comparison(summary_df: pd.DataFrame, results_df: pd.DataFrame):
    """Print comprehensive comparison table."""
    print("\n" + "=" * 100)
    print("  MutBench-Adapt v2: Multi-Strategy LOPO Results")
    print("=" * 100)

    # ---- Summary table ----
    print(f"\n{'Strategy':<25} {'Threshold':<10} {'Mean MCC':>10} {'Median':>10} "
          f"{'Std':>8} {'Min':>8} {'Max':>8} {'#Pos':>5}")
    print("-" * 90)

    for _, row in summary_df.iterrows():
        is_adapt = not row["strategy"].startswith("baseline_")
        marker = ">>>" if row["strategy"] in STRATEGY_NAMES and is_adapt else "   "
        print(
            f"{marker}{row['strategy']:<22} {row['threshold']:<10} "
            f"{row['mean_mcc']:>10.4f} {row['median_mcc']:>10.4f} "
            f"{row['std_mcc']:>8.4f} {row['min_mcc']:>8.4f} {row['max_mcc']:>8.4f} "
            f"{row['n_positive']:>5d}/{row['n_pathogens']}"
        )

    # ---- Per-pathogen breakdown for best strategy ----
    # Find best non-oracle adaptive strategy
    adapt_rows = summary_df[
        summary_df["strategy"].isin(["knn_cosine", "top3_auc", "corr_ensemble"])
    ]
    if len(adapt_rows) > 0:
        best_row = adapt_rows.iloc[0]  # already sorted by mean_mcc desc
        best_strat = best_row["strategy"]
        best_thr = best_row["threshold"]

        print(f"\n\n--- Best adaptive strategy: {best_strat} @ {best_thr} ---")
        print(f"{'Pathogen':<14} {'Adapt':>8} {'Freq':>8} {'Entropy':>8} "
              f"{'Equal':>8} {'Best1':>8} {'Random':>8}")
        print("-" * 70)

        pathogens_in_results = results_df["pathogen"].unique()
        for p in pathogens_in_results:
            p_data = results_df[results_df["pathogen"] == p]

            def get_mcc(strat, thr=best_thr):
                rows = p_data[(p_data["strategy"] == strat) & (p_data["threshold"] == thr)]
                return rows["mcc"].values[0] if len(rows) > 0 else np.nan

            adapt_mcc = get_mcc(best_strat)
            freq_mcc = get_mcc("baseline_freq")
            ent_mcc = get_mcc("baseline_entropy")
            eq_mcc = get_mcc("baseline_equal")
            best1_mcc = get_mcc("baseline_best_single")
            rand_mcc = get_mcc("baseline_random")

            # Mark best non-oracle
            non_oracle = [adapt_mcc, freq_mcc, ent_mcc, eq_mcc]
            best_val = max(non_oracle)

            def fmt(val):
                marker = "*" if abs(val - best_val) < 1e-6 else " "
                return f"{val:>7.4f}{marker}"

            print(f"{p:<14} {fmt(adapt_mcc)} {fmt(freq_mcc)} {fmt(ent_mcc)} "
                  f"{fmt(eq_mcc)} {best1_mcc:>8.4f} {rand_mcc:>8.4f}")

    # ---- Strategy comparison at top5 threshold ----
    print("\n\n--- All strategies at top5 threshold (mean MCC across pathogens) ---")
    top5_summary = summary_df[summary_df["threshold"] == "top5"].copy()
    top5_summary = top5_summary.sort_values("mean_mcc", ascending=False)
    for _, row in top5_summary.iterrows():
        bar = "#" * max(0, int(row["mean_mcc"] * 200))
        print(f"  {row['strategy']:<25} {row['mean_mcc']:>8.4f}  {bar}")


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------
def main():
    print("MutBench-Adapt v2: Multi-Strategy Pathogen-Adaptive Hotspot Detection")
    print("=" * 70)

    results_df = run_full_lopo()

    # Save detailed results
    out_path = RESULTS_DIR / "adapt_v2_lopo_results.csv"
    results_df.to_csv(out_path, index=False)
    print(f"\nSaved detailed results to {out_path}")

    # Summary
    summary_df = make_summary(results_df)
    summary_path = RESULTS_DIR / "adapt_v2_summary.csv"
    summary_df.to_csv(summary_path, index=False)
    print(f"Saved summary to {summary_path}")

    # Print comparison
    print_comparison(summary_df, results_df)


if __name__ == "__main__":
    main()
