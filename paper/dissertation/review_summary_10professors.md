# 박사학위논문 Chapter 5 (MutBench) — 10인 교수 심사 종합 보고서

**논문:** 다층적 게놈 데이터 분석을 위한 체계적 벤치마킹과 적응형 클러스터링 프레임워크
**저자:** 권휘준 (경북대학교 컴퓨터학부)
**심사 대상:** Chapter 5 — MutBench Framework
**심사 일자:** 2026-03-08

---

## 1. 종합 성적표

| # | 교수 | 전문 분야 | 등급 | 핵심 한 줄 평가 |
|---|------|-----------|------|----------------|
| 1 | Prof. Kim | 바이러스학 | **A-** | 다중 GT와 H-score 포화 발견이 탁월; 계통발생 비독립성 Ch5 내 논의 필요 |
| 2 | Prof. Park | 생물통계학 | **B** | Bootstrap CI가 점추정치를 포함하지 않는 구조적 오류가 치명적 |
| 3 | Prof. Lee | ML/클러스터링 | **B+** | 하이브리드 설계와 ablation 우수; 특성공간 정규화·TC-freq 미정의 |
| 4 | Prof. Choi | 벤치마킹 | **A-** | MOSD→MutBench 전이 탁월; 외부 독립 방법 비교 부재 |
| 5 | Prof. Jung | 구조생물학 | **B+** | GT 선정 타당; 3D 구조 맥락·glycosylation 미반영 |
| 6 | Prof. Yoon | 역학 | **B+** | 공중보건 시사점 있음; GISAID sampling bias·실시간 구현 미논의 |
| 7 | Prof. Han | 학술작문 | **B+** | Five Bridges 서사 우수; 한/영 혼재·CI 오류·방법 미정의 |
| 8 | Prof. Kang | 유전체학 | **B+** | 좌표 처리 정확; entropy gap 처리·nt/AA level 혼재 |
| 9 | Prof. Shin | CS 이론 | **B+** | ablation 체계적; hotspot-score 이론 속성·CCM 형식 보장 부족 |
| 10 | Prof. Wang | 외부심사위원 | **B+** (82/100) | Minor Revision — 자기평가 한계, 합성 데이터 의존 |

**평균 등급: B+ (A-: 2명, B+: 7명, B: 1명)**

---

## 2. 공통 강점 (모든/대부분 심사위원 동의)

### 강점 1: 다중 Ground Truth 평가의 독창성 (10/10 동의)
- Jaccard(DMS, 수렴진화) = 0.006 — 거의 완전 독립
- "population frequency ≠ functional importance" 핵심 발견
- 벤치마킹 분야 전반에 적용 가능한 방법론적 기여

### 강점 2: H-score 포화 현상의 정직한 보고 (9/10 동의)
- 2024-2025 데이터에서 모든 위치 non-zero (mean 8.47, std 0.098)
- 자기 알고리즘의 근본적 한계를 정면 보고 — 학술적 성숙도
- adaptive reference 필요성이라는 향후 연구로 자연 연결

### 강점 3: MOSD→MutBench 벤치마킹 철학 전이 (8/10 동의)
- Five Bridges 구조의 설득력
- cluster-score → hotspot-score 설계 철학 계승
- "연구 설계 > 알고리즘 선택" 발견의 교차 도메인 재현

### 강점 4: 5개 변이체 ablation study의 체계성 (7/10 동의)
- 점진적 구성요소 추가로 각 기여를 독립 측정
- CCM + HDBSCAN 하이브리드의 실증적 정당화
- HDBSCAN 파라미터 비민감성 확인 (F1 변동 < 0.005)

---

## 3. 공통 약점 — 우선순위별 정리

### 🔴 긴급 수정 (Critical) — 모든 심사위원 지적

#### 약점 1: Bootstrap CI 점추정치가 신뢰구간 밖 (10/10 지적)
- MutClust-Hybrid: 점추정치 0.776, 95% CI [0.644, 0.669]
- **통계적으로 불가능** — 모든 방법에서 동일 패턴
- 원인 추정: GT 리샘플링 시 stability 고정, 또는 CI가 개별 구성요소에 대해 계산됨
- **조치:** CI 계산 코드 재검증, BCa bootstrap 고려, 또는 최소한 불일치 원인 명시

#### 약점 2: TC-freq, CH-score 등 방법이 Methods에 미정의 (8/10 지적)
- Table 5.7 (다중 GT)에서 등장하는 방법명이 Section 5.3에서 정의되지 않음
- 5개 변이체(Table 5.2)와의 관계도 불명확
- **조치:** Section 5.3에 이 방법들의 공식 정의 추가, 또는 별도 소절 신설

### 🟡 주요 보완 (Major)

