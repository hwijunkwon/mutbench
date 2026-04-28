# 블루팀 논증 지도 (Phase 1)

작성 시점: 2026-04-28
대상: MutBench 박사학위 논문 (Ch1-Ch6 + abstract)
목적: 핵심 주장 6개 (C1~C6)를 변호 가능한 형태로 정리하고 적대적 공격 시나리오 사전 도출.

---

## 1. 주장 → 증거 매핑

| Claim | 본문 위치 (파일:라인) | 증거 종류 (실험/통계/문헌) | 신뢰도 |
|-------|----------------------|----------------------|--------|
| **C1** MutBench 8,580 평가 (10 info type * 20 scoring * 14 detection family * 39 variants * 11 pathogens) | abstract.tex:2; ch1_introduction.tex:82, 142; ch3_methods.tex:6-7, 22-29, 138-160 (Table tab:pathogen_data); ch4_results.tex:7, 242-244 (식 20*39*11 = 8,580) | 실험 설계 + 표 (pathogen_data, scoring_types, design_characteristics) + 카운트식 본문 명시 | **High**. 8,580 = 20 * 39 * 11 산술 일치. 11 pathogen 시퀀스 카운트 표 명시. "10 info type"은 ch4 627-634의 10개 feature와 일치 (frequency 3, MSA 1, evol-rate 1, deep learning 2, structure 2, chemical 1). 단, "10 information types"와 "20 scoring formulas" 관계는 ch4:243에서 "10 underlying biological features → 20 scoring variants"로 명시. |
| **C2** scoring×pathogen interaction ω²=0.296 (CI [0.195, 0.333]) — 최대 분산 성분 | abstract.tex:2, 10; ch1_introduction.tex:114, 148; ch4_results.tex:11, 359-381 (Table tab:stage2_anova), 386-394, 488-489 (cluster bootstrap); ch5_discussion.tex:281, 285 (Bayesian hierarchical posterior 0.252 [0.188,0.314], P(ω²>0.14)=0.996); ch6_conclusion.tex:12 | 3-way ANOVA + 11-pathogen cluster bootstrap (1,000 resamples) + Bayesian partial-pooling posterior + Cohen 분류 | **High**. Table tab:stage2_anova가 6개 모델 요인의 ω²을 모두 보여주고 scoring×pathogen이 최대임을 표상. CI 0.138 width는 11-cluster 유효 N 반영. 단, **caveat 명시 필요**: within-cell residual ω²≈0.39가 modeled term과 동급이라는 점이 ch4:386-390, ch4:489에서 자체 인정 → "largest *modeled* component" 표현으로 정정되어 있음. 6-category aggregation 시 0.103 (collinearity-robust 하한)도 함께 보고. |
| **C3** LOPO 0/11 + Friedman p=0.990 → universally best 없음 (pathogen-dependent) | ch4_results.tex:402-418 (Table tab:lopo_summary), 420-425 (Fig lopo_crossval), 427, 433-446 (permutation null 분석); ch5_discussion.tex:319-321; abstract.tex:10 | LOPO cross-validation + Friedman χ²=7.69, W=0.037 + 10,000 resamples permutation null | **Medium**. 본문 자체가 "LOPO 0/11 alone is null-consistent under permutation"를 명시 (P(matches=0) ≈ 0.96). Friedman p=0.990은 비유의이므로 "no universal best"의 양가적 해석 (uniformly poor vs pathogen-dependent) 본문 명시 (ch4:439). 결정적 증거는 ω²=0.296 + oracle-vs-generalized gap=0.265 + vaccine-escape audit가 **세트로** 떠받친다는 입장. LOPO/Friedman 단독으로는 weak. |
| **C4** HIV-1 7.19× vaccine escape enrichment, Bonferroni p=2.5e-16; novel-only 7.16-8.24× | abstract.tex:2, 11; ch1_introduction.tex:117, 150, 153; ch4_results.tex:864-887 (Table tab:vaccine_escape_stage3), 890-894 (key findings), 920-921 (circularity audit); ch5_discussion.tex:159-165, 174-179 (Three-tier evidence rule) | Fisher's exact + Bonferroni (780 combos) + Layer A overlap audit (37/45 disjoint = 82%) + worst-case novel-only sensitivity range | **High**. 가장 강건한 주장. 본문이 직접 "HIV-1 is the cleanest external anchor" + 82% disjoint를 명시, Bonferroni 후 H3N2와 함께 생존, SARS-CoV-2는 명시적으로 exploratory로 강등. novel-only 7.16-8.24×의 worst-case Fisher p=5.0e-12은 Bonferroni 780 보정 후에도 ~3.9e-9 수준이라 매우 robust. |
| **C5** 4-feature core (homoplasy, pLDDT, entropy, frequency) ≈ 98% (97.6%) 풀 ensemble | abstract.tex:11, 14; ch1_introduction.tex:150, 152; ch4_results.tex:801-802, 960-962, 970-971; ch5_discussion.tex:196, 244; ch6_conclusion.tex:14 | Leave-one-feature-out + cumulative addition + 12-pathogen panel (core 11 + Zika) feature ablation | **Medium-High**. 0.081/0.083 = 97.6% 산술 일치. 본문이 명시적으로 "no paired-sample significance test was performed, so we report the 4-feature and 10-feature ensembles as *numerically equivalent* under uniform weighting rather than as statistically indistinguishable" (ch4:802, ch5:244)라고 자기-제한. 따라서 "98%"는 통계적 동치가 아닌 산술적 동치라는 점이 정직하게 본문에 박혀 있음. |
| **C6** 9 distinct optimal information types across 11 pathogens | abstract.tex:13; ch1_introduction.tex:146, 148; ch4_results.tex:268-298 (Table tab:stage2_best), 296 footnote (3 pathogen freq 공유 → 9 distinct); ch5_discussion.tex:285 (Bayesian context); ch6_conclusion.tex:12 | per-pathogen best (scoring, detection) 선택 + 카운팅 footnote | **High**. Table tab:stage2_best가 11개 row 직접 나열. footnote가 "HCV, Influenza B, MERS는 모두 freq → 3개 공유, 나머지 8개 distinct → 합 9 distinct" 명시 산술. 단, 이 9 distinct가 "biological types"인지 "scoring formulas"인지 미세 혼선 가능 — 본문은 "9 distinct optimal scoring types"로 일관 표기. 10 information types 중 Tranception, ESM-2, semantic change 모두 "AI-based" 카테고리이므로 정보 타입 아닌 scoring formula로 카운트한 것이 맞음. |

