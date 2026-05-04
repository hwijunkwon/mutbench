# Professor 1: Chair, bioinformatics (strictness=medium)

## Stage 1 reports consulted
- abstract_ch1: Strong bounded problem and contribution framing, with residual prospective-sounding phrasing and dense audit-style presentation.
- ch2: Broad and current related-work positioning; strongest on task separation from VEP/surveillance benchmarks, weaker on epistatic/coupling methods and occasional forecasting language.
- ch3: Detailed, auditable methodology and large design grid, but with proxy channels, deferred checks, and some implementation-label drift.
- ch4: Strong retrospective benchmark evidence for pathogen-dependent information utility, with careful caveats around LOPO/Friedman, practical validation, and deployment refusal.
- ch5: Mature narrowing chapter with excellent limitations and claim calibration; practical value is strongest for HIV-1 and Layer C, but denominator/numeric drift remains visible.

## Specialty deep-read
- abstract+ch1: The triage boundary is genuinely front-loaded: the abstract says retrospective wet-lab triage rather than prospective deployment, and Chapter 1 repeatedly separates the 11-pathogen headline panel from 12-pathogen feature analyses. I also noticed that the new Layer C DMS evidence is stronger in the abstract than in the Chapter 1 contribution hierarchy, and "application to new pathogens"/cold-start phrasing still risks sounding more operational than the evidence supports.
- ch4: The load-bearing result is the scoring-by-pathogen interaction, not the visually tempting "all 11 unique" or LOPO 0/11 claims; the footnote correctly reduces unique best combinations to 10/11 at the parameter-variant level. The MERS precision 0.045 failure case, 3/11 vaccine-escape convenience sample, and HIV-1 as the least circular escape anchor are well disclosed.
- ch5: The limitations matrix is unusually examiner-ready, especially on Layer A heterogeneity, PLM leakage, small-cluster inference, prospective failure, and dual-use handling. I confirmed the stale 0.234 cell-level anchor appears alongside updated 0.233/0.274 language, and 11-vs-12 denominator shifts remain a polish and audit risk.

## Scores
A: 8.7
B: 8.4
C: 8.3
D: 8.5
E: 8.5
F: 8.6
G: 7.8
H: 8.0
I: 9.1
J: 8.4
total: 84.3/100

## Rationale (per item, 2-3 sentences each, citing Stage 1 evidence + your specialty observations)

A. problem statement: 8.7  
Stage 1 abstract_ch1 identifies a precise problem: region-level single-position hotspot prioritization for narrowing roughly 1,000 sites to 10--50 wet-lab candidates, plus three Chapter 1 gaps in evaluation framework, independent ground truth, and pathogen-dependence. My direct read confirms the dissertation now states its non-deployment boundary early and repeatedly. The deduction is for residual forecasting phrasing in related work and new-pathogen workflow language that slightly conflicts with the retrospective triage frame.

B. related work: 8.4  
Stage 1 ch2 shows broad, current coverage across frequency, entropy, selection, PLM, DMS, surveillance, cancer hotspot, and benchmark literature, with a defensible distinction from ViroGym, EVEREST, and ProteinGym. This is enough for a strong bioinformatics dissertation because the task boundary is well drawn. The score is capped because coupling-aware/epistatic models are treated thinly, some MutBench results leak into background, and "broadest" depends on a narrow but valid task definition.

C. methodology: 8.3  
Stage 1 ch3 and ch4 document a concrete three-component pipeline, three-layer ground truth, 20 scoring types, 39 detector variants, MCC-based Stage 2 evaluation, ANOVA, LOPO, Friedman, bootstrap, permutation, and external audits. My ch4 read supports the methodological maturity: weak corroborative tests are explicitly demoted, and MERS saturation is not disguised as success. Deductions come from proxy implementations such as Tranception/ESM substitutions, deferred Layer C threshold checks for some pathogens, homoplasy tree-source ambiguity, and non-independent reuse of the same 8,580-row grid.

