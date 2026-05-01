#!/usr/bin/env python3
"""Deduplicated raw-sequence sensitivity audit for PAHD-R input signals."""

from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parent.parent
RESULTS_DIR = PROJECT_ROOT / "results" / "mutbench"

import sys

sys.path.insert(0, str(PROJECT_ROOT / "scripts"))
import audit_pahd_r_raw_sequence_stability as rawseq  # noqa: E402

N_BOOT = 200
SUBSAMPLE_FRAC = 0.80


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


def audit_pathogen(pathogen: str, rng: np.random.Generator) -> tuple[dict[str, object], list[dict[str, object]]]:
    path = rawseq.FASTA_PATHS[pathogen]
    seqs = rawseq.read_fasta(path)
    n = rawseq.feature_length(pathogen)
    usable = [seq for seq in seqs if len(seq) >= n]
    unique = sorted(set(usable))
    _, full_var_all = rawseq.consensus_and_variation(usable, n)
    _, full_var_dedup = rawseq.consensus_and_variation(unique, n)
    pred_all = rawseq.top_pred(full_var_all, rawseq.TOP_FRAC)
    pred_dedup = rawseq.top_pred(full_var_dedup, rawseq.TOP_FRAC)

    rows = []
    n_sub = max(2, int(round(len(unique) * SUBSAMPLE_FRAC)))
    for boot_id in range(N_BOOT):
        idx = rng.choice(len(unique), size=n_sub, replace=True)
        sub = [unique[i] for i in idx]
        _, sub_var = rawseq.consensus_and_variation(sub, n)
        pred_sub = rawseq.top_pred(sub_var, rawseq.TOP_FRAC)
        rows.append({
            "pathogen": pathogen,
            "boot_id": boot_id,
            "n_unique_subsample": n_sub,
            "dedup_top_jaccard_vs_dedup_full": rawseq.jaccard(pred_dedup, pred_sub),
            "dedup_top_jaccard_vs_original_full": rawseq.jaccard(pred_all, pred_sub),
            "dedup_spearman_vs_dedup_full": pd.Series(full_var_dedup).corr(pd.Series(sub_var), method="spearman"),
        })
    boot = pd.DataFrame(rows)
    summary = {
        "pathogen": pathogen,
        "n_sequences": len(seqs),
        "n_usable": len(usable),
        "n_unique_usable": len(unique),
        "duplicate_rate_usable": 1.0 - (len(unique) / len(usable) if usable else 0.0),
        "original_vs_dedup_top_jaccard": rawseq.jaccard(pred_all, pred_dedup),
        "original_vs_dedup_spearman": pd.Series(full_var_all).corr(pd.Series(full_var_dedup), method="spearman"),
        "dedup_boot_mean_jaccard": float(boot["dedup_top_jaccard_vs_dedup_full"].mean()),
        "dedup_boot_p05_jaccard": float(boot["dedup_top_jaccard_vs_dedup_full"].quantile(0.05)),
        "dedup_boot_mean_spearman": float(boot["dedup_spearman_vs_dedup_full"].mean()),
    }
    summary["dedup_decision"] = (
        "dedup_changes_top_sites"
        if summary["original_vs_dedup_top_jaccard"] < 0.70
        else "dedup_top_sites_stable"
    )
    return summary, rows


def run() -> None:
    rng = np.random.default_rng(20260427)
    summaries = []
    boot_rows = []
    for pathogen in rawseq.FASTA_PATHS:
        summary, rows = audit_pathogen(pathogen, rng)
        summaries.append(summary)
        boot_rows.extend(rows)
    summary_df = pd.DataFrame(summaries)
    boot_df = pd.DataFrame(boot_rows)

    summary_path = RESULTS_DIR / "pahd_r_dedup_sequence_sensitivity_summary.csv"
    boot_path = RESULTS_DIR / "pahd_r_dedup_sequence_sensitivity_bootstrap.csv"
    report_path = RESULTS_DIR / "pahd_r_dedup_sequence_sensitivity_audit.md"
    summary_df.to_csv(summary_path, index=False)
    boot_df.to_csv(boot_path, index=False)

    changed = summary_df[summary_df["dedup_decision"] == "dedup_changes_top_sites"]
    report = [
        "# PAHD-R Deduplicated Sequence Sensitivity Audit",
        "",
        "Date: 2026-04-27 KST",
        "",
        "## Scope",
        "",
        (
            "This audit asks whether duplicate raw FASTA sequences materially "
            "change the top variation positions used as a proxy for sequence-derived "
            "PAHD-R inputs. It does not recompute PLM, structure, or tree features."
        ),
        "",
        "## Summary",
        "",
        markdown_table(summary_df),
        "",
        "## Deduplication-Sensitive Pathogens",
        "",
        markdown_table(changed) if len(changed) else "No pathogen crossed the top-site sensitivity threshold.",
        "",
        "## Interpretation",
        "",
        (
            "If deduplication changes top variation sites, future raw bootstrap "
            "should collapse duplicates or stratify by sampling time/location before "
            "final PAHD-R feature recomputation."
        ),
        "",
    ]
    report_path.write_text("\n".join(report), encoding="utf-8")
    print(report_path)
    print(summary_df.round(4).to_string(index=False))


if __name__ == "__main__":
    run()
