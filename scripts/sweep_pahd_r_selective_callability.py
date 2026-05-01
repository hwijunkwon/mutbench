#!/usr/bin/env python3
"""Selective/callability policy experiment for PAHD-R candidates.

The policy has two layers:

1. Pre-metric callability: uses only data/feature quality diagnostics available
   before scoring a candidate's benchmark outcome.
2. Post-audit governance: summarizes null/stability weaknesses but is not used
   to compute selective performance claims.
"""

from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parent.parent
RESULTS_DIR = PROJECT_ROOT / "results" / "mutbench"

OUT_FEATURES = RESULTS_DIR / "pahd_r_selective_callability_features.csv"
OUT_POLICY = RESULTS_DIR / "pahd_r_selective_callability_policy.csv"
OUT_RESULTS = RESULTS_DIR / "pahd_r_selective_callability_results.csv"
OUT_SUMMARY = RESULTS_DIR / "pahd_r_selective_callability_summary.csv"
OUT_REPORT = RESULTS_DIR / "pahd_r_selective_callability_sweep.md"

METRICS = ["mcc_exact", "mcc_window_10", "precision_20", "constrained_fpr", "coverage_10"]


def read_csv(path: str) -> pd.DataFrame:
    return pd.read_csv(RESULTS_DIR / path)


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


def load_callability_features() -> pd.DataFrame:
    feature = read_csv("pahd_r_data_processing_pathogen_summary.csv")
    raw = read_csv("pahd_r_raw_sequence_stability_summary.csv")
    dedup = read_csv("pahd_r_dedup_sequence_sensitivity_summary.csv")
    null = read_csv("pahd_r_core_calibrated_null_summary.csv")
    stability = read_csv("pahd_r_core_calibrated_stability.csv")
    stability_summary = (
        stability.groupby("pathogen")
        .agg(
            calibrated_mean_jaccard=("jaccard_to_base", "mean"),
            calibrated_p05_jaccard=("jaccard_to_base", lambda s: float(np.quantile(s, 0.05))),
        )
        .reset_index()
    )
    merged = (
        feature.merge(
            raw[
                [
                    "pathogen",
                    "duplicate_rate",
                    "p05_top_jaccard",
                    "raw_sequence_stability_status",
                ]
            ],
            on="pathogen",
            how="left",
        )
        .merge(
            dedup[
                [
                    "pathogen",
                    "original_vs_dedup_top_jaccard",
                    "dedup_boot_p05_jaccard",
                    "dedup_decision",
                ]
            ],
            on="pathogen",
            how="left",
        )
        .merge(
            null[
                [
                    "pathogen",
                    "null_p_exact_ge_observed",
                    "null_p_window_ge_observed",
                    "null_p_precision_ge_observed",
                ]
            ],
            on="pathogen",
            how="left",
        )
        .merge(stability_summary, on="pathogen", how="left")
    )
    return merged


def pre_metric_policy(row: pd.Series) -> tuple[str, str, float]:
    reasons = []
    score = 1.0

    if row["n_layer_a"] < 10 or row["prevalence"] < 0.01:
        reasons.append("label_sparse")
        score -= 0.45
    elif row["n_layer_a"] < 15 or row["prevalence"] < 0.02:
        reasons.append("label_low")
        score -= 0.18

    if row["max_feature_auc"] < 0.58:
        reasons.append("feature_signal_weak")
        score -= 0.35
    elif row["max_feature_auc"] < 0.62:
        reasons.append("feature_signal_borderline")
        score -= 0.20

    if row["n_inverted_features"] >= 5:
        reasons.append("feature_direction_unstable")
        score -= 0.40
    elif row["n_inverted_features"] >= 2:
        reasons.append("feature_direction_mixed")
        score -= 0.15

    if row["p05_top_jaccard"] < 0.60:
        reasons.append("raw_top_sites_unstable")
        score -= 0.35
    elif row["p05_top_jaccard"] < 0.70:
        reasons.append("raw_top_sites_borderline")
        score -= 0.12

    if row["original_vs_dedup_top_jaccard"] < 0.70:
        reasons.append("dedup_changes_top_sites")
        score -= 0.20
    elif row["original_vs_dedup_top_jaccard"] < 0.80:
        reasons.append("dedup_borderline")
        score -= 0.08

    if row["duplicate_rate"] > 0.75:
        reasons.append("high_duplicate_rate")
        score -= 0.10

    if score >= 0.72:
        cls = "callable"
    elif score >= 0.45:
        cls = "review_only"
    else:
        cls = "diagnostic_only"
    return cls, ";".join(reasons) if reasons else "no_major_pre_metric_risk", float(max(0.0, score))


def governance_flags(row: pd.Series) -> str:
    flags = []
    if row["null_p_exact_ge_observed"] > 0.10:
        flags.append("exact_null_weak")
    if row["null_p_window_ge_observed"] > 0.10:
        flags.append("window_null_weak")
    if row["null_p_precision_ge_observed"] > 0.10:
        flags.append("precision_null_weak")
    if row["calibrated_p05_jaccard"] < 0.70:
        flags.append("stability_borderline")
    return ";".join(flags) if flags else "post_audit_ok"


