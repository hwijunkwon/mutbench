# Audit v3 ch4a: `ch4_results.tex` lines 1--123

## 1. Per-paragraph audit table

| Lines | Claim(s) audited | Source check | Citations | Cross-refs | Severity |
|---|---|---|---|---|---|
| 1--3 | Chapter title and `ch:results` label. | Structural only. | n/a | Label unique/resolves. | Verified |
| 5--8 | Stage 1 is SARS-CoV-2; Stage 2 covers 11 RNA viruses, 20 scoring formulas x 14 detection families, 5 categories, 39 parameter variants. | `stage3_full_results.csv`: 8,580 rows = 20 scoring x 39 detectors x 11 pathogens; 14 families. Ch3 detection table has 5 detection categories; scoring table has 6 scoring categories. | n/a | `sec:variant_comparison`, `sec:phylo_simulation`, `sec:9pathogen_results` resolve. | Verified, with wording caution: "5 categories" must mean detection categories, not scoring categories. |
| 9--14 | Key results: scoring x pathogen largest modeled component, omega^2=0.296; all 11 unique best combos; LOPO 0/11; vaccine escape HIV-1 7.19x p_adj 2.5e-16, H3N2 9.36x, SARS-CoV-2 exploratory; Bonferroni-survivor means H3N2 ~4.7x, HIV-1 ~4--5x. | `stage3_statistics.csv` verifies omega^2=0.2962519839 and largest modeled component. `stage3_full_results.csv` verifies 11-pathogen grid. `stage3_statistics.csv` verifies LOPO match_rate=0. `vaccine_escape_stage3.csv` verifies H3N2 9.3621, HIV-1 `freq + Wavelet(t=1.5)` 7.1875, p_adj=2.47e-16, and SARS-CoV-2 exploratory after Bonferroni. H3N2 all Bonferroni-survivor mean=4.675. HIV-1 all Bonferroni-survivor mean is 2.35, and HIV-1 freq-only survivor mean is 2.73; I could not reproduce "HIV-1 ~4--5x" from the scoped CSVs. | n/a in box; table ref resolves. | `tab:vaccine_escape_stage3` resolves. | Major for HIV-1 survivor-mean derivation; otherwise verified. |
| 17--23 | Section/subsection labels for single-pathogen benchmark and variant comparison. | Structural only. | n/a | Labels unique/resolved. | Verified |
| 25 | Synthetic SARS-CoV-2-like genome 29,903 positions, 1,251 functional nt; five MutClust variants and three baselines; Hybrid F1=0.785, HS=0.778, ~43x over 0.018 random; MutClust F1 0.67--0.78, precision >0.96; HDBSCAN recall 0.944, precision 0.079; real GISAID F1=0.123. | `method_comparison.csv` verifies Hybrid precision 0.9683, recall 0.6595, F1 0.7846, HS 0.7778; v1/v2a/v2b F1 0.668--0.669 and precision 0.988--0.991; HDBSCAN precision 0.0792, recall 0.9440; frequency/sliding rows. 29,903 and 1,251 align with SARS-CoV-2 genome and Ch3 functional-region definition. Minor taxonomy issue: Ch3 defines five Stage-1 variants as including pure HDBSCAN/v3 and two baselines; this sentence calls HDBSCAN-Auto a third baseline, inconsistent with line 6 and Ch3. Random baseline 0.018 and real-GISAID F1=0.123 are present in Ch4/prior audit trail but not in an obvious source CSV. | n/a | `tab:hotspot_scores`, `sec:real_gisaid_benchmark` resolve. | Minor |
| 27--43 | Table headline synthetic metrics. | `method_comparison.csv` verifies all displayed rows to rounding; table omits HDBSCAN hotspot-score nuance but values match. | n/a | `tab:hotspot_scores` unique. | Verified |
| 45--53 | Three ground truths: functional regions 417 AA/32.8%/1,251 nt; DMS 252/19.8%; convergent 97/7.6%; Jaccard DMS vs convergent =0.006; best method differs by ground truth. | `multi_ground_truth_summary.csv` verifies best methods/F1/enrichment. 417 AA = 1,251/3 and 32.8% of 1,273 aa Spike. Ch3 ground-truth table supports domain list. Jaccard 0.006 is cited in Ch5 and prior audit trail but not present in `multi_ground_truth_summary.csv`; source path should be explicit. | `dadonaite2023dms`, `cao2023ba286`, `carabelli2023convergent` exist in `references.bib`. | `tab:multi_gt` resolves. | Minor source-path gap for Jaccard. |
| 54--74 | Multi-ground-truth table: TC-freq-v2 0.474 for functional 417; Saturated H-score 0.315; CH-score 0.188/1.70; strict TC-freq-v3 0.108/3.43. | `multi_ground_truth_summary.csv` verifies all displayed values to rounding. Recent 439->417 fix is intact in table. | n/a | `tab:multi_gt` unique. | Verified |
| 76 | No single method dominates; single-GT frameworks risk bias. | Supported by differing best methods in `multi_ground_truth_summary.csv`. | n/a | n/a | Verified |
| 78--83 | Real GISAID benchmark using 2020--2021 H-score data; 342/29,903 positions nonzero (1.14%). | Numerically internally consistent: 342/29,903=1.14%. Values are in Ch4 table and prior audit trail, but I did not locate an authoritative CSV row under `results/mutbench`. | `youn2025mutclust` exists. | `tab:real_gisaid` resolves. | Minor source-path gap |
| 85--110 | Real-GISAID table rows: MutClust variants, HDBSCAN failure, frequency/sliding; sliding F1=0.420. | Values are internally consistent and match prior audit record; explicit CSV source was not located in scoped result files. | n/a | `tab:real_gisaid` unique. | Minor |
| 112 | Synthetic-to-real drop; sliding highest F1; enrichment 6.9--8.0x; OPTICS/KDE external sweeps 30/36; external methods below Hybrid HS=0.778. | Hybrid synthetic values verified in `method_comparison.csv`; real table values same source-path gap as above. OPTICS/KDE values and sweep counts are not present in located CSVs. | n/a | `tab:external_methods`, `sec:external_comparison` defined inline and resolve. | Minor |
| 114 | Stage 1 summary: Hybrid best synthetic HS=0.778/~43x; loses on real GISAID HS=0.383 vs Fixed 0.386; enrichment 6.9--8.0x; Stage 2 follows. | Synthetic verified; real-GISAID values have explicit-source gap but match table. | n/a | `sec:9pathogen_results` resolves. | Minor |
| 116--123 | Robustness section labels and transition sentence. | Structural only. Multiple labels on one section are intentional aliases and resolve. | n/a | Labels unique/resolved. | Verified |

