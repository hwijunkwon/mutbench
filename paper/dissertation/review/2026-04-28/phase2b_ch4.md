# Ch4 Results 심층 검토

대상: `/proj/paper/paper/dissertation/chapters_en/ch4_results.tex` (972 lines)
검토일: 2026-04-28
방법: 라인 단위 텍스트 검토 + 18개 figure 시각 검사 + 수치 일관성 매트릭스(abstract / ch1 / ch5 / ch6 cross-check)

---

## Critical (수치 불일치 / 잘못된 해석)

| ID | 위치 | 문제 | 근거 | 수정 |
|---|---|---|---|---|
| C-1 | Figure caption line 104 (`dms_evaluation_top.png`) | 캡션: "Jaccard similarity = 0.006 between functional and DMS-escape positives". 그러나 본문 line 60은 같은 0.006을 "DMS-escape and convergent evolution" 간 값으로 정의하고, `multi_ground_truth_bottom.png` 그림 (C) 패널의 overlap matrix 역시 functional×DMS-escape = **0.150**, DMS-escape×Convergent evol = **0.006** 임을 직접 보여줌. | 본문/그림과 캡션이 직접 충돌. 그림(C)의 Jaccard 행렬 수치. | 캡션을 "Jaccard similarity = 0.006 between DMS-escape and convergent evolution positives"로 수정. |
| C-2 | Figure ref/text mismatch — `cross_pathogen_comparison.png` (line 210–217) | 본문 line 210은 "Figure는 top-5 scoring-type MCC across all 11 pathogens"이라 하고 직후 "MCC-best scoring type per pathogen (from Table~\ref{tab:stage2_best})"로 11개 best를 나열함(SARS-CoV-2 = Tranception, HIV-1 = entropy 등). 그러나 그림은 명백히 **mean MCC** 기준(SARS-CoV-2 top = "FUBAR pos" ≈ 0.078, HIV-1 top = "EqualWeight" ≈ 0.078)이며 Table 4.5의 best-MCC(SARS-CoV-2 0.211, HIV-1 0.275)와 전혀 다른 스케일. 즉 이 그림은 "per-pathogen best"가 아닌 "scoring별 detection-평균 MCC의 top-5"를 보여줌. 본문이 그림을 "best-per-pathogen 시각 증거"로 인용한 것은 misread 가능. | `cross_pathogen_comparison.png` (시각 검사) 및 line 210, line 215 caption 비교. SARS-CoV-2/HIV-1/HCV 패널의 1위 scoring과 Table 4.5 best 불일치. | (a) 캡션을 "Mean MCC across detectors per scoring × pathogen"로 명시; (b) 본문 인용을 "Table 4.5는 best 대비 MCC, 그림은 mean MCC—두 시각이 일관되게 pathogen-별 다양성을 보임"으로 수정; **또는** (c) 그림을 best-MCC top-5로 재생성. |
| C-3 | Figure 4.5 `stage3_anova_decomposition.png` (line 385–388) | 캡션: "A within-cell residual ω² ≈ 0.39---accounting for the unmodeled three-way interaction and parameter-variant noise---is shown for reference." 그러나 그림에는 6개 modeled effect bar만 있고 0.39 잔차 막대/주석은 **없음**. 캡션이 그림에 없는 정보를 "shown"이라 주장. | 그림 시각 검사 결과 6개 막대(0.013~0.296)만 존재; 잔차 표현 부재. | 캡션을 "is reported separately in the text"로 수정하거나, 그림에 회색 reference bar(ω²=0.39)를 추가 렌더링. |

---

## Major (논리/통계 해석 약점)

