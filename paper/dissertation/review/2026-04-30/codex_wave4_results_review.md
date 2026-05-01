# Codex Wave 4 Results Review

## Verdict

**POSITIVE-BOUNDED.** Wave 4 preserves a narrow, useful result: the shared 2-core feature reduction matches the labeled-panel 4-core comparator closely enough to keep Algorithm 1's descriptive signal alive on the current panel.

It does **not** convert the expanded 28-target panel into validation. The expanded targets are feature-compatible enough to justify Layer A curation, but the 1/28 stability result prevents any claim of deployable expanded callability.

## Headline Answer to Codex Q7

**Is the 12-pathogen heterogeneity a small-panel artifact?** Wave 4 does not directly answer that question, because the 16 new targets have no Layer A labels. The narrowed plan-v197 answer is the defensible one: the features-only expansion tests whether a future curated quorum experiment is structurally worth doing, not whether the 12-pathogen result was already an artifact.

On that narrowed question, the answer is constructive but bounded. The 16/16 unlabeled targets fall inside the labeled feature envelope, so Layer A curation is technically motivated. However, hscore is non-harmonizable across the overlap audit and expanded 2-core stability is weak, so the features-only panel cannot substitute for curated labels.

## Defensible Claims

- **The hscore audit is a real negative finding.** Dengue, HIV-1, and Norovirus all failed the overlap harmonization gate; median evidence is nowhere near the predeclared Spearman/top-decile Jaccard thresholds. The correct interpretation is not execution failure, but schema drift: hscore cannot be carried into expanded diagnostics without repair.
- **The 2-core fallback is adequate for the labeled sensitivity question.** On the 12 labeled folds, `freq+entropy` gives mean MCC=0.077, 8/12 positive folds, and paired Wilcoxon p=0.368 against the recomputed 4-core comparator. That supports "2-core approximately matches 4-core on labeled folds," not "2-core is superior."
- **D1 callability remains failed.** The labeled recheck gives 0/12 D1 passes, matching the Wave 2 failure mode. Wave 4 therefore preserves the distinction between descriptive signal and deployable callability.
- **The expanded panel is feature-compatible enough for curation.** All 16 newly added unlabeled targets are inside the labeled envelope, and the 28-target denominator is protected against overlap double counting. This supports moving to pilot Layer A curation rather than dropping the Tier 2 path.
- **Expanded stability is not yet sufficient.** Only 1/28 targets passes the stability proxy. Bootstrap signs match the full-sample signs often but not perfectly (`freq` 81.6%, `entropy` 94.4%), which indicates that sign fitting remains label-limited and should not be operationalized on unlabeled targets.

## Indefensible Claims to Avoid

- Do not say Wave 4 validates Layer A performance on the 16 new targets. No new target has Layer A in this wave.
- Do not say the abstention or callability rule is deployable on 28 targets. Expanded quorum diagnostics are feature-space feasibility checks only.
- Do not say the panel-size hypothesis is confirmed. Wave 4 motivates the curated experiment needed to test that hypothesis.
- Do not describe hscore as harmonized. The audit fired Branch 5 and forced the 2-core fallback.
- Do not use the 16/16 envelope result as a biological-success claim. It is an input-compatibility result.
- Do not treat 1/28 stability as evidence that the unlabeled targets are biologically poor. It is evidence that the current features-only sign/rank procedure is not stable enough without more labels or harmonization.

## Wave 5 Conditional Ordering

Proceed to **pilot 3 Layer A curation for YFV/Lassa/WNV** as planned. The condition from the Wave 4 review was that labeled shared-feature performance not be clearly negative before curation. The observed labeled result is bounded positive: mean MCC=0.077, 8/12 positive folds, and no significant degradation against 4-core. The curation should be framed as the next experiment that converts feature-compatible targets into a real quorum test, not as a continuation of Wave 4 validation.

If the user instead chooses the manuscript negative-results cleanup path, the ordering changes as follows: defer YFV/Lassa/WNV curation; add bounded prose to Chapter 5 that Wave 4 found hscore schema drift, 2-core labeled preservation, and insufficient expanded stability; sharpen the Future Work claim around "curated labels are rate-limiting"; and avoid adding any new Algorithm 1 performance claims beyond the 12 labeled folds.

## Defense-Readiness Re-Scoring

**Medium.** Wave 4 improves defense readiness relative to the plan-review risk because the dangerous overclaim is now easy to avoid: the result cleanly separates labeled performance from unlabeled diagnostics. The 2-core labeled result keeps the descriptive signal alive, while 0/12 D1 and 1/28 stability keep deployment claims bounded.

I would not score this High, because the central expanded-panel hypothesis remains untested until Layer A labels exist for at least a pilot set. I would also not score it Medium-High, because the hscore failure was handled by the predeclared branch and the 16/16 envelope result gives a concrete reason to proceed with curation rather than treating Wave 4 as a dead end.

## Concrete Edits to `ch5_discussion.tex` Future Work

- Add one bounded sentence: "A features-only Tier 2 sweep over 28 unique targets found that the shared `freq+entropy` core preserved bounded labeled-panel signal but that hscore was not harmonizable across overlap targets."
- Add one caution sentence: "Because the 16 newly added targets lack Layer A labels, expanded-panel stability is a feasibility diagnostic rather than validation, and the 1/28 stability result argues against any deployable expanded callability claim."
- Add one next-step sentence: "The immediate follow-up is a pilot Layer A curation of YFV, Lassa, and WNV to turn feature-compatible targets into a real quorum test."
