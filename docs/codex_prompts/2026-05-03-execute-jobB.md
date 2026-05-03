# Execute Job B — ch2 + ch3 Top 3 compressions

Execute the editing task NOW. Workspace-write OK. Do not commit.

## Required reading

`/proj/paper/paper/dissertation/review/2026-05-03/compress_lift_jobB.md`

The Top 3 candidates listed there:
1. ANOVA robustness and diagnostic tests block (ch3:820-825, 855-862)
2. Detector families + parameter variants (ch3:622-728)
3. Layer A/B/C definitions and Layer A heterogeneity (ch3:190-207, 272-313)

## Constraints

- **No appendix** (graduation thesis).
- Preserve all numerical values verbatim.
- Preserve all `\label{}`, `\ref{}`, `\cite{}` keys.
- Modify ONLY `chapters_en/ch2_background.tex` and `chapters_en/ch3_methods.tex`.
- For B1 (ANOVA robustness), if the canonical version lives in Ch4
  (`ch4:475-498` ANOVA Diagnostic Tests block), keep ch4 as canonical and
  trim ch3 with cross-reference. Or vice versa. Choose whichever already
  has the most detailed treatment, then trim the other.

## Task

Apply the three Top compressions described in the report.

After all edits:
- Run `bash paper/dissertation/build.sh digital`
- Report final page count, pages saved (target: -2.5 from 234pp), errors.

Do not modify other chapters.

## Output

`RESULT_EXEC_B: pages_before=234 pages_after=<N> saved=<N> errors=<N>`

Do not commit.
