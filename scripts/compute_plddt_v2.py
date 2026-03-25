#!/usr/bin/env python3
"""
Compute per-position pLDDT scores for 9 pathogen target proteins.
v2: Uses AlphaFold DB where available, ESMFold API with chunking + retries.
All values on 0-100 scale.
"""

import os
import sys
import time
import requests
import numpy as np
import pandas as pd
from Bio import SeqIO

BASE = "/proj/paper"
OUT_DIR = f"{BASE}/results/mutbench/structural_features"
os.makedirs(OUT_DIR, exist_ok=True)

PATHOGENS = {
    "sars2": {
        "fasta": f"{BASE}/data/ncbi_temporal/spike_500_subsample.fasta",
        "name": "SARS-CoV-2 Spike",
        "alphafold_pdb": "https://alphafold.ebi.ac.uk/files/AF-0000000365840314-model_v1.pdb",
    },
    "mers": {
        "fasta": f"{BASE}/data/mers/mers_spike_sequences.fasta",
        "name": "MERS Spike",
    },
    "hiv": {
        "fasta": f"{BASE}/data/hiv/hiv1_gp120_sequences.fasta",
        "name": "HIV-1 gp120",
    },
    "dengue": {
        "fasta": f"{BASE}/data/dengue/dengue_e_sequences.fasta",
        "name": "Dengue E protein",
    },
    "norovirus": {
        "fasta": f"{BASE}/data/norovirus/norovirus_vp1_sequences.fasta",
        "name": "Norovirus VP1",
    },
    "hcv": {
        "fasta": f"{BASE}/data/hcv/hcv_e2_sequences.fasta",
        "name": "HCV E2",
    },
    "rsv": {
        "fasta": f"{BASE}/data/rsv/rsv_f_sequences.fasta",
        "name": "RSV F protein",
    },
    "influenza_h3n2": {
        "fasta": f"{BASE}/data/influenza/h3n2_ha_sequences.fasta",
        "name": "Influenza A H3N2 HA",
    },
    "influenza_b": {
        "fasta": f"{BASE}/data/influenza/influenza_b_ha_sequences.fasta",
        "name": "Influenza B HA",
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


def try_alphafold_pdb(url):
    """Download a specific AlphaFold PDB and extract pLDDT."""
    print(f"  Trying AlphaFold: {url}")
    try:
        r = requests.get(url, timeout=60)
        if r.status_code == 200:
            positions, plddts = extract_plddt_from_pdb(r.text)
            if positions:
                print(f"  -> Success: {len(positions)} residues, scale 0-100")
                return positions, plddts, "AlphaFold_DB"
        print(f"  -> HTTP {r.status_code}")
    except Exception as e:
        print(f"  -> Error: {e}")
    return None, None, None


def esmfold_api_chunk(sequence, chunk_size=400, overlap=50, max_retries=3):
    """ESMFold API with chunking and retries. Returns pLDDT on 0-100 scale."""
    seq_len = len(sequence)

    if seq_len <= chunk_size:
        chunks = [(0, seq_len)]
    else:
        chunks = []
        start = 0
        while start < seq_len:
            end = min(start + chunk_size, seq_len)
            chunks.append((start, end))
            if end == seq_len:
                break
            start = end - overlap

    print(f"  ESMFold API: {len(chunks)} chunk(s) for {seq_len}aa")

    plddt_sum = np.zeros(seq_len)
    plddt_count = np.zeros(seq_len)

    for i, (start, end) in enumerate(chunks):
        chunk_seq = sequence[start:end]
        print(f"  Chunk {i+1}/{len(chunks)}: pos {start+1}-{end} ({len(chunk_seq)}aa)", end="")

        success = False
        for attempt in range(max_retries):
            try:
                r = requests.post(
                    "https://api.esmatlas.com/foldSequence/v1/pdb/",
                    data=chunk_seq,
                    timeout=180,
                )
                if r.status_code == 200:
                    _, chunk_plddts = extract_plddt_from_pdb(r.text)
                    for j, plddt in enumerate(chunk_plddts):
                        pos = start + j
                        if pos < seq_len:
                            plddt_sum[pos] += plddt
                            plddt_count[pos] += 1
                    print(f" -> OK")
                    success = True
                    break
                else:
                    print(f" -> {r.status_code}", end="")
                    if attempt < max_retries - 1:
                        wait = 10 * (attempt + 1)
                        print(f", retry in {wait}s", end="")
                        time.sleep(wait)
            except Exception as e:
                print(f" -> {e}", end="")
                if attempt < max_retries - 1:
                    wait = 10 * (attempt + 1)
                    print(f", retry in {wait}s", end="")
                    time.sleep(wait)

        if not success:
            print(f" FAILED after {max_retries} attempts")
            return None, None

        if i < len(chunks) - 1:
            time.sleep(3)

    valid = plddt_count > 0
    if not np.all(valid):
        print(f"  WARNING: {np.sum(~valid)} positions without pLDDT")

    plddt_avg = np.where(valid, plddt_sum / plddt_count, 0)

    # ESMFold B-factors are on 0-1 scale; convert to 0-100
    if np.max(plddt_avg) <= 1.0:
        plddt_avg = plddt_avg * 100.0
        print(f"  Converted from 0-1 to 0-100 scale")

    positions = list(range(1, seq_len + 1))
    return positions, list(plddt_avg)


def get_reference_sequence(fasta_path):
    rec = next(SeqIO.parse(fasta_path, "fasta"))
    return str(rec.seq), rec.description


def main():
    # Check which pathogens already have results
    existing = {}
    for pathogen in PATHOGENS:
        csv_path = f"{OUT_DIR}/{pathogen}_plddt.csv"
        if os.path.exists(csv_path):
            df = pd.read_csv(csv_path)
            # Check if already on 0-100 scale
            if df["pLDDT"].max() > 1.0:
                existing[pathogen] = df
                print(f"Skipping {pathogen}: already computed (0-100 scale)")
            else:
                print(f"Re-computing {pathogen}: was on 0-1 scale, converting to 0-100")

    results_summary = []

    for pathogen, info in PATHOGENS.items():
        print(f"\n{'='*60}")
        print(f"Processing: {pathogen} ({info['name']})")
        print(f"{'='*60}")

        # Check if we need to just rescale
        csv_path = f"{OUT_DIR}/{pathogen}_plddt.csv"
        if os.path.exists(csv_path):
            df = pd.read_csv(csv_path)
            if df["pLDDT"].max() <= 1.0:
                # Rescale existing 0-1 to 0-100
                df["pLDDT"] = (df["pLDDT"] * 100).round(2)
                df.to_csv(csv_path, index=False)
                mean_p = df["pLDDT"].mean()
                print(f"  Rescaled existing file to 0-100: mean={mean_p:.1f}")
                results_summary.append({
                    "pathogen": pathogen,
                    "protein": info["name"],
                    "length": len(df),
                    "source": "ESMFold_API (rescaled)",
                    "mean_plddt": round(mean_p, 1),
                    "min_plddt": round(df["pLDDT"].min(), 1),
                    "max_plddt": round(df["pLDDT"].max(), 1),
                })
                continue
            elif df["pLDDT"].max() > 1.0:
                mean_p = df["pLDDT"].mean()
                print(f"  Already computed: mean={mean_p:.1f}")
                results_summary.append({
                    "pathogen": pathogen,
                    "protein": info["name"],
                    "length": len(df),
                    "source": "existing",
                    "mean_plddt": round(mean_p, 1),
                    "min_plddt": round(df["pLDDT"].min(), 1),
                    "max_plddt": round(df["pLDDT"].max(), 1),
                })
                continue

        seq, desc = get_reference_sequence(info["fasta"])
        print(f"  Reference: {desc[:80]}")
        print(f"  Length: {len(seq)}aa")

        positions, plddts = None, None
        source = None

        # Try AlphaFold DB if URL provided
        if info.get("alphafold_pdb"):
            positions, plddts, source = try_alphafold_pdb(info["alphafold_pdb"])

        # Fall back to ESMFold API
        if positions is None:
            positions, plddts = esmfold_api_chunk(seq)
            if positions:
                source = "ESMFold_API"

        if positions is None:
            print(f"  FAILED: Could not get pLDDT for {pathogen}")
            results_summary.append({
                "pathogen": pathogen,
                "protein": info["name"],
                "length": len(seq),
                "source": "FAILED",
                "mean_plddt": None,
                "min_plddt": None,
                "max_plddt": None,
            })
            continue

        df = pd.DataFrame({
            "position": positions,
            "pLDDT": [round(p, 2) for p in plddts],
        })
        df.to_csv(csv_path, index=False)

        mean_p = np.mean(plddts)
        print(f"  Source: {source}")
        print(f"  Saved: {csv_path}")
        print(f"  Mean pLDDT: {mean_p:.1f}, Range: {min(plddts):.1f}-{max(plddts):.1f}")

        results_summary.append({
            "pathogen": pathogen,
            "protein": info["name"],
            "length": len(df),
            "source": source,
            "mean_plddt": round(mean_p, 1),
            "min_plddt": round(min(plddts), 1),
            "max_plddt": round(max(plddts), 1),
        })

        time.sleep(2)

    summary_df = pd.DataFrame(results_summary)
    summary_path = f"{OUT_DIR}/plddt_summary.csv"
    summary_df.to_csv(summary_path, index=False)
    print(f"\n\n{'='*60}")
    print("SUMMARY")
    print(f"{'='*60}")
    print(summary_df.to_string(index=False))


if __name__ == "__main__":
    main()
