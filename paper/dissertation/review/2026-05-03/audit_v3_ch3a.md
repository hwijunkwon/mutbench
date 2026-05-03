# Audit v3 ch3a: `ch3_methods.tex` lines 1--127

Scope checked against `results/mutbench/**/*.csv`, wave/layerA-prime/feature-analysis CSVs, `references.bib`, and cross-chapter labels.

## 1. Per-paragraph audit table

| Lines | Claims | Source check | Citations | Cross-refs | Severity |
|---|---|---|---|---|---|
| 1--3 | Chapter title and `ch:mutbench` label. | Structural only. Label is unique. | n/a | no issue | Verified |
| 5--12 | MutBench uses 11 RNA viruses, 20 scoring types, 14 detection families, 39 parameter variants, 3-layer GT, MCC/hotspot-score; Stage 1/2/3 framing. | `stage3_full_results.csv` verifies 8,580 rows = 11 pathogens x 20 scoring x 39 detector variants, with 14 families. `layer_c_evaluation.csv` and GT sections support 3-layer framing. However “5 detection categories” is a prose taxonomy not represented in the checked CSVs, and “hotspot-score composite metric” is Stage-1-specific while the Stage-2 archive is MCC/F1/precision/recall. | n/a in paragraph | all refs resolve: `subsec:stage3_methods`, materials/methods/framework/3layer/stage1/stage2/eval labels. `sec:9pathogen_benchmark` label at line 12 is odd but unique. | Minor |
| 21--30 | Eleven-virus panel, protein lengths, full-length note, rates/ranges, Zika excluded because only 52 unique E sequences; Zika in 12-pathogen feature analysis. | Pathogen list and post-truncation lengths match feature matrices (`SARS-CoV-2=1259`, `MERS=1330`, `RSV=550`, `H3N2=543`, `Influenza_B=560`, `HIV-1=450`, `HCV=340`, `Norovirus=536`, `Dengue=490`, `Rabies=491`, `EV-A71=261`). `provenance/genbank_queries.csv` verifies the 11 main pathogens but has no Zika query row; `feature_matrix_Zika.csv` verifies only 452 positions, not 52 unique sequences. Substitution-rate and full-length examples are not backed by a CSV in the specified source set. | No citations attached to rates/full-lengths/Zika count. | `sec:information_analysis` resolves to ch4. | Major |
| 33--34 | 8 ICTV families, 4 transmission routes, rate range, unique ratios 15.1%--100%, D614G/founder effects, H3N2 antigenic sites, Influenza B pooling, HCV HVR1 384--410, HCV sensitivity `omega^2=0.246`, Norovirus homoplasy AUC 0.944, six Layer C pathogens, Zika exclusion. | Unique ratios verify from table counts: 753/4982=15.1%, Rabies and EV-A71 100%. Layer C pathogen set matches `layer_c_evaluation.csv`: SARS-CoV-2, H3N2, HIV-1, RSV, Rabies, EV-A71. D614G is present in `layer_a_tags.csv` as functional Korber 2020 evidence. Norovirus homoplasy AUC verifies as 0.9435 in `feature_analysis/per_feature_auc.csv`. HCV `omega^2=0.246` is backed only as a body target / reported HCV-exclusion sensitivity (`cluster_bootstrap_omega_summary.csv` has HCV-excluded observed 0.2534, body target 0.246); wording “HCV-only ANOVA” appears wrong. Rate/family/transmission claims are not CSV-backed. Zika 52 remains unsupported. | `korber2020tracking` exists, but line has no direct cite. Other biological facts lack local citations in paragraph. | All refs resolve: `tab:pathogen_data`, `subsec:layer_a`, `tab:gt_positions`, `ch:discussion`, `sec:gt_heterogeneity`, `sec:information_analysis`. | Major |
| 37--42 | GenBank query/provenance, query dates 2024-11--2024-12, SARS-CoV-2 query and 3500--4000 nt filter, dedup at 100%, no <100% clustering, no HMMER filtering, MAFFT v7.505 auto, frequency/entropy definitions, min-length truncation, GT positions beyond alignment excluded. | `provenance/genbank_queries.csv` verifies query strings, dates, total hits, unique counts, and MAFFT modes for 11 pathogens. Feature matrices verify post-truncation alignment lengths. The archive does not independently verify ambiguous-base filtering, SHA-256 implementation equivalence, or that HMMER was not run; those are methods/provenance assertions. Single-position coding-region scope is present and does not regress to “point substitutions only.” | Bib entries exist for `fu2012cdhit`, `steinegger2017mmseqs2`, `eddy2011hmmer`, `katoh2013mafft`. | refs to `tab:gt_positions` and `tab:pathogen_data` resolve. | Minor |
| 44--72 | Table of sequence dataset characteristics; caption/minipage explain query date and MAFFT mode, 10/11 FFT-NS-2 and EV-A71 L-INS-i. | Counts, accessions, dates, unique counts and MAFFT modes match `provenance/genbank_queries.csv`; alignment lengths match feature matrices. 10/11 FFT-NS-2 is correct. The heuristic explanation for MAFFT `--auto` cut-over is not directly backed by the CSVs, but it is tied to the MAFFT citation. | `katoh2013mafft` exists. | `tab:pathogen_data` label unique. | Verified |
| 75--83 | Methods section/framework overview: 3-component pipeline; 20 scoring types and 14 detection families; multi-metric factorial analysis; Stages 1/2 plus separate Stage 3. | `stage3_full_results.csv` verifies 20 scoring, 14 families, MCC/precision/recall/F1. `stage3_statistics.csv` verifies factorial ANOVA. Stage separation is consistent with later labels. | n/a | `fig:mutbench_pipeline`, `subsec:stage3_methods` resolve. | Verified |
| 85--127 | Pipeline figure: input 11 pathogens; 6 scoring categories/20 types; detection 39 methods/14 families; 3-layer GT; MCC/hotspot-score; ANOVA/Friedman/LOPO. | 11/20/39/14 verified from `stage3_full_results.csv`. Statistical methods verified from `stage3_statistics.csv` plus ch3 later labels. Figure node says “39 methods” whereas prose correctly calls them 39 parameter variants/detector variants; this may confuse variants with families/methods. | n/a | figure label unique. | Minor |

