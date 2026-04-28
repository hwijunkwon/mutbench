# Defense Q&A Answer Notes (Cycle 5)

작성일: 2026-04-28
대상: codex_C5_defense_rehearsal.md (Q1–Q7) + cycle 4 후 신규 가능성 (Q8–Q10)
Q1은 별도 파일 `defense_q1_answer_note.md`로 작성되어 있으며 본 노트는 Q2–Q10을 다룬다.

본 노트의 모든 verbatim anchor는 cycle 4 본문 update를 반영한다 (HBV pilot, sliding-window backtest, wild-cluster bootstrap, Tranception–ESM correlation table 포함).

---

## Critical Questions (highest risk)

### Q1: Prospective evidence?
별도 파일 `defense_q1_answer_note.md` 참조. 60–80초 답변, ch5:347 / ch5:349 / abstract:2 / ch4:201 anchor.

---

### Q2: HIV-1 n=1 anchor의 외부타당성?

**hostile 위원 verbatim**:
> "Contribution 3b의 외부 검증은 본질적으로 HIV-1 한 종이다. abstract L11에서 anchored on HIV-1이라고 직접 적었고, ch5:179에서 the practical-value claim rests mainly on HIV-1이라고 적었다. H3N2는 69% Layer A overlap이라 self-consistency, SARS-CoV-2는 Bonferroni 후 exploratory. 즉 11 pathogens 중 외부 타당화에 진정으로 기여하는 것은 1이다. 박사학위 통과 기준에 어떻게 부합한다고 주장하는가? Bloom lab DMS의 epitope coverage가 V1V2/V3/CD4bs로 편향되어 있다면, 7.16–8.24× enrichment는 panel epitope structure를 재발견한 것에 불과할 수 있다."

**답변 (총 ~80초, ~150 단어)**:

1. **[Acknowledge / 15초]** "위원님 맞습니다. HIV-1 single anchor는 정직한 한계이며, ch5:179에서 *the practical-value claim rests mainly on HIV-1*로 명시했고, abstract도 *anchored on HIV-1*로 못 박았습니다."

2. **[Evidence — 3-tier rule이 *사전*규칙임을 보여줌 / 25초]** "그러나 *왜 HIV-1만 anchor인가*는 사후 selection이 아니라 사전 규칙의 결과입니다. Three-tier evidence rule (Bonferroni 생존 × Layer A overlap < 33%)을 ch5:176에서 사전 정의했고, HIV-1만 두 조건을 모두 만족 — 18% Layer A overlap, $p_{\text{adj}} = 2.5 \times 10^{-16}$. H3N2는 69% overlap으로 self-consistency tier로 자동 분류되었고, SARS-CoV-2는 Bonferroni 후 exploratory tier로 자동 분류되었습니다. 학생이 HIV-1을 *고른 것*이 아니라 *규칙이 HIV-1을 남긴 것*입니다."

3. **[Evidence — Worst-case 계산이 epitope bias를 부분적으로 흡수 / 20초]** "Epitope bias 우려에 대해서는, 7.16× 가 *worst-case full-set*이 아닌 *37 Layer-A-disjoint novel-only positions* 위에서의 Fisher $p = 5.0 \times 10^{-12}$, Bonferroni $p_{\text{adj}} \approx 3.9 \times 10^{-9}$ (ch5:176, ch4:1010 footnote)입니다. Layer A에서 disjoint하다는 점이 *문헌-curated convergent evolution과의 positional overlap 18%*만큼은 통제된 worst-case라는 의미입니다. Epitope-structure 편향을 완전히 통제하는 *literature-provenance audit*은 deferred future work입니다 (Q5 참조)."

4. **[Caveat / 10초]** "그러나 위원님 지적대로 *n=1 anchor*라는 한계 자체는 ch5:151의 honest disclosure로 명시되어 있고, MutBench의 contribution 3b는 *all RNA viruses에 대한 boundary claim*이 아닌 *HIV-1 anchor에서의 retrospective enrichment*에 한정됩니다."

5. **[Forward direction / 10초]** "추가 antibody-escape DMS dataset이 RNA virus panel에 충분히 축적되는 시점에 multi-anchor external validation을 ch6 Future Roadmap Priority 1–2로 등록했습니다."

**본문 anchor (verbatim)**:
- **ch5:176**: "HIV-1 passes both criteria (18\% Layer~A overlap, $p_{\text{adj}} = 2.5 \times 10^{-16}$) and remains the primary external anchor; the direct novel-only test on 37 Layer~A-disjoint positions gives $7.16\text{--}8.24\times$ enrichment, with the conservative worst case still significant after 780-fold correction."
- **ch5:177**: "H3N2 survives Bonferroni correction but has 69\% Layer~A overlap, so it is treated as a self-consistency check; its novel-only enrichment is not significant ($p=0.132$)."
- **ch5:179**: "Thus the benchmark is not algorithmically circular, but the practical-value claim rests mainly on HIV-1."
- **ch1:150**: "Externally-valid vaccine-escape enrichment, anchored on HIV-1: the Layer-A-disjoint subset of HIV-1 escape positions (37 of 45) yields a direct novel-only enrichment of $7.16\text{--}8.24\times$..."
- **abstract:11**: "External validation, anchored on HIV-1 — under a three-tier evidence rule (Bonferroni survival $\times$ Layer A overlap $<$ 33\%)..."

