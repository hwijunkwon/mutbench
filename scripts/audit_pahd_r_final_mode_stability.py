#!/usr/bin/env python3
"""Lightweight stability audit for final PAHD-R modes.

This audit creates final-mode site calls for PAHD-R-Core, PAHD-R-Augmented,
and PAHD-R-Review. It intentionally does not tune scores against Layer A
labels; labels are used only for post-hoc metrics.
"""

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


MODES = ["PAHD-R-Core", "PAHD-R-Augmented", "PAHD-R-Review"]
N_PERTURBATIONS = 300


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


def jaccard(a: np.ndarray, b: np.ndarray) -> float:
    inter = np.sum(a & b)
    union = np.sum(a | b)
    return float(inter / union) if union else 1.0


def confidence_label(prob: float) -> str:
    if prob >= 0.70:
        return "high"
    if prob >= 0.40:
        return "moderate"
    return "exploratory"


def perturbation_stability(score: np.ndarray, frac: float, seed: int) -> tuple[np.ndarray, float]:
    rng = np.random.default_rng(seed)
    base_rank = pahd.rank_percentile(score)
    base_pred = pahd.top_fraction_pred(base_rank, frac)
    counts = np.zeros(len(score), dtype=float)
    overlaps = []
    for _ in range(N_PERTURBATIONS):
        noise = rng.normal(0.0, 0.025, size=len(score))
        perturbed = pahd.rank_percentile(base_rank + noise)
        pred = pahd.top_fraction_pred(perturbed, frac)
        counts += pred.astype(float)
        overlaps.append(jaccard(base_pred, pred))
    return counts / N_PERTURBATIONS, float(np.mean(overlaps))


def evaluate(pathogen: str, df: pd.DataFrame, score: np.ndarray, frac: float) -> dict[str, float]:
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


def primary_benchmark_pathogens(data: dict[str, pd.DataFrame]) -> list[str]:
    benchmark = pd.read_csv(RESULTS_DIR / "multilayer_9pathogen_results.csv")
    return sorted(set(benchmark["pathogen"].unique()) & set(data.keys()))


def stability_decision(row: pd.Series) -> str:
    high_rate = row["high_confidence_count"] / max(row["selected_count"], 1)
    if row["mean_jaccard_to_base"] >= 0.75 and high_rate >= 0.50:
        return "stable_for_reporting"
    if row["mean_jaccard_to_base"] >= 0.65 and high_rate >= 0.30:
        return "usable_with_caution"
    return "needs_full_bootstrap_or_redesign"


