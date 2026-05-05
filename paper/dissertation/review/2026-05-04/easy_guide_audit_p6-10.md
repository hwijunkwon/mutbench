# Easy Guide Audit p6-10

## 1. 정확성 (numbers)
| Statement | Page | dissertation source | Match? |
|---|---:|---|---|
| EVEREST v3 = 2026 Jan, ViroGym = 2026 Mar | 6 | easy guide md lines 181-194 | Match within source; external recency not rechecked. |
| ViroGym 13, EVEREST v3 4 forecasting + 40 reliability | 6 | md line 194 | Match. |
| MutBench 11 pathogens | 6-10 | md lines 194, 219, 293-305; `pahd_r_data_processing_pathogen_summary.csv` has 11 rows incl. Rabies/EV-A71 in downstream tables | Match. |
| 핵심 발견: scoring x pathogen omega squared = 0.296 | 6 | md line 191; `cluster_bootstrap_omega_summary.csv` headline = 0.29625198 rounded 0.296 | Match. No stale CI appears in this chunk. |
| HIV-1 vaccine escape enrichment = 7.19x | 6 | md line 192; reference state HIV-1 7.19x | Match. Caveat: wording says "실용적 검증/실용 가능성"; should be "wet-lab triage evidence", not deployability. |
| H3N2 used as auxiliary confirmation | 6 | md line 192; reference state says H3N2 is secondary | Match. |
| Table 4: MutClust 1, Bailey 26, MOSD 10, MutBench 14 families/39 variants | 6-7 | md lines 200-207; Stage 2 design line 298 | Match. |
| Table 4: MutBench uses 11 pathogens and ANOVA+Friedman+LOPO | 7 | md lines 205-207, 299 | Match. |
| 11 RNA viruses selected | 8 | md line 219 | Match. |
| Table 5 sequence counts and lengths: SARS-CoV-2 4,982/753/1,259; H3N2 2,644/2,562/543; Norovirus 1,500/791/536; HIV-1 3,000/2,256/450; Dengue 2,000/796/490; RSV 5,070/4,779/550; Influenza B 5,325/5,019/560; MERS 1,311/530/1,330; HCV 1,362/1,067/340; Rabies 2,038/2,038/491; EV-A71 662/662/261 | 8 | md lines 243-255; lengths also align with `pahd_r_data_processing_pathogen_summary.csv` for n_positions | Match. |
| Table 6 mutation rates: SARS-CoV-2 ~1e-3, H3N2 ~4e-3, Norovirus ~2e-3, HIV-1 ~2.5e-3, Dengue ~7.6e-4, RSV ~1.5e-3, Influenza B ~2e-3, MERS ~9e-4, HCV ~1e-3, Rabies ~4e-4, EV-A71 ~4.5e-3 | 8-9 | md lines 261-271 | Match to source; no local authoritative rate CSV found. |
| Summary says HIV-1 ~1e-3 to Rabies ~4e-4 | 9 | md line 275 vs Table 6 HIV-1 ~2.5e-3 | Minor precision inconsistency: use ~2.5e-3 or say order-of-magnitude. |
| Protein length range EV-A71 261 AA to MERS 1,330 AA; 5.1x | 9-10 | md lines 275, 287; 1330/261 = 5.10 | Match. |
| Unique sequence range MERS 530 to Influenza B 5,019; 9.5x | 9-10 | md lines 279, 287; 5019/530 = 9.47 | Match. |
| All pathogens have >=530 unique sequences | 9 | md lines 243-255, 279 | Match. |
| HCV Oracle MCC 0.660, MERS 0.196 | 9 | md line 279; reference state does not override these page-local difficulty examples | Match to source, but source CSV for "Oracle MCC" not identified in this pass. |
| DNA virus mutation rate exclusion 1e-6 to 1e-8; RNA 1e-3 to 1e-4 | 9 | md line 279 | Broad order-of-magnitude statement; acceptable. |
| MAFFT v7.505, ambiguous N >=5% | 9 | md line 283 | Match to source. |
| Pipeline: 5 steps; 6 categories, 20 scoring types; 14 families, 39 variants; 8,580 evaluations | 9 | md lines 293-308; 20 x 39 x 11 = 8,580 | Match. |
| Stage 1 SARS-CoV-2 1 pathogen, 5 sub-experiments, hotspot-score; Stage 2 11 pathogens, 8,580 evaluations, MCC | 9 | md lines 301-308 | Match. |
| Figure 1 Layer C available in 6/11 | 10 | md line 287; reference state Layer C 6/11 | Match. Missing related anchor: 650 Layer-C positions is not stated here. |
| SARS-CoV-2 Spike 484 example; E484K/A | 10 | md lines 326-328 | Match to source; no numerical issue. |

