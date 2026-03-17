# MutBench PPT v4 슬라이드 수정 계획서

**현재**: v3 = 29 슬라이드
**목표**: v4 = 38 슬라이드 (생물학 기초 추가, 구조 재배치, 모든 슬라이드 이미지 포함)
**작성일**: 2026-03-17

---

## 전체 구조 변경 요약

| 변경 사항 | 현재 (v3) | 수정 (v4) |
|-----------|-----------|-----------|
| 논문 카드 | S1 (타이틀) 하단 | S3 (Prior Work)으로 이동 |
| 목차 레이아웃 | 2x3 그리드 | 세로(vertical) 리스트 |
| 생물학 기초 | 없음 | S4-S6 신규 3장 추가 |
| 용어 슬라이드 | S5 독립 슬라이드 | 삭제, 각 설명 슬라이드에 분산 통합 |
| 연구 기여 | S8 (초반) | S30으로 이동 (결과 뒤) |
| 연구 개요도 | 없음 | S7 신규 추가 |
| 9개 바이러스 설명 | 없음 | S16 신규 추가 |
| Scoring 도구 설명 | 간략 나열만 | S12 신규 추가 |
| 수식 | 텍스트 입력 | PPT 수식 편집기 사용 |

---

## 슬라이드별 상세 계획 (총 38장)

---

### S1. 타이틀 슬라이드
**현재 (v3 S1)**: 타이틀 + 논문 카드 2개 하단 배치
**변경**:
- 논문 카드 2개 **제거** (S3으로 이동)
- 빈 공간에 연구 핵심 키워드 또는 시각적 요소 배치
- 레이아웃: 상단 대학 로고/정보, 중앙 제목, 하단 저자/학과/날짜
- **필요 이미지**: 바이러스 게놈 + 벤치마크 개념을 조합한 배경 이미지
  - 검색어: `viral genome mutation analysis concept illustration`
  - 대안: PLACEHOLDER (사용자가 적절한 배경 삽입)

---

### S2. 목차 (Table of Contents)
**현재 (v3 S2)**: 2x3 그리드 레이아웃
**변경**:
- **세로(vertical) 리스트**로 전면 변경
- 왼쪽 60%: 세로 목차 리스트 (번호 + 섹션명 + 간략 설명 + 슬라이드 범위)
- 오른쪽 40%: 전체 연구 흐름을 보여주는 간략 아이콘/다이어그램
- 섹션 구성:
  1. Introduction (S3-S9)
  2. MutBench Framework (S10-S15)
  3. Stage 1: 4-Pathogen (S16-S20)
  4. Stage 2: 9-Pathogen (S21-S27)
  5. Extensions & PAHD (S28-S31)
  6. Conclusion (S32-S38)
- **필요 이미지**: 오른쪽에 flow arrow 다이어그램 (코드로 생성 가능)

---

### S3. Prior Work: MOSD & MutClust (논문 카드 통합)
**현재 (v3 S3)**: 텍스트 위주 2-column, 논문 카드 없음
**변경**:
- S1에서 이동한 **논문 카드 디자인** 적용
- 2-column 유지하되, 각 column 상단에 카드 스타일 (저널명, 제목, 아이콘)
- 하단에 "Common lesson" 배너 유지
- 각 카드에 핵심 figure 1개씩 추가
  - MOSD: cluster-score 비교 heatmap 축소 (논문에서 발췌)
  - MutClust: H-score scatter plot 축소 (논문에서 발췌)
- **필요 이미지**:
  - MOSD 논문 핵심 figure (PLACEHOLDER - 사용자 삽입)
  - MutClust 논문 핵심 figure (PLACEHOLDER - 사용자 삽입)

---

