# Cycle 4 Perspective A — Falsifiability stress test

Execute the audit task NOW. Read-only. Write only the final report.

You are an independent reviewer applying Popperian falsifiability standards
to a PhD dissertation. Active English build files are at:
`/proj/paper/paper/dissertation/chapters_en/{ch1, ch3, ch4, ch5_discussion}.tex`
plus `/proj/paper/paper/dissertation/front_en/abstract.tex`.

Use neutral terminology. Reference review reports under
`/proj/paper/paper/dissertation/review/2026-04-30/wave{1,2,3,4}/` and
`/proj/paper/paper/dissertation/review/2026-05-02/wave5_replacement/`
for technical detail rather than re-quoting it.

## Task

For each of the dissertation's THREE core contributions, evaluate:

1. **Is the contribution stated as a falsifiable claim?** A falsifiable
   claim names empirically testable conditions under which it would be
   declared false.
2. **Does the manuscript specify the falsification conditions explicitly?**
3. **Is the falsification test feasible with current resources or reasonable
   future resources?**

Three contributions to evaluate:

- **C1**: 12-pathogen literature-curated benchmark with $\omega^2_{\text{interaction}}=0.296$
- **C2**: 1023-subset Shapley audit ranking the historical 4-core at 87/1023
  and identifying a slightly better 3-core variant
- **C3**: HIV-1 search-space-reduction with 7.19x retrospective enrichment

Also evaluate FIVE specific decision points:

- **Wave 5 Branch C** (label-provenance non-equivalence)
- **Wave 4 callability rule** (0/12 abstention)
- **Wave 1 P1 HARD STOP** (per-pathogen significance gradient)
- **Wave 3 P6 four-null robustness** (4 pathogens significant under all 4 nulls)
- **Pre-registration drift** (do pre-declared branches in Wave 1-5 plans
  match the branches actually fired in the result reports?)

For the pre-registration drift item, scan
`/proj/paper/docs/plans/2026-04-30-*.md` and `/proj/paper/docs/plans/2026-05-01-*.md`
versus the matching `/proj/paper/paper/dissertation/review/2026-04-30/wave*/*.md`
result reports. Tabulate plan-vs-result branch agreement.

## Output

Write report to:
  `/proj/paper/paper/dissertation/review/2026-05-02/cycle4_A_falsifiability.md`

Structure:
1. Per-claim falsifiability status (PASS/WEAK/MISSING) for each of C1/C2/C3
   plus the five decision points, with file:line evidence
2. Pre-registration drift table (Wave 1-5 plan branch -> declared in plan -> fired in result)
3. Recommended manuscript additions for any MISSING/WEAK falsification spec
   (concrete suggested sentences, ≤80 words each)
4. Summary verdict: high / medium / low falsifiability hygiene overall
5. End with a one-line headline:
   `RESULT_A: hygiene=<high|medium|low> missing_specs=<n> drift_count=<n>`

Length budget: ≤ 2500 words. Do not commit.
