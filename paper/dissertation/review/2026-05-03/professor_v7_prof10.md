# Professor 10: Structural biology (strictness=medium)

## Scores
A: 8.0
B: 8.0
C: 7.0
D: 8.0
E: 7.0
F: 8.0
G: 7.0
H: 7.0
I: 8.0
J: 7.0
total: 75.0/100

## Rationale (≤3 sentences each item)
A: The problem is well defined as a region-level, single-position benchmark for RNA-virus surface glycoprotein hotspot prioritization rather than prospective prediction. The dissertation repeatedly distinguishes retrospective triage, adaptive selector failure, and deployability, which prevents the problem statement from overreaching. The main remaining weakness is that "hotspot" still bundles immune escape, convergent evolution, HVR membership, and functional constraint into partly non-equivalent biological concepts.

B: The related-work section is broad and current, positioning MutBench against viral VEP benchmarks, surveillance platforms, cancer hotspot tools, DMS, PLMs, and algorithm-selection methodology. The comparison to EVEREST, ViroGym, ProteinGym, EVEscape, HyPhy, and structural hotspot precedents is useful and mostly careful about task mismatch. From a structural-biology standpoint, the review could better integrate conformational epitope mapping, oligomer interfaces, glycosylation, and experimentally solved viral glycoprotein structures beyond the SARS-CoV-2 anchor.

C: The methodology is substantial: 11 pathogens, 20 scoring formulas, 39 detector variants, three-layer ground truth, MCC-based Stage 2 evaluation, and several robustness frames. The major structural deduction is that structural channels rely mainly on AlphaFold/ESMFold monomers and pLDDT/SASA, while biologically relevant trimer/dimer assemblies, glycan shielding, conformational state, and cross-pathogen experimental structure validation are mostly deferred. The statistical methodology is unusually transparent, but the label heterogeneity and small pathogen-cluster count keep the design short of a fully mature benchmark.

D: The scale is good for a dissertation benchmark: 8,580 evaluations across 11 RNA-virus surface glycoproteins, with a 12-pathogen feature-ablation extension and vaccine-escape checks on 3 pathogens. The pathogen and scoring diversity are meaningful, and the work is not just a SARS-CoV-2 case study. The deduction is that the biological scope remains narrow: surface proteins only, substitutions only, limited DMS coverage, no DNA viruses or multi-protein pathogen context, and limited structural validation outside SARS-CoV-2.

E: The interpretation is mostly disciplined and earns credit for explicitly demoting LOPO 0/11, Friedman p=0.990, H3N2 escape enrichment, SARS-CoV-2 escape enrichment, and adaptive weighting failures to their proper evidentiary tiers. The strongest interpretive point is that the headline becomes pathogen-dependent information utility rather than a universal detector claim. The main deduction is that some positive framing still leans hard on retrospective oracle enrichment and the 4-feature heuristic despite the negative null-calibration, Wave 4, Wave 5, and 0/12 callability findings.

F: The contribution is original in task framing: a region-level viral hotspot benchmark centered on information-type-by-pathogen interaction is distinct from per-variant VEP benchmarks. The quantified scoring-by-pathogen interaction and HIV-1 Layer-A-disjoint escape audit are useful contributions. Novelty is reduced by the fact that several ingredients are established tools or proxies, and the deployable algorithmic contribution remains exploratory rather than validated.

G: Practical value is real but bounded: narrowing a protein from roughly 1,000 residues to tens of candidate sites is a plausible wet-lab triage use case, especially with HIV-1 escape enrichment as the cleanest external anchor. The workflow and runtime discussion are concrete enough for a computational group to reproduce the prioritization pipeline. For vaccine design or surveillance operations, however, current evidence supports retrospective prioritization only, not prospective strain selection, calibrated risk scoring, or structurally resolved immunogen design.

H: The writing is generally clear in its ledgers, tables, and repeated scope boundaries, and the dissertation is unusually explicit about which claims are positive, negative, or exploratory. However, the text is dense, repetitive, and sometimes committee-facing rather than reader-facing, with many caveats embedded in long paragraphs and table captions. A final pass should reduce redundancy and separate load-bearing claims from audit details more cleanly.

I: Limitation awareness is strong: small n=11 adaptive inference, Layer A heterogeneity, circularity, MAFFT mode artifacts, PLM proxy collinearity, monomeric structural modeling, prospective validation failure, and dual-use risk are all disclosed. The negative Wave 4/5 and adaptive-selection results are handled honestly rather than hidden. The main missing limitation from my discipline is a more systematic account of oligomeric state, glycan shielding, conformational ensembles, and epitope accessibility as structural confounders in pLDDT/SASA-driven claims.

J: Overall maturity is acceptable-to-good: the dissertation has a coherent benchmark artifact, reproducibility/provenance planning, broad experiments, and unusually mature evidentiary self-auditing. It is not yet excellent because the central applied claim is retrospective, the structural biology layer is relatively shallow compared with the statistical layer, and several late-cycle audits substantially narrow the algorithmic claim. The work is defensible as a benchmark dissertation, but it needs external reproduction and stronger structure-aware validation before being treated as a mature deployment framework.

## Critical concerns (if any item < 6)
None.

## Strongest single deduction
J: overall maturity is limited by the mismatch between extensive retrospective benchmark evidence and the negative deployability/callability audits; fix by adding an externally curated expanded panel with time-forward validation and structure-aware oligomer/glycan-aware feature checks.

RESULT_PROF_V7_10: total=75.0/100 min_item=7.0(C,E,G,H,J) max_item=8.0(A,B,D,F,I)
