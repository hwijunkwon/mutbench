# Phase 4 Professor Committee Simulation

Scope: active English build inputs only: `front_en/abstract.tex`, `chapters_en/ch1_introduction.tex`, `chapters_en/ch3_methods.tex`, `chapters_en/ch4_results.tex`, and `chapters_en/ch5_discussion.tex`. Orphan files were not used as evidence. Phase 3 CCB was consumed from `review/2026-05-02/phase3_ccb.md`.

## Gate Status

Phase 3 CCB reports 14 arbitrated findings: 2 already addressed, 12 fix-required prose-framing items, 0 invalid, and **0 unresolved Critical findings** (`review/2026-05-02/phase3_ccb.md:76-80`). Therefore the unresolved-Critical gate is finalized as satisfied.

Current-state committee score: **80.5 / 100**.

Audit-cycle gate:

- Total >= 80/100: **PASS**.
- No single item mean < 6: **PASS**.
- No unresolved Critical from Phase 3: **PASS**.

Overall verdict for this audit cycle: **PASS, with required prose-framing revisions before final submission**.

Diagnostic criterion only, not used as gate: mean >= 7 and individual minimum >= 5. Committee mean is 8.05 and the individual minimum score is 7, so the diagnostic criterion also passes.

## 10 x 10 Score Matrix

Scores use the requested anchors: 10 perfect, 9 excellent with minor improvements only, 8 good with concrete deductions, 7 acceptable with clear weaknesses, 6 weak and revision-needed, below 6 serious deficiency.

| Professor | A 문제 정의 | B 관련 연구 | C 방법론 | D 실험 규모 | E 결과 해석 | F 기여 독창성 | G 실용 가치 | H 서술 명확성 | I 한계 인식 | J 완성도 | Mean |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 1 Chair, bioinformatics | 9 | 8 | 8 | 8 | 8 | 8 | 8 | 8 | 8 | 8 | 8.1 |
| 2 Advisor, computer science | 8 | 8 | 8 | 8 | 8 | 8 | 8 | 8 | 8 | 8 | 8.0 |
| 3 Statistics/ML | 8 | 8 | 9 | 8 | 7 | 8 | 8 | 7 | 8 | 8 | 7.9 |
| 4 Computational biology | 8 | 8 | 8 | 8 | 8 | 8 | 8 | 7 | 8 | 8 | 7.9 |
| 5 Virology/public health | 9 | 8 | 8 | 8 | 8 | 8 | 8 | 8 | 8 | 8 | 8.1 |
| 6 VEP/PLM expert | 8 | 8 | 8 | 8 | 7 | 7 | 8 | 7 | 8 | 8 | 7.7 |
| 7 Benchmark methodology | 8 | 8 | 9 | 8 | 8 | 8 | 8 | 7 | 8 | 8 | 8.0 |
| 8 Practice/field user | 8 | 8 | 8 | 8 | 8 | 7 | 7 | 7 | 7 | 8 | 7.5 |
| 9 Statistical genetics | 9 | 8 | 9 | 9 | 8 | 8 | 8 | 8 | 8 | 9 | 8.3 |
| 10 Structural biology | 9 | 9 | 10 | 10 | 8 | 8 | 9 | 8 | 8 | 9 | 8.8 |

## Item Means

| Item | Mean |
|---|---:|
| A 문제 정의 | 8.4 |
| B 관련 연구 | 8.1 |
| C 방법론 | 8.5 |
| D 실험 규모 | 8.3 |
| E 결과 해석 | 7.8 |
| F 기여 독창성 | 7.8 |
| G 실용 가치 | 8.0 |
| H 서술 명확성 | 7.5 |
| I 한계 인식 | 7.9 |
| J 완성도 | 8.2 |

Total score is the sum of item means: **80.5 / 100**.

## Professor Means

| Professor | Mean |
|---|---:|
| 1 Chair, bioinformatics | 8.1 |
| 2 Advisor, computer science | 8.0 |
| 3 Statistics/ML | 7.9 |
| 4 Computational biology | 7.9 |
| 5 Virology/public health | 8.1 |
| 6 VEP/PLM expert | 7.7 |
| 7 Benchmark methodology | 8.0 |
| 8 Practice/field user | 7.5 |
| 9 Statistical genetics | 8.3 |
| 10 Structural biology | 8.8 |

No professor assigned any score below 6; therefore no below-6 individual-score rationale is required.

## Item-Level Rationale

**A. 문제 정의, mean 8.4.** The dissertation states a clear region-level hotspot-detection problem and distinguishes it from per-variant fitness benchmarks (`chapters_en/ch1_introduction.tex:33-39`). The scope is also explicit: 11 RNA viruses, surface glycoproteins, point substitutions only (`front_en/abstract.tex:2`; `chapters_en/ch3_methods.tex:37`). Deduction is minor: some practical framing still reads broader than the proven deployment regime, especially the generic candidate-list reduction language in the abstract (`front_en/abstract.tex:11`).

**B. 관련 연구, mean 8.1.** The manuscript positions MutBench against ViroGym, EVEREST, ProteinGym, EVEscape, and related fitness-regression work while preserving task distinction (`chapters_en/ch1_introduction.tex:33`; `chapters_en/ch5_discussion.tex:46`). Deduction is modest: the broadest-benchmark claim is acceptable only because it is carefully scoped to region-level, single-position hotspot detection (`front_en/abstract.tex:4`), and should remain guarded.

