import numpy as np
from tools.mutclust.dnds_annotation.core import (
    classify_mutation, compute_cluster_dnds, annotate_clusters
)

def test_classify_synonymous():
    # GCT -> GCC = Ala -> Ala (synonymous)
    assert classify_mutation('GCT', 'GCC', codon_pos=2) == 'synonymous'

def test_classify_nonsynonymous():
    # GCT -> ACT = Ala -> Thr (nonsynonymous)
    assert classify_mutation('GCT', 'ACT', codon_pos=0) == 'nonsynonymous'

def test_cluster_dnds():
    syn_counts = 3
    nonsyn_counts = 12
    result = compute_cluster_dnds(nonsyn_counts, syn_counts, seq_length_codons=10)
    assert result > 1.0  # positive selection

def test_annotate_clusters():
    clusters = [{'start': 0, 'end': 8, 'positions': [0, 3, 6]}]
    reference_seq = 'GCTACTGCT'  # 3 codons
    mutations = {0: 'A', 3: 'G', 6: 'A'}
    result = annotate_clusters(clusters, reference_seq, mutations)
    assert 'dnds' in result[0]
    assert 'syn_count' in result[0]
    assert 'nonsyn_count' in result[0]
