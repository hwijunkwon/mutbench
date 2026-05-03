# Final Audit Stage 1: ch5_discussion

## A. Numerical consistency

Verified against the requested result artifacts.

- `stage3_full_results.csv`: 8,580 data rows, 11 pathogens, 20 scoring types, 14 detector families, 39 detector variants. Chapter claims of 8,580 evaluations and 20 x 39 grid are consistent.
- Per-pathogen oracle MCC from `stage3_full_results.csv`: mean 0.3415, range 0.1962-0.6602; mean recall 0.5517; 9 distinct optimal scoring types. Chapter values 0.341, 0.196-0.660, 0.552, and 9 distinct types are consistent.
- `stage3_statistics.csv`: scoring omega^2=0.0630, family omega^2=0.0126, pathogen omega^2=0.1173, scoring x pathogen omega^2=0.2963, family x pathogen omega^2=0.0815; Friedman chi^2=7.688, p=0.9895; LOPO match rate 0/11, mean generalized MCC 0.0315, oracle-vs-generalized gap 0.2654. Chapter values 0.013, 0.082, 0.296, Friedman 7.69/p=0.990, LOPO 0/11, gap 0.265 are consistent.
- `cluster_bootstrap_omega_summary.csv` and `omega_robustness_5way.csv`: headline omega^2=0.2963; cluster mean 0.2716 with CI [0.2008, 0.3455]; five-frame robustness includes standard cluster 0.2716, wild cluster 0.2685, phylo block 0.2719, mixed effects 0.3398, Bayesian 0.3155. Chapter CI [0.201, 0.346] and five-frame narrative are consistent.
- `vaccine_escape_stage3.csv`: H3N2 reported anchor row gives 9.3621x, p_adj=2.63e-5; HIV-1 anchor row gives 7.1875x, p_adj=2.47e-16; SARS-CoV-2 reported exploratory row gives 7.63x in the table context. Chapter rounded values 9.36x, 7.19x, 2.5e-16, 2.6e-5, and 7.63x are consistent with the cited table narrative.
- `escape_validation_adapt.csv`: H3N2 EqualWeight top-5 gives enrichment 4.012, p=0.002254, n_detected=28, n_overlap=6. Chapter 4.012x and p=0.0023 are consistent.
- `layer_c_evaluation.csv`: Layer C covers 6 pathogens and 650 positions: SARS-CoV-2 247, H3N2 112, HIV-1 48, RSV 101, Rabies 87, EV-A71 55. Best Layer C MCC range is 0.1385-0.3224; EV-A71 best is pLDDT-inv + Wavelet at 0.322; H3N2 best is semantic-change + KDE at 0.245. Chapter values are consistent.
- `feature_ablation_nested_lopo_summary.csv`: full-10=0.06975; fixed 4-core=0.08088; delta=+0.01113; CI [-0.01775,+0.04239]. Chapter values 0.070/0.081, +0.011, CI [-0.018,+0.042], p=0.61 are consistent.
- Wave audits: P1 iid 4-core MCC significance is 5/12, not 6/12, in `p1_null_per_pathogen.csv`; Chapter 5 states 5/12, consistent. P2 random expected TP at budget 50 sums to 41, consistent where referenced. P3 4-core rank is 87/1023 and 3-core rank 27/1023, consistent. P5 callable count is 0/12. P6 has 4 pathogens under the two joint nulls. W4 has mean MCC 0.0768, 8/12 positive, p=0.3677. W5 has mean MCC -0.0555 and 2/10 positive. Cycle 7B smallest one-sided Wilcoxon p versus EqualWeight-4core recomputes to 0.5608; HBFWS greater-than-baseline p recomputes to 0.7794. Chapter values are consistent.

Deviation found:

- Minor numerical stale value: Chapter 5 line 216 says ANCOVA amplifies `0.234 -> 0.264`, but Chapter 3/4 ANCOVA text and archive search indicate the adjusted value is 0.274. This is outside the mandatory CSV list but is a numerical inconsistency inside scope.

## B. Citation integrity

All 10 cite keys in `ch5_discussion.tex` resolve in `references.bib`: `gurev2025everest`, `katoh2013mafft`, `nextstrain2018hadfield`, `notin2023proteingym`, `rice1976algorithm`, `sagulenko2018treetime`, `shu2017gisaid`, `turakhia2020ultrafast`, `weirauch2013evaluation`, `wolpert1997nfl`.

Unresolved cite keys: none.

## C. Cross-reference integrity

All 51 unique `\ref{...}` keys in Chapter 5 resolve to labels in the active English build scope (`front_en`, `ch1`-`ch5`). Key targets were checked, including `alg:mutbench_coldstart`, `tab:vaccine_escape_stage3`, `tab:layer_a_vs_c`, `tab:nested_lopo_4core`, `para:p5_callability`, `para:p6_biological_nulls`, `para:w4_tier2_lopo`, and `para:w5_layer_a_prime`.

Orphan refs: none. Wrong-target evidence: none found.

## D. Triage framing consistency

Keyword audit found `deployable`, `deployment`, `operational`, `prospective`, and `Algorithm` usages, but they are bounded. Chapter 5 consistently frames current use as wet-lab triage, retrospective prioritization, exploratory cold-start heuristic, or screening-budget allocation. It explicitly says prospective detector performance/deployment/callability is not supported until external expanded-panel gates pass.

No unqualified `deployable`/`deployment`/`operational` claim was found. `20--30+` appears as a future validation/stability target and is explicitly not a guaranteed phase transition. LOPO 0/11 is paired with omega^2/Friedman/adaptive-failure context and is explicitly not standalone proof. Algorithm 1 is framed as an exploratory cold-start prioritization heuristic, not a calibrated detector.

## E. Layer C / HIV-1 anchor

Layer C anchor is correctly stated: 6/11 pathogens, 650 positions, pathogen counts 247/112/48/101/87/55, and best MCC range 0.139-0.322.

HIV-1 anchor is correctly stated: full-set enrichment 7.19x, p_adj=2.5e-16, 82% Layer-A-disjoint / 18% overlap, and 37 Layer-A-disjoint positions in the novel-only audit. The chapter consistently treats HIV-1 as the primary external anchor, H3N2 as self-consistency due to 69% overlap, and SARS-CoV-2 as exploratory.

## F. Compression regression check

No load-bearing deletion found. Bolker remains in the limitations/defense-map context as a 20-30 design/stability target, not a phase transition. "Not learnable" remains scoped to `n=11` and the tested labels/features. Equations, tables, figures, and paragraph refs used by Chapter 5 resolve; no orphaned reference was detected.

## Issue list

- Critical: none.
- Major: none.
- Minor: Chapter 5 line 216 appears stale: ANCOVA adjusted interaction is written as 0.264; surrounding active text/archive indicates 0.274.

RESULT_FINAL_AUDIT_STAGE1_ch5: critical=0 major=0 minor=1 framing_inconsistencies=0 orphan_refs=0
