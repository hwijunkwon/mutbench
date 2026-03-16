#!/usr/bin/env python3
"""Generate publication-quality figures for MutBench manuscript (9-pathogen version).

Follows figure_guidelines.md:
- Individual generation per figure
- Min font 7pt, axis labels 9pt+, titles 10pt+
- No overlapping components
- 300 DPI PNG
- Consistent color palette
"""

import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import warnings
warnings.filterwarnings('ignore')

plt.rcParams.update({
    'font.size': 10,
    'font.family': 'sans-serif',
    'axes.linewidth': 0.8,
    'axes.spines.top': False,
    'axes.spines.right': False,
    'figure.dpi': 300,
    'savefig.dpi': 300,
    'savefig.bbox': 'tight',
    'savefig.pad_inches': 0.1,
})

DATA_DIR = '/proj/paper/results/mutbench'
FIG_DIR = '/proj/paper/paper/figure'

# Consistent colors (from guidelines)
C_SCORING = '#4C72B0'
C_DETECTION = '#55A868'
C_INTERACTION = '#C44E52'
C_RESIDUAL = '#8C8C8C'

PATHOGEN_ORDER = [
    'SARS-CoV-2', 'H3N2', 'Norovirus', 'HIV-1',
    'Dengue', 'RSV', 'Influenza_B', 'MERS', 'HCV'
]

PATHOGEN_SHORT = {
    'SARS-CoV-2': 'SARS-2',
    'H3N2': 'H3N2',
    'Norovirus': 'Noro',
    'HIV-1': 'HIV-1',
    'Dengue': 'Dengue',
    'RSV': 'RSV',
    'Influenza_B': 'Flu-B',
    'MERS': 'MERS',
    'HCV': 'HCV',
}


def load_9pathogen():
    return pd.read_csv(f'{DATA_DIR}/extended_9pathogen_results.csv')


def fig1_scoring_detection_heatmap():
    """Figure 1: Scoring x Detection family heatmap (9 pathogens)."""
    df = load_9pathogen()

    pivot = df.groupby(['score', 'family'])['mcc'].mean().reset_index()
    heatmap_data = pivot.pivot(index='score', columns='family', values='mcc')

    # Order scoring formulas by mean MCC (descending)
    score_means = heatmap_data.mean(axis=1).sort_values(ascending=False)
    score_order = score_means.index.tolist()

    # Order detection families by mean MCC (descending)
    family_means = heatmap_data.mean(axis=0).sort_values(ascending=False)
    family_order = family_means.index.tolist()

    heatmap_data = heatmap_data.reindex(index=score_order, columns=family_order)

    fig, ax = plt.subplots(figsize=(8, 3.8))
    vmax = max(abs(heatmap_data.values[~np.isnan(heatmap_data.values)].min()),
               abs(heatmap_data.values[~np.isnan(heatmap_data.values)].max()))

    im = ax.imshow(heatmap_data.values, cmap='RdBu_r', aspect='auto',
                   vmin=-vmax, vmax=vmax)

    for i in range(heatmap_data.shape[0]):
        for j in range(heatmap_data.shape[1]):
            val = heatmap_data.values[i, j]
            if not np.isnan(val):
                color = 'white' if abs(val) > vmax * 0.6 else 'black'
                ax.text(j, i, f'{val:.2f}', ha='center', va='center',
                       fontsize=6, color=color)

    # Score labels with display names
    score_labels = [s.replace('E*rare', r'E$\times$rare')
                    .replace('P*E*rare', r'P$\times$E$\times$rare')
                    .replace('P*E^2', r'P$\times$E$^2$')
                    .replace('P*E', r'P$\times$E')
                    .replace('P*minority_E', r'P$\times$min_E')
                    for s in score_order]

    ax.set_xticks(np.arange(len(family_order)))
    ax.set_xticklabels(family_order, fontsize=7.5, rotation=40, ha='right')
    ax.set_yticks(np.arange(len(score_order)))
    ax.set_yticklabels(score_labels, fontsize=8)
    ax.set_xlabel('Detection family', fontsize=10)
    ax.set_ylabel('Scoring formula', fontsize=10)

    cbar = plt.colorbar(im, ax=ax, shrink=0.8, pad=0.02)
    cbar.set_label('Mean MCC (9 pathogens)', fontsize=9)
    cbar.ax.tick_params(labelsize=8)

    plt.tight_layout()
    fig.savefig(f'{FIG_DIR}/scoring_detection_heatmap.png')
    plt.close(fig)
    print('Saved Fig 1: scoring_detection_heatmap.png')


