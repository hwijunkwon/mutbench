"""MutClust variant registry for benchmark comparison."""
import numpy as np
import math

# Constants
CCM_HSCORE_MIN = 0.03
CCM_MEAN_MIN = 0.01
CCM_SUM_MIN = 0.05
CCM_MIN_POINTS = 5

class Cluster:
    def __init__(self, seed: int, positions: list[int]):
        self.seed = seed
        self.positions = positions

    @property
    def start(self) -> int:
        return min(self.positions) if self.positions else self.seed

    @property
    def end(self) -> int:
        return max(self.positions) if self.positions else self.seed

    @property
    def size(self) -> int:
        return len(self.positions)

def compute_deps(hscore: float, gamma: int = 10) -> int:
    return int(math.ceil(gamma * hscore))

def is_ccm(pos: int, hscores: np.ndarray, gamma: int = 10, minpts: int = 5) -> bool:
    h = hscores[pos]
    if h <= CCM_HSCORE_MIN:
        return False
    deps = compute_deps(h, gamma)
    start = max(0, pos - deps)
    end = min(len(hscores), pos + deps + 1)
    neighborhood = hscores[start:end]
    if np.mean(neighborhood) <= CCM_MEAN_MIN:
        return False
    if np.sum(neighborhood) <= CCM_SUM_MIN:
        return False
    nonzero = np.sum(neighborhood > 0)
    if nonzero < minpts:
        return False
    return True

def _merge_overlapping(clusters: list[Cluster]) -> list[Cluster]:
    if not clusters:
        return []
    sorted_clusters = sorted(clusters, key=lambda c: c.start)
    merged = [sorted_clusters[0]]
    for current in sorted_clusters[1:]:
        previous = merged[-1]
        if current.start <= previous.end + 1:
            all_pos = set(previous.positions) | set(current.positions)
            merged[-1] = Cluster(seed=previous.seed, positions=sorted(list(all_pos)))
        else:
            merged.append(current)
    return merged

def _expand_cluster(seed: int, hscores: np.ndarray, gamma: int, d: int, minpts: int) -> Cluster:
    cluster = Cluster(seed=seed, positions=[seed])
    deps_ccm = compute_deps(hscores[seed], gamma)
    for direction in [-1, 1]:
        distance = 0
        while True:
            distance += 1
            next_pos = seed + direction * distance
            if next_pos < 0 or next_pos >= len(hscores):
                break
            current_deps = deps_ccm - (distance / d)
            if current_deps <= 0:
                break
            if hscores[next_pos] > 0:
                cluster.positions.append(next_pos)
    cluster.positions.sort()
    return cluster

def mutclust(hscores: np.ndarray, gamma: int = 10, d: int = 3, minpts: int = 5) -> list[Cluster]:
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
        cluster = _expand_cluster(ccm, hscores, gamma, d, minpts)
        if cluster.size >= minpts:
            clusters.append(cluster)
            assigned.update(cluster.positions)
    return _merge_overlapping(clusters)


def _clusters_to_dicts(clusters):
    """Convert Cluster objects to standard dict format."""
    return [{'start': c.start, 'end': c.end, 'positions': list(c.positions)} for c in clusters]


def _expand_cluster_v1(seed, hscores, gamma, d, minpts):
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
        try:
            from tools.mutclust.dnds_annotation.core import annotate_clusters
            annotated = annotate_clusters(result, reference_seq, mutations)
            result = [c for c in annotated if c.get('dnds', 0) > 1.0]
        except ImportError:
            pass # Skip dNdS if missing
    return result

