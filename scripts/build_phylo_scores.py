#!/usr/bin/env python3
"""Build phylogeny-based homoplasy scores for all 9 MutBench pathogens.

Pipeline per pathogen:
  1. Load protein sequences from FASTA
  2. Truncate to min length across sequences
  3. Deduplicate identical sequences
  4. Subsample to max 500 sequences (for tree speed)
  5. Write aligned FASTA (already aligned after truncation)
  6. Build tree with FastTree (protein mode)
  7. Run Fitch parsimony to get per-position homoplasy counts
  8. Save CSV with position, raw_count, normalized_score
"""

import os
import sys
import subprocess
import tempfile
import hashlib
from collections import OrderedDict

import numpy as np
import pandas as pd

# Add project root to path
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, PROJECT_ROOT)

from tools.mutbench.scoring.homoplasy import fitch_parsimony_count, load_tree

# --- Configuration ---

MAX_SEQS = 500
SEED = 42
OUTPUT_DIR = os.path.join(PROJECT_ROOT, 'results', 'mutbench', 'homoplasy_scores')

# Pathogen name -> FASTA file path(s)
PATHOGEN_CONFIG = {
    'SARS-CoV-2': [
        'data/ncbi_temporal/spike_500_subsample.fasta',
    ],
    'HIV-1': [
        'data/hiv/hiv1_gp120_sequences.fasta',
    ],
    'Dengue': [
        'data/dengue/dengue_e_sequences.fasta',
    ],
    'Norovirus': [
        'data/norovirus/norovirus_vp1_sequences.fasta',
    ],
    'H3N2': [
        'data/influenza/h3n2_ha_sequences.fasta',
    ],
    'Influenza_B': [
        'data/influenza/influenza_b_ha_sequences.fasta',
    ],
    'MERS': [
        'data/mers/mers_spike_sequences.fasta',
    ],
    'HCV': [
        'data/hcv/hcv_e2_sequences.fasta',
    ],
    'RSV': [
        'data/rsv/rsv_f_sequences.fasta',
    ],
}


def read_fasta(filepath):
    """Read FASTA file, return OrderedDict of name -> sequence."""
    sequences = OrderedDict()
    current_name = None
    current_seq = []
    with open(filepath) as f:
        for line in f:
            line = line.strip()
            if line.startswith('>'):
                if current_name is not None:
                    sequences[current_name] = ''.join(current_seq)
                current_name = line[1:].split()[0]  # First word after >
                current_seq = []
            else:
                current_seq.append(line)
    if current_name is not None:
        sequences[current_name] = ''.join(current_seq)
    return sequences


def clean_sequence(seq):
    """Replace unusual amino acid characters with X, remove gaps."""
    cleaned = []
    valid_aa = set('ACDEFGHIKLMNPQRSTVWY')
    for c in seq.upper():
        if c in valid_aa:
            cleaned.append(c)
        elif c == '-' or c == '.':
            continue  # Skip gaps
        else:
            cleaned.append('X')  # Replace unknown with X
    return ''.join(cleaned)


def truncate_to_min_length(sequences):
    """Truncate all sequences to the minimum length."""
    if not sequences:
        return sequences
    min_len = min(len(seq) for seq in sequences.values())
    return OrderedDict((name, seq[:min_len]) for name, seq in sequences.items())


def deduplicate(sequences):
    """Remove duplicate sequences, keeping first occurrence."""
    seen = set()
    unique = OrderedDict()
    for name, seq in sequences.items():
        h = hashlib.md5(seq.encode()).hexdigest()
        if h not in seen:
            seen.add(h)
            unique[name] = seq
    return unique


def subsample(sequences, max_n, seed=42):
    """Randomly subsample to max_n sequences."""
    if len(sequences) <= max_n:
        return sequences
    rng = np.random.default_rng(seed)
    names = list(sequences.keys())
    chosen = rng.choice(names, size=max_n, replace=False)
    chosen_set = set(chosen)
    return OrderedDict((name, sequences[name]) for name in names if name in chosen_set)


def write_fasta(sequences, filepath):
    """Write sequences to FASTA file."""
    with open(filepath, 'w') as f:
        for name, seq in sequences.items():
            f.write(f'>{name}\n')
            # Write in 60-char lines
            for i in range(0, len(seq), 60):
                f.write(seq[i:i+60] + '\n')


def build_tree(fasta_path, tree_path):
    """Run FastTree to build a phylogenetic tree."""
    cmd = f'fasttree -quiet < {fasta_path} > {tree_path}'
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    if result.returncode != 0:
        raise RuntimeError(f'FastTree failed: {result.stderr}')
    return tree_path


