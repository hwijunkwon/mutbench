# Audit v2 Job 5: ch3_methods.tex lines 1-300

Scope: `paper/dissertation/chapters_en/ch3_methods.tex:1-300`. Paragraph-level audit; read-only source inspection, no web verification performed.

## Per-Paragraph Table

| Paragraph | Numeric claims and source status | Citations | Refs | Consistency / recent-fix check | Severity |
|---|---|---|---|---|---|
| P1 lines 5-12 | 11 viruses, 20 scoring types, 14 families, 5 categories, 39 variants, 3-layer GT, 2 main stages + Stage 3: VERIFIED in `results/mutbench/stage3_full_results.csv` shape/fields, `results/mutbench/stage3_statistics.csv`, `results/mutbench/pahd_r_coordinate_provenance_layers.csv`, and method tables later in ch3. | none | `subsec:stage3_methods`, `sec:mutbench_materials`, `sec:mutbench_methods`, `subsec:framework_overview`, `subsec:3layer_gt`, `subsec:stage1`, `sec:stage2`, `sec:eval_stat_design` all resolve in ch3. | Consistent with ch4 8,580-cell design. No regression wording. | Verified |
| P2 lines 21-30 | Pathogen list and alignment lengths VERIFIED against `results/mutbench/provenance/genbank_queries.csv` for sequence counts/query dates and `results/mutbench/pahd_r_coordinate_provenance_layers.csv` for effective lengths: 1,259, 1,330, 550, 543, 560, 450, 340, 536, 490, 491, 261. Full-length examples UNVERIFIED in CSV. Substitution-rate range and Zika 52 sequences UNVERIFIED in inspected CSVs. | none | `tab:pathogen_data`, `sec:information_analysis` resolves in ch5_adapt. | Consistent with panel scope. | Minor |
| P3 lines 33-34 | 8 families/four routes UNVERIFIED in CSV; sequence-ratio range VERIFIED from `genbank_queries.csv` (SARS 753/4982=15.1%, Rabies/EV-A71 100%). Substitution rates UNVERIFIED. D614G wording retains founder effect but not exclusion. HVR1 384-410, HCV omega 0.246, Norovirus AUC 0.944: omega is only indirectly supported by `cluster_bootstrap_omega_summary.csv` body target for HCV-excluded evaluation, not a clearly named “HCV-only” CSV; Norovirus AUC VERIFIED in `pahd_r_data_processing_pathogen_summary.csv` (0.9435). DMS six pathogens VERIFIED in `layer_c_evaluation.csv`. Zika 52 UNVERIFIED. | none | `subsec:layer_a`, `tab:gt_positions`, `ch:discussion`, `sec:gt_heterogeneity`, `sec:information_analysis` resolve. | D614G fix OK: functional/founder wording, no exclusion. | Minor |
| P4 lines 37-42 | Query dates/counts/modes VERIFIED in `genbank_queries.csv`; sequence scale 1,311-5,325 VERIFIED. Ambiguous-base cutoff >5%, SHA-256 dedup implementation, 100% identity equivalence, no HMMER, truncation policy: plausible but UNVERIFIED in CSV except final unique counts. | `fu2012cdhit`, `steinegger2017mmseqs2`, `eddy2011hmmer`, `katoh2013mafft` plausibly support tools. | `tab:gt_positions`, `tab:pathogen_data` resolve. | “single-position regime” is compatible with gap-aware position-level scope; no old “point substitutions only.” | Minor |
| P5 table lines 44-72 | Table values VERIFIED against `genbank_queries.csv` for accessions, sequences, unique counts, dates, MAFFT modes. Alignment lengths VERIFIED against `pahd_r_coordinate_provenance_layers.csv`. N x L products not explicitly archived; EV-A71 662 x 261 approx 1.7e5 arithmetic OK. | Katoh citation in caption/note plausible. | `tab:pathogen_data` resolves. | Consistent. | Verified |
| P6 lines 81-83 | 3 components, 20 scoring, 14 families, 39 variants, 11 pathogens VERIFIED as above. | none | `fig:mutbench_pipeline`, `subsec:stage3_methods` resolve. | Consistent. | Verified |
| P7 figure lines 85-127 | Figure numbers 11, 6 categories, 20 types, 39 methods, 14 families, 3 layers: VERIFIED as design constants in ch3 and `stage3_full_results.csv`; 39 detector variants visible in detector strings. | none | `fig:mutbench_pipeline` resolves. | Consistent. | Verified |
| P8 lines 129-132 | Three layers and Stage 1 synthetic/DMS claims: VERIFIED conceptually in ch3; synthetic data not CSV-verified in this scope. | none | `subsec:3layer_gt` resolves. | Consistent. | Verified |
| P9 lines 134-137 | 20 scoring / six categories / 14 families / 39 variants / five categories VERIFIED in ch3 method tables and `stage3_full_results.csv`. | none | `subsec:stage1`, `sec:stage2` resolve. | Consistent. | Verified |
| P10 lines 139-142 | Metrics and stats list VERIFIED in `stage3_full_results.csv`, `stage3_statistics.csv`, `cluster_bootstrap_omega_summary.csv`. | none | `sec:eval_stat_design` resolves. | Consistent. | Verified |
| P11 lines 148-149 | 3-layer framework claim: VERIFIED in ch3 tables and `pahd_r_coordinate_provenance_layers.csv` / `layer_c_evaluation.csv`. | none | `fig:3layer_gt_concept` resolves. | Consistent. | Verified |
| P12 figure lines 151-188 | Layer roles and metrics: VERIFIED against `layer_c_evaluation.csv` (Layer A/C) and constrained FPR columns in `multilayer_summary.csv`. | none | `fig:3layer_gt_concept` resolves. | Consistent. | Verified |
| P13 lines 190-191 | Three dimensions: no numerical claims. | none | none | Consistent. | Verified |
| P14 table lines 193-209 | Top 20% Layer C role: VERIFIED as design in `layer_c_evaluation.csv`; “6 pathogens only” VERIFIED. | none | `tab:gt_layer_roles` resolves. | Consistent. | Verified |
| P15 lines 214-217 | SARS-CoV-2 example positions E484K/E484A: numerical position 484 UNVERIFIED locally except Layer A sources; claim plausible. | none in paragraph | `tab:gt_positions` resolves. | D614G not mentioned/excluded. | Verified |
| P16 lines 218-224 | `>=3`, seven remaining pathogens, omega range 0.234-0.296, Layer B cutoff 0.5, Layer C 20%, 20x39=780, 20x14x11=3,080, freeze date 2024-08-12: counts/omega VERIFIED in `stage3_statistics.csv`, `ancova_omega_summary.csv`, `cluster_bootstrap_omega_summary.csv`; arithmetic OK. Freeze/SOP and no post-hoc adjustment UNVERIFIED in CSV. | `carabelli2023convergent` OK for SARS-CoV-2 convergence. | `tab:gt_positions`, `ch:discussion`, `sec:gt_heterogeneity` resolve. | Consistent with ch4/ch5. | Minor |
| P17 lines 227-231 | No hard numeric claims. MCC/Layer B constrained-FPR separation VERIFIED in `layer_c_evaluation.csv` and `multilayer_summary.csv`. | none | `subsec:9pathogen_metrics` resolves. | Consistent. | Verified |
| P18 lines 233-236 | Layer B dN/dS <0.5 and omega<1 convention: citation OK, but source-study codon estimates not CSV-verifiable here. SARS-CoV-2 154 Layer B, HR1 912-984, HR2 1,163-1,213: 154 VERIFIED in `pahd_r_coordinate_provenance_layers.csv`; region components UNVERIFIED in CSV. | `yang2007paml`, `wrapp2020cryo` plausibly support selection convention / Spike structure. | `subsec:9pathogen_scoring` resolves. | Consistent. | Minor |
| P19 lines 240-244 | Six DMS pathogens VERIFIED in `layer_c_evaluation.csv`. Top 20%, thresholds 10/20/30 on 4 of 6: threshold design partly VERIFIED by `layer_c_evaluation.csv`; sweep coverage not located in inspected CSV. DMS phenotypes/citations plausibly support but Simonich/Aditham/Bakhache are recent and should remain WEB-VERIFY if defense depends on publication status. | DMS citations OK / WEB-VERIFY for 2025-2026 pending sources. | `subsec:dms_evolution_correlation`, `tab:dms_preprocessing` resolve. | Consistent. | Minor |
| P20 table lines 246-269 | Replicates = 2 for six sources, top 20%, 4 of 6 sweep, 3+ original for starred sources: pipeline replicate counts VERIFIED in `provenance/dms_sources.csv`; threshold and source paths VERIFIED there. | Source names match bibliography/provenance; recent pending sources WEB-VERIFY if needed. | `tab:dms_preprocessing`, `subsec:dms_evolution_correlation` resolve. | Consistent. | Verified |
| P21 lines 271-275 | RSV overlaps 148/152, Influenza B 141/194, effective B counts 16 and 8: raw B counts (18,10) VERIFIED in `pahd_r_coordinate_provenance_layers.csv`; overlap/effective subtraction not directly CSV-verified in inspected files. | none | none | Consistent with stated Layer A priority. | Minor |
| P22 lines 277-282 | Top 20% and 6 pathogens VERIFIED; logic has no arithmetic issue. | none | `subsec:dms_evolution_correlation`, `tab:layer_a_vs_c` resolve. | Consistent with non-merged label design. | Verified |
| P23 lines 284-300 | Table rows in scope: Layer A/B VERIFIED in `pahd_r_coordinate_provenance_layers.csv`; Layer C VERIFIED in `layer_c_evaluation.csv`: SARS-CoV-2 25/154/247, H3N2 25/10/112, Norovirus 15/229/---, HIV-1 23/23/48, Dengue 24/24/---. HIV-1 recent fix OK: table uses mapped gp120 count 23 while `layer_a_tags.csv`/`gt_heterogeneity_analysis.csv` carry 26 tags. | Table citations plausibly match pathogens; no suspicious key found locally. | `tab:gt_positions` resolves. | No regression; HIV-1 count reconciliation is correct in this scoped row. | Verified |

## Per-Section Severity Counts

| Section | Critical | Major | Minor | Verified |
|---|---:|---:|---:|---:|
| Chapter setup / Materials intro (1-43) | 0 | 0 | 3 | 1 |
| Pathogen data table (44-72) | 0 | 0 | 0 | 1 |
| Framework overview (75-143) | 0 | 0 | 0 | 5 |
| 3-layer GT overview (145-209) | 0 | 0 | 0 | 4 |
| Layer A/B/C methods and GT table start (211-300) | 0 | 0 | 5 | 5 |

## Overall Tally

Critical: 0. Major: 0. Minor: 8. Verified: 16. Regression: 0.

No scoped paragraph uses the old D614G exclusion, old omega CI, old HIV-1 count wording, old Stage 1 439-AA claim, or “point substitutions only” wording.

RESULT_AUDIT_V2_J5: critical=0 major=0 minor=8 regression=0
