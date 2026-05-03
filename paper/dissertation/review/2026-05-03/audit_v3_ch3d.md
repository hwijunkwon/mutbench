# Audit v3 ch3d: Methods lines 382--508

Scope: `paper/dissertation/chapters_en/ch3_methods.tex` lines 382--508. Sources checked: `results/mutbench/**/*.csv`, wave/layerA/feature-analysis CSVs, `references.bib`, and chapter labels/refs.

## 1. Per-paragraph audit table

| Lines | Claims | Source check | Citations | Cross-refs | Severity |
|---|---|---|---|---|---|
| 382--397 | Functional-region table tail: NTD 138 nt; S1/S2 15; S2' 6; fusion peptide 54 with 3-nt overlap; HR1 219; HR2 153; dedup total 1,251 nt = 417 codons/AA; raw sum 1,254. | Arithmetic verified from intervals: 46+5+2+18+73+51 AA = 195 AA in visible rows, plus RBD 223 AA = 418 raw codons = 1,254 nt; one shared AA816 codon gives 417 unique codons = 1,251 nt. | Table provenance immediately above scope cites `wrapp2020cryo`, `mccallum2021ntd`; both bib keys present. | `tab:ground_truth` defined at line 375. | Verified |
| 400--407 | Figure maps seven regions to SARS-CoV-2 genome length 29,903; Spike nt 21,563--25,384; 1,251 unique Spike nt. | Genome length and Spike coordinates match standard NC_045512.2 coordinate convention and figure file exists at `results/mutbench/genome_hotspot_map.png`. “Minimal functional annotation” outside Spike is an interpretation, not a measured CSV claim. | No new citation in paragraph; relies on preceding region citations. | `fig:mutbench_hotspot_map` defined line 406 and referenced line 400. | Verified |
| 412--423 | 14 detection families; MutClust only virus-specific hotspot tool; H-score and entropy formulas; adaptive DBSCAN `epsilon=gamma*H_i`, `gamma=0.5`, MCC sensitivity +/-0.01 for gamma sweep; DBSCAN/HDBSCAN params; five Stage-1 variants; v2c highest HS 0.778; Stage 2 retains v1. | `stage3_full_results.csv` verifies 14 families and `MutClust-Orig` as the retained Stage-2 MutClust family. Ch4 Table `tab:hotspot_scores` and prior audit trail verify HS 0.778. **But no `gamma_sensitivity.csv` exists under `results/mutbench`; prior audit also flagged this.** HDBSCAN parameter values are method parameters, not independently sourceable from CSV in this bundle. | `youn2025mutclust` bib key present. | `eq:mutbench_hscore`, `eq:shannon_entropy`, `eq:expand_cluster`, `subsec:improvements` all defined; duplicate label pattern acceptable but `subsec:mutbench_hscore` names an equation-adjacent anchor. | Major |
| 414--421 | Displayed H-score and Shannon entropy equations. | Equations are internally consistent with line 412. | none needed. | Equation labels defined and used. | Verified |
| 428--436 | Hotspot-score = mean(recall, precision, stability); stability is mean Jaccard over 100 random 80% subsampling with 20% zeroing; Stage 2 uses MCC instead. | Formula and protocol are method definitions; Ch4 table states “100 subsamplings, 80% retention.” MCC rationale target exists at lines 725--757. | none. | `eq:hotspot_score`, `subsec:9pathogen_metrics` resolve. | Verified |
| 441--469 | Stage-1 temporal scoring variants distinct from 20 Stage-2 types; H-score saturation identified in Ch4 temporal section; top 5/10/20% and median thresholds; F1/enrichment/Cohen's d. | Stage-2 scoring count verified by `stage3_full_results.csv` unique scoring types = 20. Table entries are method definitions. Temporal section label resolves in Ch4. | none. | `subsec:9pathogen_scoring`, `sec:temporal`, `tab:alternative_scoring`, `eq:mutbench_hscore` resolve. | Verified |
| 474--476 | Three SARS-CoV-2 validation analyses; PDB 6VSB, 8-A C-alpha contact cutoff, 1,000 permutation null, enrichment ratio/z-stat; restricted to SARS-CoV-2 experimental structure; other pathogens use ESMFold. | Ch4 reports 5.92x, z=13.34, 1,000 subsets; `tab:structure_sources` says SARS-CoV-2 contact uses PDB 6VSB and others not analyzed. `hotspot3d_results.csv` is not the exact permutation-contact table but supports structural archive presence. | `wrapp2020cryo` bib key present. | `ch:results`, `sec:cross_pathogen_structural`, `tab:structure_sources` resolve. | Verified |
| 478 | Coalescent simulation: 100 replicates, N=500, founder vs 3 convergent substitutions; H-score/Fitch/TreeTime scoring; seeds 42--141. | Ch4 reports 100 replicates and N=500; `phylo_sensitivity_results.csv`/comparison support homoplasy-vs-H-score simulation outputs. Seed range is a method detail not exposed in located CSV. | none. | `sec:phylo_simulation` resolves in Ch4. | Minor |
| 480 | TreeTime v0.11 on SARS-CoV-2 IQ-TREE GTR+G 1,000 UFBoot tree; production homoplasy is Fitch/FastTree; compare Spearman and AUC; TreeTime settings listed. | `treetime_homoplasy/full_output.txt` confirms a TreeTime run on 500 Spike sequences/1273 positions; `per_position_counts.csv` has 1273 positions. Located outputs do not expose TreeTime version/IQ-TREE settings. Production homoplasy files exist under `homoplasy_scores/`; `homoplasy_gt_validation.csv` verifies AUC-style validation channel. | `sagulenko2018treetime`, `price2010fasttree` bib keys present. | All labels resolve; audit-channel boundary is clear. | Minor |
| 485 | H3N2 pilot: raw 9,000 pre-dedup 2010--2025, three 3,000-sequence windows; Stage-2 unique panel 2,562; train 2010--2015; Layer A Koel 25 sites; emerging thresholds <5% and >=10%; k=20/30/50; Fisher exact; results in Ch4. | `feature_analysis/h3n2_temporal_pilot.csv` exactly verifies reported reference sizes/overlaps/enrichments in Ch4; `stage3_full_results.csv` has H3N2 Stage-2 panel context indirectly, and Ch3 table gives 2,562. The raw 9,000/window construction is method text, not fully exposed in this CSV. | `koel2013substitutions` bib key present. | `tab:design_characteristics`, `ch:discussion`, `sec:future_work`, `subsec:h3n2_temporal_pilot` resolve. | Verified |
| 488--508 | Stage 2 extends to 11 pathogens; 20 scoring types x 39 detector variants from 14 families x 11 = 8,580; 20 scoring types in 6 categories. | `stage3_full_results.csv` parsed: 8,580 rows, 11 pathogens, 20 scoring types, 39 detector variants, 14 families; product equals 8,580. Six categories visible in `tab:scoring_types`. | none. | `sec:stage2`, `subsec:9pathogen_scoring`, `sec:scoring_detection`, `tab:scoring_types` resolve. | Verified |

