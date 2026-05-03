# Audit v2 Job 7: ch3_methods.tex lines 601--892

Scope file audited: `paper/dissertation/chapters_en/ch3_methods.tex` (requested path resolves under `paper/dissertation/`). Web search was not needed; all suspicious numerical claims were checkable locally.

## Per-paragraph table

| Lines | Unit | Numerical claims | Citations | Refs / consistency | Severity |
|---:|---|---|---|---|---|
| 601--616 | Tranception/ESM correlation table tail and note | VERIFIED against `results/mutbench/feature_analysis/tranception_esm_correlation.csv` and `_per_pathogen.csv`: HCV 340/0.737/<1e-58/0.980/<1e-200; HIV-1 450/0.043/0.36/0.158/7.8e-4; RSV 550/0.805/<1e-120/0.967/<1e-300; Norovirus 536/0.812/<1e-120/0.973/<1e-300; Dengue 490/0.828/<1e-120/0.946/<1e-200; MERS 1330/0.836/<1e-300/0.963/<1e-300; Rabies 490/0.679/<1e-65/0.949/<1e-200; EV-A71 260/0.801/<1e-58/0.919/<1e-100; Zika 451/0.643/<1e-53/0.713/<1e-70. | None. | `ch:discussion`, `sec:esm2_leakage` resolve. | Verified |
| 617--625 | Stability, structural stability, ESM-2, composite scores | 11 pathogens x 39 detectors and ESM-2 33 layers/650M VERIFIED in `results/mutbench/stage3_full_results.csv` and ESM-2 model naming in `results/mutbench/provenance/external_resource_licenses.csv`. | `thadani2023evescape` plausibly supports EVEscape construction. | Internally consistent with Ch2/Ch4 ESM-2 usage. | Verified |
| 627--632 | EqualWeight variants | VERIFIED: 8,580 rows, 20x39x11 grid, 0.296 in `results/mutbench/stage3_statistics.csv`; 12-fold nested LOPO means 0.070/0.083 close to `results/mutbench/feature_analysis/feature_ablation_nested_lopo_summary.csv` and Ch4 table; 10 features and 4-feature protocol consistent. | None. | All refs resolve. No label-leakage contradiction found. | Verified |
| 637--640 | Detection families overview | VERIFIED: 39 detectors, 14 families in `results/mutbench/stage3_full_results.csv`; excluded 2 ensembles UNVERIFIED by CSV but methodological/design claim. | None. | `tab:detection_families` resolves. | Minor |
| 641--675 | Detection-family table | VERIFIED detector counts and parameter strings against `results/mutbench/stage3_full_results.csv`: FreqThresh 4, AdaptiveKnee 1, AdaptWin 2, Wavelet 3, Spectral 2, CUSUM 3, KDE 3, ScoreDBSCAN 2, SlidingTest 2, LocalContrast 3, GradPeak 2, Bayes 2, SWAN 9, MutClust-Orig 1, total 39. | `mercatelli2020geographic`, `anastassiou2001genomic`, `arneodo2011wavelet`, `ester1996dbscan`, `tokheim2016hotmaps`, `tajima1989statistical`, `youn2025mutclust` are plausible method precedents. | `tab:detection_families`/`tab:detection_variants` duplicate target same table intentionally. | Verified |
| 677--680 | Supervised ML exclusion | 11 pathogens and 9--54 Layer A positives VERIFIED in `results/mutbench/pahd_r_data_processing_pathogen_summary.csv`; detection family omega 0.013 VERIFIED as family 0.012623 in `results/mutbench/stage3_statistics.csv`; 14/39 verified above. | None. | `subsec:variants` resolves. | Verified |
| 686--710 | Design-characteristics table | Unique seqs and lengths VERIFIED against Ch3 `tab:pathogen_data`; positive rates VERIFIED from `results/mutbench/pahd_r_data_processing_pathogen_summary.csv`; HIV-1 26 tags / 23 mapped VERIFIED by `results/mutbench/layer_a_tags.csv` and feature matrix. Time spans UNVERIFIED by CSV. | None. | `tab:design_characteristics` resolves. Recent fix HIV-1 retained. | Minor |
| 712 | Heterogeneity paragraph | Unique-count 530--5,019, length 261--1,330, positive rate 0.7--15.9 VERIFIED from Ch3 tables/`pahd_r_data_processing_pathogen_summary.csv`. DISCREPANCY: temporal coverage says ~2--50 years, but the table immediately above lists ~5--50 years. | None. | Internal mismatch with `tab:design_characteristics`. | Minor |
| 714--718 | Mitigating considerations | 1,000 sequences and +/-0.002 subsampling VERIFIED only indirectly by Ch4 lines 470--472; no local CSV found for the subsampling grid, so mark UNVERIFIED for authoritative CSV. 0.296 and n=530 VERIFIED in `stage3_statistics.csv` and Ch3 table. | None. | `sec:robustness_validation` resolves. | Minor |
| 727--740 | Metrics list | 6 DMS pathogens VERIFIED in Ch3 `tab:gt_positions` and `stage3_full_results.csv` has MCC/F1/precision/recall fields; Fisher/enrichment/constrained FPR are methodological. | None. | `eq:mcc` resolves. Layer B TN/FP treatment consistent with metric definition. | Verified |
| 742--755 | Stage metric rationale and MCC equation | 340--1,330 AA and 530--5,019 unique seqs VERIFIED from Ch3 `tab:pathogen_data`; positive rates 0.7--15.9 VERIFIED. | `chicco2020mcc` OK for MCC vs F1 in imbalanced classification. | `eq:hotspot_score`, `subsec:hotspot_score`, `eq:mcc` resolve. | Verified |
| 757 | Headline MCC paragraph | 8,580 rows and columns `mcc`, `precision`, `recall`, `f1`, `n_detected` VERIFIED in `results/mutbench/stage3_full_results.csv`; positive-rate range VERIFIED. DISCREPANCY: text says AUROC values per cell are retained in the archived CSV bundle, but `stage3_full_results.csv` has no AUROC column; no obvious AUROC per-cell file found in `results/mutbench/`. | `chicco2020mcc` OK. | Refs resolve. | Major |
| 759 | Stability excluded from Stage 2 | 11 pathogens VERIFIED; methodological claim consistent with Ch4 Stage 2 rationale. | None. | No issue. | Verified |
| 764--766 | Three-way ANOVA setup | VERIFIED in `results/mutbench/stage3_statistics.csv`: 20 levels, 14 families, 11 pathogens, 8,580 rows, residual df 7,970, 20x14x11=3,080 cells, cell omega 0.234 (rounded from `ancova_omega_summary.csv` baseline 0.2325), headline 0.296. | `cohen1988statistical` OK for thresholds. | Refs resolve. | Verified |
| 768 | Cell-level vs evaluation-level omega | VERIFIED: 0.296 in `stage3_statistics.csv`; 3,080 cells from `stage3_full_results.csv`; 0.234 approx from `ancova_omega_summary.csv`; CI [0.201,0.346] from `omega_robustness_5way.csv`. Recent fix CI retained. | Cohen threshold citation carried from prior paragraph. | Refs resolve. | Verified |
| 770 | ANCOVA | VERIFIED in `results/mutbench/ancova_omega_summary.csv`: pathogen baseline 0.1079, scoring x pathogen 0.2325 to 0.2741, family x pathogen 0.0801 to 0.0878. p<1e-167 not in that CSV; UNVERIFIED locally. | None. | `sec:scoring_input_heterogeneity` resolves. | Minor |
| 772 | Bayesian partial pooling | Archived half-Normal values VERIFIED in `results/mutbench/bayesian_omega_summary.csv`: n=8580, 4x2000, seed 42, mean 0.3185/0.319, HDI [0.246,0.396], P=0.99975. Exploratory half-Cauchy 0.252/[0.188,0.314]/0.996 not in CSV except as `body_target_*`; treat as UNVERIFIED primary output. | None. | Refs resolve. | Minor |
| 774--783 | Robust checks and omega equation | ART archived 0.343 VERIFIED in `results/mutbench/art_omega.csv`; exploratory 0.277 is body target only. Levene W/df/p, Kruskal H/p, and Bonferroni denominator 780 are UNVERIFIED by local CSV found; 20x39=780 and 8,580 arithmetic verified. | `wobbrock2011aligned`, `cohen1988statistical` OK. | `tab:vaccine_escape_stage3`, `eq:omega_squared` resolve. | Minor |
| 787--790 | LOPO | 11 iterations UNVERIFIED for current 11-pathogen design: `results/mutbench/lopo_9pathogen_cv.csv` has only 9 folds and 9-pathogen-era scoring names. 280 = 20x14 and random 1/280=0.36% VERIFIED arithmetically. | None. | Internal methods say 11-pathogen, archive appears stale/incomplete. | Major |
| 795 | Nested-LOPO 4-feature protocol | 12 folds, full10/fixed4 means and 1,000 bootstrap CI VERIFIED in `results/mutbench/feature_analysis/feature_ablation_nested_lopo*.csv`; 5,000 sign-flip p-value not present in summary CSV, UNVERIFIED. | None. | Refs resolve; label-aware variant use consistent. | Minor |
| 799--801 | Friedman test | DISCREPANCY: paragraph says 11 pathogens as blocks, but archived `results/mutbench/friedman_top20_multilayer.csv` has 9 pathogens and `results/mutbench/stage3_statistics.csv` Friedman df/source also reflects older 9/top20 setup. | `demsar2006statistical` OK. | Needs update or new archive. | Major |
| 806--807 | BCa bootstrap CIs | 10,000 resamples and n=11 coverage simulation UNVERIFIED; available `results/mutbench/pathogen_bootstrap_ci.csv` uses n_pathogens=9 for older combo CI. Cluster bootstrap 1,000 over 11 verified in `omega_robustness_5way.csv`. | None. | `ch:results` resolves. | Major |
| 809--810 | Robustness-frame triangulation | VERIFIED in `results/mutbench/omega_robustness_5way.csv`, `block_bootstrap_omega_summary.csv`, `mixed_effects_omega_summary.csv`, `bayesian_factor_omega_summary.csv`: wild [0.2005,0.3032], phylo [0.2022,0.3457], p=0.008, mixed 0.3398/ICC 0.135, Bayesian 0.3155/[0.2421,0.3882]/P=0.99975, standard [0.2008,0.3455]. Recent CI fix retained. | `cameron2008bootstrap` OK. | Refs resolve. | Verified |
| 812 | Jackknife acknowledgement | No numerical claim beyond 11 pathogens; consistent with text. | None. | Label local. | Verified |
| 814 | Mantel/Procrustes acknowledgement | No numeric claim; `mantel1967nonparametric` plausibly supports Mantel. | OK. | `sec:gt_heterogeneity` resolves but is a phantom label in Ch5 limitations, not a real section heading; minor navigation issue inherited from prior audits. | Minor |
| 818 | Subsample robustness methods | 25/50/75/100% are method settings; no authoritative CSV found, but Ch4 text repeats. | None. | No issue beyond earlier missing archive. | Minor |
| 822--825 | Feature ablation methods | 10 leave-one-out, 9-feature ensembles, subset sizes 2--9, 98% target consistent with `results/mutbench/feature_ablation_results.csv` and feature-analysis CSVs. | None. | No issue. | Verified |
| 827--836 | Weight sensitivity | 1/3, 0.05--0.95, 171 combinations, 7 scenarios consistent with Stage 1 weight-sensitivity method, but no authoritative weight-grid CSV found in `results/mutbench/`; UNVERIFIED. | None. | Stage 1 only; internally consistent. | Minor |
| 838--845 | Statistical validation bootstrap | 3 methods, 7 regions, Stage 1/Stage 2 distinction consistent with Ch4; no CSV issue because method description. | None. | `subsec:wild_cluster_future` resolves. | Verified |
| 847--851 | Permutation tests | 1,000 label permutations, 200 circular rotations, formula p=(count+1)/(Nperm+1) are method settings; no CSV found but consistent with Ch4. | None. | No issue. | Minor |
| 853 | Pairwise comparison | No numeric claim. | None. | No issue. | Verified |
| 858--864 | Stage 3 integration | 20 scoring, 10 features, groups 3/4/5/5/10, k=1..10, RF 200/depth 5/seed 42, 11 vs 12, Zika 505 AA, 3/11 and 2,340 escape evaluations: mostly VERIFIED in `stage3_full_results.csv`, `feature_ablation_results.csv`, `feature_analysis/*`, and `vaccine_escape_validation.csv` (12 rows; 3 pathogens x selected methods). 2,340 = 3x20x39 arithmetic, not directly archived. | None. | `subsec:rf_importance` is a phantom label in Ch4 but resolves; recent wording says single-position scoring/gap-aware elsewhere, no old wording here. | Minor |
| 868--870 | Code/data availability | 8,580 archive, seed 42, 100-iteration sequence 42--141, tool versions files VERIFIED in `stage3_full_results.csv`, `results/mutbench/provenance/*`. DISCREPANCY: `environment.yml` and `requirements-pinned.txt` are claimed at repository root but are absent. DOI future placeholder expected. | None. | Refs resolve. | Major |
| 872--887 | External licenses | 20-plus resources and license matrix exist, but `results/mutbench/provenance/external_resource_licenses.csv` is not robustly machine-readable: unquoted `greaney2021RBD,greaney2022spike` creates an extra field under standard CSV parsing. Several future/pending datasets are citation-only and plausible but not independently verified. | Cites for MAFFT, CD-HIT, MMseqs2, ESM-2, Tranception, EVE/EVEscape, Greaney, Haddox plausibly support resources; 2025/2026 benchmark/dataset citations are plausible but should remain citation-only. | License compatibility claim mostly consistent with matrix; machine-readable claim weakened by malformed CSV row. | Major |
| 890--892 | Chapter summary | 11 viruses, 3 layers, 20 scoring types, 14 families, Stage 3 all VERIFIED above. | None. | `ch:results` resolves. | Verified |

