# Phase 4 Professor Committee — Single Professor Evaluation

Execute the evaluation NOW. Read-only. Do not commit. Do not ask for confirmation.

You are **Professor 9**: Statistical genetics, strictness = medium.
Primary focus items: C E.

This is an **independent blind evaluation** — do not consult any prior cycle's
review reports (no `paper/dissertation/review/2026-05-03/*.md` reads).

## Scope (active build only — 215 pages)

- `paper/dissertation/front_en/abstract.tex`
- `paper/dissertation/chapters_en/ch1_introduction.tex` (which inputs `ch2_background.tex` line 54)
- `paper/dissertation/chapters_en/ch2_background.tex`
- `paper/dissertation/chapters_en/ch3_methods.tex`
- `paper/dissertation/chapters_en/ch4_results.tex`
- `paper/dissertation/chapters_en/ch5_discussion.tex`

Orphan files (NOT in build, do not cite): `back/abstract_en.tex`,
`chapters_en/ch5_adapt.tex`, `chapters_en/ch6_conclusion.tex`,
`chapters/*.tex` (Korean originals).

## Recent state (post-v219)

- ω² = 0.296 (cluster-bootstrap CI [0.201, 0.346])
- Friedman χ² = 7.69, p = 0.990
- LOPO 0/11 match
- Vaccine-escape: HIV-1 7.19× (primary anchor), H3N2 9.36× (self-consistency), SARS-CoV-2 7.63× (exploratory)
- HBFWS p = 0.78 (negative)
- Cycle 7B: 6 paradigms all fail (smallest p = 0.56)
- Wave 4: 8/12 positive, p = 0.368
- Wave 5: Layer A' MCC = -0.055, sign-opposite (bounded sensitivity check)

## Task

Score **all 10 items A-J** on a 0-10 scale. Apply your discipline's
strictness with extra rigor on your focus items; for items outside your
focus, score from your discipline's perspective without lowering rigor.

Items:
- **A. 문제 정의** (problem statement)
- **B. 관련 연구** (related work)
- **C. 방법론** (methodology)
- **D. 실험 규모** (scope/scale)
- **E. 결과 해석** (interpretation)
- **F. 기여 독창성** (novelty/contribution)
- **G. 실용 가치** (practical value)
- **H. 서술 명확성** (clarity)
- **I. 한계 인식** (limitations awareness)
- **J. 완성도** (overall maturity)

Grading anchors:
- 10 = perfect
- 9 = excellent with only minor improvements
- 8 = good with concrete deductions
- 7 = acceptable with clear weaknesses
- 6 = weak, revision-needed
- <6 = serious deficiency

## Output

Write your report to:
`paper/dissertation/review/2026-05-03/professor_v6_prof09.md`

Structure (YAML-like for easy aggregation):

```
# Professor 9: Statistical genetics (strictness=medium)

## Scores
A: <0-10>
B: <0-10>
C: <0-10>
D: <0-10>
E: <0-10>
F: <0-10>
G: <0-10>
H: <0-10>
I: <0-10>
J: <0-10>
total: <sum/100>

## Rationale (≤3 sentences each item)
A: ...
B: ...
... (J)

## Critical concerns (if any item < 6)
...

## Strongest single deduction
... (one-line: which item, why, what fix)

RESULT_PROF_V6_09: total=<x.x>/100 min_item=<x.x>(<item>) max_item=<x.x>(<item>)
```

Length budget: ≤ 1500 words.
