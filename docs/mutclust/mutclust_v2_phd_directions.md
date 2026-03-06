# MutClust v2 PhD 연구 방향 종합 분석

> 기존 개선 방향(HDBSCAN, 계통 보정, 상위성, dN/dS) 외 추가 연구 방향

---

## 추가 연구 방향 10가지 요약

| # | 방향 | 신규성 | 실현가능성 | 출판가치 | 추천도 |
|---|------|--------|-----------|----------|--------|
| 1 | 시간적 동역학 / 실시간 감시 | ★★★ | ★★★★ | ★★★★ | **최우선** |
| 2 | 범병원체 일반화 | ★★★ | ★★★★ | ★★★★ | **최우선** |
| 3 | 그래프/네트워크 기반 접근 | ★★★★ | ★★★ | ★★★★ | 높음 |
| 4 | 해석 가능한 ML 브리징 | ★★★ | ★★★ | ★★★★ | 높음 |
| 5 | 벤치마크 프레임워크 | ★★★★★ | ★★★★★ | ★★★★ | **최우선** |
| 6 | 인과 추론 | ★★★★★ | ★★ | ★★★★★ | 선택 |
| 7 | 하수 유전체학 통합 | ★★★ | ★★★ | ★★★ | 보통 |
| 8 | 재조합 인식 분석 | ★★★★ | ★★★ | ★★★★ | 높음 |
| 9 | 면역 환경 통합 | ★★★ | ★★★ | ★★★★★ | 높음 |
| 10 | One Health / 인수공통 전파 | ★★★ | ★★★ | ★★★★ | 보통 |

---

## 1. 시간적 동역학 / 실시간 감시

**핵심**: MutClust를 정적 분석에서 시계열 분석으로 확장. Emerging hotspot 조기 탐지.

- IncGridDBC (2025): 스트리밍 DBSCAN, 60배 빠른 속도
- VirusWarn (2025): mutation 기반 조기 경보 시스템
- VIRUS-MVP: 실시간 변이 기능 영향 감시
- **논문 아이디어**: "Temporal MutClust: Streaming Density-Based Detection of Emerging Mutation Hotspots"
- **대상 저널**: Bioinformatics, PLOS Computational Biology, Virus Evolution

## 2. 범병원체 일반화

**핵심**: SARS-CoV-2 전용 → influenza, HIV, Mpox, H5N1 등 범용 프레임워크

- H5N1 유행 (2024-2025)으로 시의성 매우 높음
- 게놈 유형별(비분절 RNA, 분절 RNA, DNA) 파라미터 자동 조정
- TreeSort (MBE, 2025): influenza reassortment 분석
- **논문 아이디어**: "Universal Mutation Hotspot Detection Across Pathogen Genome Types"
- **대상 저널**: Genome Biology, Nucleic Acids Research, Virus Evolution

## 3. 그래프/네트워크 기반 접근

**핵심**: 1D 좌표 → mutation co-occurrence network, 커뮤니티 탐지

- Mazzocchetti et al. (Nat Comm, 2024): coordinated substitution network
- Matrix factorization 기반 co-mutation 탐지 (PLOS Comp Bio, 2024)
- **논문 아이디어**: "From Linear Density to Network Topology: Mutation Co-occurrence Networks for Hotspot Detection"
- **대상 저널**: Nature Communications, PLOS Computational Biology

## 4. 해석 가능한 ML 브리징

**핵심**: MutClust의 해석 가능성 + 딥러닝 예측력 결합. SHAP/attention 기반.

- EVEscape (Nature, 2023), CoVFit (Nat Comm, 2025)
- Causal SHAP (arXiv, 2025)
- **논문 아이디어**: "Bridging Statistical Rigor and Deep Learning: Interpretable ML for Mutation Hotspot Functional Annotation"
- **대상 저널**: Briefings in Bioinformatics, Nature Machine Intelligence

## 5. 벤치마크 프레임워크

**핵심**: 핫스팟 탐지 방법의 표준 벤치마크가 **현재 존재하지 않음** → 큰 연구 공백

