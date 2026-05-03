# Audit v2 Job 8: `chapters_en/ch4_results.tex` lines 1--330

## Per-Paragraph Audit Table

| Para / lines | Numerical claims and source check | Citations / refs | Consistency and severity |
|---|---|---|---|
| P1 L5--7 | Stage 1 refs; Stage 2 `11`, `20`, `14`, `5`, `39`: VERIFIED against `results/mutbench/stage3_full_results.csv` (`8580` rows = `20*39*11`) and ch3 design. | `sec:variant_comparison`, `sec:phylo_simulation`, `sec:9pathogen_results` resolve in this chapter. | Minor: L6 says two baselines, but L25/table use three if HDBSCAN-Auto is counted as baseline. |
| P2 L9--14 Key box | `omega^2=0.296`: VERIFIED in `results/mutbench/stage3_statistics.csv` (`scoring×pathogen=0.29564`, rounded). LOPO `0/11`: VERIFIED in `results/mutbench/lopo_9pathogen_cv.csv`/ch4 later text. HIV-1 `7.19x`, `p_adj=2.5e-16`, H3N2 `9.36x`: VERIFIED in `results/mutbench/vaccine_escape_stage3.csv` and table footnote lines 958--972. Bonferroni survivor means rely on footnote summary; exact aggregate CSV not found in this scope. | `tab:vaccine_escape_stage3` resolves later in ch4. | Verified. |
| P3 L25 | Synthetic genome `29,903`, GT `1,251`, 5 variants/3 baselines, Hybrid `F1=0.785`, `HS=0.778`, random `0.018`, F1 range `0.67--0.78`, precision `>0.96`, HDBSCAN recall/precision `0.944/0.079`, real `F1=0.123`: MutClust values VERIFIED in `results/mutbench/method_comparison.csv`; real values in `results/mutbench/method_comparison.csv`/review trail; HDBSCAN/random baseline source not explicit in CSV list. | `tab:hotspot_scores`, `sec:real_gisaid_benchmark` resolve. | Minor: HDBSCAN/random-baseline source path should be explicit. |
| Table L27--43 | Table values for MutClust rows VERIFIED in `results/mutbench/method_comparison.csv` (Hybrid `0.968/0.659/0.785/0.706/0.778`; Original/Fixed/dNdS ranges match). HDBSCAN/Frequency/Sliding rows are UNVERIFIED from located CSVs. | Label resolves. | Minor source-path gap. |
| P4 L49--52 | Functional prose `417 AA`, `32.8%`, `1,251 nt`; DMS `252`, `19.8%`; convergent `97`, `7.6%`; Jaccard `0.006`: mostly VERIFIED against `results/mutbench/multi_ground_truth_summary.csv` and ch3 functional-region definition. | `dadonaite2023dms`, `cao2023ba286`, `carabelli2023convergent` plausibly support DMS/convergent claims; `tab:multi_gt` resolves. | Verified; recent fix: prose uses `417`, not old `439`. |
| Table L54--74 | DMS and convergent values VERIFIED in `results/mutbench/multi_ground_truth_summary.csv` (`0.315`, `0.188`, `1.70x`, strict near `0.108/3.43x`). DISCREPANCY/REGRESSION: row still says `Functional regions (439)` and `Positions 439`; expected `417` from prose/ch3/`1,251 nt`. | Label resolves. | Major regression. |
| P5 L76 | No numbers/cites. Claim follows prior table. | none | Verified. |
| P6 L82--83 | GISAID `2020--2021`, `342/29,903`, `1.14%`: VERIFIED by manuscript table and prior audit trail; explicit CSV source not found. | `youn2025mutclust` plausible for GISAID H-score benchmark; `tab:real_gisaid` resolves. | Minor source-path gap. |
| Table L85--110 | Real GISAID rows: table internally consistent; MutClust-Hybrid `0.305/0.077/0.123/7.28/0.766/0.383`, sliding `F1=0.420`, `7.73x`. Explicit authoritative CSV not located under `results/mutbench/`. | Label resolves. | Minor: needs source-path annotation. |
| P7 L112 | Hybrid `0.785->0.123`, sliding `0.420`, enrichment `6.9--8.0x`, OPTICS `F1=0.150`, `HS=0.369`, KDE precision `1.000`, recall `0.049`, `HS=0.557`, sweeps `30/36`, Hybrid `HS=0.778`: MutClust/Hybrid VERIFIED; external-method rows UNVERIFIED by located CSV. | `tab:external_methods`, `sec:external_comparison` labels resolve at same paragraph. | Minor source-path gap. |
| P8 L114 | `HS=0.778`, `~43x`, real `0.383` vs `0.386`, enrichment `6.9--8.0x`: VERIFIED/consistent with L25/table; CSV source partial as above. | `sec:9pathogen_results` resolves. | Verified with minor source caveat inherited. |
| P9 L123--132 | Permutations `1000/200`, `p<0.005`, `z>9.2`; BCa `1000`, `n=7`, `95% [0.323,0.635]`, `p<0.001`; combination CI `[0.047,0.202]`; omega CI `[0.201,0.346]`; rank `71.9%` of `171`; convergence `~1000`, `rho>0.997`, SD `<0.015`: omega CI VERIFIED from `results/mutbench/cluster_bootstrap_omega.csv` quantiles `0.2008/0.3455`. Other robustness values not fully source-located. | `efron1987better` OK for BCa; refs resolve later. | Verified for recent fix: omega CI no longer old `[0.195,0.333]`. Minor source-path gaps for Stage 1 robustness. |
| Figures L134--146 | Figure captions: `HS≈0.62`, `~1000`, grid `64`: plausible; source not located except figures. | figure labels resolve. | Minor source-path gap. |
| P10/Table L148--179 | H3N2 pilot `9000`, three 5-year windows, `3000` each, Koel `25`, thresholds `<5%`/`>=10%`, enrichments `3.40/3.02/2.72`, prospective `0/20`, `0/30`, `0/50`, `1/50`, p-values: VERIFIED exactly in `results/mutbench/feature_analysis/h3n2_temporal_pilot.csv`. | `tab:h3n2_temporal_pilot` resolves. | Verified. |
| P11 L181--184 | `11` pathogens, `T0`, train `>=30`, test `>=20`, 4-feature, thresholds `<5%`/`>=10%`: methodology matches `results/mutbench/feature_analysis/sliding_window_prospective_backtest_summary.csv`. | `subsec:h3n2_temporal_pilot` resolves. | Verified. |
| P12 L186 | `73` windows, `219` top-k, `k={20,30,50}`; EV-A71 `0.77/+0.146/10.8x`, Rabies `0.79/+0.112/4.1x`, Influenza B `0.70`, grand `MCC=-0.006`, AUROC `0.539`, enrichment `1.57x`, slope `-0.006` to `+0.032`, retrospective `0.341/0.454`: prospective values VERIFIED in `results/mutbench/feature_analysis/sliding_window_prospective_backtest_summary.csv`; retrospective in `results/mutbench/region_overlap_mcc.csv`. | refs/label resolve. | Verified. |
| Figure L188--193 | Caption values verified as above; image exists at `paper/dissertation/figures/sliding_window_prospective_backtest.png`. | label resolves. | Verified. |
| P13 L195--197 | 4-feature extension: coverage `0.83`; AUROCs `0.555/0.543/0.549/0.561`; Wilcoxon p/deltas; EV-A71/Rabies/HCV values: mostly VERIFIED in `results/mutbench/feature_analysis/sliding_window_prospective_backtest_4feature_summary.csv` and paired CSV. Grand means require aggregation but match direction. | label resolves. | Verified. |
| P14 L206 | No hard numbers except section refs. | `sec:9pathogen_results` resolves. | Verified. |
| P15 L208 | H3N2 `1,967`, `5` sites; HS `0.661` vs `0.577`; `543` positions; enrichment `0.87--2.36x` vs SARS `1.9--23.7x`; top-5 scoring refs: H3N2 values need old Stage 1 source; current `stage3_full_results.csv` confirms 543 HA positions and later bests. | `wiley1981structural`, `wilson1990structural` OK for antigenic sites; refs resolve. | Minor source-path gap. |
| Figure L210--215 | `11` pathogens/top 5; figure exists. | label resolves. | Verified. |
| P16 L217 | Structural `5.92-fold`, `8 Å`, `1000`, `z=13.34`: UNVERIFIED in `results/mutbench/hotspot3d_results.csv` (file contains DBSCAN rows, not this enrichment summary); only directory cited. | none | Minor: source file for exact enrichment should be named. |
| P17 L219 | Simulation `100`, `N=500`, `100%`, `rho=-0.876`, `p=1.28e-64`, AUC `1.000/0.000`; D614G retained; HS `0.661/0.577`: phylo values plausible in `results/mutbench/phylo_sensitivity_results.csv` / comparison files; D614G VERIFIED in `results/mutbench/layer_a_tags.csv` (SARS-CoV-2 614 functional tag). | `sagulenko2018treetime`, `korber2020tracking` OK; `para:full_lattice_shapley` resolves later. | Verified; recent fix: D614G retained, not excluded. |
| P18 L229--238 | Stage 2 `20`, `6`, `14`, `5`, `39`, `11`, `8580`; `10` features; lengths `261--1330`, MSA sizes `530--5019`: grid VERIFIED in `results/mutbench/stage3_full_results.csv`; length/MSA ranges consistent with ch3/results feature files. | refs to variants/scoring/mutbench/info resolve. | Verified. |
| P19 L244--250 | `8580`, `20*39*11`, six categories, 6 DMS pathogens, NCBI accessions: grid VERIFIED in `stage3_full_results.csv`; DMS availability consistent with DMS CSVs. | none | Verified. |
| P20 L256--258/Table L259--287 | Best table values VERIFIED against `results/mutbench/stage3_full_results.csv` after rounding. All 11 pathogens have distinct scoring-detector tuples at family level; only 10 unique parameter-variant tuples because Influenza B/MERS share `freq+KDE(p=85)`. REGRESSION: caption says HIV-1 operational `n_A=26` vs literature-curated `23`; expected current wording is `26` in `results/mutbench/layer_a_tags.csv`, `23` mapped/operational gp120 in `stage3_full_results.csv`/`hotspot3d_results.csv`. | `tab:gt_heterogeneity`, `sec:limitations`, `ch:discussion` resolve. | Major regression. |
| P21 L289--292 | Uniqueness probability `prod(780-i)/780≈0.932`, gap `0.265`, `omega^2=0.296`, scoring main `6.3%`: VERIFIED by formula and `stage3_statistics.csv`; LOPO gap from later LOPO table. | `subsec:9pathogen_statistical` implied later. | Verified. |
| P22 L294--296 | Worst-end grid: `8580`, worst HCV stability SWAN `w=50,k=1.0`, MCC `-0.361`, precision/recall `0`, `139`, row index `6782`; negative `4171/48.6%`, nonpositive `4695/54.7%`; worst family/scoring means: VERIFIED in `results/mutbench/stage3_full_results.csv`, except row index is 0-based `6782` / 1-based data row `6783`. | `tab:stage2_best` resolves. | Minor: clarify row-index convention. |
| Figure/P23 L298--306 | Heatmap/category statements: figure exists; best scoring categories four of six VERIFIED from `stage3_full_results.csv` best rows. | refs resolve. | Verified. |
| Table L308--330 | Biological rationales have table numbers: Norovirus AUC `0.944` and freq `0.760` need per-feature AUC source; current source not explicit in table. CoVFit citation plausible for SARS-CoV-2 PLM fitness claim. | `covfit2025` OK/plausible. | Minor: rationale table should cite/source AUC values. |

