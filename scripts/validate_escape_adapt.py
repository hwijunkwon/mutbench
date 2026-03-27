#!/usr/bin/env python3
"""Validate MutBench-Adapt EqualWeight ensemble against known vaccine escape positions.

Computes enrichment ratios and Fisher's exact test for:
  1. SARS-CoV-2 Spike vaccine escape sites
  2. H3N2 HA antigenic drift sites
  3. Comparison table: FreqThresh vs EqualWeight vs BestSingle(oracle)

Uses the 10-feature EqualWeight ensemble with top-10% threshold
(best-performing strategy from LOPO evaluation).

Note: For FreqThresh, if many positions share the threshold value (common
with sparse frequency distributions like SARS-CoV-2), positions with
freq > strict_threshold are selected rather than >= to avoid trivially
selecting all positions.
"""

from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
import pandas as pd
from scipy.stats import fisher_exact

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT / "tools"))

from mutbench_adapt.adapt_v2 import (
    FEATURE_NAMES,
    compute_scores,
    apply_threshold,
    load_feature_matrix,
    baseline_best_single,
)

# ---------------------------------------------------------------------------
# Known escape / antigenic drift positions (0-based AA index)
# ---------------------------------------------------------------------------
ESCAPE_SITES: dict[str, dict[str, set[int]]] = {
    "SARS-CoV-2": {
        "description": "Vaccine escape (RBD + NTD + S2)",
        "positions": {
            # Key RBD escape sites
            484, 417, 452, 501, 478, 493, 446, 477, 486, 346,
            # Additional Spike escape
            614, 681, 655, 679, 969,
        },
    },
    "H3N2": {
        "description": "Antigenic drift (sites A+B + recent drift)",
        "positions": {
            # Antigenic site A
            122, 124, 126, 131, 133, 135, 137, 142, 143, 144, 145,
            # Antigenic site B
            155, 156, 157, 158, 159, 160, 163, 164, 186, 188, 189,
            190, 192, 193, 194, 196, 197, 198,
        },
    },
}


def compute_enrichment(
    detected: np.ndarray,
    escape_mask: np.ndarray,
) -> dict:
    """Compute enrichment ratio and Fisher's exact test.

    Enrichment = (escape_in_detected / n_detected) / (n_escape / n_total)
    """
    n_total = len(detected)
    n_detected = int(detected.sum())
    n_escape = int(escape_mask.sum())

    overlap = int((detected & escape_mask).sum())

    if n_detected == 0 or n_escape == 0:
        enrichment = 0.0
    else:
        obs_rate = overlap / n_detected
        exp_rate = n_escape / n_total
        enrichment = obs_rate / exp_rate if exp_rate > 0 else 0.0

    # Fisher's exact test (2x2 contingency table)
    a = overlap
    b = n_detected - overlap
    c = n_escape - overlap
    d = n_total - n_detected - c
    odds_ratio, p_value = fisher_exact([[a, b], [c, d]], alternative="greater")

    return {
        "n_total": n_total,
        "n_detected": n_detected,
        "n_escape": n_escape,
        "n_overlap": overlap,
        "enrichment": round(enrichment, 3),
        "odds_ratio": round(odds_ratio, 3) if np.isfinite(odds_ratio) else float("inf"),
        "p_value": p_value,
        "recall": round(overlap / n_escape, 4) if n_escape > 0 else 0.0,
        "precision": round(overlap / n_detected, 4) if n_detected > 0 else 0.0,
    }


def freq_threshold_robust(scores: np.ndarray, frac: float) -> np.ndarray:
    """Top-k thresholding with guard against degenerate distributions.

    If the percentile threshold selects > 50% of positions (indicating many
    ties at the threshold), use strict > instead of >=.
    """
    thr = np.percentile(scores, 100 * (1 - frac))
    pred = scores >= thr
    # Guard: if selecting more than 2x expected, use strict inequality
    if pred.sum() > len(scores) * frac * 2:
        pred = scores > thr
    return pred


