"""Regenerate search_space_reduction.png with fixed text positioning."""
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np

fig, ax = plt.subplots(figsize=(10, 5))

strategies = ['Random\nBaseline', 'FreqThresh', 'EqualWeight\n(MutBench-Adapt)', 'Oracle\n(Upper Bound)']
enrichments = [1.0, 1.7, 4.0, 7.8]
colors = ['#C62828', '#9E9E9E', '#1565C0', '#F9A825']

bars = ax.barh(range(len(strategies)), enrichments, color=colors, height=0.6, edgecolor='white')

ax.set_yticks(range(len(strategies)))
ax.set_yticklabels(strategies, fontsize=12, fontweight='bold')
ax.set_xlabel('Enrichment Ratio (Hotspots in Top 10% / Expected)', fontsize=12)
ax.set_title('Search Space Reduction: Hotspot Enrichment in Top-Ranked Positions (H3N2)',
             fontsize=13, fontweight='bold')

# Value labels - placed to the right of bars
for bar, val in zip(bars, enrichments):
    ax.text(bar.get_width() + 0.15, bar.get_y() + bar.get_height()/2,
            f'{val}x', ha='left', va='center', fontsize=13, fontweight='bold',
            color=bar.get_facecolor())

# Dashed line at x=1
ax.axvline(x=1.0, color='gray', linestyle='--', linewidth=1, alpha=0.7)

# Annotation box - moved to upper right, clear of bars
ax.text(0.97, 0.05,
        'Top 10% of positions ranked by each strategy\n'
        'Enrichment = (observed hotspots) / (expected by chance)',
        transform=ax.transAxes, ha='right', va='bottom',
        fontsize=9, fontstyle='italic', color='#555555',
        bbox=dict(boxstyle='round,pad=0.3', facecolor='white',
                  edgecolor='#CCCCCC', alpha=0.9))

ax.set_xlim(0, 9.5)
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)

plt.tight_layout()
plt.savefig('/proj/paper/paper/dissertation/figures/search_space_reduction.png',
            dpi=300, bbox_inches='tight', facecolor='white')
print('Saved: search_space_reduction.png')
plt.close()
