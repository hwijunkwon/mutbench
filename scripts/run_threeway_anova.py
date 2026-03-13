#!/usr/bin/env python3
"""
Three-way ANOVA: scoring × detection_family × pathogen.

Reports omega-squared (less biased than eta-squared).
Treats the analysis as variance decomposition since evaluations
are deterministic function evaluations, not random samples.

Output: threeway_anova_omega.csv
"""

import pandas as pd
import numpy as np
import statsmodels.api as sm
from statsmodels.formula.api import ols
from pathlib import Path

RESULTS_DIR = Path(__file__).parent.parent / 'results' / 'mutbench'


def omega_squared(aov_table, ss_total):
    """Compute omega-squared (less biased than eta-squared)."""
    results = {}
    ms_resid = aov_table.loc['Residual', 'sum_sq'] / aov_table.loc['Residual', 'df']
    for idx in aov_table.index:
        if idx == 'Residual':
            continue
        ss = aov_table.loc[idx, 'sum_sq']
        df_eff = aov_table.loc[idx, 'df']
        w2 = (ss - df_eff * ms_resid) / (ss_total + ms_resid)
        results[idx] = max(0, w2)
    return results


def main():
    multilayer_path = RESULTS_DIR / 'multilayer_9pathogen_results.csv'
    extended_path = RESULTS_DIR / 'extended_9pathogen_results.csv'

    if multilayer_path.exists():
        df = pd.read_csv(multilayer_path)
        mcc_col = 'mcc_adaptive'
    elif extended_path.exists():
        df = pd.read_csv(extended_path)
        mcc_col = 'mcc'
    else:
        print("ERROR: No results file found")
        return

    print(f"Total evaluations: {len(df)}")

    # Three-way ANOVA with two-way interactions
    formula = (f'{mcc_col} ~ C(score) + C(family) + C(pathogen) '
               f'+ C(score):C(family) + C(score):C(pathogen) + C(family):C(pathogen)')

    model = ols(formula, data=df).fit()
    aov = sm.stats.anova_lm(model, typ=2)

    ss_total = aov['sum_sq'].sum()
    w2 = omega_squared(aov, ss_total)

    print(f"\n{'Factor':<40} {'ω²':<10} {'η²':<10} {'F':<10} {'p':<12}")
    print('-' * 82)

    results = []
    for idx in aov.index:
        if idx == 'Residual':
            continue
        eta2 = aov.loc[idx, 'sum_sq'] / ss_total
        omega = w2.get(idx, 0)
        f_val = aov.loc[idx, 'F']
        p_val = aov.loc[idx, 'PR(>F)']
        print(f"{idx:<40} {omega:<10.4f} {eta2:<10.4f} {f_val:<10.2f} {p_val:<12.2e}")

        results.append({
            'factor': idx,
            'sum_sq': round(aov.loc[idx, 'sum_sq'], 6),
            'df': int(aov.loc[idx, 'df']),
            'F': round(f_val, 4),
            'p': p_val,
            'eta_squared': round(eta2, 6),
            'omega_squared': round(omega, 6),
        })

    results_df = pd.DataFrame(results)
    output_path = RESULTS_DIR / 'threeway_anova_omega.csv'
    results_df.to_csv(output_path, index=False)
    print(f"\nSaved to {output_path}")


if __name__ == '__main__':
    main()
