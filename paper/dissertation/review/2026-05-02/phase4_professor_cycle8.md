# Phase 4 Professor Committee Simulation, Cycle 8

Scope: active English build inputs only (`front_en/abstract.tex`, `chapters_en/ch1_introduction.tex`, `chapters_en/ch3_methods.tex`, `chapters_en/ch4_results.tex`, `chapters_en/ch5_discussion.tex`). Orphan files were not used as evidence. Phase 3 CCB summary was supplied at execution time: **0 unresolved Critical findings, Phase 4 entry PASS**.

## Gate Verdict

**PASS for this audit cycle.**

- Total score: **84.2 / 100**
- Lowest item mean: **8.1** (B. related work, D. experimental scale, F. originality)
- Phase 3 unresolved Critical findings: **0**
- Gate result: total >= 80, no item mean < 6, and no unresolved Critical findings.

Cycle 8 is a small net improvement over Cycle 7 (**83.9 -> 84.2**). The removed formal falsification paragraph and reproduction-tolerance sentences do not materially weaken the defense because the manuscript still states operational negative criteria for adaptive selection and callability (`chapters_en/ch5_discussion.tex:338`, `chapters_en/ch5_discussion.tex:340`) and preserves the core reproducibility archive statement (`chapters_en/ch5_discussion.tex:375`-`390`). Compression improves the length/readability axis: Chapter 4 now points to consolidated Wave 4/5 artifact directories rather than enumerating long path lists (`chapters_en/ch4_results.tex:816`, `chapters_en/ch4_results.tex:820`), and the compressed pilot/future-work prose still preserves the key boundary that Layer A annotation remains the bottleneck (`chapters_en/ch5_discussion.tex:338`). The score lift is therefore mainly in H and J, not in the underlying scientific validity.

## Committee Matrix

Columns A-J: A problem definition, B related work, C methodology, D experimental scale, E result interpretation, F originality, G practical value, H clarity, I limitations, J completion.

| Professor | A | B | C | D | E | F | G | H | I | J | Mean |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 1. Chair, bioinformatics | 9 | 8 | 9 | 8 | 8 | 8 | 8 | 9 | 9 | 9 | 8.5 |
| 2. Advisor, computer science | 9 | 8 | 8 | 8 | 8 | 8 | 8 | 9 | 9 | 8 | 8.3 |
| 3. Statistics/ML | 8 | 8 | 9 | 8 | 9 | 8 | 8 | 9 | 9 | 8 | 8.4 |
| 4. Computational biology | 9 | 8 | 9 | 8 | 8 | 8 | 8 | 9 | 9 | 8 | 8.4 |
| 5. Virology/public health | 9 | 8 | 8 | 8 | 8 | 8 | 9 | 9 | 9 | 8 | 8.4 |
| 6. VEP/PLM expert | 8 | 9 | 8 | 8 | 8 | 9 | 8 | 8 | 9 | 8 | 8.3 |
| 7. Benchmark methodology | 9 | 8 | 9 | 9 | 8 | 8 | 8 | 9 | 10 | 9 | 8.7 |
| 8. Practice/field user | 9 | 8 | 8 | 8 | 8 | 8 | 8 | 9 | 9 | 8 | 8.3 |
| 9. Statistical genetics | 8 | 8 | 9 | 8 | 9 | 8 | 8 | 8 | 10 | 9 | 8.5 |
| 10. Structural biology | 9 | 8 | 8 | 8 | 8 | 8 | 9 | 9 | 9 | 9 | 8.5 |

## Item Means

| Item | Mean |
|---|---:|
| A. 문제 정의 | 8.7 |
| B. 관련 연구 | 8.1 |
| C. 방법론 | 8.5 |
| D. 실험 규모 | 8.1 |
| E. 결과 해석 | 8.2 |
| F. 기여 독창성 | 8.1 |
| G. 실용 가치 | 8.2 |
| H. 서술 명확성 | 8.8 |
| I. 한계 인식 | 9.1 |
| J. 완성도 | 8.4 |

Total score is the sum of item means: **84.2 / 100**.

## Per-Item Rationale

**A. 문제 정의, mean 8.7.** The problem is clearly bounded to RNA-virus, surface-glycoprotein, single-position hotspot detection (`front_en/abstract.tex:2`). The panel-scope summary prevents denominator confusion by separating the 11-pathogen main panel, 12-pathogen Stage 3 panel, and Wave sensitivity panels (`chapters_en/ch1_introduction.tex:89`). Deduction is minor: the reader still must track several nested evaluation regimes.

**B. 관련 연구, mean 8.1.** Related-work positioning is adequate and correctly distinguishes MutBench from per-variant fitness or escape-prediction benchmarks (`chapters_en/ch5_discussion.tex:76`, `chapters_en/ch5_discussion.tex:151`-`154`). Deduction remains because the PLM/VEP comparison is not a true model-family benchmark; the manuscript itself notes Tranception/ESM-2 proxy collinearity (`front_en/abstract.tex:13`; `chapters_en/ch5_discussion.tex:199`).

