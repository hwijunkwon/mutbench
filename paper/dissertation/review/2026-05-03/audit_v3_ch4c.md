# Audit v3 ch4c: `ch4_results.tex` lines 248--370

Scope checked against `results/mutbench/**/*.csv`, `codex_wave[1-5]`, `codex_layerA_prime`, `feature_analysis`, `references.bib`, and `\label{}`/`\ref{}` resolution.

## 1. Per-paragraph audit table

| Lines | Claims | Source check | Citations | Cross-refs | Severity |
|---|---|---|---|---|---|
| 248--250 | Metrics are MCC/F1/precision/recall; Layer C DMS for 6 pathogens; GenBank actual accessions. | `stage3_full_results.csv` has `mcc,precision,recall,f1`; `layer_c_evaluation.csv`/DMS files cover SARS-CoV-2, H3N2, HIV-1, RSV, Rabies, EV-A71; `provenance/genbank_queries.csv` has 11 reference accessions and query dates. | None needed here. | No refs. | Verified |
| 256--257 | 11 pathogens; best by MCC; all 11/11 distinct best combinations. | Best-by-MCC rows in `stage3_full_results.csv` verify 11 pathogens and table values, but only 10 unique `(scoring, detector)` tuples: Influenza_B and MERS both `freq + KDE(p=85)`. | None. | `tab:stage2_best` resolves. | **Major** |
| 261--285 | Table values; 4/6 categories; 9 distinct scorings; HIV-1 `n_A=23` vs `layer_a_tags.csv` 26; minipage uniqueness note. | MCC rows verified exactly/rounded: HCV 0.660, H3N2 0.534, Norovirus 0.510, Influenza_B 0.392, HIV-1 0.275, Dengue 0.274, EV-A71 0.260, Rabies 0.248, SARS-CoV-2 0.211, RSV 0.196, MERS 0.196. Feature matrices verify HIV-1 `layer_a=23`; tags verify 26. 9 scorings and 4 categories are correct. But minipage says family-level all 11 unique; false because `freq + KDE` is shared by Influenza_B/MERS. | None. | `tab:gt_heterogeneity`, `sec:limitations`, `ch:discussion` resolve in English files. | **Major** |
| 289--290 | Probability all 11 unique is ~0.932; LOPO gap 0.265 and 0/11 null-consistent. | Arithmetic for hypothetical all-unique is correct, but premise conflicts with observed 10 unique tuples. `stage3_statistics.csv` supports LOPO gap 0.265 and 0/11 over 11; older `lopo_9pathogen_cv.csv` is 9-pathogen and gives mean gap 0.277, so the manuscript should cite/source the 11-pathogen summary explicitly. | None. | None. | **Major** |
| 292 | Interaction `omega^2=0.296`, scoring main effect 6.3%, oracle/generalized gap 0.265. | `stage3_statistics.csv`: scoring x pathogen 0.296252, scoring 0.063009, LOPO metric 0.265424. | None. | None. | Verified |
| 294--296 | Worst-end grid: 8,580 cells; worst HCV/stability/SWAN row 6782 MCC -0.361; negative counts; worst families/scorings; MCC range. | `stage3_full_results.csv`: 8,580 rows; idx 6782 exactly HCV/stability/SWAN(w=50,k=1.0), MCC -0.361346, precision/recall 0, `n_detected=139`; 4,171 MCC<0 (48.6%), 4,695 MCC<=0 (54.7%); ScoreDBSCAN ep15/ep8 and `plddt_inv`, `grantham`, `tranception` means match rounded values. | None. | `tab:stage2_best` resolves. | Verified |
| 298--306 | Heatmap/category figures; no single category dominates; best scorings span four of six categories. | Figure files exist. Four categories verified from best scorings: frequency, MSA, phylogenetic, AI. The "no single category dominates" claim is interpretive but consistent with 4-category spread. | None. | `fig:scoring_detection_heatmap`, `fig:scoring_category_bar`, `tab:stage2_biology_rationales` resolve. | Verified |
| 317--327 | Biological rationale table; Norovirus AUC 0.944 vs freq 0.760; MERS fewer than 500 public spike sequences. | Norovirus AUC verified in `per_feature_auc_11pathogens.csv` / `per_feature_auc_v2.csv` (homoplasy 0.944 rounded; freq 0.760). Best scoring names align with Table. However MERS count conflicts with `provenance/genbank_queries.csv`: 1,311 hits and 530 unique after dedup, not fewer than 500 public spike sequences. Several biological rationales are plausible but not directly sourced in table. | `covfit2025` key exists; other rationale rows lack direct citations. | Table label resolves. | **Major** |
| 332--333 | Detection-family counts; FUBAR spotlight; MCC range 0.196--0.660. | Best rows give KDE 4, Wavelet 3, SlidingTest/Bayes/MutClust-Orig/SWAN 1 each; range verified. | None. | `fig:fubar_spotlight` resolves. | Verified |
| 334--335 | Lowest tier values; SARS-CoV-2 25/1259 = 2.0%; D614G retained per Korber; small TP count constrains MCC. | `feature_matrix_SARS-CoV-2.csv`: 1,259 rows, 25 Layer A positives. `layer_a_tags.csv` has SARS-CoV-2 position 614 functional, evidence "Korber 2020". Low-tier MCC values verified from best rows. | `korber2020tracking` key exists. | None. | Verified |
| 337--348 | Figure captions: category means; FUBAR H3N2 0.534 highest for H3N2. | Figure files exist; H3N2 best row is `fubar_bf + Wavelet(t=1.5)`, MCC 0.534058. Category mean statement not directly recomputed from image but consistent with archived figure. | None. | Figure labels resolve. | Verified |
| 351--370 | Statistical subsection setup; ANOVA with MCC; bias-corrected `omega^2`; table caption says scoring x pathogen 0.296 and residual ~0.39. | `stage3_statistics.csv` supports 0.296252 and modeled-factor values; residual SS is archived, and later text/table body outside this line window gives the residual framing. | `cohen1988statistical` appears later; key exists. | `subsec:9pathogen_statistical`, `subsec:9pathogen_anova`, `eq:omega_squared`, `tab:stage2_anova` resolve. | Verified |