## 2. 명확성 (clarity)
- Issues: Page 6 is mostly comparison-table dense. "per-variant fitness", "per-region", "forecasting", "reliability" remain partly English and may be hard for the intended Korean non-specialist reader.
- Page 8 is clear overall, but the sentence about nonstructural proteins says Layer A definition is "impossible"; this is strong. "본 연구의 Layer A 기준을 안정적으로 만들기 어렵다" would be safer and easier.
- Page 9 has a dense block in "핵심 고려사항 2" combining statistical power, difficulty spread, and DNA-virus exclusion. Split into 3 shorter bullets.
- Page 10 defines ground truth well. "founder effect" is used before the nearby Korean explanation; add "(창시자 효과)" on first use in this chapter chunk.

## 3. 일관성 (framing consistency)
- The chunk mostly matches the wet-lab triage reframe: MutBench is described as a benchmark and prioritization framework, not a deployable detector.
- Minor issue: Page 6 table label "실용적 검증" and wording "HIV-1 백신 회피 위치를 ... 찾음" can sound stronger than triage. Prefer "실험 검증 우선순위 축소 근거" or "wet-lab triage 근거".
- HIV-1 is consistently the clean external anchor in this chunk; H3N2 is explicitly secondary.
- Layer C is correctly described as optional/independent validation and available for 6/11, but its practical role as the primary wet-lab triage evidence is not emphasized until after page 10.

## 4. 누락 (missing anchors)
- Missing where relevant: Layer C 6/11 appears in Figure 1 caption, but "650 positions" is absent. If this chapter introduces Layer C, adding "6개 병원체 650개 위치" would align with the dissertation-level anchor.
- HIV-1 7.19x and omega squared 0.296 are present on page 6.
- Layer C 6/11 is present on page 10.
- No need to add LOPO 0/11, Friedman p=0.990, HBFWS p=0.78, or Cycle 7B on these pages unless later results are being previewed.

## 5. 잉여 (redundancy)
- No wasteful repeated anchor in pages 6-10.
- Page 8 "표면 단백질" rationale is useful but could be shortened by merging items 2 and 3 because both say antibody/vaccine target.
- Page 9 repeats "11개 바이러스" frequently across section title, paragraph, pipeline, and stage table; acceptable but compressible.

## 6. 시각적 (layout)
- Page 6: Table 3 and start of Table 4 render legibly. Dense but not broken.
- Page 7: Visual issue. Only the tail of Table 4 appears at the top; the rest of the page is blank. This is an obvious page-break/flow problem and should be fixed by keeping Table 4 together or moving it entirely to page 7.
- Page 8: Tables 5 and start of Table 6 render cleanly.
- Page 9: Table 6 continuation and Stage table render cleanly.
- Page 10: Figure 1 and caption match the image content. Figure is small but readable enough; no caption mismatch found.
- Prompt listed PNGs as `p-006.png` etc.; actual files are `p-06.png` etc. Audit used existing files.

## TOP 5 fixes
1. Keep Table 4 together to remove the mostly blank page 7.
2. Change Page 6 "실용적 검증" wording to wet-lab triage / experiment-prioritization language.
3. Add "Layer C: 6개 병원체 650개 위치" when Figure 1 or Layer C is introduced.
4. Harmonize HIV-1 mutation-rate wording: use ~2.5e-3 in the summary or call it an order-of-magnitude range.
5. Split Page 9 "왜 이 11개 바이러스인가?" into shorter bullets for non-specialist readability.

RESULT_EASY_GUIDE_AUDIT_p6_10: critical=0 major=1 minor=5 visual_issues=1
