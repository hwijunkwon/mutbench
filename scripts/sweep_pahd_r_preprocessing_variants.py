#!/usr/bin/env python3
"""Evaluate preprocessing variants for PAHD-R feature modules."""

from __future__ import annotations

from pathlib import Path
import sys

import numpy as np
import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parent.parent
RESULTS_DIR = PROJECT_ROOT / "results" / "mutbench"
sys.path.insert(0, str(PROJECT_ROOT / "scripts"))
import run_pahd_r_multi_hypothesis as pahd  # noqa: E402


CORE_MODULES = {
    "recurrence": ["freq", "rare_freq"],
    "diversity": ["entropy"],
    "phylo": ["homoplasy", "dnds_proxy"],
}

MODULE_VARIANTS = {
    "recurrence": ["raw_z", "log1p_z", "rank", "winsor_z"],
    "diversity": ["raw_z", "rank", "centered_abs_z"],
    "phylo": ["raw_z", "log1p_z", "rank", "winsor_z", "binary_presence"],
}


def winsor(values: np.ndarray, lo: float = 0.01, hi: float = 0.99) -> np.ndarray:
    values = np.nan_to_num(np.asarray(values, dtype=float), nan=0.0, posinf=0.0, neginf=0.0)
    qlo, qhi = np.quantile(values, [lo, hi])
    return np.clip(values, qlo, qhi)


def transform(values: np.ndarray, variant: str) -> np.ndarray:
    values = np.nan_to_num(np.asarray(values, dtype=float), nan=0.0, posinf=0.0, neginf=0.0)
    if variant == "raw_z":
        return pahd.robust_z(values)
    if variant == "log1p_z":
        signed = np.sign(values) * np.log1p(np.abs(values))
        return pahd.robust_z(signed)
    if variant == "rank":
        return pahd.rank_percentile(values)
    if variant == "winsor_z":
        return pahd.robust_z(winsor(values))
    if variant == "centered_abs_z":
        return pahd.robust_z(np.abs(values - np.nanmedian(values)))
    if variant == "binary_presence":
        return (values > 0).astype(float)
    raise ValueError(f"unknown preprocessing variant: {variant}")


def module_score(df: pd.DataFrame, signs: dict[str, float], module: str, variant: str) -> np.ndarray:
    parts = []
    for feat in CORE_MODULES[module]:
        x = transform(df[feat].values, variant)
        if variant not in {"rank", "binary_presence"}:
            x = x * signs.get(feat, 1.0)
        else:
            if signs.get(feat, 1.0) < 0:
                x = 1.0 - x
        parts.append(x)
    return np.mean(np.column_stack(parts), axis=1)


def evaluate(pathogen: str, df: pd.DataFrame, strategy: str, scores: np.ndarray, frac: float) -> dict[str, object]:
    pred = pahd.top_fraction_pred(scores, frac)
    result = pahd.evaluate_prediction(pathogen, "PREPROC", strategy, df, scores, pred)
    row = result.__dict__
    row["frac"] = frac
    return row


