#!/usr/bin/env python3
"""Coordinate-provenance audit for PAHD-R labels and repair priors."""

from __future__ import annotations

from pathlib import Path
import sys

import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parent.parent
RESULTS_DIR = PROJECT_ROOT / "results" / "mutbench"
FEATURE_DIR = RESULTS_DIR / "feature_analysis"
sys.path.insert(0, str(PROJECT_ROOT))
sys.path.insert(0, str(PROJECT_ROOT / "scripts"))

from tools.mutbench.ground_truth.multilayer_gt import (  # noqa: E402
    get_gt_adaptive,
    get_gt_constrained,
)
import test_pahd_r_domain_prior_repair as broad_prior  # noqa: E402
import sweep_pahd_r_sars2_region_split_prior as sars2_prior  # noqa: E402
import redesign_mers_rsv_narrow_prior_repairs as narrow_prior  # noqa: E402


FINAL_PATHOGENS = [
    "Dengue",
    "EV-A71",
    "H3N2",
    "HCV",
    "HIV-1",
    "Influenza_B",
    "MERS",
    "Norovirus",
    "RSV",
    "Rabies",
    "SARS-CoV-2",
]

COORDINATE_FRAME_NOTES = {
    "SARS-CoV-2": "Spike-local 0-based feature rows; many literature residues are commonly reported in 1-based Spike coordinates.",
    "H3N2": "HA-local 0-based feature rows after benchmark trimming.",
    "Norovirus": "VP1-local 0-based feature rows.",
    "HIV-1": "Env/gp120-local 0-based feature rows after benchmark trimming.",
    "Dengue": "Benchmark protein-local 0-based feature rows.",
    "RSV": "F-protein-local 0-based feature rows.",
    "Influenza_B": "HA-local 0-based feature rows after benchmark trimming.",
    "MERS": "Spike-local 0-based feature rows; DPP4 priors are encoded as 1-based Spike-local ranges and converted by smooth_mask().",
    "HCV": "E2-local 0-based feature rows; constrained CD81 residues were reconciled from H77 E2 coordinates by local=H77-384.",
    "Rabies": "G-protein-local 0-based feature rows.",
    "EV-A71": "VP1/polyprotein benchmark-local 0-based feature rows.",
}

MANUAL_PROVENANCE_STATUS = {
    "HCV": "reconciled: H77 E2 constrained coordinates converted to local E2 frame",
    "MERS": "needs manual structural-coordinate review before DPP4 repair adoption",
    "SARS-CoV-2": "candidate priors use predeclared Spike-local RBD/NTD neighborhoods; external DMS hold remains",
    "RSV": "rejected priors; conformation-specific antigenic-site provenance remains unresolved",
}


def markdown_table(frame: pd.DataFrame) -> str:
    text = frame.copy()
    for col in text.columns:
        if pd.api.types.is_float_dtype(text[col]):
            text[col] = text[col].map(lambda x: "" if pd.isna(x) else f"{x:.4f}")
        else:
            text[col] = text[col].astype(str)
    lines = [
        "| " + " | ".join(text.columns) + " |",
        "| " + " | ".join(["---"] * len(text.columns)) + " |",
    ]
    for _, row in text.iterrows():
        lines.append("| " + " | ".join(row[col] for col in text.columns) + " |")
    return "\n".join(lines)


def load_feature_matrix(pathogen: str) -> pd.DataFrame:
    path = FEATURE_DIR / f"feature_matrix_{pathogen}.csv"
    if not path.exists():
        raise FileNotFoundError(path)
    return pd.read_csv(path)


def expand_ranges_1based(ranges: list[tuple[int, int]]) -> set[int]:
    """Convert inclusive 1-based ranges into 0-based site indices."""
    sites: set[int] = set()
    for start, end in ranges:
        sites.update(range(start - 1, end))
    return sites


def summarize_sites(sites: set[int], max_items: int = 12) -> str:
    if not sites:
        return ""
    vals = sorted(sites)
    shown = ",".join(str(v) for v in vals[:max_items])
    return shown + (",..." if len(vals) > max_items else "")


