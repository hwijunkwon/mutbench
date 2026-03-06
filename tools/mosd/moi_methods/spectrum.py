"""Spectrum: density-aware spectral clustering."""
import numpy as np
import pandas as pd
from sklearn.cluster import SpectralClustering

def run_spectrum(omics_list: list[pd.DataFrame], n_clusters: int = 3) -> np.ndarray:
    combined = pd.concat(omics_list, axis=1).values
    model = SpectralClustering(n_clusters=n_clusters, affinity='nearest_neighbors', n_neighbors=10, random_state=42)
    return model.fit_predict(combined)
