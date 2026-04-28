# Ch1 fix 적용 보고서 (cycle 2)

작성일: 2026-04-28
대상 파일: `/proj/paper/paper/dissertation/chapters_en/ch1_introduction.tex`
적용 fix 출처: `integrated_fix_matrix.md` §3 (12건) + `ch1_review.md` §E (10항목)
원칙: 모든 변경은 텍스트만, cycle 1 LANDED fix는 그대로 유지.

---

## 요약

| 우선 | 적용 | 미적용 | 비고 |
|------|------|--------|------|
| P0 | 5건 (1-P0-4, 1-P0-6, 1-P0-7, 1-P0-8, 1-P0-9) | 0 | 모두 수정 완료 |
| P1 | 2건 (1-P1-3, 1-P1-5) | 0 | M-02 lexical collision + TikZ alignment |
| P2 | 5건 (1-P2-1, 1-P2-2, 1-P2-10, 1-P2-11, 1-P2-12) | 0 | 자기인용 교체, EVEscape/Livesey 추가, metric label, Objectives 재구조화, broadest scope |
| **합계** | **12건** | **0** | integrated_fix_matrix §3의 모든 항목 적용 |

LaTeX 컴파일은 본 작업에서 수행하지 않음 (텍스트 변경만).

---

## P0 수정 (5건)

### 1-P0-4 (C-01) — ch1:82 Objective 1 panel size 11/12 conflict
- **before** (L82): `Stage~3 for multi-source feature integration with information-type analysis across all 11 pathogens.`
- **after** (L82): `Stage~3 for multi-source feature integration on the 11-pathogen main panel, extended to 12 pathogens by adding Zika for the feature-ablation and nested-LOPO analyses (see Chapter~\ref{ch:results} Section~\ref{subsec:feature_ablation}).`
- **이유**: Ch1 내부 모순 (L82 = 11, L150 = 12)을 해소. ch4:837/795 nested-LOPO 12-pathogen과 정합.

### 1-P0-9 (m-01) — ch1:106 TikZ subbox echo
- **before** (L106): `\textbf{MutBench}: Systematic comparison of 10 information types across 11 pathogens`
- **after** (L106): `\textbf{MutBench}: Systematic comparison of 10 information types across 11 pathogens (extended to 12 with Zika for feature ablation)`
- **이유**: 1-P0-4와 lockstep. Figure 1.1 본문이 prose와 일치하도록.

### 1-P0-6 (M-01) — ch1:117 TikZ body, novel-only first
- **before** (L117): `HIV-1 vaccine-escape enrichment (full set 7.19$\times$; novel-only 7.16--8.24$\times$) --- primary external validation`
- **after** (L117): `HIV-1 vaccine-escape enrichment, novel-only $7.16$--$8.24\times$ (37 Layer-A-disjoint positions, worst-case $p{=}5{\times}10^{-12}$); full-set $7.19\times$ for completeness --- primary external anchor`
- **이유**: caption(L131) "Layer~A-disjoint subset (HIV-1, Bonferroni-significant)"와 abstract:11의 "primary anchor = novel-only" framing과 정합. full-set을 "for completeness"로 격하.

### 1-P0-7 (M-05) — ch1:148 Bolker n=11 small-cluster caveat
- **before** (L148): `... 6-category aggregation gives $\omega^2 = 0.103$ as a collinearity-robust lower bound). The conclusion rests on the interaction effect ...`
- **after** (L148): `... 6-category aggregation gives $\omega^2 = 0.103$ as a collinearity-robust lower bound; 11 pathogen clusters places the design near the small-cluster regime---above the Bolker rule-of-thumb minimum of 5--6 but below the typical recommendation of 20--30 for stable random-effects estimation, see Chapter~\ref{ch:conclusion} Section~\ref{sec:limitations}). The conclusion rests on the interaction effect ...`
- **이유**: Defense Q3 (n_clusters=11)에 본문 anchor. ch5:285 Bolker note와 cross-ref. `sec:limitations` label은 ch6에 이미 정의되어 있음 (확인됨).

