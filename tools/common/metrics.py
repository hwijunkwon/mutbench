"""Clustering evaluation metrics: ARI, NMI, F-measure, cluster-score.

Implements the metrics from the MOSD paper (Han et al., BMC Genomics 2025).
"""
import numpy as np
from sklearn.metrics import adjusted_rand_score, normalized_mutual_info_score
from itertools import combinations


def adjusted_rand_index(true_labels, pred_labels) -> float:
    """Compute Adjusted Rand Index (chance-corrected). Range: [-1, 1]."""
    return float(adjusted_rand_score(true_labels, pred_labels))


def normalized_mutual_info(true_labels, pred_labels) -> float:
    """Compute Normalized Mutual Information. Range: [0, 1]."""
    return float(normalized_mutual_info_score(true_labels, pred_labels, average_method='arithmetic'))


def f_measure_pairwise(true_labels, pred_labels) -> float:
    """Compute pair-based F-measure using set operations.

    A = |Pairs(U) ∩ Pairs(V)|
    B = |Pairs(U) - Pairs(V)|
    C = |Pairs(V) - Pairs(U)|
    F = 2A / (2A + B + C)
    """
    true_labels = np.asarray(true_labels)
    pred_labels = np.asarray(pred_labels)
    n = len(true_labels)
    if n < 2:
        return 0.0

    indices = np.arange(n)
    pairs = list(combinations(indices, 2))

    true_same = set()
    pred_same = set()
    for i, j in pairs:
        if true_labels[i] == true_labels[j]:
            true_same.add((i, j))
        if pred_labels[i] == pred_labels[j]:
            pred_same.add((i, j))

    a = len(pred_same & true_same)
    b = len(pred_same - true_same)
    c = len(true_same - pred_same)

    denom = 2 * a + b + c
    if denom == 0:
        return 0.0
    return (2 * a) / denom


def cluster_score(true_labels, pred_labels) -> float:
    """Compute cluster-score = (ARI + NMI + F-measure) / 3."""
    ari = adjusted_rand_index(true_labels, pred_labels)
    nmi = normalized_mutual_info(true_labels, pred_labels)
    fm = f_measure_pairwise(true_labels, pred_labels)
    return (ari + nmi + fm) / 3.0
