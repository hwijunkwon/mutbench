# Audit v2 Job 1: abstract + ch1 lines 1-100

Scope: `paper/dissertation/front_en/abstract.tex` lines 1-34 and `paper/dissertation/chapters_en/ch1_introduction.tex` lines 1-100. Paragraph/block-level audit.

## Per-Paragraph Table

| ID | Lines | Numerical claims | Citations | Cross-refs | Consistency / fix check | Severity |
|---|---:|---|---|---|---|---|
| A1 | abstract 2 | VERIFIED: 11 pathogens, 10 info types, 20 formulas, 14 families, 39 variants, 8,580 evals from `results/mutbench/stage3_full_results.csv` (8580 rows; 11 pathogens; 20 scoring; 14 families; 39 detectors). | none | none | Uses required "single-position scoring (gap-aware)"; no old "point substitutions only". | Verified |
| A2 | abstract 4-8 | VERIFIED: 8,580 as above; 3 layers/2-stage+Stage 3 consistent with Ch3/Ch4. External benchmark counts are literature claims: ViroGym 79 DMS/7 phenotypes web-checked; EVEREST 45 DMS/31 clades/40 viruses web-checked; ProteinGym v1.3 217 DMS and 90+ baselines web-checked. | none in abstract paragraph | none | Internally consistent with Ch3 design. | Verified |
| A3 | abstract 10-27 table | VERIFIED: 0.778 from `paper/dissertation/chapters_en/ch3_methods.tex`/Ch4 Stage 1; 0.296, Friedman 7.6879666, p=0.9895445, LOPO 0/11, gap 0.265424 from `results/mutbench/stage3_statistics.csv`; 6-category 0.103 consistent with Ch4 diagnostics; residual approx 0.39 derived from modeled omega sum in `stage3_statistics.csv`; HIV 7.19x from `results/mutbench/vaccine_escape_stage3.csv` and Ch4 table; 780 = 20x39. PARTLY UNVERIFIED: HIV novel-only 7.16-8.24x/37/p=5e-12/3.9e-9 is only exposed in `paper/dissertation/chapters_en/ch4_results.tex` footnote, not a CSV found under `results/mutbench/`. | none | `tab:abstract_evidence_ledger` defined locally. | Omega CI uses new [0.201,0.346], not old [0.195,0.333]. | Minor |
| A4 | abstract 29 | VERIFIED: 12-pathogen panel and delta +0.011, CI [-0.018,+0.042] from `results/mutbench/feature_analysis/feature_ablation_nested_lopo_summary.csv`; 87/1023 from `results/mutbench/codex_wave1/p3_full_lattice_1023.csv`; 0/12 abstention from `results/mutbench/codex_wave2/p5_callable_decisions.csv`; Layer A' mean -0.055 and precision@20 0.005 from `results/mutbench/codex_layerA_prime/lopo_summary.csv`; H3N2 4.012x p=0.0023 from `results/mutbench/escape_validation_adapt.csv`; H3N2 9.36x/SARS-CoV-2 7.63x from `vaccine_escape_stage3.csv`/Ch4. | none | none | Consistent with Ch4/Ch5 framing as bounded sensitivity, not panel extension. | Verified |
| A5 | abstract 31 | VERIFIED: 20 scoring types, 6 categories, 9 best scoring types and H3N2 fubar_bf MCC 0.534058 from `results/mutbench/stage3_full_results.csv`; SARS-CoV-2 best Tranception, RSV best ESM-2, Norovirus best homoplasy also verified there. HIV novel-only range caveat same as A3. | none | `ch:mutbench` resolves to Ch3 Materials/Method. | Consistent with Tranception/ESM collinearity note in Ch3. | Minor |
| C1 | ch1 8-12 | UNVERIFIED locally: >700M confirmed cases is not in CSVs; web check supports >700M via WHO dashboard/data pages, but `harvey2021tracking` is a 2021 variant paper and cannot support the later cumulative case count. Citations OK for variant tracking/phenotypic changes; add WHO/Our World in Data if strict. | `harvey2021tracking`, `carabelli2023convergent`: OK for variants/phenotypes, not current case count. | `tab:glossary` resolves locally. | No regression terms. | Minor |
| C2 | ch1 14-31 table | Numbers: none beyond term list. | none | `tab:glossary` defined locally. | Definitions are internally consistent. | Verified |
| C3 | ch1 33 | External benchmark numerics: ViroGym 13 viruses/79 DMS/7 phenotypes, EVEREST 45 DMS/31 clades/40 WHO viruses, ProteinGym 217 DMS/90+ baselines. Web-verified against ViroGym/EVEREST/ProteinGym pages; not expected in MutBench CSVs. | `virogym2026`, `gurev2026everest_v3`, `notin2023proteingym`, `notin2025proteingym_v13`, `thadani2023evescape`, `livesey2020using`: OK for per-variant/fitness/escape benchmark contrast. | none | Claim "none has performed region-level hotspot-detection comparison..." is plausible but broad; no contrary evidence found. | Verified |
| C4 | ch1 35-36 | No benchmark result numbers. | `bailey2018comprehensive`, `han2025mosd`, `youn2025mutclust`: OK for cancer benchmark, MOSD, MutClust context. | none | Consistent with dissertation motivation. | Verified |
| C5 | ch1 38-39 | No auditable result numbers. | `nextstrain2018hadfield`, `rambaut2020pangolin`: OK for surveillance/lineage systems. | none | Consistent. | Verified |
| C6 | ch1 41-49 | UNVERIFIED/illustrative: three-step workflow, weeks-months, millions since 2020, influenza tens of thousands/decades, 1,000 -> 50-100/top 5-10%. No local CSV path. The final search-space claim is directionally consistent with Ch4 practical framing (typical 500 -> 10-50, 7-9x). | none | `sec:intro_objectives`, `sec:intro_contributions`, `ch:mutbench`, `ch:discussion`, `sec:future_work` all resolve. | No regression terms. | Minor |
| C7 | ch1 59 | Number "three problems" matches following three problem paragraphs. | none | none | Consistent. | Verified |
| C8 | ch1 61-63 | No benchmark result numbers. | none | none | Consistent with MutClust validation limitation. | Verified |
| C9 | ch1 65-68 | Position 484/E484K/E484A examples: biologically plausible; no local CSV source required for example. | none | none | DMS wording correctly says single amino-acid substitution. | Verified |
| C10 | ch1 70-73 | No result numbers except problem ordinal. | `rice1976algorithm`: OK for algorithm selection framing. | none | Consistent. | Verified |
| C11 | ch1 79-87 | VERIFIED: Objective 1 numbers 11, 20x39x11=8,580 from `results/mutbench/stage3_full_results.csv`; 14 families verified in same CSV. | none | `ch:results`, `subsec:feature_ablation` resolve to Ch4 feature-ablation section. | Consistent with abstract scope. | Verified |
| C12 | ch1 89-100 table fragment | VERIFIED: 11 main, 12 Stage 3, 28 Wave 4 targets, 12 labeled + 16 unlabeled, 10 Layer A' targets from Ch4 Wave 4/5 text and `results/mutbench/codex_wave4/*`, `results/mutbench/codex_layerA_prime/lopo_summary.csv`. | none | DISCREPANCY: row says "Chapter discussion Paragraphs" for `para:w4_tier2_lopo` and `para:w5_layer_a_prime`, but both labels are in `paper/dissertation/chapters_en/ch4_results.tex`, not `ch5_discussion.tex`. | Cross-ref target text is misleading even though labels resolve. | Major |

