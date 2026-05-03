# Cycle 6 Job 4 -- Defense Readability and Q&A Robustness

Scope: active English manuscript files in `paper/dissertation/chapters_en/`, with required input from Cycle 6 Jobs 1--3 and the Cycle 5 professor simulation. This audit simulates oral-defense comprehension, not manuscript validity.

## 1. Q1--Q10 Results Table

| Q | Verdict | Rationale + cite |
|---|---|---|
| Q1. One-sentence thesis understandable without MutBench internals | partly | A non-specialist can understand the dissertation if the thesis is stripped to problem, finding, and use. The current abstract sentence is accurate but too caveat-dense for oral delivery because it combines scope, design size, omega, Layer A caveat, HIV-1 validation, and no prospective validation in one line (`paper/dissertation/front_en/abstract.tex:2`). |
| Q2. Main contribution in three ordered bullets | yes | Ch1 already gives the ordered hierarchy: benchmark infrastructure, pathogen-dependent information-source evidence, and external vaccine-escape validation (`paper/dissertation/chapters_en/ch1_introduction.tex:145`, `:149`, `:154`, `:158`). The candidate should use these as the spoken answer rather than reciting every audit result. |
| Q3. Ch4 explainable with 3--5 core figures/tables | yes | Ch4 has a defensible verbal spine: key-results box, per-pathogen best table, ANOVA table/figure, LOPO table/figure, and vaccine-escape table (`paper/dissertation/chapters_en/ch4_results.tex:9`, `:259`, `:352`, `:376`, `:395`, `:413`, `:915`). The risk is not figure absence but overusing late audit tables. |
| Q4. Likely objections to Layer A, LOPO, HIV-1, and 11 pathogens answered | yes | Layer A heterogeneity and reproducibility limits are explicit (`ch3_methods.tex:200`, `:207`; `ch5_discussion.tex:21`-`:22`); LOPO is explicitly not standalone proof (`ch4_results.tex:437`-`:441`); HIV-1 is distinguished from H3N2/SARS-CoV-2 (`ch4_results.tex:943`-`:952`); and 11-pathogen small-cluster limits are disclosed (`ch5_discussion.tex:182`). |
| Q5. Terminology switches likely to derail Q&A | partly | The 11 vs 12 pathogen split, 3-core vs 4-core, Layer A vs Layer A', and evaluation-level vs cell-level omega are all technically explained, but they demand high working memory (`ch1_introduction.tex:82`-`:91`; `ch4_results.tex:630`, `:657`, `:816`, `:857`; `ch5_discussion.tex:313`). A committee question can easily become a terminology clarification instead of a science question. |
| Q6. Enough "why this matters" language | yes | The introduction explains that hotspot detection prioritizes variants, vaccine targets, and drug-resistance mutations, and reduces a 1,000-position protein to a smaller experimental list (`ch1_introduction.tex:8`-`:11`, `:47`-`:49`). Ch4 and Ch5 restate the practical search-space reduction and resource-prioritization value (`ch4_results.tex:954`-`:955`; `ch5_discussion.tex:88`). |
| Q7. Five likely defense questions generated | yes | The likely questions follow directly from J1--J3 top gaps: late Ch4 audit density, estimand-vs-deployment, audit arc competing with thesis, Layer A curation, and 11/12 denominator switching. See Section 3 below. |
| Q8. Highest-risk sentence identified | yes | The most attackable sentence is the Ch5 contribution recap using "establishes practical relevance" for retrospective vaccine-escape enrichment (`ch5_discussion.tex:98`). It is directionally supported, but the verb is stronger than the evidence tier flagged in Job 3. |
| Q9. Strongest verbal opening sentence identified | yes | The best lead sentence is the final take-home message because it is plain, causal enough for a talk, and avoids most distracting caveats while preserving the core claim (`ch5_discussion.tex:329`). |
| Q10. 5-page defense subset selected | yes | The strongest defense subset should not follow the manuscript page order mechanically. It should combine the Ch1 problem/contribution page, Ch3 ground-truth/method page, Ch4 Stage 2 evidence page, Ch4 practical-validation page, and Ch5 limitations/take-home page. |

## 2. Proposed One-Sentence Thesis

MutBench shows that, for RNA-virus surface-protein hotspot detection, the biological information source that works best depends on the pathogen, so researchers should benchmark and choose information sources pathogen by pathogen rather than relying on one universal frequency-based method.

## 3. Five Likely Defense Questions

1. **If LOPO gives 0/11 matches but is null-consistent, why is pathogen-dependence still your conclusion?**  
   Estimated answer length: **1 minute**. The candidate can answer this in 1 minute by saying the conclusion rests on the scoring-by-pathogen interaction and robustness checks, while LOPO only illustrates the cost of ignoring pathogen identity (`ch4_results.tex:383`, `:437`-`:441`).

2. **Is Layer A a real biological ground truth or a heterogeneous literature construct?**  
   Estimated answer length: **1 minute**. The candidate can answer this in 1 minute: Layer A is an operational literature-curated positive set, not one uniform mechanism, and the dissertation quantifies its circularity and reproducibility limits (`ch3_methods.tex:200`-`:207`; `ch5_discussion.tex:21`-`:22`).

