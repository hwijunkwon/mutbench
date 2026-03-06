import numpy as np
import pandas as pd
from tools.mosd.benchmark.core import sample_size_test

def test_sample_size_test():
    np.random.seed(42)
    n, k = 120, 3
    labels = np.repeat(range(k), n // k)
    X = np.random.randn(n, 20)
    for c in range(k):
        X[labels == c] += np.random.randn(20) * 3
    data = pd.DataFrame(X)
    results = sample_size_test(data, labels, sizes=[10, 20, 40], repeats=2, method='CC', n_clusters=k)
    assert 'sample_size' in results.columns
    assert 'cluster_score' in results.columns
    assert len(results) == 6
