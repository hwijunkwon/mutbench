#!/usr/bin/env python3
"""Generate updated figures for 10-feature Information-Type Analysis.

Figures:
1. RF feature importance 3x3 grid (10 features, updated colors)
2. Feature correlation heatmap (mean across 9 pathogens)
3. Per-feature AUC heatmap (10 features x 9 pathogens)
"""

import os
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors

BASE = os.path.join(os.path.dirname(__file__), "..")
OUT_DIR = os.path.join(BASE, "results/mutbench")
FEAT_DIR = os.path.join(BASE, "results/mutbench/feature_analysis")
FIG_DIR = os.path.join(BASE, "paper/figure")
os.makedirs(FIG_DIR, exist_ok=True)

FEATURE_NAMES = [
    "freq", "entropy", "rare_freq", "homoplasy", "esm2_llr", "plddt",
    "sasa", "grantham", "dnds_proxy", "semantic_change"
]

FEATURE_LABELS = {
    "freq": "Frequency",
    "entropy": "Entropy",
    "rare_freq": "Rare variant",
    "homoplasy": "Homoplasy",
    "esm2_llr": "ESM-2 LLR",
    "plddt": "pLDDT",
    "sasa": "SASA (RSA)",
    "grantham": "Grantham",
    "dnds_proxy": "dN/dS proxy",
    "semantic_change": "Semantic Δ",
}

# Colors by category
FEATURE_COLORS = {
    "freq": "#4169E1",         # blue - frequency
    "entropy": "#6495ED",      # lighter blue - frequency
    "rare_freq": "#87CEEB",    # light blue - frequency
    "homoplasy": "#228B22",    # green - phylogeny
    "esm2_llr": "#8B008B",    # purple - deep learning
    "plddt": "#FF8C00",       # orange - structure
    "sasa": "#FFA500",        # amber - structure
    "grantham": "#DC143C",    # crimson - chemical
    "dnds_proxy": "#006400",  # dark green - evolutionary
    "semantic_change": "#9400D3",  # violet - deep learning
}

PATHOGEN_ORDER = [
    "SARS-CoV-2", "H3N2", "Norovirus", "HIV-1", "Dengue",
    "RSV", "Influenza_B", "MERS", "HCV", "Rabies", "EV-A71"
]

PATHOGEN_LABELS = {
    "SARS-CoV-2": "SARS-CoV-2",
    "H3N2": "H3N2",
    "Norovirus": "Norovirus",
    "HIV-1": "HIV-1",
    "Dengue": "Dengue",
    "RSV": "RSV",
    "Influenza_B": "Influenza B",
    "MERS": "MERS",
    "HCV": "HCV",
    "Rabies": "Rabies",
    "EV-A71": "EV-A71",
}


def plot_rf_importance_grid():
    """Plot 3x3 RF feature importance grid with 10 features."""
    imp_df = pd.read_csv(os.path.join(FEAT_DIR, "rf_importance_v2.csv"))
    cv_df = pd.read_csv(os.path.join(FEAT_DIR, "rf_cv_auc_v2.csv"))

    fig, axes = plt.subplots(3, 4, figsize=(18, 13))
    axes = axes.flatten()

    plotted = 0
    for pathogen in PATHOGEN_ORDER:
        if pathogen not in imp_df["pathogen"].values or pathogen not in cv_df["pathogen"].values:
            continue
        ax = axes[plotted]
        plotted += 1
        row = imp_df[imp_df["pathogen"] == pathogen].iloc[0]
        cv_row = cv_df[cv_df["pathogen"] == pathogen].iloc[0]
        cv_auc = cv_row["rf_cv_auc"]

        features = [f for f in FEATURE_NAMES if f in row.index and pd.notna(row[f])]
        values = [row[f] for f in features]
        colors = [FEATURE_COLORS[f] for f in features]
        labels = [FEATURE_LABELS[f] for f in features]

        # Sort by importance
        sorted_idx = np.argsort(values)[::-1]
        features_sorted = [features[i] for i in sorted_idx]
        values_sorted = [values[i] for i in sorted_idx]
        colors_sorted = [colors[i] for i in sorted_idx]
        labels_sorted = [labels[i] for i in sorted_idx]

        bars = ax.barh(range(len(features_sorted)), values_sorted, color=colors_sorted, edgecolor="white", linewidth=0.5)
        ax.set_yticks(range(len(features_sorted)))
        ax.set_yticklabels(labels_sorted, fontsize=8)
        ax.invert_yaxis()
        ax.set_xlabel("Importance", fontsize=9)
        ax.set_title(f"{PATHOGEN_LABELS[pathogen]} (CV AUC={cv_auc:.3f})", fontsize=11, fontweight="bold")
        ax.set_xlim(0, max(values_sorted) * 1.15)

        # Add value labels
        for bar, val in zip(bars, values_sorted):
            if val > 0.02:
                ax.text(bar.get_width() + 0.003, bar.get_y() + bar.get_height()/2,
                       f"{val:.3f}", va="center", fontsize=7)

    # Hide unused panels and use last one for legend
    for j in range(plotted, len(axes)-1):
        axes[j].axis('off')
    ax_legend = axes[len(axes)-1]
    ax_legend.axis('off')
    from matplotlib.patches import Patch
    legend_items = [
        Patch(facecolor="#4169E1", label="Frequency-based"),
        Patch(facecolor="#228B22", label="Phylogeny-based"),
        Patch(facecolor="#006400", label="Evolutionary rate"),
        Patch(facecolor="#8B008B", label="Deep learning"),
        Patch(facecolor="#FF8C00", label="Structure-based"),
        Patch(facecolor="#DC143C", label="Chemical property"),
    ]
    ax_legend.text(0.5, 0.5,
        'Bar colors indicate\nfeature category.\n\nBlue: Frequency\nGreen: Phylogeny\nPurple: Deep learning\nOrange: Structure\nRed: Chemical',
        transform=ax_legend.transAxes, ha='center', va='center',
        fontsize=10, color='#555555',
        bbox=dict(boxstyle='round,pad=0.5', facecolor='#F5F5F5', edgecolor='#CCCCCC'))

    plt.tight_layout()
    out_path = os.path.join(FIG_DIR, "feature_importance_grid.png")
    fig.savefig(out_path, dpi=300, bbox_inches="tight")
    plt.close()
    print(f"Saved: {out_path}")


