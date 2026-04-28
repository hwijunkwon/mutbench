# Abstract fix 적용 보고서

생성일: 2026-04-28
적용자: Abstract fix agent (cycle 2)
대상 파일:
- `/proj/paper/paper/dissertation/front_en/abstract.tex`
- `/proj/paper/paper/dissertation/front/abstract_kr.tex`
근거 매트릭스: `review/2026-04-28/cycle2/integrated_fix_matrix.md` §2 + cross_chapter §G
근거 리뷰: `review/2026-04-28/cycle2/abstract_review.md` §E (E1~E6)

---

## 1. 영어 abstract 수정 (Tier 2 P1/P2 추가, Cycle-1 G07/G08은 이미 LANDED — 보존)

### A-P1-4 (abstract.tex:2) — Retrospective caveat 추가
**Before**:
> ...as the primary external anchor.

**After**:
> ...as the primary external anchor (retrospective enrichment; no prospective time-forward validation).

**근거**: abstract_review E4, integrated_fix_matrix A-P1-4. Defense Q2 (epi practitioner: "no prospective?") 차단.

### A-P1-5 (abstract.tex:11) — Novel-only Bonferroni 3.9e-9 명시
**Before**:
> ...$7.16\text{--}8.24\times$ on the 37 Layer-A-disjoint positions (worst-case $p = 5 \times 10^{-12}$); H3N2...

**After**:
> ...$7.16\text{--}8.24\times$ on the 37 Layer-A-disjoint positions (worst-case $p = 5 \times 10^{-12}$; Bonferroni $p_{\text{adj}} \approx 3.9 \times 10^{-9}$ across 780 combinations); H3N2...

**근거**: cross_chapter_review §G P1, integrated_fix_matrix A-P1-5. abstract:11 / ch1:150 / ch6:15 cross-chapter 일관 (cross-chapter §9.5).

### A-P1-6 (abstract.tex:13) — Tranception/ESM-2 collinearity caveat
**Before**:
> ...reveals 9 distinct optimal information types across 11 pathogens: FUBAR...

**After**:
> ...reveals 9 distinct optimal information types across 11 pathogens (Tranception/ESM-2 channel collinearity is not separated at headline granularity; see Chapter~\ref{ch:mutbench}): FUBAR...

**근거**: abstract_review E5, integrated_fix_matrix A-P1-6, defense Q1 (TOP-1 risk) 차단. cross-chapter §9.7과 정합.

### A-P2-7 (abstract.tex:11) — Validation scope clarification
**Before**:
> ...Validation is restricted to 3/11 pathogens (2{,}340 evaluations) by availability of curated antibody-escape annotations.

**After**:
> ...Validation is restricted to 3/11 pathogens (2{,}340 evaluations) by curated antibody-escape annotation availability --- not by panel design.

**근거**: abstract_review E6. "panel design 한계가 아닌 데이터 가용성 제약" 명시 (committee 오해 차단).

### Cycle-1 G07/G08 (검증만, 수정 없음)
- abstract.tex:8 `two-stage main + Stage~3 information-integration layer` — LANDED 그대로 유지
- abstract.tex:11 / abstract.tex:14 4-feature paired-test caveat (paired Δ +0.011, CI [-0.018, +0.042], p=0.61) — LANDED 그대로 유지

---

## 2. 한국어 abstract 수정 (Cycle-1 G07/G08 한국어 전파 + 의미 동기화)

### A-P0-1 (abstract_kr.tex:12) — G08 한국어 전파 (Stage 3 layer 명시)
**Before**:
> (3) Stage~1에서 SARS-CoV-2에 대한 심층 분석, Stage~2에서 대규모 교차 병원체 비교를 수행하는 2단계 실험 설계이다.

**After**:
> (3) Stage~1에서 SARS-CoV-2에 대한 심층 분석, Stage~2에서 대규모 교차 병원체 비교를 수행하는 2단계 주 실험 설계와, 다중 정보원 통합을 평가하는 Stage~3 정보 통합 레이어로 구성된다.

**근거**: integrated_fix_matrix A-P0-1, abstract_review E1. **P0 등급** — Cycle-1 G08 fix가 영어 abstract에는 LANDED됐으나 한국어에는 propagate되지 않았음. 한국 위원회가 즉시 발견할 수 있는 모순.

### A-P0-2 (abstract_kr.tex:22) — G07 한국어 전파 (4-feature paired-test caveat)
**Before**:
> 다중 정보 통합이 실험적 탐색 범위를 축소하며(H3N2 백신 escape enrichment 4.012배, $p = 0.0023$), 4개 핵심 특징(homoplasy, pLDDT, entropy, frequency)이 전체 앙상블 성능의 98\%를 달성하였다.

