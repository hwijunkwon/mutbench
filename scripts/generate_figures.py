#!/usr/bin/env python3
"""Generate 8 publication-quality figures for MutBench manuscript."""

import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch
import matplotlib.ticker as mticker
from scipy import signal
import warnings
warnings.filterwarnings('ignore')

# Global style
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

# Consistent colors
C_SCORING = '#4C72B0'
C_DETECTION = '#55A868'
C_INTERACTION = '#C44E52'
C_RESIDUAL = '#8C8C8C'

PATHOGEN_ORDER = ['SARS-CoV-2', 'H3N2', 'Norovirus', 'HIV-1']


def fig_c1_variance_decomposition():
    """C1: ANOVA variance decomposition - stacked bar + donut."""
    df = pd.read_csv(f'{DATA_DIR}/anova_diagnostics.csv')
    df_raw = df[df['transform'] == 'raw_MCC'].copy()

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(7, 3.2),
                                    gridspec_kw={'width_ratios': [2.5, 1]})

    # Left: stacked bars per pathogen
    eta_data = {}
    for pathogen in PATHOGEN_ORDER:
        pdata = df_raw[df_raw['pathogen'] == pathogen]
        score_eta = pdata[pdata['source'] == 'score']['eta_sq'].values[0]
        family_eta = pdata[pdata['source'] == 'family']['eta_sq'].values[0]
        inter_eta = pdata[pdata['source'] == 'score x family']['eta_sq'].values[0]
        resid_eta = pdata[pdata['source'] == 'Residual']['eta_sq'].values[0]
        eta_data[pathogen] = [score_eta, family_eta, inter_eta, resid_eta]

    x = np.arange(len(PATHOGEN_ORDER))
    width = 0.55
    labels = ['Scoring', 'Detection', 'Interaction', 'Residual']
    colors = [C_SCORING, C_DETECTION, C_INTERACTION, C_RESIDUAL]

    bottoms = np.zeros(len(PATHOGEN_ORDER))
    for i, (label, color) in enumerate(zip(labels, colors)):
        vals = [eta_data[p][i] for p in PATHOGEN_ORDER]
        ax1.bar(x, vals, width, bottom=bottoms, label=label, color=color,
                edgecolor='white', linewidth=0.5)
        for j, v in enumerate(vals):
            if v > 0.05:
                ax1.text(x[j], bottoms[j] + v/2, f'{v:.0%}',
                        ha='center', va='center', fontsize=7.5, color='white',
                        fontweight='bold')
        bottoms += vals

    ax1.set_xticks(x)
    ax1.set_xticklabels(PATHOGEN_ORDER, fontsize=9)
    ax1.set_ylabel(r'Proportion of variance ($\eta^2$)', fontsize=10)
    ax1.set_ylim(0, 1.05)
    ax1.legend(loc='upper right', fontsize=8, frameon=False, ncol=2)
    ax1.set_title('(A) Per-pathogen variance decomposition', fontsize=10,
                  fontweight='bold', loc='left')

    # Right: donut chart (average across pathogens)
    avg_vals = np.mean([[eta_data[p][i] for p in PATHOGEN_ORDER] for i in range(4)], axis=1)
    wedges, texts, autotexts = ax2.pie(
        avg_vals, labels=None, colors=colors, autopct='%1.0f%%',
        startangle=90, pctdistance=0.75, wedgeprops=dict(width=0.4, edgecolor='white', linewidth=1.5))
    for t in autotexts:
        t.set_fontsize(8)
        t.set_fontweight('bold')
    ax2.set_title('(B) Cross-pathogen\naverage', fontsize=10,
                  fontweight='bold', loc='center')

    plt.tight_layout()
    fig.savefig(f'{FIG_DIR}/variance_decomposition.png')
    plt.close(fig)
    print('Saved C1: variance_decomposition.png')


