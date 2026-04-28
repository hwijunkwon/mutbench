# Ch3 Methods 심층 검토

대상: `/proj/paper/paper/dissertation/chapters_en/ch3_methods.tex` (909 lines)
검토일: 2026-04-28
검토자: Adversarial Methods Review Agent

---

## Critical (재현 불가 / 결정적 결함)

| ID | 위치 | 문제 | 근거 | 수정 |
|----|------|------|------|------|
| C1 | L131 | **Sequence cutoff date 모호**. "all available sequences as of December 2024" — 정확한 다운로드 날짜(YYYY-MM-DD), 11개 pathogen별 다운로드 일자가 다른지 여부 미명시. RSV/H3N2 등 빈번 업데이트 pathogen은 같은 "December 2024"여도 day-level 차이로 N이 다를 수 있음. | "all available sequences as of December 2024 were downloaded" (L131) — 단일 monolithic 표현, 정확한 query date 또는 query-string per pathogen 부재 | pathogen별 다운로드 일자 표(예: `Table~\ref{tab:pathogen_data}`에 "Query date" 컬럼 추가), GenBank query 전체 string을 supplement에 첨부 |
| C2 | L131--132 | **MAFFT 알고리즘 비결정성**. `--auto` mode는 입력 크기에 따라 FFT-NS-2/L-INS-i/G-INS-i 중 자동 선택; 본문은 "FFT-NS-2 is typically selected, but … may differ across pathogens, and the effect of this difference … was not controlled" (L132--133)을 자인. 11개 pathogen 각각 어느 알고리즘이 실제 선택되었는지 미보고 → 타 연구자가 같은 데이터로 alignment 재현 시 다른 알고리즘이 호출될 수 있음. | L131 "MAFFT v7.505 … with the \texttt{--auto} mode"; L132--133 미통제 자인 | 11개 pathogen별 실제 선택된 MAFFT 알고리즘과 invocation command를 명시한 supplementary table; 또는 `--retree 2 --maxiterate 0` (FFT-NS-2)으로 강제 고정한 sensitivity run 추가 |
| C3 | L296, L309, L317 | **Layer A/B/C 임계값의 사후 결정 의심**. (1) Layer A: "literature-curated" + "≥3 independent lineages" 기준은 SARS-CoV-2/H3N2에만 적용 (L296), 나머지 9개는 literature list에 의존 → unified 기준 부재. (2) Layer B: dN/dS < 0.5 (L309) — Yang 2007 인용했으나 통상 ω<1이 purifying의 정의이므로 0.5 컷의 출처와 사전 결정 시점이 불명확. (3) Layer C: top 20% (L317) — sensitivity sweep 10/20/30%은 사후 보정으로 보일 수 있음. **사전 등록(preregistration) 기록 또는 lab notebook 기재일자가 어디에도 인용되지 않음.** | L296 "≥3 independent lineages"; L309 "dN/dS $<$ 0.5"; L317 "top 20\% … threshold was chosen to balance sensitivity and specificity"; sensitivity는 4 pathogens에서만 검증 | (a) ground truth 기준이 stage 1 시작 전에 결정됐다는 명시 문장 추가 (예: "Layer A/B/C 임계값은 Stage 1 분석 시작(2024-XX-XX) 이전 freeze된 SOP에 따라 적용됨"); (b) 6개 DMS pathogen 전체에 대한 sensitivity sweep 결과를 supplement에 첨부 (현재 4개만 sweep) |
| C4 | L902--904 | **Code repository URL 부재**. Section은 "see Chapter~\ref{ch:conclusion}, Section~\ref{sec:code_availability} for the canonical repository URL, commit hash, and Zenodo DOI"로 forwarding하나 Ch3 자체에는 URL/DOI 미기재. 박사논문 심사 시점에 Ch6에 실제 채워졌는지 별도 검증 필요. | L904: "the canonical repository URL, commit hash, and Zenodo DOI" — 모두 forward reference | Ch3 footnote에 URL+commit+DOI를 직접 기재 (forward reference는 보조용으로만); 또는 적어도 placeholder 명시 |
| C5 | L820--826 | **ANOVA pre-registration 부재 + multiple testing 정책 사후 정당화 의심**. "No family-wise multiple testing correction (e.g., Bonferroni, Holm) was applied to the ANOVA results because the analysis is exploratory rather than confirmatory" (L826). 그러나 Ch5/Ch4에서 ω²=0.296 interaction 결과는 confirmatory hypothesis로 사용됨 → exploratory/confirmatory 분류가 결과에 따라 달라진 사후 라벨링일 가능성. 또한 vaccine escape 분모 780(=20×39)의 결정 시점도 불명확. | L826: exploratory 주장; 그러나 Ch4에서 동일 ω²을 핵심 conclusion으로 인용 | "scoring × pathogen interaction" hypothesis가 데이터 lock 이전에 기술됐다는 명시; 또는 동일 데이터에서 confirmatory 사용을 자제하고 hold-out validation 결과(LOPO)만으로 결론 |
| C6 | L317 | **Layer C threshold 일관성 검증 미흡**. top 20% 기준은 6 pathogen에 동일 적용되나 sensitivity sweep은 4 pathogen(SARS/H3N2/HIV/RSV)에만 수행 — Rabies와 EV-A71에 대해 threshold robustness 검증 부재. | L317: "Sensitivity analysis … checked Layer C rankings at thresholds 10\%, 20\%, and 30\% (4 pathogens with available DMS at the time of the sensitivity sweep)" | Rabies/EV-A71 sensitivity sweep 결과를 추가하거나, 명시적으로 "본 챕터에서 Layer C threshold robustness는 4 pathogen에 한해 검증되었으며, Rabies/EV-A71 robustness는 future work" 한정 |

