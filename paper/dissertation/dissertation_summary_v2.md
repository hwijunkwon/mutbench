# MutBench 학위논문 요약서 v2

**논문 제목**: Systematic Benchmarking and Adaptive Clustering Frameworks for Multi-Scale Genomic Data Analysis

**저자**: 권휘준 | **지도교수**: 정인욱 | **소속**: 경북대학교 컴퓨터학부

**버전**: v98 | **페이지**: 169 | **날짜**: 2026-03-28

---

## 연구 배경

바이러스 게놈에서 변이가 집중되는 위치(핫스팟) 중에는 면역 회피·감염력 증가 등 생물학적으로 의미 있는 위치가 있다. 핫스팟 탐지의 목적은 수천 개의 후보 위치를 좁혀 실험실 검증의 우선순위를 제공하는 것이다.

**기존 문제 3가지:**
1. 탐지 방법을 비교할 체계적 벤치마크가 없었다
2. 어떤 방법이 어떤 바이러스에 적합한지 통계적 증거가 없었다
3. 빈도·엔트로피 외 다른 정보 유형이 체계적으로 비교된 적 없었다

**관련 연구와의 차이 (Ch2 벤치마크 비교 테이블 포함):**
- EVEREST (Marks lab, 2025): 45개 DMS로 변이 효과 *예측*(VEP)을 벤치마크 → MutBench는 핫스팟 *탐지*를 벤치마크 (상보적)
- ProteinGym: 217개 DMS, 인간/일반 단백질 대상 → MutBench는 바이러스 전용
- Bailey 2018: 암 driver 벤치마크 → 체세포 변이 vs 집단 수준 변이 (방법론 전이 불가)

---

## MutBench 프레임워크

### 3층 정답 기준 (Ground Truth)

| Layer | 역할 | 정의 |
|-------|------|------|
| A | 양성 기준 | 수렴 진화 위치 (독립 계통에서 반복 출현) |
| B | 음성 기준 | 보존 구조 영역 (변이 시 기능 상실) |
| C | 독립 검증 | DMS 실험 데이터 (6개 병원체: SARS-CoV-2, H3N2, HIV-1, RSV, Rabies, EV-A71) |

### 실험 규모

| 항목 | 수 |
|------|-----|
| RNA 바이러스 | 11개 (SARS-CoV-2, H3N2, Norovirus, HIV-1, Dengue, RSV, Influenza B, MERS, HCV, Rabies, EV-A71) |
| 정보 카테고리 | 6개 (빈도, MSA, 계통, 구조, AI, 복합) |
| Scoring 유형 | 20개 |
| 탐지 알고리즘 | 14 families, 39 variants |
| **총 평가 수** | **8,580회** |

---

## 핵심 결과

### 결과 1: 어떤 정보를 쓰느냐가 어떤 알고리즘보다 23배 중요하다

| 요인 | ω² | 해석 |
|------|-----|------|
| **scoring × pathogen** | **0.296** | 어떤 정보 + 어떤 바이러스 조합이 성능의 핵심 |
| pathogen | 0.117 | 바이러스 자체 난이도 |
| scoring | 0.063 | 정보 유형 간 차이 |
| **family (알고리즘)** | **0.013** | 알고리즘 선택은 상대적으로 덜 중요 |

ω²(scoring) / ω²(family) = **4.8배**, ω²(scoring×pathogen) / ω²(family) = **22.8배**

강건성 확인: 비모수 Kruskal-Wallis (H=277.9, 일치), 6-카테고리 ANOVA (ω²=0.103, 일관)

### 결과 2: 11개 바이러스, 9가지 서로 다른 최적 scoring

