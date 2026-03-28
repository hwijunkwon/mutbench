#!/usr/bin/env python3
"""Layer C (DMS) evaluation for 6 pathogens with 20 scoring × 14 families.

Uses pre-computed DMS data to create Layer C ground truth, then evaluates
all scoring+detector combinations against both Layer A and Layer C.

DMS pathogens: SARS-CoV-2, H3N2, HIV-1, RSV, Dengue, EV-A71
"""

import sys, os
import numpy as np
import pandas as pd
from pathlib import Path

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from tools.mutbench.ground_truth.multilayer_gt import get_gt_adaptive
from scripts.run_stage3_full_detectors import (
    build_all_scorings, get_all_detectors, FEATURE_DIR,
)
from scripts.run_extended_benchmark import compute_mcc, compute_f1, postprocess

import warnings
warnings.filterwarnings('ignore')

BASE_DIR = Path(__file__).parent.parent
RESULTS_DIR = BASE_DIR / 'results' / 'mutbench'
DMS_DIR = RESULTS_DIR / 'dms_data'

# DMS pathogens and their data files
DMS_PATHOGENS = {
    'SARS-CoV-2': DMS_DIR / 'sars2_dms.csv',
    'H3N2': DMS_DIR / 'h3n2_dms.csv',
    'HIV-1': DMS_DIR / 'hiv1_dms.csv',
    'RSV': DMS_DIR / 'rsv_dms_new.csv',
    'Rabies': DMS_DIR / 'rabies_dms.csv',
    'EV-A71': DMS_DIR / 'eva71_vp1_dms.csv',
}


def get_layer_c_gt(pathogen, n_pos):
    """Get Layer C ground truth positions from DMS data.

    Returns set of 0-indexed positions, or empty set if not available.
    """
    from tools.mutbench.ground_truth.multilayer_gt import get_gt_dms

    # Built-in DMS data for SARS-CoV-2, H3N2, HIV-1, RSV
    BUILTIN_DMS = {
        'SARS-CoV-2': BASE_DIR / 'tools' / 'mutbench' / 'ground_truth' / 'bloom_ACE2_preferences.csv',
        'H3N2': None,
        'HIV-1': None,
        'RSV': None,
    }

    # Check built-in DMS loader
    builtin_path = BUILTIN_DMS.get(pathogen)
    if builtin_path and builtin_path.exists():
        from tools.mutbench.ground_truth.multilayer_gt import load_bloom_preferences
        dms_scores = load_bloom_preferences(str(builtin_path))
        gt = get_gt_dms(dms_scores, threshold_percentile=80)
        if gt:
            return gt

    # Try DMS CSV files (new pathogens + fallback)
    dms_path = DMS_PATHOGENS.get(pathogen)
    if dms_path and dms_path.exists():
        df = pd.read_csv(dms_path)
        if 'layer_c' in df.columns:
            layer_c_pos = set()
            for _, row in df.iterrows():
                if row.get('layer_c', 0) == 1:
                    pos = int(row['position']) - 1  # 0-indexed
                    if 0 <= pos < n_pos:
                        layer_c_pos.add(pos)
            return layer_c_pos
        elif 'fitness_score' in df.columns:
            # Use top 20% as Layer C
            dms_scores = {}
            for _, row in df.iterrows():
                pos = int(row['position']) - 1
                if 0 <= pos < n_pos:
                    dms_scores[pos] = abs(row['fitness_score'])
            return get_gt_dms(dms_scores, threshold_percentile=80)

    return set()


def main():
    all_results = []
    detectors = get_all_detectors()

    for pathogen in DMS_PATHOGENS:
        fm_path = FEATURE_DIR / f'feature_matrix_{pathogen}.csv'
        if not fm_path.exists():
            print(f"[SKIP] {pathogen}: no feature matrix")
            continue

        fm_df = pd.read_csv(fm_path)
        n_pos = len(fm_df)

        gt_a = get_gt_adaptive(pathogen, n_pos)
        gt_c = get_layer_c_gt(pathogen, n_pos)

        if not gt_a:
            print(f"[SKIP] {pathogen}: no Layer A GT")
            continue
        if not gt_c:
            print(f"[SKIP] {pathogen}: no Layer C GT")
            continue

        scorings = build_all_scorings(pathogen, n_pos)
        print(f"{pathogen}: {n_pos} pos, Layer A={len(gt_a)}, Layer C={len(gt_c)}, {len(scorings)} scorings")

        for scoring_name, scores in scorings.items():
            if np.all(scores == 0) or np.all(np.isnan(scores)):
                continue
            scores = np.nan_to_num(scores, nan=0.0)

            for det in detectors:
                try:
                    detected_raw, _ = det.detect(scores)
                    detected = postprocess(detected_raw, n_pos)
                except Exception:
                    detected = []

                if len(detected) == 0:
                    mcc_a, mcc_c = 0.0, 0.0
                    f1_a, f1_c = 0.0, 0.0
                else:
                    mcc_a = compute_mcc(detected, gt_a, n_pos)
                    mcc_c = compute_mcc(detected, gt_c, n_pos)
                    _, _, f1_a = compute_f1(detected, gt_a, n_pos)
                    _, _, f1_c = compute_f1(detected, gt_c, n_pos)

                all_results.append({
                    'pathogen': pathogen,
                    'scoring': scoring_name,
                    'detector': det.name,
                    'family': det.family,
                    'mcc_layer_a': round(mcc_a, 6),
                    'mcc_layer_c': round(mcc_c, 6),
                    'f1_layer_a': round(f1_a, 6),
                    'f1_layer_c': round(f1_c, 6),
                    'n_detected': len(detected),
                    'n_gt_a': len(gt_a),
                    'n_gt_c': len(gt_c),
                })

    df = pd.DataFrame(all_results)
    out_path = RESULTS_DIR / 'layer_c_evaluation.csv'
    df.to_csv(out_path, index=False)
    print(f"\nSaved {len(df)} evaluations to {out_path}")

    if len(df) == 0:
        return

    # Summary per pathogen
    print(f"\n{'='*70}")
    print("Layer A vs Layer C: Best scoring per pathogen")
    print(f"{'='*70}")
    for pathogen in df['pathogen'].unique():
        pdf = df[df['pathogen'] == pathogen]
        best_a = pdf.loc[pdf['mcc_layer_a'].idxmax()]
        best_c = pdf.loc[pdf['mcc_layer_c'].idxmax()]
        print(f"\n  {pathogen}:")
        print(f"    Best Layer A: {best_a['scoring']:25s} + {best_a['detector']:30s} MCC={best_a['mcc_layer_a']:.4f}")
        print(f"    Best Layer C: {best_c['scoring']:25s} + {best_c['detector']:30s} MCC={best_c['mcc_layer_c']:.4f}")

    # Rank correlation between Layer A and Layer C per pathogen
    from scipy import stats as sp_stats
    print(f"\n{'='*70}")
    print("Spearman rank correlation (Layer A MCC vs Layer C MCC) per pathogen")
    print(f"{'='*70}")
    for pathogen in sorted(df['pathogen'].unique()):
        pdf = df[df['pathogen'] == pathogen]
        # Aggregate by scoring (mean across detectors)
        agg = pdf.groupby('scoring')[['mcc_layer_a', 'mcc_layer_c']].mean()
        if len(agg) >= 5:
            rho, p = sp_stats.spearmanr(agg['mcc_layer_a'], agg['mcc_layer_c'])
            print(f"  {pathogen:15s}: rho={rho:.4f}, p={p:.4f} {'*' if p < 0.05 else ''}")


if __name__ == '__main__':
    main()
