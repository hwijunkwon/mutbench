# Stage 3 구조조정 및 신규 실험 계획

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 10가지 정보 유형을 scoring으로 사용한 대규모 벤치마크 실험을 수행하고, 관련 연구의 핫스팟 탐지 전문 방법을 포함하여, 논문의 Stage 3을 실험적으로 완성한다.

**Architecture:** 기존 `run_extended_benchmark.py`의 scoring formula를 10가지 정보 유형 기반으로 확장하고, EVEscape/Hie/MutClust 등 기존 문헌의 방법을 baseline으로 추가. 12개 병원체에 대해 전체 벤치마크를 재실행하여 "정보 유형 × 탐지 알고리즘 × 병원체" 3차원 분석을 완성.

**Tech Stack:** Python, NumPy, scikit-learn, BioPython, ESM-2 (fair-esm), existing MutBench pipeline

---

## 현황 분석

### 현재 실험 구조
```
Stage 2: 9 scoring (빈도/엔트로피 기반) × 14 algorithms × 9 pathogens = 3,159 evaluations
Stage 3: 10 features × 12 pathogens = per-feature AUC만 (탐지 알고리즘 미적용)
```

### 문제점
1. Stage 2의 9 scoring이 전부 빈도/엔트로피 변형 → 좁은 범위
2. Stage 3이 AUC 분석만 하고 실제 탐지 파이프라인에 넣지 않음
3. 관련 연구의 전문 방법(EVEscape, dN/dS 기반, phylogenetic 등)이 baseline으로 포함되지 않음

### 필요한 실험
```
신규: 10 information-type scoring × 14 algorithms × 12 pathogens = 1,680 evaluations
      + 문헌 기반 전문 방법 baseline 비교
```

---

## Phase 1: 신규 Scoring Formula 구현 (10가지 정보 유형)

### Task 1: 10가지 정보 유형 scoring formula 추가

**Files:**
- Modify: `/proj/paper/scripts/run_extended_benchmark.py` (compute_scores 함수 확장)
- Create: `/proj/paper/scripts/compute_info_type_scores.py` (독립 스크립트)

기존 9개 scoring (빈도/엔트로피 기반):
```
E*rare, P*E*rare, minority_E, P*minority_E, P*E, H-score, E_only, P*E^2, rank(P*E)
```

추가할 10개 information-type scoring:
```
1. freq_only        — 변이 빈도 단독
2. entropy_only     — Shannon 엔트로피 단독 (기존 E_only와 동일, 확인)
3. rare_only        — 희귀 변이 비율 단독
4. homoplasy_score  — Fitch parsimony homoplasy count (이미 계산됨)
5. esm2_llr         — ESM-2 log-likelihood ratio (이미 계산됨)
6. plddt_inv        — 1 - pLDDT/100 (낮은 pLDDT = 높은 점수, 유연한 영역)
7. sasa_score       — RSA (이미 계산됨)
8. grantham_score   — Grantham distance (이미 계산됨)
9. dnds_proxy       — dN/dS proxy (이미 계산됨)
10. semantic_score  — semantic change (이미 계산됨)
```

데이터 소스: `/proj/paper/results/mutbench/feature_analysis/feature_matrix_{pathogen}.csv`

- [ ] Step 1: feature matrix에서 10가지 scoring array를 로드하는 함수 작성
- [ ] Step 2: 기존 파이프라인의 14개 detector에 넣을 수 있도록 scoring array 포맷 통일
- [ ] Step 3: 테스트 — SARS-CoV-2에서 homoplasy_score + Wavelet(t=1.5) 조합으로 MCC 계산 확인
- [ ] Step 4: 커밋

---

## Phase 2: 문헌 기반 전문 방법 Baseline 추가

### Task 2: 관련 연구 방법 구현

**Files:**
- Create: `/proj/paper/scripts/literature_baselines.py`

관련 연구에서 실제로 핫스팟/변이 예측에 사용된 방법들:

| 방법 | 출처 | 사용하는 정보 | 구현 방식 |
|------|------|-------------|----------|
| **EVEscape-like** | Thadani 2023, Nature | fitness + accessibility + dissimilarity | esm2_llr × sasa × grantham 조합 |
| **Hie-like** | Hie 2021, Science | grammaticality + semantic change | esm2_llr + semantic_change 조합 |
| **dN/dS threshold** | 표준 진화생물학 | dN/dS > 1 = positive selection | dnds_proxy 임계값 |
| **Phylo-convergent** | ConDor, Fitch | homoplasy count | homoplasy_score 임계값 |
| **Structure-surface** | 구조 기반 연구 | SASA + pLDDT | sasa × (1-pLDDT) 조합 |
| **Multi-feature RF** | 본 연구 EqualWeight | 10 features equal weight | z-score 합산 (이미 구현) |

- [ ] Step 1: 6개 문헌 기반 방법을 scoring function으로 구현
- [ ] Step 2: 각 방법에 대해 FreqThresh(top-5%, 10%)로 탐지하여 MCC 계산
- [ ] Step 3: 테스트 — 12개 병원체에서 모두 실행 확인
- [ ] Step 4: 커밋

---

## Phase 3: 대규모 벤치마크 실행

### Task 3: 10-scoring × 14-algorithm × 12-pathogen 벤치마크

**Files:**
- Create: `/proj/paper/scripts/run_stage3_benchmark.py`
- Output: `/proj/paper/results/mutbench/stage3_results.csv`

```
10 info-type scoring × 14 algorithms (39 variants) × 12 pathogens
= 10 × 39 × 12 = 4,680 evaluations
```

기존 Stage 2 (9 scoring × 39 × 9 = 3,159)과 합치면 총 7,839 evaluations.

- [ ] Step 1: 12개 병원체의 feature matrix 로드 + 10 scoring 계산
- [ ] Step 2: 각 scoring을 14개 detector family (39 variants)에 입력하여 탐지 수행
- [ ] Step 3: Layer A ground truth 대비 MCC 계산
- [ ] Step 4: 결과를 stage3_results.csv에 저장
- [ ] Step 5: 커밋

### Task 4: 문헌 기반 baseline 벤치마크

**Files:**
- Output: `/proj/paper/results/mutbench/literature_baseline_results.csv`

- [ ] Step 1: 6개 문헌 방법 × 12 병원체 실행
- [ ] Step 2: 결과 저장
- [ ] Step 3: 커밋

---

## Phase 4: 통계 분석

### Task 5: Stage 3 ANOVA + Friedman + LOPO

**Files:**
- Create: `/proj/paper/scripts/analyze_stage3_stats.py`
- Output: `/proj/paper/results/mutbench/stage3_anova.csv`, `stage3_friedman.csv`, `stage3_lopo.csv`

핵심 질문:
1. **ANOVA**: 정보 유형 × 병원체 interaction이 Stage 2의 ω²=0.285보다 큰가?
2. **Friedman**: 정보 유형 간 순위가 병원체마다 유의하게 다른가?
3. **LOPO**: 한 병원체의 최적 정보-알고리즘 조합이 다른 병원체에 적용 가능한가?
4. **비교**: 문헌 기반 방법 vs 단일 정보 vs EqualWeight

- [ ] Step 1: 3-way ANOVA (scoring_type × detection_family × pathogen)
- [ ] Step 2: Friedman test
- [ ] Step 3: LOPO cross-validation
- [ ] Step 4: 문헌 방법 vs 기존 방법 비교표
- [ ] Step 5: 커밋

---

## Phase 5: 논문 구조조정

### Task 6: Ch4 재구성 (3-stage 구조)

**Files:**
- Modify: `/proj/paper/paper/dissertation/chapters_en/ch4_results.tex`

```
4.1 Stage 1: SARS-CoV-2 심층 분석 [현행 유지, 약간 압축]
4.2 Stage 2: 기존 방법 벤치마크 [현행 유지, 서사 수정]
    → "기존 빈도/엔트로피 기반 방법의 한계를 드러내는 단계"로 재프레이밍
4.3 Stage 3: 정보 유형 벤치마크 [신규 — 핵심 결과]
    4.3.1 10가지 정보 유형 × 14 알고리즘 × 12 병원체 결과
    4.3.2 문헌 기반 전문 방법 비교
    4.3.3 정보 유형별 ANOVA/Friedman/LOPO
    4.3.4 Feature Ablation
    4.3.5 GT Heterogeneity
    4.3.6 Vaccine Escape Validation
    4.3.7 Summary: "알고리즘보다 정보가 중요하다"
```

