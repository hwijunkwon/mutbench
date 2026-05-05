# Easy Guide Audit p11-15

## 1. 정확성 (numbers)
| Statement | Page | dissertation source | Match? |
|---|---:|---|---|
| Layer A ranges 병원체당 9~54 positions | 11 | Table 9: MERS 9, HCV 54 | Yes |
| Layer B ranges 병원체당 0~229 positions | 11 | Table 9: HCV 0, Norovirus 229 | Yes |
| Layer C available in 6/11 pathogens | 11-12 | v229 anchor; `layer_c_evaluation.csv` has SARS-CoV-2, H3N2, HIV-1, RSV, Rabies, EV-A71 | Yes |
| Jaccard similarity = 0.006 | 11 | Easy guide source line ~358; no contrary v229 anchor in scope | Yes |
| Table 9 Layer A/B counts: SARS-CoV-2 25/154, H3N2 25/10, Norovirus 15/229, HIV-1 23/23, Dengue 24/24, RSV 20/18, Influenza B 17/10, MERS 9/110, HCV 54/0, Rabies 39/42, EV-A71 27/29 | 11-12 | Easy guide source lines ~364-376; HCV Layer B footnote | Yes |
| Table 9 Layer C counts: SARS-CoV-2 252, H3N2 102, HIV-1 100, RSV 101, Rabies 87, EV-A71 55 | 11-12 | v229 anchor says Layer C 650 positions; `layer_c_evaluation.csv` prints 247, 112, 48, 101, 87, 55 = 650 | **No - stale. Printed total would be 697.** |
| HCV CD81 AA 418-535 exceeds 340 AA alignment; effective Layer B = 0 | 12 | Easy guide source line ~380; Table 9 HCV B=0 | Yes |
| Complete A+B+C pathogens = 6: SARS-CoV-2, H3N2, HIV-1, RSV, Rabies, EV-A71 | 12 | v229 Layer C 6/11 anchor | Yes |
| RSV A/B overlap 148, 152; Influenza B 141, 194; effective B RSV 16, Influenza B 8 | 12 | Easy guide source lines ~394-398 | Yes |
| Stage 1 says SARS-CoV-2 is the only pathogen with DMS, convergence, and structure 3-layer GT | 12 | Same page says 6 pathogens have complete A+B+C; Table 9 lists B and C for 6 pathogens | **No - internal contradiction/overstatement.** |
| Stage 1 DMS top 20%, 7 functional regions, 1,251 nt | 12 | Easy guide source lines ~403-407 | Yes |
| MutClust-Hybrid hotspot-score 0.778; random baseline about 0.018; about 43x | 12 | Easy guide source lines ~409-412 | Yes; 0.778/0.018 approx 43 |
| Stage 2 v1 retained as 1 of 14 detector families; v2c H-score only | 14 | Easy guide source lines ~413-415 | Yes |
| Hotspot-score formula = (recall + precision + stability)/3 | 14 | Easy guide source lines ~419-422 | Yes |
| Recall example 15/25=0.60; Precision example 15/100=0.15 | 14 | Arithmetic check | Yes |
| Stability = 80% subsampling, 100 repeats, Jaccard | 14 | Easy guide source lines ~427-429 | Yes |
| HDBSCAN-Auto F1=0.146, recall=0.944, stability=0.788 | 14 | Easy guide source lines ~433-435 | Yes |
| Stage 2 20 scoring types x 14 families / 39 variants x 11 pathogens = 8,580 evaluations | 14 | v229 anchor 8,580; arithmetic is 20 x 39 x 11 | Yes, but wording should clarify variants drive 8,580 |
| Scoring category counts: 3+3+4+3+5+2 = 20 | 14-15 | Table on p15 | Yes |

## 2. 명확성 (clarity)
- Issues: Page 15 is too dense for an "easy guide." Terms such as `pseudo-perplexity`, `log-likelihood ratio`, `Bayes factor`, `SASA`, `BLOSUM62`, `ESMFold pLDDT`, and `EVE fitness` appear in a compact table/footnote with little plain-Korean scaffolding.
- Page 12's Stage 1 list is rendered inline ("1. DMS ... 2. synthetic ... 3. 7 regions") and is hard to parse. It should be a real list.
- Page 14 explains recall/precision/stability well. This is the strongest plain-language section in the chunk.
- "DMS = 실험실에서 직접 확인한 생물학적 사실" is clear but slightly too strong because DMS assays are phenotype/cell-line-specific. Better: "실험 조건에서 직접 측정한 기능 근거."

