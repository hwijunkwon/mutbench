# 교수 10명 평가 시뮬레이션 (Phase 4, 2026-04-28)

## 대상 논문 상태
- v148 + P0 9건 수정 후 (2026-04-28)
- 206 pages, LaTeX errors 0, undefined refs 0
- 자동 검증 86/86 PASS, Statistics 10/10 PASS, Red team Critical 5건 모두 해소(caveat 또는 수정), CCB P0 9건 모두 수정 완료
- 미해소: P1 12건 (권장), P2 15건 (선택)

논문 핵심 수치 (P0 반영):
- 헤드라인 ω²(scoring×pathogen) = 0.296 (cluster-bootstrap [0.195, 0.333]; 6-category 0.103)
- LOPO 0/11 (permutation null P≈0.96 → "null-consistent corroboration"으로 격하), oracle-vs-generalized gap 0.265
- HIV-1 vaccine-escape primary anchor: full-set 7.19× / novel-only(37 Layer-A-disjoint) 7.16–8.24× (worst-case Fisher p=5.0×10⁻¹², Bonferroni p_adj≈3.9×10⁻⁹)
- H3N2 9.36× = self-consistency (69% Layer-A overlap; novel-only p=0.132 n.s.)
- SARS-CoV-2 7.63× = exploratory (Bonferroni 미통과)
- 4-feature core 97.6% retention (numerical equivalence; paired-test 미수행)
- Within-cell residual ω²≈0.39 (modeled vs unmodeled 명시)
- Bayesian hierarchical: ω²_int posterior mean 0.252, 95% HDI [0.188, 0.314], P(>0.14)=0.996
- ANCOVA(length, positive rate): scoring×pathogen 0.234→0.264 (오히려 증가)
- HCV exclude 0.246 / +Norovirus exclude 0.187 / 4 phylo-only 0.137 (모두 medium 이상)

---

## 평가표 (각 교수 × 9 항목)

| 교수 | 전공 | A | B | C | D | E | F | G | H | I | J | 평균 | 등급 |
|------|------|---|---|---|---|---|---|---|---|---|---|------|------|
| 1 | 위원장 (생물정보학) | 8 | 8 | 7 | 8 | 7 | 8 | 7 | 8 | 8 | 8 | 7.7 | PASS |
| 2 | 지도교수 (CS/SE) | 8 | 8 | 7 | 8 | 8 | 7 | 8 | 8 | 8 | 8 | 7.8 | PASS |
| 3 | 통계/ML | 7 | 8 | 7 | 7 | 7 | 7 | 6 | 8 | 8 | 7 | 7.2 | PASS |
| 4 | 계산생물학 | 8 | 7 | 7 | 7 | 7 | 7 | 7 | 8 | 8 | 7 | 7.3 | PASS |
| 5 | 바이러스/공중보건 | 8 | 7 | 7 | 7 | 7 | 7 | 7 | 8 | 8 | 7 | 7.3 | PASS |
| 6 | VEP/PLM 전문가 | 7 | 8 | 6 | 7 | 7 | 6 | 6 | 7 | 8 | 7 | 6.9 | 조건부 |
| 7 | 벤치마크 방법론 | 8 | 7 | 7 | 7 | 7 | 8 | 7 | 8 | 8 | 7 | 7.4 | PASS |
| 8 | 역학 실무자 | 7 | 6 | 7 | 6 | 7 | 7 | 6 | 7 | 8 | 7 | 6.8 | 조건부 |
| 9 | 통계유전학 | 7 | 7 | 7 | 7 | 7 | 7 | 6 | 8 | 8 | 7 | 7.1 | PASS |
| 10 | 구조생물학 | 7 | 7 | 7 | 6 | 7 | 7 | 7 | 8 | 8 | 7 | 7.1 | PASS |
| **평균** | — | **7.5** | **7.3** | **6.9** | **7.0** | **7.2** | **7.1** | **6.7** | **7.8** | **8.0** | **7.2** | **7.27** | — |
| **최저** | — | **7** | **6** | **6** | **6** | **7** | **6** | **6** | **7** | **8** | **7** | **6.8** | — |

---

## 교수별 상세 평가

### 교수 1 (위원장, 생물정보학) — 전체 구조와 논리 흐름

- 점수: A=8, B=8, C=7, D=8, E=7, F=8, G=7, H=8, I=8, J=8, 평균=**7.7**
- 강점: **3-Layer ground truth (Ch3 §3.2.2, ll.235–411)** 설계가 evolutionary/structural/functional 세 차원을 직교하게 분리하고, 각 Layer가 어느 metric에 매핑되는지 (Layer A→MCC, Layer B→constrained FPR, Layer C→DMS F1)를 Ch3 ll.353–357에서 명시한 점이 특히 견고함. 단일 hotspot 정의를 강제하지 않고 disagreement 자체를 결과로 보고하는 설계 (Table~\ref{tab:layer_a_vs_c}, Ch4 ll.541–551)는 학위논문 수준의 방법론적 성숙도를 보여줌.
- 약점: **Layer A 정의의 이질성** (Ch3 ll.290–298, ll.391–393). SARS-CoV-2/H3N2는 phylogenetic convergent evolution, HCV는 HVR diversifying selection, Norovirus는 epochal variant — 이 셋이 같은 "Layer A"라는 라벨로 묶여 ANOVA에 들어가는 것은 ω²=0.296의 일부를 "biological pathogen-dependence + curation-protocol heterogeneity"의 혼합으로 만든다. Ch4 §4.1 ll.488–490 sensitivity (HCV 제외 0.246), Ch5 ll.292 (Norovirus까지 제외 0.187, 4 phylo-only 0.137)로 mitigation은 충실하지만, 본문 헤드라인 0.296을 그대로 인용할 때 "20-type granularity 안의 within-design 효과"라는 한정사가 abstract와 ch1에 더 진하게 반영되는 게 좋음.
- 필수 질문: "Layer A의 definitional heterogeneity가 ω²=0.296의 어느 부분을 차지하는지, 11개 pathogen 모두에 동일한 evidence type (예: 모두 phylogenetically-confirmed convergent only)을 강제했을 때의 ω²을 추정할 수 있는가?"
- 답변 완성도: **8/10**. Ch5 ll.292의 4-pathogen phylo-only 분석에서 ω²=0.137이라는 부분 답이 있고 (medium 이상으로 conclusion 유지), Ch5 ll.300–308에서 명시적으로 "method × pathogen interaction이 biology + curation의 혼합임을 인정"한다. 다만 same-evidence-type 11-pathogen subset 재추정은 deferred future work로 남음.
- 종합 코멘트: **logical flow가 잘 짜여 있고 contribution → finding → caveat의 라이프사이클이 일관**. 다만 "MutBench는 hotspot detection benchmark"라는 framing은 ch1에서는 강하게 주장되나 (ll.142 "broadest region-level hotspot-detection benchmark to date") ch5/ch6에서는 "single-position 11-pathogen 안의 within-design 결과"로 톤다운되는 비대칭이 있다. abstract에 "single-position regime, 11 RNA viruses" 한정 어구를 한 번 더 명시하는 게 위원장 시각에서는 안전.

