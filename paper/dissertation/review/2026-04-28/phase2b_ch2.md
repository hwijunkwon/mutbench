# Ch2 Background 심층 검토 (Phase 2B Adversarial)

리뷰 대상: `/proj/paper/paper/dissertation/chapters_en/ch2_background.tex` (총 300 lines)
참조: `/proj/paper/paper/dissertation/references.bib` (124 entries)
검토일: 2026-04-28

요약 한 줄: 인용 키 누락은 없으나, **(a) MEME/FUBAR 잘못된 출처 인용**, **(b) OncodriveCLUST↔OncodriveCLUSTL 명칭 불일치**, **(c) "no detection-task benchmark" gap의 scope-bias**, **(d) MutClust/EVEscape 유리한 서술**, **(e) ESM-3·BloomLab 항체 escape DMS·HyPhy FEL/SLAC·Greaney 시리즈 누락**이 핵심 결함이다.

---

## Critical

| ID  | 위치 (line) | 문제 | 근거 | 수정 |
|-----|-------------|------|------|------|
| C1  | L57 | **MEME와 FUBAR 모두 `\cite{kosakovsky2020hyphy}` (HyPhy 플랫폼 논문)에 귀속** — 두 방법은 각각 별도의 1차 출처를 가진다. FUBAR의 1차 출처는 Murrell et al. 2013 (`murrell2013fubar`로 references.bib L1119에 이미 등록되어 있으나 ch2에서 사용 안 됨). MEME의 1차 출처는 Murrell et al. 2012 (PLoS Genet. 8:e1002764, **bib에 미등록**). | references.bib L1119 `murrell2013fubar` 항목은 정확히 FUBAR 원논문이며 ch3 L616에서는 `\cite{murrell2013fubar}`로 정확히 인용되어 있다. ch2에서만 일관성이 깨진다. | L57 인용을 `MEME~\cite{murrell2012meme}`(신규 등록 필요)와 `FUBAR~\cite{murrell2013fubar}`로 분리. HyPhy 플랫폼은 별도 문장으로 처리. |
| C2  | L39 vs L241 | **명명 불일치**: L39은 `OncodriveCLUST~\cite{tamborero2013oncodriveclust}`(2013, original)을 인용, L241에서는 후속 도구인 `OncodriveCLUSTL`(Arnedo-Pac et al. 2019, Bioinformatics)을 마치 동일한 도구처럼 묶어 언급. CLUSTL은 별도 도구로 별도 인용이 필요하며, 인용 키도 references.bib에 등록되지 않았다. | references.bib에 `arnedopac2019` 또는 `oncodriveclustl` 키 검색 결과 0건. | 두 가지 옵션 — (a) L241에서 "OncodriveCLUSTL"을 "OncodriveCLUST"로 통일 (정확성 우선) 또는 (b) Arnedo-Pac 2019 항목을 bib에 추가하고 두 도구를 분리해 기술. |
| C3  | L234, L242, L298 | **"no analogous detection-task benchmark exists"의 SCOPE-BIAS**. Pons 2020(L239)이 cancer 영역 35+ 도구를 cataloging했고, EVEREST/ViroGym/ProteinGym은 task가 다르다는 이유로 배제된다. 그러나 **(a) Bloom Lab의 escape calculator (Greaney 2021/2022)와 (b) Tonkin-Hill et al.의 SARS-CoV-2 hotspot benchmark**는 영역적으로 인접하면서 "viral region-level"에 더 가깝다. 또한 "detection-task benchmark"라는 개념을 "cross-pathogen × multi-source × MCC composite metric × ANOVA decomposition"이라는 매우 좁은 정의로 한정함으로써 gap이 거의 정의에 의해 보장된다. | L234 "while several recent fitness-regression benchmarks now span comparable virus panels, the region-level hotspot-detection task itself remains unstandardized" — 이 한 문장이 gap claim의 모든 부담을 짊어지나, "region-level"이라는 추가 한정이 scope를 인위적으로 좁힌다. L298 "no standardized framework exists for evaluating and comparing these methods across multiple pathogens with independent ground truth"도 동일 문제. | (1) L234에 명시적 단서 추가: "...remains unstandardized *with the specific combination of cross-pathogen panel, multi-source scoring sweep, and ANOVA-based interaction analysis*"; (2) gap이 정의-기반(definitional)임을 인정하되 그 정의 자체의 실용적 가치(novel pathogen에 대한 scoring 추천)를 별도 문장으로 정당화. |
| C4  | L143-144 | **ESM-3은 "no formal citation key is asserted" 라며 인용 없이 본문에 등장**. 학위논문 본문에서 이름을 명시 언급하면서 인용 부재라는 처리는 이례적이다. 독자가 ESM-3 정보를 추적할 출처가 없다. | "the ESM-3 generation extended the ESM family ... (no formal citation key is asserted here as the dissertation does not benchmark ESM-3 directly; ESM-3 is named only for completeness ...)" | Hayes et al. 2024 (Science 387:850, "Simulating 500 million years of evolution with a language model") 또는 Anthropic preprint를 bib에 추가하고 정식 인용. 어차피 이름을 적었다면 인용이 학술적 표준. |
| C5  | L143 | **"ProtTrans와 ESM-3는 viral VEP에 less extensively validated"** 주장의 근거 부재. ProtTrans의 viral 적용 사례를 부정한 비교 연구를 인용하지 않으면 negative claim이 unsupported. | L143-144 전체. | 객관적 표현으로 약화: "to our knowledge, no large-scale viral hotspot benchmark has incorporated ProtTrans or ESM-3 as scoring channels"로 한정. |
| C6  | L148 | **EVEscape 자기-구현(`EVEscape_composite`)에 대한 호의적 서술**. "an EVEscape-style implementation, not the original EVEscape model"라고 명시한 점은 양호하나, **EVE 대신 ESM-2 LLR을 fitness term으로 쓴 것이 본질적으로 다른 정보를 제공한다**는 점은 단점으로 명시되지 않았다. EVEscape 원논문(Thadani 2023)은 EVE 사용을 핵심 디자인 선택으로 강조하므로, 대체는 단순한 implementation 차이가 아니라 정보 내용의 변경이다. 또한 chapter 4의 EVEscape composite 결과가 어느 pathogen에서도 "best"를 차지하지 않는다는 사실(ch4 L210)을 ch2에서 미리 disclaim하지 않는다. | L148 전체 + ch4 L210의 best-per-pathogen 표. | "While conceptually parallel, this substitution materially changes the information content (ESM-2 LLR is a generic PLM mutation surprise, whereas EVE captures family-specific evolutionary distribution); empirical equivalence with the original EVEscape model is not asserted." 추가. |
| C7  | L213-228 | **Rice 1976 algorithm selection problem**: Ch2에서 정식 도입되나, **ch1 L69에서 이미 언급**되어 ch1 → ch2 흐름에서 forward-citation이 보이지 않고, Algorithm Selection Problem이 ch5 discussion(L84)에서도 다시 등장한다. ch2의 \subsection{Algorithm Selection and Benchmarking Methodology}는 **prior work review** 위치인데, 실제로는 MutBench의 정당화 framework로 사용되어 "background"의 scope를 벗어난다. | L222 "The parallel to MutBench is direct: just as AutoML selects the optimal machine learning pipeline based on dataset characteristics, MutBench's pathogen-to-scoring recommendation table selects the optimal scoring--detection combination based on pathogen characteristics." — 명백히 이 한 문장은 ch5 discussion으로 이동해야 한다. | L222를 ch5 discussion으로 이동 또는 "MutBench의 application은 ch5에서 상술"이라는 forward reference만 남기고 prior-work 자체로 한정. |

