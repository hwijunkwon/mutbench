#!/usr/bin/env python3
"""Adversarial audit for adoptable PAHD-R domain-prior repair candidates."""

from __future__ import annotations

from pathlib import Path
import sys

import numpy as np
import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parent.parent
RESULTS_DIR = PROJECT_ROOT / "results" / "mutbench"
sys.path.insert(0, str(PROJECT_ROOT / "scripts"))
import audit_pahd_r_decoy_coordinate_robustness as decoy_audit  # noqa: E402
import run_pahd_r_multi_hypothesis as pahd  # noqa: E402
import test_pahd_r_domain_prior_repair as repair  # noqa: E402


N_PERM = 200
ADOPTABLE = [
    ("HCV", "PAHD-R-Core", 0.30),
    ("HCV", "PAHD-R-Augmented", 0.30),
    ("HCV", "PAHD-R-Review", 0.20),
    ("SARS-CoV-2", "PAHD-R-Core", 0.30),
    ("SARS-CoV-2", "PAHD-R-Review", 0.30),
]


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


def evaluate(pathogen: str, df: pd.DataFrame, mode: str, score: np.ndarray) -> dict[str, float]:
    y = df["layer_a"].astype(int).values
    frac = 0.08 if mode == "PAHD-R-Review" else 0.10
    pred = pahd.top_fraction_pred(score, frac)
    p20, _ = pahd.precision_and_enrichment(y, score, 20)
    return {
        "mcc_exact": pahd.region_mcc(y, pred, 0),
        "mcc_window_10": pahd.region_mcc(y, pred, 10),
        "precision_20": p20,
        "constrained_fpr": pahd.constrained_fpr(pathogen, len(df), pred),
        "coverage_10": pahd.expanded_coverage(pred, 10),
    }


def permutation_audit(
    y: np.ndarray,
    pred: np.ndarray,
    rng: np.random.Generator,
    n_perm: int = N_PERM,
) -> tuple[float, float, float]:
    null = []
    for _ in range(n_perm):
        null.append(pahd.region_mcc(rng.permutation(y), pred, 0))
    null_arr = np.asarray(null, dtype=float)
    observed = pahd.region_mcc(y, pred, 0)
    return (
        float(null_arr.mean()),
        float(np.quantile(null_arr, 0.95)),
        float(np.mean(null_arr >= observed)),
    )


