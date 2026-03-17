# 전체 A 등급 달성을 위한 교수별 갭 분석 및 수정 계획

## 현재 → 목표

| # | 교수 | 현재 | 목표 | 갭 크기 | 핵심 블로커 |
|---|------|------|------|---------|------------|
| 1 | 바이러스학 | A- | A | 작음 | 계통발생 논의 + DMS 한계 |
| 2 | **생물통계** | **B** | **A** | **큼** | **CI 재설계 + null model 개선** |
| 3 | ML/클러스터링 | B+ | A | 중간 | 정규화 ablation + 방법 정의 |
| 4 | 벤치마킹 | A- | A | 작음 | 외부 방법 1개 + 순환 편향 분석 |
| 5 | 구조생물학 | B+ | A | 중간 | 3D 구조 논의 + glycosylation |
| 6 | 역학 | B+ | A | 중간 | sampling bias + founder effect |
| 7 | 학술작문 | B+ | A | 중간 | 언어 통일 + CI 수정 + 방법 정의 |
| 8 | 유전체학 | B+ | A | 중간 | dN/dS 보정 + nt/AA 명확화 |
| 9 | CS 이론 | B+ | A | 중간 | Hybrid 복잡도 + hotspot-score 형식 분석 |
| 10 | 외부심사 | B+ | A | 중간 | CI 수정 + 외부 방법 + 방법 정의 |

---

## 교수별 구체적 수정 사항

### Prof 1 (바이러스학, A- → A)
**필요 작업 2개:**
1. ✍️ Ch5 Discussion에 **계통발생 비독립성** 1-2 단락 추가
   - D614G founder effect가 H-score에 미치는 영향
   - dN/dS 필터가 부분적으로 완화하나 완전하지 않음을 명시
2. ✍️ DMS 한계 1 단락 추가
   - Wuhan-Hu-1 backbone에서 측정 → epistatic context 차이
   - top-20% threshold 선택의 민감도 간략 논의

### Prof 2 (생물통계, B → A) ⭐ 가장 어려운 교수
**필요 작업 5개:**
1. 🔧 **Bootstrap CI 완전 재설계** (가장 중요)
   - 옵션 A: 입력 데이터 리샘플링 후 재탐지 (gold standard, 비용 높음)
   - 옵션 B: BCa bootstrap + 명확한 리샘플링 대상 기술
   - 옵션 C: CI가 GT 불확실성을 반영함을 명시적으로 설명 + 별도 CI 종류 표기
2. 🔧 **Multiple comparison correction 추가**
   - Bonferroni 또는 Holm correction 적용, 보정 후 p-value 보고
3. 🔧 **Enrichment ratio에 Fisher's exact test 추가**
   - 특히 convergent strict (n=29)에서 3.43x의 유의성 검증
4. 🔧 **Permutation null model 개선**
   - Block permutation 또는 circular permutation으로 공간 구조 보존
5. ✍️ **Hotspot-score 가중치 민감도 분석**
   - 가중치를 (0.2, 0.2, 0.6) ~ (0.4, 0.4, 0.2) 범위에서 변경
   - 순위 불변성(rank invariance) 확인

### Prof 3 (ML/클러스터링, B+ → A)
**필요 작업 3개:**
1. ✍️ **TC-freq, CH-score, Saturated H-score 정의**를 Section 5.3에 추가
   - 각 방법의 수식, 입력, 출력 명시
2. 🔧 **특성공간 정규화 ablation 분석**
   - min-max vs z-score vs 가중치 비율 변경
   - 순위 변동 확인 → robustness 입증
3. ✍️ hotspot-score에서 **F1 대신 (p+r)/2를 사용한 이유** 논의
   - stability 포함이 핵심 차별점임을 강조

### Prof 4 (벤치마킹, A- → A)
**필요 작업 2개:**
1. 🔧 **외부 방법 1개 추가 비교**
   - 가장 현실적: 간단한 sliding window entropy 또는 frequency-threshold의 "enhanced" 버전
   - 또는: OncodriveCLUST의 핵심 로직을 바이러스 게놈에 적응
