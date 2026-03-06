"""Tests for the real-DMS-data benchmark pipeline.

Verifies the end-to-end flow from mock DMS data through ground truth
derivation, coordinate mapping, and the full benchmark runner, as well
as the ``--mode`` argument plumbing in ``scripts/run_benchmark.py``.
"""
import importlib.util
import os
import numpy as np
import pandas as pd
import pytest

from tools.mutbench.ground_truth.dms_loader import (
    dms_to_position_scores,
    get_functional_positions,
)
from tools.mutbench.ground_truth.coord_mapper import CoordinateMapper
from tools.mutbench.runner import run_benchmark
from tools.mutbench.config import BenchmarkConfig
from tools.mutbench.evaluation.metrics import hotspot_score, compute_stability


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _make_mock_dms_dataframe(n_sites=100, seed=42):
    """Create a mock DMS DataFrame mimicking Bloom lab format.

    Positions 30-50 are given large negative fitness effects so they
    should be identified as functional by ``get_functional_positions``.
    """
    rng = np.random.default_rng(seed)
    rows = []
    for aa_site in range(1, n_sites + 1):
        for mut in ['A', 'V', 'L']:
            if 30 <= aa_site <= 50:
                fitness = rng.uniform(-2.0, -0.5)
            else:
                fitness = rng.uniform(-0.1, 0.1)
            rows.append({
                'gene': 'S',
                'aa_site': aa_site,
                'mutant': mut,
                'fitness': fitness,
            })
    return pd.DataFrame(rows)


# ---------------------------------------------------------------------------
# Tests
# ---------------------------------------------------------------------------

def test_dms_pipeline_with_mock():
    """DMS -> ground truth -> benchmark pipeline works end-to-end."""
    df = _make_mock_dms_dataframe()

    # Step 1: derive per-position fitness scores
    scores = dms_to_position_scores(df, gene='S')
    assert len(scores) == 100

    # Step 2: identify functional positions
    functional_aa = get_functional_positions(scores, threshold_percentile=80)
    assert len(functional_aa) > 0
    # Most of positions 30-50 should be in the functional set
    overlap = functional_aa & set(range(30, 51))
    assert len(overlap) > 5, (
        f"Expected most of 30-50 to be functional, got overlap {len(overlap)}"
    )

    # Step 3: map AA positions to nucleotide coordinates
    mapper = CoordinateMapper(gene_start=0, gene_end=300)
    functional_nuc = mapper.aa_set_to_nuc_set(functional_aa)
    assert len(functional_nuc) > 0
    # Each AA maps to 3 nucleotides
    assert len(functional_nuc) == len(functional_aa) * 3

    # Step 4: build H-scores with signal at functional positions
    genome_length = 300
    rng = np.random.default_rng(99)
    hscores = np.full(genome_length, 0.005)
    for nuc_pos in functional_nuc:
        if 0 <= nuc_pos < genome_length:
            hscores[nuc_pos] = rng.uniform(0.1, 0.5)
    # Add a couple of strong CCM seeds
    for aa in [35, 45]:
        nuc = aa * 3
        if nuc < genome_length:
            hscores[nuc] = 1.0

    # Step 5: run benchmark
    gt = {p for p in functional_nuc if 0 <= p < genome_length}
    config = BenchmarkConfig(seed=42)
    results = run_benchmark(hscores, gt, genome_length, config=config)

    assert 'method_results' in results
    method_df = results['method_results']
    assert 'v3-hdbscan' in method_df['method'].values
    assert 'v2a-bugfix' in method_df['method'].values

    # All methods with detections should achieve above-random enrichment
    for _, row in method_df.iterrows():
        if row['n_detected'] > 0:
            assert row['enrichment_ratio'] >= 1.0, (
                f"{row['method']} enrichment {row['enrichment_ratio']:.3f} < 1"
            )


def test_compute_extended_metrics():
    """compute_extended_metrics adds stability and hotspot_score columns."""
    # We import the function from the script module dynamically so we
    # do not need to make it a package.
    script_path = os.path.join(
        os.path.dirname(__file__), '..', '..', 'scripts', 'run_benchmark.py',
    )
    spec = importlib.util.spec_from_file_location('run_benchmark', script_path)
    mod = importlib.util.module_from_spec(spec)
    # Patch sys.argv so argparse inside the module does not choke
    import sys
    orig_argv = sys.argv
    sys.argv = ['run_benchmark.py']
    try:
        spec.loader.exec_module(mod)
    finally:
        sys.argv = orig_argv

    # Build a small toy benchmark result
    genome_length = 300
    rng = np.random.default_rng(42)
    hscores = np.full(genome_length, 0.005)
    for pos in range(90, 150):
        hscores[pos] = rng.uniform(0.1, 0.5)
    hscores[105] = 1.0
    hscores[135] = 1.0
    gt = set(range(90, 150))

    config = BenchmarkConfig(seed=42)
    results = run_benchmark(hscores, gt, genome_length, config=config)
    method_df = results['method_results']

    extended = mod.compute_extended_metrics(method_df, hscores, gt, genome_length)

    assert 'stability' in extended.columns
    assert 'hotspot_score' in extended.columns
    # Registered variants should have numeric values
    v2a = extended[extended['method'] == 'v2a-bugfix']
    assert len(v2a) == 1
    assert not np.isnan(v2a['stability'].values[0])
    assert not np.isnan(v2a['hotspot_score'].values[0])
    # Baselines should have NaN
    freq = extended[extended['method'] == 'frequency']
    if len(freq) > 0:
        assert np.isnan(freq['stability'].values[0])


def test_dms_mode_flag():
    """Verify the --mode flag logic exists and the module loads cleanly."""
    script_path = os.path.join(
        os.path.dirname(__file__), '..', '..', 'scripts', 'run_benchmark.py',
    )
    spec = importlib.util.spec_from_file_location('run_benchmark', script_path)
    assert spec is not None

    mod = importlib.util.module_from_spec(spec)
    import sys
    orig_argv = sys.argv
    sys.argv = ['run_benchmark.py']
    try:
        spec.loader.exec_module(mod)
    finally:
        sys.argv = orig_argv

    # Module should expose the key functions
    assert hasattr(mod, 'run_dms_benchmark')
    assert hasattr(mod, 'compute_extended_metrics')
    assert hasattr(mod, 'main')
    assert callable(mod.run_dms_benchmark)
    assert callable(mod.compute_extended_metrics)


def test_hotspot_score_in_extended_metrics():
    """Hotspot-score is the mean of recall, precision, and stability."""
    # Directly verify the arithmetic
    r, p, s = 0.6, 0.8, 0.7
    expected = (r + p + s) / 3
    assert abs(hotspot_score(r, p, s) - expected) < 1e-9
