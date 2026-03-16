#!/usr/bin/env python3
"""
PAHD (Pathogen-Adaptive Hotspot Detection) Prototype
=====================================================
Proof-of-concept: profile-based LOPO prediction.

Three strategies compared:
1. Naive LOPO: single best combo across all training pathogens
2. PAHD 1-NN: use most-similar pathogen's best combo
3. PAHD Weighted: similarity-weighted MCC voting across all training pathogens
4. PAHD Family-first: predict best family, then best combo within family
"""

import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.metrics.pairwise import cosine_similarity
import os

RESULTS_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                           '..', 'results', 'mutbench')


def load_multilayer_results():
    path = os.path.join(RESULTS_DIR, 'multilayer_9pathogen_results.csv')
    return pd.read_csv(path)


def extract_pathogen_profiles(df):
    """
    Extract a feature vector per pathogen from the benchmark results.
    """
    profiles = {}
    for pathogen, grp in df.groupby('pathogen'):
        row0 = grp.iloc[0]
        n_seq = row0['n_sequences']
        n_uniq = row0['n_unique']
        seq_len = row0['seq_length']
        gt_a = row0['gt_adaptive_size']
        gt_b = row0['gt_constrained_size']

        # per-family performance distribution (captures method landscape)
        family_mccs = grp.groupby('family')['mcc_adaptive'].mean()

        # Only genome/GT characteristics — NO oracle performance info to avoid leakage
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


def main():
    print("=" * 70)
    print("PAHD Prototype — Profile-Based LOPO Prediction")
    print("=" * 70)

    df = load_multilayer_results()
    pathogens = sorted(df['pathogen'].unique())
    print(f"\nPathogens ({len(pathogens)}): {', '.join(pathogens)}")
    print(f"Total evaluations: {len(df)}")

    # Profiles
    profiles = extract_pathogen_profiles(df)
    print(f"\nPathogen profiles ({profiles.shape[1]} features):")
    print(profiles.round(4).to_string())

    # Similarity
    sim_df = compute_similarity(profiles)
    print("\nCosine similarity matrix:")
    print(sim_df.round(3).to_string())

    # Oracle
    print("\n--- Oracle Best Combos ---")
    for p in pathogens:
        combo, mcc = get_best_combo(df, p)
        print(f"  {p:15s}: {combo:45s} MCC={mcc:.4f}")

    # ===== Methods =====
    # 1. Naive
    naive_res = naive_lopo(df, pathogens)
    print("\n--- Naive LOPO ---")
    for _, r in naive_res.iterrows():
        print(f"  {r['held_out']:15s} → {r['predicted_combo']:45s} "
              f"MCC={r['test_mcc']:.4f}  oracle={r['oracle_mcc']:.4f}  "
              f"ratio={r['gen_ratio']:.4f}  match={r['combo_match']}")

    # 2. PAHD 1-NN
    nn_res = pahd_1nn_lopo(df, sim_df, pathogens)
    print("\n--- PAHD 1-NN ---")
    for _, r in nn_res.iterrows():
        print(f"  {r['held_out']:15s} → {r['predicted_combo']:45s} "
              f"MCC={r['test_mcc']:.4f}  oracle={r['oracle_mcc']:.4f}  "
              f"ratio={r['gen_ratio']:.4f}  (similar={r['most_similar']}, "
              f"sim={r['similarity']:.3f})")

    # 3. PAHD Weighted
    wt_res = pahd_weighted_lopo(df, sim_df, pathogens)
    print("\n--- PAHD Weighted ---")
    for _, r in wt_res.iterrows():
        print(f"  {r['held_out']:15s} → {r['predicted_combo']:45s} "
              f"MCC={r['test_mcc']:.4f}  oracle={r['oracle_mcc']:.4f}  "
              f"ratio={r['gen_ratio']:.4f}  match={r['combo_match']}")

    # 4. PAHD Family-first
    fam_res = pahd_family_lopo(df, sim_df, pathogens)
    print("\n--- PAHD Family-First ---")
    for _, r in fam_res.iterrows():
        print(f"  {r['held_out']:15s} → [{r['predicted_family']:12s}] "
              f"{r['predicted_combo']:40s} "
              f"MCC={r['test_mcc']:.4f}  oracle={r['oracle_mcc']:.4f}  "
              f"ratio={r['gen_ratio']:.4f}  match={r['combo_match']}")

    # Summary
    print("\n" + "=" * 70)
    print("SUMMARY")
    print("=" * 70)

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
        rows.append({
            'Method': name,
            'Match': f"{matches}/9",
            'MCC>0': f"{positive_count}/9",
            'Mean_MCC': round(mean_mcc, 4),
            'Mean_GenRatio': round(mean_gr, 4),
        })

    summary = pd.DataFrame(rows)
    print(summary.to_string(index=False))

    # Improvement analysis
    naive_mcc = naive_res['test_mcc'].mean()
    for name, res in methods.items():
        if name == 'Naive LOPO':
            continue
        m = res['test_mcc'].mean()
        diff = m - naive_mcc
        print(f"\n{name} vs Naive: MCC diff = {diff:+.4f}")

    # Per-pathogen comparison table
    print("\n--- Per-Pathogen MCC Comparison ---")
    comp = pd.DataFrame({
        'Pathogen': pathogens,
        'Oracle': [get_best_combo(df, p)[1] for p in pathogens],
    })
    for name, res in methods.items():
        comp[name] = res.set_index('held_out').loc[pathogens, 'test_mcc'].values
    print(comp.round(4).to_string(index=False))

    # Which PAHD method gets closest to oracle for each pathogen?
    print("\n--- Best PAHD method per pathogen ---")
    for p in pathogens:
        oracle_mcc = get_best_combo(df, p)[1]
        best_method = 'Naive LOPO'
        best_mcc = naive_res[naive_res['held_out'] == p]['test_mcc'].values[0]
        for name, res in methods.items():
            mcc = res[res['held_out'] == p]['test_mcc'].values[0]
            if mcc > best_mcc:
                best_mcc = mcc
                best_method = name
        print(f"  {p:15s}: {best_method:15s} MCC={best_mcc:.4f} "
              f"(oracle={oracle_mcc:.4f}, ratio={best_mcc/oracle_mcc:.2f})")

    # Save
    combined = pd.concat([naive_res, nn_res, wt_res, fam_res], ignore_index=True)
    combined.to_csv(os.path.join(RESULTS_DIR, 'pahd_prototype_results.csv'), index=False)
    summary.to_csv(os.path.join(RESULTS_DIR, 'pahd_prototype_summary.csv'), index=False)
    sim_df.to_csv(os.path.join(RESULTS_DIR, 'pahd_pathogen_similarity.csv'))
    profiles.to_csv(os.path.join(RESULTS_DIR, 'pahd_pathogen_profiles.csv'))
    comp.to_csv(os.path.join(RESULTS_DIR, 'pahd_comparison_table.csv'), index=False)
    print(f"\nResults saved to {RESULTS_DIR}/pahd_*.csv")


if __name__ == '__main__':
    main()
