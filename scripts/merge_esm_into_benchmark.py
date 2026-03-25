#!/usr/bin/env python3
"""
Merge ESM-LLR benchmark results into the multilayer 9-pathogen results.

The ESM-LLR scores were already computed (run_esm_scoring.py) and evaluated
through the same 39 detectors with the same multilayer GT framework.

This script:
1. Loads existing multilayer_9pathogen_results.csv (9 scoring × 39 detectors × 9 pathogens)
2. Loads esm_benchmark_results.csv (ESM-LLR × 41 detectors × 9 pathogens)
3. Filters ESM to the same 39 detectors
4. Aligns columns (adds n_sequences, n_unique from multilayer data)
5. Produces combined_10scoring_results.csv (10 scoring × 39 detectors × 9 pathogens)
6. Also re-runs ANOVA/Friedman with the 10th scoring included
"""

import sys
import os
import numpy as np
import pandas as pd
from pathlib import Path
from scipy import stats as sp_stats
import warnings
warnings.filterwarnings('ignore')

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

RESULTS_DIR = Path(__file__).parent.parent / 'results' / 'mutbench'


def main():
    # ---- Load data ----
    ml_path = RESULTS_DIR / 'multilayer_9pathogen_results.csv'
    esm_path = RESULTS_DIR / 'esm_benchmark_results.csv'

    ml = pd.read_csv(ml_path)
    esm = pd.read_csv(esm_path)

    print(f"Multilayer results: {len(ml)} rows, {ml.score.nunique()} scoring, "
          f"{ml.detector.nunique()} detectors, {ml.pathogen.nunique()} pathogens")
    print(f"ESM results: {len(esm)} rows, {esm.detector.nunique()} detectors, "
          f"{esm.pathogen.nunique()} pathogens")

    # ---- Filter ESM to same 39 detectors ----
    ml_detectors = set(ml.detector.unique())
    esm_filtered = esm[esm.detector.isin(ml_detectors)].copy()
    print(f"\nESM filtered to 39 detectors: {len(esm_filtered)} rows")

    # ---- Align columns ----
    # ESM is missing n_sequences and n_unique; fill from ML data
    seq_info = ml.groupby('pathogen')[['n_sequences', 'n_unique']].first().to_dict('index')

    esm_filtered['n_sequences'] = esm_filtered['pathogen'].map(
        lambda p: seq_info.get(p, {}).get('n_sequences', np.nan))
    esm_filtered['n_unique'] = esm_filtered['pathogen'].map(
        lambda p: seq_info.get(p, {}).get('n_unique', np.nan))

    # Ensure same column order as ML
    common_cols = list(ml.columns)
    # Check all columns exist
    missing_in_esm = [c for c in common_cols if c not in esm_filtered.columns]
    extra_in_esm = [c for c in esm_filtered.columns if c not in common_cols]
    if missing_in_esm:
        print(f"  WARNING: columns missing in ESM: {missing_in_esm}")
    if extra_in_esm:
        print(f"  Extra columns in ESM (will be dropped): {extra_in_esm}")

    esm_aligned = esm_filtered[common_cols]

    # ---- Merge ----
    combined = pd.concat([ml, esm_aligned], ignore_index=True)
    print(f"\nCombined: {len(combined)} rows")
    print(f"  Scoring methods: {sorted(combined.score.unique())}")
    print(f"  {combined.score.nunique()} scoring × "
          f"{combined.detector.nunique()} detectors × "
          f"{combined.pathogen.nunique()} pathogens")

    # ---- Save ----
    out_path = RESULTS_DIR / 'combined_10scoring_results.csv'
    combined.to_csv(out_path, index=False)
    print(f"\nSaved to {out_path}")

    # ---- Summary statistics ----
    print("\n" + "=" * 70)
    print("SUMMARY: Mean best MCC per scoring method (across 9 pathogens)")
    print("=" * 70)

    summary_rows = []
    for score in sorted(combined.score.unique()):
        score_df = combined[combined.score == score]
        best_per_pathogen = score_df.groupby('pathogen')['mcc_adaptive'].max()
        summary_rows.append({
            'scoring': score,
            'mean_best_mcc': round(best_per_pathogen.mean(), 4),
            'std_best_mcc': round(best_per_pathogen.std(), 4),
            'median_best_mcc': round(best_per_pathogen.median(), 4),
            'min_best_mcc': round(best_per_pathogen.min(), 4),
            'max_best_mcc': round(best_per_pathogen.max(), 4),
            'n_evaluations': len(score_df),
        })

    summary = pd.DataFrame(summary_rows).sort_values('mean_best_mcc', ascending=False)
    print(summary.to_string(index=False))

    # ---- ESM rank per pathogen ----
    print("\n" + "=" * 70)
    print("ESM-LLR rank among 10 scoring methods per pathogen")
    print("=" * 70)

    for pathogen in sorted(combined.pathogen.unique()):
        pat_df = combined[combined.pathogen == pathogen]
        best_per_score = pat_df.groupby('score')['mcc_adaptive'].max().sort_values(ascending=False)
        esm_mcc = best_per_score.get('ESM-LLR', np.nan)
        rank = list(best_per_score.index).index('ESM-LLR') + 1 if 'ESM-LLR' in best_per_score.index else 'N/A'
        print(f"  {pathogen}: ESM-LLR MCC={esm_mcc:.4f}, rank={rank}/10")

    # ---- ANOVA with 10 scoring methods ----
    print("\n" + "=" * 70)
    print("Two-way ANOVA: scoring × pathogen on MCC")
    print("=" * 70)

    # Best MCC per (scoring, pathogen)
    best_combos = combined.groupby(['score', 'pathogen'])['mcc_adaptive'].max().reset_index()

    # One-way ANOVA on scoring
    groups_scoring = [g['mcc_adaptive'].values for _, g in best_combos.groupby('score')]
    f_stat, p_val = sp_stats.f_oneway(*groups_scoring)
    print(f"  One-way ANOVA (scoring): F={f_stat:.4f}, p={p_val:.4f}")

    # Kruskal-Wallis (non-parametric)
    h_stat, p_kw = sp_stats.kruskal(*groups_scoring)
    print(f"  Kruskal-Wallis (scoring): H={h_stat:.4f}, p={p_kw:.4f}")

    # Friedman test on best detector per (scoring, pathogen) matrix
    # Rows = pathogens, columns = scoring methods
    pivot = best_combos.pivot(index='pathogen', columns='score', values='mcc_adaptive')
    if pivot.dropna().shape[0] >= 3:
        friedman_stat, friedman_p = sp_stats.friedmanchisquare(
            *[pivot[col].values for col in pivot.columns])
        print(f"  Friedman (scoring): chi2={friedman_stat:.4f}, p={friedman_p:.4f}")

    # ---- Interaction analysis ----
    print("\n" + "=" * 70)
    print("Interaction: does ESM-LLR have unique best combos?")
    print("=" * 70)

    for pathogen in sorted(combined.pathogen.unique()):
        pat_df = combined[combined.pathogen == pathogen]
        overall_best_idx = pat_df['mcc_adaptive'].idxmax()
        overall_best = pat_df.loc[overall_best_idx]
        is_esm = overall_best['score'] == 'ESM-LLR'
        marker = ' *** ESM-LLR wins!' if is_esm else ''
        print(f"  {pathogen}: best = {overall_best['score']} + {overall_best['detector']} "
              f"(MCC={overall_best['mcc_adaptive']:.4f}){marker}")


if __name__ == '__main__':
    main()
