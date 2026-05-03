# Audit v3 - ch3_methods.tex lines 255-381

Scope: `paper/dissertation/chapters_en/ch3_methods.tex` lines 255-381. Sources checked: `results/mutbench/**/*.csv`, wave/codex CSVs, `feature_analysis`, `codex_layerA_prime`, `references.bib`, and chapter labels/refs.

## 1. Per-Paragraph Audit Table

| Lines | Claims | Source check | Citations | Cross-refs | Severity |
|---|---|---|---|---|---|
| 255-267 | Six DMS sources, phenotype/cell line, 2 replicate columns, mean absolute effect, top-20%, 4/6 threshold sweep; DMS provenance archived. | `provenance/dms_sources.csv` confirms 3+ published and 2 pipeline replicates for SARS-CoV-2/H3N2/HIV-1 and 2 pipeline replicates for all six. `layer_c_evaluation.csv` confirms six DMS pathogens and current mapped Layer C counts. `dms_threshold_sensitivity_analysis.csv` covers only SARS-CoV-2, H3N2, HIV-1, RSV. | Cites are present in `references.bib`: Dadonaite, Lee, Haddox, Simonich, Aditham, Bakhache. | `subsec:dms_evolution_correlation` exists in Ch4. | Verified |
| 271-275 | RSV Layer A/B overlap at 148/152; Influenza B overlap at 141/194; MCC prioritizes A and effective B counts become 16 and 8. | `tools/mutbench/ground_truth/multilayer_gt.py` gives RSV Layer A 20, B 18, overlap [148,152], effective B 16; Influenza_B Layer A 17, B 10, overlap [141,194], effective B 8. | Relevant source cites present: Mas/Sullender, Ni/Wang. | No unresolved refs. | Verified |
| 277-282 | Layer A/C conflict is not merged; MCC uses Layer A; DMS F1 uses Layer C top-20%; disagreement is reported separately. | `layer_c_evaluation.csv` has separate `mcc_layer_a`, `mcc_layer_c`, `f1_layer_a`, `f1_layer_c`, `n_gt_a`, `n_gt_c`; confirms operational separation. | No new cites needed. | `subsec:dms_evolution_correlation` and `tab:layer_a_vs_c` exist in Ch4. | Verified |
| 284-318 | 3-layer count table for 11 pathogens; HCV Layer B caveat; HIV-1 23 mapped vs 26 curation tags. | Layer A counts match feature matrices for all 11. `layer_c_evaluation.csv` confirms current Layer C counts: SARS-CoV-2 247, H3N2 112, HIV-1 48, RSV 101, Rabies 87, EV-A71 55. `layer_a_tags.csv` confirms HIV-1 has 26 tags and SARS-CoV-2 includes position 614. Layer B counts match `pahd_r_coordinate_provenance_layers.csv` except HCV: table/footnote says effective B=0, but provenance still records `layer_b_count=14`. This is a stale-source inconsistency that should be reconciled or explained as superseded. | All table citation keys are present in `references.bib`; HCV HVR row has no BibTeX cite but is intentionally textual. | `tab:gt_positions`, `ch:results`, `ch:discussion` labels exist. | Major |
| 320-325 | Six pathogens have all layers; five lack DMS but are included because MCC uses Layer A and panel size/diversity matter. | Table and `layer_c_evaluation.csv` confirm exactly six DMS pathogens; non-DMS set matches. `stage3_full_results.csv` contains the 11-pathogen MCC panel. | No new cites needed. | `ch:results` exists. | Verified |
| 329-335 | Figure shows Layer A/B distribution across 11 pathogens; lengths 261-1330 AA; `C` marks DMS availability. | Figure file exists at `paper/dissertation/figures/gt_distribution_11pathogens.png`. Lengths match feature matrices: EV-A71 261, MERS 1330. | No cite needed. | `fig:gt_distribution` label exists. | Verified |
| 338-348 | Stage 1 focuses on SARS-CoV-2 and has three purposes; ground truth generated from three sources. | Consistent with surrounding methods and Stage 1 result section. No numerical claim beyond stage structure. | No issue. | `subsec:stage1`, `subsec:stage1_gt` labels exist. | Verified |
| 350-359 | Dadonaite full-length Spike DMS; pseudovirus entry; top 20% mean absolute fitness effect; codon-aware nucleotide transform; Spike start `21,563`; independence from detection p-values. | `dms_data/sars2_dms.csv` has 1,234 positions and `layer_c_sum=247`, matching current mapped top-20% count. `provenance/dms_sources.csv` confirms Dadonaite full-length entry assay. Formula is correct for 1-based AA to nucleotide mapping; Spike start is standard Wuhan-Hu-1 coordinate. | Dadonaite keys present. | `subsec:dms_ground_truth`, `eq:coordinate_transform` labels exist. | Verified |
| 361-367 | Synthetic H-scores: seed positions 484/501/417/452, score ranges, 50-position neighborhoods, background noise, 29,903 genome positions, validation caveat. | Score ranges and genome length are internally consistent. The phrase "four Spike positions most frequently mutated in major variants" is not directly supported by the audited CSVs and is questionable because D614G is also retained as a major functional/frequency site elsewhere. Safer wording: canonical VOC/immune-escape seed positions. | No direct cite on seed-frequency claim in this paragraph. | `subsec:dms_ground_truth`, `sec:multi_gt` labels exist. | Minor |
| 369-381 | Annotated functional regions based on Wrapp/McCallum; RBD 319-541 gives 669 nt. | `references.bib` contains both citations. RBD nucleotide count is arithmetically correct: `(541-319+1)*3=669`. Later table lines 381-396 (outside scope but checked) total to 1,251 nt = 417 AA after one 3-nt overlap. | Wrapp and McCallum keys present. | `tab:ground_truth` label exists. | Verified |

