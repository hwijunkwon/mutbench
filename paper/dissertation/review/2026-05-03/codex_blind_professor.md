# Codex Blind Professor Evaluation

Scope read: active English manuscript files only: abstract, Chapter 1, Chapter 3, Chapter 4, Chapter 5. Existing review reports were not consulted.

## 1. 10x10 Score Matrix

Scores are 0--10. Row total is out of 100.

| # | Professor role | A | B | C | D | E | F | G | H | I | J | Row total |
|---:|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 1 | Chair, bioinformatics | 8 | 7 | 8 | 8 | 8 | 8 | 8 | 8 | 9 | 8 | 80 |
| 2 | Advisor, CS | 8 | 8 | 8 | 8 | 8 | 8 | 8 | 8 | 9 | 8 | 81 |
| 3 | Statistics/ML | 8 | 7 | 7 | 8 | 7 | 8 | 7 | 7 | 9 | 7 | 75 |
| 4 | Computational biology | 8 | 8 | 8 | 8 | 8 | 8 | 8 | 8 | 8 | 8 | 80 |
| 5 | Virology / public health | 8 | 7 | 8 | 8 | 8 | 8 | 8 | 8 | 9 | 8 | 80 |
| 6 | VEP/PLM expert | 8 | 7 | 7 | 8 | 7 | 8 | 7 | 7 | 8 | 7 | 74 |
| 7 | Benchmark methodology | 8 | 7 | 7 | 8 | 8 | 8 | 8 | 7 | 9 | 7 | 77 |
| 8 | Practice/field user | 8 | 7 | 7 | 8 | 7 | 8 | 7 | 7 | 8 | 7 | 74 |
| 9 | Statistical genetics | 8 | 7 | 7 | 8 | 7 | 8 | 8 | 8 | 9 | 8 | 78 |
| 10 | Structural biology | 8 | 7 | 8 | 8 | 7 | 8 | 7 | 7 | 8 | 7 | 75 |

## 2. Item Means and Total

| Item | Mean |
|---|---:|
| A. Problem definition clarity | 8.0 |
| B. Related work sufficiency | 7.2 |
| C. Methodological validity | 7.5 |
| D. Experimental scale/robustness | 8.0 |
| E. Accuracy of result interpretation | 7.5 |
| F. Originality of contribution | 8.0 |
| G. Practical value | 7.6 |
| H. Clarity of writing | 7.5 |
| I. Limitation awareness/honesty | 8.6 |
| J. Dissertation completeness | 7.5 |

Total = 77.4/100. Minimum item mean = 7.2.

## 3. Per-Item Rationales for Items Below 8.0

**B. Related work sufficiency, mean 7.2.** The manuscript positions MutBench clearly against ViroGym, EVEREST, ProteinGym, EVEscape, Nextstrain, and MutClust, and the distinction between region-level hotspot detection and per-variant fitness prediction is persuasive. The weakness is document-level: Chapter 1 still contains `\input{chapters_en/ch2_background}`, while the evaluation scope identifies `ch2_background.tex` as out of active evidence. On a fresh defense read, this creates uncertainty about whether the related-work foundation is actually present in the active manuscript or delegated to a non-build/orphan component. The PLM/VEP comparison is also partially weakened by the manuscript's own admission that the Tranception channel is an ESM-2 proxy highly collinear with ESM-2 LLR for 11/12 pathogens, so claims involving PLM family differentiation need more conservative phrasing.

**C. Methodological validity, mean 7.5.** The framework is serious: 20 scoring formulas, 39 detector variants, 11 pathogens, three ground-truth layers, MCC, enrichment, ANOVA, LOPO, Friedman, bootstrap, prospective backtests, null calibrations, and nested-LOPO ablations. The deductions come from ground-truth heterogeneity and effective-sample issues. Layer A is a pathogen-specific union of convergent evolution, immune escape, HVR membership, and region-derived labels; this is biologically pragmatic but not methodologically uniform. Several labels come from one to three anchor sources per pathogen with no duplicate curation or inter-annotator agreement. The ANOVA is also performed on 8,580 evaluation rows whose independence is limited by shared MSAs, labels, scoring vectors, and parameter variants; the manuscript acknowledges the effective unit is closer to 3,080 cells or 11 pathogen clusters. These are not fatal, but they cap confidence.