| 바이러스 | 최적 scoring | 카테고리 | MCC | 생물학적 근거 |
|---------|-------------|---------|-----|-------------|
| H3N2 | FUBAR BF | 계통 | 0.534 | 깊은 계통수, 양성선택 강함 |
| Norovirus | homoplasy | MSA | 0.510 | 에포크 진화, 수렴 변이 |
| SARS-CoV-2 | Tranception | AI | 0.211 | 얕은 계통, PLM이 보상 |
| RSV | ESM-2 LLR | AI | 0.196 | 제한된 계통 다양성 |
| EV-A71 | semantic change | AI | 0.260 | 항원 표면 기능 변화 |
| Rabies | stability | AI | 0.248 | 구조 안정성 제약 |
| HCV | freq | 빈도 | 0.660 | 과변이 영역 지배 |
| Influenza B | freq | 빈도 | 0.392 | 항원 드리프트 빈도 반영 |
| Dengue | entropy_indel | MSA | 0.274 | 다양성 패턴 |

**6개 카테고리 모두** 최소 1개 바이러스에서 최적.

### 결과 3: 만능 방법은 없다 (3중 통계 검증)

| 검증 | 값 | 의미 |
|------|-----|------|
| Friedman | χ²=7.69, p=0.990, **W=0.037** | 상위 조합 구분 불가 |
| LOPO | **0/11** 일치, gap=0.265 | 일반화 완전 실패 |
| Unique combos | 11/11 | (단, 순열 검정상 93% 우연 가능 → **MCC gap이 본질**) |

### 결과 4: 다중 정보 통합 → 실험 탐색 범위 축소

**Vaccine escape enrichment (3개 병원체):**

| 병원체 | 방법 | Enrichment | p값 |
|--------|------|-----------|-----|
| SARS-CoV-2 | EqualWeight | **4.90배** | < 0.0001 |
| H3N2 | EqualWeight | **4.01배** | 0.0023 |
| H3N2 | FreqThresh (빈도만) | 2.7배 | 0.055 (비유의) |
| HIV-1 | EqualWeight | **최대 9.36배** | < 0.001 |

Layer A ↔ vaccine escape 교차 검증: Layer A 탐지 결과가 vaccine escape 위치를 유의하게 enrichment → 독립 생물학적 검증.

### 결과 5: Layer C (DMS) 독립 검증 — 6/11 병원체

| 바이러스 | Best (Layer A) | Best (Layer C) | 순위 상관 |
|---------|---------------|---------------|----------|
| SARS-CoV-2 | tranception | plddt_inv | rho=−0.13 |
| H3N2 | fubar_bf | semantic_change | rho=−0.11 |
| HIV-1 | entropy | fubar | rho=0.27 |
| RSV | esm2_llr | EVEscape_composite | rho=0.85 |
| Rabies | stability | homoplasy | rho=0.86 |
| EV-A71 | semantic_change | plddt_inv | rho=−0.18 |

- Dengue DMS 제거 (잘못된 단백질 매칭)
- 6/11 DMS 병원체: SARS-CoV-2, H3N2, HIV-1, RSV, Rabies, EV-A71
- Layer A와 C가 다른 것을 측정 → GT 편향이 아닌 실제 병원체 차이 확인.

---

## 실용적 가치

### 실험실 우선순위 제공

탐지된 핫스팟 = 실험 검증 후보 순위 리스트:
- SARS-CoV-2: **4.90배** enrichment (p < 0.0001)
- H3N2 (다중 통합): **4.01배** enrichment (p = 0.0023)
- HIV-1: **최대 9.36배** enrichment (p < 0.001)

### 새 바이러스 적용 워크플로 (~15-20분/병원체)

| 단계 | 소요 시간 | 내용 |
|------|----------|------|
| 1. 서열 수집 + MSA | ~5분 | NCBI/GISAID, MAFFT (200+ 서열) |
| 2. Feature 계산 | ~10분 | 빈도/엔트로피(초), homoplasy(2-5분), ESM-2(3-5분, GPU) |
| 3. Scoring 선택 | 즉시 | 아래 추천 테이블 참조 |
| 4. Detection + 평가 | ~30초 | KDE/Wavelet 권장 → 상위 후보 리스트 출력 |

