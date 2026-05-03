# Deep Audit Job 4: Chapter 4 Results

Scope: `paper/dissertation/chapters_en/ch4_results.tex` lines 1-989. Read-only audit of manuscript and source CSVs. Web search was not needed; suspicious numerical claims were checked against internal CSVs.

## Findings

### Major

1. **Stage 2 uniqueness headline contradicts its own table note.** Lines 12, 257, and 611 state that all 11 pathogens have unique best combinations / no two pathogens share the same best combination. But Table 4 Stage 2 note at line 285 says Influenza B and MERS share both `freq` and `KDE(p=85)`, and `stage3_full_results.csv` confirms both rows are exactly `freq + KDE(p=85)`. Therefore only 10/11 best scoring-detector-variant tuples are unique, not 11/11. This affects a headline claim, even though the chapter correctly says uniqueness itself is null-consistent.

2. **Cluster-bootstrap CI reported as `[0.195, 0.333]` does not match the authoritative summary CSV.** Lines 126, 393, 397, 490, 516, and 610 use `[0.195, 0.333]` for the 11-pathogen cluster-bootstrap CI. `results/mutbench/cluster_bootstrap_omega_summary.csv` reports `ci_lo=0.2008358030`, `ci_hi=0.3455024399` for `11pathogen_cluster_bootstrap_evaluation_level`; `wild_cluster_bootstrap_omega_summary.csv` and `omega_robustness_5way.csv` also report standard cluster `[0.2008, 0.3455]`. The `[0.195, 0.333]` value appears only as `body_target`, not as the computed interval.

3. **P1 null-calibration explanatory sentence has wrong count and overgeneralizes across nulls.** Line 841 says “5/12 pathogens have observed MCC at or below the null mean” and lists six pathogens. Deriving from `codex_wave1/p1_null_per_pathogen.csv` for 4-core MCC gives 6/12 at-or-below for iid and circular shift, 4/12 for protein-block shuffle, and 7/12 for local-burden preserving. The adjacent significance counts are correct (5/12 iid falling to 1/12 strict), but the explanatory reason is numerically wrong.

### Minor

1. **Opening Stage 1 baseline count is inconsistent.** Line 6 says “five MutClust variants and two baselines,” while line 25 and Table `tab:hotspot_scores` describe three baselines if HDBSCAN-Auto is counted with frequency and sliding-window baselines. Clarify whether HDBSCAN-Auto is a MutClust-family comparator or a baseline.

2. **Duplicate information-type sentence.** Lines 233-234 repeat the same statement about the 10-feature information-type analysis across 11 pathogens.

3. **HBFWS paragraph mixes 12-fold protocol with `n=11` phrasing.** Lines 859-861 describe a 12-pathogen nested LOPO, then say the hypothesis was rejected at `n=11` pathogens. The CSV `hbfws_lopo_results.csv` has 12 folds. If `n=11` refers to core reference pathogens excluding Zika, state that explicitly.

4. **Vaccine table caption says “top scoring type” but rows are selected representative anchors, not global maxima.** In `vaccine_escape_stage3.csv`, HIV-1’s displayed `freq + Wavelet(t=1.5)` row is verified as the intended 7.19x anchor, but it is not the global max enrichment nor min-p row. The table body is defensible, but the caption at line 950 should say “selected anchor row / best reported scoring type” rather than “top scoring type” if global optimality is not intended.

## Chunk Audit

### Chunk 1 (lines 1-130)

Numerical claims: Synthetic MutClust-Hybrid `precision=0.968`, `recall=0.659`, `F1=0.785`, `HS=0.778` verified against `results/mutbench/method_comparison.csv`. Multi-ground-truth values verified against `results/mutbench/multi_ground_truth_summary.csv` for TC-freq-v2 functional F1 0.474, Saturated H-score DMS F1 0.315, CH-score convergent F1 0.188/enrichment 1.70, and TC-freq-v3 strict F1 0.108/enrichment 3.43. Real GISAID rows were located by text search but should be explicitly source-pathed in the manuscript.

