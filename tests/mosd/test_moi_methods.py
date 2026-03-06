import numpy as np
import pandas as pd
from tools.mosd.moi_methods.snf import run_snf
from tools.mosd.moi_methods.spectrum import run_spectrum
from tools.mosd.moi_methods.consensus_clustering import run_consensus_clustering

def _make_test_omics(n=60, k=3):
    np.random.seed(42)
    labels = np.repeat(range(k), n // k)
    omics = []
    for _ in range(2):
        X = np.random.randn(n, 50)
        for c in range(k):
            X[labels == c] += np.random.randn(50) * 3
        omics.append(pd.DataFrame(X))
    return omics, labels

def test_snf_returns_labels():
    omics, true = _make_test_omics()
    labels = run_snf(omics, n_clusters=3)
    assert len(labels) == 60
    assert len(set(labels)) == 3

def test_spectrum_returns_labels():
    omics, true = _make_test_omics()
    labels = run_spectrum(omics, n_clusters=3)
    assert len(labels) == 60

def test_cc_returns_labels():
    omics, true = _make_test_omics()
    labels = run_consensus_clustering(omics, n_clusters=3)
    assert len(labels) == 60
    assert len(set(labels)) == 3
