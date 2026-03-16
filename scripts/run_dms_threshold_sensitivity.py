#!/usr/bin/env python3
"""
DMS threshold sensitivity analysis for the 9-pathogen benchmark.

Tests how DMS ground truth changes at 10%, 20% (current), and 30% thresholds
for the 4 pathogens with DMS data: SARS-CoV-2, H3N2, HIV-1, RSV.

Recomputes DMS F1 for all scoring x detection combinations and reports
per-pathogen best DMS F1, overall mean, and ranking stability.

Output: results/mutbench/dms_threshold_sensitivity_analysis.csv
"""

import sys
import os
import numpy as np
import pandas as pd
from pathlib import Path
import warnings
warnings.filterwarnings('ignore')

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from scripts.run_extended_benchmark import (
    load_fasta, compute_features, compute_scores,
    postprocess, compute_f1,
    WaveletDetector, KDEDetector, SlidingWindowTest,
    GradientPeakDetector, LocalContrastDetector, CUSUMDetector,
    AdaptivePercentileDetector, ScoreDBSCANDetector, SpectralFilterDetector,
    BayesianDetector, EnsembleVoteDetector, AdaptiveWindowDetector,
    FrequencyThresholdDetector, SWANDetector, MutClustOriginalDetector,
)

from tools.mutbench.ground_truth.multilayer_gt import (
    load_bloom_preferences, load_sars2_fitness,
)

DATA_DIR = Path(__file__).parent.parent / 'data'
RESULTS_DIR = Path(__file__).parent.parent / 'results' / 'mutbench'

# Pathogens with DMS data and their FASTA files
PATHOGENS = {
    'SARS-CoV-2': DATA_DIR / 'ncbi_temporal' / 'spike_2020_H1.fasta',
    'H3N2': DATA_DIR / 'influenza' / 'h3n2_ha_sequences.fasta',
    'HIV-1': DATA_DIR / 'cross_pathogen' / 'hiv1_gp120_sequences.fasta',
    'RSV': DATA_DIR / 'rsv' / 'rsv_f_sequences.fasta',
}

DMS_FILES = {
    'SARS-CoV-2': ('sars2', DATA_DIR / 'mutbench' / 'aamut_fitness_all.csv'),
    'HIV-1': ('bloom_prefs', DATA_DIR / 'dms' / 'hiv1_env_prefs_BG505.csv'),
    'H3N2': ('bloom_prefs', DATA_DIR / 'dms' / 'h3n2_ha_prefs_Perth2009.csv'),
    'RSV': ('rsv_effects', DATA_DIR / 'dms' / 'rsv_f_mutation_effects.csv'),
}

THRESHOLDS = [10, 20, 30]  # top X percentile (percentile = 100 - X)


def load_rsv_fitness(filepath: str) -> dict:
    """Load RSV F protein mutation effects.

    The RSV DMS file has per-mutation 'cell entry' fitness effects.
    Computes mean |effect| per position (0-based sequential_site).
    """
    df = pd.read_csv(filepath)
    site_fitness = (
        df.groupby('sequential_site')['cell entry']
        .apply(lambda x: np.mean(np.abs(x)))
        .to_dict()
    )
    # Convert to 0-based
    return {int(pos) - 1: val for pos, val in site_fitness.items()}


def load_dms_scores(pathogen: str) -> dict:
    """Load DMS position scores for a pathogen."""
    if pathogen not in DMS_FILES:
        return {}
    dtype, path = DMS_FILES[pathogen]
    if not path.exists():
        print(f"  [WARN] DMS file not found: {path}")
        return {}
    try:
        if dtype == 'sars2':
            return load_sars2_fitness(str(path))
        elif dtype == 'rsv_effects':
            return load_rsv_fitness(str(path))
        else:
            return load_bloom_preferences(str(path))
    except Exception as e:
        print(f"  [WARN] DMS load failed for {pathogen}: {e}")
        return {}


