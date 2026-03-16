#!/usr/bin/env python3
"""
PAHD (Pathogen-Adaptive Hotspot Detection) Prototype v2
========================================================
Improved feature extraction: MSA-derived score distribution statistics
instead of static metadata only.

Strategies compared:
1. Naive LOPO: single best combo across all training pathogens
2. PAHD 1-NN: use most-similar pathogen's best combo
3. PAHD Weighted: similarity-weighted MCC voting across all training pathogens
4. PAHD Family-first: predict best family, then best combo within family

v2 improvements:
- Score distribution statistics (mean, std, skewness, kurtosis) per scoring formula
- Zero-score proportion per scoring formula
- Gini coefficient of score distributions
- Spatial autocorrelation (Moran's I) of scores
- Entropy-function divergence metrics
- All computed from FASTA/MSA data — NO oracle MCC leakage
"""

import pandas as pd
import numpy as np
from scipy import stats as sp_stats
from sklearn.preprocessing import StandardScaler
from sklearn.metrics.pairwise import cosine_similarity
from pathlib import Path
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

RESULTS_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                           '..', 'results', 'mutbench')
DATA_DIR = Path(__file__).parent.parent / 'data'

PATHOGENS_FASTA = {
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


def load_multilayer_results():
    path = os.path.join(RESULTS_DIR, 'multilayer_9pathogen_results.csv')
    return pd.read_csv(path)


def _gini(arr):
    """Gini coefficient of a 1D array (0=perfect equality, 1=max inequality)."""
    arr = np.sort(np.abs(arr))
    n = len(arr)
    if n == 0 or arr.sum() == 0:
        return 0.0
    index = np.arange(1, n + 1)
    return (2 * np.sum(index * arr) - (n + 1) * np.sum(arr)) / (n * np.sum(arr))


def _morans_i(arr, lag=1):
    """Spatial autocorrelation (Moran's I) for a 1D array with ring adjacency."""
    n = len(arr)
    if n < 3:
        return 0.0
    mean = arr.mean()
    diffs = arr - mean
    var = np.sum(diffs ** 2)
    if var == 0:
        return 0.0
    # ring adjacency: each position connected to +-lag neighbors
    cross = 0.0
    w_total = 0
    for i in range(n):
        for d in range(1, lag + 1):
            j = (i + d) % n
            cross += diffs[i] * diffs[j]
            w_total += 1
            j = (i - d) % n
            cross += diffs[i] * diffs[j]
            w_total += 1
    return (n / w_total) * (cross / var)


def _run_length_stat(arr, threshold_pct=90):
    """Mean and max run length of positions above threshold percentile."""
    if len(arr) == 0 or np.all(arr == 0):
        return 0.0, 0
    thresh = np.percentile(arr[arr > 0], threshold_pct) if np.any(arr > 0) else 0
    above = arr > thresh
    runs = []
    current = 0
    for v in above:
        if v:
            current += 1
        else:
            if current > 0:
                runs.append(current)
            current = 0
    if current > 0:
        runs.append(current)
    if not runs:
        return 0.0, 0
    return np.mean(runs), max(runs)


def extract_pathogen_profiles_v2(df):
    """
    Extract rich feature vectors per pathogen from MSA-derived score distributions.

    Feature categories (NO oracle MCC leakage):
    1. Basic metadata (4): seq_length, n_unique, diversity_ratio, log_n_seq
    2. GT characteristics (4): gt sizes, densities, ratio
    3. Per-score distribution stats (9 scores x 6 stats = 54):
       mean, std, skewness, kurtosis, zero_frac, gini
    4. Aggregated score landscape (6): cross-score correlation structure
    5. Spatial features (3): Moran's I for top-3 scores
    6. Detection landscape (4): mean/std of n_detected across combos
    """
    from scripts.run_extended_benchmark import (
        load_fasta, compute_features, compute_scores,
    )

    score_names = [
        'E*rare', 'P*E*rare', 'minority_E', 'P*minority_E',
        'P*E', 'H-score', 'E_only', 'P*E^2', 'rank(P*E)',
    ]

    profiles = {}
    for pathogen, grp in df.groupby('pathogen'):
        row0 = grp.iloc[0]
        n_seq = row0['n_sequences']
        n_uniq = row0['n_unique']
        seq_len = row0['seq_length']
        gt_a = row0['gt_adaptive_size']
        gt_b = row0['gt_constrained_size']

        features = {}

        # --- Category 1: Basic metadata ---
        features['log_seq_length'] = np.log1p(seq_len)
        features['log_n_unique'] = np.log1p(n_uniq)
        features['diversity_ratio'] = n_uniq / n_seq if n_seq > 0 else 0
        features['log_n_seq'] = np.log1p(n_seq)

        # --- Category 2: GT characteristics ---
        features['adaptive_density'] = gt_a / seq_len if seq_len > 0 else 0
        features['constrained_density'] = gt_b / seq_len if seq_len > 0 else 0
        features['gt_ratio'] = gt_a / (gt_a + gt_b) if (gt_a + gt_b) > 0 else 0
        features['log_gt_total'] = np.log1p(gt_a + gt_b)

        # --- Category 3-5: MSA-derived score distributions ---
        fasta_path = PATHOGENS_FASTA.get(pathogen)
        score_arrays = {}
        if fasta_path and fasta_path.exists():
            sequences = load_fasta(str(fasta_path))
            min_len = min(len(s) for s in sequences)
            sequences = [s[:min_len] for s in sequences]
            raw_features = compute_features(sequences)
            all_scores = compute_scores(raw_features)

            # Raw features stats (P and E are the most fundamental)
            P = raw_features['P']
            E = raw_features['E']
            features['P_mean'] = P.mean()
            features['P_std'] = P.std()
            features['P_zero_frac'] = (P == 0).mean()
            features['E_mean'] = E.mean()
            features['E_std'] = E.std()
            features['E_zero_frac'] = (E == 0).mean()
            features['PE_correlation'] = np.corrcoef(P, E)[0, 1] if P.std() > 0 and E.std() > 0 else 0

            for sname in score_names:
                s_arr = all_scores[sname]
                score_arrays[sname] = s_arr
                prefix = sname.replace('*', 'x').replace('(', '').replace(')', '').replace('^', 'p')

                nz = s_arr[s_arr != 0]
                features[f'{prefix}_mean'] = s_arr.mean()
                features[f'{prefix}_std'] = s_arr.std()
                features[f'{prefix}_zero_frac'] = (s_arr == 0).mean()
                features[f'{prefix}_gini'] = _gini(s_arr)

                if len(nz) > 4:
                    features[f'{prefix}_skew'] = float(sp_stats.skew(nz))
                    features[f'{prefix}_kurtosis'] = float(sp_stats.kurtosis(nz))
                else:
                    features[f'{prefix}_skew'] = 0.0
                    features[f'{prefix}_kurtosis'] = 0.0

            # --- Category 4: Cross-score correlation structure ---
            # How correlated are different scoring formulas? (captures entropy-function divergence)
            score_matrix = np.column_stack([all_scores[s] for s in score_names])
            corr = np.corrcoef(score_matrix.T)
            corr_vals = corr[np.triu_indices_from(corr, k=1)]
            features['cross_score_corr_mean'] = corr_vals.mean()
            features['cross_score_corr_std'] = corr_vals.std()
            features['cross_score_corr_min'] = corr_vals.min()

            # --- Category 5: Spatial autocorrelation ---
            # Top-3 important scores: E*rare, P*E, H-score
            for sname in ['E*rare', 'P*E', 'H-score']:
                prefix = sname.replace('*', 'x').replace('(', '').replace(')', '').replace('^', 'p')
                s_arr = all_scores[sname]
                features[f'{prefix}_moran_i'] = _morans_i(s_arr, lag=3)
                mean_rl, max_rl = _run_length_stat(s_arr, threshold_pct=90)
                features[f'{prefix}_mean_runlen'] = mean_rl
                features[f'{prefix}_max_runlen'] = max_rl / seq_len if seq_len > 0 else 0
        else:
            # Fallback: use benchmark CSV stats if FASTA unavailable
            print(f"  [WARN] FASTA not found for {pathogen}, using fallback features")
            features['P_mean'] = 0
            features['P_std'] = 0
            features['P_zero_frac'] = 0
            features['E_mean'] = 0
            features['E_std'] = 0
            features['E_zero_frac'] = 0
            features['PE_correlation'] = 0
            for sname in score_names:
                prefix = sname.replace('*', 'x').replace('(', '').replace(')', '').replace('^', 'p')
                for suffix in ['_mean', '_std', '_zero_frac', '_gini', '_skew', '_kurtosis']:
                    features[f'{prefix}{suffix}'] = 0
            features['cross_score_corr_mean'] = 0
            features['cross_score_corr_std'] = 0
            features['cross_score_corr_min'] = 0
            for sname in ['E*rare', 'P*E', 'H-score']:
                prefix = sname.replace('*', 'x').replace('(', '').replace(')', '').replace('^', 'p')
                features[f'{prefix}_moran_i'] = 0
                features[f'{prefix}_mean_runlen'] = 0
                features[f'{prefix}_max_runlen'] = 0

        # --- Category 6: Detection landscape (from benchmark CSV, not oracle) ---
        # n_detected distribution reflects scoring characteristics, not GT performance
        nd = grp['n_detected']
        features['det_mean_ratio'] = nd.mean() / seq_len if seq_len > 0 else 0
        features['det_std_ratio'] = nd.std() / seq_len if seq_len > 0 else 0
        features['det_cv'] = nd.std() / nd.mean() if nd.mean() > 0 else 0
        # How many combos detect very few positions (< 5% of seq)?
        features['det_sparse_frac'] = (nd < 0.05 * seq_len).mean()

        profiles[pathogen] = features

    return pd.DataFrame(profiles).T


def extract_pathogen_profiles(df):
    """
    Original 8-feature profile (kept for comparison).
    """
    profiles = {}
    for pathogen, grp in df.groupby('pathogen'):
        row0 = grp.iloc[0]
        n_seq = row0['n_sequences']
        n_uniq = row0['n_unique']
        seq_len = row0['seq_length']
        gt_a = row0['gt_adaptive_size']
        gt_b = row0['gt_constrained_size']

        profiles[pathogen] = {
            'seq_length': seq_len,
            'n_unique': n_uniq,
            'gt_adaptive_size': gt_a,
            'gt_constrained_size': gt_b,
            'diversity_ratio': n_uniq / n_seq if n_seq > 0 else 0,
            'adaptive_density': gt_a / seq_len if seq_len > 0 else 0,
            'constrained_density': gt_b / seq_len if seq_len > 0 else 0,
            'gt_ratio': gt_a / (gt_a + gt_b) if (gt_a + gt_b) > 0 else 0,
        }
    return pd.DataFrame(profiles).T


def get_best_combo(df, pathogen):
    """Return the best (score, detector) combo for a pathogen by MCC."""
    sub = df[df['pathogen'] == pathogen]
    best_idx = sub['mcc_adaptive'].idxmax()
    best = sub.loc[best_idx]
    return f"{best['score']} + {best['detector']}", best['mcc_adaptive']


def compute_similarity(profiles_df):
    """Standardize then cosine similarity."""
    scaler = StandardScaler()
    X = scaler.fit_transform(profiles_df.values)
    sim = cosine_similarity(X)
    return pd.DataFrame(sim, index=profiles_df.index, columns=profiles_df.index)


def naive_lopo(df, pathogens):
    """Naive LOPO: single best combo from training mean."""
    results = []
    for held_out in pathogens:
        train = df[df['pathogen'] != held_out]
        combo_mean = train.groupby(['score', 'detector'])['mcc_adaptive'].mean()
        best_idx = combo_mean.idxmax()
        best_combo = f"{best_idx[0]} + {best_idx[1]}"

        ho = df[(df['pathogen'] == held_out) &
                (df['score'] == best_idx[0]) &
                (df['detector'] == best_idx[1])]
        test_mcc = ho['mcc_adaptive'].values[0] if len(ho) > 0 else 0.0
        oracle_combo, oracle_mcc = get_best_combo(df, held_out)

        results.append({
            'held_out': held_out,
            'method': 'Naive',
            'predicted_combo': best_combo,
            'test_mcc': round(test_mcc, 4),
            'oracle_combo': oracle_combo,
            'oracle_mcc': round(oracle_mcc, 4),
            'combo_match': best_combo == oracle_combo,
            'gen_ratio': round(test_mcc / oracle_mcc if oracle_mcc > 0 else 0, 4),
        })
    return pd.DataFrame(results)


def pahd_weighted_lopo(df, sim_df, pathogens):
    """
    PAHD Weighted: for each combo, compute similarity-weighted mean MCC
    across training pathogens. Pick the combo with highest weighted score.

    weight_i = max(0, similarity(held_out, pathogen_i))
    weighted_mcc(combo) = sum(w_i * mcc_i) / sum(w_i)
    """
    results = []
    for held_out in pathogens:
        train_pathogens = [p for p in pathogens if p != held_out]

        # get similarities (clamp to >= 0 to avoid negative weighting)
        weights = {}
        for p in train_pathogens:
            w = max(0.01, sim_df.loc[held_out, p])  # floor at 0.01
            weights[p] = w

        # for each combo, compute weighted mean MCC
        best_combo = None
        best_weighted_mcc = -999
        combos = df[['score', 'detector']].drop_duplicates()

        for _, row in combos.iterrows():
            s, d = row['score'], row['detector']
            w_sum = 0
            w_mcc = 0
            for p in train_pathogens:
                sub = df[(df['pathogen'] == p) &
                         (df['score'] == s) & (df['detector'] == d)]
                if len(sub) > 0:
                    w = weights[p]
                    w_sum += w
                    w_mcc += w * sub['mcc_adaptive'].values[0]
            if w_sum > 0:
                avg = w_mcc / w_sum
                if avg > best_weighted_mcc:
                    best_weighted_mcc = avg
                    best_combo = f"{s} + {d}"

        pred_s, pred_d = best_combo.split(' + ', 1)
        ho = df[(df['pathogen'] == held_out) &
                (df['score'] == pred_s) & (df['detector'] == pred_d)]
        test_mcc = ho['mcc_adaptive'].values[0] if len(ho) > 0 else 0.0
        oracle_combo, oracle_mcc = get_best_combo(df, held_out)

        results.append({
            'held_out': held_out,
            'method': 'PAHD-Weighted',
            'predicted_combo': best_combo,
            'test_mcc': round(test_mcc, 4),
            'oracle_combo': oracle_combo,
            'oracle_mcc': round(oracle_mcc, 4),
            'combo_match': best_combo == oracle_combo,
            'gen_ratio': round(test_mcc / oracle_mcc if oracle_mcc > 0 else 0, 4),
        })
    return pd.DataFrame(results)


def pahd_family_lopo(df, sim_df, pathogens):
    """
    PAHD Family-first: predict best detection FAMILY via weighted voting,
    then within that family, select the combo with best weighted MCC.
    Two-stage prediction reduces search space.
    """
    results = []
    for held_out in pathogens:
        train_pathogens = [p for p in pathogens if p != held_out]
        weights = {p: max(0.01, sim_df.loc[held_out, p]) for p in train_pathogens}

        # Stage 1: weighted vote for best family
        train = df[df['pathogen'] != held_out]
        family_scores = {}
        for family, fgrp in train.groupby('family'):
            w_total = 0
            w_mcc = 0
            for p in train_pathogens:
                sub = fgrp[fgrp['pathogen'] == p]
                if len(sub) > 0:
                    best_mcc = sub['mcc_adaptive'].max()
                    w = weights[p]
                    w_total += w
                    w_mcc += w * best_mcc
            if w_total > 0:
                family_scores[family] = w_mcc / w_total
        best_family = max(family_scores, key=family_scores.get)

        # Stage 2: within best family, pick best combo by weighted MCC
        family_df = df[df['family'] == best_family]
        combos = family_df[['score', 'detector']].drop_duplicates()
        best_combo = None
        best_wmcc = -999
        for _, row in combos.iterrows():
            s, d = row['score'], row['detector']
            w_sum = 0
            w_mcc = 0
            for p in train_pathogens:
                sub = family_df[(family_df['pathogen'] == p) &
                                (family_df['score'] == s) &
                                (family_df['detector'] == d)]
                if len(sub) > 0:
                    w = weights[p]
                    w_sum += w
                    w_mcc += w * sub['mcc_adaptive'].values[0]
            if w_sum > 0:
                avg = w_mcc / w_sum
                if avg > best_wmcc:
                    best_wmcc = avg
                    best_combo = f"{s} + {d}"

        pred_s, pred_d = best_combo.split(' + ', 1)
        ho = df[(df['pathogen'] == held_out) &
                (df['score'] == pred_s) & (df['detector'] == pred_d)]
        test_mcc = ho['mcc_adaptive'].values[0] if len(ho) > 0 else 0.0
        oracle_combo, oracle_mcc = get_best_combo(df, held_out)

        results.append({
            'held_out': held_out,
            'method': 'PAHD-Family',
            'predicted_family': best_family,
            'predicted_combo': best_combo,
            'test_mcc': round(test_mcc, 4),
            'oracle_combo': oracle_combo,
            'oracle_mcc': round(oracle_mcc, 4),
            'combo_match': best_combo == oracle_combo,
            'gen_ratio': round(test_mcc / oracle_mcc if oracle_mcc > 0 else 0, 4),
        })
    return pd.DataFrame(results)


def pahd_1nn_lopo(df, sim_df, pathogens):
    """PAHD 1-NN: use most-similar pathogen's best combo."""
    results = []
    for held_out in pathogens:
        train_pathogens = [p for p in pathogens if p != held_out]
        sims = sim_df.loc[held_out, train_pathogens]
        most_similar = sims.idxmax()
        sim_score = sims.max()

        pred_combo, _ = get_best_combo(df, most_similar)
        pred_s, pred_d = pred_combo.split(' + ', 1)

        ho = df[(df['pathogen'] == held_out) &
                (df['score'] == pred_s) & (df['detector'] == pred_d)]
        test_mcc = ho['mcc_adaptive'].values[0] if len(ho) > 0 else 0.0
        oracle_combo, oracle_mcc = get_best_combo(df, held_out)

        results.append({
            'held_out': held_out,
            'method': 'PAHD-1NN',
            'most_similar': most_similar,
            'similarity': round(sim_score, 4),
            'predicted_combo': pred_combo,
            'test_mcc': round(test_mcc, 4),
            'oracle_combo': oracle_combo,
            'oracle_mcc': round(oracle_mcc, 4),
            'combo_match': pred_combo == oracle_combo,
            'gen_ratio': round(test_mcc / oracle_mcc if oracle_mcc > 0 else 0, 4),
        })
    return pd.DataFrame(results)


def _run_lopo_suite(df, sim_df, pathogens, label=""):
    """Run all 4 LOPO methods and return summary dict."""
    naive_res = naive_lopo(df, pathogens)
    nn_res = pahd_1nn_lopo(df, sim_df, pathogens)
    wt_res = pahd_weighted_lopo(df, sim_df, pathogens)
    fam_res = pahd_family_lopo(df, sim_df, pathogens)

    methods = {
        'Naive LOPO': naive_res,
        'PAHD 1-NN': nn_res,
        'PAHD Weighted': wt_res,
        'PAHD Family': fam_res,
    }

    rows = []
    for name, res in methods.items():
        matches = res['combo_match'].sum()
        mean_mcc = res['test_mcc'].mean()
        mean_gr = res['gen_ratio'].mean()
        positive_count = (res['test_mcc'] > 0).sum()
        median_mcc = res['test_mcc'].median()
        rows.append({
            'Method': f"{label}{name}" if label else name,
            'Match': f"{matches}/9",
            'MCC>0': f"{positive_count}/9",
            'Mean_MCC': round(mean_mcc, 4),
            'Median_MCC': round(median_mcc, 4),
            'Mean_GenRatio': round(mean_gr, 4),
        })

    return methods, pd.DataFrame(rows), naive_res, nn_res, wt_res, fam_res


def main():
    print("=" * 70)
    print("PAHD Prototype v2 — Improved MSA-Derived Features")
    print("=" * 70)

    df = load_multilayer_results()
    pathogens = sorted(df['pathogen'].unique())
    print(f"\nPathogens ({len(pathogens)}): {', '.join(pathogens)}")
    print(f"Total evaluations: {len(df)}")

    # Oracle
    print("\n--- Oracle Best Combos ---")
    for p in pathogens:
        combo, mcc = get_best_combo(df, p)
        print(f"  {p:15s}: {combo:45s} MCC={mcc:.4f}")

    # ===== v1: Original 8-feature profiles =====
    print("\n" + "=" * 70)
    print("v1: Original 8-feature profiles")
    print("=" * 70)

    profiles_v1 = extract_pathogen_profiles(df)
    sim_v1 = compute_similarity(profiles_v1)
    print(f"Features ({profiles_v1.shape[1]}): {list(profiles_v1.columns)}")

    v1_methods, v1_summary, *_ = _run_lopo_suite(df, sim_v1, pathogens, "v1:")
    print(v1_summary.to_string(index=False))

    # ===== v2: Rich MSA-derived profiles =====
    print("\n" + "=" * 70)
    print("v2: Rich MSA-derived profiles")
    print("=" * 70)

    profiles_v2 = extract_pathogen_profiles_v2(df)
    print(f"Features ({profiles_v2.shape[1]}): {list(profiles_v2.columns[:10])}... "
          f"(+{profiles_v2.shape[1]-10} more)")

    sim_v2 = compute_similarity(profiles_v2)
    print("\nv2 Cosine similarity matrix:")
    print(sim_v2.round(3).to_string())

    v2_methods, v2_summary, naive_res, nn_res, wt_res, fam_res = \
        _run_lopo_suite(df, sim_v2, pathogens, "v2:")
    print(v2_summary.to_string(index=False))

    # ===== Head-to-head comparison =====
    print("\n" + "=" * 70)
    print("HEAD-TO-HEAD: v1 vs v2")
    print("=" * 70)

    combined_summary = pd.concat([v1_summary, v2_summary], ignore_index=True)
    print(combined_summary.to_string(index=False))

    # Per-pathogen comparison
    print("\n--- Per-Pathogen MCC Comparison (v2) ---")
    comp = pd.DataFrame({
        'Pathogen': pathogens,
        'Oracle': [get_best_combo(df, p)[1] for p in pathogens],
    })
    for name, res in v2_methods.items():
        comp[name] = res.set_index('held_out').loc[pathogens, 'test_mcc'].values
    print(comp.round(4).to_string(index=False))

    # Best PAHD method per pathogen
    print("\n--- Best PAHD method per pathogen (v2) ---")
    for p in pathogens:
        oracle_mcc = get_best_combo(df, p)[1]
        best_method = None
        best_mcc = -999
        for name, res in v2_methods.items():
            mcc = res[res['held_out'] == p]['test_mcc'].values[0]
            if mcc > best_mcc:
                best_mcc = mcc
                best_method = name
        ratio = best_mcc / oracle_mcc if oracle_mcc > 0 else 0
        print(f"  {p:15s}: {best_method:15s} MCC={best_mcc:.4f} "
              f"(oracle={oracle_mcc:.4f}, ratio={ratio:.2f})")

    # Similarity comparison: which pathogens become more/less similar?
    print("\n--- Similarity Changes (v2 - v1) ---")
    diff = sim_v2 - sim_v1
    for i, p1 in enumerate(pathogens):
        for j, p2 in enumerate(pathogens):
            if i < j:
                d = diff.loc[p1, p2]
                if abs(d) > 0.2:
                    print(f"  {p1:15s} - {p2:15s}: {sim_v1.loc[p1,p2]:+.3f} -> "
                          f"{sim_v2.loc[p1,p2]:+.3f} (delta={d:+.3f})")

    # Save
    all_v2 = pd.concat([
        naive_res.assign(profile_version='v2'),
        nn_res.assign(profile_version='v2'),
        wt_res.assign(profile_version='v2'),
        fam_res.assign(profile_version='v2'),
    ], ignore_index=True)
    all_v2.to_csv(os.path.join(RESULTS_DIR, 'pahd_prototype_results.csv'), index=False)
    combined_summary.to_csv(os.path.join(RESULTS_DIR, 'pahd_prototype_summary.csv'), index=False)
    sim_v2.to_csv(os.path.join(RESULTS_DIR, 'pahd_pathogen_similarity.csv'))
    profiles_v2.to_csv(os.path.join(RESULTS_DIR, 'pahd_pathogen_profiles.csv'))
    comp.to_csv(os.path.join(RESULTS_DIR, 'pahd_comparison_table.csv'), index=False)
    print(f"\nResults saved to {RESULTS_DIR}/pahd_*.csv")


if __name__ == '__main__':
    main()