### S4. [신규] 생물학 기초 (1): 유전체와 DNA/RNA
**신규 슬라이드**
**목적**: CS 교수 대상으로 생물학 기본 개념 설명
**내용**:
- 왼쪽: DNA 이중나선 구조 → RNA 단일가닥 비교 다이어그램
- 중앙: 뉴클레오타이드 4종 (A, T/U, G, C) 색상 코딩
- 오른쪽: 게놈 = 유전 정보 전체 (DNA/RNA 서열)
- 하단: "바이러스는 대부분 RNA 게놈 → 돌연변이율 높음" 강조 박스
- **용어 통합**: Genome, Nucleotide, RNA/DNA 용어를 이 슬라이드에서 직접 설명
- **필요 이미지**:
  - DNA vs RNA 구조 비교 다이어그램
  - 검색어: `DNA RNA structure comparison diagram simple`
  - 대안: 코드로 간단한 다이어그램 생성 또는 PLACEHOLDER

---

### S5. [신규] 생물학 기초 (2): 돌연변이와 단백질
**신규 슬라이드**
**내용**:
- 왼쪽: Central Dogma (DNA → RNA → Protein) 화살표 다이어그램
- 중앙: 돌연변이 유형 (치환, 삽입, 결실) 간단 도식
  - 정상: A-T-G-C-A → 치환: A-**G**-G-C-A
- 오른쪽: 단백질 3D 구조 변화 개념 (돌연변이가 구조/기능 변화 유발)
- 하단: "같은 위치에 돌연변이가 반복 → Mutation Hotspot" 연결
- **용어 통합**: Mutation, Protein, Variant 용어를 여기서 설명
- **필요 이미지**:
  - 돌연변이 유형 도식: 검색어 `point mutation substitution insertion deletion diagram`
  - Central Dogma: 검색어 `central dogma DNA RNA protein simple diagram`
  - 대안: PLACEHOLDER 2개

---

### S6. [신규] 생물학 기초 (3): 바이러스와 진화
**신규 슬라이드**
**내용**:
- 왼쪽: 바이러스 기본 구조 (Spike protein, envelope, RNA genome 표시)
- 중앙: 바이러스 복제 과정 → 복제 오류 = 돌연변이 발생
- 오른쪽: 자연선택 개념
  - Positive selection: 면역 회피 돌연변이 확산
  - Purifying selection: 필수 기능 손상 돌연변이 제거
  - Convergent evolution: 독립적 계통에서 같은 돌연변이 발생
- **용어 통합**: Positive selection, Purifying selection, Convergent evolution 여기서 설명
- **필요 이미지**:
  - 바이러스 구조 다이어그램: 검색어 `coronavirus structure diagram spike protein labeled`
  - 대안: PLACEHOLDER

---

### S7. [신규] 연구 개요도 (Research Overview)
**신규 슬라이드**
**내용**: 전체 연구를 하나의 다이어그램으로 요약
- 전체 슬라이드를 하나의 flow diagram으로 사용
- 흐름:
  - 문제 인식 (H-score founder bias, single-pathogen limitation)
  - → MutBench 프레임워크 설계 (pipeline, 3-layer GT)
  - → Stage 1: 4-pathogen 비교 (ranking reversal 발견)
  - → Stage 2: 9-pathogen 확장 (ANOVA, 통계 검증)
  - → PAHD 알고리즘 제안
- 좌→우 또는 위→아래 flow로 배치
- 각 단계에 핵심 숫자 포함 (9 pathogens, 2544 evaluations, omega-sq=0.285 등)
- **필요 이미지**: 코드로 생성 (matplotlib/drawio) 또는 PLACEHOLDER

---

### S8. Mutation Hotspot이란? (기존 v3 S4 기반)
**현재 (v3 S4)**: 텍스트 위주 3-column (Why occur / Why important / Current problems)
**변경**:
- 상단 정의 박스 유지
- 3-column 구조 유지하되, 각 column 상단에 **아이콘/이미지** 추가
  - Why occur: 게놈 위치별 돌연변이 밀도 히스토그램 (코드 생성)
  - Why important: 백신/약물 타겟 관련 이미지
  - Current problems: 비교 불가 상황 도식
- **용어 통합**: MSA (Multiple Sequence Alignment) 개념을 여기서 간략 설명 (별도 슬라이드 불필요)
- **필요 이미지**:
  - 게놈 위치별 돌연변이 빈도 히스토그램: `genome_hotspot_map.png` 활용 가능
  - 검색어: `mutation hotspot genome map visualization`

---

