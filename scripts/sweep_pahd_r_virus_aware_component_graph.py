#!/usr/bin/env python3
"""Virus-aware PAHD-R component and site-graph experiments.

This sweep translates virus-specific literature into two testable score families:

1. ComponentProduct: EVEscape-like component gating.
2. VirusGraph: lightweight view-specific site-neighborhood fusion.
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
import sweep_pahd_r_correlation_shrinkage as shrinkage  # noqa: E402

OUT_RESULTS = RESULTS_DIR / "pahd_r_virus_aware_component_graph_results.csv"
OUT_SUMMARY = RESULTS_DIR / "pahd_r_virus_aware_component_graph_summary.csv"
OUT_SELECTIVE = RESULTS_DIR / "pahd_r_virus_aware_component_graph_selective_summary.csv"
OUT_REPORT = RESULTS_DIR / "pahd_r_virus_aware_component_graph_sweep.md"

METRICS = ["mcc_exact", "mcc_window_10", "precision_20", "constrained_fpr", "coverage_10"]


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


def safe_rank(values: np.ndarray) -> np.ndarray:
    return np.clip(pahd.rank_percentile(np.nan_to_num(values, nan=0.0)), 1e-4, 1.0)


def component_scores(data: dict[str, pd.DataFrame], pathogens: list[str], target: str) -> dict[str, np.ndarray]:
    train_data = {p: df for p, df in data.items() if p != target and p in pathogens}
    signs = pahd.compute_feature_signs(train_data)
    df = data[target]
    full = pahd.module_scores(df, signs)

    recurrence = safe_rank(full["recurrence"].values)
    diversity = safe_rank(full["diversity"].values)
    phylo = safe_rank(full["phylo"].values)
    constraint = safe_rank(full["constraint"].values)
    structure = safe_rank(full["structure"].values)
    semantic = safe_rank(full["semantic"].values)

    sasa_access = safe_rank(df["sasa"].values)
    grantham_disrupt = safe_rank(pahd.robust_z(df["grantham"].values) * signs.get("grantham", 1.0))
    evolutionary = np.clip(0.30 * recurrence + 0.25 * diversity + 0.45 * phylo, 1e-4, 1.0)
    accessibility = np.clip(0.65 * sasa_access + 0.35 * structure, 1e-4, 1.0)
    disruption = np.clip(0.55 * semantic + 0.45 * grantham_disrupt, 1e-4, 1.0)
    viability = np.clip(0.70 * constraint + 0.30 * structure, 1e-4, 1.0)

    product_all = (viability * accessibility * disruption * evolutionary) ** 0.25
    product_no_plm = (accessibility * grantham_disrupt * evolutionary * structure) ** 0.25
    evo_access = (evolutionary * accessibility) ** 0.5
    escape_balanced = (0.30 * viability + 0.20 * accessibility + 0.20 * disruption + 0.30 * evolutionary)
    gated_evolution = evolutionary * np.sqrt(np.clip(0.50 * viability + 0.50 * accessibility, 1e-4, 1.0))

    return {
        "component_product_all": product_all,
        "component_product_no_plm": product_no_plm,
        "component_evo_access": evo_access,
        "component_escape_balanced": escape_balanced,
        "component_gated_evolution": gated_evolution,
    }


def graph_local_support(view: np.ndarray, positions: np.ndarray, k: int = 18, coord_scale: float = 12.0) -> np.ndarray:
    view = safe_rank(view)
    pos = positions.astype(float)
    dv = np.abs(view[:, None] - view[None, :])
    dp = np.abs(pos[:, None] - pos[None, :]) / max(coord_scale, 1.0)
    sim = np.exp(-(dv * dv) / 0.06 - (dp * dp) / 2.0)
    np.fill_diagonal(sim, 0.0)
    if k < len(view) - 1:
        kth = np.partition(sim, -k, axis=1)[:, -k]
        sim[sim < kth[:, None]] = 0.0
    denom = sim.sum(axis=1)
    support = np.where(denom > 1e-12, sim @ view / denom, view)
    return safe_rank(0.65 * view + 0.35 * support)


def graph_scores(data: dict[str, pd.DataFrame], pathogens: list[str], target: str) -> dict[str, np.ndarray]:
    train_data = {p: df for p, df in data.items() if p != target and p in pathogens}
    signs = pahd.compute_feature_signs(train_data)
    df = data[target]
    full = pahd.module_scores(df, signs)
    positions = df["position"].values if "position" in df else np.arange(len(df))

    views = {
        "evolution": 0.35 * safe_rank(full["recurrence"].values) + 0.25 * safe_rank(full["diversity"].values) + 0.40 * safe_rank(full["phylo"].values),
        "constraint": safe_rank(full["constraint"].values),
        "structure": safe_rank(full["structure"].values),
        "semantic": safe_rank(full["semantic"].values),
    }
    supports = {name: graph_local_support(values, positions) for name, values in views.items()}
    fusion_all = np.mean(np.column_stack(list(supports.values())), axis=1)
    fusion_core = np.mean(np.column_stack([supports["evolution"], supports["structure"]]), axis=1)
    fusion_escape = (
        0.45 * supports["evolution"]
        + 0.25 * supports["structure"]
        + 0.15 * supports["constraint"]
        + 0.15 * supports["semantic"]
    )
    compact = fusion_escape * (1.0 - 0.15 * pahd.expanded_coverage(pahd.top_fraction_pred(fusion_escape, 0.10), 10))
    return {
        "virus_graph_all_views": fusion_all,
        "virus_graph_core_views": fusion_core,
        "virus_graph_escape_weighted": fusion_escape,
        "virus_graph_escape_compact": compact,
    }


def predict(score: np.ndarray, reliability: np.ndarray, selector: str) -> np.ndarray:
    if selector == "top8":
        return pahd.top_fraction_pred(score, 0.08)
    if selector == "top10":
        return pahd.top_fraction_pred(score, 0.10)
    if selector == "reliability_top8":
        combined = 0.70 * safe_rank(score) + 0.30 * safe_rank(reliability)
        return pahd.top_fraction_pred(combined, 0.08)
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
    if row["delta_mcc_exact_vs_calibrated"] > 0 and row["delta_mcc_window_10_vs_calibrated"] >= 0 and row["delta_precision_20_vs_calibrated"] >= 0 and row["delta_constrained_fpr_vs_calibrated"] <= 0:
        return "candidate_beats_calibrated"
    if row["delta_mcc_exact_vs_core"] > 0 and row["delta_precision_20_vs_core"] >= 0 and row["delta_constrained_fpr_vs_core"] <= 0:
        return "candidate_vs_core"
    if row["delta_mcc_window_10_vs_core"] < -0.05 or row["delta_precision_20_vs_core"] < -0.05:
        return "reject"
    return "diagnostic_only"


def summarize(results: pd.DataFrame) -> pd.DataFrame:
    summary = (
        results.groupby(["entry", "score_family", "score_variant", "selector"])
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
    core = summary[summary["entry"] == "PAHD-R-Core"].iloc[0]
    calibrated = summary[summary["entry"] == "PAHD-R-Core-Calibrated"].iloc[0]
    for metric in METRICS:
        summary[f"delta_{metric}_vs_core"] = summary[f"mean_{metric}"] - float(core[f"mean_{metric}"])
        summary[f"delta_{metric}_vs_calibrated"] = summary[f"mean_{metric}"] - float(calibrated[f"mean_{metric}"])
    summary["decision"] = summary.apply(decision, axis=1)
    return summary.sort_values(["decision", "mean_mcc_exact", "mean_mcc_window_10"], ascending=[True, False, False])


def selective_summary(results: pd.DataFrame) -> pd.DataFrame:
    policy_path = RESULTS_DIR / "pahd_r_selective_callability_policy.csv"
    if not policy_path.exists():
        return pd.DataFrame()
    policy = pd.read_csv(policy_path)
    merged = results.merge(policy[["pathogen", "pre_metric_callability"]], on="pathogen", how="left")
    rows = []
    for entry, group in merged.groupby("entry"):
        for name, classes in [
            ("callable_only", ["callable"]),
            ("callable_plus_review", ["callable", "review_only"]),
        ]:
            accepted = group[group["pre_metric_callability"].isin(classes)]
            if accepted.empty:
                continue
            rows.append({
                "entry": entry,
                "policy": name,
                "accepted_pathogens": int(accepted["pathogen"].nunique()),
                "demoted_pathogens": int(group["pathogen"].nunique() - accepted["pathogen"].nunique()),
                **{f"mean_{m}": float(accepted[m].mean()) for m in METRICS},
            })
    return pd.DataFrame(rows).sort_values(["policy", "mean_mcc_exact", "mean_mcc_window_10"], ascending=[True, False, False])


def run() -> None:
    data = pahd.load_feature_matrices()
    pathogens = primary_pathogens(data)
    selectors = ["top8", "top10", "reliability_top8"]
    rows = []

    for pathogen in pathogens:
        df = data[pathogen]
        ranks = calibration.module_ranks(data, pathogens, pathogen)
        baseline_scores = final_scores.candidate_scores(data, pathogens, pathogen)
        core = baseline_scores["PAHD-R-Core"]
        core_rel = calibration.reliability_score("PAHD-R-Core", core, ranks)
        rows.append({
            "pathogen": pathogen,
            "entry": "PAHD-R-Core",
            "score_family": "baseline",
            "score_variant": "baseline",
            "selector": "top10",
            **evaluate(pathogen, df, core, pahd.top_fraction_pred(core, 0.10)),
        })
        rows.append({
            "pathogen": pathogen,
            "entry": "PAHD-R-Core-Calibrated",
            "score_family": "baseline",
            "score_variant": "baseline",
            "selector": "reliability_top8",
            **evaluate(pathogen, df, core, predict(core, core_rel, "reliability_top8")),
        })

        candidates = {}
        candidates.update({("component", k): v for k, v in component_scores(data, pathogens, pathogen).items()})
        candidates.update({("virus_graph", k): v for k, v in graph_scores(data, pathogens, pathogen).items()})
        for (family, variant), score in candidates.items():
            rel = calibration.reliability_score("PAHD-R-Core", score, ranks)
            for selector in selectors:
                rows.append({
                    "pathogen": pathogen,
                    "entry": f"{variant}:{selector}",
                    "score_family": family,
                    "score_variant": variant,
                    "selector": selector,
                    **evaluate(pathogen, df, score, predict(score, rel, selector)),
                })

    results = pd.DataFrame(rows)
    summary = summarize(results)
    selective = selective_summary(results)
    results.to_csv(OUT_RESULTS, index=False)
    summary.to_csv(OUT_SUMMARY, index=False)
    selective.to_csv(OUT_SELECTIVE, index=False)

    candidates = summary[summary["decision"].str.contains("candidate")]
    report = [
        "# PAHD-R virus-aware component and graph sweep",
        "",
        "Date: 2026-04-27 KST",
        "",
        "## Scope",
        "",
        (
            "This sweep tests virus-specific redesign ideas: EVEscape-like component "
            "gating and lightweight site-neighborhood graph fusion. It does not use "
            "target labels to fit score parameters; labels are used only for evaluation."
        ),
        "",
        "## Candidates",
        "",
        markdown_table(candidates),
        "",
        "## Top global summary",
        "",
        markdown_table(summary.sort_values(["mean_mcc_exact", "mean_mcc_window_10"], ascending=False).head(15)),
        "",
        "## Selective summary",
        "",
        markdown_table(selective.head(20)),
        "",
        "## Interpretation",
        "",
        (
            "Component/product candidates are expected to reduce false positives when "
            "one biological constraint is missing. Graph candidates are exploratory and "
            "should be rejected if they improve only regional metrics or inflate coverage."
        ),
        "",
    ]
    OUT_REPORT.write_text("\n".join(report), encoding="utf-8")
    print(OUT_REPORT)
    print(candidates.round(4).to_string(index=False) if len(candidates) else "No candidates")


if __name__ == "__main__":
    run()
