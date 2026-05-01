#!/usr/bin/env python3
"""Adversarial audit for PAHD-R redesign experiments.

The audit checks whether the observed performance could plausibly come from
label leakage or overfitting artifacts:

1. permutation-label null for the same H11 scoring path;
2. train-only orientation check for feature signs;
3. suspiciously perfect per-pathogen performance checks;
4. method-set train/held-out separation sanity checks.
"""

from __future__ import annotations

from pathlib import Path
import argparse
import sys

import numpy as np
import pandas as pd
from sklearn.metrics import matthews_corrcoef, roc_auc_score

PROJECT_ROOT = Path(__file__).resolve().parent.parent
RESULTS_DIR = PROJECT_ROOT / "results" / "mutbench"
FEATURE_DIR = RESULTS_DIR / "feature_analysis"
BENCHMARK_PATH = RESULTS_DIR / "multilayer_9pathogen_results.csv"

sys.path.insert(0, str(PROJECT_ROOT / "scripts"))
import run_pahd_r_multi_hypothesis as pahd  # noqa: E402


def mcc_exact(y_true: np.ndarray, scores: np.ndarray, frac: float = 0.10) -> float:
    pred = pahd.top_fraction_pred(scores, frac)
    if pred.sum() == 0 or pred.sum() == len(pred):
        return 0.0
    return float(matthews_corrcoef(y_true.astype(int), pred.astype(int)))


def candidate_scores_for_target(
    data: dict[str, pd.DataFrame],
    pathogens: list[str],
    target: str,
    strategy: str,
    label_column: str = "layer_a",
) -> np.ndarray:
    train_data = {p: df for p, df in data.items() if p != target and p in pathogens}
    df = data[target]

    if label_column != "layer_a":
        train_data = {p: frame.assign(layer_a=frame[label_column].values) for p, frame in train_data.items()}

    signs = pahd.compute_feature_signs(train_data)
    effects = pahd.compute_feature_effects(train_data)
    scores_df = pahd.module_scores(df, signs)
    learned = pahd.combine_modules(scores_df, pahd.learned_module_weights(effects))
    phylo = scores_df["phylo"].values
    cluster = pahd.local_background_cluster_score(scores_df["recurrence"].values, seed=200 + pathogens.index(target))
    reliability = pahd.cluster_reliability(cluster, phylo, learned)
    gated_cluster_weight = 0.15 + 0.45 * reliability
    gated_phylo_weight = 0.25
    gated_learned_weight = 1.0 - gated_cluster_weight - gated_phylo_weight
    h11 = (
        gated_learned_weight * pahd.rank_percentile(learned)
        + gated_cluster_weight * pahd.rank_percentile(cluster)
        + gated_phylo_weight * pahd.rank_percentile(phylo)
    )
    if strategy == "compactness_gated_rank_fusion":
        return h11

    if strategy == "h11_soft_constraint_post":
        constraint_rel = pahd.constraint_reliability(scores_df)
        alternatives = pahd.h11_preserving_alternatives(
            h11,
            learned,
            cluster,
            phylo,
            np.ones(len(df), dtype=float),
            cluster,
            scores_df,
            constraint_rel,
        )
        return alternatives["h11_soft_constraint_post"]

    if strategy == "non_ai_core_fusion":
        non_ai_scores_df = pahd.non_ai_module_scores(df, signs)
        non_ai_weights = pahd.learned_non_ai_weights(effects)
        non_ai_learned = pahd.combine_modules(non_ai_scores_df, non_ai_weights)
        non_ai_phylo = non_ai_scores_df["phylo"].values
        non_ai_cluster = pahd.local_background_cluster_score(
            non_ai_scores_df["recurrence"].values,
            seed=400 + pathogens.index(target),
        )
        non_ai_reliability = pahd.cluster_reliability(non_ai_cluster, non_ai_phylo, non_ai_learned)
        non_ai_cluster_weight = 0.15 + 0.45 * non_ai_reliability
        non_ai_phylo_weight = 0.25
        non_ai_learned_weight = 1.0 - non_ai_cluster_weight - non_ai_phylo_weight
        return (
            non_ai_learned_weight * pahd.rank_percentile(non_ai_learned)
            + non_ai_cluster_weight * pahd.rank_percentile(non_ai_cluster)
            + non_ai_phylo_weight * pahd.rank_percentile(non_ai_phylo)
        )

    raise ValueError(f"unknown candidate strategy: {strategy}")