### S9. Why Hotspot Detection Matters (기존 v3 S6 기반)
**현재 (v3 S6)**: 3-column (Vaccine / Surveillance / Drug) 텍스트 위주
**변경**:
- 3-column 유지
- 각 column에 **적절한 아이콘/이미지** 추가
  - Vaccine Design: 백신 주사기 + 게놈 타겟 아이콘
  - Variant Surveillance: 시계열 모니터링 개념 이미지
  - Drug Development: 약물-단백질 결합 개념 이미지
- **필요 이미지**:
  - 검색어: `vaccine development genomics icon`, `virus surveillance monitoring`, `antiviral drug target protein`
  - 대안: PLACEHOLDER 3개 (각 column 상단)

---

### S10. Problem Definition (기존 v3 S7)
**현재 (v3 S7)**: P1/P2/P3 세로 나열, 텍스트만
**변경**:
- 레이아웃 유지 (이미 잘 구조화됨)
- 각 문제(P1, P2, P3) 옆에 **시각적 예시** 작은 이미지 추가
  - P1 (No Benchmark): 서로 다른 데이터셋/메트릭 사용 비교 불가 도식
  - P2 (Single-Pathogen): 1-2개 바이러스만 테스트하는 문제 (vs 9개)
  - P3 (No Universal Best): ranking reversal 미니 차트
- **필요 이미지**: 코드로 간단한 개념 아이콘 생성 또는 PLACEHOLDER

---

### S11. MutBench Pipeline Overview (기존 v3 S9 기반)
**현재 (v3 S9)**: 파이프라인 6단계 가로 배치 + 하단에 scoring/detection 나열, 텍스트가 중앙에 떠있는 느낌
**변경**:
- **전면 재설계**
- 상단: 파이프라인 flow (Input → MSA → Scoring → Detection → GT → Eval) — 화살표 + 아이콘 강화
- 하단 전체를 2-column으로 재구성:
  - 좌측: 9 Scoring Methods (카테고리별 그룹핑 + 색상 코딩)
  - 우측: Detection Families (카테고리별 그룹핑 + 색상 코딩)
- 파이프라인 각 단계에 작은 아이콘 배치
- **빈 공간 문제 해결**: 하단 scoring/detection을 표(table) 형식으로 정리
- **필요 이미지**: 코드로 파이프라인 다이어그램 생성

---

### S12. [신규] Scoring 방법 상세 설명
**신규 슬라이드**
**내용**: 9개 scoring 방법의 원리를 간략히 설명
- 3x3 그리드 레이아웃
- 각 셀: 방법명 + 핵심 원리 1줄 + 수식 또는 개념 아이콘
  1. Shannon Entropy: 위치별 뉴클레오타이드 불확실성
  2. Jensen-Shannon Divergence: 배경 대비 분포 차이
  3. Mutation Frequency: 변이 비율 (1 - dominant)
  4. Wavelet (CWT): 다중 스케일 주파수 분석
  5. Sliding Window: 구간 평균 기반 평활화
  6. Phylo-aware Score: 계통 가중치 적용
  7. dN/dS ratio: 비동의/동의 치환 비율
  8. Kabat Variability: 위치별 아미노산 다양성
  9. Property Entropy: 물리화학적 성질 기반
- **수식**: PPT 수식 편집기 사용 (Shannon entropy H = -sum p log p 등)
- **필요 이미지**: 각 방법의 개념을 나타내는 미니 차트 (코드 생성 가능)

---

### S13. 3-Layer Ground Truth Design (기존 v3 S10)
**현재 (v3 S10)**: 좌측 figure + 우측 3개 설명 박스
**변경**:
- figure 크기 적절히 조정 (텍스트 가독성 확보)
- figure가 슬라이드의 55% 이상 차지하도록
- 우측 설명 박스 폰트 크기 유지
- **기존 figure**: `multi_ground_truth_figure.png` 사용 중 — 가독성 확인 필요
- **필요 이미지**: 기존 figure 재생성 (더 큰 폰트, 더 선명한 색상)

---

