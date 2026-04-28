# Ch6 Conclusion 심층 검토

대상: `/proj/paper/paper/dissertation/chapters_en/ch6_conclusion.tex` (118 lines, 4 sections + dual-use + code/data/numerical artifacts paragraphs)
비교: `/proj/paper/paper/dissertation/front_en/abstract.tex` (line 1-18), `/proj/paper/paper/dissertation/chapters_en/ch1_introduction.tex` (line 136-156, Section 1.4 Contributions)

---

## Critical (기여 재진술 불일치 / 결론 과장)

| ID | 위치 | 문제 | 근거 | 수정 |
|---|---|---|---|---|
| C1 | ch6 line 11 (Contribution 1) | ch6 Contribution 1은 "MutBench is the broadest …" 또는 "to our knowledge" 같은 first-claim을 **삭제**해서 abstract line 4 / ch1 line 142와 표현 강도가 일치하지 않음. abstract와 ch1은 모두 "to our knowledge, MutBench is the broadest \emph{region-level hotspot-detection} benchmark to date" 명시. ch6는 단순히 "MutBench provides a benchmark …" 로 약화. 일반적으로 결론은 abstract/intro 와 같은 강도로 재선언해야 함 (논문 결론에서 first-claim 약화는 reviewer가 "약하다" 또는 "claim 변경" 해석 가능) | abstract.tex:4, ch1_introduction.tex:142 vs ch6:11 | ch6 line 11 끝에 "MutBench provides a benchmark for viral mutation hotspot detection across 11 RNA viruses --- to our knowledge, the broadest region-level hotspot-detection benchmark to date relative to concurrent fitness-regression panels (ViroGym, EVEREST~v3, ProteinGym~v1.3) ---" 와 같이 abstract/ch1 표현을 재진술 |
| C2 | ch6 line 15 | ch6 line 15: "yields 7.19-fold enrichment **after correction**" — abstract line 2/11과 ch1 line 150은 Bonferroni $p_{adj}=2.5\times10^{-16}$ (full set 7.19$\times$) 와 novel-only $7.16\text{--}8.24\times$ ($p_{adj}\approx 3.9\times 10^{-9}$, worst-case nominal $5\times 10^{-12}$)을 분리하여 보고. ch6에서는 7.19$\times$이 (a) full set인지 (b) novel-only인지 (c) Bonferroni 적용인지 모호. 단지 "7.19-fold … after correction"은 두 수치를 합치하여 reviewer가 헷갈림. abstract Contribution 3b는 명시적으로 "primary anchor with direct novel-only Fisher enrichment $7.16\text{--}8.24\times$" 로 표현 | ch6:15 vs abstract:11, ch1:150, ch4:874 (full set 7.19$\times$, $p<0.0001$) | ch6 line 15를 "yields full-set 7.19-fold enrichment (Bonferroni $p_{adj}=2.5\times 10^{-16}$) and Layer~A-disjoint novel-only enrichment $7.16\text{--}8.24\times$ (worst-case Fisher $p=5\times 10^{-12}$)" 로 확장 — 또는 적어도 한 문장 추가하여 두 수치 모두 표시 |
| C3 | ch6 line 14 (Contribution 3) | ch6 Contribution 3는 "Third, multi-source integration supplies a practical cold-start floor" 로 한 단락으로 통합. **abstract line 11과 ch1 line 150은 "Contribution 3 is two-part" (3a 통합 인프라 / 3b 외부 검증)** 로 명시적으로 두 부분으로 분리. ch6는 이 "두-part 구조" 자체를 명시하지 않음 — Contribution 카운트가 abstract/ch1는 4개(1, 2, 3a, 3b), ch6는 3개로 다르게 읽힘. 박사논문 심사위원은 "Contribution 수치 불일치"로 지적 가능 | abstract:11 ("Contribution 3 is two-part"), ch1:150 ("Contribution 3 (two-part)") vs ch6:14-15 (단일 단락) | ch6 line 14를 "\textbf{Third (two-part)}: \textit{(3a) Multi-source integration} … \textit{(3b) External validation, anchored by HIV-1} …" 로 재구조화하여 abstract/ch1과 일치 |
| C4 | ch6 line 14 vs abstract line 11 | ch6 line 14는 "the 4-feature core … retains 97.6\% of the 10-feature EqualWeight ensemble mean MCC" — but **omits the "0.081/0.083 mean MCC", "12-pathogen Stage 3 panel", "uniform-weight LOPO top-10\%", "numerical equivalence, no paired-test significance"** which ch1 line 150 explicitly includes. ch6 omission removes the qualifying caveat that the 97.6\% figure is numerical not statistical, exposing ch6 to the Tier-2 critique that Major M3 in Phase 2 already flagged for Stage 3. Conclusion strengthening = drift toward overclaim | ch6:14 vs ch1:150, ch4:801 | ch6 line 14: "retains 97.6\% (0.081/0.083 mean MCC) of the 10-feature EqualWeight ensemble (numerical, not paired-test significance)" |

