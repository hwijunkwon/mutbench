"""MutBench benchmark visualization module."""
import matplotlib
matplotlib.use('Agg')  # Non-interactive backend
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import pandas as pd


def plot_method_comparison(results_df: pd.DataFrame, output_path: str = None):
    """Bar chart comparing Precision/Recall/F1 per method.

    Args:
        results_df: DataFrame with columns 'method', 'precision', 'recall', 'f1'
        output_path: optional path to save figure
    Returns:
        matplotlib Figure
    """
    fig, ax = plt.subplots(figsize=(10, 6))
    metrics = ['precision', 'recall', 'f1']
    x = np.arange(len(results_df))
    width = 0.25
    for i, metric in enumerate(metrics):
        if metric in results_df.columns:
            ax.bar(x + i * width, results_df[metric], width, label=metric.capitalize())
    ax.set_xlabel('Method')
    ax.set_ylabel('Score')
    ax.set_title('Method Comparison: Precision / Recall / F1')
    ax.set_xticks(x + width)
    ax.set_xticklabels(results_df['method'], rotation=45, ha='right')
    ax.legend()
    ax.set_ylim(0, 1)
    plt.tight_layout()
    if output_path:
        fig.savefig(output_path, dpi=150, bbox_inches='tight')
    return fig


def plot_genome_hotspot_map(hscores, detected_positions: set, ground_truth_positions: set,
                             output_path: str = None):
    """Genome-wide hotspot map with detected vs ground truth overlay.

    Args:
        hscores: array of H-scores per position
        detected_positions: set of detected hotspot positions
        ground_truth_positions: set of ground truth positions
        output_path: optional path to save figure
    Returns:
        matplotlib Figure
    """
    fig, axes = plt.subplots(3, 1, figsize=(14, 8), sharex=True)
    positions = np.arange(len(hscores))

    # H-score profile
    axes[0].fill_between(positions, hscores, alpha=0.7)
    axes[0].set_ylabel('H-score')
    axes[0].set_title('Genome-wide Mutation Hotspot Map')

    # Detected hotspots
    det_mask = np.zeros(len(hscores))
    for p in detected_positions:
        if 0 <= p < len(hscores):
            det_mask[p] = 1
    axes[1].fill_between(positions, det_mask, alpha=0.7, color='red')
    axes[1].set_ylabel('Detected')
    axes[1].set_yticks([0, 1])

    # Ground truth
    gt_mask = np.zeros(len(hscores))
    for p in ground_truth_positions:
        if 0 <= p < len(hscores):
            gt_mask[p] = 1
    axes[2].fill_between(positions, gt_mask, alpha=0.7, color='green')
    axes[2].set_ylabel('Ground Truth')
    axes[2].set_xlabel('Genome Position')
    axes[2].set_yticks([0, 1])

    plt.tight_layout()
    if output_path:
        fig.savefig(output_path, dpi=150, bbox_inches='tight')
    return fig


def plot_sensitivity_heatmap(sweep_df: pd.DataFrame, metric: str = 'f1',
                              output_path: str = None):
    """Parameter sensitivity heatmap for gamma vs d (averaged over minpts).

    Args:
        sweep_df: DataFrame with columns 'gamma', 'd', 'minpts', and metric columns
        metric: which metric to plot (default 'f1')
        output_path: optional path to save figure
    Returns:
        matplotlib Figure
    """
    pivot = sweep_df.groupby(['gamma', 'd'])[metric].mean().reset_index()
    pivot_table = pivot.pivot(index='gamma', columns='d', values=metric)

    fig, ax = plt.subplots(figsize=(8, 6))
    sns.heatmap(pivot_table, annot=True, fmt='.3f', cmap='YlOrRd', ax=ax)
    ax.set_title(f'Parameter Sensitivity: {metric.upper()} (averaged over minpts)')
    ax.set_xlabel('d')
    ax.set_ylabel('gamma')
    plt.tight_layout()
    if output_path:
        fig.savefig(output_path, dpi=150, bbox_inches='tight')
    return fig


def plot_dnds_enrichment(cluster_data: list[dict], output_path: str = None):
    """dN/dS enrichment plot per cluster.

    Args:
        cluster_data: list of dicts with 'dnds' key and optionally 'start', 'end'
        output_path: optional path to save figure
    Returns:
        matplotlib Figure
    """
    fig, ax = plt.subplots(figsize=(10, 5))
    dnds_values = [c.get('dnds', 0) for c in cluster_data]
    finite_values = [v if np.isfinite(v) else 10.0 for v in dnds_values]  # cap inf
    labels = [f"{c.get('start', i)}-{c.get('end', i)}" for i, c in enumerate(cluster_data)]

    colors = ['red' if v > 1 else 'blue' for v in finite_values]
    ax.bar(range(len(finite_values)), finite_values, color=colors, alpha=0.7)
    ax.axhline(y=1.0, color='black', linestyle='--', label='Neutral (dN/dS=1)')
    ax.set_xlabel('Cluster')
    ax.set_ylabel('dN/dS')
    ax.set_title('dN/dS Enrichment per Cluster')
    ax.set_xticks(range(len(labels)))
    ax.set_xticklabels(labels, rotation=45, ha='right')
    ax.legend()
    plt.tight_layout()
    if output_path:
        fig.savefig(output_path, dpi=150, bbox_inches='tight')
    return fig


def plot_hotspot_score_comparison(results_df: pd.DataFrame, output_path: str = None):
    """Bar chart comparing hotspot-score components per method.

    Shows recall, precision, stability, and hotspot_score as grouped bars.
    Only plots methods that have non-NaN hotspot_score values.

    Args:
        results_df: DataFrame with columns 'method', 'recall', 'precision', 'stability', 'hotspot_score'
        output_path: optional path to save figure
    Returns:
        matplotlib Figure
    """
    # Filter to methods with valid hotspot scores
    df = results_df.dropna(subset=['hotspot_score']).copy()
    if df.empty:
        fig, ax = plt.subplots(figsize=(10, 6))
        ax.text(0.5, 0.5, 'No methods with hotspot scores', ha='center', va='center')
        if output_path:
            fig.savefig(output_path, dpi=150, bbox_inches='tight')
        return fig

    fig, ax = plt.subplots(figsize=(12, 6))
    metrics = ['recall', 'precision', 'stability', 'hotspot_score']
    colors = ['#2196F3', '#4CAF50', '#FF9800', '#E91E63']
    x = np.arange(len(df))
    width = 0.2

    for i, (metric, color) in enumerate(zip(metrics, colors)):
        if metric in df.columns:
            label = metric.replace('_', ' ').title()
            ax.bar(x + i * width, df[metric].values, width, label=label, color=color, alpha=0.8)

    ax.set_xlabel('Method')
    ax.set_ylabel('Score')
    ax.set_title('Hotspot Score Comparison (Recall + Precision + Stability) / 3')
    ax.set_xticks(x + 1.5 * width)
    ax.set_xticklabels(df['method'].values, rotation=45, ha='right')
    ax.legend()
    ax.set_ylim(0, 1)
    plt.tight_layout()
    if output_path:
        fig.savefig(output_path, dpi=150, bbox_inches='tight')
    return fig
