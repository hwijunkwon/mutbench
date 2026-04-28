# Codex C3: Phase 4 Fairness 평가

작성일: 2026-04-28
대상: cycle 1 phase4 (7.27, B+) → cycle 3 phase4 (7.70, A−), Δ=+0.43
시각: 외부 codex IV&V 검수자, honest 비판자 입장

---

## 1. self-confirmation bias 가능성

cycle 3 phase 4 시뮬레이션은 **cycle 2-3에서 적용된 ~113 fix 목록을 모두 알고 있는 상태에서 진행**됐다. 이는 구조적 bias 위험이 크다.

- **bias 메커니즘**: cycle 3 시뮬레이터가 "이번 cycle에서 X fix가 들어갔다"는 prior를 가지고 있으면, 같은 본문을 다시 읽을 때 X fix와 관련된 문장을 우선적으로 찾고, 발견되면 "drafted as expected → +0.X"로 평가. 즉 fix의 **존재**가 **효과**로 자동 환산됨.
- **증거**: cycle3 평가표 비고 컬럼이 "EqualWeight 두 변형 분리 명시(production vs nested-LOPO)가 label leakage 의심 완전 차단" 같은 fix-anchored 문구로 채워져 있음. 외부 위원이라면 fix 이름 자체를 모르고, 본문에서 그 차단이 효과적인지 독립 판단해야 한다.
- **separation 어려움**: +0.43 중 (a) 본문 품질 향상으로 인한 진짜 회복 vs (b) 시뮬레이터가 fix 적용을 인지하고 점수에 반영한 acknowledgment bias를 분리 불가. **하한 추정: bias 기여 0.15~0.20**, 즉 **편향 보정 후 실제 회복은 +0.23~+0.28** 수준으로 추정.

**판정**: bias 정도 **중간** (high가 아닌 이유: fix 자체가 본문에 anchor되어 있어 외부 위원도 일부는 발견 가능; medium인 이유: 시뮬레이터가 fix를 미리 알고 있어 발견 비용이 0).

---

## 2. 항목별 회복 정당성

| 항목 | cycle1 | cycle3 | Δ | fix 사례 | 외부 시각 정당성 |
|------|--------|--------|---|----------|------------------|
| C 방법론 | 6.9 | 7.5 | +0.6 | EqualWeight 분리 / cell-level 4-param / wild-cluster acknowledge / Tranception ρ | **부분 정당** (+0.3~0.4 적절) |
| G 실용 | 6.7 | 7.0 | +0.3 | sec:prospective_validation_gap + H3N2 frequency-only pilot | **약하게 정당** (+0.1 적절) |
| I 한계 | 8.0 | 9.0 | +1.0 | sec:mafft_auto_artifact + Tranception ρ + single-team caveat | **과대** (+0.5 적절) |
| H 서술 | 7.8 | 8.5 | +0.7 | "operationally equivalent" 제거 + KR sync + Bonferroni 4파일 sync | **부분 정당** (+0.4 적절) |

**C +0.6 평가**: EqualWeight label-leakage 차단(코드 audit + 본문 분리 명시)은 진짜 +0.3 가치, cell-level 0.234 4-parameterization도 +0.2 가치. 그러나 wild-cluster bootstrap은 **acknowledge일 뿐 재추정 안 함**(+0.0), Tranception ρ 보고도 "channel separation 분석은 supplementary로 deferred"(+0.05). 합계 +0.5가 상한이고 +0.6은 약 +0.1 inflated. **외부 위원 권장: 7.3**.

**G +0.3 평가**: prospective evidence는 여전히 0건이다. sec:prospective_validation_gap은 **honest acknowledge일 뿐** prospective signal을 제공하지 않는다. H3N2 2010-cutoff pilot은 0/6 hit, 1/50 hit (Fisher p→1)로 오히려 **frequency-only가 prospectively 약하다는 negative result**. 외부 위원이라면 "honest gap을 인정한 것은 +0.1 가치, 그러나 negative pilot이 추가됨으로써 G 자체 ceiling은 변동 없음"으로 평가. **외부 위원 권장: 6.8** (cycle1 6.7 → +0.1).

