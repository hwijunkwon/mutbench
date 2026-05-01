#!/usr/bin/env python3
"""Negative-control and coordinate-robustness audit for PAHD-R."""

from __future__ import annotations

from pathlib import Path
import sys

import numpy as np
import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parent.parent
RESULTS_DIR = PROJECT_ROOT / "results" / "mutbench"
sys.path.insert(0, str(PROJECT_ROOT / "scripts"))
import run_pahd_r_multi_hypothesis as pahd  # noqa: E402


def candidate_scores(data: dict[str, pd.DataFrame], pathogens: list[str], target: str) -> dict[str, np.ndarray]:
    train_data = {p: df for p, df in data.items() if p != target and p in pathogens}
    df = data[target]
    signs = pahd.compute_feature_signs(train_data)
    effects = pahd.compute_feature_effects(train_data)

    scores_df = pahd.module_scores(df, signs)
    learned = pahd.combine_modules(scores_df, pahd.learned_module_weights(effects))
    phylo = scores_df["phylo"].values
    cluster = pahd.local_background_cluster_score(scores_df["recurrence"].values, seed=200 + pathogens.index(target))
    reliability = pahd.cluster_reliability(cluster, phylo, learned)
    cluster_w = 0.15 + 0.45 * reliability
    phylo_w = 0.25
    learned_w = 1.0 - cluster_w - phylo_w
    h11 = (
        learned_w * pahd.rank_percentile(learned)
        + cluster_w * pahd.rank_percentile(cluster)
        + phylo_w * pahd.rank_percentile(phylo)
    )
    h17 = pahd.h11_preserving_alternatives(
        h11,
        learned,
        cluster,
        phylo,
        np.ones(len(df), dtype=float),
        cluster,
        scores_df,
        pahd.constraint_reliability(scores_df),
    )["h11_soft_constraint_post"]

    non_ai_scores = pahd.non_ai_module_scores(df, signs)
    non_ai_weights = pahd.learned_non_ai_weights(effects)
    non_ai_learned = pahd.combine_modules(non_ai_scores, non_ai_weights)
    non_ai_phylo = non_ai_scores["phylo"].values
    non_ai_cluster = pahd.local_background_cluster_score(
        non_ai_scores["recurrence"].values,
        seed=400 + pathogens.index(target),
    )
    non_ai_rel = pahd.cluster_reliability(non_ai_cluster, non_ai_phylo, non_ai_learned)
    non_ai_cluster_w = 0.15 + 0.45 * non_ai_rel
    h18 = (
        (1.0 - non_ai_cluster_w - 0.25) * pahd.rank_percentile(non_ai_learned)
        + non_ai_cluster_w * pahd.rank_percentile(non_ai_cluster)
        + 0.25 * pahd.rank_percentile(non_ai_phylo)
    )

    review = (
        0.34 * pahd.rank_percentile(non_ai_scores["recurrence"].values)
        + 0.33 * pahd.rank_percentile(non_ai_scores["diversity"].values)
        + 0.33 * pahd.rank_percentile(non_ai_scores["phylo"].values)
    )
    review = 0.80 * pahd.rank_percentile(review) + 0.20 * pahd.rank_percentile(non_ai_cluster)

    return {
        "PAHD-R-Augmented": h17,
        "PAHD-R-Core": h18,
        "PAHD-R-Review": review,
    }


def shifted_labels(y: np.ndarray, shift: int) -> np.ndarray:
    out = np.zeros_like(y, dtype=int)
    idx = np.where(y > 0)[0] + shift
    idx = idx[(idx >= 0) & (idx < len(y))]
    out[idx] = 1
    return out


def custom_region_mcc(y_true: np.ndarray, pred: np.ndarray, window: int) -> float:
    return pahd.region_mcc(y_true.astype(int), pred.astype(bool), window)


def evaluate_with_labels(pathogen: str, df: pd.DataFrame, score: np.ndarray, y: np.ndarray, frac: float, window: int) -> dict[str, float]:
    pred = pahd.top_fraction_pred(score, frac)
    p20, e20 = pahd.precision_and_enrichment(y, score, 20)
    return {
        "mcc_exact": custom_region_mcc(y, pred, 0),
        "mcc_window": custom_region_mcc(y, pred, window),
        "precision_20": p20,
        "enrichment_20": e20,
        "constrained_fpr": pahd.constrained_fpr(pathogen, len(df), pred),
        "region_coverage": pahd.expanded_coverage(pred, window),
    }


