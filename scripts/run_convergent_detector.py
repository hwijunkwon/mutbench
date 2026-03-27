#!/usr/bin/env python3
"""Simplified convergent evolution detector using homoplasy scores.

Homoplasy counts from Fitch parsimony represent the number of independent
mutation origins per position on a phylogenetic tree. Positions with high
homoplasy are candidates for convergent evolution.

This script thresholds homoplasy scores at various cutoffs and evaluates
detection performance against Layer A (adaptive/positive selection) ground truth.
"""

import sys
sys.path.insert(0, "/proj/paper")

import numpy as np
import pandas as pd
from pathlib import Path
from sklearn.metrics import matthews_corrcoef, precision_score, recall_score, f1_score

from tools.mutbench.ground_truth.multilayer_gt import get_gt_adaptive

HOMOPLASY_DIR = Path("/proj/paper/results/mutbench/homoplasy_scores")
OUTPUT_PATH = Path("/proj/paper/results/mutbench/convergent_detector_results.csv")

PATHOGENS = [
    "SARS-CoV-2", "H3N2", "Norovirus", "HIV-1", "Dengue", "RSV",
    "Influenza_B", "MERS", "HCV", "Zika", "Rabies", "EV-A71",
]

THRESHOLDS = {
    "top5pct": lambda scores: np.percentile(scores, 95),
    "top10pct": lambda scores: np.percentile(scores, 90),
    "top20pct": lambda scores: np.percentile(scores, 80),
    "mean+1sd": lambda scores: np.mean(scores) + np.std(scores),
}


def evaluate(pred_set: set, gt_positive: set, n_total: int) -> dict:
    """Compute MCC, precision, recall, F1 for binary classification."""
    y_true = np.array([1 if i in gt_positive else 0 for i in range(n_total)])
    y_pred = np.array([1 if i in pred_set else 0 for i in range(n_total)])

    n_pred = int(y_pred.sum())
    n_gt = int(y_true.sum())
    tp = int((y_true & y_pred).sum())

    if n_pred == 0 or n_gt == 0:
        return {"mcc": 0.0, "precision": 0.0, "recall": 0.0, "f1": 0.0,
                "tp": tp, "n_pred": n_pred, "n_gt": n_gt}

    mcc = matthews_corrcoef(y_true, y_pred)
    prec = precision_score(y_true, y_pred, zero_division=0)
    rec = recall_score(y_true, y_pred, zero_division=0)
    f1 = f1_score(y_true, y_pred, zero_division=0)

    return {"mcc": mcc, "precision": prec, "recall": rec, "f1": f1,
            "tp": tp, "n_pred": n_pred, "n_gt": n_gt}


def main():
    results = []

    for pathogen in PATHOGENS:
        fpath = HOMOPLASY_DIR / f"{pathogen}_homoplasy.csv"
        if not fpath.exists():
            print(f"  SKIP {pathogen}: no homoplasy file")
            continue

        df = pd.read_csv(fpath)
        n_positions = len(df)
        raw_counts = df["raw_count"].values

        # Get Layer A ground truth
        gt_adaptive = get_gt_adaptive(pathogen, n_positions)
        if not gt_adaptive:
            print(f"  SKIP {pathogen}: no Layer A ground truth")
            continue

        print(f"\n{pathogen}: {n_positions} positions, "
              f"{len(gt_adaptive)} Layer A positives, "
              f"homoplasy range [{raw_counts.min()}-{raw_counts.max()}], "
              f"mean={raw_counts.mean():.2f}, nonzero={np.count_nonzero(raw_counts)}")

        for thresh_name, thresh_fn in THRESHOLDS.items():
            # Only threshold on nonzero scores for percentile-based methods
            # But apply to all positions
            cutoff = thresh_fn(raw_counts)

            # Positions exceeding threshold = convergent candidates
            pred_positions = set(df.loc[raw_counts > cutoff, "position"].values)

            metrics = evaluate(pred_positions, gt_adaptive, n_positions)

            row = {
                "pathogen": pathogen,
                "threshold_method": thresh_name,
                "cutoff_value": round(cutoff, 4),
                "n_positions": n_positions,
                "n_gt_positive": len(gt_adaptive),
                "n_predicted": metrics["n_pred"],
                "tp": metrics["tp"],
                "mcc": round(metrics["mcc"], 4),
                "precision": round(metrics["precision"], 4),
                "recall": round(metrics["recall"], 4),
                "f1": round(metrics["f1"], 4),
            }
            results.append(row)
            print(f"  {thresh_name}: cutoff={cutoff:.2f}, "
                  f"pred={metrics['n_pred']}, tp={metrics['tp']}, "
                  f"MCC={metrics['mcc']:.4f}, F1={metrics['f1']:.4f}")

    # Save results
    results_df = pd.DataFrame(results)
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    results_df.to_csv(OUTPUT_PATH, index=False)
    print(f"\nResults saved to {OUTPUT_PATH}")

    # Summary: best threshold per pathogen
    print("\n" + "=" * 80)
    print("BEST THRESHOLD PER PATHOGEN (by MCC)")
    print("=" * 80)
    for pathogen in PATHOGENS:
        sub = results_df[results_df["pathogen"] == pathogen]
        if sub.empty:
            continue
        best = sub.loc[sub["mcc"].idxmax()]
        print(f"  {pathogen:15s}: {best['threshold_method']:10s} "
              f"MCC={best['mcc']:.4f}  F1={best['f1']:.4f}  "
              f"P={best['precision']:.4f}  R={best['recall']:.4f}  "
              f"(pred={int(best['n_predicted'])}, tp={int(best['tp'])})")

    # Overall average MCC across pathogens (best per pathogen)
    best_per_pathogen = results_df.loc[results_df.groupby("pathogen")["mcc"].idxmax()]
    avg_mcc = best_per_pathogen["mcc"].mean()
    avg_f1 = best_per_pathogen["f1"].mean()
    print(f"\n  Average best MCC: {avg_mcc:.4f}")
    print(f"  Average best F1:  {avg_f1:.4f}")

    # Which threshold wins most often?
    print("\n  Threshold win counts:")
    wins = best_per_pathogen["threshold_method"].value_counts()
    for t, c in wins.items():
        print(f"    {t}: {c}")


if __name__ == "__main__":
    main()