**I +1.0 평가**: 가장 의심스러운 항목. 8.0 → 9.0은 학위논문 표준에서 **매우 드문 수준**(자체 보고). 외부 위원이라면 honest acknowledge는 양적 ceiling이 있다 — sec:mafft_auto_artifact + Tranception ρ + single-team caveat 모두 의미 있지만, **이미 cycle1에서 8.0이 매겨진 시점에서 추가 honest disclosure로 9.0을 받는 것은 시뮬레이터가 자기 fix에 후하게 점수**를 매긴 결과. 9.0은 "한계 인식이 학위논문 모범 사례 수준"을 의미하며, 그 정도 격상의 evidence는 부족. **외부 위원 권장: 8.5**.

**H +0.7 평가**: "operationally equivalent" → "non-rejection of inferiority" 7곳 동기화는 진짜 의미 있는 wording 정합성 개선(+0.3). KR abstract sync, Bonferroni p_adj 4파일 sync도 cross-chapter consistency로 +0.2. 그러나 +0.7은 글쓰기 등급이 7.8(평균 이상)에서 8.5(우수)로 한 등급 상승하는 것을 의미. cycle 3 본문 자체가 cycle 1보다 한 등급 더 잘 쓰여졌다고 보기는 어려움. **외부 위원 권장: 8.1** (cycle1 7.8 → +0.3).

---

## 3. 외부 위원 시뮬레이션

가정: fresh 외부 위원이 cycle 3 본문(238 pages)을 처음 본다. fix 목록은 모름.

| 시나리오 | 점수 | 근거 |
|---------|------|------|
| 가장 우호적 (honest disclosure를 적극 평가) | 7.55 | I=8.7, H=8.2, C=7.4, G=6.9 |
| 중립 외부 시각 (recommended) | **7.45** | I=8.5, H=8.1, C=7.3, G=6.8, 나머지 cycle3에서 -0.1~-0.2 |
| 엄격 외부 시각 (negative pilot 페널티) | 7.30 | G=6.5(prospective 부재), I=8.3, C=7.2 |

**외부 위원 추정 점수: 7.30 ~ 7.55, 권장 중앙값 7.45**. 즉 cycle 3 자체 보고 7.70은 약 **0.25 inflated**.

---

## 4. 각 페르소나 일관성

cycle 1 → cycle 3 페르소나별 trajectory:

- 교수6 (VEP/PLM, 가장 엄격): 6.9 → 7.6 (+0.7). cycle1에서 Tranception proxy를 -0.6 페널티했는데, cycle3에서 ρ table 추가만으로 +0.7 회복은 **과대**. 외부 PLM 전문가라면 "ρ 보고는 +0.3 가치, 그러나 contribution-level 분리 분석은 여전히 부재"로 +0.4 정도가 적절. **권장 7.3**.
- 교수8 (역학, 엄격): 6.8 → 7.2 (+0.4). H3N2 pilot이 negative result라는 사실을 시뮬레이터가 "정직성 보너스"로 흡수했지만, 외부 역학 위원이라면 "negative pilot은 G 자체 ceiling을 낮추는 evidence"로 해석. **권장 6.9**.
- 교수3 (통계/ML, 가장 엄격): 7.2 → 7.7 (+0.5). 4-parameterization sync는 의미 있으나 wild-cluster 미수행은 -0.2 페널티 유지가 외부 시각. **권장 7.5** 정도.
- 나머지 7명: cycle1 7.1~7.8 → cycle3 7.6~8.2. 평균 +0.4. 외부 시각에서는 +0.2~+0.3이 적절. **권장 평균 7.5**.

**페르소나 일관성 판정**: cycle1과 cycle3가 **같은 페르소나로 운영되었다는 보장이 약하다**. 같은 "교수6 VEP/PLM"이 cycle1에서 Tranception proxy를 매우 엄격하게 본 반면 cycle3에서는 ρ 보고 하나로 +0.7 회복을 줬는데, 진짜 같은 페르소나라면 ρ 보고 후에도 "channel-level separation 미실시"에 대해 cycle1과 동일하게 엄격해야 한다.

---

## 5. defense 92% 정당성

80% → 92% (+12pp)는 **과대 추정**. defense 통과는 strict score 외에도 (a) 위원장 컨센서스, (b) 형식 요건(분량/포맷/참고문헌), (c) defense 자체 Q&A 수행, (d) 학과·학교별 관습 등 strict score로 잡히지 않는 변수가 있다.

