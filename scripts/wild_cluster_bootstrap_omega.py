#!/usr/bin/env python3
"""Wild-cluster bootstrap CI for omega^2(scoring x pathogen).

This script implements the Cameron, Gelbach & Miller (2008) wild-cluster
bootstrap as a sharper alternative to the standard cluster-resampling
percentile bootstrap in the small-cluster regime (G = 11 pathogens).

Method (CGM 2008, Section 4.1; "wild cluster bootstrap-T"):
  1. Fit the full three-way ANOVA model (scoring + family + pathogen
     + scoring:family + scoring:pathogen + family:pathogen) on the
     8,580-row evaluation grid under the *restricted* null on the
     scoring:pathogen interaction (i.e., the headline interaction is
     dropped from the design matrix); obtain fitted values yhat and
     residuals e.
  2. For each of B replicates, draw a Rademacher weight w_g in {-1, +1}
     for each cluster (pathogen) g, and build the wild bootstrap response
            y*_{ij} = yhat_{ij} + w_{g(ij)} * e_{ij}
     where g(ij) is the pathogen of observation (ij). All observations
     in the same cluster share the same Rademacher sign, which preserves
     within-cluster dependence (the headline concern noted in ch3:916
     and ch5:289).
  3. Recompute omega^2(scoring x pathogen) from the same Type-II-like
     decomposition used in scripts/cluster_bootstrap_omega.py and
     scripts/analyze_stage3_stats.py, replacing the dependent variable
     mcc with y*. This gives the wild-bootstrap distribution of
     omega^2_{int}.
  4. Report the 95% percentile interval of the wild-bootstrap omega^2 and
     the bootstrap p-value Pr(omega2_wild <= 0).

Comparison target (ch4:529, ch3:958, ch5:289):
  Standard cluster bootstrap: omega^2_int = 0.296,
      95% percentile CI = [0.195, 0.333] (1,000 resamples; the
      archive run reported [0.201, 0.346] with random_seed=42).
  Headline body claim: 0.296.

Outputs:
  results/mutbench/wild_cluster_bootstrap_omega.csv
      per-replicate omega^2_int.
  results/mutbench/wild_cluster_bootstrap_omega_summary.csv
      side-by-side comparison: standard vs wild-cluster.

Anti-conservative caveat: the wild-cluster CI is expected to be wider
than the standard percentile CI in the small-G regime (CGM 2008,
Tables 2-3). A wider interval that still excludes Cohen's large-effect
threshold (omega^2 = 0.14) provides honest robustness corroboration.
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

# Replicate count: B = 1000 keeps wall time comparable to the existing
# standard cluster bootstrap (cluster_bootstrap_omega.py uses N_BOOT = 1000
# at random_seed=42); this is sufficient for stable percentile-CI
# estimation at G = 11 (Davidson & MacKinnon 2010) and is the same
# replicate count as the archive standard run we are comparing against.
N_BOOT = 1000
SEED = 42


def _ms_residual(df, factors, dv="mcc"):
    cells = df.groupby(factors, observed=True)[dv]
    ss_within = sum(((g - g.mean()) ** 2).sum() for _, g in cells)
    df_within = len(df) - cells.ngroups
    if df_within <= 0:
        return 0.001
    return ss_within / df_within


def omega2_interaction(df, f1="scoring", f2="pathogen", f3="family", dv="mcc"):
    """Type-II-like omega^2 for f1 x f2 interaction (3-way design).

    Identical decomposition to scripts/cluster_bootstrap_omega.py to keep
    headline reproducibility (omega^2 = 0.296 at evaluation level).
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


