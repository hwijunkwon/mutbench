#!/usr/bin/env python3
"""Sliding-window prospective backtest (Tier C2).

For each pathogen with extractable per-sequence years, perform a
rolling-window prospective evaluation:

  - For each split year T0 in a per-pathogen schedule, train on
    sequences with year < T0 (compute per-position freq, entropy).
  - Test set: positions that "newly emerge" in the post-T0 window
    (year >= T0), defined as freq < EMERGENCE_LOW in train AND
    freq >= EMERGENCE_HIGH in test (default 5%/10%, matching the
    H3N2 pilot in subsec:h3n2_temporal_pilot).
  - Score positions on the train window using freq, entropy, and a
    uniform-weight (freq, entropy) z-ensemble (the time-varying part
    of the dissertation's 4-feature core).
  - Report per-window MCC, F1, AUROC, top-K enrichment vs the
    "newly emergent" reference.

This is a prospective sanity check, not a full 4-feature evaluation:
the homoplasy and pLDDT features in the dissertation's 4-feature core
live in a different MSA coordinate frame (the protein _sequences.fasta
MSAs without year metadata), so they are *not* re-trained per window.
The freq+entropy 2-of-4 sub-ensemble nevertheless provides a genuine
forward-time generalisation measurement.

Outputs:
  results/mutbench/feature_analysis/sliding_window_prospective_backtest.csv
  results/mutbench/feature_analysis/sliding_window_prospective_backtest_summary.csv
  paper/dissertation/figures/sliding_window_prospective_backtest.png
"""

from __future__ import annotations

import os
import re
import sys
import warnings
from collections import Counter
from pathlib import Path

import numpy as np
import pandas as pd
from Bio import SeqIO
from Bio.Seq import Seq
from sklearn.metrics import matthews_corrcoef, roc_auc_score, f1_score

warnings.filterwarnings("ignore")

PROJECT_ROOT = Path(__file__).resolve().parent.parent
OUT_DIR = PROJECT_ROOT / "results" / "mutbench" / "feature_analysis"
FIG_DIR = PROJECT_ROOT / "paper" / "dissertation" / "figures"
OUT_DIR.mkdir(parents=True, exist_ok=True)
FIG_DIR.mkdir(parents=True, exist_ok=True)

# ---------------------------------------------------------------------------
# Datasets
# ---------------------------------------------------------------------------
PATHOGEN_FASTA = {
    "H3N2": "/proj/paper/data/influenza/h3n2_ha_nt_cds_aligned.fasta",
    "Influenza_B": "/proj/paper/data/influenza/influenza_b_ha_nt_cds_aligned.fasta",
    "Dengue": "/proj/paper/data/dengue/dengue_e_nt_cds_aligned.fasta",
    "RSV": "/proj/paper/data/rsv/rsv_f_nt_cds_aligned.fasta",
    "HCV": "/proj/paper/data/hcv/hcv_e2_nt_cds_aligned.fasta",
    "Norovirus": "/proj/paper/data/norovirus/norovirus_vp1_nt_cds_aligned.fasta",
    "EV-A71": "/proj/paper/data/enterovirus/eva71_vp1_nt_cds_aligned.fasta",
    "Rabies": "/proj/paper/data/rabies/rabies_g_nt_cds_aligned.fasta",
    "HIV-1": "/proj/paper/data/hiv/hiv1_gp120_nt_cds_aligned.fasta",
    "MERS": "/proj/paper/data/mers/mers_spike_nt_cds_aligned.fasta",
    "SARS-CoV-2": "/proj/paper/data/ncbi_temporal/sars2_spike_nt_cds_aligned.fasta",
}

YEAR_RE = re.compile(r"(?:19|20)\d{2}")

# Configuration
EMERGENCE_LOW = 0.05  # consensus freq < 5% in train
EMERGENCE_HIGH = 0.10  # mutation freq >= 10% in test
TOP_K = 30  # top-K ranking comparison
MIN_TRAIN = 30  # require at least 30 sequences in train window
MIN_TEST = 20  # require at least 20 in test window


# ---------------------------------------------------------------------------
# Data loading
# ---------------------------------------------------------------------------

def extract_year(description: str) -> int | None:
    ms = YEAR_RE.findall(description)
    ys = [int(m) for m in ms if 1980 <= int(m) <= 2026]
    return min(ys) if ys else None


