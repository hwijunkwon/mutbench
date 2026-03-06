"""Full integration test for MutBench pipeline.

End-to-end: mock DMS data → ground truth labels → run all methods → evaluate → results.
"""
import numpy as np
import pandas as pd
from tools.mutbench.config import BenchmarkConfig
from tools.mutbench.ground_truth.dms_loader import dms_to_position_scores, get_functional_positions
from tools.mutbench.ground_truth.coord_mapper import CoordinateMapper
from tools.mutbench.ground_truth.labeler import create_ground_truth_labels, GroundTruthSource
from tools.mutbench.runner import run_benchmark
from tools.mutbench.evaluation.metrics import evaluate_method
from tools.mutbench.variants.registry import get_variant
from tools.mutclust.dnds_annotation.core import annotate_clusters


def _make_synthetic_spike_data():
    """Create synthetic data mimicking SARS-CoV-2 Spike gene."""
    np.random.seed(42)
    gene_length_nt = 3822  # Spike gene ~1274 AA * 3
    genome_length = gene_length_nt

    # Generate H-scores: mostly low, with hotspots at known functional regions
    hscores = np.random.uniform(0, 0.02, genome_length)

    # RBD region (AA 319-541 → nt 954-1623): elevated H-scores
    rbd_start = (319 - 1) * 3
    rbd_end = 541 * 3
    hscores[rbd_start:rbd_end] = np.random.uniform(0.05, 0.3, rbd_end - rbd_start)
    # Add CCM seeds in RBD
    for pos in [484 * 3, 501 * 3, 417 * 3]:
        if pos < genome_length:
            hscores[pos] = 1.0

    # Furin cleavage site (AA 681-685 → nt 2040-2055): elevated
    furin_start = (681 - 1) * 3
    furin_end = 685 * 3
    hscores[furin_start:furin_end] = np.random.uniform(0.1, 0.5, furin_end - furin_start)
    hscores[(681 - 1) * 3] = 0.8

    # DMS-like data
    dms_data = []
    for aa in range(1, 1275):
        for mut in ['A', 'R', 'N']:
            if 319 <= aa <= 541:
                fitness = np.random.uniform(-2.0, -0.3)
            elif 681 <= aa <= 685:
                fitness = np.random.uniform(-1.5, -0.5)
            else:
                fitness = np.random.uniform(-0.1, 0.1)
            dms_data.append({'gene': 'S', 'aa_site': aa, 'mutant_aa': mut, 'fitness': fitness})

    dms_df = pd.DataFrame(dms_data)
    return hscores, dms_df, genome_length


def test_full_pipeline():
    """End-to-end integration test."""
    hscores, dms_df, genome_length = _make_synthetic_spike_data()

    # Step 1: Generate ground truth from DMS
    scores = dms_to_position_scores(dms_df, gene='S')
    functional_aa = get_functional_positions(scores, threshold_percentile=80)

    # Step 2: Map to nucleotide positions
    mapper = CoordinateMapper(gene_start=0, gene_end=genome_length - 1)
    functional_nuc = mapper.aa_set_to_nuc_set(functional_aa)

    # Step 3: Create binary labels
    labels = create_ground_truth_labels(genome_length, functional_nuc)
    assert sum(labels) > 0, "Ground truth should have functional positions"

    # Step 4: Run benchmark
    config = BenchmarkConfig(seed=42)
    results = run_benchmark(hscores, functional_nuc, genome_length, config=config)

    method_df = results['method_results']
    sensitivity_df = results['sensitivity_results']

    # Verify results structure
    assert len(method_df) >= 3
    assert 'precision' in method_df.columns
    assert 'recall' in method_df.columns
    assert 'f1' in method_df.columns
    assert len(sensitivity_df) == 64  # 4 * 4 * 4 parameter combos

    # Step 5: Verify MutClust v2a detects more than v1
    v1_row = method_df[method_df['method'] == 'v1-original']
    v2a_row = method_df[method_df['method'] == 'v2a-bugfix']
    assert len(v1_row) == 1
    assert len(v2a_row) == 1
    assert v2a_row['n_detected'].values[0] >= v1_row['n_detected'].values[0]

    # Step 6: Test dN/dS annotation on detected clusters
    v2a_clusters = get_variant('v2a-bugfix')(hscores, gamma=config.gamma, d=config.d, minpts=config.minpts)
    # Create mock mutations for dN/dS test
    reference_seq = 'A' * genome_length
    mutations = {}
    for c in v2a_clusters:
        for pos in c['positions'][:3]:
            mutations[pos] = 'T'
    if v2a_clusters:
        annotated = annotate_clusters(v2a_clusters, reference_seq, mutations)
        assert 'dnds' in annotated[0]


def test_enrichment_above_random():
    """All methods should detect functional positions better than random."""
    hscores, dms_df, genome_length = _make_synthetic_spike_data()
    scores = dms_to_position_scores(dms_df, gene='S')
    functional_aa = get_functional_positions(scores, threshold_percentile=80)
    mapper = CoordinateMapper(gene_start=0, gene_end=genome_length - 1)
    functional_nuc = mapper.aa_set_to_nuc_set(functional_aa)

    config = BenchmarkConfig(seed=42)
    results = run_benchmark(hscores, functional_nuc, genome_length, config=config)

    method_df = results['method_results']
    for _, row in method_df.iterrows():
        if row['n_detected'] > 0:
            assert row['enrichment_ratio'] >= 1.0, (
                f"Method {row['method']} has enrichment {row['enrichment_ratio']} < 1.0"
            )
