# Professor 9: Statistical genetics (strictness=medium)

## Stage 1 reports consulted
- abstract_ch1: Strong bounded problem framing around retrospective wet-lab triage, with small residual prospective wording in figures/cold-start language.
- ch2: Current and task-aware related work that distinguishes hotspot triage from surveillance and VEP benchmarks, though epistasis/coupling methods are mostly out of scope.
- ch3: Methodology is auditable and large-scale, with preregistered layer/grid choices and explicit dependence caveats, but dense prose and some deferred sensitivities.
- ch4: Results are statistically mature and unusually honest about null/negative findings; practical value is narrower than the headline benchmark scale.
- ch5: Discussion strongly calibrates claims and limitations, especially non-deployability, but denominator drift between 11- and 12-pathogen analyses remains visible.

## Specialty deep-read
- ch3_methods: I verified that Layer A/B/C roles are explicitly separated, Layer A/C conflicts are handled without forced merging, and the scoring x pathogen ANOVA grid was frozen before Stage 1. The most important statistical-genetics caveats are acknowledged rather than hidden: heterogeneous Layer A construction, only 6/11 Layer C pathogens, dependent detector variants, small pathogen-cluster count, and an ESM-2 proxy channel standing in for true Tranception-like evidence.
- ch4_results: I verified that the load-bearing evidence is the scoring x pathogen interaction, not the 11/11 uniqueness claim, Friedman, or LOPO. The chapter correctly demotes LOPO/Friedman to consistency checks, reports forward-time weakness and 0/12 callability, and makes HIV-1 the main external escape anchor; however, several practical rows still use oracle/best-combination framing and some local wording remains stronger than the evidence warrants.

## Scores
A: 8.7
B: 8.4
C: 8.5
D: 8.6
E: 8.4
F: 8.3
G: 7.7
H: 8.0
I: 9.0
J: 8.5
total: 84.1/100

## Rationale (per item, 2-3 sentences each, citing Stage 1 evidence + your specialty observations)

A. problem statement: 8.7. Stage 1 abstract/ch1 found a clear problem contract: standardized evaluation is missing, independent ground truth is missing, and pathogen-dependence of best information source is unquantified. I agree after the specialty read that the methods/results support this as a retrospective single-position wet-lab triage problem, but small phrases such as "might important mutations occur next" and "practical impact" still risk prospective-detector expectations.

B. related work: 8.4. Stage 1 ch2 shows strong separation among surveillance, VEP, selection tests, cancer hotspot tools, and MutBench's region-level hotspot detection niche. The deduction is for compressed treatment of coupling/epistasis-aware approaches and the fragility of "broadest" unless the qualifier "region-level, single-position RNA-virus hotspot benchmark" is preserved.

C. methodology: 8.5. Stage 1 ch3/ch4 emphasized the mature methodological contract: 3-layer ground truth, 20 scoring types, 14 families/39 variants, MCC primary evaluation, preregistered thresholds, and multiple robustness frames for the ANOVA. My direct read confirms strong label-metric separation and appropriate cluster/dependence caveats, but I deduct for heterogeneous Layer A definitions, only partial Layer C coverage, correlated detector/scoring channels, small n=11 pathogen inference, and several deferred sensitivities.

D. scale: 8.6. Stage 1 reports document a substantial benchmark: 11 RNA viruses, 8 families, 8,580 evaluations, broad transmission/evolutionary regimes, 73 temporal splits, and DMS checks on 6 pathogens. Scale is not perfect because the benchmark remains surface-glycoprotein/single-position only, external escape validation is 3/11, and later 12-pathogen feature/audit panels create denominator friction.

E. interpretation: 8.4. Stage 1 ch4/ch5 correctly identifies the strongest interpretive feature: the dissertation does not overread 11/11 uniqueness, LOPO 0/11, or Friedman p=0.990, and treats ANOVA/Friedman/LOPO as same-data consistency checks. My direct read confirms that the scoring x pathogen omega-squared result is handled well, with cluster-bootstrap and alternative robustness frames, but some phrases remain overstrong, especially the negative-MCC fraction being "exactly" predicted and DMS winner changes "confirming" independence.

F. novelty/contribution: 8.3. Stage 1 evidence supports novelty as a benchmark-and-audit contribution: broad region-level viral hotspot benchmark, quantified pathogen-by-information interaction, and guarded wet-lab triage validation. The novelty is less an algorithmic breakthrough than a disciplined measurement contribution; adaptive selection and cold-start learning fail under the tested n=11 regime.

G. practical value: 7.7. Stage 1 ch4/ch5 supports real triage value, especially HIV-1 vaccine-escape enrichment at 7.19x with largely Layer-A-disjoint sites and Layer C DMS validation across 6/11 pathogens. I score this lower than C/E because the strongest external validation rests mainly on HIV-1, H3N2/SARS-CoV-2 are partly self-consistency or exploratory, cold-start callability is 0/12, and best-combination/oracle framing limits direct use for a new pathogen.

H. clarity: 8.0. Stage 1 reports note useful ledgers, tables, and explicit guardrails, and I found the methods/results generally auditable. The deduction is for high density, legacy labels such as 9-pathogen anchors, repeated 11/12 denominator shifts, result-heavy methods prose, and compressed acronyms/wave labels that make the dissertation harder to read than its scientific logic requires.

I. limitations awareness: 9.0. Stage 1 ch5 found unusually explicit limitations: Layer A heterogeneity, prospective/forward-time weakness, small panel size, label provenance sensitivity, dual-use constraints, PLM leakage, MAFFT artifacts, and non-deployment. My direct read agrees; the manuscript repeatedly states that adaptive selection is unsupported at n=11 and that Layer A curation remains rate-limiting, which is a strong maturity marker.

J. overall maturity: 8.5. The manuscript is mature in statistical self-discipline: it reports negative-MCC cells, null-consistent LOPO/Friedman, weak prospective backtests, failed adaptive weighting, and formal deployment abstention. The remaining deductions are integration-level rather than fatal: dense late-stage audit prose, denominator drift, partial external validation, and a few local phrases that still sound more detector-like than triage-like.

## Strongest single deduction
one-line: G, practical value is real but still mainly HIV-1/DMS-supported and not yet a callable cold-start detector; fix by adding balanced prospective wet-lab validation on additional pathogens with predeclared non-oracle scoring choices.

RESULT_PROF_V8_09: total=84.1/100 min_item=7.7(G) max_item=9.0(I) stage1_evidence_used=5
