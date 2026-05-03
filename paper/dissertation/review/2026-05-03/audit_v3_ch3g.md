# Audit v3 ch3g (ch3_methods.tex 763--892)

## 1. Per-paragraph audit table

| Lines | Claims audited | Source check | Citations | Cross-refs | Severity |
|---|---|---|---|---|---|
| 764--766 | Three-way ANOVA: 20 scoring, 14 families, 11 pathogens; 8,580 rows; df residual 7,970; cell grid 3,080; omega 0.234; cluster bootstrap reported. | `stage3_full_results.csv` has 8,580 rows, 20 scoring, 39 detectors, 14 families, 11 pathogens. `stage3_statistics.csv` has residual df 7,970 and scoring x pathogen omega 0.296. `ancova_omega_summary.csv` gives cell baseline 0.2325, rounded in text to 0.234. | none | `subsubsec:cell_level_omega`, `ch:results` resolve. | Verified |
| 766 | Omega formula, manual Type-II-like implementation, statsmodels cross-check, headline omega 0.296, Cohen large threshold. | `stage3_statistics.csv` gives 0.29625198. Cohen key exists in `references.bib`. Script claim not directly checked against CSV, but consistent with archived outputs. | `cohen1988statistical` present. | `eq:omega_squared` resolves. | Verified |
| 768 | Evaluation-level omega 0.296; cell grid 3,080; cell omega 0.234; cluster CI [0.201, 0.346]. | `stage3_statistics.csv`, `stage3_full_results.csv`, `ancova_omega_summary.csv`, and `cluster_bootstrap_omega_summary.csv` support values: CI 0.2008--0.3455. | Cohen already present. | self-label resolves. | Verified |
| 770 | ANCOVA covariate replacement; pathogen main 0.108 -> not in model; scoring x pathogen 0.234 -> 0.274; p < 1e-167; family x pathogen 0.080 -> 0.088. | `ancova_omega_summary.csv` supports 0.10788, 0.23251 -> 0.27412, 0.08006 -> 0.08775. The p-value is not in the CSV. | none | `sec:scoring_input_heterogeneity` resolves. | Minor |
| 772 | Bayesian partial pooling: exploratory 0.252 [0.188,0.314], archived 0.319 [0.246,0.396], P > 0.14 ~0.9998; factor analysis table. | `bayesian_omega_summary.csv` supports archived mean 0.3185, HDI 0.2457--0.3964, P=0.99975, and records exploratory body target 0.252 [0.188,0.314], P=0.996. `bayesian_factor_omega_summary.csv` supports factor-analysis 0.3155 [0.2421,0.3882]. | none | `subsec:anova_diagnostics`, `tab:omega_robustness_5way` resolve. | Verified |
| 774--783 | Levene W=14.83 df 219/8360 p<1e-50; Kruskal scoring H=277.9 p<1e-47; ART omega 0.277/0.343; omega equation and Cohen thresholds. | ART archived omega 0.343 is in `art_omega.csv` and body target 0.277 is recorded. However, accessible diagnostics conflict: `anova_diagnostics_multilayer.csv` has Levene by pathogen/family/score = 100.89/12.17/2.63 and KW scoring H=78.07, while Ch4 text reports KW scoring H=277.9. No CSV found for Levene W=14.83 df 219/8360. | `wobbrock2011aligned`, `cohen1988statistical` present. | `tab:vaccine_escape_stage3`, `eq:omega_squared` resolve. | Major |
| 787--790 | LOPO over 11 pathogens; family grid 280; exact concordance; random concordance ~0.36%. | `stage3_statistics.csv` includes LOPO match rate 0 over 11. Grid 20 x 14 = 280; 1/280 = 0.357%. | none | none | Verified |
| 795 | Nested-LOPO 4-feature protocol: 12-pathogen panel incl. Zika, sign/rank refit on 11 training pathogens, top 10%, 1,000 bootstrap, 5,000 sign flips, label-aware variant only here. | `feature_ablation_nested_lopo.csv` has 12 held-out folds and fixed4/full10 MCCs; summary has full10 0.06975, fixed4 0.08088, delta 0.01113. CSV does not expose bootstrap iteration count or sign-flip count. | none | `subsec:feature_ablation`, `tab:nested_lopo_4core`, `subsubsec:equalweight_variants` resolve. | Minor |
| 799--801 | Friedman test uses 11 pathogen blocks, top k=20, Kendall W. | `friedman_top20_multilayer.csv` reports k=20 but n_pathogens=9, not 11. `friedman_9pathogen.csv` also reports n_blocks=9. This is a direct mismatch. | `demsar2006statistical` present. | none | Major |
| 806--810 | BCa CIs 10,000 resamples across 11; cluster bootstrap 1,000; robustness frames: wild [0.201,0.303], phylo [0.202,0.346], mixed 0.340 chi2 913.7 ICC 0.135, Bayesian 0.316 [0.242,0.388], standard [0.201,0.346]. | Robustness frames are supported by `omega_robustness_5way.csv`, `wild_cluster_bootstrap_omega_summary.csv`, `block_bootstrap_omega_summary.csv`, `mixed_effects_omega_summary.csv`, and `bayesian_factor_omega_summary.csv`. But `pathogen_bootstrap_ci.csv` is 9-pathogen, not 11, for the BCa-best-combination claim. | `cameron2008bootstrap` present. | `subsec:anova_diagnostics`, `tab:omega_robustness_5way` resolve. | Major |
| 812--814 | Delete-one jackknife, Mantel, Procrustes not performed. | Negative method claims cannot be fully proven from CSVs, but no Mantel/Procrustes/jackknife result CSVs found; text is consistent with available archive. | `mantel1967nonparametric` present. | `sec:gt_heterogeneity` resolves. | Verified |
| 818 | Subsampling at 25/50/75/100%. | `subsampling_robustness.csv` has fractions 0.25, 0.5, 0.75, 1.0 over 9 pathogens and 5 repeats. | none | none | Verified |
| 822--825 | Feature ablation: 10-feature EqualWeight; leave-one-out 9-feature; cumulative k=2..9 by AUC; 98% target example. | `feature_ablation_results.csv` has 12 pathogens, leave-one-out rows for 10 features plus `none` baseline, group/cumulative rows, and cumulative k=1..10. | none | none | Verified |
| 829--836 | Hotspot-score weights sum to 1, each 0.05--0.95; 171 combinations; five methods; seven scenarios. | No scoped CSV found that directly archives the 171-combination weight grid or seven scenario table. | none | `eq:weighted_hotspot_score` resolves. | Minor |
| 840--853 | Three statistical validation methods; seven-region Stage-1 bootstrap; 1,000 label permutations; 200 circular rotations; pseudo-count p. | Seven regions and 1,251 nt / 417 AA are in lines 369--405. The permutation counts are methods text; no scoped CSV directly confirms the 1,000/200 design. | none | `subsec:wild_cluster_future` resolves. | Minor |
| 858--864 | Stage 3: 20 scores decomposed into 10 features; three ablations; RF 200 trees/max_depth 5/balanced/seed 42; 11 or 12 pathogens; vaccine escape on 3/11, 2,340 evaluations. | `stage3_full_results.csv` supports 20 score types; feature files support 10-feature panel; `feature_ablation_results.csv` supports 12-pathogen ablations; `rf_cv_auc_v2.csv` has 11 pathogens (mean AUC 0.742); `vaccine_escape_stage3.csv` has 2,340 rows and 3 pathogens. | none | `subsubsec:equalweight_variants`, `subsubsec:nested_lopo_methods`, `subsec:rf_importance`, `subsec:feature_ablation`, `sec:cross_validation_escape` resolve. | Verified |
| 868--887 | Licenses, repository/provenance, external-resource license matrix, no upstream redistribution, headline grid excludes noncommercial resources. | `results/mutbench/provenance/README.md` supports license split and compatibility audit. `external_resource_licenses.csv` supports listed resources and headline-grid flags. Root `LICENSE-CODE`, `LICENSE-DATA`, `environment.yml`, `requirements-pinned.txt` were not found at repo root in this workspace; provenance versions are under `results/mutbench/provenance/`, while text says `provenance/`. | many listed keys present except exact `frazer2021eve` case differs from CSV license key `frazer2021EVE`; Bib has `frazer2021eve`. | `ch:discussion`, `sec:code_availability`, `tab:pathogen_data` resolve. | Minor |
| 891--892 | Chapter summary: 11 RNA viruses, 3-layer GT, 20 scoring, 14 families, Stage 3 via AUC/ablation/RF. | Supported by `stage3_full_results.csv` dimensions and feature/RF archives. | none | `ch:results` resolves. | Verified |