def run_method(
    df: pd.DataFrame,
    method_name: str,
    frac: float = 0.10,
) -> np.ndarray:
    """Return boolean prediction array for a given method."""
    thr_config = {"type": "topk", "frac": frac}

    if method_name == "EqualWeight":
        w = np.ones(10) / 10.0
        s = np.ones(10)
        scores = compute_scores(df, w, s)
        return apply_threshold(scores, thr_config)
    elif method_name == "FreqThresh":
        scores = df["freq"].values.copy()
        return freq_threshold_robust(scores, frac)
    elif method_name == "BestSingle":
        return baseline_best_single(df, thr_config)
    else:
        raise ValueError(f"Unknown method: {method_name}")


def main():
    frac = 0.10
    methods = ["FreqThresh", "EqualWeight", "BestSingle"]

    all_rows = []

    for pathogen, info in ESCAPE_SITES.items():
        escape_pos = info["positions"]
        desc = info["description"]

        print(f"\n{'='*70}")
        print(f"  {pathogen}: {desc}")
        print(f"{'='*70}")

        df = load_feature_matrix(pathogen)
        n_positions = len(df)

        # Build escape mask (0-based)
        escape_mask = np.zeros(n_positions, dtype=bool)
        valid_escape = set()
        for pos in escape_pos:
            if pos < n_positions:
                escape_mask[pos] = True
                valid_escape.add(pos)

        n_escape = int(escape_mask.sum())
        print(f"  Positions: {n_positions}, Escape sites: {n_escape}")
        print(f"  Escape positions (0-based): {sorted(valid_escape)}")

        for method in methods:
            pred = run_method(df, method, frac)
            result = compute_enrichment(pred, escape_mask)

            # Which escape sites were detected?
            detected_escape = sorted(
                pos for pos in valid_escape if pred[pos]
            )

            print(f"\n  [{method}]")
            print(f"    Detected: {result['n_detected']}, "
                  f"Escape in detected: {result['n_overlap']}/{n_escape}")
            print(f"    Enrichment: {result['enrichment']:.3f}x, "
                  f"Fisher p={result['p_value']:.6f}")
            print(f"    Precision: {result['precision']:.4f}, "
                  f"Recall: {result['recall']:.4f}")
            if detected_escape:
                print(f"    Detected escape sites: {detected_escape}")

            all_rows.append({
                "pathogen": pathogen,
                "method": method,
                "threshold": f"top{int(frac*100)}",
                "description": desc,
                "n_positions": result["n_total"],
                "n_detected": result["n_detected"],
                "n_escape": result["n_escape"],
                "n_overlap": result["n_overlap"],
                "enrichment": result["enrichment"],
                "odds_ratio": result["odds_ratio"],
                "p_value": result["p_value"],
                "precision": result["precision"],
                "recall": result["recall"],
                "detected_escape_sites": str(detected_escape) if detected_escape else "",
            })

    # ---------------------------------------------------------------------------
    # Additional thresholds (top5, top3) for sensitivity analysis
    # ---------------------------------------------------------------------------
    print(f"\n\n{'='*70}")
    print("  Sensitivity analysis: varying thresholds")
    print(f"{'='*70}")
    for extra_frac in [0.05, 0.03]:
        label = f"top{int(extra_frac*100)}"
        for pathogen, info in ESCAPE_SITES.items():
            df = load_feature_matrix(pathogen)
            n_positions = len(df)
            escape_mask = np.zeros(n_positions, dtype=bool)
            for pos in info["positions"]:
                if pos < n_positions:
                    escape_mask[pos] = True

            for method in methods:
                pred = run_method(df, method, extra_frac)
                result = compute_enrichment(pred, escape_mask)
                detected_escape = sorted(
                    pos for pos in info["positions"] if pos < n_positions and pred[pos]
                )
                all_rows.append({
                    "pathogen": pathogen,
                    "method": method,
                    "threshold": label,
                    "description": info["description"],
                    "n_positions": result["n_total"],
                    "n_detected": result["n_detected"],
                    "n_escape": result["n_escape"],
                    "n_overlap": result["n_overlap"],
                    "enrichment": result["enrichment"],
                    "odds_ratio": result["odds_ratio"],
                    "p_value": result["p_value"],
                    "precision": result["precision"],
                    "recall": result["recall"],
                    "detected_escape_sites": str(detected_escape) if detected_escape else "",
                })
                print(f"  {pathogen:<14} {method:<14} {label:<6} "
                      f"det={result['n_detected']:>4}, "
                      f"esc={result['n_overlap']:>3}/{result['n_escape']}, "
                      f"enrich={result['enrichment']:.3f}x, "
                      f"p={result['p_value']:.4f}")

    # ---------------------------------------------------------------------------
    # Comparison table (top10 only)
    # ---------------------------------------------------------------------------
    top10_rows = [r for r in all_rows if r["threshold"] == "top10"]
    print(f"\n\n{'='*100}")
    print("  Comparison Table: Enrichment of Escape Sites in Detected Hotspots (top-10%)")
    print(f"{'='*100}")
    print(f"{'Pathogen':<14} {'Method':<14} {'Detected':>9} {'Escape/Det':>11} "
          f"{'Enrichment':>11} {'p-value':>12} {'Recall':>8}")
    print("-" * 82)

    for row in top10_rows:
        sig = ""
        if row["p_value"] < 0.001:
            sig = "***"
        elif row["p_value"] < 0.01:
            sig = "**"
        elif row["p_value"] < 0.05:
            sig = "*"

        print(f"{row['pathogen']:<14} {row['method']:<14} {row['n_detected']:>9} "
              f"{row['n_overlap']:>4}/{row['n_escape']:<6} "
              f"{row['enrichment']:>10.3f}x {row['p_value']:>11.6f}{sig} "
              f"{row['recall']:>7.4f}")

    # ---------------------------------------------------------------------------
    # Full comparison table (all thresholds)
    # ---------------------------------------------------------------------------
    print(f"\n\n{'='*100}")
    print("  Full Comparison Table (all thresholds)")
    print(f"{'='*100}")
    print(f"{'Pathogen':<14} {'Method':<14} {'Thresh':<7} {'Det':>5} "
          f"{'Esc':>5} {'Enrich':>8} {'p-value':>10} {'Recall':>8}")
    print("-" * 75)

    for row in sorted(all_rows, key=lambda x: (x["pathogen"], x["threshold"], x["method"])):
        sig = ""
        if row["p_value"] < 0.001:
            sig = "***"
        elif row["p_value"] < 0.01:
            sig = "**"
        elif row["p_value"] < 0.05:
            sig = "*"

        print(f"{row['pathogen']:<14} {row['method']:<14} {row['threshold']:<7} "
              f"{row['n_detected']:>5} "
              f"{row['n_overlap']:>3}/{row['n_escape']:<1} "
              f"{row['enrichment']:>7.3f}x {row['p_value']:>9.4f}{sig:>4} "
              f"{row['recall']:>7.4f}")

    # ---------------------------------------------------------------------------
    # Save results
    # ---------------------------------------------------------------------------
    results_df = pd.DataFrame(all_rows)
    out_path = PROJECT_ROOT / "results" / "mutbench" / "escape_validation_adapt.csv"
    results_df.to_csv(out_path, index=False)
    print(f"\nSaved results to {out_path}")

    # ---------------------------------------------------------------------------
    # Summary
    # ---------------------------------------------------------------------------
    print("\n--- Summary (top-10% threshold) ---")
    for pathogen in ESCAPE_SITES:
        pdf = results_df[(results_df["pathogen"] == pathogen) & (results_df["threshold"] == "top10")]
        eq_row = pdf[pdf["method"] == "EqualWeight"].iloc[0]
        freq_row = pdf[pdf["method"] == "FreqThresh"].iloc[0]
        best_row = pdf[pdf["method"] == "BestSingle"].iloc[0]

        print(f"  {pathogen}:")
        print(f"    FreqThresh:  {freq_row['enrichment']:.3f}x  (p={freq_row['p_value']:.4f})")
        print(f"    EqualWeight: {eq_row['enrichment']:.3f}x  (p={eq_row['p_value']:.4f})")
        print(f"    BestSingle:  {best_row['enrichment']:.3f}x  (p={best_row['p_value']:.4f})")


if __name__ == "__main__":
    main()