| ID | 위치 | 문제 | 근거 | 수정 |
|---|---|---|---|---|
| M-1 | line 427 footnote / line 444 자기인용 불일치 | line 427: "0/11 exact-match rate is itself not unexpected given **780** unique scoring–detection combinations". line 444: "with **280** combinations and 11 pathogens, P(matches=0) ≈ 0.96". LOPO arithmetic은 (line 427 footnote에서 명시) **family-level 280**을 사용. line 427 본문이 780을 인용하는 것은 framing 오류 또는 독자 혼란 유발. | line 427 본문 vs line 427 footnote vs line 444. | line 427을 "given 280 family-level combinations (footnote)"로 수정해 일관성 확보. |
| M-2 | Friedman test 표시 (line 433–446) | "χ²=7.69, p=0.990, W=0.037, not statistically significant"만 보고. 그러나 **n=11 블록**에서 Friedman의 검정력은 매우 낮음 — 이 caveat는 ch5 line 319에 있으나 Ch4 본문에는 부재. 결과적으로 부정 결과(Friedman 비유의)를 단순 보고. | line 437 W=0.037, line 446 "weaker evidence than the surface reading suggests"는 LOPO 한정 캐비엇만 다룸; Friedman power 한계는 미언급. | "Note that Friedman's power with n=11 blocks is limited; the non-significance is consistent with both universal poor performance and pathogen-dependent rankings"를 line 438 직후에 1문장 추가. |
| M-3 | Permutation null calc 가독성 (line 300, 444–445) | line 300: "Pr(11 unique by chance from 780 combos) ≈ 0.932 (≈93%)". line 444–445: "P(matches=0) ≈ 0.96 at 280 combos". 이 두 개는 다른 사건(11 픽이 모두 distinct vs LOPO 매치 0)의 확률이지만 본문에서 이 차이를 명시하지 않음. 독자는 두 0.93/0.96이 같은 사건인 줄 오인. | line 300 ("uniqueness 11/11"), line 444 ("matches=0 in LOPO"). | 한 사건이 "11개 모두 distinct"인지 "LOPO 매치 0"인지 명시(2문장 차이). |
| M-4 | line 460 random baseline 비교 ("MCC > 0.001 SD≈0.003 by 41 SD") | "best single combo MCC=0.124, vs random baseline mean=0.001 SD=0.003, 41 standard deviations above"라 보고. 그러나 random baseline의 정의(per-pathogen random 또는 single random 적용 후 평균)가 같은 페이지 line 445의 random null(+0.017, SD≈0.034)과 매우 다름. 두 random baseline이 다른 정의로 계산되어 독자 혼란. | line 445 vs line 460의 random baseline mean/SD 차이. | line 460의 random baseline을 명시적으로 정의(예: "uniform random position selection 1000 trials, each pathogen 평균 후 11-pathogen mean of means")하거나 line 445의 통일된 null 사용. |
| M-5 | 그림 `feature_importance_grid.png` 가독성 | 12개 panel (11 pathogens) 그리드의 텍스트(중요도 값, feature label) 폰트가 매우 작아 인쇄 시 read-back 어려움. 또한 Dengue panel의 1위는 figure caption(line 701)이 "homoplasy for Norovirus and Dengue"라 주장하나, Dengue panel의 1위 feature를 정확히 읽기 어려움(시각상 pLDDT 또는 homoplasy 모두 가능하게 보임). | figure 시각 검사. | (a) panel size 확대 또는 단일 best feature를 caption에 표 형식으로 명기; (b) 또는 본 figure를 부록으로 이동하고 본문에는 best-feature-per-pathogen 막대 그림으로 대체. |
| M-6 | 그림 `cross_pathogen_comparison.png` 텍스트 가독성 | 11개 sub-panel × 5개 막대마다 작은 numeric label(0.078, 0.066 등)이 읽기 어려움. 인쇄 1열 폭에서는 사실상 판독 불가. | figure 시각 검사. | 폰트 크기 확대 또는 panel 간격 조정. |
| M-7 | LOPO permutation null & 결론 충돌 (line 442–446) | "0.265 gap is consistent with, but not statistically distinguishable from, a null in which training-based selection provides no cross-pathogen transfer" — 이 발언은 본문의 "Contribution 2 (pathogen-dependent optimality)"의 LOPO 증거를 사실상 무효화. 그러면서도 line 446에서 ANOVA + HIV-1 anchor가 결론을 지탱한다고 함. 결론은 유지되지만, 독자는 "LOPO는 null과 구별 불가"라는 강한 admission을 만나면 contribution 2의 LOPO 부분은 사실상 zero-info 임을 인정한 셈. abstract/ch1/ch6에서 LOPO 0/11을 어떻게 자리매김했는지 일관 점검 필요. | abstract line 10 "LOPO yields 0/11 ... null-consistent under permutation". ch1 line 145, line 148 "LOPO 0/11 is reported as null-consistent corroboration of the interaction effect, not as independent evidence". ch6 line 13 동일. **모든 위치에서 일관됨.** | (작은 인지 부담 외) 일관성은 OK. 다만 Ch4 본문 contribution 2 narrative에서 LOPO를 "primary evidence"가 아닌 "corroboration"으로 명시할 것(이미 line 565에서 처리됨—추가 수정 불필요). |
| M-8 | H3N2 9.36×와 4.012×의 cherry-pick 우려 | Table 4.10 H3N2 row: 본문이 9.36×만 헤드라인으로 자주 인용(line 13 fbox, line 873)하지만 4.012× ($p=0.0023$)의 EqualWeight도 동등 비중으로 보고하지는 않음. 4.012×는 Layer-A-disjoint novel positions 평가에서 사실상 더 신뢰 가능한 enrichment이지만, 헤드라인은 9.36×가 차지. | line 13 ("HIV-1 7.19×, H3N2 9.36×"), line 873 (Table 9.36×), line 893 (4.012× 보조 언급). | line 13 fbox에 H3N2 9.36×를 "self-consistency check"로 명시(현재 SARS-CoV-2만 "exploratory"로 라벨됨). |