**After**:
> 다중 정보 통합이 실험적 탐색 범위를 축소하며(H3N2 백신 escape enrichment 4.012배, $p = 0.0023$), 4개 핵심 특징(homoplasy, pLDDT, entropy, frequency)이 nested-LOPO 하에서 10-feature 앙상블과 운영적으로 동등하다(paired Δ $+0.011$ MCC, 95\% CI [$-0.018$, $+0.042$], 부호 치환 $p = 0.61$).

**근거**: integrated_fix_matrix A-P0-2, abstract_review E2. **P0 등급** — Cycle-1 G07이 retire한 "98% 달성" 표현이 한국어에 잔존. paired-test caveat (Δ +0.011, CI [-0.018, +0.042], p=0.61)로 demote.

### A-P1-3 (abstract_kr.tex:19) — HIV-1 7.16-8.24× novel-only band 추가
**Before**:
> 실용적 검증 측면에서, 병원체 최적화된 단일 scoring이 HIV-1에 대해 7.19배 백신 escape enrichment(...)를 달성하여 가장 정직한 외부 검증 근거로 기능한다. 헤드라인 H3N2 9.36배는...

**After**:
> 실용적 검증 측면에서, 병원체 최적화된 단일 scoring이 HIV-1에 대해 7.19배 백신 escape enrichment(...)를 달성하여 가장 정직한 외부 검증 근거로 기능한다(이는 retrospective enrichment이며 prospective 시간 전향 검증은 수행되지 않았다). 특히 Layer~A-disjoint 37개 위치 novel-only 검증에서 7.16--8.24배 enrichment(worst-case Fisher $p = 5 \times 10^{-12}$; 780 조합 Bonferroni 보정 후 $p_{\text{adj}} \approx 3.9 \times 10^{-9}$)가 관찰되어, primary external anchor 역할을 한다. 헤드라인 H3N2 9.36배는...

**근거**: integrated_fix_matrix A-P1-3, abstract_review E3. 영어 abstract:11에 있는 핵심 외부 검증 anchor가 한국어에 부재했던 결함 해소. retrospective caveat (A-P1-4의 한국어 mirror)도 동일 위치에 통합.

### A-P1-6 (abstract_kr.tex:21) — Tranception/ESM-2 caveat 한국어 전파
**Before**:
> 6개 정보 카테고리(...)에 걸친 20개 점수화 유형 분석에서 11개 병원체에 걸쳐 9가지 서로 다른 최적 정보 유형이 관찰되었다: FUBAR...

**After**:
> 6개 정보 카테고리(...)에 걸친 20개 점수화 유형 분석에서 11개 병원체에 걸쳐 9가지 서로 다른 최적 정보 유형이 관찰되었다(Tranception/ESM-2 채널 공선성은 헤드라인 단위에서 분리되지 않음, Chapter~\ref{ch:mutbench} 참조): FUBAR...

**근거**: integrated_fix_matrix A-P1-6, abstract_review E5. 영어 abstract A-P1-6의 mirror.

---

## 3. 한·영 sync 확인 (10개 핵심 수치)

| # | 수치 | 영어 (EN) 등장 횟수 | 한국어 (KR) 등장 횟수 | sync |
|---|------|--------------------|----------------------|------|
| 1 | 8,580 (`8{,}580`) | 2 | 1 | OK (EN intro+expanded; KR consolidated) |
| 2 | 0.296 (ω²_scoring×pathogen) | 2 | 1 | OK (EN headline+stage2; KR consolidated) |
| 3 | [0.195, 0.333] (CI) | 2 | 1 | OK |
| 4 | 0.103 (6-cat lower bound) | 1 | 1 | OK |
| 5 | 0.265 (oracle gap) | 1 | 1 | OK |
| 6 | 7.19× (HIV-1 full set) | 1 | 1 | OK |
| 7 | 7.16–8.24× (HIV-1 novel-only) | 2 | 1 | OK (KR newly added in A-P1-3) |
| 8 | 9.36× (H3N2) | 1 | 1 | OK |
| 9 | 7.63× (SARS-CoV-2) | 1 | 1 | OK |
| 10 | 4.012× (EqualWeight H3N2) | 2 | 1 | OK (EN cont3+stage3; KR consolidated) |