Citations: `dadonaite2023dms`, `cao2023ba286`, `carabelli2023convergent`, `youn2025mutclust`, `efron1987better` plausibly support the DMS, convergent-evolution, MutClust/GISAID, and BCa bootstrap claims.

Cross-refs: all refs resolved globally. Logical/outdated: minor baseline-count inconsistency at line 6.

Severity: 0 critical / 0 major / 1 minor.

### Chunk 2 (lines 131-260)

Numerical claims: H3N2 temporal pilot table verified exactly against `results/mutbench/feature_analysis/h3n2_temporal_pilot.csv` (3.40/3.02/2.72x retrospective; all 2016-2020 prospective overlaps 0; 2021-2025 Top-50 overlap 1, enrichment 1.62, p 0.4785). Sliding-window summary verified against `sliding_window_prospective_backtest_summary.csv`: 73 windows, EV-A71 MCC 0.146/AUROC 0.773/enrichment 10.785, Rabies MCC 0.112/AUROC 0.789/enrichment 4.101, grand AUROC 0.539 from per-window summaries. H3N2 structural/phylo numerical claims have plausible internal sources (`hotspot3d_results.csv`, `phylo_sensitivity_results.csv`, `phylo_real_sensitivity_comparison.csv`) but the manuscript only gives a directory for structural data.

Citations: `wiley1981structural`, `wilson1990structural`, `sagulenko2018treetime`, `korber2020tracking` plausibly support H3N2 antigenic sites, TreeTime, and D614G/founder-effect context.

Cross-refs: resolved. Logical/outdated: none beyond source-path specificity.

Severity: 0 critical / 0 major / 0 minor.

### Chunk 3 (lines 261-380)

Numerical claims: Stage 2 best table verified against `results/mutbench/stage3_full_results.csv` for all 11 per-pathogen best rows and MCCs. Worst-end disclosure verified: 8,580 rows; HCV `stability + SWAN(w=50,k=1.0)` MCC -0.361346, 4,171 negative MCC rows, 4,695 nonpositive rows. ANOVA table values verified against `results/mutbench/stage3_statistics.csv`: scoring x pathogen 0.296251984, pathogen 0.117328792, family x pathogen 0.081503745, scoring 0.063008596, scoring x family 0.038796560, family 0.012622864.

Citations: `covfit2025`, `cohen1988statistical` plausibly support CoVFit contextual statement and Cohen thresholds.

Cross-refs: resolved. Logical/outdated: major uniqueness contradiction at lines 257/285.

Severity: 0 critical / 1 major / 0 minor.

### Chunk 4 (lines 381-500)

Numerical claims: Friedman `chi^2=7.6879666`, `p=0.9895445`; LOPO match 0/11, generalized MCC 0.0315, gap 0.2654; all verified in `stage3_statistics.csv`. Cell-level omega 0.234 verified by `ancova_omega_summary.csv` baseline `C(scoring):C(pathogen)=0.232509` rounded. Counterfactual null verified in `cycle4_counterfactual_null.csv`: observed 0.2892, null upper 0.00497/0.00463, p 0.004975. Standard/wild/block/Bayesian robustness values verified in `omega_robustness_5way.csv`. Discrepancy: cluster CI `[0.195,0.333]` should not be treated as computed from current CSV.

Citations: `cohen1988statistical`, `lin2023esm2` OK for thresholds and ESM-2.

Cross-refs: resolved. Logical/outdated: “three complementary analyses” is tempered later and acceptable.

Severity: 0 critical / 1 major / 0 minor.

### Chunk 5 (lines 501-630)

Numerical claims: LOO omega values verified against `omega_loo_pathogen_sensitivity.csv` / table values. Precision@k best rows verified against `stage3_full_results.csv`. DMS Layer A vs C statistics verified in `stage3_statistics.csv` for listed Spearman correlations where present; EV-A71 LayerAvsC is not in `stage3_statistics.csv` output shown and should remain source-pathed to `layer_c_evaluation.csv`. DMS subgroup means 0.287 and 0.407 match the best-MCC table arithmetic.

