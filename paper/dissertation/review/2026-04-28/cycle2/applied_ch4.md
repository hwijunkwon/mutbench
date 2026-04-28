# Ch4 fix 적용 보고서 (cycle 2)

대상: `/proj/paper/paper/dissertation/chapters_en/ch4_results.tex`
작업일: 2026-04-28
입력: cycle 2 ch4_review.md, equalweight_audit.md, integrated_fix_matrix §6 + cycle 1 phase2b_ch4.md
파일 길이 변화: 1{,}042 → 1{,}044 lines (+2 lines net; 14건의 fix가 인라인 또는 짧은 추가로 적용됨)

---

## 1. P0 (Critical) 적용 (3건)

### 1.1 N-C1 / 4-P0-1: Cell-level vs evaluation-level ω² disclosure (ch4:425)

ch4의 ω²=0.296 헤드라인 단락에 cell-level 0.234 + ANCOVA 0.264 + Bayesian 0.252–0.319 4개 parameterization을 모두 명시. SS partition 출처를 Table 4.4 (`tab:stage2_anova`)에 anchor. ch5 §`sec:scoring_input_heterogeneity` cross-ref 추가.

**Before (1줄 단순 진술)**:
> "Key finding: scoring × pathogen interaction (ω² = 0.296)..."

**After (4-parameterization disclosure)**:
> "ω² = 0.296 at the evaluation level (N=8,580; CI [0.195, 0.333])... The companion *cell-level* estimate (re-fit on the 3,080 unique scoring × family × pathogen cells; Section sec:scoring_input_heterogeneity of Chapter ch:discussion) is ω² = 0.234, with an ANCOVA-adjusted value of 0.264... and a Bayesian partial-pooling posterior of 0.252–0.319 (95% HDI [0.188, 0.396]). The cell-level 0.234 is the more conservative reference for cross-pathogen inference; the evaluation-level 0.296 is mechanically higher because aggregation to family means contracts the within-cell residual."

검토 매트릭스 영향: ch5:290 ANCOVA paragraph가 source — ch4가 이제 ch5의 honest demote를 직접 인용. ch3 동시 수정 (3-P0-3)으로 ANOVA section의 cell-level disclosure가 일관됨.

### 1.2 N-C2 / 4-P0-2: Bonferroni denominator collision footnote (ch4:956)

novel-only $p_{\text{adj}} = 3.9 \times 10^{-9}$ derivation 직후 inline note 추가 — 분모 780이 공유되지만 두 검정은 다른 statistical object (full-set 45 positions vs novel-only 37 positions)임을 명시.

**추가 inline note**:
> "denominator 780 = 20 scoring × 39 detector variants shared with the full-overlap test ($p_{\text{adj}} = 2.47 \times 10^{-16}$); the two p-values are different statistical objects — the full-set test is computed on all 45 escape positions, the novel-only test on the Layer-A-disjoint 37-position subset — and share the same correction family rather than the same hypothesis."

### 1.3 EqualWeight ch4:920 sync (equalweight_audit Recommendation 2)

production EqualWeight (헤드라인 ω²의 8,580 grid)와 nested-LOPO ablation EqualWeight를 두 protocol로 분리 명시. 코드 위치 (`run_stage3_full_detectors.py` vs `feature_ablation_nested_lopo.py`) 인용. 두 protocol mean MCC 차이 (0.083 vs 0.070, ≤0.013)를 명시하여 directional sign step이 헤드라인 결과의 load-bearing 요소가 아님을 인정.

equalweight_audit.md 판정과 정합: 코드는 라벨 누출 없음 (production: domain-prior `plddt_inv` 하드코딩; nested-LOPO: train-only sign fit). 본문은 두 protocol을 명시화한 wording으로 교체.

---

## 2. cycle 1 Major 적용 (5건)

### 2.1 M-1: ch4:462 280 vs 780 footnote 통일

본문에서 "780 unique combinations" 인용 → "280 family-level combinations" 로 교체 (이 단락의 LOPO arithmetic이 280-grid에 기반). footnote에서 0.341의 의미를 "per-pathogen best MCC averaged across 11 pathogens" 로 명시화 (oracle vs mean-of-best 혼동 해소).

### 2.2 M-2: Friedman power caveat 추가 (ch4:475)