---

## Major

| ID | 위치 | 문제 | 근거 | 수정 |
|---|---|---|---|---|
| M1 | ch6 line 11 | Contribution 1 표현이 "20 scoring formulas, 39 detector variants" 만 언급. abstract line 2와 ch1 line 142 둘 다 "10 biological information types (20 scoring formulas) $\times$ 14 detection families (39 variants) $\times$ 11 RNA viruses = 8{,}580 evaluations" 형식. ch6는 (a) "10 biological information types" (b) "14 detection families" (c) "8,580 evaluations" 모두 빠뜨림. 결론에서 핵심 grid 크기가 빠지면 한 줄로 챕터 요약을 인용할 때 정보 손실 | ch6:11 vs abstract:2, ch1:33,82 | ch6 line 11: "MutBench provides a benchmark … combining 10 biological information types (20 scoring formulas) $\times$ 14 detection families (39 variants) $\times$ 11 RNA viruses = 8{,}580 evaluations …" |
| M2 | ch6 line 13 | "Friedman $p=0.990$ are treated as null-consistent corroboration" — abstract line 10, ch1 line 145의 표현은 LOPO에 "null-consistent" 만 적용 (Friedman 자체는 "no universally best combination"으로 별도 해석). ch6는 Friedman과 LOPO를 한 묶음으로 "null-consistent" 처리하여 Friedman의 의미를 왜곡 ($p=0.990$은 균일한 best가 없음을 보여주는 일관성 결과지, "null-consistent corroboration"이라는 표현은 부적절). 정확하게는 Friedman은 "no universally best combination", LOPO 0/11이 "null-consistent under permutation" 으로 분리해서 표현 | ch6:13 vs abstract:10, ch1:145, ch4:445-446,565 | ch6 line 13을 "Friedman $\chi^2=7.69, p=0.990$ shows no universally best combination, and LOPO 0/11 is null-consistent under permutation; both are corroborative consistency checks rather than independent evidence" 로 분리 |
| M3 | ch6 line 12 | "the 11 pathogens have 9 distinct optimal information types" — abstract line 13은 "FUBAR phylogenetic selection scores achieve the highest MCC for H3N2 (0.534), protein language model scores dominate for SARS-CoV-2 and RSV, and homoplasy scores excel for Norovirus" 같은 예시 명시. ch1 line 146도 동일한 예시 포함. ch6는 예시 전혀 없음 → 결론의 "9 distinct" claim이 근거 없이 떠 있음. 결론에서 적어도 1-2개 예시는 abstract와 일치시켜야 reviewer가 즉시 검증 가능 | ch6:12 vs abstract:13, ch1:146 | ch6 line 12 끝에 "(e.g., FUBAR for H3N2, ESM-2 for SARS-CoV-2/RSV, homoplasy for Norovirus)" 추가 |
| M4 | ch6 line 16 ("PAHD-R redesign") | "PAHD-R redesign translates these findings into a conservative evidence-fusion workflow" — abstract와 ch1 어느 곳에도 PAHD-R는 등장하지 않음. PAHD-R은 ch5(line 199-203)에서 처음 도입되어 ch6 (line 16, 73)로 직진. **결론에서 abstract/intro에 없던 새 framework가 결론에서 contribution으로 재진술됨은 reviewer "scope creep"으로 의심**. abstract Contribution 1/2/3a/3b 어디에도 PAHD-R가 없으므로 ch6 line 16의 "PAHD-R redesign translates these findings"는 (i) abstract에 PAHD-R 추가하든지 (ii) ch6에서 PAHD-R가 contribution이 아니라 ch5 discussion 산물임을 명시 | ch6:16, 70-74 vs abstract.tex (전체 PAHD-R 부재), ch1 (PAHD-R 부재) | ch6 line 16을 "Building on these findings, the PAHD-R synthesis (Chapter~\ref{ch:discussion}) demonstrates feasibility …" 처럼 ch5 산물로 재기술하거나, abstract에 한 줄 추가. 본 dissertation은 후자가 더 큰 변경이라 전자 권장 |
| M5 | ch6 line 12, 89 | $\omega^2=0.296$ 의 95\% CI [0.195, 0.333]를 ch6에서 누락. abstract line 2,10과 ch1 line 142,148 모두 "11-pathogen cluster-bootstrap 95\% interval [0.195, 0.333]" 명시. 결론은 통상 main text보다 더 간결할 수 있지만, 핵심 effect size의 CI를 결론에서 제시하는 것이 표준 practice (Bayesian HDI [0.188, 0.314]도 ch5 line 285에 보고됨) | ch6:12, 89 vs abstract:2, ch1:148, ch4:563 | ch6 line 12에 "$\omega^2=0.296$ (95\% cluster-bootstrap CI [0.195, 0.333])" 표기 |
| M6 | ch6 line 91 | "the dissertation **confirms a feasible direction** for adaptive evidence fusion, not a universal adaptive predictor" — "confirms"는 매우 강한 단정어. ch5 line 197 "These are complementary operating regimes, not a single validated universal adaptive algorithm", ch4 line 936 "oracle strategy approximately doubles EqualWeight performance, confirming that per-pathogen weighting provides genuine improvement" 와 비교했을 때 ch6의 "confirms" 사용은 조심스럽지만 "feasible direction"은 evidence가 oracle gap (0.160 vs 0.083) 한 점뿐이라는 점에서 "confirms"보다 "evidences" 또는 "suggests" 가 안전 | ch6:91 vs ch4:936, ch5:197 | ch6 line 91: "confirms" → "evidences" (또는 "supports") 권장. "the dissertation evidences a feasible direction for adaptive evidence fusion" |

