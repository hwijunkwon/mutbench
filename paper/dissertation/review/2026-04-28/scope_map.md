# Adversarial Review Scope Map (2026-04-28)

## 대상 논문
- 위치: `/proj/paper/paper/dissertation/`
- 본문: `chapters_en/ch1_introduction.tex` ~ `ch6_conclusion.tex`
- Abstract: `front_en/abstract.tex`
- 참고문헌: `references.bib`
- 빌드 산출: `thesis_en.pdf` (206 pages, v148)

## Phase 0: 자동 검증 결과
- `verify_dissertation.py`: PASS 84 / FAIL 0 / WARN 0
- LaTeX 빌드: 206p, undefined refs 0, citation undefined 0
- TODO/FIXME/PLACEHOLDER: 0건
- 마감 어조: 통과 (비격식 표현 없음)

## 핵심 주장 (Headline Claims)
| # | 주장 | 근거 위치 | 위험 신호 |
|---|------|----------|----------|
| C1 | MutBench: 10 info × 20 scoring × 14 family × 39 variants × 11 pathogens = 8,580 평가 (region-level hotspot detection 광역 벤치마크) | abstract, ch1, ch3 | 정의 명확성, 숫자 일관 |
| C2 | scoring×pathogen interaction이 최대 분산 성분 (ω²=0.296, CI[0.195, 0.333]); 6-cat aggregation lower bound ω²=0.103 | ch4 ANOVA | ω² 해석 (T-CRITICAL: 05_error_taxonomy 분류) |
| C3 | LOPO 0/11 + Friedman p=0.990 → universally best 없음, pathogen-dependent | ch4 | LOPO 0/11이 permutation null과 구별 불가 |
| C4 | HIV-1 7.19× vaccine escape enrichment, Bonferroni p=2.5e-16; novel-only 7.16-8.24× | ch4 (Contribution 3b) | Primary external anchor, 단일 pathogen |
| C5 | 4-feature core ≈ 98%(97.6%) 풀 ensemble | ch4 ablation | Paired test 부재 (numerical equivalence only) |
| C6 | 9 distinct optimal information types across 11 pathogens | ch4 | 9 vs 11 차이 해석 |

## 알려진 약점 (개시 시점)
- **W1 (회로성)**: Layer A vs frequency Spearman ρ=0.973 → freq scoring 본질적 유리. Layer C DMS는 3-4 pathogens 한정 (2,340 evals)
- **W2 (LOPO null)**: LOPO 0/11은 random permutation에서도 likely. 자체 검정력 낮음
- **W3 (overlap)**: H3N2 9.36×의 69%가 Layer A overlap. SARS-CoV-2 exploratory after Bonferroni
- **W4 (DMS 가용)**: Layer C 검증 = 3/11 pathogens만 실시 (HIV-1, H3N2, SARS-CoV-2 등)
- **W5 (정의 표류)**: Layer A = "convergent + immune-escape + HVR-membership union" — 정의 자체가 변동적, 비교 불공정 위험

## 결함 유형 매핑 (T1~T11 — 결함 유형 분류 적용)
- **T-OVERCLAIM (과대해석)**: Contribution 3b 표현 ("primary external validation"), 4-feature 98% 해석
- **T-SELECTIVE (선별 보고)**: HIV-1 anchor, H3N2 self-consistency만 부각 / 다른 pathogens DMS 미실시
- **T-CIRCULAR (회로성)**: Layer A의 freq 상관, scoring × ground truth 회로
- **T-NULL-DISGUISE (귀무 가장)**: LOPO 0/11을 강조하지 않음 + 약화 ("null-consistent corroboration")
- **T-AGG-MISMATCH (집계 불일치)**: ω²=0.296 vs 6-cat ω²=0.103 차이 + 실제 reporting 우선순위
- **T-COVERAGE (커버리지)**: 11 pathogens 주장 but Layer C 3개, escape annotation 3/11
- **T-DEF-DRIFT (정의 표류)**: Layer A union 정의가 pathogen별 다름
- **T-STAT-INTERP (통계 해석)**: ω², CI, p-value 의미와 한계 설명
- **T-FIG-COHERENCE (그림 정합)**: 18개 figure가 본문 수치와 일치, 흑백 가독, 라벨 가림
- **T-CITE-COMPLETENESS (인용 충실)**: ViroGym, EVEREST v3, ProteinGym v1.3, Rice 1976, Bailey 2018, Livesey & Marsh 2023 등

## 챕터별 라인/위험 영역
| 챕터 | 라인 | 위험 영역 |
|------|------|----------|
| Abstract | 17 | C1~C6 압축 표현, 과장 위험 |
| Ch1 Introduction | 171 | Contribution 표현, gap 정의 |
| Ch2 Background | 300 | 관련 연구 충실, 비교 공정성 |
| Ch3 Methods | 909 | 실험 설계 재현성, ground truth 정의 |
| Ch4 Results | 972 | 모든 수치, ω², LOPO, enrichment, 그림 |
| Ch5 Discussion | 336 | 한계 인식, 회로성 토의, future work |
| Ch6 Conclusion | 118 | 기여 재진술 정확성 |

## 에이전트 분담 (Phase 1+2+통계 병렬, IV&V)

### Round 1 (병렬 3 에이전트)
- **블루팀 (sonnet)**: 논증 지도 작성. Claims C1-C6 → 증거 위치 매핑 + 실패 시나리오 5개 + 챕터별 최약 지점.
- **레드팀 (opus, IV&V)**: Critical/Major/Minor 분류 공격. 블루팀 산출물 차단. T-OVERCLAIM, T-SELECTIVE, T-CIRCULAR 중점.
- **통계전문가 (opus)**: ω² 해석, CI, multiple testing, ANOVA 가정, LOPO 검정력. PASS/WARN/FAIL.

### Round 2 (병렬 6 에이전트, 챕터 분담)
- **Ch1 Reviewer (sonnet)**: gap 정의 + 인용 누락 + Contribution 표현 정확성
- **Ch2 Reviewer (sonnet)**: 관련 연구 누락 + 경쟁 연구 비교 + Bailey 2018 형평
- **Ch3 Reviewer (opus)**: 재현성 + ground truth 정의 + 통계 사전 등록 부재
- **Ch4 Reviewer (opus)**: 수치 일관 + figure 정확성 + 각 ω², CI, p 정확
- **Ch5 Reviewer (opus)**: 한계 진술 충실 + 회로성 토의 + future work
- **Ch6 Reviewer (sonnet)**: 기여 재진술 일치 + 과장 점검

### Round 3 (CCB 단일)
모든 산출물 수합 → (a) 이미 답 / (b) 답 부족 / (c) 부당 분류. Critical 미해소시 안돈.

### Round 4 (10 교수 시뮬레이션)
교수 1-10 각 9개 영역 채점, 100점 만점, 80점 합격선.

## 안돈 코드
- Critical 회로성/과대해석/선별 보고 발견 즉시 전체 정지
- 통계전문가가 ω² 해석 FAIL 표시시 즉시 정지
