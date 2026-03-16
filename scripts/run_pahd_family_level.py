#!/usr/bin/env python3
"""
PAHD Family-Level and Scoring-Level Prediction Evaluation.

Instead of predicting from 351 exact combinations (9 scoring × 39 detectors),
predict at coarser granularities:
  - Detection family level (~15 families)
  - Scoring formula level (9 formulas)

Uses 1-NN similarity-based LOPO (Leave-One-Pathogen-Out) prediction.
"""

import pandas as pd
import numpy as np
from pathlib import Path

RESULTS_DIR = Path("/proj/paper/results/mutbench")


def load_data():
    """Load benchmark results, profiles, and similarity matrix."""
    df = pd.read_csv(RESULTS_DIR / "multilayer_9pathogen_results.csv")
    sim = pd.read_csv(RESULTS_DIR / "pahd_pathogen_similarity.csv", index_col=0)
    return df, sim


def compute_oracle(df, metric="composite_score"):
    """For each pathogen, find oracle best combo, family, and scoring."""
    pathogens = sorted(df["pathogen"].unique())

    oracle = {}
    for p in pathogens:
        pdf = df[df["pathogen"] == p]
        best_idx = pdf[metric].idxmax()
        best_row = pdf.loc[best_idx]

        # Oracle exact combo
        oracle[p] = {
            "best_combo": (best_row["score"], best_row["detector"]),
            "best_family": best_row["family"],
            "best_scoring": best_row["score"],
            "oracle_mcc": best_row[metric],
        }

        # Best family: which family achieves highest max MCC?
        family_best = pdf.groupby("family")[metric].max()
        oracle[p]["best_family"] = family_best.idxmax()
        oracle[p]["best_family_mcc"] = family_best.max()

        # Best scoring: which scoring achieves highest max MCC?
        scoring_best = pdf.groupby("score")[metric].max()
        oracle[p]["best_scoring"] = scoring_best.idxmax()
        oracle[p]["best_scoring_mcc"] = scoring_best.max()

    return oracle


def lopo_family_prediction(df, sim, oracle, metric="composite_score"):
    """LOPO prediction at detection family level."""
    pathogens = sorted(df["pathogen"].unique())
    results = []

    for held_out in pathogens:
        # Find most similar training pathogen
        training = [p for p in pathogens if p != held_out]
        similarities = sim.loc[held_out, training]
        most_similar = similarities.idxmax()
        sim_value = similarities.max()

        # Predict: held-out's best family = most similar's best family
        predicted_family = oracle[most_similar]["best_family"]
        actual_family = oracle[held_out]["best_family"]
        match = predicted_family == actual_family

        # MCC achieved: best combo WITHIN predicted family for held-out
        held_out_df = df[df["pathogen"] == held_out]
        predicted_family_df = held_out_df[held_out_df["family"] == predicted_family]
        achieved_mcc = predicted_family_df[metric].max() if len(predicted_family_df) > 0 else 0.0

        results.append({
            "pathogen": held_out,
            "most_similar": most_similar,
            "similarity": sim_value,
            "predicted_family": predicted_family,
            "actual_family": actual_family,
            "family_match": match,
            "achieved_mcc": achieved_mcc,
            "oracle_mcc": oracle[held_out]["oracle_mcc"],
            "pct_of_oracle": (achieved_mcc / oracle[held_out]["oracle_mcc"] * 100)
                if oracle[held_out]["oracle_mcc"] > 0 else 0.0,
        })

    return pd.DataFrame(results)


def lopo_scoring_prediction(df, sim, oracle, metric="composite_score"):
    """LOPO prediction at scoring formula level."""
    pathogens = sorted(df["pathogen"].unique())
    results = []

    for held_out in pathogens:
        training = [p for p in pathogens if p != held_out]
        similarities = sim.loc[held_out, training]
        most_similar = similarities.idxmax()
        sim_value = similarities.max()

        predicted_scoring = oracle[most_similar]["best_scoring"]
        actual_scoring = oracle[held_out]["best_scoring"]
        match = predicted_scoring == actual_scoring

        held_out_df = df[df["pathogen"] == held_out]
        predicted_scoring_df = held_out_df[held_out_df["score"] == predicted_scoring]
        achieved_mcc = predicted_scoring_df[metric].max() if len(predicted_scoring_df) > 0 else 0.0

        results.append({
            "pathogen": held_out,
            "most_similar": most_similar,
            "similarity": sim_value,
            "predicted_scoring": predicted_scoring,
            "actual_scoring": actual_scoring,
            "scoring_match": match,
            "achieved_mcc": achieved_mcc,
            "oracle_mcc": oracle[held_out]["oracle_mcc"],
            "pct_of_oracle": (achieved_mcc / oracle[held_out]["oracle_mcc"] * 100)
                if oracle[held_out]["oracle_mcc"] > 0 else 0.0,
        })

    return pd.DataFrame(results)


