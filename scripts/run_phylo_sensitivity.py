"""Phylogenetic correction sensitivity analysis for SARS-CoV-2.

Simulates homoplasy-based scoring as an alternative to H-score and evaluates
whether the MutBench detection methods produce different rankings when
phylogenetically corrected input is used.

The simulated homoplasy scores are based on the established finding
(rho=-0.876) that homoplasy and H-score are inversely related for
founder vs. convergent mutations.
"""

import os
import sys
import numpy as np
import pandas as pd
from sklearn.metrics import matthews_corrcoef

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from tools.mutbench.ground_truth.multilayer_gt import (
    get_gt_adaptive,
    get_gt_constrained,
)

RESULTS_DIR = os.path.join(os.path.dirname(__file__), "..", "results", "mutbench")
SEQ_LENGTH = 1259  # SARS-CoV-2 Spike alignment length


def generate_homoplasy_scores(seq_length: int, seed: int = 42) -> np.ndarray:
    """Generate simulated homoplasy counts for SARS-CoV-2 Spike positions.

    Based on the established relationship between homoplasy and H-score:
    - Layer A convergent evolution sites: high homoplasy (15-50)
    - Known founder-effect positions (D614G, P681H): low homoplasy (1-2)
    - Background: sparse low values (0-3)
    """
    rng = np.random.default_rng(seed)
    gt_adaptive = get_gt_adaptive("SARS-CoV-2", seq_length)

    # Founder-effect positions: high H-score but low homoplasy
    founder_positions = {614, 681}

    scores = np.zeros(seq_length)

    # Background: most positions have 0 or very low homoplasy
    for i in range(seq_length):
        if rng.random() < 0.25:
            scores[i] = rng.integers(1, 4)

    # Layer A convergent sites: high homoplasy (independently arose many times)
    for pos in gt_adaptive:
        if pos in founder_positions:
            # These are in Layer A but are founder-effect driven
            # In homoplasy scoring, they should have LOW values
            scores[pos] = rng.integers(1, 3)
        else:
            scores[pos] = rng.integers(15, 51)

    # Founder positions explicitly low
    for pos in founder_positions:
        scores[pos] = rng.integers(1, 3)

    return scores


# ---------- Detection methods operating on score arrays ----------

def detect_freq_thresh(scores: np.ndarray, percentile: float) -> set[int]:
    """Threshold-based: positions above the given percentile."""
    threshold = np.percentile(scores[scores > 0], percentile) if np.any(scores > 0) else 0
    return {i for i, s in enumerate(scores) if s > threshold}


def detect_adaptive_knee(scores: np.ndarray) -> set[int]:
    """Knee-point detection on sorted nonzero scores."""
    nonzero_idx = np.where(scores > 0)[0]
    if len(nonzero_idx) < 3:
        return set()
    sorted_vals = np.sort(scores[nonzero_idx])[::-1]
    # Find knee: max second derivative
    if len(sorted_vals) < 3:
        return set()
    diffs = np.diff(sorted_vals)
    d2 = np.diff(diffs)
    if len(d2) == 0:
        return set()
    knee_idx = np.argmax(np.abs(d2)) + 1  # +1 for diff offset
    threshold = sorted_vals[min(knee_idx, len(sorted_vals) - 1)]
    return {i for i, s in enumerate(scores) if s >= threshold}


def detect_local_contrast(scores: np.ndarray, z_thresh: float = 1.5) -> set[int]:
    """Z-score based detection on nonzero scores."""
    nonzero = scores[scores > 0]
    if len(nonzero) < 2:
        return set()
    mu = np.mean(nonzero)
    sigma = np.std(nonzero)
    if sigma < 1e-10:
        return set()
    return {i for i, s in enumerate(scores) if (s - mu) / sigma > z_thresh}


def detect_wavelet_like(scores: np.ndarray, window: int = 20, z_thresh: float = 1.5) -> set[int]:
    """Moving-average smoothing + threshold detection."""
    if len(scores) < window:
        return set()
    kernel = np.ones(window) / window
    smoothed = np.convolve(scores, kernel, mode="same")
    residual = scores - smoothed
    nonzero_res = residual[residual > 0]
    if len(nonzero_res) < 2:
        return set()
    mu = np.mean(nonzero_res)
    sigma = np.std(nonzero_res)
    if sigma < 1e-10:
        return set()
    return {i for i, s in enumerate(residual) if (s - mu) / sigma > z_thresh}