---

## Major

| ID  | 위치 | 문제 | 근거 | 수정 |
|-----|------|------|------|------|
| M1  | L31, L34 | **Mullick 2021 (entropy)과 koyama2020/obermeyer2022는 같은 단락에 있으나 둘 다 SARS-CoV-2 단일 pathogen 한정**. "single-pathogen 연구만 존재"라는 ch2의 후반 gap claim을 직접 뒷받침하지만, 이 단락에서는 그 연결이 만들어지지 않는다. | L34 "single information types ... without systematic comparison" | L34 끝에 "(a single-pathogen, single-information limitation that motivates the multi-pathogen comparison in Section~\ref{sec:bg_benchmarking_gap})" 추가. |
| M2  | L43-49 | **Phylogenetic non-independence 단락에서 HyPhy/Pond를 인용하면서 BUSTED, FEL, SLAC**(같은 HyPhy 패키지의 다른 method)이 누락. ch2 L241은 "MEME, FUBAR, FEL"을 묶어 언급하지만, FEL의 별도 출처(Kosakovsky Pond & Frost 2005, MBE 22:1208)는 부재. | L57-60에서 MEME/FUBAR만 명시, FEL은 L241에서만 이름이 나옴. | L57 단락에 FEL을 추가 (Kosakovsky Pond & Frost 2005), 또는 L241에서 FEL 언급을 삭제하여 일관성 확보. |
| M3  | L99-117 | **DMS as ground truth 단락에서 BloomLab의 *항체 escape DMS* 시리즈가 누락**: Greaney et al. 2021 *Cell Host Microbe* 29:44 (RBD-antibody escape), Greaney et al. 2022 *PLoS Pathogens* (full Spike escape). 본 학위논문은 vaccine escape cross-validation(Layer C)을 핵심 contribution으로 하는데 *그 ground truth의 학문적 계보*인 Greaney 시리즈를 ch2에서 다루지 않는 것은 중대한 누락이다. | L100-106에서 Starr 2020(RBD binding), Dadonaite 2023(Spike entry), Lee 2018(H3N2 HA), Bloom-Neher 2023만 인용. Greaney 시리즈는 어디에도 없음. | L106 다음에 한 단락 추가: "Greaney et al.~\cite{greaney2021RBD,greaney2022spike} extended DMS to antibody-escape mapping for the SARS-CoV-2 RBD and full Spike, providing per-position escape scores against multiple monoclonal antibodies and convalescent sera. These escape DMS datasets directly inform the Layer~C cross-validation paradigm of MutBench (Section~\ref{sec:cross_validation_escape})." 두 항목 bib 추가 필요. |
| M4  | L154 | **EVEREST 인용 시 v1만 사용** (`gurev2025everest`); v3 expansion(`gurev2026everest_v3`)은 L112, L237에서만 호출됨. v3가 PLM ≪ alignment claim의 더 강한 증거이므로 L154에서도 v3를 함께 인용해야 일관적이다. | L154 "The EVEREST benchmark~\cite{gurev2025everest} found that PLMs substantially underperform alignment-based methods on viral proteins" | `\cite{gurev2025everest,gurev2026everest_v3}`로 변경. |
| M5  | L196-198 | **Rodriguez-Rivas 2022 (DCA) 단락이 매우 길고 epistasis exclusion에 대한 *후방* 정당화로 변형**된다. 단락 후반(L198) "This single-position restriction is a design choice, not a neutral simplification..."는 이미 Background가 아니라 **methodological caveat**. ch2 background에서 이를 다루는 것은 정당하나 분량이 chapter summary 부분(L299)과 중복된다. | L198 ↔ L299 "Coupling-aware methods (DCA, EVcouplings, GREMLIN, ...) remain explicitly out of scope ..." | L198 후반(About epistasis-driven realism)을 chapter summary로 흡수해 단일 위치에서 다루기. |
| M6  | L216-219 | **NFL theorem 적용의 부정확성**. Wolpert-Macready 1997 NFL은 *uniform prior over all problem instances*에서만 성립한다. "no single algorithm outperforms all others across all possible problem instances"는 이 prior 가정 없이 일반화되었다. NFL이 hotspot detection에 strict하게 적용된다는 주장은 over-statement. | L217 단락. | L217 마지막에 "(strictly speaking, NFL holds in expectation over a uniform problem distribution; the empirical interaction $\omega^2 = 0.296$ provides domain-specific rather than universal evidence)" 추가. |
| M7  | L233 (Bailey 2018 형평) | Bailey 2018은 L233에서만 본문 등장 + L270 표 1열로 비교. **본문에서 Bailey의 한계** (cancer-specific, 26 tools all curated by authors, no PRC analysis 등)는 거론되지 않아 "MutBench의 모범"으로만 그려진다. ch5 L287에서 "독립 재현 gap"으로만 다시 언급되지만 그 또한 우호적. | L233 + L270 비교표. | L233 다음 문장 추가: "Bailey 2018, while methodologically rigorous within cancer genomics, was confined to a single disease domain (somatic tumor mutations), used a single curated tool ensemble (26 methods chosen by the consortium), and did not include a scoring--method interaction analysis; its replication in viral genomics requires the cross-pathogen design adopted in MutBench." |
| M8  | L246-260 (VEP Benchmarks 서브섹션) | **자기 contribution 강조 비율이 과도**: L254-260 5문장이 모두 MutBench 우월성 주장이며, ProteinGym/EVEREST/ViroGym 자체의 강점은 거의 거론되지 않음. ch2는 "related work review"가 본 목적이지 contribution restatement가 아니다. | L254 "MutBench's unique contribution is..." 부터 L260까지. | (1) L254-260을 ch5 discussion으로 이동 또는 (2) L254 시작에 "Building on these foundations,"를 두고 분량을 절반으로 축소. ch3 L9-13의 framework 설명과 중복도 검토. |
| M9  | L237 (ViroGym) | **ViroGym 인용은 single source(`virogym2026`, arXiv preprint, 2026-03)에 의존**. arXiv 만의 비-피어리뷰 사전인쇄(2026-03 issue)를 "comparable benchmark"로 동등 대우하는 것은 신중해야 한다. | bib L1220-1226. | "(arXiv preprint, March 2026; pre-peer-review)" 단서 추가. |
| M10 | L243-285 (전체) | **표 1과 본문이 부분 중복**: 본문 L246-260이 표 1의 행을 풀어쓴 것에 가깝다. | L267-282 표 vs L254-260 본문. | 표를 *primary*로 두고 본문에서는 표가 보여주지 않는 *질적 차이*만 서술. |

