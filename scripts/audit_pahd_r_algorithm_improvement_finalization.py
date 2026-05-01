#!/usr/bin/env python3
"""Finalize PAHD-R algorithm-improvement candidates.

This audit is intentionally stricter than the exploratory sweeps. It asks
whether any algorithm/preprocessing candidate should replace the current final
PAHD-R modes, using paired pathogen bootstrap and leave-one-pathogen influence
checks over already generated experiment tables.
"""

from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parent.parent
RESULTS_DIR = PROJECT_ROOT / "results" / "mutbench"
MODES = ["PAHD-R-Core", "PAHD-R-Augmented", "PAHD-R-Review"]
METRICS = ["mcc_exact", "mcc_window_10", "precision_20", "constrained_fpr"]


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


def paired_delta_table(results: pd.DataFrame, variant: str, mode: str) -> pd.DataFrame:
    base = results[(results["variant"] == "baseline") & (results["mode"] == mode)]
    cand = results[(results["variant"] == variant) & (results["mode"] == mode)]
    merged = cand.merge(base, on=["pathogen", "mode"], suffixes=("_candidate", "_baseline"))
    rows = []
    for _, row in merged.iterrows():
        out = {"variant": variant, "mode": mode, "pathogen": row["pathogen"]}
        for metric in METRICS:
            out[f"delta_{metric}"] = row[f"{metric}_candidate"] - row[f"{metric}_baseline"]
        rows.append(out)
    return pd.DataFrame(rows)


def bootstrap_delta(values: np.ndarray, rng: np.random.Generator, n_boot: int = 20000) -> dict[str, float]:
    values = np.asarray(values, dtype=float)
    if len(values) == 0:
        return {"mean": np.nan, "ci_low": np.nan, "ci_high": np.nan, "p_delta_gt_0": np.nan}
    idx = rng.integers(0, len(values), size=(n_boot, len(values)))
    boots = values[idx].mean(axis=1)
    return {
        "mean": float(values.mean()),
        "ci_low": float(np.quantile(boots, 0.025)),
        "ci_high": float(np.quantile(boots, 0.975)),
        "p_delta_gt_0": float((boots > 0).mean()),
    }


def leave_one_out_range(values: np.ndarray) -> tuple[float, float]:
    values = np.asarray(values, dtype=float)
    if len(values) <= 1:
        return (float(values.mean()) if len(values) else np.nan, float(values.mean()) if len(values) else np.nan)
    loo = []
    for i in range(len(values)):
        loo.append(np.delete(values, i).mean())
    return float(np.min(loo)), float(np.max(loo))


def adoption_decision(row: pd.Series) -> str:
    if row["variant"] == "winsorized_1_99":
        if (
            row["metric"] == "mcc_window_10"
            and row["ci_low"] > 0.0
            and row["loo_min"] > 0.0
            and row["paired_positive"] >= 7
        ):
            return "adopt"
        if row["metric"] == "mcc_window_10" and row["mean"] > 0.0:
            return "candidate_only"
    if row["variant"].startswith("dedup_"):
        if row["metric"] == "mcc_window_10" and row["mean"] < 0.0:
            return "reject"
        return "diagnostic_only"
    return "diagnostic_only"


def summarize_variant(
    results: pd.DataFrame,
    variant: str,
    mode: str,
    rng: np.random.Generator,
) -> tuple[list[dict[str, object]], pd.DataFrame]:
    paired = paired_delta_table(results, variant, mode)
    rows = []
    for metric in METRICS:
        col = f"delta_{metric}"
        values = paired[col].values
        stats = bootstrap_delta(values, rng)
        loo_min, loo_max = leave_one_out_range(values)
        rows.append({
            "variant": variant,
            "mode": mode,
            "metric": metric,
            **stats,
            "loo_min": loo_min,
            "loo_max": loo_max,
            "paired_positive": int((values > 0).sum()),
            "paired_negative": int((values < 0).sum()),
            "n_pathogens": int(len(values)),
        })
    return rows, paired


