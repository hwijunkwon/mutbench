# MutBench 학위논문 요약서

**논문 제목**: Systematic Benchmarking and Adaptive Clustering Frameworks for Multi-Scale Genomic Data Analysis

**저자**: 권휘준 | **지도교수**: 정인욱 | **소속**: 경북대학교 컴퓨터학부

---

## 연구 배경

바이러스 게놈에서 변이가 집중되는 위치를 핫스팟이라 한다. 핫스팟 중에는 면역 회피, 감염력 증가 등 생물학적으로 의미 있는 위치가 있고, 단순히 특정 계통이 번성하면서 빈도만 높아진 위치도 있다.

핫스팟 탐지는 세 단계로 진행된다: (1) 수주~수개월간 전 세계에서 바이러스 유전자 서열을 시퀀싱하여 수집, (2) 수집된 서열을 정렬(MSA)하고 통계적 알고리즘으로 변이 집중 위치를 식별, (3) 식별된 후보 위치를 실험실에서 하나씩 생물학적으로 검증. 2단계(통계 분석)에서 후보를 효과적으로 줄여야 3단계(실험 검증)의 인적·시간적·비용적 효율이 높아진다. 예를 들어 1,000개 아미노산 위치를 가진 바이러스 단백질에서 후보를 50~100개로 줄이면 실험 검증에 드는 수개월의 시간을 절약할 수 있다. 본 논문은 2단계에서 사용되는 다양한 탐지 방법을 체계적으로 비교·평가하는 벤치마크 연구이다.

기존에는 이 분야에 세 가지 공백이 있었다. 첫째, 핫스팟 탐지 방법을 비교할 체계적 벤치마크가 없었다. 둘째, 어떤 방법이 어떤 바이러스에 적합한지 통계적 증거가 없었다. 셋째, 빈도·엔트로피 외에 계통 분석, 단백질 언어모델, 구조 정보 등 다양한 정보 유형이 체계적으로 비교된 적 없었다. 관련 벤치마크로 EVEREST(Marks lab, 2025)는 45개 DMS로 변이 효과 *예측*(VEP)을 벤치마크하지만 핫스팟 *탐지*와는 다른 문제이고, ProteinGym은 인간/일반 단백질 대상이며, Bailey 2018의 암 driver 벤치마크는 체세포 변이로 방법론 전이가 불가능하다.

---

## 연구 목적

1. 바이러스 변이 핫스팟 탐지를 위한 최초의 체계적 벤치마크 프레임워크(MutBench) 구축
2. 병원체마다 최적의 탐지 방법이 다르다는 것을 통계적으로 입증하고, 그 원인이 "알고리즘 선택"이 아니라 "정보 유형 선택"에 있음을 규명
3. 20가지 점수화 유형(6개 정보 카테고리)의 분석을 통해 어떤 정보가 어떤 바이러스의 핫스팟 예측에 유효한지 규명하고, 다중 정보 통합이 실험 탐색 범위를 축소함을 검증

---

## MutBench 프레임워크

### 3층 정답 기준 (Ground Truth)

핫스팟 탐지 자체는 가능하지만, 탐지된 위치가 생물학적으로 의미 있는지 평가하기 위한 정답 기준이 필요하다.

| Layer | 생물학적 의미 | 역할 | 출처 |
|-------|-------------|------|------|
| A | 자연선택이 반복 작용한 위치 (수렴 진화) | 양성 기준 (11개 병원체) | 문헌 기반 (Carabelli, Koel, Lindesmith 등) |
| B | 변이하면 바이러스가 죽는 위치 (정화 선택) | 음성 기준 | 구조 도메인, dN/dS < 0.5 |
| C | 실험실에서 기능 영향이 확인된 위치 (DMS) | 독립 교차 검증 (6개 병원체) | Dadonaite 2024, Lee 2018, Haddox 2018, Bloom lab 2026, Aditham 2025, Bakhache 2025 |

### 실험 규모

- **11개 RNA 바이러스**: SARS-CoV-2, H3N2, Norovirus, HIV-1, Dengue, RSV, Influenza B, MERS, HCV, Rabies, EV-A71 (6개 바이러스 과 커버)
- **6개 정보 카테고리, 20가지 점수화 유형**: 빈도 기반(3), MSA 유래(3), 계통 분석(4, FUBAR 포함), 구조 기반(3), AI 기반(5, ESM-2/Tranception 포함), 복합(2)
- **14개 탐지 알고리즘 패밀리** (39가지 파라미터 변형): Wavelet, KDE, SWAN, CUSUM, Bayes, MutClust 등
- **총 8,580회 평가** (20 scoring × 39 detector × 11 pathogens)

