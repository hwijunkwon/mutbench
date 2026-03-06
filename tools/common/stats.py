"""Statistical testing utilities: BH correction, bootstrap testing."""
import numpy as np


def benjamini_hochberg(pvalues: list[float]) -> list[float]:
    """Apply Benjamini-Hochberg FDR correction.

    Returns adjusted p-values in original order.
    """
    pvalues = np.asarray(pvalues)
    n = len(pvalues)
    sorted_idx = np.argsort(pvalues)
    sorted_pvals = pvalues[sorted_idx]

    adjusted = np.empty(n)
    adjusted[sorted_idx[-1]] = min(sorted_pvals[-1], 1.0)

    for i in range(n - 2, -1, -1):
        rank = i + 1
        raw = sorted_pvals[i] * n / rank
        adjusted[sorted_idx[i]] = min(raw, adjusted[sorted_idx[i + 1]], 1.0)

    return adjusted.tolist()


def bootstrap_test(observed: float, null_distribution: np.ndarray) -> float:
    """Compute bootstrap p-value: fraction of null >= observed."""
    null_distribution = np.asarray(null_distribution)
    return float(np.mean(null_distribution >= observed))
