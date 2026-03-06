# 논문 심층 정리: Identification of Severity Related Mutation Hotspots in SARS-CoV-2 Using a Density-Based Clustering Approach

---

## 1. 논문 기본정보

| 항목 | 내용 |
|------|------|
| **제목** | Identification of severity related mutation hotspots in SARS-CoV-2 using a density-based clustering approach |
| **저자** | Sohyun Youn^1†, Dabin Jeong^2†, Hwijun Kwon^1†, Eonyong Han^1, Sun Kim^2,3,4,5, Inuk Jung^1* (†공동1저자) |
| **저널** | BioData Mining (2025) 18:61 |
| **출판일** | Received: 2025.03.28 / Accepted: 2025.08.15 / Published online: 2025.09.01 |
| **DOI** | https://doi.org/10.1186/s13040-025-00476-3 |
| **코드 저장소** | https://github.com/cobi-git/mutclust |
| **데이터** | CODA (Clinical and Omics Data Archive): CODA_D23017 |
| **라이선스** | Creative Commons Attribution-NonCommercial-NoDerivatives 4.0 International |
| **소속** | ^1경북대학교 컴퓨터공학과, ^2Wellcome Sanger Institute, ^3AIGENDRUG Co., ^4서울대학교 컴퓨터공학과, ^5서울대학교 AI 학제간프로그램 |

---

## 2. 연구 배경 및 동기

### 2.1 SARS-CoV-2 변이 분석의 중요성

COVID-19는 전 세계적으로 7억 건 이상의 확진과 700만 명 이상의 사망을 초래한 감염병으로, SARS-CoV-2의 지속적 진화와 치명적 변이체(lethal variants)의 출현으로 인해 공중보건 시스템에 전례 없는 부담을 주었다. 바이러스의 변이는 전파력(transmissibility), 중증 유발 능력(ability to cause severe disease), 항체 회피 능력(capacity to evade antibodies) 등 바이러스의 핵심 특성을 변화시키므로, 변이와 질병 중증도(severity) 간의 연관성을 규명하는 것이 백신 설계, 면역 모니터링, 실시간 게놈 감시에 필수적이다.

### 2.2 기존 접근법의 한계

#### 빈도 기반 접근법 (Frequency-based approach)
- **원리**: 아미노산 또는 뉴클레오타이드 수준에서 변이 빈도를 계산하여, 자주 발생하는 변이가 기능적으로 중요하다고 가정
- **한계 1 - Lineage bias**: 특정 계통(lineage)이 데이터베이스에서 과대 대표되면, 해당 계통의 변이가 빈도 순위에서 과도하게 높은 점수를 받음
- **한계 2 - 희귀 변이 간과**: 빈도는 낮지만 다양한 형태로 나타나는 변이(rare but diverse mutations)를 놓침 -- 이러한 변이는 바이러스의 적응(viral adaptation)이나 면역 회피(immune evasion)를 시사할 수 있음

#### 엔트로피 기반 접근법 (Entropy-based approach)
- **원리**: Shannon entropy를 사용하여 특정 위치의 뉴클레오타이드 다양성(diversity)을 측정
- **한계**: 전체 변이 빈도(overall mutation prevalence)를 반영하지 못함 -- 극히 드물지만 다양한 위치도 높은 엔트로피 점수를 받을 수 있음

### 2.3 밀도 기반 접근의 필요성

기능적으로 중요한 변이 핫스팟(mutation hotspot)은 구조적 또는 면역학적 선택압(selective pressure) 하에 있는 영역에서 발생하며, 비균일(nonuniform)하고 불규칙한 패턴으로 클러스터를 형성하는 경향이 있다. 그러나 고정 길이 슬라이딩 윈도우(fixed-length sliding windows)나 전통적 클러스터링 알고리즘으로는 바이러스 게놈의 생물학적 복잡성을 포착하기에 부적합하다. 따라서 변이의 **빈도와 다양성을 동시에 고려**하면서, **게놈 위치에 따라 적응적으로 클러스터 경계를 조절**하는 밀도 기반 접근법이 필요하다.

---

## 3. 선행연구 분석

### 3.1 빈도 기반 접근법

| 연구 | 방법 | 대상 | 한계 |
|------|------|------|------|
| Huang et al. (2022) | 기계학습 기반 변이-중증도 연관 | SARS-CoV-2 | 빈도 편향(lineage bias) |
| Kim et al. (2022) | NGS 데이터 벡터화 + 클러스터링 | SARS-CoV-2 코돈 | 다양성 미반영 |
| Harvey et al. (2021) | Spike 변이 + 면역 회피 리뷰 | SARS-CoV-2 variant | 서술적 분석 |
| Goswami et al. (2021) | 핫스팟의 반복서열/CpG island 농축 | SARS-CoV-2 | 밀도 구조 미반영 |

빈도 기반 접근은 직관적이고 구현이 단순하나, **자주 나타나지만 다양성이 낮은 변이**(예: lineage-defining mutation)에 편향되며, 빈도는 낮으나 면역학적으로 중요한 변이를 간과한다.

### 3.2 엔트로피 기반 접근법

Shannon entropy는 뉴클레오타이드의 불확실성(uncertainty)을 측정하는 정보이론적 지표이다. 그러나 기존의 뉴클레오타이드 엔트로피(nucleotide entropy)는 **변이 여부와 무관하게** 모든 뉴클레오타이드의 분포를 반영하므로, 변이가 발생한 조건 하에서의 실질적 다양성을 포착하지 못한다.

### 3.3 Mullick et al. (2021)

- **방법**: Shannon entropy + K-means 클러스터링
- **대상**: SARS-CoV-2 Spike protein에 한정
- **기여**: Spike 단백질 내 핫스팟 탐지
- **한계**:
  - Spike protein에만 한정되어 전체 게놈 분석 불가
  - K-means는 사전에 클러스터 수를 지정해야 하며, 밀도 구조를 반영하지 못함
  - 빈도와 다양성의 결합 지표 부재

### 3.4 DBSCAN 직접 적용의 문제

DBSCAN(Density-Based Spatial Clustering of Applications with Noise)은 밀도 기반 클러스터링의 대표적 알고리즘이나, SARS-CoV-2 게놈에 직접 적용 시 심각한 한계를 보인다.

본 논문에서 동일 데이터(29,903개 뉴클레오타이드)에 DBSCAN을 적용한 결과:
- **입력**: 변이 비율(mutation percentage)과 엔트로피(entropy)를 2차원 특징으로 사용
- **파라미터**: MinPts = 5, epsilon = 0.15 (k-distance plot 기반)
- **결과**: 총 4개 클러스터 -- Cluster0(29,831개, **99.76%**), Cluster1(9), Cluster2(16), Cluster3(10), Noise(37)
- **문제**: 전체 데이터의 99.76%가 하나의 거대 클러스터로 통합되어, 생물학적으로 의미 있는 핫스팟 구분이 불가능

이는 DBSCAN의 **고정된 global epsilon과 MinPts**가 게놈 전체의 밀도 변이를 반영하지 못하기 때문이다.

### 3.5 선행연구 대비 본 연구의 차별점

