#!/usr/bin/env python3
"""Build thesis-facing final PAHD-R reporting table."""

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
    modes = pd.read_csv(RESULTS_DIR / "pahd_r_final_mode_table.csv")
    repaired = pd.read_csv(RESULTS_DIR / "pahd_r_repaired_prior_candidate_decisions.csv")
    sars2 = pd.read_csv(RESULTS_DIR / "pahd_r_sars2_region_split_prior_decisions.csv")
    sars2_neighborhood_path = RESULTS_DIR / "pahd_r_sars2_epitope_neighborhood_validation_decision.csv"
    sars2_neighborhood = (
        pd.read_csv(sars2_neighborhood_path)
        if sars2_neighborhood_path.exists()
        else pd.DataFrame()
    )
    sars2_dms_path = RESULTS_DIR / "pahd_r_sars2_external_dms_validation_decision.csv"
    sars2_dms = pd.read_csv(sars2_dms_path) if sars2_dms_path.exists() else pd.DataFrame()
    mers_path = RESULTS_DIR / "pahd_r_mers_rsv_narrow_prior_decisions.csv"
    mers_rsv = pd.read_csv(mers_path) if mers_path.exists() else pd.DataFrame()
    algorithm_decision_path = RESULTS_DIR / "pahd_r_calibrated_core_final_decision_table.csv"
    algorithm_decisions = (
        pd.read_csv(algorithm_decision_path)
        if algorithm_decision_path.exists()
        else pd.DataFrame()
    )
    hybrid_path = RESULTS_DIR / "pahd_r_virus_aware_hybrid_summary.csv"
    hybrid_summary = pd.read_csv(hybrid_path) if hybrid_path.exists() else pd.DataFrame()

    base_rows = []
    for _, row in modes.iterrows():
        base_rows.append({
            "entry": row["mode"],
            "scope": "global",
            "status": "adopted",
            "exact_mcc": row["exact_mcc"],
            "mcc_window_10": row["mcc_window_10"],
            "precision_20": row["precision_20"],
            "constrained_fpr": row["constrained_fpr"],
            "coverage_10": row["coverage_10"],
            "audit_status": f"permutation {row['permutation_status']}; decoy margin exact {row['decoy_exact_margin']:.4f}",
            "recommended_use": row["recommended_use"],
            "caveat": "Report with exact MCC, Precision@20, constrained FPR, and coverage.",
        })

    if len(algorithm_decisions):
        candidate_rows = algorithm_decisions[
            algorithm_decisions["entry"].isin([
                "PAHD-R-Core-Calibrated",
                "PAHD-R-Core-ShrinkCompact",
                "PAHD-R-Core-ShrinkRegion",
            ])
        ]
        for _, row in candidate_rows.iterrows():
            base_rows.append({
                "entry": row["entry"],
                "scope": "global",
                "status": "candidate, not adopted",
                "exact_mcc": row["exact_mcc"],
                "mcc_window_10": row["mcc_window_10"],
                "precision_20": row["precision_20"],
                "constrained_fpr": row["constrained_fpr"],
                "coverage_10": row["coverage_10"],
                "audit_status": row["decision"],
                "recommended_use": "global algorithm candidate for future validation",
                "caveat": row["reason"],
            })

    if len(hybrid_summary):
        hybrid = hybrid_summary[
            hybrid_summary["entry"] == "core90_component_evo_access10:reliability_top8"
        ]
        if len(hybrid):
            row = hybrid.iloc[0]
            base_rows.append({
                "entry": "PAHD-R-Core90-ComponentEvoAccess10-Calibrated",
                "scope": "global",
                "status": "candidate, not adopted",
                "exact_mcc": row["mean_mcc_exact"],
                "mcc_window_10": row["mean_mcc_window_10"],
                "precision_20": row["mean_precision_20"],
                "constrained_fpr": row["mean_constrained_fpr"],
                "coverage_10": row["mean_coverage_10"],
                "audit_status": row["decision"],
                "recommended_use": "virus-aware auxiliary-fusion candidate",
                "caveat": (
                    "Improves Core but does not beat Core-Calibrated; retain as "
                    "candidate-only pending null, stability, and external validation."
                ),
            })

    hcv = repaired[
        (repaired["pathogen"] == "HCV")
        & (repaired["variant"] == "domain_prior")
        & (repaired["adoption_decision"] == "adoptable")
    ]
    for _, row in hcv.iterrows():
        base_rows.append({
            "entry": f"HCV repair + {row['mode']}",
            "scope": "HCV only",
            "status": "adopted optional repair",
            "exact_mcc": row["mcc_exact"],
            "mcc_window_10": row["mcc_window_10"],
            "precision_20": row["precision_20"],
            "constrained_fpr": row["constrained_fpr"],
            "coverage_10": row["coverage_10"],
            "audit_status": (
                f"permutation p={row['empirical_p_null_ge_observed']:.4f}; "
                f"beats {row['best_control_variant']} control"
            ),
            "recommended_use": "optional HCV E2 repair layer",
            "caveat": "Do not generalize this repair to other pathogens.",
        })

    sars_candidates = sars2[sars2["adoption_decision"] == "candidate"].copy()
    if len(sars_candidates):
        best_sars = (
            sars_candidates.sort_values(
                ["mode", "delta_mcc_exact", "delta_precision_20", "coverage_10"],
                ascending=[True, False, False, True],
            )
            .groupby("mode")
            .head(1)
        )
        for _, row in best_sars.iterrows():
            status = "manual-review supported candidate"
            caveat = "Requires predeclared epitope-neighborhood validation before adoption."
            if len(sars2_neighborhood):
                decision = sars2_neighborhood.iloc[0]
                if decision["adoption_decision"] == "neighborhood_validated_candidate":
                    status = "neighborhood-validated candidate"
                    caveat = (
                        "Validated for predeclared RBD neighborhoods; not an exact-site adopted repair."
                    )
            if len(sars2_dms):
                dms_decision = sars2_dms.iloc[0]
                if dms_decision["external_dms_decision"] == "external_dms_hold":
                    caveat += " Local DMS Layer C validation is on hold."
            base_rows.append({
                "entry": f"SARS-CoV-2 {row['region']} repair + {row['mode']}",
                "scope": "SARS-CoV-2 only",
                "status": status,
                "exact_mcc": row["mcc_exact"],
                "mcc_window_10": row["mcc_window_10"],
                "precision_20": row["precision_20"],
                "constrained_fpr": row["constrained_fpr"],
                "coverage_10": row["coverage_10"],
                "audit_status": (
                    f"permutation p={row['empirical_p_null_ge_observed']:.4f}; "
                    f"beats {row['best_control']} control"
                ),
                "recommended_use": "candidate conservative SARS-CoV-2 review repair",
                "caveat": caveat,
            })

    if len(mers_rsv):
        mers_candidates = mers_rsv[
            (mers_rsv["pathogen"] == "MERS")
            & (mers_rsv["adoption_decision"] == "candidate")
        ].copy()
        if len(mers_candidates):
            best_mers = (
                mers_candidates.sort_values(
                    ["delta_mcc_exact", "delta_precision_20", "precision_20"],
                    ascending=[False, False, False],
                )
                .head(2)
            )
            for _, row in best_mers.iterrows():
                base_rows.append({
                    "entry": f"MERS {row['prior']} repair + {row['mode']}",
                    "scope": "MERS only",
                    "status": "candidate, not adopted",
                    "exact_mcc": row["mcc_exact"],
                    "mcc_window_10": None,
                    "precision_20": row["precision_20"],
                    "constrained_fpr": row["constrained_fpr"],
                    "coverage_10": row["coverage_10"],
                    "audit_status": (
                        f"permutation p={row['empirical_p_null_ge_observed']:.4f}; "
                        f"beats {row['best_control']} control"
                    ),
                    "recommended_use": "candidate MERS DPP4/contact repair",
                    "caveat": "Sparse-label candidate; requires manual structural/coordinate review.",
                })

    table = pd.DataFrame(base_rows)
    table.to_csv(RESULTS_DIR / "pahd_r_final_reporting_table.csv", index=False)

    report = [
        "# PAHD-R Final Reporting Table",
        "",
        "Date: 2026-04-27 KST",
        "",
        markdown_table(table),
        "",
        "## Reporting Rules",
        "",
        "- Do not report MCC +/-10 alone.",
        "- Always pair region metrics with exact MCC, Precision@20, constrained FPR, and coverage.",
        "- Present Core/Augmented/Review as global shared PAHD-R modes.",
        "- Present calibrated, shrinkage, and virus-aware hybrid entries as global candidates only.",
        "- Present HCV repair as an optional pathogen-specific repair layer.",
        "- Present SARS-CoV-2 split-prior repair as a neighborhood-validated candidate only, not as a finalized exact-site global method.",
        "- Present MERS narrow DPP4 repair as a candidate only.",
        "- RSV remains an unrepaired weak case.",
        "",
    ]
    out = RESULTS_DIR / "pahd_r_final_reporting_table.md"
    out.write_text("\n".join(report), encoding="utf-8")
    print(out)
    print(table.round(4).to_string(index=False))


if __name__ == "__main__":
    run()
