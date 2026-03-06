"""IntNMF wrapper. Simplified implementation using KMeans."""
import numpy as np
import pandas as pd
from sklearn.cluster import KMeans

def run_intnmf(omics_list: list[pd.DataFrame], n_clusters: int = 3) -> np.ndarray:
    combined = pd.concat(omics_list, axis=1).values
    km = KMeans(n_clusters=n_clusters, n_init=10, random_state=42)
    return km.fit_predict(combined)
