#!/usr/bin/env python3
"""Add FUBAR positive selection scores to feature matrices and re-run Stage 3."""

import sys, os, json
import numpy as np
import pandas as pd
from pathlib import Path
from math import sqrt

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from tools.mutbench.ground_truth.multilayer_gt import get_gt_adaptive
from scripts.run_extended_benchmark import (
    WaveletDetector, AdaptivePercentileDetector,
    FrequencyThresholdDetector, MutClustOriginalDetector,
    compute_mcc, compute_f1, postprocess,
)

import warnings
warnings.filterwarnings('ignore')

FEATURE_DIR = Path(__file__).parent.parent / 'results' / 'mutbench' / 'feature_analysis'
RESULTS_DIR = Path(__file__).parent.parent / 'results' / 'mutbench'

PATHOGEN_FUBAR = {
    'SARS-CoV-2': 'data/ncbi_temporal/sars2_spike_codon_aln.fasta.FUBAR.json',
    'H3N2': 'data/influenza/h3n2_ha_codon_aln.fasta.FUBAR.json',
    'Norovirus': 'data/norovirus/norovirus_vp1_codon_aln.fasta.FUBAR.json',
    'HIV-1': 'data/hiv/hiv1_gp120_codon_aln.fasta.FUBAR.json',
    'Dengue': 'data/dengue/dengue_e_codon_aln.fasta.FUBAR.json',
    'RSV': 'data/rsv/rsv_f_codon_aln.fasta.FUBAR.json',
    'Influenza_B': 'data/influenza/influenza_b_ha_codon_aln.fasta.FUBAR.json',
    'MERS': 'data/mers/mers_spike_codon_aln.fasta.FUBAR.json',
    'HCV': 'data/hcv/hcv_e2_codon_aln.fasta.FUBAR.json',
    'Rabies': 'data/rabies/rabies_g_codon_aln.fasta.FUBAR.json',
    'EV-A71': 'data/enterovirus/eva71_vp1_codon_aln.fasta.FUBAR.json',
}

PATHOGENS = list(PATHOGEN_FUBAR.keys())


def parse_fubar(json_path, n_positions):
    """Parse FUBAR JSON and return arrays aligned to n_positions.

    Returns dict with:
      fubar_beta_alpha: beta - alpha (positive = positive selection signal)
      fubar_prob_pos: Prob[alpha<beta] (posterior prob of positive selection)
      fubar_bf: BayesFactor[alpha<beta] (Bayes factor for positive selection)
    """
    with open(json_path) as f:
        d = json.load(f)

    rows = d['MLE']['content']['0']
    n_codons = len(rows)

    # Extract columns: alpha(0), beta(1), beta-alpha(2), Prob[pos](4), BF(5)
    beta_alpha = np.array([r[2] for r in rows])  # beta - alpha
    prob_pos = np.array([r[4] for r in rows])     # Prob[alpha<beta]
    bf = np.array([r[5] for r in rows])           # BayesFactor

    # Align to protein positions (truncate or pad)
    def align(arr):
        if len(arr) >= n_positions:
            return arr[:n_positions]
        else:
            return np.pad(arr, (0, n_positions - len(arr)), constant_values=0)

    return {
        'fubar_beta_alpha': align(beta_alpha),
        'fubar_prob_pos': align(prob_pos),
        'fubar_bf': align(bf),
    }


def normalize_01(arr):
    mn, mx = np.nanmin(arr), np.nanmax(arr)
    if mx - mn == 0:
        return np.zeros_like(arr)
    return (arr - mn) / (mx - mn)


