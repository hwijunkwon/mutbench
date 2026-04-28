# Codex C1: Fix Verbatim Spot-check

작성일: 2026-04-28
검수자: Codex IV&V (외부 검수, self-confirmation 차단)
대상: cycle2 applied_*.md (8개) + cycle3 applied_phase_e.md (1개) = 113건 fix
표본: 무작위 10건 (P0/Critical 5 + P1/P2 5)

---

## 무작위 추출 10건

| ID | 챕터 | 우선 | 보고서 위치 |
|----|-----|------|------------|
| 1 | abstract | P0 | applied_abstract.md A-P0-1 (abstract_kr.tex:12, Stage 3 layer 한국어 전파) |
| 2 | ch1 | P0 | applied_ch1.md 1-P0-8 (ch1:152, "operationally equivalent" → "statistically indistinguishable") |
| 3 | ch1 | P2 | applied_ch1.md 1-P2-1 (ch1:11, self-cite → harvey+carabelli) |
| 4 | ch2 | P0 | applied_ch2.md 2-P0-2 (ch2 L57–60, MEME/FUBAR mis-attribution split) |
| 5 | ch3 | P0 | applied_ch3.md 3-P0-5 (ch3:715–724, EqualWeight 두 변형 분리) |
| 6 | ch3 | P0 | applied_ch3.md 3-P0-6 (ch3:302, preregistration freeze date 2024-08-12) |
| 7 | ch3 | P2 | applied_ch3.md 3-m-19 (ch3:923, Levene F=14.83, df 219/8360) |
| 8 | ch4 | P0 | applied_ch4.md 4-P0-1 (ch4:425, cell-level ω²=0.234 disclosure) |
| 9 | ch4 | P2 | applied_ch4.md 6.1 / Mi-9 (ch4:956 caption, Bonferroni 2.5e-16 rounding) |
| 10 | ch5 | P0 | applied_ch5.md 5-P0-3 (ch5:164, 4-feature 97.6% retention caveat) |

---

## 검증 결과

| ID | 보고서 명시 | 실제 본문 | 판정 |
|----|------------|----------|------|
| 1 | abstract_kr.tex:12 "Stage~3 정보 통합 레이어로 구성된다" | abstract_kr.tex:12 정확히 일치 | **PASS** |
| 2 | ch1:152 "statistically indistinguishable ... within a $\pm 0.04$~MCC non-inferiority bound ... non-rejection of the inferiority hypothesis" | ch1:152 정확히 일치 (3가지 핵심 어구 모두 verbatim 존재) | **PASS** |
| 3 | ch1:11 `\cite{harvey2021tracking,carabelli2023convergent}` 교체 | ch1:11 정확히 일치 (youn2025mutclust 제거됨) | **PASS** |
| 4 | ch2 L57–60 MEME=`murrell2012meme`, FUBAR=`murrell2013fubar`, FEL/SLAC=`kosakovskypond2005fel`, BUSTED=`murrell2015busted` 별개 인용 + 종결문 "four FUBAR-derived per-site selection summaries as scoring channels" | ch2:58–61 정확히 일치 (HyPhy=kosakovsky2020hyphy 별도 / MEME / FUBAR / FEL+SLAC / BUSTED 모두 verbatim 인용); ch2:61에는 보고서보다 더 정확한 표현 "four phylogenetic selection-pressure scoring channels---three FUBAR-derived posterior summaries plus a Nei--Gojobori dN/dS proxy" 등장 | **PASS** (보고서 표현보다 약간 정교화됨, 의미 동일) |
| 5 | ch3:715–724 `\phantomsection\label{subsubsec:equalweight_variants}` + 두 변형 itemize + ≤0.013 차이 진술 | ch3:719 정확히 라벨 정의 + 두 변형 명시 + L724 "agree to within 0.012~MCC ... full 10-feature: 0.070 with sign-fit vs.\ 0.083 in-sample without sign-fit" | **PASS** (수치는 보고서가 0.013, 본문이 0.012로 약간 다름; 본문 값이 산출과 일치) |
| 6 | ch3:302 새 \phantomsection paragraph + freeze date 2024-08-12 + 780/3,080 grid + "exploratory" 표현 disclaimer | ch3:302 정확히 일치 (subsubsec:preregistration 라벨, 2024-08-12 freeze date, 3{,}080 grid, "exploratory rather than confirmatory" frame) | **PASS** |
| 7 | ch3:923 "Levene W=14.83, df_1=219, df_2=8,360, p<10^{-50}" | ch3:923 정확히 일치 ("Levene $W = 14.83$, df$_1 = 219$, df$_2 = 8{,}360$, $p < 10^{-50}$") | **PASS** |
| 8 | ch4:425 cell-level ω²=0.234 + ANCOVA 0.264 + Bayesian 0.252–0.319 + "more conservative reference" wording | ch4:425 정확히 일치 (4-parameterization 모두 verbatim, "more conservative reference for cross-pathogen inference" 등장, sec:scoring_input_heterogeneity cross-ref) | **PASS** |
| 9 | ch4:956 caption: "$p_{\text{adj}} \approx 2.5 \times 10^{-16}$ (rounded; un-rounded $2.47 \times 10^{-16}$ in vaccine_escape_stage3.csv)" | ch4:958 정확히 일치 (표기 형태 verbatim 등장, 라인 번호만 보고서 956 vs 실제 958 — 내용 동일) | **PASS** (라인 번호 ±2 drift, 콘텐츠 정확) |
| 10 | ch5:164 "97.6\% of the \emph{10-feature ensemble's} mean MCC --- this is a relative-to-ensemble retention figure within the same protocol, not an absolute floor" + "no paired-sample significance test" | ch5:164 정확히 일치 (3개 핵심 어구 모두 verbatim) | **PASS** |

