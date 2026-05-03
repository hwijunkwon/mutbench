# Professor 7: Benchmark methodology (strictness=medium)

## Scores
A: 8.0
B: 8.0
C: 7.5
D: 7.5
E: 8.0
F: 8.0
G: 7.0
H: 8.0
I: 9.0
J: 7.5
total: 78.5/100

## Rationale (≤3 sentences each item)
A: The problem is clearly defined as region-level, single-position hotspot prioritization for retrospective wet-lab triage, not as prospective variant prediction. The three motivating gaps--standardized comparison, independent ground truth, and pathogen-dependent method choice--are coherent and consistently carried through the abstract, introduction, methods, results, and discussion. Deduction: the problem boundary is narrower than the broad public-health language sometimes suggests, especially because the evidence covers surface glycoprotein substitutions only.

B: The related-work coverage is strong across viral hotspot tools, cancer hotspot analogies, DMS/VEP benchmarks, surveillance platforms, algorithm selection, and benchmark-bias methodology. The dissertation usefully distinguishes MutBench from ProteinGym, EVEREST, ViroGym, EVEscape, and surveillance systems by task rather than by superficial domain overlap. Deduction: some very recent benchmark comparisons are necessarily preprint/version-sensitive, and several non-benchmarked families such as coupling-aware models remain discussed rather than experimentally integrated.

C: The methodology is substantially above average: 20 scoring formulas, 14 detection families, 39 variants, a three-layer ground truth, MCC-centered Stage 2 evaluation, cluster/bootstrap robustness frames, LOPO/Friedman checks, circularity audits, and pre-registered thresholds create a serious benchmark design. The strongest methodological deductions are Layer A heterogeneity and single-team curation without duplicate recuration or inter-annotator agreement, plus scoring-channel dependence/proxy duplication and technical input heterogeneity across MAFFT/tree/structure/PLM pipelines. The dissertation acknowledges most of these issues unusually well, but acknowledgement does not fully replace independent label reproducibility or a larger, externally replicated benchmark.

D: The experimental grid is large at 8,580 evaluations and the 11-pathogen panel spans meaningful RNA-virus surface-glycoprotein diversity, with 6 DMS-covered pathogens and 3 escape-audit pathogens. From a benchmark-methodology perspective, however, the true inferential scale is closer to 11 pathogen clusters and 3,080 family-aggregated cells than to 8,580 independent observations. The small-cluster regime, missing DMS for 5/11 pathogens, and escape validation for only 3/11 pathogens justify a concrete deduction despite the broad computational sweep.

E: Results are interpreted with commendable restraint: LOPO 0/11 is not overclaimed, Friedman p=0.990 is treated as low-power/non-transfer evidence rather than a magic proof, and the HIV-1 anchor is separated from H3N2 self-consistency and SARS-CoV-2 exploratory support. The negative adaptive-selection audits, Wave 4/5 failures, and 0/12 callability result are integrated rather than hidden. Deduction: the dissertation still leans heavily on the omega-squared interaction and enrichment anchors, while the absolute MCC values and retrospective-only evidence require careful reader discipline.

F: The contribution is novel in the detection-task benchmarking niche: a standardized multi-pathogen, multi-information-type hotspot benchmark is a real contribution distinct from per-variant fitness/VEP leaderboards. The quantified scoring-by-pathogen interaction and the external escape-enrichment audit are valuable additions. Deduction: several components are recombinations of established scoring families, and novelty rests more on benchmark integration and audit discipline than on a new detection algorithm.

G: Practical value is plausible but bounded: search-space reduction from roughly 1,000 positions to 10--50 candidates with HIV-1 7.19x escape enrichment is a useful retrospective wet-lab triage result. The dissertation correctly refuses deployment claims after prospective and adaptive audits fail. Deduction: practical utility outside the curated 11-pathogen retrospective panel remains unproven, and the cold-start recipe is formally abstained from deployment on the current panel.

H: The writing is technically clear, with ledgers and tables that make claim boundaries, panel distinctions, circularity, and negative audits traceable. The manuscript is much stronger than typical benchmark dissertations in separating headline claims from auxiliary checks. Deduction: the density of audit names, stages, waves, variants, and repeated caveats creates cognitive load, and some terminology shifts between Stage 2/Stage 3 and 11/12-pathogen scopes require careful reading.

I: Limitations awareness is excellent. The dissertation explicitly names Layer A provenance heterogeneity, small pathogen count, non-independence of detector variants, PLM leakage/collinearity, MAFFT-auto artifacts, one-team reproducibility, prospective validation failure, dual-use risk, and scope limits. This is one of the strongest aspects of the work; the remaining deduction is only that several limitations remain unresolved rather than merely rhetorical.

J: Overall maturity is good but not yet excellent. The artifact is internally coherent, reproducible in principle, statistically audited, and appropriately conservative, which is a mature benchmark posture. The maturity ceiling is set by the lack of independent recuration/rebenchmarking, the small number of pathogen clusters, heterogeneous labels, partial external validation, and no supported prospective callability.

## Critical concerns (if any item < 6)
None.

## Strongest single deduction
C: methodology loses the most credit because Layer A label heterogeneity and single-team, non-duplicated curation remain the load-bearing benchmark validity risk; the best fix is an independent recuration/adjudication subset plus source-swap sensitivity before expanding claims.

RESULT_PROF_V7_07: total=78.5/100 min_item=7.0(G) max_item=9.0(I)
