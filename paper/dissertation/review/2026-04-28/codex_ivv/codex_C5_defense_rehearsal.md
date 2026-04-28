# Codex C5: 1시간 Hostile Defense Rehearsal

**시뮬레이션 위원**: 외부 학과 hostile 위원 (역학/통계/감염병 임상 어딘가에서 데려온, "벤치마크 같은 건 별로 본 적 없고 prospective evidence를 본능적으로 요구하는" 타입)
**defense 시간**: 90분 (30분 발표 + 60분 Q&A), hostile 위원 본인의 발언 시간은 사실상 25–30분
**작성 기준일**: 2026-04-28

---

## Phase 1: 첫 5분 인상

abstract와 ch1의 첫 페이지(~L50)만 읽고 hostile 위원으로서의 즉각 반응:

**즉각 식별되는 강점**
- 8,580 evaluation cells, 11 pathogens, 20 scoring × 39 detector — scale 자체는 한 학과 박사학위 표준을 명백히 넘어선다.
- 한 줄 안에 cluster-bootstrap CI, Bonferroni $p_{\text{adj}}$, "non-rejection of inferiority"라는 용어가 같이 등장 — 통계 honesty 면에서 학생이 단어를 골라 썼다는 인상.
- "no prospective time-forward validation"을 abstract 본문 안에 못 박은 것 — 외부 위원 입장에서 점수를 깎기 전에 학생이 먼저 인정한 것이라 첫 인상이 부드러워짐.

**즉각 식별되는 결함 / 의심**
- abstract L2가 "headline result"부터 "the optimal information source is pathogen-dependent"라고 단언하는데, $\omega^2_{\text{scoring}\times\text{pathogen}}=0.296$ 가 *실제로 무엇을 의미*하는지 abstract만 보면 모른다. 위원장이 "그래서 0.296이 크다는 거야 작다는 거야?"라고 물으면 학생은 본문으로 도망쳐야 한다.
- "11 RNA viruses"인지 "12 pathogens"인지 abstract 안에서도 흔들린다 (ch1 L82, L106, L142). cycle3가 통일했다지만 외부 위원은 *왜 panel이 두 개인가*부터 의심한다.
- HIV-1 single anchor 문제는 abstract L11이 직접 노출 — "anchored on HIV-1"이라고 했는데, 외부 위원의 거의 본능적 반응은 *"한 종에서 본 결과를 어떻게 일반 RNA 바이러스로 확장하는가"*이다.
- "non-rejection of inferiority, not pre-specified equivalence"는 *통계적으로 정확한* 표현이지만, 외부 위원 입장에서는 "그러면 4-feature가 충분하다는 주장은 *어떤 강도*로 하는가?"가 즉각 떠오른다.

**첫 인상 점수**: **6.5 / 10**
(scale·honesty은 7~8, single-anchor + 흔들리는 panel size는 5~6 사이. hostile 위원의 첫 인상은 평균 위원보다 0.5~1점 낮게 나오는 것이 정상.)

---

## Phase 2: 25분 Critical Q (3건)

### Q1 — Prospective evidence 부재의 직격탄

- **위원**: hostile 외부
- **질문 (verbatim)**: "Section 4.5 (`ch4:198`)에 H3N2 time-stratified pilot이 있는데, 2010–2015로 학습해서 2016–2020에 나타난 positions에 대해 frequency 단독으로는 0/20, 0/30, 0/50, 그리고 2021–2025에는 1/50을 잡았다. Fisher $p \to 1.00$. 이게 'frequency alone is retrospectively diagnostic but prospectively weak'라고 학생이 이미 ch4:201에 적었는데, 그러면 *MutBench의 4-feature core나 EqualWeight integration이 prospectively 더 낫다*는 증거는 어디에 있는가? 이 dissertation의 어디에서도 'multi-source가 prospective하게도 frequency를 이긴다'는 head-to-head 결과를 본 적이 없다. 그렇다면 abstract의 'reduces the experimental search space' 라는 주장은 retrospective 4×만 보여주고 멈춘 것이고, *forward-time*에서는 학생이 직접 stress-test한 결과가 없다. 맞는가?"
- **본문 anchor**: `ch4:198–222` (H3N2 pilot 표), `ch5:337–342` (sec:prospective_validation_gap), `ch5:155` (3-problem return)
- **학생 답변 가능성**: **중간**
  - 학생이 *답할 수 있는* 부분: ch5:337의 정직한 인정 + ch4의 결과는 frequency single-feature이지 multi-source가 아님 + multi-source prospective는 Priority 1 future work
  - 학생이 *답하기 어려운* 부분: hostile 위원이 "그래서 *MutBench의 핵심 운용 주장이 retrospective evidence만으로 지지*되고 있다"는 결론을 강제하면 학생은 인정해야 한다. 이 단계에서 학생이 "검증은 retrospective이고, prospective는 future work"라고 말하는 순간 hostile 위원은 *"그럼 박사학위 *지금*에 이 학생이 *해결*한 문제는 무엇인가?"*로 압박을 이어간다.
