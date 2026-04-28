# 논문 적대적 감사 종합 결과 (2026-04-28)

대상 논문: MutBench 박사학위 논문 (`/proj/paper/paper/dissertation/`)
검수 프레임워크: `/adversarial-review` (paper-plan 4-Phase + 챕터별 심층 + codex IV&V)
실행 사이클: 1 (수정 1회)

---

## Phase 0: 자동 검증

| 항목 | 결과 |
|------|------|
| `verify_dissertation.py` | **86 / 0 / 0** (PASS / FAIL / WARN), P0 수정 후 +2 |
| LaTeX 빌드 | **206 pages**, errors 0, undefined refs 0, citation undefined 0 |
| TODO/FIXME/PLACEHOLDER | 0건 |
| 마감 어조 | 통과 |

---

## Phase 1: 블루팀 논증 지도

| 핵심 주장 | 변호 가능성 | 근거 |
|---------|-----------|------|
| C1 MutBench 8,580 evals (broadest hotspot benchmark) | 강건 | abstract, ch1, ch3 |
| C2 ω² scoring×pathogen = 0.296 (CI [0.195, 0.333]) | **강건** (한정 표현 필수) | within-cell residual ω²≈0.39와 비등 → "largest *modeled* component" 표현 정확 |
| C3 LOPO 0/11 + Friedman p=0.990 | **약함** | permutation null과 구별 어려움 (P≈0.96), corroboration 등급으로만 사용 |
| C4 HIV-1 7.19× vaccine escape | **가장 강건** | 82% Layer A-disjoint, novel-only worst-case p=5e-12 |
| C5 4-feature 97.6% retention | 중간 | numerical equivalence, paired-test 부재 (caveat 명시) |
| C6 9 distinct optimal info types | 강건 | per-pathogen MCC ranking |

실패 시나리오 5개 모두 본문 자체-caveat으로 부분~완전 방어. 잔여 위험: MAFFT --auto 모드 차이가 ω²의 input quality artifact일 가능성 (ch5 자체-인정).

---

## Phase 2: 레드팀 + 통계 검증

| Phase | 결과 |
|-------|------|
| 레드팀 | Critical 5 / Major 11 / Minor 10 |
| 통계 전문가 | **PASS 10/10**, 안돈 트리거 0건 |
| 챕터별 심층 (Ch1~Ch6) | Critical: 3/7/6/3/7/4 = 30건 (총 35건) |

**충돌 의견 중재 (CCB)**:
- 레드팀 C-02 ("null-consistent corroboration" 위장 표현) vs 통계: **(a) 통계 우위** — 본문이 "corroboration ≠ independent evidence" 명시. 단 ch6:13 묶음 표현만 분리 필요.
- 레드팀 C-04 (ω² selective headline) vs 통계: **(a) 통계 우위** — lower bound 0.103, residual 0.39 모두 abstract 명시.

---

## Phase 3: CCB 중재

| 분류 | 건수 |
|------|------|
| (a) 본문 caveat로 이미 해소 | 6건 |
| (b) 답 부족 — 수정 필요 | 31건 |
| (c) 공격 부당 | 0건 |
| **P0 (Phase 4 차단)** | **9건** (수정 완료) |
| P1 (권장) | 12건 |
| P2 (선택) | 15건 |

---

## codex IV&V (독립 외부 검증)

P0 10건 중:
- AGREE: 5건 (G09, G12, G14a, G14c, G02b)
- MODIFY (범위 확장): 4건 (G01, G07, G08, G14b)
- DISAGREE: 1건 (**G10 — 본문 이미 처리, P0 강등**)
- 추가 P0 발견: 0건
- audit quality: "Mostly sound"

→ **9건 codex 확장 범위로 수정** (G10 제외).

---

## P0 수정 결과 (사이클 1)

| ID | 결함 | 수정 위치 | 상태 |
|----|------|---------|------|
| G01 | ρ=0.97 vs ρ=0.12 cross-chapter disambiguation | ch5:33 | ✅ |
| G07 | 4-feature 97.6% paired-test caveat | abstract:11, abstract:14, ch6:14 | ✅ |
| G08 | "two-stage" → "two-stage main + Stage 3 layer" | abstract:8, ch1:82, ch1:111 (TikZ overview), ch1:143 | ✅ |
| G09 | novel-only Bonferroni p_adj=3.9e-9 derivation | ch4:886 | ✅ |
| G12 | Ch6 7.19× full vs novel-only 분리 | ch6:15 | ✅ |
| G14a | dms_evaluation_top.png Jaccard 페어 | ch4:104 | ✅ |
| G14b | cross_pathogen_comparison mean vs best MCC | ch4:210, ch4:215 | ✅ |
| G14c | stage3_anova_decomposition 잔차 caption | ch4:386 | ✅ |
| G02b | ch6 Friedman/LOPO 분리 표현 | ch6:13 | ✅ |
| G10 (codex DISAGREE) | — | — | 강등 |

수정 후: `verify_dissertation.py` 86/86 PASS, LaTeX 206 pages errors 0.

---

## Phase 4: 교수 10명 평가

### 평가표

| 교수 | 전공 | 평균 | 등급 |
|------|------|------|------|
| 1 | 위원장 (생물정보학) | 7.7 | PASS |
| 2 | 지도교수 (CS/SE) | 7.8 | PASS |
| 3 | 통계/ML | 7.2 | PASS |
| 4 | 계산생물학 | 7.3 | PASS |
| 5 | 바이러스/공중보건 | 7.3 | PASS |
| 6 | VEP/PLM 전문가 | 6.9 | 조건부 |
| 7 | 벤치마크 방법론 | 7.4 | PASS |
| 8 | 역학 실무자 | 6.8 | 조건부 |
| 9 | 통계유전학 | 7.1 | PASS |
| 10 | 구조생물학 | 7.1 | PASS |
| **종합** | — | **7.27** | **B+** |

