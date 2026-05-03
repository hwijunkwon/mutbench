# Phase 4 Professor Committee Simulation, Cycle 2

Scope: active English build inputs only (`front_en/abstract.tex`, `chapters_en/ch1_introduction.tex`, `chapters_en/ch3_methods.tex`, `chapters_en/ch4_results.tex`, `chapters_en/ch5_discussion.tex`). Orphan files were not used as evidence. Phase 3 CCB is consumed as supplied: 14 findings arbitrated, 12 prose-framing fixes required, 0 unresolved Critical findings, Phase 4 entry PASS. The Cycle 2 manuscript state was re-read at the edited locations before scoring.

## Gate Verdict

**PASS for this audit cycle.**

- Total score: **81.3 / 100**
- Lowest item mean: **7.7** (G. practical value)
- Phase 3 unresolved Critical findings: **0**

The applied Cycle 2 edits materially lift the cycle-1 concerns about over-staking. The abstract now qualifies the omega-squared claim under heterogeneous literature-curated Layer A labels (`front_en/abstract.tex:2`), bounds practical use with full-lattice, abstention, and Layer A' negative results (`front_en/abstract.tex:11`), and the introduction explicitly calls the 4-core a retrospective fixed historical recipe rather than a lattice-optimal or prospectively callable detector (`chapters_en/ch1_introduction.tex:156`). Chapter 4 likewise reframes Algorithm 1 as an exploratory search-space-reduction heuristic (`chapters_en/ch4_results.tex:696`) and Chapter 5 states that Layer A and Layer A' are non-interchangeable label provenances (`chapters_en/ch5_discussion.tex:278`).

## 10 x 10 Score Matrix

Columns A-J: A problem definition, B related work, C methodology, D experimental scale, E result interpretation, F originality, G practical value, H clarity, I limitations, J completion.

| Professor | A | B | C | D | E | F | G | H | I | J | Mean |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 1. Chair, bioinformatics | 9 | 8 | 9 | 8 | 8 | 8 | 8 | 8 | 9 | 9 | 8.4 |
| 2. Advisor, computer science | 9 | 8 | 8 | 8 | 8 | 8 | 8 | 8 | 9 | 8 | 8.2 |
| 3. Statistics/ML | 8 | 8 | 8 | 8 | 7 | 8 | 7 | 8 | 9 | 8 | 7.9 |
| 4. Computational biology | 9 | 8 | 8 | 8 | 8 | 8 | 8 | 8 | 9 | 8 | 8.2 |
| 5. Virology/public health | 9 | 8 | 8 | 8 | 8 | 8 | 8 | 8 | 9 | 8 | 8.2 |
| 6. VEP/PLM expert | 8 | 7 | 8 | 7 | 7 | 8 | 7 | 7 | 9 | 8 | 7.6 |
| 7. Benchmark methodology | 9 | 8 | 9 | 8 | 8 | 8 | 8 | 8 | 9 | 9 | 8.4 |
| 8. Practice/field user | 9 | 8 | 8 | 8 | 8 | 8 | 7 | 7 | 9 | 8 | 8.0 |
| 9. Statistical genetics | 8 | 8 | 9 | 8 | 8 | 8 | 8 | 8 | 9 | 8 | 8.2 |
| 10. Structural biology | 9 | 8 | 8 | 8 | 8 | 8 | 8 | 8 | 9 | 8 | 8.2 |

## Item Means

| Item | Mean |
|---|---:|
| A. 문제 정의 | 8.7 |
| B. 관련 연구 | 7.9 |
| C. 방법론 | 8.3 |
| D. 실험 규모 | 7.9 |
| E. 결과 해석 | 7.8 |
| F. 기여 독창성 | 8.0 |
| G. 실용 가치 | 7.7 |
| H. 서술 명확성 | 7.8 |
| I. 한계 인식 | 9.0 |
| J. 완성도 | 8.2 |

Total score is the sum of item means: **81.3 / 100**.

## Per-Item Rationale and Targeted Fixes for Means Below 8

