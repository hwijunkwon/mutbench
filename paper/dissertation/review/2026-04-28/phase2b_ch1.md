# Ch1 Introduction 심층 검토

대상: `/proj/paper/paper/dissertation/chapters_en/ch1_introduction.tex` (171 lines)
검토 일자: 2026-04-28
검토자: Phase 2B Adversarial Agent

---

## Critical (논문 합격 차단)

| ID | 위치 (라인) | 문제 | 근거 | 수정 제안 |
|----|------------|------|------|----------|
| C1 | L150 | **HIV-1 novel-only Bonferroni p값 불일치.** Ch1은 novel-only 7.16-8.24×에 대해 "Bonferroni-adjusted $p_{\text{adj}} \approx 3.9 \times 10^{-9}$ across 780 combinations"으로 기술. 그러나 ch4 Table tab:vaccine_escape_stage3 캡션 (L886)은 HIV-1 Bonferroni-adjusted = $2.47 \times 10^{-16}$ (full 7.19× 기준), abstract L2도 동일하게 "$2.5 \times 10^{-16}$"로 표기. Ch1은 novel-only에 별도의 Bonferroni 값을 부여했지만 이 수치 ($3.9 \times 10^{-9}$)가 ch4에 명시적으로 등장하지 않음 — 어디서 왔는지 추적 불가. | Ch1 L150 vs ch4 L886 vs abstract L2 | (a) Ch1 L150에서 $3.9 \times 10^{-9}$의 출처를 ch4 Table 또는 본문에 명시하거나, (b) full-set의 $2.5 \times 10^{-16}$만 인용하고 novel-only는 nominal Fisher p만 보고. |
| C2 | L150 vs L153 | **"7.19×" 숫자가 두 가지 의미로 동시 사용됨 (의미 충돌).** L150은 HIV-1 full=7.19× 또는 novel=7.16-8.24×만 언급하지만 L153에서 "HIV-1 full 7.19×"와 "H3N2 novel-only drops to 7.19× ($p=0.132$)"가 같은 paragraph에 나옴. 동일 숫자가 한 번은 HIV-1 강력한 anchor, 한 번은 H3N2 비유의(NS) 결과를 가리킴 → 심사위원이 "어느 7.19가 어떤 것인가" 즉시 혼동. | Ch1 L153 "...7.19× enrichment on the full HIV-1 escape set... drops to 7.19× with Fisher $p = 0.132$ (not significant)" | H3N2 novel-only 수치를 명시적으로 분리: "drops to 7.19× **for H3N2's 9 novel positions**, distinct from the HIV-1 full-set 7.19×" 또는 H3N2 novel-only 수치를 다른 라운딩(7.2× 또는 7.19×_H3N2)으로 표시. |
| C3 | L82 vs L150 | **"Two-stage experimental design" 주장과 "Stage 3" 등장 모순.** L82 (Objective 1)와 L143 (Contribution 1)은 "two-stage experimental design"으로 정의. 그러나 L150에서 "12-pathogen **Stage~3** panel"이 갑자기 등장 — Ch1은 Stage 3을 어디에서도 정의/소개하지 않음. ch3 methods L7은 "two-stage main design with a Stage~3 information-integration layer"라고 명시적으로 분리하지만 Ch1은 이 구조를 반영하지 않아 독자가 Stage 3 등장 시 혼란. | Ch1 L82, L143 ("two-stage") vs L150 ("Stage~3") + ch3 L7 | Objective 1과 Contribution 1에서 "two-stage main design plus a Stage~3 information-integration layer" 또는 "three-stage design (Stage~1 SARS-CoV-2 anchor; Stage~2 cross-pathogen MCC; Stage~3 information-integration)"로 일관화. Figure 1.1 Research overview 캡션에도 Stage 3 명시. |

---

## Major (심사위원 반드시 지적)

