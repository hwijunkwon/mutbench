# 박사학위논문 구조 및 내용 정리

**제목 (한글):** 다층적 게놈 데이터 분석을 위한 체계적 벤치마킹과 적응형 클러스터링 프레임워크
**제목 (영문):** Systematic Benchmarking and Adaptive Clustering Frameworks for Multi-Scale Genomic Data Analysis
**저자:** 권휘준
**지도교수:** 정인욱
**소속:** 경북대학교 대학원 컴퓨터학부
**총 페이지:** 152p
**컴파일:** XeLaTeX + bibtex, 에러 0개

---

## 전면부

- 겉표지 (博士學位論文)
- 속표지
- 인준지 (심사위원 5인 서명란)
- 감사의 글
- 한글 초록
- 목차 / 표목차 / 그림목차

---

## 제 1 장: Introduction (~10p)

| 절 | 내용 |
|---|---|
| 1.1 Research Background | 게놈 데이터 폭증, 다중오믹스 통합과 바이러스 감시의 도전 |
| 1.2 Research Motivation | Problem 1: MOI 벤치마크 부재, Problem 2: 핫스팟 탐지 평가 부재, Problem 3: 방법론 전이 부재 |
| 1.3 Research Objectives | MOSD 구축, MutClust 개발, MutBench 통합 |
| 1.4 Research Contributions | 최초 MOI 벤치마크, 적응형 핫스팟 탐지, 통합 벤치마크 프레임워크, 교차 도메인 전이 |
| 1.5 Dissertation Organization | 6장 구조 안내 |

---

## 제 2 장: Literature Review (~20p)

| 절 | 내용 |
|---|---|
| 2.1 Multi-Omics Integration | SNF, CIMLR, NEMO, PINS 등 MOI 방법론 동향, 그래프/행렬분해/합의 기반 접근, 기존 벤치마크 한계 |
| 2.2 Viral Mutation Hotspot Detection | 빈도 기반, 엔트로피 기반, 암 게놈학 핫스팟, 밀도 기반 접근 |
| 2.3 Clustering-Based Bioinformatics | DBSCAN, HDBSCAN, OPTICS, 계통발생 인식, 적응형 클러스터링 |
| 2.4 Benchmarking Frameworks | Weber et al. 가이드라인, MOSD, DMS ground truth |
| 2.5 Research Gaps | (1) MOI 설계 프레임워크 (2) 핫스팟 벤치마크 (3) 교차 전이 부재 |

---

## 제 3 장: MOSD Framework [Paper 1, BMC Genomics 2025, 26:769] (~25p)

| 절 | 내용 |
|---|---|
| 3.1 Introduction | TCGA 다중오믹스 통합 벤치마킹의 필요성 |
| 3.2 Methods | MOSD 프레임워크: 9 요인, 7 벤치마크 데이터셋, 10 MOI 방법, cluster-score = (ARI+NMI+F)/3 |
| 3.3 Experimental Results | 샘플 크기(26개↑), 피처 선택(1-10%), 전처리, 노이즈 강건성, 클래스 균형, 생물학적 요인, 방법 비교 |
| 3.4 Guidelines | 5가지 정량적 연구 설계 가이드라인 도출 |
| 3.5 Chapter Summary | → Chapter 5(MutBench) 연결: "같은 벤치마킹 철학을 바이러스 게놈학에 적용" |

---

## 제 4 장: MutClust Algorithm [Paper 2, BioData Mining 2025, 18:61] (~30p)

| 절 | 내용 |
|---|---|
| 4.1 Introduction | SARS-CoV-2 변이 핫스팟 탐지의 필요성 |
| 4.2 Methods | H-score = log₂(P×E×100+1), CCM 조건, 적응적 이웃 반경(Dε), 감쇠 인자, 알고리즘 워크플로우 |
| | 데이터: GISAID 시퀀스 + KDCA 환자 코호트 |
| | 중증도 연관 분석, 면역학적 분석 (네트워크 전파, DEG, HLA-에피톱) |
| 4.3 Results | 477개 핫스팟, 중증도 연관 핫스팟, NK세포 기능장애 발견, 인플루엔자 검증 |
| 4.4 Complexity | O(n²) |
| 4.5 Summary & Limitations | 한계: (1) 하드코딩 파라미터 (2) 벤치마크 부재 (3) expand_cluster 버그 → "Chapter 5에서 해결" |

---

## 제 5 장: MutBench Framework [Paper 3, 투고 준비] (~35p) ⭐ 핵심 챕터

### 5.1 서론
- MOSD→MutClust→MutBench 연결 동기
- 벤치마킹 공백 문제: 바이러스 핫스팟 탐지에 체계적 평가 프레임워크 없음

### 5.2 관련 연구
- 기존 핫스팟 탐지 방법론 (MutSpot, HotMAPS, OncodriveCLUST)
- 벤치마킹 프레임워크 (Weber et al. 2019)

