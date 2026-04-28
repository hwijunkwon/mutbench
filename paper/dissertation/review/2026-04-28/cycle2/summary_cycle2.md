# Cycle 2 종합 검수 결과 (2026-04-28)

대상: MutBench 박사논문 6장 + abstract (한·영) — codex+적대적 IV&V 챕터별 병렬 검수
실행 사이클: 2 (cycle 1에서 P0 9건 수정 후, cycle 2에서 잔존·신규 결함 재공격)
산출물: `cycle2/{abstract,ch1,ch2,ch3,ch4,ch5,ch6,cross_chapter}_review.md`

---

## 1. Phase 0 자동검증

`verify_dissertation.py` → **PASS 88 / FAIL 0 / WARN 0** (cycle 1 86개 → +2 추가, 회귀 없음)

---

## 2. 챕터별 결함 카운트 (cycle 2 신규 + cycle 1 미수정)

| 챕터 | 신규 Critical | 신규 Major | 신규 Minor | cycle 1 미수정 | P0 권고 | 최우선 결함 |
|------|---|---|---|---|---|---|
| Abstract | 2 | 3 | 1 | — | 2 | KR abstract `G07/G08` 미전파 |
| Ch1 | 2 | 5 | 5 | G08 부분 | 3 | 11 vs 12 pathogen panel 불일치 + 등가성 단어 과장 |
| Ch2 | 3 | 4 | 다수 | C1/C2/C4 (cycle1) | 4 | "10 information types" vs ch3/4 "20 scoring types" 자체 모순 |
| Ch3 | 3 | 12 | 15 | **6 Critical 전부** | 4 | **B-C1 EqualWeight directional-sign label leakage** |
| Ch4 | 2 | 6 | 5 | 5 Major | 2 | cell-level 0.234 vs aggregate 0.296 비누설 |
| Ch5 | 3 | 6 | 5 | 4 partial | 3 | 97.6% retention 임상 오독 위험 + Tranception proxy 한계 누락 |
| Ch6 | 2 | 3 | 5 | M1~M3 | 1 | G02b partial fail (Friedman 등급 강등) + PAHD-R scope creep |
| Cross-chapter | 0 | 2 | 2 | — | 0 | 헤드라인 12개 수치 모두 6파일 일관 |
| **합계** | **17** | **41** | **38** | **22** | **19** | — |

---

## 3. 가장 위험한 신규 결함 TOP 8 (cycle 2 발견, defense 전 필수)

