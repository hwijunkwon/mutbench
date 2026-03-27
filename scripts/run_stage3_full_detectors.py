#!/usr/bin/env python3
"""
Stage 3 FULL Benchmark: 18 scoring types x 39 detector variants (14 families) x 11 pathogens.

This is the DEFINITIVE benchmark run.

Scoring types (18):
  From feature_matrix: freq, entropy, rare_freq, homoplasy, esm2_llr,
                        plddt_inv, sasa, grantham, dnds_proxy, semantic_change,
                        EVEscape_composite, EqualWeight
  From separate CSVs:   tranception, stability, stability_structural,
                        freq_with_indel, entropy_with_indel
  New:                  fubar (posterior probability of positive selection)

Detection families (14, 39 variants — Ensemble excluded):
  Wavelet(3), KDE(3), SlidingTest(2), GradPeak(2), LocalContrast(3),
  CUSUM(3), AdaptiveKnee(1), ScoreDBSCAN(2), Spectral(2), Bayes(2),
  AdaptWin(2), FreqThresh(4), SWAN(9), MutClust-Orig(1)

Pathogens: 11 (Zika excluded)

Evaluates against Layer A (adaptive) ground truth.
Total expected: 18 x 39 x 11 = 7,722 evaluations (some may be skipped if
scores are all zeros or files missing).
"""

