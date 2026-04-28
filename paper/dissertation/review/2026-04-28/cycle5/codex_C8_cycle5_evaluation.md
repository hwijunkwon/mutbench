# Codex C8: Cycle 5 외부 재평가 (최종)

작성: 2026-04-28 (codex IV&V Step 8)
시각: cycle 1~4 + Phase F + cycle 5까지 의도적으로 거리를 두고 본문 verbatim·supplementary CSV·빌드 산출물만 재독한 외부 위원
직전 baseline: C7 외부 7.81 / strict unconditional PASS / defense 91-94%

---

## A. 4 측정 verbatim 검증

| Tier | 측정 결과 | 본문 통합 위치 | supplementary 산출물 | 평가 |
|------|---------|--------------|------------------|------|
| **D2** 4-feature ensemble | grand-mean MCC -0.0009/-0.0060/+0.0042/-0.0097, AUROC 0.555/0.543/0.549/0.561; +homoplasy Wilcoxon p<0.001, 4-feat p=0.016, +pLDDT p=0.170; EV-A71 MCC 0.146→0.188 | ch4:279-281 paragraph `para:sliding_window_4feature` 신설 + ch4:284-286 figure caption + ch5:351 sec:prospective_validation_gap 단락 | `sliding_window_prospective_backtest_4feature.csv`, `sliding_window_prospective_c2_vs_d2_paired.csv`, `sliding_window_prospective_4feature_diagnostics.csv`, `figures/sliding_window_prospective_backtest_4feature.png` (모두 존재 확인) | **PASS** — verbatim "$0.555$, $0.543$, $0.549$, and $0.561$", "$p<0.001$ (+homoplasy, mean $\Delta=+0.005$, 44 better/$5$ worse/$24$ tied across 73 windows)", "$p=0.016$ (4-feature, mean $\Delta=-0.009$)", "EV-A71 (mean MCC $0.146 \to 0.188$ with homoplasy; AUROC $0.773 \to 0.844$)" 모두 일치. honest framing "+homoplasy yields a small but statistically distinguishable improvement... while pLDDT alone and the 4-feature combination slightly degrade the Top-30 MCC despite a marginally higher mean AUROC" 정직 보고. HCV 파괴 ("homoplasy is destructive in the HCV regime where the empirical homoplasy distribution is essentially flat") 명시. |
| **D4** Provenance 6 file | 6 파일 모두 `/proj/paper/results/mutbench/provenance/`에 실재 (genbank_queries.csv 3.4KB, dms_sources.csv 2.3KB, tool_versions.txt 2.7KB, external_resource_licenses.csv 4.2KB, README.md 4.0KB, commit.txt 0.4KB) | ch3:1028 (license matrix sentence 신설), ch3:1032 (license_matrix file 명시), ch3:1036 (ESM-3 esm3_sm_open_v1 + Cambrian 1.0 명시) | 6 file all on-disk; ESM-3 excludability `used_in_headline_grid=No` flag 가 mechanically auditable | **PASS** — ch3:1028 verbatim "A machine-readable per-resource license matrix... is archived in \texttt{results/mutbench/provenance/external\_resource\_licenses.csv}; the bullet list below is a human-readable summary" 일치. ch3:1036 verbatim "ESM-3 (\texttt{esm3\_sm\_open\_v1})" + "Cambrian 1.0 non-commercial license (academic only)" 일치. TODO 3건 중 2건 (ch3:1023 라이선스 confirm, ch3:1033 ESM-3 license version) resolved; ch5:359 KNU IBC TODO만 잔존. |
| **D5** 4-way ω² | block bootstrap [0.202, 0.346] mean 0.272 / mixed-effects pseudo-ω²=0.340 ICC=0.135 LRT χ²₁=913.7 p<10⁻¹⁹⁸ / 4-way Table | ch3:966-968 (2 paragraphs 신규 — Phylogenetic block + Linear mixed-effects), ch4:589 paragraph + Table 4.9 `tab:omega_robustness_4way`, ch5:289 4-frame 비교 ("under all four inferential frames") | `block_bootstrap_omega_summary.csv`, `mixed_effects_omega_summary.csv`, `omega_robustness_4way.csv` (모두 존재) | **PASS** — ch3:966 verbatim "$[0.202, 0.346]$ for $\omega^2_{\text{int}}$ (mean $0.272$, $\Pr(\omega^2 \leq 0.14) = 0.008$); the lower bound matches the pathogen-level cluster bootstrap to three decimal places" 일치. ch3:968 verbatim "$\chi^2_1 = 913.7$, $p < 10^{-198}$" + "pseudo-$\omega^2_{\text{int}} = ... = 0.340$" 일치. ch4:589 verbatim Table 4.9 4-row "Phylogenetic block (G\,=\,8) & 0.272 & 0.202 & 0.346 & 0.143" 일치. ch5:289 verbatim "the cluster-bootstrap lower bound (0.195), the wild-cluster lower bound (0.201), and the phylogenetic-block lower bound (0.202) and remains above Cohen's large-effect threshold ($\omega^2 > 0.14$) under all four inferential frames" 일치. CSV 직접 검증: lower bound 0.2008 / 0.2005 / 0.2022 — 세 자리 소수점 일치 주장 정확. |
| **D8** Defense Q&A notes | Q1-Q10 (Q1은 별도 파일), 각 60-90초 답변 + verbatim anchor + Q[N]a/b/c 후속 + Slide A/B/C 권고 | (본문 update 없음 — 학생 사전 준비 자료) | `defense_qa_notes.md` 39 KB | **PASS (간접)** — 본문 anchor (ch5:179, ch5:285, ch5:330, ch5:347, ch5:329, ch4:578 등) 모두 cycle 4 verbatim과 일치 확인. Q3 (ω² cherry-pick) Q9 (wild-cluster) 답변에 cycle 5 Tier D5 (4-way) 결과는 미반영 — defense 직전 학생이 1-2 문장 추가 갱신 필요 (minor). |

