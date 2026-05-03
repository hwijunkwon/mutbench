#!/usr/bin/env python3
"""
Cycle 4 Perspective D — Counterfactual null sanity for omega^2 = 0.296.

Tests three counterfactual nulls:
  1. Pathogen-label permutation: shuffle pathogen column on the 8,580 grid,
     recompute scoring x pathogen interaction omega^2.
  2. Score-shuffle: shuffle scoring column.
  3. Family-shuffle (control): shuffle family column.

If the observed omega^2 = 0.296 sits in the upper tail of the pathogen-label
null distribution, the interaction reflects genuine pathogen-specific
benchmark behavior. If it sits near the middle, the headline is plausibly
panel-heterogeneity artefact under the same evaluation protocol.

Usage:
  python3 scripts/cycle4_counterfactual_null.py
Output:
  results/mutbench/cycle4_counterfactual_null.csv
"""
import sys
from pathlib import Path

import numpy as np
import pandas as pd
from statsmodels.formula.api import ols
from statsmodels.stats.anova import anova_lm


ROOT = Path("/proj/paper")
GRID_CSV = ROOT / "results" / "mutbench" / "stage3_full_results.csv"
OUT_CSV = ROOT / "results" / "mutbench" / "cycle4_counterfactual_null.csv"
SEED = 42
N_PERM = 200


def omega2_interaction(df: pd.DataFrame) -> float:
    """Compute omega^2 for the C(scoring):C(pathogen) interaction.

    Uses the same three-way ANOVA structure as the dissertation:
      mcc ~ C(scoring) + C(family) + C(pathogen) + C(scoring):C(pathogen) + C(family):C(pathogen)
    """
    f = (
        "mcc ~ C(scoring) + C(family) + C(pathogen) "
        "+ C(scoring):C(pathogen) + C(family):C(pathogen)"
    )
    model = ols(f, df).fit()
    a = anova_lm(model, typ=2)
    ms_res = a.loc["Residual", "sum_sq"] / a.loc["Residual", "df"]
    ss_tot = ((df.mcc - df.mcc.mean()) ** 2).sum()
    row = "C(scoring):C(pathogen)"
    omega2 = (a.loc[row, "sum_sq"] - a.loc[row, "df"] * ms_res) / (ss_tot + ms_res)
    return float(omega2)


def run_null(df: pd.DataFrame, mode: str, n_perm: int, seed: int) -> np.ndarray:
    """Run n_perm permutations under the given null mode."""
    rng = np.random.default_rng(seed)
    out = np.empty(n_perm)
    for b in range(n_perm):
        g = df.copy()
        if mode == "pathogen":
            g["pathogen"] = rng.permutation(g["pathogen"].to_numpy())
        elif mode == "scoring":
            g["scoring"] = rng.permutation(g["scoring"].to_numpy())
        elif mode == "family":
            g["family"] = rng.permutation(g["family"].to_numpy())
        else:
            raise ValueError(f"unknown mode: {mode}")
        out[b] = omega2_interaction(g)
        if (b + 1) % 50 == 0:
            print(f"  {mode} permutation {b+1}/{n_perm}", file=sys.stderr)
    return out


def main():
    df = pd.read_csv(GRID_CSV)
    print(f"Loaded {len(df)} rows from {GRID_CSV.name}")
    print(f"Pathogens: {df.pathogen.nunique()}; scorings: {df.scoring.nunique()}; "
          f"families: {df.family.nunique()}")

    obs = omega2_interaction(df)
    print(f"Observed omega^2(scoring x pathogen) = {obs:.4f}")
    print(f"  Manuscript headline: 0.296 (cell-level 0.234)")

    rows = []
    for mode in ["pathogen", "scoring", "family"]:
        print(f"\nRunning {N_PERM} permutations under '{mode}' null ...")
        null_dist = run_null(df, mode, N_PERM, SEED)
        q025, q975 = np.quantile(null_dist, [0.025, 0.975])
        median = float(np.median(null_dist))
        mean = float(np.mean(null_dist))
        # one-sided p: fraction of null >= observed (large omega^2)
        p_one_sided = float((null_dist >= obs).sum() + 1) / (N_PERM + 1)
        print(f"  null median = {median:.4f}, mean = {mean:.4f}, "
              f"95% interval [{q025:.4f}, {q975:.4f}], "
              f"one-sided p (null >= obs) = {p_one_sided:.4f}")
        rows.append({
            "null_mode": mode,
            "n_perm": N_PERM,
            "observed_omega2": obs,
            "null_median": median,
            "null_mean": mean,
            "null_lower_2.5": q025,
            "null_upper_97.5": q975,
            "p_one_sided_null_ge_obs": p_one_sided,
            "verdict": "obs above null upper" if obs > q975 else (
                "obs within null 95%" if obs >= q025 else "obs below null lower"
            ),
            "seed": SEED,
        })

    out = pd.DataFrame(rows)
    OUT_CSV.parent.mkdir(parents=True, exist_ok=True)
    out.to_csv(OUT_CSV, index=False)
    print(f"\nWrote {OUT_CSV}")
    print(out.to_string(index=False))


if __name__ == "__main__":
    main()
