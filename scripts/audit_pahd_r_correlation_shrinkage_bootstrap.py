#!/usr/bin/env python3
"""Paired bootstrap audit for PAHD-R correlation-shrinkage candidates."""

from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parent.parent
RESULTS_DIR = PROJECT_ROOT / "results" / "mutbench"

IN_RESULTS = RESULTS_DIR / "pahd_r_correlation_shrinkage_results.csv"
OUT_SUMMARY = RESULTS_DIR / "pahd_r_correlation_shrinkage_bootstrap_summary.csv"
OUT_DELTAS = RESULTS_DIR / "pahd_r_correlation_shrinkage_paired_deltas.csv"
OUT_DECISIONS = RESULTS_DIR / "pahd_r_correlation_shrinkage_final_decisions.csv"
OUT_REPORT = RESULTS_DIR / "pahd_r_correlation_shrinkage_bootstrap.md"

METRICS = ["mcc_exact", "mcc_window_10", "precision_20", "constrained_fpr", "coverage_10"]
CANDIDATES = [
    "h18_collapsed_seq_evolution_70:top8",
    "h18_collapsed_seq_evolution_70:reliability_top8",
    "h18_corr_weight_shrink_0.5:reliability_top8",
]
BASELINES = ["PAHD-R-Core", "PAHD-R-Core-Calibrated"]


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


def bootstrap(values: np.ndarray, rng: np.random.Generator, n_boot: int = 20000) -> dict[str, float]:
    values = np.asarray(values, dtype=float)
    idx = rng.integers(0, len(values), size=(n_boot, len(values)))
    boot = values[idx].mean(axis=1)
    return {
        "mean_delta": float(values.mean()),
        "ci_low": float(np.quantile(boot, 0.025)),
        "ci_high": float(np.quantile(boot, 0.975)),
        "p_delta_gt_0": float((boot > 0).mean()),
        "positive_pathogens": int((values > 0).sum()),
        "negative_pathogens": int((values < 0).sum()),
        "zero_pathogens": int((values == 0).sum()),
    }


def metric_decision(row: pd.Series) -> str:
    metric = row["metric"]
    if metric in {"mcc_exact", "mcc_window_10", "precision_20"}:
        if row["mean_delta"] > 0 and row["ci_low"] >= -0.005:
            return "supports_candidate"
        if row["mean_delta"] < -0.01:
            return "risk_loss"
    if metric in {"constrained_fpr", "coverage_10"}:
        if row["mean_delta"] < 0 and row["ci_high"] <= 0.01:
            return "supports_candidate"
        if row["mean_delta"] > 0.01:
            return "risk_inflation"
    return "diagnostic"


def final_decision(row: pd.Series) -> str:
    if row["baseline"] == "PAHD-R-Core":
        if (
            row["mcc_exact"] > 0
            and row["mcc_window_10"] >= 0
            and row["precision_20"] >= 0
            and row["constrained_fpr"] < 0
            and row["coverage_10"] <= 0.005
        ):
            return "candidate_vs_core"
        return "diagnostic_vs_core"
    if (
        row["mcc_exact"] >= -0.003
        and row["mcc_window_10"] >= 0
        and row["precision_20"] >= 0
        and row["constrained_fpr"] < 0
    ):
        return "candidate_tradeoff_vs_calibrated"
    return "diagnostic_vs_calibrated"


def run() -> None:
    rng = np.random.default_rng(20260427)
    results = pd.read_csv(IN_RESULTS)
    rows = []
    deltas = []
    for candidate in CANDIDATES:
        cand = results[results["entry"] == candidate]
        if cand.empty:
            continue
        for baseline in BASELINES:
            base = results[results["entry"] == baseline]
            merged = cand.merge(base, on="pathogen", suffixes=("_candidate", "_baseline"))
            if merged.empty:
                continue
            for _, row in merged.iterrows():
                rec = {
                    "candidate": candidate,
                    "baseline": baseline,
                    "pathogen": row["pathogen"],
                }
                for metric in METRICS:
                    rec[f"delta_{metric}"] = row[f"{metric}_candidate"] - row[f"{metric}_baseline"]
                deltas.append(rec)
            for metric in METRICS:
                values = merged[f"{metric}_candidate"].values - merged[f"{metric}_baseline"].values
                rows.append(
                    {
                        "candidate": candidate,
                        "baseline": baseline,
                        "metric": metric,
                        **bootstrap(values, rng),
                    }
                )

    summary = pd.DataFrame(rows)
    summary["metric_decision"] = summary.apply(metric_decision, axis=1)
    paired = pd.DataFrame(deltas)
    final = (
        summary.pivot_table(
            index=["candidate", "baseline"],
            columns="metric",
            values="mean_delta",
        )
        .reset_index()
        .rename_axis(columns=None)
    )
    final["final_decision"] = final.apply(final_decision, axis=1)

    summary.to_csv(OUT_SUMMARY, index=False)
    paired.to_csv(OUT_DELTAS, index=False)
    final.to_csv(OUT_DECISIONS, index=False)

    report = [
        "# PAHD-R correlation-shrinkage bootstrap audit",
        "",
        "Date: 2026-04-27 KST",
        "",
        "## Final decisions",
        "",
        markdown_table(final),
        "",
        "## Bootstrap summary",
        "",
        markdown_table(summary),
        "",
        "## Per-pathogen paired deltas",
        "",
        markdown_table(paired),
        "",
        "## Interpretation",
        "",
        (
            "`h18_collapsed_seq_evolution_70` is the main candidate if it improves "
            "PAHD-R-Core while lowering constrained FPR. Against PAHD-R-Core-Calibrated, "
            "it should be treated as a trade-off candidate unless it also preserves "
            "the calibrated exact/window gains."
        ),
        "",
    ]
    OUT_REPORT.write_text("\n".join(report), encoding="utf-8")
    print(OUT_REPORT)
    print(final.round(4).to_string(index=False))


if __name__ == "__main__":
    run()
