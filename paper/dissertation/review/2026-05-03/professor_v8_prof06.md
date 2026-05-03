# Professor 6: VEP/PLM expert (strictness=highest)

## Stage 1 reports consulted
- abstract_ch1: Strong bounded framing as retrospective wet-lab triage, but residual prospective/cold-start wording and figure phrasing still tug toward detector claims.
- ch2: Strong task-aware related work distinguishing MutBench from VEP/surveillance benchmarks, with compressed PLM/coupling-aware coverage and some result leakage.
- ch3: Mature methods scaffold with frozen thresholds, layer separation, and 8,580-cell design, but uneven DMS coverage, redundant PLM channels, and legacy/deployability wording remain.
- ch4: Strong audited results chapter; load-bearing evidence is scoring x pathogen omega^2 and HIV-1 escape, while LOPO/uniqueness/cold-start should be read cautiously.
- ch5: Mature discussion and limitations; practical value is well reframed as triage, but denominator drift and cold-start non-deployability require strict attention.

## Specialty deep-read
- ch3_methods: The Layer A/B/C separation is real and useful, especially the explicit A/C conflict rule, but Layer C is only 6/11 and the DMS threshold sweep is only complete for 4/6. The VEP/PLM channel naming is a weakness: the "Tranception" channel is an ESM-2 masked-marginal pseudo-perplexity proxy, so the AI-based category is less independent than its 20-channel count suggests.
- ch4_results: The best VEP/PLM signals are pathogen-specific rather than generally strong: Tranception/ESM-2 help SARS-CoV-2/RSV but underperform or invert elsewhere, and ESM-2 contributes negatively in the 12-pathogen Shapley audit. The HIV-1 7.19x escape enrichment is the cleanest practical anchor; H3N2 is mostly self-consistency and SARS-CoV-2 is exploratory after correction.
- ch5_discussion: The discussion is unusually candid about PLM leakage/proxy collinearity, winner's curse, and 0/12 callability. However, the 4-feature cold-start core is explicitly historical and dominated by a 3-core, so it cannot be treated as a novel optimized VEP-style selector.

## Scores
A: 8.5
B: 8.1
C: 8.3
D: 8.0
E: 8.4
F: 7.8
G: 7.5
H: 7.8
I: 9.0
J: 8.3
total: 81.7/100

## Rationale (per item, 2-3 sentences each, citing Stage 1 evidence + your specialty observations)

A. problem statement: 8.5. Stage 1 abstract_ch1 shows the problem is clear: standardized viral hotspot evaluation, independent ground truth, and pathogen-dependent method choice, all bounded to retrospective wet-lab triage. I deduct because ch2/ch3 still contain "might occur next," "surveillance," and "deployability" residues that can reopen a prospective-detector expectation.

B. related work: 8.1. Stage 1 ch2 gives strong boundary work versus ProteinGym, EVEREST, ViroGym, Nextstrain/PANGO, cancer hotspot tools, HyPhy, and surveillance; this is the right comparator logic for a region-level single-position benchmark. As a VEP/PLM reader, I find the PLM, epistasis/coupling-aware, and structure-aware history too compressed, and the benchmark excludes DCA/EVcouplings-like regimes that matter for modern VEP context.

C. methodology: 8.3. Stage 1 ch3 and ch4 document an auditable design: frozen Layer A/B/C thresholds, 20 scoring types, 39 detector variants, MCC primary metric, ANOVA/LOPO/Friedman, and cluster/phylogenetic robustness. Direct reading confirms serious care, but the PLM channel dependence, incomplete DMS threshold sweeps for Rabies/EV-A71, MAFFT non-ablation, and uneven label provenance prevent a higher score.

D. scale (panel size, breadth): 8.0. The 11-pathogen, 8-family, 8,580-evaluation main panel is large for a dissertation hotspot benchmark, and Stage 1 ch3/ch4 correctly note breadth across transmission routes, protein lengths, and evolutionary regimes. Strictly, however, this is still one surface-glycoprotein single-position regime, Layer C is 6/11, escape validation is 3/11, adaptive inference fails at n=11, and 11-vs-12 denominator switching adds friction.

E. interpretation (results reading): 8.4. Stage 1 ch4/ch5 show commendable interpretation discipline: uniqueness is demoted as chance-likely, LOPO 0/11 is null-consistent, Friedman p=0.990 is not overclaimed, and "largest source" is narrowed to largest modeled component. I deduct for occasional overstrong local wording, especially negative-MCC cells being "exactly" predicted by pathogen-dependent optimality and Layer C winner differences "confirming" independence.

F. novelty/contribution: 7.8. The novelty is real as a benchmark-and-audit contribution: broad RNA-virus region-level hotspot benchmarking, quantitative scoring x pathogen interaction, and a bounded HIV-1 practical anchor. But from a VEP/PLM perspective it is not a new deployable predictor, not a strong adaptive selector, not comprehensive VEP benchmarking, and the 4-core cold-start recipe is historical rather than optimized.

G. practical value (wet-lab triage utility): 7.5. Stage 1 ch4/ch5 support practical value as search-space reduction, especially HIV-1 7.19x enrichment with 82% Layer-A-disjoint escape positions and Layer C DMS validation across 650 positions in 6 pathogens. The strict deduction is that the strongest practical statement relies on a post-hoc optimal scoring-detector choice and a narrow external set; cold-start gives only modest enrichment and is formally abstained from deployment at 0/12 callable folds.

H. clarity (writing): 7.8. Stage 1 reports consistently note good ledgers, tables, and claim-boundary language, and the methods/results captions often expose exactly the caveat a specialist wants. The writing is nevertheless dense, acronym-heavy, and patch-like in places, with legacy labels, denominator drift, and long audit paragraphs that reduce readability.

I. limitations awareness: 9.0. Stage 1 ch5 is very strong here: Layer A heterogeneity, PLM leakage, small n, winner's curse, sub-lineage pooling, prospective failure, dual-use, and independent reproduction are all named and bounded. My direct read confirms the most damaging limitations are not hidden: grand mean prospective AUROC 0.539, 0/12 callability, and seven adaptive paradigms failing at n=11 are explicitly retained.

J. overall maturity: 8.3. The manuscript is mature in evidence hierarchy, reproducibility anchors, negative-result handling, and refusal to claim deployment. I withhold a higher score because the scientific narrative still carries late-stage repair artifacts: 11/12 denominator shifts, PLM proxy caveats, retained "hotspot detector" language, and practical tables that could be overused beyond the evidence.

## Strongest single deduction
one-line: G, because practical wet-lab utility is credible for retrospective HIV-1-anchored triage but not yet general, cold-start, or deployable; fix by adding independent residue-level escape/DMS validation for more pathogens under a pre-specified non-oracle protocol.

RESULT_PROF_V8_06: total=81.7/100 min_item=7.5(G) max_item=9.0(I) stage1_evidence_used=5
