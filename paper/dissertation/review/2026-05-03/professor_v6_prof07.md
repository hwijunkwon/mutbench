# Professor 7: Benchmark methodology (strictness=medium)

## Scores
A: 8.0
B: 8.0
C: 7.5
D: 8.0
E: 7.5
F: 8.0
G: 7.0
H: 8.0
I: 9.0
J: 7.5
total: 78.5/100

## Rationale (≤3 sentences each item)
A: The problem statement is well-defined: region-level, single-position hotspot detection for RNA-virus surface glycoproteins, explicitly separated from per-variant fitness prediction. The work clearly identifies the absence of standardized ground truth, metrics, and cross-pathogen benchmark design. Deduction: the biological object "hotspot" remains operationally plural because Layer A, Layer B, Layer C, and escape validation each encode different notions of importance.

B: Related work is broad and current, including hotspot detection, density clustering, DMS, surveillance systems, algorithm selection, and concurrent VEP benchmarks. The task distinction from ViroGym/EVEREST/ProteinGym is generally convincing and repeatedly clarified. Deduction: the review sometimes reads defensively and could better synthesize benchmark-design principles into fewer, sharper criteria.

C: The benchmark methodology is substantially stronger than typical dissertation benchmarks: the grid is preregistered, MCC choice is justified for class imbalance, row-level versus cell-level ANOVA is disclosed, and cluster/wild/phylogenetic/Bayesian robustness frames are reported. The central design weakness is Layer A: single-team curation, pathogen-specific evidence rules, dominant anchor sources, and no inter-curator reproducibility mean that the benchmark partly measures curation-protocol response as well as pathogen biology. A second deduction is that prospective validation and deployable adaptive selection are explicitly negative, so the methodology is robust for retrospective comparison but not yet a mature selection system.

D: The scope is good for an active dissertation build: 11 main pathogens, 20 scoring formulas, 14 families, 39 variants, and 8,580 evaluation cells, with Stage 3 sensitivity on a 12-pathogen panel. The scale is broad for region-level viral hotspot detection and the pathogen diversity is meaningful. Deduction: the effective inferential unit is still only 11 pathogens, with 5/8 singleton families for some adaptive analyses, which limits claims about generalizable algorithm selection.

E: Interpretation is careful and mostly statistically disciplined: LOPO 0/11 and Friedman p=0.990 are treated as null-consistent corroboration, not independent proof, and HIV-1 is correctly elevated above H3N2/SARS-CoV-2 as the cleaner escape anchor. The dissertation is especially good at distinguishing top-1 enrichment from Bonferroni-survivor means and retrospective from prospective value. Deduction: some practical sections still risk sounding more actionable than the evidence warrants given 0/12 callability and weak time-forward performance.

F: The contribution is original in benchmark framing rather than in a single detection algorithm: it makes the information-source-by-pathogen interaction the main object of study. The combination of three-layer ground truth, scoring/detector factorial decomposition, and external escape audit is a genuine contribution for viral hotspot evaluation. Deduction: novelty is bounded by dependence on curated labels and established feature classes, and the cold-start 4-core is useful but not an optimal or deployable new method.

G: Practical value is real but retrospective: HIV-1 shows strong Layer-A-disjoint escape enrichment and the framework can reduce a protein-scale search space to a smaller candidate set. The workflow and runtime discussion make the benchmark operationally plausible for research prioritization. Deduction: practical deployment is not supported; the prospective backtest is weak overall, adaptive weighting fails, and the abstention rule calls 0/12 folds.

H: The manuscript is clear at the claim-boundary level: headline ledgers, scope tables, validation hierarchy, and limitation matrices make the evidential status unusually transparent. It also repeatedly reconciles potentially confusing details such as 11 vs 12 pathogens, 20 scoring formulas vs 10 features, and production vs nested-LOPO EqualWeight. Deduction: the density of caveats and repeated audits can make the narrative hard to follow, and some sections would benefit from consolidation.

I: Limitations awareness is excellent. The manuscript directly names Layer A heterogeneity, winner's curse, PLM collinearity/leakage, row dependence, small pathogen count, lack of independent reproduction, MAFFT-auto artifacts, scope boundaries, dual-use risk, and prospective validation failure. The main remaining gap is not awareness but resolution: several limitations are disclosed rather than experimentally closed.

J: Overall maturity is good: the study has a coherent benchmark artifact, documented provenance, multiple robustness frames, negative results, and an appropriately bounded conclusion. It is defense-ready as a retrospective benchmark methodology contribution. Deduction: it is not yet mature as a broadly generalizable benchmark standard because labels were curated by one team, no external rerun is shown, and the adaptive/callability program fails on the current panel.

## Critical concerns (if any item < 6)
None.

## Strongest single deduction
C/J: the benchmark's strongest inference still depends on heterogeneous, single-team Layer A curation and an 11-pathogen effective panel; fix by adding independent duplicate curation plus a 20--30+ pathogen external rerun with time-forward validation.

RESULT_PROF_V6_07: total=78.5/100 min_item=7.0(G) max_item=9.0(I)