---

## 핵심 결과

### 결과 1: 어떤 정보를 쓰느냐가 어떤 알고리즘보다 23배 중요하다

3-way ANOVA(scoring × family × pathogen)로 성능 분산을 분해한 결과:

| 요인 | ω² | 해석 |
|------|-----|------|
| **scoring × pathogen** | **0.296 (최대)** | 어떤 정보가 어떤 바이러스에 맞는가가 성능의 핵심 |
| pathogen | 0.117 | 바이러스 자체의 난이도 차이 |
| family × pathogen | 0.082 | 어떤 알고리즘이 어떤 바이러스에 맞는가 |
| scoring | 0.063 | 정보 유형 간 평균적 차이 |
| scoring × family | 0.039 | 정보-알고리즘 간 상호작용 |
| **family (알고리즘)** | **0.013** | 알고리즘 선택은 상대적으로 덜 중요 |

scoring 주효과(0.063) ÷ family 주효과(0.013) = **4.8배**, scoring×pathogen(0.296) ÷ family(0.013) = **22.8배**. 즉 "어떤 알고리즘을 쓰느냐"보다 "어떤 생물학적 정보를 쓰느냐"가 성능을 결정하는 핵심 요인이며, 그 효과는 바이러스에 따라 근본적으로 달라진다. 비모수 Kruskal-Wallis 검정(H=277.9)과 6-카테고리 ANOVA(ω²=0.103)에서도 동일한 결론이 확인되었다.

### 결과 2: 11개 바이러스, 9가지 서로 다른 최적 scoring

| 바이러스 | 최적 scoring | 카테고리 | MCC | 생물학적 근거 |
|---------|-------------|---------|-----|-------------|
| HCV | freq | 빈도 | 0.660 | 과변이 영역(HVR1/HVR2)이 지배적 신호 |
| H3N2 | FUBAR Bayes factor | 계통 | 0.534 | 수십 년 계통수에서 양성선택 강함 |
| Norovirus | homoplasy | MSA | 0.510 | GII.4 에포크 진화로 수렴 변이 발생 (AUC 0.944) |
| Influenza B | freq | 빈도 | 0.392 | 항원 드리프트 빈도 반영 |
| HIV-1 | entropy | MSA | 0.275 | 높은 다양성, 엔트로피가 변이 분포 포착 |
| Dengue | entropy_with_indel | MSA | 0.274 | 다양성 패턴 |
| EV-A71 | semantic change | AI | 0.260 | VP1 항원 표면의 기능적 변화 포착 |
| Rabies | stability | AI | 0.248 | G 단백질 pH 의존 구조 전환 제약 |
| SARS-CoV-2 | Tranception | AI | 0.211 | 얕은 팬데믹 계통, PLM이 넓은 진화 맥락 보상 |
| RSV | ESM-2 LLR | AI | 0.196 | 제한된 계통 다양성, PLM이 대안 신호 |
| MERS | freq | 빈도 | 0.196 | 희소 게놈에서 빈도가 가장 안정적 |

**6개 정보 카테고리가 모두 최소 1개 바이러스에서 최적**으로 선택됨. 이는 특정 카테고리를 배제할 근거가 없음을 의미한다.

### 결과 3: 만능 방법은 없다 (3중 통계 검증)

| 검증 방법 | 결과 | 의미 |
|----------|------|------|
| ANOVA | ω² = 0.296 (최대 분산원) | scoring×pathogen 상호작용이 성능을 지배 |
| Friedman 검정 | χ²=7.69, p=0.990, W=0.037 | 상위 20개 조합 간 유의한 차이 없음 |
| LOPO 교차검증 | 0/11 일치, gap=0.265 | 10개로 학습한 최적을 나머지 1개에 적용 불가 |
| 고유 최적 조합 | 11/11 | 11개 바이러스 모두 다른 최적 (순열 맥락: 93% 우연 가능 → MCC gap이 본질) |

### 결과 4: 다중 정보 통합 → 실험 탐색 범위 축소

탐지된 핫스팟과 실험적으로 확인된 백신 escape 위치의 일치를 3개 병원체에서 검증 (20 scoring × 39 detector = 2,340회 평가):