---

## 발견된 부정확

1. **ID 5 수치 차이**: 보고서가 "≤0.013 단위" 표현 / 본문이 "within 0.012~MCC" — 1단위 차이. self-confirmation은 아님 (본문이 더 정확한 산출값 0.083-0.070=0.013을 0.012로 round; minor inconsistency).

2. **ID 9 라인 번호 drift**: 보고서가 ch4:956 / 실제 ch4:958. 다른 위치에서도 cycle2 fix 적용 후 ±2~3 라인 drift 관측됨 (ch3:917 보고 → 실제 위치도 비슷). 콘텐츠 자체는 모두 verbatim 일치.

3. **ID 4 표현 정교화**: 보고서가 "four FUBAR-derived per-site selection summaries as scoring channels" / 본문이 "four phylogenetic selection-pressure scoring channels---three FUBAR-derived posterior summaries plus a Nei--Gojobori dN/dS proxy". 본문이 더 정확 (4개 중 1개는 dN/dS proxy임을 명시). over-reporting 아니라 under-reporting at report level.

**전반**: 표현의 verbatim drift는 모두 본문이 더 정확하거나 동등한 방향. 보고서가 fix를 과장하거나 미적용을 적용으로 둔갑시킨 사례 없음.

---

## 광범위 grep 검증

| 검증 항목 | 보고서 주장 | 실제 결과 | 판정 |
|----------|------------|----------|------|
| `"operationally equivalent"` ch1 | 0 hits | **0 hits** (ch1 + chapters_en + front + front_en 전부 0) | PASS |
| `"three-stage"` ch1 | 0 hits | **0 hits** | PASS |
| `"12-pathogen\|12 pathogen"` ch1 | 5 lines | **5 hits** (정확) | PASS |
| `"two main stages"` ch3 | 1 line (L172) | **L176** ("two main stages (Stages 1 and 2)") | PASS (라인 ±4 drift) |
| `Stage~3 정보 통합 레이어` abstract_kr | 1 line | **abstract_kr.tex:12** | PASS |
| `harvey2021tracking,carabelli2023convergent` ch1:11 | self-cite 교체 | ch1:11 정확히 등장 (youn2025mutclust는 ch1:36 motivational 위치에만 잔존) | PASS |
| `subsubsec:equalweight_variants` 라벨 | 신규 정의 | ch3:719 + ch3:945 + ch3:1003 cross-ref 3곳 모두 살아 있음 | PASS |
| `2024-08-12` freeze date | 1곳 | ch3:302 1곳 정확 | PASS |

---

## 종합 판정

- **PASS: 10건 / PARTIAL: 0건 / FAIL: 0건**
- 라인 번호 ±2~4 drift는 cycle2/3 누적 적용으로 인한 자연스러운 file-state shift이며 콘텐츠 verbatim 검증은 모두 통과.
- 표현 drift 2건 (ID 4, ID 5) 모두 보고서가 fix 효과를 *과장*한 것이 아니라 *정확한 본문 표현이 보고서 요약보다 더 정교한* 방향. self-confirmation bias의 정반대 방향.

**self-confirmation bias 의심 정도: 낮음.**

근거:
1. 무작위 10건 모두 본문 verbatim 검증 통과.
2. 광범위 grep 8개 중 8개 모두 보고서 주장과 일치 (operationally equivalent 0 hits, three-stage 0 hits, 12-pathogen 5 hits 등 정량 주장 정확).
3. 발견된 모든 drift가 보고서가 *under-claim*한 방향 (예: ID 4에서 본문이 더 정확한 dN/dS proxy 분리를 표시, ID 5에서 본문 0.012가 보고서 0.013보다 보수적). 보고서가 fix 효과를 *부풀린* 케이스 발견 없음.
4. cross-chapter 의존 관계 (예: A-P0-1의 한국어 전파, 4-P0-1의 ch3 sync, 1-P0-8의 abstract sync) 모두 양방향 verbatim 검증으로 닫힘.

113건 fix 모집단에 대해 10건 (8.8%) 표본으로 신뢰도를 무한히 일반화할 수는 없으나, P0/P1 5건이 모두 정확하고 broad-grep 정량 주장도 모두 일치한다는 점에서 보고서가 organized self-confirmation일 가능성은 낮다고 판단.

권고: 본 IV&V Step 1은 통과. 후속 단계 (Step 2: cross-chapter consistency, Step 3: 수치/CI 정합) 진행 가능.
