# Professor 3: Statistics/ML (strictness=high)

## Stage 1 reports consulted
- abstract_ch1: Strong bounded triage framing, clear problem/contribution ledgers, with minor residual prospective/cold-start wording drift.
- ch2: Current and task-aware related work, strongest on benchmark-gap positioning, weaker on compressed coupling/epistasis and unbenchmarked method families.
- ch3: Mature methodological scaffold with frozen thresholds, explicit Layer A/B/C separation, and large 8,580-cell design, but dense prose, deferred sensitivities, and dependent channels.
- ch4: Strong statistically audited results chapter; ANOVA/HIV-1 are load-bearing, while LOPO/Friedman and uniqueness are correctly demoted but still easy to over-read.
- ch5: Mature limitations and interpretation chapter that preserves non-deployability, though denominator drift and dense audit/wave prose remain.

## Specialty deep-read
- ch3_methods: Beyond Stage 1, I verified that the methods explicitly distinguish evaluation-level 8,580 rows from the 3,080 cell-level grid, acknowledge detector-variant dependence, and give a conservative cell-level omega-squared reference. I also confirmed the Tranception channel is an ESM-2 proxy with high correlation to ESM-2 for 11/12 pathogens, so the 20 scoring types are not fully independent.
- ch4_results: Beyond Stage 1, I verified that the chapter now treats LOPO 0/11 and Friedman p=0.990 as failures-to-reject rather than positive proof, and that the 0.265 LOPO gap is not statistically distinguishable from the random-combination null. I also confirmed the HIV-1 vaccine-escape anchor is strong and mostly Layer-A-disjoint, while H3N2/SARS-CoV-2 are appropriately downgraded.

## Scores
A: 8.5
B: 8.3
C: 8.2
D: 8.5
E: 8.4
F: 8.1
G: 7.6
H: 8.0
I: 9.0
J: 8.3
total: 82.9/100

## Rationale (per item, 2-3 sentences each, citing Stage 1 evidence + your specialty observations)

A. problem statement: 8.5. Stage 1 abstract/ch1 finds a clear, bounded problem: lack of a standardized region-level hotspot benchmark, independent ground truth, and evidence on pathogen-dependent information sources. I deduct slightly because Stage 1 also flags lingering phrases such as "might important mutations occur next," "practical impact," and "cold-start recipe," which can pull the reader back toward prospective detector expectations.

B. related work: 8.3. Stage 1 ch2 shows strong separation among surveillance, VEP benchmarks, selection tests, cancer hotspot work, and MutBench's single-position region-level detection task. The deduction is for compressed treatment of coupling/epistasis-aware approaches and the fact that several method families are reviewed but not benchmarked, leaving the literature bridge narrower than the breadth claim may imply.

C. methodology: 8.2. Stage 1 ch3/ch4 support a strong methodology: frozen Layer A/B/C thresholds, 20 scoring types, 39 detector variants, MCC primary evaluation, ANOVA with cluster-aware robustness, and explicit Layer A/C conflict handling. My deep read confirms good dependence awareness, but strict ML grading must penalize the dependent detector variants, the ESM-2/Tranception proxy collinearity, deferred merged-channel and structural QC sensitivities, and the small 11-cluster inferential base.

D. scale (panel size, breadth): 8.5. Stage 1 ch3/ch4 document substantial scale: 11 RNA viruses, 8 ICTV families, 8,580 evaluations, 73 temporal splits, 6 DMS pathogens, and 3 escape-validation pathogens. The benchmark is broad for a dissertation, but not broad enough for adaptive weighting, and the scale is heterogeneous because Layer C is 6/11, vaccine escape is 3/11, and the later feature/audit panel shifts to 12 pathogens with Zika.

E. interpretation (results reading): 8.4. Stage 1 ch4/ch5 correctly identify omega-squared and HIV-1 as load-bearing while demoting 11/11 uniqueness, LOPO 0/11, and Friedman p=0.990. My deep read confirms the manuscript explicitly says the LOPO gap is null-consistent, but I deduct for remaining local overstatements: negative-MCC cells are "exactly" what pathogen-dependent optimality predicts, and the Layer C divergence paragraph speculates that more ground truths would only reinforce heterogeneity.

F. novelty/contribution: 8.1. Stage 1 supports novelty as a benchmark-and-audit contribution: broad region-level RNA-virus hotspot benchmarking plus a quantified scoring-by-pathogen interaction. It is less novel as an algorithmic contribution because pathogen heterogeneity is biologically unsurprising, cold-start/adaptive selection fails at n=11, and the 4-core is explicitly a historical fixed configuration rather than an optimum.

G. practical value (wet-lab triage utility): 7.6. Stage 1 ch4/ch5 identify real triage value: HIV-1 escape enrichment of 7.19x, 82% Layer-A-disjoint positions, and a plausible reduction from hundreds or roughly 1,000 positions to 10-50 candidates. The deduction is the largest because practical validation rests mainly on one external anchor, the reported top results are partly oracle/post-hoc best-combination envelopes, vaccine escape covers only 3/11 pathogens, and the cold-start algorithm is formally abstained from deployment.

H. clarity (writing): 8.0. Stage 1 reports praise the ledgers, tables, and repeated guardrails, and the source chapters are unusually auditable. I deduct for density, result leakage into methods/background, legacy labels such as 9-pathogen anchors, denominator shifts between 11 and 12 pathogens, and figure/table language that occasionally says more than the fine print.

I. limitations awareness: 9.0. Stage 1 ch5 gives unusually explicit limitations: Layer A heterogeneity, weak forward-time performance, small panel, PLM leakage, sampling bias, dual use, no calibrated detector claim, and deployment abstention. This is the strongest item; remaining deductions are for unresolved limitations rather than undisclosed ones, especially no independent Layer A recuration and unquantified alignment/structural-quality sensitivities.

J. overall maturity: 8.3. The manuscript is statistically mature in its self-correction: it preserves the triage frame, reports negative/null results, distinguishes independent validation from self-consistency, and uses robustness frames for the omega-squared claim. Strictly, it still reads like a late-stage audit integration in places, with denominator drift, dense caveat layering, and a main positive practical claim that is narrower than the full 11-pathogen benchmark.

## Strongest single deduction
one-line: G, because wet-lab triage utility is real but rests mainly on HIV-1 plus limited 3/11 escape validation; fix by adding independent residue-level escape or DMS-style external anchors for more pathogens under a fixed non-oracle protocol.

RESULT_PROF_V8_03: total=82.9/100 min_item=7.6(G) max_item=9.0(I) stage1_evidence_used=5
