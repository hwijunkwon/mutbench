import numpy as np
from tools.mutclust.hscore.core import (
    compute_nucleotide_ratios, compute_mutation_ratio,
    compute_mutation_entropy, compute_hscore, compute_hscores_from_counts,
)

def test_nucleotide_ratios():
    counts = {'A': 80, 'T': 10, 'G': 5, 'C': 5}
    ratios = compute_nucleotide_ratios(counts)
    assert abs(ratios['A'] - 0.8) < 1e-10
    assert abs(sum(ratios.values()) - 1.0) < 1e-10

def test_mutation_ratio_no_mutation():
    ratios = {'A': 1.0, 'T': 0.0, 'G': 0.0, 'C': 0.0}
    assert compute_mutation_ratio(ratios, ref='A') == 0.0

def test_mutation_ratio_all_mutated():
    ratios = {'A': 0.0, 'T': 0.5, 'G': 0.3, 'C': 0.2}
    assert abs(compute_mutation_ratio(ratios, ref='A') - 1.0) < 1e-10

def test_mutation_entropy_single_type():
    ratios = {'A': 0.0, 'T': 1.0, 'G': 0.0, 'C': 0.0}
    assert compute_mutation_entropy(ratios, ref='A') == 0.0

def test_mutation_entropy_diverse():
    ratios = {'A': 0.0, 'T': 0.5, 'G': 0.3, 'C': 0.2}
    E = compute_mutation_entropy(ratios, ref='A')
    assert E < 0

def test_hscore_formula():
    P, E = 0.5, -1.5
    H = compute_hscore(P, E)
    expected = np.log2(P * abs(E) * 100 + 1)
    assert abs(H - expected) < 1e-10

def test_hscore_zero_mutation():
    assert compute_hscore(0.0, 0.0) == 0.0

def test_full_pipeline():
    counts_per_position = [
        {'A': 70, 'T': 15, 'G': 10, 'C': 5},
        {'A': 5, 'T': 90, 'G': 3, 'C': 2},
        {'A': 25, 'T': 25, 'G': 25, 'C': 25},
    ]
    refs = ['A', 'T', 'A']
    hscores = compute_hscores_from_counts(counts_per_position, refs)
    assert len(hscores) == 3
    assert hscores[2] > hscores[1]
