# Chapter Deep Eval: ch4_results

## In-scope rubric items
- C
- D
- E
- F
- G

## Per-item evidence

### C
**Strongest evidence**:
- Lines 208-213 define the Stage 2 design and metric choice: "20 scoring types... 14 detection method families... 39 parameter variants... 11 pathogens... 8,580 evaluations" and "Stage~2 uses MCC rather than hotspot-score" because stability was not cross-validated across pathogen lengths/MSA sizes.
- Lines 329-371 give a layered statistical method: "three complementary statistical analyses," ANOVA with "bias-corrected effect size omega^2," cluster-bootstrap CI "[0.201, 0.346]," and counterfactual null permutations collapsing the interaction to near zero.
- Lines 901-904 distinguish production EqualWeight from nested-LOPO sign fitting, including "no per-feature sign fit from labels" for the headline protocol and a held-out fold protocol for ablation.

**Weakest evidence / gaps**:
- The methodology is sometimes reconstructed in-results rather than cleanly specified before use. Example: line 367 explains evaluation-level vs cell-level omega only after headline ANOVA, and line 404 explains why 0.341 and 0.297 are not comparable only in a footnote.
- LOPO and Friedman are repeatedly included in the method suite even though later text admits they are "failures-to-reject" and not positive evidence (lines 577-586).

**Hidden issues for panel awareness**:
- Early chapter line 7 says detection families are "(5 categories, 39 parameter variants)," while line 208 says 14 families span 5 categories and scoring types are "organized into 6 categories." Bulk readers may miss that category counts refer to different axes.
- The 3-layer ground truth is stated broadly at lines 225-226, but DMS Layer C is only available for 6/11 pathogens. Any method claim sounding "3-layer" should be read as partially missing Layer C.
- The chapter says "All 11 pathogens exhibit unique best combinations" at line 238, but the table footnote at line 262 admits only 10/11 are unique at parameter-variant tuple level because Influenza B and MERS share freq + KDE p=85.

**Suggested score range**: 8.0--8.8

### D
**Strongest evidence**:
- Line 223 provides strong scale evidence: "8,580 evaluations (20 scoring formulas x 39 detection parameter variants from 14 families x 11 pathogens)."
- Lines 164-176 add temporal breadth: "73 temporal splits in 11 pathogens" and 219 top-k evaluations, plus static-prior extensions.
- Lines 543-570 add an experimental ground-truth breadth check: DMS Layer C for 6 pathogens, with MCC_C values spanning 0.139-0.322 and all 6 changing best scoring type versus Layer A.

**Weakest evidence / gaps**:
- External vaccine/antibody escape validation is only "3 of 11 pathogens" and explicitly a "data-availability convenience sample" (lines 946-949).
- Several later analyses quietly switch to a 12-pathogen feature panel including Zika (lines 608, 635, 862-867), while the main benchmark remains 11 pathogens. This is understandable but raises comparability friction.

**Hidden issues for panel awareness**:
- The "11 pathogens" scale is strong for a dissertation benchmark, but not enough for adaptive weighting: lines 827-831 reject HBFWS/Cycle 7B "at n=11 under the tested feature, label, and validation regime."
- Panel size limits are not just statistical; Layer A curation is rate-limiting. Line 819 states "feature expansion alone does not relax the panel-size limit, and Layer A curation remains rate-limiting."
- Stage 1 and prospective pilots add breadth, but the forward-time signal is weak: line 164 reports grand mean MCC "-0.006" and AUROC "0.539."

**Suggested score range**: 8.2--9.0

### E
**Strongest evidence**:
- Lines 266-269 correctly demote the flashy 11/11 uniqueness result: chance probability is "approximately 93%" and the substantive finding is omega^2 plus the oracle-generalized MCC gap.
- Lines 367-371 carefully define "largest source" as "largest modeled component," disclose residual omega^2 about 0.39, and state that ANOVA/Friedman/LOPO are "consistency checks on the same data, not independent replications."
- Lines 541, 577-586, and 807-811 show mature negative-result interpretation: MERS perfect recall is a "failure case"; LOPO/Friedman are null-consistent; the Cold-Start algorithm is exploratory and "formally abstained from deployment."

**Weakest evidence / gaps**:
- Some result interpretations still overreach in local wording. Line 273 says the near-half negative-MCC fraction is "exactly what pathogen-dependent optimality predicts," which is stronger than the evidence supports because bad grid cells can also arise from weak detectors/noisy features.
- Line 570 says more ground truths would reinforce pathogen-adaptive heterogeneity. That is plausible but speculative; a third ground truth could also reveal label-provenance dependence more than pathogen biology.

**Hidden issues for panel awareness**:
- The chapter often uses the oracle-vs-generalized 0.265 gap, but line 424 says that gap is "not statistically distinguishable" from a random-combination null. Bulk readers may over-credit LOPO.
- Practical interpretation depends heavily on the HIV-1 external anchor; H3N2 and SARS-CoV-2 are mostly self-consistency/exploratory due to Layer A overlap (lines 937, 944, 949).
- The DMS section caption at line 553 says differing Layer A/C winners "confirming their independence," but line 570 appropriately backs down to "non-identical aspects." The caption is slightly overstrong.

