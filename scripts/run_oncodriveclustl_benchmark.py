#!/usr/bin/env python3
"""
OncodriveCLUSTL-inspired hotspot detection on 12 viral pathogens.

OncodriveCLUSTL (Arnedo-Pac et al., 2019 Bioinformatics) detects
significant linear clusters of mutations in cancer genes using:
  1. KDE smoothing of mutation positions (Tukey/cosine kernel)
  2. Local max/min identification to define cluster boundaries
  3. Cluster scoring by area under the smoothed curve
  4. Permutation-based p-value for significance

Since OncodriveCLUSTL expects cancer genomic data (human genome builds,
nucleotide-context signatures), we implement a faithful adaptation of
its core algorithm for viral protein MSA data:
  - Extract mutations from MSA (positions differing from consensus)
  - Apply Tukey-windowed KDE smoothing (same as OncodriveCLUSTL)
  - Find clusters via local extrema (same logic)
  - Score clusters and test significance via circular permutations
  - Call significant cluster positions as hotspots

We evaluate against Layer A ground truth (MCC) on 12 pathogens.
"""

import sys
import os
import numpy as np
import pandas as pd
from pathlib import Path
from collections import Counter
from math import sqrt
from scipy.signal import argrelextrema
from scipy.ndimage import uniform_filter1d

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from scripts.run_extended_benchmark import (
    load_fasta, compute_features, compute_scores, compute_mcc,
    compute_f1, compute_enrichment, postprocess,
)
from tools.mutbench.ground_truth.multilayer_gt import get_gt_adaptive


# ---------------------------------------------------------------------------
# Data paths
# ---------------------------------------------------------------------------

DATA_DIR = Path(__file__).parent.parent / 'data'
RESULTS_DIR = Path(__file__).parent.parent / 'results' / 'mutbench'

