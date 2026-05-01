#!/usr/bin/env python3
"""Negative-control-aware calibration and reliability-gated PAHD-R sweep."""

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

MODES = ["PAHD-R-Core", "PAHD-R-Augmented", "PAHD-R-Review"]


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


def primary_pathogens(data: dict[str, pd.DataFrame]) -> list[str]:
    benchmark = pd.read_csv(RESULTS_DIR / "multilayer_9pathogen_results.csv")
    return sorted(set(benchmark["pathogen"].unique()) & set(data.keys()))


def module_ranks(data: dict[str, pd.DataFrame], pathogens: list[str], target: str) -> pd.DataFrame:
    train_data = {p: df for p, df in data.items() if p != target and p in pathogens}
    signs = pahd.compute_feature_signs(train_data)
    effects = pahd.compute_feature_effects(train_data)
    df = data[target]
    full = pahd.module_scores(df, signs)
    non_ai = pahd.non_ai_module_scores(df, signs)
    out = pd.DataFrame(index=np.arange(len(df)))
    for module in full.columns:
        out[f"full_{module}"] = pahd.rank_percentile(full[module].values)
    for module in non_ai.columns:
        out[f"core_{module}"] = pahd.rank_percentile(non_ai[module].values)
    full_learned = pahd.combine_modules(full, pahd.learned_module_weights(effects))
    core_learned = pahd.combine_modules(non_ai, pahd.learned_non_ai_weights(effects))
    out["full_learned"] = pahd.rank_percentile(full_learned)
    out["core_learned"] = pahd.rank_percentile(core_learned)
    return out


def reliability_score(mode: str, score: np.ndarray, ranks: pd.DataFrame) -> np.ndarray:
    score_rank = pahd.rank_percentile(score)
    if mode == "PAHD-R-Core":
        cols = ["core_recurrence", "core_diversity", "core_phylo", "structure_non_ai", "core_learned"]
    elif mode == "PAHD-R-Review":
        cols = ["core_recurrence", "core_diversity", "core_phylo"]
    else:
        cols = ["full_recurrence", "full_diversity", "full_phylo", "full_constraint", "full_structure", "full_semantic", "full_learned"]
    cols = [col for col in cols if col in ranks]
    support = ranks[cols].mean(axis=1).values if cols else score_rank
    agreement = np.zeros(len(score), dtype=float)
    for q in [0.80, 0.85, 0.90]:
        top_count = np.zeros(len(score), dtype=float)
        for col in cols:
            top_count += ranks[col].values >= q
        agreement += top_count / max(len(cols), 1)
    agreement /= 3.0
    return 0.55 * score_rank + 0.30 * support + 0.15 * agreement


def predict_variant(score: np.ndarray, reliability: np.ndarray, mode: str, variant: str) -> np.ndarray:
    base_frac = 0.08 if mode == "PAHD-R-Review" else 0.10
    pred = np.zeros(len(score), dtype=bool)
    if variant == "baseline":
        return pahd.top_fraction_pred(score, base_frac)
    if variant.startswith("quantile_"):
        q = float(variant.split("_", 1)[1]) / 100.0
        pred[score >= np.quantile(score, q)] = True
        return pred
    if variant.startswith("reliability_top_"):
        frac = float(variant.rsplit("_", 1)[1]) / 100.0
        combined = 0.70 * pahd.rank_percentile(score) + 0.30 * pahd.rank_percentile(reliability)
        return pahd.top_fraction_pred(combined, frac)
    if variant.startswith("reliability_gate_"):
        parts = variant.split("_")
        score_q = float(parts[2]) / 100.0
        rel_q = float(parts[3]) / 100.0
        pred[(score >= np.quantile(score, score_q)) & (reliability >= np.quantile(reliability, rel_q))] = True
        if pred.sum() == 0:
            return pahd.top_fraction_pred(score, max(0.02, base_frac / 4.0))
        return pred
    if variant.startswith("decoy_margin_"):
        q = float(variant.rsplit("_", 1)[1]) / 100.0
        score_rank = pahd.rank_percentile(score)
        rel_rank = pahd.rank_percentile(reliability)
        margin = score_rank - (1.0 - rel_rank)
        pred[margin >= np.quantile(margin, q)] = True
        return pred
    raise ValueError(f"unknown variant: {variant}")


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
        "no_call_rate": float(1.0 - pred.mean()),
    }


def decision(row: pd.Series) -> str:
    if row["variant"] == "baseline":
        return "current_reference"
    if (
        row["delta_precision_20"] > 0.0
        and row["delta_constrained_fpr"] <= 0.0
        and row["delta_mcc_window_10"] >= -0.01
    ):
        return "candidate_review_calibration"
    if (
        row["delta_mcc_exact"] > 0.0
        and row["delta_precision_20"] >= 0.0
        and row["delta_constrained_fpr"] <= 0.02
    ):
        return "candidate_exact_calibration"
    if row["delta_mcc_window_10"] < -0.08 or row["delta_precision_20"] < -0.05:
        return "reject"
    return "diagnostic_only"