### S14. Evaluation Metric: MCC (기존 v3 S11)
**현재 (v3 S11)**: 좌측 수식+설명, 우측 큰 이미지, 하단 좌측 빈 공간
**변경**:
- **수식**: PPT 수식 편집기로 MCC 공식 입력 (plain text 대체)
- 좌측 빈 공간에 **confusion matrix 다이어그램** 추가 (TP/TN/FP/FN 시각화)
- 우측 이미지 크기 적절히 조정
- 하단에 "Why MCC > F1?" 비교표 추가
- **필요 이미지**:
  - confusion matrix 다이어그램 (코드 생성)
  - MCC vs F1 비교 차트: `mcc_vs_f1_fairness.png` 활용

---

### S15. Two-Stage Experimental Design (기존 v3 S12)
**현재 (v3 S12)**: 2-column (Stage 1 / Stage 2), 하단 좌측 빈 공간
**변경**:
- 2-column 유지
- 각 column에 **사용 데이터 규모** 시각화 (아이콘 + 숫자)
- 하단 빈 공간에 **Stage 1→Stage 2 확장 화살표 다이어그램** 추가
- 또는 하단에 데이터 출처 표(table) 추가
- **필요 이미지**: 코드로 생성 (stage 전환 다이어그램)

---

### S16. [신규] 9개 바이러스 소개
**신규 슬라이드**
**내용**: 벤치마크에 사용된 9개 바이러스의 특성 비교
- 표(table) 형태: 바이러스명 | 게놈 크기 | 서열 수 | 주요 특징
- 또는 3x3 그리드로 각 바이러스 카드
  1. SARS-CoV-2: ~30kb RNA, Spike 중심
  2. Influenza: segmented RNA, 항원 변이
  3. HIV: ~10kb RNA, 높은 변이율
  4. Dengue: ~11kb RNA, 4개 혈청형
  5. MERS: ~30kb RNA, 낙타 유래
  6. RSV: ~15kb RNA, 영유아 감염
  7. Norovirus: ~7.5kb RNA, 위장관 감염
  8. HCV: ~9.6kb RNA, 만성 간염
  9. Ebola: ~19kb RNA, 출혈열
- 각 바이러스 옆에 작은 아이콘/이미지
- **필요 이미지**:
  - 바이러스 구조 아이콘 9개: 검색어 `[virus name] structure icon simple`
  - 대안: PLACEHOLDER (사용자가 각 바이러스 이미지 삽입)

---

### S17. Stage 1: Method Comparison Results (기존 v3 S13)
**현재 (v3 S13)**: 좌측 큰 figure + 우측 key findings
**변경**:
- figure 크기 조정 — 텍스트 읽을 수 있도록 (현재 너무 축소 가능성)
- figure 가로 65%, key findings 35%
- key findings 박스에 강조 색상 추가
- **기존 figure**: `method_comparison.png` — 재생성 필요시 폰트 크게
- **필요 이미지**: 기존 figure 활용, 필요시 재생성

---

### S18. Parameter Sensitivity Analysis (기존 v3 S14)
**현재 (v3 S14)**: 좌측 figure + 우측 4개 findings 박스
**변경**:
- figure 크기 검증 (텍스트 가독성)
- findings 박스 색상 코딩 (sensitivity 수준별)
- **기존 figure**: `sensitivity_heatmap.png` 활용
- **필요 이미지**: 기존 활용

---

### S19. Synthetic vs Real Data Gap (기존 v3 S15)
**현재 (v3 S15)**: 비교표 형태 (Aspect | Synthetic | Real)
**변경**:
- 비교표 상단에 좌/우 레이블 강조 (Synthetic vs Real 헤더 색상 대비)
- 비교 포인트마다 **핵심 차이를 강조하는 하이라이트** 추가
- 하단 결론 박스 유지
- 빈 공간에 synthetic vs real 데이터의 분포 비교 차트 추가
- **필요 이미지**:
  - synthetic vs real 분포 비교: 코드로 간단한 히스토그램 쌍 생성 가능
  - 대안: PLACEHOLDER

---