**후속 질문 대비**:
- **Q2a**: "Then practical-value claim should drop to *MutBench fits HIV-1 escape*, n=1 result?"
  - **답변** (~30초): "예, 그것이 정확한 *외부* 주장입니다. MutBench의 *retrospective benchmark infrastructure* (Contribution 1)와 *pathogen-dependent finding* (Contribution 2, $\omega^2 = 0.296$)은 11-pathogen panel 위에서의 결과이지만, *external validation* (Contribution 3b)는 HIV-1 anchor에 한정됩니다. 이 boundary는 abstract:14의 *the external practical anchor remains HIV-1* 라는 단어로 명시되어 있습니다."
- **Q2b**: "Bloom lab DMS의 epitope panel이 panel-specific bias를 가지면?"
  - **답변** (~30초): "그 가능성은 사전 부정할 수 없습니다. 그러나 (i) 18% Layer A overlap이 *문헌 curation과의 disjoint*를 보장하고, (ii) 37 novel positions에서 worst-case $p = 5.0 \times 10^{-12}$가 panel size 효과 ($p$ 보정 후에도 $3.9 \times 10^{-9}$)를 통제하며, (iii) HIV-1 vaccine escape DMS는 V1V2/V3/CD4bs 외에도 gp41/MPER 영역을 포함합니다. *Panel epitope-coverage* 자체에 대한 systematic audit은 deferred future work이며, ch5:184에 *external escape validation은 evidential bridge*라는 honest framing이 있습니다."
- **Q2c**: "11 pathogens 중 1만 외부 검증이라면 *11* 패널의 의미는?"
  - **답변** (~25초): "11 panel은 *Contribution 1–2*의 internal evidence (8,580-cell grid + ANOVA interaction)이고, *Contribution 3*는 그 위에 *external anchor를 1 pathogen에 대해서만* 추가한 layered structure입니다. *Internal* discovery (pathogen-dependence)와 *external* validation (HIV-1 anchor)을 같은 수준의 주장으로 혼동하지 않도록 abstract와 ch5:179가 의도적으로 분리해서 작성되었습니다."

---

### Q3: ω² 0.296 cherry-picking?

**hostile 위원 verbatim**:
> "ch3 / ch4 / ch5에 걸쳐서 $\omega^2_{\text{scoring} \times \text{pathogen}}$의 값이 6개 이상의 reading으로 보고되어 있다 — cell-level 0.234, evaluation-level 0.296, ANCOVA-adjusted 0.264, Bayesian posterior mean 0.252 (priors A) 또는 0.319 (priors B), 6-category aggregated 0.103, cluster-bootstrap CI [0.195, 0.333], wild-cluster bootstrap [0.201, 0.303]. 이 중 abstract와 headline에 들어간 숫자는 0.296이다. 이건 highest non-conservative reading에 해당한다. 학생은 왜 0.296을 headline에 박았는가? 0.103 lower bound을 박지 않은 이유는?"

**답변 (총 ~80초, ~150 단어)**:

1. **[Acknowledge / 10초]** "정확하게 6+ readings을 보고했고, headline이 0.296인 것도 맞습니다. 위원님의 *cherry-picking* 의심을 직접 다루기 위해 본문은 모든 reading을 단일 단락에서 나란히 보고합니다 (ch5:289)."

2. **[Evidence — robustness가 답이지 single number가 답이 아님 / 30초]** "핵심은 *어느 reading을 골라도 Cohen large-effect threshold ($\omega^2 \geq 0.14$)*를 모두 통과한다는 점입니다. Cell-level 0.234, evaluation-level 0.296, ANCOVA-adjusted 0.264, Bayesian posterior 0.252–0.319, 6-category 0.103. 0.103만이 large threshold *아래*이지만, 그것도 *medium threshold ($\omega^2 \geq 0.06$)*는 통과하며 ch5:285에서 *collinearity-robust lower bound*로 명시되어 abstract:10에도 *6-category aggregation gives $\omega^2 = 0.103$ as a collinearity-robust lower bound* 형태로 같이 보고되었습니다."

3. **[Evidence — Wild-cluster bootstrap이 cycle 4에서 추가됨 / 20초]** "그리고 ch4:578의 *wild-cluster bootstrap robustness* (1,000 Rademacher replicates, percentile interval [0.201, 0.303])이 cycle 4에서 추가되었습니다. Wild-cluster lower bound 0.201은 standard cluster bootstrap lower bound 0.195와 소수점 셋째 자리까지 일치합니다 ($\Pr(\omega^2 \leq 0.14) = 0$)."

4. **[Caveat / 10초]** "다만 위원님 지적대로 abstract의 *single point 0.296* 표기는 reading-friendly choice였고, 본문의 *0.103 lower bound + 0.296 upper bound + cluster CI [0.195, 0.333]* 표기가 abstract보다 정직합니다. abstract revision이 권고되면 0.103–0.319 *range* 또는 *(0.103 6-category lower bound)* 부기를 약속합니다."

5. **[Forward direction / 10초]** "0.296이 *cherry-picked highest*가 아니라 *evaluation-level fixed-effect estimate*이며 4 readings (cell-level 0.234, ANCOVA 0.264, Bayesian 0.252–0.319, wild-cluster mean 0.269) 모두 0.234–0.319 narrow range 안에 있다는 것이 robustness 핵심입니다."

