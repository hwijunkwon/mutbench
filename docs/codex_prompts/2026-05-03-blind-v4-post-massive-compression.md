# Phase 4 blind v4 — post-massive-compression confirmation

Execute the audit task NOW. Read-only. Write only the final report.

You are an independent reviewer running a fresh PhD dissertation defense
simulation. **No prior cycle context.** Do not consult any review reports
under `paper/dissertation/review/`.

## Active build

- `front_en/abstract.tex`
- `chapters_en/ch1_introduction.tex` (which inputs `ch2_background.tex` at line 54)
- `chapters_en/ch2_background.tex`
- `chapters_en/ch3_methods.tex`
- `chapters_en/ch4_results.tex`
- `chapters_en/ch5_discussion.tex`

The active English build at PDF render produces `thesis_en.pdf` 215 pages.
Previous reference: blind v3 = 81.54/100 on 234pp (post-cycle-4-6 audit
ledger compression but BEFORE Top-12 chapter-level compression).

The Top-12 compressions just applied:
- Abstract evidence ledger table (+ ch1 panel-scope clarification)
- ch2 + ch3 ANOVA robustness consolidation, detector/Layer A definition
  consolidation
- ch4 per-pathogen rationales table, ANOVA diagnostics trim, vaccine-escape
  consolidation
- ch5 future-work + limitations table consolidation, code/data tightening

All numerical results preserved verbatim (ω², MCC, p-values, ranks, Shapley,
Branch C, 0/12 callable, etc.).

## Task

Apply the same 10-professor 9-item rubric. Score the post-compression
manuscript blind. Compare to v3 81.54.

## Required: read manuscript freshly

Score the 215-page manuscript independently. After scoring, **explicitly
compare to v3 81.54**: per-item delta, net delta. The compressions reduced
length 19 pages without removing scientific evidence.

## Output

Write report to:
  `/proj/paper/paper/dissertation/review/2026-05-03/codex_blind_professor_v4.md`

Structure:
1. 10×10 score matrix
2. Item means + total
3. Per-item rationale for items < 8.0
4. Gate verdict
5. Per-item delta from v3 81.54 (axis lift/drop, 1-line each)
6. Net delta and verdict on whether the larger compression hurt/helped/neutral
7. End with one-line:
   `RESULT_BLIND_V4: total=<x.x>/100 min_item=<x.x> verdict=<PASS|FAIL> delta_from_v3=<+x.x|-x.x>`

Length budget: ≤ 2500 words. Do not commit.