---

## Minor

| ID  | 위치 | 문제 | 수정 |
|-----|------|------|------|
| m1  | L20 | "$10^{-3}$ to $10^{-5}$ substitutions per nucleotide per replication cycle" — Sanjuán et al. 2010 (`sanjuan2010viral`, bib L1275)이 직접적 1차 출처. `holmes2009evolution`은 책으로 간접 인용. | `\cite{holmes2009evolution,sanjuan2010viral}` 병기 권장. |
| m2  | L31 | "Mullick et al.~\cite{mullick2021entropy}" — 본 단락은 Shannon entropy 개념 자체를 도입하는데 Shannon 1948 등 1차 entropy 정의 인용은 부재. | 단순 entropy 개념은 무인용 서술 가능. 그대로 두어도 무방. |
| m3  | L52-54 | "Sliding window methods" 단락에 *어떤* 기존 sliding-window 도구도 인용되지 않음. SWAN(ch3 L703에서 사용)이나 Sonesson 2003 CUSUM(`sonesson2003cusum`, bib L792)이 후보. | `\cite{sonesson2003cusum}` 또는 SWAN 인용 추가. |
| m4  | L65 | DBSCAN 인용 `ester1996dbscan` — 정확. |
| m5  | L74 | "youn2025mutclust" 자기 인용에 99.76\%, 4 clusters 같은 매우 구체적 수치 — DBSCAN 실패 사례를 youn2025mutclust 문서에서 그대로 가져온 것이라면 ch3에서 재현 가능 여부 명시 필요. | ch3과의 cross-ref 확인. |
| m6  | L83 | OPTICS는 1999, "complementary approach"는 chronological misleading (DBSCAN 1996 → OPTICS 1999 → HDBSCAN 2013 순서). | "OPTICS, an earlier extension of DBSCAN by..." 같은 명시 추천. |
| m7  | L122 | "EVE achieves state-of-the-art performance on clinical variant classification" — 2026년 시점에서 AlphaMissense, ESM2, GPN-MSA 등 후속 연구가 EVE를 상회. "achieves" → "achieved at the time of publication". |
| m8  | L150-151 | AlphaMissense 단락이 두 번 등장(L150-151과 L252). 중복. | L252에서 "AlphaMissense (introduced earlier)"로 단축하거나 한 곳으로 통합. |
| m9  | L173 | "PANGO~\cite{rambaut2020pangolin}" — 정확하나 PANGO는 분류 시스템이고 pangolin은 도구. 두 개념이 혼동된 채 인용. | "PANGO lineage system, implemented in the pangolin tool~\cite{rambaut2020pangolin}"으로 분리. |
| m10 | L180 | "surveillance answers `what has happened?' while hotspot detection aims to answer `where might important mutations occur next?'" — Nextstrain의 *forecasting* 모듈(Bedford lab의 augur frequency forecasting, Hadfield 2018 후속)을 무시. | "primary function" 정도로 단서 부여. |
| m11 | L192-193 | Maher 2022 결과 "epidemiological features dominated over sequence-based features" — 이 결과는 본 dissertation의 Stage 2 frequency dominance와 강한 평행. ch4 cross-ref 추가 권장. |
| m12 | L196-198 | DCA → "epistasis-aware extensions are flagged as future work in Chapter~\ref{ch:discussion}" — ch5 discussion에서 실제로 이를 future work로 처리하는지 확인 필요. ch5 L323에서 family-pair 분석이 있으나 epistasis future work로의 직접 forward는 ch6 conclusion 쪽이다. cross-ref가 약간 어긋남. |
| m13 | L246-249 단락 첫 문장 | "Recent years have seen significant progress" — 학위논문에서는 시간 표현 회피 권장. "Recent benchmarks for VEP..."로 시작. |
| m14 | L264 표 caption | "Comparison of MutBench with related benchmarks" — 너무 짧음. "Cross-benchmark comparison: task, scope, ground-truth, methods compared"로 확장 권장. |
| m15 | L289-300 | Chapter Summary가 SECTION 2: MutClust Summary(L289-290)라는 주석 안에 들어있다. 주석 라벨과 실제 내용이 불일치. | 주석을 "Chapter Summary"로 수정. |