def permutation_audit(data: dict[str, pd.DataFrame], pathogens: list[str], n_perm: int = 100) -> pd.DataFrame:
    strategies = ["compactness_gated_rank_fusion", "h11_soft_constraint_post", "non_ai_core_fusion"]
    rows = []
    rng = np.random.default_rng(20260426)
    observed_mcc = {}

    for strategy in strategies:
        for target in pathogens:
            y = data[target]["layer_a"].astype(int).values
            scores = candidate_scores_for_target(data, pathogens, target, strategy)
            observed_mcc[(strategy, target)] = mcc_exact(y, scores)

    for perm_id in range(n_perm):
        permuted = {}
        for pathogen, df in data.items():
            frame = df.copy()
            frame["perm_layer_a"] = rng.permutation(frame["layer_a"].astype(int).values)
            permuted[pathogen] = frame
        for strategy in strategies:
            for target in pathogens:
                y_perm = permuted[target]["perm_layer_a"].astype(int).values
                scores = candidate_scores_for_target(
                    permuted,
                    pathogens,
                    target,
                    strategy,
                    label_column="perm_layer_a",
                )
                rows.append({
                    "perm_id": perm_id,
                    "strategy": strategy,
                    "pathogen": target,
                    "mcc_exact": mcc_exact(y_perm, scores),
                    "auroc": roc_auc_score(y_perm, scores)
                    if y_perm.sum() > 1 and (len(y_perm) - y_perm.sum()) > 1 and np.std(scores) > 1e-12
                    else np.nan,
                })

    null_df = pd.DataFrame(rows)
    obs = pd.DataFrame([
        {"strategy": strategy, "pathogen": pathogen, "observed_mcc_exact": observed_mcc[(strategy, pathogen)]}
        for strategy in strategies
        for pathogen in pathogens
    ])
    path_summary = (
        null_df.groupby(["strategy", "pathogen"])
        .agg(
            null_mean_mcc=("mcc_exact", "mean"),
            null_p95_mcc=("mcc_exact", lambda x: float(np.quantile(x, 0.95))),
            null_mean_auroc=("auroc", "mean"),
        )
        .reset_index()
        .merge(obs, on=["strategy", "pathogen"], how="left")
    )
    path_summary["exceeds_null_p95"] = path_summary["observed_mcc_exact"] > path_summary["null_p95_mcc"]
    return null_df, path_summary


def leakage_sanity_checks(data: dict[str, pd.DataFrame], pathogens: list[str]) -> pd.DataFrame:
    rows = []
    for target in pathogens:
        train_data = {p: df for p, df in data.items() if p != target and p in pathogens}
        signs_train = pahd.compute_feature_signs(train_data)
        signs_all = pahd.compute_feature_signs({p: data[p] for p in pathogens})
        sign_mismatches = sum(signs_train[feat] != signs_all[feat] for feat in pahd.FEATURES)
        target_y = data[target]["layer_a"].astype(int).values
        rows.append({
            "pathogen": target,
            "n_positions": len(data[target]),
            "n_layer_a": int(target_y.sum()),
            "label_prevalence": float(target_y.mean()),
            "train_vs_all_sign_mismatches": int(sign_mismatches),
            "gt_columns_present": ",".join([c for c in data[target].columns if c.startswith("layer_")]),
        })
    return pd.DataFrame(rows)


def result_outlier_checks() -> pd.DataFrame:
    result_path = RESULTS_DIR / "pahd_r_multi_hypothesis_results.csv"
    if not result_path.exists():
        return pd.DataFrame()
    df = pd.read_csv(result_path)
    rows = []
    for strategy in ["compactness_gated_rank_fusion", "h11_soft_constraint_post", "reliability_gated_postprocessed"]:
        sub = df[df["strategy"] == strategy]
        if sub.empty:
            continue
        rows.append({
            "strategy": strategy,
            "max_exact_mcc": float(sub["mcc_exact"].max()),
            "min_exact_mcc": float(sub["mcc_exact"].min()),
            "max_precision_20": float(sub["precision_20"].max()),
            "n_perfect_precision20": int((sub["precision_20"] >= 1.0).sum()),
            "n_negative_exact": int((sub["mcc_exact"] < 0).sum()),
        })
    return pd.DataFrame(rows)


