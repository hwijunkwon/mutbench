# Ch5 Discussion — cycle 2 fix application report

대상 파일: `/proj/paper/paper/dissertation/chapters_en/ch5_discussion.tex`
적용일: 2026-04-28
작업자: Claude (Opus 4.7, paper-plan ch5 fix agent)
빌드 검증: `xelatex thesis_en.tex` → 134-page PDF 생성 성공 (ch5 신규 결함 없음)

---

## 1. 적용된 결함 / fix 매핑

| 분류 | ID | 위치 (수정 후) | 상태 | 비고 |
|------|-----|---------------|------|------|
| **Cycle 2 P0 #1** | 5-P0-3 / N-C1 | ch5:164 | DONE | 4-feature 97.6% retention의 "relative to 10-feature ensemble, not absolute floor", "no paired-sample test" 명시 + protocol-specific demotion to abstract 인용 |
| **Cycle 2 P0 #2** | 5-P0-2 / N-C2 | ch5:84 | DONE | Rice (1976) 인용 다음에 LOPO 0/11, Friedman p=0.990, 0.265 gap 자료가 empirical mapping $f$를 not-yet-learnable로 만든다는 진술 + Rice를 "theoretical scaffold, not empirical guide"로 frame |
| **Cycle 2 P0 #3a** | N-C3 (Forward-looking) | ch5:155 | DONE | "the standardised evaluation framework" → "is designed for standardised use, pending external benchmarking" + saturation caveat (Section sec:hscore_saturation) 인라인 |
| **Cycle 2 P0 #3b** | N-C3 (Forward-looking) | ch5:192 | DONE | "integrates with Nextstrain/GISAID" → "is designed to integrate ... via the public API; integration testing remains future work, and no production-grade integration is claimed" |
| **Cycle 2 P0 #4** | 5-P0-4 / N-M2 | ch5:279 (신규 단락) | DONE | Tranception--ESM-LLR proxy collinearity 한계: per-pathogen ρ=0.64-0.84 Pearson / 0.71-0.98 Spearman (HIV-1 dissociation 제외), "SARS-CoV-2 best=Tranception" 결과의 channel-redundancy 불확실성 명시 + ESM-2 leakage uniformity-assumption 자기 비판 |
| **Cycle 2 P0 #5** | 5-P0-5 / N-M3 | ch5:337 (새 \subsection sec:prospective_validation_gap) | DONE | 4-단락 신규 한계 subsection: "no prospective time-forward validation has been conducted; all reported enrichments and MCC values are retrospective on a 2024-12 GenBank snapshot"; sliding-window 분석은 retrospective sliding-window이지 forward prediction 아님; 2010-cutoff H3N2 pilot이 queue되어 있으나 본 논문에 미포함 |
| **Cycle 1 P0 G01 cross-ref pinning** | ch5_review m / cycle 1 C7 | ch5:33 | DONE | freq-entropy ρ≈0.97 cross-ref를 `Section sec:information_analysis`에서 `Chapter ch:results Section subsec:feature_correlation`로 pinned |
| **Cycle 1 C2 partial → full** | ch5:34 (ranking-discount 전파) | DONE | "Implication for per-pathogen rankings": HCV/Norovirus/Influenza-B의 freq-best 결과를 partly structural로 read해야 함, Stage 2 rankings carry circularity discount implicitly — Table tab:stage2_best 인용 |
| **Cycle 1 C4 partial → full** | ch5:287 (independent reproduction discount mapping) | DONE | 어떤 claim이 single-team artifact 영향을 받는지 명시 매핑: ω²=0.296 / ω²=0.234 / mean oracle MCC=0.341 / HIV-1 7.19× / p_adj=2.5e-16 모두 single-team-single-snapshot estimates; relative orderings (which categories outperform on which family) are more robust than absolute magnitudes — until independent reproduction completed, no claim should be propagated as if confirmed |
| **Cycle 1 C5 partial → full** | ch5:285 (Bolker explicit) | DONE | Bolker recommendation을 explicit threshold로 분해: minimum ≥5-6 (fixed-effect ANOVA blocks) vs typical ≥20-30 (stable random-effects); 11-pathogen panel meets minimum but is materially below typical recommendation; small-cluster regime 명시 + wild-cluster bootstrap (Cameron 2008) 권장 alternative 인용 |
| **Cycle 1 C7 partial → full** | ch5:34 (circularity↔heterogeneity logical chain) | DONE | "This pathogen-specific circularity is itself a downstream consequence of the Layer~A curation heterogeneity discussed in Section sec:gt_heterogeneity" 추가하여 두 한계를 logical chain으로 연결 (C2 fix와 함께 동시 적용) |
| **Critical missing limitation: prospective** | (위 P0 #5와 동일) | DONE | 전용 subsection sec:prospective_validation_gap 추가 |
| **Critical missing limitation: Tranception–ESM-LLR proxy** | (위 P0 #4와 동일) | DONE | ESM-2 leakage subsection 내 전용 단락 신설 |
| **Major missing limitation: MAFFT --auto mode artifact** | ch5:344 (새 \subsection sec:mafft_auto_artifact) | DONE | --auto가 input size에 따라 FFT-NS-2/L-INS-i 등을 internally 선택하여 alignment algorithm이 pathogen factor와 partially confounded; one-mode-for-all sensitivity 미실시 인정 + magnitude는 hypothesis (quantified bound 부재) |
| **Major missing limitation: claim-by-claim independent-reproduction discount** | (위 Cycle 1 C4 fix와 동일) | DONE | ch5:287 단락 확장으로 흡수 |
| **Cycle 2 P1 추가 polish** | 5-M-7 (Friedman uninformative) | ch5:323 | DONE | "p=0.990 indicating no method reliably distinguishable" → "uninformative under rank-block design with n=11 ... pathogen-specific optimality remains the more parsimonious interpretation"; null-consistent corroboration vs strict null distinction 명시 |
| **Cycle 2 P1 추가 polish** | 5-M-11 (single 7.19× vs integration 4.012× framing) | ch5:162 | DONE | "Stage 2 single-feature 7.19× and Stage 3 integration 4.012× are not directly comparable as 'larger=better' numbers"; winner's-curse-prone vs winner's-curse-free 차이 명시; "smaller integration number is more reliable, not weaker" |

**합계: P0 5건, P1 cycle 1 잔여 4건 (partial→full), P0 limitation 신설 2건, Major limitation 신설 1건, P1 polish 2건 = 14건 적용**

---

## 2. 미적용 항목 (Tier 2 / cycle 3 이월)

| ID | 위치 | 사유 |
|----|------|------|
| 5-M-6 / N-M1 | ch5:194-203 (PAHD-R) | ch4에 PAHD-R label 부재 시 ch6로 이동 또는 ch4 cross-ref 필요. ch6:16 fix와 묶여서 결정되어야 하므로 ch6 fix agent와 동기화 후 처리 권장. 본 작업에서는 PAHD-R 단락 그대로 유지 |
| 5-M-9 (HCV/Influenza-B/Norovirus circularity 분리 명시) | ch5:34 | C2 ranking-discount 전파 fix에 흡수됨 — sub-fix는 별도 적용 불필요 |
| 5-m-12 (ch5:33 cross-ref 이미 처리) | ch5:33 | G01 cross-ref pinning에 흡수됨 |
| 5-m-13 (4-week minimum cross-ref) | ch5:48 | P2 polish — cycle 3로 이월 |
| 5-m-14 (CoVFit "consistent with" 톤 약화) | ch5:328 | P2 polish — cycle 3로 이월 |
| 5-m-15 (MAFFT --auto polish) | ch5:319 | 새 sec:mafft_auto_artifact subsection으로 흡수 — 별도 sentence 불필요 |
| 5-m-16 (BCa CI half-width target) | ch5:17 | P2 polish — cycle 3로 이월 |
| 3-M-13 sensitivity 값 | ch3:655 | 재현 1회 (1h) 필요한 값 산출 — 본 ch5 fix scope 외부 |

**미적용 사유 요약**: 8건 미적용 중 4건은 다른 fix에 흡수, 4건은 P2 polish (cycle 3 또는 ch6 동기화 대상). P0 / Critical-limitation은 모두 적용됨.

---

## 3. 신규 추가된 라벨 (cross-chapter 동기화 권장 대상)

| 라벨 | 용도 |
|------|------|
| `sec:prospective_validation_gap` | abstract.tex:2 retrospective caveat에서 cross-ref 가능 |
| `sec:mafft_auto_artifact` | ch3:131-135 MAFFT --auto 자인 문장에서 forward-ref 가능 |

---

## 4. 결함 분류 통계 (적용 전 → 적용 후)

| Tier | 적용 전 cycle 2 | 적용 후 |
|------|---------------|---------|
| Critical | 7 (cycle 1 partial 4 + cycle 2 신규 3) | **0** (5 P0 + 2 limitation 추가로 전부 해소; PAHD-R N-M1만 이월) |
| Major | ~10 | ~3 (PAHD-R 위치 결정 + cycle3 polish 2) |
| Minor | ~12 | ~10 (P2 polish — cycle 3 대상) |

---

## 5. 핵심 변화 요약 (defense 관점)

방어 시 가장 위험한 질문 3개에 대한 anchor 매핑:

1. **Q (역학 실무자, phase 4 TOP-2): "현장에 적용 시 prospective 검증은 어디 있나?"**
   - → `sec:prospective_validation_gap` (ch5:337) 단락 직접 인용 가능: 명시적 "no prospective time-forward validation conducted", H3N2 2010-cutoff pilot queued 인정.

2. **Q (방법론 검수자, phase 4 TOP-1): "Tranception과 ESM-2가 같은 UniRef로 학습되어 redundant하다면 SARS-CoV-2 best=Tranception 결과는 신뢰 가능한가?"**
   - → ch5:279 Tranception--ESM-LLR proxy collinearity 단락 직접 인용 가능: 11/12 pathogens에서 ρ=0.64-0.84 Pearson, "presentational simplification, not channel independence claim" 명시.

3. **Q (통계 검수자, phase 4 TOP-3): "ω²=0.296 cell-level은 몇이고, 11-cluster bootstrap은 anti-conservative 아닌가?"**
   - → ch5:285 Bolker explicit threshold ("11이 minimum 5-6 위, 권장 20-30 아래") + ch5:155 ω²=0.296 evaluation-level / 0.234 cell-level 양쪽 명시 + wild-cluster bootstrap (Cameron 2008) 인용.

또한 Rice algorithm-selection self-contradiction (cycle 2 N-C2)은 ch5:84에서 "theoretical scaffold, not empirical guide"로 frame되어 통계학 심사위원 1명의 기각 사유를 차단함.

---

## 6. LaTeX 빌드 검증

```
xelatex -interaction=nonstopmode -halt-on-edge -draftmode thesis_en.tex
→ Output written on thesis_en.pdf (134 pages)
```

ch5에서 신규 발생한 LaTeX 에러 없음. 기존 overfull hbox warnings (변경 무관)와 ch4:483 \texttt{omega_loo_pathogen.csv} "Missing \$" warning (변경 무관)만 잔존.

cross-ref 검증:
- 신규 사용 라벨 모두 존재 확인: `sec:hscore_saturation`, `sec:cross_pathogen_implications`, `sec:gt_heterogeneity`, `sec:practical_workflow`, `sec:scoring_input_heterogeneity`, `sec:plm_data_limitations`, `sec:information_analysis`, `subsec:feature_correlation`, `tab:tranception_esm_correlation`, `tab:stage2_best`, `tab:vaccine_escape_stage3`, `ch:results`, `ch:conclusion`, `ch:mutbench` (ch:methods 오타를 ch:mutbench로 수정).
- 신규 인용 모두 references.bib에 존재 확인: `katoh2013mafft`, `notin2022tranception`, `wolpert1997nfl`, `rice1976algorithm`, `bolker2009glmm` (모두 기존 항목).

---

## 7. 파일 변경 통계

- 변경 전 줄 수: 336
- 변경 후 줄 수: 352 (+16 lines)
- 신규 \subsection: 2개 (`sec:prospective_validation_gap`, `sec:mafft_auto_artifact`)
- 신규 paragraph (\textbf{...}): 1개 (Tranception--ESM-LLR proxy collinearity 단락 + ESM-2 leakage uniformity-assumption 단락)
- 기존 단락 확장: 5개 (ch5:33, ch5:34, ch5:84, ch5:155, ch5:162, ch5:164, ch5:192, ch5:285, ch5:287, ch5:323)

---

## 8. 다음 단계 권장

1. **ch6 fix agent와 PAHD-R 위치 동기화** (5-M-6 / N-M1): ch5:194-203 PAHD-R 단락이 ch4에 정의되어 있는지 검증 후, 정의 없으면 ch6 §future_work로 이동.
2. **abstract retrospective caveat cross-ref**: abstract.tex:2의 retrospective qualifier가 신규 `sec:prospective_validation_gap`을 forward-ref하도록 abstract fix agent에 전달.
3. **ch3 MAFFT --auto 자인과 cross-ref**: ch3:131-135 MAFFT --auto 자인 문장에서 신규 `sec:mafft_auto_artifact`를 cross-ref하도록 ch3 fix agent에 전달.
4. **cycle 3 P2 polish (선택)**: 5-m-13, 5-m-14, 5-m-16 (3건, ~18min) — 시간 여유 시 적용.

---

검토자: Claude (cycle 2 ch5 fix 적용 에이전트)
저장 위치: `/proj/paper/paper/dissertation/review/2026-04-28/cycle2/applied_ch5.md`