| 관점 | 선행연구 | 본 연구 (MutClust) |
|------|---------|------------------|
| **변이 중요도 지표** | 빈도 또는 엔트로피 단독 사용 | H-score: 빈도 x 다양성 결합 |
| **엔트로피 정의** | Nucleotide entropy (전체 분포) | Mutation entropy (변이 조건부 분포) |
| **클러스터링** | K-means (고정 클러스터 수) 또는 DBSCAN (고정 epsilon) | MutClust: H-score 비례 local epsilon + 감쇠 인자 |
| **분석 범위** | Spike protein 또는 특정 영역 | 전체 게놈 (29,903 bp) |
| **중증도 연관** | 빈도 기반 연관 | 다중오믹스 기반 (EHR + 사이토카인 + scRNA-seq + HLA) |
| **면역학적 해석** | 제한적 | Network propagation + DEG + HLA-에피토프 친화도 |
| **검증** | SARS-CoV-2에 한정 | 인플루엔자 게놈으로 추가 검증 |

---

## 4. 연구 방법론

### 4.1 H-score 지표

H-score는 특정 게놈 위치의 **변이 빈도(mutation frequency)**와 **변이 다양성(mutation diversity)**을 동시에 반영하는 새로운 변이 중요도 지표이다.

#### 수식 유도 (단계별)

**Step 1: 뉴클레오타이드 비율 (Nucleotide ratio)**

위치 i에서 뉴클레오타이드 k의 빈도를 f_ik라 하면 (k는 {A, T, G, C}), 각 뉴클레오타이드 j의 비율은:

```
r_ij = f_ij / Sigma_{k in {A,T,G,C}} f_ik          ... (Eq. 1)
```

- 전체 서열 수 대비 해당 위치에서 특정 뉴클레오타이드가 관찰된 비율
- 224,318개 SARS-CoV-2 서열에 대해 각 위치별로 계산

**Step 2: 변이 비율 (Mutation ratio, P_i)**

위치 i에서 변이된 뉴클레오타이드 집합을 M_i라 정의하면 (참조 서열과 다른 뉴클레오타이드):

```
P_i = Sigma_{k in M_i} r_ik                         ... (Eq. 2)
```

- P_i는 해당 위치에서 변이가 발생한 전체 비율 (0~1)
- P_i가 높을수록 해당 위치에서 변이가 빈번하게 발생

**Step 3: 변이 엔트로피 (Mutation entropy, E_i)**

```
E_i = Sigma_{k in M_i} (r_ik / P_i) * log_2(r_ik / P_i)    ... (Eq. 3)
```

- **핵심 차이**: 변이가 발생했다는 **조건 하에서**의 다양성만 측정
- r_ik/P_i는 변이 뉴클레오타이드 내에서의 조건부 확률(conditional probability)
- E_i 값이 클수록 (절대값) 변이 유형이 다양함을 의미

**Step 4: H-score**

```
H_i = log_2(P_i * E_i * 100 + 1)                    ... (Eq. 4)
```

- P_i * E_i: 빈도와 다양성의 곱 -- 두 요소를 동시에 반영
- *100: P_i * E_i의 값이 매우 작을 수 있으므로 스케일 조정 (해석 가능한 범위로 변환)
- +1: log_2(0) 방지를 위한 smoothing 상수
- log_2: 값의 범위를 압축하여 극단값의 영향을 완화

#### Mutation Entropy vs Nucleotide Entropy

| 항목 | Nucleotide Entropy | Mutation Entropy |
|------|-------------------|-----------------|
| **정의** | 모든 뉴클레오타이드(A,T,G,C) 분포의 불확실성 | 변이 발생 조건 하에서 변이 유형의 다양성 |
| **계산 대상** | {A, T, G, C} 전체 | M_i (변이된 뉴클레오타이드만) |
| **c315 H-score percentile** | 99.8% (거의 최고 -- 탐지 불가) | 2.3% (중간 이하 -- 의미있는 구분 가능) |
| **c442 H-score percentile** | 97.3% | 5.2% |
| **문제점** | 변이 여부와 무관하게 높은 점수 부여 가능 | - |
| **Severity 관련 변이 포착** | 어려움 | 효과적 |

**핵심 통찰**: c315와 c442는 중증도(severity)와 가장 강하게 연관된 핫스팟이다. Nucleotide entropy로 계산하면 이들이 99.8%, 97.3% percentile로 거의 최상위에 위치하여 다른 핫스팟과 구분이 되지 않는다. 반면, mutation entropy를 사용하면 2.3%, 5.2% percentile로, 상대적으로 중간 수준의 H-score를 가지면서도 severity와 강한 연관을 보여 -- mutation entropy가 severity-related 변이를 더 잘 포착함을 실증한다.

#### H-score의 장점

1. **빈도 + 다양성 통합**: 단일 스칼라 값으로 두 특성을 동시에 반영
2. **Lineage bias 완화**: 빈도만 높고 다양성이 낮은 lineage-defining 변이의 과대평가 방지
3. **희귀 변이 포착**: 빈도는 중간이지만 다양한 형태의 변이(severity 관련)를 탐지
4. **MutClust의 입력**: local epsilon 계산에 직접 활용되어, 생물학적 중요도에 비례한 클러스터링 가능
5. **해석 용이**: log 스케일로 값의 범위가 압축되어 비교 및 시각화에 적합

### 4.2 MutClust 알고리즘

MutClust는 DBSCAN 프레임워크에 기반하되, 바이러스 게놈의 변이 특성에 맞게 핵심적인 개선을 도입한 밀도 기반 클러스터링 알고리즘이다.

#### DBSCAN과의 핵심 차이

| 항목 | DBSCAN | MutClust |
|------|--------|----------|
| **epsilon (반경)** | 고정된 global 값 (전체 데이터에 동일 적용) | H-score 기반 local 동적 조정 (위치마다 다름) |
| **MinPts** | 고정 global 값 | 고정 (5), CCM 조건과 연동 |
| **클러스터 경계** | 고정 (epsilon에 의해 결정) | 감쇠 인자(diminishing factor, d=3)로 동적 조절 |
| **핵심 개념** | Core point (밀도 조건 충족) | Core Candidate Mutation (CCM, 4가지 조건) |
| **입력 차원** | 2차원 (mutation %, entropy) | 1차원 (H-score 값, 게놈 위치) |
| **적응성** | 밀도 변화에 취약 | H-score에 비례하여 자동 적응 |
| **SARS-CoV-2 결과** | 4개 클러스터 (99.76% 단일 클러스터) | **477개** 의미 있는 핫스팟 |

#### CCM (Core Candidate Mutation) 4가지 조건

CCM은 MutClust에서 클러스터의 씨앗(seed)이 되는 핵심 변이 위치이다. 다음 **4가지 조건을 모두 충족**해야 CCM으로 인정된다:

| 조건 | 수식 | 의미 | 임계값 |
|------|------|------|--------|
| **조건 1** | H_i > 0.03 | 해당 위치 자체의 H-score가 충분히 높음 | 0.03 |
| **조건 2** | mean(H-scores in Deps) > 0.01 | 할당된 이웃 영역(Deps) 내 평균 H-score가 충분 | 0.01 |
| **조건 3** | sum(H-scores in Deps) > 0.05 | Deps 내 H-score 합이 충분 | 0.05 |
| **조건 4** | count(mutant bases in Deps) > 5 | Deps 내 변이 위치 수가 MinPts 이상 | 5 (= MinPts) |

- 조건 1: 개별 위치의 중요도 보장
- 조건 2-3: 주변 환경의 품질 보장 (고립된 높은 H-score 위치 필터링)
- 조건 4: DBSCAN의 MinPts에 해당하는 최소 밀도 조건