**C. 방법론, mean 8.5.** Methods are strong: ground-truth thresholds and the ANOVA grid are frozen (`chapters_en/ch3_methods.tex:209`), headline EqualWeight is separated from label-aware nested-LOPO ablation (`chapters_en/ch3_methods.tex:615`-`620`), and MCC/Bonferroni choices are explicit (`chapters_en/ch3_methods.tex:805`, `chapters_en/ch3_methods.tex:825`). Deduction remains for heterogeneous Layer A construction (`chapters_en/ch3_methods.tex:207`).

**D. 실험 규모, mean 8.1.** The 8,580-evaluation grid is dissertation-scale (`front_en/abstract.tex:2`), and the sensitivity programme is substantial. The limiting scale is cross-pathogen inference: the 11-pathogen panel remains in the small-cluster regime, below the 20-30 level for stable random-effects estimation (`chapters_en/ch5_discussion.tex:209`). External escape validation is available for only 3/11 pathogens (`chapters_en/ch4_results.tex:949`).

**E. 결과 해석, mean 8.2.** Interpretation is careful and slightly cleaner after compression. The manuscript states that LOPO 0/11 is null-consistent rather than standalone proof (`front_en/abstract.tex:10`; `chapters_en/ch4_results.tex:600`-`604`), separates HIV-1 from H3N2/SARS-CoV-2 as the external anchor (`chapters_en/ch4_results.tex:943`-`952`), and treats Layer A' as non-equivalent rather than validating Layer A (`chapters_en/ch4_results.tex:820`). Deduction remains because pathogen-specific performance still mixes biology, curation protocol, and auxiliary input quality (`chapters_en/ch4_results.tex:894`-`895`).

**F. 기여 독창성, mean 8.1.** The contribution is original as a region-level, multi-information-source hotspot benchmark (`chapters_en/ch1_introduction.tex:147`-`158`). Deduction is that the algorithmic output is a bounded retrospective heuristic, not a prospectively callable detector (`chapters_en/ch4_results.tex:696`; `chapters_en/ch4_results.tex:808`).

**G. 실용 가치, mean 8.2.** Practical value is credible but bounded. HIV-1 provides the cleanest retrospective anchor with 82% Layer-A-disjoint escape positions (`front_en/abstract.tex:11`; `chapters_en/ch5_discussion.tex:125`), and the workflow gives actionable screening steps (`chapters_en/ch5_discussion.tex:160`). The deployment deduction remains: the pre-registered callability rule refuses all 12 folds (`chapters_en/ch4_results.tex:808`), and recommended use is retrospective prioritization only (`chapters_en/ch5_discussion.tex:311`-`312`).

**H. 서술 명확성, mean 8.8.** Cycle 8 improves readability without removing load-bearing evidence. The abstract carries the negative and abstention boundaries (`front_en/abstract.tex:11`), the panel-scope paragraph is early (`chapters_en/ch1_introduction.tex:89`), and the defense map gives committee-facing wording (`chapters_en/ch5_discussion.tex:353`-`369`). Compression of artifact paths and future-work detail reduces audit-log density. Deduction is residual: the abstract remains dense because it carries many necessary caveats.

**I. 한계 인식, mean 9.1.** Limitations remain unusually explicit: Layer A curation reproducibility is disclosed (`chapters_en/ch5_discussion.tex:48`-`49`), small-cluster inference is bounded (`chapters_en/ch5_discussion.tex:209`), PLM data overlap is acknowledged (`chapters_en/ch5_discussion.tex:194`-`201`), and prospective use is withheld (`chapters_en/ch5_discussion.tex:311`-`312`). Cycle 8 loses only a tenth relative to Cycle 7 because formal falsification prose was removed; functional decision rules remain in future work (`chapters_en/ch5_discussion.tex:338`).

**J. 완성도, mean 8.4.** The dissertation is defense-ready under this audit. The critical gate is clear, adverse Wave results are integrated, and CSV-to-table provenance remains listed (`chapters_en/ch5_discussion.tex:378`-`390`). Deduction remains for final-production polish: the Zenodo DOI is still future insertion (`chapters_en/ch5_discussion.tex:375`-`376`), and independent recuration/reproduction are not yet complete.

## Items Below 8

No item mean is below 8. Therefore no mandatory mean-<8 targeted fixes are triggered.

Smallest remaining high-yield fixes: independently recurate a Layer A subset with agreement statistics; add one more clean external or time-forward validation anchor; insert the final Zenodo DOI.

## Sub-6 Scores

No professor assigned any item score below 6, so no sub-6 one-sentence rationales are required.

## Diagnostic Criterion

Skill-defined diagnostic criterion, reported but not used as the gate:

- Mean >= 7: **PASS** (overall mean 8.42)
- Individual minimum >= 5: **PASS** (minimum individual score 8)

## Overall Assessment

Cycle 8 passes the simulated committee gate. The updated manuscript is marginally stronger than Cycle 7 because compression improves readability and completion without weakening the load-bearing evidence. The main residual weaknesses are unchanged and scientifically appropriate for post-defense work: Layer A reproducibility, external/prospective validation breadth, and prospective callability.
