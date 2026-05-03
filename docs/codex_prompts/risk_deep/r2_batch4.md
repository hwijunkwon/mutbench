# Risk-2 Deep batch 4 — Cold-Start + Cycle 7B + Subset/Lattice (blocks #14, #18, #19)

Execute the analysis NOW. Read-only. Do not commit.

## Context

The largest single compression target: block #14 (Cold-Start algorithm + audit ledger prose, 188→105–115 lines, ~6pp savings) + #18 (Cycle 7B six paradigms, 28→8 lines, ~3pp savings) + #19 (subset/lattice/Shapley, 39→17 lines, ~1.5pp savings).

These are the heart of the "we tried adaptive selection and it failed" prose narrative that the wet-lab triage reframe absorbs into the audit ledger table.

## Input files (read fully)

- `paper/dissertation/chapters_en/ch4_results.tex` (lines 706–893 Cold-Start + audit + ledger; 863–890 Cycle 7B; 795–833 subset/lattice)
- `paper/dissertation/review/2026-05-03/risk2_compression_analysis.md`
- `paper/dissertation/review/2026-05-03/risk1_framing_analysis.md` (guardrails: never let LOPO 0/11 stand alone; pair "not learnable" with "at n=11")

## Task: produce 3 line-level plans

For each block:

1. Identify the existing audit ledger row(s) that already preserve the numerics.
2. List any narrative content that should remain (interpretation, boundary statements).
3. Provide concrete replacement draft (≤ 60% of original for #14 guarded; ≤ 30% for #18 guarded; ≤ 50% for #19 guarded).
4. Verify Algorithm 1 reference + Table refs (audit_ledger, cold_start_baseline_progression, nested_lopo_4core, subset_selection_top10) all preserved.
5. Critical preservation: ω² 0.296 cluster CI, 4-core MCC 0.081 vs full-10 0.070, 1023 lattice rank 87, 3-core rank 27, p2 decision curve 41 random baseline, P1 6/12 / 4/12 / 7/12 at-or-below-mean counts, P5 0/12 callable, HBFWS p=0.78, Cycle 7B 6 paradigms p≥0.56.
6. Compute exact line savings per block.

## Output

`paper/dissertation/review/2026-05-03/r2_deep_batch4.md`

End with: `RESULT_R2_DEEP_BATCH4: blocks=3 line_savings=<n> ledger_rows_added=<n>`

Length budget: ≤ 3000 words.
