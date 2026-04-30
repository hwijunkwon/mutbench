Below are the highest-ROI additional experiments I would run. I would prioritize experiments that make Algorithm 1 look like a controlled, falsifiable search-space-reduction method, not another failed adaptive-weighting attempt.

**P1. Cold-Start Null Calibration / Label-Permutation Stress Test**

**Hypothesis:** The fixed 4-feature Cold-Start ensemble performs above realistic null callsets even after preserving pathogen-specific label prevalence and candidate-list size.

**Protocol:** Use the existing 12-pathogen feature matrices and Algorithm 1’s fixed top-10% calls. For each pathogen, generate 1,000-10,000 null label sets preserving the number of Layer A positives; preferably use circular shifts or block permutations along protein coordinates to preserve regional clustering better than iid shuffles. Recompute MCC, precision@top10%, enrichment, and ±10-window MCC for the 4-core, full-10, and best single feature. Report where the observed 4-core lies in the null distribution per pathogen and globally via paired sign-flip or Stouffer aggregation.

**Expected outcome:** Null mean should sit near MCC 0 and enrichment 1.0. The 4-core mean MCC of ~0.081 should likely land above the null globally, though not for every pathogen. I would expect 7-9 of 12 pathogens to be directionally positive, with the strongest support from pathogens already carrying the search-space-reduction claim.

**Defense question pre-empted:** “Is this just a top-10% heuristic that would look good under any clustered ground truth?”

**Compute budget:** ~1-3 CPU-hours.

**Risk if it fails:** Moderate. A global null failure would weaken the method claim. A few per-pathogen failures are acceptable and consistent with the dissertation’s pathogen-dependence argument.

---

**P2. Rank-Calibration / Reliability Curve for Algorithm 1**

**Hypothesis:** Cold-Start scores are useful as a rank-ordered prioritization signal: higher score deciles contain higher empirical hotspot density even when absolute classification accuracy is modest.

**Protocol:** For each pathogen, compute the fixed 4-core score for every position, bin positions into deciles, and plot empirical Layer A prevalence, ±10-window coverage, and enrichment by decile. Add leave-one-pathogen bootstrap confidence bands. Compare against full-10, best single feature, and random deciles. The key table should report top-10%, top-20%, and bottom-50% prevalence/enrichment.

**Expected outcome:** Top decile should be enriched over baseline but uneven. The likely strongest claim is not “calibrated probability,” but “monotone or near-monotone prioritization in aggregate.” Given current MCC values, expect noisy middle deciles and clearer top-vs-bottom separation.

**Defense question pre-empted:** “If MCC is only ~0.08, why should anyone trust the ranked list?”

**Compute budget:** <1 CPU-hour.

**Risk if it fails:** Low to moderate. If monotonicity is weak, the result can still be reported as “top-k enrichment, not probability calibration.” It would mainly argue against overclaiming calibrated risk.

---

**P3. Fixed-Core Necessity Audit: Leave-One-Feature-Out and Shapley-Style Decomposition**

**Hypothesis:** The 4-core is not arbitrary; its features contribute complementary signal, and removing any major component reduces at least one robustness metric.

**Protocol:** Evaluate all fixed subsets of the 4-core: each single feature, all pairs, all triples, and the full four-feature ensemble under the same nested-LOPO/top-10% protocol. Report paired deltas versus the full 4-core for MCC, enrichment, precision@top10%, and pathogen win count. Optionally compute a simple Shapley-style contribution over the 15 subsets, without fitting new weights.

**Expected outcome:** Frequency/entropy/homoplasy probably carry most of the signal. pLDDT may be weaker or pathogen-specific, so the best defensible outcome may be: “three features carry the average lift, pLDDT improves coverage/robustness on structural regimes but is optional.” That is still useful because it clarifies why Algorithm 1 is constructed as a multi-source ensemble.

**Defense question pre-empted:** “Why these four features? Why not just frequency plus entropy?”

**Compute budget:** ~1-2 CPU-hours.

**Risk if it fails:** Low. If one feature is dead weight, revise Algorithm 1 text to call it optional or report a 3-core sensitivity. That improves honesty more than it hurts.

---

**P4. Detector-Arbitrariness / Consensus Stability Audit**

**Hypothesis:** The method’s practical value is driven by scoring information, not by cherry-picking one detector variant; high-performing detector families converge on overlapping candidate regions.

**Protocol:** Rerun or reuse Stage 3 detector callsets for the 4-core and full-10 scores. Compute pairwise Jaccard overlap, rank correlation, and consensus frequency across the 39 detector variants per pathogen. Compare hotspot enrichment for positions called by ≥25%, ≥50%, and ≥75% of detectors. Stratify by detector family if available: Wavelet, HDBSCAN/MutClust, threshold-based, etc.

**Expected outcome:** Consensus will likely improve precision/enrichment while reducing recall. Agreement may be moderate rather than high, which is fine if consensus calls are enriched and detector disagreement is concentrated near threshold boundaries.

**Defense question pre-empted:** “Are the results an artifact of one detector setting?”

**Compute budget:** ~1-4 CPU-hours if callsets are already recoverable; <24 hours even if rerunning Stage 3 call generation.

**Risk if it fails:** Low. A null result would support the existing claim that detector choice matters and that the benchmark exposes this variability.

---

**P5. Prospective Failure-Mode Decomposition / Selective Callability Diagnostic**

**Hypothesis:** MutBench should not be claimed as universally prospective, but existing temporal backtests can identify regimes where forward-time prioritization is plausible versus regimes where the method should abstain.

**Protocol:** Use the existing 73-window temporal backtest outputs. Stratify windows by measurable pre-test diagnostics: number of year-tagged positions, baseline emergence rate, score variance, entropy/frequency dispersion, top-decile separation, and pathogen family. Compare AUROC/MCC/enrichment across diagnostic strata. The goal is not to train a new predictor, but to define descriptive “callable” versus “not callable” regimes and test whether EV-A71/Rabies/Influenza B fall into the callable stratum.

**Expected outcome:** I would expect partial separation: EV-A71 and Rabies likely look callable; HCV and several others likely remain uncallable. The strongest conclusion would be a disciplined abstention rule, not a rescued prospective claim.

**Defense question pre-empted:** “You admit prospective validation is weak. When should this method be used, and when should it not be trusted?”

**Compute budget:** ~1-3 CPU-hours.

**Risk if it fails:** Low. If no diagnostic separates success from failure, it reinforces the current limitation and avoids overclaiming. It does not damage the retrospective search-space-reduction contribution.

---

**Prioritized order:** P1, P2, P3, P5, P4.

If defense were tomorrow, I would skip P4 first. P1-P3 directly strengthen Algorithm 1 as a plausible method; P5 is the best way to handle the prospective-validation vulnerability without pretending the existing negative temporal evidence is positive.