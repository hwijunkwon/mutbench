#!/usr/bin/env python3
"""Region-split SARS-CoV-2 prior sweep for PAHD-R repair candidates."""

from __future__ import annotations

from pathlib import Path
import hashlib
import sys

import numpy as np
import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parent.parent
RESULTS_DIR = PROJECT_ROOT / "results" / "mutbench"
sys.path.insert(0, str(PROJECT_ROOT / "scripts"))
import audit_pahd_r_decoy_coordinate_robustness as decoy_audit  # noqa: E402
import run_pahd_r_multi_hypothesis as pahd  # noqa: E402
import test_pahd_r_domain_prior_repair as repair  # noqa: E402


PATHOGEN = "SARS-CoV-2"
MODES = ["PAHD-R-Core", "PAHD-R-Augmented", "PAHD-R-Review"]
WEIGHTS = [0.05, 0.10, 0.15, 0.20, 0.30]
N_PERM = 200

REGION_PRIORS = {
    "ntd_supersite": [(14, 20), (140, 158), (242, 264)],
    "rbd": [(319, 541)],
    "rbd_ace2_escape": [(346, 346), (371, 376), (405, 408), (417, 417), (440, 446), (452, 460), (478, 501)],
    "s1s2_furin": [(675, 690)],
    "rbd_plus_ntd": [(14, 20), (140, 158), (242, 264), (319, 541)],
    "rbd_plus_furin": [(319, 541), (675, 690)],
}


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


def evaluate(df: pd.DataFrame, mode: str, score: np.ndarray) -> dict[str, float]:
    y = df["layer_a"].astype(int).values
    frac = 0.08 if mode == "PAHD-R-Review" else 0.10
    pred = pahd.top_fraction_pred(score, frac)
    p20, _ = pahd.precision_and_enrichment(y, score, 20)
    return {
        "mcc_exact": pahd.region_mcc(y, pred, 0),
        "mcc_window_10": pahd.region_mcc(y, pred, 10),
        "precision_20": p20,
        "constrained_fpr": pahd.constrained_fpr(PATHOGEN, len(df), pred),
        "coverage_10": pahd.expanded_coverage(pred, 10),
    }


def permutation_p(y: np.ndarray, pred: np.ndarray, rng: np.random.Generator) -> tuple[float, float, float]:
    observed = pahd.region_mcc(y, pred, 0)
    null = np.array([pahd.region_mcc(rng.permutation(y), pred, 0) for _ in range(N_PERM)])
    return float(null.mean()), float(np.quantile(null, 0.95)), float(np.mean(null >= observed))


def shifted_ranges(ranges: list[tuple[int, int]], shift: int, n: int) -> list[tuple[int, int]]:
    out = []
    for start, end in ranges:
        s = max(1, start + shift)
        e = min(n, end + shift)
        if s <= e:
            out.append((s, e))
    return out


def prior_score(n: int, region: str, control: str) -> np.ndarray:
    ranges = REGION_PRIORS[region]
    if control == "real":
        return repair.smooth_mask(n, ranges)
    if control == "shift_plus_80":
        return repair.smooth_mask(n, shifted_ranges(ranges, 80, n))
    if control == "shift_minus_80":
        return repair.smooth_mask(n, shifted_ranges(ranges, -80, n))
    if control == "random_matched":
        total_width = sum(end - start + 1 for start, end in ranges)
        mean_width = max(5, int(round(total_width / max(1, len(ranges)))))
        digest = hashlib.sha256(f"{PATHOGEN}:{region}".encode("utf-8")).hexdigest()
        rng = np.random.default_rng(int(digest[:8], 16))
        starts = rng.choice(np.arange(1, n + 1), size=len(ranges), replace=False)
        random_ranges = [(int(s), min(n, int(s) + mean_width - 1)) for s in starts]
        return repair.smooth_mask(n, random_ranges)
    raise ValueError(control)


