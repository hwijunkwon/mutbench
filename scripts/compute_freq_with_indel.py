#!/usr/bin/env python3
"""
Compute freq_with_indel and entropy_with_indel scoring for all 12 pathogens.

Unlike the standard freq/entropy which exclude gap characters ('-', '.', 'N', 'X'),
these versions INCLUDE '-' (gaps/indels) as a valid allele state.
Only 'X' is excluded.

Then runs 4 detectors and evaluates against Layer A ground truth,
appending results to stage3_results.csv as scoring="freq_with_indel"
and scoring="entropy_with_indel".
"""

import sys
import os
import numpy as np
import pandas as pd
from pathlib import Path
from collections import Counter
from math import log2, sqrt

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
    load_fasta,
)

import warnings
warnings.filterwarnings('ignore')

# ---------------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------------
BASE = Path(__file__).parent.parent
FEATURE_DIR = BASE / 'results' / 'mutbench' / 'feature_analysis'
RESULTS_DIR = BASE / 'results' / 'mutbench'

PATHOGEN_FASTA = {
    'SARS-CoV-2': 'data/ncbi_temporal/spike_500_subsample.fasta',
    'H3N2': 'data/influenza/h3n2_ha_sequences.fasta',
    'Norovirus': 'data/norovirus/norovirus_vp1_sequences.fasta',
    'HIV-1': 'data/hiv/hiv1_gp120_sequences.fasta',
    'Dengue': 'data/dengue/dengue_e_sequences.fasta',
    'RSV': 'data/rsv/rsv_f_sequences.fasta',
    'Influenza_B': 'data/influenza/influenza_b_ha_sequences.fasta',
    'MERS': 'data/mers/mers_spike_sequences.fasta',
    'HCV': 'data/hcv/hcv_e2_sequences.fasta',
    'Zika': 'data/zika/zika_e_sequences.fasta',
    'Rabies': 'data/rabies/rabies_g_sequences.fasta',
    'EV-A71': 'data/enterovirus/eva71_vp1_sequences.fasta',
}

PATHOGENS = list(PATHOGEN_FASTA.keys())


def compute_features_with_indel(sequences):
    """Compute per-position freq and entropy INCLUDING gaps as a variant state.

    '-' is kept as a valid allele. Only 'X' is excluded.
    '.' and 'N' are also excluded (ambiguous), but '-' (indel) is kept.
    """
    n_seqs = len(sequences)
    seq_len = min(len(s) for s in sequences)

    freq_arr = np.zeros(seq_len)
    entropy_arr = np.zeros(seq_len)

    for pos in range(seq_len):
        col = [s[pos] for s in sequences if pos < len(s)]
        # Include '-' as a valid state; exclude only 'X'
        counts = Counter(c for c in col if c != 'X')

        if not counts:
            continue

        total = sum(counts.values())
        if total == 0:
            continue

        # Most common character (could be '-' if mostly gaps)
        consensus_char = counts.most_common(1)[0][0]
        consensus_count = counts[consensus_char]

        # freq_with_indel: 1 - (most common frequency)
        freq_arr[pos] = 1.0 - consensus_count / total

        # entropy_with_indel: Shannon entropy over all states including '-'
        entropy = 0.0
        for char, count in counts.items():
            f = count / total
            if f > 0:
                entropy -= f * log2(f)
        entropy_arr[pos] = entropy

    return freq_arr, entropy_arr


def get_detectors():
    return [
        WaveletDetector(threshold=1.0),
        AdaptivePercentileDetector(),
        FrequencyThresholdDetector(percentile=80),
        MutClustOriginalDetector(gamma=10, d=3, minpts=5),
    ]


