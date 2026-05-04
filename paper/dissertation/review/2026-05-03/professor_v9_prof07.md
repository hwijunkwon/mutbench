# Professor 7: Benchmark methodology (strictness=medium)

## Stage 1 reports consulted
- abstract_ch1: Strong bounded problem and contribution framing, with residual prospective-sounding phrases and dense audit-style presentation.
- ch2: Broad and current related-work positioning; strongest on task-boundary distinction from VEP/surveillance/cancer benchmarks, weaker on epistatic/coupling methods.
- ch3: Detailed, auditable methodology and scale; deductions for proxy channels, deferred checks, homoplasy tree-source ambiguity, and label/category drift.
- ch4: Mature retrospective benchmark interpretation with strong ANOVA/escape evidence; deductions for same-data statistical lenses, weak prospective transfer, and uniqueness/headline slips.
- ch5: Strong limitations and claim calibration; practical value is narrowed appropriately to retrospective wet-lab triage, with HIV-1 as the main external anchor.

## Specialty deep-read
- ch3: The preregistration paragraph is a methodological strength: Layer A/B/C thresholds, the 20 x 39 grid, the 3,080 cell factor structure, and the vaccine-escape Bonferroni denominator are explicitly frozen. Direct reading also confirmed that Layer C is genuinely integrated as a separate DMS axis, but only 4/6 DMS threshold sweeps are complete; ch3 also still reports a stale cell-level 0.234 in places while ch4 now uses 0.233, and the opening/category labels remain mildly unsynchronized.
- ch4: The best part is not the 8,580-row headline itself but the careful interpretation around it: MCC is justified, LOPO 0/11 and Friedman p=0.990 are explicitly null-consistent, and the cluster/bootstrap robustness is framed as same-data triangulation. Direct reading confirmed a local overstatement in the opening/table caption that all 11 best combinations are unique, while the footnote correctly says Influenza B and MERS share freq + KDE p=85 at the parameter-variant level.

## Scores
A: 8.6
B: 8.4
C: 8.3
D: 8.4
E: 8.5
F: 8.3
G: 7.9
H: 7.9
I: 9.0
J: 8.4
total: 83.7/100

## Rationale (per item, 2-3 sentences each, citing Stage 1 evidence + your specialty observations)

A. problem statement: The abstract/ch1 Stage 1 report shows a precise problem: region-level single-position hotspot prioritization for retrospective wet-lab triage, including the practical reduction from about 1,000 positions to 10--50 candidates. The problem is better than merely adequate because it names three gaps: standardized evaluation, independent ground truth, and pathogen-dependent method behavior. I deduct for residual forecasting language in ch2 ("predicting variant emergence," "might important mutations occur next") that softens the otherwise clean non-deployment boundary.

B. related work: Ch2 Stage 1 reports strong breadth across frequency, entropy, phylogenetic selection, homoplasy, DMS, PLMs, surveillance, VEP, cancer hotspot tools, and benchmarking methodology. The dissertation makes the crucial distinction that ProteinGym/EVEREST/ViroGym are per-variant fitness or escape benchmarks, not region-level hotspot-detection benchmarks. The ceiling is limited by compressed coverage of coupling/epistasis-aware methods and by occasional results leakage into the background.

C. methodology: Ch3 and ch4 provide a strong methodological contract: three-layer ground truth, 20 scoring types, 39 detector variants, MCC as primary Stage 2 metric, ANOVA effect-size decomposition, LOPO, Friedman, permutation, and cluster-aware robustness. Direct ch3 reading confirms unusually useful preregistration of thresholds and grid structure, plus explicit separation of Layer A MCC, Layer B constrained FPR, and Layer C DMS F1. Deductions come from proxy implementations for Tranception/EVEscape, incomplete 6-pathogen DMS threshold robustness, the IQ-TREE/FastTree homoplasy ambiguity flagged by Stage 1, and small stale numeric anchors.