def fit_restricted_anova_yhat(df, dv="mcc"):
    """Compute yhat under the restricted ANOVA model that imposes the
    null on the scoring x pathogen interaction.

    Restricted model:
        y ~ scoring + family + pathogen
              + scoring:family + family:pathogen
        (no scoring:pathogen, no three-way)

    This is the wild-cluster bootstrap for testing / interval-estimating
    the scoring x pathogen interaction (Cameron, Gelbach & Miller 2008,
    Section 4.1, "wild cluster bootstrap-T" / "WCR" variant): residuals
    from the *restricted* model carry the scoring x pathogen signal that
    we are bootstrapping, and the cluster-level Rademacher sign flip
    propagates within-pathogen dependence into the bootstrap distribution.

    Implementation: closed-form additive (main + two two-way) fit. Let
        mu        = grand mean
        a_s       = scoring main effect
        b_f       = family main effect
        c_p       = pathogen main effect
        ab_{sf}   = scoring:family interaction (centred)
        bc_{fp}   = family:pathogen interaction (centred)
    The restricted yhat is mu + a + b + c + ab + bc, fit by means
    (balanced cell counts within each (s,f,p) so cell counts cancel in
    the centring step). For unbalanced cell counts the closed form is
    an approximation; we therefore center each effect via group means
    after subtracting lower-order effects, which matches the Type-I
    sequential decomposition used in the headline ANOVA.
    """
    y = df[dv].to_numpy()
    s = df["scoring"].to_numpy()
    f = df["family"].to_numpy()
    p = df["pathogen"].to_numpy()

    mu = y.mean()
    r = y - mu

    a_map = pd.Series(r).groupby(s).transform("mean").to_numpy()
    r1 = r - a_map

    b_map = pd.Series(r1).groupby(f).transform("mean").to_numpy()
    r2 = r1 - b_map

    c_map = pd.Series(r2).groupby(p).transform("mean").to_numpy()
    r3 = r2 - c_map

    ab_map = pd.Series(r3).groupby([s, f]).transform("mean").to_numpy()
    r4 = r3 - ab_map

    bc_map = pd.Series(r4).groupby([f, p]).transform("mean").to_numpy()
    r5 = r4 - bc_map

    yhat = mu + a_map + b_map + c_map + ab_map + bc_map
    e = y - yhat
    return yhat, e


def wild_cluster_bootstrap(df, n_boot=N_BOOT, seed=SEED):
    """Wild-cluster bootstrap omega^2(scoring x pathogen).

    Cluster unit: pathogen (G = 11). Rademacher weights w_g in {-1, +1}
    per cluster, applied to within-cell residuals from the full
    saturated three-way fit.
    """
    pathogens = sorted(df["pathogen"].unique())
    g = len(pathogens)
    pathogen_to_idx = {p: i for i, p in enumerate(pathogens)}
    cluster_idx = df["pathogen"].map(pathogen_to_idx).to_numpy()

    yhat, e = fit_restricted_anova_yhat(df)
    work = df.copy()

    rng = np.random.default_rng(seed)
    boot_omega = np.empty(n_boot, dtype=float)
    t0 = time.time()
    for b in range(n_boot):
        # Rademacher (+/-1) per cluster, broadcast to observations.
        w = rng.choice([-1.0, 1.0], size=g)
        y_star = yhat + w[cluster_idx] * e
        work["mcc_wild"] = y_star
        boot_omega[b] = omega2_interaction(work, dv="mcc_wild")
        if (b + 1) % 100 == 0:
            elapsed = time.time() - t0
            rate = (b + 1) / elapsed
            eta = (n_boot - b - 1) / rate
            print(f"  rep {b+1}/{n_boot} | rate {rate:.1f}/s | eta {eta:.0f}s")
    return boot_omega


