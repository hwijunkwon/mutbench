import numpy as np
import pandas as pd
from tools.mutbench.runner import run_benchmark
from tools.mutbench.config import BenchmarkConfig


def test_run_benchmark_mock():
    np.random.seed(42)
    genome_length = 500
    hscores = np.zeros(genome_length)
    # Create two hotspot regions
    hscores[100:120] = np.random.uniform(0.1, 0.5, 20)
    hscores[110] = 1.0
    hscores[300:320] = np.random.uniform(0.1, 0.5, 20)
    hscores[310] = 0.8

    # Ground truth: positions 100-119 and 300-319
    gt = set(range(100, 120)) | set(range(300, 320))

    config = BenchmarkConfig(seed=42)
    results = run_benchmark(hscores, gt, genome_length, config=config)

    assert 'method_results' in results
    assert 'sensitivity_results' in results
    assert isinstance(results['method_results'], pd.DataFrame)
    assert isinstance(results['sensitivity_results'], pd.DataFrame)
    assert len(results['method_results']) >= 3  # at least variants + baselines
    assert 'method' in results['method_results'].columns
    assert 'f1' in results['method_results'].columns


def test_run_benchmark_with_counts():
    np.random.seed(42)
    genome_length = 100
    hscores = np.zeros(genome_length)
    hscores[40:50] = 0.5
    gt = set(range(40, 50))

    counts = [{'A': 90, 'T': 5, 'G': 3, 'C': 2}] * genome_length
    for i in range(40, 50):
        counts[i] = {'A': 25, 'T': 25, 'G': 25, 'C': 25}

    config = BenchmarkConfig(seed=42)
    results = run_benchmark(hscores, gt, genome_length, config=config,
                             counts_per_position=counts)

    methods = results['method_results']['method'].tolist()
    assert 'entropy' in methods