---

## 2. 실패 시나리오 5개

### 시나리오 1: "ω²=0.296의 분산 분해는 within-cell residual 0.39에 잠식되어 있어 modeled term이 dominant라는 주장은 selective"
- **공격 가정**: 적대자가 "modeled ω² 합 ≈ 0.61, residual 0.39, 즉 변산의 39%는 unmodeled three-way interaction과 parameter-variant noise. 그렇다면 'largest source of variance'는 잘못된 표현"이라고 주장.
- **방어 가능 여부**: **방어 가능 (이미 본문이 동일 우려 자체-인정)**. ch4:390의 "'largest source' in this dissertation reads as 'largest modeled component'"와 ch4:386-388 figure caption이 residual 0.39을 별도 표시. ch5:279의 detector-family Simpson's-paradox check가 "framing 'information matters more than algorithm' compares modeled main effects only and is not a claim that detection algorithms are irrelevant within a fixed (scoring, pathogen) cell"로 추가 caveat. → 보강 영역: residual 0.39를 분해할 4-way ANOVA를 선택적으로 시연하면 Tier 1 강도. 현재는 computational cost 명시로 deferred.
- **추가 보강 필요**: parameter-variant 자유도가 detection family마다 다르다는 사실을 더 명시적으로 표 자체에 표기 (39 variants가 14 family에 어떻게 분포되어 있는지).