---

## Minor

| ID | 위치 | 문제 | 근거 | 수정 |
|---|---|---|---|---|
| m1 | ch6 line 11 | "(literature-curated adaptive positives, constrained negatives, and DMS fitness where available)" — Layer A의 정확한 정의가 abstract line 6, ch1 line 143과 다름. 표준 표현은 "Layer A: a pathogen-specific union of convergent-evolution, immune-escape, and HVR-membership evidence types, with immune-escape positions dominating". ch6 표현 "literature-curated adaptive positives"는 더 일반적인 단어로 압축되어 있어 reviewer가 "adaptive"가 abstract의 "convergent-evolution + immune-escape + HVR" union임을 즉시 매핑하기 어려움 | ch6:11 vs abstract:6, ch1:143 | ch6 line 11을 "literature-curated Layer~A positives (union of convergent-evolution, immune-escape, and HVR evidence)" 로 정확화 |
| m2 | ch6 line 14 | "the H3N2 integration case yields 4.012-fold escape enrichment" — $p=0.0023$ 빠짐. abstract line 11, ch1 line 150은 모두 "$p=0.0023$" 동반. 결론에서 effect size를 보고할 때 p-value 제시는 표준 | ch6:14 vs abstract:11, ch1:150, ch4:878 | ch6 line 14: "4.012-fold escape enrichment ($p=0.0023$)" |
| m3 | ch6 line 70 ("PAHD-R") 단락 | "13-dimensional profile space" — ch5 line 285의 Bayesian model이나 다른 통계 부분에서 명시되지 않은 dimension. ch5 어디에서도 "13-dimensional profile space"의 출처를 찾을 수 없음. 만약 이것이 13개 pathogen profile features 라면 source가 결론에 처음 등장하는 것은 부적절 | ch6:72 (단어 "13-dimensional profile space") vs ch5 전체 (직접 언급 없음 추정) | ch5 line 285 또는 ch4 ch5 어딘가에서 13차원 프로파일이 정의되어야 함. 정의가 없으면 "13-dimensional" 삭제 또는 "high-dimensional" 로 변경 |
| m4 | ch6 line 78 | "Homoplasy-based scoring captures signals distinct from frequency (simulation $\rho=-0.876$; real GISAID $\rho=-0.107$)" — ch4 line 254 (in ch5)에서 인용 정확. 그러나 ch6는 simulation $\rho=-0.876$의 의미를 모호하게 인용. 단순히 "distinct"를 보이려는 점에서는 OK이나, $\rho=-0.876$은 강한 음의 상관, $\rho=-0.107$은 약한 음의 상관 — 두 값이 서로 다른 signal regime을 가진다는 점이 누락 | ch6:78 vs ch5:254 | ch6 line 78에 "(simulation $\rho=-0.876$, strong negative; real GISAID $\rho=-0.107$, weak)" 정도 첨가. 또는 그냥 그대로 유지 (Minor) |
| m5 | ch6 line 73 | "HCV E2 is the only adopted optional repair" — ch5 line 203 "HCV E2 is adopted after coordinate reconciliation, while SARS-CoV-2 RBD/ACE2 and MERS DPP4/contact remain candidates and RSV remains unrepaired"와 일치하지만, ch4 line 950 "HCV E2 coordinate reconciliation is adopted as an optional repair (exact MCC 0.5257, FPR 0.0000)" — 즉 단순한 "the only adopted optional repair" 보다는 ch5/ch4의 "after coordinate reconciliation" 문맥을 살리면 좋음 | ch6:73 vs ch5:203, ch4:950 | ch6 line 73: "HCV E2 (after coordinate reconciliation) is the only adopted optional repair" |
| m6 | ch6 line 92 ("Take-home message") | 강조 표현 "explains more performance variance than choosing among detection algorithms" — 정확히는 "$\omega^2_{scoring \times pathogen}=0.296$ vs detection-family main effect" 비교가 main-effect 한정이지, 종합적인 detection-algorithm contribution 비교는 아님. ch4 line 392 "scoring~$\times$~pathogen (0.296), pathogen (0.117), and family~$\times$~pathogen (0.082)" 보면 family$\times$pathogen 0.082는 still substantial한 detection-algorithm effect | ch6:92 vs ch4:392 | "explains more performance variance than choosing among detection algorithms alone" 또는 "than the detection-algorithm main effect" 처럼 main effect 한정 |
| m7 | ch6 line 16 | "without claiming a completed universal adaptive predictor" — ch6 line 91도 "not a universal adaptive predictor". "completed universal adaptive predictor" 와 "universal adaptive predictor" 두 표현이 ch6 안에서 다르게 출현. 통일 권장 | ch6:16 vs ch6:91 | "without claiming a universal adaptive predictor" 로 통일 |
| m8 | ch6 line 70-83 (Future Research Directions) | 본문 단락 "Pathogen-Aware Adaptive Method Selection" / "Integration of Phylogenetic Correction" / "Additional Research Directions" 가 Table~\ref{tab:future_roadmap} (Priority 1-4)와 1-1 매핑되지 않음. 표는 (1) Phylogenetic/time correction, (2) Adaptive method selection, (3) Scope extension, (4) Reproduction and release 인 반면, 본문은 (a) Adaptive Method Selection, (b) Phylogenetic Correction, (c) Additional Directions. **Priority 4 (Reproduction and release) 가 본문 단락에서 사라짐** | ch6:60-67 (Table) vs ch6:70-83 (단락) | 본문에 Priority 4 (Reproduction/release) 단락 1-2줄 추가하거나 표/본문 연결 명시 |
| m9 | ch6 line 90 | "self-consistency evidence" 와 "self-consistency check" 표현이 dissertation 전반에서 혼용. abstract line 11 "self-consistency check", ch1 line 150 "self-consistency check", ch6 line 15 "self-consistency check", ch6 line 90 "self-consistency evidence". 통일 권장 | ch6:15 vs ch6:90 | "self-consistency check" 로 통일 |

