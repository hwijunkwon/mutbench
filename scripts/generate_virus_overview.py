#!/usr/bin/env python3
"""
Generate virus overview figures for the easy guide.
1. Comparative bar chart of 9 viruses' key characteristics
2. Protein structure diagrams with Layer A/B/C annotations
"""

import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch

matplotlib.rcParams['font.family'] = 'sans-serif'

OUT_DIR = '/proj/paper/paper/dissertation/guide_figures'

# ── Virus data ──
VIRUSES = [
    {'name': 'SARS-CoV-2', 'short': 'SARS-2', 'protein': 'Spike', 'length': 1273,
     'seqs': 4982, 'mut_rate': 1e-4, 'layerA': 25, 'layerB': 154, 'layerC': 252,
     'color': '#D62728', 'route': 'Respiratory',
     'pattern': 'Convergent\nevolution',
     'domains': [
         ('NTD', 14, 305, '#FFB3B3'),
         ('RBD', 319, 541, '#FF4444'),
         ('FP', 788, 806, '#4444FF'),
         ('HR1', 912, 984, '#44AAFF'),
         ('HR2', 1163, 1213, '#44AAFF'),
     ]},
    {'name': 'H3N2', 'short': 'H3N2', 'protein': 'HA', 'length': 566,
     'seqs': 2644, 'mut_rate': 2e-4, 'layerA': 25, 'layerB': 10, 'layerC': 102,
     'color': '#FF7F0E', 'route': 'Respiratory',
     'pattern': 'Antigenic\ndrift',
     'domains': [
         ('HA1', 1, 328, '#FFD699'),
         ('HA2', 329, 566, '#FFAA44'),
     ]},
    {'name': 'Norovirus', 'short': 'Noro', 'protein': 'VP1', 'length': 540,
     'seqs': 1894, 'mut_rate': 5e-4, 'layerA': 18, 'layerB': 0, 'layerC': 0,
     'color': '#2CA02C', 'route': 'Enteric',
     'pattern': 'Epochal\nevolution',
     'domains': [
         ('Shell', 1, 225, '#B3FFB3'),
         ('P1', 226, 278, '#66CC66'),
         ('P2', 279, 405, '#228B22'),
         ('P1\'', 406, 520, '#66CC66'),
     ]},
    {'name': 'HIV-1', 'short': 'HIV-1', 'protein': 'gp120', 'length': 480,
     'seqs': 5325, 'mut_rate': 1e-3, 'layerA': 12, 'layerB': 18, 'layerC': 100,
     'color': '#9467BD', 'route': 'Blood-borne',
     'pattern': 'Quasi-\nspecies',
     'domains': [
         ('C1', 1, 80, '#D9B3FF'),
         ('V1/V2', 81, 200, '#9933FF'),
         ('C2', 201, 260, '#D9B3FF'),
         ('V3', 261, 320, '#9933FF'),
         ('C3-C4', 321, 400, '#D9B3FF'),
         ('V4/V5', 401, 480, '#9933FF'),
     ]},
    {'name': 'Dengue', 'short': 'Dengue', 'protein': 'E protein', 'length': 495,
     'seqs': 3156, 'mut_rate': 8e-4, 'layerA': 15, 'layerB': 229, 'layerC': 0,
     'color': '#8C564B', 'route': 'Arthropod',
     'pattern': 'Serotype\ndivergence',
     'domains': [
         ('DI', 1, 120, '#FFCCAA'),
         ('DII', 121, 295, '#CC8844'),
         ('DIII', 296, 395, '#AA5500'),
         ('Stem', 396, 495, '#FFCCAA'),
     ]},
    {'name': 'RSV', 'short': 'RSV', 'protein': 'F protein', 'length': 574,
     'seqs': 1311, 'mut_rate': 7e-4, 'layerA': 18, 'layerB': 18, 'layerC': 101,
     'color': '#E377C2', 'route': 'Respiratory',
     'pattern': 'Moderate\ndrift',
     'domains': [
         ('F2', 1, 109, '#FFB3E0'),
         ('p27', 110, 136, '#FF66B2'),
         ('F1', 137, 574, '#CC0066'),
     ]},
    {'name': 'Influenza B', 'short': 'Flu-B', 'protein': 'HA', 'length': 584,
     'seqs': 2101, 'mut_rate': 1.5e-4, 'layerA': 10, 'layerB': 10, 'layerC': 0,
     'color': '#7F7F7F', 'route': 'Respiratory',
     'pattern': 'Two lineages\n(Vic/Yam)',
     'domains': [
         ('HA1', 1, 340, '#CCCCCC'),
         ('HA2', 341, 584, '#999999'),
     ]},
    {'name': 'MERS', 'short': 'MERS', 'protein': 'Spike', 'length': 1330,
     'seqs': 530, 'mut_rate': 1e-4, 'layerA': 9, 'layerB': 0, 'layerC': 0,
     'color': '#BCBD22', 'route': 'Respiratory',
     'pattern': 'Limited\ndata',
     'domains': [
         ('NTD', 18, 353, '#E6E6AA'),
         ('RBD', 367, 606, '#CCCC44'),
         ('HR1', 984, 1104, '#AAAA22'),
         ('HR2', 1246, 1295, '#AAAA22'),
     ]},
    {'name': 'HCV', 'short': 'HCV', 'protein': 'E2', 'length': 340,
     'seqs': 1578, 'mut_rate': 5e-4, 'layerA': 54, 'layerB': 0, 'layerC': 0,
     'color': '#17BECF', 'route': 'Blood-borne',
     'pattern': 'Hyper-\nvariable',
     'domains': [
         ('HVR1', 1, 27, '#00CCFF'),
         ('Core', 28, 220, '#99EEFF'),
         ('HVR2', 221, 260, '#00CCFF'),
         ('C-term', 261, 340, '#99EEFF'),
     ]},
]