## 2. Per-section severity counts

| Section | Critical | Major | Minor | Verified |
|---|---:|---:|---:|---:|
| Carry-over setup, 248--250 | 0 | 0 | 0 | 1 |
| Per-pathogen best method analysis, 253--350 | 0 | 4 | 0 | 7 |
| Statistical analysis opening, 351--370 | 0 | 0 | 0 | 1 |

## 3. Recent-fix verification

| Anchor | Status | Check |
|---|---|---|
| omega CI `[0.201,0.346]`, phylo-block `[0.202,0.346]`, wild `[0.201,0.303]` | PRESENT | Not in scoped lines, but present later in Ch4 and Ch3; `omega_robustness_5way.csv` confirms rounded intervals. |
| HIV-1 Layer A `n=23` gp120; `n=26` tags | PRESENT | Scoped caption matches; feature matrix and `layer_a_tags.csv` verify. |
| D614G retained in Layer A per Korber 2020 | PRESENT | Scoped line 335 and `layer_a_tags.csv` verify position 614 retained. |
| Stage 1 functional regions `417 AA` not `439` | PRESENT | Outside scope line 50; correct. |
| Single-position scoring, gap-aware, not "point substitutions only" | PRESENT | Ch3 states single-position coding-region regime; no scoped regression found. |
| P1 null at-or-below-mean `6/12`, `4/12`, `7/12` | REGRESSION | Detailed paragraph line 841 is corrected, but audit-ledger line 747 still says `5/12 iid sig -> 1/12`, mixing significance with the fixed at-or-below-mean anchor. |
| Decision curve budget 50 random baseline `41` expected TPs | PRESENT | Ch4 line 837 and `codex_wave1/p2_decision_curve.csv` verify random sum at budget 50 = 41. |

## 4. Compression candidates

| Lines | Candidate reduction |
|---|---|
| 261 caption | Move HIV-1 count caveat to footnote or table note; reduce caption by ~35--45 words without losing table meaning. |
| 285 minipage | Replace with: "Nine scoring types appear; `freq` is shared by HCV, Influenza B, and MERS. Influenza B and MERS also share `KDE(p=85)`, so 10/11 parameter tuples are unique." Saves >35 words and fixes the claim. |
| 296 paragraph | Split or compress operational-cost interpretation; the verified numeric floor can be retained while removing ~60 words of repeated "pathogen-aware" explanation. |
| 317--327 rationale table | Shorten reason cells by 15--25 words each for HCV, Dengue, MERS, and SARS-CoV-2; current wording mixes result explanation with unsupported biological narration. |

## 5. Overall tally

Scoped rows: Critical 0, Major 4, Minor 0, Verified 9. Recent-fix regressions: 1.

RESULT_AUDIT_V3_ch4c: critical=0 major=4 minor=0 regression=1
