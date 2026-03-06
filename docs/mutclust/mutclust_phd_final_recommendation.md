# MutClust PhD 최종 추천: 범병원체 핫스팟 탐지 프레임워크

---

## 최종 추천: 범병원체 일반화 (핵심 알고리즘 개선 포함)

### 한 문장 요약
> "큰 팀이 하지 않는 빈 공간에서, 공개 데이터로, 시의적절한 문제를, GPU 없이 풀 수 있는 유일한 방향"

---

## 왜 이것인가?

### 1. 경쟁 안전성 최고
- "범용 바이러스 핫스팟 탐지 프레임워크"라는 니치에 **아무도 없음**
- Nextstrain: 병원체별 별도 분석
- PLM 도구들(ESM, EVEscape): 개별 바이러스 적합도 예측에 집중
- ESM-2조차 "WHO 우선순위 40개 팬데믹 위협 바이러스 중 절반 이상에서 신뢰할 수 없는 예측" (bioRxiv, 2025)

### 2. 데이터 완전 무료 접근
- SARS-CoV-2: NCBI GenBank (수백만 서열)
- H5N1: USDA가 2024년부터 NCBI에 적극 공개
- Mpox: NCBI GenBank + BV-BRC
- Influenza: NCBI Influenza Virus Database
- **GISAID 의존 불필요** (2025년 10월 Nextstrain에 데이터 제공 중단 사태)

### 3. 시의성 최강
- H5N1: 2024-2025 미국 낙농업 대유행, 70건+ 인체 감염
- WHO Global Genomic Surveillance Strategy 2022-2032: 범병원체 감시 명시적 요구
- "팬데믹 대비(pandemic preparedness)"가 현재 최강 연구비 서사

### 4. SARS-CoV-2 관심 소멸 회피
- COVID 논문 비율: 2021년 4.7% → 2024년 1.9% 급감
- H5N1/Mpox로 다각화 시 졸업 시점(2028-2029)까지 시의성 유지

### 5. 알고리즘 개선을 자연스럽게 포함
- 범병원체 확장 위해 HDBSCAN, 자동 파라미터, 계통 보정이 **필수**
- 재조합 인식(Influenza reassortment, XBB 등)도 자연 포함

### 6. GPU 불필요
- 밀도 기반 클러스터링은 CPU로 충분
- 한국연구재단 과제 서버, KOBIC 활용 가능

---

## 다른 방향을 추천하지 않는 이유

| 방향 | 핵심 문제 |
|------|----------|
| 실시간 감시 | CoVerage, PETRA, TEMPO 등 **대형 팀이 이미 선점**. GISAID 데이터 불안정. |
| 해석 가능한 ML | Meta(ESM), Harvard(EVEscape), DeepMind(AlphaGenome)와 **경쟁 불가**. GPU 필요. |
| 네트워크 접근 | Mazzocchetti(Nat Comm, 2024)가 선점. 열린 문제가 너무 많아 범위 통제 어려움. |
| 면역 환경 | 인구 면역 데이터 비공개. 다학제적 전문성 부족 위험. |
| 재조합 인식 | 단독으로 박사논문 채우기에 범위가 너무 좁음. |
| 핵심 알고리즘만 | "so what?" 질문에 약함. 과학적 질문이 아닌 공학적 개선. |

---

## 논문 구조 (3편, 2.5년)

### 논문 1 (Year 1): MutClust v2 + 벤치마크
**"MutBench: A Benchmarking Framework for Viral Mutation Hotspot Detection"**
- HDBSCAN 자동 파라미터 + 계통 보정 + dN/dS 통합
- 시뮬레이션 기반 ground-truth 생성
- 기존 방법 체계적 비교 (원본 MutClust, Shannon entropy, 빈도 기반, 슬라이딩 윈도우)
- **대상**: Bioinformatics / GigaScience
- **기간**: 6-9개월

### 논문 2 (Year 1.5-2): 범병원체 프레임워크
**"Universal Mutation Hotspot Detection Across Diverse Pathogen Genome Architectures"**
- 4개 병원체: SARS-CoV-2 / Influenza A / H5N1 / Mpox
- 게놈 유형별 차이 처리:
  - 비분절 RNA (~30kb): SARS-CoV-2
  - 분절 RNA (~13.5kb): Influenza, H5N1 (reassortment 처리)
  - DNA (~197kb): Mpox (APOBEC3 편집 보정)
- 병원체 간 핫스팟 패턴 비교 분석
- **대상**: Genome Biology / Nucleic Acids Research
- **기간**: 12개월

### 논문 3 (Year 2-2.5): 차기 아웃브레이크 적용
**"Rapid Hotspot Characterization for Emerging Pathogens"**
- 프레임워크의 실전 적용 (차기 아웃브레이크 또는 H5N1 심화)
- DMS 데이터 통합으로 핫스팟 기능 해석
- "새로운 위협에 즉시 적용 가능" 입증
- **대상**: Nature Communications / Virus Evolution
- **기간**: 12개월

---

## 박사논문 통합 서사

> "바이러스 변이 핫스팟은 바이러스 진화의 핵심 메커니즘이지만, 기존 탐지 방법은
> 단일 병원체에 특화되어 있고 체계적 비교 프레임워크가 부재했다. 본 연구에서는
> (1) 밀도 기반 핫스팟 탐지의 첫 번째 벤치마크 프레임워크를 구축하고,
> (2) RNA/DNA 바이러스의 다양한 게놈 구조에 자동 적응하는 범용 탐지 알고리즘을 개발하며,
> (3) 이를 실제 아웃브레이크에 적용하여 팬데믹 대비 도구로서의 실용성을 입증했다."

---

## 위험 요소 및 대응

| 위험 | 대응 |
|------|------|
| 누군가 범병원체 프레임워크 선발표 | Paper 1(벤치마크)을 빠르게 발표하여 선점 |
| MutClust 원저자가 v2 발표 | 벤치마크 + 범병원체 확장은 원저자와 다른 방향 |
| SARS-CoV-2 관심 소멸 | H5N1/Mpox로 다각화 완료 |
| "단순 확장" 평가 위험 | 게놈 유형별 근본적 차이(분절/비분절, RNA/DNA, APOBEC3) 강조 |

---

## 참고 문헌
- [ESM viral prediction limitations](https://www.biorxiv.org/content/10.1101/2025.08.04.668549v3.full)
- [GISAID data controversy](https://nextstrain.org/blog/2025-11-06-gisaid-based-ncov-analyses)
- [H5N1 sequences at NCBI](https://ncbiinsights.ncbi.nlm.nih.gov/2025/01/08/avian-influenza-a-h5n1-virus-sequences-from-ncbi/)
- [Mpox mutation landscape](https://www.biorxiv.org/content/10.1101/2024.09.19.613877v1.full)
- [COVID research decline](https://jamanetwork.com/journals/jama/fullarticle/2837354)
- [WHO Genomic Surveillance Strategy](https://www.who.int/initiatives/genomic-surveillance-strategy)
