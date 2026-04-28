#!/usr/bin/env python3
"""Tier D5: Phylogenetic block bootstrap + linear mixed-effects model
for omega^2(scoring x pathogen) on the 8,580-row Stage~3 evaluation grid.

This script extends the cycle-4 wild-cluster bootstrap (Tier B3, see
scripts/wild_cluster_bootstrap_omega.py and the headline numbers in
ch3:964, ch4:578, ch5:289) with two further small-cluster robustness
checks requested by the cycle-5 audit:

(D5.1) Phylogenetic *block* bootstrap.
   The 11 pathogens are partitioned into eight viral families
   (Coronaviridae, Orthomyxoviridae, Flaviviridae, Picornaviridae,
   Caliciviridae, Retroviridae, Pneumoviridae, Rhabdoviridae). Pathogen
   identities within a family are *not* exchangeable across families,
   but families themselves are the natural exchangeable phylogenetic
   unit (Felsenstein 1985 spirit: independent contrasts at the family
   level rather than at the pathogen level). The bootstrap therefore
   resamples *families* with replacement, expanding each draw to the
   pathogens in that family. We report the percentile CI of omega^2.

(D5.2) Linear mixed-effects model.
   y_{ij} = mu + alpha_{scoring,i} + u_pathogen,j + e_{ij}
   where alpha is a fixed scoring effect (20 levels) and u is a random
   pathogen intercept (11 levels) with u ~ Normal(0, sigma^2_pathogen)
   and e ~ Normal(0, sigma^2_resid). Variance components and the
   intra-class correlation (ICC = sigma^2_path / (sigma^2_path +
   sigma^2_resid)) translate to a model-based pseudo-omega^2 for the
   pathogen factor for triangulation against the ANOVA-based
   omega^2(scoring x pathogen). The cluster-corrected variance ratio
   complements the wild-cluster CI as a model-based robustness frame.

Outputs:
  results/mutbench/block_bootstrap_omega.csv          per-replicate omega^2
  results/mutbench/block_bootstrap_omega_summary.csv  block-boot summary row
  results/mutbench/mixed_effects_omega_summary.csv    mixed-effects summary
  results/mutbench/omega_robustness_4way.csv          4-method comparison

References:
  Cameron, Gelbach, Miller (2008) Bootstrap-Based Improvements for
    Inference with Clustered Errors. ReStat 90(3): 414-427.
  Felsenstein (1985) Phylogenies and the comparative method.
    Am Nat 125(1): 1-15.
  Bolker et al. (2009) GLMMs in ecology and evolution. TREE 24(3):
    127-135.
"""

from __future__ import annotations

import sys
import time
from pathlib import Path

import numpy as np
import pandas as pd

PROJECT = Path(__file__).resolve().parent.parent
RESULTS = PROJECT / "results" / "mutbench"
INPUT = RESULTS / "stage3_full_results.csv"

N_BOOT = 1000
SEED = 42

# Phylogenetic block (viral family) assignment for the 11 Stage~3
# pathogens. Sources: ICTV taxonomy (2023 release), NCBI Virus.
# Coronaviridae: SARS-CoV-2, MERS-CoV (both Betacoronavirus).
# Orthomyxoviridae: H3N2 (Influenza A), Influenza B virus.
# Flaviviridae: HCV (Hepacivirus), Dengue (Flavivirus).
# Picornaviridae: EV-A71 (Enterovirus A).
# Caliciviridae: Norovirus (Norwalk virus).
# Retroviridae: HIV-1 (Lentivirus).
# Pneumoviridae: RSV (formerly Paramyxoviridae; reclassified ICTV 2016).
# Rhabdoviridae: Rabies (Lyssavirus).
PHYLO_BLOCKS: dict[str, list[str]] = {
    "Coronaviridae": ["SARS-CoV-2", "MERS"],
    "Orthomyxoviridae": ["H3N2", "Influenza B"],
    "Flaviviridae": ["HCV", "Dengue"],
    "Picornaviridae": ["EV-A71"],
    "Caliciviridae": ["Norovirus"],
    "Retroviridae": ["HIV-1"],
    "Pneumoviridae": ["RSV"],
    "Rhabdoviridae": ["Rabies"],
}


