#!/usr/bin/env python3
"""
Stage 3 Full Benchmark Statistical Analysis & Figure Generation
===============================================================
Reads: stage3_full_results.csv (7,683 evaluations)
       fairness_analysis.csv
       layer_c_evaluation.csv

Outputs:
  - 7 publication figures
  - stage3_statistics.csv
  - Console printout of all key numbers
"""

import os
import warnings
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import seaborn as sns
from scipy import stats
from itertools import product

warnings.filterwarnings("ignore")

# ── Paths ──────────────────────────────────────────────────────────────
BASE = "/proj/paper"
RESULTS = os.path.join(BASE, "results/mutbench")
FIG_DIR = os.path.join(BASE, "paper/figure")
FIG_DIR2 = os.path.join(BASE, "paper/dissertation/figures")
os.makedirs(FIG_DIR, exist_ok=True)
os.makedirs(FIG_DIR2, exist_ok=True)

# ── Load data ──────────────────────────────────────────────────────────
df = pd.read_csv(os.path.join(RESULTS, "stage3_full_results.csv"))
fairness = pd.read_csv(os.path.join(RESULTS, "fairness_analysis.csv"))
layer_c = pd.read_csv(os.path.join(RESULTS, "layer_c_evaluation.csv"))

print(f"Loaded {len(df)} evaluations: {df['scoring'].nunique()} scorings × "
      f"{df['family'].nunique()} families × {df['pathogen'].nunique()} pathogens")
print(f"Fairness: {len(fairness)} pathogens, Layer C: {len(layer_c)} rows")

# ── Scoring categories ─────────────────────────────────────────────────
SCORING_CATEGORY = {
    "freq": "Frequency",
    "freq_with_indel": "Frequency",
    "rare_freq": "Frequency",
    "entropy": "MSA",
    "entropy_with_indel": "MSA",
    "homoplasy": "MSA",
    "fubar": "Phylo",
    "fubar_pos_sel": "Phylo",
    "fubar_bf": "Phylo",
    "dnds_proxy": "Phylo",
    "grantham": "Structure",
    "sasa": "Structure",
    "plddt_inv": "Structure",
    "stability": "AI",
    "stability_structural": "AI",
    "esm2_llr": "AI",
    "tranception": "AI",
    "semantic_change": "AI",
    "EVEscape_composite": "Composite",
    "EqualWeight": "Composite",
}

df["scoring_category"] = df["scoring"].map(SCORING_CATEGORY)

# ══════════════════════════════════════════════════════════════════════
# 1. THREE-WAY ANOVA  (scoring × family × pathogen)
# ══════════════════════════════════════════════════════════════════════
print("\n" + "=" * 70)
print("1. THREE-WAY ANOVA  (Type II, omega-squared)")
print("=" * 70)


def omega_squared_manual(df_data, factors, dv="mcc"):
    """
    Compute omega-squared for main effects and all 2-way interactions
    via manual sum-of-squares decomposition (Type II-like).
    """
    grand_mean = df_data[dv].mean()
    ss_total = ((df_data[dv] - grand_mean) ** 2).sum()
    N = len(df_data)

    results = {}

    # Main effects
    for f in factors:
        group_means = df_data.groupby(f)[dv].mean()
        group_counts = df_data.groupby(f)[dv].count()
        ss = sum(group_counts[g] * (group_means[g] - grand_mean) ** 2
                 for g in group_means.index)
        k = df_data[f].nunique()
        ms_resid = _ms_residual(df_data, factors, dv)
        omega2 = (ss - (k - 1) * ms_resid) / (ss_total + ms_resid)
        omega2 = max(0, omega2)
        results[f] = {"SS": ss, "df": k - 1, "omega2": omega2}

    # 2-way interactions
    from itertools import combinations
    for f1, f2 in combinations(factors, 2):
        cell_means = df_data.groupby([f1, f2])[dv].mean()
        cell_counts = df_data.groupby([f1, f2])[dv].count()
        f1_means = df_data.groupby(f1)[dv].mean()
        f2_means = df_data.groupby(f2)[dv].mean()

        ss_interaction = 0
        for (a, b), mean_ab in cell_means.items():
            n_ab = cell_counts.get((a, b), 0)
            expected = f1_means[a] + f2_means[b] - grand_mean
            ss_interaction += n_ab * (mean_ab - expected) ** 2

        k1, k2 = df_data[f1].nunique(), df_data[f2].nunique()
        df_int = (k1 - 1) * (k2 - 1)
        ms_resid = _ms_residual(df_data, factors, dv)
        omega2 = (ss_interaction - df_int * ms_resid) / (ss_total + ms_resid)
        omega2 = max(0, omega2)
        results[f"{f1}×{f2}"] = {"SS": ss_interaction, "df": df_int, "omega2": omega2}

    # Residual
    ss_model = sum(r["SS"] for r in results.values())
    ss_resid = ss_total - ss_model
    df_resid = N - 1 - sum(r["df"] for r in results.values())
    results["Residual"] = {"SS": ss_resid, "df": df_resid, "omega2": 0}

    return results


