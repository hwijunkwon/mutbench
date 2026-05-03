# Audit v3 ch4d: lines 371-494

## 1. Per-paragraph audit table

| Lines | Claims | Source check | Citations | Cross-refs | Severity |
|---|---|---|---|---|---|
| 371-383 | ANOVA table: 20 scoring, 14 families, 11 pathogens; omega2 rows 0.296/0.117/0.082/0.063/0.039/0.013; Cohen tiers. | `stage3_full_results.csv` has 8,580 rows = 20 x 39 x 11 and 14 families. Recomputed Type-II no-threeway omega2 gives approx scoring x pathogen 0.290, pathogen 0.117, family x pathogen 0.077, scoring 0.062, scoring x family 0.031, family 0.012. `cluster_bootstrap_omega_summary.csv` supports headline 0.296252, but no scoped CSV found that exactly supports all table rows, especially 0.039. | `cohen1988statistical` present. | Table label `tab:stage2_anova` defined at line 365. | Minor |
| 386-390 | Figure caption repeats omega2=0.296 and residual approx 0.39. | Headline 0.296 supported by summary; residual from recompute is 1 - modeled omega sum approx 0.411, not approx 0.39 unless using the dissertation's alternate partition. No figure data CSV checked. | None. | `fig:variance_decomposition` defined. | Minor |
| 393 | Key finding: N=8,580; cluster CI [0.201,0.346]; cell-level 3,080, omega2=0.234; ANCOVA 0.264; Bayesian 0.252-0.319 HDI [0.188,0.396]. | N and 20x14x11 cells verified. `cluster_bootstrap_omega_summary.csv` gives [0.200836,0.345502]. `ancova_omega_summary.csv` gives baseline 0.2325 and ANCOVA 0.2741, not 0.234/0.264. `bayesian_omega_summary.csv` supports 0.3185 HDI [0.2457,0.3964] and body target 0.252 [0.188,0.314], not combined HDI [0.188,0.396]. | `cohen1988statistical` present. | `tab:stage2_anova`, `sec:scoring_input_heterogeneity`, `ch:discussion` defined. | Major |
| 395 | Top three components total about 50%. | Stated values sum 0.495. Recomputed current CSV comparable sum 0.484. | None. | None. | Verified |
| 397 | Same 8,580 dataset; ANOVA/Friedman/LOPO; counterfactual nulls. | Counterfactual null fully matches `cycle4_counterfactual_null.csv` after rounding: observed 0.289218; pathogen median 0.000178, CI [-0.004023,0.004971]; scoring median -0.000101; family median 0.282681, CI [0.279487,0.285536]. But Friedman chi2=7.69 p=.990 and LOPO 0/11 gap=.265 are not supported by available Friedman/LOPO CSVs (see below). | None. | None. | Major |
| 399 | 20-type omega2=.296, 6-category=.103, preliminary 9-score family x pathogen=.285, full 20-score scoring x pathogen=.296. | 20-type supported by summary. `threeway_anova_omega.csv` is a 9-score/9-pathogen file and gives family x pathogen omega2=.289637, scoring x pathogen=.084685; close to preliminary claim but not exact .285. No source found for 6-category .103 in scoped files. | None. | `ch:introduction` defined. | Minor |
| 401-430 | LOPO: 11 pathogens, 280 combinations, 0/11 match, generalized .032, oracle .297, gap .265, P0 approx .96, 780-grid footnote. | `lopo_9pathogen_cv.csv` has 9 rows, not 11. It gives generalized mean .0214, oracle .2982, gap .2769, 0/9 matches. The text also cites "training on remaining 10 pathogens" but archived file is 9-pathogen. Null P0 for 280 and 11 is mathematically about .961, but not archived in named CSV. | None. | `fig:lopo_crossval`, `tab:lopo_summary`, `subsec:precision_at_k`, `tab:precision_at_k` labels defined. | Major |
| 432-443 | Friedman top-20 across 11 blocks: chi2=7.69, p=.990, W=.037; power approx .15; LOPO range .196-.660. | Contradicted by available CSVs: `friedman_top20_multilayer.csv` gives chi2=42.4407, p=.001545, n_pathogens=9, k=20; `friedman_9pathogen.csv` gives chi2=603.81, p=3.56e-125, n=9, k=369. W arithmetic for claimed 7.69/(11x19)=.0368 is internally correct. Oracle range .196-.660 matches Table line 269/278 and `stage3_full_results.csv` per-pathogen maxima. | None. | `subsec:9pathogen_friedman` defined. | Critical |
| 445 | Nemenyi: 190 pairs, 0 significant, p range [.989,1.000], median 1.000; named rank gaps/order. | `nemenyi_summary.csv` has 190 rows, 0 raw/Bonferroni significant, p min .989201, median ~1.000. Most differentiated pair and high-rank cluster match. "Most similar" in file is actually `dnds_proxy+Wavelet` vs `freq+Wavelet`, rank gap 0.0; the named gap .18 pair is not the minimum. Omnibus p=.990 premise unsupported. | None. | Files named exist. | Minor |
| 447-451 | LOPO permutation null: 10,000 resamples; random combo mean .017, SDs .034/.027, observed .032, p .25-.28; interpretation tempered. | No `lopo` permutation CSV with these values found under requested results. `lopo_9pathogen_cv.csv` observed mean is .0214, not .032. | None. | None. | Major |
| 453 | Auxiliary quantities: `lopo_9pathogen_cv.csv`, `stage3_full_results.csv`, `cluster_bootstrap_omega_loo.csv`; HCV-excluded .246; immune-only n/omega values. | File existence verified. `cluster_bootstrap_omega_loo.csv` HCV-excluded row is .25341; `cluster_bootstrap_omega_summary.csv` has body target .246 and HCV-excluded cell .2214. Immune-only body targets .199/.187/.137 present in summary, but exact statement mixes observed/body target values. | None. | `tab:omega_loo_pathogen_sensitivity`, `subsec:anova_diagnostics`, `ch:discussion`, `sec:gt_heterogeneity` defined. | Minor |
| 455-467 | BCa best single combo P*E+Wavelet t=1.5; mean .124 CI [.047,.202]; Norovirus example; 36% of oracle .341; random mean .001 SD .003, 41 SD. | CI appears only in dissertation text, not in requested CSVs. The named best combo is not reproducible from `stage3_full_results.csv` alone without a BCa source file. The Norovirus example matches old 9-pathogen LOPO context ("remaining 8"), conflicting with 11-pathogen wording. Random baseline panel-mean draws are explicitly "reserved for release", so not auditable from requested CSVs. | None. | `subsec:9pathogen_bootstrap` defined. | Major |
| 469-473 | Subsampling fractions 25/50/75/100%; mean MCC stable 0.054-.058; variation within +/- .002. | `subsampling_robustness.csv` fraction means: .05763, .05509, .05426, .05576. Range .054-.058 and max deviation from 100% .00150 verified. | None. | `subsec:9pathogen_subsampling` defined. | Verified |
| 476-483 | Supplementary/ESM: ESM-2 650M; masked marginal; RSV best .196; SARS-CoV-2 top-3; poor Norovirus/HIV-1; correlations Norovirus +.63, HIV-1 -.35. | `esm_comparison_summary.csv` and `stage3_full_results.csv` verify RSV esm best .1963 and SARS-CoV-2 tied near third/top group (.1675). Norovirus/HIV-1 ESM ranks 10/10 in ESM summary and are poor. `esm_correlation_analysis.csv` verifies Norovirus max rho .6326 and HIV-1 E*rare rho -.3477 (p values rounded as stated). Model/cropping details not in CSV; `lin2023esm2` present. | `lin2023esm2` present. | `subsec:esm_validation` defined. | Verified |
| 485-490 | ANOVA diagnostics: Shapiro W=.974 p<1e-29; Levene all factors; skew .14, kurtosis 2.83; effective cells 3,080; 5-way robustness intervals. | Robustness intervals verified in `omega_robustness_5way.csv` after rounding: cluster [0.201,0.346], wild [0.201,0.303], phylo [0.202,0.346], mixed .3398, Bayesian [0.242,0.388], naive [0.260,0.321] stated in text but not in this table. Shapiro/Levene/skew/kurtosis source not found in requested CSVs. | None. | `tab:omega_robustness_5way` defined immediately after scope; label exists. | Minor |
| 494 | Table caption says five frames lower bound above .14. | Matches `omega_robustness_5way.csv` except mixed row has no percentile CI; caption handles this. | None. | Label at line 495 exists. | Verified |