import sys
import os
import time
import numpy as np
import pandas as pd
from pathlib import Path
from math import sqrt

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from tools.mutbench.ground_truth.multilayer_gt import get_gt_adaptive
from scripts.run_extended_benchmark import (
    WaveletDetector,
    KDEDetector,
    SlidingWindowTest,
    GradientPeakDetector,
    LocalContrastDetector,
    CUSUMDetector,
    AdaptivePercentileDetector,
    ScoreDBSCANDetector,
    SpectralFilterDetector,
    BayesianDetector,
    AdaptiveWindowDetector,
    FrequencyThresholdDetector,
    SWANDetector,
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
BASE_DIR = Path(__file__).parent.parent
FEATURE_DIR = BASE_DIR / 'results' / 'mutbench' / 'feature_analysis'
RESULTS_DIR = BASE_DIR / 'results' / 'mutbench'

# 11 pathogens (Zika excluded)
PATHOGENS = [
    'SARS-CoV-2', 'H3N2', 'Norovirus', 'HIV-1', 'Dengue', 'RSV',
    'Influenza_B', 'MERS', 'HCV', 'Rabies', 'EV-A71',
]


# ---------------------------------------------------------------------------
# Scoring construction
# ---------------------------------------------------------------------------

def normalize_01(arr):
    """Min-max normalize to [0, 1]."""
    mn, mx = np.nanmin(arr), np.nanmax(arr)
    if mx - mn == 0:
        return np.zeros_like(arr, dtype=float)
    return (arr - mn) / (mx - mn)


def load_supplementary_csv(pathogen, suffix, score_col, n_pos):
    """Load a supplementary scoring CSV and align to n_pos positions.

    Returns 1D array of length n_pos (0-filled where data is missing).
    """
    fpath = FEATURE_DIR / f'{pathogen}_{suffix}.csv'
    if not fpath.exists():
        return None

    df = pd.read_csv(fpath)
    arr = np.zeros(n_pos, dtype=float)

    if 'position' not in df.columns or score_col not in df.columns:
        return None

    for _, row in df.iterrows():
        pos = int(row['position'])
        if 0 <= pos < n_pos:
            val = row[score_col]
            if pd.notna(val):
                arr[pos] = float(val)
    return arr


def build_all_scorings(pathogen, n_pos):
    """Build all 18 scoring arrays for a pathogen.

    Returns dict: scoring_name -> 1D numpy array of length n_pos.
    """
    # Load main feature matrix
    fpath = FEATURE_DIR / f'feature_matrix_{pathogen}.csv'
    if not fpath.exists():
        return {}

    df = pd.read_csv(fpath)
    scorings = {}

    # Align feature matrix to n_pos (use position column if available)
    if 'position' in df.columns:
        # Build aligned arrays
        def aligned(col):
            arr = np.zeros(n_pos, dtype=float)
            for _, row in df.iterrows():
                pos = int(row['position'])
                if 0 <= pos < n_pos and pd.notna(row[col]):
                    arr[pos] = float(row[col])
            return arr

        freq = aligned('freq')
        entropy = aligned('entropy')
        rare_freq = aligned('rare_freq')
        homoplasy = aligned('homoplasy')
        esm2_llr = aligned('esm2_llr')
        plddt = aligned('plddt')
        sasa = aligned('sasa')
        grantham = aligned('grantham')
        dnds_proxy = aligned('dnds_proxy')
        semantic_change = aligned('semantic_change')
    else:
        # Assume rows are ordered 0..n-1
        n = min(len(df), n_pos)
        freq = np.zeros(n_pos); freq[:n] = df['freq'].values[:n]
        entropy = np.zeros(n_pos); entropy[:n] = df['entropy'].values[:n]
        rare_freq = np.zeros(n_pos); rare_freq[:n] = df['rare_freq'].values[:n]
        homoplasy = np.zeros(n_pos); homoplasy[:n] = df['homoplasy'].values[:n]
        esm2_llr = np.zeros(n_pos); esm2_llr[:n] = df['esm2_llr'].values[:n]
        plddt = np.zeros(n_pos); plddt[:n] = df['plddt'].values[:n]
        sasa = np.zeros(n_pos); sasa[:n] = df['sasa'].values[:n]
        grantham = np.zeros(n_pos); grantham[:n] = df['grantham'].values[:n]
        dnds_proxy = np.zeros(n_pos); dnds_proxy[:n] = df['dnds_proxy'].values[:n]
        semantic_change = np.zeros(n_pos); semantic_change[:n] = df['semantic_change'].values[:n]

    # --- 1-10: Direct features ---
    scorings['freq'] = freq
    scorings['entropy'] = entropy
    scorings['rare_freq'] = rare_freq
    scorings['homoplasy'] = homoplasy
    scorings['esm2_llr'] = esm2_llr

    plddt_max = np.max(plddt) if np.max(plddt) > 0 else 1.0
    scorings['plddt_inv'] = plddt_max - plddt

    scorings['sasa'] = sasa
    scorings['grantham'] = grantham
    scorings['dnds_proxy'] = dnds_proxy
    scorings['semantic_change'] = semantic_change

    # --- 11: EVEscape composite ---
    esm2_norm = normalize_01(esm2_llr)
    sasa_norm = normalize_01(sasa)
    grantham_norm = normalize_01(grantham)
    scorings['EVEscape_composite'] = esm2_norm * sasa_norm * grantham_norm

    # --- 12: EqualWeight ---
    plddt_inv = plddt_max - plddt
    features_for_eq = [
        freq, entropy, rare_freq, homoplasy, esm2_llr,
        plddt_inv, sasa, grantham, dnds_proxy, semantic_change,
    ]
    normed = np.array([normalize_01(f) for f in features_for_eq])
    scorings['EqualWeight'] = np.mean(normed, axis=0)

    # --- 13: tranception ---
    arr = load_supplementary_csv(pathogen, 'tranception', 'tranception_score', n_pos)
    if arr is not None:
        scorings['tranception'] = arr

    # --- 14-15: stability, stability_structural ---
    stab_path = FEATURE_DIR / f'{pathogen}_stability.csv'
    if stab_path.exists():
        stab_df = pd.read_csv(stab_path)
        if 'stability_score' in stab_df.columns:
            arr = np.zeros(n_pos, dtype=float)
            for _, row in stab_df.iterrows():
                pos = int(row['position'])
                if 0 <= pos < n_pos and pd.notna(row['stability_score']):
                    arr[pos] = float(row['stability_score'])
            scorings['stability'] = arr
        if 'stability_structural' in stab_df.columns:
            arr = np.zeros(n_pos, dtype=float)
            for _, row in stab_df.iterrows():
                pos = int(row['position'])
                if 0 <= pos < n_pos and pd.notna(row['stability_structural']):
                    arr[pos] = float(row['stability_structural'])
            scorings['stability_structural'] = arr

    # --- 16-17: freq_with_indel, entropy_with_indel ---
    indel_path = FEATURE_DIR / f'{pathogen}_freq_with_indel.csv'
    if indel_path.exists():
        indel_df = pd.read_csv(indel_path)
        for col_name in ['freq_with_indel', 'entropy_with_indel']:
            if col_name in indel_df.columns:
                arr = np.zeros(n_pos, dtype=float)
                for _, row in indel_df.iterrows():
                    pos = int(row['position'])
                    if 0 <= pos < n_pos and pd.notna(row[col_name]):
                        arr[pos] = float(row[col_name])
                scorings[col_name] = arr

    # --- 18: FUBAR (posterior probability of positive selection) ---
    arr = load_supplementary_csv(pathogen, 'fubar', 'fubar_score', n_pos)
    if arr is not None:
        scorings['fubar'] = arr

    return scorings


# ---------------------------------------------------------------------------
# Detectors (14 families, 39 variants — Ensemble excluded)
# ---------------------------------------------------------------------------

def get_all_detectors():
    """Return all 39 detector instances (14 families, no Ensemble)."""
    return [
        # Wavelet (3)
        WaveletDetector(threshold=1.0),
        WaveletDetector(threshold=1.5),
        WaveletDetector(threshold=2.0),
        # KDE (3)
        KDEDetector(threshold_pct=75),
        KDEDetector(threshold_pct=80),
        KDEDetector(threshold_pct=85),
        # SlidingTest (2)
        SlidingWindowTest(p_threshold=0.01),
        SlidingWindowTest(p_threshold=0.05),
        # GradPeak (2)
        GradientPeakDetector(min_prominence=0.2),
        GradientPeakDetector(min_prominence=0.5),
        # LocalContrast (3)
        LocalContrastDetector(z_thresh=1.0),
        LocalContrastDetector(z_thresh=1.5),
        LocalContrastDetector(z_thresh=2.0),
        # CUSUM (3)
        CUSUMDetector(drift=0.3, h_factor=3.0),
        CUSUMDetector(drift=0.5, h_factor=4.0),
        CUSUMDetector(drift=0.5, h_factor=5.0),
        # AdaptiveKnee (1)
        AdaptivePercentileDetector(),
        # ScoreDBSCAN (2)
        ScoreDBSCANDetector(eps_pos=8, min_pts=3),
        ScoreDBSCANDetector(eps_pos=15, min_pts=3),
        # Spectral (2)
        SpectralFilterDetector(z_thresh=1.5),
        SpectralFilterDetector(z_thresh=2.0),
        # Bayes (2)
        BayesianDetector(prior_hotspot=0.1, threshold=0.5),
        BayesianDetector(prior_hotspot=0.15, threshold=0.4),
        # AdaptWin (2)
        AdaptiveWindowDetector(seed_pct=90, expand_thresh=0.5),
        AdaptiveWindowDetector(seed_pct=85, expand_thresh=0.4),
        # FreqThresh (4)
        FrequencyThresholdDetector(percentile=80),
        FrequencyThresholdDetector(percentile=85),
        FrequencyThresholdDetector(percentile=90),
        FrequencyThresholdDetector(percentile=95),
        # SWAN (9)
        SWANDetector(window_size=10, k=1.0),
        SWANDetector(window_size=10, k=1.5),
        SWANDetector(window_size=10, k=2.0),
        SWANDetector(window_size=20, k=1.0),
        SWANDetector(window_size=20, k=1.5),
        SWANDetector(window_size=20, k=2.0),
        SWANDetector(window_size=50, k=1.0),
        SWANDetector(window_size=50, k=1.5),
        SWANDetector(window_size=50, k=2.0),
        # MutClust-Orig (1)
        MutClustOriginalDetector(gamma=10, d=3, minpts=5),
    ]


# ---------------------------------------------------------------------------
# Main benchmark
# ---------------------------------------------------------------------------

def main():
    RESULTS_DIR.mkdir(parents=True, exist_ok=True)
    detectors = get_all_detectors()

    n_detectors = len(detectors)
    families = sorted(set(d.family for d in detectors))
    print(f"Detectors: {n_detectors} variants across {len(families)} families")
    print(f"Families: {', '.join(families)}")
    print(f"Pathogens: {len(PATHOGENS)}")
    print(f"Target scorings: 18")
    print()

    all_results = []
    t_start = time.time()

    for pathogen in PATHOGENS:
        t_p = time.time()

        # Determine n_pos from feature matrix
        fpath = FEATURE_DIR / f'feature_matrix_{pathogen}.csv'
        if not fpath.exists():
            print(f"[SKIP] {pathogen}: feature matrix not found")
            continue

        fm_df = pd.read_csv(fpath)
        n_pos = len(fm_df)

        # Ground truth: Layer A
        gt_set = get_gt_adaptive(pathogen, n_pos)
        if not gt_set:
            print(f"[SKIP] {pathogen}: no Layer A ground truth")
            continue

        # Build all scorings
        scorings = build_all_scorings(pathogen, n_pos)

        n_scoring = len(scorings)
        n_eval = 0

        print(f"{pathogen}: {n_pos} pos, {len(gt_set)} GT sites, "
              f"{n_scoring} scorings available")

        for scoring_name, scores in scorings.items():
            if np.all(scores == 0) or np.all(np.isnan(scores)):
                continue

            # Replace NaN with 0
            scores = np.nan_to_num(scores, nan=0.0)

            for det in detectors:
                try:
                    detected_raw, _ = det.detect(scores)
                    detected = postprocess(detected_raw, n_pos)
                except Exception:
                    detected = []

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
                    'family': det.family,
                    'mcc': round(mcc, 6),
                    'precision': round(prec, 6),
                    'recall': round(rec, 6),
                    'f1': round(f1, 6),
                    'n_detected': len(detected),
                })
                n_eval += 1

        elapsed = time.time() - t_p
        print(f"  -> {n_eval} evaluations in {elapsed:.1f}s")

    # Save results
    df_results = pd.DataFrame(all_results)
    out_path = RESULTS_DIR / 'stage3_full_results.csv'
    df_results.to_csv(out_path, index=False)

    total_time = time.time() - t_start

    print(f"\n{'='*70}")
    print(f"STAGE 3 FULL BENCHMARK COMPLETE")
    print(f"{'='*70}")
    print(f"Total evaluations: {len(df_results)}")
    print(f"Total time: {total_time:.1f}s")
    print(f"Output: {out_path}")

    if len(df_results) == 0:
        return

    # --- Summary statistics ---

    # Unique counts
    print(f"\nUnique pathogens: {df_results['pathogen'].nunique()}")
    print(f"Unique scorings:  {df_results['scoring'].nunique()}")
    print(f"Unique detectors: {df_results['detector'].nunique()}")
    print(f"Unique families:  {df_results['family'].nunique()}")

    # Mean MCC per scoring (across all pathogens and detectors)
    print(f"\n{'='*70}")
    print("MEAN MCC PER SCORING (across all pathogens x detectors)")
    print(f"{'='*70}")
    scoring_summary = (
        df_results.groupby('scoring')['mcc']
        .agg(['mean', 'std', 'count'])
        .sort_values('mean', ascending=False)
    )
    for scoring, row in scoring_summary.iterrows():
        print(f"  {scoring:25s}  mean={row['mean']:.4f}  std={row['std']:.4f}  n={int(row['count'])}")

    # Mean MCC per detection family
    print(f"\n{'='*70}")
    print("MEAN MCC PER DETECTION FAMILY (across all pathogens x scorings)")
    print(f"{'='*70}")
    family_summary = (
        df_results.groupby('family')['mcc']
        .agg(['mean', 'std', 'count'])
        .sort_values('mean', ascending=False)
    )
    for fam, row in family_summary.iterrows():
        print(f"  {fam:20s}  mean={row['mean']:.4f}  std={row['std']:.4f}  n={int(row['count'])}")

    # Mean MCC per pathogen
    print(f"\n{'='*70}")
    print("MEAN MCC PER PATHOGEN (across all scorings x detectors)")
    print(f"{'='*70}")
    path_summary = (
        df_results.groupby('pathogen')['mcc']
        .agg(['mean', 'std', 'max', 'count'])
        .sort_values('mean', ascending=False)
    )
    for path, row in path_summary.iterrows():
        print(f"  {path:15s}  mean={row['mean']:.4f}  std={row['std']:.4f}  "
              f"max={row['max']:.4f}  n={int(row['count'])}")

    # Best combo per pathogen
    print(f"\n{'='*70}")
    print("BEST COMBO PER PATHOGEN (by MCC)")
    print(f"{'='*70}")
    for pathogen in PATHOGENS:
        pdf = df_results[df_results['pathogen'] == pathogen]
        if len(pdf) == 0:
            continue
        best_idx = pdf['mcc'].idxmax()
        best = pdf.loc[best_idx]
        print(f"  {pathogen:15s}: {best['scoring']:25s} + {best['detector']:30s}  "
              f"MCC={best['mcc']:.4f}  F1={best['f1']:.4f}  P={best['precision']:.3f}  R={best['recall']:.3f}")

    # Top 20 overall combos
    print(f"\n{'='*70}")
    print("TOP 20 OVERALL COMBOS (by mean MCC across pathogens)")
    print(f"{'='*70}")
    combo_summary = (
        df_results.groupby(['scoring', 'detector', 'family'])['mcc']
        .agg(['mean', 'std'])
        .sort_values('mean', ascending=False)
        .head(20)
    )
    for (scoring, detector, family), row in combo_summary.iterrows():
        print(f"  {scoring:25s} + {detector:30s} [{family:15s}]  "
              f"mean={row['mean']:.4f}  std={row['std']:.4f}")

    # FUBAR-specific summary
    fubar_results = df_results[df_results['scoring'] == 'fubar']
    if len(fubar_results) > 0:
        print(f"\n{'='*70}")
        print(f"FUBAR SCORING RESULTS ({len(fubar_results)} evaluations)")
        print(f"{'='*70}")
        fubar_by_family = (
            fubar_results.groupby('family')['mcc']
            .agg(['mean', 'max'])
            .sort_values('mean', ascending=False)
        )
        for fam, row in fubar_by_family.iterrows():
            print(f"  {fam:20s}  mean={row['mean']:.4f}  max={row['max']:.4f}")

        fubar_by_pathogen = (
            fubar_results.groupby('pathogen')['mcc']
            .agg(['mean', 'max'])
            .sort_values('mean', ascending=False)
        )
        print(f"\n  FUBAR per pathogen:")
        for path, row in fubar_by_pathogen.iterrows():
            print(f"    {path:15s}  mean={row['mean']:.4f}  max={row['max']:.4f}")

    # Number of unique best combos
    best_combos = set()
    for pathogen in PATHOGENS:
        pdf = df_results[df_results['pathogen'] == pathogen]
        if len(pdf) == 0:
            continue
        best_idx = pdf['mcc'].idxmax()
        best = pdf.loc[best_idx]
        best_combos.add((best['scoring'], best['family']))
    print(f"\nUnique best (scoring, family) combos across pathogens: {len(best_combos)}")


if __name__ == '__main__':
    main()