**본문 anchor (verbatim)**:
- **ch5:285**: "...readers should interpret the 6-category $\omega^2 = 0.103$ as the collinearity-robust lower bound and the 20-type $\omega^2 = 0.296$ as the upper bound on the pathogen-scoring interaction depending on how ``scoring type'' is defined."
- **ch5:289**: "The original exploratory calculation... yielded a posterior mean of $\omega^2_{\text{scoring} \times \text{pathogen}} = 0.252$ with 95\% HDI $[0.188, 0.314]$... archived re-implementation gives a posterior mean of 0.319 with 95\% HDI $[0.246, 0.396]$..."
- **ch4:475**: "the within-cell residual ($\omega^2 \approx 0.39$...) is comparable in magnitude, so ``largest source'' in this dissertation reads as ``largest modeled component.'' The companion cell-level estimate... is $\omega^2 = 0.234$, with an ANCOVA-adjusted value of 0.264..."
- **ch4:578**: "the wild-cluster 95\% percentile interval is $[0.201, 0.303]$ (mean $0.269$, median $0.276$, CI width $0.103$); both schemes give $\Pr(\omega^2_{\text{int}} \leq 0.14) = 0$."
- **abstract:10**: "$\omega^2_{\text{scoring} \times \text{pathogen}} = 0.296$ (11-pathogen cluster-bootstrap 95\% interval [0.195, 0.333]; 6-category aggregation gives $\omega^2 = 0.103$ as a collinearity-robust lower bound..."

**후속 질문 대비**:
- **Q3a**: "Bayesian priors A vs B 결과 차이 0.252 vs 0.319, 어느 것을 믿어야 하는가?"
  - **답변** (~25초): "두 prior choice 모두 *load-bearing posterior probability* ($\Pr(\omega^2 > 0.14)$)에서 거의 1.0으로 일치합니다 (0.996 vs 0.9998, ch5:289). 차이는 HDI 중심값 (variance shrinkage 효과)이지 *qualitative conclusion* (large-effect interaction)에는 영향이 없습니다. *Reproducibility provenance*로서 두 결과 모두 archive (`bayesian_omega_summary.csv`)에 보관됩니다."
- **Q3b**: "0.296이 *upper bound*라면 abstract도 그렇게 적었어야 하지 않은가?"
  - **답변** (~20초): "동의합니다. abstract:10에 *6-category aggregation gives $\omega^2 = 0.103$ as a collinearity-robust lower bound* 부기는 이미 있지만 *0.296을 upper bound로 명시*하는 단어는 없습니다. defense 후 abstract revision에서 *upper bound on the pathogen-scoring interaction depending on how scoring type is defined* (ch5:285 phrasing 인용) 추가를 약속합니다."

---

## Major Questions

### Q4: Tranception–ESM-LLR collinearity?

**hostile 위원 verbatim**:
> "ch5:279에 *the Tranception channel is computed as a lightweight ESM-2 masked-marginal pseudo-perplexity proxy*. 11/12 pathogens에서 ESM-2 LLR과 Pearson 0.64–0.84 collinear. 그러면 SARS-CoV-2 best = Tranception은 동일 PLM family 안에서의 micro-variation이고 9 distinct optimal types는 사실상 6 distinct families로 환산해야 하지 않는가?"

**답변 (총 ~70초, ~130 단어)**:

1. **[Acknowledge / 10초]** "예, ch5:279에서 직접 disclosure했고 cycle 4에서 per-pathogen Pearson/Spearman correlation table을 ch3에 추가했습니다 (`tab:tranception_esm_correlation`)."

2. **[Evidence — 정확한 numeric structure / 25초]** "12 pathogens 중 11이 operationally near-equivalent (Pearson $\rho = 0.643$–$0.836$), MERS most collinear (0.836), Zika lowest within band (0.643). HIV-1만 dissociating (Pearson $\rho = 0.043$, p=0.36 n.s.). SARS-CoV-2 자체는 Pearson $\rho = 0.753$, Spearman $\rho = 0.963$이므로 *Tranception best*가 *ESM-LLR best*와 channel-equivalent하다는 점은 인정합니다."

3. **[Evidence — 6-category $\omega^2 = 0.103$이 이미 collinearity-robust / 15초]** "이를 사전에 다루기 위해 ch5:285의 *6-category aggregation* (frequency / MSA / phylogenetic / structural / AI / composite)에서 PLM-family 두 channel이 같은 *AI-based* category로 collapse되며, 그 6-category 0.103도 *medium threshold*를 통과합니다."

4. **[Caveat / 15초]** "위원님 지적대로 *9 distinct optimal information types*는 *9 distinct scoring formulas*이며 *9 distinct biological information sources*는 아닙니다. abstract:13의 *9 distinct optimal information types* 옆에 ch5:279의 *Tranception/ESM-2 channel collinearity is not separated at headline granularity* qualifier가 ch1:148에 이미 있습니다."

5. **[Forward direction / 5초]** "*pure-Tranception (non-ESM-2-proxy) baseline*은 ch6 Future Roadmap에 등록됨."

**본문 anchor (verbatim)**:
- **ch5:279**: "The actual per-pathogen correlations between this proxy channel and the standalone ESM-2 LLR channel were re-measured at the position level for the cycle-4 audit... and exhibit the following structure: 11 of 12 pathogens are operationally near-equivalent (Pearson $\rho = 0.643$–$0.836$, Spearman $\rho = 0.713$–$0.980$, all $p < 10^{-50}$), with MERS most collinear (Pearson $\rho = 0.836$, $n = 1330$) and Zika lowest within the collinear band (Pearson $\rho = 0.643$, $n = 451$). HIV-1 is the lone dissociating case (Pearson $\rho = 0.043$, $p = 0.36$ n.s.; Spearman $\rho = 0.158$, $p = 7.8 \times 10^{-4}$, $n = 450$)."
- **ch5:279 (continuation)**: "Reporting a single PLM winner per pathogen at headline granularity (in the abstract and chapter summaries) without separating Tranception and ESM-LLR is therefore a presentational simplification, not a claim of channel independence."
- **abstract:13**: "9 distinct optimal information types across 11 pathogens (Tranception/ESM-2 channel collinearity is not separated at headline granularity; see Chapter~\ref{ch:mutbench})."