def get_gt_dms(dms_scores: dict, threshold_percentile: float = 80) -> set:
    """Get DMS ground truth positions at a given percentile threshold."""
    if not dms_scores:
        return set()
    values = list(dms_scores.values())
    threshold = np.percentile(values, threshold_percentile)
    return {pos for pos, val in dms_scores.items() if val >= threshold}


def get_detectors():
    """Return all detectors (same as multilayer benchmark)."""
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


def main():
    RESULTS_DIR.mkdir(parents=True, exist_ok=True)

    score_names = [
        'E*rare', 'P*E*rare', 'minority_E', 'P*minority_E',
        'P*E', 'H-score', 'E_only', 'P*E^2', 'rank(P*E)',
    ]

    detectors = get_detectors()
    all_results = []

    for pathogen, fasta_path in PATHOGENS.items():
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

        # Compute features and scores
        features = compute_features(sequences)
        all_scores = compute_scores(features)

        # Load DMS scores
        dms_scores = load_dms_scores(pathogen)
        if not dms_scores:
            print(f"  [SKIP] No DMS data for {pathogen}")
            continue

        # For each threshold, compute GT and evaluate
        for top_pct in THRESHOLDS:
            threshold_percentile = 100 - top_pct
            gt_dms = get_gt_dms(dms_scores, threshold_percentile=threshold_percentile)

            # Filter to valid range
            gt_dms = {p for p in gt_dms if 0 <= p < min_len}

            print(f"  Top {top_pct}% threshold: {len(gt_dms)} GT positions")

            if not gt_dms:
                continue

            # Evaluate all score x detector combos
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

                    _, _, dms_f1 = compute_f1(detected, gt_dms, min_len)

                    all_results.append({
                        'threshold': top_pct,
                        'pathogen': pathogen,
                        'best_combo': f"{score_name} + {det.name}",
                        'dms_f1': round(dms_f1, 4),
                        'n_gt_positions': len(gt_dms),
                    })

    df = pd.DataFrame(all_results)

    # Save full results
    output_path = RESULTS_DIR / 'dms_threshold_sensitivity_analysis.csv'
    df.to_csv(output_path, index=False)
    print(f"\n{'='*60}")
    print(f"Saved {len(df)} evaluations to {output_path}")

    # Summary analysis
    print(f"\n{'='*60}")
    print("SUMMARY: Best DMS F1 per pathogen per threshold")
    print('='*60)

    summary_rows = []
    for threshold in THRESHOLDS:
        tdf = df[df['threshold'] == threshold]
        for pathogen in sorted(tdf['pathogen'].unique()):
            pdf = tdf[tdf['pathogen'] == pathogen]
            best_idx = pdf['dms_f1'].idxmax()
            best = pdf.loc[best_idx]
            print(f"  Top {threshold}% | {pathogen:12s} | {best['best_combo']:40s} | "
                  f"F1={best['dms_f1']:.4f} | n_gt={best['n_gt_positions']}")
            summary_rows.append({
                'threshold': threshold,
                'pathogen': pathogen,
                'best_combo': best['best_combo'],
                'dms_f1': best['dms_f1'],
                'n_gt_positions': best['n_gt_positions'],
            })

    # Overall mean best F1 per threshold
    print(f"\nOverall mean best DMS F1 per threshold:")
    for threshold in THRESHOLDS:
        sdf = pd.DataFrame([r for r in summary_rows if r['threshold'] == threshold])
        mean_f1 = sdf['dms_f1'].mean()
        print(f"  Top {threshold}%: mean best F1 = {mean_f1:.4f}")

    # Ranking stability
    print(f"\nMethod ranking stability across thresholds:")
    for pathogen in sorted(df['pathogen'].unique()):
        combos = []
        for threshold in THRESHOLDS:
            tdf = df[(df['threshold'] == threshold) & (df['pathogen'] == pathogen)]
            if len(tdf) == 0:
                continue
            best_idx = tdf['dms_f1'].idxmax()
            combos.append(tdf.loc[best_idx, 'best_combo'])
        stable = len(set(combos)) == 1
        print(f"  {pathogen}: {'STABLE' if stable else 'CHANGES'} "
              f"({' -> '.join(combos)})")


if __name__ == '__main__':
    main()
