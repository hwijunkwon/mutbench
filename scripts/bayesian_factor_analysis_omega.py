#!/usr/bin/env python3
"""Tier E1: Bayesian factor analysis posterior for omega^2(scoring x pathogen).

This script extends the cycle-5 Tier D5 4-way robustness frame
(standard cluster, wild-cluster, phylogenetic block, mixed-effects)
to a 5-way frame by adding a Bayesian *factor analysis* posterior on
the 20 (scoring) x 11 (pathogen) matrix of cell-mean MCC values.

Model (two-way factor structure on the 20 x 11 design):
    y_{ijk} ~ Normal(mu + alpha_i + beta_j + gamma_{ij}, sigma_residual)
    alpha_i  ~ Normal(0, sigma_scoring)         scoring  factor    (i=1..20)
    beta_j   ~ Normal(0, sigma_pathogen)        pathogen factor    (j=1..11)
    gamma_ij ~ Normal(0, sigma_interaction)     scoring x pathogen (i,j)

The model is fit on the evaluation-level (8,580 row) MCC values so
that the within-cell residual variance is identifiable separately
from the scoring x pathogen interaction variance (single observation
per cell would otherwise collapse the two onto the same likelihood).
Non-centered (Matt-trick) parameterization is used for the factor
effects to mitigate Neal's funnel between sigma_* and the
corresponding raw effects (Betancourt and Girolami, 2015).

omega^2_int posterior:
    omega^2_int = sigma_interaction^2 /
                  (sigma_scoring^2 + sigma_pathogen^2
                   + sigma_interaction^2 + sigma_residual^2)

Distinguishing features versus the existing evaluation-level Bayesian
hierarchical model (scripts/bayesian_omega.py, 8580 obs, half-Normal(0.2)
priors, *three-way* (scoring + family + pathogen + scoring x pathogen)
decomposition):
  (i) two-way *factor* decomposition that folds the family axis into
      the residual term, focusing the variance partition on the
      load-bearing scoring x pathogen interaction (this is the same
      20x11 design that underlies the four frequentist frames in
      omega_robustness_4way.csv);
  (ii) hyperprior scales of HalfNormal(0.5) on the variance components
       and HalfNormal(0.2) on the residual, encoding a prior belief
       that the cell-level MCC scale is O(0.1) but allowing the
       factor variances to reach O(1) without truncation;
  (iii) wider prior on mu (Normal(0, 1)) so that the grand-mean
        location is data-driven rather than prior-driven;
  (iv) non-centered reparameterization for stability at small group
       counts (n_pathogen = 11).

Outputs:
  results/mutbench/bayesian_factor_omega_summary.csv       1-row summary
  results/mutbench/bayesian_factor_omega_posterior.csv     post draws
  results/mutbench/omega_robustness_5way.csv               5-method table

References:
  Cameron, Gelbach, Miller (2008) Bootstrap-Based Improvements for
    Inference with Clustered Errors. ReStat 90(3): 414-427.
  Felsenstein (1985) Phylogenies and the comparative method.
    Am Nat 125(1): 1-15.
  Bolker et al. (2009) GLMMs in ecology and evolution. TREE 24(3):
    127-135.
  Gelman & Hill (2007) Data Analysis Using Regression and
    Multilevel/Hierarchical Models. Cambridge UP. (factor structure
    interpretation of two-way random ANOVA.)
"""

from __future__ import annotations

import os
import sys
from pathlib import Path

os.environ.setdefault(
    "PYTENSOR_FLAGS", "compiledir_format=compiledir_%(short_platform)s"
)

import numpy as np
import pandas as pd
import pymc as pm
import arviz as az

PROJECT = Path(__file__).resolve().parent.parent
RESULTS = PROJECT / "results" / "mutbench"
INPUT = RESULTS / "stage3_full_results.csv"

DRAWS = 2000
TUNE = 2000
CHAINS = 4
SEED = 42