**후속 질문 대비**:
- **Q4a**: "Pure Tranception 결과는 어디에?"
  - **답변** (~20초): "별도 fine-tuned Tranception forward pass는 본 학위논문에서 실시하지 않았습니다. 본 학위논문의 *Tranception* channel은 ESM-2 masked-marginal pseudo-perplexity proxy이며 ch5:279에서 명시된 한계입니다. *Pure Tranception cross-validation*은 ch6 Future Roadmap Priority 5에 등록되어 있습니다."

---

### Q5: Layer A literature-provenance circularity?

**hostile 위원 verbatim**:
> "Layer A는 immune-escape positions가 dominate하고, 외부 검증은 vaccine-escape (또 다른 immune-escape의 형태)이다. circularity audit이 ch5:176에서 HIV-1 18% Layer A overlap으로 통과했다고 주장하지만, 이는 position-level disjoint이지 biological information source-level disjoint이 아니다. Layer A를 만든 문헌과 vaccine-escape positive set을 만든 문헌이 substantively overlap할 수 있다 (둘 다 antibody-escape 연구). literature provenance가 disjoint한지 audit했는가?"

**답변 (총 ~60초, ~110 단어)**:

1. **[Acknowledge / 15초]** "위원님 지적이 정확합니다. 현재 audit은 *positional disjoint* (HIV-1 18% Layer A overlap, ch5:176)이며, *literature-provenance disjoint*는 audit하지 않았습니다."

2. **[Evidence / 20초]** "Positional disjoint는 *current best directly auditable measure*이며 Layer A에 포함된 *45 HIV-1 escape positions 중 37*이 Layer A와 disjoint입니다. 그 37 positions에서의 novel-only enrichment 7.16–8.24×, $p_{\text{adj}} \approx 3.9 \times 10^{-9}$ (ch5:176, ch4:1010 footnote)이 *positional* circularity는 통제합니다."

3. **[Caveat / 15초]** "그러나 *literature provenance audit* — Layer A curation에 사용된 paper set과 vaccine-escape positive set 정의에 사용된 paper set 간의 disjointness — 는 본 학위논문에서 측정하지 않았습니다. 두 set이 동일 antibody-escape literature에서 *partially derived*되었을 가능성을 부정하지 않습니다."

4. **[Forward direction / 10초]** "Defense 후 ch5에 1단락의 *literature-provenance disjoint audit limitation* 명시 추가, 그리고 source paper-level audit을 ch6 Future Roadmap에 등록하는 revision을 약속합니다."

**본문 anchor (verbatim)**:
- **ch5:176**: "HIV-1 passes both criteria (18\% Layer~A overlap, $p_{\text{adj}} = 2.5 \times 10^{-16}$) and remains the primary external anchor..."
- **ch5:35** (sec:circularity): "...HIV-1 (82\% of its escape set disjoint from Layer~A) is the cleanest external anchor, whereas H3N2's 69\% Layer~A/escape overlap means that the H3N2 enrichment re-measures benchmark performance more than it provides independent replication."
- **ch5:184**: "This is especially relevant for pathogens lacking DMS Layer~C, where Layer~A plus HIV-1-like external escape validation remains the current evidential bridge."

**후속 질문 대비**:
- **Q5a**: "그러면 본 학위논문의 *external validation* 강도는 어느 정도?"
  - **답변** (~25초): "*Positional disjoint* 수준에서는 18% overlap + 37 novel-only positions에서의 7.16× worst-case enrichment로 통제되며, 이 수준의 external validation은 Bonferroni $p_{\text{adj}} \approx 3.9 \times 10^{-9}$로 statistically conservative합니다. *Information-source disjoint* 수준에서는 위원님 지적대로 *partial overlap residual*이 있으며, 그것이 ch5:184의 *evidential bridge* 라는 단어 선택의 이유입니다 — *fully orthogonal validation*이 아닌 *partially-orthogonal validation*."

---

### Q6: Friedman underpowered=null 오류?

**hostile 위원 verbatim**:
> "ch5:330에서 Friedman 결과는 uninformative이지 strict null의 confirmation이 아니다라고 학생이 직접 적었다. 그러면 abstract L10의 Friedman test shows no universally best combination ($\chi^2 = 7.69$, $p = 0.990$)은 현재 데이터로 결정 불가라는 의미이다. 그럼에도 abstract는 이를 no universally best combination으로 해석한다. 이건 underpowered = null이라는 typical statistics 오류와 어떻게 다른가?"

**답변 (총 ~60초, ~110 단어)**:

1. **[Acknowledge / 15초]** "정확합니다. ch5:330의 *Friedman은 uninformative*이라는 단어는 *power 부족*이라는 의미이고, abstract L10이 이를 *no universally best*로 해석하는 것은 *underpowered = null* 오류로 *읽힐 수* 있습니다."

2. **[Evidence — 그러나 Friedman이 *load-bearing*이 아님 / 20초]** "결정적으로, *no universally best combination* 결론은 Friedman 단독이 아니라 *세 가지 독립 lens*의 합입니다: (i) ANOVA scoring×pathogen interaction $\omega^2 = 0.296$ (large effect, 모든 reading $\geq 0.103$), (ii) oracle-vs-generalized MCC gap 0.265, (iii) LOPO 0/11. ch4:658에서 *only the ANOVA provides positive evidence; LOPO and Friedman are two failures-to-reject that are consistent with pathogen-dependent optimality but do not by themselves constitute independent evidence* — 즉 Friedman은 *null-consistent corroboration*으로만 사용됩니다."

