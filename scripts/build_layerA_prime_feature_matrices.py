#!/usr/bin/env python3
"""
Build augmented feature matrices for the 10 Class A Layer A' targets.

Output schema mirrors the 12-panel `feature_matrix_*.csv`:
  position, freq, entropy, layer_a_prime
Source: data/cross_pathogen/{slug}_position_scores.csv (frequency, entropy)
        results/mutbench/layer_a_prime/{slug}_layer_a_prime.csv (positives)
The Layer A' positions get layer_a_prime=1; all others get 0.

Output: results/mutbench/feature_matrix_layerA_prime/{slug}.csv
"""
import csv
from pathlib import Path

ROOT = Path("/proj/paper")
CROSS = ROOT / "data" / "cross_pathogen"
LAP_DIR = ROOT / "results" / "mutbench" / "layer_a_prime"
OUT_DIR = ROOT / "results" / "mutbench" / "feature_matrix_layerA_prime"
INVENTORY = ROOT / "results" / "mutbench" / "layerA_prime_inventory.csv"


def main():
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    with INVENTORY.open() as f:
        rows = list(csv.DictReader(f))
    summary = []
    print(f"{'target':<42} {'n_pos':>5} {'n_layer_a_prime':>16} {'prevalence':>10}")
    print("-" * 80)
    for r in rows:
        if r["refined_class"] != "A":
            continue
        slug = r["target"]
        cross_csv = CROSS / f"{slug}_position_scores.csv"
        lap_csv = LAP_DIR / f"{slug}_layer_a_prime.csv"
        if not cross_csv.exists() or not lap_csv.exists():
            print(f"{slug:<42} SKIP (missing input)")
            continue
        with lap_csv.open() as f:
            la_positions = {int(row["position"]) for row in csv.DictReader(f)}
        out_rows = []
        with cross_csv.open() as f:
            for row in csv.DictReader(f):
                pos = int(row["position"])
                # Map cross_pathogen 'frequency' → 'freq' for parity with feature_matrix_*.csv
                out_rows.append({
                    "position": pos,
                    "freq": row.get("frequency", row.get("freq", "")),
                    "entropy": row.get("entropy", ""),
                    "layer_a_prime": 1 if pos in la_positions else 0,
                })
        out_csv = OUT_DIR / f"{slug}.csv"
        with out_csv.open("w", newline="") as f:
            w = csv.DictWriter(f, fieldnames=["position", "freq", "entropy", "layer_a_prime"])
            w.writeheader()
            for row in out_rows:
                w.writerow(row)
        n_pos = len(out_rows)
        n_la = sum(1 for r in out_rows if r["layer_a_prime"] == 1)
        prev = n_la / n_pos if n_pos else 0
        print(f"{slug:<42} {n_pos:>5} {n_la:>16} {prev:>10.3%}")
        summary.append({"target": slug, "n_positions": n_pos, "n_layer_a_prime": n_la, "prevalence": prev})

    print(f"\nWrote {len(summary)} feature matrices to {OUT_DIR}/")
    out_idx = OUT_DIR / "_index.csv"
    with out_idx.open("w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=["target", "n_positions", "n_layer_a_prime", "prevalence"])
        w.writeheader()
        for r in summary:
            w.writerow(r)
    print(f"Index: {out_idx}")


if __name__ == "__main__":
    main()