---

## 누락 의심 인용 (구체적 후보)

| 후보 | 출처 | 왜 필요 | 어디에 |
|------|------|---------|--------|
| Greaney et al. 2021, *Cell Host & Microbe* 29:44 | RBD antibody escape DMS | Layer C escape ground truth의 직접 1차 출처 | L106 다음 |
| Greaney et al. 2022, *PLoS Pathogens* 18:e1010592 | Full Spike escape DMS | 위와 동일 | L106 다음 |
| Murrell et al. 2012, *PLoS Genet.* 8:e1002764 | MEME 1차 출처 | C1 수정에 필요 | L57 |
| Hayes et al. 2024-2025 (ESM-3) | ESM-3 1차 출처 | C4 수정에 필요 | L143 |
| Arnedo-Pac et al. 2019, *Bioinformatics* 35:4788 | OncodriveCLUSTL | C2 수정에 필요 | L241 |
| Kosakovsky Pond & Frost 2005, *MBE* 22:1208 | FEL 원논문 | M2 수정에 필요 | L57 또는 L241 |
| Sanjuán et al. 2010, *J Virol* 84:9733 | Viral mutation rate quantification | m1 (이미 bib에 등록됨) | L20 |
| Tonkin-Hill et al. 2021 / Singer et al. (ROBERT) | SARS-CoV-2 hotspot/recurrent mutation framework | gap claim의 fairness | L234 또는 L240 (4)번 항목 |
| Bedford et al. 2014 *PLoS Pathogens* 또는 Łuksza & Lässig 2014 *Nature* | Influenza forecasting framework | 표 비교에서 prediction 진영 균형 | L249 단락 끝 |
| Smith et al. 2004 (`smith2004antigenic`, 이미 bib에 있으나 ch2 본문에서는 L249 한 번만 등장) | antigenic cartography 시조 | L201 hie2021learning 단락에 함께 |