**B. Related work, mean 7.9.** Strongest reason: the dissertation positions MutBench well against concurrent fitness-regression benchmarks, but the PLM/VEP distinction still requires careful reading because the Tranception channel is implemented as a lightweight ESM-2 proxy and is near-equivalent to ESM-2 for most pathogens (`chapters_en/ch5_discussion.tex:168`). Smallest targeted fix: add one compact sentence in the related-work comparison table or surrounding prose that separates true model-family comparison from proxy-channel comparison.

**D. Experimental scale, mean 7.9.** Strongest reason: 8,580 evaluations are broad for region-level hotspot detection, but cross-pathogen inference still rests on 11 pathogen clusters and the manuscript itself states this is below the 20-30 level usually preferred for stable random-effects estimation (`chapters_en/ch5_discussion.tex:179`). The Cycle 2 edit improves this by saying the selected viruses span a deliberately diverse but non-exhaustive range (`chapters_en/ch3_methods.tex:29`). Smallest targeted fix: add a one-row "what would change at 20-30 pathogens" note in the scale/limitations discussion, emphasizing inference rather than raw evaluation count.

**E. Result interpretation, mean 7.8.** Strongest reason: interpretation is now substantially better bounded, but the core result still mixes biology, curation protocol, and auxiliary-input quality. The manuscript discloses this directly: Layer A heterogeneity may inflate the interaction and MCC values are not absolutely comparable across pathogens (`chapters_en/ch5_discussion.tex:193`), and scoring inputs inherit tree, structure, and model-quality variation (`chapters_en/ch5_discussion.tex:188`). The Cycle 2 wording lifted the prior deduction by changing the ANOVA footnote to a bias-corrected modeled effect-size estimate (`chapters_en/ch4_results.tex:372`) and by adding the abstract caveat (`front_en/abstract.tex:2`). Smallest targeted fix: wherever "pathogen biology" is used as shorthand, prefer "pathogen-specific benchmark behavior" unless the evidence isolates biology from curation/input quality.

**G. Practical value, mean 7.7.** Strongest reason: the HIV-1 search-space-reduction anchor is useful, but deployability remains bounded: the abstract states the pre-registered callability rule abstains on 0/12 folds and Layer A' sensitivity is negative (`front_en/abstract.tex:11`), while Chapter 5 reiterates 0/12 prospective callability (`chapters_en/ch5_discussion.tex:307`). The Cycle 2 edits correctly downgrade Algorithm 1 to an exploratory heuristic (`chapters_en/ch4_results.tex:696`). Smallest targeted fix: add a one-paragraph "recommended use today" box: retrospective prioritization only, report abstention status, do not claim prospective detector performance without an expanded-panel validation.

**H. Clarity, mean 7.8.** Strongest reason: the dissertation is candid and technically rich, but the density of qualifications can obscure the main claim. Chapter 5's audit boundary is now split into Wave 1-3, Wave 4, and Wave 5 paragraphs (`chapters_en/ch5_discussion.tex:270`, `chapters_en/ch5_discussion.tex:274`, `chapters_en/ch5_discussion.tex:277`), which lifts the cycle-1 clarity deduction, but some long paragraphs remain hard to parse for committee readers. Smallest targeted fix: convert the main caveat cluster into a compact "claim / evidence / boundary" table.

## No Scores Below 6

No professor assigned any item score below 6, so no sub-6 one-sentence rationales are required.

## Diagnostic Criterion

Skill-defined diagnostic criterion, reported but not used as the gate:

- Mean >= 7: **PASS** (overall mean 8.13)
- Individual minimum >= 5: **PASS** (minimum individual item score 7)

## Committee Summary

The committee would view the updated dissertation as passable and defensible after Cycle 2. Its strongest areas are problem definition, limitation awareness, methodological breadth, and benchmark completion. The remaining deductions are not Critical blockers; they are scope and interpretation limits: only 11 pathogen clusters, heterogeneous Layer A provenance, proxy/collinearity in PLM channels, and practical use limited to retrospective prioritization until callability succeeds on a larger externally validated panel.