### 시나리오 2: "HIV-1 vaccine-escape 검증은 entropy×Wavelet이 Layer A best지만 freq×Wavelet이 escape best라 두 베스트가 다르다 — escape가 Layer A를 지지하지 않는다"
- **공격 가정**: 적대자가 "Table tab:stage2_best에서 HIV-1 best = entropy MCC=0.275이지만 escape best는 freq 7.19× — 두 다른 scoring이라 cross-validation이 일관되지 않음."
- **방어 가능 여부**: **부분 방어 가능**. ch4:891이 이미 직접 거론: "HIV-1 Layer A best is *entropy* with Wavelet(t=2.0), MCC 0.275; HIV-1 escape best is *freq* with Wavelet(t=1.5), enrichment 7.19× — both frequency-derived and correlated at ρ ≈ 0.97" — 둘 다 frequency-derived 범주 내라고 명시. ch4:739의 feature correlation 연구도 "ρ_freq-entropy = 0.97"을 supporting evidence로 사용. → "category 수준에서 일치하나 type 수준에서는 다름"이라는 nuance를 명확히 인정한 상태에서 외부 검증 주장은 "Frequency 카테고리가 HIV-1에 가장 좋다"는 더 약한 형태로 재진술 필요.
- **추가 보강 필요**: 만약 reviewer가 "왜 entropy로 escape 검증을 안 했냐?"고 물으면 entropy 7.19× 결과를 별도 보고하는 supplementary table이 있으면 강건. 현재는 freq best만 보고됨.

### 시나리오 3: "8,580 evaluation 자유도는 부풀려져 있다 — within-cell parameter-variant 자유도는 39이고, 이 39 variants는 실질 독립이 아님"
- **공격 가정**: ANOVA 가정인 N=8,580 sample size 가정이 effective N이 훨씬 작다 (3,080 unique cells). degree-of-freedom inflation으로 모든 p-value, ω² CI가 anti-conservative.
- **방어 가능 여부**: **방어 가능 (정확히 본문이 다룸)**. ch4:486-489: "the effective number of independent units is closer to the number of unique cells (20×14×11 = 3,080) than N = 8,580. The ω² estimates should therefore be interpreted as indicative effect sizes... The cluster bootstrap reported below is explicitly the effective-N-aware correction: resampling is performed *at the pathogen level* (11 independent clusters)". → 이 caveat은 본문에서 핵심 방어선이며 cluster bootstrap CI [0.195, 0.333]가 effective-N 보정된 해석으로 사용됨.
- **추가 보강 필요**: wild cluster bootstrap (G=11이 percentile 권장 N=30 미만)을 실제 시도해서 CI가 어떻게 변하는지 시연하는 것이 Tier 1 강도. 현재는 "recommended for any future cycle"로 deferred (ch4:489).

### 시나리오 4: "11 pathogen 패널 자체가 phylogenetic non-independence를 가지고 있다 — 3 family pair (Coronaviridae, Orthomyxoviridae, Flaviviridae)가 ANOVA의 'independent block' 가정을 위반"
- **공격 가정**: ANOVA SE가 underestimated; 11 pathogen이 사실상 8 family로 가야 함.
- **방어 가능 여부**: **방어 가능 (within-family heterogeneity 분석으로)**. ch5:323의 within-family check가 정면 답변: "within each family pair, the best-performing scoring types differ (FUBAR Bayes factor for H3N2 vs.\ frequency for Influenza B; frequency for HCV vs.\ entropy_with_indel for Dengue; Tranception for SARS-CoV-2 vs.\ frequency for MERS), indicating that phylogenetic relatedness does not determine method preference. This within-family heterogeneity strengthens rather than weakens the pathogen-adaptive finding." → 핵심 방어 논리.
- **추가 보강 필요**: phylogenetically-corrected ANOVA (e.g., PGLS) 시연이 있으면 강건. 현재는 within-family pair-level descriptive comparison만.

