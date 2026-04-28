# CCB 중재 보고서 (Phase 3, 2026-04-28)

검토 대상: MutBench 박사학위 논문 (`abstract.tex`, `ch1`–`ch6`)
입력: Phase 1 블루팀, Phase 2 레드팀(C5/M11/m10) + 통계전문가(10/10 PASS), Phase 2B Ch1–Ch6 (총 Critical 30건)
방법: IV&V (블루/레드/통계 중 어느 한 쪽에 휘둘리지 않고 본문 직접 확인). 인용은 `<file>:<line>`.

---

## 0. 결함 분류 정의

- **(a) 이미 답 있음**: 본문에 caveat/약화/disambiguation이 명시되어 결함 주장 무효
- **(b) 답 부족**: 본문에 부분적 답만 있거나 누락 → 수정 필요
- **(c) 공격 부당**: 결함 주장 자체가 잘못 (근거 부정확 / scope 벗어남)

---

## 1. 통합 결함 목록 (중복 제거)

레드팀 C-level 5건 + Major 11 + Phase 2B Ch1-6 Critical 30건 + 통계 PASS 10건을 통합.
**중복 통합 그룹** 우선 처리:

### 1.1 통합 그룹 (같은 결함이 여러 위치에서 보고)

| 통합ID | 결함 (요약) | 보고 위치 (Phase) | 분류 | 우선순위 |
|--------|-----------|------|------|----------|
| **G01** | 두 ρ 값 (Layer A↔freq point-biserial 0.12 vs entropy↔freq Pearson 0.97) disambiguation | 통계 #9, 레드팀 C-01/M-06, Ch5 C1, 블루 시나리오 5 | **(b) 답 부족** | P0 |
| **G02** | LOPO/Friedman "null-consistent corroboration" 표현의 정직성 vs 위장 | 레드팀 C-02 vs 통계 #4 (충돌!), Ch4 M-7, Ch5 M12, Ch6 M2, 블루 #6 | **(a) 이미 답 있음** (충돌 중재 후) | — |
| **G03** | ω² aggregation 5중 보고 (0.296/0.103/0.234/0.264/0.252) — selective headline | 레드팀 C-04 vs 통계 #1 (충돌!), Ch4 본문, Ch5 L281/285/290/292 | **(a) 이미 답 있음** (충돌 중재 후) | — |
| **G04** | HIV-1 단일 anchor 일반화 + winner's curse | 레드팀 C-03/M-08, Ch5 C4/M3/M8, Ch6 C2, 블루 #1 | **(b) 답 부족** | P1 |
| **G05** | Layer A 정의 비대칭 (curation heterogeneity) → ω² interpretation | 레드팀 C-05, Ch5 C7, 블루 시나리오 5 | **(a) 이미 답 있음** | — |
| **G06** | "broadest" claim의 task-redefinition trivial 1등 의혹 | 레드팀 M-01, Ch1 L142/abstract L4, 블루 약점 | **(a) 이미 답 있음** | — |
| **G07** | 4-feature 97.6%의 paired-test 부재 caveat 누락 (abstract/ch6) | 레드팀 M-05, Ch4 Mi-8, Ch5 C6, Ch6 C4 | **(b) 답 부족** | P0 |
| **G08** | Two-stage vs Stage 3 구조 모순 (ch1 vs ch3) | Ch1 C3, Ch1 m2 | **(b) 답 부족** | P0 |
| **G09** | Ch1 L150 novel-only Bonferroni $p_{\text{adj}}\approx3.9\times10^{-9}$ 출처 미확인 | Ch1 C1 | **(b) 답 부족** | P0 |
| **G10** | Ch1 L153 "7.19×" 두 의미 (HIV-1 full vs H3N2 novel) 한 paragraph 충돌 | Ch1 C2 | **(b) 답 부족** | P0 |
| **G11** | Ch6 Contribution 재진술 약화 (broadest/8580/two-part 누락) | Ch6 C1/C3/M1 | **(b) 답 부족** | P1 |
| **G12** | Ch6 7.19× full vs novel-only 모호 표기 | Ch6 C2 | **(b) 답 부족** | P0 |
| **G13** | Ch6 PAHD-R scope creep (abstract/ch1 부재) | Ch5 M7, Ch6 M4 | **(b) 답 부족** | P1 |
| **G14** | Ch4 figure caption 오류 3건 (C-1 Jaccard 페어, C-2 mean vs best, C-3 잔차 0.39) | Ch4 C-1/C-2/C-3 | **(b) 답 부족** | P0 |
| **G15** | Ch3 재현성: cutoff date / MAFFT 비결정성 / repo URL forward-ref | Ch3 C1/C2/C4 | **(b) 답 부족** | P1 |
| **G16** | Ch3 preregistration 부재 (Layer A/B/C 임계값, Bonferroni 분모 780) | Ch3 C3/C5 | **(b) 답 부족** | P1 |
| **G17** | Ch3 Layer C threshold sweep 4/6 pathogen만 | Ch3 C6, 블루 약점 | **(b) 답 부족** | P2 |
| **G18** | Ch2 MEME/FUBAR 1차 출처 오류 (kosakovsky2020hyphy로 일괄) | Ch2 C1 | **(b) 답 부족** | P1 |
| **G19** | Ch2 OncodriveCLUST↔CLUSTL 명명 불일치 | Ch2 C2 | **(b) 답 부족** | P1 |
| **G20** | Ch2 ESM-3 본문 등장 + 인용 부재 | Ch2 C4 | **(b) 답 부족** | P1 |
| **G21** | Ch2 Greaney escape DMS 시리즈 누락 | Ch2 M3 | **(b) 답 부족** | P1 |
| **G22** | Ch2 EVEscape composite의 EVE→ESM-2 substitution disclaim 부재 | Ch2 C6 | **(b) 답 부족** | P2 |
| **G23** | Ch2 "no detection-task benchmark" gap의 scope-bias | Ch2 C3 | **(b) 답 부족** | P2 |
| **G24** | Ch1 Information-type panel 11 vs 12 (Zika) 충돌 | Ch1 M8 | **(b) 답 부족** | P1 |
| **G25** | Ch1 cancer benchmark 인용 빈약 (bailey2018 단독) | Ch1 M1 | **(b) 답 부족** | P2 |
| **G26** | Ch1 EVEscape/Livesey & Marsh 누락 | Ch1 M4 | **(b) 답 부족** | P2 |
| **G27** | Ch1 youn2025mutclust "core task" 자기 인용 위치 부적절 | Ch1 M3 | **(b) 답 부족** | P2 |
| **G28** | Ch4 Friedman n=11 power 한계 caveat ch4 누락 (ch5에만) | Ch4 M-2 | **(b) 답 부족** | P2 |
| **G29** | Ch4 random baseline SD 0.003 vs 0.034 정합성 (M-10 + Ch4 M-4) | 레드팀 M-10, Ch4 M-4 | **(b) 답 부족** | P2 |
| **G30** | Ch4 H3N2 "9.36×" headline에 self-consistency 라벨 명시 부족 | Ch4 M-8 | **(b) 답 부족** | P2 |
| **G31** | Ch5 NFL "stronger evidence" 일반화 비약 | Ch5 C3, 레드 m | **(b) 답 부족** | P1 |
| **G32** | Ch5 11-cluster Bolker rule-of-thumb 미달 직접 진술 부재 | Ch5 C5 | **(b) 답 부족** | P2 |
| **G33** | Ch5 independent reproduction 한계가 1문장만 (claim별 매핑 없음) | Ch5 C4 | **(b) 답 부족** | P2 |
| **G34** | Ch5 NFL/회로성 chain (정의 비대칭→회로성) cross-ref 부재 | Ch5 C7 | **(b) 답 부족** | P2 |
| **G35** | Ch6 H3N2 9.36× / SARS-CoV-2 7.63× / CI [0.195, 0.333] 누락 | Ch6 M3/M5 | **(b) 답 부족** | P2 |
| **G36** | Ch6 "confirms" → "evidences" 톤 강도 | Ch6 M6 | **(b) 답 부족** | P2 |
| **G37** | 레드팀 C-04(b) 6-cat 0.103 lower bound와 main 0.296 표현 균형 | 레드팀 C-04 | **(c) 공격 부당** (충돌 중재 후) | — |
| **G38** | 레드팀 M-09 "11/11 unique" Influenza B/MERS 동일 (freq+KDE p=85) | 레드팀 M-09 | **(a) 이미 답 있음** (footnote 9 distinct 명시) | — |
| **G39** | 레드팀 m-06 HIV-1 "23/45" 두 의미 (Layer A 23 vs detected∩escape 23) | 레드팀 m-06 | **(b) 답 부족** | P2 |
| **G40** | Ch3 EqualWeight directional sign (LOPO leakage 우려) | Ch3 M8 | **(b) 답 부족** | P1 |

