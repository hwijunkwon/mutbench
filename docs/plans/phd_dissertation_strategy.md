# 박사 졸업논문 전략: MOSD + MutClust 통합

> **핵심 서사**: "다층적 게놈 데이터를 위한 체계적 벤치마킹과 적응형 클러스터링"

---

## 1. 왜 두 논문이 자연스럽게 연결되는가?

### 1.1 공유 철학: "클러스터링을 통한 생물학적 발견"

| 관점 | MOSD (Paper 1) | MutClust (Paper 2) |
|------|----------------|---------------------|
| **핵심 방법** | 10가지 클러스터링 방법 비교 평가 | 적응형 밀도 기반 클러스터링 개발 |
| **데이터 유형** | 다중오믹스 (GE, ME, MI, CNV) | 바이러스 게놈 서열 + 다중오믹스 |
| **목표** | 암 서브타입 분류 | 변이 핫스팟 탐지 + 중증도 연관 |
| **평가 체계** | cluster-score = (ARI+NMI+F)/3 | Bootstrap testing (체계적 평가 부재) |
| **연구 설계** | 9가지 요인의 체계적 벤치마크 | 단일 파라미터 설정, 벤치마크 없음 |
| **임상 연결** | Subtype, Gender, Stage, Age | Severity (moderate vs severe) |
| **게놈 범위** | 10개 TCGA 암종 (범암 일반화) | SARS-CoV-2 + 인플루엔자 (범병원체 가능성) |

### 1.2 핵심 연결 다리 5가지

**Bridge 1: 벤치마킹 방법론의 전이**
- MOSD는 MOI 분야에 최초의 통합 벤치마크를 만듦
- 변이 핫스팟 탐지 분야에도 이러한 벤치마크가 **전혀 존재하지 않음**
- MOSD의 벤치마킹 철학(단일 요인 분리, 변수 통제, 다중 평가지표)을 MutClust 도메인에 적용

**Bridge 2: 연구 설계 원칙의 적용**
- MOSD 발견: 샘플 수 ≥26/class, 특성선택 1-10%, 노이즈 ≤30%, 클래스 균형 ≤3:1
- MutClust 현황: severe=42 vs moderate=345 (8.2:1 비율!), 연구 설계 최적화 없음
- **MOSD의 가이드라인을 MutClust의 downstream 분석에 직접 적용 가능**

**Bridge 3: 평가 지표 체계의 통합**
- MOSD의 cluster-score는 3가지 관점(우연보정, 정보이론, 집합기반)을 통합
- MutClust는 bootstrap p-value만 사용 → 순환적 검정, 과도한 보수성 문제
- **"hotspot-score"라는 새로운 다관점 평가 지표 설계 가능**

**Bridge 4: 다중 요인 민감도 분석**
- MOSD는 7가지 벤치마크로 각 요인의 고유 영향을 분리 측정
- MutClust는 파라미터(gamma, d, CCM 임계값) 민감도 분석 부재
- **MutClust에도 MOSD 스타일의 체계적 요인 분석 적용**

**Bridge 5: 범용화(일반화) 패턴**
- MOSD: 10개 암종으로 범암 일반화 달성
- MutClust: SARS-CoV-2 + 인플루엔자 검증했으나 파라미터 재조정 없이
- **MOSD의 범암 접근을 MutClust의 범병원체 확장에 적용**

---

## 2. 추천 졸업논문 구조

### 논문 제목 (안)

**한글**: "다층적 게놈 데이터 분석을 위한 체계적 벤치마킹과 적응형 클러스터링 프레임워크"

**영문**: "Systematic Benchmarking and Adaptive Clustering Frameworks for Multi-Scale Genomic Data Analysis"

### 구조

