# Phase E 잔여 결함 패치 보고

Date: 2026-04-28
Cycle: 3 / Phase E (post-Phase-D residuals)
Scope: 7 patches across ch1, ch2, ch4, ch5, ch6 covering Critical regression (Greaney mis-anchor), Critical regression (4 phantom CSVs), Major (FUBAR count drift, contribution count convention, ω² CI), Major-cosmetic (PAHD-R cross-ref), and Critical Ch1 self-contradiction.
Build: xelatex + bibtex + xelatex×2, 238 pages, 0 errors, 0 undefined refs, 0 multiply-defined labels.
verify_dissertation.py: 90 PASS / 0 FAIL / 0 WARN.

---

## 1. Ch1 L150 자체-모순 수정 (1-P0-8 잔존 / cycle3 B-1 / Major)

**Before** (chapters_en/ch1_introduction.tex:150)
> ...the operational claim of equivalence is anchored on the nested-LOPO test.

**After**
> ...the non-rejection of inferiority is anchored on the nested-LOPO test (paired delta $+0.011$~MCC, 95\% CI [$-0.018$, $+0.042$], sign-flip permutation $p = 0.61$, within the $\pm 0.04$~MCC bound stated below).

L150과 L152가 같은 단락에서 충돌하던 어구("operational claim of equivalence" vs "non-rejection of the inferiority hypothesis ... not as a pre-specified equivalence claim")을 통일. 두 문장 모두 동일 nested-LOPO 결과를 인용하며 paired Δ / CI / p값을 명시.

---

## 2. Ch2 L109 Greaney mis-anchor 수정 (cycle3 B.1 / Critical 회귀)

**Before** (chapters_en/ch2_background.tex:109)
> ...These antibody-escape DMS datasets, together with the Bloom-lab broader escape-DMS catalog, are the direct experimental antecedent of the Layer~C cross-validation paradigm used in MutBench (Section~\ref{sec:cross_validation_escape}, Chapter~\ref{ch:results})...

**After**
> ...(both SARS-CoV-2-specific). These SARS-CoV-2 antibody-escape DMS datasets, together with the Bloom-lab broader escape-DMS catalog, are the direct experimental antecedent of the **vaccine-escape cross-validation analysis** reported in Chapter~\ref{ch:discussion} (Section~\ref{sec:cross_validation_escape}; results tabulated in Chapter~\ref{ch:results} Table~\ref{tab:vaccine_escape_stage3}), which audits per-pathogen MutBench top-$k$ output against curated antibody-/vaccine-escape position lists for HIV-1 (Moore--Williamson 2015), H3N2 (Lee et al.~2018) and SARS-CoV-2. Layer~C ground truth in MutBench remains *fitness*-DMS based and is sourced from Dadonaite et al.~2024 (SARS-CoV-2 cell entry), Lee et al.~2018 (H3N2 replicative fitness), Haddox et al.~2018 (HIV-1 viral growth in TZM-bl), Simonich et al.\ (RSV), Aditham et al.\ (Rabies) and Bakhache et al.\ (EV-A71); see Section~\ref{subsec:bg_dms} of this chapter and Table~\ref{tab:gt_positions} of Chapter~\ref{ch:mutbench}. The two ground-truth tracks are therefore orthogonal: antibody-escape DMS feeds the vaccine-escape audit, fitness-DMS feeds Layer~C, and each contributes a distinct per-position evaluation signal that is largely independent of literature-curated adaptive positives (Layer~A) and of purifying-selection negatives (Layer~B).

**Layer C vs vaccine-escape 명확화**:
- antibody-escape DMS (Greaney) → **vaccine-escape audit** (ch4 Table~\ref{tab:vaccine_escape_stage3}, ch5 Section~\ref{sec:cross_validation_escape})
- fitness-DMS (Dadonaite/Lee/Haddox/Simonich/Aditham/Bakhache) → **Layer C**
- Greaney is SARS-CoV-2-specific 명시
- 7.19× HIV-1 anchor는 vaccine-escape audit의 결과 (Layer C가 아니라 Moore-Williamson 2015 escape position list)

**Cross-ref 정정**: 원본은 `sec:cross_validation_escape`를 ch:results에 위치한다고 잘못 적시(실제는 ch:discussion 169 line). `tab:gt_layers`(존재하지 않음) → `tab:gt_positions` (ch3:365 실존)으로 대체.

---

## 3. Ch2 L61 FUBAR count drift 수정 (cycle3 B.2 / Major)

