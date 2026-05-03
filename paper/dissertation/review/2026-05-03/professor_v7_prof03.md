# Professor 3: Statistics/ML (strictness=high)

## Scores
A: 8.0
B: 8.0
C: 6.5
D: 8.0
E: 7.5
F: 8.0
G: 7.0
H: 8.0
I: 9.0
J: 7.0
total: 77.0/100

## Rationale (≤3 sentences each item)
A: The problem is now sharply bounded: region-level, single-position hotspot prioritization for RNA-virus surface glycoproteins, not prospective deployment. The research questions map cleanly to benchmark construction, pathogen-dependent information utility, and escape-enrichment triage. The remaining weakness is that "hotspot" remains operationally plural because Layer A, Layer C, escape validation, and prospective emergence are intentionally different targets.

B: The related-work section covers hotspot detection, phylogenetic selection, DMS, PLMs, algorithm selection, and contemporary VEP benchmarks with useful task distinctions. It appropriately positions EVEREST, ProteinGym, ViroGym, and MutClust without overclaiming direct comparability. Coverage is broad, but some reviewed items are very recent/preprint-level and the causal boundary between VEP and hotspot detection could be tighter.

C: Methodology is extensive and unusually transparent, with preregistered thresholds, a large factorial grid, MCC under class imbalance, cluster-aware omega checks, nested-LOPO for the 4-core, null calibration, and explicit negative gates. The core statistical weakness is that the 8,580 rows are not independent, the effective pathogen panel is only 11, Layer A is heterogeneous and single-team curated, and several channels are proxies or collinear rather than fully independent biological information sources. The dissertation mitigates these risks better than most, but from a Statistics/ML standard this is still a bounded retrospective benchmark, not a stable inferential or predictive model.

D: The experimental scale is good for a dissertation: 20 scoring formulas, 39 detector variants, 11 main pathogens, 8,580 evaluations, plus 12-pathogen feature audits and Wave 4/5 sensitivity checks. Sequence counts and protein diversity are substantial within the defined RNA-virus surface-protein scope. The scale is not yet sufficient for adaptive method selection, random-effect stability, prospective validation, or broad pathogen generalization.

E: The interpretation is disciplined: LOPO 0/11 and Friedman p=0.990 are correctly treated as null-consistent corroboration rather than positive proof, and HIV-1 is separated from H3N2 self-consistency and SARS-CoV-2 exploratory evidence. The strongest interpretation is the scoring-by-pathogen interaction and retrospective triage value, not a universal detector. Some passages still lean on upper-envelope top-1 enrichments and family-prior recommendations that require careful reader attention to avoid over-reading.

F: The contribution is novel in framing hotspot detection as a multi-information, cross-pathogen benchmark with a quantified scoring-by-pathogen interaction. The three-layer ground truth and escape-circularity audit are useful additions beyond typical single-pathogen hotspot papers. The novelty is more in benchmark design and failure-bounded statistical synthesis than in a new predictive algorithm.

G: Practical value is credible as retrospective search-space reduction, especially the HIV-1 Layer-A-disjoint escape anchor and the explicit candidate-list economics. The cold-start recipe is simple and operational, but the abstention results, weak prospective backtest, and Wave 5 sign-opposite sensitivity prevent deployment-level value. Practical use should remain triage for experimental planning, not surveillance forecasting.

H: The dissertation is generally clear, with strong ledgers, caveat tables, and repeated scope boundaries. Statistical distinctions such as evaluation-level vs cell-level omega, production EqualWeight vs nested-LOPO EqualWeight, and top-1 vs fixed-threshold enrichment are explicitly explained. The price is density: many caveats are packed into long paragraphs, and readers may need effort to separate headline evidence from audit history.

I: Limitations awareness is excellent. The text directly acknowledges Layer A provenance, circularity, small clusters, PLM/proxy collinearity, prospective failure, callability abstention, dual-use risk, MAFFT artifacts, and non-interchangeability of Layer A and Layer A'. This is the strongest part of the thesis from a statistical review perspective.

J: Overall maturity is acceptable-to-good, with substantial evidence hygiene, reproducibility detail, and mature negative framing. It falls short of higher maturity because the inferential center still rests on a small heterogeneous pathogen panel, retrospective labels, partial external validation, and no independent recuration or independent replication. The work is defensible as a bounded benchmark dissertation, not as a finished deployable ML system.

## Critical concerns (if any item < 6)
None.

## Strongest single deduction
C: Methodology loses most credit from the combination of n=11 pathogen-level inference, heterogeneous single-team Layer A labels, dependent evaluation rows, and proxy/collinear scoring channels; the fix is an independently recurated expanded pathogen panel with held-out prospective validation and pre-specified external escape/DMS endpoints.

RESULT_PROF_V7_03: total=77.0/100 min_item=6.5(C) max_item=9.0(I)
