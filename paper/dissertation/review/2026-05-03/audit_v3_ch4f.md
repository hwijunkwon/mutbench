# Audit v3 ch4f: lines 619--742

## 1. Per-paragraph audit table

| Lines | Claims | Source check | Citations | Cross-refs | Severity |
|---|---|---|---|---|---|
| 619--621 | DMS-available group: 6 pathogens, mean best MCC 0.287, range 0.196--0.534; DMS-unavailable: 5 pathogens, mean 0.407, range 0.196--0.660; Mann--Whitney U=10, p=0.43; interpret DMS-unavailable as phylogenetic-pattern evidence. | Verified from `stage3_full_results.csv`: available mean 0.2873887, min 0.196313, max 0.534058; unavailable mean 0.4065258, min 0.196198, max 0.660155; scipy two-sided U=10, p=0.428571. | No inline citation needed; archive named. | `subsec:dms_subgroup`, `tab:dms_subgroup` labels exist. | Verified |
| 624--628 | 20 scoring formulas derive from 10 biological features across 6 categories; multiple formulas map to same feature; composites combine features. | Consistent with `ch4_results.tex` earlier lines 232/247 and feature-analysis CSV feature set. Note category naming differs slightly from earlier "MSA-derived/AI-based/composite" taxonomy, but not numerically wrong. | No citation needed. | `sec:information_analysis` and compatibility `ch:adapt` labels exist. | Verified |
| 630 | Prior sections showed scoring x pathogen omega^2=0.296; section motivates feature-level explanation. | Verified against `threeway_anova_omega.csv`/`cluster_bootstrap_omega_summary.csv` headline point 0.296252 and prior text. | No citation issue. | None. | Verified |
| 633--636 | Per-feature AUC leaders, RF CV AUC, feature correlations, leakage caveat, mechanistic link to omega^2=0.296. | Mostly verified. `per_feature_auc_v2.csv`: Norovirus homoplasy 0.9435, H3N2 pLDDT 0.787, SARS-CoV-2 ESM2 0.586, MERS ESM2 0.695, HIV-1 entropy 0.730, HCV dN/dS 0.680. RF mean/range verified: 0.74209, 0.5848--0.8988. Correlations verified: freq-entropy 0.9658, freq-dN/dS 0.8658, pLDDT-SASA -0.1858, max |homoplasy-other| 0.2328. Minor issue: "remaining pathogens cluster around homoplasy or pLDDT" is not fully true for EV-A71, whose top feature is ESM2 (0.596). | No inline literature citations required. Script/file provenance named. | Labels exist. | Minor |
| 639--667 | Leave-one-feature-out ablation table: 12-pathogen baseline 0.083, core-11 0.093, homoplasy largest contributor, ESM2/SASA removal improves. | Verified from `feature_ablation_results.csv`: baseline 0.08288; no-Zika baseline 0.09251; removal means match rounded table values. Ordering is preserved excluding Zika. "Proportionally rescaled deltas" in caption is imprecise; deltas are recomputed under core-11, not a strict scalar rescaling. | No citation issue. | `tab:feature_ablation`; `fig:feature_ablation` phantom label exists. | Minor |
| 669--702 | Nested-LOPO full-10 vs fixed 4-core means, CIs, paired delta, p=0.61, per-fold table, unchanged folds. | Verified from `feature_ablation_nested_lopo.csv` and summary: full 0.069754 CI [0.017024,0.129505], 4-core 0.080882 CI [0.007723,0.166397], delta 0.011128 CI [-0.017747,0.042390]. Per-fold rows match after rounding. p=0.6132 appears in TeX but is not in the summary CSV; still internally tabled. | No citation issue. | `tab:nested_lopo_4core` exists. | Verified |
| 704 | ESM2/SASA noise on average; ESM2 best for MERS and SASA best for Norovirus; legacy adaptive methods underperform EqualWeight; oracle ceiling 0.160; 20--30+ pathogen need. | Adaptive numbers verified from `adapt_v2_summary.csv`: kNN max 0.020, Top-3 AUC 0.049, correlation ensemble 0.043, EqualWeight 0.083, oracle 0.160. Major factual error: `per_feature_auc_v2.csv` shows Norovirus best is homoplasy 0.9435; SASA is 0.7472 and ranks sixth. ESM2 for MERS is correct. | Future-work citation is cross-ref only; acceptable. | `ch:discussion`, `sec:future_work`, `subsec:adaptive_weighting_limits` exist. | Major |
| 706--708 | Tier 1 cold-start recipe, nested-LOPO anchor, subset rank 13/210, search-space reduction to 20--80 with 7--9x enrichment, complexity/runtime, Tier 2 family priors and block-bootstrap CI [0.202,0.346]. | Nested-LOPO verified as above; subset rank verified in `subset_selection_robustness_210combos.csv` rank 13/210. Block CI verified in `block_bootstrap_omega_summary.csv`: [0.2022,0.3457]. Family priors match `tab:scoring_recommendation` labels. Minor unsupported claim: median end-to-end wall-clock below ten minutes on CPU is not backed by a CSV in the allowed result set. The 20--80 / 7--9x enrichment is deferred to later section, outside this scoped chunk; no contradiction found. | Cross-ref citations only. | All refs resolve: `para:p5_callability`, `subsubsec:equalweight_variants`, `alg:mutbench_coldstart`, `tab:cold_start_baseline_progression`, `tab:nested_lopo_4core`, `tab:subset_selection_top10`, `subsec:search_space_reduction`, `tab:scoring_recommendation`, `subsec:anova_diagnostics`, `ch:discussion`, `sec:limitations`. | Minor |
| 710--733 | Algorithm: inputs, 4 features, z-score, signs, uniform average, top-10% threshold. | Consistent with nested-LOPO protocol and `feature_ablation_nested_lopo.csv`. Minor ambiguity: KwIn says pLDDT optional, but pseudocode still loops over pLDDT without specifying fallback when no structure is available. | No citation issue. | `alg:mutbench_coldstart` exists. | Minor |
| 735--742 | Audit-ledger table shell and caption. | Only caption/label in scope; rows start after line 742, so no numerical claims audited here. | No citation issue. | `tab:audit_ledger` exists. | Verified |

