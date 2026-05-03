# Audit v3 ch4b: `chapters_en/ch4_results.tex` lines 124--247

## 1. Per-paragraph audit table

| Lines | Claims audited | Source check | Citations | Cross-refs | Severity |
|---|---|---|---|---|---|
| 124 | Permutation tests: 1,000 random + 200 circular, all `p < 0.005`, `z > 9.2`. | Claim appears in prose, but I did not find a matching permutation-summary CSV in the scoped archive by filename/content search. Needs explicit source pointer. | None needed. | No refs. | Minor |
| 126 | Region-level BCa CI `[0.323, 0.635]`; pairwise bootstrap `p < 0.001`; later combination-level CI `[0.047, 0.202]`; cluster CI `[0.201, 0.346]`. | Cluster CI matches `cluster_bootstrap_omega_summary.csv` (`0.2008, 0.3455`) and `omega_robustness_5way.csv`. Combination CI matches `pathogen_bootstrap_ci.csv` for `P*E + Wavelet(t=1.5)`. Region-level CI/pairwise p not found as a CSV in scope, but repeated consistently in Ch5. | `efron1987better` present in `references.bib`. | `subsec:9pathogen_bootstrap`, `subsec:anova_diagnostics` defined later. | Verified |
| 128--132 | Weight sensitivity `71.9%` of 171; convergence at ~1,000 sequences; `rho > 0.997`, SD `<0.015`; F1 most sensitive to gamma; MinPts minimal. | `sensitivity_results.csv` supports gamma-driven F1 variability. I did not find a visible weight-sensitivity or sample-size convergence CSV in `results/mutbench`; labels exist only as phantoms/figures. | None. | `fig:sample_size_convergence`, `fig:mutbench_sensitivity` defined in scope. | Minor |
| 137--145 | Figure captions repeat convergence and 64-grid sensitivity claims. | Sensitivity grid count: `sensitivity_results.csv` has 64 combinations. Convergence source not found. | None. | Figure labels defined. | Minor |
| 151--179 | H3N2 pilot: 9,000 sequences in 3 windows; `n=3,000` each; Layer A 25 sites; retrospective enrichment `2.7--3.4x`; prospective overlaps `0/20,0/30,0/50`; `1/50` in 2021--2025; table values. | Table values exactly match `feature_analysis/h3n2_temporal_pilot.csv`: overlaps/ref sizes/enrichments/Fisher p all verified. CSV does not expose the 9,000/3,000 sampling claim, but it is consistent with the table design. | Text says Koel 2013 without `\cite`; `koel2013substitutions` exists in bib. | `tab:h3n2_temporal_pilot`, `subsec:feature_ablation` defined. | Verified |
| 184 | Sliding-window method: 11 pathogens, train/test thresholds, freq+entropy z-ensemble, emergence definition. | Consistent with `feature_analysis/sliding_window_prospective_backtest_summary.csv` and full backtest CSV naming; thresholds not independently visible in summary header. | None. | `subsec:h3n2_temporal_pilot` defined. | Verified |
| 186--193 | 73 windows, 219 top-k evaluations; EV-A71/Rabies/Influenza B AUROC/MCC/enrichment; grand means; slopes; retrospective MCC headline. | `sliding_window_prospective_backtest_summary.csv`: windows sum 73, evaluations 219. Unweighted pathogen means match reported grand mean MCC `-0.006`, AUROC `0.539`, enrichment `1.57x`; window-weighted means would be MCC `-0.001`, AUROC `0.555`, enrichment `2.66x`, so "grand mean" should specify unweighted by pathogen. EV-A71/Rabies/Influenza B and slope range verified. `region_overlap_mcc.csv` all-11 mean exact `0.341`, window-10 `0.454` verified. | None. | Figure label defined; `tab:region_overlap_mcc` in Ch5; `sec:prospective_validation_gap` in Ch5. | Minor |
| 197 | 4-feature extension: coverage `0.83`; AUROCs `0.555/0.543/0.549/0.561`; Wilcoxon p/deltas; EV-A71, Rabies, HCV examples. | AUROCs and deltas/p-values match window-weighted calculations and `sliding_window_prospective_c2_vs_d2_paired.csv`. Caveat: prose switches from unweighted "grand mean" in line 186 to window-weighted AUROC here without saying so. HCV AUROC collapse `0.31 -> 0.09` and EV-A71/Rabies values verified in `sliding_window_prospective_backtest_4feature_summary.csv`. Mean coverage `0.83` not found in CSV except likely coverage diagnostics. | None. | Paragraph label defined. | Minor |
| 200--206 | Section labels and transition to H3N2/structure/phylo. | No numerical claim beyond section scope. | None. | All labels defined; refs to `sec:9pathogen_results` defined in scope. | Verified |
| 208--215 | H3N2 HA: 1,967 sequences, 5 antigenic sites, Fixed HS `0.661` vs Hybrid `0.577`, all 543 positions nonzero H-score, enrichment `0.87--2.36x`; figure top-5 scoring types and Stage 2 refs. | H3N2 543 length appears in multiple CSVs. The exact 1,967 sequence count and HS/enrichment range were not found in current CSVs; older Stage 2 files show H3N2 `n_unique=2562`, not 1,967. Requires archived Stage 1 H3N2 source pointer or correction. | `wiley1981structural`, `wilson1990structural` present. | `fig:cross_pathogen_comparison`, `tab:stage2_best`, `subsec:9pathogen_statistical`, `subsec:9pathogen_lopo` defined. | Major |
| 217 | 3D structural analysis: PDB 6VSB, `5.92x` within-8-A contact enrichment, 1,000 random subsets, `z=13.34`; source in `structural_features/`. | `structural_features/` contains SASA/pLDDT CSVs and PDBs but no CSV with 5.92, 8A contact enrichment, random subsets, or z=13.34. Not auditable from declared CSV sources. | None. | No refs. | Major |
| 219 | Coalescent simulation: 100 reps, `N=500`, H-score ranks founder above convergent `100%`; Fitch rho/p; TreeTime/Fitch AUC 1.000 vs H-score 0.000; D614G retained in Layer A via Korber 2020. | Method setup appears in Ch3. `phylo_sensitivity_results.csv`/comparison supports homoplasy advantage but not all simulation summary fields. D614G verified: `layer_a_tags.csv` has SARS-CoV-2 position 614 functional with Korber 2020; feature matrix marks position 614 `layer_a=1`. | `sagulenko2018treetime`, `korber2020tracking` present. | All labels defined; `para:full_lattice_shapley` defined later. | Verified |
| 229--247 | Stage 2 scale: 20 scoring types, 14 families, 39 variants, 11 pathogens, 8,580 evaluations; 10 biological features; categories; MCC rationale with lengths 261--1,330 and MSA sizes 530--5,019. | `stage3_full_results.csv`: 8,580 rows, 20 scoring values, 39 detectors, 14 families, 11 pathogens verified. Scoring list matches CSV names modulo prose display names. Length range 261--1,330 matches feature matrices/stage files. MSA-size range not directly checked in this line-level pass. | None. | `subsec:variants`, `tab:scoring_types`, `ch:mutbench`, `sec:information_analysis` defined. | Verified |