**Before** (chapters_en/ch2_background.tex:61)
> MutBench incorporates four FUBAR-derived per-site selection summaries as scoring channels (Chapter~\ref{ch:mutbench}, Section~\ref{sec:scoring_detection}), enabling direct comparison...

**After**
> MutBench incorporates four phylogenetic selection-pressure scoring channels---three FUBAR-derived posterior summaries (FUBAR posterior probability, FUBAR positive-selection indicator, FUBAR Bayes factor) plus a Nei--Gojobori dN/dS proxy (Chapter~\ref{ch:mutbench}, Section~\ref{sec:scoring_detection})---enabling direct comparison of selection-based features against frequency-based and PLM-based alternatives within a unified framework. FEL, SLAC, and BUSTED are reviewed here for completeness of the HyPhy family but are not benchmarked as scoring channels in the present panel; coverage of the broader selection-test family is left to future work (Chapter~\ref{ch:conclusion}).

ch3:611-614/640 ("three FUBAR-based scores + dN/dS proxy")와 ch4:293과 정합. cycle3 B.4 (FEL/SLAC/BUSTED scope mismatch)도 같은 패치로 동시에 닫힘 — FEL/SLAC/BUSTED가 panel에 미포함이며 future-work로 처리됨을 명시.

---

## 4. Ch4 phantom CSV 4건 정정 (cycle3 C1 / Critical 회귀)

| CSV | 처리 | 매핑 / 제거 / supplementary |
|---|---|---|
| `lopo_per_pathogen.csv` (ch4:483) | **(a) 매핑** | → `lopo_9pathogen_cv.csv` (실존; held_out / test_mcc / oracle_mcc 컬럼) |
| `omega_loo_pathogen.csv` (ch4:483) | **(a) 매핑** | → `cluster_bootstrap_omega_loo.csv` (실존; excluded_pathogen / omega2 컬럼; 11-fold LOOCV) |
| `random_baseline_means.csv` (ch4:497) | **(b) supplementary** | "per-pathogen means computed from the 780-combination random-assignment distribution underlying the LOPO permutation null --- see permutation-null block above; the per-replicate panel-mean draws are queued for release as a supplementary CSV with the Zenodo provenance bundle"로 재서술. 41-SD 비교 anchor는 보존. |
| `structural_enrichment_summary.csv` (ch4:254) | **(b) 부분 매핑 + supplementary** | "per-permutation null draws under preparation as a supplementary CSV; pairwise contact source data are archived in `results/mutbench/structural_features/` and the per-pathogen 3D contact tables in `hotspot3d_results.csv`"로 대체. 5.92× / z=13.34 anchor 보존. |

**검증**: `grep "lopo_per_pathogen|omega_loo_pathogen|random_baseline_means|structural_enrichment_summary"` over chapters_en/ + front_en/ + back/ → 0 hits 후-패치.

**부수효과**: ch5 cycle3 re-attack B.2가 언급한 ch4:483 underscore-in-`\texttt{}` build error도 같은 edit에서 해소 (`omega\_loo\_pathogen.csv`는 `cluster\_bootstrap\_omega\_loo.csv`로 교체되며 underscore 모두 escape됨).

---

## 5. Ch5 PAHD-R cross-ref 추가 (cycle3 C-Minor / Major-cosmetic)

**Before** (chapters_en/ch5_discussion.tex:200)
> PAHD-R narrows the gap between the ceiling and floor without erasing the limitation.

**After**
> PAHD-R narrows the gap between the ceiling and floor without erasing the limitation (definitional anchor and the full algorithmic specification reside in Chapter~\ref{ch:results}, Section~\ref{subsec:adaptive_weighting_limits}, ``PAHD-R redesign audit'' paragraph (\ref{para:pahd_r_redesign_audit}); this section provides the interpretive synthesis only).

**부수 추가**: ch4_results.tex:1012에 `\phantomsection\label{para:pahd_r_redesign_audit}` 추가. `subsec:adaptive_weighting_limits` (ch4:1000)는 기존 label.

---

## 6. Ch6 contribution counting convention 통일 (cycle3 M3-1 / Major)

**Before** (chapters_en/ch6_conclusion.tex:10)
> This dissertation contributes four results, organized as Contributions~1, 2, 3a, and 3b.

**After**
> This dissertation presents four results that map to three contributions, with Contribution~3 reported in two parts (3a and 3b).

ch1:155 "These three contributions form a logical hierarchy" / abstract:11 "Contribution 3 is two-part" 표현과 word-count 일치 ("three contributions"). ch6 본문의 (3a)/(3b) bold marker는 그대로 유지.

