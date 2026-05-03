# Professor 9: Statistical genetics (strictness=medium)

## Scores
A: 8.0
B: 8.0
C: 7.0
D: 8.0
E: 7.0
F: 8.0
G: 7.0
H: 8.0
I: 9.0
J: 8.0
total: 78.0/100

## Rationale (≤3 sentences each item)
A: The problem is well defined as region-level, single-position RNA-virus surface-glycoprotein hotspot detection rather than per-variant fitness prediction. The dissertation repeatedly states the task boundaries, the active 11-pathogen panel, and the distinction between retrospective prioritization and prospective deployment. The remaining weakness is that "hotspot" remains operationally plural because Layer A, Layer B, Layer C, escape audit, and future-emergence labels encode different biological meanings.

B: The related work is broad and current, covering viral hotspot methods, cancer hotspot analogues, DMS, PLMs, EVEscape/ProteinGym/EVEREST/ViroGym, and algorithm-selection framing. It appropriately distinguishes MutBench from per-variant VEP benchmarks and discloses that some cited recent resources are preprints or versioned releases. The section is somewhat overextended, and several parallels are descriptive rather than directly benchmark-comparable.

C: The methodology is serious and mostly defensible: a pre-specified 20 scoring × 39 detector × 11 pathogen grid, MCC under class imbalance, explicit ground-truth layers, cluster/wild/phylogenetic/Bayesian robustness checks, and nested-LOPO for feature ablation. From a statistical-genetics perspective, the main concern is residual dependence and heterogeneity: detector variants share MSAs and labels, pathogens are only 11 clusters, Layer A mixes immune escape/convergence/HVR membership, and no independent recuration or inter-annotator reliability is available. The dissertation acknowledges these issues, but they materially reduce causal interpretability of the scoring × pathogen effect.

D: The experimental scope is good for a dissertation: 8,580 main evaluations across 11 viruses, 20 scoring formulas, 14 detector families, plus Stage 3 feature-ablation and negative adaptive audits. The pathogen panel spans useful evolutionary regimes and uses several orthogonal evidence tracks. The scale is still modest at the effective unit of inference, because the headline pathogen-level inference rests on 11 viruses and only 3/11 have curated vaccine-escape external anchors.

E: The interpretation is careful in many places: LOPO 0/11 is treated as null-consistent, H3N2 escape is called self-consistency, SARS-CoV-2 exploratory, and the 4-core is not described as deployable. However, the manuscript still leans heavily on retrospective enrichment and top-of-grid per-pathogen optima despite winner's-curse risk and prospective backtests near chance for most pathogens. The strongest statistical claim should be phrased as "large within-panel interaction under heterogeneous labels," not as general pathogen-adaptive learnability.

F: The contribution is novel and useful: a region-level hotspot-detection benchmark that decomposes biological information sources across viruses is distinct from standard VEP and DMS benchmarks. The scoring × pathogen interaction framing and the HIV-1 Layer-A-disjoint escape audit are meaningful additions. Novelty is reduced slightly by reliance on existing feature families, proxy implementations for some scores, and an exploratory rather than deployable adaptive-selection result.

G: Practical value is real but bounded. The HIV-1 enrichment result and search-space reduction framing are useful for retrospective prioritization, and the work provides a concrete audit framework for future surveillance tools. Practical deployment is not yet supported: prospective signal is weak overall, the abstention rule calls 0/12 folds, and adaptive methods fail to beat EqualWeight under nested-LOPO.

H: The dissertation is unusually explicit about definitions, boundaries, numerics, and caveats, which helps readability and defense readiness. Tables such as the evidence ledger, panel-scope ledger, validation ledger, and limitations matrix make the argument auditable. The main clarity deduction is density: many repeated caveats, overlapping stage names, and multiple EqualWeight/omega/LOPO variants make the reader work hard to track which statistic supports which claim.

I: Limitations awareness is excellent. The manuscript directly names Layer A curation heterogeneity, small-cluster inference, label circularity, prospective-validation failure, winner's curse, PLM/channel redundancy, MAFFT/input heterogeneity, and dual-use constraints. It also reports several negative results rather than hiding them, including HBFWS p = 0.78, Cycle 7B failures, Wave 4 non-significance, Wave 5 sign-opposite Layer A' sensitivity, and 0/12 callability.

J: Overall maturity is good: the dissertation has a coherent benchmark, reproducibility/provenance hooks, statistical diagnostics, and a disciplined hierarchy of claims. It is not at "excellent" maturity because the effective independent sample size is small, ground-truth provenance is not independently audited, and the practical/adaptive claims remain exploratory. As a finished dissertation, it is defensible if the oral defense keeps the conclusions within the stated retrospective, single-position, within-panel scope.

## Critical concerns (if any item < 6)
None.

## Strongest single deduction
C: Layer A label-provenance heterogeneity plus only 11 pathogen clusters weakens the inferential status of the scoring × pathogen interaction; the fix is an independently recurated 20--30+ pathogen panel with source-swapped Layer A sensitivity and time-forward validation.

RESULT_PROF_V6_09: total=78.0/100 min_item=7.0(C,E,G) max_item=9.0(I)