---

## 형평성 평가

**자기 인용 비율**: ch2의 `\cite` 호출 중 저자 본인 그룹 출처는 다음과 같다.
- `youn2025mutclust` — L34("Large-scale frequency-based"), L74, L89, L241, L297 등 **5회**
- `han2025mosd` — ch2에 **0회 (ch1에서만)**
- 본 학위논문 직속 partner 인용 (Jung Inuk lab) 합계: 5회

총 unique citation key: 51개. **자기 인용 비율 = 5/51 ≈ 9.8%** — 절대값으로는 과도하지 않으나, **MutClust(youn2025mutclust)의 비판적 한계 명시는 단 1회(L297 "single pathogen, single information type, self-referential validation")만 등장**하고, 그 외 4회는 모두 호의적 맥락(adaptive solution, prior state-of-the-art, baseline)이다. **L74의 "99.76% merged into a single massive cluster"는 DBSCAN의 실패 사례를 youn2025mutclust의 결과로 인용하는데, 이는 자기-인용으로 자기-방법(MutClust)의 motivation을 정당화하는 순환적 구조에 가깝다.**

**외부 vs 자기 균형**: 외부 인용은 51-5 = 46개로 양적으로는 충분. 그러나:
- **prior detection-task benchmarks 인용은 사실상 0개**(C3 참조). 모두 prediction-task로 정의-배제됨.
- **PLM landscape (ESM-2, ESM-3, ProtTrans, Tranception, EVE, AlphaMissense)**는 잘 다루어졌으나 **ESM-IF(inverse folding), SaProt, ProteinMPNN** 등 구조-인식 PLM 계열은 미언급.
- **DMS landscape**: Starr/Dadonaite/Lee/Bloom-Neher는 다루었으나 **Greaney 시리즈(M3) 누락**이 가장 큰 균형 문제.

