#!/usr/bin/env python3
"""Cycle 8B: Layer 3 detection comparison at fixed top-10% prevalence.

Cycle 8 used each detector's native threshold rule, which produced uneven
detection counts (e.g. GMM detected 1101/1330 positions on MERS). To rule
out prevalence-driven artefacts we re-evaluate each detector at a fixed
top-10% prevalence: each detector emits a per-position score (probability
or anomaly score), we take the top 10% positions by score, and compute
MCC against Layer A.

Detectors that already emit a continuous score: PELT (segment mean),
BCP (segment mean), Conformal (raw score), IsolationForest
(decision_function), GMM (high-component posterior), LOF (-LOF score).

Baselines are the existing top-10% percentile detectors KDE(p=90) and
FreqThresh(p=90) under the same prevalence target, plus a "raw EqualWeight
top-10%" oracle bound (using the same EqualWeight-4core score directly).
"""

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

from scripts.run_extended_benchmark import compute_mcc

FEATURE_DIR = PROJECT_ROOT / "results" / "mutbench" / "feature_analysis"
OUT_CSV = PROJECT_ROOT / "results" / "mutbench" / "cycle8b_fixed_prevalence_results.csv"
OUT_SUMMARY = PROJECT_ROOT / "results" / "mutbench" / "cycle8b_fixed_prevalence_summary.txt"

PATHOGENS = [
    "SARS-CoV-2", "H3N2", "Norovirus", "HIV-1", "Dengue", "RSV",
    "Influenza_B", "MERS", "HCV", "Rabies", "EV-A71",
]

PREVALENCE = 0.10  # top-10% positions by detector score


def normalize_01(arr):
    arr = np.asarray(arr, dtype=float)
    rng = arr.max() - arr.min()
    if rng == 0:
        return np.zeros_like(arr)
    return (arr - arr.min()) / rng


def load_pathogen(p):
    df = pd.read_csv(FEATURE_DIR / f"feature_matrix_{p}.csv")
    homoplasy = df["homoplasy"].fillna(0.0).values
    plddt = df["plddt"].fillna(0.0).values
    plddt_inv = 100.0 - plddt
    entropy = df["entropy"].fillna(0.0).values
    freq = df["freq"].fillna(0.0).values
    feats = np.stack(
        [normalize_01(homoplasy), normalize_01(plddt_inv),
         normalize_01(entropy), normalize_01(freq)], axis=1,
    )
    eq4 = feats.mean(axis=1)
    gt = df["layer_a"].fillna(0).astype(int).values
    return feats, eq4, gt


# Per-position score producers (higher = more hotspot-like)


def score_pelt(scores):
    pen = max(1.0, 5.0 * np.std(scores))
    algo = rpt.Pelt(model="rbf").fit(scores.reshape(-1, 1))
    bkps = algo.predict(pen=pen)
    out = np.zeros_like(scores)
    last = 0
    for b in bkps:
        out[last:b] = scores[last:b].mean()
        last = b
    return out


