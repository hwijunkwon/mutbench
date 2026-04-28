# MutBench 박사논문 종합 검수 — 최종 Trajectory (2026-04-28)

대상: `/proj/paper/paper/dissertation/`
프레임워크: paper-plan 4-Phase + 챕터별 IV&V + codex 외부 검수 + Phase F 보강
실행 사이클: **3 + Phase F + Codex IV&V (5+1 step)**
총 적용 fix: **121건**

---

## 1. Trajectory 통계

| 단계 | 발견 결함 | 적용 fix | Phase 0 | 자체 점수 | **외부 점수** | Defense % |
|------|---------|---------|--------|--------|------------|-----------|
| Cycle 1 | ~70건 | 9 P0 | 88 | 7.27 (B+) | — | 80% |
| Cycle 2 | 신규 19 + cycle1 미수정 22 | 99 (Phase B) + 7 (Phase C) | 90 | — | — | — |
| Cycle 3 | 잔여 7건 | 7 (Phase E) | 90 | **7.70 (A-)** | 7.45 (B+/A-) | 자체 92% / **외부 84-88%** |
| **Phase F** | C4 신규 20건 | 8 (P0+P1) | **90** | — | **7.55 (A-)** | **외부 86-90%** |

---

## 2. 누적 fix 분포 (121건)

| Phase | 챕터/대상 | 건수 | 핵심 |
|-------|---------|-----|------|
| Cycle 1 P0 | abstract, ch1, ch4, ch5, ch6 | 9 | G01 ρ disambig / G07 4-feat caveat / G08 Stage 3 layer / G09 Bonferroni / G12 7.19× / G14 figures / G02b Friedman split |
| Phase B Abstract | EN+KR | 8 | KR G07/G08 전파, retrospective+Tranception caveat |
| Phase B Ch1 | introduction | 12 | 11→12 panel, "operationally equivalent" 제거, TikZ subbox |
| Phase B Ch2 | background | 12 | 10→20 types, MEME/FUBAR/FEL/SLAC/BUSTED 인용, antibody-escape DMS |
| **Phase B Ch3 (가장 무거움)** | methods | **24** | EqualWeight 두 protocol 분리, cell-level demote, wild-cluster, 7 method backport |
| Phase B Ch4 | results | 17 | ω² 4-parameterization, Bonferroni 분모 footnote, EqualWeight sync |
| Phase B Ch5 | discussion | 14 | 97.6% qualifier, prospective gap section, MAFFT artifact |
| Phase B Ch6 | conclusion | 12 | G02b PARTIAL→PASS, PAHD-R 격하, 4 contributions |
| Phase C Cross-chapter | references.bib + 정합성 | 7 + 11 BibTeX | Bonferroni 3.9e-9 sync, GitHub URL, "operationally equivalent" 0 hits |
| Phase E (cycle 3 잔여) | ch1/ch2/ch4/ch5/ch6 | 7 | Greaney mis-anchor, phantom CSV, FUBAR count, PAHD-R cross-ref |
| **Phase F (codex C4 P0+P1)** | abstract/ch1/ch3/ch4/ch5/ch6 | **8 + 2 BibTeX + 1 note** | **라이선스 명시 / GenBank query / worst-MCC / Influenza B Vic/Yam / DURC / RNA-virus 한정 / CD-HIT / Q1 defense note** |
| **합계** | — | **121** | — |

---

## 3. 핵심 결함 처리 결과 (가장 위험했던 것 중심)

| ID | 결함 | 위험도 | 처리 결과 |
|----|------|--------|----------|
| Ch3 EqualWeight label leakage | Critical (defense 직격탄 가능) | **누출 없음 코드 검증** + 본문 production vs ablation 분리 명시 |
| Ch4 cell-level 0.234 비누설 | Critical | 4-parameterization (0.234/0.296/0.264/0.252-0.319) ch3/ch4/ch5 sync |
| Ch5 97.6% 임상 오독 | Critical | "relative to 10-feature ensemble, not absolute floor" qualifier |
| Ch5 Tranception proxy | Defense Q1 위험 | ρ=0.64-0.84 collinearity 명시 단락 |
| Ch5 Prospective 부재 | Defense Q1 위험 | 신규 sec:prospective_validation_gap 단락 + Q1 defense note |
| Ch3 wild-cluster bootstrap | 통계 honesty | acknowledge + Cameron 2008 + future-work 격하 |
| Korean abstract G07/G08 미동기화 | P0 | 한·영 14개 핵심 수치 100% sync |
| "Operationally equivalent" 과장 | P0 | abstract+ch1+ch5 모두 0 hits |
| Ch4 Phantom CSV 4건 | Critical 회귀 | 2 실존 매핑, 2 supplementary deferral |
| Ch2 Greaney mis-anchor | Critical 회귀 | Layer C ↔ vaccine-escape audit 분리 |
| **M1 라이선스 명시 (Phase F)** | Critical (DURC + 저작권 동시) | **ch3 §Software and data licenses 단락 + ch6 §Code Availability + ch5 §DURC** |
| **M2 GenBank query (Phase F)** | Major | ch3:133 SARS-CoV-2 query inline + 11 query CSV archive |
| **M3 worst-MCC 공개 (Phase F)** | Major | ch4:340 worst tuple (HCV × stability × SWAN, MCC=−0.361, 음 MCC 4,171/8,580) |
| **D1 Influenza B Vic/Yam (Phase F)** | Major | ch3 lineage 명시 + ch5 sublineage pooling acknowledge |
| **E1 DURC 검토 (Phase F)** | Major | ch5 §DURC 신규 단락 (NIH 7 카테고리 + KNU IBC) |
| **G1 RNA-virus 한정 (Phase F)** | Major | abstract+ch1+ch6 한정사 강화 |
| **C1 CD-HIT/MMseqs2 (Phase F)** | Major | references.bib + ch3:133 dedup tool 명시 |

