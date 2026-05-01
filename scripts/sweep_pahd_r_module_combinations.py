#!/usr/bin/env python3
"""Sweep PAHD-R evidence module combinations under LOPO evaluation."""

from __future__ import annotations

from itertools import combinations
from pathlib import Path
import sys

import numpy as np
import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parent.parent
RESULTS_DIR = PROJECT_ROOT / "results" / "mutbench"
sys.path.insert(0, str(PROJECT_ROOT / "scripts"))
import run_pahd_r_multi_hypothesis as pahd  # noqa: E402


MODULE_SETS = {
    "recurrence": ["freq", "rare_freq"],
    "diversity": ["entropy"],
    "phylo": ["homoplasy", "dnds_proxy"],
    "structure": ["sasa", "grantham"],
    "constraint": ["esm2_llr", "plddt"],
    "semantic": ["semantic_change"],
}


def module_scores_for_set(df: pd.DataFrame, signs: dict[str, float], modules: dict[str, list[str]]) -> pd.DataFrame:
    out = {}
    for module, feats in modules.items():
        parts = [pahd.robust_z(df[feat].values) * signs.get(feat, 1.0) for feat in feats]
        out[module] = np.mean(np.column_stack(parts), axis=1)
    return pd.DataFrame(out)


def feature_effects_for_modules(train_data: dict[str, pd.DataFrame], modules: dict[str, list[str]]) -> dict[str, float]:
    effects = pahd.compute_feature_effects(train_data)
    weights = {}
    for module, feats in modules.items():
        weights[module] = float(np.mean([effects.get(feat, 0.0) for feat in feats]))
    return pahd.normalize_weights(weights)


def rank_fusion_score(scores_df: pd.DataFrame, weights: dict[str, float]) -> np.ndarray:
    weights = pahd.normalize_weights(weights)
    score = np.zeros(len(scores_df))
    for module, weight in weights.items():
        score += weight * pahd.rank_percentile(scores_df[module].values)
    return score


def cluster_augmented_score(scores_df: pd.DataFrame, base_score: np.ndarray, selected_modules: set[str]) -> np.ndarray:
    if "recurrence" not in selected_modules:
        return base_score
    cluster = pahd.local_background_cluster_score(scores_df["recurrence"].values)
    parts = [0.80 * pahd.rank_percentile(base_score), 0.20 * pahd.rank_percentile(cluster)]
    return sum(parts)


def evaluate_combo(
    pathogen: str,
    df: pd.DataFrame,
    combo_name: str,
    score: np.ndarray,
    frac: float,
) -> dict[str, object]:
    pred = pahd.top_fraction_pred(score, frac)
    result = pahd.evaluate_prediction(pathogen, "COMBO", combo_name, df, score, pred)
    row = result.__dict__
    row["frac"] = frac
    return row


def combo_names() -> list[tuple[str, tuple[str, ...]]]:
    names = list(MODULE_SETS.keys())
    combos = []
    for r in range(1, len(names) + 1):
        for combo in combinations(names, r):
            combos.append(("+".join(combo), combo))
    return combos


def run() -> None:
    data = pahd.load_feature_matrices()
    benchmark = pd.read_csv(RESULTS_DIR / "multilayer_9pathogen_results.csv")
    pathogens = sorted(set(benchmark["pathogen"].unique()) & set(data.keys()))

    rows = []
    for target in pathogens:
        train_data = {p: df for p, df in data.items() if p != target and p in pathogens}
        signs = pahd.compute_feature_signs(train_data)
        df = data[target]
        for combo_name, combo in combo_names():
            selected = {module: MODULE_SETS[module] for module in combo}
            scores_df = module_scores_for_set(df, signs, selected)
            weights = feature_effects_for_modules(train_data, selected)
            base = rank_fusion_score(scores_df, weights)
            cluster_aug = cluster_augmented_score(scores_df, base, set(combo))
            for score_name, score in [
                ("rank", base),
                ("rank_cluster_aug", cluster_aug),
            ]:
                strategy = f"{score_name}:{combo_name}"
                for frac in [0.08, 0.10, 0.12, 0.15]:
                    rows.append(evaluate_combo(target, df, strategy, score, frac))

    result_df = pd.DataFrame(rows)
    summary = (
        result_df
        .groupby(["strategy", "frac"])
        .agg(
            mean_mcc_exact=("mcc_exact", "mean"),
            mean_mcc_window_10=("mcc_window_10", "mean"),
            mean_precision_20=("precision_20", "mean"),
            mean_constrained_fpr=("constrained_fpr", "mean"),
            mean_region_coverage_10=("region_coverage_10", "mean"),
            mean_auroc=("auroc", "mean"),
            positive_pathogens=("mcc_exact", lambda x: int((x > 0).sum())),
            n_pathogens=("pathogen", "nunique"),
        )
        .reset_index()
    )
    summary["objective_balanced"] = (
        summary["mean_mcc_exact"]
        + 0.30 * summary["mean_mcc_window_10"]
        + 0.15 * summary["mean_precision_20"]
        - 0.10 * summary["mean_constrained_fpr"].fillna(0.0)
        - 0.05 * summary["mean_region_coverage_10"]
    )
    summary = summary.sort_values(
        ["objective_balanced", "mean_mcc_exact", "mean_mcc_window_10"],
        ascending=False,
    )

    module_rows = []
    for module in MODULE_SETS:
        with_module = summary[summary["strategy"].str.contains(module, regex=False)]
        without_module = summary[~summary["strategy"].str.contains(module, regex=False)]
        module_rows.append({
            "module": module,
            "mean_objective_with": float(with_module["objective_balanced"].mean()),
            "mean_objective_without": float(without_module["objective_balanced"].mean()),
            "delta_with_minus_without": float(with_module["objective_balanced"].mean() - without_module["objective_balanced"].mean()),
            "best_rank_with": int(summary.reset_index(drop=True).index[summary["strategy"].str.contains(module, regex=False)][0]) + 1
            if len(with_module) else np.nan,
        })
    module_df = pd.DataFrame(module_rows).sort_values("delta_with_minus_without", ascending=False)

    result_df.to_csv(RESULTS_DIR / "pahd_r_module_combination_results.csv", index=False)
    summary.to_csv(RESULTS_DIR / "pahd_r_module_combination_summary.csv", index=False)
    module_df.to_csv(RESULTS_DIR / "pahd_r_module_contribution_summary.csv", index=False)

    report = [
        "# PAHD-R Module Combination Sweep",
        "",
        "Date: 2026-04-26 KST",
        "",
        "## Scope",
        "",
        "All non-empty combinations of six evidence modules were evaluated under LOPO:",
        "",
        "- recurrence",
        "- diversity",
        "- phylo",
        "- structure",
        "- constraint",
        "- semantic",
        "",
        "Each combination was tested with rank fusion and recurrence-cluster-augmented rank fusion at top-8/10/12/15 percent operating points.",
        "",
        "## Top 20 Combinations",
        "",
        markdown_table(summary.head(20)),
        "",
        "## Module Contribution",
        "",
        markdown_table(module_df),
        "",
        "## Interpretation",
        "",
        (
            "This is a broad screening sweep, not a final model-selection proof. "
            "The result should be used to identify robust module families and "
            "candidate combinations for adversarial follow-up."
        ),
        "",
    ]
    out = RESULTS_DIR / "pahd_r_module_combination_sweep.md"
    out.write_text("\n".join(report), encoding="utf-8")
    print(out)
    print(summary.head(15).round(4).to_string(index=False))


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


if __name__ == "__main__":
    run()