**C. 방법론, mean 8.5.** Methods are strong: the benchmark design, MCC definition, metric separation, ANOVA design, cell-level omega check, ANCOVA, and Bayesian cross-check are described in detail (`chapters_en/ch3_methods.tex:775-820`). The committee views the methodology as dissertation-sufficient. Residual deduction reflects dependence among detector variants and heterogeneous Layer A definitions, both acknowledged rather than hidden (`chapters_en/ch3_methods.tex:813-816`; `chapters_en/ch3_methods.tex:306`).

**D. 실험 규모, mean 8.3.** The 8,580-cell grid across 20 scoring formulas, 39 detector variants, and 11 pathogens is substantial (`front_en/abstract.tex:2`; `chapters_en/ch3_methods.tex:5-7`). The scale is strongest for benchmark comparison, weaker for learning pathogen-to-method selection because n=11 pathogens is small; the manuscript acknowledges that adaptive deployment needs 20-30+ pathogens (`chapters_en/ch5_discussion.tex:291`, `chapters_en/ch5_discussion.tex:299`).

**E. 결과 해석, mean 7.8.** Strongest reason for deduction: several interpretations remain slightly over-causal or under-qualified in first-pass prose. The abstract foregrounds omega-squared without carrying the curation-protocol caveat that Layer A partly confounds biology and annotation protocol (`front_en/abstract.tex:2`, compared with heterogeneity disclosure at `chapters_en/ch3_methods.tex:306`). The table footnote still describes omega-squared as "proportion of total variance explained" (`chapters_en/ch4_results.tex:372`), whereas the methods/results discussion elsewhere correctly frames it as a bias-corrected modeled estimate (`chapters_en/ch3_methods.tex:814`; `chapters_en/ch4_results.tex:383`). The adaptive-weighting discussion also says the failures "isolate the constraint to the panel size itself" (`chapters_en/ch4_results.tex:857`), which is stronger than the evidence permits. Smallest targeted fix: apply the Phase 3 wording at `front_en/abstract.tex:2`, `chapters_en/ch4_results.tex:372`, and `chapters_en/ch4_results.tex:857` to make the caveats local to the claims.

**F. 기여 독창성, mean 7.8.** Strongest reason for deduction: the benchmark and decomposition contribution are original and useful, but the cold-start contribution is still framed more strongly than the final audits support. Contribution 3 calls the 4-feature core a practical cold-start recipe (`chapters_en/ch1_introduction.tex:154-156`), while the audit paragraph reports full-lattice rank 87/1023, a slightly better 3-core, 0/12 callability, and negative Layer A' transfer (`chapters_en/ch5_discussion.tex:272`, `chapters_en/ch5_discussion.tex:301`). The Chapter 4 algorithm paragraph also says the evidence operationalizes into a deployable algorithm (`chapters_en/ch4_results.tex:696`) and later says the baseline comparison defends it as "a method rather than a heuristic" (`chapters_en/ch4_results.tex:725`). Smallest targeted fix: relabel this contribution consistently as a retrospective search-space-reduction heuristic, not a prospectively callable detector or lattice-optimal method.

**G. 실용 가치, mean 8.0.** Practical value is real but bounded. The strongest anchor is HIV-1 vaccine-escape enrichment with high Layer-A-disjoint proportion (`front_en/abstract.tex:11`; `chapters_en/ch4_results.tex:943-952`). The committee does not deduct below 8 because the manuscript now discloses that validation is feasible for only 3/11 pathogens and explains why (`chapters_en/ch4_results.tex:949`). Remaining practical risk is the abstention result: 0/12 folds are callable under the pre-registered rule (`chapters_en/ch5_discussion.tex:301`), so deployment should be presented as triage guidance only.

**H. 서술 명확성, mean 7.5.** Strongest reason for deduction: the dissertation contains the required caveats, but some are too far from the claims they qualify. The abstract's search-space-reduction and 4-core compactness sentence (`front_en/abstract.tex:11`) omits the full-lattice downgrade and Layer A' negative transfer later disclosed in Chapter 5 (`chapters_en/ch5_discussion.tex:272`, `chapters_en/ch5_discussion.tex:301`). The dense Wave 1-5 audit paragraph combines multiple audit families in one long paragraph (`chapters_en/ch5_discussion.tex:272`), making the defense logic harder to follow. Smallest targeted fix: make the Phase 3 abstract sentence edits and split the Chapter 5 audit paragraph into the three suggested blocks.

**I. 한계 인식, mean 7.9.** Strongest reason for deduction: limitations are extensive and generally candid, but several limiting facts need to be moved closer to the claims they limit. The limitations table is strong on scope, ground-truth incompleteness, phylogenetic/sampling bias, and panel size (`chapters_en/ch5_discussion.tex:250-268`). However, first-page prose still under-qualifies the abstention and Layer A' boundaries (`front_en/abstract.tex:11`). Smallest targeted fix: add the Phase 3 abstract sentence noting 0/12 callability and negative Layer A' sensitivity.

**J. 완성도, mean 8.2.** The active manuscript is mature, evidence-rich, and internally audited. The completion deduction is for final-pass prose alignment, not missing core experiments: Phase 3 classifies all remaining items as prose-framing fixes rather than fabrication, concealment, or active-build defects (`review/2026-05-02/phase3_ccb.md:78-80`). The final polish should prioritize claim-local caveats and removal of over-deployment language.

## Committee Synthesis

The dissertation is above the pass threshold in its current state because the main benchmark contribution, statistical design, and practical HIV-1 anchor are coherent and well documented. The major remaining risk is rhetorical: several headline passages still state the strongest version of the contribution before the reader sees the audits that narrow it. Phase 3's 12 required fixes are therefore correctly characterized as prose-framing revisions. Applying them would most directly lift H, F, I, and E; it would likely raise the total score into the mid-80s without requiring new experiments.
