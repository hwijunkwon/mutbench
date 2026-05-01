#!/usr/bin/env python3
"""Finalize decision table for PAHD-R-Core-Calibrated candidate."""

from __future__ import annotations

from pathlib import Path

import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parent.parent
RESULTS_DIR = PROJECT_ROOT / "results" / "mutbench"


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


def run() -> None:
    final_modes = pd.read_csv(RESULTS_DIR / "pahd_r_final_reporting_table.csv")
    final_modes = final_modes[final_modes["scope"] == "global"].copy()
    calibrated = pd.read_csv(RESULTS_DIR / "pahd_r_core_calibrated_global_summary.csv").iloc[0]
    wins = pd.read_csv(RESULTS_DIR / "pahd_r_algorithm_improvement_final_decisions.csv")
    temporal = pd.read_csv(RESULTS_DIR / "pahd_r_temporal_candidate_resampling_summary.csv")
    region = pd.read_csv(RESULTS_DIR / "pahd_r_region_first_summary.csv")
    shrinkage_path = RESULTS_DIR / "pahd_r_shrinkage_adversarial_global_summary.csv"
    shrinkage = pd.read_csv(shrinkage_path) if shrinkage_path.exists() else pd.DataFrame()
    selective_path = RESULTS_DIR / "pahd_r_selective_callability_summary.csv"
    selective = pd.read_csv(selective_path) if selective_path.exists() else pd.DataFrame()

    rows = []
    for row in final_modes.itertuples():
        rows.append({
            "entry": row.entry,
            "type": "current_default",
            "exact_mcc": row.exact_mcc,
            "mcc_window_10": row.mcc_window_10,
            "precision_20": row.precision_20,
            "constrained_fpr": row.constrained_fpr,
            "coverage_10": row.coverage_10,
            "decision": "keep_default",
            "reason": row.status,
        })
    rows.append({
        "entry": "PAHD-R-Core-Calibrated",
        "type": "new_candidate",
        "exact_mcc": calibrated["mean_mcc_exact"],
        "mcc_window_10": calibrated["mean_mcc_window_10"],
        "precision_20": calibrated["mean_precision_20"],
        "constrained_fpr": calibrated["mean_constrained_fpr"],
        "coverage_10": calibrated["mean_coverage_10"],
        "decision": "candidate_not_default",
        "reason": "Improves Core exact/region/FPR/coverage, but per-pathogen null weaknesses remain.",
    })
    wins_row = wins[wins["candidate"] == "winsorized_1_99"].iloc[0]
    rows.append({
        "entry": "winsorized_1_99",
        "type": "preprocessing_candidate",
        "exact_mcc": None,
        "mcc_window_10": wins_row["best_mean_delta_mcc_window_10"],
        "precision_20": None,
        "constrained_fpr": None,
        "coverage_10": None,
        "decision": wins_row["final_decision"],
        "reason": wins_row["reason"],
    })
    best_temporal = temporal.sort_values("mean_delta_mcc_window_10", ascending=False).iloc[0]
    rows.append({
        "entry": f"temporal_resampling:{best_temporal['scheme']}/{best_temporal['mode']}",
        "type": "temporal_candidate",
        "exact_mcc": best_temporal["mean_delta_mcc_exact"],
        "mcc_window_10": best_temporal["mean_delta_mcc_window_10"],
        "precision_20": best_temporal["mean_delta_precision_20"],
        "constrained_fpr": best_temporal["mean_delta_constrained_fpr"],
        "coverage_10": None,
        "decision": best_temporal["decision"],
        "reason": "Temporal candidate fails resampling/strict-bin robustness.",
    })
    best_region = region[region["variant"] != "baseline"].sort_values("mean_mcc_exact", ascending=False).iloc[0]
    rows.append({
        "entry": f"region_first:{best_region['variant']}/{best_region['mode']}",
        "type": "region_first_candidate",
        "exact_mcc": best_region["mean_mcc_exact"],
        "mcc_window_10": best_region["mean_mcc_window_10"],
        "precision_20": best_region["mean_precision_20"],
        "constrained_fpr": best_region["mean_constrained_fpr"],
        "coverage_10": best_region["mean_coverage_10"],
        "decision": best_region["decision"],
        "reason": "Region-first NMS failed to improve exact/top-k and often inflated coverage.",
    })
    if not shrinkage.empty:
        for row in shrinkage.itertuples():
            if row.strategy == "PAHD-R-Core-ShrinkCompact":
                decision = "candidate_tradeoff"
                reason = (
                    "Lower FPR/coverage than Core and Core-Calibrated, but window null support "
                    "is weaker and it does not replace Core-Calibrated."
                )
            else:
                decision = "candidate_tradeoff"
                reason = (
                    "Best shrinkage regional trade-off with lower FPR, but decoy/window-null "
                    "weaknesses require candidate-only reporting."
                )
            rows.append({
                "entry": row.strategy,
                "type": "shrinkage_candidate",
                "exact_mcc": row.mean_mcc_exact,
                "mcc_window_10": row.mean_mcc_window_10,
                "precision_20": row.mean_precision_20,
                "constrained_fpr": row.mean_constrained_fpr,
                "coverage_10": row.mean_coverage_10,
                "decision": decision,
                "reason": reason,
            })
    if not selective.empty:
        selective_candidates = selective[
            (selective["policy"] == "callable_only")
            & (selective["decision"] == "selective_candidate")
        ]
        for row in selective_candidates.itertuples():
            rows.append({
                "entry": f"Selective:{row.candidate}/callable_only",
                "type": "selective_reporting_candidate",
                "exact_mcc": row.mean_mcc_exact,
                "mcc_window_10": row.mean_mcc_window_10,
                "precision_20": row.mean_precision_20,
                "constrained_fpr": row.mean_constrained_fpr,
                "coverage_10": row.mean_coverage_10,
                "decision": "selective_candidate_not_default",
                "reason": (
                    f"Accepted {row.n_pathogens}/9 pathogens and demoted {row.n_abstained}/9; "
                    "use only as reject-option reporting with abstention counts."
                ),
            })

    decisions = pd.DataFrame(rows)
    csv_path = RESULTS_DIR / "pahd_r_calibrated_core_final_decision_table.csv"
    report_path = RESULTS_DIR / "pahd_r_calibrated_core_final_decision.md"
    decisions.to_csv(csv_path, index=False)
    report = [
        "# PAHD-R Calibrated Core Final Decision",
        "",
        "Date: 2026-04-27 KST",
        "",
        "## Decision Table",
        "",
        markdown_table(decisions),
        "",
        "## Verdict",
        "",
        (
            "PAHD-R-Core-Calibrated is the best new candidate from the latest "
            "improvement round, but it should not replace the current default modes. "
            "Shrinkage candidates add useful low-FPR trade-offs but should also remain "
            "candidate-only because decoy/window-null weaknesses remain. Selective "
            "callability candidates provide a stronger conservative reporting layer, "
            "but they are not all-pathogen defaults because they abstain/demote weak "
            "pathogens. These modes can be retained pending stronger per-pathogen null "
            "and external validation."
        ),
        "",
    ]
    report_path.write_text("\n".join(report), encoding="utf-8")
    print(report_path)
    print(decisions.to_string(index=False))


if __name__ == "__main__":
    run()