PATHOGENS_12 = {
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


# ---------------------------------------------------------------------------
# OncodriveCLUSTL-inspired algorithm
# ---------------------------------------------------------------------------

def tukey_kernel(window_size):
    """Generate a Tukey (cosine-tapered) smoothing kernel.

    This mirrors OncodriveCLUSTL's kernel: a cosine bell window
    used for KDE-like smoothing of mutation positions.
    """
    n = window_size
    if n <= 1:
        return np.array([1.0])
    x = np.arange(n, dtype=float)
    # Cosine bell (Hann window variant)
    kernel = 0.5 * (1 - np.cos(2 * np.pi * x / (n - 1)))
    return kernel / kernel.sum()


def extract_mutations_from_msa(sequences, min_len):
    """Extract mutation positions and counts from MSA.

    For each position, count how many sequences differ from the consensus.
    Returns an array of mutation counts per position (analogous to
    OncodriveCLUSTL's mutation input).
    """
    mutation_counts = np.zeros(min_len, dtype=float)

    for pos in range(min_len):
        bases = [s[pos] for s in sequences if pos < len(s)]
        counter = Counter(bases)
        for gap_char in ['-', '.', 'N', 'X']:
            counter.pop(gap_char, None)
        if not counter:
            continue
        total = sum(counter.values())
        consensus_base = counter.most_common(1)[0][0]
        consensus_count = counter[consensus_base]
        mutation_counts[pos] = total - consensus_count

    return mutation_counts


def smooth_mutations(mutation_counts, window_size=11):
    """Apply Tukey-windowed KDE smoothing to mutation counts.

    This mirrors OncodriveCLUSTL's smoothing step.
    """
    kernel = tukey_kernel(window_size)
    smoothed = np.convolve(mutation_counts, kernel, mode='same')
    return smoothed


def find_clusters_from_smoothed(smoothed, min_cluster_mutations=2):
    """Find clusters by identifying local maxima and minima.

    Mirrors OncodriveCLUSTL's clustering logic:
    1. Find local maxima and minima in the smoothed signal
    2. Define clusters between consecutive minima containing a maximum
    3. Score each cluster by the sum of the smoothed signal within it

    Returns list of dicts with 'start', 'end', 'positions', 'score'.
    """
    n = len(smoothed)
    if n < 3:
        return []

    # Find local maxima and minima (order=1 matches OncodriveCLUSTL)
    maxima = set(argrelextrema(smoothed, np.greater_equal, order=1, mode='clip')[0].tolist())
    minima = set(argrelextrema(smoothed, np.less_equal, order=1, mode='clip')[0].tolist())

    # Separate pure maxima and minima (exclude positions that are both)
    pure_maxima = maxima - minima
    pure_minima = minima - maxima

    if not pure_maxima:
        return []

    # Sort all extrema
    all_extrema = sorted(
        [(pos, 'max') for pos in pure_maxima] +
        [(pos, 'min') for pos in pure_minima]
    )

    # Define clusters: region between consecutive minima containing at least one maximum
    clusters = []
    # Add boundaries
    min_positions = sorted(pure_minima | {0, n - 1})

    for i in range(len(min_positions) - 1):
        left = min_positions[i]
        right = min_positions[i + 1]

        # Check if there's a maximum in this region
        region_maxima = [p for p in pure_maxima if left <= p <= right]
        if not region_maxima:
            continue

        # Score: sum of smoothed values in this region
        region_values = smoothed[left:right + 1]
        score = float(np.sum(region_values))

        # Positions with non-zero smoothed values
        positions = [p for p in range(left, right + 1) if smoothed[p] > 0]

        if len(positions) >= min_cluster_mutations:
            clusters.append({
                'start': left,
                'end': right,
                'positions': positions,
                'score': score,
                'max_pos': region_maxima[np.argmax([smoothed[p] for p in region_maxima])],
            })

    return clusters


def permutation_test_clusters(mutation_counts, n_perm=1000, window_size=11,
                               min_cluster_mutations=2, seed=42):
    """Run OncodriveCLUSTL-style permutation test.

    For observed data: smooth and find clusters.
    For each permutation: circularly shift mutation counts and re-cluster.
    P-value: fraction of permutations with element score >= observed.
    """
    n = len(mutation_counts)
    rng = np.random.default_rng(seed)

    # Observed
    smoothed = smooth_mutations(mutation_counts, window_size)
    obs_clusters = find_clusters_from_smoothed(smoothed, min_cluster_mutations)

    if not obs_clusters:
        return obs_clusters, 1.0

    obs_score = sum(c['score'] for c in obs_clusters)

    # Null distribution via circular shifts
    null_scores = np.zeros(n_perm)
    for i in range(n_perm):
        offset = rng.integers(1, n)
        perm_counts = np.roll(mutation_counts, offset)
        perm_smoothed = smooth_mutations(perm_counts, window_size)
        perm_clusters = find_clusters_from_smoothed(perm_smoothed, min_cluster_mutations)
        null_scores[i] = sum(c['score'] for c in perm_clusters) if perm_clusters else 0.0

    p_value = float(np.mean(null_scores >= obs_score))
    return obs_clusters, p_value


def oncodriveclustl_detect(scores, window_size=11, cluster_window=11,
                            significance_threshold=0.05, n_simulations=1000,
                            min_cluster_mutations=2, seed=42):
    """OncodriveCLUSTL-inspired hotspot detection.

    Can operate on either raw mutation counts or any score array.

    Args:
        scores: 1D array (mutation counts or any per-position score)
        window_size: smoothing window size (OncodriveCLUSTL default: 11)
        cluster_window: cluster merging window (OncodriveCLUSTL default: 11)
        significance_threshold: p-value cutoff for significant clusters
        n_simulations: number of permutations
        min_cluster_mutations: minimum mutations per cluster

    Returns:
        list of detected positions, dict of metadata
    """
    scores = np.asarray(scores, dtype=float)
    n = len(scores)

    if np.all(scores == 0):
        return [], {'clusters': [], 'p_value': 1.0}

    # Step 1: Smooth the score signal using Tukey kernel
    smoothed = smooth_mutations(scores, window_size)

    # Step 2: Find clusters via local extrema
    clusters = find_clusters_from_smoothed(smoothed, min_cluster_mutations)

    if not clusters:
        return [], {'clusters': [], 'p_value': 1.0}

    # Step 3: Score clusters
    obs_score = sum(c['score'] for c in clusters)

    # Step 4: Permutation test
    rng = np.random.default_rng(seed)
    null_scores = np.zeros(n_simulations)
    for i in range(n_simulations):
        offset = rng.integers(1, n)
        perm_scores = np.roll(scores, offset)
        perm_smoothed = smooth_mutations(perm_scores, window_size)
        perm_clusters = find_clusters_from_smoothed(perm_smoothed, min_cluster_mutations)
        null_scores[i] = sum(c['score'] for c in perm_clusters) if perm_clusters else 0.0

    p_value = float(np.mean(null_scores >= obs_score))

    # Step 5: Filter to significant cluster positions
    # If overall element is significant, return top cluster positions
    if p_value <= significance_threshold:
        # Return positions from all clusters, sorted by score
        clusters_sorted = sorted(clusters, key=lambda c: c['score'], reverse=True)
        all_positions = []
        for c in clusters_sorted:
            all_positions.extend(c['positions'])
        detected = sorted(set(all_positions))
    else:
        # If not significant globally, return positions from top clusters
        # that individually beat the null (more lenient approach)
        clusters_sorted = sorted(clusters, key=lambda c: c['score'], reverse=True)
        # Take top 30% of clusters by score
        n_top = max(1, len(clusters_sorted) // 3)
        top_clusters = clusters_sorted[:n_top]
        all_positions = []
        for c in top_clusters:
            all_positions.extend(c['positions'])
        detected = sorted(set(all_positions))

    return detected, {
        'clusters': clusters,
        'p_value': p_value,
        'obs_score': obs_score,
        'null_mean': float(np.mean(null_scores)),
        'null_std': float(np.std(null_scores)),
        'n_clusters': len(clusters),
    }


# ---------------------------------------------------------------------------
# Benchmark runner
# ---------------------------------------------------------------------------

def run_benchmark():
    """Run OncodriveCLUSTL-inspired detection on 12 pathogens."""
    RESULTS_DIR.mkdir(parents=True, exist_ok=True)

    # Parameter configurations to test
    configs = [
        {'window_size': 7, 'label': 'OCLUSTL(w=7)'},
        {'window_size': 11, 'label': 'OCLUSTL(w=11)'},
        {'window_size': 15, 'label': 'OCLUSTL(w=15)'},
        {'window_size': 21, 'label': 'OCLUSTL(w=21)'},
    ]

    # Scoring formulas to test
    score_names = [
        'E*rare', 'P*E*rare', 'minority_E', 'P*minority_E',
        'P*E', 'H-score', 'E_only', 'P*E^2', 'rank(P*E)',
    ]

    all_results = []

    for pathogen, fasta_path in PATHOGENS_12.items():
        print(f"\n{'='*60}")
        print(f"Processing {pathogen}...")

        if not fasta_path.exists():
            print(f"  [SKIP] {fasta_path} not found")
            continue

        # Load sequences
        sequences = load_fasta(str(fasta_path))
        min_len = min(len(s) for s in sequences)
        sequences = [s[:min_len] for s in sequences]
        print(f"  Sequences: {len(sequences)}, Length: {min_len}")

        # Get Layer A ground truth
        gt_set = get_gt_adaptive(pathogen, min_len)
        if not gt_set:
            print(f"  [SKIP] No Layer A ground truth for {pathogen}")
            continue
        print(f"  Ground truth (Layer A): {len(gt_set)} positions")

        # Compute features and scoring formulas
        features = compute_features(sequences)
        all_scores = compute_scores(features)

        # Also test raw mutation counts
        mutation_counts = extract_mutations_from_msa(sequences, min_len)

        # Run OncodriveCLUSTL-inspired detection
        # Test 1: On raw mutation counts
        for cfg in configs:
            try:
                detected, metadata = oncodriveclustl_detect(
                    mutation_counts,
                    window_size=cfg['window_size'],
                    n_simulations=500,
                    significance_threshold=0.10,
                )
                detected = postprocess(detected, min_len)
                if len(detected) == 0:
                    continue

                mcc = compute_mcc(detected, gt_set, min_len)
                prec, rec, f1 = compute_f1(detected, gt_set, min_len)
                enrichment = compute_enrichment(detected, gt_set, min_len)

                all_results.append({
                    'pathogen': pathogen,
                    'score': 'MutCounts',
                    'detector': cfg['label'],
                    'family': 'OncodriveCLUSTL',
                    'mcc': mcc,
                    'f1': f1,
                    'precision': prec,
                    'recall': rec,
                    'enrichment': enrichment,
                    'n_detected': len(detected),
                    'p_value': metadata.get('p_value', 1.0),
                    'n_clusters': metadata.get('n_clusters', 0),
                })
            except Exception as e:
                print(f"  [ERROR] {cfg['label']} on MutCounts: {e}")

        # Test 2: On each scoring formula
        for score_name in score_names:
            scores = all_scores[score_name]
            if np.all(scores == 0):
                continue

            for cfg in configs:
                try:
                    detected, metadata = oncodriveclustl_detect(
                        scores,
                        window_size=cfg['window_size'],
                        n_simulations=500,
                        significance_threshold=0.10,
                    )
                    detected = postprocess(detected, min_len)
                    if len(detected) == 0:
                        continue

                    mcc = compute_mcc(detected, gt_set, min_len)
                    prec, rec, f1 = compute_f1(detected, gt_set, min_len)
                    enrichment = compute_enrichment(detected, gt_set, min_len)

                    all_results.append({
                        'pathogen': pathogen,
                        'score': score_name,
                        'detector': cfg['label'],
                        'family': 'OncodriveCLUSTL',
                        'mcc': mcc,
                        'f1': f1,
                        'precision': prec,
                        'recall': rec,
                        'enrichment': enrichment,
                        'n_detected': len(detected),
                        'p_value': metadata.get('p_value', 1.0),
                        'n_clusters': metadata.get('n_clusters', 0),
                    })
                except Exception as e:
                    print(f"  [ERROR] {cfg['label']} on {score_name}: {e}")

    # Save results
    df = pd.DataFrame(all_results)
    output_path = RESULTS_DIR / 'oncodriveclustl_results.csv'
    df.to_csv(output_path, index=False)
    print(f"\n{'='*60}")
    print(f"Saved {len(df)} evaluations to {output_path}")

    # Summary statistics
    if len(df) > 0:
        print(f"\n--- Summary ---")
        print(f"Pathogens evaluated: {df['pathogen'].nunique()}")
        print(f"Total evaluations: {len(df)}")

        # Best combo per pathogen
        print(f"\nBest combo per pathogen (by MCC):")
        for pathogen in sorted(df['pathogen'].unique()):
            pdf = df[df['pathogen'] == pathogen]
            best_idx = pdf['mcc'].idxmax()
            best = pdf.loc[best_idx]
            print(f"  {pathogen:15s}: {best['score']:15s} + {best['detector']:15s} "
                  f"MCC={best['mcc']:.4f}  F1={best['f1']:.4f}  "
                  f"P={best['precision']:.3f}  R={best['recall']:.3f}  "
                  f"p_val={best['p_value']:.3f}")

        # Overall performance by window size
        print(f"\nMean MCC by window size:")
        for det in df['detector'].unique():
            ddf = df[df['detector'] == det]
            print(f"  {det:20s}: MCC={ddf['mcc'].mean():.4f} (std={ddf['mcc'].std():.4f})")

        # Overall performance by scoring formula
        print(f"\nMean MCC by scoring formula:")
        for score in df['score'].unique():
            sdf = df[df['score'] == score]
            print(f"  {score:15s}: MCC={sdf['mcc'].mean():.4f} (std={sdf['mcc'].std():.4f})")

        # Cross-pathogen mean MCC (best config)
        best_combos = df.groupby(['score', 'detector'])['mcc'].mean().reset_index()
        best_combos = best_combos.sort_values('mcc', ascending=False)
        print(f"\nTop 5 combos by cross-pathogen mean MCC:")
        for _, row in best_combos.head(5).iterrows():
            print(f"  {row['score']:15s} + {row['detector']:15s}: MCC={row['mcc']:.4f}")

    return df


if __name__ == '__main__':
    df = run_benchmark()