def _ms_residual(df_data, factors, dv="mcc"):
    """Estimate MS_residual from cell-level residuals."""
    cells = df_data.groupby(factors)[dv]
    ss_within = sum(((g - g.mean()) ** 2).sum() for _, g in cells)
    df_within = len(df_data) - len(cells)
    if df_within <= 0:
        return 0.001
    return ss_within / df_within


anova_results = omega_squared_manual(df, ["scoring", "family", "pathogen"])

stats_rows = []
print(f"\n{'Source':<30} {'SS':>10} {'df':>6} {'ω²':>8}")
print("-" * 58)
for src, vals in anova_results.items():
    print(f"{src:<30} {vals['SS']:10.4f} {vals['df']:6d} {vals['omega2']:8.4f}")
    stats_rows.append({"test": "ANOVA", "source": src,
                        "value": vals["omega2"], "metric": "omega_squared",
                        "SS": vals["SS"], "df": vals["df"]})

# Stage 2 comparison
print(f"\n  Stage 2 ω²(family×pathogen) = 0.285")
old_fp = 0.285
new_fp = anova_results.get("family×pathogen", {}).get("omega2", 0)
new_sp = anova_results.get("scoring×pathogen", {}).get("omega2", 0)
print(f"  Stage 3 ω²(family×pathogen) = {new_fp:.4f}")
print(f"  Stage 3 ω²(scoring×pathogen) = {new_sp:.4f}")
print(f"  Largest interaction: {'scoring×pathogen' if new_sp > new_fp else 'family×pathogen'}")

# ══════════════════════════════════════════════════════════════════════
# 2. FRIEDMAN TEST  (top 20 combos ranked across 11 pathogens)
# ══════════════════════════════════════════════════════════════════════
print("\n" + "=" * 70)
print("2. FRIEDMAN TEST")
print("=" * 70)

combo_pathogen = df.groupby(["scoring", "family", "pathogen"])["mcc"].mean().reset_index()
combo_mean = combo_pathogen.groupby(["scoring", "family"])["mcc"].mean().reset_index()
combo_mean = combo_mean.sort_values("mcc", ascending=False)
top20 = combo_mean.head(20)[["scoring", "family"]].values.tolist()

# Build matrix: 20 combos × 11 pathogens
pathogens = sorted(df["pathogen"].unique())
friedman_matrix = []
combo_labels = []
for s, f in top20:
    row = []
    for p in pathogens:
        val = combo_pathogen.loc[
            (combo_pathogen["scoring"] == s) &
            (combo_pathogen["family"] == f) &
            (combo_pathogen["pathogen"] == p), "mcc"
        ]
        row.append(val.values[0] if len(val) > 0 else np.nan)
    friedman_matrix.append(row)
    combo_labels.append(f"{s}+{f}")

friedman_matrix = np.array(friedman_matrix)

# Drop combos with any NaN
from scipy.stats import friedmanchisquare, rankdata

valid_mask = ~np.isnan(friedman_matrix).any(axis=1)
friedman_clean = friedman_matrix[valid_mask]
combo_labels_clean = [c for c, v in zip(combo_labels, valid_mask) if v]
print(f"  Valid combos (no NaN): {len(friedman_clean)}/{len(friedman_matrix)}")

# Rank within each pathogen (column)
ranks = np.apply_along_axis(lambda x: rankdata(-x), axis=0, arr=friedman_clean)

# scipy friedmanchisquare expects each arg = one treatment's values across blocks
args = [friedman_clean[i, :] for i in range(len(friedman_clean))]
chi2, p_friedman = friedmanchisquare(*args)

print(f"  Top {len(top20)} scoring×family combos across {len(pathogens)} pathogens")
print(f"  Friedman chi² = {chi2:.4f}, p = {p_friedman:.6f}")
print(f"  Significant (p<0.05): {'YES' if p_friedman < 0.05 else 'NO'}")

stats_rows.append({"test": "Friedman", "source": "top20_combos",
                    "value": chi2, "metric": "chi_squared",
                    "SS": p_friedman, "df": len(top20) - 1})

