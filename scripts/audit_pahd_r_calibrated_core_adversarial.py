#!/usr/bin/env python3
"""Adversarial validation for PAHD-R-Core-Calibrated (reliability_top_8)."""

from __future__ import annotations

from pathlib import Path
import sys

import numpy as np
import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parent.parent
RESULTS_DIR = PROJECT_ROOT / "results" / "mutbench"
sys.path.insert(0, str(PROJECT_ROOT / "scripts"))

import audit_pahd_r_decoy_coordinate_robustness as final_scores  # noqa: E402
import run_pahd_r_multi_hypothesis as pahd  # noqa: E402
import sweep_pahd_r_calibration_reliability as calib  # noqa: E402
import sweep_pahd_r_targeted_dedup_winsorized as targeted  # noqa: E402

N_PERM = 500
N_PERTURB = 300


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


def predict_core_calibrated(data: dict[str, pd.DataFrame], pathogens: list[str], pathogen: str) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    scores = final_scores.candidate_scores(data, pathogens, pathogen)
    ranks = calib.module_ranks(data, pathogens, pathogen)
    score = scores["PAHD-R-Core"]
    reliability = calib.reliability_score("PAHD-R-Core", score, ranks)
    pred = calib.predict_variant(score, reliability, "PAHD-R-Core", "reliability_top_8")
    return score, reliability, pred


def evaluate_pred(pathogen: str, df: pd.DataFrame, score: np.ndarray, pred: np.ndarray, y: np.ndarray | None = None) -> dict[str, float]:
    y_true = df["layer_a"].astype(int).values if y is None else y.astype(int)
    p20, e20 = pahd.precision_and_enrichment(y_true, score, 20)
    return {
        "mcc_exact": pahd.region_mcc(y_true, pred, 0),
        "mcc_window_10": pahd.region_mcc(y_true, pred, 10),
        "precision_20": p20,
        "enrichment_20": e20,
        "constrained_fpr": pahd.constrained_fpr(pathogen, len(df), pred),
        "coverage_10": pahd.expanded_coverage(pred, 10),
        "pred_frac": float(pred.mean()),
    }


def jaccard(a: np.ndarray, b: np.ndarray) -> float:
    union = np.sum(a | b)
    return float(np.sum(a & b) / union) if union else 1.0