#### 파라미터 설정

| 파라미터 | 기호 | 값 | 역할 | 결정 근거 |
|---------|------|---|------|---------|
| **Eps scaling factor** | gamma | 10 | CCM의 local epsilon 크기 결정 | 5-dist plot의 valley 위치(500)에 기반 |
| **Diminishing factor** | d (partial) | 3 | 클러스터 확장 시 경계 감쇠 비율 | 저 H-score 영역 배제를 위한 경험적 설정 |
| **MinPts** | MinPts | 5 | 클러스터 내 최소 변이 위치 수 | CCM 조건 4와 일치, 5-dist 계산 근거 |

**Deps (epsilon neighborhood) 계산:**

```
Deps_CCM = ceil(gamma * H_i)                         ... (Eq. 5)
```

- H-score가 높은 위치에 더 넓은 반경(neighborhood)을 할당
- 생물학적 중요도가 높은 영역은 더 넓은 범위에서 이웃을 탐색

**Deps 감쇠 (Diminishing):**

```
Deps_CCM = Deps_CCM - (Deps_CCM - Deps_i) / d       ... (Eq. 6)
```

- CCM에서 멀어질수록 Deps가 점진적으로 축소
- 저 H-score 영역이 클러스터에 포함되는 것을 방지
- 현재 거리(Deps_i)가 원래 Deps_CCM을 초과하면 확장 종료, epsilon으로 대체

#### 알고리즘 동작 과정

**Phase 1: CCM 탐색**
1. 전체 게놈(29,903 위치)에 대해 H-score 계산
2. 각 위치에 Deps_CCM = ceil(gamma * H_i) 할당
3. 4가지 CCM 조건을 모두 충족하는 위치를 CCM으로 선정
4. 각 CCM이 하나의 잠재 클러스터 중심이 됨

**Phase 2: 클러스터 확장**
1. 임의의 CCM에서 출발
2. CCM의 Deps 내에서 H-score가 높은 영역을 포함하며 양방향(좌우)으로 확장
3. 확장 시마다 Deps를 감쇠 인자(d)로 축소하여 경계 조절
4. MinPts 조건(변이 위치 수 >= 5)이 충족되는 한 확장 계속
5. 조건 미충족 또는 Deps 소진 시 해당 클러스터 확정
6. 모든 CCM에 대해 반복 -- CCM 수 = 최종 클러스터 수

**파라미터 결정 과정 (5-dist plot):**
- CCM 조건을 충족하는 위치들에 대해 k=5 최근접 이웃 거리(5-dist) 계산
- 5-dist를 정렬하여 k-dist plot 생성
- Valley(급격한 변화점)가 거리 500에서 관찰
- gamma=10, d=3으로 설정 시 핫스팟 크기가 500 미만으로 제한됨을 확인

### 4.3 중증도 연관 분석

#### KDCA 코호트 데이터

| 항목 | 내용 |
|------|------|
| **출처** | 질병관리청(KDCA) 국책 사업 |
| **병원** | 충남대학교병원, 서울의료원, 삼성서울병원 (3개 기관) |
| **환자 수** | 387명 |
| **중증도 분류** | WHO ordinal scale 기준: score >= 6 → Severe (42명), score < 6 → Moderate (345명) |
| **인구 통계** | 남 211 / 여 176, 60세 이하 258 / 60세 초과 129 |
| **동반 질환** | 80명 중 31명이 중증 관련 (고지혈증 24, 갑상선기능저하 5, 이상지질혈증 3 등) |
| **계통(Lineage)** | 22개 계통 -- B.1.497(155), B.1.619(58), AY.69(56), B.1.619.1(34) 등 |
| **다중오믹스** | SARS-CoV-2 서열, EHR, 사이토카인 프로필, HLA 표현형(213명), scRNA-seq |
| **시간적 특성** | 입원 기간 중 다중 시점에서 샘플 수집 |

#### 통계 검정 방법

**1. Feature Selection (중증도 연관 핫스팟 선별):**
- SelectKBest (scikit-learn) + ANOVA F-test
- 477개 핫스팟 각각에 대해 중증도(moderate vs severe) 그룹 간 차이 검정
- k = 'all'로 설정하여 모든 핫스팟 평가
- FDR corrected p-value 기준 유의한 28개 핫스팟 선별

**2. FDR Correction (Benjamini-Hochberg):**
```
다중 검정 보정:
1. 모든 p-value를 오름차순 정렬
2. 각 p-value에 순위(rank) 부여
3. adjusted p-value = p-value * (총 검정 수 / rank)
4. adjusted p-value < 0.05인 핫스팟만 선택
→ 28개 severity-related hotspot 선별
```

**3. Bootstrap Testing (핫스팟 유의성 검증):**
```
각 477개 핫스팟에 대해:
1. 해당 핫스팟과 동일 크기의 랜덤 게놈 영역을 1,000회 샘플링
2. 각 랜덤 영역에서 계산:
   - 변이 수 (number of mutations)
   - 평균 H-score (mean H-score)
   - H-score 합 (sum of H-scores)
3. 실제 핫스팟의 값과 비교하여 p-value 계산
4. H0: 해당 클러스터는 우연히 발생 가능
5. Benjamini-Hochberg correction 적용
```

**4. 환자 클러스터링 (Hierarchical Clustering):**
- 28개 핫스팟을 열(column), 387명 환자를 행(row)으로 하는 변이 수 행렬 구성
- Seaborn clustermap을 이용한 계층적 클러스터링 수행
- 7개 환자 그룹으로 분할
- 10명 미만 그룹(cluster 4: 1명, cluster 5: 5명, cluster 7: 1명) 제외
- 나머지 4개 그룹을 중증도에 따라 분류:
  - **SMS (Severe Mutation Signature)**: Cluster 6 (53명, 중증 비율 최고)
  - **MMS (Moderate Mutation Signature)**: Cluster 1(123명), Cluster 2(186명), Cluster 3(18명) (중등도 비율 상대적 높음)

### 4.4 면역학적 분석

#### Network Propagation

**목적**: SARS-CoV-2 변이 핫스팟이 인간 유전자에 미치는 영향을 간접적으로 평가

**네트워크 구축:**
- PPI 데이터베이스: STRING + Biogrid
- 바이러스 유전자 필터링: Coronaviridae 계열 (Human coronavirus 229E, Human SARS coronavirus, SARS-CoV-2 등)
- 인간 유전자 필터링: mSigDB 면역 관련 유전자
- STRING + Biogrid 네트워크를 연결하여 통합 유전자-유전자 상호작용 네트워크 구성

**Seed 유전자 준비:**
- 각 환자 그룹(MMS, SMS)별로 변이 핫스팟에 해당하는 바이러스 유전자를 seed로 설정
- ENSEMBL 참조 게놈으로 핫스팟 영역에 해당하는 유전자 매핑
- 변이 수 > 2인 핫스팟의 바이러스 유전자만 포함

**전파 수식:**
```
p^(t+1) = (1 - alpha) * W * p^t + alpha * p_0        ... (Network propagation)

- alpha = 0.01 (시드 영향 유지 비율, restart probability)
- W: 인접 행렬 (adjacency matrix, 정규화됨)
- p_0: 초기 노드 자원 벡터 (시드 유전자 = 1, 나머지 = 0)
- p^t: t번째 반복에서의 노드 자원 벡터
- 수렴 시까지 반복
- 수렴 후 각 노드의 자원량 = 시드 유전자로부터의 영향도
```