**4/4 verbatim PASS**. xelatex 266 pages (cycle 4 259 → +7 pages: D2 paragraph + figure ~4 pages, D5 paragraphs + Table 4.9 ~3 pages). 모든 cycle 5 산출물 on-disk + 본문 reference triangulate 일치.

---

## B. D3 (DNA virus 추가) 미완료 영향 평가

D3 (HSV-1 또는 추가 DNA virus pilot)는 cycle 5에서 시도되었으나 **실패/미완료**로 분류되었다. 외부 시각 평가:

1. **Cycle 4 C1 HBV pilot이 이미 single-pathogen DNA-virus null result로 정착**. ch5:329 단락이 "this null result is a direct empirical sanity check on the design rationale"로 frame되어 **DNA virus 검증 시도 자체는 측정 발생함**. D3는 **추가** pilot이지 대체가 아님.
2. D3 부재로 인한 약점은 (i) 1 DNA virus(HBV)만 — 2종 비교 불가 (ii) HBV null result의 generalization 주장 약화. 그러나 **본문 어디에도 "DNA virus 일반화" 주장이 없음**. ch5:329 + ch6:85 모두 "single-pathogen DNA-virus density pilot" 한정 표현.
3. **외부 점수 영향 추정**: -0.05 ~ -0.10 (G 항목, "DNA virus 확장" 미달). 그러나 cycle 4에서 G가 7.25로 thresh 0.25 여유 확보 — D3 부재가 G를 thresh 아래로 밀지 못함.
4. Defense 단발 trigger 가능성: **Low**. *"왜 HBV 외 다른 DNA virus는 시도 안 했나?"* 질문에 학생은 "HBV pilot의 정직한 null result로 design rationale (RNA virus 한정 scope)이 empirically backed되었으며, 추가 DNA virus pilot은 ch6 Future Roadmap Priority 3으로 등록"으로 1단계 답변 가능.

**판정: D3 미완료는 강점 추가 실패이지 약점 노출이 아님. 점수에는 -0.02 ~ -0.05 정도의 minor 영향만**.

---

## C. 항목별 외부 점수 재추정