---

## Contribution 일관성 매트릭스

| Contribution | abstract 표현 | ch1 표현 | ch6 표현 | 일치? | 강도 차이 |
|---|---|---|---|---|---|
| **C1: MutBench benchmark** | "MutBench is the broadest \emph{region-level hotspot-detection} benchmark to date" + "10 info types (20 scoring) × 14 detection families (39 variants) × 11 pathogens = 8,580 evals" + "3-layer GT + hotspot-score + 2-stage design" (abstract:2,4-8) | "To our knowledge, MutBench is the broadest hotspot-detection benchmark to date" + "10 info types into 20 scoring formulas across 6 categories" + "3-layer ground truth" + "hotspot-score composite metric" + "2-stage design" (ch1:142-143) | "MutBench provides a benchmark for viral mutation hotspot detection across 11 RNA viruses, combining 20 scoring formulas, 39 detector variants, and a three-layer ground truth (literature-curated adaptive positives, constrained negatives, and DMS fitness where available)" (ch6:11) | **Partial** | ch6 약화: (a) "broadest"/"to our knowledge" 제거, (b) "10 information types" 누락, (c) "14 detection families" 누락, (d) "8,580 evaluations" 누락, (e) hotspot-score metric 명시 누락, (f) "2-stage design" 누락. **결론은 abstract보다 약하게 표현됨** |
| **C2: Pathogen-dependent optimal info source** | "$\omega^2=0.296$ (CI [0.195, 0.333]; 6-cat=0.103; residual≈0.39)" + "Friedman $p=0.990$" + "LOPO 0/11" + "0.265 oracle gap" + "9 distinct optimal info types" (abstract:10,13) | "$\omega^2=0.296$ (CI [0.195, 0.333]; 6-cat=0.103)" + "9 distinct" + "FUBAR/PLM/homoplasy 예시" + "Friedman $p=0.990$" + "LOPO 0/11" (ch1:145-148) | "$\omega^2=0.296$ at 20-type granularity; 0.103 at 6-category granularity" + "9 distinct optimal info types" + "0.265 gap" + "LOPO 0/11 and Friedman $p=0.990$ are null-consistent corroboration" (ch6:12-13) | **Mostly aligned** | ch6 누락: (a) CI [0.195, 0.333], (b) within-cell residual $\omega^2\approx 0.39$, (c) Friedman $\chi^2=7.69$ 수치, (d) FUBAR/PLM/homoplasy 예시. ch6 언어 변경: "Friedman + LOPO 모두 null-consistent corroboration" — 이는 Friedman의 의미 왜곡 (M2 참조) |
| **C3a: Multi-source integration infrastructure** | "4-feature core captures ≈98\% (97.6\%) of 10-feature ensemble; EqualWeight H3N2 enrichment 4.012× ($p=0.0023$)" (abstract:11) | "4-feature core (homoplasy, pLDDT, entropy, frequency) retains ≈98\% (97.6\%, 0.081/0.083 mean MCC) of full 10-feature EqualWeight ensemble on 12-pathogen Stage 3 panel under uniform-weight LOPO top-10\% (numerical equivalence, no paired-test significance), and EqualWeight 4.012-fold H3N2 enrichment ($p=0.0023$) within top-5 integration comparison" (ch1:150) | "the 4-feature core (homoplasy, pLDDT, entropy, frequency) retains 97.6\% of the 10-feature EqualWeight ensemble mean MCC, and the H3N2 integration case yields 4.012-fold escape enrichment" (ch6:14) | **Partial** | ch6 누락: (a) 0.081/0.083 mean MCC 절대값, (b) 12-pathogen Stage 3 panel scope, (c) "uniform-weight LOPO top-10\%" protocol, (d) "numerical equivalence, no paired-test" caveat, (e) $p=0.0023$ for 4.012×, (f) "within top-5 integration comparison" scope. **ch6는 caveat을 모두 제거하여 더 강한 어조** |
| **C3b: External validation (HIV-1)** | "three-tier evidence rule (Bonferroni × Layer A overlap < 33\%); HIV-1 primary anchor with novel-only $7.16\text{--}8.24\times$ on 37 Layer A-disjoint positions ($p=5\times 10^{-12}$); H3N2 ($9.36\times$, 69\% overlap) self-consistency; SARS-CoV-2 ($7.63\times$) exploratory after Bonferroni; 3/11 pathogens (2,340 evals)" (abstract:11) | "Layer A-disjoint subset (37/45) yields novel-only $7.16\text{--}8.24\times$ ($p_{adj}\approx 3.9\times 10^{-9}$ across 780 combos; nominal $5\times 10^{-12}$); H3N2 9.36× self-consistency; SARS-CoV-2 exploratory" + circularity audit reference (ch1:150,153) | "External validation is anchored by HIV-1, where the escape set is largely Layer A-disjoint (82\%) and yields 7.19-fold enrichment after correction; H3N2 self-consistency, SARS-CoV-2 exploratory" (ch6:15) + Concluding Remarks "7.19×, 82\% Layer A-disjoint" (ch6:90) | **Mismatch** | ch6는 "7.19×" 만 보고 — 이는 abstract/ch1의 **full set 값**. 그러나 ch6 line 15는 "Layer A-disjoint (82\%)" + "7.19×" 를 결합하여 7.19×가 novel-only인지 full set인지 모호. abstract Contribution 3b는 명시적으로 novel-only $7.16\text{--}8.24\times$ 를 anchor로 삼음. **ch6 표현은 (a) 두 수치 분리 누락, (b) 9.36× 값 누락, (c) 7.16-8.24× 명시 누락, (d) 2,340 evals scope 누락** (Critical C2 참조) |
| **Contribution count** | "Contribution 1, 2, 3 (two-part: 3a, 3b)" — 명시적 4-part 표현 (abstract:11) | "Contribution 1, 2, 3 (two-part)" — 명시적 4-part (ch1:150) | "First, Second, Third" — 단순 3-part (ch6:10-14) | **Mismatch** | abstract/ch1는 explicit "two-part" 표시, ch6는 단일 "Third"로 통합. Contribution 3a vs 3b 분리 표시 부재 (Critical C3 참조) |

