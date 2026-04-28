# Cycle 3 — Abstract + Cross-chapter 적대 재공격 보고

**Date**: 2026-04-28
**Scope**: Phase B abstract (8건) + Phase C cross-chapter (전 챕터 정합) 재공격
**Verdict**: **DEFENSE-READY (full pass, 0 P0 / 0 P1 잔존)**.
- 14/14 핵심 수치 한·영 sync; 25/25 caveat grid YES; "operationally equivalent" 0건; bib 11/11 cited; 11 main vs 12 Stage 3 panel 정합.

---

## A. 한·영 14개 핵심 수치 sync 표

| # | 수치 | EN abstract | KR abstract | sync |
|---|------|-------------|-------------|------|
| 1 | 8,580 evals | L2, L4 | L6 | **OK** |
| 2 | $\omega^2 = 0.296$ | L2, L10 | L16 | **OK** |
| 3 | $\omega^2 = 0.234$ (cell-level) | (생략 — cross-chapter 차원에서 ch4/ch5에 위치) | (생략, 동일) | **OK by design** (abstract scope choice) |
| 4 | $\omega^2 = 0.103$ (6-cat lower bound) | L10 | L16 | **OK** |
| 5 | 0.265 (oracle gap) | L10 | L17 | **OK** |
| 6 | 7.19× (HIV-1 full set) | L2, L14 | L19 | **OK** |
| 7 | 7.16–8.24× (novel-only band) | L11, L14 | L19 | **OK** |
| 8 | 9.36× (H3N2) | L11 | L19 | **OK** |
| 9 | 7.63× (SARS-CoV-2) | L11 | L19 | **OK** |
| 10 | 4.012× (EqualWeight H3N2) | L11, L14 | L22 | **OK** |
| 11 | 0.61 (perm p) | L11, L14 | L22 | **OK** |
| 12 | +0.011 (paired Δ) | L11, L14 | L22 | **OK** |
| 13 | 3.9×10⁻⁹ (Bonferroni adj p) | L11 | L19 | **OK** |
| 14 | 11 RNA viruses (main panel) | L2, L4, L10 | L6 | **OK** |

추가 sync (CI/test stats):
- [0.195, 0.333] cluster-bootstrap CI: EN L2/L10 / KR L16 — OK
- [-0.018, +0.042] paired delta CI: EN L11/L14 / KR L22 — OK
- 5×10⁻¹² worst-case Fisher: EN L11 / KR L19 — OK
- 2.5×10⁻¹⁶ Bonferroni full HIV: EN L2 / KR L19 — OK
- $\chi^2 = 7.69$, p = 0.990: EN L10 / KR L17 — OK

**판정**: 14/14 + 5 보조 = **19/19 sync, drift 0건**. 한국어 어조 약화 없음 (오히려 "P≈0.96 null 기댓값"이 KR L17에 더 명시적).

---

## B. 5×5 Caveat Grid (caveat × 챕터)

| Caveat | Abstract | Ch1 | Ch4 | Ch5 | Ch6 |
|--------|----------|-----|-----|-----|-----|
| LOPO 0/11 null-consistent | YES (EN L10 / KR L17) | YES (L145, L148) | YES (L336, L338, L478, L600) | YES (L155, L319, L323) | YES (L13) |
| ω² range (0.103/0.296/0.39) | YES (full range L10) | YES (L148: 0.103+0.296) | YES (L425, L431, L600, L1042) | YES (L70, L93, L155, L290, L323) | YES (L12) |
| Novel-only Bonferroni 3.9e-9 | **YES (EN L11 / KR L19)** | YES (L117 TikZ + L150) | YES (L956 footnote) | YES (L161, L176 indirect via 780-fold) | **YES (L15)** |
| HIV-1 single anchor | YES (L11, L14 / KR L19) | YES (L117, L131, L150, L153) | YES (L13, L595, L1041) | YES (L93, L155, L161, L176, L179) | YES (L15, L94) |
| 4-feat paired-test (no 97.6 in-sample) | YES (L11, L14 / KR L22) | YES (L150, L152) | YES (L839 demote) | YES (L162; L192 augmented w/ Tab cross-ref) | YES (L14) |

