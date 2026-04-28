# Phase 4 교수 10명 시뮬레이션 (Cycle 3)

작성일: 2026-04-28
대상: v151 (cycle 2-3 ~100건 fix 적용 후)
참조 baseline: cycle 1 phase4_professor.md (평균 7.27, B+)
주요 변경: ch3 9 Critical closed, ch5 sec:prospective_validation_gap + sec:mafft_auto_artifact 추가, Tranception–ESM-LLR ρ=0.64–0.84 collinearity 명시, KR abstract G07/G08 sync, Bonferroni p_adj=3.9e-9 4파일 sync, cell-level 0.234 4-parameterization 모든 챕터 sync, "operationally equivalent" → "non-rejection of inferiority", BibTeX 11개 신규(FEL/SLAC/BUSTED/ESM-3/SaProt/Greaney/Łuksza/Huddleston).

---

## 평가표

| 교수 | 전공 | A | B | C | D | E | F | G | H | I | J | 평균 | 등급 | 비고 |
|------|------|---|---|---|---|---|---|---|---|---|---|------|------|------|
| 1 | 위원장 (생물정보학) | 8 | 8 | 8 | 8 | 8 | 8 | 7 | 9 | 9 | 8 | **8.1** | PASS | "single-position regime, 11 RNA viruses" 한정사 abstract/ch1/ch5 일관, 4-parameterization 진솔 |
| 2 | 지도교수 (CS/SE) | 8 | 8 | 8 | 8 | 8 | 7 | 8 | 9 | 9 | 8 | **8.1** | PASS | provenance manifest + Zenodo + GitHub kksuhj sync, BibTeX 11개 추가 |
| 3 | 통계/ML | 8 | 8 | 8 | 7 | 8 | 7 | 7 | 9 | 9 | 8 | **7.9** | PASS | cell-level 0.234 demote가 ch3/ch4/ch5 sync, wild-cluster 미수행은 정직하게 acknowledge, Bayesian dual run 명시 |
| 4 | 계산생물학 | 8 | 7 | 7 | 7 | 8 | 8 | 7 | 8 | 9 | 8 | **7.7** | PASS | per-pathogen mechanism 해석 그대로 강건, Layer C phenotype heterogeneity는 여전히 현실적 한계 |
| 5 | 바이러스/공중보건 | 8 | 7 | 7 | 7 | 7 | 7 | 7 | 8 | 9 | 7 | **7.4** | PASS | sec:prospective_validation_gap 추가가 G 점수에 정직성 보너스, 그러나 prospective 자체는 여전히 미수행 |
| 6 | VEP/PLM 전문가 | 8 | 8 | 7 | 7 | 8 | 7 | 7 | 8 | 9 | 7 | **7.6** | PASS | Tranception–ESM-LLR ρ=0.64–0.84 명시(HIV-1만 dissociate, ρ=0.04)가 cycle1 6.9 → 7.6, 결정적 회복 |
| 7 | 벤치마크 방법론 | 8 | 8 | 8 | 7 | 8 | 8 | 7 | 9 | 9 | 8 | **8.0** | PASS | broadest qualifier 일관, 3-tier evidence rule 명시, FEL/SLAC/BUSTED 인용 추가가 literature breadth 보강 |
| 8 | 역학 실무자 | 7 | 7 | 7 | 6 | 7 | 7 | 6 | 8 | 9 | 7 | **7.1** | PASS (조건부) | H3N2 2010-cutoff pilot이 ch4에 추가됐으나 frequency-only 1-pathogen 한정 — prospective gap은 여전히 본질적 약점 |
| 9 | 통계유전학 | 8 | 7 | 8 | 7 | 8 | 7 | 7 | 9 | 9 | 8 | **7.8** | PASS | EqualWeight 두 변형 분리 명시(production vs nested-LOPO)가 label leakage 의심 완전 차단 |
| 10 | 구조생물학 | 7 | 7 | 7 | 7 | 7 | 7 | 7 | 8 | 9 | 7 | **7.3** | PASS | structure source mapping은 여전히 본문 미명시(supplementary), MERS pLDDT inverse 해석은 mechanism 그대로 |
| **평균** | — | **7.8** | **7.5** | **7.5** | **7.1** | **7.7** | **7.3** | **7.0** | **8.5** | **9.0** | **7.6** | **7.70** | — | — |
| **최저** | — | **7** | **7** | **7** | **6** | **7** | **7** | **6** | **8** | **9** | **7** | **7.1** | — | — |

---

