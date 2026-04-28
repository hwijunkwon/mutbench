#!/usr/bin/env python3
"""Tier B1 (cycle 4): Per-pathogen Tranception--ESM-LLR correlation measurement.

This script (re-)measures, for each of the 12 pathogens that have both a
Tranception per-position score CSV and an ESM-2 LLR ``.npy`` array, the
position-level Pearson and Spearman correlations between the two PLM
channels.  It writes a self-contained supplementary CSV with columns:

    pathogen, n_positions, sample_overlap, pearson_rho, pearson_p,
    spearman_rho, spearman_p, status

so that the dissertation supplementary table is reproducible and
verifiable from a single command.  Numerical values are saved at full
float64 precision; the LaTeX table formats them at 3 decimal places.

Outputs
-------
results/mutbench/feature_analysis/tranception_esm_correlation_per_pathogen.csv
    Tier B1 supplementary table (this file).

Notes
-----
* ESM-LLR vectors are stored as ``.npy`` indexed 0..N-1.
* Tranception score CSVs are stored with columns ``position`` (0-based,
  contiguous) and ``tranception_score``.
* When the two arrays disagree in length (HIV-1: ESM=450, TRA=480; Rabies:
  ESM=524, TRA=490; EV-A71: ESM=297, TRA=260; Zika: ESM=504, TRA=451) we
  take the prefix of length ``min(len(ESM), len(TRA))`` from both and
  record this in the ``sample_overlap`` column.  The ``n_positions``
  column reports the size of that overlap (positions actually used in
  the correlation), and ``sample_overlap`` reports the fraction
  ``overlap / max(len(ESM), len(TRA))`` to make truncation visible.
* ``status`` is ``"ok"`` when the correlation completed; ``"err"`` if a
  numerical issue was encountered.
"""

from __future__ import annotations

import os
import sys
from typing import Optional

import numpy as np
import pandas as pd
from scipy.stats import pearsonr, spearmanr

REPO = "/proj/paper"
ESM_DIR = os.path.join(REPO, "results/mutbench/esm_scores")
FEAT_DIR = os.path.join(REPO, "results/mutbench/feature_analysis")
OUT_PATH = os.path.join(FEAT_DIR, "tranception_esm_correlation_per_pathogen.csv")

# Display order: alphabetical on the public benchmark, with Zika last (it is
# the Stage-3-only 12th pathogen).
PATHOGENS = [
    "SARS-CoV-2",
    "H3N2",
    "Influenza_B",
    "HCV",
    "HIV-1",
    "RSV",
    "Norovirus",
    "Dengue",
    "MERS",
    "Rabies",
    "EV-A71",
    "Zika",
]


def _load_tranception(name: str) -> Optional[np.ndarray]:
    path = os.path.join(FEAT_DIR, f"{name}_tranception.csv")
    if not os.path.exists(path):
        return None
    df = pd.read_csv(path)
    if "position" not in df.columns or "tranception_score" not in df.columns:
        raise ValueError(f"{path}: missing required columns")
    df = df.sort_values("position").reset_index(drop=True)
    n = int(df["position"].max()) + 1
    arr = np.full(n, np.nan, dtype=np.float64)
    arr[df["position"].astype(int).values] = df["tranception_score"].values
    return arr


def _load_esm_llr(name: str) -> Optional[np.ndarray]:
    path = os.path.join(ESM_DIR, f"{name}_esm_llr.npy")
    if not os.path.exists(path):
        return None
    return np.load(path).astype(np.float64)


def _measure(name: str) -> dict:
    tra = _load_tranception(name)
    esm = _load_esm_llr(name)
    row = {
        "pathogen": name,
        "len_tranception": 0 if tra is None else int(tra.size),
        "len_esm_llr": 0 if esm is None else int(esm.size),
        "n_positions": 0,
        "sample_overlap": np.nan,
        "pearson_rho": np.nan,
        "pearson_p": np.nan,
        "spearman_rho": np.nan,
        "spearman_p": np.nan,
        "status": "missing",
    }
    if tra is None or esm is None:
        return row

    n_use = int(min(tra.size, esm.size))
    n_max = int(max(tra.size, esm.size))
    x = tra[:n_use]
    y = esm[:n_use]
    mask = np.isfinite(x) & np.isfinite(y)
    n_eff = int(mask.sum())
    row["n_positions"] = n_eff
    row["sample_overlap"] = float(n_use / n_max) if n_max > 0 else np.nan

    if n_eff < 3:
        row["status"] = "err"
        return row

    try:
        pr, pp = pearsonr(x[mask], y[mask])
        sr, sp = spearmanr(x[mask], y[mask])
    except Exception as exc:  # pragma: no cover
        row["status"] = f"err:{exc}"
        return row

    row["pearson_rho"] = float(pr)
    row["pearson_p"] = float(pp)
    row["spearman_rho"] = float(sr)
    row["spearman_p"] = float(sp)
    row["status"] = "ok"
    return row


def main() -> int:
    rows = [_measure(p) for p in PATHOGENS]
    df = pd.DataFrame(rows, columns=[
        "pathogen", "n_positions", "sample_overlap",
        "pearson_rho", "pearson_p", "spearman_rho", "spearman_p",
        "len_tranception", "len_esm_llr", "status",
    ])
    df.to_csv(OUT_PATH, index=False)
    print(f"Wrote {OUT_PATH}")
    # Compact stdout summary for the report.
    with pd.option_context("display.float_format", "{:0.4f}".format,
                           "display.width", 200, "display.max_columns", 20):
        print(df.to_string(index=False))

    # Identify highlighted pathogens for the ch5 anchor.
    ok = df[df["status"] == "ok"].copy()
    if not ok.empty:
        most_collinear = ok.loc[ok["pearson_rho"].idxmax()]
        most_dissoc = ok.loc[ok["pearson_rho"].idxmin()]
        print()
        print(f"Highest Pearson rho : {most_collinear['pathogen']} "
              f"(rho={most_collinear['pearson_rho']:.3f}, "
              f"n={int(most_collinear['n_positions'])})")
        print(f"Lowest  Pearson rho : {most_dissoc['pathogen']} "
              f"(rho={most_dissoc['pearson_rho']:.3f}, "
              f"p={most_dissoc['pearson_p']:.3g}, "
              f"n={int(most_dissoc['n_positions'])})")

    return 0


if __name__ == "__main__":
    sys.exit(main())