- cycle1 80%: phase4 평균 7.27, C/G strict 미달 → 80% 합리적.
- cycle3 92%: phase4 평균 7.70, 외부 시각 보정 후 7.45. **외부 보정 시 defense 통과 추정 85~88%**.
- +12pp는 항목별 회복(C +0.6, G +0.3)이 모두 strict thresh 통과로 해석된 결과지만, G=7.0은 **정확히 thresh 경계** — 외부 위원 한 명이 G를 6으로 채점하면 strict 미달. 92%는 "G가 이미 7.0으로 안전 통과"라는 가정에 의존하는데, G의 평균 7.0은 robust하지 않음(외부 시각 6.8).

**권장 defense %: 85% ~ 88%** (cycle1 80% → +5~8pp가 합리적).

---

## 6. 적대 시각: prospective/method 자격 점검

- **prospective evidence 0건 vs G +0.3**: 부당하다. honest acknowledge는 -0.5 페널티를 -0.3으로 완화할 뿐, +0.3 회복으로 전환되지 않는다. cycle3가 sec:prospective_validation_gap 추가를 +0.3으로 환산한 것은 **disclosure inflation**(disclosure를 contribution으로 오인). 외부 위원: G +0.1 (acknowledge 보너스).
- **method 강해진 게 아닌 documentation 강해진 vs C +0.6**: 부분 부당. EqualWeight 분리는 진짜 method clarification(+0.2~0.3 정당), wild-cluster acknowledge는 method 미강화(+0.0), Tranception ρ는 +0.1 (보고만, 분리 없음). **C +0.6은 +0.4가 상한**.
- **honest acknowledge로 I +1.0 vs method cap**: 외부 위원 시각에서 honest는 한계 항목(I)에 +0.5까지가 자연스러운 상한. +1.0(8.0→9.0)은 시뮬레이터의 self-favoring.

**적대 시각 결론**: 권장 보정 — **C 7.5→7.3, G 7.0→6.8, I 9.0→8.5, H 8.5→8.1**. 합계 평균 **7.70 → 7.45 (~A−/B+ 경계)**.

---

## 7. 권장 점수 보정

| 항목 | cycle3 자체 | **외부 권장** | Δ |
|------|------------|-------------|---|
| C 방법론 | 7.5 | **7.3** | -0.2 |
| G 실용 | 7.0 | **6.8** | -0.2 |
| H 서술 | 8.5 | **8.1** | -0.4 |
| I 한계 | 9.0 | **8.5** | -0.5 |
| 종합 평균 | 7.70 | **7.45** | -0.25 |
| Defense % | 92% | **85~88%** | -4~7pp |

---

## 종합 판정

- **bias 정도**: **중간** (medium). cycle3 시뮬레이터가 fix 적용을 prior로 알고 있어 disclosure inflation이 일부 항목(I, H, G)에서 명확히 관찰됨. 다만 본문에 fix가 anchor되어 있어 high까지는 아님.
- **외부 위원이 줄 점수 추정**: **7.45** (range 7.30 ~ 7.55).
- **Strict 기준**: 외부 시각에서도 평균 ≥ 7 통과, G=6.8이 thresh 0.2 미달이지만 cycle1과 동일한 "조건부 PASS" 영역. **unconditional PASS는 과대 보고**.
- **Lenient 기준**: 외부 시각 74.5점, B+ 영역 (cycle1 72.7 → +1.8). cycle3 자체 보고 77.0(A−)은 inflated.
- **Defense % 외부 추정**: 85~88% (cycle3 92%는 +4~7pp inflated).

**최종 권고**:
1. cycle 3 phase 4 점수는 **외부 시각 7.45 / Strict 조건부 PASS / Defense 85~88%**로 톤다운하여 보고.
2. C, G, I, H 4개 항목은 cycle 3 시뮬레이터가 self-fix를 후하게 평가한 acknowledgment bias가 명확.
3. lenient A− 등급 주장 보류 권고 — 외부 시각으로는 cycle1의 B+ 영역에서 0.2~0.3 회복 수준.
4. cycle 3가 진짜 7.70을 받으려면 prospective 4-feature pilot + Tranception channel-level separation 분석 두 건의 **실제 evidence**(disclosure 아님)가 필요.

(약 600 단어)
