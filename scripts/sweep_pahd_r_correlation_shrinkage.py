#!/usr/bin/env python3
"""Correlation-aware shrinkage candidates for PAHD-R-Core.

The data-processing audit found strong redundancy among recurrence/diversity
features and dN/dS proxy features.  This sweep tests whether reducing that
double-counting improves PAHD-R without using target labels for fitting.
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
import sweep_pahd_r_calibration_reliability as calibration  # noqa: E402


OUT_RESULTS = RESULTS_DIR / "pahd_r_correlation_shrinkage_results.csv"
OUT_SUMMARY = RESULTS_DIR / "pahd_r_correlation_shrinkage_summary.csv"
OUT_REPORT = RESULTS_DIR / "pahd_r_correlation_shrinkage_sweep.md"

CORE_MODULES = ["recurrence", "diversity", "phylo", "structure_non_ai"]


def markdown_table(frame: pd.DataFrame) -> str:
    if frame.empty:
        return "_No rows._"
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
    return sorted(set(benchmark["pathogen"].unique()) & set(data))


def concat_train_module_scores(
    data: dict[str, pd.DataFrame],
    pathogens: list[str],
    target: str,
    signs: dict[str, float],
) -> pd.DataFrame:
    parts = []
    for pathogen in pathogens:
        if pathogen == target:
            continue
        parts.append(pahd.non_ai_module_scores(data[pathogen], signs)[CORE_MODULES])
    return pd.concat(parts, ignore_index=True)


def module_redundancy_penalty(train_scores: pd.DataFrame) -> dict[str, float]:
    corr = train_scores.corr(method="spearman").abs().fillna(0.0)
    penalties = {}
    for module in CORE_MODULES:
        others = [m for m in CORE_MODULES if m != module]
        penalties[module] = float(corr.loc[module, others].mean())
    return penalties


def shrink_weights(weights: dict[str, float], penalties: dict[str, float], strength: float) -> dict[str, float]:
    shrunk = {
        module: weight / (1.0 + strength * penalties.get(module, 0.0))
        for module, weight in weights.items()
    }
    return pahd.normalize_weights(shrunk)


def residualize(values: np.ndarray, base: np.ndarray) -> np.ndarray:
    x = np.asarray(base, dtype=float)
    y = np.asarray(values, dtype=float)
    if np.std(x) < 1e-12 or np.std(y) < 1e-12:
        return y
    x0 = x - x.mean()
    beta = float(np.dot(x0, y - y.mean()) / max(np.dot(x0, x0), 1e-12))
    return y - beta * x0


def core_shrinkage_scores(
    data: dict[str, pd.DataFrame],
    pathogens: list[str],
    target: str,
) -> dict[str, np.ndarray]:
    train_data = {p: df for p, df in data.items() if p != target and p in pathogens}
    signs = pahd.compute_feature_signs(train_data)
    effects = pahd.compute_feature_effects(train_data)
    base_weights = pahd.learned_non_ai_weights(effects)
    train_scores = concat_train_module_scores(data, pathogens, target, signs)
    penalties = module_redundancy_penalty(train_scores)

    df = data[target]
    scores = pahd.non_ai_module_scores(df, signs)[CORE_MODULES].copy()
    out: dict[str, np.ndarray] = {}
    phylo = scores["phylo"].values
    cluster = pahd.local_background_cluster_score(
        scores["recurrence"].values,
        seed=400 + pathogens.index(target),
    )

    def h18_like(learned_score: np.ndarray) -> np.ndarray:
        reliability = pahd.cluster_reliability(cluster, phylo, learned_score)
        cluster_w = 0.15 + 0.45 * reliability
        return (
            (1.0 - cluster_w - 0.25) * pahd.rank_percentile(learned_score)
            + cluster_w * pahd.rank_percentile(cluster)
            + 0.25 * pahd.rank_percentile(phylo)
        )

    for strength in [0.5, 1.0, 1.5, 2.0]:
        weights = shrink_weights(base_weights, penalties, strength)
        learned = pahd.combine_modules(scores, weights)
        out[f"corr_weight_shrink_{strength:.1f}"] = learned
        out[f"h18_corr_weight_shrink_{strength:.1f}"] = h18_like(learned)

    residual_scores = scores.copy()
    residual_scores["diversity"] = residualize(scores["diversity"].values, scores["recurrence"].values)
    residual_scores["phylo"] = residualize(scores["phylo"].values, scores["recurrence"].values)
    residual_learned = pahd.combine_modules(residual_scores, base_weights)
    out["residualize_diversity_phylo_vs_recurrence"] = residual_learned
    out["h18_residualize_diversity_phylo_vs_recurrence"] = h18_like(residual_learned)

    seq_evolution = (
        0.40 * pahd.rank_percentile(scores["recurrence"].values)
        + 0.25 * pahd.rank_percentile(scores["diversity"].values)
        + 0.35 * pahd.rank_percentile(scores["phylo"].values)
    )
    structure = pahd.rank_percentile(scores["structure_non_ai"].values)
    for seq_weight in [0.60, 0.70, 0.80, 0.90]:
        collapsed = (
            seq_weight * seq_evolution + (1.0 - seq_weight) * structure
        )
        out[f"collapsed_seq_evolution_{int(seq_weight * 100)}"] = collapsed
        out[f"h18_collapsed_seq_evolution_{int(seq_weight * 100)}"] = h18_like(collapsed)

    return out


def predict(score: np.ndarray, reliability: np.ndarray, selector: str) -> np.ndarray:
    if selector == "top10":
        return pahd.top_fraction_pred(score, 0.10)
    if selector == "top8":
        return pahd.top_fraction_pred(score, 0.08)
    if selector == "reliability_top8":
        combined = 0.70 * pahd.rank_percentile(score) + 0.30 * pahd.rank_percentile(reliability)
        return pahd.top_fraction_pred(combined, 0.08)
    if selector == "reliability_top10":
        combined = 0.70 * pahd.rank_percentile(score) + 0.30 * pahd.rank_percentile(reliability)
        return pahd.top_fraction_pred(combined, 0.10)
    raise ValueError(selector)


def evaluate(pathogen: str, df: pd.DataFrame, score: np.ndarray, pred: np.ndarray) -> dict[str, float]:
    y = df["layer_a"].astype(int).values
    p20, e20 = pahd.precision_and_enrichment(y, score, 20)
    return {
        "n_predicted": int(pred.sum()),
        "pred_frac": float(pred.mean()),
        "mcc_exact": pahd.region_mcc(y, pred, 0),
        "mcc_window_10": pahd.region_mcc(y, pred, 10),
        "precision_20": p20,
        "enrichment_20": e20,
        "constrained_fpr": pahd.constrained_fpr(pathogen, len(df), pred),
        "coverage_10": pahd.expanded_coverage(pred, 10),
    }


def decision(row: pd.Series) -> str:
    if row["entry"] == "PAHD-R-Core":
        return "current_default"
    if row["entry"] == "PAHD-R-Core-Calibrated":
        return "existing_candidate"
    if (
        row["delta_mcc_exact_vs_core"] > 0
        and row["delta_mcc_window_10_vs_core"] > 0
        and row["delta_precision_20_vs_core"] >= 0
        and row["delta_constrained_fpr_vs_core"] <= 0
    ):
        return "candidate"
    if (
        row["delta_mcc_exact_vs_core_calibrated"] > 0
        and row["delta_mcc_window_10_vs_core_calibrated"] >= 0
        and row["delta_constrained_fpr_vs_core_calibrated"] <= 0
    ):
        return "candidate_beats_calibrated"
    if row["delta_mcc_window_10_vs_core"] < -0.05 or row["delta_precision_20_vs_core"] < -0.05:
        return "reject"
    return "diagnostic_only"


def run() -> None:
    data = pahd.load_feature_matrices()
    pathogens = primary_pathogens(data)
    rows = []
    selectors = ["top10", "top8", "reliability_top8", "reliability_top10"]

    for pathogen in pathogens:
        df = data[pathogen]
        baseline_scores = final_scores.candidate_scores(data, pathogens, pathogen)
        ranks = calibration.module_ranks(data, pathogens, pathogen)

        core_score = baseline_scores["PAHD-R-Core"]
        core_rel = calibration.reliability_score("PAHD-R-Core", core_score, ranks)
        rows.append(
            {
                "pathogen": pathogen,
                "entry": "PAHD-R-Core",
                "score_variant": "baseline",
                "selector": "top10",
                **evaluate(pathogen, df, core_score, pahd.top_fraction_pred(core_score, 0.10)),
            }
        )
        rows.append(
            {
                "pathogen": pathogen,
                "entry": "PAHD-R-Core-Calibrated",
                "score_variant": "baseline",
                "selector": "reliability_top8",
                **evaluate(pathogen, df, core_score, predict(core_score, core_rel, "reliability_top8")),
            }
        )

        for score_variant, score in core_shrinkage_scores(data, pathogens, pathogen).items():
            rel = calibration.reliability_score("PAHD-R-Core", score, ranks)
            for selector in selectors:
                rows.append(
                    {
                        "pathogen": pathogen,
                        "entry": f"{score_variant}:{selector}",
                        "score_variant": score_variant,
                        "selector": selector,
                        **evaluate(pathogen, df, score, predict(score, rel, selector)),
                    }
                )

    results = pd.DataFrame(rows)
    summary = (
        results.groupby(["entry", "score_variant", "selector"])
        .agg(
            mean_mcc_exact=("mcc_exact", "mean"),
            mean_mcc_window_10=("mcc_window_10", "mean"),
            mean_precision_20=("precision_20", "mean"),
            mean_constrained_fpr=("constrained_fpr", "mean"),
            mean_coverage_10=("coverage_10", "mean"),
            mean_pred_frac=("pred_frac", "mean"),
            positive_exact_pathogens=("mcc_exact", lambda x: int((x > 0).sum())),
        )
        .reset_index()
    )
    core = summary.loc[summary["entry"] == "PAHD-R-Core"].iloc[0]
    calibrated = summary.loc[summary["entry"] == "PAHD-R-Core-Calibrated"].iloc[0]
    for metric in ["mcc_exact", "mcc_window_10", "precision_20", "constrained_fpr", "coverage_10"]:
        summary[f"delta_{metric}_vs_core"] = summary[f"mean_{metric}"] - float(core[f"mean_{metric}"])
        summary[f"delta_{metric}_vs_core_calibrated"] = summary[f"mean_{metric}"] - float(calibrated[f"mean_{metric}"])
    summary["decision"] = summary.apply(decision, axis=1)
    summary = summary.sort_values(
        ["decision", "mean_mcc_exact", "mean_mcc_window_10", "mean_constrained_fpr"],
        ascending=[True, False, False, True],
    )

    results.to_csv(OUT_RESULTS, index=False)
    summary.to_csv(OUT_SUMMARY, index=False)

    candidates = summary[summary["decision"].str.contains("candidate")]
    top_diagnostics = summary.sort_values(
        ["mean_mcc_exact", "mean_mcc_window_10", "mean_constrained_fpr"],
        ascending=[False, False, True],
    ).head(15)
    report = [
        "# PAHD-R correlation-aware shrinkage sweep",
        "",
        "Date: 2026-04-27 KST",
        "",
        "## Purpose",
        "",
        (
            "The data-processing audit showed strong redundancy among freq, entropy, "
            "and dnds_proxy. This sweep tests unsupervised correlation-aware shrinkage "
            "of PAHD-R-Core evidence before candidate calling."
        ),
        "",
        "## Candidates",
        "",
        markdown_table(candidates),
        "",
        "## Top diagnostics",
        "",
        markdown_table(top_diagnostics),
        "",
        "## Interpretation",
        "",
        (
            "A shrinkage candidate is useful only if it improves exact and regional "
            "MCC without increasing constrained FPR or relying on broader coverage. "
            "If candidates do not beat PAHD-R-Core-Calibrated, shrinkage should be "
            "kept as a diagnostic design direction rather than a default change."
        ),
        "",
        "## Decision",
        "",
        (
            "Only entries marked `candidate` or `candidate_beats_calibrated` should "
            "advance to bootstrap validation. Rejected entries usually either lose "
            "exact/top-k performance or inflate coverage even when FPR decreases."
        ),
        "",
    ]
    OUT_REPORT.write_text("\n".join(report), encoding="utf-8")
    print(OUT_REPORT)
    print(candidates.round(4).to_string(index=False) if len(candidates) else "No candidates")


if __name__ == "__main__":
    run()
