#!/usr/bin/env python3
"""Virus-aware PAHD-R hybrid score experiments.

This sweep tests whether virus-specific component and local graph signals are
useful as auxiliary evidence, rather than replacing the PAHD-R-Core rank.
Weights are fixed a priori and are not fitted to target labels.
"""

from __future__ import annotations

from pathlib import Path
import sys

import numpy as np
import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parent.parent
RESULTS_DIR = PROJECT_ROOT / "results" / "mutbench"
sys.path.insert(0, str(PROJECT_ROOT / "scripts"))

import audit_pahd_r_decoy_coordinate_robustness as final_scores  # noqa: E402
import run_pahd_r_multi_hypothesis as pahd  # noqa: E402
import sweep_pahd_r_calibration_reliability as calibration  # noqa: E402
import sweep_pahd_r_virus_aware_component_graph as virus_aware  # noqa: E402

OUT_RESULTS = RESULTS_DIR / "pahd_r_virus_aware_hybrid_results.csv"
OUT_SUMMARY = RESULTS_DIR / "pahd_r_virus_aware_hybrid_summary.csv"
OUT_SELECTIVE = RESULTS_DIR / "pahd_r_virus_aware_hybrid_selective_summary.csv"
OUT_REPORT = RESULTS_DIR / "pahd_r_virus_aware_hybrid_sweep.md"

METRICS = ["mcc_exact", "mcc_window_10", "precision_20", "constrained_fpr", "coverage_10"]


def rank_blend(*weighted_scores: tuple[float, np.ndarray]) -> np.ndarray:
    total = np.zeros_like(weighted_scores[0][1], dtype=float)
    weight_sum = 0.0
    for weight, score in weighted_scores:
        total += weight * virus_aware.safe_rank(score)
        weight_sum += weight
    return total / max(weight_sum, 1e-12)


def candidate_aux_scores(data: dict[str, pd.DataFrame], pathogens: list[str], pathogen: str) -> dict[str, np.ndarray]:
    components = virus_aware.component_scores(data, pathogens, pathogen)
    graphs = virus_aware.graph_scores(data, pathogens, pathogen)
    return {
        "component_evo_access": components["component_evo_access"],
        "component_gated_evolution": components["component_gated_evolution"],
        "graph_core_views": graphs["virus_graph_core_views"],
        "graph_escape_weighted": graphs["virus_graph_escape_weighted"],
        "graph_all_views": graphs["virus_graph_all_views"],
    }


def make_hybrids(core: np.ndarray, aux: dict[str, np.ndarray]) -> dict[str, np.ndarray]:
    rows: dict[str, np.ndarray] = {}
    for name, score in aux.items():
        for alpha in [0.10, 0.20, 0.35, 0.50]:
            tag = f"core{int((1-alpha)*100):02d}_{name}{int(alpha*100):02d}"
            rows[tag] = rank_blend((1.0 - alpha, core), (alpha, score))
    for alpha in [0.10, 0.20, 0.35]:
        tag = f"core{int((1-alpha)*100):02d}_component_graph{int(alpha*100):02d}"
        rows[tag] = rank_blend(
            (1.0 - alpha, core),
            (alpha / 2.0, aux["component_evo_access"]),
            (alpha / 2.0, aux["graph_escape_weighted"]),
        )
    for alpha in [0.10, 0.20, 0.35]:
        tag = f"core{int((1-alpha)*100):02d}_gated_graph{int(alpha*100):02d}"
        rows[tag] = rank_blend(
            (1.0 - alpha, core),
            (alpha / 2.0, aux["component_gated_evolution"]),
            (alpha / 2.0, aux["graph_core_views"]),
        )
    return rows


def predict(score: np.ndarray, reliability: np.ndarray, selector: str) -> np.ndarray:
    if selector == "top8":
        return pahd.top_fraction_pred(score, 0.08)
    if selector == "top10":
        return pahd.top_fraction_pred(score, 0.10)
    if selector == "reliability_top8":
        combined = 0.70 * virus_aware.safe_rank(score) + 0.30 * virus_aware.safe_rank(reliability)
        return pahd.top_fraction_pred(combined, 0.08)
    raise ValueError(selector)


def evaluate(pathogen: str, df: pd.DataFrame, score: np.ndarray, pred: np.ndarray) -> dict[str, float]:
    y = df["layer_a"].astype(int).values
    p20, e20 = pahd.precision_and_enrichment(y, score, 20)
    return {
        "n_predicted": int(pred.sum()),
        "pred_frac": float(pred.mean()),
        "mcc_exact": pahd.region_mcc(y, pred, 0),
        "mcc_window_10": pahd.region_mcc(y, pred, 10),
        "precision_20": p20,
        "enrichment_20": e20,
        "constrained_fpr": pahd.constrained_fpr(pathogen, len(df), pred),
        "coverage_10": pahd.expanded_coverage(pred, 10),
    }


def markdown_table(frame: pd.DataFrame) -> str:
    return virus_aware.markdown_table(frame)