**결과 해석:**
- 각 그룹(MMS, SMS)에서 전파 점수가 가장 높은 상위 100개 인간 유전자 선택
- EnrichR을 이용한 Gene Ontology (GO) enrichment 분석
- MMS: 항미생물 체액 면역(Immunoglobulin A, IgM) 농축
- SMS: **NK 세포 매개 세포독성(NK cell mediated cytotoxicity)** 농축

#### DEG 분석 (scRNA-seq)

| 항목 | 내용 |
|------|------|
| **대상** | 387명 중 scRNA-seq 데이터 보유 106명 |
| **데이터 형태** | 단일세포 pseudobulk 샘플 (세포 유형별 aggregation) |
| **시간점** | 환자당 1~7개 시간점 (longitudinal) |
| **샘플 수** | MMS 261개 + SMS 92개 = 353개 pseudobulk 샘플 |
| **분석 도구** | edgeR (version 3.32.1) |
| **통계 검정** | Fisher's exact test + Benjamini-Hochberg correction |
| **필터링** | 80% 이상 샘플에서 0 count인 유전자 제외 → 12,537개 유전자 분석 |
| **결과** | 3,951개 DEGs (p-adj < 0.05) |

**NK 세포 관련 주요 발견:**

| 범주 | 유전자 | SMS에서의 변화 | 유의성 |
|------|--------|-------------|--------|
| **억제 수용체 (Inhibitory receptors)** | KIR2DL1 | 감소 (down) | 유의 |
| | KIR2DL3 | 감소 | 보고됨 |
| | KIR3DL2 | 감소 | 보고됨 |
| **활성화 수용체 (Activating receptors)** | NCR1 (NKp46) | 증가 (up) | 유의 |
| | NCR3 (NKp30) | 증가 | 보고됨 |
| | NKG2D | 증가 | 유의 |
| | NKG2C | 증가 | 보고됨 |
| **공동활성화 수용체 (Co-activating receptors)** | CD226 | 증가 | 유의 |
| | CD244 | 증가 | 유의 |
| | CD352 | 증가 | 유의 |
| **세포독성 분자 (Cytotoxic molecules)** | PRF1 (perforin) | 증가 | 유의 |
| | GZMA (granzyme A) | 증가 | 유의 |

**사이토카인 수준 (cytokine profile):**
- IFN-gamma: SMS에서 유의미하게 상승
- TNF: SMS에서 유의미하게 상승
- 이는 사이토카인 폭풍(cytokine release syndrome, CRS)과의 연관을 시사

#### HLA-에피토프 친화도 분석

**분석 과정:**
1. 387명 중 213명의 HLA genotype 데이터 확보
2. 6개 HLA loci에서 빈도 상위 10개 HLA allele 합집합 → 총 39개 HLA
3. c315 핫스팟: 4,095개 HLA-에피토프 쌍의 친화도 계산
4. c442 핫스팟: 13,104개 HLA-에피토프 쌍의 친화도 계산
5. 기준: 참조 서열(reference) 에피토프의 친화도 < 500 nM → mild/strong affinity
6. c315에서 29쌍, c442에서 9쌍이 기준 충족
7. 각 환자의 변이 서열에서 파생된 에피토프의 친화도와 참조 친화도 비교

**주요 결과 (c315 핫스팟, Table 3):**

| HLA Allele | Peptide | Reference 친화도 (nM) | MMS 친화도 | SMS 친화도 | MMS LFC | SMS LFC |
|------------|---------|---------------------|-----------|-----------|---------|---------|
| HLA-A*31:01 | KSWMESEFR | 17 | 17.5 | 8,342 | 0.04 | 8.94 |
| HLA-A*31:01 | KNNKSWMESEFR | 126 | 129 | 21,609 | 0.03 | 7.42 |
| HLA-A*33:03 | NKSWMESEFR | 293 | 304 | 28,571 | 0.05 | 6.61 |
| HLA-A*33:03 | NNKSWMESEFR | 340 | 350 | 31,303 | 0.04 | 6.52 |
| HLA-A*31:01 | NKSWMESEFR | 402 | 418 | 25,382 | 0.05 | 5.98 |
| HLA-C*14:03 | YYHKNNKSWMESEF | 227 | 382 | 8,250 | 0.75 | 5.18 |
| HLA-C*14:02 | YYHKNNKSWMESEF | 227 | 382 | 8,250 | 0.75 | 5.18 |
| HLA-A*11:01 | KSWMESEFR | 279 | 283 | 0.0293 | 0.02 | 5.05 |

- SMS 그룹에서 8개 HLA-에피토프 쌍의 친화도가 유의미하게 **감소** (LFC 증가 = 친화도 약화)
- 특히 HLA-A*31:01, HLA-A*33:03에서 가장 큰 변화
- HLA-A*11:01, HLA-C*14:02는 기존 연구에서 중증 COVID-19와 연관된 allele
- c442에서는 이러한 경향이 관찰되지 않음

---

## 5. 핵심 결과

### 5.1 핫스팟 탐지 결과 (477개)

- **입력 데이터**: GISAID 224,318개 SARS-CoV-2 서열 (2020.01~2022.11)
- **참조 게놈**: Wuhan-Hu-1 (hCoV-19/Wuhan/WIV04/2019, 29,903 bp)
- **서열 정렬**: MAFFT v7.490
- **H-score 할당**: 29,903개 중 29,409개 위치 (98.3%)에 H-score 부여
  - Prefix/suffix의 소수 위치는 서열 변이가 높아 severity와 무관할 가능성으로 제외
- **핫스팟 수**: **477개** mutation hotspot 탐지
- **Lineage-dividing 변이**: 477개 중 88개 핫스팟이 lineage-dividing 변이 포함
- **검증**: 알려진 10개 기능적 변이(functional mutation) 중 **9개가 핫스팟 내 포함**

| 변이 | 효과 | 핫스팟 |
|------|------|--------|
| D614G | 세포 유형 transduction 증가, 단백질 분해 저항, 전파력 4~9배 | c346 |
| V483a | 강한 약물 저항성 | c338 |
| E484K | 빠른 전파, 강한 바이러스 전파 | c338 |
| N501Y | ACE2 친화도 증가, 중화항체 결합 관련 | c340 |
| L452R | 항체 중화 약화, 감염 능력 증가 | c334 |
| Q677 (Q677P, Q677H) | ACE2를 통한 숙주 세포 진입 촉진 | c350 |
| P681H | RBD 근처 디설파이드 결합 파괴 가능성 | c350 |
| E484Q | 감염/전파 증가 | c338 |
| S447G/N | hACE2 결합 친화도 증가 | c337 |
| S943P | 감염 숙주 내 바이러스 재조합 | **미포함** |

S943P만 유일하게 미포함 -- S943P는 재조합(recombination) 관련으로, 빈도/다양성 기반 탐지 범위를 벗어남

### 5.2 중증도 연관 결과 (28개 핫스팟, MMS vs SMS)

28개 severity-related hotspot의 유전자별 분포:

| 유전자 | 핫스팟 수 | 주요 핫스팟 |
|--------|---------|----------|
| ORF1a | 6 | c22, c90, c118, c123, c124, c198 |
| ORF1b | 3 | c239, c258, c298 |
| S (Spike) | 6 | c309, **c315**, c319, c334, c337, c350 |
| S (추가) | 1 | c364 |
| ORF3a | 2 | c385, c390 |
| M | 1 | c412 |
| ORF7a | 1 | c429 |
| ORF7a/ORF7b | 1 | c431 |
| ORF8 | 1 | c438 |
| ORF8/N | 1 | **c442** |
| N | 4 | c444, c460, c462, c468 |
| ORF10 | 1 | c474 |

**c315와 c442 -- SMS 시그니처 핫스팟:**

| 항목 | c315 (S protein) | c442 (ORF8/N) |
|------|-----------------|---------------|
| 위치 | 21,965~22,039 | 28,230~28,404 |
| Mutation ratio | 0.97 | 0.79 |
| SMS 평균 변이 수 | **7.04** | **9.04** |
| MMS 평균 변이 수 | 0.24 | 1.23 |
| 차이 (SMS - MMS) | 6.80 | 7.81 |
| 특징 | SMS에서 유일하게 평균 변이 수 > 7인 핫스팟 | SMS에서 유일하게 평균 변이 수 > 7인 핫스팟 |

c315와 c442만이 SMS 그룹에서 평균 변이 수 7 이상을 보여, MMS와 SMS를 구분하는 핵심 요인으로 작용한다.

### 5.3 NK 세포 기능 이상 발견

**Network propagation 결과:**
- MMS 그룹: 항미생물 체액면역(antimicrobial humoral response) 관련 GO term 농축 (IgA, IgM)
- SMS 그룹: **NK 세포 매개 세포독성(NK cell mediated cytotoxicity)** 관련 GO term 최상위 농축

**DEG 분석을 통한 NK 세포 수용체 불균형 확인:**
- **억제 수용체 감소 + 활성화 수용체 증가** → NK 세포의 과활성화(hyperactivation) 패턴
- 정상 상태: 활성화-억제 신호의 균형 → 감염 세포만 선택적 제거
- SMS(중증): 균형 파괴 → 과도한 NK 활성화 → 정상 세포 손상 가능 → 사이토카인 폭풍 연관
- 세포독성 분자(PRF1, GZMA) 상승이 이를 뒷받침
- 기존 연구에서도 중증 COVID-19 환자에서 adaptive-like NK 세포 축적과 NKG2C 상승, KIR 감소가 보고됨

**개념 모델 (Fig. 7 - Conceptual Model):**
1. 정상: HLA-I 정상 발현 → NK 억제 수용체 활성화 → 정상세포 보호
2. 중증: c315 변이 → 에피토프 친화도 감소 → HLA-I 발현 감소 → 억제 신호 부족 → 활성화 수용체 우세 → 과도한 세포독성 반응

> 논문은 Fig. 7을 명확히 "hypothesis-driven conceptual model"로 제시하며, 직접적 실험 증거가 아님을 명시

### 5.4 HLA 분석 결과

- c315에서 29개 HLA-에피토프 쌍 중 **8개에서 SMS 그룹의 친화도 유의미 감소**
- 친화도 감소 = 에피토프-HLA 결합력 약화 = APC 표면에서의 에피토프 제시 시간 단축
- 이는 T/B 세포의 선별 과정(screening process)에 영향을 미쳐 적응면역 반응(adaptive immune response) 저하 가능
- HLA-A*11:01, HLA-C*14:02: 기존 중국 코호트 연구에서도 중증 연관 보고
- c442에서는 이러한 경향이 관찰되지 않음 -- c315가 HLA-mediated immune evasion에 더 직접적

### 5.5 인플루엔자 검증 결과

**데이터:**
- GISAID에서 276,910개 인플루엔자 서열 수집
- 10,000개 이상 서열을 가진 strain만 포함
- A-H1N1 (26,703), A-H3N2 (52,734), B-Victoria (197,473)
- 인플루엔자: 8개 게놈 세그먼트, 각 890~2,341 bp (SARS-CoV-2의 약 1/10)

**결과:**
- 세그먼트당 최대 39개 핫스팟 (B-Victoria PB1)
- 총 24회 분석 (3 strain x 8 segment) 수행

**알려진 변이 검출 성공:**

| 변이 | 위치 | 임상적 의의 | 핫스팟 |
|------|------|---------|--------|
| D222G | H1N1-HA | 높은 사망률(high mortality) | c4 |
| T123V | H1N1-NS1 | 중증(severe outcome) | c3 |
| E627K | H2N2-PB2 | 조류→인간 감염(avian-to-human adaptation) | c31 |
| K338R | B-PB2 | 병원성 증가(increased pathogenicity) | c14 |

**의의와 한계:**
- SARS-CoV-2에 최적화된 파라미터(gamma=10, d=3)를 그대로 사용했음에도 임상적으로 중요한 변이를 포함하는 핫스팟 탐지 성공
- MutClust의 범용성(generalizability) 가능성 시사
- 그러나 게놈 크기 차이(~2,300 bp vs ~30,000 bp)로 인해 최적 결과를 위한 파라미터 재조정 필요

---

## 6. 연구 기여 및 의의

### 6.1 H-score: 새로운 변이 중요도 지표

- **기존 한계 극복**: 빈도만 또는 엔트로피만으로는 포착할 수 없는 severity-related 변이를 효과적으로 탐지
- **Mutation entropy 도입**: 변이 발생 조건 하에서의 다양성을 측정하여, nucleotide entropy 대비 중증도 관련 변이 식별력 향상
- **스칼라 지표**: 빈도와 다양성을 단일 값으로 통합하여 후속 분석(클러스터링, 비교)에 직접 활용 가능
- **범용성**: SARS-CoV-2뿐 아니라 인플루엔자에도 적용 가능함을 검증

### 6.2 MutClust: 적응형 밀도 클러스터링

- **DBSCAN의 근본적 한계 해결**: Global epsilon → Local epsilon (H-score 비례)
- **생물학적 의미 반영**: 변이의 중요도에 따라 클러스터 크기를 자동 조절
- **감쇠 인자(diminishing factor)**: 클러스터 경계에서 저 H-score 영역을 적응적으로 제외
- **실질적 성과**: DBSCAN 4개 vs MutClust **477개** 핫스팟, 10개 알려진 기능적 변이 중 9개 포함
- **확장성**: 1차원 게놈 위치 데이터에 최적화되었으나, 2차원 특징 공간에서의 위치-빈도 데이터에도 적용 가능

### 6.3 생물학적 발견: NK 세포 가설

- **다층적 증거 통합**: Network propagation (단백질 상호작용) + DEG (전사체) + 사이토카인 (단백질체) + HLA (면역유전학) → 일관된 NK 세포 기능 이상 패턴
- **새로운 메커니즘 가설**: SARS-CoV-2가 NK 세포의 활성화-억제 수용체 균형을 교란하여 중증을 유발할 수 있다는 가설 제시
- **기존 연구와의 정합성**: 중증 COVID-19 환자에서 adaptive-like NK 세포 축적, NKG2C 상승, KIR 감소 등 기존 보고와 일치
- **기존 연구와의 차별점**: 기존 바이러스-NK 연구는 주로 바이러스의 NK 회피(evasion) 전략에 초점 → 본 연구는 활성화-억제 수용체의 **상보적 변화(complementary changes)**가 NK 과활성화를 유발하는 새로운 관점 제시

---

## 7. 한계점 및 향후 연구

### 7.1 In silico 분석의 한계

