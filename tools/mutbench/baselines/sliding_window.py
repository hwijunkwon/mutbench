"""Sliding-window baseline for hotspot detection.

Computes the mean score inside a sliding window and flags windows that
exceed the top ``threshold_pct`` percentile.
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
    window_size: int = 20,
    threshold_pct: float = 10,
    gap: int = 2,
) -> list[dict[str, Any]]:
    """Detect hotspots using a sliding-window average.

    Parameters
    ----------
    scores:
        Array-like of per-position mutation scores.
    window_size:
        Number of positions in each sliding window (default 20).
    threshold_pct:
        Percentage of top-scoring windows to flag (default 10).
    gap:
        Maximum gap between consecutive flagged window start positions
        to merge them into a single cluster (default 2).

    Returns
    -------
    list[dict]
        Each dict has keys ``start``, ``end``, ``positions``.
    """
    arr = np.asarray(scores, dtype=float)
    n = len(arr)

    if n == 0 or window_size < 1:
        return []

    # Compute window averages using a cumulative sum for efficiency.
    effective_window = min(window_size, n)
    cumsum = np.concatenate(([0.0], np.cumsum(arr)))
    n_windows = n - effective_window + 1
    window_avgs = (cumsum[effective_window:] - cumsum[:n_windows]) / effective_window

    if len(window_avgs) == 0:
        return []

    # Determine the threshold value from the top threshold_pct% of window avgs.
    sorted_vals = np.sort(window_avgs)[::-1]
    n_top = max(1, int(math.ceil(len(sorted_vals) * threshold_pct / 100)))
    threshold = sorted_vals[min(n_top, len(sorted_vals)) - 1]

    # Flag windows at or above the threshold (but only if avg > 0).
    flagged_starts = [
        int(i) for i in np.where((window_avgs >= threshold) & (window_avgs > 0))[0]
    ]

    if not flagged_starts:
        return []

    # Expand each flagged window to its full set of positions, then merge.
    all_positions: set[int] = set()
    for start in flagged_starts:
        for pos in range(start, start + effective_window):
            all_positions.add(pos)

    return _group_positions(sorted(all_positions), gap=gap)