def run() -> None:
    data = pahd.load_feature_matrices()
    benchmark = pd.read_csv(RESULTS_DIR / "multilayer_9pathogen_results.csv")
    pathogens = sorted(set(benchmark["pathogen"].unique()) & set(data.keys()))
    rng = np.random.default_rng(20260426)

    rows = []
    for pathogen, mode, weight in ADOPTABLE:
        df = data[pathogen]
        y = df["layer_a"].astype(int).values
        base = decoy_audit.candidate_scores(data, pathogens, pathogen)[mode]
        variants = {
            "baseline": base,
            "domain_prior": repair.repaired_score(
                base,
                repair.domain_prior(pathogen, len(df), "domain_prior"),
                weight,
            ),
            "shift_plus_80": repair.repaired_score(
                base,
                repair.domain_prior(pathogen, len(df), "domain_prior_shift_plus_80"),
                weight,
            ),
            "shift_minus_80": repair.repaired_score(
                base,
                repair.domain_prior(pathogen, len(df), "domain_prior_shift_minus_80"),
                weight,
            ),
            "broad_random_region": repair.repaired_score(
                base,
                repair.domain_prior(pathogen, len(df), "broad_random_region"),
                weight,
            ),
        }

        base_metrics = evaluate(pathogen, df, mode, base)
        for variant, score in variants.items():
            metrics = evaluate(pathogen, df, mode, score)
            frac = 0.08 if mode == "PAHD-R-Review" else 0.10
            pred = pahd.top_fraction_pred(score, frac)
            null_mean, null_p95, empirical_p = permutation_audit(y, pred, rng)
            rows.append({
                "pathogen": pathogen,
                "mode": mode,
                "repair_weight": weight,
                "variant": variant,
                **metrics,
                "delta_mcc_exact": metrics["mcc_exact"] - base_metrics["mcc_exact"],
                "delta_mcc_window_10": metrics["mcc_window_10"] - base_metrics["mcc_window_10"],
                "delta_precision_20": metrics["precision_20"] - base_metrics["precision_20"],
                "delta_constrained_fpr": metrics["constrained_fpr"] - base_metrics["constrained_fpr"],
                "delta_coverage_10": metrics["coverage_10"] - base_metrics["coverage_10"],
                "null_mean_mcc": null_mean,
                "null_p95_mcc": null_p95,
                "empirical_p_null_ge_observed": empirical_p,
            })

    results = pd.DataFrame(rows)
    domain = results[results["variant"] == "domain_prior"].copy()
    controls = results[results["variant"].isin(["shift_plus_80", "shift_minus_80", "broad_random_region"])].copy()
    control_best = (
        controls.sort_values(["pathogen", "mode", "mcc_exact", "precision_20"], ascending=[True, True, False, False])
        .groupby(["pathogen", "mode"])
        .head(1)[["pathogen", "mode", "variant", "mcc_exact", "mcc_window_10", "precision_20", "coverage_10"]]
        .rename(columns={
            "variant": "best_control_variant",
            "mcc_exact": "best_control_mcc_exact",
            "mcc_window_10": "best_control_mcc_window_10",
            "precision_20": "best_control_precision_20",
            "coverage_10": "best_control_coverage_10",
        })
    )
    decision = domain.merge(control_best, on=["pathogen", "mode"], how="left")
    decision["beats_control_exact"] = decision["mcc_exact"] > decision["best_control_mcc_exact"]
    decision["beats_control_precision"] = decision["precision_20"] >= decision["best_control_precision_20"]
    decision["passes_permutation"] = decision["empirical_p_null_ge_observed"] <= 0.01
    decision["has_reportable_constrained_fpr"] = decision["constrained_fpr"].notna()
    decision["adoption_decision"] = np.where(
        decision["beats_control_exact"]
        & decision["beats_control_precision"]
        & decision["passes_permutation"]
        & decision["has_reportable_constrained_fpr"],
        "adoptable",
        np.where(
            decision["beats_control_exact"]
            & decision["beats_control_precision"]
            & decision["passes_permutation"],
            "adoptable_after_coordinate_review",
            "hold_or_reject",
        ),
    )

    results.to_csv(RESULTS_DIR / "pahd_r_repaired_prior_candidate_audit_results.csv", index=False)
    decision.to_csv(RESULTS_DIR / "pahd_r_repaired_prior_candidate_decisions.csv", index=False)

    report = [
        "# PAHD-R Repaired Prior Candidate Audit",
        "",
        "Date: 2026-04-26 KST",
        "",
        "## Domain-Prior Decisions",
        "",
        markdown_table(decision[[
            "pathogen",
            "mode",
            "repair_weight",
            "mcc_exact",
            "delta_mcc_exact",
            "mcc_window_10",
            "delta_mcc_window_10",
            "precision_20",
            "delta_precision_20",
            "constrained_fpr",
            "coverage_10",
            "best_control_variant",
            "best_control_mcc_exact",
            "best_control_precision_20",
            "empirical_p_null_ge_observed",
            "has_reportable_constrained_fpr",
            "adoption_decision",
        ]]),
        "",
        "## Full Variant Results",
        "",
        markdown_table(results),
        "",
        "## Interpretation",
        "",
        "- A repaired prior candidate must pass label permutation and beat shifted/random prior controls on exact MCC.",
        "- Candidates that improve versus baseline but fail to beat controls should remain exploratory.",
        "- HCV candidates are adoptable only when constrained FPR is reportable in the local feature coordinate frame.",
        "",
    ]
    out = RESULTS_DIR / "pahd_r_repaired_prior_candidate_audit.md"
    out.write_text("\n".join(report), encoding="utf-8")
    print(out)
    print(decision.round(4).to_string(index=False))


if __name__ == "__main__":
    run()