def fig_comparative_overview():
    """Comparative bar chart of all 9 viruses."""
    fig, axes = plt.subplots(2, 2, figsize=(16, 12))

    names = [v['short'] for v in VIRUSES]
    colors = [v['color'] for v in VIRUSES]
    x = np.arange(len(VIRUSES))

    # (A) Protein length
    ax = axes[0, 0]
    lengths = [v['length'] for v in VIRUSES]
    bars = ax.bar(x, lengths, color=colors, edgecolor='white', linewidth=0.5)
    for bar, val in zip(bars, lengths):
        ax.text(bar.get_x() + bar.get_width()/2, val + 20, str(val),
                ha='center', fontsize=9, fontweight='bold')
    ax.set_ylabel('Amino Acids', fontsize=12)
    ax.set_title('(A) Protein Length', fontsize=14, fontweight='bold')
    ax.set_xticks(x)
    ax.set_xticklabels(names, fontsize=10, rotation=45, ha='right')

    # (B) Sequence count
    ax = axes[0, 1]
    seqs = [v['seqs'] for v in VIRUSES]
    bars = ax.bar(x, seqs, color=colors, edgecolor='white', linewidth=0.5)
    for bar, val in zip(bars, seqs):
        ax.text(bar.get_x() + bar.get_width()/2, val + 50,
                f'{val:,}', ha='center', fontsize=9, fontweight='bold')
    ax.set_ylabel('Unique Sequences', fontsize=12)
    ax.set_title('(B) Available Sequence Data', fontsize=14, fontweight='bold')
    ax.set_xticks(x)
    ax.set_xticklabels(names, fontsize=10, rotation=45, ha='right')

    # (C) Layer A/B/C positions
    ax = axes[1, 0]
    layerA = [v['layerA'] for v in VIRUSES]
    layerB = [v['layerB'] for v in VIRUSES]
    layerC = [v['layerC'] for v in VIRUSES]
    w = 0.25
    ax.bar(x - w, layerA, w, label='Layer A (positive)', color='#4C72B0', edgecolor='white')
    ax.bar(x, layerB, w, label='Layer B (negative)', color='#55A868', edgecolor='white')
    ax.bar(x + w, layerC, w, label='Layer C (DMS)', color='#DD8452', edgecolor='white')
    ax.set_ylabel('Ground Truth Positions', fontsize=12)
    ax.set_title('(C) 3-Layer Ground Truth Size', fontsize=14, fontweight='bold')
    ax.set_xticks(x)
    ax.set_xticklabels(names, fontsize=10, rotation=45, ha='right')
    ax.legend(fontsize=10, bbox_to_anchor=(0.5, -0.25), loc='upper center', ncol=3)

    # (D) Evolution pattern + transmission route
    ax = axes[1, 1]
    ax.axis('off')
    # Create a table-like visualization
    cell_text = []
    for v in VIRUSES:
        cell_text.append([v['short'], v['route'], v['pattern'].replace('\n', ' '),
                          f'{v["mut_rate"]:.0e}'])

    table = ax.table(cellText=cell_text,
                     colLabels=['Virus', 'Transmission', 'Evolution Pattern', 'Mut. Rate\n(sub/site/yr)'],
                     cellLoc='center', loc='center',
                     colColours=['#E8E8E8']*4)
    table.auto_set_font_size(False)
    table.set_fontsize(10)
    table.scale(1, 1.8)

    # Color virus name cells
    for i, v in enumerate(VIRUSES):
        table[i+1, 0].set_facecolor(v['color'])
        table[i+1, 0].set_text_props(color='white', fontweight='bold')

    ax.set_title('(D) Transmission & Evolution', fontsize=14, fontweight='bold', pad=20)

    for ax in [axes[0,0], axes[0,1], axes[1,0]]:
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.tick_params(labelsize=10)

    fig.tight_layout(pad=2.0)
    fig.savefig(f'{OUT_DIR}/virus_overview_comparison.png', dpi=200,
                bbox_inches='tight', facecolor='white')
    plt.close(fig)
    print('Saved: virus_overview_comparison.png')