### 1-P0-8 (C-02) — ch1:152 "operationally equivalent" non-inferiority bound
- **before** (L152): `Feature ablation identifies a 4-feature core (homoplasy, pLDDT, entropy, frequency) that is operationally equivalent to the full 10-feature ensemble under nested-LOPO (paired delta $+0.011$ MCC; 95\% CI [$-0.018$, $+0.042$]; permutation $p = 0.61$; Table~\ref{tab:nested_lopo_4core}).`
- **after** (L152): `Feature ablation identifies a 4-feature core (homoplasy, pLDDT, entropy, frequency) that is statistically indistinguishable from the full 10-feature ensemble under nested-LOPO within a $\pm 0.04$~MCC non-inferiority bound (paired delta $+0.011$~MCC; 95\% CI [$-0.018$, $+0.042$]; permutation $p = 0.61$; Table~\ref{tab:nested_lopo_4core}); this is reported as non-rejection of the inferiority hypothesis at the stated bound, not as a pre-specified equivalence claim.`
- **이유**: codex P5-01 SERIOUS 결함 해소 (equivalence overclaim). Non-rejection of inferiority + 명시적 margin 표기. ch4:839 ("operational equivalence under nested-LOPO ($p = 0.61$, paired delta CI [$-0.018$, $+0.042$])")는 표현 약간 다르지만 의미상 정합 — 추가 cross-chapter 동기화 필요는 §아래 메모 참조.

---

## Major / P1 수정 (2건)

### 1-P1-3 (M-02) — ch1:41 "three-stage process" lexical collision
- **before** (L41-46): `In practice, mutation hotspot detection follows a three-stage process. In the first stage (\textit{sequence collection}) ... In the second stage (\textit{computational analysis}) ... In the third stage (\textit{experimental validation}) ...`
- **after** (L41-46): `In practice, mutation hotspot detection follows a three-step pipeline (sequence collection $\rightarrow$ computational analysis $\rightarrow$ experimental validation); to avoid lexical collision with the Stage~1/2/3 experimental design introduced in Sections~\ref{sec:intro_objectives}--\ref{sec:intro_contributions}, the present chapter uses the term ``step'' for the bench-side workflow. In the first step (\textit{sequence collection}) ... In the second step (\textit{computational analysis}) ... In the third step (\textit{experimental validation}) ...`
- **이유**: L41-50의 bench-side "Stage 1/2/3"과 L82/L143의 experimental-design "Stage 1/2/3"이 같은 어휘를 공유하던 충돌 제거. "step"으로 분리.

### 1-P1-5 — ch1:111 TikZ subbox prose alignment
- **before** (L111): `(design) {2-Stage + Integration};`
- **after** (L111): `(design) {2-Stage main + Stage~3 layer};`
- **이유**: cycle 1 G08 fix가 prose에 적용되었으나 TikZ subbox가 미정합 (PARTIAL). abstract:8 "two-stage main + Stage 3 layer" 표현과 일치.

---

## Minor / P2 수정 (5건)

### 1-P2-1 (m-04) — ch1:11 self-cite replacement
- **before** (L11): `... a core task in vaccine design, antiviral drug development, and real-time genomic surveillance~\cite{youn2025mutclust}.`
- **after** (L11): `... a core task in vaccine design, antiviral drug development, and real-time genomic surveillance~\cite{harvey2021tracking,carabelli2023convergent}.`
- **이유**: "core task의 외부 근거"를 자기인용(MutClust)이 아닌 SARS-CoV-2 surveillance(harvey)+ convergent-evolution(carabelli) 외부 문헌으로. references.bib에 두 키 모두 등재 확인됨 (L212, L470).

### 1-P2-2 (m-05) — ch1:33 EVEscape + Livesey 추가
- **before** (L33): concurrent benchmarks 단락에 ViroGym/EVEREST/ProteinGym만 인용.
- **after** (L33): `... ProteinGym~\cite{notin2023proteingym,notin2025proteingym_v13}, 217 DMS / 90+ baselines; EVEscape~\cite{thadani2023evescape}, an immune-escape predictor combining fitness, accessibility, and antibody dissimilarity; and the variant-effect benchmark of Livesey \& Marsh~\cite{livesey2020using}), but none ...`
- **이유**: cycle 1 G26 unaddressed. references.bib L950 (thadani2023evescape) + L982 (livesey2020using) 등재 확인됨. 외부 비교 baseline 보강.

### 1-P2-10 (m-02) — ch1:146 metric label "MCC-best"
- **before** (L146): `... with 9 distinct best-performing scoring types observed---including FUBAR phylogenetic selection scores for H3N2, protein language model scores for SARS-CoV-2 and RSV, and homoplasy for Norovirus.`
- **after** (L146): `... with 9 distinct MCC-best scoring types observed---including FUBAR phylogenetic selection scores for H3N2, protein language model scores for SARS-CoV-2 and RSV (MCC-best at the scoring--detector cell), and homoplasy for Norovirus.`
- **이유**: L151 이미 `(per-feature AUC)` 라벨 명시되어 있음. L146에 `MCC-best`를 명시하여 두 metric 혼동 차단.

