# Deep audit Job 1: abstract + Chapter 1

Scope: `front_en/abstract.tex`; `chapters_en/ch1_introduction.tex` lines 1-207. Sources checked: listed `results/mutbench/*.csv`, Chapter 3-5 cross-refs, and `references.bib` (126 entries). No web search was needed.

## Summary findings

- **Major:** Abstract/Ch1 report the cluster-bootstrap interval as `[0.195, 0.333]`, matching the `body_target` field, but the numeric CI columns in `results/mutbench/cluster_bootstrap_omega_summary.csv` are `[0.2008, 0.3455]`. If the CSV is authoritative, this is a discrepancy.
- **Major:** The requested “point substitutions only” scope is not cleanly represented. The manuscript says “single-position” and later “surface glycoprotein substitutions,” but the 20-formula grid includes `freq_with_indel` and `entropy_with_indel`; strict “point substitutions only” wording would conflict unless clarified as position-level outputs with gap-aware descriptors.
- **Major:** Contribution 3’s “from ~1,000 to 20-80 (top 5-10%)” mixes a rounded protein-length example with actual detector outputs. The HIV-1 full-set 7.19x row detects 32 positions; H3N2 9.36x detects 18; SARS-CoV-2 7.63x detects 11. The 20-80 range is directionally defensible for top-budget framing, but not all cited enrichment anchors fall inside it.
- **Minor:** The abstract says “Stage 1 SARS-CoV-2 MutClust-Hybrid hotspot-score 0.778” under a “controlled single-pathogen check”; Chapter 4 clarifies this is synthetic SARS-CoV-2-like data, not real GISAID data. The abstract should preserve that boundary.
- **Minor:** The abstract says validation is “restricted to 3/11 pathogens by curated antibody-escape annotation availability”; the rest of the chapter is consistent, but “HIV-1 primary anchor” should remain the headline because H3N2/SARS-CoV-2 are partly circular/exploratory.

### Chunk 1 (abstract + ch1 lines 1-105)

#### Numerical claims