def translate_codon_aln(nt_seq: str) -> str:
    aa = []
    for i in range(0, len(nt_seq) - 2, 3):
        codon = nt_seq[i:i + 3].upper()
        if "-" in codon or "N" in codon:
            aa.append("-")
            continue
        try:
            tr = str(Seq(codon).translate())
            if tr == "*":
                aa.append("-")
            else:
                aa.append(tr)
        except Exception:
            aa.append("X")
    return "".join(aa)


def load_pathogen(pathogen: str, fp: str):
    recs = list(SeqIO.parse(fp, "fasta"))
    rows = []
    for r in recs:
        y = extract_year(r.description)
        if y is None:
            continue
        aa = translate_codon_aln(str(r.seq))
        rows.append({"id": r.id, "year": y, "aa": aa})
    if not rows:
        return None, None
    df = pd.DataFrame(rows)
    L = max(len(s) for s in df["aa"])
    df["aa"] = df["aa"].apply(lambda s: s + "-" * (L - len(s)))
    return df, L


# ---------------------------------------------------------------------------
# Feature computation
# ---------------------------------------------------------------------------

def compute_freq_entropy(seqs: list[str]) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    """Per-position freq (1 - consensus%), entropy, and consensus character."""
    if not seqs:
        return np.zeros(0), np.zeros(0), np.array([], dtype="<U1")
    L = len(seqs[0])
    freq = np.zeros(L)
    ent = np.zeros(L)
    cons = np.empty(L, dtype="<U1")
    cons[:] = "-"
    for pos in range(L):
        col = [s[pos] for s in seqs]
        counts = Counter(c for c in col if c not in ("-", ".", "X", "N"))
        if not counts:
            continue
        total = sum(counts.values())
        if total == 0:
            continue
        most_aa, most_n = counts.most_common(1)[0]
        cons[pos] = most_aa
        freq[pos] = 1.0 - most_n / total
        e = 0.0
        for k in counts.values():
            f = k / total
            if f > 0:
                e -= f * np.log2(f)
        ent[pos] = e
    return freq, ent, cons


def compute_emergent_positions(
    train_seqs: list[str],
    test_seqs: list[str],
    train_freq: np.ndarray,
    test_freq: np.ndarray,
    low: float = EMERGENCE_LOW,
    high: float = EMERGENCE_HIGH,
) -> np.ndarray:
    """Positions where consensus is stable in train (freq < low) but a
    non-consensus allele rises to freq >= high in test."""
    return ((train_freq < low) & (test_freq >= high)).astype(int)


# ---------------------------------------------------------------------------
# Scoring & metrics
# ---------------------------------------------------------------------------

def safe_mcc(y, yhat):
    y = np.asarray(y, dtype=int); yhat = np.asarray(yhat, dtype=int)
    if y.sum() == 0 or y.sum() == len(y):
        return float("nan")
    if yhat.sum() == 0 or yhat.sum() == len(yhat):
        return 0.0
    return matthews_corrcoef(y, yhat)


def safe_f1(y, yhat):
    y = np.asarray(y, dtype=int); yhat = np.asarray(yhat, dtype=int)
    if y.sum() == 0:
        return float("nan")
    return f1_score(y, yhat)


def safe_auroc(y, score):
    y = np.asarray(y, dtype=int); score = np.asarray(score, dtype=float)
    if y.sum() == 0 or y.sum() == len(y):
        return float("nan")
    try:
        return roc_auc_score(y, score)
    except ValueError:
        return float("nan")


def topk_threshold(score: np.ndarray, k: int) -> np.ndarray:
    if k >= len(score):
        return np.ones_like(score, dtype=int)
    thr = np.sort(score)[-k]
    return (score >= thr).astype(int)


def topk_enrichment(score: np.ndarray, y: np.ndarray, k: int) -> tuple[float, float]:
    """Return enrichment fold and Fisher one-sided p (top-K)."""
    from scipy.stats import fisher_exact
    pred = topk_threshold(score, k)
    a = int(((pred == 1) & (y == 1)).sum())
    b = int(((pred == 1) & (y == 0)).sum())
    c = int(((pred == 0) & (y == 1)).sum())
    d = int(((pred == 0) & (y == 0)).sum())
    n_pos = int(y.sum())
    n = len(y)
    if n_pos == 0 or k == 0 or n == 0:
        return float("nan"), float("nan")
    base = n_pos / n
    obs = a / max(k, 1)
    fold = obs / base if base > 0 else float("nan")
    try:
        _, p = fisher_exact([[a, b], [c, d]], alternative="greater")
    except Exception:
        p = float("nan")
    return fold, p


