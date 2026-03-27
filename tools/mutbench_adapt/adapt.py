#!/usr/bin/env python3
"""MutBench-Adapt: Pathogen-adaptive hotspot detection via kNN profile matching.

Implements the full pipeline:
  1. Pathogen profile extraction from feature matrices
  2. Feature weight determination via kNN in profile space
  3. Hotspot score computation (weighted z-score combination)
  4. LOPO (Leave-One-Pathogen-Out) cross-validation
  5. Comparison against baselines (FreqThresh, EntropyThresh, EqualWeight, Random, BestSingle)

Usage:
    python -m tools.mutbench_adapt.adapt          # from project root
    python tools/mutbench_adapt/adapt.py           # direct
"""

from __future__ import annotations

import os
import sys
from dataclasses import dataclass, field
from pathlib import Path

import numpy as np
import pandas as pd
from scipy.spatial.distance import euclidean
from scipy.stats import skew
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import matthews_corrcoef, roc_auc_score
from sklearn.model_selection import StratifiedKFold

# ---------------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------------
PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent  # /proj/paper
FEATURE_DIR = PROJECT_ROOT / "results" / "mutbench" / "feature_analysis"
RESULTS_DIR = PROJECT_ROOT / "results" / "mutbench"
GT_MODULE = PROJECT_ROOT / "tools" / "mutbench" / "ground_truth"

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

PROFILE_FEATURES = [
    "seq_count", "seq_length", "mean_freq", "mean_entropy",
    "diversity_ratio", "gap_fraction", "max_freq", "freq_skewness",
]


# ---------------------------------------------------------------------------
# Data classes
# ---------------------------------------------------------------------------
@dataclass
class MutBenchAdaptResult:
    """Output of MutBench-Adapt for a single pathogen."""
    positions: np.ndarray
    scores: np.ndarray
    is_hotspot: np.ndarray
    feature_contributions: np.ndarray  # (L, 10)
    weights: np.ndarray               # (10,)
    signs: np.ndarray                 # (10,)
    matched_pathogens: list           # [(name, distance, alpha), ...]
    threshold: float
    threshold_strategy: str


# ---------------------------------------------------------------------------
# 1. Load feature matrix
# ---------------------------------------------------------------------------
def load_feature_matrix(pathogen: str) -> pd.DataFrame:
    """Load the precomputed feature matrix for a pathogen."""
    path = FEATURE_DIR / f"feature_matrix_{pathogen}.csv"
    if not path.exists():
        raise FileNotFoundError(f"Feature matrix not found: {path}")
    return pd.read_csv(path)


# ---------------------------------------------------------------------------
# 2. Pathogen profile extraction
# ---------------------------------------------------------------------------
def extract_profile(df: pd.DataFrame) -> np.ndarray:
    """Extract an 8-dimensional profile vector from a feature matrix.

    Profile features:
        0: seq_count     – number of positions (proxy for protein length)
        1: seq_length    – same as seq_count for precomputed matrices
        2: mean_freq     – mean mutation frequency
        3: mean_entropy  – mean Shannon entropy
        4: diversity_ratio – fraction of positions with freq > 0.01
        5: gap_fraction  – fraction of positions with freq == 0 (invariant)
        6: max_freq      – maximum position frequency
        7: freq_skewness – skewness of frequency distribution
    """
    freq = df["freq"].values
    entropy = df["entropy"].values

    n_positions = len(df)
    mean_freq = np.mean(freq)
    mean_entropy = np.mean(entropy)
    diversity_ratio = np.mean(freq > 0.01)
    gap_fraction = np.mean(freq == 0.0)
    max_freq = np.max(freq)
    freq_skew = skew(freq) if np.std(freq) > 0 else 0.0

    return np.array([
        n_positions,    # seq_count / seq_length (same here)
        n_positions,    # seq_length
        mean_freq,
        mean_entropy,
        diversity_ratio,
        gap_fraction,
        max_freq,
        freq_skew,
    ])