def process_pathogen(pathogen_name, fasta_paths):
    """Process a single pathogen through the full pipeline."""
    print(f'\n{"="*60}')
    print(f'Processing: {pathogen_name}')
    print(f'{"="*60}')

    # Step 1: Load sequences
    all_sequences = OrderedDict()
    for fpath in fasta_paths:
        full_path = os.path.join(PROJECT_ROOT, fpath)
        if not os.path.exists(full_path):
            print(f'  WARNING: {full_path} not found, skipping')
            continue
        seqs = read_fasta(full_path)
        print(f'  Loaded {len(seqs)} sequences from {fpath}')
        all_sequences.update(seqs)

    if not all_sequences:
        print(f'  ERROR: No sequences found for {pathogen_name}')
        return None

    # Step 2: Clean sequences
    cleaned = OrderedDict()
    for name, seq in all_sequences.items():
        c = clean_sequence(seq)
        if len(c) >= 50:  # Skip very short sequences
            cleaned[name] = c
    print(f'  After cleaning: {len(cleaned)} sequences')

    # Step 3: Truncate to min length
    truncated = truncate_to_min_length(cleaned)
    seq_len = len(next(iter(truncated.values())))
    print(f'  Sequence length after truncation: {seq_len}')

    # Step 4: Deduplicate
    unique = deduplicate(truncated)
    print(f'  After deduplication: {len(unique)} unique sequences')

    if len(unique) < 10:
        print(f'  WARNING: Only {len(unique)} unique sequences — too few for reliable tree')

    # Step 5: Subsample
    sampled = subsample(unique, MAX_SEQS, seed=SEED)
    print(f'  After subsampling (max {MAX_SEQS}): {len(sampled)} sequences')

    # Step 6: Write aligned FASTA and build tree
    with tempfile.TemporaryDirectory() as tmpdir:
        aligned_path = os.path.join(tmpdir, 'aligned.fasta')
        tree_path = os.path.join(tmpdir, 'tree.nwk')

        write_fasta(sampled, aligned_path)
        print(f'  Building tree with FastTree...')
        build_tree(aligned_path, tree_path)
        print(f'  Tree built successfully')

        # Step 7: Run Fitch parsimony
        tree = load_tree(tree_path)
        n_terminals = len(tree.get_terminals())
        print(f'  Tree has {n_terminals} terminal nodes')

        print(f'  Running Fitch parsimony ({seq_len} positions)...')
        counts = fitch_parsimony_count(tree, sampled, seq_len)

    # Step 8: Normalize and save
    max_count = counts.max()
    if max_count > 0:
        normalized = counts / max_count
    else:
        normalized = counts.astype(float)

    df = pd.DataFrame({
        'position': np.arange(1, seq_len + 1),  # 1-indexed
        'raw_count': counts,
        'normalized_score': np.round(normalized, 6),
    })

    output_path = os.path.join(OUTPUT_DIR, f'{pathogen_name}_homoplasy.csv')
    df.to_csv(output_path, index=False)
    print(f'  Saved: {output_path}')

    # Summary statistics
    nonzero = counts[counts > 0]
    print(f'\n  --- Summary ---')
    print(f'  Total positions: {seq_len}')
    print(f'  Positions with changes: {len(nonzero)} ({100*len(nonzero)/seq_len:.1f}%)')
    print(f'  Max changes: {max_count}')
    print(f'  Mean changes (nonzero): {nonzero.mean():.2f}' if len(nonzero) > 0 else '  Mean changes: 0')
    print(f'  Median changes (nonzero): {np.median(nonzero):.1f}' if len(nonzero) > 0 else '  Median changes: 0')

    return {
        'pathogen': pathogen_name,
        'n_sequences_raw': len(all_sequences),
        'n_unique': len(unique),
        'n_used': len(sampled),
        'seq_length': seq_len,
        'positions_with_changes': int(len(nonzero)),
        'pct_positions_changed': round(100 * len(nonzero) / seq_len, 1),
        'max_changes': int(max_count),
        'mean_changes_nonzero': round(float(nonzero.mean()), 2) if len(nonzero) > 0 else 0,
        'few_sequences_warning': len(unique) < 50,
    }


def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    results = []
    for pathogen_name, fasta_paths in PATHOGEN_CONFIG.items():
        try:
            info = process_pathogen(pathogen_name, fasta_paths)
            if info:
                results.append(info)
        except Exception as e:
            print(f'  ERROR processing {pathogen_name}: {e}')
            import traceback
            traceback.print_exc()

    # Print summary table
    if results:
        print(f'\n\n{"="*80}')
        print('SUMMARY')
        print(f'{"="*80}')
        summary_df = pd.DataFrame(results)
        print(summary_df.to_string(index=False))

        summary_path = os.path.join(OUTPUT_DIR, 'homoplasy_summary.csv')
        summary_df.to_csv(summary_path, index=False)
        print(f'\nSummary saved: {summary_path}')

        # Note limitations
        few_seqs = [r['pathogen'] for r in results if r['few_sequences_warning']]
        if few_seqs:
            print(f'\nWARNING: Pathogens with <50 unique sequences (limited reliability):')
            for p in few_seqs:
                print(f'  - {p}')


if __name__ == '__main__':
    main()
