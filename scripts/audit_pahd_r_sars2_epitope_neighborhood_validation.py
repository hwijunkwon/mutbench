#!/usr/bin/env python3
"""Predeclared SARS-CoV-2 RBD epitope-neighborhood validation.

This audit evaluates the SARS-CoV-2 Review repair candidate against a
predeclared RBD neighborhood label set, instead of expanding labels after
looking at candidate predictions.
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
import test_pahd_r_domain_prior_repair as repair  # noqa: E402


PATHOGEN = "SARS-CoV-2"
MODE = "PAHD-R-Review"
REPAIR_REGION = [(346, 346), (371, 376), (405, 408), (417, 417), (440, 446), (452, 460), (478, 501)]
REPAIR_WEIGHT = 0.20
N_PERM = 500

# Predeclared from RBD escape/convergent-evolution literature and Layer A
# evidence sources, not from PAHD-R candidate top predictions.
EPITOPE_NEIGHBORHOODS_1BASED = {
    "r346_cluster": (344, 348),
    "s371_t376_omicron_cluster": (369, 378),
    "d405_r408_cluster": (403, 410),
    "k417_region": (415, 419),
    "k440_g446_region": (438, 448),
    "l452_n460_region": (450, 462),
    "t478_e484_region": (476, 486),
    "f490_q501_region": (488, 503),
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


def label_mask(n: int, neighborhoods: dict[str, tuple[int, int]]) -> np.ndarray:
    mask = np.zeros(n, dtype=int)
    for start_1, end_1 in neighborhoods.values():
        start = max(0, start_1 - 1)
        end = min(n, end_1)
        mask[start:end] = 1
    return mask


def random_matched_prior(n: int, ranges: list[tuple[int, int]]) -> np.ndarray:
    total_width = sum(end - start + 1 for start, end in ranges)
    mean_width = max(5, int(round(total_width / max(1, len(ranges)))))
    digest = hashlib.sha256(f"{PATHOGEN}:manual_neighborhood".encode("utf-8")).hexdigest()
    rng = np.random.default_rng(int(digest[:8], 16))
    starts = rng.choice(np.arange(1, n + 1), size=len(ranges), replace=False)
    random_ranges = [(int(s), min(n, int(s) + mean_width - 1)) for s in starts]
    return repair.smooth_mask(n, random_ranges)


def shifted_ranges(ranges: list[tuple[int, int]], shift: int, n: int) -> list[tuple[int, int]]:
    out = []
    for start, end in ranges:
        s = max(1, start + shift)
        e = min(n, end + shift)
        if s <= e:
            out.append((s, e))
    return out


def eval_against_labels(y: np.ndarray, score: np.ndarray, frac: float = 0.08) -> dict[str, float]:
    pred = pahd.top_fraction_pred(score, frac)
    p20, _ = pahd.precision_and_enrichment(y, score, 20)
    p50, _ = pahd.precision_and_enrichment(y, score, 50)
    return {
        "mcc_exact": pahd.region_mcc(y, pred, 0),
        "mcc_window_10": pahd.region_mcc(y, pred, 10),
        "precision_20": p20,
        "precision_50": p50,
        "recall_top_frac": float(np.sum(pred & (y > 0)) / max(1, int(y.sum()))),
        "coverage_10": pahd.expanded_coverage(pred, 10),
        "n_positive": int(y.sum()),
        "n_predicted": int(pred.sum()),
    }


def permutation_p(y: np.ndarray, score: np.ndarray, rng: np.random.Generator) -> tuple[float, float, float]:
    pred = pahd.top_fraction_pred(score, 0.08)
    observed = pahd.region_mcc(y, pred, 0)
    null = np.array([pahd.region_mcc(rng.permutation(y), pred, 0) for _ in range(N_PERM)])
    return float(null.mean()), float(np.quantile(null, 0.95)), float(np.mean(null >= observed))


def run() -> None:
    data = pahd.load_feature_matrices()
    benchmark = pd.read_csv(RESULTS_DIR / "multilayer_9pathogen_results.csv")
    pathogens = sorted(set(benchmark["pathogen"].unique()) & set(data.keys()))
    df = data[PATHOGEN]
    n = len(df)
    base = decoy_audit.candidate_scores(data, pathogens, PATHOGEN)[MODE]
    rng = np.random.default_rng(20260426)

    real_prior = repair.smooth_mask(n, REPAIR_REGION)
    variants = {
        "baseline_review": base,
        "rbd_ace2_escape_repair": repair.repaired_score(base, real_prior, REPAIR_WEIGHT),
        "shift_plus_80_control": repair.repaired_score(base, repair.smooth_mask(n, shifted_ranges(REPAIR_REGION, 80, n)), REPAIR_WEIGHT),
        "shift_minus_80_control": repair.repaired_score(base, repair.smooth_mask(n, shifted_ranges(REPAIR_REGION, -80, n)), REPAIR_WEIGHT),
        "random_matched_control": repair.repaired_score(base, random_matched_prior(n, REPAIR_REGION), REPAIR_WEIGHT),
    }

    exact_y = df["layer_a"].astype(int).values
    neighborhood_y = label_mask(n, EPITOPE_NEIGHBORHOODS_1BASED)

    rows = []
    for label_set, y in [("exact_layer_a", exact_y), ("predeclared_rbd_neighborhood", neighborhood_y)]:
        base_metrics = eval_against_labels(y, variants["baseline_review"])
        for variant, score in variants.items():
            metrics = eval_against_labels(y, score)
            null_mean, null_p95, empirical_p = permutation_p(y, score, rng)
            rows.append({
                "label_set": label_set,
                "variant": variant,
                **metrics,
                "delta_precision_20": metrics["precision_20"] - base_metrics["precision_20"],
                "delta_mcc_exact": metrics["mcc_exact"] - base_metrics["mcc_exact"],
                "delta_mcc_window_10": metrics["mcc_window_10"] - base_metrics["mcc_window_10"],
                "null_mean_mcc": null_mean,
                "null_p95_mcc": null_p95,
                "empirical_p_null_ge_observed": empirical_p,
            })

    results = pd.DataFrame(rows)
    neighborhood = results[results["label_set"] == "predeclared_rbd_neighborhood"].copy()
    candidate = neighborhood[neighborhood["variant"] == "rbd_ace2_escape_repair"].iloc[0]
    controls = neighborhood[neighborhood["variant"].str.contains("control", regex=False)]
    best_control = controls.sort_values(["precision_20", "mcc_exact"], ascending=False).iloc[0]
    mcc_margin = candidate["mcc_exact"] - best_control["mcc_exact"]
    decision = pd.DataFrame([{
        "candidate": "SARS-CoV-2 rbd_ace2_escape + PAHD-R-Review",
        "label_set": "predeclared_rbd_neighborhood",
        "candidate_precision_20": candidate["precision_20"],
        "baseline_precision_20": neighborhood[neighborhood["variant"] == "baseline_review"].iloc[0]["precision_20"],
        "best_control": best_control["variant"],
        "best_control_precision_20": best_control["precision_20"],
        "candidate_mcc_exact": candidate["mcc_exact"],
        "best_control_mcc_exact": best_control["mcc_exact"],
        "candidate_mcc_margin_vs_control": mcc_margin,
        "candidate_permutation_p": candidate["empirical_p_null_ge_observed"],
        "beats_baseline_precision": candidate["precision_20"] > neighborhood[neighborhood["variant"] == "baseline_review"].iloc[0]["precision_20"],
        "beats_control_precision": candidate["precision_20"] >= best_control["precision_20"],
        "beats_or_ties_control_mcc": mcc_margin >= -1e-12,
        "passes_permutation": candidate["empirical_p_null_ge_observed"] <= 0.01,
    }])
    decision["adoption_decision"] = np.where(
        decision["beats_baseline_precision"]
        & decision["beats_control_precision"]
        & decision["beats_or_ties_control_mcc"]
        & decision["passes_permutation"],
        "neighborhood_validated_candidate",
        "hold",
    )

    results.to_csv(RESULTS_DIR / "pahd_r_sars2_epitope_neighborhood_validation_results.csv", index=False)
    decision.to_csv(RESULTS_DIR / "pahd_r_sars2_epitope_neighborhood_validation_decision.csv", index=False)

    report = [
        "# PAHD-R SARS-CoV-2 Epitope-Neighborhood Validation",
        "",
        "Date: 2026-04-26 KST",
        "",
        "## Predeclared Neighborhoods",
        "",
        markdown_table(pd.DataFrame([
            {"neighborhood": name, "start_1based": start, "end_1based": end}
            for name, (start, end) in EPITOPE_NEIGHBORHOODS_1BASED.items()
        ])),
        "",
        "## Decision",
        "",
        markdown_table(decision),
        "",
        "## Full Results",
        "",
        markdown_table(results),
        "",
        "## Interpretation",
        "",
        "- This audit uses predeclared RBD epitope-neighborhood labels rather than labels expanded after seeing predictions.",
        "- The candidate is promoted only if it beats baseline and shifted/random controls on neighborhood precision and MCC.",
        "- Exact Layer A results are retained separately to avoid changing the original endpoint.",
        "",
    ]
    out = RESULTS_DIR / "pahd_r_sars2_epitope_neighborhood_validation.md"
    out.write_text("\n".join(report), encoding="utf-8")
    print(out)
    print(decision.round(4).to_string(index=False))
    print(neighborhood.round(4).to_string(index=False))


if __name__ == "__main__":
    run()
