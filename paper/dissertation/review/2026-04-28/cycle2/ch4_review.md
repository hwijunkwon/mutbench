# Ch4 Cycle-2 Adversarial Review

Target: `/proj/paper/paper/dissertation/chapters_en/ch4_results.tex` (1,042 lines)
Date: 2026-04-28 (cycle 2)
Method: Re-read after cycle-1 P0 patches; line-level audit; figure/table/text triangulation; selective-reporting probe.

---

## A. Cycle-1 P0 fix verification

| Cycle-1 ID | Target line | Fix expected | Current state | Verdict |
|---|---|---|---|---|
| G14a | ch4:104 (Fig dms_evaluation_top caption) | "Jaccard 0.006 between functional and DMS-escape" → "between DMS-escape and convergent-evolution" | ch4:104 reads "Jaccard similarity = 0.006 between DMS-escape and convergent-evolution positives" | LANDED |
| G14b | ch4:210 / ch4:215 (cross_pathogen_comparison framing) | Disambiguate "best per pathogen" vs "mean MCC across detectors for top-5 scoring" | ch4:245 (text) and ch4:250 (caption) now both read "mean MCC across detectors for the top-5 scoring types"; cross-reference to Table 4.5 inserted | LANDED but **shifted line numbers** (210→245, 215→250) — reviewers using the cycle-1 line index will mis-locate |
| G14c | ch4:386 (stage3_anova_decomposition caption) | "shown" → "reported separately" because the 0.39 residual is not a bar | ch4:421 caption: "is reported separately in the text and is not included as a bar in this figure" | LANDED (line 386→421) |
| G09 | ch4:886 (novel-only Bonferroni derivation) | Provide explicit `5.0e-12 × 780 ≈ 3.9e-9` derivation | ch4:956 footnote contains the full equation | LANDED (line 886→956) |

**Internal consistency**: all four patches now read coherently. Line-number drift (~30–70 lines) is expected from inserted clauses but the cycle-1 issue tracker should be updated.

---

## B. New adversarial findings

### Critical (publication-blocking)

**Critical-1 (NEW). Cell-level vs evaluation-level ω² mixed in the same paragraph.** ch4:425–431 reports the headline 0.296 with cluster-bootstrap CI [0.195,0.333] but never quotes the cell-level ω² (0.234, ch5:290). Three sentences later, ch4:431 references the "shift from family×pathogen dominance ... to scoring×pathogen dominance"  — both numbers (0.285 vs 0.296) are evaluation-level. A hostile reviewer demands: *what is ω² when N is reduced to the cell-level 3,080?* Ch4 mentions 3,080 only in passing (ch4:522) without re-running ω². Cycle-1 issue Mi-5 already flagged this; cycle-1 P0 patches did not address it.

**Critical-2 (NEW). Novel-only Bonferroni denominator collision.** ch4:956 quotes `5.0e-12 × 780 ≈ 3.9e-9` and elsewhere (ch4:425) treats 780 as the per-pathogen family. But the abstract / ch1 / ch6 cite `2.5e-16` (full-overlap full-family Bonferroni). The novel-only `3.9e-9` is a *different* statistical object (different escape subset, same denominator). The footnote is correct, but no cross-reference clarifies that abstract's `2.5e-16` (full-set) and ch4:956's `3.9e-9` (novel-only) are not the same test under the same correction. Reviewer attack: "you applied Bonferroni 780 to a *novel* 37-position subset, but the search space for that subset is unspecified."

### Major

**Major-1.** **LOPO null-consistent framing still lives in summary block ch4:600.** Cycle-1 G02b moved the corroboration framing to ch6, but ch4:600 still says "LOPO null-consistent corroboration" without citing the one-sided p≈0.25–0.28 from ch4:480. A reader skimming only the Summary of Key Findings sees corroboration without the failure-to-reject context.

**Major-2.** **Friedman power caveat still missing in Ch4** (cycle-1 phase2b_ch4 issue M-2 was not patched). ch4:464–475 reports χ²=7.69, p=0.990 with two interpretations but never states *"power is low at n=11 blocks"*. ch5:319 has it; ch4 still omits it. This is a chapter-level self-containment defect.

**Major-3.** **Random-baseline SD inconsistency persists.** ch4:480 quotes random-baseline SD≈0.034 (per-combo LOPO null), ch4:495 quotes SD=0.003 ("41 standard deviations"). Same chapter, two random baselines, two SDs differing by 10×, no footnote distinguishing them. Cycle-1 phase2b_ch4 M-4 flagged it; not addressed.