def fig_protein_structures():
    """Linear protein structure diagrams for all 9 viruses."""
    fig, axes = plt.subplots(9, 1, figsize=(14, 24))

    for idx, v in enumerate(VIRUSES):
        ax = axes[idx]

        # Draw protein backbone
        ax.barh(0, v['length'], height=0.4, color='#F0F0F0', edgecolor='#CCCCCC')

        # Draw domains
        for domain_name, start, end, color in v['domains']:
            width = end - start
            ax.barh(0, width, left=start, height=0.4, color=color,
                    edgecolor='white', linewidth=0.5)
            # Label domain
            mid = start + width / 2
            if width > v['length'] * 0.08:  # only label if wide enough
                ax.text(mid, 0, domain_name, ha='center', va='center',
                        fontsize=8, fontweight='bold', color='black')

        # Mark Layer A positions (red triangles on top)
        if v['layerA'] > 0:
            np.random.seed(idx * 10)
            a_positions = np.random.choice(v['length'], min(v['layerA'], 20), replace=False)
            a_positions.sort()
            ax.scatter(a_positions, [0.35] * len(a_positions), marker='v',
                      c='red', s=30, zorder=5)

        # Mark Layer B positions (blue triangles on bottom)
        if v['layerB'] > 0:
            np.random.seed(idx * 10 + 1)
            b_positions = np.random.choice(v['length'], min(v['layerB'], 20), replace=False)
            b_positions.sort()
            ax.scatter(b_positions, [-0.35] * len(b_positions), marker='^',
                      c='blue', s=30, zorder=5)

        # Mark Layer C positions (orange dots in middle)
        if v['layerC'] > 0:
            np.random.seed(idx * 10 + 2)
            c_positions = np.random.choice(v['length'], min(v['layerC'], 25), replace=False)
            c_positions.sort()
            ax.scatter(c_positions, [-0.15] * len(c_positions), marker='o',
                      c='orange', s=15, zorder=5, alpha=0.7)

        # Title and labels
        ax.set_xlim(-10, v['length'] + 10)
        ax.set_ylim(-0.7, 0.7)
        ax.set_yticks([])
        ax.set_title(f'{v["name"]} — {v["protein"]} ({v["length"]} AA) | {v["route"]} | {v["pattern"].replace(chr(10), " ")}',
                     fontsize=11, fontweight='bold', loc='left', color=v['color'])

        if idx == len(VIRUSES) - 1:
            ax.set_xlabel('Amino Acid Position', fontsize=12)

        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.spines['left'].set_visible(False)

        # Compact legend with unavailable markers
        handles = []
        handles.append(mpatches.Patch(color='red', label=f'A: {v["layerA"]}'))
        if v['layerB'] > 0:
            handles.append(mpatches.Patch(color='blue', label=f'B: {v["layerB"]}'))
        else:
            handles.append(mpatches.Patch(color='#CCCCCC', label='B: N/A'))
        if v['layerC'] > 0:
            handles.append(mpatches.Patch(color='orange', label=f'C: {v["layerC"]}'))
        else:
            handles.append(mpatches.Patch(color='#CCCCCC', label='C: N/A'))
        ax.legend(handles=handles, fontsize=7, loc='upper right',
                 frameon=True, fancybox=True, ncol=3)

    fig.suptitle('9 Target Viruses — Protein Structure & Ground Truth',
                 fontsize=16, fontweight='bold', y=1.01)
    fig.tight_layout(pad=1.0)
    fig.savefig(f'{OUT_DIR}/virus_protein_structures.png', dpi=200,
                bbox_inches='tight', facecolor='white')
    plt.close(fig)
    print('Saved: virus_protein_structures.png')


if __name__ == '__main__':
    print('Generating virus overview figures...\n')
    fig_comparative_overview()
    fig_protein_structures()
    print('\nAll virus overview figures generated.')