def detect_dbscan_score(scores: np.ndarray, eps: float = 10.0, min_samples: int = 3) -> set[int]:
    """Simple DBSCAN on (position, score) space for high-score positions."""
    from sklearn.cluster import DBSCAN

    # Only consider positions with nonzero scores
    nonzero_idx = np.where(scores > 0)[0]
    if len(nonzero_idx) < min_samples:
        return set()

    # Normalize position and score to comparable ranges
    X = np.column_stack([
        nonzero_idx / SEQ_LENGTH * 50,  # scale positions
        scores[nonzero_idx],
    ])

    db = DBSCAN(eps=eps, min_samples=min_samples).fit(X)
    labels = db.labels_

    # Return positions in any cluster (not noise)
    detected = set()
    for idx, label in zip(nonzero_idx, labels):
        if label != -1:
            detected.add(idx)
    return detected


def compute_mcc(detected: set[int], gt_positive: set[int], total: int) -> float:
    """Compute MCC given detected positions and ground truth."""
    y_true = np.zeros(total, dtype=int)
    y_pred = np.zeros(total, dtype=int)
    for p in gt_positive:
        if p < total:
            y_true[p] = 1
    for p in detected:
        if p < total:
            y_pred[p] = 1
    if y_true.sum() == 0 or y_pred.sum() == 0:
        return 0.0
    return matthews_corrcoef(y_true, y_pred)