---

### 교수 2 (지도교수, CS/SE) — 재현성 + 일관성

- 점수: A=8, B=8, C=7, D=8, E=8, F=7, G=8, H=8, I=8, J=8, 평균=**7.8**
- 강점: **재현성 인프라가 학위논문 표준을 상회**. Ch3 §3.2.5 ll.902–904 (random seed 42, library 버전 pinning, Python/NumPy/SciPy/IQ-TREE/HyPhy/ESM-2 명시), Ch6 §code_availability ll.96–107 (GitHub tag, Zenodo DOI, 25-second reproducibility for 8,580-evaluation grid), Ch6 §numerical_artifacts ll.109–118 (CSV-to-table-cell provenance manifest)이 일관되게 갖춰져 있음. v144→v148 trajectory에서 P0 9건이 모두 닫혔고 LaTeX errors 0, 86/86 PASS는 SE 시각으로 좋은 신호.
- 약점: **검증·테스트 분리의 약점**. 8,580-evaluation grid는 단일 seed (42), 단일 GISAID snapshot, 단일 codebase로 산출 (Ch5 ll.287 "single team using a single codebase against a single GISAID snapshot"). independent reproduction이 Priority 5로 deferred되어 있어 — Bailey 2018 PanCancer reproducibility audit과의 비교 (Ch5 ll.287)가 적절하지만, 학위논문 수준에서 적어도 두 번째 GISAID snapshot에서의 sanity reproduction은 있어야 SE 기준에서 안전.
- 필수 질문: "동일 codebase에서 다른 GISAID snapshot (예: 2025-Q1 vs. Q3)으로 재실행했을 때 ω²=0.296의 변동 폭은? 0.265 oracle-gap이 여전히 동일 부호로 유지되는가?"
- 답변 완성도: **6/10**. Ch4 §subsampling_robustness ll.462–466에 25/50/75/100% subsampling에서 MCC 변동 ±0.002이 있어 within-snapshot 안정성은 확보되었으나, between-snapshot/temporal-replication은 Ch5 §representativeness ll.260–268에서 "future direction"으로 처리. 내부 안정성 ≠ 외부 재현성이라는 SE 구분이 본문에 더 명시되면 좋음.
- 종합 코멘트: 코드/데이터/seed/version/manifest의 4종 세트가 갖춰졌고, 25-second reproducibility는 학위논문 중에서도 우수한 수준. 다만 single-snapshot single-team이라는 구조적 한계는 정직하게 한 번 더 강조하는 게 좋음.

---

### 교수 3 (통계/ML) — ω², LOPO, 다중비교, 검정력 (가장 엄격)

