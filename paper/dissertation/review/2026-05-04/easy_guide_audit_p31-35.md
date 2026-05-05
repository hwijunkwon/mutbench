# Easy Guide Audit p31-35

## 1. 정확성 (numbers)
| Statement | Page | dissertation source | Match? |
|---|---:|---|---|
| Frequency-entropy rho=0.97; homoplasy rho<0.23 | 31 | easy guide md lines 927, 931 | Yes |
| Ablation: 12 pathogens incl. Zika; homoplasy removal ΔMCC=-0.028; 4-feature 97.6%, MCC 0.081 vs 0.083; 11-pathogen baseline 0.083 -> 0.093 | 31 | md line 932 | Yes to source; source-level claim not independently re-verified here |
| Layer A 80-100% immune escape; optimum info split into 5 types; omega^2=0.296 | 31 | md line 933; stage3_statistics.csv gives 0.29625198 | Yes |
| Vaccine escape table: H3N2 9.36x, HIV-1 7.19x, SARS-CoV-2 7.63x | 31 | md lines 939-943; reference anchors | Yes |
| HIV-1 clean external validation: entropy MCC 0.275, freq 7.19x, Bonferroni p=2.5e-16, 82% Layer-A-disjoint | 31 | md line 964; reference anchors | Yes, but incomplete: omits 37/45 novel count |
| H3N2 self-consistency: 69% Layer A overlap; novel-only 9 positions; enrichment 7.19x, Fisher p=0.132 | 31 | md line 965 | Yes to source |
| SARS-CoV-2 7.63x loses Bonferroni significance | 31 | md line 966 | Yes |
| EqualWeight escape enrichment: H3N2 4.01x p=0.0023, HIV-1 4.17x p=0.0037, SARS-CoV-2 2.67x p=0.171, 2/30 | 32 | md lines 972-978 | Yes |
| Adaptive weights: kNN 0.020, Top-3 AUC 0.049, correlation-aware 0.043, EqualWeight 0.083, Oracle 0.160, 13D/11 ratio ~1.1, 20-30 pathogens | 32 | md lines 996-1002 | Yes |
| PAHD-R modes: exact/+-10/P@20/FPR/coverage values | 33 | md lines 1018-1022; pahd_r_final_reporting_table.csv | Text source yes; rendered PDF clips FPR/coverage/status columns |
| HCV E2 repair exact MCC 0.5257, constrained FPR 0.0000; SARS-CoV-2 repair exact 0.2304, +-10 0.8761, P@20 0.1000 | 33-34 | md lines 1049-1050; PAHD-R CSVs | Yes |
| Selective callable-only answers 4/9 viruses | 34 | md line 1064 | Yes |
| MutClust-Hybrid hotspot-score 95% CI [0.323, 0.635] | 35 | md lines 694, 1098 | Source-consistent, but wording says "Stage 2 MCC" while metric is Stage 1 hotspot-score CI. Major clarity/accuracy label issue |
| Synthetic F1=0.785 vs real F1=0.123; 29,903 positions, 1.14% nonzero H-score; enrichment 6.9-8.0x | 35 | md lines 657, 672, 1102 | Yes |
| 3D spatial contact enrichment 5.92x, z=13.34 | 35 | md lines 720, 1106 | Yes |
| founder mutation 90%, convergent 15 origins, founder top in 100%, rho=-0.876 | 35 | md line 1112 | Yes |
| Oracle MCC=0.341; generalized MCC=0.032 | 35 | md lines 842, 1116-1120; stage3_statistics.csv mean_gen_mcc=0.0315 | Yes |
| Exact MCC 0.289 -> +-5 0.638 -> +-10 0.712; H3N2 +-10 0.964 | 35 | md line 1126; region_overlap_mcc.csv has H3N2 +-10=0.9638 but 9-pathogen mean is exact 0.289, +-5 0.638, +-10 0.712 | Mostly yes, but label as "Exact 기준 MCC" is underspecified and conflicts with nearby/later 11-pathogen oracle mean 0.341/0.472/0.454. Needs denominator/method label |

