import numpy as np
import pandas as pd
from tools.mosd.feature_selection.core import select_features_chi2, select_features_anova

def test_chi2_selects_informative():
    np.random.seed(42)
    n = 100
    labels = np.array([0]*50 + [1]*50)
    f1 = labels + np.random.normal(0, 0.1, n)
    noise = np.random.normal(0, 1, (n, 9))
    data = pd.DataFrame(np.column_stack([f1, noise]), columns=[f'f{i}' for i in range(10)])
    data = data - data.min() + 0.01
    selected = select_features_chi2(data, labels, top_pct=10)
    assert 'f0' in selected.columns

def test_anova_selects_informative():
    np.random.seed(42)
    n = 100
    labels = np.array([0]*50 + [1]*50)
    f1 = labels * 5 + np.random.normal(0, 0.5, n)
    noise = np.random.normal(0, 1, (n, 9))
    data = pd.DataFrame(np.column_stack([f1, noise]), columns=[f'f{i}' for i in range(10)])
    selected = select_features_anova(data, labels, top_pct=10)
    assert 'f0' in selected.columns

def test_top_pct_limits_features():
    np.random.seed(42)
    n = 100
    labels = np.array([0]*50 + [1]*50)
    data = pd.DataFrame(np.random.rand(n, 100), columns=[f'f{i}' for i in range(100)])
    selected = select_features_chi2(data, labels, top_pct=10)
    assert selected.shape[1] == 10
