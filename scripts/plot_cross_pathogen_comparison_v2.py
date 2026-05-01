"""Regenerate cross_pathogen_comparison.png with 11 pathogens, 20 scoring types."""
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

df = pd.read_csv('/proj/paper/results/mutbench/stage3_full_results.csv')

# For each pathogen, get the top 5 scoring types by mean MCC
pathogens = ['SARS-CoV-2', 'H3N2', 'Norovirus', 'HIV-1', 'Dengue',
             'RSV', 'Influenza_B', 'MERS', 'HCV', 'Rabies', 'EV-A71']

# Get top 5 scoring types globally (by mean MCC across all pathogens)
global_top = df.groupby('scoring')['mcc'].mean().nlargest(5).index.tolist()

# Nice labels
label_map = {
    'freq': 'Frequency',
    'entropy': 'Entropy',
    'homoplasy': 'Homoplasy',
    'fubar_bf': 'FUBAR BF',
    'esm2_llr': 'ESM-2 LLR',
    'tranception': 'Tranception',
    'plddt_inv': 'pLDDT inv',
    'semantic_change': 'Semantic',
    'stability': 'Stability',
    'dnds_proxy': 'dN/dS',
    'rare_freq': 'Rare freq',
    'EqualWeight': 'EqualWeight',
    'EVEscape_composite': 'EVEscape',
    'entropy_with_indel': 'Entropy+indel',
    'freq_with_indel': 'Freq+indel',
    'fubar': 'FUBAR prob',
    'fubar_pos_sel': 'FUBAR pos',
    'grantham': 'Grantham',
    'sasa': 'SASA',
    'stability_structural': 'Stab.struct',
}

colors = ['#1565C0', '#E53935', '#43A047', '#8E24AA', '#FB8C00']

fig, axes = plt.subplots(4, 3, figsize=(14, 14))
fig.suptitle('Cross-Pathogen MCC Comparison (11 Pathogens, Top 5 Scoring Types)',
             fontsize=14, fontweight='bold')

for idx, pathogen in enumerate(pathogens):
    row, col = idx // 3, idx % 3
    ax = axes[row, col]

    sub = df[df['pathogen'] == pathogen]

    # Mean MCC per scoring type, get top 5 for THIS pathogen
    scoring_mcc = sub.groupby('scoring')['mcc'].mean().sort_values(ascending=True)
    top5 = scoring_mcc.nlargest(5).sort_values()

    bars = ax.barh(range(len(top5)), top5.values, color=colors[:len(top5)], height=0.6)

    labels = [label_map.get(s, s) for s in top5.index]
    ax.set_yticks(range(len(top5)))
    ax.set_yticklabels(labels, fontsize=8)
    ax.set_title(pathogen, fontsize=11, fontweight='bold')
    ax.set_xlim(-0.1, max(0.7, top5.max() * 1.2))

    # Value labels
    for bar, val in zip(bars, top5.values):
        ax.text(val + 0.01, bar.get_y() + bar.get_height()/2,
                f'{val:.3f}', va='center', fontsize=7)

    ax.axvline(x=0, color='gray', linewidth=0.8, linestyle='--', alpha=0.5)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.tick_params(axis='x', labelsize=7)

# Hide unused panel
axes[3, 2].axis('off')

plt.tight_layout(rect=[0, 0, 1, 0.95])
plt.savefig('/proj/paper/paper/dissertation/figures/cross_pathogen_comparison.png',
            dpi=300, bbox_inches='tight', facecolor='white')
print('Saved: cross_pathogen_comparison.png (11 pathogens, 20 scoring)')
plt.close()
