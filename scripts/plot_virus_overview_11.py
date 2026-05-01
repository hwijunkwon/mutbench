"""Generate 4-panel virus overview comparison for 11 pathogens (v1 style)."""

import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np

PATHOGENS = [
    ("SARS-CoV-2", 1259, 753, 25, 154, 252, "Respiratory", "Convergent evolution", "~2 yr"),
    ("H3N2", 543, 2562, 25, 10, 102, "Respiratory", "Antigenic drift", "~50 yr"),
    ("Norovirus", 536, 791, 15, 229, 0, "Enteric", "Epochal evolution", "~20 yr"),
    ("HIV-1", 450, 2256, 26, 23, 100, "Blood-borne", "Quasispecies", "~30 yr"),
    ("Dengue", 490, 796, 24, 24, 0, "Arthropod", "Serotype cycling", "~20 yr"),
    ("RSV", 550, 4779, 20, 18, 101, "Respiratory", "Limited drift", "~10 yr"),
    ("Flu-B", 560, 5019, 17, 10, 0, "Respiratory", "Vic/Yam lineages", "~10 yr"),
    ("MERS", 1330, 530, 9, 110, 0, "Respiratory", "Zoonotic spillover", "~5 yr"),
    ("HCV", 340, 1067, 54, 0, 0, "Blood-borne", "Hypervariable", "~30 yr"),
    ("Rabies", 524, 2038, 39, 42, 87, "Neurotropic", "Slow/conserved", "~50 yr"),
    ("EV-A71", 297, 662, 27, 29, 55, "Neurotropic", "Genotype switching", "~20 yr"),
]

names = [p[0] for p in PATHOGENS]
lengths = [p[1] for p in PATHOGENS]
seqs = [p[2] for p in PATHOGENS]
layer_a = [p[3] for p in PATHOGENS]
layer_b = [p[4] for p in PATHOGENS]
layer_c = [p[5] for p in PATHOGENS]

# Colors by transmission route
route_colors = {
    "Respiratory": "#E53935",
    "Blood-borne": "#8E24AA",
    "Enteric": "#43A047",
    "Arthropod": "#FB8C00",
    "Neurotropic": "#1E88E5",
}
colors = [route_colors[p[6]] for p in PATHOGENS]

fig, axes = plt.subplots(2, 2, figsize=(14, 10))
fig.suptitle("11 Pathogens: Data Characteristics Overview", fontsize=14, fontweight="bold")

x = np.arange(len(names))

# (A) Protein Length
ax = axes[0, 0]
bars = ax.bar(x, lengths, color=colors, edgecolor="white", linewidth=0.5)
ax.set_ylabel("Amino Acids", fontsize=10)
ax.set_title("(A) Protein Length", fontsize=12, fontweight="bold")
ax.set_xticks(x)
ax.set_xticklabels(names, rotation=45, ha="right", fontsize=8)
for bar, val in zip(bars, lengths):
    ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 15,
            str(val), ha="center", va="bottom", fontsize=7, fontweight="bold")

# (B) Available Sequence Data
ax = axes[0, 1]
bars = ax.bar(x, seqs, color=colors, edgecolor="white", linewidth=0.5)
ax.set_ylabel("Unique Sequences", fontsize=10)
ax.set_title("(B) Available Sequence Data", fontsize=12, fontweight="bold")
ax.set_xticks(x)
ax.set_xticklabels(names, rotation=45, ha="right", fontsize=8)
for bar, val in zip(bars, seqs):
    ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 30,
            f"{val:,}", ha="center", va="bottom", fontsize=7, fontweight="bold")

# (C) 3-Layer Ground Truth Size
ax = axes[1, 0]
w = 0.25
ax.bar(x - w, layer_a, width=w, color="#1565C0", label="Layer A (positive)")
ax.bar(x, layer_b, width=w, color="#2E7D32", label="Layer B (negative)")
ax.bar(x + w, layer_c, width=w, color="#E65100", label="Layer C (DMS)")
ax.set_ylabel("Ground Truth Positions", fontsize=10)
ax.set_title("(C) 3-Layer Ground Truth Size", fontsize=12, fontweight="bold")
ax.set_xticks(x)
ax.set_xticklabels(names, rotation=45, ha="right", fontsize=8)
ax.legend(fontsize=8, loc="upper right")

# (D) Transmission & Evolution table
ax = axes[1, 1]
ax.axis("off")
ax.set_title("(D) Transmission & Evolution", fontsize=12, fontweight="bold")

col_labels = ["Virus", "Transmission", "Evolution", "Time Span"]
cell_data = [[p[0], p[6], p[7], p[8]] for p in PATHOGENS]
cell_colors = [[route_colors[p[6]]+"30" if i == 0 else "white"
                for i in range(4)] for p in PATHOGENS]

table = ax.table(cellText=cell_data, colLabels=col_labels,
                 cellColours=cell_colors, loc="center",
                 cellLoc="center", colColours=["#E0E0E0"]*4)
table.auto_set_font_size(False)
table.set_fontsize(7.5)
table.scale(1.0, 1.3)

# Header bold
for (row, col), cell in table.get_celld().items():
    if row == 0:
        cell.set_text_props(fontweight="bold", fontsize=8)
    # Color virus name column
    if col == 0 and row > 0:
        cell.set_text_props(fontweight="bold", color=colors[row-1])

plt.tight_layout(rect=[0, 0, 1, 0.96])
plt.savefig("/proj/paper/paper/dissertation/guide_figures/virus_overview_comparison_v2.png",
            dpi=300, bbox_inches="tight")
print("Saved: guide_figures/virus_overview_comparison_v2.png")
plt.close()