- Network propagation, DEG 분석, HLA-에피토프 친화도 분석 모두 **in silico**(컴퓨터 시뮬레이션) 기반
- Fig. 7의 개념 모델은 hypothesis-driven이며, 직접적 실험 증거(direct experimental evidence)에 기반하지 않음
- 현재 수준은 **correlation**(상관관계)이며, **causation**(인과관계) 입증은 추가 실험 필요
- 필요한 실험적 검증: HLA-binding assay, peptide processing validation, NK cell cytotoxicity test

### 7.2 파라미터 범용성

- gamma=10, d=3은 SARS-CoV-2 게놈(~30 kb)에 최적화된 값
- 인플루엔자 게놈(~2.3 kb/segment)에도 동일 파라미터를 적용 → 임상적으로 중요한 변이 탐지에 성공하였으나, 최적 결과를 보장하지는 않음
- 게놈 크기, 변이율(mutation rate), 서열 수에 따라 파라미터 재조정이 필요
- **향후**: k-dist 기반 adaptive parameter selection 모듈 개발

### 7.3 코호트 크기

- 387명 (moderate 345 + severe 42) -- severe 그룹이 상대적으로 소규모
- 이는 실제 임상 분포를 반영하지만, 통계적 검정력(statistical power) 제약
- HLA genotype은 213명으로 더 축소
- Bootstrap testing과 BH correction으로 보완하였으나, 더 큰 코호트에서의 재현성 검증이 바람직
- 단일 국가(한국) 코호트로, 유전적 배경(genetic background)의 다양성 제한

### 7.4 향후 연구 방향

1. **파라미터 자동 최적화**: 게놈 크기별 k-dist 기반 adaptive parameter selection
2. **범용 바이러스 적용**: HIV, HBV, 추가 인플루엔자 strain, TCGA somatic mutation
3. **NK 세포 가설 실험적 검증**: in vitro HLA-binding assay, NK cell cytotoxicity test
4. **웹 서비스 개발**: 범용 mutation hotspot 탐지 도구 공개
5. **실시간 게놈 감시**: 새로운 변이체 출현 시 실시간 핫스팟 업데이트 파이프라인

---

## 8. 핵심 수식 및 개념

### 8.1 H-score 수식 상세

```
[입력]
  f_ik: 위치 i에서 뉴클레오타이드 k의 관찰 빈도 (k in {A, T, G, C})
  M_i: 위치 i에서 참조 서열과 다른 변이 뉴클레오타이드 집합

[Step 1] 뉴클레오타이드 비율
  r_ij = f_ij / SUM_{k in {A,T,G,C}} f_ik

[Step 2] 변이 비율 (Mutation ratio)
  P_i = SUM_{k in M_i} r_ik
  * 범위: [0, 1]
  * P_i = 0이면 해당 위치에 변이 없음
  * P_i = 1이면 모든 서열이 참조와 다름

[Step 3] 변이 엔트로피 (Mutation entropy)
  E_i = SUM_{k in M_i} (r_ik / P_i) * log2(r_ik / P_i)
  * r_ik / P_i: 변이 내 조건부 확률
  * 범위: [-(log2|M_i|), 0]
  * |E_i|가 클수록 변이 유형이 균등 분포 (높은 다양성)
  * |E_i| = 0이면 단일 변이 유형만 존재

[Step 4] H-score
  H_i = log2(P_i * E_i * 100 + 1)
  * P_i * E_i: 빈도와 다양성의 곱 (두 특성 동시 반영)
  * x100: 스케일 조정 (소수값을 해석 가능 범위로)
  * +1: log2(0) 방지 (smoothing)
  * log2: 극단값 압축

[해석]
  H_i 높음 → 변이 빈도 높고 + 변이 유형이 다양 → 기능적으로 중요할 가능성 높음
  H_i 낮음 → 변이 드물거나 + 변이 유형 단일 → 상대적으로 보존된 위치
```

### 8.2 MutClust 알고리즘 의사코드

```
Algorithm: MutClust

Input:
  H[1..N]: 각 게놈 위치의 H-score 배열
  gamma: eps scaling factor (default: 10)
  d: diminishing factor (default: 3)
  MinPts: 최소 변이 위치 수 (default: 5)

Output:
  Clusters: mutation hotspot 목록

Phase 1: CCM 탐색
──────────────────
CCM_list = empty list

FOR each position i in genome:
  Deps_i = CEIL(gamma * H[i])      // Eq. 5: local epsilon 할당
  neighbors = positions within distance Deps_i of i

  IF  (1) H[i] > 0.03                           AND
      (2) MEAN(H-scores in neighbors) > 0.01    AND
      (3) SUM(H-scores in neighbors) > 0.05     AND
      (4) COUNT(mutant bases in neighbors) > MinPts THEN
    ADD i to CCM_list
  END IF
END FOR

Phase 2: 클러스터 확장
──────────────────────
Clusters = empty list

FOR each CCM in CCM_list:
  cluster = {CCM}
  Deps_current = CEIL(gamma * H[CCM])   // 초기 Deps
  distance = 0

  // 양방향(좌, 우)으로 확장
  FOR each direction in {LEFT, RIGHT}:
    current_pos = CCM
    local_Deps = Deps_current

    WHILE TRUE:
      distance = distance + 1
      next_pos = current_pos + direction

      // Deps 감쇠 (Eq. 6)
      local_Deps = local_Deps - (Deps_current - distance) / d

      IF distance > local_Deps THEN
        local_Deps = Deps_current      // Eps로 리셋
        BREAK
      END IF

      IF next_pos is mutant base THEN
        ADD next_pos to cluster
      END IF

      // MinPts 조건 확인
      IF COUNT(mutant bases in cluster) >= MinPts THEN
        CONTINUE expansion
      END IF
    END WHILE
  END FOR

  ADD cluster to Clusters
END FOR

RETURN Clusters
```

### 8.3 Network Propagation 수식

```
[수식]
  p^(t+1) = (1 - alpha) * W * p^t + alpha * p_0

[변수 정의]
  G = (V, E): 유전자-유전자 상호작용 네트워크
  V_s subset V: 시드 유전자 (바이러스 유전자)
  W: |V| x |V| 인접 행렬 (adjacency matrix, 행 정규화)
  p_0: |V|-차원 초기 자원 벡터
    - p_0[i] = 1  if  gene_i in V_s (시드 유전자)
    - p_0[i] = 0  otherwise
  p^t: t번째 반복에서의 자원 벡터
  alpha = 0.01: restart probability (시드 영향 유지 비율)

[알고리즘]
  1. p^0 = p_0 으로 초기화
  2. 반복: p^(t+1) = (1-alpha)*W*p^t + alpha*p_0
  3. ||p^(t+1) - p^t|| < threshold 이면 수렴 → 종료
  4. 수렴 후 p_final[i] = 유전자 i에 대한 시드 유전자의 영향도

[해석]
  - (1-alpha)*W*p^t: 이웃 노드로의 자원 전파 (diffusion)
  - alpha*p_0: 시드 유전자로의 restart (시드 영향 유지)
  - alpha가 작을수록 → 전파 범위 넓어짐 (더 먼 유전자까지 영향)
  - alpha가 클수록 → 시드 유전자 근처에 영향 집중

[후처리]
  - 인간 유전자만 필터링 (바이러스 유전자 제외)
  - 상위 100개 유전자 선택 → GO enrichment 분석 (EnrichR)
```

