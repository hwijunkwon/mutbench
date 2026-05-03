# Final Audit Aggregate (master v227, 197pp)

## 1. Stage 1 summary

| Scope | Critical | Major | Minor | Notes |
|---|---:|---:|---:|---|
| Abstract + Ch1 | 0 | 0 | 1 | Wave 4/5 paragraph refs resolve to Ch4, but Ch1 sentence attributes them to Discussion. |
| Ch2 background | 0 | 1 | 1 | Bolker retention check fails literally; Layer C/HIV-1 numerics partially summarized rather than fully printed. |
| Ch3 methods | 0 | 0 | 2 | HCV sensitivity number stale/ambiguous; local git metadata does not expose v227. |
| Ch4 results | 0 | 1 | 2 | Bolker 20--30+ statement lacks local citation; Layer C counts not printed; HIV-1 EqualWeight wording could be clearer. |
| Ch5 discussion | 0 | 0 | 1 | ANCOVA adjusted interaction stale: Ch5 says 0.264, Ch3/archive indicate 0.274. |
| **Total** | **0** | **2** | **7** | No Stage 1 critical defects. |

## 2. Cross-chapter numerical consistency

| Anchor | Chapters where appears | Values found | Match |
|---|---|---|---|
| Scoring x pathogen omega^2 | Abstract/Ch1, Ch2, Ch3, Ch4, Ch5 | 0.296; cluster CI [0.201, 0.346] | PASS |
| Five-frame omega CIs | Ch3, Ch4, Ch5 narrative | standard [0.201, 0.346], wild [0.201, 0.303], phylo [0.202, 0.346], mixed 0.340 lower 0.188, Bayesian HDI [0.242, 0.388] | PASS |
| Friedman / LOPO | Abstract/Ch1, Ch3, Ch4, Ch5 | chi^2 7.69, p 0.990; LOPO 0/11 | PASS |
| HIV-1 vaccine escape | Abstract/Ch1, Ch2, Ch4, Ch5 | 7.19x; p_adj approx 2.5e-16; 82% Layer-A-disjoint; 37/45 novel in Ch1/Ch4/Ch5 | PASS |
| H3N2 / SARS-CoV-2 escape | Abstract/Ch1, Ch4, Ch5 | H3N2 9.36x; SARS-CoV-2 7.63x exploratory | PASS |
| HBFWS | Abstract, Ch4, Ch5 | p = 0.78 / 0.779 rounded | PASS |
| Cycle 7B | Abstract, Ch4, Ch5 | six paradigms; smallest p = 0.56 | PASS |
| Wave 4 | Ch1, Ch4, Ch5 | 8/12 positive; p = 0.368 | PASS |
| Wave 5 Layer A' | Abstract, Ch1, Ch4, Ch5 | mean MCC = -0.055 | PASS |
| 4-core vs full-10 | Ch1, Ch3, Ch4, Ch5 | 0.0809 vs 0.0698; paired delta +0.011; p = 0.61 | PASS |
| Subset ranks | Ch4, Ch5 | restricted 4-core rank 13/210; full lattice 87/1023; 3-core rank 27/1023 | PASS |
| P1 null calibration | Ch4, Ch5 | at/below-null counts 6/12 iid/circular, 4/12 block, 7/12 local-burden; significance count 5/12 iid degrades to 1/12 strict | PASS |
| P2 decision curve | Ch4 | random 41 at budget 50; 4-core 66; 3-core 68 | PASS |
| P5 callable | Ch4, Ch5 | 0/12 callable | PASS |
| P6 nulls | Ch4, Ch5 | 5/12 sasa and plddt; 4/12 joint nulls | PASS |
| Layer C | Abstract/Ch1, Ch3, Ch4, Ch5 | 6 pathogens; 650 positions; SARS-CoV-2 247, H3N2 112, HIV-1 48, RSV 101, Rabies 87, EV-A71 55; best MCC 0.139--0.322 | PASS |

Cross-chapter key-anchor verdict: **PASS**. The two Stage 1 numerical stale values (Ch3 HCV sensitivity 0.246 vs archive ambiguity, Ch5 ANCOVA 0.264 vs 0.274) are outside the requested key-anchor list but remain recommended fixes.

## 3. Bibliography orphan analysis

Active citation scope used: `front_en/abstract.tex`, `chapters_en/ch1_introduction.tex`, `ch2_background.tex`, `ch3_methods.tex`, `ch4_results.tex`, and `ch5_discussion.tex`. `ch5_adapt.tex` is excluded because it is commented out in `thesis_en.tex`.

BibTeX keys defined: 126. Unique active cite keys: 122. Cited keys missing from `references.bib`: **none**.

Bib keys defined but never cited in the active build:

- `bolker2009glmm`
- `chen2022gisaid`
- `ioannidis2008winner`
- `kaku2024virological`

Citation integrity verdict: **FAIL for orphan cleanup**, but no unresolved active citation key was found.

## 4. Triage framing global verdict

Stage 1 D-sections found **0 framing inconsistencies** across all scopes. The manuscript consistently bounds current claims as retrospective wet-lab triage, search-space reduction, exploratory cold-start prioritization, or screening-budget allocation. LOPO 0/11 is paired with Friedman/HBFWS/Cycle 7B failures and small-panel caveats, not used as standalone proof. Algorithm 1 is repeatedly framed as not a globally calibrated detector and formally abstained from deployment under P5. The 20--30+ pathogen language is framed as a stability/design target rather than a proven phase transition.

Remaining stragglers: no unbounded `deployable`, `deployment`, `prospective detector`, or `phase transition` claim was found. Bounded uses of `operational` remain in Ch3/Ch5; they describe metric operationalization, operational implication, or feasibility, not deployment. The only framing-adjacent issue is citation support: Ch2 lacks the Bolker rule entirely and Ch4 has 20--30+ stability-target language without a local Bolker citation.

