# Chapter Deep Eval: ch3_methods

## In-scope rubric items
- C
- D
- H

## Per-item evidence

### C
**Strongest evidence**:
- Clear full-pipeline contract: "three-component pipeline architecture" with "(1) ground truth construction", "(2) systematic scoring and detection", and "(3) multi-metric evaluation with factorial statistical analysis" (lines 81--82).
- Ground-truth construction is operationally explicit and non-circular: Layer A is "literature-curated adaptive or diversifying positions treated as hotspot positives for MCC" and "no computational tool was applied to identify new convergent evolution positions" (lines 214--223).
- Strong statistical-methods transparency: the ANOVA uses "8,580 evaluation rows" with scoring, family, pathogen, and interactions, while acknowledging that the effective unit is closer to "3,080 scoring--family--pathogen cells" and reporting cell-level omega as the conservative reference (lines 764--768).

**Weakest evidence / gaps**:
- Several important channels are proxies rather than full implementations: "Tranception" is "computed using ESM-2 masked-marginal pseudo-perplexity as a lightweight proxy" and original Tranception "was not run directly" (line 585); EVEscape substitutes ESM-2 for EVE because "EVE training is not feasible" (lines 624--625).
- Some robustness checks are incomplete or deferred: Layer C threshold robustness is "verified on 4 of 6 DMS pathogens" with Rabies/EV-A71 deferred (line 242); HMMER filtering is "not applied" and left for the next curation cycle (line 37).

**Hidden issues for panel awareness**:
- Homoplasy implementation has a subtle internal conflict: the scoring section says trees were reconstructed with "IQ-TREE 2" and homoplasy by Fitch parsimony on "the resulting maximum-likelihood tree" (line 545), but the TreeTime audit note says Stage 2 production homoplasy is Fitch parsimony on a "FastTree ML approximation" (line 480). A bulk reader may miss that the production tree source is ambiguous.
- The methods chapter carries result claims inside methods, e.g. MutClust-Hybrid "achieves the highest hotspot-score" (line 423), detector family contributes only omega = 0.013 (line 678), and ANCOVA/omega results (lines 768--772). This helps reproducibility but blurs methods/results boundaries.
- Layer B is introduced as "true negatives" (line 227) but later clarified as not universal MCC negatives, only a constrained-FPR audit set (lines 230--232, 203--205). The contract is ultimately clear, but the initial phrasing can mislead skimming panelists.

**Suggested score range**: 8.0--8.8. Methodology is detailed, auditable, and guarded, but proxy channels, deferred checks, and the homoplasy-source inconsistency keep it below a near-perfect methods score.

### D
**Strongest evidence**:
- Broad pathogen panel: "Eleven RNA viruses" spanning respiratory, blood-borne/sexually transmitted, enteric, arthropod-borne, and neurotropic groups (lines 21--26), with "8 ICTV viral families and four transmission routes" (line 34).
- Substantial computational grid: Stage 2 evaluates "20 scoring types x 39 detection parameter variants ... x 11 pathogens = 8,580 combinations" (line 492), summarized as 20 scoring types in six categories (lines 498--535) and 39 methods in 14 families (lines 637--667).
- Sequence-scale documentation is concrete: Table 3.1 lists per-pathogen sequences, unique sequences, alignment lengths, query dates, and MAFFT modes, with unique counts ranging from 530 to 5,019 and lengths from 261 to 1,330 AA (lines 52--64).

**Weakest evidence / gaps**:
- Breadth is explicitly non-exhaustive and uneven: the chapter says the benchmark covers a "deliberately diverse but non-exhaustive range" (line 29), while Zika is excluded from Stage 2 because only 52 unique sequences were available (line 30).
- Ground-truth breadth is uneven: Layer C is available for only six pathogens (lines 240, 320--322), and HCV has "effective Layer B = 0" due to coordinate-handling caveats (lines 304, 314).

**Hidden issues for panel awareness**:
- Detection-category labels drift. The chapter opening says 14 families span five categories including "adaptive window" (line 6), while Table 3.6 uses Threshold-based, Signal processing, Density and clustering, Statistical/model-based, and Legacy (lines 652--665). "AdaptWin" is listed under Threshold-based, not an adaptive-window category.
- Table 3.8 includes a Zika row even though the table caption says "11 benchmark pathogens" and Zika is only Stage 3/supplementary (lines 554--579). The footnote explains this, but the table visually weakens the clean 11-pathogen boundary.
- The design-characteristics paragraph states temporal coverage is "~2--50 years" (line 712), while the table above lists a minimum of "~5 yr" (lines 697--707). This is a small anchor-preservation slip that can matter in a methods audit.

