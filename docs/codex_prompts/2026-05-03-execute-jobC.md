# Execute Job C — ch4 Top 3 compressions

Execute the editing task NOW. Workspace-write OK. Do not commit.

## Required reading

`/proj/paper/paper/dissertation/review/2026-05-03/compress_lift_jobC.md`

The Top 3 candidates listed there:
- C1 per-pathogen rationales table (ch4:305-325 area)
- C2 ANOVA diagnostics prose trim (ch4:475-526 area)
- C3 vaccine-escape validation consolidation (ch4:937-955 area)

## Constraints

- **No appendix** (graduation thesis).
- Preserve all numerical values verbatim (ω², MCC, p-values, ranks, Shapley).
- Preserve all `\label{}`, `\ref{}`, `\cite{}` keys.
- Modify ONLY `chapters_en/ch4_results.tex`.
- For C2 (ANOVA diagnostics), keep all five lower bounds (0.195, 0.201,
  0.202, 0.242, 0.188) in main text; trim implementation detail (PyMC
  version, Rhat, ESS, sampler settings, hyperprior names).
- For C1, the per-pathogen biology rationales are currently prose in
  Ch4:305-325; convert to a compact table (pathogen | best scoring | reason)
  with `\small`.

## Task

Apply the three Top compressions described in the report.

After all edits:
- Run `bash paper/dissertation/build.sh digital`
- Report final page count, pages saved (target: -2.4 from 234pp), errors.

Do not modify other chapters.

## Output

`RESULT_EXEC_C: pages_before=234 pages_after=<N> saved=<N> errors=<N>`

Do not commit.
