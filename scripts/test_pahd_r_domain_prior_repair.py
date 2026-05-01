#!/usr/bin/env python3
"""Domain-prior repair tests for weak PAHD-R cases.

The priors are broad literature/domain masks, not fitted to Layer A labels.
Shifted-prior controls are included to check whether gains are merely caused by
adding any broad region bonus.
"""

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


PRIOR_RANGES_1BASED = {
    # MERS-CoV spike receptor-binding subdomain / DPP4 interface neighborhood.
    # Includes broad RBD plus interface contacts around Y499, L506, D510, E513,
    # E536-D539, Y540, W553, V555.
    "MERS": [(367, 606), (490, 565)],
    # RSV F broad antigenic/prioritized regions: site O/nirsevimab neighborhood,
    # site II/palivizumab neighborhood, and additional F antigenic regions.
    "RSV": [(60, 80), (190, 215), (250, 280), (340, 390), (420, 440)],
    # SARS-CoV-2 spike distributed adaptive regions: NTD supersite segments, RBD,
    # and S1/S2 furin-cleavage neighborhood.
    "SARS-CoV-2": [(14, 20), (140, 158), (242, 264), (319, 541), (675, 690)],
    # HCV E2 broad HVR1 and CD81/neutralizing-face neighborhoods in the local
    # feature coordinate frame. This is exploratory because HCV coordinate
    # reconciliation remains incomplete.
    "HCV": [(1, 30), (80, 115), (185, 230), (260, 310)],
}

WEIGHTS = [0.05, 0.10, 0.15, 0.20, 0.30]
MODES = ["PAHD-R-Core", "PAHD-R-Augmented", "PAHD-R-Review"]


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


def smooth_mask(n: int, ranges_1based: list[tuple[int, int]], flank: int = 8) -> np.ndarray:
    mask = np.zeros(n, dtype=float)
    for start_1, end_1 in ranges_1based:
        start = max(0, start_1 - 1)
        end = min(n, end_1)
        mask[start:end] = 1.0
        for offset in range(1, flank + 1):
            decay = 1.0 - offset / (flank + 1)
            if start - offset >= 0:
                mask[start - offset] = max(mask[start - offset], decay)
            if end - 1 + offset < n:
                mask[end - 1 + offset] = max(mask[end - 1 + offset], decay)
    return mask


def shifted_ranges(ranges_1based: list[tuple[int, int]], shift: int, n: int) -> list[tuple[int, int]]:
    shifted = []
    for start, end in ranges_1based:
        s = max(1, start + shift)
        e = min(n, end + shift)
        if s <= e:
            shifted.append((s, e))
    return shifted


def domain_prior(pathogen: str, n: int, variant: str) -> np.ndarray:
    ranges = PRIOR_RANGES_1BASED.get(pathogen, [])
    if not ranges:
        return np.zeros(n, dtype=float)
    if variant == "domain_prior":
        return smooth_mask(n, ranges)
    if variant == "domain_prior_shift_plus_80":
        return smooth_mask(n, shifted_ranges(ranges, 80, n))
    if variant == "domain_prior_shift_minus_80":
        return smooth_mask(n, shifted_ranges(ranges, -80, n))
    if variant == "broad_random_region":
        digest = hashlib.sha256(pathogen.encode("utf-8")).hexdigest()
        rng = np.random.default_rng(int(digest[:8], 16))
        starts = rng.choice(np.arange(n), size=min(5, n), replace=False)
        random_ranges = [(int(s) + 1, min(n, int(s) + 45)) for s in starts]
        return smooth_mask(n, random_ranges)
    raise ValueError(variant)


def repaired_score(base_score: np.ndarray, prior: np.ndarray, weight: float) -> np.ndarray:
    if np.std(prior) < 1e-12:
        return base_score
    return (1.0 - weight) * pahd.rank_percentile(base_score) + weight * pahd.rank_percentile(prior)


def evaluate(pathogen: str, df: pd.DataFrame, mode: str, score: np.ndarray) -> dict[str, float]:
    y = df["layer_a"].astype(int).values
    frac = 0.08 if mode == "PAHD-R-Review" else 0.10
    pred = pahd.top_fraction_pred(score, frac)
    p20, _ = pahd.precision_and_enrichment(y, score, 20)
    return {
        "mcc_exact": pahd.region_mcc(y, pred, 0),
        "mcc_window_10": pahd.region_mcc(y, pred, 10),
        "precision_20": p20,
        "constrained_fpr": pahd.constrained_fpr(pathogen, len(df), pred),
        "coverage_10": pahd.expanded_coverage(pred, 10),
    }


