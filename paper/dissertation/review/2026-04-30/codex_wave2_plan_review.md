# Codex Wave 2 P5 Plan Review

## Verdict

**PROCEED WITH MODIFICATIONS.** The plan is faithful to the P5 callability rule in substance, but it needs tightening before Task 2: clarify that D4 uses held-out annotation-density metadata, make abstention reasons first-class outputs, remove the misleading “no held-out labels” wording, keep the inversion guardrail per-method, and treat P1 overlap as a diagnostic sanity check rather than a criterion.

## Q1. Implementation fidelity

D1-D4 mostly match the §3 spec. Use **7/11** as the default D1 quorum: it is stricter than a bare majority without making the gate so brittle that one noisy training pathogen dominates. Do not raise the default to 8/11; reserve 8/11 for the sensitivity sweep. D2 bootstrapping over the 11 training pathogens is the right resampling unit because callability is a cross-pathogen deployment decision, not a within-pathogen position-level claim. D3’s 0.10 × per-feature SD is acceptable as a predeclared stress perturbation, but call it a fixed stability stress test unless actual measurement variance is available. D3 should include both score jitter and sign re-fit on bootstrap training pathogens; this captures rank and sign uncertainty. D4’s [1%, 20%] prevalence band is acceptable; do not tighten to 15% just because HCV sits near 15.9%, since that would read as outcome-aware.

## Q2. Inversion guardrail scope

Keep the inversion guardrail **per-method**. A 3-core rule should not be forced to abstain merely because the historical 4-core inverts on the same fold, especially after P3 weakened the fixed 4-core rationale. Report guardrail status separately for 3-core and 4-core. Add a secondary “any-method inversion observed” flag for interpretation only, not for callability.

## Q3. Default thresholds

The D1 × D2 sweep range is appropriate: quorum {5, 6, 7, 8}/11 and D2 lower bound {1.05, 1.10, 1.20, 1.50} covers permissive, default, strict, and very strict regimes. Do **not** vary D3 thresholds, D4 prevalence band, or inversion count in the main sweep; that would multiply researcher degrees of freedom and weaken the pre-registration. If D3 or D4 is unexpectedly rate-limiting, report that descriptively and defer altered thresholds to a future protocol.

## Q4. Endpoint reporting

Yes: add per-pathogen abstention reason columns for D1, D2, D3, D4, and inversion, and include them in the report table. Keep “always-deploy + random on abstained” as a secondary comparator, but label it as a policy baseline, not a competing model. Also report decision-curve budgets 20, 50, and 80 on callable pathogens; TP@50 remains the primary budget, while 20 and 80 show whether the conclusion depends on one arbitrary review budget.

## Q5. Cross-check against P1's 5 iid-significant pathogens

Do **not** formalize an expected overlap threshold such as ≥3/5. The P1 significant set is prior evidence that motivated P5, but using it as a pass/fail condition would import the Wave 1 outcome into the Wave 2 decision rule. Keep overlap as a qualitative implementation sanity check: if overlap is 0/5, inspect for coding errors or diagnostic mismatch; if the implementation is correct, report the divergence transparently.

## Q6. Plan-level concerns

The main leakage concern is D4 wording. D4 uses held-out Layer A positive count and prevalence, so the plan must state that this is held-out annotation-density metadata used only to decide whether evaluation is statistically interpretable; it is not score-, rank-, MCC-, enrichment-, or p-value-based. The implementation should output all diagnostic components even when an early criterion fails, avoiding hidden short-circuit behavior. The inner sweep must be reported as sensitivity only, unless a stricter threshold is selected using inner training-only logic before outer evaluation; do not choose a looser threshold after seeing outer callable performance. Finally, if the plan keeps “inner LOO” language, the script should actually perform inner training-only threshold selection or rename the step to “threshold sensitivity sweep.”

## Q7. After P5 - Wave 3 ordering

Highest ROI after any nonzero P5 success is **(d) P6 biological-realistic local nulls on the existing 12-pathogen panel**. It directly addresses the largest remaining defense risk: whether callable-pathogen signal survives a more credible local/domain-aware null. Next is **(b) Tier 2 features-only LOPO at n≈30**, because it tests callability coverage without waiting for full curation. Third is **(a) pilot 3 Layer A literature curation for YFV/Lassa/WNV**, useful but slower and narrower. Fourth is **(c) Tier 3 EVE/PLM**, which is interesting but least direct for defending the current Algorithm 1 abstention claim.

## Concrete Edits

- `/proj/paper/docs/plans/2026-04-30-wave2-p5-callability.md:31`: Change “training-estimated measurement noise proxy” to “fixed stability stress perturbation; replace with empirical measurement variance only if available before execution.”
- `/proj/paper/docs/plans/2026-04-30-wave2-p5-callability.md:32`: Replace “Uses no scores or held-out labels in the decision” with “Uses only held-out annotation-density metadata: positive count, rankable-site count, and prevalence; no held-out scores, ranks, MCC, enrichment, or p-values.”
- `/proj/paper/docs/plans/2026-04-30-wave2-p5-callability.md:36`: Change “not callable for this fold family” to “not callable for this fold-method pair”; add “also record whether either method fired the guardrail as an interpretive flag.”
- `/proj/paper/docs/plans/2026-04-30-wave2-p5-callability.md:40-41`: Add TP@20 and TP@80 as secondary decision-curve budgets; retain MCC and TP@50 as primary endpoints.
- `/proj/paper/docs/plans/2026-04-30-wave2-p5-callability.md:55`: Add columns for `d1_fail`, `d2_fail`, `d3_fail`, `d4_fail`, `inversion_fail`, and a compact `abstention_reason`.
- `/proj/paper/docs/plans/2026-04-30-wave2-p5-callability.md:180`: Remove `top-20 precision` from the primary deployment record unless it is explicitly defined as secondary; replace with `TP@20, TP@50, TP@80`.
- `/proj/paper/docs/plans/2026-04-30-wave2-p5-callability.md:239`: Replace “should overlap meaningfully” with “overlap is a qualitative implementation sanity check only; it is not a pass/fail criterion.”
- `/proj/paper/docs/plans/2026-04-30-wave2-p5-callability.md:261-274`: If thresholds are not actually selected by inner LOO before outer evaluation, rename this section from “inner LOO” to “predeclared threshold sensitivity sweep.”

## Wave 3 Ordering Recommendation

Run **P6 biological-realistic local nulls first**, then **Tier 2 features-only LOPO at n≈30**, then **pilot 3 Layer A curation**, then **EVE/PLM site-effect**. P6 is the most direct next defense of P5 because it asks whether the callable subset survives the null model most likely to be challenged.
