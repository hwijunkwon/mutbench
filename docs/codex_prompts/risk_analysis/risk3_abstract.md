# Risk Analysis 3 — Abstract reframe: anchor preservation check

Execute the analysis NOW. Read-only. Do not commit.

## Context

The abstract (`paper/dissertation/front_en/abstract.tex`) will be rewritten to lead with **wet-lab triage value** rather than statistical-interaction headlines. Draft replacement:

> MutBench is a hotspot-prioritization framework that narrows ~1,000 protein positions to 10–50 candidate sites with 7–9× enrichment for vaccine-escape positions (HIV-1 7.19×, H3N2 9.36×, SARS-CoV-2 7.63×; HIV-1 82% Layer-A-disjoint as the primary external anchor). The framework is positioned as a wet-lab experimental triage tool, not a deployable per-position detector; comprehensive audit at panel size n=11 (LOPO 0/11, P5 0/12 callable, HBFWS p=0.78, Cycle 7B six adaptive paradigms all fail) provides falsification-resistant evidence that a deployable cross-pathogen detector is not learnable at the current panel size, formalising the panel-size threshold (~20–30 pathogens, Bolker rule-of-thumb) at which adaptive method selection becomes possible. The headline scoring×pathogen interaction (ω²=0.296, 95% CI [0.201, 0.346]) operationalises this non-learnability as quantified pathogen-dependence rather than as a methodological failure.

## Question

1. Does the new abstract preserve all **numerical anchors** present in the current abstract? Specifically check:
   - 11 pathogens, 20 scoring × 14 detection × 39 variants = 8,580 evaluations
   - ω² = 0.296, CI [0.201, 0.346]
   - HIV-1 7.19×, p_adj = 2.5×10⁻¹⁶
   - 82% Layer-A-disjoint
   - Friedman p = 0.990
   - LOPO 0/11
   - HBFWS p = 0.78
   - Wave 5 Layer A' MCC −0.055
2. Are there any **load-bearing concept** in the current abstract that the new draft drops? (e.g., 3-layer ground truth, 10 information types, etc.)
3. Does the new draft introduce any **new claim** that the dissertation body does not support? (Cross-check against `chapters_en/ch4_results.tex` and `chapters_en/ch5_discussion.tex`.)
4. Is the "wet-lab triage tool" claim quantified concretely enough? Compare to the existing search-space-reduction wording at ch4 line ~931 (subsec:search_space_reduction).
5. The current abstract has an evidence ledger table (tab:abstract_evidence_ledger) — should it be kept, modified, or removed?

## Output

`paper/dissertation/review/2026-05-03/risk3_abstract_analysis.md`

Structure:
1. Anchor preservation table (anchor, in current abstract, in new draft, verdict)
2. Concept gap list (what's dropped that should stay)
3. Body-claim consistency check (any new abstract claim not in body)
4. Concrete suggested edits to the draft (specific phrase changes, additions)
5. Verdict on the evidence-ledger table: keep / modify / remove
6. One-line: `RESULT_RISK3: anchors_preserved=<n>/<n> concepts_dropped=<n> new_claims_unsupported=<n> verdict=<accept|revise|reject>`

Length budget: ≤ 1500 words.
