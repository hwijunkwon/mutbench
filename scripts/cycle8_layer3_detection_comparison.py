#!/usr/bin/env python3
"""Cycle 8: Layer 3 detection-algorithm comparison vs the existing 22-detector grid.

Tests 6 detection paradigms not in the dissertation's stage 3 grid:

  1. PELT (Pruned Exact Linear Time change-point) on the EqualWeight-4core score.
  2. BCP (Binary segmentation change-point via window BIC).
  3. ConformalThreshold (cross-pathogen calibrated quantile of EqualWeight scores).
  4. IsolationForest on the 4-feature multivariate vector (homoplasy, pLDDT_inv,
     entropy, freq).
  5. GMM (2-component Gaussian Mixture posterior on the 4-feature vector).
  6. LOF (Local Outlier Factor on the 4-feature vector).

Scope: same 11-pathogen Layer A panel as stage 3 (Zika excluded). The
EqualWeight-4core scoring is fixed so the comparison is purely about Layer 3
(detection algorithm), independent of the Layer 2 (integration) Cycle 7B
results.

Baselines for paired Wilcoxon (one-sided H1: new detector > baseline):
  - KDE(p=85)  — best stage 3 family of the existing grid for general use.
  - Wavelet(t=1.5) — second-best stage 3 family on Layer A.

Output:
  results/mutbench/cycle8_layer3_results.csv
  results/mutbench/cycle8_layer3_summary.txt
"""

import os
import sys
import warnings
from pathlib import Path

import numpy as np
import pandas as pd
from scipy.stats import wilcoxon
from sklearn.ensemble import IsolationForest
from sklearn.mixture import GaussianMixture
from sklearn.neighbors import LocalOutlierFactor

import ruptures as rpt

warnings.filterwarnings("ignore")

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from scripts.run_extended_benchmark import (
    KDEDetector,
    WaveletDetector,
    compute_mcc,
)

FEATURE_DIR = PROJECT_ROOT / "results" / "mutbench" / "feature_analysis"
OUT_CSV = PROJECT_ROOT / "results" / "mutbench" / "cycle8_layer3_results.csv"
OUT_SUMMARY = PROJECT_ROOT / "results" / "mutbench" / "cycle8_layer3_summary.txt"

PATHOGENS = [
    "SARS-CoV-2", "H3N2", "Norovirus", "HIV-1", "Dengue", "RSV",
    "Influenza_B", "MERS", "HCV", "Rabies", "EV-A71",
]

PLDDT_MAX = 100.0  # for inverse transform


def normalize_01(arr):
    arr = np.asarray(arr, dtype=float)
    rng = arr.max() - arr.min()
    if rng == 0:
        return np.zeros_like(arr)
    return (arr - arr.min()) / rng


def load_pathogen(pathogen):
    """Return (4-feature matrix [L,4], EqualWeight-4core score [L], gt [L]).

    4-feature core: homoplasy, plddt_inv, entropy, freq (the EqualWeight-4core
    that all 7 Cycle 7B paradigms could not beat).
    """
    df = pd.read_csv(FEATURE_DIR / f"feature_matrix_{pathogen}.csv")
    # 4-core features
    homoplasy = df["homoplasy"].fillna(0.0).values
    plddt = df["plddt"].fillna(0.0).values
    plddt_inv = PLDDT_MAX - plddt
    entropy = df["entropy"].fillna(0.0).values
    freq = df["freq"].fillna(0.0).values
    feats = np.stack(
        [normalize_01(homoplasy), normalize_01(plddt_inv),
         normalize_01(entropy), normalize_01(freq)],
        axis=1,
    )  # [L, 4]
    eq4 = feats.mean(axis=1)
    gt = df["layer_a"].fillna(0).astype(int).values
    return feats, eq4, gt


# -- New detectors (BaseDetector-compatible) -------------------------------


