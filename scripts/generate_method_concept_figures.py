#!/usr/bin/env python3
"""
Generate step-by-step concept diagrams for 4 detection methods.
Each method gets a 4-panel figure showing how it works.
"""

import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

matplotlib.rcParams['font.family'] = 'sans-serif'
matplotlib.rcParams['axes.grid'] = False

OUT_DIR = '/proj/paper/paper/dissertation/guide_figures'

# Shared synthetic score profile
np.random.seed(42)
N = 200
positions = np.arange(N)
scores = np.random.exponential(0.02, N)
# Insert 2 hotspot regions
scores[60:75] = np.random.uniform(0.3, 0.8, 15)
scores[140:155] = np.random.uniform(0.4, 0.9, 15)
# A few scattered medium values
scores[30] = 0.15
scores[100] = 0.12
scores[180] = 0.18


def fig_freqthresh():
    """FreqThresh: 4-step concept diagram."""
    fig, axes = plt.subplots(4, 1, figsize=(12, 10), sharex=True)
    colors = {'bg': '#E8E8E8', 'hot': '#D62728', 'line': '#4C72B0', 'thresh': '#FF7F0E'}

    # Step 1: Raw score profile
    ax = axes[0]
    ax.bar(positions, scores, width=1.0, color=colors['line'], alpha=0.7, edgecolor='none')
    ax.set_ylabel('Score', fontsize=12)
    ax.set_title('Step 1: Calculate score for each genomic position', fontsize=13, fontweight='bold', loc='left')
    ax.set_ylim(0, 1.0)

    # Step 2: Sort scores
    ax = axes[1]
    sorted_scores = np.sort(scores)[::-1]
    ax.bar(np.arange(N), sorted_scores, width=1.0, color=colors['line'], alpha=0.7, edgecolor='none')
    ax.set_ylabel('Score (sorted)', fontsize=12)
    ax.set_title('Step 2: Sort all scores from highest to lowest', fontsize=13, fontweight='bold', loc='left')
    ax.set_ylim(0, 1.0)

    # Step 3: Draw threshold line (top 10%)
    ax = axes[2]
    k = int(N * 0.10)
    threshold = sorted_scores[k]
    bar_colors = [colors['hot'] if s >= threshold else colors['bg'] for s in sorted_scores]
    ax.bar(np.arange(N), sorted_scores, width=1.0, color=bar_colors, alpha=0.8, edgecolor='none')
    ax.axhline(y=threshold, color=colors['thresh'], linestyle='--', linewidth=2)
    ax.annotate(f'Top 10% threshold = {threshold:.2f}', xy=(1.02, threshold),
                xycoords=('axes fraction', 'data'), fontsize=11, color=colors['thresh'],
                va='center', ha='left', fontweight='bold', annotation_clip=False)
    ax.set_ylabel('Score (sorted)', fontsize=12)
    ax.set_title('Step 3: Set threshold at top k% (e.g., top 10%)', fontsize=13, fontweight='bold', loc='left')
    ax.set_ylim(0, 1.0)

    # Step 4: Apply to original positions → hotspots
    ax = axes[3]
    bar_colors_orig = [colors['hot'] if s >= threshold else colors['bg'] for s in scores]
    ax.bar(positions, scores, width=1.0, color=bar_colors_orig, alpha=0.8, edgecolor='none')
    ax.axhline(y=threshold, color=colors['thresh'], linestyle='--', linewidth=1.5, alpha=0.5)
    # Annotate hotspot regions
    for start, end in [(60, 75), (140, 155)]:
        ax.annotate('Hotspot', xy=((start+end)/2, 0.85), fontsize=11,
                    ha='center', color=colors['hot'], fontweight='bold')
    ax.set_ylabel('Score', fontsize=12)
    ax.set_xlabel('Genomic Position', fontsize=12)
    ax.set_title('Step 4: Positions above threshold = detected hotspots (red)', fontsize=13, fontweight='bold', loc='left')
    ax.set_ylim(0, 1.0)

    for ax in axes:
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.tick_params(labelsize=10)

    fig.tight_layout(pad=1.5)
    fig.savefig(f'{OUT_DIR}/concept_freqthresh.png', dpi=200, bbox_inches='tight', facecolor='white')
    plt.close(fig)
    print('Saved: concept_freqthresh.png')


