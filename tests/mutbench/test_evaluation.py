import numpy as np
from tools.mutbench.evaluation.metrics import (
    precision, recall, f1_score, enrichment_ratio,
    dnds_enrichment, evaluate_method
)

def test_precision_perfect():
    assert precision({1, 2, 3}, {1, 2, 3}) == 1.0

def test_precision_partial():
    assert precision({1, 2, 3, 4}, {1, 2}) == 0.5

def test_precision_empty():
    assert precision(set(), {1, 2}) == 0.0

def test_recall_perfect():
    assert recall({1, 2, 3}, {1, 2, 3}) == 1.0

def test_recall_partial():
    assert recall({1}, {1, 2}) == 0.5

def test_f1_perfect():
    assert f1_score({1, 2, 3}, {1, 2, 3}) == 1.0

def test_f1_zero():
    assert f1_score({4, 5}, {1, 2}) == 0.0

def test_enrichment_above_random():
    detected = {1, 2, 3, 4, 5}
    gt = {1, 2, 3, 100, 200}
    ratio = enrichment_ratio(detected, gt, genome_length=1000)
    assert ratio > 1.0

def test_dnds_enrichment():
    vals = [1.5, 2.0, 3.0]
    assert abs(dnds_enrichment(vals) - 2.1667) < 0.01

def test_evaluate_method():
    clusters = [{'start': 0, 'end': 4, 'positions': [0, 1, 2, 3, 4]}]
    gt = {0, 1, 2, 10, 20}
    result = evaluate_method(clusters, gt, genome_length=100)
    assert 'precision' in result
    assert 'recall' in result
    assert 'f1' in result
    assert result['precision'] == 0.6
    assert result['recall'] == 0.6
