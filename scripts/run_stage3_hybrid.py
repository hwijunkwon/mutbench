#!/usr/bin/env python3
"""
Stage 3 Benchmark: Replace MutClust-Orig with MutClust-Hybrid in stage3_results.csv.

MutClust-Hybrid = CCM seed detection + HDBSCAN boundary determination (v2c-full).
Runs on all 16 scoring types (excluding indel_freq) x 12 pathogens.
Evaluates against Layer A ground truth using MCC.

Steps:
  1. Load each pathogen's feature matrix and build all 16 scorings.
  2. Run MutClust-Hybrid (detect_v2c) on each scoring x pathogen.
  3. Remove MutClust-Orig rows from stage3_results.csv.
  4. Remove indel_freq rows from stage3_results.csv.
  5. Add MutClust-Hybrid rows.
  6. Print comparison: MutClust-Orig mean MCC vs MutClust-Hybrid mean MCC.
"""

import sys
import os
import numpy as np
import pandas as pd
from pathlib import Path

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from tools.mutbench.ground_truth.multilayer_gt import get_gt_adaptive
from tools.mutbench.variants.registry import detect_v2c
from scripts.run_extended_benchmark import (
    BaseDetector,
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

PATHOGENS = [
    'SARS-CoV-2', 'H3N2', 'Norovirus', 'HIV-1', 'Dengue', 'RSV',
    'Influenza_B', 'MERS', 'HCV', 'Zika', 'Rabies', 'EV-A71',
]


# ---------------------------------------------------------------------------
# MutClust-Hybrid Detector (wraps detect_v2c: CCM seed + HDBSCAN boundary)
# ---------------------------------------------------------------------------

class MutClustHybridDetector(BaseDetector):
    """MutClust Hybrid: CCM seed detection + HDBSCAN cluster boundaries.

    Uses detect_v2c from tools.mutbench.variants.registry.
    """

    def __init__(self, gamma=10, minpts=5, min_cluster_size=5, min_samples=3):
        self.gamma = gamma
        self.minpts = minpts
        self.min_cluster_size = min_cluster_size
        self.min_samples = min_samples

    @property
    def name(self):
        return "MutClust-Hybrid"

    @property
    def family(self):
        return "MutClust-Hybrid"

    def detect(self, scores):
        scores = np.asarray(scores, dtype=float)
        clusters = detect_v2c(
            scores,
            gamma=self.gamma,
            minpts=self.minpts,
            min_cluster_size=self.min_cluster_size,
            min_samples=self.min_samples,
        )
        positions = []
        for c in clusters:
            if isinstance(c, dict) and 'positions' in c:
                positions.extend(c['positions'])
            elif hasattr(c, 'positions'):
                positions.extend(c.positions)
        return sorted(set(positions)), {'n_clusters': len(clusters)}


# ---------------------------------------------------------------------------
# Scoring builder (same logic as run_stage3_benchmark.py + stability + tranception)
# ---------------------------------------------------------------------------

def normalize_01(arr):
    mn, mx = np.nanmin(arr), np.nanmax(arr)
    if mx - mn == 0:
        return np.zeros_like(arr)
    return (arr - mn) / (mx - mn)


def build_all_scorings(pathogen, n_pos):
    """Build all 16 scoring arrays for a pathogen.

    Returns dict: scoring_name -> 1D numpy array (length n_pos).
    """
    scorings = {}

    # --- Base 13 scorings from feature matrix ---
    feat_path = FEATURE_DIR / f'feature_matrix_{pathogen}.csv'
    if not feat_path.exists():
        return scorings

    df = pd.read_csv(feat_path)

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

    scorings['freq'] = freq
    scorings['entropy'] = entropy
    scorings['rare_freq'] = rare_freq
    scorings['H-score'] = np.log2(freq * entropy * 100 + 1)
    scorings['homoplasy'] = homoplasy
    scorings['esm2_llr'] = esm2_llr

    plddt_max = np.max(plddt) if np.max(plddt) > 0 else 1.0
    scorings['plddt_inv'] = plddt_max - plddt

    scorings['sasa'] = sasa
    scorings['grantham'] = grantham
    scorings['dnds_proxy'] = dnds_proxy
    scorings['semantic_change'] = semantic_change

    esm2_norm = normalize_01(esm2_llr)
    sasa_norm = normalize_01(sasa)
    grantham_norm = normalize_01(grantham)
    scorings['EVEscape_composite'] = esm2_norm * sasa_norm * grantham_norm

    plddt_inv = plddt_max - plddt
    features_for_eq = [
        freq, entropy, rare_freq, homoplasy, esm2_llr,
        plddt_inv, sasa, grantham, dnds_proxy, semantic_change,
    ]
    normed = np.array([normalize_01(f) for f in features_for_eq])
    scorings['EqualWeight'] = np.mean(normed, axis=0)

    # --- Tranception scoring ---
    tc_path = FEATURE_DIR / f'{pathogen}_tranception.csv'
    if tc_path.exists():
        df_tc = pd.read_csv(tc_path)
        tc_scores = np.zeros(n_pos)
        for _, row in df_tc.iterrows():
            pos = int(row['position'])
            if 0 <= pos < n_pos:
                tc_scores[pos] = row['tranception_score']
        scorings['tranception'] = tc_scores

    # --- Stability scorings ---
    stab_path = FEATURE_DIR / f'{pathogen}_stability.csv'
    if stab_path.exists():
        stab_df = pd.read_csv(stab_path)

        for scoring_name, col_name in [('stability', 'stability_score'),
                                        ('stability_structural', 'stability_structural')]:
            if col_name in stab_df.columns:
                scores = stab_df[col_name].values.astype(float)
                if len(scores) > n_pos:
                    scores = scores[:n_pos]
                elif len(scores) < n_pos:
                    scores = np.concatenate([scores, np.zeros(n_pos - len(scores))])
                scores = np.nan_to_num(scores, nan=0.0)
                scorings[scoring_name] = scores

    return scorings


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    RESULTS_DIR.mkdir(parents=True, exist_ok=True)
    detector = MutClustHybridDetector(gamma=10, minpts=5, min_cluster_size=5, min_samples=3)
    hybrid_results = []

    for pathogen in PATHOGENS:
        feat_path = FEATURE_DIR / f'feature_matrix_{pathogen}.csv'
        if not feat_path.exists():
            print(f"[SKIP] {pathogen}: feature matrix not found at {feat_path}")
            continue

        df_feat = pd.read_csv(feat_path)
        n_pos = len(df_feat)

        gt_set = get_gt_adaptive(pathogen, n_pos)
        if not gt_set:
            print(f"[SKIP] {pathogen}: no Layer A ground truth")
            continue

        print(f"\n{'='*60}")
        print(f"{pathogen}: {n_pos} positions, {len(gt_set)} Layer-A GT sites")

        scorings = build_all_scorings(pathogen, n_pos)

        for scoring_name, scores in scorings.items():
            if np.all(scores == 0) or np.all(np.isnan(scores)):
                print(f"  {scoring_name}: all zeros/NaN, skipping")
                continue

            try:
                detected_raw, _ = detector.detect(scores)
                detected = postprocess(detected_raw, n_pos)
            except Exception as e:
                print(f"  {scoring_name} + {detector.name}: ERROR {e}")
                continue

            if len(detected) == 0:
                mcc = 0.0
                prec, rec, f1 = 0.0, 0.0, 0.0
            else:
                mcc = compute_mcc(detected, gt_set, n_pos)
                prec, rec, f1 = compute_f1(detected, gt_set, n_pos)

            hybrid_results.append({
                'pathogen': pathogen,
                'scoring': scoring_name,
                'detector': detector.name,
                'mcc': round(mcc, 6),
                'precision': round(prec, 6),
                'recall': round(rec, 6),
                'f1': round(f1, 6),
                'n_detected': len(detected),
            })

            print(f"  {scoring_name:25s} + {detector.name}: MCC={mcc:.4f}, "
                  f"F1={f1:.4f}, n_detected={len(detected)}")

    df_hybrid = pd.DataFrame(hybrid_results)
    print(f"\n{'='*60}")
    print(f"MutClust-Hybrid evaluations: {len(df_hybrid)}")

    # --- Load existing results and compute comparison ---
    stage3_path = RESULTS_DIR / 'stage3_results.csv'
    if stage3_path.exists():
        df_existing = pd.read_csv(stage3_path)
    else:
        print("ERROR: stage3_results.csv not found!")
        return

    # Extract MutClust-Orig rows for comparison
    df_orig = df_existing[df_existing['detector'] == 'MutClust-Orig(g=10)'].copy()
    # Exclude indel_freq from orig for fair comparison
    df_orig_no_indel = df_orig[df_orig['scoring'] != 'indel_freq']

    print(f"\n{'='*60}")
    print("COMPARISON: MutClust-Orig vs MutClust-Hybrid")
    print(f"{'='*60}")

    orig_mean_mcc = df_orig_no_indel['mcc'].mean() if len(df_orig_no_indel) > 0 else 0.0
    hybrid_mean_mcc = df_hybrid['mcc'].mean() if len(df_hybrid) > 0 else 0.0

    print(f"  MutClust-Orig   mean MCC = {orig_mean_mcc:.4f}  (n={len(df_orig_no_indel)})")
    print(f"  MutClust-Hybrid mean MCC = {hybrid_mean_mcc:.4f}  (n={len(df_hybrid)})")
    print(f"  Delta = {hybrid_mean_mcc - orig_mean_mcc:+.4f}")

    # Per-pathogen comparison
    print(f"\n{'='*60}")
    print("PER-PATHOGEN COMPARISON (mean MCC across scorings)")
    print(f"{'='*60}")
    print(f"  {'Pathogen':15s}  {'Orig':>8s}  {'Hybrid':>8s}  {'Delta':>8s}")
    print(f"  {'-'*15}  {'-'*8}  {'-'*8}  {'-'*8}")

    worse_cases = []
    for pathogen in PATHOGENS:
        orig_sub = df_orig_no_indel[df_orig_no_indel['pathogen'] == pathogen]
        hybrid_sub = df_hybrid[df_hybrid['pathogen'] == pathogen]
        orig_m = orig_sub['mcc'].mean() if len(orig_sub) > 0 else 0.0
        hybrid_m = hybrid_sub['mcc'].mean() if len(hybrid_sub) > 0 else 0.0
        delta = hybrid_m - orig_m
        marker = " <-- WORSE" if delta < 0 else ""
        print(f"  {pathogen:15s}  {orig_m:8.4f}  {hybrid_m:8.4f}  {delta:+8.4f}{marker}")
        if delta < 0:
            worse_cases.append((pathogen, orig_m, hybrid_m))

    if worse_cases:
        print(f"\n  NOTE: MutClust-Hybrid performs worse for {len(worse_cases)} pathogen(s):")
        for p, o, h in worse_cases:
            print(f"    {p}: Orig={o:.4f}, Hybrid={h:.4f}")
        print("  Replacing anyway as requested.")

    # Per-scoring comparison
    print(f"\n{'='*60}")
    print("PER-SCORING COMPARISON (mean MCC across pathogens)")
    print(f"{'='*60}")
    print(f"  {'Scoring':25s}  {'Orig':>8s}  {'Hybrid':>8s}  {'Delta':>8s}")
    print(f"  {'-'*25}  {'-'*8}  {'-'*8}  {'-'*8}")

    all_scorings = sorted(df_hybrid['scoring'].unique())
    for scoring in all_scorings:
        orig_sub = df_orig_no_indel[df_orig_no_indel['scoring'] == scoring]
        hybrid_sub = df_hybrid[df_hybrid['scoring'] == scoring]
        orig_m = orig_sub['mcc'].mean() if len(orig_sub) > 0 else float('nan')
        hybrid_m = hybrid_sub['mcc'].mean() if len(hybrid_sub) > 0 else float('nan')
        delta = hybrid_m - orig_m if not (np.isnan(orig_m) or np.isnan(hybrid_m)) else float('nan')
        print(f"  {scoring:25s}  {orig_m:8.4f}  {hybrid_m:8.4f}  {delta:+8.4f}")

    # --- Update stage3_results.csv ---
    # Remove MutClust-Orig rows
    df_no_orig = df_existing[df_existing['detector'] != 'MutClust-Orig(g=10)']
    # Remove indel_freq rows
    df_no_orig_no_indel = df_no_orig[df_no_orig['scoring'] != 'indel_freq']
    # Add MutClust-Hybrid rows
    df_combined = pd.concat([df_no_orig_no_indel, df_hybrid], ignore_index=True)

    df_combined.to_csv(stage3_path, index=False)
    print(f"\n{'='*60}")
    print(f"Updated {stage3_path}")
    print(f"  Removed {len(df_existing) - len(df_no_orig)} MutClust-Orig rows")
    print(f"  Removed {len(df_no_orig) - len(df_no_orig_no_indel)} indel_freq rows")
    print(f"  Added {len(df_hybrid)} MutClust-Hybrid rows")
    print(f"  Total rows: {len(df_combined)} (was {len(df_existing)})")

    # Final summary: mean MCC per detector
    print(f"\n{'='*60}")
    print("FINAL: Mean MCC per detector (updated stage3_results.csv)")
    print(f"{'='*60}")
    det_summary = (
        df_combined.groupby('detector')['mcc']
        .agg(['mean', 'std', 'count'])
        .sort_values('mean', ascending=False)
    )
    for det, row in det_summary.iterrows():
        print(f"  {det:30s}  mean={row['mean']:.4f}  std={row['std']:.4f}  n={int(row['count'])}")


if __name__ == '__main__':
    main()