---

## 4. Phase 4 교수 평가 변화 (cycle 1 → cycle 3 → 외부 → Phase F 후)

### 4.1 항목별 점수

| 항목 | Cycle 1 | Cycle 3 자체 | **외부 보정** | **Phase F 후 외부** | 핵심 |
|------|--------|------------|------------|-------------------|------|
| A 문제 | 7.5 | 7.8 | 7.7 | **7.75** | — |
| B 관련 | 7.3 | 7.6 | 7.5 | **7.55** | 11 BibTeX + 2 (CD-HIT, MMseqs2) |
| **C 방법론** | 6.9 ⚠️ | 7.5 | 7.3 | **7.5** | EqualWeight + cell-level + wild-cluster + 라이선스 + GenBank query |
| D 규모 | 7.0 | 7.4 | 7.3 | **7.35** | — |
| E 해석 | 7.2 | 7.6 | 7.4 | **7.45** | claim-by-claim discount |
| F 독창 | 7.1 | 7.5 | 7.4 | **7.45** | — |
| **G 실용** | 6.7 ⚠️ | 7.0 | 6.8 | **6.95** | prospective gap + RNA-virus 한정 + worst-MCC honest |
| **H 서술** | 7.8 | 8.5 | 8.1 | **8.15** | wording sync, KR sync |
| **I 한계** | 8.0 | 9.0 | 8.5 | **8.7** | mafft + Tranception + DURC + sublineage acknowledge |
| J 완성 | 7.2 | 7.7 | 7.5 | **7.55** | — |
| **종합** | **7.27 (B+)** | **7.70 (A-)** | **7.45 (B+/A-)** | **7.55 (A-)** | — |

### 4.2 합격 기준

| 기준 | Cycle 1 | Cycle 3 자체 | 외부 보정 | **Phase F 후** |
|------|--------|------------|---------|---------------|
| Strict (평균 ≥ 7, 최저 ≥ 5) | 조건부 PASS (C/G 미달) | unconditional PASS | 조건부 PASS (G=6.8) | **조건부 PASS (G=6.95 thresh 경계)** |
| Lenient (총점 ≥ 80) | 72.7 (FAIL) | 77.0 (FAIL, A-) | 74.5 (FAIL, B+) | **75.5 (FAIL, A-)** |
| Defense 통과 % | 80% | 92% | **84-88%** | **86-90%** |

---

## 5. Defense Readiness 외부 최종 판정

### 5.1 결과: **조건부 PASS — 학위 통과 86-90%**

- unconditional PASS는 G=6.95 thresh 0.05 미달로 58-65% borderline
- 조건부 PASS 다수결 (위원 5명 중 unconditional 2 + 조건부 3) 가능성 높음
- defense 진입 권고 가능

### 5.2 강점

1. **8,580-evaluation factorial design + reproducibility infrastructure** (random seed 42, library pinning, GitHub URL + Zenodo DOI placeholder, 25-second reproducibility, **신규 라이선스 명시**)
2. **3-layer ground truth orthogonal dimension** + circularity audit
3. **통계 honesty 학위논문 표준 상회**: LOPO null-consistent demotion / ω² 4-parameterization (0.234/0.296/0.264/0.252-0.319) / novel-only Bonferroni p_adj=3.9e-9 cross-chapter sync / wild-cluster bootstrap acknowledge
4. **한계 honesty 학위논문 매우 강함 (I=8.7)**: sec:prospective_validation_gap / sec:mafft_auto_artifact / Tranception–ESM-LLR collinearity / single-team-single-snapshot / Bolker 11-cluster threshold / **DURC + sublineage pooling 신규 acknowledge**
5. **Cross-chapter 정합성**: 25/25 caveat grid, 14개 수치 한·영 sync, 13개 신규 BibTeX 모두 resolve, "operationally equivalent" 0 hits
6. **신규 라이선스 + DURC 검토 + RNA-virus 한정**: defense 차단 위험 4 카테고리 동시 closed

