#!/usr/bin/env python3
"""
Pathogen-level BCa bootstrap CI for method rankings.

Resamples pathogens (not synthetic regions) to estimate uncertainty
of mean MCC across the 9-pathogen benchmark.

Output: pathogen_bootstrap_ci.csv
"""

import pandas as pd
import numpy as np
from scipy.stats import norm
from pathlib import Path

RESULTS_DIR = Path(__file__).parent.parent / 'results' / 'mutbench'
N_BOOT = 10000
SEED = 42


def bca_ci(data, n_boot=10000, alpha=0.05, rng=None):
    """BCa bootstrap confidence interval on the mean."""
    if rng is None:
        rng = np.random.RandomState(SEED)

    n = len(data)
    theta_hat = np.mean(data)

    # Bootstrap distribution
    boot_thetas = np.array([
        np.mean(data[rng.choice(n, n, replace=True)])
        for _ in range(n_boot)
    ])

    # Bias correction (z0)
    z0 = norm.ppf(np.mean(boot_thetas < theta_hat))
    if not np.isfinite(z0):
        z0 = 0.0

    # Acceleration (a) via jackknife
    jack_thetas = np.array([np.mean(np.delete(data, i)) for i in range(n)])
    jack_mean = jack_thetas.mean()
    num = np.sum((jack_mean - jack_thetas) ** 3)
    den = 6 * (np.sum((jack_mean - jack_thetas) ** 2) ** 1.5)
    a = num / den if den != 0 else 0

    # Adjusted percentiles
    z_lo = norm.ppf(alpha / 2)
    z_hi = norm.ppf(1 - alpha / 2)

    def adj(z):
        val = z0 + (z0 + z) / (1 - a * (z0 + z))
        return norm.cdf(val)

    a1, a2 = adj(z_lo), adj(z_hi)
    a1 = max(0.001, min(a1, 0.999))
    a2 = max(0.001, min(a2, 0.999))

    ci_lower = np.percentile(boot_thetas, 100 * a1)
    ci_upper = np.percentile(boot_thetas, 100 * a2)

    return theta_hat, ci_lower, ci_upper, z0, a


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

    df['combo'] = df['score'] + ' + ' + df['detector']
    pathogens = sorted(df['pathogen'].unique())

    rng = np.random.RandomState(SEED)

    # Top-20 combos by mean MCC
    combo_means = df.groupby('combo')[mcc_col].mean().sort_values(ascending=False)
    top_combos = combo_means.head(20).index.tolist()

    results = []
    for combo in top_combos:
        combo_df = df[df['combo'] == combo]
        mcc_per_pathogen = np.array([
            combo_df[combo_df['pathogen'] == p][mcc_col].values[0]
            if len(combo_df[combo_df['pathogen'] == p]) > 0 else 0.0
            for p in pathogens
        ])

        theta, ci_lo, ci_hi, z0, a = bca_ci(mcc_per_pathogen, N_BOOT, rng=rng)

        results.append({
            'combo': combo,
            'mean_mcc': round(theta, 4),
            'ci_lower': round(ci_lo, 4),
            'ci_upper': round(ci_hi, 4),
            'ci_width': round(ci_hi - ci_lo, 4),
            'z0': round(z0, 4),
            'acceleration': round(a, 4),
            'n_pathogens': len(pathogens),
        })

    results_df = pd.DataFrame(results)
    output_path = RESULTS_DIR / 'pathogen_bootstrap_ci.csv'
    results_df.to_csv(output_path, index=False)
    print(results_df.to_string())
    print(f"\nSaved to {output_path}")


if __name__ == '__main__':
    main()