# ---------------------------------------------------------------------------
# 3. Compute RF importance for a pathogen (10-feature RF → Layer A)
# ---------------------------------------------------------------------------
def compute_rf_importance(df: pd.DataFrame, n_estimators: int = 500,
                          random_state: int = 42) -> np.ndarray:
    """Train a Random Forest on the 10 features to predict Layer A.

    Returns feature importance vector of shape (10,).
    """
    X = df[FEATURE_NAMES].values.copy()
    y = df["layer_a"].values.astype(int)

    # Handle NaN/Inf
    X = np.nan_to_num(X, nan=0.0, posinf=0.0, neginf=0.0)

    # Check class balance
    n_pos = y.sum()
    if n_pos < 2:
        # Not enough positives for meaningful RF
        return np.ones(10) / 10.0

    rf = RandomForestClassifier(
        n_estimators=n_estimators,
        max_depth=None,
        min_samples_leaf=3,
        class_weight="balanced",
        random_state=random_state,
        n_jobs=-1,
    )
    rf.fit(X, y)
    return rf.feature_importances_


# ---------------------------------------------------------------------------
# 4. Compute per-feature AUC and Spearman rho sign
# ---------------------------------------------------------------------------
def compute_feature_signs(df: pd.DataFrame) -> np.ndarray:
    """For each feature, compute the sign of association with Layer A.

    Uses the AUC convention: AUC > 0.5 → positive sign, AUC < 0.5 → negative.
    Returns sign vector of shape (10,) with values in {-1, 0, +1}.
    """
    y = df["layer_a"].values.astype(int)
    signs = np.zeros(10)

    n_pos = y.sum()
    n_neg = len(y) - n_pos
    if n_pos < 2 or n_neg < 2:
        return np.ones(10)  # default positive

    for i, feat in enumerate(FEATURE_NAMES):
        x = df[feat].values.copy()
        x = np.nan_to_num(x, nan=0.0)
        try:
            auc = roc_auc_score(y, x)
            if auc > 0.5:
                signs[i] = 1.0
            elif auc < 0.5:
                signs[i] = -1.0
            else:
                signs[i] = 0.0
        except ValueError:
            signs[i] = 1.0

    return signs


# ---------------------------------------------------------------------------
# 5. Build reference database
# ---------------------------------------------------------------------------
def build_reference_database(
    pathogens: list[str],
    rf_importance_df: pd.DataFrame | None = None,
    auc_df: pd.DataFrame | None = None,
) -> tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray, list[str]]:
    """Build profile, weight, and sign matrices for reference pathogens.

    Returns:
        P_ref: (n_ref, 8) profile matrix
        W_ref: (n_ref, 10) RF importance weights
        S_ref: (n_ref, 10) sign matrix
        mu_sigma: (2, 8) mean and std for standardization
        names: list of pathogen names
    """
    profiles = []
    weights = []
    signs = []
    used_names = []

    for pathogen in pathogens:
        try:
            df = load_feature_matrix(pathogen)
        except FileNotFoundError:
            print(f"  [WARN] Skipping {pathogen}: no feature matrix")
            continue

        # Profile
        profile = extract_profile(df)
        profiles.append(profile)

        # RF importance: use precomputed if available, else compute
        if rf_importance_df is not None and pathogen in rf_importance_df["pathogen"].values:
            row = rf_importance_df[rf_importance_df["pathogen"] == pathogen]
            w = row[FEATURE_NAMES].values.flatten()
        else:
            w = compute_rf_importance(df)

        weights.append(w)

        # Signs: use precomputed AUC if available, else compute
        if auc_df is not None and pathogen in auc_df["pathogen"].values:
            s = np.zeros(10)
            for i, feat in enumerate(FEATURE_NAMES):
                rows = auc_df[(auc_df["pathogen"] == pathogen) & (auc_df["feature"] == feat)]
                if len(rows) > 0:
                    auc_val = rows["auc"].values[0]
                    s[i] = 1.0 if auc_val >= 0.5 else -1.0
                else:
                    s[i] = 1.0
        else:
            s = compute_feature_signs(df)

        signs.append(s)
        used_names.append(pathogen)

    P_ref = np.array(profiles)
    W_ref = np.array(weights)
    S_ref = np.array(signs)

    # Standardization parameters
    mu = P_ref.mean(axis=0)
    sigma = P_ref.std(axis=0)
    sigma[sigma == 0] = 1.0  # avoid division by zero

    return P_ref, W_ref, S_ref, np.stack([mu, sigma]), used_names