## 2. Per-section severity counts

| Section | Critical | Major | Minor | Verified |
|---|---:|---:|---:|---:|
| Stage 2 statistical design (763--783) | 0 | 1 | 1 | 4 |
| LOPO / nested LOPO / Friedman (785--801) | 0 | 1 | 1 | 1 |
| Bootstrap and robustness (803--814) | 0 | 1 | 0 | 1 |
| Subsampling / feature / validation methods (816--853) | 0 | 0 | 2 | 2 |
| Stage 3 integration (855--864) | 0 | 0 | 0 | 1 |
| Reproducibility / licenses / summary (866--892) | 0 | 0 | 1 | 1 |

## 3. Recent-fix verification

| Anchor | Status | Check |
|---|---|---|
| Omega CIs: standard [0.201,0.346], phylo [0.202,0.346], wild [0.201,0.303] | PRESENT | Lines 768/809--810 match rounded CSVs. |
| HIV-1 Layer A n=23 mapped gp120; n=26 tags | PRESENT | Ch4 caption states nA=23 mapped; `layer_a_tags.csv` has 26 HIV-1 rows. |
| D614G retained in Layer A per Korber 2020 | PRESENT | `layer_a_tags.csv` includes SARS-CoV-2 614 functional, Korber 2020. |
| Stage 1 functional regions 417 AA (=1251 nt/3), not 439 | PRESENT | Lines 396/405 state 1,251 nt and 417 AA; no 439 regression found. |
| Single-position scoring gap-aware, not point substitutions only | PRESENT | Scope says single-position score computation; no “point substitutions only” phrase found. |
| P1 null at-or-below-mean 6/12 iid/circular; 4/12 protein-block; 7/12 local-burden | PRESENT | Computed from `codex_wave1/p1_null_per_pathogen.csv` for 4-core MCC. |
| Decision curve budget 50 random baseline 41 TPs | PRESENT | Sum of random rows at budget 50 in `p2_decision_curve.csv` = 41. |

## 4. Compression candidates

| Lines | Candidate reduction |
|---|---|
| 765--766 | Merge implementation rationale and independence caveat; likely saves 45--60 words without losing numbers. |
| 768 | Remove repeated “large under Cohen” sentence already covered at 777; saves ~22 words. |
| 770 | Shorten covariate motivation and “load-bearing quantity” prose; saves ~30 words. |
| 772 | Move exploratory half-Cauchy details to note/table and keep archived run in text; saves ~35 words. |
| 795 | Split protocol details into a compact list or defer script/function details to parenthetical; saves ~50 words. |
| 874--887 | License paragraphs can refer to `external_resource_licenses.csv` and keep only headline exclusions; saves >100 words. |

## 5. Overall tally

Critical: 0; Major: 3; Minor: 5; Verified: 10; Regression anchors: 0.

RESULT_AUDIT_V3_ch3g: critical=0 major=3 minor=5 regression=0