## 항목별 평균 (cycle 1 vs cycle 3)

| 항목 | 의미 | cycle 1 | cycle 3 | Δ | 핵심 fix |
|------|------|---------|---------|---|----------|
| A. 문제 (problem motivation) | 7.5 | 7.8 | **+0.3** | broadest qualifier 보강, "single-position regime" 한정사 |
| B. 관련 (literature) | 7.3 | 7.5 | **+0.2** | BibTeX 11개 추가(FEL/SLAC/BUSTED/ESM-3/SaProt/Greaney/Łuksza/Huddleston), EVEscape/Livesey 추가 |
| C. 방법론 (methodology) | 6.9 | **7.5** | **+0.6** | EqualWeight 두 변형 분리, cell-level 0.234 4-parameterization, wild-cluster acknowledge, Bayesian dual run |
| D. 규모 (scale) | 7.0 | 7.1 | +0.1 | DMS 6/11 + 11 pathogen 자체는 변화 없음, cycle 3에서는 단순 disclosure 강화 |
| E. 해석 (interpretation) | 7.2 | 7.7 | **+0.5** | circularity audit ch5:33–35 chain화, ranking-discount 명시, novel-only enrichment cross-pathogen 일관 |
| F. 독창 (novelty) | 7.1 | 7.3 | +0.2 | broadest qualifier가 task-orthogonality 명시로 더 fair, 그러나 ViroGym 13 viruses는 여전히 비교 부담 |
| G. 실용 (practical value) | 6.7 | **7.0** | **+0.3** | sec:prospective_validation_gap 추가, H3N2 2010-cutoff pilot 추가 — 그러나 frequency-only 1-pathogen pilot이라 만족도 제한 |
| H. 서술 (writing) | 7.8 | 8.5 | **+0.7** | "operationally equivalent" → "non-rejection of inferiority" 일관, Bonferroni p_adj=3.9e-9 4파일 sync, KR abstract sync |
| I. 한계 (limitation honesty) | 8.0 | 9.0 | **+1.0** | sec:prospective_validation_gap, sec:mafft_auto_artifact, single-team-single-snapshot caveat 일관 |
| J. 완성 (overall completeness) | 7.2 | 7.6 | **+0.4** | cross-chapter consistency, verify_dissertation 90 PASS / 0 FAIL |

**Cycle 1 → Cycle 3 평균**: 7.27 → **7.70** (+0.43, B+ → A−)
**최저 항목 평균**: G=6.7 → **G=7.0** (+0.3, strict 7-thresh 경계 통과)

---

## 가장 위험한 Defense 질문 TOP 3 (cycle 3)

### 1. (교수 8, 역학) — Prospective 1-pathogen pilot의 negative result 해석

**질문**: "ch4 §H3N2 time-stratified pilot에서 frequency-only 학습으로 2016–2020 신변종 6개 중 0개 hit, 2021–2025 7개 중 1개 hit (Fisher p→1)을 보고했는데, 이것은 'frequency alone is prospectively weak' 증거이자 동시에 'MutBench의 prospective signal 자체가 약하다'는 증거이다. multi-source 4-feature core가 prospective enrichment을 유의하게 회복할 수 있다는 evidence는 어디 있는가?"

**위험도**: HIGH. cycle 3가 가장 정직하게 추가한 ch4:198–222의 H3N2 pilot이 의도치 않게 'practical value 약점'을 강화했음. ch5:343에서 "frequency alone retrospectively diagnostic but prospectively weak"으로 frame했으나, 4-feature core의 prospective 검증이 본문에 없음.

**Defense 대응**: 4-feature core prospective re-evaluation을 P1 future work로 인정 + ch5:34의 ranking-discount paragraph에서 "retrospective enrichment values are upper-envelope estimates; prospective magnitudes are expected to be smaller, possibly substantially"로 강화. PAHD-R Core mode가 floor 역할.

---

### 2. (교수 6, VEP/PLM) — Tranception–ESM-LLR collinearity의 contribution-level 영향

**질문**: "ch5:279에서 Tranception–ESM-LLR per-pathogen ρ=0.64–0.84 (Pearson) / 0.71–0.98 (Spearman)이 11 of 12 pathogens에서 측정됐고 HIV-1만 dissociate (ρ=0.04). 그런데 SARS-CoV-2의 'best=Tranception'(MCC=0.534)은 ESM-LLR의 SARS-CoV-2 MCC와 0.02 이내인가? 두 channel이 사실상 같다면 abstract Table에서 'Tranception/ESM-2 channel collinearity is not separated at headline granularity' 단순 disclaimer만으로 충분한가, 아니면 6-카테고리 aggregation처럼 'PLM-class' 단일 channel로 합쳐서 ω²을 재추정해야 하는가?"

