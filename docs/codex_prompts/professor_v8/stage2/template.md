# Phase 4 Stage 2 — Professor Score Aggregator

Execute the evaluation NOW. Read-only. Do not commit. Do not ask for confirmation.

You are **Professor {N}**: {ROLE}, strictness = {STRICTNESS}.
Primary focus items: {FOCUS_ITEMS}.

This is an **independent blind evaluation**. **DO** consult the Stage 1 chapter
reports listed below (they are chapter-deep evaluations from neutral
chapter-evaluators); **DO NOT** consult any prior cycle's score reports
(no v6/v7 outputs).

## Stage 1 chapter reports (must read all 5)

- `paper/dissertation/review/2026-05-03/professor_v8_stage1_abstract_ch1.md`
- `paper/dissertation/review/2026-05-03/professor_v8_stage1_ch2.md`
- `paper/dissertation/review/2026-05-03/professor_v8_stage1_ch3.md`
- `paper/dissertation/review/2026-05-03/professor_v8_stage1_ch4.md`
- `paper/dissertation/review/2026-05-03/professor_v8_stage1_ch5.md`

## Your specialty deep-read chapter

After reading the 5 Stage 1 reports, **directly re-read** these chapters yourself
because they fall in your area of specialty:

{SPECIALTY_CHAPTERS}

## Manuscript scope (197pp)

Active build:
- `paper/dissertation/front_en/abstract.tex`
- `paper/dissertation/chapters_en/ch1_introduction.tex`
- `paper/dissertation/chapters_en/ch2_background.tex`
- `paper/dissertation/chapters_en/ch3_methods.tex`
- `paper/dissertation/chapters_en/ch4_results.tex`
- `paper/dissertation/chapters_en/ch5_discussion.tex`

## Recent state (post-triage-reframe + Layer C re-anchoring)

- 215pp -> 197pp via 6-step compression
- Wet-lab triage framing as primary contribution; deployment refused
- Abstract evidence ledger row 1: Layer C 6/11 pathogens (650 positions, MCC 0.139-0.322) + HIV-1 7.19x vaccine escape (82% disjoint, 37 of 45 novel)
- ch5 sec:vaccine_escape retitled "Wet-Lab Validation: Layer C DMS and Vaccine Escape"
- Cycle 7B / HBFWS / LOPO 0/11 paired with "at n=11, under tested regime"
- omega^2 = 0.296 (cluster-bootstrap CI [0.201, 0.346])
- Friedman chi^2 = 7.69, p = 0.990
- ANOVA 5-frame triangulation narrative restored

## Task

Score **all 10 items A-J** on a 0-10 scale. Apply discipline strictness.
Use Stage 1 chapter reports as primary evidence; verify in your specialty
chapter directly. Stage 1 reports flag many hidden issues that bulk-read
panels miss; weigh those appropriately.

Items:
- A. problem statement
- B. related work
- C. methodology
- D. scale (panel size, breadth)
- E. interpretation (results reading)
- F. novelty/contribution
- G. practical value (wet-lab triage utility)
- H. clarity (writing)
- I. limitations awareness
- J. overall maturity

Grading anchors: 10 perfect; 9 excellent minor improvements; 8 good with
deductions; 7 acceptable; 6 weak revision-needed; <6 serious deficiency.

## Output

Write your report to:
`paper/dissertation/review/2026-05-03/professor_v8_prof{N_PADDED}.md`

Structure:

```
# Professor {N}: {ROLE} (strictness={STRICTNESS})

## Stage 1 reports consulted
- abstract_ch1: <one-line summary of key takeaway>
- ch2: <takeaway>
- ch3: <takeaway>
- ch4: <takeaway>
- ch5: <takeaway>

## Specialty deep-read
- <chapter>: <what you noticed beyond Stage 1 report>

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

## Rationale (per item, 2-3 sentences each, citing Stage 1 evidence + your specialty observations)

## Strongest single deduction
one-line: which item, why, what fix

RESULT_PROF_V8_{N_PADDED}: total=<x.x>/100 min_item=<x.x>(<item>) max_item=<x.x>(<item>) stage1_evidence_used=<count>
```

Length budget: <= 2000 words.
