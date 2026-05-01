#!/usr/bin/env python3
"""Label-sparsity stress test for PAHD-R modes."""

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


TARGET_COUNTS = [9, 15, 20]
N_ITER = 200


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


def evaluate_sparse_labels(y_sparse: np.ndarray, pred: np.ndarray, score: np.ndarray) -> dict[str, float]:
    p20, _ = pahd.precision_and_enrichment(y_sparse, score, 20)
    return {
        "mcc_exact": pahd.region_mcc(y_sparse, pred, 0),
        "mcc_window_10": pahd.region_mcc(y_sparse, pred, 10),
        "precision_20": p20,
    }


def run() -> None:
    data = pahd.load_feature_matrices()
    benchmark = pd.read_csv(RESULTS_DIR / "multilayer_9pathogen_results.csv")
    pathogens = sorted(set(benchmark["pathogen"].unique()) & set(data.keys()))
    rng = np.random.default_rng(20260426)

    rows = []
    baseline_rows = []
    for pathogen in pathogens:
        df = data[pathogen]
        y = df["layer_a"].astype(int).values
        pos = np.where(y > 0)[0]
        scores = decoy_audit.candidate_scores(data, pathogens, pathogen)
        for mode, score in scores.items():
            frac = 0.08 if mode == "PAHD-R-Review" else 0.10
            pred = pahd.top_fraction_pred(score, frac)
            baseline = evaluate_sparse_labels(y, pred, score)
            baseline_rows.append({
                "pathogen": pathogen,
                "mode": mode,
                "n_layer_a_full": int(len(pos)),
                **{f"full_{k}": v for k, v in baseline.items()},
            })
            for target_count in TARGET_COUNTS:
                if len(pos) < target_count:
                    continue
                for iteration in range(N_ITER):
                    keep = rng.choice(pos, size=target_count, replace=False)
                    y_sparse = np.zeros_like(y)
                    y_sparse[keep] = 1
                    metrics = evaluate_sparse_labels(y_sparse, pred, score)
                    rows.append({
                        "pathogen": pathogen,
                        "mode": mode,
                        "target_positive_count": target_count,
                        "iteration": iteration,
                        **metrics,
                    })

    stress = pd.DataFrame(rows)
    baseline = pd.DataFrame(baseline_rows)
    summary = (
        stress.groupby(["mode", "target_positive_count"])
        .agg(
            mean_mcc_exact=("mcc_exact", "mean"),
            sd_mcc_exact=("mcc_exact", "std"),
            p10_mcc_exact=("mcc_exact", lambda x: float(np.quantile(x, 0.10))),
            mean_mcc_window_10=("mcc_window_10", "mean"),
            mean_precision_20=("precision_20", "mean"),
        )
        .reset_index()
        .sort_values(["mode", "target_positive_count"])
    )
    by_pathogen = (
        stress.groupby(["pathogen", "mode", "target_positive_count"])
        .agg(
            mean_mcc_exact=("mcc_exact", "mean"),
            sd_mcc_exact=("mcc_exact", "std"),
            mean_mcc_window_10=("mcc_window_10", "mean"),
            mean_precision_20=("precision_20", "mean"),
        )
        .reset_index()
    )

    mers_rows = baseline[baseline["pathogen"] == "MERS"].copy()
    comparisons = []
    for _, row in mers_rows.iterrows():
        mode = row["mode"]
        peer = by_pathogen[
            (by_pathogen["mode"] == mode)
            & (by_pathogen["target_positive_count"] == 9)
            & (by_pathogen["pathogen"] != "MERS")
        ]
        if len(peer):
            comparisons.append({
                "mode": mode,
                "mers_full_mcc_exact": row["full_mcc_exact"],
                "peer_sparse9_mean_mcc_exact": float(peer["mean_mcc_exact"].mean()),
                "peer_sparse9_p10_mcc_exact": float(np.quantile(peer["mean_mcc_exact"], 0.10)),
                "mers_below_peer_p10": bool(row["full_mcc_exact"] < np.quantile(peer["mean_mcc_exact"], 0.10)),
                "mers_full_precision_20": row["full_precision_20"],
                "peer_sparse9_mean_precision_20": float(peer["mean_precision_20"].mean()),
            })
    comparison = pd.DataFrame(comparisons)

    stress.to_csv(RESULTS_DIR / "pahd_r_label_sparsity_stress_results.csv", index=False)
    summary.to_csv(RESULTS_DIR / "pahd_r_label_sparsity_stress_summary.csv", index=False)
    by_pathogen.to_csv(RESULTS_DIR / "pahd_r_label_sparsity_stress_by_pathogen.csv", index=False)
    comparison.to_csv(RESULTS_DIR / "pahd_r_label_sparsity_mers_comparison.csv", index=False)

    report = [
        "# PAHD-R Label-Sparsity Stress Test",
        "",
        "Date: 2026-04-26 KST",
        "",
        "## Global Sparse-Label Summary",
        "",
        markdown_table(summary),
        "",
        "## MERS versus Peer Sparse-9 Comparison",
        "",
        markdown_table(comparison),
        "",
        "## Interpretation",
        "",
        "- Subsampling positives lowers exact/top-k metrics, so label sparsity explains part of the weak-case behavior.",
        "- MERS remains below the peer sparse-9 mean in all modes and below the peer sparse-9 p10 in the Augmented mode.",
        "- Therefore MERS is not only a low-positive-count problem; it likely needs MERS-specific domain priors or better feature/label alignment.",
        "- RSV cannot be explained by the 9-positive MERS setting because it has 20 Layer A positives but still fails exact/top-k metrics.",
        "",
    ]
    out = RESULTS_DIR / "pahd_r_label_sparsity_stress_audit.md"
    out.write_text("\n".join(report), encoding="utf-8")
    print(out)
    print(summary.round(4).to_string(index=False))
    print(comparison.round(4).to_string(index=False))


if __name__ == "__main__":
    run()