### 바이러스 패밀리별 추천

| 패밀리 | 추천 scoring | 근거 |
|--------|-------------|------|
| Orthomyxoviridae (인플루엔자) | 계통 (FUBAR) | 깊은 계통수, 양성선택 |
| Coronaviridae (코로나, MERS) | AI (PLM) | 얕은 계통, PLM 보상 |
| Caliciviridae (노로) | MSA (homoplasy) | 수렴 변이 패턴 |
| Retroviridae (HIV) | MSA (entropy) | 높은 다양성 |
| Flaviviridae (HCV, 뎅기) | 빈도 기반 | 과변이 영역 지배 |
| Pneumoviridae (RSV) | AI (ESM-2) | 제한된 계통 신호 |

---

## 기여

| # | 기여 | 핵심 수치 |
|---|------|----------|
| 1 | **MutBench 프레임워크** | 최초의 바이러스 핫스팟 벤치마크 (3층 GT, 8,580 evals) |
| 2 | **통계적 입증** | scoring×pathogen ω²=0.296, Friedman W=0.037, LOPO 0/11 |
| 3 | **정보 유형 분석** | 20 scoring (6카테고리)에서 9가지 최적, 통합 시 최대 9.36배 enrichment |

---

## 한계

| 한계 | 심각도 | 대응 |
|------|--------|------|
| Layer A 정의 이질성 | 중 | Layer C 독립 검증 + 같은 과 내에서도 최적 상이 |
| DMS 6/11 병원체만 | 중 | Layer A가 주 평가, DMS는 보조 검증 |
| 11개 바이러스 계통적 비독립 | 중 | 같은 과 쌍 내에서도 최적 scoring 상이 |
| 일부 scoring 정보원 중복 | 하 | 6-카테고리 ANOVA ω²=0.103으로 확인 |
| 소프트웨어 패키지 미제공 | 중 | GitHub 공개 예정 |

---

## 논문 구성 (6장, 169페이지)

| 장 | 제목 | 한 줄 |
|---|------|------|
| 1 | Introduction | 비교 기준이 없다 → 3가지 공백 → MutBench |
| 2 | Related Research | 기존 방법 + VEP 벤치마크(EVEREST) + 벤치마크 비교 테이블 + 공백 확인 |
| 3 | Methods | 11 바이러스 × 20 scoring × 39 detector, ANOVA/Friedman/LOPO |
| 4 | Results | **scoring×pathogen = 최대 분산원** + 정보 유형 분석 + 실용 검증 (모든 그림 11 pathogens) |
| 5 | Discussion | 타당성, 한계, 워크플로, 계통 비독립성 |
| 6 | Conclusion | 3가지 기여 + 미래 방향 |

---

## v98 주요 변경사항

- 모든 그림/테이블 11 pathogens 반영 (9-pathogen 잔존 완전 제거)
- DMS 6/11 검증 완료 (Dengue DMS 제거 — NS5를 E protein에 잘못 매칭)
- Rabies DMS: 시뮬레이션 → 실제 데이터 (Aditham 2025, Cell Host & Microbe)
- Vaccine escape: 3개 병원체 (SARS-CoV-2, H3N2, HIV-1), 최대 9.36배 enrichment
- Layer A ↔ vaccine escape 교차 검증 (H3N2: FUBAR BF가 양쪽 모두 최적)
- Ch2에 벤치마크 비교 테이블 추가 (MutBench vs EVEREST vs ProteinGym vs Bailey)
- ESM comparison table 삭제 (20-scoring 체계에 통합됨)
- Precision@k 테이블 11 pathogens 업데이트
- Ch1 접근성 개선, Ch3 다중검정 정당화, Ch5 NFL 한정, Ch6 CLI 예시
- 169 페이지, 에러 0, PAHD 0, 구데이터 잔존 0