**위험도**: MEDIUM-HIGH. cycle 3의 가장 강한 fix(ρ table)가 동시에 새 압박점을 노출. 그러나 abstract:13("Tranception/ESM-2 channel collinearity is not separated at headline granularity; see Chapter ch:mutbench")가 demote를 명시하고, 6-카테고리 0.103 lower bound가 collinearity-robust로 이미 보고됨.

**Defense 대응**: 6-카테고리 0.103을 lower bound로 인용 → 두 channel 합치면 20-type → 19-type이지만 ω² shift는 cluster-bootstrap CI 폭(0.195–0.333) 안에서 흡수됨. SARS-CoV-2-specific에 한해 Tranception-vs-ESM-LLR MCC 차이를 supplementary로 보고할 의향.

---

### 3. (교수 3, 통계/ML) — Wild-cluster bootstrap 미수행의 conservativeness 영향

**질문**: "ch3:959와 ch4:526에서 'wild-cluster bootstrap is queued as deferred future work'로 명시했지만, G=11 cluster에서 percentile bootstrap이 anti-conservative라는 사실 자체가 cluster-bootstrap CI [0.195, 0.333]의 lower bound 0.195를 불안정하게 만든다. ANCOVA 0.264, Bayesian posterior mean 0.252, HCV-excluded 0.199, 4-phylo-only 0.137 중 어느 것이 wild-cluster reasoning 하에 'conservative point estimate'인가?"

**위험도**: MEDIUM. cycle 3가 wild-cluster를 정직하게 acknowledge하고 6 sensitivities(0.137 worst-case)를 모두 보고했지만, 'headline 0.296'을 abstract에 retain한 결정은 reporting convention 선택. 그러나 모든 6개 reading이 Cohen medium 이상이라는 사실이 buffer.

**Defense 대응**: "headline은 evaluation-level 0.296, conservative reference는 cell-level 0.234, lower envelope는 4-phylo-only 0.137; 모두 medium 이상이며 wild-cluster 재추정도 0.137 이하로는 가지 않을 것으로 예상"이 ch3/ch5에 4-parameterization으로 이미 명시됨.

---

## 합격 기준 평가

### Strict 기준 (paper-plan: 평균 ≥ 7, 최저 ≥ 5)

- 9 항목 평균 ≥ 7: 평균 **7.70** → **PASS**
- 항목별 10-교수 평균 검사:
  - A=7.8 PASS, B=7.5 PASS, C=**7.5** PASS (cycle1 6.9 → +0.6 회복), D=7.1 PASS, E=7.7 PASS, F=7.3 PASS, **G=7.0** PASS (cycle1 6.7 → +0.3 정확히 thresh), H=8.5 PASS, I=9.0 PASS, J=7.6 PASS
  - **모든 10개 항목 strict 7-thresh 통과** (cycle1은 C/G 2개 미달 → cycle3는 0개 미달)
- 개별 최저 ≥ 5: 모든 cell ≥ 6 (D=6 두 명: 교수8, 교수10 — Layer C phenotype heterogeneity 한정), G=6 한 명(교수8) → **PASS**
- 종합: **PASS** (cycle1 조건부 PASS → cycle3 unconditional PASS)

### Lenient 기준 (총점 ≥ 80)

- 100점 환산 평균 = 7.70 × 10 = **77.0점**
- 등급: **A−** (cycle1 B+ 72.7 → cycle3 A− 77.0; +4.3점)
- 합격 (≥80): **FAIL** (lenient 80-thresh 3.0점 미달; cycle1보다 4.3점 가까워졌으나 prospective validation 부재가 단일 차단)

### Defense 통과 가능성

- **PASS 92%, 조건부 PASS 7%, FAIL 1%** (cycle1: 80% PASS, 18% 조건부, 2% FAIL → cycle3: +12 PASS pp)
- 차단 위험: 거의 없음. 가장 hostile한 위원이 ch5 sec:prospective_validation_gap을 "honest gap"으로 인정하면 통과.

---

## cycle 1 → cycle 3 trajectory

### 가장 큰 개선 항목 (Top 3)

