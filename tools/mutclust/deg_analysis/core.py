"""Differential Expression Gene analysis using Mann-Whitney U test."""
import numpy as np
import pandas as pd
from scipy import stats
from tools.common.stats import benjamini_hochberg

def filter_low_expression(counts, zero_pct_threshold=0.8):
    zero_frac = (counts == 0).sum(axis=0) / len(counts)
    return counts.loc[:, zero_frac < zero_pct_threshold]

def find_degs(counts, groups, fdr=0.05, test='mannwhitney'):
    groups = np.array(groups)
    unique_groups = np.unique(groups)
    if len(unique_groups) != 2:
        raise ValueError(f"Expected 2 groups, got {len(unique_groups)}")
    g1_mask = groups == unique_groups[0]
    g2_mask = groups == unique_groups[1]
    results = []
    for gene in counts.columns:
        vals1 = counts.loc[g1_mask, gene].values.astype(float)
        vals2 = counts.loc[g2_mask, gene].values.astype(float)
        log2fc = np.log2((vals1.mean() + 1) / (vals2.mean() + 1))
        if test == 'mannwhitney':
            stat, pval = stats.mannwhitneyu(vals1, vals2, alternative='two-sided')
        else:
            stat, pval = stats.ttest_ind(vals1, vals2)
        results.append({'gene': gene, 'mean_g1': vals1.mean(), 'mean_g2': vals2.mean(),
                        'log2fc': log2fc, 'statistic': stat, 'pvalue': pval})
    df = pd.DataFrame(results)
    df['adjusted_p'] = benjamini_hochberg(df['pvalue'].tolist())
    df['significant'] = df['adjusted_p'] < fdr
    return df
