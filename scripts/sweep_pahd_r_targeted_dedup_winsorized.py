#!/usr/bin/env python3
"""Targeted dedup/time-aware sequence-feature sweep for PAHD-R.

This experiment follows up the raw-sequence adversarial audit. It asks whether
the two dedup-sensitive pathogens, HIV-1 and MERS, benefit from replacing only
their recurrence/diversity inputs with deduplicated sequence-derived proxies,
and whether the earlier winsorized preprocessing candidate survives that
stricter input-control setting.
"""

from __future__ import annotations

from collections import Counter, defaultdict
from copy import deepcopy
from pathlib import Path
import re
import sys

import numpy as np
import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parent.parent
RESULTS_DIR = PROJECT_ROOT / "results" / "mutbench"
sys.path.insert(0, str(PROJECT_ROOT / "scripts"))

import audit_pahd_r_decoy_coordinate_robustness as final_scores  # noqa: E402
import audit_pahd_r_raw_sequence_stability as rawseq  # noqa: E402
import run_pahd_r_multi_hypothesis as pahd  # noqa: E402

MODES = ["PAHD-R-Core", "PAHD-R-Augmented", "PAHD-R-Review"]
TARGETS = ["HIV-1", "MERS"]
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


def primary_pathogens(data: dict[str, pd.DataFrame]) -> list[str]:
    benchmark = pd.read_csv(RESULTS_DIR / "multilayer_9pathogen_results.csv")
    return sorted(set(benchmark["pathogen"].unique()) & set(data.keys()))


def read_fasta_records(path: Path) -> list[tuple[str, str]]:
    records: list[tuple[str, str]] = []
    header: str | None = None
    seq_parts: list[str] = []
    for raw in path.read_text(encoding="utf-8").splitlines():
        line = raw.strip()
        if not line:
            continue
        if line.startswith(">"):
            if header is not None:
                records.append((header, "".join(seq_parts).upper()))
            header = line[1:]
            seq_parts = []
        else:
            seq_parts.append(line)
    if header is not None:
        records.append((header, "".join(seq_parts).upper()))
    return records


def extract_year(header: str) -> int | None:
    match = YEAR_RE.search(header)
    if match is None:
        return None
    year = int(match.group(1))
    if 1970 <= year <= 2026:
        return year
    return None


def shannon_entropy(chars: list[str]) -> float:
    valid = [c for c in chars if c not in {"-", "X", "?", "J", "B", "Z"}]
    if not valid:
        return 0.0
    counts = np.array(list(Counter(valid).values()), dtype=float)
    probs = counts / counts.sum()
    return float(-(probs * np.log2(probs)).sum())


def variation_entropy(seqs: list[str], n: int) -> tuple[np.ndarray, np.ndarray]:
    if not seqs:
        return np.zeros(n), np.zeros(n)
    _, variation = rawseq.consensus_and_variation(seqs, n)
    entropy = np.zeros(n, dtype=float)
    for pos in range(n):
        entropy[pos] = shannon_entropy([seq[pos] for seq in seqs])
    if entropy.max() > 0:
        entropy = entropy / entropy.max()
    return variation, entropy


def sequence_proxy(pathogen: str, n: int, mode: str) -> tuple[np.ndarray, np.ndarray, dict[str, object]]:
    path = rawseq.FASTA_PATHS.get(pathogen)
    if path is None or not path.exists():
        return np.zeros(n), np.zeros(n), {"proxy_status": "missing_fasta"}
    records = read_fasta_records(path)
    usable = [(h, s) for h, s in records if len(s) >= n]
    unique_by_seq = {s: h for h, s in usable}
    unique = sorted(unique_by_seq)
    years = defaultdict(list)
    for header, seq in usable:
        year = extract_year(header)
        if year is not None:
            years[year].append(seq)
    assigned = sum(len(v) for v in years.values())
    meta = {
        "proxy_status": "ok",
        "n_records": len(records),
        "n_usable": len(usable),
        "n_unique": len(unique),
        "duplicate_rate": 1.0 - (len(unique) / len(usable) if usable else 0.0),
        "year_assigned_frac": assigned / len(usable) if usable else 0.0,
        "n_years": len(years),
    }
    if mode == "dedup":
        variation, entropy = variation_entropy(unique, n)
        return variation, entropy, meta
    if mode == "time_equalized":
        eligible_years = {y: sorted(set(seqs)) for y, seqs in years.items() if len(set(seqs)) >= 3}
        meta["n_eligible_years"] = len(eligible_years)
        if meta["year_assigned_frac"] < 0.20 or len(eligible_years) < 2:
            meta["proxy_status"] = "insufficient_time_metadata"
            return np.zeros(n), np.zeros(n), meta
        variations = []
        entropies = []
        for seqs in eligible_years.values():
            variation, entropy = variation_entropy(seqs, n)
            variations.append(variation)
            entropies.append(entropy)
        return np.mean(np.vstack(variations), axis=0), np.mean(np.vstack(entropies), axis=0), meta
    raise ValueError(f"unknown sequence proxy mode: {mode}")