```
Chapter 1: Introduction (서론)
├── 1.1 다중오믹스 통합의 도전과제
├── 1.2 바이러스 변이 핫스팟 탐지의 필요성
├── 1.3 클러스터링: 두 문제를 관통하는 핵심 방법론
└── 1.4 연구 목적 및 구성

Chapter 2: Literature Review (문헌 고찰)
├── 2.1 다중오믹스 통합 방법론 동향
├── 2.2 변이 핫스팟 탐지 방법론 동향
├── 2.3 벤치마킹 프레임워크의 중요성
└── 2.4 연구 공백 (Research Gap) 정의

Chapter 3: [Paper 1] MOSD Framework (출판 완료)
├── 3.1 BMC Genomics (2025) 26:769
├── 3.2 9가지 요인, 7가지 벤치마크, 10가지 방법
├── 3.3 정량적 연구 설계 가이드라인
└── 3.4 요약 및 시사점

Chapter 4: [Paper 2] MutClust Algorithm (출판 완료)
├── 4.1 BioData Mining (2025) 18:61
├── 4.2 H-score, 적응형 DBSCAN, CCM
├── 4.3 477개 핫스팟, NK세포 가설
└── 4.4 요약 및 한계점

Chapter 5: [Paper 3 - NEW] MutBench: 통합 프레임워크
├── 5.1 시뮬레이션 기반 핫스팟 벤치마크
├── 5.2 MutClust v2 알고리즘 개선
├── 5.3 MOSD-guided 연구 설계 적용
├── 5.4 범병원체 검증
└── 5.5 결과 및 가이드라인

Chapter 6: Discussion & Conclusion
├── 6.1 세 논문의 통합적 기여
├── 6.2 한계점
├── 6.3 향후 연구
└── 6.4 결론
```

---

## 3. 새 논문 (Paper 3) 상세 설계

### 제목 (안)

**"MutBench: Systematic Benchmarking and Study Design-Guided Improvement of Viral Mutation Hotspot Detection"**

또는

**"From Study Design to Discovery: Benchmarking-Driven Improvement of Density-Based Mutation Hotspot Detection Across Diverse Pathogen Genomes"**

### 3.1 Part A: 벤치마킹 프레임워크 (MOSD 방법론 전이)

MOSD에서 암 서브타입 클러스터링을 체계적으로 평가한 것처럼, 변이 핫스팟 탐지 방법들을 최초로 체계적 비교한다.

**비교 대상 방법 (6가지):**

| 방법 | 유형 | 설명 |
|------|------|------|
| MutClust (원본) | 적응형 밀도 기반 | H-score + adaptive DBSCAN |
| MutClust v2 | 개선된 적응형 | HDBSCAN + 자동 파라미터 |
| Shannon entropy | 엔트로피 기반 | 위치별 뉴클레오타이드 다양성 |
| 빈도 기반 | 통계 기반 | 변이 빈도 상위 N% |
| 슬라이딩 윈도우 | 고정 윈도우 | 고정 크기 윈도우의 변이 밀도 |
| HDBSCAN (직접) | 범용 밀도 기반 | 2D 특징(빈도, 엔트로피)에 HDBSCAN |

**벤치마크 요인 (MOSD의 9요인에서 영감):**

| MOSD 요인 | MutBench 대응 요인 | 테스트 설계 |
|-----------|-------------------|-----------|
| Sample size | **서열 수** | 100, 500, 1K, 5K, 10K, 50K, 200K 서열 |
| Feature selection | **게놈 크기** | 2kb (인플루엔자 세그먼트) ~ 200kb (Mpox) |
| Preprocessing | **정렬 품질** | MAFFT vs MUSCLE vs Minimap2 |
| Noise | **서열 오류율** | 0%, 1%, 5%, 10% 인위적 오류 주입 |
| Class balance | **계통 균형** | 균등 vs 실제 불균형 (Alpha 80% 등) |
| Number of classes | **계통 수** | 1, 5, 10, 22개 계통 혼합 |
| Cancer subtype | **병원체 유형** | 비분절 RNA, 분절 RNA, DNA |
| Omics combination | *(해당 없음)* | - |
| Clinical feature | **알려진 기능 변이 포착율** | 10개 알려진 기능 변이의 recall |

**평가 지표 (cluster-score에서 영감받은 hotspot-score):**

```
hotspot-score = (Recall_known + Precision_simulated + Stability_bootstrap) / 3

- Recall_known: 알려진 기능적 변이(D614G, E484K 등)를 포함하는 핫스팟 비율
- Precision_simulated: 시뮬레이션 ground-truth에서의 정밀도
- Stability_bootstrap: 서열 서브샘플링 시 핫스팟 재현율
```