---

## 7. Ch6 ω² 95% CI 추가 (cycle3 m3-1 / Minor)

**Before** (chapters_en/ch6_conclusion.tex:12)
> $\omega^2=0.296$ at 20-type granularity; 0.103 at 6-category granularity

**After**
> $\omega^2=0.296$ at 20-type granularity, 95\% cluster-bootstrap CI [0.195, 0.333]; 0.103 at 6-category granularity

abstract:2/abstract:10/ch1:148이 carry하는 95% CI를 ch6에서도 동일하게 표시.

---

## 8. verify_dissertation.py 결과

```
[PASS] 90
[FAIL] 0
[WARN]  0
Total checks: 90

No failures detected.
```

7개 카테고리 (forbidden patterns / key statistics / CSV vs table / LaTeX structure / scoring formula vs code / permutation formula / MOSD weight) 전부 PASS. cycle3 C1 (phantom CSV)도 reverify 결과 회귀 없음.

---

## 9. xelatex 빌드 결과

- **xelatex pass 1**: clean, output 238 pages
- **bibtex**: clean (`The top-level auxiliary file: thesis_en.aux`)
- **xelatex pass 2**: clean, 238 pages
- **xelatex pass 3**: clean, 238 pages

**Errors**: 0 (`grep "^!" thesis_en.log` → 0 hits)
**Undefined references**: 0 (`grep "Reference.*undefined" thesis_en.log` → 0 hits)
**Undefined citations**: 0
**Multiply-defined labels**: 0
**Warnings**: only Underfull/Overfull \hbox typesetting warnings (CJK Korean abstract font kerning); structural integrity intact.

새로 추가한 cross-ref 모두 해소:
- `subsec:adaptive_weighting_limits` (ch4:1000) — 기존
- `para:pahd_r_redesign_audit` (ch4:1012) — Phase E 신설
- `tab:gt_positions` (ch3:365) — 기존
- `tab:vaccine_escape_stage3` (ch4:937) — 기존
- `sec:cross_validation_escape` (ch5:169) — 기존, chapter ref만 ch:results→ch:discussion 정정

---

## 10. 잠재적 잔존

1. **ch4:497 41-SD 본문 ↔ supplementary CSV deferral**: random baseline 분포 자체는 본문에 SD=0.003 명시되어 있으나, 41-SD 계산을 재현할 per-replicate 행렬은 Zenodo bundle 시점에 공개 필요. 본문 검증은 가능 (mean=0.001, SD=0.003, observed=0.124 → 0.123/0.003 ≈ 41SD).
2. **ch4:254 5.92× / z=13.34 supplementary**: structural_features/ 폴더의 pairwise contact tables는 실존하나 1,000 permutation null draws의 per-replicate 값은 별도 supplementary 필요.
3. **cycle3 ch4 잔존 Major (M1/M2/M3)**: keybox 2.5e-16 vs ch1 3.9e-9 propagation, 597 "same dataset" vs 606 "separate external" framing, Friedman power-vs-failure 라벨 — Phase E 범위 외 (별도 cycle 권장).
4. **cycle3 ch1 B-3/B-4 (TikZ overflow)**: 컴파일 결과 238페이지 출력 정상 — overflow는 시각적으로 발생하지 않음 (xelatex 로그에 overfull \hbox 경고는 본문 단락 수준이며 TikZ 박스 관련 아님).
5. **cycle3 ch4 Cycle3-C2 (475 "support interpretation (2)")**: Phase E 범위 외 (별도 cycle 권장).
6. **cycle3 ch5 잔존 Minor (m-1, m-13, m-14)**: polish-tier, 차단 위험 없음.
7. **cycle3 ch2 B.3 / B.5 / B.6**: B.4는 동시 패치로 닫힘. B.3 (structure-aware PLM dead pointer) / B.5 (ProtTrans hedge) / B.6 (information families vs features lexical) — 잔존 Minor.

---

## 합계

| Category | Count |
|---|---|
| Critical 회귀 닫힘 | 2 (Greaney mis-anchor + 4 phantom CSV) |
| Major 닫힘 | 3 (FUBAR count drift, contribution convention, Ch1 L150 self-contradiction) |
| Major-cosmetic 닫힘 | 1 (PAHD-R cross-ref) |
| Minor 닫힘 | 1 (ω² CI) |
| **Total** | **7** |

Build status: 238 pages, 0 errors, 0 undefined refs, verify 90/0/0.
