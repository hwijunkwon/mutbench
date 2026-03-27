#!/usr/bin/env python3
"""
3D Structural Hotspot Detection for 12 viral proteins.

Two approaches:
  1. DBSCAN clustering of mutated positions in 3D CA-atom space
  2. 3D contact density: count mutated neighbors within a radius

Evaluates against Layer A ground truth (MCC, precision, recall).
"""

import os
import sys
import warnings
import numpy as np
import pandas as pd
from Bio.PDB import PDBParser
from sklearn.cluster import DBSCAN
from sklearn.metrics import matthews_corrcoef, precision_score, recall_score
from scipy.spatial.distance import pdist, squareform

warnings.filterwarnings("ignore")

# === Configuration ===
PDB_DIR = "/proj/paper/results/mutbench/structural_features/pdb_structures"
FEAT_DIR = "/proj/paper/results/mutbench/feature_analysis"
OUT_DIR = "/proj/paper/results/mutbench"

DBSCAN_EPS = 8.0        # Angstroms
DBSCAN_MIN_SAMPLES = 3
CONTACT_RADIUS = 10.0    # Angstroms
CONTACT_THRESHOLD_PERCENTILE = 75  # top 25% of contact counts => hotspot

# Mapping: pdb filename stem -> feature matrix pathogen name
PATHOGEN_MAP = {
    "sars2": "SARS-CoV-2",
    "influenza_h3n2": "H3N2",
    "norovirus": "Norovirus",
    "hiv": "HIV-1",
    "dengue": "Dengue",
    "rsv": "RSV",
    "influenza_b": "Influenza_B",
    "mers": "MERS",
    "hcv": "HCV",
    "zika": "Zika",
    "rabies": "Rabies",
    "eva71": "EV-A71",
}


def load_pdb_ca_coords(pdb_path):
    """Load CA atom coordinates indexed by residue sequence number."""
    parser = PDBParser(QUIET=True)
    structure = parser.get_structure("protein", pdb_path)
    ca_coords = {}
    for model in structure:
        for chain in model:
            for residue in chain:
                if residue.id[0] != " ":
                    continue  # skip hetero atoms / water
                resnum = residue.id[1]
                if "CA" in residue:
                    ca_coords[resnum] = residue["CA"].get_vector().get_array()
    return ca_coords


def load_feature_matrix(pathogen_name):
    """Load feature matrix; returns DataFrame with position, freq, layer_a."""
    path = os.path.join(FEAT_DIR, f"feature_matrix_{pathogen_name}.csv")
    df = pd.read_csv(path)
    return df


def run_dbscan_hotspot(mutated_positions, ca_coords, eps=DBSCAN_EPS,
                       min_samples=DBSCAN_MIN_SAMPLES):
    """
    Run DBSCAN on 3D coordinates of mutated positions.
    Returns set of positions assigned to any cluster (not noise).
    """
    # Filter to mutated positions that have CA coords
    valid = [(pos, ca_coords[pos + 1]) for pos in mutated_positions
             if (pos + 1) in ca_coords]
    if len(valid) < min_samples:
        return set(), 0

    positions = [v[0] for v in valid]
    coords = np.array([v[1] for v in valid])

    clustering = DBSCAN(eps=eps, min_samples=min_samples, metric="euclidean")
    labels = clustering.fit_predict(coords)

    n_clusters = len(set(labels) - {-1})
    hotspot_positions = set()
    for pos, label in zip(positions, labels):
        if label != -1:
            hotspot_positions.add(pos)

    return hotspot_positions, n_clusters


def run_contact_density_hotspot(mutated_positions, ca_coords,
                                radius=CONTACT_RADIUS,
                                threshold_pct=CONTACT_THRESHOLD_PERCENTILE):
    """
    For each mutated position, count how many other mutated positions
    are within `radius` Angstroms in 3D space. Positions with contact
    count >= threshold percentile are called hotspots.
    """
    valid = [(pos, ca_coords[pos + 1]) for pos in mutated_positions
             if (pos + 1) in ca_coords]
    if len(valid) < 2:
        return set()

    positions = [v[0] for v in valid]
    coords = np.array([v[1] for v in valid])

    dist_matrix = squareform(pdist(coords, metric="euclidean"))
    contact_counts = np.sum(dist_matrix <= radius, axis=1) - 1  # exclude self

    if contact_counts.max() == 0:
        return set()

    threshold = np.percentile(contact_counts, threshold_pct)
    threshold = max(threshold, 2)  # at least 2 contacts

    hotspot_positions = set()
    for pos, count in zip(positions, contact_counts):
        if count >= threshold:
            hotspot_positions.add(pos)

    return hotspot_positions


def evaluate(all_positions, hotspot_positions, gt_labels):
    """Compute MCC, precision, recall."""
    y_true = []
    y_pred = []
    for pos in all_positions:
        y_true.append(int(gt_labels.get(pos, 0)))
        y_pred.append(1 if pos in hotspot_positions else 0)

    y_true = np.array(y_true)
    y_pred = np.array(y_pred)

    if y_true.sum() == 0 or y_pred.sum() == 0:
        return 0.0, 0.0, 0.0

    mcc = matthews_corrcoef(y_true, y_pred)
    prec = precision_score(y_true, y_pred, zero_division=0)
    rec = recall_score(y_true, y_pred, zero_division=0)
    return mcc, prec, rec