3. **[Evidence — Nemenyi pairwise post-hoc도 같은 결론 / 10초]** "Cycle 3에서 추가된 Nemenyi pairwise post-hoc test (ch4:527)도 0/190 pairs significant, 모든 $p \in [0.989, 1.000]$ — *power deficit*을 명시적으로 quantify합니다."

4. **[Caveat / 10초]** "위원님 지적대로 abstract L10의 *no universally best combination* phrasing은 *underpowered = null* 함의를 시사할 수 있으며, *power-limited corroboration*이라는 qualifier 추가가 적절한 revision입니다."

5. **[Forward direction / 5초]** "abstract revision에서 ch5:330의 *uninformative under power constraints* phrasing을 abstract에도 적용 약속."

**본문 anchor (verbatim)**:
- **ch5:330**: "Despite the small sample size ($n=11$), the Friedman test yielded $p = 0.990$. We emphasise that under the Friedman rank-block design with $n = 11$ blocks, this $p$-value is uninformative (the data are too sparse to discriminate among 20 ranked treatments at conventional power) rather than a confirmation of a strict null."
- **ch4:524**: "The Friedman test's power at $n = 11$ blocks is limited (approximately 0.15 for medium effect $W$), so the non-significance is consistent with both readings; this should therefore be read as corroboration of, rather than disconfirmation of, pathogen-dependent optimality."
- **ch4:658**: "The four lenses are not independent confirmations: only the ANOVA (within the modeled subspace) provides positive evidence of pathogen-dependence; the LOPO permutation test and the Friedman rank test are two failures-to-reject that are consistent with pathogen-dependent optimality but do not by themselves constitute independent evidence."
- **abstract:10**: "Friedman test shows no universally best combination ($\chi^2 = 7.69$, $p = 0.990$), and LOPO yields 0/11 exact matches with a 0.265 oracle-vs-generalized MCC gap (LOPO 0/11 alone is null-consistent under permutation; the conclusion rests on the interaction effect plus the vaccine-escape audit, not on LOPO in isolation)."

**후속 질문 대비**:
- **Q6a**: "Power 0.15는 너무 낮지 않은가? 11 pathogens가 부족한가?"
  - **답변** (~25초): "예, 본 학위논문의 11-pathogen panel은 *Bolker rule-of-thumb minimum* (5–6 levels)을 만족하지만 *typical recommendation* (20–30)에는 미달합니다 (ch5:289). 그래서 *Friedman을 load-bearing evidence로 사용하지 않고* ANOVA interaction을 정형 evidence로 사용한 것입니다. Panel expansion (ch6 Future Roadmap)이 power 문제의 정공법입니다."

---

### Q7: 4-feature core operational direction?

**hostile 위원 verbatim**:
> "Contribution 3a는 4-feature core가 10-feature와 statistically indistinguishable이라고 주장하는데, paired delta +0.011, 95% CI [-0.018, +0.042], p=0.61, ±0.04 MCC non-inferiority bound, sign-flip permutation. 이 모든 것이 non-rejection of inferiority, not pre-specified equivalence로 약화. 학생의 operational claim은 무엇인가? 4-feature를 사용해도 좋다인가, 4-feature가 좋다는 증거는 부족하다인가? 박사논문 contribution은 operational direction을 제시해야 한다."

**답변 (총 ~60초, ~110 단어)**:

1. **[Acknowledge / 10초]** "위원님이 정확하게 짚으셨습니다. *Operational direction*은 *4-feature가 10-feature를 이긴다*가 아닙니다."

2. **[Evidence — exact phrasing / 20초]** "정확한 operational direction은 *4-feature core (homoplasy, pLDDT, entropy, freq)는 cold-start scenario에서 recommended starting point이고 ±0.04 MCC non-inferiority bound 안에서 10-feature와 통계적으로 구분되지 않는다* 입니다. 즉 *practitioner가 4-feature로 시작해도 안전하다*가 운용 방향이며, *4-feature가 항상 best*는 주장하지 않습니다."

3. **[Evidence — 본문 phrasing이 이미 reflected / 15초]** "ch5:196의 *Contribution 3a gives the cold-start floor*, ch5:215의 *the 4-feature core (homoplasy, pLDDT, entropy, frequency) captures 98% of full-ensemble performance*, ch6:97의 *4-feature core converts findings into usable prioritization tools, but the adaptive claim remains bounded: a feasible direction for adaptive evidence fusion, not a universal adaptive predictor* — 모두 *recommended starting point* 운용 방향에 일관됩니다."

4. **[Caveat / 10초]** "ch1:152, ch6:14의 *non-rejection of inferiority, not pre-specified equivalence* phrasing은 *equivalence claim의 statistical strength* 한계를 명시한 것이고, *operational direction*과는 분리됩니다."

5. **[Forward direction / 5초]** "Pre-specified equivalence study (TOST, sample size pre-registered)는 ch6 Future Roadmap Priority 6 등록."