- 점수: A=7, B=8, C=7, D=7, E=7, F=7, G=6, H=8, I=8, J=7, 평균=**7.2**
- 강점: **통계 audit이 모범적**. (1) ω² 계산이 non-partial form (Ch3 Eq. 17, ll.829–831)으로 명시되었고, (2) Type II SS, Cohen tier, effective N 보정 (cluster bootstrap [0.195, 0.333])이 모두 보고됨, (3) ART two-way ANOVA (Ch3 ll.825) ω²=0.277로 distribution-free 보강, (4) Bayesian hierarchical (Ch5 ll.285) ω²_int posterior mean 0.252 [0.188, 0.314], P(>0.14)=0.996로 random-effect-feasibility까지 다룸. **Bonferroni 분모 명시가 P0 수정 후 깔끔**: 780 per-pathogen + 8,580 cross-pathogen footnote (Ch3 ll.826).
- 약점: **LOPO 0/11의 통계적 위치 자체**. Ch4 ll.442–446에서 P0 수정으로 "permutation null P≈0.96 → null-consistent corroboration"으로 격하되었지만, abstract (l.10 "LOPO 0/11 alone is null-consistent")와 ch1 ll.145 "LOPO 0/11 is reported as null-consistent corroboration"까지 톤다운이 일관됨에도 불구하고, **0.265 oracle-vs-generalized gap의 통계적 유의성도 약함** (Ch4 ll.445 "one-sided p≈0.25–0.28, only 0.4–0.6 SD above null"). 즉 LOPO-기반 두 통계 (match rate, gap) 모두 약하다는 사실은 정직하게 적혀 있으나, 결과적으로 contribution 2의 evidential weight는 ANOVA interaction + HIV-1 escape audit 두 다리에 거의 모두 실린다. 통계 시각에서 이 두 다리가 모두 cluster-bootstrap CI [0.195, 0.333] (ω²)와 Bonferroni p_adj≈3.9×10⁻⁹ (HIV-1 novel-only)으로 충분히 안정적이라는 점은 인정.
- 필수 질문: "8,580 evaluations에서 effective independent unit이 3,080 cells (또는 11 pathogens)에 가깝다는 점을 인정한다면, 헤드라인 ω²=0.296 자체를 evaluation-level에서 cell-level (0.234)로 demote하지 않는 이유는? 그리고 cluster bootstrap 11 clusters는 wild-cluster bootstrap (Cameron 2008)이 권장되는 G≤30 영역인데, 본문 (Ch4 ll.489)에서 percentile bootstrap을 채택하면서 small-cluster anti-conservatism caveat을 적은 것 외에 추가 sensitivity는?"
- 답변 완성도: **7/10**. Ch4 ll.487–489에 cell-level (3,080) 기재와 cluster bootstrap 채택 근거, ll.489 wild-cluster recommendation as future work까지 명시되어 있어 통계적 honesty는 충분. 다만 "헤드라인을 0.234로 demote할까 아니면 0.296을 유지할까"의 결정이 fully principled하기보다는 reporting convention 선택임 — defense에서 압박 가능.
- 종합 코멘트: **post-P0의 통계 honesty는 학위논문 표준을 상회**. LOPO를 "null-consistent corroboration"으로 명시적으로 격하한 것, ART/Bayesian/ANCOVA/cluster-bootstrap 4중 cross-check, winner's curse (Ch5 ll.283) 인정, 모두 좋음. Lenient 기준 통과지만 strict 기준에서 G=6은 "통계 자체는 견고하나 그것을 surveillance에 즉시 deploy 가능한 evidence로 보기엔 약하다"는 의미.

---

### 교수 4 (계산생물학) — 데이터 규모, 결과 해석

- 점수: A=8, B=7, C=7, D=7, E=7, F=7, G=7, H=8, I=8, J=7, 평균=**7.3**
- 강점: **per-pathogen biological rationale의 깊이**. Ch4 ll.314–327에서 11개 pathogen 각각의 best scoring 선정 이유 (HIV-1 entropy/quasispecies, Norovirus homoplasy/epochal evolution, SARS-CoV-2 Tranception/shallow phylogeny, MERS freq/sparse data)가 evolutionary biology 메커니즘과 연결됨. 단순 "ω²=0.296" 보고에 그치지 않고 mechanism으로 한 단계 더 들어간 점이 계산생물학 시각에서 좋음. **Layer A vs Layer C ranking divergence** (Table~\ref{tab:layer_a_vs_c}) — 6개 DMS pathogen 모두에서 best scoring이 다르고, ρ_A,C가 두 개만 유의 — 는 evolutionary fitness ≠ functional fitness라는 학습 포인트로 해석되어야 한다는 본문 (Ch4 ll.553–554)이 적절.
- 약점: **DMS Layer C가 6/11에 그치고, 그중 phenotype heterogeneity도 큼** (Ch3 Table~\ref{tab:dms_preprocessing} ll.327–337: pseudovirus entry vs. authentic replication; HEK293T vs. MDCK vs. TZM-bl). ranking이 "stable across 15–25%"라는 sensitivity (Ch3 ll.317)는 좋지만, cross-pathogen의 Layer C 비교가 그 자체로 apples-to-oranges. EV-A71 RD-cell replicative fitness와 SARS-CoV-2 HEK293T pseudovirus entry가 Layer A vs Layer C divergence의 메커니즘 설명에 들어가야 더 설득력 있음.
- 필수 질문: "Layer C가 6 pathogens에서 정의되지만 phenotype (entry vs. replicative fitness)과 cell line이 모두 다른데, Table~\ref{tab:layer_a_vs_c}의 'Layer A vs Layer C divergence'를 'evolutionary vs functional dimension'으로 일반화할 때, 그 divergence 중 어느 정도가 phenotype heterogeneity로 설명되는가?"
- 답변 완성도: **7/10**. Ch3 ll.319–344 Table~\ref{tab:dms_preprocessing}와 ll.342의 sensitivity sweep 노트가 phenotype heterogeneity를 직시하고 있고, Ch5 ll.328–329 PLM/structure data quality heterogeneity까지 인정. 다만 "phenotype heterogeneity가 ranking divergence의 어느 정도를 설명하는가"의 정량적 분해는 본문에 없음 — defense에서 압박 가능.
- 종합 코멘트: 11 pathogen의 evolutionary diversity를 잘 활용했고, biological mechanism과 statistical finding이 한 번씩 짝지어진다는 점은 학위논문 수준의 성숙도. cross-pathogen interpretation의 honesty도 좋음.

---

### 교수 5 (바이러스/공중보건) — 실용성, 실제 surveillance 적용

