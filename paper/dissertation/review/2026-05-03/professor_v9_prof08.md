# Professor 8: Practice/field user (strictness=high)

## Stage 1 reports consulted
- abstract_ch1: Strong bounded benchmark-and-triage framing, but residual prospective-sounding wording and dense audit labels remain.
- ch2: Related work is broad and current, with good task-boundary separation from VEP/surveillance/cancer benchmarks; epistatic/coupling methods are thin.
- ch3: Methods are detailed and auditable at large scale, but proxy implementations, deferred checks, and label/category drift cap confidence.
- ch4: Results are unusually transparent and well-tempered; practical value is real but retrospective, HIV-1-heavy, and not deployable.
- ch5: Discussion strongly narrows claims and discloses limitations; some denominator/numeric drift and audit-memo density reduce polish.

## Specialty deep-read
- abstract+ch1: The problem is now clearly wet-lab triage, not prospective deployment, and the evidence ledger is useful for a field reader. I also saw practical language such as "cold-start recipe" and "Practical Impact" that can still be read as more operational than the evidence supports.
- ch4: The strongest practice-facing evidence is HIV-1 escape enrichment plus Layer C DMS validation for 6/11 pathogens, but the chapter itself reports weak prospective backtests, 0/12 callability, MERS saturation, and null-consistent LOPO.
- ch5: The limitations matrix is a major strength for real-world use decisions. The recommended-use paragraph correctly restricts MutBench to retrospective prioritization, though the step-by-step novel-virus workflow and family-prior table still require cautious wording in any field-facing deployment context.

## Scores
A: 8.4
B: 8.3
C: 8.2
D: 8.4
E: 8.3
F: 8.2
G: 7.7
H: 7.5
I: 9.0
J: 8.1
total: 82.1/100

## Rationale

**A. problem statement: 8.4**  
Stage 1 abstract_ch1 correctly flagged an unusually explicit problem: region-level single-position hotspot prioritization for retrospective wet-lab triage, with the practical target of reducing roughly 1,000 positions to 10--50 candidates. My direct read confirms the three Chapter 1 gaps are concrete and useful for practitioners: no standardized framework, no independent ground truth, and no statistical evidence for pathogen-dependent method choice. The deduction is for residual forecasting-flavored phrases in Chapter 2 and operational wording in Chapter 1/5 that can still over-activate deployment expectations.

**B. related work: 8.3**  
Stage 1 ch2 shows strong coverage across frequency, entropy, density, selection, DMS, PLMs, surveillance, and adjacent benchmarks, and it distinguishes MutBench from ViroGym, EVEREST, and ProteinGym by task. That distinction is credible: MutBench is region-level hotspot prioritization, not per-variant fitness or escape prediction. The ceiling is limited by compressed treatment of epistatic/coupling-aware methods and some results leakage into the related-work chapter.

**C. methodology: 8.2**  
Stage 1 ch3/ch4 support a solid methods score: three-layer ground truth, 20 scoring types, 39 detector variants, MCC-centered cross-pathogen evaluation, and cluster-aware robustness are all auditable. The direct Chapter 4 read shows the strongest methodological maturity is not the raw 8,580-row grid but the admission that effective independence is closer to 3,080 cells and that ANOVA assumptions fail. Deductions come from proxy channels, deferred robustness checks, homoplasy tree-source ambiguity, and Layer A heterogeneity.

**D. scale (panel size, breadth): 8.4**  
Stage 1 ch3/ch4 establish strong scale for this task: 11 RNA viruses, 8 ICTV families, several transmission routes, 20 scoring formulas, 14 detector families, and 8,580 evaluations. Layer C adds meaningful wet-lab breadth across 6/11 pathogens and 650 positions. The cap is that 11 pathogen clusters remain statistically small, Zika/12-pathogen analyses blur boundaries, and external escape validation is feasible for only 3/11 pathogens.

**E. interpretation (results reading): 8.3**  
Stage 1 ch4/ch5 consistently show good interpretive discipline: "all unique" and LOPO 0/11 are explicitly treated as null-consistent, while the load-bearing evidence is the scoring-by-pathogen interaction and bounded escape/DMS validation. My direct read confirms Chapter 4 repeatedly rescues possible overreadings with caveats, including poor prospective transfer and the non-independence of statistical lenses. The deduction is for local overstatements such as "exactly what pathogen-dependent optimality predicts" and a few captions stronger than the prose.

**F. novelty/contribution: 8.2**  
The novelty is real but narrow: a broad RNA-virus, region-level, single-position hotspot benchmark plus a quantified pathogen-by-information interaction and guarded triage validation. Stage 1 abstract_ch1/ch4/ch5 all support that this is not being sold as a deployable detector, which makes the contribution more defensible. It does not reach a higher score because the contribution is mostly benchmark synthesis and empirical calibration, not an operational ML method, and independent disjoint-panel replication remains future work.

**G. practical value (wet-lab triage utility): 7.7**  
As a practice/field user, I give credit for concrete triage economics: 10--50 candidate positions, HIV-1 7.19x escape enrichment with 82% Layer-A-disjoint support, and Layer C DMS validation across 6/11 pathogens with best MCC 0.139--0.322. Chapter 5 correctly frames the practical claim as search-space reduction, not high absolute prediction accuracy. The main deduction is that prospective transfer is weak, callability is 0/12, H3N2 is mostly self-consistency, SARS-CoV-2 is exploratory, and the strongest independent practical anchor is mainly HIV-1.

**H. clarity (writing): 7.5**  
The ledger style helps auditability, and Stage 1 reports correctly note that the abstract, Chapter 1, and Chapter 5 provide unusually explicit boundaries. For a field user, however, the manuscript is dense with labels, waves, layers, HBFWS/Cycle 7B terms, p-values, archive references, and 11-vs-12 panel shifts. Direct reading also found small polish issues such as "four chapters" after a merged related-work chapter and a visible "all 11 unique" headline that needs the footnote to be correct.

**I. limitations awareness: 9.0**  
Stage 1 ch5 is persuasive here: the limitations matrix covers label heterogeneity, small n, PLM leakage, prospective failure, dual use, source-selection limits, and reproduction. My direct read confirms the manuscript plainly says retrospective prioritization only and refuses calibrated detector or family-conditional classifier claims until external callability gates are met. Remaining deductions are for unresolved limitations, especially lack of independent recuration/inter-annotator agreement and unquantified MAFFT-mode sensitivity.

**J. overall maturity: 8.1**  
The dissertation is mature in claim calibration: it reports negative results, preserves provenance anchors, distinguishes evidence tiers, and repeatedly avoids deployable-detector claims. Stage 1 reports also show good panel hygiene around Layer A/B/C, HIV-1 vs H3N2/SARS-CoV-2, and Bolker 20--30 as a design target rather than proof. I deduct for patched-feeling audit density, denominator/numeric drift, and the fact that real-world maturity is still retrospective-benchmark maturity rather than validated field deployment.

## Strongest single deduction
one-line: G, practical value is limited by weak prospective transfer and 0/12 callability despite useful HIV-1-anchored retrospective wet-lab triage; fix by adding externally validated prospective or held-out expanded-panel triage evidence.

RESULT_PROF_V9_08: total=82.1/100 min_item=7.5(H) max_item=9.0(I) stage1_evidence_used=5
