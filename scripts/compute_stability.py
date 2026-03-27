#!/usr/bin/env python3
"""Compute per-position structural stability proxy for 12 viral proteins.

Since full physics-based stability predictors (FoldX, RaSP, ThermoMPNN) are
either too slow or require heavy GPU dependencies, we use a BLOSUM62-based
proxy for structural stability:

For each MSA position:
  1. Identify the consensus (wild-type) amino acid
  2. For each observed substitution, look up BLOSUM62(wt, mut)
  3. Compute: stability_score = -mean(BLOSUM62(wt, mut)) weighted by frequency
     - Negative BLOSUM62 scores = rare/radical substitutions = potentially destabilizing
     - We negate so that HIGHER stability_score = MORE destabilizing position

This is conceptually related to ΔΔG prediction: radical substitutions (low BLOSUM62)
tend to be destabilizing, while conservative substitutions (high BLOSUM62) are
typically neutral. The BLOSUM62 matrix captures evolutionary substitution rates
which correlate with structural/functional tolerance.

Additionally, we incorporate per-residue pLDDT from ESMFold structures as a
structural confidence weight. Low-pLDDT regions are disordered/flexible and
mutations there are less likely to cause folding defects.
"""

import os
import sys
import numpy as np
import pandas as pd
from collections import Counter

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

# ── BLOSUM62 matrix ──────────────────────────────────────────────────────
# Standard BLOSUM62 substitution matrix (Henikoff & Henikoff 1992)
_BLOSUM62_STR = """
   A  R  N  D  C  Q  E  G  H  I  L  K  M  F  P  S  T  W  Y  V
A  4 -1 -2 -2  0 -1 -1  0 -2 -1 -1 -1 -1 -2 -1  1  0 -3 -2  0
R -1  5  0 -2 -3  1  0 -2  0 -3 -2  2 -1 -3 -2 -1 -1 -3 -2 -3
N -2  0  6  1 -3  0  0  0  1 -3 -3  0 -2 -3 -2  1  0 -4 -2 -3
D -2 -2  1  6 -3  0  2 -1 -1 -3 -4 -1 -3 -3 -1  0 -1 -4 -3 -3
C  0 -3 -3 -3  9 -3 -4 -3 -3 -1 -1 -3 -1 -2 -3 -1 -1 -2 -2 -1
Q -1  1  0  0 -3  5  2 -2  0 -3 -2  1  0 -3 -1  0 -1 -2 -1 -2
E -1  0  0  2 -4  2  5 -2  0 -3 -3  1 -2 -3 -1  0 -1 -3 -2 -2
G  0 -2  0 -1 -3 -2 -2  6 -2 -4 -4 -2 -3 -3 -2  0 -2 -2 -3 -3
H -2  0  1 -1 -3  0  0 -2  8 -3 -3 -1 -2 -1 -2 -1 -2 -2  2 -3
I -1 -3 -3 -3 -1 -3 -3 -4 -3  4  2 -3  1  0 -3 -2 -1 -3 -1  3
L -1 -2 -3 -4 -1 -2 -3 -4 -3  2  4 -2  2  0 -3 -2 -1 -2 -1  1
K -1  2  0 -1 -3  1  1 -2 -1 -3 -2  5 -1 -3 -1  0 -1 -3 -2 -2
M -1 -1 -2 -3 -1  0 -2 -3 -2  1  2 -1  5  0 -2 -1 -1 -1 -1  1
F -2 -3 -3 -3 -2 -3 -3 -3 -1  0  0 -3  0  6 -4 -2 -2  1  3 -1
P -1 -2 -2 -1 -3 -1 -1 -2 -2 -3 -3 -1 -2 -4  7 -1 -1 -4 -3 -2
S  1 -1  1  0 -1  0  0  0 -1 -2 -2  0 -1 -2 -1  4  1 -3 -2 -2
T  0 -1  0 -1 -1 -1 -1 -2 -2 -1 -1 -1 -1 -2 -1  1  5 -2 -2  0
W -3 -3 -4 -4 -2 -2 -3 -2 -2 -3 -2 -3 -1  1 -4 -3 -2 11  2 -3
Y -2 -2 -2 -3 -2 -1 -2 -3  2 -1 -1 -2 -1  3 -3 -2 -2  2  7 -1
V  0 -3 -3 -3 -1 -2 -2 -3 -3  3  1 -2  1 -1 -2 -2  0 -3 -1  4
"""

