# Audit v3 ch4g: lines 743-866

Scope: `paper/dissertation/chapters_en/ch4_results.tex` lines 743-866. Sources checked: requested MutBench CSV trees, `references.bib`, and chapter labels/refs.

## 1. Per-paragraph audit table

| Lines | Claims | Source check | Citations | Cross-refs | Severity |
|---|---|---|---|---|---|
| 743-758 | Audit ledger: P1/P2/P3/P5/P6/W4/W5/HBFWS/Cycle7B headline values. | Mostly matches downstream CSVs. Note P1 ledger says `5/12 iid sig`, which is correct for significance, while the recent at-or-below-mean anchor is `6/12` and is correctly stated at line 841. | No citations in scoped row text. | All `para:*` refs resolve in ch4. | Verified, with Minor wording risk |
| 760-793 | Baseline progression: top-1 0.0147; cumulative top-K values; full-10 0.0698; fixed 4-core 0.0809; oracle 0.0950; delta/CI claims. | `feature_ablation_nested_lopo.csv` means match all table values; `subset_selection_robustness_210combos.csv` gives core 0.0808818 and oracle 0.0949888. CI `[+0.008,+0.166]` matches `tab:nested_lopo_4core` in ch4. | No direct citation required; CSV paths given. | `alg:mutbench_coldstart`, `tab:cold_start_baseline_progression`, `tab:subset_selection_top10`, `tab:p5/w4/w5`, `tab:nested_lopo_4core` resolve. | Verified |
| 795-829 | 210-combination subset robustness: 13/210, top 6.2%, best subset, median/IQR, top-13 homoplasy, top-10 semantic_change 5/10. | `subset_selection_robustness_210combos.csv`: 210 rows; core rank 13, MCC 0.0808818; best `freq,entropy,homoplasy,semantic_change` 0.0949888; median 0.0524515; IQR `[0.0377165,0.0699841]`; homoplasy 13/13; semantic_change 5/10. | CSV path given; no bib citation needed. | `tab:subset_selection_top10`, `tab:nested_lopo_4core` resolve. | Verified |
| 831-833 | Full lattice and Shapley: 1023 subsets; 4-core rank 87; top 7-feature 0.0968; 3-core rank 27, 0.0866; Shapley values. | `p3_full_lattice_1023.csv` confirms 1023 rows, top subset 0.0968418, core rank 87, 3-core rank 27 and delta `+0.00576`; `p3_shapley.csv` confirms homoplasy/freq/entropy positive and pLDDT `-0.001501`, ESM2 `-0.014383`. | None in scope. | `tab:audit_ledger` resolves. | Verified |
| 835-837 | P2 rank reliability: aggregate deltas, Spearman means, CI-excluding pathogens, Rabies inversion, decision curve at budget 50, ECE. | `p2_method_summary.csv` confirms aggregate deltas and Spearman means. `p2_decision_curve.csv` confirms budget-50 sums: 4-core 66, 3-core 68, random 41. `p2_top_vs_bottom.csv` confirms Rabies inversion (`-0.123`, CI `[-0.245,-0.003]`, rho `-0.763`). However the “positive 4-core CI excluding zero” list is wrong: HIV-1 has CI `[0,0.109]` and does not exclude zero; the fifth CI-excluding fold is Rabies, but negative. Correct wording should be “4 positive CI-excluding folds plus Rabies inversion” or list only H3N2/Norovirus/Dengue/Influenza_B as positive. | None in scope. | `alg:mutbench_coldstart`, `tab:audit_ledger` resolve. | Major |
| 839-841 | P1 null calibration: 100k permutations; Stouffer `p=1.00`; at-or-below counts `6/12`, `6/12`, `4/12`, `7/12`; sig counts `5/12`, `3/12`, `2/12`, `1/12`; pathogen p-values. | `p1_null_per_pathogen.csv` and `p1_null_summary.csv` confirm all counts and named p-values. This is the recent-fix anchor and is present. | None in scope. | `alg:mutbench_coldstart`, `tab:audit_ledger` resolve. | Verified |
| 843-845 | P5 callability: defaults 0/12; D1 max quorum 5/11, threshold 7/11; 32-config sweep; only `(5/11,1.05)` calls and P1-negative; D3 pLDDT penalty. | `p5_callable_decisions.csv`, `p5_endpoint_summary.csv`, and `p5_threshold_sensitivity_sweep.csv` confirm 0/12 callable and sweep behavior. Mismatch: line 845 says D3 pass count `3/12` vs `11/12`; P5 CSV gives 4-core D3 `2/12` and 3-core `11/12`. Conclusion unaffected. | None in scope. | `para:null_calibration`, `alg:mutbench_coldstart`, `tab:audit_ledger` resolve. | Minor |
| 847-849 | P6 biological nulls: four nulls, 100k perms, all valid 12/12, 4-core sig counts 5/5/4/4, 3-core 5/3/4/3, Norovirus all four, Stouffer cancellation, 27/96 and 29/96 cells. | `p6_null_per_pathogen.csv`, `p6_null_summary.csv`, and `p6_p1_p6_robustness.csv` confirm null definitions, valid counts, significance counts, and robustness cell totals. | None in scope. | `tab:audit_ledger` resolves. | Verified |
| 851-853 | W4 Tier 2: 0/3 harmonization pass; 2-core fallback; mean 0.077, sd 0.136, 8/12 positive, p=0.368, D1 0/12; 1/28 stable; union quorum 16; sign agreements 81.6/94.4; 16/16 envelope-compatible. | `w4_feature_schema_audit.csv`, `w4_labeled_lopo_summary.csv`, `w4_labeled_callability_recheck.csv`, `w4_expanded_stability_per_target.csv`, and `w4_expanded_quorum_reachability.csv` confirm all. | None in scope. | `tab:audit_ledger` resolves. | Verified |
| 855-857 | W5 Layer A prime: 10/16 Class A, prevalence 2.0%-14.5%, mean -0.055, sd 0.068, median -0.057, 2/10 positive, precision@20 0.005, sign negative and stable, Welch p=0.0089, residues 98-111. | `codex_layerA_prime/per_target.csv`, `lopo_summary.csv`, `sign_bootstrap.csv`, and `cross_panel_comparison.csv` confirm the numeric claims. The “residues 98-111” independence statement is not directly evidenced in the opened summary CSVs but is consistent with the W5 narrative. | `references.bib` appears to lack a UniProt citation; consider adding if UniProtKB is named in prose. | `tab:audit_ledger` resolves. | Verified, Minor citation gap |
| 859-861 | HBFWS: 12-pathogen LOPO, prior range, mean 0.058 vs 0.078, delta -0.020, Wilcoxon p=0.78, family deltas, three zero deltas, n=11 phrasing. | `hbfws_lopo_results.csv` confirms 12 held-out folds, means 0.0583 and 0.0779, delta -0.0196, paired/singleton deltas `-0.014/-0.027`, three zero deltas, 5 singleton folds among 8 families. “Rejected at n=11” is interpretable as 11 training pathogens per fold; clarify if meant as total held-out panel size. | None in scope. | `tab:audit_ledger` resolves. | Verified, Minor wording risk |
| 863-866 | Cycle 7B opening claim: six paradigms against EqualWeight-4core; table retained after scope. | `adaptive_weighting_comparison.csv` and lines 866-890 confirm six methods; computed one-sided Wilcoxon p-values match later table, smallest `0.5608`. | None in scope. | `tab:adaptive_weighting_comparison` resolves. | Verified |