1. **I. 한계 (limitation honesty): +1.0** (8.0 → 9.0)
   - sec:prospective_validation_gap (4-단락 신규 subsection, ch5:337–343)
   - sec:mafft_auto_artifact (단일 fixed mode 미수행 정직하게 acknowledge, ch5:344–347)
   - single-team-single-snapshot caveat을 ω²/oracle MCC/HIV-1 7.19×에 claim-by-claim로 매핑(ch5:291)
   - 이 점수가 9.0인 것은 학위논문 표준에서 매우 드문 수준

2. **H. 서술 (writing): +0.7** (7.8 → 8.5)
   - "operationally equivalent" → "non-rejection of inferiority within ±0.04 MCC bound" 7곳 일관 demote
   - Bonferroni p_adj=3.9e-9 (abstract/ch1/ch4/ch6) sync, KR abstract도 sync
   - 11/12 panel size 모순 5곳 통일 (ch1:82/106/142/143/150)
   - "broadest" qualifier가 항상 "region-level, single-position hotspot-detection benchmark, 11 RNA viruses"로 한정 노출

3. **C. 방법론 (methodology): +0.6** (6.9 → 7.5) — **cycle1 lowest 항목 정확 회복**
   - EqualWeight 두 변형 분리(ch3:719–724): production(라벨 무관) vs nested-LOPO(라벨 인지하나 cleanly held-out) — label leakage 의심 차단
   - cell-level 0.234 / ANCOVA 0.264 / Bayesian 0.252–0.319 4-parameterization을 ch3:917–921 + ch4:425 + ch5:285–290 일관 보고
   - wild-cluster bootstrap acknowledge(ch3:959, ch4:526) — anti-conservativeness 정직하게 명시
   - Bayesian dual run(exploratory + archived) 명시(ch5:289)

### 잔여 약점 (Top 3)

1. **G. 실용 (practical value): 7.0 — strict thresh 경계** (cycle1 6.7 → cycle3 7.0; +0.3)
   - sec:prospective_validation_gap이 honest disclosure이지만 prospective evidence 자체는 여전히 부재
   - H3N2 2010-cutoff pilot은 frequency-only 1-pathogen이라 contribution 강도 제한
   - PAHD-R Core/Augmented/Review 3 mode는 9-pathogen panel 한정 (변화 없음)

2. **D. 규모 (scale): 7.1** (cycle1 7.0 → cycle3 7.1; +0.1)
   - DMS Layer C 6/11 phenotype heterogeneity는 여전히 현실적 한계 (cycle 3 fix 무관)
   - 11 pathogens은 ANOVA 표본으로 small-G (Bolker minimum 통과, typical 미달) — 정직 명시되었으나 본질 변화 없음
   - structural feature input quality cross-pathogen 비균질 (교수10 — pathogen별 structure source mapping이 여전히 supplementary로만 deferred)

3. **F. 독창 (novelty): 7.3** (cycle1 7.1 → cycle3 7.3; +0.2)
   - "broadest region-level hotspot-detection benchmark" task-qualified로 fair하지만 ViroGym(13 viruses)이 더 큰 virus count
   - cycle 3는 task-orthogonality 명시 강화로 buffer를 추가했으나 originality 자체는 여전히 task-qualified

---

## cycle 1 lowest scores 항목 회복 분석 (요청된 핵심 질문)

### G (practical value): 6.7 → 7.0 (+0.3)

**얼마나 회복?**: 부분 회복(strict 7-thresh 경계 통과). cycle 2 fix가 G를 직접 겨냥했으나 prospective validation 자체의 부재가 단일 ceiling.

**기여 fix**:
- sec:prospective_validation_gap 4-단락 신규 (ch5:337–343): 정직성으로 -0.5 → -0.2 (펜티 완화)
- ch4:198–222 H3N2 2010-cutoff pilot: deploy-readiness signal +0.2
- ch5:192 "no production-grade integration is claimed"로 forward-looking 톤다운: +0.1
- 합계 약 +0.3 회복

**남은 ceiling**: prospective 4-feature core re-evaluation 미수행(P1 future). 이것이 해소되어야 G≥8 가능.

### C (methodology): 6.9 → 7.5 (+0.6)

**얼마나 회복?**: 거의 완전 회복(strict 7-thresh 0.5 여유로 통과). cycle 1에서 가장 큰 우려였던 EqualWeight label leakage / wild-cluster bootstrap / cell-level vs evaluation-level이 모두 본문 명시 단계로 격상.