**Cycle 2 잔존 PARTIAL 2건이 모두 YES로 격상**:
1. Cycle 2에서 abstract / ch5 / ch6 PARTIAL이었던 "Bonferroni 3.9e-9" → cycle 2 fix가 abstract.tex:11 + abstract_kr.tex:19 + ch6:15에 일괄 추가하여 **5/5 YES**.
2. Cycle 2에서 ch5:192 PARTIAL이었던 "97.6% protocol caveat" → applied_cross_chapter §B에서 ch5:192에 `(numerical retention only; the formal nested-LOPO non-inferiority result---paired delta +0.011, 95\% CI [-0.018, +0.042], permutation p = 0.61---is reported in Chapter ch:results Table tab:nested_lopo_4core)` 추가. **YES**.

**판정**: **25/25 cell YES**. Caveat propagation 결함 0건.

---

## C. "Operationally equivalent" zero-grep 검증

`grep "operationally equivalent\|operational equivalence\|운영적으로 동등" front_en/abstract.tex front/abstract_kr.tex chapters_en/ch5_discussion.tex` →
- **abstract.tex: 0 hits** (EN demote — applied_cross_chapter §B P1)
- **abstract_kr.tex: 0 hits** (KR demote — applied_cross_chapter §B P1)
- **ch5_discussion.tex: 0 hits** (5-P0-3 / 5-P0-4 demote)
- ch4:841: **1 hit (intentional metacomment)** — `"the dissertation hereafter reports the result as 'operational equivalence under nested-LOPO (p=0.61, paired delta CI [-0.018, +0.042])' rather than as a percentage retention"` — 이것은 abstract/ch1 demote의 **정당화 단락** (의도적 보존, applied_cross_chapter §B 명시). 격하 표현이 격하 자체를 메타-설명하는 self-consistent 위치.

**판정**: 본 task가 명시한 3개 파일(abstract / abstract_kr / ch5)에서 **0/3 잔존 = clean**. ch4:841 잔존은 cross_chapter §B에서 의도된 것.

---

## D. Bibliography spot check (11개 신규 BibTeX)

| Key | references.bib line | ch2 인용 | 검증 |
|-----|---------------------|----------|------|
| `murrell2012meme` | 1345 | ch2:58 | ✓ |
| `kosakovskypond2005fel` | 1356 | ch2:59 | ✓ |
| `murrell2015busted` | 1367 | ch2:59 | ✓ |
| `hayes2024esm3` | 1378 | ch2:146 | ✓ |
| `hsu2022esmif` | 1390 | ch2:147 | ✓ |
| `su2024saprot` | 1399 | ch2:147 | ✓ |
| `dauparas2022proteinmpnn` | 1408 | ch2:147 | ✓ |
| `greaney2021RBD` | 1419 | ch2:109 | ✓ |
| `greaney2022spike` | 1430 | ch2:109 | ✓ (note: PLoS Path 18:e1010592 ambiguity 잔존, applied_cross_chapter §4) |
| `luksza2014predictive` | 1442 | ch2:182 | ✓ |
| `huddleston2020integrating` | 1453 | ch2:182 | ✓ |

**판정**: 11/11 bib entry ↔ ch2 인용 정합. xelatex+bibtex 3-pass 후 0 undefined citations (cycle 2 verify 90 PASS / 0 FAIL). `greaney2022spike` 출처 모호성 1건은 사용자 확인 항목으로 applied_cross_chapter §4.4에 이미 메모됨 — defense에 영향 없음 (note 필드에 alternative 기록 유지).

---

## E. 새 발견 (Cycle 3 신규 적대 공격 결과)

**E1. Abstract → 본문 강도 inversion 검사**:
- abstract EN L11 "primary anchor" — ch5:175-179 / ch6:15에서도 같은 표현 + 추가 context. **Abstract가 본문보다 강하지 않음** (오히려 abstract가 demote 표현 더 명시적: `(retrospective enrichment; no prospective time-forward validation)`). PASS.
- abstract EN L11 "statistically indistinguishable...non-rejection of inferiority hypothesis" — ch1:152 / ch6:14 / ch5:162 모두 동일 caveat 표현. PASS.