def plot_feature_correlation_heatmap():
    """Plot mean feature correlation heatmap."""
    corr_df = pd.read_csv(os.path.join(FEAT_DIR, "feature_correlation_mean.csv"), index_col=0)

    # Reorder
    feat_order = [f for f in FEATURE_NAMES if f in corr_df.columns]
    corr_df = corr_df.loc[feat_order, feat_order]

    labels = [FEATURE_LABELS.get(f, f) for f in feat_order]

    fig, ax = plt.subplots(figsize=(10, 8))

    # Custom colormap
    cmap = plt.cm.RdBu_r
    norm = mcolors.TwoSlopeNorm(vmin=-0.3, vcenter=0, vmax=1.0)

    im = ax.imshow(corr_df.values, cmap=cmap, norm=norm, aspect="auto")

    ax.set_xticks(range(len(labels)))
    ax.set_yticks(range(len(labels)))
    ax.set_xticklabels(labels, rotation=45, ha="right", fontsize=10)
    ax.set_yticklabels(labels, fontsize=10)

    # Add correlation values
    for i in range(len(labels)):
        for j in range(len(labels)):
            val = corr_df.values[i, j]
            if not np.isnan(val):
                color = "white" if abs(val) > 0.6 else "black"
                ax.text(j, i, f"{val:.2f}", ha="center", va="center",
                       fontsize=8, color=color, fontweight="bold" if abs(val) > 0.5 else "normal")

    cbar = fig.colorbar(im, ax=ax, shrink=0.8, label="Spearman ρ")
    ax.set_title("Mean Feature Correlation Across 11 Pathogens", fontsize=13, fontweight="bold", pad=15)

    plt.tight_layout()
    out_path = os.path.join(FIG_DIR, "feature_correlation_heatmap.png")
    fig.savefig(out_path, dpi=300, bbox_inches="tight")
    plt.close()
    print(f"Saved: {out_path}")


def plot_auc_heatmap():
    """Plot per-feature AUC heatmap (9 pathogens × 10 features)."""
    pivot = pd.read_csv(os.path.join(FEAT_DIR, "per_feature_auc_11pathogens.csv"), index_col=0)
    feat_order = [f for f in FEATURE_NAMES if f in pivot.columns]
    pivot = pivot[feat_order]
    pivot = pivot.loc[[p for p in PATHOGEN_ORDER if p in pivot.index]]

    labels_x = [FEATURE_LABELS.get(f, f) for f in feat_order]
    labels_y = [PATHOGEN_LABELS.get(p, p) for p in pivot.index]

    fig, ax = plt.subplots(figsize=(12, 6))

    cmap = plt.cm.RdYlGn
    norm = mcolors.TwoSlopeNorm(vmin=0.15, vcenter=0.5, vmax=0.95)

    im = ax.imshow(pivot.values, cmap=cmap, norm=norm, aspect="auto")

    ax.set_xticks(range(len(labels_x)))
    ax.set_yticks(range(len(labels_y)))
    ax.set_xticklabels(labels_x, rotation=45, ha="right", fontsize=10)
    ax.set_yticklabels(labels_y, fontsize=10)

    # Add AUC values and bold the best per pathogen
    for i in range(pivot.shape[0]):
        best_j = pivot.values[i].argmax() if not np.all(np.isnan(pivot.values[i])) else -1
        for j in range(pivot.shape[1]):
            val = pivot.values[i, j]
            if not np.isnan(val):
                color = "white" if val > 0.8 or val < 0.3 else "black"
                weight = "bold" if j == best_j else "normal"
                ax.text(j, i, f"{val:.3f}", ha="center", va="center",
                       fontsize=8, color=color, fontweight=weight)

    cbar = fig.colorbar(im, ax=ax, shrink=0.8, label="AUC")
    n_path = pivot.shape[0]
    ax.set_title(f"Per-Feature AUC for Layer A Prediction (10 Features × {n_path} Pathogens)",
                fontsize=12, fontweight="bold", pad=15)

    plt.tight_layout()
    out_path = os.path.join(FIG_DIR, "feature_auc_heatmap.png")
    fig.savefig(out_path, dpi=300, bbox_inches="tight")
    plt.close()
    print(f"Saved: {out_path}")


if __name__ == "__main__":
    plot_rf_importance_grid()
    plot_feature_correlation_heatmap()
    plot_auc_heatmap()
    print("\nAll figures generated!")
