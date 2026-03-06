"""Similarity Network Fusion (SNF) wrapper."""
import numpy as np
import pandas as pd
from sklearn.metrics import pairwise_distances
from sklearn.cluster import spectral_clustering

def _make_affinity(X, k=20, mu=0.5):
    dist = pairwise_distances(X, metric='euclidean')
    knn_dist = np.sort(dist, axis=1)[:, 1:k+1]
    sigma = knn_dist.mean(axis=1)
    sigma_matrix = np.outer(sigma, sigma)
    sigma_matrix[sigma_matrix == 0] = 1e-10
    W = np.exp(-dist**2 / (mu * sigma_matrix))
    np.fill_diagonal(W, 0)
    return W

def _normalize_affinity(W):
    D = W.sum(axis=1)
    D[D == 0] = 1e-10
    return W / D[:, None]

def _snf_fuse(affinities, k=20, n_iter=20):
    n = affinities[0].shape[0]
    m = len(affinities)
    P = [_normalize_affinity(W) for W in affinities]
    S = []
    for W in affinities:
        S_i = np.zeros_like(W)
        for i in range(n):
            neighbors = np.argsort(W[i])[-k:]
            S_i[i, neighbors] = W[i, neighbors]
        S_i = (S_i + S_i.T) / 2
        S_i = _normalize_affinity(S_i)
        S.append(S_i)
    for _ in range(n_iter):
        P_new = []
        for j in range(m):
            others = [P[i] for i in range(m) if i != j]
            avg_others = np.mean(others, axis=0)
            P_j = S[j] @ avg_others @ S[j].T
            P_j = _normalize_affinity(P_j)
            P_new.append(P_j)
        P = P_new
    fused = np.mean(P, axis=0)
    fused = (fused + fused.T) / 2
    return fused

def run_snf(omics_list: list[pd.DataFrame], n_clusters: int = 3, k: int = 20, n_iter: int = 20) -> np.ndarray:
    affinities = [_make_affinity(df.values, k=k) for df in omics_list]
    fused = _snf_fuse(affinities, k=k, n_iter=n_iter)
    fused = np.maximum(fused, 0)
    return spectral_clustering(fused, n_clusters=n_clusters, random_state=42)