# Top 5 combos
print("\n  Top 5 combos (mean MCC across pathogens):")
for i, (s, f) in enumerate(top20[:5]):
    mean_mcc = combo_mean.loc[(combo_mean["scoring"] == s) & (combo_mean["family"] == f), "mcc"].values[0]
    print(f"    {i+1}. {s} + {f}: {mean_mcc:.4f}")

# ══════════════════════════════════════════════════════════════════════
# 3. LOPO CROSS-VALIDATION
# ══════════════════════════════════════════════════════════════════════
print("\n" + "=" * 70)
print("3. LEAVE-ONE-PATHOGEN-OUT (LOPO) CROSS-VALIDATION")
print("=" * 70)

lopo_results = []
for held_out in pathogens:
    train_pathogens = [p for p in pathogens if p != held_out]
    # Best combo from training pathogens
    train_df = combo_pathogen[combo_pathogen["pathogen"].isin(train_pathogens)]
    train_mean = train_df.groupby(["scoring", "family"])["mcc"].mean().reset_index()
    best_row = train_mean.loc[train_mean["mcc"].idxmax()]
    best_s, best_f = best_row["scoring"], best_row["family"]

    # Apply to held-out
    test_val = combo_pathogen.loc[
        (combo_pathogen["scoring"] == best_s) &
        (combo_pathogen["family"] == best_f) &
        (combo_pathogen["pathogen"] == held_out), "mcc"
    ]
    test_mcc = test_val.values[0] if len(test_val) > 0 else np.nan

    # Actual best for held-out
    actual_best = combo_pathogen.loc[
        combo_pathogen["pathogen"] == held_out
    ].sort_values("mcc", ascending=False).iloc[0]
    actual_best_mcc = actual_best["mcc"]
    actual_best_combo = f"{actual_best['scoring']}+{actual_best['family']}"

    match = (best_s == actual_best["scoring"]) and (best_f == actual_best["family"])

    lopo_results.append({
        "held_out": held_out,
        "predicted_combo": f"{best_s}+{best_f}",
        "predicted_mcc": test_mcc,
        "actual_best_combo": actual_best_combo,
        "actual_best_mcc": actual_best_mcc,
        "match": match,
        "mcc_gap": actual_best_mcc - test_mcc,
    })
    print(f"  {held_out:15s} | predicted: {best_s}+{best_f} → MCC={test_mcc:.4f} | "
          f"actual best: {actual_best_combo} → MCC={actual_best_mcc:.4f} | "
          f"gap={actual_best_mcc - test_mcc:.4f} {'✓' if match else '✗'}")

lopo_df = pd.DataFrame(lopo_results)
match_rate = lopo_df["match"].mean()
mean_gen_mcc = lopo_df["predicted_mcc"].mean()
mean_gap = lopo_df["mcc_gap"].mean()
print(f"\n  Match rate: {match_rate:.1%}")
print(f"  Mean generalization MCC: {mean_gen_mcc:.4f}")
print(f"  Mean MCC gap (best - predicted): {mean_gap:.4f}")

stats_rows.append({"test": "LOPO", "source": "match_rate",
                    "value": match_rate, "metric": "proportion",
                    "SS": mean_gen_mcc, "df": len(pathogens)})
stats_rows.append({"test": "LOPO", "source": "mean_gen_mcc",
                    "value": mean_gen_mcc, "metric": "MCC",
                    "SS": mean_gap, "df": len(pathogens)})

# ══════════════════════════════════════════════════════════════════════
# 4. ADDITIONAL KEY STATISTICS
# ══════════════════════════════════════════════════════════════════════
print("\n" + "=" * 70)
print("4. ADDITIONAL KEY STATISTICS")
print("=" * 70)

# Best per pathogen
print("\n  Best scoring+detector per pathogen:")
for p in pathogens:
    pdf = df[df["pathogen"] == p].sort_values("mcc", ascending=False).iloc[0]
    print(f"    {p:15s}: {pdf['scoring']}+{pdf['detector']} → MCC={pdf['mcc']:.4f}")

# Unique best combos
best_combos = []
for p in pathogens:
    pdf = combo_pathogen[combo_pathogen["pathogen"] == p].sort_values("mcc", ascending=False).iloc[0]
    best_combos.append((pdf["scoring"], pdf["family"]))
n_unique = len(set(best_combos))
print(f"\n  Unique best scoring+family combos: {n_unique}/{len(pathogens)}")