def build_scorings(df, fubar_data):
    """Build all scoring arrays including FUBAR-based ones."""
    scorings = {}

    freq = df['freq'].values
    entropy = df['entropy'].values
    rare_freq = df['rare_freq'].values
    homoplasy = df['homoplasy'].values
    esm2_llr = df['esm2_llr'].values
    plddt = df['plddt'].values
    sasa = df['sasa'].values
    grantham = df['grantham'].values
    dnds_proxy = df['dnds_proxy'].values
    semantic_change = df['semantic_change'].values

    # Original 13 scorings
    scorings['freq'] = freq
    scorings['entropy'] = entropy
    scorings['rare_freq'] = rare_freq
    scorings['H-score'] = np.log2(freq * entropy * 100 + 1)
    scorings['homoplasy'] = homoplasy
    scorings['esm2_llr'] = esm2_llr
    plddt_max = np.max(plddt) if np.max(plddt) > 0 else 1.0
    scorings['plddt_inv'] = plddt_max - plddt
    scorings['sasa'] = sasa
    scorings['grantham'] = grantham
    scorings['dnds_proxy'] = dnds_proxy
    scorings['semantic_change'] = semantic_change
    scorings['EVEscape_composite'] = normalize_01(esm2_llr) * normalize_01(sasa) * normalize_01(grantham)
    plddt_inv = plddt_max - plddt
    features_for_eq = [freq, entropy, rare_freq, homoplasy, esm2_llr,
                       plddt_inv, sasa, grantham, dnds_proxy, semantic_change]
    normed = np.array([normalize_01(f) for f in features_for_eq])
    scorings['EqualWeight'] = np.mean(normed, axis=0)

    # Additional scorings from previous runs
    if 'tranception' in df.columns:
        scorings['tranception'] = df['tranception'].values
    if 'stability' in df.columns:
        scorings['stability'] = df['stability'].values
    if 'stability_structural' in df.columns:
        scorings['stability_structural'] = df['stability_structural'].values
    if 'freq_with_indel' in df.columns:
        scorings['freq_with_indel'] = df['freq_with_indel'].values
    if 'entropy_with_indel' in df.columns:
        scorings['entropy_with_indel'] = df['entropy_with_indel'].values

    # NEW: FUBAR-based scorings
    if fubar_data:
        # FUBAR positive selection: max(beta-alpha, 0) — only positive selection signal
        ba = fubar_data['fubar_beta_alpha']
        scorings['fubar_pos_sel'] = np.maximum(ba, 0)

        # FUBAR posterior probability of positive selection
        scorings['fubar_prob'] = fubar_data['fubar_prob_pos']

        # FUBAR Bayes Factor for positive selection
        scorings['fubar_bf'] = fubar_data['fubar_bf']

    return scorings


def get_detectors():
    return [
        WaveletDetector(threshold=1.0),
        AdaptivePercentileDetector(),
        FrequencyThresholdDetector(percentile=80),
        MutClustOriginalDetector(gamma=10, d=3, minpts=5),
    ]


def main():
    RESULTS_DIR.mkdir(parents=True, exist_ok=True)
    detectors = get_detectors()
    all_results = []

    for pathogen in PATHOGENS:
        fpath = FEATURE_DIR / f'feature_matrix_{pathogen}.csv'
        if not fpath.exists():
            print(f"[SKIP] {pathogen}: feature matrix not found")
            continue

        df = pd.read_csv(fpath)
        n_pos = len(df)

        gt_set = get_gt_adaptive(pathogen, n_pos)
        if not gt_set:
            print(f"[SKIP] {pathogen}: no Layer A ground truth")
            continue

        # Parse FUBAR
        fubar_path = PATHOGEN_FUBAR.get(pathogen)
        fubar_data = None
        if fubar_path and os.path.exists(fubar_path):
            try:
                fubar_data = parse_fubar(fubar_path, n_pos)
                print(f"{pathogen}: FUBAR loaded ({n_pos} positions)")
            except Exception as e:
                print(f"{pathogen}: FUBAR parse error: {e}")

        scorings = build_scorings(df, fubar_data)

        print(f"{pathogen}: {n_pos} pos, {len(gt_set)} GT, {len(scorings)} scorings")

        for scoring_name, scores in scorings.items():
            if np.all(scores == 0) or np.all(np.isnan(scores)):
                continue

            # Replace NaN with 0
            scores = np.nan_to_num(scores, nan=0.0)

            for det in detectors:
                try:
                    detected_raw, _ = det.detect(scores)
                    detected = postprocess(detected_raw, n_pos)
                except Exception:
                    continue

                if len(detected) == 0:
                    mcc, prec, rec, f1 = 0.0, 0.0, 0.0, 0.0
                else:
                    mcc = compute_mcc(detected, gt_set, n_pos)
                    prec, rec, f1 = compute_f1(detected, gt_set, n_pos)

                all_results.append({
                    'pathogen': pathogen,
                    'scoring': scoring_name,
                    'detector': det.name,
                    'mcc': round(mcc, 6),
                    'precision': round(prec, 6),
                    'recall': round(rec, 6),
                    'f1': round(f1, 6),
                    'n_detected': len(detected),
                })

    df_results = pd.DataFrame(all_results)
    out_path = RESULTS_DIR / 'stage3_results.csv'
    df_results.to_csv(out_path, index=False)
    print(f"\nSaved {len(df_results)} evaluations to {out_path}")

    # Summary
    if len(df_results) > 0:
        print(f"\nMean MCC per scoring:")
        summary = df_results.groupby('scoring')['mcc'].agg(['mean', 'std']).sort_values('mean', ascending=False)
        for s, row in summary.iterrows():
            print(f"  {s:25s}  mean={row['mean']:.4f}  std={row['std']:.4f}")

        print(f"\nBest combo per pathogen:")
        for p in df_results['pathogen'].unique():
            pdf = df_results[df_results['pathogen'] == p]
            best = pdf.loc[pdf['mcc'].idxmax()]
            print(f"  {p:15s}: {best['scoring']:25s} + {best['detector']:30s}  MCC={best['mcc']:.4f}")


if __name__ == '__main__':
    main()
