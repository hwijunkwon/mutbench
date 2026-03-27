#!/usr/bin/env python3
"""
Stage 3 Benchmark: Add tranception and indel_freq scoring to stage3_results.csv.

For each of 12 pathogens:
  - tranception: load pre-computed scores from feature_analysis/{pathogen}_tranception.csv
  - indel_freq: compute per-position gap frequency from MSA FASTA files
Run through 4 detectors: Wavelet(t=1.0), AdaptiveKnee, FreqThresh(top-20%), MutClust-Orig
Evaluate against Layer A ground truth (MCC).
Append results to stage3_results.csv.
"""

import sys
import os
import numpy as np
import pandas as pd
from pathlib import Path
from collections import Counter

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
BASE_DIR = Path(__file__).parent.parent
FEATURE_DIR = BASE_DIR / 'results' / 'mutbench' / 'feature_analysis'
RESULTS_DIR = BASE_DIR / 'results' / 'mutbench'
DATA_DIR = BASE_DIR / 'data'

PATHOGENS = [
    'SARS-CoV-2', 'H3N2', 'Norovirus', 'HIV-1', 'Dengue', 'RSV',
    'Influenza_B', 'MERS', 'HCV', 'Zika', 'Rabies', 'EV-A71',
]

# Protein-level FASTA (unaligned) - kept for reference
FASTA_PATHS = {
    'SARS-CoV-2': DATA_DIR / 'ncbi_temporal' / 'spike_2020_H1.fasta',
    'H3N2': DATA_DIR / 'influenza' / 'h3n2_ha_sequences.fasta',
    'Norovirus': DATA_DIR / 'norovirus' / 'norovirus_vp1_sequences.fasta',
    'HIV-1': DATA_DIR / 'cross_pathogen' / 'hiv1_gp120_sequences.fasta',
    'Dengue': DATA_DIR / 'dengue' / 'dengue_e_sequences.fasta',
    'RSV': DATA_DIR / 'rsv' / 'rsv_f_sequences.fasta',
    'Influenza_B': DATA_DIR / 'influenza' / 'influenza_b_ha_sequences.fasta',
    'MERS': DATA_DIR / 'mers' / 'mers_spike_sequences.fasta',
    'HCV': DATA_DIR / 'hcv' / 'hcv_e2_sequences.fasta',
    'Zika': DATA_DIR / 'zika' / 'zika_e_sequences.fasta',
    'Rabies': DATA_DIR / 'rabies' / 'rabies_g_sequences.fasta',
    'EV-A71': DATA_DIR / 'enterovirus' / 'eva71_vp1_sequences.fasta',
}

# Nucleotide-level aligned FASTA (for indel_freq computation)
NT_ALIGNED_PATHS = {
    'SARS-CoV-2': DATA_DIR / 'ncbi_temporal' / 'sars2_spike_nt_cds_aligned.fasta',
    'H3N2': DATA_DIR / 'influenza' / 'h3n2_ha_nt_cds_aligned.fasta',
    'Norovirus': DATA_DIR / 'norovirus' / 'norovirus_vp1_nt_cds_aligned.fasta',
    'HIV-1': DATA_DIR / 'hiv' / 'hiv1_gp120_nt_cds_aligned.fasta',
    'Dengue': DATA_DIR / 'dengue' / 'dengue_e_nt_cds_aligned.fasta',
    'RSV': DATA_DIR / 'rsv' / 'rsv_f_nt_cds_aligned.fasta',
    'Influenza_B': DATA_DIR / 'influenza' / 'influenza_b_ha_nt_cds_aligned.fasta',
    'MERS': DATA_DIR / 'mers' / 'mers_spike_nt_cds_aligned.fasta',
    'HCV': DATA_DIR / 'hcv' / 'hcv_e2_nt_cds_aligned.fasta',
    'Zika': DATA_DIR / 'zika' / 'zika_e_nt_cds_aligned.fasta',
    'Rabies': DATA_DIR / 'rabies' / 'rabies_g_nt_cds_aligned.fasta',
    'EV-A71': DATA_DIR / 'enterovirus' / 'eva71_vp1_nt_cds_aligned.fasta',
}


def compute_indel_freq_nt(sequences):
    """Compute per-codon gap frequency from nucleotide-aligned sequences.

    For each codon (3 nt), a sequence is considered to have a gap at that
    protein position if any of the 3 nucleotides is a gap character.
    Returns per-protein-position gap frequency array.
    """
    n_seqs = len(sequences)
    min_len = min(len(s) for s in sequences)
    n_codons = min_len // 3
    gap_freq = np.zeros(n_codons)

    for codon_idx in range(n_codons):
        nt_start = codon_idx * 3
        gap_count = 0
        for s in sequences:
            codon = s[nt_start:nt_start + 3]
            if '-' in codon or '.' in codon:
                gap_count += 1
        gap_freq[codon_idx] = gap_count / n_seqs

    return gap_freq


def get_detectors():
    return [
        WaveletDetector(threshold=1.0),
        AdaptivePercentileDetector(),
        FrequencyThresholdDetector(percentile=80),
        MutClustOriginalDetector(gamma=10, d=3, minpts=5),
    ]


