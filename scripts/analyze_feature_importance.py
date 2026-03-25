#!/usr/bin/env python3
"""Build position-level feature matrices for 9 pathogens and compute per-feature AUC.

Features:
  - freq: mutation frequency at each position
  - entropy: Shannon entropy at each position
  - rare_freq: rare variant frequency (allele freq < 0.01)
  - homoplasy: normalized homoplasy score
  - esm2_llr: ESM-2 log-likelihood ratio
  - plddt: AlphaFold pLDDT score
  - layer_a: binary ground truth (Layer A adaptive sites)

Output:
  - feature_matrix_{pathogen}.csv per pathogen
  - per_feature_auc.csv summary table
"""

import sys
import os
import warnings
warnings.filterwarnings("ignore")

import numpy as np
import pandas as pd
from scipy.stats import spearmanr
from sklearn.metrics import roc_auc_score
from collections import Counter

# Add project root to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from tools.mutbench.ground_truth.multilayer_gt import get_gt_adaptive

# ── Pathogen config ──────────────────────────────────────────────────────
PATHOGENS = {
    "SARS-CoV-2": {
        "fasta": "data/ncbi_temporal/spike_500_subsample.fasta",
        "homoplasy": "results/mutbench/homoplasy_scores/SARS-CoV-2_homoplasy.csv",
        "esm": "results/mutbench/esm_scores/SARS-CoV-2_esm_llr.npy",
        "plddt": "results/mutbench/structural_features/sars2_plddt.csv",
    },
    "H3N2": {
        "fasta": "data/influenza/h3n2_ha_sequences.fasta",
        "homoplasy": "results/mutbench/homoplasy_scores/H3N2_homoplasy.csv",
        "esm": "results/mutbench/esm_scores/H3N2_esm_llr.npy",
        "plddt": "results/mutbench/structural_features/influenza_h3n2_plddt.csv",
    },
    "Norovirus": {
        "fasta": "data/norovirus/norovirus_vp1_sequences.fasta",
        "homoplasy": "results/mutbench/homoplasy_scores/Norovirus_homoplasy.csv",
        "esm": "results/mutbench/esm_scores/Norovirus_esm_llr.npy",
        "plddt": "results/mutbench/structural_features/norovirus_plddt.csv",
    },
    "HIV-1": {
        "fasta": "data/hiv/hiv1_gp120_sequences.fasta",
        "homoplasy": "results/mutbench/homoplasy_scores/HIV-1_homoplasy.csv",
        "esm": "results/mutbench/esm_scores/HIV-1_esm_llr.npy",
        "plddt": "results/mutbench/structural_features/hiv_plddt.csv",
    },
    "Dengue": {
        "fasta": "data/dengue/dengue_e_sequences.fasta",
        "homoplasy": "results/mutbench/homoplasy_scores/Dengue_homoplasy.csv",
        "esm": "results/mutbench/esm_scores/Dengue_esm_llr.npy",
        "plddt": "results/mutbench/structural_features/dengue_plddt.csv",
    },
    "RSV": {
        "fasta": "data/rsv/rsv_f_sequences.fasta",
        "homoplasy": "results/mutbench/homoplasy_scores/RSV_homoplasy.csv",
        "esm": "results/mutbench/esm_scores/RSV_esm_llr.npy",
        "plddt": "results/mutbench/structural_features/rsv_plddt.csv",
    },
    "Influenza_B": {
        "fasta": "data/influenza/influenza_b_ha_sequences.fasta",
        "homoplasy": "results/mutbench/homoplasy_scores/Influenza_B_homoplasy.csv",
        "esm": "results/mutbench/esm_scores/Influenza_B_esm_llr.npy",
        "plddt": "results/mutbench/structural_features/influenza_b_plddt.csv",
    },
    "MERS": {
        "fasta": "data/mers/mers_spike_sequences.fasta",
        "homoplasy": "results/mutbench/homoplasy_scores/MERS_homoplasy.csv",
        "esm": "results/mutbench/esm_scores/MERS_esm_llr.npy",
        "plddt": "results/mutbench/structural_features/mers_plddt.csv",
    },
    "HCV": {
        "fasta": "data/hcv/hcv_e2_sequences.fasta",
        "homoplasy": "results/mutbench/homoplasy_scores/HCV_homoplasy.csv",
        "esm": "results/mutbench/esm_scores/HCV_esm_llr.npy",
        "plddt": "results/mutbench/structural_features/hcv_plddt.csv",
    },
}

BASE = os.path.join(os.path.dirname(__file__), "..")
OUT_DIR = os.path.join(BASE, "results/mutbench/feature_analysis")
os.makedirs(OUT_DIR, exist_ok=True)


