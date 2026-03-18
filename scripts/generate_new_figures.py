#!/usr/bin/env python3
"""
Generate new figures for the dissertation.
Figure 1: Region-Overlap MCC Bar Chart (for Chapter 5)
"""

import pandas as pd
import matplotlib.pyplot as plt
import matplotlib
import numpy as np

matplotlib.rcParams['font.family'] = 'sans-serif'
matplotlib.rcParams['axes.grid'] = True
matplotlib.rcParams['grid.alpha'] = 0.3


def generate_region_overlap_bar():
    """
    Region-Overlap MCC Bar Chart.
    9 pathogens on x-axis, 3 grouped bars (Exact, +/-5, +/-10) per pathogen.
    """
    csv_path = '/proj/paper/results/mutbench/region_overlap_mcc.csv'
    df = pd.read_csv(csv_path)

    # Pathogen order (fixed)
    PATHOGENS = ['SARS-CoV-2', 'H3N2', 'Norovirus', 'HIV-1', 'Dengue',
                 'RSV', 'Influenza_B', 'MERS', 'HCV']

    # Extract one row per pathogen (the oracle/best combo per pathogen)
    data = []
    for p in PATHOGENS:
        row = df[df['pathogen'] == p].iloc[0]
        data.append({
            'pathogen': p,
            'Exact': row['mcc_exact'],
            '±5': row['mcc_window_5'],
            '±10': row['mcc_window_10'],
        })
    plot_df = pd.DataFrame(data)

    # Display labels
    label_map = {
        'SARS-CoV-2': 'SARS-CoV-2', 'H3N2': 'H3N2', 'Norovirus': 'Noro',
        'HIV-1': 'HIV-1', 'Dengue': 'Dengue', 'RSV': 'RSV',
        'Influenza_B': 'Flu-B', 'MERS': 'MERS', 'HCV': 'HCV'
    }

    fig, ax = plt.subplots(figsize=(14, 7), constrained_layout=True)

    x = np.arange(len(PATHOGENS))
    width = 0.25
    colors = ['#4C72B0', '#55A868', '#DD8452']
    labels_bar = ['Exact', '±5', '±10']

    for i, (col, color, label) in enumerate(zip(['Exact', '±5', '±10'], colors, labels_bar)):
        bars = ax.bar(x + (i - 1) * width, plot_df[col], width,
                      label=label, color=color, edgecolor='white', linewidth=0.5)
        # Add value annotations on top of bars
        for bar_item in bars:
            height = bar_item.get_height()
            ax.annotate(f'{height:.3f}',
                        xy=(bar_item.get_x() + bar_item.get_width() / 2, height),
                        xytext=(0, 3), textcoords='offset points',
                        ha='center', va='bottom', fontsize=9, rotation=45)

    # Mean lines
    for i, (col, color) in enumerate(zip(['Exact', '±5', '±10'], colors)):
        mean_val = plot_df[col].mean()
        ax.axhline(y=mean_val, color=color, linestyle='--', alpha=0.5, linewidth=1.0)
        ax.text(len(PATHOGENS) - 0.3, mean_val + 0.01,
                f'Mean={mean_val:.3f}', color=color, fontsize=10, ha='right')

    ax.set_xlabel('Pathogen', fontsize=14)
    ax.set_ylabel('MCC', fontsize=14)
    ax.set_title('Region-Overlap MCC by Pathogen and Evaluation Window', fontsize=14, fontweight='bold')
    ax.set_xticks(x)
    ax.set_xticklabels([label_map[p] for p in PATHOGENS], fontsize=12)
    ax.tick_params(axis='y', labelsize=12)
    ax.legend(fontsize=12, title='Window', title_fontsize=12, loc='upper left')
    ax.set_ylim(0, 1.15)

    # Remove top/right spines
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)

    out_path = '/proj/paper/results/mutbench/region_overlap_bar.png'
    fig.savefig(out_path, dpi=300, bbox_inches='tight')
    plt.close(fig)
    print(f'Saved: {out_path}')


if __name__ == '__main__':
    generate_region_overlap_bar()