D. scale (panel size, breadth): 8.5  
Stage 1 ch3/ch4 support strong scale: 11 RNA viruses across families and routes, 8,580 evaluation cells, 3,080 more independent scoring-family-pathogen cells, 6 Layer C DMS pathogens, 73 temporal splits, and 2,340 vaccine-escape enrichment evaluations. For this task, the panel is broad and biologically meaningful. The cap is statistical rather than cosmetic: cluster inference has only 11 pathogens, Layer C covers 6/11, escape validation covers 3/11 by convenience, and Zika/12-pathogen analyses can blur the headline panel.

E. interpretation (results reading): 8.5  
Stage 1 ch4/ch5 highlight unusually careful interpretation: "largest modeled component" is distinguished from residual variance, LOPO 0/11 and Friedman p=0.990 are treated as null-consistent, and the oracle-vs-generalized gap is the real operational signal. My direct read confirms the dissertation refuses to turn weak prospective backtests into deployment claims. Deductions remain for occasional over-strong local wording, especially "exactly what pathogen-dependent optimality predicts," "confirming independence" in the Layer C caption, and "with benchmark validity established."

F. novelty/contribution: 8.6  
Stage 1 abstract_ch1, ch4, and ch5 support a real contribution: a broad RNA-virus region-level hotspot benchmark, quantified pathogen-by-information interaction with omega squared 0.296, and a guarded wet-lab triage result with HIV-1 and Layer C anchors. My specialty read agrees that novelty lies in benchmark/task/statistical framing, not in inventing a deployable detector. The deduction is that the contribution is internally constructed and still awaits independent disjoint-panel replication, while the cold-start recipe is useful but not a proven adaptive selector.

G. practical value (wet-lab triage utility): 7.8  
Stage 1 ch4/ch5 show practical value in search-space reduction, HIV-1 7.19x escape enrichment with 82% Layer-A-disjoint support, and Layer C DMS validation across 6/11 pathogens with MCC 0.139--0.322. My direct read confirms the practical claim is strongest as a ranked screening-budget allocator. The score is lower because prospective transfer is weak, callability is 0/12, H3N2 is mostly self-consistency, SARS-CoV-2 is exploratory, and vaccine-escape generalization to 8/11 pathogens is unknown.

H. clarity (writing): 8.0  
Stage 1 reports consistently credit the ledgers, tables, and boundary statements for making a complex audit readable. I agree: the manuscript is unusually explicit about panel scope, evidence hierarchy, and negative findings. Deductions are for density, acronym/load-bearing numeric compression, category/count drift, "four chapters" despite merged background, stale 0.234 alongside updated values, and occasional patched-feeling audit prose.

I. limitations awareness: 9.1  
Stage 1 ch5 identifies this as a major strength, and my direct read confirms it: Layer A heterogeneity, prospective failure, dual-use risk, PLM leakage, winner's curse, small n, reproduction limits, MAFFT artifacts, and scope limits are all disclosed in a defense-ready matrix. The dissertation does not merely list limitations; it uses them to narrow the claim to retrospective triage. The small deduction is because some important limitations remain unresolved rather than merely bounded, especially independent recuration/inter-annotator agreement and single-mode alignment sensitivity.

J. overall maturity: 8.4  
Stage 1 abstract_ch1/ch5 show mature claim calibration: non-deployability is explicit, negative adaptive-selection audits are reported, and panel/evidence tiers are separated. My direct read confirms the work is substantially more mature than a typical benchmark because failed gates are not hidden. The score is capped by one-team provenance, small-cluster inference, denominator/numeric drift, and a manuscript style that sometimes reads like late-stage audit containment rather than a fully settled dissertation narrative.

## Strongest single deduction
one-line: G, practical value is credible for retrospective wet-lab triage but not yet for prospective deployment because escape validation is mainly HIV-1/3-pathogen and callability is 0/12; fix by adding an independently curated expanded panel with time-forward validation and predeclared callable subsets.

RESULT_PROF_V9_01: total=84.3/100 min_item=7.8(G) max_item=9.1(I) stage1_evidence_used=5