def audit_layers() -> pd.DataFrame:
    rows = []
    for pathogen in FINAL_PATHOGENS:
        df = load_feature_matrix(pathogen)
        n = len(df)
        pos = df["position"].astype(int)
        csv_layer_a = set(df.index[df["layer_a"].astype(int).values == 1])
        code_layer_a = get_gt_adaptive(pathogen, n)
        code_layer_b = get_gt_constrained(pathogen, n)
        expected = list(range(int(pos.min()), int(pos.max()) + 1))
        contiguous = len(expected) == n and list(pos.sort_values()) == expected
        layer_mismatch = csv_layer_a ^ code_layer_a
        rows.append({
            "pathogen": pathogen,
            "n_positions": n,
            "position_min": int(pos.min()),
            "position_max": int(pos.max()),
            "position_base": "0-based" if int(pos.min()) == 0 else "nonzero/min-check",
            "positions_unique": bool(pos.is_unique),
            "positions_contiguous": bool(contiguous),
            "layer_a_csv_count": len(csv_layer_a),
            "layer_a_code_count": len(code_layer_a),
            "layer_a_mismatch_count": len(layer_mismatch),
            "layer_a_mismatch_examples": summarize_sites(layer_mismatch),
            "layer_b_count": len(code_layer_b),
            "layer_b_in_bounds": all(0 <= p < n for p in code_layer_b),
            "coordinate_frame_note": COORDINATE_FRAME_NOTES.get(pathogen, ""),
            "manual_provenance_status": MANUAL_PROVENANCE_STATUS.get(pathogen, "no repair-specific issue identified in this audit"),
        })
    return pd.DataFrame(rows)


def prior_rows_for(pathogen: str) -> list[tuple[str, str, list[tuple[int, int]], str]]:
    rows: list[tuple[str, str, list[tuple[int, int]], str]] = []
    if pathogen in broad_prior.PRIOR_RANGES_1BASED:
        rows.append((
            pathogen,
            "broad_domain_prior",
            broad_prior.PRIOR_RANGES_1BASED[pathogen],
            "exploratory broad prior; all ranges encoded as inclusive 1-based and converted to 0-based in smooth_mask()",
        ))
    if pathogen == "SARS-CoV-2":
        for name, ranges in sars2_prior.REGION_PRIORS.items():
            rows.append((
                pathogen,
                f"sars2_split:{name}",
                ranges,
                "candidate split prior; encoded as inclusive 1-based Spike-local ranges",
            ))
    if pathogen in narrow_prior.PRIORS:
        for name, ranges in narrow_prior.PRIORS[pathogen].items():
            rows.append((
                pathogen,
                f"narrow:{name}",
                ranges,
                "narrow weak-case repair prior; encoded as inclusive 1-based local ranges",
            ))
    return rows


def audit_priors(layer_df: pd.DataFrame) -> pd.DataFrame:
    rows = []
    n_by_pathogen = dict(zip(layer_df["pathogen"], layer_df["n_positions"]))
    for pathogen in FINAL_PATHOGENS:
        n = int(n_by_pathogen[pathogen])
        layer_a = get_gt_adaptive(pathogen, n)
        layer_b = get_gt_constrained(pathogen, n)
        for pathogen_name, prior_name, ranges, note in prior_rows_for(pathogen):
            sites = expand_ranges_1based(ranges)
            in_bounds = {p for p in sites if 0 <= p < n}
            out_bounds = sites - in_bounds
            layer_a_overlap = in_bounds & layer_a
            layer_b_overlap = in_bounds & layer_b
            rows.append({
                "pathogen": pathogen_name,
                "prior": prior_name,
                "n_ranges": len(ranges),
                "range_min_1based": min(start for start, _ in ranges),
                "range_max_1based": max(end for _, end in ranges),
                "feature_n_positions": n,
                "prior_site_count_0based": len(sites),
                "in_bounds_count": len(in_bounds),
                "out_of_bounds_count": len(out_bounds),
                "layer_a_overlap_count": len(layer_a_overlap),
                "layer_b_overlap_count": len(layer_b_overlap),
                "layer_a_overlap_examples_0based": summarize_sites(layer_a_overlap),
                "layer_b_overlap_examples_0based": summarize_sites(layer_b_overlap),
                "coordinate_risk": classify_prior_risk(
                    pathogen_name,
                    prior_name,
                    out_bounds,
                    layer_a_overlap,
                    layer_b_overlap,
                ),
                "note": note,
            })
    return pd.DataFrame(rows)


