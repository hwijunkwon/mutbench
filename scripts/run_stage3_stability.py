#!/usr/bin/env python3
"""
Stage 3 Benchmark: stability and stability_structural scoring for 12 pathogens.

Loads pre-computed stability scores, runs 4 detectors, evaluates against Layer A GT (MCC).
Appends results to stage3_results.csv.
"""

import sys
import os
import numpy as np
import pandas as pd
from pathlib import Path

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

FEATURE_DIR = Path(__file__).parent.parent / 'results' / 'mutbench' / 'feature_analysis'
RESULTS_DIR = Path(__file__).parent.parent / 'results' / 'mutbench'

PATHOGENS = [
    'SARS-CoV-2', 'H3N2', 'Norovirus', 'HIV-1', 'Dengue', 'RSV',
    'Influenza_B', 'MERS', 'HCV', 'Zika', 'Rabies', 'EV-A71',
]

SCORING_COLS = {
    'stability': 'stability_score',
    'stability_structural': 'stability_structural',
}


def get_detectors():
    return [
        WaveletDetector(threshold=1.0),
        AdaptivePercentileDetector(),
        FrequencyThresholdDetector(percentile=80),
        MutClustOriginalDetector(gamma=10, d=3, minpts=5),
    ]


def main():
    detectors = get_detectors()
    all_results = []

    for pathogen in PATHOGENS:
        # Load stability CSV
        stab_path = FEATURE_DIR / f'{pathogen}_stability.csv'
        if not stab_path.exists():
            print(f"[SKIP] {pathogen}: stability file not found at {stab_path}")
            continue

        stab_df = pd.read_csv(stab_path)

        # Get feature matrix length for ground truth alignment
        feat_path = FEATURE_DIR / f'feature_matrix_{pathogen}.csv'
        if feat_path.exists():
            feat_df = pd.read_csv(feat_path)
            n_pos = len(feat_df)
        else:
            # Fallback: use stability length
            n_pos = len(stab_df)

        # Ground truth: Layer A (adaptive)
        gt_set = get_gt_adaptive(pathogen, n_pos)
        if not gt_set:
            print(f"[SKIP] {pathogen}: no Layer A ground truth")
            continue

        print(f"\n{'='*60}")
        print(f"{pathogen}: n_pos={n_pos}, stability_len={len(stab_df)}, "
              f"{len(gt_set)} Layer-A GT sites")

        for scoring_name, col_name in SCORING_COLS.items():
            if col_name not in stab_df.columns:
                print(f"  [SKIP] {scoring_name}: column '{col_name}' not found")
                continue

            scores = stab_df[col_name].values.astype(float)

            # Align with feature matrix length (truncate if needed)
            if len(scores) > n_pos:
                scores = scores[:n_pos]
            elif len(scores) < n_pos:
                # Pad with zeros
                scores = np.concatenate([scores, np.zeros(n_pos - len(scores))])

            if np.all(scores == 0) or np.all(np.isnan(scores)):
                print(f"  {scoring_name}: all zeros/NaN, skipping")
                continue

            # Replace NaN with 0
            scores = np.nan_to_num(scores, nan=0.0)

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

    if not all_results:
        print("No results generated.")
        return

    df_new = pd.DataFrame(all_results)

    # Append to existing stage3_results.csv
    out_path = RESULTS_DIR / 'stage3_results.csv'
    if out_path.exists():
        df_existing = pd.read_csv(out_path)
        # Remove any prior stability rows to avoid duplicates
        df_existing = df_existing[~df_existing['scoring'].isin(SCORING_COLS.keys())]
        df_combined = pd.concat([df_existing, df_new], ignore_index=True)
    else:
        df_combined = df_new

    df_combined.to_csv(out_path, index=False)
    print(f"\n{'='*60}")
    print(f"Appended {len(df_new)} new evaluations to {out_path}")
    print(f"Total rows now: {len(df_combined)}")

    # Summary: mean MCC for stability scorings
    print(f"\n{'='*60}")
    print("STABILITY SCORING RESULTS")
    print(f"{'='*60}")
    for scoring_name in SCORING_COLS:
        subset = df_new[df_new['scoring'] == scoring_name]
        if len(subset) == 0:
            continue
        mean_mcc = subset['mcc'].mean()
        std_mcc = subset['mcc'].std()
        print(f"\n  {scoring_name}:")
        print(f"    Mean MCC = {mean_mcc:.4f} (std = {std_mcc:.4f}, n = {len(subset)})")

        # Per detector
        for det_name in subset['detector'].unique():
            det_sub = subset[subset['detector'] == det_name]
            print(f"      {det_name:30s}  mean MCC = {det_sub['mcc'].mean():.4f}")

    # Compare with existing scorings
    print(f"\n{'='*60}")
    print("COMPARISON: Mean MCC per scoring (all scorings)")
    print(f"{'='*60}")
    summary = (
        df_combined.groupby('scoring')['mcc']
        .agg(['mean', 'std', 'count'])
        .sort_values('mean', ascending=False)
    )
    for scoring, row in summary.iterrows():
        marker = " <-- NEW" if scoring in SCORING_COLS else ""
        print(f"  {scoring:25s}  mean={row['mean']:.4f}  std={row['std']:.4f}  n={int(row['count'])}{marker}")


if __name__ == '__main__':
    main()
