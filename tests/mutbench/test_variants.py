import numpy as np
from tools.mutbench.variants.registry import list_variants, get_variant, VARIANTS

def test_all_variants_registered():
    variants = list_variants()
    assert 'v1-original' in variants
    assert 'v2a-bugfix' in variants
    assert 'v2b-bugfix+dnds' in variants
    assert 'v2c-full' in variants

def test_variants_return_correct_format():
    np.random.seed(42)
    hscores = np.zeros(1000)
    hscores[100:120] = np.random.uniform(0.1, 0.5, 20)
    hscores[110] = 1.0
    for name in list_variants():
        detect_fn = get_variant(name)
        results = detect_fn(hscores)
        for r in results:
            assert 'start' in r
            assert 'end' in r
            assert 'positions' in r

def test_v2a_detects_more_than_v1():
    """Bugfix should detect more positions due to expanded cluster range."""
    np.random.seed(42)
    hscores = np.zeros(1000)
    hscores[100:120] = np.random.uniform(0.1, 0.5, 20)
    hscores[110] = 1.0
    v1_results = get_variant('v1-original')(hscores)
    v2a_results = get_variant('v2a-bugfix')(hscores)
    v1_positions = sum(len(r['positions']) for r in v1_results)
    v2a_positions = sum(len(r['positions']) for r in v2a_results)
    assert v2a_positions >= v1_positions

def test_v2b_filters_by_dnds():
    """v2b should return fewer or equal clusters compared to v2a (filters neutral)."""
    np.random.seed(42)
    hscores = np.zeros(500)
    hscores[100:130] = np.random.uniform(0.1, 0.5, 30)
    hscores[115] = 1.0
    v2a = get_variant('v2a-bugfix')(hscores, gamma=10, d=3, minpts=5)
    v2b = get_variant('v2b-bugfix+dnds')(hscores, gamma=10, d=3, minpts=5,
                                          reference_seq='A' * 500,
                                          mutations={115: 'T', 116: 'T'})
    assert len(v2b) <= len(v2a)