def main():
    print("Wild-cluster bootstrap omega^2(scoring x pathogen)")
    print("=" * 72)
    if not INPUT.exists():
        sys.exit(f"missing input: {INPUT}")
    df = pd.read_csv(INPUT)
    df["pathogen"] = df["pathogen"].replace({"Influenza_B": "Influenza B"})
    print(f"Loaded {len(df)} rows; pathogens={df['pathogen'].nunique()}")

    headline = omega2_interaction(df)
    print(f"Headline omega^2(scoring x pathogen): {headline:.4f}")

    print(f"\nWild-cluster bootstrap (Cameron-Gelbach-Miller 2008):")
    print(f"  cluster unit  = pathogen (G = 11)")
    print(f"  weight type   = Rademacher (+/-1)")
    print(f"  residual base = restricted ANOVA (no scoring:pathogen)")
    print(f"  B = {N_BOOT}, seed = {SEED}")

    boot_wild = wild_cluster_bootstrap(df, n_boot=N_BOOT, seed=SEED)

    ci_lo = float(np.percentile(boot_wild, 2.5))
    ci_hi = float(np.percentile(boot_wild, 97.5))
    p_zero = float(np.mean(boot_wild <= 0.0))
    p_cohen = float(np.mean(boot_wild <= 0.14))
    print(f"\nWild-cluster results:")
    print(f"  mean omega^2     = {boot_wild.mean():.4f}")
    print(f"  median           = {np.median(boot_wild):.4f}")
    print(f"  95% percentile CI = [{ci_lo:.4f}, {ci_hi:.4f}]")
    print(f"  Pr(omega^2 <= 0)  = {p_zero:.4f}")
    print(f"  Pr(omega^2 <= 0.14, Cohen large) = {p_cohen:.4f}")

    # Standard cluster bootstrap (already archived) for side-by-side.
    std = pd.read_csv(RESULTS / "cluster_bootstrap_omega.csv")
    std_arr = std["omega2_scoring_x_pathogen"].to_numpy()
    std_lo = float(np.percentile(std_arr, 2.5))
    std_hi = float(np.percentile(std_arr, 97.5))
    print(f"\nStandard cluster bootstrap (archive, B = {len(std_arr)}):")
    print(f"  mean omega^2     = {std_arr.mean():.4f}")
    print(f"  95% percentile CI = [{std_lo:.4f}, {std_hi:.4f}]")
    print(f"  CI width: standard = {std_hi - std_lo:.4f}, "
          f"wild = {ci_hi - ci_lo:.4f}")

    out = RESULTS / "wild_cluster_bootstrap_omega.csv"
    pd.DataFrame({
        "iteration": np.arange(N_BOOT),
        "omega2_scoring_x_pathogen": boot_wild,
    }).to_csv(out, index=False)
    print(f"\nWrote {out}")

    summary = pd.DataFrame([
        {
            "bootstrap_method": "standard_cluster_percentile",
            "cluster_unit": "pathogen",
            "G_clusters": 11,
            "B_replicates": int(len(std_arr)),
            "omega2_point": round(headline, 4),
            "omega2_mean": round(float(std_arr.mean()), 4),
            "ci_lower_2p5": round(std_lo, 4),
            "ci_upper_97p5": round(std_hi, 4),
            "ci_width": round(std_hi - std_lo, 4),
            "p_omega2_le_0": round(float(np.mean(std_arr <= 0.0)), 4),
            "p_omega2_le_0p14_cohen": round(float(np.mean(std_arr <= 0.14)), 4),
            "body_target_ci": "[0.195, 0.333]",
            "source_csv": "results/mutbench/cluster_bootstrap_omega.csv",
        },
        {
            "bootstrap_method": "wild_cluster_rademacher",
            "cluster_unit": "pathogen",
            "G_clusters": 11,
            "B_replicates": N_BOOT,
            "omega2_point": round(headline, 4),
            "omega2_mean": round(float(boot_wild.mean()), 4),
            "ci_lower_2p5": round(ci_lo, 4),
            "ci_upper_97p5": round(ci_hi, 4),
            "ci_width": round(ci_hi - ci_lo, 4),
            "p_omega2_le_0": round(p_zero, 4),
            "p_omega2_le_0p14_cohen": round(p_cohen, 4),
            "body_target_ci": "(new; CGM 2008 sharper alternative)",
            "source_csv": "results/mutbench/wild_cluster_bootstrap_omega.csv",
        },
    ])
    out_sum = RESULTS / "wild_cluster_bootstrap_omega_summary.csv"
    summary.to_csv(out_sum, index=False)
    print(f"Wrote {out_sum}")
    print("\nSummary:")
    print(summary.to_string(index=False))


if __name__ == "__main__":
    main()
