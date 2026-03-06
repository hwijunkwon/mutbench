"""MutClust variant registry for benchmark comparison."""
import numpy as np
from math import ceil
from tools.mutclust.mutclust_algo.core import (
    mutclust, Cluster, compute_deps, is_ccm, _merge_overlapping,
    CCM_HSCORE_MIN, CCM_MEAN_MIN, CCM_SUM_MIN,
)


def _clusters_to_dicts(clusters):
    """Convert Cluster objects to standard dict format."""
    return [{'start': c.start, 'end': c.end, 'positions': list(c.positions)} for c in clusters]


def _expand_cluster_v1(seed, hscores, gamma, d, minpts):
    """Original (buggy) expand_cluster with cumulative subtraction."""
    from tools.mutclust.mutclust_algo.core import Cluster
    cluster = Cluster(seed=seed, positions=[seed])
    deps_ccm = compute_deps(hscores[seed], gamma)
    for direction in [-1, 1]:
        current_deps = deps_ccm
        distance = 0
        while True:
            distance += 1
            next_pos = seed + direction * distance
            if next_pos < 0 or next_pos >= len(hscores):
                break
            current_deps = current_deps - (deps_ccm - distance) / d  # BUG: cumulative
            if distance > current_deps:
                break
            if hscores[next_pos] > 0:
                cluster.positions.append(next_pos)
    cluster.positions.sort()
    return cluster


def _mutclust_v1(hscores, gamma=10, d=3, minpts=5):
    """Original MutClust with buggy expand_cluster."""
    hscores = np.asarray(hscores, dtype=float)
    n = len(hscores)
    ccms = [i for i in range(n) if is_ccm(i, hscores, gamma, minpts)]
    if not ccms:
        return []
    clusters = []
    assigned = set()
    for ccm in ccms:
        if ccm in assigned:
            continue
        cluster = _expand_cluster_v1(ccm, hscores, gamma, d, minpts)
        if cluster.size >= minpts:
            clusters.append(cluster)
            assigned.update(cluster.positions)
    return _merge_overlapping(clusters)


# --- Registry ---

VARIANTS = {}

def register(name):
    def decorator(fn):
        VARIANTS[name] = fn
        return fn
    return decorator

def get_variant(name):
    return VARIANTS[name]

def list_variants():
    return list(VARIANTS.keys())

@register('v1-original')
def detect_v1(hscores, **params):
    gamma = params.get('gamma', 10)
    d = params.get('d', 3)
    minpts = params.get('minpts', 5)
    clusters = _mutclust_v1(hscores, gamma, d, minpts)
    return _clusters_to_dicts(clusters)

@register('v2a-bugfix')
def detect_v2a(hscores, **params):
    gamma = params.get('gamma', 10)
    d = params.get('d', 3)
    minpts = params.get('minpts', 5)
    clusters = mutclust(hscores, gamma, d, minpts)
    return _clusters_to_dicts(clusters)

@register('v2b-bugfix+dnds')
def detect_v2b(hscores, **params):
    gamma = params.get('gamma', 10)
    d = params.get('d', 3)
    minpts = params.get('minpts', 5)
    clusters = mutclust(hscores, gamma, d, minpts)
    result = _clusters_to_dicts(clusters)
    reference_seq = params.get('reference_seq')
    mutations = params.get('mutations')
    if reference_seq and mutations:
        from tools.mutclust.dnds_annotation.core import annotate_clusters
        annotated = annotate_clusters(result, reference_seq, mutations)
        result = [c for c in annotated if c.get('dnds', 0) > 1.0]
    return result

@register('v2c-full')
def detect_v2c(hscores, **params):
    gamma = params.get('gamma', 10)
    d = params.get('d', 3)
    minpts = params.get('minpts', 5)
    clusters = mutclust(hscores, gamma, d, minpts)
    return _clusters_to_dicts(clusters)

@register('v3-hdbscan')
def detect_v3_hdbscan(hscores, **params):
    """HDBSCAN-based automatic hotspot detection. No gamma/d/minpts needed."""
    from sklearn.cluster import HDBSCAN
    hscores = np.asarray(hscores, dtype=float)

    nonzero_idx = np.where(hscores > 0)[0]
    if len(nonzero_idx) < 2:
        return []

    X = np.column_stack([
        nonzero_idx.astype(float),
        hscores[nonzero_idx],
    ])

    pos_range = nonzero_idx[-1] - nonzero_idx[0] if len(nonzero_idx) > 1 else 1
    X[:, 0] = X[:, 0] / max(pos_range, 1) * np.max(hscores[nonzero_idx])

    min_cluster_size = params.get('min_cluster_size', 5)
    min_samples = params.get('min_samples', 3)

    clusterer = HDBSCAN(
        min_cluster_size=min_cluster_size,
        min_samples=min_samples,
        metric='euclidean',
    )
    labels = clusterer.fit_predict(X)

    clusters = []
    for label in set(labels):
        if label == -1:
            continue
        mask = labels == label
        positions = sorted(nonzero_idx[mask].tolist())
        if positions:
            clusters.append({
                'start': positions[0],
                'end': positions[-1],
                'positions': positions,
            })

    return sorted(clusters, key=lambda c: c['start'])
