#!/usr/bin/env python3
"""Vaccine escape enrichment for 20 scoring × 39 detectors × available pathogens.

Computes enrichment ratio and Fisher's exact test for each scoring-detector
combination against known vaccine/antibody escape positions.
"""
import sys, os
import numpy as np
import pandas as pd
from pathlib import Path
from scipy.stats import fisher_exact

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from tools.mutbench.ground_truth.multilayer_gt import get_gt_adaptive
from scripts.run_stage3_full_detectors import (
    build_all_scorings, get_all_detectors, FEATURE_DIR,
)
from scripts.run_extended_benchmark import compute_mcc, postprocess

import warnings
warnings.filterwarnings('ignore')

BASE_DIR = Path(__file__).parent.parent
RESULTS_DIR = BASE_DIR / 'results' / 'mutbench'

# Known escape positions (0-indexed)
ESCAPE_SITES = {
    "SARS-CoV-2": {
        "positions": {
            484, 417, 452, 501, 478, 493, 446, 477, 486, 346,
            614, 681, 655, 679, 969,
            371, 373, 375, 376, 405, 408, 440, 444, 445, 490,
            498, 505, 339, 440, 456, 460, 484, 486, 493,
        },
        "n_total_positions": 1259,
    },
    "H3N2": {
        "positions": {
            122, 124, 126, 131, 133, 135, 137, 142, 143, 144, 145,
            155, 156, 157, 158, 159, 160, 163, 164, 186, 188, 189,
            190, 192, 193, 194, 196, 197, 198,
        },
        "n_total_positions": 543,
    },
    "HIV-1": {
        "positions": {
            130, 132, 133, 134, 135, 136, 137, 138, 139, 140,
            141, 142, 143, 144, 145, 146, 147, 148, 149, 150,
            160, 161, 162, 163, 164, 165, 166, 167, 168, 169,
            170, 171, 172, 173, 174, 175, 176, 177, 178, 179,
            296, 297, 298, 299, 300,
        },
        "n_total_positions": 450,
    },
}


def compute_enrichment(detected_set, escape_set, n_total):
    n_detected = len(detected_set)
    n_escape = len(escape_set)
    overlap = len(detected_set & escape_set)

    if n_detected == 0 or n_escape == 0:
        return 0.0, 1.0, overlap

    obs_rate = overlap / n_detected
    exp_rate = n_escape / n_total
    enrichment = obs_rate / exp_rate if exp_rate > 0 else 0.0

    a = overlap
    b = n_detected - overlap
    c = n_escape - overlap
    d = n_total - n_detected - c
    _, p_value = fisher_exact([[a, b], [max(0, c), max(0, d)]], alternative="greater")

    return enrichment, p_value, overlap


def main():
    detectors = get_all_detectors()
    all_results = []

    for pathogen, info in ESCAPE_SITES.items():
        escape_set = info["positions"]
        n_total = info["n_total_positions"]

        fm_path = FEATURE_DIR / f'feature_matrix_{pathogen}.csv'
        if not fm_path.exists():
            continue

        fm_df = pd.read_csv(fm_path)
        n_pos = len(fm_df)
        scorings = build_all_scorings(pathogen, n_pos)

        print(f"{pathogen}: {n_pos} pos, {len(escape_set)} escape sites, {len(scorings)} scorings")

        for scoring_name, scores in scorings.items():
            if np.all(scores == 0) or np.all(np.isnan(scores)):
                continue
            scores = np.nan_to_num(scores, nan=0.0)

            for det in detectors:
                try:
                    detected_raw, _ = det.detect(scores)
                    detected = postprocess(detected_raw, n_pos)
                except Exception:
                    detected = []

                detected_set = set(detected)
                enrichment, p_value, overlap = compute_enrichment(
                    detected_set, escape_set, n_pos
                )

                all_results.append({
                    'pathogen': pathogen,
                    'scoring': scoring_name,
                    'detector': det.name,
                    'family': det.family,
                    'n_detected': len(detected),
                    'n_escape': len(escape_set),
                    'n_overlap': overlap,
                    'enrichment': round(enrichment, 4),
                    'p_value': p_value,
                })

    df = pd.DataFrame(all_results)
    out_path = RESULTS_DIR / 'vaccine_escape_stage3.csv'
    df.to_csv(out_path, index=False)
    print(f"\nSaved {len(df)} evaluations to {out_path}")

    # Summary: best enrichment per pathogen
    for pathogen in ESCAPE_SITES:
        pdf = df[(df['pathogen'] == pathogen) & (df['enrichment'] > 0)]
        if len(pdf) == 0:
            continue
        # Best by enrichment with p < 0.05
        sig = pdf[pdf['p_value'] < 0.05]
        if len(sig) > 0:
            best = sig.loc[sig['enrichment'].idxmax()]
            print(f"\n{pathogen} best significant: {best['scoring']}+{best['detector']}")
            print(f"  Enrichment={best['enrichment']:.2f}×, p={best['p_value']:.4f}, overlap={best['n_overlap']}/{best['n_escape']}")
        else:
            best = pdf.loc[pdf['enrichment'].idxmax()]
            print(f"\n{pathogen} best (not significant): {best['scoring']}+{best['detector']}")
            print(f"  Enrichment={best['enrichment']:.2f}×, p={best['p_value']:.4f}")


if __name__ == '__main__':
    main()
