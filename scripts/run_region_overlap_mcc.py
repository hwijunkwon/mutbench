#!/usr/bin/env python3
"""
Region-overlap MCC analysis for MutBench.

For each pathogen, finds the oracle (best MCC) combination using the current
detection pipeline, then computes MCC under three evaluation modes:
  1. Position-exact: TP only if detected == GT position
  2. Window-5: TP if detected is within +/-5 of any GT position
  3. Window-10: TP if detected is within +/-10 of any GT position

This quantifies the conservativeness of position-exact evaluation by showing
that detected hotspots are spatially proximate to ground truth even when
not exactly overlapping.

Region-overlap evaluation follows the standard genomics convention:
  - TP: detected position within +/-w of any GT position
  - FP: detected position NOT within +/-w of any GT position
  - FN: GT position NOT within +/-w of any detected position
  - TN: remaining positions
"""

import sys
import os
import numpy as np
import pandas as pd
from pathlib import Path
from math import sqrt
import warnings
warnings.filterwarnings('ignore')

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from scripts.run_extended_benchmark import (
    load_fasta, compute_features, compute_scores, postprocess,
    compute_mcc as compute_mcc_sets,
    WaveletDetector, KDEDetector, SlidingWindowTest,
    GradientPeakDetector, LocalContrastDetector, CUSUMDetector,
    AdaptivePercentileDetector, ScoreDBSCANDetector, SpectralFilterDetector,
    BayesianDetector, EnsembleVoteDetector, AdaptiveWindowDetector,
    FrequencyThresholdDetector, SWANDetector, MutClustOriginalDetector,
)
from tools.mutbench.ground_truth.multilayer_gt import get_gt_adaptive

DATA_DIR = Path(__file__).parent.parent / 'data'
RESULTS_DIR = Path(__file__).parent.parent / 'results' / 'mutbench'

PATHOGENS = {
    'SARS-CoV-2': DATA_DIR / 'ncbi_temporal' / 'spike_2020_H1.fasta',
    'H3N2': DATA_DIR / 'influenza' / 'h3n2_ha_sequences.fasta',
    'Norovirus': DATA_DIR / 'norovirus' / 'norovirus_vp1_sequences.fasta',
    'HIV-1': DATA_DIR / 'cross_pathogen' / 'hiv1_gp120_sequences.fasta',
    'Dengue': DATA_DIR / 'dengue' / 'dengue_e_sequences.fasta',
    'RSV': DATA_DIR / 'rsv' / 'rsv_f_sequences.fasta',
    'Influenza_B': DATA_DIR / 'influenza' / 'influenza_b_ha_sequences.fasta',
    'MERS': DATA_DIR / 'mers' / 'mers_spike_sequences.fasta',
    'HCV': DATA_DIR / 'hcv' / 'hcv_e2_sequences.fasta',
}


def get_all_detectors():
    """Return all detector instances."""
    return [
        WaveletDetector(threshold=1.0),
        WaveletDetector(threshold=1.5),
        WaveletDetector(threshold=2.0),
        KDEDetector(threshold_pct=75),
        KDEDetector(threshold_pct=80),
        KDEDetector(threshold_pct=85),
        SlidingWindowTest(p_threshold=0.01),
        SlidingWindowTest(p_threshold=0.05),
        GradientPeakDetector(min_prominence=0.2),
        GradientPeakDetector(min_prominence=0.5),
        LocalContrastDetector(z_thresh=1.0),
        LocalContrastDetector(z_thresh=1.5),
        LocalContrastDetector(z_thresh=2.0),
        CUSUMDetector(drift=0.3, h_factor=3.0),
        CUSUMDetector(drift=0.5, h_factor=4.0),
        CUSUMDetector(drift=0.5, h_factor=5.0),
        AdaptivePercentileDetector(),
        ScoreDBSCANDetector(eps_pos=8, min_pts=3),
        ScoreDBSCANDetector(eps_pos=15, min_pts=3),
        SpectralFilterDetector(z_thresh=1.5),
        SpectralFilterDetector(z_thresh=2.0),
        BayesianDetector(prior_hotspot=0.1, threshold=0.5),
        BayesianDetector(prior_hotspot=0.15, threshold=0.4),
        EnsembleVoteDetector(min_votes=2),
        EnsembleVoteDetector(min_votes=3),
        AdaptiveWindowDetector(seed_pct=90, expand_thresh=0.5),
        AdaptiveWindowDetector(seed_pct=85, expand_thresh=0.4),
        FrequencyThresholdDetector(percentile=80),
        FrequencyThresholdDetector(percentile=85),
        FrequencyThresholdDetector(percentile=90),
        FrequencyThresholdDetector(percentile=95),
        SWANDetector(window_size=10, k=1.0),
        SWANDetector(window_size=10, k=1.5),
        SWANDetector(window_size=10, k=2.0),
        SWANDetector(window_size=20, k=1.0),
        SWANDetector(window_size=20, k=1.5),
        SWANDetector(window_size=20, k=2.0),
        SWANDetector(window_size=50, k=1.0),
        SWANDetector(window_size=50, k=1.5),
        SWANDetector(window_size=50, k=2.0),
        MutClustOriginalDetector(gamma=10, d=3, minpts=5),
    ]