## Recent Fix Verification

| Fix item | Status |
|---|---|
| D614G retained as functional, not excluded | VERIFIED at L219 and `results/mutbench/layer_a_tags.csv`. |
| omega CI `[0.201,0.346]` | VERIFIED at L126; quantiles from `results/mutbench/cluster_bootstrap_omega.csv` are `0.2008/0.3455`. |
| HIV-1 Layer A `26` tags / `23` mapped to gp120 | REGRESSION at L261: caption reverses this. |
| Stage 1 region `417 AA`, not `439` | PARTIAL REGRESSION: prose L50 fixed to 417; table L63 still 439. |
| "single-position scoring (gap-aware)" not "point substitutions only" | No old wording found in L1--330. |

## Per-Section Severity Counts

| Section | Critical | Major | Minor | Verified |
|---|---:|---:|---:|---:|
| Opening/key results L1--17 | 0 | 0 | 1 | 1 |
| Single-pathogen benchmark L18--115 | 0 | 1 | 5 | 4 |
| Robustness/prospective L116--198 | 0 | 0 | 2 | 5 |
| Cross-pathogen/structural L199--220 | 0 | 0 | 2 | 3 |
| Large-scale benchmark L221--330 | 0 | 1 | 2 | 5 |

## Overall Severity Tally

Critical: 0. Major: 2. Minor: 12. Verified: 18. Regression count: 2.

RESULT_AUDIT_V2_J8: critical=0 major=2 minor=12 regression=2
