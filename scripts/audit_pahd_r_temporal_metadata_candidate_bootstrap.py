#!/usr/bin/env python3
"""Bootstrap audit for staged temporal-metadata PAHD-R candidates."""

from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parent.parent
RESULTS_DIR = PROJECT_ROOT / "results" / "mutbench"
MODES = ["PAHD-R-Core", "PAHD-R-Augmented", "PAHD-R-Review"]
VARIANTS = [
    "time_meta_alpha_25_winsorized",
    "time_meta_alpha_50_winsorized",
    "time_meta_y10_alpha_25_winsorized",
    "time_meta_y10_alpha_50_winsorized",
    "time_meta_alpha_25",
    "time_meta_alpha_50",
    "time_meta_alpha_100",
    "time_meta_y10_alpha_25",
    "time_meta_y10_alpha_50",
]
METRICS = ["mcc_exact", "mcc_window_10", "precision_20", "constrained_fpr"]


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
        "paired_positive": int((values > 0).sum()),
        "paired_negative": int((values < 0).sum()),
    }


def decision(row: pd.Series) -> str:
    if row["metric"] != "mcc_window_10":
        return "diagnostic"
    if row["mean_delta"] >= 0.015 and row["ci_low"] > 0.0 and row["paired_positive"] >= 6:
        return "strong_candidate"
    if row["mean_delta"] >= 0.015 and row["p_delta_gt_0"] >= 0.75:
        return "candidate_needs_more_validation"
    if row["mean_delta"] <= -0.050:
        return "reject"
    return "diagnostic"


def run() -> None:
    rng = np.random.default_rng(20260427)
    results = pd.read_csv(RESULTS_DIR / "pahd_r_temporal_metadata_control_results.csv")
    rows = []
    paired_rows = []
    for variant in VARIANTS:
        for mode in MODES:
            base = results[(results["variant"] == "baseline") & (results["mode"] == mode)]
            cand = results[(results["variant"] == variant) & (results["mode"] == mode)]
            merged = cand.merge(base, on=["pathogen", "mode"], suffixes=("_candidate", "_baseline"))
            for metric in METRICS:
                values = merged[f"{metric}_candidate"].values - merged[f"{metric}_baseline"].values
                row = {"variant": variant, "mode": mode, "metric": metric, **bootstrap(values, rng)}
                rows.append(row)
            for _, item in merged.iterrows():
                paired_rows.append({
                    "variant": variant,
                    "mode": mode,
                    "pathogen": item["pathogen"],
                    **{
                        f"delta_{metric}": item[f"{metric}_candidate"] - item[f"{metric}_baseline"]
                        for metric in METRICS
                    },
                })
    summary = pd.DataFrame(rows)
    summary["decision"] = summary.apply(decision, axis=1)
    paired = pd.DataFrame(paired_rows)

    top = summary[summary["metric"] == "mcc_window_10"].sort_values(["mean_delta", "p_delta_gt_0"], ascending=False)
    summary_path = RESULTS_DIR / "pahd_r_temporal_metadata_candidate_bootstrap_summary.csv"
    paired_path = RESULTS_DIR / "pahd_r_temporal_metadata_candidate_paired_deltas.csv"
    report_path = RESULTS_DIR / "pahd_r_temporal_metadata_candidate_bootstrap.md"
    summary.to_csv(summary_path, index=False)
    paired.to_csv(paired_path, index=False)

    report = [
        "# PAHD-R Temporal Metadata Candidate Bootstrap",
        "",
        "Date: 2026-04-27 KST",
        "",
        "## Scope",
        "",
        (
            "This audit checks staged temporal-metadata candidates with paired "
            "pathogen bootstrap. It is exploratory follow-up evidence only."
        ),
        "",
        "## Region MCC Candidates",
        "",
        markdown_table(top),
        "",
        "## Full Bootstrap Summary",
        "",
        markdown_table(summary),
        "",
        "## Interpretation",
        "",
        (
            "Temporal metadata enables a more meaningful follow-up experiment than "
            "header-only time stratification. Candidates still need external and "
            "out-of-sample validation before thesis adoption."
        ),
        "",
    ]
    report_path.write_text("\n".join(report), encoding="utf-8")
    print(report_path)
    print(top.round(4).head(10).to_string(index=False))


if __name__ == "__main__":
    run()
