# PhD Presentation v8 — 수정 이력 전체 기록

**대상 파일**: `PhD_Presentation_v8_EN.pptx`
**최종 슬라이드 수**: 22장
**작업 기간**: 2026-03-05

---

## 1차 수정: v8 기본 보정

> 사용자가 PowerPoint에서 v7 → v8로 수동 편집한 후, 검토 및 보정 요청

### 1-1. 슬라이드 4 제목 변경
- **변경 전**: "Paper 1: The Challenge of Multi-Omics Integration"
- **변경 후**: "Paper 1"
- **이유**: 슬라이드 12(Paper 2)와 동일한 형식 통일

### 1-2. 슬라이드 15 중복 제거
- "Key Innovations" 텍스트가 두 개 존재 (정상 4.9" + 중복 오버레이 7.7")
- 7.7" 너비의 대형 오버레이 shape 제거

### 1-3. 슬라이드 18 신규 생성 (Influenza Cross-Validation)
- Paper 2 Summary에 포함되어 있던 인플루엔자 검증 내용을 별도 슬라이드로 분리
- 3개 strain 카드 (A/H1N1, A/H3N2, B/Victoria) + 하단 요약 카드
- 슬라이드 재배치: 최종 위치 18번 (Paper 2 Summary 앞)

### 1-4. 슬라이드 번호 및 TOC 갱신
- 전체 20장 → 21장
- N/21 형식으로 모든 슬라이드 번호 갱신
- TOC: Paper 2 → 11–19, Conclusion → 20–21

**백업**: `PhD_Presentation_v8_EN_backup.pptx`
**스크립트**: `modify_v8.py`

---

## 2차 수정: 로고 및 시각 보정

### 2-1. RED 배경 슬라이드 로고 흰색화
- 슬라이드 11–19 (Paper 2 구간): RED 헤더 위의 KNU 로고를 흰색 버전으로 교체
- `knu_symbol_white.png` 생성 (PIL/numpy로 모든 비투명 픽셀 → #FFFFFF)

### 2-2. 슬라이드 21 (Thank You) 로고 제거
- Q&A 슬라이드 우측 상단 로고 삭제 (불필요)

---

## 3차 수정: 콘텐츠 리뷰 반영

> 3개 병렬 에이전트로 논문 PDF 대조 검토 수행 후 14건 이슈 도출

### 3-1. 슬라이드 9 (Guidelines) — PINSPlus 표현 수정
- **변경 전**: "Maintains performance even at 80% noise"
- **변경 후**: "Highest noise robustness; last to degrade"
- **이유**: 논문에 따르면 80% noise에서는 **모든 알고리즘이 실패** (cluster-score < 0.10). PINSPlus가 "가장 마지막까지 버틴다"는 의미이지 "80%에서도 잘 작동한다"는 의미가 아님.

### 3-2. 슬라이드 17 (Severity) — SMS/MMS 약어 정의 추가
- "Dominant Signatures in Severe Patients" 제목 아래에 텍스트 박스 추가:
  - "SMS = Severe Mutation Signature"
  - "MMS = Moderate Mutation Signature"
- **이유**: SMS/MMS가 핵심 비교 지표로 사용되나 어디에서도 정의되지 않았음

### 3-3. 스크립트 문서 전면 재작성
주요 변경 사항:

| 항목 | 내용 |
|------|------|
| S3 Epitope 연결 | "뒤에 나올 Spike 변이의 면역 회피와 직결됩니다" 추가 |
| S4 TCGA 확장 | 첫 언급 시 "The Cancer Genome Atlas" 풀어쓰기 |
| S5 BLCA 명시 | "이 특징 수는 BLCA(방광암) 기준" 추가 |
| S6 요인 카운팅 기준 | "체계적으로 변화시켜 효과를 측정한 것" 설명 추가 |
| S9 PINSPlus | "80%에서도 성능 유지" → "가장 높은 내성, 마지막까지 성능 유지" |
| S10→S11 전환 | Paper 1→2 브릿지 문장 추가 |
| S15 CCM 확장 | "Core Cluster Member" 풀어쓰기 |
| S17 SMS/MMS | 첫 사용 시 풀어쓰기 + BH 보정 대상(28개) 명시 |
| S17 NK cell 한계 | "가설 기반 개념적 모델이며 실험적 검증 필요" 강조 |
| S17 KDCA 설명 | "질병관리청(KDCA)" 풀어쓰기 + 코호트 구성 설명 |
| 총 시간 | 22분10초 → 18분05초로 축약 |

### 3-4. 슬라이드 6 (Prior Work) — 테이블 수치 검증
- MOSD 논문의 "요인 분석" = 해당 요인을 **독립변수로 체계적 조작**하여 효과 측정
- 현재 수치 (Rappoport 0/6 comp, Duan 0/6 comp 등)은 논문 방법론과 일치 → **변경 불필요**
- 스크립트에서 카운팅 기준 설명 추가로 보완

**백업**: `PhD_Presentation_v8_EN_pre_review.pptx`
**스크립트**: `fix_v8_review.py`

---

## 4차 수정: 결과 슬라이드 추가 + 결론 강화 + 로고 정렬

> 콘텐츠 갭 분석 결과 S9(Guidelines)에 근거 figure가 전혀 없는 것이 가장 큰 문제로 확인

### 4-1. 슬라이드 9 신규 삽입 — "Paper 1: Benchmark Results"
- **위치**: S8 (Data and Benchmark Design)과 기존 S9 (Guidelines) 사이
- **콘텐츠**:
  - TEAL 헤더: "Paper 1: Benchmark Results — Evidence for Guidelines"
  - 3개 Evidence Figure (가로 배치):
    - 좌: Sample Size ≥26 + Class Balance <3:1 violin plots (`mosd_p5.png`)
    - 중: Feature Selection 1–10% optimal window (`mosd_p6.png`)
    - 우: Noise Tolerance 30% cliff (`mosd_p7.png`)
  - 하단 요약 카드: 4개 핵심 발견 정리
- **이유**: S10(Guidelines)에서 "26개 이상", "10% 이하", "30% 미만" 등의 가이드라인을 주장하지만 근거 데이터가 없어, 심사위원의 "이 수치의 근거가 뭐냐" 질문에 대응 불가

### 4-2. 슬라이드 21 (Conclusion) — 두 논문 연결 강화
- **변경 전** (표면적 공통점):

| 카드 | 제목 |
|------|------|
| 1 | Robust Data Design (MOSD) |
| 2 | Context-Aware Algorithm (MutClust) |
| 3 | From Data to Clinical Insight |

- **변경 후** (연구 철학적 연결):

| 카드 | 제목 | 핵심 메시지 |
|------|------|------------|
| 1 | **Evaluating Methods (MOSD)** | 기존 10가지 방법을 평가하는 프레임워크 |
| 2 | **Creating Methods (MutClust)** | DBSCAN의 한계를 극복하는 새 알고리즘 창조 |
| 3 | **Unifying Theme: Data-Driven Discovery** | 평가자 → 창조자 진화 + 데이터 기반 임계값 발견 |

- **연결 논리**: Paper 1에서 기존 방법을 체계적으로 평가한 경험이 Paper 2에서 새로운 알고리즘을 설계하는 데 이어짐. 두 논문 모두 자의적 기준이 아닌 **데이터에서 도출된 정량적 임계값**을 제시 (26 samples, 10% features, 3:1 ratio, 30% noise | γ from 5-dist plot, CCM 4조건, BH 보정).

### 4-3. 슬라이드 22 (Thank You) — 로고 중앙 정렬
- **변경 전**: left = 5.90" (중심 = 6.40", 슬라이드 중심 6.67"에서 0.27" 좌측 편향)
- **변경 후**: left = 6.17" (중심 = 6.67", 정확히 슬라이드 중앙)