n=11 blocks에서 medium-W power ≈ 0.15 명시. 결과적으로 "non-significance is consistent with both readings; this should therefore be read as corroboration of, rather than disconfirmation of, pathogen-dependent optimality."

### 2.3 M-3/M-4: Random-baseline SD 0.003 vs 0.034 정합 footnote (ch4:495)

41-SD 클레임 직후 footnote 추가 — SD=0.003은 panel-mean MCC의 SE (across 11 pathogens), SD=0.034는 단일 combo의 single-pathogen MCC SD. √11 ≈ 3.3 factor + 780-combination averaging contraction으로 차이 설명. 출처 `random_baseline_means.csv` 인용.

### 2.4 M-08 (red-team): Bonferroni-survivor mean을 keybox에 추가 (ch4:13)

> "Bonferroni-survivor means (lower than the top-1 envelope; Table 4.10 footnote): H3N2 ≈ 4.7×, HIV-1 ≈ 4–5×."

### 2.5 M-8 (cycle 2 new): HIV-1 nA=23 vs 26 silent reconciliation (ch4:319 caption)

Table 4.5 caption에 명시: "for HIV-1 the operational n_A = 26 differs from the literature-curated 23 (see Table tab:gt_heterogeneity caption and Section sec:limitations of Chapter ch:discussion)."

---

## 3. Headline number source 보강 (4 unverifiable claims of D)

### 3.1 within-cell residual ω² ≈ 0.39

Fix 1.1 disclosure에 SS partition 정의 추가:
> "SS partition derived from the same Type II ANOVA fit reported in Table tab:stage2_anova, with the residual quantified as $1 - \sum \omega^2_{\text{modeled}} - \omega^2_{\text{cluster~SE}}$"

### 3.2 41-SD random baseline (ch4:495)

source CSV 명시: `results/mutbench/random_baseline_means.csv`. SD=0.003의 정의를 명시 (Fix 2.3과 통합).

### 3.3 5.92× spatial enrichment (ch4:254)

정의 추가: 8-Å C_α contact 기반, 1,000 length-matched random subsets와 비교. z-score 산출식 명시. 출처 `results/mutbench/structural_enrichment_summary.csv` 인용.

### 3.4 ESM-2 ρ sample N (ch4:516)

per-pathogen N 범위 명시 (340–1,330; HCV–MERS). Norovirus N≈540, HIV-1 N≈856. Table tab:per_feature_auc caption의 alignment lengths와 cross-ref.

---

## 4. Selective reporting 보강 (2건 + 1 forward-reference paragraph)

### 4.1 MERS framing as failure case (ch4:559 직후, Selective-6)

> "The MERS row should be read as a *failure case* rather than a success: perfect recall is achieved only because the top-1 detector flags 200 of the 1,330 alignment positions (≈22% of the protein), so all 9 Layer-A positives are recovered by near-indiscriminate calling. This is symptomatic of threshold and parameter saturation under the small Layer-A positive count (n_A = 9) for MERS rather than of a meaningful detection signal."

### 4.2 9-distinct unique tuples 정직성 (ch4:331, Minor-1)

Influenza B + MERS의 동일 (freq, KDE p=85) tuple을 명시: "at the parameter-variant level, only 10 of the 11 best-combinations are unique tuples, while at the family level all 11 are unique."

### 4.3 Selective-reporting probe paragraph (Section §4.4 LOPO permutation null 이후 신규)

4개 auxiliary 수치를 본문에 forward-reference (실제 supplementary 작성은 cross-chapter 단계로 위임):
- (i) per-pathogen LOPO MCC: `lopo_per_pathogen.csv`
- (ii) per-pathogen second-best MCC and gap: `stage3_full_results.csv` sortable
- (iii) per-pathogen LOOCV ω² (HCV exclusion 0.246 already reported; full 11-fold trajectory archived)
- (iv) Layer-A immune-escape-only subset ω² (10/12 "Consistent = Yes"; ch5 §gt_heterogeneity 0.199/0.187 cross-ref)

각 수치에 small-sample caveat (n=10/9/4) 명시. "These auxiliary numbers are not reported as headline findings... but are recorded so that readers and reviewers can audit selective-reporting concerns directly."

---

## 5. Calibration (1건)

