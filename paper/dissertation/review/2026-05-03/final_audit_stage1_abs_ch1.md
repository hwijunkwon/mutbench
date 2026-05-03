# Final Audit Stage 1: abstract+ch1

Scope audited: `paper/dissertation/front_en/abstract.tex` and `paper/dissertation/chapters_en/ch1_introduction.tex` on `master` `746549a`. Audit was read-only except for this report.

## A. Numerical consistency

Verified against the requested CSVs.

- Benchmark scale: `stage3_full_results.csv` has 8580 data rows, 11 pathogens, 20 scoring formulas, 39 detector variants, and 14 families. Abstract line 2/17 and ch1 lines 51, 129 are consistent.
- Main ANOVA/Friedman/LOPO: `stage3_statistics.csv` gives scoring-pathogen omega^2 = 0.2962519839, Friedman p = 0.9895445, LOPO match rate = 0/11, mean generalized MCC = 0.031508. Abstract lines 19-20/25 and ch1 lines 132-135 are consistent.
- Bootstrap omega: `cluster_bootstrap_omega_summary.csv` gives 11-pathogen bootstrap mean 0.271561, CI [0.200836, 0.345502], supporting the rounded CI [0.201, 0.346]. `omega_robustness_5way.csv` contains the five-frame robustness rows, including wild-cluster Rademacher mean 0.2685, CI [0.2005, 0.3032]. No deviation in scoped text.
- Vaccine escape: `vaccine_escape_stage3.csv` verifies H3N2 fubar_bf + Wavelet(t=2.0): 9.3621x, 9/29, p=3.37e-08; HIV-1 freq + Wavelet(t=1.5): 7.1875x, 23/45, p=3.16e-19, Bonferroni 780x = 2.46e-16; SARS-CoV-2 fubar_pos_sel + FreqThresh(p=85): 7.6303x, 2/30, p=0.026424, Bonferroni non-survivor. Abstract and ch1 rounded values are consistent.
- Fixed escape protocol: `escape_validation_adapt.csv` verifies H3N2 EqualWeight top-5 enrichment 4.012, p=0.002254; scoped ch1 line 150 is consistent.
- Layer C: `layer_c_evaluation.csv` verifies 6 pathogens and 650 positions: SARS-CoV-2 247, H3N2 112, HIV-1 48, RSV 101, Rabies 87, EV-A71 55. Best MCCs are 0.139-0.322: HIV-1 0.138527, H3N2 0.244504, EV-A71 0.322436. Abstract line 17 is consistent.
- Feature ablation: `feature_ablation_nested_lopo_summary.csv` verifies full-10 = 0.069754, fixed-4 = 0.080882, delta = 0.011128, CI [-0.017747, 0.042390]. Ch1 line 152 is consistent.
- Wave/adaptive boundaries: `p1_null_per_pathogen.csv` supports P1 4-core p20 6/12; `p2_decision_curve.csv` verifies random budget-50 total 41; `p3_full_lattice_1023.csv` ranks 4-core 87th; `p5_callable_decisions.csv` gives 0/12 callable for both 3-core and 4-core; `p6_null_summary.csv` contains four null types; `w4_labeled_lopo_summary.csv` gives 8/12 positive and p=0.367658; `codex_layerA_prime/lopo_summary.csv` gives mean MCC -0.055488; `adaptive_weighting_comparison.csv` gives Cycle 7B rank-aggregation Wilcoxon p=0.560759; `hbfws_lopo_results.csv` gives HBFWS greater-than Wilcoxon p=0.779366. Scoped abstract/ch1 claims using these values are consistent.

## B. Citation integrity

Found 18 citation calls containing 14 unique keys: `bailey2018comprehensive`, `carabelli2023convergent`, `gurev2026everest_v3`, `han2025mosd`, `harvey2021tracking`, `livesey2020using`, `nextstrain2018hadfield`, `notin2023proteingym`, `notin2025proteingym_v13`, `rambaut2020pangolin`, `rice1976algorithm`, `thadani2023evescape`, `virogym2026`, `youn2025mutclust`.

All 14 keys exist in `paper/dissertation/references.bib`. No unresolved citations.

## C. Cross-reference integrity

Found 26 `\ref{}` calls containing 12 unique keys. All labels exist in the active English build files (`front_en`, `chapters_en/ch1-ch5`, `back`), with no duplicate labels and no orphan references.

Resolved targets checked: `ch:background`, `ch:mutbench`, `ch:results`, `ch:discussion`, `fig:research_overview`, `subsec:feature_ablation`, `tab:nested_lopo_4core`, `tab:stage2_anova`, `sec:future_work`, `sec:limitations`, `para:w4_tier2_lopo`, `para:w5_layer_a_prime`.

Minor target-context issue: ch1 line 65 says Wave 4-5 paragraphs are in Chapter Discussion, but `para:w4_tier2_lopo` and `para:w5_layer_a_prime` resolve to `chapters_en/ch4_results.tex` lines 818 and 822. The refs are not orphaned, but the surrounding chapter attribution is wrong.

## D. Triage framing consistency

Keyword audit for `deployable`, `deployment`, `operational`, `prospective detector`, `operational`, `phase transition`, `20--30`, `LOPO 0/11`, and `Algorithm 1` found no overclaim.

- Abstract line 2 explicitly says retrospective wet-lab triage, not prospective deployment.
- Abstract lines 20, 25, 27 pair non-deployability/not-learnable language with `n=11` and tested-regime qualifiers.
- LOPO 0/11 is paired with Friedman/HBFWS/adaptive failures in the abstract and with omega^2/Friedman/vaccine-escape context in ch1 lines 132-135.
- Bolker 20--30 is framed as design guidance, not a phase transition.
- No scoped claim says Algorithm 1 is a calibrated detector.

## E. Layer C / HIV-1 anchor

Layer C anchor is correctly cited in the abstract: 6/11 pathogens, 650 total positions, exact per-pathogen counts, best MCC range 0.139-0.322, EV-A71 0.322 with pLDDT-inv + Wavelet, and H3N2 0.245 with semantic-change + KDE.

HIV-1 anchor is correctly cited: full-set enrichment 7.19x, Bonferroni p_adj approx 2.5e-16, 37/45 Layer-A-disjoint positions (82%), and novel-only enrichment 7.16-8.24x with p_adj approx 3.9e-9 in ch1.

## F. Compression regression check

Load-bearing claims survived compression. Bolker remains a design target, not a sufficiency/phase-transition claim. “Not learnable” is qualified by `n=11` and tested-regime language. No equations, figures, or tables in scope have orphaned references.

The only compression-sensitive regression found is the minor chapter-attribution mismatch for Wave 4/5 paragraph refs in ch1 line 65.

## Issue list

- Critical: None.
- Major: None.
- Minor: ch1 line 65: `para:w4_tier2_lopo` and `para:w5_layer_a_prime` resolve to Chapter 4 results paragraphs, but the sentence attributes them to Chapter Discussion.

RESULT_FINAL_AUDIT_STAGE1_abs_ch1: critical=0 major=0 minor=1 framing_inconsistencies=0 orphan_refs=0