- **무력화 시 후속 Q**: "Bailey 2018 (PanCancer)이 prior to reproducibility effort에 한 번도 prospective check 없이 박사학위를 통과시킨 게 학과 standard라고 학생은 말할 것인가? 한 학생의 학위 결정에서 'future work에 미루고 그 미룬 일이 *지금* 학생의 contribution에 핵심적인 것'은 보통 *조건부 통과*의 트리거다."

### Q2 — HIV-1 single anchor의 외부타당성

- **위원**: hostile 외부
- **질문**: "Contribution 3b의 외부 검증은 본질적으로 HIV-1 한 종이다. abstract L11에서 *anchored on HIV-1*이라고 직접 적었고, ch5:179에서 *the practical-value claim rests mainly on HIV-1*이라고 적었다. H3N2는 69% Layer A overlap이라 self-consistency check, SARS-CoV-2는 Bonferroni 후 exploratory. 즉 11 pathogens 중 *외부 타당화에 진정으로 기여하는 것은 1*이다. 이 학위논문의 핵심 *contribution 3*가 *n=1*에 의존하고 있다는 것을 학생은 어떻게 박사학위 통과 기준에 부합한다고 주장할 것인가? 만약 HIV-1 antibody-escape 데이터셋(예: Bloom lab DMS)에 *체계적인 sampling bias*가 있다면 — 예를 들어 broadly neutralizing antibody panel의 epitope coverage가 V1V2/V3/CD4bs로 편향되어 있다면 — 학생의 7.16–8.24× enrichment는 *그 panel의 epitope structure*를 재발견한 것에 불과할 수 있다."
- **본문 anchor**: `ch1:150` (Contribution 3b 정의), `ch5:176–179` (3-tier evidence rule), `abstract L11`
- **학생 답변 가능성**: **낮음**
  - 학생이 답할 수 있는 부분: 3-tier evidence rule (Bonferroni × <33% overlap)이 사후가 아니라 사전 규칙임을 보여줄 수 있다 + Layer-A-disjoint 37 positions에서도 7.16×가 worst-case라는 점.
  - 학생이 답하기 어려운 부분: *왜 다른 RNA 바이러스에 antibody-escape DMS 데이터셋이 부족한가*는 현실적 데이터 가용성 문제이지 학생의 잘못이 아니지만, hostile 위원은 "그게 *학생의 한계가 아니라 학위논문 자체의 한계*"라고 밀어붙일 수 있다. *n=1 anchor*라는 한계는 ch5:151 ("HIV-1 single anchor")에서 *honest 인정*되어 있지만, hostile 위원은 *honest 인정으로 통과시킬 결함*인지 *조건부 통과를 요구할 결함*인지 결정한다.
- **무력화 시 후속 Q**: "그렇다면 학생의 contribution 3는 *MutBench가 HIV-1 escape에 잘 맞는다*는 1-pathogen 결과로 격하되어야 한다는 것을 인정하는가? 이 case에서 *practically reduces the experimental search space*라는 abstract 주장은 1-pathogen 케이스로 약화되어야 하지 않는가?"

### Q3 — $\omega^2$의 다중 reading: cherry-picking 의심

