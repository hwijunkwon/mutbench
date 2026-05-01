#!/usr/bin/env python3
"""Region-first/site-within-region PAHD-R sweep."""

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
import sweep_pahd_r_targeted_dedup_winsorized as targeted  # noqa: E402

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


def smooth(values: np.ndarray, radius: int) -> np.ndarray:
    values = np.asarray(values, dtype=float)
    out = np.zeros_like(values)
    for i in range(len(values)):
        lo = max(0, i - radius)
        hi = min(len(values), i + radius + 1)
        out[i] = values[lo:hi].mean()
    return out


def region_first_pred(score: np.ndarray, frac: float, radius: int, sites_per_region: int) -> np.ndarray:
    n = len(score)
    k = max(1, int(round(n * frac)))
    n_regions = max(1, int(np.ceil(k / sites_per_region)))
    score_rank = pahd.rank_percentile(score)
    region_score = smooth(score_rank, radius)
    centers = []
    suppressed = np.zeros(n, dtype=bool)
    for idx in np.argsort(-region_score):
        if suppressed[idx]:
            continue
        centers.append(int(idx))
        suppressed[max(0, idx - radius): min(n, idx + radius + 1)] = True
        if len(centers) >= n_regions:
            break
    chosen = []
    for center in centers:
        lo = max(0, center - radius)
        hi = min(n, center + radius + 1)
        local = np.arange(lo, hi)
        best = local[np.argsort(-score_rank[local])[:sites_per_region]]
        chosen.extend(best.tolist())
    chosen = sorted(set(chosen), key=lambda i: -score_rank[i])[:k]
    pred = np.zeros(n, dtype=bool)
    pred[chosen] = True
    return pred


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


def decision(row: pd.Series) -> str:
    if row["variant"] == "baseline":
        return "current_reference"
    if row["delta_mcc_exact"] > 0 and row["delta_precision_20"] >= 0 and row["delta_coverage_10"] <= 0.02:
        return "candidate_region_first"
    if row["delta_mcc_window_10"] < -0.08 or row["delta_precision_20"] < -0.05:
        return "reject"
    return "diagnostic_only"


def run() -> None:
    data = pahd.load_feature_matrices()
    pathogens = targeted.primary_pathogens(data)
    variants = [
        ("baseline", 0, 0),
        ("region_r5_s1", 5, 1),
        ("region_r8_s1", 8, 1),
        ("region_r10_s1", 10, 1),
        ("region_r5_s2", 5, 2),
        ("region_r8_s2", 8, 2),
        ("region_r10_s2", 10, 2),
    ]
    rows = []
    for pathogen in pathogens:
        scores = final_scores.candidate_scores(data, pathogens, pathogen)
        for mode in MODES:
            frac = 0.08 if mode == "PAHD-R-Review" else 0.10
            for variant, radius, sites_per_region in variants:
                if variant == "baseline":
                    pred = pahd.top_fraction_pred(scores[mode], frac)
                else:
                    pred = region_first_pred(scores[mode], frac, radius, sites_per_region)
                rows.append({
                    "variant": variant,
                    "pathogen": pathogen,
                    "mode": mode,
                    **evaluate(pathogen, data[pathogen], scores[mode], pred),
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
    summary = summary.sort_values(["mode", "mean_mcc_exact", "mean_precision_20"], ascending=[True, False, False])

    results_path = RESULTS_DIR / "pahd_r_region_first_results.csv"
    summary_path = RESULTS_DIR / "pahd_r_region_first_summary.csv"
    report_path = RESULTS_DIR / "pahd_r_region_first_sweep.md"
    results.to_csv(results_path, index=False)
    summary.to_csv(summary_path, index=False)

    candidates = summary[summary["decision"] == "candidate_region_first"]
    report = [
        "# PAHD-R Region-First Sweep",
        "",
        "Date: 2026-04-27 KST",
        "",
        "## Scope",
        "",
        "This sweep detects compact high-score regions first, then selects top sites within each region.",
        "",
        "## Candidates",
        "",
        markdown_table(candidates) if len(candidates) else "No region-first candidate passed criteria.",
        "",
        "## Full Summary",
        "",
        markdown_table(summary),
        "",
    ]
    report_path.write_text("\n".join(report), encoding="utf-8")
    print(report_path)
    print(candidates.round(4).to_string(index=False) if len(candidates) else "No candidates")


if __name__ == "__main__":
    run()
