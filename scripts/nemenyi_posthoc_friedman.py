#!/usr/bin/env python3
"""
Nemenyi Post-Hoc Test for Friedman Rank-Block Result (Tier B4)
==============================================================
Reads:  results/mutbench/stage3_full_results.csv
Output:
  - results/mutbench/nemenyi_pairwise_pvalues.csv  (20x20 matrix; same combo
    set as the Friedman test in analyze_stage3_stats.py)
  - results/mutbench/nemenyi_summary.csv           (long-form pairwise list
    sorted by p-value; significant pairs flagged at alpha=0.05 raw and
    Bonferroni-adjusted)
  - results/mutbench/nemenyi_provenance.json      (data-shape provenance,
    Friedman echo, top/bottom-p pair list, environment)

The Friedman omnibus test (chi^2=7.69, p=0.990 for the top-20 scoring x
detection family combinations across 11 pathogens; ch4 §9pathogen_friedman)
is omnibus: it cannot reject the null that all 20 combinations share an
identical cross-pathogen ranking. The Nemenyi post-hoc test extends the
Friedman framework to all 20*19/2 = 190 pairwise comparisons, so we can
report (a) whether any pairs cross alpha and (b) the most-different and
least-different pairs even when the omnibus does not reject. The post-hoc
result is presented as a complement to, not a replacement for, the omnibus
acknowledgment.
"""
import json
import os
import sys
from datetime import datetime, timezone

import numpy as np
import pandas as pd

ROOT = "/proj/paper"
RESULTS = os.path.join(ROOT, "results", "mutbench")

INPUT = os.path.join(RESULTS, "stage3_full_results.csv")
OUT_MATRIX = os.path.join(RESULTS, "nemenyi_pairwise_pvalues.csv")
OUT_SUMMARY = os.path.join(RESULTS, "nemenyi_summary.csv")
OUT_PROV = os.path.join(RESULTS, "nemenyi_provenance.json")


