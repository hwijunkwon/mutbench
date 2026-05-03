# Compression-with-lift review — Job A: abstract + ch1

Execute the review NOW. Read-only. Write only the final report.

You are looking for compression opportunities that ALSO improve readability /
defense quality (like the audit ledger that just lifted blind score by +0.6
while cutting 7 pages).

## Scope

- `paper/dissertation/front_en/abstract.tex`
- `paper/dissertation/chapters_en/ch1_introduction.tex`

## Pattern to find

The recently successful pattern: dense prose with multiple parallel items
(e.g., 9 audit paragraphs) → compact table + trimmed prose. This LIFTED
score because it (a) made evidence more findable, (b) reduced repeated
caveats, (c) improved gradeability for committee readers.

Look for the same pattern in your assigned scope:

1. **Table-izable lists**: prose enumerations of N parallel items that
   would render better as a table (audit/contribution/method/dataset/etc.)
2. **Repeated caveats**: same limitation/qualifier appearing multiple times
   in different paragraphs
3. **Long single sentences**: 100+ word sentences that could be split or
   restructured
4. **Footnote-tier content in main text**: file paths, version numbers,
   procedural detail, citations to internal review reports
5. **Redundant cross-references**: paragraph mentioning "as shown in
   Section X, Y, Z" when one suffices
6. **Aspirational framing**: hedging that adds words without precision

For each candidate, give:
- File:line range
- What it currently does (1 sentence)
- Compression strategy (table-ize / consolidate / trim / split / footnote)
- Expected page saving (estimate)
- Expected score impact: **lift / neutral / drop** (with reasoning)
- Risk level: low / medium / high

## Expected output

Write report to:
  `/proj/paper/paper/dissertation/review/2026-05-03/compress_lift_jobA.md`

Structure:
1. List of 5-10 candidates with the fields above
2. Top 3 recommended (highest lift/risk ratio)
3. Sample compressed prose for the #1 candidate (≤ 200 words showing
   what the after-state looks like)
4. End with one-line:
   `RESULT_JOBA: candidates=<n> top3_pages_saved=<n> top3_score_impact=<+x.x|0|-x.x>`

Length budget: ≤ 2200 words. Do not commit. Do not modify any source file.
