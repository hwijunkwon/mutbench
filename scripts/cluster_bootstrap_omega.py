#!/usr/bin/env python3
"""Cluster bootstrap CI for omega^2(scoring x pathogen) — 11-pathogen panel.

Resampling unit: pathogen (cluster). At each iteration, draw 11 pathogens
with replacement, build the resampled long table, then recompute the
manual Type-II-like omega^2 decomposition. Report mean, percentile 95%
CI, and the two robustness restrictions disclosed in the body
(HCV-excluded; phylogenetic-only 4 pathogens: SARS-CoV-2, H3N2, HIV-1,
RSV).

Headline body claims being checked:
  - omega^2(scoring x pathogen) = 0.296
  - 11-pathogen percentile CI = [0.195, 0.333]
  - HCV-excluded omega^2 = 0.246 (ch5:289-292)
  - 4-phylo-only restriction omega^2 = 0.137 (ch5:292)

Outputs:
  results/mutbench/cluster_bootstrap_omega.csv  (per-iteration omega^2)
  results/mutbench/cluster_bootstrap_omega_summary.csv
"""

from __future__ import annotations

import os
import sys
from itertools import combinations
from pathlib import Path

import numpy as np
import pandas as pd

PROJECT = Path(__file__).resolve().parent.parent
RESULTS = PROJECT / "results" / "mutbench"
INPUT = RESULTS / "stage3_full_results.csv"

N_BOOT = 1000
SEED = 42
# Body definition (ch5:292): four pathogens whose Layer A is constructed
# from phylogenetically-confirmed convergent evolution (excludes HCV's
# HVR diversifying selection and Norovirus's epochal-variant positions).
FOUR_PHYLO_ONLY = ["SARS-CoV-2", "H3N2", "MERS", "EV-A71"]
HCV_EXCLUDED = None  # n=10
HCV_NORO_EXCLUDED = ["HCV", "Norovirus"]  # n=9


def _ms_residual(df, factors, dv="mcc"):
    cells = df.groupby(factors, observed=True)[dv]
    ss_within = sum(((g - g.mean()) ** 2).sum() for _, g in cells)
    df_within = len(df) - cells.ngroups
    if df_within <= 0:
        return 0.001
    return ss_within / df_within


def omega2_interaction(df, f1="scoring", f2="pathogen", f3="family", dv="mcc"):
    """Compute omega^2 for the f1 x f2 interaction under a 3-way design.

    Manual Type-II-like decomposition matching analyze_stage3_stats.py:
    SS_interaction(f1, f2) accounts for f1, f2 main effects;
    MS_residual is computed from within-cell residuals over (f1, f2, f3).
    """
    factors = [f1, f2, f3]
    grand_mean = df[dv].mean()
    ss_total = ((df[dv] - grand_mean) ** 2).sum()
    if ss_total < 1e-12:
        return 0.0
    f1_means = df.groupby(f1, observed=True)[dv].mean()
    f2_means = df.groupby(f2, observed=True)[dv].mean()
    cell_means = df.groupby([f1, f2], observed=True)[dv].mean()
    cell_counts = df.groupby([f1, f2], observed=True)[dv].count()
    ss_int = 0.0
    for (a, b), mean_ab in cell_means.items():
        n_ab = cell_counts.get((a, b), 0)
        expected = f1_means[a] + f2_means[b] - grand_mean
        ss_int += n_ab * (mean_ab - expected) ** 2
    k1, k2 = df[f1].nunique(), df[f2].nunique()
    df_int = (k1 - 1) * (k2 - 1)
    ms_resid = _ms_residual(df, factors, dv)
    omega2 = (ss_int - df_int * ms_resid) / (ss_total + ms_resid)
    return max(0.0, omega2)


def cluster_resample(df, pathogens, rng):
    """Resample pathogens with replacement; build long table.

    To preserve cell counts when a pathogen is drawn multiple times, we
    relabel each draw so it acts as a distinct cluster.
    """
    pieces = []
    for k, p in enumerate(pathogens):
        sub = df[df["pathogen"] == p].copy()
        if k == 0 or p not in [pp for pp in pathogens[:k]]:
            sub["pathogen"] = p
        else:
            sub["pathogen"] = f"{p}__rep{k}"
        pieces.append(sub)
    return pd.concat(pieces, ignore_index=True)


