"""Shannon entropy baseline for hotspot detection.

Computes per-position Shannon entropy over nucleotide counts and flags
positions with unusually high diversity as candidate hotspots.
"""

from __future__ import annotations

import math
from typing import Any


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


def _shannon_entropy(counts: dict[str, int]) -> float:
    """Compute Shannon entropy (bits) from a nucleotide count dictionary."""
    total = sum(counts.values())
    if total == 0:
        return 0.0
    entropy = 0.0
    for count in counts.values():
        if count > 0:
            p = count / total
            entropy -= p * math.log2(p)
    return entropy


def detect_hotspots(
    scores: list[dict[str, int]],
    *,
    threshold_pct: float = 10,
    gap: int = 2,
) -> list[dict[str, Any]]:
    """Detect hotspots using Shannon entropy over nucleotide counts.

    Parameters
    ----------
    scores:
        List of nucleotide count dicts per position, e.g.
        ``[{'A': 80, 'T': 10, 'G': 5, 'C': 5}, ...]``.
    threshold_pct:
        Percentage of top-entropy positions to flag (default 10).
    gap:
        Maximum gap between consecutive flagged positions to merge
        them into a single cluster (default 2).

    Returns
    -------
    list[dict]
        Each dict has keys ``start``, ``end``, ``positions``.
    """
    entropies = [_shannon_entropy(c) for c in scores]

    if not entropies:
        return []

    # Determine the threshold value from the top threshold_pct% of entropies.
    sorted_vals = sorted(entropies, reverse=True)
    n_top = max(1, int(math.ceil(len(sorted_vals) * threshold_pct / 100)))
    threshold = sorted_vals[min(n_top, len(sorted_vals)) - 1]

    # Flag positions at or above the threshold (but only if entropy > 0).
    flagged = [i for i, h in enumerate(entropies) if h >= threshold and h > 0]

    return _group_positions(flagged, gap=gap)
