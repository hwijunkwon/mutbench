#!/usr/bin/env python3
"""Convert EVE all-singles CSVs to per-position feature CSVs.

For each protein, reads the EVE output (mutations + evol_indices),
extracts positions from mutation names (format: A123G -> position 123),
computes mean |evol_indices| per position, and saves as feature CSV
compatible with the scoring pipeline.

Output: {PATHOGEN}_eve.csv with columns: position, fubar_score
"""

import os
import re
import numpy as np
import pandas as pd
from pathlib import Path

# EVE protein name -> pathogen name mapping
PROTEIN_TO_PATHOGEN = {
    'SPIKE_SARS2': 'SARS-CoV-2',
    'HA_H3N2': 'H3N2',
    'VP1_NORO': 'Norovirus',
    'GP120_HIV1': 'HIV-1',
    'E_DENV': 'Dengue',
    'F_RSV': 'RSV',
    'HA_INFLUB': 'Influenza_B',
    'SPIKE_MERS': 'MERS',
    'E2_HCV': 'HCV',
    'G_RABIES': 'Rabies',
    'VP1_EVA71': 'EV-A71',
}

EVE_SCORES_DIR = Path('/proj/paper/results/mutbench/eve_scores')
FEATURE_DIR = Path('/proj/paper/results/mutbench/feature_analysis')
MSA_DIR = Path('/proj/paper/data/eve_msa')


def get_seq_length_from_msa(protein_name):
    """Read MSA header to get sequence length (focus positions)."""
    msa_path = MSA_DIR / f'{protein_name}.a2m'
    if not msa_path.exists():
        return None
    with open(msa_path) as f:
        header = f.readline().strip()
        # e.g. >SPIKE_SARS2/1-1269
        seq_lines = []
        for line in f:
            line = line.strip()
            if line.startswith('>'):
                break
            seq_lines.append(line)
    seq = ''.join(seq_lines)
    # Count non-gap uppercase positions (focus columns)
    non_gap = sum(1 for c in seq if c.isupper() and c != '-')
    return non_gap


def get_feature_length(pathogen):
    """Get expected feature length from existing feature CSVs."""
    # Try to read any existing feature CSV for this pathogen
    for suffix in ['fubar_bf', 'fubar_pos_sel', 'fubar']:
        fpath = FEATURE_DIR / f'{pathogen}_{suffix}.csv'
        if fpath.exists():
            df = pd.read_csv(fpath)
            return len(df)
    return None


def convert_eve_scores(protein_name, pathogen):
    """Convert EVE all-singles output to per-position feature CSV."""
    # Find the EVE output file
    eve_csv = EVE_SCORES_DIR / f'{protein_name}_20000_samples.csv'
    if not eve_csv.exists():
        print(f'  SKIP: {eve_csv} not found')
        return False

    df = pd.read_csv(eve_csv)
    # Remove 'wt' row
    df = df[df['mutations'] != 'wt'].copy()

    if len(df) == 0:
        print(f'  SKIP: no valid mutations for {protein_name}')
        return False

    # Parse positions from mutation strings (e.g., A123G -> 123)
    positions = []
    for mut in df['mutations']:
        # Handle multi-mutations (colon-separated)
        parts = mut.split(':')
        # Use first mutation's position
        m = re.match(r'[A-Z](\d+)[A-Z]', parts[0])
        if m:
            positions.append(int(m.group(1)))
        else:
            positions.append(None)
    df['position_raw'] = positions
    df = df.dropna(subset=['position_raw'])
    df['position_raw'] = df['position_raw'].astype(int)

    # Compute mean |evol_indices| per raw position
    pos_scores = df.groupby('position_raw')['evol_indices'].apply(
        lambda x: np.mean(np.abs(x))
    ).reset_index()
    pos_scores.columns = ['position_raw', 'score']

    # Determine target length from existing features
    n_pos = get_feature_length(pathogen)
    if n_pos is None:
        n_pos = get_seq_length_from_msa(protein_name)
    if n_pos is None:
        # Fallback: use max position
        n_pos = int(pos_scores['position_raw'].max()) + 1
        print(f'  WARNING: no reference length found, using max position: {n_pos}')

    # Map raw positions (1-indexed from MSA) to 0-indexed
    # EVE positions start from focus_start_loc in MSA header
    min_pos = int(pos_scores['position_raw'].min())

    # Create output array
    arr = np.zeros(n_pos, dtype=float)
    for _, row in pos_scores.iterrows():
        idx = int(row['position_raw']) - min_pos  # 0-indexed
        if 0 <= idx < n_pos:
            arr[idx] = row['score']

    out_df = pd.DataFrame({
        'position': range(n_pos),
        'fubar_score': arr,
    })

    out_path = FEATURE_DIR / f'{pathogen}_eve.csv'
    out_df.to_csv(out_path, index=False)
    print(f'  SAVED: {out_path} ({n_pos} positions, {len(pos_scores)} with scores)')
    return True


def main():
    FEATURE_DIR.mkdir(parents=True, exist_ok=True)

    success = 0
    for protein_name, pathogen in PROTEIN_TO_PATHOGEN.items():
        print(f'Processing {protein_name} -> {pathogen}')
        if convert_eve_scores(protein_name, pathogen):
            success += 1

    print(f'\nDone: {success}/{len(PROTEIN_TO_PATHOGEN)} proteins converted')


if __name__ == '__main__':
    main()
