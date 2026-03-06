import numpy as np
from tools.mutbench.variants.registry import get_variant, list_variants

def test_v3_hdbscan_registered():
    assert 'v3-hdbscan' in list_variants()

def test_v3_hdbscan_detects_hotspots():
    np.random.seed(42)
    hscores = np.zeros(500)
    hscores[100:130] = np.random.uniform(0.1, 0.5, 30)
    hscores[115] = 1.0
    hscores[300:320] = np.random.uniform(0.1, 0.5, 20)
    hscores[310] = 0.8
    clusters = get_variant('v3-hdbscan')(hscores)
    assert len(clusters) >= 1
    all_pos = set()
    for c in clusters:
        all_pos.update(c['positions'])
        assert 'start' in c
        assert 'end' in c
    assert any(100 <= p <= 130 for p in all_pos)

def test_v3_hdbscan_no_clusters_in_noise():
    np.random.seed(99)
    hscores = np.zeros(500)
    # Scatter a few very low-amplitude positions (sparse noise, not a dense block)
    noise_positions = np.random.choice(500, size=15, replace=False)
    hscores[noise_positions] = np.random.uniform(0.001, 0.005, 15)
    clusters = get_variant('v3-hdbscan')(hscores)
    assert len(clusters) <= 2

def test_v3_hdbscan_params():
    np.random.seed(42)
    hscores = np.zeros(200)
    hscores[50:70] = 0.5
    clusters = get_variant('v3-hdbscan')(hscores, min_cluster_size=5, min_samples=3)
    assert isinstance(clusters, list)
