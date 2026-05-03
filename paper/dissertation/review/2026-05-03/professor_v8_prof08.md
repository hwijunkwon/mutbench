# Professor 8: Practice/field user (strictness=high)

## Stage 1 reports consulted
- abstract_ch1: Strong bounded framing and contribution hierarchy, with residual prospective/cold-start wording drift.
- ch2: Current and task-aware related work; strong benchmark-gap framing, but compressed coverage of coupling/epistasis and some result leakage.
- ch3: Mature auditable methods and substantial scale, offset by dense prose, deferred sensitivities, and uneven ground-truth depth.
- ch4: Strong statistical results and honest negative audits; practical value depends mainly on HIV-1 and several scope shifts need careful reading.
- ch5: Excellent limitations and claim calibration; denominator drift and dense audit/wave material weaken readability.

## Specialty deep-read
- abstract+ch1: The abstract now leads with "retrospective wet-lab triage rather than prospective deployment" and the Chapter 1 panel-scope ledger is useful; however, the figure still says "Practical Impact" and the objective/contribution language still uses "cold-start recipe" in ways a field user could over-read.
- ch4: The strongest practice-facing passage is the vaccine-escape audit: HIV-1 has 7.19x enrichment with 82% Layer-A-disjoint support, while H3N2 is explicitly downgraded to self-consistency and SARS-CoV-2 remains exploratory. I also noted the forward-time sanity check is weak overall (grand mean MCC -0.006, AUROC 0.539), which matters for field use.
- ch5: The discussion is impressively explicit that use is retrospective prioritization only, with 0/12 callable folds and failed adaptive selection. The practical workflow is useful, but it mixes an informed-use ceiling with a cold-start heuristic that the later audits show is not an optimum.

## Scores
A: 8.5
B: 8.3
C: 8.4
D: 8.5
E: 8.4
F: 8.2
G: 7.6
H: 7.8
I: 9.1
J: 8.4
total: 83.2/100

## Rationale (per item, 2-3 sentences each, citing Stage 1 evidence + your specialty observations)

**A. problem statement: 8.5**  
Stage 1 abstract_ch1 shows a clear problem frame: no standardized viral hotspot benchmark, no independent ground-truth framework, and no quantified pathogen-dependence of best methods. My direct read confirms that the abstract and Chapter 1 repeatedly delimit the task as single-position wet-lab triage, not prospective deployment. I deduct because small wording slips remain: "Practical Impact," "variant monitoring," and "cold-start recipe" can still invite a field user to expect operational prediction.

**B. related work: 8.3**  
Stage 1 ch2 supports a high score: it separates MutBench from surveillance tools, VEP benchmarks, selection tests, and cancer hotspot precedents, and it anchors the benchmark gap against current comparators. The weakness is not absence of literature, but uneven depth: coupling-aware/epistasis methods are mostly excluded, HyPhy-family coverage is selective, and some final-result numbers appear inside the background. For a practice-facing evaluation, the task boundary is persuasive enough, but not exhaustive enough for a 9.

**C. methodology: 8.4**  
Stage 1 ch3 and ch4 identify a strong methodological contract: 3-layer ground truth, 20 scoring types, 39 detector variants, frozen thresholds, MCC evaluation, ANOVA with cluster-bootstrap CI, and explicit LOPO/Friedman interpretation. My ch4 read confirms the methods are unusually transparent about residuals, null permutations, and production versus nested-LOPO EqualWeight protocols. Deductions come from deferred ablations, partial Layer C availability, correlated scoring channels, and result-like material embedded in methods/results boundaries.

**D. scale (panel size, breadth): 8.5**  
Stage 1 ch3/ch4 document a substantial dissertation-scale benchmark: 11 RNA viruses, 8,580 evaluations, 73 temporal splits, and Layer C DMS checks for 6 pathogens. This is broad for region-level single-position viral hotspot benchmarking and includes biologically diverse surface glycoproteins. It is still not broad enough for deployable adaptive inference, whole-virus scope, or balanced external validation, and the 11/12-pathogen denominator shifts reduce apparent cleanliness.

**E. interpretation (results reading): 8.4**  
Stage 1 ch4/ch5 show mature interpretation: uniqueness is demoted because it is likely by chance, LOPO 0/11 is treated as null-consistent corroboration, and Friedman p=0.990 is not oversold. My direct read confirms the discussion explains low MCC, forward-time weakness, oracle/generalized gaps, and the difference between retrospective signal and callability. I deduct for a few overstrong local phrasings, especially "exactly what pathogen-dependent optimality predicts" and some claims that additional ground truths would reinforce rather than possibly complicate the story.

**F. novelty/contribution: 8.2**  
The novelty is strongest as a benchmark-and-audit contribution: broad single-position viral hotspot evaluation, quantified scoring-by-pathogen interaction, and guarded external triage validation. Stage 1 rightly notes that "different pathogens favor different methods" is biologically unsurprising; the contribution is the measurement, scale, and discipline of the negative adaptive-selector result. I deduct because the cold-start 4-core is a historical heuristic rather than an optimized contribution, and the "broadest" claim depends on a narrow region-level qualifier.

**G. practical value (wet-lab triage utility): 7.6**  
As a field user, I see real practical value: the abstract, ch4, and ch5 converge on search-space reduction from about 1,000 positions to 10-50 candidates, with HIV-1 7.19x escape enrichment and Layer C DMS support across 6/11 pathogens. But strict scoring must penalize the narrow independent validation base: vaccine-escape validation is 3/11 pathogens, HIV-1 is the main clean external anchor, H3N2 is mostly self-consistency, SARS-CoV-2 exploratory, and cold-start callability is 0/12. This is useful retrospective triage, not a field-ready prospective tool.

**H. clarity (writing): 7.8**  
Stage 1 reports consistently praise ledgers, scope tables, and careful guardrails, and I agree that these prevent dangerous overclaiming. The cost is density: Stage/Cycle/Wave/Layer terminology, 11-versus-12 panels, long caveat paragraphs, and anchor-preservation labels make the dissertation harder for non-specialist field users to operationalize. The writing is defensible and mostly clear, but not clean.

**I. limitations awareness: 9.1**  
Stage 1 ch5 gives the strongest evidence here: explicit limitations on Layer A heterogeneity, prospective failure, PLM leakage, winner's curse, small panel size, independent reproduction, dual-use risk, and MAFFT artifacts. My direct read confirms the manuscript states retrospective prioritization only and requires future callability/adaptive-method gates before deployment. I reserve a small deduction because several limitations remain unresolved by design, especially independent recuration and source-selection sensitivity.

**J. overall maturity: 8.4**  
The manuscript is scientifically mature in the way that matters most: it keeps negative results visible, refuses deployment, distinguishes evidence tiers, and provides provenance anchors. Stage 1 reports and my direct read both show the post-reframe version has repaired major overclaim risk. The remaining maturity deductions are integration-level: denominator drift, dense audit patches, practical claims that still need oral clarification, and dependence on one main external field anchor.

## Strongest single deduction
one-line: G, because independent wet-lab/escape validation is too narrow for field-ready use; fix by adding balanced residue-level external validation or prospective callable-fold evidence beyond the HIV-1 anchor.

RESULT_PROF_V8_08: total=83.2/100 min_item=7.6(G) max_item=9.1(I) stage1_evidence_used=5
