#!/usr/bin/env python3
"""Adversarial audit for PAHD-R shrinkage trade-off candidates."""

from __future__ import annotations

from pathlib import Path
import sys

import numpy as np
import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parent.parent
RESULTS_DIR = PROJECT_ROOT / "results" / "mutbench"
sys.path.insert(0, str(PROJECT_ROOT / "scripts"))

import run_pahd_r_multi_hypothesis as pahd  # noqa: E402
import sweep_pahd_r_calibration_reliability as calib  # noqa: E402
import sweep_pahd_r_correlation_shrinkage as shrink  # noqa: E402
import sweep_pahd_r_targeted_dedup_winsorized as targeted  # noqa: E402

N_PERM = 500
N_PERTURB = 300

OUT_PREFIX = "pahd_r_shrinkage_adversarial"

CANDIDATES = {
    "PAHD-R-Core-ShrinkCompact": ("h18_collapsed_seq_evolution_70", "top8"),
    "PAHD-R-Core-ShrinkRegion": ("h18_collapsed_seq_evolution_70", "reliability_top8"),
}


def markdown_table(frame: pd.DataFrame) -> str:
    if frame.empty:
        return "_No rows._"
    text = frame.copy()
    for col in text.columns:
        if pd.api.types.is_float_dtype(text[col]):
            text[col] = text[col].map(lambda x: "" if pd.isna(x) else f"{x:.4f}")
        else:
            text[col] = text[col].astype(str)
    lines = [
        "| " + " | ".join(text.columns) + " |",
        "| " + " | ".join(["---"] * len(text.columns)) + " |",
    ]
    for _, row in text.iterrows():
        lines.append("| " + " | ".join(row[col] for col in text.columns) + " |")
    return "\n".join(lines)


def evaluate_pred(
    pathogen: str,
    df: pd.DataFrame,
    score: np.ndarray,
    pred: np.ndarray,
    y: np.ndarray | None = None,
) -> dict[str, float]:
    y_true = df["layer_a"].astype(int).values if y is None else y.astype(int)
    p20, e20 = pahd.precision_and_enrichment(y_true, score, 20)
    return {
        "mcc_exact": pahd.region_mcc(y_true, pred, 0),
        "mcc_window_10": pahd.region_mcc(y_true, pred, 10),
        "precision_20": p20,
        "enrichment_20": e20,
        "constrained_fpr": pahd.constrained_fpr(pathogen, len(df), pred),
        "coverage_10": pahd.expanded_coverage(pred, 10),
        "pred_frac": float(pred.mean()),
    }


def jaccard(a: np.ndarray, b: np.ndarray) -> float:
    union = np.sum(a | b)
    return float(np.sum(a & b) / union) if union else 1.0


def candidate_prediction(
    data: dict[str, pd.DataFrame],
    pathogens: list[str],
    pathogen: str,
    strategy: str,
) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    score_variant, selector = CANDIDATES[strategy]
    scores = shrink.core_shrinkage_scores(data, pathogens, pathogen)
    score = scores[score_variant]
    ranks = calib.module_ranks(data, pathogens, pathogen)
    reliability = calib.reliability_score("PAHD-R-Core", score, ranks)
    pred = shrink.predict(score, reliability, selector)
    return score, reliability, pred


