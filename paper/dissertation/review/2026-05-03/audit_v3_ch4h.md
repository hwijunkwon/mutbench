# Audit v3 ch4h: lines 867-989

Scope: `paper/dissertation/chapters_en/ch4_results.tex` lines 867-989. Sources checked: requested `results/mutbench/**/*.csv`, wave directories, `codex_layerA_prime`, `feature_analysis`, `references.bib`, and cross-chapter `\label{}` / `\ref{}` targets.

## 1. Per-paragraph audit table

| Lines | Claims | Source check | Citations | Cross-refs | Severity |
|---|---|---|---|---|---|
| 867-888 | Cycle 7B adaptive-weighting table: EqualWeight-4core baseline 0.078; six new methods fail; Wilcoxon one-sided p-values. | Values verified from `adaptive_weighting_comparison.csv`; Wilcoxon recomputation matches: EQ10 p=0.288, XGB 0.966, RF 0.909, LR 0.703, AlgSel 0.689, HBFWS-phylo 0.837, RankAgg 0.561. CSV has 12 folds. | none needed | `tab:nested_lopo_4core` exists; local label exists. | Verified |
| 890 | Seven adaptive failures at `n=11`; smallest p=0.56; deltas; LOPO 0/11, Friedman p=0.990, oracle gap 0.265; EV-A71 held-out MCC 0.146 vs 0.013. | Deltas/p-values and EV-A71 row verified. But CSV has 12 folds (core 11 + Zika), not `n=11`. Also "single positive EV-A71 fold" is inaccurate if read as only AlgSel improvement: AlgSel exceeds baseline in 5/12 folds (Norovirus, HIV-1, RSV, MERS, EV-A71). | none | `tab:audit_ledger` exists. | Major |
| 896-898 | Layer A definitions may differ; tags analyzed across 12-pathogen feature-analysis scope. | `gt_heterogeneity_analysis.csv` has 12 pathogens; `layer_a_tags.csv` supports biological tag types. | none | `subsec:feature_ablation`, `tab:gt_heterogeneity` exist. | Verified |
| 900-925 | Ground-truth heterogeneity table, including HIV-1 `n_A=26` tag count and `n=23` mapped Stage 2 positions. | All rows match `gt_heterogeneity_analysis.csv` after rounding. `layer_a_tags.csv` has 26 HIV-1 rows; `feature_matrix_HIV-1.csv` has 23 `layer_a=1` rows. | none | `tab:gt_positions`, `sec:limitations` exist. | Verified |
| 927-928 | Immune_escape >=71%; 5 best features; 10/12 consistent; argues against composition as sole explanation for omega2=0.296. | Verified: min immune 70.83% Dengue; best features are esm2_llr, plddt, homoplasy, entropy, dnds_proxy; 10 `True`; omega2=0.296 in `cluster_bootstrap_omega_summary.csv` and Stage 3 text. | none | `ch:discussion` exists. | Verified |
| 934 | Most informative feature differs by pathogen; evaluates search-space reduction with all 10 features. | Supported by heterogeneity table and feature-ablation outputs. | none | none | Verified |
| 936 | EqualWeight production vs nested-LOPO protocols; production 0.083, nested 0.070; difference <=0.013; adaptive weighting noisy. | Production 0.08288 from `feature_ablation_results.csv`; nested full-10 0.06975 from `feature_ablation_nested_lopo_summary.csv`; difference 0.01313, which rounds to 0.013. Method description is consistent with Ch3 equal-weight variants. | none | `subsec:feature_ablation`, `tab:nested_lopo_4core` exist. | Verified |
| 938-939 | 12-pathogen LOPO set; EqualWeight top-10% mean 0.083, FreqThresh 0.075, random ~0; core 11 baseline 0.093; 9/11 positive EqualWeight and 8/11 FreqThresh. | EqualWeight 0.08288/9 positives over 12 and core 0.09251/9 positives verified from `feature_ablation_results.csv`. Random ~0 is plausible from random baselines. FreqThresh 0.075 was not directly recoverable from the checked ablation CSVs (`Frequency-only` group is 0.069; Stage3 `freq+FreqThresh(p=90)` is 0.095). | none | `subsec:feature_ablation` exists. | Minor |
| 941-946 | Vaccine escape validation: 20x39x3 = 2340; H3N2 29, SARS-CoV-2 30, HIV-1 45; Fisher formula; remaining 8 unavailable. | `vaccine_escape_stage3.csv` has 780 rows/pathogen and denominators 29/30/45. Formula matches columns. | none | `tab:vaccine_escape_stage3` exists. | Verified |
| 948-974 | Vaccine escape table/footnote: top single-scoring rows, EqualWeight fixed top-5 rows, Bonferroni details, Layer A overlap. | Single-scoring rows verified in `vaccine_escape_stage3.csv`: H3N2 9.3621, HIV-1 7.1875, SARS-CoV-2 7.6303. HIV-1 EqualWeight 4.1667 p=0.003734 verified. H3N2 EqualWeight top-5 verified in `escape_validation_adapt.csv`. Problem: SARS-CoV-2 fixed top-5 row cites `escape_validation_adapt.csv`, where `n_escape=15`, overlap `2/15`, enrichment 2.665; text/table report `2/30`. | none | table label exists. | Major |
| 976-977 | HIV-1 is load-bearing external anchor; all three nominally significant; H3N2/HIV-1 survive Bonferroni; SARS-CoV-2 exploratory; HIV-1 Layer A entropy/Wavelet MCC 0.275; freq correlation rho~0.97. | Main significance claims verified for the three displayed rows. Caution: `vaccine_escape_stage3.csv` contains stronger Bonferroni-surviving SARS-CoV-2 rows for other scorers; claim is true only for the displayed "top scoring type per pathogen" framing, not global best p-value. Correlation rho=0.97 matches information-analysis text. | none | `sec:information_analysis` exists. | Minor |
| 979 | H3N2 self-consistency: 9/29, 8 already Layer A, novel-only p=0.132; EqualWeight top-5 captures 137,155,159,160,186,188; FreqThresh misses 160/186. | EqualWeight/FreqThresh top-5 sites verified in `escape_validation_adapt.csv`; 9/29 from `vaccine_escape_stage3.csv`. Novel-only details not present in the checked CSVs but consistent with footnote framing. | none | none | Verified |
| 981 | Vaccine escape feasible for 3/11; remaining 8 excluded in four categories. | Consistent with `vaccine_escape_stage3.csv` pathogen coverage. Exclusion rationales are narrative/curation claims; no contradictory CSV found. | none | local `tab:escape_availability` label exists. | Verified |
| 983-984 | Layer A/escape circularity; H3N2/SARS-CoV-2 self-consistency; HIV-1 least circular. | Supported by Layer A overlap footnote and `layer_a_tags.csv` immune_escape tags. | none | `ch:mutbench`, `tab:vaccine_escape_stage3` exist. | Verified |
| 986-987 | Typical 500-aa protein narrows to 10-50 positions with 7-9x enrichment. | Detector counts in vaccine table span 11-32 for top rows and top-percentile protocols imply 15-50 for 500 aa. Enrichment 7-9x applies to single-scoring anchors, not EqualWeight rows; wording is acceptable but broad. | none | none | Verified |

