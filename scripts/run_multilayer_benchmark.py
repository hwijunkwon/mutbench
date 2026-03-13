#!/usr/bin/env python3
"""
9-pathogen benchmark with 3-layer ground truth framework.

Reuses the detection/scoring infrastructure from run_extended_benchmark.py
but replaces the GT with the adaptive/constrained/DMS framework.

Outputs:
  - multilayer_9pathogen_results.csv  (primary: all evaluations)
  - multilayer_summary.csv            (best combo per pathogen per GT layer)
"""

import sys
import os
import numpy as np
import pandas as pd
from pathlib import Path
import warnings
warnings.filterwarnings('ignore')

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Reuse existing infrastructure
from scripts.run_extended_benchmark import (
    load_fasta, compute_features, compute_scores,
    postprocess, compute_mcc, compute_f1, compute_enrichment,
    # Detector classes
    WaveletDetector, KDEDetector, SlidingWindowTest,
    GradientPeakDetector, LocalContrastDetector, CUSUMDetector,
    AdaptivePercentileDetector, ScoreDBSCANDetector, SpectralFilterDetector,
    BayesianDetector, EnsembleVoteDetector, AdaptiveWindowDetector,
    FrequencyThresholdDetector, SWANDetector, MutClustOriginalDetector,
)

# New GT framework
from tools.mutbench.ground_truth.multilayer_gt import (
    get_gt_adaptive, get_gt_constrained,
    get_gt_dms, load_bloom_preferences, load_sars2_fitness,
)


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

DMS_FILES = {
    'SARS-CoV-2': ('sars2', DATA_DIR / 'mutbench' / 'aamut_fitness_all.csv'),
    'HIV-1': ('bloom_prefs', DATA_DIR / 'dms' / 'hiv1_env_prefs_BG505.csv'),
    'H3N2': ('bloom_prefs', DATA_DIR / 'dms' / 'h3n2_ha_prefs_Perth2009.csv'),
    'RSV': ('bloom_prefs', DATA_DIR / 'dms' / 'rsv_f_mutation_effects.csv'),
}


def load_dms_scores(pathogen: str) -> dict[int, float]:
    """Load DMS position scores for a pathogen (if available)."""
    if pathogen not in DMS_FILES:
        return {}
    dtype, path = DMS_FILES[pathogen]
    if not path.exists():
        return {}
    try:
        if dtype == 'sars2':
            return load_sars2_fitness(str(path))
        else:
            return load_bloom_preferences(str(path))
    except Exception as e:
        print(f"  [WARN] DMS load failed for {pathogen}: {e}")
        return {}


def get_detectors():
    """Return all detectors (same as run_extended_benchmark)."""
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
        unique_count = len(set(sequences))
        print(f"  Sequences: {len(sequences)} (unique: {unique_count}), Length: {min_len}")

        # Compute features and scores
        features = compute_features(sequences)
        all_scores = compute_scores(features)

        # Load GT layers
        gt_adaptive = get_gt_adaptive(pathogen, min_len)
        gt_constrained = get_gt_constrained(pathogen, min_len)
        dms_scores = load_dms_scores(pathogen)
        gt_dms = get_gt_dms(dms_scores) if dms_scores else set()

        print(f"  GT Adaptive: {len(gt_adaptive)} pos")
        print(f"  GT Constrained: {len(gt_constrained)} pos")
        print(f"  GT DMS: {len(gt_dms)} pos")

        if not gt_adaptive:
            print(f"  [SKIP] No adaptive GT for {pathogen}")
            continue

        # Evaluate all score × detector combos
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

                # Layer A: Adaptive (primary metric)
                mcc_a = compute_mcc(detected, gt_adaptive, min_len)
                p_a, r_a, f1_a = compute_f1(detected, gt_adaptive, min_len)
                enrich_a = compute_enrichment(detected, gt_adaptive, min_len)

                # Layer B: Constrained (false positive rate)
                constrained_fpr = 0.0
                if gt_constrained:
                    constrained_fpr = len(detected_set & gt_constrained) / len(gt_constrained)

                # Layer C: DMS (if available)
                dms_f1 = np.nan
                if gt_dms:
                    _, _, dms_f1 = compute_f1(detected, gt_dms, min_len)

                # Composite: adaptive F1 penalized by constrained FPR
                composite = f1_a - 0.3 * constrained_fpr

                all_results.append({
                    'pathogen': pathogen,
                    'score': score_name,
                    'detector': det.name,
                    'family': det.family,
                    'n_sequences': len(sequences),
                    'n_unique': unique_count,
                    'seq_length': min_len,
                    'gt_adaptive_size': len(gt_adaptive),
                    'gt_constrained_size': len(gt_constrained),
                    'gt_dms_size': len(gt_dms),
                    'mcc_adaptive': round(mcc_a, 4),
                    'f1_adaptive': round(f1_a, 4),
                    'precision_adaptive': round(p_a, 4),
                    'recall_adaptive': round(r_a, 4),
                    'enrichment_adaptive': round(enrich_a, 4),
                    'constrained_fpr': round(constrained_fpr, 4),
                    'dms_f1': round(dms_f1, 4) if not np.isnan(dms_f1) else np.nan,
                    'composite_score': round(composite, 4),
                    'n_detected': len(detected),
                })

    df = pd.DataFrame(all_results)
    output_path = RESULTS_DIR / 'multilayer_9pathogen_results.csv'
    df.to_csv(output_path, index=False)
    print(f"\n{'='*60}")
    print(f"Saved {len(df)} evaluations to {output_path}")

    # Summary: best combo per pathogen
    if len(df) > 0:
        print(f"\nBest combo per pathogen (by MCC adaptive):")
        summary_rows = []
        for pathogen in df['pathogen'].unique():
            pdf = df[df['pathogen'] == pathogen]
            best_idx = pdf['mcc_adaptive'].idxmax()
            best = pdf.loc[best_idx]
            print(f"  {pathogen}: {best['score']} + {best['detector']} "
                  f"(MCC={best['mcc_adaptive']:.4f}, FPR={best['constrained_fpr']:.4f})")
            summary_rows.append({
                'pathogen': pathogen,
                'best_score': best['score'],
                'best_detector': best['detector'],
                'best_family': best['family'],
                'mcc_adaptive': best['mcc_adaptive'],
                'f1_adaptive': best['f1_adaptive'],
                'constrained_fpr': best['constrained_fpr'],
                'dms_f1': best['dms_f1'],
                'composite_score': best['composite_score'],
            })

        summary_df = pd.DataFrame(summary_rows)
        summary_path = RESULTS_DIR / 'multilayer_summary.csv'
        summary_df.to_csv(summary_path, index=False)
        print(f"\nSummary saved to {summary_path}")


if __name__ == '__main__':
    main()