# Overall MCC stats
print(f"\n  Overall MCC: mean={df['mcc'].mean():.4f}, median={df['mcc'].median():.4f}, "
      f"std={df['mcc'].std():.4f}")
print(f"  MCC range: [{df['mcc'].min():.4f}, {df['mcc'].max():.4f}]")

# ══════════════════════════════════════════════════════════════════════
# FIGURE GENERATION
# ══════════════════════════════════════════════════════════════════════
plt.rcParams.update({
    "font.size": 11,
    "axes.titlesize": 13,
    "axes.labelsize": 12,
    "xtick.labelsize": 10,
    "ytick.labelsize": 10,
    "figure.dpi": 300,
    "savefig.dpi": 300,
    "savefig.bbox": "tight",
})


def save_fig(fig, name):
    p1 = os.path.join(FIG_DIR, name)
    p2 = os.path.join(FIG_DIR2, name)
    fig.savefig(p1, dpi=300, bbox_inches="tight", facecolor="white")
    fig.savefig(p2, dpi=300, bbox_inches="tight", facecolor="white")
    plt.close(fig)
    print(f"  Saved: {p1}")


# ── Fig 1: Scoring × Pathogen MCC Heatmap ─────────────────────────────
print("\n" + "=" * 70)
print("FIGURE 1: Scoring × Pathogen Heatmap")
print("=" * 70)

pivot = df.groupby(["scoring", "pathogen"])["mcc"].mean().unstack()
# Order scorings by mean MCC
scoring_order = pivot.mean(axis=1).sort_values(ascending=False).index
pivot = pivot.loc[scoring_order]

fig, ax = plt.subplots(figsize=(14, 9))
sns.heatmap(pivot, cmap="RdYlGn", center=0, annot=True, fmt=".3f",
            linewidths=0.5, ax=ax, cbar_kws={"label": "Mean MCC"})

# Bold best per pathogen
for j, p in enumerate(pivot.columns):
    best_i = pivot[p].idxmax()
    row_idx = list(pivot.index).index(best_i)
    ax.texts[row_idx * len(pivot.columns) + j].set_fontweight("bold")
    ax.texts[row_idx * len(pivot.columns) + j].set_fontsize(9)

ax.set_title("Stage 3: Mean MCC by Scoring Method × Pathogen", fontsize=14, pad=12)
ax.set_xlabel("Pathogen")
ax.set_ylabel("Scoring Method")
plt.yticks(rotation=0)
plt.xticks(rotation=35, ha="right")
save_fig(fig, "stage3_scoring_pathogen_heatmap.png")

# ── Fig 2: Scoring Category Bar Chart ──────────────────────────────────
print("\nFIGURE 2: Scoring Category Bar Chart")
print("=" * 70)

cat_mcc = df.groupby("scoring_category")["mcc"].agg(["mean", "std", "count"]).reset_index()
cat_mcc = cat_mcc.sort_values("mean", ascending=False)

fig, ax = plt.subplots(figsize=(10, 6))
colors = {"Frequency": "#e74c3c", "MSA": "#3498db", "Phylo": "#2ecc71",
          "Structure": "#9b59b6", "AI": "#f39c12", "Composite": "#1abc9c"}
bar_colors = [colors.get(c, "#95a5a6") for c in cat_mcc["scoring_category"]]

bars = ax.bar(cat_mcc["scoring_category"], cat_mcc["mean"],
              yerr=cat_mcc["std"], capsize=5, color=bar_colors,
              edgecolor="black", linewidth=0.8, alpha=0.85)

for bar, val in zip(bars, cat_mcc["mean"]):
    ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 0.005,
            f"{val:.4f}", ha="center", va="bottom", fontsize=10, fontweight="bold")

ax.set_ylabel("Mean MCC")
ax.set_title("Mean MCC by Scoring Category (Stage 3, 11 Pathogens)", fontsize=13)
ax.set_ylim(bottom=min(0, cat_mcc["mean"].min() - 0.02))
ax.axhline(y=0, color="gray", linestyle="--", alpha=0.5)
ax.grid(axis="y", alpha=0.3)
save_fig(fig, "stage3_scoring_category_bar.png")

# ── Fig 3: ANOVA Decomposition (Stage 2 vs Stage 3) ───────────────────
print("\nFIGURE 3: ANOVA Variance Decomposition")
print("=" * 70)

# Stage 3 data
s3_labels = []
s3_vals = []
for src, vals in anova_results.items():
    if src != "Residual":
        s3_labels.append(src)
        s3_vals.append(vals["omega2"])
s3_labels.append("Residual")
s3_vals.append(1 - sum(s3_vals))

