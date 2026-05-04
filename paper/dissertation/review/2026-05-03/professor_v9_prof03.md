# Professor 3: Statistics/ML (strictness=high)

## Stage 1 reports consulted
- abstract_ch1: Strong bounded framing as retrospective wet-lab triage, with good ledgers and non-deployability guardrails, but residual prospective-sounding wording and dense shorthand.
- ch2: Broad, current related-work positioning that separates MutBench from VEP, surveillance, cancer-hotspot, and selection-method benchmarks; epistasis/coupling methods are only lightly treated.
- ch3: Detailed, auditable methods and strong scale documentation; deductions for proxy channels, deferred robustness checks, Layer B wording, and implementation-label drift.
- ch4: Strongest statistical evidence is the scoring x pathogen interaction plus HIV-1 escape anchor; LOPO/Friedman/unique-best results are correctly downgraded to weak or null-consistent corroboration.
- ch5: Mature narrowing chapter with explicit limitations, deployment refusal, and evidence hierarchy; denominator/numeric drift and defense-memo density remain polish risks.

## Specialty deep-read
- ch3_methods: I verified the methodological contract, preregistered grid, 8,580-row versus 3,080-cell distinction, DMS 6/11 coverage, Tranception/EVEscape proxy substitutions, HMMER deferral, and the Layer B "true negatives" phrasing. The homoplasy tree-source issue is now mostly clarified in text as production Fitch on FastTree with IQ-TREE only for the SARS-CoV-2 TreeTime audit, but the chapter remains dense and still carries results inside methods.
- ch4_results: I verified that the load-bearing statistics are properly caveated: ANOVA assumptions fail, row independence is limited, cluster-aware frames are used, LOPO 0/11 and Friedman p=0.990 are not positive evidence, and HIV-1 is the main external escape anchor. I also confirmed local overstatements remain: "all 11 unique" appears in headline/caption despite the footnote admitting only 10/11 unique parameter-variant tuples, and the DMS caption overstates "independence" before the prose backs off to non-identical aspects.

## Scores
A: 8.6
B: 8.4
C: 8.1
D: 8.3
E: 8.2
F: 8.3
G: 7.8
H: 7.9
I: 9.0
J: 8.4
total: 82.0/100

## Rationale

**A. problem statement: 8.6**  
Stage 1 abstract_ch1 shows a precise, bounded problem: region-level single-position hotspot prioritization for retrospective wet-lab triage, with the search-space reduction target explicitly stated. I deduct because ch2 still contains forecasting-flavored phrases such as "predicting variant emergence" and "might important mutations occur next," which slightly weakens the deployment guardrail.

**B. related work: 8.4**  
Stage 1 ch2 documents a broad taxonomy and does the important comparative work against ViroGym, ProteinGym, EVEREST, EVEscape, surveillance, cancer tools, and selection/homoplasy methods. The ceiling is limited by compressed treatment of coupling-aware/epistatic methods and by some results-summary material leaking into the background chapter.

**C. methodology: 8.1**  
Stage 1 ch3 and ch4 show a strong pipeline: explicit Layer A/B/C construction, 20 scoring types, 39 detector variants, MCC-centered evaluation, preregistered thresholds, and cluster-aware statistical robustness. My direct read confirms the design is serious, but strict ML deductions remain for proxy implementations (Tranception as ESM-2 pseudo-perplexity, EVEscape substituting ESM-2 for EVE), incomplete DMS threshold sweeps on 2/6 DMS pathogens, no HMMER screen, failed ANOVA assumptions, and limited independence among 8,580 rows.

**D. scale (panel size, breadth): 8.3**  
Stage 1 ch3/ch4 support a large computational grid and biologically diverse 11-virus panel spanning 8 ICTV families, 20 scoring formulas, 14 detector families, and Layer C DMS for 6 pathogens. I deduct because statistical cluster size is still only G=11, Layer C and escape validation are uneven, Zika/12-pathogen analyses can blur the main-panel boundary, and the nominal row count overstates independent information.

**E. interpretation (results reading): 8.2**  
Stage 1 ch4/ch5 show unusually careful interpretation: "largest source" is narrowed to largest modeled component, residual variance is comparable, LOPO/Friedman are null-consistent, and MERS is called a failure case despite perfect recall. My direct read confirms that the final prose often rescues overclaims, but headline/caption slips remain around "all 11 unique," DMS "independence," and the strong phrase that negative MCC is "exactly" what pathogen-dependent optimality predicts.

**F. novelty/contribution: 8.3**  
The contribution is real as a benchmark/statistical-framing result: broad region-level viral hotspot benchmarking, quantified scoring x pathogen interaction, 9 distinct optimal scoring types, and a bounded negative result for adaptive selection at n=11. It is not an operational ML breakthrough or deployable detector, and some novelty depends on the internally curated benchmark rather than independent disjoint-panel replication.

**G. practical value (wet-lab triage utility): 7.8**  
Stage 1 ch4/ch5 support practical triage value through search-space reduction, Layer C DMS validation for 6/11 pathogens, and a strong HIV-1 vaccine-escape anchor with 7.19x enrichment and mostly Layer-A-disjoint positions. I keep this below 8 because prospective transfer is weak, 0/12 callability leads to formal deployment abstention, H3N2 is largely self-consistency, SARS-CoV-2 is exploratory, and the practical claim rests disproportionately on HIV-1.

**H. clarity (writing): 7.9**  
The dissertation is clear in its ledgers, tables, and boundary statements, and Stage 1 reports consistently note that the audit style helps panel interpretation. The cost is high density: abbreviations, stage/layer/wave labels, long caveat-packed paragraphs, "Materials and Method" polish, and 11-vs-12 terminology make the manuscript harder to read than the underlying design warrants.

**I. limitations awareness: 9.0**  
Stage 1 ch5 is very strong here: it discloses weak forward transfer, label heterogeneity, small n, Layer A provenance issues, PLM leakage/correlation risks, winner's curse, MAFFT sensitivity, and dual-use constraints. The remaining deduction is for unresolved limitations rather than unacknowledged ones: no independent recuration/inter-annotator agreement, no full alignment-mode sensitivity, and no independent pathogen-panel replication.

**J. overall maturity: 8.4**  
Overall maturity is high because the manuscript reports negative results, refuses deployment, distinguishes evidence tiers, preserves reproducibility anchors, and frames Bolker 20-30 as a design target rather than proof. I deduct for patched-source feel, denominator drift between 11 and 12 pathogen analyses, proxy-channel caveats, and the fact that the central statistical claim still depends on one small-cluster benchmark despite multiple robustness frames.

## Strongest single deduction
one-line: G, because practical wet-lab triage is plausible but not deployable or broadly externally validated; the fix is an independent prospective/disjoint-pathogen validation with fixed thresholds and residue-level wet-lab outcome labels.

RESULT_PROF_V9_03: total=82.0/100 min_item=7.8(G) max_item=9.0(I) stage1_evidence_used=5