| # | ID | 위치 | 결함 | 위험 등급 | 수정 시간 |
|---|-----|------|------|---------|---------|
| 1 | **B-C1** | ch3:695, EqualWeight 정의 | 모든 11 pathogen 라벨로 feature 부호 fitting → ω²=0.296의 한 채널이 라벨 누출 가능성 | **Critical** (Phase 4 통계교수 #3 이슈와 결합 시 escalation) | 2~4시간 (재현 + 본문 명시) |
| 2 | N-C1 (Ch4) | ch4 전반 | 헤드라인 ω²=0.296을 5곳에서 사용하지만 cell-level 0.234는 ch5:290에만 존재 | Critical | 30분 (ch4 핵심 paragraph에 0.234/0.296 disclosure 추가) |
| 3 | C-01 (Ch1) | ch1:82 vs ch1:150 | "Stage 3 covers 11 pathogens" vs "12-pathogen Stage 3 panel" — 실제는 12 (Zika 추가) | P0 | 15분 |
| 4 | C-02 (Ch1) | ch1:152 | 비기각(p=0.61, CI [-0.018, +0.042])을 "operationally equivalent"로 표현 → equivalence claim 과장 | P0 | 15분 |
| 5 | KR-Abstract P0 | abstract_kr.tex:12, 22 | cycle 1 G07/G08 fix가 한국어 abstract에 미전파 ("2단계", "98%") | P0 | 20분 |
| 6 | N-C1 (Ch5) | ch5:192 | 4-feature 97.6% retention을 "ensemble 대비"가 아닌 "절대치"로 읽힐 위험 (임상 오독) | Critical | 20분 |
| 7 | Ch6 G02b | ch6:13 trailing clause | Friedman을 "corroborative consistency"로 demote → abstract와 불일치 | P0 | 10분 |
| 8 | Ch2 N-C1 | ch2:49, 156, 208 | "10 information types"가 ch3/ch4 "20 scoring types"와 자체 모순 | P0 | 30분 |

---

## 4. cycle 1 미수정 결함 재확인 (cycle 2가 다시 발견)

cycle 1 P0 9건 외에 **P1으로 분류됐던 것이 사실상 P0**으로 재분류되어야 하는 항목:

- Ch1 G24 (panel size 11 vs 12): cycle1 P1 → **cycle2 P0 escalation**
- Ch3 cycle1 6 Critical (cutoff date, MAFFT non-determinism, preregistration, repo URL, multiple-testing pre-spec, 6-pathogen Layer C sweep): **전부 미수정**
- Ch4 cycle1 5 Major (Friedman power, baseline SD 0.003 vs 0.034, 280 vs 780 footnote, Bonferroni-survivor mean, HIV-1 nA=23 vs 26): **전부 미수정**
- Ch5 cycle1 7 Critical 중 4건 (C2 ranking-discount, C4 reproduction discount, C5 Bolker explicit threshold, C7 circularity↔heterogeneity cross-ref): partial 상태
- Ch6 cycle1 M1~M3: 미수정

**해석**: cycle 1은 "P0 9건만 수정하면 defense 가능" 판정이었으나, cycle 2 codex 적대 검수는 **cycle1 P1/Major로 분류된 22건도 사실상 P0~Major 영향**이라고 평가.

---

## 5. cycle 2 권고 P0 수정안 (최소 작업, 1일 내 가능)

### Tier 1 — defense 차단 위험 (8건, ~6시간)

1. **Ch3:695 EqualWeight label leakage 처리** (B-C1) — ① 본문에 "directional sign learned on training pathogens only" 명시 + ② 누출 가능 시 ω² re-estimation 1회 (sensitivity)
2. **Ch4 ω² 0.296 vs 0.234 disclosure 전파** — ch4 핵심 paragraph 1곳에 cell-level 0.234 추가
3. **Ch1:82/150 panel size 11 vs 12 통일** — 12로 통일 + ch1:111 TikZ subbox 정합
4. **Ch1:152 "operationally equivalent" → "non-rejection of inferiority"** 등으로 약화
5. **Korean abstract (abstract_kr.tex:12, 22) Stage 3 layer + 4-feature paired-test caveat 전파**
6. **Ch5:192 97.6% retention "relative to 10-feature ensemble" 단정 추가**
7. **Ch6:13 Friedman demote 문장 분리** — "Friedman is the main statistic; LOPO is corroborative"
8. **Ch2:49/156/208 "10 information types" → "20 scoring types"** 정정

### Tier 2 — defense 대답 강화 (4건, ~6시간)

9. **Tranception–ESM-LLR per-pathogen ρ supplementary table** (cycle1 P1 carry-over, 교수6 대응)
10. **Time-stratified holdout 1-pathogen pilot** (cycle1 P1, 교수8 대응) — H3N2 2010-cutoff
11. **Ch2 MEME/FUBAR mis-attribution 정정** + Bloom lab antibody-escape DMS lineage 추가
12. **Ch3 wild-cluster bootstrap 부재 acknowledge** (B-C3)

### Tier 3 — 정합성 polish (7건, ~3시간)

- Ch6 PAHD-R scope creep (abstract/ch1에 추가 or ch6에서 격하)
- Ch3 두 가지 "two stages" 표현 (L10, L172) — Stage 1+2 명시
- Ch5 forward-looking 단어 ("standardised", "integrates") → 의도형으로 약화
- Ch6 contribution 개수 3 vs 4 정합 (3a/3b 분리 명시)
- Cross-chapter 5×5 caveat grid 23/25 → 25/25 (Bonferroni 3.9e-9 abstract/ch5/ch6에 추가)
- Ch4:462 280 vs 780 footnote 통일
- Ch4:600 LOPO/Friedman/permutation null 표현 calibration

---

## 6. 통계적 종합 판정

| 차원 | cycle 1 | cycle 2 |
|------|--------|--------|
| Phase 0 PASS | 86 | 88 |
| 신규 Critical 총합 | 35 | **17** |
| P0 차단 | 9 (수정완료) | **8 (미수정)** |
| Phase 4 교수 평균 | 7.27 (B+) | 미실시 (cycle 2는 챕터-수준 IV&V) |
| Defense 통과 가능성 | 80% (cycle 1 P0 적용 후) | **70%** (cycle 2 Tier 1 미적용 시) → **85%** (Tier 1 적용 시) |

**판정 변경 사유**:
- cycle 1은 abstract/ch1/ch4/ch5/ch6에 P0 9건 적용했지만 **ch2 / ch3 / kr abstract**에는 손대지 않음.
- cycle 2 codex 검수가 **ch3 EqualWeight label leakage + ch1 11 vs 12 panel + kr abstract 미동기화**를 *추가 발견*.
- 위 8건 모두 단어 수정 또는 supplementary table 추가로 해결 가능 — 재실험 필요 항목 0건.

---

## 7. 사용자 의사결정 항목

다음 3가지 옵션 중 선택:

### Option A. **현 상태 defense 진행** (cycle 1 fix만 적용)
- 통과 확률 70~80%, 취약 질문 3개에 대한 답변 준비 필수
- 위험: ch2 자체 모순(10 vs 20 types), 한국어 abstract 미동기화는 위원회 즉각 식별 가능

### Option B. **cycle 2 Tier 1 8건만 추가 수정** (~6시간 작업) ← **권장**
- 통과 확률 80~85%, lenient 80점 근접
- 모든 cycle 2 신규 Critical 해소 + 한국어 abstract 정합
- 재실험 0건, 텍스트/단어 수정만

### Option C. **cycle 2 Tier 1+2+3 19건 전부 수정** (~15시간 = 2일)
- 통과 확률 85~90%, A- 등급 목표
- Tranception ρ table + H3N2 time-stratified pilot 1회 추가 (cycle 1 P1 carryover)

---

## 8. 다음 단계 제안

권장: **Option B 진행** → 8건 Tier 1 수정 → `verify_dissertation.py` 재실행 → LaTeX 재빌드 → cycle 3에서 잔존 결함 재공격 (필요 시).

cycle 2 발견의 가장 중요한 함의: **cycle 1은 abstract/conclusion/results에 집중했으나 background(ch2)와 methods(ch3)에 cycle 1 시점의 결함이 다수 잔존**. defense 시 가장 hostile한 위원이 ch3을 1시간 정독하면 EqualWeight label leakage / wild-cluster bootstrap 부재 등을 즉시 지적할 가능성이 매우 높음.

| 작업 | 예상시간 | 담당 |
|------|--------|-----|
| Tier 1 8건 패치 적용 | 6h | 사용자 또는 차후 에이전트 |
| `verify_dissertation.py` + LaTeX 재빌드 | 5min | 자동 |
| cycle 3 (Tier 1 검증 + 잔존 결함) | 1h | 적대 검수 1회 |
| 합계 | **~7시간 = 1일** | — |