def parse_msa(fasta_path: str) -> np.ndarray:
    """Parse FASTA into 2D character array (n_seqs x seq_len).

    If sequences have different lengths, keep only those matching the modal
    length (the most common length). This gives a de-facto aligned matrix
    for datasets where the majority of sequences share a reference length.
    """
    from Bio import SeqIO
    records = list(SeqIO.parse(fasta_path, "fasta"))
    lengths = [len(r.seq) for r in records]
    modal_len = max(set(lengths), key=lengths.count)
    filtered = [r for r in records if len(r.seq) == modal_len]
    n_dropped = len(records) - len(filtered)
    if n_dropped > 0:
        print(f"    Kept {len(filtered)}/{len(records)} seqs with modal length {modal_len} "
              f"(dropped {n_dropped})")
    return np.array([list(str(r.seq).upper()) for r in filtered])


def compute_freq_entropy(msa: np.ndarray):
    """Compute per-position mutation frequency, Shannon entropy, and rare freq."""
    n_seqs, seq_len = msa.shape
    freq = np.zeros(seq_len)
    entropy = np.zeros(seq_len)
    rare_freq = np.zeros(seq_len)

    # Determine consensus (most frequent AA at each position)
    for pos in range(seq_len):
        col = msa[:, pos]
        counts = Counter(col)
        # Remove gaps from consideration
        total = sum(v for k, v in counts.items() if k not in ("-", "X", "."))
        if total == 0:
            continue

        # Consensus = most frequent non-gap character
        non_gap = {k: v for k, v in counts.items() if k not in ("-", "X", ".")}
        if not non_gap:
            continue
        consensus_aa = max(non_gap, key=non_gap.get)

        # Mutation frequency = 1 - consensus_freq
        consensus_freq = non_gap[consensus_aa] / total
        freq[pos] = 1.0 - consensus_freq

        # Shannon entropy
        probs = np.array([v / total for v in non_gap.values()])
        probs = probs[probs > 0]
        entropy[pos] = -np.sum(probs * np.log2(probs))

        # Rare variant frequency: sum of alleles with freq < 0.01
        rare_sum = sum(v / total for v in non_gap.values() if v / total < 0.01)
        rare_freq[pos] = rare_sum

    return freq, entropy, rare_freq


def load_homoplasy(path: str) -> np.ndarray:
    """Load homoplasy normalized_score. Returns array indexed by position (0-based)."""
    df = pd.read_csv(path)
    max_pos = df["position"].max() + 1
    arr = np.zeros(max_pos)
    arr[df["position"].values] = df["normalized_score"].values
    return arr


def load_plddt(path: str) -> np.ndarray:
    """Load pLDDT. Position column is 1-based in the CSV."""
    df = pd.read_csv(path)
    # Determine if 0-based or 1-based
    min_pos = df["position"].min()
    if min_pos >= 1:
        positions = df["position"].values - 1  # convert to 0-based
    else:
        positions = df["position"].values
    max_pos = positions.max() + 1
    arr = np.full(max_pos, np.nan)
    arr[positions] = df["pLDDT"].values
    return arr


def load_esm(path: str) -> np.ndarray:
    """Load ESM-2 LLR scores."""
    return np.load(path)


def build_feature_matrix(pathogen: str, cfg: dict) -> pd.DataFrame:
    """Build feature matrix for one pathogen."""
    fasta_path = os.path.join(BASE, cfg["fasta"])

    # Compute freq, entropy, rare_freq from MSA
    print(f"  Parsing MSA: {cfg['fasta']}")
    msa = parse_msa(fasta_path)
    seq_len = msa.shape[1]
    freq, entropy, rare_freq = compute_freq_entropy(msa)

    # Determine minimum length across all features
    lengths = {"msa": seq_len}

    # Load homoplasy
    homoplasy = None
    hom_path = os.path.join(BASE, cfg["homoplasy"])
    if os.path.exists(hom_path):
        homoplasy = load_homoplasy(hom_path)
        lengths["homoplasy"] = len(homoplasy)
    else:
        print(f"  WARNING: homoplasy not found: {hom_path}")

    # Load ESM
    esm = None
    esm_path = os.path.join(BASE, cfg["esm"])
    if os.path.exists(esm_path):
        esm = load_esm(esm_path)
        lengths["esm"] = len(esm)
    else:
        print(f"  WARNING: ESM not found: {esm_path}")

    # Load pLDDT
    plddt = None
    plddt_path = os.path.join(BASE, cfg["plddt"])
    if os.path.exists(plddt_path):
        plddt = load_plddt(plddt_path)
        lengths["plddt"] = len(plddt)
    else:
        print(f"  WARNING: pLDDT not found: {plddt_path}")

    min_len = min(lengths.values())
    print(f"  Lengths: {lengths} -> using min_len={min_len}")

    # Get Layer A ground truth
    layer_a_set = get_gt_adaptive(pathogen, min_len)
    layer_a = np.zeros(min_len, dtype=int)
    for p in layer_a_set:
        if p < min_len:
            layer_a[p] = 1

    # Build DataFrame
    df = pd.DataFrame({
        "position": np.arange(min_len),
        "freq": freq[:min_len],
        "entropy": entropy[:min_len],
        "rare_freq": rare_freq[:min_len],
    })

    if homoplasy is not None:
        df["homoplasy"] = homoplasy[:min_len]
    if esm is not None:
        df["esm2_llr"] = esm[:min_len]
    if plddt is not None:
        df["plddt"] = plddt[:min_len]

    df["layer_a"] = layer_a

    return df


