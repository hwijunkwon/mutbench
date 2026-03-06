"""Smoke tests for MutBench visualization module."""
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')
from matplotlib.figure import Figure
from tools.mutbench.visualization.plots import (
    plot_method_comparison, plot_genome_hotspot_map,
    plot_sensitivity_heatmap, plot_dnds_enrichment
)


def test_plot_method_comparison():
    df = pd.DataFrame({
        'method': ['MutClust', 'Entropy', 'Frequency'],
        'precision': [0.8, 0.6, 0.5],
        'recall': [0.7, 0.5, 0.6],
        'f1': [0.75, 0.55, 0.55],
    })
    fig = plot_method_comparison(df)
    assert isinstance(fig, Figure)


def test_plot_genome_hotspot_map():
    hscores = np.random.uniform(0, 0.1, 500)
    hscores[100:120] = 0.5
    detected = set(range(100, 120))
    gt = set(range(105, 125))
    fig = plot_genome_hotspot_map(hscores, detected, gt)
    assert isinstance(fig, Figure)


def test_plot_sensitivity_heatmap():
    rows = []
    for g in [5, 10, 15]:
        for d in [2, 3, 4]:
            for m in [3, 5]:
                rows.append({'gamma': g, 'd': d, 'minpts': m, 'f1': np.random.uniform(0.3, 0.8)})
    df = pd.DataFrame(rows)
    fig = plot_sensitivity_heatmap(df, metric='f1')
    assert isinstance(fig, Figure)


def test_plot_dnds_enrichment():
    clusters = [
        {'start': 100, 'end': 120, 'dnds': 2.5},
        {'start': 300, 'end': 330, 'dnds': 0.8},
        {'start': 500, 'end': 520, 'dnds': float('inf')},
    ]
    fig = plot_dnds_enrichment(clusters)
    assert isinstance(fig, Figure)
