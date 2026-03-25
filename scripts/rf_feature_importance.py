#!/usr/bin/env python3
"""Random Forest feature importance analysis for MutBench 9-pathogen benchmark.

For each pathogen, trains an RF classifier to predict Layer A (convergent evolution)
from 6 positional features, extracts feature importances, and generates a 3x3 grid figure.
"""

import os
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import StratifiedKFold, cross_val_score
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

PATHOGENS = [
    'SARS-CoV-2', 'H3N2', 'Norovirus',
    'HIV-1', 'Dengue', 'RSV',
    'Influenza_B', 'MERS', 'HCV',
]

FEATURES = ['freq', 'entropy', 'rare_freq', 'homoplasy', 'esm2_llr', 'plddt']

FEATURE_LABELS = {
    'freq': 'Frequency',
    'entropy': 'Entropy',
    'rare_freq': 'Rare freq.',
    'homoplasy': 'Homoplasy',
    'esm2_llr': 'ESM-2 LLR',
    'plddt': 'pLDDT',
}

# Color coding by feature type
FEATURE_COLORS = {
    'freq': '#2171b5',       # frequency-based: blue
    'entropy': '#2171b5',    # frequency-based: blue
    'rare_freq': '#2171b5',  # frequency-based: blue
    'homoplasy': '#238b45',  # phylogeny: green
    'esm2_llr': '#7b3294',   # deep learning: purple
    'plddt': '#d95f0e',      # structure: orange
}

DISPLAY_PATHOGENS = {
    'SARS-CoV-2': 'SARS-CoV-2',
    'H3N2': 'H3N2',
    'Norovirus': 'Norovirus',
    'HIV-1': 'HIV-1',
    'Dengue': 'Dengue',
    'RSV': 'RSV',
    'Influenza_B': 'Influenza B',
    'MERS': 'MERS',
    'HCV': 'HCV',
}

DATA_DIR = '/proj/paper/results/mutbench/feature_analysis'
OUT_DIR = '/proj/paper/results/mutbench/feature_analysis'
FIG_DIR = '/proj/paper/results/mutbench'


def main():
    os.makedirs(OUT_DIR, exist_ok=True)
    os.makedirs(FIG_DIR, exist_ok=True)

    importance_rows = []
    auc_rows = []

    for pathogen in PATHOGENS:
        fpath = os.path.join(DATA_DIR, f'feature_matrix_{pathogen}.csv')
        df = pd.read_csv(fpath)

        X = df[FEATURES].values
        y = df['layer_a'].values

        # Handle NaN/inf
        X = np.nan_to_num(X, nan=0.0, posinf=0.0, neginf=0.0)

        n_pos = int(y.sum())
        n_total = len(y)
        print(f'{pathogen}: {n_total} positions, {n_pos} Layer A positives ({100*n_pos/n_total:.1f}%)')

        # Determine n_splits: need at least 2 positives per fold
        max_folds = max(2, n_pos // 2)
        n_splits = min(5, max_folds)

        rf = RandomForestClassifier(
            n_estimators=100,
            class_weight='balanced',
            random_state=42,
            n_jobs=-1,
        )

        # Cross-validation AUC
        skf = StratifiedKFold(n_splits=n_splits, shuffle=True, random_state=42)
        cv_aucs = cross_val_score(rf, X, y, cv=skf, scoring='roc_auc')
        mean_auc = cv_aucs.mean()
        std_auc = cv_aucs.std()

        auc_rows.append({
            'pathogen': pathogen,
            'mean_cv_auc': round(mean_auc, 4),
            'std': round(std_auc, 4),
            'n_folds': n_splits,
            'n_positions': n_total,
            'n_layer_a': n_pos,
        })

        # Fit on full data for importances
        rf.fit(X, y)
        importances = rf.feature_importances_

        for feat, imp in zip(FEATURES, importances):
            importance_rows.append({
                'pathogen': pathogen,
                'feature': feat,
                'importance': round(imp, 4),
                'cv_auc': round(mean_auc, 4),
            })

        print(f'  CV AUC: {mean_auc:.3f} +/- {std_auc:.3f}')
        for feat, imp in zip(FEATURES, importances):
            print(f'  {feat}: {imp:.4f}')

    # Save CSVs
    imp_df = pd.DataFrame(importance_rows)
    imp_df.to_csv(os.path.join(OUT_DIR, 'rf_importance.csv'), index=False)

    auc_df = pd.DataFrame(auc_rows)
    auc_df.to_csv(os.path.join(OUT_DIR, 'rf_cv_auc.csv'), index=False)

    print(f'\nSaved: {os.path.join(OUT_DIR, "rf_importance.csv")}')
    print(f'Saved: {os.path.join(OUT_DIR, "rf_cv_auc.csv")}')

    # --- Generate 3x3 grid figure ---
    fig, axes = plt.subplots(3, 3, figsize=(14, 12))
    fig.subplots_adjust(hspace=0.45, wspace=0.35)

    for idx, pathogen in enumerate(PATHOGENS):
        ax = axes[idx // 3][idx % 3]
        sub = imp_df[imp_df['pathogen'] == pathogen].set_index('feature')

        vals = [sub.loc[f, 'importance'] for f in FEATURES]
        colors = [FEATURE_COLORS[f] for f in FEATURES]
        labels = [FEATURE_LABELS[f] for f in FEATURES]

        bars = ax.bar(range(len(FEATURES)), vals, color=colors, edgecolor='black', linewidth=0.5)
        ax.set_xticks(range(len(FEATURES)))
        ax.set_xticklabels(labels, rotation=45, ha='right', fontsize=10)
        ax.set_ylabel('Importance', fontsize=11)
        cv_auc = auc_df[auc_df['pathogen'] == pathogen]['mean_cv_auc'].values[0]
        ax.set_title(f'{DISPLAY_PATHOGENS[pathogen]} (AUC={cv_auc:.2f})', fontsize=14, fontweight='bold')
        ax.set_ylim(0, max(vals) * 1.25 if max(vals) > 0 else 0.5)

        # Add value labels on bars
        for bar, val in zip(bars, vals):
            if val > 0.01:
                ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + max(vals) * 0.02,
                        f'{val:.2f}', ha='center', va='bottom', fontsize=8)

    # Legend
    from matplotlib.patches import Patch
    legend_elements = [
        Patch(facecolor='#2171b5', edgecolor='black', label='Frequency-based'),
        Patch(facecolor='#238b45', edgecolor='black', label='Phylogeny'),
        Patch(facecolor='#7b3294', edgecolor='black', label='Deep learning'),
        Patch(facecolor='#d95f0e', edgecolor='black', label='Structure'),
    ]
    fig.legend(handles=legend_elements, loc='lower center', ncol=4, fontsize=12,
               bbox_to_anchor=(0.5, -0.02), frameon=True)

    fig.suptitle('Random Forest Feature Importance by Pathogen', fontsize=16, fontweight='bold', y=1.01)

    out_fig = os.path.join(FIG_DIR, 'feature_importance_grid.png')
    fig.savefig(out_fig, dpi=300, bbox_inches='tight', facecolor='white')
    plt.close()
    print(f'Saved figure: {out_fig}')

    # Print summary table
    print('\n=== Summary: Top feature per pathogen ===')
    for pathogen in PATHOGENS:
        sub = imp_df[imp_df['pathogen'] == pathogen]
        best = sub.loc[sub['importance'].idxmax()]
        print(f"  {pathogen}: {best['feature']} ({best['importance']:.4f})")


if __name__ == '__main__':
    main()
