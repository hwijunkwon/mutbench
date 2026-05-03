# Audit v3 ch4e: lines 495--618

## 1. Per-paragraph audit table

| Lines | Claims | Source check | Citations | Cross-refs | Severity |
|---|---|---|---|---|---|
| 495--508 | Five-way omega robustness table; HCV-excluded omega2=0.246; Layer A heterogeneity caveat. | Table values match `omega_robustness_5way.csv`: standard cluster 0.2716 [0.2008,0.3455], wild 0.2685 [0.2005,0.3032], phylo-block 0.2719 [0.2022,0.3457], mixed 0.3398, Bayesian 0.3155 [0.2421,0.3882]. HCV-excluded 0.246 is referenced in `scripts/cluster_bootstrap_omega.py` as the body target but I did not find a clean CSV row naming this sensitivity result. Caveat wording is appropriate. | None in paragraph. | `tab:omega_robustness_5way` resolves. | Minor |
| 510--538 | LOO omega span, mean/median/s.d., leverage ordering, Cohen threshold, Kruskal-Wallis tests. | Verified against `cluster_bootstrap_omega_loo.csv` / `omega_loo_pathogen_sensitivity.csv`: span [0.2534,0.3126], mean 0.2933, median 0.2973, sample s.d. 0.0154; HCV largest +0.0426, Norovirus -0.0166, all others abs <=0.0106. Kruskal-Wallis recomputed from `stage3_full_results.csv`: pathogen H=1120.77 p=1.76e-234; family H=129.07 p=3.21e-21; scoring H=277.88 p=6.68e-48. | `cohen1988statistical` exists in `references.bib`. | `tab:omega_loo_pathogen_sensitivity` resolves. | Verified |
| 540--571 | Top-1 precision/recall/detection size/best MCC table; mean precision 0.338, recall 0.552; MERS failure interpretation. | Verified from per-pathogen maxima in `stage3_full_results.csv`: all table rows match rounded values. Mean precision=0.33823, recall=0.55167, mean MCC=0.34154. MERS top row has precision=0.045, recall=1.0, n_detected=200, n_gt=9; `pahd_r_data_processing_pathogen_summary.csv` supports MERS length 1330, so 200/1330=15.0%. | None. | `subsec:precision_at_k`, `tab:precision_at_k` resolve. | Verified |
| 573--578 | DMS validation: four threshold-sensitivity pathogens; DMS fitness correlations; 10/20/30% threshold effects; stable rankings in 15--25% range. | `dms_threshold_sensitivity_analysis.csv` covers 4 pathogens (SARS-CoV-2, H3N2, HIV-1, RSV). Best mean DMS F1 by threshold verifies 0.328 -> 0.377 -> 0.479. Best combo changes with threshold for H3N2/HIV-1/SARS-CoV-2; RSV changes from 10% to 20% and stays same at 30%, so "altered ... in all 4 pathogens" is true if comparing the sweep endpoints, not every adjacent step. I did not find a CSV provenance row for the DMS-fitness Spearman values 0.191/0.412/-0.363/-0.370 or their p-values. | None. | `subsec:dms_evolution_correlation`, `tab:dms_threshold_sensitivity`, and `subsec:3layer_gt` resolve. | Minor |
| 579--601 | Layer A vs C best scoring table and rank-correlation interpretation. | Verified from `layer_c_evaluation.csv`. Best rows: SARS-CoV-2 A tranception 0.211 / C plddt_inv 0.186; H3N2 A fubar_bf 0.534 / C semantic_change 0.245; HIV-1 A entropy 0.275 / C fubar 0.139; RSV A esm2_llr 0.196 / C EVEscape_composite 0.180; Rabies A stability 0.248 / C homoplasy 0.182; EV-A71 A semantic_change 0.260 / C plddt_inv 0.322. Per-scoring Spearman values match `stage3_statistics.csv`: RSV 0.8109 p=1.45e-5, H3N2 -0.5503 p=0.01194, SARS-CoV-2 -0.104, HIV-1 0.306, Rabies 0.325, EV-A71 0.214. | All DMS bibkeys exist: `dadonaite2024nature`, `lee2018h3n2dms`, `haddox2018hiv1dms`, `simonich2026rsvdms`, `aditham2025rabies`, `bakhache2025eva71`. | `tab:layer_a_vs_c`, `ch:mutbench` resolve. | Verified |
| 604--616 | Key-finding summary: omega interaction, unique best combinations, LOPO, Friedman, independence caveat. | Omega2=0.296 and CI [0.201,0.346] verified from `stage3_statistics.csv` / `omega_robustness_5way.csv`; Friedman chi2=7.68797 p=0.98954 verified; LOPO match=0/11, mean generalization MCC=0.0315, gap=0.2654 verified in `stage3_statistics.csv` (permutation p range is prose-sourced in lines 447--450, not a dedicated CSV found here). DISCREPANCY: "9 distinct scoring types" is stale; current `stage3_full_results.csv` best rows have 10 distinct scoring labels: entropy_with_indel, semantic_change, fubar_bf, freq, entropy, dnds_proxy, homoplasy, esm2_llr, stability, tranception. The 11 best scoring+detector tuples are unique. | `cohen1988statistical` cited earlier; no new citations. | `subsec:pahd_motivation_summary` resolves. | Major |
| 617--618 | Compatibility label only. | No factual claim. | None. | `subsec:pahd_prototype` resolves. | Verified |

