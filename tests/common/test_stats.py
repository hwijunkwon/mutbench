import numpy as np
from tools.common.stats import benjamini_hochberg, bootstrap_test


def test_bh_correction_basic():
    pvalues = [0.01, 0.04, 0.03, 0.20]
    adjusted = benjamini_hochberg(pvalues)
    assert len(adjusted) == 4
    assert all(a >= p for a, p in zip(adjusted, pvalues))


def test_bh_all_significant():
    pvalues = [0.001, 0.002, 0.003]
    adjusted = benjamini_hochberg(pvalues)
    assert all(a < 0.05 for a in adjusted)


def test_bootstrap_test_significant():
    np.random.seed(42)
    observed = 100.0
    null_dist = np.random.normal(50, 10, 1000)
    p = bootstrap_test(observed, null_dist)
    assert p < 0.05


def test_bootstrap_test_not_significant():
    np.random.seed(42)
    observed = 50.0
    null_dist = np.random.normal(50, 10, 1000)
    p = bootstrap_test(observed, null_dist)
    assert p > 0.05
