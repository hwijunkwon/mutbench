"""Consensus Clustering (CC)."""
import numpy as np
import pandas as pd
from sklearn.cluster import KMeans, spectral_clustering

def run_consensus_clustering(omics_list: list[pd.DataFrame], n_clusters: int = 3, n_resamples: int = 100, subsample_frac: float = 0.8) -> np.ndarray:
    combined = pd.concat(omics_list, axis=1).values
    n = combined.shape[0]
    consensus = np.zeros((n, n))
    counts = np.zeros((n, n))
    for _ in range(n_resamples):
        idx = np.random.choice(n, size=int(n * subsample_frac), replace=False)
        km = KMeans(n_clusters=n_clusters, n_init=10, random_state=None)
        labels = km.fit_predict(combined[idx])
        for i in range(len(idx)):
            for j in range(i + 1, len(idx)):
                counts[idx[i], idx[j]] += 1
                counts[idx[j], idx[i]] += 1
                if labels[i] == labels[j]:
                    consensus[idx[i], idx[j]] += 1
                    consensus[idx[j], idx[i]] += 1
    counts[counts == 0] = 1
    consensus_matrix = consensus / counts
    return spectral_clustering(consensus_matrix, n_clusters=n_clusters, random_state=42)
