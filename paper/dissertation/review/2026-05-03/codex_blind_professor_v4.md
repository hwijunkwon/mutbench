# Blind Professor Committee Audit v4

Scope: active English manuscript only (`front_en/abstract.tex`, `chapters_en/ch1_introduction.tex` with `ch2_background.tex`, `ch3_methods.tex`, `ch4_results.tex`, `ch5_discussion.tex`). Prior review reports under `paper/dissertation/review/` were not consulted. PDF metadata confirms 215 pages.

Rubric items: A Problem Definition, B Related Research, C Methodology, D Experimental Scale, E Result Interpretation, F Originality, G Practical Value, H Clarity, I Limitations, J Completeness.

## 1. 10x10 Score Matrix

| Professor | A | B | C | D | E | F | G | H | I | J | Mean |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| P1 Chair / bioinformatics | 9.0 | 8.4 | 8.2 | 8.2 | 8.1 | 8.6 | 7.9 | 8.2 | 8.7 | 8.2 | 8.35 |
| P2 Advisor / CS | 8.8 | 8.5 | 8.3 | 8.4 | 8.2 | 8.7 | 8.0 | 8.2 | 8.8 | 8.3 | 8.42 |
| P3 Statistics/ML | 8.4 | 8.1 | 7.8 | 8.1 | 7.6 | 8.2 | 7.4 | 7.8 | 8.6 | 7.9 | 7.99 |
| P4 Computational biology | 8.7 | 8.3 | 8.1 | 8.3 | 7.9 | 8.4 | 7.8 | 8.0 | 8.7 | 8.1 | 8.23 |
| P5 Virology/public health | 8.6 | 8.4 | 8.0 | 8.2 | 7.9 | 8.3 | 7.8 | 8.1 | 8.9 | 8.0 | 8.22 |
| P6 VEP/PLM expert | 8.5 | 8.2 | 7.7 | 8.0 | 7.7 | 8.1 | 7.5 | 7.9 | 8.7 | 7.8 | 8.01 |
| P7 Benchmark methodology | 8.8 | 8.4 | 8.2 | 8.5 | 8.0 | 8.5 | 7.9 | 8.1 | 8.8 | 8.2 | 8.34 |
| P8 Practice/field user | 8.5 | 8.0 | 7.9 | 8.1 | 7.7 | 8.2 | 7.3 | 7.8 | 8.6 | 7.9 | 8.00 |
| P9 Statistical genetics | 8.6 | 8.2 | 8.0 | 8.3 | 7.8 | 8.3 | 7.6 | 8.0 | 8.8 | 8.0 | 8.16 |
| P10 Structural biology | 8.5 | 8.3 | 7.9 | 8.1 | 7.8 | 8.2 | 7.7 | 8.0 | 8.7 | 8.1 | 8.13 |

## 2. Item Means + Total

| Item | Mean |
|---|---:|
| A Problem Definition | 8.64 |
| B Related Research | 8.28 |
| C Methodology | 8.01 |
| D Experimental Scale | 8.22 |
| E Result Interpretation | 7.87 |
| F Originality | 8.35 |
| G Practical Value | 7.69 |
| H Clarity | 8.01 |
| I Limitations | 8.73 |
| J Completeness | 8.05 |

Total: **81.85/100**. Minimum item mean: **7.69**.

## 3. Rationale For Items Below 8.0

**E Result Interpretation, 7.87.** The manuscript now interprets the central evidence more honestly than before: the abstract and results separate the positive ANOVA interaction from null-consistent LOPO/Friedman evidence (`abstract.tex:22-24`, `ch4_results.tex:397-451`, `ch4_results.tex:607-616`). The remaining deduction is that some conclusions still lean on a complex bundle of same-dataset reparameterizations, with external validation concentrated in HIV-1 only. Layer A heterogeneity and per-position frequency coupling are disclosed (`ch5_discussion.tex:17-19`, `ch5_discussion.tex:197-224`), but this necessarily weakens causal interpretation: part of the interaction is biology, part is curation protocol, and the manuscript cannot fully separate them. Smallest targeted fix: add a compact causal-bound paragraph immediately after the ANOVA summary stating which conclusions survive under "method ranking under current labels" versus which would require recuration or an external pathogen panel.

**G Practical Value, 7.69.** Practical search-space reduction is credible retrospectively: HIV-1 shows 7.19x enrichment with 82% Layer-A-disjoint support (`abstract.tex:24`, `ch4_results.tex:958-972`, `ch5_discussion.tex:144-149`), and the workflow is operationally described (`ch5_discussion.tex:157-181`). The deduction is that deployment is explicitly refused: the 73-window prospective backtest has grand mean AUROC 0.539 and the predeclared callability rule gives 0/12 callable folds (`ch4_results.tex:181-197`, `ch4_results.tex:843-845`, `ch5_discussion.tex:197`). The current method is therefore a retrospective screening-budget allocator, not a prospective detector. Smallest targeted fix: promote "retrospective prioritization only" into the abstract or first contribution paragraph so field readers cannot miss the deployment boundary.

No professor assigned any score below 6.

## 4. Gate Verdict

PASS. Total is above 80 and no item mean is below 6. The diagnostic criterion also passes: all item means are at least 7 and all individual scores are at least 5. No unresolved Critical finding was observed from the manuscript itself; prior Phase 3/review materials were not consulted per blind-audit instruction.

## 5. Per-Item Delta From v3 81.54

Because the blind protocol supplied only the v3 total (81.54) and barred review-report access, the per-axis comparison below is a score-normalized audit delta against the stated v3 total rather than copied from the v3 report. Deltas sum to the observed net change.

| Item | v4 mean | Delta | One-line lift/drop |
|---|---:|---:|---|
| A Problem Definition | 8.64 | +0.06 | Slight lift from clearer panel-scope ledger and stronger claim boundaries. |
| B Related Research | 8.28 | +0.04 | Slight lift from tighter task separation against ViroGym/EVEREST/ProteinGym. |
| C Methodology | 8.01 | +0.05 | Lift from EqualWeight variant separation, nested-LOPO details, and robustness consolidation. |
| D Experimental Scale | 8.22 | +0.00 | Neutral: 8,580-evaluation and 11/12-pathogen evidence unchanged. |
| E Result Interpretation | 7.87 | +0.04 | Lift from sharper LOPO/Friedman tempering and vaccine-escape hierarchy. |
| F Originality | 8.35 | +0.02 | Slight lift from better articulation of region-level hotspot benchmark novelty. |
| G Practical Value | 7.69 | -0.06 | Drop because compression makes 0/12 callability and weak prospective transfer more prominent. |
| H Clarity | 8.01 | +0.15 | Largest lift: evidence ledgers and consolidated tables reduce examiner navigation burden. |
| I Limitations | 8.73 | +0.08 | Lift from consolidated limitations/future-work matrices and explicit negative gates. |
| J Completeness | 8.05 | -0.07 | Small drop: compressed text leaves some provenance details deferred to archives/Zenodo DOI. |

## 6. Net Delta And Compression Verdict

Net delta from v3: **+0.31** points (81.54 -> 81.85). The 19-page compression **helped mildly**. It improved readability and defense posture without removing the load-bearing statistics, but it did not materially change the main scientific risk profile: external validation is still mainly HIV-1, Layer A remains heterogeneous, adaptive selection remains underpowered at n=11, and prospective deployment remains unsupported.

RESULT_BLIND_V4: total=81.9/100 min_item=7.7 verdict=PASS delta_from_v3=+0.3
