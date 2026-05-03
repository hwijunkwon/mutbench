# Audit v3 ch3f: lines 636-762

## 1. Per-paragraph audit table

| Lines | Claims audited | Source check | Citations | Cross-refs | Severity |
|---|---|---|---|---|---|
| 637-639 | 39 detection methods, 14 families; 2 dependent ensembles excluded; methods convert 1D score arrays to calls. | `stage3_full_results.csv`: 8,580 rows = 20 scoring x 39 detectors x 11 pathogens; `family.nunique=14`; detector strings confirm 39 variants. Exclusion rationale not directly represented in CSV but is methodological. | n/a | `tab:detection_families` present. | Verified |
| 641-675 | Detector family table: variant counts and parameters; total 39; strings match `stage3_full_results.csv`; cited method precedents. | Variant counts from unique (`family`,`detector`) rows: FreqThresh 4, AdaptiveKnee 1, AdaptWin 2, Wavelet 3, Spectral 2, CUSUM 3, KDE 3, ScoreDBSCAN 2, SlidingTest 2, LocalContrast 3, GradPeak 2, Bayes 2, SWAN 9, MutClust-Orig 1. Sum = 39. Parameters match detector strings. | All cited keys present in `references.bib`: `mercatelli2020geographic`, `anastassiou2001genomic`, `arneodo2011wavelet`, `ester1996dbscan`, `tokheim2016hotmaps`, `tajima1989statistical`, `youn2025mutclust`. | Labels `tab:detection_families`, `tab:detection_variants` present and unique within `chapters_en`. | Verified |
| 677-680 | 11 pathogens each have 9-54 Layer A positives; detection-family omega2=0.013; 1-9 family variants; ANOVA models family (14) not 39 variants; MutClust variants section. | Feature matrices: Layer A counts range MERS 9 to HCV 54. `stage3_statistics.csv`: `family` omega2 = 0.012623, rounds to 0.013. Family count = 14 and detector count = 39. Note: older `threeway_anova_omega.csv` has a conflicting, obsolete-looking family omega2 = 0.022673 and only 9 scoring df; report should rely on `stage3_statistics.csv` for the 20-scoring grid. | n/a | `subsec:variants` present. | Verified |
| 686-710 | Table of structural characteristics: unique sequences, AA lengths, time spans, positive rates, HIV 23/450 vs 26 tags. | Unique seqs match `genbank_queries.csv`/Table 1; AA lengths and Layer A positive rates match feature matrices: SARS2 25/1259=2.0%, H3N2 25/543=4.6%, Norovirus 15/536=2.8%, HIV 23/450=5.1%, Dengue 24/490=4.9%, RSV 20/550=3.6%, FluB 17/560=3.0%, MERS 9/1330=0.7%, HCV 54/340=15.9%, Rabies 39/491=7.9%, EV-A71 27/261=10.3%. `layer_a_tags.csv`: HIV-1 has 26 tags. Time spans are not directly auditable from listed CSVs. | n/a | `tab:design_characteristics` present. | Verified |
| 712 | Heterogeneity ranges: unique seqs 530-5,019; length 261-1,330; temporal coverage ~2-50 years; Layer A positive rate 0.7-15.9%; pathogen factor conflates biology and availability. | Numeric ranges for unique seqs, length, and positive rate verified. Temporal coverage conflicts with table in same scope, whose minimum listed span is ~5 yr (SARS-CoV-2/MERS), not ~2 yr. No CSV source in scope supports ~2 yr. | n/a | n/a | Minor |
| 714-718 | Subsampling robustness stabilizes near 1,000 sequences and varies by < +/-0.002 at 25-100%; key interaction omega2=0.296; equalizing to n=530 MERS would reduce power. | `stage3_statistics.csv`: scoring x pathogen omega2 = 0.296252. MERS unique n=530 verified. However `subsampling_robustness.csv` does not support the stated < +/-0.002 over 25-100% as written: overall mean MCC range across fractions is 0.00337, and per-pathogen mean ranges are larger (e.g., H3N2 0.0456, SARS2 0.0320). The sentence may refer to an unreported subset, but the cited archive does not substantiate it. | n/a | `sec:robustness_validation` present in Chapter 4. | Major |
| 721-740 | Evaluation metrics; Layer A positives only; Layer B in MCC non-Layer-A pool and separate constrained FPR; DMS F1 for 6 pathogens. | `stage3_full_results.csv` has MCC/F1/precision/recall/n_detected, but not constrained FPR or DMS F1. Layer C availability for 6 pathogens matches Table `gt_positions` and DMS files. MCC label logic is methodological and consistent with feature matrices' binary `layer_a` column. | n/a | `eq:mcc` present below. | Verified |
| 742-755 | Stage 1 hotspot-score vs Stage 2 MCC rationale; length/MSA ranges 340-1,330 and 530-5,019; positive rates 0.7-15.9%; MCC formula/range/zero denominator convention; Chicco/Jurman citation. | Length range excludes EV-A71 because min 261 in the same table; if this sentence intentionally refers to a subset, it is not stated. MSA range and positive-rate range verified. MCC formula is standard. `chicco2020mcc` exists. | `chicco2020mcc` present. | `eq:hotspot_score`, `subsec:hotspot_score`, `eq:mcc` present. | Minor |
| 757 | 8,580 evaluation cells; columns `mcc`, `precision`, `recall`, `f1`, `n_detected`; MCC used for ANOVA and best-method analysis; positive rates 0.7-15.9%; F1/AUROC values per cell retained. | 8,580 and listed columns verified in `stage3_full_results.csv`. Cross-refs exist. Problem: `stage3_full_results.csv` contains no AUROC column, and no scoped archive row-level AUROC source was found. The phrase "F1 and AUROC values per cell are ... retained in the archived CSV bundle" is unsupported for AUROC. | `chicco2020mcc` present. | `subsec:9pathogen_statistics`, `ch:results`, `subsec:9pathogen_best_combos`, `tab:gt_positions` present. | Major |
| 759-762 | Stage 1 stability excluded from Stage 2 due to non-comparable Bernoulli masking across length/MSA variation; ANOVA heading/label. | Methodological claim consistent with Stage 2 using MCC columns only; no contradiction found. | n/a | `subsec:9pathogen_statistics` label present. | Verified |