---

## Major

| ID | 위치 | 문제 | 근거 | 수정 |
|----|------|------|------|------|
| M1 | L131 | **GISAID 미사용 정당화 부재**. SARS-CoV-2/Influenza의 표준 reference DB는 GISAID; NCBI GenBank만 사용한 이유와 데이터 coverage 차이의 영향이 미논의. SARS-CoV-2 4,982 sequences는 GISAID 1500만+ sequence와 비교 시 매우 작음. | L131: "FASTA sequences for each pathogen were collected from NCBI GenBank by querying each target protein name" | "GISAID 대신 NCBI GenBank를 사용한 이유(API 접근성/redistribution license/등)와 그것이 cross-pathogen 균일성에 미치는 영향" 1 paragraph 추가 |
| M2 | L296 | **Layer A 정의의 pathogen별 비대칭 quantitative impact**. "discussed in Chapter 5"로 forward — Methods에서 정량 영향(ω²) 수치 미제시. 검토자가 Methods만 보고는 ω²=0.296의 ground-truth-dependence를 평가 불가. | L296: "Chapter~\ref{ch:discussion} where its quantitative impact on the headline $\omega^2 = 0.296$ is discussed" | Ch3에서 직접 sensitivity number(예: "Layer A 정의를 phylogenetic-only로 통일 시 ω²=X로 변동") 한 줄 명시 |
| M3 | L317, L319, L323 | **DMS 데이터 출처 query/version 미고정**. Dadonaite 2023/2024 등은 GitHub 또는 zenodo에 release 별로 다른 버전이 있음. 본문은 "released processed-fitness tables"이라고만 적고 commit hash/zenodo DOI를 명기하지 않음. | L319: "Table~\ref{tab:dms_preprocessing} … cell-line and replicate-aggregation choices follow the released-source defaults" | DMS 6개 source의 각 download URL + version/commit/DOI를 Table dms_preprocessing에 컬럼으로 추가 |
| M4 | L514--519 | **hotspot-score 합성 메트릭의 근거 빈약**. (recall+precision+stability)/3 단순 평균의 정당성: weighted alternative 비교(Eq.~\ref{eq:weighted_hotspot_score} L867)는 있으나, F1 (=harmonic mean of recall, precision)을 stability와 결합하는 alternative와의 비교 부재. 또한 stability를 0.33 weight로 배치한 근거(prior)가 없음. | L514: $\text{hotspot-score} = (\text{recall}+\text{precision}+\text{stability})/3$; L865--873 weight sensitivity는 있으나 F1 alternative 비교 없음 | F1+stability 조합과의 ranking-correlation 보고; 또는 단순 평균 채택 이유 (예: "non-monotonic harmonic mean이 stability와 interaction 시 불안정하여 arithmetic mean 채택") 명시 |
| M5 | L516--518 | **stability metric definition 모호**. "100 random 80% subsampling iterations … Bernoulli mask independently zeroes out approximately 20% of genomic positions" — Bernoulli vs. fixed 80% subsample 구분 모호 (Bernoulli with p=0.8은 평균만 80%); seed 고정 명시는 L904에 있으나 stability 100 iteration의 seed sequence(예: 42, 43, …, 141) 미명시. | L516--518 | "100 iteration seed = 42..141" 또는 "seed=42, repeated draws from default RNG" 명시 |
| M6 | L613 | **IQ-TREE bootstrap 1,000 + Fitch parsimony homoplasy** 절차. 1,000 ultrafast bootstrap은 reported되나 실제 homoplasy 계산이 (a) ML tree 1개에 대해서인지, (b) bootstrap consensus에서인지, (c) bootstrap 별 평균인지 모호. 또한 outgroup 선택, multifurcation 처리 미명시. | L613: "Homoplasy counts were computed by Fitch parsimony on the resulting maximum-likelihood tree" — 단일 ML tree만 사용한 것으로 보이나 bootstrap support 활용 미명시 | "Single ML tree without bootstrap weighting; outgroup = X" 명시; bootstrap support filter 적용 여부 |
| M7 | L617 | **FUBAR 설정**. "default posterior probability threshold of 0.9"라고만 적었으나 grid (default 20×20), genetic code (default universal), branches (Internal/All) 미명시. | L617 | grid size, branch class, FUBAR cache 처리 명시 |
| M8 | L631 | **EqualWeight 'directional sign rule'의 leakage 위험**. "training pathogens"에서 sign을 결정한다 했으나 Stage 2/3에서 모든 11 pathogen이 evaluation set인데 어느 pathogen이 "training"인지 미정의. LOPO 안에서 sign이 fold별 재계산되는지 일괄 결정인지 모호 → Layer A label leakage 가능성. | L631: "empirically observed sign of the feature's per-position correlation with Layer A on the training pathogens" | LOPO에서 sign이 (a) all 11 pathogen 일괄결정, (b) fold별 n-1 pathogen 재결정 중 어느 것인지 명시; leakage 위험 명시 |
| M9 | L840 | **LOPO chance level 계산 오류 가능성**. "Under random selection from 280 possible combinations (20 × 14), the expected concordance rate is approximately 0.36\%". 1/280 = 0.357% 맞지만, 이는 "test-best와 train-best가 정확히 동일 cell"일 확률; concordance를 어떻게 정의하는지(top-1 일치 vs. rank correlation) Methods에 미명시. | L840 | concordance 정의 명시: "training-best 1개 cell vs. test-best 1개 cell의 정확 일치" |
| M10 | L500 | **HDBSCAN 파라미터 기본값 채택의 정당화 부재**. min_cluster_size=5, min_samples=1, eom — 작은 protein(EV-A71 261 AA)에 대한 sensitivity 미보고; 5개 변형 중 v3가 cross-pathogen에서 어떻게 작동하는지 ambiguous. | L499--500 | 작은 alignment(261 AA)에 대한 HDBSCAN 안정성 sensitivity 추가 |
| M11 | L673 | **Supervised ML 제외 정당화**. "9--54 Layer A positives … insufficient for training generalizable classifiers" 주장. 그러나 RF는 Stage 3 (L898)에서 사용됨 → 모순 또는 boundary 불분명. | L673 vs. L898 | "Stage 3 RF는 feature importance triangulation only, hotspot detector로 사용 안함" 명시 (이 점 일부는 L898에 있으나 L673와의 일관성 강화 필요) |
| M12 | L309 | **Layer B "evolutionary conservation" 기준의 pathogen 적용 범위**. dN/dS<0.5 기준은 모든 pathogen에 일괄 적용되었나, 아니면 일부 pathogen은 순수 structural-essentiality만 사용했나? Table gt_positions에 Layer B 카운트(0~229)는 큰 분산 → 기준 일관성 의문. | L309: 두 evidence type 언급, but pathogen별 어느 것이 적용됐는지 표기 부재 | Table에 "Layer B 기준 type" 컬럼 추가 (e.g., "Structural+dN/dS", "Structural only") |
| M13 | L879--881 | **Region-level bootstrap이 Stage 1만의 도구**. 7개 functional region을 단위로 한 bootstrap은 Stage 1 SARS-CoV-2 전용; Stage 2 11 pathogen에 대해서는 region-level resampling 절차가 없는데 이 sub-section은 Section eval_stat_design (Stage 2 포함) 안에 위치 → scope confusion. | L879 위치(stage 2 evaluation section 내) | 명시적으로 "Stage 1 only" 라벨 부착 |
| M14 | L319 | **Replicate count 모두 "2"로 동일** Table dms_preprocessing. 여러 source 중 H3N2/HIV-1 등은 실제 publication에서 3+ replicate가 있는 경우가 있음 → 검증 필요. | L331--336 | original publication별 replicate count 재확인 후 정확 기재 |