## 2. Per-Section Severity Counts

| Section | Critical | Major | Minor | Verified |
|---|---:|---:|---:|---:|
| DMS preprocessing table tail | 0 | 0 | 0 | 1 |
| Layer overlap/conflict handling | 0 | 0 | 0 | 2 |
| 3-layer count table and notes | 0 | 1 | 0 | 2 |
| Ground-truth distribution figure | 0 | 0 | 0 | 1 |
| Stage 1 ground-truth generation | 0 | 0 | 1 | 2 |

## 3. Recent-Fix Verification

| Anchor | Status | Check |
|---|---|---|
| omega^2 CI cluster `[0.201, 0.346]`, phylogenetic-block `[0.202, 0.346]`, wild-cluster `[0.201, 0.303]` | PRESENT | Ch4 lines and CSVs confirm: cluster `0.2008-0.3455`, block `0.2022-0.3457`, wild `0.2005-0.3032`. |
| HIV-1 Layer A: `n=23` mapped to gp120; `n=26` in `layer_a_tags.csv` | PRESENT | Lines 299/316 and CSVs confirm 23 mapped, 26 tags. |
| D614G retained in Layer A per Korber 2020 | PRESENT | `layer_a_tags.csv` includes SARS-CoV-2 position 614; Ch4 states retained per `korber2020tracking`; BibTeX key exists. |
| Stage 1 functional regions: `417 AA` = 1251 nt / 3, not 439 | PRESENT | Lines 381-396 confirm 1,251 nt and 417 codons/AA. |
| Single-position scoring, gap-aware, not "point substitutions only" | PRESENT | Ch3 earlier states single-position coding-region regime; no scoped regression to "point substitutions only" found. |
| P1 null at-or-below-mean: 6/12 iid/circular; 4/12 protein-block; 7/12 local-burden | PRESENT | `codex_wave1/p1_null_per_pathogen.csv` confirms for 4-core MCC. |
| Decision curve budget 50 random baseline: 41 expected TPs | PRESENT | `codex_wave1/p2_decision_curve.csv` random, budget 50 sums to 41. |

## 4. Compression Candidates

| Lines | Candidate reduction |
|---|---|
| 277-282 | Compress Layer A/C conflict handling by about 55-75 words: keep the three metric-routing bullets and remove the final restatement beginning "Thus a position..." because it repeats the same operational rule. |
| 314-316 | Compress HCV and HIV notes by about 35-45 words by moving "scoring x pathogen interaction..." to one clause and avoiding repeated "benchmark feature matrix" phrasing. |
| 320-325 | Compress inclusion rationale by about 25-35 words by merging points (1) and (2): MCC only needs Layer A, while Layer C is supplementary and six pathogens are underpowered for ANOVA/Friedman/LOPO. |
| 361-367 | Compress synthetic benchmark caveat by about 30-45 words by combining the "known by design" and "does not directly measure biological performance" sentences. |

## 5. Overall Tally

Critical: 0; Major: 1; Minor: 1; Verified rows: 11; regressions against recent-fix anchors: 0.

RESULT_AUDIT_V3_ch3c: critical=0 major=1 minor=1 regression=0
