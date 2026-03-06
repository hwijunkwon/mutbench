import numpy as np
from tools.mutbench.cross_pathogen.influenza import (
    get_antigenic_positions_nuc, analyze_influenza, HA_SEGMENT_LENGTH
)

def test_antigenic_positions():
    positions = get_antigenic_positions_nuc()
    assert len(positions) > 0
    assert all(0 <= p < HA_SEGMENT_LENGTH for p in positions)

def test_analyze_influenza_mock():
    np.random.seed(42)
    ref_len = 300  # short mock
    ref = ''.join(np.random.choice(['A','T','G','C'], ref_len))
    alignment = [
        ''.join(np.random.choice(['A','T','G','C'], ref_len))
        for _ in range(20)
    ]
    result = analyze_influenza(alignment, ref, gamma=10, d=3, minpts=3)
    assert 'hscores' in result
    assert 'n_clusters' in result
    assert 'clusters' in result
    assert len(result['hscores']) == ref_len
