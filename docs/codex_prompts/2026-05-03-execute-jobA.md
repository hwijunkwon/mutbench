# Execute Job A — abstract + ch1 Top 3 compressions

Execute the editing task NOW. Workspace-write OK. Do not commit.

## Required reading

`/proj/paper/paper/dissertation/review/2026-05-03/compress_lift_jobA.md`

The Top 3 candidates listed there:
1. Abstract evidence ledger
2. Contribution 3 validation ledger
3. Panel-scope ledger

## Constraints

- **No appendix** (graduation thesis).
- Preserve all numerical values verbatim (ω², MCC, p-values, percentages, ranks).
- Preserve all `\label{}`, `\ref{}`, `\cite{}` keys; do not break the build.
- Modify ONLY `front_en/abstract.tex` and `chapters_en/ch1_introduction.tex`.

## Task

Apply the three Top compressions described in the report. For each:

1. Read the candidate's "Compression strategy" and "Sample compressed prose".
2. Apply the compression in-place.
3. If the strategy is "table-ize", create a new compact table inside the
   relevant section (NOT in an appendix). Use `\small` and ≤ 5 columns.
4. If the strategy is "consolidate", trim repeated content and add cross-
   references to the canonical version.
5. If the strategy is "trim", shorten verbose phrasing without losing numbers.

After all edits:
- Run `bash paper/dissertation/build.sh digital`
- Report:
  - Final page count
  - Pages saved (target: -1 to -1.75 from current 234pp)
  - Errors / undefined / multiply-defined counts

Do not modify other chapters.

## Output

After editing, print a one-line summary:
`RESULT_EXEC_A: pages_before=234 pages_after=<N> saved=<N> errors=<N>`

Do not commit.