def winsorize(frame: pd.DataFrame, lo: float = 0.01, hi: float = 0.99) -> pd.DataFrame:
    out = frame.copy()
    for col in pahd.FEATURES:
        vals = np.nan_to_num(out[col].values, nan=0.0)
        low, high = np.quantile(vals, [lo, hi])
        out[col] = np.clip(vals, low, high)
    return out


def apply_targeted_sequence_proxy(
    data: dict[str, pd.DataFrame],
    proxy_mode: str,
    alpha: float,
    targets: list[str],
) -> tuple[dict[str, pd.DataFrame], list[dict[str, object]]]:
    out = deepcopy(data)
    metadata = []
    for pathogen in targets:
        if pathogen not in out:
            continue
        frame = out[pathogen].copy()
        variation, entropy, meta = sequence_proxy(pathogen, len(frame), proxy_mode)
        meta = {"pathogen": pathogen, "proxy_mode": proxy_mode, "alpha": alpha, **meta}
        metadata.append(meta)
        if meta["proxy_status"] != "ok" or np.std(variation) <= 1e-12:
            out[pathogen] = frame
            continue
        frame["freq"] = (1.0 - alpha) * np.nan_to_num(frame["freq"].values, nan=0.0) + alpha * variation
        frame["rare_freq"] = (1.0 - alpha) * np.nan_to_num(frame["rare_freq"].values, nan=0.0) + alpha * variation
        frame["entropy"] = (1.0 - alpha) * np.nan_to_num(frame["entropy"].values, nan=0.0) + alpha * entropy
        out[pathogen] = frame
    return out, metadata


def make_variant(data: dict[str, pd.DataFrame], variant: str) -> tuple[dict[str, pd.DataFrame], list[dict[str, object]]]:
    if variant == "baseline":
        return data, []
    if variant == "winsorized_1_99":
        return {p: winsorize(df) for p, df in data.items()}, []

    match = re.fullmatch(r"(dedup|time)_alpha_([0-9]+)(?:_winsorized)?", variant)
    if match is None:
        raise ValueError(f"unknown variant: {variant}")
    proxy_mode = "dedup" if match.group(1) == "dedup" else "time_equalized"
    alpha = int(match.group(2)) / 100.0
    out, metadata = apply_targeted_sequence_proxy(data, proxy_mode, alpha, TARGETS)
    if variant.endswith("_winsorized"):
        out = {p: winsorize(df) for p, df in out.items()}
    return out, metadata


def evaluate(pathogen: str, df: pd.DataFrame, score: np.ndarray, mode: str) -> dict[str, float]:
    frac = 0.08 if mode == "PAHD-R-Review" else 0.10
    y = df["layer_a"].astype(int).values
    pred = pahd.top_fraction_pred(score, frac)
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
    if str(row["variant"]).startswith("time_") and int(row["effective_proxy_targets"]) == 0:
        return "metadata_only_insufficient_time"
    if (
        row["delta_mcc_window_10"] >= 0.015
        and row["delta_mcc_exact"] >= -0.010
        and row["delta_constrained_fpr"] <= 0.020
        and row["target_delta_mcc_window_10"] >= -0.020
    ):
        return "candidate_input_control"
    if row["delta_mcc_window_10"] <= -0.080 or row["target_delta_mcc_window_10"] <= -0.080:
        return "rejected_input_control"
    return "diagnostic_only"


