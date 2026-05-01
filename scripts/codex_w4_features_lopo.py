#!/usr/bin/env python3
"""Wave 4 Tier-2 feature/LOPO scaffold.

Task 1 implements only --audit-only. Modeling modes are reserved for later
Wave 4 tasks and intentionally raise NotImplementedError.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

import numpy as np
import pandas as pd
import scipy.stats as stats


random_seed = 42
RANDOM_SEED = random_seed
RNG = np.random.default_rng(42)

ROOT = Path(__file__).resolve().parents[1]
FEATURE_DIR = ROOT / "results" / "mutbench" / "feature_analysis"
CROSS_DIR = ROOT / "data" / "cross_pathogen"
OUT_DIR = ROOT / "results" / "mutbench" / "codex_wave4"

INVENTORY_CSV = OUT_DIR / "w4_input_inventory.csv"
SCHEMA_AUDIT_CSV = OUT_DIR / "w4_feature_schema_audit.csv"

OVERLAP_SLUGS = {"dengue_e", "hiv1_gp120", "norovirus_vp1"}
OVERLAP_PAIRS = {
    "Dengue": "dengue_e",
    "HIV-1": "hiv1_gp120",
    "Norovirus": "norovirus_vp1",
}


def slug_label(slug: str) -> str:
    return slug.replace("_", " ").replace("-", " ").title()


def clean_values(values: pd.Series) -> str:
    cleaned = []
    for value in sorted(values.dropna().unique().tolist()):
        if isinstance(value, (np.integer, int)):
            cleaned.append(int(value))
        elif isinstance(value, (np.floating, float)) and float(value).is_integer():
            cleaned.append(int(value))
        elif isinstance(value, (np.floating, float)):
            cleaned.append(float(value))
        else:
            cleaned.append(value)
    return json.dumps(cleaned, separators=(",", ":"))


def require_columns(path: Path, df: pd.DataFrame, columns: list[str]) -> None:
    missing = [column for column in columns if column not in df.columns]
    if missing:
        raise ValueError(f"{path} missing required columns: {missing}")


def build_inventory() -> pd.DataFrame:
    rows = []

    feature_paths = sorted(FEATURE_DIR.glob("feature_matrix_*.csv"))
    cross_paths = sorted(CROSS_DIR.glob("*_position_scores.csv"))

    for path in feature_paths:
        pathogen = path.stem.removeprefix("feature_matrix_")
        df = pd.read_csv(path)
        require_columns(path, df, ["position", "freq", "entropy", "layer_a"])
        rows.append(
            {
                "slug": pathogen,
                "pathogen_label": pathogen,
                "source_type": "feature_matrix",
                "is_labeled": True,
                "is_overlap": False,
                "audit_only": False,
                "unique_target_inclusion": True,
                "n_positions": int(df.shape[0]),
                "has_freq": "freq" in df.columns,
                "has_entropy": "entropy" in df.columns,
                "has_hscore": "hscore" in df.columns,
                "has_layer_a": "layer_a" in df.columns,
                "ground_truth_values": clean_values(df["layer_a"]),
            }
        )

    for path in cross_paths:
        slug = path.stem.removesuffix("_position_scores")
        is_overlap = slug in OVERLAP_SLUGS
        df = pd.read_csv(path)
        require_columns(path, df, ["position", "frequency", "entropy", "hscore", "ground_truth"])
        rows.append(
            {
                "slug": slug,
                "pathogen_label": slug_label(slug),
                "source_type": "cross_pathogen",
                "is_labeled": False,
                "is_overlap": is_overlap,
                "audit_only": is_overlap,
                "unique_target_inclusion": not is_overlap,
                "n_positions": int(df.shape[0]),
                "has_freq": "frequency" in df.columns,
                "has_entropy": "entropy" in df.columns,
                "has_hscore": "hscore" in df.columns,
                "has_layer_a": "layer_a" in df.columns,
                "ground_truth_values": clean_values(df["ground_truth"]),
            }
        )

    return pd.DataFrame(
        rows,
        columns=[
            "slug",
            "pathogen_label",
            "source_type",
            "is_labeled",
            "is_overlap",
            "audit_only",
            "unique_target_inclusion",
            "n_positions",
            "has_freq",
            "has_entropy",
            "has_hscore",
            "has_layer_a",
            "ground_truth_values",
        ],
    )


def top_fraction_positions(df: pd.DataFrame, score_col: str, fraction: float = 0.10) -> set[int]:
    n_top = max(1, int(np.ceil(df.shape[0] * fraction)))
    ranked = df.sort_values([score_col, "position"], ascending=[False, True], kind="mergesort")
    return set(ranked.head(n_top)["position"].astype(int).tolist())


def build_schema_audit() -> pd.DataFrame:
    rows = []
    for pathogen, cross_slug in OVERLAP_PAIRS.items():
        labeled_path = FEATURE_DIR / f"feature_matrix_{pathogen}.csv"
        cross_path = CROSS_DIR / f"{cross_slug}_position_scores.csv"

        labeled = pd.read_csv(labeled_path)
        cross = pd.read_csv(cross_path)
        require_columns(labeled_path, labeled, ["position", "freq", "entropy"])
        require_columns(cross_path, cross, ["position", "hscore"])

        labeled_work = labeled[["position", "freq", "entropy"]].copy()
        labeled_work["hscore_labeled"] = labeled_work["freq"] * labeled_work["entropy"]
        cross_work = cross[["position", "hscore"]].rename(columns={"hscore": "hscore_cross"})

        aligned = labeled_work.merge(cross_work, on="position", how="inner")
        if aligned.shape[0] < 2:
            rho = np.nan
            pvalue = np.nan
        else:
            result = stats.spearmanr(aligned["hscore_labeled"], aligned["hscore_cross"])
            rho = float(result.statistic)
            pvalue = float(result.pvalue)

        top_labeled = top_fraction_positions(aligned, "hscore_labeled")
        top_cross = top_fraction_positions(aligned, "hscore_cross")
        intersection = top_labeled & top_cross
        union = top_labeled | top_cross
        jaccard = float(len(intersection) / len(union)) if union else np.nan
        harmonizable = bool(rho >= 0.70 and jaccard >= 0.50)

        rows.append(
            {
                "pathogen_pair": f"{pathogen}:{cross_slug}",
                "n_positions_labeled": int(labeled.shape[0]),
                "n_positions_cross": int(cross.shape[0]),
                "n_positions_aligned": int(aligned.shape[0]),
                "spearman_rho": rho,
                "spearman_p": pvalue,
                "top10pct_jaccard": jaccard,
                "top10pct_overlap_count": int(len(intersection)),
                "harmonizable_per_threshold": harmonizable,
            }
        )

    return pd.DataFrame(
        rows,
        columns=[
            "pathogen_pair",
            "n_positions_labeled",
            "n_positions_cross",
            "n_positions_aligned",
            "spearman_rho",
            "spearman_p",
            "top10pct_jaccard",
            "top10pct_overlap_count",
            "harmonizable_per_threshold",
        ],
    )


def print_invariants(inventory: pd.DataFrame) -> bool:
    checks = [
        ("unique_target_inclusion == 28", inventory[inventory.unique_target_inclusion].shape[0] == 28),
        ("audit_only == 3", inventory[inventory.audit_only].shape[0] == 3),
        (
            "source_type feature_matrix == 12",
            inventory[inventory.source_type == "feature_matrix"].shape[0] == 12,
        ),
        (
            "source_type cross_pathogen == 19",
            inventory[inventory.source_type == "cross_pathogen"].shape[0] == 19,
        ),
    ]
    all_passed = True
    print("Inventory invariants:")
    for label, passed in checks:
        print(f"  {'PASS' if passed else 'FAIL'} {label}")
        all_passed = all_passed and passed
    return all_passed


def print_schema_summary(schema_audit: pd.DataFrame) -> None:
    print("Schema hscore overlap audit:")
    for row in schema_audit.itertuples(index=False):
        verdict = "PASS" if row.harmonizable_per_threshold else "FAIL"
        print(
            "  "
            f"{verdict} {row.pathogen_pair}: "
            f"aligned={row.n_positions_aligned}, "
            f"rho={row.spearman_rho:.4f}, "
            f"p={row.spearman_p:.4g}, "
            f"top10_jaccard={row.top10pct_jaccard:.4f}, "
            f"top10_overlap={row.top10pct_overlap_count}"
        )

    n_harmonizable = int(schema_audit["harmonizable_per_threshold"].sum())
    if n_harmonizable < 2:
        verdict = "2-core fallback recommended"
    else:
        verdict = "hscore harmonization gate passes"
    print(f"Overall hscore harmonizable pairs: {n_harmonizable}/3; {verdict}.")


def run_audit_only() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    inventory = build_inventory()
    schema_audit = build_schema_audit()

    inventory.to_csv(INVENTORY_CSV, index=False)
    schema_audit.to_csv(SCHEMA_AUDIT_CSV, index=False)

    print(f"Wrote {INVENTORY_CSV}")
    print(f"Wrote {SCHEMA_AUDIT_CSV}")
    all_invariants_passed = print_invariants(inventory)
    print_schema_summary(schema_audit)
    if not all_invariants_passed:
        raise AssertionError("One or more Wave 4 Task 1 inventory invariants failed.")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Wave 4 Tier-2 feature/LOPO scaffold")
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--audit-only", action="store_true", help="write Task 1 inventory/schema audit CSVs")
    mode.add_argument("--labeled-only", action="store_true", help="reserved for Task 2")
    mode.add_argument("--expanded", action="store_true", help="reserved for Task 3")
    mode.add_argument("--smoke", action="store_true", help="reserved for Tasks 2-3")
    mode.add_argument("--full", action="store_true", help="reserved for Tasks 2-3")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    if args.audit_only:
        run_audit_only()
        return
    raise NotImplementedError("Only --audit-only is implemented in Wave 4 Task 1.")


if __name__ == "__main__":
    main()
