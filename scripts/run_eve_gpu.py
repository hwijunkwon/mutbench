#!/usr/bin/env python3
"""Run EVE VAE training on GPU for all virus proteins sequentially.

Uses reduced architecture (1000/500/200, z=30) and 100k steps.
Skips Zika (excluded from benchmark).
After training, computes evolutionary indices for all single mutations.
"""

import os
import sys
import subprocess
import time
import json
import numpy as np
import pandas as pd
from pathlib import Path

BASE_DIR = Path('/proj/paper')
EVE_DIR = BASE_DIR / 'tools' / 'EVE'
MSA_DIR = BASE_DIR / 'data' / 'eve_msa'
WEIGHTS_DIR = BASE_DIR / 'data' / 'eve_weights'
RESULTS_DIR = BASE_DIR / 'results' / 'mutbench'
CHECKPOINT_DIR = EVE_DIR / 'results' / 'VAE_parameters'
LOG_DIR = BASE_DIR / 'results' / 'eve_logs'

MAPPING_FILE = MSA_DIR / 'virus_mapping.csv'
MODEL_PARAMS = MSA_DIR / 'virus_model_params.json'

# Skip Zika (too few sequences, excluded from benchmark)
SKIP = {'E_ZIKV'}

# Map EVE protein names to MutBench pathogen names
EVE_TO_PATHOGEN = {
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


def train_vae(protein_index):
    """Train EVE VAE for a single protein."""
    cmd = [
        sys.executable, str(EVE_DIR / 'train_VAE.py'),
        '--MSA_data_folder', str(MSA_DIR),
        '--MSA_list', str(MAPPING_FILE),
        '--protein_index', str(protein_index),
        '--MSA_weights_location', str(WEIGHTS_DIR),
        '--VAE_checkpoint_location', str(CHECKPOINT_DIR),
        '--model_name_suffix', 'virus_v1',
        '--model_parameters_location', str(MODEL_PARAMS),
        '--training_logs_location', str(LOG_DIR),
    ]

    env = os.environ.copy()
    env['CUDA_VISIBLE_DEVICES'] = '0'

    result = subprocess.run(
        cmd, capture_output=True, text=True, env=env,
        cwd=str(EVE_DIR), timeout=3600  # 1 hour max per protein
    )
    return result


def compute_evol_indices(protein_index):
    """Compute evolutionary indices (all single mutations) for a trained model."""
    mapping = pd.read_csv(MAPPING_FILE)
    protein_name = mapping['protein_name'][protein_index]
    model_name = f'{protein_name}_virus_v1'

    cmd = [
        sys.executable, str(EVE_DIR / 'compute_evol_indices.py'),
        '--MSA_data_folder', str(MSA_DIR),
        '--MSA_list', str(MAPPING_FILE),
        '--protein_index', str(protein_index),
        '--MSA_weights_location', str(WEIGHTS_DIR),
        '--VAE_checkpoint_location', str(CHECKPOINT_DIR),
        '--model_name_suffix', 'virus_v1',
        '--model_parameters_location', str(MODEL_PARAMS),
        '--computation_mode', 'all_singles',
        '--all_singles_mutations_folder', str(RESULTS_DIR / 'eve_scores'),
        '--num_samples_compute_evol_indices', '20000',
        '--batch_size_compute_evol_indices', '2048',
    ]

    env = os.environ.copy()
    env['CUDA_VISIBLE_DEVICES'] = '0'

    result = subprocess.run(
        cmd, capture_output=True, text=True, env=env,
        cwd=str(EVE_DIR), timeout=3600
    )
    return result


def eve_to_position_scores(eve_csv_path, n_positions):
    """Convert EVE per-mutation scores to per-position scores.

    Returns array of length n_positions with mean |EVE_score| per position.
    """
    df = pd.read_csv(eve_csv_path)
    scores = np.zeros(n_positions)
    counts = np.zeros(n_positions)

    for _, row in df.iterrows():
        # EVE mutation format: A123G (wt, pos, mut)
        mut = row.get('mutant', row.get('mutation', ''))
        try:
            pos = int(mut[1:-1]) - 1  # 0-indexed
            if 0 <= pos < n_positions:
                val = abs(row.get('evol_indices', row.get('EVE_scores', 0)))
                scores[pos] += val
                counts[pos] += 1
        except (ValueError, IndexError):
            continue

    mask = counts > 0
    scores[mask] /= counts[mask]
    return scores


def main():
    os.makedirs(CHECKPOINT_DIR, exist_ok=True)
    os.makedirs(LOG_DIR, exist_ok=True)
    os.makedirs(RESULTS_DIR / 'eve_scores', exist_ok=True)

    mapping = pd.read_csv(MAPPING_FILE)
    print(f"EVE GPU Training Pipeline")
    print(f"Proteins: {len(mapping)}")
    print(f"Skipping: {SKIP}")
    print()

    for idx in range(len(mapping)):
        protein_name = mapping['protein_name'][idx]

        if protein_name in SKIP:
            print(f"[SKIP] {protein_name}")
            continue

        # Check if already done
        checkpoint = CHECKPOINT_DIR / f'{protein_name}_virus_v1_final'
        if checkpoint.exists():
            print(f"[DONE] {protein_name}: checkpoint exists, skipping training")
        else:
            print(f"[TRAIN] {protein_name}...")
            t0 = time.time()
            result = train_vae(idx)
            elapsed = time.time() - t0
            print(f"  Training completed in {elapsed:.0f}s")

            if result.returncode != 0:
                print(f"  ERROR: {result.stderr[-500:]}")
                continue
            else:
                # Print last few lines of stdout
                lines = result.stdout.strip().split('\n')
                for line in lines[-5:]:
                    print(f"  {line}")

        # Compute evolutionary indices
        eve_score_path = RESULTS_DIR / 'eve_scores' / f'{protein_name}_virus_v1_all_singles.csv'
        if eve_score_path.exists():
            print(f"  Evol indices already computed")
        else:
            print(f"  Computing evolutionary indices...")
            t0 = time.time()
            result = compute_evol_indices(idx)
            elapsed = time.time() - t0
            print(f"  Evol indices computed in {elapsed:.0f}s")

            if result.returncode != 0:
                print(f"  ERROR: {result.stderr[-500:]}")
                continue

        print()

    # Convert EVE scores to per-position scores for stage3
    print("=" * 60)
    print("Converting EVE scores to per-position format...")
    feature_dir = BASE_DIR / 'results' / 'mutbench' / 'feature_analysis'

    for protein_name, pathogen in EVE_TO_PATHOGEN.items():
        eve_csv = RESULTS_DIR / 'eve_scores' / f'{protein_name}_virus_v1_all_singles.csv'
        if not eve_csv.exists():
            print(f"  {pathogen}: no EVE scores found")
            continue

        fm_path = feature_dir / f'feature_matrix_{pathogen}.csv'
        if not fm_path.exists():
            print(f"  {pathogen}: no feature matrix found")
            continue

        fm = pd.read_csv(fm_path)
        n_pos = len(fm)

        pos_scores = eve_to_position_scores(eve_csv, n_pos)
        out_df = pd.DataFrame({
            'position': range(1, n_pos + 1),
            'fubar_score': pos_scores,  # Using same column name for compatibility
        })
        out_path = feature_dir / f'{pathogen}_eve.csv'
        out_df.to_csv(out_path, index=False)
        print(f"  {pathogen}: {np.sum(pos_scores > 0)} positions with EVE signal -> {out_path}")

    print("\nDone!")


if __name__ == '__main__':
    main()
