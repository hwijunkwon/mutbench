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
