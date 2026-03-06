# MutClust 심층 분석: 문제점 및 v2 개선 방향

> 컴퓨팅 및 생물학 관점에서의 종합 분석 보고서

---

## 1. 알고리즘 설계 문제

### 1.1 적응형 Epsilon (Deps)의 순환 의존성

`Deps = ceil(gamma * H_i)` 공식에서 H-score가 높은 위치는 넓은 이웃 반경을 할당받아 CCM 조건을 충족하기 쉬워지고, H-score가 낮은 위치는 좁은 반경으로 CCM이 될 수 없다. **부익부 빈익빈(Matthew effect)** 구조로, 중간 밀도 영역의 핫스팟을 체계적으로 놓칠 수 있다.

예: H=0.02인 위치 → Deps=1 (자기 자신+양쪽 1개), H=5인 위치 → Deps=50 (양쪽 50bp 탐색)

### 1.2 HDBSCAN/OPTICS 대비 이론적 열위

현대 밀도 기반 클러스터링의 표준인 HDBSCAN은 epsilon 자동 선택이 가능하고, OPTICS는 계층적 클러스터링으로 다양한 밀도 수준에서 클러스터를 추출한다. MutClust는 이론적 수렴 보장이나 최적성 증명이 없는 독자적 수식에 의존한다.

### 1.3 1차원 제약 (핵심 한계)

게놈 위치의 1D 선형 거리만 사용하여 **3D 단백질 구조에서의 공간적 근접성을 완전히 무시**한다.

- HotMAPS (Tokheim et al., Cancer Research 2016)는 3D 구조에서 1D로는 발견 불가능한 **30개 추가 핫스팟**을 식별
- RBD에서 떨어진 위치의 변이가 3D 공간에서 RBD와 근접하여 알로스테릭 영향을 줄 수 있으나, MutClust는 이를 포착 불가

---

## 2. 파라미터 문제

### 2.1 고정 Gamma의 민감도

Gamma=10은 SARS-CoV-2(~30kb)에서 경험적으로 결정되었으나:

- gamma=8이나 gamma=12에서의 결과 변화에 대한 체계적 분석 부재
- 인플루엔자(~2.3kb)에 동일 파라미터 사용 시 상대적으로 매우 넓은 탐색 범위 할당
- 논문 자체도 "adaptive parameter selection 모듈 개발"을 향후 연구로 인정

### 2.2 CCM 임계값의 하드코딩

| 파라미터 | 값 | 문제 |
|---------|-----|------|
| HSCORE_MIN | 0.03 | 서열 수에 따라 H-score 분포 변화 |
| MEAN_MIN | 0.01 | 통계적 근거 불명확 |
| SUM_MIN | 0.05 | 선택 기준 미설명 |
| MinPts | 5 | 게놈 크기에 독립적 |

224,318개 서열에 최적화된 값이므로, 서열 수가 1,000개 또는 1,000,000개이면 부적절해진다.

---

## 3. H-score 수학적 문제

### 3.1 공식: `H_i = log2(P_i * |E_i| * 100 + 1)`

**(a) 고빈도 단일 변이의 무시**

P_i = 1 (모든 서열에 변이)이고 변이 종류가 1개이면 E_i = 0 → H_i = 0. **빈도가 최대임에도 H-score가 0**이 되어 D614G 같은 고정된 변이를 완전히 무시한다.

**(b) 매직 넘버 100**

스케일링 상수 100은 순위에 영향 없지만 CCM 임계값과 결합 시스템을 형성. {100, 0.03, 0.01, 0.05}라는 4차원 결합 공간의 최적성이 미검증.

**(c) Shannon 추정량의 편향**

소규모 표본에서 Shannon entropy 추정은 편향이 크며, Chao et al.의 비편향 추정량이 더 우수한 것으로 보고됨.

---

## 4. 통계적 타당성 문제

### 4.1 Bootstrap 검정의 순환성

핫스팟을 "변이 밀도가 높은 영역"으로 정의한 후, bootstrap에서 "변이 밀도가 높은지" 재검정. **순환적 구조(circular testing)**로, 독립적 외부 검증이 아니다.

### 4.2 복합 통계량의 과도한 보수성

```python
if rand_count >= obs_count and rand_mean >= obs_mean and rand_sum >= obs_sum:
```

3가지 통계량의 AND 조건은 statistical power를 심각하게 저하. 개별 p=0.05일 때 결합 p ≈ 0.000125.

### 4.3 P-value 해상도