# ---------------------------------------------------------------------------
# 6. kNN weight interpolation
# ---------------------------------------------------------------------------
def knn_interpolate(
    query_profile: np.ndarray,
    P_ref: np.ndarray,
    W_ref: np.ndarray,
    S_ref: np.ndarray,
    mu_sigma: np.ndarray,
    k: int = 3,
) -> tuple[np.ndarray, np.ndarray, list[tuple[int, float, float]]]:
    """Find k nearest neighbors and interpolate weights and signs.

    Returns:
        w: (10,) interpolated feature weights
        s: (10,) interpolated sign vector
        neighbors: list of (index, distance, alpha)
    """
    mu, sigma = mu_sigma[0], mu_sigma[1]
    q_std = (query_profile - mu) / sigma
    P_std = (P_ref - mu) / sigma

    n_ref = len(P_ref)
    distances = np.array([euclidean(q_std, P_std[j]) for j in range(n_ref)])

    k_actual = min(k, n_ref)
    nn_idx = np.argsort(distances)[:k_actual]
    nn_dist = distances[nn_idx]

    # Inverse-distance weighting
    eps = 1e-8
    inv_d = 1.0 / (nn_dist + eps)
    alpha = inv_d / inv_d.sum()

    # Interpolate weights and signs
    w = sum(alpha[i] * W_ref[nn_idx[i]] for i in range(k_actual))
    s = sum(alpha[i] * S_ref[nn_idx[i]] for i in range(k_actual))

    neighbors = [(int(nn_idx[i]), float(nn_dist[i]), float(alpha[i]))
                  for i in range(k_actual)]

    return w, s, neighbors


# ---------------------------------------------------------------------------
# 7. Hotspot score computation
# ---------------------------------------------------------------------------
def compute_hotspot_scores(
    df: pd.DataFrame,
    w: np.ndarray,
    s: np.ndarray,
    threshold_frac: float = 0.05,
    ambiguity_cutoff: float = 0.2,
) -> MutBenchAdaptResult:
    """Compute per-position hotspot scores using weighted z-score combination.

    Steps:
        1. Z-score normalize each feature across positions
        2. Apply directional sign correction
        3. Zero out features with ambiguous direction (|s| < cutoff)
        4. Compute weighted sum
        5. Threshold at top fraction
    """
    F = df[FEATURE_NAMES].values.copy()
    F = np.nan_to_num(F, nan=0.0, posinf=0.0, neginf=0.0)
    L = F.shape[0]

    # Check feature availability
    available = np.std(F, axis=0) > 1e-10

    # Zero out unavailable features
    w_adj = w.copy()
    s_adj = s.copy()
    w_adj[~available] = 0.0

    # Zero out ambiguous-direction features
    w_adj[np.abs(s_adj) < ambiguity_cutoff] = 0.0

    # Renormalize weights
    if w_adj.sum() > 0:
        w_adj = w_adj / w_adj.sum()

    # Z-score normalize each feature
    Z = np.zeros_like(F)
    for f_idx in range(10):
        if available[f_idx]:
            mu_f = np.mean(F[:, f_idx])
            std_f = np.std(F[:, f_idx])
            if std_f > 0:
                Z[:, f_idx] = (F[:, f_idx] - mu_f) / std_f

    # Apply directional sign
    Z_prime = Z * np.sign(s_adj)

    # Weighted combination
    scores = Z_prime @ w_adj
    contributions = Z_prime * w_adj[np.newaxis, :]

    # Threshold: top fraction
    thr = np.percentile(scores, 100 * (1 - threshold_frac))
    is_hotspot = scores >= thr

    return MutBenchAdaptResult(
        positions=np.arange(L),
        scores=scores,
        is_hotspot=is_hotspot,
        feature_contributions=contributions,
        weights=w_adj,
        signs=s_adj,
        matched_pathogens=[],  # filled by caller
        threshold=thr,
        threshold_strategy="topk",
    )


# ---------------------------------------------------------------------------
# 8. Baseline methods
# ---------------------------------------------------------------------------
def baseline_freq_thresh(df: pd.DataFrame, frac: float = 0.05) -> np.ndarray:
    """Top frac% by frequency alone."""
    freq = df["freq"].values
    thr = np.percentile(freq, 100 * (1 - frac))
    return freq >= thr


def baseline_entropy_thresh(df: pd.DataFrame, frac: float = 0.05) -> np.ndarray:
    """Top frac% by entropy alone."""
    ent = df["entropy"].values
    thr = np.percentile(ent, 100 * (1 - frac))
    return ent >= thr


def baseline_equal_weight(df: pd.DataFrame, frac: float = 0.05) -> np.ndarray:
    """All 10 features with equal weight (1/10 each), positive direction."""
    w = np.ones(10) / 10.0
    s = np.ones(10)  # all positive
    result = compute_hotspot_scores(df, w, s, threshold_frac=frac,
                                     ambiguity_cutoff=0.0)
    return result.is_hotspot