def compute_naive_global_best(df, metric="composite_score"):
    """Naive baseline: use global best combo for all pathogens."""
    pathogens = sorted(df["pathogen"].unique())

    # Global best combo across all pathogens (average MCC)
    combo_avg = df.groupby(["score", "detector", "family"])[metric].mean()
    best_combo_idx = combo_avg.idxmax()
    best_score, best_detector, best_family = best_combo_idx

    results = []
    for p in pathogens:
        pdf = df[(df["pathogen"] == p) & (df["score"] == best_score) & (df["detector"] == best_detector)]
        achieved_mcc = pdf[metric].values[0] if len(pdf) > 0 else 0.0
        oracle_mcc = df[df["pathogen"] == p][metric].max()
        results.append({
            "pathogen": p,
            "achieved_mcc": achieved_mcc,
            "oracle_mcc": oracle_mcc,
        })

    return pd.DataFrame(results)


def main():
    df, sim = load_data()
    oracle = compute_oracle(df)

    print("=" * 80)
    print("PAHD FAMILY-LEVEL AND SCORING-LEVEL PREDICTION EVALUATION")
    print("=" * 80)

    # --- Oracle info ---
    print("\n--- Oracle Best Family and Scoring per Pathogen ---")
    for p in sorted(oracle.keys()):
        o = oracle[p]
        print(f"  {p:15s}  Family: {o['best_family']:15s}  Scoring: {o['best_scoring']:12s}  "
              f"Oracle MCC: {o['oracle_mcc']:.4f}")

    # --- Family-level LOPO ---
    family_results = lopo_family_prediction(df, sim, oracle)
    print("\n--- Family-Level LOPO Prediction ---")
    for _, row in family_results.iterrows():
        match_str = "MATCH" if row["family_match"] else "MISS"
        print(f"  {row['pathogen']:15s}  1-NN: {row['most_similar']:15s}  "
              f"Pred: {row['predicted_family']:15s}  Actual: {row['actual_family']:15s}  "
              f"[{match_str}]  MCC: {row['achieved_mcc']:.4f}  "
              f"({row['pct_of_oracle']:.1f}% of oracle)")

    family_match_rate = family_results["family_match"].sum()
    family_mean_mcc = family_results["achieved_mcc"].mean()
    family_median_mcc = family_results["achieved_mcc"].median()
    family_mean_pct = family_results["pct_of_oracle"].mean()

    print(f"\n  Family match rate: {family_match_rate}/9")
    print(f"  Mean MCC: {family_mean_mcc:.4f}")
    print(f"  Median MCC: {family_median_mcc:.4f}")
    print(f"  Mean % of oracle: {family_mean_pct:.1f}%")

    # --- Scoring-level LOPO ---
    scoring_results = lopo_scoring_prediction(df, sim, oracle)
    print("\n--- Scoring-Level LOPO Prediction ---")
    for _, row in scoring_results.iterrows():
        match_str = "MATCH" if row["scoring_match"] else "MISS"
        print(f"  {row['pathogen']:15s}  1-NN: {row['most_similar']:15s}  "
              f"Pred: {row['predicted_scoring']:12s}  Actual: {row['actual_scoring']:12s}  "
              f"[{match_str}]  MCC: {row['achieved_mcc']:.4f}  "
              f"({row['pct_of_oracle']:.1f}% of oracle)")

    scoring_match_rate = scoring_results["scoring_match"].sum()
    scoring_mean_mcc = scoring_results["achieved_mcc"].mean()
    scoring_median_mcc = scoring_results["achieved_mcc"].median()
    scoring_mean_pct = scoring_results["pct_of_oracle"].mean()

    print(f"\n  Scoring match rate: {scoring_match_rate}/9")
    print(f"  Mean MCC: {scoring_mean_mcc:.4f}")
    print(f"  Median MCC: {scoring_median_mcc:.4f}")
    print(f"  Mean % of oracle: {scoring_mean_pct:.1f}%")

    # --- Naive global best ---
    naive_results = compute_naive_global_best(df)
    naive_mean_mcc = naive_results["achieved_mcc"].mean()
    naive_median_mcc = naive_results["achieved_mcc"].median()
    naive_mean_pct = (naive_results["achieved_mcc"] / naive_results["oracle_mcc"] * 100).mean()

    # --- Existing PAHD combo-level results ---
    pahd_combo = pd.read_csv(RESULTS_DIR / "pahd_comparison_table.csv")
    pahd_1nn_mean = pahd_combo["PAHD 1-NN"].mean()
    pahd_1nn_median = pahd_combo["PAHD 1-NN"].median()
    oracle_mean = pahd_combo["Oracle"].mean()
    oracle_median = pahd_combo["Oracle"].median()
    pahd_1nn_pct = (pahd_combo["PAHD 1-NN"] / pahd_combo["Oracle"] * 100).mean()
    naive_lopo_mean = pahd_combo["Naive LOPO"].mean()
    naive_lopo_median = pahd_combo["Naive LOPO"].median()
    naive_lopo_pct = (pahd_combo["Naive LOPO"] / pahd_combo["Oracle"] * 100).mean()

    # --- Comparison table ---
    print("\n" + "=" * 80)
    print("COMPARISON TABLE")
    print("=" * 80)
    print(f"{'Level':<35} {'Match':>5} {'Mean MCC':>10} {'Median MCC':>12} {'vs Oracle':>10}")
    print("-" * 72)
    print(f"{'Oracle (exact combo)':<35} {'9/9':>5} {oracle_mean:>10.4f} {oracle_median:>12.4f} {'100.0%':>10}")
    print(f"{'PAHD Family (1-NN)':<35} {f'{family_match_rate}/9':>5} {family_mean_mcc:>10.4f} {family_median_mcc:>12.4f} {f'{family_mean_pct:.1f}%':>10}")
    print(f"{'PAHD Scoring (1-NN)':<35} {f'{scoring_match_rate}/9':>5} {scoring_mean_mcc:>10.4f} {scoring_median_mcc:>12.4f} {f'{scoring_mean_pct:.1f}%':>10}")
    print(f"{'PAHD Combo (1-NN, v2)':<35} {'0/9':>5} {pahd_1nn_mean:>10.4f} {pahd_1nn_median:>12.4f} {f'{pahd_1nn_pct:.1f}%':>10}")
    print(f"{'Naive (global best combo)':<35} {'-':>5} {naive_mean_mcc:>10.4f} {naive_median_mcc:>12.4f} {f'{naive_mean_pct:.1f}%':>10}")
    print(f"{'Naive LOPO (from pahd_comparison)':<35} {'-':>5} {naive_lopo_mean:>10.4f} {naive_lopo_median:>12.4f} {f'{naive_lopo_pct:.1f}%':>10}")

    # --- Save results ---
    # Detailed family results
    family_results.to_csv(RESULTS_DIR / "pahd_family_level_results.csv", index=False)
    scoring_results.to_csv(RESULTS_DIR / "pahd_scoring_level_results.csv", index=False)

    # Summary comparison table
    summary = pd.DataFrame([
        {"Level": "Oracle (exact combo)", "Match_Rate": "9/9",
         "Mean_MCC": round(oracle_mean, 4), "Median_MCC": round(oracle_median, 4),
         "vs_Oracle_pct": 100.0},
        {"Level": "PAHD Detection Family (1-NN)", "Match_Rate": f"{family_match_rate}/9",
         "Mean_MCC": round(family_mean_mcc, 4), "Median_MCC": round(family_median_mcc, 4),
         "vs_Oracle_pct": round(family_mean_pct, 1)},
        {"Level": "PAHD Scoring Formula (1-NN)", "Match_Rate": f"{scoring_match_rate}/9",
         "Mean_MCC": round(scoring_mean_mcc, 4), "Median_MCC": round(scoring_median_mcc, 4),
         "vs_Oracle_pct": round(scoring_mean_pct, 1)},
        {"Level": "PAHD Exact Combo (1-NN, v2)", "Match_Rate": "0/9",
         "Mean_MCC": round(pahd_1nn_mean, 4), "Median_MCC": round(pahd_1nn_median, 4),
         "vs_Oracle_pct": round(pahd_1nn_pct, 1)},
        {"Level": "Naive (global best)", "Match_Rate": "-",
         "Mean_MCC": round(naive_mean_mcc, 4), "Median_MCC": round(naive_median_mcc, 4),
         "vs_Oracle_pct": round(naive_mean_pct, 1)},
    ])
    summary.to_csv(RESULTS_DIR / "pahd_family_level_comparison.csv", index=False)

    print(f"\nSaved: {RESULTS_DIR / 'pahd_family_level_results.csv'}")
    print(f"Saved: {RESULTS_DIR / 'pahd_scoring_level_results.csv'}")
    print(f"Saved: {RESULTS_DIR / 'pahd_family_level_comparison.csv'}")


if __name__ == "__main__":
    main()