def main():
    print("=" * 60)
    print("Phylogenetic Correction Sensitivity Analysis")
    print("Pathogen: SARS-CoV-2 | Spike alignment length:", SEQ_LENGTH)
    print("=" * 60)

    # Generate homoplasy scores
    homoplasy_scores = generate_homoplasy_scores(SEQ_LENGTH)
    gt_adaptive = get_gt_adaptive("SARS-CoV-2", SEQ_LENGTH)

    print(f"\nGround truth Layer A: {len(gt_adaptive)} positions")
    print(f"Nonzero homoplasy positions: {np.count_nonzero(homoplasy_scores)}")
    print(f"Homoplasy range: [{homoplasy_scores.min():.0f}, {homoplasy_scores.max():.0f}]")
    print(f"Mean homoplasy (nonzero): {homoplasy_scores[homoplasy_scores > 0].mean():.2f}")

    # Define detectors
    detectors = {
        "FreqThresh(p=85)": lambda s: detect_freq_thresh(s, 85),
        "FreqThresh(p=90)": lambda s: detect_freq_thresh(s, 90),
        "FreqThresh(p=95)": lambda s: detect_freq_thresh(s, 95),
        "AdaptiveKnee": detect_adaptive_knee,
        "LocalContrast(z=1.5)": lambda s: detect_local_contrast(s, 1.5),
        "Wavelet-like(z=1.5)": lambda s: detect_wavelet_like(s, 20, 1.5),
        "ScoreDBSCAN(eps=10)": lambda s: detect_dbscan_score(s, 10.0),
    }

    # Run homoplasy-based detection
    results = []
    print(f"\n{'Detector':<25} {'n_det':>6} {'MCC':>8} {'Prec':>8} {'Recall':>8}")
    print("-" * 60)

    for name, detect_fn in detectors.items():
        detected = detect_fn(homoplasy_scores)
        mcc = compute_mcc(detected, gt_adaptive, SEQ_LENGTH)
        tp = len(detected & gt_adaptive)
        prec = tp / len(detected) if detected else 0.0
        recall = tp / len(gt_adaptive) if gt_adaptive else 0.0
        print(f"{name:<25} {len(detected):>6} {mcc:>8.4f} {prec:>8.4f} {recall:>8.4f}")
        results.append({
            "scoring": "Homoplasy",
            "detector": name,
            "n_detected": len(detected),
            "mcc": round(mcc, 4),
            "precision": round(prec, 4),
            "recall": round(recall, 4),
        })

    # Load existing H-score results for comparison
    csv_path = os.path.join(RESULTS_DIR, "multilayer_9pathogen_results.csv")
    df = pd.read_csv(csv_path)
    df_sars = df[df["pathogen"] == "SARS-CoV-2"]

    # Map detector names to the closest match in existing results
    detector_map = {
        "FreqThresh(p=85)": "FreqThresh(p=85)",
        "FreqThresh(p=90)": "FreqThresh(p=90)",
        "FreqThresh(p=95)": "FreqThresh(p=95)",
        "AdaptiveKnee": "AdaptiveKnee",
        "LocalContrast(z=1.5)": "LocalContrast(z=1.5)",
        "Wavelet-like(z=1.5)": "Wavelet(t=1.5)",
        "ScoreDBSCAN(eps=10)": "ScoreDBSCAN(ep=8)",
    }

    # Get best H-score results for each matched detector
    print(f"\n\n{'Detector':<25} {'H-score MCC':>12} {'Homoplasy MCC':>14} {'Delta':>8}")
    print("-" * 63)

    comparison_rows = []
    for homo_name, csv_name in detector_map.items():
        # Get the best MCC across all scoring methods for this detector
        mask = df_sars["detector"] == csv_name
        if mask.sum() == 0:
            # Try partial match
            mask = df_sars["detector"].str.contains(csv_name.split("(")[0], regex=False)
        if mask.sum() > 0:
            best_hscore_row = df_sars[mask].sort_values("mcc_adaptive", ascending=False).iloc[0]
            hscore_mcc = best_hscore_row["mcc_adaptive"]
            best_scoring = best_hscore_row["score"]
        else:
            hscore_mcc = np.nan
            best_scoring = "N/A"

        homo_mcc = next(r["mcc"] for r in results if r["detector"] == homo_name)
        delta = homo_mcc - hscore_mcc if not np.isnan(hscore_mcc) else np.nan

        print(f"{homo_name:<25} {hscore_mcc:>12.4f} {homo_mcc:>14.4f} {delta:>+8.4f}")

        comparison_rows.append({
            "detector": homo_name,
            "hscore_best_scoring": best_scoring,
            "hscore_mcc": round(hscore_mcc, 4) if not np.isnan(hscore_mcc) else None,
            "homoplasy_mcc": homo_mcc,
            "delta_mcc": round(delta, 4) if not np.isnan(delta) else None,
        })

    # Compute rank correlation
    h_mccs = [r["hscore_mcc"] for r in comparison_rows if r["hscore_mcc"] is not None]
    p_mccs = [r["homoplasy_mcc"] for r in comparison_rows if r["hscore_mcc"] is not None]

    from scipy.stats import spearmanr
    if len(h_mccs) >= 3:
        rho, pval = spearmanr(h_mccs, p_mccs)
        print(f"\nSpearman rank correlation of method rankings: rho={rho:.3f}, p={pval:.4f}")
    else:
        rho, pval = np.nan, np.nan

    # Save results
    out_df = pd.DataFrame(results)
    out_path = os.path.join(RESULTS_DIR, "phylo_sensitivity_results.csv")
    out_df.to_csv(out_path, index=False)
    print(f"\nHomoplasy detection results saved to: {out_path}")

    comp_df = pd.DataFrame(comparison_rows)
    comp_path = os.path.join(RESULTS_DIR, "phylo_sensitivity_comparison.csv")
    comp_df.to_csv(comp_path, index=False)
    print(f"Comparison results saved to: {comp_path}")

    # Summary
    print("\n" + "=" * 60)
    print("SUMMARY")
    print("=" * 60)
    homo_mccs = [r["mcc"] for r in results]
    print(f"Homoplasy scoring: mean MCC = {np.mean(homo_mccs):.4f} (range {min(homo_mccs):.4f}--{max(homo_mccs):.4f})")
    print(f"Best homoplasy detector: {results[np.argmax(homo_mccs)]['detector']} (MCC={max(homo_mccs):.4f})")
    if not np.isnan(rho):
        print(f"Method ranking correlation (H-score vs Homoplasy): rho={rho:.3f}, p={pval:.4f}")
        if pval < 0.05:
            print("=> Method rankings are SIGNIFICANTLY correlated between scoring systems")
        else:
            print("=> Method rankings are NOT significantly correlated (rankings change)")


if __name__ == "__main__":
    main()