def fig_c2_cross_pathogen():
    """C2: Per-pathogen MCC for top 5 cross-pathogen combinations."""
    df = pd.read_csv(f'{DATA_DIR}/mcc_algorithm_results.csv')

    combos = [
        ('E*rare', 'Wavelet(t=1.0)', r'E$\times$rare + Wavelet(1.0)'),
        ('E*rare', 'Wavelet(t=1.5)', r'E$\times$rare + Wavelet(1.5)'),
        ('minority_E', 'Wavelet(t=1.5)', 'minority_E + Wavelet(1.5)'),
        ('H-score', 'SlidingTest(p=0.05)', 'H-score + SlidingTest(0.05)'),
        ('P*E', 'AdaptiveKnee', r'P$\times$E + AdaptiveKnee'),
    ]

    colors = ['#4C72B0', '#DD8452', '#55A868', '#C44E52', '#8172B3']

    fig, axes = plt.subplots(1, 4, figsize=(7, 2.8), sharey=True)

    for idx, pathogen in enumerate(PATHOGEN_ORDER):
        ax = axes[idx]
        mcc_vals = []
        for score, detector, label in combos:
            row = df[(df['pathogen'] == pathogen) & (df['score'] == score) &
                     (df['detector'] == detector)]
            if len(row) > 0:
                mcc_vals.append(row['mcc'].values[0])
            else:
                mcc_vals.append(0)

        y_pos = np.arange(len(combos))
        bars = ax.barh(y_pos, mcc_vals, height=0.6, color=colors,
                       edgecolor='white', linewidth=0.5)

        for j, (bar, val) in enumerate(zip(bars, mcc_vals)):
            if val > 0:
                ax.text(val + 0.01, j, f'{val:.3f}', va='center', fontsize=7)
            else:
                ax.text(0.01, j, f'{val:.3f}', va='center', fontsize=7)

        ax.set_xlim(-0.1, 0.8)
        ax.set_title(pathogen, fontsize=9, fontweight='bold')
        ax.axvline(x=0, color='black', linewidth=0.5, linestyle='-')

        if idx == 0:
            ax.set_yticks(y_pos)
            ax.set_yticklabels([c[2] for c in combos], fontsize=7.5)
        else:
            ax.set_yticks(y_pos)
            ax.set_yticklabels([])

        ax.set_xlabel('MCC', fontsize=9)

    plt.tight_layout()
    fig.savefig(f'{FIG_DIR}/cross_pathogen_comparison.png')
    plt.close(fig)
    print('Saved C2: cross_pathogen_comparison.png')


def fig_c3_scoring_detection_heatmap():
    """C3: Interaction heatmap of scoring x detection family."""
    df = pd.read_csv(f'{DATA_DIR}/mcc_algorithm_results.csv')

    def get_family(det):
        for prefix in ['Wavelet', 'KDE', 'AdaptWin', 'AdaptiveKnee',
                       'SlidingTest', 'CUSUM', 'Bayes', 'Ensemble',
                       'GradPeak', 'LocalContrast', 'ScoreDBSCAN', 'Spectral']:
            if det.startswith(prefix):
                return prefix
        return det

    df['family'] = df['detector'].apply(get_family)

    pivot = df.groupby(['score', 'family'])['mcc'].mean().reset_index()
    heatmap_data = pivot.pivot(index='score', columns='family', values='mcc')

    score_order = ['E*rare', 'P*E*rare', 'minority_E', 'P*minority_E',
                   'P*E', 'P*E^2', 'rank(P*E)', 'E_only', 'H-score']
    score_order = [s for s in score_order if s in heatmap_data.index]

    family_order = sorted(heatmap_data.columns)
    heatmap_data = heatmap_data.reindex(index=score_order, columns=family_order)

    fig, ax = plt.subplots(figsize=(7, 3.5))
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

    ax.set_xticks(np.arange(len(family_order)))
    ax.set_xticklabels(family_order, fontsize=7.5, rotation=40, ha='right')
    ax.set_yticks(np.arange(len(score_order)))
    ax.set_yticklabels(score_order, fontsize=8)
    ax.set_xlabel('Detection family', fontsize=10)
    ax.set_ylabel('Scoring formula', fontsize=10)

    cbar = plt.colorbar(im, ax=ax, shrink=0.8, pad=0.02)
    cbar.set_label('Mean MCC (4 pathogens)', fontsize=9)
    cbar.ax.tick_params(labelsize=8)

    plt.tight_layout()
    fig.savefig(f'{FIG_DIR}/scoring_detection_heatmap.png')
    plt.close(fig)
    print('Saved C3: scoring_detection_heatmap.png')