def fig_sliding_window():
    """Sliding Window: 4-step concept diagram."""
    fig, axes = plt.subplots(4, 1, figsize=(12, 10), sharex=True)
    colors = {'bg': '#E8E8E8', 'hot': '#55A868', 'line': '#4C72B0', 'win': '#FF7F0E'}
    window_size = 15

    # Step 1: Raw score profile
    ax = axes[0]
    ax.bar(positions, scores, width=1.0, color=colors['line'], alpha=0.7, edgecolor='none')
    ax.set_ylabel('Score', fontsize=12)
    ax.set_title('Step 1: Score profile across the genome', fontsize=13, fontweight='bold', loc='left')
    ax.set_ylim(0, 1.0)

    # Step 2: Show sliding window
    ax = axes[1]
    ax.bar(positions, scores, width=1.0, color=colors['line'], alpha=0.4, edgecolor='none')
    # Draw window boxes at several positions
    for win_start in [20, 60, 100, 140]:
        rect = mpatches.FancyBboxPatch((win_start, 0), window_size, 0.95,
                                        boxstyle="round,pad=0.5", linewidth=2,
                                        edgecolor=colors['win'], facecolor='none')
        ax.add_patch(rect)
    ax.annotate(f'Window size = {window_size}', xy=(25, 0.92), fontsize=11,
                color=colors['win'], fontweight='bold')
    ax.set_ylabel('Score', fontsize=12)
    ax.set_title('Step 2: Slide a window across the genome, computing mean in each window',
                 fontsize=13, fontweight='bold', loc='left')
    ax.set_ylim(0, 1.0)

    # Step 3: Window means + global mean threshold
    ax = axes[2]
    window_means = np.convolve(scores, np.ones(window_size)/window_size, mode='same')
    global_mean = np.mean(scores)
    global_std = np.std(scores)
    z_threshold = global_mean + 2 * global_std

    ax.plot(positions, window_means, color=colors['line'], linewidth=2, label='Window mean')
    ax.axhline(y=z_threshold, color=colors['hot'], linestyle='--', linewidth=2)
    ax.annotate(f'Threshold (mean + 2σ = {z_threshold:.3f})', xy=(1.02, z_threshold),
                xycoords=('axes fraction', 'data'), fontsize=10, color=colors['hot'],
                va='center', ha='left', fontweight='bold', annotation_clip=False)
    ax.fill_between(positions, 0, window_means,
                    where=window_means > z_threshold,
                    color=colors['hot'], alpha=0.3)
    ax.set_ylabel('Window Mean', fontsize=12)
    ax.set_title('Step 3: Windows significantly above background (z-test, p < 0.05)',
                 fontsize=13, fontweight='bold', loc='left')
    ax.legend(fontsize=10, bbox_to_anchor=(0.5, -0.15), loc='upper center')

    # Step 4: Detected hotspots
    ax = axes[3]
    detected = window_means > z_threshold
    bar_colors = [colors['hot'] if d else colors['bg'] for d in detected]
    ax.bar(positions, scores, width=1.0, color=bar_colors, alpha=0.8, edgecolor='none')
    for start, end in [(55, 80), (135, 160)]:
        mid = (start + end) / 2
        if any(detected[start:end]):
            ax.annotate('Hotspot', xy=(mid, 0.85), fontsize=11,
                        ha='center', color=colors['hot'], fontweight='bold')
    ax.set_ylabel('Score', fontsize=12)
    ax.set_xlabel('Genomic Position', fontsize=12)
    ax.set_title('Step 4: Significant windows = detected hotspots (green)',
                 fontsize=13, fontweight='bold', loc='left')
    ax.set_ylim(0, 1.0)

    for ax in axes:
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.tick_params(labelsize=10)

    fig.tight_layout(pad=1.5)
    fig.savefig(f'{OUT_DIR}/concept_slidingwindow.png', dpi=200, bbox_inches='tight', facecolor='white')
    plt.close(fig)
    print('Saved: concept_slidingwindow.png')


