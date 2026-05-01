# Wave 4 — Tier-2 Features-Only LOPO

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

The hscore overlap audit failed on all three audit pairs (`Dengue:dengue_e`, `HIV-1:hiv1_gp120`, `Norovirus:norovirus_vp1`), with 0/3 passing the predeclared harmonization threshold. Per the review, hscore was therefore excluded from expanded diagnostics and the analysis used the 2-core fallback `freq,entropy`.

Algorithm 1 sign fitting was preserved on labeled folds: for each held-out pathogen, signs were fit only from the other 11 labeled pathogens, then applied to the held-out fold. Expanded stability used 1,000 bootstrap sign fits with `random_seed=42`, resampling labeled pathogens with replacement; unlabeled targets were scored after sign fitting and were never sampled into the sign estimator.

## Inputs

Denominators: `n_unique_targets=28`, `n_labeled_eval=12`, `n_cross_pathogen_csv=19`, `n_overlap=3`, `n_unlabeled_expanded=16`. The three overlap cross-pathogen files were audit-only and excluded from unique-target counts.

## Top-Line Findings

| Finding | Result | Interpretation |
|---|---:|---|
| hscore harmonization audit | 0/3 PASS | 2-core fallback active |
| Labeled 12-fold 2-core LOPO | mean MCC 0.077; 8/12 positive | paired Wilcoxon vs 4-core p=0.368 |
| D1 callability recheck | 0/12 | Matches Wave 2 failure mode |
| Expanded 28-target stability | 1/28 pass; 16/16 unlabeled inside envelope | quorum_pass=False |
| Sign-fitting bootstrap | freq 81.6%; entropy 94.4% | Matches full-sample sign |

## Per-Pathogen Labeled MCC Table

| Pathogen | n | Layer A | 2-core MCC | 4-core MCC | Delta | P@20 | D1 |
|---|---:|---:|---:|---:|---:|---:|---:|
| SARS-CoV-2 | 1259 | 25 | 0.047 | 0.047 | 0.000 | 0.05 | fail |
| H3N2 | 543 | 25 | 0.101 | 0.072 | 0.029 | 0.15 | fail |
| Norovirus | 536 | 15 | 0.281 | 0.357 | -0.075 | 0.15 | fail |
| HIV-1 | 450 | 23 | 0.091 | -0.010 | 0.101 | 0.05 | fail |
| Dengue | 490 | 24 | 0.019 | 0.019 | 0.000 | 0.10 | fail |
| RSV | 550 | 20 | -0.065 | -0.065 | 0.000 | 0.00 | fail |
| Influenza_B | 560 | 17 | 0.184 | 0.219 | -0.035 | 0.20 | fail |
| MERS | 1330 | 9 | 0.003 | -0.028 | 0.031 | 0.00 | fail |
| HCV | 340 | 54 | 0.365 | 0.150 | 0.215 | 0.45 | fail |
| Zika | 452 | 27 | -0.023 | -0.023 | 0.000 | 0.05 | fail |
| Rabies | 491 | 39 | -0.049 | -0.049 | 0.000 | 0.05 | fail |
| EV-A71 | 261 | 27 | -0.033 | 0.050 | -0.083 | 0.05 | fail |

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

Wave 5 ordering remains pilot 3 Layer A curation for YFV/Lassa/WNV, per the Codex plan review Wave 5 ordering recommendation. The condition was that labeled 3-core/2-core performance not be clearly negative; the observed 2-core mean MCC was 0.077, with 8/12 positive folds, so the result is bounded positive. The pilot must still be interpreted as curation toward a future quorum test, not as validation from Wave 4.

## Cross-References

- Figure: `results/mutbench/codex_wave4/w4_summary_figure.png`
- Labeled folds: `results/mutbench/codex_wave4/w4_labeled_lopo_per_fold.csv`
- Expanded stability: `results/mutbench/codex_wave4/w4_expanded_stability_per_target.csv`
- Quorum diagnostic: `results/mutbench/codex_wave4/w4_expanded_quorum_reachability.csv`
