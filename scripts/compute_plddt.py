#!/usr/bin/env python3
"""
Compute per-position pLDDT scores for 9 pathogen target proteins.

Strategy:
1. Try AlphaFold Database (pre-computed, high quality)
2. Fall back to ESMFold API with chunking for long sequences
3. Extract pLDDT from PDB B-factor column

Output: results/mutbench/structural_features/{pathogen}_plddt.csv
"""

import os
import sys
import time
import requests
import numpy as np
import pandas as pd
from Bio import SeqIO
from io import StringIO

BASE = "/proj/paper"
OUT_DIR = f"{BASE}/results/mutbench/structural_features"
os.makedirs(OUT_DIR, exist_ok=True)

# 9 pathogens with their FASTA files and UniProt accessions for AlphaFold DB
PATHOGENS = {
    "sars2": {
        "fasta": f"{BASE}/data/ncbi_temporal/spike_500_subsample.fasta",
        "name": "SARS-CoV-2 Spike",
        "uniprot": "P0DTC2",  # SARS-CoV-2 Spike
    },
    "mers": {
        "fasta": f"{BASE}/data/mers/mers_spike_sequences.fasta",
        "name": "MERS Spike",
        "uniprot": "R9UQ53",  # MERS-CoV Spike (K9N5Q8 is another)
    },
    "hiv": {
        "fasta": f"{BASE}/data/hiv/hiv1_gp120_sequences.fasta",
        "name": "HIV-1 gp120",
        "uniprot": None,  # HIV has many strains, no single reference
    },
    "dengue": {
        "fasta": f"{BASE}/data/dengue/dengue_e_sequences.fasta",
        "name": "Dengue E protein",
        "uniprot": None,
    },
    "norovirus": {
        "fasta": f"{BASE}/data/norovirus/norovirus_vp1_sequences.fasta",
        "name": "Norovirus VP1",
        "uniprot": None,
    },
    "hcv": {
        "fasta": f"{BASE}/data/hcv/hcv_e2_sequences.fasta",
        "name": "HCV E2",
        "uniprot": None,
    },
    "rsv": {
        "fasta": f"{BASE}/data/rsv/rsv_f_sequences.fasta",
        "name": "RSV F protein",
        "uniprot": None,
    },
    "influenza_h3n2": {
        "fasta": f"{BASE}/data/influenza/h3n2_ha_sequences.fasta",
        "name": "Influenza A H3N2 HA",
        "uniprot": None,
    },
    "influenza_b": {
        "fasta": f"{BASE}/data/influenza/influenza_b_ha_sequences.fasta",
        "name": "Influenza B HA",
        "uniprot": None,
    },
}


def extract_plddt_from_pdb(pdb_text):
    """Extract per-residue pLDDT from PDB B-factor column (CA atoms)."""
    positions = []
    plddts = []
    for line in pdb_text.split("\n"):
        if line.startswith("ATOM") and line[12:16].strip() == "CA":
            resnum = int(line[22:26].strip())
            bfactor = float(line[60:66].strip())
            positions.append(resnum)
            plddts.append(bfactor)
    return positions, plddts


def try_alphafold_db(uniprot_id):
    """Try to download AlphaFold prediction from the database."""
    if not uniprot_id:
        return None, None

    url = f"https://alphafold.ebi.ac.uk/files/AF-{uniprot_id}-F1-model_v4.pdb"
    print(f"  Trying AlphaFold DB: {url}")
    try:
        r = requests.get(url, timeout=30)
        if r.status_code == 200:
            positions, plddts = extract_plddt_from_pdb(r.text)
            if positions:
                print(f"  -> AlphaFold DB success: {len(positions)} residues")
                return positions, plddts
        else:
            print(f"  -> AlphaFold DB returned {r.status_code}")
    except Exception as e:
        print(f"  -> AlphaFold DB error: {e}")
    return None, None