def main():
    print("Cluster bootstrap omega^2(scoring x pathogen)")
    print("=" * 70)
    if not INPUT.exists():
        sys.exit(f"missing input: {INPUT}")
    df = pd.read_csv(INPUT)
    df["pathogen"] = df["pathogen"].replace({"Influenza_B": "Influenza B"})
    print(f"Loaded {len(df)} rows; pathogens={df['pathogen'].nunique()}")

    # Headline reproduction
    headline = omega2_interaction(df)
    print(f"Headline omega^2(scoring x pathogen) on full panel: {headline:.4f}")

    # 11-pathogen cluster bootstrap
    pathogens_full = sorted(df["pathogen"].unique())
    rng = np.random.default_rng(SEED)
    boot_full = []
    for i in range(N_BOOT):
        sample = list(rng.choice(pathogens_full, size=len(pathogens_full), replace=True))
        sub = cluster_resample(df, sample, rng)
        boot_full.append(omega2_interaction(sub))
    boot_full = np.asarray(boot_full)
    print(f"\n11-pathogen cluster bootstrap (n={N_BOOT}):")
    print(f"  mean omega^2 = {boot_full.mean():.4f}")
    print(f"  median       = {np.median(boot_full):.4f}")
    print(f"  95% percentile CI = [{np.percentile(boot_full, 2.5):.4f}, {np.percentile(boot_full, 97.5):.4f}]")

    # HCV-excluded restriction (evaluation-level, ch4:525 -> 0.246)
    hcv_out = df[df["pathogen"] != "HCV"]
    omega_hcv_excl = omega2_interaction(hcv_out)
    print(f"\nEvaluation-level HCV-excluded omega^2 = {omega_hcv_excl:.4f}  (body ch4:525 = 0.246)")

    # Cell-level HCV-excluded (ch5:292 -> 0.199); n=10
    cell_means_full = df.groupby(["scoring", "family", "pathogen"], observed=True)["mcc"].mean().reset_index()
    cell_means_hcv = cell_means_full[cell_means_full["pathogen"] != "HCV"]
    omega_hcv_cell = omega2_interaction(cell_means_hcv)
    print(f"Cell-level HCV-excluded omega^2     = {omega_hcv_cell:.4f}  (body ch5:292 = 0.199)")

    # Cell-level HCV+Norovirus excluded (ch5:292 -> 0.187); n=9
    cell_means_hn = cell_means_full[~cell_means_full["pathogen"].isin(HCV_NORO_EXCLUDED)]
    omega_hn_cell = omega2_interaction(cell_means_hn)
    print(f"Cell-level HCV+Noro excluded omega^2 = {omega_hn_cell:.4f}  (body ch5:292 = 0.187)")

    # Cell-level 4-phylo-only (ch5:292 -> 0.137); n=4
    cell_means_4 = cell_means_full[cell_means_full["pathogen"].isin(FOUR_PHYLO_ONLY)]
    omega_4_cell = omega2_interaction(cell_means_4)
    print(f"Cell-level 4-phylo-only omega^2     = {omega_4_cell:.4f}  (body ch5:292 = 0.137)")

    # Evaluation-level (legacy comparison, may diverge from cell-level)
    phylo = df[df["pathogen"].isin(FOUR_PHYLO_ONLY)]
    omega_phylo_eval = omega2_interaction(phylo)
    print(f"Evaluation-level 4-phylo-only omega^2 = {omega_phylo_eval:.4f}  (Cohen large = 0.14)")

    # Per-pathogen leave-one-out
    print("\nLeave-one-pathogen omega^2 (sensitivity):")
    loo_rows = []
    for p in pathogens_full:
        sub = df[df["pathogen"] != p]
        o = omega2_interaction(sub)
        loo_rows.append({"excluded_pathogen": p, "omega2": o})
        print(f"  exclude {p:<14s} -> omega^2 = {o:.4f}")

    # Save artifacts
    pd.DataFrame({"iteration": np.arange(N_BOOT), "omega2_scoring_x_pathogen": boot_full}).to_csv(
        RESULTS / "cluster_bootstrap_omega.csv", index=False
    )
    summary = pd.DataFrame([
        {"protocol": "headline_full_panel_evaluation_level", "n_pathogens": len(pathogens_full),
         "omega2_mean": float(headline), "ci_lo": np.nan, "ci_hi": np.nan,
         "body_target": 0.296},
        {"protocol": "11pathogen_cluster_bootstrap_evaluation_level", "n_pathogens": len(pathogens_full),
         "omega2_mean": float(boot_full.mean()),
         "ci_lo": float(np.percentile(boot_full, 2.5)),
         "ci_hi": float(np.percentile(boot_full, 97.5)),
         "body_target": "[0.195, 0.333]"},
        {"protocol": "HCV_excluded_evaluation_level", "n_pathogens": len(pathogens_full) - 1,
         "omega2_mean": float(omega_hcv_excl), "ci_lo": np.nan, "ci_hi": np.nan,
         "body_target": 0.246},
        {"protocol": "HCV_excluded_cell_level", "n_pathogens": len(pathogens_full) - 1,
         "omega2_mean": float(omega_hcv_cell), "ci_lo": np.nan, "ci_hi": np.nan,
         "body_target": 0.199},
        {"protocol": "HCV_Noro_excluded_cell_level", "n_pathogens": len(pathogens_full) - 2,
         "omega2_mean": float(omega_hn_cell), "ci_lo": np.nan, "ci_hi": np.nan,
         "body_target": 0.187},
        {"protocol": "phylo_only_4pathogen_cell_level",
         "n_pathogens": len(FOUR_PHYLO_ONLY),
         "omega2_mean": float(omega_4_cell), "ci_lo": np.nan, "ci_hi": np.nan,
         "body_target": 0.137},
        {"protocol": "phylo_only_4pathogen_evaluation_level",
         "n_pathogens": len(FOUR_PHYLO_ONLY),
         "omega2_mean": float(omega_phylo_eval), "ci_lo": np.nan, "ci_hi": np.nan,
         "body_target": "(not directly reported)"},
    ])
    summary.to_csv(RESULTS / "cluster_bootstrap_omega_summary.csv", index=False)
    pd.DataFrame(loo_rows).to_csv(RESULTS / "cluster_bootstrap_omega_loo.csv", index=False)
    print(f"\nSaved CSVs in {RESULTS}")


if __name__ == "__main__":
    main()