## 2. Per-section severity counts

| Section | Critical | Major | Minor | Verified |
|---|---:|---:|---:|---:|
| Chapter opening / roadmap (1--12) | 0 | 0 | 1 | 1 |
| Materials: target pathogens/data (15--72) | 0 | 2 | 1 | 1 |
| Methods: framework overview/figure (75--127) | 0 | 0 | 1 | 1 |

## 3. Recent-fix verification

| Anchor | Status | Check |
|---|---|---|
| `omega^2` CI cluster `[0.201, 0.346]`, phylogenetic-block `[0.202, 0.346]`, wild-cluster `[0.201, 0.303]` | NOT PRESENT | No in-scope claim; CSVs verify rounded values in `cluster_bootstrap_omega_summary.csv`, `block_bootstrap_omega_summary.csv`, `wild_cluster_bootstrap_omega_summary.csv`. |
| HIV-1 Layer A `n=23` mapped to gp120; `n=26` in `layer_a_tags.csv` | NOT PRESENT | No in-scope text. CSVs verify `per_feature_auc.csv` has HIV-1 `n_layer_a=23`; `layer_a_tags.csv` has 26 HIV-1 rows. |
| D614G retained in Layer A per Korber 2020 | PRESENT | Line 34 mentions D614G as founder/functional context; `layer_a_tags.csv` contains SARS-CoV-2 614 functional, Korber 2020. No exclusion regression. |
| Stage 1 functional regions `417 AA` not `439` | NOT PRESENT | No in-scope functional-region count. No `439` in scoped lines. Later ch4/ch3 lines show 417. |
| Single-position scoring, gap-aware, not “point substitutions only” | PRESENT | Line 37 says “single-position regime within the coding region”; no “point substitutions only” in scope. “Gap-aware” term itself is not present. |
| P1 null at-or-below-mean `6/12`, `4/12`, `7/12` | NOT PRESENT | No in-scope claim. Later ch4 line 841 has the corrected values; `p1_null_per_pathogen.csv` supports the audit. |
| Decision curve budget 50 random baseline `41` expected TPs | NOT PRESENT | No in-scope claim. `codex_wave1/p2_decision_curve.csv` sums random budget-50 expected TPs to 41. |

## 4. Compression candidates

| Lines | Candidate | Reduction |
|---|---|---:|
| 5--12 | Combine roadmap sentences and remove repeated Stage 1/2/3 explanation; keep one sentence for design and one for section map. | 35--55 words |
| 33--34 | Split or compress the long “Per-pathogen biological context” paragraph; move detailed examples to table notes or later Layer A section. | 80--120 words |
| 37 | This paragraph is overpacked. Move CD-HIT/MMseqs/HMMER caveats to provenance note; keep GenBank query, filtering, dedup, MAFFT, scoring definitions. | 120--180 words |
| 68--71 | Shorten MAFFT `--auto` heuristic note to “EV-A71 selected L-INS-i; all others selected FFT-NS-2; modes are logged for reproducibility.” | 35--45 words |
| 81--83 plus figure caption | Remove duplicated framework wording already stated in lines 5--12 and caption. | 20--35 words |

## 5. Overall tally

Critical: 0; Major: 2; Minor: 4; Verified: 4; Regression: 0.

RESULT_AUDIT_V3_ch3a: critical=0 major=2 minor=4 regression=0