def run() -> None:
    data = pahd.load_feature_matrices()
    benchmark = pd.read_csv(RESULTS_DIR / "multilayer_9pathogen_results.csv")
    pathogens = sorted(set(benchmark["pathogen"].unique()) & set(data.keys()))

    decoy_rows = []
    coord_rows = []
    rng = np.random.default_rng(20260426)

    for target in pathogens:
        df = data[target]
        y = df["layer_a"].astype(int).values
        scores = candidate_scores(data, pathogens, target)

        decoys = {}
        for name, score in scores.items():
            decoys[name] = score
            decoys[f"decoy_shuffle:{name}"] = rng.permutation(score)
            decoys[f"decoy_reverse:{name}"] = score[::-1]
        decoys["decoy_random_uniform"] = rng.random(len(df))
        region_seed = np.zeros(len(df))
        for start in rng.choice(np.arange(len(df)), size=min(10, len(df)), replace=False):
            region_seed[max(0, start - 5): min(len(df), start + 6)] += 1.0
        decoys["decoy_random_regions"] = region_seed + 0.05 * rng.random(len(df))

        for strategy, score in decoys.items():
            frac = 0.08 if strategy == "PAHD-R-Review" else 0.10
            metrics = evaluate_with_labels(target, df, score, y, frac, 10)
            decoy_rows.append({"pathogen": target, "strategy": strategy, "frac": frac, **metrics})

        for strategy, score in scores.items():
            frac = 0.08 if strategy == "PAHD-R-Review" else 0.10
            for shift in [-10, -5, -3, 0, 3, 5, 10]:
                y_shift = shifted_labels(y, shift)
                for window in [5, 10, 15, 20]:
                    metrics = evaluate_with_labels(target, df, score, y_shift, frac, window)
                    coord_rows.append({
                        "pathogen": target,
                        "strategy": strategy,
                        "frac": frac,
                        "label_shift": shift,
                        "window": window,
                        **metrics,
                    })

    decoy_df = pd.DataFrame(decoy_rows)
    coord_df = pd.DataFrame(coord_rows)

    decoy_summary = (
        decoy_df.groupby("strategy")
        .agg(
            mean_mcc_exact=("mcc_exact", "mean"),
            mean_mcc_window_10=("mcc_window", "mean"),
            mean_precision_20=("precision_20", "mean"),
            mean_constrained_fpr=("constrained_fpr", "mean"),
            mean_region_coverage_10=("region_coverage", "mean"),
            positive_pathogens=("mcc_exact", lambda x: int((x > 0).sum())),
        )
        .reset_index()
        .sort_values(["mean_mcc_window_10", "mean_mcc_exact"], ascending=False)
    )

    coord_summary = (
        coord_df.groupby(["strategy", "label_shift", "window"])
        .agg(
            mean_mcc_exact=("mcc_exact", "mean"),
            mean_mcc_window=("mcc_window", "mean"),
            mean_precision_20=("precision_20", "mean"),
            mean_region_coverage=("region_coverage", "mean"),
        )
        .reset_index()
        .sort_values(["strategy", "window", "label_shift"])
    )

    decoy_df.to_csv(RESULTS_DIR / "pahd_r_decoy_control_results.csv", index=False)
    decoy_summary.to_csv(RESULTS_DIR / "pahd_r_decoy_control_summary.csv", index=False)
    coord_df.to_csv(RESULTS_DIR / "pahd_r_coordinate_robustness_results.csv", index=False)
    coord_summary.to_csv(RESULTS_DIR / "pahd_r_coordinate_robustness_summary.csv", index=False)

    report = [
        "# PAHD-R Decoy and Coordinate Robustness Audit",
        "",
        "Date: 2026-04-26 KST",
        "",
        "## Decoy Control Summary",
        "",
        markdown_table(decoy_summary),
        "",
        "## Coordinate Robustness Summary",
        "",
        markdown_table(coord_summary[
            (coord_summary["window"] == 10)
            & (coord_summary["label_shift"].isin([-10, -5, 0, 5, 10]))
        ]),
        "",
        "## Interpretation",
        "",
        (
            "Decoy controls should remain below the real PAHD-R strategies. "
            "Coordinate-shift results should degrade as labels move away from "
            "their original positions; moderate degradation supports the need "
            "for region-level reporting."
        ),
        "",
    ]
    out = RESULTS_DIR / "pahd_r_decoy_coordinate_robustness_audit.md"
    out.write_text("\n".join(report), encoding="utf-8")
    print(out)
    print(decoy_summary.round(4).to_string(index=False))


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
