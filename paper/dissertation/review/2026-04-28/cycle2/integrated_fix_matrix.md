# 통합 fix 매트릭스 (cycle 2)

생성일: 2026-04-28
입력: cycle 2 8개 review.md (abstract/ch1~ch6/cross_chapter) + cycle 1 phase2b_ch1~6.md + summary.md
대상 에이전트: 챕터별 fix 에이전트 (병렬 적용 가능)
원칙: 텍스트 수정만 (재실험 0건). 모든 fix는 file:line 정확 명시.

---

## 1. 전체 통계

| 분류 | 건수 | 비고 |
|------|------|------|
| **총 결함** | **44건** | cycle 2 신규 19건 + cycle 1 미수정 22건 + cross-chapter polish 3건 |
| P0 (defense 차단) | 19건 | Tier 1 + cycle 1 carry-over critical |
| P1 (defense 답변 강화) | 14건 | Tier 2 + cycle 1 P1 carry-over |
| P2 (정합성 polish) | 11건 | Tier 3 + minor cosmetic |
| 재실험 필요 | **0건** | 모든 fix가 텍스트/표/수식 차원에서 해결 가능 (B-C1 EqualWeight leakage는 *명시화* 권장만) |
| 챕터별 작업 시간 합계 | **~14.5시간** | abstract 0.7h + ch1 1.5h + ch2 1.7h + ch3 5.0h + ch4 2.0h + ch5 1.8h + ch6 1.0h + cross 0.8h |

---

## 2. Abstract fix list (KR + EN)

| ID | 우선 | file:line | 결함 (current) → 수정 (proposed) | 시간 | 의존성/충돌 |
|----|------|-----------|-----------------------------------|------|------------|
| A-P0-1 | **P0** | abstract_kr.tex:12 | `2단계 실험 설계` → `2단계 주 실험 설계 + Stage~3 정보 통합 레이어` (cycle 1 G08을 한국어에 전파; abstract_review E1) | 5min | ch1:82, ch1:111 TikZ subbox와 동시 검사 (G08 family) |
| A-P0-2 | **P0** | abstract_kr.tex:22 | `4개 핵심 특징(homoplasy, pLDDT, entropy, frequency)이 전체 앙상블 성능의 98%를 달성` → `4개 핵심 특징(homoplasy, pLDDT, entropy, frequency)이 nested-LOPO 하에서 10-feature 앙상블과 운영적으로 동등(paired Δ +0.011, 95% CI [−0.018, +0.042], 부호 치환 p=0.61)` (cycle 1 G07을 한국어에 전파; abstract_review E2) | 10min | ch1:152, ch5:192의 동일 표현과 통합 검증 |
| A-P1-3 | P1 | abstract_kr.tex:19 | (현재 novel-only HIV-1 band 부재) → `Layer~A-disjoint 37개 위치 novel-only 7.16–8.24배(worst-case Fisher p=5×10⁻¹²; Bonferroni 보정 p_adj≈3.9×10⁻⁹)` 추가 (abstract_review E3 + cross_chapter G) | 8min | abstract.tex:11, ch6:15 동일 보강 |
| A-P1-4 | P1 | abstract.tex:2 | `primary external anchor` → `primary external anchor (retrospective enrichment; no prospective time-forward validation)` (abstract_review E4) | 5min | ch5:266 prospective sentence와 정합 |
| A-P1-5 | P1 | abstract.tex:11 (novel-only Bonferroni 누락) | `worst-case $p = 5 \times 10^{-12}$` → `worst-case $p = 5 \times 10^{-12}$ (Bonferroni $p_{\text{adj}} \approx 3.9 \times 10^{-9}$ across 780 combinations)` (cross_chapter G P1) | 5min | ch6:15와 함께 패치 |
| A-P1-6 | P1 | abstract.tex:13 + abstract_kr.tex:21 | `9 distinct optimal information types` → 끝에 `(Tranception/ESM-2 channel collinearity not separated at headline granularity; see Ch3 Section~\ref{subsubsec:tranception_separation})` 1-clause 추가 (abstract_review E5) | 5min | ch3:655 Tranception correlation table 인용 |
| A-P2-7 | P2 | abstract.tex:11 | `restricted to 3/11 pathogens (2,340 evaluations)` → `restricted to 3/11 pathogens (2,340 evaluations) by curated antibody-escape annotation availability — not by panel design` (abstract_review E6) | 3min | — |

**Abstract 합계: 7건, ~41분**

---

## 3. Ch1 fix list

