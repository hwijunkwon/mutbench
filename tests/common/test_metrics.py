import numpy as np
from tools.common.metrics import adjusted_rand_index, normalized_mutual_info, f_measure_pairwise, cluster_score


def test_ari_perfect():
    true = [0, 0, 1, 1, 2, 2]
    pred = [0, 0, 1, 1, 2, 2]
    assert adjusted_rand_index(true, pred) == 1.0


def test_ari_random():
    true = [0, 0, 1, 1]
    pred = [0, 1, 0, 1]
    assert adjusted_rand_index(true, pred) < 0.1


def test_nmi_perfect():
    true = [0, 0, 1, 1, 2, 2]
    pred = [0, 0, 1, 1, 2, 2]
    assert normalized_mutual_info(true, pred) == 1.0


def test_f_measure_perfect():
    true = [0, 0, 1, 1, 2, 2]
    pred = [0, 0, 1, 1, 2, 2]
    assert f_measure_pairwise(true, pred) == 1.0


def test_cluster_score():
    true = [0, 0, 1, 1, 2, 2]
    pred = [0, 0, 1, 1, 2, 2]
    assert cluster_score(true, pred) == 1.0


def test_cluster_score_partial():
    true = [0, 0, 0, 1, 1, 1]
    pred = [0, 0, 1, 1, 1, 1]
    score = cluster_score(true, pred)
    assert 0.0 < score < 1.0