3. **Why is HIV-1 the practical anchor instead of H3N2, which has higher enrichment?**  
   Estimated answer length: **1 sentence**. The candidate can answer in one sentence: H3N2 overlaps Layer A heavily, while HIV-1 has 82% Layer-A-disjoint escape positions and survives the novel-only Bonferroni audit (`ch4_results.tex:943`-`:952`).

4. **Can you recommend a method for a new pathogen today?**  
   Estimated answer length: **1 minute**. The candidate can answer in 1 minute, but only if careful: the 4-feature core is a retrospective cold-start heuristic, not a prospectively callable detector; the abstention rule currently refuses deployment on 0/12 folds (`ch4_results.tex:694`-`:696`; `ch5_discussion.tex:313`).

5. **Why should I trust conclusions from only 11 pathogens, and why do some analyses use 12?**  
   Estimated answer length: **5 minutes**. Mark: **CANNOT answer well in 1 minute**. The answer requires separating the 11-pathogen main benchmark from the 12-pathogen Stage 3 feature-ablation panel, then explaining fixed-effect scope, small-cluster robustness, and future expansion (`ch1_introduction.tex:82`-`:91`; `ch3_methods.tex:812`-`:816`; `ch5_discussion.tex:182`).

## 4. Highest-Risk and Strongest Sentences

**Highest-risk sentence (Q8):**

> "Returning to the three problems identified in Chapter~\ref{ch:introduction}: the evaluation framework, comprising the three-layer ground truth and the hotspot-score metric (Contribution~1), is designed for standardised use, pending external benchmarking by independent teams (with the saturation caveat in Section~\ref{sec:hscore_saturation}); pathogen-dependence is quantified by the interaction effect ($\omega^2 = 0.296$ at the evaluation level, $\omega^2 = 0.234$ at the cell level) and corroborated by LOPO 0/11 (Contribution~2); cross-validation against vaccine-escape positions establishes practical relevance, anchored by HIV-1 (Contribution~3)." (`paper/dissertation/chapters_en/ch5_discussion.tex:98`)

Why it is risky: "establishes practical relevance" is too strong for retrospective, partially overlapping validation. A hostile committee member can ask whether the sentence conflicts with the manuscript's own no-prospective-validation and 3/11 validation limits.

**Strongest opening sentence (Q9):**

> "\textbf{Take-home message}: choosing the right biological information source for the pathogen explains more performance variation than the detection-algorithm main effect alone, and MutBench quantifies that asymmetry." (`paper/dissertation/chapters_en/ch5_discussion.tex:329`)

Why it is strong: it is short, committee-readable, and centers the dissertation's clearest original contribution without opening with omega, Layer A, or audit terminology.

## 5. Five-Page Defense Subset

1. **Chapter 1: Research Background + Motivation** -- Use the problem statement and why hotspot detection matters (`ch1_introduction.tex:8`-`:11`, `:33`-`:39`, `:47`-`:49`).
2. **Chapter 1: Objectives + Contributions** -- Present the three contribution hierarchy exactly in order (`ch1_introduction.tex:79`-`:91`, `:145`-`:158`).
3. **Chapter 3: Ground Truth + Statistical Design** -- Show Layer A/B/C and the pre-specified ANOVA/LOPO frame (`ch3_methods.tex:186`-`:207`, `:209`, `:812`-`:825`).
4. **Chapter 4: Stage 2 Core Evidence** -- Use Key Results, Table `stage2_best`, Table `stage2_anova`, and LOPO/Friedman calibration (`ch4_results.tex:9`-`:14`, `:244`-`:292`, `:352`-`:441`).
5. **Chapter 4/5: Practical Anchor + Boundaries** -- Use HIV-1 escape validation, circularity audit, Layer A limitation, small-cluster limitation, abstention rule, and take-home message (`ch4_results.tex:908`-`:955`; `ch5_discussion.tex:21`-`:22`, `:182`, `:313`, `:328`-`:329`).

## 6. Recommended Manuscript Additions

1. Add a one-page "defense map" table: claim, evidence, boundary, allowed oral wording. This directly addresses the Cycle 5 clarity weakness and prevents committee members from assembling the claim tiers from scattered caveats.

2. Add a small panel-scope box near Ch1 objectives: main benchmark = 11 pathogens; Stage 3 feature-ablation = 12 with Zika; expanded features-only pilots are not benchmark extensions. This would prevent denominator confusion.

3. Replace "establishes practical relevance" with "supports retrospective practical relevance, anchored by HIV-1." This preserves the contribution while aligning with no prospective validation and 3/11 escape-panel availability.

4. Add a spoken-answer paragraph for LOPO: "LOPO is not my proof; it is the operational failure mode that illustrates why the interaction matters." This would make the null-consistent result easier to defend verbally.

5. Add a compact Layer A provenance summary: one row per pathogen with evidence type, dominant source, positive count, and main caveat. This would reduce repeated Q&A around whether Layer A is one biological construct.

RESULT_J4: readability=medium q_a_robustness=medium top_risk=retrospective_vs_deployment
