#!/usr/bin/env python3
"""Build Wave 4 Task 4 figure and report from precomputed CSV outputs."""

from __future__ import annotations

import os
from pathlib import Path

os.environ.setdefault("MPLCONFIGDIR", "/tmp/matplotlib")

import matplotlib.pyplot as plt
import pandas as pd
from matplotlib.patches import Rectangle


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "results" / "mutbench" / "codex_wave4"
REPORT = ROOT / "paper" / "dissertation" / "review" / "2026-04-30" / "wave4" / "w4_tier2_features_lopo.md"
FIGURE = OUT / "w4_summary_figure.png"


def fmt(value: float, digits: int = 3) -> str:
    return f"{value:.{digits}f}"


def bool_text(value: object) -> str:
    return "True" if bool(int(value)) else "False"


def build_figure() -> None:
    per_fold = pd.read_csv(OUT / "w4_labeled_lopo_per_fold.csv")
    stability = pd.read_csv(OUT / "w4_expanded_stability_per_target.csv")
    scores = pd.read_csv(OUT / "w4_expanded_target_scores.csv")
    quorum = pd.read_csv(OUT / "w4_expanded_quorum_reachability.csv").iloc[0]

    fig, axes = plt.subplots(2, 2, figsize=(14, 10), dpi=200)

    # Panel A: per-fold labeled MCC comparison.
    ax = axes[0, 0]
    ordered = per_fold.sort_values("mcc_top10", ascending=False).reset_index(drop=True)
    x = range(len(ordered))
    width = 0.38
    ax.bar([i - width / 2 for i in x], ordered["mcc_top10"], width, label="2-core MCC", color="#3b82f6")
    ax.bar(
        [i + width / 2 for i in x],
        ordered["historical_4core_mcc_top10"],
        width,
        label="Recomputed 4-core MCC",
        color="#94a3b8",
    )
    ax.axhline(0, color="#111827", linewidth=1.0)
    ax.set_xticks(list(x))
    ax.set_xticklabels(ordered["pathogen"], rotation=45, ha="right")
    ax.set_ylabel("Top-10% MCC")
    ax.set_title("A. Labeled LOPO MCC")
    ax.legend(frameon=False, fontsize=9)
    ax.grid(axis="y", alpha=0.25)

    # Panel B: per-target stability thresholds.
    ax = axes[0, 1]
    for is_labeled, marker, color, label in [
        (1, "^", "#2563eb", "Labeled (12)"),
        (0, "o", "#f97316", "Unlabeled (16)"),
    ]:
        subset = stability[stability["is_labeled"] == is_labeled]
        ax.scatter(
            subset["median_pairwise_jaccard"],
            subset["p10_pairwise_jaccard"],
            s=55,
            marker=marker,
            color=color,
            edgecolor="white",
            linewidth=0.6,
            label=label,
            alpha=0.9,
        )
    ax.axvline(0.60, color="#374151", linestyle="--", linewidth=1.0)
    ax.axhline(0.40, color="#374151", linestyle="--", linewidth=1.0)
    ax.set_xlim(-0.03, 1.03)
    ax.set_ylim(-0.03, max(0.52, stability["p10_pairwise_jaccard"].max() + 0.08))
    ax.set_xlabel("Median pairwise Jaccard")
    ax.set_ylabel("10th percentile pairwise Jaccard")
    ax.set_title("B. Per-target bootstrap stability")
    ax.legend(frameon=False, fontsize=9, loc="upper left")
    ax.grid(alpha=0.25)

    # Panel C: feature-spread coverage and labeled envelope.
    ax = axes[1, 0]
    labeled = scores[scores["is_labeled"] == 1]
    xmin, xmax = labeled["mean_freq"].min(), labeled["mean_freq"].max()
    ymin, ymax = labeled["mean_entropy"].min(), labeled["mean_entropy"].max()
    ax.add_patch(
        Rectangle(
            (xmin, ymin),
            xmax - xmin,
            ymax - ymin,
            facecolor="#d1d5db",
            edgecolor="#6b7280",
            alpha=0.28,
            label="Labeled envelope",
        )
    )
    for is_labeled, marker, color, label in [
        (1, "^", "#2563eb", "Labeled"),
        (0, "o", "#f97316", "Unlabeled"),
    ]:
        subset = scores[scores["is_labeled"] == is_labeled]
        ax.scatter(
            subset["mean_freq"],
            subset["mean_entropy"],
            s=55,
            marker=marker,
            color=color,
            edgecolor="white",
            linewidth=0.6,
            alpha=0.9,
            label=label,
        )
    ax.set_xlabel("Mean frequency")
    ax.set_ylabel("Mean entropy")
    ax.set_title("C. Feature-spread coverage")
    ax.legend(frameon=False, fontsize=9)
    ax.grid(alpha=0.25)

    # Panel D: sign-fitting bootstrap stability.
    ax = axes[1, 1]
    bars = [
        ("freq", quorum["pct_bootstrap_sign_freq_matches_full"]),
        ("entropy", quorum["pct_bootstrap_sign_entropy_matches_full"]),
    ]
    ax.bar([b[0] for b in bars], [b[1] for b in bars], color=["#10b981", "#14b8a6"], width=0.55)
    for idx, (_, value) in enumerate(bars):
        ax.text(idx, value + 2, f"{value:.1f}%", ha="center", va="bottom", fontsize=11)
    ax.set_ylim(0, 105)
    ax.set_ylabel("Bootstrap matches full-sample sign (%)")
    ax.set_title("D. Sign-fitting stability")
    ax.grid(axis="y", alpha=0.25)

    fig.suptitle("Wave 4 Tier-2 Features-Only LOPO Summary", fontsize=16, y=0.98)
    fig.tight_layout(rect=[0, 0, 1, 0.96])
    fig.savefig(FIGURE)
    plt.close(fig)


