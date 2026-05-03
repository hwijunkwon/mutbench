# Execute Job D — ch5 Top 3 compressions

Execute the editing task NOW. Workspace-write OK. Do not commit.

## Required reading

`/proj/paper/paper/dissertation/review/2026-05-03/compress_lift_jobD.md`

The Top 3 candidates listed there:
- D1 Future-work programme / Wave 2-5 repetition
- D2 Limitations prose + limitations table consolidation
- D3 Code/data availability + numerical artifact listing

## Constraints

- **No appendix** (graduation thesis).
- Preserve all numerical values verbatim.
- Preserve all `\label{}`, `\ref{}`, `\cite{}` keys.
- Modify ONLY `chapters_en/ch5_discussion.tex`.
- Preserve `tab:future_roadmap`, `tab:defense_map`, `tab:layer_a_provenance`,
  `tab:audit_ledger` references.

## Task

Apply the three Top compressions described in the report. For D2, if a
limitations table doesn't exist yet in Ch5, create one (with `\small`,
≤ 5 columns: Limitation | Implication | Mitigation in this dissertation |
Where addressed); migrate scattered limitation paragraphs into the table
+ a brief introductory paragraph.

After all edits:
- Run `bash paper/dissertation/build.sh digital`
- Report final page count, pages saved (target: -2.6 from 234pp), errors.

Do not modify other chapters.

## Output

`RESULT_EXEC_D: pages_before=234 pages_after=<N> saved=<N> errors=<N>`

Do not commit.