@register('v2c-full')
def detect_v2c(hscores, **params):
    """MutClust CCM seed detection + HDBSCAN cluster boundaries + dN/dS filtering."""
    from sklearn.cluster import HDBSCAN as _HDBSCAN
    hscores = np.asarray(hscores, dtype=float)
    n = len(hscores)
    gamma = params.get('gamma', 10)
    minpts = params.get('minpts', 5)
    min_cluster_size = params.get('min_cluster_size', 5)
    min_samples = params.get('min_samples', 3)

    # Step 1: Find CCM seeds using MutClust criterion
    ccm_seeds = [i for i in range(n) if is_ccm(i, hscores, gamma, minpts)]
    if not ccm_seeds:
        return []

    # Step 2: Collect non-zero positions in regions around CCM seeds
    # Use deps range around each seed
    candidate_positions = set()
    for seed in ccm_seeds:
        deps = compute_deps(hscores[seed], gamma)
        start = max(0, seed - deps)
        end = min(n, seed + deps + 1)
        for pos in range(start, end):
            if hscores[pos] > 0:
                candidate_positions.add(pos)

    candidate_positions = sorted(candidate_positions)
    if len(candidate_positions) < 2:
        return []

    # Step 3: HDBSCAN clustering on candidate positions
    idx = np.array(candidate_positions)
    X = np.column_stack([
        idx.astype(float),
        hscores[idx],
    ])
    pos_range = idx[-1] - idx[0] if len(idx) > 1 else 1
    X[:, 0] = X[:, 0] / max(pos_range, 1) * np.max(hscores[idx])

    clusterer = _HDBSCAN(
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
        positions = sorted(idx[mask].tolist())
        if positions:
            clusters.append({
                'start': positions[0],
                'end': positions[-1],
                'positions': positions,
            })

    clusters = sorted(clusters, key=lambda c: c['start'])

    # Step 4: Optional dN/dS filtering
    reference_seq = params.get('reference_seq')
    mutations = params.get('mutations')
    if reference_seq and mutations:
        try:
            from tools.mutclust.dnds_annotation.core import annotate_clusters
            annotated = annotate_clusters(clusters, reference_seq, mutations)
            clusters = [c for c in annotated if c.get('dnds', 0) > 1.0]
        except ImportError:
            pass # Skip dNdS if missing

    return clusters

@register('v3-hdbscan')
def detect_v3_hdbscan(hscores, **params):
    """HDBSCAN-based automatic hotspot detection. No gamma/d/minpts needed."""
    from sklearn.cluster import HDBSCAN
    hscores = np.asarray(hscores, dtype=float)

    # Adaptive threshold: filter out background noise before clustering.
    # Use an explicit threshold if provided, otherwise use median of non-zero
    # scores as the cutoff to separate signal from background.
    nonzero_vals = hscores[hscores > 0]
    if len(nonzero_vals) < 2:
        return []
    score_threshold = params.get('score_threshold', float(np.median(nonzero_vals)))

    nonzero_idx = np.where(hscores > score_threshold)[0]
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

@register('v4-optics')
def detect_v4_optics(hscores, **params):
    """OPTICS density-based clustering on (position, H-score) feature space."""
    from sklearn.cluster import OPTICS as _OPTICS
    hscores = np.asarray(hscores, dtype=float)

    # Same adaptive threshold as v3-hdbscan
    nonzero_vals = hscores[hscores > 0]
    if len(nonzero_vals) < 2:
        return []
    score_threshold = params.get('score_threshold', float(np.median(nonzero_vals)))

    nonzero_idx = np.where(hscores > score_threshold)[0]
    if len(nonzero_idx) < 2:
        return []

    # Build 2D feature space (position, H-score) — same as HDBSCAN variants
    X = np.column_stack([
        nonzero_idx.astype(float),
        hscores[nonzero_idx],
    ])
    pos_range = nonzero_idx[-1] - nonzero_idx[0] if len(nonzero_idx) > 1 else 1
    X[:, 0] = X[:, 0] / max(pos_range, 1) * np.max(hscores[nonzero_idx])

    min_samples = params.get('min_samples', 5)
    xi = params.get('xi', 0.05)

    clusterer = _OPTICS(
        min_samples=min_samples,
        xi=xi,
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


def _percentile_normalize(hscores, top_pct=30):
    """Normalize H-scores to percentile ranks, zeroing out low-signal positions.

    Converts absolute H-scores to relative rankings so that only positions
    with scores above the (100 - top_pct) percentile retain signal.
    This adapts to varying diversity levels across viruses/timepoints.
    """
    hscores = np.asarray(hscores, dtype=float)
    nonzero = hscores[hscores > 0]
    if len(nonzero) == 0:
        return np.zeros_like(hscores)

    threshold = np.percentile(nonzero, 100 - top_pct)
    normalized = np.zeros_like(hscores)

    above = hscores >= threshold
    if np.any(above):
        vals = hscores[above]
        from scipy.stats import rankdata
        ranks = rankdata(vals, method='average')
        max_h = np.max(nonzero)
        normalized[above] = (ranks / ranks.max()) * max_h

    return normalized


@register('v5-kde')
def detect_v5_kde(hscores, **params):
    """KDE-based hotspot detection: estimate density of H-scores, find peaks."""
    from scipy.stats import gaussian_kde
    from scipy.signal import find_peaks
    hscores = np.asarray(hscores, dtype=float)

    # Filter to positions with non-zero H-scores
    nonzero_idx = np.where(hscores > 0)[0]
    if len(nonzero_idx) < 3:
        return []

    # Use H-scores as weights for KDE over genomic positions
    values = hscores[nonzero_idx]
    bandwidth = params.get('bandwidth', None)

    # Build KDE of H-score-weighted positions
    try:
        kde = gaussian_kde(nonzero_idx, weights=values, bw_method=bandwidth)
    except (np.linalg.LinAlgError, ValueError):
        return []

    # Evaluate KDE across all positions
    n = len(hscores)
    x_grid = np.arange(n, dtype=float)
    density = kde(x_grid)

    # Find peaks in the density
    peak_threshold_pct = params.get('peak_threshold_pct', 90)
    threshold = np.percentile(density[density > 0], peak_threshold_pct) if np.any(density > 0) else 0
    min_peak_distance = params.get('min_peak_distance', 50)

    peaks, properties = find_peaks(density, height=threshold, distance=min_peak_distance)
    if len(peaks) == 0:
        return []

    # Expand each peak into a cluster: include nearby positions with H-score > 0
    cluster_radius = params.get('cluster_radius', 30)
    clusters = []
    assigned = set()
    for peak in peaks:
        start = max(0, peak - cluster_radius)
        end = min(n, peak + cluster_radius + 1)
        positions = []
        for pos in range(start, end):
            if hscores[pos] > 0 and pos not in assigned:
                positions.append(pos)
        if len(positions) >= 3:
            assigned.update(positions)
            positions.sort()
            clusters.append({
                'start': positions[0],
                'end': positions[-1],
                'positions': positions,
            })

    return sorted(clusters, key=lambda c: c['start'])


@register('v6-normalized')
def detect_v6_normalized(hscores, **params):
    """MutClust with percentile-normalized H-scores.

    Addresses H-score saturation in high-diversity data by converting
    absolute scores to relative rankings before DBSCAN clustering.
    Only the top N% of positions retain signal.
    """
    top_pct = params.get('top_pct', 30)
    norm_hscores = _percentile_normalize(hscores, top_pct=top_pct)

    gamma = params.get('gamma', 10)
    d = params.get('d', 3)
    minpts = params.get('minpts', 5)
    clusters = mutclust(norm_hscores, gamma, d, minpts)
    return _clusters_to_dicts(clusters)
