# Defense Q1 Answer Note — Prospective Evidence Gap

작성일: 2026-04-28
대상 질문: codex_C5_defense_rehearsal.md Q1 (가장 위험한 단일 질문)

---

## Q1 (verbatim, hostile 외부 위원)

> "Section 4.5 (`ch4:198`)에 H3N2 time-stratified pilot이 있는데, 2010–2015로 학습해서 2016–2020에 나타난 positions에 대해 frequency 단독으로는 0/20, 0/30, 0/50, 그리고 2021–2025에는 1/50을 잡았다. Fisher $p \to 1.00$. 이게 'frequency alone is retrospectively diagnostic but prospectively weak'라고 학생이 이미 ch4:201에 적었는데, 그러면 *MutBench의 4-feature core나 EqualWeight integration이 prospectively 더 낫다*는 증거는 어디에 있는가? 이 dissertation의 어디에서도 'multi-source가 prospective하게도 frequency를 이긴다'는 head-to-head 결과를 본 적이 없다. 그렇다면 abstract의 'reduces the experimental search space' 라는 주장은 retrospective 4×만 보여주고 멈춘 것이고, *forward-time*에서는 학생이 직접 stress-test한 결과가 없다. 맞는가?"

---

## 답변 구성 (총 ~150 단어, 60–90초)

### Step 1 — Honest disclosure 인정 (15초, ~30 단어)

> "정답은 *맞습니다*. Prospective time-forward validation은 이 학위논문에 부재하며, 그 부재 자체를 ch5:337 (\sec:prospective_validation_gap)에서 명시적으로 honest disclosure로 못 박았습니다."

**Anchor**: ch5:337–342, ch4:201, abstract 첫 문단의 "no prospective time-forward validation" qualifier.

### Step 2 — H3N2 pilot의 정확한 framing (20초, ~40 단어)

> "H3N2 pilot의 0/20, 0/30, 0/50, 1/50 결과는 *frequency single-feature*에 대한 method-of-failure analysis입니다 — frequency-only detector가 forward-time에서 약하다는 것을 보여주는 부정적 증거이며, MutBench 4-feature core나 EqualWeight integration의 prospective 결과는 \emph{측정하지 않았습니다}. 이 두 결과를 같은 evaluation에 두지 않은 것은 의도적 선택이며, multi-source의 prospective head-to-head는 Priority 1 future work입니다."

**Anchor**: ch4:198–222 (H3N2 pilot table), ch5:337–342, ch6:62 (Future Roadmap Priority 2).

### Step 3 — 본 논문의 contribution 경계 (20초, ~40 단어)

> "본 학위논문의 contribution은 *retrospective benchmark 인프라* (Contribution 1: 8,580-cell MutBench grid), *retrospective pathogen-dependent finding* (Contribution 2: $\omega^2 = 0.296$), 그리고 *retrospective external anchor* (Contribution 3b: HIV-1 vaccine-escape Bonferroni $p_{\text{adj}} = 2.5 \times 10^{-16}$)에 한정됩니다. Prospective deployment claim은 의도적으로 보류했고, abstract의 'reduces the experimental search space'는 retrospective enrichment evidence (HIV-1 7.19$\times$, H3N2 4.012$\times$)에 anchor된 표현입니다."

**Anchor**: ch1:141–155 (3 contributions), ch5:337–342 (boundary), abstract:11.

### Step 4 — Future work 명시 (10초, ~20 단어)

> "Prospective forward-time holdout (training $T \le T_0$, testing $T > T_0$)은 ch6 Future Roadmap Priority 1로 등록되어 있고, MutBench 인프라가 이를 받아들일 수 있는 상태로 설계되어 있습니다."

**Anchor**: ch6:60–67 (Future Roadmap), ch5:342 (forward-time holdout queued).

---

## 후속 질문 대비

### 후속 Q1a: "Then why call it MutBench?"

**답변** (~40 단어):
> "MutBench는 *retrospective evaluation framework*의 brand이며, prospective deployment는 follow-up work입니다. 이 명칭은 'mutation hotspot benchmark'를 줄인 것으로, 'benchmark' 용어 자체가 학계에서 retrospective 비교 측정 도구를 의미하며 (ProteinGym, ViroGym, EVEREST와 동일 framing), prospective predictor를 의미하지 않습니다. 그 한계는 abstract 첫 줄과 ch5:337–342에 명시했습니다."