## 2. 명확성 (clarity)
- Issues: Page 32's adaptive-weight paragraph is too compressed: four MCC values are run into one line in the PDF. Use a small table or bullets with one strategy per line.
- Page 35 says "Stage 2의 MCC" then reports "MutClust-Hybrid의 hotspot-score 95% CI"; this mixes Stage 2 MCC with Stage 1 hotspot-score and will confuse readers.
- Technical terms still needing one-phrase definitions in this chunk: Bonferroni, oracle, self-consistency, feature-value correlation, constrained FPR, coverage, BCa bootstrap, founder effect, homoplasy. Some were likely defined earlier, but pages 31-35 use them densely.
- "Exact MCC 0.289..." on page 35 needs scope: appears to be the region-overlap calculation over the available subset, not the 11-pathogen oracle headline.

## 3. 일관성 (framing consistency)
- Strong: PAHD-R is consistently framed as a review/prioritization framework, not a deployable detector or universal AI predictor.
- Strong: HIV-1 is correctly described as the clean external validation anchor; H3N2 is self-consistency, SARS-CoV-2 exploratory.
- Major framing gap: the practical validation section still foregrounds vaccine escape enrichment. The reference state says Layer C DMS 6/11 pathogens is the primary wet-lab/functional anchor. Within pages 31-35, Layer C appears only as an independence example on page 35, not as the primary practical evidence.

## 4. 누락 (missing anchors)
- Missing/underweighted: Layer C 6/11 pathogens, 650 positions, MCC 0.139-0.322 should be referenced near 4.5.4 or the start of Discussion because this chunk discusses practical validation.
- Missing precision: HIV-1 82% Layer-A-disjoint is present, but 37/45 novel is not.
- Present: HIV-1 7.19x and omega^2=0.296 are present and correctly framed.

## 5. 잉여 (redundancy)
- HIV-1/H3N2/SARS enrichment appears in Table 23 and then again immediately in bullets. This is useful for interpretation, but can be shortened by moving p_adj/disjoint/self-consistency qualifiers into the table or a compact "interpretation" row.
- Page 34's "말하면 안 되는/되는 표현" is useful defense guidance, but five bullets each is long for the easy guide. Keep the three highest-risk phrases.

## 6. 시각적 (layout)
- Page 31 tables render cleanly.
- Page 32 figure and Table 25 render cleanly, but the adaptive-weight sentence is visually crowded.
- Visual issue: Page 33 PAHD-R mode table is clipped on the right. The PDF shows only part of "Constrained F..." and loses the Coverage/final-status columns from the markdown table.
- Visual issue: Page 34 "추가 후보" table overruns the right margin; long interpretation text is cut off.
- Page 34 repair table split across pages is acceptable, though the continuation lacks a repeated section title/context.
- Page 35 renders cleanly.

## TOP 5 fixes
1. Add the Layer C DMS practical anchor in or near 4.5.4: 6/11 pathogens, 650 positions, MCC 0.139-0.322, and state it is the primary functional/wet-lab anchor; keep HIV-1 7.19x as external vaccine-escape anchor.
2. Fix page 35 metric wording: do not call the MutClust-Hybrid hotspot-score CI "Stage 2 MCC"; label it Stage 1 hotspot-score or replace with a Stage 2 MCC CI if intended.
3. Clarify page 35 region-window numbers: specify the subset/method behind 0.289 -> 0.638 -> 0.712, or align with the 11-pathogen oracle mean 0.341 -> 0.472 -> 0.454.
4. Reformat the page 33 PAHD-R mode table to fit: drop Coverage/status, rotate, shrink, or split into "metrics" and "adoption" tables.
5. Reformat the page 34 additional-candidates table with wrapped paragraph cells or bullets so no text is clipped.

RESULT_EASY_GUIDE_AUDIT_p31_35: critical=0 major=4 minor=7 visual_issues=2