## 2. Per-section severity counts

| Section | Critical | Major | Minor | Verified |
|---|---:|---:|---:|---:|
| Stage 1 robustness tail, lines 124--145 | 0 | 0 | 3 | 1 |
| H3N2 temporal pilot, lines 148--179 | 0 | 0 | 0 | 1 |
| Sliding-window backtest, lines 181--197 | 0 | 0 | 2 | 1 |
| Cross-pathogen/structural validation, lines 200--219 | 0 | 2 | 0 | 2 |
| Stage 2 scale intro, lines 222--247 | 0 | 0 | 0 | 1 |

## 3. Recent-fix verification

| Anchor | Status | Check |
|---|---|---|
| omega2 CIs `[0.201,0.346]`, phylo-block `[0.202,0.346]`, wild `[0.201,0.303]` | PRESENT | Line 126 has cluster CI; later line 490 has all three; CSVs confirm rounded values. |
| HIV-1 Layer A `n=23` mapped, `n=26` tags | PRESENT | Not in scoped lines, but line 902/ch5 and CSVs confirm: `feature_matrix_HIV-1.csv` layer sum 23; `layer_a_tags.csv` HIV-1 rows 26. |
| D614G retained in Layer A per Korber 2020 | PRESENT | Line 219 present; CSVs confirm position 614 retained. |
| Stage 1 functional regions `417 AA` (=1251 nt/3), not 439 | PRESENT | Lines 25/50/63 show 1,251 nt and 417 AA; no scoped regression. |
| Single-position scoring, gap-aware, not point-substitutions-only | PRESENT | Ch5 line 239 says single-position benchmark; no "point substitutions only" regression found. |
| P1 null at/below mean: `6/12`, `4/12`, `7/12` | PRESENT | Line 841 has 6/12 iid/circular, 4/12 block, 7/12 local-burden. |
| Decision curve budget 50 random baseline `41` expected TPs | PRESENT | Line 837 has `41` for random allocation. |

## 4. Compression candidates

| Lines | Candidate reduction |
|---|---|
| 126 | Split or compress the long CI-disambiguation sentence; about 30--45 words can be saved by moving resampling-unit caveat to a footnote. |
| 151 | Remove repeated "Frequency alone, trained on..." wording after the numeric result; about 18--25 words saved. |
| 186 | The final interpretive sentence duplicates "forward-time signal" language; about 20 words saved. |
| 197 | Very dense paragraph; move per-pathogen examples or file list to a parenthetical/footnote; 35+ words saved. |
| 231--234 | Lines 233 and 234 duplicate the information-type-analysis sentence; remove one for about 18 words saved. |

## 5. Overall tally

Critical: 0; Major: 2; Minor: 5; Verified: 7; Regressions: 0.

RESULT_AUDIT_V3_ch4b: critical=0 major=2 minor=5 regression=0
