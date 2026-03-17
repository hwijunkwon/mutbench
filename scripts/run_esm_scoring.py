#!/usr/bin/env python3
"""
ESM-2 Protein Language Model scoring for MutBench.

Computes per-position ESM-LLR (log-likelihood ratio) using wild-type marginal
scoring with ESM-2 650M, then evaluates through MutBench detection pipeline.

For proteins > 1022 AA (ESM-2 context limit): sliding window with overlap.

Output:
  - results/mutbench/esm_scores/{pathogen}_esm_llr.npy
  - results/mutbench/esm_benchmark_results.csv
  - results/mutbench/esm_correlation_analysis.csv
"""

import sys
import os
import numpy as np
import pandas as pd
from pathlib import Path
from collections import Counter
from scipy import stats as sp_stats
import warnings
import gc

warnings.filterwarnings('ignore')

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Reuse existing MutBench infrastructure
from scripts.run_extended_benchmark import (
    load_fasta, compute_features, compute_scores,
    postprocess, compute_mcc, compute_f1, compute_enrichment,
    WaveletDetector, KDEDetector, SlidingWindowTest,
    GradientPeakDetector, LocalContrastDetector, CUSUMDetector,
    AdaptivePercentileDetector, ScoreDBSCANDetector, SpectralFilterDetector,
    BayesianDetector, EnsembleVoteDetector, AdaptiveWindowDetector,
    FrequencyThresholdDetector, SWANDetector, MutClustOriginalDetector,
)

from tools.mutbench.ground_truth.multilayer_gt import (
    get_gt_adaptive, get_gt_constrained,
    get_gt_dms, load_bloom_preferences, load_sars2_fitness,
)

DATA_DIR = Path(__file__).parent.parent / 'data'
RESULTS_DIR = Path(__file__).parent.parent / 'results' / 'mutbench'
ESM_DIR = RESULTS_DIR / 'esm_scores'

PATHOGENS = {
    'SARS-CoV-2': DATA_DIR / 'ncbi_temporal' / 'spike_2020_H1.fasta',
    'H3N2': DATA_DIR / 'influenza' / 'h3n2_ha_sequences.fasta',
    'Norovirus': DATA_DIR / 'norovirus' / 'norovirus_vp1_sequences.fasta',
    'HIV-1': DATA_DIR / 'cross_pathogen' / 'hiv1_gp120_sequences.fasta',
    'Dengue': DATA_DIR / 'dengue' / 'dengue_e_sequences.fasta',
    'RSV': DATA_DIR / 'rsv' / 'rsv_f_sequences.fasta',
    'Influenza_B': DATA_DIR / 'influenza' / 'influenza_b_ha_sequences.fasta',
    'MERS': DATA_DIR / 'mers' / 'mers_spike_sequences.fasta',
    'HCV': DATA_DIR / 'hcv' / 'hcv_e2_sequences.fasta',
}

DMS_FILES = {
    'SARS-CoV-2': ('sars2', DATA_DIR / 'mutbench' / 'aamut_fitness_all.csv'),
    'HIV-1': ('bloom_prefs', DATA_DIR / 'dms' / 'hiv1_env_prefs_BG505.csv'),
    'H3N2': ('bloom_prefs', DATA_DIR / 'dms' / 'h3n2_ha_prefs_Perth2009.csv'),
    'RSV': ('bloom_prefs', DATA_DIR / 'dms' / 'rsv_f_mutation_effects.csv'),
}

ESM_MAX_LEN = 1022  # ESM-2 context window (excluding BOS/EOS tokens)
OVERLAP = 256


# -------------------------------------------------------------------------
# ESM-2 scoring
# -------------------------------------------------------------------------

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
            consensus.append('A')  # fallback
    return ''.join(consensus)


def compute_esm_llr_single(model, alphabet, batch_converter, sequence, device):
    """Compute ESM-LLR for a single sequence that fits within context window.

    ESM-LLR[i] = -log P(wt_aa_i | context)
    using wild-type marginal scoring (single forward pass).

    Returns 1D array of length len(sequence).
    """
    import torch

    data = [("protein", sequence)]
    _, _, batch_tokens = batch_converter(data)
    batch_tokens = batch_tokens.to(device)

    with torch.no_grad():
        results = model(batch_tokens, repr_layers=[], return_contacts=False)
        logits = results["logits"]  # (1, seq_len+2, vocab_size) including BOS/EOS

    # log_softmax over vocabulary dimension
    log_probs = torch.log_softmax(logits, dim=-1)

    # Extract wt token log-probabilities (skip BOS token at position 0)
    llr = np.zeros(len(sequence))
    for i, aa in enumerate(sequence):
        token_idx = alphabet.get_idx(aa)
        # Position i in sequence corresponds to position i+1 in tokens (after BOS)
        llr[i] = -log_probs[0, i + 1, token_idx].item()

    return llr


