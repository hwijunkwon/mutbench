import numpy as np
from tools.mutclust.bootstrap.core import bootstrap_hotspot_test

def test_significant_hotspot():
    np.random.seed(42)
    hscores = np.zeros(1000)
    hscores[100:120] = np.random.uniform(0.5, 1.0, 20)
    result = bootstrap_hotspot_test(hscores, start=100, end=119, n_iter=500)
    assert result['p_value'] < 0.05

def test_nonsignificant_region():
    np.random.seed(42)
    hscores = np.random.uniform(0, 0.01, 1000)
    result = bootstrap_hotspot_test(hscores, start=100, end=119, n_iter=500)
    assert result['p_value'] > 0.05