2. ✍️ **합성 GT seed 위치 변경 시 강건성**
   - 현재 seed (484, 501, 417, 452) 외에 다른 위치로 변경해도 순위 유지되는지

### Prof 5 (구조생물학, B+ → A)
**필요 작업 3개:**
1. ✍️ Discussion에 **3D 구조 한계** 인정 단락 추가
   - 선형 서열 기반 평가의 한계, HotMAPS 같은 3D 접근과의 차이
   - PDB 6VSB 기반 solvent accessibility 분석은 향후 연구로
2. ✍️ **Glycosylation/이황화결합** 한계 언급
   - 22개 N-glycosylation 부위가 정화 선택 하에서 dN/dS 필터에 의해 배제될 수 있음
3. ✍️ **수렴 진화 위치의 구조적 설명** 1-2 문장
   - E484: class II 항체 에피토프 접촉 잔기
   - N501Y: ACE2 Y41과 pi-stacking

### Prof 6 (역학, B+ → A)
**필요 작업 3개:**
1. ✍️ **GISAID sampling bias** 논의 추가
   - 지리적 편향 (고소득국 과대 대표), 시간적 편향
   - 주별 층화가 시간만 보정, 지역/임상 보정 안됨을 명시
2. ✍️ **Founder effect vs positive selection 구분 한계** 논의
   - JN.1 확산에서 L455S는 면역 회피, 파생 계통은 founder effect 가능
   - H-score/TC-freq가 이 둘을 구분 못함을 한계로 명시
3. ✍️ **공중보건 실용성** 논의 강화
   - TC-freq의 시간 윈도우, 경보 역치 설정 등 운용 파라미터 논의
   - 기존 감시 프레임워크(Nextstrain, WHO TAG-VE)와의 관계 언급

### Prof 7 (학술작문, B+ → A)
**필요 작업 3개:**
1. 📝 **언어 통일** — 전체 영어 또는 전체 한국어 결정
   - 경북대 규정상 한국어 논문이면 전체 한국어로 통일
2. ✍️ TC-freq 등 **방법 미정의 문제 해결** (Prof 3과 동일)
3. ✍️ **5.2절(관련 연구) 확장** + 5.5절 중복 제거
   - 결과와 논의 간 반복 서술 축소

### Prof 8 (유전체학, B+ → A)
**필요 작업 3개:**
1. ✍️ **dN/dS 계산 방법론 상세화**
   - Nei-Gojobori 또는 Li-Wu-Luo 부위 수 보정 사용 여부 명시
   - 짧은 클러스터에서의 통계적 불확실성 언급
2. ✍️ **nt vs AA 수준 명확화**
   - "1,273개 위치"가 AA임을 명시, wobble position 영향 논의
   - nt 수준 선택 근거 (비코딩 영역 포함 가능성)
3. ✍️ **indel 처리 전략** Methods에 명시
   - ins214EPE, 69-70 결실 등의 처리 방법

### Prof 9 (CS 이론, B+ → A)
**필요 작업 3개:**
1. ✍️ **MutClust-Hybrid 복잡도 분석** 추가
   - CCM seeding O(M log M) + HDBSCAN O(k log k), k = CCM 후보 수
   - k << M이므로 전체 O(N + M log M)에 지배됨을 논증
2. ✍️ **Hotspot-score 형식적 성질** (최소 보조정리 수준)
   - Boundedness: [0, 1]
   - Monotonicity: 각 구성요소에 단조증가
   - 가중치 민감도 분석으로 rank invariance 입증
3. ✍️ **Bug fix closed-form 분석** 추가
   - 누적 감쇠의 점화식 해석, 선형 감쇠 대비 종료 시점 비율

### Prof 10 (외부심사, B+ → A)
**필요 작업 3개:**
1. 🔧 Bootstrap CI 수정 (Prof 2와 동일)
2. ✍️ TC-freq 등 방법 정의 (Prof 3과 동일)
3. 🔧 외부 방법 추가 또는 프레임워크 범용성 명시적 증명

---

## 작업 통합 — 중복 제거 후 실제 작업 목록

### 🔧 코드/실험 작업 (6개)

