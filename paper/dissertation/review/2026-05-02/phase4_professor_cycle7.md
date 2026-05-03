# Phase 4 Professor Committee Simulation, Cycle 7

Scope: active English build inputs only (`front_en/abstract.tex`, `chapters_en/ch1_introduction.tex`, `chapters_en/ch3_methods.tex`, `chapters_en/ch4_results.tex`, `chapters_en/ch5_discussion.tex`). Orphan files were not used as evidence. Phase 3 CCB summary was supplied at execution time: **0 unresolved Critical findings, Phase 4 entry PASS**.

## Gate Verdict

**PASS for this audit cycle.**

- Total score: **83.9 / 100**
- Lowest item mean: **8.1** (B. 관련 연구, D. 실험 규모, E. 결과 해석, F. 기여 독창성)
- Phase 3 unresolved Critical findings: **0**
- Gate result: total >= 80, no item mean < 6, and no unresolved Critical findings.

Cycle 7 improves the main Cycle 5 weakness: defense readability. The panel-scope summary now explicitly separates the 11-pathogen main panel, the 12-pathogen Stage 3 feature-ablation panel, and the Wave 4-5 features-only sensitivity panels (`chapters_en/ch1_introduction.tex:89`). Chapter 5 now includes a Layer A provenance table (`chapters_en/ch5_discussion.tex:24`) and a defense-map table that gives claim, evidence tier, boundary, and allowed oral wording (`chapters_en/ch5_discussion.tex:329`). These additions lift H from a borderline-good score to a solid good/excellent score. The remaining deductions are substantive rather than cosmetic: Layer A remains single-team and source-dominated in places (`chapters_en/ch5_discussion.tex:48`-`49`), external escape validation remains available for only 3/11 pathogens (`chapters_en/ch4_results.tex:905` and `chapters_en/ch4_results.tex:939`), and the prospective callability rule still abstains on 0/12 folds (`chapters_en/ch4_results.tex:806`-`808`).

## Committee Matrix

Columns A-J: A problem definition, B related work, C methodology, D experimental scale, E result interpretation, F originality, G practical value, H clarity, I limitations, J completion.

| Professor | A | B | C | D | E | F | G | H | I | J | Mean |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 1. Chair, bioinformatics | 9 | 8 | 9 | 8 | 8 | 8 | 8 | 9 | 9 | 9 | 8.5 |
| 2. Advisor, computer science | 9 | 8 | 8 | 8 | 8 | 8 | 8 | 9 | 9 | 8 | 8.3 |
| 3. Statistics/ML | 8 | 8 | 9 | 8 | 8 | 8 | 8 | 8 | 9 | 8 | 8.2 |
| 4. Computational biology | 9 | 8 | 9 | 8 | 8 | 8 | 8 | 9 | 9 | 8 | 8.4 |
| 5. Virology/public health | 9 | 8 | 8 | 8 | 8 | 8 | 9 | 9 | 9 | 8 | 8.4 |
| 6. VEP/PLM expert | 8 | 9 | 8 | 8 | 8 | 9 | 8 | 8 | 9 | 8 | 8.3 |
| 7. Benchmark methodology | 9 | 8 | 9 | 9 | 8 | 8 | 8 | 9 | 10 | 9 | 8.7 |
| 8. Practice/field user | 9 | 8 | 8 | 8 | 8 | 8 | 8 | 8 | 9 | 8 | 8.2 |
| 9. Statistical genetics | 8 | 8 | 9 | 8 | 9 | 8 | 8 | 8 | 10 | 8 | 8.4 |
| 10. Structural biology | 9 | 8 | 8 | 8 | 8 | 8 | 9 | 9 | 9 | 9 | 8.5 |

## Item Means

| Item | Mean |
|---|---:|
| A. 문제 정의 | 8.7 |
| B. 관련 연구 | 8.1 |
| C. 방법론 | 8.5 |
| D. 실험 규모 | 8.1 |
| E. 결과 해석 | 8.1 |
| F. 기여 독창성 | 8.1 |
| G. 실용 가치 | 8.2 |
| H. 서술 명확성 | 8.6 |
| I. 한계 인식 | 9.2 |
| J. 완성도 | 8.3 |

Total score is the sum of item means: **83.9 / 100**.

## Per-Item Rationale

**A. 문제 정의, mean 8.7.** The problem is now well scoped to region-level, single-position hotspot detection for RNA-virus surface glycoproteins, point substitutions only (`front_en/abstract.tex:2`). The panel-scope summary removes a prior ambiguity by assigning the 11-pathogen, 12-pathogen, and Wave 4-5 panels to distinct inferential roles (`chapters_en/ch1_introduction.tex:89`). Deduction is minor: the dissertation still requires the reader to track several nested panels.

**B. 관련 연구, mean 8.1.** The manuscript positions MutBench against per-variant fitness or escape-prediction benchmarks and states that it targets region-level detection rather than variant fitness (`chapters_en/ch5_discussion.tex:76`). Deduction remains because the PLM/VEP-related framing is necessarily proxy-based and collinear at headline granularity; the abstract itself notes Tranception/ESM-2 channel collinearity is not separated at headline level (`front_en/abstract.tex:13`).