def baseline_best_single(df: pd.DataFrame, frac: float = 0.05) -> np.ndarray:
    """Oracle: use the single feature with best AUC for this pathogen.

    This is an oracle baseline (uses labels), not available in practice.
    """
    y = df["layer_a"].values.astype(int)
    if y.sum() < 2:
        return np.zeros(len(df), dtype=bool)

    best_auc = -1
    best_pred = None
    for feat in FEATURE_NAMES:
        x = df[feat].values.copy()
        x = np.nan_to_num(x, nan=0.0)
        try:
            auc = roc_auc_score(y, x)
        except ValueError:
            continue
        # Use max(auc, 1-auc) since direction may be inverted
        eff_auc = max(auc, 1 - auc)
        if eff_auc > best_auc:
            best_auc = eff_auc
            if auc >= 0.5:
                thr = np.percentile(x, 100 * (1 - frac))
                best_pred = x >= thr
            else:
                thr = np.percentile(x, frac * 100)
                best_pred = x <= thr

    return best_pred if best_pred is not None else np.zeros(len(df), dtype=bool)


def baseline_random(n_positions: int, frac: float = 0.05,
                    random_state: int = 42) -> np.ndarray:
    """Random selection at expected hotspot rate."""
    rng = np.random.RandomState(random_state)
    return rng.random(n_positions) < frac