def zscore_uniform(*arrays) -> np.ndarray:
    Z = []
    for a in arrays:
        a = np.nan_to_num(a, nan=0.0, posinf=0.0, neginf=0.0)
        s = a.std()
        if s > 1e-10:
            Z.append((a - a.mean()) / s)
        else:
            Z.append(np.zeros_like(a))
    return np.mean(Z, axis=0)


# ---------------------------------------------------------------------------
# Window scheduling
# ---------------------------------------------------------------------------

def build_windows(years: np.ndarray, min_train: int, min_test: int):
    """Choose split years T0 such that train (year < T0) has >= min_train
    sequences and test (year >= T0) has >= min_test sequences. Steps every
    integer year between (year_min+1) and (year_max-1)."""
    counts = pd.Series(years).value_counts().sort_index()
    cum = counts.cumsum()
    total = counts.sum()
    splits = []
    for T0 in sorted(np.unique(years)):
        n_train = int(cum.get(T0 - 1, 0))
        n_test = int(total - n_train)
        if n_train >= min_train and n_test >= min_test and T0 > years.min():
            splits.append((int(T0), n_train, n_test))
    return splits


# ---------------------------------------------------------------------------
# Main loop
# ---------------------------------------------------------------------------

def evaluate_pathogen(pathogen: str, df: pd.DataFrame, L: int) -> list[dict]:
    years = df["year"].values
    yr_min, yr_max = int(years.min()), int(years.max())
    splits = build_windows(years, MIN_TRAIN, MIN_TEST)
    rows = []
    print(f"\n[{pathogen}] L={L} year_range={yr_min}-{yr_max} "
          f"n_seq={len(df)} n_splits={len(splits)}")
    for T0, n_train, n_test in splits:
        train = df[df["year"] < T0]["aa"].tolist()
        test = df[df["year"] >= T0]["aa"].tolist()
        f_tr, e_tr, _ = compute_freq_entropy(train)
        f_te, e_te, _ = compute_freq_entropy(test)
        # Emergent ground truth: freq < low in train AND freq >= high in test
        y_emerge = compute_emergent_positions(train, test, f_tr, f_te,
                                              EMERGENCE_LOW, EMERGENCE_HIGH)
        if y_emerge.sum() == 0:
            print(f"  T0={T0}: 0 emergent positions, skip")
            continue
        # Scores from training window only (prospective):
        #  - freq_train: directly the train mutation frequency
        #  - entropy_train: training entropy
        #  - 2feat (freq+entropy z-uniform mean)
        score_freq = f_tr
        score_ent = e_tr
        score_2 = zscore_uniform(f_tr, e_tr)
        # Top-K threshold for MCC/F1
        for name, sc in (("freq", score_freq), ("entropy", score_ent),
                         ("freq+entropy", score_2)):
            pred = topk_threshold(sc, TOP_K)
            mcc = safe_mcc(y_emerge, pred)
            f1 = safe_f1(y_emerge, pred)
            auroc = safe_auroc(y_emerge, sc)
            fold, fisher_p = topk_enrichment(sc, y_emerge, TOP_K)
            rows.append({
                "pathogen": pathogen,
                "split_year": T0,
                "n_train": n_train,
                "n_test": n_test,
                "n_emergent": int(y_emerge.sum()),
                "n_positions": L,
                "score": name,
                "top_k": TOP_K,
                "mcc": round(mcc, 4) if np.isfinite(mcc) else float("nan"),
                "f1": round(f1, 4) if np.isfinite(f1) else float("nan"),
                "auroc": round(auroc, 4) if np.isfinite(auroc) else float("nan"),
                "topk_enrichment_fold": round(fold, 3) if np.isfinite(fold) else float("nan"),
                "topk_fisher_p_one_sided": round(fisher_p, 4) if np.isfinite(fisher_p) else float("nan"),
            })
        print(f"  T0={T0}: train={n_train} test={n_test} emerge={int(y_emerge.sum())} "
              f"MCC[freq+ent]={[r['mcc'] for r in rows if r['split_year']==T0 and r['score']=='freq+entropy'][0]:.3f}")
    return rows