def main() -> int:
    print("Tier E1: Bayesian factor analysis omega^2 posterior")
    print("=" * 72)
    if not INPUT.exists():
        sys.exit(f"missing input: {INPUT}")
    df = pd.read_csv(INPUT)
    df["pathogen"] = df["pathogen"].replace({"Influenza_B": "Influenza B"})
    print(f"Loaded {len(df)} rows; "
          f"{df['scoring'].nunique()} scoring x "
          f"{df['pathogen'].nunique()} pathogen")

    # Bayesian factor analysis is fit on the *evaluation-level* (8,580
    # row) MCC values rather than the 220-cell mean matrix because the
    # within-cell residual variance is otherwise non-identifiable from
    # the scoring x pathogen interaction variance (single observation
    # per cell collapses sigma_int and sigma_residual onto the same
    # likelihood). This matches the existing bayesian_omega.py
    # evaluation-level design but drops the family axis to focus on
    # the load-bearing scoring x pathogen factor structure: the omega^2
    # of interest is computed directly from the (scoring, pathogen)
    # variance components rather than from a three-way decomposition.
    n_scoring = df["scoring"].nunique()
    n_pathogen = df["pathogen"].nunique()
    scoring_cats = pd.Categorical(df["scoring"])
    pathogen_cats = pd.Categorical(df["pathogen"])
    scoring_idx = scoring_cats.codes.astype(int)
    pathogen_idx = pathogen_cats.codes.astype(int)
    y = df["mcc"].astype(float).values

    print(f"Factor analysis design: {n_scoring} scoring x "
          f"{n_pathogen} pathogen, {len(df)} evaluation rows")
    print(f"y mean={y.mean():.4f}, sd={y.std(ddof=1):.4f}, "
          f"min={y.min():.4f}, max={y.max():.4f}")

    with pm.Model() as model:
        # Hyperpriors for factor scales (variance components).
        # HalfNormal(0.5) is weakly informative on the factor sd scale
        # given that |mcc| < 1 by definition. The residual scale uses
        # a tighter HalfNormal(0.2) reflecting the within-cell mcc
        # spread observed across the 39 detector parameter variants.
        sigma_scoring = pm.HalfNormal("sigma_scoring", sigma=0.5)
        sigma_pathogen = pm.HalfNormal("sigma_pathogen", sigma=0.5)
        sigma_interaction = pm.HalfNormal("sigma_interaction", sigma=0.5)
        sigma_residual = pm.HalfNormal("sigma_residual", sigma=0.2)

        # Grand mean.
        mu = pm.Normal("mu", 0.0, 1.0)

        # Non-centered (Matt Trick) parameterization for the factor
        # effects to mitigate Neal's funnel between sigma_* and the
        # corresponding raw effects. This is the standard cure for the
        # divergent transitions that appear in centered hierarchical
        # models when group sizes are small (Betancourt and Girolami,
        # 2015; PyMC documentation, Reparameterization page).
        scoring_eff_raw = pm.Normal("scoring_eff_raw", 0.0, 1.0,
                                    shape=n_scoring)
        pathogen_eff_raw = pm.Normal("pathogen_eff_raw", 0.0, 1.0,
                                     shape=n_pathogen)
        interaction_eff_raw = pm.Normal("interaction_eff_raw", 0.0, 1.0,
                                        shape=(n_scoring, n_pathogen))

        scoring_eff = pm.Deterministic(
            "scoring_eff", sigma_scoring * scoring_eff_raw)
        pathogen_eff = pm.Deterministic(
            "pathogen_eff", sigma_pathogen * pathogen_eff_raw)
        interaction_eff = pm.Deterministic(
            "interaction_eff", sigma_interaction * interaction_eff_raw)

        # Linear predictor (evaluation-level: 8,580 rows).
        mu_ij = (mu + scoring_eff[scoring_idx] + pathogen_eff[pathogen_idx]
                 + interaction_eff[scoring_idx, pathogen_idx])

        # Observation likelihood. The residual sigma_residual absorbs
        # within-cell variance from the 39 detector parameter variants
        # (the family axis is intentionally folded into residual to
        # focus the variance decomposition on the load-bearing
        # scoring x pathogen interaction).
        pm.Normal("y", mu=mu_ij, sigma=sigma_residual, observed=y)

        # omega^2_int posterior derived deterministically.
        omega2_int = pm.Deterministic(
            "omega2_int",
            sigma_interaction**2 / (
                sigma_scoring**2 + sigma_pathogen**2
                + sigma_interaction**2 + sigma_residual**2
            ),
        )

        idata = pm.sample(
            draws=DRAWS, tune=TUNE, chains=CHAINS,
            random_seed=SEED, progressbar=False, target_accept=0.95,
            return_inferencedata=True,
        )

    # Posterior summary.
    posterior = idata.posterior["omega2_int"].values.flatten()
    post_mean = float(posterior.mean())
    post_median = float(np.median(posterior))
    hdi_lo, hdi_hi = az.hdi(posterior, hdi_prob=0.95)
    p_gt_014 = float((posterior > 0.14).mean())
    p_gt_010 = float((posterior > 0.10).mean())
    p_gt_020 = float((posterior > 0.20).mean())

    # Convergence diagnostics.
    summ = az.summary(
        idata, var_names=[
            "omega2_int", "sigma_scoring", "sigma_pathogen",
            "sigma_interaction", "sigma_residual",
        ],
        round_to=6,
    )
    print("\nConvergence diagnostics (R-hat / ESS):")
    print(summ.to_string())

    rhat_omega = float(summ.loc["omega2_int", "r_hat"])
    ess_bulk_omega = float(summ.loc["omega2_int", "ess_bulk"])
    ess_tail_omega = float(summ.loc["omega2_int", "ess_tail"])

    summary_row = {
        "protocol": "bayesian_factor_analysis_evaluation_level",
        "n_observations": len(df),
        "n_scoring": n_scoring,
        "n_pathogen": n_pathogen,
        "posterior_mean_omega2_int": post_mean,
        "posterior_median": post_median,
        "hdi_lo_95": float(hdi_lo),
        "hdi_hi_95": float(hdi_hi),
        "P_gt_0.14": p_gt_014,
        "P_gt_0.10": p_gt_010,
        "P_gt_0.20": p_gt_020,
        "rhat_omega": rhat_omega,
        "ess_bulk_omega": ess_bulk_omega,
        "ess_tail_omega": ess_tail_omega,
        "draws": DRAWS, "tune": TUNE, "chains": CHAINS, "seed": SEED,
        "prior_sigma_factors": "HalfNormal(0.5)",
        "prior_sigma_residual": "HalfNormal(0.2)",
        "prior_mu": "Normal(0, 1)",
    }
    print("\nPosterior summary:")
    for k, v in summary_row.items():
        print(f"  {k:<32s} = {v}")

    pd.DataFrame([summary_row]).to_csv(
        RESULTS / "bayesian_factor_omega_summary.csv", index=False
    )
    pd.DataFrame({"omega2_int_draw": posterior}).to_csv(
        RESULTS / "bayesian_factor_omega_posterior.csv", index=False
    )
    print(f"\nSaved CSVs in {RESULTS}")

    # ---- 5-way robustness comparison ----
    fourway = pd.read_csv(RESULTS / "omega_robustness_4way.csv")
    bayes_row = pd.DataFrame([{
        "method": "bayesian_factor_analysis",
        "frame": "bayesian_posterior",
        "G_or_B": n_pathogen,
        "omega2_point_or_mean": round(post_mean, 4),
        "ci_lower_2p5": round(float(hdi_lo), 4),
        "ci_upper_97p5": round(float(hdi_hi), 4),
        "ci_width": round(float(hdi_hi - hdi_lo), 4),
        "notes": ("cycle6 Tier E1; PyMC 5.28; evaluation-level 20x11 "
                  "factor analysis (family axis folded into residual); "
                  f"HalfNormal(0.5/0.2) priors; non-centered; "
                  f"{CHAINS} chains x {DRAWS} draws; seed={SEED}; "
                  f"R-hat={rhat_omega:.3f}; "
                  f"ESS_bulk={ess_bulk_omega:.0f}; "
                  f"P(omega^2>0.14)={p_gt_014:.4f}"),
    }])
    fiveway = pd.concat([fourway, bayes_row], axis=0, ignore_index=True)
    out_5way = RESULTS / "omega_robustness_5way.csv"
    fiveway.to_csv(out_5way, index=False)
    print(f"\n5-way robustness comparison written to {out_5way}")
    print(fiveway.to_string(index=False))
    return 0


if __name__ == "__main__":
    sys.exit(main())
