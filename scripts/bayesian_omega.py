#!/usr/bin/env python3
"""Bayesian hierarchical posterior for omega^2(scoring x pathogen).

Cell-level Normal hierarchical model on the 3{,}080 (scoring x family x
pathogen) cell means:
  y_{ij} = mu + alpha_i + beta_j + gamma_{ij} + eps_{ij}
where alpha_i ~ N(0, sigma_alpha^2), beta_j ~ N(0, sigma_beta^2),
gamma_{ij} ~ N(0, sigma_gamma^2), eps_{ij} ~ N(0, sigma^2).
omega^2_int = sigma_gamma^2 / (sigma_alpha^2 + sigma_beta^2 +
              sigma_gamma^2 + sigma^2).

Body claim (ch5:285): posterior mean omega^2_int ~ 0.252,
95% HDI [0.188, 0.314], P(omega^2_int > 0.14) ~ 0.996.

Outputs:
  results/mutbench/bayesian_omega_summary.csv
  results/mutbench/bayesian_omega_posterior.csv
"""

from __future__ import annotations

import os
import sys
from pathlib import Path

os.environ.setdefault("PYTENSOR_FLAGS", "compiledir_format=compiledir_%(short_platform)s")

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


def main():
    print("Bayesian hierarchical omega^2 posterior")
    print("=" * 70)
    df = pd.read_csv(INPUT)
    df["pathogen"] = df["pathogen"].replace({"Influenza_B": "Influenza B"})

    # Evaluation-level: 8,580 observations (20 scoring x 14 family x 11 pathogen)
    print(f"Evaluation-level dataset: {len(df)} rows "
          f"({df['scoring'].nunique()} scoring x {df['pathogen'].nunique()} pathogen)")

    scoring_idx = pd.Categorical(df["scoring"]).codes
    pathogen_idx = pd.Categorical(df["pathogen"]).codes
    n_scoring = int(scoring_idx.max() + 1)
    n_pathogen = int(pathogen_idx.max() + 1)
    y = df["mcc"].astype(float).values

    with pm.Model() as model:
        sigma_alpha = pm.HalfNormal("sigma_alpha", sigma=0.2)
        sigma_beta = pm.HalfNormal("sigma_beta", sigma=0.2)
        sigma_gamma = pm.HalfNormal("sigma_gamma", sigma=0.2)
        sigma = pm.HalfNormal("sigma", sigma=0.2)

        mu = pm.Normal("mu", 0.0, 0.5)
        alpha = pm.Normal("alpha", 0.0, sigma_alpha, shape=n_scoring)
        beta = pm.Normal("beta", 0.0, sigma_beta, shape=n_pathogen)
        gamma = pm.Normal(
            "gamma", 0.0, sigma_gamma,
            shape=(n_scoring, n_pathogen),
        )

        mu_ij = mu + alpha[scoring_idx] + beta[pathogen_idx] + gamma[scoring_idx, pathogen_idx]
        pm.Normal("y", mu=mu_ij, sigma=sigma, observed=y)

        omega2_int = pm.Deterministic(
            "omega2_int",
            sigma_gamma**2 / (sigma_alpha**2 + sigma_beta**2 + sigma_gamma**2 + sigma**2),
        )

        idata = pm.sample(
            draws=DRAWS, tune=TUNE, chains=CHAINS,
            random_seed=SEED, progressbar=False, target_accept=0.9,
        )

    posterior = idata.posterior["omega2_int"].values.flatten()
    summary_row = {
        "protocol": "bayesian_hierarchical_evaluation_level",
        "n_observations": len(df),
        "posterior_mean_omega2_int": float(posterior.mean()),
        "posterior_median": float(np.median(posterior)),
        "hdi_lo_95": float(az.hdi(posterior, hdi_prob=0.95)[0]),
        "hdi_hi_95": float(az.hdi(posterior, hdi_prob=0.95)[1]),
        "P_gt_0.14": float((posterior > 0.14).mean()),
        "P_gt_0.10": float((posterior > 0.10).mean()),
        "P_gt_0.20": float((posterior > 0.20).mean()),
        "draws": DRAWS, "tune": TUNE, "chains": CHAINS, "seed": SEED,
        "body_target_mean": 0.252,
        "body_target_hdi": "[0.188, 0.314]",
        "body_target_P_gt_0.14": 0.996,
    }
    print("\nPosterior summary:")
    for k, v in summary_row.items():
        print(f"  {k:<32s} = {v}")

    pd.DataFrame([summary_row]).to_csv(RESULTS / "bayesian_omega_summary.csv", index=False)
    pd.DataFrame({"omega2_int_draw": posterior}).to_csv(RESULTS / "bayesian_omega_posterior.csv", index=False)
    print(f"\nSaved CSVs in {RESULTS}")


if __name__ == "__main__":
    main()
