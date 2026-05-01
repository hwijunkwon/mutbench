#!/usr/bin/env python3
"""Audit whether AI/PLM-derived features are justified in PAHD-R."""

from __future__ import annotations

from pathlib import Path
import sys

import numpy as np
import pandas as pd
from sklearn.metrics import roc_auc_score

PROJECT_ROOT = Path(__file__).resolve().parent.parent
RESULTS_DIR = PROJECT_ROOT / "results" / "mutbench"
sys.path.insert(0, str(PROJECT_ROOT / "scripts"))
import run_pahd_r_multi_hypothesis as pahd  # noqa: E402


AI_FEATURES = ["esm2_llr", "plddt", "semantic_change"]
CORE_MODULES = {
    "recurrence": ["freq", "rare_freq"],
    "diversity": ["entropy"],
    "phylo": ["homoplasy", "dnds_proxy"],
    "structure_non_ai": ["sasa", "grantham"],
}


def auc_or_nan(y: np.ndarray, x: np.ndarray) -> float:
    x = np.nan_to_num(x, nan=0.0)
    if y.sum() < 2 or (len(y) - y.sum()) < 2 or np.std(x) < 1e-12:
        return np.nan
    try:
        return float(roc_auc_score(y, x))
    except ValueError:
        return np.nan


def no_ai_module_scores(df: pd.DataFrame, signs: dict[str, float]) -> pd.DataFrame:
    out = {}
    for module, feats in CORE_MODULES.items():
        parts = [pahd.robust_z(df[feat].values) * signs.get(feat, 1.0) for feat in feats]
        out[module] = np.mean(np.column_stack(parts), axis=1)
    return pd.DataFrame(out)


def no_ai_feature_effects(train_data: dict[str, pd.DataFrame]) -> dict[str, float]:
    effects = {}
    for feat in [f for feats in CORE_MODULES.values() for f in feats]:
        vals = []
        for df in train_data.values():
            y = df["layer_a"].astype(int).values
            x = np.nan_to_num(df[feat].values, nan=0.0)
            val = auc_or_nan(y, x)
            if not np.isnan(val):
                vals.append(abs(val - 0.5))
        effects[feat] = float(np.mean(vals)) if vals else 0.0
    return effects


def learned_weights_for_modules(effects: dict[str, float], modules: dict[str, list[str]]) -> dict[str, float]:
    weights = {}
    for module, feats in modules.items():
        weights[module] = float(np.mean([effects.get(feat, 0.0) for feat in feats]))
    return pahd.normalize_weights(weights)


def no_ai_h11_score(data: dict[str, pd.DataFrame], pathogens: list[str], target: str) -> np.ndarray:
    train_data = {p: df for p, df in data.items() if p != target and p in pathogens}
    df = data[target]
    signs = pahd.compute_feature_signs(train_data)
    effects = no_ai_feature_effects(train_data)
    scores_df = no_ai_module_scores(df, signs)
    learned = pahd.combine_modules(scores_df, learned_weights_for_modules(effects, CORE_MODULES))
    phylo = scores_df["phylo"].values
    cluster = pahd.local_background_cluster_score(scores_df["recurrence"].values, seed=400 + pathogens.index(target))
    reliability = pahd.cluster_reliability(cluster, phylo, learned)
    gated_cluster_weight = 0.15 + 0.45 * reliability
    gated_phylo_weight = 0.25
    gated_learned_weight = 1.0 - gated_cluster_weight - gated_phylo_weight
    return (
        gated_learned_weight * pahd.rank_percentile(learned)
        + gated_cluster_weight * pahd.rank_percentile(cluster)
        + gated_phylo_weight * pahd.rank_percentile(phylo)
    )


def eval_scores(pathogen: str, df: pd.DataFrame, scores: np.ndarray) -> dict[str, float]:
    pred = pahd.top_fraction_pred(scores, 0.10)
    result = pahd.evaluate_prediction(pathogen, "AUDIT", "no_ai_h11", df, scores, pred)
    return {
        "mcc_exact": result.mcc_exact,
        "mcc_window_10": result.mcc_window_10,
        "precision_20": result.precision_20,
        "constrained_fpr": result.constrained_fpr,
        "region_coverage_10": result.region_coverage_10,
        "auroc": result.auroc,
    }


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


