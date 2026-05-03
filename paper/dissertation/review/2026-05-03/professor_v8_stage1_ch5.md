# Chapter Deep Eval: ch5_discussion

## In-scope rubric items
- E
- F
- G
- I
- J

## Per-item evidence

### E
**Strongest evidence**:
- The chapter gives a disciplined interpretation of the headline interaction: "Detection-family choice contributes little variance ($\omega^2=0.013$), about 23 times less than the scoring~$\times$~pathogen interaction ($\omega^2=0.296$)" and converts that into the operational reading "wet-lab triage---choose the information source" (line 68).
- It explicitly rejects over-reading LOPO: "LOPO gives 0/11 exact matches, Friedman gives $p=0.990$, and the oracle-vs-generalised gap is $0.265$" as evidence that mapping from pathogen properties to optimal scoring is "not yet learnable" (line 70), then later states LOPO 0/11 is "corroborative" rather than independent evidence (line 237).
- It makes low absolute MCC intelligible rather than defensive: "Mean oracle MCC across 11 pathogens is $0.341$" but is explained by exact matching, class imbalance, and stringency; windowed MCC rises to $0.472$ at $\pm5$ (line 78; table lines 80-109).

**Weakest evidence / gaps**:
- The chapter leans heavily on cross-references to Chapter 4 for the underlying statistical frames; within this chapter, the reader gets conclusions more than diagnostic detail for the ANOVA robustness.
- Some interpretive claims depend on dense parenthetical caveats, e.g. the EqualWeight/HIV-1/H3N2 comparison (line 128), which is technically careful but cognitively hard to verify in one pass.

**Hidden issues for panel awareness**:
- The chapter alternates between 11-pathogen main-panel language and 12-pathogen audit/wave language: e.g. main results use 11 pathogens (lines 68, 121, 235-236), while audit paragraphs say "current 12-pathogen panel" and "0/12 callable" (line 244). This may be justified by later pilot/audit additions, but a bulk reader may miss the denominator shift.
- "H-score saturation" and homoplasy alternatives are discussed before the main practical claims (lines 55-60), but the opening line says "With benchmark validity established" (line 52). That phrase can sound stronger than the immediately following caveats warrant.

**Suggested score range**: 8.0--8.8

### F
**Strongest evidence**:
- The contribution claim is concrete and scoped: "to our knowledge, MutBench is the broadest region-level, single-position hotspot-detection benchmark to date for RNA viruses" with "10 biological information types (20 scoring formulas) $\times$ 14 detection families (39 variants) $\times$ 11 RNA viruses = 8,580 evaluations" (line 235).
- The chapter differentiates MutBench from nearby benchmarks: "EVEREST and ProteinGym... target per-variant fitness or escape prediction. MutBench evaluates region-level hotspot prioritization" (line 72).
- The novel analytical result is clearly stated: "optimal biological information source is pathogen-dependent" with $\omega^2=0.296$, CI [0.201, 0.346], 9 distinct optimal information types, and oracle-vs-generalized gap 0.265 (line 236).

**Weakest evidence / gaps**:
- "Broadest ... to date" is plausible but still a fragile novelty phrase unless the rest of the dissertation has exhaustively justified the comparison set; Chapter 5 itself only names EVEREST/ProteinGym/ViroGym briefly (lines 72, 147-150).
- The 4-feature core is presented as a practical recipe (lines 5, 238), but later audits state it is "strictly dominated by the 3-feature variant" and "historical fixed configuration" (line 244), weakening its novelty as an optimized contribution.

**Hidden issues for panel awareness**:
- The chapter handles the 4-core contradiction responsibly, but the professor panel should notice that the "cold-start core" is not a discovered optimum; it is a bounded heuristic retained after negative audits (lines 238, 244, 254).
- Layer A' failure (line 250) quietly limits the generality of the benchmark-label concept: the novelty is not "any structured label provenance works," but "this literature-curated Layer A benchmark supports these within-panel findings."

**Suggested score range**: 8.0--8.7

### G
**Strongest evidence**:
- The wet-lab validation section is strongly reframed: "Layer~C DMS validation directly measures functional impact in the laboratory and covers 6 of 11 pathogens (650 positions...)" with Layer C MCC $0.139$--$0.322$ and differing Layer A vs Layer C best scorings (line 127).
- Practical value is defined as triage/search-space reduction: "reducing the experimental search space rather than achieving high absolute prediction accuracy" (line 128), and "narrow[s] the candidate list from ~1,000 to approximately 10--50 positions" with $7$--$9\times$ enrichment (line 238).
- The chapter gives a concrete workflow for new pathogens: sequence collection, feature computation, scoring priors, detector grid, runtime "15--20 min on a single GPU," and cold-start runtime "under 10 min on CPU" except AlphaFold2 (line 156).

**Weakest evidence / gaps**:
- The practical-value claim "rests mainly on HIV-1" (line 145); H3N2 is downgraded to self-consistency and SARS-CoV-2 exploratory (lines 142-145, 286).
- The family-level scoring recommendation table (lines 158-175) may look more actionable than the data support; the text correctly calls it a "first-pass prior" (line 156), but the table itself is terse and could be over-used.