- **위원**: hostile 외부
- **질문**: "ch3 / ch4 / ch5에 걸쳐서 $\omega^2_{\text{scoring}\times\text{pathogen}}$의 값이 *6개 이상*의 reading으로 보고되어 있다 — cell-level 0.234, evaluation-level 0.296, ANCOVA-adjusted 0.264, Bayesian posterior mean 0.252 (priors A) 또는 0.319 (priors B), 6-category aggregated 0.103, cluster-bootstrap CI [0.195, 0.333], wild-cluster bootstrap *deferred*. 이 중 *abstract와 headline에 들어간 숫자는 0.296*이다. 이건 *highest non-conservative reading*에 해당한다. wild-cluster bootstrap을 미실시한 상태에서 — Cameron 2008이 명시적으로 cluster <30일 때 percentile cluster bootstrap이 anti-conservative라고 한 그 critique를 학생이 ch5:289에서 직접 인용했음에도 — 학생은 왜 0.296을 headline에 박았는가? 0.103 (lower bound)을 headline에 박지 않은 이유는 무엇인가? 이건 reader-friendly한 *highest defensible number*를 고른 cherry-picking 아닌가?"
- **본문 anchor**: `ch3:959`, `ch4:425–526`, `ch5:285–291`
- **학생 답변 가능성**: **중간 (방어 가능하지만 시간 소모)**
  - 학생이 답할 수 있는 부분: 6-category 0.103도 *abstract에서 함께 보고*되고 있고 ("collinearity-robust lower bound"), Bayesian HDI [0.188, 0.314]가 cluster-bootstrap CI [0.195, 0.333]과 거의 일치한다는 점. 그리고 "0.296"의 reading은 evaluation-level *fixed-effect* 추정치로, 6 readings 중 *어느 것을 골라도 large-effect threshold (0.14)*를 넘는다는 점. 즉 *robust*하다.
  - 학생이 답하기 어려운 부분: hostile 위원이 "그러면 abstract에 0.103–0.319 *range*로 적었어야 한다"고 강제하면 학생은 abstract revision을 약속해야 한다 (이미 ch1:148 "$\omega^2 = 0.296$ ... 6-category aggregation gives $\omega^2 = 0.103$ as a collinearity-robust lower bound" 형식으로 본문에서는 사실상 그렇게 했지만, abstract L10 본문은 0.296을 single point로 표시).
- **무력화 시 후속 Q**: "위원장님, 이 학생은 통계적 honesty의 *형식*은 갖추었지만 (모든 reading을 보고함), 그 *형식*과 *headline에 박은 숫자*가 *사실상 같은 메시지*라는 것이 학위논문 honesty의 의미입니다. 1줄 abstract에 0.296을 single point로 적은 것은, 한 단어로 말하면 *presentational dishonesty*입니다."

---

## Phase 3: 25분 Major Q (4건)

### Q4 — Tranception–ESM-LLR channel collinearity

- **위원**: hostile 외부 (또는 PLM 전문가 내부 위원과 협공)
- **질문**: "ch5:279에 *the 'Tranception' channel is computed as a lightweight ESM-2 masked-marginal pseudo-perplexity proxy*라고 적혀 있다. 그리고 11/12 pathogens에서 ESM-2 LLR과 Pearson 0.64–0.84 collinear이다. 그러면 *SARS-CoV-2 best = Tranception*이라는 abstract의 결과는 *동일한 PLM family 안에서의 micro-variation*에 불과할 가능성이 매우 높다. 9 distinct optimal types라고 했는데, 사실상 *6 distinct families*로 환산해야 하지 않는가?"
- **본문 anchor**: `ch5:279–281`, `abstract L13`, `ch4` (Tranception channel definition)
- **학생 예상 답변**: ch1:148 "Tranception/ESM-2 channel collinearity is not separated at headline granularity"라는 caveat이 *이미 있다*는 점, 6-category $\omega^2 = 0.103$은 collinearity-robust lower bound이며 그 안에서도 large-effect threshold를 통과한다는 점.
- **무력화 시 후속 Q**: "그러면 abstract의 *9 distinct optimal information types*라는 주장은 *9 distinct scoring formulas*이지 *9 distinct biological information sources*가 아니라는 것을 인정하는가? 이는 abstract 본문 수정이 필요하다."

### Q5 — Layer A의 immune-escape 우세 → circular reasoning 잔여