#### 약점 3: 계통발생 비독립성이 Ch5 본문에서 미논의 (6/10 지적)
- D614G founder effect 문제가 Ch6에만 있고 Ch5에는 없음
- H-score는 각 서열을 독립으로 가정하나 실제 계통 구조 존재
- **조치:** Section 5.5 (Discussion)에 1-2 단락 추가

#### 약점 4: 외부 독립 방법과의 비교 부재 (5/10 지적)
- 5개 변이체가 모두 MutClust 변형 — "자기 평가" 한계
- 빈도 기준선·슬라이딩 윈도우는 naive baseline, 경쟁 방법 아님
- **조치:** OncodriveCLUST 등 최소 1개 외부 방법 추가, 또는 프레임워크 범용성 강조

#### 약점 5: hotspot-score 가중치 민감도 분석 부재 (6/10 지적)
- precision/recall/stability에 동일 가중치(1/3)의 이론적 근거 부족
- MOSD 선례만으로는 정당화 불충분 (동질 vs 이질적 구성)
- **조치:** 가중치 변경 시 순위 불변성(rank invariance) 분석 추가

#### 약점 6: 한국어/영어 혼재 문제 (3/10 지적, 작문 전문가 강조)
- Ch5만 한국어, 나머지 영어 — 문체적 통일성 훼손
- **조치:** 전체 한국어 또는 전체 영어로 통일

### 🟢 권장 보완 (Minor)

| # | 약점 | 지적 교수 수 | 조치 |
|---|------|-------------|------|
| 7 | 합성 GT의 순환 편향 (CCM으로 생성, CCM으로 탐지) | 3 | seed 위치 변경 시 강건성 분석 |
| 8 | Shannon entropy gap/ambiguous 문자 처리 미명시 | 2 | Methods에 처리 방식 기술 |
| 9 | nt/AA level 분석 혼재 | 2 | 1,273이 AA인지 nt인지 명확화 |
| 10 | 3D 구조 맥락 미반영 | 2 | Discussion에 한계 인정 |
| 11 | GISAID sampling bias 논의 부족 | 2 | 지리적·임상적 편향 논의 추가 |
| 12 | permutation null model이 과도하게 관대 | 2 | circular/block permutation 고려 |
| 13 | 참고문헌 40여편으로 부족 (80-100편 기대) | 1 | 원논문 참고문헌 통합 |
| 14 | glycosylation/이황화결합 GT 미포함 | 1 | Discussion에 한계 언급 |
| 15 | enrichment ratio 통계적 유의성 미검증 | 1 | Fisher's exact test 추가 |
| 16 | 코드/데이터 공개 URL 미명시 | 1 | GitHub URL 추가 |

---

## 4. 외부심사위원 방어 예상 질문 (Prof. Wang)

1. **"MutBench가 MutClust 변이체만 비교하는 것은 벤치마킹이 아니라 알고리즘 개선 연구 아닌가?"**
   → 프레임워크 범용성(plug-in 구조)과 현재 비교 대상의 제한성을 구분하여 답변

2. **"H-score 포화가 확인되었는데, MutClust의 실용적 수명이 이미 끝난 것 아닌가?"**
   → adaptive reference, TC-freq 접근법의 구체적 가능성 설명

3. **"Five Bridges 중 Bridge 3, 5가 불완전하다면, 통합 서사의 근거로 충분한가?"**
   → 나머지 3개 bridge의 구체적·검증 가능한 연결로 충분함을 논증

---

## 5. 수정 우선순위 로드맵

```
Phase 1 (즉시 수정 — 1-2일):
├── Bootstrap CI 재계산 및 수정
├── TC-freq, CH-score 등 Methods 정의 추가
└── Table 수치 오류 전면 검증

Phase 2 (주요 보완 — 3-5일):
├── 계통발생 비독립성 논의 Ch5 추가
├── hotspot-score 가중치 민감도 분석
├── 언어 통일 (한/영 결정)
└── 외부 방법 1개 이상 추가 비교

Phase 3 (권장 보완 — 1주):
├── enrichment ratio 유의성 검정
├── 참고문헌 확충 (80편 이상)
├── 3D 구조 한계 Discussion 추가
└── 코드/데이터 공개 URL 추가
```

---

## 6. 종합 판정

**현재 상태: B+ (Minor Revision 필요)**

Phase 1 수정만으로도 **B+ → A-** 상승 가능.
Phase 1 + Phase 2 완료 시 **A-** 확보.
전체 Phase 완료 시 **A** 수준 도달 가능.

핵심 메시지: 다중 GT 평가, H-score 포화 발견, MOSD→MutBench 전이라는 **세 가지 독창적 기여는 모든 심사위원이 인정**. Bootstrap CI 오류와 방법 미정의라는 **기술적 결함만 수정하면 학위논문으로서 충분한 수준**.
