# PhD Presentation v8 — 콘텐츠 검토 리포트

**검토 일시**: 2026-03-05
**대상 파일**: `PhD_Presentation_v8_EN.pptx` (21 slides)
**검토 방법**: 3개 병렬 에이전트 (MOSD PDF 대조, MutClust PDF 대조, 내러티브/스크립트 품질)

---

## 1. CRITICAL — 반드시 수정

### 1-1. 슬라이드 6 (Prior Work) — 요인 커버리지 수치 불일치

**현재 상태**: 각 선행연구의 Computational(6개)/Biological(3개) 요인 커버리지를 표시하고 있으나, 논문(MOSD Playbook)과 수치가 일치하지 않음.

| 연구 | 슬라이드 표기 (Comp) | 논문 실제 | 슬라이드 표기 (Bio) | 논문 실제 |
|------|---------------------|----------|---------------------|----------|
| Rappoport 2018 | 0/6 | ~4-5/6 (sample size, preprocessing 등 분석) | 2/3 | 2/3 |
| Chauvel 2020 | 2/6 | 2/6 | 0/3 | 3/3 (cancer subtype 포함) |

**위험**: 심사위원이 논문을 읽고 왔을 경우 즉시 지적 가능.
**권장**: 논문 Table 1 기준으로 수치 재검증 후 수정.

---

### 1-2. 슬라이드 18 (Influenza Validation) — E627K 바이러스 귀속 오류

**현재 상태**: E627K 변이를 "H2N2"와 연결하여 표시.
**문제**: 분석 대상 바이러스는 **H1N1, H3N2, B/Victoria** 3종이며 H2N2는 포함되지 않음.
E627K(PB2 segment)는 **B/Victoria**에서 검출됨.

**위험**: 바이러스학 전공 심사위원이 있을 경우 신뢰도 하락.
**권장**: "B/Victoria" 카드의 E627K 설명에서 바이러스명 정정.

---

## 2. HIGH — 강력 권장

### 2-1. 슬라이드 17 (Severity) — SMS/MMS 약어 미정의

**현재 상태**: "SMS avg 7.04 vs MMS avg 0.24" 등 SMS/MMS가 핵심 비교 지표로 사용되나, 어디에서도 정의되지 않음.

- SMS = Severe Mutation Signature
- MMS = Moderate Mutation Signature

**권장**: 슬라이드 17 또는 12(Background)에서 약어 정의 추가. 스크립트에서도 첫 언급 시 풀어서 설명.

---

### 2-2. 슬라이드 9 (Guidelines) — PINSPlus 80% noise 표현 오해 소지

**현재 상태**: "PINSPlus maintains performance at 80% noise"로 표현.
**논문 원문**: 80% noise level에서는 **모든 방법이 실패**한다고 기술. PINSPlus가 가장 robust하다는 의미이나, 현재 표현은 "80%에서도 잘 작동한다"는 인상을 줌.

**권장**: "PINSPlus shows highest noise robustness (last to degrade)" 등으로 수정하거나, 스크립트에서 "80%에서는 모든 방법이 실패하지만, PINSPlus가 가장 늦게 성능이 떨어집니다"로 보충.

---

### 2-3. 슬라이드 18 (Influenza) — Bootstrap/BH 보정 대상 혼동

**현재 상태**: 477개 hotspot 전체에 대한 BH 보정으로 설명될 여지 있음.
**논문 원문**: Bootstrap resampling + BH correction은 **28개 severity-linked hotspot**에 대해 수행됨.

**권장**: 슬라이드/스크립트에서 "28개 severity hotspot에 대한 통계적 검증" 명시.

---

### 2-4. 스크립트 — 총 발표 시간 초과

**현재 배분 합계**: ~22분 10초
**목표**: 20분

| 구간 | 현재 | 비고 |
|------|------|------|
| S1–S3 (도입) | ~3분 | |
| S4–S10 (Paper 1) | ~8분 | |
| S11–S19 (Paper 2) | ~9분 | 인플루엔자 슬라이드 추가로 증가 |
| S20–S21 (결론) | ~2분10초 | |

**권장**: 각 슬라이드 스크립트에서 ~10초씩 단축하거나, Paper 1/2 각각 1분씩 축약.

---

## 3. MEDIUM — 권장

### 3-1. 슬라이드 3 (Terminology) — Epitope 미사용