### 8.4 통계 검정 수식

**Benjamini-Hochberg FDR Correction:**
```
[입력] m개의 p-value: p_1, p_2, ..., p_m
[정렬] p_(1) <= p_(2) <= ... <= p_(m)

[보정]
  adjusted_p_(i) = p_(i) * m / i

  단, 단조성 보장:
  adjusted_p_(i) = min(adjusted_p_(i), adjusted_p_(i+1))
  (뒤에서부터 순차적으로 적용)

[판정]
  adjusted_p_(i) < 0.05 → 유의미 (reject H0)

[적용]
  - 477개 핫스팟의 severity 연관 검정 → 28개 선별
  - DEG 분석 (12,537개 유전자) → 3,951개 DEG 선별
```

**Bootstrap Testing:**
```
[대상] 각 핫스팟 cluster_j (j = 1, ..., 477)
[절차]
  FOR b = 1 to 1000:
    random_region = 게놈에서 cluster_j와 동일 크기의 랜덤 영역 추출
    compute:
      n_mut_b = random_region 내 변이 수
      mean_H_b = random_region 내 평균 H-score
      sum_H_b = random_region 내 H-score 합
  END FOR

  p_value = (1/1000) * COUNT(n_mut_b >= n_mut_observed AND
                               mean_H_b >= mean_H_observed AND
                               sum_H_b >= sum_H_observed)

[H0] 해당 클러스터의 변이 밀도와 H-score 특성이 우연히 발생 가능
[판정] BH correction 후 adjusted p < 0.05 → 유의미한 핫스팟
```

**Fisher's Exact Test (DEG 분석):**
```
[적용] edgeR에서 MMS vs SMS 간 유전자 발현 차이 검정
[2x2 분할표]
              Group1(MMS)  Group2(SMS)
  Expressed      a            b
  Not expressed  c            d

[수식]
  P = C(a+b, a) * C(c+d, c) / C(n, a+c)
  여기서 n = a+b+c+d

[판정] BH correction 후 adjusted p < 0.05 → DEG
[결과] 12,537개 유전자 중 3,951개 DEG 식별
```

---

## 9. 예상 질문 및 답변

### 기술적 질문 (Technical Questions)

---

**Q1: H-score에서 x100 상수의 역할은 무엇이며, 다른 값을 사용하면 결과가 달라지는가?**

**A**: H-score 수식 H_i = log_2(P_i * E_i * 100 + 1)에서 x100은 스케일링 상수(scaling constant)이다. P_i * E_i의 값이 매우 작을 수 있으므로(0~1 범위의 곱), x100으로 스케일을 조정한 후 log_2를 취하여 해석 가능한 범위로 변환한다. +1은 log_2(0)을 방지하는 smoothing 상수이다.

x100 대신 다른 값(예: 1000)을 사용해도 **H-score의 상대적 순위(rank order)는 변하지 않는다**. 이는 log 변환이 단조증가(monotonically increasing) 함수이기 때문이다. 다만 절대값의 범위가 달라지므로, CCM 임계값(0.03, 0.01, 0.05) 등도 함께 조정해야 한다. 본질적으로 100은 SARS-CoV-2 데이터에서 경험적으로 적절한 동적 범위를 제공하도록 선택된 값이다.

---

**Q2: MutClust에서 gamma=10, d=3 파라미터는 어떻게 결정했으며, 다른 게놈에서도 유효한가?**

**A**: 파라미터 결정은 k-dist plot 분석에 기반한다. CCM 조건을 충족하는 위치들의 5-dist(k=5 최근접 이웃까지의 거리)를 계산하여 정렬한 후, valley(급격한 변화점)가 거리 500에서 관찰되었다. gamma=10, d=3으로 설정하면 핫스팟 크기가 500 미만으로 제한되어, 밀도 높은 변이 클러스터를 효과적으로 탐지할 수 있다.

다른 게놈에 대한 범용성은 인플루엔자 검증에서 부분적으로 확인되었다. 동일 파라미터로 D222G, T123V, E627K, K338R 등 알려진 중증 관련 변이를 포함하는 핫스팟을 탐지하는 데 성공했다. 그러나 인플루엔자 게놈은 SARS-CoV-2의 약 1/10 크기이므로, **최적 결과를 위해서는 게놈 크기와 변이율에 맞는 파라미터 재조정이 필요**하다. 이는 향후 연구에서 k-dist 기반 adaptive parameter selection으로 해결할 계획이다.

---

**Q3: Mutation entropy와 nucleotide entropy의 수학적 차이를 설명하고, c315에서 왜 다른 결과가 나오는지 설명하라.**

**A**: 수학적 차이는 엔트로피 계산에 사용되는 확률 분포의 범위에 있다.

- **Nucleotide entropy**: H_nuc = -SUM_{k in {A,T,G,C}} r_ik * log_2(r_ik). 변이 여부와 무관하게 모든 4개 뉴클레오타이드의 분포를 반영한다.
- **Mutation entropy**: E_i = SUM_{k in M_i} (r_ik/P_i) * log_2(r_ik/P_i). 변이가 발생했다는 조건 하에서 변이 뉴클레오타이드만의 분포를 반영한다.

c315에서 nucleotide entropy가 99.8 percentile인 이유는, 이 위치에서 참조 뉴클레오타이드의 비율이 매우 낮고(P_i = 0.97, 즉 97%가 변이) A, T, G, C가 상대적으로 균등하게 분포하기 때문이다. 그러나 mutation entropy 관점에서 보면, 변이 뉴클레오타이드 내의 분포가 **특정 유형에 편중**되어 있어(다양성이 상대적으로 낮음) 2.3 percentile에 머문다.

이는 c315가 "빈도는 매우 높지만 다양성은 중간"이라는 특성을 가짐을 의미하며, 이러한 변이가 severity와 강하게 연관된다는 것이 H-score의 핵심 통찰이다.

---

**Q4: Network propagation에서 alpha=0.01로 매우 낮은 값을 사용한 이유는?**

**A**: alpha는 restart probability로, 각 반복에서 시드 유전자로 돌아가는 비율을 결정한다. alpha=0.01은 매 반복에서 자원의 1%만 시드로 복귀하고, 99%는 이웃 노드로 전파된다는 의미이다.

낮은 alpha를 선택한 이유는 **바이러스 유전자(시드)의 영향이 인간 유전자 네트워크 전체에 충분히 퍼지도록** 하기 위해서이다. 바이러스-인간 상호작용은 직접적인 PPI 외에도 간접적 경로(indirect pathway)를 통해 광범위한 면역 반응을 유도한다. alpha가 높으면 시드 유전자 근처에만 영향이 집중되어 간접 효과를 포착하지 못한다.

실제로 이 설정에서 상위 100개 영향 유전자를 선택한 결과, MMS에서는 체액면역(humoral immunity), SMS에서는 NK 세포 세포독성(cytotoxicity)이라는 생물학적으로 일관된 GO term이 농축되었으며, 이는 alpha 선택의 타당성을 간접적으로 지지한다.

---

**Q5: Bootstrap testing에서 1,000회 반복이 충분한지, 그리고 랜덤 영역 선택 시 어떤 제약이 있었는가?**

**A**: 1,000회 반복은 p-value의 해상도를 0.001까지 제공하며, BH correction 후 significance level 0.05에서의 판별에는 충분하다. 만약 더 엄격한 threshold(예: 0.001)를 사용하거나 더 정밀한 p-value 추정이 필요하다면 10,000회 이상으로 확장할 수 있으나, 477개 핫스팟 각각에 대해 수행하므로 계산 비용과의 균형을 고려했다.