- 시뮬레이션 기반 ground-truth 데이터셋 생성
- MutClust vs Shannon entropy vs 빈도 기반 등 체계적 비교
- GENOMICON-Seq (2025), PySNV (2024) 참고
- **논문 아이디어**: "MutBench: A Simulation and Benchmarking Framework for Viral Mutation Hotspot Detection"
- **대상 저널**: Genome Biology, Bioinformatics, GigaScience

## 6. 인과 추론

**핵심**: 핫스팟-표현형 상관관계 → 인과관계. 반사실적(counterfactual) 분석.

- 바이러스 유전학의 인과 추론은 거의 미개척
- Deep Mutational Scanning 데이터를 "intervention"으로 활용
- **논문 아이디어**: "Beyond Correlation: Causal Inference for Linking Mutation Hotspots to Viral Phenotypic Changes"
- **대상 저널**: Nature Methods, PNAS (난이도 높지만 임팩트 최고)

## 7. 하수 유전체학 통합

**핵심**: 임상 + 하수 감시 데이터 통합, 인구 수준 핫스팟 동역학

- LolliPop (PLOS Comp Bio, 2025), Aquascope (CDC)
- 혼합 시료 deconvolution 후 MutClust 적용
- **논문 아이디어**: "Integrating Clinical and Wastewater Genomic Data for Population-Level Hotspot Surveillance"
- **대상 저널**: Genome Biology, Water Research

## 8. 재조합 인식 분석

**핵심**: 재조합 breakpoint 근처의 false positive 핫스팟 필터링

- RecombinHunt (Nat Comm, 2024), sc2ts (2025)
- XBB, XE 등 재조합체 핫스팟 아티팩트 문제
- **논문 아이디어**: "Recombination-Aware Hotspot Detection: Disentangling Selection from Recombination Artifacts"
- **대상 저널**: Virus Evolution, Molecular Biology and Evolution

## 9. 면역 환경 통합

**핵심**: 인구 면역 이력(백신, 자연감염)이 핫스팟 출현에 미치는 영향

- Nature (2025): SARS-CoV-2 evolution on dynamic immune landscape
- EvoScape (2025): AUROC 0.891로 EVEscape 0.669 대비 크게 개선
- DMS 데이터와 핫스팟의 기능적 해석
- **논문 아이디어**: "Immune-Driven Mutation Hotspot Dynamics in SARS-CoV-2"
- **대상 저널**: Nature Communications, Cell

## 10. One Health / 인수공통 전파

**핵심**: 동물-인간 간 cross-species 핫스팟 비교, spillover 위험 예측

- BERT-infect (2025): 26개 바이러스 과 spillover 위험 평가
- H5N1 PB2 M631L (Nat Comm, 2025): 조류-포유류 적응 핵심 돌연변이
- **논문 아이디어**: "Cross-Species Mutation Hotspot Analysis for Predicting Zoonotic Spillover Risk"
- **대상 저널**: Nature, The Lancet Microbe

---

## PhD 논문 구조 제안 (4편 논문)

### 논문 1: MutClust v2 핵심 알고리즘 + 벤치마크
- HDBSCAN 자동 파라미터 + 계통 보정 + dN/dS 통합
- MutBench 시뮬레이션 벤치마크 프레임워크
- **대상**: Bioinformatics / Genome Biology
- **기간**: ~1년

### 논문 2: 시간적 확장 + 네트워크 통합
- Temporal MutClust (incremental DBSCAN)
- Co-occurrence network + emerging hotspot 조기 탐지
- **대상**: PLOS Computational Biology / Nature Communications
- **기간**: 1~1.5년

### 논문 3: 범병원체 일반화 + 재조합 인식
- SARS-CoV-2, Influenza, H5N1, Mpox 범용 프레임워크
- 재조합 아티팩트 필터링
- **대상**: Virus Evolution / Nucleic Acids Research
- **기간**: 1~1.5년

### 논문 4: 면역 환경 통합 + 해석 가능한 ML
- DMS 데이터 기반 핫스팟 기능 해석
- 면역 선택 압력 하의 핫스팟 진화 예측
- **대상**: Nature Communications / Briefings in Bioinformatics
- **기간**: 1.5~2년
