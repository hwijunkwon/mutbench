# Professor 4: Computational biology (strictness=medium)

## Scores
A: 8.0
B: 8.0
C: 7.0
D: 7.0
E: 7.5
F: 8.0
G: 7.0
H: 8.0
I: 8.5
J: 7.5
total: 76.5/100

## Rationale (≤3 sentences each item)
A: The problem definition is clear: viral hotspot detection lacks standardized, multi-pathogen benchmarking and independent validation. The dissertation appropriately narrows the claim to RNA-virus surface glycoproteins and single-position, region-level prioritization. The remaining weakness is that "hotspot" spans immune escape, convergence, HVR membership, and functional constraint, so the biological target is still heterogeneous.

B: The related-work review covers viral surveillance, cancer hotspot methods, phylogenetic selection, DMS, PLMs, VEP benchmarks, and algorithm selection with good breadth. The comparison to ProteinGym, EVEREST, ViroGym, and EVEscape is current and mostly careful about task differences. It is somewhat overextended in places, and several very recent preprints are treated as useful context but cannot yet support strong community-consensus claims.

C: The methodology is ambitious and mostly defensible: 20 scoring formulas, 39 detector variants, three-layer ground truth, MCC/escape-enrichment anchors, ANOVA, Friedman, LOPO, and nested-LOPO feature audits. The main deductions are Layer A heterogeneity, single-team label curation without inter-annotator reproducibility, MAFFT/truncation/input-quality caveats, and partial DMS availability. The statistical framing has improved by admitting that LOPO and Friedman are null-consistent rather than independent proof.

D: The scale is substantial for a dissertation: 11 active pathogens, 8,580 evaluations, 6 DMS-covered pathogens, 3 external escape-audit pathogens, and multiple negative adaptive-selection audits. From a computational-biology standpoint, however, the scale is still modest for cross-pathogen inference: n=11 is below the stated 20-30 pathogen stability target, external escape validation exists for only 3/11 pathogens, and prospective signal is weak or absent across most temporal backtests. Thus the work is large computationally but only moderate biologically for generalization.

E: The interpretation is commendably guarded: HIV-1 is identified as the primary external anchor, H3N2 as self-consistency, SARS-CoV-2 as exploratory, and adaptive deployment is explicitly refused at n=11. The dissertation correctly treats omega-squared as the main positive evidence and demotes LOPO/Friedman to consistency checks. The deduction is that some narrative language still leans on per-pathogen top winners and search-space reduction despite winner's-curse, label-circularity, and negative Wave 5 provenance sensitivity.

F: The contribution is novel in task framing: region-level viral hotspot benchmarking across biological information sources is distinct from per-variant VEP benchmarks. The quantified scoring-by-pathogen interaction and practical escape-enrichment ledger are meaningful contributions. Novelty is reduced by reliance on existing feature classes and detectors rather than a new biological model.

G: Practical value is real but bounded: reducing roughly 1,000 positions to 10-50 candidates with strong HIV-1 escape enrichment is useful for retrospective wet-lab triage. The cold-start 4-core or 3-core recipe is operationally simple, and runtime/provenance claims make reuse plausible. Practical deployment value is limited by 0/12 callability, weak prospective backtests, and label-provenance non-equivalence.

H: The writing is unusually transparent about evidence tiers, caveats, and claim boundaries, and the ledgers make the thesis defensible. Some sections are dense, repetitive, and audit-heavy, which can obscure the main biological story. Overall clarity is good, but the document would benefit from tighter separation of primary evidence from historical development audits.

I: Limitation awareness is a strength: the dissertation explicitly discusses Layer A circularity, curation reproducibility, small pathogen count, sub-lineage pooling, prospective validation gaps, MAFFT artifacts, DMS sparsity, dual-use risk, and winner's curse. The negative HBFWS, Cycle 7B, Wave 4, and Wave 5 results are incorporated rather than hidden. The only notable gap is that several limitations are disclosed rather than experimentally resolved, especially independent recuration and prospective external validation.

J: Overall maturity is solid: the work has a coherent benchmark artifact, meaningful statistics, external audits, and unusually disciplined boundaries. It is not yet a mature deployable computational-biology method, and the biological evidence base remains constrained by label provenance and panel size. As a dissertation, it is above acceptable and close to strong, provided the final defense keeps the retrospective-triage framing.

## Critical concerns (if any item < 6)
None.

## Strongest single deduction
D: experimental scope is computationally broad but biologically underpowered for cross-pathogen generalization; fix by expanding to 20-30+ independently curated pathogens with time-forward labels and duplicate Layer A recuration.

RESULT_PROF_V7_04: total=76.5/100 min_item=7.0(C,D,G) max_item=8.5(I)