def main() -> int:
    df = pd.read_csv(INPUT)
    pathogens = sorted(df["pathogen"].unique())

    # Mirror analyze_stage3_stats.py construction of the top-20 combo block.
    combo_pathogen = (
        df.groupby(["scoring", "family", "pathogen"])["mcc"].mean().reset_index()
    )
    combo_mean = (
        combo_pathogen.groupby(["scoring", "family"])["mcc"].mean().reset_index()
    )
    # Match analyze_stage3_stats.py:175 — sort combos by mean MCC
    # (descending) and take the top 20, so we land on the identical
    # 20-combo set the published Friedman chi^2=7.69 / p=0.990 was
    # computed on.
    combo_mean = combo_mean.sort_values("mcc", ascending=False)
    top20 = combo_mean.head(20)[["scoring", "family"]].values.tolist()

    rows, labels = [], []
    for s, f in top20:
        row = []
        for p in pathogens:
            val = combo_pathogen.loc[
                (combo_pathogen["scoring"] == s)
                & (combo_pathogen["family"] == f)
                & (combo_pathogen["pathogen"] == p),
                "mcc",
            ]
            row.append(val.values[0] if len(val) > 0 else np.nan)
        rows.append(row)
        labels.append(f"{s}+{f}")

    matrix = np.array(rows)
    valid_mask = ~np.isnan(matrix).any(axis=1)
    matrix_clean = matrix[valid_mask]
    labels_clean = [c for c, v in zip(labels, valid_mask) if v]
    n_combos = matrix_clean.shape[0]
    n_pathogens = matrix_clean.shape[1]
    print(f"  Matrix: {n_combos} combos x {n_pathogens} pathogens")

    # Friedman echo (sanity-check it matches the published 7.69 / 0.990).
    from scipy.stats import friedmanchisquare, rankdata

    args = [matrix_clean[i, :] for i in range(n_combos)]
    chi2, p_friedman = friedmanchisquare(*args)
    print(f"  Friedman chi2 = {chi2:.4f}, p = {p_friedman:.6f} (echo)")

    # Nemenyi expects a (blocks x treatments) array, i.e. (pathogens x combos),
    # one row per block and one column per treatment.
    import scikit_posthocs as sp

    block_x_treatment = matrix_clean.T  # 11 pathogens x 20 combos
    nemenyi_df = sp.posthoc_nemenyi_friedman(block_x_treatment)
    nemenyi_df.index = labels_clean
    nemenyi_df.columns = labels_clean
    nemenyi_df.to_csv(OUT_MATRIX)
    print(f"  Wrote {OUT_MATRIX} ({nemenyi_df.shape[0]}x{nemenyi_df.shape[1]})")

    # Long-form pair table.
    n_pairs = n_combos * (n_combos - 1) // 2
    bonf_alpha = 0.05 / n_pairs
    rank_means = rankdata(-matrix_clean, axis=0).mean(axis=1)
    rank_lookup = {labels_clean[i]: float(rank_means[i]) for i in range(n_combos)}

    pair_rows = []
    for i in range(n_combos):
        for j in range(i + 1, n_combos):
            a, b = labels_clean[i], labels_clean[j]
            p = float(nemenyi_df.iat[i, j])
            pair_rows.append(
                {
                    "combo_a": a,
                    "combo_b": b,
                    "mean_rank_a": rank_lookup[a],
                    "mean_rank_b": rank_lookup[b],
                    "rank_diff_abs": abs(rank_lookup[a] - rank_lookup[b]),
                    "p_value": p,
                    "sig_raw_0p05": p < 0.05,
                    "sig_bonferroni_0p05": p < bonf_alpha,
                }
            )
    pairs_df = pd.DataFrame(pair_rows).sort_values("p_value").reset_index(drop=True)
    pairs_df.to_csv(OUT_SUMMARY, index=False)
    print(f"  Wrote {OUT_SUMMARY} ({len(pairs_df)} pairs)")

    n_sig_raw = int(pairs_df["sig_raw_0p05"].sum())
    n_sig_bonf = int(pairs_df["sig_bonferroni_0p05"].sum())
    print(f"  Pairs sig at raw alpha=0.05: {n_sig_raw}/{n_pairs}")
    print(
        f"  Pairs sig at Bonferroni alpha=0.05/{n_pairs}={bonf_alpha:.2e}: "
        f"{n_sig_bonf}/{n_pairs}"
    )

    most_diff = pairs_df.iloc[0].to_dict()
    most_sim = pairs_df.iloc[-1].to_dict()
    print(
        f"  Most differentiated pair: {most_diff['combo_a']} vs "
        f"{most_diff['combo_b']}, p = {most_diff['p_value']:.4f}"
    )
    print(
        f"  Most similar pair:        {most_sim['combo_a']} vs "
        f"{most_sim['combo_b']}, p = {most_sim['p_value']:.4f}"
    )

    prov = {
        "generated_utc": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "input": INPUT,
        "matrix_shape": [int(n_combos), int(n_pathogens)],
        "pathogens": pathogens,
        "combos": labels_clean,
        "friedman_chi2": float(chi2),
        "friedman_p_value": float(p_friedman),
        "n_pairs": int(n_pairs),
        "bonferroni_alpha": float(bonf_alpha),
        "n_sig_raw_0p05": n_sig_raw,
        "n_sig_bonferroni_0p05": n_sig_bonf,
        "most_differentiated": {
            "combo_a": most_diff["combo_a"],
            "combo_b": most_diff["combo_b"],
            "p_value": float(most_diff["p_value"]),
            "rank_diff_abs": float(most_diff["rank_diff_abs"]),
        },
        "most_similar": {
            "combo_a": most_sim["combo_a"],
            "combo_b": most_sim["combo_b"],
            "p_value": float(most_sim["p_value"]),
            "rank_diff_abs": float(most_sim["rank_diff_abs"]),
        },
        "top10_lowest_p_pairs": pairs_df.head(10).to_dict(orient="records"),
        "top10_highest_p_pairs": pairs_df.tail(10)
        .sort_values("p_value", ascending=False)
        .to_dict(orient="records"),
        "scikit_posthocs_version": sp.__version__,
        "numpy_version": np.__version__,
        "pandas_version": pd.__version__,
        "python_version": sys.version,
    }
    with open(OUT_PROV, "w") as fh:
        json.dump(prov, fh, indent=2)
    print(f"  Wrote {OUT_PROV}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
