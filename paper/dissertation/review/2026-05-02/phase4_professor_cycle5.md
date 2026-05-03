# Phase 4 Professor Committee Simulation, Cycle 5

Scope: active English build inputs only (`front_en/abstract.tex`, `chapters_en/ch1_introduction.tex`, `chapters_en/ch3_methods.tex`, `chapters_en/ch4_results.tex`, `chapters_en/ch5_discussion.tex`). Orphan files were not used as evidence. Phase 3 CCB is consumed as supplied: **0 unresolved Critical findings, Phase 4 entry PASS**. This score reflects the Cycle 5 manuscript state after the counterfactual-null, Layer A curation-limit, falsification, scope, and reproduction-tolerance edits.

## Gate Verdict

**PASS for this audit cycle.**

- Total score: **82.9 / 100**
- Lowest item mean: **7.8** (H. 서술 명확성)
- Phase 3 unresolved Critical findings: **0**
- Gate result: total >= 80, no item mean < 6, and no unresolved Critical findings.

The Cycle 5 updates lift the highest-risk Cycle 4 concern. Chapter 4 now directly tests the counterfactual-null question for the headline interaction: pathogen-identity and scoring-identity shuffles collapse the scoring-by-pathogen interaction to near zero, while the observed reproduced value remains more than 60x above the null upper bound (`chapters_en/ch4_results.tex:387`). Chapter 5 also adds explicit curation-reproducibility limitations, including no duplicate curation/agreement estimate, no source-selection sensitivity, and region-derived position-certainty caveats (`chapters_en/ch5_discussion.tex:278`-`282`), plus falsification criteria and reproduction tolerances (`chapters_en/ch5_discussion.tex:319`-`322`). These edits mainly raise C and I; H remains the residual weakness because the defense logic is now highly complete but dense.

## Committee Matrix

Columns A-J: A problem definition, B related work, C methodology, D experimental scale, E result interpretation, F originality, G practical value, H clarity, I limitations, J completion.

| Professor | A | B | C | D | E | F | G | H | I | J | Mean |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 1. Chair, bioinformatics | 9 | 8 | 9 | 8 | 8 | 8 | 8 | 8 | 9 | 9 | 8.4 |
| 2. Advisor, computer science | 9 | 8 | 8 | 8 | 8 | 8 | 8 | 8 | 9 | 8 | 8.2 |
| 3. Statistics/ML | 8 | 8 | 9 | 8 | 8 | 8 | 8 | 8 | 9 | 8 | 8.2 |
| 4. Computational biology | 9 | 8 | 9 | 8 | 8 | 8 | 8 | 8 | 9 | 8 | 8.3 |
| 5. Virology/public health | 9 | 8 | 8 | 8 | 8 | 8 | 8 | 8 | 9 | 8 | 8.2 |
| 6. VEP/PLM expert | 8 | 9 | 8 | 8 | 8 | 9 | 8 | 7 | 9 | 8 | 8.2 |
| 7. Benchmark methodology | 9 | 8 | 9 | 9 | 8 | 8 | 8 | 8 | 10 | 9 | 8.6 |
| 8. Practice/field user | 9 | 8 | 8 | 8 | 8 | 8 | 8 | 7 | 9 | 8 | 8.1 |
| 9. Statistical genetics | 8 | 8 | 9 | 8 | 9 | 8 | 8 | 8 | 10 | 8 | 8.4 |
| 10. Structural biology | 9 | 8 | 8 | 8 | 8 | 8 | 8 | 8 | 9 | 9 | 8.3 |

## Item Means

| Item | Mean |
|---|---:|
| A. 문제 정의 | 8.7 |
| B. 관련 연구 | 8.1 |
| C. 방법론 | 8.5 |
| D. 실험 규모 | 8.1 |
| E. 결과 해석 | 8.1 |
| F. 기여 독창성 | 8.1 |
| G. 실용 가치 | 8.0 |
| H. 서술 명확성 | 7.8 |
| I. 한계 인식 | 9.2 |
| J. 완성도 | 8.3 |

Total score is the sum of item means: **82.9 / 100**.

## Per-Item Rationale

**A. 문제 정의, mean 8.7.** The problem is sharply framed as a region-level, single-position hotspot-detection benchmark for RNA-virus surface glycoproteins, point substitutions only (`front_en/abstract.tex:2`; `chapters_en/ch1_introduction.tex:82`-`91`). Remaining deduction: the reader must keep the main 11-pathogen panel and 12-pathogen feature-ablation extension separate (`chapters_en/ch1_introduction.tex:86`). No targeted fix required for the gate; a one-line panel-scope table would reduce friction.

**B. 관련 연구, mean 8.1.** Related work positioning is adequate because MutBench is distinguished from per-variant fitness-regression benchmarks and framed as region-level detection (`front_en/abstract.tex:4`; `chapters_en/ch1_introduction.tex:145`-`147`). Residual deduction: PLM/VEP channels are still necessarily proxy-based and collinear at headline granularity (`front_en/abstract.tex:13`). Smallest fix: add a compact related-work comparison row separating region-level detection, per-position scoring, and per-variant fitness prediction.

