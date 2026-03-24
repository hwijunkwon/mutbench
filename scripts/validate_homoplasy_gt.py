#!/usr/bin/env python3
"""Validate homoplasy scores against Layer A ground truth for HIV-1, HCV, H3N2.

For each pathogen:
1. Load homoplasy scores
2. Load Layer A ground truth positions
3. Compare mean homoplasy at Layer A vs non-Layer A
4. Mann-Whitney U test
5. ROC analysis (AUC)
"""

import sys
from pathlib import Path
import numpy as np
import pandas as pd
from scipy.stats import mannwhitneyu
from sklearn.metrics import roc_auc_score, roc_curve

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from tools.mutbench.ground_truth.multilayer_gt import get_gt_adaptive, get_gt_constrained

HOMOPLASY_DIR = PROJECT_ROOT / "results" / "mutbench" / "homoplasy_scores"

PATHOGENS = ["HIV-1", "HCV", "H3N2"]


def analyze_pathogen(pathogen):
    """Run full validation for one pathogen."""
    print(f"\n{'='*60}")
    print(f"  {pathogen} — Homoplasy vs Layer A Ground Truth")
    print(f"{'='*60}")

    # Load homoplasy scores
    hom_path = HOMOPLASY_DIR / f"{pathogen}_homoplasy.csv"
    if not hom_path.exists():
        print(f"  ERROR: {hom_path} not found")
        return None

    df = pd.read_csv(hom_path)
    max_pos = len(df)
    scores = df["normalized_score"].values
    print(f"  Loaded {max_pos} positions from {hom_path.name}")

    # Get Layer A (adaptive) ground truth
    layer_a = get_gt_adaptive(pathogen, max_pos)
    layer_b = get_gt_constrained(pathogen, max_pos)
    print(f"  Layer A (adaptive) positions: {len(layer_a)}")
    print(f"  Layer B (constrained) positions: {len(layer_b)}")
    print(f"  Layer A positions: {sorted(layer_a)[:20]}{'...' if len(layer_a) > 20 else ''}")

    # Create binary labels
    all_positions = set(range(max_pos))
    non_layer_a = all_positions - layer_a

    # Get scores for each group
    scores_a = [scores[p] for p in layer_a if p < max_pos]
    scores_non_a = [scores[p] for p in non_layer_a if p < max_pos]

    mean_a = np.mean(scores_a)
    mean_non_a = np.mean(scores_non_a)
    median_a = np.median(scores_a)
    median_non_a = np.median(scores_non_a)

    print(f"\n  --- Descriptive Statistics ---")
    print(f"  Layer A:     mean={mean_a:.4f}, median={median_a:.4f}, n={len(scores_a)}")
    print(f"  Non-Layer A: mean={mean_non_a:.4f}, median={median_non_a:.4f}, n={len(scores_non_a)}")
    print(f"  Mean difference: {mean_a - mean_non_a:+.4f}")
    print(f"  Fold enrichment: {mean_a / (mean_non_a + 1e-10):.2f}x")

    # Also check Layer B (should be LOW homoplasy)
    if layer_b:
        scores_b = [scores[p] for p in layer_b if p < max_pos]
        mean_b = np.mean(scores_b)
        print(f"  Layer B (constrained): mean={mean_b:.4f}, n={len(scores_b)}")
        print(f"  Layer A vs B difference: {mean_a - mean_b:+.4f}")

    # Mann-Whitney U test
    print(f"\n  --- Mann-Whitney U Test ---")
    stat, pval = mannwhitneyu(scores_a, scores_non_a, alternative="greater")
    print(f"  U statistic: {stat:.1f}")
    print(f"  p-value (one-sided, A > non-A): {pval:.6f}")
    print(f"  Significant at alpha=0.05: {'YES' if pval < 0.05 else 'NO'}")
    print(f"  Significant at alpha=0.01: {'YES' if pval < 0.01 else 'NO'}")

    # ROC analysis
    print(f"\n  --- ROC Analysis ---")
    y_true = np.zeros(max_pos, dtype=int)
    for p in layer_a:
        if p < max_pos:
            y_true[p] = 1

    auc = roc_auc_score(y_true, scores)
    print(f"  AUC: {auc:.4f}")
    print(f"  Interpretation: {'Good' if auc > 0.7 else 'Moderate' if auc > 0.6 else 'Poor'} discrimination")

    # Find best threshold
    fpr, tpr, thresholds = roc_curve(y_true, scores)
    # Youden's J
    j_scores = tpr - fpr
    best_idx = np.argmax(j_scores)
    best_thresh = thresholds[best_idx]
    best_tpr = tpr[best_idx]
    best_fpr = fpr[best_idx]
    print(f"  Best threshold (Youden's J): {best_thresh:.4f}")
    print(f"  At best threshold: TPR={best_tpr:.3f}, FPR={best_fpr:.3f}")

    # Top-k analysis
    print(f"\n  --- Top-K Enrichment ---")
    for k_pct in [5, 10, 20]:
        k = max(1, int(max_pos * k_pct / 100))
        top_k_positions = set(np.argsort(scores)[-k:])
        hits = len(top_k_positions & layer_a)
        expected = len(layer_a) * k / max_pos
        enrichment = hits / (expected + 1e-10)
        print(f"  Top {k_pct}% ({k} positions): {hits}/{len(layer_a)} Layer A hits, "
              f"enrichment={enrichment:.2f}x (expected {expected:.1f})")

    # Effect size (Cohen's d)
    pooled_std = np.sqrt(
        ((len(scores_a) - 1) * np.std(scores_a, ddof=1)**2 +
         (len(scores_non_a) - 1) * np.std(scores_non_a, ddof=1)**2) /
        (len(scores_a) + len(scores_non_a) - 2)
    )
    cohens_d = (mean_a - mean_non_a) / (pooled_std + 1e-10)
    print(f"\n  Cohen's d: {cohens_d:.4f}")
    print(f"  Effect size: {'Large' if abs(cohens_d) > 0.8 else 'Medium' if abs(cohens_d) > 0.5 else 'Small' if abs(cohens_d) > 0.2 else 'Negligible'}")

    return {
        "pathogen": pathogen,
        "n_layer_a": len(layer_a),
        "n_total": max_pos,
        "mean_layer_a": mean_a,
        "mean_non_a": mean_non_a,
        "mean_diff": mean_a - mean_non_a,
        "fold_enrichment": mean_a / (mean_non_a + 1e-10),
        "mann_whitney_U": stat,
        "p_value": pval,
        "auc": auc,
        "cohens_d": cohens_d,
        "best_threshold": best_thresh,
        "best_tpr": best_tpr,
        "best_fpr": best_fpr,
    }


def main():
    print("=" * 60)
    print("  Homoplasy Score Validation Against Layer A Ground Truth")
    print("=" * 60)

    results = []
    for pathogen in PATHOGENS:
        r = analyze_pathogen(pathogen)
        if r:
            results.append(r)

    # Summary table
    print("\n\n" + "=" * 70)
    print("  SUMMARY TABLE")
    print("=" * 70)
    print(f"{'Pathogen':<12} {'N_A':<6} {'Mean_A':<10} {'Mean_nonA':<10} "
          f"{'p-value':<12} {'AUC':<8} {'Cohen_d':<10}")
    print("-" * 70)
    for r in results:
        print(f"{r['pathogen']:<12} {r['n_layer_a']:<6} {r['mean_layer_a']:<10.4f} "
              f"{r['mean_non_a']:<10.4f} {r['p_value']:<12.6f} "
              f"{r['auc']:<8.4f} {r['cohens_d']:<10.4f}")

    # Save results
    out_path = HOMOPLASY_DIR / "homoplasy_gt_validation.csv"
    pd.DataFrame(results).to_csv(out_path, index=False)
    print(f"\nResults saved to {out_path}")
    print("\nDone!")


if __name__ == "__main__":
    main()