## 2. Per-section severity counts

| Section | Critical | Major | Minor | Verified |
|---|---:|---:|---:|---:|
| Functional regions + map | 0 | 0 | 0 | 2 |
| MutClust variant comparison | 0 | 1 | 0 | 1 |
| Hotspot-score metric | 0 | 0 | 0 | 1 |
| Temporal scoring variants | 0 | 0 | 0 | 1 |
| Structural/phylogenetic validation | 0 | 0 | 2 | 1 |
| H3N2 temporal protocol | 0 | 0 | 0 | 1 |
| Stage 2 opening/scoring table | 0 | 0 | 0 | 1 |

## 3. Recent-fix verification

| Anchor | Status | Check |
|---|---|---|
| Omega CIs: cluster [0.201, 0.346], phylo-block [0.202, 0.346], wild [0.201, 0.303] | PRESENT | `omega_robustness_5way.csv` has 0.2008--0.3455, 0.2022--0.3457, 0.2005--0.3032; Ch4 current text uses rounded values. |
| HIV-1 Layer A n=23 gp120 MCC; n=26 in `layer_a_tags.csv` | PRESENT | `hotspot3d_results.csv` HIV-1 row has `n_gt_positive=23`; `layer_a_tags.csv` has 26 HIV-1 rows. |
| D614G retained in Layer A per Korber 2020 | PRESENT | `layer_a_tags.csv` includes SARS-CoV-2 position 614 functional, Korber 2020; Ch4 states retained. |
| Stage 1 functional regions 417 AA, not 439 | PRESENT | Line 396 says 417 codons/AA; no 439 in scope. |
| Single-position scoring gap-aware, not point substitutions only | PRESENT | Ch3 line 37 says single-position coding-region regime; Stage-2 table includes `freq_with_indel` and `entropy_with_indel`; no “point substitutions only” regression found in scope. |
| P1 null at-or-below mean counts: 6/12 iid/circular, 4/12 block, 7/12 local | PRESENT | `codex_wave1/p1_null_per_pathogen.csv` supports the corrected counts; no conflicting text found in audited lines. |
| Decision curve budget 50 random baseline = 41 expected TPs | PRESENT | `codex_wave1/p2_decision_curve.csv` sums random budget-50 expected TP to 41. |

## 4. Compression candidates

| Lines | Candidate | Estimated reduction |
|---|---|---:|
| 412 | Split the long MutClust/HDBSCAN parameter sentence: move H-score formula references to equations and keep only parameter deltas in prose. | 35--50 words |
| 423 | Compress Stage-2 retention rationale to “v2c is H-score-specific; Stage 2 keeps published v1, whose non-H-score rows bypass the upstream H-score bug.” | 35--45 words |
| 476 | Shorten spatial-contact paragraph by removing general cutoff justification and merging permutation/enrichment definitions. | 25--35 words |
| 480 | Compress TreeTime paragraph by moving settings to a parenthetical appendix-style sentence. | 25--40 words |
| 485 | H3N2 pilot paragraph can be divided and shortened; the Fisher table formula and future-work sentence can be moved to methods supplement. | 60--90 words |

## 5. Overall tally

Critical: 0; Major: 1; Minor: 2; Verified rows: 9; Recent-fix regressions: 0.

RESULT_AUDIT_V3_ch3d: critical=0 major=1 minor=2 regression=0
