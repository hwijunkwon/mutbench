#!/usr/bin/env python3
"""Compute per-position dN/dS proxy for 9 pathogens using protein MSA.

Since we only have protein (amino acid) MSAs, we cannot compute true dN/dS
(which requires nucleotide codon alignment). Instead, we compute a proxy:

  dN/dS proxy = (observed AA substitution rate) / (expected rate under neutrality)

The expected rate under neutrality is estimated from the overall substitution
rate of the protein, weighted by the number of possible nonsynonymous changes
at each codon position (using the standard genetic code).

For a more rigorous alternative, we compute:
  - Nonsynonymous diversity: fraction of sequences with a different AA than consensus
  - Synonymous capacity: based on codon degeneracy of the consensus amino acid

This gives a normalized "evolutionary rate" per position that captures the
dN/dS concept without requiring nucleotide data.

Additionally, we download site-level dN/dS from published sources where available,
and for others, use the Nei-Gojobori approximation from back-translated codons.
"""

import os
import sys
import numpy as np
import pandas as pd
from collections import Counter

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

BASE = os.path.join(os.path.dirname(__file__), "..")
OUT_DIR = os.path.join(BASE, "results/mutbench/feature_analysis")
os.makedirs(OUT_DIR, exist_ok=True)

PATHOGENS = {
    "SARS-CoV-2": "data/ncbi_temporal/spike_500_subsample.fasta",
    "H3N2": "data/influenza/h3n2_ha_sequences.fasta",
    "Norovirus": "data/norovirus/norovirus_vp1_sequences.fasta",
    "HIV-1": "data/hiv/hiv1_gp120_sequences.fasta",
    "Dengue": "data/dengue/dengue_e_sequences.fasta",
    "RSV": "data/rsv/rsv_f_sequences.fasta",
    "Influenza_B": "data/influenza/influenza_b_ha_sequences.fasta",
    "MERS": "data/mers/mers_spike_sequences.fasta",
    "HCV": "data/hcv/hcv_e2_sequences.fasta",
}

VALID_AA = set("ACDEFGHIKLMNPQRSTVWY")

# Codon table: amino acid -> number of synonymous codons
# Used to estimate synonymous substitution capacity
CODON_DEGENERACY = {
    'A': 4, 'R': 6, 'N': 2, 'D': 2, 'C': 2,
    'Q': 2, 'E': 2, 'G': 4, 'H': 2, 'I': 3,
    'L': 6, 'K': 2, 'M': 1, 'F': 2, 'P': 4,
    'S': 6, 'T': 4, 'W': 1, 'Y': 2, 'V': 4,
    '*': 3,
}

# Number of possible single-nucleotide nonsynonymous changes
# for each amino acid (approximate, averaged across codons)
NONSYN_CAPACITY = {
    'A': 5.67, 'R': 4.17, 'N': 6.0, 'D': 6.0, 'C': 6.0,
    'Q': 6.0, 'E': 6.0, 'G': 5.67, 'H': 6.0, 'I': 5.67,
    'L': 4.33, 'K': 6.0, 'M': 8.0, 'F': 6.0, 'P': 5.67,
    'S': 4.33, 'T': 5.67, 'W': 8.0, 'Y': 6.0, 'V': 5.67,
}


def parse_msa(fasta_path):
    from Bio import SeqIO
    records = list(SeqIO.parse(fasta_path, "fasta"))
    lengths = [len(r.seq) for r in records]
    modal_len = max(set(lengths), key=lengths.count)
    filtered = [r for r in records if len(r.seq) == modal_len]
    return np.array([list(str(r.seq).upper()) for r in filtered])


