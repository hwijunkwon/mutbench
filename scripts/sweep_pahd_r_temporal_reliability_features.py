#!/usr/bin/env python3
"""Use temporal metadata as reliability features, not score replacement."""

from __future__ import annotations

from collections import defaultdict
from pathlib import Path
import re
import sys

import numpy as np
import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parent.parent
RESULTS_DIR = PROJECT_ROOT / "results" / "mutbench"
META_PATH = PROJECT_ROOT / "data" / "additional" / "pahd_r_temporal_metadata" / "combined_temporal_metadata.csv"

sys.path.insert(0, str(PROJECT_ROOT / "scripts"))
import audit_pahd_r_decoy_coordinate_robustness as final_scores  # noqa: E402
import audit_pahd_r_raw_sequence_stability as rawseq  # noqa: E402
import run_pahd_r_multi_hypothesis as pahd  # noqa: E402
import sweep_pahd_r_targeted_dedup_winsorized as targeted  # noqa: E402

MODES = ["PAHD-R-Core", "PAHD-R-Augmented", "PAHD-R-Review"]
TARGETS = {"HIV-1", "MERS"}
ACCESSION_RE = re.compile(r"^([A-Z]{1,4}_?\d+(?:\.\d+)?)\b")
YEAR_RE = re.compile(r"(?<![A-Za-z0-9])((?:19|20)\d{2})(?![A-Za-z0-9])")


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


def accession_from_header(header: str) -> str:
    match = ACCESSION_RE.search(header)
    return match.group(1) if match else ""


def year_from_text(value: object) -> int | None:
    match = YEAR_RE.search(str(value))
    if match is None:
        return None
    year = int(match.group(1))
    return year if 1970 <= year <= 2026 else None


def metadata_years() -> dict[str, int]:
    meta = pd.read_csv(META_PATH)
    years = {}
    for row in meta.itertuples():
        year = year_from_text(getattr(row, "collection_date", "")) or year_from_text(getattr(row, "ncbi_create_date", ""))
        if year is not None and isinstance(row.accession, str):
            years[row.accession] = year
    return years


def temporal_features(pathogen: str, n: int, min_unique: int = 10) -> pd.DataFrame:
    year_map = metadata_years()
    by_year: dict[int, set[str]] = defaultdict(set)
    for header, seq in targeted.read_fasta_records(rawseq.FASTA_PATHS[pathogen]):
        if len(seq) < n:
            continue
        year = year_map.get(accession_from_header(header))
        if year is not None:
            by_year[year].add(seq)
    eligible = {year: sorted(seqs) for year, seqs in by_year.items() if len(seqs) >= min_unique}
    if len(eligible) < 2:
        return pd.DataFrame({
            "temporal_presence_frac": np.zeros(n),
            "temporal_rank_stability": np.zeros(n),
            "early_late_replicates": np.zeros(n),
            "temporal_outlier_penalty": np.ones(n),
            "temporal_reliability": np.zeros(n),
        })
    variations = []
    for year in sorted(eligible):
        variation, _ = targeted.variation_entropy(eligible[year], n)
        variations.append(variation)
    mat = np.vstack(variations)
    top_mask = mat >= np.quantile(mat, 0.90, axis=1)[:, None]
    presence = top_mask.mean(axis=0)
    ranks = np.vstack([pahd.rank_percentile(row) for row in mat])
    stability = 1.0 - np.nan_to_num(ranks.std(axis=0), nan=1.0)
    stability = np.clip(stability, 0.0, 1.0)
    mid = len(variations) // 2
    early = mat[:mid].mean(axis=0)
    late = mat[mid:].mean(axis=0)
    early_late = ((early >= np.quantile(early, 0.90)) & (late >= np.quantile(late, 0.90))).astype(float)
    outlier_penalty = 1.0 - (mat.max(axis=0) / (mat.sum(axis=0) + 1e-12))
    outlier_penalty = np.clip(outlier_penalty, 0.0, 1.0)
    reliability = (
        0.35 * pahd.rank_percentile(presence)
        + 0.30 * pahd.rank_percentile(stability)
        + 0.20 * early_late
        + 0.15 * pahd.rank_percentile(outlier_penalty)
    )
    return pd.DataFrame({
        "temporal_presence_frac": presence,
        "temporal_rank_stability": stability,
        "early_late_replicates": early_late,
        "temporal_outlier_penalty": outlier_penalty,
        "temporal_reliability": reliability,
    })


def adjust_score(pathogen: str, score: np.ndarray, temp: pd.DataFrame | None, variant: str) -> np.ndarray:
    if pathogen not in TARGETS or temp is None:
        return score
    base = pahd.rank_percentile(score)
    rel = temp["temporal_reliability"].values
    if variant == "baseline":
        return score
    if variant == "temporal_rel_05":
        return 0.95 * base + 0.05 * pahd.rank_percentile(rel)
    if variant == "temporal_rel_10":
        return 0.90 * base + 0.10 * pahd.rank_percentile(rel)
    if variant == "temporal_filter_top":
        gated = base.copy()
        gated[rel < np.quantile(rel, 0.50)] *= 0.90
        return gated
    if variant == "temporal_el_replicate":
        gated = base.copy()
        gated[temp["early_late_replicates"].values <= 0] *= 0.92
        return gated
    raise ValueError(variant)