def pathogen_table(per_fold: pd.DataFrame) -> str:
    columns = [
        "Pathogen",
        "n",
        "Layer A",
        "2-core MCC",
        "4-core MCC",
        "Delta",
        "P@20",
        "D1",
    ]
    lines = ["| " + " | ".join(columns) + " |", "|" + "|".join(["---"] + ["---:"] * 7) + "|"]
    for row in per_fold.itertuples(index=False):
        lines.append(
            "| "
            + " | ".join(
                [
                    str(row.pathogen),
                    str(row.n_positions),
                    str(row.n_layer_a_pos),
                    fmt(row.mcc_top10, 3),
                    fmt(row.historical_4core_mcc_top10, 3),
                    fmt(row.delta_2core_minus_4core, 3),
                    fmt(row.precision_at_20, 2),
                    "pass" if row.callability_d1_pass else "fail",
                ]
            )
            + " |"
        )
    return "\n".join(lines)


def top_line_table(summary: pd.Series, schema: pd.DataFrame, quorum: pd.Series) -> str:
    rows = [
        (
            "hscore harmonization audit",
            f"{int(schema['harmonizable_per_threshold'].sum())}/{len(schema)} PASS",
            "2-core fallback active",
        ),
        (
            "Labeled 12-fold 2-core LOPO",
            f"mean MCC {summary['mean_mcc_top10']:.3f}; {int(summary['n_positive_mcc'])}/12 positive",
            f"paired Wilcoxon vs 4-core p={summary['paired_wilcoxon_2core_vs_4core_greater_p']:.3f}",
        ),
        (
            "D1 callability recheck",
            f"{int(summary['d1_callability_recheck_pass_count'])}/12",
            "Matches Wave 2 failure mode",
        ),
        (
            "Expanded 28-target stability",
            f"{int(quorum['n_usable_targets'])}/28 pass; {int(quorum['n_inside_envelope'])}/16 unlabeled inside envelope",
            f"quorum_pass={bool_text(quorum['quorum_pass'])}",
        ),
        (
            "Sign-fitting bootstrap",
            f"freq {quorum['pct_bootstrap_sign_freq_matches_full']:.1f}%; entropy {quorum['pct_bootstrap_sign_entropy_matches_full']:.1f}%",
            "Matches full-sample sign",
        ),
    ]
    lines = ["| Finding | Result | Interpretation |", "|---|---:|---|"]
    lines.extend(f"| {a} | {b} | {c} |" for a, b, c in rows)
    return "\n".join(lines)