## 2. Per-section severity counts

| Section | Critical | Major | Minor | Verified |
|---|---:|---:|---:|---:|
| ANOVA variance decomposition, 371-399 | 0 | 2 | 3 | 1 |
| LOPO/Friedman/Nemenyi/permutation, 401-453 | 1 | 3 | 2 | 0 |
| BCa/subsampling/ESM/diagnostics, 455-494 | 0 | 1 | 1 | 3 |

## 3. Recent-fix verification

| Anchor | Status | Check |
|---|---|---|
| omega2 CIs [0.201,0.346], phylo [0.202,0.346], wild [0.201,0.303] | PRESENT | Lines 393/490 and `omega_robustness_5way.csv` match after rounding. |
| HIV-1 Layer A n=23 mapped gp120; n=26 tags | PRESENT | `feature_matrix_HIV-1.csv` layer_a sum=23; `layer_a_tags.csv` HIV-1 rows=26; line 430 footnote/cross-chapter text preserve distinction. |
| D614G retained per Korber 2020 | PRESENT | Outside scope but present in ch4 line 219; `korber2020tracking` bib entry exists. |
| Stage 1 functional regions 417 AA, not 439 | NOT PRESENT | Not in lines 371-494; no regression observed in scope. |
| Single-position scoring gap-aware, not point substitutions only | NOT PRESENT | Not in scoped lines; no contradictory "point substitutions only" found in scope. |
| P1 null at-or-below mean 6/12 iid/circular, 4/12 block, 7/12 local burden | PRESENT | Outside scope but present in ch4 line 841. |
| Decision curve budget 50 random baseline 41 TPs | PRESENT | Outside scope but present in ch4 line 837 and requested CSV exists. |

## 4. Compression candidates

| Lines | Candidate reduction |
|---|---|
| 393 | Split or compress by moving cell-level/ANCOVA/Bayesian details to Table note; likely saves >80 words without losing the key finding. |
| 397 | Counterfactual-null paragraph can be tabled as observed/null median/CI rows; saves >60 words. |
| 430 | Footnote can be shortened to "280 family-level vs 780 variant-level; not directly comparable"; saves >70 words. |
| 445 | Nemenyi paragraph can drop cluster-order examples or move them to supplement; saves >100 words. |
| 467 | Random-baseline footnote can be replaced by one sentence once source CSV exists; saves >80 words. |
| 490 | Robustness intervals are repeated in following table; prose can cite table only; saves >45 words. |

## 5. Overall tally

Critical=1, Major=6, Minor=6, Verified=5. Recent-fix regressions=0.

RESULT_AUDIT_V3_ch4d: critical=1 major=6 minor=6 regression=0