---

## 수치 일관성 매트릭스 (ch6 vs 다른 위치)

| 수치 | ch6 | abstract | ch1 | ch4 | 일치? |
|---|---|---|---|---|---|
| $\omega^2_{scoring\times pathogen}$ (20-type) | 0.296 (line 12, 89) | 0.296 (line 2, 10) | 0.296 (line 145, 148) | 0.296 (line 11, 368, 386, 390, 394, 396, 563, 970) | **Pass** (값 일치). ch6는 CI 누락 (Major M5) |
| $\omega^2$ (6-category) | 0.103 (line 12) | 0.103 (line 10) | 0.103 (line 148) | 0.103 (ch5:281), ch4 본문에는 없음 | **Pass** |
| Within-cell residual $\omega^2$ | (없음) | $\approx 0.39$ (line 10) | $\approx 0.39$ (line 148) | $\approx 0.39$ (line 361, 386, 390, 394, 396, 563, 970) | ch6 누락 — Major M5 |
| 95\% CI [0.195, 0.333] | (없음) | [0.195, 0.333] (line 2, 10) | [0.195, 0.333] (line 148) | [0.195, 0.333] (line 394, 563, 970) | ch6 누락 — Major M5 |
| Friedman $\chi^2$, $p$ | $p=0.990$ (line 13, $\chi^2$ 미표기) | $\chi^2=7.69, p=0.990$ (line 10) | $p=0.990$ (line 147, $\chi^2$ 미표기) | $\chi^2=7.69, p=0.990$ (line 394) | **Pass** ($p$ 값 일치, $\chi^2$ 부분 누락) |
| LOPO 0/11 + null-consistent | "0/11 ... null-consistent corroboration" (line 13) | "0/11 ... null-consistent under permutation" (line 10) | "0/11 matches ... null-consistent under permutation" (line 145, 148) | "0/11 ... null-consistent ... $P\approx 0.96$" (line 423, 565) | **Pass** (의미 일치). 단 ch6는 Friedman과 묶어서 표현 — Major M2 |
| Oracle-vs-generalized MCC gap | 0.265 (line 12) | 0.265 (line 10) | (ch1에는 직접 표기 없음) | 0.265 (line 301, 414, 427, 440, 442, 970) | **Pass** |
| Oracle MCC ceiling | 0.160 (line 72) | (없음) | (없음) | 0.160 (line 936) | **Pass** (ch6와 ch4 일치) |
| EqualWeight MCC | 0.083 (line 72) | (없음) | 0.083 (line 150, "0.081/0.083") | 0.083 (line 769, 782, 798, 801, 854, 936, 961, 963) | **Pass** |
| 4-feature core retention | 97.6\% (line 14) | "≈98\% (97.6\%)" (line 11, 14) | "≈98\% (97.6\%, 0.081/0.083)" (line 150, 152) | 97.6\% (line 801, 961, 971), "98\%" (ch5:215, 244) | **Pass** (값 일치). ch6는 0.081/0.083 절대값 누락 (Critical C4) |
| H3N2 enrichment | 4.012× (line 14, table) | 4.012× ($p=0.0023$, line 11, 14) | 4.012× ($p=0.0023$, line 150, 153) | 4.012× ($p=0.0023$, line 878, 893, 962) | **Pass** (값 일치). ch6는 $p=0.0023$ 누락 — Minor m2 |
| HIV-1 full set enrichment | 7.19× (line 15, 90) | 7.19× ($p=2.5\times 10^{-16}$, line 2, 11) | 7.19× ($p=2.5\times 10^{-16}$, line 150, 153) | 7.19× ($p<0.0001$, line 874, 891, 921) | **Pass** (값 일치) BUT ch6는 full set인지 novel-only인지 모호 + Bonferroni $p$ 누락 — Critical C2 |
| HIV-1 novel-only | (없음 — 7.19만 보고) | $7.16\text{--}8.24\times$ ($p=5\times 10^{-12}$, line 11, 14) | $7.16\text{--}8.24\times$ (line 117, 150, 153) | $7.16\text{--}8.24\times$ (line 886, 921) | **ch6 누락** — Critical C2 |
| HIV-1 Layer A-disjoint % | 82\% (line 15, 90) | 82\% (line 11) | 82\% (line 153, 921) | 82\% (line 891, 921) | **Pass** |
| H3N2 9.36× | (없음 — 본문에서 표기 안 함) | 9.36× (line 11) | 9.36× (line 150, 153) | 9.36× (line 873, 891, 893) | **ch6 누락** — Major M3/M5 (단순 "self-consistency check"만 보고) |
| SARS-CoV-2 7.63× | (없음) | 7.63× (line 11) | (ch1 본문 직접 없음) | 7.63× (line 921) | ch6 누락 (의도적이라면 OK; "exploratory" 으로 처리) |
| 9 distinct info types | "9 distinct optimal information types" (line 12, 89) | "9 distinct" (line 13) | "9 distinct" (line 145-146, 148) | "9 distinct" (line 272, 565, 749, 891, 960) | **Pass** |
| Hotspot-score 0.778 | (없음) | 0.778 (line 10) | (없음) | (Stage 1) | OK (ch6는 Stage 2/3 결론에 집중) |
| 8,580 evaluations | (line 105 — code/data 단락에만) | 8,580 (line 2) | 8,580 (line 33, 82) | 8,580 (line 394, 970) | ch6 본문(Contribution 1)에는 누락 — Major M1 |

