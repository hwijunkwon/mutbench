# Codex IV&V 종합 보고서 (외부 검수)

대상: cycle 1~3 검수·수정 결과의 외부 IV&V (independent verification & validation)
실행: 5단계 codex 점검 (C1~C5) 병렬 후 종합
산출물: `codex_ivv/codex_{C1~C5}.md` + 본 종합 (`codex_C0_synthesis.md`)

---

## 1. 5단계 codex 점검 결과 요약

| Step | 점검 대상 | 결과 | 핵심 발견 |
|------|---------|------|---------|
| **C1** | 113건 fix verbatim 무작위 10건 | **10/10 PASS** | self-confirmation bias 낮음, 보고서 모두 under-claim 방향 |
| **C2** | LaTeX 라벨/cross-ref hygiene | **PASS (zero error)** | 7 신규 라벨 모두 정의·resolve, 11 신규 BibTeX 정합 |
| **C3** | Phase 4 7.70 (A-) fairness | **bias 중간** | 점수 0.25 inflated → 외부 7.45, defense 92% → 85-88% |
| **C4** | 외부 적대적 새 공격 | **20건 신규 결함** | cycle 1-3가 공유한 8 blind spot 발견 |
| **C5** | 1시간 hostile defense rehearsal | **조건부 PASS 다수결** | 첫인상 6.5/10, defense 84-88%, prospective 부재가 가장 위험 |

---

## 2. 핵심 발견 (cycle 3 self-evaluation 보정)

### 2.1 cycle 3 자체 평가 vs codex IV&V 보정

| 차원 | Cycle 3 자체 | **Codex IV&V 보정** | Gap |
|------|------------|------------------|-----|
| Phase 4 평균 점수 | **7.70 (A-)** | **7.45** | 0.25 inflated |
| Strict 합격 | unconditional PASS | **조건부 PASS** (G=7.0 thresh 경계) | downgrade |
| Lenient 80점 | 77.0 (FAIL, A-) | 74.5 (FAIL, B+) | downgrade |
| Defense 통과 % | **92%** | **84-88%** (4-8pp 낮음) | overstated |
| 신규 결함 | 0건 | **20건 (Critical 1, Major 9, Minor 10)** | 공유 blind spot |
| Fix verbatim | 113건 적용 | **10/10 PASS 검증** | confirmed |
| LaTeX hygiene | OK | **PASS (2 orphan label only)** | confirmed |

### 2.2 가장 inflated된 Phase 4 항목 (C3 진단)

| 항목 | Cycle 3 자체 | **외부 보정** | 진단 |
|------|------------|------------|------|
| **I. 한계** | 9.0 | **8.5** | 학위논문 매우 드문 9.0은 self-favoring 신호 |
| **H. 서술** | 8.5 | **8.1** | wording sync로 +0.7 한 등급 격상 evidence 부족 |
| **C. 방법론** | 7.5 | **7.3** | wild-cluster acknowledge(미수행)는 +0.0이어야 |
| **G. 실용** | 7.0 | **6.8** | prospective evidence 0건이고 H3N2 pilot은 negative result(0/6, 1/50) |

**근본 원인**: cycle 3 phase 4 시뮬레이터가 cycle 2-3 fix 목록을 미리 알고 있어 disclosure inflation 발생. 같은 페르소나가 cycle 1에서 엄격하게 -0.6 깎았던 항목을 cycle 3에서 honest disclosure 하나로 +0.7 회복시킴 → 페르소나 일관성 약함.

---

## 3. C4 신규 발견 결함 — 20건 blind spot

cycle 1-3 검수가 **8 차원**에서 점검 자체를 안 했음:

### 3.1 Critical 1건

| ID | 결함 | defense 차단 위험 |
|----|------|----------------|
| **M1** | Tranception/EVEscape/EVEREST score 사용 시 라이선스 명시 부재 | **있음** (DURC + 저작권 위반 동시) |

### 3.2 Major 9건

