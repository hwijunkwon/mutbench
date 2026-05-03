# Professor 7: Benchmark methodology (strictness=medium)

## Stage 1 reports consulted
- abstract_ch1: Strong bounded problem frame around retrospective wet-lab triage, with minor residual prospective wording in figures/related-work phrasing.
- ch2: Strong task-aware related work separating MutBench from VEP, surveillance, and selection-test benchmarks, but compressed coverage of coupling/epistasis families.
- ch3: Methodology is auditable and broad, with preregistered thresholds/grid and explicit layer roles; weaknesses are dense prose, legacy labels, and uneven Layer C coverage.
- ch4: Results are statistically mature around omega, LOPO, Friedman, and escape validation, but practical claims depend on narrow anchors and some local overstrong phrasing.
- ch5: Discussion gives unusually strong limitations and deployment refusal, while denominator drift between 11- and 12-pathogen scopes remains a readability risk.

## Specialty deep-read
- ch3_methods: Beyond Stage 1, I found the benchmark contract especially strong: Layer A/B/C roles are separated, thresholds and the ANOVA grid are frozen, and cell-level versus evaluation-level omega is explicitly distinguished. I also confirmed methodology polish issues: old `9pathogen` labels, MAFFT `--auto` not ablated, result-like claims inside methods, and a "Tranception" channel that is really an ESM-2 masked-marginal proxy for most practical purposes.
- ch4_results: Beyond Stage 1, I confirmed that the load-bearing statistical evidence is the scoring x pathogen interaction with robustness frames, not 11/11 uniqueness, LOPO 0/11, or Friedman. I also confirmed the practical-value ceiling: HIV-1 is the only strong external escape anchor, H3N2 is mainly self-consistency, SARS-CoV-2 is exploratory, and cold-start/adaptive weighting is formally not deployable under the tested regime.

## Scores
A: 8.6
B: 8.4
C: 8.4
D: 8.5
E: 8.4
F: 8.2
G: 7.7
H: 8.0
I: 9.0
J: 8.5
total: 83.7/100

## Rationale (per item, 2-3 sentences each, citing Stage 1 evidence + your specialty observations)

A. The problem statement is clear and disciplined: Stage 1 abstract/ch1 notes the computational niche between sequence collection and experimental validation, plus the explicit "wet-lab triage rather than prospective deployment" framing. I deduct modestly because Stage 1 also found residual prospective phrasing such as "might important mutations occur next," "Practical Impact," and "cold-start recipe," which can blur the non-deployable claim.

B. Related work is strong for benchmark positioning: Stage 1 ch2 shows a clear distinction from surveillance tools, VEP benchmarks, cancer hotspot methods, and HyPhy-style selection tests. The score is not higher because coverage of coupling-aware/epistasis-aware methods is acknowledged but not deeply integrated, and some result leakage into Chapter 2 makes the background feel partly retrospective.

C. Methodology is a central strength. Stage 1 ch3 and my direct read confirm a large, auditable design: three-layer ground truth, 20 scoring types, 14 detection families, 39 variants, MCC as headline metric, preregistered thresholds/grid, and cluster-aware omega interpretation. Deductions come from uneven DMS coverage, partially redundant AI/PLM scoring channels, unablated MAFFT and structural-QC choices, result-heavy methods prose, and the small effective pathogen cluster count.

D. Scale is good for a dissertation benchmark: Stage 1 ch3/ch4 documents 11 RNA viruses, 8,580 evaluation cells, 73 temporal splits, broad sequence counts, 8 ICTV families, and 6/11 Layer C DMS pathogens. It is not an all-virus or all-protein benchmark, Layer C and escape validation are uneven, Zika appears only in the 12-pathogen feature/audit scope, and n=11 remains too small for adaptive selection.

E. Interpretation is mature. Stage 1 ch4/ch5 emphasizes that the dissertation correctly demotes 11/11 uniqueness, treats LOPO/Friedman as same-data checks rather than independent proof, discloses negative-MCC cells, and makes low MCC intelligible under class imbalance. I deduct for occasional overstrong local wording in ch4, such as negative cells being "exactly" what pathogen-dependent optimality predicts and a DMS caption implying independence more strongly than the evidence warrants.

F. Novelty is strong but scoped. Stage 1 abstract/ch1/ch4/ch5 support novelty as a broad region-level single-position RNA-virus hotspot benchmark plus quantified pathogen-by-information interaction, not as a deployable prediction algorithm. The deduction reflects that "different pathogens favor different methods" is biologically plausible rather than surprising, the "broadest" claim depends on a narrow task boundary, and the cold-start 4-core is a retained heuristic rather than an optimized contribution.

G. Practical value is real but narrower than the methodological contribution. Stage 1 ch4/ch5 and my direct read show a concrete triage story: Layer C DMS on 6/11 pathogens, HIV-1 escape enrichment at 7.19x with mostly Layer-A-disjoint positions, and candidate reduction from roughly 1,000 positions to about 10-50. The score is capped because external escape validation covers only 3/11 pathogens, HIV-1 carries most independent weight, the strongest search-space claims use optimal/post-hoc combinations, and cold-start callability is 0/11 or 0/12 under tested gates.

H. Clarity is good at the level of ledgers, tables, and claim boundaries. Stage 1 reports repeatedly note that the manuscript uses evidence ledgers, layer tables, and limitation matrices to control interpretation. I deduct because the prose is dense, many audit/wave labels are compressed, old `9pathogen` labels persist in ch3, result claims appear inside methods/background, and 11-vs-12 denominator shifts require close attention.

I. Limitations awareness is excellent. Stage 1 ch5 documents a broad limitations matrix covering Layer A heterogeneity, forward-time weakness, PLM leakage, Simpson's paradox, winner's curse, small panel size, prospective gap, dual-use, and MAFFT artifacts. The manuscript also explicitly refuses deployment and reports failed adaptive weighting, HBFWS, Cycle 7B, Layer A' substitution, and callable-subset gates; the remaining deduction is that several limitations are disclosed rather than resolved.

J. Overall maturity is high. Stage 1 abstract/ch1/ch5 shows mature evidence hierarchy: 11-pathogen main panel, 6-pathogen DMS Layer C, HIV-1 primary external anchor, H3N2 self-consistency, SARS-CoV-2 exploratory, and no prospective detector claim. I withhold a higher score because the manuscript still shows late-cycle patching artifacts, denominator drift, dense audit appendages in the main narrative, and dependence on a small cluster count for its central benchmark inference.

## Strongest single deduction
one-line: G, because practical wet-lab triage value is promising but rests on limited external validation and oracle/post-hoc best-combination evidence; fix by adding balanced independent escape/DMS validation for more pathogens under a fixed pre-specified triage protocol.

RESULT_PROF_V8_07: total=83.7/100 min_item=7.7(G) max_item=9.0(I) stage1_evidence_used=5
