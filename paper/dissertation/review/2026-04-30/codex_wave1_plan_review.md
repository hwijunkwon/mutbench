# Codex Wave 1 Plan Review

## Verdict

**PROCEED WITH MODIFICATIONS.** The Wave 1 scope is correct: P1-P4 are the right method-core audits to run before new curation, expanded panels, or EVE/PLM work. Do not proceed exactly as written, because three details would weaken defense value: P3 should compute formal Shapley weights, P4 should include control scorings if positions are re-materialized, and failure-mode prose branches should be predeclared before results exist.

## Q1. Scope and ordering

**Use P3 -> P2 -> P1 -> P4, with a hard stop after P1.** The slate's ideal order put null calibration first, but the execution plan's order is defensible because P3 and P2 are cheap, exercise the shared scoring code, and produce framing needed for the dissertation text. Moving P1 first is only worth it if compute queue time is uncertain. The plan should state that P3/P2 are preparatory audits, not evidence to preserve if P1 globally fails; if P1 iid fails, stop before P4 and prose insertion.

## Q2. Protocol fidelity

Four separate P1 nulls are acceptable and better than collapsing to only the strongest null, because the gradient from iid to circular/block/local is itself the result. P3 should compute the **formal Shapley value**, not the unweighted mean marginal proxy; the full lattice already provides every subset, so using the exact binomial weighting costs nothing and avoids an avoidable committee objection. P2 isotonic calibration is fine as the primary nonparametric curve. Do not add Platt/beta calibration in Wave 1 unless isotonic looks unstable; a monotone rank audit is the point, not a calibration-model bakeoff.

## Q3. P4 detector-consensus re-run

Option **(a)** is acceptable, but not with only favored scorings. Re-run with `--save-positions` for 4-core, full-10, and at least three predeclared controls: frequency-only, entropy-only, and homoplasy-only. That keeps the compute small while preventing the consensus claim from being accused of score-selection bias. If the code can cheaply emit positions for all 20 scorings, do all 20; otherwise the five-scoring subset is enough for Wave 1 and should be labeled a targeted consensus audit, not the full Stage 3 consensus study.

## Q4. Out-of-scope items

Deferral is correct. Pilot 3 Layer A curation and Tier 2 n=30 LOPO do not belong in Wave 1 because the new-pathogen ground truth is placeholder `-1`; adding them now would mix method-core validation with annotation work. EVE/PLM site-effect is also correctly deferred because it tests incremental feature value, not whether Algorithm 1's current claims survive. The only interaction is interpretive: if P1/P2 show weak signal, Wave 2 should prioritize callability/abstention before expanded curation.

## Q5. Failure-mode handling

The plan should include explicit branches. Handling these reactively invites post hoc prose. Predeclared failure responses make the result usable even when negative: they turn "the method failed" into "the dissertation narrowed the claim correctly." Add the table below to the plan before execution and require Task 6 prose to follow it.

| Failure trigger | Predefined response |
|---|---|
| P1 iid Stouffer p > 0.05 globally | Remove any claim that Algorithm 1 beats a prevalence-preserving null. Reframe as an exploratory ranking heuristic; keep P2/P3 as descriptive diagnostics only; do not add detector-agnostic or search-space-reduction language as a headline. |
| P3 4-core rank > 50/1023 | Replace "non-arbitrary 4-core" with "fixed historical 4-core benchmarked against the lattice." Report the best compact subset and, if a 3-core dominates, mark pLDDT optional or move to a sensitivity appendix. |
| P2 decile slope essentially flat | Drop probability/calibration language. Frame Algorithm 1 as not rank-reliable on current Layer A labels; retain only per-pathogen diagnostic results and any isolated budget gains with confidence intervals. |
| P4 consensus enrichment <= detector mean | Remove "detector-agnostic consensus" framing. State that detector choice remains material; use consensus only as a reproducibility diagnostic, not as a high-confidence candidate set. |

## Q6. Documentation cadence

The existing cadence is almost enough, but add a per-task standalone report directory: `paper/dissertation/review/2026-04-30/wave1/`. NOTES.md is too terse for defense provenance, and the memory file is operational state, not a citable review artifact. Each P1-P4 task should write a 1-2 page Markdown report with command, inputs, outputs, top-line numbers, failure-branch status, and interpretation. Dissertation prose should still wait until all four are stable.

## Q7. Add/remove/strengthen

Add cheap audits that improve defense readiness: P3 should report top-10% and top-20%, exact and +/-10 MCC, precision@20/enrichment, per-pathogen win counts, and formal Shapley for at least MCC plus enrichment. P2 should include monotonic trend tests across deciles and bootstrap CIs for top-vs-bottom separation, not just point prevalence. P1 should use one-sided enrichment p-values as primary and two-sided only as sensitivity, because the scientific question is whether observed signal is above null. P4 should match candidate-list sizes when comparing consensus to detector means and should report candidate count, precision gain, and recall loss together. Remove premature memory updates after P1; write memory only after Wave 1 is complete or explicitly mark it partial.

## Concrete Edits To The Plan

- `docs/plans/2026-04-30-codex-experiment-execution.md:11`: change "update relevant memory file ... after each task" to "append NOTES.md after each task; write memory only at Wave 1 completion, with optional partial status marked clearly."
- `docs/plans/2026-04-30-codex-experiment-execution.md:25`: change P4 description to "from materialized detector callset positions; summary CSV alone is insufficient."
- `docs/plans/2026-04-30-codex-experiment-execution.md:27-31`: add report outputs under `paper/dissertation/review/2026-04-30/wave1/p1_null_calibration.md` through `p4_detector_consensus.md`.
- `docs/plans/2026-04-30-codex-experiment-execution.md:133-135`: replace Shapley text with the formal definition: average each subset-size stratum equally using weight `1 / (n * C(n-1, |S|))`, or equivalently report `sum_k mean_{|S|=k}[v(S U {f}) - v(S)] / n`.
- `docs/plans/2026-04-30-codex-experiment-execution.md:239-264`: remove the unweighted proxy implementation and require a `frozenset -> metric` lookup with formal Shapley weights; include the empty-set value `v(empty)=0`.
- `docs/plans/2026-04-30-codex-experiment-execution.md:300`: expand the P3 sanity check to verify exact agreement with existing 4-of-10 row where protocols overlap, not only within `~0.005`.
- `docs/plans/2026-04-30-codex-experiment-execution.md:403`: add "and top-vs-bottom bootstrap CI excludes zero or is explicitly reported as inconclusive."
- `docs/plans/2026-04-30-codex-experiment-execution.md:438`: make one-sided above-null p-value primary; keep two-sided as sensitivity.
- `docs/plans/2026-04-30-codex-experiment-execution.md:482`: add the full failure-mode table from this review and require stopping before Task 5 if P1 iid fails globally.
- `docs/plans/2026-04-30-codex-experiment-execution.md:505-519`: re-run positions for 4-core, full-10, frequency-only, entropy-only, and homoplasy-only at minimum; all 20 scorings if runtime is acceptable.
- `docs/plans/2026-04-30-codex-experiment-execution.md:527-531`: require matched-size comparisons for consensus enrichment versus detector-specific calls.
- `docs/plans/2026-04-30-codex-experiment-execution.md:558-590`: require prose to follow the predefined failure branch rather than just "honest disclosure."

## Time-To-Defense Risk Score

**Medium.** The scope is right and the compute is plausible, but the current plan has enough protocol shortcuts and underspecified implementation details that it could produce results that are hard to defend. With the edits above, risk drops to low-medium for Wave 1 because negative outcomes become controlled revisions rather than surprises.
