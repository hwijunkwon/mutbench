# Audit v2 Job 4: ch2_background.tex lines 151-299

Scope: `paper/dissertation/chapters_en/ch2_background.tex:151-299`. Paragraph-level audit; web not used because local bib/results were sufficient for suspicious claims.

## Per-Paragraph Table

| Lines | Section | Numerical claims | Citations | Cross-refs | Consistency / recent-fix check | Severity |
|---:|---|---|---|---|---|---|
| 151-156 | PLMs / EVEREST | 10 info families, 20 scoring channels: VERIFIED via `results/mutbench/stage3_full_results.csv` (20 scorings) and `paper/dissertation/chapters_en/ch3_methods.tex` scoring table. | `gurev2025everest`, `gurev2026everest_v3`: OK for viral VEP/PLM-vs-alignment framing. | `subsec:bg_benchmarking_gap`, `sec:information_analysis` resolve correctly. | Consistent with Ch4 pathogen-dependence framing; no old fix wording. | Verified |
| 158-165 | ProteinGym contrast | >70 predictors, 217 DMS, 2.7M variants: VERIFIED for original ProteinGym via `references.bib:notin2023proteingym`; not a MutBench CSV claim. Task/domain/objective contrast is internally consistent. | `notin2023proteingym`: OK. | None. | Per-region hotspot vs per-substitution VEP distinction consistent across Ch2/Ch5. | Verified |
| 170-181 | Surveillance platforms | No quantitative result claims beyond enumerated reasons (1)-(3). | `nextstrain2018hadfield`, `rambaut2020pangolin`, `luksza2014predictive`, `huddleston2020integrating`: OK. | None. | Consistent with benchmark/surveillance distinction. | Verified |
| 183-185 | Data sources | No result numerics. | `shu2017gisaid`: OK; outbreak.info uncited but descriptive. | None. | Consistent. | Verified |
| 190-194 | Maher features | No result numerics. | `maher2022predicting`: OK for SARS-CoV-2 future-variant feature analysis. | `sec:information_analysis` resolves. | Single-pathogen limitation consistent. | Verified |
| 196-198 | DCA / epistasis | AUC 0.76 vs 0.63: VERIFIED from cited paper metadata/claim, not local CSV; mark WEB-VERIFY if strict source check is required. 20-scoring panel: VERIFIED via `results/mutbench/stage3_full_results.csv`. | `rodriguez2022epistatic`: OK. | `sec:scoring_detection`, `ch:discussion`, `ch:results` resolve. | Strong internal consistency; explicitly avoids overclaiming single-position regime. No “point substitutions only” regression. | Verified |
| 200-201 | Semantic change | No numeric result claims. | `hie2021learning`: OK. | None. | Consistent with PLM-feature rationale. | Verified |
| 203-204 | EVEscape | Three-component score: VERIFIED from `references.bib:thadani2023evescape`; no local CSV. | `thadani2023evescape`: OK. | None. | Consistent with multi-source framing. | Verified |
| 206-208 | Cross-pathogen feature gap | 20 scoring channels, 10 info families, 11 pathogens: VERIFIED via `results/mutbench/stage3_full_results.csv` and `paper/dissertation/chapters_en/ch3_methods.tex`. | No new cites. | `sec:information_analysis` resolves. | Consistent with Ch3/Ch4. | Verified |
| 213-215 | Algorithm selection | Stage 1 / Stage 2 / 11 pathogens: VERIFIED via `paper/dissertation/chapters_en/ch3_methods.tex` and `results/mutbench/stage3_full_results.csv`. | `rice1976algorithm`: OK. | `ch:results`, `subsec:9pathogen_metrics` resolve. | Label name is stale (`9pathogen`) but target is correct. | Minor |
| 217-219 | No Free Lunch | No numeric result claims. | `wolpert1997nfl`: OK. | None. | Consistent. | Verified |
| 221-223 | Meta-learning / AutoML | No numeric result claims. | `kerschke2019algorithm`, `bischl2016aslib`, `feurer2015automl`, `kotthoff2016algorithm`: OK. | `ch:discussion` resolves. | Consistent. | Verified |
| 225-228 | Benchmarking principles | Three requirements, 14 families, 3-layer GT, Stage 1/2 metrics: VERIFIED via `paper/dissertation/chapters_en/ch3_methods.tex`; 14 families also via `results/mutbench/stage3_full_results.csv`. | `weber2019benchmarking`, `mangul2019systematic`, `boulesteix2017towards`, `youn2025mutclust`: OK. | `ch:discussion`, `subsec:9pathogen_metrics` resolve. | Self-assessment caveat consistent. | Verified |
| 233-242 | Benchmarking gap | Bailey 26 tools / 9,423 exomes: VERIFIED via `references.bib:bailey2018comprehensive`; ViroGym 13/79/552,937/7: VERIFIED via `references.bib:virogym2026`; 40+ cancer methods: VERIFIED via `references.bib:pons2020computational`. | Cites plausibly support claims. | None. | Consistent except upcoming table contradicts Bailey tool count. | Verified |
| 246-252 | VEP benchmarks | ProteinGym 217 and 2.7M: VERIFIED via `references.bib:notin2023proteingym`; EVEREST v3 45/31/4/40/16: VERIFIED via `references.bib:gurev2026everest_v3`; no MutBench CSV involved. | `notin2023proteingym`, `frazer2021eve`, `thadani2023evescape`, `gurev2025everest`, `gurev2026everest_v3`, `plant2025antigenic`, `shah2024h3n2ml`, `smith2004antigenic`, `cheng2023alphamissense`: OK. | `ch:results`, `sec:cross_validation_escape` resolve. | Consistent with Ch5 caution that EVEREST is parallel, not independent confirmation. | Verified |
| 254-260 | MutBench capabilities | `omega^2=0.296`: VERIFIED in `results/mutbench/stage3_statistics.csv` (0.29625198). CI [0.201,0.346]: VERIFIED in `results/mutbench/cluster_bootstrap_omega.csv` percentiles (0.20086, 0.34549). 11 pathogens / 20 types / 39 variants / 8,580 evals: VERIFIED in `results/mutbench/stage3_full_results.csv`. `omega^2≈0.39` residual: VERIFIED by SS share in `results/mutbench/stage3_statistics.csv`, not direct omega field. HIV-1 7.19x and p=2.5e-16: VERIFIED via `results/mutbench/vaccine_escape_stage3.csv` row `HIV-1,freq,Wavelet(t=1.5)` (7.1875; p 3.16e-19 × 780 = 2.47e-16). H3N2 9.36x: VERIFIED same CSV (9.3621). 82% disjoint / 69% overlap: VERIFIED only in `paper/dissertation/chapters_en/ch4_results.tex` table footnote, not a CSV found. | Cites in preceding paragraph support comparison; no citation problem. | `tab:vaccine_escape_stage3`, `tab:benchmark_comparison` resolve. | Recent fixes OK: CI uses new [0.201,0.346]; no old CI regression. | Minor |
| 262-283 | Benchmark comparison table | DISCREPANCY: Bailey row says `~10 tools`, but line 233 says 26 computational tools and `references.bib:bailey2018comprehensive` supports 26. Caption says EVEREST v3 and ProteinGym v1.3 are peer-reviewed; local `references.bib:gurev2026everest_v3` is bioRxiv and `notin2025proteingym_v13` is a website release, so this is SUSPICIOUS/DISCREPANCY. Other table numerics mostly verified from bib/local CSV: MutBench 11/780/omega yes; ViroGym 13/79 yes; ProteinGym 217/90+ yes. | Table citations OK, but peer-review status claim is not supported by local bib entries. | Label resolves. | Internally inconsistent with line 233 and references. | Major |
| 285 | Motivation sentence | No numeric claims. | None. | `ch:mutbench` resolves. | Consistent. | Verified |
| 293-299 | Related research summary | 11 pathogens / 20 scoring types / 6 categories / 14 families: VERIFIED via `results/mutbench/stage3_full_results.csv` and Ch3 method table. `omega^2=0.296`: VERIFIED in `results/mutbench/stage3_statistics.csv`. | `youn2025mutclust`: OK. | `sec:bg_hotspot`, `ch:discussion`, `sec:future_work`, `ch:mutbench` resolve. | Recent fixes OK: “single-position scoring regime” present; no old “point substitutions only” wording. | Verified |

## Per-Section Severity Counts

| Section | Critical | Major | Minor | Verified |
|---|---:|---:|---:|---:|
| PLM / ProteinGym / surveillance / feature importance (151-208) | 0 | 0 | 0 | 9 |
| Algorithm selection and benchmarking methodology (213-228) | 0 | 0 | 1 | 4 |
| Benchmarking gap and comparison (233-285) | 0 | 1 | 1 | 3 |
| Related research summary (293-299) | 0 | 0 | 0 | 1 |

## Overall Severity Tally

Critical: 0  
Major: 1  
Minor: 2  
Verified paragraphs: 17  
Regression: 0 in scoped ch2 lines 151-299.

Main actionable issue: fix Table `tab:benchmark_comparison` caption/status and Bailey method count. Suggested replacement: Bailey methods compared = `26 tools`; caption should say ViroGym and EVEREST v3 are preprints and ProteinGym v1.3 is a release/update unless externally confirmed peer-reviewed.

RESULT_AUDIT_V2_J4: critical=0 major=1 minor=2 regression=0
