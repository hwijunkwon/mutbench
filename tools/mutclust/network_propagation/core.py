"""Network propagation: p^(t+1) = (1-alpha)*W*p^t + alpha*p_0"""
import numpy as np
import networkx as nx

def build_adjacency_matrix(G):
    nodes = sorted(G.nodes())
    n = len(nodes)
    node_idx = {node: i for i, node in enumerate(nodes)}
    W = np.zeros((n, n))
    for u, v in G.edges():
        i, j = node_idx[u], node_idx[v]
        W[i, j] = 1; W[j, i] = 1
    row_sums = W.sum(axis=1)
    row_sums[row_sums == 0] = 1
    W = W / row_sums[:, None]
    return W, nodes

def propagate(G, seeds, alpha=0.01, max_iter=1000, tol=1e-6):
    W, nodes = build_adjacency_matrix(G)
    n = len(nodes)
    node_idx = {node: i for i, node in enumerate(nodes)}
    p0 = np.zeros(n)
    for seed in seeds:
        if seed in node_idx:
            p0[node_idx[seed]] = 1.0
    if p0.sum() == 0:
        return {node: 0.0 for node in nodes}
    p0 = p0 / p0.sum()
    p = p0.copy()
    for _ in range(max_iter):
        p_new = (1 - alpha) * W.T @ p + alpha * p0
        if np.linalg.norm(p_new - p) < tol:
            break
        p = p_new
    return {node: float(p[i]) for i, node in enumerate(nodes)}

def get_top_genes(scores, n=100, exclude=None):
    if exclude is None:
        exclude = set()
    filtered = {k: v for k, v in scores.items() if k not in exclude}
    return sorted(filtered.items(), key=lambda x: x[1], reverse=True)[:n]