def compute_esm_llr_sliding(model, alphabet, batch_converter, sequence, device):
    """Compute ESM-LLR for long sequences using sliding window.

    For sequences > ESM_MAX_LEN, use overlapping windows and average
    scores in overlap regions.
    """
    seq_len = len(sequence)
    if seq_len <= ESM_MAX_LEN:
        return compute_esm_llr_single(model, alphabet, batch_converter, sequence, device)

    # Sliding window
    scores_sum = np.zeros(seq_len)
    counts = np.zeros(seq_len)
    step = ESM_MAX_LEN - OVERLAP

    starts = list(range(0, seq_len - ESM_MAX_LEN + 1, step))
    # Ensure last window covers the end
    if starts[-1] + ESM_MAX_LEN < seq_len:
        starts.append(seq_len - ESM_MAX_LEN)

    for start in starts:
        end = start + ESM_MAX_LEN
        window_seq = sequence[start:end]
        window_llr = compute_esm_llr_single(model, alphabet, batch_converter, window_seq, device)
        scores_sum[start:end] += window_llr
        counts[start:end] += 1

    # Average overlapping regions
    counts[counts == 0] = 1
    return scores_sum / counts


def compute_esm_scores(pathogens_consensus, device='cuda'):
    """Compute ESM-LLR for all pathogens."""
    import torch
    import esm

    print("Loading ESM-2 650M model...")
    model, alphabet = esm.pretrained.esm2_t33_650M_UR50D()
    batch_converter = alphabet.get_batch_converter()
    model = model.eval()
    model = model.to(device)
    print(f"  Model loaded on {device}")

    esm_results = {}
    for pathogen, consensus in pathogens_consensus.items():
        print(f"\n  Computing ESM-LLR for {pathogen} (len={len(consensus)})...")

        if len(consensus) > ESM_MAX_LEN:
            print(f"    Using sliding window (windows needed: "
                  f"{(len(consensus) - OVERLAP) // (ESM_MAX_LEN - OVERLAP) + 1})")
            llr = compute_esm_llr_sliding(model, alphabet, batch_converter, consensus, device)
        else:
            llr = compute_esm_llr_single(model, alphabet, batch_converter, consensus, device)

        # Save
        save_path = ESM_DIR / f"{pathogen}_esm_llr.npy"
        np.save(save_path, llr)
        print(f"    Saved to {save_path}")
        print(f"    Stats: mean={llr.mean():.4f}, std={llr.std():.4f}, "
              f"min={llr.min():.4f}, max={llr.max():.4f}")

        esm_results[pathogen] = llr

        # Clear GPU cache
        torch.cuda.empty_cache()
        gc.collect()

    # Clean up model
    del model
    torch.cuda.empty_cache()
    gc.collect()

    return esm_results


def load_dms_scores(pathogen):
    """Load DMS position scores for a pathogen (if available)."""
    if pathogen not in DMS_FILES:
        return {}
    dtype, path = DMS_FILES[pathogen]
    if not path.exists():
        return {}
    try:
        if dtype == 'sars2':
            return load_sars2_fitness(str(path))
        else:
            return load_bloom_preferences(str(path))
    except Exception as e:
        print(f"  [WARN] DMS load failed for {pathogen}: {e}")
        return {}