- 11 RNA viruses / 20 scoring formulas / 14 families / 39 variants / 8,580 evaluations: **VERIFIED**. `stage3_full_results.csv` has 8,580 rows, 11 pathogens, 20 scoring values, 39 detector variants, 14 families.
- “10 biological information types”: **VERIFIED WITH TERMINOLOGY CAVEAT**. Chapter 4 uses “10 underlying biological features”; the scoring grid contains 20 formulas spanning six categories.
- Stage 1 MutClust-Hybrid hotspot-score 0.778: **VERIFIED** against Ch4 Table text (`HS=0.778`), but only for synthetic/controlled Stage 1.
- `omega^2_scoring x pathogen = 0.296`: **VERIFIED**. `cluster_bootstrap_omega_summary.csv` headline row has `0.2962519839`; Ch4 Table `tab:stage2_anova` repeats 0.296.
- Cluster-bootstrap CI `[0.195, 0.333]`: **DISCREPANCY**. Manuscript matches CSV `body_target`; numeric CSV columns for the 11-pathogen cluster bootstrap are `[0.2008358, 0.3455024]`.
- 6-category aggregation `omega^2=0.103`; residual `~0.39`: **VERIFIED** against Ch4 lines around `tab:stage2_anova`/text.
- Friedman `chi^2=7.69`, `p=0.990`; LOPO `0/11`; oracle-vs-generalized MCC gap `0.265`: **VERIFIED** against Ch4 LOPO/Friedman sections.
- HIV-1 full-set Fisher enrichment `7.19x`: **VERIFIED**. `vaccine_escape_stage3.csv` HIV-1 `freq` or `dnds_proxy` + `Wavelet(t=1.5)` has enrichment `7.1875`, 32 detected, 23 overlaps, p `3.16e-19`. Bonferroni x780 gives ~`2.46e-16`, matching `2.5e-16`.
- HIV-1 82% Layer-A-disjoint; novel-only `7.16-8.24x` on 37 positions; worst-case `p=5e-12`, Bonferroni `3.9e-9`: **UNVERIFIED IN LISTED CSVs**. These are repeated in Ch4/Ch5 prose, but not recoverable from `vaccine_escape_stage3.csv` alone.
- Feature-ablation: paired delta `+0.011`, CI `[-0.018,+0.042]`: **VERIFIED** from `feature_ablation_nested_lopo_summary.csv` (`0.0111275`, `-0.017747`, `0.042390`).
- Full-10 LOPO `0.070`, fixed-4 `0.081`: **VERIFIED** from the same summary CSV.
- 4-core rank `87/1023`: **VERIFIED** from `codex_wave1/p3_full_lattice_1023.csv` (`is_core_4` combo ranks 87 by mean MCC).
- Layer A' mean MCC `-0.055`, precision@20 `0.005`: **VERIFIED** from `codex_layerA_prime/lopo_summary.csv`.
- H3N2 `9.36x`: **VERIFIED** from `vaccine_escape_stage3.csv` (`fubar_bf` + `Wavelet(t=2.0)`, enrichment `9.3621`).
- H3N2 69% Layer-A overlap: **UNVERIFIED IN `vaccine_escape_stage3.csv` ALONE**. The `9.36x` detector row has 9 detected escape overlaps; the 69% claim appears to refer to escape-set/Layer-A circularity from Ch4 prose, not the detector-overlap column. Needs label clarity but not necessarily wrong.
- SARS-CoV-2 `7.63x`: **VERIFIED** from `vaccine_escape_stage3.csv` (`fubar_pos_sel` + `FreqThresh(p=85)`, enrichment `7.6303`).
- EqualWeight H3N2 `4.012x`, `p=0.0023`: **UNVERIFIED IN `vaccine_escape_stage3.csv`**. Closest H3N2 EqualWeight rows need a separate integration table not listed; Ch4 prose supports the claim but the listed CSV does not expose it directly.
- 9 distinct optimal information types across 11 pathogens; H3N2 MCC `0.534`; SARS-CoV-2/RSV PLM; Norovirus homoplasy: **VERIFIED**. `stage3_full_results.csv` maxima show 9 distinct best scorings; H3N2 `fubar_bf` MCC `0.534058`, SARS-CoV-2 `tranception`, RSV `esm2_llr`, Norovirus `homoplasy`.
- Ch1 lines 9, 33, 42, 47, 49, 82-86, 98-100: **MOSTLY VERIFIED/PLAUSIBLE**. More than 700M SARS-CoV-2 cases is stable; “13 viruses/79 DMS/7 phenotypes,” “45 DMS/31 clades/40 WHO viruses,” and “217 DMS/90+ baselines” match `references.bib` titles/metadata and local prose. “Millions” and “tens of thousands” are broad background claims.
- Panel-scope box: **VERIFIED**. Ch4/Ch5 define 11 main, 12-pathogen feature panel as 11+Zika, Wave 4 as 12 labeled + 16 unlabeled = 28, and Wave 5 as 10 UniProt-derived targets.

#### Citations

- `harvey2021tracking`, `carabelli2023convergent`: support SARS-CoV-2 variant tracking/convergent evolution/immune escape; **OK**.
- `virogym2026`, `gurev2026everest_v3`, `notin2023proteingym`, `notin2025proteingym_v13`, `thadani2023evescape`, `livesey2020using`: support concurrent variant-effect/fitness/escape benchmark context; **OK**, assuming the 2026/2025 entries are accepted dissertation-local references.
- `bailey2018comprehensive`: cancer hotspot benchmark analogy; **OK**.
- `han2025mosd`, `youn2025mutclust`: prior author framework/method claims; **OK** per local bibliography.
- `nextstrain2018hadfield`, `rambaut2020pangolin`: surveillance/classification platforms; **OK**.
- `rice1976algorithm`: algorithm selection problem; **OK**.

#### Cross-refs