def run() -> None:
    data = pahd.load_feature_matrices()
    benchmark = pd.read_csv(RESULTS_DIR / "multilayer_9pathogen_results.csv")
    pathogens = sorted(set(benchmark["pathogen"].unique()) & set(data.keys()))
    df = data[PATHOGEN]
    y = df["layer_a"].astype(int).values
    scores = decoy_audit.candidate_scores(data, pathogens, PATHOGEN)
    rng = np.random.default_rng(20260426)

    rows = []
    for mode in MODES:
        base = scores[mode]
        base_metrics = evaluate(df, mode, base)
        rows.append({
            "mode": mode,
            "region": "baseline",
            "control": "baseline",
            "weight": 0.0,
            **base_metrics,
            "delta_mcc_exact": 0.0,
            "delta_mcc_window_10": 0.0,
            "delta_precision_20": 0.0,
            "delta_constrained_fpr": 0.0,
            "delta_coverage_10": 0.0,
            "null_mean_mcc": np.nan,
            "null_p95_mcc": np.nan,
            "empirical_p_null_ge_observed": np.nan,
        })
        for region in REGION_PRIORS:
            for control in ["real", "shift_plus_80", "shift_minus_80", "random_matched"]:
                prior = prior_score(len(df), region, control)
                for weight in WEIGHTS:
                    score = repair.repaired_score(base, prior, weight)
                    metrics = evaluate(df, mode, score)
                    frac = 0.08 if mode == "PAHD-R-Review" else 0.10
                    pred = pahd.top_fraction_pred(score, frac)
                    null_mean, null_p95, empirical_p = permutation_p(y, pred, rng)
                    rows.append({
                        "mode": mode,
                        "region": region,
                        "control": control,
                        "weight": weight,
                        **metrics,
                        "delta_mcc_exact": metrics["mcc_exact"] - base_metrics["mcc_exact"],
                        "delta_mcc_window_10": metrics["mcc_window_10"] - base_metrics["mcc_window_10"],
                        "delta_precision_20": metrics["precision_20"] - base_metrics["precision_20"],
                        "delta_constrained_fpr": metrics["constrained_fpr"] - base_metrics["constrained_fpr"],
                        "delta_coverage_10": metrics["coverage_10"] - base_metrics["coverage_10"],
                        "null_mean_mcc": null_mean,
                        "null_p95_mcc": null_p95,
                        "empirical_p_null_ge_observed": empirical_p,
                    })

    results = pd.DataFrame(rows)
    real = results[results["control"] == "real"].copy()
    controls = results[results["control"].isin(["shift_plus_80", "shift_minus_80", "random_matched"])].copy()
    best_controls = (
        controls.sort_values(["mode", "region", "mcc_exact", "precision_20"], ascending=[True, True, False, False])
        .groupby(["mode", "region"])
        .head(1)[["mode", "region", "control", "mcc_exact", "precision_20"]]
        .rename(columns={
            "control": "best_control",
            "mcc_exact": "best_control_mcc_exact",
            "precision_20": "best_control_precision_20",
        })
    )
    decisions = real.merge(best_controls, on=["mode", "region"], how="left")
    decisions["beats_control_exact"] = decisions["mcc_exact"] > decisions["best_control_mcc_exact"]
    decisions["beats_control_precision"] = decisions["precision_20"] >= decisions["best_control_precision_20"]
    decisions["passes_permutation"] = decisions["empirical_p_null_ge_observed"] <= 0.01
    decisions["adoption_decision"] = np.where(
        (decisions["delta_mcc_exact"] > 0)
        & (decisions["delta_precision_20"] >= 0)
        & decisions["beats_control_exact"]
        & decisions["beats_control_precision"]
        & decisions["passes_permutation"],
        "candidate",
        "reject",
    )
    best = (
        decisions.sort_values(
            ["adoption_decision", "mode", "delta_mcc_exact", "delta_precision_20"],
            ascending=[True, True, False, False],
        )
        .groupby("mode")
        .head(5)
    )

    results.to_csv(RESULTS_DIR / "pahd_r_sars2_region_split_prior_results.csv", index=False)
    decisions.to_csv(RESULTS_DIR / "pahd_r_sars2_region_split_prior_decisions.csv", index=False)

    report = [
        "# PAHD-R SARS-CoV-2 Region-Split Prior Sweep",
        "",
        "Date: 2026-04-26 KST",
        "",
        "## Best Decision Rows",
        "",
        markdown_table(best[[
            "mode",
            "region",
            "weight",
            "mcc_exact",
            "delta_mcc_exact",
            "mcc_window_10",
            "delta_mcc_window_10",
            "precision_20",
            "delta_precision_20",
            "constrained_fpr",
            "coverage_10",
            "best_control",
            "best_control_mcc_exact",
            "best_control_precision_20",
            "empirical_p_null_ge_observed",
            "adoption_decision",
        ]]),
        "",
        "## Interpretation",
        "",
        "- A SARS-CoV-2 repair candidate must improve exact MCC, preserve or improve Precision@20, pass p<=0.01, and beat shifted/random-region controls.",
        "- Rows that only improve MCC +/-10 are rejected as region-review artifacts.",
        "",
    ]
    out = RESULTS_DIR / "pahd_r_sars2_region_split_prior_sweep.md"
    out.write_text("\n".join(report), encoding="utf-8")
    print(out)
    print(best.round(4).to_string(index=False))


if __name__ == "__main__":
    run()