---

## 2. 의견 충돌 중재 (필수)

### 충돌 1: "null-consistent corroboration" 표현 (G02)

**레드팀 입장 (Phase 2 C-02)**:
- ch4:445 자체가 "0.265 gap는 null과 not statistically distinguishable, p≈0.25-0.28"
- Friedman p=0.990은 "no agreement"
- "null-consistent corroboration" 표현은 부정 결과를 긍정 보강 증거로 위장. **윤리 기준 위반**.

**통계 전문가 입장 (Phase 2 통계 #4)**:
- "표현 정확", "정직성 차원 PASS"
- ch4:565 "we therefore report ... and treat LOPO as corroboration of the ANOVA interaction rather than as independent evidence" — independent evidence 아님을 직접 명시
- abstract:10도 "LOPO 0/11 alone is null-consistent under permutation; the conclusion rests on the interaction effect plus the vaccine-escape audit" — load-bearing 증거의 분리 명시.

**CCB 판정**: **(a) 이미 답 있음**

**근거 (IV&V로 본문 직접 확인)**:
- abstract.tex:10 "LOPO 0/11 alone is null-consistent under permutation; the conclusion rests on the interaction effect plus the vaccine-escape audit, not on LOPO in isolation" — 정확
- ch1_introduction.tex:145 "LOPO 0/11 is reported as null-consistent corroboration of the interaction effect, not as independent evidence" — 정확
- ch4_results.tex:565 "treat LOPO as corroboration of the ANOVA interaction rather than as independent evidence" — 정확
- ch4_results.tex:560 "two primary analyses (ω² + HIV-1) plus two null-consistent corroborations (LOPO, Friedman). The four lenses re-parameterize the same dataset and are not independent replications" — 명시

**부당 판정 사유**: 레드팀의 "위장(disguise)" 주장은 본문이 corroboration ≠ independent evidence를 명시적으로 박았다는 사실을 기각한다. 통계 전문가가 옳다.

**예외 (부분 인정)**: ch6_conclusion.tex:13은 "Friedman p=0.990 are treated as null-consistent corroboration"으로 Friedman과 LOPO를 묶어서 표현 — Friedman은 본래 "no universally best"의 의미이지 null-consistent 표현은 LOPO에 한정. 이 부분만 G02 → (b) 답 부족 (Ch6 M2 항목)으로 분리. **수정 권고**: ch6:13을 "Friedman χ²=7.69, p=0.990 shows no universally best combination; LOPO 0/11 is null-consistent under permutation; both are corroborative consistency checks rather than independent evidence" (Ch6 M2 patch).

---

### 충돌 2: ω² aggregation (G03)

**레드팀 입장 (Phase 2 C-04)**:
- 5가지 ω² 값 (0.296 / 0.103 / 0.234 / 0.264 / 0.252) 중 가장 큰 0.296만 abstract headline
- 6-category aggregation 0.103은 pathogen main effect 0.117과 사실상 동급
- 4-pathogen restriction 0.137은 medium tier (Cohen large 임계 0.14 미달)
- "Reporting 메인을 가장 우호적인 추정에 둔 selective reporting"

**통계 전문가 입장 (Phase 2 통계 #1)**:
- "modeled" 한정 표현 충실 — "largest *modeled* component" (ch4:390 "in this dissertation reads as 'largest modeled component'")
- 6-cat 0.103 lower bound 명시 (ch4:396, ch5:281)
- 잔차 ω²≈0.39 자수 (ch4:361, 386, 390)
- 4-pathogen 0.137 robustness (ch5:292) 자기 보고
- Bayesian partial-pooling 0.252 (ch5:285), ANCOVA 0.264 (ch5:290), ART 0.277 (ch3:825) 다중 lens consistency
- PASS

**CCB 판정**: **(a) 이미 답 있음 + (b) 부분 보강 권장**

**근거 (IV&V로 본문 직접 확인)**:
- abstract.tex:10 "[0.195, 0.333]; 6-category aggregation gives ω² = 0.103 as a collinearity-robust lower bound; within-cell residual ω² ≈ 0.39" — abstract headline에 lower bound + residual 모두 박혀 있음
- ch1_introduction.tex:148 동일한 caveat 표시
- ch4:386, 390, 396 잔차 0.39 + 6-cat 0.103 모두 명시
- ch5:281 "Below Cohen's large threshold" 자수
- ch5:292 "n=4에서 ω²=0.137" robustness 자수
- ch5:285 Bayesian HDI [0.188, 0.314]

**판정 정당성**: 통계 전문가가 옳다. 레드팀 C-04의 "selective"라는 라벨은 본문이 모든 추정치를 명시적으로 박은 사실을 기각한다.

**부분 보강 권고 (Tier 2)**:
- abstract headline은 단일 0.296을 사용하지만 같은 paragraph (line 10)에 lower bound 0.103과 residual 0.39를 명시 — 표현 강도는 정직.
- **단**, 4-pathogen subset 0.137은 abstract/ch1에 누락. ch5:292에만 등장. → P2 (선택). 표현 약화 위험은 medium 수준 (Cohen large 0.14의 lower bound 0.055 차이로 초과).
- 권고: ch1_introduction.tex:148 caveat 끝에 "(under 4-pathogen homogeneous-curation subset, ω² = 0.137; see Section ...)" 1줄 추가 가능. P2 (선택).

---

### 충돌 3 (잠재): 레드팀 C-01 회로성 vs 통계 #9 (조건부 PASS)

레드팀 C-01: "Layer A vs freq Spearman ρ≈0.97 회로성. ω²=0.296 인과 해석이 회로 구조 위에 세워짐."

통계 #9: "ρ=0.97 (entropy↔freq feature correlation) ≠ ρ=0.12 (Layer A membership↔freq score point-biserial). 두 ρ 다른 양. 1줄 disambiguation 권고이나 합격선 통과."

**CCB 판정**: **(b) 답 부족** (P0)

**근거**:
- ch4:739 freq--entropy ρ=0.97 (feature-feature)
- ch5:33 mean |ρ|=0.12 (Layer A membership ↔ freq score, point-biserial) — 회로성의 직접 지표
- 본문에서 이 둘을 명시적으로 구별하는 1문장이 부재 (통계 #9 + Ch5 C1 동일 결론)
- 레드팀이 두 ρ를 합쳐서 "회로 구조"로 묶은 부분은 통계 #9가 정확히 지적한 혼동의 사례

**판정**: 통계 #9가 옳고, 레드팀 C-01의 강도(=Critical로 본문 무효화)는 과장. 그러나 disambiguation 누락은 실재. → **(b) 답 부족, P0** (1-2줄 추가만으로 해결).

---

## 3. Critical 분류 결과 (총 35건 Critical-level)

> 입력: 레드팀 C 5건 + Phase 2B Critical (Ch1=3, Ch2=7, Ch3=6, Ch4=3, Ch5=7, Ch6=4) = 30건 → 합 35건. 중복 통합 후 G01–G40 그룹.

### 분류 카운트
| 분류 | 건수 (통합 후) | 설명 |
|------|--------------|------|
| **(a) 이미 답 있음** | **6건** (G02, G03, G05, G06, G37, G38) | 본문 명시적 caveat/약화로 해결 |
| **(b) 답 부족** | **31건** | 수정 필요 |
| **(c) 공격 부당** | **0건** | 통합 후 부당 단독 항목 없음 (G37은 (a)로 흡수) |
| **(통합 후 unmodified Critical)** | (Phase 2 통계 PASS 10/10) | 별도 결함 없음 |

(b) 답 부족 31건 중:
- **P0 (필수 수정)**: 8건 — G01, G07, G08, G09, G10, G12, G14 (3건 figure caption 통합), 추가 ch6:13 Friedman 분리 (G02 부분 추출)
- **P1 (권장 수정)**: 11건 — G04, G11, G13, G15, G16, G18, G19, G20, G21, G24, G31, G40
- **P2 (선택)**: 12건 — G17, G22, G23, G25, G26, G27, G28, G29, G30, G32, G33, G34, G35, G36, G39

---

## 4. P0 (필수 수정) 목록

| ID | 결함 | 위치 (file:line) | 수정 텍스트 (가능시 구체) | 난이도 |
|----|------|-------|-----------------|--------|
| **G01** | 두 ρ 값 disambiguation | `ch5_discussion.tex:33` (또는 `ch4:891`) | 1문장 추가: "Note: per-position point-biserial ρ (Layer A membership ↔ freq score, mean \|ρ\|=0.12) is conceptually distinct from feature-feature Pearson ρ (e.g., entropy↔freq ρ=0.97 in Section feature_correlation), which describes redundancy among scoring inputs rather than circularity with ground truth." | 낮음 (1-2줄) |
| **G07** | 4-feature 97.6% paired-test 부재 caveat (abstract/ch6) | `abstract.tex:11`, `ch6_conclusion.tex:14` | abstract: "...retains $\approx$98\% (97.6\%; numerical equivalence under uniform-weight LOPO, no paired-test significance)..." / ch6: 동일 표현 추가 | 낮음 (1-2줄, 두 파일) |
| **G08** | Two-stage vs Stage 3 구조 모순 | `ch1_introduction.tex:82`, `:143` | "two-stage experimental design" → "two-stage main experimental design plus a Stage~3 information-integration layer" (또는 "three-stage design") | 낮음 (1-2줄) |
| **G09** | Ch1 novel-only Bonferroni $p_{\text{adj}}\approx3.9\times10^{-9}$ 출처 | `ch1_introduction.tex:150` | (a) ch4 본문/표에 명시적으로 추가하거나 (ch4:886 footnote에 "novel-only $p_{\text{adj}} \approx 3.9 \times 10^{-9}$ across 780 combinations" 1줄 추가), 또는 (b) ch1에서 nominal Fisher만 보고하고 Bonferroni 표현 삭제 | 낮음 (1-2줄, 권고 (a)) |
| **G10** | Ch1 L153 "7.19×" 두 의미 충돌 | `ch1_introduction.tex:153` | H3N2 novel-only를 명시 분리: "H3N2's novel-only enrichment is 7.19× **for 9 novel positions**, distinct from the HIV-1 full-set 7.19× (Fisher $p = 0.132$ for H3N2 novel-only, indicating no significant external signal beyond Layer A overlap)" | 낮음 (1-2줄) |
| **G12** | Ch6 7.19× full vs novel-only 모호 | `ch6_conclusion.tex:15` | "yields full-set 7.19-fold enrichment (Bonferroni $p_{\text{adj}}=2.5\times 10^{-16}$) and Layer A-disjoint novel-only enrichment 7.16–8.24× (worst-case Fisher $p=5\times 10^{-12}$)" | 낮음 (1-2줄) |
| **G14a** | Ch4 figure caption Jaccard 페어 오류 | `ch4_results.tex:104` (`dms_evaluation_top.png` caption) | "Jaccard similarity = 0.006 between functional and DMS-escape" → "Jaccard similarity = 0.006 between DMS-escape and convergent evolution positives" | 낮음 (1줄) |
| **G14b** | Ch4 cross_pathogen_comparison best vs mean misframe | `ch4_results.tex:210, 215` | (a) caption을 "Mean MCC across detectors per scoring × pathogen"로 명시; (b) 본문 인용을 "Table 4.5는 best 대비 MCC, 그림은 mean MCC"로 분리 | 낮음 (텍스트 1-2줄) 또는 중간 (figure 재생성 시) |
| **G14c** | Ch4 stage3_anova 잔차 0.39 "shown" caption 오류 | `ch4_results.tex:386-388` | caption "is shown for reference" → "is reported separately in the text" | 낮음 (1줄) |
| **G02 부분 (ch6)** | Ch6 Friedman/LOPO null-consistent 묶음 표현 | `ch6_conclusion.tex:13` | "LOPO 0/11 and Friedman p=0.990 are treated as null-consistent corroboration" → "Friedman χ²=7.69, p=0.990 shows no universally best combination; LOPO 0/11 is null-consistent under permutation; both are corroborative consistency checks rather than independent evidence" | 낮음 (1-2줄) |

**P0 합계: 9 항목 (3 figure + 6 텍스트), 모두 즉시 수정 가능 (총 약 1-2시간 작업).**

---

## 5. P1 (권장 수정) 목록

| ID | 결함 | 위치 | 수정 권고 | 난이도 |
|----|------|------|-----------|--------|
| **G04** | HIV-1 단일 anchor + winner's curse abstract/ch1/ch6 미반영 | `abstract.tex:11`, `ch1:150`, `ch6:15` | "Bonferroni-survivor mean ≈4–5×" 또는 "n=1 anchor"를 abstract/ch6에 명시 | 낮음 |
| **G11** | Ch6 Contribution 1 약화 ("broadest"/"to our knowledge"/8580 누락) | `ch6_conclusion.tex:11` | abstract:4 표현 직접 재진술 + 8,580 evals 명시 | 낮음 |
| **G13** | PAHD-R scope creep | `ch6_conclusion.tex:16` | "PAHD-R redesign translates these findings" → "Building on these findings, the PAHD-R synthesis (Chapter 5) demonstrates feasibility" 또는 abstract에 PAHD-R 1줄 추가 | 낮음 |
| **G15** | Ch3 재현성 (cutoff/MAFFT/repo URL forward-ref) | `ch3:131, 132, 904` | (a) cutoff date를 YYYY-MM-DD로, (b) MAFFT 알고리즘 per pathogen supplementary, (c) repo URL을 ch3 footnote에 직접 기재 | 중간 (수치 확정 시) |
| **G16** | Ch3 preregistration / Bonferroni 분모 결정 시점 | `ch3:296, 826` | "Layer A/B/C 임계값과 Bonferroni 780 분모는 Stage 1 분석 시작 이전 freeze" 1문장 추가 (실제로 그러했다면) | 낮음 (단, 실제 사실 확인 필요) |
| **G18** | MEME/FUBAR 1차 출처 분리 | `ch2:57` | `\cite{kosakovsky2020hyphy}` → `MEME~\cite{murrell2012meme}`(신규 bib 추가) + `FUBAR~\cite{murrell2013fubar}` | 낮음 (bib 1개 추가 + 인용 교체) |
| **G19** | OncodriveCLUST/CLUSTL 명명 일관 | `ch2:241` | "OncodriveCLUSTL"을 "OncodriveCLUST"로 통일 (정확성 우선) 또는 Arnedo-Pac 2019 bib 추가 | 낮음 |
| **G20** | ESM-3 인용 부재 | `ch2:143-144` | Hayes et al. 2024-2025 정식 인용 또는 ESM-3 본문 언급 삭제 | 낮음 (bib 1개 추가) |
| **G21** | Greaney escape DMS 시리즈 누락 | `ch2:106` 다음 | Greaney 2021 (Cell Host Microbe), Greaney 2022 (PLoS Path) 추가 | 낮음 (bib 2개 + 1 paragraph) |
| **G24** | Ch1 information-type panel 11 vs 12 충돌 | `ch1:82` | "across all 11 pathogens" → "11-pathogen panel (extended to 12 with Zika for feature ablation)" | 낮음 |
| **G31** | Ch5 NFL "stronger evidence" 비약 | `ch5:84` | "stronger practical evidence ... than the abstract theorem alone" → "complementary practical evidence within a biologically meaningful problem class, while NFL itself remains a statement about all possible problem distributions" | 낮음 |
| **G40** | Ch3 EqualWeight directional sign LOPO leakage 명시 | `ch3:631` | "sign이 LOPO 안에서 fold별 재계산되는지 또는 일괄 결정인지" 명시 | 낮음 |

**P1 합계: 12 항목, 총 약 4-6시간 작업 (1주 내 완수 가능).**

---

## 6. P2 (선택) 목록

| ID | 결함 | 위치 | 수정 권고 | 난이도 |
|----|------|------|-----------|--------|
| G17 | Layer C threshold sweep 4→6 pathogen 확장 | ch3:317, 4 pathogens 분석 | Rabies/EV-A71 sweep 추가 | 중간 (재분석 1일) |
| G22 | EVEscape composite EVE→ESM-2 substitution disclaim | ch2:148 | substitution 한계 명시 | 낮음 |
| G23 | Ch2 "no detection-task benchmark" scope-bias | ch2:234 | "with the specific combination of cross-pathogen × multi-source × MCC × ANOVA" 단서 | 낮음 |
| G25 | Ch1 cancer benchmark 인용 빈약 | ch1:35 | weber2019, tokheim2016, lawrence2013 등 추가 | 낮음 |
| G26 | Ch1 EVEscape/Livesey & Marsh 누락 | ch1:33 | thadani2023evescape, livesey2020using 추가 | 낮음 |
| G27 | youn2025mutclust "core task" 자기 인용 | ch1:11 | carabelli2023convergent로 교체 | 낮음 |
| G28 | Ch4 Friedman n=11 power caveat ch4 누락 | ch4:438 | "Friedman's power with n=11 blocks is limited" 1문장 | 낮음 |
| G29 | Ch4 random baseline SD 0.003 vs 0.034 | ch4:445, 460 | random baseline 정의 명시 | 낮음 |
| G30 | Ch4 H3N2 9.36× self-consistency fbox 라벨 | ch4:13 | fbox에 "self-consistency check" 라벨 | 낮음 |
| G32 | Ch5 11-cluster Bolker 미달 직접 진술 | ch5:319-321 | "minimum (5–6) 위, 권장(20–30) 아래" 1문장 | 낮음 |
| G33 | Ch5 independent reproduction 1문장 → claim 매핑 | ch5:287 | "single-team-single-snapshot estimate"로 어떤 claim이 영향받는지 1-2 문장 | 낮음 |
| G34 | Ch5 정의 비대칭→회로성 chain cross-ref | ch5:33 | sec:gt_heterogeneity cross-ref | 낮음 |
| G35 | Ch6 H3N2 9.36× / SARS 7.63× / CI 누락 | ch6:12-15 | abstract와 동일 강도 재진술 | 낮음 |
| G36 | Ch6 "confirms" 톤 조정 | ch6:91 | "confirms" → "evidences" | 낮음 |
| G39 | HIV-1 23/45 두 의미 (Layer A 23 vs detected 23) | ch4:874, 921 | 명확 구분 footnote | 낮음 |

**P2 합계: 15 항목, 총 약 4-8시간 작업 (단, G17은 재분석 1일).**

---

## 7. 안돈 평가

### 미해소 (b) Critical 카운트

| 우선순위 | 건수 | Phase 4 진입 차단 여부 |
|---------|------|----------------------|
| P0 (b) Critical | **9건** | **차단** |
| P1 (b) Critical | 12건 | 차단 안 함 (권장 수정) |
| P2 (b) | 15건 | 차단 안 함 (선택) |

### 안돈 트리거 평가

**미해소 (b) Critical = 9건 (P0)**.

**Phase 4 (교수 평가) 진입 가능 여부**: **NO** (조건부).

**이유**:
- P0 9건 중 가장 위험한 항목:
  1. **G09 (ch1:150 novel-only Bonferroni $p_{\text{adj}}\approx3.9\times10^{-9}$ 출처 미확인)** — 학위 심사에서 "수치 출처 추적 불가"로 fabrication 의혹 가능. 즉시 수정 필수.
  2. **G14 (ch4 figure caption 3건 오류)** — 학위 심사 1차 지적 사항 가능성 매우 높음.
  3. **G10 (ch1:153 "7.19×" 두 의미 한 paragraph 충돌)** — 같은 페이지에서 동일 숫자가 다른 의미를 가짐.
  4. **G08 (two-stage vs Stage 3 구조 모순)** — abstract/ch1과 ch3가 design 카운트가 다름.
  5. **G07 (4-feature 97.6% paired-test 부재 caveat 누락)** — Tier 2 reviewer가 즉각 지적.

이들은 모두 1-2줄 텍스트 수정으로 해결 가능 (총 약 1-2시간). **수정 후 Phase 4 진입 즉시 가능**.

### 통계 영역 안돈

통계 전문가 10/10 PASS, 안돈 사유 0건. ω² 해석, LOPO null, HIV-1 enrichment, Bonferroni, sample size, effect size, 회로성 audit, 재현성 통계 모두 정직 표현 PASS.

---

## 8. CCB 종합 판정

### 현재 상태: **CONDITIONAL PASS**

**근거**:

1. **통계적 정직성**: 상위권. LOPO null-consistency, winner's curse, cluster bootstrap caveat, ART, Kruskal-Wallis, ANCOVA, Bayesian partial pooling — 모두 본문 자수. 통계 #4 + #1 모두 PASS, 충돌 중재 결과 통계 측 우위 (레드팀 C-02/C-04는 본문 명시적 한정 표현을 기각했다는 점에서 부당).

2. **수치 일관성**: Phase 0의 84/84 PASS + Ch4 cross-check 매트릭스 20+ 핵심 수치 모두 일관. 라운딩 차이 (2.47 vs 2.5e-16) 1건 외에 결함 없음.

3. **Critical 결함의 본질**:
   - 6건은 본문 caveat로 이미 해소됨 (a)
   - 31건은 (b) 수정 필요이나 31건 중 P0 9건만 합격 차단
   - P0 9건 모두 1-2줄 수정으로 해결 가능 (재실험 불필요)
   - 부당 (c) 단독 0건

4. **합격 차단 핵심**: G09 (출처 미확인 Bonferroni), G10 (7.19× 두 의미), G14 (figure caption 3건), G07 (paired-test caveat), G08 (two-stage 모순), G02 부분 (ch6:13 Friedman/LOPO 분리) — 텍스트 수정만으로 해결.

### Phase 4 진입 조건

다음 P0 9건 수정 후 Phase 4 진입:
1. G01 — 두 ρ disambiguation (ch5:33)
2. G07 — 4-feature 97.6% paired-test caveat (abstract:11, ch6:14)
3. G08 — two-stage → "two-stage main + Stage 3 layer" (ch1:82, 143)
4. G09 — novel-only $3.9\times10^{-9}$ 출처 명시 (ch4:886) 또는 ch1:150 표현 변경
5. G10 — H3N2 novel-only "7.19×" 분리 표시 (ch1:153)
6. G12 — Ch6 7.19× full vs novel-only 분리 (ch6:15)
7. G14a — figure caption Jaccard 페어 정정 (ch4:104)
8. G14b — cross_pathogen_comparison mean vs best 정정 (ch4:210, 215)
9. G14c — stage3_anova 잔차 caption 정정 (ch4:386)
10. G02 부분 — ch6:13 Friedman/LOPO 분리 표현

**예상 작업량**: 1-2시간 (텍스트 수정만, 재분석/재실험 불필요).

### 최종 권고

**즉시 수정** (Tier 1, P0 10건). 이후 Phase 4 (교수 평가) 진입 가능.

P1 (12건) 보강은 Phase 4 평가 동안 또는 final defense 전에 권장. 실험/분석 재가동 불필요한 **순수 텍스트/인용 보강**이라 1주 내 완수 가능.

P2 (15건) 보강은 final draft 단계. G17 (Layer C sweep 6 pathogen) 1건만 중간 난이도 (재분석 1일). 나머지 14건은 모두 텍스트 1-2줄.

**재실험 권고**: **없음**. 모든 결함이 기존 데이터의 표현/문서화 차원이며 실험 재가동 불필요.

**본문 그대로 + 약점 인정**: NO. P0 9건은 단순 부주의/누락이라 수정해야 할 정직 결함이며 "약점 인정"으로 우회할 사유가 없다.

---

## 부록: Phase 별 산출물 정합성 확인

| Phase | 산출물 | 결함 카운트 | CCB 처리 |
|-------|--------|-----------|---------|
| Phase 0 verify | 84/84 PASS | 0 | 검증 통과 |
| Phase 1 블루팀 | 변호 가능 6 claim + 5 시나리오 + 5 보강 항목 | (참고용) | 시나리오 1, 3, 4 = (a) 본문 자수, 시나리오 2 = G04, 시나리오 5 = G05/(a) |
| Phase 2 레드팀 | C 5건 / M 11 / m 10 | 16 critical+major | C-01 → G01/(b), C-02 → (a), C-03 → G04/(b), C-04 → (a), C-05 → G05/(a). M-01 → (a), M-05 → G07/(b), M-06 → G01 통합, M-08 → G04 통합, M-11 → 일관성 caveat 존재/(a). |
| Phase 2 통계 | 10/10 PASS, 안돈 0 | 0 | 충돌 중재에 사용 |
| Phase 2B Ch1 | C 3건 | C1 → G09, C2 → G10, C3 → G08 |
| Phase 2B Ch2 | C 7건 | C1 → G18, C2 → G19, C3 → G23, C4 → G20, C5 → 부분 (b) P2, C6 → G22, C7 → ch5 이동 P2 |
| Phase 2B Ch3 | C 6건 | C1/C2/C4 → G15, C3/C5 → G16, C6 → G17 |
| Phase 2B Ch4 | C 3건 | C-1/C-2/C-3 → G14 |
| Phase 2B Ch5 | C 7건 | C1 → G01, C2 → 부분 G05 보강 P2, C3 → G31, C4 → G33 P2, C5 → G32 P2, C6 → G07, C7 → G34 P2 |
| Phase 2B Ch6 | C 4건 | C1 → G11, C2 → G12, C3 → G11 통합, C4 → G07 통합 |

**총 통합 그룹**: 40개 (G01–G40). (a) 6건 + (b) 31건 + (c) 부당 단독 0건 + (참고) 3건.

---

**검토자**: CCB 중재 에이전트 (Phase 3, 2026-04-28)
**저장 위치**: `/proj/paper/paper/dissertation/review/2026-04-28/phase3_ccb.md`
