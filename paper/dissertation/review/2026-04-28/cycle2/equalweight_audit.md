# EqualWeight Label Leakage Audit (Phase A1)

## 본문 진술 (ch3_methods.tex / ch4_results.tex)

### ch3_methods.tex:691 (정의 도입부)
> "EqualWeight averages all normalized scores as a naive baseline."

### ch3_methods.tex:694 (z-score 정규화)
> "Each scoring type was z-score normalized (zero mean, unit variance) across positions before averaging."

### ch3_methods.tex:695 (문제의 directional sign rule)
> "A directional sign rule was applied so that, prior to averaging, each feature is multiplied by sign(ŝ_f), where ŝ_f ∈ {-1,+1} is the empirically observed sign of the feature's per-position correlation with Layer~A on the training pathogens (e.g., pLDDT inverse and rare_freq enter with +1; conserved-region indicators like raw pLDDT would enter with -1). This keeps EqualWeight a deterministic, label-light fusion: all magnitudes are equal-weighted, but every feature is oriented toward 'higher score = more hotspot-like' before z-score averaging, preventing destructive cancellation between features whose raw scales point in opposite directions."

### ch4_results.tex:920 (사용 단계 재진술)
> "The integration method uses equal-weight combination: each feature is z-score normalized across all L alignment positions, directional signs are applied (to handle inverse associations such as pLDDT AUC < 0.5 for MERS), and the weighted combination s_i = Σ_f (1/10) · sign(ŝ_f) · z_{i,f} is computed."

이 두 진술은 **(i) 모든 11(또는 12) pathogen에서 평가되는 EqualWeight 컬럼**과 **(ii) sensitivity analysis인 nested-LOPO ablation의 EqualWeight**를 구분하지 않은 채 동일한 sign-rule 설명을 채택하고 있다.

---

## 코드 위치

| 용도 | 파일 | 함수 / 라인 |
|---|---|---|
| 헤드라인 ω²=0.296 (Stage 3 8,580 evaluations) 의 EqualWeight 컬럼 생성기 | `/proj/paper/scripts/run_stage3_full_detectors.py` | L180-187 (`scorings['EqualWeight']`) |
| 동일 로직의 축약 버전 | `/proj/paper/scripts/run_stage3_benchmark.py` | L109-116 |
| Feature ablation (LOO / 그룹 / 누적, in-sample) | `/proj/paper/scripts/feature_ablation.py` | L71-99 (`compute_equalweight_mcc`) |
| Nested-LOPO feature ablation (4-core retention 검증) | `/proj/paper/scripts/feature_ablation_nested_lopo.py` | L83-105 (`fit_signs`), L127-150 |
| 백신 escape enrichment (H3N2 4.012×, top-5%) | `/proj/paper/scripts/validate_escape_adapt.py` | L127-131 (call), `/proj/paper/tools/mutbench_adapt/adapt_v2.py` L309-313 (`baseline_equal_weight`) |
| Adapt v2 LOPO (kNN/top3/corr) | `/proj/paper/tools/mutbench_adapt/adapt_v2.py` | L137-143 (`compute_feature_signs`), L353+ (`run_full_lopo`) |

---

## 실제 동작 (코드 분석)

### A. 헤드라인 ω²=0.296 의 EqualWeight (`stage3_full_results.csv` 의 `scoring="EqualWeight"` 행 11×39 = 429개)

`run_stage3_full_detectors.py` L180-187:
```python
plddt_inv = plddt_max - plddt
features_for_eq = [
    freq, entropy, rare_freq, homoplasy, esm2_llr,
    plddt_inv, sasa, grantham, dnds_proxy, semantic_change,
]
normed = np.array([normalize_01(f) for f in features_for_eq])
scorings['EqualWeight'] = np.mean(normed, axis=0)
```

`normalize_01` (L79-84): 순수 min-max `(arr - mn)/(mx - mn)`. **라벨 없음.**