| ID | 결함 |
|----|------|
| M2 | GenBank query (terms, dates, filter)가 본문에 부재 — Cutoff date만 명시 |
| M3 | 8580 evaluation 중 worst-MCC detector·scoring 조합 비공개 |
| S1 | Mantel test (distance matrix correlation) 미사용 |
| S2 | F1·AUROC가 본문에 등장하지만 헤드라인 MCC 선택 정당화 부재 |
| D1 | Influenza B Vic vs Yam 분리 부재 |
| D3 | SARS-CoV-2 Omicron 시점 score 분석 부재 |
| E1 | DURC (Dual Use Research of Concern) 명목 검토 부재 |
| G1 | "MutBench" 명사 vs "RNA-virus only" 한정사 — generalization scope mismatch |
| C1 | CD-HIT·MMseqs2 (sequence clustering) 사용 시 인용 부재 |

### 3.3 Minor 10건

| ID | 결함 |
|----|------|
| S3 | Bootstrap 외 jackknife 측정 부재 |
| D2 | HIV-1 group M vs O 분리 |
| D4 | HCV genotype 1 vs 3 분리 |
| E2 | DMS 데이터 사용 약관 명시 부재 |
| E3 | 한국 IBC 검토 명시 부재 |
| G2 | "severity" 격상 표현 |
| G3 | 5'/3' UTR 처리 부재 |
| C2 | Foldseek (structural homology) 인용 |
| C3 | AlphaFold-Multimer vs AlphaFold2 monomer |
| C4 | HMMER (HMM-based search) 인용 |

### 3.4 Blind spot 차원 (8개)

cycle 1-3가 점검 frame 안에 한 번도 안 넣은 차원:
1. **Licensing** (저작권/라이선스)
2. **Query reproducibility** (GenBank 등 외부 DB query)
3. **Negative-result reporting** (worst case 공개)
4. **Alternate distance-matrix tests** (Mantel, jackknife)
5. **Sub-lineage stratification** (group M/O, genotype)
6. **Formal ethics compliance** (DURC, IBC, 약관)
7. **Structural-tool breadth** (Foldseek, AlphaFold-Multimer)
8. **Dedup tooling citation** (CD-HIT, MMseqs2, HMMER)

---

## 4. C5 1시간 hostile defense rehearsal 결과

### 4.1 시뮬레이션 결과

| 단계 | 결과 |
|------|------|
| 첫 5분 인상 (abstract + ch1) | **6.5/10** (single-anchor + 흔들리는 panel 정의로 깎임) |
| Critical Q 3건 | Q1 prospective 부재가 가장 위험 (학생이 ch5:337 honest disclosure와 모순되면 fail trigger) |
| Major Q 4건 | Tranception–ESM-LLR collinearity, Layer A literature-provenance, Friedman underpowered=null, 4-feature operational direction |
| 5명 위원 분포 | **unconditional pass 2 + 조건부 pass 3 → 조건부 다수결** |
| 최종 결과 | **조건부 PASS** — abstract framing 약화 + ch6 4-feature recommendation 격하 + Tranception supplementary 추가 등 revision 요구 |

### 4.2 가장 위험한 단일 질문

**Q1**: "프로spective time-forward validation이 부재합니다. 그런데 학생 본인이 ch4:201에서 H3N2 2010-cutoff pilot이 0/20 또는 1/50 negative result라고 적었습니다. 이것을 *기 수행된 prospective evidence*라고 보긴 어렵지 않나요?"

**위험**: fail trigger는 아니나, 학생 답이 ch5:337 honest disclosure와 모순되면 위험으로 발전 가능.

---

## 5. 종합 외부 판정

### 5.1 Cycle 3 결과 보정

| 항목 | Cycle 3 자체 | **Codex IV&V** |
|------|------------|--------------|
| Phase 0 verify | 90/0/0 PASS | **PASS** (확인) |
| LaTeX 빌드 | 238 pages, 0 errors | **PASS** (확인) |
| Fix 적용 honest? | 113건 적용 | **YES** (10/10 verbatim) |
| Phase 4 점수 | 7.70 (A-) | **7.45** (0.25 inflated, B+/A-) |
| Defense 통과 확률 | 92% | **84-88%** |
| 잔여 결함 | 0 unaddressed | **20건 blind spot** |
| 최종 추천 | unconditional PASS | **조건부 PASS** |