### 4-4. 전체 정합성 갱신
- 슬라이드 번호: N/22 (전체 22장)
- TOC (S2): Paper 1 → Slides 4–11, Paper 2 → Slides 12–20, Conclusion → Slides 21–22
- 스크립트 문서: 22장 체계로 전면 반영

**백업**: `PhD_Presentation_v8_EN_pre_final.pptx`
**스크립트**: `fix_v8_final.py`

---

## 5차 수정: S9 리디자인 — Cluster-score 정의 + 6개 Figure 셀

> 사용자 요청: "cluster score에 대한 내용이 빠져있다. 그리고 s9에 기존그림들 제거하고 한 항목씩 그림넣을 공간을 만들어줘"

### 5-1. 기존 S9 콘텐츠 제거
- 3개 Playbook 페이지 이미지 (mosd_p5, p6, p7) + 3개 라벨 + 요약 카드 + 텍스트 → 총 8개 shape 제거
- 헤더, 타이틀, 푸터, 로고, 슬라이드 번호 (shape 0–5)는 유지

### 5-2. Cluster-score 정의 배너 추가
- **위치**: 타이틀 바로 아래 (top=0.95", height=0.50")
- **디자인**: TEAL_L (#E0F2F1) 배경, TEAL (#0D7377) 테두리, 라운드 사각형
- **텍스트**:
  > Evaluation Metric: Cluster-score = ( ARI + NMI + F-measure ) / 3 — Combines chance-corrected, information-theoretic, and set-based perspectives to avoid single-metric bias

### 5-3. 6개 Figure Placeholder 셀 (3열 × 2행 그리드)
- **셀 크기**: ~3.91" × 2.6" (gap: 0.20" 가로, 0.15" 세로)
- **각 셀 구성**:
  1. 상단: 제목 (TEAL bold) + 임계값 (NAVY bold)
  2. 중앙: 흰색 [Figure] placeholder 영역 (수동 그림 삽입용)
  3. 하단: 캡션 (DGRAY, 9pt)

| 위치 | 제목 | 임계값 | 캡션 |
|------|------|--------|------|
| 1행 좌 | 1. Sample Size | ≥ 26 per class | Variance stabilizes at 26; below → catastrophic failure |
| 1행 중 | 2. Class Balance | < 3:1 ratio | Imbalance >3:1 → bimodal distribution (p<0.0001) |
| 1행 우 | 3. Feature Selection | 1–10% optimal | Peak at 1–10%; using 100% → system failure |
| 2행 좌 | 4. Noise Tolerance | < 30% threshold | 30% cliff; >80% → total failure (score <0.10) |
| 2행 중 | 5. Omics Combination | GE-ME preferred | Gene Expression + Methylation best across 10 cancers |
| 2행 우 | 6. Subtype Distinctness | Molecular > clinical | Molecularly distinct pairs → high score (>0.90) |

### 5-4. 타이틀 업데이트
- **변경 전**: "Paper 1: Benchmark Results — Evidence for Guidelines"
- **변경 후**: "Paper 1: Benchmark Results"

### 5-5. 스크립트 문서 업데이트
- S9 섹션 전면 재작성: Cluster-score 정의 설명 + 6개 항목별 근거 설명 구어체 스크립트
- 발표 시간: 1분 30초 (6개 항목 × ~15초)

**백업**: `PhD_Presentation_v8_EN_pre_s9redesign.pptx`
**스크립트**: `fix_s9_redesign.py`

---

## 최종 슬라이드 구성 (22장)

| # | 제목 | 구간 |
|---|------|------|
| 1 | Title | 도입 |
| 2 | Table of Contents | 도입 |
| 3 | Key Terminology | 도입 |
| 4 | Paper 1 (Cover) | Paper 1 |
| 5 | Paper 1: The Challenge of Multi-Omics Integration | Paper 1 |
| 6 | Paper 1: Prior Work and Research Gap | Paper 1 |
| 7 | Paper 1: MOSD — 9-Factor Benchmark Framework | Paper 1 |
| 8 | Paper 1: Data and Benchmark Design | Paper 1 |
| **9** | **Paper 1: Benchmark Results — Evidence for Guidelines** | **Paper 1 (NEW)** |
| 10 | Paper 1: MOSD Guidelines & Method Profiles | Paper 1 |
| 11 | Paper 1 Summary: MOSD Framework | Paper 1 |
| 12 | Paper 2 (Cover) | Paper 2 |
| 13 | Paper 2: The Frequency Trap | Paper 2 |
| 14 | Paper 2: Three Approaches Compared | Paper 2 |
| 15 | Paper 2: H-score | Paper 2 |
| 16 | Paper 2: MutClust Algorithm | Paper 2 |
| 17 | Paper 2: Hotspot Detection Results | Paper 2 |
| 18 | Paper 2: Severity & Biological Significance | Paper 2 |
| 19 | Paper 2: Influenza Cross-Validation | Paper 2 |
| 20 | Paper 2 Summary | Paper 2 |
| 21 | Conclusion | 결론 |
| 22 | Thank You / Q&A | 결론 |

---

## 백업 파일 목록

| 파일 | 시점 | 설명 |
|------|------|------|
| `PhD_Presentation_v8_EN_backup.pptx` | 1차 수정 전 | 사용자 원본 v8 |
| `PhD_Presentation_v8_EN_pre_review.pptx` | 3차 수정 전 | 리뷰 반영 직전 |
| `PhD_Presentation_v8_EN_pre_final.pptx` | 4차 수정 전 | 결과 슬라이드 추가 직전 |
| `PhD_Presentation_v8_EN_pre_s9redesign.pptx` | 5차 수정 전 | S9 리디자인 직전 |

## 수정 스크립트 목록

| 파일 | 용도 |
|------|------|
| `modify_v8.py` | 1차: 제목, 중복제거, 인플루엔자 슬라이드, 재배치 |
| `fix_v8_review.py` | 3차: PINSPlus 표현, SMS/MMS 정의 |
| `fix_v8_final.py` | 4차: 결과 슬라이드, 결론 강화, 로고 정렬 |
| `fix_s9_redesign.py` | 5차: S9 리디자인 (Cluster-score 정의 + 6개 Figure 셀) |

---

## 예상 발표 시간

| 구간 | 슬라이드 | 시간 |
|------|---------|------|
| 도입 | S1–S3 | 1분 15초 |
| Paper 1 | S4–S11 | 7분 55초 |
| Paper 2 | S12–S20 | 8분 25초 |
| 결론 | S21–S22 | 1분 30초 |
| **합계** | **22장** | **~19분 05초** |

> 여유시간 약 1분 — S9(결과) 또는 S19(인플루엔자) 속도 조절로 대응