def run() -> None:
    rng = np.random.default_rng(20260427)
    data = pahd.load_feature_matrices()
    pathogens = targeted.primary_pathogens(data)

    observed_rows = []
    null_rows = []
    decoy_rows = []
    stability_rows = []
    site_rows = []

    for pathogen in pathogens:
        df = data[pathogen]
        y = df["layer_a"].astype(int).values
        score, reliability, pred = predict_core_calibrated(data, pathogens, pathogen)
        observed = evaluate_pred(pathogen, df, score, pred)
        observed_rows.append({"pathogen": pathogen, "strategy": "PAHD-R-Core-Calibrated", **observed})
        for pos in np.where(pred)[0]:
            site_rows.append({
                "pathogen": pathogen,
                "position": int(pos),
                "score": float(score[pos]),
                "reliability": float(reliability[pos]),
            })

        for perm_id in range(N_PERM):
            y_perm = rng.permutation(y)
            metrics = evaluate_pred(pathogen, df, score, pred, y_perm)
            null_rows.append({"pathogen": pathogen, "perm_id": perm_id, **metrics})

        decoys = {
            "shuffle_score": rng.permutation(score),
            "reverse_score": score[::-1],
            "random_uniform": rng.random(len(score)),
        }
        region_seed = np.zeros(len(score))
        for start in rng.choice(np.arange(len(score)), size=min(10, len(score)), replace=False):
            region_seed[max(0, start - 5): min(len(score), start + 6)] += 1.0
        decoys["random_regions"] = region_seed + 0.05 * rng.random(len(score))
        for decoy_name, decoy_score in decoys.items():
            if decoy_name in {"shuffle_score", "reverse_score"}:
                decoy_rel = reliability
            else:
                decoy_rel = rng.random(len(score))
            decoy_pred = calib.predict_variant(decoy_score, decoy_rel, "PAHD-R-Core", "reliability_top_8")
            metrics = evaluate_pred(pathogen, df, decoy_score, decoy_pred)
            decoy_rows.append({"pathogen": pathogen, "decoy": decoy_name, **metrics})

        for boot_id in range(N_PERTURB):
            noise = rng.normal(0.0, 0.03, size=len(score))
            rel_noise = rng.normal(0.0, 0.03, size=len(reliability))
            noisy_score = score + noise
            noisy_rel = np.clip(reliability + rel_noise, 0.0, 1.0)
            noisy_pred = calib.predict_variant(noisy_score, noisy_rel, "PAHD-R-Core", "reliability_top_8")
            stability_rows.append({
                "pathogen": pathogen,
                "boot_id": boot_id,
                "jaccard_to_base": jaccard(pred, noisy_pred),
                "selection_overlap": float(np.mean(noisy_pred[pred])) if pred.sum() else 0.0,
                **evaluate_pred(pathogen, df, noisy_score, noisy_pred),
            })

    observed_df = pd.DataFrame(observed_rows)
    null_df = pd.DataFrame(null_rows)
    decoy_df = pd.DataFrame(decoy_rows)
    stability_df = pd.DataFrame(stability_rows)
    site_df = pd.DataFrame(site_rows)

    null_summary_rows = []
    for row in observed_df.itertuples():
        sub = null_df[null_df["pathogen"] == row.pathogen]
        null_summary_rows.append({
            "pathogen": row.pathogen,
            "observed_mcc_exact": row.mcc_exact,
            "observed_mcc_window_10": row.mcc_window_10,
            "observed_precision_20": row.precision_20,
            "null_p_exact_ge_observed": float((sub["mcc_exact"] >= row.mcc_exact).mean()),
            "null_p_window_ge_observed": float((sub["mcc_window_10"] >= row.mcc_window_10).mean()),
            "null_p_precision_ge_observed": float((sub["precision_20"] >= row.precision_20).mean()),
            "null_p95_mcc_window_10": float(sub["mcc_window_10"].quantile(0.95)),
        })
    null_summary = pd.DataFrame(null_summary_rows)

    global_summary = pd.DataFrame([{
        "strategy": "PAHD-R-Core-Calibrated",
        "mean_mcc_exact": observed_df["mcc_exact"].mean(),
        "mean_mcc_window_10": observed_df["mcc_window_10"].mean(),
        "mean_precision_20": observed_df["precision_20"].mean(),
        "mean_constrained_fpr": observed_df["constrained_fpr"].mean(),
        "mean_coverage_10": observed_df["coverage_10"].mean(),
        "mean_stability_jaccard": stability_df["jaccard_to_base"].mean(),
        "p05_stability_jaccard": stability_df["jaccard_to_base"].quantile(0.05),
        "pathogens_exact_above_null_p95": int((null_summary["observed_mcc_exact"] > null_df.groupby("pathogen")["mcc_exact"].quantile(0.95).values).sum()),
        "pathogens_window_above_null_p95": int((null_summary["observed_mcc_window_10"] > null_summary["null_p95_mcc_window_10"]).sum()),
    }])

    for name, frame in [
        ("pahd_r_core_calibrated_observed.csv", observed_df),
        ("pahd_r_core_calibrated_null.csv", null_df),
        ("pahd_r_core_calibrated_null_summary.csv", null_summary),
        ("pahd_r_core_calibrated_decoys.csv", decoy_df),
        ("pahd_r_core_calibrated_stability.csv", stability_df),
        ("pahd_r_core_calibrated_site_calls.csv", site_df),
        ("pahd_r_core_calibrated_global_summary.csv", global_summary),
    ]:
        frame.to_csv(RESULTS_DIR / name, index=False)

    decoy_summary = (
        decoy_df.groupby("decoy")
        .agg(
            mean_mcc_exact=("mcc_exact", "mean"),
            mean_mcc_window_10=("mcc_window_10", "mean"),
            mean_precision_20=("precision_20", "mean"),
            mean_constrained_fpr=("constrained_fpr", "mean"),
            mean_coverage_10=("coverage_10", "mean"),
        )
        .reset_index()
    )
    stability_summary = (
        stability_df.groupby("pathogen")
        .agg(
            mean_jaccard=("jaccard_to_base", "mean"),
            p05_jaccard=("jaccard_to_base", lambda s: float(np.quantile(s, 0.05))),
            mean_mcc_exact=("mcc_exact", "mean"),
            mean_mcc_window_10=("mcc_window_10", "mean"),
        )
        .reset_index()
    )

    report_path = RESULTS_DIR / "pahd_r_core_calibrated_adversarial_audit.md"
    report = [
        "# PAHD-R-Core-Calibrated Adversarial Audit",
        "",
        "Date: 2026-04-27 KST",
        "",
        "## Scope",
        "",
        (
            "This audit tests the reliability_top_8 calibrated Core candidate "
            "against label permutations, decoy scores, and score/reliability "
            "perturbations."
        ),
        "",
        "## Global Summary",
        "",
        markdown_table(global_summary),
        "",
        "## Observed Per Pathogen",
        "",
        markdown_table(observed_df),
        "",
        "## Permutation Null Summary",
        "",
        markdown_table(null_summary),
        "",
        "## Decoy Summary",
        "",
        markdown_table(decoy_summary),
        "",
        "## Stability Summary",
        "",
        markdown_table(stability_summary),
        "",
        "## Interpretation",
        "",
        (
            "The candidate should only be promoted if it beats permutation and decoy "
            "controls while preserving acceptable perturbation stability. If a gain "
            "is driven by a few pathogens or fails null checks, keep it candidate-only."
        ),
        "",
    ]
    report_path.write_text("\n".join(report), encoding="utf-8")
    print(report_path)
    print(global_summary.round(4).to_string(index=False))


if __name__ == "__main__":
    run()