---

## 챕터 종합 평가

**합격선: CONDITIONAL** — 수치 정확성은 대체로 일치하나 (ω²=0.296, 4.012×, 0.265 gap, 97.6\% 등 핵심 값 모두 일치), **Contribution 재진술의 구조적 일관성**과 **HIV-1 enrichment 표현 정확성**이 abstract/ch1 대비 심각하게 약화. 박사논문 결론은 abstract와 동일 강도로 contribution을 재선언해야 함.

**핵심 문제 요약**:

1. **Contribution 1 (C1, M1)**: ch6는 "broadest"/"to our knowledge" 표현을 삭제하고 핵심 grid 차원 (10 info types, 14 detection families, 8,580 evals)을 누락. abstract와 ch1은 모두 "MutBench is the broadest" first-claim 명시. 결론에서 first-claim 약화는 reviewer가 "claim 변경" 또는 "약한 결론"으로 해석 가능.

2. **Contribution 3 분할 (C3)**: abstract와 ch1은 "Contribution 3 is two-part" (3a infrastructure / 3b external validation)을 명시. ch6는 단일 "Third" 단락으로 통합 — Contribution count가 4 vs 3으로 다르게 읽힘.

3. **HIV-1 enrichment 모호성 (C2, 매트릭스 HIV-1 행)**: abstract는 full set 7.19× (Bonferroni $p_{adj}=2.5\times10^{-16}$) 와 novel-only $7.16\text{--}8.24\times$를 분리. ch6는 단지 "7.19-fold enrichment after correction" — full set인지 novel-only인지 모호. abstract Contribution 3b의 anchor는 novel-only $7.16\text{--}8.24\times$이므로 ch6는 abstract anchor를 약화.