**C. 방법론, mean 8.5.** The methods are strong: thresholds and the ANOVA grid are preregistered (`chapters_en/ch3_methods.tex:209`), the production EqualWeight column is separated from label-aware nested-LOPO ablation (`chapters_en/ch3_methods.tex:617`-`620`), and the vaccine-escape Bonferroni denominator is explicit (`chapters_en/ch3_methods.tex:825`). Deduction remains because Layer A is operationally heterogeneous rather than a uniform assay-derived label set (`chapters_en/ch3_methods.tex:207`).

**D. 실험 규모, mean 8.1.** The 8,580-evaluation main benchmark is substantial for a dissertation (`chapters_en/ch1_introduction.tex:86`), and the audit programme adds useful sensitivity analyses. The limiting factor is not detector count but cross-pathogen inference: 11 pathogen clusters remain below the 20-30 level discussed for stable random-effects estimation (`chapters_en/ch5_discussion.tex:209`). External practical validation is also restricted to 3/11 pathogens by annotation availability (`front_en/abstract.tex:11`).

**E. 결과 해석, mean 8.1.** Interpretation is careful in the updated state. The abstract and discussion explicitly state that LOPO 0/11 is null-consistent and not standalone proof (`front_en/abstract.tex:10`; `chapters_en/ch5_discussion.tex:268`). The strongest deduction is causal isolation: pathogen-specific benchmark behavior still mixes biology, curation protocol, and auxiliary input quality; Chapter 4 states this boundary directly (`chapters_en/ch4_results.tex:894`-`895`).

**F. 기여 독창성, mean 8.1.** The originality is credible: a region-level, multi-information-source benchmark across 11 RNA-virus targets is a distinct contribution (`chapters_en/ch1_introduction.tex:151`-`158`). Deduction is that the practical algorithmic output is a bounded retrospective heuristic, not a prospectively callable detector; Chapter 4 now says the cold-start recipe is exploratory and not callable under P5 (`chapters_en/ch4_results.tex:696`).

**G. 실용 가치, mean 8.2.** Cycle 7 improves practical defensibility by softening the claim to retrospective practical relevance and by giving recommended-use boundaries. HIV-1 remains a strong external anchor with 82% Layer-A-disjoint novel-only enrichment (`front_en/abstract.tex:11`; `chapters_en/ch5_discussion.tex:125`). The deduction remains deployment-facing: the current abstention rule refuses all 12 folds (`chapters_en/ch4_results.tex:808`), and Chapter 5 restricts near-term use to retrospective prioritization (`chapters_en/ch5_discussion.tex:302`).

**H. 서술 명확성, mean 8.6.** This is the largest Cycle 7 improvement. The panel-scope summary in Chapter 1 (`chapters_en/ch1_introduction.tex:89`), the Layer A provenance table in Chapter 5 (`chapters_en/ch5_discussion.tex:24`), and the defense map (`chapters_en/ch5_discussion.tex:329`) make the claim/evidence/boundary structure much easier to defend. Deduction is only residual: the abstract is still dense because it carries many necessary caveats (`front_en/abstract.tex:10`-`13`).

**I. 한계 인식, mean 9.2.** The dissertation is unusually explicit about its boundaries: Layer A curation reproducibility limits are stated (`chapters_en/ch5_discussion.tex:48`-`49`), the Layer A' sensitivity result is negative and treated as label-provenance non-equivalence (`chapters_en/ch4_results.tex:820`), and falsification criteria are specified (`chapters_en/ch5_discussion.tex:365`). Remaining deduction is executional: independent recuration, source-selection sensitivity, and time-forward validation are still future work.

**J. 완성도, mean 8.3.** The manuscript is now defense-ready under this audit cycle: the core evidence is bounded, the critical gate is clear, and CSV/table provenance is listed in Chapter 5 (`chapters_en/ch5_discussion.tex:384`-`393`). Deduction remains for final-production polish: the Zenodo DOI is still described as future insertion (`chapters_en/ch5_discussion.tex:378`), and some numerical caveats remain disclosed rather than eliminated.

## Items Below 8

No item mean is below 8. Therefore no mandatory mean-<8 targeted fixes are triggered. The smallest useful remaining fixes are: independent recuration of a Layer A subset with agreement statistics; expanded external escape or time-forward validation beyond the current 3/11 pathogens; and insertion of the final Zenodo DOI.

## Sub-6 Scores

No professor assigned any item score below 6, so no sub-6 one-sentence rationales are required.

## Diagnostic Criterion

Skill-defined diagnostic criterion, reported but not used as the gate:

- Mean >= 7: **PASS** (overall mean 8.39)
- Individual minimum >= 5: **PASS** (minimum individual score 8)

## Overall Assessment

The Cycle 7 manuscript passes the simulated committee gate. The dissertation is no longer failing on defense readability: claim boundaries are visible early, provenance is summarized, and the oral-defense wording is explicitly constrained. The remaining weaknesses are appropriate dissertation limitations rather than gate blockers: external validation breadth, Layer A reproducibility, and prospective callability remain the major targets for post-defense work.