def get_detectors():
    """Return all detectors (same as multilayer benchmark)."""
    return [
        WaveletDetector(threshold=1.0),
        WaveletDetector(threshold=1.5),
        WaveletDetector(threshold=2.0),
        KDEDetector(threshold_pct=75),
        KDEDetector(threshold_pct=80),
        KDEDetector(threshold_pct=85),
        SlidingWindowTest(p_threshold=0.01),
        SlidingWindowTest(p_threshold=0.05),
        GradientPeakDetector(min_prominence=0.2),
        GradientPeakDetector(min_prominence=0.5),
        LocalContrastDetector(z_thresh=1.0),
        LocalContrastDetector(z_thresh=1.5),
        LocalContrastDetector(z_thresh=2.0),
        CUSUMDetector(drift=0.3, h_factor=3.0),
        CUSUMDetector(drift=0.5, h_factor=4.0),
        CUSUMDetector(drift=0.5, h_factor=5.0),
        AdaptivePercentileDetector(),
        ScoreDBSCANDetector(eps_pos=8, min_pts=3),
        ScoreDBSCANDetector(eps_pos=15, min_pts=3),
        SpectralFilterDetector(z_thresh=1.5),
        SpectralFilterDetector(z_thresh=2.0),
        BayesianDetector(prior_hotspot=0.1, threshold=0.5),
        BayesianDetector(prior_hotspot=0.15, threshold=0.4),
        EnsembleVoteDetector(min_votes=2),
        EnsembleVoteDetector(min_votes=3),
        AdaptiveWindowDetector(seed_pct=90, expand_thresh=0.5),
        AdaptiveWindowDetector(seed_pct=85, expand_thresh=0.4),
        FrequencyThresholdDetector(percentile=80),
        FrequencyThresholdDetector(percentile=85),
        FrequencyThresholdDetector(percentile=90),
        FrequencyThresholdDetector(percentile=95),
        SWANDetector(window_size=10, k=1.0),
        SWANDetector(window_size=10, k=1.5),
        SWANDetector(window_size=10, k=2.0),
        SWANDetector(window_size=20, k=1.0),
        SWANDetector(window_size=20, k=1.5),
        SWANDetector(window_size=20, k=2.0),
        SWANDetector(window_size=50, k=1.0),
        SWANDetector(window_size=50, k=1.5),
        SWANDetector(window_size=50, k=2.0),
        MutClustOriginalDetector(gamma=10, d=3, minpts=5),
    ]


# -------------------------------------------------------------------------
# Main pipeline
# -------------------------------------------------------------------------

