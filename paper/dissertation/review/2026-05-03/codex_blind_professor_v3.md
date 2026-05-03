# Codex Blind Professor Evaluation v3

Scope audited: post-compression active English manuscript only: `front_en/abstract.tex`, `chapters_en/ch1_introduction.tex` with active `ch2_background.tex` input, `chapters_en/ch3_methods.tex`, `chapters_en/ch4_results.tex`, and `chapters_en/ch5_discussion.tex`. I did not use orphan `chapters_en/ch5_adapt.tex` or any review report as manuscript evidence. I consulted v2 only after independent scoring to compute the required deltas.

## 1. 10 x 10 Score Matrix

Scores are 0-10 for rubric items A-J.

| # | Role | A | B | C | D | E | F | G | H | I | J | Total |
|---:|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 1 | Chair (bioinformatics) | 8.6 | 8.7 | 8.0 | 8.2 | 8.1 | 8.6 | 8.1 | 8.5 | 8.7 | 8.3 | 83.8 |
| 2 | Advisor (CS) | 8.8 | 8.6 | 8.2 | 8.3 | 8.1 | 8.6 | 8.2 | 8.5 | 8.8 | 8.4 | 84.5 |
| 3 | Statistics-strict | 8.3 | 8.4 | 7.2 | 7.8 | 7.4 | 8.1 | 7.6 | 8.0 | 8.5 | 7.6 | 78.9 |
| 4 | Computational Biology | 8.5 | 8.4 | 7.8 | 8.0 | 7.8 | 8.3 | 7.9 | 8.3 | 8.7 | 8.1 | 81.8 |
| 5 | Virology / public health | 8.6 | 8.5 | 7.7 | 8.0 | 7.9 | 8.1 | 8.0 | 8.3 | 8.9 | 8.1 | 82.1 |
| 6 | VEP-strictest | 8.2 | 8.2 | 7.5 | 7.6 | 7.7 | 8.0 | 7.5 | 7.9 | 8.6 | 7.8 | 79.0 |
| 7 | Benchmark methodology | 8.5 | 8.5 | 8.0 | 8.3 | 7.9 | 8.4 | 8.0 | 8.3 | 8.7 | 8.2 | 82.8 |
| 8 | Practice-strict | 8.2 | 8.3 | 7.5 | 7.8 | 7.7 | 8.0 | 7.5 | 7.9 | 8.5 | 7.9 | 79.3 |
| 9 | Statistical Genetics | 8.6 | 8.6 | 7.8 | 8.1 | 7.7 | 8.4 | 7.9 | 8.3 | 8.8 | 8.2 | 82.4 |
| 10 | Structural Biology | 8.5 | 8.4 | 7.7 | 8.1 | 7.5 | 8.2 | 7.7 | 8.1 | 8.6 | 8.0 | 80.8 |

## 2. Item Means and Total

| Item | Mean |
|---|---:|
| A. 문제정의 / problem definition | 8.48 |
| B. 관련연구 / related research | 8.46 |
| C. 방법론 / methodological validity | 7.74 |
| D. 실험규모 / experimental scale and robustness | 8.02 |
| E. 결과해석 / result interpretation | 7.78 |
| F. 독창성 / originality | 8.27 |
| G. 실용가치 / practical value | 7.84 |
| H. 명확성 / clarity | 8.21 |
| I. 한계 / limitations | 8.68 |
| J. 완성도 / completeness | 8.06 |

Total = **81.54/100**. Minimum item mean = **7.74**.

## 3. Per-Item Rationale for Items Below 8.0

**C. Methodological validity (7.74).** The design is defensible: pre-specified Layer A/B/C logic, MCC under class imbalance, 8,580-cell grid, cluster/wild/phylogenetic/Bayesian robustness frames, Layer C checks, and clear separation of production EqualWeight from nested-LOPO sign-fitting. The remaining deductions are real: Layer A is a heterogeneous single-team curation target without inter-annotator reproducibility; PLM channels remain partly collinear/proxy-based; DMS threshold sensitivity is incomplete for all DMS pathogens; structural channels rely mostly on monomer predicted structures; and prospective/callability evidence is negative or bounded.

**E. Result interpretation (7.78).** The manuscript is mostly careful. It correctly demotes LOPO 0/11 and Friedman p=0.990 to null-consistent corroboration, treats H3N2 escape as self-consistency, anchors external practical evidence on HIV-1, and refuses deployment under 0/12 callability. Deductions remain because some headline language still leans on retrospective top-1 envelopes, the family-prior recipe can sound more operational than validated, and pathogen-dependence is still partly inseparable from curation/input-quality heterogeneity.

**G. Practical value (7.84).** HIV-1 search-space reduction is useful and well bounded, the code/provenance plan is strong, and the cold-start recipe is operationally described. However, the work remains a retrospective prioritization framework, not a prospective detector: external escape validation covers 3/11 pathogens, prospective backtests are weak for most pathogens, and the abstention rule refuses deployment on all current folds.

## 4. Gate Verdict

**PASS.** Total is 81.54/100, no item mean is below 6.0, and I found no unresolved Critical defect. This is a more comfortable narrow pass than v2, mainly because the post-compression version is easier to defend: the evidentiary limits are now more findable and less diluted by repeated audit prose.

## 5. Per-Item Delta from v2 80.9

| Item | v2 mean | v3 mean | Delta | One-line interpretation |
|---|---:|---:|---:|---|
| A | 8.47 | 8.48 | +0.01 | Essentially unchanged; the problem framing was already strong. |
| B | 8.46 | 8.46 | +0.00 | No material change; related research content is preserved. |
| C | 7.69 | 7.74 | +0.05 | Small lift from clearer audit/protocol separation, not from new methodology. |
| D | 7.93 | 8.02 | +0.09 | Ledger improves robustness navigability; evidence base itself is unchanged. |
| E | 7.68 | 7.78 | +0.10 | Trimmed repetition and tighter caveats reduce over-interpretation risk. |
| F | 8.27 | 8.27 | +0.00 | Originality unchanged by compression. |
| G | 7.82 | 7.84 | +0.02 | Slight usability gain; deployability limits remain. |
| H | 8.07 | 8.21 | +0.14 | Largest lift: fewer repeated robustness paragraphs and a clearer Ch4 ledger. |
| I | 8.59 | 8.68 | +0.09 | Limitations are more concentrated and harder to miss. |
| J | 7.96 | 8.06 | +0.10 | Shorter active build feels more defense-ready and less audit-cycle cluttered. |

## 6. Net Delta and Compression Verdict

Net delta from v2's 80.9 baseline: **+0.6 points** (80.9 -> 81.5). Compression **helped modestly**. It did not solve the underlying scientific constraints: small pathogen count, heterogeneous Layer A, retrospective dominance, limited external validation, and failed prospective callability all remain. But it improved the dissertation as a defense document by turning scattered robustness material into a concise audit ledger and reducing Ch5 restatement. The result is clearer, more complete in presentation, and slightly safer interpretively.

RESULT_BLIND_V3: total=81.5/100 min_item=7.7 verdict=PASS delta_from_v2=+0.6