| ID | 위치 (라인) | 문제 | 근거 | 수정 제안 |
|----|------------|------|------|----------|
| M1 | L33-35 | **"no region-level hotspot detection benchmark" gap 주장 — bailey2018 "partial benchmark in cancer genomics"만 언급하며 viral 영역 cancer benchmark 외 선행 시도가 정말 없는지 검증 부족.** L35에서 "despite partial benchmark studies in cancer genomics~\cite{bailey2018comprehensive}"로 단 하나만 인용. weber2019benchmarking, lawrence2013mutsigcv, tamborero2013oncodriveclust, tokheim2016hotmaps, munoz2020mutspot 등 references.bib에 등재된 cancer mutation hotspot 벤치마크는 인용되지 않음. 적대적 심사위원이 "왜 weber2019만 ch3 등에서 언급하고 ch1 gap statement에는 빠지는가" 질문 가능. | Ch1 L33-35 vs references.bib (lawrence2013mutsigcv, tamborero2013oncodriveclust, tokheim2016hotmaps, munoz2020mutspot, weber2019benchmarking 모두 존재) | L35 "partial benchmark studies in cancer genomics~\cite{bailey2018comprehensive}"를 "...~\cite{bailey2018comprehensive,weber2019benchmarking,tokheim2016hotmaps}" 등으로 확장하여 cancer benchmark 검토가 충분했음을 보여주고 viral gap을 더 견고하게 정당화. |
| M2 | L77-88 | **Objectives와 Contributions가 거의 1:1 매핑 (새로움 부족 인상).** Objective 1 = MutBench 구축; Contribution 1 = MutBench. Objective 2 = dominant factor 식별 (ANOVA, Friedman, LOPO); Contribution 2 = $\omega^2 = 0.296$ + LOPO 0/11. Objective 3 = pathogen-specific information types + multi-source integration; Contribution 3 = 4-feature core + HIV-1 enrichment. 심사위원: "Contribution이 Objective의 단순 재진술 아닌가? 새로운 인사이트(예: 9 distinct optimal types, scoring×pathogen interaction이 detector보다 큼)가 Objective에 미리 포함되어 있어 surprise factor가 없음." | L77-88 Objectives vs L141-153 Contributions | Objectives는 "research questions" (열린 질문), Contributions는 "answers" (구체 수치/메커니즘)로 명확히 분리. 예: Objective 2를 "Quantify which factor dominates among scoring, detection, and pathogen"로 두고, Contribution 2에서 "scoring×pathogen interaction is the largest modeled variance component, with 9 distinct optimal types"로 답변하는 구조. 또는 Contribution 1에 "first systematic decomposition revealing scoring×pathogen interaction" 같은 새로움 표현 추가. |
| M3 | L36 | **자기 인용(han2025mosd, youn2025mutclust)이 Ch1 전체 8개 인용 중 2개 (25%) — 비율 자체는 허용 가능하나 위치가 문제.** L11 "core task...~\cite{youn2025mutclust}" — youn2025mutclust(MutClust)가 "core task의 정의/근거"로 인용되는 것은 자기-순환 인상 (자기 알고리즘을 hotspot 중요성의 근거로 인용). L36은 motivation으로 자기 인용이 정당화되나 L11의 위치는 적대적 심사가 "본인의 이전 논문을 본인 연구의 'core task' 근거로 사용"이라 지적 가능. | Ch1 L11, L36 | L11의 youn2025mutclust 인용을 harvey2021tracking 또는 carabelli2023convergent (이미 references.bib에 존재) 등 외부 문헌으로 교체. L36 motivational 자기 인용은 그대로 유지. |
| M4 | L33 | **Bailey 2018, ProteinGym, ViroGym, EVEREST v3는 인용되었으나 Livesey & Marsh, EVEscape는 누락.** references.bib에 livesey2020using과 thadani2023evescape가 존재. EVEscape는 변이 fitness/escape 예측 분야의 핵심 baseline으로 ch1의 "concurrent benchmarks" 단락에서 언급되어야 함 (특히 vaccine-escape 외부 검증을 강조하는 Ch1 입장에서). Livesey & Marsh는 DMS 기반 평가의 표준 reference. | references.bib에 entries 존재; ch1 L33 에서 누락 | L33 concurrent benchmarks 목록에 EVEscape (\cite{thadani2023evescape}) 또는 DMS 평가 reference로 livesey2020using 추가. 특히 EVEscape는 viral-escape 예측 task로 본 연구와 직접 비교 대상. |
| M5 | L57-69 | **세 개 problems가 contribution을 자동 정당화하도록 좁게 정의됨.** Problem 1 (no standardized framework) → Contribution 1 (MutBench framework); Problem 2 (no independent ground truth) → Contribution 1 (3-layer GT); Problem 3 (no pathogen-dependence statistics) → Contribution 2 ($\omega^2$). 적대적 심사: "이 세 문제는 본 연구가 풀 수 있도록 만든 strawman 아닌가?" 다른 명백한 gap (예: 인구학/표본 추출 편향, indel 처리, 동시변이 epistasis)이 problem definition에 빠져 있음. | Ch1 L57-69 vs ch6 L44 ("phylogenetic and sampling bias", "indel handling", "scope constraints"가 limitations에 등장) | (a) Problem definition에 자기 비판적 단서 추가: "These three problems do not exhaust all gaps; phylogenetic/sampling bias and indel handling are deferred to Chapter 6 limitations." 또는 (b) Problem 정의를 더 일반화: "no quantitative comparison of biological information types for region-level detection"으로 단일 핵심 gap에 집중. |
| M6 | L131 (Figure caption) | **Figure 1.1 caption은 "external vaccine-escape validation on a Layer~A-disjoint subset (HIV-1, Bonferroni-significant)"로 정확하지만 figure body L117은 "HIV-1 vaccine-escape enrichment (full set 7.19$\times$; novel-only 7.16--8.24$\times$) --- primary external validation"로 표기.** Body는 full-set 7.19×를 먼저 보여주고 novel-only를 부수적으로 표기 — 그러나 ch6 conclusion (L91)은 "HIV-1 escape enrichment (7.19×, 82% Layer A-disjoint)"로 표기 (도식과 일치하지 않는 단순화). Figure 1.1이 abstract와 ch6의 표현(novel-only가 primary anchor)을 정확히 반영하지 못함. | Ch1 L117 (figure body), L131 (caption) vs abstract L11, ch6 L91 | Figure body L117을 "HIV-1 vaccine-escape enrichment: novel-only 7.16-8.24× (37 Layer-A-disjoint positions, $p = 5 \times 10^{-12}$) — primary external anchor"로 변경. full-set 7.19×는 부차적 정보로 격하. |
| M7 | L145 | **Contribution 2 표현이 abstract와 다름.** Ch1 L145: "9 distinct optimal information types across 11 pathogens; LOPO 0/11 is reported as null-consistent corroboration..." — "null-consistent corroboration"로 LOPO를 약화. Abstract L10도 같은 표현 사용. Ch6 L13도 동일. **표현 일치는 OK.** 그러나 Ch1 L142의 "designed to answer the question: which biological information source is most effective for which pathogen?"이 ch6 L88 "viral hotspot detection is driven more by the fit between pathogen and biological information source than by detector choice alone"보다 약함 — Ch1이 핵심 인사이트("detector choice보다 information-source가 dominate")를 명시하지 않고 general question 형태로만 제시. | Ch1 L142 vs ch6 L88 | Contribution 1 또는 2 본문에 ch6의 핵심 take-home을 미리 알림: "...complementing concurrent fitness-regression benchmarks ... by establishing that the choice of biological information source explains more performance variance than the choice of detector." |
| M8 | L82 | **"information-type analysis across all 11 pathogens" — 그러나 ch4 L760은 정보형 분석은 12-pathogen (Zika 추가) 패널에서 수행되었다고 명시.** Ch1 L82 Objective 1의 sub-bullet은 "information-type analysis across all 11 pathogens"로 11 표기. 그러나 ch4 L760: "extended from the core 11 pathogens to 12 pathogens by adding Zika...for per-feature contribution estimates". L150 (Contribution 3a)은 "12-pathogen Stage~3 panel"로 12 표기. 즉 Ch1 내부에서 11 (L82)과 12 (L150)가 충돌. | Ch1 L82 vs L150 vs ch4 L760, L765 | L82를 "information-type analysis on the same 11-pathogen panel (extended to 12 with Zika for feature ablation; see Chapter~\ref{ch:results} Section~\ref{subsec:feature_ablation})"로 수정. |