def evaluate(pathogen: str, df: pd.DataFrame, score: np.ndarray, mode: str) -> dict[str, float]:
    frac = 0.08 if mode == "PAHD-R-Review" else 0.10
    pred = pahd.top_fraction_pred(score, frac)
    y = df["layer_a"].astype(int).values
    p20, e20 = pahd.precision_and_enrichment(y, score, 20)
    return {
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
    if row["target_delta_mcc_window_10"] > 0.01 and row["delta_mcc_exact"] >= -0.005 and row["delta_constrained_fpr"] <= 0.01:
        return "candidate_temporal_reliability"
    if row["target_delta_mcc_window_10"] < -0.05 or row["delta_mcc_window_10"] < -0.03:
        return "reject"
    return "diagnostic_only"


def run() -> None:
    data = pahd.load_feature_matrices()
    pathogens = targeted.primary_pathogens(data)
    temporal = {p: temporal_features(p, len(data[p])) for p in pathogens if p in TARGETS}
    variants = ["baseline", "temporal_rel_05", "temporal_rel_10", "temporal_filter_top", "temporal_el_replicate"]
    rows = []
    feature_rows = []
    for pathogen, frame in temporal.items():
        feature_rows.append({
            "pathogen": pathogen,
            "mean_temporal_reliability": frame["temporal_reliability"].mean(),
            "mean_presence_frac": frame["temporal_presence_frac"].mean(),
            "early_late_replicate_sites": int(frame["early_late_replicates"].sum()),
        })
    for pathogen in pathogens:
        scores = final_scores.candidate_scores(data, pathogens, pathogen)
        for mode in MODES:
            for variant in variants:
                score = adjust_score(pathogen, scores[mode], temporal.get(pathogen), variant)
                rows.append({
                    "variant": variant,
                    "pathogen": pathogen,
                    "mode": mode,
                    **evaluate(pathogen, data[pathogen], score, mode),
                })
    results = pd.DataFrame(rows)
    features = pd.DataFrame(feature_rows)
    summary = (
        results.groupby(["variant", "mode"])
        .agg(
            mean_mcc_exact=("mcc_exact", "mean"),
            mean_mcc_window_10=("mcc_window_10", "mean"),
            mean_precision_20=("precision_20", "mean"),
            mean_constrained_fpr=("constrained_fpr", "mean"),
            mean_coverage_10=("coverage_10", "mean"),
        )
        .reset_index()
    )
    target_summary = (
        results[results["pathogen"].isin(TARGETS)]
        .groupby(["variant", "mode"])
        .agg(target_mean_mcc_window_10=("mcc_window_10", "mean"), target_precision_20=("precision_20", "mean"))
        .reset_index()
    )
    summary = summary.merge(target_summary, on=["variant", "mode"], how="left")
    baseline = summary[summary["variant"] == "baseline"][
        ["mode", "mean_mcc_exact", "mean_mcc_window_10", "mean_precision_20", "mean_constrained_fpr", "target_mean_mcc_window_10"]
    ].rename(columns={
        "mean_mcc_exact": "baseline_mcc_exact",
        "mean_mcc_window_10": "baseline_mcc_window_10",
        "mean_precision_20": "baseline_precision_20",
        "mean_constrained_fpr": "baseline_constrained_fpr",
        "target_mean_mcc_window_10": "target_baseline_mcc_window_10",
    })
    summary = summary.merge(baseline, on="mode", how="left")
    summary["delta_mcc_exact"] = summary["mean_mcc_exact"] - summary["baseline_mcc_exact"]
    summary["delta_mcc_window_10"] = summary["mean_mcc_window_10"] - summary["baseline_mcc_window_10"]
    summary["delta_precision_20"] = summary["mean_precision_20"] - summary["baseline_precision_20"]
    summary["delta_constrained_fpr"] = summary["mean_constrained_fpr"] - summary["baseline_constrained_fpr"]
    summary["target_delta_mcc_window_10"] = summary["target_mean_mcc_window_10"] - summary["target_baseline_mcc_window_10"]
    summary["decision"] = summary.apply(decision, axis=1)
    summary = summary.sort_values(["mode", "target_delta_mcc_window_10"], ascending=[True, False])

    results_path = RESULTS_DIR / "pahd_r_temporal_reliability_feature_results.csv"
    summary_path = RESULTS_DIR / "pahd_r_temporal_reliability_feature_summary.csv"
    feature_path = RESULTS_DIR / "pahd_r_temporal_reliability_features.csv"
    report_path = RESULTS_DIR / "pahd_r_temporal_reliability_feature_sweep.md"
    results.to_csv(results_path, index=False)
    summary.to_csv(summary_path, index=False)
    features.to_csv(feature_path, index=False)
    report = [
        "# PAHD-R Temporal Reliability Feature Sweep",
        "",
        "Date: 2026-04-27 KST",
        "",
        "## Scope",
        "",
        "This sweep uses temporal metadata as a low-weight reliability feature for HIV-1/MERS only, not as recurrence/diversity replacement.",
        "",
        "## Temporal Feature Summary",
        "",
        markdown_table(features),
        "",
        "## Results",
        "",
        markdown_table(summary),
        "",
    ]
    report_path.write_text("\n".join(report), encoding="utf-8")
    print(report_path)
    print(summary.round(4).to_string(index=False))


if __name__ == "__main__":
    run()