---

## Minor

| ID | 위치 | 문제 | 수정 |
|---|---|---|---|
| Mi-1 | line 226 | "ρ = -0.876, p = 1.28 × 10^{-64}" — 수치 자체는 일관되나, 100 replicates × N=500 simulation으로 어떻게 p<10^-64가 나오는지(sample size, test type) 본문에서 명시되지 않음. | "Spearman rank test on N=… correlations across 100 replicates" 등 검정 단위 1줄 추가. |
| Mi-2 | line 415 (Table 4.6) | "Permutation null P(matches = 0) at 280 combinations ≈ 0.96" — 이 0.96이 어떻게 계산되었는지(10,000 resample) line 443에서야 등장. Table footnote에 동일 정보 1줄 추가하면 self-contained. | Table 4.6 mini-page footnote에 "(10,000 random-combo permutations)" 추가. |
| Mi-3 | line 247 ("Stage 2 uses MCC rather than hotspot-score") | hotspot-score를 stage 1에서 사용했다가 stage 2에서 MCC로 전환한 이유는 명시되었으나, 두 metric 간 어떻게 비교 가능한지에 대한 직접 표/식이 없음. 읽기 흐름 끊김. | "Mapping between hotspot-score and MCC is provided in Section X" 또는 footnote 추가. |
| Mi-4 | line 230 (Stage 1 phylo summary) | "frequency-based scores systematically conflate founder effects with positive selection" — 후속 chapters/section 어디서 이 문제를 stage 2 결과 해석에 반영했는지 cross-ref 필요. | "(see Section~\ref{subsec:9pathogen_best_combos}, SARS-CoV-2 Tranception rationale)" cross-ref 추가. |
| Mi-5 | line 488 ("effective number of independent units is closer to ... 3,080 than N=8,580") | 좋은 정직한 limitation, 다만 ANOVA F-test의 sensitivity가 어떻게 변하는지(예: F-stat 재계산) 부재. 결과는 "indicative effect sizes"라 함. | "Re-running ANOVA at N=3,080 cell-aggregate scale yields ω²(scoring × pathogen) = X (vs 0.296 at N=8,580)" 1줄 추가하면 더 강한 evidence. (이미 ch5 line 290에 cell-level 0.234가 보고됨; ch4에 forward-ref 추가하면 됨) |
| Mi-6 | line 493 ("Precision@k Analysis") | Table 4.7의 column "n_det"는 detection size(검출된 positions 수). MERS=200으로 "perfect recall"을 얻었지만 precision=0.045. 즉 거의 무차별 검출. 이 한계를 본문에서 명시 — 현재 line 524는 "MERS shows precision 0.045 with perfect recall"만 언급. | "(MERS recovers all 9 Layer A positions only by detecting 200 positions, i.e., 22% of the 1,330 AA protein, indicating threshold/parameter saturation)" 보강. |
| Mi-7 | Table 4.10 caption (line 865) | "20 scoring × 39 detectors" = 780 combinations. Bonferroni correction은 caption에서 "across 780 combinations"라 명시되나, 일부 분석은 280 family-level combinations 사용. line 886의 footnote는 780만 언급. | Bonferroni denominator 적용 시 정확히 780(detector-variant)인지 확인하고, family-level 분석과 다름을 cross-ref. |
| Mi-8 | line 802 ("4 features ≈98% (97.6%) ... no paired-sample significance test was performed") | "numerically equivalent rather than statistically indistinguishable" 기술은 정직함. 그러나 abstract line 11과 ch6 line 14는 단순히 "97.6%" 값만 헤드라인으로 사용 — 같은 정직 caveat가 abstract/ch6에 누락됨(현재 ch4만 정직). | abstract/ch6에 "(numerical equivalence under uniform-weight LOPO; no paired-sample significance test)" 단서 추가. |
| Mi-9 | line 886 caption Bonferroni 수치 | "HIV-1 $p_{\text{adj}} = 2.47 \times 10^{-16}$"; abstract/ch6 본문은 "$2.5 \times 10^{-16}$"로 라운딩. 차이는 표시 정밀도 issue. | 단일 라운딩 정책(예: 모든 곳 "2.5e-16")으로 통일. |
| Mi-10 | line 947 (PAHD-R section) | "selective callability reached callable-only exact MCC 0.2742, ±10 MCC 0.7276, Precision@20 0.3500, FPR 0.0354 while accepting only 4 of 9 pathogens" — pathogen 11개 panel인데 "9"라는 숫자가 등장. 다른 분석은 11 또는 12(Zika 포함)임. | "9 of 9 PAHD-R-applicable pathogens" 또는 "9 (HCV/SARS-CoV-2/MERS/RSV/H3N2/HIV-1/Norovirus/Dengue/Influenza B 등)"으로 의미 명시. |
| Mi-11 | line 893 H3N2 EqualWeight 위치 인용 | "positions 137, 155, 159, 160, 186, 188" = 6 positions / 29 antigenic sites. Table 4.10에 "6/29"로 일관. ✓ | 일관 — 수정 불필요. |
| Mi-12 | line 467 (subsampling 0.054–0.058 / "core 11 baseline 0.093") | 본문 line 854 "core 11 baseline 0.093"; line 854 vs line 467(0.054–0.058) — line 467은 stage 2 single-combo baseline이지만 line 854는 EqualWeight baseline. 두 baseline은 다른 metric(전자: 모든 combo 평균; 후자: EqualWeight 평균). 헷갈림. | 각 baseline의 정의를 1줄 footnote 추가. |
| Mi-13 | line 60 / line 104 외 — 본문 검토 누락 figure | 검토 spec에 명시된 18개 figure 중 ch4에 실제 사용된 것: 16개. 누락 2개(`genome_hotspot_map`, `gt_distribution_11pathogens`)는 ch3에서 사용됨. 이는 spec issue지 ch4 issue 아님. | 수정 불필요. |