### 5.3 방법론
| 항목 | 내용 |
|---|---|
| 프레임워크 구조 | 3계층: Ground Truth 생성 → 탐지 방법 → 평가 지표 |
| 5가지 변이체 | v1: MutClust-Original, v2a: Fixed, v2b: dNdS, **v2c: Hybrid**, v3: HDBSCAN-Auto |
| 버그 수정 | expand_cluster 누적 감쇠 → 단일 단계 감쇠 (71-95% 범위 손실 해결) |
| Hybrid 접근 | CCM 시드 탐지 + HDBSCAN 경계 결정 |
| hotspot-score | (recall + precision + stability) / 3 |
| DMS 벤치마크 | Dadonaite et al. 2023 cell entry fitness |
| 통계적 검증 | Bootstrap CI (100회), Permutation test (1000회), Pairwise comparison |

### 5.4 실험 결과

**Table 5.1: 변이체 비교 (핵심 결과)**

| Method | Precision | Recall | F1 | Hotspot-score |
|---|---|---|---|---|
| MutClust-Original | 0.991 | 0.504 | 0.669 | 0.638 |
| MutClust-Fixed | 0.988 | 0.506 | 0.669 | 0.646 |
| MutClust-dNdS | 0.988 | 0.506 | 0.669 | 0.646 |
| **MutClust-Hybrid** | **0.968** | **0.659** | **0.785** | **0.778** |
| HDBSCAN-Auto | 0.079 | 0.944 | 0.146 | 0.603 |

**통계적 검증:**
- 모든 method: permutation p < 0.001 (random보다 유의하게 우수)
- v2c-full vs 나머지: 모든 pairwise p < 0.001
- Bootstrap 95% CI: v2c-full hotspot-score 0.776 [0.644, 0.669]

**샘플 크기 민감도:**
- n=1,000이면 Spearman ρ > 0.997 수렴
- Hotspot-score ~0.62로 안정화
- 결론: 10K 시퀀스 충분

**시간적 일반화 (GISAID 2024-2025):**
- 9,957개 full-genome sequences (2024-01-01 ~ 2025-12-31, Host: Human)
- **H-score 포화**: 1,273 위치 전부 non-zero (mean 8.47, std 0.098) ← 2020-2021은 114 non-zero
- precision ~0.33 (= 1,251/3,819 baseline rate)로 수렴 → 판별력 상실
- 원인: Omicron 계통이 Wuhan-Hu-1 대비 너무 많은 변이 축적

**다중 Ground Truth 평가 (핵심 새 기여):**

| Ground Truth | 크기 | 최적 방법 | F1 | Enrichment |
|---|---|---|---|---|
| Functional regions | 439 (34.5%) | TC-freq-v2 | 0.474 | 1.16x |
| DMS-escape (top20%) | 252 (19.8%) | Saturated H-score | 0.315 | 1.11x |
| Convergent evolution | 97 (7.6%) | CH-score | 0.188 | 1.70x |
| Convergent strict | 29 (2.3%) | TC-freq-v3 | 0.108 | **3.43x** |

- Jaccard(DMS, Convergent) = **0.006** (거의 독립) → 서로 다른 생물학적 현상 측정
- **핵심 발견: "Population frequency ≠ functional importance" — 상보적 평가 관점**

### 5.5 논의
1. MOSD 벤치마킹 철학의 바이러스 게놈학 적용
2. 도메인 정보 + 자동 탐지의 하이브리드가 최적
3. H-score 포화 현상: adaptive reference 필요
4. 상보적 평가 관점: 단일 ground truth로는 불충분

### 5.6 소결
- MutBench의 5가지 기여 요약 → Chapter 6으로 연결

---

## 제 6 장: Conclusion (~12p)

| 절 | 내용 |
|---|---|
| 6.1 통합적 기여 | MOSD(정량적 기반), MutClust(적응형 탐지), MutBench(통합 벤치마크) |
| 6.2 Five Bridges | Bridge 1: 벤치마킹 전이 (cluster-score → hotspot-score) |
| | Bridge 2: 연구 설계 (9 요인 → 5 변이체) |
| | Bridge 3: 평가 지표 (복합 지표 철학) |
| | Bridge 4: 민감도 분석 (파라미터 → 샘플 크기) |
| | Bridge 5: 일반화 (TCGA → SARS-CoV-2 → 범병원체) |
| 6.3 한계점 | MOSD 한계, 계통발생 비독립성, 시뮬레이션-실제 갭, 단일 병원체, position-level 평가, NK세포 가설 미검증 |
| 6.4 향후 연구 | TreeTime 보정, 범병원체 확장, 다중 DMS 표현형, 실시간 감시, 딥러닝 통합 |
| 6.5 Concluding Remarks | "체계적 벤치마킹과 적응형 클러스터링이 게놈 데이터의 다양한 스케일에서 생물학적 발견을 촉진" |

---

## 후면부
- 참고문헌 (20+ references, bibtex)
- 영문 Abstract

---

## 주요 수치 요약

| 항목 | 값 |
|---|---|
| 총 페이지 | 152p |
| 챕터 수 | 6 |
| 테이블 수 (Ch5) | 8개 |
| 수식 수 (Ch5) | 5개 |
| GISAID 시퀀스 (시간적 검증) | 9,957개 (2024-2025) |
| MutClust-Hybrid hotspot-score | 0.778 (최고) |
| TC-freq-v3 enrichment | 3.43x (convergent strict) |
| GT 독립성 (DMS vs Convergent) | Jaccard = 0.006 |
| 통계적 유의성 | 모든 p < 0.001 |