def fig_dbscan():
    """DBSCAN: 4-step concept diagram."""
    fig, axes = plt.subplots(2, 2, figsize=(12, 10))
    colors_list = ['#4C72B0', '#D62728', '#55A868', '#8C8C8C', '#DD8452']

    # Generate 2D points (position, score)
    pos_norm = positions / N  # normalize to [0,1]
    pts_x = pos_norm
    pts_y = scores

    # Step 1: Scatter plot of all positions
    ax = axes[0, 0]
    ax.scatter(pts_x, pts_y, s=15, c='#4C72B0', alpha=0.6, edgecolors='none')
    ax.set_xlabel('Genomic Position (normalized)', fontsize=11)
    ax.set_ylabel('Score', fontsize=11)
    ax.set_title('Step 1: Map each position to\n2D space (position, score)', fontsize=13, fontweight='bold')
    ax.set_ylim(-0.05, 1.0)

    # Step 2: Show epsilon circles around some points
    ax = axes[0, 1]
    ax.scatter(pts_x, pts_y, s=15, c='#4C72B0', alpha=0.4, edgecolors='none')
    # Draw epsilon circles around hotspot points
    eps = 0.06
    for i in range(62, 72, 2):
        circle = plt.Circle((pts_x[i], pts_y[i]), eps, fill=False,
                            edgecolor='#FF7F0E', linewidth=1.5, alpha=0.7)
        ax.add_patch(circle)
    ax.set_xlabel('Genomic Position (normalized)', fontsize=11)
    ax.set_ylabel('Score', fontsize=11)
    ax.set_title(f'Step 2: For each point, check how many\nneighbors within ε={eps} radius',
                 fontsize=13, fontweight='bold')
    ax.set_ylim(-0.05, 1.0)
    ax.set_xlim(-0.05, 1.05)

    # Step 3: Points colored by cluster assignment
    ax = axes[1, 0]
    # Simple clustering simulation
    cluster_labels = np.full(N, -1)  # -1 = noise
    cluster_labels[58:77] = 0  # cluster 1
    cluster_labels[138:157] = 1  # cluster 2

    for cl, color in zip([-1, 0, 1], ['#CCCCCC', '#D62728', '#55A868']):
        mask = cluster_labels == cl
        label = 'Noise' if cl == -1 else f'Cluster {cl+1}'
        ax.scatter(pts_x[mask], pts_y[mask], s=20, c=color, alpha=0.7,
                  edgecolors='none', label=label)
    ax.set_xlabel('Genomic Position (normalized)', fontsize=11)
    ax.set_ylabel('Score', fontsize=11)
    ax.set_title('Step 3: Dense regions automatically\ngrouped into clusters', fontsize=13, fontweight='bold')
    ax.legend(fontsize=10, bbox_to_anchor=(0.5, -0.18), loc='upper center', ncol=3)
    ax.set_ylim(-0.05, 1.0)

    # Step 4: Back to genome coordinates — clusters = hotspots
    ax = axes[1, 1]
    bar_colors = []
    for cl in cluster_labels:
        if cl == 0:
            bar_colors.append('#D62728')
        elif cl == 1:
            bar_colors.append('#55A868')
        else:
            bar_colors.append('#E8E8E8')
    ax.bar(positions, scores, width=1.0, color=bar_colors, alpha=0.8, edgecolor='none')
    ax.annotate('Hotspot 1', xy=(67, 0.85), fontsize=11, ha='center',
                color='#D62728', fontweight='bold')
    ax.annotate('Hotspot 2', xy=(147, 0.85), fontsize=11, ha='center',
                color='#55A868', fontweight='bold')
    ax.set_xlabel('Genomic Position', fontsize=11)
    ax.set_ylabel('Score', fontsize=11)
    ax.set_title('Step 4: Each cluster = one hotspot region', fontsize=13, fontweight='bold')
    ax.set_ylim(0, 1.0)

    for ax in axes.flat:
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.tick_params(labelsize=10)

    fig.tight_layout(pad=2.0)
    fig.savefig(f'{OUT_DIR}/concept_dbscan.png', dpi=200, bbox_inches='tight', facecolor='white')
    plt.close(fig)
    print('Saved: concept_dbscan.png')