추가 sync 확인:
- Bonferroni `2.5e-16` (HIV-1 full): EN=1, KR=1 ✓
- Bonferroni `3.9e-9` (HIV-1 novel-only Bonferroni adjusted): EN=1, KR=1 ✓ (cross-chapter §9.5 일괄 추가)
- Worst-case `5e-12`: EN=1, KR=1 ✓
- paired Δ `+0.011`, CI [-0.018, +0.042], permutation `p=0.61`: EN=2, KR=1 ✓
- `Stage~3` layer: EN=1 (line 8), KR=1 (line 12) ✓ (G08 한국어 전파 확인)
- Tranception caveat: EN=1 (line 13), KR=1 (line 21) ✓ (A-P1-6 일괄 적용)
- Retrospective/prospective caveat: EN=1 (line 2), KR=1 (line 19) ✓ (A-P1-4 + KR mirror)

**Drift 0건** — Cycle 1 abstract_review에서 식별한 한국어 P0 drift 2건이 모두 해소됨.

---

## 4. 잠재적 cross-chapter 영향 (cross-chapter 단계 검증 필요)

### 4.1. cross-chapter §9.1 (G08 family)
abstract.tex:8 / abstract_kr.tex:12 모두 `Stage~3 layer/정보 통합 레이어`로 통일됨. 다음 위치도 동일 표현 유지하는지 cross-chapter agent가 확인 필요:
- `chapters_en/ch1_introduction.tex` line 41 (three-step pipeline), line 82 (12-pathogen Stage 3 panel), line 111 (TikZ subbox `2-Stage main + Stage 3 layer`)
- `chapters_en/ch3_methods.tex` line 10, 172 (`two main stages` 또는 `Stages 1 and 2`)

### 4.2. cross-chapter §9.5 (Novel-only Bonferroni 3.9e-9)
Abstract 양쪽에 추가됨. 다음 위치 sync 필요:
- `chapters_en/ch1_introduction.tex` line 117 (TikZ HIV-1 enrichment), line 150
- `chapters_en/ch6_conclusion.tex` line 15 (6-P1-7 fix)

### 4.3. cross-chapter §9.7 (Tranception–ESM-LLR collinearity)
Abstract 양쪽에 caveat 추가됨. 다음 위치도 일관 caveat 필요:
- `chapters_en/ch3_methods.tex` line 655 (Tranception correlation table — sensitivity ω² 추가; 3-M-13)
- `chapters_en/ch5_discussion.tex` line 271-277 (5-P0-4 — leakage paragraph)

### 4.4. Retrospective/prospective caveat (A-P1-4 신규)
Abstract 양쪽에 추가. ch5:266-268 (5-P0-5 prospective sentence)와 정합 필요. ch6:91 future work에서도 prospective protocol 언급 검증.

### 4.5. 4-feature paired-test caveat (G07 family — kr 신규 동기화)
abstract_kr.tex:22가 영어 abstract와 동일한 nested-LOPO + paired-test caveat 사용. ch1:152 (1-P0-8 `statistically indistinguishable within ±0.04 MCC`), ch5:162 (5-P0-3), ch6:14 — cross-chapter §9.3 일괄 동기화 필요.

---

## 5. 최종 메모

1. **Cycle 1에서 LANDED된 영어 G07/G08 fix 보존됨** — abstract.tex:8/11/14 변경 없음, 검증만 수행.

2. **abstract_review가 식별한 P0 한국어 drift 2건이 모두 해소됨** (E1, E2 = A-P0-1, A-P0-2). 이는 abstract_review §F의 헤드라인 finding ("Cycle-1 P0 fixes landed correctly in English but were not propagated to Korean")을 직접 해결.

3. **Tier 2 P1 caveat 4건 (en+kr)** 추가:
   - 한·영 retrospective caveat (A-P1-4 + 한국어 mirror)
   - 한·영 Bonferroni 3.9e-9 (A-P1-5 + A-P1-3)
   - 한·영 Tranception/ESM-2 collinearity (A-P1-6)
   - 한·영 HIV-1 novel-only band (A-P1-3)

4. **A-P2-7 (validation scope clarity)** — 한국어는 이미 "주석 데이터 가용성에 의한 것이다"로 충분 — 추가 수정 불필요. 영어만 패치.

5. **길이**: EN 14 lines (변경 전 17 → 17 유지), KR 27 lines (변경 전 27 → 27 유지). 양쪽 모두 1-page 범위 내.

6. **수정 위치 summary**:
   - `front_en/abstract.tex`: 4건 (lines 2, 11×2, 13)
   - `front/abstract_kr.tex`: 4건 (lines 12, 19, 21, 22)

7. **재실험 0건** — 모든 fix가 텍스트 수정만으로 완료. integrated_fix_matrix §11의 재실험 0건 원칙 준수.

8. **다음 단계**: cross-chapter agent가 §4의 5개 cross-reference를 grep으로 일괄 검증 권장 (`grep -n "two-stage\|Stage~3\|3.9.*10\|Tranception\|retrospective" chapters_en/*.tex front*/*.tex`).