## 2. Per-section severity counts

| Section | Critical | Major | Minor | Verified |
|---|---:|---:|---:|---:|
| Cycle 7B adaptive weighting | 0 | 1 | 0 | 1 |
| Ground truth heterogeneity | 0 | 0 | 0 | 3 |
| Practical validation/search-space reduction | 0 | 1 | 2 | 8 |

## 3. Recent-fix verification

| Anchor | Status | Check |
|---|---|---|
| omega2 CI `[0.201,0.346]`; phylogenetic-block `[0.202,0.346]`; wild-cluster `[0.201,0.303]` | PRESENT | Lines 490 and Ch3 methods lines 809-810 match summaries: cluster 0.2008-0.3455, block 0.2022-0.3457, wild 0.2005-0.3032. |
| HIV-1 Layer A `n=23` mapped; `n=26` tags | PRESENT | Line 902; CSV counts verified. |
| D614G retained in Layer A per Korber 2020 | PRESENT | Lines 219/335; `layer_a_tags.csv` has SARS-CoV-2 position 614 functional, Korber 2020; `references.bib` has `korber2020tracking`. |
| Stage 1 functional regions `417 AA` (=1251 nt/3), not 439 | PRESENT | Lines 50/63 and Ch3 methods line 396. |
| Single-position scoring, gap-aware, not point substitutions only | PRESENT | Ch3 methods line 37 states single-position regime; no scoped regression found. |
| P1 at-or-below-mean `6/12` iid/circular; `4/12` protein-block; `7/12` local-burden | PRESENT | Line 841; recomputed from `p1_null_per_pathogen.csv`. |
| Decision curve budget 50 random baseline `41` expected TPs | PRESENT | Line 837; `p2_decision_curve.csv` random budget-50 sum = 41. |

## 4. Compression candidates

| Lines | Candidate reduction |
|---|---|
| 936 | Compress protocol paragraph by ~55 words by moving script/protocol implementation details to Methods and keeping only production vs nested distinction plus MCC agreement. |
| 972 | Footnote can drop redundant "unrounded" parentheticals and pipeline prose; estimated reduction ~35 words. |
| 981 | Four exclusion categories can be shortened to category labels plus examples; estimated reduction ~30 words. |
| 986-987 | Remove the second sentence or fold it into the first; estimated reduction ~18 words. |

## 5. Overall tally

Critical: 0; Major: 2; Minor: 2; Verified rows: 12; Regressions against recent-fix anchors: 0.

RESULT_AUDIT_V3_ch4h: critical=0 major=2 minor=2 regression=0