### 5.2 핵심 결론

1. **fix 적용 자체는 honest** — 113건 보고가 사실관계로 verbatim 일치 (under-claim 방향)
2. **LaTeX hygiene 깨끗** — 2 orphan label만 있고 비차단
3. **Phase 4 점수 self-confirmation bias 0.25** — fix 적용을 알고 있는 시뮬레이터가 후하게 채점
4. **Defense % 4-8pp 과대** — 92% → 외부 84-88%
5. **신규 20건 blind spot** — 8 차원 (licensing/query/negative/test/lineage/ethics/structure/dedup)이 cycle 1-3 frame 밖이었음
6. **조건부 PASS 다수결** — unconditional pass는 위원 분포상 어려움, revision 요구 가능

### 5.3 Defense 차단 가능 항목

| 우선 | 항목 | 처리 |
|-----|------|------|
| **P0** | M1 라이선스 명시 (DURC 동시) | abstract / ch3에 1 paragraph 추가 (~30분) |
| **P0** | Q1 prospective 답변 노트 | 사용자 사전 준비 |
| **P1** | M2 GenBank query 명시 | ch3 supplementary table |
| **P1** | M3 worst-MCC 공개 | ch4 paragraph 추가 |
| **P1** | D1 Influenza B Vic vs Yam | ch4/ch5 paragraph |
| **P1** | E1 DURC 검토 | ch5 한 paragraph |
| **P1** | G1 RNA-virus 한정 표현 강화 | abstract / ch1 / ch6 wording |
| **P1** | C1 CD-HIT 인용 | references.bib + ch3:line |

위 8건 (~6시간 작업) 처리 시 외부 추정 defense % 88% → 92% 복원 가능.

---

## 6. 사용자 의사결정 항목

### Option A. 현 상태 (cycle 3 그대로) defense 진행
- 외부 추정 defense 84-88%
- 조건부 PASS 다수결
- Q1 (prospective) + 라이선스에 답변 노트 사전 준비

### Option B. **Codex C4 P0+P1 8건 추가 패치** (~6시간) ← **권장**
- defense % 88-92% 복원
- C4 critical/major 9건 closed
- prospective 답변 노트 + 라이선스 명시 추가

### Option C. C4 P0+P1+P2 20건 전부 (~1.5일)
- defense % 92-95%
- A- 등급 확보

---

## 7. 신뢰도 평가

| 차원 | 평가 |
|------|------|
| C1 verbatim 신뢰도 | 매우 높음 (사실관계만) |
| C2 LaTeX hygiene 신뢰도 | 매우 높음 (빌드 결과 객관적) |
| **C3 fairness 평가 신뢰도** | **중간** (외부 시각 추정도 한계 있음) |
| **C4 신규 공격 신뢰도** | **높음** (cycle 1-3 frame 밖 차원, 사실관계 다수) |
| C5 defense rehearsal 신뢰도 | 중간 (시뮬레이션이라 학생 실제 답변 능력 미반영) |

**해석**:
- C1/C2는 객관적 사실 — cycle 3 fix와 빌드는 honest
- C3/C5는 추정 — cycle 3 phase 4가 self-confirmation bias 있을 가능성 시사
- C4는 가장 acionable — 8 blind spot 차원의 20건 결함은 모두 evidence 기반

---

## 8. 산출물 인덱스

```
codex_ivv/
├── codex_C1_verbatim.md          ← 10/10 PASS, drift under-claim
├── codex_C2_latex_hygiene.md     ← LaTeX zero error, 2 orphan
├── codex_C3_fairness.md          ← 7.70 → 7.45 (0.25 inflated)
├── codex_C4_new_attacks.md       ← 20건 신규 결함 (8 blind spot)
├── codex_C5_defense_rehearsal.md ← 조건부 PASS 다수결, 84-88%
└── codex_C0_synthesis.md         ← 본 문서
```
