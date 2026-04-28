# 통계 전문가 검증 (Phase 2 통계)

**리뷰어 역할**: 독립 통계 전문가 (블루팀/레드팀 산출물 미열람)
**대상**: `ch3_methods.tex` (Section 3.2.5 평가/통계), `ch4_results.tex` (ANOVA, Friedman, LOPO, enrichment), `front_en/abstract.tex`
**Phase 0 결과**: 84/84 PASS — 수치 일관성은 통과
**판정 기준**: PASS / WARN / FAIL + 파일:라인 근거

---

## 항목별 판정 표

| # | 항목 | 판정 | 근거 (파일:라인) | 위험 요인 | 보강 권고 |
|---|------|------|-----------------|----------|----------|
| 1 | ω²=0.296 해석 (20-type, 6-cat, 잔차, CI) | **PASS** | abstract:10; ch4:368, 386, 390, 394, 396, 489, 563; ch5:281, 310 | "modeled" 한정 표현 충실 — 독립 검증 시 잔차 ω²≈0.39 명시 위치가 분산되어 있음 | 표 4.1 캡션에서 modeled vs total 구분 1줄로 통일 가능하나 현재로도 합격 |
| 2 | ANOVA 가정 검정 (Shapiro, Levene, skew/kurt, N) | **PASS** | ch4:485-486 (Shapiro W=0.974 p<10⁻²⁹, skew=0.14, kurtosis=2.83, N=8,580); ch3:823 (Levene); ch4:486-491 (effective-N) | Shapiro 거부 + Levene 거부, 그러나 N=8,580로 robust 주장 + ART 보조 (ch3:825) + Kruskal-Wallis (ch4:491) — 적절 | 합격 |
| 3 | Friedman χ²=7.69, p=0.990 해석 | **PASS** (제한된) | ch4:434, 437-440 (W=0.037, two interpretations); ch3:842-846 (방법); ch5:319 | 검정력 없음 (n=11 blocks × k=20)에 명시. 두 해석 (universal poor vs pathogen-dependent) 병기. p=0.990을 "no universally best"의 직접 증거로는 쓰지 않고 LOPO/oracle gap으로 disambiguate (ch4:440). 정직 | 정직성 합격. (소견: Friedman 검정 통계량의 식 정의(χ² = n(k-1)W)와 일관된지 확인 — n=11, k=20 시 W=0.037 → χ²=11×19×0.037=7.74 ≈ 7.69, 일치) |
| 4 | LOPO 0/11 + 0.265 gap + permutation null | **PASS** (정직성 우수) | ch4:411-415 (P(matches=0)≈0.96 in table); ch4:442-446 (10,000 resamples; 0.265 gap p≈0.25-0.28); ch4:565 ("null-consistent corroboration"); ch1:148; ch5:319-321; ch6:13; abstract:10 | LOPO 0/11이 random null과 구별 불가 — **본문에 명시적 자수**. 0.265 gap도 p≈0.25-0.28로 약함 명시. "corroboration not independent evidence" 표현 일관 | 정직 자기 비판 — 합격. 단, Table tab:lopo_summary에 "P(matches=0)≈0.96"이 행으로 들어가 있어 표만 봐도 명확함은 우수 |
| 5 | HIV-1 7.19× / Bonferroni p=2.5e-16 | **PASS** | ch4:874 (table 7.19×, 23/45); ch4:886 (footnote: Bonferroni 780 combinations, p_adj=2.47e-16); ch4:891 (전체 해석); ch4:921 (circularity audit: 37/45 = 82% Layer-A-disjoint); abstract:11; ch5:161 | Bonferroni 분모=780 명시 (per-pathogen family). 분모 정당성: ch3:826 ("per-pathogen family used in Chapter 4 is 20×39=780") — 명시. Novel-only 7.16-8.24× sensitivity range는 disjoint 37 positions에 대한 것 — ch4:886, ch4:921 일관. | 합격. 분모를 8,580 (cross-pathogen)로 잡아도 tier 변화 없음 명시 (ch4:886) — 견고 |
| 6 | 다중 비교 보정 일관성 | **PASS (조건부)** | ch4:886 (footnote: H3N2 p_adj=2.63e-5, HIV-1 p_adj=2.47e-16, SARS-CoV-2 p_adj→1.00); ch5:161 | H3N2 9.36× Bonferroni-survives 명시. SARS-CoV-2 7.63× **소실** 명시 ("exploratory only"). H3N2 4.012×/EqualWeight p=0.0023은 단일 검정 (top-5% 통합)이라 Bonferroni 적용 안 됨 — 검정 family가 다름. 정당화 가능하나 **명시적 family 정의는 부분적**. ch3:826에서 일반 정책 명시되어 있으나 EqualWeight 검정의 family 크기는 서술 없음 | (조건부) EqualWeight 통합 검정의 family 명시 권고: "EqualWeight-vs-FreqThresh-vs-BestSingle" 3-method 비교라면 Bonferroni 분모 3 — 그렇다면 0.0023×3=0.0069 여전히 유의. 1줄 추가하면 완전. 현재로도 PASS |
| 7 | 샘플 크기 명시 | **PASS** | N=8,580 4회 명시 (ch3:560, ch4:886, ch4:970, ch5:240); 2,340 vaccine-escape 1회 (ch4:857); n=11 pathogens, n=6 DMS, n=3 escape annotated, n=12 (Stage 3 + Zika) 모두 caption/본문 | Stage별, 분석별 부분집합 크기 일관 | 합격. ch3:821, ch4:487-488은 effective-N (3,080 unique cells) 추가 보고 — 우수 |
| 8 | Effect size + p-value 동반 | **PASS** | ANOVA: ω² + Cohen tier (ch4:368-374); enrichment: ratio + p-value + Bonferroni (ch4:874-886); LOPO: gap=0.265 + permutation p (ch4:444-445); Friedman: χ² + W (ch4:434, 437); Kruskal-Wallis (ch3:825); Spearman (ch4:226, 481, 529, 553) | Spearman 결과는 ρ + p 모두 동반. p-value 단독 보고 사례 발견되지 않음 | 합격 — 모든 검정에 effect size + p 동반 |
| 9 | 회로성 자기 점검 (Layer A vs freq) | **PASS (조건부)** | ch4:696 (HIV-1 entropy↔freq ρ=0.97); ch4:739 (freq--entropy ρ=0.97); ch4:891 (freq vs entropy ρ≈0.97); ch5:33 (per-pathogen point-biserial mean \|ρ\|=0.12, range [-0.06,+0.33], 명시적 audit); ch5:35 (Layer C as freq-independent dim); ch4:543-553 (Layer A vs Layer C divergence table+분석) | **메모(Memory)에 적힌 "ρ=0.973"는 본문에 정확히 0.973 형태로는 없음**. 본문은 "ρ=0.97" (rounded) — 수치적으로는 동일 사실 (entropy↔freq 상관). Layer A 자체와 freq의 직접 상관은 ch5:33의 point-biserial \|ρ\|=0.12 (Layer A membership vs freq score) — 별개 measure, 회로성 audit으로 적절. **혼동 위험**: "Layer A vs freq ρ=0.973" 문구가 본문에 단일 출처로 통합되어 있지 않음 | (1) ch5:33의 0.12 (Layer A membership↔freq score per-position)와 ch4:696의 0.97 (entropy↔freq feature correlation)은 서로 다른 양 — 독자 혼동 가능. 1줄 명시 권고 ("이 두 ρ는 다른 것: 전자=membership↔score, 후자=feature↔feature"). 현재 PASS이나 보강 시 더 명확 |
| 10 | 재현성 통계 (seed, split, bootstrap, code/data) | **PASS** | ch3:902-904 (seed=42, NumPy 1.24 SciPy 1.11 IQ-TREE 2 HyPhy 2.5 ESM-2 esm2_t33_650M_UR50D 모두 pin); ch3:850-851 (BCa 10,000 resamples; cluster 1,000 resamples); ch4:443 (permutation 10,000 resamples); ch4:175-176 (region BCa 1,000); ch4:466 (subsampling 25/50/75/100%); ch4:174 (permutation 1,000 random + 200 circular); ch5:287 (independent reproduction 명시적 미진행 — Priority 5) | 모든 randomized 분석에 seed=42 + 반복 수 명시. Code/data Zenodo DOI 약속 (ch3:903). | 합격. 외부 독립 재현은 미수행 명시 — 정직 (ch5:287) |