**Major-4.** **footnote at ch4:462 says "780 combinations" but the same paragraph computes LOPO with 280** (cycle-1 phase2b_ch4 M-1, not patched). Footnote does explain the 280-vs-780 split, but the body sentence at ch4:462 still cites 780 as the rationale for 0/11 not being unexpected — this is the family-level (280) calculation domain. Confusing.

**Major-5 (NEW). HIV-1 Layer-A operational vs literature count drift.** Table 4.10 footnote (ch4:886) reports HIV-1 nA=26 (operational), but Table 4.5 (ch4:319) lists HIV-1 best MCC=0.275 against Layer A — the sample size is silent. Reviewer demands: "is HIV-1's MCC 0.275 computed at n=23 (literature) or n=26 (operational)?" ch3 reconciliation exists but is not cross-referenced inside Ch4.

### Minor

**Minor-1.** Table 4.5 (ch4:307) caption claims "9 distinct optimal scoring types"; the footnote (ch4:331) explains 3 pathogens share *freq* with different detection families. The detection-parameter difference between Influenza B (KDE p=85) and MERS (KDE p=85) is not visible in the table — both list `KDE (p=85)` at ch4:318 and ch4:325. So in the table, two pathogens (Influenza B, MERS) have *literally identical* (scoring=freq, detection=KDE p=85) tuples. This breaks the "11/11 unique combinations" claim at the parameter level. Already flagged in cycle-1 phase2_redteam.md M-09; not patched.

**Minor-2.** Table 4.10 (ch4:944) shows SARS-CoV-2 best=`FUBAR pos. sel.` but Table 4.5 (ch4:323) lists SARS-CoV-2 best=`Tranception`. The framing is "best for escape enrichment" vs "best by MCC", which is correct but the contrast is not re-stated near Table 4.10.

**Minor-3.** ch4:462 footnote uses "the larger detector-variant oracle of 0.341" but the per-pathogen mean MCC value 0.341 in Table 4.7 (ch4:553) is the *average best-MCC* across pathogens, not an oracle. Two separate quantities collapsed under one label.

---

## C. Headline number audit

| Claim | Line | Source/file | Status |
|---|---|---|---|
| ω²(scoring×pathogen)=0.296 | 11, 338, 396, 421, 425 | results/mutbench/anova_omega.csv (implied) | OK; consistent with abstract/ch5/ch6 |
| 95% CI [0.195, 0.333] | 176, 425, 489, 523 | cluster_bootstrap_omega.csv | OK |
| 6-cat aggregation ω²=0.103 | 430 | ch5:281 | OK (ch4 refers, ch5 derives) |
| within-cell residual ω²≈0.39 | 11, 396, 421, 425 | ANOVA SS partition | **Unverifiable in ch4 alone**; no table or CSV cited; only narrative. Reviewer demands SS_within / SS_total. |
| LOPO 0/11 | 12, 446 | results/mutbench/lopo_results.csv | OK |
| Friedman χ²=7.69, p=0.990 | 469 | scipy.stats.friedmanchisquare | OK; verified χ²=11×19×0.037=7.74 ≈ 7.69 |
| Permutation null P(matches=0)≈0.96 | 450, 479 | 10,000 resamples (ch4:478) | OK |
| Oracle-vs-generalized gap=0.265 | 336, 449, 462 | derivation: 0.297−0.032 | OK |
| HIV-1 7.19× full | 13, 943 | vaccine_escape_stage3.csv | OK |
| HIV-1 Bonferroni p_adj=2.47e-16 | 956 | derivation: 780 × p_raw | OK; but abstract uses 2.5e-16 (rounding). Cycle-1 Mi-9 still pending. |
| HIV-1 novel-only 7.16–8.24× | 956 | provenance text | OK |
| HIV-1 novel-only worst-case p=5.0e-12 | 956 | provenance text | OK |
| HIV-1 novel-only p_adj=3.9e-9 | 956 | derivation cited inline | OK (cycle-1 G09 fix) |
| H3N2 9.36× | 13, 942 | vaccine_escape_stage3.csv | OK |
| H3N2 novel-only 7.19× p=0.132 | 962 | provenance | OK |
| H3N2 EqualWeight 4.012× p=0.0023 | 947 | escape_validation_adapt.csv | OK |
| SARS-CoV-2 7.63× exploratory | 13, 944 | vaccine_escape_stage3.csv | OK |
| 4-feature in-sample 97.6% | 836 | demoted: now "within-pathogen ablation descriptor" | OK (cycle-1 G07) |
| 4-feature nested-LOPO p=0.61 | 837 | feature_ablation_nested_lopo_summary.csv | OK |
| MCC range 0.196–0.660 | 365 | Table 4.5 | OK |
| Mean precision 0.338 / recall 0.552 / MCC 0.341 | 553 | Table 4.7 | OK; recomputed from per-pathogen rows |
| 41-SD claim (best=0.124, baseline mean=0.001 SD=0.003) | 495 | source unspecified | **PROBLEM — source CSV not cited; SD=0.003 inconsistent with SD=0.034 at ch4:480** |
| 5.92-fold spatial enrichment z=13.34 | 254 | unspecified | unverifiable in ch4 alone |
| ESM-2 ρ=0.63 (Norovirus); ρ=−0.35 (HIV-1) | 516 | unspecified | unverifiable; sample N not stated |