4. **Caveat 누락 (C4, M3)**: ch6는 4-feature core 97.6\%의 "numerical equivalence, no paired-test significance" caveat 제거, "12-pathogen Stage 3 panel" scope 제거. ch1 line 150에는 명시. **결론에서 caveat 제거 → reviewer가 "결론에서 strengthening" 의심**.

5. **PAHD-R scope creep (M4)**: PAHD-R는 abstract와 ch1 어느 곳에도 없음 (ch5에서 처음 도입). ch6 line 16 "PAHD-R redesign translates these findings"는 결론에서 새 contribution-like framework 등장으로 읽힘. ch5 산물임을 명시하거나 abstract에 한 줄 추가 필요.

6. **Friedman 의미 왜곡 (M2)**: "Friedman $p=0.990$ ... null-consistent corroboration" — Friedman의 정확한 의미는 "no universally best combination". null-consistent는 LOPO에 적용. 표현 분리 필요.

**합격 조건**: Critical 4건 (C1-C4) 전부 수정 + Major 6건 중 적어도 4건 (특히 M1, M2, M3, M4) 수정 시 PASS. Minor는 cosmetic 수준이라 후순위.

**수치 일관성 자체는 PASS**: ω²=0.296, 0.265 gap, 0.083/0.160 oracle, 4.012× ($p=0.0023$ 누락 외), 97.6\%, 82\% — 모든 핵심 수치가 abstract/ch1/ch4와 정확히 일치. 단, ch6 본문에서 핵심 수치들의 **caveat (CI, residual, $p$-value)가 체계적으로 누락**되어 결론이 abstract보다 더 단정적으로 읽히는 inflation 위험이 있음.

