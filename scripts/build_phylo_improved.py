#!/usr/bin/env python3
"""Improved SARS-CoV-2 homoplasy scoring with temporal stratified sampling.

Loads all available NCBI temporal SARS-CoV-2 spike protein sequences,
filters, deduplicates, stratified subsamples to 2000 sequences,
aligns with MAFFT, builds tree with FastTree, runs Fitch parsimony,
and maps back to amino acid positions using reference mapping.
"""

import os
import sys
import subprocess
import tempfile
import hashlib
import random
from collections import defaultdict
from pathlib import Path

import numpy as np
import pandas as pd

# Add project root to path
PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from tools.mutbench.scoring.homoplasy import fitch_parsimony_count, load_tree


# --- Configuration ---
DATA_DIR = PROJECT_ROOT / "data" / "ncbi_temporal"
OUTPUT_DIR = PROJECT_ROOT / "results" / "mutbench" / "homoplasy_scores"
TOTAL_SUBSAMPLE = 2000
SEED = 42
MIN_LEN = 1250
MAX_LEN = 1300

# Key positions to check (0-based AA positions in Spike)
KEY_POSITIONS = {
    "D614G": 614,
    "E484K": 484,
    "N501Y": 501,
    "L452R": 452,
    "K417N": 417,
    "P681H": 681,
}

STANDARD_AA = set("ACDEFGHIKLMNPQRSTVWY")


def load_fasta(filepath):
    """Load FASTA file, return list of (header, sequence) tuples."""
    records = []
    header = None
    seq_parts = []
    with open(filepath) as f:
        for line in f:
            line = line.strip()
            if line.startswith(">"):
                if header is not None:
                    records.append((header, "".join(seq_parts)))
                header = line[1:].split()[0]  # Use accession only
                seq_parts = []
            else:
                seq_parts.append(line)
    if header is not None:
        records.append((header, "".join(seq_parts)))
    return records


def clean_sequence(seq):
    """Replace non-standard amino acids with gap."""
    return "".join(c if c in STANDARD_AA else "-" for c in seq.upper())


