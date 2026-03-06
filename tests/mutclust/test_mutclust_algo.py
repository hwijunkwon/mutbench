import numpy as np
from tools.mutclust.mutclust_algo.core import compute_deps, is_ccm, mutclust

def test_compute_deps():
    assert compute_deps(1.0, gamma=10) == 10
    assert compute_deps(0.5, gamma=10) == 5
    assert compute_deps(0.0, gamma=10) == 0

def test_ccm_conditions():
    hscores = np.zeros(100)
    hscores[45:55] = 0.1
    hscores[50] = 0.5
    assert is_ccm(50, hscores, gamma=10, minpts=5)

def test_ccm_fails_low_hscore():
    hscores = np.zeros(100)
    hscores[50] = 0.01
    assert not is_ccm(50, hscores, gamma=10, minpts=5)

def test_mutclust_finds_clusters():
    np.random.seed(42)
    hscores = np.zeros(1000)
    hscores[100:120] = np.random.uniform(0.1, 0.5, 20)
    hscores[110] = 1.0
    hscores[500:530] = np.random.uniform(0.1, 0.5, 30)
    hscores[515] = 1.2
    clusters = mutclust(hscores, gamma=10, d=3, minpts=5)
    assert len(clusters) >= 2
    positions = set()
    for c in clusters:
        positions.update(c.positions)
    assert 110 in positions
    assert 515 in positions

def test_mutclust_no_clusters_in_noise():
    hscores = np.random.uniform(0, 0.01, 500)
    clusters = mutclust(hscores, gamma=10, d=3, minpts=5)
    assert len(clusters) == 0

def test_expand_cluster_range_preserved():
    """Bug: cumulative subtraction causes premature cluster termination.
    A CCM with H=1.0 (deps=10) should expand ~7-10 positions, not 2-3."""
    hscores = np.zeros(100)
    hscores[40:60] = 0.1  # dense region
    hscores[50] = 1.0     # CCM seed
    from tools.mutclust.mutclust_algo.core import _expand_cluster
    cluster = _expand_cluster(50, hscores, gamma=10, d=3, minpts=5)
    # With H=1.0, deps_ccm=10, cluster should span at least 7 positions each direction
    assert cluster.size >= 10, f"Cluster too small: {cluster.size} (bug: premature termination)"
