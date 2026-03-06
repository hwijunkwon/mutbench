import numpy as np
from tools.mutbench.evaluation.metrics import hotspot_score, compute_stability
from tools.mutbench.variants.registry import get_variant

def test_hotspot_score():
    score = hotspot_score(
        recall_known=0.8,
        precision_simulated=0.9,
        stability=0.7,
    )
    assert abs(score - 0.8) < 1e-10

def test_hotspot_score_perfect():
    assert hotspot_score(1.0, 1.0, 1.0) == 1.0

def test_hotspot_score_zero():
    assert hotspot_score(0.0, 0.0, 0.0) == 0.0

def test_stability_score():
    np.random.seed(42)
    hscores = np.zeros(500)
    hscores[100:120] = 0.5
    detect_fn = get_variant('v2a-bugfix')
    stability = compute_stability(hscores, detect_fn, n_iter=10, subsample_frac=0.8, seed=42)
    assert 0.0 <= stability <= 1.0

def test_stability_deterministic():
    np.random.seed(42)
    hscores = np.zeros(300)
    hscores[50:70] = 0.5
    detect_fn = get_variant('v2a-bugfix')
    s1 = compute_stability(hscores, detect_fn, n_iter=10, subsample_frac=0.8, seed=42)
    s2 = compute_stability(hscores, detect_fn, n_iter=10, subsample_frac=0.8, seed=42)
    assert s1 == s2