### 시나리오 5: "Layer A 정의 자체가 pathogen마다 다르다 (HCV는 HVR, Norovirus는 epochal, 나머지는 immune escape) — interaction은 biology가 아니라 curation protocol"
- **공격 가정**: 적대자가 ω²=0.296이 ground truth construction heterogeneity의 artifact일 수 있다고 주장.
- **방어 가능 여부**: **부분 방어 가능 (이미 다층 sensitivity 분석)**. ch5:292의 "Layer-A curation-protocol subset analysis"가 정면 답변: HCV 제외 → ω²=0.199; Norovirus까지 제외 → 0.187; 4-pathogen phylogenetic-only subset (SARS-CoV-2, H3N2, MERS, EV-A71) → 0.137 (n=4에 비해 여전히 medium 이상). ch4:842의 GT heterogeneity 결과는 "5 different best features emerge despite immune_escape ≥71% across all 12 pathogens" + "10/12 pathogens retain same best feature when restricting to immune_escape-only"로 robustness 시연. → 이 시나리오는 여러 단계의 sensitivity 분석으로 둘러싸여 있어 강건하나, 4-pathogen subset의 0.137은 large threshold 0.14보다 약간 낮음.
- **추가 보강 필요**: 정의 통일된 same-evidence-type subset re-estimation은 ch4:490이 "deferred to future work"로 명시. Phase 2 보강 1순위.

---

## 3. 챕터별 최약 지점