def main():
    random.seed(SEED)
    np.random.seed(SEED)

    # --- Step 1: Discover and load all available FASTA files ---
    fasta_files = {}
    # Check standard temporal files
    for fname in sorted(DATA_DIR.glob("spike_*.fasta")):
        if "subsample" in fname.name or "nwk" in fname.suffix:
            continue
        # Extract period label from filename
        label = fname.stem.replace("spike_", "")
        fasta_files[label] = fname

    # Also check for any 2024/2025 data in other directories
    for extra_dir in [PROJECT_ROOT / "data" / "sars-cov-2", PROJECT_ROOT / "data" / "sarscov2"]:
        if extra_dir.exists():
            for f in extra_dir.glob("*.fasta"):
                fasta_files[f.stem] = f

    print(f"Found {len(fasta_files)} FASTA files:")
    for label, path in sorted(fasta_files.items()):
        print(f"  {label}: {path}")

    # --- Step 2: Load all sequences, clean, filter by length ---
    period_sequences = {}  # period -> list of (header, cleaned_seq)
    for label, path in sorted(fasta_files.items()):
        records = load_fasta(str(path))
        cleaned = []
        for header, seq in records:
            cseq = clean_sequence(seq)
            # Remove gaps for length check
            ungapped = cseq.replace("-", "")
            if MIN_LEN <= len(ungapped) <= MAX_LEN:
                cleaned.append((header, ungapped))
        period_sequences[label] = cleaned
        print(f"  {label}: {len(records)} raw -> {len(cleaned)} after length filter [{MIN_LEN}-{MAX_LEN}]")

    # --- Step 3: Deduplicate within each period ---
    period_unique = {}
    for label, seqs in period_sequences.items():
        seen_hashes = set()
        unique = []
        for header, seq in seqs:
            h = hashlib.md5(seq.encode()).hexdigest()
            if h not in seen_hashes:
                seen_hashes.add(h)
                unique.append((header, seq))
        period_unique[label] = unique
        print(f"  {label}: {len(seqs)} -> {len(unique)} unique sequences")

    # --- Step 4: Stratified subsample ---
    total_unique = sum(len(v) for v in period_unique.values())
    print(f"\nTotal unique sequences: {total_unique}")

    if total_unique <= TOTAL_SUBSAMPLE:
        print(f"Total unique ({total_unique}) <= target ({TOTAL_SUBSAMPLE}), using all.")
        sampled = {}
        for label, seqs in period_unique.items():
            sampled[label] = seqs
    else:
        sampled = {}
        # Proportional allocation
        remaining = TOTAL_SUBSAMPLE
        labels_sorted = sorted(period_unique.keys())
        for i, label in enumerate(labels_sorted):
            n_unique = len(period_unique[label])
            if i == len(labels_sorted) - 1:
                n_alloc = remaining
            else:
                n_alloc = int(round(TOTAL_SUBSAMPLE * n_unique / total_unique))
            n_take = min(n_alloc, n_unique)
            sampled[label] = random.sample(period_unique[label], n_take)
            remaining -= n_take
            print(f"  {label}: allocated {n_alloc}, taking {n_take} (of {n_unique} unique)")

    all_seqs = []
    for label in sorted(sampled.keys()):
        for header, seq in sampled[label]:
            # Tag header with period for traceability
            all_seqs.append((f"{header}_{label}", seq))

    print(f"\nTotal sampled sequences: {len(all_seqs)}")

    # --- Step 5: Write to temp FASTA and run MAFFT ---
    with tempfile.NamedTemporaryFile(mode="w", suffix=".fasta", delete=False) as f:
        input_fasta = f.name
        for header, seq in all_seqs:
            f.write(f">{header}\n{seq}\n")

    aligned_fasta = input_fasta.replace(".fasta", "_aligned.fasta")
    print(f"\nRunning MAFFT alignment on {len(all_seqs)} sequences...")
    result = subprocess.run(
        ["mafft", "--auto", "--quiet", "--thread", "4", input_fasta],
        capture_output=True, text=True, timeout=3600
    )
    if result.returncode != 0:
        print(f"MAFFT error: {result.stderr}")
        sys.exit(1)

    with open(aligned_fasta, "w") as f:
        f.write(result.stdout)
    print("MAFFT alignment complete.")

    # --- Step 6: Load alignment ---
    alignment_dict = {}
    records = load_fasta(aligned_fasta)
    for header, seq in records:
        alignment_dict[header] = seq

    aln_length = len(next(iter(alignment_dict.values())))
    print(f"Alignment length: {aln_length}")

    # --- Step 7: Reference mapping ---
    # Use first sequence as reference proxy
    ref_name = list(alignment_dict.keys())[0]
    ref_aln_seq = alignment_dict[ref_name]
    print(f"Reference sequence: {ref_name}")

    # Build mapping: AA position (0-based) -> alignment column
    aa_to_aln = {}
    aa_pos = 0
    for aln_col, char in enumerate(ref_aln_seq):
        if char != "-":
            aa_to_aln[aa_pos] = aln_col
            aa_pos += 1
    ref_aa_len = aa_pos
    print(f"Reference AA length: {ref_aa_len}")

    # Reverse mapping: alignment column -> AA position
    aln_to_aa = {v: k for k, v in aa_to_aln.items()}

    # --- Step 8: Run FastTree ---
    tree_file = input_fasta.replace(".fasta", ".nwk")
    print(f"\nRunning FastTree on {len(alignment_dict)} sequences...")
    with open(tree_file, "w") as tf:
        result = subprocess.run(
            ["fasttree", "-quiet", "-nosupport", aligned_fasta],
            stdout=tf, stderr=subprocess.PIPE, text=True, timeout=3600
        )
    if result.returncode != 0:
        print(f"FastTree error: {result.stderr}")
        sys.exit(1)
    print("FastTree complete.")

    # --- Step 9: Fitch parsimony ---
    print("\nRunning Fitch parsimony...")
    tree = load_tree(tree_file)
    raw_counts = fitch_parsimony_count(tree, alignment_dict, aln_length)
    print(f"Raw counts computed for {aln_length} alignment columns.")

    # --- Step 10: Map back to AA positions ---
    aa_counts = np.zeros(ref_aa_len, dtype=int)
    for aln_col in range(aln_length):
        if aln_col in aln_to_aa:
            aa_counts[aln_to_aa[aln_col]] = raw_counts[aln_col]

    # Normalize
    max_count = aa_counts.max() if aa_counts.max() > 0 else 1
    normalized = aa_counts / max_count

    # --- Step 11: Save results ---
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    output_path = OUTPUT_DIR / "SARS-CoV-2_homoplasy_improved.csv"
    df = pd.DataFrame({
        "position": range(ref_aa_len),
        "raw_count": aa_counts,
        "normalized_score": normalized,
    })
    df.to_csv(output_path, index=False)
    print(f"\nResults saved to {output_path}")

    # --- Step 12: Key position checks ---
    print("\n=== Key Position Homoplasy Scores ===")
    print(f"{'Mutation':<10} {'Position':<10} {'Raw Count':<12} {'Normalized':<12}")
    print("-" * 44)
    for name, pos in sorted(KEY_POSITIONS.items(), key=lambda x: x[1]):
        if pos < ref_aa_len:
            print(f"{name:<10} {pos:<10} {aa_counts[pos]:<12} {normalized[pos]:<12.4f}")
        else:
            print(f"{name:<10} {pos:<10} OUT OF RANGE")

    # --- Step 13: Compare with original ---
    original_path = OUTPUT_DIR / "SARS-CoV-2_homoplasy.csv"
    if original_path.exists():
        orig_df = pd.read_csv(original_path)
        print("\n=== Comparison with Original (500 seq) ===")
        # Spearman correlation
        from scipy.stats import spearmanr
        min_len = min(len(df), len(orig_df))
        rho, p = spearmanr(df["normalized_score"].values[:min_len],
                           orig_df["normalized_score"].values[:min_len])
        print(f"Spearman rho: {rho:.4f}, p-value: {p:.2e}")

        # Compare key positions
        print(f"\n{'Mutation':<10} {'Pos':<6} {'Original':<12} {'Improved':<12} {'Change':<10}")
        print("-" * 50)
        for name, pos in sorted(KEY_POSITIONS.items(), key=lambda x: x[1]):
            if pos < min_len:
                orig_val = orig_df["normalized_score"].values[pos]
                new_val = df["normalized_score"].values[pos]
                change = new_val - orig_val
                print(f"{name:<10} {pos:<6} {orig_val:<12.4f} {new_val:<12.4f} {change:+.4f}")

    # Summary stats
    print("\n=== Summary Statistics ===")
    print(f"Total positions: {ref_aa_len}")
    print(f"Mean raw count: {aa_counts.mean():.2f}")
    print(f"Max raw count: {aa_counts.max()} at position {aa_counts.argmax()}")
    print(f"Positions with 0 changes: {(aa_counts == 0).sum()}")
    print(f"Top 20 positions by raw count:")
    top20_idx = np.argsort(aa_counts)[-20:][::-1]
    for idx in top20_idx:
        print(f"  Position {idx}: {aa_counts[idx]} changes (normalized: {normalized[idx]:.4f})")

    # Cleanup temp files
    for f in [input_fasta, aligned_fasta, tree_file]:
        if os.path.exists(f):
            os.remove(f)

    print("\nDone!")


if __name__ == "__main__":
    main()
