#!/usr/bin/env python3
"""Compute per-residue SASA (Solvent Accessible Surface Area) for 9 pathogens.

Uses ESMFold API to obtain PDB structures, then BioPython ShrakeRupley
to compute per-residue SASA. Normalizes to RSA (Relative Solvent Accessibility)
using Tien et al. (2013) max ASA values.

Output: per-position RSA (0-1 scale, 1 = fully exposed).
"""

import os
import sys
import time
import requests
import numpy as np
import pandas as pd
from io import StringIO
from Bio import SeqIO
from Bio.PDB import PDBParser
from Bio.PDB.SASA import ShrakeRupley

BASE = os.path.join(os.path.dirname(__file__), "..")
OUT_DIR = os.path.join(BASE, "results/mutbench/structural_features")
PDB_DIR = os.path.join(OUT_DIR, "pdb_structures")
os.makedirs(PDB_DIR, exist_ok=True)

# Max ASA values from Tien et al. (2013) PLOS ONE for normalization to RSA
MAX_ASA = {
    'A': 129, 'R': 274, 'N': 195, 'D': 193, 'C': 167,
    'E': 223, 'Q': 225, 'G': 104, 'H': 224, 'I': 197,
    'L': 201, 'K': 236, 'M': 224, 'F': 240, 'P': 159,
    'S': 155, 'T': 172, 'W': 285, 'Y': 263, 'V': 174,
}

PATHOGENS = {
    "SARS-CoV-2": {
        "fasta": "data/ncbi_temporal/spike_500_subsample.fasta",
        "name": "sars2",
    },
    "H3N2": {
        "fasta": "data/influenza/h3n2_ha_sequences.fasta",
        "name": "influenza_h3n2",
    },
    "Norovirus": {
        "fasta": "data/norovirus/norovirus_vp1_sequences.fasta",
        "name": "norovirus",
    },
    "HIV-1": {
        "fasta": "data/hiv/hiv1_gp120_sequences.fasta",
        "name": "hiv",
    },
    "Dengue": {
        "fasta": "data/dengue/dengue_e_sequences.fasta",
        "name": "dengue",
    },
    "RSV": {
        "fasta": "data/rsv/rsv_f_sequences.fasta",
        "name": "rsv",
    },
    "Influenza_B": {
        "fasta": "data/influenza/influenza_b_ha_sequences.fasta",
        "name": "influenza_b",
    },
    "MERS": {
        "fasta": "data/mers/mers_spike_sequences.fasta",
        "name": "mers",
    },
    "HCV": {
        "fasta": "data/hcv/hcv_e2_sequences.fasta",
        "name": "hcv",
    },
}


def get_reference_sequence(fasta_path):
    """Get first sequence from FASTA as reference."""
    rec = next(SeqIO.parse(fasta_path, "fasta"))
    return str(rec.seq).replace("-", "").replace("X", "A")  # clean


def fold_with_esmfold(sequence, pdb_path, chunk_size=400, overlap=50, max_retries=3):
    """Fold sequence with ESMFold API, save PDB. Handle long sequences by chunking."""
    if os.path.exists(pdb_path):
        print(f"    PDB already exists: {pdb_path}")
        return True

    seq_len = len(sequence)
    if seq_len > chunk_size:
        # For long sequences, fold only a representative chunk or use full sequence
        # ESMFold API has a ~400aa limit for reliable folding
        print(f"    Sequence too long ({seq_len}aa) for single ESMFold call")
        print(f"    Using chunked folding with overlap...")
        return fold_chunked(sequence, pdb_path, chunk_size, overlap, max_retries)

    for attempt in range(max_retries):
        try:
            r = requests.post(
                "https://api.esmatlas.com/foldSequence/v1/pdb/",
                data=sequence,
                timeout=180,
            )
            if r.status_code == 200:
                with open(pdb_path, "w") as f:
                    f.write(r.text)
                print(f"    Folded OK: {seq_len}aa")
                return True
            else:
                print(f"    HTTP {r.status_code}, attempt {attempt+1}/{max_retries}")
                if attempt < max_retries - 1:
                    time.sleep(10 * (attempt + 1))
        except Exception as e:
            print(f"    Error: {e}, attempt {attempt+1}/{max_retries}")
            if attempt < max_retries - 1:
                time.sleep(10 * (attempt + 1))

    return False