**Suggested score range**: 8.3--9.1

### F
**Strongest evidence**:
- Line 221 names the contribution: "statistical demonstration that the most predictive biological information source is pathogen-dependent."
- Line 269 frames the non-trivial contribution as quantifying interaction magnitude, showing information type dominates detection algorithm, and quantifying the cost of ignoring pathogen identity.
- Lines 598-603 connect novelty to wet-lab triage: useful input information changes by pathogen, and univariate AUCs show no single feature should be promoted globally.

**Weakest evidence / gaps**:
- The novelty is less the discovery that pathogens differ and more the scale/statistical quantification. The chapter acknowledges this at line 269, but a strict panel may find "different pathogens favor different methods" biologically unsurprising.
- The Cold-Start 4-core is not the optimal subset: line 799 says the 3-core strictly dominates and "the 4-core is therefore a historical fixed configuration, not an optimum."

**Hidden issues for panel awareness**:
- "All 11 unique best combinations" is not a novelty anchor because chance uniqueness is 93% (line 266) and one parameter-level duplicate exists (line 262).
- AI/PLM novelty is real but uneven: line 457 shows ESM-2 best for RSV/top-3 for SARS-CoV-2 but poor on Norovirus/HIV-1.
- Novelty is strongest as a benchmark-and-audit contribution, not as a deployable algorithmic breakthrough, because P5 gives 0/12 callable folds (line 811).

**Suggested score range**: 7.8--8.7

### G
**Strongest evidence**:
- Line 674 operationalizes the evidence into a wet-lab triage recipe: compute homoplasy, optional pLDDT, entropy, frequency; rank top 10%; and narrow "roughly 1,000 positions to 20--80 candidates."
- Lines 923-937 give concrete escape enrichment: HIV-1 7.19x with 23/45 overlap, Bonferroni-adjusted p about 2.47e-16, and 82% Layer-A-disjoint escape positions with novel-only adjusted p about 3.9e-9.
- Lines 951-952 state the intended practical transformation: for a 500-position protein, "approximately 10--50 positions with 7--9-fold enrichment," a guided investigation rather than exhaustive search.

**Weakest evidence / gaps**:
- Practical evidence is narrow: only 3/11 vaccine-escape datasets, with only HIV-1 as least-circular external anchor (lines 942-949).
- Cold-Start practical value is modest under strict nulls: line 803 gives only about 1.6x expected true positives at 50 sites/pathogen; line 807 says global Stouffer p=1.00 under four nulls; line 811 abstains from deployment.

**Hidden issues for panel awareness**:
- The strongest practical claim uses "optimal scoring--detection combination" (line 952), which is oracle/post-hoc and not necessarily available for a new pathogen.
- EqualWeight practical rows are not fully harmonized: line 937 says H3N2/SARS-CoV-2 and HIV-1 use different pipelines because HIV-1 was not yet integrated into the fixed top-5% pipeline.
- The phrase "called as hotspots" at line 901 could sound detector-like despite the triage reframing; surrounding text mitigates this, but panelists may penalize residual detector language.

**Suggested score range**: 7.0--8.2

## Cross-cutting observations

- The chapter substantially helps the new "wet-lab triage, not deployable detector" framing. Strong guardrails appear at lines 108, 165, 598, 674, 807, and 811.
- The biggest hidden strength is intellectual honesty: it discloses negative-MCC cells, null-consistent LOPO, non-significant Friedman/Nemenyi, ANOVA assumption failures, circularity in escape validation, and deployment abstention.
- The biggest hidden risk is that headline boxes and captions can still sound stronger than the fine print: "unique best combinations," "confirming independence," "exactly what pathogen-dependent optimality predicts," and "optimal combination narrows" need professor-level contextual reading.
- Main benchmark scope shifts among 11 pathogens, 6 DMS pathogens, 3 escape-validation pathogens, and 12 feature-panel pathogens including Zika. The chapter usually flags this, but cross-scope comparisons remain easy to misread.

## Bottom line for Stage 2 panel

Chapter 4 is strongest as a statistically audited benchmark showing pathogen-dependent information-source performance at meaningful scale. The load-bearing evidence is the scoring x pathogen omega^2 interaction with cluster/phylogenetic robustness and the HIV-1 escape anchor, not 11/11 uniqueness, LOPO 0/11, or Friedman. The chapter actively helps panel-level interpretation by refusing deployability and exposing weak/null results, but it also contains subtle overstrong local phrases and scope shifts that a bulk-read panel could miss. Score it high for methodology, scale, and interpretation maturity; score practical value more cautiously because the strongest wet-lab validation is narrow and partly post-hoc/oracle-framed.

RESULT_PROF_V8_STAGE1_ch4: in_scope_items=5 hidden_issues=17 recommended_score_floor=7.0 recommended_score_ceiling=9.1