---

## Minor

| ID | 위치 (라인) | 문제 | 근거 | 수정 제안 |
|----|------------|------|------|----------|
| m1 | L33 | "ViroGym~\cite{virogym2026}, 13 viruses / 79 DMS / 7 phenotypes"의 구체 숫자 인용은 충실하나 ProteinGym 217 DMS도 명시 — concurrent benchmark 비교가 dense하여 도입부 흐름이 끊김. | L33 단일 문장 길이 | 표나 별도 paragraph로 분리하거나 핵심 차이 (region-level vs per-variant)만 강조하고 숫자는 ch2로 이동. |
| m2 | L41-50 | "three-stage process" (sequence collection / computational analysis / experimental validation) — 서술은 명확하나 본 연구의 Stage 1/2/3과 용어 충돌 (독자가 "process의 stage"와 "experimental design의 stage"를 혼동 가능). | L41 "three-stage process" vs L82 "two-stage experimental design" | L41-50의 "three-stage process"를 "three-step pipeline" 또는 "three-phase workflow"로 변경하여 본 연구 Stage 1/2/3과 구분. |
| m3 | L46 | "Deep Mutational Scanning (DMS)"가 두 번 정의됨: L27 Glossary 표 + L46 본문 풀네임. L62-63 "DMS; a technique that experimentally measures..."에서 또 정의. 중복. | L27, L46, L62-63 | Glossary 표(L27)를 single source로 두고 본문에서는 약어만 사용. L62-63 괄호 정의 삭제. |
| m4 | L114 | Figure body 텍스트 "$\omega^2_{\text{scoring} \times \text{pathogen}}{=}0.296$, 9 types" — 9 types는 "9 distinct optimal types"의 축약이나 초독자에게 모호. | L114 | "9 distinct optimal scoring types"로 명시. |
| m5 | L155 | "Contribution~3 provides secondary external and practical checks rather than a separate claim of a validated general adaptive algorithm." — Contribution 3을 "secondary"로 명시한 자기 강도 조절은 ch6 L91의 "PAHD-R workflow convert these findings into usable prioritization tools, but the adaptive claim remains bounded"와 일관되나, abstract L11은 "Contribution 3 is two-part" + Contribution 3b를 "primary external anchor"로 표기 — Ch1의 "secondary"와 abstract의 "primary anchor" 표현 강도 차이. | Ch1 L155 vs abstract L11 | Ch1 L155를 "Contribution~3 provides multi-source integration infrastructure (3a) and external practical validation anchored on HIV-1 (3b); the adaptive predictor claim remains bounded as discussed in Chapter~\ref{ch:conclusion}"로 수정. "secondary"라는 자체 약화 표현 제거. |
| m6 | L150 | "0.081/0.083 mean MCC" 표기 — 분자/분모 의미 명시 없음. 4-feature/10-feature ratio? | L150 | "(0.081 of 0.083 mean MCC)" 또는 "(0.081 vs 0.083 = 97.6%)" 명시. |
| m7 | L11, L36 | "youn2025mutclust"가 두 번 인용 — L11은 hotspot의 "core task" 근거, L36은 motivation. M3 권고로 L11 교체 시 자연 해소. | (M3 참조) | M3와 통합. |