def decision(row: pd.Series) -> str:
    if row["entry"] == "PAHD-R-Core":
        return "current_default"
    if row["entry"] == "PAHD-R-Core-Calibrated":
        return "existing_candidate"
    if (
        row["delta_mcc_exact_vs_calibrated"] > 0
        and row["delta_mcc_window_10_vs_calibrated"] >= 0
        and row["delta_precision_20_vs_calibrated"] >= 0
        and row["delta_constrained_fpr_vs_calibrated"] <= 0
    ):
        return "candidate_beats_calibrated"
    if (
        row["delta_mcc_exact_vs_core"] > 0
        and row["delta_mcc_window_10_vs_core"] >= 0
        and row["delta_precision_20_vs_core"] >= 0
        and row["delta_constrained_fpr_vs_core"] <= 0
    ):
        return "candidate_vs_core"
    if row["delta_mcc_exact_vs_core"] >= -0.01 and row["delta_constrained_fpr_vs_core"] <= -0.02:
        return "candidate_tradeoff"
    if row["delta_mcc_exact_vs_core"] < -0.04 or row["delta_precision_20_vs_core"] < -0.05:
        return "reject"
    return "diagnostic_only"


def summarize(results: pd.DataFrame) -> pd.DataFrame:
    summary = (
        results.groupby(["entry", "score_family", "score_variant", "selector"])
        .agg(
            mean_mcc_exact=("mcc_exact", "mean"),
            mean_mcc_window_10=("mcc_window_10", "mean"),
            mean_precision_20=("precision_20", "mean"),
            mean_constrained_fpr=("constrained_fpr", "mean"),
            mean_coverage_10=("coverage_10", "mean"),
            mean_pred_frac=("pred_frac", "mean"),
            positive_exact_pathogens=("mcc_exact", lambda x: int((x > 0).sum())),
        )
        .reset_index()
    )
    core = summary[summary["entry"] == "PAHD-R-Core"].iloc[0]
    calibrated = summary[summary["entry"] == "PAHD-R-Core-Calibrated"].iloc[0]
    for metric in METRICS:
        summary[f"delta_{metric}_vs_core"] = summary[f"mean_{metric}"] - float(core[f"mean_{metric}"])
        summary[f"delta_{metric}_vs_calibrated"] = summary[f"mean_{metric}"] - float(calibrated[f"mean_{metric}"])
    summary["decision"] = summary.apply(decision, axis=1)
    return summary.sort_values(["decision", "mean_mcc_exact", "mean_mcc_window_10"], ascending=[True, False, False])


def selective_summary(results: pd.DataFrame) -> pd.DataFrame:
    return virus_aware.selective_summary(results)


def run() -> None:
    data = pahd.load_feature_matrices()
    pathogens = virus_aware.primary_pathogens(data)
    selectors = ["top8", "top10", "reliability_top8"]
    rows = []

    for pathogen in pathogens:
        df = data[pathogen]
        ranks = calibration.module_ranks(data, pathogens, pathogen)
        baseline_scores = final_scores.candidate_scores(data, pathogens, pathogen)
        core = baseline_scores["PAHD-R-Core"]
        core_rel = calibration.reliability_score("PAHD-R-Core", core, ranks)
        rows.append({
            "pathogen": pathogen,
            "entry": "PAHD-R-Core",
            "score_family": "baseline",
            "score_variant": "baseline",
            "selector": "top10",
            **evaluate(pathogen, df, core, pahd.top_fraction_pred(core, 0.10)),
        })
        rows.append({
            "pathogen": pathogen,
            "entry": "PAHD-R-Core-Calibrated",
            "score_family": "baseline",
            "score_variant": "baseline",
            "selector": "reliability_top8",
            **evaluate(pathogen, df, core, predict(core, core_rel, "reliability_top8")),
        })

        for variant, score in make_hybrids(core, candidate_aux_scores(data, pathogens, pathogen)).items():
            rel = calibration.reliability_score("PAHD-R-Core", score, ranks)
            for selector in selectors:
                rows.append({
                    "pathogen": pathogen,
                    "entry": f"{variant}:{selector}",
                    "score_family": "hybrid",
                    "score_variant": variant,
                    "selector": selector,
                    **evaluate(pathogen, df, score, predict(score, rel, selector)),
                })

    results = pd.DataFrame(rows)
    summary = summarize(results)
    selective = selective_summary(results)
    results.to_csv(OUT_RESULTS, index=False)
    summary.to_csv(OUT_SUMMARY, index=False)
    selective.to_csv(OUT_SELECTIVE, index=False)

    candidates = summary[summary["decision"].str.contains("candidate")]
    top = summary.sort_values(["mean_mcc_exact", "mean_mcc_window_10"], ascending=False).head(20)
    report = [
        "# PAHD-R virus-aware hybrid sweep",
        "",
        "Date: 2026-04-27 KST",
        "",
        "## Scope",
        "",
        (
            "This sweep blends PAHD-R-Core with virus-aware component and graph signals. "
            "Weights are fixed before evaluation; labels are used only for scoring."
        ),
        "",
        "## Candidates",
        "",
        markdown_table(candidates),
        "",
        "## Top global summary",
        "",
        markdown_table(top),
        "",
        "## Selective summary",
        "",
        markdown_table(selective.head(20)),
        "",
    ]
    OUT_REPORT.write_text("\n".join(report), encoding="utf-8")
    print(OUT_REPORT)
    print(candidates.round(4).to_string(index=False) if len(candidates) else "No candidates")


if __name__ == "__main__":
    run()