**Net**: 4 of 23 headline claims have provenance gaps (within-cell residual, 41-SD, spatial enrichment, ESM-2 ρ).

---

## D. Figure-text consistency check (5 figures)

1. **`stage3_anova_decomposition.png`** (ch4:421): Caption now correctly says residual ω²≈0.39 is *not* a bar — cycle-1 G14c fix verified.
2. **`cross_pathogen_comparison.png`** (ch4:250): Caption correctly says "mean MCC across detectors for top-5 scoring types"; cycle-1 G14b fix verified. Body text at ch4:245 also clarified.
3. **`stage3_lopo_crossval.png`** (ch4:459): Caption says 0/11 is null-consistent (P≈0.96) and points to the gap as the readable signal — consistent with body text. OK.
4. **`stage3_scoring_pathogen_heatmap.png`** (ch4:343): Caption says "best MCC across all detection families for a given scoring–pathogen combination". Heatmap max ≈ 0.303 (visual), but Table 4.5 best (HCV)=0.660. Phase 2b cycle-1 already flagged this — visual range vs tabulated max diverge because the heatmap aggregates differently. Caption is technically OK but a reader who eyeballs the heatmap will not see HCV=0.660.
5. **`feature_importance_grid.png`** (ch4:736): Caption attributes Dengue best to homoplasy. Per Table 4.6 (ch4:689), Dengue homoplasy AUC=0.770 is indeed highest — caption OK in fact. Cycle-1 phase2b M-5 readability concern still applies.

---

## E. Selective reporting findings

A hostile reviewer demands these missing values:

1. **Per-pathogen ω²(scoring×detection family)**. Ch4 presents only the panel-aggregate. With 11 clusters, leaving out HCV gives 0.246 (ch4:525), but no full LOOCV table (e.g., ω² with each pathogen excluded). Lower-bound robustness is asserted, not tabulated.
2. **Bonferroni-survivor mean enrichment as headline number**. The chapter-summary block (ch4:13) headlines top-1 9.36×/7.19×/7.63×; the Bonferroni-survivor mean (~4.7× H3N2, ~4–5× HIV-1) is buried in the Table 4.10 footnote (ch4:956) and never referenced in the keybox. Cycle-1 phase2_redteam.md M-08 demanded this; not addressed.
3. **Second-best scoring type per pathogen**. Table 4.5 lists only the best. A reviewer who suspects winner's curse asks: "what is the gap between best and second-best?" — not shown.
4. **Per-pathogen LOPO MCC table**. Figure 4.7 shows it visually; numbers are not tabulated. Recovery requires reading the figure.
5. **Subgroup ω² by Layer-A evidence type** (immune-escape only vs convergent-evolution only). ch4:911 reports "10/12 retain best feature when restricted to immune-escape-only" but does not re-compute ω² on the homogeneous subset.
6. **Failure cases for top-1 combinations**. Table 4.7 row "MERS precision=0.045 with perfect recall" implies the detector flagged 200 of 1,330 positions — i.e., 22% of the protein. This *is* mentioned (ch4:559) but framed as a limitation rather than a failure. Cycle-1 phase2b Mi-6.

---

## F. Cell-level vs aggregate ω² disambiguation

ch4 reports ω²=0.296 in five places (ch4:11, 338, 396, 421, 425) **without any of them re-stating the cell-level alternative**. ch4:431 forward-references the family×pathogen→scoring×pathogen *evaluation-level* shift (0.285→0.296). ch5:290 carries the cell-level 0.234, ANCOVA-adjusted 0.264, partial-pooled 0.252. These do not appear in ch4 except via narrative gestures at the residual.

**Verdict**: ch4 *over-presents* the 0.296 headline. A reviewer who reads only ch4 would not learn that the cell-level estimate is 0.234. Phase 4 professor #3 (statistics/ML) flagged this exact concern as "MEDIUM risk" — i.e., the cycle-1 P0 patches did not propagate ch5's honest demote into ch4's results-side framing.