| ID | 우선 | file:line | 결함 (current) → 수정 (proposed) | 시간 | 의존성/충돌 |
|----|------|-----------|-----------------------------------|------|------------|
| 1-P2-1 | P2 | ch1:11 | `core task~\cite{youn2025mutclust}` (자기 인용) → `core task~\cite{harvey2021tracking}` 또는 `\cite{carabelli2023convergent}` (cycle 1 M3, ch1_review m-04) | 5min | references.bib에 두 키 모두 등재 확인 필요 |
| 1-P2-2 | P2 | ch1:33 | concurrent benchmarks 단락에 `\cite{thadani2023evescape}` (EVEscape) + `\cite{livesey2020using}` (Livesey & Marsh) 추가 (cycle 1 G26, ch1_review m-05) | 10min | references.bib에 두 키 모두 등재됨 |
| 1-P1-3 | **P1** | ch1:41 | `three-stage process` (Stage 1 sequence collection / Stage 2 computational / Stage 3 experimental) → `three-step pipeline (sequence collection → computational analysis → experimental validation)` — `Stage` 단어 §1.1에서 모두 제거 (ch1_review M-02, cycle 1 m2) | 10min | ch1:82, ch1:143 "Stage 3 information-integration"과 어휘 충돌 해소 |
| 1-P0-4 | **P0** | ch1:82 | `for multi-source feature integration with information-type analysis across all 11 pathogens` → `for multi-source feature integration; nested-LOPO on the 12-pathogen Stage~3 panel (extended from the 11-pathogen main panel by adding Zika; see Section~\ref{subsec:feature_ablation})` (ch1_review C-01 = cycle 1 G24 escalation; summary_cycle2 #3) | 10min | **ch1:106 TikZ "10 information types across 11 pathogens" 동시 수정 (1-P0-9)**; ch1:142 "broadest" scope 표현 검토 (M-04) |
| 1-P1-5 | **P1** | ch1:111 (TikZ subbox) | `2-Stage + Integration` → `2-Stage main + Stage 3 layer` (cycle 1 G08 잔재 — TikZ가 prose 패치와 미정합; ch1_review G08 PARTIAL) | 5min | abstract.tex:8 "two-stage main + Stage 3 layer"와 정합 |
| 1-P0-6 | **P0** | ch1:117 (TikZ body) | `HIV-1 vaccine-escape enrichment (full set 7.19$\times$; novel-only 7.16--8.24$\times$) --- primary external validation` → `HIV-1 vaccine-escape enrichment: novel-only 7.16--8.24$\times$ (37 Layer-A-disjoint positions, worst-case $p = 5 \times 10^{-12}$); full-set 7.19$\times$ shown for completeness --- primary external anchor` (ch1_review M-01 = cycle 1 M6) | 10min | abstract:11 / ch1:131 caption "primary anchor=novel-only"와 일관 |
| 1-P0-7 | **P0** | ch1:148 | `cluster-bootstrap CI [0.195, 0.333]` → 끝에 `; 11 pathogen clusters, near the small-cluster regime (Bolker minimum 5--6, recommendation $\geq$20--30); see Section~\ref{sec:limitations}` 추가 (ch1_review M-05; Defense Q3) | 8min | ch5:285 Bolker 인용과 cross-ref |
| 1-P0-8 | **P0** | ch1:152 (and ch1:150 wording) | `operationally equivalent to the full 10-feature ensemble under nested-LOPO` → `statistically indistinguishable from the full 10-feature ensemble within a $\pm$0.04 MCC non-inferiority bound under nested-LOPO` (ch1_review C-02; codex P5-01 collateral; summary_cycle2 #4) | 10min | abstract:14, ch5:155, ch6:14 동일 표현 동기화 (이 4곳에서 "operationally equivalent" 모두 약화) |
| 1-P0-9 | **P0** | ch1:106 (TikZ subbox) | `10 information types across 11 pathogens` → `10 information types across 11 pathogens (extended to 12 with Zika for feature ablation)` (ch1_review m-01 — 1-P0-4와 동시 수정) | 5min | 1-P0-4 동시 수정 필요 |
| 1-P2-10 | P2 | ch1:151 + ch1:146 | metric label 부재 — L151 `protein language model scores ... ESM-2 for SARS-CoV-2` 끝에 `(per-feature AUC)`, L146 `protein language model scores for SARS-CoV-2 and RSV` 끝에 `(MCC-best)` (ch1_review m-02) | 5min | — |
| 1-P2-11 | P2 | ch1:77–88 (Objectives) | Objective 2/3을 closed statement → open question으로 reframe (ch1_review M-03 = cycle 1 M2): Objective 2 = `Determine which factor — scoring, detector, or pathogen — dominates variance`; Objective 3 = `Test whether a small information core suffices and whether multi-source integration externally validates on vaccine-escape sets` | 15min | Contribution 1/2/3 본문 표현 변경 없음 |
| 1-P2-12 | P2 | ch1:142 | `broadest` 클레임 scope — `8,580 evaluations across 11-pathogen main panel` → `8,580 evaluations across 11-pathogen main panel + 12-pathogen Stage~3 feature-integration extension` 또는 footnote (ch1_review M-04) | 8min | 1-P0-4와 정합 검증 |

**Ch1 합계: 12건, ~1.7시간**

---

## 4. Ch2 fix list

> **Status**: cycle 1 P0 9건 수정 시 ch2는 손대지 않음. cycle 2 codex 검수가 자체-모순(N-C1: "10 vs 20"), Weber 미스적용(N-C3), MEME/FUBAR 오인용(C1) 등을 재발견. 모든 fix는 cycle 1 phase2b_ch2.md + cycle 2 ch2_review.md 통합.

| ID | 우선 | file:line | 결함 (current) → 수정 (proposed) | 시간 | 의존성/충돌 |
|----|------|-----------|-----------------------------------|------|------------|
| 2-P0-1 | **P0** | ch2:49, ch2:156, ch2:208 | `10 information types` (3개 위치 모두) → `20 scoring types derived from 10 underlying biological features` (ch2_review N-C1; summary_cycle2 #8) | 15min | ch3 / ch4 표현 (`20 scoring × 39 detectors × 11 pathogens = 8,580`)과 정합. **3개 위치 모두 동일 패턴 적용** |
| 2-P0-2 | **P0** | ch2:57 | `MEME and FUBAR~\cite{kosakovsky2020hyphy}` → `MEME~\cite{murrell2012meme}` and `FUBAR~\cite{murrell2013fubar}`; HyPhy 플랫폼은 별도 문장 분리 (cycle 1 C1, ch2_review N-M3 일부 + Edits row P0) | 10min | references.bib에 `murrell2012meme` 신규 등록 필요 (`murrell2013fubar`은 이미 등재 L1119) |
| 2-P0-3 | **P0** | ch2:154 | `\cite{gurev2025everest}` → `\cite{gurev2025everest,gurev2026everest_v3}; the strength of this as independent corroboration is qualified in Section~\ref{subsec:bg_benchmarking_gap} (PLM≪alignment is a cross-study parallel, not independent corroboration)` (ch2_review N-C2) | 10min | ch2:248 disclaimer와 cross-link |
| 2-P0-4 | **P0** | ch2:228 | `MutBench adheres to these principles` → `with the partial exception that MutClust~\cite{youn2025mutclust}, developed in the same lab, is one of the 14 evaluated detection families; this is mitigated by identical evaluation conditions and blinded ground truth across all methods` (ch2_review N-C3; Weber independent-evaluation 위반 인정) | 10min | ch2:227 Boulesteix self-assessment-bias citation과 정합 |
| 2-P1-5 | P1 | ch2:106 (after Bloom-Neher) | DMS lineage 단락에 새 paragraph 삽입: `Greaney et al.~\cite{greaney2021RBD,greaney2022spike} extended DMS to antibody-escape mapping for the SARS-CoV-2 RBD and full Spike. These escape DMS datasets directly inform the Layer~C cross-validation paradigm (Section~\ref{sec:cross_validation_escape}).` (cycle 1 M3, ch2_review N-M4) | 15min | references.bib에 `greaney2021RBD`, `greaney2022spike` 신규 등록 필요 |
| 2-P1-6 | P1 | ch2:143–144 | `the ESM-3 generation extended the ESM family ... (no formal citation key is asserted here ...)` → 옵션 (a) Hayes et al. 2024 (Science 387:850) 인용 + bib 등재; 또는 (b) ESM-3 언급 자체 삭제 (cycle 1 C4, ch2_review P1) | 15min | bib에 `hayes2024esm3` 추가 시 다른 챕터 cross-ref 영향 없음 |
| 2-P1-7 | P1 | ch2:237 (table caption tab:benchmark_comparison) | 캡션에 `ViroGym row reflects the March 2026 arXiv preprint (pre-peer-review)` 추가 (cycle 1 M9, ch2_review N-M2) | 5min | 표 자체에 행 추가는 불필요; caption 1-clause |
| 2-P1-8 | P1 | ch2:39 또는 ch2:241 | OncodriveCLUST(L39) vs OncodriveCLUSTL(L241) 명명 불일치 — 옵션 (a) L241을 `OncodriveCLUST`로 통일, 또는 (b) `arnedopac2019` bib 등재 + 두 도구 분리 기술 (cycle 1 C2) | 8min | 옵션 (a) 권장 (수정 최소) |
| 2-P2-9 | P2 | ch2:56–60 | Selection-based methods 1-paragraph → 2 sentences 추가: FEL/SLAC/BUSTED 명시 + `kosakovskypond2005fel` (신규 bib 등재) (cycle 1 M2, ch2_review P2) | 12min | bib 신규 등록 필요 |
| 2-P2-10 | P2 | ch2:222 | `MutBench's pathogen-to-scoring recommendation table selects the optimal scoring–detection combination` → ch5 discussion으로 이동 또는 forward-reference만 남김 (cycle 1 C7) | 8min | ch5에 이미 유사 진술 있음 — 중복 검토 |
| 2-P2-11 | P2 | ch2:20 | `\cite{holmes2009evolution}` (textbook 2°) → `\cite{holmes2009evolution,sanjuan2010viral}` (Sanjuán 1° added) (cycle 1 m1, ch2_review N-m1) | 3min | bib에 sanjuan2010viral 이미 등재 (L1275) |
| 2-P2-12 | P2 | ch2:289 | `%% SECTION 2: MutClust Summary` (잘못된 주석 라벨) → `%% Chapter Summary` (cycle 1 m15, ch2_review N-m3) | 2min | comment-only, 본문 영향 없음 |
| 2-P2-13 | P2 | ch2:172–180 | Surveillance 단락에 Bedford-lab forecasting (Łuksza & Lässig 2014, Huddleston 2020) 추가 (ch2_review N-m2) | 10min | bib 신규 등록 가능성 |

**Ch2 합계: 13건, ~2시간 (P0 4건 = 45분, P1 4건 = 43분, P2 5건 = 35min)**

---

## 5. Ch3 fix list (가장 큰 작업)

> **Status**: cycle 1에서 ch3 6 Critical 전부 미수정. cycle 2가 추가로 3건 신규 Critical (B-C1 EqualWeight leakage, B-C2 cell-level demotion, B-C3 wild-cluster) 발견. 본 매트릭스는 cycle 2 ch3_review §F의 F1~F20 중심으로 정리.

| ID | 우선 | file:line | 결함 (current) → 수정 (proposed) | 시간 | 의존성/충돌 |
|----|------|-----------|-----------------------------------|------|------------|
| 3-P0-1 (F1) | **P0** | ch3:131 | `all available sequences as of December 2024 were downloaded` (cutoff date 모호) → Table tab:pathogen_data에 "Query date (YYYY-MM-DD)" 컬럼 추가 + GenBank query strings supplementary table (cycle 1 C1) | 30min | Table 수정 필요. ch3 본문 line drift 가능 |
| 3-P0-2 (F2) | **P0** | ch3:131–135 | `MAFFT v7.505 ... --auto` (비결정성 자인만) → 11-pathogen별 실제 선택된 algorithm log table 추가 + Katoh & Standley 2013 §2 인용 (cycle 1 C2) | 25min | bib에 katoh2013 인용 등재 확인 |
| 3-P0-3 (F3) | **P0** | ch3:885 (or ANOVA paragraph) | `$\omega^2 = 0.296$` 헤드라인 → 추가: `Cell-level aggregation (3,080 unique scoring×family×pathogen cells) yields $\omega^2 = 0.234$; the evaluation-level 0.296 reflects within-cell residual contraction. The cell-level value is the more conservative reference.` (ch3_review B-C2 = cycle 2 신규 Critical; ch4_review Critical-1과 정합) | 15min | **ch4:425 동일 disclosure 추가 필요 (Ch4 fix 3-1과 정합)**; ch5:290 ANCOVA paragraph가 source |
| 3-P0-4 (F4) | **P0** | ch3:912–916 | BCa 10,000 + cluster 1,000 — 추가 sentence: `The 11-cluster percentile bootstrap is anti-conservative for $G \leq 30$; wild-cluster bootstrap (Cameron et al. 2008) is the recommended sharper alternative (currently disclosed in Section~\ref{subsec:wild_cluster_future} of Chapter~\ref{ch:results}; deferred to future work).` (ch3_review B-C3 = cycle 2 신규 Critical) | 10min | ch4:524 wild-cluster admission과 정합 |
| 3-P0-5 (F5) | **P0** | ch3:695 (EqualWeight directional sign rule) | `signs are fit on training pathogens` (모호) → 명시: `Signs are fit (a) on all 11 pathogens for the Stage~2 EqualWeight column (declared as a label-aware feature; this column's MCC is therefore an upper bound and is excluded from any LOPO-style generalization claim), or (b) refit per fold inside nested-LOPO (Stage 3 / Section~\ref{subsec:feature_ablation}).` (ch3_review B-C1 = cycle 2 신규 Critical; summary_cycle2 #1) | 25min | **ch4의 EqualWeight 컬럼 인용 모두 검토** (특히 ch4:801 nested-LOPO 결과); ch5:162와 정합 |
| 3-P0-6 (cycle 1 C3) | **P0** | ch3:296, 309, 317 | Layer A/B/C 임계값 사후 결정 의심 — 추가: `Layer A/B/C thresholds and the 20×39 ANOVA grid were frozen in the SOP prior to Stage 1 analysis (lab-notebook entry 2024-XX-XX); no post-hoc adjustment was performed.` (cycle 1 C3 + C5; preregistration 명시) | 15min | 실제 lab notebook 일자 확인 필요. 사용자 입력 필요 (lab-notebook ref) |
| 3-P0-7 (F13 / cycle 1 C4) | **P0** | ch3:967 (Code & Data) | `forward ref to ch6` → 직접 인라인: `Repository: \url{https://github.com/.../mutbench} (commit hash XXXXXXX), Zenodo DOI: 10.5281/zenodo.XXXXXXX, environment file: environment.yml.` (cycle 1 C4) | 10min | ch6 sec:code_availability와 일치 검증 (sync) |
| 3-M-8 (F6) | P1 | ch3:317 | Layer C sweep `4 pathogens` → 옵션 (a) Rabies/EV-A71 sweep 추가 실행, 또는 (b) `Threshold robustness verified on 4/6 DMS pathogens; Rabies/EV-A71 sweep deferred to future work` (cycle 1 C6) | 10min | (a) 재실험 30min~1h; (b) 텍스트만 — **(b) 권장 (재실험 0건 원칙)** |
| 3-M-9 (F7) | **P1** | ch3:899–905 (after LOPO) | 새 subsubsection 삽입: `Nested-LOPO 4-feature evaluation`: 12-fold 구조, sign refit per training-pathogen set, paired bootstrap 1,000 resamples, sign-flip permutation 5,000 iterations (ch3_review B-M5; ch4 L837 protocol을 ch3에 backport) | 25min | ch4:837–839 nested-LOPO description과 동일 표현 사용 |
| 3-M-10 (F8) | **P1** | ch3:881 (after ANOVA) | 새 paragraph: ANCOVA fit (statsmodels Type II OLS, log(length) + Layer-A positive rate as covariates, cell-level grid, 0.234 → 0.264 result) (ch3_review B-M4; ch5:290에서 backport) | 20min | ch5:290 ANCOVA description과 일치 |
| 3-M-11 (F9) | **P1** | ch3:881 (after ANOVA, after F8) | 새 paragraph "Bayesian partial-pooling cross-check": PyMC 5.28 priors (half-Cauchy / half-Normal σ=0.2), chains 2×800 / 4×2,000, R-hat, posteriors 0.252 / 0.319 (ch3_review B-M3; ch5:285에서 backport) | 25min | ch5:285 Bayesian description과 일치 |
| 3-M-12 (F10) | P1 | ch3:202 (after Stage 1 intro) | 새 subsubsection "Time-stratified prospective protocol (H3N2 pilot)": 2010–2015 train, 2016–2020 test, freq <5%/≥10% emergent definition, Fisher one-sided (ch3_review B-M2; ch4:198 protocol backport) | 20min | ch4:198 prospective sanity check description과 일치 |
| 3-M-13 (F11) | P1 | ch3:655 | `near-equivalent for 11 of 12 pathogens` → append: `Sensitivity ω² with Tranception channel removed (single-PLM model): ω²_{scoring×pathogen} = X.XXX. The two channels are retained in the headline model for completeness; the merged-channel sensitivity is the more conservative reference.` (ch3_review B-M1; cycle 1 P1 carryover) | 20min | 실제 sensitivity 값 X.XXX 산출 필요 (재현 1회). **Option B (Tier 2)에 해당** |
| 3-M-14 (F12) | P1 | ch3:499 | `shifts per-pathogen MCC by ±0.01 on average` → append: `(\texttt{results/mutbench/gamma_sensitivity.csv}, mean ± SD across 11 pathogens)` (ch3_review B-M6) | 5min | CSV 파일 존재 확인 필요 |
| 3-M-15 | P1 | ch3 (general) | DMS preprocessing — 6 source 각각 download URL + version/commit/DOI를 Table dms_preprocessing에 컬럼으로 추가 (cycle 1 M3, M14) | 25min | Table 수정 |
| 3-m-16 (F14) | P2 | ch3:946–951 | permutation methods: circular permutation N (e.g., 200), pseudo-count rule `p = (count+1)/(N+1)` 추가 (cycle 1 m12) | 5min | — |
| 3-m-17 (F15) | P2 | ch3:319 (Table dms_preprocessing) | `Mean across 2 replicates` 모두 → 원논문 검증 (H3N2 Lee 2018, HIV-1 Haddox 2018 ≥3 replicate 가능성) (cycle 1 M14) | 15min | 원논문 확인 필요 |
| 3-m-18 (F16) | P2 | ch3:615, 619, 688 | IQ-TREE 2 / HyPhy v2.5 / ESM-2 — patch versions (e.g., IQ-TREE 2.2.0, HyPhy 2.5.46) + ESM-2 HF revision SHA (cycle 1 m5–m7) | 10min | 실제 환경 버전 확인 필요 |
| 3-m-19 (F17) | P2 | ch3:887 | `Levene's test ... p<0.05` → F statistic + df 명시 (cycle 1 m9) | 5min | 실제 F, df 산출 |
| 3-m-20 (F18) | P2 | ch3:914 | BCa caveat at n=11 — simulated coverage 추가 (e.g., `≈ 88% nominal-95% under the present effect size`) (cycle 1 m13) | 10min | 시뮬레이션 결과 필요 |
| 3-m-21 (F19) | P2 | ch3:296 | One-line numeric forward-disclosure: `Stage 2 sensitivity (ch5 §X) shows ω² = 0.234–0.296 across Layer-A normalisations` (cycle 1 M2) | 5min | ch5 §gt_heterogeneity와 일치 |
| 3-m-22 (F20) | P2 | ch3:943 (region-level BCa) | header `(Stage 1 only)` 추가 — Stage 2 cross-pathogen design에 부적용 (cycle 1 M13) | 3min | — |
| 3-m-23 | P2 | ch3:10, ch3:172 | `two stages` (bare) → `two main stages` 또는 `Stages 1 and 2` (cross_chapter B P2; G08 잔재) | 5min | abstract:8, ch1:82와 정합 (`two-stage main` 표현 fortify) |

**Ch3 합계: 23건, ~5시간 (P0 7건 = 130min, P1 8건 = 150min, P2 8건 = 60min)**

---

## 6. Ch4 fix list

| ID | 우선 | file:line | 결함 (current) → 수정 (proposed) | 시간 | 의존성/충돌 |
|----|------|-----------|-----------------------------------|------|------------|
| 4-P0-1 | **P0** | ch4:425 | `(ω²=0.296; CI [0.195,0.333])` → `(ω²=0.296 evaluation-level; CI [0.195,0.333]; cell-level ω²=0.234, see Section~\ref{sec:critical_appraisal_anova} of Chapter~\ref{ch:discussion})` (ch4_review Critical-1; summary_cycle2 #2) | 8min | **3-P0-3 (Ch3 F3)와 동일 disclosure가 Ch3에 추가되어야 정합**. ch5:290이 source |
| 4-P0-2 | **P0** | ch4:956 | `novel-only $p_{\text{adj}} = 5.0 \times 10^{-12} \times 780 \approx 3.9 \times 10^{-9}$` → footnote 추가: `Note: this denominator (780) is shared with the full-overlap test ($p_{\text{adj}}=2.47 \times 10^{-16}$); the two p-values are different statistical objects (different position subsets) under the same correction family.` (ch4_review Critical-2) | 10min | abstract:11, ch1:150 동일 표기 검증 |
| 4-M-3 | P1 | ch4:475 | `this non-significance admits two interpretations` → append: `Friedman power at n=11 blocks is limited (~0.15 for medium W), so the non-significance is consistent with both readings; this is corroboration, not disconfirmation, of pathogen-dependence.` (ch4_review Major-2; cycle 1 M-2) | 10min | ch5:319와 정합 |
| 4-M-4 | P1 | ch4:495 | `exceeds the random baseline (mean=0.001, SD=0.003) by approximately 41 standard deviations` → footnote: `This SD=0.003 is the SD of mean across 11 pathogens for a single random combo (different from the single-pathogen single-combo SD=0.034 cited at ch4:480; the former is the SE of a panel mean, the latter the SD of one combo's MCC).` (ch4_review Major-3; cycle 1 M-4) | 10min | — |
| 4-M-5 | P1 | ch4:462 | `given 780 unique scoring–detection combinations` → `given 280 family-level combinations (footnote)` (ch4_review Major-4; cycle 1 M-1) | 5min | ch4:444 (`P(matches=0) ≈ 0.96 at 280`)와 정합 |
| 4-M-6 | P1 | ch4:13 (key box) | `HIV-1 7.19×, H3N2 9.36×` → append: `Bonferroni-survivor mean: H3N2 ≈4.7×, HIV-1 ≈4–5× (Table 4.10 footnote)` (ch4_review Selective-2; cycle 1 phase2_redteam M-08) | 8min | — |
| 4-M-7 | P1 | ch4:600 (Summary block) | `LOPO null-consistent corroboration` → `LOPO 0/11 + 0.265 gap (one-sided permutation $p \approx 0.25$–$0.28$; null-consistent, treated as corroboration not independent evidence)` (ch4_review Major-1; ch6:13와 정합) | 8min | ch6:13 G02b PARTIAL fix와 동시 적용 |
| 4-M-8 | P1 | ch4:886 (footnote) / ch4:319 (Table 4.5) | HIV-1 Layer-A operational vs literature count drift — Table 4.5 HIV-1 row에 nA 표기 또는 Table footnote에 cross-ref `(see Table 4.10 footnote for nA=23/26 reconciliation)` (ch4_review Major-5) | 5min | ch3:391 reconciliation note와 정합 |
| 4-m-9 | P2 | ch4:331 | `Nine distinct scoring types appear as best` → append: `Note Influenza B and MERS share both scoring (freq) and detection-parameter (KDE p=85) — at the parameter level only 10/11 combinations are unique.` (ch4_review Minor-1; cycle 1 phase2_redteam M-09) | 5min | — |
| 4-m-10 | P2 | abstract / ch4:956 | `p_adj=2.5e-16` (abstract) vs `2.47e-16` (ch4:956 footnote) — 라운딩 정책 통일 (`2.5e-16` 일관 사용 권장) (ch4_review Minor; cycle 1 Mi-9) | 3min | abstract.tex:2와 일관 |
| 4-m-11 | P2 | ch4:104 (caption regression) | line drift 확인 — cycle 1 G14a fix는 LANDED, but line numbers shifted (210→245, 215→250). 검증만 (수정 불필요) | 0min | — |

**Ch4 합계: 11건, ~70분 (P0 2건 = 18min, P1 6건 = 46min, P2 3건 = 8min)**

---

## 7. Ch5 fix list

| ID | 우선 | file:line | 결함 (current) → 수정 (proposed) | 시간 | 의존성/충돌 |
|----|------|-----------|-----------------------------------|------|------------|
| 5-P0-1 | **P0** | ch5:155 | `the standardised evaluation framework is provided by the three-layer ground truth and hotspot-score metric` → append: `(with the saturation caveat in Section~\ref{sec:hscore_saturation})` (ch5_review N-M4 escalated; ch5:46–48 saturation 인정과 정합) | 5min | — |
| 5-P0-2 | **P0** | ch5:84 | Rice citation 다음에 추가: `though the empirical mapping $f$ is not yet learnable from this 11-pathogen panel (LOPO 0/11; Section~\ref{sec:cross_pathogen_implications}).` (ch5_review N-C2) | 8min | — |
| 5-P0-3 | **P0** | ch5:162 + ch5:164 | `4-feature core (homoplasy, pLDDT, entropy, frequency) retained 97.6% of the full 10-feature ensemble's mean MCC` → append: `*relative to the 10-feature ensemble, not relative to an oracle*; no paired-sample significance test in this within-pathogen demonstration, see Section~\ref{sec:practical_workflow}` (ch5_review N-C1; summary_cycle2 #6) | 10min | abstract:11/14, ch1:150/152, ch6:14 동일 표현 동기화 |
| 5-P0-4 | **P0** | ch5:271–277 (after ESM-2 leakage paragraph) | 새 sentence: `Tranception (Notin 2022) was also trained on UniRef variants; per-pathogen $\rho$(Tranception, ESM-LLR) ranges 0.64–0.84 Pearson / 0.71–0.98 Spearman (Section~\ref{subsubsec:tranception_separation}, Chapter~\ref{ch:mutbench}). The SARS-CoV-2 best=Tranception result should be interpreted with channel-redundancy uncertainty.` (ch5_review N-M2; phase 4 TOP-1 risk) | 12min | ch3:655 Tranception correlation table와 정합 |
| 5-P0-5 | **P0** | ch5:266–268 (new sentence) | 추가: `No prospective time-forward validation has been conducted; all reported enrichments and MCC values are retrospective on a 2024-12 GenBank snapshot. A pilot 2010-cutoff H3N2 holdout is queued (Section~\ref{ch:conclusion}).` (ch5_review N-M3; phase 4 professor 8 — TOP-2 risk) | 10min | abstract:2 retrospective caveat와 정합 |
| 5-M-6 | P1 | ch5:194–203 (PAHD-R) | PAHD-R 첫 도입이 ch5에 있음 — Results에 \label 부재 시 ch6로 이동 또는 ch4 cross-ref 추가 (ch5_review N-M1; cycle 1 M7) | 15min | ch6:16 PAHD-R 등장과 정합. **ch6:16 fix와 함께 결정** |
| 5-M-7 | P1 | ch5:319 | `$p = 0.990$, indicating that no single method can be reliably distinguished` → `$p = 0.990$; under the Friedman rank-block design with $n = 11$ blocks the test is uninformative rather than confirming a null, and pathogen-specific optimality remains the more parsimonious interpretation given the ANOVA interaction and oracle-vs-generalized gap` (ch5_review N-M6) | 10min | ch4:475 (4-M-3)과 일관 |
| 5-M-8 | P1 | ch5:287 (independent reproduction) | 1 sentence → expand: `Specifically, the headline interaction ($\omega^2 = 0.296$), oracle MCC means (0.341), and HIV-1 7.19× enrichment are single-team-single-snapshot estimates; relative orderings are more robust than absolute magnitudes.` (ch5_review M-8 / cycle 1 C4) | 10min | — |
| 5-M-9 | P1 | ch5:34 | HCV/Influenza-B/Norovirus circularity — append: `Implication: HCV's freq-best ranking and Norovirus's epochal-Layer-A coupling should be read as partly structural; per-pathogen rankings in Tables~\ref{tab:stage2_best} carry this discount implicitly.` (ch5_review M-9 / cycle 1 C2) | 10min | ch4:307 Table 4.5 framing과 정합 |
| 5-M-10 | P1 | ch5:285 | append: `11 pathogens meets Bolker et al.'s minimum ($\geq$5–6) for fixed-effect ANOVA blocks but is below the typical recommendation ($\geq$20–30) for stable random-effects estimation.` (ch5_review M-10 / cycle 1 C5) | 8min | ch1:148 (1-P0-7)과 정합 |
| 5-M-11 | P1 | ch5:161–162 | `single-feature 7.19× and integration 4.012×` 비교 모호 — 추가: `Stage 2 single-feature 7.19$\times$ (winner's-curse-prone, top-of-780 selection) and Stage 3 integration 4.012$\times$ (winner's-curse-free, fixed 10-feature ensemble) are not directly comparable; the smaller integration number is *more reliable*, not weaker.` (ch5_review N-M5) | 10min | — |
| 5-m-12 | P2 | ch5:33 (cross-ref) | append `\ref{sec:gt_heterogeneity}` after `ground-truth curation style` (ch5_review m / cycle 1 C7) | 3min | — |
| 5-m-13 | P2 | ch5:48 | `appropriate temporal resolution remains a future challenge` → `appropriate temporal resolution beyond the 4-week minimum (Section~\ref{sec:practical_surveillance}) remains a future challenge` (ch5_review N-m2) | 5min | ch5:190 4-week minimum과 정합 |
| 5-m-14 | P2 | ch5:325–328 | `consistent with MutBench's central finding` → `as a parallel observation, not as confirmation, of the pathogen-dependent information principle` (ch5_review m) | 5min | — |
| 5-m-15 | P2 | ch5:319 (scope) | append MAFFT --auto sentence: `MSA construction used MAFFT --auto across all pathogens; per-pathogen mode (FFT-NS-2 / L-INS-i) was not held constant, which may contribute marginally to the input-quality component of the interaction.` (ch5_review N-m4) | 8min | ch3:131–135 자인과 정합 |
| 5-m-16 | P2 | ch5:17 | `expand by including ORF1ab, N protein` → 구체적 sample size target 추가 (e.g., `Targeting at least n=20 region-level samples ... would halve the BCa half-width`) (cycle 1 M1) | 8min | — |

**Ch5 합계: 16건, ~110분 (P0 5건 = 45min, P1 6건 = 63min, P2 5건 = 29min)**

---

## 8. Ch6 fix list

| ID | 우선 | file:line | 결함 (current) → 수정 (proposed) | 시간 | 의존성/충돌 |
|----|------|-----------|-----------------------------------|------|------------|
| 6-P0-1 | **P0** | ch6:13 | `Friedman ... shows no universally best combination across pathogens; LOPO 0/11 is null-consistent under permutation; both serve as corroborative consistency checks rather than independent evidence.` → `Friedman $\chi^2{=}7.69$, $p{=}0.990$ shows no universally best combination across pathogens (consistent with the interaction effect); LOPO 0/11 is null-consistent under permutation and is reported as corroborative rather than independent evidence.` (ch6_review C-1; G02b PARTIAL fail; summary_cycle2 #7) | 10min | ch4:600 (4-M-7)과 정합. abstract:10 표현 검증 |
| 6-P0-2 | **P0** | ch6:11 | `MutBench provides a benchmark ... combining 20 scoring formulas, 39 detector variants, and a three-layer ground truth (literature-curated adaptive positives, ...)` → `To our knowledge, MutBench is the broadest region-level, single-position hotspot-detection benchmark to date for RNA viruses, combining 10 biological information types (20 scoring formulas) $\times$ 14 detection families (39 variants) $\times$ 11 pathogens = 8{,}580 evaluations, a three-layer ground truth (Layer~A union of convergent-evolution, immune-escape, and HVR evidence; Layer~B purifying-selection negatives; Layer~C DMS where available), and the hotspot-score composite metric.` (ch6_review C-2 + M-1 + m-2; cycle 1 phase2b ch6 C1·M1) | 15min | abstract:2/4, ch1:142와 강도 일관 |
| 6-P1-3 | P1 | ch6:14 | Contribution 3을 단일 `Third` → `\textbf{Third (two-part).} \textit{(3a) Multi-source integration infrastructure}: ... \textit{(3b) External validation, anchored by HIV-1}: ...` (ch6_review M-2; cycle 1 phase2b ch6 C3·M3) | 15min | abstract:11, ch1:150 (two-part 명시)와 일관 |
| 6-P1-4 | P1 | ch6:14 (within Third paragraph) | 4.012× H3N2 enrichment에 `($p=0.0023$)` 추가 (ch6_review m-1) | 2min | abstract:11, ch1:150과 일관 |
| 6-P0-5 | **P0** | ch6:16 | `The PAHD-R redesign translates these findings into a conservative evidence-fusion workflow, confirming the feasibility and audit boundaries of adaptive extension without claiming a completed universal adaptive predictor.` → `Building on these three contributions, the PAHD-R synthesis (Chapter~\ref{ch:discussion}) demonstrates the feasibility and audit boundaries of an adaptive evidence-fusion workflow without claiming a universal adaptive predictor; PAHD-R is presented as a discussion-level synthesis, not as an additional benchmark contribution.` (ch6_review C-2 PAHD-R scope creep) | 10min | ch5:194–203 PAHD-R 정의 (5-M-6)와 정합 |
| 6-P1-6 | P1 | ch6:91 | `the dissertation **confirms** a feasible direction for adaptive evidence fusion` → `the dissertation evidences a feasible direction for adaptive evidence fusion` (ch6_review M-3) | 2min | — |
| 6-P1-7 | P1 | ch6:15 (HIV-1 novel-only Bonferroni) | `worst-case Fisher $p = 5.0 \times 10^{-12}$` → `worst-case Fisher $p = 5.0 \times 10^{-12}$ (Bonferroni $p_{\text{adj}} \approx 3.9 \times 10^{-9}$ across 780 combinations)` (cross_chapter G P1; abstract A-P1-5와 동일 패턴) | 5min | abstract:11과 동시 패치 |
| 6-m-8 | P2 | ch6:72 | `13-dimensional profile space` → `high-dimensional pathogen profile space` (또는 13 dims 정의 추가) (ch6_review m-3) | 5min | ch5/ch4에 13-dim 출처 정의 부재 — `high-dimensional`로 약화 권장 |
| 6-m-9 | P2 | ch6:83 | `DNA-virus extension, multi-protein evaluation, indel-aware scoring, ...` (vague) → `DNA-virus extension (e.g., HBV polymerase, HSV glycoprotein), multi-protein evaluation beyond surface glycoproteins, indel-aware scoring, virus-tuned PLM features, and real-time surveillance integration via Nextstrain pipelines.` (ch6_review m future-work specificity) | 10min | — |
| 6-m-10 | P2 | ch6:81 (no Reproduction paragraph in §6.3) | 1-sentence paragraph 추가: `**Reproduction and Release.** The archived CSVs, provenance manifest, and Zenodo tag (Section~\ref{sec:code_availability}) close the reproducibility gap as a defense-time deliverable.` (ch6_review m-4 / Priority 4 누락) | 8min | ch6 Table tab:future_roadmap Priority 4와 정합 |
| 6-m-11 | P2 | ch6:92 | `explains more performance variance than choosing among detection algorithms` → `explains more performance variance than the detection-algorithm main effect alone` (ch6_review m-5) | 3min | ch4:392 family×pathogen ω²=0.082 substantial한 사실 인정 |
| 6-m-12 | P2 | ch6:90 vs ch6:15 | `self-consistency evidence` (L90) vs `self-consistency check` (L15) 혼용 → `self-consistency check`로 통일 (cycle 1 phase2b ch6 m9) | 3min | abstract:11, ch1:150 일관 |

**Ch6 합계: 12건, ~85분 (P0 3건 = 35min, P1 4건 = 24min, P2 5건 = 29min)**

---

## 9. Cross-chapter 의존성 그래프

수정 충돌/연쇄 검증이 필요한 결함 묶음. 한 챕터 패치 시 다른 챕터도 동시 검사.

### 9.1. G08 family (Stage 3 layer 표현 통일)
- **Trigger**: A-P0-1 (abstract_kr:12), 1-P1-3 (ch1:41 "three-stage process"), 1-P1-5 (ch1:111 TikZ subbox), 3-m-23 (ch3:10/172 "two stages")
- **Cross-check**: abstract:8 ("two-stage main + Stage 3 layer"), ch1:82, ch1:143, ch3:7 — 모두 일관 표현 사용
- **Action**: 4개 fix를 *한 묶음*으로 적용. 한 곳만 수정 후 grep `two-stage\|two stage\|2-Stage` 전수 점검 권장

### 9.2. 11 vs 12 pathogen panel (G24 escalation)
- **Trigger**: 1-P0-4 (ch1:82 "across all 11 pathogens"), 1-P0-9 (ch1:106 TikZ)
- **Cross-check**: ch1:142 ("8,580 evaluations across 11-pathogen"), ch1:150 ("12-pathogen Stage~3 panel"), ch4:837 (12-pathogen nested-LOPO), abstract:11
- **Action**: ch1:82와 ch1:106 동시 수정. ch1:142 footnote 검토 (1-P2-12). abstract는 이미 11/12 분리 명시 — 추가 수정 불필요

### 9.3. 4-feature 97.6% / "operationally equivalent" 표현
- **Trigger**: A-P0-2 (kr:22), 1-P0-8 (ch1:152), 5-P0-3 (ch5:162/164)
- **Cross-check**: abstract:14, ch4:839 (G07 LANDED), ch6:14 (G07 LANDED, 97.6% 미사용 — paired delta primary)
- **Action**: 4개 위치(kr:22, ch1:152, ch5:162, ch5:164)에서 "operationally equivalent / 98% / 97.6% retention"을 일관 demote. ch4:839와 ch6:14는 이미 paired-delta-primary로 처리됨 — 추가 작업 없음

### 9.4. ω² cell-level 0.234 disclosure
- **Trigger**: 3-P0-3 (ch3:885), 4-P0-1 (ch4:425)
- **Cross-check**: ch5:290 (ANCOVA — source), abstract:10 (`within-cell residual ω² ≈ 0.39` 명시 — cell-level 0.234와 다른 quantity), ch1:148
- **Action**: ch3와 ch4 동시 패치. abstract와 ch1은 cell-level demote 미반영 — P2 추가 권장 가능 (within `cycle3` polish)

### 9.5. Novel-only Bonferroni 3.9e-9
- **Trigger**: A-P1-3 (kr:19), A-P1-5 (en abstract:11), 6-P1-7 (ch6:15)
- **Cross-check**: ch1:150 (3.9e-9 명시), ch4:956 footnote (full 도출)
- **Action**: 3곳에 동일 표현 `(Bonferroni $p_{\text{adj}} \approx 3.9 \times 10^{-9}$ across 780 combinations)` 일괄 추가

### 9.6. Friedman / LOPO 분리 표현 (G02b)
- **Trigger**: 4-M-7 (ch4:600), 6-P0-1 (ch6:13)
- **Cross-check**: abstract:10, ch1:147, ch5:319 (5-M-7)
- **Action**: ch4:600 + ch6:13 동시 패치. ch5:319는 별도 wording 약간 다름 (Friedman uninformative under n=11) — 일관성 충돌 없음

### 9.7. Tranception–ESM-LLR collinearity
- **Trigger**: A-P1-6 (abstract:13/kr:21), 3-M-13 (ch3:655 sensitivity), 5-P0-4 (ch5:271–277)
- **Cross-check**: ch3:657–684 (Tranception correlation table — 이미 LANDED cycle 1 P1 fix)
- **Action**: 3개 위치 모두 caveat 추가. ch3:655 sensitivity는 재현 1회 필요 (Option B / Tier 2)

### 9.8. PAHD-R scope creep
- **Trigger**: 5-M-6 (ch5:194–203), 6-P0-5 (ch6:16)
- **Cross-check**: abstract / ch1에 PAHD-R 부재 — 결론에서 신규 framework 등장 위험
- **Action**: ch5에서 ch4 cross-ref 추가 또는 ch6로 이동; ch6:16에서 "discussion-level synthesis, not benchmark contribution"으로 격하

### 9.9. Bolker n=11 small-cluster regime
- **Trigger**: 1-P0-7 (ch1:148), 5-M-10 (ch5:285)
- **Cross-check**: ch3:912–916 (3-P0-4 wild-cluster bootstrap acknowledge)
- **Action**: 3개 위치에서 일관된 "11이 minimum (5–6) 위, 권장 (≥20–30) 아래" 진술

### 9.10. EqualWeight directional sign leakage (B-C1)
- **Trigger**: 3-P0-5 (ch3:695)
- **Cross-check**: ch4 EqualWeight 컬럼 인용 (특히 ch4:801, 854, 936, 961, 963), ch5:162 (5-P0-3와 정합)
- **Action**: ch3:695 명시화 후 ch4의 EqualWeight 인용 모두 검토 — Stage 2 EqualWeight column이 label-aware임을 인정. ch5에서 implication 명시

---

## 10. 충돌 위험 결함

같은 라인 또는 인접 영역을 건드리는 fix가 충돌 위험 있음. 통합 수정안 제시.

### 10.1. Ch1:150–153 (Contribution 3 단락)
**충돌 fix**: 1-P0-8 (ch1:152 "operationally equivalent"), 1-P2-12 (ch1:142 broadest scope), 1-P0-6 (ch1:117 TikZ — 인접 figure)

**통합 수정안**: ch1:150–153 paragraph를 한 번에 재작성:
- L150 Contribution 3 (two-part) 표현 유지 (cycle 1 G07 LANDED)
- L152 `operationally equivalent` → `statistically indistinguishable within $\pm$0.04 MCC non-inferiority bound`
- L142 broadest scope에 `(11-pathogen main + 12-pathogen Stage 3 extension)` footnote
- L117 TikZ는 별도 figure body — 충돌 없음, 단 일관 표현 검증

### 10.2. Ch3:881–916 (ANOVA + Bootstrap subsection)
**충돌 fix**: 3-P0-3 (ch3:885 cell-level 0.234), 3-M-10 (ch3:881 ANCOVA paragraph 추가), 3-M-11 (ch3:881 Bayesian paragraph 추가), 3-P0-4 (ch3:912–916 wild-cluster), 3-m-19 (ch3:887 Levene F)

**통합 수정안**: ch3 §3.2.5.1 (ANOVA section)을 한 번에 확장:
1. L881 직후: ANCOVA paragraph (3-M-10)
2. ANCOVA 다음: Bayesian partial-pooling paragraph (3-M-11)
3. L885 headline ω²=0.296 → cell-level 0.234 disclosure (3-P0-3)
4. L887 Levene F statistic 추가 (3-m-19)
5. L912–916 BCa/cluster bootstrap → wild-cluster acknowledge (3-P0-4)

전체 §3.2.5.1을 한 번에 rewrite. 작업 시간 누적 ~80min (개별 합 = 80min, 충돌로 인한 중복 작업 0).

### 10.3. Ch3:131–135 (MAFFT + cutoff)
**충돌 fix**: 3-P0-1 (ch3:131 cutoff date), 3-P0-2 (ch3:131–135 MAFFT)

**통합 수정안**: §3.2.1 Sequence Collection 단락 + Table tab:pathogen_data를 한 번에 확장:
- Table에 "Query date (YYYY-MM-DD)" 컬럼 + "MAFFT algorithm selected" 컬럼 추가
- 본문 L131–135 자인 문장을 "see Table for per-pathogen log"로 단축

### 10.4. Ch5:155 + ch5:162 (Contribution recap)
**충돌 fix**: 5-P0-1 (ch5:155 saturation caveat), 5-P0-3 (ch5:162 4-feature 97.6%)

**통합 수정안**: ch5 §6.0 (Contribution recap paragraph)를 한 번에 정리:
- L155 contribution 1 saturation caveat append
- L161–162 4-feature retention "relative to 10-feature ensemble" caveat append
- L161–162 단일/통합 enrichment 구분 (5-M-11)

작업 합 = 30min (5-P0-1 + 5-P0-3 + 5-M-11)

### 10.5. Abstract.tex:2 + abstract.tex:11
**충돌 fix**: A-P1-4 (L2 retrospective caveat), A-P1-5 (L11 Bonferroni 3.9e-9)

**통합 수정안**: 두 fix가 다른 sentence를 건드림 — 충돌 없음. 단일 commit으로 가능.

---

## 11. 재실험 필요 결함

**없음** — 모든 fix가 텍스트/표/수식 차원에서 해결 가능.

다만 다음 fix는 *재현 1회* (수정이 아닌 *값 산출*)이 필요:

| Fix | 재현 작업 | 시간 |
|------|-----------|------|
| 3-M-13 (ch3:655 Tranception removal sensitivity ω²) | 단일 Tranception 채널 제거 후 ANOVA 1회 | 30–60min |
| 3-m-17 (ch3:319 Replicate count 검증) | 원논문 6편 확인 | 20min |
| 3-m-18 (ch3:615/619/688 patch versions) | 환경 버전 확인 (`mafft --version`, `iqtree -v`, etc.) | 5min |
| 3-m-19 (ch3:887 Levene F, df) | scipy.stats.levene 결과 재출력 | 5min |
| 3-m-20 (ch3:914 BCa coverage simulation) | n=11 시뮬레이션 1회 | 30min |
| 3-P0-6 (ch3:296/309/317 preregistration) | lab notebook 일자 확인 | 5min (사용자 확인) |

**총 재현 작업 시간**: ~2시간 (모두 Tier 2 또는 P1·P2)
**Tier 1 (P0 19건)에 한정한 재현 작업 시간**: ~5min (3-P0-6 lab notebook 일자만)

---

## 12. 권장 작업 순서

### Phase A: 사전 검증 (30min)
1. **3-P0-5 (EqualWeight code 검증)** — Stage 2 EqualWeight column이 실제 어떻게 label에서 sign을 학습하는지 코드 추적. 만약 LOPO 내부에서 fold별 재계산되면 leakage 없음 (텍스트 명시화로 충분); 만약 all-11 pathogen 일괄 fitting이면 명시 + sensitivity 권장.
2. **3-P0-6 (lab notebook 일자)** — 사용자 확인.

### Phase B: 챕터별 병렬 패치 (P0만, ~6시간)
3개 챕터-fix 에이전트 병렬 실행 권장:

**Agent 1 (Abstract + Ch1, ~90min)**
- A-P0-1, A-P0-2 (kr abstract 동기화)
- 1-P0-4 + 1-P0-9 (panel 11/12 일괄)
- 1-P0-6 (TikZ HIV-1 novel-only 우선)
- 1-P0-7 (Bolker caveat)
- 1-P0-8 (operationally equivalent)
- 1-P1-3 + 1-P1-5 (G08 vocabulary)

**Agent 2 (Ch2 + Ch3, ~3.5시간)**
- 2-P0-1, 2-P0-2, 2-P0-3, 2-P0-4 (ch2 4개 P0)
- 3-P0-1, 3-P0-2 (cutoff + MAFFT — Table 동시 수정)
- 3-P0-3 (cell-level 0.234)
- 3-P0-4 (wild-cluster)
- 3-P0-5 (EqualWeight leakage 명시화)
- 3-P0-6 (preregistration)
- 3-P0-7 (repo URL inline)

**Agent 3 (Ch4 + Ch5 + Ch6, ~2.5시간)**
- 4-P0-1 (cell-level 0.234 — ch3와 정합)
- 4-P0-2 (Bonferroni denominator)
- 5-P0-1, 5-P0-2, 5-P0-3, 5-P0-4, 5-P0-5 (ch5 5개 P0)
- 6-P0-1 (Friedman demote)
- 6-P0-2 (broadest re-statement)
- 6-P0-5 (PAHD-R scope creep)

### Phase C: Cross-chapter 정합 검증 (30min)
모든 P0 패치 후 §9 "Cross-chapter 의존성 그래프"의 10개 묶음을 grep으로 일괄 검증:
- `grep -n "two-stage\|two stage\|2-Stage" abstract*.tex ch*.tex` → G08 family
- `grep -n "11 pathogen\|12 pathogen\|11-pathogen\|12-pathogen"` → 11/12 panel
- `grep -n "operationally equivalent\|97.6%\|98%"` → 4-feature 표현
- `grep -n "0.234\|cell-level"` → ω² demote
- `grep -n "3.9.*10\|3\\.9 \\\\times 10"` → novel-only Bonferroni
- 등

### Phase D: P1/P2 추가 패치 (선택, ~6시간)
Tier 2 (4건 P1 강화) + Tier 3 (7건 polish):
- 3-M-13 (Tranception sensitivity, 재현 1회)
- 4-M-3, 4-M-4, 4-M-5, 4-M-6, 4-M-7
- 5-M-6 (PAHD-R 위치), 5-M-7, 5-M-8, 5-M-9, 5-M-10, 5-M-11
- 6-P1-3, 6-P1-4, 6-P1-7
- 나머지 P2

### Phase E: 자동검증 + LaTeX 재빌드 (5min)
- `python verify_dissertation.py` (88/88 PASS 유지 확인)
- `cd presentation && latexmk` 또는 thesis 빌드
- cycle 3 적대 검수 (선택)

---

## 13. 챕터별 작업 시간 요약

| 챕터 | P0 | P1 | P2 | 합계 |
|------|----|----|----|------|
| Abstract (KR + EN) | 15min (2건) | 23min (4건) | 3min (1건) | **~41min (7건)** |
| Ch1 | 48min (5건) | 25min (3건) | 33min (4건) | **~106min (12건)** |
| Ch2 | 45min (4건) | 43min (4건) | 38min (5건) | **~126min (13건)** |
| Ch3 | 130min (7건) | 150min (8건) | 60min (8건) | **~340min (23건)** |
| Ch4 | 18min (2건) | 46min (6건) | 8min (3건) | **~72min (11건)** |
| Ch5 | 45min (5건) | 63min (6건) | 29min (5건) | **~137min (16건)** |
| Ch6 | 35min (3건) | 24min (4건) | 29min (5건) | **~88min (12건)** |
| Cross-chapter polish | — | — | 30min | 30min |
| **합계** | **336min (28건)** | **374min (35건)** | **230min (41건)** | **~940min ≈ 15.7시간 (94건)** |

(주: 위 합계는 각 fix를 *독립적으로* 시간 추정한 값. §10 "충돌 위험 결함"의 통합 수정안을 적용하면 ch3/ch5 등에서 ~30min 절약 가능 → 실제 작업 시간 ~14시간.)

### 권장 실행 옵션 (summary_cycle2 §7 기준)

| Option | 작업 범위 | 작업 시간 | 통과 확률 |
|--------|-----------|----------|----------|
| **A**. 현 상태 defense | cycle 1 fix만 | 0h | 70~80% |
| **B**. Tier 1 P0 19건 (권장) | §12 Phase A+B+C+E | ~7h | 80~85% |
| **C**. Tier 1+2+3 모두 (Tier 2 = 재현 1건 포함) | §12 Phase A~E 전체 | ~15h | 85~90% |

---

## 14. 최종 메모

1. **재실험 0건 원칙**: cycle 2가 새로 발견한 모든 결함은 *텍스트 수정*으로 해결 가능. Tranception sensitivity (3-M-13)와 Levene F (3-m-19) 등 5건만 재현 1회 (계산 1회) 필요 — 모두 P1·P2.

2. **EqualWeight leakage (3-P0-5)는 가장 위험한 신규 결함**: code-level 검증이 *반드시* 선행되어야 함. 검증 결과:
   - **Case 1**: LOPO fold별 sign 재계산 → 명시화로 해결 (15min)
   - **Case 2**: 전체 11 pathogen으로 sign fitting → 추가 sensitivity 1회 (1h) + 텍스트 명시화

3. **한국어 abstract 동기화 (A-P0-1, A-P0-2)는 가장 저비용 고가치 fix**: 15분 작업으로 cycle 1 G07/G08 family를 한국어에도 propagate. 한국 위원회는 즉각 식별 가능.

4. **Ch3가 가장 무거움 (5시간, 23건)**: cycle 1 시점의 6 Critical 미수정이 누적. ch3 §3.2.5.1 ANOVA section의 통합 rewrite (§10.2)가 효율적.

5. **Cross-chapter validation은 단일 grep으로 가능**: §12 Phase C 권장 grep 명령들을 패치 후 1회 실행.

6. **Cycle 2에서 발견된 cycle 1 P1 escalation (P0 재분류)**:
   - Ch1 G24 (panel 11 vs 12) → 1-P0-4
   - Ch3 cycle 1 6 Critical 전부 → 3-P0-1~3-P0-7
   - Ch4 cycle 1 5 Major (Friedman power, baseline SD, 280 vs 780, Bonferroni-survivor mean, HIV-1 nA) → 4-M-3~4-M-8 (P1 유지)
   - Ch5 cycle 1 7 Critical 4건 partial → 5-P0-3 (C6), 5-M-8/9/10 (C2/C4/C5/C7)
   - Ch6 cycle 1 M1~M3 → 6-P0-2/6-P1-3/6-P1-6

7. **방어 시 가장 위험한 질문 매핑** (phase4_professor.md TOP-3):
   - Q1 (Tranception/ESM-2 collinearity): A-P1-6 + 3-M-13 + 5-P0-4
   - Q2 (Time-forward validation 부재): A-P1-4 + 5-P0-5 + 3-M-12 (H3N2 pilot protocol)
   - Q3 (cell-level demote + wild-cluster): 3-P0-3 + 3-P0-4 + 4-P0-1 + 5-M-10

위 매핑된 9개 fix 모두 적용 시 TOP-3 질문 답변이 본문에 anchor됨.

---

**산출물 검증**: 본 매트릭스는 cycle 2 8개 review.md + cycle 1 6개 phase2b.md + summary 2개를 모두 통합. 총 fix 94건 (P0 28, P1 35, P2 31). 추측은 review.md의 인용 범위 내로 제한; line 번호는 모두 cycle 2 review.md의 file:line 명시값을 그대로 사용.