**기여 fix**:
- EqualWeight 두 변형 분리(ch3:719–724): label leakage 의심 -0.5 → 0 (완전 차단) 
- cell-level 0.234 4-parameterization 모든 챕터 sync (ch3:917, ch4:425, ch5:285–290): -0.3 → 0 (완전 sync)
- wild-cluster bootstrap acknowledge(ch3:959, ch4:526): -0.2 → -0.1 (acknowledge로 펜티 완화)
- Tranception–ESM-LLR ρ table(ch5:279, Table tab:tranception_esm_correlation): -0.3 → -0.1 (channel separation 한정 acknowledge)
- 합계 약 +0.6 회복

**남은 ceiling**: wild-cluster bootstrap 실제 재추정 + Tranception-vs-ESM-LLR contribution-level 분리 분석 두 건이 P1으로 남음. 두 건 처리 시 C≥8 가능.

---

## 최종 판정

- **결과**: **PASS (Strict 기준 unconditional PASS, Lenient 80점 기준 FAIL but A− 등급)**

- **판정 근거**:
  1. **Strict**: 평균 7.70(cycle1 7.27, +0.43), 항목별 평균 모두 ≥7(cycle1 C/G 2개 미달 → cycle3 0개 미달), 최저 cell 6(cycle1과 동일, 어느 교수도 5 이하 채점 안 함). 9 항목 평균 ≥7 + 항목별 최저 5 이상 두 조건 모두 통과.
  2. **Lenient**: 77.0점(cycle1 72.7, +4.3). 80점 기준에는 3점 미달. 그러나 학위논문 defense 합격에는 strict가 표준이며, lenient 80점은 "우수, 사소한 개선만"의 A0/A+ 영역 — A− 77.0은 통과 영역.
  3. **Defense 통과 가능성**: 92% PASS / 7% 조건부 / 1% FAIL (cycle1 80/18/2 → cycle3 92/7/1, +12 pp PASS).
  4. **cycle 1 lowest 항목 회복**: G 6.7 → 7.0(+0.3, strict thresh 정확 통과), C 6.9 → 7.5(+0.6, strict thresh 0.5 여유 통과). **두 항목 모두 회복**, 특히 C는 정확히 cycle1에서 가장 우려됐던 EqualWeight label leakage / cell-level demote / wild-cluster acknowledge 세 fix가 모두 본문에 anchor됨.

- **다음 액션**:
  - **defense 진행 권장**. cycle 3 추가 수정 없이도 통과 가능성 92%. 특히 ch5 sec:prospective_validation_gap이 "honest gap" disclosure로 G 점수의 ceiling을 정직성 보너스로 상쇄.
  - **선택적 P1 보강** (defense 전 가능, 통과 확률 92→95%):
    1. Tranception-vs-ESM-LLR per-pathogen MCC delta supplementary table (교수6 대응; 2시간; ch5:279 paragraph 1 sentence 추가).
    2. 4-feature core 4-pathogen prospective pilot (H3N2 2010-cutoff에 4-feature 추가; 1일; ch4 §198 paragraph 확장). 이것이 처리되면 G≥7.5 가능.
    3. structure source per-pathogen mapping table을 본문에 backport(현재 supplementary; 교수10 대응; 2시간).
  - **lenient 80점 도달**(A 등급)에는 위 3건 중 #2(prospective 4-feature pilot)가 단일 결정타. 그러나 defense 통과 자체에는 불필요.

- **종합 코멘트**:
  cycle 1 phase 4의 두 결정적 약점(C=6.9, G=6.7)이 cycle 2-3 ~100건 fix를 통해 정확히 회복됐다. 특히 C(방법론)는 cycle 1에서 EqualWeight label leakage / cell-level demote / wild-cluster bootstrap 세 우려가 모두 본문 anchor 단계로 격상되어 +0.6 회복(strict thresh 0.5 여유로 통과); G(실용)는 sec:prospective_validation_gap 정직 disclosure + H3N2 pilot 추가로 +0.3 회복(strict thresh 경계 통과). I(한계 정직성)는 9.0으로 학위논문 표준에서 매우 드문 수준이며, cycle 1에서 이미 8.0이었던 강점이 cycle 2-3 fix를 통해 "가장 큰 강점"으로 더욱 성숙. cycle 3 가장 위험한 defense 질문 3건(prospective 1-pathogen 한정, Tranception–ESM-LLR contribution 분리, wild-cluster 미수행) 모두 본문에 partial answer가 있고, 위원이 Question을 던졌을 때 본문에 "we acknowledge this and queue as future work" 명시 anchor가 존재. defense 통과는 **정량적·정성적으로 모두 충분**하며, 추가 fix 없이도 92% PASS가 합리적 추정.
