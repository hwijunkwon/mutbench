# Professor 10: Structural biology (strictness=medium)

## Stage 1 reports consulted
- abstract_ch1: Strong bounded problem framing around retrospective wet-lab triage, with minor residual prospective wording and "cold-start recipe" tension.
- ch2: Strong current related-work positioning for region-level hotspot benchmarking, but compressed treatment of coupling/epistasis-aware methods and some result leakage into background.
- ch3: Auditable methodology and large 8,580-cell design, with candid dependence caveats, uneven Layer C coverage, and dense revision-polish artifacts.
- ch4: Statistically mature results chapter; load-bearing evidence is the scoring-by-pathogen interaction plus HIV-1/DMS validation, not uniqueness, LOPO, or Friedman.
- ch5: Mature claim calibration and limitations matrix; practical value is credibly reframed as triage, while denominator drift and narrow independent external validation remain important.

## Specialty deep-read
- ch4: The DMS section is useful structurally because pLDDT-inv wins Layer C for SARS-CoV-2 and EV-A71, and Layer A/Layer C winners differ in all 6 DMS pathogens. However, the text's caption-level "confirming independence" is stronger than the later, more accurate claim that the layers capture non-identical aspects; DMS MCC values are modest (0.139--0.322).
- ch5: The discussion correctly treats pLDDT as an optional structural extension rather than a core proven driver: the full lattice/Shapley audit says the 4-core is historical and the 3-core dominates it, with pLDDT slightly negative on average. I also credit the structural null audits, but they are descriptive robustness checks, not independent deployment evidence.

## Scores
A: 8.6
B: 8.3
C: 8.4
D: 8.5
E: 8.4
F: 8.2
G: 7.8
H: 8.0
I: 9.1
J: 8.5
total: 83.8/100

## Rationale (per item, 2-3 sentences each, citing Stage 1 evidence + your specialty observations)

A. The problem statement is one of the manuscript's stronger features: Stage 1 abstract/ch1 found a clear gap around standardized hotspot evaluation, independent ground truth, and pathogen-dependent method choice, all bounded to wet-lab triage rather than deployment. I deduct modestly because Stage 1 also found residual prospective language such as "might important mutations occur next" and "practical impact," which matters because the defense depends on keeping the claim non-deployable.

B. Chapter 2 gives a strong task-aware literature frame, distinguishing surveillance, VEP benchmarks, cancer hotspot work, selection tests, and viral region-level hotspot detection. The deduction is for compressed treatment of modern coupling/epistasis-aware approaches and some fragility in "broadest" language, especially because structural biology readers will expect clearer separation between single-position scoring and residue-network/epistatic effects.

C. The methodology is detailed and mostly audit-ready: Stage 1 ch3/ch4 emphasized frozen grids, Layer A/B/C roles, 20 scoring types, 39 detector variants, MCC choice, ANOVA, bootstrap, and LOPO distinctions. I withhold a higher score because some methods are reconstructed in the results, several sensitivity checks are deferred or uneven, PLM channels are partially redundant, and DMS Layer C exists for only 6/11 pathogens.

D. Scale is good for a dissertation: 11 RNA viruses, 8,580 main evaluations, 73 temporal splits, 219 top-k evaluations, and diverse surface glycoproteins with substantial sequence counts. The main limitation is heterogeneity of evidence depth: five pathogens lack Layer C, vaccine escape validation covers only 3/11, and several audits move to a 12-pathogen scope including Zika, which creates comparability friction.

E. Interpretation is mature overall. Stage 1 ch4/ch5 correctly identified that the manuscript demotes 11/11 uniqueness, LOPO 0/11, and Friedman p=0.990 to consistency or null evidence while centering omega^2=0.296 and the HIV-1 external anchor. My direct read confirms this discipline, but I penalize local overstatements such as "confirming independence" for Layer C and "exactly what pathogen-dependent optimality predicts"; these should be softened to avoid causal over-reading.

F. Novelty is strong as a benchmark-and-audit contribution: the combination of region-level RNA-virus hotspot benchmarking, pathogen-by-information interaction quantification, and guarded wet-lab triage evidence is distinctive. It is less strong as an algorithmic breakthrough, because the cold-start 4-core is historical rather than optimal, adaptive selection fails at n=11, and the biological fact that pathogens differ is not itself surprising without the quantified benchmark.

G. Practical value is real but bounded. Stage 1 ch4/ch5 show credible triage utility through Layer C DMS for 6/11 pathogens and HIV-1 escape enrichment of 7.19x with 82% Layer-A-disjoint positions, plus a plausible search-space reduction from about 1,000 sites to 10--50 candidates. The deduction is substantial because HIV-1 carries most independent external value, H3N2 is partly self-consistency, SARS-CoV-2 is exploratory after correction, and the strongest "optimal scoring-detection" claim is oracle/post-hoc rather than cold-start deployable.

H. The writing is clear in its evidence ledgers, tables, and claim boundaries, and Stage 1 found the abstract/introduction especially useful for controlling interpretation. However, the manuscript is dense and sometimes reads like an audit packet, with overloaded labels (Layer, Stage, Wave, Cycle, HBFWS), denominator shifts, legacy labels, and long caveat paragraphs that reduce readability for non-specialists.

I. Limitations awareness is excellent. Stage 1 ch5 identified a comprehensive limitations matrix covering Layer A heterogeneity, small panel size, prospective failure, label provenance, dual-use, PLM leakage, sampling, MAFFT artifacts, and independent reproduction. My direct read confirms the most important boundary is not hidden: 0/11 or 0/12 callability/generalization failures block deployment, and retrospective triage is the recommended use.

J. Overall maturity is high because the manuscript now refuses the stronger detector claim, reports negative audits, separates evidence tiers, and presents reproducibility anchors. I do not score it higher because the dissertation still shows signs of late-stage patch integration: 11-vs-12 denominator drift, anchor-preservation labels, dense audit paragraphs, and occasional stronger captions than body text. From a structural biology standpoint, the use of pLDDT/SASA is thoughtful but not yet a decisive structural-mechanistic contribution.

## Strongest single deduction
one-line: G, practical value is promising but rests mainly on HIV-1 plus partial DMS support; fix by adding independent residue-level escape/DMS validation across more pathogen families under a pre-specified non-oracle triage protocol.

RESULT_PROF_V8_10: total=83.8/100 min_item=7.8(G) max_item=9.1(I) stage1_evidence_used=5
