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
- The chapter interprets the main result as an information-source effect, not a detector-family win: "Detection-family choice contributes little variance ($\omega^2=0.013$), about 23 times less than the scoring~$\times$~pathogen interaction ($\omega^2=0.296$)" and the operational implication is "wet-lab triage---choose the information source" (line 68).
- It explicitly limits LOPO: "LOPO gives 0/11 exact matches, Friedman gives $p=0.990$, and the oracle-vs-generalised gap is $0.265$" as evidence the mapping is "not yet learnable" at $n=11$ (line 70); later, LOPO 0/11 is "corroborative" rather than independent evidence (line 237).
- It makes low MCC interpretable: "Mean oracle MCC across 11 pathogens is $0.341$" but this is attributed to exact matching, imbalance, and ground-truth stringency; windowed MCC rises to $0.472$ at $\pm5$ (lines 78, 80-109).

**Weakest evidence / gaps**:
- The statistical interpretation relies heavily on cross-references to Chapter 4; Chapter 5 gives polished conclusions more than the underlying ANOVA/wild-cluster diagnostic detail.
- Some interpretation is technically careful but hard to audit in one pass, especially the EqualWeight/HIV-1/H3N2 comparison and winner's-curse distinction (line 128).

**Hidden issues for panel awareness**:
- Denominator drift: primary claims use 11 pathogens (lines 68, 121, 235-236), while audit/wave material uses "current 12-pathogen panel" and "0/12 callable" (lines 244, 254). Likely explainable, but easy to read as inconsistency.
- Possible stale numeric anchor: line 121 says "$\omega^2 = 0.234$ at the cell level," while the cleanup state says ANCOVA/cell values were updated to 0.233/0.274; line 216 uses "0.233 to 0.274." Panel should not conflate these.
- "With benchmark validity established" (line 52) sounds stronger than the following H-score saturation and homoplasy limitations warrant.

**Suggested score range**: 8.0--8.8

### F
**Strongest evidence**:
- The contribution is concrete and scoped: "broadest region-level, single-position hotspot-detection benchmark to date for RNA viruses" with "10 biological information types (20 scoring formulas) $\times$ 14 detection families (39 variants) $\times$ 11 RNA viruses = 8,580 evaluations" (line 235).
- It distinguishes MutBench from nearby benchmarks: EVEREST and ProteinGym target "per-variant fitness or escape prediction," whereas MutBench evaluates "region-level hotspot prioritization" (line 72); ViroGym/EVEREST head-to-head is deferred because tasks differ (lines 147-150).
- The novel result is sharply stated: pathogen-dependent information source choice, $\omega^2=0.296$ with cluster-bootstrap CI [0.201, 0.346], 9 distinct optimal information types, and oracle-vs-generalized MCC gap 0.265 (line 236).

**Weakest evidence / gaps**:
- "Broadest ... to date" remains a fragile phrase unless the related-work comparison elsewhere is exhaustive; this chapter only briefly names EVEREST, ProteinGym, and ViroGym.
- The 4-feature core is framed as a recipe (lines 5, 238), but later audits say it is "strictly dominated by the 3-feature variant" and a "historical fixed configuration" (line 244).

**Hidden issues for panel awareness**:
- The cold-start core is not an optimized discovery; it is a bounded heuristic retained after negative audits, with pLDDT only an "optional structural extension" after Shapley analysis (line 244).
- Layer A' failure limits generality: "Layer A and Layer A' are not interchangeable label provenances" (line 250), so the contribution is this literature-curated benchmark, not a universal label-provenance framework.

**Suggested score range**: 8.0--8.7

### G
**Strongest evidence**:
- The wet-lab value is anchored on two axes: "Layer~C DMS validation directly measures functional impact in the laboratory" and covers "6 of 11 pathogens" / 650 positions, with Layer C MCC $0.139$--$0.322$ and Layer C-best scoring differing from Layer A-best in all 6 (line 127).
- Practical value is correctly framed as triage: "reducing the experimental search space rather than achieving high absolute prediction accuracy" (line 128); contribution summary says typical candidate lists narrow from "~1,000 to approximately 10--50 positions" with $7$--$9\times$ enrichment (line 238).
- The workflow is operational: sequence thresholds, MAFFT, feature costs, GPU/CPU runtimes, detector-grid timing, family priors, and a cold-start option are all specified (line 156; table lines 158-175).

**Weakest evidence / gaps**:
- The chapter admits "the practical-value claim rests mainly on HIV-1" (line 145); H3N2 is self-consistency and SARS-CoV-2 exploratory after correction (lines 142-145, 286).
- The family-level recommendation table is useful but thin for decision-making; the text wisely calls it a "first-pass prior" (line 156), but the table itself may look more prescriptive than the evidence supports.