**Bailey 2018 형평성**: M7 참조. 단순 비교 reference로 등장하며 그 한계는 거론되지 않는다.

---

## VEP vs hotspot 구분의 명확성

L161-165, L235-242, L282 (표 caption)에서 task 차이를 **task / domain / analysis objective** 3축으로 명시한다. 명료하나 다음 약점이 있다:
- **per-region** 정의의 정량적 기준(region size, threshold)이 ch2에서 제시되지 않음 (ch3에서 다루어진다 가정 시 forward ref 필요).
- L162 "binary classification problem over genomic regions" — region이 무엇인지 (residue range? domain?)가 ch2 자체에서 self-contained하지 않다.
- gap claim이 (per-variant fitness regression) ≠ (per-region detection)이라는 *task-distinction*에 의존하므로, 이 distinction 자체의 임상/감시적 중요성을 한 단락 더 정당화하면 설득력 강화.

**평가**: PASS with conditions — distinction 자체는 정확하나 region 정의의 self-containedness가 부족.

---

## 인용 형식 일관성

- `\cite{...}` 호출 56건 모두 references.bib에 존재 확인 (MISSING 0건).
- 단, **C1, C2, C4의 경우 인용 키는 존재하나 1차 출처가 잘못 매핑**된 의미상의 오류.
- `notin2023proteingym,notin2025proteingym_v13` 같은 multi-key 인용 형식 일관 (5회 발견).

---

## Rice 1976 일관성 (chapter간)

- ch1 L69: "specific instance of the algorithm selection problem~\cite{rice1976algorithm}"
- ch2 L213-228: 정식 도입 (subsection)
- ch5 L84: 결과 해석에 적용
- ch6 L74: future work로 재활용 (kerschke 함께)

→ **4개 챕터에서 일관 사용. ch2가 framework 소개, ch5가 적용, ch6가 확장.** 단, **ch2 L222 ("MutBench's pathogen-to-scoring recommendation table selects ...")는 ch5의 영역**이며 background에 들어가 있는 것이 부적절(C7).

---

## 챕터 종합 평가

**판정**: **CONDITIONAL PASS**

**이유 (PASS 측면)**:
- 51개 외부 인용으로 frequency/entropy/density-based clustering/PLM/surveillance/feature importance/algorithm selection의 6대 영역을 폭넓게 커버.
- VEP benchmark vs detection benchmark distinction을 task/domain/objective 3축으로 명시.
- ProteinGym v1.3, EVEREST v3, ViroGym 2026 같은 최신(2025-2026) benchmark를 모두 인용.
- 인용 키 missing 0건, multi-key 인용 형식 일관.

**이유 (CONDITIONAL 측면 — fix 필요)**:
1. **C1 (MEME/FUBAR 1차 출처 오류)** — 학위논문에서 1차 출처 오류는 심사 시 즉시 지적될 수 있음.
2. **C2 (OncodriveCLUST/CLUSTL 명명 불일치)** — 두 도구를 혼동.
3. **C3 (gap claim의 scope-bias)** — gap이 정의-기반임을 인정하거나 scope를 명시 한정.
4. **M3 (Greaney escape DMS 누락)** — Layer C의 1차 학문적 계보가 빠져 있음.
5. **C4 (ESM-3 인용 부재)** — 본문 언급 + 인용 부재는 이례적.

**우선순위 수정 (5건이 모두 fix되면 PASS로 격상)**:
1. C1: MEME/FUBAR 인용 분리 → `murrell2013fubar`(이미 bib) 사용 + `murrell2012meme` 신규 추가
2. C2: L39 또는 L241 둘 중 하나로 명명 통일
3. M3: Greaney 2021/2022 인용 추가 (Layer C 학문적 계보 보강)
4. C3: L234에 "with the specific combination of..." 단서 추가
5. C4: ESM-3 정식 인용 또는 본문에서 ESM-3 언급 삭제

이 5건은 **반나절 작업**으로 처리 가능하며, 이후 ch2는 PASS 수준에 도달한다.
