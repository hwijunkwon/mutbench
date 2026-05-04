# Professor 6: VEP/PLM expert (strictness=highest)

## Stage 1 reports consulted
- abstract_ch1: Strong bounded triage problem, clear ledgers, but residual prospective wording and dense labels.
- ch2: Broad, current related-work positioning against VEP/surveillance/cancer benchmarks; epistasis/coupling treatment remains compressed.
- ch3: Auditable pipeline and large grid, with important caveats around proxy PLM channels, deferred checks, and scope-label drift.
- ch4: Strong retrospective evidence for scoring x pathogen interaction and HIV-1 escape anchor; LOPO/Friedman are correctly weak/null-consistent.
- ch5: Mature narrowing chapter with excellent limitations; practical claim rests mainly on HIV-1 plus 6/11 Layer C DMS, not deployability.

## Specialty deep-read
- ch3: The PLM/VEP implementation is weaker than its labels imply: Tranception is an ESM-2 pseudo-perplexity proxy, EVEscape substitutes ESM-2 for EVE, and the merged-channel sensitivity is deferred. Structural channels also rely heavily on monomer ESMFold/AlphaFold proxies, with oligomeric SASA left unresolved.
- ch4: The load-bearing result is genuinely the modeled scoring x pathogen effect, supported by five robustness frames, but the "all 11 unique" language is internally overstrong because only 10/11 tuples are unique at parameter-variant level. DMS Layer C is valuable but low-MCC and shows ground-truth divergence rather than a unified validation win.
- ch5: The discussion is commendably strict about deployment refusal, prospective weakness, and Layer A heterogeneity. I would still penalize the cold-start recipe language because the 4-core is admitted to be historical, dominated by a 3-core, globally null-calibrated, and 0/12 callable.

## Scores
A: 8.5
B: 8.3
C: 8.0
D: 8.2
E: 8.4
F: 8.1
G: 7.6
H: 7.8
I: 9.0
J: 8.3
total: 82.2/100

## Rationale (per item, 2-3 sentences each, citing Stage 1 evidence + your specialty observations)

**A. problem statement: 8.5.** Stage 1 abstract/ch1 found a precise problem: region-level, single-position hotspot prioritization for retrospective wet-lab triage, reducing roughly 1,000 positions to 10--50 candidates. That framing is strong and mostly preserved in ch4/ch5, but related-work phrases about predicting emergence and "might important mutations occur next" still activate a prospective-detector expectation that the data do not support.

**B. related work: 8.3.** Stage 1 ch2 shows strong coverage across frequency, entropy, phylogenetic selection, DMS, PLMs, surveillance, VEP benchmarks, and cancer hotspot analogues, with good task separation from ProteinGym, EVEREST, and ViroGym. As a VEP/PLM reader, I deduct for thin treatment of DCA/EVcouplings/GREMLIN-style coupling models and for only briefly explaining why single-position hotspot detection is the right abstraction despite known epistasis in viral escape.

**C. methodology: 8.0.** Stage 1 ch3/ch4 correctly emphasizes the auditable 3-layer ground truth, frozen thresholds, 20 x 39 x 11 grid, MCC choice, and robustness frames. The strict deduction is that several named channels are proxies: Tranception is not Tranception, EVEscape is not full EVEscape, stability is BLOSUM-based rather than physics-based, and the homoplasy production tree source has ambiguity; these are disclosed but materially lower method fidelity.

**D. scale (panel size, breadth): 8.2.** The computational breadth is large: 11 RNA viruses, 8 ICTV families, 20 scoring formulas, 14 detector families, 39 variants, and 8,580 evaluation rows, with DMS for 6 pathogens and escape audits for 3. The ceiling is capped because independent pathogen clusters are only 11, Layer C is uneven, escape validation is a convenience sample, and repeated detector variants overstate independent sample size relative to the 3,080-cell effective grid.

**E. interpretation (results reading): 8.4.** Stage 1 ch4/ch5 found unusually careful interpretation: "largest modeled component," LOPO 0/11 as corroborative/null-consistent, Friedman p=0.990 as no universal winner, and MERS called a failure case despite perfect recall. I still deduct for local overstatements such as "exactly what pathogen-dependent optimality predicts," "confirming independence" for Layer C, and headline "all 11 unique" phrasing that needs the footnote to become true enough.

**F. novelty/contribution: 8.1.** The novelty is real as a benchmark-and-evidence contribution: region-level viral hotspot benchmarking, quantified pathogen-dependent information utility, and guarded wet-lab triage validation. It is not a new deployable VEP model, not a full PLM advance, and not a universal adaptive selector; the PLM contribution is especially narrow because key PLM-labeled channels are ESM-2-derived proxies.

**G. practical value (wet-lab triage utility): 7.6.** Practical value is credible for retrospective triage: HIV-1 gives 7.19x escape enrichment with 82% Layer-A-disjoint positions, and Layer C gives a separate DMS axis across 6/11 pathogens. The score stays below 8 because H3N2 is mostly self-consistency, SARS-CoV-2 is exploratory after correction, prospective backtests are weak, and cold-start deployment is explicitly refused at 0/12 callable folds.

**H. clarity (writing): 7.8.** Stage 1 reports consistently note useful ledgers, self-contained tables, and explicit caveats. The manuscript is also dense, audit-patched, and terminology-heavy: Stage 2/Stage 3, 11 vs 12 pathogens, 10 families vs 6 categories, HBFWS/Cycle 7B/Wave labels, and long compressed paragraphs make a correct reading possible but not easy.

**I. limitations awareness: 9.0.** This is the strongest item. Stage 1 ch5 identifies a comprehensive limitations matrix covering Layer A heterogeneity, PLM leakage/proxy collinearity, small n, winner's curse, sub-lineage pooling, prospective failure, dual use, MAFFT artifacts, and reproduction limits; my reread confirms these are not cosmetic caveats but operationally constrain the claims.

**J. overall maturity: 8.3.** The work is mature in claim calibration, provenance, negative-result reporting, and refusal to oversell deployment. It loses points for source-level inconsistency and patched density, especially numeric/denominator drift, proxy-channel caveats deferred to future cycles, and cold-start wording that remains more recipe-like than the audits justify.

## Strongest single deduction
one-line: C, PLM/VEP method fidelity is weaker than the labels suggest; fix by renaming proxy channels unambiguously, running or removing true-model comparisons, and completing the merged-PLM sensitivity.

RESULT_PROF_V9_06: total=82.2/100 min_item=7.6(G) max_item=9.0(I) stage1_evidence_used=5