def main():
    FEATURE_DIR.mkdir(parents=True, exist_ok=True)
    RESULTS_DIR.mkdir(parents=True, exist_ok=True)

    detectors = get_detectors()
    all_results = []
    feature_data = {}  # pathogen -> (freq, entropy, n_pos)

    # Step 1: Compute features for all pathogens
    print("=" * 60)
    print("STEP 1: Computing freq_with_indel and entropy_with_indel")
    print("=" * 60)

    for pathogen in PATHOGENS:
        fasta_rel = PATHOGEN_FASTA[pathogen]
        fasta_path = BASE / fasta_rel
        if not fasta_path.exists():
            print(f"[SKIP] {pathogen}: FASTA not found at {fasta_path}")
            continue

        print(f"\n  Loading {pathogen} from {fasta_rel}...")
        sequences = load_fasta(str(fasta_path))
        print(f"    {len(sequences)} sequences loaded")

        freq_arr, entropy_arr = compute_features_with_indel(sequences)
        n_pos = len(freq_arr)
        print(f"    {n_pos} positions")
        print(f"    freq_with_indel:    mean={freq_arr.mean():.4f}, max={freq_arr.max():.4f}, nonzero={np.count_nonzero(freq_arr)}")
        print(f"    entropy_with_indel: mean={entropy_arr.mean():.4f}, max={entropy_arr.max():.4f}, nonzero={np.count_nonzero(entropy_arr)}")

        # Count how many positions have gap as most common
        seq_len = n_pos
        gap_dominant = 0
        for pos in range(seq_len):
            col = [s[pos] for s in sequences if pos < len(s)]
            counts = Counter(c for c in col if c != 'X')
            if counts and counts.most_common(1)[0][0] == '-':
                gap_dominant += 1
        print(f"    gap-dominant positions: {gap_dominant}")

        # Save feature CSV
        out_df = pd.DataFrame({
            'position': np.arange(n_pos),
            'freq_with_indel': freq_arr,
            'entropy_with_indel': entropy_arr,
        })
        out_path = FEATURE_DIR / f'{pathogen}_freq_with_indel.csv'
        out_df.to_csv(out_path, index=False)
        print(f"    Saved to {out_path}")

        feature_data[pathogen] = (freq_arr, entropy_arr, n_pos)

    # Step 2: Run detectors and evaluate
    print(f"\n{'=' * 60}")
    print("STEP 2: Running 4 detectors x 2 scorings x 12 pathogens")
    print("=" * 60)

    for pathogen in PATHOGENS:
        if pathogen not in feature_data:
            continue

        freq_arr, entropy_arr, n_pos = feature_data[pathogen]

        # Ground truth
        gt_set = get_gt_adaptive(pathogen, n_pos)
        if not gt_set:
            print(f"[SKIP] {pathogen}: no Layer A ground truth")
            continue

        print(f"\n  {pathogen}: {n_pos} positions, {len(gt_set)} Layer-A GT sites")

        scorings = {
            'freq_with_indel': freq_arr,
            'entropy_with_indel': entropy_arr,
        }

        for scoring_name, scores in scorings.items():
            if np.all(scores == 0):
                print(f"    {scoring_name}: all zeros, skipping")
                continue

            for det in detectors:
                try:
                    detected_raw, _ = det.detect(scores)
                    detected = postprocess(detected_raw, n_pos)
                except Exception as e:
                    print(f"    {scoring_name} + {det.name}: ERROR {e}")
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

    # Step 3: Update stage3_results.csv
    print(f"\n{'=' * 60}")
    print("STEP 3: Updating stage3_results.csv")
    print("=" * 60)

    stage3_path = RESULTS_DIR / 'stage3_results.csv'
    if stage3_path.exists():
        existing = pd.read_csv(stage3_path)
        n_before = len(existing)

        # Remove old indel_freq rows
        n_indel_freq = len(existing[existing['scoring'] == 'indel_freq'])
        existing = existing[existing['scoring'] != 'indel_freq']
        print(f"  Removed {n_indel_freq} 'indel_freq' rows")

        # Remove any old freq_with_indel / entropy_with_indel rows (idempotent)
        n_old_fwi = len(existing[existing['scoring'].isin(['freq_with_indel', 'entropy_with_indel'])])
        existing = existing[~existing['scoring'].isin(['freq_with_indel', 'entropy_with_indel'])]
        if n_old_fwi > 0:
            print(f"  Removed {n_old_fwi} old freq_with_indel/entropy_with_indel rows")

        # Append new results
        new_df = pd.DataFrame(all_results)
        combined = pd.concat([existing, new_df], ignore_index=True)
        combined.to_csv(stage3_path, index=False)
        print(f"  Was {n_before} rows -> now {len(combined)} rows")
        print(f"  Added {len(new_df)} new rows (freq_with_indel + entropy_with_indel)")
    else:
        new_df = pd.DataFrame(all_results)
        new_df.to_csv(stage3_path, index=False)
        print(f"  Created with {len(new_df)} rows")

    # Step 4: Comparison
    print(f"\n{'=' * 60}")
    print("STEP 4: Comparison — freq vs freq_with_indel, entropy vs entropy_with_indel")
    print("=" * 60)

    # Load final stage3 results
    df = pd.read_csv(stage3_path)

    for base_scoring, indel_scoring in [('freq', 'freq_with_indel'), ('entropy', 'entropy_with_indel')]:
        print(f"\n  --- {base_scoring} vs {indel_scoring} ---")

        df_base = df[df['scoring'] == base_scoring][['pathogen', 'detector', 'mcc']].rename(columns={'mcc': 'mcc_base'})
        df_indel = df[df['scoring'] == indel_scoring][['pathogen', 'detector', 'mcc']].rename(columns={'mcc': 'mcc_indel'})

        if df_base.empty:
            print(f"    No '{base_scoring}' rows found in stage3_results.csv")
            continue
        if df_indel.empty:
            print(f"    No '{indel_scoring}' rows found in stage3_results.csv")
            continue

        merged = pd.merge(df_base, df_indel, on=['pathogen', 'detector'], how='inner')
        merged['delta'] = merged['mcc_indel'] - merged['mcc_base']

        print(f"    {'Pathogen':15s} {'Detector':30s} {'MCC_base':>10s} {'MCC_indel':>10s} {'Delta':>10s}")
        print(f"    {'-'*15} {'-'*30} {'-'*10} {'-'*10} {'-'*10}")
        for _, row in merged.iterrows():
            sign = '+' if row['delta'] >= 0 else ''
            print(f"    {row['pathogen']:15s} {row['detector']:30s} {row['mcc_base']:10.4f} {row['mcc_indel']:10.4f} {sign}{row['delta']:9.4f}")

        mean_delta = merged['delta'].mean()
        print(f"\n    Mean delta MCC ({indel_scoring} - {base_scoring}): {mean_delta:+.4f}")

        # Summary by pathogen
        pathogen_summary = merged.groupby('pathogen')['delta'].mean().sort_values(ascending=False)
        print(f"\n    Per-pathogen mean delta:")
        for p, d in pathogen_summary.items():
            print(f"      {p:15s}: {d:+.4f}")


if __name__ == '__main__':
    main()
