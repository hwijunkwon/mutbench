#!/usr/bin/env python3
"""Raw FASTA availability and sequence-subsample stability audit for PAHD-R.

This is deliberately a proxy audit: it tests whether raw sequence variation
signals are stable under sequence subsampling. It does not regenerate PLM,
structure, MEME/FUBAR, or final PAHD-R scores.
"""

from __future__ import annotations

from collections import Counter
from pathlib import Path

import numpy as np
import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parent.parent
RESULTS_DIR = PROJECT_ROOT / "results" / "mutbench"
FEATURE_DIR = RESULTS_DIR / "feature_analysis"

FASTA_PATHS = {
    "SARS-CoV-2": PROJECT_ROOT / "data" / "ncbi_temporal" / "spike_500_subsample.fasta",
    "H3N2": PROJECT_ROOT / "data" / "influenza" / "h3n2_ha_sequences.fasta",
    "Norovirus": PROJECT_ROOT / "data" / "norovirus" / "norovirus_vp1_sequences.fasta",
    "HIV-1": PROJECT_ROOT / "data" / "hiv" / "hiv1_gp120_sequences.fasta",
    "Dengue": PROJECT_ROOT / "data" / "dengue" / "dengue_e_sequences.fasta",
    "RSV": PROJECT_ROOT / "data" / "rsv" / "rsv_f_sequences.fasta",
    "Influenza_B": PROJECT_ROOT / "data" / "influenza" / "influenza_b_ha_sequences.fasta",
    "MERS": PROJECT_ROOT / "data" / "mers" / "mers_spike_sequences.fasta",
    "HCV": PROJECT_ROOT / "data" / "hcv" / "hcv_e2_sequences.fasta",
}

N_BOOT = 200
SUBSAMPLE_FRAC = 0.80
TOP_FRAC = 0.10


def read_fasta(path: Path) -> list[str]:
    records: list[str] = []
    current: list[str] = []
    with path.open(encoding="utf-8") as handle:
        for line in handle:
            line = line.strip()
            if not line:
                continue
            if line.startswith(">"):
                if current:
                    records.append("".join(current).upper())
                    current = []
            else:
                current.append(line)
        if current:
            records.append("".join(current).upper())
    return records


def consensus_and_variation(seqs: list[str], length: int) -> tuple[str, np.ndarray]:
    trimmed = [seq[:length].ljust(length, "-") for seq in seqs]
    consensus = []
    for i in range(length):
        counts = Counter(seq[i] for seq in trimmed if seq[i] not in {"-", "X", "?"})
        consensus.append(counts.most_common(1)[0][0] if counts else "-")
    cons = "".join(consensus)
    variation = np.zeros(length, dtype=float)
    for i, aa in enumerate(cons):
        valid = [seq[i] for seq in trimmed if seq[i] not in {"-", "X", "?"}]
        if valid and aa != "-":
            variation[i] = sum(x != aa for x in valid) / len(valid)
    return cons, variation


def top_pred(score: np.ndarray, frac: float) -> np.ndarray:
    k = max(1, int(round(len(score) * frac)))
    pred = np.zeros(len(score), dtype=bool)
    pred[np.argsort(-score)[:k]] = True
    return pred


def jaccard(a: np.ndarray, b: np.ndarray) -> float:
    union = np.sum(a | b)
    return float(np.sum(a & b) / union) if union else 1.0


def feature_length(pathogen: str) -> int:
    df = pd.read_csv(FEATURE_DIR / f"feature_matrix_{pathogen}.csv")
    return len(df)


