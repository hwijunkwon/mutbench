#!/usr/bin/env python3
"""Resampling stress test for staged PAHD-R temporal metadata candidates."""

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
N_BOOT = 200


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
        collection_year = year_from_text(getattr(row, "collection_date", ""))
        create_year = year_from_text(getattr(row, "ncbi_create_date", ""))
        year = collection_year or create_year
        if year is not None and isinstance(row.accession, str):
            years[row.accession] = year
    return years


def records_by_year(pathogen: str, n: int) -> dict[int, list[str]]:
    year_map = metadata_years()
    records = targeted.read_fasta_records(rawseq.FASTA_PATHS[pathogen])
    by_year: dict[int, set[str]] = defaultdict(set)
    for header, seq in records:
        if len(seq) < n:
            continue
        year = year_map.get(accession_from_header(header))
        if year is not None:
            by_year[year].add(seq)
    return {year: sorted(seqs) for year, seqs in by_year.items()}


def selected_years(by_year: dict[int, list[str]], scheme: str, rng: np.random.Generator, min_unique: int) -> list[int]:
    eligible = sorted(year for year, seqs in by_year.items() if len(seqs) >= min_unique)
    if not eligible:
        return []
    if scheme == "all_y3":
        return sorted(year for year, seqs in by_year.items() if len(seqs) >= 3)
    if scheme == "all_y10":
        return eligible
    if scheme == "early_half":
        return eligible[: max(2, len(eligible) // 2)]
    if scheme == "late_half":
        return eligible[max(0, len(eligible) // 2):]
    if scheme == "odd_years":
        chosen = [year for year in eligible if year % 2 == 1]
        return chosen if len(chosen) >= 2 else eligible
    if scheme == "even_years":
        chosen = [year for year in eligible if year % 2 == 0]
        return chosen if len(chosen) >= 2 else eligible
    if scheme == "bootstrap_years":
        return list(rng.choice(eligible, size=len(eligible), replace=True))
    raise ValueError(f"unknown scheme: {scheme}")


def proxy_from_years(by_year: dict[int, list[str]], years: list[int], n: int) -> tuple[np.ndarray, np.ndarray]:
    variations = []
    entropies = []
    for year in years:
        variation, entropy = targeted.variation_entropy(by_year[year], n)
        variations.append(variation)
        entropies.append(entropy)
    if not variations:
        return np.zeros(n), np.zeros(n)
    return np.mean(np.vstack(variations), axis=0), np.mean(np.vstack(entropies), axis=0)


def apply_temporal_variant(
    base: dict[str, pd.DataFrame],
    scheme: str,
    rng: np.random.Generator,
    alpha: float = 0.25,
    min_unique: int = 3,
) -> tuple[dict[str, pd.DataFrame], list[dict[str, object]]]:
    out = deepcopy(base)
    meta_rows = []
    for pathogen in TARGETS:
        frame = out[pathogen].copy()
        by_year = records_by_year(pathogen, len(frame))
        years = selected_years(by_year, scheme, rng, min_unique=min_unique)
        variation, entropy = proxy_from_years(by_year, years, len(frame))
        meta_rows.append({
            "scheme": scheme,
            "pathogen": pathogen,
            "min_unique": min_unique,
            "n_years_selected": len(years),
            "year_min": min(years) if years else np.nan,
            "year_max": max(years) if years else np.nan,
            "proxy_status": "ok" if np.std(variation) > 1e-12 else "empty_or_constant",
        })
        if np.std(variation) > 1e-12:
            frame["freq"] = (1.0 - alpha) * np.nan_to_num(frame["freq"].values, nan=0.0) + alpha * variation
            frame["rare_freq"] = (1.0 - alpha) * np.nan_to_num(frame["rare_freq"].values, nan=0.0) + alpha * variation
            frame["entropy"] = (1.0 - alpha) * np.nan_to_num(frame["entropy"].values, nan=0.0) + alpha * entropy
        out[pathogen] = frame
    return {p: targeted.winsorize(df) for p, df in out.items()}, meta_rows


def evaluate_data(data: dict[str, pd.DataFrame], pathogens: list[str], scheme: str, replicate: int) -> list[dict[str, object]]:
    rows = []
    for pathogen in pathogens:
        scores = final_scores.candidate_scores(data, pathogens, pathogen)
        for mode in MODES:
            rows.append({
                "scheme": scheme,
                "replicate": replicate,
                "pathogen": pathogen,
                "mode": mode,
                **targeted.evaluate(pathogen, data[pathogen], scores[mode], mode),
            })
    return rows


def summarize(results: pd.DataFrame) -> pd.DataFrame:
    baseline = (
        results[results["scheme"] == "baseline"]
        .groupby(["pathogen", "mode"])[["mcc_exact", "mcc_window_10", "precision_20", "constrained_fpr"]]
        .mean()
        .reset_index()
        .rename(columns={
            "mcc_exact": "baseline_mcc_exact",
            "mcc_window_10": "baseline_mcc_window_10",
            "precision_20": "baseline_precision_20",
            "constrained_fpr": "baseline_constrained_fpr",
        })
    )
    merged = results.merge(baseline, on=["pathogen", "mode"], how="left")
    for metric in ["mcc_exact", "mcc_window_10", "precision_20", "constrained_fpr"]:
        merged[f"delta_{metric}"] = merged[metric] - merged[f"baseline_{metric}"]
    summary = (
        merged[merged["scheme"] != "baseline"]
        .groupby(["scheme", "mode"])
        .agg(
            mean_delta_mcc_exact=("delta_mcc_exact", "mean"),
            mean_delta_mcc_window_10=("delta_mcc_window_10", "mean"),
            p_delta_mcc_window_10_gt_0=("delta_mcc_window_10", lambda s: float((s > 0).mean())),
            ci_low_delta_mcc_window_10=("delta_mcc_window_10", lambda s: float(np.quantile(s, 0.025))),
            ci_high_delta_mcc_window_10=("delta_mcc_window_10", lambda s: float(np.quantile(s, 0.975))),
            mean_delta_precision_20=("delta_precision_20", "mean"),
            mean_delta_constrained_fpr=("delta_constrained_fpr", "mean"),
            n_rows=("pathogen", "size"),
        )
        .reset_index()
    )
    target = (
        merged[(merged["scheme"] != "baseline") & (merged["pathogen"].isin(TARGETS))]
        .groupby(["scheme", "mode"])
        .agg(target_mean_delta_mcc_window_10=("delta_mcc_window_10", "mean"))
        .reset_index()
    )
    summary = summary.merge(target, on=["scheme", "mode"], how="left")
    summary["decision"] = summary.apply(decision, axis=1)
    return summary.sort_values(["mode", "mean_delta_mcc_window_10"], ascending=[True, False])


def decision(row: pd.Series) -> str:
    if row["mean_delta_mcc_window_10"] >= 0.015 and row["ci_low_delta_mcc_window_10"] > 0 and row["target_mean_delta_mcc_window_10"] >= 0:
        return "strong_candidate"
    if row["mean_delta_mcc_window_10"] >= 0.015 and row["p_delta_mcc_window_10_gt_0"] >= 0.65:
        return "weak_candidate"
    if row["mean_delta_mcc_window_10"] <= -0.03 or row["target_mean_delta_mcc_window_10"] <= -0.08:
        return "reject"
    return "diagnostic"


def run() -> None:
    rng = np.random.default_rng(20260427)
    base = pahd.load_feature_matrices()
    pathogens = targeted.primary_pathogens(base)
    baseline = {p: targeted.winsorize(df) for p, df in base.items()}
    rows = evaluate_data(baseline, pathogens, "baseline", 0)
    meta_rows = []

    deterministic = ["all_y3", "all_y10", "early_half", "late_half", "odd_years", "even_years"]
    for scheme in deterministic:
        min_unique = 10 if scheme == "all_y10" else 3
        data, metas = apply_temporal_variant(base, scheme, rng, min_unique=min_unique)
        rows.extend(evaluate_data(data, pathogens, scheme, 0))
        meta_rows.extend(metas)
    for replicate in range(N_BOOT):
        data, metas = apply_temporal_variant(base, "bootstrap_years", rng, min_unique=3)
        rows.extend(evaluate_data(data, pathogens, "bootstrap_years", replicate))
        meta_rows.extend({"replicate": replicate, **m} for m in metas)

    result_df = pd.DataFrame(rows)
    meta_df = pd.DataFrame(meta_rows)
    summary = summarize(result_df)

    results_path = RESULTS_DIR / "pahd_r_temporal_candidate_resampling_results.csv"
    meta_path = RESULTS_DIR / "pahd_r_temporal_candidate_resampling_metadata.csv"
    summary_path = RESULTS_DIR / "pahd_r_temporal_candidate_resampling_summary.csv"
    report_path = RESULTS_DIR / "pahd_r_temporal_candidate_resampling_audit.md"
    result_df.to_csv(results_path, index=False)
    meta_df.to_csv(meta_path, index=False)
    summary.to_csv(summary_path, index=False)

    report = [
        "# PAHD-R Temporal Candidate Resampling Audit",
        "",
        "Date: 2026-04-27 KST",
        "",
        "## Scope",
        "",
        (
            "This stress test asks whether the staged temporal candidate survives "
            "year resampling, early/late splits, odd/even-year splits, and strict "
            "year-bin filtering. Baseline is winsorized PAHD-R without temporal "
            "proxy replacement."
        ),
        "",
        "## Summary",
        "",
        markdown_table(summary),
        "",
        "## Verdict",
        "",
        (
            "A temporal candidate is only credible if its region-MCC gain remains "
            "positive under resampling and does not degrade the targeted HIV-1/MERS "
            "mean. Weak candidates should remain exploratory and out of thesis "
            "claims."
        ),
        "",
    ]
    report_path.write_text("\n".join(report), encoding="utf-8")
    print(report_path)
    print(summary.round(4).to_string(index=False))


if __name__ == "__main__":
    run()