| 병원체 | 최적 scoring | Enrichment | p값 | 비고 |
|--------|-------------|-----------|-----|------|
| H3N2 | FUBAR Bayes factor | **9.36배** | < 0.0001 | 9/29 antigenic drift 위치 포착 |
| HIV-1 | freq | **7.19배** | < 0.0001 | 23/45 항체 escape 위치 포착 |
| SARS-CoV-2 | FUBAR pos. sel. | **7.63배** | 0.026 | 2/30 escape 위치 포착 |
| H3N2 (EqualWeight 통합) | 10가지 통합 | **4.01배** | 0.0023 | antigenic site A+B 모두 포착 |
| H3N2 (빈도만) | FreqThresh | 2.7배 | 0.055 (비유의) | site B 놓침 |

**핵심 발견**: Layer A 벤치마크에서 최적으로 식별된 scoring 유형(H3N2→FUBAR, HIV-1→freq)이 vaccine escape enrichment에서도 최적. 이 교차 검증은 Layer A가 순환적 편향이 아닌 실제 생물학적 신호를 포착함을 독립적으로 확인한다.

다중 정보 통합(EqualWeight)은 빈도만으로 놓치는 구조적으로 제약된 항원 위치(H3N2 site B: positions 160, 186)를 추가로 포착하여, 단일 정보 접근보다 실험 탐색 범위를 더 효과적으로 축소한다.

### 결과 5: Layer C (DMS) 독립 검증

6개 병원체에서 Layer A (문헌 기반)와 Layer C (DMS 실험)의 최적 scoring이 다른지 비교:

| 바이러스 | Best (Layer A) | Best (Layer C) | 순위 상관 | DMS 출처 |
|---------|---------------|---------------|----------|---------|
| SARS-CoV-2 | tranception | plddt_inv | rho=−0.13 | Dadonaite 2024, *Nature* |
| H3N2 | fubar_bf | semantic_change | rho=−0.11 | Lee 2018, *PNAS* |
| HIV-1 | entropy | fubar | rho=0.27 | Haddox 2018, *eLife* |
| RSV | esm2_llr | EVEscape composite | rho=0.85 | Bloom lab 2026, *bioRxiv* |
| Rabies | stability | homoplasy | rho=0.86 | Aditham 2025, *Cell Host & Microbe* |
| EV-A71 | semantic_change | plddt_inv | rho=−0.18 | Bakhache 2025, *Nat Microbiology* |

4/6 병원체에서 Layer A와 C의 순위 상관이 비유의. 이는 두 Layer가 다른 생물학적 측면을 측정하고 있음을 확인하며, Layer A 기반 벤치마크 결과가 특정 정보 유형에 편향되지 않았음을 지지한다. EVEREST(Marks lab, 2025)도 동일한 6개 병원체에서 DMS가 없으며, 나머지 5개 병원체(Norovirus, Influenza B, MERS, HCV, Dengue)는 현재 전 세계적으로 해당 표적 단백질의 DMS 데이터가 존재하지 않는다.

### 결과 6: 10개 Feature 통합 분석

Per-feature AUC 분석 (11 병원체 × 10 feature):

| 바이러스 | 최적 feature | AUC |
|---------|------------|-----|
| Norovirus | homoplasy | **0.944** |
| H3N2 | pLDDT | 0.787 |
| HIV-1 | entropy | 0.730 |
| MERS | ESM-2 LLR | 0.695 |
| HCV | dN/dS proxy | 0.680 |
| Rabies | pLDDT | 0.650 |
| EV-A71 | ESM-2 LLR | 0.596 |
| SARS-CoV-2 | ESM-2 LLR | 0.586 |

**5가지 서로 다른 최적 feature**가 11개 병원체에서 관찰됨.

Random Forest 다변량 모델은 단변량 AUC를 대폭 초과 (Norovirus: 0.944→0.899, MERS: 0.695→0.875). Feature 제거 분석에서 **homoplasy**가 가장 중요. **4개 feature**(homoplasy, pLDDT, entropy, freq)만으로 전체의 **98% 성능** 달성.

---

## 실용적 가치

### 실험실 우선순위 제공

핫스팟 탐지의 최종 목적은 실험 검증 후보의 순위 리스트를 제공하는 것이다. 최적 scoring-detection 조합으로 탐지된 핫스팟은:
- H3N2: 29개 antigenic drift 위치 중 9개를 **9.36배** enrichment로 포착 (p < 0.0001)
- HIV-1: 45개 항체 escape 위치 중 23개를 **7.19배** enrichment로 포착 (p < 0.0001)
- SARS-CoV-2: **4.90배** enrichment (p < 0.0001)

### 새 바이러스 적용 워크플로 (~15-20분/병원체)