### 1-P2-11 (M-03) — ch1:77-88 Objectives 재구조화
- **before** (Objectives 2 & 3): "Identify the dominant factor..." / "Identify pathogen-specific predictive information types..."
- **after** (Objective 2): `\textbf{Determine which factor---scoring type, detection method, or pathogen---dominates the variance in hotspot-detection performance}, and whether the dominant factor is a main effect or an interaction. Operationally, this asks whether a single ``best'' scoring--detection combination exists across pathogens, and is addressed through factorial Analysis of Variance (ANOVA), Friedman test, and Leave-One-Pathogen-Out (LOPO) cross-validation.`
- **after** (Objective 3): `\textbf{Test whether a small information core is sufficient for hotspot detection, and whether multi-source integration externally validates on antibody/vaccine-escape sets.} This decomposes into two open questions: (i) Among 10 biological information types, does a compact subset retain the discriminative power of the full ensemble under proper held-out-pathogen evaluation? (ii) Does multi-source integration reduce the experimental search space on independently-curated vaccine-escape positions, particularly on positions that are disjoint from the literature-curated Layer~A ground truth?`
- **이유**: Objectives ↔ Contributions 1:1 mapping 해소. Open question으로 reframe하여 Contributions 2/3에 surprise factor 부여.

### 1-P2-12 (M-04) — ch1:142 broadest scope footnote
- **before** (L142): `... 8{,}580 evaluation cells across the 20-type single-position scoring regime and the 11-pathogen panel ...`
- **after** (L142): `... 8{,}580 evaluation cells across the 20-type single-position scoring regime and the 11-pathogen main panel, with the Stage~3 feature-integration analysis extended to a 12-pathogen panel by adding Zika ...`
- **이유**: L150 Contribution 3a "12-pathogen Stage 3 panel"과 정합. L143과 L167도 함께 정합화 (아래 정합 fix 참조).

---

## 정합 (consistency) 추가 fix

위 fix 적용 과정에서 발견된 ch1 내부 panel-size 표현 추가 정합화:

### L143 — Contribution 1 본문 Stage 1/2/3 panel size 명시
- **before**: `... a large-scale comparison across eleven pathogens (Stage~2), and multi-source feature-integration analysis (Stage~3).`
- **after**: `... a large-scale comparison across the 11-pathogen main panel (Stage~2), and multi-source feature-integration analysis on the 12-pathogen panel (Stage~3, extended from the main panel with Zika; Section~\ref{subsec:feature_ablation}).`

### L167 — Dissertation organization Information-Type Analysis 12-pathogen 명시
- **before**: `... and Information-Type Analysis (feature ablation, ground truth heterogeneity, search space reduction, and multi-source integration across 11 pathogens).`
- **after**: `... and Information-Type Analysis (feature ablation on the 12-pathogen Stage~3 panel, ground truth heterogeneity, search space reduction, and multi-source integration).`

---

## 적용 미달성 / skip한 결함

**없음**. integrated_fix_matrix §3의 12개 fix + ch1_review §E의 10개 권고사항 모두 본 패치에 통합되었음.

note: 1-P2-10에서 ch1:151 "(per-feature AUC)"는 cycle 1에 이미 추가되어 있었으므로 L146의 "MCC-best"만 추가하는 것으로 충분함.

---

## 잠재적 cross-chapter 영향 (메모만 — 본 작업에서는 미적용)

다음은 ch1 내부 패치만으로는 닫히지 않는 cross-chapter 정합 항목. 별도 cross-chapter 단계에서 처리 권장.

### 1. Panel size 12 명시 (G24 family)
- **abstract.tex** (en): L11이 Contribution 3a를 "12-pathogen Stage~3 panel"로 이미 표기 — OK. 단 abstract 헤드라인 (L4 등)에서 "11-pathogen"만 노출하는 라인이 있다면 footnote 검토 필요.
- **abstract_kr.tex**: 한국어 abstract도 11/12 분리가 명시되어 있는지 별도 확인 필요 (cycle 2 매트릭스에서 abstract_kr.tex:12의 G08 fix는 별도 다루어짐).
- **ch4_results.tex**: L795 ("extended from the core 11 pathogens to 12 pathogens by adding Zika"), L837 ("nested-LOPO ... 11 training pathogens"), L881, L922 모두 일관 — OK. Ch1의 12-pathogen 표현이 ch4와 정합됨.
- **ch6_conclusion.tex**: L14 "12-pathogen Stage~3 panel" 명시 — OK.