# Stage 2 data (from old 9-pathogen results)
s2_data = {
    "pathogen": 0.083,
    "family": 0.350,
    "scoring": 0.010,
    "scoring×family": 0.050,
    "scoring×pathogen": 0.100,
    "family×pathogen": 0.285,
}
s2_resid = 1 - sum(s2_data.values())
s2_labels = list(s2_data.keys()) + ["Residual"]
s2_vals = list(s2_data.values()) + [s2_resid]

fig, axes = plt.subplots(1, 2, figsize=(16, 7))

cmap_colors = plt.cm.Set2(np.linspace(0, 1, max(len(s2_labels), len(s3_labels))))

# Stage 2
ax = axes[0]
s2_sorted = sorted(zip(s2_vals, s2_labels), reverse=True)
s2_v, s2_l = zip(*s2_sorted)
bars = ax.barh(range(len(s2_l)), s2_v, color=cmap_colors[:len(s2_l)],
               edgecolor="black", linewidth=0.6)
ax.set_yticks(range(len(s2_l)))
ax.set_yticklabels(s2_l)
for i, v in enumerate(s2_v):
    ax.text(v + 0.005, i, f"{v:.3f}", va="center", fontsize=10)
ax.set_xlabel("ω² (omega-squared)")
ax.set_title("Stage 2 (9 pathogens, 9 scoring, 41 det.)", fontsize=12)
ax.set_xlim(0, max(s2_v) * 1.25)
ax.invert_yaxis()

# Stage 3
ax = axes[1]
s3_sorted = sorted(zip(s3_vals, s3_labels), reverse=True)
s3_v, s3_l = zip(*s3_sorted)
bars = ax.barh(range(len(s3_l)), s3_v, color=cmap_colors[:len(s3_l)],
               edgecolor="black", linewidth=0.6)
ax.set_yticks(range(len(s3_l)))
ax.set_yticklabels(s3_l)
for i, v in enumerate(s3_v):
    ax.text(v + 0.005, i, f"{v:.3f}", va="center", fontsize=10)
ax.set_xlabel("ω² (omega-squared)")
ax.set_title(f"Stage 3 (11 pathogens, 18 scoring, 39 det.)", fontsize=12)
ax.set_xlim(0, max(s3_v) * 1.25)
ax.invert_yaxis()

fig.suptitle("ANOVA Variance Decomposition: Stage 2 vs Stage 3", fontsize=14, y=1.02)
plt.tight_layout()
save_fig(fig, "stage3_anova_decomposition.png")

# ── Fig 4: Best per Pathogen (grouped bar) ─────────────────────────────
print("\nFIGURE 4: Best Scoring + Detector per Pathogen")
print("=" * 70)

best_per = []
for p in pathogens:
    pdf = df[df["pathogen"] == p]
    # Best scoring (mean across detectors)
    s_best = pdf.groupby("scoring")["mcc"].mean().idxmax()
    s_mcc = pdf.groupby("scoring")["mcc"].mean().max()
    # Best family (mean across scorings)
    f_best = pdf.groupby("family")["mcc"].mean().idxmax()
    f_mcc = pdf.groupby("family")["mcc"].mean().max()
    # Best combo
    combo = pdf.groupby(["scoring", "family"])["mcc"].mean()
    best_combo_idx = combo.idxmax()
    best_combo_mcc = combo.max()
    best_per.append({
        "pathogen": p, "best_scoring": s_best, "scoring_mcc": s_mcc,
        "best_family": f_best, "family_mcc": f_mcc,
        "best_combo": f"{best_combo_idx[0]}+{best_combo_idx[1]}",
        "combo_mcc": best_combo_mcc,
    })

bdf = pd.DataFrame(best_per)

fig, ax = plt.subplots(figsize=(14, 7))
x = np.arange(len(pathogens))
w = 0.25

bars1 = ax.bar(x - w, bdf["scoring_mcc"], w, label="Best Scoring", color="#3498db",
               edgecolor="black", linewidth=0.5)
bars2 = ax.bar(x, bdf["family_mcc"], w, label="Best Detector Family", color="#e74c3c",
               edgecolor="black", linewidth=0.5)
bars3 = ax.bar(x + w, bdf["combo_mcc"], w, label="Best Combo", color="#2ecc71",
               edgecolor="black", linewidth=0.5)

# Labels on bars
for bars, col in [(bars1, "best_scoring"), (bars2, "best_family"), (bars3, "best_combo")]:
    for bar, label in zip(bars, bdf[col]):
        lbl = label if len(label) < 15 else label[:13] + ".."
        ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 0.003,
                lbl, ha="center", va="bottom", fontsize=6.5, rotation=55)