---

## 수치 일관성 매트릭스

| 핵심 수치 | abstract | ch1 | ch4 | ch5 | ch6 | 일치? |
|---|---|---|---|---|---|---|
| ω²(scoring×pathogen) = 0.296 | ✓ line 2/10 | ✓ line 114/145/148 | ✓ line 11/303/368/394 | ✓ line 70/82/93 | ✓ line 12/89 | **OK** |
| 95% CI [0.195, 0.333] | ✓ line 2/10 | ✓ line 148 | ✓ line 11/176/394/488 | ✓ line 290 | ✓ line 12 | **OK** |
| 6-cat aggregation ω² = 0.103 | ✓ line 10 | ✓ line 148 | ✓ line 396 | ✓ line 281/93 | ✓ line 12 | **OK** |
| within-cell residual ω² ≈ 0.39 | ✓ line 10 | — | ✓ line 11/361/386/390 | ✓ line 279 | — | OK (abstract+ch4+ch5만 사용; ch1/ch6는 미사용 일관) |
| LOPO 0/11 | ✓ line 10 | ✓ line 145 | ✓ line 12/411/427/565 | ✓ line 155/164/319/321 | ✓ line 13 | **OK** |
| oracle-vs-generalized gap = 0.265 | ✓ line 10 | ✓ line 195 | ✓ line 301/394/414/440/445/565 | ✓ line 195/319/321 | ✓ line 12 | **OK** |
| Friedman χ²=7.69, p=0.990 | ✓ line 10 | ✓ line 147 | ✓ line 394/434/566 | ✓ line 319 | — | OK (ch6 미언급은 acceptable 요약) |
| HIV-1 7.19× full set | ✓ line 2/11 | ✓ line 117/153 | ✓ line 13/874 | ✓ line 161 | ✓ line 15/90 | **OK** |
| HIV-1 Bonferroni p_adj = 2.5e-16 | ✓ line 2 (2.5e-16) | ✓ line 153 (2.5e-16) | ✓ line 886 (2.47e-16) | ✓ line 161 (2.5e-16) | ✓ line 15 (간접) | **수치 차이(2.47 vs 2.5)는 라운딩**, 정책 통일 권장 (Mi-9) |
| HIV-1 novel-only 7.16–8.24× | ✓ line 11/14 | ✓ line 150/153 | ✓ line 886 | — | — | OK |
| HIV-1 novel-only Fisher p=5.0e-12 | ✓ line 11/14 | ✓ line 150/153 | ✓ line 886 | — | — | OK |
| H3N2 9.36× (full overlap) | ✓ line 11 | — | ✓ line 13/873/893/921/971 | ✓ line 161 | — | OK |
| H3N2 69% Layer A overlap | ✓ line 11 | — | ✓ line 886/921/971 | ✓ line 161 | — | OK |
| H3N2 novel-only 7.19× p=0.132 | — | ✓ line 153 | ✓ line 893/971 | — | — | abstract/ch6 미언급은 의도적 — OK |
| SARS-CoV-2 7.63× exploratory | ✓ line 11 | — | ✓ line 13/875 | ✓ line 161 | ✓ line 15 (간접) | **OK** |
| 4-feature 97.6% (≈98%) | ✓ line 11/14 | ✓ line 150/152 | ✓ line 801/961/971 | ✓ line 196/244 | ✓ line 14 | **OK** |
| H3N2 enrichment 4.012× p=0.0023 | ✓ line 11/14 | ✓ line 153 | ✓ line 878/893/962 | ✓ line 162 | ✓ line 14 | **OK** |
| N = 8,580 | ✓ line 2 | — | ✓ line 7/242/257/394/486/489/970 | ✓ line 290 | — | **OK** |
| best MCC range 0.196–0.660 | — | — | ✓ line 330/440/577 | — | — | OK (ch4-국지) |
| Mean precision 0.338 / recall 0.552 / MCC 0.341 | — | — | ✓ line 518/524 | — | — | **계산 검증 OK** (재계산 일치) |
| H3N2 Wavelet detector | — | — | ✓ line 281 (t=1.5) / line 873 (t=2.0) | — | — | **차이 있음 — Layer A best vs escape best 다름 — line 891에서 explicit 설명 OK** |