def run() -> None:
    base_data = pahd.load_feature_matrices()
    pathogens = primary_pathogens(base_data)
    variants = [
        "baseline",
        "winsorized_1_99",
        "dedup_alpha_25",
        "dedup_alpha_50",
        "dedup_alpha_100",
        "dedup_alpha_25_winsorized",
        "dedup_alpha_50_winsorized",
        "time_alpha_50",
        "time_alpha_50_winsorized",
    ]
    rows = []
    metadata_rows = []
    for variant in variants:
        data, metadata = make_variant(base_data, variant)
        metadata_rows.extend({"variant": variant, **row} for row in metadata)
        for pathogen in pathogens:
            scores = final_scores.candidate_scores(data, pathogens, pathogen)
            for mode in MODES:
                rows.append({
                    "variant": variant,
                    "pathogen": pathogen,
                    "mode": mode,
                    **evaluate(pathogen, data[pathogen], scores[mode], mode),
                })

    results = pd.DataFrame(rows)
    metadata_df = pd.DataFrame(metadata_rows)
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
        .agg(target_mean_mcc_window_10=("mcc_window_10", "mean"))
        .reset_index()
    )
    summary = summary.merge(target_summary, on=["variant", "mode"], how="left")
    if len(metadata_df):
        effective = (
            metadata_df[metadata_df["proxy_status"] == "ok"]
            .groupby("variant")
            .size()
            .reset_index(name="effective_proxy_targets")
        )
        summary = summary.merge(effective, on="variant", how="left")
    else:
        summary["effective_proxy_targets"] = 0
    summary["effective_proxy_targets"] = summary["effective_proxy_targets"].fillna(0).astype(int)
    baseline = summary[summary["variant"] == "baseline"][
        [
            "mode",
            "mean_mcc_exact",
            "mean_mcc_window_10",
            "mean_precision_20",
            "mean_constrained_fpr",
            "mean_coverage_10",
            "target_mean_mcc_window_10",
        ]
    ].rename(columns={
        "mean_mcc_exact": "baseline_mcc_exact",
        "mean_mcc_window_10": "baseline_mcc_window_10",
        "mean_precision_20": "baseline_precision_20",
        "mean_constrained_fpr": "baseline_constrained_fpr",
        "mean_coverage_10": "baseline_coverage_10",
        "target_mean_mcc_window_10": "target_baseline_mcc_window_10",
    })
    summary = summary.merge(baseline, on="mode", how="left")
    summary["delta_mcc_exact"] = summary["mean_mcc_exact"] - summary["baseline_mcc_exact"]
    summary["delta_mcc_window_10"] = summary["mean_mcc_window_10"] - summary["baseline_mcc_window_10"]
    summary["delta_precision_20"] = summary["mean_precision_20"] - summary["baseline_precision_20"]
    summary["delta_constrained_fpr"] = summary["mean_constrained_fpr"] - summary["baseline_constrained_fpr"]
    summary["target_delta_mcc_window_10"] = summary["target_mean_mcc_window_10"] - summary["target_baseline_mcc_window_10"]
    summary["decision"] = summary.apply(decision, axis=1)
    summary = summary.sort_values(["mode", "mean_mcc_window_10", "mean_mcc_exact"], ascending=[True, False, False])

    results_path = RESULTS_DIR / "pahd_r_targeted_dedup_winsorized_results.csv"
    summary_path = RESULTS_DIR / "pahd_r_targeted_dedup_winsorized_summary.csv"
    metadata_path = RESULTS_DIR / "pahd_r_targeted_dedup_winsorized_metadata.csv"
    report_path = RESULTS_DIR / "pahd_r_targeted_dedup_winsorized_sweep.md"
    results.to_csv(results_path, index=False)
    summary.to_csv(summary_path, index=False)
    metadata_df.to_csv(metadata_path, index=False)

    report = [
        "# PAHD-R Targeted Dedup/Time/Winsorized Sweep",
        "",
        "Date: 2026-04-27 KST",
        "",
        "## Scope",
        "",
        (
            "This sweep targets HIV-1 and MERS because the deduplicated raw-sequence "
            "audit showed their top variation sites are sensitive to duplicate "
            "handling. Only recurrence/diversity inputs (`freq`, `rare_freq`, "
            "`entropy`) are blended with deduplicated or time-equalized sequence "
            "proxies; PLM, structure, phylogeny, and labels are unchanged."
        ),
        "",
        "## Input Metadata",
        "",
        markdown_table(metadata_df) if len(metadata_df) else "No targeted metadata rows were generated.",
        "",
        "## Summary",
        "",
        markdown_table(summary[[
            "variant",
            "mode",
            "mean_mcc_exact",
            "mean_mcc_window_10",
            "mean_precision_20",
            "mean_constrained_fpr",
            "target_mean_mcc_window_10",
            "effective_proxy_targets",
            "delta_mcc_exact",
            "delta_mcc_window_10",
            "target_delta_mcc_window_10",
            "delta_constrained_fpr",
            "decision",
        ]]),
        "",
        "## Interpretation",
        "",
        (
            "A candidate must improve mean MCC +/-10 without materially degrading "
            "exact MCC, constrained FPR, or the targeted HIV-1/MERS mean. Time "
            "equalization is only interpretable when header year coverage is "
            "sufficient; otherwise it is retained as a metadata audit rather than "
            "a performance claim."
        ),
        "",
    ]
    report_path.write_text("\n".join(report), encoding="utf-8")
    print(report_path)
    print(summary.round(4).to_string(index=False))


if __name__ == "__main__":
    run()
