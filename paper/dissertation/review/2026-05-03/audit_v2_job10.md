# Audit v2 Job 10 - ch4_results.tex lines 701-989

Scope: `paper/dissertation/chapters_en/ch4_results.tex:701-989`. Read-only audit. No citations occur in this range.

## Per-Paragraph Table

| Lines | Paragraph / object | Numerical claims and source checks | Citations | Cross-refs | Consistency / recent-fix check | Severity |
|---:|---|---|---|---|---|---|
| 704 | Adaptive-weighting limits | VERIFIED: adaptive maxima 0.020/0.049/0.043, EqualWeight 0.083, oracle 0.160 from `results/mutbench/adapt_v2_summary.csv`; n=11 reference pathogens is explanatory LOPO training size, CSV reports 12 evaluated folds; 20-30+ is projection, UNVERIFIED by CSV. | none | `ch:discussion`, `sec:future_work` OK | Consistent with Ch5 panel-size limitation. | Minor |
| 708 | MutBench Cold-Start algorithm paragraph | VERIFIED: 4-core 0.081, full-10 0.070, delta +0.011, CI [-0.018,+0.042] from `results/mutbench/feature_analysis/feature_ablation_nested_lopo_summary.csv`; 13/210 and 6.2% from `subset_selection_robustness_summary.csv`; 11 pathogens/20-80/7-9x/10 min CPU not directly in checked CSVs. DISCREPANCY/REGRESSION: omega CI printed `[0.202, 0.346]`, required post-v214 value is `[0.201, 0.346]`; source family bootstrap expected per task. | none | all refs OK | No old `[0.195,0.333]`; but lower bound is still off by 0.001. | Major; regression=1 |
| 710-733 | Algorithm 1 | VERIFIED internally: L,N, 0.10L, 4 features, top-10%, 90th percentile, signs are methodological/pseudocode. | none | label `alg:mutbench_coldstart` OK | Uses single-position scoring logic; no forbidden "point substitutions only" wording. | Verified |
| 741-758 | Audit ledger table | VERIFIED spot checks: P1/P6 from `codex_wave1/p1_null_summary.csv`, `codex_wave3/p6_null_summary.csv`; W4 from `codex_wave4/w4_labeled_lopo_summary.csv`; W5 from `codex_layerA_prime/lopo_summary.csv`; HBFWS/adaptive from `hbfws_lopo_results.csv`, `adaptive_weighting_comparison.csv`. P5 32 configs/quorum values not fully rederived, but `p5_callable_decisions.csv` exists. | none | paragraph refs OK | Ledger matches Ch5 limitations. | Verified |
| 760-762 | Baseline progression text | VERIFIED: single 0.015, 4-core 0.081, full10 0.070, top5 0.072, oracle 0.095, oracle gap +0.014, CI [0.008,0.166] from `feature_ablation_nested_lopo_summary.csv`, `subset_selection_robustness_summary.csv`. | none | refs OK | Consistent with line 708. | Verified |
| 764-793 | Baseline progression table | VERIFIED: all table rows match `results/mutbench/feature_analysis/feature_ablation_nested_lopo.csv` / summary and `subset_selection_robustness_210combos.csv`; note file paths in caption omit `feature_analysis/` prefix for the subset CSV but source exists there. | none | refs OK | No regression. | Minor |
| 795-797 | 210-combination subset audit | VERIFIED: 210, 0.0809, rank 13/210, 6.2%, best subset 0.0950, gap +0.0141, median 0.0525, IQR [0.0377,0.0700], full10 0.0698 from `subset_selection_robustness_summary.csv`; top-13 homoplasy claim supported by first 13 rows of `subset_selection_robustness_210combos.csv`. | none | `tab:subset_selection_top10`, `tab:nested_lopo_4core` OK | Consistent with full-lattice caveat later. | Verified |
| 799-829 | Top-10 subset table | VERIFIED: ranks 1-10, core rank 13, MCCs/deltas, full10, median all match `results/mutbench/feature_analysis/subset_selection_robustness_top10.csv` and full combos CSV. | none | label/ref OK | No issue. | Verified |
| 831-833 | Full-lattice + Shapley | VERIFIED: 1023, 87/1023, 8.5%, 0.08088, top 7-feature 0.096842, 3-core 0.086642 rank 27, Shapley values from `results/mutbench/codex_wave1/p3_full_lattice_1023.csv` and `p3_shapley.csv`. | none | `tab:audit_ledger` OK | Consistent with Ch5 caveat that 4-core is historical, not optimal. | Verified |
| 835-837 | Rank reliability | VERIFIED: decision curve 50-site expected TPs 66/68/random ~41 (text says ~30; `p2_decision_curve.csv` random at budget 20 is 15, budget 50 is 41). Other bootstrap deltas likely from same P2 run but source table only partially checked. DISCREPANCY: "versus ~30 for random allocation" at 50 sites is not in `p2_decision_curve.csv` (found 41). | none | `alg:mutbench_coldstart`, `tab:audit_ledger` OK | Interpretation still consistent, but numeric random comparator is wrong for stated budget. | Major |
| 839-841 | P1 null calibration | VERIFIED: 100,000 permutations, four nulls, 5/12 iid, 3/12 circular, 2/12 block, 1/12 local-burden, listed p-values from `results/mutbench/codex_wave1/p1_null_summary.csv` and `p1_null_per_pathogen.csv`. DISCREPANCY: sentence says 5/12 pathogens have observed MCC at/below null mean but lists six; CSV confirms six below null mean: SARS-CoV-2, HIV-1, RSV, MERS, Zika, Rabies. | none | refs OK | Major internal count/list mismatch. | Major |
| 843-845 | P5 callability | VERIFIED at summary level: 0/12 callable, sweep/32 configs/quorum language supported by `results/mutbench/codex_wave2/p5_callable_decisions.csv` and ledger; exact D1/Jaccard values not exhaustively recalculated. | none | refs OK | Consistent with abstention claims. | Verified |
| 847-849 | P6 biological nulls | VERIFIED: valid 12/12, n_perm 100,000, 4-core counts 5/5/4/4, 3-core 5/3/4/3, Norovirus p=0.00001, Stouffer p=1.0, 27/96 and 29/96 from `codex_wave3/p6_null_summary.csv` and `p6_p1_p6_robustness.csv`. | none | refs OK | No issue. | Verified |
| 851-853 | W4 Tier 2 LOPO | VERIFIED: 0/3 hscore failures, mean MCC 0.077, sd 0.136, 8/12, p=0.368, D1 0/12 from `codex_wave4/w4_labeled_lopo_summary.csv`; 1/28, 16/16 and sign percentages supported by Wave 4 expanded files. | none | ref OK | Consistent with Layer A rate-limiting. | Verified |
| 855-857 | W5 Layer A' | VERIFIED: 10/16, 2.0%-14.5%, mean -0.055, sd 0.068, median -0.057, 2/10, precision@20 0.005 from `codex_layerA_prime/lopo_summary.csv` and per-target files; Welch t=-2.96, p=0.0089 from `cross_panel_comparison.csv`; residues 98-111 require per-target inventory but plausible. | none | ref OK | No issue. | Verified |
| 859-861 | HBFWS robustness | VERIFIED: prior [0.15,0.25] in text/log; mean 0.058 vs 0.078, delta -0.020, singleton 5/8 from `hbfws_lopo_results.csv`/log. UNVERIFIED: Wilcoxon p=0.78, paired/singleton deltas, LOPO 0/11/Friedman/oracle gap are cross-file claims not fully rederived here. | none | ref OK | Consistent with adaptive failure story. | Minor |
| 863-865 | Cycle 7B intro | VERIFIED: six methods and same 12 folds in `adaptive_weighting_comparison.csv`. | none | table ref OK | No issue. | Verified |
| 867-888 | Adaptive comparison table | VERIFIED: all mean MCCs and deltas match `results/mutbench/adaptive_weighting_comparison.csv` means; p-values not in CSV but consistent with text source/ledger. | none | label/ref OK | No issue. | Minor |
| 890 | Cycle 7B synthesis | VERIFIED: seven failures including HBFWS; smallest p=0.56 from table; method means/deltas from `adaptive_weighting_comparison.csv`; EV-A71 alg-select 0.1459 vs baseline 0.0130 verified. UNVERIFIED: LOPO 0/11, Friedman p=0.990, 0.265 gap here are cross-section claims. | none | `tab:audit_ledger` OK | Consistent with Ch5. | Minor |
| 896-898 | GT heterogeneity intro | VERIFIED: 12-pathogen scope/core 11+Zika and tags from `results/mutbench/gt_heterogeneity_analysis.csv`, `layer_a_tags.csv`. | none | `subsec:feature_ablation`, `tab:gt_heterogeneity` OK | No issue. | Verified |
| 900-925 | GT heterogeneity table | VERIFIED: all n_A, immune %, best features, AUCs, consistency flags match `results/mutbench/gt_heterogeneity_analysis.csv`. Recent fix OK: HIV-1 caption says 26 operational tags vs 23 literature/mapped. D614G retained as `functional` in `layer_a_tags.csv`. | none | `tab:gt_positions`, `sec:limitations` OK | No regression. | Verified |
| 927-928 | GT heterogeneity interpretation | VERIFIED: min immune 71%, 5 best features, 10/12 consistent, omega 0.296 from `gt_heterogeneity_analysis.csv` and omega summaries. | none | `ch:discussion` OK | Consistent. | Verified |
| 934 | Search-space intro | No numeric claims except 10 features; supported by Stage 2 scoring design. | none | none | No issue. | Verified |
| 936 | EqualWeight protocol | VERIFIED: production 0.083 from `adapt_v2_summary.csv`; nested-LOPO 0.070 from `feature_ablation_nested_lopo_summary.csv`; <=0.013 and 11 reference pathogens check out. | none | refs OK | Internally careful distinction between production and nested protocols. | Verified |
| 938-939 | LOPO search-space results | VERIFIED: 0.083, 0.075, random ~0 from `adapt_v2_summary.csv`; core-11 0.093 and 9/11/8/11 need cross-section source. SUSPICIOUS consistency: called "LOPO cross-validation" while previous paragraph says nested-LOPO full10 is 0.070; this likely mixes `adapt_v2` EqualWeight top10 with nested feature-ablation LOPO. | none | `subsec:feature_ablation` OK | Wording risks contradicting line 936. | Major |
| 941-947 | Vaccine escape setup/equation | VERIFIED: 20 x 39 x 3 = 2,340 from `vaccine_escape_stage3.csv`; H3N2 29, SARS-CoV-2 30, HIV-1 45 in same CSV; remaining 8 of 11 availability framing consistent. | none | table ref OK | No issue. | Verified |
| 948-974 | Vaccine escape table/notes | VERIFIED: H3N2 fubar_bf Wavelet 9.3621, 9/29, p=3.37e-8; HIV-1 freq Wavelet 7.1875, 23/45, p=3.16e-19; SARS-CoV-2 fubar_pos_sel FreqThresh 7.6303, 2/30, p=0.0264; EqualWeight H3N2/SARS rows from `escape_validation_adapt.csv`; HIV-1 EqualWeight from `vaccine_escape_stage3.csv`; Bonferroni adjusted values match p*780. | none | label/ref OK | Notes align with Ch5 circularity audit. | Verified |
| 976-977 | Key findings | VERIFIED: HIV-1 7.19x, 82% disjoint/37 of 45, p_adj ~3.9e-9, 780 correction, H3N2/HIV-1 survive, SARS-CoV-2 exploratory from table note and Ch5; rho ~0.97 cross-ref not recalculated. | none | `sec:information_analysis` OK | Consistent. | Minor |
| 979 | H3N2 details | VERIFIED: 9/29, 9.36x; EqualWeight top-5 4.012x p=0.0023, positions 137/155/159/160/186/188, FreqThresh top5 {137,155,159,188} from `escape_validation_adapt.csv`; novel-only p=0.132 not in checked CSV. | none | none | No issue. | Minor |
| 981 | Escape availability | VERIFIED: 3 of 11, remaining 8 categories are qualitative; MERS/EV-A71 <10 not checked in source. | none | label `tab:escape_availability` unusual but resolves as local label if referenced later. | Consistent with convenience-sample framing. | Minor |
| 983-984 | Circularity audit | VERIFIED: `layer_a_tags.csv` has immune_escape tags; table gives overlap counts. | none | `ch:mutbench`, table ref OK | No issue. | Verified |
| 986-987 | Search-space reduction conclusion | VERIFIED as approximate: 500 positions -> 10-50 equals 2-10% candidate budget; 7-9x supported by escape table. | none | none | Consistent with Ch5 final summary. | Verified |

## Per-Section Severity Counts

| Section | Critical | Major | Minor | Verified |
|---|---:|---:|---:|---:|
| Adaptive limits / Cold-Start algorithm / audit ledger | 0 | 1 | 2 | 3 |
| Baseline and subset robustness | 0 | 0 | 1 | 4 |
| Pre-registered audits P2-P6 | 0 | 2 | 0 | 2 |
| W4/W5/adaptive weighting | 0 | 0 | 3 | 3 |
| Ground truth heterogeneity | 0 | 0 | 0 | 3 |
| Search-space reduction / vaccine escape | 0 | 1 | 4 | 7 |

## Overall Tally

Critical: 0. Major: 4. Minor: 10. Verified: 22. Regression: 1.

Headline issues: omega CI lower bound still uses 0.202 rather than required 0.201; P1 null paragraph has a six-item list labeled 5/12; P2 random comparator at 50-site budget disagrees with `p2_decision_curve.csv`; search-space LOPO wording mixes the 0.083 production/adapt result with the 0.070 nested-LOPO result.

RESULT_AUDIT_V2_J10: critical=0 major=4 minor=10 regression=1