---

## G. Cross-pathogen generalization claim — does the data support it?

ch4 explicitly demotes LOPO at three places (ch4:336, 462, 480, 600) to "corroboration not independent evidence". The summary block at ch4:600 still couples "LOPO null-consistent corroboration" with "Friedman χ²=7.69 p=0.990" as evidence lines for pathogen-dependent optimality.

**The data say**: ANOVA interaction ω²=0.296 (modeled-only, large), Friedman p=0.990 (no rank concordance), LOPO 0/11 + 0.265 gap (one-sided p≈0.25, null-consistent). Two of three lenses *fail to reject the null of universality*. The chapter is honest about each in isolation but the four-lens summary at ch4:595 still presents them as "consistent evidence". A precise statement would be: *only ANOVA (within the modeled subspace) supports pathogen-dependence; the other three lenses do not contradict it but provide no positive evidence*.

---

## H. Recommended cycle-2 edits

| Severity | File:Line | Current | Proposed | Rationale |
|---|---|---|---|---|
| Critical | ch4:425 | "(ω²=0.296; CI [0.195,0.333])" | "(ω²=0.296 evaluation-level; CI [0.195,0.333]; cell-level ω²=0.234, see Section~\ref{sec:critical_appraisal_anova} of Chapter~\ref{ch:discussion})" | Force ch4 to acknowledge the cell-level demote |
| Critical | ch4:956 | "novel-only $p_{\text{adj}} = 5.0 \times 10^{-12} \times 780 \approx 3.9 \times 10^{-9}$" | add: "Note: this denominator (780) is shared with the full-overlap test ($p_{\text{adj}}=2.47 \times 10^{-16}$); the two p-values are different statistical objects (different position subsets) under the same correction family." | Disambiguate Critical-2 |
| Major | ch4:475 | "this non-significance admits two interpretations" | append "Friedman power at n=11 blocks is limited (~0.15 for medium W), so the non-significance is consistent with both readings; this is corroboration, not disconfirmation, of pathogen-dependence." | Major-2 |
| Major | ch4:495 | "exceeds the random baseline (mean=0.001, SD=0.003) by approximately 41 standard deviations" | add footnote: "This SD=0.003 is the SD of mean across 11 pathogens for a single random combo (different from the single-pathogen single-combo SD=0.034 cited at ch4:480; the former is the SE of a panel mean, the latter the SD of one combo's MCC)." | Major-3 |
| Major | ch4:462 | "given 780 unique scoring–detection combinations" | "given 280 family-level combinations (footnote)" | Major-4 (cycle-1 M-1 not patched) |
| Major | ch4:13 (key box) | "HIV-1 7.19×, H3N2 9.36×" | append: "Bonferroni-survivor mean: H3N2 ≈4.7×, HIV-1 ≈4–5× (Table 4.10 footnote)" | Selective reporting #2 |
| Major | ch4:600 | "LOPO null-consistent corroboration" | "LOPO 0/11 + 0.265 gap (one-sided permutation p≈0.25–0.28; null-consistent, treated as corroboration not independent evidence)" | A null result should not be summarized in two words |
| Minor | ch4:331 | "Nine distinct scoring types appear as best" | append: "Note Influenza B and MERS share both scoring (freq) and detection-parameter (KDE p=85) — at the parameter level only 10/11 combinations are unique." | Minor-1 honesty |
| Minor | abstract / ch4:956 | "p_adj=2.5e-16" vs "2.47e-16" | unify rounding policy (cycle-1 Mi-9 not patched) | Minor |

---

## I. Severity summary

| Tier | Cycle-1 unresolved | Cycle-2 new | Total |
|---|---|---|---|
| Critical | 0 | **2** (cell-level ω², Bonferroni denominator collision) | 2 |
| Major | **5** (M-1, M-2, M-3, M-4, M-08 selective reporting) | **1** (HIV-1 nA drift) | 6 |
| Minor | **3** (M-09 unique-tuple, Mi-9 rounding, Mi-6 MERS framing) | **2** | 5 |

**Verdict**: Cycle-1 P0 patches landed cleanly at the four target lines, but cycle-1 phase2b_ch4.md flagged 13 substantive issues and only 4 (G09, G14a-c) were patched. The remaining 9 plus 2 cycle-2-new criticals constitute the cycle-2 P0 list. Highest priority: ch4:425 cell-level disambiguation and ch4:956 denominator collision footnote.

End of cycle-2 ch4 review.