### 2. "operationally equivalent" 약화 (1-P0-8 family)
- **abstract.tex**: L11/L14에 "operationally equivalent to the 10-feature ensemble under nested-LOPO" 표현 잔존. integrated_fix_matrix §9.3에 따라 abstract:14, ch5:155 등도 동일 패턴으로 약화 필요. **본 ch1 작업에서는 ch1만 처리** — abstract/ch5 동기화는 cross-chapter 단계.
- **ch4:839**: "operational equivalence under nested-LOPO ($p=0.61$, paired delta CI [$-0.018$, $+0.042$])" 표현 — ch1의 "non-inferiority bound" 표현보다 약함. 의미는 동일하나 문구 통일 권장 (cross-chapter polish).
- **ch5_adapt.tex** L155 / L162 / L164: 5-P0-3 fix 대기.
- **ch6:14**: "statistically indistinguishable from the full 10-feature EqualWeight ensemble" 표현은 ch1과 일치 — OK.

### 3. Bolker n=11 small-cluster (1-P0-7 family)
- ch5:285 (5-M-10) 동일 caveat 추가 권장. ch1:148이 cross-ref `sec:limitations`(ch6:20)을 가리키므로 ch6 §sec:limitations에 Bolker 내용 명시되어야 anchor 닫힘.
- ch3:912-916 (3-P0-4) wild-cluster bootstrap 인정과 정합 필요.

### 4. Self-cite 약화 (1-P2-1 family)
- ch1:11 자기인용 제거 후, ch1:36 motivational 자기인용(han2025mosd, youn2025mutclust)은 그대로 유지(정당함). 다른 chapter에서도 youn2025mutclust가 "core task" 근거로 인용되는 위치가 있다면 검토 필요.

### 5. EVEscape/Livesey & Marsh 인용 추가 (1-P2-2 family)
- ch2 background에서도 EVEscape/Livesey가 누락되어 있다면 추가 권장 (ch2_review에서 별도 처리).

---

## 검증 (grep)

```bash
$ grep -c "operationally equivalent" /proj/paper/paper/dissertation/chapters_en/ch1_introduction.tex
0  # ch1에서 모두 제거됨

$ grep -c "three-stage" /proj/paper/paper/dissertation/chapters_en/ch1_introduction.tex
0  # bench-side workflow lexical collision 해소

$ grep -c "12 pathogen\|12-pathogen" /proj/paper/paper/dissertation/chapters_en/ch1_introduction.tex
5  # L82, L106, L142, L143, L150, L167 — 모든 Stage 3 panel 언급에 12 명시됨
```

---

## 최종 메모

1. **cycle 1 P0 9건 (G01, G02b, G07, G08, G09, G10, G12, G14a-c)** 검증: ch1:148 LOPO null-consistent corroboration 표현(G02b), L150 Contribution 3 (3a)/(3b) 분할 표기(G07), L150 Bonferroni 3.9e-9(G09), L153 H3N2 7.19× novel-only 분리(G10) 모두 LANDED 상태 그대로 유지됨. G08만 cycle 2에서 PARTIAL → 본 패치 1-P1-5 (TikZ subbox)로 PASS 완료.

2. **컴파일 검증 미수행**: 본 작업은 텍스트 패치만 수행. LaTeX 컴파일 / verify_dissertation.py 실행은 cross-chapter 적용 후 일괄 수행 권장.

3. **TikZ 무결성**: L106 subbox는 길이가 늘어났으나 `mainbox` 스타일이 `minimum width=10cm`로 정의되어 있어 텍스트 줄바꿈 처리될 가능성 높음 — 빌드 시 시각적 점검 필요. L117은 `\times`가 줄바꿈 안전하게 처리되도록 `{=}5{\times}10^{-12}` 형태로 spacing 압축. L111 subbox는 `~` (tilde)로 non-breaking space 사용.

4. **자기 비판**: 1-P2-11 (Objectives reframe)이 가장 큰 구조적 변경. Objective 2/3이 길어졌으나 "open question → answer in Contributions" 흐름으로 surprise factor 강화. 심사위원이 Objectives만 읽어도 변수의 ANOVA/LOPO/feature-ablation/external-anchor 구조를 사전 파악 가능.