def main():
    import torch

    ESM_DIR.mkdir(parents=True, exist_ok=True)

    device = 'cuda' if torch.cuda.is_available() else 'cpu'
    print(f"Device: {device}")
    if device == 'cuda':
        print(f"  GPU: {torch.cuda.get_device_name(0)}")
        print(f"  Memory: {torch.cuda.get_device_properties(0).total_memory / 1e9:.1f} GB")

    # ---- Step 1: Build consensus sequences and compute ESM-LLR ----
    print("\n" + "=" * 60)
    print("STEP 1: Building consensus sequences and computing ESM-LLR")
    print("=" * 60)

    pathogens_consensus = {}
    pathogens_seqlen = {}

    for pathogen, fasta_path in PATHOGENS.items():
        if not fasta_path.exists():
            print(f"  [SKIP] {fasta_path} not found")
            continue
        sequences = load_fasta(str(fasta_path))
        min_len = min(len(s) for s in sequences)
        sequences = [s[:min_len] for s in sequences]
        consensus = build_consensus(sequences, min_len)
        pathogens_consensus[pathogen] = consensus
        pathogens_seqlen[pathogen] = min_len
        print(f"  {pathogen}: consensus len={len(consensus)}")

    # Check for cached ESM scores
    cached = {}
    for pathogen in pathogens_consensus:
        cache_path = ESM_DIR / f"{pathogen}_esm_llr.npy"
        if cache_path.exists():
            cached[pathogen] = np.load(cache_path)
            print(f"  {pathogen}: loaded from cache")

    to_compute = {k: v for k, v in pathogens_consensus.items() if k not in cached}

    if to_compute:
        new_scores = compute_esm_scores(to_compute, device=device)
        esm_scores = {**cached, **new_scores}
    else:
        esm_scores = cached
        print("  All ESM scores loaded from cache")

    # ---- Step 2: Run detection pipeline ----
    print("\n" + "=" * 60)
    print("STEP 2: Running ESM-LLR through detection pipeline")
    print("=" * 60)

    detectors = get_detectors()
    all_results = []

    for pathogen in esm_scores:
        llr = esm_scores[pathogen]
        seq_len = pathogens_seqlen[pathogen]

        # Load ground truth
        gt_adaptive = get_gt_adaptive(pathogen, seq_len)
        gt_constrained = get_gt_constrained(pathogen, seq_len)
        dms_pos_scores = load_dms_scores(pathogen)
        gt_dms = get_gt_dms(dms_pos_scores) if dms_pos_scores else set()

        print(f"\n  {pathogen}: GT_A={len(gt_adaptive)}, GT_B={len(gt_constrained)}, "
              f"GT_C={len(gt_dms)}")

        if not gt_adaptive:
            continue

        for det in detectors:
            try:
                detected_raw, _ = det.detect(llr)
                detected = postprocess(detected_raw, seq_len)
                detected_set = set(detected)
            except Exception:
                continue

            if len(detected) == 0:
                continue

            mcc_a = compute_mcc(detected, gt_adaptive, seq_len)
            p_a, r_a, f1_a = compute_f1(detected, gt_adaptive, seq_len)
            enrich_a = compute_enrichment(detected, gt_adaptive, seq_len)

            constrained_fpr = 0.0
            if gt_constrained:
                constrained_fpr = len(detected_set & gt_constrained) / len(gt_constrained)

            dms_f1 = np.nan
            if gt_dms:
                _, _, dms_f1 = compute_f1(detected, gt_dms, seq_len)

            composite = f1_a - 0.3 * constrained_fpr

            all_results.append({
                'pathogen': pathogen,
                'score': 'ESM-LLR',
                'detector': det.name,
                'family': det.family,
                'seq_length': seq_len,
                'gt_adaptive_size': len(gt_adaptive),
                'gt_constrained_size': len(gt_constrained),
                'gt_dms_size': len(gt_dms),
                'mcc_adaptive': round(mcc_a, 4),
                'f1_adaptive': round(f1_a, 4),
                'precision_adaptive': round(p_a, 4),
                'recall_adaptive': round(r_a, 4),
                'enrichment_adaptive': round(enrich_a, 4),
                'constrained_fpr': round(constrained_fpr, 4),
                'dms_f1': round(dms_f1, 4) if not np.isnan(dms_f1) else np.nan,
                'composite_score': round(composite, 4),
                'n_detected': len(detected),
            })

    esm_df = pd.DataFrame(all_results)
    esm_path = RESULTS_DIR / 'esm_benchmark_results.csv'
    esm_df.to_csv(esm_path, index=False)
    print(f"\n  Saved {len(esm_df)} ESM evaluations to {esm_path}")

    # ---- Step 3: Compare with existing 9 scoring results ----
    print("\n" + "=" * 60)
    print("STEP 3: Comparison with existing scoring methods")
    print("=" * 60)

    existing_path = RESULTS_DIR / 'multilayer_9pathogen_results.csv'
    if existing_path.exists():
        existing_df = pd.read_csv(existing_path)
        print(f"  Loaded {len(existing_df)} existing evaluations")

        comparison_rows = []
        for pathogen in esm_df['pathogen'].unique():
            # Best ESM-LLR
            esm_pat = esm_df[esm_df['pathogen'] == pathogen]
            if len(esm_pat) == 0:
                continue
            best_esm_idx = esm_pat['mcc_adaptive'].idxmax()
            best_esm = esm_pat.loc[best_esm_idx]

            # Best existing per scoring
            exist_pat = existing_df[existing_df['pathogen'] == pathogen]
            if len(exist_pat) == 0:
                continue

            # Overall best existing
            best_exist_idx = exist_pat['mcc_adaptive'].idxmax()
            best_exist = exist_pat.loc[best_exist_idx]

            # Best per scoring formula
            scoring_bests = {}
            for score_name in exist_pat['score'].unique():
                score_pat = exist_pat[exist_pat['score'] == score_name]
                if len(score_pat) > 0:
                    best_idx = score_pat['mcc_adaptive'].idxmax()
                    scoring_bests[score_name] = score_pat.loc[best_idx, 'mcc_adaptive']

            # Rank ESM-LLR among scoring methods
            all_best_mccs = list(scoring_bests.values()) + [best_esm['mcc_adaptive']]
            all_best_mccs_sorted = sorted(all_best_mccs, reverse=True)
            esm_rank = all_best_mccs_sorted.index(best_esm['mcc_adaptive']) + 1

            row = {
                'pathogen': pathogen,
                'esm_best_mcc': best_esm['mcc_adaptive'],
                'esm_best_detector': best_esm['detector'],
                'existing_best_mcc': best_exist['mcc_adaptive'],
                'existing_best_score': best_exist['score'],
                'existing_best_detector': best_exist['detector'],
                'esm_rank_among_10': esm_rank,
                'esm_vs_best_delta': round(
                    best_esm['mcc_adaptive'] - best_exist['mcc_adaptive'], 4),
            }
            # Add per-scoring-formula best MCCs
            for sname, smcc in scoring_bests.items():
                row[f'best_{sname}'] = smcc

            comparison_rows.append(row)

            print(f"  {pathogen}: ESM-LLR best={best_esm['mcc_adaptive']:.4f} "
                  f"({best_esm['detector']}), "
                  f"Existing best={best_exist['mcc_adaptive']:.4f} "
                  f"({best_exist['score']}+{best_exist['detector']}), "
                  f"ESM rank={esm_rank}/10")

        comp_df = pd.DataFrame(comparison_rows)
        comp_path = RESULTS_DIR / 'esm_comparison_summary.csv'
        comp_df.to_csv(comp_path, index=False)
        print(f"\n  Comparison saved to {comp_path}")

    # ---- Step 4: Correlation analysis ----
    print("\n" + "=" * 60)
    print("STEP 4: Correlation analysis")
    print("=" * 60)

    corr_rows = []
    for pathogen in esm_scores:
        llr = esm_scores[pathogen]
        seq_len = pathogens_seqlen[pathogen]
        fasta_path = PATHOGENS[pathogen]

        # Load sequences and compute MSA-based scores
        sequences = load_fasta(str(fasta_path))
        min_len = min(len(s) for s in sequences)
        sequences = [s[:min_len] for s in sequences]
        features = compute_features(sequences)
        msa_scores = compute_scores(features)

        print(f"\n  {pathogen}:")

        # Correlate ESM-LLR with each MSA-based scoring formula
        for score_name, score_arr in msa_scores.items():
            if np.std(score_arr) == 0 or np.std(llr) == 0:
                continue
            rho, pval = sp_stats.spearmanr(llr[:len(score_arr)], score_arr[:len(llr)])
            corr_rows.append({
                'pathogen': pathogen,
                'comparison': f'ESM-LLR vs {score_name}',
                'spearman_rho': round(rho, 4),
                'p_value': round(pval, 6),
            })
            print(f"    ESM-LLR vs {score_name}: rho={rho:.4f}, p={pval:.4g}")

        # DMS correlation
        dms_pos_scores = load_dms_scores(pathogen)
        if dms_pos_scores:
            # Align positions
            common_pos = sorted(set(dms_pos_scores.keys()) & set(range(len(llr))))
            if len(common_pos) >= 10:
                dms_vals = [dms_pos_scores[p] for p in common_pos]
                esm_vals = [llr[p] for p in common_pos]
                rho_dms, pval_dms = sp_stats.spearmanr(esm_vals, dms_vals)
                corr_rows.append({
                    'pathogen': pathogen,
                    'comparison': 'ESM-LLR vs DMS',
                    'spearman_rho': round(rho_dms, 4),
                    'p_value': round(pval_dms, 6),
                })
                print(f"    ESM-LLR vs DMS: rho={rho_dms:.4f}, p={pval_dms:.4g} "
                      f"(n={len(common_pos)} positions)")

    corr_df = pd.DataFrame(corr_rows)
    corr_path = RESULTS_DIR / 'esm_correlation_analysis.csv'
    corr_df.to_csv(corr_path, index=False)
    print(f"\n  Correlation analysis saved to {corr_path}")

    # ---- Summary ----
    print("\n" + "=" * 60)
    print("SUMMARY")
    print("=" * 60)

    if len(esm_df) > 0:
        print(f"\nTotal ESM evaluations: {len(esm_df)}")
        print(f"\nBest ESM-LLR combo per pathogen:")
        for pathogen in esm_df['pathogen'].unique():
            pat_df = esm_df[esm_df['pathogen'] == pathogen]
            best_idx = pat_df['mcc_adaptive'].idxmax()
            best = pat_df.loc[best_idx]
            print(f"  {pathogen}: {best['detector']} "
                  f"(MCC={best['mcc_adaptive']:.4f}, "
                  f"FPR={best['constrained_fpr']:.4f})")

        # Cross-pathogen mean
        best_per_pathogen = esm_df.groupby('pathogen')['mcc_adaptive'].max()
        print(f"\nMean best MCC across pathogens: {best_per_pathogen.mean():.4f}")
        print(f"Std: {best_per_pathogen.std():.4f}")


if __name__ == '__main__':
    main()