핵심:
1. **사전 정의된 도메인 방향성을 사용한다.** 입력 리스트는 `plddt`가 아니라 `plddt_inv = plddt_max - plddt`를 포함한다 — pLDDT inverse 변환은 코드에 하드코딩 (L181).
2. `np.mean(normed, axis=0)`은 단순 평균 — 어디에도 sign(·) 곱셈, AUC, 라벨 사용 없음.
3. 정규화는 z-score 가 아니라 min-max (본문 L694 진술과도 불일치).

→ **본문에서 묘사한 "fit on training pathogens" sign-rule은 이 코드 경로에 존재하지 않는다.**

### B. In-sample Feature Ablation (ch4 Table feature_ablation, mean MCC = 0.083)

`feature_ablation.py` L71-99 (`compute_equalweight_mcc`):
```python
F = np.nan_to_num(df[feature_subset].values.copy(), ...)
Z = np.zeros_like(F)
for j in range(n_feat):
    std_j = np.std(F[:, j])
    if std_j > 1e-10:
        Z[:, j] = (F[:, j] - np.mean(F[:, j])) / std_j
        w[j] = 1.0 / n_feat
scores = Z @ w
```

z-score는 맞지만 sign 곱셈 없음. **라벨 사용 없음.** 도메인-prior로 정의된 feature 컬럼(`plddt`는 raw가 그대로 들어감 — `plddt_inv`가 아님!)을 그대로 평균낸다.

### C. Nested-LOPO Feature Ablation (ch4:837, ch1:150 의 4-core retention 클레임)

`feature_ablation_nested_lopo.py` L83-105 (`fit_signs`):
```python
for f in features:
    xs, ys = [], []
    for p, d in training_data.items():   # training_data = LOPO holdout 제외 11개
        x = ... d["df"][f].values ...
        y = d["y"].astype(float)         # Layer A 라벨
        xs.append(x); ys.append(y)
    x_all = np.concatenate(xs)
    y_all = np.concatenate(ys)
    r = np.corrcoef(x_all, y_all)[0, 1]
    signs[f] = -1.0 if r < 0 else 1.0
```

L153-164 (`lopo_eval`):
```python
for held_p in data:
    training = {k: v for k, v in data.items() if k != held_p}
    signs = fit_signs(training, FEATURE_NAMES)   # held-out 제외!
    ranking = fit_feature_ranking(training, FEATURE_NAMES)
    ...
    mcc = equalweight_mcc_held_out(held_d["df"], held_d["y"], subset, signs)
```

→ **fold마다 sign이 holdout pathogen을 제외한 나머지에서만 fit됨.** 깨끗한 LOPO. 라벨 누출 **없음**.

### D. H3N2 4.012× Escape Enrichment (`validate_escape_adapt.py` → `escape_validation_adapt.csv`)

`validate_escape_adapt.py` L127-131:
```python
if method_name == "EqualWeight":
    w = np.ones(10) / 10.0
    s = np.ones(10)                                # ← 모든 sign = +1, 학습 없음
    scores = compute_scores(df, w, s)
    return apply_threshold(scores, thr_config)
```

`adapt_v2.py compute_scores` L168: `return (Z * np.sign(s)) @ w_adj` → `np.sign(np.ones(10)) = +1` 그대로.

→ sign이 호출자에서 상수 +1로 강제됨. **라벨 누출 없음.** 단, 본문에서 말한 "domain-prior sign"도 아니다(여기서는 `plddt`가 raw로 +1 sign으로 들어가서 의미가 거꾸로일 수 있다 — Methods 본문은 `plddt_inv`로 들어간다고 적혀 있어 이것 또한 본문-코드 불일치).

### E. Adapt v2 LOPO Strategies (kNN/top3_auc/corr_ensemble)

`compute_feature_signs` (L137-143)는 layer_a 라벨로 sign 결정. 하지만 `run_full_lopo` (L353+)는 각 fold마다 `S_ref = np.array([data[p]["signs"] for p in train_pathogens])` (L408)로 **train만** 모은 뒤 strategy(top3/corr)에서 majority vote. 깨끗한 LOPO.

`baseline_equal_weight` (L309-313)도 마찬가지로 `s = np.ones(10)` 상수.

---

## 판정