1,000회 반복에서 최소 비영 p-value = 0.001. 477개 핫스팟에 BH 보정 시 adj_p = 0.001 × 477 = 0.477로, p=0인 경우만 유의하게 됨.

### 4.4 Contaminated Null

랜덤 영역 추출 시 핫스팟 자체가 추출될 수 있어, 귀무 분포에 대안 가설 데이터가 혼입.

---

## 5. 생물학적 한계

### 5.1 동의 변이(synonymous) vs 비동의 변이(non-synonymous) 미구분

H-score는 뉴클레오타이드 수준에서 계산하므로 아미노산 변경 여부를 구별하지 않음.

- SARS-CoV-2 S 유전자의 dN/dS = 2.191로 강한 양의 선택 확인 ([Spectrum, 2023](https://journals.asm.org/doi/10.1128/spectrum.02654-23))
- 동의 변이도 mRNA 접힘, 번역 효율에 영향 ([PMC 2022](https://pmc.ncbi.nlm.nih.gov/articles/PMC9561399/))

### 5.2 상위성(Epistasis) 미반영

각 게놈 위치를 **독립적으로** 평가. 그러나:

- Omicron의 출현은 **상위성이 핵심적 역할**을 한다는 것을 극적으로 보여줌: 개별 변이로는 적합도 낮지만 특정 조합에서만 높은 감염력/면역 회피
- Turbowicz et al. (Genome Biology 2024): 상호정보 기반으로 Spike 코돈 498-501 상위성을 **7개 샘플**만으로도 탐지 가능
- Rodriguez-Rivas et al. (PNAS 2022): DCA 기반 공변이 모델이 단순 보존도 프로필보다 변이 예측에 월등히 우수

### 5.3 샘플링 편향 미보정

- 지리적 편향: 영국의 집중 시퀀싱으로 Alpha 변이 빈도 과대 추정 ([Lemey et al., 2022](https://journals.plos.org/globalpublichealth/article?id=10.1371/journal.pgph.0000577))
- 시간적 편향: 2020~2022년 합산 시 특정 시기 우세 계통의 변이 과대 대표
- 설립자 효과: 변이 빈도 급증이 적응적 변화가 아닌 설립자 이벤트일 수 있음 ([Zeng et al., 2021](https://journals.plos.org/plosone/article?id=10.1371/journal.pone.0255169))

### 5.4 반복 변이 vs 공유 조상 미구분

D614G가 거의 모든 서열에서 관찰되지만, 독립적 양의 선택이 아니라 단일 설립자 이벤트의 결과일 수 있다. **계통수 정보 없이는 변이의 진화적 독립성을 평가할 수 없다.**

### 5.5 임상 연관성의 인과 추론 한계

- 핫스팟-중증도 연관은 ANOVA 상관관계일 뿐, 인과관계 입증 미완
- 387명 코호트에서 22개 계통 혼재로 계통 효과/변이 효과 교란(confounding)
- DEG 분석은 바이러스 변이의 직접 효과가 아닌 숙주 면역 반응 차이일 수 있음

---

## 6. 구현 수준 문제

### 6.1 `_expand_cluster` 감쇠 공식 잠재적 버그

```python
current_deps = current_deps - (deps_ccm - distance) / d
```

`deps_ccm - distance`가 음수가 되면 (distance > deps_ccm), `current_deps`가 **증가**하여 감쇠 의도와 반대 동작. CCM에서 멀어질수록 반경이 다시 넓어지는 비직관적 동작을 유발할 수 있다.

### 6.2 H-score 계산의 비벡터화

이중 Python 루프로 224,318 서열 × 29,903 위치 = ~67억 회 사전 검색. numpy 벡터화로 수백 배 개선 가능.

### 6.3 Bootstrap 병렬화 미적용

477 × 1,000 = 477,000회의 독립적 랜덤 샘플링이 순차 실행. `multiprocessing`/`joblib`으로 CPU 코어 수에 비례한 속도 개선 가능.

### 6.4 Network Propagation의 Dense 행렬

`np.zeros((n, n))` 사용으로, n=20,000이면 ~3.2GB 메모리 소비. `scipy.sparse` 사용 시 수십 배 절약 가능.

### 6.5 재현성 미보장

Bootstrap에 `np.random.seed()` 미설정으로 동일 입력에서 다른 결과 가능.

---

## 7. 최신 경쟁 방법론 (2023-2026)

### 7.1 단백질 언어 모델

| 도구 | 특징 | 참조 |
|------|------|------|
| **ESM-2/ESM-3** | log-likelihood ratio로 변이 적합도 추정, 15B~98B 파라미터 | [EvolutionaryScale](https://www.evolutionaryscale.ai/blog/esm3-release) |
| **InstructPLM-mu** | 150M ESM2에서 1시간 미세조정으로 ESM3 능가 | [bioRxiv 2025](https://www.biorxiv.org/content/10.1101/2025.04.25.650688v1.full) |
| **PLM + SARS-CoV-2** | 전팬데믹 데이터로 팬데믹 진화 궤적 예측 | [Nature Comm. 2026](https://www.nature.com/articles/s41467-026-69569-9) |

### 7.2 구조 통합 면역 회피 예측

| 도구 | 특징 | 참조 |
|------|------|------|
| **EVEscape** | 적합도 × 접근성 × 비유사성, 2020년 이전 데이터로 팬데믹 변이 예측 | [Nature 2023](https://www.nature.com/articles/s41586-023-06617-0) |
| **PRIEST** | 시계열 + 구조 통합, 면역 회피 변이 예측 | [BIB 2024](https://academic.oup.com/bib/article/25/3/bbae218/7671044) |
| **EvoScape** | 진화 + 구조 통합 임베딩, top-K differential pooling | [bioRxiv 2025](https://www.biorxiv.org/content/10.1101/2025.07.31.667864v1.full) |
| **MT-TopLap** | AlphaFold 3 + 위상적 데이터 분석 | [PMC 2024](https://pmc.ncbi.nlm.nih.gov/articles/PMC11601794/) |

### 7.3 변이 예측 프레임워크

| 도구 | 특징 | 참조 |
|------|------|------|
| **PETRA** | 시간적 재가중치 진화 트랜스포머, XEC/LP.8.1 사전 예측 | [arXiv 2025](https://arxiv.org/html/2511.03976v1) |
| **TEMPO** | 계통수 기반 트랜스포머, 39개 중 22개 변이 예측 | [PMC 2022](https://pmc.ncbi.nlm.nih.gov/articles/PMC9747230/) |
| **ViralForesight** | 단백질 언어 모델 + in silico 진화 | [PMC 2025](https://pmc.ncbi.nlm.nih.gov/articles/PMC12204194/) |

### 7.4 MutClust vs 최신 방법 비교

| 측면 | MutClust | 최신 딥러닝 방법 |
|------|---------|--------------|
| 예측 vs 탐지 | **사후적** 핫스팟 탐지 | **사전적** 변이 예측 |
| 구조 정보 | 1D 서열 위치만 | 3D 구조 (AlphaFold) |
| 시간 정보 | 미사용 | 시계열 진화 정보 |
| 학습 능력 | 고정 수식 | 데이터로부터 패턴 학습 |
| 배경 돌연변이율 | 미보정 | 복제 타이밍, 후성유전학 보정 |
| 해석 가능성 | **높음 (투명한 수식)** | 제한적 (블랙박스) |
| 데이터 요구량 | **낮음** | 높음 |

---

## 8. MutClust v2 개선 방향 제안

### 8.1 즉시 적용 가능 (코드 수정)

| 개선 | 설명 | 난이도 |
|------|------|--------|
| H-score 벡터화 | numpy 배열 연산으로 전환, ~100배 속도 향상 | 낮음 |
| Bootstrap 병렬화 | `multiprocessing.Pool` 적용 | 낮음 |
| `scipy.sparse` | Network propagation의 dense → sparse 행렬 | 낮음 |
| `np.random.seed()` | 재현성 보장 | 낮음 |
| `_expand_cluster` 버그 수정 | 감쇠 공식에서 distance > deps_ccm 처리 | 낮음 |

### 8.2 중기 개선 (알고리즘 확장)

#### (a) 3D 구조 통합 클러스터링

- AlphaFold2/ESMFold 예측 구조로 잔기 간 3D 유클리드 거리 계산
- `compute_deps`에서 3D 이웃 반경으로 확장
- 1D + 3D 교집합/합집합을 통한 포괄적 핫스팟 탐지
- HotMAPS 스타일 Getis-Ord G-통계량 적용

#### (b) 계통발생 보정

- TreeTime으로 각 변이의 독립적 발생 횟수(homoplasy count) 계산
- `P_i_corrected = n_independent_events / total_branches`로 대체
- 시간적 계층화로 시기별 서열 비율 정규화

#### (c) 기능적 주석 통합

- 비동의 변이에 가중치, 동의 변이에 감소된 가중치
- 단백질 도메인 정보(Pfam, InterPro) 활용
- 확장 H-score: `H_i_v2 = log2(P_i * |E_i| * W_func * 100 + 1)`

#### (d) HDBSCAN 기반 자동 파라미터

- gamma 수동 설정 대신 HDBSCAN의 밀도 기반 자동 클러스터 선택
- CCM 임계값을 데이터 분포의 백분위수 기반으로 자동 설정

#### (e) 통계 검정 개선

- Bootstrap 반복 10,000회 이상, 또는 적응적 횟수 선택
- 순환 검정 대신 외부 검증 (교차 검증, 독립 데이터셋)
- 복합 통계량 AND → 단일 통합 통계량 (Fisher's combined test)

### 8.3 장기 개선 (패러다임 확장)

#### (a) 상위성 감지 모듈

- MI(Mutual Information) / DCA(Direct Coupling Analysis)로 공변이 위치 쌍 탐지
- 핫스팟 내/핫스팟 간 상위성 네트워크 구축

#### (b) 딥러닝 통합 변이 영향 예측

- ESM-2 log-likelihood ratio → 위치별 적합도 점수
- EVEscape 프레임워크의 세 요소(적합도, 접근성, 비유사성)를 핫스팟 수준에서 집계
- **H-score + ESM fitness + structural accessibility**의 다중 스케일 점수 체계

#### (c) 다중 스케일 분석 프레임워크

```
Level 1: 뉴클레오타이드 (현재 H-score)
    ↓
Level 2: 코돈 (동의/비동의, dN/dS)
    ↓
Level 3: 아미노산 (ESM fitness, 물리화학적 변화)
    ↓
Level 4: 도메인 (RBD, NTD, furin site)
    ↓
Level 5: 3D 구조 (AlphaFold 공간 클러스터링)
    ↓
Level 6: 기능 (ACE2 결합, 항체 회피, 전파력)
```

#### (d) 실시간 감시 시스템

- 스트리밍 데이터 점진적 H-score 업데이트
- 새로운 계통 출현 시 자동 경고
- wastewater 감시 데이터 통합

#### (e) HLA 분석 고도화

- NetMHCpan 4.1 / MHCflurry 2.0 통합
- T세포 + B세포 에피토프 분석
- 인구 수준 HLA 빈도 기반 population coverage 계산

---

## 9. 우선순위 로드맵

| 단계 | 내용 | 영향도 | 난이도 |
|------|------|--------|--------|
| **v2.0** | 코드 최적화 + 버그 수정 + 재현성 | 중 | 낮음 |
| **v2.1** | HDBSCAN 기반 자동 파라미터 + 통계 개선 | 높음 | 중간 |
| **v2.2** | 3D 구조 통합 + 기능적 주석 | 높음 | 높음 |
| **v2.3** | 계통발생 보정 + 상위성 탐지 | 높음 | 높음 |
| **v3.0** | ESM/EVEscape 통합 + 다중 스케일 | 최고 | 최고 |

---

## 참고 문헌

### 3D 구조 기반 분석
- Tokheim et al. (2016) "Exome-Scale Discovery of Hotspot Mutation Regions Using 3D Protein Structure" Cancer Research
- Niu et al. (2020) "HotSpot3D web server" Bioinformatics
- Gao et al. (2019) "Leveraging protein dynamics to identify cancer mutational hotspots" PNAS

### 바이러스 진화 및 편향
- Lemey et al. (2022) "Impact of sampling bias on viral phylogeographic reconstruction" PLOS Global Public Health
- Zeng et al. (2021) "SARS-CoV-2 variant evolution in the United States" PLOS ONE
- De Maio et al. (2025) "Rate variation and recurrent sequence errors in pandemic-scale phylogenetics" Nature Methods

### 상위성 및 공변이
- Turbowicz et al. (2024) "Real-time identification of epistatic interactions in SARS-CoV-2" Genome Biology
- Rodriguez-Rivas et al. (2022) "Epistatic models predict mutable sites in SARS-CoV-2" PNAS

### 딥러닝 및 변이 예측
- Notin et al. (2023) "EVEscape: Learning from prepandemic data to forecast viral escape" Nature
- Lin et al. (2023) "ESM-2/ESM-3" EvolutionaryScale
- Frazer et al. (2021) "Disease variant prediction with deep generative models (EVE)" Nature

### 방법론 비교
- Munoz et al. (2020) "MutSpot: Non-coding mutation hotspot detection" npj Genomic Medicine
- Osia et al. (2024) "Phylogenetic signatures reveal multilevel selection" Wellcome Open Research