def fig2_cross_pathogen_top5():
    """Figure 2: Per-pathogen MCC for top 5 cross-pathogen combinations."""
    df = load_9pathogen()

    # Find top 5 by cross-pathogen mean MCC
    combo_means = df.groupby(['score', 'detector'])['mcc'].mean().reset_index()
    combo_means = combo_means.sort_values('mcc', ascending=False).head(5)

    combos = []
    for _, row in combo_means.iterrows():
        label = row['score'].replace('E*rare', r'E$\times$rare') + '\n+ ' + row['detector']
        combos.append((row['score'], row['detector'], label))

    colors = ['#4C72B0', '#DD8452', '#55A868', '#C44E52', '#8172B3']

    # Legend labels
    legend_labels = []
    for score, detector, _ in combos:
        s = score.replace('E*rare', r'E$\times$rare').replace('P*E', r'P$\times$E')
        legend_labels.append(f'{s} + {detector}')

    fig, axes = plt.subplots(3, 3, figsize=(10, 7))
    axes = axes.flatten()

    for idx, pathogen in enumerate(PATHOGEN_ORDER):
        ax = axes[idx]
        mcc_vals = []
        for score, detector, label in combos:
            row = df[(df['pathogen'] == pathogen) & (df['score'] == score) &
                     (df['detector'] == detector)]
            mcc_vals.append(row['mcc'].values[0] if len(row) > 0 else 0)

        y_pos = np.arange(len(combos))
        bars = ax.barh(y_pos, mcc_vals, height=0.6, color=colors,
                       edgecolor='white', linewidth=0.5)

        for j, (bar, val) in enumerate(zip(bars, mcc_vals)):
            x_text = max(val + 0.01, 0.01)
            ax.text(x_text, j, f'{val:.3f}', va='center', fontsize=7)

        ax.set_xlim(-0.25, 0.75)
        ax.set_title(pathogen, fontsize=9, fontweight='bold')
        ax.axvline(x=0, color='black', linewidth=0.5, linestyle='-')
        ax.set_yticks([])

        if idx >= 6:
            ax.set_xlabel('MCC', fontsize=9)

    # Shared legend at bottom
    from matplotlib.patches import Patch
    legend_patches = [Patch(facecolor=colors[i], label=legend_labels[i])
                      for i in range(len(combos))]
    fig.legend(handles=legend_patches, loc='lower center',
               ncol=3, fontsize=7.5, frameon=False,
               bbox_to_anchor=(0.5, -0.02))

    plt.tight_layout(rect=[0, 0.06, 1, 1])
    fig.savefig(f'{FIG_DIR}/cross_pathogen_comparison.png')
    plt.close(fig)
    print('Saved Fig 2: cross_pathogen_comparison.png')


def fig3_scoring_comparison():
    """Figure 3: Scoring formula comparison across 9 pathogens."""
    df = load_9pathogen()

    # Best detection per scoring-pathogen pair
    best_per = df.groupby(['pathogen', 'score'])['mcc'].max().reset_index()
    pivot = best_per.pivot(index='score', columns='pathogen', values='mcc')
    pivot = pivot[PATHOGEN_ORDER]

    # Order by mean MCC
    pivot['mean'] = pivot.mean(axis=1)
    pivot = pivot.sort_values('mean', ascending=False)

    scores = pivot.index.tolist()
    score_labels = [s.replace('E*rare', r'E$\times$rare')
                    .replace('P*E*rare', r'P$\times$E$\times$rare')
                    .replace('P*E^2', r'P$\times$E$^2$')
                    .replace('P*E', r'P$\times$E')
                    .replace('P*minority_E', r'P$\times$min_E')
                    for s in scores]

    n_scores = len(scores)
    n_pathogens = len(PATHOGEN_ORDER)

    # Color palette for 9 pathogens
    pathogen_colors = ['#4C72B0', '#DD8452', '#55A868', '#C44E52', '#8172B3',
                       '#937860', '#DA8BC3', '#8C8C8C', '#CCB974']

    fig, ax = plt.subplots(figsize=(10, 4.5))

    bar_width = 0.08
    group_width = n_pathogens * bar_width
    x = np.arange(n_scores)

    for pi, pathogen in enumerate(PATHOGEN_ORDER):
        offset = (pi - n_pathogens/2 + 0.5) * bar_width
        vals = [pivot.loc[s, pathogen] for s in scores]
        ax.bar(x + offset, vals, bar_width * 0.9,
               label=PATHOGEN_SHORT[pathogen],
               color=pathogen_colors[pi], edgecolor='white', linewidth=0.3)

    # Add mean line markers
    for si, score in enumerate(scores):
        mean_val = pivot.loc[score, 'mean']
        ax.plot(si, mean_val, 'k_', markersize=12, markeredgewidth=2, zorder=10)

    ax.set_xticks(x)
    ax.set_xticklabels(score_labels, fontsize=8.5, rotation=20, ha='right')
    ax.set_ylabel('Best MCC (per pathogen)', fontsize=10)
    ax.set_xlabel('Scoring formula', fontsize=10)
    ax.legend(fontsize=7, frameon=False, ncol=5, loc='upper right',
              bbox_to_anchor=(1.0, 1.0))

    # Add "mean" marker to legend
    ax.plot([], [], 'k_', markersize=8, markeredgewidth=2, label='Mean')
    handles, labels = ax.get_legend_handles_labels()
    ax.legend(handles, labels, fontsize=7, frameon=False, ncol=5,
              loc='upper right', bbox_to_anchor=(1.0, 1.0))

    ax.axhline(y=0, color='black', linewidth=0.3)
    plt.tight_layout()
    fig.savefig(f'{FIG_DIR}/scoring_comparison.png')
    plt.close(fig)
    print('Saved Fig 3: scoring_comparison.png')


