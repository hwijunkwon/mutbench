# Codex blind professor evaluation v2 — corrected orphan classification

Execute the audit task NOW. Read-only. Write only the final report.

You are an independent reviewer running a fresh PhD dissertation defense
simulation. **No prior cycle context.** Do not consult any review reports
under `paper/dissertation/review/` — read only the active manuscript.

## Active build (CORRECTED)

The dissertation builds via `paper/dissertation/thesis_en.tex` which inputs:
- `front_en/abstract.tex`
- `chapters_en/ch1_introduction.tex` — which itself inputs `chapters_en/ch2_background.tex` at line 54 as a "Related Research" section (per v170 macro cut). **`ch2_background.tex` is therefore in the active build, not orphan.**
- `chapters_en/ch3_methods.tex`
- `chapters_en/ch4_results.tex`
- `chapters_en/ch5_discussion.tex`
- `front/abstract_kr.tex`

**Orphan** (NOT in active build, do not cite as evidence):
- `chapters_en/ch5_adapt.tex` (orphan; `ch5_discussion.tex` does not `\input` it)
- `chapters/*.tex` Korean mirror (orphan per v206 policy)

`ch6_conclusion.tex` does not exist.

The active English build at PDF render produces `thesis_en.pdf` 241 pages,
0 errors, 0 undefined refs, 0 multiply-defined.

## Task

Simulate the 10-professor committee from the standard rubric:

| # | Role | Strictness | Focus items |
|---|------|---|---|
| 1 | Chair (bioinformatics) | medium | A, B, F |
| 2 | Advisor (CS) | medium | overall balance |
| 3 | Statistics/ML | strict | C, E, J |
| 4 | Computational biology | medium | D, E |
| 5 | Virology / public health | medium | G, I |
| 6 | VEP/PLM expert | strictest | B, D, F |
| 7 | Benchmark methodology | medium | C, D, J |
| 8 | Practice/field user | strict | A, G, H |
| 9 | Statistical genetics | medium | C, E |
| 10 | Structural biology | medium | E, J |

9-item rubric:

A. 문제 정의 명확성
B. 관련 연구 충실도 (note: Related Research is a section inside Ch1 via the ch2_background input, NOT a separate Ch2)
C. 방법론 타당성
D. 실험 규모/견고성
E. 결과 해석 정확성
F. 기여의 독창성
G. 실용적 가치
H. 서술 명확성
I. 한계 인식/정직성
J. 논문 완성도

Score 0–10 per professor per item. Anchors: 10=perfect, 9=excellent (minor improvements only), 8=good (concrete deductions exist), 7=acceptable with clear weaknesses, 6=weak revision-needed, <6=serious deficiency.

Pass criterion: total ≥ 80/100, no item mean < 6, no unresolved Critical.

## Required: read manuscript freshly

Do NOT use any prior score or cycle context. Read the active manuscript files
(including `ch2_background.tex` since it is in the build via Ch1 input) as if
you have never seen them. Form your own judgment.

## Output

Write report to:
  `/proj/paper/paper/dissertation/review/2026-05-03/codex_blind_professor_v2.md`

Structure:
1. 10×10 score matrix
2. Item means + total
3. Per-item rationale for any item < 8.0
4. Gate verdict (PASS/FAIL)
5. **One paragraph at end**: comparison to v1 blind evaluation (which had
   ch2_background incorrectly labelled as orphan and gave total 77.4) — does
   knowing ch2_background is part of Ch1 change the B (Related work) and
   any related axes? Explicit delta from v1.
6. End with one-line headline:
   `RESULT_BLIND_V2: total=<x.x>/100 min_item=<x.x> verdict=<PASS|FAIL> delta_from_v1=<+x.x|-x.x>`

Length budget: ≤ 2500 words. Do not commit.