## 2. Per-section severity counts

| Section | Critical | Major | Minor | Verified |
|---|---:|---:|---:|---:|
| Detection methods, 636-680 | 0 | 0 | 0 | 3 |
| Design considerations, 683-718 | 0 | 1 | 1 | 1 |
| Evaluation metrics/statistical design, 721-762 | 0 | 1 | 1 | 2 |

## 3. Recent-fix verification

| Anchor | Status | Check |
|---|---|---|
| omega2 CI cluster `[0.201, 0.346]`; phylo-block `[0.202, 0.346]`; wild-cluster `[0.201, 0.303]` | PRESENT | Present in ch3 lines 809-810 and ch4 line 490; CSV summaries show 0.2008-0.3455, 0.2022-0.3457, 0.2005-0.3032. |
| HIV-1 Layer A `n=23` mapped to gp120; `n=26` in tags | PRESENT | Scope line 690; feature matrix count 23; `layer_a_tags.csv` HIV-1 rows 26. |
| D614G retained in Layer A per Korber 2020 | PRESENT | `layer_a_tags.csv`: SARS-CoV-2 614 functional, "Korber 2020"; `korber2020tracking` in bib. |
| Stage 1 functional regions 417 AA = 1251 nt / 3, not 439 | PRESENT | ch3 line 396 and ch4 line 50 state 1,251 nt / 417 AA. |
| Single-position scoring, gap-aware, not "point substitutions only" | PRESENT | ch3 line 37 states single-position coding-region regime; no scoped regression to "point substitutions only" found. Gap/indel-aware scoring channels present (`freq_with_indel`, `entropy_with_indel`). |
| P1 null at-or-below-mean: 6/12 iid/circular, 4/12 protein-block, 7/12 local-burden | PRESENT | ch4 line 841; recomputed from `p1_null_per_pathogen.csv`. |
| Decision curve budget 50 random baseline 41 expected TPs | PRESENT | ch4 line 837; `p2_decision_curve.csv` budget 50 random sum = 41. |

## 4. Compression candidates

| Lines | Candidate reduction |
|---|---|
| 639 | Compress by >=15 words: "Two dependent majority-vote ensemble variants were excluded because they reused existing threshold methods and violated independence assumptions." |
| 673 | Compress by >=20 words by moving citation precedents to a shorter clause: "Detector strings in `stage3_full_results.csv` are authoritative for reproduction; citations document standard precedents for thresholding, wavelets, DBSCAN/hotspot clustering, sliding-window tests, and MutClust." |
| 714-718 | Compress by >=35 words after fixing unsupported subsampling wording: "Three factors mitigate this limitation: robustness checks reduce concern about sample-size dominance; the primary interaction is estimated within pathogens; and subsampling every pathogen to MERS n=530 would reduce power without equalizing temporal coverage or protein length." |
| 757 | Compress by >=50 words and fix AUROC: "For all 8,580 cells, `stage3_full_results.csv` archives MCC, F1, precision, recall, and detected-count columns. MCC is the headline metric because positive rates vary from 0.7% to 15.9%, Chicco and Jurman support MCC under large negative-class imbalance, and all confusion-matrix cells carry biological cost." |

## 5. Overall tally

Critical = 0; Major = 2; Minor = 2; Verified = 9; regressions among recent-fix anchors = 0.

RESULT_AUDIT_V3_ch3f: critical=0 major=2 minor=2 regression=0
