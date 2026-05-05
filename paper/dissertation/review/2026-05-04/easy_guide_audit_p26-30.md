# Easy Guide Audit p26-30

## 1. 정확성 (numbers)
| Statement | Page | dissertation source | Match? |
|---|---:|---|---|
| FUBAR BF table: SARS-CoV-2 0.044, EV-A71 0.002, HIV-1 0.021, Norovirus -0.011, Dengue -0.037, ranks 3/20 etc. | 26 | `dissertation_easy_guide_v2.md` lines 774-789; current `results/mutbench/stage3_full_results.csv` best-per-`fubar_bf` gives SARS-CoV-2 0.139, EV-A71 0.235, HIV-1 0.214, Norovirus 0.139, Dengue 0.126. | **No / under-specified.** If this is fixed-detector, mean, or another FUBAR statistic, label it. As written, "FUBAR BF 성능" and rank vs 20 scoring reads as best-per-scoring and appears stale. |
| scoring × pathogen ω²=0.296; ANOVA factor values 0.117, 0.082, 0.063, 0.039, 0.013 | 27-28 | `results/mutbench/stage3_statistics.csv`: 0.2962519, 0.1173288, 0.0815037, 0.0630086, 0.0387966, 0.0126229 | Match after rounding. |
| Bootstrap CI [0.201, 0.346], HCV-excluded ω²=0.246 | 27 | Reference state; md line 815-816 | Match reference state. |
| Friedman χ²=7.69, p=0.990, Kendall W=0.037 | 27 | `stage3_statistics.csv`: χ²=7.68797, p=0.98954; md line 827 | Match after rounding. |
| LOPO 0/11, mean generalized MCC 0.032, oracle 0.297, gap 0.265, variant ceiling 0.341 | 27-29 | `stage3_statistics.csv`: match_rate 0, mean_gen_mcc 0.031508, gap source value 0.265424; md lines 834-844 | Match after rounding. |
| Layer A vs Layer C table: SARS 0.186, H3N2 0.245, HIV-1 0.139, RSV 0.180, Rabies 0.182, EV-A71 0.322 | 29 | `results/mutbench/layer_c_evaluation.csv`; md lines 850-861 and 1328-1337 | Match, but the following sentence is stale. |
| "6개 DMS 병원체 중 5개에서 Layer A와 Layer C의 최적 scoring이 서로 달라" | 29 | md lines 1324-1337: 6/11 Layer C pathogens; all 6 have Layer A optimum != Layer C optimum | **No.** Should be "6개 모두" and should reinforce Layer C 6/11 as wet-lab anchor. |
| HIV-1 vaccine escape 7.19배, Bonferroni p=2.5e-16 | 29 | reference state; md lines 869, 964 | Match. |
| Best single-feature AUC table: Norovirus 0.944, Flu-B 0.805, H3N2 0.787, Dengue 0.770, HIV-1 0.730, MERS 0.695, HCV 0.680, SARS 0.586, RSV 0.561 | 30 | `results/mutbench/feature_analysis/per_feature_auc_11pathogens.csv` | Match for listed rows. Rabies 0.650 and EV-A71 0.596 are omitted, but not numerically wrong. |
| Random Forest CV AUC table values, including MERS 0.875, RSV 0.737, HIV-1 0.802 | 30 | md lines 904-916; figure/source not fully cross-checked in CSV during this audit | Matches markdown source; no CSV contradiction found in scope. |

## 2. 명확성 (clarity)
- Issues: p27 "5-frame 보강 (standard cluster, wild-cluster Rademacher~[?], phylogenetic block..., Bayesian factor analysis HDI...)" is too dense for an easy guide and includes a broken citation marker. Move details to a footnote-style parenthesis or simplify to "다섯 가지 재분석에서도 큰 효과로 유지".
- Issues: p27 LOPO paragraph is conceptually correct but long. Define LOPO in one plain sentence first, then give the null-consistent caveat.
- Issues: p30 Random Forest is introduced without plain explanation. Add "여러 정보를 조합해 어떤 정보가 예측에 많이 기여했는지 보는 방법" before the table.
- Issues: AUC, MCC, ω² are used correctly, but p26-30 assumes earlier definitions. For a standalone easy-guide chunk, add short parenthetical reminders only where first used on these pages.

## 3. 일관성 (framing consistency)
- The section mostly matches the wet-lab triage reframe: it avoids "deployable detector" wording and treats LOPO/Friedman as null-consistent support rather than primary proof.
- Major issue: p29 still makes HIV-1 the "실제 쓸모" headline, while the reference state says practical value should be anchored primarily by Layer C DMS 6/11 pathogens. HIV-1 can remain the cleanest external vaccine-escape anchor, but Layer C should be foregrounded as the wet-lab anchor in the same summary.
- HIV-1 wording is consistent with the clean external-validation framing, but the chunk omits the stronger details: 82% Layer-A-disjoint and 37/45 novel.

## 4. 누락 (missing anchors)
- Missing: Layer C wet-lab anchor is underpowered in prose. The page has the Layer A vs C table, but does not state "Layer C 6/11 pathogens, 650 positions, MCC 0.139-0.322" or that EV-A71 0.322 and H3N2 0.245 are the strongest functional anchors.
- Missing: HIV-1 7.19x appears, but p29 does not include p_adj=2.5e-16 with the Layer-A-disjoint 82% / 37 of 45 novel context. Add one short sentence.
- Present: ω²=0.296 and Friedman p=0.990 are appropriately repeated where relevant.

## 5. 잉여 (redundancy)
- p27-p29 repeats the LOPO null caveat three times: method paragraph, Figure 9 caption, and interpretation. Keep it in the method paragraph and caption; shorten the p29 interpretation to focus on the 0.265 MCC gap.
- p29 Stage 2 summary restates ω²=0.296 immediately after the ANOVA/LOPO pages. This is acceptable as a summary, but can be shortened if Layer C anchor text is added.

## 6. 시각적 (layout)
- Visual issue: figure numbering is inconsistent. p26 body says Figure 10 but caption renders Figure 7; p27 says Figure 12; p28 captions render Figure 8 and Figure 9; p30 says Figure 14 but the heatmap is not shown on p30.
- Visual issue: table numbering is inconsistent. p26 Table 18, p27 text "Table 17" but rendered Table 19, p30 text "Table 19" but rendered Table 21.
- Visual issue: p30 appears to render the AUC heatmap alt/caption text as normal text without the actual figure in this page range. If the figure appears on a neighboring page, the reference should not imply it is visible before the table.
- Tables are readable and not clipped. p27 text block is dense but does not overlap.

## TOP 5 fixes
1. Replace p29 "5개에서 Layer A와 Layer C..." with "6개 모두에서..." and add "Layer C DMS 6/11 병원체, 650 positions, MCC 0.139-0.322" as the practical wet-lab anchor.
2. Recompute or relabel the p26 FUBAR BF table. Against current `stage3_full_results.csv`, several MCC/rank values look stale unless they refer to a fixed detector or non-best aggregation.
3. Fix rendered figure/table numbering references: Figure 10/12/13/14 and Table 17/19 should match the PDF captions or use unnumbered wording ("아래 그림/표").
4. Add HIV-1 anchor context on p29: 7.19x, p_adj=2.5e-16, 82% Layer-A-disjoint, 37/45 novel.
5. Simplify the p27 robustness paragraph and remove the broken `Rademacher~[?]` citation artifact.

RESULT_EASY_GUIDE_AUDIT_p26_30: critical=0 major=4 minor=5 visual_issues=3
