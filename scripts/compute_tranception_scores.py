#!/usr/bin/env python3
"""
Compute per-site ESM-2 pseudo-perplexity (masked marginal) scores for 12 pathogens.

This is DIFFERENT from the existing esm2_llr feature which uses wild-type marginal
scoring (single forward pass, no masking). Here we:
  1. Mask each position one at a time
  2. Forward pass through ESM-2
  3. Record -log P(true_aa | masked context) = pseudo-perplexity per site

This is analogous to Tranception-style scoring (autoregressive log-likelihood),
but using ESM-2's masked language model as a proxy.

Output: {pathogen}_tranception.csv with columns: position, tranception_score
"""

import os
import sys
import gc
import numpy as np
import pandas as pd
from pathlib import Path
from collections import Counter

import torch
import esm

PROJECT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

RESULTS_DIR = PROJECT_ROOT / 'results' / 'mutbench' / 'feature_analysis'
DATA_DIR = PROJECT_ROOT / 'data'

PATHOGENS = {
    'SARS-CoV-2': DATA_DIR / 'ncbi_temporal' / 'spike_2020_H1.fasta',
    'H3N2': DATA_DIR / 'influenza' / 'h3n2_ha_sequences.fasta',
    'Norovirus': DATA_DIR / 'norovirus' / 'norovirus_vp1_sequences.fasta',
    'HIV-1': DATA_DIR / 'hiv' / 'hiv1_gp120_sequences.fasta',
    'Dengue': DATA_DIR / 'dengue' / 'dengue_e_sequences.fasta',
    'RSV': DATA_DIR / 'rsv' / 'rsv_f_sequences.fasta',
    'Influenza_B': DATA_DIR / 'influenza' / 'influenza_b_ha_sequences.fasta',
    'MERS': DATA_DIR / 'mers' / 'mers_spike_sequences.fasta',
    'HCV': DATA_DIR / 'hcv' / 'hcv_e2_sequences.fasta',
    'Zika': DATA_DIR / 'zika' / 'zika_e_sequences.fasta',
    'Rabies': DATA_DIR / 'rabies' / 'rabies_g_sequences.fasta',
    'EV-A71': DATA_DIR / 'enterovirus' / 'eva71_vp1_sequences.fasta',
}

ESM_MAX_LEN = 1022
OVERLAP = 256
BATCH_SIZE = 10  # Number of masked variants per batch


def load_fasta(path):
    """Load FASTA sequences, return list of strings."""
    sequences = []
    current = []
    with open(path) as f:
        for line in f:
            line = line.strip()
            if line.startswith('>'):
                if current:
                    sequences.append(''.join(current))
                    current = []
            else:
                current.append(line)
    if current:
        sequences.append(''.join(current))
    return sequences


def build_consensus(sequences, max_len):
    """Build consensus protein sequence from MSA."""
    consensus = []
    for pos in range(max_len):
        aa_counts = Counter()
        for seq in sequences:
            if pos < len(seq):
                aa = seq[pos]
                if aa not in ('-', '.', 'X', '*'):
                    aa_counts[aa] += 1
        if aa_counts:
            consensus.append(aa_counts.most_common(1)[0][0])
        else:
            consensus.append('A')
    return ''.join(consensus)


def compute_masked_ppl_single(model, alphabet, batch_converter, sequence, device):
    """Compute masked pseudo-perplexity for a sequence <= ESM_MAX_LEN.

    For each position i, mask it, forward pass, get -log P(true_aa | context).
    Uses batching to mask multiple positions per forward pass for efficiency.
    """
    seq_len = len(sequence)
    scores = np.zeros(seq_len)

    # Get token indices for the wild-type sequence
    data = [("protein", sequence)]
    _, _, wt_tokens = batch_converter(data)
    wt_tokens = wt_tokens.to(device)

    mask_idx = alphabet.mask_idx

    # Process in batches of positions
    for batch_start in range(0, seq_len, BATCH_SIZE):
        batch_end = min(batch_start + BATCH_SIZE, seq_len)
        batch_positions = list(range(batch_start, batch_end))
        n_batch = len(batch_positions)

        # Create masked token tensors for this batch
        # Each element masks a different position
        masked_batch = wt_tokens.repeat(n_batch, 1)  # (n_batch, seq_len+2)
        for i, pos in enumerate(batch_positions):
            masked_batch[i, pos + 1] = mask_idx  # +1 for BOS token

        with torch.no_grad():
            results = model(masked_batch, repr_layers=[], return_contacts=False)
            logits = results["logits"]  # (n_batch, seq_len+2, vocab_size)

        log_probs = torch.log_softmax(logits, dim=-1)

        for i, pos in enumerate(batch_positions):
            aa = sequence[pos]
            token_idx = alphabet.get_idx(aa)
            # Score = -log P(true_aa | masked context)
            scores[pos] = -log_probs[i, pos + 1, token_idx].item()

    return scores