| 단계 | 소요 시간 | 내용 |
|------|----------|------|
| 1. 서열 수집 + MSA | ~5분 | NCBI/GISAID에서 200+ 서열, MAFFT 정렬 |
| 2. Feature 계산 | ~10분 | 빈도/엔트로피(초), homoplasy(2-5분), ESM-2(3-5분, GPU) |
| 3. Scoring 선택 | 즉시 | 바이러스 패밀리별 추천 테이블 참조 |
| 4. Detection + 평가 | ~30초 | KDE/Wavelet 권장 → 상위 후보 리스트 출력 |

### 바이러스 패밀리별 추천

| 패밀리 | 대표 바이러스 | 추천 scoring | 근거 |
|--------|-------------|-------------|------|
| Orthomyxoviridae | 인플루엔자 A/B | 계통 (FUBAR) | 깊은 계통수, 양성선택 신호 강함 |
| Coronaviridae | SARS-CoV-2, MERS | AI (PLM) | 얕은 계통, PLM이 넓은 진화 맥락 보상 |
| Caliciviridae | Norovirus | MSA (homoplasy) | 에포크 진화로 수렴 변이 패턴 현저 |
| Retroviridae | HIV | MSA (entropy) | 높은 다양성, 엔트로피가 변이 분포 포착 |
| Flaviviridae | HCV, Dengue | 빈도 기반 | 과변이 영역이 지배적 신호 |
| Pneumoviridae | RSV | AI (ESM-2) | 제한된 계통 다양성, PLM이 대안 신호 |

---

## 기여

| # | 기여 | 내용 | 핵심 수치 |
|---|------|------|----------|
| 1 | **MutBench 프레임워크** | 바이러스 핫스팟 탐지 분야 최초의 체계적 벤치마크. 3층 GT, 복합 평가 지표, 2단계 설계 | 8,580회 평가, 11 병원체 |
| 2 | **통계적 입증** | "어떤 정보가 어떤 바이러스에 맞는가"가 핵심임을 3가지 독립 통계로 입증. Vaccine escape 교차 검증으로 Layer A 타당성 확인 | ω²=0.296, W=0.037, LOPO 0/11 |
| 3 | **정보 유형 분석** | 20 scoring (6카테고리)에서 9가지 서로 다른 최적 유형 발견. 다중 정보 통합으로 실험 탐색 범위 축소 검증 | 최대 9.36배 enrichment, 4 feature로 98% |

---

## 한계

| 한계 | 심각도 | 현재 대응 |
|------|--------|----------|
| Layer A 정의 이질성 (병원체마다 다른 기준) | 중 | Layer C 독립 검증 (6/11) + vaccine escape 교차 검증 + 같은 과 내에서도 최적 상이 |
| DMS 데이터는 6/11 병원체만 존재 | 중 | EVEREST도 동일 공백. Layer A가 주 평가, DMS는 보조 검증 |
| 11개 바이러스의 계통적 비독립성 | 중 | 3개 과 쌍(Coronaviridae, Orthomyxoviridae, Flaviviridae) 내에서도 최적 scoring 상이 |
| 일부 scoring 유형이 동일 정보원에서 파생 | 하 | 6-카테고리 ANOVA ω²=0.103으로 카테고리 수준에서도 일관된 결과 확인 |
| RNA 바이러스만 검증 (DNA 바이러스 미포함) | 하 | 6개 주요 RNA 바이러스 과 커버. DNA 바이러스는 변이율이 낮아 H-score 전제와 불일치 |

---

## 논문 구성 (6장, 169페이지)

| 장 | 제목 | 내용 |
|---|------|------|
| 1 | Introduction | 핫스팟 탐지 3단계 프로세스, 3가지 공백, 3가지 기여 |
| 2 | Related Research | 기존 방법(빈도/엔트로피/MutClust) + VEP 벤치마크(EVEREST, ProteinGym, EVEscape) + 벤치마크 비교 테이블 + 공백 확인 |
| 3 | Methods | 11 바이러스, 3층 GT, 20 scoring(6카테고리), 39 detector(14 families), ANOVA/Friedman/LOPO 통계 설계 |
| 4 | Results | Stage 1 (SARS-CoV-2 검증, hotspot-score 0.778) + Stage 2 (8,580 evals, scoring×pathogen = 최대 분산원) + 정보 유형 분석 (10 feature, RF, ablation) + vaccine escape 교차 검증 + Layer C 독립 검증 |
| 5 | Discussion | 방법론 타당성, H-score 한계, Layer A 이질성 대응, ESM-2 데이터 중복, GISAID 편향, 계통 비독립성, 실용 워크플로 |
| 6 | Conclusion | 3가지 기여 요약, 한계, 미래 방향 (적응적 방법 선택, DNA 바이러스 확장, 계통 보정 통합) |
