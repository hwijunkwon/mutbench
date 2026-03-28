"""Position-level evaluation metrics for mutation hotspot benchmark."""
import numpy as np


def precision(detected_positions: set[int], ground_truth_positions: set[int]) -> float:
    if not detected_positions:
        return 0.0
    return len(detected_positions & ground_truth_positions) / len(detected_positions)


def recall(detected_positions: set[int], ground_truth_positions: set[int]) -> float:
    if not ground_truth_positions:
        return 0.0
    return len(detected_positions & ground_truth_positions) / len(ground_truth_positions)


def f1_score(detected_positions: set[int], ground_truth_positions: set[int]) -> float:
    p = precision(detected_positions, ground_truth_positions)
    r = recall(detected_positions, ground_truth_positions)
    if p + r == 0:
        return 0.0
    return 2 * p * r / (p + r)


def enrichment_ratio(detected_positions: set[int],
                      ground_truth_positions: set[int],
                      genome_length: int) -> float:
    if not detected_positions or genome_length == 0:
        return 0.0
    observed_ratio = len(detected_positions & ground_truth_positions) / len(detected_positions)
    expected_ratio = len(ground_truth_positions) / genome_length
    if expected_ratio == 0:
        return float('inf') if observed_ratio > 0 else 0.0
    return observed_ratio / expected_ratio


def dnds_enrichment(cluster_dnds_values: list[float]) -> float:
    if not cluster_dnds_values:
        return 0.0
    finite_vals = [v for v in cluster_dnds_values if np.isfinite(v)]
    if not finite_vals:
        return float('inf')
    return float(np.mean(finite_vals))


def evaluate_method(detected_clusters: list[dict],
                     ground_truth_positions: set[int],
                     genome_length: int) -> dict:
    detected = set()
    for c in detected_clusters:
        detected.update(c['positions'])
    return {
        'precision': precision(detected, ground_truth_positions),
        'recall': recall(detected, ground_truth_positions),
        'f1': f1_score(detected, ground_truth_positions),
        'enrichment_ratio': enrichment_ratio(detected, ground_truth_positions, genome_length),
        'n_detected': len(detected),
        'n_clusters': len(detected_clusters),
    }


def hotspot_score(recall_known: float, precision_simulated: float, stability: float) -> float:
    """Composite hotspot evaluation score (inspired by MOSD cluster-score).

    hotspot-score = (recall_known + precision_simulated + stability) / 3
    """
    return (recall_known + precision_simulated + stability) / 3


def compute_stability(hscores, detect_fn, n_iter: int = 100,
                      subsample_frac: float = 0.8, seed: int = 42) -> float:
    """Bootstrap subsampling stability of detected hotspots.

    Subsamples the H-scores n_iter times, runs detection on each subsample,
    and computes the mean Jaccard similarity with the full-data result.
    """
    hscores = np.asarray(hscores, dtype=float)
    n = len(hscores)

    # Full-data reference
    full_clusters = detect_fn(hscores)
    full_positions = set()
    for c in full_clusters:
        full_positions.update(c['positions'])

    if not full_positions:
        return 0.0

    rng = np.random.default_rng(seed)
    jaccard_scores = []

    for _ in range(n_iter):
        # Create subsampled H-scores (zero out random positions)
        mask = rng.random(n) < subsample_frac
        sub_hscores = hscores.copy()
        sub_hscores[~mask] = 0.0

        sub_clusters = detect_fn(sub_hscores)
        sub_positions = set()
        for c in sub_clusters:
            sub_positions.update(c['positions'])

        # Jaccard similarity
        if not full_positions and not sub_positions:
            jaccard_scores.append(1.0)
        elif not full_positions or not sub_positions:
            jaccard_scores.append(0.0)
        else:
            intersection = len(full_positions & sub_positions)
            union = len(full_positions | sub_positions)
            jaccard_scores.append(intersection / union)

    return float(np.mean(jaccard_scores))


def circular_permutation_test(
    hscores,
    detect_fn,
    ground_truth_positions: set[int],
    genome_length: int,
    n_perm: int = 1000,
    metric_fn=None,
    seed: int = 42,
    detect_kwargs: dict | None = None,
) -> dict:
    """Block (circular) permutation null model for hotspot detection significance.

    Instead of randomly shuffling H-scores (which destroys spatial
    autocorrelation), this rotates the entire H-score vector by a random
    offset.  Position i's H-score becomes position (i + k) mod N.  Hotspot
    detection is re-run on the rotated scores and evaluated against the
    *original* ground-truth positions.  This tests whether the spatial
    overlap between detected hotspots and ground truth is non-random while
    preserving the clustering structure of the H-scores.

    Args:
        hscores: 1-D array of H-scores (length = genome_length).
        detect_fn: Callable that takes (hscores, **kwargs) and returns a
            list of cluster dicts (each with a 'positions' key).
        ground_truth_positions: Set of ground-truth nucleotide positions.
        genome_length: Total genome length (should equal len(hscores)).
        n_perm: Number of circular permutations (default 1000).
        metric_fn: Optional callable(detected_set, gt_set) -> float.
            Defaults to F1 score.
        seed: Random seed.
        detect_kwargs: Extra keyword arguments forwarded to detect_fn.

    Returns:
        dict with keys: observed, null_mean, null_std, p_value, null_dist.
    """
    hscores = np.asarray(hscores, dtype=float)
    n = len(hscores)
    if detect_kwargs is None:
        detect_kwargs = {}
    if metric_fn is None:
        metric_fn = f1_score

    # --- Observed statistic ---
    obs_clusters = detect_fn(hscores, **detect_kwargs)
    obs_positions = set()
    for c in obs_clusters:
        obs_positions.update(c['positions'])
    observed = metric_fn(obs_positions, ground_truth_positions)

    # --- Null distribution via circular shifts ---
    rng = np.random.default_rng(seed)
    null_values = np.empty(n_perm)

    for i in range(n_perm):
        # Random offset in [1, n-1] to avoid identity rotation
        offset = rng.integers(1, n)
        rotated = np.roll(hscores, offset)

        perm_clusters = detect_fn(rotated, **detect_kwargs)
        perm_positions = set()
        for c in perm_clusters:
            perm_positions.update(c['positions'])

        null_values[i] = metric_fn(perm_positions, ground_truth_positions)

    null_mean = float(np.mean(null_values))
    null_std = float(np.std(null_values))
    # One-sided p-value: proportion of null >= observed
    p_value = float(np.mean(null_values >= observed))

    return {
        'observed': observed,
        'null_mean': null_mean,
        'null_std': null_std,
        'p_value': p_value,
        'null_dist': null_values,
    }