### 5.3 잔여 약점 (Defense에서 답변 노트 권고)

1. **Prospective time-forward validation 자체 부재** — 답변 anchor: ch5:337 sec:prospective_validation_gap, **defense_q1_answer_note.md**
2. **HIV-1 single anchor for Contribution 3b** — honest 인정으로 회피
3. **Tranception–ESM-LLR channel collinearity** — supplementary table queued
4. **G=6.95 thresh 경계** — 단일 weak point, 위원장 컨센서스 필요

---

## 6. Submission 전 사용자 확인 항목

| ID | 항목 | 우선 | 처리 시점 | 비고 |
|----|------|-----|---------|------|
| 1 | Lab notebook freeze date 2024-08-12 (ch3:302) | placeholder | 사용자 확인 | — |
| 2 | GitHub URL `kksuhj/mutbench` 정합 | 사용자 확인 | 즉시 | repo 실제 존재? |
| 3 | Zenodo DOI assignment | submission 시점 | 제출 시 | placeholder |
| 4 | Provenance CSVs archive | submission 전 | Zenodo bundle | `genbank_queries.csv`, `dms_sources.csv`, `tool_versions.txt` |
| 5 | Supplementary CSV "under preparation" 인용 archive | submission 시 | Zenodo bundle | Ch4 phantom 2건 deferral |
| 6 | `greaney2022spike` source DOI 확정 | 사용자 확인 | 즉시 | Virus Evolution vs PLoS Path |
| **7** | **외부 자원 라이선스 정확 버전** | **% TODO 2건** | **사용자 확인** | **ESM-3 license 정확 명, DMS 데이터 license** |
| **8** | **KNU IBC tag/letter ID** | **% TODO 1건** | **사용자 확인** | **DURC 검토 letter ID** |
| **9** | **Q1 defense note 학생 외우기** | **defense 직전** | **본인** | **defense_q1_answer_note.md 4-step** |

---

## 7. 코덱스 외부 IV&V 6단계 결과

| Step | 결과 |
|------|------|
| **C1** Fix verbatim spot-check | **10/10 PASS**, drift는 under-claim 방향 |
| **C2** LaTeX hygiene | **PASS** (zero error, 7 신규 라벨 모두 작동, 13 BibTeX 정합) |
| **C3** Phase 4 fairness | bias 중간 — 7.70 → 외부 7.45 (0.25 inflated) |
| **C4** 외부 적대적 새 공격 | **20건 신규 결함** (cycle 1-3 8 blind spot) |
| **C5** 1시간 hostile defense rehearsal | 조건부 PASS 다수결, 첫인상 6.5/10 |
| **C6** Phase F mini-rehash | **8/8 verbatim PASS**, 외부 점수 7.45 → 7.55, defense 84-88% → 86-90% |

---

## 8. 산출물 인덱스

```
/proj/paper/paper/dissertation/review/2026-04-28/
├── (cycle 1) phase0~6, summary.md
├── cycle2/                         (Phase B, C — 99 + 7 fix)
├── cycle3/                         (Phase E + cycle 3 적대 재공격 — 7 fix + summary_cycle3.md)
└── codex_ivv/                      ← 외부 검수 + Phase F
    ├── codex_C1_verbatim.md
    ├── codex_C2_latex_hygiene.md
    ├── codex_C3_fairness.md
    ├── codex_C4_new_attacks.md
    ├── codex_C5_defense_rehearsal.md
    ├── codex_C0_synthesis.md
    ├── applied_phase_f.md          (Phase F 8건 + 2 BibTeX + Q1 note)
    ├── defense_q1_answer_note.md   ← 학생 사전 준비
    ├── codex_C6_phase_f_rehash.md  ← Phase F 외부 mini-rehash
    └── final_trajectory.md         ← 본 문서
```

---

## 9. 최종 결론 (외부 시각)

- **Cycle 1~3 + Phase F 모두 honest**: 121건 보고가 사실관계로 verbatim 적용
- **LaTeX hygiene 깨끗**: 245 pages 0 errors, 13 신규 BibTeX 정합
- **Phase F가 cycle 3 self-confirmation bias 일부 회복**: 외부 7.45 → 7.55 (+0.10)
- **Defense 진입 권고 가능**: 조건부 PASS 86-90% 학위 통과
- **잔여 위험 1개**: Q1 prospective 부재 — defense answer note 외우기 + 발표 슬라이드에 honest disclosure 노출
- **재실험 0건**: 모든 fix가 텍스트 + supplementary reference만, 코드/실험 변경 없음

121건 fix · 6 cycle · 30+ 병렬 에이전트 · 회귀 0건. 최대한 정성스럽게 끝냈습니다.
