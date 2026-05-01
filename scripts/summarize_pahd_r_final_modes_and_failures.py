#!/usr/bin/env python3
"""Final-mode reporting table and pathogen-level failure audit for PAHD-R."""

from __future__ import annotations

from pathlib import Path
import sys

import numpy as np
import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parent.parent
RESULTS_DIR = PROJECT_ROOT / "results" / "mutbench"
sys.path.insert(0, str(PROJECT_ROOT / "scripts"))
import run_pahd_r_multi_hypothesis as pahd  # noqa: E402


MODE_TO_STRATEGY = {
    "PAHD-R-Core": "non_ai_core_fusion",
    "PAHD-R-Augmented": "h11_soft_constraint_post",
    "PAHD-R-Review": "rank_cluster_aug:recurrence+diversity+phylo@top8",
}

MODE_USE = {
    "PAHD-R-Core": "no-AI exact/top-k baseline",
    "PAHD-R-Augmented": "balanced region-prioritization default",
    "PAHD-R-Review": "low-FPR conservative review mode",
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


def load_required_csv(name: str) -> pd.DataFrame:
    path = RESULTS_DIR / name
    if not path.exists():
        raise FileNotFoundError(path)
    return pd.read_csv(path)


def build_final_mode_table() -> pd.DataFrame:
    decoy_summary = load_required_csv("pahd_r_decoy_control_summary.csv")
    decoy_results = load_required_csv("pahd_r_decoy_control_results.csv")
    adv_global = load_required_csv("pahd_r_adversarial_global_summary.csv")
    review_global_path = RESULTS_DIR / "pahd_r_review_permutation_global_summary.csv"
    review_global = pd.read_csv(review_global_path) if review_global_path.exists() else pd.DataFrame()

    real_modes = list(MODE_TO_STRATEGY)
    decoy_only = decoy_results[~decoy_results["strategy"].isin(real_modes)]
    max_decoy_exact = float(decoy_only.groupby("strategy")["mcc_exact"].mean().max())
    max_decoy_precision = float(decoy_only.groupby("strategy")["precision_20"].mean().max())

    rows = []
    for mode in real_modes:
        row = decoy_summary[decoy_summary["strategy"] == mode].iloc[0]
        strategy = MODE_TO_STRATEGY[mode]
        adv = adv_global[adv_global["strategy"] == strategy]
        if len(adv):
            perm_status = (
                f"pass, p={float(adv.iloc[0]['empirical_p_null_ge_observed']):.4f}"
            )
        elif mode == "PAHD-R-Review" and len(review_global):
            perm_status = (
                f"pass, p={float(review_global.iloc[0]['empirical_p_null_ge_observed']):.4f}"
            )
        else:
            perm_status = "not run for this derived review mode"
        rows.append({
            "mode": mode,
            "representative_strategy": strategy,
            "exact_mcc": row["mean_mcc_exact"],
            "mcc_window_10": row["mean_mcc_window_10"],
            "precision_20": row["mean_precision_20"],
            "constrained_fpr": row["mean_constrained_fpr"],
            "coverage_10": row["mean_region_coverage_10"],
            "positive_pathogens": int(row["positive_pathogens"]),
            "permutation_status": perm_status,
            "decoy_exact_margin": row["mean_mcc_exact"] - max_decoy_exact,
            "decoy_precision_margin": row["mean_precision_20"] - max_decoy_precision,
            "recommended_use": MODE_USE[mode],
        })
    return pd.DataFrame(rows)


def feature_health(pathogen: str, df: pd.DataFrame) -> dict[str, float]:
    y = df["layer_a"].astype(int).values
    out = {
        "n_positions": len(df),
        "n_layer_a": int(y.sum()),
        "prevalence": float(y.mean()),
    }
    for feature in pahd.FEATURES:
        x = np.nan_to_num(df[feature].values, nan=0.0)
        out[f"{feature}_std"] = float(np.std(x))
        if y.sum() > 1 and (len(y) - y.sum()) > 1 and np.std(x) > 1e-12:
            try:
                from sklearn.metrics import roc_auc_score

                auc = float(roc_auc_score(y, x))
            except ValueError:
                auc = np.nan
        else:
            auc = np.nan
        out[f"{feature}_auc"] = auc
    return out


def top_feature_summary(health: dict[str, float]) -> tuple[str, str]:
    aucs = []
    weak = []
    for feature in pahd.FEATURES:
        auc = health.get(f"{feature}_auc", np.nan)
        std = health.get(f"{feature}_std", 0.0)
        if pd.notna(auc):
            aucs.append((feature, abs(float(auc) - 0.5), float(auc)))
        if std < 1e-8:
            weak.append(feature)
    aucs.sort(key=lambda item: item[1], reverse=True)
    top = ", ".join(f"{feat}:{auc:.2f}" for feat, _, auc in aucs[:3])
    low_var = ", ".join(weak[:4]) if weak else ""
    return top, low_var


def build_failure_audit() -> pd.DataFrame:
    data = pahd.load_feature_matrices()
    decoy_results = load_required_csv("pahd_r_decoy_control_results.csv")
    coord = load_required_csv("pahd_r_coordinate_robustness_results.csv")
    null_summary = load_required_csv("pahd_r_adversarial_null_summary.csv")
    review_null_path = RESULTS_DIR / "pahd_r_review_permutation_per_pathogen.csv"
    if review_null_path.exists():
        review_null = pd.read_csv(review_null_path)
        review_null = review_null.rename(columns={
            "observed_mcc_exact": "observed_mcc_exact",
        })
    else:
        review_null = pd.DataFrame()

    real_modes = list(MODE_TO_STRATEGY)
    decoy_only = decoy_results[~decoy_results["strategy"].isin(real_modes)]
    max_decoy_by_pathogen = decoy_only.groupby("pathogen").agg(
        max_decoy_exact=("mcc_exact", "max"),
        max_decoy_precision_20=("precision_20", "max"),
    )

    rows = []
    for pathogen in sorted(set(decoy_results["pathogen"])):
        if pathogen not in data:
            continue
        health = feature_health(pathogen, data[pathogen])
        top_features, low_var_features = top_feature_summary(health)
        for mode in real_modes:
            current = decoy_results[
                (decoy_results["pathogen"] == pathogen)
                & (decoy_results["strategy"] == mode)
            ].iloc[0]
            strategy = MODE_TO_STRATEGY[mode]
            null_key = strategy
            null_row = null_summary[
                (null_summary["pathogen"] == pathogen)
                & (null_summary["strategy"] == null_key)
            ]
            if len(null_row):
                exceeds_null = bool(null_row.iloc[0]["exceeds_null_p95"])
                null_p95 = float(null_row.iloc[0]["null_p95_mcc"])
            elif mode == "PAHD-R-Review" and len(review_null):
                review_row = review_null[
                    (review_null["pathogen"] == pathogen)
                    & (review_null["strategy"] == "PAHD-R-Review")
                ]
                if len(review_row):
                    exceeds_null = bool(review_row.iloc[0]["exceeds_null_p95"])
                    null_p95 = float(review_row.iloc[0]["null_p95_mcc"])
                else:
                    exceeds_null = np.nan
                    null_p95 = np.nan
            else:
                exceeds_null = np.nan
                null_p95 = np.nan

            coord_mode = coord[
                (coord["pathogen"] == pathogen)
                & (coord["strategy"] == mode)
                & (coord["window"] == 10)
            ]
            base = coord_mode[coord_mode["label_shift"] == 0].iloc[0]
            shifted = coord_mode[coord_mode["label_shift"] != 0]
            exact_drop = float(base["mcc_exact"] - shifted["mcc_exact"].min())
            window_inflation = float(shifted["mcc_window"].max() - base["mcc_window"])

            max_decoy = max_decoy_by_pathogen.loc[pathogen]
            flags = []
            if health["n_layer_a"] < 15:
                flags.append("label_sparse")
            if current["mcc_exact"] < 0.10:
                flags.append("weak_exact")
            if current["precision_20"] < 0.10:
                flags.append("weak_top20")
            if pd.notna(exceeds_null) and not exceeds_null:
                flags.append("not_above_null_p95")
            if current["region_coverage"] > 0.50:
                flags.append("broad_region")
            if window_inflation > 0.04:
                flags.append("window_shift_sensitive")
            if pd.isna(current["constrained_fpr"]):
                flags.append("constraint_coords_missing")
            elif current["constrained_fpr"] > 0.15:
                flags.append("high_constrained_fpr")
            if current["mcc_exact"] - max_decoy["max_decoy_exact"] < 0.03:
                flags.append("small_decoy_margin")

            rows.append({
                "pathogen": pathogen,
                "mode": mode,
                "n_positions": int(health["n_positions"]),
                "n_layer_a": int(health["n_layer_a"]),
                "prevalence": health["prevalence"],
                "exact_mcc": current["mcc_exact"],
                "mcc_window_10": current["mcc_window"],
                "precision_20": current["precision_20"],
                "constrained_fpr": current["constrained_fpr"],
                "coverage_10": current["region_coverage"],
                "null_p95_exact": null_p95,
                "exceeds_null_p95": exceeds_null,
                "decoy_exact_margin": current["mcc_exact"] - max_decoy["max_decoy_exact"],
                "decoy_precision_margin": current["precision_20"] - max_decoy["max_decoy_precision_20"],
                "shift_exact_drop": exact_drop,
                "shift_window_inflation": window_inflation,
                "top_feature_auc": top_features,
                "low_variance_features": low_var_features,
                "flags": ";".join(flags) if flags else "ok",
            })
    return pd.DataFrame(rows)


def summarize_flags(audit: pd.DataFrame) -> pd.DataFrame:
    rows = []
    for mode, group in audit.groupby("mode"):
        all_flags: list[str] = []
        for flags in group["flags"]:
            all_flags.extend([flag for flag in str(flags).split(";") if flag and flag != "ok"])
        counts = pd.Series(all_flags).value_counts()
        for flag, count in counts.items():
            rows.append({"mode": mode, "flag": flag, "pathogen_count": int(count)})
    return pd.DataFrame(rows).sort_values(["mode", "pathogen_count", "flag"], ascending=[True, False, True])


def write_report(final_modes: pd.DataFrame, audit: pd.DataFrame, flag_summary: pd.DataFrame) -> None:
    weak = audit[audit["flags"] != "ok"].copy()
    weak["severity_score"] = (
        (weak["exact_mcc"] < 0.10).astype(int)
        + (weak["precision_20"] < 0.10).astype(int)
        + weak["flags"].str.contains("not_above_null_p95", regex=False).astype(int)
        + weak["flags"].str.contains("label_sparse", regex=False).astype(int)
        + weak["flags"].str.contains("constraint_coords_missing", regex=False).astype(int)
    )
    weak = weak.sort_values(["severity_score", "pathogen", "mode"], ascending=[False, True, True])

    lines = [
        "# PAHD-R Final Modes and Failure Audit",
        "",
        "Date: 2026-04-26 KST",
        "",
        "## Final Mode Table",
        "",
        markdown_table(final_modes),
        "",
        "## Failure-Flag Summary",
        "",
        markdown_table(flag_summary) if len(flag_summary) else "No failure flags.",
        "",
        "## Highest-Priority Failure Rows",
        "",
        markdown_table(weak.head(24)[[
            "pathogen",
            "mode",
            "n_layer_a",
            "exact_mcc",
            "mcc_window_10",
            "precision_20",
            "constrained_fpr",
            "decoy_exact_margin",
            "shift_window_inflation",
            "flags",
        ]]),
        "",
        "## Interpretation",
        "",
        "- `PAHD-R-Core` remains the strongest no-AI exact/top-k mode.",
        "- `PAHD-R-Augmented` remains the balanced default for region prioritization.",
        "- `PAHD-R-Review` has the lowest constrained FPR and highest window MCC; it should still be described as a conservative review mode rather than the exact/top-k default.",
        "- Weak rows are concentrated in sparse or pathogen-specific regimes; they should be treated as follow-up targets, not hidden by the global mean.",
        "- Region-level metrics remain useful only when paired with exact MCC, Precision@20, constrained FPR, and coverage.",
        "",
        "## Next Experimental Actions",
        "",
        "1. Run a label-sparsity stress test for MERS and other low-positive pathogens.",
        "2. Reconcile HCV constrained-coordinate metadata.",
        "3. Add domain priors for RSV F, MERS RBD-DPP4, and SARS-CoV-2 distributed regions.",
        "4. Test whether pathogen-specific priors improve weak cases without damaging global decoy/permutation audits.",
        "",
    ]
    (RESULTS_DIR / "pahd_r_final_modes_and_failure_audit.md").write_text("\n".join(lines), encoding="utf-8")


def run() -> None:
    final_modes = build_final_mode_table()
    audit = build_failure_audit()
    flag_summary = summarize_flags(audit)

    final_modes.to_csv(RESULTS_DIR / "pahd_r_final_mode_table.csv", index=False)
    audit.to_csv(RESULTS_DIR / "pahd_r_pathogen_failure_audit.csv", index=False)
    flag_summary.to_csv(RESULTS_DIR / "pahd_r_failure_flag_summary.csv", index=False)
    write_report(final_modes, audit, flag_summary)

    print(RESULTS_DIR / "pahd_r_final_modes_and_failure_audit.md")
    print(final_modes.round(4).to_string(index=False))
    print()
    print(flag_summary.to_string(index=False))


if __name__ == "__main__":
    run()