| 챕터 | 가장 약한 단락/주장 | 위험 종류 | 보강 방향 |
|------|------------------|----------|----------|
| Ch1 (Intro) | ch1:142-143 "MutBench is the broadest hotspot-detection benchmark to date" | 비교 우위 주장이 task 분리(detection vs prediction)에 의존 — ViroGym 13 viruses, EVEREST v3 40 viruses의 panel이 MutBench 11 viruses보다 큼 | "broadest *region-level hotspot-detection* benchmark"라는 task-specific 한정 표현으로 일관 사용 (이미 abstract:4에 정확히 그 형태로 적힘 — Ch1과 abstract 표현 일관성 점검) |
| Ch2 (Background) | ch2:248 EVEREST v3 reliability fail "over half of WHO-40 panel" 인용 → 본문이 "we describe this as a cross-study *parallel* on pathogen-dependence rather than as independent corroboration of non-transferability per se"로 명시적 자기-제한 | pathogen-dependence의 외부 corroboration이 EVEREST에 의존한다고 잘못 주장하지 않도록 한정 표현이 충분한지 점검 | parallel 표현은 적절. 추가로 ProteinGym과의 comparison에서 task 차이(continuous Spearman vs binary MCC)를 Table tab:benchmark_comparison footnote (ch2:282)에서 다시 강조 — 이미 충실. |
| Ch3 (Methods) | ch3:296의 Layer A heterogeneity 자체-인정. ch3:317 Layer C top-20% threshold 선정 근거 | top-20% 임계값이 임의적이라는 reviewer 공격 가능 | ch3:317이 sensitivity sweep 10/20/30%에서 ranking 안정 (Section ref:dms_evolution_correlation)을 cite, 정면 방어. **약점**: sensitivity sweep이 4 pathogen(SARS-CoV-2, H3N2, HIV-1, RSV)에만 수행 — DMS 가용 6 pathogen 중 Rabies, EV-A71는 이 sweep 미포함. 보강 = sweep을 6 pathogen 전부로 확장. |
| Ch3 (Methods) | ch3:131-133 MAFFT --auto가 pathogen마다 다른 알고리즘을 선택할 수 있고 이 차이가 통제되지 않았다는 자체-인정 | input MSA quality가 systematic하게 pathogen-dependent하면 ω² 일부가 input quality artifact라는 공격 가능 | ch5:294-298 "Scoring input heterogeneity"가 "scoring × pathogen interaction therefore captures both genuine biological signal differences and input quality differences, which cannot be fully separated without controlled experiments using standardized auxiliary inputs"로 정직 인정. → **이 caveat 자체가 가장 약한 부분**: residual error에 input quality 분산이 흡수되어 있을 가능성. 보강 = MAFFT 모드를 한 가지(L-INS-i)로 강제한 robustness re-run을 supplementary로 제시. |
| Ch4 (Results) | ch4:300-301 "permutation analysis shows P(11 unique by chance) ≈ 0.93" 자체-인정 | 11/11 unique combination이 통계적으로 expected 결과라는 정면 인정 — uniqueness 자체로는 근거 약함 | 본문이 "the substantive finding is not the uniqueness itself but the large performance gap between oracle and generalized selection"로 즉시 재방향 (ch4:301). 그러나 abstract:13의 "9 distinct optimal information types" 표현이 9-distinct를 강조하므로, abstract와 ch4:300-301의 자기-제한이 약간 어긋남. 보강 = abstract에서 "9 distinct ... emphasizing oracle-vs-generalized 0.265 MCC gap as the load-bearing quantity" 형태로 표현. |
| Ch4 (Results) | ch4:443-446 LOPO permutation null 결과: "observed training-best generalized MCC of +0.032 exceeds null mean (+0.017) but only by approximately 0.4-0.6 SD, yielding one-sided p ≈ 0.25-0.28" | LOPO oracle-vs-generalized 0.265 gap 자체가 random combination null과 statistically distinguishable하지 않다는 정면 인정 — abstract:10 "0.265 oracle-vs-generalized MCC gap"이 이 caveat 없이 인용됨 | ch4:446의 "tempering does not invalidate the pathogen-adaptive conclusion"는 ω²=0.296 + 9 distinct + HIV-1 anchor의 세트 증거에 의존한다고 명시. 그러나 abstract와 Ch6 conclusion이 0.265 gap을 caveat 없이 사용하므로 이 부분이 가장 위험. 보강 = abstract에 "0.265 gap (null-consistent under permutation; load-bearing claim is the ω² interaction + HIV-1 anchor)"으로 한정. |
| Ch4 (Results) | ch4:685 RF CV의 자체-caveat: "5-fold split is at the position level within each pathogen, so adjacent residues with correlated features can land in different folds. This makes the reported AUC prone to spatial-autocorrelation leakage" | RF CV AUC (0.742 mean)가 spatial leakage 의심. mechanism explanation으로 사용되지만 generalization estimate로는 부적절 | 본문이 정면 인정. RF CV는 "feature-complementarity illustration"으로만 한정 사용 → 적절. region/domain-blocked CV가 future work. C2/C5 핵심 주장이 RF CV AUC에 의존하지 않음(ω²과 ablation에 의존)이라 critical risk 아님. |
| Ch5 (Discussion) | ch5:84의 Rice algorithm-selection framework 매핑 | 전체 11 pathogen이 Rice의 problem space로 충분히 representative하다는 가정을 reviewer가 공격 가능 | ch5:84가 명시적으로 "unlike the theoretical NFL result, which applies to all possible problem distributions, the empirical finding here is grounded in a specific, biologically meaningful problem class (11 RNA viruses)" — 한정 표현 충실. |
| Ch5 (Discussion) | ch5:285 Bayesian hierarchical posterior 분석 (mean 0.252, HDI [0.188, 0.314]) | 11 cluster의 frequentist mixed-effects 불가 → Bayesian으로 우회. half-Cauchy prior 선택의 정당성 검토 필요 | ch5:285가 Bolker et al. 권장 random-factor levels 5-6+ 기준 인용으로 정당화. 단 prior sensitivity analysis 없음. 보강 = inverse-Gamma vs half-Cauchy prior comparison. |
| Ch6 (Conclusion) | ch6:14 "4-feature core retains 97.6% of the 10-feature EqualWeight ensemble mean MCC" | abstract와 conclusion에서 동일 표현이지만, ch4:802의 "no paired-sample significance test was performed"가 conclusion에는 누락 | "97.6% (numerical equivalence, no paired test)" 형태로 conclusion에서도 명시 |

---

## 4. 종합

