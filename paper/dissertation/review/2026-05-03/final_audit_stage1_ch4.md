# Final Audit Stage 1: ch4_results

Observed repo state: `master` at `746549a` (requested v227 was not separately resolvable from git metadata). Scope file: `paper/dissertation/chapters_en/ch4_results.tex` (954 lines). Audit was read-only except for this report.

## A. Numerical consistency

Verified against the specified CSV authorities.

- `stage3_full_results.csv`: 8,580 data rows confirmed. Best-per-pathogen rows match Table `stage2_best` and precision@k table values: MCC range 0.196--0.660, mean 0.3415; HCV best 0.660, H3N2 0.534, SARS-CoV-2 0.211, MERS/RSV 0.196. Worst grid row confirmed: HCV x `stability` x `SWAN(w=50,k=1.0)`, MCC -0.361346, precision/recall/F1 0, `n_detected=139`. Negative-MCC counts confirmed: 4,171/8,580 (48.6%) and 4,695/8,580 (54.7%) <=0. Worst detector and scoring means match: ScoreDBSCAN eps 15/8, `plddt_inv`, `grantham`, `tranception`.
- `stage3_statistics.csv`: ANOVA omega values match ch4: scoring 0.063, pathogen 0.117, scoring x pathogen 0.296252, family x pathogen 0.0815; Friedman chi-square 7.687967 with p=0.989545; LOPO match 0/11, generalized MCC 0.0315, gap 0.2654.
- `cluster_bootstrap_omega_summary.csv` and `omega_robustness_5way.csv`: headline omega 0.296252 and cluster CI [0.200836, 0.345502] match rounded [0.201, 0.346]. Five-frame robustness values match: standard [0.2008,0.3455], wild [0.2005,0.3032], phylo [0.2022,0.3457], mixed pseudo-omega 0.3398/lower 0.188, Bayesian [0.2421,0.3882]. Cameron 2008 wild-cluster citation is present.
- `layer_c_evaluation.csv`: six Layer C pathogens and counts verified: SARS-CoV-2 247, H3N2 112, HIV-1 48, RSV 101, Rabies 87, EV-A71 55. Best Layer C MCC range confirmed 0.138527--0.322436; table values round correctly. Note: the counts are not printed in ch4, only the pathogen set and DMS source citations are.
- `vaccine_escape_stage3.csv`: HIV-1 `freq`/Wavelet(t=1.5) 23/45, enrichment 7.1875, p=3.16e-19, Bonferroni p_adj 2.47e-16 verified. H3N2 FUBAR BF/Wavelet(t=2.0) 9/29, enrichment 9.3621, p=3.37e-8 verified. SARS-CoV-2 FUBAR pos sel/FreqThresh(p=85) 2/30, enrichment 7.6303, p=0.026424 verified. HIV-1 EqualWeight CUSUM(d=0.5,h=5.0) 4.1667, p=0.003734 verified.
- `escape_validation_adapt.csv`: H3N2 EqualWeight top-5 enrichment 4.012, p=0.002254, detected sites 137/155/159/160/186/188 verified; SARS-CoV-2 top-5 EqualWeight 2.665, p=0.170515 verified.
- `feature_ablation_nested_lopo_summary.csv`: full-10 0.069754 [0.0170,0.1295], fixed-4 0.080882 [0.0077,0.1664], paired delta +0.011128 [-0.0177,+0.0424] verified.
- Wave audits: P1 4-core iid <= null mean 6/12 and iid significant 5/12 verified; P2 budget-50 random expected TP 41, 4-core 66, 3-core 68 verified; P3 4-core rank 87/1023 verified; P5 callable 0/12 for both 3-core and 4-core verified; P6 four structural nulls and 4-core significant counts 5/5/4/4 verified; W4 8/12 positive p=0.367658 verified; W5 mean MCC -0.055488 verified.
- Adaptive failures: Cycle 7B smallest one-sided Wilcoxon p among the six adaptive methods is 0.560759 for rank aggregation; HBFWS mean 0.0583 vs EqualWeight-4core 0.0779, delta -0.0196, p=0.779366 verified.

## B. Citation integrity

21 cite instances, 19 unique keys. All keys resolve in `paper/dissertation/references.bib`. No unresolved citation keys found.

## C. Cross-reference integrity

129 `\ref{...}` instances, 64 unique targets. All referenced labels exist in the active front/ch1--ch5 TeX set. No duplicate labels found. No orphaned equation/table/figure references found in ch4.

Semantic spot-check: no ch4 reference target was obviously wrong from its local context. A compatibility label `ch:adapt` exists inside ch4's `Information-Type Analysis` section, but ch4 itself does not reference it.

## D. Triage framing consistency

Keyword audit found no unqualified deployability/prospective-detector claims. Relevant wording is consistently bounded:

- Stage 1: “retrospective sanity check,” “do not upgrade it into a prospective detector.”
- 4-core: “retrospective audit,” “not a prospectively callable detector.”
- Algorithm 1: explicitly “retrospective triage, not deployment,” “not a globally calibrated detector,” and “formally abstained from deployment.”
- LOPO 0/11 is repeatedly paired with null-consistency, omega/Friedman framing, and adaptive failures; no standalone overclaim found.
- The 20--30+ pathogen language is qualified as a “stability target rather than a proven phase transition.”

Framing inconsistencies found: 0.

## E. Layer C / HIV-1 anchor

Layer C anchor is numerically correct and source-cited for DMS datasets in Table `layer_a_vs_c`; best-MCC range 0.139--0.322 matches the CSV. The six Layer C ground-truth counts are verified in CSV but are not explicitly printed in ch4.

HIV-1 vaccine escape anchor is correctly framed: 7.19x, p_adj approximately 2.5e-16, 8/45 Layer-A overlap, 37/45 Layer-A-disjoint (82%), novel-only p_adj approximately 3.9e-9, and H3N2/SARS-CoV-2 marked as self-consistency/exploratory rather than equivalent external anchors.

## F. Compression regression check

- Bolker rule-of-thumb: regression found. ch4 line 670 retains “20--30+ pathogens recommended as a stability target rather than as a proven phase transition,” but ch4 does not directly cite `bolker2009glmm`; the Bolker citation appears in ch5 discussion. For a chapter-deep defense read, add the citation locally or make the cross-chapter dependency explicit.
- “Not learnable”: phrase does not appear in ch4; no unqualified use found. ch5 pairs it with `n=11`.
- Equations/tables/figures: no orphaned refs found.
- Load-bearing triage claims retained: P5 abstention, P6 descriptive-only, W4/W5 failures, HBFWS/Cycle7B failures, and HIV-1 anchor all remain present.

## Issue list

- Critical: None.
- Major: ch4 retains the 20--30+ stability-target statement but lacks a direct Bolker citation in the chapter; only ch5 carries `bolker2009glmm`.
- Minor: Layer C counts are verified in `layer_c_evaluation.csv` but not printed in ch4, so the “6 pathogens + counts” anchor is less self-auditable from the chapter text alone.
- Minor: The HIV-1 EqualWeight CUSUM row is verified, but the surrounding label “best-detector grid” could be read as “best detector”; other EqualWeight HIV-1 grid rows have lower p-values. This is wording clarity, not a numerical error.

RESULT_FINAL_AUDIT_STAGE1_ch4: critical=0 major=1 minor=2 framing_inconsistencies=0 orphan_refs=0