## 2. Per-section severity counts

| Section | Critical | Major | Minor | Verified |
|---|---:|---:|---:|---:|
| DMS subgroup sanity check | 0 | 0 | 0 | 1 |
| Information-Type Analysis intro | 0 | 0 | 0 | 2 |
| Per-feature discriminative power | 0 | 0 | 1 | 0 |
| Feature ablation analysis | 0 | 1 | 2 | 1 |
| Cold-start algorithm | 0 | 0 | 2 | 1 |

## 3. Recent-fix verification

| Anchor | Status | Check |
|---|---|---|
| omega^2 CIs: cluster [0.201,0.346], phylo-block [0.202,0.346], wild-cluster [0.201,0.303] | PRESENT | Scope includes phylo-block [0.202,0.346] at line 708. Cluster and wild values verified in `cluster_bootstrap_omega_summary.csv`/`wild_cluster_bootstrap_omega_summary.csv`; no scoped regression. |
| HIV-1 Layer A n=23 gp120 MCC vs n=26 tags | PRESENT | `feature_matrix_HIV-1.csv` has `layer_a` sum 23; `layer_a_tags.csv` has 26 HIV-1 rows. Not stated in scoped lines, but no contradiction. |
| D614G retained in Layer A per Korber 2020 | PRESENT | Ch4 lines 219/335 retain D614G with `korber2020tracking`; `references.bib` entry exists. No scoped regression. |
| Stage 1 functional regions 417 AA, not 439 | PRESENT | Ch4 lines 50/63 use 417 AA. No scoped regression. |
| Single-position scoring is gap-aware, not point substitutions only | PRESENT | Ch3 line 37 scopes single-position coding-region vectors; ch3 lines 513/516 and ch4 line 628 include indel/gap-aware frequency/entropy variants. No scoped regression. |
| P1 null at-or-below-mean: 6/12 iid/circular, 4/12 protein-block, 7/12 local-burden | PRESENT | Recomputed from `codex_wave1/p1_null_per_pathogen.csv` for 4-core MCC; no scoped regression. |
| Decision curve budget 50 random baseline = 41 expected TPs | PRESENT | `codex_wave1/p2_decision_curve.csv` sums to random=41 at budget 50. No scoped regression. |

## 4. Compression candidates

| Lines | Candidate | Reduction |
|---|---|---:|
| 636 | Split or compress the long feature-AUC/RF/correlation paragraph by moving per-pathogen AUC examples into a compact table note and retaining only leaders plus RF/correlation summary in prose. | 90+ words |
| 642--646 | Merge sentence and caption overlap: table caption already explains delta direction and baseline. | 25--35 words |
| 669 | Remove repeated nested-LOPO details already in Table caption; retain means, CI, p, and interpretation. | 35--45 words |
| 704 | Compress legacy adaptive-weighting sentence after fixing Norovirus/SASA error; table/source carries exact strategy names. | 25--35 words |
| 708 | Split Tier 1/Tier 2 into shorter paragraphs and move complexity/runtime to algorithm caption or methods note. | 120+ words |

## 5. Overall tally

Critical: 0; Major: 1; Minor: 5; Verified rows: 6; Regressions: 0.

RESULT_AUDIT_V3_ch4f: critical=0 major=1 minor=5 regression=0