- 점수: A=8, B=7, C=7, D=7, E=7, F=7, G=7, H=8, I=8, J=7, 평균=**7.3**
- 강점: **Ch5 §practical_workflow (ll.206–245)의 실무 운용 가이드**. Step 1 (sequence collection ≥200, MAFFT 5분), Step 2 (frequency seconds → homoplasy 2–5분 → ESM-2 GPU 3–5분 → structure optional), Step 3 (Table~\ref{tab:scoring_recommendation} family-level prior로 Coronaviridae→PLM, Orthomyxoviridae→FUBAR), Step 4 (KDE/Wavelet default, 39-detector grid 25초). RTX 3090 1대로 15–20분/pathogen이라는 구체적 자원 요구도 보고. Nextstrain/GISAID와의 통합 경로 (Ch5 ll.192) 명시. surveillance 시각으로 deploy 가능 수준의 specificity.
- 약점: **현장 적용 검증의 부재**. (1) 모든 결과는 retrospective — 2024년 12월까지 GenBank snapshot 기반, time-forward validation (예: 2025년 신변종 출현 시 MutBench가 실제로 hotspot 후보를 사전 예측할 수 있었는가)이 없음. (2) Table~\ref{tab:scoring_recommendation} (Ch5 ll.220–237)이 "starting prior"이라고 명시되었지만 6개 family-level recommendation 모두 단일 pathogen 사례에서 도출되었음 — Coronaviridae=PLM은 SARS-CoV-2 1개, Orthomyxoviridae=FUBAR는 H3N2 1개 (Influenza B는 freq, 본문에 명시되어 있으나 prior table은 family 레벨로 단순화). 이는 surveillance practitioner가 신변종에 적용할 때 "내 virus가 정말 family prior에 fit하는가"를 판단하기 어렵게 만듦.
- 필수 질문: "신변종 (예: 2024년 mpox clade Ib, 또는 가상의 새 RNA virus)에 MutBench를 적용할 때, family-level prior가 우연히 적합하지 않은 경우 (예: family 내 같은 surface protein인데 sub-clade마다 selection regime이 다른 경우)를 진단할 수 있는 internal check가 있는가?"
- 답변 완성도: **6/10**. Ch5 ll.218 "treat the recommended category as a first-pass prior, not as a general algorithmic rule"과 ll.234–235 "evaluate additional categories whenever computational resources permit"이 정직한 면피를 제공하지만, "신변종 sanity check" 자체는 본문에 없음. PAHD-R의 Core/Augmented/Review 3 mode (Ch4 ll.940–948)가 부분 답이지만 9-pathogen panel 한정.
- 종합 코멘트: workflow는 deploy 가능 수준으로 정리되어 있고 dual-use considerations (Ch6 ll.94)도 적절. surveillance 실용성은 G=7로 타당.

---

### 교수 6 (VEP/PLM 전문가) — EVE/EVEscape/ProteinGym 비교 공정성 (최엄격)

- 점수: A=7, B=8, C=6, D=7, E=7, F=6, G=6, H=7, I=8, J=7, 평균=**6.9**
- 강점: **Concurrent benchmark (ProteinGym v1.3, EVEREST v3, ViroGym 2026)와의 task-orthogonality 명시**. Ch2 ll.161–165 (per-mutation regression vs per-region detection, general VEP vs viral, prediction ranking vs interaction quantification 3개 축으로 differentiation), Ch5 ll.181–184 ("a fair head-to-head would require task-aligned binarization, so it remains future work")가 "비교 안 한 게 도피가 아니라 task-orthogonal이라서"라는 입장을 견고하게 만든다. EVEREST가 "PLM이 alignment-based보다 underperform"이라고 보고한 것을 MutBench가 RSV (ESM-2 best), SARS-CoV-2 (Tranception best) 2/11에서 PLM이 winning이라고 보고하는 차이에 대한 reconciliation (Ch5 ll.277)도 정직.
- 약점: **여기서 두 개의 큰 약점이 있음**:
  1. **EVEscape composite와 Tranception은 둘 다 "proxy"로 구현됨** (Ch3 ll.623 "Tranception scoring channel is computed using ESM-2 masked-marginal pseudo-perplexity as a lightweight proxy"; Ch3 ll.628 "EVEscape composite ... substitutes the ESM-2 masked-marginal score for the original EVE fitness term"). 즉 MutBench의 "Tranception"과 "EVEscape"는 원본 모델이 아니다. SARS-CoV-2의 best scoring이 "Tranception"이라는 결과 (Ch4 Table~\ref{tab:stage2_best})는 사실상 "ESM-2 pseudo-perplexity" 결과이고, 이것은 ESM-LLR과 분리된 채널처럼 보고된다 (Ch3 Table~\ref{tab:scoring_types} ll.596). PLM 전문가 시각에서 이 두 channel의 실질적 독립성이 의문 — Ch5 ll.624 "absolute values differ"라는 caveat가 있지만, SARS-CoV-2의 winning이 진짜 autoregressive vs masked-marginal 차이를 잡은 것이 아니라 normalization/aggregation 차이일 수 있음.
  2. **Contribution 1의 "broadest region-level hotspot-detection benchmark to date"** (Ch1 ll.142)이 ViroGym (13 viruses, Mar 2026)이 더 큰 virus count임을 인정한 후에도 ("region-level hotspot-detection"이라는 task qualifier로 distinguishing) 유지된다. 이 distinguishing은 fair하지만 originality는 약화 — 따라서 F=6.
- 필수 질문: "Tranception channel과 EVEscape composite channel이 모두 ESM-2 masked-marginal을 internal로 사용한다면, SARS-CoV-2가 'Tranception best'라는 결과는 ESM-2 channel과 어떻게 분리되어 해석되는가? 진짜 autoregressive vs masked-marginal 차이를 검증하려면 원본 Tranception inference가 필요하지 않은가?"
- 답변 완성도: **5/10**. Ch3 ll.623–625에 proxy 사용 사실은 명시되었으나, "proxy 결과를 본문에서 'Tranception'으로 부르는 것의 적절성"과 "ESM-2 masked-marginal과의 구분 가능성"에 대한 통계적 검증 (예: Spearman ρ between Tranception-proxy column and ESM-LLR column on SARS-CoV-2)이 본문에 없음 — 두 channel이 거의 동일하다면 SARS-CoV-2의 best=Tranception은 실질적으로 best=ESM-LLR과 같다고 봐야 함.
- 종합 코멘트: VEP/PLM 시각에서 가장 엄격하게 보면 (a) Tranception/EVEscape proxy의 채널 분리 검증이 부족하고, (b) ProteinGym/EVEREST와의 task-orthogonality 주장은 fair하지만 그것이 곧 "broadest"의 근거는 아님. 평균 6.9는 strict 기준 (≥7)에 미달이지만 9 항목 중 어떤 것도 5 이하가 아니라서 lenient에서는 통과. defense에서 가장 까다로운 질문이 이 교수에게서 나올 가능성 큼.

