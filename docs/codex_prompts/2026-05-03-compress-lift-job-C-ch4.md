# Compression-with-lift review — Job C: ch4_results

Execute the review NOW. Read-only. Write only the final report.

You are looking for compression opportunities that ALSO improve readability /
defense quality. Ch4 was already partially compressed (audit ledger added,
9 audit paragraphs trimmed) — find what's LEFT to compress beyond that.

## Scope

- `paper/dissertation/chapters_en/ch4_results.tex` (post-compression state, ~970 lines)

## Already done (do not re-recommend)

- 9 audit paragraphs (P1, P2, P3, P5, P6, W4, W5, HBFWS, Cycle 7B) trimmed
- New summary table `tab:audit_ledger` added
- Wave 4 / Wave 5 artefact path lists removed
- HBFWS Bayesian model spec compressed
- Falsification criteria paragraph removed

## Pattern to find

Same as audit ledger pattern: dense prose with parallel items → compact
table + trimmed prose. Lifts score by making evidence findable + reducing
clutter.

Look for:

1. **Other table-izable enumerations** in Ch4 (e.g., per-pathogen
   biological rationales, scoring vs detector best-cell tables)
2. **Long ANOVA Diagnostic Tests block** (line ~475-526): 5 inferential
   frames + LOO sensitivity. Already keep all five lower bounds; check
   if implementation detail can move further into a smaller table or
   shorter prose
3. **Verbose method-restatement in results** (cycle 6 partially handled)
4. **Repeated metric definitions** (MCC, top-10%, enrichment etc.)
5. **Vaccine escape narrative** (line ~937-955) — pipeline notes,
   denominator arithmetic
6. **Cold-start algorithm + pseudocode** — could the algorithm box itself
   be tightened?
7. **HBFWS adaptive comparison + Cycle 7B intro prose** before the
   adaptive_weighting_comparison table

For each candidate:
- File:line range
- What it currently does
- Compression strategy
- Expected page saving
- Expected score impact: lift / neutral / drop
- Risk level

## Expected output

Write report to:
  `/proj/paper/paper/dissertation/review/2026-05-03/compress_lift_jobC.md`

Structure:
1. List of 5-10 candidates
2. Top 3 recommended
3. Sample compressed prose for the #1 candidate (≤ 200 words)
4. End with one-line:
   `RESULT_JOBC: candidates=<n> top3_pages_saved=<n> top3_score_impact=<+x.x|0|-x.x>`

Length budget: ≤ 2200 words. Do not commit.