## Recent fix verification

- D614G: VERIFIED retained as `functional` in `results/mutbench/layer_a_tags.csv` and Ch4 uses 417 AA functional regions; no exclusion regression found.
- Omega CI: VERIFIED current text uses [0.201, 0.346], not [0.195, 0.333].
- HIV-1 Layer A: VERIFIED 26 source tags / 23 mapped to gp120 appears in caption.
- Stage 1 region: no old 439 wording in this chunk; Ch4 current text uses 417 AA.
- Single-position scoring/gap-aware: no old "point substitutions only" wording in this chunk.

## Severity counts by section

| Section | Critical | Major | Minor | Verified |
|---|---:|---:|---:|---:|
| Scoring/detection methods, 601--680 | 0 | 0 | 2 | 5 |
| Design/evaluation metrics, 686--759 | 0 | 1 | 3 | 5 |
| ANOVA/validation/statistics, 764--853 | 0 | 4 | 8 | 5 |
| Stage 3/reproducibility/licenses, 855--892 | 0 | 2 | 1 | 1 |

## Overall severity tally

Critical: 0. Major: 7. Minor: 14. Regression: 0. Verified rows: 16.

Headline: stale or missing support files remain the main risk: 11-pathogen LOPO/Friedman/BCa claims cite archives that are still 9-pathogen-era or absent, and reproducibility claims name missing environment files.

RESULT_AUDIT_V2_J7: critical=0 major=7 minor=14 regression=0