def method_set_sanity() -> pd.DataFrame:
    benchmark = pd.read_csv(BENCHMARK_PATH)
    rows = []
    for target in sorted(benchmark["pathogen"].unique()):
        train = benchmark[benchmark["pathogen"] != target]
        target_df = benchmark[benchmark["pathogen"] == target]
        train_combos = set(map(tuple, train[["score", "detector"]].values))
        target_combos = set(map(tuple, target_df[["score", "detector"]].values))
        overlap = train_combos & target_combos
        rows.append({
            "pathogen": target,
            "train_combos": len(train_combos),
            "target_combos": len(target_combos),
            "overlap_combos": len(overlap),
            "target_only_combos": len(target_combos - train_combos),
        })
    return pd.DataFrame(rows)


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


def run() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--n-perm", type=int, default=500)
    args = parser.parse_args()

    data = pahd.load_feature_matrices()
    benchmark = pd.read_csv(BENCHMARK_PATH)
    pathogens = sorted(set(benchmark["pathogen"].unique()) & set(data.keys()))

    null_df, null_summary = permutation_audit(data, pathogens, n_perm=args.n_perm)
    leakage_df = leakage_sanity_checks(data, pathogens)
    outlier_df = result_outlier_checks()
    method_df = method_set_sanity()

    null_df.to_csv(RESULTS_DIR / "pahd_r_adversarial_null_permutations.csv", index=False)
    null_summary.to_csv(RESULTS_DIR / "pahd_r_adversarial_null_summary.csv", index=False)
    leakage_df.to_csv(RESULTS_DIR / "pahd_r_adversarial_leakage_checks.csv", index=False)
    outlier_df.to_csv(RESULTS_DIR / "pahd_r_adversarial_outlier_checks.csv", index=False)
    method_df.to_csv(RESULTS_DIR / "pahd_r_adversarial_method_set_checks.csv", index=False)

    global_rows = []
    for strategy in sorted(null_summary["strategy"].unique()):
        obs = null_summary[null_summary["strategy"] == strategy]["observed_mcc_exact"].mean()
        null_means = null_df[null_df["strategy"] == strategy].groupby("perm_id")["mcc_exact"].mean().values
        global_rows.append({
            "strategy": strategy,
            "observed_mean_mcc": float(obs),
            "null_mean_mcc": float(np.mean(null_means)),
            "empirical_p_null_ge_observed": float(np.mean(null_means >= obs)),
        })
    global_df = pd.DataFrame(global_rows)
    global_df.to_csv(RESULTS_DIR / "pahd_r_adversarial_global_summary.csv", index=False)
    report = [
        "# PAHD-R Adversarial Audit",
        "",
        "Date: 2026-04-26 KST",
        "",
        "## Permutation Null",
        "",
        f"- permutation runs: {args.n_perm}",
        "",
        markdown_table(global_df),
        "",
        "## Per-Pathogen Null",
        "",
        markdown_table(null_summary),
        "",
        "## Leakage Sanity Checks",
        "",
        markdown_table(leakage_df),
        "",
        "## Result Outlier Checks",
        "",
        markdown_table(outlier_df),
        "",
        "## Method-Set Separation Checks",
        "",
        markdown_table(method_df),
        "",
        "## Interpretation",
        "",
        (
            "No audit can prove absence of leakage, but this run checks whether "
            "the H11 path survives label randomization and whether result files "
            "show suspicious perfect-performance patterns. Any pathogen whose "
            "observed MCC does not exceed its permutation p95 remains a weak "
            "case and should not be overclaimed."
        ),
        "",
    ]
    report_path = RESULTS_DIR / "pahd_r_adversarial_audit.md"
    report_path.write_text("\n".join(report), encoding="utf-8")
    print(report_path)
    print(global_df.round(4).to_string(index=False))


if __name__ == "__main__":
    run()