def fig5_variance_decomposition():
    """Figure 5: ANOVA variance decomposition (9 pathogens)."""
    df = pd.read_csv(f'{DATA_DIR}/anova_9pathogen.csv')
    df = df[df['dataset'] != 'Combined']

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(8, 3.5),
                                    gridspec_kw={'width_ratios': [3, 1]})

    # Left: stacked bars per pathogen
    eta_data = {}
    for _, row in df.iterrows():
        pathogen = row['dataset']
        eta_data[pathogen] = [
            row['eta2_scoring'],
            row['eta2_detection'],
            row['eta2_residual']
        ]

    pathogens_in_order = [p for p in PATHOGEN_ORDER if p in eta_data]
    short_labels = [PATHOGEN_SHORT[p] for p in pathogens_in_order]

    x = np.arange(len(pathogens_in_order))
    width = 0.55
    labels = ['Scoring', 'Detection', 'Residual']
    colors = [C_SCORING, C_DETECTION, C_RESIDUAL]

    bottoms = np.zeros(len(pathogens_in_order))
    for i, (label, color) in enumerate(zip(labels, colors)):
        vals = [eta_data[p][i] for p in pathogens_in_order]
        ax1.bar(x, vals, width, bottom=bottoms, label=label, color=color,
                edgecolor='white', linewidth=0.5)
        for j, v in enumerate(vals):
            if v > 0.06:
                ax1.text(x[j], bottoms[j] + v/2, f'{v:.0%}',
                        ha='center', va='center', fontsize=6.5, color='white',
                        fontweight='bold')
        bottoms += vals

    ax1.set_xticks(x)
    ax1.set_xticklabels(short_labels, fontsize=8, rotation=30, ha='right')
    ax1.set_ylabel(r'Proportion of variance ($\eta^2$)', fontsize=10)
    ax1.set_ylim(0, 1.05)
    ax1.legend(loc='upper right', fontsize=8, frameon=False)
    ax1.set_title('(A) Per-pathogen variance decomposition', fontsize=10,
                  fontweight='bold', loc='left')

    # Right: donut chart (average across 9 pathogens)
    avg_vals = np.mean([[eta_data[p][i] for p in pathogens_in_order]
                        for i in range(3)], axis=1)
    wedges, texts, autotexts = ax2.pie(
        avg_vals, labels=None, colors=colors, autopct='%1.0f%%',
        startangle=90, pctdistance=0.72,
        wedgeprops=dict(width=0.4, edgecolor='white', linewidth=1.5))
    for t in autotexts:
        t.set_fontsize(9)
        t.set_fontweight('bold')

    # Add legend below donut
    ax2.legend(labels, loc='lower center', fontsize=7.5, frameon=False,
               bbox_to_anchor=(0.5, -0.15), ncol=1)
    ax2.set_title('(B) Cross-pathogen\naverage (n=9)', fontsize=10,
                  fontweight='bold', loc='center')

    plt.tight_layout()
    fig.savefig(f'{FIG_DIR}/variance_decomposition.png')
    plt.close(fig)
    print('Saved Fig 5: variance_decomposition.png')


def fig_detection_ranking():
    """Additional: Detection family ranking across 9 pathogens."""
    df = load_9pathogen()

    # Best scoring per detection-pathogen pair, then mean across pathogens
    best_per = df.groupby(['pathogen', 'family'])['mcc'].max().reset_index()
    family_means = best_per.groupby('family')['mcc'].mean().sort_values(ascending=True)

    fig, ax = plt.subplots(figsize=(5, 4))

    colors = [C_DETECTION if f == 'Wavelet' else '#8C8C8C' for f in family_means.index]
    bars = ax.barh(np.arange(len(family_means)), family_means.values,
                   height=0.6, color=colors, edgecolor='white', linewidth=0.5)

    for i, (fam, val) in enumerate(family_means.items()):
        ax.text(val + 0.005, i, f'{val:.3f}', va='center', fontsize=7.5)

    ax.set_yticks(np.arange(len(family_means)))
    ax.set_yticklabels(family_means.index, fontsize=8)
    ax.set_xlabel('Mean MCC (best scoring per pathogen, 9 pathogens)', fontsize=9)
    ax.set_title('Detection family ranking', fontsize=10, fontweight='bold', loc='left')

    plt.tight_layout()
    fig.savefig(f'{FIG_DIR}/detection_ranking.png')
    plt.close(fig)
    print('Saved additional: detection_ranking.png')


if __name__ == '__main__':
    import os
    os.makedirs(FIG_DIR, exist_ok=True)

    fig1_scoring_detection_heatmap()
    fig2_cross_pathogen_top5()
    fig3_scoring_comparison()
    fig5_variance_decomposition()
    fig_detection_ranking()

    print('\nAll 9-pathogen figures generated.')
