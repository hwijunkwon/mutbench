# Audit v2 Job 3: ch2_background.tex lines 1--150

Scope file: `paper/dissertation/chapters_en/ch2_background.tex` lines 1--150. Evidence checked against `paper/dissertation/thesis_en.aux`, `paper/dissertation/references.bib`, and relevant `results/mutbench/` CSV/MD files.

## Per-Paragraph Table

| Para | Lines | Numerical claims | Citations | Cross-refs | Consistency / recent-fix check | Severity |
|---|---:|---|---|---|---|---|
| P0 | 1--7 | No scientific numeric claim. | None. | `ch:background`, `sec:bg_hotspot` defined; aux resolves `sec:bg_hotspot` to Related Research. | OK. | Verified |
| P1 | 9 | No numeric claim. | None. | None. | Intro sentence consistent. | Verified |
| P2 | 14--18 | `10^{-3}`--`10^{-5}` RNA-virus mutation rates: literature-backed, no MutBench CSV expected; VERIFIED by `holmes2009evolution`, `sanjuan2010viral`. Enumerated 3 applications and 4 method categories are narrative taxonomy, not CSV. | Both citations plausibly support viral mutation-rate range. | None. | OK. | Verified |
| P3 | 20--24 | D614G near-fixation/fitness/founder-effect claim: no numeric result; D614G retained as functional in `results/mutbench/layer_a_tags.csv` row `SARS-CoV-2,614,functional`. | No direct cite in paragraph; underlying Korber evidence appears in Layer A CSV. | None. | Recent fix OK: not excluded. | Verified |
| P4 | 26--30 | No result numeric except method-specific claims. | `mullick2021entropy`, `koyama2020variant`, `obermeyer2022analysis` plausibly support entropy/K-means and SARS-CoV-2 large-scale frequency/fitness analyses. | None. | OK. | Verified |
| P5 | 32--37 | `3D` and `>1,000 times larger`: no repository CSV; broad biology claim is plausible but not source-pinned in paragraph. | Cancer-method citations match claims. | None. | Internal contrast with viral setting OK. | Minor |
| P6 | 39--45 | `10` underlying information families and `20` scoring channels: VERIFIED against `results/mutbench/stage3_full_results.csv` (20 `score` levels) and Ch3 methods; older `combined_10scoring_results.csv` has 10 underlying scores. | Phylogeny/homoplasy citations plausible. | `sec:information_analysis` resolves to Ch3/Results Information-Type Analysis. | OK. | Verified |
| P7 | 47--50 | No result numeric. | None. | None. | OK. | Verified |
| P8 | 52--57 | `omega > 1`; `four` selection-pressure channels and `three` FUBAR summaries: supported by Ch3 scoring text and `results/mutbench/stage3_full_results.csv` scores `fubar`, `fubar_pos`, `fubar_bf`, `dnds_proxy`. | HyPhy/MEME/FUBAR/FEL/SLAC/BUSTED citations plausible. | `ch:mutbench`, `sec:scoring_detection`, `ch:discussion`, `sec:future_work` all resolve in aux. | OK. | Verified |
| P9 | 59--65 | DBSCAN parameters are definitional; no result CSV expected. | `ester1996dbscan` OK. | None. | OK. | Verified |
| P10 | 67--71 | `99.76%`, `epsilon=0.15`, `MinPts=5`, `4` clusters: VERIFIED only in `docs/mutclust/논문2_MutClust_심층정리.md`, not under `results/mutbench/` or `paper/dissertation/`; no authoritative CSV found. | `youn2025mutclust` plausibly supports, but repository evidence path is non-result documentation. | None. | Claim should cite a result archive if treated as quantitative benchmark evidence. | Minor |
| P11 | 73--78 | `single parameter` is a method claim; `probabilistic` wording OK. | `campello2013hdbscan` plausible. | None. | OK. | Verified |
| P12 | 80--83 | No result numeric; `xi` extraction method is standard OPTICS detail. | `ankerst1999optics` plausible. | None. | OK. | Verified |
| P13 | 85--86 | No result numeric; H-score definition qualitative. | `youn2025mutclust` plausible. | None. | OK. | Verified |
| P14 | 88--94 | `all possible single amino acid substitutions`, `single`, `every position`: DMS definition, literature-backed. | `fowler2014dms` OK. | `subsec:bg_dms` defined and resolves. | OK. | Verified |
| P15 | 96--97 | `thousands` is generic literature claim; no CSV expected. | None. | None. | OK. | Verified |
| P16 | 99--103 | SARS-CoV-2 RBD/full Spike/H3N2/proteome DMS claims: literature-backed. `two SARS-CoV-2 proteins` is from `bloom2023fitness` context, not a MutBench CSV. | `starr2020dms`, `dadonaite2023dms`, `lee2018h3n2dms`, `bloom2023fitness` all plausible. | None. | OK. | Verified |
| P17 | 105 | Very dense. `top-k`, HIV-1/H3N2/SARS-CoV-2 escape audit and Layer A/B/C distinctions: internal refs resolve; DMS source list partly names papers without `\cite{}` for Moore--Williamson, Dadonaite 2024, Haddox, Simonich, Aditham, Bakhache in this sentence. | `greaney2021RBD`, `greaney2022spike` OK; missing formal cite commands for several named source datasets. | `ch:discussion`, `sec:cross_validation_escape`, `ch:results`, `tab:vaccine_escape_stage3`, `tab:gt_positions`, `ch:mutbench` all resolve. | Internally consistent with Ch3 Layer C table and escape audit framing. | Minor |
| P18 | 107--112 | `45` viral DMS datasets, `40` WHO panel: VERIFIED by `paper/dissertation/references.bib` note for `gurev2026everest_v3`; not a MutBench CSV. Pseudovirus/authentic examples consistent with Ch3 DMS table. | `gurev2026everest_v3` plausibly supports; current but not web-verified. | `ch:mutbench` resolves. | OK. | Verified |
| P19 | 114--116 | No internal numeric claim. | `livesey2020using` plausibly supports DMS-as-benchmark. | None. | OK. | Verified |
| P20 | 118--121 | No result numeric; VAE/MSA claims literature-backed. | `riesselman2018deep`, `frazer2021eve` plausible. | None. | OK. | Verified |
| P21 | 124--135 | `650 million` parameters and `~250 million` UniRef sequences: citation-backed by ESM-2/Rives; no MutBench CSV. LLR formula OK. | `lin2023esm2`, `rives2021biological` plausible. | None. | OK. | Verified |
| P22 | 137--139 | No result numeric. | `notin2022tranception` plausible. | None. | OK. | Verified |
| P23 | 141--144 | `>2 billion` ProtTrans sequences: citation-backed. `8,580` headline grid and ESM-3 license exclusion: VERIFIED by Ch3 license section and `results/mutbench/stage3_full_results.csv` row count. `20-scoring panel` supported by Stage3 scores. | `elnaggar2022prottrans`, `hayes2024esm3`, structure-aware PLM citations plausible. | `ch:mutbench`, `para:external_licenses` resolve. | OK. | Verified |
| P24 | 146--148 | `three components`; EVEscape composite form: supported by Ch3 scoring text and `results/mutbench/stage3_full_results.csv` score `EVEscape_composite`. | `thadani2023evescape` OK. | `sec:scoring_detection` resolves. | OK. | Verified |
| P25 | 150 | Incomplete paragraph in scope. No auditable result numeric in line 150. | `cheng2023alphamissense` plausible for AlphaMissense. | None in scoped line. | No issue in scoped line only. | Verified |