### 변호 가능한 핵심 주장 (강한 것부터)
1. **C4 (HIV-1 7.19× vaccine escape, 82% Layer A-disjoint, p_adj=2.5e-16)**: 가장 강건. 본문이 three-tier evidence rule (Bonferroni × Layer A independence)을 명시 적용해 HIV-1을 primary anchor로 격상하고 H3N2/SARS-CoV-2를 self-consistency/exploratory로 강등. novel-only worst-case p=5.0e-12은 780배 보정 후에도 견고. 적대자가 흔드려면 Layer A definition 자체를 흔들어야 하고 그것은 시나리오 5에서 다층 sensitivity로 방어됨.
2. **C2 (ω²=0.296, CI [0.195, 0.333])**: 강건한 통계 주장. cluster bootstrap + Bayesian posterior 둘 다 Cohen large threshold (>0.14) 위. 단, "largest *modeled* component"라는 표현으로만 사용해야 하며 "largest source of variance"는 within-cell residual 0.39와 비교했을 때 불정확. 본문은 이미 정확히 한정 표현 사용.
3. **C1 (8,580 evaluations)**: 산술적 사실. design 문서화 충실. 단, "10 information types × 20 scoring formulas" 관계를 처음 보는 reader가 혼동할 수 있어 ch4:243-244의 "10 underlying biological features → 20 scoring variants" 명시가 핵심.
4. **C6 (9 distinct optimal types)**: 산술적 사실. footnote에 명시. 단 11/11 uniqueness가 P≈0.93으로 random에서 expected라는 점은 self-disclosed → 강한 증거가 아닌 descriptive observation으로 사용.
5. **C5 (4-feature core ≈ 98%)**: numerical equivalence (paired test 없음) 자체-인정 후 정직 사용. Tier 2 강도.
6. **C3 (LOPO 0/11 + Friedman p=0.990)**: **가장 약함**. 본문이 직접 "null-consistent under permutation"으로 corroboration 등급 강등. 단독 evidence 아닌 ω² + HIV-1 anchor와 세트로만 작동.

### 사용자가 즉시 보강해야 할 항목 (priority 순)
1. **abstract와 Ch6 conclusion에서 "0.265 oracle-vs-generalized gap" 표현에 caveat 추가**: ch4:443-446의 "p ≈ 0.25-0.28 vs random null" tempering이 이 두 곳에서 누락. abstract:10에는 "LOPO 0/11 alone is null-consistent under permutation" 표현이 있으나 0.265 gap 자체에 대한 한정은 없음.
2. **MAFFT --auto의 pathogen별 알고리즘 차이 robustness re-run**: 단일 모드(L-INS-i 또는 G-INS-i)로 강제한 supplementary ANOVA 결과를 1 paragraph로 보고. 시나리오에서 ω²의 input quality artifact 의심을 잠재울 가장 cost-effective 보강.
3. **DMS top-20% threshold sensitivity sweep을 6 pathogen 전부로 확장**: 현재 4 pathogen만. Rabies, EV-A71의 ranking stability 확인.
4. **HIV-1 vaccine escape에 entropy scoring (Layer A best) 결과를 supplementary로 보고**: 시나리오 2의 "두 best가 다르다" 공격 사전 차단. ρ=0.97 correlation은 이미 본문이지만 directly entropy-with-Wavelet escape enrichment 수치를 보여주면 closure.
5. **Layer A same-evidence-type subset (immune-escape-only) re-estimation**: 현재 ch4:842가 "10/12 pathogens retain same best feature when restricting" 정도로 stop. ω² subset estimation까지 가면 시나리오 5 완전 차단.

### 위험-거부 진술 (사용자가 외부에 공개적으로 진술 가능한 형태)
- "MutBench는 region-level hotspot-detection benchmark이며, per-variant fitness regression task의 ProteinGym/EVEREST/ViroGym과 직접 비교 불가."
- "ω²=0.296은 *modeled* term 중 최대이며, within-cell residual 0.39 (parameter-variant noise + unmodeled three-way)와 비등하다."
- "LOPO 0/11과 Friedman p=0.990은 단독으로 pathogen-dependence를 입증하지 않는다 (permutation null과 distinguishable하지 않음). Load-bearing 증거는 ω² + 9 distinct optimal types + HIV-1 7.19× anchor의 세트."
- "External validation은 HIV-1에 의해 carry되며 (82% Layer A-disjoint), H3N2/SARS-CoV-2의 enrichment는 self-consistency / exploratory로 강등."
- "11 pathogen은 Rice algorithm-selection space의 representative panel이 아니라 biologically-meaningful sample이며, 20-30+ pathogen으로 확장이 deployable adaptive selection의 prerequisite."