def run() -> None:
    data = pahd.load_feature_matrices()
    pathogens = primary_benchmark_pathogens(data)
    if not pathogens:
        raise ValueError("No primary benchmark pathogens found.")

    summary_rows = []
    site_rows = []

    for pathogen in pathogens:
        df = data[pathogen]
        scores = final_scores.candidate_scores(data, pathogens, pathogen)
        for mode in MODES:
            frac = 0.08 if mode == "PAHD-R-Review" else 0.10
            score = pahd.rank_percentile(scores[mode])
            pred = pahd.top_fraction_pred(score, frac)
            stability_prob, mean_jaccard = perturbation_stability(
                score,
                frac,
                seed=20260427 + 37 * pathogens.index(pathogen) + MODES.index(mode),
            )
            selected_probs = stability_prob[pred]
            labels = [confidence_label(float(p)) for p in selected_probs]
            metrics = evaluate(pathogen, df, score, frac)
            summary = {
                "pathogen": pathogen,
                "mode": mode,
                "frac": frac,
                "selected_count": int(pred.sum()),
                "mean_selection_prob": float(selected_probs.mean()) if len(selected_probs) else 0.0,
                "median_selection_prob": float(np.median(selected_probs)) if len(selected_probs) else 0.0,
                "min_selection_prob": float(selected_probs.min()) if len(selected_probs) else 0.0,
                "high_confidence_count": int(sum(label == "high" for label in labels)),
                "moderate_count": int(sum(label == "moderate" for label in labels)),
                "exploratory_count": int(sum(label == "exploratory" for label in labels)),
                "mean_jaccard_to_base": mean_jaccard,
                **metrics,
            }
            summary_rows.append(summary)

            order = np.argsort(-score)
            rank_by_pos = np.empty(len(score), dtype=int)
            rank_by_pos[order] = np.arange(1, len(score) + 1)
            for pos in np.where(pred)[0]:
                site_rows.append({
                    "pathogen": pathogen,
                    "mode": mode,
                    "position": int(df.iloc[pos]["position"]),
                    "index": int(pos),
                    "score": float(score[pos]),
                    "score_rank": int(rank_by_pos[pos]),
                    "stability_prob": float(stability_prob[pos]),
                    "confidence": confidence_label(float(stability_prob[pos])),
                    "layer_a_label": int(df.iloc[pos]["layer_a"]),
                })

    summary_df = pd.DataFrame(summary_rows)
    summary_df["stability_decision"] = summary_df.apply(stability_decision, axis=1)
    site_df = pd.DataFrame(site_rows)

    mode_summary = (
        summary_df.groupby("mode")
        .agg(
            mean_selection_prob=("mean_selection_prob", "mean"),
            mean_jaccard_to_base=("mean_jaccard_to_base", "mean"),
            high_confidence_rate=("high_confidence_count", lambda s: float(s.sum() / summary_df.loc[s.index, "selected_count"].sum())),
            mean_mcc_exact=("mcc_exact", "mean"),
            mean_mcc_window_10=("mcc_window_10", "mean"),
            mean_precision_20=("precision_20", "mean"),
            mean_constrained_fpr=("constrained_fpr", "mean"),
            stable_pathogens=("stability_decision", lambda s: int((s == "stable_for_reporting").sum())),
            caution_pathogens=("stability_decision", lambda s: int((s == "usable_with_caution").sum())),
            redesign_pathogens=("stability_decision", lambda s: int((s == "needs_full_bootstrap_or_redesign").sum())),
        )
        .reset_index()
        .sort_values(["mean_jaccard_to_base", "mean_mcc_window_10"], ascending=False)
    )

    summary_path = RESULTS_DIR / "pahd_r_final_mode_stability_summary.csv"
    site_path = RESULTS_DIR / "pahd_r_final_mode_site_calls.csv"
    mode_path = RESULTS_DIR / "pahd_r_final_mode_stability_by_mode.csv"
    report_path = RESULTS_DIR / "pahd_r_final_mode_stability_audit.md"
    summary_df.to_csv(summary_path, index=False)
    site_df.to_csv(site_path, index=False)
    mode_summary.to_csv(mode_path, index=False)

    report = [
        "# PAHD-R Final-Mode Stability Audit",
        "",
        "Date: 2026-04-27 KST",
        "",
        "## Scope",
        "",
        (
            "This round regenerates site calls for the final PAHD-R-Core, "
            "PAHD-R-Augmented, and PAHD-R-Review modes. Stability is measured "
            "with score perturbation only; Layer A labels are used after ranking "
            "for metrics, not for score fitting or candidate selection."
        ),
        (
            f"The primary evaluation cohort is fixed to the current benchmark "
            f"file: {len(pathogens)} pathogens from `multilayer_9pathogen_results.csv`."
        ),
        "",
        "## Mode Summary",
        "",
        markdown_table(mode_summary),
        "",
        "## Pathogen-Level Summary",
        "",
        markdown_table(summary_df.sort_values(["pathogen", "mode"])),
        "",
        "## Interpretation",
        "",
        (
            "The output replaces the older final-site-call table for reporting "
            "purposes because it uses the final PAHD-R mode names and score paths."
        ),
        (
            "This is not a substitute for full sequence/tree bootstrap stability. "
            "Any mode-pathogen pair marked `needs_full_bootstrap_or_redesign` "
            "should remain cautious in the thesis and PPT."
        ),
        "",
        "## Outputs",
        "",
        f"- `{summary_path.relative_to(PROJECT_ROOT)}`",
        f"- `{mode_path.relative_to(PROJECT_ROOT)}`",
        f"- `{site_path.relative_to(PROJECT_ROOT)}`",
        "",
    ]
    report_path.write_text("\n".join(report), encoding="utf-8")
    print(report_path)
    print(mode_summary.round(4).to_string(index=False))


if __name__ == "__main__":
    run()