### S20. Cross-Pathogen Ranking Reversal (기존 v3 S16)
**현재 (v3 S16)**: 좌측 figure + 우측 "9/9" 강조
**변경**:
- figure 크기 확인/조정
- "9/9 unique best combinations" 시각적 강조 강화
- **기존 figure**: `cross_pathogen_comparison.png` 또는 `cross_pathogen_top5.png` 활용
- **필요 이미지**: 기존 활용

---

### S21. Stage 2: Scaling to 9 Pathogens (기존 v3 S17)
**현재 (v3 S17)**: 3개 큰 숫자 카드 (9 / 2,544 / 4)
**변경**:
- 레이아웃 유지 (이미 시각적으로 좋음)
- 각 카드에 작은 아이콘 추가 (바이러스 아이콘, 그래프 아이콘, 통계 아이콘)
- 하단에 9개 바이러스 이름 가로 배열 (아이콘 포함)
- **필요 이미지**: 아이콘 3개 (코드 또는 PLACEHOLDER)

---

### S22. Two-Way ANOVA: Variance Decomposition (기존 v3 S18)
**현재 (v3 S18)**: 좌측 figure + 우측 3개 결과 박스
**변경**:
- figure 가독성 확인
- 우측 박스에 비율 시각화 (작은 bar chart 또는 파이 차트 추가)
- **기존 figure**: `variance_decomposition.png` 활용
- **수식**: ANOVA 수식은 PPT 수식 편집기로 (필요시)
- **필요 이미지**: 기존 활용 + 미니 파이 차트 (코드 생성)

---

### S23. Per-Pathogen Best Combinations (기존 v3 S19)
**현재 (v3 S19)**: 좌측 figure + 우측 텍스트
**변경**:
- figure 크기 최적화
- 우측에 "H-score founder bias" 관련 scatter plot 미니 버전 추가
- **기존 figure**: `scoring_detection_heatmap.png` 또는 `cross_pathogen_comparison.png`
- **필요 이미지**: 기존 활용

---

### S24. Friedman Test & LOPO CV (기존 v3 S20)
**현재 (v3 S20)**: 2-column 텍스트 위주
**변경**:
- 각 column에 **결과 차트/테이블** 추가
  - Friedman: rank distribution bar chart 또는 rank table
  - LOPO: 9개 pathogen 예측 결과 confusion 또는 hit/miss 표
- 텍스트 줄이고 시각화 강화
- **필요 이미지**:
  - Friedman rank chart: 코드로 생성
  - LOPO hit/miss table: 코드로 생성
  - 대안: PLACEHOLDER 2개

---

### S25. ESM-2 Protein Language Model Validation (기존 v3 S21)
**현재 (v3 S21)**: 비교표 (Without/With ESM-2)
**변경**:
- 표 레이아웃 유지 (이미 깔끔)
- 하단에 ESM-2 아키텍처 개념도 또는 "protein language model" 개념 다이어그램 추가
- **필요 이미지**:
  - 검색어: `ESM-2 protein language model architecture diagram`
  - 대안: PLACEHOLDER

---

### S26. KEY FINDING: No Universal Best Method (기존 v3 S22)
**현재 (v3 S22)**: 4개 결과 박스 (ANOVA / Unique Best / Friedman / LOPO)
**변경**:
- 레이아웃 유지 (핵심 요약 슬라이드로 효과적)
- 각 박스에 작은 아이콘/시각적 강조 추가
- 중앙 상단 "No single method" 배너 강조 강화 (색상/크기)
- **필요 이미지**: 미니 아이콘 4개 (코드 또는 PLACEHOLDER)

---

### S27. PAHD: Pathogen-Adaptive Hotspot Detection (기존 v3 S23)
**현재 (v3 S23)**: 3단계 flow + 하단 결과
**변경**:
- 3단계 flow에 **각 단계별 아이콘/다이어그램** 강화
- 하단 결과 영역에 **baseline 비교 bar chart** 추가 (텍스트 대신 시각화)
- **필요 이미지**:
  - baseline comparison bar chart: `new_methodology_comparison.png` 활용 가능
  - 또는 코드로 MCC 비교 bar chart 생성

---

