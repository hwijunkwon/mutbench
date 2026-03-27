#!/usr/bin/env python3
"""Compute per-position mean Grantham distance for 9 pathogens.

For each position in the MSA, compute the mean Grantham distance between
the consensus amino acid and all observed variant amino acids, weighted
by their frequencies. Higher values = more radical substitutions.

Grantham R (1974) Science 185:862-864.
"""

import os
import sys
import numpy as np
import pandas as pd
from collections import Counter

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

# Grantham distance matrix (selected pairs)
# Full 20x20 matrix from Grantham 1974
GRANTHAM = {
    ('A','R'):112,('A','N'):111,('A','D'):126,('A','C'):195,('A','Q'):91,('A','E'):107,
    ('A','G'):60,('A','H'):86,('A','I'):94,('A','L'):96,('A','K'):106,('A','M'):84,
    ('A','F'):113,('A','P'):27,('A','S'):99,('A','T'):58,('A','W'):148,('A','Y'):112,('A','V'):64,
    ('R','N'):86,('R','D'):96,('R','C'):180,('R','Q'):43,('R','E'):54,('R','G'):125,
    ('R','H'):29,('R','I'):97,('R','L'):102,('R','K'):26,('R','M'):91,('R','F'):97,
    ('R','P'):103,('R','S'):110,('R','T'):71,('R','W'):101,('R','Y'):77,('R','V'):96,
    ('N','D'):23,('N','C'):139,('N','Q'):46,('N','E'):42,('N','G'):80,('N','H'):68,
    ('N','I'):149,('N','L'):153,('N','K'):94,('N','M'):142,('N','F'):158,('N','P'):91,
    ('N','S'):46,('N','T'):65,('N','W'):174,('N','Y'):143,('N','V'):133,
    ('D','C'):154,('D','Q'):61,('D','E'):45,('D','G'):94,('D','H'):81,('D','I'):168,
    ('D','L'):172,('D','K'):101,('D','M'):160,('D','F'):177,('D','P'):108,('D','S'):65,
    ('D','T'):85,('D','W'):181,('D','Y'):160,('D','V'):152,
    ('C','Q'):154,('C','E'):170,('C','G'):159,('C','H'):174,('C','I'):198,('C','L'):198,
    ('C','K'):202,('C','M'):196,('C','F'):205,('C','P'):169,('C','S'):112,('C','T'):149,
    ('C','W'):215,('C','Y'):194,('C','V'):192,
    ('Q','E'):29,('Q','G'):87,('Q','H'):24,('Q','I'):109,('Q','L'):113,('Q','K'):53,
    ('Q','M'):101,('Q','F'):116,('Q','P'):76,('Q','S'):68,('Q','T'):42,('Q','W'):130,
    ('Q','Y'):99,('Q','V'):96,
    ('E','G'):98,('E','H'):40,('E','I'):134,('E','L'):138,('E','K'):56,('E','M'):126,
    ('E','F'):140,('E','P'):93,('E','S'):80,('E','T'):65,('E','W'):152,('E','Y'):122,('E','V'):121,
    ('G','H'):98,('G','I'):135,('G','L'):138,('G','K'):127,('G','M'):127,('G','F'):153,
    ('G','P'):42,('G','S'):56,('G','T'):59,('G','W'):184,('G','Y'):147,('G','V'):109,
    ('H','I'):94,('H','L'):99,('H','K'):32,('H','M'):87,('H','F'):100,('H','P'):77,
    ('H','S'):89,('H','T'):47,('H','W'):115,('H','Y'):83,('H','V'):84,
    ('I','L'):5,('I','K'):102,('I','M'):10,('I','F'):21,('I','P'):95,('I','S'):142,
    ('I','T'):89,('I','W'):61,('I','Y'):33,('I','V'):29,
    ('L','K'):107,('L','M'):15,('L','F'):22,('L','P'):98,('L','S'):145,('L','T'):92,
    ('L','W'):61,('L','Y'):36,('L','V'):32,
    ('K','M'):95,('K','F'):102,('K','P'):103,('K','S'):121,('K','T'):78,('K','W'):110,
    ('K','Y'):85,('K','V'):97,
    ('M','F'):28,('M','P'):87,('M','S'):135,('M','T'):81,('M','W'):67,('M','Y'):36,('M','V'):21,
    ('F','P'):114,('F','S'):155,('F','T'):103,('F','W'):40,('F','Y'):22,('F','V'):50,
    ('P','S'):74,('P','T'):38,('P','W'):147,('P','Y'):110,('P','V'):68,
    ('S','T'):58,('S','W'):177,('S','Y'):144,('S','V'):124,
    ('T','W'):128,('T','Y'):92,('T','V'):69,
    ('W','Y'):37,('W','V'):88,
    ('Y','V'):55,
}