---

### 교수 7 (벤치마크 방법론) — benchmark scope, ground truth 정의

- 점수: A=8, B=7, C=7, D=7, E=7, F=8, G=7, H=8, I=8, J=7, 평균=**7.4**
- 강점: **Weber 2019 / Mangul 2019 / Boulesteix 2017 neutral benchmarking 3원칙**을 Ch2 ll.225–227에서 명시 인용하고, Ch2 ll.227 "MutBench adheres to these principles by evaluating all methods—including the author's own MutClust—under identical conditions"로 self-assessment bias를 직접 언급. 9 pathogens × 20 scoring × 14 families × 39 variants의 factorial design 자체가 benchmark methodology 시각에서 정합. Table~\ref{tab:benchmark_comparison} (Ch2 ll.262–283)로 ProteinGym/EVEREST/ViroGym/Bailey 2018과의 5×6 비교 매트릭스를 제공하는 것도 모범.
- 약점: **3-pathogen vaccine-escape validation의 "convenience sample" 성격**. Ch4 ll.895–917 Table~\ref{tab:escape_availability}가 8 pathogens 각각에 대해 escape data 부재 이유를 정리한 것은 정직하지만, 결과적으로 contribution 3b의 "external validation"은 HIV-1 단일 anchor에 의존 (3-tier rule: HIV-1 primary, H3N2 self-consistency, SARS-CoV-2 exploratory). benchmark methodology 시각에서 단일 anchor는 "demonstration"이지 "validation"이 아님 — 3a (multi-source integration infrastructure)와 3b (external validation)을 분리한 P0 수정은 좋지만, 3b가 "anchored on HIV-1"이라는 단서가 ch1 ll.150과 abstract ll.11에 한 번 더 진하게 들어가야 함.
- 필수 질문: "11 pathogens 중 vaccine-escape validation이 가능한 pathogen이 3개로 제한된 상황에서, 'cross-pathogen benchmark'와 'cross-pathogen external validation'이 다른 scope임을 명시했는가? Contribution 3b의 evidential weight가 본질적으로 single-pathogen (HIV-1) anchor에 실린다는 사실이 abstract/ch6에 적절히 demoted 되었는가?"
- 답변 완성도: **8/10**. abstract ll.11 ("HIV-1 is the primary anchor"; "validation is restricted to 3/11 pathogens"), Ch1 ll.150 ("anchored on HIV-1", "self-consistency check", "exploratory"), Ch4 ll.890–891 (Bonferroni 분모 명시), Ch5 §three-tier_evidence_rule ll.174–179, Ch6 ll.15가 모두 일관되게 demoted를 표현. P0 수정의 가장 잘 된 부분 중 하나.
- 종합 코멘트: benchmark methodology 시각에서 design은 정합하고, post-P0의 demotion이 일관됨. F=8은 "broadest region-level hotspot-detection benchmark"라는 originality 주장이 task-qualified로 fair한 점에 따른 것.

---

### 교수 8 (역학 실무자) — 현장 적용 가능성 (Strict)

- 점수: A=7, B=6, C=7, D=6, E=7, F=7, G=6, H=7, I=8, J=7, 평균=**6.8**
- 강점: **dual-use considerations** (Ch6 ll.94)이 명시됨 — raw GISAID redistribution 금지, region-level rankings only (variant-level engineering recipe 아님), HHS P3CO/Select Agent biosafety review 통합. 역학 실무자 시각에서 이 단락은 학위논문 중 우수한 수준. Ch5 ll.190–192 SARS-CoV-2 generation time 5d, sequence submission delay 14d, minimum 4-week TC-freq alert window 등 timing이 구체적.
- 약점: **현장 적용성이 본질적으로 제한됨**. (1) 11 pathogens은 모두 surface protein 단일 (Spike, HA, gp120, F, E, VP1) — surveillance 실무에서 internal protein (NSP, polymerase) hotspot은 drug resistance에 critical하지만 benchmark scope 외 (Ch5 ll.314–319). (2) RNA virus only (Ch5 ll.317), DNA virus extension은 future work. (3) **time-forward / prospective validation 부재** — 모든 결과가 retrospective snapshot 기반. surveillance가 "지금 이 시점에 다음 mutation을 예측"하는 prospective 작업인 만큼, 본문의 "vaccine escape enrichment 7.19×"는 이미 알려진 escape position을 retrospective enrichment한 결과지 prospective 발견이 아님. (4) PAHD-R Core/Augmented/Review 3 mode (Ch4 ll.940–948)는 deployment-ready로 가는 한 걸음이지만 9-pathogen panel 한정이라 "candidate"로 남음 (Ch6 ll.73).
- 필수 질문: "MutBench가 retrospective enrichment에서 prospective surveillance로 가려면 어떤 trigger condition이 필요한가? 현재 panel에서 time-stratified holdout (예: 2024 이전 데이터로 학습/선택, 2024 이후로 검증)이 가능한 pathogen이 있는가?"
- 답변 완성도: **6/10**. Ch5 §temporal_window_dependence ll.265–268에서 SARS-CoV-2 6-month window 분석으로 frequency AUC 0.337→0.472 (2020-H1 → 2021-H1), entropy 0.328→0.507의 temporal drift는 보고됨. 즉 time-stratification이 필요하다는 인식은 있으나, "prospective validation"으로의 명시적 trigger condition (예: "이 정도의 ω² stability가 확보된 pathogen만 deploy")은 본문에 없음.
- 종합 코멘트: 역학 실무자 시각에서 strict (≥7) 기준에 약간 미달 (B=6, D=6, G=6). lenient에서는 통과하지만 "현장 deploy ready"가 아니라 "deploy를 위한 reference benchmark"라는 framing이 abstract/ch1에 한 번 더 들어가는 게 안전. P1 항목 중 prospective validation pilot이 가장 우선순위.