---

## Minor

| ID | 위치 | 문제 | 근거 | 수정 |
|----|------|------|------|------|
| m1 | L6 | "39 parameter variants"가 abstract paragraph에서 첫 등장하나 39 = 3+3+2+2+3+3+1+2+2+2+2+4+9+1 = 39 산술 검증 필요. Table 4 합산도 일치 | L686--707 | 표 하단에 산술 합계 한 줄 추가(이미 39로 표기됨) — pass; 다만 본문에서 합산 배경(왜 SWAN만 9-variant인가) 한 문장 부족 |
| m2 | L46 | DMS 인용이 "Dadonaite et al. (2024)"로 in-text 형식; 다른 곳은 \cite — 스타일 일관성 결여 | L46 | `\cite{dadonaite2024nature}` 사용 |
| m3 | L391 | HIV-1 reconciliation note: 23 (literature) vs. 26 (alignment QC). "the difference does not affect any headline conclusion … binary label, not a count"는 정확하나 검토자가 stages 간 number 추적이 어렵다 → table에 두 column(Literature, Operational) 명시가 더 견고 | L391 | tab:gt_positions에 "Literature / Operational" 두 컬럼 |
| m4 | L500 | "pinned in the released configuration files described in the Code and Data Availability subsection at the end of this chapter" — actual file name 미기재 (e.g., `configs/detector_params.yaml`) | L500 | actual file path 명시 |
| m5 | L613 | IQ-TREE 2 — minor version (2.x.y) 미명시; 결과 차이 가능 | L613 | full version (예: 2.2.0) |
| m6 | L617 | HyPhy v2.5 — minor version 미명시 | L617 | full version (예: 2.5.46) |
| m7 | L626 | ESM-2 checkpoint hash/release date 미명시 (Hugging Face 버전 변경 가능) | L626 | HF revision SHA 명시 |
| m8 | L820 | "20 levels (scoring), 14 levels (family), 11 levels (pathogen)" — 14 family 중 SWAN 9-variant가 family 차원에서 어떻게 collapse 되는지 본문에 구체화 부족 (Table 4와 합산 매핑 명시) | L715에 일부 있음 | "각 family 내 variants는 within-cell observation으로 처리되어 residual에 흡수" 한 줄 추가 |
| m9 | L823 | Levene's test 구체적 통계량(F, df) 미보고 | L823 | F=X, p=Y 명시 |
| m10 | L825 | ART ANOVA 결과 보고; 그러나 Aligned Rank Transform은 Wobbrock의 다른 software(`ARTool`) 가정 — 사용된 implementation(R `ARTool` v?, Python equivalent?)명시 부족 | L825 | `ARTool R package vX.Y.Z` 명시 |
| m11 | L851 | "1,000 resamples" combination-level cluster bootstrap — 10,000 (BCa pathogen-level)와 차이 정당화는 있으나 (compute footprint), reproducibility 측면에서 ratio 정당화 부족 | L851 | 1,000 → 충분 검증 (예: percentile CI half-width 변화 표) supplement |
| m12 | L884--887 | Permutation N=1,000 — "$count/n_{\text{perm}}$" pseudo-count 처리(0 발생 시 p < 1/1001 표기 등) 미명시 | L887 | "p = (count+1)/(n+1)" 또는 "p < 0.001 reported when count=0" 명시 |
| m13 | L850 | "$n=11$이라 BCa 95% coverage가 nominal보다 낮다"고 인정하나 simulation으로 actual coverage를 대체 보고하지 않음 | L850 | n=11 시뮬레이션 coverage(예: actual 90%) 한 줄 |
| m14 | L132 | MAFFT v7.505 — `--auto` mode 결정 로직(sequence 수>200 → FFT-NS-2 등) 인용 부재 | L132 | Katoh & Standley 2013 Section 인용 |
| m15 | L905 | "library versions … pinned in the released environment file" — `environment.yml` or `requirements.txt` 파일명 미명시 | L905 | actual filename |
| m16 | L317 | "balance sensitivity and specificity" — 임계값 선택 metric (Youden's J 등) 미명시 | L317 | "qualitative balance based on …" 또는 정량 metric |
| m17 | L498 | "$\gamma = 0.5$ … sensitivity to $\gamma \in \{0.25, 0.5, 1.0\}$ shifts … by ±0.01" — 검증 시 어느 pathogen에서? 11 pathogen 평균인지 SARS-CoV-2만인지 불명 | L498 | "across 11 pathogens (mean ± SD)" 또는 "for SARS-CoV-2" 명시 |
| m18 | L674 | ω² = 0.013 (detection family) 수치를 Methods에서 forward citation 없이 그대로 인용 — Methods는 결과를 미리 본문에 노출함 | L674 | "(reported in Chapter 4, Table X)" cross-ref |

---

## 재현성 체크리스트

| 항목 | 명시 여부 | 위치 |
|------|---------|------|
| 데이터 origin (NCBI GenBank vs. GISAID) | YES (NCBI GenBank only) | L131 |
| GenBank query string per pathogen | NO (예시 1개만) | L131 |
| Pathogen별 reference accession | YES | Table pathogen_data, L148--158 |
| 시퀀스 cutoff date (정확한 YYYY-MM-DD) | NO ("December 2024"만, day-level 미명시) | L131 |
| 다운로드 일자 per pathogen | NO | (없음) |
| 사용 sequence count (raw / unique / aligned) | YES (raw, unique 두 개; aligned는 동일 가정) | Table L148--158 |
| QC 기준 (>5% N 제거, dedup) | YES | L131 |
| Truncation 절차 (min length) | YES | L134--135 |
| MAFFT version | YES (v7.505) | L131 |
| MAFFT 옵션 (--auto vs 명시 알고리즘) | PARTIAL (--auto, but actual algorithm per pathogen 미보고) | L131--133 |
| MAFFT 비결정성 통제 | NO (자인됨) | L132--133 |
| IQ-TREE version | PARTIAL (major version 2; minor 미명시) | L613 |
| IQ-TREE bootstrap N | YES (1,000 ultrafast) | L613 |
| Tree outgroup / rooting | NO | (없음) |
| HyPhy version | PARTIAL (v2.5; minor 미명시) | L617 |
| HyPhy MG94×REV codon model | YES | L617 |
| FUBAR posterior threshold | YES (0.9) | L617 |
| FUBAR grid size, branches | NO | (없음) |
| Random seed (global) | YES (seed=42) | L904 |
| Stability bootstrap N | YES (100 iter) | L517 |
| Stability per-iteration seed sequence | NO | (없음) |
| BCa bootstrap N | YES (10,000) | L850 |
| Cluster bootstrap N | YES (1,000) | L851 |
| Permutation N (label shuffle) | YES (1,000) | L884 |
| Permutation N (circular) | NO (N 미명시) | L885--886 |
| Permutation pseudo-count (count=0 처리) | NO | L887 |
| Subsample fractions | YES (25/50/75/100%) | L855 |
| Subsample iterations per fraction | NO | L855 |
| Code repository URL | NO (Ch6 forward ref) | L904 |
| Commit hash | NO (Ch6 forward ref) | L904 |
| Zenodo DOI | NO (Ch6 forward ref) | L904 |
| 컴퓨팅 환경 (Python/OS) | PARTIAL (Python 3.10, NumPy 1.24, SciPy 1.11; OS 없음, GPU 없음) | L904 |
| ESM-2 checkpoint | YES (esm2_t33_650M_UR50D) | L626, L904 |
| ESM-2 HF revision SHA | NO | (없음) |
| environment.yml / requirements.txt 파일명 | NO | L904 |
| DMS source URL/version per pathogen | NO (인용만) | Table dms_preprocessing |
| DMS replicate count (publication별) | PARTIAL (모두 "2"로 동일하게 적힘 — 검증 필요) | Table L331--336 |
| Layer A literature reference (per pathogen) | YES | Table gt_positions |
| Layer A 기준 통일 여부 | NO (heterogeneous, 자인됨) | L296, L393 |
| Layer B dN/dS threshold | YES (0.5) | L309 |
| Layer B pathogen별 적용 type | NO | (없음) |
| Layer C top-X% threshold | YES (20%) | L317 |
| Layer C threshold sensitivity sweep | PARTIAL (4/6 pathogen만) | L317 |
| Layer A/B overlap 처리 | YES | L346--350 |
| Layer A/C 충돌 처리 | YES | L352--357 |
| Detector parameter table | YES | Table detection_variants L686--707 |
| Detector default seeds (random_state) | PARTIAL (RF: 42; HDBSCAN/DBSCAN: deterministic; 기타 detector seed 명시 없음) | L499, L898 |
| RF hyperparameters | YES (200, max_depth 5, balanced, seed 42) | L898 |
| RF cross-validation 방식 | YES (stratified 5-fold per pathogen) | L898 |
| ANOVA SS type | YES (Type II) | L822 |
| ω² formula | YES (non-partial, Eq L829) | L829--831 |
| Multiple testing 정책 | YES (no correction for ANOVA; Bonferroni 780 for vaccine escape) | L826 |
| Bonferroni 분모 결정 시점 (preregistration) | NO | (없음) |
| Pre-registration / SOP freeze date | NO | (없음 — 본 챕터 어디에도 preregistration 또는 lock-date 명시 없음) |
| EqualWeight directional sign 결정 절차 (LOPO 내 leakage 통제) | NO | L631 |

---

## 챕터 종합 평가

**합격선: CONDITIONAL** — 박사학위 통과 가능하나 다음 조건 충족 시.

**Strengths:**
- Methods 챕터로서 framework architecture, ground truth 다층 설계, scoring/detection family 분류, evaluation metric 다양성, statistical safeguard(parametric+nonparametric+ART)는 잘 구성됨.
- ω², LOPO, BCa, cluster bootstrap, permutation 등 통계 다중 lens 사용은 호평.
- HCV E2 좌표 caveat (L389), HIV-1 23 vs. 26 reconciliation (L391), Layer A heterogeneity 자인(L296)는 정직.

**Weaknesses (PASS 위해 반드시 보강):**

1. **Critical C1 (cutoff date), C2 (MAFFT 비결정성), C4 (URL/DOI)** 는 재현성 핵심으로 Ch3 자체에 정확한 값(YYYY-MM-DD, pathogen별 MAFFT 알고리즘 표, URL+commit+DOI)을 직접 기재해야 함. Ch6 forward reference만으로는 부족.
2. **Critical C3 (preregistration 명시 부재)**: Layer A/B/C 임계값과 ω² 분석의 hypothesis가 데이터 lock 이전에 결정되었는지 명시(또는 lab notebook 일자 인용) 필요. 없으면 "exploratory only" 라벨링이 일관되어야 함 (현재 L826 vs. Ch4/5의 confirmatory 사용은 모순).
3. **Critical C5 (Bonferroni 780 분모)**: 사후 결정 의심을 해소하기 위해 "20×39 family는 사전에 fixed grid"라는 명시 + result lock 일자 기재.
4. **Major M3, M14 (DMS source version)**: Layer C 재현을 위한 DMS preprocessing version/commit 6개 모두 보강 필요.
5. **Major M8 (EqualWeight directional sign)**: LOPO 내 sign 재계산 여부는 leakage에 직접 영향. Methods에서 명확화 필수.

**그 외:**
- hotspot-score 합성식의 단순 평균 정당화(M4)는 박사논문 수준에서는 alternative metric (F1+stability) 비교 추가가 안전.
- Minor 항목 18건은 supplementary 또는 footnote 1줄 추가로 해결 가능.

**최종 판정:** Critical 6건 중 적어도 C1, C2, C3, C4, C5(=preregistration/cutoff/MAFFT/URL 4축) 직접 보강 시 **PASS**. 그렇지 않으면 reproducibility section 부실로 외부 심사위원이 "독립 재현 불가" 지적 가능성 매우 높음.