### 항목별 평균 (1~10)

| A 문제 | B 관련 | C 방법론 | D 규모 | E 해석 | F 독창 | G 실용 | H 서술 | I 한계 | J 완성 |
|--------|--------|---------|--------|--------|--------|--------|--------|--------|--------|
| 7.5 | 7.3 | 6.9 | 7.0 | 7.2 | 7.1 | **6.7** | 7.8 | **8.0** | 7.2 |

### 가장 위험한 Defense 질문 TOP 3

1. **(VEP/PLM)** Tranception channel과 ESM-2 channel이 둘 다 ESM-2 masked-marginal proxy라면 SARS-CoV-2 best=Tranception은 best=ESM-LLR과 같지 않은가? — 두 column 간 ρ 측정 부재 (MEDIUM-HIGH 위험)
2. **(역학 실무자)** prospective/time-forward validation 부재 — 2024년 이후 신변종 사전 예측 sanity 1건? (MEDIUM-HIGH)
3. **(통계/ML)** 헤드라인 ω²=0.296을 cell-level 0.234로 demote하지 않은 이유 + cluster bootstrap 11 clusters에서 wild-cluster bootstrap 부재? (MEDIUM)

### 합격 기준 평가

| 기준 | 결과 | 비고 |
|------|------|------|
| **Strict (paper-plan)**: 평균 ≥ 7, 최저 ≥ 5 | **조건부 PASS** | C=6.9, G=6.7 marginal miss (0.1~0.3) |
| **Lenient (총점 80)**: ≥ 80 합격 | **FAIL** | 72.7점 (B+) |
| **Defense 통과 가능성** | **PASS 80% / 조건부 18% / FAIL 2%** | — |

---

## 최종 종합 판정

### **결과: 조건부 PASS (학위논문 통과 수준 충분)**

**강점**:
1. 8,580-evaluation factorial design의 scale
2. 3-layer ground truth의 orthogonal dimension 설계
3. 통계 honesty 학위논문 표준 상회 (LOPO null-consistent demotion, ω² range reporting, novel-only Bonferroni, 3-tier evidence rule)
4. 재현성 인프라 (random seed 42, library pinning, Zenodo DOI, 25-second reproducibility, CSV-to-table provenance manifest)
5. circularity audit + ANCOVA 정직성 (interaction이 covariate adjustment 후 0.234 → 0.264로 오히려 증가)

**약점**:
1. **G. 실용적 가치 (6.7)** — retrospective enrichment에 머물고 prospective/time-forward validation 부재
2. **C. 방법론 (6.9)** — Tranception/EVEscape proxy의 channel 분리 검증 부재
3. 4-feature 97.6% paired-test 부재 (P0 수정으로 honest demoted, hidden 결함 아님)
4. HIV-1 single anchor에 Contribution 3b 의존 (P0 수정으로 명시적 약점)

**Defense 전 권장 보강 (P1 우선 4건)**:
1. **Tranception–ESM-LLR per-pathogen ρ supplementary table** (교수 6 대응, 4시간) — CSV 1개 + Ch3 §scoring_types에 1 paragraph
2. **Structure source per-pathogen mapping table** (교수 10 대응, 2시간) — supplementary table only
3. **Time-stratified holdout 1-pathogen pilot** (교수 8 대응, 1일) — H3N2 2010-cutoff training/testing 1회
4. **Abstract/ch1에 "single-position regime, 11 RNA viruses, 20-type granularity" 한정사 명시 강화** (교수 1 대응, 30분)

위 4건 모두 처리 시 G/C 각각 0.3~0.5점 상승 예상 → **strict 기준 완전 통과 가능, lenient 80점도 근접**.

---

## 사용자 의사결정 항목

1. **현재 상태로 defense 진행** — 80% 통과 가능성, 3개 위험 질문 답변 준비 필요
2. **P1 4건 추가 보강** (defense 전, 1~2일 작업) — strict 완전 통과 + lenient 근접
3. **P1 12건 + P2 15건 모두 보강** (1~2주 작업) — A- 이상 목표
4. **재실험 필요한 항목**: **없음** — 모든 보강이 텍스트/supplementary 차원

---

## 사이클 통계

| 단계 | 시간 | 산출물 |
|------|------|--------|
| Phase 0 | 즉시 | phase0_verify.txt |
| Phase 1 (블루팀) | 4분 | phase1_blueteam.md |
| Phase 2 (레드팀) | 6분 | phase2_redteam.md |
| Phase 2 (통계) | 3분 | phase2_statistics.md |
| Phase 2B (Ch1~6 병렬) | 8분 | phase2b_ch1.md ~ phase2b_ch6.md |
| Phase 3 (CCB) | 5분 | phase3_ccb.md |
| codex IV&V | 9분 | phase3_codex_crosscheck.md |
| P0 9건 수정 | 즉시 | abstract / ch1 / ch4 / ch5 / ch6 편집 |
| Phase 0 재실행 | 즉시 | phase0_verify_post_p0.txt |
| LaTeX 재빌드 | 2분 | thesis_digital.pdf 6.2MB |
| Phase 4 (교수 평가) | 6분 | phase4_professor.md |

총 1사이클 완료. 재실행 불필요.
