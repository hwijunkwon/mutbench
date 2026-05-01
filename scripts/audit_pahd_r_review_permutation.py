#!/usr/bin/env python3
"""Permutation audit for the PAHD-R-Review derived mode."""

from __future__ import annotations

from pathlib import Path
import sys

import numpy as np
import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parent.parent
RESULTS_DIR = PROJECT_ROOT / "results" / "mutbench"
sys.path.insert(0, str(PROJECT_ROOT / "scripts"))
import audit_pahd_r_decoy_coordinate_robustness as decoy_audit  # noqa: E402
import run_pahd_r_multi_hypothesis as pahd  # noqa: E402


def markdown_table(frame: pd.DataFrame) -> str:
    text = frame.copy()
    for col in text.columns:
        if pd.api.types.is_float_dtype(text[col]):
            text[col] = text[col].map(lambda x: f"{x:.4f}")
        else:
            text[col] = text[col].astype(str)
    lines = [
        "| " + " | ".join(text.columns) + " |",
        "| " + " | ".join(["---"] * len(text.columns)) + " |",
    ]
    for _, row in text.iterrows():
        lines.append("| " + " | ".join(row[col] for col in text.columns) + " |")
    return "\n".join(lines)


def run(n_perm: int = 200) -> None:
    data = pahd.load_feature_matrices()
    benchmark = pd.read_csv(RESULTS_DIR / "multilayer_9pathogen_results.csv")
    pathogens = sorted(set(benchmark["pathogen"].unique()) & set(data.keys()))
    rng = np.random.default_rng(20260426)

    observed_rows = []
    null_rows = []

    for pathogen in pathogens:
        df = data[pathogen]
        y = df["layer_a"].astype(int).values
        score = decoy_audit.candidate_scores(data, pathogens, pathogen)["PAHD-R-Review"]
        pred = pahd.top_fraction_pred(score, 0.08)
        observed = pahd.region_mcc(y, pred, 0)
        observed_rows.append({
            "strategy": "PAHD-R-Review",
            "pathogen": pathogen,
            "observed_mcc_exact": observed,
            "observed_mcc_window_10": pahd.region_mcc(y, pred, 10),
            "observed_precision_20": pahd.precision_and_enrichment(y, score, 20)[0],
        })
        for perm in range(n_perm):
            y_perm = rng.permutation(y)
            null_rows.append({
                "strategy": "PAHD-R-Review",
                "pathogen": pathogen,
                "perm": perm,
                "null_mcc_exact": pahd.region_mcc(y_perm, pred, 0),
            })

    observed_df = pd.DataFrame(observed_rows)
    null_df = pd.DataFrame(null_rows)
    per_pathogen = (
        null_df.groupby(["strategy", "pathogen"])
        .agg(
            null_mean_mcc=("null_mcc_exact", "mean"),
            null_p95_mcc=("null_mcc_exact", lambda x: float(np.quantile(x, 0.95))),
        )
        .reset_index()
        .merge(observed_df, on=["strategy", "pathogen"], how="left")
    )
    per_pathogen["exceeds_null_p95"] = (
        per_pathogen["observed_mcc_exact"] > per_pathogen["null_p95_mcc"]
    )

    null_global = (
        null_df.groupby(["strategy", "perm"])
        .agg(null_mean_mcc=("null_mcc_exact", "mean"))
        .reset_index()
    )
    observed_global = float(observed_df["observed_mcc_exact"].mean())
    global_summary = pd.DataFrame([{
        "strategy": "PAHD-R-Review",
        "observed_mean_mcc": observed_global,
        "null_mean_mcc": float(null_global["null_mean_mcc"].mean()),
        "null_p95_mean_mcc": float(np.quantile(null_global["null_mean_mcc"], 0.95)),
        "empirical_p_null_ge_observed": float(np.mean(null_global["null_mean_mcc"] >= observed_global)),
        "n_perm": n_perm,
    }])

    observed_df.to_csv(RESULTS_DIR / "pahd_r_review_permutation_observed.csv", index=False)
    null_df.to_csv(RESULTS_DIR / "pahd_r_review_permutation_null.csv", index=False)
    per_pathogen.to_csv(RESULTS_DIR / "pahd_r_review_permutation_per_pathogen.csv", index=False)
    global_summary.to_csv(RESULTS_DIR / "pahd_r_review_permutation_global_summary.csv", index=False)

    report = [
        "# PAHD-R-Review Permutation Audit",
        "",
        "Date: 2026-04-26 KST",
        "",
        "## Global Summary",
        "",
        markdown_table(global_summary),
        "",
        "## Per-Pathogen Summary",
        "",
        markdown_table(per_pathogen.sort_values("pathogen")),
        "",
        "## Interpretation",
        "",
        "- The audit tests whether the Review mode exact-MCC result is reproduced under permuted Layer A labels.",
        "- A global empirical p-value of 0 supports the mode as a real signal rather than a label-permutation artifact.",
        "- Pathogen-level rows that do not exceed the null p95 should remain weak-case caveats.",
        "",
    ]
    out = RESULTS_DIR / "pahd_r_review_permutation_audit.md"
    out.write_text("\n".join(report), encoding="utf-8")
    print(out)
    print(global_summary.round(4).to_string(index=False))
    print(per_pathogen.round(4).to_string(index=False))


if __name__ == "__main__":
    run()
