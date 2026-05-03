# Professor 8: Practice/field user (strictness=high)

## Scores
A: 8.0
B: 8.0
C: 7.0
D: 8.0
E: 7.0
F: 8.0
G: 6.0
H: 6.5
I: 9.0
J: 7.5
total: 75.0/100

## Rationale (≤3 sentences each item)
A: The problem statement is well scoped to region-level, single-position RNA-virus surface glycoprotein hotspot detection and clearly separates this task from per-variant fitness prediction. From a practice perspective, the motivating use case is strong, but the dissertation sometimes moves between surveillance, vaccine-escape prioritization, retrospective benchmarking, and cold-start deployment in ways that require careful boundary reading. The final practical problem is therefore defined well, but not perfectly operationalized for a field user.

B: The related-work coverage is broad and usefully distinguishes hotspot detection from VEP benchmarks, surveillance systems, phylogenetic selection tools, DMS resources, and cancer hotspot methods. The comparison to ViroGym, EVEREST, ProteinGym, EVEscape, ConDor, and Nextstrain is relevant to positioning MutBench. The deduction is that the literature review is sometimes defensive and benchmark-comparison-heavy, while fewer pages are spent translating prior operational surveillance needs into concrete end-user requirements.

C: The methodology is ambitious and mostly transparent: 3-layer ground truth, 20 scoring formulas, 14 detection families, 39 variants, MCC, ANOVA, Friedman, LOPO, bootstrap, escape-enrichment audit, and nested-LOPO ablations are all specified. The major weakness is not hidden but still serious: Layer A is heterogeneous, one-team curated, partly source-dominated, and absolute MCC across pathogens is not directly comparable. The small 11-pathogen panel, retrospective design, retained within-family dependence, and non-deployable adaptive selection keep this below an excellent methodological score.

D: The experimental scale is substantial for a dissertation-level active build: 8,580 main evaluations across 11 RNA viruses, 12-pathogen feature analyses, and several additional robustness and sensitivity audits. The scope is nevertheless narrower than a field user would want for deployment because it is limited to surface glycoproteins, single-position scoring, available curated labels, and only 3/11 pathogens with residue-level vaccine-escape validation. The scale is strong as a benchmark artifact, moderate as an operational validation base.

E: The interpretation is unusually candid about negative findings: LOPO 0/11 is treated as null-consistent, Friedman p=0.990 is not overclaimed, H3N2 is downgraded to self-consistency, SARS-CoV-2 is exploratory, and Wave 5 is correctly framed as label-provenance non-equivalence. The main concern is that practical search-space reduction is still emphasized strongly despite forward-time AUROC near chance for most pathogens and 0/12 callability under the pre-registered rule. The interpretation is responsible, but the field-facing takeaway still needs more conservative phrasing.

F: The contribution is original in framing a region-level hotspot-detection benchmark distinct from per-variant fitness prediction and in quantifying scoring-by-pathogen dependence. The strongest contribution is the benchmark architecture plus the interaction evidence, not a deployable predictor. Novelty is reduced somewhat because several input information types and detectors are established tools, and the work integrates and audits them rather than introducing a fundamentally new biological model.

G: Practical value is real but bounded: HIV-1 provides a credible retrospective external anchor with 7.19x enrichment and strong Layer-A-disjoint support, and the benchmark can guide experimental prioritization from hundreds or thousands of positions to a smaller candidate set. However, a field user cannot yet treat the system as prospectively callable: only 3/11 pathogens have escape validation, the forward-time backtest is weak for most pathogens, adaptive methods fail, and the abstention rule calls 0/12 folds. This item receives the strongest deduction because the dissertation's operational promise remains retrospective and exploratory.

H: The dissertation is materially clearer than many technical benchmarks because it uses ledgers, scope tables, audit labels, and repeated boundary statements. At the same time, the document is dense, cross-reference-heavy, and overloaded with versioned audit language, protocol distinctions, and similar-sounding panels: 11-pathogen main, 12-pathogen Stage 3, Wave 4, Wave 5, Layer A, Layer A', 3-core, 4-core, EqualWeight, HBFWS, and Cycle 7B. A field user can eventually understand the evidence hierarchy, but the manuscript needs a much cleaner operational summary and fewer defense-time digressions in the main line.

I: Limitation awareness is a major strength. The dissertation explicitly acknowledges Layer A heterogeneity, curation reproducibility limits, source-selection sensitivity, winner's curse, small-cluster inference, prospective validation failure, label-provenance non-equivalence, dual-use risk, and the lack of independent reproduction. The only deduction is that some limitations are so numerous and late-stage that they should more directly reshape the headline practical claims.

J: Overall maturity is good: the active build shows a coherent benchmark, reproducibility intent, extensive statistical diagnostics, and a disciplined handling of negative results. It is not yet mature as a field-deployable system because prospective validation, independent recuration, external reproduction, and callability gates remain unresolved. As a dissertation benchmark it is solid; as a practice-facing decision tool it is still pre-deployment.

## Critical concerns (if any item < 6)
None under the formal threshold. The closest concern is G: the work has practical retrospective value, but not enough prospective, callable validation for a high field-use score.

## Strongest single deduction
G, because the central practical claim needs prospective validation and callable-fold success; fix by expanding to 20--30+ externally curated pathogens with time-forward validation and preserving the pre-registered abstention gate.

RESULT_PROF_V6_08: total=75.0/100 min_item=6.0(G) max_item=9.0(I)