def _parse_blosum62():
    """Parse the BLOSUM62 matrix string into a dict."""
    lines = _BLOSUM62_STR.strip().split('\n')
    aas = lines[0].split()
    matrix = {}
    for line in lines[1:]:
        parts = line.split()
        aa1 = parts[0]
        for j, val in enumerate(parts[1:]):
            aa2 = aas[j]
            matrix[(aa1, aa2)] = int(val)
    return matrix

BLOSUM62 = _parse_blosum62()
VALID_AA = set("ACDEFGHIKLMNPQRSTVWY")


def get_blosum62(aa1, aa2):
    """Get BLOSUM62 score between two amino acids."""
    if aa1 == aa2:
        return BLOSUM62.get((aa1, aa2), 0)
    return BLOSUM62.get((aa1, aa2), BLOSUM62.get((aa2, aa1), None))


def parse_msa(fasta_path):
    """Parse MSA FASTA, keeping only sequences of modal length."""
    from Bio import SeqIO
    records = list(SeqIO.parse(fasta_path, "fasta"))
    lengths = [len(r.seq) for r in records]
    modal_len = max(set(lengths), key=lengths.count)
    filtered = [r for r in records if len(r.seq) == modal_len]
    return np.array([list(str(r.seq).upper()) for r in filtered])


def extract_plddt_from_pdb(pdb_path):
    """Extract per-residue pLDDT from ESMFold PDB (stored in B-factor column).

    Returns array of pLDDT values (0-100) per residue, or None if file missing.
    """
    if not os.path.exists(pdb_path):
        return None

    from Bio.PDB import PDBParser
    parser = PDBParser(QUIET=True)
    structure = parser.get_structure("protein", pdb_path)

    plddt_per_residue = []
    for model in structure:
        for chain in model:
            for residue in chain:
                # Get CA atom B-factor (pLDDT in ESMFold PDBs)
                if 'CA' in residue:
                    plddt_per_residue.append(residue['CA'].get_bfactor())
                elif residue.get_unpacked_list():
                    plddt_per_residue.append(residue.get_unpacked_list()[0].get_bfactor())
        break  # Only first model

    return np.array(plddt_per_residue)


def compute_stability_per_position(msa, plddt=None):
    """Compute BLOSUM62-based stability proxy at each position.

    stability_score = -mean(BLOSUM62(wt, mut)) weighted by mutation frequency.
    Higher score = more radical/destabilizing substitutions observed.

    If pLDDT available, we also compute a structure-weighted version:
    stability_structural = stability_score * (pLDDT / 100)
    (mutations in well-folded regions are more likely to be destabilizing)
    """
    n_seqs, seq_len = msa.shape
    stability_scores = np.zeros(seq_len)

    for pos in range(seq_len):
        col = msa[:, pos]
        counts = Counter(c for c in col if c in VALID_AA)
        if not counts:
            continue

        consensus = max(counts, key=counts.get)

        # Weighted mean BLOSUM62 score for non-consensus AAs
        weighted_sum = 0.0
        weight_total = 0.0
        for aa, count in counts.items():
            if aa == consensus:
                continue
            b62 = get_blosum62(consensus, aa)
            if b62 is not None:
                weighted_sum += b62 * count
                weight_total += count

        if weight_total > 0:
            # Negate: low BLOSUM62 (radical) -> high stability_score
            stability_scores[pos] = -(weighted_sum / weight_total)

    return stability_scores


# ── Pathogen configuration ───────────────────────────────────────────────
PATHOGENS = {
    "SARS-CoV-2": {
        "fasta": "data/ncbi_temporal/spike_500_subsample.fasta",
        "pdb": "sars2.pdb",
    },
    "H3N2": {
        "fasta": "data/influenza/h3n2_ha_sequences.fasta",
        "pdb": "influenza_h3n2.pdb",
    },
    "Norovirus": {
        "fasta": "data/norovirus/norovirus_vp1_sequences.fasta",
        "pdb": "norovirus.pdb",
    },
    "HIV-1": {
        "fasta": "data/hiv/hiv1_gp120_sequences.fasta",
        "pdb": "hiv.pdb",
    },
    "Dengue": {
        "fasta": "data/dengue/dengue_e_sequences.fasta",
        "pdb": "dengue.pdb",
    },
    "RSV": {
        "fasta": "data/rsv/rsv_f_sequences.fasta",
        "pdb": "rsv.pdb",
    },
    "Influenza_B": {
        "fasta": "data/influenza/influenza_b_ha_sequences.fasta",
        "pdb": "influenza_b.pdb",
    },
    "MERS": {
        "fasta": "data/mers/mers_spike_sequences.fasta",
        "pdb": "mers.pdb",
    },
    "HCV": {
        "fasta": "data/hcv/hcv_e2_sequences.fasta",
        "pdb": "hcv.pdb",
    },
    "Zika": {
        "fasta": "data/zika/zika_e_sequences.fasta",
        "pdb": "zika.pdb",
    },
    "Rabies": {
        "fasta": "data/rabies/rabies_g_sequences.fasta",
        "pdb": "rabies.pdb",
    },
    "EV-A71": {
        "fasta": "data/enterovirus/eva71_vp1_sequences.fasta",
        "pdb": "eva71.pdb",
    },
}

