# Easy Guide Audit p16-20

## 1. 정확성 (numbers)
| Statement | Page | dissertation source | Match? |
|---|---:|---|---|
| Stage 2 scoring types = 20, categories = 6 | 16 | easy_guide_v2.md:481; v229 reference state | Yes |
| 14 detection families, 39 parameter variants | 16 | easy_guide_v2.md:483-507; Stage 2 design | Yes |
| Family variant counts: FreqThresh 4, AdaptiveKnee 1, AdaptWin 2, Wavelet 3, Spectral 2, CUSUM 3, KDE 3, ScoreDBSCAN 2, SlidingTest 2, LocalContrast 3, GradPeak 2, Bayes 2, SWAN 9, MutClust-Orig 1 | 16 | easy_guide_v2.md:488-507 | Yes |
| Dataset imbalance: MERS 530 vs Influenza B 5,019; EV-A71 261 AA vs MERS 1,330 AA; 9.5x and 5.1x | 16 | easy_guide_v2.md:513-515 | Yes |
| Time span: SARS-CoV-2 2019-2024 vs H3N2/Rabies about 50 years | 16 | easy_guide_v2.md:515 | Yes |
| Layer A positive rate: MERS 0.7% vs HCV 15.9%; subsampling stabilizes near 1,000 sequences; min equalization 530 | 16 | easy_guide_v2.md:516-521 | Yes |
| scoring x pathogen omega^2=0.296 | 16-17 | stage3_statistics.csv: scoring x pathogen omega=0.2962519839; v229 anchor omega^2=0.296 | Yes, but CI [0.201, 0.346] is omitted where this anchor is explained |
| Hotspot-score example: 0.778, about 66% recall, 97% precision, 71% stability, 25 positives | 17 | method_comparison cited by prior audit; easy_guide_v2.md:532, 586-590 | Yes |
| MCC range -1 to +1; hotspots 1-16% | 17 | easy_guide_v2.md:533 | Yes |
| 20% removal; alignment length 261-1,330 AA; MSA 530-5,019 | 17 | easy_guide_v2.md:537 | Yes |
| 8,580 evaluations = 20 scoring x 39 detector variants x 11 pathogens | 17 | easy_guide_v2.md:439, 541; stage3_statistics.csv | Yes |
| ANOVA factors listed as 20 x 14 x 11 | 17 | easy_guide_v2.md:543 | Mostly: family-level explanation is 14 families, but 8,580 uses 39 variants; wording should explicitly distinguish family vs variant |
| Friedman p=0.990 | 17 | stage3_statistics.csv p=0.9895444533; v229 anchor p=0.990 | Yes |
| LOPO 0/11; permutation P about 0.96; oracle-generalized MCC gap 0.265 | 17 | stage3_statistics.csv match_rate=0, mean_gen_mcc=0.0315, gap=0.2654; easy_guide_v2.md:545 | Yes |
| Score ranges: freq 0-1, homoplasy 0-53, pLDDT 0-100; AI 5 vs homoplasy 1; category ANOVA omega^2=0.103 | 17 | easy_guide_v2.md:552-554 | Yes |
| Layer A/frequency rho: mean 0.12; HCV 0.33, Influenza B 0.26, Norovirus 0.23; feature rho=0.97 | 18 | easy_guide_v2.md:555; stage3_statistics.csv fairness rho=0.9727 for feature-level | Yes |
| Stage 1 list says "5 experiments", table lists 4.1.1-4.1.6 = 6 rows | 19 | easy_guide_v2.md:567-576 | No: internal count mismatch |
| Synthetic genome 29,903 positions; 7 functional regions; 1,251 positions | 19 | thesis_text.txt lines around 2920-2963; easy_guide_v2.md:582 | Yes |
| "5 MutClust improvements + 2 baselines" but Table 13 has only 5 methods | 19 | easy_guide_v2.md:582-590; prior audit notes method-count inconsistency | No: statement/table mismatch |
| Table 13 metrics: MutClust-Hybrid P=0.968, R=0.659, F1=0.785, stability=0.706, hotspot-score=0.778; HDBSCAN P=0.079, R=0.944, F1=0.146, stability=0.788, HS=0.604 | 19 | easy_guide_v2.md:584-590; prior audit verified against method_comparison.csv | Yes |
| Real GISAID F1 drop to 0.123 | 19 | easy_guide_v2.md:596, 657 | Yes |
| Figure 3 genome 29,903 positions; Spike 21,563-25,384 | 20 | easy_guide_v2.md:602 | Yes |
| Table 14: Functional 439/F1 0.474; DMS 252/F1 0.315; convergent 97/F1 0.188/enrichment 1.70x; strict F1 0.108/enrichment 3.43x | 20 | multi_ground_truth_summary.csv; easy_guide_v2.md:618-623 | Yes |