def run() -> None:
    rng = np.random.default_rng(20260427)
    data = pahd.load_feature_matrices()
    pathogens = targeted.primary_pathogens(data)

    observed_rows = []
    null_rows = []
    decoy_rows = []
    stability_rows = []
    site_rows = []

    for pathogen in pathogens:
        df = data[pathogen]
        y = df["layer_a"].astype(int).values
        for strategy in CANDIDATES:
            score, reliability, pred = candidate_prediction(data, pathogens, pathogen, strategy)
            observed_rows.append({"pathogen": pathogen, "strategy": strategy, **evaluate_pred(pathogen, df, score, pred)})
            for pos in np.where(pred)[0]:
                site_rows.append({
                    "pathogen": pathogen,
                    "strategy": strategy,
                    "position": int(pos),
                    "score": float(score[pos]),
                    "reliability": float(reliability[pos]),
                })

            for perm_id in range(N_PERM):
                y_perm = rng.permutation(y)
                null_rows.append({
                    "pathogen": pathogen,
                    "strategy": strategy,
                    "perm_id": perm_id,
                    **evaluate_pred(pathogen, df, score, pred, y_perm),
                })

            decoys = {
                "shuffle_score": rng.permutation(score),
                "reverse_score": score[::-1],
                "random_uniform": rng.random(len(score)),
            }
            region_seed = np.zeros(len(score))
            for start in rng.choice(np.arange(len(score)), size=min(10, len(score)), replace=False):
                region_seed[max(0, start - 5): min(len(score), start + 6)] += 1.0
            decoys["random_regions"] = region_seed + 0.05 * rng.random(len(score))
            for decoy_name, decoy_score in decoys.items():
                decoy_rel = reliability if decoy_name in {"shuffle_score", "reverse_score"} else rng.random(len(score))
                score_variant, selector = CANDIDATES[strategy]
                decoy_pred = shrink.predict(decoy_score, decoy_rel, selector)
                decoy_rows.append({
                    "pathogen": pathogen,
                    "strategy": strategy,
                    "decoy": decoy_name,
                    **evaluate_pred(pathogen, df, decoy_score, decoy_pred),
                })

            for boot_id in range(N_PERTURB):
                noisy_score = score + rng.normal(0.0, 0.03, size=len(score))
                noisy_rel = np.clip(reliability + rng.normal(0.0, 0.03, size=len(reliability)), 0.0, 1.0)
                score_variant, selector = CANDIDATES[strategy]
                noisy_pred = shrink.predict(noisy_score, noisy_rel, selector)
                stability_rows.append({
                    "pathogen": pathogen,
                    "strategy": strategy,
                    "boot_id": boot_id,
                    "jaccard_to_base": jaccard(pred, noisy_pred),
                    "selection_overlap": float(np.mean(noisy_pred[pred])) if pred.sum() else 0.0,
                    **evaluate_pred(pathogen, df, noisy_score, noisy_pred),
                })

    observed_df = pd.DataFrame(observed_rows)
    null_df = pd.DataFrame(null_rows)
    decoy_df = pd.DataFrame(decoy_rows)
    stability_df = pd.DataFrame(stability_rows)
    site_df = pd.DataFrame(site_rows)

    null_summary_rows = []
    for row in observed_df.itertuples():
        sub = null_df[(null_df["pathogen"] == row.pathogen) & (null_df["strategy"] == row.strategy)]
        null_summary_rows.append({
            "pathogen": row.pathogen,
            "strategy": row.strategy,
            "observed_mcc_exact": row.mcc_exact,
            "observed_mcc_window_10": row.mcc_window_10,
            "observed_precision_20": row.precision_20,
            "null_p_exact_ge_observed": float((sub["mcc_exact"] >= row.mcc_exact).mean()),
            "null_p_window_ge_observed": float((sub["mcc_window_10"] >= row.mcc_window_10).mean()),
            "null_p_precision_ge_observed": float((sub["precision_20"] >= row.precision_20).mean()),
            "null_p95_mcc_exact": float(sub["mcc_exact"].quantile(0.95)),
            "null_p95_mcc_window_10": float(sub["mcc_window_10"].quantile(0.95)),
        })
    null_summary = pd.DataFrame(null_summary_rows)

    global_summary = (
        observed_df.groupby("strategy")
        .agg(
            mean_mcc_exact=("mcc_exact", "mean"),
            mean_mcc_window_10=("mcc_window_10", "mean"),
            mean_precision_20=("precision_20", "mean"),
            mean_constrained_fpr=("constrained_fpr", "mean"),
            mean_coverage_10=("coverage_10", "mean"),
            mean_pred_frac=("pred_frac", "mean"),
        )
        .reset_index()
    )
    stability_global = (
        stability_df.groupby("strategy")
        .agg(
            mean_stability_jaccard=("jaccard_to_base", "mean"),
            p05_stability_jaccard=("jaccard_to_base", lambda s: float(np.quantile(s, 0.05))),
        )
        .reset_index()
    )
    null_counts = (
        null_summary.assign(
            exact_above_null_p95=lambda d: d["observed_mcc_exact"] > d["null_p95_mcc_exact"],
            window_above_null_p95=lambda d: d["observed_mcc_window_10"] > d["null_p95_mcc_window_10"],
        )
        .groupby("strategy")
        .agg(
            pathogens_exact_above_null_p95=("exact_above_null_p95", "sum"),
            pathogens_window_above_null_p95=("window_above_null_p95", "sum"),
        )
        .reset_index()
    )
    global_summary = global_summary.merge(stability_global, on="strategy").merge(null_counts, on="strategy")

    decoy_summary = (
        decoy_df.groupby(["strategy", "decoy"])
        .agg(
            mean_mcc_exact=("mcc_exact", "mean"),
            mean_mcc_window_10=("mcc_window_10", "mean"),
            mean_precision_20=("precision_20", "mean"),
            mean_constrained_fpr=("constrained_fpr", "mean"),
            mean_coverage_10=("coverage_10", "mean"),
        )
        .reset_index()
    )
    stability_summary = (
        stability_df.groupby(["strategy", "pathogen"])
        .agg(
            mean_jaccard=("jaccard_to_base", "mean"),
            p05_jaccard=("jaccard_to_base", lambda s: float(np.quantile(s, 0.05))),
            mean_mcc_exact=("mcc_exact", "mean"),
            mean_mcc_window_10=("mcc_window_10", "mean"),
        )
        .reset_index()
    )

    for name, frame in [
        (f"{OUT_PREFIX}_observed.csv", observed_df),
        (f"{OUT_PREFIX}_null.csv", null_df),
        (f"{OUT_PREFIX}_null_summary.csv", null_summary),
        (f"{OUT_PREFIX}_decoys.csv", decoy_df),
        (f"{OUT_PREFIX}_decoy_summary.csv", decoy_summary),
        (f"{OUT_PREFIX}_stability.csv", stability_df),
        (f"{OUT_PREFIX}_stability_summary.csv", stability_summary),
        (f"{OUT_PREFIX}_site_calls.csv", site_df),
        (f"{OUT_PREFIX}_global_summary.csv", global_summary),
    ]:
        frame.to_csv(RESULTS_DIR / name, index=False)

    report = [
        "# PAHD-R shrinkage candidate adversarial audit",
        "",
        "Date: 2026-04-27 KST",
        "",
        "## Scope",
        "",
        (
            "This audit tests ShrinkCompact and ShrinkRegion against label "
            "permutations, decoy scores, and score/reliability perturbations."
        ),
        "",
        "## Global Summary",
        "",
        markdown_table(global_summary),
        "",
        "## Observed Per Pathogen",
        "",
        markdown_table(observed_df),
        "",
        "## Permutation Null Summary",
        "",
        markdown_table(null_summary),
        "",
        "## Decoy Summary",
        "",
        markdown_table(decoy_summary),
        "",
        "## Stability Summary",
        "",
        markdown_table(stability_summary),
        "",
        "## Interpretation",
        "",
        (
            "Shrinkage candidates are useful only as trade-off review modes if they "
            "lower constrained FPR without failing null and stability checks. "
            "They should not replace Core-Calibrated unless they also improve exact "
            "and window null robustness across pathogens."
        ),
        "",
    ]
    report_path = RESULTS_DIR / f"{OUT_PREFIX}_audit.md"
    report_path.write_text("\n".join(report), encoding="utf-8")
    print(report_path)
    print(global_summary.round(4).to_string(index=False))


if __name__ == "__main__":
    run()