---

### 교수 9 (통계유전학) — 인과 추론, 회로성

- 점수: A=7, B=7, C=7, D=7, E=7, F=7, G=6, H=8, I=8, J=7, 평균=**7.1**
- 강점: **circularity audit이 학위논문 수준에서 가장 충실한 부분**. Ch5 §3.3 ll.30–37 — Layer A membership과 per-position frequency의 point-biserial correlation을 11-pathogen 모두 측정 (mean |ρ|=0.12, range [-0.06, +0.33]; HCV/Influenza B/Norovirus 0.23–0.33 vs. SARS-CoV-2/MERS/EV-A71 ≈0). 이는 "benchmark이 frequency-favoring하게 circular"라는 의심을 정량적으로 응답한 것. Ch4 ll.920–921 Layer A/escape overlap (HIV-1 18%, SARS-CoV-2 60%, H3N2 69%)도 명시. **3-tier evidence rule** (Ch5 ll.174–179)은 통계유전학의 표준적 cleanliness 기준 (Bonferroni survival × Layer A independence)을 직접 적용한 것.
- 약점: **인과 vs 상관 분리의 약점**. (1) ω²=0.296 interaction이 "scoring × pathogen" but "pathogen"은 biological pathogen + curation protocol + sequencing depth + protein length + Layer A density의 confounded composite (Ch3 ll.770–771 "the 'pathogen' factor in the ANOVA is therefore a composite variable"). Ch5 ll.290 ANCOVA로 length/positive-rate adjustment 후 0.234→0.264로 오히려 증가하는 결과 (이게 confounding이 아니라 진짜 interaction이라는 증거)는 좋지만, 모든 confounder를 동시 control한 mediation analysis는 없음. (2) **Random Forest CV가 position-level 5-fold** (Ch4 ll.685 footnote)으로 spatial autocorrelation leakage 주의 명시 — 즉 RF CV AUC 0.742 (Table~\ref{tab:rf_cv_auc})는 generalization estimate가 아닌 "feature complementarity illustration"으로 demoted. 이것은 정직한 demotion이지만, 결과적으로 "10 features가 4-feature core로 압축 가능하다"는 contribution 3a의 base는 RF가 아닌 EqualWeight LOPO + paired-test 부재의 numerical equivalence (97.6%). 통계유전학 시각에서 이 demotion이 contribution 3a의 강도를 약화시킨다.
- 필수 질문: "ω²=0.296의 'pathogen' factor가 length, Layer A positive rate, sequencing depth, protein family의 confounded composite임을 ANCOVA로 부분 absorption했는데, length × positive-rate × scoring의 3-way interaction이 instead of biological pathogen-dependence 'data structure-dependence'라는 대안 가설을 reject할 수 있는가?"
- 답변 완성도: **7/10**. Ch5 ll.290 ANCOVA에서 length+positive-rate adjustment 후 interaction이 증가 (0.234→0.264)한다는 결과가 강력한 부분 답. 또한 Ch5 ll.292의 phylo-only 4-pathogen subset에서도 0.137 (medium 이상) 유지가 추가 답. 다만 "data structure dependence"라는 대안 가설을 explicitly reject하는 단락은 본문에 없고 — defense에서 압박 가능.
- 종합 코멘트: circularity audit과 ANCOVA가 통계유전학 시각에서 가장 잘 처리된 부분. RF CV의 demotion이 정직하지만 contribution 3a의 evidence weight를 약화시킨 trade-off가 있음.

---

### 교수 10 (구조생물학) — pLDDT, 구조 분석 정확성