### S28. Phylogenetic Correction & Region Overlap (기존 v3 S24)
**현재 (v3 S24)**: 2-column 텍스트 위주
**변경**:
- 좌측 (Phylogenetic): phylogenetic tree 다이어그램 추가
- 우측 (Region Overlap): region-level vs position-level 비교 다이어그램
- 텍스트 비율 줄이고 시각화 비율 높이기
- **필요 이미지**:
  - phylogenetic tree: 검색어 `phylogenetic tree virus evolution diagram simple`
  - region overlap: `lopo_region_precision.png` 활용 가능
  - 대안: PLACEHOLDER 2개

---

### S29. Scoring-Detection Heatmap & Baseline Comparison (기존 v3 S25)
**현재 (v3 S25)**: figure 기반 (확인 필요)
**변경**:
- heatmap figure 크기 최적화 (가독성 확보)
- baseline comparison 테이블/차트 추가
- **기존 figure**: `scoring_detection_heatmap.png` 활용
- **필요 이미지**: 기존 활용

---

### S30. Research Contributions (기존 v3 S8 → 여기로 이동)
**현재 (v3 S8)**: 4개 기여 (C1-C4) 2x2 그리드
**변경 (위치 이동)**:
- 결과 이후로 배치 → 결과를 본 뒤 기여가 더 설득력 있음
- 레이아웃 유지하되 각 기여에 **관련 결과 숫자** 추가
- 각 기여 박스에 해당 결과 슬라이드 번호 참조 추가
- **필요 이미지**: 기여별 미니 아이콘 (코드 또는 PLACEHOLDER)

---

### S31. Discussion (기존 v3 S26)
**현재 (v3 S26)**: 텍스트 위주
**변경**:
- 주요 논점을 시각적으로 구조화
- 좌/우 비교: "What we expected" vs "What we found"
- 또는 strengths/limitations 2-column
- **필요 이미지**: 개념적 비교 다이어그램 (코드 생성 또는 PLACEHOLDER)

---

### S32. Contributions, Limitations & Future Work (기존 v3 S27)
**현재 (v3 S27)**: 텍스트 나열
**변경**:
- 3-section 레이아웃: Contributions | Limitations | Future Work
- 각 섹션에 아이콘 + 핵심 포인트
- Future Work에 PAHD 완성 로드맵 타임라인 추가
- **필요 이미지**: 타임라인 다이어그램 (코드 생성)

---

### S33. Key Takeaway (기존 v3 S28)
**현재 (v3 S28)**: 핵심 메시지
**변경**:
- 큰 텍스트 + 배경 이미지 조합
- 핵심 메시지 1-2문장만 크게
- 배경에 연구 개요도(S7)의 축소 버전 또는 관련 이미지
- **필요 이미지**: 반투명 배경 이미지 (PLACEHOLDER)

---

### S34. Thank You (기존 v3 S29)
**현재 (v3 S29)**: 감사 슬라이드
**변경**:
- 대학 로고 + 연구실 정보
- 이메일, GitHub 링크 추가
- QR 코드 (GitHub repo) 추가 고려
- **필요 이미지**: QR 코드 (코드 생성 가능)

---

### S35-S38. [백업 슬라이드] 예상 질의응답 대비
**신규 4장** (발표 시간에는 미포함, Q&A용)

**S35. 백업: DMS 데이터 상세**
- DMS 실험 원리, Starr 2020 / Dadonaite 2023 데이터
- DMS fitness landscape figure
- **필요 이미지**: `dms_scatter.png`, `dms_evaluation_comparison.png`

**S36. 백업: ANOVA 상세 결과**
- full ANOVA table, effect size 해석
- **필요 이미지**: `variance_decomposition.png` 상세 버전

**S37. 백업: 개별 바이러스 결과 비교**
- 9개 바이러스 각각의 top-5 방법 비교
- **필요 이미지**: `cross_pathogen_top5.png`

**S38. 백업: Wavelet 분석 상세**
- CWT scalogram 설명
- **필요 이미지**: `cwt_scalogram.png`, `scalogram_sarscov2.png`

---

## 이미지 소요 분류

