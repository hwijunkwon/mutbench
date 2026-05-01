#!/usr/bin/env python3
"""SARS-CoV-2 external DMS validation for the PAHD-R Review repair candidate."""

from __future__ import annotations

from pathlib import Path
import hashlib
import sys

import numpy as np
import pandas as pd
from sklearn.metrics import roc_auc_score

PROJECT_ROOT = Path(__file__).resolve().parent.parent
RESULTS_DIR = PROJECT_ROOT / "results" / "mutbench"
sys.path.insert(0, str(PROJECT_ROOT / "scripts"))
import audit_pahd_r_decoy_coordinate_robustness as decoy_audit  # noqa: E402
import run_pahd_r_multi_hypothesis as pahd  # noqa: E402
import test_pahd_r_domain_prior_repair as repair  # noqa: E402


PATHOGEN = "SARS-CoV-2"
MODE = "PAHD-R-Review"
RBD_ACE2_ESCAPE = [(346, 346), (371, 376), (405, 408), (417, 417), (440, 446), (452, 460), (478, 501)]
WEIGHT = 0.20


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


def shifted_ranges(ranges: list[tuple[int, int]], shift: int, n: int) -> list[tuple[int, int]]:
    out = []
    for start, end in ranges:
        s = max(1, start + shift)
        e = min(n, end + shift)
        if s <= e:
            out.append((s, e))
    return out


def random_matched_prior(n: int) -> np.ndarray:
    widths = [end - start + 1 for start, end in RBD_ACE2_ESCAPE]
    digest = hashlib.sha256(f"{PATHOGEN}:external_dms".encode("utf-8")).hexdigest()
    rng = np.random.default_rng(int(digest[:8], 16))
    starts = rng.choice(np.arange(1, n + 1), size=len(widths), replace=False)
    ranges = [(int(start), min(n, int(start) + width - 1)) for start, width in zip(starts, widths)]
    return repair.smooth_mask(n, ranges)


def load_sars2_dms(n: int) -> tuple[np.ndarray, np.ndarray]:
    dms = pd.read_csv(RESULTS_DIR / "dms_data" / "sars2_dms.csv")
    y = np.zeros(n, dtype=int)
    fitness = np.zeros(n, dtype=float)
    for _, row in dms.iterrows():
        idx = int(row["position"]) - 1
        if 0 <= idx < n:
            y[idx] = int(row["layer_c"] > 0)
            fitness[idx] = float(row["fitness_score"])
    return y, fitness


def evaluate(y: np.ndarray, score: np.ndarray, frac: float = 0.08) -> dict[str, float]:
    pred = pahd.top_fraction_pred(score, frac)
    p20, _ = pahd.precision_and_enrichment(y, score, 20)
    p50, _ = pahd.precision_and_enrichment(y, score, 50)
    auroc = float(roc_auc_score(y, score)) if y.sum() > 1 and (len(y) - y.sum()) > 1 else np.nan
    return {
        "mcc_exact": pahd.region_mcc(y, pred, 0),
        "mcc_window_10": pahd.region_mcc(y, pred, 10),
        "precision_20": p20,
        "precision_50": p50,
        "auroc": auroc,
        "recall_top_frac": float(np.sum(pred & (y > 0)) / max(1, int(y.sum()))),
        "coverage_10": pahd.expanded_coverage(pred, 10),
    }


def run() -> None:
    data = pahd.load_feature_matrices()
    benchmark = pd.read_csv(RESULTS_DIR / "multilayer_9pathogen_results.csv")
    pathogens = sorted(set(benchmark["pathogen"].unique()) & set(data.keys()))
    df = data[PATHOGEN]
    n = len(df)
    base = decoy_audit.candidate_scores(data, pathogens, PATHOGEN)[MODE]
    y_dms, fitness = load_sars2_dms(n)

    variants = {
        "baseline_review": base,
        "rbd_ace2_escape_repair": repair.repaired_score(base, repair.smooth_mask(n, RBD_ACE2_ESCAPE), WEIGHT),
        "shift_plus_80_control": repair.repaired_score(base, repair.smooth_mask(n, shifted_ranges(RBD_ACE2_ESCAPE, 80, n)), WEIGHT),
        "shift_minus_80_control": repair.repaired_score(base, repair.smooth_mask(n, shifted_ranges(RBD_ACE2_ESCAPE, -80, n)), WEIGHT),
        "random_matched_control": repair.repaired_score(base, random_matched_prior(n), WEIGHT),
    }

    rows = []
    for name, score in variants.items():
        metrics = evaluate(y_dms, score)
        top20 = np.argsort(-score)[:20]
        rows.append({
            "variant": name,
            **metrics,
            "mean_top20_dms_fitness": float(np.mean(fitness[top20])),
            "median_top20_dms_fitness": float(np.median(fitness[top20])),
            "n_dms_positive": int(y_dms.sum()),
        })
    results = pd.DataFrame(rows)
    candidate = results[results["variant"] == "rbd_ace2_escape_repair"].iloc[0]
    baseline = results[results["variant"] == "baseline_review"].iloc[0]
    controls = results[results["variant"].str.contains("control", regex=False)]
    best_control = controls.sort_values(["precision_20", "mcc_exact"], ascending=False).iloc[0]
    decision = pd.DataFrame([{
        "candidate": "SARS-CoV-2 rbd_ace2_escape + PAHD-R-Review",
        "candidate_dms_precision_20": candidate["precision_20"],
        "baseline_dms_precision_20": baseline["precision_20"],
        "best_control": best_control["variant"],
        "best_control_dms_precision_20": best_control["precision_20"],
        "candidate_dms_mcc": candidate["mcc_exact"],
        "best_control_dms_mcc": best_control["mcc_exact"],
        "candidate_dms_auroc": candidate["auroc"],
        "baseline_dms_auroc": baseline["auroc"],
        "beats_baseline_dms_precision": candidate["precision_20"] > baseline["precision_20"],
        "beats_control_dms_precision": candidate["precision_20"] >= best_control["precision_20"],
        "beats_control_dms_mcc": candidate["mcc_exact"] > best_control["mcc_exact"],
    }])
    decision["external_dms_decision"] = np.where(
        decision["beats_baseline_dms_precision"]
        & decision["beats_control_dms_precision"]
        & decision["beats_control_dms_mcc"],
        "external_dms_supported",
        "external_dms_hold",
    )

    results.to_csv(RESULTS_DIR / "pahd_r_sars2_external_dms_validation_results.csv", index=False)
    decision.to_csv(RESULTS_DIR / "pahd_r_sars2_external_dms_validation_decision.csv", index=False)

    report = [
        "# PAHD-R SARS-CoV-2 External DMS Validation",
        "",
        "Date: 2026-04-26 KST",
        "",
        "## Decision",
        "",
        markdown_table(decision),
        "",
        "## Variant Results",
        "",
        markdown_table(results),
        "",
        "## Interpretation",
        "",
        "- This audit uses the local SARS-CoV-2 DMS Layer C table as an external functional validation layer.",
        "- The candidate must beat baseline and shifted/random controls on DMS Precision@20 and MCC to be considered externally supported.",
        "- This does not convert the candidate into an adopted exact-site Layer A repair; it only supports the RBD-neighborhood review interpretation.",
        "",
    ]
    out = RESULTS_DIR / "pahd_r_sars2_external_dms_validation.md"
    out.write_text("\n".join(report), encoding="utf-8")
    print(out)
    print(decision.round(4).to_string(index=False))
    print(results.round(4).to_string(index=False))


if __name__ == "__main__":
    run()