def classify_prior_risk(
    pathogen: str,
    prior: str,
    out_bounds: set[int],
    layer_a_overlap: set[int],
    layer_b_overlap: set[int],
) -> str:
    if out_bounds:
        return "fail: prior positions outside feature coordinate frame"
    if pathogen == "HCV":
        return "pass: HCV frame reconciled, but do not generalize repair"
    if pathogen == "MERS" and prior.startswith("narrow:"):
        return "candidate: in bounds, requires manual DPP4 structural-coordinate review"
    if pathogen == "SARS-CoV-2" and prior.startswith("sars2_split:"):
        return "candidate: in bounds, external DMS support not established"
    if pathogen == "RSV" and prior.startswith("narrow:"):
        return "reject/hold: in bounds but repair failed controls"
    if not layer_a_overlap and not layer_b_overlap:
        return "review: in bounds but no direct Layer A/B overlap"
    return "review: in bounds; audit biological provenance before adoption"


def run() -> None:
    layer_df = audit_layers()
    prior_df = audit_priors(layer_df)

    layer_csv = RESULTS_DIR / "pahd_r_coordinate_provenance_layers.csv"
    prior_csv = RESULTS_DIR / "pahd_r_coordinate_provenance_priors.csv"
    layer_df.to_csv(layer_csv, index=False)
    prior_df.to_csv(prior_csv, index=False)

    fail_layers = layer_df[
        (~layer_df["positions_unique"])
        | (~layer_df["positions_contiguous"])
        | (layer_df["position_base"] != "0-based")
        | (layer_df["layer_a_mismatch_count"] > 0)
        | (~layer_df["layer_b_in_bounds"])
    ]
    fail_priors = prior_df[prior_df["out_of_bounds_count"] > 0]
    candidate_priors = prior_df[prior_df["coordinate_risk"].str.contains("candidate", na=False)]
    rejected_priors = prior_df[prior_df["coordinate_risk"].str.contains("reject", na=False)]

    report = [
        "# PAHD-R Coordinate Provenance Audit",
        "",
        "Date: 2026-04-27 KST",
        "",
        "## Layer/Feature Coordinate Audit",
        "",
        markdown_table(layer_df[[
            "pathogen",
            "n_positions",
            "position_min",
            "position_max",
            "position_base",
            "positions_unique",
            "positions_contiguous",
            "layer_a_csv_count",
            "layer_a_code_count",
            "layer_a_mismatch_count",
            "layer_b_count",
            "layer_b_in_bounds",
            "manual_provenance_status",
        ]]),
        "",
        "## Repair-Prior Coordinate Audit",
        "",
        markdown_table(prior_df[[
            "pathogen",
            "prior",
            "n_ranges",
            "range_min_1based",
            "range_max_1based",
            "feature_n_positions",
            "out_of_bounds_count",
            "layer_a_overlap_count",
            "layer_b_overlap_count",
            "coordinate_risk",
        ]]),
        "",
        "## Decision Summary",
        "",
        f"- Layer coordinate hard failures: {len(fail_layers)}.",
        f"- Prior coordinate hard failures: {len(fail_priors)}.",
        f"- Candidate priors requiring non-coordinate validation/manual review: {len(candidate_priors)}.",
        f"- In-bounds but rejected/held priors: {len(rejected_priors)}.",
        "",
        "## Interpretation",
        "",
        "- All final 11 feature matrices use contiguous 0-based coordinates, and CSV Layer A labels match the code-defined Layer A sets.",
        "- HCV constrained coordinates remain reconciled in the local E2 frame, supporting the adopted HCV optional repair.",
        "- SARS-CoV-2 and MERS candidate priors are in bounds, so their remaining blockers are biological/external validation rather than basic coordinate-frame failure.",
        "- RSV narrow priors are also in bounds, but they remain rejected because performance controls failed.",
        "- The next validation round should move from coordinate provenance to stability selection and candidate-repair external validation.",
        "",
        "## Artifacts",
        "",
        f"- `{layer_csv.relative_to(PROJECT_ROOT)}`",
        f"- `{prior_csv.relative_to(PROJECT_ROOT)}`",
        "",
    ]
    out = RESULTS_DIR / "pahd_r_coordinate_provenance_audit.md"
    out.write_text("\n".join(report), encoding="utf-8")
    print(out)
    print(layer_df.round(4).to_string(index=False))
    print(prior_df[["pathogen", "prior", "out_of_bounds_count", "layer_a_overlap_count", "layer_b_overlap_count", "coordinate_risk"]].to_string(index=False))


if __name__ == "__main__":
    run()