| 항목 | Cycle 4 외부 (C7) | **Cycle 5 외부** | 회복 폭 | 근거 |
|------|----------------|------------------|--------|------|
| **C** 방법론 | 7.85 | **8.05** | +0.20 | D5 4-way ω² robustness — Phase F 시점 single bootstrap → cycle 4 cluster+wild 2-way → cycle 5 4-way (cluster, wild, phylogenetic block, mixed-effects). 모든 4 frame이 lower bound 0.20 부근 일치 + Cohen large 통과는 **statistical robustness의 표준적 정공법**. mixed-effects LRT p<10⁻¹⁹⁸ 가 강력한 model-based corroboration. |
| **G** 실용 | 7.25 | **7.30** | +0.05 | D2 4-feature ensemble은 mixed result — homoplasy 단독 추가 p<0.001이지만 mean Δ=+0.005 (small), 4-feature는 mean Δ=-0.009 (slight regression). Per-pathogen pattern이 retrospective LOPO와 일관되어 **honest evidence 보강** but **operational claim 격상은 아님**. EV-A71 MCC 0.146→0.188 + AUROC 0.773→0.844는 single-pathogen highlight. |
| **I** 한계 | 8.85 | **9.00** | +0.15 | D2 honest report (HCV 파괴, 4-feat regression) + D4 ESM-3 license version frozen (esm3_sm_open_v1, Cambrian 1.0) + D5 Bolker n=11 caveat 명시 + Self-Liang 1987 boundary correction 명시. "9.0 thresh와 0.15 차이" → **9.0 도달**. |
| **H** 서술 | 8.30 | **8.40** | +0.10 | ch3:966-968 신규 2단락 (block bootstrap, mixed-effects) + ch4:589 신규 paragraph + Table 4.9 + ch5:289 4-frame 비교 + ch5:351 4-feature 단락 — 서술 완성도 향상. defense Q&A notes는 학생 자체 자료이지 본문 H가 아님. |
| **J** 완성 | 7.65 | **7.85** | +0.20 | D4 provenance 6 file이 placeholder/TODO에서 실재 CSV로 격상. 2/3 TODO resolved (ch3:1023, ch3:1033). external_resource_licenses.csv가 mechanically auditable. ESM-3 excludability에 `used_in_headline_grid=No` flag. submission readiness 직접 보강. |
| **A** 기여 | 변경 없음 | 변경 없음 | 0 | D2/D4/D5 모두 contribution 추가가 아닌 robustness/provenance 보강. |
| **B** 정확성 | 변경 없음 | 변경 없음 | 0 | 측정값 모두 supplementary CSV로 triangulated. |
| **D**/**E**/**F** | 변경 없음 | 변경 없음 | 0 | D5의 Felsenstein/Self-Liang 1987 spirit 표기 처리로 추가 .bib 등록 없음. |

### C.2 종합

| 지표 | Cycle 4 외부 | **Cycle 5 외부** |
|------|-----------|-----------------|
| Phase 4 평균 | 7.81 | **7.92 (+0.11)** |
| Strict 합격 | unconditional PASS | **unconditional PASS (모든 thresh 통과)** |
| Lenient 80점 | 78.1 (A-) | **79.2 (A-) — 80점 0.8 미달** |
| Defense % | 91-94% | **93-95%** |
| Unconditional pass | 72-80% | **78-85%** |

**핵심 변화**: cycle 4의 unconditional PASS가 **cycle 5에서 깊이로 두꺼워짐**. C 방법론 7.85→8.05, J 완성 7.65→7.85, I 한계 8.85→9.00 — **세 항목이 모두 +0.15 이상**. lenient 80점 통과는 **0.8 미달**로 여전히 미달이지만, defense % 추정은 +2pp 추가 회복.

---

## D. 각 측정의 evidence 가치 평가

| 측정 | 직접 영향 | 외부 가치 |
|------|---------|----------|
| **D2** 4-feature | C +0.05 / G +0.05 / I +0.05 | 진짜 statistical evidence (paired Wilcoxon p<0.001 +homoplasy)이지만 mean Δ가 작아 (+0.005) operational claim 격상은 못 함. **그러나 honest report (HCV 파괴, 4-feat regression)**는 cycle 4 sliding-window의 honest framing pattern을 그대로 계승. 단점: per-pathogen mapping coverage HCV 0.24, HIV-1 0.29 — 위원이 mapping quality 단발 질문하면 1단계 답변 (CDS-aln vs canonical protein-MSA frame disagree, frame-2 translate retry는 future). |
| **D4** Provenance | J +0.20 / I +0.05 | reproducibility의 mechanical audit가능성 — placeholder CSV → 실재 6 file. **ESM-3 excludability claim이 machine-readable (`used_in_headline_grid=No` flag)**가 가장 큰 가치. license-compatibility audit ("every load-bearing 8,580-evaluation cell uses inputs from MIT/BSD/GPL/CC-BY-class") 검증가능. submission readiness 직접 보강. |
| **D5** 4-way ω² | C +0.15 / I +0.05 | **statistical robustness의 표준 정공법**. cycle 4 wild-cluster (2-way)에서 cycle 5 4-way (block bootstrap + mixed-effects 추가). 4 frame lower bound 0.201/0.201/0.202/0.340 — Cohen large 통과 robust. Self-Liang 1987 boundary correction LRT p<10⁻¹⁹⁸은 model-based corroboration의 강한 signal. 그러나 ICC=0.135는 raw MCC 분산의 13.5%만 pathogen level — 위원 단발: "그럼 pathogen RE는 marginal 아닌가?" 1단계 답변 (LRT p<10⁻¹⁹⁸로 boundary case에서도 매우 유의 + variance-component pseudo-ω²=0.340가 Cohen large). |
| **D8** Defense notes | 간접 (defense % +2pp) | 본문 H/A/B/C/D/E/F/G/I/J 어디에도 점수 영향 없음. 그러나 Q1-Q10 verbatim 답변 + Slide A "Three Honest Disclosures" 권고가 **학생 fail trigger 거리를 추가 1단계 멀어지게**. cycle 4 시점에서 학생이 "측정 없음"으로 답변하던 상황이 cycle 5에서 "측정+verbatim anchor 외움"으로 격상. **Defense % +2pp의 직접 trigger**. |

