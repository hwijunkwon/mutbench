# Codex Blind Professor Evaluation v2

Scope audited: active English manuscript only (`thesis_en.tex` inputs), including `chapters_en/ch2_background.tex` as the Related Research section inside Chapter 1. I did not use orphan chapters as evidence.

## 1. 10 x 10 Score Matrix

Scores are 0-10 for rubric items A-J.

| # | Role | A | B | C | D | E | F | G | H | I | J | Total |
|---:|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 1 | Chair (bioinformatics) | 8.6 | 8.7 | 8.0 | 8.1 | 8.0 | 8.6 | 8.1 | 8.3 | 8.6 | 8.2 | 83.2 |
| 2 | Advisor (CS) | 8.8 | 8.6 | 8.1 | 8.2 | 8.0 | 8.6 | 8.2 | 8.4 | 8.7 | 8.3 | 83.9 |
| 3 | Statistics/ML | 8.3 | 8.4 | 7.2 | 7.8 | 7.3 | 8.1 | 7.6 | 7.9 | 8.4 | 7.5 | 78.5 |
| 4 | Computational biology | 8.5 | 8.4 | 7.8 | 8.0 | 7.7 | 8.3 | 7.9 | 8.1 | 8.6 | 8.0 | 81.3 |
| 5 | Virology / public health | 8.6 | 8.5 | 7.7 | 7.9 | 7.8 | 8.1 | 8.0 | 8.1 | 8.8 | 8.0 | 81.5 |
| 6 | VEP/PLM expert | 8.2 | 8.2 | 7.4 | 7.5 | 7.6 | 8.0 | 7.5 | 7.8 | 8.5 | 7.7 | 78.4 |
| 7 | Benchmark methodology | 8.5 | 8.5 | 7.9 | 8.2 | 7.8 | 8.4 | 8.0 | 8.1 | 8.6 | 8.1 | 82.1 |
| 8 | Practice/field user | 8.2 | 8.3 | 7.5 | 7.7 | 7.6 | 8.0 | 7.4 | 7.7 | 8.4 | 7.8 | 78.6 |
| 9 | Statistical genetics | 8.6 | 8.6 | 7.7 | 8.0 | 7.6 | 8.4 | 7.8 | 8.2 | 8.7 | 8.1 | 81.7 |
| 10 | Structural biology | 8.4 | 8.4 | 7.6 | 7.9 | 7.4 | 8.2 | 7.7 | 8.1 | 8.6 | 7.9 | 80.2 |

## 2. Item Means and Total

| Item | Mean |
|---|---:|
| A. Problem definition clarity | 8.47 |
| B. Related research completeness | 8.46 |
| C. Methodological validity | 7.69 |
| D. Experimental scale/robustness | 7.93 |
| E. Accuracy of result interpretation | 7.68 |
| F. Originality of contribution | 8.27 |
| G. Practical value | 7.82 |
| H. Narrative clarity | 8.07 |
| I. Honest limitation recognition | 8.59 |
| J. Dissertation completeness | 7.96 |

Total = **80.94/100**. Minimum item mean = **7.68**.

## 3. Per-Item Rationale for Items Below 8.0

**C. Methodological validity (7.69).** The methodology is defensible but still carries notable inference limits. Layer A is a heterogeneous literature-curated union across convergent evolution, immune escape, HVR membership, and functional annotations; this is openly disclosed, but it means the primary MCC target is not a single biological construct. Some evaluation choices are strong, including MCC for class imbalance, cluster/wild/phylogenetic bootstrap triangulation, Layer C DMS checks, and ANCOVA sensitivity. Deductions remain for single-team curation without inter-annotator reproducibility, PLM proxy collinearity, incomplete DMS threshold sweeps for all DMS pathogens, MAFFT `--auto` not ablated, and retrospective dominant evidence.

**D. Experimental scale/robustness (7.93).** The 8,580-cell grid across 11 pathogens is large for a dissertation and the robustness section is unusually extensive. However, the effective independent pathogen count remains small for cross-pathogen generalization. Several external validations cover only 3/11 pathogens; DMS covers 6/11; prospective backtesting is weak for most pathogens; and the manuscript itself shows 0/12 callability under the abstention rule. The scale is strong as a benchmark snapshot, less strong as deployable generalization.

**E. Result interpretation accuracy (7.68).** The dissertation is mostly careful in distinguishing positive evidence from null-consistent corroboration. It correctly downgrades LOPO 0/11 and Friedman p=0.990 from independent proof to consistency checks, treats H3N2 escape as self-consistency, and anchors external value mainly on HIV-1. Deductions remain because several headline phrases still risk over-reading retrospective top-1 envelopes, category-vs-channel distinctions, and pathogen-dependence as biological rather than partly curation/input-quality dependent. The Korean abstract is also less caveated than the English abstract/discussion.

**G. Practical value (7.82).** The HIV-1 escape enrichment and search-space reduction are genuinely useful as retrospective prioritization. The practical workflow, code/data release plan, and dual-use mitigation are good. The deduction is that deployment remains explicitly unsupported: 0/12 callable under the current abstention rule, prospective evidence transfers poorly for eight pathogens, and family-level scoring priors are provisional rather than validated on held-out families.

**J. Dissertation completeness (7.96).** The active manuscript is coherent, builds cleanly, has a current Related Research section, and includes extensive limitations, provenance, and statistical diagnostics. Remaining deductions are mostly polish and consistency: the “9-item rubric”/A-J type mismatch is external to this report but the manuscript has analogous small inconsistencies; some results sections are dense with audit-cycle material; “Chapter 2” historical comments and retained labels are understandable but still slightly distracting; and the Korean abstract lags the final caveat calibration.

## 4. Gate Verdict

**PASS.** The total is 80.94/100, no item mean is below 6.0, and I found no unresolved Critical deficiency in the active manuscript. This is a narrow pass: the work clears the PhD defense threshold because it is honest, broad, and statistically self-critical, not because every biological or prospective claim is settled.

## 5. Comparison to v1 Blind Evaluation

Compared with v1 blind evaluation (reported total 77.4, with `ch2_background.tex` incorrectly treated as orphan), recognizing `ch2_background.tex` as active materially changes the Related Research axis and modestly helps adjacent axes. The active Related Research section reviews hotspot methods, density clustering, DMS, PLMs/VEP benchmarks, surveillance platforms, feature-importance work, algorithm selection, and the region-level benchmarking gap, including ViroGym/EVEREST/ProteinGym task-orthogonality. I therefore raise B from the likely sub-pass/acceptable range implied by v1 to 8.46. That also slightly improves A, F, H, and J because the problem framing, novelty boundary, organization, and literature positioning are better supported when the merged Related Research section is counted. It does not remove the core deductions in C/E/G: Layer A heterogeneity, small pathogen panel, retrospective validation, PLM proxy collinearity, and weak prospective/callability evidence remain. Net delta from v1 is **+3.5 points** (80.9 vs 77.4), enough to change the gate from fail to narrow pass.

RESULT_BLIND_V2: total=80.9/100 min_item=7.7 verdict=PASS delta_from_v1=+3.5