def main():
    results_dbscan = []
    results_contact = []

    print(f"{'Pathogen':<18} {'#Pos':>5} {'#Mut':>5} {'#GT+':>5} "
          f"{'DB_Clust':>8} {'DB_Hot':>6} {'DB_MCC':>7} {'DB_P':>6} {'DB_R':>6} "
          f"{'CT_Hot':>6} {'CT_MCC':>7} {'CT_P':>6} {'CT_R':>6}")
    print("-" * 120)

    for pdb_stem, feat_name in sorted(PATHOGEN_MAP.items()):
        pdb_path = os.path.join(PDB_DIR, f"{pdb_stem}.pdb")
        if not os.path.exists(pdb_path):
            print(f"WARNING: {pdb_path} not found, skipping")
            continue

        # Load data
        ca_coords = load_pdb_ca_coords(pdb_path)
        df = load_feature_matrix(feat_name)

        all_positions = set(df["position"].values)
        mutated_positions = set(df[df["freq"] > 0]["position"].values)
        gt_labels = dict(zip(df["position"], df["layer_a"].astype(int)))

        n_gt_positive = sum(1 for v in gt_labels.values() if v == 1)

        # Check how many positions map to PDB
        mapped = sum(1 for p in all_positions if (p + 1) in ca_coords)

        # DBSCAN approach
        hotspot_db, n_clusters = run_dbscan_hotspot(mutated_positions, ca_coords)
        mcc_db, prec_db, rec_db = evaluate(all_positions, hotspot_db, gt_labels)

        # Contact density approach
        hotspot_ct = run_contact_density_hotspot(mutated_positions, ca_coords)
        mcc_ct, prec_ct, rec_ct = evaluate(all_positions, hotspot_ct, gt_labels)

        print(f"{feat_name:<18} {len(all_positions):>5} {len(mutated_positions):>5} "
              f"{n_gt_positive:>5} "
              f"{n_clusters:>8} {len(hotspot_db):>6} {mcc_db:>7.3f} {prec_db:>6.3f} {rec_db:>6.3f} "
              f"{len(hotspot_ct):>6} {mcc_ct:>7.3f} {prec_ct:>6.3f} {rec_ct:>6.3f}")

        results_dbscan.append({
            "pathogen": feat_name,
            "method": "DBSCAN_3D",
            "n_positions": len(all_positions),
            "n_mutations": len(mutated_positions),
            "n_gt_positive": n_gt_positive,
            "n_mapped_to_pdb": mapped,
            "n_clusters": n_clusters,
            "n_hotspot_calls": len(hotspot_db),
            "cluster_positions": ";".join(str(p) for p in sorted(hotspot_db)),
            "mcc": round(mcc_db, 4),
            "precision": round(prec_db, 4),
            "recall": round(rec_db, 4),
        })

        results_contact.append({
            "pathogen": feat_name,
            "method": "ContactDensity_3D",
            "n_positions": len(all_positions),
            "n_mutations": len(mutated_positions),
            "n_gt_positive": n_gt_positive,
            "n_mapped_to_pdb": mapped,
            "n_clusters": 0,
            "n_hotspot_calls": len(hotspot_ct),
            "cluster_positions": ";".join(str(p) for p in sorted(hotspot_ct)),
            "mcc": round(mcc_ct, 4),
            "precision": round(prec_ct, 4),
            "recall": round(rec_ct, 4),
        })

    # Combine and save
    all_results = pd.DataFrame(results_dbscan + results_contact)
    out_path = os.path.join(OUT_DIR, "hotspot3d_results.csv")
    all_results.to_csv(out_path, index=False)
    print(f"\nResults saved to {out_path}")

    # Summary statistics
    print("\n=== Summary ===")
    for method in ["DBSCAN_3D", "ContactDensity_3D"]:
        subset = all_results[all_results["method"] == method]
        avg_mcc = subset["mcc"].mean()
        avg_prec = subset["precision"].mean()
        avg_rec = subset["recall"].mean()
        print(f"{method:>20s}:  avg MCC={avg_mcc:.3f}  avg Prec={avg_prec:.3f}  avg Rec={avg_rec:.3f}")

    # Parameter sensitivity: try different DBSCAN eps values
    print("\n=== DBSCAN Parameter Sensitivity (eps) ===")
    print(f"{'eps':>5} {'avg_MCC':>8} {'avg_Prec':>9} {'avg_Rec':>8}")
    for eps in [6.0, 8.0, 10.0, 12.0, 15.0]:
        mccs = []
        for pdb_stem, feat_name in sorted(PATHOGEN_MAP.items()):
            pdb_path = os.path.join(PDB_DIR, f"{pdb_stem}.pdb")
            if not os.path.exists(pdb_path):
                continue
            ca_coords = load_pdb_ca_coords(pdb_path)
            df = load_feature_matrix(feat_name)
            all_positions = set(df["position"].values)
            mutated_positions = set(df[df["freq"] > 0]["position"].values)
            gt_labels = dict(zip(df["position"], df["layer_a"].astype(int)))

            hotspot_db, _ = run_dbscan_hotspot(mutated_positions, ca_coords, eps=eps)
            mcc_db, _, _ = evaluate(all_positions, hotspot_db, gt_labels)
            mccs.append(mcc_db)
        print(f"{eps:>5.1f} {np.mean(mccs):>8.3f}")


if __name__ == "__main__":
    main()
