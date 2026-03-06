import numpy as np
from tools.mutclust.hla_affinity.core import generate_epitopes, compute_log_fold_change

def test_generate_epitopes():
    seq = "ACDEFGHIKLMNPQRSTVWY"
    epitopes = generate_epitopes(seq, min_len=8, max_len=9)
    assert len(epitopes) > 0
    assert all(8 <= len(e) <= 9 for e in epitopes)

def test_generate_epitopes_short():
    seq = "ACD"
    epitopes = generate_epitopes(seq, min_len=8, max_len=9)
    assert len(epitopes) == 0

def test_log_fold_change():
    lfc = compute_log_fold_change(100.0, 200.0)
    assert abs(lfc - 1.0) < 1e-10

def test_log_fold_change_decreased():
    lfc = compute_log_fold_change(100.0, 50.0)
    assert lfc < 0