def run() -> None:
    data = pahd.load_feature_matrices()
    pathogens = primary_pathogens(data)
    variants = [
        "baseline",
        "quantile_90",
        "quantile_92",
        "quantile_95",
        "reliability_top_8",
        "reliability_top_10",
        "reliability_gate_85_60",
        "reliability_gate_90_50",
        "reliability_gate_90_70",
        "decoy_margin_90",
        "decoy_margin_92",
    ]
    rows = []
    for pathogen in pathogens:
        scores = final_scores.candidate_scores(data, pathogens, pathogen)
        ranks = module_ranks(data, pathogens, pathogen)
        for mode in MODES:
            score = scores[mode]
            rel = reliability_score(mode, score, ranks)
            for variant in variants:
                pred = predict_variant(score, rel, mode, variant)
                rows.append({
                    "pathogen": pathogen,
                    "mode": mode,
                    "variant": variant,
                    **evaluate(pathogen, data[pathogen], score, pred),
                })
    results = pd.DataFrame(rows)
    summary = (
        results.groupby(["variant", "mode"])
        .agg(
            mean_mcc_exact=("mcc_exact", "mean"),
            mean_mcc_window_10=("mcc_window_10", "mean"),
            mean_precision_20=("precision_20", "mean"),
            mean_constrained_fpr=("constrained_fpr", "mean"),
            mean_coverage_10=("coverage_10", "mean"),
            mean_pred_frac=("pred_frac", "mean"),
            positive_exact_pathogens=("mcc_exact", lambda s: int((s > 0).sum())),
        )
        .reset_index()
    )
    baseline = summary[summary["variant"] == "baseline"][
        ["mode", "mean_mcc_exact", "mean_mcc_window_10", "mean_precision_20", "mean_constrained_fpr", "mean_coverage_10"]
    ].rename(columns={
        "mean_mcc_exact": "baseline_mcc_exact",
        "mean_mcc_window_10": "baseline_mcc_window_10",
        "mean_precision_20": "baseline_precision_20",
        "mean_constrained_fpr": "baseline_constrained_fpr",
        "mean_coverage_10": "baseline_coverage_10",
    })
    summary = summary.merge(baseline, on="mode", how="left")
    summary["delta_mcc_exact"] = summary["mean_mcc_exact"] - summary["baseline_mcc_exact"]
    summary["delta_mcc_window_10"] = summary["mean_mcc_window_10"] - summary["baseline_mcc_window_10"]
    summary["delta_precision_20"] = summary["mean_precision_20"] - summary["baseline_precision_20"]
    summary["delta_constrained_fpr"] = summary["mean_constrained_fpr"] - summary["baseline_constrained_fpr"]
    summary["delta_coverage_10"] = summary["mean_coverage_10"] - summary["baseline_coverage_10"]
    summary["decision"] = summary.apply(decision, axis=1)
    summary = summary.sort_values(["mode", "decision", "mean_precision_20", "mean_mcc_exact"], ascending=[True, True, False, False])

    results_path = RESULTS_DIR / "pahd_r_calibration_reliability_results.csv"
    summary_path = RESULTS_DIR / "pahd_r_calibration_reliability_summary.csv"
    report_path = RESULTS_DIR / "pahd_r_calibration_reliability_sweep.md"
    results.to_csv(results_path, index=False)
    summary.to_csv(summary_path, index=False)

    candidates = summary[summary["decision"].str.startswith("candidate")]
    report = [
        "# PAHD-R Calibration and Reliability Sweep",
        "",
        "Date: 2026-04-27 KST",
        "",
        "## Scope",
        "",
        (
            "This sweep tests negative-control-aware quantile calibration and "
            "module-agreement reliability gating. It keeps the current PAHD-R score "
            "families and changes only prediction selection/calibration."
        ),
        "",
        "## Candidates",
        "",
        markdown_table(candidates) if len(candidates) else "No candidate passed the calibration criteria.",
        "",
        "## Full Summary",
        "",
        markdown_table(summary),
        "",
        "## Interpretation",
        "",
        (
            "A useful calibration candidate should improve precision or exact MCC "
            "without relying on broader coverage or higher constrained FPR. Candidates "
            "from this sweep are review-mode candidates unless paired/pathogen-level "
            "checks support default adoption."
        ),
        "",
    ]
    report_path.write_text("\n".join(report), encoding="utf-8")
    print(report_path)
    print(candidates.round(4).to_string(index=False) if len(candidates) else "No candidates")


if __name__ == "__main__":
    run()