- **위원**: hostile 외부
- **질문**: "Layer A는 'pathogen-specific union of convergent-evolution, immune-escape, and HVR-membership evidence types, with immune-escape positions dominating the curated set' (abstract L6)이다. 그리고 외부 검증은 vaccine-escape (또 다른 immune-escape의 형태)이다. circularity audit이 ch5:176에서 *HIV-1 18% Layer A overlap*으로 통과했다고 주장하지만, 이는 *position*-level disjoint이지 *biological information source*-level disjoint이 아니다. Layer A를 만든 *문헌 evidence*와 vaccine-escape *positive set*을 만든 문헌이 *substantively overlap*할 수 있다 (둘 다 antibody-escape 연구에서 나옴). 학생은 *literature provenance*가 Layer A와 escape set 간에 disjoint한지 audit했는가?"
- **본문 anchor**: `ch5:176–184` (3-tier rule), `ch4` (Table vaccine_escape_stage3)
- **학생 예상 답변**: 18% positional overlap이 가장 directly auditable한 양이다. literature-provenance audit은 deferred (Priority N future work)일 가능성이 높다.
- **무력화 시 후속 Q**: "그러면 *MutBench의 positional disjoint*는 *information disjoint*가 아니라는 한계를 ch5에 명시적으로 추가해야 한다. 현재 본문에는 이 한계가 없다."

### Q6 — Friedman p=0.990: null인가 underpowered인가

- **위원**: hostile 외부
- **질문**: "ch5:323에서 *Friedman 결과는 uninformative이지 strict null의 confirmation이 아니다*라고 학생이 직접 적었다. 그러면 abstract L10의 *Friedman test shows no universally best combination ($\chi^2 = 7.69$, $p = 0.990$)*은 *현재 데이터로는 결정 불가*라는 의미이다. 그럼에도 abstract는 이를 *no universally best combination*으로 *해석*하고 있다. 이건 *underpowered = null*이라는 typical statistics 오류와 어떻게 다른가?"
- **본문 anchor**: `ch5:323`, `abstract L10`
- **학생 예상 답변**: ANOVA interaction (0.296)과 oracle-vs-generalized MCC gap (0.265) 두 *독립 증거*가 같은 방향을 가리키고 Friedman은 *null-consistent corroboration*으로만 사용했다는 점 (실제로 ch5:323이 정확히 그렇게 적혀있다).
- **무력화 시 후속 Q**: "그러면 abstract L10의 Friedman 줄은 *삭제 또는 약화*가 필요하다. 현재 표현은 underpowered=null 오류를 *시사*하고 있다."

### Q7 — 4-feature core: 어떤 강도의 주장인가?

- **위원**: hostile 외부 (통계 위원과 협공)
- **질문**: "Contribution 3a는 *4-feature core가 10-feature와 statistically indistinguishable*이라고 주장하는데, *paired delta +0.011, 95% CI [-0.018, +0.042], p=0.61, ±0.04 MCC non-inferiority bound, sign-flip permutation*이라는 도구를 모두 동원했다. 이 모든 것이 *non-rejection of inferiority, not pre-specified equivalence*로 약화되어 있다. 그러면 학생의 *operational claim*은 무엇인가? *4-feature를 사용해도 좋다*인가, *4-feature가 좋다는 증거는 부족하다*인가? 박사논문 contribution은 *operational direction*을 제시해야 한다."
- **본문 anchor**: `ch1:150–152`, `ch4:526` 부근 nested-LOPO 표.
- **학생 예상 답변**: "4-feature를 출발점으로 권고하지만, 10-feature를 *이긴다*고 주장하지 않는다. operational direction은 *practitioner가 4-feature로 시작해도 안전하다*이지 *4-feature가 항상 best*가 아니다." — 이건 honest answer이고 hostile 위원도 받아들일 수 있다.
- **무력화 시 후속 Q**: "그러면 ch6 conclusion에서 4-feature를 *recommended starting point*로 격하해서 적었는가? abstract에서도 그 격하를 반영했는가?"

---

## Phase 4: 결론

### 위원장 판단 추정

위원장은 *consensus 추구* 성향이 보통이고 한 명의 hostile 위원이 *모든 질문을 답 못 하게 만드는* 시나리오를 피하려 한다. 따라서:

