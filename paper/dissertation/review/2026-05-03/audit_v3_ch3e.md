# Audit v3 ch3e: ch3_methods.tex lines 509-635

Scope audited read-only against requested CSVs, `references.bib`, and cross-chapter labels. Report file is the only write.

## 1. Per-paragraph audit table

| Lines | Claims | Source check | Citations | Cross-refs | Severity |
|---|---|---|---|---|---|
| 509-539 | Scoring taxonomy totals: 3 frequency, 3 MSA-derived, 4 phylogenetic, 3 structural, 5 AI, 2 composite = 20 channels. | `stage3_full_results.csv` has 8,580 rows, 20 scoring labels, 39 rows per pathogen/scoring, 11 pathogens. Channel names align with CSV (`freq`, `rare_freq`, `freq_with_indel`, `entropy`, `entropy_with_indel`, `homoplasy`, `dnds_proxy`, `fubar`, `fubar_pos_sel`, `fubar_bf`, `plddt_inv`, `sasa`, `grantham`, `esm2_llr`, `tranception`, `semantic_change`, `stability`, `stability_structural`, `EVEscape_composite`, `EqualWeight`). `plddt inverse` description says `$1-\text{pLDDT}$`, but implementation uses `plddt_max - plddt` before min-max normalization (`scripts/run_stage3_full_detectors.py:166-187`), with pLDDT on 0-100 scale. | None needed in table. | None. | Minor |
| 541-542 | Frequency scores reflect MSA mutation frequency, rare variants, indel-inclusive counts; susceptible to sampling/alignment artifacts. | Supported by scoring labels and feature files (`*_freq_with_indel.csv` plus Stage 2 scoring grid). Qualitative caveat reasonable. | None. | None. | Verified |
| 544-545 | Entropy and homoplasy definitions; IQ-TREE 2, ModelFinder, 1,000 ultrafast bootstraps; Fitch parsimony origins per amino-acid substitution. | Feature files include homoplasy and entropy-derived channels; tool/version statement is consistent with methods text elsewhere and `tool_versions` references. “Amino acid substitution” does not regress single-position/gap-aware scope; it is not “point substitutions only.” | `minh2020iqtree` present in `references.bib`. | None. | Verified |
| 547-549 | dN/dS proxy uses Nei-Gojobori; FUBAR scores use HyPhy MG94xREV, threshold 0.9. | Requested CSVs contain per-pathogen `*_dnds.csv`, `*_fubar.csv`, `*_fubar_pos_sel.csv`, `*_fubar_bf.csv`; labels match the described channels. HyPhy v2.5/MG94xREV not directly encoded in CSV headers, but consistent with methods/provenance. | `murrell2013fubar` present. | None. | Verified |
| 551-552 | Structural sources: SARS-CoV-2 AlphaFold DB for pLDDT and SASA; all other pathogens ESMFold; AlphaFold-Multimer/Foldseek/DALI not used; SASA Shrake-Rupley release; PDB 6VSB only direct anchor. | **Mismatch.** `structural_features/plddt_summary.csv` reports SARS-CoV-2 `AlphaFold_DB`, but also Norovirus `AlphaFold_DB`; H3N2, HIV-1, Dengue, HCV, RSV, MERS, Influenza_B are `ESMFold_API`. `structural_features/sasa_summary.csv` reports SARS-CoV-2 and all listed pathogens as `ESMFold`, not AlphaFold DB. Therefore the combined “pLDDT and SASA” source sentence is wrong for SASA and omits Norovirus AlphaFold pLDDT. The “not Multimer / not Foldseek-DALI” caveats are supported by text/source search. | `grantham1974amino`, `evans2021af2multimer`, `vankempen2024foldseek`, `wrapp2020cryo` present. | `tab:structure_sources`, `ch:discussion`, `sec:plm_data_limitations` exist. | Major |
| 554-581 | Table `structure_sources`: SARS-CoV-2 AlphaFold DB for pLDDT/SASA; all other pathogens ESMFold; 3D contact only SARS-CoV-2 PDB 6VSB; Zika Stage 3 only. | **Same mismatch as lines 551-552.** Table is inaccurate for pLDDT source because Norovirus is AlphaFold DB in `plddt_summary.csv`, and inaccurate for SASA source because `sasa_summary.csv` lists SARS-CoV-2 SASA as ESMFold. Table also includes Rabies, EV-A71, Zika rows not present in the displayed pLDDT/SASA summaries, though per-feature matrices exist for those pathogens; source traceability for those table cells is incomplete in the summary CSVs. Stage 3 Zika-only statement is consistent with Stage 2 11-pathogen `stage3_full_results.csv` excluding Zika and feature-analysis files including Zika. | `wrapp2020cryo` present. | `ch:results`, `sec:structure_analysis`, `subsec:stage3_methods` exist. | Major |
| 583-586 | ESM-2 LLR is masked-marginal pseudo-LL / surprise; Tranception is ESM-2 pseudo-perplexity proxy; 11/12 high correlations; HIV-1 exception; headline omega2 0.296 retained and merged-channel sensitivity deferred. | Correlation CSV matches table values and HIV exception. `stage3_full_results.csv` and `cluster_bootstrap_omega_summary.csv` support headline omega2 0.296. Wording “all p < 1e-50 except Zika” is wrong/ambiguous: Zika also has Pearson p `4.46e-54` and Spearman p `3.98e-71`; the excluded case is HIV-1 Pearson p `0.361`. `random_seed=42` is not encoded in the two correlation CSVs and no seed string appears in the measurement script, so this is not independently traceable from the requested sources. | `notin2022tranception` present. | `tab:tranception_esm_correlation`, `sec:esm2_leakage`, `ch:discussion` exist. | Minor |
| 588-616 | Correlation table N/rho/p values; per-pathogen CSV confirms three-decimal table values and overlap/status columns. | Verified against both `tranception_esm_correlation.csv` and `tranception_esm_correlation_per_pathogen.csv`: N, Pearson, Spearman, and p-value inequalities all match rounded table values. Per-pathogen file includes `n_positions`, `sample_overlap`, p-values, `status`. | None beyond caption. | `subsubsec:tranception_separation`, `tab:tranception_esm_correlation`, `sec:esm2_leakage` exist. | Verified |
| 617-620 | Stability proxy is negative mean BLOSUM62 weighted by mutation frequency; structural variant multiplies by pLDDT/100; FoldX/RoseTTAFold not run; ESM-2 checkpoint has 33 layers/650M params. | `scripts/compute_stability.py` comments and stability CSVs support BLOSUM/pLDDT proxy framing. ESM-2 checkpoint string appears in methods and is standard for `esm2_t33_650M_UR50D`; no contradiction in CSVs. | None. | None. | Verified |
| 622-625 | EVEscape-style composite multiplies min-max ESM-2, SASA, Grantham; EVE not trained. | `scripts/run_stage3_full_detectors.py:174-178` exactly multiplies normalized `esm2_llr`, `sasa`, `grantham`. | `thadani2023evescape` present. | None. | Verified |
| 627-632 | EqualWeight has production label-free min-max variant and nested-LOPO sign-fit variant; production contributes 8,580 grid and omega2 0.296; nested full10 mean 0.070 vs production/in-sample 0.083; no LOPO claim for headline EqualWeight. | Production implementation verified at `run_stage3_full_detectors.py:180-187`: 10 predefined features, min-max, uniform mean, no label sign fit/z-score. Nested sign-fit verified at `feature_ablation_nested_lopo.py` (`fit_signs`, held-out z-score). `feature_ablation_nested_lopo_summary.csv` gives full10 LOPO mean `0.069754` and fixed4 `0.080882`; 0.083 in-sample production value is referenced in results text but not directly in the summary CSV opened here. Difference 0.083 - 0.070 is 0.013, while manuscript says within 0.012; depending on unrounded source, this is a small rounding inconsistency. | None. | `subsec:feature_ablation`, `tab:nested_lopo_4core`, `tab:stage2_anova`, `tab:stage2_best`, `tab:vaccine_escape_stage3`, `ch:results` exist. | Minor |

