# Audit v3 ch3b: `ch3_methods.tex` lines 128--254

Read-only audit against `results/mutbench/**/*.csv`, wave CSVs, `feature_analysis`, `references.bib`, and chapter labels.

## 1. Per-paragraph audit table

| Lines | Claims | Source check | Citations | Cross-refs | Severity |
|---|---|---|---|---|---|
| 129--132 | 3-layer ground truth; Layer A positives, Layer B constrained negatives, Layer C DMS; Stage 1 synthetic + DMS functional annotations. | Three-layer roles match `tab:gt_positions`, `layer_c_evaluation.csv`, and surrounding methods. Stage 1 synthetic/DMS detail is outside this chunk but consistent with later Stage 1 section. | none | `subsec:3layer_gt` resolves. | Verified |
| 134--137 | 20 scoring types, 6 scoring categories, 14 detector families, 39 variants, 5 detector categories; Stage 2 factorial design. | `stage3_full_results.csv` verifies 20 scoring values, 39 detector variants, 14 families, 11 pathogens, 8,580 rows. Category labels are manuscript taxonomy, not a CSV field, but consistent with listed score/family names. | none | `subsec:stage1`, `sec:stage2` resolve. | Verified |
| 139--142 | Metrics: MCC, F1, enrichment, constrained FPR, DMS F1; statistical methods ANOVA/Friedman/LOPO; Stage 1 hotspot-score, Stage 2 MCC. | Metrics columns verified in `combined_10scoring_results.csv`, `multilayer_9pathogen_results.csv`, `stage3_full_results.csv`, and `method_comparison.csv`; ANOVA/Friedman/LOPO result files exist. | none | `sec:eval_stat_design` resolves. | Verified |
| 145--149 | 3-layer framework uses three independent biological evidence sources; figure illustrates structure. | Conceptual claim consistent with source layer separation. "Independent" is methodological independence, not statistical independence; no contradiction found. | none | `fig:3layer_gt_concept` resolves. | Verified |
| 151--188 | Figure says Layer A true positives/MCC, Layer B constrained negatives/FPR, Layer C DMS validation/DMS F1; three orthogonal dimensions. | Matches `layer_c_evaluation.csv` and evaluation columns. Layer B "true negatives" is qualified by constrained FPR in caption/integration, avoiding universal-negative overclaim. | none | figure label resolves. | Verified |
| 190--209 | Table: Layer C top 20%; DMS available for 6 pathogens. | `layer_c_evaluation.csv` has exactly 6 pathogens: EV-A71, H3N2, HIV-1, RSV, Rabies, SARS-CoV-2. Top-20% definition is reflected by `layer_c` indicators and DMS table text. | none | `tab:gt_layer_roles` resolves. | Verified |
| 211--217 | Layer A literature-curated adaptive/diversifying positions; SARS-CoV-2 E484K in Beta/Gamma/Mu and E484A in Omicron; union per `tab:gt_positions`. | Layer A positions/tags verified in `layer_a_tags.csv`; exact lineage emergence is citation-backed but not locally CSV-verifiable. No D614G exclusion language. | no direct cite in paragraph; table source referenced. | `tab:gt_positions` resolves. | Minor |
| 218--220 | Pathogen-specific Layer A criteria: SARS-CoV-2/H3N2 convergent sites with >=3 lineages; Norovirus epochal; HCV HVR1/HVR2; seven remaining pathogens immune-escape lists; heterogeneity omega range 0.234--0.296. | Tag counts and pathogen composition match `layer_a_tags.csv`/`tab:gt_positions`. `gt_heterogeneity_analysis.csv` and robustness summaries support a range ending at 0.296; exact 0.234 lower bound is consistent with discussion text but not exposed as a clearly named row in the inspected summary files. | table source references. | `ch:discussion`, `sec:gt_heterogeneity`, `tab:gt_positions` resolve. | Minor |
| 221--223 | Preregistered thresholds/grid: Layer B dN/dS <0.5, Layer C top 20%, `20 x 39 = 780`, `20 x 14 x 11 = 3,080`, SOP freeze 2024-08-12, no post-hoc adjustment, Bonferroni denominator 780; SARS-CoV-2 examples from Carabelli; no de novo convergent-position discovery. | Arithmetic correct. `stage3_full_results.csv` verifies 20/39/14/11. SOP/freeze/no-post-hoc claims are not independently verifiable from listed CSVs. Carabelli key exists. | `carabelli2023convergent` exists in `references.bib`. | `subsubsec:preregistration` created here. | Minor |
| 225--231 | Layer B purifying/essential sites as constrained-negative reference; in MCC they are part of all non-Layer-A positions; constrained FPR computed against Layer B. | Evaluation contract matches `multilayer_9pathogen_results.csv` columns (`gt_constrained_size`, `constrained_fpr`) and `subsec:9pathogen_metrics`. The biological wording "any mutation here is lethal or severely deleterious" is stronger than the operational evidence and should read "often" or "expected to". | none | `subsec:9pathogen_metrics` resolves. | Minor |
| 233--236 | Layer B criteria: structural essentiality/evolutionary conservation, dN/dS <0.5, `dnds_proxy` is a feature not construction criterion; SARS-CoV-2 154 Layer B positions including HR1 912--984, HR2 1163--1213, cysteines; no de novo computation. | SARS-CoV-2 Layer B count 154 verified in `tab:gt_positions` and `multilayer_9pathogen_results.csv`. `dnds_proxy` exists as a Stage 3 scoring channel in `stage3_full_results.csv`. HR ranges/cysteines are citation-backed but not directly represented in inspected CSVs. | `yang2007paml`, `wrapp2020cryo` exist. | `subsec:9pathogen_scoring` resolves. | Verified |
| 238--244 | Six DMS pathogens; top 20% mean absolute effect; threshold sweep at 10/20/30 on 4 of 6; Rabies/EV-A71 deferred; "rankings stable" and "no observed pathogen rotates winning Layer-C-aligned scoring"; DMS phenotypes by pathogen. | Six pathogens verified in `layer_c_evaluation.csv`; sweep coverage and thresholds verified in `dms_threshold_sensitivity_analysis.csv`. **Contradiction:** best scoring is not stable for 3/4 swept pathogens: SARS-CoV-2 changes `rank(P*E)` to `E*rare`; HIV-1 changes `E*rare`/`P*E*rare`/`minority_E`; RSV changes `rank(P*E)` to `P*minority_E`. Only H3N2 keeps `rank(P*E)`. Phenotype/source rows broadly match `provenance/dms_sources.csv`, though SARS-CoV-2 also has Greaney RBD and Dadonaite full-Spike entries. | all cited DMS keys exist. | `subsec:dms_evolution_correlation`, `tab:dms_preprocessing` resolve. | **Major** |
| 246--254 | DMS preprocessing table caption: mean absolute effect, top-20% threshold, processed-fitness tables, replicate aggregates consumed by pipeline. | Top-20% and released processed-table framing match `dms_data/*.csv` (`fitness_score`, `n_mutations`, `layer_c`) and `provenance/dms_sources.csv` (`replicates_in_pipeline=2`). "Every possible single amino acid substitution" from line 241 is slightly overbroad because DMS CSVs show `n_mutations` can be 19 or fewer at some positions. | none in caption. | `tab:dms_preprocessing` resolves. | Minor |