# ---------------------------------------------------------------------------
# 9. LOPO cross-validation
# ---------------------------------------------------------------------------
def run_lopo(
    k: int = 3,
    threshold_frac: float = 0.05,
    n_random_trials: int = 100,
) -> pd.DataFrame:
    """Leave-One-Pathogen-Out cross-validation.

    For each of 12 pathogens:
      1. Hold it out from the reference database
      2. Build reference from remaining 11
      3. Predict hotspot positions
      4. Evaluate MCC against Layer A ground truth
      5. Compare against baselines
    """
    # Load precomputed data
    rf_imp_path = FEATURE_DIR / "rf_importance_v2.csv"
    auc_path = FEATURE_DIR / "per_feature_auc_v2.csv"

    rf_imp_df = pd.read_csv(rf_imp_path) if rf_imp_path.exists() else None
    auc_df = pd.read_csv(auc_path) if auc_path.exists() else None

    # First: compute RF importance for any pathogen missing from rf_importance_v2
    existing_pathogens = set()
    if rf_imp_df is not None:
        existing_pathogens = set(rf_imp_df["pathogen"].values)

    new_rows = []
    for pathogen in ALL_PATHOGENS:
        if pathogen not in existing_pathogens:
            print(f"  Computing RF importance for {pathogen}...")
            try:
                df = load_feature_matrix(pathogen)
                imp = compute_rf_importance(df)
                row = {feat: imp[i] for i, feat in enumerate(FEATURE_NAMES)}
                row["pathogen"] = pathogen
                new_rows.append(row)
            except Exception as e:
                print(f"    [WARN] Failed for {pathogen}: {e}")

    if new_rows:
        new_df = pd.DataFrame(new_rows)
        if rf_imp_df is not None:
            rf_imp_df = pd.concat([rf_imp_df, new_df], ignore_index=True)
        else:
            rf_imp_df = new_df
        # Save updated importance
        cols = FEATURE_NAMES + ["pathogen"]
        rf_imp_df[cols].to_csv(rf_imp_path, index=False)
        print(f"  Saved updated RF importance to {rf_imp_path}")

    results = []

    for target in ALL_PATHOGENS:
        print(f"\n{'='*60}")
        print(f"  LOPO target: {target}")
        print(f"{'='*60}")

        # Load target feature matrix
        try:
            df_target = load_feature_matrix(target)
        except FileNotFoundError:
            print(f"  [SKIP] No feature matrix for {target}")
            continue

        n_positions = len(df_target)

        # Ground truth (Layer A)
        gt_set = get_gt_adaptive(target, max_len=n_positions)
        gt_vec = np.zeros(n_positions, dtype=int)
        for pos in gt_set:
            if pos < n_positions:
                gt_vec[pos] = 1

        n_gt = gt_vec.sum()
        if n_gt == 0:
            print(f"  [SKIP] No Layer A ground truth for {target}")
            continue

        print(f"  Positions: {n_positions}, Layer A sites: {n_gt}")

        # Build reference from all except target
        ref_pathogens = [p for p in ALL_PATHOGENS if p != target]
        P_ref, W_ref, S_ref, mu_sigma, ref_names = build_reference_database(
            ref_pathogens, rf_imp_df, auc_df
        )

        # Extract target profile
        target_profile = extract_profile(df_target)

        # kNN interpolation
        w, s, neighbors = knn_interpolate(
            target_profile, P_ref, W_ref, S_ref, mu_sigma, k=k
        )

        neighbor_names = [ref_names[idx] for idx, _, _ in neighbors]
        neighbor_dists = [d for _, d, _ in neighbors]
        neighbor_alphas = [a for _, _, a in neighbors]

        print(f"  Nearest neighbors: {list(zip(neighbor_names, [f'{d:.3f}' for d in neighbor_dists]))}")
        print(f"  Interpolated weights: {dict(zip(FEATURE_NAMES, [f'{x:.4f}' for x in w]))}")

        # MutBench-Adapt prediction
        adapt_result = compute_hotspot_scores(
            df_target, w, s,
            threshold_frac=threshold_frac,
        )

        # Use layer_a from df if available, else use gt_vec
        if "layer_a" in df_target.columns:
            y_true = df_target["layer_a"].values.astype(int)
        else:
            y_true = gt_vec

        # --- MCC for MutBench-Adapt ---
        adapt_mcc = matthews_corrcoef(y_true, adapt_result.is_hotspot.astype(int))

        # --- Baselines ---
        freq_pred = baseline_freq_thresh(df_target, frac=threshold_frac)
        freq_mcc = matthews_corrcoef(y_true, freq_pred.astype(int))

        entropy_pred = baseline_entropy_thresh(df_target, frac=threshold_frac)
        entropy_mcc = matthews_corrcoef(y_true, entropy_pred.astype(int))

        equal_pred = baseline_equal_weight(df_target, frac=threshold_frac)
        equal_mcc = matthews_corrcoef(y_true, equal_pred.astype(int))

        best_single_pred = baseline_best_single(df_target, frac=threshold_frac)
        best_single_mcc = matthews_corrcoef(y_true, best_single_pred.astype(int))

        # Random baseline: average over multiple trials
        random_mccs = []
        for trial in range(n_random_trials):
            rand_pred = baseline_random(n_positions, frac=threshold_frac,
                                         random_state=trial)
            random_mccs.append(matthews_corrcoef(y_true, rand_pred.astype(int)))
        random_mcc = np.mean(random_mccs)

        # --- AUROC for MutBench-Adapt ---
        try:
            adapt_auroc = roc_auc_score(y_true, adapt_result.scores)
        except ValueError:
            adapt_auroc = np.nan

        row = {
            "pathogen": target,
            "n_positions": n_positions,
            "n_layer_a": n_gt,
            "adapt_mcc": adapt_mcc,
            "adapt_auroc": adapt_auroc,
            "freq_mcc": freq_mcc,
            "entropy_mcc": entropy_mcc,
            "equal_weight_mcc": equal_mcc,
            "best_single_mcc": best_single_mcc,
            "random_mcc": random_mcc,
            "nn_1": neighbor_names[0] if len(neighbor_names) > 0 else "",
            "nn_2": neighbor_names[1] if len(neighbor_names) > 1 else "",
            "nn_3": neighbor_names[2] if len(neighbor_names) > 2 else "",
            "nn_1_dist": neighbor_dists[0] if len(neighbor_dists) > 0 else np.nan,
            "nn_2_dist": neighbor_dists[1] if len(neighbor_dists) > 1 else np.nan,
            "nn_3_dist": neighbor_dists[2] if len(neighbor_dists) > 2 else np.nan,
        }
        # Add individual weights
        for i, feat in enumerate(FEATURE_NAMES):
            row[f"w_{feat}"] = adapt_result.weights[i]
            row[f"s_{feat}"] = adapt_result.signs[i]

        results.append(row)

        print(f"  Adapt MCC:       {adapt_mcc:.4f}")
        print(f"  Adapt AUROC:     {adapt_auroc:.4f}")
        print(f"  FreqThresh MCC:  {freq_mcc:.4f}")
        print(f"  EntropyThr MCC:  {entropy_mcc:.4f}")
        print(f"  EqualWeight MCC: {equal_mcc:.4f}")
        print(f"  BestSingle MCC:  {best_single_mcc:.4f}")
        print(f"  Random MCC:      {random_mcc:.4f}")

    return pd.DataFrame(results)


