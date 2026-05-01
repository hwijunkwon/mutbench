#!/usr/bin/env python3
"""Paired bootstrap audit for PAHD-R calibration/reliability candidates."""

from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parent.parent
RESULTS_DIR = PROJECT_ROOT / "results" / "mutbench"
METRICS = ["mcc_exact", "mcc_window_10", "precision_20", "constrained_fpr", "coverage_10"]


def markdown_table(frame: pd.DataFrame) -> str:
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
    }


def decision(row: pd.Series) -> str:
    if row["metric"] == "mcc_exact" and row["mean_delta"] > 0 and row["ci_low"] > -0.005 and row["positive_pathogens"] >= row["negative_pathogens"]:
        return "candidate_exact"
    if row["metric"] == "constrained_fpr" and row["mean_delta"] < 0 and row["ci_high"] <= 0.02:
        return "candidate_fpr"
    if row["metric"] == "coverage_10" and row["mean_delta"] < 0:
        return "candidate_compactness"
    if row["metric"] == "mcc_window_10" and row["mean_delta"] < -0.01:
        return "risk_region_loss"
    return "diagnostic"


def run() -> None:
    rng = np.random.default_rng(20260427)
    results = pd.read_csv(RESULTS_DIR / "pahd_r_calibration_reliability_results.csv")
    candidates = ["reliability_top_8", "decoy_margin_92", "reliability_top_10"]
    rows = []
    paired_rows = []
    for variant in candidates:
        for mode in sorted(results["mode"].unique()):
            if not ((results["variant"] == variant) & (results["mode"] == mode)).any():
                continue
            base = results[(results["variant"] == "baseline") & (results["mode"] == mode)]
            cand = results[(results["variant"] == variant) & (results["mode"] == mode)]
            merged = cand.merge(base, on=["pathogen", "mode"], suffixes=("_candidate", "_baseline"))
            if merged.empty:
                continue
            for metric in METRICS:
                values = merged[f"{metric}_candidate"].values - merged[f"{metric}_baseline"].values
                rows.append({"variant": variant, "mode": mode, "metric": metric, **bootstrap(values, rng)})
            for _, row in merged.iterrows():
                paired_rows.append({
                    "variant": variant,
                    "mode": mode,
                    "pathogen": row["pathogen"],
                    **{f"delta_{metric}": row[f"{metric}_candidate"] - row[f"{metric}_baseline"] for metric in METRICS},
                })
    summary = pd.DataFrame(rows)
    summary["decision"] = summary.apply(decision, axis=1)
    paired = pd.DataFrame(paired_rows)
    final = (
        summary[summary["metric"].isin(["mcc_exact", "mcc_window_10", "constrained_fpr", "coverage_10"])]
        .pivot_table(index=["variant", "mode"], columns="metric", values="mean_delta")
        .reset_index()
    )
    final["final_decision"] = final.apply(
        lambda r: (
            "candidate_review_mode"
            if r.get("mcc_exact", 0) > 0 and r.get("mcc_window_10", 0) >= -0.005 and r.get("constrained_fpr", 1) <= 0.02
            else "diagnostic_only"
        ),
        axis=1,
    )

    summary_path = RESULTS_DIR / "pahd_r_calibration_candidate_bootstrap_summary.csv"
    paired_path = RESULTS_DIR / "pahd_r_calibration_candidate_paired_deltas.csv"
    final_path = RESULTS_DIR / "pahd_r_calibration_candidate_final_decisions.csv"
    report_path = RESULTS_DIR / "pahd_r_calibration_candidate_bootstrap.md"
    summary.to_csv(summary_path, index=False)
    paired.to_csv(paired_path, index=False)
    final.to_csv(final_path, index=False)

    report = [
        "# PAHD-R Calibration Candidate Bootstrap",
        "",
        "Date: 2026-04-27 KST",
        "",
        "## Final Candidate Decisions",
        "",
        markdown_table(final),
        "",
        "## Bootstrap Summary",
        "",
        markdown_table(summary),
        "",
        "## Paired Deltas",
        "",
        markdown_table(paired),
        "",
    ]
    report_path.write_text("\n".join(report), encoding="utf-8")
    print(report_path)
    print(final.round(4).to_string(index=False))


if __name__ == "__main__":
    run()