def fig_c4_cwt_scalogram():
    """C4: CWT scalogram illustration with synthetic E*rare profile."""
    np.random.seed(42)

    n = 200
    positions = np.arange(1, n + 1)

    # Base: low background with hotspot peaks
    base = np.random.exponential(0.3, n)
    hotspots = [35, 80, 120, 155]
    for h in hotspots:
        width = np.random.randint(3, 8)
        height = np.random.uniform(2.0, 5.0)
        base[max(0, h-width):min(n, h+width)] += height * np.exp(
            -0.5 * ((np.arange(max(0, h-width), min(n, h+width)) - h) / (width/2))**2)

    scores = base

    scales = np.array([2, 4, 8, 16, 32])

    # Manual CWT with Ricker wavelet (scipy.signal.cwt removed in newer versions)
    def ricker(points, a):
        A = 2 / (np.sqrt(3 * a) * (np.pi**0.25))
        wsq = a**2
        vec = np.arange(0, points) - (points - 1.0) / 2
        tsq = vec**2
        mod = (1 - tsq / wsq)
        gauss = np.exp(-tsq / (2 * wsq))
        return A * mod * gauss

    def manual_cwt(data, scales):
        output = np.zeros((len(scales), len(data)))
        for i, scale in enumerate(scales):
            N = min(10 * scale, len(data))
            if N % 2 == 0:
                N += 1
            wavelet = ricker(N, scale)
            conv = np.convolve(data, wavelet, mode='same')
            output[i] = conv[:len(data)]
        return output

    cwt_matrix = manual_cwt(scores, scales)

    z_scores = np.abs(cwt_matrix)
    z_norm = (z_scores - z_scores.mean(axis=1, keepdims=True)) / (z_scores.std(axis=1, keepdims=True) + 1e-10)
    consensus = (z_norm > 1.0).sum(axis=0)
    detected = positions[consensus >= 2]

    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(7, 3.5),
                                    gridspec_kw={'height_ratios': [1, 1.2]},
                                    sharex=True)

    # Top: raw score profile
    ax1.fill_between(positions, 0, scores, color='#4C72B0', alpha=0.3)
    ax1.plot(positions, scores, color='#4C72B0', linewidth=0.8)
    for d in detected:
        if scores[d-1] > np.percentile(scores, 70):
            ax1.axvline(d, color='#C44E52', alpha=0.15, linewidth=2)
    ax1.set_ylabel('Score', fontsize=10)
    ax1.set_title('(A) Mutation score profile', fontsize=10,
                  fontweight='bold', loc='left')

    for h in hotspots:
        ax1.annotate('', xy=(h, scores[h]*0.95), xytext=(h, scores[h]*1.15),
                    arrowprops=dict(arrowstyle='->', color='#C44E52', lw=1.2))

    # Bottom: CWT coefficients heatmap
    im = ax2.imshow(np.abs(cwt_matrix), aspect='auto', cmap='YlOrRd',
                    extent=[1, n, len(scales)-0.5, -0.5],
                    interpolation='bilinear')
    ax2.set_yticks(np.arange(len(scales)))
    ax2.set_yticklabels([str(s) for s in scales], fontsize=8)
    ax2.set_ylabel('CWT scale', fontsize=10)
    ax2.set_xlabel('Position', fontsize=10)
    ax2.set_title('(B) CWT coefficient magnitudes', fontsize=10,
                  fontweight='bold', loc='left')

    for d in detected:
        if scores[d-1] > np.percentile(scores, 70):
            ax2.axvline(d, color='white', alpha=0.4, linewidth=0.5, linestyle='--')

    cbar = plt.colorbar(im, ax=ax2, shrink=0.8, pad=0.02)
    cbar.set_label('|CWT coefficient|', fontsize=8)
    cbar.ax.tick_params(labelsize=7)

    plt.tight_layout()
    fig.savefig(f'{FIG_DIR}/cwt_scalogram.png')
    plt.close(fig)
    print('Saved C4: cwt_scalogram.png')