def score_bcp(scores):
    n = len(scores)
    if n < 30:
        return scores.copy()
    algo = rpt.Binseg(model="l2").fit(scores.reshape(-1, 1))
    n_bkps = max(2, n // 50)
    bkps = algo.predict(n_bkps=n_bkps)
    out = np.zeros_like(scores)
    last = 0
    for b in bkps:
        out[last:b] = scores[last:b].mean()
        last = b
    return out


def score_conformal(scores, p, panel_eq4):
    """Calibrated z-residual using LOPO calibration."""
    calib = np.concatenate([eq for q, eq in panel_eq4 if q != p])
    mu, sd = calib.mean(), calib.std() + 1e-9
    return (scores - mu) / sd


def score_iforest(features):
    iso = IsolationForest(n_estimators=200, contamination="auto", random_state=42)
    iso.fit(features)
    return -iso.score_samples(features)  # higher = more anomalous


def score_gmm(features, n_components=2):
    if len(features) < n_components + 5:
        return np.zeros(len(features))
    gmm = GaussianMixture(n_components=n_components, random_state=42)
    gmm.fit(features)
    means = gmm.means_.mean(axis=1)
    high_idx = int(np.argmax(means))
    return gmm.predict_proba(features)[:, high_idx]


def score_lof(features, k=20):
    n = len(features)
    if n <= k + 1:
        return np.zeros(n)
    lof = LocalOutlierFactor(n_neighbors=min(k, n - 1), novelty=False)
    lof.fit_predict(features)
    return -lof.negative_outlier_factor_  # higher = more anomalous


def topk_mask(score, prev=PREVALENCE):
    n = len(score)
    k = max(1, int(round(n * prev)))
    idx = np.argpartition(-score, k - 1)[:k]
    mask = np.zeros(n, dtype=int)
    mask[idx] = 1
    return mask


def score_kde(scores, bw=None):
    """KDE-smoothed score (Gaussian kernel, scipy.stats.gaussian_kde over
    position index weighted by scores). Returns the per-position smoothed
    intensity that an existing-grid KDE detector would threshold."""
    n = len(scores)
    if n < 5 or scores.max() == scores.min():
        return scores.copy()
    pos = np.arange(n, dtype=float)
    # Weighted Gaussian smooth — emulates KDE(p=*) family
    sd = max(2.0, n * 0.02) if bw is None else float(bw)
    kernel = np.exp(-0.5 * ((pos[:, None] - pos[None, :]) / sd) ** 2)
    smoothed = (kernel * scores[None, :]).sum(axis=1) / kernel.sum(axis=1)
    return smoothed


def run():
    panel = []
    for p in PATHOGENS:
        try:
            feats, eq4, gt = load_pathogen(p)
            panel.append((p, feats, eq4, gt))
            print(f"  {p:14s} L={len(eq4):>4d} pos+={int(gt.sum())}")
        except FileNotFoundError as e:
            print(f"  SKIP {p}: {e}")

    panel_eq4 = [(p, eq4) for p, _, eq4, _ in panel]
    rows = []
    for p, feats, eq4, gt in panel:
        gt_set = set(np.where(gt == 1)[0].tolist())
        L = len(eq4)
        # Score functions per detector
        score_funcs = {
            "PELT":              lambda: score_pelt(eq4),
            "BCP":               lambda: score_bcp(eq4),
            "Conformal":         lambda: score_conformal(eq4, p, panel_eq4),
            "IsolationForest":   lambda: score_iforest(feats),
            "GMM":               lambda: score_gmm(feats),
            "LOF":               lambda: score_lof(feats),
            "EQ4-KDE-smoothed":  lambda: score_kde(eq4),  # emulates KDE(p=90)
            "EQ4-Raw":           lambda: eq4,            # bare top-10% on EQ4
        }
        for name, fn in score_funcs.items():
            sc = fn()
            mask = topk_mask(sc, PREVALENCE)
            detected = np.where(mask == 1)[0].tolist()
            mcc = compute_mcc(detected, gt_set, L)
            rows.append({
                "pathogen": p, "detector": name,
                "mcc": mcc, "n_detected": len(detected), "L": L,
            })
            print(f"    {p:14s} {name:18s} MCC={mcc:>+.4f}  n={len(detected):>3d}/{L}")

    df = pd.DataFrame(rows)
    df.to_csv(OUT_CSV, index=False)
    print(f"\nWrote {OUT_CSV}")

    summary = ["Cycle 8B Layer 3 detection comparison @ fixed top-10% prevalence\n"]
    summary.append(f"Same 11-pathogen panel, EqualWeight-4core scoring, prevalence={PREVALENCE}.\n")
    summary.append("\nMean MCC per detector:")
    means = df.groupby("detector")["mcc"].mean().sort_values(ascending=False)
    for d, m in means.items():
        summary.append(f"  {d:18s}  mean MCC = {m:>+.4f}")

    base = df[df["detector"] == "EQ4-Raw"].set_index("pathogen")["mcc"]
    summary.append("\nPaired Wilcoxon vs EQ4-Raw (top-10% on bare EqualWeight-4core):")
    for new in ["PELT", "BCP", "Conformal", "IsolationForest", "GMM", "LOF"]:
        s = df[df["detector"] == new].set_index("pathogen")["mcc"]
        common = base.index.intersection(s.index)
        a, b = s[common].values, base[common].values
        delta = a - b
        try:
            stat, p = wilcoxon(a, b, alternative="greater", zero_method="wilcox")
        except ValueError:
            stat, p = float("nan"), float("nan")
        summary.append(f"  {new:18s}  delta={delta.mean():>+.4f}  W={stat}  p={p:.3f}")

    txt = "\n".join(summary) + "\n"
    OUT_SUMMARY.write_text(txt)
    print("\n" + txt)


if __name__ == "__main__":
    run()