---

## E. lenient 80점 통과?

| 단계 | Lenient 점수 | 80점 통과 |
|------|------------|----------|
| C3 외부 | 74.5 (B+) | 미달 (-5.5) |
| Phase F | 75.5 (B+) | 미달 (-4.5) |
| Cycle 4 | 78.1 (A-) | 미달 (-1.9) |
| **Cycle 5** | **79.2 (A-)** | **미달 (-0.8)** |

**판정: 80점 미달 (-0.8)이지만 회복 trajectory는 견고**. cycle 4→5에서 +1.1점 (가장 큰 회복은 Phase F→cycle 4 +2.6점). cycle 6 (가상)에서 KNU IBC TODO 해결 + B2 (H3N2 time-stratified pilot) 재시도 + D3 (DNA virus 추가) 재시도 중 1-2건만 성공해도 **80점 통과**. 그러나 cycle 5 시점 strict thresh PASS + defense 93-95%이므로 **80점 미달은 학위 통과의 binding constraint이 아님** (lenient 80점은 *우수성* 기준이지 *통과* 기준이 아님).

---

## F. Trajectory

| Cycle | 자체 점수 | 외부 점수 | Strict | Defense % | Lenient 80 |
|-------|---------|---------|-------|-----------|------------|
| Cycle 1 | 7.27 (B+) | — | 미평가 | 80% | — |
| Cycle 2 | 7.50 | — | 미평가 | 82-85% | — |
| Cycle 3 | 7.70 (A-) | 7.45 | 조건부 | 92% / 84-88% | 74.5 |
| Phase F | — | 7.55 | 조건부 (G 0.05 미달) | 86-90% | 75.5 |
| Cycle 4 | — | 7.81 | unconditional PASS | 91-94% | 78.1 |
| **Cycle 5** | — | **7.92** | **unconditional PASS (more depth)** | **93-95%** | **79.2** |

**핵심 패턴**:
- 외부 점수 회복: 7.45 → 7.55 (+0.10) → 7.81 (+0.26) → **7.92 (+0.11)**. Cycle 4의 +0.26 big jump 후 cycle 5는 보조 보강 단계 (deepening, not breakthrough).
- Defense % 회복: 84-88% → 86-90% (+2pp) → 91-94% (+5pp) → **93-95% (+2pp)**.
- **Strict thresh는 cycle 4에서 처음 PASS. Cycle 5는 모든 thresh를 더 넓은 여유로 통과** (G 7.25 → 7.30, C 7.85 → 8.05, I 8.85 → 9.00). 어떤 thresh도 cycle 5에서 추가로 위험에 빠지지 않음.
- C0 (cycle 3 시점) 자체 추정 "92% 복원" → cycle 4 외부 91-94% → **cycle 5 외부 93-95%**: in-house 낙관 추정이 외부 시각으로 finally 입증되고 **추가 안전 마진 확보**.

---

## G. 잔여 약점