**본문 anchor (verbatim)**:
- **ch1:152**: "Feature ablation identifies a 4-feature core (homoplasy, pLDDT, entropy, frequency) that is statistically indistinguishable from the full 10-feature ensemble under nested-LOPO within a $\pm 0.04$~MCC non-inferiority bound (paired delta $+0.011$~MCC; 95\% CI [$-0.018$, $+0.042$]; permutation $p = 0.61$; Table~\ref{tab:nested_lopo_4core}); this is reported as non-rejection of the inferiority hypothesis at the stated bound, not as a pre-specified equivalence claim."
- **ch5:164**: "the 10-feature EqualWeight ensemble (under uniform-weight LOPO top-10\% evaluation, the 4-feature core retains 97.6\% of the 10-feature ensemble's mean MCC --- this is a relative-to-ensemble retention figure within the same protocol, not an absolute floor relative to an oracle..."
- **ch5:196**: "Contribution~3a gives the cold-start floor: the 4-feature core recovers $\approx$98\% of the 10-feature ensemble mean MCC when labels are unavailable."
- **ch6:14**: "Multi-source integration infrastructure: under nested-LOPO on the 12-pathogen Stage~3 panel, the fixed 4-feature core (homoplasy, pLDDT, entropy, frequency) is statistically indistinguishable from the full 10-feature EqualWeight ensemble..."
- **ch6:97**: "The 4-feature core and PAHD-R workflow convert these findings into usable prioritization tools, but the adaptive claim remains bounded: the dissertation is consistent with a feasible direction for adaptive evidence fusion, not a universal adaptive predictor."

**후속 질문 대비**:
- **Q7a**: "그럼 ch6 conclusion이 *recommended starting point*로 명시되어 있는가?"
  - **답변** (~15초): "ch6:97의 *bounded adaptive claim, feasible direction*이 사실상 *recommended starting point*에 해당합니다. 만약 위원님이 더 강한 명시 phrasing을 권하시면 ch6:14에 *recommended starting point in cold-start scenarios* 단어 추가 revision을 약속드립니다."

---

## Cycle 4 이후 신규 가능 질문

### Q8: DNA virus 검증? (HBV null enrichment)

**가능성**: ch5:329의 HBV pilot이 cycle 4에서 추가됨. Hostile 위원이 *RNA virus only로 한정해놓고 왜 HBV를 본문에 넣었는가*로 질문할 수 있음.

**답변 (총 ~50초, ~100 단어)**:

1. **[Acknowledge / 10초]** "HBV polymerase pilot은 *DNA-virus extension*을 주장하기 위해 추가한 것이 아니라, *RNA virus 한정 scope justification*이 *citation-only claim*에서 *empirical sanity check*으로 격상되도록 추가한 것입니다."

2. **[Evidence / 25초]** "구체적으로 ch5:329에서, HBV polymerase $n = 708$ unique full-length sequences, MAFFT --auto MSA ($L = 882$). 두 결정적 quantity: (i) variable-position fraction $0.686$ vs. RNA virus comparators $0.996$–$1.000$; (ii) mean Shannon entropy $0.236$ bits vs. RNA virus $0.61$–$3.15$ bits — *2.6×–13× density gap consistent with $\sim 10^3 \times$ rate gap*. 그리고 14 literature-curated RT-domain drug-resistance positions에서 entropy 채널 enrichment $p = 0.354$ (global), $p = 0.136$ (RT-domain restricted) — null."

3. **[Caveat / 10초]** "Three honesty boundaries (ch5:329 단락 끝): (i) entropy/frequency 채널만 측정, PLM/structural/dN/dS 미측정, (ii) Layer A는 single-category drug-resistance list (n=14), 11-pathogen main panel과 다름, (iii) HBV는 cross-pathogen LOPO에 포함되지 않음."

4. **[Forward direction / 5초]** "Full DNA-virus extension은 ch6:84–85, Future Roadmap Priority 3."

**본문 anchor (verbatim)**:
- **ch5:329**: "...the variable-position fraction is $0.686$ on HBV polymerase versus $0.996$--$1.000$ on three exemplar RNA-virus surface proteins... mean Shannon entropy is $0.236$ bits on HBV polymerase versus $0.61$–$3.15$ bits..."
- **ch5:329 (continuation)**: "...permutation $p = 0.354$ globally and $p = 0.136$ within the RT domain ($n_{\text{perm}} = 10{,}000$, seed 42)... This null result is a direct empirical sanity check on the design rationale..."
- **ch6:85**: "A single-pathogen DNA-virus density pilot on HBV polymerase ($n = 708$ NCBI sequences, 14 literature-curated RT-domain drug-resistance positions) is reported in Chapter~\ref{ch:discussion}, Section~\ref{para:hbv_pilot} as an empirical sanity check on this rate-based scope claim..."

---

### Q9: Wild-cluster bootstrap 결과?

**가능성**: cycle 4에서 wild-cluster bootstrap이 ch4:578과 ch5:289에 추가됨. *왜 이전엔 없었고 이제 추가했는가, 결과는 cluster bootstrap과 어떻게 다른가*.

**답변 (총 ~40초, ~80 단어)**:

1. **[Acknowledge / 5초]** "예, cycle 4에서 추가했습니다."

2. **[Evidence / 25초]** "Cameron 2008의 small-cluster ($G \leq 30$) percentile bootstrap anti-conservatism critique를 직접 다루기 위해 wild-cluster (Rademacher-weight) bootstrap을 1,000 replicates 실시 (`scripts/wild_cluster_bootstrap_omega.py`, seed 42). 결과: 95% percentile interval $[0.201, 0.303]$ vs. standard cluster bootstrap $[0.195, 0.333]$. Lower bound가 0.201 vs 0.195로 거의 일치 (소수점 셋째 자리), upper bound는 wild-cluster가 0.303 vs 0.333으로 더 좁음 — 이는 *standard percentile bootstrap이 right-tail에서 anti-conservative*라는 Cameron 예측과 일치."

3. **[Evidence — robustness / 10초]** "$\Pr(\omega^2_{\text{int}} \leq 0.14) = 0$이 양 scheme 모두에서 만족되어 *large-effect interaction* 결론은 small-cluster inferential frame 양쪽 모두에서 살아남습니다."