**현재 상태**: 용어집에 Epitope를 정의했으나, 이후 어떤 슬라이드에서도 직접 사용되지 않음.

**권장**:
- (A) Terminology에서 Epitope 삭제, 또는
- (B) 슬라이드 17(Biological Significance)에서 "immune recognition disruption → epitope region 변이" 등으로 연결

---

### 3-2. 슬라이드 10→11 — Paper 전환 브릿지 부재

**현재 상태**: Paper 1 Summary(S10) → Paper 2 Cover(S11) 전환 시 맥락 연결 없음.

**권장 스크립트 추가**:
> "Paper 1에서 multi-omics 통합의 벤치마크 프레임워크를 구축했다면, Paper 2에서는 이를 실제 바이러스 변이 데이터에 적용하여 임상적 의미를 도출합니다."

---

### 3-3. 슬라이드 12/17 — KDCA 코호트 설명 부족

**현재 상태**: "KDCA 387-patient cohort"가 갑자기 등장. KDCA(질병관리청)가 무엇인지, 데이터를 어떻게 확보했는지 설명 없음.

**권장**: 스크립트에서 "질병관리청(KDCA)으로부터 제공받은 국내 COVID-19 환자 387명의 임상 데이터"로 한 줄 도입.

---

### 3-4. 슬라이드 17 — NK cell 모델 한계 미강조

**현재 상태**: 슬라이드에 "⚠ In silico; experimental validation needed" 한 줄 있으나, 심사에서 NK cell 메커니즘의 근거를 질문받을 가능성 높음.

**논문 원문**: "hypothesis-driven conceptual diagram" — 실험적 검증이 아닌 계산적 추론임을 명시.

**권장**: 스크립트에서 "이 NK cell 회피 메커니즘은 저희의 가설 기반 모델이며, 실험적 검증은 향후 과제입니다"로 강조.

---

### 3-5. 스크립트 전반 — 약어 미확장

첫 사용 시 풀어쓰기가 필요한 약어:

| 약어 | 풀어쓰기 | 첫 등장 |
|------|---------|---------|
| MOI | Multi-Omics Integration | S5 스크립트 |
| CCM | Consensus Clustering-based Method | S9 스크립트 |
| TCGA | The Cancer Genome Atlas | S5 스크립트 |
| SMS | Severe Mutation Signature | S17 스크립트 |
| MMS | Moderate Mutation Signature | S17 스크립트 |
| KDCA | Korea Disease Control and Prevention Agency | S12/17 스크립트 |

---

## 4. LOW — 선택적 개선

### 4-1. 슬라이드 5 — Feature 수치의 일반화

**현재 상태**: "60,660 mRNA, 485,577 methylation" 등 수치가 BLCA(방광암) 데이터셋 기준이나, 슬라이드에서 특정 암종 한정임이 명시되지 않아 일반적인 수치로 오해 가능.

**권장**: "(e.g., BLCA)" 또는 스크립트에서 "방광암 데이터를 예로 들면" 한 마디 추가.

---

### 4-2. 슬라이드 7 — Clinical Feature 순서

**현재 상태**: Clinical feature가 순서대로 나열되어 있어 hierarchy처럼 보이나, 논문에서는 명시적 우선순위를 제시하지 않음.

**권장**: 스크립트에서 "이 세 가지 임상적 요인을 동등하게 분석했습니다"로 명확화.

---

### 4-3. 스크립트 — 한국어 표현 개선

| 현재 | 권장 | 이유 |
|------|------|------|
| "삭제" (deletion 맥락) | "결실(deletion)" | 유전학 전문 용어 |
| "심각합니다" | "중대한 문제입니다" | 학술적 레지스터 |
| "엄청난" | "현저한" / "유의미한" | 구어체 → 학술적 |

---

## 요약

| 등급 | 건수 | 핵심 키워드 |
|------|------|------------|
| **CRITICAL** | 2 | S6 요인수치, S18 바이러스명 |
| **HIGH** | 4 | SMS/MMS 정의, PINSPlus 표현, BH 보정 대상, 시간 초과 |
| **MEDIUM** | 5 | Epitope, 전환 브릿지, KDCA 설명, NK cell 한계, 약어 |
| **LOW** | 3 | BLCA 명시, hierarchy 명확화, 한국어 표현 |

**총 14건** — Critical 2건과 High 4건을 우선 수정 권장.