**Hidden issues for panel awareness**:
- There are two different "practical" modes that can blur: exhaustive per-pathogen rerun after labels/features exist (line 130) versus cold-start when labels are unavailable (line 156). The former is stronger operationally; the latter is more speculative.
- The chapter says DMS Layer C covers the "majority of the panel" (line 127), but 6/11 is a bare majority and not evenly distributed across all viral families; panel should avoid interpreting it as broad wet-lab validation across the full scope.

**Suggested score range**: 7.7--8.5

### I
**Strongest evidence**:
- Limitations awareness is unusually explicit: "residual risks concentrate" in Layer A heterogeneity, failure to transfer to forward time, and dual-use release restrictions (line 193).
- The defense limitations matrix covers concrete risks with mitigations: sampling bias, temporal-window dependence, PLM leakage, Simpson's paradox, winner's curse, small panel, independent reproduction, technical covariates, Layer A heterogeneity, sub-lineage pooling, scope, prospective gap, dual-use, and MAFFT artifact (lines 197-224).
- It states the deployment boundary directly: "retrospective prioritization only" and "not as a calibrated detector or family-conditional classifier" until callability and adaptive-method gates are met (line 254).

**Weakest evidence / gaps**:
- Several limitations are disclosed but unresolved by design: no independent Layer A recuration, no source-selection sensitivity, no IEDB-grade audit trail (line 49).
- The MAFFT `--auto` artifact is acknowledged as "expected effect is small but unquantified" (line 222), which is candid but leaves an input-quality weakness open.

**Hidden issues for panel awareness**:
- The limitations section may be so comprehensive that it buries the most damaging point: forward-time/prospective performance is weak, with grand mean AUROC 0.539 and 0/12 callable (lines 193, 220, 254).
- The "not algorithmically circular" phrase is true in a narrow sense (line 145), but the chapter also admits structural coupling of frequency and Layer A for HCV/Influenza B/Norovirus (lines 17-18). Panel should distinguish algorithmic circularity from label-signal coupling.

**Suggested score range**: 8.8--9.4

### J
**Strongest evidence**:
- The chapter is mature in claim calibration: it repeatedly narrows from detector/deployment to triage, e.g. "not a single universal algorithm" (line 177), "not a universal adaptive predictor" (line 286), and defense wording that explicitly says "not a prospective deployment claim" (line 298).
- It preserves reproducibility anchors: table captions cite source CSVs and distinguish legacy archives from current table sources (lines 82, 312-328), and code/data availability lists tag, commit hash location, licenses, and load-bearing files (lines 319-328).
- The chapter contains negative results rather than hiding them: adaptive redesign "is not adopted as a contribution" (line 239), Wave 4 leaves panel-size limits intact (line 247), and Wave 5 fires a negative provenance-sensitivity branch (line 250).

**Weakest evidence / gaps**:
- The chapter is dense and sometimes reads like a defense memo more than a dissertation discussion; lines 242-250 compress many audits, branches, nulls, and waves into long paragraphs that may overwhelm non-specialists.
- Some labels/anchors are awkwardly preserved via multiple `\phantomsection\label{...}` chains (lines 55-56, 180-191), suggesting anchor-preservation pressure after compression rather than clean chapter structure.

**Hidden issues for panel awareness**:
- The chapter actively helps maturity by admitting failed gates, but it may hurt perceived maturity if panelists see the wave/audit additions as late-stage patching rather than integrated scientific narrative.
- Internal consistency is mostly strong, but "Layer A positions across 12 pathogens" in the curation limitation (line 49), "11 RNA viruses" in contributions (line 235), and "current 12-pathogen panel" in audits (line 244) need oral clarification.

**Suggested score range**: 8.2--9.0

## Cross-cutting observations

- Chapter 5 actively helps panel-level interpretation for E, G, I, and J because it repeatedly converts high-risk claims into bounded retrospective triage claims.
- It also hurts any attempted "deployable detector" reading: the chapter explicitly reports 0/11 or 0/12 generalization/callability failures and states that prospective deployment is unsupported.
- The strongest hidden issue is denominator drift: 11-pathogen primary benchmark vs 12-pathogen audit/wave panel. This is probably explainable, but it is easy for a bulk-read panel to treat as inconsistency.
- Another subtle issue is that external validation is not symmetrical: HIV-1 carries most independent practical value, H3N2 is partly self-consistency, SARS-CoV-2 is exploratory, and Layer C is only 6/11.
- The chapter's clarity is locally high in claim wording but globally dense. The limitations matrix is excellent, while the wave/audit paragraphs risk exhausting readers.

## Bottom line for Stage 2 panel

Chapter 5 is not trying to rescue a deployable detector; it is doing the more mature thing of narrowing MutBench into a retrospective wet-lab triage framework. The strongest detail-aware takeaway is that interpretation, limitations, and practical value are all anchored by explicit caveats: HIV-1 is the main independent escape-validation anchor, Layer C gives a separate DMS axis for 6/11 pathogens, LOPO/callability failures block deployment, and the 4-feature cold-start recipe is a bounded heuristic rather than an optimized universal selector. The panel should reward the claim calibration, but should also notice the denominator drift between 11-pathogen primary results and 12-pathogen audit language.

RESULT_PROF_V8_STAGE1_ch5: in_scope_items=5 hidden_issues=10 recommended_score_floor=7.7 recommended_score_ceiling=9.4