**과대해석/단정 표현 점검**:
- ch6 line 88 "is driven more by the fit between pathogen and biological information source than by detector choice alone" — abstract/ch1과 일치, OK
- ch6 line 91 "the dissertation **confirms** a feasible direction" — "confirms"는 강함, "evidences"가 안전 (M6)
- ch6 line 92 take-home "explains more performance variance than choosing among detection algorithms" — main effect 한정 명시 필요 (m6)
- ch6 line 16 "without claiming a completed universal adaptive predictor" / line 91 "not a universal adaptive predictor" — limitations honest, OK

**Limitations honesty**: ch6 Table tab:limitations_summary는 6개 항목 모두 ch5와 일관 (HIV-1 anchor, GT incompleteness, sampling bias, metric stringency, small panel, scope) — 약화 없음. **Limitations 정직성 PASS**.

**Future work alignment**: ch6 Future Roadmap (Priority 1-4)와 ch5 future work (TreeTime/UShER, 20-30 pathogens, DNA virus, indel, reproduction)이 정합. 단 ch6 본문 단락에서 Priority 4 (Reproduction/release)가 빠짐 (m8).

**Practical impact 근거**: ch6 line 94 "vaccine-strain selection, surveillance triage, and antibody design" — ch4 vaccine-escape 결과 (HIV-1 7.19×, H3N2 4.012×) 와 ch5 practical workflow (line 192) 에서 근거 있음. Dual-use considerations 단락도 적절. **Practical impact 근거 PASS**.

저장 위치: `/proj/paper/paper/dissertation/review/2026-04-28/phase2b_ch6.md`