전반적으로 수치 일관성은 매우 양호. 단일 라운딩 차이(2.47e-16 vs 2.5e-16) 및 H3N2 detector parameter (t=1.5 vs t=2.0)만 주의 사항.

---

## 그림 검증 결과

| 그림 | 본문 참조? | 데이터 범위 | 가독성 | 캡션 정확? | 기타 |
|---|---|---|---|---|---|
| `multi_ground_truth_top.png` | line 85, 91 | OK (F1 0–0.5, enrichment 1–3.5×) | 양호 | ✓ | A/B 패널 라벨 명확 |
| `multi_ground_truth_bottom.png` | line 85, 99 | OK (Jaccard 0–0.3, sizes 29–439) | 양호 | ✓ | (C) 판넬에서 0.006 위치 = DMS-escape×Convergent evol |
| `dms_evaluation_top.png` | line 85, 105 | OK (F1, Cohen's d) | 양호 | **C-1 오류** — Jaccard 0.006 텍스트가 잘못된 페어 |
| `dms_evaluation_bottom.png` | line 85, 112 | OK (산점도 + PR) | 보통 (산점도 잘 안 읽힘) | ✓ | (C) 산점도 컬러 점 분포 매우 dense |
| `sample_size_convergence.png` | line 188 | OK (HS 0.55–0.65) | 양호 | ✓ | "1K"에서 plateau 명확 |
| `sensitivity_heatmap.png` | line 195 | OK (F1 0.175–0.792) | 양호 | "64 combinations" 보고이나 그림은 16 cells (4γ × 4d, MinPts averaged) — 캡션이 명시 | OK (averaged over minpts 그림 제목에 명시) |
| `cross_pathogen_comparison.png` | line 213, 216 | mean MCC 0.005–0.30 정도 | 작은 텍스트, 인쇄 시 가독성 부족 | **C-2 오류** — best 대 mean 혼란 | M-6 가독성 |
| `stage3_scoring_pathogen_heatmap.png` | line 305, 309 | OK (mean MCC −0.115 to +0.303) | 양호 | ✓ "best MCC across detection families" — 이건 mean이 아닌 max across detectors. 본문은 line 308에서 정확히 "best MCC across all detection families for a given scoring–pathogen combination"라 명시 ✓ | heatmap의 max가 0.303 (HCV+dnds_proxy) vs Table 4.5 HCV best 0.660 — 그림이 보여주는 것은 각 cell의 best (across detection families)이지만 0.660이 보이지 않음. 시각상 혼란. |
| `stage3_scoring_category_bar.png` | line 334, 338 | mean MCC −0.01 to +0.04 | 양호 | ✓ | error bar 매우 큰 폭 — 본문에서 "large per-pathogen variation" 강조 |
| `stage3_fubar_spotlight.png` | line 342, 345 | MCC 0.07–0.66 | 양호 | ✓ H3N2 별표 위치 정확 | 그림 자체는 표 4.5와 일치 |
| `stage3_anova_decomposition.png` | line 384, 388 | ω² 0.013–0.296 | 양호 | **C-3** — caption은 잔차 0.39 "shown" 주장하나 그림에 부재 |
| `stage3_lopo_crossval.png` | line 421, 424 | MCC −0.25 to +0.65 | 양호 | ✓ gap 주석 정확 (mean = 0.265 재계산 일치) | predicted MCC가 음수인 pathogens (HCV, EV-A71, RSV, Rabies) 시각 명확 |
| `feature_auc_heatmap.png` | line 671, 674 | AUC 0.16–0.94 | 양호 | ✓ | Table 4.6와 모든 값 일치 |
| `feature_correlation_heatmap.png` | line 733, 736 | ρ −0.19 to +1.00 | 양호 | ✓ | freq–entropy 0.97, freq–dN/dS 0.87 본문 일치 |
| `feature_importance_grid.png` | line 699, 702 | importance 0–0.35 | **M-5 가독성 부족** — 11개 panel 텍스트 매우 작음 | ✓ (Dengue panel 1위 식별이 시각상 어려움) |
| `feature_ablation_bars.png` | line 763, 766 | ΔMCC −0.028 to +0.004 | 양호 | ✓ Homoplasy −0.028, ESM-2 +0.004, SASA +0.003 본문 일치 |
| `genome_hotspot_map.png` | (ch3에서 사용) | (ch4 무관) | — | — | spec 외 항목 — 검토 무관 |
| `gt_distribution_11pathogens.png` | (ch3에서 사용) | (ch4 무관) | — | — | spec 외 항목 — 검토 무관 |

요약: 18개 figure 중 ch4 본문에서 실제 인용되는 것은 16개. 그 중 **3개는 캡션-본문/그림 mismatch (C-1, C-2, C-3)**, 2개는 가독성 개선 필요 (M-5, M-6).

---

## 챕터 종합 평가

**합격선: CONDITIONAL (조건부 합격)**

### 이유

**강점**
1. 수치 일관성은 abstract/ch1/ch5/ch6/figure caption 사이에서 매우 높음(20+ 핵심 수치 cross-check 모두 일치).
2. 부정 결과(LOPO 0/11 null-consistent, Friedman p=0.990, novel-only H3N2 p=0.132, 4-feature paired-test 미실행) 모두 본문에서 정직하게 보고. cherry-pick 우려 낮음.
3. 통계 검정 + ranking 결합이 거의 모든 결과에 동반 (ANOVA + cluster bootstrap, LOPO + permutation null, vaccine escape + Fisher exact + Bonferroni).
4. circularity audit (line 920–921)가 H3N2/SARS-CoV-2/HIV-1 enrichment를 self-consistency vs external evidence로 구분, 외부 anchor를 HIV-1로 명시 — 정직하고 균형적.
5. 3개 figure–caption 오류 (C-1, C-2, C-3)는 모두 **수정 가능** (텍스트/렌더 1회 수정으로 해결).

**약점 (조건부 합격 사유)**
1. **C-1**: figure caption이 잘못된 ground truth 페어를 명시(0.006이 functional×DMS-escape라고 잘못 적힘). 학위 심사에서 "수치 부주의"로 지적될 수 있음 — 즉시 수정 필요.
2. **C-2**: `cross_pathogen_comparison.png` 그림은 mean MCC, 본문 인용은 best MCC framing — 외부 reviewer가 "그림이 결과를 misrepresent"라고 지적할 가능성.
3. **C-3**: 캡션이 그림에 없는 정보를 "shown"이라 주장.
4. **M-2**: Friedman p=0.990 보고 시 n=11 small-block power 한계가 ch4 본문에 없음(ch5에는 있음) — chapter-level self-containment 부족.
5. **M-5/M-6**: 2개 figure 가독성이 인쇄 1열 폭에서 부족.

**수정 우선순위**
1. **즉시 (Critical)**: C-1, C-2, C-3 — 1시간 작업.
2. **권장 (Major)**: M-1 (footnote 280/780 일관), M-2 (Friedman caveat 1줄), M-5/M-6 (figure 폰트), M-8 (H3N2 self-consistency 라벨 fbox 반영).
3. **선택 (Minor)**: 라운딩 통일(Mi-9), random baseline 정의 명시(M-4/Mi-7), 등 ~10건은 시간 여유 시.

C-1/C-2/C-3 수정 후 무조건적 합격(PASS) 가능. 미수정 상태로는 학위 심사에서 "figure caption 수치 오류"가 1차 지적사항으로 등장할 위험.

---

## 부록: 라인별 핵심 인용

- L11: "scoring × pathogen interaction (ω² = 0.296)" — abstract/ch1/ch5/ch6 모두 일치.
- L60: "Jaccard similarity between DMS-escape and convergent evolution = 0.006" (정확).
- L104: "Jaccard similarity = 0.006 between functional and DMS-escape positives" — **❌ C-1**: 페어 오류.
- L210, L215: cross_pathogen_comparison "best per pathogen" framing — **❌ C-2**: 그림은 mean.
- L300: "P(11 unique by chance) ≈ 0.932" (780-combination calc).
- L386: "within-cell residual ω² ≈ 0.39 ... shown for reference" — **❌ C-3**: 그림에 부재.
- L427: "given 780 unique scoring–detection combinations" — **❌ M-1**: 280을 의도한 듯하나 780 인용.
- L444: "with 280 combinations, P(matches=0) ≈ 0.96".
- L445: "0.265 gap ... not statistically distinguishable from null" — 정직한 admission.
- L488–489: cluster vs naive bootstrap CI 비교 — 모범적 정직성.
- L518: Mean precision 0.338, recall 0.552, MCC 0.341 — 재계산 일치.
- L802: "no paired-sample significance test was performed" — 정직, abstract/ch6 단서 추가 권장 (Mi-8).
- L886: HIV-1 p_adj = 2.47e-16 vs abstract/ch1/ch5의 2.5e-16 — 라운딩.
- L920–921: circularity audit, HIV-1 외부 anchor 명시.

---

검토 종료 (2026-04-28).