**Hidden issues for panel awareness**:
- Two practical regimes are easy to blur: exhaustive per-pathogen rerun after features/labels exist (line 130) versus cold-start prioritization when labels are unavailable (line 156). The former is better supported.
- "Layer C covers the majority of the panel" (line 127) is technically true at 6/11 but a bare majority and not equivalent to broad wet-lab coverage across all families.

**Suggested score range**: 7.7--8.5

### I
**Strongest evidence**:
- The limitations are explicit and examiner-facing: residual risks are Layer A heterogeneity, poor forward-time transfer, and dual-use release constraints (line 193).
- The defense limitations matrix is unusually comprehensive: sampling bias, temporal dependence, PLM leakage, Simpson's paradox, winner's curse, small $n$, reproduction, covariates, label heterogeneity, sub-lineage pooling, scope, prospective gap, dual use, and MAFFT artifact (lines 197-224).
- Deployment boundaries are direct: recommended use is "retrospective prioritization only" and Algorithm 1 is "not as a calibrated detector or family-conditional classifier" until callability and adaptive-method gates are met (line 254).

**Weakest evidence / gaps**:
- Some limitations remain unresolved: no independent recuration, no inter-annotator agreement, no source-selection sensitivity, and no IEDB-grade audit trail (line 49).
- MAFFT `--auto` is acknowledged but unquantified: expected small effect, but no single-mode sensitivity rerun (line 222).

**Hidden issues for panel awareness**:
- The most damaging limitation can get buried by the matrix: forward/prospective performance is weak, with grand mean AUROC 0.539 and 0/12 callable (lines 193, 220, 254).
- "Not algorithmically circular" (line 145) is narrow; line 18 still admits frequency scoring is partly structural for HCV/Influenza B/Norovirus due to label-signal coupling.

**Suggested score range**: 8.8--9.4

### J
**Strongest evidence**:
- The chapter is mature in claim calibration: "not a single universal algorithm" (line 177), "not a universal adaptive predictor" (line 286), and defense wording says HIV-1 is "not a prospective deployment claim" (line 298).
- It preserves reproducibility anchors: table captions identify source CSVs and legacy archive caveats (line 82), and code/data availability lists release tag, commit hash location, licenses, redistributed artifacts, runtime, and load-bearing files (lines 319-328).
- It reports negative results rather than hiding them: adaptive fusion "is not adopted as a contribution" (line 239), Wave 4 leaves the panel-size limit open (line 247), and Wave 5 reports negative provenance sensitivity (line 250).

**Weakest evidence / gaps**:
- The chapter sometimes reads like a defense audit memo rather than an integrated discussion; lines 242-250 compress many waves, nulls, branches, and sensitivity checks into long paragraphs.
- Multiple `\phantomsection\label{...}` chains (lines 55-56, 180-191) show anchor-preservation pressure after compression and make the source feel patched.

**Hidden issues for panel awareness**:
- The late wave/audit material helps maturity by narrowing claims, but may hurt perceived polish if panelists read it as last-minute claim containment.
- Internal consistency is mostly good, but line 49 uses 12-pathogen Layer A curation language, the contribution uses 11 RNA viruses (line 235), and audits use 12-pathogen language (line 244). This needs oral clarification.

**Suggested score range**: 8.2--9.0

## Cross-cutting observations

- Chapter 5 actively HELPS panel-level interpretation for E, G, I, and J by converting risky "detector" language into bounded retrospective wet-lab triage.
- It actively HURTS any deployable-detector interpretation: LOPO 0/11, 0/12 callability, Layer A' failure, and weak prospective transfer are all disclosed.
- The biggest hidden issue is denominator/numeric drift: 11 vs 12 pathogens, plus the 0.234 vs 0.233/0.274 interaction anchors.
- External validation is asymmetric: HIV-1 carries the strongest independent practical-value claim; H3N2 is partly self-consistency; SARS-CoV-2 is exploratory; Layer C is 6/11.
- Clarity is strong at the sentence-claim level but dense globally. The limitations matrix is excellent; the wave/audit paragraphs are the main readability risk.

## Bottom line for Stage 2 panel

Chapter 5 should be read as a mature narrowing chapter, not as a rescue of a deployable detector. The detail-aware reading is that MutBench's defensible endpoint is retrospective wet-lab triage: HIV-1 is the main independent escape-validation anchor, Layer C supplies a separate DMS axis for 6/11 pathogens, and the cold-start 4-core is a bounded heuristic rather than an optimized universal selector. The panel should reward the claim calibration and limitations awareness, while watching the subtle denominator/numeric drift that a bulk read could miss.

RESULT_PROF_V9_STAGE1_ch5: in_scope_items=5 hidden_issues=12 recommended_score_floor=7.7 recommended_score_ceiling=9.4