def get_grantham(aa1, aa2):
    """Get Grantham distance between two amino acids."""
    if aa1 == aa2:
        return 0
    key = (aa1, aa2)
    if key in GRANTHAM:
        return GRANTHAM[key]
    key = (aa2, aa1)
    if key in GRANTHAM:
        return GRANTHAM[key]
    return np.nan


def parse_msa(fasta_path):
    from Bio import SeqIO
    records = list(SeqIO.parse(fasta_path, "fasta"))
    lengths = [len(r.seq) for r in records]
    modal_len = max(set(lengths), key=lengths.count)
    filtered = [r for r in records if len(r.seq) == modal_len]
    return np.array([list(str(r.seq).upper()) for r in filtered])


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

BASE = os.path.join(os.path.dirname(__file__), "..")
OUT_DIR = os.path.join(BASE, "results/mutbench/feature_analysis")
os.makedirs(OUT_DIR, exist_ok=True)

VALID_AA = set("ACDEFGHIKLMNPQRSTVWY")


def compute_grantham_per_position(msa):
    """Compute mean Grantham distance at each position."""
    n_seqs, seq_len = msa.shape
    grantham_scores = np.zeros(seq_len)

    for pos in range(seq_len):
        col = msa[:, pos]
        counts = Counter(c for c in col if c in VALID_AA)
        if not counts:
            continue

        consensus = max(counts, key=counts.get)
        total = sum(counts.values())

        # Weighted mean Grantham distance from consensus
        weighted_sum = 0.0
        weight_total = 0.0
        for aa, count in counts.items():
            if aa == consensus:
                continue
            g = get_grantham(consensus, aa)
            if not np.isnan(g):
                weighted_sum += g * count
                weight_total += count

        if weight_total > 0:
            grantham_scores[pos] = weighted_sum / weight_total
        # If no variants, score stays 0

    return grantham_scores


def main():
    print("=" * 60)
    print("Computing per-position Grantham distance for 9 pathogens")
    print("=" * 60)

    all_results = []

    for pathogen, fasta_rel in PATHOGENS.items():
        fasta_path = os.path.join(BASE, fasta_rel)
        print(f"\n  {pathogen}: {fasta_rel}")

        msa = parse_msa(fasta_path)
        print(f"    MSA shape: {msa.shape}")

        scores = compute_grantham_per_position(msa)

        # Save
        df = pd.DataFrame({"position": np.arange(len(scores)), "grantham": scores})
        out_path = os.path.join(OUT_DIR, f"{pathogen}_grantham.csv")
        df.to_csv(out_path, index=False)

        nonzero = np.sum(scores > 0)
        print(f"    Mean={scores.mean():.2f}, Max={scores.max():.1f}, "
              f"Nonzero={nonzero}/{len(scores)}")

        all_results.append({
            "pathogen": pathogen,
            "n_positions": len(scores),
            "mean_grantham": round(scores.mean(), 2),
            "max_grantham": round(scores.max(), 1),
            "nonzero_positions": int(nonzero),
        })

    summary = pd.DataFrame(all_results)
    summary.to_csv(os.path.join(OUT_DIR, "grantham_summary.csv"), index=False)
    print(f"\n{summary.to_string(index=False)}")
    print("\nDone!")


if __name__ == "__main__":
    main()
