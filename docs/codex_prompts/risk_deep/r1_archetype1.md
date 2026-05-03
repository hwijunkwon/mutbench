# Risk-1 Deep archetype 1 — Statistician committee member rebuttal expansion

Execute the analysis NOW. Read-only. Do not commit.

## Context

Risk-1 produced a guarded verdict with 3 short rebuttal sketches. The user wants finer-granularity analysis: extend the **statistician** rebuttal to a defense-script (3 follow-up questions, with anticipated probes and best response).

## Inputs

- `paper/dissertation/review/2026-05-03/risk1_framing_analysis.md` (initial sketch)
- `paper/dissertation/chapters_en/ch3_methods.tex` Statistical Design section (lines 721–854)
- `paper/dissertation/chapters_en/ch4_results.tex` ANOVA + LOPO + Friedman + Nemenyi sections (lines 352–538)

## Statistician role

Specialty: statistical genetics / cluster bootstrap / mixed effects. Strict on: power, anti-conservative bootstrap, multiple comparison, post-hoc null calibration, ad-hoc thresholds.

## Task

Produce a defense-script with these elements:

### 1. Opening question (1 sentence) — already in risk1
Statistician: "You have 11 pathogen clusters. You cannot prove non-learnability or a panel-size threshold from 11 units; the cluster bootstrap and random-effects interpretation are underpowered or anti-conservative."

### 2. Three follow-up questions (anticipated)

For EACH:
- Quote the question
- Why this question is hard
- Best 2–3 sentence rebuttal anchored in dissertation evidence (cite ch3/ch4 line numbers)
- Backup citation if the question goes deeper (Bolker GLMM, MacKinnon-Roodman cluster bootstrap, Cohen ω² thresholds, etc.)

### 3. Trap questions (2 questions where the dissertation is genuinely weak)

For each: quote, why weak, best honest acknowledgement + scope-narrowing response.

### 4. One-line summary of the statistician's most likely deduction (in points)

## Output

`paper/dissertation/review/2026-05-03/r1_deep_statistician.md`

End with: `RESULT_R1_DEEP_STAT: anticipated_score=<x.x>/10 weak_count=<n> rebuttable_count=<n>`

Length: ≤ 2000 words.