1. **D3 (DNA virus 추가) 실패** — 1 DNA virus(HBV)만, 2종 비교 불가. 그러나 본문이 "single-pathogen pilot" 한정으로 frame되어 약점 노출은 minor. Defense 단발 trigger 가능성: Low.
2. **KNU IBC TODO 잔존 (ch5:359)** — cycle 5에서 D4가 ch3:1023, ch3:1033 TODO 2건 resolved, KNU IBC TODO 1건만 잔존. submission 직전 confirm 필수.
3. **D2 결과가 mixed (MCC 약간 down, AUROC 약간 up)** — 4-feature가 prospective regime에서 free lunch 아님. honest report로 cushion되었으나 "Contribution 3a 4-feature core가 prospective에서도 작동한다"는 강한 주장 못 함. 본문이 "consistent with the retrospective LOPO finding"으로 frame되어 cushion. Defense 단발 trigger 가능성: Low-Medium.
4. **D2 mapping coverage 일부 pathogen에서 낮음** (HCV 0.24, HIV-1 0.29) — frame-2 translate + region trimming retry는 future. 본문 limitation으로 명시.
5. **B2 H3N2 time-stratified pilot 부재** — cycle 4에서 API 거부, cycle 5에서 별도 시도 없음. C2 sliding-window가 11-pathogen panel로 generalization. Defense 단발 trigger 가능성: Low.
6. **lenient 80점 미달 (-0.8)** — 학위 통과의 binding constraint은 아니지만 *우수성* 기준 미달.

---

## H. 최종 권고

### H.1 Defense 진입 가능 여부 — **가능, 안전 마진 추가 확보**

| 지표 | 판정 |
|------|-----|
| Strict 합격 | **PASS (unconditional, all thresh + extra margin)** |
| Phase 4 평균 (외부) | **7.92 (A-)** |
| Defense % | **93-95%** |
| Q1 fail trigger 거리 | **3단계 (Phase F 1단계 + Cycle 4 +1단계 + Cycle 5 +1단계)** |
| 잔여 결함 | **0 critical / 0 major / 6 minor (모두 cushion)** |

### H.2 추가 작업 (defense 전 P0)

1. **KNU IBC review tag/letter ID confirm + ch5:359 TODO 제거** (1시간) — submission 정공법.
2. **Defense Q&A notes Q3/Q9에 cycle 5 Tier D5 결과 1-2 문장 추가** (30분) — 4-way ω² (block 0.202, mixed-effects 0.340)을 학생 답변에 포함.
3. **Defense 슬라이드 limitations slide 갱신** (30분) — *Three honest disclosures* (cycle 4) + *Four-frame ω² robustness* + *4-feature mixed result* 추가. cycle 4 권고된 Slide A/B/C 그대로 유지.
4. **D3 추가 시도는 권고하지 않음** — D3 실패 history + HBV null result + ch6:85 future work 등록으로 충분. Defense 직전 추가 시도는 새 결함 노출 risk.
5. **학생 자체 작업**: Q1-Q10 verbatim 답변 음독 연습 (12분 분량) + 본문 anchor (ch5:179, ch5:285, ch5:330, ch5:347-349, ch5:329, ch4:578, ch4:589, ch5:289 4-frame) line:column 외움.

### H.3 추가 작업 (defense 후, optional)

- B2 H3N2 time-stratified pilot 재시도 (epidemiology framing) — defense 후 conference paper 차원.
- D3 second DNA virus (HSV-1, Adenovirus) — DNA virus 확장 contribution 분리 가능.
- 4-feature core forward-time 재학습 (mapping coverage 향상) — 별도 cycle.
- Pre-specified TOST equivalence study (4-feature vs 10-feature) — ch6 Future Roadmap Priority 6.

### H.4 외부 판정

**unconditional PASS (학위 통과 93-95%, 추가 안전 마진 확보)**.

cycle 1 (B+, 80%) → cycle 3 (A-, 84-88%) → Phase F (조건부 86-90%) → cycle 4 (unconditional A-, 91-94%) → **cycle 5 (unconditional A-, 93-95%)**의 trajectory는 *iterative deepening의 정공법*을 cycle 4에서 입증하고 cycle 5에서 *추가 안전 마진 확보*했다. 4 measurement 적용 (D2/D4/D5/D8)으로 **strict thresh를 더 넓은 여유로 통과**, defense %를 +2pp 추가 회복, Q1 fail trigger 거리를 추가 1단계 확보. D3 실패는 점수 영향 minor (-0.02 ~ -0.05). lenient 80점 미달 (-0.8)은 학위 통과의 binding constraint 아님.

**defense 진입 권고 — 학생은 본 노트의 H.2 5건 사전 작업만 완료하면 된다**.

---

## I. 한 줄 요약

> Cycle 4의 unconditional PASS가 cycle 5에서 두 항목 (C 방법론 +0.20, J 완성 +0.20, I 한계 +0.15)에서 깊이로 두꺼워졌다. 외부 점수 7.81 → 7.92, defense % 91-94% → 93-95%. D3 실패는 대세에 영향 없음. Defense 진입 가능, lenient 80점은 -0.8 미달이지만 학위 통과 기준은 아님.