def fig_wavelet():
    """Wavelet: 4-step concept diagram."""
    fig, axes = plt.subplots(4, 1, figsize=(12, 10), sharex=True)
    colors = {'bg': '#E8E8E8', 'hot': '#8172B3', 'line': '#4C72B0', 'cwt': '#DD8452'}

    # Mexican hat wavelet (Ricker wavelet) implementation
    def ricker_wavelet(points, a):
        A = 2 / (np.sqrt(3 * a) * (np.pi**0.25))
        wsq = a**2
        vec = np.arange(0, points) - (points - 1.0) / 2
        tsq = vec**2
        mod = (1 - tsq / wsq)
        gauss = np.exp(-tsq / (2 * wsq))
        return A * mod * gauss

    # Simple CWT
    widths = np.arange(2, 20)
    cwt_matrix = np.zeros((len(widths), N))
    for i, w in enumerate(widths):
        wavelet = ricker_wavelet(min(10 * w, N), w)
        cwt_matrix[i] = np.convolve(scores, wavelet, mode='same')

    # Step 1: Raw score profile
    ax = axes[0]
    ax.bar(positions, scores, width=1.0, color=colors['line'], alpha=0.7, edgecolor='none')
    ax.set_ylabel('Score', fontsize=12)
    ax.set_title('Step 1: Score profile across the genome', fontsize=13, fontweight='bold', loc='left')
    ax.set_ylim(0, 1.0)

    # Step 2: CWT transform (show scalogram-like)
    ax = axes[1]
    ax.imshow(np.abs(cwt_matrix), aspect='auto', cmap='YlOrRd',
              extent=[0, N, widths[-1], widths[0]])
    ax.set_ylabel('Scale', fontsize=12)
    ax.set_title('Step 2: Wavelet transform — detect peaks at multiple scales',
                 fontsize=13, fontweight='bold', loc='left')

    # Step 3: CWT coefficients at one scale + threshold
    ax = axes[2]
    scale_idx = 5
    coeffs = np.abs(cwt_matrix[scale_idx])
    ax.plot(positions, coeffs, color=colors['cwt'], linewidth=2)
    thresh = np.mean(coeffs) + 1.5 * np.std(coeffs)
    ax.axhline(y=thresh, color=colors['hot'], linestyle='--', linewidth=2)
    ax.fill_between(positions, 0, coeffs, where=coeffs > thresh,
                    color=colors['hot'], alpha=0.3)
    ax.annotate(f'Threshold (mean + 1.5σ)', xy=(1.02, thresh),
                xycoords=('axes fraction', 'data'), fontsize=10, color=colors['hot'],
                va='center', ha='left', fontweight='bold', annotation_clip=False)
    ax.set_ylabel('CWT Coefficient', fontsize=12)
    ax.set_title(f'Step 3: At scale={widths[scale_idx]}, find regions above threshold',
                 fontsize=13, fontweight='bold', loc='left')

    # Step 4: Detected hotspots
    ax = axes[3]
    detected = coeffs > thresh
    bar_colors = [colors['hot'] if d else colors['bg'] for d in detected]
    ax.bar(positions, scores, width=1.0, color=bar_colors, alpha=0.8, edgecolor='none')
    for start, end in [(57, 78), (137, 158)]:
        mid = (start + end) / 2
        if any(detected[start:end]):
            ax.annotate('Hotspot', xy=(mid, 0.85), fontsize=11,
                        ha='center', color=colors['hot'], fontweight='bold')
    ax.set_ylabel('Score', fontsize=12)
    ax.set_xlabel('Genomic Position', fontsize=12)
    ax.set_title('Step 4: Significant regions = detected hotspots (purple)',
                 fontsize=13, fontweight='bold', loc='left')
    ax.set_ylim(0, 1.0)

    for ax in axes:
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.tick_params(labelsize=10)

    fig.tight_layout(pad=1.5)
    fig.savefig(f'{OUT_DIR}/concept_wavelet.png', dpi=200, bbox_inches='tight', facecolor='white')
    plt.close(fig)
    print('Saved: concept_wavelet.png')