def build_policy(features: pd.DataFrame) -> pd.DataFrame:
    rows = []
    for row in features.itertuples(index=False):
        s = pd.Series(row._asdict())
        cls, reasons, score = pre_metric_policy(s)
        rows.append(
            {
                "pathogen": s["pathogen"],
                "pre_metric_callability": cls,
                "callability_score": score,
                "pre_metric_reasons": reasons,
                "post_audit_governance_flags": governance_flags(s),
            }
        )
    return pd.DataFrame(rows)


def load_candidate_observed() -> pd.DataFrame:
    core_cal = read_csv("pahd_r_core_calibrated_observed.csv")
    core_cal = core_cal.rename(columns={"strategy": "candidate"})
    shrink_path = RESULTS_DIR / "pahd_r_shrinkage_adversarial_observed.csv"
    frames = [core_cal]
    if shrink_path.exists():
        shrink = pd.read_csv(shrink_path).rename(columns={"strategy": "candidate"})
        frames.append(shrink)
    out = pd.concat(frames, ignore_index=True)
    return out


def aggregate_metrics(frame: pd.DataFrame) -> dict[str, float]:
    out = {f"mean_{metric}": float(frame[metric].mean()) if len(frame) else np.nan for metric in METRICS}
    out["n_pathogens"] = int(frame["pathogen"].nunique()) if len(frame) else 0
    return out


def evaluate_selective(observed: pd.DataFrame, policy: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
    merged = observed.merge(policy, on="pathogen", how="left")
    rows = []
    summary_rows = []
    for candidate, group in merged.groupby("candidate"):
        all_metrics = aggregate_metrics(group)
        summary_rows.append(
            {
                "candidate": candidate,
                "policy": "all_pathogens",
                "accepted_classes": "callable,review_only,diagnostic_only",
                "n_abstained": 0,
                **all_metrics,
            }
        )
        for policy_name, classes in [
            ("callable_only", ["callable"]),
            ("callable_plus_review", ["callable", "review_only"]),
        ]:
            accepted = group[group["pre_metric_callability"].isin(classes)]
            abstained = group[~group["pre_metric_callability"].isin(classes)]
            summary_rows.append(
                {
                    "candidate": candidate,
                    "policy": policy_name,
                    "accepted_classes": ",".join(classes),
                    "n_abstained": int(abstained["pathogen"].nunique()),
                    **aggregate_metrics(accepted),
                }
            )
        for row in group.itertuples(index=False):
            rows.append(row._asdict())
    return pd.DataFrame(rows), pd.DataFrame(summary_rows)


def decision(row: pd.Series) -> str:
    if row["policy"] == "all_pathogens":
        return "reference"
    if row["n_pathogens"] < 4:
        return "too_selective_for_primary_claim"
    if (
        row["mean_mcc_exact"] >= 0.20
        and row["mean_precision_20"] >= 0.20
        and row["mean_constrained_fpr"] <= 0.10
    ):
        return "selective_candidate"
    return "diagnostic_policy"


def run() -> None:
    features = load_callability_features()
    policy = build_policy(features)
    observed = load_candidate_observed()
    results, summary = evaluate_selective(observed, policy)
    summary["decision"] = summary.apply(decision, axis=1)

    features.to_csv(OUT_FEATURES, index=False)
    policy.to_csv(OUT_POLICY, index=False)
    results.to_csv(OUT_RESULTS, index=False)
    summary.to_csv(OUT_SUMMARY, index=False)

    policy_counts = (
        policy.groupby("pre_metric_callability")
        .agg(n_pathogens=("pathogen", "count"), pathogens=("pathogen", lambda s: ", ".join(sorted(s))))
        .reset_index()
    )
    report = [
        "# PAHD-R selective/callability experiment",
        "",
        "Date: 2026-04-27 KST",
        "",
        "## Scope",
        "",
        (
            "This experiment tests whether PAHD-R should abstain or demote "
            "pathogens before making equal-strength performance claims. The "
            "pre-metric policy uses label sparsity, feature diagnostics, and "
            "raw/dedup stability. Null/stability outcomes are reported separately "
            "as governance checks and are not used to define the selective policy."
        ),
        "",
        "## Pre-metric callability policy",
        "",
        markdown_table(policy.sort_values(["pre_metric_callability", "pathogen"])),
        "",
        "## Callability counts",
        "",
        markdown_table(policy_counts),
        "",
        "## Selective performance summary",
        "",
        markdown_table(summary.sort_values(["candidate", "policy"])),
        "",
        "## Interpretation",
        "",
        (
            "Callable-only performance should be interpreted as a selective/reject-option "
            "mode, not as the primary all-pathogen benchmark. A useful selective policy "
            "must improve accepted-set metrics while transparently reporting abstained "
            "pathogens and the pre-metric reasons for demotion."
        ),
        "",
    ]
    OUT_REPORT.write_text("\n".join(report), encoding="utf-8")
    print(OUT_REPORT)
    print(policy.sort_values(["pre_metric_callability", "pathogen"]).to_string(index=False))
    print(summary.round(4).to_string(index=False))


if __name__ == "__main__":
    run()
