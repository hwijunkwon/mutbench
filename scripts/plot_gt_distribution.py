"""Plot 3-layer ground truth position distribution for all 11 pathogens.
Layer C (DMS) positions shown as orange bars, same style as A/B.
"""

import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np
import pandas as pd
import sys
sys.path.insert(0, "/proj/paper")

from tools.mutbench.ground_truth.multilayer_gt import get_gt_adaptive, get_gt_constrained

PATHOGENS = [
    ("SARS-CoV-2", "Spike", 1259, "sars2_dms.csv"),
    ("H3N2", "HA", 543, "h3n2_dms.csv"),
    ("Norovirus", "VP1", 536, None),
    ("HIV-1", "Env gp120", 450, "hiv1_dms.csv"),
    ("Dengue", "E protein", 490, None),
    ("RSV", "F protein", 550, "rsv_dms_new.csv"),
    ("Influenza B", "HA", 560, None),
    ("MERS", "Spike", 1330, None),
    ("HCV", "E2", 340, None),
    ("Rabies", "G protein", 524, "rabies_dms.csv"),
    ("EV-A71", "VP1", 297, "eva71_vp1_dms.csv"),
]

CODE_NAMES = {
    "SARS-CoV-2": "SARS-CoV-2", "H3N2": "H3N2", "Norovirus": "Norovirus",
    "HIV-1": "HIV-1", "Dengue": "Dengue", "RSV": "RSV",
    "Influenza B": "Influenza_B", "MERS": "MERS", "HCV": "HCV",
    "Rabies": "Rabies", "EV-A71": "EV-A71",
}

DMS_DIR = "/proj/paper/results/mutbench/dms_data"

def load_layer_c(dms_file, max_len):
    """Load Layer C positions from DMS CSV."""
    if dms_file is None:
        return set()
    df = pd.read_csv(f"{DMS_DIR}/{dms_file}")
    if "layer_c" in df.columns:
        positions = set(df[df["layer_c"] == 1]["position"].values)
    else:
        # Fallback: top 20% fitness
        threshold = np.percentile(df["fitness_score"], 80)
        positions = set(df[df["fitness_score"] >= threshold]["position"].values)
    return {p for p in positions if p < max_len}


fig, axes = plt.subplots(11, 1, figsize=(12, 13))
fig.suptitle("3-Layer Ground Truth Position Distribution (11 Pathogens)",
             fontsize=13, fontweight="bold", y=0.99)

colors = {"A": "#1565C0", "B": "#2E7D32", "C": "#E65100"}

for i, (name, protein, aln_len, dms_file) in enumerate(PATHOGENS):
    ax = axes[i]
    code_name = CODE_NAMES[name]
    layer_a = sorted(get_gt_adaptive(code_name, aln_len))
    layer_b = sorted(get_gt_constrained(code_name, aln_len))
    layer_c = sorted(load_layer_c(dms_file, aln_len))

    ax.set_xlim(0, aln_len)

    # Three rows: Layer A (top), Layer B (middle), Layer C (bottom)
    row_a = 0.35
    row_b = 0.0
    row_c = -0.35
    bar_h = 0.28

    # Gray backbones for each row
    for row in [row_a, row_b, row_c]:
        ax.barh(row, aln_len, height=bar_h, color="#F0F0F0", edgecolor="#DDDDDD",
                linewidth=0.2, left=0)

    # Layer A (blue)
    for pos in layer_a:
        ax.barh(row_a, 1, height=bar_h, color=colors["A"], edgecolor="none",
                left=pos, alpha=0.9)

    # Layer B (green)
    for pos in layer_b:
        ax.barh(row_b, 1, height=bar_h, color=colors["B"], edgecolor="none",
                left=pos, alpha=0.8)

    # Layer C (orange) — same style as A/B
    if layer_c:
        for pos in layer_c:
            ax.barh(row_c, 1, height=bar_h, color=colors["C"], edgecolor="none",
                    left=pos, alpha=0.8)

    # Counts
    a_count = len(layer_a)
    b_count = len(layer_b)
    c_count = len(layer_c) if layer_c else "---"
    counts = f"A:{a_count}  B:{b_count}  C:{c_count}"

    # Left label
    ax.set_yticks([0])
    ax.set_yticklabels([f"{name}\n({protein}, {aln_len} AA)"],
                       fontsize=7.5, fontweight="bold")
    ax.tick_params(axis="y", length=0, pad=5)

    # Right counts
    ax.text(1.02, 0.5, counts, transform=ax.transAxes, ha="left", va="center",
            fontsize=6.5, color="#333333", family="monospace")

    # No row labels on far left to avoid overlap with pathogen name

    ax.set_ylim(-0.55, 0.55)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.spines["left"].set_visible(False)

    tick_step = 50 if aln_len < 400 else 100 if aln_len < 700 else 200
    ax.set_xticks(range(0, aln_len + 1, tick_step))
    ax.tick_params(axis="x", labelsize=5.5, pad=1)
    if i == 10:
        ax.set_xlabel("Amino Acid Position (0-based)", fontsize=9)
    ax.spines["bottom"].set_linewidth(0.3)

plt.subplots_adjust(left=0.20, right=0.88, top=0.95, bottom=0.05, hspace=0.55)

# Legend
legend_patches = [
    mpatches.Patch(color=colors["A"], label="Layer A: Convergent Evolution (TP)"),
    mpatches.Patch(color=colors["B"], label="Layer B: Purifying Selection (TN)"),
    mpatches.Patch(color=colors["C"], label="Layer C: DMS Functional Sites"),
    mpatches.Patch(color="#F0F0F0", edgecolor="#DDDDDD",
                   label="Non-annotated positions"),
]
fig.legend(handles=legend_patches, loc="lower center", ncol=4, fontsize=7.5,
           bbox_to_anchor=(0.55, -0.01))

plt.savefig("/proj/paper/paper/dissertation/figures/gt_distribution_11pathogens.png",
            dpi=300, bbox_inches="tight")
print("Saved: gt_distribution_11pathogens.png")
plt.close()