def compute_masked_ppl_sliding(model, alphabet, batch_converter, sequence, device):
    """Masked pseudo-perplexity for long sequences using sliding window."""
    seq_len = len(sequence)
    if seq_len <= ESM_MAX_LEN:
        return compute_masked_ppl_single(model, alphabet, batch_converter, sequence, device)

    scores_sum = np.zeros(seq_len)
    counts = np.zeros(seq_len)
    step = ESM_MAX_LEN - OVERLAP

    starts = list(range(0, seq_len - ESM_MAX_LEN + 1, step))
    if starts[-1] + ESM_MAX_LEN < seq_len:
        starts.append(seq_len - ESM_MAX_LEN)

    for start in starts:
        end = start + ESM_MAX_LEN
        window_seq = sequence[start:end]
        window_scores = compute_masked_ppl_single(
            model, alphabet, batch_converter, window_seq, device
        )
        scores_sum[start:end] += window_scores
        counts[start:end] += 1

    counts[counts == 0] = 1
    return scores_sum / counts


def main():
    device = 'cuda' if torch.cuda.is_available() else 'cpu'
    print(f"Device: {device}")
    if device == 'cuda':
        print(f"  GPU: {torch.cuda.get_device_name(0)}")
        mem_gb = torch.cuda.get_device_properties(0).total_memory / 1e9
        print(f"  Memory: {mem_gb:.1f} GB")

    RESULTS_DIR.mkdir(parents=True, exist_ok=True)

    # Load ESM-2 650M
    print("\nLoading ESM-2 650M model...")
    model, alphabet = esm.pretrained.esm2_t33_650M_UR50D()
    batch_converter = alphabet.get_batch_converter()
    model = model.eval()
    model = model.to(device)
    print("  Model loaded.")

    summary_rows = []

    for pathogen, fasta_path in PATHOGENS.items():
        out_path = RESULTS_DIR / f'{pathogen}_tranception.csv'

        # Check cache
        if out_path.exists():
            existing = pd.read_csv(out_path)
            print(f"\n[CACHED] {pathogen}: {len(existing)} positions (skipping)")
            summary_rows.append({
                'pathogen': pathogen,
                'n_positions': len(existing),
                'mean_score': existing['tranception_score'].mean(),
                'std_score': existing['tranception_score'].std(),
                'status': 'cached',
            })
            continue

        if not fasta_path.exists():
            print(f"\n[SKIP] {pathogen}: {fasta_path} not found")
            continue

        print(f"\n[COMPUTE] {pathogen}...")

        # Build consensus
        sequences = load_fasta(str(fasta_path))
        min_len = min(len(s) for s in sequences)
        sequences = [s[:min_len] for s in sequences]
        consensus = build_consensus(sequences, min_len)
        print(f"  Consensus length: {len(consensus)}")

        # Compute masked pseudo-perplexity
        if len(consensus) > ESM_MAX_LEN:
            n_windows = (len(consensus) - OVERLAP) // (ESM_MAX_LEN - OVERLAP) + 1
            print(f"  Using sliding window ({n_windows} windows)")
            scores = compute_masked_ppl_sliding(
                model, alphabet, batch_converter, consensus, device
            )
        else:
            print(f"  Single pass (len={len(consensus)} <= {ESM_MAX_LEN})")
            scores = compute_masked_ppl_single(
                model, alphabet, batch_converter, consensus, device
            )

        # Save
        df = pd.DataFrame({
            'position': range(len(scores)),
            'tranception_score': scores,
        })
        df.to_csv(out_path, index=False)
        print(f"  Saved to {out_path}")
        print(f"  Stats: mean={scores.mean():.4f}, std={scores.std():.4f}, "
              f"min={scores.min():.4f}, max={scores.max():.4f}")

        summary_rows.append({
            'pathogen': pathogen,
            'n_positions': len(scores),
            'mean_score': scores.mean(),
            'std_score': scores.std(),
            'status': 'computed',
        })

        # Clear GPU cache
        torch.cuda.empty_cache()
        gc.collect()

    # Cleanup
    del model
    torch.cuda.empty_cache()
    gc.collect()

    # Print summary
    print("\n" + "=" * 70)
    print("SUMMARY: ESM-2 Masked Pseudo-Perplexity (Tranception-proxy) Scores")
    print("=" * 70)
    summary_df = pd.DataFrame(summary_rows)
    print(summary_df.to_string(index=False))

    # Correlation with existing esm2_llr
    print("\n\nCorrelation with existing ESM-2 LLR (wild-type marginal):")
    from scipy.stats import spearmanr
    for pathogen in PATHOGENS:
        tranc_path = RESULTS_DIR / f'{pathogen}_tranception.csv'
        feat_path = RESULTS_DIR / f'feature_matrix_{pathogen}.csv'
        if tranc_path.exists() and feat_path.exists():
            tranc = pd.read_csv(tranc_path)
            feat = pd.read_csv(feat_path)
            n = min(len(tranc), len(feat))
            if n > 10:
                rho, pval = spearmanr(
                    tranc['tranception_score'].values[:n],
                    feat['esm2_llr'].values[:n]
                )
                print(f"  {pathogen}: rho={rho:.4f}, p={pval:.2e} (n={n})")

    print("\nDone.")


if __name__ == '__main__':
    main()
