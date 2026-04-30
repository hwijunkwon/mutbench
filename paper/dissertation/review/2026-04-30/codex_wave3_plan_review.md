# Codex Wave 3 P6 Plan Review

## Verdict

**PROCEED WITH MODIFICATIONS.** P6 is the correct Wave 3 experiment and the four nulls are defensible. The plan needs three fixes before Task 2: define stratum collapse correctly, reframe P6 as structurally explicit rather than an ordered strictness ladder beyond P1, and add the missing LaTeX label/reporting guardrails.

## Q1. Null Type Selection

Keep the four planned nulls. SASA and pLDDT are the right structural marginals; SASA x frequency and pLDDT x entropy are the right first joint structural-evolutionary stress tests. Do not add dN/dS unless it already exists per site for all 12 pathogens in the same feature matrices; acquiring or deriving it now expands scope and creates another provenance problem. Do not add domain-stratified or secondary-structure nulls in Wave 3 unless annotations are already complete and coordinate-stable. P6.4 overlaps conceptually with P1 local-burden, but its structural conditioning via pLDDT makes it useful.

## Q2. Quintile vs. Tertile Binning

Use 5 bins for marginal nulls and 3 x 3 bins for joint nulls. That is the right balance between biological matching and finite-label support. Do not use 5 x 5 cells on the current 12-pathogen panel; sparse positives will make the null mostly immobile for MERS-like pathogens. Do not switch to uniform quartiles just for aesthetic consistency. Continuous rank-local shuffles are attractive, but they are a new method; defer them unless P6 becomes a dedicated methods appendix.

## Q3. Stratum Collapse Handling

Revise the collapse rule. A cell with zero positives is not a failure; it is exactly what stratum-preserving shuffling should preserve. The failure condition is a degenerate null: too few cells contain both positives and negatives, too few positives are movable, or the permutation distribution has near-zero variance. Do not pool adjacent cells or use pathogen-specific 2 x 2 binning in the primary analysis. For a collapsed pathogen-null pair, report `no_result_degenerate_null`; otherwise keep all cells fixed or shuffled as dictated by their labels.

## Q4. Comparison Against P1 Local-Burden Null

Keep all four P6 nulls, but reframe them as **structurally explicit biological nulls**, not as four fully independent tests and not as a monotone strictness extension of P1. P1 local-burden conditions on local evolutionary burden; P6 asks whether the signal survives explicit structural or structural-evolutionary matching. In the report, state the overlap with P1 local-burden directly and treat concordance across P1 local-burden and P6 as robustness, not independent replication.

## Q5. Headline Statistic

Use two headlines, in this order: per-null counts of individually significant pathogens, then Norovirus survival across all four P6 nulls. The unified P1+P6 gradient is useful as a figure, but it should not be the main claim because the eight nulls are not a single ordered ladder of increasing strictness. The strictest defensible sentence is: "Under structurally explicit P6 nulls, N of 12 pathogens retain individual significance under each null, and Norovirus does/does not survive all four."

## Q6. Wave 3 Scope

P6-only is the right Wave 3 scope. Combining it with Tier 2 features-only LOPO or new Layer A curation would blur the purpose of the wave and make the defense narrative harder to audit. P6 answers the live objection against the current 12-pathogen result: whether callable-subset signal is a structural/evolutionary clustering artifact. Finish that cleanly before adding panel-size or manual-curation questions.

## Q7. After P6 - Wave 4 Ordering

If at least one pathogen survives P6, the Wave 4 order should be: **(a) Tier 2 features-only LOPO at n~30**, then **(b) pilot 3 Layer A curation for YFV/Lassa/WNV**, then **(d) defense rehearsal / 6-agent cumulative review**, then **(c) EVE/PLM site-effect**. Tier 2 is the highest ROI because it tests whether the 12-pathogen heterogeneity is a small-panel artifact. Manual curation is next because it converts selected Tier 2 targets into real validation. EVE/PLM is lower priority unless the committee specifically challenges missing external site-effect evidence.

## Q8. Plan-Level Concerns

The main risk is accidental overclaiming, not leakage. Strata are computed from existing feature columns and labels are only shuffled, so there is no obvious held-out performance leakage. The implementation must use fixed predeclared nulls regardless of which one is favorable, include `(b + 1)/(n_perm + 1)` p-value smoothing, report `n_valid` denominators for skipped pathogen-null pairs, and avoid selecting the "best" P6 null after seeing results. Also add explicit handling for missing/constant/NA feature columns and ensure metrics are computed on the full position set, not only on permutable cells.

## Concrete Edits

- `/proj/paper/docs/plans/2026-04-30-wave3-p6-biological-nulls.md:34`: Replace the comparison paragraph with language that P6 is "structurally explicit" and partially overlapping with P1 local-burden, not independent replication.
- `/proj/paper/docs/plans/2026-04-30-wave3-p6-biological-nulls.md:49`: Replace "0 positives in some cells" as collapse. Define collapse as fewer than two strata with both positive and negative labels, fewer than five movable positives, or near-zero null variance; otherwise keep zero-positive cells fixed.
- `/proj/paper/docs/plans/2026-04-30-wave3-p6-biological-nulls.md:159-160`: Replace "Cells with <2 positions or 0 positives are flagged and omitted" with "Cells with no possible label movement are kept fixed in the full-length label vector; only degenerate pathogen-null pairs are reported as no-result."
- `/proj/paper/docs/plans/2026-04-30-wave3-p6-biological-nulls.md:68`: Change expected row count from fixed `384` to `up to 384`, with `n_valid`, `degenerate_null`, and `skip_reason` columns.
- `/proj/paper/docs/plans/2026-04-30-wave3-p6-biological-nulls.md:71`: Rename the "unified gradient" description so it is a comparative robustness figure, not a strict ordered ladder.
- `/proj/paper/docs/plans/2026-04-30-wave3-p6-biological-nulls.md:207`: Replace "Norovirus should remain strongly significant" with "Check Norovirus against the predeclared branch; do not treat failure as an implementation error unless diagnostics indicate one."
- `/proj/paper/docs/plans/2026-04-30-wave3-p6-biological-nulls.md:267-279`: Add `\label{para:p6_biological_nulls}` immediately after the new P6 paragraph heading, since Ch5 references it.
- `/proj/paper/docs/plans/2026-04-30-wave3-p6-biological-nulls.md:271-275`: Require the Ch4 paragraph to report denominators for any skipped pathogen-null pairs and to distinguish unadjusted per-pathogen p<0.05 counts from Stouffer global summaries.

## Wave 4 Ordering Recommendation

Run **Tier 2 features-only LOPO at n~30** first, then **pilot 3 Layer A curation**, then **defense rehearsal / 6-agent review**, then **EVE/PLM site-effect**. If P6 fails completely, skip Tier 2 expansion until the dissertation prose is reframed around negative/bounded findings.

## Defense-Readiness Risk Re-Scoring

**Medium.** P6 meaningfully addresses the largest remaining committee objection if it is executed and reported with the modifications above. Risk stays medium, not low, because Wave 2 produced 0/12 callable under the pre-registered abstention rule and because P6 can only defend descriptive signal, not prospective deployability.
