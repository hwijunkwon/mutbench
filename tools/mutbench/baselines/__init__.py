"""Baseline hotspot detection methods for MutBench."""

from tools.mutbench.baselines.shannon_entropy import (
    detect_hotspots as entropy_detect,
)
from tools.mutbench.baselines.frequency_based import (
    detect_hotspots as frequency_detect,
)
from tools.mutbench.baselines.sliding_window import (
    detect_hotspots as window_detect,
)

__all__ = ["entropy_detect", "frequency_detect", "window_detect"]