### A. 기존 figure 활용 (재생성/크기 조정 필요)
| 슬라이드 | 파일명 | 비고 |
|----------|--------|------|
| S13 | `multi_ground_truth_figure.png` | 폰트 크게 재생성 |
| S17 | `method_comparison.png` | 가독성 확인 |
| S18 | `sensitivity_heatmap.png` | 가독성 확인 |
| S20 | `cross_pathogen_comparison.png` | 기존 활용 |
| S22 | `variance_decomposition.png` | 기존 활용 |
| S27 | `new_methodology_comparison.png` | baseline bar chart |
| S29 | `scoring_detection_heatmap.png` | 기존 활용 |
| S8 | `genome_hotspot_map.png` | hotspot 개념 |
| S14 | `mcc_vs_f1_fairness.png` | MCC 비교 |
| S28 | `lopo_region_precision.png` | region overlap |
| S35 | `dms_scatter.png` | 백업 |
| S38 | `cwt_scalogram.png`, `scalogram_sarscov2.png` | 백업 |

### B. 웹 검색으로 확보 필요
| 슬라이드 | 검색어 | 용도 |
|----------|--------|------|
| S4 | `DNA RNA structure comparison diagram` | 생물학 기초 |
| S5 | `point mutation types diagram`, `central dogma simple` | 돌연변이/단백질 |
| S6 | `coronavirus structure diagram labeled` | 바이러스 구조 |
| S9 | `vaccine genomics`, `virus surveillance` | 응용 분야 아이콘 |
| S25 | `ESM-2 protein language model architecture` | ESM-2 개념 |
| S28 | `phylogenetic tree virus evolution simple` | 계통수 |

### C. 코드로 생성 가능
| 슬라이드 | 내용 | 방법 |
|----------|------|------|
| S7 | 연구 개요 flow diagram | matplotlib/drawio |
| S11 | 파이프라인 다이어그램 | python-pptx shapes |
| S12 | scoring 방법 개념 미니차트 | matplotlib |
| S14 | confusion matrix 다이어그램 | matplotlib |
| S22 | 미니 파이 차트 | matplotlib |
| S24 | Friedman rank chart, LOPO table | matplotlib |
| S27 | baseline comparison bar chart | matplotlib |
| S34 | QR 코드 | qrcode library |

### D. PLACEHOLDER (사용자가 직접 삽입)
| 슬라이드 | 내용 |
|----------|------|
| S1 | 타이틀 배경 이미지 |
| S3 | MOSD/MutClust 논문 핵심 figure 각 1개 |
| S16 | 9개 바이러스 아이콘 |
| S19 | synthetic vs real 분포 비교 |
| S33 | Key Takeaway 배경 이미지 |

---

## 수식 PPT 편집기 적용 대상

| 슬라이드 | 수식 내용 |
|----------|-----------|
| S12 | Shannon Entropy: H = -Sigma p_i log_2 p_i |
| S12 | JSD, dN/dS 등 간략 수식 |
| S14 | MCC = (TP*TN - FP*FN) / sqrt((TP+FP)(TP+FN)(TN+FP)(TN+FN)) |
| S22 | omega-squared 수식 |

---

## 구현 우선순위

### Phase 1 (구조 변경) — 가장 먼저
1. 슬라이드 순서 재배치 (S8 → S30으로 이동)
2. S1에서 논문 카드 제거, S3에 통합
3. S2 목차 세로 레이아웃 변경
4. S5 용어 슬라이드 삭제, 내용 분산

### Phase 2 (신규 슬라이드 추가)
5. S4-S6 생물학 기초 3장 추가
6. S7 연구 개요도 추가
7. S12 Scoring 상세 설명 추가
8. S16 9개 바이러스 소개 추가
9. S35-S38 백업 슬라이드 추가

### Phase 3 (시각 개선)
10. 모든 슬라이드에 이미지/figure 확보
11. 기존 figure 가독성 검증 및 재생성
12. 빈 공간 채우기 (S11→S14, S12→S15 등)
13. S9→S11 파이프라인 재설계

### Phase 4 (마무리)
14. 수식 PPT 편집기 적용
15. 웹 검색 이미지 삽입
16. PLACEHOLDER 위치 마킹
17. 전체 일관성 검토 (색상, 폰트, 여백)