def compute_auc_stats(df: pd.DataFrame, pathogen: str) -> list[dict]:
    """Compute per-feature AUC and Spearman rho against layer_a."""
    features = [c for c in df.columns if c not in ("position", "layer_a")]
    y = df["layer_a"].values
    n_pos = int(y.sum())

    if n_pos == 0 or n_pos == len(y):
        print(f"  WARNING: {pathogen} has {n_pos} Layer A sites out of {len(y)} — skipping AUC")
        return []

    results = []
    for feat in features:
        x = df[feat].values
        # Handle NaN
        mask = ~np.isnan(x)
        x_clean = x[mask]
        y_clean = y[mask]

        if len(np.unique(y_clean)) < 2:
            continue

        try:
            auc = roc_auc_score(y_clean, x_clean)
        except ValueError:
            auc = np.nan

        rho, p_val = spearmanr(x_clean, y_clean)

        results.append({
            "pathogen": pathogen,
            "feature": feat,
            "auc": round(auc, 4),
            "spearman_rho": round(rho, 4),
            "p_value": round(p_val, 6) if p_val is not None else np.nan,
            "n_positions": len(y_clean),
            "n_layer_a": int(y_clean.sum()),
        })

    return results


def main():
    all_auc_results = []

    for pathogen, cfg in PATHOGENS.items():
        print(f"\n{'='*60}")
        print(f"Processing: {pathogen}")
        print(f"{'='*60}")

        df = build_feature_matrix(pathogen, cfg)

        # Save feature matrix
        out_path = os.path.join(OUT_DIR, f"feature_matrix_{pathogen}.csv")
        df.to_csv(out_path, index=False)
        print(f"  Saved: {out_path} ({len(df)} positions, {int(df['layer_a'].sum())} Layer A)")

        # Compute AUC
        auc_results = compute_auc_stats(df, pathogen)
        all_auc_results.extend(auc_results)

    # Save summary
    auc_df = pd.DataFrame(all_auc_results)
    auc_path = os.path.join(OUT_DIR, "per_feature_auc.csv")
    auc_df.to_csv(auc_path, index=False)
    print(f"\nSaved AUC summary: {auc_path}")

    # Print summary table
    print("\n" + "=" * 80)
    print("PER-FEATURE AUC SUMMARY (ROC AUC against Layer A)")
    print("=" * 80)

    pivot = auc_df.pivot_table(index="pathogen", columns="feature", values="auc")
    # Reorder features
    feat_order = ["freq", "entropy", "rare_freq", "homoplasy", "esm2_llr", "plddt"]
    feat_order = [f for f in feat_order if f in pivot.columns]
    pivot = pivot[feat_order]
    print(pivot.to_string(float_format=lambda x: f"{x:.3f}"))

    print("\n" + "=" * 80)
    print("SPEARMAN CORRELATION SUMMARY")
    print("=" * 80)
    pivot_rho = auc_df.pivot_table(index="pathogen", columns="feature", values="spearman_rho")
    pivot_rho = pivot_rho[[f for f in feat_order if f in pivot_rho.columns]]
    print(pivot_rho.to_string(float_format=lambda x: f"{x:.3f}"))

    # Cross-pathogen variance
    print("\n" + "=" * 80)
    print("CROSS-PATHOGEN AUC VARIANCE (higher = more pathogen-dependent)")
    print("=" * 80)
    for feat in feat_order:
        if feat in pivot.columns:
            vals = pivot[feat].dropna()
            print(f"  {feat:12s}: mean={vals.mean():.3f}, std={vals.std():.3f}, "
                  f"range=[{vals.min():.3f}, {vals.max():.3f}]")


if __name__ == "__main__":
    main()
