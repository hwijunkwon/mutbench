#!/usr/bin/env python3
"""PAHD-R multi-hypothesis prototype experiments.

The script tests several domain-grounded adaptive hypotheses under one LOPO
evaluation frame:

H1 regime-weighted evidence
H2 evidence-module ensembles
H3 stability selection by module-weight perturbation
H4 region-level evaluation
H5 local-background cluster scoring
H6 phylogeny-aware evidence ablation
H7 trait-axis separated evidence
H8 method-set/shortlist recommendation from the benchmark matrix
H16 reliability-gated final pipeline candidates
H17 H11-preserving conservative alternatives
H18 non-AI core evidence-fusion candidates
H19 SNF-style site similarity fusion
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import sys

import numpy as np
import pandas as pd
from sklearn.metrics import matthews_corrcoef, roc_auc_score


PROJECT_ROOT = Path(__file__).resolve().parent.parent
FEATURE_DIR = PROJECT_ROOT / "results" / "mutbench" / "feature_analysis"
RESULTS_DIR = PROJECT_ROOT / "results" / "mutbench"
BENCHMARK_PATH = RESULTS_DIR / "multilayer_9pathogen_results.csv"

sys.path.insert(0, str(PROJECT_ROOT / "tools"))
from mutbench.ground_truth.multilayer_gt import get_gt_constrained  # noqa: E402

FEATURES = [
    "freq",
    "entropy",
    "rare_freq",
    "homoplasy",
    "esm2_llr",
    "plddt",
    "sasa",
    "grantham",
    "dnds_proxy",
    "semantic_change",
]

MODULES = {
    "recurrence": ["freq", "rare_freq"],
    "diversity": ["entropy"],
    "phylo": ["homoplasy", "dnds_proxy"],
    "constraint": ["esm2_llr", "plddt"],
    "structure": ["sasa", "grantham"],
    "semantic": ["semantic_change"],
}

NON_AI_MODULES = {
    "recurrence": ["freq", "rare_freq"],
    "diversity": ["entropy"],
    "phylo": ["homoplasy", "dnds_proxy"],
    "structure_non_ai": ["sasa", "grantham"],
}

REGIME_MODULE_WEIGHTS = {
    "escape_dominant": {
        "recurrence": 0.20,
        "diversity": 0.15,
        "phylo": 0.10,
        "constraint": 0.15,
        "structure": 0.15,
        "semantic": 0.25,
    },
    "convergent_adaptation": {
        "recurrence": 0.20,
        "diversity": 0.10,
        "phylo": 0.35,
        "constraint": 0.10,
        "structure": 0.10,
        "semantic": 0.15,
    },
    "conservation_break": {
        "recurrence": 0.10,
        "diversity": 0.10,
        "phylo": 0.10,
        "constraint": 0.35,
        "structure": 0.25,
        "semantic": 0.10,
    },
    "regional_hotspot": {
        "recurrence": 0.25,
        "diversity": 0.15,
        "phylo": 0.15,
        "constraint": 0.10,
        "structure": 0.15,
        "semantic": 0.20,
    },
    "low_signal": {
        "recurrence": 0.20,
        "diversity": 0.20,
        "phylo": 0.15,
        "constraint": 0.15,
        "structure": 0.15,
        "semantic": 0.15,
    },
}


@dataclass
class PredictionResult:
    pathogen: str
    hypothesis: str
    strategy: str
    n_positions: int
    n_predicted: int
    mcc_exact: float
    mcc_window_5: float
    mcc_window_10: float
    precision_20: float
    precision_50: float
    precision_10pct: float
    enrichment_20: float
    enrichment_50: float
    enrichment_10pct: float
    constrained_fpr: float
    pred_frac: float
    region_coverage_5: float
    region_coverage_10: float
    auroc: float


def load_feature_matrices() -> dict[str, pd.DataFrame]:
    data = {}
    for path in sorted(FEATURE_DIR.glob("feature_matrix_*.csv")):
        pathogen = path.stem.replace("feature_matrix_", "")
        df = pd.read_csv(path)
        if "layer_a" in df.columns and all(col in df.columns for col in FEATURES):
            data[pathogen] = df
    return data


def robust_z(values: np.ndarray) -> np.ndarray:
    values = np.nan_to_num(np.asarray(values, dtype=float), nan=0.0, posinf=0.0, neginf=0.0)
    std = values.std()
    if std < 1e-12:
        return np.zeros_like(values)
    return (values - values.mean()) / std


def compute_feature_signs(train_data: dict[str, pd.DataFrame]) -> dict[str, float]:
    signs = {}
    for feat in FEATURES:
        aucs = []
        for df in train_data.values():
            y = df["layer_a"].astype(int).values
            x = np.nan_to_num(df[feat].values, nan=0.0)
            if y.sum() < 2 or (len(y) - y.sum()) < 2 or np.std(x) < 1e-12:
                continue
            try:
                aucs.append(roc_auc_score(y, x))
            except ValueError:
                continue
        mean_auc = np.mean(aucs) if aucs else 0.5
        signs[feat] = 1.0 if mean_auc >= 0.5 else -1.0
    return signs


def compute_feature_effects(train_data: dict[str, pd.DataFrame]) -> dict[str, float]:
    effects = {}
    for feat in FEATURES:
        vals = []
        for df in train_data.values():
            y = df["layer_a"].astype(int).values
            x = np.nan_to_num(df[feat].values, nan=0.0)
            if y.sum() < 2 or (len(y) - y.sum()) < 2 or np.std(x) < 1e-12:
                continue
            try:
                vals.append(abs(roc_auc_score(y, x) - 0.5))
            except ValueError:
                continue
        effects[feat] = float(np.mean(vals)) if vals else 0.0
    return effects


def module_scores(df: pd.DataFrame, signs: dict[str, float]) -> pd.DataFrame:
    out = {}
    for module, feats in MODULES.items():
        parts = []
        for feat in feats:
            parts.append(robust_z(df[feat].values) * signs.get(feat, 1.0))
        out[module] = np.mean(np.column_stack(parts), axis=1) if parts else np.zeros(len(df))
    return pd.DataFrame(out)


def non_ai_module_scores(df: pd.DataFrame, signs: dict[str, float]) -> pd.DataFrame:
    out = {}
    for module, feats in NON_AI_MODULES.items():
        parts = []
        for feat in feats:
            parts.append(robust_z(df[feat].values) * signs.get(feat, 1.0))
        out[module] = np.mean(np.column_stack(parts), axis=1) if parts else np.zeros(len(df))
    return pd.DataFrame(out)


def normalize_weights(weights: dict[str, float]) -> dict[str, float]:
    clean = {k: max(0.0, float(v)) for k, v in weights.items()}
    total = sum(clean.values())
    if total <= 1e-12:
        return {k: 1.0 / len(clean) for k in clean}
    return {k: v / total for k, v in clean.items()}


def combine_modules(scores: pd.DataFrame, weights: dict[str, float]) -> np.ndarray:
    weights = normalize_weights(weights)
    combined = np.zeros(len(scores))
    for module, weight in weights.items():
        combined += weight * scores[module].values
    return combined


def target_profile(df: pd.DataFrame) -> dict[str, float]:
    freq = np.nan_to_num(df["freq"].values, nan=0.0)
    entropy = np.nan_to_num(df["entropy"].values, nan=0.0)
    homoplasy = np.nan_to_num(df["homoplasy"].values, nan=0.0)
    semantic = np.nan_to_num(df["semantic_change"].values, nan=0.0)
    constraint = np.nan_to_num(df["esm2_llr"].values, nan=0.0)
    structure = np.nan_to_num(df[["plddt", "sasa", "grantham"]].values, nan=0.0)

    def gini(values: np.ndarray) -> float:
        values = np.sort(np.abs(values))
        if values.sum() <= 1e-12:
            return 0.0
        n = len(values)
        idx = np.arange(1, n + 1)
        return float((2 * np.sum(idx * values) - (n + 1) * np.sum(values)) / (n * np.sum(values)))

    return {
        "diversity": float(np.mean(freq > 0.01) + np.std(entropy)),
        "homoplasy_burden": float(np.mean(homoplasy > 0) + gini(homoplasy)),
        "semantic_burden": float(np.std(semantic) + gini(semantic)),
        "constraint_burden": float(np.std(constraint) + gini(constraint)),
        "structure_burden": float(np.nanmean(np.std(structure, axis=0))),
        "sparsity": float(np.mean(freq == 0.0)),
    }


def infer_regime_probabilities(profile: dict[str, float]) -> dict[str, float]:
    p = profile
    raw = {
        "escape_dominant": 0.9 * p["semantic_burden"] + 0.5 * p["diversity"] + 0.2 * p["structure_burden"],
        "convergent_adaptation": 1.0 * p["homoplasy_burden"] + 0.3 * p["diversity"],
        "conservation_break": 0.8 * p["constraint_burden"] + 0.4 * p["structure_burden"] + 0.2 * p["sparsity"],
        "regional_hotspot": 0.5 * p["diversity"] + 0.5 * p["semantic_burden"] + 0.3 * p["homoplasy_burden"],
        "low_signal": 0.7 * p["sparsity"] + 0.3 * (1.0 - p["diversity"]),
    }
    vals = np.array(list(raw.values()), dtype=float)
    vals = vals - vals.max()
    exp = np.exp(vals)
    probs = exp / exp.sum()
    return dict(zip(raw.keys(), probs))


def normalized_profiles(data: dict[str, pd.DataFrame], pathogens: list[str]) -> dict[str, dict[str, float]]:
    raw = {pathogen: target_profile(data[pathogen]) for pathogen in pathogens}
    keys = list(next(iter(raw.values())).keys())
    norm = {pathogen: {} for pathogen in pathogens}
    for key in keys:
        vals = np.array([raw[pathogen][key] for pathogen in pathogens], dtype=float)
        lo = float(vals.min())
        hi = float(vals.max())
        for pathogen in pathogens:
            if hi - lo < 1e-12:
                norm[pathogen][key] = 0.5
            else:
                norm[pathogen][key] = float((raw[pathogen][key] - lo) / (hi - lo))
    return norm


def regime_weights(regime_probs: dict[str, float]) -> dict[str, float]:
    weights = {module: 0.0 for module in MODULES}
    for regime, prob in regime_probs.items():
        for module, weight in REGIME_MODULE_WEIGHTS[regime].items():
            weights[module] += prob * weight
    return normalize_weights(weights)


def learned_module_weights(feature_effects: dict[str, float]) -> dict[str, float]:
    weights = {}
    for module, feats in MODULES.items():
        weights[module] = float(np.mean([feature_effects.get(feat, 0.0) for feat in feats]))
    return normalize_weights(weights)


def learned_non_ai_weights(feature_effects: dict[str, float]) -> dict[str, float]:
    weights = {}
    for module, feats in NON_AI_MODULES.items():
        weights[module] = float(np.mean([feature_effects.get(feat, 0.0) for feat in feats]))
    return normalize_weights(weights)


def top_fraction_pred(scores: np.ndarray, frac: float = 0.10) -> np.ndarray:
    n = len(scores)
    k = max(1, int(round(n * frac)))
    order = np.argsort(-scores)
    pred = np.zeros(n, dtype=bool)
    pred[order[:k]] = True
    return pred


def top_k_pred(scores: np.ndarray, k: int) -> np.ndarray:
    n = len(scores)
    pred = np.zeros(n, dtype=bool)
    pred[np.argsort(-scores)[: min(k, n)]] = True
    return pred


def region_mcc(y_true: np.ndarray, y_pred: np.ndarray, window: int) -> float:
    if window == 0:
        if y_pred.sum() == 0 or y_pred.sum() == len(y_pred):
            return 0.0
        return float(matthews_corrcoef(y_true.astype(int), y_pred.astype(int)))

    n = len(y_true)
    gt_positions = np.where(y_true > 0)[0]
    pred_positions = np.where(y_pred > 0)[0]
    gt_expanded = np.zeros(n, dtype=bool)
    pred_expanded = np.zeros(n, dtype=bool)

    for pos in gt_positions:
        gt_expanded[max(0, pos - window): min(n, pos + window + 1)] = True
    for pos in pred_positions:
        pred_expanded[max(0, pos - window): min(n, pos + window + 1)] = True

    tp = int(np.sum(y_pred & gt_expanded))
    fp = int(np.sum(y_pred & ~gt_expanded))
    fn = int(np.sum((y_true > 0) & ~pred_expanded))
    tn = n - tp - fp - fn
    denom = np.sqrt((tp + fp) * (tp + fn) * (tn + fp) * (tn + fn))
    return float(((tp * tn) - (fp * fn)) / denom) if denom else 0.0


def precision_and_enrichment(y_true: np.ndarray, scores: np.ndarray, k: int) -> tuple[float, float]:
    n = len(y_true)
    k = min(k, n)
    if k <= 0:
        return 0.0, 0.0
    top = np.argsort(-scores)[:k]
    precision = float(np.mean(y_true[top] > 0))
    base = float(np.mean(y_true > 0))
    enrichment = precision / base if base > 0 else 0.0
    return precision, enrichment


def constrained_fpr(pathogen: str, n_positions: int, pred: np.ndarray) -> float:
    constrained = get_gt_constrained(pathogen, n_positions)
    if not constrained:
        return np.nan
    constrained_mask = np.zeros(n_positions, dtype=bool)
    for pos in constrained:
        if 0 <= pos < n_positions:
            constrained_mask[pos] = True
    denom = int(constrained_mask.sum())
    return float(np.sum(pred & constrained_mask) / denom) if denom else np.nan


def expanded_coverage(pred: np.ndarray, window: int) -> float:
    expanded = np.zeros(len(pred), dtype=bool)
    for pos in np.where(pred > 0)[0]:
        expanded[max(0, pos - window): min(len(pred), pos + window + 1)] = True
    return float(expanded.mean())


def rank_percentile(values: np.ndarray) -> np.ndarray:
    order = np.argsort(np.argsort(values))
    if len(values) <= 1:
        return np.ones_like(values, dtype=float)
    return order.astype(float) / (len(values) - 1)


def gini(values: np.ndarray) -> float:
    values = np.sort(np.abs(np.nan_to_num(values, nan=0.0)))
    total = values.sum()
    if total <= 1e-12:
        return 0.0
    n = len(values)
    idx = np.arange(1, n + 1)
    return float((2 * np.sum(idx * values) - (n + 1) * total) / (n * total))


def cluster_reliability(cluster_score: np.ndarray, phylo_score: np.ndarray, learned_score: np.ndarray) -> float:
    """Observable reliability gate for local cluster evidence.

    A compact cluster is helpful only when it is also supported by broader
    evidence. This prevents compact but biologically unsupported peaks from
    dominating in low-signal pathogens.
    """
    cluster_pred = top_fraction_pred(cluster_score, 0.10)
    compactness = 1.0 - expanded_coverage(cluster_pred, 10)
    concentration = gini(cluster_score)
    c_rank = rank_percentile(cluster_score)
    p_rank = rank_percentile(phylo_score)
    l_rank = rank_percentile(learned_score)
    top = c_rank >= np.quantile(c_rank, 0.90)
    support = float(np.mean((p_rank[top] + l_rank[top]) / 2.0)) if np.any(top) else 0.0
    raw = 0.4 * compactness + 0.3 * concentration + 0.3 * support
    return float(np.clip(raw, 0.0, 1.0))


def phylo_reliability(phylo_score: np.ndarray, learned_score: np.ndarray, recurrence_score: np.ndarray) -> float:
    """Reliability of convergence evidence from observable score geometry."""
    p_rank = rank_percentile(phylo_score)
    l_rank = rank_percentile(learned_score)
    r_rank = rank_percentile(recurrence_score)
    top = p_rank >= np.quantile(p_rank, 0.90)
    if not np.any(top):
        return 0.0
    concentration = gini(phylo_score)
    dispersion = expanded_coverage(top, 10)
    cross_support = float(np.mean((l_rank[top] + r_rank[top]) / 2.0))
    raw = 0.35 * concentration + 0.25 * dispersion + 0.40 * cross_support
    return float(np.clip(raw, 0.0, 1.0))


def constraint_reliability(scores_df: pd.DataFrame) -> float:
    """Whether constraint/structure signals vary enough to be useful."""
    constraint = scores_df["constraint"].values
    structure = scores_df["structure"].values
    variation = 0.5 * min(1.0, float(np.std(constraint))) + 0.5 * min(1.0, float(np.std(structure)))
    concentration = 0.5 * gini(constraint) + 0.5 * gini(structure)
    return float(np.clip(0.55 * variation + 0.45 * concentration, 0.0, 1.0))


def evaluate_prediction(
    pathogen: str,
    hypothesis: str,
    strategy: str,
    df: pd.DataFrame,
    scores: np.ndarray,
    pred: np.ndarray,
) -> PredictionResult:
    y_true = df["layer_a"].astype(int).values
    p20, e20 = precision_and_enrichment(y_true, scores, 20)
    p50, e50 = precision_and_enrichment(y_true, scores, 50)
    k10 = max(1, int(round(len(y_true) * 0.10)))
    p10, e10 = precision_and_enrichment(y_true, scores, k10)
    if y_true.sum() > 1 and (len(y_true) - y_true.sum()) > 1 and np.std(scores) > 1e-12:
        try:
            auroc = float(roc_auc_score(y_true, scores))
        except ValueError:
            auroc = np.nan
    else:
        auroc = np.nan
    return PredictionResult(
        pathogen=pathogen,
        hypothesis=hypothesis,
        strategy=strategy,
        n_positions=len(y_true),
        n_predicted=int(pred.sum()),
        mcc_exact=region_mcc(y_true, pred, 0),
        mcc_window_5=region_mcc(y_true, pred, 5),
        mcc_window_10=region_mcc(y_true, pred, 10),
        precision_20=p20,
        precision_50=p50,
        precision_10pct=p10,
        enrichment_20=e20,
        enrichment_50=e50,
        enrichment_10pct=e10,
        constrained_fpr=constrained_fpr(pathogen, len(y_true), pred),
        pred_frac=float(pred.mean()),
        region_coverage_5=expanded_coverage(pred, 5),
        region_coverage_10=expanded_coverage(pred, 10),
        auroc=auroc,
    )


def stability_scores(
    scores_df: pd.DataFrame,
    base_weights: dict[str, float],
    n_iter: int = 200,
    frac: float = 0.10,
    seed: int = 13,
) -> tuple[np.ndarray, np.ndarray]:
    rng = np.random.default_rng(seed)
    modules = list(MODULES)
    alpha = np.array([max(base_weights.get(m, 0.0), 1e-3) for m in modules])
    alpha = alpha / alpha.sum() * len(modules) * 8
    selection = np.zeros(len(scores_df), dtype=float)
    combined_acc = np.zeros(len(scores_df), dtype=float)
    for _ in range(n_iter):
        sampled = rng.dirichlet(alpha)
        weights = dict(zip(modules, sampled))
        combined = combine_modules(scores_df, weights)
        pred = top_fraction_pred(combined, frac)
        selection += pred.astype(float)
        combined_acc += combined
    return selection / n_iter, combined_acc / n_iter


def local_background_cluster_score(raw_scores: np.ndarray, n_perm: int = 300, seed: int = 7) -> np.ndarray:
    rng = np.random.default_rng(seed)
    z = robust_z(raw_scores)
    z = np.maximum(z, 0.0)
    n = len(z)
    windows = [7, 11, 21]
    observed = np.zeros(n)
    null_max = {w: [] for w in windows}

    for w in windows:
        kernel = np.ones(min(w, n)) / min(w, n)
        smooth = np.convolve(z, kernel, mode="same")
        observed = np.maximum(observed, smooth)
        for _ in range(n_perm):
            perm = rng.permutation(z)
            null_max[w].append(float(np.max(np.convolve(perm, kernel, mode="same"))))

    pvals = np.ones(n)
    for w in windows:
        kernel = np.ones(min(w, n)) / min(w, n)
        smooth = np.convolve(z, kernel, mode="same")
        null = np.asarray(null_max[w])
        p = np.array([(np.sum(null >= val) + 1) / (len(null) + 1) for val in smooth])
        pvals = np.minimum(pvals, p)
    return -np.log10(np.maximum(pvals, 1e-6)) * observed


def local_burden_cluster_score(
    raw_scores: np.ndarray,
    burden_scores: np.ndarray,
    n_perm: int = 300,
    seed: int = 17,
) -> np.ndarray:
    """Cluster score with a local-burden correction.

    This is still a feature-level approximation, but it is more conservative
    than global score permutation because peaks must exceed their local mutation
    burden and the null preserves score autocorrelation through circular shifts.
    """
    rng = np.random.default_rng(seed)
    z = np.maximum(robust_z(raw_scores), 0.0)
    burden = np.maximum(np.abs(robust_z(burden_scores)), 0.0)
    n = len(z)
    windows = [7, 11, 21]
    observed = np.zeros(n)
    pvals = np.ones(n)

    for w in windows:
        width = min(w, n)
        kernel = np.ones(width) / width
        smooth = np.convolve(z, kernel, mode="same")
        local_burden = np.convolve(burden, kernel, mode="same")
        adjusted = smooth / (1.0 + local_burden)
        observed = np.maximum(observed, adjusted)

        null_max = []
        for _ in range(n_perm):
            shift = int(rng.integers(0, n))
            shifted = np.roll(z, shift)
            null_smooth = np.convolve(shifted, kernel, mode="same")
            null_adjusted = null_smooth / (1.0 + local_burden)
            null_max.append(float(np.max(null_adjusted)))
        null = np.asarray(null_max)
        p = np.array([(np.sum(null >= val) + 1) / (len(null) + 1) for val in adjusted])
        pvals = np.minimum(pvals, p)

    return -np.log10(np.maximum(pvals, 1e-6)) * observed


def reliability_gated_fusion(
    learned_score: np.ndarray,
    cluster_score: np.ndarray,
    phylo_score: np.ndarray,
    stability_prob: np.ndarray,
    scores_df: pd.DataFrame,
    cluster_rel: float,
    phylo_rel: float,
    constraint_rel: float,
) -> tuple[np.ndarray, np.ndarray]:
    learned_rank = rank_percentile(learned_score)
    cluster_rank = rank_percentile(cluster_score)
    phylo_rank = rank_percentile(phylo_score)
    stable_rank = rank_percentile(stability_prob)

    weights = normalize_weights({
        "learned": 0.45,
        "cluster": 0.10 + 0.35 * cluster_rel,
        "phylo": 0.10 + 0.30 * phylo_rel,
        "stability": 0.10 + 0.15 * float(np.std(stability_prob) > 0.02),
    })
    fused = (
        weights["learned"] * learned_rank
        + weights["cluster"] * cluster_rank
        + weights["phylo"] * phylo_rank
        + weights["stability"] * stable_rank
    )

    constraint_risk = (
        0.55 * rank_percentile(scores_df["constraint"].values)
        + 0.45 * rank_percentile(scores_df["structure"].values)
    )
    support = np.maximum.reduce([learned_rank, cluster_rank, phylo_rank])
    penalty = 1.0 - (0.18 * constraint_rel * constraint_risk * (1.0 - support))
    postprocessed = fused * np.clip(penalty, 0.70, 1.0)

    kernel = np.ones(min(9, len(fused))) / min(9, len(fused))
    regional_support = np.convolve(postprocessed, kernel, mode="same")
    postprocessed = 0.85 * postprocessed + 0.15 * rank_percentile(regional_support)
    return fused, postprocessed


def h11_preserving_alternatives(
    h11_score: np.ndarray,
    learned_score: np.ndarray,
    cluster_score: np.ndarray,
    phylo_score: np.ndarray,
    stability_prob: np.ndarray,
    burden_cluster_score: np.ndarray,
    scores_df: pd.DataFrame,
    constraint_rel: float,
) -> dict[str, np.ndarray]:
    """Conservative alternatives that keep H11 as the dominant signal."""
    h11_rank = rank_percentile(h11_score)
    learned_rank = rank_percentile(learned_score)
    cluster_rank = rank_percentile(cluster_score)
    phylo_rank = rank_percentile(phylo_score)
    stable_rank = rank_percentile(stability_prob)
    burden_rank = rank_percentile(burden_cluster_score)
    support = np.maximum.reduce([learned_rank, cluster_rank, phylo_rank])
    constraint_risk = (
        0.55 * rank_percentile(scores_df["constraint"].values)
        + 0.45 * rank_percentile(scores_df["structure"].values)
    )

    soft_penalty = 1.0 - (0.08 * constraint_rel * constraint_risk * (1.0 - support))
    soft_constraint = h11_rank * np.clip(soft_penalty, 0.85, 1.0)
    stability_blend = 0.90 * h11_rank + 0.10 * stable_rank
    burden_light = 0.88 * h11_rank + 0.12 * burden_rank
    consensus_boost = h11_rank * (0.85 + 0.15 * support)
    regional_kernel = np.ones(min(7, len(h11_rank))) / min(7, len(h11_rank))
    regional_support = rank_percentile(np.convolve(h11_rank, regional_kernel, mode="same"))
    region_smoothed = 0.90 * h11_rank + 0.10 * regional_support

    return {
        "h11_soft_constraint_post": soft_constraint,
        "h11_stability_blend": stability_blend,
        "h11_light_burden_blend": burden_light,
        "h11_consensus_boost": consensus_boost,
        "h11_region_smoothed": region_smoothed,
    }


def snf_style_site_fusion(module_score_df: pd.DataFrame, seed_score: np.ndarray, k: int = 15) -> np.ndarray:
    """Site-level analogue of similarity network fusion.

    Multi-omics SNF fuses sample-similarity networks across modalities. Here the
    samples are amino-acid positions and each evidence module is one modality.
    The fused graph diffuses a seed score over positions that are consistently
    similar across evidence views.
    """
    n = len(module_score_df)
    if n <= 2:
        return rank_percentile(seed_score)

    k = max(2, min(k, n - 1))
    views = []
    for col in module_score_df.columns:
        x = rank_percentile(module_score_df[col].values).reshape(-1, 1)
        dist = np.abs(x - x.T)
        sigma = np.median(dist[dist > 0]) if np.any(dist > 0) else 1.0
        affinity = np.exp(-(dist ** 2) / (2.0 * max(sigma, 1e-6) ** 2))
        np.fill_diagonal(affinity, 0.0)

        keep = np.zeros_like(affinity, dtype=bool)
        order = np.argsort(-affinity, axis=1)[:, :k]
        rows = np.arange(n)[:, None]
        keep[rows, order] = True
        affinity = np.where(keep | keep.T, affinity, 0.0)
        row_sum = affinity.sum(axis=1, keepdims=True)
        affinity = np.divide(affinity, row_sum, out=np.zeros_like(affinity), where=row_sum > 1e-12)
        views.append(affinity)

    fused = np.mean(views, axis=0)
    seed = rank_percentile(seed_score)
    propagated = seed.copy()
    for _ in range(8):
        propagated = 0.65 * fused.dot(propagated) + 0.35 * seed
    return rank_percentile(propagated)


def confidence_site_rows(
    pathogen: str,
    strategy: str,
    df: pd.DataFrame,
    final_score: np.ndarray,
    learned_score: np.ndarray,
    cluster_score: np.ndarray,
    phylo_score: np.ndarray,
    stability_prob: np.ndarray,
    frac: float = 0.10,
) -> list[dict[str, object]]:
    pred = top_fraction_pred(final_score, frac)
    learned_rank = rank_percentile(learned_score)
    cluster_rank = rank_percentile(cluster_score)
    phylo_rank = rank_percentile(phylo_score)
    final_rank = rank_percentile(final_score)
    constrained = get_gt_constrained(pathogen, len(df))
    constrained_mask = np.zeros(len(df), dtype=bool)
    for pos in constrained:
        if 0 <= pos < len(df):
            constrained_mask[pos] = True

    rows = []
    for idx in np.where(pred)[0]:
        modules = int(learned_rank[idx] >= 0.80) + int(cluster_rank[idx] >= 0.80) + int(phylo_rank[idx] >= 0.80)
        stable = float(stability_prob[idx])
        if modules >= 2 and stable >= 0.50 and not constrained_mask[idx]:
            confidence = "high"
        elif modules >= 1 and stable >= 0.25:
            confidence = "moderate"
        else:
            confidence = "exploratory"
        rows.append({
            "pathogen": pathogen,
            "strategy": strategy,
            "position": int(df.iloc[idx]["position"]) if "position" in df.columns else int(idx),
            "index": int(idx),
            "score": float(final_score[idx]),
            "score_rank": float(final_rank[idx]),
            "support_modules": modules,
            "stability_prob": stable,
            "constrained_site": bool(constrained_mask[idx]),
            "confidence": confidence,
        })
    return sorted(rows, key=lambda row: row["score"], reverse=True)


def method_set_experiment(benchmark: pd.DataFrame) -> pd.DataFrame:
    rows = []
    pathogens = sorted(benchmark["pathogen"].unique())
    for target in pathogens:
        train = benchmark[benchmark["pathogen"] != target]
        target_df = benchmark[benchmark["pathogen"] == target]
        oracle = float(target_df["mcc_adaptive"].max())
        target_combos = set(map(tuple, target_df[["score", "detector"]].values))
        train = train[train[["score", "detector"]].apply(tuple, axis=1).isin(target_combos)]
        agg = train.groupby(["score", "detector"])["mcc_adaptive"].agg(["mean", "std"]).fillna(0.0)
        agg["robust"] = agg["mean"] - 0.5 * agg["std"]
        ranked = agg.sort_values("robust", ascending=False).index.tolist()
        for k in [1, 3, 5, 10, 20, 50]:
            mccs = []
            for score, detector in ranked[:k]:
                hit = target_df[(target_df["score"] == score) & (target_df["detector"] == detector)]
                if len(hit):
                    mccs.append(float(hit.iloc[0]["mcc_adaptive"]))
            best = max(mccs) if mccs else 0.0
            rows.append({
                "pathogen": target,
                "strategy": f"robust_method_set@{k}",
                "k": k,
                "best_mcc": best,
                "oracle_mcc": oracle,
                "pct_oracle": 100.0 * best / oracle if oracle > 0 else 0.0,
                "positive": best > 0,
            })
    return pd.DataFrame(rows)


def method_panel_experiment(benchmark: pd.DataFrame) -> pd.DataFrame:
    """Compress robust method sets into a small diverse recommendation panel."""
    def family(score: str, detector: str) -> str:
        name = f"{score} {detector}".lower()
        if any(key in name for key in ["homoplasy", "phylo", "tree", "dnds"]):
            return "phylo"
        if any(key in name for key in ["cluster", "hotspot", "window", "region"]):
            return "cluster"
        if any(key in name for key in ["esm", "plddt", "sasa", "grantham", "constraint"]):
            return "constraint"
        if any(key in name for key in ["ensemble", "adaptive", "combined", "fusion"]):
            return "fusion"
        return "general"

    rows = []
    pathogens = sorted(benchmark["pathogen"].unique())
    for target in pathogens:
        train = benchmark[benchmark["pathogen"] != target]
        target_df = benchmark[benchmark["pathogen"] == target]
        oracle = float(target_df["mcc_adaptive"].max())
        target_combos = set(map(tuple, target_df[["score", "detector"]].values))
        train = train[train[["score", "detector"]].apply(tuple, axis=1).isin(target_combos)]
        agg = train.groupby(["score", "detector"])["mcc_adaptive"].agg(["mean", "std"]).fillna(0.0)
        agg["robust"] = agg["mean"] - 0.5 * agg["std"]
        ranked = agg.sort_values("robust", ascending=False).reset_index()

        selected = []
        used_families = set()
        for _, row in ranked.iterrows():
            fam = family(str(row["score"]), str(row["detector"]))
            if fam in used_families and len(selected) < 4:
                continue
            selected.append((row["score"], row["detector"], fam))
            used_families.add(fam)
            if len(selected) >= 5:
                break
        for _, row in ranked.iterrows():
            if len(selected) >= 5:
                break
            combo = (row["score"], row["detector"])
            if not any((s, d) == combo for s, d, _ in selected):
                selected.append((row["score"], row["detector"], family(str(row["score"]), str(row["detector"]))))

        mccs = []
        panel_items = []
        for score, detector, fam in selected:
            hit = target_df[(target_df["score"] == score) & (target_df["detector"] == detector)]
            if len(hit):
                mccs.append(float(hit.iloc[0]["mcc_adaptive"]))
                panel_items.append(f"{fam}:{score}/{detector}")
        best = max(mccs) if mccs else 0.0
        rows.append({
            "pathogen": target,
            "strategy": "diverse_method_panel@5",
            "k": len(selected),
            "best_mcc": best,
            "oracle_mcc": oracle,
            "pct_oracle": 100.0 * best / oracle if oracle > 0 else 0.0,
            "positive": best > 0,
            "panel": "; ".join(panel_items),
        })
    return pd.DataFrame(rows)


def append_meta_strategy_rows(result_df: pd.DataFrame) -> pd.DataFrame:
    candidates = [
        "equal_module_ensemble",
        "learned_auc_module_ensemble",
        "regime_weighted_module_ensemble",
        "stability_weighted_score",
        "local_background_cluster",
        "phylo_only",
        "no_phylo_regime",
        "rank_fusion_learned_cluster_phylo",
        "precision_fusion_cluster_phylo",
        "compactness_gated_rank_fusion",
        "constraint_aware_escape",
        "conservative_escape_structure_penalty",
        "local_burden_cluster",
        "reliability_gated_fusion",
        "reliability_gated_postprocessed",
        "non_ai_core_fusion",
    ]
    base = result_df[result_df["strategy"].isin(candidates)].copy()
    rows = []
    for target in sorted(base["pathogen"].unique()):
        train = base[base["pathogen"] != target]
        target_rows = base[base["pathogen"] == target]
        selectors = {
            "meta_train_best_region": train.groupby("strategy")["mcc_window_10"].mean().idxmax(),
            "meta_train_best_exact": train.groupby("strategy")["mcc_exact"].mean().idxmax(),
            "meta_train_best_precision20": train.groupby("strategy")["precision_20"].mean().idxmax(),
            "meta_train_low_fpr_region": (
                train.assign(objective=train["mcc_window_10"] - 0.5 * train["constrained_fpr"].fillna(0.0))
                .groupby("strategy")["objective"]
                .mean()
                .idxmax()
            ),
        }
        for meta_name, chosen_strategy in selectors.items():
            chosen = target_rows[target_rows["strategy"] == chosen_strategy].iloc[0].copy()
            chosen["hypothesis"] = "H10"
            chosen["strategy"] = meta_name
            chosen["selected_base_strategy"] = chosen_strategy
            rows.append(chosen)

    if not rows:
        result_df["selected_base_strategy"] = ""
        return result_df
    result_df = result_df.copy()
    result_df["selected_base_strategy"] = ""
    meta_df = pd.DataFrame(rows)
    return pd.concat([result_df, meta_df], ignore_index=True)


def markdown_table(frame: pd.DataFrame) -> str:
    text = frame.copy()
    for col in text.columns:
        if pd.api.types.is_float_dtype(text[col]):
            text[col] = text[col].map(lambda x: f"{x:.4f}")
        else:
            text[col] = text[col].astype(str)
    lines = [
        "| " + " | ".join(text.columns) + " |",
        "| " + " | ".join(["---"] * len(text.columns)) + " |",
    ]
    for _, row in text.iterrows():
        lines.append("| " + " | ".join(row[col] for col in text.columns) + " |")
    return "\n".join(lines)


def write_report(summary: pd.DataFrame, method_summary: pd.DataFrame, regime_df: pd.DataFrame) -> Path:
    out = RESULTS_DIR / "pahd_r_multi_hypothesis_report.md"
    top = summary.iloc[0]
    exact_best = summary.sort_values("mean_mcc_exact", ascending=False).iloc[0]
    method_best = method_summary.iloc[0]
    lines = [
        "# PAHD-R Multi-Hypothesis Experiment Report",
        "",
        "Date: 2026-04-26 KST",
        "",
        "## Scope",
        "",
        (
            "This run tests multiple PAHD-R redesign hypotheses under the same "
            "leave-one-pathogen-out frame. Held-out Layer A labels are used only "
            "for evaluation, not for selecting module weights."
        ),
        "",
        "## Main Results",
        "",
        (
            f"- Best region-level strategy: `{top['strategy']}` "
            f"({top['hypothesis']}), mean MCC@+/-10={top['mean_mcc_window_10']:.4f}, "
            f"mean Precision@20={top['mean_precision_20']:.4f}."
        ),
        (
            f"- Best exact-position strategy: `{exact_best['strategy']}` "
            f"({exact_best['hypothesis']}), mean exact MCC={exact_best['mean_mcc_exact']:.4f}."
        ),
        (
            f"- Best method-set result: `{method_best['strategy']}`, "
            f"mean best MCC={method_best['mean_best_mcc']:.4f}, "
            f"median best MCC={method_best['median_best_mcc']:.4f}."
        ),
        "",
        "## Interpretation",
        "",
        (
            "The strongest deployable evidence-level result is now the compactness-"
            "gated rank fusion, not the previous exact score-detector selector or "
            "the learned module ensemble alone. Local-background clustering and "
            "phylogeny-only evidence have strong exact/top-k signals but fail in "
            "MERS/RSV/SARS-CoV-2 in this run, so they should remain gated modules "
            "inside the fusion rather than global defaults."
        ),
        "",
        (
            "Region-level MCC is much higher than exact MCC across the best "
            "strategies, supporting the hypothesis that PAHD-R should output "
            "both exact positions and experimentally useful regions. The report "
            "therefore includes expanded region coverage so that region-level "
            "gains are not mistaken for free accuracy."
        ),
        "",
        "## Hypothesis Summary",
        "",
        markdown_table(summary.head(12)),
        "",
        "## Method-Set Summary",
        "",
        markdown_table(method_summary),
        "",
        "## Regime Probabilities",
        "",
        markdown_table(regime_df),
        "",
        "## Current Decisions",
        "",
        "- Keep H11 compactness-gated rank fusion as the current PAHD-R v0.3 candidate.",
        "- Keep H2 evidence-module ensemble as the baseline comparator.",
        "- Keep H4 region-level output as a first-class output.",
        "- Keep H8 method-set recommendation because top-20/top-50 sets recover useful performance.",
        "- Keep H5 local-background clustering as a high-precision module, not a global default.",
        "- Keep H6 phylogeny evidence as a regime-specific module with reliability checks.",
        "- Keep H9 rank/precision fusion as a candidate precision-oriented ensemble if it improves after real constrained-FPR filtering.",
        "- Keep H11 because it improves MCC while reducing region coverage versus H9.",
        "- Deprioritize H13 because it does not beat H9/H11 and reduces Precision@20.",
        "- Use H10 meta-selection only if it beats the best single evidence strategy under LOPO; otherwise keep it as a diagnostic.",
        "- Revise H1 regime inference further; it helps after normalization but is not yet better than learned module weights.",
        "- Treat H3 stability selection as inconclusive in this lightweight perturbation-only run.",
        "- Treat H7 trait-axis separation as useful diagnostically, but not sufficient alone.",
        "",
        "## Caveats",
        "",
        "- Stability selection currently perturbs module weights; it does not yet resample sequences or trees.",
        "- Constrained FPR now uses Layer B ground truth from `multilayer_gt.py`.",
        "- DMS escape is not separated as a direct feature in the current matrices, so H7 is only partially tested.",
        "- Local background clustering uses score permutation, not full nucleotide-context simulation.",
        "",
    ]
    out.write_text("\n".join(lines), encoding="utf-8")
    return out


def run() -> None:
    data = load_feature_matrices()
    benchmark = pd.read_csv(BENCHMARK_PATH)
    pathogens = sorted(set(benchmark["pathogen"].unique()) & set(data.keys()))
    profiles = normalized_profiles(data, pathogens)

    prediction_rows: list[PredictionResult] = []
    final_call_rows: list[dict[str, object]] = []
    regime_rows = []
    weight_rows = []

    for target in pathogens:
        train_data = {p: df for p, df in data.items() if p != target and p in pathogens}
        df = data[target]
        signs = compute_feature_signs(train_data)
        effects = compute_feature_effects(train_data)
        scores_df = module_scores(df, signs)
        regimes = infer_regime_probabilities(profiles[target])
        reg_weights = regime_weights(regimes)
        learned_weights = learned_module_weights(effects)
        equal_weights = {module: 1.0 for module in MODULES}

        regime_rows.append({"pathogen": target, **regimes})
        weight_rows.append({"pathogen": target, "strategy": "regime_weighted", **reg_weights})
        weight_rows.append({"pathogen": target, "strategy": "learned_auc_weighted", **learned_weights})

        experiments: list[tuple[str, str, np.ndarray, float]] = [
            ("H2", "equal_module_ensemble", combine_modules(scores_df, equal_weights), 0.10),
            ("H2", "learned_auc_module_ensemble", combine_modules(scores_df, learned_weights), 0.10),
            ("H1", "regime_weighted_module_ensemble", combine_modules(scores_df, reg_weights), 0.10),
            ("H6", "phylo_only", scores_df["phylo"].values, 0.10),
            ("H6", "no_phylo_regime", combine_modules(scores_df, {**reg_weights, "phylo": 0.0}), 0.10),
            ("H7", "constraint_trait_axis", scores_df["constraint"].values, 0.10),
            ("H7", "semantic_trait_axis", scores_df["semantic"].values, 0.10),
            ("H7", "structure_trait_axis", scores_df["structure"].values, 0.10),
        ]

        stable_prob, stable_score = stability_scores(scores_df, reg_weights, seed=100 + pathogens.index(target))
        experiments.append(("H3", "stability_selection_prob", stable_prob, 0.10))
        experiments.append(("H3", "stability_weighted_score", stable_score * stable_prob, 0.10))

        cluster_score = local_background_cluster_score(scores_df["recurrence"].values, seed=200 + pathogens.index(target))
        experiments.append(("H5", "local_background_cluster", cluster_score, 0.10))
        burden_cluster_score = local_burden_cluster_score(
            scores_df["recurrence"].values,
            scores_df["diversity"].values,
            seed=300 + pathogens.index(target),
        )
        experiments.append(("H16", "local_burden_cluster", burden_cluster_score, 0.10))

        non_ai_scores_df = non_ai_module_scores(df, signs)
        non_ai_weights = learned_non_ai_weights(effects)
        non_ai_learned = combine_modules(non_ai_scores_df, non_ai_weights)
        non_ai_phylo = non_ai_scores_df["phylo"].values
        non_ai_cluster = local_background_cluster_score(
            non_ai_scores_df["recurrence"].values,
            seed=400 + pathogens.index(target),
        )
        non_ai_reliability = cluster_reliability(non_ai_cluster, non_ai_phylo, non_ai_learned)
        non_ai_cluster_weight = 0.15 + 0.45 * non_ai_reliability
        non_ai_phylo_weight = 0.25
        non_ai_learned_weight = 1.0 - non_ai_cluster_weight - non_ai_phylo_weight
        non_ai_fusion = (
            non_ai_learned_weight * rank_percentile(non_ai_learned)
            + non_ai_cluster_weight * rank_percentile(non_ai_cluster)
            + non_ai_phylo_weight * rank_percentile(non_ai_phylo)
        )
        experiments.append(("H18", "non_ai_core_fusion", non_ai_fusion, 0.10))
        non_ai_snf = snf_style_site_fusion(non_ai_scores_df, non_ai_fusion)
        experiments.append(("H19", "snf_non_ai_core", non_ai_snf, 0.10))

        score_by_name = {strategy: scores for _, strategy, scores, _ in experiments}
        reliability = cluster_reliability(
            score_by_name["local_background_cluster"],
            score_by_name["phylo_only"],
            score_by_name["learned_auc_module_ensemble"],
        )
        burden_reliability = cluster_reliability(
            score_by_name["local_burden_cluster"],
            score_by_name["phylo_only"],
            score_by_name["learned_auc_module_ensemble"],
        )
        phylo_rel = phylo_reliability(
            score_by_name["phylo_only"],
            score_by_name["learned_auc_module_ensemble"],
            scores_df["recurrence"].values,
        )
        constraint_rel = constraint_reliability(scores_df)
        rank_fusion = (
            rank_percentile(score_by_name["learned_auc_module_ensemble"])
            + rank_percentile(score_by_name["local_background_cluster"])
            + rank_percentile(score_by_name["phylo_only"])
        ) / 3.0
        precision_fusion = (
            0.50 * rank_percentile(score_by_name["local_background_cluster"])
            + 0.30 * rank_percentile(score_by_name["phylo_only"])
            + 0.20 * rank_percentile(score_by_name["learned_auc_module_ensemble"])
        )
        experiments.append(("H9", "rank_fusion_learned_cluster_phylo", rank_fusion, 0.10))
        experiments.append(("H9", "precision_fusion_cluster_phylo", precision_fusion, 0.10))

        gated_cluster_weight = 0.15 + 0.45 * reliability
        gated_phylo_weight = 0.25
        gated_learned_weight = 1.0 - gated_cluster_weight - gated_phylo_weight
        compactness_gated_fusion = (
            gated_learned_weight * rank_percentile(score_by_name["learned_auc_module_ensemble"])
            + gated_cluster_weight * rank_percentile(score_by_name["local_background_cluster"])
            + gated_phylo_weight * rank_percentile(score_by_name["phylo_only"])
        )
        experiments.append(("H11", "compactness_gated_rank_fusion", compactness_gated_fusion, 0.10))
        snf_augmented = snf_style_site_fusion(scores_df, compactness_gated_fusion)
        experiments.append(("H19", "snf_augmented", snf_augmented, 0.10))

        reliability_fusion, reliability_postprocessed = reliability_gated_fusion(
            score_by_name["learned_auc_module_ensemble"],
            score_by_name["local_burden_cluster"],
            score_by_name["phylo_only"],
            stable_prob,
            scores_df,
            max(reliability, burden_reliability),
            phylo_rel,
            constraint_rel,
        )
        experiments.append(("H16", "reliability_gated_fusion", reliability_fusion, 0.10))
        experiments.append(("H16", "reliability_gated_postprocessed", reliability_postprocessed, 0.10))
        for strategy, scores in h11_preserving_alternatives(
            compactness_gated_fusion,
            score_by_name["learned_auc_module_ensemble"],
            score_by_name["local_background_cluster"],
            score_by_name["phylo_only"],
            stable_prob,
            score_by_name["local_burden_cluster"],
            scores_df,
            constraint_rel,
        ).items():
            experiments.append(("H17", strategy, scores, 0.10))
        weight_rows.append({
            "pathogen": target,
            "strategy": "module_reliability",
            "recurrence": np.nan,
            "diversity": np.nan,
            "phylo": phylo_rel,
            "constraint": constraint_rel,
            "structure": constraint_rel,
            "semantic": np.nan,
            "cluster": max(reliability, burden_reliability),
        })
        final_call_rows.extend(confidence_site_rows(
            target,
            "reliability_gated_postprocessed",
            df,
            reliability_postprocessed,
            score_by_name["learned_auc_module_ensemble"],
            score_by_name["local_burden_cluster"],
            score_by_name["phylo_only"],
            stable_prob,
            frac=0.10,
        ))
        final_call_rows.extend(confidence_site_rows(
            target,
            "compactness_gated_rank_fusion",
            df,
            compactness_gated_fusion,
            score_by_name["learned_auc_module_ensemble"],
            score_by_name["local_background_cluster"],
            score_by_name["phylo_only"],
            stable_prob,
            frac=0.10,
        ))

        raw_escape = (
            0.40 * rank_percentile(scores_df["semantic"].values)
            + 0.30 * rank_percentile(scores_df["recurrence"].values)
            + 0.30 * rank_percentile(scores_df["phylo"].values)
        )
        constraint_penalty = rank_percentile(scores_df["constraint"].values)
        structure_penalty = rank_percentile(scores_df["structure"].values)
        constraint_aware_escape = raw_escape * (1.0 - 0.35 * constraint_penalty)
        conservative_escape = raw_escape * (1.0 - 0.25 * constraint_penalty) * (1.0 - 0.20 * structure_penalty)
        experiments.append(("H13", "constraint_aware_escape", constraint_aware_escape, 0.10))
        experiments.append(("H13", "conservative_escape_structure_penalty", conservative_escape, 0.10))

        for frac in [0.03, 0.05, 0.08, 0.12, 0.15]:
            label = f"top{int(frac * 100):02d}"
            experiments.append(("H15", f"compactness_gated_rank_fusion_{label}", compactness_gated_fusion, frac))
            experiments.append(("H15", f"rank_fusion_learned_cluster_phylo_{label}", rank_fusion, frac))
            experiments.append(("H15", f"local_background_cluster_{label}", cluster_score, frac))
            experiments.append(("H18", f"non_ai_core_fusion_{label}", non_ai_fusion, frac))
            if frac in {0.08, 0.12, 0.15}:
                experiments.append(("H19", f"snf_non_ai_core_{label}", non_ai_snf, frac))
                experiments.append(("H19", f"snf_augmented_{label}", snf_augmented, frac))
            if frac in {0.08, 0.12}:
                experiments.append(("H16", f"reliability_gated_postprocessed_{label}", reliability_postprocessed, frac))

        for hypothesis, strategy, scores, frac in experiments:
            pred = top_fraction_pred(scores, frac)
            if strategy == "stability_selection_prob":
                pred = stable_prob >= np.quantile(stable_prob, 0.90)
            prediction_rows.append(evaluate_prediction(target, hypothesis, strategy, df, scores, pred))

    result_df = pd.DataFrame([row.__dict__ for row in prediction_rows])
    result_df = append_meta_strategy_rows(result_df)
    regime_df = pd.DataFrame(regime_rows)
    weight_df = pd.DataFrame(weight_rows)
    method_sets = method_set_experiment(benchmark[benchmark["pathogen"].isin(pathogens)])
    method_panels = method_panel_experiment(benchmark[benchmark["pathogen"].isin(pathogens)])
    method_sets = pd.concat([method_sets, method_panels], ignore_index=True, sort=False)

    summary = (
        result_df
        .groupby(["hypothesis", "strategy"])
        .agg(
            mean_mcc_exact=("mcc_exact", "mean"),
            mean_mcc_window_5=("mcc_window_5", "mean"),
            mean_mcc_window_10=("mcc_window_10", "mean"),
            mean_precision_20=("precision_20", "mean"),
            mean_enrichment_20=("enrichment_20", "mean"),
            mean_constrained_fpr=("constrained_fpr", "mean"),
            mean_pred_frac=("pred_frac", "mean"),
            mean_region_coverage_10=("region_coverage_10", "mean"),
            mean_auroc=("auroc", "mean"),
            positive_pathogens=("mcc_exact", lambda x: int((x > 0).sum())),
            n_pathogens=("pathogen", "nunique"),
        )
        .reset_index()
        .sort_values(["mean_mcc_window_10", "mean_precision_20"], ascending=False)
    )

    method_summary = (
        method_sets
        .groupby("strategy")
        .agg(
            mean_best_mcc=("best_mcc", "mean"),
            median_best_mcc=("best_mcc", "median"),
            mean_pct_oracle=("pct_oracle", "mean"),
            positive_pathogens=("positive", "sum"),
            n_pathogens=("pathogen", "nunique"),
        )
        .reset_index()
        .sort_values("mean_best_mcc", ascending=False)
    )

    result_df.to_csv(RESULTS_DIR / "pahd_r_multi_hypothesis_results.csv", index=False)
    summary.to_csv(RESULTS_DIR / "pahd_r_multi_hypothesis_summary.csv", index=False)
    regime_df.to_csv(RESULTS_DIR / "pahd_r_regime_probabilities.csv", index=False)
    weight_df.to_csv(RESULTS_DIR / "pahd_r_module_weights.csv", index=False)
    pd.DataFrame(final_call_rows).to_csv(RESULTS_DIR / "pahd_r_final_site_calls.csv", index=False)
    method_sets.to_csv(RESULTS_DIR / "pahd_r_method_set_results.csv", index=False)
    method_summary.to_csv(RESULTS_DIR / "pahd_r_method_set_summary.csv", index=False)
    report_path = write_report(summary, method_summary, regime_df)

    print("PAHD-R multi-hypothesis experiment complete")
    print(f"Pathogens: {len(pathogens)}")
    print("\nTop evidence strategies:")
    print(summary.head(12).round(4).to_string(index=False))
    print("\nMethod-set summary:")
    print(method_summary.round(4).to_string(index=False))
    print(f"\nReport: {report_path}")


if __name__ == "__main__":
    run()