def run() -> None:
    data = pahd.load_feature_matrices()
    benchmark = pd.read_csv(RESULTS_DIR / "multilayer_9pathogen_results.csv")
    pathogens = sorted(set(benchmark["pathogen"].unique()) & set(data.keys()))

    rows = []
    for target in pathogens:
        train_data = {p: df for p, df in data.items() if p != target and p in pathogens}
        signs = pahd.compute_feature_signs(train_data)
        df = data[target]

        # One-module preprocessing variants.
        for module, variants in MODULE_VARIANTS.items():
            for variant in variants:
                scores = module_score(df, signs, module, variant)
                for frac in [0.08, 0.10, 0.12]:
                    rows.append(evaluate(target, df, f"{module}:{variant}", scores, frac))

        # Core backbone variants where one module transform changes at a time.
        baseline_variants = {"recurrence": "raw_z", "diversity": "raw_z", "phylo": "raw_z"}
        for changed_module, variants in MODULE_VARIANTS.items():
            for variant in variants:
                config = dict(baseline_variants)
                config[changed_module] = variant
                config_key = f"changed={changed_module};" + ",".join(f"{m}={config[m]}" for m in CORE_MODULES)
                module_scores = {}
                for module in CORE_MODULES:
                    module_scores[module] = module_score(df, signs, module, config[module])
                score_df = pd.DataFrame(module_scores)
                fused = (
                    0.34 * pahd.rank_percentile(score_df["recurrence"].values)
                    + 0.33 * pahd.rank_percentile(score_df["diversity"].values)
                    + 0.33 * pahd.rank_percentile(score_df["phylo"].values)
                )
                cluster = pahd.local_background_cluster_score(score_df["recurrence"].values)
                fused_cluster = 0.80 * pahd.rank_percentile(fused) + 0.20 * pahd.rank_percentile(cluster)
                name = "core_preproc:" + config_key
                for frac in [0.08, 0.10, 0.12]:
                    rows.append(evaluate(target, df, name, fused_cluster, frac))

    result_df = pd.DataFrame(rows)
    summary = (
        result_df
        .groupby(["strategy", "frac"])
        .agg(
            mean_mcc_exact=("mcc_exact", "mean"),
            mean_mcc_window_10=("mcc_window_10", "mean"),
            mean_precision_20=("precision_20", "mean"),
            mean_constrained_fpr=("constrained_fpr", "mean"),
            mean_region_coverage_10=("region_coverage_10", "mean"),
            mean_auroc=("auroc", "mean"),
            positive_pathogens=("mcc_exact", lambda x: int((x > 0).sum())),
            n_pathogens=("pathogen", "nunique"),
        )
        .reset_index()
    )
    summary["objective_balanced"] = (
        summary["mean_mcc_exact"]
        + 0.30 * summary["mean_mcc_window_10"]
        + 0.15 * summary["mean_precision_20"]
        - 0.10 * summary["mean_constrained_fpr"].fillna(0.0)
        - 0.05 * summary["mean_region_coverage_10"]
    )
    summary = summary.sort_values(["objective_balanced", "mean_mcc_exact"], ascending=False)

    variant_rows = []
    for strategy in summary["strategy"].unique():
        if ":" not in strategy or strategy.startswith("core_preproc"):
            continue
        module, variant = strategy.split(":", 1)
        sub = summary[summary["strategy"] == strategy]
        best = sub.iloc[0]
        variant_rows.append({
            "module": module,
            "variant": variant,
            "best_frac": best["frac"],
            "best_objective": best["objective_balanced"],
            "best_mcc_exact": best["mean_mcc_exact"],
            "best_mcc_window_10": best["mean_mcc_window_10"],
            "best_precision_20": best["mean_precision_20"],
            "best_constrained_fpr": best["mean_constrained_fpr"],
        })
    variant_df = pd.DataFrame(variant_rows).sort_values(["module", "best_objective"], ascending=[True, False])

    result_df.to_csv(RESULTS_DIR / "pahd_r_preprocessing_variant_results.csv", index=False)
    summary.to_csv(RESULTS_DIR / "pahd_r_preprocessing_variant_summary.csv", index=False)
    variant_df.to_csv(RESULTS_DIR / "pahd_r_preprocessing_by_module_summary.csv", index=False)

    report = [
        "# PAHD-R Preprocessing Variant Sweep",
        "",
        "Date: 2026-04-26 KST",
        "",
        "## Top 20 Strategies",
        "",
        markdown_table(summary.head(20)),
        "",
        "## Best Variant By Module",
        "",
        markdown_table(variant_df),
        "",
        "## Interpretation",
        "",
        (
            "This sweep tests whether module-specific preprocessing changes the "
            "PAHD-R backbone. It should be interpreted as a sensitivity analysis "
            "before selecting final preprocessing defaults."
        ),
        "",
    ]
    out = RESULTS_DIR / "pahd_r_preprocessing_variant_sweep.md"
    out.write_text("\n".join(report), encoding="utf-8")
    print(out)
    print(summary.head(15).round(4).to_string(index=False))


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


if __name__ == "__main__":
    run()