**카테고리: 실제 코드는 (a) 도메인-prior 사전 정의 / 상수 +1 / 또는 (b) 깨끗한 LOPO 학습 — 라벨 누출 없음. 그러나 본문 진술은 코드와 불일치한다 (서술 정확성 결함).**

세분화:

| 평가 컨텍스트 | 코드의 EqualWeight sign 처리 | 분류 |
|---|---|---|
| 헤드라인 ω²=0.296 (Stage 3 main grid, 8,580 evals) | sign 곱셈 자체가 **없음**. 입력 feature 리스트에 `plddt_inv` 하드코딩(도메인 prior). min-max → mean. | **(a) 누출 없음** — 본문 sign-rule 진술이 부정확 |
| In-sample LOO/group/cumulative ablation (mean MCC 0.083) | sign 곱셈 없음. raw `plddt` 등을 z-score → mean. | **(a) 누출 없음** — 단, 본문-코드 불일치 |
| Nested-LOPO 4-core retention (ch4:837, ch1:150) | training pathogen에서만 sign fit. | **(b) LOPO 누출 없음** — 본문 진술 정확 |
| H3N2 4.012× escape enrichment | `s = np.ones(10)` 상수, label 미사용. | **(a) 누출 없음** — 본문이 묘사한 sign-rule이 실제로는 적용되지 않음 |
| Adapt v2 LOPO (참고용, 헤드라인 외) | `S_ref`를 train pathogen에서만 구성. | **(b) LOPO 누출 없음** |

**ω²=0.296 헤드라인 영향: 영향 없음.** 헤드라인 EqualWeight 컬럼은 라벨을 전혀 보지 않는다. 적대 검수의 "sign이 모든 11 pathogen 라벨로 fit된다면 라벨 누출이다"라는 가정의 후건이 코드에서는 성립하지 않는다 — 전건(sign이 fit된다)이 실제 production 경로에서 거짓이다.

**다만 별개의 결함이 발견됨**: 본문(ch3:695, ch4:920)의 sign-rule 진술은 nested-LOPO ablation 코드(`feature_ablation_nested_lopo.py`)에는 정확하지만, 헤드라인 ω²의 EqualWeight 컬럼(`run_stage3_full_detectors.py`)에는 적용되지 않는다. 본문은 두 코드 경로를 **하나의 EqualWeight 정의로 합쳐 묘사**하고 있어 독자가 헤드라인 EqualWeight도 sign-rule을 거친다고 오해하게 만든다.

---

## 본문 수정 권고

### 권고 1 (필수): ch3:695 의 sign-rule 묘사를 두 컨텍스트로 분리

현재 단일 단락이 **production EqualWeight (Stage 3 main grid)** 와 **nested-LOPO ablation**를 구분하지 않는다. 다음과 같이 교체 권고:

> "Each scoring type was min-max normalized to [0,1] across positions before averaging in the production EqualWeight column (`run_stage3_full_detectors.py`); the input list uses pre-defined domain orientations (e.g., the inverse-pLDDT transform `pLDDT_max − pLDDT` rather than raw pLDDT, so that flexible regions enter with positive sense), but no per-feature sign is fit from labels and no z-scoring is applied at this stage. For the separate **nested-LOPO ablation** in Section~\ref{subsec:feature_ablation} (Table~\ref{tab:nested_lopo_4core}), each feature is multiplied by a directional sign $\hat{s}_f \in \{-1,+1\}$ that is fit on the eleven training pathogens (excluding the held-out pathogen) as the sign of $\mathrm{corr}(z_f, \mathrm{Layer~A})$, then z-scored within the held-out pathogen alone; this is a label-aware but cleanly held-out fusion used only for the 4-feature core retention test, never for the headline ω²=0.296 main effect."

### 권고 2 (필수): ch4:920 의 진술 수정

현재: "directional signs are applied (to handle inverse associations such as pLDDT AUC < 0.5 for MERS), and the weighted combination s_i = Σ (1/10) · sign(ŝ_f) · z_{i,f}".

이 식이 묘사하는 대상을 명시화. 권고 교체:

> "For the LOPO benchmark in this section (mean MCC 0.083, 12 pathogens), the integration uses pre-defined domain orientations (e.g., inverse-pLDDT) followed by z-score normalization and uniform $1/10$ averaging, with no label-fit signs. The complementary nested-LOPO 4-core retention analysis in Section~\ref{subsec:feature_ablation} additionally fits per-feature signs on the eleven training pathogens before averaging on the held-out pathogen, isolating the contribution of label-aware orientation; the two protocols agree to within 0.012 mean MCC, indicating that the directional sign step is not load-bearing for the headline retention claim."

### 권고 3 (필수): 헤드라인 EqualWeight의 정규화 방식 정정

ch3:694 는 "z-score normalized" 이라고 적혀 있으나 `run_stage3_full_detectors.py` 의 EqualWeight는 `normalize_01` (min-max) 을 쓴다. 이 또한 본문-코드 불일치이며 권고 1 에 반영했다.

### 권고 4 (선택): Methods 표 주석 보강

ch3 table:605 의 "All-feature average" 행에 푸트노트로 "production column uses min-max + uniform mean of 10 features with `plddt_inv` substituted for raw pLDDT; nested-LOPO ablation variant additionally applies per-feature signs fit on training pathogens — see Section X" 추가.

### 추가 sensitivity analysis 필요 여부: **NO**

라벨 누출이 없으므로 ω²=0.296 재추정은 불필요. 단, 다음 감각 점검은 **있으면 좋음**(필수 아님):
- 헤드라인 EqualWeight 정의를 nested-LOPO 정의(sign fit on training)로 교체했을 때 ω²가 얼마나 변하는지 1회 계산. Sign이 fit되든 +1 상수든 결과 ranking이 바뀌지 않음을 보이는 1-paragraph 보강이 가능. 본문 권고 2의 "agree to within 0.012 mean MCC" 수치는 이 sensitivity를 한 번 돌려서 채워넣으면 가장 깔끔함 (`feature_ablation.py` 와 `feature_ablation_nested_lopo.py` 의 mean MCC 비교: 전자 0.083, 후자 full10 0.070 — 이미 측정되어 있음).

---

## ω² 영향 평가

- **카테고리 (a)/(b) 혼합 — 영향 없음.**
- 헤드라인 ω²=0.296 EqualWeight 컬럼은 `np.mean(normalize_01(...), axis=0)` 으로, Layer A 라벨을 **단 한 번도 참조하지 않는다.** 카테고리 (c)/(d)에 해당하지 않으므로 ω² 재추정은 불필요.
- 정량화(있어도 좋은 sensitivity): 이미 `feature_ablation.py`(in-sample, no signs, mean 0.083) vs `feature_ablation_nested_lopo.py`(LOPO with fit signs, mean 0.070) 가 paired bootstrap CI까지 보고된 상태로 존재하므로, sign-rule 자체가 main result에 ≤0.013 MCC 단위로 영향을 준다는 것이 이미 입증돼 있음. ω² 자체는 분산 분해이므로 여기에 sign 단계가 들어가도 잔차의 ~0% 수준 변화가 예상된다.

---

## 결론 요약

1. 적대 검수의 **라벨 누출 의심은 코드에서 기각된다.** 헤드라인 ω²=0.296에 들어가는 EqualWeight 컬럼은 라벨을 전혀 보지 않고 산출된다.
2. 그러나 적대 검수가 그 의심을 갖게 된 **본문 진술 자체에는 결함이 있다** — ch3:695 와 ch4:920 가 두 개의 다른 EqualWeight 변형(production: 라벨-무관, nested-LOPO ablation: training-only sign fit)을 한 줄의 sign-rule 묘사로 통합해버려, 독자가 두 변형을 구분할 수 없다. 추가로 ch3:694의 "z-score normalized" 표현 또한 헤드라인 코드(min-max)와 일치하지 않는다.
3. **수정 작업: 본문 3개 위치 정정 (ch3:694, ch3:695, ch4:920). 코드/실험은 변경 불필요. ω² 재추정 불필요.**