def run() -> None:
    data = pahd.load_feature_matrices()
    benchmark = pd.read_csv(RESULTS_DIR / "multilayer_9pathogen_results.csv")
    pathogens = sorted(set(benchmark["pathogen"].unique()) & set(data.keys()))
    current = pd.read_csv(RESULTS_DIR / "pahd_r_multi_hypothesis_results.csv")
    h17 = current[current["strategy"] == "h11_soft_constraint_post"].set_index("pathogen")

    feature_rows = []
    ablation_rows = []
    for pathogen in pathogens:
        df = data[pathogen]
        y = df["layer_a"].astype(int).values
        for feat in AI_FEATURES:
            x = np.nan_to_num(df[feat].values, nan=0.0)
            feature_rows.append({
                "pathogen": pathogen,
                "feature": feat,
                "coverage_nonzero": float(np.mean(x != 0.0)),
                "std": float(np.std(x)),
                "auc_layer_a": auc_or_nan(y, x),
                "auc_layer_a_inverted": auc_or_nan(y, -x),
            })

        scores = no_ai_h11_score(data, pathogens, pathogen)
        no_ai = eval_scores(pathogen, df, scores)
        row = {"pathogen": pathogen}
        for metric, value in no_ai.items():
            row[f"no_ai_{metric}"] = value
            row[f"h17_{metric}"] = float(h17.loc[pathogen, metric])
            row[f"delta_no_ai_minus_h17_{metric}"] = value - float(h17.loc[pathogen, metric])
        ablation_rows.append(row)

    feature_df = pd.DataFrame(feature_rows)
    ablation_df = pd.DataFrame(ablation_rows)
    summary = pd.DataFrame([{
        "strategy": "h11_soft_constraint_post",
        "mean_mcc_exact": float(h17["mcc_exact"].mean()),
        "mean_mcc_window_10": float(h17["mcc_window_10"].mean()),
        "mean_precision_20": float(h17["precision_20"].mean()),
        "mean_constrained_fpr": float(h17["constrained_fpr"].mean()),
        "mean_auroc": float(h17["auroc"].mean()),
    }, {
        "strategy": "non_ai_core_fusion",
        "mean_mcc_exact": float(ablation_df["no_ai_mcc_exact"].mean()),
        "mean_mcc_window_10": float(ablation_df["no_ai_mcc_window_10"].mean()),
        "mean_precision_20": float(ablation_df["no_ai_precision_20"].mean()),
        "mean_constrained_fpr": float(ablation_df["no_ai_constrained_fpr"].mean()),
        "mean_auroc": float(ablation_df["no_ai_auroc"].mean()),
    }])

    feature_df.to_csv(RESULTS_DIR / "pahd_r_plm_feature_validity.csv", index=False)
    ablation_df.to_csv(RESULTS_DIR / "pahd_r_no_ai_feature_ablation.csv", index=False)
    summary.to_csv(RESULTS_DIR / "pahd_r_no_ai_feature_ablation_summary.csv", index=False)

    report = [
        "# PAHD-R AI/PLM Feature Validity Audit",
        "",
        "Date: 2026-04-26 KST",
        "",
        "## Summary",
        "",
        markdown_table(summary),
        "",
        "## Interpretation",
        "",
        (
            "This audit tests whether the final PAHD-R candidate depends on "
            "AI-derived features (`esm2_llr`, `plddt`, `semantic_change`). The "
            "no-AI ablation removes those features and rebuilds the H11-style "
            "fusion from recurrence, diversity, phylogeny, SASA, and Grantham "
            "signals only."
        ),
        "",
        "If the no-AI ablation is competitive, PLM features should be described "
        "as optional supporting evidence rather than the foundation of PAHD-R.",
        "",
    ]
    out = RESULTS_DIR / "pahd_r_plm_feature_validity_audit.md"
    out.write_text("\n".join(report), encoding="utf-8")
    print(out)
    print(summary.round(4).to_string(index=False))


if __name__ == "__main__":
    run()