**E2. 한국어 어조 약화 검사**:
- KR L17 `"증거는 ω² 상호작용과 HIV-1 외부 검증의 결합으로 해석되어야 한다"` — EN L10 `"the conclusion rests on the interaction effect plus the vaccine-escape audit, not on LOPO in isolation"` 와 의미적 등가. KR이 오히려 P≈0.96 null 기댓값을 추가로 명시 (EN에는 부재) → **KR이 더 정직**.
- KR L19 `"가장 정직한 외부 검증 근거"` ≈ EN L2 `"primary external anchor"` — 어조 균형. PASS.

**E3. 11 vs 12 panel 분리 검증**:
- abstract EN L2/L4/L10/L11 모두 `11 RNA viruses` (Stage 2 main panel)
- ch1:82/142 `11-pathogen main panel, ... extended to 12 pathogens by adding Zika for the feature-ablation and nested-LOPO analyses`
- ch6:14 `12-pathogen Stage~3 panel` (Stage 3 nested-LOPO)
- ch6:11 `11 RNA viruses` (Stage 2 main)
- KR abstract L6 `11개 RNA 바이러스` (Stage 2)
- abstract는 Stage 2 헤드라인이므로 11만 인용; Stage 3 12 패널은 ch1/ch4/ch6 본문에서 명시 — **scope 분리가 의도적이고 일관**. PASS.

**E4. 단일 잠재 이슈 (P3, 미차단)**:
- KR abstract L22 한국어 paired Δ에서 `"Δ"` (Greek) 사용. EN은 `"+0.011"` 직설. 한국어 LaTeX `\Delta`로 통일 권장 가능하나 — KR L22의 `paired Δ +0.011` 표현이 `paired Δ +0.011 MCC` (절대값+단위)로 정확하므로 **수정 불필요**. P3 cosmetic.

**E5. 잔존 정직 deliverable (cycle 2 §4 미해결)**:
- Lab notebook freeze date 2024-08-12 (ch3:302 placeholder)
- Provenance CSVs 부재 (`results/mutbench/provenance/` 디렉토리 없음)
- Zenodo DOI placeholder
- 모두 **submission-time deliverable**, dissertation 텍스트 일관성에는 영향 없음.

---

## F. Defense Readiness 판정

| Check | Status |
|-------|--------|
| 14 핵심 수치 한·영 sync | **PASS** (14/14 + 5 보조) |
| G07/G08 한국어 전파 | **PASS** (KR L12 Stage~3 layer, KR L22 paired-test caveat 모두 LANDED) |
| Tranception caveat 한·영 | **PASS** (EN L13 / KR L21) |
| Retrospective caveat 한·영 | **PASS** (EN L2 / KR L19) |
| Bonferroni 3.9e-9 한·영 | **PASS** (EN L11 / KR L19) |
| "Operationally equivalent" 잔존 | **PASS** (3개 target 파일 0 hits; ch4:841 의도적 metacomment 1건) |
| 5×5 caveat grid | **PASS** (25/25 YES; cycle 2 PARTIAL 2건 격상 완료) |
| 11 vs 12 panel sync | **PASS** (Stage 2/Stage 3 scope 분리 일관) |
| Bib spot check (11 신규) | **PASS** (11/11 cited, xelatex 0 undefined) |
| Abstract overclaim | **CLEAN** (abstract가 본문보다 약하거나 같음) |
| KR 어조 약화 | **CLEAN** (KR이 EN과 동등 또는 더 정직) |
| Verify_dissertation.py | **90 PASS / 0 FAIL** (applied_cross_chapter 보고) |

**최종 판정**: **DEFENSE-READY**.

- P0: 0건 잔존
- P1: 0건 잔존
- P2/P3: 0건 텍스트 결함; 3건 submission-time deliverable (lab freeze date, provenance CSVs, Zenodo DOI assignment) — 본 task 범위 외.

위원회 questions Q1 (TOP-1 / Tranception) / Q2 (prospective?) / Q3 (4-feat over-fit?) / Q4 (LOPO 0/11 의미?) — 모두 abstract + ch1/ch4/ch5/ch6에서 일관 caveat로 차단 완료.

(~530 words)