def fig_cusum():
    """CUSUM: 4-step concept diagram."""
    fig, axes = plt.subplots(4, 1, figsize=(12, 10), sharex=True)
    colors = {'bg': '#E8E8E8', 'hot': '#DD8452', 'line': '#4C72B0'}

    # Step 1: Raw score profile
    ax = axes[0]
    ax.bar(positions, scores, width=1.0, color=colors['line'], alpha=0.7, edgecolor='none')
    ax.set_ylabel('Score', fontsize=12)
    ax.set_title('Step 1: Score profile across the genome', fontsize=13, fontweight='bold', loc='left')
    ax.set_ylim(0, 1.0)

    # Step 2: z-normalize
    ax = axes[1]
    z_scores = (scores - np.mean(scores)) / np.std(scores)
    ax.plot(positions, z_scores, color=colors['line'], linewidth=1.5)
    ax.axhline(y=0, color='gray', linewidth=0.8)
    ax.set_ylabel('Z-score', fontsize=12)
    ax.set_title('Step 2: Z-normalize scores (subtract mean, divide by std)', fontsize=13, fontweight='bold', loc='left')

    # Step 3: Cumulative sum
    ax = axes[2]
    cusum_pos = np.zeros(N)
    for i in range(1, N):
        cusum_pos[i] = max(0, cusum_pos[i-1] + z_scores[i] - 0.5)
    ax.plot(positions, cusum_pos, color=colors['hot'], linewidth=2)
    thresh_c = np.mean(cusum_pos) + 2 * np.std(cusum_pos)
    ax.axhline(y=thresh_c, color='red', linestyle='--', linewidth=1.5)
    ax.fill_between(positions, 0, cusum_pos, where=cusum_pos > thresh_c, color=colors['hot'], alpha=0.3)
    ax.annotate('Threshold', xy=(1.02, thresh_c), xycoords=('axes fraction', 'data'),
                fontsize=10, color='red', va='center', ha='left', fontweight='bold', annotation_clip=False)
    ax.set_ylabel('CUSUM', fontsize=12)
    ax.set_title('Step 3: Cumulative sum rises sharply in hotspot regions', fontsize=13, fontweight='bold', loc='left')

    # Step 4: Detected
    ax = axes[3]
    detected = cusum_pos > thresh_c
    bar_colors = [colors['hot'] if d else colors['bg'] for d in detected]
    ax.bar(positions, scores, width=1.0, color=bar_colors, alpha=0.8, edgecolor='none')
    ax.set_ylabel('Score', fontsize=12)
    ax.set_xlabel('Genomic Position', fontsize=12)
    ax.set_title('Step 4: Change-point regions = detected hotspots (orange)', fontsize=13, fontweight='bold', loc='left')
    ax.set_ylim(0, 1.0)

    for ax in axes:
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.tick_params(labelsize=10)
    fig.tight_layout(pad=1.5)
    fig.savefig(f'{OUT_DIR}/concept_cusum.png', dpi=200, bbox_inches='tight', facecolor='white')
    plt.close(fig)
    print('Saved: concept_cusum.png')


def fig_kde():
    """KDE: 4-step concept diagram."""
    from scipy.stats import gaussian_kde

    fig, axes = plt.subplots(4, 1, figsize=(12, 10), sharex=True)
    colors = {'bg': '#E8E8E8', 'hot': '#55A868', 'line': '#4C72B0', 'kde': '#D62728'}

    # Step 1: Raw score profile
    ax = axes[0]
    ax.bar(positions, scores, width=1.0, color=colors['line'], alpha=0.7, edgecolor='none')
    ax.set_ylabel('Score', fontsize=12)
    ax.set_title('Step 1: Score profile across the genome', fontsize=13, fontweight='bold', loc='left')
    ax.set_ylim(0, 1.0)

    # Step 2: Weight positions by score
    ax = axes[1]
    weighted_pos = []
    for i, s in enumerate(scores):
        weighted_pos.extend([i] * int(s * 100))
    weighted_pos = np.array(weighted_pos) if len(weighted_pos) > 0 else np.array([0])
    ax.hist(weighted_pos, bins=100, color=colors['line'], alpha=0.6, density=True, edgecolor='none')
    ax.set_ylabel('Weighted Density', fontsize=12)
    ax.set_title('Step 2: Weight each position by its score (high score = more weight)', fontsize=13, fontweight='bold', loc='left')

    # Step 3: Fit KDE curve
    ax = axes[2]
    if len(weighted_pos) > 1:
        kde = gaussian_kde(weighted_pos, bw_method=0.03)
        x_kde = np.linspace(0, N, 500)
        density = kde(x_kde)
    else:
        x_kde = np.linspace(0, N, 500)
        density = np.zeros_like(x_kde)
    ax.plot(x_kde, density, color=colors['kde'], linewidth=2)
    thresh_k = np.percentile(density, 90)
    ax.axhline(y=thresh_k, color=colors['hot'], linestyle='--', linewidth=1.5)
    ax.fill_between(x_kde, 0, density, where=density > thresh_k, color=colors['hot'], alpha=0.3)
    ax.annotate('90th percentile', xy=(1.02, thresh_k), xycoords=('axes fraction', 'data'),
                fontsize=10, color=colors['hot'], va='center', ha='left', fontweight='bold', annotation_clip=False)
    ax.set_ylabel('KDE Density', fontsize=12)
    ax.set_title('Step 3: Fit smooth density curve → peaks = candidate hotspots', fontsize=13, fontweight='bold', loc='left')

    # Step 4: Detected
    ax = axes[3]
    kde_at_pos = kde(positions) if len(weighted_pos) > 1 else np.zeros(N)
    detected = kde_at_pos > thresh_k
    bar_colors = [colors['hot'] if d else colors['bg'] for d in detected]
    ax.bar(positions, scores, width=1.0, color=bar_colors, alpha=0.8, edgecolor='none')
    ax.set_ylabel('Score', fontsize=12)
    ax.set_xlabel('Genomic Position', fontsize=12)
    ax.set_title('Step 4: High-density regions = detected hotspots (green)', fontsize=13, fontweight='bold', loc='left')
    ax.set_ylim(0, 1.0)

    for ax in axes:
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.tick_params(labelsize=10)
    fig.tight_layout(pad=1.5)
    fig.savefig(f'{OUT_DIR}/concept_kde.png', dpi=200, bbox_inches='tight', facecolor='white')
    plt.close(fig)
    print('Saved: concept_kde.png')