def fig_c5_threshold_sensitivity():
    """C5: Threshold sensitivity - mean MCC vs wavelet threshold per scoring."""
    df = pd.read_csv(f'{DATA_DIR}/mcc_algorithm_results.csv')

    wavelet_df = df[df['detector'].str.startswith('Wavelet')].copy()
    wavelet_df['threshold'] = wavelet_df['detector'].str.extract(r't=(\d+\.?\d*)').astype(float)

    means = wavelet_df.groupby(['score', 'threshold'])['mcc'].mean().reset_index()

    scores = sorted(means['score'].unique())
    thresholds = sorted(means['threshold'].unique())

    fig, ax = plt.subplots(figsize=(3.5, 3))

    for score in scores:
        sdata = means[means['score'] == score].sort_values('threshold')
        if score == 'E*rare':
            ax.plot(sdata['threshold'], sdata['mcc'], '-o', color='#4C72B0',
                   linewidth=2.2, markersize=5, label=r'E$\times$rare', zorder=10)
        else:
            ax.plot(sdata['threshold'], sdata['mcc'], '-', color='#AAAAAA',
                   linewidth=0.8, alpha=0.6)

    ax.plot([], [], '-', color='#AAAAAA', linewidth=0.8, label='Other formulas')
    ax.legend(fontsize=8, frameon=False, loc='upper right')

    ax.set_xlabel('Wavelet z-threshold', fontsize=10)
    ax.set_ylabel('Mean MCC (4 pathogens)', fontsize=10)
    ax.set_xticks(thresholds)

    plt.tight_layout()
    fig.savefig(f'{FIG_DIR}/threshold_sensitivity.png')
    plt.close(fig)
    print('Saved C5: threshold_sensitivity.png')


def fig_c6_ablation_heatmap():
    """C6: Ablation study - E*rare components + wavelet design choices."""
    df_abl = pd.read_csv(f'{DATA_DIR}/exrare_ablation.csv')

    df_wav = df_abl[df_abl['detector'] == 'Wavelet(t=1.0)']
    scoring_means = df_wav.groupby('scoring')['mcc'].mean()

    score_order_a = ['E*rare', 'E_only', 'rare_only', 'E+rare (0.5/0.5)',
                     'E+rare (0.7/0.3)', 'H-score']
    score_labels_a = [r'E$\times$rare', 'E only', 'rare only',
                      'E+rare (0.5/0.5)', 'E+rare (0.7/0.3)', 'H-score']

    mcc_a = [scoring_means.get(s, 0) for s in score_order_a]

    df_zsign = pd.read_csv(f'{DATA_DIR}/zscore_sign_ablation.csv')
    df_pad = pd.read_csv(f'{DATA_DIR}/padding_ablation.csv')
    df_thresh = pd.read_csv(f'{DATA_DIR}/threshold_method_ablation.csv')

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(7, 3.2),
                                    gridspec_kw={'width_ratios': [1.2, 1.8]})

    # Panel A: bar chart
    colors_a = ['#4C72B0' if s == 'E*rare' else '#8C8C8C' for s in score_order_a]
    ax1.barh(np.arange(len(score_order_a)), mcc_a, height=0.6,
             color=colors_a, edgecolor='white', linewidth=0.5)
    for i, v in enumerate(mcc_a):
        ax1.text(v + 0.005, i, f'{v:.3f}', va='center', fontsize=7.5)
    ax1.set_yticks(np.arange(len(score_order_a)))
    ax1.set_yticklabels(score_labels_a, fontsize=8)
    ax1.set_xlabel('Mean MCC (4 pathogens)', fontsize=9)
    ax1.set_title('(A) Scoring ablation', fontsize=10,
                  fontweight='bold', loc='left')
    ax1.invert_yaxis()

    # Panel B: grouped bars for design choices
    design_groups = {}

    zsign_means = df_zsign.groupby('z_mode')['mcc'].mean()
    design_groups['z-score sign'] = {
        '|z| (both)': zsign_means.get('|z| > t (both)', 0),
        'z > t (+)': zsign_means.get('z > t (positive)', 0),
        'z < -t (-)': zsign_means.get('z < -t (negative)', 0),
    }

    pad_means = df_pad.groupby('padding')['mcc'].mean()
    design_groups['Padding'] = dict(pad_means)

    thresh_means = df_thresh.groupby('threshold_method')['mcc'].mean()
    design_groups['Threshold'] = {
        'z-score': thresh_means.get('z-score (current)', 0),
        'percentile': thresh_means.get('percentile (1-sigma equiv)', 0),
        'MAD': thresh_means.get('MAD-based', 0),
    }

    group_names = list(design_groups.keys())
    group_colors = ['#4C72B0', '#55A868', '#C44E52']

    y_pos = []
    y_labels = []
    bar_colors = []
    vals_b = []
    current_y = 0

    for gi, gname in enumerate(group_names):
        variants = design_groups[gname]
        for vname, val in variants.items():
            y_pos.append(current_y)
            y_labels.append(vname)
            bar_colors.append(group_colors[gi])
            vals_b.append(val)
            current_y += 0.7
        current_y += 0.5

    ax2.barh(y_pos, vals_b, height=0.55, color=bar_colors,
             edgecolor='white', linewidth=0.5)
    for i, v in enumerate(vals_b):
        ax2.text(v + 0.005, y_pos[i], f'{v:.3f}', va='center', fontsize=7)

    ax2.set_yticks(y_pos)
    ax2.set_yticklabels(y_labels, fontsize=7.5)
    ax2.set_xlabel('Mean MCC (4 pathogens)', fontsize=9)
    ax2.set_title('(B) Wavelet design choices', fontsize=10,
                  fontweight='bold', loc='left')
    ax2.invert_yaxis()

    # Add group separator lines and labels on right side
    current_y = 0
    for gi, gname in enumerate(group_names):
        n = len(design_groups[gname])
        mid_y = current_y + (n - 1) * 0.7 / 2
        # Group label on the right
        ax2.text(1.02, mid_y, gname, ha='left', va='center',
                fontsize=7, fontweight='bold', color=group_colors[gi],
                transform=ax2.get_yaxis_transform())
        # Separator line between groups
        if gi < len(group_names) - 1:
            sep_y = current_y + n * 0.7 + 0.25 - 0.35
            ax2.axhline(sep_y, color='#CCCCCC', linewidth=0.5, linestyle='--')
        current_y += n * 0.7 + 0.5

    plt.tight_layout()
    fig.savefig(f'{FIG_DIR}/ablation_heatmap.png')
    plt.close(fig)
    print('Saved C6: ablation_heatmap.png')