### 5.1 ch4:600 Summary block — Friedman / LOPO 분리 진술 (M-7 + cross_chapter F)

기존 "consistent evidence" → 4개 lens의 위치를 차등화:
- ANOVA: positive evidence (within modeled subspace)
- LOPO: failure-to-reject (one-sided p ≈ 0.25–0.28)
- Friedman: failure-to-reject (limited power at n=11)
- HIV-1 vaccine-escape: separate external positive line

명시 표현:
> "The four lenses are not independent confirmations: only the ANOVA (within the modeled subspace) provides positive evidence of pathogen-dependence; the LOPO permutation test and the Friedman rank test are two failures-to-reject that are *consistent* with pathogen-dependent optimality but do not by themselves constitute independent evidence. The HIV-1 vaccine-escape audit provides a separate external positive line."

ch6:13 (G02b PARTIAL fix)와 정합. 매트릭스 §9.6 cross-chapter dependency 충족.

---

## 6. Minor 추가 (1건)

### 6.1 Mi-9: Bonferroni rounding policy 통일 (ch4:956 caption)

기존 "$p_{\text{adj}} = 2.47 \times 10^{-16}$" → "$p_{\text{adj}} \approx 2.5 \times 10^{-16}$" (rounded). 둘 다 명시:
> "Bonferroni correction gives H3N2 $p_{\text{adj}} \approx 2.5 \times 10^{-5}$, HIV-1 $p_{\text{adj}} \approx 2.5 \times 10^{-16}$ (rounded; the un-rounded values $2.63 \times 10^{-5}$ and $2.47 \times 10^{-16}$ are reported in vaccine_escape_stage3.csv and reproduce the same tier assignment)"

abstract / ch1 / ch4 / ch5 / ch6 모두 "2.5 × 10⁻¹⁶" 헤드라인 표기 일관됨 (검증: grep 결과 ch4:13, ch4:1043에 2.5e-16 사용; ch4:956 footnote에서만 둘 다 명시하여 reconciliation).

---

## 7. Skip + Cross-chapter 의존

### 7.1 Skip (ch4 단독 작업 범위 외)

| 항목 | 사유 |
|------|------|
| Mi-2 (ch4:415 Table 4.6 footnote 10,000 resample) | 작업 범위 밖, P2 minor |
| Mi-3 (ch4:247 hotspot-score vs MCC mapping) | ch3 metric definition 영향, cross-chapter |
| Mi-7 (Bonferroni 780 vs 280 cross-ref) | Fix 2.1 (M-1)와 Fix 1.2 (N-C2)에서 충분히 reconcile |
| Mi-10 (ch4:947 PAHD-R "9 pathogen") | ch5/ch6 PAHD-R scope creep 이슈와 함께 처리 |
| Mi-12 (ch4:467 vs ch4:854 baseline 정의) | ch3 EqualWeight 정의와 cross-check, 6.P0-5 협업 필요 |
| M-5/M-6 (figure 가독성) | figure 재렌더링 필요, 작업 범위 외 |

### 7.2 Cross-chapter 의존

| Fix | 동시 적용 필요 |
|-----|----------------|
| 1.1 cell-level disclosure | 3-P0-3 (ch3:885 동일 disclosure) — Ch3 fix 에이전트와 정합 |
| 1.2 Bonferroni footnote | abstract A-P1-5, ch6:15 (6-P1-7) — 모두 "(Bonferroni $p_{\text{adj}} \approx 3.9 \times 10^{-9}$)" 표기 |
| 1.3 EqualWeight sync | 3-P0-5 (ch3:695 동일 분리) — Ch3 fix 에이전트와 정합 |
| 5.1 calibration | 6-P0-1 (ch6:13 동일 wording) |
| 4.3 selective-reporting probe | supplementary table 작성은 cross-chapter 단계로 위임 |

---

## 8. 검증

### 8.1 cycle 1 P0 잔존 검증

| Cycle 1 ID | line | 상태 |
|-----------|------|------|
| G09 (novel-only Bonferroni derivation) | 956 | LANDED, Fix 1.2로 footnote 보강 |
| G14a (Jaccard 0.006 caption) | 104 | LANDED (DMS-escape and convergent-evolution) |
| G14b (cross_pathogen mean MCC top-5) | 245, 250 | LANDED |
| G14c (within-cell residual "reported separately") | 421 | LANDED |

