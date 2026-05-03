# Professor 9: Statistical genetics (strictness=medium)

## Scores
A: 8.0
B: 8.0
C: 7.0
D: 8.0
E: 8.0
F: 8.0
G: 7.5
H: 7.0
I: 9.0
J: 8.0
total: 78.5/100

## Rationale (≤3 sentences each item)
A: The problem statement is well scoped around region-level, single-position hotspot prioritization rather than prospective variant prediction. It clearly distinguishes benchmarking, pathogen-dependent information utility, and retrospective wet-lab triage. The remaining weakness is that the motivating question sometimes drifts between hotspot detection, adaptive method selection, and vaccine-escape prioritization, requiring repeated boundary statements.

B: The related work is broad and current, covering viral hotspot methods, HyPhy/FUBAR-style selection tests, DMS, PLMs, EVEREST/ProteinGym/ViroGym, and benchmark-design principles. It appropriately distinguishes per-variant VEP benchmarks from per-region hotspot detection. Some claims rely on very recent preprints and the narrative is dense, but the literature positioning is materially strong.

C: The methodology is ambitious and mostly transparent: 11 pathogens, 20 scoring formulas, 39 detector variants, three-layer ground truth, MCC-centered evaluation, ANOVA, Friedman, LOPO, cluster/bootstrap robustness frames, and escape-enrichment audits. The main methodological deduction is that Layer A is heterogeneous and single-team curated, the effective pathogen cluster count is only 11, several scoring channels are correlated or proxy-derived, and the ANOVA grid contains dependence among parameter variants. The dissertation discloses these issues well, but disclosure does not fully remove their impact on causal/statistical interpretation.

D: The experimental scope is substantial for a dissertation: 8,580 primary evaluations across diverse RNA-virus surface glycoproteins, plus DMS validation where available, prospective sanity checks, feature-ablation audits, and multiple adaptive-weighting negative controls. From a statistical genetics viewpoint, 11 pathogen units is still small for stable random-effect or adaptive-selection inference. The scale is strong for a benchmark artifact but moderate for broad evolutionary generalization.

E: The interpretation is disciplined: LOPO 0/11 and Friedman p=0.990 are treated as null-consistent corroboration rather than independent positive evidence, H3N2 is correctly downgraded to self-consistency, and SARS-CoV-2 escape validation is exploratory. The HIV-1 Layer-A-disjoint escape result is appropriately elevated as the primary practical anchor. The main weakness is that some practical and family-prior language still risks sounding more deployable than the negative prospective and callability audits support.

F: The contribution is original in combining hotspot detection, multi-information scoring, pathogen-by-information interaction quantification, and practical escape-enrichment auditing. The strongest novelty is the quantified scoring x pathogen interaction and the explicit negative result that adaptive selection is not learnable at n=11. The novelty is less in individual scoring/detection algorithms, many of which are adapted or proxy channels.

G: Practical value is real but bounded: search-space reduction to roughly 10-50 candidate positions with HIV-1 external enrichment is useful for wet-lab triage. The work is not yet a deployable surveillance detector, and prospective backtests show weak mean performance with formal abstention on the current panel. Thus the practical value is credible for retrospective prioritization, not for operational forecasting.

H: The writing is generally clear at the claim-boundary level and repeatedly tells the reader what is and is not load-bearing. However, the manuscript is very dense, with many audit labels, repeated caveats, and overlapping stage/panel definitions that tax readability. A tighter hierarchy of primary evidence versus secondary audits would improve examiner accessibility.

I: Limitations awareness is excellent. The dissertation openly documents Layer A provenance problems, circularity risk, winner's curse, small-cluster inference, PLM/proxy collinearity, prospective-validation failure, label-provenance non-equivalence, and dual-use concerns. Few dissertations state negative gates this explicitly.

J: Overall maturity is high: the work has a coherent benchmark artifact, extensive provenance, robust statistical triangulation, and disciplined interpretation of negative results. The major maturity gap is not execution but evidential scope: independent recuration/reproduction and a larger pathogen panel are still needed before the strongest generalization claims become stable. As a defended dissertation, it is solid and unusually self-critical.

## Critical concerns (if any item < 6)
None.

## Strongest single deduction
C: methodology loses the most because the central scoring x pathogen inference rests on heterogeneous Layer A labels, only 11 pathogen clusters, and dependent/correlated scoring-detector cells; the fix is an independently recurated expanded 20-30+ pathogen panel with predeclared label provenance and a cell-level mixed/clustered primary model.

RESULT_PROF_V7_09: total=78.5/100 min_item=7.0(C,H) max_item=9.0(I)
