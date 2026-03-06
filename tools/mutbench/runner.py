"""MutBench benchmark runner — orchestrates the full evaluation pipeline."""
import numpy as np
import pandas as pd
from tools.mutbench.config import BenchmarkConfig
from tools.mutbench.evaluation.metrics import evaluate_method
from tools.mutbench.variants.registry import list_variants, get_variant
from tools.mutbench.baselines.shannon_entropy import detect_hotspots as entropy_detect
from tools.mutbench.baselines.frequency_based import detect_hotspots as freq_detect
from tools.mutbench.baselines.sliding_window import detect_hotspots as window_detect
from tools.mutbench.sensitivity.sweep import ParameterSweep


def get_all_methods():
    """Return dict of method_name -> detect_fn for all methods."""
    methods = {}
    for name in list_variants():
        methods[name] = get_variant(name)
    methods['entropy'] = lambda hscores, **kw: entropy_detect(
        [{'A': 0, 'T': 0, 'G': 0, 'C': 0}] * len(hscores), **kw
    )
    methods['frequency'] = lambda hscores, **kw: freq_detect(hscores, **kw)
    methods['sliding_window'] = lambda hscores, **kw: window_detect(hscores, **kw)
    return methods


def run_benchmark(hscores, ground_truth_positions: set, genome_length: int,
                   config: BenchmarkConfig = None,
                   counts_per_position: list = None) -> dict:
    """Run the full benchmark pipeline.

    Args:
        hscores: array of H-scores per position
        ground_truth_positions: set of known functional positions
        genome_length: total genome length
        config: benchmark configuration
        counts_per_position: nucleotide counts per position (for entropy baseline)

    Returns:
        dict with 'method_results', 'sensitivity_results' keys
    """
    if config is None:
        config = BenchmarkConfig()

    hscores = np.asarray(hscores, dtype=float)

    # Run all MutClust variants
    method_results = []
    for name in list_variants():
        detect_fn = get_variant(name)
        clusters = detect_fn(hscores, gamma=config.gamma, d=config.d, minpts=config.minpts)
        metrics = evaluate_method(clusters, ground_truth_positions, genome_length)
        metrics['method'] = name
        method_results.append(metrics)

    # Run baselines
    # Frequency-based
    freq_clusters = freq_detect(hscores, threshold_pct=10, gap=2)
    freq_metrics = evaluate_method(freq_clusters, ground_truth_positions, genome_length)
    freq_metrics['method'] = 'frequency'
    method_results.append(freq_metrics)

    # Sliding window
    sw_clusters = window_detect(hscores, window_size=20, threshold_pct=10, gap=2)
    sw_metrics = evaluate_method(sw_clusters, ground_truth_positions, genome_length)
    sw_metrics['method'] = 'sliding_window'
    method_results.append(sw_metrics)

    # Entropy baseline (only if counts provided)
    if counts_per_position is not None:
        ent_clusters = entropy_detect(counts_per_position, threshold_pct=10, gap=2)
        ent_metrics = evaluate_method(ent_clusters, ground_truth_positions, genome_length)
        ent_metrics['method'] = 'entropy'
        method_results.append(ent_metrics)

    # Parameter sensitivity
    sweep = ParameterSweep()
    sensitivity_results = sweep.run(
        hscores,
        lambda clusters: evaluate_method(clusters, ground_truth_positions, genome_length)
    )

    return {
        'method_results': pd.DataFrame(method_results),
        'sensitivity_results': pd.DataFrame(sensitivity_results),
    }