## Per-Section Severity Counts

| Section | Paragraphs | Critical | Major | Minor | Verified | Regression |
|---|---:|---:|---:|---:|---:|---:|
| Related Research header | P0--P1 | 0 | 0 | 0 | 2 | 0 |
| Mutation Hotspot Detection Methods | P2--P8 | 0 | 0 | 1 | 6 | 0 |
| Density-Based Clustering | P9--P13 | 0 | 0 | 1 | 4 | 0 |
| Deep Mutational Scanning as Ground Truth | P14--P20 | 0 | 0 | 1 | 6 | 0 |
| Protein Language Models for VEP | P21--P25 | 0 | 0 | 0 | 5 | 0 |

## Overall Severity Tally

Critical: 0; Major: 0; Minor: 3; Verified: 23; Regression: 0.

Recent-fix verification: no scoped paragraph uses old D614G exclusion wording, old omega CI `[0.195, 0.333]`, old HIV-1 Layer A count wording, old Stage 1 `439 AA`, or `point substitutions only`. Active cross-chapter text checked in Ch3/Ch5 uses `[0.201, 0.346]`, HIV-1 `26 (23 mapped)`, and `single-position scoring (gap-aware)`.

RESULT_AUDIT_V2_J3: critical=0 major=0 minor=3 regression=0