### 후속 Q1b: "그럼 contribution 3a/3b도 retrospective뿐인가?"

**답변** (~40 단어):
> "예, 3a (4-feature core)와 3b (HIV-1 anchor) 모두 retrospective evidence에 anchor됩니다. 3a는 nested-LOPO (paired delta $+0.011$, $p = 0.61$)로 *non-rejection of inferiority*를 입증한 것이고, 3b는 Bonferroni $p_{\text{adj}}$로 retrospective enrichment의 통계적 유의성을 입증한 것입니다. 두 결과 모두 prospective deployment evidence가 아니라는 점은 ch5:337에서 명시했습니다."

### 후속 Q1c: "그렇다면 박사학위 *지금* 학생이 *해결*한 문제는 무엇인가?"

**답변** (~50 단어):
> "본 학위논문이 *지금* 해결한 문제는 세 가지입니다. (1)~RNA-virus 단일 위치 hotspot detection의 region-level benchmark 인프라 부재 — 8,580-cell MutBench grid로 해결. (2)~'어떤 정보 source가 어떤 pathogen에 가장 효과적인가'에 대한 통계적 답변 부재 — $\omega^2_{\text{scoring}\times\text{pathogen}} = 0.296$ (large-effect)로 해결. (3)~Multi-source integration의 외부 검증 부재 — HIV-1 vaccine-escape anchor로 해결. *Prospective deployment*는 *지금* 해결한 문제가 아니라 *지금 인프라로 풀 수 있게 된* 문제이며, 그 차이를 정직히 표시했습니다."

---

## 답변에서 *피해야* 할 표현

1. **"검증은 retrospective이고, prospective는 future work"** — 이렇게만 답하면 위원이 "그럼 *지금* 학생의 contribution은 무엇인가?"로 압박을 강화함. 반드시 Step 3 (본 논문의 contribution 경계)을 같이 명시.
2. **"prospective도 사실상 됐다"** — ch5:337의 honest disclosure와 모순됨. 절대 시도 금지.
3. **"H3N2 pilot이 multi-source를 포함한다"** — 사실과 다름. H3N2 pilot은 frequency single-feature 결과임 (ch4:198–222). 이 사실을 흔들면 fail trigger.

---

## 외워야 할 정확한 anchor (verbatim)

- **ch5:337**: "A central honesty disclosure is that no \emph{prospective}, time-forward validation has been conducted in this dissertation."
- **ch5:342**: "Until a prospective evaluation is completed, the operational claim 'MutBench can be used to prioritise emerging hotspots' is supported by retrospective enrichment evidence only..."
- **abstract:2**: "no prospective time-forward validation" (within the headline result sentence)
- **ch4:201**: "frequency alone is retrospectively diagnostic but prospectively weak" (H3N2 pilot conclusion)

---

## 발표 슬라이드 권고 (Phase 0 사전 차단)

30분 발표의 *마지막 limitation slide*에 다음 한 줄을 직접 띄우고 발표할 것:

> **"Three honest disclosures: (1) prospective gap, (2) HIV-1 single anchor, (3) Tranception–ESM channel proxy."**

이 슬라이드를 본 hostile 위원은 Q1을 던지더라도 *학생이 이미 알고 있다*는 정보를 가지고 시작하므로 fail trigger 거리에서 약 1단계 멀어진다 (codex_C5 §Phase 4 권고).

---

## 답변 시간 가이드

- Step 1 (인정) — 15초
- Step 2 (H3N2 pilot framing) — 20초
- Step 3 (contribution 경계) — 20초
- Step 4 (future work) — 10초
- **총 65–80초**

후속 질문은 *답이 짧을수록 좋다*. Q1a/Q1b/Q1c 각각 30–45초 이내로 종결.

---

## 종합 위험 평가

이 노트의 정확한 phrasing을 외워서 들어가면, codex_C5 §Phase 4 추정 ("조건부 PASS, 84–88%")이 흔들리지 않는다. 흔들면 *학생 본인의 답변이 본문 (ch5:337)과 모순*되는 순간이 발생하고, 이것이 진짜 fail trigger임 (codex_C5 §Phase 4 마지막 단락).
