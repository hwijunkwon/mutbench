# Audit v2 Job 11 -- ch5:1-150

Scope: `paper/dissertation/chapters_en/ch5_discussion.tex` lines 1--150. CSVs checked under `results/mutbench/`.

## Per-Paragraph Table

| Unit | Lines | Numeric claims | Citations | Refs | Consistency / recent-fix check | Severity |
|---|---:|---|---|---|---|---|
| P1 | 5 | 4-feature, 10-feature, Delta +0.011, p=0.61, n=11: VERIFIED against `results/mutbench/feature_analysis/feature_ablation_nested_lopo_summary.csv` for delta; p appears in manuscript/table, not CSV. | none | `ch:results`, `sec:information_analysis` resolve to ch4. | Consistent with ch4 nested-LOPO framing; no regressions. | Verified |
| P2 | 10 | n=7, CI [0.323,0.635], p<0.001, HS 0.778/0.383, 6.9--8.0x: VERIFIED as ch4 Stage 1 values; primary CSV not obvious in current bundle. | none | local labels OK. | No recent-fix issue. | Minor |
| P3 | 16--19 | mean \|rho\|=0.12, range -0.06..+0.33, per-pathogen values, D614G homoplasy=2, position 476 homoplasy=53, 3-lineage discriminator, 6/11, HIV-1 82%, H3N2 69%: mostly VERIFIED via ch4 text, `results/mutbench/feature_analysis/feature_correlation_mean.csv`, `results/mutbench/vaccine_escape_stage3.csv`; point-biserial audit source CSV not found. | none | `sec:information_analysis`, `subsec:feature_correlation`, `tab:stage2_best`, `sec:gt_heterogeneity`, `sec:vaccine_escape`, `tab:vaccine_escape_stage3` resolve correctly. | D614G retained as functional/founder-discounted, not excluded: OK. | Minor |
| T1 | 21--46 | Layer A table counts: per-pathogen counts VERIFIED in `results/mutbench/layer_a_tags.csv`; HIV-1 26 tags / 23 mapped to gp120 VERIFIED against `layer_a_tags.csv` and `combined_10scoring_results.csv`. Total row 308 VERIFIED. "11 dominant sources" is qualitative but odd for 12 pathogen rows. | none | `tab:layer_a_provenance` local label OK. | HIV-1 26/23 recent fix OK. | Verified |
| P4 | 48--52 | `layer_a_tags.csv` "309 positions across 12 pathogens": DISCREPANCY, found 308 data rows (`wc -l`=309 incl. header; group sum=308). 1--3 anchor pubs, HCV 54, H3N2 25, HIV-1 26, HIV-1 82%, 3D 5.92-fold: HCV/H3/HIV and 82% VERIFIED; 5.92 supported by ch4 text/source directory but not a CSV row found. | none | `ch:results`, `tab:vaccine_escape_stage3`, `sec:structure_analysis`, `sec:external_comparison`, `subsubsec:equalweight_variants` resolve. | No recent-fix regression. | Minor |
| P5 | 58 | 2024--2025, 1,259 positions, sigma=0.098, 3.43x, Jaccard=0.006: VERIFIED against ch4 Stage 1 table/text; source CSV not obvious. | none | `sec:multi_gt` resolves. | No regression. | Minor |
| P6 | 60 | rho=-0.876, D614G=2 vs position 476=53, HIV-1 AUC=0.706 p=0.0002, H3N2 0.561 p=0.147, HCV 0.390, omega2=0.296: rho/D614G/476 supported by ch4; AUC values match `results/mutbench/extended_scoring_comparison.csv` for HIV-1 0.706; p-values need provenance; omega2 VERIFIED in `cluster_bootstrap_omega_summary.csv`. | none | `subsec:phylo_correction_poc` resolves. | D614G wording is retained/functional, not excluded. | Minor |
| P7 | 69--70 | No quantitative claim except "no universally best": supported by `stage3_full_results.csv` heterogeneity and ch4. | `nextstrain2018hadfield` OK for surveillance system. | `ch:results` resolves. | Consistent. | Verified |
| P8 | 72 | omega2 family=0.013 and scoring x pathogen=0.296, "23 times": VERIFIED by ch4 table and `cluster_bootstrap_omega_summary.csv`; 0.013 is ch4 table, not the older `threeway_anova_omega.csv` file. | none | none | Consistent with ch4. | Verified |
| P9 | 74 | n=11, LOPO 0/11, Friedman p=0.990, gap=0.265, AUC 0.763 vs 0.944: VERIFIED in ch4 text; `nemenyi_provenance.json` gives Friedman p=0.9895; AUC source likely feature AUC table, CSV path not found in root bundle. | `rice1976algorithm`, `wolpert1997nfl` OK. | `sec:future_work`, `subsec:esm_validation` resolve. | LOPO is correctly tempered as null-consistent. | Minor |
| P10 | 76 | omega2 0.296 VERIFIED; 0.103 at 6-category granularity UNVERIFIED in CSV bundle; HIV-1 7.19x and 82% VERIFIED in `vaccine_escape_stage3.csv`. | `gurev2025everest`, `notin2023proteingym` plausibly support per-variant framing. | local label OK. | Consistent, but 0.103 needs provenance. | Minor |
| P11 | 82 | Mean oracle MCC 0.341, range 0.196--0.660, positive rates 0.7--15.9%, random baseline 0.001, F1 0.3--0.5, window mean 0.472, Influenza B 0.894: mostly VERIFIED from ch4 Table `tab:precision_at_k` and ch5 table; underlying `region_overlap_mcc.csv` conflicts with table values below. | `weirauch2013evaluation` OK for TFBS comparison. | `tab:stage2_best`, `tab:region_overlap_mcc` resolve. | Depends on discrepant T2. | Major |
| T2 | 84--113 | DISCREPANCY: caption says upper block reproduces `results/mutbench/region_overlap_mcc.csv`, but values differ. Examples: SARS exact expected 0.211, found 0.2271; H3N2 exact expected 0.534, found 0.5209; Influenza B +/-5 expected 0.894, found 0.5581; MERS exact expected 0.196, found 0.0708. EV-A71/Rabies rows cite archived `stage3_full_results.csv`, but not directly audited here. | none | table label OK. | This is the main numeric table failure in scope. | Major |
| P12 | 115 | No numerical/citation/ref claims. | none | none | OK. | Verified |
| P13 | 120 | Mean recall 0.552, 8/25 SARS-CoV-2, positions 160/186, +/-10 mean 0.341->0.454, Influenza B 0.924, 1--2 residues, EV-A71 recall 0.185, Rabies 0.308, lengths 261/491 AA: precision/recall/lengths VERIFIED in ch4 `tab:precision_at_k`; window claims inherit T2 discrepancy/unverified EV/Rabies derivation. | none | `tab:precision_at_k`, `subsec:search_space_reduction` resolve. | No Stage 1 439/417 wording in scope. | Major |
| P14 | 125 | Contribution 1/2/3, omega2 0.296/0.234, LOPO 0/11, HIV-1 82%: VERIFIED by `cluster_bootstrap_omega_summary.csv`, `ancova_omega_summary.csv` for 0.234 baseline, ch4 LOPO/table, `vaccine_escape_stage3.csv`. | none | `ch:introduction`, `sec:hscore_saturation` resolve. | LOPO caveat wording is current. | Verified |
| P15 | 131--132 | H3N2 9.36x, HIV-1 7.19x, SARS-CoV-2 7.63x, 780, p_adj HIV-1 2.5e-16, H3N2 2.6e-5, H3N2 EqualWeight 4.012x p=0.0023: VERIFIED in `vaccine_escape_stage3.csv` and `escape_validation_adapt.csv`. | none | `tab:vaccine_escape_stage3`, `ch:results`, `subsec:search_space_reduction` resolve. | Multiple-comparison and circularity wording consistent. | Verified |
| P16 | 134--135 | LOPO 0/11 VERIFIED; 10-feature/4-feature/97.6% retention DISCREPANCY: current `feature_analysis/feature_ablation_nested_lopo_summary.csv` has fixed4/full10 retention ratio 1.1595 (115.95%), not 97.6%. 13/210 and 6.2%-tile VERIFIED in `feature_analysis/subset_selection_robustness_210combos.csv`; 20x39 and 25s runtime supported by ch3/ch4 text, not CSV. | none | `tab:scoring_recommendation`, `tab:subset_selection_top10`, `tab:vaccine_escape_stage3` resolve. | Not a listed post-v214 regression, but stale numeric wording remains. | Major |
| P17 | 141--149 | 3 pathogens, 2,340 evaluations, HIV-1 18% overlap, p_adj=2.5e-16, 37 novel positions, 7.16--8.24x, 780-fold, H3N2 69%, p=0.132: VERIFIED in ch4 Table `tab:vaccine_escape_stage3` footnote/text and `vaccine_escape_stage3.csv` for total rows. | none | none | Practical-value claim properly narrowed to HIV-1. | Verified |

## Per-Section Severity Counts

| Section | Critical | Major | Minor | Verified |
|---|---:|---:|---:|---:|
| Chapter intro / methodological validity (1--52) | 0 | 0 | 5 | 2 |
| H-score limitations (55--60) | 0 | 0 | 2 | 0 |
| Cross-pathogen generalization (63--76) | 0 | 0 | 2 | 2 |
| Oracle ceiling / recall (79--120) | 0 | 3 | 0 | 1 |
| Practical implications / vaccine escape (123--150) | 0 | 1 | 0 | 3 |

## Overall Tally

Critical: 0. Major: 4. Minor: 9. Verified: 8. Regression: 0.

Recent-fix verification: D614G retained/not excluded OK; omega CI old wording absent in scope; HIV-1 Layer A 26 tags / 23 mapped OK; no Stage 1 439 AA wording in scope; no "point substitutions only" wording in scope.

RESULT_AUDIT_V2_J11: critical=0 major=4 minor=9 regression=0
