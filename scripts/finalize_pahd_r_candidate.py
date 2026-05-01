#!/usr/bin/env python3
"""Finalize PAHD-R candidate comparison from experiment outputs."""

from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parent.parent
RESULTS_DIR = PROJECT_ROOT / "results" / "mutbench"


BASELINE = "compactness_gated_rank_fusion"
REFINEMENT = "h11_soft_constraint_post"


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


def compare_candidates(results: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
    keep = results[results["strategy"].isin([BASELINE, REFINEMENT])].copy()
    metrics = [
        "mcc_exact",
        "mcc_window_5",
        "mcc_window_10",
        "precision_20",
        "precision_50",
        "constrained_fpr",
        "region_coverage_10",
        "auroc",
    ]
    wide = keep.pivot(index="pathogen", columns="strategy", values=metrics)
    rows = []
    for pathogen in sorted(keep["pathogen"].unique()):
        row = {"pathogen": pathogen}
        for metric in metrics:
            base = float(wide.loc[pathogen, (metric, BASELINE)])
            ref = float(wide.loc[pathogen, (metric, REFINEMENT)])
            row[f"h11_{metric}"] = base
            row[f"h17_{metric}"] = ref
            row[f"delta_{metric}"] = ref - base
        rows.append(row)
    per_pathogen = pd.DataFrame(rows)

    summary_rows = []
    for strategy in [BASELINE, REFINEMENT]:
        sub = keep[keep["strategy"] == strategy]
        summary_rows.append({
            "strategy": strategy,
            "mean_mcc_exact": float(sub["mcc_exact"].mean()),
            "mean_mcc_window_10": float(sub["mcc_window_10"].mean()),
            "mean_precision_20": float(sub["precision_20"].mean()),
            "mean_constrained_fpr": float(sub["constrained_fpr"].mean()),
            "mean_region_coverage_10": float(sub["region_coverage_10"].mean()),
            "mean_auroc": float(sub["auroc"].mean()),
            "positive_pathogens": int((sub["mcc_exact"] > 0).sum()),
            "n_pathogens": int(sub["pathogen"].nunique()),
        })
    summary = pd.DataFrame(summary_rows)
    delta = {
        "strategy": "delta_h17_minus_h11",
        "mean_mcc_exact": summary.iloc[1]["mean_mcc_exact"] - summary.iloc[0]["mean_mcc_exact"],
        "mean_mcc_window_10": summary.iloc[1]["mean_mcc_window_10"] - summary.iloc[0]["mean_mcc_window_10"],
        "mean_precision_20": summary.iloc[1]["mean_precision_20"] - summary.iloc[0]["mean_precision_20"],
        "mean_constrained_fpr": summary.iloc[1]["mean_constrained_fpr"] - summary.iloc[0]["mean_constrained_fpr"],
        "mean_region_coverage_10": summary.iloc[1]["mean_region_coverage_10"] - summary.iloc[0]["mean_region_coverage_10"],
        "mean_auroc": summary.iloc[1]["mean_auroc"] - summary.iloc[0]["mean_auroc"],
        "positive_pathogens": summary.iloc[1]["positive_pathogens"] - summary.iloc[0]["positive_pathogens"],
        "n_pathogens": summary.iloc[1]["n_pathogens"],
    }
    summary = pd.concat([summary, pd.DataFrame([delta])], ignore_index=True)
    return summary, per_pathogen


def weak_pathogen_analysis(per_pathogen: pd.DataFrame, audit: pd.DataFrame) -> pd.DataFrame:
    if "strategy" in audit.columns:
        audit = audit[audit["strategy"] == BASELINE].copy()
    merged = per_pathogen.merge(audit[["pathogen", "null_p95_mcc", "exceeds_null_p95"]], on="pathogen", how="left")
    rows = []
    for _, row in merged.iterrows():
        weak_reasons = []
        if not bool(row["exceeds_null_p95"]):
            weak_reasons.append("does_not_exceed_permutation_p95")
        if row["h11_precision_20"] <= 0.0:
            weak_reasons.append("zero_precision20")
        if row["h11_mcc_exact"] <= 0.0:
            weak_reasons.append("nonpositive_exact_mcc")
        if row["h11_mcc_exact"] < row["null_p95_mcc"]:
            weak_reasons.append("below_null_p95")
        rows.append({
            "pathogen": row["pathogen"],
            "h11_exact_mcc": row["h11_mcc_exact"],
            "h17_exact_mcc": row["h17_mcc_exact"],
            "h11_precision20": row["h11_precision_20"],
            "h17_precision20": row["h17_precision_20"],
            "exceeds_null_p95": bool(row["exceeds_null_p95"]),
            "weak_case": bool(weak_reasons),
            "weak_reasons": ";".join(weak_reasons),
        })
    return pd.DataFrame(rows)


def run() -> None:
    results = pd.read_csv(RESULTS_DIR / "pahd_r_multi_hypothesis_results.csv")
    audit = pd.read_csv(RESULTS_DIR / "pahd_r_adversarial_null_summary.csv")

    summary, per_pathogen = compare_candidates(results)
    weak = weak_pathogen_analysis(per_pathogen, audit)

    summary.to_csv(RESULTS_DIR / "pahd_r_final_candidate_summary.csv", index=False)
    per_pathogen.to_csv(RESULTS_DIR / "pahd_r_final_candidate_per_pathogen.csv", index=False)
    weak.to_csv(RESULTS_DIR / "pahd_r_weak_pathogen_error_analysis.csv", index=False)

    delta = summary[summary["strategy"] == "delta_h17_minus_h11"].iloc[0]
    if (
        delta["mean_mcc_exact"] >= -1e-12
        and delta["mean_precision_20"] >= -1e-12
        and delta["mean_constrained_fpr"] <= 1e-12
        and delta["mean_mcc_window_10"] > 0
    ):
        decision = "Adopt h11_soft_constraint_post as PAHD-R v0.3.1."
    else:
        decision = "Keep compactness_gated_rank_fusion as PAHD-R v0.3."

    report = [
        "# PAHD-R Final Candidate Comparison",
        "",
        "Date: 2026-04-26 KST",
        "",
        "## Decision",
        "",
        decision,
        "",
        "The refinement is accepted only if it preserves exact MCC, Precision@20, "
        "and constrained FPR while improving region-level MCC.",
        "",
        "## Candidate Summary",
        "",
        markdown_table(summary),
        "",
        "## Per-Pathogen Deltas",
        "",
        markdown_table(per_pathogen[[
            "pathogen",
            "delta_mcc_exact",
            "delta_mcc_window_10",
            "delta_precision_20",
            "delta_constrained_fpr",
            "delta_region_coverage_10",
            "delta_auroc",
        ]]),
        "",
        "## Weak Pathogen Analysis",
        "",
        markdown_table(weak),
        "",
        "## Interpretation",
        "",
        (
            "The final candidate is a conservative postprocessing refinement, "
            "not a new model family. Weak pathogens remain weak after the "
            "refinement and should be discussed as limits rather than hidden "
            "inside the mean score."
        ),
        "",
    ]
    report_path = RESULTS_DIR / "pahd_r_final_candidate_comparison.md"
    report_path.write_text("\n".join(report), encoding="utf-8")
    print(report_path)
    print(decision)


if __name__ == "__main__":
    run()