def fig_bayes():
    """Bayes: 4-step concept diagram."""
    fig, axes = plt.subplots(4, 1, figsize=(12, 10), sharex=True)
    colors = {'bg': '#E8E8E8', 'hot': '#8172B3', 'line': '#4C72B0', 'prior': '#FF7F0E'}

    prior = 0.05  # prior probability of hotspot

    # Step 1: Raw scores
    ax = axes[0]
    ax.bar(positions, scores, width=1.0, color=colors['line'], alpha=0.7, edgecolor='none')
    ax.set_ylabel('Score', fontsize=12)
    ax.set_title('Step 1: Observed scores at each position', fontsize=13, fontweight='bold', loc='left')
    ax.set_ylim(0, 1.0)

    # Step 2: Prior probability
    ax = axes[1]
    ax.axhline(y=prior, color=colors['prior'], linewidth=2)
    ax.fill_between(positions, 0, prior, color=colors['prior'], alpha=0.2)
    ax.set_ylabel('Prior P(hotspot)', fontsize=12)
    ax.set_title(f'Step 2: Set prior probability = {prior} (expect {prior*100:.0f}% of positions are hotspots)',
                 fontsize=13, fontweight='bold', loc='left')
    ax.set_ylim(0, 0.2)

    # Step 3: Posterior probability (Bayes update)
    ax = axes[2]
    # Simple Bayesian: posterior proportional to prior * likelihood(score)
    likelihood = scores / (np.max(scores) + 1e-10)
    posterior = (prior * likelihood) / (prior * likelihood + (1 - prior) * (1 - likelihood + 1e-10))
    ax.plot(positions, posterior, color=colors['hot'], linewidth=2)
    thresh_b = 0.5
    ax.axhline(y=thresh_b, color='red', linestyle='--', linewidth=1.5)
    ax.fill_between(positions, 0, posterior, where=posterior > thresh_b, color=colors['hot'], alpha=0.3)
    ax.annotate('P > 0.5 = hotspot', xy=(1.02, thresh_b), xycoords=('axes fraction', 'data'),
                fontsize=10, color='red', va='center', ha='left', fontweight='bold', annotation_clip=False)
    ax.set_ylabel('Posterior P(hotspot)', fontsize=12)
    ax.set_title('Step 3: Combine prior + observed score → posterior probability', fontsize=13, fontweight='bold', loc='left')
    ax.set_ylim(0, 1.0)

    # Step 4: Detected
    ax = axes[3]
    detected = posterior > thresh_b
    bar_colors = [colors['hot'] if d else colors['bg'] for d in detected]
    ax.bar(positions, scores, width=1.0, color=bar_colors, alpha=0.8, edgecolor='none')
    ax.set_ylabel('Score', fontsize=12)
    ax.set_xlabel('Genomic Position', fontsize=12)
    ax.set_title('Step 4: Posterior > 0.5 = detected hotspots (purple)', fontsize=13, fontweight='bold', loc='left')
    ax.set_ylim(0, 1.0)

    for ax in axes:
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.tick_params(labelsize=10)
    fig.tight_layout(pad=1.5)
    fig.savefig(f'{OUT_DIR}/concept_bayes.png', dpi=200, bbox_inches='tight', facecolor='white')
    plt.close(fig)
    print('Saved: concept_bayes.png')