## 2. Per-section severity counts

| Section | Critical | Major | Minor | Verified |
|---|---:|---:|---:|---:|
| Audit ledger | 0 | 0 | 1 | 1 |
| Cold-start baseline progression | 0 | 0 | 0 | 1 |
| Subset selection robustness | 0 | 0 | 0 | 1 |
| Full-lattice + Shapley | 0 | 0 | 0 | 1 |
| Rank reliability / decision curve | 0 | 1 | 0 | 0 |
| P1 null calibration | 0 | 0 | 0 | 1 |
| P5 callability | 0 | 0 | 1 | 0 |
| P6 biological nulls | 0 | 0 | 0 | 1 |
| W4 Tier 2 | 0 | 0 | 0 | 1 |
| W5 Layer A prime | 0 | 0 | 1 | 1 |
| HBFWS | 0 | 0 | 1 | 1 |
| Cycle 7B opening | 0 | 0 | 0 | 1 |

## 3. Recent-fix verification

| Anchor | Status | Evidence |
|---|---|---|
| Omega CIs `[0.201,0.346]`, phylo `[0.202,0.346]`, wild `[0.201,0.303]` | PRESENT | ch4 line 490; CSV summaries support. |
| HIV-1 Layer A `n=23` mapped gp120; `n=26` tags | PRESENT | ch4 line 261 and line 902 captions. |
| D614G retained per Korber 2020 | PRESENT | ch4 lines 219 and 335; `korber2020tracking` exists in `references.bib`. |
| Stage 1 functional regions `417 AA = 1251 nt / 3`, not 439 | PRESENT | ch4 line 25 uses 1,251 nucleotide positions; no scoped regression to 439 found. |
| Single-position scoring gap-aware, not point substitutions only | NOT PRESENT IN SCOPE | No conflicting scoped wording found. |
| P1 at-or-below-mean `6/12`, `4/12`, `7/12` | PRESENT | ch4 line 841; CSV confirms iid/circular 6, protein-block 4, local-burden 7. |
| Budget-50 random baseline `41` TPs | PRESENT | ch4 line 837; CSV confirms random sum 41. |

Regressions: 0.

## 4. Compression candidates

| Lines | Candidate | Reduction |
|---|---|---:|
| 762 | Split long paragraph and remove repeated “without consulting held-out labels” / deployability refs already in surrounding section. | 35-55 words |
| 797 | Compress repeated “near-optimal but not literally best” and duplicate `+0.0141`/CI language also in table footnote. | 45-70 words |
| 827 | Footnote repeats claims from lines 797 and table rows; keep only source/semantic-change note. | 20-30 words |
| 853 | W4 paragraph can move detailed branch language to ledger and keep only result chain. | 25-40 words |
| 857 | W5 paragraph can omit either prevalence range or Branch C sentence from main text if table remains. | 20-35 words |

## 5. Overall tally

Critical: 0. Major: 1. Minor: 4. Verified rows: 11. Recent-fix regressions: 0.

RESULT_AUDIT_V3_ch4g: critical=0 major=1 minor=4 regression=0
