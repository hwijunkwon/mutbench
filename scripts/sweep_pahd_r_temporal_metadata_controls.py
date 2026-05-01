#!/usr/bin/env python3
"""PAHD-R time-stratified input-control experiment using staged NCBI metadata.

This is a follow-up experiment only. It uses newly staged accession-level
collection dates for HIV-1 and MERS to test whether temporal equalization of
sequence-derived recurrence/diversity proxies improves final PAHD-R modes.
It does not update thesis claims by itself.
"""

from __future__ import annotations

from collections import defaultdict
from copy import deepcopy
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
TARGETS = ["HIV-1", "MERS"]
ACCESSION_RE = re.compile(r"^([A-Z]{1,4}_?\d+(?:\.\d+)?)\b")
YEAR_RE = re.compile(r"(?<![A-Za-z0-9])((?:19|20)\d{2})(?![A-Za-z0-9])")


def accession_from_header(header: str) -> str:
    match = ACCESSION_RE.search(header)
    return match.group(1) if match else ""


def year_from_text(text: object) -> int | None:
    match = YEAR_RE.search(str(text))
    if match is None:
        return None
    year = int(match.group(1))
    if 1970 <= year <= 2026:
        return year
    return None


def metadata_years() -> dict[str, int]:
    meta = pd.read_csv(META_PATH)
    years = {}
    for row in meta.itertuples():
        year = year_from_text(getattr(row, "collection_date", "")) or year_from_text(getattr(row, "ncbi_year", ""))
        if year is not None and isinstance(row.accession, str):
            years[row.accession] = year
    return years


def temporal_equalized_proxy(pathogen: str, n: int, min_unique_per_year: int = 3) -> tuple[np.ndarray, np.ndarray, dict[str, object]]:
    year_map = metadata_years()
    path = rawseq.FASTA_PATHS[pathogen]
    records = targeted.read_fasta_records(path)
    usable = [(h, s) for h, s in records if len(s) >= n]
    by_year: dict[int, set[str]] = defaultdict(set)
    assigned = 0
    for header, seq in usable:
        accession = accession_from_header(header)
        year = year_map.get(accession)
        if year is None:
            continue
        assigned += 1
        by_year[year].add(seq)
    eligible = {year: sorted(seqs) for year, seqs in by_year.items() if len(seqs) >= min_unique_per_year}
    meta = {
        "pathogen": pathogen,
        "n_usable": len(usable),
        "n_temporal_assigned": assigned,
        "temporal_coverage": assigned / len(usable) if usable else 0.0,
        "n_years": len(by_year),
        "n_eligible_years": len(eligible),
        "min_unique_per_year": min_unique_per_year,
        "proxy_status": "ok" if len(eligible) >= 2 else "insufficient_temporal_bins",
    }
    if len(eligible) < 2:
        return np.zeros(n), np.zeros(n), meta
    variations = []
    entropies = []
    for seqs in eligible.values():
        variation, entropy = targeted.variation_entropy(seqs, n)
        variations.append(variation)
        entropies.append(entropy)
    return np.mean(np.vstack(variations), axis=0), np.mean(np.vstack(entropies), axis=0), meta


def apply_temporal_proxy(
    data: dict[str, pd.DataFrame],
    alpha: float,
    min_unique_per_year: int,
) -> tuple[dict[str, pd.DataFrame], list[dict[str, object]]]:
    out = deepcopy(data)
    metas = []
    for pathogen in TARGETS:
        frame = out[pathogen].copy()
        variation, entropy, meta = temporal_equalized_proxy(pathogen, len(frame), min_unique_per_year=min_unique_per_year)
        meta["alpha"] = alpha
        metas.append(meta)
        if meta["proxy_status"] == "ok" and np.std(variation) > 1e-12:
            frame["freq"] = (1.0 - alpha) * np.nan_to_num(frame["freq"].values, nan=0.0) + alpha * variation
            frame["rare_freq"] = (1.0 - alpha) * np.nan_to_num(frame["rare_freq"].values, nan=0.0) + alpha * variation
            frame["entropy"] = (1.0 - alpha) * np.nan_to_num(frame["entropy"].values, nan=0.0) + alpha * entropy
        out[pathogen] = frame
    return out, metas


def make_variant(base: dict[str, pd.DataFrame], variant: str) -> tuple[dict[str, pd.DataFrame], list[dict[str, object]]]:
    if variant == "baseline":
        return base, []
    if variant == "winsorized_1_99":
        return {p: targeted.winsorize(df) for p, df in base.items()}, []
    match = re.fullmatch(r"time_meta(?:_y([0-9]+))?_alpha_([0-9]+)(?:_winsorized)?", variant)
    if match is None:
        raise ValueError(f"unknown variant: {variant}")
    min_unique_per_year = int(match.group(1) or 3)
    alpha = int(match.group(2)) / 100.0
    out, metas = apply_temporal_proxy(base, alpha, min_unique_per_year=min_unique_per_year)
    if variant.endswith("_winsorized"):
        out = {p: targeted.winsorize(df) for p, df in out.items()}
    return out, metas