ax.set_xticks(x)
ax.set_xticklabels(pathogens, rotation=35, ha="right")
ax.set_ylabel("Mean MCC")
ax.set_title("Best Scoring, Detector Family, and Combo per Pathogen", fontsize=13)
ax.legend(loc="upper right")
ax.grid(axis="y", alpha=0.3)
ax.axhline(y=0, color="gray", linestyle="--", alpha=0.5)
save_fig(fig, "stage3_best_per_pathogen.png")

# ── Fig 5: Detector Family Comparison ──────────────────────────────────
print("\nFIGURE 5: Detector Family Comparison")
print("=" * 70)

fam_mcc = df.groupby("family")["mcc"].agg(["mean", "std"]).reset_index()
fam_mcc = fam_mcc.sort_values("mean", ascending=True)

fig, ax = plt.subplots(figsize=(10, 7))
colors_det = plt.cm.viridis(np.linspace(0.2, 0.9, len(fam_mcc)))
bars = ax.barh(fam_mcc["family"], fam_mcc["mean"], xerr=fam_mcc["std"],
               capsize=3, color=colors_det, edgecolor="black", linewidth=0.5)
for bar, val in zip(bars, fam_mcc["mean"]):
    ax.text(val + 0.003, bar.get_y() + bar.get_height() / 2,
            f"{val:.4f}", va="center", fontsize=10)

ax.set_xlabel("Mean MCC (across all scorings and pathogens)")
ax.set_title("Detection Family Performance Comparison (Stage 3)", fontsize=13)
ax.axvline(x=0, color="gray", linestyle="--", alpha=0.5)
ax.grid(axis="x", alpha=0.3)
save_fig(fig, "stage3_detector_comparison.png")

# ── Fig 6: Fairness Scatter ────────────────────────────────────────────
print("\nFIGURE 6: Fairness Scatter")
print("=" * 70)

# Compute freq MCC per pathogen
freq_mcc = df[df["scoring"] == "freq"].groupby("pathogen")["mcc"].mean().reset_index()
freq_mcc.columns = ["pathogen", "freq_mcc"]

fair_plot = fairness.merge(freq_mcc, on="pathogen", how="inner")

fig, ax = plt.subplots(figsize=(9, 7))
scatter = ax.scatter(fair_plot["rpb"], fair_plot["freq_mcc"],
                     s=fair_plot["n_positions"] / 3, alpha=0.7,
                     c=fair_plot["p_value"].apply(lambda x: "red" if x < 0.05 else "steelblue"),
                     edgecolors="black", linewidth=0.8)

for _, row in fair_plot.iterrows():
    ax.annotate(row["pathogen"],
                (row["rpb"], row["freq_mcc"]),
                textcoords="offset points", xytext=(8, 5), fontsize=9)

# Correlation
rho, p_rho = stats.spearmanr(fair_plot["rpb"], fair_plot["freq_mcc"])
ax.set_xlabel("Point-Biserial r (Frequency–Layer A correlation)")
ax.set_ylabel("Mean Frequency-Scoring MCC")
ax.set_title(f"Fairness: Freq–GT Correlation vs Freq MCC\n(Spearman ρ={rho:.3f}, p={p_rho:.4f})",
             fontsize=13)
ax.axhline(y=0, color="gray", linestyle="--", alpha=0.4)
ax.axvline(x=0, color="gray", linestyle="--", alpha=0.4)
ax.grid(alpha=0.3)

# Legend for significance
from matplotlib.lines import Line2D
legend_elements = [
    Line2D([0], [0], marker='o', color='w', markerfacecolor='red',
           markersize=10, label='rpb significant (p<0.05)'),
    Line2D([0], [0], marker='o', color='w', markerfacecolor='steelblue',
           markersize=10, label='rpb not significant'),
]
ax.legend(handles=legend_elements, loc="best")
save_fig(fig, "stage3_fairness_scatter.png")

print(f"  Fairness: Spearman rho={rho:.3f}, p={p_rho:.4f}")
stats_rows.append({"test": "Fairness", "source": "rpb_vs_freq_mcc",
                    "value": rho, "metric": "spearman_rho",
                    "SS": p_rho, "df": len(fair_plot)})

# ── Fig 7: Layer A vs Layer C ──────────────────────────────────────────
print("\nFIGURE 7: Layer A vs Layer C Comparison")
print("=" * 70)

