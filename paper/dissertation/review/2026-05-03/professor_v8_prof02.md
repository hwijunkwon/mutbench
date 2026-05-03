# Professor 2: Advisor, computer science (strictness=medium)

## Stage 1 reports consulted
- abstract_ch1: Strong problem framing and contribution hierarchy, with small residual prospective wording and figure/cold-start tensions.
- ch2: Current and well-scoped related work distinguishes hotspot triage from surveillance and VEP benchmarks, but leaves coupling/epistasis methods outside scope.
- ch3: Methodological scaffold is auditable and broad, with preregistered grids and layer separation, but dense prose and some deferred sensitivities.
- ch4: Results are statistically mature, especially on the scoring-by-pathogen interaction, while practical validation is narrow and partly oracle/post-hoc.
- ch5: Discussion strongly calibrates claims and limitations, but denominator drift between 11- and 12-pathogen analyses remains a clarity risk.

## Specialty deep-read
- abstract+ch1: The abstract explicitly says retrospective wet-lab triage rather than prospective deployment, and Chapter 1 repeats the 11-pathogen headline boundary. I also saw residual language such as "Practical Impact" and "practical cold-start recipe" that could invite a more deployable reading than intended.
- ch3: The methods chapter directly supports the Stage 1 assessment: the 20 scoring types, 14 families, 39 variants, 8,580 evaluations, and Layer A/B/C roles are clear. However, legacy labels such as `9pathogen`, very long method-ledger paragraphs, and deferred MAFFT/DMS/PLM sensitivities visibly reduce polish.
- ch5: The discussion is unusually strong on claim calibration: it names forward-time weakness, 0/12 callability, Layer A heterogeneity, and dual-use constraints. The chapter also reads like a compressed defense memo in places, and the 11/12 denominator shifts require careful attention.

## Scores
A: 8.6
B: 8.4
C: 8.4
D: 8.6
E: 8.5
F: 8.3
G: 7.8
H: 8.0
I: 9.1
J: 8.6
total: 84.3/100

## Rationale (per item, 2-3 sentences each, citing Stage 1 evidence + your specialty observations)

A. problem statement: 8.6  
Stage 1 abstract_ch1 finds a clear non-deployable problem frame: standardized evaluation, independent ground truth, and pathogen-dependent method choice are stated as concrete gaps. My direct read confirms that the abstract and introduction consistently position MutBench between sequence collection and experimental validation, but the few prospective phrases in Chapter 1 and Chapter 2 slightly weaken the guardrail.

B. related work: 8.4  
Stage 1 ch2 shows strong related-work positioning: surveillance, VEP benchmarks, selection tests, cancer precedents, and viral hotspot detection are separated rather than conflated. The deduction is for compressed treatment of some modern coupling/epistasis and structure-aware methods, plus result leakage into the background that makes the literature chapter feel somewhat retrospective.

C. methodology: 8.4  
Stage 1 ch3 and ch4 support a high score because the methodological contract is explicit: Layer A for positives, Layer B for constrained negatives, Layer C for DMS validation, frozen grids, MCC, ANOVA, Friedman, and LOPO. My direct read confirms that this is technically serious, but deferred sensitivities for MAFFT mode, some DMS thresholds, structural QC, and correlated PLM/proxy channels keep it below excellent.

D. scale (panel size, breadth): 8.6  
Stage 1 ch3 and ch4 document real scale: 11 RNA viruses, diverse surface glycoproteins, 20 scoring formulas, 39 detector variants, and 8,580 evaluations, plus 73 temporal splits and 6-pathogen DMS validation. The deduction is that the scale is broad for a dissertation but still biologically bounded to RNA-virus surface proteins, with uneven Layer C/B depth and insufficient n=11 for adaptive selector learning.

E. interpretation (results reading): 8.5  
Stage 1 ch4 and ch5 emphasize mature interpretation: the 11/11 uniqueness result is demoted, LOPO/Friedman are not oversold, and low MCC is explained through exact-position stringency and class imbalance. My Chapter 5 read confirms this calibration, though local phrases such as "confirming independence" for Layer C and "exactly what pathogen-dependent optimality predicts" remain somewhat stronger than the evidence.

F. novelty/contribution: 8.3  
Stage 1 reports support novelty as a benchmark-and-audit contribution: region-level single-position hotspot benchmarking across RNA viruses plus a quantified scoring-by-pathogen interaction. This is less an algorithmic breakthrough than a well-scoped evaluation contribution, and the cold-start 4-core is explicitly not an optimum, so I score novelty high but not exceptional.

G. practical value (wet-lab triage utility): 7.8  
Stage 1 ch4 and ch5 identify the strongest practical evidence: search-space reduction to roughly 10-50 positions, Layer C DMS validation for 6/11 pathogens, and HIV-1 escape enrichment with substantial Layer-A-disjoint support. The score is lower because the cleanest external anchor is mostly HIV-1, H3N2 is self-consistency-heavy, SARS-CoV-2 is exploratory, and cold-start/callability audits refuse deployment.

H. clarity (writing): 8.0  
Stage 1 reports note that ledgers, tables, and boundary statements make the manuscript unusually auditable. My direct reads agree, but the manuscript is dense, uses many stage/layer/wave acronyms, preserves legacy labels, and sometimes shifts between 11- and 12-pathogen denominators in ways that will burden non-specialist readers.

I. limitations awareness: 9.1  
Stage 1 ch5 gives the strongest evidence here: Layer A heterogeneity, small panel size, forward-time weakness, PLM leakage, winner's curse, independent reproduction, scope boundaries, dual-use, and MAFFT artifacts are all explicitly disclosed. My direct read confirms that limitations are not decorative; they actively constrain the recommendation to retrospective triage and refuse prospective detector claims.

J. overall maturity: 8.6  
Across Stage 1 reports, the manuscript shows mature scientific behavior: it reports negative audits, separates evidence tiers, limits LOPO/Friedman interpretation, and preserves reproducibility anchors. The remaining maturity deductions come from late-stage compression artifacts, denominator drift, and a few pieces of over-actionable language around cold-start use.

## Strongest single deduction
one-line: G, practical value is real for wet-lab triage but rests too heavily on HIV-1 and post-hoc/oracle-framed enrichment; fix by adding prospective or independently held-out wet-lab validation across more pathogens.

RESULT_PROF_V8_02: total=84.3/100 min_item=7.8(G) max_item=9.1(I) stage1_evidence_used=5