---

## 누락 인용 후보

- **`thadani2023evescape` (EVEscape)**: vaccine-escape/immune-escape 예측 분야의 가장 가까운 baseline — Ch1 L33 concurrent benchmarks 단락에서 직접 비교 대상으로 언급 필요. 본 연구 외부 검증이 vaccine-escape이므로 더더욱 인용 필수.
- **`livesey2020using` (Livesey & Marsh)**: DMS 기반 평가/벤치마크의 표준 reference — Ch1 L46 또는 L33에서 DMS validation 근거로 인용 필요.
- **`weber2019benchmarking` 또는 `lawrence2013mutsigcv`/`tamborero2013oncodriveclust`/`tokheim2016hotmaps`**: Ch1 L35의 "partial benchmark studies in cancer genomics" 근거로 bailey2018 단독 인용은 불충분. 이들 중 1-2개 추가 권장.
- **`carabelli2023convergent`** (이미 references.bib 등재): L11 "core task"의 외부 근거 인용으로 자기 인용(youn2025mutclust) 대체 가능.
- **`korber2020tracking`** (이미 등재): L9 SARS-CoV-2 mutation tracking 맥락에서 harvey2021tracking과 함께 인용 가능 (현재 harvey만 단독).

---

## 챕터 종합 평가

**강점**:
- Concurrent benchmarks (ViroGym/EVEREST v3/ProteinGym v1.3) 인용은 최신성 확보.
- 3-stage process (sequence collection / computational analysis / experimental validation) 서술은 일반 독자에게 task 맥락을 명확히 제공.
- $\omega^2 = 0.296$, 9 distinct types, LOPO 0/11 등 핵심 수치가 abstract와 일치.
- Contribution 3 (3a/3b) 분할 및 "novel-only" 감사 (37 Layer-A-disjoint)는 적대적 비판을 사전에 흡수하는 정직한 자기 critique.
- Figure 1.1은 problem→framework→finding→impact의 logical flow를 시각화.
- Fairness/circularity audit (Layer A/escape overlap, novel-only enrichment) 재진술이 abstract, ch4, ch6와 일관됨.