# Exclude EV-A71 (only 1 Layer C position due to VP1-only coverage)
layer_c_valid = layer_c[layer_c["pathogen"] != "EV-A71"].copy()

# Aggregate: best MCC per scoring per pathogen (across detectors)
lc_agg = (layer_c_valid.groupby(["pathogen", "scoring"])
          [["mcc_layer_a", "mcc_layer_c"]].max().reset_index())

dms_pathogens = sorted(lc_agg["pathogen"].unique())
n_dms = len(dms_pathogens)

fig, axes = plt.subplots(1, n_dms, figsize=(5 * n_dms, 7), sharey=False)
if n_dms == 1:
    axes = [axes]

for idx, p in enumerate(dms_pathogens):
    ax = axes[idx]
    pdata = lc_agg[lc_agg["pathogen"] == p].copy()
    pdata = pdata.sort_values("mcc_layer_a", ascending=False)

    x = np.arange(len(pdata))
    w = 0.35
    ax.bar(x - w / 2, pdata["mcc_layer_a"], w, label="Layer A (literature)",
           color="#3498db", edgecolor="black", linewidth=0.5)
    ax.bar(x + w / 2, pdata["mcc_layer_c"], w, label="Layer C (DMS)",
           color="#e74c3c", edgecolor="black", linewidth=0.5)

    ax.set_xticks(x)
    ax.set_xticklabels(pdata["scoring"], rotation=45, ha="right", fontsize=6)
    ax.set_ylabel("MCC")
    ax.set_title(p, fontsize=12)
    ax.axhline(y=0, color="gray", linestyle="--", alpha=0.5)
    ax.grid(axis="y", alpha=0.3)
    if idx == 0:
        ax.legend(fontsize=9)

fig.suptitle("Layer A vs Layer C (DMS) Ground Truth: Scoring Method Rankings",
             fontsize=14, y=1.02)
plt.tight_layout()
save_fig(fig, "stage3_layer_a_vs_c.png")

# Rank correlation per DMS pathogen
print("\n  Layer A vs C rank correlations:")
for p in dms_pathogens:
    pdata = lc_agg[lc_agg["pathogen"] == p]
    if len(pdata) >= 5:
        rho_ac, p_ac = stats.spearmanr(pdata["mcc_layer_a"], pdata["mcc_layer_c"])
        print(f"    {p}: Spearman rho={rho_ac:.3f}, p={p_ac:.4f}")
        stats_rows.append({"test": "LayerAvsC", "source": p,
                            "value": rho_ac, "metric": "spearman_rho",
                            "SS": p_ac, "df": len(pdata)})

# ══════════════════════════════════════════════════════════════════════
# SAVE STATISTICS
# ══════════════════════════════════════════════════════════════════════
stats_df = pd.DataFrame(stats_rows)
stats_path = os.path.join(RESULTS, "stage3_statistics.csv")
stats_df.to_csv(stats_path, index=False)
print(f"\nSaved statistics to {stats_path}")

# ══════════════════════════════════════════════════════════════════════
# KEY NUMBERS SUMMARY
# ══════════════════════════════════════════════════════════════════════
print("\n" + "=" * 70)
print("KEY NUMBERS FOR THE PAPER")
print("=" * 70)
print(f"  Total evaluations: {len(df)}")
print(f"  Scorings: {df['scoring'].nunique()}, Families: {df['family'].nunique()}, "
      f"Pathogens: {df['pathogen'].nunique()}")
print(f"  Detectors (param variants): {df['detector'].nunique()}")

print(f"\n  ANOVA main effects:")
for src in ["scoring", "family", "pathogen"]:
    print(f"    ω²({src}) = {anova_results[src]['omega2']:.4f}")
print(f"  ANOVA interactions:")
for src in ["scoring×family", "scoring×pathogen", "family×pathogen"]:
    if src in anova_results:
        print(f"    ω²({src}) = {anova_results[src]['omega2']:.4f}")

print(f"\n  Largest variance source: ", end="")
all_effects = {k: v["omega2"] for k, v in anova_results.items() if k != "Residual"}
largest = max(all_effects, key=all_effects.get)
print(f"{largest} (ω²={all_effects[largest]:.4f})")

print(f"\n  Friedman chi² = {chi2:.4f}, p = {p_friedman:.6f}")
print(f"  LOPO match rate = {match_rate:.1%}, mean gen MCC = {mean_gen_mcc:.4f}")
print(f"  Unique best combos: {n_unique}/{len(pathogens)}")
print(f"  Fairness rpb-vs-mcc: rho={rho:.3f}, p={p_rho:.4f}")

