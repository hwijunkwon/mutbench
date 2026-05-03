# Cycle 4 Perspective D — Counterfactual null sanity

Execute the audit task NOW. Read-only. Write only the final report. You may
read CSVs and run small calculations using stdlib + numpy + scipy + pandas
if needed. No network, no plotting. Do not modify input data.

## Task

Evaluate whether the dissertation includes a counterfactual-null sanity
check on the headline interaction effect $\omega^2 = 0.296$. Specifically:

1. Does the manuscript test what $\omega^2$ would be if the position-level
   labels were randomly shuffled (with prevalence preserved) instead of
   literature-curated?
2. Does it test what would happen if the score values were shuffled while
   keeping labels fixed?
3. Does it test what would happen if the pathogen identities were shuffled
   across the same 8,580 evaluation cells?
4. If any of these are missing, can you compute a quick sanity estimate
   from existing CSVs in `/proj/paper/results/mutbench/feature_analysis/`
   and `/proj/paper/results/mutbench/codex_wave1/`?

The relevant existing tests in the manuscript are P1 (four nulls including
local-burden-preserving) and P6 (four structural-explicit nulls). Read
`/proj/paper/paper/dissertation/review/2026-04-30/wave1/p1_null_calibration.md`
and `/proj/paper/paper/dissertation/review/2026-04-30/wave3/p6_biological_nulls.md`
to see what's already covered.

The DIFFERENCE between existing nulls and counterfactual-null:
- Existing nulls: shuffle scores or labels per pathogen, recompute MCC
- Counterfactual-null asked here: shuffle the entire LABEL ASSIGNMENT
  procedure (i.e., what if Layer A were drawn from a random subset of
  positions matching the prevalence rate), then re-run the full
  scoring x pathogen ANOVA. Does $\omega^2$ stay near 0.296 or collapse?

If the manuscript DOES NOT have this check, recommend a small
sensitivity analysis the user could run in <30 minutes from existing CSVs
without changing data.

## Output

Write report to:
  `/proj/paper/paper/dissertation/review/2026-05-02/cycle4_D_counterfactual.md`

Structure:
1. Coverage table: counterfactual-null variant -> covered / partially
   covered / missing (with file:line of nearest existing analog)
2. Estimated risk if missing: would the headline $\omega^2 = 0.296$
   plausibly survive the missing test?
3. Smallest sensitivity-analysis script the user could add (Python
   pseudocode, ≤ 30 lines), using only existing CSVs.
4. End with a one-line headline:
   `RESULT_D: covered=<n>/3 missing_risk=<low|medium|high>`

Length budget: ≤ 2200 words. Do not commit.