## 2. Per-section severity counts

| Section | Critical | Major | Minor | Verified |
|---|---:|---:|---:|---:|
| Chapter opening / key-results box (1--14) | 0 | 1 | 0 | 2 |
| SARS-CoV-2 synthetic benchmark (17--43) | 0 | 0 | 1 | 2 |
| Multi-ground-truth evaluation (45--76) | 0 | 0 | 1 | 2 |
| Real GISAID benchmark / Stage 1 close (78--114) | 0 | 0 | 4 | 0 |
| Robustness section lead-in (116--123) | 0 | 0 | 0 | 1 |

## 3. Recent-fix verification

| Anchor | Status | Evidence |
|---|---|---|
| omega^2 CI `[0.201, 0.346]`; phylo-block `[0.202, 0.346]`; wild `[0.201, 0.303]` | PRESENT outside scope; no scoped regression | Ch4 line 126 has `[0.201,0.346]`; `omega_robustness_4way.csv` has 0.2008/0.3455, 0.2022/0.3457, 0.2005/0.3032. |
| HIV-1 Layer A: n=23 gp120 MCC; n=26 tags | PRESENT outside scope; no scoped regression | `region_overlap_mcc.csv` HIV gt_size=23; `layer_a_tags.csv` has 26 HIV-1 rows. |
| D614G retained in Layer A per Korber 2020 | PRESENT outside scope; no scoped regression | `layer_a_tags.csv` has SARS-CoV-2 position 614 functional, Korber 2020. |
| Stage 1 functional regions: 417 AA, not 439 | PRESENT | Lines 50 and 63 use 417; no 439 in scope. |
| Single-position scoring gap-aware, not "point substitutions only" | NOT PRESENT in scope; no regression | No bad wording in lines 1--123; Ch3 uses single-position/gap-aware-compatible wording. |
| P1 null at-or-below-mean 6/12 iid/circular, 4/12 protein-block, 7/12 local-burden | PRESENT outside scope; no scoped regression | `codex_wave1/p1_null_per_pathogen.csv` reproduces 6/6/4/7 for 4-core MCC. |
| Decision curve budget-50 random baseline 41 TPs | PRESENT outside scope; no scoped regression | `codex_wave1/p2_decision_curve.csv` random budget-50 sums to 41. |

## 4. Compression candidates

| Lines | Candidate | Estimated reduction |
|---|---|---:|
| 25 | Move comparator ranges into Table 1 and keep only Hybrid headline plus real-GISAID boundary. | 45--60 words |
| 49--52 | Combine ground-truth definitions and non-overlap sentence; table already carries best-method evidence. | 20--30 words |
| 112--114 | Merge real-GISAID/external-method paragraph with Stage 1 summary; keep OPTICS/KDE as parenthetical. | 35--55 words |

## 5. Overall tally

Critical 0; Major 1; Minor 6; Verified 9; Regression 0.

RESULT_AUDIT_V3_ch4a: critical=0 major=1 minor=6 regression=0
