# 논문 심층 정리: MOSD 프레임워크를 통한 다중오믹스 통합 연구 설계 가이드라인

---

## 1. 논문 기본정보

| 항목 | 내용 |
|------|------|
| **제목** | A review on multi-omics integration for aiding study design of large scale TCGA cancer datasets |
| **저자** | Eonyong Han<sup>1,dagger</sup>, Hwijun Kwon<sup>1,dagger</sup>, Inuk Jung<sup>1,*</sup> (<sup>dagger</sup>공동 제1저자) |
| **소속** | School of Computer Science and Engineering, Kyungpook National University, Buk-gu, Daegu 41566, Republic of Korea |
| **저널** | BMC Genomics (2025) 26:769 |
| **DOI** | [10.1186/s12864-025-11925-y](https://doi.org/10.1186/s12864-025-11925-y) |
| **게재일** | 접수 2025.03.12 / 승인 2025.07.18 / 온라인 2025.08.22 |
| **코드 저장소** | [https://github.com/cobi-git/MOPARAM](https://github.com/cobi-git/MOPARAM) |
| **라이선스** | Creative Commons Attribution-NonCommercial-NoDerivatives 4.0 International |
| **키워드** | Multi-omics, Integration, Study design, Machine learning |

---

## 2. 연구 배경 및 동기

### 2.1 다중오믹스 통합(Multi-Omics Integration, MOI)의 중요성

고처리량 시퀀싱(High-throughput sequencing) 기술의 급격한 발전으로, 유전체학(Genomics), 전사체학(Transcriptomics), 후성유전체학(Epigenomics), 단백질체학(Proteomics), 대사체학(Metabolomics) 등 다양한 오믹스 데이터의 동시 생산이 가능해졌다. 다중오믹스 통합(MOI)은 이러한 다층적 생물학적 데이터를 결합하여 암과 같은 복잡 질환의 분자적 기전을 포괄적으로 이해하는 데 핵심적인 역할을 한다.

MOI의 핵심 가치는 다음과 같다:
- **상보적 정보 제공**: 서로 다른 오믹스 계층은 상호 보완적인 생물학적 신호를 제공하며, 때로는 상충하는 신호를 보일 수도 있다. 예를 들어, 대장직장암(Colorectal carcinoma) 연구에서 메틸화 프로파일은 유전적 계통(Genetic lineages)과 연관되었으나, 전사 프로그램은 아클론(Subclonal) 수준의 유전적 정체성과 불일치하는 연결을 보였다.
- **질병 메커니즘의 다층적 해석**: 단일 오믹스로는 포착할 수 없는 복잡한 조절 네트워크와 분자적 상호작용을 밝힐 수 있다.
- **임상적 활용 가능성**: 암 서브타입(Cancer subtype) 분류, 예후 예측, 치료 반응 예측 등에 활용 가능하다.

### 2.2 기존 벤치마크 연구의 한계

기존 연구들은 MOI 분석에서 다음과 같은 주요 도전과제를 개별적으로 다루어 왔다:
- **차원의 저주(Curse of dimensionality)**: 오믹스 데이터의 특성(Feature) 수가 샘플 수를 크게 초과하는 문제
- **데이터 이질성(Data heterogeneity)**: 오믹스 유형별로 측정 단위, 분포, 스케일이 상이
- **결측 데이터(Missing data)**: 다중 오믹스 계층 간 샘플 매칭 불완전성
- **클래스 불균형(Class imbalances)**: 특정 암 서브타입의 환자 수가 극단적으로 적은 경우
- **확장성(Scalability)**: 대규모 데이터셋 처리의 계산적 부담

그러나 이러한 연구들은 각각 1~3개의 요인만을 독립적으로 조사하였으며, **요인 간 상호작용을 고려한 통합적 프레임워크를 제시하지 못했다**.

### 2.3 연구의 필요성

본 연구의 핵심 동기는 다음과 같다:
1. **통합 가이드라인의 부재**: 연구자가 MOI 분석을 설계할 때 참고할 수 있는 체계적인 Study Design 가이드라인이 존재하지 않았다.
2. **분산된 지식의 통합 필요**: 개별 벤치마크 연구에서 얻은 통찰을 하나의 일관된 프레임워크로 정리할 필요가 있었다.
3. **실용적 권고사항의 필요**: 적절한 샘플 수, 특성 선택 비율, 전처리 전략, 오믹스 조합 등에 대한 구체적이고 정량적인 권고가 필요했다.

---

## 3. 선행연구 분석

### 3.1 각 선행연구별 상세 비교

#### (1) Mirza et al. (2019) [27]

| 항목 | 내용 |
|------|------|
| **초점** | MOI의 5가지 핵심 도전과제 정의 |
| **내용** | 차원의 저주, 데이터 이질성, 결측 데이터, 클래스 불균형, 확장성을 MOI의 주요 도전과제로 최초 체계화 |
| **기여** | 본 연구의 MOSD 프레임워크 설계를 위한 개념적 토대 제공 |
| **한계** | 도전과제를 정의하는 데 그쳤으며, 구체적인 벤치마크나 가이드라인을 제시하지 않음 |

#### (2) Chauvel et al. (2020) [28]

| 항목 | 내용 |
|------|------|
| **초점** | 샘플 크기(Sample size)가 클러스터링 성능에 미치는 영향 |
| **데이터** | TCGA-BRCA (348명), 시뮬레이션 데이터 |
| **오믹스** | mRNA, miRNA, Methylation, Protein |
| **방법** | BCC, MDI, iCluster, moCluster, JiVE, iNMF (6개) |
| **평가지표** | ARI (Adjusted Rand Index) |
| **주요 발견** | 샘플 수에 따른 클러스터링 성능 변화 패턴 확인 |
| **한계** | **단일 암종(BRCA)**만 사용하여 일반화 제한; Feature selection, Noise, Balance 등 미검토 |

#### (3) Rappoport & Shamir (2018, 2019) [30]

| 항목 | 내용 |
|------|------|
| **초점** | MOI 방법의 포괄적 벤치마크 |
| **데이터** | TCGA 10개 암종 (AML, BIC, COAD, GBM, KIRC, LIHC, LUSC, SKCM, OV, SARC) |
| **오믹스** | GE, ME, MI |
| **방법** | Spectral, LRAcluster, PINS, SNF, MKL-LPP, MCCA, MultiNMF, iClusterBayes 등 (9개) |
| **평가지표** | Survival analysis (log-rank), Clinical distribution |
| **주요 발견** | 노이즈(Noise), 불균형(Balance), 서브타입(Subtype) 요인에 대한 개별 테스트 수행 |
| **한계** | 각 요인에 대해 **단일 테스트**만 수행하여 요인 간 상호작용 미반영; MOI 방법 성능 개선을 위한 조건을 충분히 파악하지 못함 |

#### (4) Pierre-Jean et al. (2020) [29]

| 항목 | 내용 |
|------|------|
| **초점** | Feature selection이 MOI 성능에 미치는 영향 |
| **데이터** | BXD (64), Obesity (13), Liver cancer (360) - 시뮬레이션 중심 |
| **오믹스** | GE, ME, CNV, Mutation |
| **방법** | RGCCA, intNMF, SNF 등 포함 13개 비지도학습 방법 |
| **평가지표** | F-measure, ARI, Survival analysis |
| **주요 발견** | Feature selection의 비율이 클러스터링 품질에 유의미한 영향; 가우시안(Gaussian), 이진(Binary), 베타유사(Beta-like) 표현 등 시뮬레이션 데이터셋으로 검증 |
| **한계** | **시뮬레이션 중심** 설계로 실제 임상 데이터에의 적용성 검증 부족; 다른 요인(Sample size, Noise 등) 미검토 |

#### (5) Tini et al. (2019) [24]

| 항목 | 내용 |
|------|------|
| **초점** | 비지도 클러스터링 방법론 비교 |
| **데이터** | BXD (66명, 마우스 간), Platelet (12명, 혈소판 반응성), BRCA (491명, 유방암) — 3개 데이터셋 |
| **오믹스** | GE, ME, MI |
| **방법** | MCCA, JiVE, MCIA, MFA, SNF (5개) |
| **평가지표** | F-measure |
| **주요 발견** | Feature selection과 Noise가 클러스터링 성능에 미치는 영향 일부 확인; 샘플 크기에 대한 부분적 분석 |
| **한계** | Feature selection 방법이 변동계수(Coefficient of variation) 기반 필터링에 한정되어 최적 특성 수 결정에 제한적; Noise 적용 방식이 제한적 |

#### (6) Duan et al. (2021) [31]

| 항목 | 내용 |
|------|------|
| **초점** | 다중오믹스 데이터 통합 방법의 평가 및 비교 |
| **데이터** | TCGA 9개 암종 (ACC, BRCA, COAD, KIRP, KIRC, LIHC, LUAD, LUSC, THYM) |
| **오믹스** | GE, ME, MI, CNV |
| **방법** | LRAcluster, PINSPlus, CC, MCIA, mixKernel, SGCCA, iClusterPlus, MoCluster, CiMLR, MOFA, SNF, NEMO, CMLR, MultiNMF, PFA 등 (10+개) |
| **평가지표** | Precision, NMI, ARI, F-measure |
| **주요 발견** | 4종 오믹스에서 11가지 조합을 테스트하여 최적 오믹스 조합 탐색; 임상 특성(Subtype, Gender, Stage, Age) 연관 분석; Noise, Balance 요인 일부 검토 |
| **한계** | 9가지 요인을 통합한 **일관된 가이드라인 미제공**; Sample size, Feature selection 등 핵심 계산적 요인 체계적 미검토 |

### 3.2 선행연구 종합 비교표

| 연구 | 샘플크기 | 특성선택 | 전처리 | 노이즈 | 균형 | 클래스수 | 서브타입 | 오믹스조합 | 임상특성 | 데이터 | 방법수 | 평가지표 |
|------|:------:|:------:|:----:|:-----:|:---:|:------:|:------:|:-------:|:------:|------|:-----:|--------|
| Chauvel [28] | S | S | X | S | X | S | X | X | X | BRCA(348) | 6 | ARI |
| Rappoport [30] | X | X | X | X | X | O | X | X | O | TCGA 10종 | 9 | Survival, Clinical |
| Pierre-Jean [29] | S | S | S | O | S | S | X | O | O | BXD 등 3종 | 13 | F-measure, ARI |
| Tini [24] | S | O | X | O | X | S | X | O | O | BXD(66), Platelet(12), BRCA(491) | 5 | F-measure |
| Duan [31] | X | O | X | O | X | O | X | O | X | TCGA 9종 | 10+ | Precision, NMI, ARI, F |
| **본 연구 (MOSD)** | **X** | **X** | **X** | **X** | **X** | **X** | **X** | **X** | **X** | **TCGA 10종** | **10** | **ARI, NMI, F, cluster-score** |

> **범례**: X = 주요 요인으로 체계적 분석, O = 부분적으로 다룸, S = 시뮬레이션이나 간접적으로 다룸, 빈칸 = 미다룸

### 3.3 선행연구 대비 본 연구의 차별점

| 차별점 | 설명 |
|--------|------|
| **최초의 통합 프레임워크** | 9가지 요인(계산적 6개 + 생물학적 3개)을 단일 프레임워크(MOSD)로 체계화한 최초의 연구 |
| **포괄적 벤치마크 설계** | 7가지 벤치마크 테스트를 설계하여 각 요인의 영향을 체계적으로 분리 평가 (변수 통제 설계) |
| **다중 암종 적용** | TCGA 10개 암종, 3,988명 환자 데이터에 대해 동일한 프레임워크를 적용하여 일반화 가능성 확보 |
| **다중 평가지표** | ARI, NMI, F-measure 3가지를 통합한 cluster-score를 도입하여 단일 지표의 편향 방지 |
| **정량적 가이드라인** | "클래스당 최소 26개 샘플", "전체 특성의 1~10% 선택", "노이즈 30% 이하" 등 구체적 수치 기반 권고 제공 |
| **선행연구 한계 해결** | Chauvel의 단일 암종 한계, Rappoport의 단일 테스트 한계, Pierre-Jean의 시뮬레이션 한계, Tini의 제한적 Feature selection, Duan의 통합 가이드라인 부재를 모두 해소 |

---

## 4. 연구 방법론

### 4.1 MOSD 프레임워크 개요

MOSD(Multi-Omics Study Design)는 다중오믹스 통합 분석의 설계를 체계적으로 안내하기 위한 포괄적 프레임워크이다. 핵심 구조는 다음과 같다:

```
MOSD Framework
├── Computational Factors (계산적 요인, 6개)
│   ├── (1) Sample size (샘플 크기)
│   ├── (2) Feature selection (특성 선택)
│   ├── (3) Preprocessing strategy (전처리 전략)
│   ├── (4) Noise characterization (노이즈 특성화)
│   ├── (5) Class balance (클래스 균형)
│   └── (6) Number of classes (클래스 수)
│
└── Biological Factors (생물학적 요인, 3개)
    ├── (7) Cancer subtype combination (암 서브타입 조합)
    ├── (8) Omics combination (오믹스 조합)
    └── (9) Clinical feature correlation (임상 특성 연관성)
```

프레임워크의 검증은 **7가지 벤치마크 테스트**를 통해 수행되었으며, 각 테스트는 하나의 요인을 분리하여 평가하되 다른 변수를 고정(Default setting)하는 통제된 실험 설계를 따랐다. 각 벤치마크는 10회 반복(Random sample selection)을 통해 통계적 견고성을 확보하였다.

### 4.2 9가지 요인 상세 설명

#### 계산적 요인 (Computational Factors)

**(1) Sample Size (샘플 크기)**

MOI에서 차원의 저주(Curse of dimensionality)와 확장성(Scalability) 문제를 동시에 다루는 요인이다.

- **테스트 설계**: 클래스당 최소 5개에서 최대 샘플 수까지 점진적으로 증가시키며 성능 변화를 관찰. 간격(Interval)은 3으로 설정.
- **핵심 발견**: 클래스당 26개 이상에서 성능 분산이 현저히 감소하며 안정화. 평균 cluster-score는 약 0.5에서 0.55 범위로 완만한 상승을 보이나, 최소 점수(Minimum score)가 크게 개선되어 저성능 결과의 발생을 방지.
- **의의**: 절대적 성능 향상보다는 **결과의 일관성(Consistency)** 확보가 샘플 크기 증가의 주된 효과.

**(2) Feature Selection (특성 선택)**

오믹스 데이터에서 생물학적으로 관련된 특성을 선별하는 과정이다.

- **방법**: Chi-square test를 GE, MI, ME에 적용 (그룹 레이블 기반으로 특성과 클래스 간 독립성 검정). ANOVA를 CNV에 적용 (음수값 포함으로 Chi-square 부적합).
- **테스트 설계**: 1%부터 100%까지 단계적으로 특성 비율 증가. 초기 단계는 1% 간격, 10% 이후는 10% 간격.
- **핵심 발견**: **전체 특성의 1~10% 선택 시 최적 성능** (평균 cluster-score 약 0.55). 20~50%에서 점진적 하락, 60~100%에서 현저한 저하 (평균 약 0.4). 전체 특성 대비 **최대 34% 성능 향상**.
- **선택 근거**: 분산 기반(Variance-based)이나 모델 특정적(Model-specific) 방법 대신 그룹 정보 기반 방법을 채택하여 알고리즘 비의존적(Algorithm-agnostic) 특성 확보.

**(3) Preprocessing Strategy (전처리 전략)**

다중오믹스 데이터의 이질성을 해소하기 위한 데이터 변환 방법이다.

| 전처리 유형 | 방법 | 설명 |
|-----------|------|------|
| **RAW** | log2 변환 | 원본 데이터의 고유 구조를 보존하면서 기본적 계산 분석 가능 |
| **NORM** | Quantile normalization + Min-Max (0-1) scaling | 오믹스 계층 간 균일한 분포를 형성하여 표준화된 비교 촉진 |
| **GL** (Gene Level) | 유전자 수준 통합 | 정규화 데이터를 유전자 수준으로 평균화. ME는 프로모터 상류 2kb 내 CpG probe의 beta 값 평균, MI는 표적 유전자의 기하평균, CNV는 유전자 영역 내 세그먼트 값 평균 |

- **핵심 발견**: 전처리 간 성능 차이가 대부분 **0.1 미만**으로 미미. NORM이 전반적으로 약간 우세하나, 성별(Gender) 분석에서는 +0.20~+0.27의 유의미한 향상. 암종별로 선호하는 전처리가 상이 (예: LUAD - GL 선호, STAD - NORM 선호). RAW가 BLCA, BRCA, KIRP의 노이즈 내성 테스트에서 오히려 우세한 경우도 있음 (정규화가 관련 생물학적 특성을 약화시킬 가능성).

**(4) Noise Characterization (노이즈 특성화)**

기술적, 생물학적 원인에 의한 데이터 오류가 MOI 결과에 미치는 영향을 평가하는 요인이다.

- **테스트 설계**: 가우시안 노이즈(Gaussian noise)를 GE, MI, ME, CNV 각 오믹스 계층에 10% 단위로 10%~100%까지 도입.
- **핵심 발견**:
  - **0~50%**: 안정적 성능 유지 (cluster-score 약 0.5 유지)
  - **50~80%**: 점진적 하락 시작
  - **80% 이상**: 급격한 성능 붕괴 (cluster-score 0.10 이하), MOI 방법과 무관하게 신뢰할 수 없는 클러스터링
  - **권장**: 노이즈 수준 **30% 이하** 유지
- **흥미로운 관찰**: 고노이즈 수준에서 성능 분산이 오히려 감소 -- 높은 노이즈가 결과를 예측 가능하게(다만 저품질로) 만듦.

**(5) Class Balance (클래스 균형)**

암 서브타입이나 임상 범주 간 샘플 수의 불균형이 클러스터링 성능에 미치는 영향이다.

- **테스트 설계**: 균형 상태에서 시작하여 점진적으로 불균형을 도입. 불균형 비율(Imbalance ratio)을 체계적으로 변화.
- **핵심 발견**: 불균형 비율 **3:1 초과 시 유의미한 성능 저하** (adj. p < 0.0001). 균형 클래스(< 3:1): 평균 cluster-score 약 0.58, 넓은 상위 분포. 불균형 클래스(> 3:1): 평균 약 0.52, 이중 모드(Bimodal) 분포로 두 가지 성능 패턴 출현.
- **의의**: Mirza et al. [27]이 클래스 불균형을 MOI의 도전과제로 정의한 것을 확장하여, **구체적 임계값(3:1)**을 제시.

**(6) Number of Classes (클래스 수)**

서브타입 수 증가가 클러스터링 난이도에 미치는 영향이다.

- **테스트 설계**: 최소 2개에서 최대 서브타입 수까지 조합을 변화시키며 평가. 모든 테스트는 최소 2개의 구별되는 서브타입 레이블을 포함하는 데이터셋에서 수행.
- **핵심 발견**: 서브타입 수 증가 시 **점진적 성능 하락**. 분자적으로 유사한 서브타입이 포함될수록 난이도 급증 (예: BRCA LumA-LumB 구별이 LumB-Basal 구별보다 훨씬 어려움). iClusterPlus는 다중 서브타입 구별에서 일관되게 낮은 성능을 보임.

#### 생물학적 요인 (Biological Factors)

**(7) Cancer Subtype Combination (암 서브타입 조합)**

어떤 서브타입 조합이 클러스터링 성능에 영향을 미치는지 평가하는 요인이다.

- **핵심 발견**: 분자적으로 구별 가능한(Molecularly distinct) 서브타입 쌍이 높은 클러스터링 성능을 보임.
  - **고성능 조합 예시**: BRCA Luminal B vs. Basal (cluster-score > 0.90), STAD CIN vs. EBV (cluster-score > 0.90)
  - **저성능 조합 예시**: BRCA Luminal A vs. Luminal B (에스트로겐 수용체 양성 및 유사한 발현 프로파일 공유), COAD CMS2 vs. CMS3 (유사한 상피 특성 및 겹치는 유전체 특성)
- **의의**: 연구 설계 시 **분자적으로 뚜렷한 서브타입을 우선 선택**해야 신뢰할 수 있는 클러스터링 결과를 얻을 수 있음을 실증적으로 확인.

**(8) Omics Combination (오믹스 조합)**

어떤 오믹스 계층의 조합이 특정 임상 특성 분석에 가장 효과적인지 평가하는 요인이다.

- **테스트 설계**: 단일 오믹스(GE 단독)부터 전체 조합(GE-ME-MI-CNV)까지 11가지 조합을 4가지 임상 특성(Subtype, Gender, Stage, Age)에 대해 테스트.
- **핵심 발견**:
  - **GE-ME 조합**이 전반적으로 가장 효과적인 오믹스 쌍으로 부상, 특히 서브타입 분석에서 우수
  - **CNV 포함 조합**은 종종 성능 저하를 유발
  - GE-MI도 서브타입에 유익하나, 다른 임상 특성에서는 일관되지 않음
  - 오믹스 계층 추가가 자동적으로 성능을 향상시키지 않음 -- 비선형적 관계(Non-linear relationships)로 인해 특정 임상 특성에서 오히려 이질성 증폭 가능
- **방법별 차이**: SNF, COCA, NEMO는 GE-ME 사용 시 Gender 분류에 일관된 강점; iCluster, MOFA는 다른 맥락이나 임상 변수에서 우수할 수 있음.

**(9) Clinical Feature Correlation (임상 특성 연관성)**

MOI 결과와 다양한 임상 특성 간의 연관성 강도를 평가하는 요인이다.

- **평가 대상 임상 특성**: Molecular subtype, Gender, Pathological stage, Age
- **핵심 발견**:
  - **Subtype**: 가장 강한 클러스터링 신호를 보임 -- 분자적 서브타입이 오믹스 데이터에 가장 직접적으로 반영
  - **Gender**: 성별 기반 분자적 패턴이 일부 암종에서 잘 포착됨 (BRCA 제외 -- 극단적 성별 불균형으로 분석 제외)
  - **Pathological stage**: 가장 도전적인 임상 특성 -- 전반적으로 낮은 cluster-score, 좁은 분포
  - **Age**: 중간 수준의 난이도

### 4.3 사용 데이터

#### TCGA 10개 암종 (총 3,988명)

| 암종 약어 | 암종명 (영문) | 환자 수 | GE 특성 수 | ME 특성 수 | MI 특성 수 | CNV 특성 수 | 서브타입 수 |
|---------|-----------|:------:|:--------:|:--------:|:--------:|:---------:|:--------:|
| BLCA | Bladder Urothelial Carcinoma | 400 | 17,390 | 396,065 | 2,195 | 21,933 | 4 |
| BRCA | Breast Invasive Carcinoma | 592 | - | - | 2,222 | - | 4 (PAM50) |
| COAD | Colon Adenocarcinoma | 249 | - | - | 2,097 | - | 4 (CMS) |
| HNSC | Head and Neck Squamous Cell Carcinoma | 471 | - | - | 2,229 | - | 4 |
| KIRP | Kidney Renal Papillary Cell Carcinoma | 268 | - | - | 2,099 | - | 3 |
| LIHC | Liver Hepatocellular Carcinoma | 357 | 17,390 | - | 2,157 | - | 3 |
| LUAD | Lung Adenocarcinoma | 442 | - | - | 2,211 | - | 6 |
| SKCM | Skin Cutaneous Melanoma | 350 | - | - | 2,203 | - | 4 |
| STAD | Stomach Adenocarcinoma | 365 | - | - | 2,161 | - | 4 |
| THCA | Thyroid Carcinoma | 494 | - | - | 2,201 | - | 5 |

- **선택 기준**: 환자 매칭 오믹스 및 임상 데이터 가용성, 암종당 최소 100명 이상의 환자 (견고한 통계 분석 보장)
- **데이터 소스**: UCSC Xena browser [35], TCGAbiolinks [36]를 통한 바코드 검증
- **4종 오믹스**: Gene Expression (GE), Methylation (ME), miRNA (MI), Copy Number Variation (CNV)
- **임상 특성**: Molecular subtype, Gender, Pathological stage (I-IV), Age (Young 0-39, Middle 40-64, Old 65+)
- **결측 처리**: 결측값이 포함된 오믹스 특성을 완전 제거하는 보수적 접근법 채택 (No imputation). 10명 미만의 샘플 그룹도 제외.

### 4.4 10개 MOI 방법 설명

10개 방법은 구현의 용이성, 학술적 보급도, R/Python 구현 가용성, 기본 파라미터(Default parameters)로의 실행 효과성 등 3가지 기준으로 선정되었다.

| 방법 | 약어 | 핵심 접근법 | MOSD에서의 강점 |
|------|-----|----------|-------------|
| **Similarity Network Fusion** | SNF [40] | 각 오믹스에서 유사도 네트워크 구축 후 융합 | 이산형/연속형 임상 특성 모두 처리, 소규모 샘플 내성 |
| **Spectrum** | Spectrum [41] | 밀도 인식 스펙트럴 클러스터링, k-NN 그래프 + GMM | 대규모 데이터 확장성, 미세한 밀도 변화 포착 |
| **PINSPlus** | PP [42,43] | 각 오믹스 계층별 연결성 그래프(Connectivity graph) 구축 후 융합 | 기존/신규 서브타입 탐지 가능, 임상적 함의 |
| **COCA** | COCA [45] | 각 오믹스를 one-hot 클러스터 행렬로 변환 후 합의(Consensus) 클러스터링 | 교차 오믹스 상관 식별, 엄격한 정규화 불필요 |
| **LRAcluster** | LRAcluster [46] | 저랭크 근사(Low-rank approximation), 가우시안 분포 가정 | 고차원 데이터 압축, 공유 공분산 구조 탐지 |
| **Consensus Clustering** | CC [47] | 반복적 리샘플링 + 합의 솔루션 도출 | 고차원/이질적 데이터에 강건, 클러스터 안정성 평가 |
| **MOFA** | MOFA [48] | 다중오믹스를 잠재 인자(Latent factors)로 분해, 선형 인자 모델 | 결측 데이터 통합, 이상치(Outlier) 식별, 해석 가능성 |
| **NEMO** | NEMO [44] | 오믹스별 쌍별 거리 계산 + k-NN 그래프 + 그래프 기반 클러스터링 | 부분 데이터(Partial datasets) 우수, 결측 보정 불필요, 빠른 실행 |
| **IntNMF** | IntNMF [51,52] | 공유 기저 행렬(Basis matrix) W + 오믹스별 계수 행렬 H, 비음수 행렬 분해 | 대규모 데이터, 분포 가정 불필요, 교차검증 기반 클러스터 수 선택 |
| **iClusterPlus** | iClusterPlus [49,50] | 확률론적 결합 잠재변수 모델, Lasso 페널티(L1-norm) | 차원 축소 + 비정보적 특성 제거, 이진/범주/연속형 데이터 통합 |

### 4.5 평가 지표

#### (1) Rand Index (RI) 및 Adjusted Rand Index (ARI)

클러스터링 정확도를 쌍별(Pairwise) 일치로 측정한다.

$$RI = \frac{TP + TN}{TP + FP + TN + FN}$$

- TP: 동일 클러스터에 올바르게 할당된 쌍
- TN: 다른 클러스터에 올바르게 할당된 쌍
- FP: 동일 클러스터에 잘못 할당된 쌍
- FN: 다른 클러스터에 잘못 할당된 쌍

$$ARI = \frac{RI - Expected(RI)}{Max(RI) - Expected(RI)}$$

- **범위**: [-1, 1], 1 = 완벽 일치, 0 = 랜덤 수준
- **특징**: 우연(Chance)에 의한 일치를 보정

#### (2) Normalized Mutual Information (NMI)

정보이론(Information theory)에 기반하여 진짜 레이블(T)과 클러스터링 결과(C) 간 공유 정보를 측정한다.

확률 분포 정의:

$$P(i) = \frac{|T_i|}{N}, \quad P'(j) = \frac{|C_j|}{N}, \quad P(i,j) = \frac{|T \cap C|}{N}$$

상호 정보량(Mutual Information):

$$MI = \sum_{i \in T} \sum_{j \in C} P(i,j) \log\left(\frac{P(i,j)}{P(i) \cdot P'(j)}\right)$$

엔트로피(Entropy):

$$H(T) = -\sum_{i \in T} P(i) \log(P(i)), \quad H(C) = -\sum_{j \in C} P'(j) \log(P'(j))$$

정규화:

$$NMI = \frac{MI(T,C)}{mean(H(T), H(C))}$$

- **범위**: [0, 1], 1 = 완벽 일치, 0 = 완전 랜덤

#### (3) F-measure (Pair-based)

집합 연산(Set operations) 기반의 쌍별 클러스터링 평가이다.

$$A = |Pairs(U) \cap Pairs(V)|$$
$$B = |Pairs(U) - Pairs(V)|$$
$$C = |Pairs(V) - Pairs(U)|$$

- U: 예측 클러스터, V: 진짜 클러스터
- Pairs(X): 집합 X 내 모든 가능한 원소 쌍

$$F\text{-}measure = \frac{2A}{2A + B + C}$$

#### (4) Cluster-score (통합 지표)

$$cluster\text{-}score = \frac{ARI + NMI + F\text{-}measure}{3}$$

- 세 지표의 **산술 평균**으로 계산
- 각 지표가 서로 다른 관점(우연 보정, 정보이론, 집합 기반)을 반영하므로 단일 지표 편향 방지
- 본 벤치마크에서 ARI 값이 모두 비음수였으므로 별도 정규화 없이 평균 가능
- **향후 고려**: ARI 음수값 발생 시 0-1 정규화 후 평균하는 방식 필요

### 4.6 벤치마크 설계

7가지 벤치마크 테스트의 전체 구조:

| 벤치마크 | 대상 요인 | 변화시키는 변수 | 고정 변수 | 반복 횟수 |
|---------|---------|------------|---------|:-------:|
| 1. Sample size test | 샘플 크기 | 클래스당 5~최대 (간격 3) | 전처리, 특성, 오믹스 조합 | 10 |
| 2. Feature selection test | 특성 비율 | 1%~100% (19단계) | 샘플 크기, 전처리, 오믹스 조합 | 10 |
| 3. Preprocessing test | 전처리 전략 | RAW, NORM, GL | 샘플 크기, 특성, 오믹스 조합 | 10 |
| 4. Noise tolerance test | 노이즈 수준 | 10%~100% (10단계) | 샘플 크기, 전처리, 특성 | 10 |
| 5. Class balance test | 불균형 비율 | 균형~최대 불균형 (11단계) | 전처리, 특성, 오믹스 조합 | 10 |
| 6. Cancer subtype combination test | 서브타입 조합 | 2개~최대 서브타입 조합 | 전처리, 특성, 샘플 크기 | 10 |
| 7. Omics combination test | 오믹스 조합 | 11가지 조합 (단일~전체) | 전처리, 특성, 샘플 크기 | 10 |

각 벤치마크는 **단일 요인 분리 원칙**을 따라 다른 모든 변수를 기본값(Default)으로 고정하여, 해당 요인의 고유한 영향을 정밀하게 측정하였다.

---

## 5. 핵심 결과

### 5.1 요인별 주요 발견

#### 계산적 요인 결과 요약

| 요인 | 핵심 발견 | 정량적 가이드라인 | 근거 |
|------|---------|-------------|------|
| **Sample size** | 26개 이상에서 분산 감소, 평균 성능은 완만한 상승 | 클래스당 최소 **26개** 샘플 | 26개 이후 violin plot 분포 현저히 좁아짐 |
| **Feature selection** | 적은 특성이 전체 특성 대비 우수, 최대 34% 향상 | 전체의 **1~10%** 선택 | 1-10%에서 평균 0.55, 90-100%에서 0.4 수준 |
| **Preprocessing** | 전처리 간 차이 대부분 < 0.1, NORM 약간 우세 | 암종/목적에 따라 선택, **전처리보다 다른 요인에 집중** 권장 | Gender 분석에서만 NORM이 +0.20~+0.27 |
| **Noise** | 0-50% 안정, 50-80% 점진 하락, 80%+ 급락 | 노이즈 **30% 이하** 유지 | 80% 초과 시 cluster-score < 0.10 |
| **Class balance** | 3:1 초과 시 유의미한 성능 저하 | 불균형 비율 **3:1 이하** 유지 | adj. p < 0.0001 (Wilcoxon 검정) |
| **Number of classes** | 서브타입 증가 시 점진적 하락, 유사 서브타입 포함 시 악화 | 뚜렷한 분자적 구별이 있는 서브타입 우선 | BRCA LumA-LumB 쌍에서 현저한 성능 저하 |

#### 생물학적 요인 결과 요약

| 요인 | 핵심 발견 | 권장사항 |
|------|---------|---------|
| **Cancer subtype combination** | 분자적으로 구별 가능한 서브타입 쌍이 높은 성능 (예: BRCA LumB-Basal > 0.90) | 연구 설계 시 분자적으로 뚜렷한 서브타입 조합을 우선 선택 |
| **Omics combination** | GE-ME가 가장 효과적, CNV 포함 시 종종 성능 저하 | Subtype 분석에는 **GE-ME** 조합 우선; 오믹스 추가가 자동으로 성능 향상을 의미하지 않음 |
| **Clinical feature** | Subtype에서 가장 강한 신호, Stage가 가장 도전적 | 분석 목적에 맞는 오믹스-방법 조합 선택 필요; Stage 분석은 근본적으로 어려움을 인지 |

### 5.2 방법별 성능 비교 (Table 3 기반)

| 테스트 시나리오 | Top Method | Runner-up | Notable Performer |
|-------------|-----------|-----------|------------------|
| **Sample size** | SNF (5/10) | NEMO (2/10) | PP (2/10) |
| **Feature selection** | SNF (4/10) | NEMO (2/10) | PP, CC (2/10 each) |
| **Balance** | SNF, NEMO (3/10 each) | PP (2/10) | CC (1/10) |
| **Noise tolerance** | PP (3/10) | SNF, NEMO, CC (2/10 each) | - |
| **Subtype combination** | SNF (5/10) | NEMO (2/10) | MOFA, CC (1/10 each) |
| **Omics (Subtype)** | NEMO (4/10) | SNF, Spectrum (2/10 each) | CC, IntNMF (1/10 each) |
| **Omics (Gender)** | CC (4/9) | LRAcluster (2/9) | SNF, COCA, IntNMF (1/9 each) |
| **Omics (Stage)** | NEMO (5/10) | PP, CC (2/10 each) | COCA (1/10) |
| **Omics (Age)** | NEMO (3/10) | IntNMF, CC, LRAcluster (2/10 each) | Spectrum (1/10) |

> 괄호 안의 숫자는 10개 암종 중 해당 방법이 최고 cluster-score를 달성한 횟수 (예: 5/10 = 10개 암종 중 5개에서 1위)

#### 방법별 강점 프로파일

| 방법 | 주요 강점 영역 | 약점 |
|------|----------|------|
| **SNF** | 구조적 테스트(Sample size, Feature selection, Subtype) 전반에서 일관된 강점 | 임상 특성 분석에서 상대적 약세 |
| **NEMO** | 임상 특성 분석(Stage, Age, Subtype omics)에서 탁월 | 일부 구조적 테스트에서 SNF에 열세 |
| **PP (PINSPlus)** | 노이즈 내성(Noise tolerance)에서 최강 | 다른 시나리오에서 2위 수준 |
| **CC** | 성별(Gender) 분석에서 특화된 강점 | 일부 구조적 테스트에서 중간 수준 |
| **LRAcluster** | Gender, Age 관련 분석에서 특화 | 전반적 성능 중간 |
| **IntNMF** | Age 분석에서 강점 | 다른 시나리오에서 약세 |
| **iClusterPlus** | 다중 서브타입 구별에서 일관되게 **저성능** | 전체적으로 하위권 |
| **MOFA** | 특정 서브타입 조합에서 강점 | 일관된 상위 성능은 아님 |
| **Spectrum** | Subtype omics 분석에서 준수 | 전반적으로 중간 수준 |
| **COCA** | Stage 분석에서 간헐적 강점 | 전반적으로 중간 수준 |

### 5.3 MOSD 가이드라인 요약

본 연구에서 도출된 근거 기반(Evidence-based) 권고사항을 종합하면 다음과 같다:

**계산적 설계 권고 (Computational Design Recommendations):**

1. 클래스당 약 **26개 이상**의 샘플을 확보하여 결과의 안정성(일관성) 보장
2. 전체 특성의 **10% 미만**을 선택하여 클러스터링 성능을 극대화 (최대 34% 향상)
3. 샘플 불균형 비율을 **3:1 이하**로 유지
4. 노이즈 수준을 **30% 이하**로 관리
5. 전처리 전략은 암종 및 분석 목적에 따라 유연하게 선택하되, 전처리보다 Feature selection과 Sample size에 더 큰 우선순위 부여

**생물학적 설계 권고 (Biological Design Recommendations):**

6. 분자적으로 뚜렷이 구별되는(Molecularly distinct) 서브타입을 우선 분석 대상으로 선택
7. 오믹스 조합은 **GE-ME**를 기본으로, 분석 목적에 따라 최적 조합 탐색
8. 분석 방법은 연구 목적에 맞게 선택: 구조적 분석에는 **SNF**, 임상 특성 분석에는 **NEMO**, 노이즈가 우려되면 **PP**

---

## 6. 연구 기여 및 의의

### 6.1 학술적 기여

| 기여 영역 | 구체적 내용 |
|---------|---------|
| **프레임워크 제안** | 다중오믹스 통합 분석의 Study Design을 체계화한 최초의 통합 프레임워크(MOSD) 제시 |
| **벤치마크 방법론** | 단일 요인 분리 원칙에 기반한 7가지 벤치마크를 설계하여, 각 요인의 고유 영향을 정밀하게 측정하는 방법론 수립 |
| **지식 통합** | 분산되어 있던 선행연구(Mirza, Chauvel, Rappoport, Pierre-Jean, Tini, Duan)의 개별적 발견을 하나의 일관된 체계로 통합 |
| **평가 지표 도입** | ARI, NMI, F-measure를 통합한 cluster-score를 도입하여 다관점 성능 평가 체계 확립 |
| **방법론적 통찰** | 10개 MOI 방법의 시나리오별 강약점 프로파일을 체계적으로 제시하여, 연구 목적에 맞는 방법 선택을 위한 근거 제공 |

### 6.2 실용적 가치

| 실용적 가치 | 구체적 활용 |
|----------|---------|
| **연구 설계 체크리스트** | 다중오믹스 연구를 시작하는 연구자가 9가지 요인을 체크리스트처럼 활용하여 실험 설계 최적화 |
| **정량적 기준** | "클래스당 26개", "특성 10% 미만", "불균형 3:1 이하", "노이즈 30% 이하" 등 구체적 숫자 기반 의사결정 지원 |
| **방법 선택 가이드** | 연구 목적(서브타입 분류, 임상 특성 분석, 노이즈 환경 등)에 따른 최적 MOI 방법 추천 |
| **재현성 향상** | GitHub 코드 저장소(MOPARAM)를 통한 전처리 파이프라인 및 벤치마크 코드 공개로 재현 가능한 연구 지원 |
| **이론-실무 간극 해소** | MOI의 이론적 도전과제를 실증적 가이드라인으로 전환하여 이론과 실무 간의 간극 해소 |

---

## 7. 한계점 및 향후 연구

### 7.1 인정된 한계

| 한계 | 상세 설명 | 영향 범위 |
|------|---------|---------|
| **TCGA 특화** | 가이드라인이 TCGA 데이터에서 도출되었으므로 다른 데이터셋(ICGC, CCLE, CPTAC)에 직접 일반화 시 주의 필요 | 일반화 가능성 |
| **Bulk 수준 한정** | 단일세포(Single-cell) 다중오믹스, 공간 전사체학(Spatial transcriptomics) 등 신규 데이터 유형 미포함 | 데이터 유형 범위 |
| **Feature selection 방법 제한** | Chi-square와 ANOVA만 사용. Lasso, Mutual information, 딥러닝 기반 등 다른 방법과의 비교 미수행 | 방법론적 다양성 |
| **전처리 차이의 미미함** | 전처리 간 차이가 대부분 0.1 미만으로, 전처리의 진정한 영향을 과소평가했을 가능성 | 결과 해석 |
| **시간적 변이 미반영** | 시간적 샘플링(Temporal sampling)이나 종단적 데이터(Longitudinal data) 미포함 | 연구 범위 |
| **해상도 한계** | 단일세포 해상도(Single-cell resolution)에서의 MOSD 적용 미검증 | 기술 발전 대응 |

### 7.2 향후 확장 방향

논문에서 제시하는 향후 연구 방향:

1. **신규 데이터 양식(Modality) 확장**: 시간적 샘플링(Temporal sampling), 단일세포 해상도(Single-cell resolution) 등 새로운 데이터 양식 및 추가 요인(Dropout rate, Sparsity, Batch effect 등)을 MOSD에 통합
2. **다양한 데이터셋 검증**: ICGC, CCLE, CPTAC 등 다른 대규모 다중오믹스 아카이브에서 가이드라인의 외적 타당성(External validity) 검증
3. **가이드라인 지속적 개선**: 복잡한 분자 데이터를 의미 있는 임상적, 생물학적 통찰로 효율적으로 변환하기 위한 가이드라인의 지속적 정제(Refinement)

---

## 8. 핵심 수식 및 개념

### 8.1 클러스터링 평가 지표 수식

#### Rand Index (RI)

$$RI = \frac{TP + TN}{TP + FP + TN + FN}$$

**해석**: 전체 샘플 쌍 중 올바르게 분류된 쌍의 비율. 우연에 의한 일치를 보정하지 않는 원시 지표.

#### Adjusted Rand Index (ARI)

$$ARI = \frac{RI - Expected(RI)}{Max(RI) - Expected(RI)}$$

**해석**: RI에서 우연에 의해 기대되는 일치(Expected RI)를 보정. 범위는 [-1, 1]이며, 0은 랜덤 수준, 1은 완벽 일치를 의미. 본 벤치마크에서는 모든 ARI 값이 비음수(non-negative)였음.

#### Mutual Information (MI)

$$MI = \sum_{i \in T} \sum_{j \in C} P(i,j) \cdot \log\left(\frac{P(i,j)}{P(i) \cdot P'(j)}\right)$$

여기서:
- $P(i) = |T_i| / N$: 진짜 클래스 i에 속할 확률
- $P'(j) = |C_j| / N$: 클러스터 j에 할당될 확률
- $P(i,j) = |T \cap C| / N$: 클래스 i이면서 클러스터 j에 속할 결합 확률

#### Normalized Mutual Information (NMI)

$$NMI = \frac{MI(T,C)}{mean(H(T), H(C))}$$

여기서:
- $H(T) = -\sum_{i \in T} P(i) \log(P(i))$: 진짜 레이블의 엔트로피
- $H(C) = -\sum_{j \in C} P'(j) \log(P'(j))$: 클러스터링 결과의 엔트로피

**해석**: MI를 두 분포의 평균 엔트로피로 정규화하여 [0, 1] 범위로 표준화. 서로 다른 클러스터링 시나리오 간 비교 가능.

#### F-measure (Pair-based)

$$A = |Pairs(U) \cap Pairs(V)|$$
$$B = |Pairs(U) - Pairs(V)|$$
$$C = |Pairs(V) - Pairs(U)|$$
$$F\text{-}measure = \frac{2A}{2A + B + C}$$

**해석**: 예측 클러스터(U)와 진짜 클러스터(V)의 쌍별 일치를 집합 연산으로 평가. 정밀도(Precision)와 재현율(Recall)의 조화 평균에 해당.

#### Cluster-score

$$cluster\text{-}score = \frac{ARI + NMI + F\text{-}measure}{3}$$

**해석**: 세 가지 서로 다른 관점의 평가 지표를 동등한 가중치로 통합한 종합 성능 지표.

### 8.2 통계 검정 방법

#### Wilcoxon Rank-Sum Test

클래스 균형(Balance) 벤치마크에서 균형 그룹(< 3:1)과 불균형 그룹(> 3:1) 간 cluster-score 분포의 유의미한 차이를 검정하는 데 사용. Adjusted p-value < 0.0001으로 통계적 유의성 확인.

#### Chi-square Test (Feature Selection)

GE, MI, ME 오믹스에서 특성 선택에 사용. 각 특성과 그룹 레이블(서브타입) 간의 독립성을 검정하여 p-value로 순위화한 후, 상위 특성을 선택.

#### ANOVA (Feature Selection)

CNV 오믹스에서 특성 선택에 사용. 음수값을 포함하는 CNV 데이터의 특성상 Chi-square 대신 ANOVA를 적용하여 그룹 간 평균 차이를 검정.

#### 반복 샘플링 (10-fold Random Sample Selection)

각 벤치마크를 10회 반복 수행하여 결과의 통계적 견고성(Statistical robustness)을 확보. 매 반복마다 무작위 샘플 선택을 달리하여 특정 샘플 조합에 대한 편향 방지.

---

## 9. 예상 질문 및 답변

### 기술적 질문 (Technical Questions)

---

**Q1. cluster-score가 단순 산술평균인 이유는 무엇이며, 가중 평균이나 다른 통합 방식이 더 적절하지 않은가?**

**A1.** cluster-score를 단순 산술평균으로 설계한 이유는 세 가지이다. 첫째, ARI(우연 보정 관점), NMI(정보이론 관점), F-measure(집합 연산 관점)는 각각 서로 다른 수학적 원리에 기반하므로, 어떤 하나의 지표에 편향되지 않도록 동등한 가중치를 부여하는 것이 공정하다. 둘째, 본 벤치마크에서 모든 ARI 값이 비음수(non-negative)였으므로, 세 지표 모두 [0, 1] 범위에서 동작하여 별도 정규화 없이 평균이 가능했다. 셋째, 가중 평균을 사용하려면 각 지표의 상대적 중요도에 대한 사전 가정(prior assumption)이 필요한데, 이는 벤치마크의 객관성을 해칠 수 있다. 다만 논문에서도 향후 ARI 음수값이 발생하는 연구에서는 0-1 정규화 후 평균하는 방식을 고려해야 한다고 명시하였다.

---

**Q2. Feature selection에서 Chi-square와 ANOVA만 사용한 것이 방법론적으로 충분한가?**

**A2.** 이 선택은 의도적인 설계 결정이다. 본 연구의 목적은 특정 Feature selection 방법의 우수성을 입증하는 것이 아니라, Feature selection이라는 **요인 자체**의 영향을 평가하는 것이다. Chi-square(GE, MI, ME)와 ANOVA(CNV)를 선택한 이유는 다음과 같다: (1) 그룹 레이블(서브타입) 기반 방법으로, 특정 클러스터링 알고리즘에 의존하지 않는 알고리즘 비의존적(Algorithm-agnostic) 접근; (2) 분산 기반(Variance-based) 방법이나 모델 특정적(Model-specific) 방법은 특정 MOI 방법에 편향된 결과를 생성할 수 있음; (3) CNV의 경우 음수값 포함으로 Chi-square 부적합하여 ANOVA를 대안으로 사용. 한계로서 Lasso, Mutual information, 딥러닝 기반 방법 등과의 비교를 수행하지 않은 점은 인정하며, 이는 향후 연구에서 확장 가능하다.

---

**Q3. 전처리 간 성능 차이가 0.1 미만인데, 이것이 "전처리가 중요하지 않다"는 결론으로 이어질 수 있는가?**

**A3.** 전처리 간 차이가 작다는 것 자체가 중요한 발견이다. 이는 연구자에게 "전처리 선택에 과도한 시간을 투자하기보다 Feature selection이나 Sample size 같은 더 영향력 있는 요인에 집중하라"는 실용적 메시지를 전달한다. 그러나 "전처리가 중요하지 않다"고 단정하는 것은 과도한 해석이다. 이유는 다음과 같다: (1) 성별(Gender) 분석에서 NORM은 +0.20~+0.27의 유의미한 향상을 보였으며, 이는 특정 분석 맥락에서 전처리의 중요성을 시사; (2) 암종별로 선호 전처리가 상이하여 (LUAD-GL, STAD-NORM), 일률적 적용은 부적절; (3) RAW가 일부 노이즈 테스트에서 오히려 우수한 경우도 있어, 정규화가 관련 생물학적 신호를 약화시킬 가능성도 존재. 따라서 결론은 "전처리는 맥락 의존적(Context-dependent)이며, 절대적 중요도는 Feature selection보다 낮다"이다.

---

**Q4. 벤치마크에서 요인을 분리하여 평가하는 방식이 요인 간 상호작용(Interaction effect)을 간과할 수 있지 않은가?**

**A4.** 이는 본 연구의 설계적 Trade-off에 해당한다. 단일 요인 분리(Single-factor isolation) 설계를 채택한 이유는 다음과 같다: (1) 9가지 요인의 모든 가능한 조합을 테스트하면 조합 폭발(Combinatorial explosion)이 발생하여 계산적으로 비현실적; (2) 단일 요인의 고유 영향을 먼저 파악하는 것이 다요인 상호작용 연구의 필수 전제 조건; (3) 다른 변수를 기본값(Default)으로 고정함으로써 각 요인의 독립적 효과를 깨끗하게 측정 가능. 한계로서 요인 간 상호작용(예: Feature selection 비율과 Noise 수준의 결합 효과)을 직접 평가하지 않은 점은 인정한다. 그러나 MOSD의 가치는 개별 요인의 효과를 먼저 정립하고, 이를 기반으로 향후 상호작용 연구로 확장할 수 있는 토대를 마련한 데 있다.

---

**Q5. NEMO가 임상 특성 분석에서 강한 이유와 SNF가 구조적 테스트에서 강한 이유를 알고리즘적으로 설명할 수 있는가?**

**A5.** SNF는 각 오믹스 유형에서 유사도 네트워크(Similarity network)를 구축하고 이를 반복적으로 융합하는 방식으로, 샘플 간 전반적 유사성 패턴을 잘 포착한다. 이 접근법은 샘플 크기 변화나 특성 비율 변화와 같은 구조적 변동에 대해 네트워크의 전역적(Global) 구조가 견고하게 유지되므로 구조적 테스트에서 강점을 보인다. 또한 이산형과 연속형 특성 모두를 처리할 수 있고 소규모 샘플에도 내성이 있다. 반면 NEMO는 오믹스별 쌍별 거리를 계산한 후 k-NN 그래프를 구축하고 국소적(Local) 이웃 패턴에 기반한 그래프 클러스터링을 수행한다. 이 지역적 접근법은 특정 임상 특성(Stage, Age)과 연관된 미세한 분자적 차이를 더 민감하게 포착할 수 있으며, 부분 데이터(Partial datasets)에서도 결측 보정 없이 작동하는 유연성이 임상 데이터의 불완전성에 잘 대응한다.

---

### 비판적 질문 (Critical Questions)

---

**Q6. TCGA 데이터에서 도출한 가이드라인을 다른 데이터셋이나 질환에 일반화할 수 있는가?**

**A6.** 직접적 일반화에는 주의가 필요하다. 그러나 다음과 같은 근거로 합리적 수준의 일반화 가능성이 있다: (1) TCGA는 가장 포괄적이고 잘 큐레이션된 다중오믹스 아카이브로, 10개 암종, 3,988명 환자, 4종 오믹스를 포함하여 상당한 대표성을 가짐; (2) 9가지 요인(샘플 크기, 노이즈 등)은 데이터셋 특이적이 아닌 범용적 통계/계산적 원리에 기반하므로, 요인의 방향성(Direction)은 다른 데이터에서도 유사할 것으로 기대; (3) 구체적 수치(26개, 10%, 3:1 등)는 TCGA에 최적화된 값이므로 다른 맥락에서 재검증 필요. MOSD의 핵심 가치는 구체적 숫자보다 **"이러한 요인들을 체계적으로 고려해야 한다"는 프레임워크 자체**에 있으며, 이 프레임워크는 데이터셋에 무관하게 적용 가능하다.

---

**Q7. 10개 MOI 방법의 선정 기준이 충분히 포괄적인가? 딥러닝 기반 방법이 빠져 있는 것은 문제가 아닌가?**

**A7.** 10개 방법은 구현 용이성, 학술적 보급도, R/Python 가용성이라는 3가지 기준으로 선정되었다. 이 기준은 실용적 관점에서 합리적이며, 선정된 방법들은 클러스터링, 행렬 분해(Matrix factorization), 네트워크 통합(Network integration) 등 주요 계산 접근법을 포괄한다. 딥러닝 기반 방법(예: Autoencoder, GAN 기반 통합)이 제외된 것은 다음과 같은 이유로 정당화된다: (1) 딥러닝 방법은 하이퍼파라미터에 민감하여 "기본 파라미터(Default parameters)로의 실행"이라는 공정 비교 기준에 부합하지 않음; (2) 학술적으로 가장 널리 사용되는 전통적 방법들을 우선 평가하는 것이 벤치마크의 기본 원칙; (3) 향후 딥러닝 방법이 성숙해지면 MOSD 프레임워크에 추가 가능. 실제로 Duan et al. [31]의 Subtype-GAN 같은 딥러닝 방법이 등장하고 있으나, 아직 범용적 벤치마크에 포함할 수준의 표준화가 이루어지지 않았다.

---

**Q8. 결측 데이터를 완전 제거(Complete case deletion)한 보수적 접근이 결과를 편향시킬 수 있는가?**

**A8.** 결측 데이터의 완전 제거는 확실히 제한점이다. 이 접근법은 다음과 같은 잠재적 편향을 유발할 수 있다: (1) 특정 오믹스 계층에서 결측이 많은 샘플이 체계적으로 배제되어 남은 샘플이 전체 모집단을 대표하지 못할 수 있음; (2) 10명 미만 그룹의 제외로 희귀 서브타입 정보 손실. 그러나 이 결정의 근거도 분명하다: (1) 보간(Imputation)은 그 자체로 편향을 도입하며, 특히 MOI에서 오믹스 계층 간 상관 구조가 복잡하여 보간의 적절성 검증이 어려움; (2) 결측 처리 방법 자체가 추가 요인이 되어 벤치마크의 해석을 복잡하게 만듦; (3) 완전 제거 후에도 3,988명이라는 충분한 샘플 수를 확보. 논문에서도 이를 "데이터 희소성(Sparsity)에서 비롯되는 잠재적 편향을 최소화하기 위한 보수적 접근"으로 설명하고 있다.

---

**Q9. 본 연구가 "리뷰(Review)"로 분류되면서 동시에 벤치마크를 수행하는 것이 적절한가? 원저(Original research)와 리뷰의 경계가 모호하지 않은가?**

**A9.** 이 논문은 전통적인 서술적 리뷰(Narrative review)나 순수 원저 연구의 범주에 정확히 들어맞지 않는, **체계적 벤치마크 리뷰(Systematic benchmark review)**의 성격을 가진다. 제목에 "A review"를 포함한 이유는 선행연구(6개 이상)를 체계적으로 종합하고 비교한 리뷰적 요소가 핵심 기여의 일부이기 때문이다. 동시에, 기존 연구를 단순히 정리하는 것을 넘어 **자체 벤치마크 설계 및 실행**을 통해 새로운 가이드라인을 도출했다는 점에서 원저 연구의 요소도 포함한다. BMC Genomics에서 "RESEARCH" 논문으로 분류된 것은 이러한 하이브리드적 성격을 인정한 것이다. 실제로 바이오인포매틱스 분야에서는 이러한 "벤치마크+리뷰" 형식의 논문이 높은 인용 영향력을 가지는 경향이 있다.

---

**Q10. MOSD 프레임워크가 향후 단일세포(Single-cell) 다중오믹스로 확장될 때, 현재 가이드라인이 얼마나 유효할 것으로 예상되는가?**

**A10.** 현재 가이드라인의 직접 적용은 어렵지만, 프레임워크의 구조는 확장 가능하다. 구체적으로 분석하면: (1) **유효할 가능성이 있는 요인**: Feature selection의 중요성, Class balance의 영향, 방법 선택의 맥락 의존성 등 원리적 수준의 가이드라인은 단일세포에도 적용 가능; (2) **수정이 필요한 요인**: Sample size 기준(26개)은 세포 수 기준으로 재정립 필요 (단일세포에서는 수천~수만 세포가 일반적), Noise characterization은 Dropout rate, Sparsity, 기술적 노이즈(Technical noise) 등 단일세포 특유의 노이즈 유형 반영 필요; (3) **추가되어야 할 요인**: Batch effect, Cell type annotation quality, Doublet rate 등 단일세포 특유의 요인; (4) **데이터 규모 차이**: Bulk (수백~수천 샘플) vs. Single-cell (수만~수십만 세포)로 확장성 문제가 더욱 심각. 따라서 MOSD의 "9가지 요인을 체계적으로 평가한다"는 프레임워크적 접근은 유효하나, 구체적 요인과 수치는 단일세포 맥락에 맞게 재설계되어야 한다.

---

> **문서 작성일**: 2026-03-04
> **원 논문**: Han et al., BMC Genomics (2025) 26:769
> **참고 자료**: 논문 PDF 전문 + 연구요약 및 보충자료 (박사 졸업구술시험용)