## 2. 명확성 (clarity)
- Issues: page 16's long parameter sentence is too dense for "쉬운 설명"; it can be moved to a note or split by detector family.
- Issues: page 17 defines MCC, Constrained FPR, DMS F1 well, but ANOVA/Friedman/LOPO still use "oracle", "generalized", "permutation", "corroboration", "BCa bootstrap CI" without plain Korean explanations.
- Issues: page 18 has one very technical correlation bullet alone on the page; "point-biserial", "feature-level collinearity" need a one-sentence Korean gloss.
- Issues: page 19 says "5개 실험" then lists 6; this is confusing before any technical detail.

## 3. 일관성 (framing consistency)
- No "deployable detector" overclaim found in pages 16-20. The wording stays mostly in benchmark/evaluation/triage territory.
- HIV-1 anchor is not discussed in this chunk, so no inconsistent HIV-1 wording found.
- Layer C is presented as independent DMS validation, but not yet as the primary practical wet-lab evidence. Since page 17-18 already discuss DMS F1 and Layer C, this is a framing gap rather than a contradiction.

## 4. 누락 (missing anchors)
- Missing: omega^2=0.296 is present, but the v229 robustness CI [0.201, 0.346] is absent in the ANOVA explanation.
- Missing: where DMS F1/Layer C is introduced, add the practical anchor "Layer C DMS is available for 6/11 pathogens, 650 positions, best MCC 0.139-0.322" or a short forward reference.
- Missing: HIV-1 7.19x is not necessary in the Stage 1 pages, but in the evaluation-design paragraph a forward reference to "external validation is anchored later by HIV-1" would help align the chunk with the dissertation-level argument.

## 5. 잉여 (redundancy)
- Page 16 repeats all 39 parameter variants in prose after Table 11. For easy-guide readability, keep either the table plus a short "39 variants total" sentence, or move parameter details to an appendix-style note.
- Page 19 repeats the synthetic-overestimation caution acceptably; not wasteful because it prevents overclaiming.

## 6. 시각적 (layout)
- Page 16 Table 11 renders correctly, but the parameter paragraph below it is visually dense.
- Page 17 renders correctly, but the page is text-heavy.
- Page 18 is a major layout issue: nearly blank page with only one bullet at the top. Pull content back, insert the Chapter 4 break earlier/later, or force a cleaner page break.
- Page 20 Figure 3 image and caption match. Table 14 renders correctly. No obvious caption mismatch.

## TOP 5 fixes
1. Fix page 19 count mismatch: either "6개 실험" or remove one listed row.
2. Fix page 19 method-count mismatch: change "5가지 MutClust 개선 버전 + 2가지 기준선" to match the 5 displayed methods, or show all 7 methods.
3. Add omega^2 robustness CI [0.201, 0.346] near the omega^2=0.296 ANOVA explanation.
4. Add a concise Layer C anchor where DMS F1 is introduced: 6/11 pathogens, 650 positions, MCC 0.139-0.322.
5. Repair the page 18 flow; it should not be an almost blank page for a single technical bullet.

RESULT_EASY_GUIDE_AUDIT_p16_20: critical=0 major=3 minor=5 visual_issues=1