def _ms_residual(df, factors, dv="mcc"):
    cells = df.groupby(factors, observed=True)[dv]
    ss_within = sum(((g - g.mean()) ** 2).sum() for _, g in cells)
    df_within = len(df) - cells.ngroups
    if df_within <= 0:
        return 0.001
    return ss_within / df_within


def omega2_interaction(df, f1="scoring", f2="pathogen", f3="family", dv="mcc"):
    """Type-II-like omega^2 for f1 x f2 interaction (3-way design).

    Identical decomposition to scripts/cluster_bootstrap_omega.py and
    scripts/wild_cluster_bootstrap_omega.py to keep the headline
    omega^2 = 0.296 reproducible across the four robustness frames.
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


# -----------------------------------------------------------------------------
# D5.1: Phylogenetic block bootstrap
# -----------------------------------------------------------------------------


def block_bootstrap(df: pd.DataFrame, blocks: dict[str, list[str]],
                    n_boot: int = N_BOOT, seed: int = SEED) -> np.ndarray:
    """Resample viral *families* with replacement; expand to pathogens.

    For each replicate we draw len(blocks) families with replacement
    (so the bootstrap-sample family count equals the original eight),
    then concatenate the rows of every pathogen in each sampled family.
    A duplicate-family draw appears multiple times in the resampled
    table (standard Efron-Tibshirani bootstrap on the block index set).
    omega^2 is recomputed on the resulting long table.
    """
    family_names = list(blocks.keys())
    g = len(family_names)
    rng = np.random.default_rng(seed)
    boot_omega = np.empty(n_boot, dtype=float)
    pathogen_subsets = {fam: df[df["pathogen"].isin(paths)].copy()
                        for fam, paths in blocks.items()}
    t0 = time.time()
    for b in range(n_boot):
        sampled = rng.choice(family_names, size=g, replace=True)
        # Concat each sampled family's rows; duplicates reappear.
        # Add a replicate index to keep the design identifiable when
        # the same pathogen recurs in a single bootstrap draw.
        parts = []
        for k, fam in enumerate(sampled):
            tbl = pathogen_subsets[fam].copy()
            tbl["pathogen"] = tbl["pathogen"].astype(str) + f"#rep{k}"
            parts.append(tbl)
        boot = pd.concat(parts, axis=0, ignore_index=True)
        boot_omega[b] = omega2_interaction(boot)
        if (b + 1) % 100 == 0:
            elapsed = time.time() - t0
            rate = (b + 1) / elapsed
            eta = (n_boot - b - 1) / rate
            print(f"  block-boot rep {b+1}/{n_boot} | "
                  f"rate {rate:.1f}/s | eta {eta:.0f}s")
    return boot_omega


# -----------------------------------------------------------------------------
# D5.2: Linear mixed-effects model
# -----------------------------------------------------------------------------


def fit_mixed_effects(df: pd.DataFrame) -> dict:
    """Fit MCC ~ scoring + (1|pathogen).

    Variance components: sigma^2_pathogen (random intercept),
    sigma^2_resid. ICC = sigma^2_path / (sigma^2_path + sigma^2_resid).

    For triangulation with the ANOVA omega^2(scoring x pathogen) we
    additionally fit a model with a (1|scoring:pathogen) random
    interaction term and report the variance attributed to that
    interaction; the bias-corrected pseudo-omega^2_int from the
    variance-component decomposition is the model-based companion to
    the percentile bootstrap CIs.
    """
    import statsmodels.formula.api as smf

    out: dict = {}

    # --- Model 0: unconditional pathogen RE (no scoring fixed effect) ---
    md_0 = smf.mixedlm("mcc ~ 1", data=df, groups=df["pathogen"])
    mdf_0 = md_0.fit(reml=True)
    var_pathogen0 = float(mdf_0.cov_re.iloc[0, 0])
    var_resid0 = float(mdf_0.scale)
    icc0 = var_pathogen0 / (var_pathogen0 + var_resid0) if \
        (var_pathogen0 + var_resid0) > 0 else 0.0
    out["model0_loglik"] = float(mdf_0.llf)
    out["model0_var_pathogen"] = var_pathogen0
    out["model0_var_resid"] = var_resid0
    out["model0_icc_pathogen"] = icc0

    # --- Model A: pathogen random intercept + scoring fixed effect ---
    md_a = smf.mixedlm("mcc ~ C(scoring)", data=df, groups=df["pathogen"])
    mdf_a = md_a.fit(reml=True)
    var_pathogen = float(mdf_a.cov_re.iloc[0, 0])
    var_resid = float(mdf_a.scale)
    icc = var_pathogen / (var_pathogen + var_resid) if \
        (var_pathogen + var_resid) > 0 else 0.0

    out["modelA_loglik"] = float(mdf_a.llf)
    out["modelA_var_pathogen"] = var_pathogen
    out["modelA_var_resid"] = var_resid
    out["modelA_icc_pathogen"] = icc
    out["modelA_aic"] = float(mdf_a.aic)
    out["modelA_bic"] = float(mdf_a.bic)
    out["modelA_converged"] = bool(mdf_a.converged)

    # --- Model B: nested (scoring:pathogen) random interaction ---
    # Crossed random effects in MixedLM require a non-trivial vc_formula
    # construction; we instead fit a pathogen + scoring:pathogen
    # variance-component model using the standard "groups + vc_formula"
    # idiom (Bates 2010-style).
    df2 = df.copy()
    df2["scoring_pathogen"] = (df2["scoring"].astype(str) + "_x_"
                                + df2["pathogen"].astype(str))
    vc = {"scoring_pathogen": "0 + C(scoring_pathogen)"}
    md_b = smf.mixedlm("mcc ~ C(scoring)", data=df2,
                       groups=df2["pathogen"],
                       vc_formula=vc, re_formula="1")
    try:
        mdf_b = md_b.fit(reml=True, maxiter=200)
        var_pathogen_b = float(mdf_b.cov_re.iloc[0, 0])
        # vc variance is in vcomp
        try:
            var_int_b = float(mdf_b.vcomp[0])
        except Exception:
            var_int_b = float("nan")
        var_resid_b = float(mdf_b.scale)
        total_b = var_pathogen_b + var_int_b + var_resid_b
        omega2_int_mixed = var_int_b / total_b if total_b > 0 else 0.0
        out["modelB_loglik"] = float(mdf_b.llf)
        out["modelB_var_pathogen"] = var_pathogen_b
        out["modelB_var_scoringXpathogen"] = var_int_b
        out["modelB_var_resid"] = var_resid_b
        out["modelB_omega2_int_mixed"] = omega2_int_mixed
        out["modelB_aic"] = float(mdf_b.aic)
        out["modelB_bic"] = float(mdf_b.bic)
        out["modelB_converged"] = bool(mdf_b.converged)
    except Exception as exc:
        out["modelB_error"] = repr(exc)
        out["modelB_omega2_int_mixed"] = float("nan")

    # --- Likelihood-ratio test: pathogen random intercept vs OLS null ---
    import statsmodels.api as sm
    ols = sm.OLS.from_formula("mcc ~ C(scoring)", data=df).fit()
    lr_stat = 2.0 * (mdf_a.llf - ols.llf)
    # 50:50 chi^2_0/chi^2_1 mixture for one-sided variance test
    # (Self & Liang 1987); take chi^2_1 p-value and halve.
    from scipy.stats import chi2
    p_lrt = 0.5 * (1.0 - chi2.cdf(lr_stat, df=1)) if lr_stat > 0 else 1.0
    out["lrt_stat_pathogen_vs_OLS"] = float(lr_stat)
    out["lrt_p_pathogen_vs_OLS"] = float(p_lrt)
    out["ols_loglik"] = float(ols.llf)

    return out


# -----------------------------------------------------------------------------
# Main
# -----------------------------------------------------------------------------


def main():
    print("Tier D5: phylogenetic block bootstrap + mixed-effects")
    print("=" * 72)
    if not INPUT.exists():
        sys.exit(f"missing input: {INPUT}")
    df = pd.read_csv(INPUT)
    df["pathogen"] = df["pathogen"].replace({"Influenza_B": "Influenza B"})
    print(f"Loaded {len(df)} rows; pathogens={df['pathogen'].nunique()}")

    # Sanity-check that every pathogen is assigned to a family.
    assigned = {p for paths in PHYLO_BLOCKS.values() for p in paths}
    missing = set(df["pathogen"].unique()) - assigned
    if missing:
        sys.exit(f"unassigned pathogens: {sorted(missing)}")
    print(f"Phylogenetic blocks: {len(PHYLO_BLOCKS)} viral families")
    for fam, paths in PHYLO_BLOCKS.items():
        print(f"  {fam:18s} {paths}")

    headline = omega2_interaction(df)
    print(f"\nHeadline omega^2(scoring x pathogen): {headline:.4f}")

    # ---- D5.1 phylogenetic block bootstrap ----
    print(f"\n[D5.1] Phylogenetic block bootstrap (B={N_BOOT}, seed={SEED}):")
    boot_block = block_bootstrap(df, PHYLO_BLOCKS, n_boot=N_BOOT, seed=SEED)
    bb_lo = float(np.percentile(boot_block, 2.5))
    bb_hi = float(np.percentile(boot_block, 97.5))
    bb_mean = float(boot_block.mean())
    bb_med = float(np.median(boot_block))
    p_zero_block = float(np.mean(boot_block <= 0.0))
    p_cohen_block = float(np.mean(boot_block <= 0.14))
    print(f"  mean omega^2     = {bb_mean:.4f}")
    print(f"  median           = {bb_med:.4f}")
    print(f"  95% percentile CI = [{bb_lo:.4f}, {bb_hi:.4f}]")
    print(f"  CI width         = {bb_hi - bb_lo:.4f}")
    print(f"  Pr(omega^2 <= 0)        = {p_zero_block:.4f}")
    print(f"  Pr(omega^2 <= 0.14)     = {p_cohen_block:.4f}")

    out_block = RESULTS / "block_bootstrap_omega.csv"
    pd.DataFrame({
        "iteration": np.arange(N_BOOT),
        "omega2_scoring_x_pathogen": boot_block,
    }).to_csv(out_block, index=False)
    print(f"  -> wrote {out_block}")

    block_summary = pd.DataFrame([{
        "bootstrap_method": "phylogenetic_block_family",
        "block_unit": "viral_family",
        "G_blocks": len(PHYLO_BLOCKS),
        "n_pathogens": df["pathogen"].nunique(),
        "B_replicates": N_BOOT,
        "omega2_point": round(headline, 4),
        "omega2_mean": round(bb_mean, 4),
        "omega2_median": round(bb_med, 4),
        "ci_lower_2p5": round(bb_lo, 4),
        "ci_upper_97p5": round(bb_hi, 4),
        "ci_width": round(bb_hi - bb_lo, 4),
        "p_omega2_le_0": round(p_zero_block, 4),
        "p_omega2_le_0p14_cohen": round(p_cohen_block, 4),
        "source_csv": "results/mutbench/block_bootstrap_omega.csv",
    }])
    out_block_sum = RESULTS / "block_bootstrap_omega_summary.csv"
    block_summary.to_csv(out_block_sum, index=False)
    print(f"  -> wrote {out_block_sum}")

    # ---- D5.2 mixed-effects ----
    print(f"\n[D5.2] Linear mixed-effects model:")
    mix = fit_mixed_effects(df)
    print(f"  Model A (pathogen RE only):")
    print(f"    var_pathogen = {mix['modelA_var_pathogen']:.6f}")
    print(f"    var_resid    = {mix['modelA_var_resid']:.6f}")
    print(f"    ICC          = {mix['modelA_icc_pathogen']:.4f}")
    print(f"    LRT vs OLS:  chi^2 = {mix['lrt_stat_pathogen_vs_OLS']:.3f}, "
          f"p = {mix['lrt_p_pathogen_vs_OLS']:.3e}")
    print(f"  Model B (pathogen RE + scoring:pathogen VC):")
    if "modelB_error" in mix:
        print(f"    error: {mix['modelB_error']}")
    else:
        print(f"    var_pathogen   = {mix['modelB_var_pathogen']:.6f}")
        print(f"    var_int        = {mix['modelB_var_scoringXpathogen']:.6f}")
        print(f"    var_resid      = {mix['modelB_var_resid']:.6f}")
        print(f"    omega^2_int_mix= {mix['modelB_omega2_int_mixed']:.4f}")

    mix_rows = [{"key": k, "value": v} for k, v in mix.items()]
    out_mix = RESULTS / "mixed_effects_omega_summary.csv"
    pd.DataFrame(mix_rows).to_csv(out_mix, index=False)
    print(f"  -> wrote {out_mix}")

    # ---- 4-way comparison table ----
    # Pull standard + wild from existing summary csv.
    wild_sum = pd.read_csv(RESULTS / "wild_cluster_bootstrap_omega_summary.csv")
    std_row = wild_sum[wild_sum["bootstrap_method"] ==
                       "standard_cluster_percentile"].iloc[0]
    wild_row = wild_sum[wild_sum["bootstrap_method"] ==
                        "wild_cluster_rademacher"].iloc[0]

    omega2_int_mixed = mix.get("modelB_omega2_int_mixed", float("nan"))

    rows = [
        {"method": "standard_cluster_percentile",
         "frame": "frequentist_bootstrap",
         "G_or_B": int(std_row["G_clusters"]),
         "omega2_point_or_mean": round(float(std_row["omega2_mean"]), 4),
         "ci_lower_2p5": round(float(std_row["ci_lower_2p5"]), 4),
         "ci_upper_97p5": round(float(std_row["ci_upper_97p5"]), 4),
         "ci_width": round(float(std_row["ci_width"]), 4),
         "notes": "cycle1; archive run, seed=42, B=1000"},
        {"method": "wild_cluster_rademacher",
         "frame": "frequentist_bootstrap",
         "G_or_B": int(wild_row["G_clusters"]),
         "omega2_point_or_mean": round(float(wild_row["omega2_mean"]), 4),
         "ci_lower_2p5": round(float(wild_row["ci_lower_2p5"]), 4),
         "ci_upper_97p5": round(float(wild_row["ci_upper_97p5"]), 4),
         "ci_width": round(float(wild_row["ci_width"]), 4),
         "notes": "cycle4 Tier B3; CGM 2008; seed=42, B=1000"},
        {"method": "phylogenetic_block_family",
         "frame": "frequentist_bootstrap",
         "G_or_B": len(PHYLO_BLOCKS),
         "omega2_point_or_mean": round(bb_mean, 4),
         "ci_lower_2p5": round(bb_lo, 4),
         "ci_upper_97p5": round(bb_hi, 4),
         "ci_width": round(bb_hi - bb_lo, 4),
         "notes": ("cycle5 Tier D5; Felsenstein 1985 spirit; "
                   "block=viral family; seed=42, B=1000")},
        {"method": "mixed_effects_pathogen_RE",
         "frame": "model_based",
         "G_or_B": df["pathogen"].nunique(),
         "omega2_point_or_mean": (round(omega2_int_mixed, 4)
                                  if not np.isnan(omega2_int_mixed)
                                  else float("nan")),
         "ci_lower_2p5": float("nan"),
         "ci_upper_97p5": float("nan"),
         "ci_width": float("nan"),
         "notes": ("cycle5 Tier D5; statsmodels MixedLM; "
                   "var-comp pseudo-omega^2; ICC_pathogen="
                   f"{mix['modelA_icc_pathogen']:.3f}; "
                   f"LRT p={mix['lrt_p_pathogen_vs_OLS']:.2e}")},
    ]
    fourway = pd.DataFrame(rows)
    out_4way = RESULTS / "omega_robustness_4way.csv"
    fourway.to_csv(out_4way, index=False)
    print(f"\n4-way robustness comparison written to {out_4way}")
    print(fourway.to_string(index=False))


if __name__ == "__main__":
    main()