Citations: DMS citations (`dadonaite2024nature`, `lee2018h3n2dms`, `haddox2018hiv1dms`, `simonich2026rsvdms`, `aditham2025rabies`, `bakhache2025eva71`) plausibly support DMS source claims.

Cross-refs: resolved. Logical/outdated: none.

Severity: 0 critical / 0 major / 0 minor.

### Chunk 6 (lines 631-770)

Numerical claims: Nested-LOPO summary verified against `feature_ablation_nested_lopo_summary.csv`: full 10-feature mean 0.069754, 4-core 0.080882, delta 0.011128, CI bounds as reported. Audit ledger P3 values verified against `codex_wave1/p3_full_lattice_1023.csv` and `p3_shapley.csv`: 4-core rank 87/1023, 3-core rank 27/1023, pLDDT Shapley -0.001501, ESM-2 -0.014383. P5 0/12 callable verified against `codex_wave2/p5_callable_decisions.csv` (24 method-fold rows, 0 callable). P6 counts verified against `codex_wave3/p6_null_summary.csv`.

Citations: none in this chunk beyond cross-refs.

Cross-refs: resolved. Logical/outdated: duplicate information-type sentence earlier; no issue in this chunk.

Severity: 0 critical / 0 major / 1 minor.

### Chunk 7 (lines 771-870)

Numerical claims: Cold-start baseline progression and 210-subset claims verified against `feature_ablation_nested_lopo.csv` and `subset_selection_robustness_210combos.csv` where named; 4-core rank 13/210 and MCC 0.0809 match. Full-lattice and Shapley claims verified as above. P1 significance counts derived from `p1_null_per_pathogen.csv`: 4-core iid 5/12, circular 3/12, block 2/12, local-burden 1/12 Norovirus only. P5 and P6 claims verified. Wave 4 summary verified against `codex_wave4/w4_labeled_lopo_summary.csv`: mean MCC 0.076798, 8/12 positive, p 0.3677, D1 pass 0.

Citations: none.

Cross-refs: resolved. Logical/outdated: P1 explanatory sentence count is wrong.

Severity: 0 critical / 1 major / 0 minor.

### Chunk 8 (lines 871-989)

Numerical claims: Cycle 7B method means verified against `adaptive_weighting_comparison.csv`: EQ4 0.07794, EQ10 0.08344, XGB 0.01626, RF 0.01873, LR 0.05605, 1-NN 0.06627, HBFWS-phylo 0.06308, rank aggregation 0.06248. HBFWS verified against `hbfws_lopo_results.csv`: HBFWS 0.05830, EQ4 0.07794, delta -0.01964. Wave 5 verified against `codex_layerA_prime/lopo_summary.csv`: mean -0.05549, sd 0.06783, 2/10 positive, precision@20 0.005. Vaccine escape exact anchor rows verified in `vaccine_escape_stage3.csv`: HIV-1 `freq + Wavelet(t=1.5)` enrichment 7.1875, p 3.16e-19, Bonferroni p 2.47e-16; H3N2 `fubar_bf + Wavelet(t=2.0)` 9.3621; SARS-CoV-2 `fubar_pos_sel + FreqThresh(p=85)` 7.6303, p 0.0264. HIV novel-only range was not directly present in this CSV schema, so the manuscript should retain or expose its derived source.

Citations: none in this chunk. Cross-refs: resolved. Logical/outdated: vaccine caption wording is mildly ambiguous.

Severity: 0 critical / 0 major / 2 minor.

## Summary

The main quantitative backbone is mostly reproducible from the cited CSVs: Stage 3 ANOVA/Friedman/LOPO, 4-core nested LOPO, full-lattice/Shapley, P5, P6, Wave 4, Wave 5, HBFWS, Cycle 7B, and the HIV-1 vaccine-escape anchor all check out. The main issues are not hidden arithmetic failures but manuscript-level inconsistencies: the overstated 11/11 uniqueness claim, the stale cluster-bootstrap interval, and a wrong P1 explanatory count.

RESULT_DEEP_J4: critical=0 major=3 minor=4