- 점수: A=7, B=7, C=7, D=6, E=7, F=7, G=7, H=8, I=8, J=7, 평균=**7.1**
- 강점: **structural feature heterogeneity의 정직한 인정**. Ch5 ll.295–296 — "pathogens with high-quality experimental structures (e.g., SARS-CoV-2 Spike) may show inflated structural feature importance relative to pathogens relying on predicted structures." 즉 pLDDT/SASA가 SARS-CoV-2에서는 6VSB cryo-EM 기반인데 다른 pathogen에서는 ESMFold prediction이라는 input quality heterogeneity를 명시. Ch4 ll.218 5.92-fold spatial contact enrichment (z=13.34, 1000 permutations)는 SARS-CoV-2의 6VSB 기반 valid한 structural validation. Ch4 §per_feature_auc Table~\ref{tab:per_feature_auc}에서 pLDDT가 H3N2/RSV/Rabies 3개 pathogen에서 best feature, MERS에서는 inverse (AUC=0.162) — 이는 MERS's Layer A가 disordered region에 위치한다는 biological 해석으로 이어지고 (Ch4 ll.679), 구조생물학 시각에서 mechanistically 그럴듯.
- 약점: **AlphaFold/ESMFold 의존도가 큰데 structural quality benchmark이 일관되지 않음**. (1) 11 pathogens 중 어느 것이 experimental structure (PDB), 어느 것이 ESMFold prediction을 사용했는지 본문에 명시적 table 없음 (Ch3 ll.620 SASA preprocessing 노트는 있으나 pathogen별 structure source는 분산). (2) pLDDT inverse (1-pLDDT)가 "low confidence ≈ flexible/disordered"로 사용되는데 (Ch3 ll.591), pLDDT의 본래 의미는 prediction confidence이지 disorder ground truth가 아니다 — pLDDT<50이 disorder의 proxy라는 것은 Wilson 2022 (Ch4 ll.636에 인용)이 있으나, 이 mapping의 cross-pathogen 일관성은 본문에 검증되지 않음. 즉 MERS의 pLDDT AUC 0.162가 진짜 "Layer A=disordered"인지, MERS Spike의 ESMFold prediction quality 자체가 낮은 것인지 분리 안 됨. (3) Ch5 ll.328–329 "controlling for structure source (experimental vs. predicted) in future analyses would strengthen"는 정직한 인정이지만 학위논문에 적절한 sensitivity (예: pLDDT 평균이 낮은 pathogen subset 제외 후 ω² 재추정)는 deferred.
- 필수 질문: "11 pathogens의 structural feature (pLDDT, SASA)가 experimental structure 기반인지 ESMFold prediction 기반인지 정리된 supplementary table이 있는가? MERS pLDDT AUC 0.162가 'Layer A=disordered region'이라는 biological 해석인지, MERS Spike ESMFold prediction quality가 낮은 데서 오는 noise인지 어떻게 분리하는가?"
- 답변 완성도: **6/10**. Ch3 ll.620–621에서 "ESMFold/Shrake–Rupley-derived release"가 main result라는 언급은 있으나 pathogen별 structure source mapping table은 본문에 없고 supplementary로 deferred. MERS-specific structure quality validation도 본문에 없음.
- 종합 코멘트: 구조생물학 시각에서 D=6은 "structural feature input quality가 cross-pathogen 일관되지 않아 conclusion의 일부 (특히 MERS pLDDT inverse)가 robust하지 않다"는 의미. 다만 mechanism 해석은 그럴듯하고, 5.92-fold spatial contact enrichment (SARS-CoV-2 6VSB)는 valid structural validation.

---

## 합격 기준 평가

### Strict 기준 (paper-plan)
- 평균 ≥ 7: 9 항목 평균 7.27 (10 교수 평균) → **PASS**
- 항목별 평균 검사 (각 항목의 10-교수 평균이 ≥7인가):
  - A=7.5 PASS, B=7.3 PASS, C=6.9 **FAIL** (-0.1), D=7.0 PASS, E=7.2 PASS, F=7.1 PASS, G=6.7 **FAIL** (-0.3), H=7.8 PASS, I=8.0 PASS, J=7.2 PASS
- 개별 최저 ≥ 5: 모든 cell이 6 이상 (어느 교수도 어느 항목도 5 이하 채점 안 함) → **PASS**
- 종합: **조건부 PASS** (C=6.9, G=6.7가 strict 7-thresh 미달; 두 항목 모두 0.3 이내 marginal)

### Lenient 기준 (총점)
- 100점 환산 평균 = 7.27 × 10 = **72.7점**
- 등급: **B+** (80 미만; B+ 영역 70–79)
- 합격 (≥80): **FAIL** (lenient 80-thresh 미달, 7.3점차)

**보정 해석**: lenient 80 기준은 "9-item 평균 8.0"을 의미하며 이는 학위논문 표준에서 "우수, 사소한 개선만"에 해당. MutBench는 P0 수정 후에도 G/C에서 6점대 약점이 남아 lenient 통과는 어렵다. **strict 기준으로는 조건부 PASS** (C와 G에서 0.3 이내 marginal miss).

---

## 가장 취약한 항목 TOP 3

1. **G. 실용적 가치 (10-교수 평균 6.7)** — Strict thresh 0.3 미달.
   - 핵심 약점: surveillance/현장 deploy ready가 아니고 retrospective enrichment에 머무름. time-forward / prospective validation 부재. PAHD-R 9-pathogen 한정. Tranception/EVEscape이 proxy 구현이라 PLM 시각에서 deploy 신뢰성 약함.
   - 가장 강하게 감점한 교수: 교수 6 (VEP/PLM, G=6), 교수 8 (역학 실무자, G=6), 교수 9 (통계유전학, G=6), 교수 3 (통계/ML, G=6).

2. **C. 방법론 타당성 (10-교수 평균 6.9)** — Strict thresh 0.1 미달 (marginal).
   - 핵심 약점: ω²=0.296의 effective N 보정 (3,080 cells vs 8,580 evaluations), wild-cluster bootstrap 부재 (G=11<30), single-snapshot single-team reproduction, RF position-level 5-fold leakage (이미 demoted), Tranception proxy의 ESM-LLR과의 분리 검증 부재.
   - 가장 강하게 감점한 교수: 교수 6 (VEP, C=6).

3. **D. 실험 규모/견고성 (10-교수 평균 7.0)** — Strict 통과 (marginal).
   - 핵심 약점: DMS Layer C 6/11 그리고 그중 phenotype heterogeneity (entry vs replicative fitness, cell line 차이). escape validation 3/11 (HIV-1 only 진정 external). 11 pathogens은 ANOVA 표본으로는 small-G. structural feature input quality의 cross-pathogen 비균질.
   - 가장 강하게 감점한 교수: 교수 8 (역학, D=6), 교수 10 (구조생물학, D=6).

---

## 가장 위험한 defense 질문 TOP 3