def detect_pelt(scores, top_k_target=None):
    """PELT change-point segmentation; emit positions whose segment mean is in
    the top decile across segments."""
    pen = max(1.0, 5.0 * np.std(scores))
    algo = rpt.Pelt(model="rbf").fit(scores.reshape(-1, 1))
    bkps = algo.predict(pen=pen)
    seg_means = []
    last = 0
    for b in bkps:
        seg_means.append((last, b, scores[last:b].mean()))
        last = b
    if not seg_means:
        return np.zeros_like(scores, dtype=int)
    means = np.array([m[2] for m in seg_means])
    threshold = np.quantile(means, 0.9)
    mask = np.zeros_like(scores, dtype=int)
    for s, e, mu in seg_means:
        if mu >= threshold:
            mask[s:e] = 1
    return mask


def detect_bcp(scores):
    """Binary segmentation via ruptures Window/BinSeg; same top-decile-segment
    rule as PELT."""
    n = len(scores)
    if n < 30:
        return np.zeros(n, dtype=int)
    algo = rpt.Binseg(model="l2").fit(scores.reshape(-1, 1))
    n_bkps = max(2, n // 50)
    bkps = algo.predict(n_bkps=n_bkps)
    last = 0
    seg = []
    for b in bkps:
        seg.append((last, b, scores[last:b].mean()))
        last = b
    means = np.array([m[2] for m in seg])
    threshold = np.quantile(means, 0.9)
    mask = np.zeros(n, dtype=int)
    for s, e, mu in seg:
        if mu >= threshold:
            mask[s:e] = 1
    return mask


def detect_conformal(scores, pathogen, calib_set):
    """Cross-pathogen conformal threshold: take the 90th-percentile residual
    of EqualWeight scores from the calibration pathogens (LOPO calibration)."""
    calib_scores = np.concatenate([s for p, s in calib_set if p != pathogen])
    threshold = np.quantile(calib_scores, 0.9)
    return (scores >= threshold).astype(int)


def detect_isolation_forest(features, n_estimators=200):
    """Multivariate outlier detection on the 4-feature vector."""
    iso = IsolationForest(
        n_estimators=n_estimators, contamination=0.1, random_state=42,
    )
    iso.fit(features)
    pred = iso.predict(features)  # +1 = inlier, -1 = outlier
    return (pred == -1).astype(int)


def detect_gmm(features, n_components=2):
    """2-component GMM; flag positions whose posterior on the higher-mean
    component exceeds 0.5."""
    if len(features) < n_components + 5:
        return np.zeros(len(features), dtype=int)
    gmm = GaussianMixture(n_components=n_components, random_state=42)
    gmm.fit(features)
    means = gmm.means_.mean(axis=1)
    high_idx = int(np.argmax(means))
    posterior = gmm.predict_proba(features)[:, high_idx]
    return (posterior >= 0.5).astype(int)


def detect_lof(features, k=20):
    """Local Outlier Factor on the 4-feature vector."""
    n = len(features)
    if n <= k + 1:
        return np.zeros(n, dtype=int)
    lof = LocalOutlierFactor(n_neighbors=min(k, n - 1), contamination=0.1)
    pred = lof.fit_predict(features)
    return (pred == -1).astype(int)


# -- Driver ----------------------------------------------------------------


def run():
    panel = []
    for p in PATHOGENS:
        try:
            feats, eq4, gt = load_pathogen(p)
            panel.append((p, feats, eq4, gt))
            print(f"  {p:14s} L={len(eq4):>4d} pos+={int(gt.sum())}")
        except FileNotFoundError as e:
            print(f"  SKIP {p}: {e}")
    if not panel:
        print("No pathogens loaded; aborting.")
        return

    calib_set = [(p, eq4) for p, _, eq4, _ in panel]

    rows = []
    for p, feats, eq4, gt in panel:
        gt_set = set(np.where(gt == 1)[0].tolist())
        L = len(eq4)

        # New Layer 3 detectors (mask -> position list)
        for name, mask in [
            ("PELT", detect_pelt(eq4)),
            ("BCP", detect_bcp(eq4)),
            ("Conformal", detect_conformal(eq4, p, calib_set)),
            ("IsolationForest", detect_isolation_forest(feats)),
            ("GMM", detect_gmm(feats)),
            ("LOF", detect_lof(feats)),
        ]:
            detected = np.where(mask == 1)[0].tolist()
            mcc = compute_mcc(detected, gt_set, L)
            rows.append({
                "pathogen": p, "detector": name,
                "mcc": mcc, "n_detected": len(detected), "L": L,
            })
            print(f"    {p:14s} {name:18s} MCC={mcc:>+.4f}  detected={len(detected):>4d}")

        # Baselines (existing stage 3 grid)
        for det in [KDEDetector(threshold_pct=85), WaveletDetector(threshold=1.5)]:
            try:
                positions, _ = det.detect(eq4)
                detected = list(positions)
            except Exception as e:
                detected = []
                print(f"    {p}: {det.name} failed ({e})")
            mcc = compute_mcc(detected, gt_set, L)
            rows.append({
                "pathogen": p, "detector": det.name,
                "mcc": mcc, "n_detected": len(detected), "L": L,
            })
            print(f"    {p:14s} {det.name:18s} MCC={mcc:>+.4f}  detected={len(detected):>4d}")

    df = pd.DataFrame(rows)
    df.to_csv(OUT_CSV, index=False)
    print(f"\nWrote {OUT_CSV} ({len(df)} rows)")

    # Paired Wilcoxon vs each baseline
    summary_lines = ["Cycle 8 Layer 3 detection-algorithm comparison\n"]
    summary_lines.append(
        "Protocol: 11 pathogens, EqualWeight-4core scoring fixed, top-10% prevalence "
        "threshold approximated by detector-internal threshold. MCC computed against "
        "Layer A. Paired Wilcoxon, one-sided greater (H1: new detector > baseline).\n"
    )
    summary_lines.append("\nMean MCC per detector:")
    means = df.groupby("detector")["mcc"].mean().sort_values(ascending=False)
    for d, m in means.items():
        summary_lines.append(f"  {d:25s}  mean MCC = {m:>+.4f}")

    summary_lines.append("\nPaired Wilcoxon vs KDE(p=85):")
    base_kde = df[df["detector"] == "KDE(p=85)"].set_index("pathogen")["mcc"]
    for new in ["PELT", "BCP", "Conformal", "IsolationForest", "GMM", "LOF"]:
        new_s = df[df["detector"] == new].set_index("pathogen")["mcc"]
        common = base_kde.index.intersection(new_s.index)
        a, b = new_s[common].values, base_kde[common].values
        delta = a - b
        try:
            stat, p = wilcoxon(a, b, alternative="greater", zero_method="wilcox")
        except ValueError:
            stat, p = float("nan"), float("nan")
        summary_lines.append(
            f"  {new:18s}  delta={delta.mean():>+.4f}  W={stat}  p={p:.3f}"
        )

    summary_lines.append("\nPaired Wilcoxon vs Wavelet(t=1.5):")
    base_w = df[df["detector"] == "Wavelet(t=1.5)"].set_index("pathogen")["mcc"]
    for new in ["PELT", "BCP", "Conformal", "IsolationForest", "GMM", "LOF"]:
        new_s = df[df["detector"] == new].set_index("pathogen")["mcc"]
        common = base_w.index.intersection(new_s.index)
        a, b = new_s[common].values, base_w[common].values
        delta = a - b
        try:
            stat, p = wilcoxon(a, b, alternative="greater", zero_method="wilcox")
        except ValueError:
            stat, p = float("nan"), float("nan")
        summary_lines.append(
            f"  {new:18s}  delta={delta.mean():>+.4f}  W={stat}  p={p:.3f}"
        )

    txt = "\n".join(summary_lines) + "\n"
    OUT_SUMMARY.write_text(txt)
    print(f"Wrote {OUT_SUMMARY}\n")
    print(txt)


if __name__ == "__main__":
    run()