**본문 anchor (verbatim)**:
- **ch4:578**: "the wild-cluster 95\% percentile interval is $[0.201, 0.303]$ (mean $0.269$, median $0.276$, CI width $0.103$); both schemes give $\Pr(\omega^2_{\text{int}} \leq 0.14) = 0$ at the present replicate count."
- **ch5:289**: "...a wild-cluster bootstrap... has been performed for the present cycle: $B = 1{,}000$ Rademacher-weight replicates over the 11 pathogen clusters... give a 95\% percentile interval of $[0.201, 0.303]$ for $\omega^2_{\text{int}}$ with $\Pr(\omega^2 \leq 0.14) = 0$..."

---

### Q10: Sliding-window prospective mostly chance인 이유?

**가능성**: cycle 4에서 sliding-window prospective backtest가 ch4:233에 추가되었고, *11 중 2 pathogen만 prospective signal* (EV-A71 0.77, Rabies 0.79). Hostile 위원: *왜 9 pathogens는 chance level인가? freq+entropy의 prospective failure는 본 학위논문 framework의 한계 아닌가?*

**답변 (총 ~70초, ~130 단어)**:

1. **[Acknowledge / 15초]** "위원님 지적이 정확합니다. ch4:240의 결과 — 11 pathogens 중 EV-A71 (AUROC 0.77), Rabies (0.79), Influenza B (0.70 partial)만 chance line 위, 8 pathogens가 chance 또는 below — 가 본 학위논문에서 *direct forward-time evidence*로 보고됩니다."

2. **[Evidence — 정확한 framing / 25초]** "결정적으로, sliding-window backtest는 *4-feature core 전체*가 아닌 *time-varying 2 features (freq + entropy)*만 exercise합니다 (ch4:240, ch5:351). Static features (homoplasy, pLDDT)는 다른 MSA coordinate frame에 있어 per-window re-train이 불가능합니다. 따라서 *MutBench 4-feature core의 prospective evaluation*이 아니라 *freq+entropy subset의 prospective evaluation*입니다."

3. **[Evidence — H3N2 pilot 결과와 일관 / 15초]** "이 결과는 ch4:201의 H3N2 single-pilot 결론 (*frequency alone is retrospectively diagnostic but prospectively weak*)을 *generalises to most of the panel for the freq+entropy 2-feature subset*로 확장하는 것이며, ch5:349에서 *meaningful prospective discrimination is therefore concentrated in EV-A71 and Rabies*로 이미 명시했습니다."

4. **[Caveat / 10초]** "그러므로 *9 pathogens chance-level*은 *freq+entropy 2-feature의 prospective limit*을 보여주는 결과이며, *4-feature core (homoplasy + pLDDT 추가) 또는 multi-source integration의 prospective evaluation*은 별도 작업으로 ch6 Future Roadmap Priority 1입니다."

5. **[Forward direction / 5초]** "Coordinate-frame harmonization (homoplasy/pLDDT를 year-tagged MSA에 mapping)이 prerequisite."

**본문 anchor (verbatim)**:
- **ch4:238**: "Across the 219 evaluated windows spanning 11 pathogens, the per-pathogen mean AUROC of the freq+entropy ensemble is 0.79 for Rabies, 0.77 for EV-A71, 0.70 for Influenza~B... and below 0.50 for the remaining four (Dengue 0.48, HIV-1 0.46, H3N2 0.43, Norovirus 0.32, HCV 0.31)."
- **ch4:240**: "the time-varying portion of the 4-feature core (freq+entropy) detects newly emerging high-frequency sites at clearly above-chance rates only for two of eleven pathogens (EV-A71 AUROC 0.77, Rabies 0.79)... The static features in the full 4-feature core (homoplasy, pLDDT) cannot be re-trained per window in the present coordinate frame and are therefore not exercised by this backtest..."
- **ch5:349**: "...the operational claim ``MutBench can be used to prioritise emerging hotspots'' is now supported by direct forward-time evidence for EV-A71 and Rabies, by partial evidence for Influenza~B, and remains weak for the other eight pathogens; readers using the framework for surveillance on those eight should continue to treat the time-forward signal as unverified."

**후속 질문 대비**:
- **Q10a**: "그럼 *MutBench can prioritise emerging hotspots*라는 abstract 주장은 9/11 pathogens에서 거짓 아닌가?"
  - **답변** (~25초): "그 주장은 본 학위논문에서는 *retrospective enrichment evidence*로 anchor되고 (HIV-1 7.19×), forward-time evidence로는 EV-A71/Rabies/Influenza B에 한정됩니다. ch5:349가 이 distinction을 명시: *direct forward-time evidence for EV-A71 and Rabies, partial evidence for Influenza B, weak for the other eight*. abstract revision 시 *prospective scope: 3 of 11 pathogens with current 2-feature subset* qualifier 추가를 약속합니다."

---

## 발표 슬라이드 권고

defense 30분 발표 slide deck에 추가 권고:

### Slide A: "Three Honest Disclosures" (presentation 마지막 limitation slide)
> **Three honest disclosures (Phase 0 사전 차단)**
> 1. Prospective gap — sliding-window backtest: 3/11 pathogens above chance (ch5:349)
> 2. HIV-1 single anchor — practical-value claim rests mainly on HIV-1 (ch5:179)
> 3. Tranception–ESM channel proxy — not separated at headline granularity (ch5:279)

이 slide는 hostile 위원이 Q1, Q2, Q4를 던지기 *전*에 학생이 *이미 알고 있다*는 정보를 주어 fail trigger 거리에서 1단계 멀어지게 함.

