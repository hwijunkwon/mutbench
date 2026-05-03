# Deep Audit Job 3 — Chapter 3 Methods

Scope: `paper/dissertation/chapters_en/ch3_methods.tex` lines 1-892. Read-only audit against manuscript, `results/mutbench/*`, `results/mutbench/feature_analysis/feature_matrix_*.csv`, and `data/cross_pathogen/*_position_scores.csv`. Web spot-checks used for current DMS citations: [Dadonaite 2024 Nature](https://www.nature.com/articles/s41586-024-07636-1), [Aditham 2025 Cell Host & Microbe/PubMed](https://pubmed.ncbi.nlm.nih.gov/40398416/), [Bakhache 2025 Nature Microbiology](https://www.nature.com/articles/s41564-024-01871-y), and [Simonich 2026 bioRxiv/PMC](https://pmc.ncbi.nlm.nih.gov/articles/PMC12918976/).

## Executive Findings

- **Critical:** D614G is included in the curated Layer A source table (`results/mutbench/layer_a_tags.csv`, SARS-CoV-2 position 614) but Chapter 4 explicitly says D614G is excluded from Layers A and B because it is a founder effect. This is a direct ground-truth contradiction.
- **Major:** DMS Layer C counts in Chapter 3 Table `tab:gt_positions` do not match `results/mutbench/layer_c_evaluation.csv` for SARS-CoV-2, H3N2, and HIV-1.
- **Major:** HIV-1 Layer A count has three incompatible operational values: 23 in Chapter 3 Table `tab:gt_positions`, 26 in `layer_a_tags.csv`/`gt_heterogeneity_analysis.csv`, and 23 in `feature_matrix_HIV-1.csv`/`layer_c_evaluation.csv`.
- **Major:** Stage 1 functional-region count is internally inconsistent: Chapter 3 defines 1,251 nt = 417 AA, while Chapter 4 describes 439 AA functional regions.
- **Verified:** The headline Stage 2 grid is correct: `20 scoring × 39 detector variants × 11 pathogens = 8,580` rows in `results/mutbench/stage3_full_results.csv`; 20 scoring labels, 39 detector labels, 14 families, 11 pathogens.

### Chunk 1 (lines 1-150)

#### Numerical Claims
- 11 RNA viruses / 20 scoring / 14 detection families / 39 variants: **VERIFIED** in `stage3_full_results.csv` (`pathogen=11`, `scoring=20`, `detector=39`, `family=14`).
- Table `tab:pathogen_data` sequence counts, unique counts, query dates, and MAFFT modes: **VERIFIED** against `results/mutbench/provenance/genbank_queries.csv`.
- Surface proteins and lengths in Table 3.1 area: **MOSTLY VERIFIED** against feature matrices: SARS-CoV-2 1259, H3N2 543, Norovirus 536, HIV-1 450, Dengue 490, RSV 550, Influenza B 560, MERS 1330, HCV 340, Rabies 491, EV-A71 261. Feature matrices match these lengths.
- Zika exclusion: **PARTLY VERIFIED / DISCREPANCY**. Chapter says Zika is excluded from Stage 2 and included in supplementary 12-pathogen feature analysis. Internal data confirm `feature_matrix_Zika.csv` exists, but its length is 452 rows, while line 863 later says Zika E protein is 505 AA and Table `tab:tranception_esm_correlation` uses N=451.

#### Citations
- `fu2012cdhit`, `steinegger2017mmseqs2`, `eddy2011hmmer`, `katoh2013mafft`: support deduplication/alignment tooling claims / OK.
- Biological claims such as substitution rates and epochal evolution are mostly uncited in this chunk. Not necessarily false, but they should be treated as narrative background rather than audited quantitative claims.

#### Cross-refs
- All `\ref`/`\eqref` labels in Chapter 3 resolve somewhere in the chapter set; no missing labels found.

#### Logical Consistency
- `\label{sec:9pathogen_benchmark}` and `\label{subsec:9pathogen_data}` are outdated names for an 11-pathogen benchmark. **Minor**.

#### Outdated Content
- Label names retain “9pathogen”; text is updated to 11 pathogens. **Minor**.

#### Severity
- 0 Critical / 1 Major / 2 Minor.

### Chunk 2 (lines 151-300)

#### Numerical Claims
- `20 × 39 = 780` and `20 × 14 × 11 = 3,080`: **VERIFIED** by arithmetic and factor counts in `stage3_full_results.csv`.
- Layer B dN/dS `<0.5`, Layer C top 20%, freeze date 2024-08-12: **UNVERIFIED**. I found no lab-notebook/SOP file in the checked paths; the CSV bundle confirms outputs, not preregistration timing.
- DMS availability for six pathogens: **VERIFIED** in `layer_c_evaluation.csv`: SARS-CoV-2, H3N2, HIV-1, RSV, Rabies, EV-A71.

#### Citations
- `carabelli2023convergent`, `cao2023ba286`: plausibly support SARS-CoV-2 convergent/escape site curation.
- `wrapp2020cryo`: supports Spike structural domains / OK.
- `yang2007paml`: supports dN/dS interpretation broadly / OK, but it does not itself justify the dissertation-specific Layer B threshold.
- DMS citations: Dadonaite 2024, Aditham 2025, Bakhache 2025, and Simonich 2026 were spot-checked externally and plausibly support DMS/fitness or entry/antibody phenotype claims. Simonich 2026 is a preprint, not peer reviewed.

#### Cross-refs
- `subsec:3layer_gt`, `tab:gt_positions`, and related refs resolve.

#### Logical Consistency
- Layer definitions are consistent with Chapter 4 at the metric level: Layer A for MCC, Layer B constrained FPR, Layer C DMS F1.
- However, the chapter’s “all thresholds frozen before Stage 1” claim is hard to reconcile with later text saying Rabies/EV-A71 DMS releases became available later in the cycle. **Major unless SOP proves the future-data rule was frozen without the datasets.**

#### Outdated Content
- None material.

#### Severity
- 0 Critical / 1 Major / 0 Minor.

### Chunk 3 (lines 301-450)

#### Numerical Claims
- Layer A counts in Table `tab:gt_positions`: **DISCREPANCY**.
  - Chapter table, 11 pathogens: SARS 25, H3N2 25, Noro 15, HIV-1 23, Dengue 24, RSV 20, Flu B 17, MERS 9, HCV 54, Rabies 39, EV-A71 27 = **278**.
  - `layer_a_tags.csv`: same plus Zika, but HIV-1=26 and total **308** across 12 pathogens; excluding Zika = **281**.
  - `feature_matrix_HIV-1.csv` has `layer_a` sum **23**, while `gt_heterogeneity_analysis.csv` has HIV-1 **26**.
- Layer C counts in Table `tab:gt_positions`: **DISCREPANCY** against `layer_c_evaluation.csv`.
  - SARS-CoV-2: chapter 252 vs CSV 247.
  - H3N2: chapter 102 vs CSV 112.
  - HIV-1: chapter 100 vs CSV 48.
  - RSV 101, Rabies 87, EV-A71 55 match.
- DMS Layer C availability for six pathogens: **VERIFIED**.

#### Citations
- `koel2013substitutions`, `lindesmith2012/2013`, `moore2015williamson`, `twiddy2002dengue`, `holmes2003dengue`, `mas2018rsv`, `sullender2000rsv`, `ni2013influenzab`, `wang2008influenzab`, `kim2016mers`, `tang2014mers`, `benmansour1991rabies`, `huang2015eva71`: broadly plausible for pathogen-specific Layer A curation; not all support exact coordinate mappings without the curated extraction table.

#### Cross-refs
- `fig:gt_distribution`, `tab:dms_preprocessing`, and `tab:gt_positions` resolve.

#### Logical Consistency
- **Critical:** `layer_a_tags.csv` includes SARS-CoV-2 position 614 as Layer A (“D614G increases infectivity and spike stability”), but Chapter 4 line 219 says “D614G is accordingly excluded from Layers A and B.” This undermines the ground-truth contract.
- HCV Layer B = 0 is explained clearly and is consistent within Chapter 3.

#### Outdated Content
- Table footnote says HIV-1 23 is canonical and 26 operational, but the operational feature matrix checked for HIV-1 still sums to 23. **Major**.

#### Severity
- 1 Critical / 3 Major / 0 Minor.

### Chunk 4 (lines 451-600)

#### Numerical Claims
- SARS-CoV-2 Spike gene start `g_start=21,563`, genome length 29,903, synthetic seed positions 484/501/417/452, 100 random 80% subsamplings, seeds 42-141: **PLAUSIBLE / partially source-backed**; no direct CSV checked for the synthetic run in this pass.
- Functional-region table: nucleotide counts sum correctly to 1,254 with 3 nt overlap = 1,251 nt. **VERIFIED by arithmetic**.
- Functional-region AA equivalent: **DISCREPANCY with Chapter 4**. 1,251 nt corresponds to 417 codons/AA, but Chapter 4 line 50 states “functional regions (439 AA, 34.5% of Spike).”
- MutClust variants = five: **CONSISTENT** with Chapter 4 Stage 1 tables.
- MutClust-Hybrid hotspot-score 0.778: **CONSISTENT** with Chapter 4 Table `tab:hotspot_scores`.
- Gamma sensitivity `±0.01` archived in `gamma_sensitivity.csv`: **UNVERIFIED**; no such file found under `results/mutbench` in this pass.

#### Citations
- `dadonaite2023dms`, `dadonaite2024nature`: external spot-check supports full-spike pseudovirus DMS, cell entry, ACE2 binding, and serum escape.
- `wrapp2020cryo`, `mccallum2021ntd`: plausible support for Spike domain and NTD supersite annotation.
- `youn2025mutclust`: citation exists in BibTeX; not externally verified here.

#### Cross-refs
- Equations `eq:coordinate_transform`, `eq:mutbench_hscore`, `eq:shannon_entropy`, `eq:hotspot_score` resolve.

#### Logical Consistency
- Stage 1 uses functional/DMS/synthetic ground truths, while Stage 2 uses Layer A MCC. This distinction is mostly clear, but the manuscript also references convergent-evolution ground truth in Chapter 4 line 50 as 97 positions, while Chapter 3’s Stage 2 SARS Layer A is 25. The distinction should be made explicit near Stage 1 to prevent the appearance of conflicting SARS-CoV-2 positives. **Major**.

#### Outdated Content
- None material.

#### Severity
- 0 Critical / 2 Major / 0 Minor.

### Chunk 5 (lines 601-750)

#### Numerical Claims
- `20 × 39 × 11 = 8,580`: **VERIFIED** exactly in `stage3_full_results.csv`.
- 20 scoring types, six categories: **VERIFIED** against `stage3_full_results.csv` scoring labels.
- 14 detection families and 39 variants: **VERIFIED** against `stage3_full_results.csv`; family/variant counts match table.
- Detection categories: **MINOR TERMINOLOGY DRIFT**. Early text says five categories including “adaptive window”; table uses Threshold-based, Signal processing, Density and clustering, Statistical/model-based, Legacy. `AdaptWin` is classified as Threshold-based in the table, not a separate adaptive-window category.
- Table `tab:tranception_esm_correlation`: **PARTLY DISCREPANT** with feature-matrix lengths for Rabies and EV-A71. Table N gives Rabies 490 and EV-A71 260, but feature matrices have 491 and 261 rows.
- Stage 2 design characteristics: **VERIFIED** for unique seqs and AA lengths against `genbank_queries.csv` and feature matrices. Positive-rate calculations align with the stated operational counts except the HIV-1 operational/source split noted above.

#### Citations
- `minh2020iqtree`, `murrell2013fubar`, `grantham1974amino`, `evans2021af2multimer`, `vankempen2024foldseek`, `lin2023esm2`, `notin2022tranception`, `thadani2023evescape`: plausible for method/tool context.
- Important caveat is well disclosed: “Tranception” is an ESM-2 pseudo-perplexity proxy, not the original model.

#### Cross-refs
- `tab:scoring_types`, `tab:structure_sources`, `tab:detection_families`, and `tab:design_characteristics` resolve.

#### Logical Consistency
- The ANOVA family-vs-variant rationale is consistent with Chapter 4: variants remain rows; family is the modeled detector factor.

#### Outdated Content
- “39 methods” sometimes means “39 detector parameter variants,” not independent method families. The chapter often clarifies this, but figure text and prose could be tightened. **Minor**.

#### Severity
- 0 Critical / 0 Major / 3 Minor.

### Chunk 6 (lines 751-892)

#### Numerical Claims
- ANOVA factors: 20 scoring, 14 family, 11 pathogen; 8,580 rows; residual df 7,970: **VERIFIED** in `stage3_statistics.csv`.
- Headline `omega^2_scoring×pathogen = 0.296`: **VERIFIED** (`0.296252`) in `stage3_statistics.csv`.
- Cell-level ANCOVA values: **MOSTLY VERIFIED** in `ancova_omega_summary.csv`; chapter line 770 says interaction rises to 0.274, matching CSV 0.274124. Chapter 5 later says 0.264, which is outside this chapter but is a cross-chapter drift. **Minor here / Major if auditing Chapter 5.**
- Bayesian 0.319, HDI [0.246, 0.396], P>0.14=0.9998: **VERIFIED** in `bayesian_omega_summary.csv`.
- 5-frame robustness diagnostics: **VERIFIED** in `omega_robustness_5way.csv`: standard cluster, wild cluster, phylogenetic block, mixed effects, Bayesian factor analysis. Chapter text says “four complementary frames” plus standard cluster, so the “5-way” reference is accurate.
- 19 cross-pathogen position-score files: **VERIFIED** in `data/cross_pathogen/*_position_scores.csv`.

#### Citations
- `chicco2020mcc`, `cohen1988statistical`, `wobbrock2011aligned`, `demsar2006statistical`, `cameron2008bootstrap`, `mantel1967nonparametric`: plausible support for metric/statistical-method claims.
- License/current benchmark citations (`gurev2026everest_v3`, `notin2025proteingym_v13`, `virogym2026`) were not fully externally audited; given current-date sensitivity, these should be rechecked before final submission.

#### Cross-refs
- All statistical cross-refs resolve, including `subsec:anova_diagnostics`, `tab:omega_robustness_5way`, and `subsec:stage3_methods`.

#### Logical Consistency
- The fixed-effect ANOVA rationale is defensible and explicitly bounded: detector variants are residual, family/pathogen/scoring are fixed factors, and inference is interpreted through cluster-aware checks.
- The “BCa bootstrap” paragraph says 10,000 resamples, but Chapter 4 line 126 says the combination-level BCa CI used 1,000 resamples. These may refer to different intervals, but the wording should explicitly separate them. **Minor**.

#### Outdated Content
- `9pathogen` label names persist in method labels (`subsec:9pathogen_metrics`, `subsec:9pathogen_statistics`, etc.). Cosmetic but stale. **Minor**.

#### Severity
- 0 Critical / 0 Major / 3 Minor.

## Specific Item Verdicts

- 11 pathogens × surface glycoproteins × subtypes/lengths: **VERIFIED for core 11 lengths**; **Zika Stage 3 length inconsistent** (505 vs 452/451).
- 8,580 evaluation grid: **VERIFIED**.
- 14 detection families × 39 variants: **VERIFIED**.
- Layer A/B/C definitions consistent with Chapter 4: **PARTLY**, but D614G contradiction is **critical**.
- Layer A counts: **DISCREPANCY**. `layer_a_tags.csv` confirms the requested 12-pathogen total is **308**, not 309; core 11 excluding Zika is **281** using HIV-1=26, while Chapter 3 Table uses **278** with HIV-1=23.
- DMS Layer C availability: **VERIFIED** for six pathogens.
- Stage 1 SARS-CoV-2 specific numbers: **PARTLY VERIFIED**, but functional-region AA count and 25-vs-97 convergent-positive distinction need correction/clarification.
- ANOVA fixed-effect design rationale: **VERIFIED/defensible**, with appropriate caveats.
- 5-frame robustness diagnostics references: **VERIFIED** in `omega_robustness_5way.csv`.

RESULT_DEEP_J3: critical=1 major=8 minor=8