**E. Result interpretation accuracy, mean 7.5.** The strongest interpretations are appropriately bounded: "largest modeled component," "retrospective anchor," "LOPO 0/11 is null-consistent," "HIV-1 is the cleanest external validation," and "not a prospective deployment claim." However, the manuscript still has pressure toward over-interpretation. The top-1 vaccine-escape enrichments are winner's-curse prone; H3N2 and SARS-CoV-2 escape sets overlap Layer A substantially; the 4-feature core fails global null calibration and has 0/12 callable folds under the abstention rule; Wave 5 Layer A' is negative. The discussion eventually states these caveats, but the headline narrative remains more confident than the strictest statistical reading would allow.

**G. Practical value, mean 7.6.** The practical search-space-reduction story is meaningful, especially the HIV-1 Layer-A-disjoint enrichment and the explicit 20--80-position prioritization framing. Runtime and operational steps are described. The deduction is that the value is retrospective and bounded: vaccine/antibody escape validation covers only 3/11 pathogens, SARS-CoV-2 is exploratory after Bonferroni, H3N2 is partly self-consistency, frequency-only prospective tests are near chance for most pathogens, and the formal callability rule abstains on 0/12 folds. This is useful as a retrospective prioritization benchmark, not yet as a deployable surveillance detector.

**H. Writing clarity, mean 7.5.** The manuscript is unusually transparent, but it is also over-dense. Many paragraphs carry several caveats, cross-references, CSV provenance notes, and reinterpretations in one block. This improves honesty but hurts defense readability. There are also structural inconsistencies: Chapter 1 says the dissertation has four chapters but references a related-research section that is effectively an input; methods/results/discussion repeat many of the same caveats; and Stage 2/Stage 3/12-pathogen/Wave-panel terminology requires careful tracking. A committee can follow it, but it demands more effort than a polished dissertation should.

**J. Dissertation completeness, mean 7.5.** The active manuscript contains the core dissertation arc and a substantial concluding discussion, so it is not incomplete in substance. The deductions are for build and integration polish. The active Chapter 1 includes an external background input excluded by the task scope, several claims point to archived CSVs or scripts rather than tables fully auditable in the manuscript, some tables mix main 11-pathogen, 12-pathogen, and wave-only scopes, and the code/Zenodo statement still says a DOI will be minted at final submission. These are revision-needed completeness issues, not evidence of a missing scientific core.

## 4. Gate Verdict

FAIL as submitted under the stated numeric pass criterion. The total is 77.4/100, below the required 80/100, although no item mean is below 6 and I identify no single unresolved Critical flaw. This is a near-pass major-revision outcome: the manuscript has a defensible scientific contribution, but a fresh committee would require tightening of related-work/build integration, ground-truth provenance, statistical framing, and deployability language before granting a clean pass.

## 5. Fresh-vs-Iterative Meta-Comment

How does this fresh evaluation differ from what an iteratively-tuned committee might conclude? An iteratively-tuned committee that had watched prior revisions might reward the manuscript more heavily for its accumulated caveat discipline: it now says "largest modeled component," discounts LOPO, distinguishes HIV-1 from H3N2/SARS-CoV-2, discloses Layer A heterogeneity, and refuses deployment under a callability rule. A fresh committee, however, experiences those caveats as part of the manuscript's first-order evidentiary burden rather than as evidence of improvement from an earlier state. My score therefore reflects the active manuscript independently: strong and unusually honest, but still below a clean-pass threshold because the central benchmark depends on heterogeneous labels, small pathogen clusters, retrospective validation, and a document structure that still feels patched around prior objections.

RESULT_BLIND: total=77.4/100 min_item=7.2 verdict=FAIL
