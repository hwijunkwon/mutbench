# Phase 4 blind professor — post-compression confirmation

Execute the audit task NOW. Read-only. Write only the final report.

You are an independent reviewer running a fresh PhD dissertation defense
simulation. **No prior cycle context.** Do not consult any review reports
under `paper/dissertation/review/`.

## Active build

- `front_en/abstract.tex`
- `chapters_en/ch1_introduction.tex` (which inputs `ch2_background.tex` at line 54)
- `chapters_en/ch2_background.tex` (active via ch1 input)
- `chapters_en/ch3_methods.tex`
- `chapters_en/ch4_results.tex`
- `chapters_en/ch5_discussion.tex`

The active English build at PDF render produces `thesis_en.pdf` 234 pages
(previously 241; -7 pages from in-place compression: audit-ledger summary
table + audit paragraph trims + 5-frame robustness consolidation).

Orphan: `chapters_en/ch5_adapt.tex`. `ch6_conclusion.tex` does not exist.

## Task

Apply the same 10-professor 9-item rubric used in
`paper/dissertation/review/2026-05-03/codex_blind_professor_v2.md` (which
gave total 80.9/100 on the previous, 241-page, version).

10 professors with mixed strictness as in v2 (Chair/Advisor/Statistics-strict/
ComputationalBiology/Virology/VEP-strictest/Benchmark/Practice-strict/
StatisticalGenetics/StructuralBiology).

9 items: A 문제정의, B 관련연구, C 방법론, D 실험규모, E 결과해석,
F 독창성, G 실용가치, H 명확성, I 한계, J 완성도. Score 0-10 each.

Pass: total ≥ 80, no item < 6, no Critical.

## Required: read manuscript freshly

Score the post-compression manuscript independently. Do NOT consult v2 score.
After scoring, **explicitly compare to v2's 80.9**: how much did the
compression help/hurt? Per-axis delta. The compression added one Robustness
Audit Ledger summary table (`tab:audit_ledger`) in Ch4 and trimmed the
5-frame robustness restatement in Ch5; everything else is preserved.

## Output

Write report to:
  `/proj/paper/paper/dissertation/review/2026-05-03/codex_blind_professor_v3.md`

Structure:
1. 10×10 score matrix
2. Item means + total
3. Per-item rationale for items < 8.0
4. Gate verdict
5. Per-item delta from v2 80.9 (axis lift/drop, 1-line each)
6. Net delta and verdict on whether compression hurt/helped/neutral
7. End with one-line:
   `RESULT_BLIND_V3: total=<x.x>/100 min_item=<x.x> verdict=<PASS|FAIL> delta_from_v2=<+x.x|-x.x>`

Length budget: ≤ 2500 words. Do not commit.