## 3. 일관성 (framing consistency)
- Wet-lab triage framing is mostly respected. The chunk discusses benchmarks, cross-validation, and candidate prioritization; it does not claim a deployable detector.
- Major consistency issue: page 12 says SARS-CoV-2 is the only pathogen with all three GT layers, while the same page correctly says 6 pathogens have complete A+B+C. This should be softened to "Stage 1 당시/가장 데이터가 풍부한 기준 병원체" or "가장 풍부하고 잘 검증된 병원체."
- Layer C is presented as independent validation in methods, but not yet as the primary practical anchor. In v229, Layer C 6/11 plus HIV-1 7.19x are the practical anchors; this chunk gives only the coverage count and omits the 650/MCC 0.139-0.322 anchor.
- HIV-1 7.19x anchor is not in this chunk, so there is no inconsistent HIV-1 wording here.

## 4. 누락 (missing anchors)
- Missing where relevant: Layer C should be printed with the current v229 anchor: 6/11 pathogens, 650 positions, best Layer C MCC 0.139-0.322. This chunk is the natural place because it introduces Layer C and Table 9.
- Missing local caveat: Layer C assays differ by phenotype and cell line; the "생물학적 사실" wording would benefit from one sentence noting this is direct experimental evidence but not universal in-vivo truth.
- HIV-1 7.19x and omega2=0.296 are not required on pages 11-13, but page 14 introduces Stage 2 and could foreshadow omega2=0.296 as the later result. Not a defect if the result section covers it later.

## 5. 잉여 (redundancy)
- The Layer C availability point is repeated on pages 11 and 12, but not wastefully; it supports Table 9 and the "why include incomplete pathogens" explanation.
- Page 12 repeats "6 pathogens" and "11 pathogens" several times in close proximity. This is acceptable, but the paragraph can be shortened by merging the DMS availability sentence with the "complete A+B+C" sentence.
- Page 15 footnote is overloaded. It would read better split into three short bullets with one-line "why proxy?" explanations.

## 6. 시각적 (layout)
- Page 11 Table 8 and the start of Table 9 render cleanly.
- Page 12 Table 9 continuation renders correctly; the page break is acceptable and the HCV footnote is visible.
- Page 13 figure is present and generally readable, but the caption text says only blue Layer A and green Layer B are mapped; the figure and page 11 lead-in include Layer C, and the legend shows orange Layer C. Caption should explicitly mention orange Layer C.
- Page 13 figure labels are small; acceptable in PDF view but marginal for printed reading.
- Page 15 table has a serious layout problem: narrow columns cause awkward wrapping (`entropy_with_indel`, `stability_structural`, `log-likelihood ratio`, BLOSUM62/pLDDT text). It is readable but not polished and undermines the easy-guide goal.
- Page 15 footnote is cut mid-sentence at page bottom ("EVEscape 원..."). This is a page-break issue; the note should move or be shortened.

## TOP 5 fixes
1. Update Table 9 Layer C counts to v229/current CSV: SARS-CoV-2 247, H3N2 112, HIV-1 48, RSV 101, Rabies 87, EV-A71 55; add total 650 if space permits.
2. Fix page 12 contradiction: replace "3층 GT를 모두 갖춘 유일한 병원체" with "가장 데이터가 풍부한 기준 병원체" or equivalent.
3. Add the Layer C practical anchor near Table 9: "6/11 pathogens, 650 positions, best Layer C MCC 0.139-0.322" and keep it framed as wet-lab triage evidence.
4. Revise Figure 2 caption to include orange Layer C and align with the legend.
5. Reformat page 15 scoring table/footnote: use smaller font, landscape/longtable, or split into category subsections so terms do not wrap awkwardly and the footnote does not break mid-sentence.

RESULT_EASY_GUIDE_AUDIT_p11_15: critical=0 major=3 minor=5 visual_issues=3
