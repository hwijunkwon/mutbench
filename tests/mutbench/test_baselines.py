"""Tests for baseline hotspot detection methods."""

import numpy as np

from tools.mutbench.baselines.shannon_entropy import detect_hotspots as entropy_detect
from tools.mutbench.baselines.frequency_based import detect_hotspots as freq_detect
from tools.mutbench.baselines.sliding_window import detect_hotspots as window_detect


def test_entropy_detects_hotspot():
    # Position 50 has diverse mutations = high entropy
    counts = [{"A": 100, "T": 0, "G": 0, "C": 0}] * 100
    counts[50] = {"A": 25, "T": 25, "G": 25, "C": 25}
    results = entropy_detect(counts, threshold_pct=5, gap=2)
    positions = set()
    for r in results:
        positions.update(r["positions"])
    assert 50 in positions


def test_frequency_detects_hotspot():
    hscores = np.zeros(100)
    hscores[40:50] = 0.5
    results = freq_detect(hscores, threshold_pct=15, gap=2)
    assert len(results) >= 1
    positions = set()
    for r in results:
        positions.update(r["positions"])
    assert 45 in positions


def test_sliding_window_detects_hotspot():
    hscores = np.zeros(200)
    hscores[80:100] = 1.0
    results = window_detect(hscores, window_size=20, threshold_pct=10)
    assert len(results) >= 1


def test_all_methods_return_correct_format():
    counts = [{"A": 90, "T": 5, "G": 3, "C": 2}] * 50
    hscores = np.random.uniform(0, 0.1, 50)
    hscores[25] = 1.0
    for detect_fn, args in [
        (entropy_detect, (counts,)),
        (freq_detect, (hscores,)),
        (window_detect, (hscores,)),
    ]:
        results = detect_fn(*args)
        for r in results:
            assert "start" in r
            assert "end" in r
            assert "positions" in r
