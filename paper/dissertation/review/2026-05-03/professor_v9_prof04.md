# Professor 4: Computational biology (strictness=medium)

## Stage 1 reports consulted
- abstract_ch1: Strong bounded problem and claim ledger; residual prospective-sounding phrases and dense abbreviations remain.
- ch2: Broad, current related-work framing separates hotspot-region benchmarking from VEP/surveillance/cancer tools, with thin epistasis/coupling coverage.
- ch3: Detailed auditable methods and large grid; proxy channels, deferred checks, and some label/category drift cap the methods score.
- ch4: Strong retrospective benchmark and interpretation; load-bearing evidence is ANOVA plus HIV-1 escape, not LOPO/Friedman or uniqueness.
- ch5: Mature narrowing discussion with excellent limitations; practical value rests mainly on HIV-1 plus 6/11 Layer C DMS coverage.

## Specialty deep-read
- ch4: The chapter is biologically convincing when it treats the scoring x pathogen interaction as the largest modeled component, with residual variance and small G=11 cluster limits kept visible. I also noted direct practical asymmetry: HIV-1 is the clean external vaccine-escape anchor, H3N2 is mostly self-consistency, SARS-CoV-2 is exploratory, and the 3-pathogen escape audit is explicitly availability-selected.
- ch5: The discussion correctly re-centers MutBench as retrospective wet-lab triage, not a deployable detector. Beyond Stage 1, I noticed the strongest computational-biology maturity is the separation of DMS functional validation (6/11, 650 positions, MCC 0.139--0.322) from antibody/vaccine escape validation, but the text still occasionally presents a cold-start recipe more operationally than the negative callability audits warrant.

## Scores
A: 8.6
B: 8.4
C: 8.3
D: 8.4
E: 8.5
F: 8.4
G: 7.9
H: 8.0
I: 9.0
J: 8.5
total: 84.0/100

## Rationale (per item, 2-3 sentences each, citing Stage 1 evidence + your specialty observations)

A. Problem statement: 8.6. The abstract/ch1 Stage 1 report shows an unusually clear and bounded problem: region-level single-position hotspot prioritization for retrospective wet-lab triage, with a concrete search-space reduction target. I deduct modestly because Stage 1 also flags residual "predicting variant emergence" / "might occur next" language in ch2 that can blur the non-deployment boundary.

B. Related work: 8.4. The ch2 Stage 1 report supports a strong score: the dissertation distinguishes MutBench from ProteinGym, EVEREST, ViroGym, surveillance, phylogenetic selection, and cancer hotspot work rather than flattening them. The ceiling is limited by compressed treatment of coupling-aware and epistatic methods and by some MutBench result material leaking into background.

C. Methodology: 8.3. Stage 1 ch3 and ch4 document a transparent pipeline: layered ground truth, 20 scoring types, 39 detector variants, MCC/F1/precision/recall, ANOVA, LOPO, Friedman, bootstrap, permutation, DMS and escape audits. I deduct for proxy implementations such as Tranception/ESM substitutions, incomplete Layer C threshold robustness, the homoplasy tree-source ambiguity, and the fact that many inferential lenses reuse the same 8,580-row dataset.

D. Scale: 8.4. The scale is good for this task: 11 RNA viruses across 8 ICTV families, 20 x 39 x 11 = 8,580 evaluations, 3,080 effective scoring-family-pathogen cells, 6/11 Layer C DMS pathogens, 73 temporal splits, and 2,340 escape enrichment evaluations. Computationally and biologically this is broad, but the independent pathogen cluster count remains only 11, Layer C is a bare majority, and escape validation covers only 3/11 pathogens by data availability.

E. Interpretation: 8.5. Stage 1 ch4/ch5 and my deep read show careful interpretation: uniqueness is explicitly null-consistent, LOPO 0/11 and Friedman p=0.990 are corroborative rather than independent positive evidence, and "largest source" is narrowed to "largest modeled component." Deductions come from local overstatements such as negative-MCC cells being "exactly" what pathogen-dependent optimality predicts and a ch4 DMS caption that overstates "independence" before the prose qualifies it.

F. Novelty/contribution: 8.4. The contribution is solid: a broad region-level viral hotspot benchmark, quantified pathogen-by-information interaction, and guarded wet-lab triage validation, rather than another per-variant VEP benchmark. It is not a deployable adaptive selector or a new biological law; novelty is strongest as empirical benchmarking and calibrated negative evidence at n=11.

G. Practical value: 7.9. Practical value is real for wet-lab triage: ch4/ch5 support approximate reduction from hundreds or ~1,000 positions to 10--50 candidates, HIV-1 7.19x escape enrichment with 82% Layer-A-disjoint positions, and Layer C functional validation in 6/11 pathogens. The main deduction is that forward-time performance is weak, 0/12 folds are callable under the abstention rule, H3N2 is mostly self-consistency, and the escape validation set is a 3-pathogen convenience sample.

H. Clarity: 8.0. Stage 1 reports credit the dissertation's ledgers, tables, caveats, and contribution hierarchy, and I agree that the audit-style structure helps expert readers. The writing is dense, abbreviation-heavy, and sometimes patched by footnotes or late caveats; denominator drift between 11 and 12 pathogens and category/count drift require attentive reading.

I. Limitations awareness: 9.0. Ch5 is especially strong: it names Layer A heterogeneity, lack of independent recuration, PLM leakage, Simpson's paradox, winner's curse, small n, prospective failure, dual-use risk, and MAFFT/source limitations. The dissertation also refuses deployment and states concrete gates for future callability, so the remaining deductions are for unresolved rather than hidden limitations.

J. Overall maturity: 8.5. Overall, this is a mature dissertation-level benchmark with reproducibility anchors, negative results retained, claim ledgers, and a disciplined shift from detector claims to wet-lab triage. I deduct for residual polish and consistency issues, one-team/one-codebase provenance, small-panel adaptive inference, and the fact that practical external validation is still asymmetric.

## Strongest single deduction
one-line: G, because practical triage is promising but still rests mainly on HIV-1 plus partial Layer C coverage while prospective deployment/callability fails; fix by adding an externally validated expanded panel with predeclared time-forward callability gates.

RESULT_PROF_V9_04: total=84.0/100 min_item=7.9(G) max_item=9.0(I) stage1_evidence_used=5