Verdict: **CONSISTENT**.

## 5. Cross-reference orphans

Stage 1 found no unresolved `\ref{}` targets and no duplicate labels. Independent active-build parsing found 230 unique labels, 138 unique referenced labels, 407 ref instances, **0 refs to non-existent labels**, and **0 duplicate labels**.

Labels defined but never referenced in the active source:

`ch:adapt`, `ch:conclusion`, `eq:coordinate_transform`, `eq:expand_cluster`, `eq:weighted_hotspot_score`, `fig:feature_ablation`, `fig:variance_decomposition`, `para:cold_start_baseline_progression`, `para:mutbench_algorithm`, `para:sliding_window_4feature`, `para:stage2_worst_mcc`, `sec:9pathogen_benchmark`, `sec:bootstrap_interpretation`, `sec:circularity`, `sec:comparison_prior_work`, `sec:complementary_gt`, `sec:contribution_summary`, `sec:cross_pathogen_implications`, `sec:design_considerations`, `sec:final_conclusion`, `sec:homoplasy_scoring`, `sec:influenza_validation`, `sec:intro_background`, `sec:intro_contributions`, `sec:intro_motivation`, `sec:intro_objectives`, `sec:intro_organization`, `sec:oracle_mcc_ceiling`, `sec:practical_surveillance`, `sec:practical_workflow`, `sec:real_gisaid_benchmark`, `sec:recall_analysis`, `sec:sensitivity_analysis`, `sec:single_pathogen_benchmark`, `sec:statistical_validation`, `sec:synthetic_real_gap`, `subsec:9pathogen_anova`, `subsec:9pathogen_data`, `subsec:9pathogen_detection`, `subsec:9pathogen_friedman`, `subsec:9pathogen_scale`, `subsec:9pathogen_subsampling`, `subsec:9pathogen_supplementary`, `subsec:adaptive_weighting_limits`, `subsec:alternative_scoring`, `subsec:bg_algorithm_selection`, `subsec:bg_density_clustering`, `subsec:bg_feature_importance`, `subsec:bg_hotspot_methods`, `subsec:bg_plm`, `subsec:bg_surveillance`, `subsec:dms_subgroup`, `subsec:gt_heterogeneity_results`, `subsec:homoplasy_sensitivity`, `subsec:improvements`, `subsec:info_type_implications`, `subsec:mutbench_hscore`, `subsec:pahd_motivation_summary`, `subsec:pahd_prototype`, `subsec:per_feature_auc`, `subsec:stage1_gt`, `subsec:statistical_methods`, `subsec:treetime_gisaid_validation`, `subsec:weight_sensitivity_methods`, `subsubsec:bayesian_methods`, `subsubsec:h3n2_temporal_methods`, `subsubsec:headline_metric_choice`, `subsubsec:jackknife_acknowledgement`, `subsubsec:mantel_acknowledgement`, `subsubsec:preregistration`, `subsubsec:structural_phylo_validation`, `subsubsec:tranception_separation`, `tab:abstract_evidence_ledger`, `tab:bootstrap_ci`, `tab:defense_map`, `tab:detection_variants`, `tab:dms_subgroup`, `tab:dms_threshold_sensitivity`, `tab:dnds_threshold`, `tab:escape_availability`, `tab:external_methods`, `tab:gt_layer_roles`, `tab:hdbscan_sensitivity`, `tab:homoplasy_validation`, `tab:influenza`, `tab:intro_external_validation_ledger`, `tab:intro_panel_scope`, `tab:lopo_summary`, `tab:phylo_sensitivity`, `tab:rf_cv_auc`, `tab:sliding_window_backtest`, `tab:weight_sensitivity`.

These are not broken references, but they are cross-reference orphans under the literal defined-but-unreferenced criterion.

## 6. Defense readiness checklist

| Category | Verdict | Basis |
|---|---|---|
| Phase 4 gate | PASS | 83.63. |
| Numerical consistency | PASS | All requested cross-chapter key anchors match where they occur. |
| Citation integrity | FAIL | No missing active cite keys, but 4 BibTeX entries are defined and unused. |
| Triage framing | PASS | No unbounded deployment/operational/phase-transition claim found. |
| Cross-reference integrity | YELLOW | No missing refs; many unreferenced labels remain. |
| Defense readiness | YELLOW | Scientifically consistent, but cleanup remains before a clean final defense package. |

## 7. Recommended fixes

1. Add or remove local Bolker support consistently: either cite `bolker2009glmm` where Ch4 uses the 20--30+ stability-target statement and decide whether Ch2 should carry the rule, or remove the unused BibTeX key if the rule is intentionally supported only in prose without citation.
2. Resolve the four orphan BibTeX entries: `bolker2009glmm`, `chen2022gisaid`, `ioannidis2008winner`, `kaku2024virological`.
3. Fix the Ch5 ANCOVA stale value from 0.264 to 0.274 if Ch3/archive remain authoritative.
4. Resolve the Ch3 HCV sensitivity wording/number: clarify HCV-only vs HCV-excluded and align 0.246/0.253 with the archive.
5. Correct Ch1's Wave 4/5 attribution from Discussion to Results, or move/alias the paragraph targets.
6. Decide whether the 92 unreferenced labels are intentional navigation anchors. Remove stale compatibility labels such as `ch:adapt`/`ch:conclusion` if they are no longer useful.
7. Optionally print the full Layer C count anchor in Ch2/Ch4 for self-auditability, since the values are already correct in Ch3/Ch5.

RESULT_FINAL_AUDIT_AGGREGATE: critical=0 major=2 minor=9 consistency=PASS citation=FAIL framing=PASS defense_readiness=YELLOW