def run() -> None:
    data = pahd.load_feature_matrices()
    benchmark = pd.read_csv(RESULTS_DIR / "multilayer_9pathogen_results.csv")
    pathogens = sorted(set(benchmark["pathogen"].unique()) & set(data.keys()))

    rows = []
    for pathogen in pathogens:
        df = data[pathogen]
        scores = decoy_audit.candidate_scores(data, pathogens, pathogen)
        for mode in MODES:
            base_score = scores[mode]
            base_metrics = evaluate(pathogen, df, mode, base_score)
            rows.append({
                "pathogen": pathogen,
                "mode": mode,
                "variant": "baseline",
                "weight": 0.0,
                **base_metrics,
            })
            for variant in [
                "domain_prior",
                "domain_prior_shift_plus_80",
                "domain_prior_shift_minus_80",
                "broad_random_region",
            ]:
                prior = domain_prior(pathogen, len(df), variant)
                for weight in WEIGHTS:
                    score = repaired_score(base_score, prior, weight)
                    metrics = evaluate(pathogen, df, mode, score)
                    rows.append({
                        "pathogen": pathogen,
                        "mode": mode,
                        "variant": variant,
                        "weight": weight,
                        **metrics,
                    })

    results = pd.DataFrame(rows)
    baseline = results[results["variant"] == "baseline"][
        ["pathogen", "mode", "mcc_exact", "mcc_window_10", "precision_20", "constrained_fpr", "coverage_10"]
    ].rename(columns={
        "mcc_exact": "baseline_mcc_exact",
        "mcc_window_10": "baseline_mcc_window_10",
        "precision_20": "baseline_precision_20",
        "constrained_fpr": "baseline_constrained_fpr",
        "coverage_10": "baseline_coverage_10",
    })
    compared = results.merge(baseline, on=["pathogen", "mode"], how="left")
    for metric in ["mcc_exact", "mcc_window_10", "precision_20", "constrained_fpr", "coverage_10"]:
        compared[f"delta_{metric}"] = compared[metric] - compared[f"baseline_{metric}"]

    weak_targets = ["MERS", "RSV", "SARS-CoV-2", "HCV"]
    weak = compared[
        (compared["pathogen"].isin(weak_targets))
        & (compared["variant"] != "baseline")
    ].copy()
    weak["objective"] = (
        weak["delta_mcc_exact"]
        + 0.35 * weak["delta_mcc_window_10"]
        + 0.50 * weak["delta_precision_20"]
        - 0.25 * weak["delta_coverage_10"].clip(lower=0)
        - 0.25 * weak["delta_constrained_fpr"].fillna(0).clip(lower=0)
    )

    best_by_target = (
        weak.sort_values(["pathogen", "mode", "objective"], ascending=[True, True, False])
        .groupby(["pathogen", "mode"])
        .head(1)
        .reset_index(drop=True)
    )

    global_summary = (
        compared.groupby(["mode", "variant", "weight"])
        .agg(
            mean_mcc_exact=("mcc_exact", "mean"),
            mean_mcc_window_10=("mcc_window_10", "mean"),
            mean_precision_20=("precision_20", "mean"),
            mean_constrained_fpr=("constrained_fpr", "mean"),
            mean_coverage_10=("coverage_10", "mean"),
            mean_delta_mcc_exact=("delta_mcc_exact", "mean"),
            mean_delta_precision_20=("delta_precision_20", "mean"),
        )
        .reset_index()
        .sort_values(["mode", "variant", "weight"])
    )

    domain_summary = global_summary[global_summary["variant"] == "domain_prior"].copy()
    shifted_summary = global_summary[global_summary["variant"].str.contains("shift|random", regex=True)].copy()
    adoption = best_by_target[
        (best_by_target["variant"] == "domain_prior")
        & (best_by_target["delta_mcc_exact"] > 0)
        & (best_by_target["delta_precision_20"] >= 0)
    ].copy()

    results.to_csv(RESULTS_DIR / "pahd_r_domain_prior_repair_results.csv", index=False)
    compared.to_csv(RESULTS_DIR / "pahd_r_domain_prior_repair_compared.csv", index=False)
    best_by_target.to_csv(RESULTS_DIR / "pahd_r_domain_prior_repair_best_by_target.csv", index=False)
    global_summary.to_csv(RESULTS_DIR / "pahd_r_domain_prior_repair_global_summary.csv", index=False)

    report = [
        "# PAHD-R Domain-Prior Repair Test",
        "",
        "Date: 2026-04-26 KST",
        "",
        "## Best Weak-Target Rows",
        "",
        markdown_table(best_by_target[[
            "pathogen",
            "mode",
            "variant",
            "weight",
            "mcc_exact",
            "delta_mcc_exact",
            "mcc_window_10",
            "delta_mcc_window_10",
            "precision_20",
            "delta_precision_20",
            "constrained_fpr",
            "coverage_10",
            "objective",
        ]]),
        "",
        "## Adoptable Domain-Prior Rows",
        "",
        markdown_table(adoption[[
            "pathogen",
            "mode",
            "variant",
            "weight",
            "delta_mcc_exact",
            "delta_mcc_window_10",
            "delta_precision_20",
            "delta_constrained_fpr",
            "delta_coverage_10",
        ]]) if len(adoption) else "No domain-prior rows met the adoption filter.",
        "",
        "## Domain-Prior Global Summary",
        "",
        markdown_table(domain_summary),
        "",
        "## Shifted/Random Prior Global Control Summary",
        "",
        markdown_table(shifted_summary.head(30)),
        "",
        "## Interpretation",
        "",
        "- A domain prior is considered adoptable only if it improves exact MCC and does not reduce Precision@20 for the target row.",
        "- Shifted and random region controls are included because broad masks can improve window metrics without real coordinate recovery.",
        "- Rows that improve only MCC +/-10 should be treated as region-review hints, not exact predictor improvements.",
        "",
    ]
    out = RESULTS_DIR / "pahd_r_domain_prior_repair_audit.md"
    out.write_text("\n".join(report), encoding="utf-8")
    print(out)
    print(best_by_target.round(4).to_string(index=False))
    print()
    print(adoption.round(4).to_string(index=False) if len(adoption) else "No adoptable domain-prior rows.")


if __name__ == "__main__":
    run()