## Recent Fix Verification

- D614G: VERIFIED fixed in Ch4 line 219 and `results/mutbench/layer_a_tags.csv` line 9: retained as functional/stability-affecting, not excluded.
- Omega CI: scoped abstract and Ch1 use [0.201, 0.346]. VERIFIED. Note stale body-target text `[0.195, 0.333]` remains in `results/mutbench/cluster_bootstrap_omega_summary.csv`, but not in scoped prose.
- HIV-1 Layer A: REGRESSION outside scope. Ch3 line 316 is correct (26 tags, 23 mapped gp120), but Ch4 lines 261 and 902 still reverse this as operational 26 vs literature-curated 23.
- Stage 1 region: REGRESSION outside scope. Ch4 line 50 says 417 AA, but Ch4 table line 63 still says `Functional regions (439)`.
- Single-position scoring: scoped abstract uses required "single-position scoring (gap-aware)"; no scoped old "point substitutions only" wording found.

## Per-Section Severity Counts

| Section | Critical | Major | Minor | Verified | Regression |
|---|---:|---:|---:|---:|---:|
| Abstract | 0 | 0 | 2 | 3 | 0 |
| Ch1 Research Background | 0 | 0 | 2 | 7 | 0 |
| Ch1 Objectives/table lines 79-100 | 0 | 1 | 0 | 1 | 0 |
| Cross-chapter fix verification | 0 | 2 | 0 | 3 | 2 |

## Overall Severity Tally

Critical: 0. Major: 3. Minor: 4. Regression: 2. Verified paragraph/block checks: 11.

Web sources used for citation sanity: WHO SARS-CoV-2 tracking/data pages; ViroGym summary page; EVEREST Sciety/Research Square summary; ProteinGym official GitHub/PyPI pages.

RESULT_AUDIT_V2_J1: critical=0 major=3 minor=4 regression=2