- [ ] Step 1: Stage 2 서사를 "기존 방법의 한계를 드러내는 단계"로 수정
- [ ] Step 2: Ch5(현 info analysis)를 Ch4 Section 4.3으로 이동
- [ ] Step 3: Stage 3 신규 실험 결과 삽입 (표, 그림)
- [ ] Step 4: 문헌 방법 비교 결과 삽입
- [ ] Step 5: 커밋

### Task 7: Ch5(현 info analysis) 삭제, Ch1/Ch6/Ch7 수정

**Files:**
- Delete: `/proj/paper/paper/dissertation/chapters_en/ch5_adapt.tex` (Ch4로 흡수)
- Modify: `/proj/paper/paper/dissertation/thesis_en.tex` (챕터 구성)
- Modify: `/proj/paper/paper/dissertation/chapters_en/ch1_introduction.tex`
- Modify: `/proj/paper/paper/dissertation/chapters_en/ch6_conclusion.tex`
- Modify: `/proj/paper/paper/dissertation/front_en/abstract.tex`
- Modify: `/proj/paper/paper/dissertation/front/abstract_kr.tex`

- [ ] Step 1: thesis_en.tex에서 ch5_adapt 제거, 챕터 번호 조정
- [ ] Step 2: Ch1 기여/목적/구성 수정
- [ ] Step 3: 결론 수정
- [ ] Step 4: 영문/한국어 초록 수정
- [ ] Step 5: 커밋

### Task 8: 그림 생성

**Files:**
- Create: `/proj/paper/scripts/generate_stage3_figures.py`

필요한 그림:
1. Stage 3 ANOVA 분산 분해 (Stage 2와 비교)
2. 정보 유형 × 알고리즘 히트맵 (12개 병원체별)
3. 문헌 방법 vs 기존 방법 비교 bar chart
4. 정보 유형별 best pathogen 매핑

- [ ] Step 1: 4개 그림 생성
- [ ] Step 2: Ch4에 삽입
- [ ] Step 3: 커밋

---

## Phase 6: 요약본 및 최종 검수

### Task 9: 요약본 전면 갱신

**Files:**
- Modify: `/proj/paper/paper/dissertation/dissertation_easy_guide.md`
- Modify: `/proj/paper/paper/dissertation/dissertation_summary.md`

- [ ] Step 1: 3-stage 실험 구조 반영
- [ ] Step 2: 문헌 방법 비교 결과 추가
- [ ] Step 3: Stage 3 핵심 수치 반영
- [ ] Step 4: PDF 재생성
- [ ] Step 5: 커밋

### Task 10: 최종 마감 검수

- [ ] Step 1: 수치 일관성 (모든 파일)
- [ ] Step 2: 참조 무결성 (undefined 0건)
- [ ] Step 3: 한국어 동기화
- [ ] Step 4: digital + print 빌드
- [ ] Step 5: 교수 평가

---

## 예상 일정

| Phase | 작업 | 예상 소요 |
|-------|------|----------|
| 1 | 10 scoring 구현 | 1시간 |
| 2 | 문헌 baseline 구현 | 2시간 |
| 3 | 대규모 벤치마크 실행 | 3-4시간 (ESM-2 GPU) |
| 4 | 통계 분석 | 1시간 |
| 5 | 논문 구조조정 | 3-4시간 |
| 6 | 요약본 + 검수 | 2시간 |
| **합계** | | **12-14시간** |

## 핵심 리스크

| 리스크 | 심각도 | 완화 |
|--------|--------|------|
| Stage 3 ANOVA에서 정보 유형 interaction이 Stage 2보다 작으면? | 높음 | 그래도 "정보 유형별 최적 병원체가 다르다"는 per-feature AUC로 이미 확인됨 |
| 문헌 방법이 기존 방법보다 훨씬 우수하면? | 중간 | 오히려 좋은 결과 — "이런 방법이 더 좋다"를 보여주는 것 |
| 3개 신규 병원체(Zika 52개)에서 결과 불안정 | 낮음 | Zika 제외하고 11개로 분석 가능 |