**Suggested score range**: 8.2--9.0. Scale is one of the chapter's strongest dimensions: the panel is broad for wet-lab triage benchmarking, and the grid is large. Deductions mainly come from uneven ground truth and a few scope/labeling slips.

### H
**Strongest evidence**:
- The chapter opens with a useful roadmap: it names the framework, pathogen count, scoring/detection counts, ground-truth layers, and section order in the first 11 lines (lines 5--11).
- Tables and captions are unusually self-contained: Table 3.1 defines query dates and MAFFT modes (lines 44--70), Table 3.3 defines DMS preprocessing and source releases (lines 246--268), and Table 3.6 ties detector parameter names to the archived CSV strings (lines 641--674).
- Limitations and caveats are written inline rather than hidden: examples include "not a universal non-hotspot label" for Layer B (lines 203--205), the AlphaFold-Multimer/SASA limitation (line 551), and the Tranception--ESM-2 redundancy caveat (lines 585--586).

**Weakest evidence / gaps**:
- The chapter is dense. Very long paragraphs combine materials, preprocessing, exclusions, provenance, tool choices, and limitations in one block, especially the GenBank/MSA paragraph (lines 37--41) and AI-based scoring section (lines 583--586).
- Some phrasing is overloaded for a methods chapter: repeated references to headline omega, vaccine-escape denominators, and downstream chapter conclusions make it harder to separate protocol from findings (lines 221, 678, 768--776).

**Hidden issues for panel awareness**:
- Title grammar is slightly unpolished: "Materials and Method" (line 2) rather than the standard "Materials and Methods." Minor, but it is first-viewport prose.
- Stage labels may confuse readers: line 7 says a "two-stage main design with a Stage 3 information-integration layer," while other file/result names use "stage3" for the full result archive. The text mostly clarifies this, but the terminology is cognitively heavy.
- Figure 3.1 text says "Scoring Types (6 categories, 20 types)" and "Detection Methods (39 methods, 14 families)" (lines 95--107), while the opening says detection spans "5 categories" (line 6). The figure is readable, but category accounting is not fully synchronized.

**Suggested score range**: 7.6--8.4. Clarity is strong at the evidence-table level and weaker at the prose-compression level. A strict professor may penalize density and category drift; a methods-oriented reader may value the caveat-rich style.

## Cross-cutting observations

- This chapter actively HELPS C and D panel interpretation by exposing many potential attacks before reviewers need to infer them: preregistration, exact query dates, threshold choices, Layer A/B/C conflict handling, LOPO definitions, cluster-bootstrap caveats, and license/provenance details are all documented.
- It can mildly HURT H because the same defensive thoroughness creates high reading load. Several sentences are doing the work of methods, results, limitations, and audit response simultaneously.
- The most important hidden technical issue is the production homoplasy tree-source mismatch (IQ-TREE vs FastTree). Because homoplasy is one of the central information types, Stage 2 should treat this as a clarification target even if it likely does not change the rubric score much.
- The chapter is well aligned with the wet-lab triage reframing: MCC, constrained FPR, DMS F1, vaccine-escape cross-validation, and explicit false-positive cost language all support a follow-up prioritization tool rather than a deployable detector.

## Bottom line for Stage 2 panel

Bulk readers will likely notice the impressive scale but may miss that the methodological maturity is carried by many small guardrails: pre-frozen thresholds, non-merged ground-truth layers, cell-level omega, cluster-aware intervals, and explicit proxy-channel caveats. The chapter is strongest on C and D, but the panel should discount slightly for implementation-label drift: homoplasy's production tree source is inconsistent, detection category labels are not perfectly synchronized, and Zika/Stage 3 rows blur the 11-pathogen boundary. These are clarification-level issues, not fatal design flaws.

RESULT_PROF_V9_STAGE1_ch3: in_scope_items=3 hidden_issues=9 recommended_score_floor=7.6 recommended_score_ceiling=9.0
