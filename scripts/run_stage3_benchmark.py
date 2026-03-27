#!/usr/bin/env python3
"""
Stage 3 Benchmark: 13 scoring types x 4 detectors x 12 pathogens.

Uses pre-computed feature matrices (no FASTA recomputation needed).
Evaluates against Layer A (adaptive) ground truth using MCC.
"""

import sys
import os
import numpy as np
import pandas as pd
from pathlib import Path
from math import sqrt

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from tools.mutbench.ground_truth.multilayer_gt import get_gt_adaptive
from scripts.run_extended_benchmark import (
    WaveletDetector,
    AdaptivePercentileDetector,
    FrequencyThresholdDetector,
    MutClustOriginalDetector,
    compute_mcc,
    compute_f1,
    postprocess,
)

import warnings
warnings.filterwarnings('ignore')

# ---------------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------------
FEATURE_DIR = Path(__file__).parent.parent / 'results' / 'mutbench' / 'feature_analysis'
RESULTS_DIR = Path(__file__).parent.parent / 'results' / 'mutbench'

PATHOGENS = [
    'SARS-CoV-2', 'H3N2', 'Norovirus', 'HIV-1', 'Dengue', 'RSV',
    'Influenza_B', 'MERS', 'HCV', 'Zika', 'Rabies', 'EV-A71',
]

# ---------------------------------------------------------------------------
# Scoring definitions
# ---------------------------------------------------------------------------

def normalize_01(arr):
    """Min-max normalize to [0, 1]."""
    mn, mx = np.nanmin(arr), np.nanmax(arr)
    if mx - mn == 0:
        return np.zeros_like(arr)
    return (arr - mn) / (mx - mn)


def build_scorings(df):
    """Build 13 scoring arrays from a feature matrix DataFrame.

    Returns dict: scoring_name -> 1D numpy array.
    """
    scorings = {}

    freq = df['freq'].values
    entropy = df['entropy'].values
    rare_freq = df['rare_freq'].values
    homoplasy = df['homoplasy'].values
    esm2_llr = df['esm2_llr'].values
    plddt = df['plddt'].values
    sasa = df['sasa'].values
    grantham = df['grantham'].values
    dnds_proxy = df['dnds_proxy'].values
    semantic_change = df['semantic_change'].values

    # 1-3: Basic sequence features
    scorings['freq'] = freq
    scorings['entropy'] = entropy
    scorings['rare_freq'] = rare_freq

    # 4: H-score
    scorings['H-score'] = np.log2(freq * entropy * 100 + 1)

    # 5: homoplasy
    scorings['homoplasy'] = homoplasy

    # 6: ESM-2 LLR
    scorings['esm2_llr'] = esm2_llr

    # 7: pLDDT inverse (flexible = high score)
    plddt_max = np.max(plddt) if np.max(plddt) > 0 else 1.0
    scorings['plddt_inv'] = plddt_max - plddt

    # 8: SASA
    scorings['sasa'] = sasa

    # 9: Grantham
    scorings['grantham'] = grantham

    # 10: dN/dS proxy
    scorings['dnds_proxy'] = dnds_proxy

    # 11: Semantic change
    scorings['semantic_change'] = semantic_change

    # 12: EVEscape composite = esm2_llr * sasa * grantham (each normalized to [0,1])
    esm2_norm = normalize_01(esm2_llr)
    sasa_norm = normalize_01(sasa)
    grantham_norm = normalize_01(grantham)
    scorings['EVEscape_composite'] = esm2_norm * sasa_norm * grantham_norm

    # 13: EqualWeight = mean of 10 normalized features
    plddt_inv = plddt_max - plddt
    features_for_eq = [
        freq, entropy, rare_freq, homoplasy, esm2_llr,
        plddt_inv, sasa, grantham, dnds_proxy, semantic_change,
    ]
    normed = np.array([normalize_01(f) for f in features_for_eq])
    scorings['EqualWeight'] = np.mean(normed, axis=0)

    return scorings


# ---------------------------------------------------------------------------
# Detectors
# ---------------------------------------------------------------------------