# ---------------------------------------------------------------------------
# 10. Summary table
# ---------------------------------------------------------------------------
def make_summary(lopo_df: pd.DataFrame) -> pd.DataFrame:
    """Create summary statistics across all pathogens."""
    methods = {
        "MutBench-Adapt": "adapt_mcc",
        "FreqThresh": "freq_mcc",
        "EntropyThresh": "entropy_mcc",
        "EqualWeight": "equal_weight_mcc",
        "BestSingle (oracle)": "best_single_mcc",
        "Random": "random_mcc",
    }

    rows = []
    for name, col in methods.items():
        vals = lopo_df[col].values
        rows.append({
            "method": name,
            "mean_mcc": np.mean(vals),
            "median_mcc": np.median(vals),
            "std_mcc": np.std(vals),
            "min_mcc": np.min(vals),
            "max_mcc": np.max(vals),
            "n_best": sum(
                1 for i in range(len(lopo_df))
                if col != "random_mcc" and
                lopo_df.iloc[i][col] == lopo_df.iloc[i][
                    ["adapt_mcc", "freq_mcc", "entropy_mcc",
                     "equal_weight_mcc"]
                ].max()
            ),
        })

    return pd.DataFrame(rows)


# ---------------------------------------------------------------------------
# 11. Print comparison table
# ---------------------------------------------------------------------------
def print_comparison_table(lopo_df: pd.DataFrame, summary_df: pd.DataFrame):
    """Print a clear comparison table to stdout."""

    print("\n" + "=" * 90)
    print("  MutBench-Adapt LOPO Cross-Validation Results")
    print("=" * 90)

    # Per-pathogen table
    header = f"{'Pathogen':<14} {'Adapt':>7} {'Freq':>7} {'Entropy':>7} {'Equal':>7} {'Best1':>7} {'Random':>7} {'NN1':<12}"
    print(f"\n{header}")
    print("-" * len(header))

    for _, row in lopo_df.iterrows():
        # Highlight the best non-oracle method
        non_oracle = [row["adapt_mcc"], row["freq_mcc"],
                      row["entropy_mcc"], row["equal_weight_mcc"]]
        best_val = max(non_oracle)

        def fmt(val, is_best=False):
            marker = "*" if abs(val - best_val) < 1e-6 and is_best else " "
            return f"{val:>6.3f}{marker}"

        print(
            f"{row['pathogen']:<14} "
            f"{fmt(row['adapt_mcc'], True)} "
            f"{fmt(row['freq_mcc'], True)} "
            f"{fmt(row['entropy_mcc'], True)} "
            f"{fmt(row['equal_weight_mcc'], True)} "
            f"{row['best_single_mcc']:>6.3f}  "
            f"{row['random_mcc']:>6.3f}  "
            f"{row['nn_1']:<12}"
        )

    print("-" * len(header))

    # Summary
    print(f"\n{'Method':<22} {'Mean':>7} {'Median':>7} {'Std':>7} {'Min':>7} {'Max':>7}")
    print("-" * 60)
    for _, row in summary_df.iterrows():
        print(
            f"{row['method']:<22} "
            f"{row['mean_mcc']:>7.4f} "
            f"{row['median_mcc']:>7.4f} "
            f"{row['std_mcc']:>7.4f} "
            f"{row['min_mcc']:>7.4f} "
            f"{row['max_mcc']:>7.4f}"
        )

    print("\n* = best non-oracle method for that pathogen")
    print("BestSingle = oracle per-pathogen best single feature (uses labels)")


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------
def main():
    print("MutBench-Adapt: Pathogen-Adaptive Hotspot Detection")
    print("=" * 60)

    # Run LOPO
    lopo_df = run_lopo(k=3, threshold_frac=0.05, n_random_trials=100)

    # Save detailed results
    lopo_path = RESULTS_DIR / "adapt_lopo_results.csv"
    lopo_df.to_csv(lopo_path, index=False)
    print(f"\nSaved LOPO results to {lopo_path}")

    # Summary
    summary_df = make_summary(lopo_df)
    summary_path = RESULTS_DIR / "adapt_summary.csv"
    summary_df.to_csv(summary_path, index=False)
    print(f"Saved summary to {summary_path}")

    # Print table
    print_comparison_table(lopo_df, summary_df)


if __name__ == "__main__":
    main()