- 위원장은 hostile 위원의 **Q1 (prospective)** 와 **Q3 (cherry-picking)** 를 *학위 통과 트리거*가 아니라 *조건부 revision*으로 옮기려 시도할 가능성이 높다.
- 위원장은 학생이 ch5:337 (sec:prospective_validation_gap)과 ch5:285 ($\omega^2$ 6-reading caveat)를 *본문에 명시적으로 적은 것*을 통과 사유로 사용한다 ("학생이 한계를 인지하고 있다").
- 위원장은 hostile 위원에게 "*revision으로 cover 가능한 항목인가, fail trigger인가?*"를 물어볼 것이고, hostile 위원은 보통 *조건부*에 동의한다 (학위논문 *내용물*은 충분하고, *프레이밍*이 약간 강하다는 의견).

### 5명 위원 분포 추정

| 위원 | 입장 | Q1~Q7 중 우려하는 것 |
|------|------|--------------------|
| 위원장 (생물정보학) | Lenient pass | Q3 (presentation strength) — revision으로 충분 |
| 지도교수 (CS/SE) | Strong pass | 거의 없음 — scale + reproducibility 강점에 집중 |
| 통계/ML 위원 | Mid (revision 권고) | Q3, Q6, Q7 — wild-cluster bootstrap 1회 측정 권고 |
| 계산생물학 / 바이러스 위원 | Mid pass | Q2, Q5 — single anchor 한계 인정으로 충분 |
| **외부 hostile 위원** | **조건부 통과** | Q1, Q2 — 그러나 fail까지 가지 않음 |

5명 중 *unconditional pass* 2명 + *조건부 pass* 3명 = **조건부 통과 다수결**.

### Fail trigger 분석

- 학위 fail은 *단일 질문 답 못 함*이 아니라 **(a) 3-4개 critical question을 모두 답 못 함** OR **(b) 1개 질문에서 데이터/통계 *조작* 의심을 위원장이 받음**일 때 발생한다.
- 본 학위논문은 (a)에 해당하지 않는다 — 학생이 Q3, Q6, Q7은 본문에서 *이미 honest로 처리*했고 답변 anchor가 명확하다.
- (b)도 해당하지 않는다 — equalweight_audit.md가 라벨 누출 의혹을 retire 처리.
- 가장 위험한 fail trigger는 *학생이 Q1에 대해 자기변호를 시도하다가 abstract와 ch5:337의 honest disclosure가 충돌하는 진술을 하는 경우*. 즉 *학생 본인의 답변이 본문과 모순*이 되는 순간이 진짜 fail trigger이다.

### 최종 추정

**조건부 PASS** (revision-required pass, 학위는 통과)

조건부 revision 항목 (최저 acceptable):
1. abstract L10에서 Friedman 줄 *underpowered* qualifier 추가 또는 *0.296* 옆에 *(0.103 6-category lower bound)* 명시.
2. ch6 또는 ch5에서 "4-feature core = recommended starting point, not provably optimal" 한 줄 명시 (사실상 본문에는 있으나 conclusion 강도 약화 필요).
3. Tranception–ESM-LLR per-pathogen ρ supplementary table 추가 (1–2시간 작업으로 가능, summary_cycle3 §5에 이미 식별됨).

---

## 가장 위험한 단일 질문

**Q1 (Prospective evidence 부재)** — H3N2 pilot의 0/20, 0/30, 0/50, 1/50.

이 질문이 가장 위험한 이유:
- ch4 본문의 negative result가 그대로 인용 가능 (위원이 본문을 끌어와 학생의 부담으로 변환).
- 학생의 답이 *future work*로 회피하면 *학위 자체*의 contribution 약화.
- 학생의 답이 *retrospective evidence가 충분*하다고 강하게 방어하면 ch5:337의 honest disclosure와 모순.
- 답변의 *narrow-path*가 좁다: "frequency single-feature pilot이고 multi-source는 미평가, retrospective evidence가 1차 증거이며 prospective는 future work"라는 정확한 phrasing이 필요하다. 흔들리면 fail trigger 근처까지 간다.

이 질문을 *답변 노트*로 사전에 외워서 들어가는 것이 학생에게 가장 큰 우선순위.

---

## Defense % 외부 추정