**약점**:
- **C1 (가장 심각)**: HIV-1 novel-only Bonferroni p값 ($3.9 \times 10^{-9}$)이 ch4 본문/표에 추적되지 않음. 검토자가 출처 확인 시 실패하면 fabrication 의혹 가능.
- **C2**: 같은 paragraph (L153) 내에서 "7.19×"가 HIV-1 full과 H3N2 novel-only를 동시에 가리켜 즉시 혼동 유발.
- **C3**: "Two-stage" vs Stage 3 등장 구조 모순 — Ch1이 본 연구의 실제 design (2+1)을 반영하지 않음.
- Objectives와 Contributions의 1:1 매핑으로 새로움(novelty) 인상 약함 (M2).
- Cancer benchmark 인용이 bailey2018 1편으로 빈약 (M1).
- EVEscape, Livesey & Marsh 누락 (M4).
- Information-type panel 크기 (11 vs 12)가 Ch1 내부에서 충돌 (M8).
- L11의 youn2025mutclust 자기 인용이 "core task" 근거로 사용된 위치 부적절 (M3).

**합격선 통과 여부**: **CONDITIONAL**

- **이유**: Critical 3건 (특히 C1: novel-only Bonferroni $3.9 \times 10^{-9}$ 출처 불명) 중 적어도 1건은 적대적 심사에서 즉시 지적당할 가능성 매우 높음. C2는 같은 페이지에서 같은 숫자가 두 가지 의미를 갖는 명백한 혼란 야기. C3는 본 연구의 design이 실제로 3-stage임에도 Ch1이 2-stage라 주장하여 ch3과 모순 (구조적 일관성 결함).
- C1, C2, C3 수정 + Major M3 (L11 자기 인용), M8 (11/12 충돌) 수정 시 PASS 가능.
- Major M1, M4, M5, M6, M7은 심사위원 질의 가능성 높으나 지적 후 답변으로 방어 가능 — 사전 수정 권장이지만 합격 차단은 아님.
- Minor 7건은 전수 수정 시 가독성 개선되나 합격 영향 없음.

**우선순위 수정 권고 (5건)**:
1. **C1**: Ch1 L150의 "$3.9 \times 10^{-9}$"를 ch4 본문에서 명시 또는 삭제하고 nominal Fisher만 보고.
2. **C2**: Ch1 L153에서 H3N2 novel-only "7.19×"를 명시적으로 분리 ("for H3N2's 9 novel positions" 등).
3. **C3**: Ch1 L82, L143의 "two-stage experimental design"를 "two-stage main design plus Stage 3 information-integration layer"로 통일.
4. **M3**: Ch1 L11의 youn2025mutclust 인용을 carabelli2023convergent 또는 harvey2021tracking으로 교체.
5. **M8**: Ch1 L82의 "across all 11 pathogens"를 "11-pathogen panel (extended to 12 with Zika for feature ablation)"로 수정.