# Global best
overall_best = df.loc[df["mcc"].idxmax()]
print(f"\n  Global best single evaluation:")
print(f"    {overall_best['pathogen']}: {overall_best['scoring']}+{overall_best['detector']} "
      f"→ MCC={overall_best['mcc']:.4f}")

print("\n  DONE. All figures and statistics saved.")

# ══════════════════════════════════════════════════════════════════════
# FIGURE 8: LOPO Cross-Validation Visualization
# ══════════════════════════════════════════════════════════════════════
print("\nFIGURE 8: LOPO Cross-Validation")
print("=" * 70)

# Use already-computed lopo_results from section 3
lopo_viz = pd.DataFrame(lopo_results)
lopo_viz = lopo_viz.rename(columns={
    "held_out": "pathogen",
    "predicted_mcc": "predicted_mcc",
    "actual_best_mcc": "actual_mcc",
    "mcc_gap": "gap",
}).sort_values("actual_mcc", ascending=True)
lopo_df = lopo_viz

fig, ax = plt.subplots(figsize=(10, 6))
y_pos = np.arange(len(lopo_df))
w = 0.35
ax.barh(y_pos - w/2, lopo_df["predicted_mcc"], w, label="Predicted (LOPO)",
        color="#e74c3c", edgecolor="black", linewidth=0.5)
ax.barh(y_pos + w/2, lopo_df["actual_mcc"], w, label="Actual best",
        color="#2ecc71", edgecolor="black", linewidth=0.5)

ax.set_yticks(y_pos)
ax.set_yticklabels(lopo_df["pathogen"], fontsize=10)
ax.set_xlabel("MCC", fontsize=12)
ax.set_title("Leave-One-Pathogen-Out Cross-Validation: 0/11 Match", fontsize=13)
ax.legend(fontsize=10)
ax.axvline(x=0, color="gray", linestyle="--", alpha=0.5)
ax.grid(axis="x", alpha=0.3)

# Annotate gaps
for i, row in enumerate(lopo_df.itertuples()):
    ax.annotate(f"gap={row.gap:.2f}", (max(row.predicted_mcc, row.actual_mcc) + 0.01, i),
                fontsize=7, va="center")

plt.tight_layout()
save_fig(fig, "stage3_lopo_crossval.png")

# ══════════════════════════════════════════════════════════════════════
# FIGURE 9: FUBAR Spotlight — H3N2 best scoring
# ══════════════════════════════════════════════════════════════════════
print("\nFIGURE 9: FUBAR Spotlight")
print("=" * 70)

fubar_scorings = [s for s in df["scoring"].unique() if "fubar" in s.lower()]
if fubar_scorings:
    fubar_df = df[df["scoring"].isin(fubar_scorings)]

    # Per-pathogen best FUBAR MCC vs best overall MCC
    fig, ax = plt.subplots(figsize=(10, 6))
    path_list = sorted(df["pathogen"].unique())
    x_pos = np.arange(len(path_list))

    fubar_best = []
    overall_best_mcc = []
    for p in path_list:
        pdf = df[df["pathogen"] == p]
        fubar_pdf = fubar_df[fubar_df["pathogen"] == p]
        overall_best_mcc.append(pdf["mcc"].max())
        fubar_best.append(fubar_pdf["mcc"].max() if len(fubar_pdf) > 0 else 0)

    w = 0.35
    ax.bar(x_pos - w/2, overall_best_mcc, w, label="Overall best",
           color="#3498db", edgecolor="black", linewidth=0.5)
    ax.bar(x_pos + w/2, fubar_best, w, label="Best FUBAR scoring",
           color="#e67e22", edgecolor="black", linewidth=0.5)

    ax.set_xticks(x_pos)
    ax.set_xticklabels(path_list, rotation=45, ha="right", fontsize=9)
    ax.set_ylabel("MCC", fontsize=12)
    ax.set_title("FUBAR Phylogenetic Scoring vs Overall Best per Pathogen", fontsize=13)
    ax.legend(fontsize=10)
    ax.axhline(y=0, color="gray", linestyle="--", alpha=0.5)
    ax.grid(axis="y", alpha=0.3)

    # Annotate where FUBAR is best
    for i, (fb, ob) in enumerate(zip(fubar_best, overall_best_mcc)):
        if fb > 0 and abs(fb - ob) < 0.01:
            ax.annotate("★", (i, fb + 0.01), ha="center", fontsize=14, color="#e67e22")

    plt.tight_layout()
    save_fig(fig, "stage3_fubar_spotlight.png")