| Source | Estimate |
|--------|----------|
| summary_cycle3.md (in-house) | 92% |
| **codex 외부 (hostile 위원 1명 시뮬레이션)** | **84–88%** |

격차 원인:
- in-house simulation은 *consensus 추구 위원장* 가정 하에서의 평균 통과율.
- hostile 위원 1명이 *조건부 pass*를 강하게 고집하면 *unconditional pass* 확률이 92% → 50–60%대로 떨어지지만, **학위 통과 자체** (조건부 pass 포함)는 여전히 84–88%.
- 즉 *unconditional pass* 92% vs *학위 통과* 84–88%의 차이가 in-house와 외부의 6–8pp gap을 설명한다.
- summary_cycle3.md의 92%는 *학위 통과* 의미로 해석하면 약 4pp 낙관적, *unconditional* 의미로 해석하면 35pp 이상 낙관적이다.

---

## 사전 준비 권장 (학생용)

defense 1주일 전까지 작성할 5개 답변 노트:

1. **Q1 (prospective) 답변 노트** — ~150 단어, ch4:198–222 표 + ch5:337 단락의 *exact phrasing* 외울 것. 핵심: "frequency single-feature pilot이며, multi-source 4-feature core의 prospective evaluation은 Priority 1 future work이다. 본 학위논문의 contribution은 *retrospective benchmarking infrastructure + retrospective external anchor (HIV-1)*에 한정되며, prospective claim은 의도적으로 보류했다."

2. **Q2 (HIV-1 single anchor) 답변 노트** — ~120 단어, ch5:176–184 + ch1:150 인용. 핵심: "3-tier evidence rule은 사후 selection이 아닌 사전 규칙이며, HIV-1은 18% Layer A overlap + Bonferroni $p_{\text{adj}}=2.5\times10^{-16}$ + Layer-A-disjoint 37 positions에서도 7.16× worst-case라는 *independent dimensions*를 만족한다. n=1 anchor 한계는 ch5:151과 summary_cycle3 §6에 명시 인정."

3. **Q3 (cherry-picking $\omega^2$) 답변 노트** — ~120 단어, 6 readings 표를 외워서 *모든 reading이 large-effect threshold (0.14)*를 통과한다는 점을 강조. 0.103도 6-category aggregation에서 abstract 본문에 *함께* 적혀 있다는 사실. *robust*가 답이지 *0.296을 고른 것*이 답이 아니다.

4. **Q5 (Layer A circularity literature provenance) 답변 노트** — ~80 단어, 18% positional disjoint이 *current best auditable measure*이며, *literature-provenance level disjoint audit*는 deferred future work라는 정직한 인정. revision 요구되면 ch5에 1단락 추가 약속.

5. **Q7 (4-feature operational direction) 답변 노트** — ~100 단어, "*recommended starting point* not *provably optimal*"이라는 *exact phrasing* 사용. ch6 conclusion에서 동일한 phrasing이 사용되었음을 확인 (필요 시 한 줄 추가).

추가 권고:
- Q4 (Tranception collinearity) 와 Q6 (Friedman) 는 *답변 anchor가 본문에 이미 있고*, 학생이 본문 인용만으로 60–90초 내에 답할 수 있다 — 별도 노트 필요 없음.
- 30분 발표 슬라이드의 *마지막 limitation slide*에 *"3 honest disclosures: prospective gap, single anchor, Tranception–ESM proxy"* 한 줄을 *직접* 띄우고 발표하는 것을 강력 권고. hostile 위원의 첫 instinct를 약화시키는 가장 효과적인 단일 조치.

---

**총평**: 이 학위논문은 *내용물의 두께*는 박사학위 표준을 상회하고, *honest disclosure의 형식*이 외부 위원이 fail trigger를 누르기 어렵게 만든다. 그러나 *headline framing*은 conservative reading(예: 0.103, *recommended starting point*, novel-only 7.16×)이 아니라 *strongest defensible reading*(0.296, *statistically indistinguishable*, full-set 7.19×)으로 작성되어 있어, hostile 위원이 *cherry-picking* 카드를 꺼낼 수 있다. 이는 fail trigger가 아니라 *조건부 revision* trigger이다. 따라서 정당한 외부 추정은 **84–88% (학위 통과) / 50–60% (unconditional pass)**.