def fig_c7_lopo_region():
    """C7: LOPO cross-validation + region-level precision."""
    lopo_data = {
        'SARS-CoV-2': {'train': 0.341, 'test': 0.168},
        'H3N2': {'train': 0.325, 'test': 0.215},
        'Norovirus': {'train': 0.254, 'test': 0.224},
        'HIV-1': {'train': 0.298, 'test': 0.297},
    }

    df_reg = pd.read_csv(f'{DATA_DIR}/region_overlap_results.csv')

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(7, 3),
                                    gridspec_kw={'width_ratios': [1, 1.2]})

    # Left: LOPO bar chart
    x = np.arange(len(PATHOGEN_ORDER))
    width = 0.3
    train_vals = [lopo_data[p]['train'] for p in PATHOGEN_ORDER]
    test_vals = [lopo_data[p]['test'] for p in PATHOGEN_ORDER]

    ax1.bar(x - width/2, train_vals, width, label='Train (3 pathogens)',
            color='#4C72B0', edgecolor='white', linewidth=0.5)
    ax1.bar(x + width/2, test_vals, width, label='Test (held-out)',
            color='#DD8452', edgecolor='white', linewidth=0.5)

    for i in range(len(PATHOGEN_ORDER)):
        ax1.text(x[i] - width/2, train_vals[i] + 0.008, f'{train_vals[i]:.3f}',
                ha='center', va='bottom', fontsize=7)
        ax1.text(x[i] + width/2, test_vals[i] + 0.008, f'{test_vals[i]:.3f}',
                ha='center', va='bottom', fontsize=7)

    ax1.set_xticks(x)
    ax1.set_xticklabels(PATHOGEN_ORDER, fontsize=8, rotation=15, ha='right')
    ax1.set_ylabel('MCC', fontsize=10)
    ax1.legend(fontsize=7.5, frameon=False)
    ax1.set_ylim(0, 0.42)
    ax1.set_title('(A) LOPO cross-validation', fontsize=10,
                  fontweight='bold', loc='left')

    # Right: Region-level MCC vs window size
    top_combos = [
        'E*rare + Wavelet(t=1.0)',
        'E*rare + Wavelet(t=1.5)',
        'H-score + SlidingTest(p=0.05)',
        'E_only + AdaptiveKnee',
        'P*E^2 + AdaptWin(s=90)',
    ]

    colors_r = ['#4C72B0', '#DD8452', '#55A868', '#C44E52', '#8172B3']
    windows = sorted(df_reg['window'].unique())

    for ci, combo in enumerate(top_combos):
        combo_data = df_reg[df_reg['combo'] == combo]
        if len(combo_data) == 0:
            continue
        w_means = combo_data.groupby('window')['relaxed_mcc'].mean()
        label = combo.replace('E*rare', r'E$\times$rare')
        ax2.plot(w_means.index, w_means.values, '-o', color=colors_r[ci],
                linewidth=1.2, markersize=3, label=label)

    ax2.set_xlabel('Window size w (positions)', fontsize=9)
    ax2.set_ylabel('Relaxed MCC', fontsize=9)
    ax2.legend(fontsize=6.5, frameon=False, loc='lower right')
    ax2.set_title('(B) Region-level precision', fontsize=10,
                  fontweight='bold', loc='left')

    plt.tight_layout()
    fig.savefig(f'{FIG_DIR}/lopo_region_precision.png')
    plt.close(fig)
    print('Saved C7: lopo_region_precision.png')