def build_report() -> None:
    per_fold = pd.read_csv(OUT / "w4_labeled_lopo_per_fold.csv")
    summary = pd.read_csv(OUT / "w4_labeled_lopo_summary.csv").iloc[0]
    schema = pd.read_csv(OUT / "w4_feature_schema_audit.csv")
    inventory = pd.read_csv(OUT / "w4_input_inventory.csv")
    quorum = pd.read_csv(OUT / "w4_expanded_quorum_reachability.csv").iloc[0]

    n_unique = int(inventory["unique_target_inclusion"].sum())
    n_labeled = int(inventory["is_labeled"].sum())
    n_cross = int((inventory["source_type"] == "cross_pathogen").sum())
    n_overlap = int(inventory["is_overlap"].sum())
    n_unlabeled = int(((inventory["unique_target_inclusion"]) & (~inventory["is_labeled"])).sum())

    report = f"""# Wave 4 — Tier-2 Features-Only LOPO

**Status:** Complete — 2026-05-01  
**Spec:** `docs/plans/2026-04-30-wave4-tier2-features-lopo.md` §Task 4  
**Plan:** `docs/plans/2026-04-30-wave4-tier2-features-lopo.md`  
**Codex review:** `paper/dissertation/review/2026-04-30/codex_wave4_plan_review.md`  
**Branch:** `experiments/waves`

## Command

```bash
cd /proj/paper && python scripts/codex_w4_features_lopo.py --audit-only
cd /proj/paper && python scripts/codex_w4_features_lopo.py --labeled-only | tee results/mutbench/codex_wave4/w4_labeled_lopo.log
cd /proj/paper && python scripts/codex_w4_features_lopo.py --expanded | tee results/mutbench/codex_wave4/w4_expanded_stability.log
cd /proj/paper && python scripts/codex_w4_task4_summary.py
```

Run logs: `results/mutbench/codex_wave4/w4_labeled_lopo.log`; `results/mutbench/codex_wave4/w4_expanded_stability.log`.

## Method

Wave 4 used the Option E hybrid design: labeled performance evaluation remained restricted to the original 12 Layer-A targets, while the expanded 28-target union was diagnostic only. The expanded component assessed feature-space coverage, bootstrap rank stability, and structural quorum reachability; it did not compute unlabeled Layer-A performance, callability, or validation endpoints.

The hscore overlap audit failed on all three audit pairs (`Dengue:dengue_e`, `HIV-1:hiv1_gp120`, `Norovirus:norovirus_vp1`), with {int(schema['harmonizable_per_threshold'].sum())}/{len(schema)} passing the predeclared harmonization threshold. Per the review, hscore was therefore excluded from expanded diagnostics and the analysis used the 2-core fallback `freq,entropy`.

Algorithm 1 sign fitting was preserved on labeled folds: for each held-out pathogen, signs were fit only from the other 11 labeled pathogens, then applied to the held-out fold. Expanded stability used 1,000 bootstrap sign fits with `random_seed=42`, resampling labeled pathogens with replacement; unlabeled targets were scored after sign fitting and were never sampled into the sign estimator.

## Inputs

Denominators: `n_unique_targets={n_unique}`, `n_labeled_eval={n_labeled}`, `n_cross_pathogen_csv={n_cross}`, `n_overlap={n_overlap}`, `n_unlabeled_expanded={n_unlabeled}`. The three overlap cross-pathogen files were audit-only and excluded from unique-target counts.

## Top-Line Findings

{top_line_table(summary, schema, quorum)}

## Per-Pathogen Labeled MCC Table

{pathogen_table(per_fold)}

## Failure-Mode Branch Applied

Two predeclared branches govern the interpretation.

Branch 5 fired first because hscore drift was large:

> If Dengue/HIV-1/Norovirus feature_matrix-derived hscore rankings and cross_pathogen hscore rankings have median Spearman rho <0.70 or top-10% Jaccard <0.50, exclude hscore from expanded diagnostics and rerun/report a 2-core `freq, entropy` sensitivity, or stop at the input-audit stage if the 2-core rerun is not performed.

After the 2-core fallback, the closest outcome branch is Branch 2: labeled 2-core performance was bounded positive, but expanded stability was weak.

> Preserve the descriptive labeled-panel signal, but conclude that the 19 features-only targets are too heterogeneous or schema-shifted for stable transfer without additional feature harmonization. Next step becomes Layer A pilot plus feature augmentation, not expanded callability.

The 16/16 unlabeled envelope result is structurally useful, but `quorum_pass=False` prevents any expanded callability claim.

## Comparison with Wave 1+2+3

- Wave 1 P1: 5/12 pathogens were individually significant under the iid null.
- Wave 2 P5: 0/12 targets were callable; the D1 quorum was unreachable at 7/11.
- Wave 3 P6: H3N2, Norovirus, Dengue, and Influenza_B survived all four biological-realistic nulls; Norovirus survived 4/4 P6 nulls and the P1 local-burden null.
- Wave 4: 2-core performance was bounded positive and statistically indistinguishable from the recomputed 4-core comparator, D1 remained 0/12 callable, expanded stability was 1/28, and 16/16 unlabeled targets fell inside the labeled feature envelope.

Triangulation: the panel-size constraint is confirmed, but not solved by features-only expansion. Layer A curation remains the rate-limiting next step.

## Caveats

- hscore non-harmonizability is a finding, not an execution failure.
- 2-core approximately matching 4-core means hscore/pLDDT are not the current bottleneck in this labeled sensitivity analysis.
- The 1/28 stability result is bootstrap instability of sign fitting, not evidence that the 16 new targets are biologically bad.
- The 16/16 envelope result means the new targets are feature-compatible enough for Layer A curation to proceed.

## Files Produced

- `results/mutbench/codex_wave4/w4_input_inventory.csv`
- `results/mutbench/codex_wave4/w4_feature_schema_audit.csv`
- `results/mutbench/codex_wave4/w4_labeled_lopo_per_fold.csv`
- `results/mutbench/codex_wave4/w4_labeled_lopo_summary.csv`
- `results/mutbench/codex_wave4/w4_labeled_callability_recheck.csv`
- `results/mutbench/codex_wave4/w4_expanded_stability_per_target.csv`
- `results/mutbench/codex_wave4/w4_expanded_quorum_reachability.csv`
- `results/mutbench/codex_wave4/w4_summary_figure.png`
- `paper/dissertation/review/2026-04-30/wave4/w4_tier2_features_lopo.md`

## Decision

Wave 5 ordering remains pilot 3 Layer A curation for YFV/Lassa/WNV, per the Codex plan review Wave 5 ordering recommendation. The condition was that labeled 3-core/2-core performance not be clearly negative; the observed 2-core mean MCC was {summary['mean_mcc_top10']:.3f}, with {int(summary['n_positive_mcc'])}/12 positive folds, so the result is bounded positive. The pilot must still be interpreted as curation toward a future quorum test, not as validation from Wave 4.

## Cross-References

- Figure: `results/mutbench/codex_wave4/w4_summary_figure.png`
- Labeled folds: `results/mutbench/codex_wave4/w4_labeled_lopo_per_fold.csv`
- Expanded stability: `results/mutbench/codex_wave4/w4_expanded_stability_per_target.csv`
- Quorum diagnostic: `results/mutbench/codex_wave4/w4_expanded_quorum_reachability.csv`
"""
    REPORT.parent.mkdir(parents=True, exist_ok=True)
    REPORT.write_text(report, encoding="utf-8")


def main() -> None:
    build_figure()
    build_report()
    print(f"Figure path: {FIGURE}")
    print(f"Report path: {REPORT}")
    print("TASK 4 DONE")


if __name__ == "__main__":
    main()
