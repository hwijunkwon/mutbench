# Phase 4 blind v5 — post-deep-audit-fix confirmation

Execute the audit task NOW. Read-only. Write only the final report.

You are an independent reviewer running a fresh PhD dissertation defense
simulation. **No prior cycle context.** Do not consult any review reports.

## Active build (215 pp)

- `front_en/abstract.tex`
- `chapters_en/ch1_introduction.tex` (which inputs `ch2_background.tex` line 54)
- `chapters_en/ch2_background.tex`
- `chapters_en/ch3_methods.tex`
- `chapters_en/ch4_results.tex`
- `chapters_en/ch5_discussion.tex`

Previous reference: blind v4 = 81.85/100 on 215pp (post-Top-12 compression
but BEFORE deep audit fixes).

## What just changed

A 5-chapter deep audit (10-page chunks) flagged 1 Critical + 22 Major.
Critical + 6 Major now fixed in-place:

- **Critical D614G**: ch4 said "excluded from Layer A/B"; CSV/feature_matrix
  show D614G IS in Layer A as a "functional" tag. Fixed: ch4 now says D614G
  is retained as a documented functional substitution per Korber 2020.
- **M1 ω² CI**: manuscript [0.195, 0.333] → current archived
  [0.201, 0.346] (matches `cluster_bootstrap_omega_summary.csv`).
- **M2 HIV-1 Layer A**: ch5 provenance table notes 26 in
  `layer_a_tags.csv` vs 23 mapped to gp120 in feature_matrix.
- **M3 Stage 1 region**: ch4's 439 AA → 417 AA (matches ch3's 1251 nt = 417 codons).
- **M4 DMS Layer C counts**: ch3 table aligned to `layer_c_evaluation.csv`.
- **M5 "point substitutions only"** softened to gap-aware single-position scoring.
- **M6 "20-80 positions"** range adjusted to match actual detector outputs.

All numerical headlines unchanged: ω² = 0.296, 0/12 callable, Branch C with
MCC = -0.055, rank 87/27, p = 0.78 HBFWS, etc.

## Task

Apply the same 10-professor 9-item rubric. Score the post-audit-fix
manuscript blind. Compare to v4 81.85.

## Output

Write report to:
  `paper/dissertation/review/2026-05-03/codex_blind_professor_v5.md`

Structure:
1. 10×10 score matrix
2. Item means + total
3. Per-item rationale for items < 8.0
4. Gate verdict
5. Per-item delta from v4 81.85
6. Net delta and verdict on whether the audit fixes hurt/helped/neutral
7. End with one-line:
   `RESULT_BLIND_V5: total=<x.x>/100 min_item=<x.x> verdict=<PASS|FAIL> delta_from_v4=<+x.x|-x.x>`

Length budget: ≤ 2500 words. Do not commit.