랜덤 영역 선택 시 핵심 제약은 **동일 크기(same size as the cluster)의 연속 게놈 영역**을 무작위로 추출한다는 것이다. 이는 핫스팟이 특정 크기의 연속 영역이라는 구조적 특성을 귀무가설에도 반영한다. 각 랜덤 영역에서 변이 수, 평균 H-score, H-score 합의 3가지 통계량을 동시에 비교하여, 단일 지표에 의한 false positive를 줄였다.

---

### 비판적 질문 (Critical Questions)

---

**Q6: 387명 코호트에서 severe 42명은 통계적으로 충분한가? Selection bias는 없는가?**

**A**: Severe 42명이 상대적으로 소규모인 것은 사실이며, 이는 본 연구의 인정하는 한계이다. 그러나 다음 관점에서 타당성을 주장할 수 있다:

1. **임상 분포 반영**: 한국 COVID-19 환자 중 중증 비율은 실제로 약 10% 수준이며, 345:42 비율은 이를 반영
2. **KDCA 코호트의 포괄성**: 한국에서 가장 포괄적인 multi-omics COVID-19 데이터셋으로, EHR, 사이토카인, scRNA-seq, HLA, 바이러스 서열을 모두 포함
3. **통계적 보완**: FDR correction(BH), bootstrap testing(1,000회), 계층적 클러스터링을 통한 다단계 검증
4. **Selection bias**: 3개 병원에서 수집하여 단일 기관 편향을 줄였으나, 한국 인구의 유전적 동질성(homogeneity)에 의한 generalizability 제한은 존재

한계를 인정하며, 더 큰 다국적 코호트에서의 재현성 검증이 바람직하다. 특히 HLA 분석은 213명으로 더 축소되므로, HLA 다양성이 높은 인구에서의 추가 검증이 필요하다.

---

**Q7: NK 세포 기능 이상 발견은 correlation인가 causation인가? 이를 어떻게 구분하는가?**

**A**: 현재 수준은 **correlation**(상관관계)이며, 논문에서도 이를 명확히 인정하고 있다. Fig. 7은 "hypothesis-driven conceptual model"로 명시되어 있으며, 직접적 실험 증거에 기반하지 않는다.

다만, 단순한 correlation을 넘어서는 근거들이 있다:
1. **다층적 일관성**: Network propagation(단백질 상호작용), DEG(전사체), 사이토카인(단백질체), HLA(면역유전학) -- 독립적인 4가지 분석에서 일관된 패턴
2. **메커니즘적 가설**: c315 변이 → HLA 에피토프 친화도 감소 → APC의 에피토프 제시 변화 → NK 억제 신호 감소 → 과활성화라는 구체적 경로 제안
3. **기존 문헌과의 정합성**: 중증 환자에서 adaptive-like NK 세포 축적, NKG2C 상승, KIR 감소 보고와 일치

Causation 입증을 위해 필요한 실험: (1) HLA-binding assay로 변이 에피토프의 친화도 변화 직접 측정, (2) peptide processing validation으로 항원 처리 과정 확인, (3) NK cell cytotoxicity test로 c315 변이 조건에서의 NK 기능 직접 평가.

---

**Q8: MutClust가 477개 핫스팟을 탐지했는데, 이 중 대부분이 false positive일 가능성은 없는가?**

**A**: False positive 우려에 대해 다음과 같은 검증이 수행되었다:

1. **기능적 변이 검증**: 알려진 10개 기능적 변이 중 9개가 핫스팟 내 포함 -- 높은 sensitivity
2. **Bootstrap testing**: 477개 핫스팟 각각에 대해 1,000회 랜덤 샘플링 후 BH correction -- 통계적으로 유의미한 클러스터만 유지
3. **Severity 연관 검증**: 477개 중 28개만 severity와 유의미한 연관(FDR corrected) -- 선별적
4. **생물학적 해석**: 28개 중 c315, c442가 MMS vs SMS를 구분하는 핵심 요인으로 작동 -- 기능적 의미 확인

그러나 477개 모두가 생물학적으로 중요하다고 주장하는 것은 아니다. 핫스팟은 "변이 빈도와 다양성이 동시에 높은 영역"을 의미하며, 모든 핫스팟이 반드시 phenotypic effect를 가지는 것은 아니다. 28개의 severity-related 핫스팟이 임상적으로 가장 관련성 높은 부분집합이다.

---

**Q9: 인플루엔자 검증에서 SARS-CoV-2와 동일한 파라미터를 사용한 것이 적절한가?**

**A**: 이는 의도적인 실험 설계이다. 동일 파라미터 사용의 목적은 **MutClust의 범용성(generalizability)을 가장 보수적으로 테스트**하기 위해서이다.

인플루엔자 게놈은 SARS-CoV-2의 약 1/10 크기(~2,300 bp vs ~30,000 bp)이므로, gamma=10은 상대적으로 넓은 반경을 할당하게 된다. 그럼에도 D222G(고사망률), T123V(중증), E627K(조류-인간 적응), K338R(병원성 증가) 등 알려진 임상적 변이를 포함하는 핫스팟을 탐지하는 데 성공했다.

이는 MutClust가 **파라미터에 과도하게 민감하지 않다**(robustness)는 긍정적 증거이다. 동시에, 최적 성능을 위해서는 게놈 특성에 맞는 파라미터 조정이 필요하다는 한계도 인정한다. 이것이 향후 연구에서 k-dist 기반 adaptive parameter selection을 개발하려는 동기이다.

---

**Q10: H-score가 정말 빈도와 다양성을 "동시에" 반영하는가? P_i가 매우 높고 E_i가 매우 낮은 경우(또는 그 반대)에도 H-score가 적절한 값을 보이는가?**

**A**: H-score = log_2(P_i * E_i * 100 + 1)에서 곱셈(P_i * E_i)은 두 요소 중 하나라도 낮으면 전체 H-score가 낮아지는 구조이다. 이는 의도된 설계이다.

**경우 1: P_i 높음 + E_i 낮음 (빈도 높고 다양성 낮음)**
- 예: Lineage-defining mutation -- 거의 모든 서열에서 동일한 단일 변이
- P_i * E_i가 작아져 H-score 낮음 → lineage bias에 의한 과대평가 방지

**경우 2: P_i 낮음 + E_i 높음 (빈도 낮고 다양성 높음)**
- 예: 극히 드물지만 다양한 변이가 발생하는 위치
- P_i * E_i가 작아져 H-score 낮음 → 노이즈 위치 필터링

**경우 3: P_i 중간 + E_i 중간 (빈도와 다양성 모두 적절)**
- 예: c315, c442 같은 severity-related 변이
- P_i * E_i가 적절한 값 → 중간 수준의 H-score → 다른 핫스팟과 구별 가능

이 특성이 c315가 mutation entropy 기준 H-score 2.3 percentile(nucleotide entropy 기준 99.8%)에 위치하는 이유이다. 곱셈 구조는 "빈도만 높은 변이"와 "다양성만 높은 변이"를 모두 걸러내는 AND 조건으로 작동하며, 이는 severity와 연관된 변이의 특성(중간 빈도 + 적절한 다양성)을 포착하는 데 효과적이다.

---