def get_detectors():
    return [
        WaveletDetector(threshold=1.0),
        AdaptivePercentileDetector(),
        FrequencyThresholdDetector(percentile=80),
        MutClustOriginalDetector(gamma=10, d=3, minpts=5),
    ]


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    RESULTS_DIR.mkdir(parents=True, exist_ok=True)
    detectors = get_detectors()
    all_results = []

    for pathogen in PATHOGENS:
        fpath = FEATURE_DIR / f'feature_matrix_{pathogen}.csv'
        if not fpath.exists():
            print(f"[SKIP] {pathogen}: feature matrix not found at {fpath}")
            continue

        df = pd.read_csv(fpath)
        n_pos = len(df)

        # Ground truth: Layer A (adaptive)
        gt_set = get_gt_adaptive(pathogen, n_pos)
        if not gt_set:
            print(f"[SKIP] {pathogen}: no Layer A ground truth")
            continue

        print(f"\n{'='*60}")
        print(f"{pathogen}: {n_pos} positions, {len(gt_set)} Layer-A GT sites")

        scorings = build_scorings(df)

        for scoring_name, scores in scorings.items():
            if np.all(scores == 0):
                print(f"  {scoring_name}: all zeros, skipping")
                continue

            for det in detectors:
                try:
                    detected_raw, _ = det.detect(scores)
                    detected = postprocess(detected_raw, n_pos)
                except Exception as e:
                    print(f"  {scoring_name} + {det.name}: ERROR {e}")
                    continue

                if len(detected) == 0:
                    mcc = 0.0
                    prec, rec, f1 = 0.0, 0.0, 0.0
                else:
                    mcc = compute_mcc(detected, gt_set, n_pos)
                    prec, rec, f1 = compute_f1(detected, gt_set, n_pos)

                all_results.append({
                    'pathogen': pathogen,
                    'scoring': scoring_name,
                    'detector': det.name,
                    'mcc': round(mcc, 6),
                    'precision': round(prec, 6),
                    'recall': round(rec, 6),
                    'f1': round(f1, 6),
                    'n_detected': len(detected),
                })

    # Save results
    df_results = pd.DataFrame(all_results)
    out_path = RESULTS_DIR / 'stage3_results.csv'
    df_results.to_csv(out_path, index=False)
    print(f"\n{'='*60}")
    print(f"Saved {len(df_results)} evaluations to {out_path}")

    # Summary: mean MCC per scoring across pathogens
    if len(df_results) > 0:
        print(f"\n{'='*60}")
        print("SUMMARY: Mean MCC per scoring (across 12 pathogens)")
        print(f"{'='*60}")
        summary = (
            df_results.groupby('scoring')['mcc']
            .agg(['mean', 'std', 'count'])
            .sort_values('mean', ascending=False)
        )
        for scoring, row in summary.iterrows():
            print(f"  {scoring:25s}  mean={row['mean']:.4f}  std={row['std']:.4f}  n={int(row['count'])}")

        # Also: mean MCC per detector
        print(f"\n{'='*60}")
        print("SUMMARY: Mean MCC per detector (across all scorings)")
        print(f"{'='*60}")
        det_summary = (
            df_results.groupby('detector')['mcc']
            .agg(['mean', 'std', 'count'])
            .sort_values('mean', ascending=False)
        )
        for det, row in det_summary.iterrows():
            print(f"  {det:30s}  mean={row['mean']:.4f}  std={row['std']:.4f}  n={int(row['count'])}")

        # Best combo per pathogen
        print(f"\n{'='*60}")
        print("Best combo per pathogen (by MCC):")
        print(f"{'='*60}")
        for pathogen in df_results['pathogen'].unique():
            pdf = df_results[df_results['pathogen'] == pathogen]
            if len(pdf) == 0:
                continue
            best_idx = pdf['mcc'].idxmax()
            best = pdf.loc[best_idx]
            print(f"  {pathogen:15s}: {best['scoring']:25s} + {best['detector']:30s}  MCC={best['mcc']:.4f}  F1={best['f1']:.4f}")


if __name__ == '__main__':
    main()