**시뮬레이션 기반 Ground-Truth:**
- pyvolve/INDELible로 계통수 기반 서열 시뮬레이션
- 특정 위치에 인위적 양의 선택 주입 → "알려진" 핫스팟 생성
- GENOMICON-Seq (2025) 참고하여 현실적 변이 패턴 모사

### 3.2 Part B: MutClust v2 핵심 개선 (알고리즘)

MOSD의 발견("method choice matters", "study design affects outcome")에 기반하여 MutClust를 개선한다.

**개선 1: HDBSCAN 기반 자동 파라미터**
- 문제: gamma=10, d=3, CCM 임계값이 SARS-CoV-2에 하드코딩
- 해결: HDBSCAN의 밀도 기반 자동 클러스터 선택 도입
- MOSD에서 "전처리보다 방법 선택이 중요"라는 발견 → 방법 자체의 자동 적응이 핵심

**개선 2: 계통발생 보정 (Phylogenetic correction)**
- 문제: D614G 같은 설립자 효과 vs 반복적 양의 선택 구분 불가
- 해결: TreeTime 활용, 독립적 발생 횟수 기반 P_i 보정
- MOSD에서 "샘플링 편향이 결과에 영향"이라는 발견의 변이 분석 버전

**개선 3: dN/dS 통합**
- 문제: 동의/비동의 변이 미구분
- 해결: 코돈 수준 H-score + dN/dS 가중치
- 생물학적 해석력 향상

**개선 4: _expand_cluster 버그 수정 + 벡터화**
- distance > deps_ccm 시 감쇠 역전 버그 수정
- numpy 벡터화로 100배+ 속도 향상

### 3.3 Part C: MOSD-Guided 연구 설계 적용

MOSD의 구체적 가이드라인을 MutClust의 downstream 분석에 적용하여 결과 개선을 입증한다.

**적용 1: 클래스 균형 개선**
- MOSD 발견: 불균형 3:1 초과 시 성능 저하
- MutClust 현황: severe:moderate = 42:345 = **8.2:1** (MOSD 기준 위반)
- 조치: SMOTE/downsampling으로 균형 조정 후 재분석, 개선 효과 정량화

**적용 2: 특성 선택 최적화**
- MOSD 발견: 전체 특성의 1-10% 선택 시 최적
- MutClust 현황: 477개 핫스팟 전체를 downstream에 사용
- 조치: 477개 중 상위 10-50개 핫스팟만 선택 vs 전체 사용 비교

**적용 3: 다중 평가지표 도입**
- MOSD 발견: 단일 지표보다 cluster-score가 편향 방지에 효과적
- MutClust 현황: bootstrap p-value 단일 지표
- 조치: hotspot-score 도입으로 다관점 평가

### 3.4 Part D: 범병원체 검증

MOSD가 10개 암종으로 일반화한 것처럼, 4개 병원체로 범용성 검증한다.

| 병원체 | 게놈 유형 | 크기 | 데이터 출처 |
|--------|----------|------|-----------|
| SARS-CoV-2 | 비분절 RNA | ~30kb | NCBI GenBank |
| Influenza A (H1N1/H3N2) | 분절 RNA (8세그먼트) | ~13.5kb | NCBI Influenza DB |
| H5N1 | 분절 RNA | ~13.5kb | NCBI/USDA |
| Mpox | DNA (이중가닥) | ~197kb | NCBI/BV-BRC |

**게놈 유형별 핵심 차이 처리:**
- 분절 게놈: reassortment 처리 (세그먼트별 독립 분석 + 교차 세그먼트 패턴)
- DNA 바이러스: APOBEC3 편집 시그니처 보정
- 게놈 크기 차이: 자동 파라미터로 해결 (Part B의 HDBSCAN)

---

## 4. 왜 이 조합이 최적인가?

### 4.1 학술적 강점

