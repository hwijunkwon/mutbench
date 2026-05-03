# Professor 1: Chair, bioinformatics (strictness=medium)

## Stage 1 reports consulted
- abstract_ch1: Strong bounded framing around retrospective wet-lab triage, with minor residual prospective/cold-start wording drift.
- ch2: Current, task-aware related work that separates MutBench from VEP, surveillance, and selection-test benchmarks, but leaves coupling/epistasis outside scope.
- ch3: Methodological scaffold is auditable and broad, with frozen design and layer separation, though dense prose and legacy labels remain.
- ch4: Strong results interpretation around scoring-by-pathogen interaction and HIV-1 validation, with hidden risks in oracle framing, scope shifts, and narrow external validation.
- ch5: Mature discussion and limitations, explicitly rejecting deployment; denominator drift and late audit density remain visible weaknesses.

## Specialty deep-read
- abstract+ch1: The triage frame is genuinely front-loaded: the abstract states retrospective wet-lab triage rather than prospective deployment, and Chapter 1's panel-scope ledger usefully prevents confusing 11-pathogen headline claims with 12-pathogen feature/audit panels. I also noticed remaining rhetoric that could still be read as stronger than warranted: "practical impact," "cold-start recipe," and "might important mutations occur next" are not fully harmonized with the non-deployable guardrail.
- ch4: Direct reading confirmed that the load-bearing evidence is the scoring x pathogen interaction with cluster-bootstrap CI and counterfactual nulls, plus HIV-1 escape enrichment; the manuscript appropriately demotes LOPO 0/11 and Friedman p=0.990 to consistency checks. The DMS section is valuable but the caption's "confirming independence" is somewhat stronger than the later text, which more carefully says Layer A and C capture non-identical aspects.
- ch5: The discussion is unusually candid: it states forward-time AUROC 0.539, 0/12 callable folds, Layer A curation limits, PLM leakage/collinearity, winner's curse, and dual-use risks. The strongest practical section still rests mainly on HIV-1, while the 4-core cold-start recipe is explicitly a historical heuristic and is even strictly dominated by a 3-core variant in the audit.

## Scores
A: 8.6
B: 8.3
C: 8.3
D: 8.5
E: 8.5
F: 8.4
G: 7.8
H: 7.9
I: 9.1
J: 8.6
total: 84.0/100

## Rationale (per item, 2-3 sentences each, citing Stage 1 evidence + your specialty observations)

A. problem statement: 8.6. Stage 1 abstract_ch1 identifies a clear problem: absence of a standardized benchmark, independent ground truth, and statistical evidence for pathogen-dependent method choice. My direct read confirms that the abstract and Chapter 1 make the wet-lab triage niche explicit, but some prospective language and "practical impact" wording still slightly weaken the discipline of the problem frame.

B. related work: 8.3. Stage 1 ch2 finds strong, current positioning against ProteinGym, EVEREST, ViroGym, surveillance platforms, cancer hotspot methods, HyPhy, and other adjacent literatures. I deduct because epistasis/coupling-aware methods are reviewed as out of scope rather than benchmarked, some method-history coverage is compressed, and result numbers leak into the background chapter.

C. methodology: 8.3. Stage 1 ch3 and ch4 show a serious methodological contract: three-layer ground truth, 20 scoring types, 14 detector families, 39 variants, MCC-centered Stage 2 evaluation, frozen grids, ANOVA, cluster bootstrap, LOPO, and counterfactual nulls. My direct ch4 read supports the design, but deductions remain for dependent variants, uneven Layer C coverage, deferred sensitivities, and methods/results boundary blur.

D. scale: 8.5. Stage 1 ch3/ch4 document substantial scale for a dissertation benchmark: 11 RNA-virus glycoproteins, 8,580 evaluations, 73 temporal splits, and DMS Layer C for 6 pathogens. The scale is not a general viral-mutation universe: it is surface glycoproteins, single-position substitution labels, heterogeneous Layer A rates, and only 3 pathogens with vaccine/antibody escape validation.

E. interpretation: 8.5. Stage 1 ch4/ch5 emphasize mature interpretation: the manuscript demotes 11/11 uniqueness, LOPO 0/11, and Friedman p=0.990, while interpreting omega^2=0.296 as the real interaction evidence. My direct read confirms careful failure-case language for MERS and non-deployment, but some local phrases remain overstrong, especially "exactly what pathogen-dependent optimality predicts" and "confirming independence."

F. novelty/contribution: 8.4. Stage 1 abstract_ch1, ch4, and ch5 support a real contribution: a broad region-level single-position RNA-virus hotspot benchmark, quantified pathogen-by-information interaction, and guarded wet-lab triage anchor. Novelty is narrower than a deployable predictor or general VEP system, and the cold-start 4-core is a bounded heuristic rather than an optimized algorithmic breakthrough.

G. practical value: 7.8. Stage 1 ch4/ch5 show concrete practical value as search-space reduction: HIV-1 7.19x escape enrichment, 82% Layer-A-disjoint support, 37/45 novel positions, plus Layer C DMS validation over 6/11 pathogens. I score this lower than the benchmark items because the strongest external validation rests mainly on HIV-1, H3N2 is mostly self-consistency, SARS-CoV-2 is exploratory, and prospective/callable performance is refused.

H. clarity: 7.9. Stage 1 reports praise the ledgers, tables, evidence hierarchy, and explicit guardrails, all of which I found helpful in the abstract, Chapter 1, and Chapter 5. The deduction is for density: many paragraphs read like audit ledgers, terminology shifts among 11/12/Wave panels require attention, and legacy labels/cross-reference artifacts remain.

I. limitations awareness: 9.1. Stage 1 ch5 identifies unusually strong limitations awareness, and direct reading confirms a broad matrix covering Layer A heterogeneity, small n, winner's curse, prospective gap, PLM leakage, input artifacts, sub-lineage pooling, dual-use, and independent reproduction. The score is high because the manuscript does not hide damaging results: 73-window AUROC 0.539, 0/12 callable folds, Layer A' failure, and failed adaptive methods are all surfaced.

J. overall maturity: 8.6. Stage 1 abstract_ch1 and ch5 show mature claim calibration: the thesis now reads as a retrospective benchmark and wet-lab triage framework, not a prospective detector. Remaining maturity deductions come from late-stage integration complexity, denominator drift between 11 and 12 pathogen contexts, and some prose that still bears compression/revision scars.

## Strongest single deduction
one-line: G, practical value is real but primarily HIV-1-anchored and retrospective; fix by adding balanced independent wet-lab/escape validation across more of the 11-pathogen panel under a predeclared non-oracle protocol.

RESULT_PROF_V8_01: total=84.0/100 min_item=7.8(G) max_item=9.1(I) stage1_evidence_used=5