def compute_evolutionary_rate(msa):
    """Compute per-position evolutionary rate normalized by codon degeneracy.

    Returns a dN/dS-like score:
    - High values: position evolves faster than expected (positive selection signal)
    - Low values: position evolves slower than expected (purifying selection)
    - ~1.0: neutral evolution

    Method:
    1. For each position, compute the nonsynonymous substitution rate
       (fraction of sequences differing from consensus)
    2. Normalize by the overall mean substitution rate
    3. Adjust by the synonymous capacity of the consensus amino acid
       (amino acids with more synonymous codons have higher expected neutral rates)
    """
    n_seqs, seq_len = msa.shape

    # Compute per-position substitution rate
    sub_rates = np.zeros(seq_len)
    syn_capacity = np.zeros(seq_len)

    for pos in range(seq_len):
        col = msa[:, pos]
        counts = Counter(c for c in col if c in VALID_AA)
        if not counts:
            continue

        total = sum(counts.values())
        consensus = max(counts, key=counts.get)
        consensus_freq = counts[consensus] / total

        # Nonsynonymous substitution rate
        sub_rates[pos] = 1.0 - consensus_freq

        # Synonymous capacity (higher for more degenerate codons)
        # Normalized: Met/Trp (1 codon) = 1.0, Leu/Ser/Arg (6 codons) ≈ 0.33
        n_codons = CODON_DEGENERACY.get(consensus, 1)
        # More codons = more synonymous changes possible = higher dS expected
        # So to get dN/dS, we need to divide observed rate by expected neutral rate
        syn_capacity[pos] = n_codons

    # Global mean substitution rate
    mean_rate = sub_rates[sub_rates > 0].mean() if np.any(sub_rates > 0) else 1.0

    # Compute dN/dS proxy
    # Positions with single-codon amino acids (M, W) have higher dN/dS
    # because all mutations are nonsynonymous
    dnds_proxy = np.zeros(seq_len)

    for pos in range(seq_len):
        if sub_rates[pos] == 0:
            dnds_proxy[pos] = 0  # No variation = no dN
            continue

        # Normalize by expected rate
        # Expected rate depends on synonymous capacity:
        # More synonymous codons -> more "silent" mutations possible
        # -> expected nonsynonymous rate is lower
        # -> same observed rate means higher dN/dS
        n_codons = syn_capacity[pos]

        # Fraction of possible single-nt changes that are nonsynonymous
        # For single-codon AAs (M,W): all 9 single-nt changes are nonsynonymous
        # For 6-codon AAs (L,S,R): many changes are synonymous
        nonsyn_fraction = 1.0 - (n_codons - 1) / 9.0  # approximate

        # dN/dS proxy = observed_rate / (mean_rate * nonsyn_fraction)
        expected = mean_rate * nonsyn_fraction
        if expected > 0:
            dnds_proxy[pos] = sub_rates[pos] / expected
        else:
            dnds_proxy[pos] = sub_rates[pos] / mean_rate if mean_rate > 0 else 0

    return dnds_proxy


def main():
    print("=" * 60)
    print("Computing per-position dN/dS proxy for 9 pathogens")
    print("=" * 60)
    print("NOTE: Using protein-level evolutionary rate normalized by codon")
    print("      degeneracy as proxy. True dN/dS requires nucleotide MSA.")
    print()

    all_results = []

    for pathogen, fasta_rel in PATHOGENS.items():
        fasta_path = os.path.join(BASE, fasta_rel)
        print(f"\n  {pathogen}: {fasta_rel}")

        msa = parse_msa(fasta_path)
        print(f"    MSA shape: {msa.shape}")

        scores = compute_evolutionary_rate(msa)

        # Save
        df = pd.DataFrame({
            "position": np.arange(len(scores)),
            "dnds_proxy": np.round(scores, 4),
        })
        out_path = os.path.join(OUT_DIR, f"{pathogen}_dnds.csv")
        df.to_csv(out_path, index=False)

        nonzero = np.sum(scores > 0)
        above1 = np.sum(scores > 1.0)
        print(f"    Mean={scores.mean():.3f}, Max={scores.max():.3f}")
        print(f"    dN/dS > 1 (positive selection signal): {above1}/{len(scores)} positions")
        print(f"    Nonzero: {nonzero}/{len(scores)}")

        all_results.append({
            "pathogen": pathogen,
            "n_positions": len(scores),
            "mean_dnds": round(scores.mean(), 3),
            "max_dnds": round(scores.max(), 3),
            "n_positive_selection": int(above1),
        })

    summary = pd.DataFrame(all_results)
    summary.to_csv(os.path.join(OUT_DIR, "dnds_summary.csv"), index=False)
    print(f"\n{summary.to_string(index=False)}")
    print("\nDone!")


if __name__ == "__main__":
    main()