| 기준 | 평가 |
|------|------|
| **두 논문 필수성** | Bridge paper가 MOSD의 벤치마킹 방법론 + MutClust의 알고리즘을 모두 필요로 함 |
| **새로운 기여** | 변이 핫스팟 탐지의 최초 벤치마크 프레임워크 (MutBench) |
| **기존 논문 가치 증대** | MOSD의 범용성 입증 (암 → 바이러스) + MutClust의 한계 극복 |
| **통합 서사 강도** | "벤치마킹 → 알고리즘 → 통합 프레임워크" 자연스러운 진행 |
| **심사위원 설득력** | 방법론적 기여 + 도메인 특화 기여 + 범용화 기여의 3중 구조 |

### 4.2 실현가능성

| 기준 | 평가 |
|------|------|
| **데이터 접근** | 모든 데이터 무료 (NCBI GenBank, TCGA) |
| **컴퓨팅 자원** | CPU만으로 충분 (GPU 불필요) |
| **기간** | 12-15개월 (시뮬레이션 3개월 + 알고리즘 4개월 + 범병원체 3개월 + 논문 작성 3개월) |
| **기존 코드 활용** | 이미 구현된 12개 도구를 기반으로 확장 |
| **경쟁 위험** | "범용 핫스팟 벤치마크"라는 니치에 아무도 없음 |

### 4.3 출판 전략

| 논문 | 대상 저널 | 임팩트 | 타이밍 |
|------|----------|--------|--------|
| Paper 1 (MOSD) | BMC Genomics | IF ~4.5 | ✅ 출판 완료 |
| Paper 2 (MutClust) | BioData Mining | IF ~4.5 | ✅ 출판 완료 |
| Paper 3 (MutBench) | **Bioinformatics** 또는 **Genome Biology** | IF 5.8~12.3 | 투고 목표 |

Paper 3의 저널 선택:
- **Bioinformatics** (IF 5.8): 벤치마크 + 알고리즘 논문에 최적, 리뷰 기간 짧음
- **Genome Biology** (IF 12.3): 범병원체 일반화의 임팩트가 충분하면 도전 가능
- **Nucleic Acids Research** (IF 14.9): 웹 서버/데이터베이스 함께 공개 시
- **GigaScience** (IF 7.7): 데이터 중심 + 벤치마크에 우호적

---

## 5. 졸업논문 통합 서사

> **"게놈 데이터 분석에서 클러스터링은 핵심 방법론이지만, 그 성능은 연구 설계와 알고리즘 선택에 크게 좌우된다. 본 연구에서는 (1) 다중오믹스 통합을 위한 최초의 체계적 연구 설계 프레임워크(MOSD)를 구축하여 9가지 요인의 영향을 정량화하고 구체적 가이드라인을 제시하였으며, (2) 바이러스 게놈의 변이 핫스팟 탐지를 위한 적응형 밀도 기반 클러스터링 알고리즘(MutClust)을 개발하여 SARS-CoV-2에서 477개 핫스팟과 NK세포 기능 이상 가설을 도출하였고, (3) 두 접근법을 통합하여 변이 핫스팟 탐지의 최초 벤치마크 프레임워크(MutBench)를 구축하고, 연구 설계 원칙에 기반한 알고리즘 개선과 범병원체 일반화를 달성하였다. 이를 통해 체계적 벤치마킹과 적응형 클러스터링이 게놈 데이터의 다양한 스케일에서 생물학적 발견을 촉진할 수 있음을 입증하였다."**

---

## 6. 위험 요소 및 대응

| 위험 | 확률 | 대응 |
|------|------|------|
| 누군가 핫스팟 벤치마크 선발표 | 낮음 | 현재 이 니치에 아무도 없음. 빠르게 시뮬레이션 데이터 공개로 선점 |
| MutClust 원저자가 v2 발표 | 중간 | 벤치마크 + 연구설계 적용은 원저자와 다른 방향. 공동 연구 제안도 가능 |
| 범병원체 중 하나의 데이터 부족 | 낮음 | H5N1, Mpox 모두 NCBI에 적극 공개 중 |
| "단순 확장" 평가 위험 | 중간 | MOSD→MutClust 방법론 전이의 비자명성 강조, 게놈 유형별 근본 차이 부각 |
| Paper 3 높은 저널 reject | 중간 | Bioinformatics를 1차 타겟으로 안전하게, GigaScience를 백업 |

