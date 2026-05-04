# Professor 9: Statistical genetics (strictness=medium)

## Stage 1 reports consulted
- abstract_ch1: Strong bounded problem framing and contribution ledgers; residual prospective wording and incomplete Layer C integration into Chapter 1 remain.
- ch2: Broad, current related-work map with a defensible task distinction from VEP/DMS benchmarks; epistatic/coupling methods and forecasting-flavored language are the main weaknesses.
- ch3: Detailed, auditable methods and large grid; proxy channels, deferred checks, tree-source/category drift, and dense prose cap the score.
- ch4: Strong retrospective benchmark interpretation centered on the scoring x pathogen interaction; practical value is real but narrower than deployable prediction.
- ch5: Mature claim calibration and limitations matrix; denominator/numeric drift and defense-audit density reduce polish.

## Specialty deep-read
- ch3_methods: I verified the preregistered 20 x 39 x 11 grid, the 3,080-cell factor structure, Layer A/B/C contracts, and DMS availability for 6 pathogens. The methods are strong, but the homoplasy production description conflicts locally: one passage says IQ-TREE plus Fitch on the resulting ML tree, while the TreeTime audit note says Stage 2 production used Fitch on a FastTree ML approximation; Tranception and EVEscape are also explicitly proxies rather than original implementations.
- ch4_results: I verified the main interpretation: omega^2=0.296 is correctly framed as the largest modeled component, with cluster/wild/phylogenetic/Bayesian robustness and the 3,080-cell caveat. I also confirmed the guardrails: LOPO 0/11 and Friedman p=0.990 are null-consistent, MERS is treated as a failure case despite recall 1.0, and HIV-1 is the main external escape anchor.

## Scores
A: 8.6
B: 8.4
C: 8.0
D: 8.4
E: 8.4
F: 8.3
G: 7.8
H: 7.9
I: 9.0
J: 8.4
total: 83.2/100

## Rationale (per item, 2-3 sentences each, citing Stage 1 evidence + your specialty observations)

A. problem statement: 8.6  
Stage 1 abstract_ch1 reports an unusually explicit problem: region-level, single-position hotspot prioritization for retrospective wet-lab triage, narrowing roughly 1,000 residues to 10--50 candidates. The score is below 9 because Stage 1 ch2 and abstract_ch1 both flag residual forecasting wording ("predicting variant emergence", "might important mutations occur next") that slightly conflicts with the triage-only posture.

B. related work: 8.4  
Stage 1 ch2 finds broad and current coverage across frequency, entropy, phylogenetic, cancer-hotspot, DMS, PLM, VEP, and benchmark-methodology work, with a clear distinction from EVEREST, ProteinGym, and ViroGym. I deduct for compressed treatment of coupling/epistasis-aware models and some results leakage into background, but the task-boundary work is strong.

C. methodology: 8.0  
Stage 1 ch3 and ch4 support a strong methods score: the pipeline, ground-truth layers, metrics, preregistered grid, MCC rationale, and robustness frames are detailed and reproducible. My direct read confirms the statistical design is serious, but the score is capped by proxy scoring channels, deferred Layer C threshold sweeps for Rabies/EV-A71, no HMMER filtering, and the unresolved IQ-TREE/FastTree production homoplasy inconsistency.

D. scale (panel size, breadth): 8.4  
Stage 1 ch3/ch4 show substantial scale: 11 RNA viruses, 8 ICTV families, 20 scoring types, 39 detector variants, 8,580 evaluations, and 6-pathogen DMS Layer C. The statistical genetics deduction is that the real cluster count is still only 11 pathogens, external escape validation is 3/11 by availability, Layer C is 6/11, and the 12-pathogen Zika analyses must not be conflated with the main panel.

E. interpretation (results reading): 8.4  
Stage 1 ch4 and ch5 show commendable restraint: uniqueness and LOPO 0/11 are not treated as independent positive evidence, residual omega is acknowledged, and MERS saturation is explicitly called a failure case. My direct read confirms the load-bearing evidence is the scoring x pathogen interaction plus HIV-1 escape validation, but local overstatements remain, including "exactly what pathogen-dependent optimality predicts" for negative MCC cells and a Layer C caption that says differing winners "confirm" independence before the prose softens it.

F. novelty/contribution: 8.3  
Stage 1 abstract_ch1, ch4, and ch5 support a real contribution: a broad RNA-virus region-level benchmark, a quantified pathogen-by-information interaction, and a guarded wet-lab triage validation axis. The novelty is empirical and framing-based rather than a deployable new detector, and it depends on the constructed benchmark without disjoint pathogen-panel replication.

G. practical value (wet-lab triage utility): 7.8  
Stage 1 ch4/ch5 show useful triage value: Layer C DMS covers 6/11 pathogens, and HIV-1 vaccine escape gives a strong external anchor with 7.19x enrichment and 82% Layer-A-disjoint positions. The practical score is held under 8 because prospective transfer is weak, callability is 0/12 under the tested regime, H3N2 is mostly self-consistency, and the cold-start pipeline is a screening-budget allocator rather than a validated detector.

H. clarity (writing): 7.9  
Stage 1 reports credit the manuscript for evidence ledgers, self-contained tables, and explicit caveats. I agree, but chapter 3 and 4 are dense and sometimes source-audit-like; category counts, 11-vs-12 denominators, "Materials and Method", and repeated result summaries inside methods create avoidable reading load.

I. limitations awareness: 9.0  
Stage 1 ch5 gives the strongest evidence here: the manuscript openly discusses Layer A heterogeneity, weak prospective transfer, small n, label provenance, PLM leakage, dual-use release, MAFFT artifacts, and deployment abstention. The limitation treatment is unusually mature; deductions are only for unresolved items such as no independent recuration/inter-annotator agreement and incomplete sensitivity checks.

J. overall maturity: 8.4  
Across Stage 1 reports, the dissertation looks mature because it reports negative results, distinguishes retrospective triage from deployment, preserves reproducibility anchors, and avoids treating LOPO/Friedman as stronger than they are. The remaining maturity risks are the patched-feeling denominator drift, proxy-channel caveats, and a few headline/caption slips such as all-unique combinations despite the 10/11 parameter-tuple caveat.

## Strongest single deduction
one-line: G, because wet-lab triage utility is credible but still rests mainly on HIV-1 plus 6/11 DMS coverage while prospective/callability audits are negative; fix by adding independent residue-level escape/DMS validation for more pathogens under one fixed threshold pipeline.

RESULT_PROF_V9_09: total=83.2/100 min_item=7.8(G) max_item=9.0(I) stage1_evidence_used=5
