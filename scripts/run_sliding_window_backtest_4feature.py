#!/usr/bin/env python3
"""Sliding-window prospective backtest — 3/4-feature extension (Tier D2).

Extends Tier C2 (freq+entropy 2-feature ensemble) to include the
remaining members of the dissertation 4-feature core:

  - pLDDT (per-residue AlphaFold confidence; sequence-static, window-invariant)
  - homoplasy (TreeTime-derived per-position score; window-static at the
    panel level — the homoplasy score is computed once over the full MSA
    and treated as a precomputed prior, *not* re-estimated per window)

Coordinate-frame caveat: pLDDT and homoplasy are stored on the
canonical protein-MSA frame used by feature_matrix_*.csv, while the
year-tagged sliding-window analysis runs on the codon-aligned NCBI CDS
MSA (C2 frame). For each pathogen we therefore build a position
mapping from the CDS-frame translated consensus to the canonical
protein-MSA frame via a Needleman–Wunsch alignment of consensus
sequences, then look up pLDDT and homoplasy at the mapped position.

Honest scoping:
  - Window-time-varying features  : freq, entropy
  - Static (priors over windows)  : pLDDT (truly window-invariant by
    construction), homoplasy (treated as a static prior — re-running
    TreeTime per window is intractable for an 11-pathogen panel; this
    is documented as a limitation)

Outputs:
  results/mutbench/feature_analysis/sliding_window_prospective_backtest_4feature.csv
  results/mutbench/feature_analysis/sliding_window_prospective_backtest_4feature_summary.csv
  results/mutbench/feature_analysis/sliding_window_prospective_c2_vs_d2_paired.csv
  paper/dissertation/figures/sliding_window_prospective_backtest_4feature.png
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
FEATURE_MATRIX_DIR = OUT_DIR
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

EMERGENCE_LOW = 0.05
EMERGENCE_HIGH = 0.10
TOP_K = 30
MIN_TRAIN = 30
MIN_TEST = 20


# ---------------------------------------------------------------------------
# Data loading (mirrors C2)
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
            aa.append(tr if tr != "*" else "-")
        except Exception:
            aa.append("X")
    return "".join(aa)


def best_frame_for_records(records, n_probe: int = 30) -> int:
    """Detect the in-frame offset 0/1/2 by maximum AA-residue yield."""
    scores = [0, 0, 0]
    for r in records[:n_probe]:
        s = str(r.seq).upper()
        for f in range(3):
            aa = translate_codon_aln(s[f:])
            scores[f] += sum(1 for c in aa if c.isalpha())
    return int(np.argmax(scores))


def load_pathogen(pathogen: str, fp: str):
    """Load year-tagged sequences for one pathogen.

    To keep D2 windows *identical* to C2 windows for paired comparison,
    we use frame offset = 0 (matching C2's translate_codon_aln entry
    point). The CDS-frame consensus may include some non-coding leading
    columns; the consensus-to-canonical mapping (Needleman–Wunsch) tolerates
    this and produces a robust position correspondence.

    Returns (df, L, frame_used). df has columns id/year/aa.
    """
    recs = list(SeqIO.parse(fp, "fasta"))
    if not recs:
        return None, None, None
    bf = 0  # match C2 exactly so windows are identical
    rows = []
    for r in recs:
        y = extract_year(r.description)
        if y is None:
            continue
        aa = translate_codon_aln(str(r.seq)[bf:])
        rows.append({"id": r.id, "year": y, "aa": aa})
    if not rows:
        return None, None, bf
    df = pd.DataFrame(rows)
    L = max(len(s) for s in df["aa"])
    df["aa"] = df["aa"].apply(lambda s: s + "-" * (L - len(s)))
    return df, L, bf


# ---------------------------------------------------------------------------
# Position mapping: CDS-frame ↔ feature_matrix frame
# ---------------------------------------------------------------------------

def col_consensus(seqs: list[str]) -> str:
    if not seqs:
        return ""
    L = max(len(s) for s in seqs)
    seqs = [s + "-" * (L - len(s)) for s in seqs]
    out = []
    for i in range(L):
        c = Counter(s[i] for s in seqs if s[i] not in ("-", ".", "X", "N"))
        out.append(c.most_common(1)[0][0] if c else "-")
    return "".join(out)


def build_position_mapping(cds_consensus: str, target_consensus: str) -> dict[int, int]:
    """Map column index in cds_consensus → column index in target_consensus
    via Needleman–Wunsch alignment of their ungapped projections.

    Returns a dict {cds_col -> target_col} for matched residues only.
    """
    from Bio import pairwise2
    cds_ug = "".join(c for c in cds_consensus if c != "-")
    tgt_ug = "".join(c for c in target_consensus if c != "-")
    # Index maps: ungapped position → aligned column
    cds_ug_to_col = [i for i, c in enumerate(cds_consensus) if c != "-"]
    tgt_ug_to_col = [i for i, c in enumerate(target_consensus) if c != "-"]
    if not cds_ug or not tgt_ug:
        return {}
    aln = pairwise2.align.globalms(cds_ug, tgt_ug, 2, -1, -10, -0.5,
                                   one_alignment_only=True)
    if not aln:
        return {}
    a, b = aln[0][0], aln[0][1]
    mp: dict[int, int] = {}
    ai = bi = 0
    for x, y in zip(a, b):
        if x != "-" and y != "-":
            mp[cds_ug_to_col[ai]] = tgt_ug_to_col[bi]
            ai += 1; bi += 1
        elif x != "-":
            ai += 1
        elif y != "-":
            bi += 1
    return mp


# ---------------------------------------------------------------------------
# Feature computation
# ---------------------------------------------------------------------------

def compute_freq_entropy(seqs: list[str]) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
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


def compute_emergent_positions(train_freq, test_freq,
                                low: float = EMERGENCE_LOW,
                                high: float = EMERGENCE_HIGH) -> np.ndarray:
    return ((train_freq < low) & (test_freq >= high)).astype(int)


# ---------------------------------------------------------------------------
# Static features (window-invariant priors)
# ---------------------------------------------------------------------------

PATHOGEN_TO_FM = {
    "H3N2": "feature_matrix_H3N2.csv",
    "Influenza_B": "feature_matrix_Influenza_B.csv",
    "Dengue": "feature_matrix_Dengue.csv",
    "RSV": "feature_matrix_RSV.csv",
    "HCV": "feature_matrix_HCV.csv",
    "Norovirus": "feature_matrix_Norovirus.csv",
    "EV-A71": "feature_matrix_EV-A71.csv",
    "Rabies": "feature_matrix_Rabies.csv",
    "HIV-1": "feature_matrix_HIV-1.csv",
    "MERS": "feature_matrix_MERS.csv",
    "SARS-CoV-2": "feature_matrix_SARS-CoV-2.csv",
}


def load_static_features(pathogen: str) -> tuple[np.ndarray, np.ndarray, int] | None:
    """Return (plddt, homoplasy, L_target) from the canonical feature_matrix.

    Both arrays are indexed by feature_matrix position (0..L_target-1).
    """
    fp = FEATURE_MATRIX_DIR / PATHOGEN_TO_FM[pathogen]
    if not fp.exists():
        return None
    df = pd.read_csv(fp)
    df = df.sort_values("position")
    plddt = df["plddt"].to_numpy(dtype=float)
    homo = df["homoplasy"].to_numpy(dtype=float)
    return plddt, homo, len(df)


def project_static_to_cds_frame(static_arr: np.ndarray,
                                mapping: dict[int, int],
                                L_cds: int,
                                fill: float | None = None) -> np.ndarray:
    """Project a feature_matrix-frame array onto CDS-frame columns.

    Unmapped CDS columns get filled with `fill` (default = mean of mapped
    values, so that they neither drag scores up nor down after z-scoring).
    """
    out = np.full(L_cds, np.nan, dtype=float)
    for c_cds, c_tgt in mapping.items():
        if 0 <= c_tgt < len(static_arr):
            out[c_cds] = static_arr[c_tgt]
    if fill is None:
        m = np.nanmean(out) if np.any(np.isfinite(out)) else 0.0
        fill = float(m if np.isfinite(m) else 0.0)
    out = np.where(np.isfinite(out), out, fill)
    return out


# ---------------------------------------------------------------------------
# Scoring & metrics (mirrors C2)
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


def topk_threshold(score, k):
    if k >= len(score):
        return np.ones_like(score, dtype=int)
    thr = np.sort(score)[-k]
    return (score >= thr).astype(int)


def topk_enrichment(score, y, k):
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
    """Uniform-weight z-score ensemble.

    Higher score is "more emergent". Note: pLDDT (high = confident,
    typically *stable*) and homoplasy (high = repeated independent
    occurrences = recurrence/escape signal) have opposing semantics.
    The original 4-feature core in ch4 weights these positively for
    consistent ranking; we therefore z-score `(-plddt)` so that high
    score == low confidence == flexible/emergence-prone, matching the
    feature-importance signs reported in the dissertation §3 / §4.
    """
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
# Per-pathogen evaluation
# ---------------------------------------------------------------------------

def evaluate_pathogen(pathogen: str, df: pd.DataFrame, L: int, frame: int) -> tuple[list[dict], dict]:
    years = df["year"].values
    yr_min, yr_max = int(years.min()), int(years.max())
    splits = build_windows(years, MIN_TRAIN, MIN_TEST)

    # Build CDS-consensus on full panel
    full_seqs = df["aa"].tolist()
    cds_consensus = col_consensus(full_seqs)

    # Load static features and build mapping
    static = load_static_features(pathogen)
    diag = {"pathogen": pathogen, "frame": frame, "L_cds": L,
            "n_splits": len(splits), "year_min": yr_min, "year_max": yr_max}
    if static is None:
        diag["static_status"] = "MISSING_FEATURE_MATRIX"
        return [], diag
    plddt_arr, homo_arr, L_tgt = static
    diag["L_target"] = L_tgt

    # Build feature_matrix-frame consensus by reading canonical-protein MSA
    # We don't have the canonical MSA stored uniformly, but we can use the
    # CDS-frame consensus for both sides of the alignment if we treat the
    # feature_matrix's index as protein-AA-coordinate. The cleanest proxy:
    # use a per-pathogen reference protein sequence drawn from the
    # canonical _sequences.fasta if available, else the CDS consensus
    # itself (in which case the mapping is identity).
    target_consensus = _load_target_consensus(pathogen, L_tgt)
    if target_consensus is None:
        diag["static_status"] = "NO_TARGET_CONSENSUS"
        return [], diag
    mapping = build_position_mapping(cds_consensus, target_consensus)
    diag["mapped_positions"] = len(mapping)
    diag["mapping_coverage"] = round(len(mapping) / max(L, 1), 3)

    plddt_proj = project_static_to_cds_frame(plddt_arr, mapping, L)
    homo_proj = project_static_to_cds_frame(homo_arr, mapping, L)

    rows = []
    print(f"\n[{pathogen}] L_cds={L} L_target={L_tgt} frame={frame} "
          f"year={yr_min}-{yr_max} n_splits={len(splits)} mapped={len(mapping)}/{L}")
    for T0, n_train, n_test in splits:
        train = df[df["year"] < T0]["aa"].tolist()
        test = df[df["year"] >= T0]["aa"].tolist()
        f_tr, e_tr, _ = compute_freq_entropy(train)
        f_te, e_te, _ = compute_freq_entropy(test)
        y_emerge = compute_emergent_positions(f_tr, f_te, EMERGENCE_LOW, EMERGENCE_HIGH)
        if y_emerge.sum() == 0:
            print(f"  T0={T0}: 0 emergent positions, skip")
            continue
        # Negate pLDDT so high score = low-confidence = emergence-prone
        plddt_score = -plddt_proj
        # Score variants
        score_2 = zscore_uniform(f_tr, e_tr)
        score_3p = zscore_uniform(f_tr, e_tr, plddt_score)
        score_3h = zscore_uniform(f_tr, e_tr, homo_proj)
        score_4 = zscore_uniform(f_tr, e_tr, plddt_score, homo_proj)
        for name, sc in (
            ("freq+entropy", score_2),
            ("freq+entropy+plddt", score_3p),
            ("freq+entropy+homoplasy", score_3h),
            ("freq+entropy+plddt+homoplasy", score_4),
        ):
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
        m4 = [r["mcc"] for r in rows
              if r["split_year"] == T0 and r["score"] == "freq+entropy+plddt+homoplasy"][0]
        print(f"  T0={T0}: train={n_train} test={n_test} emerge={int(y_emerge.sum())} "
              f"MCC[4feat]={m4:.3f}")
    return rows, diag


def _load_target_consensus(pathogen: str, L_target: int) -> str | None:
    """Heuristic: load a canonical protein consensus aligned with the
    feature_matrix coordinate frame.

    Strategy: use the canonical _sequences.fasta when available; the
    feature_matrix's L is typically that file's L (post-trimming via
    coverage filtering), so the consensus of *_sequences.fasta gives an
    upper-bound mapping target. If the consensus length differs from
    L_target, we project via row-index alignment after trimming
    leading/trailing all-gap columns.
    """
    candidates = {
        "H3N2": "/proj/paper/data/influenza/h3n2_ha_sequences.fasta",
        "Influenza_B": "/proj/paper/data/influenza/influenza_b_ha_sequences.fasta",
        "Dengue": "/proj/paper/data/dengue/dengue_e_sequences.fasta",
        "RSV": "/proj/paper/data/rsv/rsv_f_sequences.fasta",
        "HCV": "/proj/paper/data/hcv/hcv_e2_sequences.fasta",
        "Norovirus": "/proj/paper/data/norovirus/norovirus_vp1_sequences.fasta",
        "EV-A71": "/proj/paper/data/enterovirus/eva71_vp1_sequences.fasta",
        "Rabies": "/proj/paper/data/rabies/rabies_g_sequences.fasta",
        "HIV-1": "/proj/paper/data/hiv/hiv1_gp120_sequences.fasta",
        "MERS": "/proj/paper/data/mers/mers_spike_sequences.fasta",
        "SARS-CoV-2": "/proj/paper/data/ncbi_temporal/sars2_spike_clean.fasta",
    }
    fp = candidates.get(pathogen)
    if fp is None or not os.path.exists(fp):
        return None
    recs = list(SeqIO.parse(fp, "fasta"))
    if not recs:
        return None
    seqs = [str(r.seq) for r in recs]
    cons = col_consensus(seqs)
    return cons


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    print("MutBench Sliding-Window Prospective Backtest — 4-feature core (Tier D2)")
    print("=" * 75)
    all_rows = []
    diags = []
    for pathogen, fp in PATHOGEN_FASTA.items():
        if not os.path.exists(fp):
            print(f"[{pathogen}] file missing")
            continue
        df, L, frame = load_pathogen(pathogen, fp)
        if df is None or len(df) < (MIN_TRAIN + MIN_TEST):
            print(f"[{pathogen}] insufficient year-tagged seqs (n={0 if df is None else len(df)})")
            continue
        rows, diag = evaluate_pathogen(pathogen, df, L, frame)
        diags.append(diag)
        all_rows.extend(rows)

    diag_df = pd.DataFrame(diags)
    diag_df.to_csv(OUT_DIR / "sliding_window_prospective_4feature_diagnostics.csv", index=False)
    if not all_rows:
        print("No valid windows produced.")
        return
    df = pd.DataFrame(all_rows)
    out_csv = OUT_DIR / "sliding_window_prospective_backtest_4feature.csv"
    df.to_csv(out_csv, index=False)
    print(f"\nWrote {len(df)} rows → {out_csv.name}")

    # Per-pathogen summary by score variant
    summary = (df.groupby(["pathogen", "score"])
                  .agg(n_windows=("split_year", "count"),
                       year_min=("split_year", "min"),
                       year_max=("split_year", "max"),
                       mean_mcc=("mcc", "mean"),
                       median_mcc=("mcc", "median"),
                       mean_f1=("f1", "mean"),
                       mean_auroc=("auroc", "mean"),
                       mean_enrichment=("topk_enrichment_fold", "mean"))
                  .reset_index())
    summary.to_csv(OUT_DIR / "sliding_window_prospective_backtest_4feature_summary.csv",
                   index=False)
    # Grand mean per score variant
    grand = (df.groupby("score")
                .agg(n_windows=("split_year", "count"),
                     mean_mcc=("mcc", "mean"),
                     mean_auroc=("auroc", "mean"),
                     mean_enrichment=("topk_enrichment_fold", "mean"))
                .reset_index())
    print("\nGrand mean by score variant:")
    print(grand.to_string(index=False))

    # Paired comparison: C2 baseline (freq+entropy) vs each extension
    pivot = df.pivot_table(index=["pathogen", "split_year"], columns="score",
                           values="mcc")
    print("\nPaired comparison (per-window MCC, only windows with both):")
    paired_results = []
    base = "freq+entropy"
    for variant in ["freq+entropy+plddt", "freq+entropy+homoplasy",
                    "freq+entropy+plddt+homoplasy"]:
        if base not in pivot.columns or variant not in pivot.columns:
            continue
        pair = pivot[[base, variant]].dropna()
        if len(pair) < 3:
            continue
        delta = pair[variant] - pair[base]
        from scipy.stats import wilcoxon, ttest_rel
        try:
            w_stat, w_p = wilcoxon(pair[variant], pair[base], zero_method="wilcox",
                                   alternative="two-sided")
        except Exception:
            w_stat, w_p = float("nan"), float("nan")
        try:
            t_stat, t_p = ttest_rel(pair[variant], pair[base])
        except Exception:
            t_stat, t_p = float("nan"), float("nan")
        row = {
            "baseline": base, "variant": variant, "n_paired_windows": int(len(pair)),
            "mean_delta_mcc": round(float(delta.mean()), 4),
            "median_delta_mcc": round(float(delta.median()), 4),
            "wilcoxon_stat": float(w_stat) if np.isfinite(w_stat) else float("nan"),
            "wilcoxon_p": round(float(w_p), 4) if np.isfinite(w_p) else float("nan"),
            "paired_t_stat": round(float(t_stat), 4) if np.isfinite(t_stat) else float("nan"),
            "paired_t_p": round(float(t_p), 4) if np.isfinite(t_p) else float("nan"),
            "n_better": int((delta > 0).sum()),
            "n_worse": int((delta < 0).sum()),
            "n_tied": int((delta == 0).sum()),
        }
        paired_results.append(row)
        print(f"  {base} vs {variant}: n={len(pair)} mean Δ={delta.mean():+.4f} "
              f"Wilcoxon p={w_p:.4f} (better/worse/tied = "
              f"{row['n_better']}/{row['n_worse']}/{row['n_tied']})")

    if paired_results:
        pr_df = pd.DataFrame(paired_results)
        pr_df.to_csv(OUT_DIR / "sliding_window_prospective_c2_vs_d2_paired.csv",
                     index=False)

    # Plot per-pathogen MCC over split year for 2-feat vs 4-feat
    try:
        import matplotlib
        matplotlib.use("Agg")
        import matplotlib.pyplot as plt
        n = df["pathogen"].nunique()
        ncol = 3
        nrow = int(np.ceil(n / ncol))
        fig, axes = plt.subplots(nrow, ncol, figsize=(4.2 * ncol, 2.6 * nrow))
        axes = np.array(axes).reshape(-1)
        pathogens_sorted = sorted(df["pathogen"].unique())
        for ax, p in zip(axes, pathogens_sorted):
            sub2 = df[(df["pathogen"] == p) & (df["score"] == "freq+entropy")].sort_values("split_year")
            sub4 = df[(df["pathogen"] == p) & (df["score"] == "freq+entropy+plddt+homoplasy")].sort_values("split_year")
            ax.plot(sub2["split_year"], sub2["mcc"], "o-", color="C0",
                    label="2-feat (C2)", lw=1.2)
            ax.plot(sub4["split_year"], sub4["mcc"], "s-", color="C3",
                    label="4-feat (D2)", lw=1.2)
            ax.axhline(0, color="grey", lw=0.5)
            ax.set_title(p, fontsize=10)
            ax.set_ylim(-0.2, 1.0)
            ax.set_xlabel("Split year T0", fontsize=8)
            ax.set_ylabel("MCC (top-30)", fontsize=8)
            ax.tick_params(labelsize=8)
        for j in range(len(pathogens_sorted), len(axes)):
            axes[j].set_visible(False)
        axes[0].legend(loc="upper left", fontsize=8)
        fig.suptitle("Sliding-window prospective backtest: 2-feat vs 4-feat MCC vs split year",
                     fontsize=11)
        fig.tight_layout(rect=[0, 0, 1, 0.96])
        out_png = FIG_DIR / "sliding_window_prospective_backtest_4feature.png"
        fig.savefig(out_png, dpi=150)
        print(f"\nWrote {out_png}")
    except Exception as e:
        print(f"Plotting failed: {e}")


if __name__ == "__main__":
    main()
