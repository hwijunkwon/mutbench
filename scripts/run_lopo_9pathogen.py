#!/usr/bin/env python3
"""
Leave-One-Pathogen-Out (LOPO) 9-pathogen cross-validation.

For each held-out pathogen:
  1. Select best combo by mean MCC across 8 training pathogens
  2. Evaluate that combo on the held-out pathogen
  3. Compare with oracle (best possible on held-out)
  4. gap = oracle - LOPO shows generalization loss

Output: lopo_9pathogen_cv.csv
"""

import pandas as pd
import numpy as np
from pathlib import Path

RESULTS_DIR = Path(__file__).parent.parent / 'results' / 'mutbench'


def main():
    # Try multilayer first, fall back to extended
    multilayer_path = RESULTS_DIR / 'multilayer_9pathogen_results.csv'
    extended_path = RESULTS_DIR / 'extended_9pathogen_results.csv'

    if multilayer_path.exists():
        df = pd.read_csv(multilayer_path)
        mcc_col = 'mcc_adaptive'
        print(f"Using multilayer results ({len(df)} rows)")
    elif extended_path.exists():
        df = pd.read_csv(extended_path)
        mcc_col = 'mcc'
        print(f"Using extended results ({len(df)} rows)")
    else:
        print("ERROR: No results file found")
        return

    df['combo'] = df['score'] + ' + ' + df['detector']
    pathogens = sorted(df['pathogen'].unique())
    print(f"Pathogens ({len(pathogens)}): {pathogens}")

    results = []
    for held_out in pathogens:
        train_pathogens = [p for p in pathogens if p != held_out]
        train_df = df[df['pathogen'].isin(train_pathogens)]
        test_df = df[df['pathogen'] == held_out]

        # Best combo by mean MCC on training set
        combo_means = train_df.groupby('combo')[mcc_col].mean()
        best_combo = combo_means.idxmax()
        train_mcc = combo_means[best_combo]

        # Test on held-out
        test_row = test_df[test_df['combo'] == best_combo]
        test_mcc = test_row[mcc_col].values[0] if len(test_row) > 0 else 0.0

        # Oracle
        oracle_mcc = test_df[mcc_col].max()
        oracle_combo = test_df.loc[test_df[mcc_col].idxmax(), 'combo']

        gap = oracle_mcc - test_mcc
        ratio = test_mcc / oracle_mcc if oracle_mcc > 0 else 0

        results.append({
            'held_out': held_out,
            'best_train_combo': best_combo,
            'train_mean_mcc': round(train_mcc, 4),
            'test_mcc': round(test_mcc, 4),
            'oracle_mcc': round(oracle_mcc, 4),
            'oracle_combo': oracle_combo,
            'gap': round(gap, 4),
            'generalization_ratio': round(ratio, 4),
            'combo_match': best_combo == oracle_combo,
        })

        print(f"\n{held_out}:")
        print(f"  Train best: {best_combo} (mean={train_mcc:.4f})")
        print(f"  Test: {test_mcc:.4f}  Oracle: {oracle_mcc:.4f}  Gap: {gap:.4f}")

    results_df = pd.DataFrame(results)
    output_path = RESULTS_DIR / 'lopo_9pathogen_cv.csv'
    results_df.to_csv(output_path, index=False)

    print(f"\n{'='*60}")
    print(f"Mean generalization ratio: {results_df['generalization_ratio'].mean():.4f}")
    print(f"Mean gap: {results_df['gap'].mean():.4f}")
    print(f"Combo matches: {results_df['combo_match'].sum()}/{len(pathogens)}")
    print(f"Saved to {output_path}")


if __name__ == '__main__':
    main()