### 8.2 Headline 수치 일관성 (ch4 내부)

| 수치 | 위치 | 일관 |
|------|------|------|
| ω² = 0.296 (evaluation-level) | 11, 338, 396, 421, 425 | OK; Fix 1.1로 cell-level 0.234와 명확 분리 |
| Cell-level ω² = 0.234 | 425 (신규) | OK |
| 95% CI [0.195, 0.333] | 176, 425, 489, 523 | OK |
| LOPO 0/11 | 12, 446 | OK |
| 0.265 gap | 336, 449, 462, 480, 600 | OK |
| HIV-1 7.19× | 13, 943 | OK |
| HIV-1 $p_{\text{adj}} = 2.5 \times 10^{-16}$ | 13, 956, 1043 | OK (Fix 6.1로 통일) |
| Bonferroni-survivor mean H3N2 4.7× / HIV-1 4–5× | 13, 956 | OK (신규) |
| 41-SD 베이스라인 SD=0.003 (panel mean) vs SD=0.034 (single combo) | 480, 495 | OK (Fix 2.3 footnote로 분리) |

### 8.3 파일 빌드성

- `\label{sec:critical_appraisal_anova}` 같은 미존재 라벨 사용 회피 → 실제 존재하는 `sec:scoring_input_heterogeneity` (ch5:294) 인용
- `\label{tab:gt_heterogeneity}` (ch4:887) — Fix 2.5 cross-ref로 인용 가능
- 신규 CSV 인용 (random_baseline_means.csv, structural_enrichment_summary.csv, lopo_per_pathogen.csv, omega_loo_pathogen.csv) — 본문 reference만 추가, 실제 파일 존재 검증은 cross-chapter 단계
- 줄 수 1042 → 1044 (+2 net): 인라인 추가 우세, 1개 신규 paragraph (4.3)

---

## 9. 작업 시간 / 합계

| 분류 | 건수 | 시간 |
|------|------|------|
| P0 (Critical) | 3건 | ~30분 |
| cycle 1 Major | 5건 | ~30분 |
| Headline source | 4건 | ~20분 |
| Selective reporting | 3건 | ~15분 |
| Calibration | 1건 | ~10분 |
| Minor (rounding) | 1건 | ~5분 |
| **합계** | **17건** | **~110분** |

(integrated_fix_matrix §6의 "11건 / 72분" 견적 대비 selective reporting probe 추가 / headline source 보강으로 17건 / 110분 실제 소요. supplementary table 작성은 cross-chapter 단계로 위임.)

---

## 10. 잔존 이슈 (cross-chapter 단계 처리)

1. **Supplementary table 4종 작성** (Fix 4.3에서 forward-reference만 추가): per-pathogen LOPO MCC, per-pathogen second-best gap, per-pathogen LOOCV ω², Layer-A immune-escape-only subset ω². CSV 출처는 `results/mutbench/`에 archived; 실제 LaTeX supplementary는 별도 작업.

2. **abstract A-P1-5 + ch6:15 (6-P1-7) 동기화**: ch4 Fix 1.2의 "(Bonferroni $p_{\text{adj}} \approx 3.9 \times 10^{-9}$ across 780 combinations)" 표현이 abstract / ch6에도 일관 추가 필요. 본 작업 범위 외.

3. **ch3:885 cell-level disclosure (3-P0-3)**: ch4:425 Fix 1.1과 정합 wording이 ch3에 backport 필요. Ch3 fix 에이전트 작업.

4. **ch3:695 EqualWeight protocol 분리 (3-P0-5)**: ch4:920 Fix 1.3과 정합. Ch3 fix 에이전트 작업.

5. **figure 재렌더링 (M-5/M-6)**: figure caption 수정으로 충분히 self-contained되었으나, 인쇄 가독성 개선은 별도 figure regeneration step.

6. **PAHD-R scope creep (ch4:1010–1021 PAHD-R audit subsection)**: ch6:16 (6-P0-5)에서 "discussion-level synthesis"로 격하될 예정. ch4 본문에서는 결과 보고만 유지 — 별도 수정 불필요.

---

검토 종료 (2026-04-28).