def fig_c8_dms_scatter():
    """C8: DMS fitness vs E*rare scatter plot."""
    df_pos = pd.read_csv(f'{DATA_DIR}/new_methodology_position_scores.csv')
    df_bloom = pd.read_csv(f'{DATA_DIR}/bloom_deep_analysis.csv')

    df_bloom_sub = df_bloom[['codon_site', 'mean_fitness']].copy()
    df_bloom_sub.rename(columns={'codon_site': 'position'}, inplace=True)

    merged = pd.merge(df_pos, df_bloom_sub, on='position', how='inner')

    # Compute E*rare: entropy * (1 - freq_vs_consensus)
    merged['exrare'] = merged['entropy'] * (1 - merged['freq_vs_consensus'])

    valid = merged.dropna(subset=['mean_fitness', 'exrare'])

    # Correlation
    df_corr = pd.read_csv(f'{DATA_DIR}/dms_continuous_correlation.csv')
    exrare_row = df_corr[df_corr['scoring_formula'] == 'E*rare']
    rho = exrare_row['spearman_rho'].values[0] if len(exrare_row) > 0 else 0
    pval = exrare_row['spearman_pvalue'].values[0] if len(exrare_row) > 0 else 1

    fig, ax = plt.subplots(figsize=(3.5, 3.2))

    gt_mask = valid['is_functional'] == True
    non_gt = valid[~gt_mask]
    gt = valid[gt_mask]

    ax.scatter(non_gt['mean_fitness'], non_gt['exrare'],
              s=8, alpha=0.3, color='#8C8C8C', label='Non-GT', rasterized=True,
              edgecolors='none')
    ax.scatter(gt['mean_fitness'], gt['exrare'],
              s=12, alpha=0.6, color='#C44E52', label='GT-narrow', rasterized=True,
              edgecolors='none')

    ax.text(0.05, 0.95, f'Spearman $\\rho$ = {rho:.3f}\np = {pval:.4f}',
           transform=ax.transAxes, fontsize=8, va='top',
           bbox=dict(boxstyle='round,pad=0.3', facecolor='white',
                     edgecolor='#CCCCCC', alpha=0.9))

    ax.set_xlabel('DMS mean fitness effect', fontsize=10)
    ax.set_ylabel(r'E$\times$rare score', fontsize=10)
    ax.legend(fontsize=8, frameon=False, loc='upper right',
             markerscale=1.5)

    plt.tight_layout()
    fig.savefig(f'{FIG_DIR}/dms_scatter.png')
    plt.close(fig)
    print('Saved C8: dms_scatter.png')


if __name__ == '__main__':
    import os
    os.makedirs(FIG_DIR, exist_ok=True)

    fig_c1_variance_decomposition()
    fig_c2_cross_pathogen()
    fig_c3_scoring_detection_heatmap()
    fig_c4_cwt_scalogram()
    fig_c5_threshold_sensitivity()
    fig_c6_ablation_heatmap()
    fig_c7_lopo_region()
    fig_c8_dms_scatter()

    print('\nAll 8 figures generated successfully.')