| # | 작업 | 영향 교수 | 난이도 | 소요시간 |
|---|------|----------|--------|---------|
| C1 | Bootstrap CI 재설계 및 재계산 | 전원(10) | ⭐⭐⭐ | 4-6h |
| C2 | Hotspot-score 가중치 민감도 분석 | 2,3,9,10 | ⭐⭐ | 2-3h |
| C3 | Enrichment ratio Fisher's exact test | 2 | ⭐ | 1h |
| C4 | Permutation null model 개선 (block) | 2 | ⭐⭐ | 2-3h |
| C5 | 특성공간 정규화 ablation | 3 | ⭐⭐ | 2-3h |
| C6 | 외부 방법 1개 구현 및 비교 | 4,10 | ⭐⭐⭐ | 4-6h |

### ✍️ 논문 집필 작업 (10개)

| # | 작업 | 영향 교수 | 분량 |
|---|------|----------|------|
| W1 | TC-freq, CH-score, Saturated H-score 정의 (5.3절) | 3,7,9,10 | ~2p |
| W2 | 계통발생 비독립성 논의 (5.5절) | 1,6,8 | ~1p |
| W3 | DMS 한계 논의 (epistatic context, threshold) | 1 | ~0.5p |
| W4 | 3D 구조 한계 + glycosylation/수렴진화 구조 설명 | 5 | ~1p |
| W5 | GISAID sampling bias + founder effect | 6 | ~1p |
| W6 | dN/dS 방법론 상세 + nt/AA 명확화 + indel | 8 | ~1p |
| W7 | Hybrid 복잡도 + hotspot-score 형식 성질 | 9 | ~1.5p |
| W8 | 공중보건 실용성 (TC-freq 운용 파라미터) | 6 | ~0.5p |
| W9 | 5.2절 확장 + 5.5절 중복 제거 | 7 | ~1p |
| W10 | 언어 통일 (전체 한국어 또는 전체 영어) | 7 | ~전체 |

---

## 실행 순서 (최적 경로)

```
Day 1: [코드] C1 (Bootstrap CI 재설계) — 가장 큰 임팩트
Day 1: [코드] C2 (가중치 민감도) — C1과 병렬 가능
Day 1: [집필] W1 (방법 정의 추가) — 가장 많은 교수 영향

Day 2: [코드] C3 (Fisher's exact) + C4 (Block permutation)
Day 2: [집필] W2 (계통발생) + W3 (DMS) + W5 (sampling bias)

Day 3: [코드] C5 (정규화 ablation)
Day 3: [집필] W4 (구조 한계) + W6 (dN/dS) + W7 (복잡도/형식 분석)

Day 4: [코드] C6 (외부 방법 구현)
Day 4: [집필] W8 (공중보건) + W9 (절 균형)

Day 5: [집필] W10 (언어 통일) — 가장 시간 소요
Day 5: 전체 리뷰 + 참고문헌 확충
```

### 예상 결과

| Day | 완료 작업 | Prof 2 | 기타 교수 |
|-----|----------|--------|----------|
| Day 1 | C1+C2+W1 | B → B+ | 대부분 B+ → A- |
| Day 2 | C3+C4+W2+W3+W5 | B+ → A- | A- → A |
| Day 3 | C5+W4+W6+W7 | A- | 나머지 → A |
| Day 4 | C6+W8+W9 | A- → A | A 확보 |
| Day 5 | W10 + 마무리 | A | **전원 A** |

---

## 핵심 메시지

**전체 A를 받으려면 필수 3대 작업:**
1. 🔧 **Bootstrap CI 재설계** — 이것만 해도 B→B+, 나머지 A- 가능
2. ✍️ **TC-freq 등 방법 정의 추가** — 8명 교수에게 영향
3. 🔧 **가중치 민감도 분석** — hotspot-score 정당화의 핵심

**가장 어려운 교수:** Prof 2 (통계) — CI 재설계 + null model + Fisher's test + correction 모두 필요
**가장 쉬운 교수:** Prof 1 (바이러스학) — Discussion에 2 단락만 추가하면 A- → A