## 2. Per-section severity counts

| Section | Critical | Major | Minor | Verified |
|---|---:|---:|---:|---:|
| Components overview, 128--142 | 0 | 0 | 0 | 3 |
| 3-layer framework and roles, 145--209 | 0 | 0 | 0 | 4 |
| Layer A, 211--223 | 0 | 0 | 3 | 0 |
| Layer B, 225--236 | 0 | 0 | 1 | 1 |
| Layer C/table start, 238--254 | 0 | 1 | 1 | 0 |

## 3. Recent-fix verification

| Anchor | Status | Check |
|---|---|---|
| omega CI `[0.201, 0.346]`; phylogenetic-block `[0.202, 0.346]`; wild-cluster `[0.201, 0.303]` | PRESENT | Not in scoped lines except 0.234--0.296 range. Current CSVs verify rounded intervals from `cluster_bootstrap_omega_summary.csv`, `block_bootstrap_omega_summary.csv`, `wild_cluster_bootstrap_omega_summary.csv`; no scoped regression. |
| HIV-1 Layer A `n=23` mapped gp120; `n=26` curation tags | PRESENT | `tab:gt_positions` uses 23; `layer_a_tags.csv` has 26 HIV-1 rows; no scoped regression. |
| D614G retained in Layer A per Korber 2020, not excluded | PRESENT | `layer_a_tags.csv` includes `SARS-CoV-2,614,functional`; scoped text does not exclude D614G. |
| Stage 1 functional regions `417 AA` (=1251 nt/3), not 439 | PRESENT | Outside scope at ch3 line 396; correct value present; no scoped regression. |
| Single-position scoring gap-aware, not "point substitutions only" | PRESENT | No scoped bad wording; broader ch3 uses single-position regime. |
| P1 null at-or-below mean: 6/12 iid/circular; 4/12 block; 7/12 local-burden | PRESENT | Outside scope; current ch4 text has corrected counts. |
| Decision curve budget 50 random baseline: 41 expected TPs | PRESENT | Outside scope; current ch4 text uses 41, not ~30. |

## 4. Compression candidates

| Lines | Candidate reduction |
|---|---|
| 221 | Split or compress preregistration paragraph by moving SOP freeze, Bonferroni policy, and ANOVA correction nuance to a footnote; likely saves 60--90 words without losing claims. |
| 227--231 | Replace explanatory contrast between positive and purifying selection with one sentence plus metric contract; likely saves 25--35 words. |
| 241--243 | Compress DMS explanation and threshold caveat after fixing the stability claim; likely saves 50--80 words. |
| 248 | Table caption can drop replicate-publication caveat to the footnote already present below the table; likely saves 25--40 words. |

## 5. Overall tally

Critical: 0; Major: 1; Minor: 5; Verified: 8; Recent-fix regressions: 0.

RESULT_AUDIT_V3_ch3b: critical=0 major=1 minor=5 regression=0
