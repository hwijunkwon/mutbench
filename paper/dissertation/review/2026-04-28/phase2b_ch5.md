# Ch5 Discussion 심층 검토

대상: `/proj/paper/paper/dissertation/chapters_en/ch5_discussion.tex` (336 lines)
검토일: 2026-04-28
검토 유형: 심층 적대적 검토 (한계 인식, 회로성, future work, generalization)

---

## Critical (한계 누락 / 결과 과대 일반화)

| ID | 위치 | 문제 | 근거 | 수정 |
|----|------|------|------|------|
| C1 | L33–35 (회로성) | **두 ρ 값(0.97 vs 0.12)의 disambiguation이 본문에서 완전히 누락**. Layer A 회로성 토의에서 point-biserial $\rho=0.12$ (Layer A 멤버십 ↔ per-position frequency)만 인용되고, ch4_results.tex L696·L739에서 보고된 freq-entropy 상관 $\rho=0.97$은 별개 맥락(feature-level Pearson)임에도 동일 ρ로 혼동될 위험. 독자는 "회로성 0.12"와 "feature-level 0.97"의 의미 차이를 모르고 결합할 수 있음 | L33의 "$|\rho|=0.12$"는 점-biserial(이진 GT vs 연속 score), L696·L739의 "$\rho=0.97$"은 feature-feature Pearson — 두 ρ를 나란히 언급한 곳 없음 | L33 직후 1문장 추가: "This per-position $\rho$ is conceptually distinct from the feature--feature Pearson correlations reported in Section~\ref{sec:feature_correlation} (e.g., freq--entropy $\rho = 0.97$), which describe redundancy among scoring inputs rather than circularity with ground truth." |
| C2 | L33–35 (회로성) | Layer A 회로성을 "pathogen-specific"으로 풀어주지만, **이로부터 따라오는 결과 해석의 비대칭성을 한계로 명시하지 않음**. HCV(+0.33), Influenza B(+0.26), Norovirus(+0.23)에서 frequency 기반 method의 우월한 성능은 부분적으로 회로성에 기인. 그런데 Table나 다른 곳에서 "HCV best = frequency"로 보고할 때 이 회로성 디스카운트 적용 안 함 | L33: "frequency $\approx$ Layer~A by construction" 으로만 모호하게 처리. HCV·Norovirus에서 frequency가 1위인 결과(L323)와 이 회로성 사이의 연결 끊김 | "Implication: HCV's frequency-best ranking and Norovirus's epochal-variant Layer~A define-frequency-as-correct relationship mean that these pathogens' rankings should be discounted as partially structural rather than mechanistically interpreted." 추가 |
| C3 | L84 ("11 RNA viruses … stronger practical evidence … than the abstract theorem alone") | **NFL (Wolpert 1997)의 일반화 주장이 11종 RNA virus → "stronger practical evidence"로 비약**. NFL은 "all problem distributions"에 대한 부정 진술이고, 11 RNA virus 결과는 NFL의 *empirical demonstration이 아니라 한 specific class에서의 algorithm-selection 필요성*을 보일 뿐. "stronger evidence than abstract theorem" 표현은 잘못된 비교 | L84: "stronger practical evidence for pathogen-adaptive selection than the abstract theorem alone" — NFL은 "method selection이 필요하다"가 아니라 "범용 best가 없다"의 진술. 11 case가 NFL 자체를 보강하지 않음 | "stronger practical evidence" → "complementary practical evidence within a biologically meaningful problem class, while NFL itself remains a statement about all possible problem distributions and is neither tested nor strengthened by 11 cases" |
| C4 | 전반 | **External independent reproduction 부재 한계가 1문장(L287)으로만 언급되고, 이로부터 따라오는 결과 신뢰도 디스카운트는 명시 안 됨**. "queued for next cycle"이라는 약속만 있을 뿐 *현재 결과의 어떤 claim을 약화시키는가*가 빠짐 | L287: "queued for the next cycle (Priority~5)"만 적시. ω²=0.296, oracle MCC 0.341, HIV-1 7.19× 등 핵심 수치 어느 것이 single-team artifact 영향을 받는지 매핑 없음 | "Until independent reproduction is completed, the headline interaction effect ($\omega^2 = 0.296$), oracle MCC means, and family-level recommendations should be treated as single-team-single-snapshot estimates; the relative orderings are more robust than the absolute magnitudes." |
| C5 | L319 ("scope") + L283 (winner's curse) | **11-cluster rule-of-thumb 미달 자체가 한 곳에 집약 진술되지 않음**. Bolker (≥5–6) 인용은 L285에 있지만, "11종이 cluster-level 추론에 대해 sub-threshold"라는 직접 진술은 없음. L321이 가장 가깝지만 LOPO에 한정 | L285: Bolker는 인용되나 11이 그 기준 위 vs 아래인지 모호. "feasible by Bolker criterion" 표현은 *현재 11도 만족*인지 *20–30이 되어야*인지 헷갈림 | L319 또는 L321 끝에: "The 11-pathogen panel meets Bolker et al.'s minimum (5--6) for fixed-effect ANOVA blocks but is below the typical recommendation for stable mixed-effects estimation; cluster-level conclusions should therefore be treated as preliminary." |
| C6 | L17, L155, L162 등 (cold-start / EqualWeight 4-feature) | **97.6% / 98% retention 주장의 통계적 근거 부재 명시는 L244에서만**: "no paired-sample significance test was performed". 그런데 L17·L162·L196에서는 단언적("retains ≈98%")으로 표현 → 같은 챕터 내 inconsistency | L162: "the 4-feature core retains $\approx$98\% of its mean MCC" (단언) vs L244: "numerical rather than statistical equivalence claim" | L162·L196에 "(numerical only; no significance test, see Sec.~\ref{sec:practical_workflow})" 추가하여 일관성 확보 |
| C7 | L33 (회로성) | **Layer A 정의 비대칭(C 카테고리)을 회로성 토의 안에 포함시키지 않음**. 회로성 효과는 정의 비대칭의 *결과*인데, 정의 비대칭 자체는 sec:gt_heterogeneity (L300)에서 별도로 다루어짐 → 두 한계가 분리되어 독자는 회로성과 정의 비대칭의 logical chain을 못 이음 | L33의 "ground-truth curation style" → L300의 "heterogeneity in how Layer~A is defined" 사이 cross-reference 없음 | L33 끝: "This pathogen-specific circularity is itself a downstream consequence of the Layer~A curation heterogeneity discussed in Section~\ref{sec:gt_heterogeneity}." |

---

## Major

| ID | 위치 | 문제 | 근거 | 수정 |
|----|------|------|------|------|
| M1 | L17 ("Future work should expand…") | **Future work 구체성 부족**: "additional protein domains (e.g., ORF1ab, N protein)"만 제시. 몇 개 도메인이면 BCa CI half-width가 어느 정도까지 줄어드는지, 어떤 sample size가 target인지 부재 | L17은 "expand the effective sample size" 1문장으로 종결 | "Targeting at least $n=20$ region-level samples (e.g., adding 13 SARS-CoV-2 genome-wide ORFs) would halve the BCa half-width under the same resampling design (linear approximation)." |
| M2 | L48 ("appropriate temporal resolution remains a future challenge") | **너무 일반론**. TC-freq의 적정 window가 4주(L190 cited), 26주(L267), 또는 다른 값인지 — 본문 다른 곳에서 4주 minimum을 제시하면서 여기서는 미정으로 처리 → 모순 | L190: "minimum 4-week window is required" / L48: "appropriate temporal resolution remains a future challenge" | L48: "appropriate temporal resolution beyond the 4-week minimum (Section~\ref{sec:practical_surveillance}) — specifically the trade-off between detection latency and noise for 4-, 12-, and 26-week windows — remains a future challenge." |
| M3 | L156–166 (Vaccine Escape) | **Discussion vs Results 중복 과다**: 9.36×, 7.19×, 7.63×, $p_{\text{adj}}=2.5\times 10^{-16}$ 등 수치를 ch4 Table 8.x에서 그대로 재진술 → 진정한 "interpretation/integration" 비중 낮음 | L161–162에서 ch4 결과를 거의 통째로 재인용 | 수치는 줄이고 *implication* 강조: "These three pathogens span three distinct evidential roles — primary anchor (HIV-1), self-consistency probe (H3N2), exploratory signal (SARS-CoV-2) — and a benchmark relying on a single anchor pathogen is methodologically vulnerable, motivating the multi-anchor expansion proposed in Chapter~\ref{ch:conclusion}." |
| M4 | L84 (NFL + Rice) | **자기-인용 과잉 / 자기-강조**: "stronger practical evidence … than the abstract theorem alone"는 학술적 겸손 결여. NFL/Rice 인용을 자기 결과의 *일반화 보강*으로 사용. Discussion에서는 *제한*이 더 적절 | L84: 단일 문장에서 NFL과 Rice 두 시그니처 인용 + "stronger evidence" + "practical implications" 누적 | "stronger practical evidence … than the abstract theorem alone" → "an empirical instance consistent with NFL's prediction within a specific problem class, without claiming to generalize NFL beyond it" |
| M5 | L161 + L162 | **EqualWeight integration enrichment 4.012× (L162)와 stage 2 sweep 단독-feature top 7.19× (L161)이 한 문단에서 어떻게 비교되는지 불분명**. "single-feature approaches do not [survive Bonferroni]"는 statement가 disambiguation 괄호로 보호되긴 했으나, 일반 독자에게는 "통합이 단일보다 좋다 vs 통합 4.012가 단일 7.19보다 작다"로 모순처럼 보임 | L162: 두 문장이 인접해 비교 의미가 흐려짐 | "stage 2 single-feature 7.19× and integration-block 4.012× are not directly comparable: the former selects the per-pathogen best of 780 combinations (winner's-curse-prone), the latter is a fixed 10-feature uniform-weight ensemble (winner's-curse-free)." |
| M6 | L155 (Contribution recap) | **3 contributions 재진술이 introduction과 거의 동일**. "Returning to the three problems" 형태는 Discussion 첫 문단에 한 번이면 충분. L5에서 이미 "interprets the results … and discusses methodological implications" 선언했으므로 중복 | L5와 L155 모두 "ch1으로 돌아간다"는 narrative 사용 | L155 1문장으로 축소 또는 conclusion으로 이동 |
| M7 | L194–203 (PAHD-R 단락) | **PAHD-R는 ch5에서 처음 등장 — Discussion에서 새 시스템 정의는 anti-pattern**. "PAHD-R as a bounded synthesis" 문단은 chapter 6으로 이동되어야 (논문은 "future framework"를 Discussion에서 신규 도입하지 말아야) | L199: "PAHD-R narrows the gap between the ceiling and floor" — 이 시스템이 Results에서 정의/검증되었는지 불명. Core/Augmented/Review 3 modes는 ch5에서 처음 등장 | (a) PAHD-R가 Results에서 정의되었다면 그 reference 추가, (b) 정의되지 않았다면 PAHD-R 단락을 ch6 future work로 이동 |
| M8 | L162–164 ("MutBench provides practical value through three mechanisms") | **반론 anticipation 불완전**: "LOPO 0/11 generalization 실패"라는 negative 결과를 가지고 있는데, 이를 "그래도 practical value 있다"로 변호. 그러나 reviewer가 "LOPO 0/11이면 *왜 method selection algorithm 없이도* 진단적이라고 부를 수 있나?"를 물을 때 답변 부족 | L163–164: "(1) family-level recommendation (2) 4-feature core (3) 25-second exhaustive sweep" — 모두 *대안*이지 LOPO 실패의 *수습*은 아님 | "An anticipated objection: if LOPO yields 0/11, why call MutBench prescriptive? Response: MutBench is descriptive (it characterizes the (scoring, pathogen) landscape) and prescriptive only in the weak sense (family-level priors + cold-start ensemble). Strong prescription would require a validated meta-learner mapping pathogen genomic features → optimal combination, which is explicitly future work." |
| M9 | L283 (winner's curse) | **불확실성 정량화는 잘 되어 있으나, mitigation으로 제시된 "9 distinct scoring types from 4 of 6 categories" → "much lower random probability"는 정량화 부재**. 정확한 multinomial coefficient 또는 simulation 결과 없음 | L283: "(1) 9 distinct scoring types from 4 of 6 categories, which has much lower random probability" — "much lower" 정량화 없음 | 다음 중 하나: (a) "approximately $7.4 \times 10^{-3}$ under category-uniform sampling" (계산), (b) "(simulation deferred)", (c) Mitigation 항목에서 제거 |
| M10 | L271–277 (ESM-2 leakage) | **leakage 한계가 "uniform across all pathogens" claim으로 dismiss됨**. 그러나 leakage의 *uniformity*는 검증 안 됨: SARS-CoV-2가 UniRef에 압도적으로 많이 representation되어 있으면 leakage도 비대칭 | L275: "this concern applies uniformly to all 11 pathogens" — 가정에 불과 | "Note that 'uniform' is an assumption rather than a quantified claim: the magnitude of leakage likely scales with the volume of pathogen-specific sequences in UniRef50/90 (e.g., SARS-CoV-2 likely overrepresented post-2020), and a per-pathogen leakage audit is deferred to future work." |
| M11 | L290 (technical-covariate ANCOVA) | **결과 자체는 견고하지만 표현이 과도하게 reassuring**. "interaction is amplified rather than attenuated by technical-covariate adjustment"는 사실이지만, 0.234 → 0.264 +0.030 shift를 "amplified"라고 부르기엔 미미 | L290: "interaction \emph{rises} from $\omega^2 = 0.234$ … to $\omega^2 = 0.264$" — 0.030 변화를 "amplified"로 표현 | "modestly rises by 0.030 (a sign-positive but small shift)" |
| M12 | L319 (LOPO 0/11 + Friedman p=0.990 결합) | **두 null 결과가 "sample size 부족 vs truly pathogen-specific" 양립하는 것은 정확하지만, 이 둘의 결합이 *어느 쪽 가설*에 더 무게를 두는지 명시 필요** | L319 + L321이 분리되어 두 null 결과가 일관적인지 약간 모호 | L321: "The combined evidence — LOPO 0/11, Friedman $p=0.990$, and oracle--generalized gap 0.265 MCC — is *jointly more compatible* with truly pathogen-specific optimality than with sample-size insufficiency, though neither alone is dispositive." |
| M13 | L155 (Contribution 1 재진술) | "the standardised evaluation framework is provided by the three-layer ground truth and hotspot-score metric" — 그러나 hotspot-score 자체의 한계(L46–48: saturation)는 같은 chapter에서 인정. 따라서 "Contribution 1"을 *제한 없이* recap하는 것은 self-contradictory | L155 vs L46–48 | L155: "Contribution~1 (the three-layer ground truth and hotspot-score metric, with the saturation caveat noted in Section~\ref{sec:hscore_saturation})" |

---

## Minor

| ID | 위치 | 문제 | 근거 | 수정 |
|----|------|------|------|------|
| m1 | L5–6 | "complementing the statistical evidence" — soft language 과다 | L5–6은 chapter introduction으로 적합하지만 "reinforces" + "complementing"은 hedge 중복 | "reinforces" 또는 "complements" 중 하나 선택 |
| m2 | L33 ("(+0.33), (+0.26) and (+0.23)") | HCV/Influenza B/Norovirus 3개만 명시 — 나머지 8 pathogen은 "$\approx 0$"으로 묶임. 연속체임에도 binary cutoff처럼 보임 | L33: 음의 ρ 한 개($-0.06$)와 양의 ρ 다수, 중간값 처리 부재 | "11 pathogens exhibit a continuum from $\rho=-0.06$ to $+0.33$; we group them at $|\rho|>0.2$ for narrative simplicity but emphasize the gradient." |
| m3 | L70 ("This mirrors the detection-level finding…") | "mirrors" — 주장 강도 약화 가능 | "mirrors" → "is consistent with" |
| m4 | L82 ("23 times smaller") | 0.013 vs 0.296 = 22.77배. 23은 반올림이지만 "approximately"가 빠짐 | L82: "approximately 23 times smaller" | 이미 "approximately" 있음 — OK, 무시 가능 |
| m5 | L162 (긴 paragraph) | 한 paragraph에 5+ 수치(9.36×, 7.19×, 7.63×, p_adj, 4.012×, 0.0023, 780, 4-feature 98%) — 가독성 저하 | L161–162가 sub-paragraph 분할 없는 25+ 줄 | 2 paragraphs로 분할 (Bonferroni 결과 / Integration 결과) |
| m6 | L189–192 | "minimum 4-week window" 근거가 "5 days generation time + 14 days submission delay"로만 제시 — 정확한 calculation은 부재 | L190: "minimum 4-week window is required for real-time TC-freq alerts" — 4주가 어떻게 5+14에서 도출되는지 불명 | "(2 generation times + submission delay $\approx 24$ days, rounded up to 4 weeks)" |
| m7 | L215 ("3--5 minutes per protein in the benchmark environment") | ESM-2 inference 시간이 "in the benchmark environment"로만 묶임 — RTX 3090 spec은 L243에서야 등장 | L215 vs L243 | L215에 "(NVIDIA RTX 3090 GPU)" 즉시 추가 |
| m8 | L244 | "NVIDIA RTX 3090" model이 future-proof하지 않음 (consumer GPU). 학위 논문에서는 *minimum spec*으로 기술 권장 | L243–244: 특정 GPU spec | "tested on a single consumer-class GPU (NVIDIA RTX 3090, 24GB VRAM); any GPU with $\geq$16GB VRAM should suffice for ESM-2 base-650M inference." |
| m9 | L262 ("over 80\%") | "High-income countries contribute over 80\%" — 인용은 chen2022gisaid이지만 "80\%" specific number는 시간이 흘러 변동 가능 | L262: "over 80\% of total sequences" | "over 80\% as of 2022~\cite{chen2022gisaid}" |
| m10 | L267 | "feature discriminative power changes substantially" — "substantially"는 정량화 모호 | L267: 0.337 → 0.472은 0.135 increase, AUC scale에서 "substantial"한지 명시 | "(absolute AUC change $+0.135$ over 12 months; effect size moderate-to-large for 1,259-position-scale comparisons)" |
| m11 | L285 (Bayesian hierarchical 결과) | 결과는 견고하나 paragraph 길이가 chapter 어느 곳보다 김 → 잠재적 sub-section화 권장 | L285는 단일 paragraph | "\paragraph{Bayesian hierarchical robustness check.}" 추가 |
| m12 | L292 ("$\omega^2 = 0.137$, still above Cohen's medium threshold despite the loss of statistical power") | 4 pathogens로 ω² 추정의 신뢰구간 부재 | L292: "n=4"에서 ω²=0.137 — CI 없음 | "(95\% CI omitted due to n=4; point estimate only)" |
| m13 | L301–308 (gt_heterogeneity) | "however, this heterogeneity reflects the real-world challenge" 식의 self-defense 톤 — Discussion의 한계 단락에서는 *방어*보다 *인정*이 더 효과적 | L307: "no single criterion … is applicable across all pathogens" — 한계인지 정당화인지 불명 | "We acknowledge that this is partly a definitional limitation of the framework, not solely a property of pathogen biology." |
| m14 | L319 "$p=0.990$" | Friedman p-value가 0.990 — 이는 *전혀 차이 없음*을 의미. "no single method can be reliably distinguished as superior across all pathogens"로 해석되는 게 맞으나, 일부 독자는 "p=0.990 = strong evidence FOR null"로 잘못 읽을 위험 | L319 | "(p=0.990, indicating that the data are uninformative for distinguishing among the 20 scoring types under Friedman's rank-block design; this is consistent with — but does not by itself prove — pathogen-specific optimality)" |
| m15 | L325–328 (PLM limitations) | "Recent work on CoVFit~\cite{covfit2025}, which fine-tunes ESM-2 on SARS-CoV-2 epidemiological and DMS data" — covfit2025 인용이 self-validating으로 사용됨 ("consistent with MutBench's central finding"). | L328: "consistent with MutBench's central finding" | "We note as a parallel observation, not as confirmation, that CoVFit's pathogen-specific PLM adaptation is consistent with the pathogen-dependent information principle here." |

---

## 한계 진술 체크리스트

| 한계 | 본문 언급 | 위치 | 강도 (충분/부분/누락) |
|------|----------|------|---------------------|
| Layer A 회로성 (frequency 상관) | O | L33–35 | **부분** — point-biserial $\rho=0.12$는 정량화되었으나, freq-feature $\rho=0.97$과의 disambiguation 부재 (C1) |
| LOPO 검정력 부족 (n=11) | O | L319, L321 | **충분** (단 Bolker 기준과의 직접 매핑은 C5에서 보강 권장) |
| HIV-1 단일 anchor의 일반화 한계 | O | L179, L184 | **부분** — "HIV-1 is the cleanest external anchor"는 명시되었으나, *단일 anchor 의존*의 일반화 위험을 별도 한계로 명시하지 않음 (M3 참조) |
| Layer C DMS 3–4 pathogens 한정 | △ | L35 ("6 of 11 pathogens") | **부분** — 숫자는 있으나, "DMS coverage 부족이 Layer C 결과 일반화를 어떻게 제한하는가"의 진술 없음 |
| MAFFT --auto 의존 | X | (없음) | **누락** — ch3 L131 "MAFFT v7.505 --auto" 사용은 명시되었으나, ch5에서 MSA quality 의존성 한계 미언급 (단 L295에서 "tree quality varies across pathogens" 우회 언급) |
| 합성 데이터 vs 실제 데이터 차이 | O | L21–26 | **충분** (synthetic-real gap 별도 sub-section, 이중-benchmark contribution으로 풀어냄) |
| External 독립 재현 부재 | O | L287 | **부분** — 1문장으로만 처리. 어떤 claim이 single-team artifact 영향을 받는지 매핑 부재 (C4) |
| Winner's curse | O | L283 | **충분** — 정량화·완화 시도·permutation 미래 작업까지 명시 |
| Cluster bootstrap 가정 | △ | L285 (HDI [0.188, 0.314]가 cluster bootstrap [0.195]와 일치) | **부분** — cluster bootstrap *가정* 자체(예: pathogen-level exchangeability)는 명시되지 않음 |
| Layer A pathogen별 정의 비대칭 | O | L300–308, L33 | **충분** (sec:gt_heterogeneity 별도 sub-section) — 단 회로성과의 logical chain은 약함 (C7) |
| 11-cluster rule-of-thumb 미달 | △ | L285 (Bolker 인용) | **부분** — 인용은 있으나 11이 minimum (5–6) 위 vs 권장(20–30) 아래라는 직접 진술 부재 (C5) |

추가 누락 후보:
- **MAFFT --auto의 mode 비결정성**: --auto는 input size에 따라 FFT-NS-2 / L-INS-i / G-INS-i 자동 선택 — pathogen마다 다른 알고리즘이 적용되었을 가능성. ch5에서 미언급 (M14 후보)
- **Synthetic data 생성 방식의 한계**: ch5 L21–26은 synthetic vs real *gap*을 다루지만, synthetic *생성 자체*의 가정(독립 mutation, uniform fitness landscape 등) 한계는 미언급
- **dN/dS proxy의 nucleotide-data 결손**: ch4 L739에서 "absence of nucleotide-level synonymous substitution data"가 인정되나 ch5에서 cross-reference 안 됨

---

## Future work 평가

| 방향 | 위치 | 구체성 | 실현 가능성 |
|------|------|--------|------------|
| 추가 protein domain 확장 (ORF1ab, N) | L17 | **낮음** (개수·power gain 무명시) | 높음 |
| Temporal contrast scoring 적정 resolution | L48 | **낮음** (4주 minimum과 모순, M2) | 중간 |
| Tree-quality-controlled phylogenetic correction | L256 | **중간** ("temporally aligned data") | 중간 |
| Fitness regression의 task-aligned binarization | L183 | **중간** ("future work rather than a missing leaderboard") | 높음 |
| 구조원천(experimental vs predicted) 통제 | L329 | **낮음** ("controlling for structure source in future analyses") | 중간 |
| Permutation-based significance testing (winner's curse) | L283 | **높음** (정확한 protocol 시사) | 높음 |
| Mixed-effects model (20–30+ pathogens) | L285 | **중간** ("when benchmark expands to 20--30+ pathogens") | 낮음 (large data acquisition) |
| 표준 분석 시간 윈도우 | L268 | **중간** ("standardizing the analysis time window") | 높음 |
| Pathogen-specific fine-tuned PLMs | L328 | **낮음** (CoVFit 인용으로 대체) | 중간 |
| Layer A non-leakage PLM 평가 | L277 | **중간** ("PLMs trained on databases that exclude viral sequences") | 중간 (viral-free PLM 구하기 어려움) |
| HCV E2 conservation analysis | L313 | **중간** | 높음 |
| Independent multi-tool reproduction | L287 | **낮음** ("queued for next cycle (Priority 5)") | 높음 |

**전반적 평가**: future work이 12+ 곳에 산발적으로 흩어져 있으며 chapter 내 통합 sub-section 부재. **conclusion (ch6)에 정리되어 있어야 하며, ch5에서는 "future work 통합 sub-section" 1개로 요약 권장**. 구체성 측면에서 "낮음"이 5건, "중간"이 6건, "높음"이 2건 — 평균적으로 일반론 비중이 높음.

---

## 챕터 종합 평가

**합격선: CONDITIONAL PASS**

**이유**:

**강점**:
1. 한계 인식의 *범위*는 우수 — 11개 핵심 한계 중 8개를 명시적으로 다룸.
2. ANCOVA / Bayesian hierarchical / cluster bootstrap의 multi-method robustness 입증은 학술적으로 견고 (L285, L290).
3. Winner's curse에 대한 정량적 mitigation (L283)은 학위논문 수준에서 보기 드문 깊이.
4. Synthetic vs real, 회로성, ESM-2 leakage 등 *비판자가 가장 먼저 제기할 issue*들에 대한 사전 답변 우수.
5. Ground truth heterogeneity와 그 ANOVA 함의의 연결 정직함 (L300–310).

**약점 (조건부 통과의 근거)**:
1. **C1 (회로성 ρ disambiguation)**: 두 ρ 값(0.12 vs 0.97)이 다른 의미임이 본문에서 명시되지 않음 — 학위 심사위원의 1순위 질문이 될 가능성 매우 높음.
2. **C3 (NFL 일반화)**: "stronger evidence than abstract theorem alone"는 NFL의 기술적 의미 오해. 통계학 심사위원 1명만 있어도 기각 사유.
3. **C4 (independent reproduction)**: 1문장 처리는 PhD 수준 dissertation에서 부족 — claim별 디스카운트 매핑 필요.
4. **M7 (PAHD-R 신규 개념)**: Discussion에서 신규 시스템 정의는 anti-pattern. ch4에서 정의되지 않았다면 ch6로 이동.
5. **M8 (LOPO 0/11 반론 anticipation)**: "그래도 practical value 있다"는 변호가 약함 — descriptive vs prescriptive 구별 필요.
6. **Future work 산발성**: 12곳에 분산, 1개 통합 sub-section 권장.

**조건 (PASS로 승급하기 위한 minimum)**:
- C1, C3, C4 반드시 수정 (각각 1–3문장 추가).
- M7 (PAHD-R) 위치 결정 — ch4 정의 reference 추가 또는 ch6 이동.
- M5 (4.012× vs 7.19× 직접 비교 명료화) — disambiguation 1문장 추가.
- 한계 체크리스트에서 "MAFFT --auto 의존"과 "DMS coverage 6/11"의 명시적 진술 1–2문장 추가.

**권장 등급 변경 후**: Major rewrite 1주 이내 가능, **Tier 1 patch (Critical만 수정) 시 약 0.5–1일 작업량**.

**최종 종합 점수 (10점 척도)**:
- 한계 인식 범위: 8/10
- 회로성 토의 명료성: 5/10 (C1 영향)
- Future work 구체성: 5/10
- Discussion vs Results 차별화: 7/10
- 반론 anticipation: 7/10
- Methodological implications: 8/10
- Self-citation balance: 6/10 (M4)
- Generalization 정확성: 6/10 (C3 영향)
- **종합: 6.5/10 → CONDITIONAL PASS**

---

검토자: Claude (적대적 검토 에이전트, paper-plan Phase 2b)
저장 위치: `/proj/paper/paper/dissertation/review/2026-04-28/phase2b_ch5.md`