BASE = os.path.join(os.path.dirname(__file__), "..")
PDB_DIR = os.path.join(BASE, "results/mutbench/structural_features/pdb_structures")
OUT_DIR = os.path.join(BASE, "results/mutbench/feature_analysis")
os.makedirs(OUT_DIR, exist_ok=True)


def main():
    print("=" * 65)
    print("Computing per-position stability proxy (BLOSUM62) for 12 pathogens")
    print("=" * 65)
    print("\nMethod: stability_score = -mean(BLOSUM62(wt, mut)) weighted by freq")
    print("  Higher score = more radical substitutions = potentially destabilizing")
    print("  pLDDT weighting: stability * (pLDDT/100) for structure-aware score\n")

    all_results = []

    for pathogen, cfg in PATHOGENS.items():
        fasta_path = os.path.join(BASE, cfg["fasta"])
        pdb_path = os.path.join(PDB_DIR, cfg["pdb"])

        print(f"  {pathogen}:")
        print(f"    FASTA: {cfg['fasta']}")

        if not os.path.exists(fasta_path):
            print(f"    WARNING: FASTA not found, skipping")
            continue

        # Parse MSA
        msa = parse_msa(fasta_path)
        print(f"    MSA: {msa.shape[0]} sequences x {msa.shape[1]} positions")

        # Extract pLDDT from PDB
        plddt = extract_plddt_from_pdb(pdb_path)
        if plddt is not None:
            print(f"    PDB: {len(plddt)} residues, mean pLDDT={plddt.mean():.1f}")
        else:
            print(f"    PDB: not found, using stability score without pLDDT weighting")

        # Compute stability scores
        stability = compute_stability_per_position(msa, plddt)

        # Build output DataFrame
        result = {
            "position": np.arange(len(stability)),
            "stability_score": np.round(stability, 4),
        }

        # Add pLDDT-weighted version if PDB available
        if plddt is not None:
            # Align lengths (MSA may differ from PDB)
            min_len = min(len(stability), len(plddt))
            stability_structural = np.zeros(len(stability))
            stability_structural[:min_len] = stability[:min_len] * (plddt[:min_len] / 100.0)
            result["stability_structural"] = np.round(stability_structural, 4)
            result["plddt"] = np.zeros(len(stability))
            result["plddt"][:min_len] = np.round(plddt[:min_len], 2)

        df = pd.DataFrame(result)
        out_path = os.path.join(OUT_DIR, f"{pathogen}_stability.csv")
        df.to_csv(out_path, index=False)

        # Stats
        nonzero = np.sum(stability > 0)
        print(f"    Stability: mean={stability.mean():.3f}, max={stability.max():.2f}, "
              f"variable_positions={nonzero}/{len(stability)}")

        all_results.append({
            "pathogen": pathogen,
            "n_positions": len(stability),
            "n_sequences": msa.shape[0],
            "mean_stability": round(stability.mean(), 4),
            "max_stability": round(stability.max(), 2),
            "variable_positions": int(nonzero),
            "pct_variable": round(100 * nonzero / len(stability), 1),
            "has_plddt": plddt is not None,
        })

        print(f"    Saved: {out_path}")

    # Summary
    summary = pd.DataFrame(all_results)
    summary_path = os.path.join(OUT_DIR, "stability_summary.csv")
    summary.to_csv(summary_path, index=False)

    print(f"\n{'=' * 65}")
    print("Summary:")
    print(summary.to_string(index=False))
    print(f"\nSaved summary: {summary_path}")
    print(f"Computed stability for {len(all_results)} pathogens")
    print("Done!")


if __name__ == "__main__":
    main()