def evaluate_scoring(scoring_name, scores, gt_set, n_pos, detectors):
    """Run all detectors on a scoring and return result rows."""
    results = []
    if np.all(scores == 0):
        print(f"  {scoring_name}: all zeros, skipping")
        return results

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

        results.append({
            'pathogen': '',  # filled by caller
            'scoring': scoring_name,
            'detector': det.name,
            'mcc': round(mcc, 6),
            'precision': round(prec, 6),
            'recall': round(rec, 6),
            'f1': round(f1, 6),
            'n_detected': len(detected),
        })

    return results


def main():
    RESULTS_DIR.mkdir(parents=True, exist_ok=True)
    detectors = get_detectors()
    all_results = []

    for pathogen in PATHOGENS:
        # Determine n_pos from feature matrix
        fmat_path = FEATURE_DIR / f'feature_matrix_{pathogen}.csv'
        if not fmat_path.exists():
            print(f"[SKIP] {pathogen}: feature matrix not found")
            continue

        df_feat = pd.read_csv(fmat_path)
        n_pos = len(df_feat)

        # Ground truth: Layer A (adaptive)
        gt_set = get_gt_adaptive(pathogen, n_pos)
        if not gt_set:
            print(f"[SKIP] {pathogen}: no Layer A ground truth")
            continue

        print(f"\n{'='*60}")
        print(f"{pathogen}: {n_pos} positions, {len(gt_set)} Layer-A GT sites")

        # --- Tranception scoring ---
        tranception_path = FEATURE_DIR / f'{pathogen}_tranception.csv'
        if tranception_path.exists():
            df_tc = pd.read_csv(tranception_path)
            # Build score array aligned to positions
            tc_scores = np.zeros(n_pos)
            for _, row in df_tc.iterrows():
                pos = int(row['position'])
                if 0 <= pos < n_pos:
                    tc_scores[pos] = row['tranception_score']

            rows = evaluate_scoring('tranception', tc_scores, gt_set, n_pos, detectors)
            for r in rows:
                r['pathogen'] = pathogen
            all_results.extend(rows)
            print(f"  tranception: {len(rows)} evaluations")
        else:
            print(f"  [SKIP] tranception: file not found at {tranception_path}")

        # --- Indel freq scoring (from nucleotide-aligned FASTA) ---
        nt_path = NT_ALIGNED_PATHS.get(pathogen)
        if nt_path and nt_path.exists():
            nt_sequences = load_fasta(str(nt_path))
            indel_scores = compute_indel_freq_nt(nt_sequences)
            n_indel = len(indel_scores)
            n_nonzero = np.count_nonzero(indel_scores)
            print(f"  indel_freq: {n_indel} codon positions, {n_nonzero} non-zero gaps")

            # Trim or pad to match n_pos
            if n_indel > n_pos:
                indel_scores = indel_scores[:n_pos]
            elif n_indel < n_pos:
                indel_scores = np.pad(indel_scores, (0, n_pos - n_indel))

            rows = evaluate_scoring('indel_freq', indel_scores, gt_set, n_pos, detectors)
            for r in rows:
                r['pathogen'] = pathogen
            all_results.extend(rows)
            print(f"  indel_freq: {len(rows)} evaluations")
        else:
            print(f"  [SKIP] indel_freq: NT-aligned FASTA not found for {pathogen}")

    # Build DataFrame of new results
    df_new = pd.DataFrame(all_results)
    print(f"\n{'='*60}")
    print(f"New evaluations: {len(df_new)}")

    # Append to existing stage3_results.csv
    stage3_path = RESULTS_DIR / 'stage3_results.csv'
    if stage3_path.exists():
        df_existing = pd.read_csv(stage3_path)
        # Remove any previous tranception/indel_freq rows to avoid duplicates
        df_existing = df_existing[~df_existing['scoring'].isin(['tranception', 'indel_freq'])]
        df_combined = pd.concat([df_existing, df_new], ignore_index=True)
    else:
        df_combined = df_new

    df_combined.to_csv(stage3_path, index=False)
    print(f"Saved {len(df_combined)} total evaluations to {stage3_path}")

    # --- Summary ---
    if len(df_new) > 0:
        print(f"\n{'='*60}")
        print("NEW SCORING RESULTS: Mean MCC per scoring")
        print(f"{'='*60}")
        for scoring in ['tranception', 'indel_freq']:
            subset = df_new[df_new['scoring'] == scoring]
            if len(subset) > 0:
                mean_mcc = subset['mcc'].mean()
                std_mcc = subset['mcc'].std()
                print(f"  {scoring:25s}  mean={mean_mcc:.4f}  std={std_mcc:.4f}  n={len(subset)}")

        # Compare with existing 13 scoring results
        print(f"\n{'='*60}")
        print("COMPARISON: Mean MCC across ALL 15 scorings (sorted)")
        print(f"{'='*60}")
        summary = (
            df_combined.groupby('scoring')['mcc']
            .agg(['mean', 'std', 'count'])
            .sort_values('mean', ascending=False)
        )
        for scoring, row in summary.iterrows():
            marker = " <-- NEW" if scoring in ('tranception', 'indel_freq') else ""
            print(f"  {scoring:25s}  mean={row['mean']:.4f}  std={row['std']:.4f}  n={int(row['count'])}{marker}")


if __name__ == '__main__':
    main()