---

## FAIL/WARN 상세

**FAIL: 0건**
**WARN: 0건**
**조건부 PASS: 2건** (#6, #9 — 명시적 1-2줄 보강 권고이나 합격선은 통과)

전 항목 PASS. 통계적 자기 비판 (LOPO null, winner's curse, ANCOVA, partial pooling, ART, Kruskal-Wallis, cluster bootstrap, wild-cluster bootstrap caveat 등) 다수 본문에 명시되어 정직성 매우 우수.

---

## 핵심 결론 통계 신뢰도

### C2 (ω²=0.296): **높음**
**이유**:
1. 11-pathogen cluster-bootstrap CI [0.195, 0.333] 보고 (ch4:488-489), 하한도 Cohen's large 임계 (0.14)를 크게 상회
2. 6-category aggregation collinearity-robust lower bound ω²=0.103 보고 (ch5:281, ch4:396) — "largest" 표현이 20-type 모델 한정 명시
3. Within-cell residual ω²≈0.39 명시 (ch4:361 caption, ch4:386 caption, ch4:390 본문) — 잔차가 모형보다 크다는 사실 자수
4. ART 비모수 ω²=0.277 (ch3:825), Bayesian partial-pooling 0.252 95% HDI [0.188, 0.314] (ch5:285) — 다중 lens consistency
5. ANCOVA (length, positive rate 보정) 후 0.234→0.264 (ch5:290) — 견고
6. Kruskal-Wallis H=277.9 p<10⁻⁴⁷ (ch3:825) — 비모수 안전망
7. **유일 약점**: 11 클러스터는 percentile-bootstrap rule-of-thumb 30 미달 (ch4:489) — 본문에서 wild-cluster bootstrap 권고 명시. 안전망 충분

### C3 (LOPO 0/11): **중간** (정직성으로 표현된 약함)
**이유**:
1. 0/11 자체는 random null 하 P(matches=0)≈0.96으로 **유의하지 않음** (ch4:415, 444) — 본문에 정면 명시
2. Mean generalized MCC=0.032 vs random null mean=+0.017 (SD 0.027-0.034)으로 0.4-0.6 SD 차이, one-sided p≈0.25-0.28 (ch4:445) — **null과 구별 불가**
3. 0.265 oracle-vs-generalized gap도 통계적 유의 미달 명시
4. Conclusion: "null-consistent corroboration", "not independent evidence" (ch1:148, ch4:565, ch6:13) — 표현 정직
5. **이는 약점이 아니라 정직성의 강점**: LOPO만으로는 약함을 인정하고 ω² + HIV-1 anchor에 부담을 떠넘김

판정: 통계 자체는 약하지만 **표현은 정확하므로 정직성 차원에서 PASS**. 위험은 독자가 "0/11 = 강한 증거"로 오독할 가능성이지만 본문 다수 위치에서 차단됨.

### C4 (HIV-1 7.19×): **높음**
**이유**:
1. Bonferroni 분모=780 명시, p_adj=2.47×10⁻¹⁶ — 매우 강한 유의
2. Novel-only audit: 37/45 (82%) Layer-A-disjoint, 7.16-8.24× sensitivity range (ch4:886, ch4:921) — 회로성 차단
3. Worst-case Fisher p=5×10⁻¹² novel-only (ch4:886) — Layer A 의존성 제거 후에도 강한 유의
4. Top-1 winner's curse 인정, Bonferroni-survivor mean ≈4-5× 보고 (ch4:886, ch5:283)
5. **약점**: 단일 pathogen anchor — H3N2 (69% overlap), SARS-CoV-2 (Bonferroni 소실)는 self-consistency/exploratory로 명시 강등
6. Fisher exact test 적용 정당: 2×2 테이블, 경계값 정의 명시 (ch4:858-861)

**일반화 한계**: 11 중 3개 pathogens만 escape 검증, 나머지 8개 별도 audit table (tab:escape_availability, ch4:903-916)으로 사유 명시 — 데이터 가용성 사유 — 표현 정직.

---

## 안돈 트리거 항목

### ω² 해석 FAIL: **없음**
- "Largest modeled variance component" 표현 정확 (모형 안에서만)
- 잔차 ω²≈0.39 자수 (ch4:361, 386, 390)
- 6-cat lower bound 0.103 + 20-type upper bound 0.296 양방 명시
- CI [0.195, 0.333] cluster-bootstrap 산출 정당 (1,000 resamples, ch3:851, ch4:488)

### Critical 통계 결함: **없음**
다음과 같은 자기 비판이 본문에 이미 포함되어 있어 안돈 사유 부재:
- LOPO 0/11 = null-consistent (ch4:444)
- Winner's curse + 4.7× Bonferroni-survivor mean (ch5:283)
- 11-cluster bootstrap rule-of-thumb 미달 (ch4:489)
- HIV-1 anchor의 단일 pathogen 한계 명시 (ch4:918)
- Layer A 정의 표류 (curation-protocol heterogeneity, ch4:490, ch5:33)
- Bayesian partial-pooling 0.252 (ch5:285) — shrinkage 후에도 above-threshold

---

## 가장 위험한 항목 1건 (TOP RISK)

**#9 회로성 자기 점검 — 두 ρ 값의 명목적 혼동 가능성**

**상세**:
- 본문에 두 종류의 상관 ρ가 등장:
  - **(A) Per-position feature correlation**: entropy ↔ freq ρ=0.97 (ch4:696, ch4:739, ch4:891)
  - **(B) Per-position point-biserial**: Layer A membership ↔ freq score ρ mean |0.12|, range [-0.06, +0.33] (ch5:33)
- (A)는 "two features encode similar info"이고 (B)는 "frequency 점수가 Layer A를 직접 예측하는 정도" — **수학적으로 다른 양**
- 메모리에 등재된 "Layer A vs freq Spearman ρ=0.973"는 (A)의 entropy↔freq를 가리키는 것으로 추정되나, "Layer A vs freq" 단어는 (B)와 매칭되어 보일 수 있음
- 회로성 주장의 강도가 (A) 0.97인지 (B) 0.12인지에 따라 결론이 크게 달라짐

**위험도**: 중간 (현재로도 PASS이나 독자/심사관 혼동 가능)
**권고 보강**: ch5:33 또는 ch4:891 부근에 1-2줄 추가
> "주: 본 논문에서 보고하는 두 ρ는 다른 양이다 — entropy↔freq feature 상관 ρ=0.97 (각 score가 비슷한 정보를 인코딩함을 의미)와 Layer A membership↔freq score point-biserial mean |ρ|=0.12 (frequency 점수가 Layer A를 직접 예측하는 강도)는 별도. 회로성의 직접 지표는 후자이다."

이 보강 없이도 통계 표현은 정확하지만, 명시적 disambiguation이 있으면 심사 단계에서의 오독 위험을 차단할 수 있음.

---

## 종합 평가

| 항목 | PASS | WARN | FAIL |
|------|------|------|------|
| 카운트 | 10 | 0 | 0 |

**총합**: 10/10 PASS, **안돈 트리거 없음**

**통계적 정직성 평가**: **상위권**.
- LOPO null-consistency, winner's curse, cluster bootstrap caveat, ART, Kruskal-Wallis, ANCOVA, Bayesian partial pooling — 모두 본문에 자수
- "Largest modeled" 한정 표현, "null-consistent corroboration" 표현 일관
- HIV-1 anchor의 단일성 인정, 8 pathogens audit table로 미수행 사유 명시

**최우선 보강 권고 (Optional, 합격선 통과 후 가독성 개선)**:
1. (#9) 두 ρ 값 명시적 disambiguation 1-2줄 (ch5:33 또는 ch4:891)
2. (#6) EqualWeight 통합 검정의 family 정의 1줄 (ch4:878 근처)

이 두 보강은 모두 1-2줄 추가만으로 가능하며 본질적 통계 결함은 없음.

---

**Reviewer note**: 본 검증은 블루팀/레드팀 산출물을 열람하지 않고 독립적으로 수행되었으며, 인용된 모든 라인은 직접 파일을 읽어 확인되었다. 84/84 PASS Phase 0 검증 결과와 본 검증 결과가 일관되어 통계 영역에서는 안돈 사유 없음.
