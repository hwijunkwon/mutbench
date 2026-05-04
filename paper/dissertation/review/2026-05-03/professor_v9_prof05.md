# Professor 5: Virology/public health (strictness=medium)

## Stage 1 reports consulted
- abstract_ch1: Strong bounded problem and contribution framing; remaining risk is prospective-sounding language around variant emergence and cold-start use.
- ch2: Broad, current related-work positioning; strongest on task distinction from VEP/surveillance benchmarks, weaker on epistasis/coupling depth.
- ch3: Detailed and auditable methods with strong scale; deductions for proxy channels, deferred checks, and tree/source/category labeling drift.
- ch4: Mature retrospective benchmark and interpretation; practical value is real but bounded by weak prospective/callability results and HIV-1-heavy external anchoring.
- ch5: Strongest claim-calibration and limitations chapter; excellent deployment boundaries, with some denominator/numeric drift and audit-memo density.

## Specialty deep-read
- ch4: The HIV-1 vaccine-escape row is the most convincing public-health relevance signal: 7.19x enrichment, 82% Layer-A-disjoint escape set, and novel-only Bonferroni significance. H3N2 is explicitly self-consistency after Layer-A overlap, SARS-CoV-2 is exploratory after correction, and the 73-window prospective backtest is near chance overall, so the chapter supports retrospective wet-lab triage rather than surveillance deployment.
- ch5: The limitations section is unusually candid for virology/public health use: it names forward-time failure, 0/12 callability, dual-use release constraints, label heterogeneity, and no independent recuration. I also noticed the practical workflow still reads fairly operational for novel pathogens, but the recommended-use paragraph correctly restricts today’s use to retrospective prioritization with abstention status.

## Scores
A: 8.6
B: 8.4
C: 8.2
D: 8.5
E: 8.4
F: 8.3
G: 7.8
H: 7.9
I: 9.1
J: 8.5
total: 83.7/100

## Rationale (per item, 2-3 sentences each, citing Stage 1 evidence + your specialty observations)

A. problem statement: 8.6  
Stage 1 abstract/ch1 finds a precise problem: region-level single-position hotspot prioritization for retrospective wet-lab triage, with the concrete experimental-economics target of narrowing roughly 1,000 positions to 10--50. I agree this is strong and unusually bounded; the deduction is for residual forecasting language in ch2 and some operational "novel RNA virus" workflow language in ch5 that could over-activate public-health deployment expectations.

B. related work: 8.4  
Stage 1 ch2 reports broad coverage across frequency, entropy, cancer hotspot tools, phylogenetic selection, DMS, PLMs, surveillance platforms, and adjacent VEP benchmarks. The task distinction from ViroGym/EVEREST/ProteinGym is well handled, but coupling-aware and epistatic methods are thinly reviewed, which matters for viral escape biology where residue interactions can dominate phenotype.

C. methodology: 8.2  
Stage 1 ch3 and ch4 show an auditable pipeline: three-layer ground truth, 20 scoring types, 39 detector variants, MCC-centered evaluation, ANOVA/LOPO/Friedman/bootstrap/permutation checks, and clear proxy-channel caveats. I deduct for proxy implementations such as Tranception/ESM substitutions, deferred DMS threshold checks for some pathogens, homoplasy tree-source ambiguity, and limited independence because several statistical lenses reuse the same 8,580-row grid.

D. scale (panel size, breadth): 8.5  
The 11-virus, 8-family, multi-transmission-route panel and 8,580 evaluation cells are strong for a doctoral benchmark, as Stage 1 ch3/ch4 emphasize. Scale is still statistically small for cluster inference and public-health generalization: external escape validation covers 3/11 pathogens, Layer C covers 6/11, and feature/callability audits drift to 12 with Zika, which complicates the clean denominator.

E. interpretation (results reading): 8.4  
Stage 1 ch4/ch5 repeatedly notes mature interpretation: LOPO 0/11 and Friedman p=0.990 are treated as null-consistent corroboration, not independent proof, and "largest source" is narrowed to largest modeled component. My direct read confirms this discipline, including explicit MERS failure-case wording and HIV-1-vs-H3N2 evidence tiering; deductions remain for occasional stronger captions or phrases such as "confirming independence" for Layer C and "exactly what pathogen-dependent optimality predicts."

F. novelty/contribution: 8.3  
The contribution is credible as a benchmark/statistical/triage contribution: broad RNA-virus region-level hotspot benchmark, quantified scoring-by-pathogen interaction, and guarded wet-lab validation. It is not a new deployable surveillance detector or mechanistic virology discovery engine, and some novelty depends on internal benchmark construction without an independent disjoint pathogen-panel replication.

G. practical value (wet-lab triage utility): 7.8  
For wet-lab triage, the work has real value: Layer C DMS validation spans 6/11 pathogens and 650 positions, HIV-1 gives a strong largely disjoint vaccine-escape anchor, and the framework can reduce screening budgets to candidate lists. The public-health deduction is substantial because practical value rests mainly on HIV-1 for independent escape validation, H3N2 is mostly self-consistency, SARS-CoV-2 is exploratory, prospective backtests are weak, and the cold-start algorithm is formally abstained from deployment at 0/12 callable folds.

H. clarity (writing): 7.9  
Stage 1 reports consistently find strong audit ledgers, self-contained tables, and explicit boundaries, but also dense prose, many stage/wave/layer labels, and some denominator/category drift. My specialty read found the same: the ch5 limitations matrix is excellent, while the workflow/audit paragraphs are hard to parse and can obscure the core virology message under many branch labels and archival details.

I. limitations awareness: 9.1  
This is the strongest item. Stage 1 ch5 identifies an unusually comprehensive limitations matrix covering sampling bias, temporal dependence, PLM leakage, Simpson's paradox, winner's curse, small n, independent reproduction, label heterogeneity, sub-lineage pooling, prospective gap, dual use, and MAFFT artifacts; my direct read confirms the forward-time and dual-use limits are not buried. Remaining deductions are for unresolved limitations, especially no independent recuration/inter-annotator agreement, unquantified MAFFT-mode sensitivity, and repeated 11/12 denominator drift.

J. overall maturity: 8.5  
The dissertation reads as mature because it reports negative results, refuses deployment, distinguishes evidence tiers, preserves code/data provenance, and avoids turning weak LOPO/callability into a claim. Maturity is not perfect because the document still feels patched in places after compression, with stale numeric anchors and audit-heavy paragraphs, and because independent external validation remains asymmetric.

## Strongest single deduction
one-line: G, practical value is bounded by HIV-1-heavy external validation plus weak prospective/callability evidence; fix by adding balanced, residue-level escape/DMS validation and time-forward callable evaluation across more pathogens.

RESULT_PROF_V9_05: total=83.7/100 min_item=7.8(G) max_item=9.1(I) stage1_evidence_used=5