**C. 방법론, mean 8.5.** Cycle 4's highest-risk methodological deduction is lifted. The counterfactual-null paragraph now directly shows the headline interaction is not a random pathogen-label or scoring-label artifact (`chapters_en/ch4_results.tex:387`), complementing preregistered thresholds and the frozen ANOVA grid (`chapters_en/ch3_methods.tex:209`). Residual deduction: Layer A itself remains a heterogeneous literature-curated construct, not a uniformly assayed label system (`chapters_en/ch3_methods.tex:207`). Smallest fix: add a supplementary curation protocol template for source extraction and adjudication.

**D. 실험 규모, mean 8.1.** The main benchmark is broad for a dissertation: 8,580 evaluations across 20 scoring formulas, 39 detector variants, and 11 pathogens (`front_en/abstract.tex:2`; `chapters_en/ch1_introduction.tex:86`). The residual deduction is cross-pathogen inference: 11 pathogen clusters remain below the 20-30 level preferred for stable random-effects estimation (`chapters_en/ch5_discussion.tex:182`). Smallest fix: expanded external panel with matched labels, not more detector variants.

**E. 결과 해석, mean 8.1.** Interpretation is now well bounded: the manuscript calls the interaction the largest modeled component, discloses the within-cell residual, and treats LOPO/Friedman as consistency checks rather than independent replications (`chapters_en/ch4_results.tex:383`-`387`). The counterfactual null further lifts the Cycle 4 deduction. Residual deduction: the interaction still mixes biology, curation protocol, and input-quality variation (`chapters_en/ch5_discussion.tex:191`-`196`). Smallest fix: consistently use "pathogen-specific benchmark behavior" when causal isolation is not shown.

**F. 기여 독창성, mean 8.1.** The contribution remains original as a region-level, multi-information-source RNA-virus benchmark with a large detector grid and layered labels (`chapters_en/ch1_introduction.tex:145`-`149`). Deduction is modest: the practical algorithmic output is a bounded heuristic rather than a prospectively callable predictor (`chapters_en/ch1_introduction.tex:156`; `chapters_en/ch5_discussion.tex:284`-`285`). Smallest fix: title Contribution 3 explicitly as retrospective search-space reduction.

**G. 실용 가치, mean 8.0.** HIV-1 provides the strongest practical anchor, with Layer-A-disjoint escape enrichment carried in the abstract (`front_en/abstract.tex:11`) and caveated against H3N2/SARS-CoV-2 overlap (`chapters_en/ch4_results.tex:951`-`952`). Deduction remains because deployability is refused by the current abstention rule: 0/12 callable folds (`chapters_en/ch5_discussion.tex:313`). Smallest fix: provide a recommended reporting checklist for users: target scope, abstention status, label provenance, and whether validation is retrospective or prospective.

**H. 서술 명확성, mean 7.8.** Strongest reason: the dissertation is now candid but overloaded. The abstract and Chapter 5 carry many necessary caveats in dense paragraphs, including negative callability, Layer A' non-equivalence, future panel rules, falsification criteria, and reproduction tolerances (`front_en/abstract.tex:10`-`13`; `chapters_en/ch5_discussion.tex:311`-`322`). Smallest targeted fix: add a one-page "claim / evidence / boundary / allowed use" table at the end of Chapter 5 and shorten the surrounding prose.

**I. 한계 인식, mean 9.2.** Cycle 5 substantially lifts this item. The manuscript now explicitly states Layer A curation reproducibility limits, scope exclusions, falsification criteria, prospective validation gaps, small-cluster inference limits, and reproduction tolerances (`chapters_en/ch5_discussion.tex:182`-`184`, `218`-`220`, `317`-`322`). Remaining deduction is not disclosure but execution: the formal recuration/agreement study and source-selection sensitivity are still future work. Smallest fix: independently recurate a 10-20% label subset and report agreement plus coordinate-error rate.

**J. 완성도, mean 8.3.** The audit package is mature: Phase 3 reports 0 unresolved Critical findings (`review/2026-05-02/phase3_ccb.md:76`-`80`), Cycle 5 adds the missing counterfactual-null result, and Chapter 5 binds release and reproduction artifacts to archived CSVs (`chapters_en/ch5_discussion.tex:322`-`334`). Deduction remains for final-production polish: dense prose and minor reproducibility tolerances remain disclosed rather than fully eliminated.

## Sub-6 Scores

No professor assigned any item score below 6, so no sub-6 one-sentence rationales are required.

## Diagnostic Criterion

Skill-defined diagnostic criterion, reported but not used as the gate:

- Mean >= 7: **PASS** (overall mean 8.29)
- Individual minimum >= 5: **PASS** (minimum individual score 7)

## Overall Assessment

The committee would pass the updated dissertation. The most important Cycle 4 methodological weakness has been directly addressed by a counterfactual null, and the added limitation/falsification/reproduction language makes the dissertation defensible under adversarial questioning. The remaining weakness is presentation clarity, not a gate-level validity problem: the work would benefit from a compact final claim-boundary table so committee readers can see exactly what is proven, what is retrospective, and what is deferred.