## 2. Per-section severity counts

| Section in scope | Critical | Major | Minor | Verified |
|---|---:|---:|---:|---:|
| Scoring taxonomy and frequency/MSA/phylo definitions, 509-549 | 0 | 0 | 1 | 3 |
| Structural scores/source table, 551-581 | 0 | 2 | 0 | 0 |
| AI/Tranception/stability, 583-620 | 0 | 0 | 1 | 2 |
| Composite/EqualWeight, 622-632 | 0 | 0 | 1 | 1 |
| **Total** | **0** | **2** | **3** | **6** |

## 3. Recent-fix verification

| Anchor | Status | Check |
|---|---|---|
| omega2 CIs `[0.201,0.346]`, phylo-block `[0.202,0.346]`, wild-cluster `[0.201,0.303]` | NOT PRESENT in scoped lines | CSVs support rounded values: cluster `[0.2008,0.3455]`, block `[0.2022,0.3457]`, wild `[0.2005,0.3032]`; no regression in scope. |
| HIV-1 Layer A `n=23` mapped; `n=26` tags | NOT PRESENT | CSV check supports `adapt_lopo_results.csv` HIV-1 positives 23 and `layer_a_tags.csv` HIV-1 rows 26. |
| D614G retained per Korber 2020 | NOT PRESENT | `layer_a_tags.csv` has SARS-CoV-2 position 614 functional Korber 2020; no regression in scope. |
| Stage 1 functional regions `417 AA` | NOT PRESENT | Lines outside scope (ch3 396; ch4 50) use 417/1251, not 439. |
| Single-position scoring, gap-aware, not point substitutions only | PRESENT | Scope uses position-level scoring and indel-inclusive channels; no “point substitutions only” regression. |
| P1 null at/below mean 6/12 iid/circular, 4/12 protein-block, 7/12 local-burden | NOT PRESENT | `p1_null_per_pathogen.csv` recomputation gives exactly those counts. |
| Decision curve budget 50 random baseline 41 expected TPs | NOT PRESENT | `p2_decision_curve.csv` sum for random budget 50 = 41. |

## 4. Compression candidates

| Lines | Candidate | Reduction |
|---|---|---:|
| 551-552 | Split structural-source details into a corrected compact table note: “pLDDT sources differ by pathogen; SASA uses ESMFold/Shrake-Rupley; no Multimer/Foldseek/DALI quantitative alignment was run.” | >=70 words |
| 583-586 | Shorten Tranception caveat by moving HIV-1 interpretation and merged-channel sensitivity to table note/discussion only. | >=45 words |
| 614 | Remove duplicate statement that the supplementary per-pathogen CSV confirms table rounding; keep only underlying CSV path and columns. | >=30 words |
| 627-632 | Replace long EqualWeight prose with two bullets plus one sentence: production label-free min-max average; nested-LOPO sign-fit sensitivity only. | >=60 words |

## 5. Overall tally

Critical 0; Major 2; Minor 3; Verified 6; recent-fix regressions 0.

RESULT_AUDIT_V3_ch3e: critical=0 major=2 minor=3 regression=0
