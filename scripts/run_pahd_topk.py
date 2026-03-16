#!/usr/bin/env python3
"""
Compute top-k hit rate analysis for PAHD Family-first prototype results.

For each held-out pathogen, checks whether the PAHD-predicted combination
falls within the oracle's top-5 and top-10 combinations (ranked by MCC).
"""

import pandas as pd
import numpy as np
import os

RESULTS_DIR = "/proj/paper/results/mutbench"

def main():
    # Load PAHD results (Family-first only)
    pahd = pd.read_csv(os.path.join(RESULTS_DIR, "pahd_prototype_results.csv"))
    pahd_family = pahd[pahd["method"] == "PAHD-Family"].copy()

    # Load benchmark results
    bench = pd.read_csv(os.path.join(RESULTS_DIR, "extended_9pathogen_results.csv"))

    pathogens = pahd_family["held_out"].unique()
    results = []

    for pathogen in pathogens:
        row = pahd_family[pahd_family["held_out"] == pathogen].iloc[0]
        predicted_combo = row["predicted_combo"]
        test_mcc = row["test_mcc"]
        oracle_mcc = row["oracle_mcc"]

        # Get all combinations for this pathogen, ranked by MCC
        pathogen_results = bench[bench["pathogen"] == pathogen].copy()
        # Create combo string: score + detector
        pathogen_results["combo"] = pathogen_results["score"] + " + " + pathogen_results["detector"]
        pathogen_results = pathogen_results.sort_values("mcc", ascending=False).reset_index(drop=True)

        # Get top-k combos
        top5_combos = set(pathogen_results.head(5)["combo"].values)
        top10_combos = set(pathogen_results.head(10)["combo"].values)

        in_top5 = predicted_combo in top5_combos
        in_top10 = predicted_combo in top10_combos

        # Also find rank of predicted combo
        rank_match = pathogen_results[pathogen_results["combo"] == predicted_combo]
        rank = rank_match.index[0] + 1 if len(rank_match) > 0 else -1

        total_combos = len(pathogen_results)

        # Family-level analysis: check if predicted family matches oracle's top families
        predicted_family = row.get("predicted_family", "")
        if pd.isna(predicted_family) or predicted_family == "":
            # Extract family from detector part of predicted_combo
            det_part = predicted_combo.split(" + ", 1)[1] if " + " in predicted_combo else predicted_combo
            predicted_family = det_part.split("(")[0]

        # Get best family for this pathogen (family of oracle combo)
        oracle_combo_str = row["oracle_combo"]
        oracle_det = oracle_combo_str.split(" + ", 1)[1] if " + " in oracle_combo_str else oracle_combo_str
        oracle_family = oracle_det.split("(")[0]

        # Top families by best MCC within each family
        family_best = pathogen_results.groupby("family")["mcc"].max().sort_values(ascending=False)
        top3_families = list(family_best.head(3).index)
        top5_families = list(family_best.head(5).index)
        family_in_top3 = predicted_family in top3_families
        family_in_top5 = predicted_family in top5_families

        # Percentile of predicted rank
        percentile = (1 - rank / total_combos) * 100 if rank > 0 else 0

        results.append({
            "pathogen": pathogen,
            "predicted_combo": predicted_combo,
            "predicted_family": predicted_family,
            "oracle_family": oracle_family,
            "test_mcc": test_mcc,
            "oracle_mcc": oracle_mcc,
            "predicted_rank": rank,
            "total_combos": total_combos,
            "percentile": round(percentile, 1),
            "in_top5": in_top5,
            "in_top10": in_top10,
            "family_in_top3": family_in_top3,
            "family_in_top5": family_in_top5,
        })

        print(f"{pathogen}: predicted='{predicted_combo}' (fam={predicted_family}), "
              f"rank={rank}/{total_combos} (top {100-percentile:.0f}%), "
              f"test_mcc={test_mcc:.4f}, oracle_mcc={oracle_mcc:.4f}, "
              f"top5={'Y' if in_top5 else 'N'}, top10={'Y' if in_top10 else 'N'}, "
              f"fam_top3={'Y' if family_in_top3 else 'N'}, fam_top5={'Y' if family_in_top5 else 'N'}")

    df = pd.DataFrame(results)

    # Summary statistics
    top5_hits = df["in_top5"].sum()
    top10_hits = df["in_top10"].sum()
    n = len(df)
    mean_mcc = df["test_mcc"].mean()
    median_mcc = df["test_mcc"].median()

    # Naive baseline (from PAHD results)
    pahd_naive = pahd[pahd["method"] == "Naive"].copy()
    naive_mean = pahd_naive["test_mcc"].mean()
    naive_median = pahd_naive["test_mcc"].median()

    family_top3_hits = df["family_in_top3"].sum()
    family_top5_hits = df["family_in_top5"].sum()
    median_percentile = df["percentile"].median()

    print(f"\n=== PAHD Family-first Top-k Analysis ===")
    print(f"Top-5 hit rate:  {top5_hits}/{n}")
    print(f"Top-10 hit rate: {top10_hits}/{n}")
    print(f"Family top-3 hit rate: {family_top3_hits}/{n}")
    print(f"Family top-5 hit rate: {family_top5_hits}/{n}")
    print(f"Mean test MCC:   {mean_mcc:.4f}")
    print(f"Median test MCC: {median_mcc:.4f}")
    print(f"Naive mean MCC:  {naive_mean:.4f}")
    print(f"Naive median MCC:{naive_median:.4f}")
    print(f"Median rank:     {df['predicted_rank'].median():.0f}")
    print(f"Median percentile: {median_percentile:.1f}%")

    # Save
    summary_row = pd.DataFrame([{
        "metric": "top5_hits", "value": top5_hits,
    }, {
        "metric": "top10_hits", "value": top10_hits,
    }, {
        "metric": "n_pathogens", "value": n,
    }, {
        "metric": "mean_test_mcc", "value": round(mean_mcc, 4),
    }, {
        "metric": "median_test_mcc", "value": round(median_mcc, 4),
    }, {
        "metric": "naive_mean_mcc", "value": round(naive_mean, 4),
    }, {
        "metric": "naive_median_mcc", "value": round(naive_median, 4),
    }, {
        "metric": "family_top3_hits", "value": family_top3_hits,
    }, {
        "metric": "family_top5_hits", "value": family_top5_hits,
    }, {
        "metric": "median_percentile", "value": round(median_percentile, 1),
    }])

    out_path = os.path.join(RESULTS_DIR, "pahd_topk_results.csv")
    # Save both detail and summary
    df.to_csv(out_path, index=False)
    summary_path = os.path.join(RESULTS_DIR, "pahd_topk_summary.csv")
    summary_row.to_csv(summary_path, index=False)

    print(f"\nSaved details to {out_path}")
    print(f"Saved summary to {summary_path}")


if __name__ == "__main__":
    main()
