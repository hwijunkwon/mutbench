#!/usr/bin/env python3
"""Narrow-prior repair redesign for MERS and RSV weak cases."""

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


MODES = ["PAHD-R-Core", "PAHD-R-Augmented", "PAHD-R-Review"]
WEIGHTS = [0.05, 0.10, 0.15, 0.20, 0.30]
N_PERM = 300

PRIORS = {
    "MERS": {
        # Narrow DPP4-interface/contact neighborhoods from structural studies:
        # S465, Y499, L506/D510, and E536-D539/DPP4 patch residues.
        "dpp4_exact_contacts": [(465, 465), (499, 499), (506, 510), (536, 539)],
        "dpp4_escape_neighborhood": [(484, 484), (506, 511), (530, 542)],
        "dpp4_combined_narrow": [(465, 465), (484, 484), (499, 499), (506, 511), (530, 542)],
    },
    "RSV": {
        # Narrow antibody/escape regions, replacing the earlier broad site masks.
        "site_ii_palivizumab": [(255, 276)],
        "site_v_escape": [(422, 429)],
        "site_zero_nirsevimab": [(68, 68), (208, 208)],
        "adaptive_antibody_sites": [(148, 174), (255, 276), (422, 429)],
        "compact_escape_sites": [(148, 163), (255, 276), (422, 429)],
    },
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


def shifted_ranges(ranges: list[tuple[int, int]], shift: int, n: int) -> list[tuple[int, int]]:
    out = []
    for start, end in ranges:
        s = max(1, start + shift)
        e = min(n, end + shift)
        if s <= e:
            out.append((s, e))
    return out


def random_matched_ranges(pathogen: str, prior_name: str, ranges: list[tuple[int, int]], n: int) -> list[tuple[int, int]]:
    digest = hashlib.sha256(f"{pathogen}:{prior_name}".encode("utf-8")).hexdigest()
    rng = np.random.default_rng(int(digest[:8], 16))
    widths = [end - start + 1 for start, end in ranges]
    starts = rng.choice(np.arange(1, n + 1), size=len(widths), replace=False)
    return [(int(start), min(n, int(start) + width - 1)) for start, width in zip(starts, widths)]


def make_prior(pathogen: str, prior_name: str, n: int, control: str) -> np.ndarray:
    ranges = PRIORS[pathogen][prior_name]
    if control == "real":
        return repair.smooth_mask(n, ranges, flank=3)
    if control == "shift_plus_80":
        return repair.smooth_mask(n, shifted_ranges(ranges, 80, n), flank=3)
    if control == "shift_minus_80":
        return repair.smooth_mask(n, shifted_ranges(ranges, -80, n), flank=3)
    if control == "random_matched":
        return repair.smooth_mask(n, random_matched_ranges(pathogen, prior_name, ranges, n), flank=3)
    raise ValueError(control)


def evaluate(pathogen: str, df: pd.DataFrame, mode: str, score: np.ndarray, y: np.ndarray | None = None) -> dict[str, float]:
    labels = df["layer_a"].astype(int).values if y is None else y.astype(int)
    frac = 0.08 if mode == "PAHD-R-Review" else 0.10
    pred = pahd.top_fraction_pred(score, frac)
    p20, _ = pahd.precision_and_enrichment(labels, score, 20)
    return {
        "mcc_exact": pahd.region_mcc(labels, pred, 0),
        "mcc_window_10": pahd.region_mcc(labels, pred, 10),
        "precision_20": p20,
        "constrained_fpr": pahd.constrained_fpr(pathogen, len(df), pred),
        "coverage_10": pahd.expanded_coverage(pred, 10),
    }


def permutation_p(y: np.ndarray, score: np.ndarray, mode: str, rng: np.random.Generator) -> tuple[float, float, float]:
    frac = 0.08 if mode == "PAHD-R-Review" else 0.10
    pred = pahd.top_fraction_pred(score, frac)
    observed = pahd.region_mcc(y, pred, 0)
    null = np.array([pahd.region_mcc(rng.permutation(y), pred, 0) for _ in range(N_PERM)])
    return float(null.mean()), float(np.quantile(null, 0.95)), float(np.mean(null >= observed))


def load_rsv_dms_labels(n: int) -> np.ndarray:
    path = RESULTS_DIR / "dms_data" / "rsv_dms_new.csv"
    df = pd.read_csv(path)
    y = np.zeros(n, dtype=int)
    for pos in df.loc[df["layer_c"] > 0, "position"].astype(int):
        idx = pos - 1
        if 0 <= idx < n:
            y[idx] = 1
    return y


def run() -> None:
    data = pahd.load_feature_matrices()
    benchmark = pd.read_csv(RESULTS_DIR / "multilayer_9pathogen_results.csv")
    pathogens = sorted(set(benchmark["pathogen"].unique()) & set(data.keys()))
    rng = np.random.default_rng(20260426)
    rows = []

    for pathogen in ["MERS", "RSV"]:
        df = data[pathogen]
        scores = decoy_audit.candidate_scores(data, pathogens, pathogen)
        dms_y = load_rsv_dms_labels(len(df)) if pathogen == "RSV" else None
        for mode in MODES:
            base = scores[mode]
            base_metrics = evaluate(pathogen, df, mode, base)
            base_dms = evaluate(pathogen, df, mode, base, dms_y) if dms_y is not None else {}
            for prior_name in PRIORS[pathogen]:
                for control in ["real", "shift_plus_80", "shift_minus_80", "random_matched"]:
                    prior = make_prior(pathogen, prior_name, len(df), control)
                    for weight in WEIGHTS:
                        score = repair.repaired_score(base, prior, weight)
                        metrics = evaluate(pathogen, df, mode, score)
                        null_mean, null_p95, empirical_p = permutation_p(df["layer_a"].astype(int).values, score, mode, rng)
                        row = {
                            "pathogen": pathogen,
                            "mode": mode,
                            "prior": prior_name,
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
                        }
                        if dms_y is not None:
                            dms_metrics = evaluate(pathogen, df, mode, score, dms_y)
                            row.update({
                                "dms_mcc_exact": dms_metrics["mcc_exact"],
                                "dms_precision_20": dms_metrics["precision_20"],
                                "delta_dms_precision_20": dms_metrics["precision_20"] - base_dms["precision_20"],
                            })
                        rows.append(row)

    results = pd.DataFrame(rows)
    decisions = []
    for (pathogen, mode, prior), group in results.groupby(["pathogen", "mode", "prior"]):
        real = group[group["control"] == "real"].copy()
        controls = group[group["control"] != "real"].copy()
        if real.empty or controls.empty:
            continue
        best_real = real.sort_values(["delta_precision_20", "delta_mcc_exact", "precision_20"], ascending=False).iloc[0]
        best_control = controls.sort_values(["precision_20", "mcc_exact"], ascending=False).iloc[0]
        decision = {
            "pathogen": pathogen,
            "mode": mode,
            "prior": prior,
            "weight": best_real["weight"],
            "mcc_exact": best_real["mcc_exact"],
            "delta_mcc_exact": best_real["delta_mcc_exact"],
            "precision_20": best_real["precision_20"],
            "delta_precision_20": best_real["delta_precision_20"],
            "constrained_fpr": best_real["constrained_fpr"],
            "coverage_10": best_real["coverage_10"],
            "empirical_p_null_ge_observed": best_real["empirical_p_null_ge_observed"],
            "best_control": best_control["control"],
            "best_control_mcc_exact": best_control["mcc_exact"],
            "best_control_precision_20": best_control["precision_20"],
            "beats_control_precision": best_real["precision_20"] >= best_control["precision_20"],
            "beats_control_mcc": best_real["mcc_exact"] > best_control["mcc_exact"],
            "passes_permutation": best_real["empirical_p_null_ge_observed"] <= 0.01,
        }
        if pathogen == "RSV":
            best_control_dms = controls.sort_values(["dms_precision_20", "dms_mcc_exact"], ascending=False).iloc[0]
            decision.update({
                "dms_precision_20": best_real.get("dms_precision_20", np.nan),
                "delta_dms_precision_20": best_real.get("delta_dms_precision_20", np.nan),
                "best_control_dms_precision_20": best_control_dms.get("dms_precision_20", np.nan),
                "beats_control_dms_precision": best_real.get("dms_precision_20", -np.inf) >= best_control_dms.get("dms_precision_20", np.inf),
            })
        decisions.append(decision)

    decisions_df = pd.DataFrame(decisions)
    def decide(row: pd.Series) -> str:
        if not (row["delta_mcc_exact"] > 0 and row["delta_precision_20"] >= 0):
            return "reject"
        if not (row["beats_control_precision"] and row["beats_control_mcc"] and row["passes_permutation"]):
            return "reject"
        if row["pathogen"] == "RSV" and not bool(row.get("beats_control_dms_precision", False)):
            return "hold_external_dms"
        return "candidate"

    decisions_df["adoption_decision"] = decisions_df.apply(decide, axis=1)
    results.to_csv(RESULTS_DIR / "pahd_r_mers_rsv_narrow_prior_results.csv", index=False)
    decisions_df.to_csv(RESULTS_DIR / "pahd_r_mers_rsv_narrow_prior_decisions.csv", index=False)

    best = decisions_df.sort_values(["adoption_decision", "pathogen", "mode", "delta_mcc_exact"], ascending=[True, True, True, False])
    report = [
        "# PAHD-R MERS/RSV Narrow-Prior Repair Redesign",
        "",
        "Date: 2026-04-26 KST",
        "",
        "## Decision Rows",
        "",
        markdown_table(best),
        "",
        "## Interpretation",
        "",
        "- MERS priors were narrowed from broad RBD regions to DPP4 contact/escape neighborhoods.",
        "- RSV priors were narrowed from broad antigenic regions to antibody/escape-site neighborhoods.",
        "- RSV candidates additionally need to avoid losing to shifted/random controls on local DMS Layer C precision.",
        "- Rows that lose to shifted/random controls remain rejected even if they improve over baseline.",
        "",
    ]
    out = RESULTS_DIR / "pahd_r_mers_rsv_narrow_prior_redesign.md"
    out.write_text("\n".join(report), encoding="utf-8")
    print(out)
    print(best.round(4).to_string(index=False))


if __name__ == "__main__":
    run()
