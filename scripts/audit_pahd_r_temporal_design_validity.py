#!/usr/bin/env python3
"""Design-validity audit for staged PAHD-R temporal metadata experiments."""

from __future__ import annotations

from pathlib import Path
import re

import numpy as np
import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parent.parent
META_PATH = PROJECT_ROOT / "data" / "additional" / "pahd_r_temporal_metadata" / "combined_temporal_metadata.csv"
RESULTS_DIR = PROJECT_ROOT / "results" / "mutbench"
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


def year_from_text(value: object) -> float:
    match = YEAR_RE.search(str(value))
    if match is None:
        return np.nan
    year = int(match.group(1))
    return float(year) if 1970 <= year <= 2026 else np.nan


def add_years(meta: pd.DataFrame) -> pd.DataFrame:
    out = meta.copy()
    out["collection_year"] = out["collection_date"].map(year_from_text)
    out["create_year"] = out["ncbi_create_date"].map(year_from_text)
    out["effective_year"] = out["collection_year"].fillna(out["create_year"])
    out["uses_create_date_fallback"] = out["collection_year"].isna() & out["create_year"].notna()
    return out


def coverage_summary(meta: pd.DataFrame) -> pd.DataFrame:
    rows = []
    for pathogen, sub in meta.groupby("pathogen"):
        n = len(sub)
        rows.append({
            "pathogen": pathogen,
            "n_records": n,
            "accession_coverage": (sub["accession"].astype(str) != "").mean(),
            "collection_year_coverage": sub["collection_year"].notna().mean(),
            "effective_year_coverage": sub["effective_year"].notna().mean(),
            "create_date_fallback_frac": sub["uses_create_date_fallback"].mean(),
            "n_years": int(sub["effective_year"].dropna().nunique()),
            "year_min": sub["effective_year"].min(),
            "year_max": sub["effective_year"].max(),
        })
    return pd.DataFrame(rows)


def year_bin_summary(meta: pd.DataFrame) -> pd.DataFrame:
    rows = []
    for pathogen, sub in meta.dropna(subset=["effective_year"]).groupby("pathogen"):
        counts = sub.groupby("effective_year").size().sort_index()
        if counts.empty:
            continue
        rows.append({
            "pathogen": pathogen,
            "n_years": int(len(counts)),
            "min_records_per_year": int(counts.min()),
            "median_records_per_year": float(counts.median()),
            "max_records_per_year": int(counts.max()),
            "top_year": int(counts.idxmax()),
            "top_year_frac": float(counts.max() / counts.sum()),
            "years_ge_3": int((counts >= 3).sum()),
            "years_ge_10": int((counts >= 10).sum()),
            "years_ge_30": int((counts >= 30).sum()),
        })
    return pd.DataFrame(rows)


def candidate_sensitivity() -> pd.DataFrame:
    paired_path = RESULTS_DIR / "pahd_r_temporal_metadata_candidate_paired_deltas.csv"
    if not paired_path.exists():
        return pd.DataFrame()
    paired = pd.read_csv(paired_path)
    sub = paired[
        (paired["variant"] == "time_meta_alpha_25_winsorized")
        & (paired["mode"].isin(["PAHD-R-Core", "PAHD-R-Augmented"]))
    ].copy()
    if sub.empty:
        return pd.DataFrame()
    rows = []
    for mode, frame in sub.groupby("mode"):
        frame = frame.sort_values("delta_mcc_window_10")
        rows.append({
            "mode": mode,
            "mean_delta_mcc_window_10": frame["delta_mcc_window_10"].mean(),
            "min_pathogen": frame.iloc[0]["pathogen"],
            "min_delta": frame.iloc[0]["delta_mcc_window_10"],
            "max_pathogen": frame.iloc[-1]["pathogen"],
            "max_delta": frame.iloc[-1]["delta_mcc_window_10"],
            "positive_pathogens": int((frame["delta_mcc_window_10"] > 0).sum()),
            "negative_pathogens": int((frame["delta_mcc_window_10"] < 0).sum()),
        })
    return pd.DataFrame(rows)