---

## 7. 구체적 실행 로드맵

### Phase 1: 시뮬레이션 벤치마크 구축 (3개월)

```
Month 1: 시뮬레이션 엔진 개발
- pyvolve 기반 바이러스 서열 시뮬레이터
- 인위적 핫스팟(양의 선택) 주입 모듈
- 다양한 게놈 크기/변이율 파라미터 세트

Month 2: 벤치마크 실행
- 6가지 방법 × 7가지 요인 × 10회 반복
- hotspot-score 계산 파이프라인
- MOSD 스타일 시각화 (violin plot, heatmap)

Month 3: 벤치마크 논문 초안
- 요인별 주요 발견 정리
- 가이드라인 도출 (MOSD 가이드라인과 대비)
```

### Phase 2: MutClust v2 개발 (4개월)

```
Month 4-5: 핵심 알고리즘 개선
- HDBSCAN 통합 + 자동 파라미터
- 계통발생 보정 (TreeTime)
- dN/dS 가중치
- expand_cluster 버그 수정 + 벡터화

Month 6-7: MOSD-guided 분석 개선
- 클래스 균형 조정 실험
- 특성 선택 최적화 실험
- hotspot-score 기반 평가
- KDCA 코호트 재분석으로 개선 효과 입증
```

### Phase 3: 범병원체 검증 (3개월)

```
Month 8-9: 데이터 수집 및 적용
- SARS-CoV-2 (기존 + 최신 변이)
- Influenza A (H1N1, H3N2, H5N1)
- Mpox (APOBEC3 보정)
- 각 병원체별 알려진 기능 변이로 검증

Month 10: 비교 분석 및 일반화
- 게놈 유형별 최적 설정 도출
- 범병원체 패턴 비교
- 자동 파라미터의 범용성 입증
```

### Phase 4: 논문 작성 및 졸업논문 통합 (3-5개월)

```
Month 11-12: Paper 3 작성 및 투고
Month 13-15: 졸업논문 통합 작성
```

---

## 8. 대안 경로: TCGA 암 데이터에 MutClust 적용 (Option B)

> **Agent 2의 핵심 발견**: 바이러스 대신 TCGA 암 데이터에 MutClust를 적용하면 두 논문을 더 밀접하게 연결할 수 있다.

### 8.1 개요

MutClust의 밀도 기반 핫스팟 탐지를 암 유전자(TP53, KRAS, PIK3CA 등)의 체세포 변이에 적용하고, 추출된 핫스팟 특징을 MOSD의 10가지 MOI 방법에 추가 오믹스 레이어로 투입한다.

### 8.2 장단점 비교

| 기준 | Option A: 범병원체 벤치마크 | Option B: TCGA 암 적용 |
|------|--------------------------|----------------------|
| **두 논문 연결 강도** | 방법론적 연결 (벤치마킹 철학 전이) | **직접적 연결** (같은 TCGA 데이터) |
| **신규성** | **높음** (범병원체 핫스팟 벤치마크 없음) | 중간 (DMCM, OncodriveCLUST 등 선행 존재) |
| **경쟁 위험** | **낮음** (니치에 아무도 없음) | 중간 (deepCDG, GRAFT 등 GNN 경쟁) |
| **데이터 재사용** | 새 데이터 (NCBI 바이러스) | **기존 MOSD 데이터 재활용** |
| **시의성** | **높음** (H5N1, pandemic preparedness) | 보통 |
| **GPU 필요** | 불필요 | 불필요 |
| **논문 임팩트** | Bioinformatics/Genome Biology | PLOS Comp Bio/Bioinformatics |
| **PhD 서사 강도** | 강함 (벤치마킹→알고리즘→범용화) | **매우 강함** (같은 데이터에서 두 방법 통합) |

### 8.3 결론: 하이브리드 접근 추천

**두 옵션을 결합**하는 것이 최적이다:

1. **TCGA 적용 (Option B의 핵심)**: MutClust를 TCGA 체세포 변이에 적용하여 핫스팟 특징 추출 → MOSD 파이프라인에 투입 → cluster-score로 평가. 이는 두 논문의 직접적 연결을 만든다.

