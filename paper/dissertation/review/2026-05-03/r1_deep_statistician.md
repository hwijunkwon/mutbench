# Risk-1 Deep Statistician Rebuttal Script

## Opening question

**Statistician:** "You have 11 pathogen clusters. You cannot prove non-learnability or a panel-size threshold from 11 units; the cluster bootstrap and random-effects interpretation are underpowered or anti-conservative."

## Follow-up questions

### 1. Small-cluster bootstrap

**Quote.** "Why should I trust a 95% cluster-bootstrap interval with only 11 clusters, especially when the thesis itself says small-cluster bootstrap can be anti-conservative?"

**Why hard.** This is the cleanest statistical attack: the dissertation uses pathogen as the effective cluster, and 11 is below the usual comfort zone for cluster-robust inference. If the answer treats the interval as a precise confidence statement, the committee member can dismiss the headline CI as overconfident.

**Best rebuttal.** I would not ask you to treat the 11-cluster interval as a definitive population CI. The dissertation explicitly says the effective independent unit is closer to the 3,080 scoring-family-pathogen cells than to 8,580 rows, interprets the ANOVA through pathogen-cluster checks, and labels the 11-cluster BCa/percentile frame approximate with observed undercoverage in a small simulation (Ch3 lines 764-768, 803-810). The defensible claim is convergence across frames: standard cluster, wild-cluster Rademacher, phylogenetic block, mixed-effects variance component, Bayesian factor analysis, cell-level aggregation, ANCOVA, and leave-one-pathogen-out sensitivity all keep the scoring-by-pathogen effect above the practical large-effect reference (Ch4 lines 393-397, 485-508, 510-517).

**Backup citation.** Use MacKinnon and Webb on wild-cluster inference with few clusters, Cameron, Gelbach, and Miller on bootstrap-based cluster correction, and Roodman's `boottest` guidance as the reason for treating the interval as a robustness frame rather than a magic fix. The exact defense language should be: "small-G bootstrap is a caveat I accept; the inference rests on triangulation and effect-size stability, not nominal 95% coverage."

### 2. Random effects and mixed models

**Quote.** "Are you estimating a pathogen random effect from 11 levels and then generalizing to all pathogens?"

**Why hard.** A statistician in statistical genetics or ecology will know that random-effect variance components are unstable with few levels, and 11 viruses are not a probability sample from the universe of pathogens. Treating the mixed-effects result as population inference would be an overreach.

**Best rebuttal.** No; the mixed-effects result is a diagnostic cross-check, not the load-bearing estimator. The dissertation's primary estimator is fixed-factor variance decomposition on the observed benchmark panel, with the more conservative cell-level scoring-by-pathogen effect reported separately from the evaluation-level value (Ch3 lines 764-772; Ch4 lines 393-395). The mixed-effects pseudo-omega result is included alongside wild-cluster, phylogenetic block, and Bayesian factor-analysis frames to test whether the qualitative interaction survives model re-expression; the defended claim is "pathogen-dependent information utility in this 11-pathogen panel," not a random sample theorem about all viruses (Ch3 lines 809-810; Ch4 lines 489-490, 500-504).

**Backup citation.** Bolker et al. on GLMM practice and Ben Bolker's mixed-model guidance support the rule-of-thumb that random effects with few levels should be interpreted cautiously and that 20-30 levels is a design target, not a discovered threshold. A concise oral answer: "I am not selling 11 as enough for stable pathogen-population variance; I am using 11 to falsify a deployable universal-selector claim within this audited panel."

### 3. Multiple comparisons and post-hoc null calibration

**Quote.** "You searched 20 scoring types, 14 families, 39 variants, top-20 Friedman ranks, 190 Nemenyi pairs, and multiple robustness analyses. How do I know this is not selective reporting?"

**Why hard.** The benchmark has a large analytic lattice, and a statistician will worry that the headline interaction, best combination, and post-hoc summaries were found after looking. The Nemenyi results are especially vulnerable because post-hoc tests after a non-significant Friedman test can look like fishing.

**Best rebuttal.** The ANOVA is not presented as 780 pairwise discoveries; it decomposes pre-specified factors and reports a bias-corrected effect size, while the dissertation explicitly separates variance-component interpretation from pairwise multiple testing (Ch3 lines 761-777). The Friedman/Nemenyi block is deliberately negative: Friedman gives p = 0.990 and W = 0.037, and Nemenyi reports 0/190 significant pairs even before Bonferroni; that is not a discovery claim but a calibration showing the 11-block design cannot distinguish top methods by rank (Ch4 lines 432-445). The LOPO section also includes permutation nulls showing that 0/11 exact matches and the 0.265 gap are weak in isolation, so the dissertation is actively downgrading tempting post-hoc evidence rather than amplifying it (Ch4 lines 447-453).

**Backup citation.** Cohen's omega-squared benchmarks can justify the large-effect reference only as a conventional scale, with the dissertation already warning that computational benchmarks may need different calibration (Ch3 lines 766-777; Ch4 lines 382-393). Demsar is the appropriate backup for Friedman/Nemenyi over classifiers across datasets, but the answer should stress that Nemenyi is descriptive/null-confirming here, not proof of no difference.

## Trap questions

### 1. A real panel-size threshold

**Quote.** "Where is the power analysis proving that 20-30 pathogens is the threshold for learnability or random-effects validity?"

**Why weak.** The dissertation does not estimate a formal phase transition or perform a prospective power analysis for 20, 25, or 30 pathogens. It uses 20-30 as a design target motivated by mixed-model practice and by the observed instability of 11-cluster validation, not as an empirical theorem.

**Best honest response.** I agree that the thesis does not prove a 20-30 pathogen threshold. The correct wording is that n = 11 is sufficient to expose a finite-panel non-deployability problem under the tested design, while 20-30 is a next-study design requirement for credible random-effect and held-out-panel inference. I would remove or soften any phrasing that sounds like a discovered threshold and say "target panel size for a confirmatory study."

### 2. Biology versus label-provenance confounding

**Quote.** "How do you know scoring-by-pathogen interaction is biology, rather than different Layer A curation rules producing different winners?"

**Why weak.** This is genuinely hard because the dissertation admits Layer A mixes convergent evolution, immune escape, and HVR-membership evidence types. HCV exclusion, positive-rate adjustment, and counterfactual nulls reduce the concern but do not fully separate biological pathogen dependence from label-construction dependence.

**Best honest response.** I would acknowledge that the interaction is a joint property of pathogen biology, protein/input structure, and Layer A provenance. The dissertation partially addresses this by using MCC under explicit Layer A definitions, adjusting for protein length and positive rate, excluding HCV, running leave-one-pathogen-out omega sensitivity, and showing the interaction survives cell-level and Bayesian frames (Ch3 lines 770-772; Ch4 lines 397-399, 508-517). The narrow claim should therefore be "pathogen-dependent information utility under the dissertation's curated label regime," not "pure biological causality."

## Most likely deduction

**Most likely deduction: 1.0-1.5 points.** A strict statistician would likely accept the guarded finite-panel result but deduct for small-G inference, lack of formal power analysis for the 20-30 target, and incomplete separation of biological signal from label-provenance signal.

`RESULT_R1_DEEP_STAT: anticipated_score=7.2/10 weak_count=2 rebuttable_count=3`
