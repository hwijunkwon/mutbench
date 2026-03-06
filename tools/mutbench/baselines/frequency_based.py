"""Frequency-based baseline for hotspot detection.

Flags positions whose mutation frequency (or hscore) exceeds the top
``threshold_pct`` percentile and groups consecutive hits into clusters.
"""

from __future__ import annotations

import math
from typing import Any

import numpy as np


def _group_positions(positions: list[int], gap: int = 2) -> list[dict[str, Any]]:
    """Group sorted positions into clusters with max *gap* between consecutive."""
    if not positions:
        return []
    clusters: list[dict[str, Any]] = []
    current = [positions[0]]
    for p in positions[1:]:
        if p - current[-1] <= gap:
            current.append(p)
        else:
            clusters.append(
                {"start": current[0], "end": current[-1], "positions": current}
            )
            current = [p]
    clusters.append({"start": current[0], "end": current[-1], "positions": current})
    return clusters


def detect_hotspots(
    scores: np.ndarray | list[float],
    *,
    threshold_pct: float = 10,
    gap: int = 2,
) -> list[dict[str, Any]]:
    """Detect hotspots by thresholding mutation frequencies / hscores.

    Parameters
    ----------
    scores:
        Array-like of per-position mutation scores.
    threshold_pct:
        Percentage of top-scoring positions to flag (default 10).
    gap:
        Maximum gap between consecutive flagged positions to merge
        them into a single cluster (default 2).

    Returns
    -------
    list[dict]
        Each dict has keys ``start``, ``end``, ``positions``.
    """
    arr = np.asarray(scores, dtype=float)
    if arr.size == 0:
        return []

    # Determine the threshold value from the top threshold_pct% of scores.
    sorted_vals = np.sort(arr)[::-1]
    n_top = max(1, int(math.ceil(len(sorted_vals) * threshold_pct / 100)))
    threshold = sorted_vals[min(n_top, len(sorted_vals)) - 1]

    # Flag positions at or above the threshold (but only if score > 0).
    flagged = [int(i) for i in np.where((arr >= threshold) & (arr > 0))[0]]

    return _group_positions(flagged, gap=gap)