def compute_mcc(tp, fp, fn, tn):
    """Compute MCC from confusion matrix values."""
    denom = sqrt((tp + fp) * (tp + fn) * (tn + fp) * (tn + fn))
    if denom == 0:
        return 0.0
    return (tp * tn - fp * fn) / denom


def compute_region_overlap_metrics(detected_set, gt_set, seq_length, window):
    """Compute MCC with region-overlap evaluation.

    A detected position d is TP if min(|d - g| for g in GT) <= window.
    A GT position g is recalled if min(|g - d| for d in detected) <= window.
    """
    if window == 0:
        tp = len(detected_set & gt_set)
        fp = len(detected_set - gt_set)
        fn = len(gt_set - detected_set)
        tn = seq_length - tp - fp - fn
        return compute_mcc(tp, fp, fn, tn), tp, fp, fn, tn

    # Expand GT by +/-window for precision evaluation
    expanded_gt = set()
    for g in gt_set:
        for offset in range(-window, window + 1):
            p = g + offset
            if 0 <= p < seq_length:
                expanded_gt.add(p)

    # TP: detected positions that fall within expanded GT
    tp = len(detected_set & expanded_gt)
    fp = len(detected_set) - tp

    # Expand detected by +/-window for recall evaluation
    expanded_det = set()
    for d in detected_set:
        for offset in range(-window, window + 1):
            p = d + offset
            if 0 <= p < seq_length:
                expanded_det.add(p)

    # FN: GT positions not covered by expanded detected
    fn = len(gt_set - expanded_det)
    tn = seq_length - tp - fp - fn

    return compute_mcc(tp, fp, fn, tn), tp, fp, fn, tn


def main():
    RESULTS_DIR.mkdir(parents=True, exist_ok=True)

    score_names = [
        'E*rare', 'P*E*rare', 'minority_E', 'P*minority_E',
        'P*E', 'H-score', 'E_only', 'P*E^2', 'rank(P*E)',
    ]
    detectors = get_all_detectors()

    results = []

    for pathogen, fasta_path in PATHOGENS.items():
        if not fasta_path.exists():
            print(f"[SKIP] {pathogen}: FASTA not found")
            continue

        print(f"\nProcessing {pathogen}...")
        sequences = load_fasta(str(fasta_path))
        min_len = min(len(s) for s in sequences)
        sequences = [s[:min_len] for s in sequences]

        features = compute_features(sequences)
        all_scores = compute_scores(features)
        gt_set = get_gt_adaptive(pathogen, min_len)

        # Find oracle: best exact MCC across all score x detector combos
        best_mcc = -1.0
        best_detected = None
        best_score = None
        best_det_name = None

        for score_name in score_names:
            scores = all_scores[score_name]
            if np.all(scores == 0):
                continue
            for det in detectors:
                try:
                    detected_raw, _ = det.detect(scores)
                    detected = postprocess(detected_raw, min_len)
                    detected_set = set(detected)
                except Exception:
                    continue
                if len(detected) == 0:
                    continue

                mcc = compute_mcc_sets(detected, gt_set, min_len)
                if mcc > best_mcc:
                    best_mcc = mcc
                    best_detected = detected_set
                    best_score = score_name
                    best_det_name = det.name

        if best_detected is None:
            print(f"  [ERROR] No valid detection for {pathogen}")
            continue

        print(f"  Oracle: {best_score} + {best_det_name}, "
              f"MCC={best_mcc:.4f}, n_detected={len(best_detected)}")

        row = {
            'pathogen': pathogen,
            'score': best_score,
            'detector': best_det_name,
            'n_detected': len(best_detected),
            'gt_size': len(gt_set),
            'seq_length': min_len,
        }

        for window, label in [(0, 'exact'), (5, 'window_5'), (10, 'window_10')]:
            mcc_w, tp, fp, fn, tn = compute_region_overlap_metrics(
                best_detected, gt_set, min_len, window
            )
            row[f'mcc_{label}'] = round(mcc_w, 4)
            row[f'tp_{label}'] = tp
            row[f'fp_{label}'] = fp
            row[f'fn_{label}'] = fn
            row[f'tn_{label}'] = tn

            print(f"  {label}: MCC={mcc_w:.4f} (TP={tp}, FP={fp}, FN={fn})")

        results.append(row)

    result_df = pd.DataFrame(results)

    print(f"\n{'='*60}")
    print("Mean oracle MCC across 9 pathogens:")
    for col in ['mcc_exact', 'mcc_window_5', 'mcc_window_10']:
        mean_val = result_df[col].mean()
        print(f"  {col}: {mean_val:.3f}")

    # Improvement ratios
    exact_mean = result_df['mcc_exact'].mean()
    w5_mean = result_df['mcc_window_5'].mean()
    w10_mean = result_df['mcc_window_10'].mean()
    print(f"\n  Improvement exact->window_5: +{(w5_mean - exact_mean):.3f} ({(w5_mean/exact_mean - 1)*100:.1f}%)")
    print(f"  Improvement exact->window_10: +{(w10_mean - exact_mean):.3f} ({(w10_mean/exact_mean - 1)*100:.1f}%)")

    outpath = RESULTS_DIR / 'region_overlap_mcc.csv'
    result_df.to_csv(outpath, index=False)
    print(f"\nSaved to {outpath}")


if __name__ == '__main__':
    main()