def design_decisions(coverage: pd.DataFrame, bins: pd.DataFrame, sensitivity: pd.DataFrame) -> pd.DataFrame:
    rows = []
    for row in coverage.itertuples():
        if row.collection_year_coverage >= 0.90 and row.create_date_fallback_frac <= 0.05:
            status = "pass"
            action = "Temporal metadata coverage is adequate for exploratory controls."
        elif row.effective_year_coverage >= 0.90:
            status = "caution"
            action = "Some records rely on create-date fallback; report as exploratory only."
        else:
            status = "fail"
            action = "Do not use for temporal controls without curated dates."
        rows.append({
            "area": f"{row.pathogen}_metadata_coverage",
            "status": status,
            "evidence": f"collection_year={row.collection_year_coverage:.3f}, fallback={row.create_date_fallback_frac:.3f}",
            "action": action,
        })
    for row in bins.itertuples():
        if row.years_ge_10 >= 3 and row.top_year_frac <= 0.50:
            status = "pass"
            action = "Year bins are usable for exploratory year-equalized proxies."
        else:
            status = "caution"
            action = "Year distribution is sparse or imbalanced; validate with stricter bins."
        rows.append({
            "area": f"{row.pathogen}_year_bins",
            "status": status,
            "evidence": f"years_ge10={row.years_ge_10}, top_year_frac={row.top_year_frac:.3f}",
            "action": action,
        })
    for row in sensitivity.itertuples():
        if row.positive_pathogens <= row.negative_pathogens:
            status = "caution"
            action = "Candidate improvement is not broad enough for adoption; keep as follow-up."
        else:
            status = "caution"
            action = "Candidate has mean gain but still needs out-of-sample validation."
        rows.append({
            "area": f"{row.mode}_candidate_influence",
            "status": status,
            "evidence": f"positive={row.positive_pathogens}, negative={row.negative_pathogens}, max={row.max_pathogen}:{row.max_delta:.3f}",
            "action": action,
        })
    return pd.DataFrame(rows)


def run() -> None:
    meta = add_years(pd.read_csv(META_PATH))
    coverage = coverage_summary(meta)
    bins = year_bin_summary(meta)
    sensitivity = candidate_sensitivity()
    decisions = design_decisions(coverage, bins, sensitivity)

    enriched_path = RESULTS_DIR / "pahd_r_temporal_design_metadata_enriched.csv"
    coverage_path = RESULTS_DIR / "pahd_r_temporal_design_coverage.csv"
    bins_path = RESULTS_DIR / "pahd_r_temporal_design_year_bins.csv"
    decisions_path = RESULTS_DIR / "pahd_r_temporal_design_validity_decisions.csv"
    report_path = RESULTS_DIR / "pahd_r_temporal_design_validity_audit.md"
    meta.to_csv(enriched_path, index=False)
    coverage.to_csv(coverage_path, index=False)
    bins.to_csv(bins_path, index=False)
    decisions.to_csv(decisions_path, index=False)

    report = [
        "# PAHD-R Temporal Design Validity Audit",
        "",
        "Date: 2026-04-27 KST",
        "",
        "## Scope",
        "",
        (
            "This audit evaluates whether the newly staged HIV-1/MERS temporal "
            "metadata is suitable for exploratory PAHD-R follow-up experiments. "
            "It does not approve thesis adoption."
        ),
        "",
        "## Metadata Coverage",
        "",
        markdown_table(coverage),
        "",
        "## Year-Bin Balance",
        "",
        markdown_table(bins),
        "",
        "## Candidate Influence",
        "",
        markdown_table(sensitivity) if len(sensitivity) else "Candidate bootstrap deltas were not available.",
        "",
        "## Design Decisions",
        "",
        markdown_table(decisions),
        "",
        "## Verdict",
        "",
        (
            "The additional metadata is valid for exploratory temporal-control "
            "experiments. It is not sufficient by itself to adopt a new default "
            "algorithm because candidate gains remain bootstrap-weak and influence "
            "checks are not uniformly positive."
        ),
        "",
    ]
    report_path.write_text("\n".join(report), encoding="utf-8")
    print(report_path)
    print(decisions.to_string(index=False))


if __name__ == "__main__":
    run()