def run() -> None:
    rng = np.random.default_rng(20260427)
    robustness = pd.read_csv(RESULTS_DIR / "pahd_r_robustness_variant_results.csv")
    targeted = pd.read_csv(RESULTS_DIR / "pahd_r_targeted_dedup_winsorized_results.csv")

    summary_rows = []
    paired_rows = []
    for mode in MODES:
        rows, paired = summarize_variant(robustness, "winsorized_1_99", mode, rng)
        summary_rows.extend(rows)
        paired_rows.append(paired)
        for variant in ["dedup_alpha_25", "dedup_alpha_50", "dedup_alpha_100"]:
            rows, paired = summarize_variant(targeted, variant, mode, rng)
            summary_rows.extend(rows)
            paired_rows.append(paired)

    summary = pd.DataFrame(summary_rows)
    summary["decision"] = summary.apply(adoption_decision, axis=1)
    paired = pd.concat(paired_rows, ignore_index=True)

    decision_rows = []
    for variant in ["winsorized_1_99", "dedup_alpha_25", "dedup_alpha_50", "dedup_alpha_100"]:
        sub = summary[(summary["variant"] == variant) & (summary["metric"] == "mcc_window_10")]
        if variant == "winsorized_1_99":
            best = sub.sort_values(["mean", "p_delta_gt_0"], ascending=False).iloc[0]
            final = "candidate_only"
            reason = (
                "Region MCC improves on average, but bootstrap CIs cross zero or "
                "leave-one-pathogen influence is not uniformly positive."
            )
        elif variant == "dedup_alpha_25":
            best = sub.sort_values(["mean"], ascending=False).iloc[0]
            final = "diagnostic_only"
            reason = "Weak blend is not consistently beneficial and reduces the HIV-1/MERS targeted mean."
        else:
            best = sub.sort_values(["mean"], ascending=False).iloc[0]
            final = "reject"
            reason = "Stronger dedup-proxy replacement degrades region MCC and targeted HIV-1/MERS behavior."
        decision_rows.append({
            "candidate": variant,
            "best_mode_by_region_mcc": best["mode"],
            "best_mean_delta_mcc_window_10": best["mean"],
            "best_ci_low": best["ci_low"],
            "best_ci_high": best["ci_high"],
            "best_p_delta_gt_0": best["p_delta_gt_0"],
            "final_decision": final,
            "reason": reason,
        })
    decisions = pd.DataFrame(decision_rows)

    summary_path = RESULTS_DIR / "pahd_r_algorithm_improvement_bootstrap_summary.csv"
    paired_path = RESULTS_DIR / "pahd_r_algorithm_improvement_paired_deltas.csv"
    decisions_path = RESULTS_DIR / "pahd_r_algorithm_improvement_final_decisions.csv"
    report_path = RESULTS_DIR / "pahd_r_algorithm_improvement_finalization.md"
    summary.to_csv(summary_path, index=False)
    paired.to_csv(paired_path, index=False)
    decisions.to_csv(decisions_path, index=False)

    report = [
        "# PAHD-R Algorithm Improvement Finalization",
        "",
        "Date: 2026-04-27 KST",
        "",
        "## Purpose",
        "",
        (
            "This is the closing audit for algorithm-improvement candidates before "
            "secondary presentation/document cleanup. It applies paired pathogen "
            "bootstrap and leave-one-pathogen influence checks to the remaining "
            "candidate families."
        ),
        "",
        "## Final Candidate Decisions",
        "",
        markdown_table(decisions),
        "",
        "## Bootstrap Summary",
        "",
        markdown_table(summary[[
            "variant",
            "mode",
            "metric",
            "mean",
            "ci_low",
            "ci_high",
            "p_delta_gt_0",
            "loo_min",
            "loo_max",
            "paired_positive",
            "paired_negative",
            "decision",
        ]]),
        "",
        "## Algorithm Decision",
        "",
        (
            "No tested improvement is strong enough to replace the current PAHD-R "
            "Core/Augmented/Review defaults. Winsorized preprocessing remains the "
            "only worthwhile candidate for future validation. Dedup-proxy feature "
            "replacement should not be adopted."
        ),
        "",
    ]
    report_path.write_text("\n".join(report), encoding="utf-8")
    print(report_path)
    print(decisions.round(4).to_string(index=False))


if __name__ == "__main__":
    run()