def fold_chunked(sequence, pdb_path, chunk_size=400, overlap=50, max_retries=3):
    """Fold long sequence in chunks, combine PDB files."""
    seq_len = len(sequence)
    # For SASA computation, we just need per-residue values
    # Use non-overlapping chunks and concatenate results
    chunks = []
    start = 0
    while start < seq_len:
        end = min(start + chunk_size, seq_len)
        chunks.append((start, end))
        if end == seq_len:
            break
        start = end - overlap

    print(f"    Chunking: {len(chunks)} chunks for {seq_len}aa")

    all_pdb_lines = []
    atom_counter = 0
    residue_offset = 0

    for i, (start, end) in enumerate(chunks):
        chunk_seq = sequence[start:end]
        print(f"    Chunk {i+1}/{len(chunks)}: pos {start+1}-{end} ({len(chunk_seq)}aa)", end="")

        success = False
        for attempt in range(max_retries):
            try:
                r = requests.post(
                    "https://api.esmatlas.com/foldSequence/v1/pdb/",
                    data=chunk_seq,
                    timeout=180,
                )
                if r.status_code == 200:
                    print(f" -> OK")
                    # Parse PDB and adjust residue numbers
                    for line in r.text.split("\n"):
                        if line.startswith("ATOM"):
                            # Adjust residue number for non-first chunks
                            resnum = int(line[22:26].strip())
                            # Only keep non-overlapping residues
                            if i > 0 and resnum <= overlap:
                                continue
                            new_resnum = resnum + start if i == 0 else resnum + start
                            atom_counter += 1
                            new_line = (
                                line[:6] +
                                f"{atom_counter:5d}" +
                                line[11:22] +
                                f"{new_resnum:4d}" +
                                line[26:]
                            )
                            all_pdb_lines.append(new_line)
                    success = True
                    break
                else:
                    print(f" -> {r.status_code}", end="")
                    if attempt < max_retries - 1:
                        time.sleep(10 * (attempt + 1))
            except Exception as e:
                print(f" -> {e}", end="")
                if attempt < max_retries - 1:
                    time.sleep(10 * (attempt + 1))

        if not success:
            print(f" FAILED")
            return False

        if i < len(chunks) - 1:
            time.sleep(3)

    # Write combined PDB
    with open(pdb_path, "w") as f:
        f.write("\n".join(all_pdb_lines))
        f.write("\nEND\n")

    return True


def compute_sasa_from_pdb(pdb_path):
    """Compute per-residue SASA from PDB file using BioPython ShrakeRupley."""
    parser = PDBParser(QUIET=True)
    structure = parser.get_structure("protein", pdb_path)
    model = structure[0]

    sr = ShrakeRupley()
    sr.compute(model, level="R")

    positions = []
    sasa_values = []
    rsa_values = []

    for chain in model:
        for residue in chain:
            if residue.id[0] != ' ':  # skip hetero
                continue
            resname = residue.get_resname()
            # Convert 3-letter to 1-letter
            from Bio.Data.IUPACData import protein_letters_3to1
            try:
                aa1 = protein_letters_3to1.get(resname.capitalize(), 'X')
            except:
                aa1 = 'X'

            resnum = residue.id[1]
            sasa = residue.sasa

            # Normalize to RSA
            max_asa = MAX_ASA.get(aa1.upper(), 200)
            rsa = min(sasa / max_asa, 1.0) if max_asa > 0 else 0.0

            positions.append(resnum)
            sasa_values.append(round(sasa, 2))
            rsa_values.append(round(rsa, 4))

    return positions, sasa_values, rsa_values


def main():
    print("=" * 60)
    print("Computing per-residue SASA/RSA for 9 pathogens")
    print("=" * 60)

    all_results = []

    for pathogen, cfg in PATHOGENS.items():
        print(f"\n{'='*40}")
        print(f"  {pathogen}")
        print(f"{'='*40}")

        # Check if already computed
        out_csv = os.path.join(OUT_DIR, f"{cfg['name']}_sasa.csv")
        if os.path.exists(out_csv):
            print(f"    Already computed: {out_csv}")
            df = pd.read_csv(out_csv)
            all_results.append({
                "pathogen": pathogen,
                "n_residues": len(df),
                "mean_rsa": round(df["RSA"].mean(), 3),
                "source": "existing",
            })
            continue

        fasta_path = os.path.join(BASE, cfg["fasta"])
        seq = get_reference_sequence(fasta_path)
        print(f"    Sequence length: {len(seq)}aa")

        # Get PDB structure
        pdb_path = os.path.join(PDB_DIR, f"{cfg['name']}.pdb")
        ok = fold_with_esmfold(seq, pdb_path)
        if not ok:
            print(f"    FAILED to get structure for {pathogen}")
            continue

        # Compute SASA
        try:
            positions, sasa_values, rsa_values = compute_sasa_from_pdb(pdb_path)
        except Exception as e:
            print(f"    SASA computation failed: {e}")
            continue

        # Save
        df = pd.DataFrame({
            "position": positions,
            "SASA": sasa_values,
            "RSA": rsa_values,
        })
        df.to_csv(out_csv, index=False)
        print(f"    Saved: {out_csv} ({len(df)} residues)")
        print(f"    Mean RSA={df['RSA'].mean():.3f}, Range=[{df['RSA'].min():.3f}, {df['RSA'].max():.3f}]")

        all_results.append({
            "pathogen": pathogen,
            "n_residues": len(df),
            "mean_rsa": round(df["RSA"].mean(), 3),
            "source": "ESMFold",
        })

        time.sleep(2)

    summary = pd.DataFrame(all_results)
    summary.to_csv(os.path.join(OUT_DIR, "sasa_summary.csv"), index=False)
    print(f"\n\nSummary:\n{summary.to_string(index=False)}")
    print("\nDone!")


if __name__ == "__main__":
    main()