1. **(교수 6, VEP/PLM) "Tranception channel과 EVEscape composite channel이 모두 ESM-2 masked-marginal을 internal로 사용한다면, SARS-CoV-2의 'best=Tranception' 결과는 ESM-2 channel과 분리되어 해석되는가? Spearman ρ(Tranception_proxy, ESM-LLR) on SARS-CoV-2 column이 0.95 이상이라면 사실상 같은 channel 아닌가?"**
   - 위험도: **HIGH**. 본문에 두 column 간 ρ가 측정되지 않았고, "absolute values differ"만 적혀 있음 (Ch3 ll.624). 이 ρ가 높으면 SARS-CoV-2 best scoring 해석이 흔들림 (Tranception이 진짜 winning이 아니라 ESM-LLR이 winning).
   - Defense 대응: Tranception column과 ESM-LLR column의 SARS-CoV-2 per-position ρ를 즉시 계산하여 보고. 0.85 이상이면 "두 channel은 사실상 같은 정보를 capture하므로 'best=PLM-class'로 해석"으로 demoted. 0.85 미만이면 normalization/aggregation 차이가 의미 있다고 주장.

2. **(교수 8, 역학) "MutBench가 retrospective enrichment에서 prospective surveillance로 가려면 어떤 trigger condition이 필요한가? 현재 panel에서 time-stratified holdout (2024 이전 학습, 2024 이후 검증)이 가능한 pathogen이 있는가?"**
   - 위험도: **HIGH**. 본문에서 가장 약한 부분. SARS-CoV-2 6-month window analysis (Ch5 ll.265–268)는 prospective의 가장 가까운 답이지만 "feature AUC drift"이지 "prospective hotspot prediction"이 아님.
   - Defense 대응: H3N2가 1968년부터 50-year 데이터이므로 2010-cutoff training, 2010–2024 testing이 technically 가능. 그러나 본문에는 없음 → 정직하게 "future work, P1 우선순위"로 인정. PAHD-R Core mode가 prospective deployment의 floor 역할을 한다고 주장.

3. **(교수 3, 통계/ML) "8,580 evaluations에서 effective independent unit이 3,080 cells 또는 11 pathogens에 가깝다는 점을 인정한다면, 헤드라인 ω²=0.296을 cell-level 0.234로 demote하지 않은 이유는? cluster bootstrap 11 clusters는 wild-cluster bootstrap (Cameron 2008)이 권장되는 G≤30 영역인데 percentile bootstrap을 채택한 추가 sensitivity는?"**
   - 위험도: **MEDIUM-HIGH**. Ch4 ll.487–489에 cell-level (3,080) 기재와 wild-cluster recommendation as future work는 적혀 있어 일부 답은 본문에 있음.
   - Defense 대응: 세 가지 reading 모두 large-effect threshold 통과 — evaluation-level 0.296, cell-level 0.234, ANCOVA-adjusted 0.264, Bayesian posterior mean 0.252, HCV-excluded 0.246, 4-phylo-only 0.137 (medium). 즉 "0.296은 upper envelope, 0.234가 conservative point, 0.137이 worst-case lower bound"의 range를 제시. wild-cluster bootstrap은 P1 future work로 인정.

---

## 종합 판정

- **합격 여부**: **조건부 PASS (Strict 기준)**, **FAIL (Lenient 80점 기준)**
  - Strict paper-plan 기준에서: 항목별 평균 ≥ 7 조건이 C=6.9, G=6.7 두 항목에서 0.1–0.3 marginal miss. 그러나 모든 cell이 ≥6, 9 항목 평균 7.27, 평균 등급 B+로 학위논문 통과 수준에는 충분.
  - 학위논문 defense 합격 가능성: **PASS 80%, 조건부 PASS 18%, FAIL 2%**.

- **권장 보강 (defense 전 가능)**: P1 항목 중 다음 4개를 우선 처리.
  1. **Tranception–ESM-LLR per-pathogen ρ supplementary table 추가** (교수 6 대응; 4시간 작업; CSV 1개 + 1-paragraph note in Ch3 §scoring_types).
  2. **Structure source per-pathogen mapping table 추가** (교수 10 대응; 2시간; supplementary table only, 본문 변경 없음).
  3. **Time-stratified holdout 1-pathogen pilot** — H3N2를 2010-cutoff training/testing으로 1회 실행 (교수 8 대응; 1일 작업; ch4 §temporal에 1-paragraph 추가).
  4. **Abstract와 ch1에 "single-position regime, 11 RNA viruses, 20-type granularity" 한정사 명시 강화** (교수 1 대응; 30분; abstract ll.10과 ch1 ll.142 paraphrase).
  - 위 4개 모두 처리하면 G/C 각각 0.3–0.5 점 상승 예상 → strict 기준 완전 통과.

- **최종 코멘트**:
  MutBench는 P0 수정 후 통계 honesty (LOPO null-consistent demotion, ω² range reporting, novel-only Bonferroni, 3-tier evidence rule)와 재현성 인프라가 학위논문 표준을 상회하는 수준으로 정리되었음. 가장 큰 강점은 (1) 8,580-evaluation factorial design의 scale, (2) 3-layer ground truth의 orthogonal dimension 설계, (3) circularity audit과 ANCOVA의 정직성 (interaction이 covariate adjustment 후 오히려 증가). 가장 큰 약점은 (1) Tranception/EVEscape proxy의 channel 분리 검증 부재 (PLM 시각), (2) prospective/time-forward validation 부재 (역학 시각), (3) 4-feature core 97.6%의 paired-test 부재 (이미 정직하게 demoted되었지만 contribution 3a의 evidence weight 약화). HIV-1 single anchor에 contribution 3b가 의존하는 구조는 P0 수정으로 명시적으로 demoted되어 이제는 honest 약점이지 hidden 약점이 아니다. 학위 논문으로서 defense 통과 수준은 **충분**, 그러나 "deploy-ready surveillance benchmark"라는 더 강한 framing을 lenient 80점 기준으로 끌어올리려면 prospective pilot 1건 + Tranception 분리 검증이 필수.