def main():
    print("MutBench Sliding-Window Prospective Backtest (Tier C2)")
    print("=" * 70)
    all_rows = []
    coverage = []
    for pathogen, fp in PATHOGEN_FASTA.items():
        if not os.path.exists(fp):
            print(f"[{pathogen}] file missing: {fp}")
            coverage.append({"pathogen": pathogen, "status": "MISSING_FASTA"})
            continue
        df, L = load_pathogen(pathogen, fp)
        if df is None or len(df) < (MIN_TRAIN + MIN_TEST):
            print(f"[{pathogen}] insufficient year-tagged seqs (n={0 if df is None else len(df)})")
            coverage.append({"pathogen": pathogen, "status": "INSUFFICIENT_YEAR_DATA",
                             "n_year_tagged": 0 if df is None else len(df)})
            continue
        coverage.append({
            "pathogen": pathogen, "status": "ok",
            "n_year_tagged": len(df),
            "n_positions": L,
            "year_min": int(df["year"].min()), "year_max": int(df["year"].max()),
        })
        rows = evaluate_pathogen(pathogen, df, L)
        all_rows.extend(rows)

    cov_df = pd.DataFrame(coverage)
    cov_df.to_csv(OUT_DIR / "sliding_window_prospective_coverage.csv", index=False)
    print(f"\nCoverage: {len(cov_df)} pathogens; ok={(cov_df['status']=='ok').sum()}")
    if not all_rows:
        print("No valid windows produced.")
        return
    df = pd.DataFrame(all_rows)
    df.to_csv(OUT_DIR / "sliding_window_prospective_backtest.csv", index=False)
    print(f"Wrote {len(df)} rows to sliding_window_prospective_backtest.csv")

    # Per-pathogen summary on freq+entropy
    fe = df[df["score"] == "freq+entropy"].copy()
    summary = (fe.groupby("pathogen")
                  .agg(n_windows=("split_year", "count"),
                       year_min=("split_year", "min"),
                       year_max=("split_year", "max"),
                       mean_mcc=("mcc", "mean"),
                       median_mcc=("mcc", "median"),
                       mean_f1=("f1", "mean"),
                       mean_auroc=("auroc", "mean"),
                       mean_enrichment=("topk_enrichment_fold", "mean"))
                  .reset_index())
    # Concept-drift slope: linear regression of MCC over window index (per pathogen)
    slopes = []
    for p, g in fe.groupby("pathogen"):
        g = g.dropna(subset=["mcc"]).sort_values("split_year")
        if len(g) >= 3:
            x = g["split_year"].values.astype(float)
            y = g["mcc"].values.astype(float)
            slope = float(np.polyfit(x, y, 1)[0])
            slopes.append({"pathogen": p, "trend_slope_mcc_per_year": round(slope, 4)})
        else:
            slopes.append({"pathogen": p, "trend_slope_mcc_per_year": float("nan")})
    sl_df = pd.DataFrame(slopes)
    summary = summary.merge(sl_df, on="pathogen", how="left")
    summary.to_csv(OUT_DIR / "sliding_window_prospective_backtest_summary.csv",
                   index=False)
    print("\nSummary (freq+entropy 2-feature core):")
    print(summary.to_string(index=False))

    # Plot MCC over time per pathogen
    try:
        import matplotlib
        matplotlib.use("Agg")
        import matplotlib.pyplot as plt
        n = fe["pathogen"].nunique()
        ncol = 3
        nrow = int(np.ceil(n / ncol))
        fig, axes = plt.subplots(nrow, ncol, figsize=(4.2 * ncol, 2.6 * nrow),
                                 sharex=False, sharey=False)
        axes = np.array(axes).reshape(-1)
        for ax, (p, g) in zip(axes, fe.groupby("pathogen")):
            g = g.sort_values("split_year")
            ax.plot(g["split_year"], g["mcc"], "o-", color="C0", label="freq+entropy")
            sub_freq = df[(df["pathogen"] == p) & (df["score"] == "freq")].sort_values("split_year")
            ax.plot(sub_freq["split_year"], sub_freq["mcc"], "x--", color="C1",
                    label="freq", alpha=0.6)
            ax.axhline(0, color="grey", lw=0.5)
            ax.set_title(p, fontsize=10)
            ax.set_ylim(-0.2, 1.0)
            ax.tick_params(labelsize=8)
            ax.set_xlabel("Split year T0", fontsize=8)
            ax.set_ylabel("MCC (top-30)", fontsize=8)
        # Hide unused axes
        for j in range(n, len(axes)):
            axes[j].set_visible(False)
        # Single legend
        axes[0].legend(loc="upper left", fontsize=8)
        fig.suptitle("Sliding-window prospective backtest: per-pathogen MCC vs split year",
                     fontsize=11)
        fig.tight_layout(rect=[0, 0, 1, 0.96])
        out_png = FIG_DIR / "sliding_window_prospective_backtest.png"
        fig.savefig(out_png, dpi=150)
        print(f"Wrote {out_png}")
    except Exception as e:
        print(f"Plotting failed: {e}")


if __name__ == "__main__":
    main()
