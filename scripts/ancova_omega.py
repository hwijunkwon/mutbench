#!/usr/bin/env python3
"""ANCOVA on the cell-level Stage 3 grid.

Fit a statsmodels Type II OLS ANCOVA with two pathogen-constant continuous
covariates -- log(alignment length) and Layer A positive rate -- and the
three categorical factors used in the headline ANOVA (scoring, family,
pathogen) plus the load-bearing scoring x pathogen and family x pathogen
interactions. Compute non-partial omega^2 for each ANOVA term and report
the directional shift relative to the unconditional cell-level baseline.

Inputs:
  results/mutbench/stage3_full_results.csv  (8,580 rows)
  per-pathogen alignment lengths (hard-coded below from Table 3.1)
  per-pathogen Layer A positive rate (hard-coded below from Table 3.2)

Outputs:
  results/mutbench/ancova_omega_summary.csv

The dissertation Section 3 ANCOVA paragraph cites this script for the
claims pathogen main effect omega^2 0.108 -> ~0 and scoring x pathogen
0.234 -> 0.264 after adjustment.
"""

import math
from pathlib import Path

import numpy as np
import pandas as pd
import statsmodels.api as sm
import statsmodels.formula.api as smf
from statsmodels.stats.anova import anova_lm

ROOT = Path(__file__).resolve().parent.parent
INPUT = ROOT / "results" / "mutbench" / "stage3_full_results.csv"
OUT = ROOT / "results" / "mutbench" / "ancova_omega_summary.csv"

ALIGN_LEN = {
    "SARS-CoV-2": 1259, "H3N2": 543, "Norovirus": 536, "HIV-1": 450,
    "Dengue": 490, "RSV": 550, "Influenza_B": 560, "MERS": 1330,
    "HCV": 340, "Rabies": 491, "EV-A71": 261,
}
LAYER_A_POS_COUNT = {
    "SARS-CoV-2": 25, "H3N2": 25, "Norovirus": 15, "HIV-1": 23,
    "Dengue": 24, "RSV": 20, "Influenza_B": 17, "MERS": 9,
    "HCV": 54, "Rabies": 39, "EV-A71": 27,
}


def omega_squared(anova_table, term):
    """Non-partial omega^2 with SS_total + MS_error denominator."""
    ss_term = anova_table.loc[term, "sum_sq"]
    df_term = anova_table.loc[term, "df"]
    ms_err = anova_table.loc["Residual", "sum_sq"] / anova_table.loc["Residual", "df"]
    ss_total = anova_table["sum_sq"].sum()
    return (ss_term - df_term * ms_err) / (ss_total + ms_err)


def fit(df, formula, label):
    model = smf.ols(formula, data=df).fit()
    table = anova_lm(model, typ=2)
    return {
        term: omega_squared(table, term)
        for term in table.index if term != "Residual"
    }, table


def main():
    df = pd.read_csv(INPUT)
    cell = df.groupby(["pathogen", "scoring", "family"], as_index=False)["mcc"].mean()
    cell["log_align_len"] = cell["pathogen"].map(lambda p: math.log(ALIGN_LEN[p]))
    cell["layer_a_rate"] = cell["pathogen"].map(
        lambda p: LAYER_A_POS_COUNT[p] / ALIGN_LEN[p]
    )

    print(f"Cell-level grid: {cell.shape[0]} rows ({cell['pathogen'].nunique()} pathogens"
          f" x {cell['scoring'].nunique()} scoring x {cell['family'].nunique()} family)")

    base_formula = (
        "mcc ~ C(scoring) + C(family) + C(pathogen)"
        " + C(scoring):C(pathogen) + C(family):C(pathogen)"
    )
    base_omega, base_table = fit(cell, base_formula, "baseline")

    # ANCOVA: replace the categorical pathogen *main effect* with the two
    # pathogen-constant continuous covariates. Pathogen still enters via
    # the load-bearing scoring x pathogen and family x pathogen
    # interactions, so the rise in those interactions under adjustment
    # is the directional quantity reported in the dissertation. This
    # follows the convention that covariates "absorb" the pathogen
    # main-effect variance they were chosen to proxy (alignment depth
    # and Layer A density).
    ancova_formula = (
        "mcc ~ C(scoring) + C(family) + log_align_len + layer_a_rate"
        " + C(scoring):C(pathogen) + C(family):C(pathogen)"
    )
    ancova_omega, ancova_table = fit(cell, ancova_formula, "ancova")

    rows = []
    terms_of_interest = [
        "C(scoring)", "C(family)", "C(pathogen)",
        "C(scoring):C(pathogen)", "C(family):C(pathogen)",
    ]
    for term in terms_of_interest:
        rows.append({
            "term": term,
            "omega2_baseline": base_omega.get(term, float("nan")),
            "omega2_ancova": ancova_omega.get(term, float("nan")),
            "delta": ancova_omega.get(term, 0) - base_omega.get(term, 0),
        })
    out = pd.DataFrame(rows)
    out.to_csv(OUT, index=False)

    pd.set_option("display.float_format", lambda x: f"{x:+.4f}")
    print("\n=== Cell-level baseline (no covariates) ===")
    print(base_table.round(4))
    print("\n=== ANCOVA (log align len + Layer A rate as covariates) ===")
    print(ancova_table.round(4))
    print("\n=== omega^2 summary ===")
    print(out.to_string(index=False))
    print(f"\nWrote {OUT}")


if __name__ == "__main__":
    main()
