#!/usr/bin/env python3
"""Compute pathogen-level meta-features across the expanded 27-pathogen panel.

For each pathogen with a position-score CSV in data/cross_pathogen/, derive:
  - n_positions (alignment length)
  - mean_freq, std_freq, mean_entropy, std_entropy, mean_hscore
  - variable_pos_frac (fraction with entropy > 0.1)
  - top10pct_hscore_density (mean h-score within top-decile)

These describe how much of the pathogen-feature space is covered by the
expanded panel relative to the original 11-pathogen panel — a proxy for
whether n>=24 unlocks regions of the meta-feature space that n=11 missed.
"""

import csv
import json
import math
from pathlib import Path

CROSS = Path("/proj/paper/data/cross_pathogen")
OUT = Path("/proj/paper/results/mutbench/expanded_panel_metafeatures.csv")
OUT.parent.mkdir(exist_ok=True, parents=True)

EXISTING_11 = {
    "dengue_e", "hiv1_gp120", "norovirus_vp1",
    # Sequence-level CSVs for the other 8 (h3n2, sars2, eva71, hcv, mers, rabies, rsv, zika, infb)
    # live in their pathogen subdirs and are not in cross_pathogen/. The 3 listed above are
    # the cross_pathogen-canonical members; the remainder are tagged via their slug suffix.
}


def slug_from_csv(path):
    return path.name.replace("_position_scores.csv", "")


def stats_for(path):
    freqs, ents, hs = [], [], []
    with open(path) as f:
        r = csv.DictReader(f)
        for row in r:
            try:
                freqs.append(float(row["frequency"]))
                ents.append(float(row["entropy"]))
                hs.append(float(row["hscore"]))
            except (KeyError, ValueError):
                continue
    if not ents:
        return None
    n = len(ents)

    def mean(xs):
        return sum(xs) / len(xs)

    def std(xs):
        m = mean(xs)
        return math.sqrt(sum((x - m) ** 2 for x in xs) / max(1, len(xs) - 1))

    var_frac = sum(1 for e in ents if e > 0.1) / n
    sorted_h = sorted(hs, reverse=True)
    top_decile = sorted_h[: max(1, n // 10)]
    return {
        "n_positions": n,
        "mean_freq": round(mean(freqs), 6),
        "std_freq": round(std(freqs), 6),
        "mean_entropy": round(mean(ents), 6),
        "std_entropy": round(std(ents), 6),
        "mean_hscore": round(mean(hs), 6),
        "variable_pos_frac": round(var_frac, 4),
        "top10pct_hscore_density": round(mean(top_decile), 6),
    }


def main():
    csvs = sorted(CROSS.glob("*_position_scores.csv"))
    print(f"Found {len(csvs)} pathogen score CSVs")

    rows = []
    for c in csvs:
        s = slug_from_csv(c)
        row = stats_for(c)
        if row is None:
            print(f"  SKIP {s} — empty")
            continue
        row["slug"] = s
        rows.append(row)

    # Stats summary
    fields = [
        "slug", "n_positions", "mean_freq", "std_freq",
        "mean_entropy", "std_entropy", "mean_hscore",
        "variable_pos_frac", "top10pct_hscore_density",
    ]
    with open(OUT, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=fields)
        w.writeheader()
        for row in rows:
            w.writerow({k: row.get(k, "") for k in fields})
    print(f"Wrote {OUT}")

    # Coverage report
    print(f"\n=== Meta-feature coverage ===")
    print(f"{'pathogen':45s}{'L':>6s}{'meanH':>9s}{'varFrac':>9s}{'h-density':>11s}")
    for row in sorted(rows, key=lambda r: -r["variable_pos_frac"]):
        print(
            f"  {row['slug']:42s}{row['n_positions']:>6d}"
            f"{row['mean_entropy']:>9.4f}{row['variable_pos_frac']:>9.4f}"
            f"{row['top10pct_hscore_density']:>11.4f}"
        )

    # Range expansion: compute std across the panel for each meta-feature
    print(f"\n=== Panel-level meta-feature spread (std across pathogens) ===")
    for k in ["mean_freq", "std_freq", "mean_entropy", "std_entropy",
              "mean_hscore", "variable_pos_frac", "top10pct_hscore_density"]:
        vals = [r[k] for r in rows]
        m = sum(vals) / len(vals)
        sd = math.sqrt(sum((v - m) ** 2 for v in vals) / max(1, len(vals) - 1))
        print(f"  {k:30s}  mean={m:>8.4f}  std={sd:>8.4f}  range=[{min(vals):.4f}, {max(vals):.4f}]")


if __name__ == "__main__":
    main()