def esmfold_api_chunk(sequence, chunk_size=400, overlap=50):
    """
    Use ESMFold API with chunking for sequences > 400aa.
    Overlapping chunks are averaged in overlap regions.
    """
    seq_len = len(sequence)
    if seq_len <= chunk_size:
        # Single request
        print(f"  ESMFold API: single request ({seq_len}aa)")
        r = requests.post(
            "https://api.esmatlas.com/foldSequence/v1/pdb/",
            data=sequence,
            timeout=120,
        )
        if r.status_code == 200:
            positions, plddts = extract_plddt_from_pdb(r.text)
            return positions, plddts
        else:
            print(f"  -> ESMFold API error: {r.status_code} {r.text[:100]}")
            return None, None

    # Chunked approach
    print(f"  ESMFold API: chunking {seq_len}aa into {chunk_size}aa chunks (overlap={overlap})")

    # Calculate chunk boundaries
    chunks = []
    start = 0
    while start < seq_len:
        end = min(start + chunk_size, seq_len)
        chunks.append((start, end))
        if end == seq_len:
            break
        start = end - overlap

    # Accumulate pLDDT values (for averaging overlaps)
    plddt_sum = np.zeros(seq_len)
    plddt_count = np.zeros(seq_len)

    for i, (start, end) in enumerate(chunks):
        chunk_seq = sequence[start:end]
        print(f"  Chunk {i+1}/{len(chunks)}: positions {start+1}-{end} ({len(chunk_seq)}aa)")

        try:
            r = requests.post(
                "https://api.esmatlas.com/foldSequence/v1/pdb/",
                data=chunk_seq,
                timeout=120,
            )
            if r.status_code == 200:
                _, chunk_plddts = extract_plddt_from_pdb(r.text)
                for j, plddt in enumerate(chunk_plddts):
                    pos = start + j
                    if pos < seq_len:
                        plddt_sum[pos] += plddt
                        plddt_count[pos] += 1
            else:
                print(f"    -> Error: {r.status_code}")
                return None, None
        except Exception as e:
            print(f"    -> Error: {e}")
            return None, None

        # Rate limiting
        if i < len(chunks) - 1:
            time.sleep(2)

    # Average overlapping regions
    valid = plddt_count > 0
    if not np.all(valid):
        print(f"  WARNING: {np.sum(~valid)} positions without pLDDT")

    plddt_avg = np.where(valid, plddt_sum / plddt_count, 0)
    positions = list(range(1, seq_len + 1))
    plddts = list(plddt_avg)

    return positions, plddts


def get_reference_sequence(fasta_path):
    """Get the first sequence from a FASTA file."""
    rec = next(SeqIO.parse(fasta_path, "fasta"))
    return str(rec.seq), rec.description


def main():
    results_summary = []

    for pathogen, info in PATHOGENS.items():
        print(f"\n{'='*60}")
        print(f"Processing: {pathogen} ({info['name']})")
        print(f"{'='*60}")

        # Get reference sequence
        seq, desc = get_reference_sequence(info["fasta"])
        print(f"  Reference: {desc[:80]}")
        print(f"  Length: {len(seq)}aa")

        positions, plddts = None, None
        source = None

        # Option B: Try AlphaFold DB first (better quality than ESMFold API)
        if info.get("uniprot"):
            positions, plddts = try_alphafold_db(info["uniprot"])
            if positions:
                source = "AlphaFold_DB"

        # Option A: ESMFold API (with chunking)
        if positions is None:
            positions, plddts = esmfold_api_chunk(seq)
            if positions:
                source = "ESMFold_API"

        if positions is None:
            print(f"  FAILED: Could not get pLDDT for {pathogen}")
            results_summary.append({
                "pathogen": pathogen,
                "length": len(seq),
                "source": "FAILED",
                "mean_plddt": None,
            })
            continue

        # Save CSV
        df = pd.DataFrame({
            "position": positions,
            "pLDDT": [round(p, 2) for p in plddts],
        })

        out_path = f"{OUT_DIR}/{pathogen}_plddt.csv"
        df.to_csv(out_path, index=False)

        mean_plddt = np.mean(plddts)
        print(f"  Source: {source}")
        print(f"  Saved: {out_path}")
        print(f"  Mean pLDDT: {mean_plddt:.1f}")
        print(f"  Min pLDDT: {min(plddts):.1f}, Max pLDDT: {max(plddts):.1f}")

        results_summary.append({
            "pathogen": pathogen,
            "protein": info["name"],
            "length": len(seq),
            "source": source,
            "mean_plddt": round(mean_plddt, 1),
            "min_plddt": round(min(plddts), 1),
            "max_plddt": round(max(plddts), 1),
        })

        # Rate limiting between pathogens
        time.sleep(1)

    # Save summary
    summary_df = pd.DataFrame(results_summary)
    summary_path = f"{OUT_DIR}/plddt_summary.csv"
    summary_df.to_csv(summary_path, index=False)
    print(f"\n\nSummary saved to {summary_path}")
    print(summary_df.to_string(index=False))


if __name__ == "__main__":
    main()
