#!/usr/bin/env python3
"""Robustness and alternative-preprocessing sweep for final PAHD-R modes.

The sweep asks two adversarial questions:

1. Which evidence families are load-bearing for each final PAHD-R mode?
2. Do simple robust preprocessing variants improve over the current baseline?

Layer A labels are used only in leave-one-pathogen-out training statistics and
post-hoc evaluation, following the existing PAHD-R score path.
"""

from __future__ import annotations

from collections import Counter
from copy import deepcopy
from pathlib import Path
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


def primary_pathogens(data: dict[str, pd.DataFrame]) -> list[str]:
    benchmark = pd.read_csv(RESULTS_DIR / "multilayer_9pathogen_results.csv")
    return sorted(set(benchmark["pathogen"].unique()) & set(data.keys()))


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


def neutralize(frame: pd.DataFrame, columns: list[str]) -> pd.DataFrame:
    out = frame.copy()
    for col in columns:
        if col in out:
            vals = np.nan_to_num(out[col].values, nan=0.0)
            out[col] = float(np.median(vals))
    return out


def rank_normalize(frame: pd.DataFrame) -> pd.DataFrame:
    out = frame.copy()
    for col in pahd.FEATURES:
        out[col] = pahd.rank_percentile(np.nan_to_num(out[col].values, nan=0.0))
    return out


def winsorize(frame: pd.DataFrame, lo: float = 0.01, hi: float = 0.99) -> pd.DataFrame:
    out = frame.copy()
    for col in pahd.FEATURES:
        vals = np.nan_to_num(out[col].values, nan=0.0)
        low, high = np.quantile(vals, [lo, hi])
        out[col] = np.clip(vals, low, high)
    return out


def shannon_entropy(chars: list[str]) -> float:
    valid = [c for c in chars if c not in {"-", "X", "?"}]
    if not valid:
        return 0.0
    counts = np.array(list(Counter(valid).values()), dtype=float)
    probs = counts / counts.sum()
    return float(-(probs * np.log2(probs)).sum())


def dedup_sequence_features(pathogen: str, n: int) -> tuple[np.ndarray, np.ndarray]:
    path = rawseq.FASTA_PATHS.get(pathogen)
    if path is None or not path.exists():
        return np.zeros(n), np.zeros(n)
    seqs = rawseq.read_fasta(path)
    usable = sorted({seq for seq in seqs if len(seq) >= n})
    if not usable:
        return np.zeros(n), np.zeros(n)
    consensus, variation = rawseq.consensus_and_variation(usable, n)
    entropy = np.zeros(n, dtype=float)
    for i in range(n):
        entropy[i] = shannon_entropy([seq[i] for seq in usable])
    if entropy.max() > 0:
        entropy = entropy / entropy.max()
    return variation, entropy


def dedup_variation_variant(data: dict[str, pd.DataFrame], pathogens: list[str]) -> dict[str, pd.DataFrame]:
    out = deepcopy(data)
    for pathogen in pathogens:
        frame = out[pathogen].copy()
        variation, entropy = dedup_sequence_features(pathogen, len(frame))
        if np.std(variation) > 1e-12:
            frame["freq"] = variation
            frame["rare_freq"] = variation
            frame["entropy"] = entropy
        out[pathogen] = frame
    return out


def make_variant(data: dict[str, pd.DataFrame], pathogens: list[str], variant: str) -> dict[str, pd.DataFrame]:
    if variant == "baseline":
        return data
    if variant == "rank_normalized":
        return {p: rank_normalize(df) for p, df in data.items()}
    if variant == "winsorized_1_99":
        return {p: winsorize(df) for p, df in data.items()}
    if variant == "dedup_sequence_variation":
        return dedup_variation_variant(data, pathogens)

    groups = {
        "drop_recurrence_diversity": ["freq", "rare_freq", "entropy"],
        "drop_phylo": ["homoplasy", "dnds_proxy"],
        "drop_ai_constraint_semantic": ["esm2_llr", "semantic_change"],
        "drop_structure": ["plddt", "sasa", "grantham"],
    }
    if variant in groups:
        return {p: neutralize(df, groups[variant]) for p, df in data.items()}
    raise ValueError(f"unknown variant: {variant}")


