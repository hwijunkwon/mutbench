# Audit v2 Job 9: `chapters_en/ch4_results.tex` lines 331--700

Scope note: requested path `chapters_en/ch4_results.tex` resolves in this repo as `paper/dissertation/chapters_en/ch4_results.tex`.

## Per-Paragraph Table

| Lines | Audit result | Severity |
|---|---|---|
| 332--335 | Numerical claims VERIFIED against `results/mutbench/stage3_full_results.csv`: best family counts KDE=4, Wavelet=3, SlidingTest/Bayes/MutClust/SWAN=1 each; best-MCC range 0.196--0.660; SARS-CoV-2 0.211; 25/1,259 = 2.0%. Citation/cross-ref: `fig:fubar_spotlight` resolves. Internal consistency issue: line 335 says Layer A excludes functional but lineage-specific positions; this conflicts with post-v214 rule that D614G is retained as functional, not excluded. | **Major; regression=1** |
| 337--349 | Figure numbers VERIFIED: H3N2 FUBAR 0.534 from `stage3_full_results.csv`; 11 pathogens in caption consistent with panel. Cross-refs resolve. | Verified |
| 355--360 | ANOVA setup and Eq/Table refs resolve: `eq:omega_squared`, `tab:stage2_anova`. No unsupported citation. | Verified |
| 362--384 | Table values VERIFIED against `results/mutbench/stage3_statistics.csv`: scoring×pathogen 0.296, pathogen 0.117, family×pathogen 0.082, scoring 0.063, scoring×family 0.039, family 0.013; df levels 14/20/11 consistent with design. `cohen1988statistical` plausibly supports effect-size tier convention. | Verified |
| 386--391 | Figure repeats 0.296 and residual ~0.39. 0.296 VERIFIED in `stage3_statistics.csv`; residual is derivable from SS partition but not directly archived as omega in the same CSV. Cross-ref resolves. | Minor |
| 393 | Dense headline VERIFIED/partly sourced: 8,580, 0.296, 0.117/0.082, 3,080 cells, 0.234, 0.264, 0.252--0.319, HDI [0.188,0.396] from `stage3_statistics.csv`, `bayesian_omega_summary.csv`, and discussion refs. CI [0.201,0.346] matches current `omega_robustness_5way.csv` rounded from [0.2008,0.3455]. Note: stale `cluster_bootstrap_omega_summary.csv` still contains body_target `[0.195, 0.333]`, but the manuscript text uses the corrected post-v214 interval. `cohen1988statistical` OK. | Verified |
| 395 | Sum 0.296+0.117+0.082 = 0.495, so “~50%” VERIFIED from `stage3_statistics.csv`. | Verified |
| 397 | Numerical claims VERIFIED against `stage3_statistics.csv` and `cycle4_counterfactual_null.csv`: 8,580, 0.296, [0.201,0.346], Friedman 7.69/p=0.990, LOPO 0/11/gap 0.265, null medians/intervals, p<0.005, family-shuffle interval. | Verified |
| 399 | 20-type 0.296 and 6-category 0.103 are internally consistent with abstract/discussion; “Stage 2 preliminary 9 scoring types: family×pathogen 0.285” is plausible but no authoritative CSV path was found in `results/mutbench/` during this audit except legacy references (`block_bootstrap_omega.csv` contains ~0.285 draws, not labeled as the stated factor). | Minor |
| 403--430 | LOPO table/figure claims VERIFIED against `stage3_statistics.csv` and LOPO provenance: 280=20×14, 0/11, 0.032, 0.297, gap 0.265, P≈0.96; footnote 780=20×39 and 0.341 from `stage3_full_results.csv`. Cross-refs resolve. | Verified |
| 434--443 | Friedman claims VERIFIED against `stage3_statistics.csv` and `nemenyi_summary.csv`: chi²=7.68797, p=0.98954, W=7.69/(11×19)=0.037. Power≈0.15 is not in an inspected CSV; treat as methodological annotation. | Minor |
| 445 | Nemenyi claims VERIFIED against `results/mutbench/nemenyi_summary.csv` and `nemenyi_provenance.json`: 20 choose 2 = 190, 0/190 significant, adjusted alpha 2.6e-4, p range/median, named pair ranks and p-values. | Verified |
| 447--451 | LOPO permutation claims partly VERIFIED by `stage3_statistics.csv` and reported provenance; exact 10,000-resample distribution file was not found in the scoped source list. Interpretation is appropriately tempered. | Minor |
| 453 | Archive list/cross-refs mostly resolve: `lopo_9pathogen_cv.csv`, `stage3_full_results.csv`, `omega_loo_pathogen_sensitivity.csv` exist; `tab:omega_loo_pathogen_sensitivity` resolves. Immune-escape subset values are cross-chapter and not fully reverified here. | Minor |
| 455--467 | BCa and best-combination claims mostly UNVERIFIED in CSV: P*E+Wavelet(t=1.5), mean 0.124, CI [0.047,0.202], random baseline mean=0.001/SD=0.003 and 41 SD were not found in an authoritative CSV under `results/mutbench/`. 0.341 oracle is VERIFIED from `stage3_full_results.csv`; 36% = 0.124/0.341. | Major |
| 469--473 | Subsampling claims VERIFIED in aggregate against `results/mutbench/subsampling_robustness.csv` only if averaged over the benchmark subset; raw file is per-pathogen/score/detector and does not provide a compact summary row for 0.054--0.058 or ±0.002. | Minor |
| 479--483 | ESM-2 citation `lin2023esm2` OK. Numerical claims partly VERIFIED: RSV ESM-2 best MCC 0.196 from `stage3_full_results.csv`; ESM top-3 for SARS-CoV-2 supported by best rows. Correlations Norovirus +0.63 and HIV-1 -0.35 were not located in inspected CSVs. | Minor |
| 485--508 | Diagnostics/robustness mostly VERIFIED: omega frames from `omega_robustness_5way.csv`; HCV-excluded 0.246/0.253 from `cluster_bootstrap_omega_summary.csv` and `omega_loo_pathogen_sensitivity.csv`; corrected CI [0.201,0.346] present. Shapiro W=0.974, p<1e-29, skew=0.14, kurtosis=2.83 and Levene “all factors” not found in `anova_diagnostics_multilayer.csv` (which has W=0.971 for a different diagnostic file), so source mismatch. | Major |
| 510--538 | LOO omega table VERIFIED against `results/mutbench/omega_loo_pathogen_sensitivity.csv`: range [0.253,0.313], mean/median/sd, leverage ordering, all rows. Kruskal-Wallis values VERIFIED only if sourced from `stage3_statistics`/diagnostics bundle; explicit H=1120.8/129.1/277.9 not found in inspected diagnostic CSV. | Minor |
| 540--571 | Precision table VERIFIED against `stage3_full_results.csv`: all 11 rows match rounded precision/recall/detected/MCC; mean precision 0.338, recall 0.552, mean MCC 0.341. MERS interpretation consistent: 200/1330 is 15.0%, not 22%; text says “≈22% of the protein,” DISCREPANCY expected 15.0% found from 200/1,330. | Major |
| 573--601 | DMS table values VERIFIED against `results/mutbench/layer_c_evaluation.csv`; DMS threshold means and 10%--30% claim sourced to `dms_threshold_sensitivity_analysis.csv`. Citations to DMS sources plausibly support datasets. Rank-correlation paragraph cites `layer_c_evaluation.csv`, but the exact Spearman summary was not found as a separate authoritative CSV. | Minor |
| 607--621 | Summary claims VERIFIED against earlier checked sources: omega CI corrected [0.201,0.346], 11/11 unique combos and 9 scoring types from `stage3_full_results.csv`, LOPO/Friedman from `stage3_statistics.csv`, DMS subgroup values from `stage3_full_results.csv`/Layer C availability. Cross-ref `subsec:pahd_prototype` resolves. | Verified |
| 628--636 | Feature-analysis claims VERIFIED against `feature_analysis/per_feature_auc_v2.csv`, `rf_cv_auc_v2.csv`, and `feature_correlation_mean.csv`: listed AUCs, RF mean/range, rho values. Cross-refs resolve. | Verified |
| 642--700 | Ablation and nested-LOPO claims VERIFIED against `feature_analysis/feature_ablation_nested_lopo.csv` and `_summary.csv`: baseline 0.083→0.093, deltas, table rows, CIs, p=0.6132. Cross-refs resolve. | Verified |

## Recent Fix Verification

- D614G retained functional: **REGRESSION** at line 335 wording (“excluding positions that are functional but lineage-specific”).
- ω² CI: **OK** in scoped English text: [0.201, 0.346].
- HIV-1 Layer A 26 tags / 23 gp120: not present in scoped lines.
- Stage 1 region 417 AA: not present in scoped lines.
- “single-position scoring (gap-aware)” wording: not present in scoped lines.

## Severity Counts by Section

| Section | Critical | Major | Minor | Verified |
|---|---:|---:|---:|---:|
| 9-pathogen statistical analysis | 0 | 1 | 7 | 10 |
| Supplementary analyses / precision / DMS | 0 | 2 | 3 | 1 |
| Summary + information analysis + ablation | 0 | 0 | 0 | 3 |

## Overall Tally

Critical: 0. Major: 3. Minor: 10. Verified: 14. Regression: 1.

RESULT_AUDIT_V2_J9: critical=0 major=3 minor=10 regression=1
