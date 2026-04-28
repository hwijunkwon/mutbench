#!/usr/bin/env python3
"""Aligned Rank Transform (ART) ANOVA for omega^2(scoring x pathogen).

Wobbrock et al. 2011, "The Aligned Rank Transform for Nonparametric
Factorial Analyses Using Only ANOVA Procedures."

For the scoring x pathogen interaction:
  1. Fit OLS Y ~ scoring + pathogen (main effects only).
  2. Compute aligned response Y_aligned = Y - fitted + grand_mean.
     This removes main-effect contributions, isolating the
     interaction + residual.
  3. Rank-transform Y_aligned.
  4. Refit OLS rank ~ scoring + pathogen + scoring:pathogen.
  5. Compute omega^2 for the interaction using the SS-based
     non-partial form to match the body's `analyze_stage3_stats.py`.

Body claim: ART omega^2(scoring x pathogen) = 0.277 (ch3:825 / ch3:889).

Outputs:
  results/mutbench/art_omega.csv
"""

from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd
from scipy.stats import rankdata
import statsmodels.formula.api as smf
import statsmodels.api as sm

PROJECT = Path(__file__).resolve().parent.parent
RESULTS = PROJECT / "results" / "mutbench"
INPUT = RESULTS / "stage3_full_results.csv"


def omega2_from_ss(ss_effect, df_effect, ms_resid, ss_total):
    """Non-partial omega^2 used by analyze_stage3_stats.py."""
    if ss_total + ms_resid < 1e-12:
        return 0.0
    return max(0.0, (ss_effect - df_effect * ms_resid) / (ss_total + ms_resid))


def art_interaction_omega(df, f1="scoring", f2="pathogen", dv="mcc"):
    """Compute ART omega^2 for the f1 x f2 interaction.

    Aligning step removes f1 and f2 main effects (and grand mean) so the
    aligned response carries only the interaction + residual.
    """
    df = df.copy()
    df["_y"] = df[dv].astype(float)
    grand_mean = df["_y"].mean()

    # Step 1: fit main-effects-only model
    main_model = smf.ols(f"_y ~ C({f1}) + C({f2})", data=df).fit()
    # Step 2: align (subtract main-effect fit, add grand mean back)
    df["_y_aligned"] = df["_y"] - main_model.fittedvalues + grand_mean
    # Step 3: rank-transform aligned response
    df["_rank"] = rankdata(df["_y_aligned"].values)

    # Step 4: refit full model with interaction on the ranks
    full_model = smf.ols(f"_rank ~ C({f1}) + C({f2}) + C({f1}):C({f2})", data=df).fit()
    aov = sm.stats.anova_lm(full_model, typ=2)
    interaction_term = f"C({f1}):C({f2})"
    if interaction_term not in aov.index:
        # statsmodels formats interaction labels as C(a):C(b); fall back
        for k in aov.index:
            if (f1 in k) and (f2 in k) and (":" in k):
                interaction_term = k
                break
    ss_int = float(aov.loc[interaction_term, "sum_sq"])
    df_int = float(aov.loc[interaction_term, "df"])
    ss_resid = float(aov.loc["Residual", "sum_sq"])
    df_resid = float(aov.loc["Residual", "df"])
    ms_resid = ss_resid / df_resid if df_resid > 0 else 1e-3
    ss_total = float(np.sum((df["_rank"] - df["_rank"].mean()) ** 2))

    omega2 = omega2_from_ss(ss_int, df_int, ms_resid, ss_total)
    return omega2, ss_int, df_int, ms_resid, ss_total


def main():
    print("ART (Aligned Rank Transform) omega^2(scoring x pathogen)")
    print("=" * 70)
    df = pd.read_csv(INPUT)
    df["pathogen"] = df["pathogen"].replace({"Influenza_B": "Influenza B"})

    # Headline ART
    om, ss_int, df_int, ms_resid, ss_total = art_interaction_omega(df)
    print(f"ART omega^2(scoring x pathogen) on full panel: {om:.4f}")
    print(f"  SS_int={ss_int:.2f}  df_int={df_int}  MS_resid={ms_resid:.4f}  SS_total={ss_total:.2f}")
    print(f"  Body target (ch3:825/889): 0.277")

    # Sensitivity: HCV-excluded
    df_hcv = df[df["pathogen"] != "HCV"]
    om_hcv, *_ = art_interaction_omega(df_hcv)
    print(f"\nART HCV-excluded: omega^2 = {om_hcv:.4f}")

    # Sensitivity: 4-phylo-only (SARS, H3N2, MERS, EV-A71)
    df_phylo = df[df["pathogen"].isin(["SARS-CoV-2", "H3N2", "MERS", "EV-A71"])]
    om_phylo, *_ = art_interaction_omega(df_phylo)
    print(f"ART 4-phylo-only: omega^2 = {om_phylo:.4f}")

    out = pd.DataFrame([
        {"protocol": "ART_full_panel", "n_pathogens": df["pathogen"].nunique(),
         "omega2": float(om), "ss_int": ss_int, "df_int": df_int,
         "ms_resid": ms_resid, "ss_total": ss_total, "body_target": 0.277},
        {"protocol": "ART_HCV_excluded", "n_pathogens": df_hcv["pathogen"].nunique(),
         "omega2": float(om_hcv), "ss_int": np.nan, "df_int": np.nan,
         "ms_resid": np.nan, "ss_total": np.nan, "body_target": np.nan},
        {"protocol": "ART_4phylo_only", "n_pathogens": df_phylo["pathogen"].nunique(),
         "omega2": float(om_phylo), "ss_int": np.nan, "df_int": np.nan,
         "ms_resid": np.nan, "ss_total": np.nan, "body_target": np.nan},
    ])
    out.to_csv(RESULTS / "art_omega.csv", index=False)
    print(f"\nSaved {RESULTS / 'art_omega.csv'}")


if __name__ == "__main__":
    main()
