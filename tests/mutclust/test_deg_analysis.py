import numpy as np
import pandas as pd
from tools.mutclust.deg_analysis.core import find_degs, filter_low_expression

def test_find_degs_detects_differential():
    np.random.seed(42)
    n_genes, n_samples = 100, 50
    groups = ['A']*25 + ['B']*25
    counts = pd.DataFrame(np.random.poisson(10, (n_samples, n_genes)),
                          columns=[f'gene{i}' for i in range(n_genes)])
    counts.iloc[:25, 0] = np.random.poisson(50, 25)
    counts.iloc[25:, 0] = np.random.poisson(5, 25)
    degs = find_degs(counts, groups, fdr=0.05)
    assert 'gene0' in degs[degs['significant']]['gene'].values

def test_filter_low_expression():
    counts = pd.DataFrame({
        'gene1': [0, 0, 0, 0, 10],
        'gene2': [5, 3, 7, 2, 8],
    })
    filtered = filter_low_expression(counts, zero_pct_threshold=0.8)
    assert 'gene2' in filtered.columns
    assert 'gene1' not in filtered.columns