D. scale: The benchmark is broad for this task: 11 RNA viruses, 8 ICTV families, four transmission routes, 20 scoring types, 14 detector families, 39 parameter variants, 8,580 evaluations, 3,080 scoring-family-pathogen cells, 6 DMS pathogens, and 3 escape-validation pathogens. Ch3 documents real sequence scale and per-pathogen query dates; ch4 adds 73 temporal splits and 2,340 escape enrichment evaluations. I deduct because the effective statistical cluster count remains only 11, Layer C covers 6/11, escape validation covers 3/11 by convenience, and Zika creates recurring 11-vs-12 scope drift.

E. interpretation: Ch4 and ch5 are careful where it matters: the load-bearing positive evidence is the scoring x pathogen interaction, not LOPO 0/11, Friedman, or all-unique best combinations. The discussion also correctly reads low MCC in light of exact-position scoring, imbalance, and ground-truth stringency. Deductions are for local overstatements: "exactly what pathogen-dependent optimality predicts" for negative MCC cells and the DMS caption's too-strong "confirming independence" language.

F. novelty/contribution: The contribution is solid as a benchmark-methodology and empirical-statistical contribution: a broad region-level hotspot benchmark, quantified pathogen-by-information interaction, and guarded wet-lab triage validation. Stage 1 reports support the novelty through the 8,580-cell design, omega-squared 0.296 with cluster-bootstrap CI, 9 distinct optimal scoring types, and the HIV-1 escape anchor. It is not a new deployable detector or a definitive universal biology result, so I keep it in the low-eights rather than excellent-plus.

G. practical value: Practical value is real but bounded: the work operationalizes wet-lab triage as search-space reduction, with HIV-1 showing 7.19x escape enrichment, 82% Layer-A-disjoint escape positions, and strong novel-only significance. Ch5 adds Layer C DMS validation across 6/11 pathogens and the candidate-list framing of roughly 10--50 positions. The deduction is substantial because prospective transfer is weak, 0/12 folds are callable for deployment, H3N2 is mostly self-consistency, and SARS-CoV-2 is exploratory.

H. clarity: The manuscript uses ledgers, tables, captions, and audit statements well; Stage 1 repeatedly notes that caveats are visible rather than hidden. Ch3/ch4 are especially clear about effective units, MCC choice, and evidence hierarchy once read carefully. The writing is still dense, acronym-heavy, and occasionally patched: "Materials and Method," repeated information-type sentences in ch4, category drift, and headline/footnote tension create reading friction.

I. limitations awareness: This is the strongest item. Ch5's limitations matrix directly names Layer A heterogeneity, poor forward-time transfer, small n, PLM leakage, winner's curse, sampling bias, MAFFT artifacts, dual-use constraints, reproduction, and deployment boundaries. Ch4 and ch3 also disclose negative prospective backtests, failed adaptive weighting, incomplete DMS sweeps, HCV Layer B caveats, and non-independence of the 8,580 rows. The only reason this is not higher is that some limitations remain unresolved rather than merely acknowledged.

J. overall maturity: The work is mature in benchmark-methodology terms: it refuses deployment, separates retrospective triage from prospective prediction, preserves primary-vs-secondary evidence hierarchy, reports negative audits, and treats LOPO/Friedman as weak corroboration. Direct ch4 reading confirms the important statistical humility that the three lenses are consistency checks on the same data, not independent replication. Remaining maturity deductions come from scope/numeric drift, proxy methods, small cluster count, and a few headline statements that are more aggressive than their own footnotes.

## Strongest single deduction
one-line: G, because practical wet-lab triage is useful but still rests mainly on retrospective/HIV-1 evidence while prospective callability is 0/12; fix by adding a pre-registered forward-time wet-lab or escape-validation panel beyond HIV-1.

RESULT_PROF_V9_07: total=83.7/100 min_item=7.9(G) max_item=9.0(I) stage1_evidence_used=5