## 2. Per-section severity counts

| Section | Critical | Major | Minor | Verified |
|---|---:|---:|---:|---:|
| Omega robustness / LOO, 495--538 | 0 | 0 | 1 | 1 |
| Precision@k, 540--571 | 0 | 0 | 0 | 1 |
| DMS validation, 573--601 | 0 | 0 | 1 | 1 |
| Summary, 604--618 | 0 | 1 | 0 | 1 |

## 3. Recent-fix verification

| Anchor | Status | Check |
|---|---|---|
| omega2 CIs: cluster [0.201,0.346], phylo-block [0.202,0.346], wild [0.201,0.303] | PRESENT | Lines 500--502 match `omega_robustness_5way.csv`; no old [0.195,0.333] in scope. |
| HIV-1 Layer A n=23 mapped; n=26 tags | NOT PRESENT | Not discussed in lines 495--618. Cross-scope spot check: Ch3 line 316 and Ch5 caption retain the 23/26 reconciliation; `layer_a_tags.csv` has 26 HIV-1 rows. |
| D614G retained in Layer A per Korber 2020 | NOT PRESENT | Not discussed in scope. Cross-scope spot check: Ch4 line 335 and `layer_a_tags.csv` retain D614G as functional; `korber2020tracking` exists. |
| Stage 1 functional regions 417 AA (=1251/3), not 439 | NOT PRESENT | Not discussed in scope. Cross-scope spot check: Ch3 line 396 uses 417 codons/AA. |
| Single-position scoring, gap-aware; not point substitutions only | NOT PRESENT | No relevant wording in scope; no "point substitutions only" phrase in lines 495--618. |
| P1 null at-or-below mean: 6/12 iid/circular, 4/12 block, 7/12 local-burden | NOT PRESENT | Outside scope, but Ch4 line 841 currently contains the fixed 6/12, 4/12, 7/12 values; recomputed from `codex_wave1/p1_null_per_pathogen.csv`. |
| Decision curve budget 50 random baseline 41 expected TPs | NOT PRESENT | Outside scope, but Ch4 line 837 currently says 41; verified from `codex_wave1/p2_decision_curve.csv`. |

Regressions in this scoped slice: 0.

## 4. Compression candidates

| Lines | Candidate reduction |
|---|---|
| 571 | Can cut about 35--45 words by merging the MERS failure explanation: "MERS is a failure case: recall=1.0 comes from flagging 200/1330 positions (15%), recovering all 9 positives by broad calling rather than signal." |
| 576--578 | Can cut about 25--35 words by moving individual rho values or threshold winner changes to a table note; retain direction-mixed correlations and F1 sweep means in text. |
| 600 | Strong candidate: the post-hoc rationalisation paragraph can be compressed by 90+ words. Keep the Spearman results, "not fully independent", and prior-definition caveat; move the hypothetical third-ground-truth argument to discussion. |
| 607--616 | Can cut about 30--45 words by combining bullets 3 and 4 into "two null-consistent failures-to-reject" and avoiding repeat of the non-independence caveat already stated before and after the list. |

## 5. Overall tally

Rows audited: 7. Verified=4, Minor=2, Major=1, Critical=0. Recent-fix regressions=0.

RESULT_AUDIT_V3_ch4e: critical=0 major=1 minor=2 regression=0
