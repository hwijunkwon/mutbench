# Paper Tools Implementation Design

## Overview

두 논문(MOSD, MutClust)의 핵심 알고리즘/도구를 Python CLI 도구로 구현한다.

## Scope

### 논문1 (MOSD) - 6개 도구
1. **cluster_score**: ARI + NMI + F-measure 통합 점수 계산
2. **feature_selection**: Chi-square/ANOVA 기반 특성 선택
3. **preprocessing**: RAW/NORM/GL 전처리 파이프라인
4. **benchmark**: 7가지 벤치마크 테스트 러너
5. **moi_methods**: 10개 MOI 방법 래퍼 (SNF, Spectrum, PINSPlus, COCA, LRAcluster, CC, MOFA, NEMO, IntNMF, iClusterPlus)

### 논문2 (MutClust) - 6개 도구
1. **hscore**: H-score 계산기 (mutation frequency x mutation entropy)
2. **mutclust_algo**: MutClust 적응형 밀도 클러스터링 알고리즘
3. **bootstrap**: Bootstrap 유의성 검정 (1,000회 반복)
4. **network_propagation**: PPI 네트워크 기반 유전자 영향도 전파
5. **deg_analysis**: Differential Expression Gene 분석
6. **hla_affinity**: HLA-에피토프 결합 친화도 분석

## Architecture

```
/proj/paper/
├── docs/                          # 문서 정리
│   ├── mosd/                      # MOSD 논문 관련 문서
│   ├── mutclust/                  # MutClust 논문 관련 문서
│   ├── figures/                   # 그림 파일
│   ├── presentation/              # 발표 자료
│   └── plans/                     # 설계 문서
│
├── tools/
│   ├── common/                    # 공유 유틸리티
│   │   ├── __init__.py
│   │   ├── metrics.py             # ARI, NMI, F-measure 계산
│   │   ├── stats.py               # BH correction, bootstrap 등
│   │   └── io_utils.py            # 데이터 I/O 헬퍼
│   │
│   ├── mosd/                      # 논문1 도구
│   │   ├── cluster_score/
│   │   │   ├── __init__.py
│   │   │   ├── __main__.py        # CLI 진입점
│   │   │   └── core.py            # 핵심 로직
│   │   ├── feature_selection/
│   │   │   ├── __init__.py
│   │   │   ├── __main__.py
│   │   │   └── core.py
│   │   ├── preprocessing/
│   │   │   ├── __init__.py
│   │   │   ├── __main__.py
│   │   │   └── core.py
│   │   ├── benchmark/
│   │   │   ├── __init__.py
│   │   │   ├── __main__.py
│   │   │   └── core.py
│   │   └── moi_methods/
│   │       ├── __init__.py
│   │       ├── __main__.py
│   │       ├── snf.py
│   │       ├── spectrum.py
│   │       ├── pinsplus.py
│   │       ├── coca.py
│   │       ├── lracluster.py
│   │       ├── consensus_clustering.py
│   │       ├── mofa.py
│   │       ├── nemo.py
│   │       ├── intnmf.py
│   │       └── iclusterplus.py
│   │
│   └── mutclust/                  # 논문2 도구
│       ├── hscore/
│       │   ├── __init__.py
│       │   ├── __main__.py
│       │   └── core.py
│       ├── mutclust_algo/
│       │   ├── __init__.py
│       │   ├── __main__.py
│       │   └── core.py
│       ├── bootstrap/
│       │   ├── __init__.py
│       │   ├── __main__.py
│       │   └── core.py
│       ├── network_propagation/
│       │   ├── __init__.py
│       │   ├── __main__.py
│       │   └── core.py
│       ├── deg_analysis/
│       │   ├── __init__.py
│       │   ├── __main__.py
│       │   └── core.py
│       └── hla_affinity/
│           ├── __init__.py
│           ├── __main__.py
│           └── core.py
│
└── requirements.txt
```

## Tech Stack

- **Language**: Python 3.10+
- **Core**: numpy, scipy, pandas, scikit-learn
- **Bio**: biopython (FASTA 파싱), networkx (네트워크 분석)
- **Stats**: statsmodels (다중 검정 보정)
- **CLI**: argparse (표준 라이브러리)
- **Clustering**: scikit-learn, snfpy (SNF Python 구현)

## CLI Interface

각 도구는 `python -m tools.<paper>.<tool>` 형태로 실행:

```bash
# MOSD
python -m tools.mosd.cluster_score --pred pred.csv --true true.csv
python -m tools.mosd.feature_selection --input data.csv --method chi2 --top-pct 10
python -m tools.mosd.preprocessing --input data.csv --strategy NORM --output out.csv
python -m tools.mosd.benchmark --test sample_size --data-dir ./data/ --repeats 10
python -m tools.mosd.moi_methods --method SNF --input data.csv --k 3

# MutClust
python -m tools.mutclust.hscore --input aligned.fasta --ref reference.fasta --output hscores.csv
python -m tools.mutclust.mutclust_algo --input hscores.csv --gamma 10 --d 3 --minpts 5
python -m tools.mutclust.bootstrap --clusters hotspots.csv --genome-size 29903 --n-iter 1000
python -m tools.mutclust.network_propagation --seeds seeds.txt --network ppi.txt --alpha 0.01
python -m tools.mutclust.deg_analysis --counts counts.csv --groups groups.csv --fdr 0.05
python -m tools.mutclust.hla_affinity --epitopes epitopes.csv --hla-alleles alleles.txt
```

## Team Structure (Claude Team Code)

- **Lead**: 전체 조율, 공통 모듈, 문서 정리
- **mosd-dev**: MOSD 6개 도구 구현 (worktree 격리)
- **mutclust-dev**: MutClust 6개 도구 구현 (worktree 격리)

## Key Algorithms

### H-score (MutClust)
```
H_i = log2(P_i * E_i * 100 + 1)
- P_i = sum of mutation ratios at position i
- E_i = Shannon entropy of mutation types (conditional on mutation)
```

### MutClust Clustering
```
1. Compute Deps_CCM = ceil(gamma * H_i) for each position
2. Identify CCM positions (4 conditions: H>0.03, mean>0.01, sum>0.05, count>MinPts)
3. Expand clusters bidirectionally with diminishing factor d
```

### Cluster-score (MOSD)
```
cluster_score = (ARI + NMI + F_measure) / 3
```

### Network Propagation
```
p^(t+1) = (1-alpha) * W * p^t + alpha * p_0
- alpha=0.01, W=normalized adjacency matrix
- Converge until ||p^(t+1) - p^t|| < threshold
```