2. **범병원체 검증 (Option A의 핵심)**: 동시에 바이러스 데이터에서도 벤치마크 수행. 이는 범용성을 입증한다.

이렇게 하면 Bridge Paper가 **"Cancer AND Virus 양쪽에서 작동하는 통합 프레임워크"**가 되어, 단일 도메인보다 훨씬 강력한 기여가 된다.

---

## 9. 최신 관련 연구 (2023-2026, 에이전트 조사 결과)

### 암 변이 + 다중오믹스 통합 최신 동향

| 방법 | 연도 | 핵심 | 참고 |
|------|------|------|------|
| CIMLR | 2018+ | 점 변이+CNV+메틸화+발현으로 32개 암종 서브타이핑 | Nat Comm |
| deepCDG | 2025 | GCN으로 변이+메틸화+발현 통합, 드라이버 유전자 예측 | BIB |
| DriverOmicsNet | 2025 | GCN+WGCNA, 15개 암종 5,555 샘플 | BIB |
| GRAFT | 2025 | 그래프 트랜스포머, 변이+메틸화+발현 48D 특징 | BIB |
| ModVAR | 2025 | DNA서열+구조+오믹스로 드라이버 변이 분류, AUROC 0.985 | Comm Med |
| NetFlow3D | 2024 | 3D 구조 기반 변이 클러스터링 + 네트워크 전파 | Nat Comm |
| DMCM | 2019 | 적응형 커널 밀도 추정 기반 변이 클러스터링 (MutClust 직접 경쟁자) | Bioinformatics |
| DCMC | 2025 | 분리 대조 다중뷰 클러스터링, 10개 데이터셋에서 19개 방법 대비 우수 | PLOS Comp Bio |
| mlscluster | 2024 | 다수준 선택 기반 계통 클러스터링, SARS-CoV-2 120만 서열 | Wellcome OR |

### 핵심 발견

1. **적응형 클러스터링이 두 분야의 공통 트렌드**: 변이 핫스팟(DMCM, MutClust)과 다중오믹스 서브타이핑(DCMC, CSSEC) 모두 적응형 방법으로 수렴
2. **변이 + 다중오믹스 통합 연구 설계 도구가 부재**: MultiPower는 다중오믹스 검정력만, SEQPower는 변이 검정력만 다룸. 두 가지를 통합한 도구 없음
3. **GNN이 통합 프레임워크로 부상**: 하지만 GPU 필요 + 블랙박스 문제 → MutClust의 해석 가능성이 차별화 포인트
4. **바이러스 게놈학이 다중오믹스 통합에서 뒤처짐**: MutClust가 바이러스에서 가장 직접적인 연결 사례

---

## 10. 참고 문헌 (Bridge Paper 관련)

### 벤치마킹 방법론
- Han et al. (2025) "MOSD: Multi-omics study design" BMC Genomics 26:769
- Weber et al. (2019) "Essential guidelines for computational method benchmarking" Genome Biology 20:125
- Mangul et al. (2019) "Systematic benchmarking of omics computational tools" Nature Communications 10:1393

### 핫스팟 탐지 방법
- Youn, Jeong, Kwon et al. (2025) "MutClust" BioData Mining 18:61
- Munoz et al. (2020) "MutSpot" npj Genomic Medicine 5:22
- Tokheim et al. (2016) "HotMAPS" Cancer Research 76:13

### 범병원체 분석
- CoVerage (2025) Nat Comm 16:6281 - in silico genomic surveillance
- Mazzocchetti et al. (2024) Nat Comm - coordinated substitution networks
- Osia et al. (2024) "mlscluster" Wellcome Open Research

### 다중오믹스 + 변이 통합
- CIMLR (2018) Nat Comm - multi-omic cancer subtypes including point mutations
- DriverOmicsNet (2025) BIB - multi-omics cancer driver gene prediction
- GRAFT (2025) BIB - graph-aware fusion for driver gene prediction

### 시뮬레이션 도구
- GENOMICON-Seq (2025) - 현실적 서열 시뮬레이션
- PySNV (2024) - 변이 시뮬레이터
- pyvolve - 진화 서열 시뮬레이션