- `tab:glossary`, `ch:mutbench`, `ch:results`, `ch:discussion`, `sec:future_work`, `subsec:feature_ablation`, `para:w4_tier2_lopo`, `para:w5_layer_a_prime`, `fig:research_overview`: **VERIFIED**, labels exist and target the intended objects.

#### Logical consistency / outdated content

- No “9 pathogens,” “12-pathogen Stage 2,” or “PAHD” stale wording in this chunk.
- The scope wording is internally close but not exact: “single-position” is consistent; “point substitutions only” would be too strong without noting indel-inclusive scoring formulas.

#### Severity

- 0 Critical / 2 Major / 3 Minor.

### Chunk 2 (ch1 lines 106-207)

#### Numerical claims

- Contribution 1: 11 RNA viruses, 8,580 cells, 20 scoring formulas, 39 variants, 14 families, 10 information types, six categories, 12-pathogen Stage 3 with Zika: **VERIFIED** from `stage3_full_results.csv`, Ch3 scope, and Ch4 feature-ablation section.
- Contribution 2: `omega^2=0.296`, 9 optimal information types, LOPO `0/11`, Friedman `p=0.990`, CI `[0.195,0.333]`, 6-category `0.103`, residual `~0.39`: **VERIFIED EXCEPT CI DISCREPANCY** as above.
- Contribution 3: `~1,000` to `20-80` / top `5-10%` and `7-9x`: **PARTLY VERIFIED**. Enrichments are supported for HIV-1/H3N2/SARS-CoV-2 anchors, but detector counts vary (HIV-1 32; H3N2 18; SARS-CoV-2 11 for cited anchors), so “20-80” is a practical-budget generalization, not a literal range for every cited result.
- HIV-1 37/45 novel-only and Bonferroni values: **UNVERIFIED IN LISTED CSVs**; repeated in Ch4/Ch5 prose but no row-level listed source.
- H3N2 `9.36x`; EqualWeight `4.012x`, `p=0.0023`; SARS-CoV-2 “persists after correction”: **MIXED**. H3N2 9.36 is verified; EqualWeight 4.012 not exposed in `vaccine_escape_stage3.csv`; SARS-CoV-2 `7.63x` has nominal p `0.0264`, which would not survive a 780-test Bonferroni by itself, so “persists after multiple-comparison correction” needs its exact supporting row/table identified.
- 4-core nested-LOPO values in table: **VERIFIED** from `feature_ablation_nested_lopo_summary.csv`.
- Dissertation has four chapters: **VERIFIED** by local chapter labels (`ch1`, `ch3`, `ch4`, `ch5`, with background input merged into Ch1).

#### Citations

- `virogym2026`, `gurev2026everest_v3`, `notin2025proteingym_v13`: used for benchmark comparison in Contribution 1; **OK**.
- No new citations in lines 172-207.

#### Cross-refs

- `tab:intro_external_validation_ledger`, `tab:stage2_anova`, `tab:nested_lopo_4core`, `ch:background`, `ch:mutbench`, `ch:results`, `ch:discussion`, `sec:limitations`: **VERIFIED**. Targets exist and match intended objects.

#### Logical consistency / outdated content

- Contribution hierarchy is **consistent** with Ch3-5: C1 builds artifact/framework; C2 reports modeled pathogen-dependent information utility; C3 is external validation with HIV-1 as primary anchor and 4-core as bounded robustness, not a separate headline contribution.
- The “SARS-CoV-2 exploratory” row conflicts with “persists after multiple-comparison correction” unless a separate corrected statistic is cited; the visible CSV row nearest 7.63 has p `0.0264`, not Bonferroni-significant across 780.
- No stale “9 pathogen,” “12-pathogen Stage 2,” or “PAHD” wording found in scoped lines.

#### Severity

- 0 Critical / 1 Major / 1 Minor.

## Overall

The chapter is largely aligned with the active Ch3-5 evidence hierarchy and the current panel definitions. The highest-risk defense issues are not the main framework counts, which verify cleanly, but the few headline numerical claims whose exact support is either only in prose or differs from the numeric CSV columns.

RESULT_DEEP_J1: critical=0 major=3 minor=4