def audit_pathogen(pathogen: str, fasta_path: Path, rng: np.random.Generator) -> tuple[dict[str, object], list[dict[str, object]]]:
    if not fasta_path.exists():
        return {
            "pathogen": pathogen,
            "fasta_path": str(fasta_path.relative_to(PROJECT_ROOT)),
            "status": "missing_fasta",
        }, []

    seqs = read_fasta(fasta_path)
    lengths = np.array([len(seq) for seq in seqs], dtype=int)
    feat_len = feature_length(pathogen)
    usable = [seq for seq in seqs if len(seq) >= feat_len]
    unique_ratio = len(set(seqs)) / len(seqs) if seqs else 0.0

    summary: dict[str, object] = {
        "pathogen": pathogen,
        "fasta_path": str(fasta_path.relative_to(PROJECT_ROOT)),
        "status": "ok" if usable else "no_sequence_reaches_feature_length",
        "n_sequences": len(seqs),
        "n_unique_sequences": len(set(seqs)),
        "unique_ratio": unique_ratio,
        "duplicate_rate": 1.0 - unique_ratio,
        "min_length": int(lengths.min()) if len(lengths) else 0,
        "median_length": float(np.median(lengths)) if len(lengths) else 0.0,
        "max_length": int(lengths.max()) if len(lengths) else 0,
        "feature_length": feat_len,
        "n_usable_for_feature_length": len(usable),
    }
    if not usable:
        return summary, []

    _, full_variation = consensus_and_variation(usable, feat_len)
    full_pred = top_pred(full_variation, TOP_FRAC)
    rows = []
    n_sub = max(2, int(round(len(usable) * SUBSAMPLE_FRAC)))
    for boot_id in range(N_BOOT):
        idx = rng.choice(len(usable), size=n_sub, replace=True)
        sub = [usable[i] for i in idx]
        _, sub_variation = consensus_and_variation(sub, feat_len)
        sub_pred = top_pred(sub_variation, TOP_FRAC)
        rows.append({
            "pathogen": pathogen,
            "boot_id": boot_id,
            "subsample_frac": SUBSAMPLE_FRAC,
            "n_subsample": n_sub,
            "top_jaccard_vs_full": jaccard(full_pred, sub_pred),
            "spearman_rank_corr": pd.Series(full_variation).corr(pd.Series(sub_variation), method="spearman"),
        })

    boot_df = pd.DataFrame(rows)
    summary.update({
        "mean_top_jaccard": float(boot_df["top_jaccard_vs_full"].mean()),
        "p05_top_jaccard": float(boot_df["top_jaccard_vs_full"].quantile(0.05)),
        "mean_spearman": float(boot_df["spearman_rank_corr"].mean()),
        "p05_spearman": float(boot_df["spearman_rank_corr"].quantile(0.05)),
        "raw_sequence_stability_status": (
            "pass_proxy"
            if boot_df["top_jaccard_vs_full"].mean() >= 0.70 and boot_df["spearman_rank_corr"].mean() >= 0.80
            else "review_raw_sampling"
        ),
    })
    return summary, rows


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


def run() -> None:
    rng = np.random.default_rng(20260427)
    summaries = []
    boot_rows = []
    for pathogen, path in FASTA_PATHS.items():
        summary, rows = audit_pathogen(pathogen, path, rng)
        summaries.append(summary)
        boot_rows.extend(rows)

    summary_df = pd.DataFrame(summaries)
    boot_df = pd.DataFrame(boot_rows)
    summary_path = RESULTS_DIR / "pahd_r_raw_sequence_stability_summary.csv"
    boot_path = RESULTS_DIR / "pahd_r_raw_sequence_stability_bootstrap.csv"
    report_path = RESULTS_DIR / "pahd_r_raw_sequence_stability_audit.md"
    summary_df.to_csv(summary_path, index=False)
    boot_df.to_csv(boot_path, index=False)

    report = [
        "# PAHD-R Raw Sequence Stability Audit",
        "",
        "Date: 2026-04-27 KST",
        "",
        "## Scope",
        "",
        (
            "This audit checks raw FASTA availability, duplicate burden, length "
            "compatibility with feature matrices, and top-variation stability "
            "under 80% sequence bootstrap. It is a proxy for raw-data robustness, "
            "not a full PAHD-R recomputation."
        ),
        "",
        "## Summary",
        "",
        markdown_table(summary_df),
        "",
        "## Interpretation",
        "",
        (
            "Pathogens marked `review_raw_sampling` need sequence sampling review "
            "before making strong raw-data robustness claims. Passing this proxy "
            "does not validate PLM, structure, or phylogenetic feature stability."
        ),
        "",
    ]
    report_path.write_text("\n".join(report), encoding="utf-8")
    print(report_path)
    print(summary_df[[
        "pathogen",
        "n_sequences",
        "duplicate_rate",
        "mean_top_jaccard",
        "mean_spearman",
        "raw_sequence_stability_status",
    ]].round(4).to_string(index=False))


if __name__ == "__main__":
    run()