def evaluate(pathogen: str, df: pd.DataFrame, score: np.ndarray, mode: str) -> dict[str, float]:
    frac = 0.08 if mode == "PAHD-R-Review" else 0.10
    y = df["layer_a"].astype(int).values
    pred = pahd.top_fraction_pred(score, frac)
    p20, e20 = pahd.precision_and_enrichment(y, score, 20)
    return {
        "frac": frac,
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
    if row["delta_mcc_window_10"] >= 0.02 and row["delta_mcc_exact"] >= -0.01 and row["delta_constrained_fpr"] <= 0.02:
        return "candidate_preprocessing_improvement"
    if row["delta_mcc_exact"] <= -0.04 or row["delta_mcc_window_10"] <= -0.08:
        return "load_bearing_or_rejected"
    return "diagnostic_only"


def run() -> None:
    base_data = pahd.load_feature_matrices()
    pathogens = primary_pathogens(base_data)
    variants = [
        "baseline",
        "rank_normalized",
        "winsorized_1_99",
        "dedup_sequence_variation",
        "drop_recurrence_diversity",
        "drop_phylo",
        "drop_ai_constraint_semantic",
        "drop_structure",
    ]
    rows = []
    for variant in variants:
        data = make_variant(base_data, pathogens, variant)
        for pathogen in pathogens:
            scores = final_scores.candidate_scores(data, pathogens, pathogen)
            for mode in MODES:
                metrics = evaluate(pathogen, data[pathogen], scores[mode], mode)
                rows.append({
                    "variant": variant,
                    "pathogen": pathogen,
                    "mode": mode,
                    **metrics,
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
    summary["decision"] = summary.apply(decision, axis=1)
    summary = summary.sort_values(["mode", "mean_mcc_window_10", "mean_mcc_exact"], ascending=[True, False, False])

    results_path = RESULTS_DIR / "pahd_r_robustness_variant_results.csv"
    summary_path = RESULTS_DIR / "pahd_r_robustness_variant_summary.csv"
    report_path = RESULTS_DIR / "pahd_r_robustness_variant_sweep.md"
    results.to_csv(results_path, index=False)
    summary.to_csv(summary_path, index=False)

    candidate = summary[summary["decision"] == "candidate_preprocessing_improvement"]
    rejected = summary[summary["decision"] == "load_bearing_or_rejected"]
    report = [
        "# PAHD-R Robustness Variant Sweep",
        "",
        "Date: 2026-04-27 KST",
        "",
        "## Scope",
        "",
        (
            "This sweep tests final PAHD-R modes under robust preprocessing "
            "alternatives and adversarial evidence-family ablations on the "
            "9-pathogen primary benchmark. It is used for model stress testing, "
            "not for unbounded hyperparameter search."
        ),
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
            "mean_coverage_10",
            "delta_mcc_exact",
            "delta_mcc_window_10",
            "delta_precision_20",
            "delta_constrained_fpr",
            "decision",
        ]]),
        "",
        "## Candidate Improvements",
        "",
        markdown_table(candidate) if len(candidate) else "No variant met the candidate-improvement rule.",
        "",
        "## Load-Bearing Or Rejected Variants",
        "",
        markdown_table(rejected) if len(rejected) else "No variant crossed the rejection/load-bearing threshold.",
        "",
        "## Interpretation",
        "",
        (
            "A candidate preprocessing variant must improve region MCC without "
            "materially harming exact MCC or constrained FPR. Ablations that "
            "collapse performance identify evidence families that should not be "
            "removed from the final design."
        ),
        "",
        "## Outputs",
        "",
        f"- `{results_path.relative_to(PROJECT_ROOT)}`",
        f"- `{summary_path.relative_to(PROJECT_ROOT)}`",
        "",
    ]
    report_path.write_text("\n".join(report), encoding="utf-8")
    print(report_path)
    print(summary[[
        "variant",
        "mode",
        "mean_mcc_exact",
        "mean_mcc_window_10",
        "mean_precision_20",
        "mean_constrained_fpr",
        "delta_mcc_window_10",
        "decision",
    ]].round(4).to_string(index=False))


if __name__ == "__main__":
    run()
