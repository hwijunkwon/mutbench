# Cycle 6 Job 2 — Method + Data appropriateness

Execute the audit task NOW. Read-only. Write only the final report.

You are a method/data appropriateness reviewer. Active English build files at
`/proj/paper/paper/dissertation/chapters_en/`. Use neutral terminology.

This Job covers axes 3 (Method) and 6 (Data) of the cycle 6 design at
`paper/dissertation/review/2026-05-02/cycle6_design_review.md`.

**IMPORTANT**: Do NOT duplicate cycle 4 reports. Cycle 4 F covered statistical
model alternatives, B covered Layer A curation reproducibility, G covered
HIV-1 cherry-pick, H covered generalisation scope. THIS Job evaluates
"appropriateness for the stated claim", not curation reproducibility or
adversarial alternatives. Reference cycle 4 reports rather than re-do them.

## Task: Axis 3 — Method Appropriateness

Apply M1-M7. Verdict (appropriate/qualified/inappropriate or similar) + evidence + rationale.

M1. Is omega/ANOVA the right estimand for "pathogen-dependent optimality"?
   I.e., does omega^2 of scoring x pathogen interaction directly answer the
   research question, or is it a proxy that loses information?
M2. Is Friedman test used for the correct rank-level question?
   The Friedman p=0.990 is reported. What's the question Friedman answers,
   and does the reported result interpret it correctly?
M3. Is LOPO interpreted correctly as corroborative evidence vs standalone proof?
M4. Are bootstrap and cluster-bootstrap units defensible for the uncertainty claim?
   I.e., is "pathogen" the right resampling unit, or should it be "per-evaluation row"?
M5. Do Bayesian checks clarify robustness, or create unnecessary method sprawl?
M6. Would a simpler blocked-permutation result be more defense-useful than
   additional complex models?
M7. Are all analyses reported in Ch4 sufficiently specified in Ch3?

## Task: Axis 6 — Data Appropriateness

Apply D1-D7. Verdict + evidence + rationale.

D1. Is the 11-pathogen panel adequate for the stated RNA-virus single-position scope?
D2. Is the 12-pathogen Stage 3 panel clearly separated from 11-pathogen claims?
D3. Are sequence sources, filters, deduplication, alignment, date scope verifiable from methods?
D4. Is Layer A appropriate for positive labels despite heterogeneous evidence types?
   (Frame as "fit for the claim it supports", not "perfectly curated".)
D5. Are Layer B and Layer C used only for claims they can support?
D6. Is HIV-1 external validation independent and strong enough for the practical anchor role?
D7. Are missing alternative datasets and unavailable validation panels acknowledged?

## Output

Write report to:
  `/proj/paper/paper/dissertation/review/2026-05-02/cycle6_job2_method_data.md`

Structure:
1. Axis 3 results table (7 rows)
2. Axis 6 results table (7 rows)
3. Top 3 cross-axis gaps with concrete prose suggestions (≤80 words each)
4. Verdict summary
5. End with one-line headline:
   `RESULT_J2: method=<strong|medium|weak> data=<strong|medium|weak> top_gap=<short_phrase>`

Length budget: ≤ 2800 words. Do not commit.