def decision(row: pd.Series) -> str:
    if row["variant"] == "baseline":
        return "current_reference"
    if row["variant"] == "winsorized_1_99":
        return "candidate_only_from_prior_round"
    if row["delta_mcc_window_10"] >= 0.015 and row["delta_mcc_exact"] >= -0.010 and row["target_delta_mcc_window_10"] >= -0.020:
        return "candidate_temporal_control"
    if row["delta_mcc_window_10"] <= -0.050 or row["target_delta_mcc_window_10"] <= -0.080:
        return "rejected_temporal_control"
    return "diagnostic_only"


def run() -> None:
    base = pahd.load_feature_matrices()
    pathogens = targeted.primary_pathogens(base)
    variants = [
        "baseline",
        "winsorized_1_99",
        "time_meta_alpha_25",
        "time_meta_alpha_50",
        "time_meta_alpha_100",
        "time_meta_alpha_25_winsorized",
        "time_meta_alpha_50_winsorized",
        "time_meta_y10_alpha_25",
        "time_meta_y10_alpha_50",
        "time_meta_y10_alpha_25_winsorized",
        "time_meta_y10_alpha_50_winsorized",
    ]
    rows = []
    meta_rows = []
    for variant in variants:
        data, metas = make_variant(base, variant)
        meta_rows.extend({"variant": variant, **m} for m in metas)
        for pathogen in pathogens:
            scores = final_scores.candidate_scores(data, pathogens, pathogen)
            for mode in MODES:
                rows.append({
                    "variant": variant,
                    "pathogen": pathogen,
                    "mode": mode,
                    **targeted.evaluate(pathogen, data[pathogen], scores[mode], mode),
                })
    results = pd.DataFrame(rows)
    meta = pd.DataFrame(meta_rows)
    summary = (
        results.groupby(["variant", "mode"])
        .agg(
            mean_mcc_exact=("mcc_exact", "mean"),
            mean_mcc_window_10=("mcc_window_10", "mean"),
            mean_precision_20=("precision_20", "mean"),
            mean_constrained_fpr=("constrained_fpr", "mean"),
            target_mean_mcc_window_10=("mcc_window_10", lambda s: np.nan),
        )
        .reset_index()
    )
    target_summary = (
        results[results["pathogen"].isin(TARGETS)]
        .groupby(["variant", "mode"])
        .agg(target_mean_mcc_window_10=("mcc_window_10", "mean"))
        .reset_index()
    )
    summary = summary.drop(columns=["target_mean_mcc_window_10"]).merge(target_summary, on=["variant", "mode"], how="left")
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
    summary = summary.sort_values(["mode", "mean_mcc_window_10"], ascending=[True, False])

    results_path = RESULTS_DIR / "pahd_r_temporal_metadata_control_results.csv"
    summary_path = RESULTS_DIR / "pahd_r_temporal_metadata_control_summary.csv"
    metadata_path = RESULTS_DIR / "pahd_r_temporal_metadata_control_metadata.csv"
    report_path = RESULTS_DIR / "pahd_r_temporal_metadata_control_report.md"
    results.to_csv(results_path, index=False)
    summary.to_csv(summary_path, index=False)
    meta.to_csv(metadata_path, index=False)

    report = [
        "# PAHD-R Temporal Metadata Control Experiment",
        "",
        "Date: 2026-04-27 KST",
        "",
        "## Scope",
        "",
        (
            "This experiment uses newly staged NCBI collection-date metadata for "
            "HIV-1 and MERS. It is a follow-up data experiment only and is not "
            "automatically incorporated into thesis claims."
        ),
        "",
        "## Metadata",
        "",
        targeted.markdown_table(meta),
        "",
        "## Summary",
        "",
        targeted.markdown_table(summary[[
            "variant",
            "mode",
            "mean_mcc_exact",
            "mean_mcc_window_10",
            "mean_precision_20",
            "mean_constrained_fpr",
            "target_mean_mcc_window_10",
            "delta_mcc_exact",
            "delta_mcc_window_10",
            "target_delta_mcc_window_10",
            "decision",
        ]]),
        "",
        "## Interpretation",
        "",
        (
            "Temporal equalization is now technically feasible from staged metadata. "
            "Adoption still requires the same adversarial criteria as other "
            "algorithm updates: no exact-MCC degradation, positive paired/bootstrapped "
            "region-MCC evidence, and no targeted HIV-1/MERS collapse."
        ),
        "",
    ]
    report_path.write_text("\n".join(report), encoding="utf-8")
    print(report_path)
    print(summary.round(4).to_string(index=False))


if __name__ == "__main__":
    run()