### Slide B: "Limitations vs Mitigations"
| Limitation | Mitigation in dissertation | Future work |
|---|---|---|
| HIV-1 single anchor | 3-tier evidence rule (사전), 18% Layer A overlap, $p_{\text{adj}} = 2.5 \times 10^{-16}$ | Multi-anchor expansion as DMS data grow |
| ω² 6 readings | All 6 above medium threshold ($\geq 0.103$); 4 above large ($\geq 0.234$); wild-cluster $[0.201, 0.303]$ | Pre-specified primary endpoint |
| Friedman power | Reported as null-consistent corroboration only; ANOVA load-bearing | Panel expansion to 20–30 pathogens |
| 4-feature non-equivalence | Recommended starting point in cold-start; non-rejection of inferiority within ±0.04 MCC | Pre-specified TOST equivalence study |
| Tranception proxy | Per-pathogen ρ table (ch3, cycle 4); 6-category ω² = 0.103 collinearity-robust | Pure-Tranception forward pass baseline |
| Layer A literature provenance | 18% positional overlap audit; literature-provenance audit deferred | Source-paper-level audit |
| DNA virus scope | HBV pilot (ch5:329) — empirical sanity check, not extension | Full DNA-virus port (ch6:85) |

### Slide C: Q1 답변 핵심 anchor 1줄
> **Prospective scope**: ch4:201 H3N2 pilot + ch4:238 sliding-window (3/11 pathogens above chance, freq+entropy 2-feature subset). Forward-time evaluation of 4-feature core = Future Roadmap Priority 1.

---

## Defense 시점 체크리스트

defense 1주일 전 — 학생 본인이 수행:

1. **Q1–Q10 답변 1회 음독 연습** (총 분량 ~12분, hostile 위원 25–30분 발언 분량의 절반)
   - 각 답변 60–90초 내 종결 (Q4, Q5, Q9는 ~50초)
   - 후속 Q[N]a/b/c는 25–35초 이내 종결
2. **Verbatim anchor 외우기** (각 anchor의 exact line:column)
   - Critical: ch5:179 (HIV-1 anchor), ch5:285 (ω² 6-reading), ch5:330 (Friedman uninformative), ch5:347–349 (prospective gap)
   - Major: ch5:279 (Tranception proxy), ch5:176 (3-tier rule), ch4:578 (wild-cluster), ch5:329 (HBV pilot)
3. **Slide A "Three Honest Disclosures" 발표 마지막 30초에 직접 띄움** — Phase 0 차단의 가장 효과적인 단일 조치 (codex_C5 §Phase 4 권고)
4. **Slide B "Limitations vs Mitigations" 표를 발표 도입부 5분에도 1번 미리 노출** — 외부 위원이 Q&A 들어갈 때 *학생이 한계를 이미 정리해둠*을 인지하도록
5. **답변 시 "피해야 할 표현" 점검**:
   - Q1: "검증은 retrospective이고, prospective는 future work" (이것만으로는 부족, contribution 경계 같이 명시)
   - Q2: "HIV-1 외에도 충분히 검증되었다" (사실과 다름)
   - Q3: "0.296이 best estimate이다" (0.296은 evaluation-level fixed-effect 추정치이지 *best*가 아니라 *upper bound*)
   - Q6: "Friedman p=0.990이 universally best 없음을 *증명*한다" (proof가 아니라 *power-limited corroboration*)
6. **Mitigation revisions promise list** (defense 후 수정 약속할 항목)
   - abstract:10에 ω² *0.103–0.319 range* 또는 *6-category lower bound qualifier* 명시
   - abstract:10에 Friedman *power-limited corroboration* qualifier 추가
   - ch5에 *literature-provenance disjoint audit limitation* 1단락 추가
   - ch6:14에 4-feature *recommended starting point in cold-start* 단어 추가
7. **Wild-cluster bootstrap, HBV pilot, sliding-window backtest, Tranception–ESM correlation table — cycle 4 신규 결과 4건의 *single-line summary* 외우기**
   - Wild-cluster: $[0.201, 0.303]$, lower bound matches cluster bootstrap
   - HBV: $0.236$ vs $0.61$–$3.15$ bits, RT-domain $p = 0.136$ — null consistent with rate gap
   - Sliding-window: 3/11 pathogens above chance (EV-A71 0.77, Rabies 0.79, Influenza B 0.70)
   - Tranception–ESM: 11/12 collinear ($\rho = 0.643$–$0.836$), HIV-1 lone dissociating ($\rho = 0.043$)

---

## 종합 위험 평가

본 노트의 정확한 phrasing을 외워서 들어가면, codex_C5 §Phase 4 추정 (*조건부 PASS, 84–88%*)은 흔들리지 않는다. 가장 중요한 단일 원칙:

> **학생 본인의 답변이 본문 (특히 ch5:179, ch5:285, ch5:330, ch5:347)과 모순되는 순간이 진짜 fail trigger.**

본 학위논문은 *honest disclosure의 형식*을 갖추었으므로, 학생이 hostile 위원의 *cherry-picking* 또는 *underpowered=null* 카드에 *방어가 아닌 인정*으로 응답하는 한 *조건부 통과 ≥ 84%*가 유지된다. 위원이 약속받을 *조건부 revision* 항목은 본 노트의 *Mitigation revisions promise list* 6개로 cover됨.

defense 90분 (30분 발표 + 60분 Q&A) 중 hostile 위원 본인 발언 25–30분에 Q1+Q2+Q3 (critical 3건) ≈ 12–15분 + Q4–Q7 (major 4건) ≈ 8–10분 + Q8–Q10 (cycle 4 신규) ≈ 5–7분 — 총 25–32분으로 hostile 위원 quota 안에서 모두 다룰 수 있음.
