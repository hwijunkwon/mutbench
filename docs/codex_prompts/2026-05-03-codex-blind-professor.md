# Codex blind professor evaluation — fresh independent check

Execute the audit task NOW. Read-only. Write only the final report.

You are an independent reviewer running a fresh PhD dissertation defense
simulation. **No prior cycle context.** Do not consult any review reports
under `paper/dissertation/review/` — read only the active manuscript.

## Active build manuscript only

- `/proj/paper/paper/dissertation/front_en/abstract.tex`
- `/proj/paper/paper/dissertation/chapters_en/ch1_introduction.tex`
- `/proj/paper/paper/dissertation/chapters_en/ch3_methods.tex`
- `/proj/paper/paper/dissertation/chapters_en/ch4_results.tex`
- `/proj/paper/paper/dissertation/chapters_en/ch5_discussion.tex`

Orphan files (NOT in build, do not cite as evidence): `chapters_en/ch2_background.tex`,
`chapters_en/ch5_adapt.tex`, `chapters_en/ch6_conclusion.tex` (does not exist),
all `chapters/*.tex` (Korean mirror, out of build per v206 policy).

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
B. 관련 연구 충실도
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

Do NOT use any prior score or cycle context. Read the manuscript files
above as if you have never seen them. Form your own judgment.

## Output

Write report to:
  `/proj/paper/paper/dissertation/review/2026-05-03/codex_blind_professor.md`

Structure:
1. 10×10 score matrix
2. Item means + total
3. Per-item rationale for any item < 8.0
4. Gate verdict (PASS/FAIL)
5. **One paragraph at end**: "How does this fresh evaluation differ from
   what an iteratively-tuned committee might conclude?" — your meta-comment
   on whether the score reflects the manuscript independently or is
   sensitive to expectation framing.
6. End with one-line headline:
   `RESULT_BLIND: total=<x.x>/10*10 min_item=<x.x> verdict=<PASS|FAIL>`

Length budget: ≤ 2500 words. Do not commit.