def fig_ensemble():
    """Ensemble: 4-step concept diagram."""
    fig, axes = plt.subplots(2, 2, figsize=(12, 10))
    colors_methods = ['#4C72B0', '#D62728', '#55A868', '#DD8452']
    color_final = '#8172B3'

    # Simulate 4 sub-detectors with different results
    np.random.seed(123)
    detections = []
    method_names = ['FreqThresh', 'Wavelet', 'DBSCAN', 'SlidingWin']
    for i, name in enumerate(method_names):
        det = np.zeros(N, dtype=bool)
        # Each method detects slightly different regions
        det[58+i*2:77-i] = True
        det[138+i:157-i*2] = True
        # Some false positives unique to each method
        if i == 0: det[30:35] = True
        if i == 1: det[100:103] = True
        if i == 2: det[180:183] = True
        detections.append(det)

    # Step 1-2: Show 4 individual detectors
    for idx in range(4):
        if idx < 2:
            ax = axes[0, idx]
        else:
            ax = axes[1, idx - 2]

        if idx < 3:
            det = detections[idx]
            bar_colors = [colors_methods[idx] if d else '#E8E8E8' for d in det]
            ax.bar(positions, scores, width=1.0, color=bar_colors, alpha=0.7, edgecolor='none')
            ax.set_title(f'Detector {idx+1}: {method_names[idx]}', fontsize=13, fontweight='bold')
            ax.set_ylabel('Score', fontsize=11)
            ax.set_ylim(0, 1.0)
            # Count detections
            n_det = np.sum(det)
            ax.annotate(f'{n_det} positions detected', xy=(0.98, 0.95),
                       xycoords='axes fraction', fontsize=10, ha='right', va='top',
                       color=colors_methods[idx], fontweight='bold')
        else:
            # Step 4: Majority vote (3/4 agree)
            vote_count = np.sum(detections, axis=0)
            majority = vote_count >= 3
            bar_colors = [color_final if m else '#E8E8E8' for m in majority]
            ax.bar(positions, scores, width=1.0, color=bar_colors, alpha=0.8, edgecolor='none')
            ax.set_title('Ensemble: Majority vote (≥3/4 agree)', fontsize=13, fontweight='bold')
            ax.set_ylabel('Score', fontsize=11)
            ax.set_ylim(0, 1.0)
            n_final = np.sum(majority)
            ax.annotate(f'{n_final} positions (false positives removed)',
                       xy=(0.98, 0.95), xycoords='axes fraction', fontsize=10,
                       ha='right', va='top', color=color_final, fontweight='bold')
            for start, end in [(58, 77), (138, 157)]:
                mid = (start + end) / 2
                if any(majority[start:end]):
                    ax.annotate('Hotspot', xy=(mid, 0.88), fontsize=11,
                               ha='center', color=color_final, fontweight='bold')

        ax.set_xlabel('Genomic Position', fontsize=11)
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.tick_params(labelsize=10)

    # Relabel panels
    axes[0, 0].set_title('Step 1: Detector 1 (FreqThresh)', fontsize=13, fontweight='bold')
    axes[0, 1].set_title('Step 2: Detector 2 (Wavelet)', fontsize=13, fontweight='bold')
    axes[1, 0].set_title('Step 3: Detector 3 (DBSCAN)', fontsize=13, fontweight='bold')
    axes[1, 1].set_title('Step 4: Majority vote — only agreed regions kept', fontsize=13, fontweight='bold')

    fig.tight_layout(pad=2.0)
    fig.savefig(f'{OUT_DIR}/concept_ensemble.png', dpi=200, bbox_inches='tight', facecolor='white')
    plt.close(fig)
    print('Saved: concept_ensemble.png')


if __name__ == '__main__':
    print('Generating method concept diagrams...\n')
    fig_freqthresh()
    fig_sliding_window()
    fig_dbscan()
    fig_wavelet()
    fig_cusum()
    fig_kde()
    fig_bayes()
    fig_ensemble()
    print('\nAll 8 concept diagrams generated.')
