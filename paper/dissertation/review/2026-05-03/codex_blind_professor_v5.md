# Phase 4 Blind Professor v5 Report

Fresh active-build review only. Scope read: `front_en/abstract.tex`, `chapters_en/ch1_introduction.tex` with `ch2_background.tex` input, `ch3_methods.tex`, `ch4_results.tex`, and `ch5_discussion.tex`.

## 1. 10x10 Score Matrix

| Professor | A Problem | B Related | C Method | D Robustness | E Interpretation | F Originality | G Practical | H Clarity | I Limits | J Completion |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| P1 Chair | 8.6 | 8.4 | 8.2 | 8.3 | 8.0 | 8.5 | 8.0 | 8.3 | 8.9 | 8.3 |
| P2 Advisor | 8.5 | 8.3 | 8.2 | 8.4 | 8.0 | 8.5 | 8.0 | 8.2 | 8.8 | 8.2 |
| P3 Statistics/ML | 8.3 | 8.1 | 7.8 | 8.0 | 7.5 | 8.2 | 7.7 | 7.9 | 8.7 | 7.8 |
| P4 Comp Bio | 8.5 | 8.4 | 8.1 | 8.4 | 7.9 | 8.4 | 7.9 | 8.2 | 8.8 | 8.2 |
| P5 Virology | 8.6 | 8.5 | 8.1 | 8.3 | 7.9 | 8.5 | 8.0 | 8.3 | 8.9 | 8.3 |
| P6 VEP/PLM | 8.4 | 7.9 | 7.9 | 8.0 | 7.6 | 8.1 | 7.6 | 7.9 | 8.7 | 7.9 |
| P7 Benchmark | 8.4 | 8.3 | 8.0 | 8.3 | 7.8 | 8.4 | 7.8 | 8.2 | 8.8 | 8.1 |
| P8 Field User | 8.3 | 8.2 | 8.0 | 8.2 | 7.8 | 8.3 | 7.5 | 7.9 | 8.7 | 8.0 |
| P9 Stat Genetics | 8.6 | 8.4 | 8.2 | 8.4 | 8.0 | 8.4 | 8.0 | 8.4 | 8.9 | 8.3 |
| P10 Structural | 8.7 | 8.5 | 8.5 | 8.7 | 8.5 | 8.7 | 8.5 | 8.7 | 8.8 | 8.9 |

## 2. Item Means + Total

| Item | Mean |
|---|---:|
| A. Problem definition clarity | 8.5 |
| B. Related work completeness | 8.3 |
| C. Methodological validity | 8.1 |
| D. Experimental scale/robustness | 8.3 |
| E. Accuracy of result interpretation | 7.9 |
| F. Originality of contribution | 8.4 |
| G. Practical value | 7.9 |
| H. Expository clarity | 8.2 |
| I. Limitation awareness/honesty | 8.8 |
| J. Dissertation completeness | 8.2 |

Total: **82.6/100**. Minimum item: **7.9**.

## 3. Rationales for Items Below 8.0

**E. Result interpretation accuracy, 7.9.** The audit fixes help substantially: D614G is now treated as a retained functional/stability substitution rather than incorrectly excluded, the omega interval is aligned to `[0.201, 0.346]`, and the discussion correctly distinguishes Layer A tag counts from feature-matrix counts. The remaining problem is not conceptual but active-build polish: Chapter 4 prose reports functional regions as 417 AA, but Table `tab:multi_gt` still says `Functional regions (439)` and `Positions 439` (`ch4_results.tex:49-64`). Chapter 4 also reverses the HIV-1 count reconciliation in two captions, stating operational `n_A = 26` versus literature-curated 23, while the methods state feature-matrix `23` and tag-table `26` (`ch4_results.tex:261`; `ch3_methods.tex:299,316`). These are local but examiner-visible numerical inconsistencies.

**G. Practical value, 7.9.** The practical story is honest and useful, especially the HIV-1 escape enrichment anchor and search-space reduction framing. However, the manuscript also correctly says prospective deployment is not supported: the audit ledger reports `0/12` callable folds (`ch4_results.tex:747-755`), the limitations section says forward-time transfer is weak (`ch5_discussion.tex:197`), and recommended use is retrospective prioritization only (`ch5_discussion.tex:257-258`). That boundary is scientifically appropriate but caps the practical-value score below 8.

## 4. Gate Verdict

**PASS.** Total is above 80, no item mean is below 6, and I do not find an unresolved Critical in the active build. The remaining issues are Major-to-Minor active-build consistency defects, not defense-blocking contradictions.

## 5. Per-Item Delta from v4 81.85

| Item | v5 mean | Delta vs v4 baseline |
|---|---:|---:|
| A | 8.5 | +0.0 |
| B | 8.3 | +0.0 |
| C | 8.1 | +0.1 |
| D | 8.3 | +0.1 |
| E | 7.9 | +0.3 |
| F | 8.4 | +0.0 |
| G | 7.9 | +0.0 |
| H | 8.2 | +0.1 |
| I | 8.8 | +0.1 |
| J | 8.2 | +0.1 |

The per-item deltas are calibrated against the stated v4 total rather than a re-read v4 report. Most gain is in E/J: the corrected D614G treatment, omega CI, Stage 1 region count in prose, gap-aware wording, and provenance caveats make the manuscript more defensible.

## 6. Net Delta and Verdict on Fixes

Net delta: **+0.8** points from v4 81.85 to v5 82.6. Verdict: **helped**. The fixes improve factual alignment and reduce the chance of a single examiner finding a fatal inconsistency. The gain is capped because Chapter 4 still contains residual numerical/caption mismatches, and because the practical claim remains deliberately bounded by negative callability and prospective-transfer results.

RESULT_BLIND_V5: total=82.6/100 min_item=7.9 verdict=PASS delta_from_v4=+0.8
