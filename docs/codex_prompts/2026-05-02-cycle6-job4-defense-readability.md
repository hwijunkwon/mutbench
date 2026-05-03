# Cycle 6 Job 4 — Defense Readability + Q&A Robustness

Execute the audit task NOW. Read-only. Write only the final report.

You are simulating an oral PhD defense committee evaluating verbal
comprehension and Q&A robustness. Active English build files at
`/proj/paper/paper/dissertation/chapters_en/`. Use neutral terminology.

This Job covers axis 8 of the cycle 6 design and CONSUMES the outputs of
Jobs 1, 2, 3 to build a Q&A risk map.

## Required reading (consume as input)

- `paper/dissertation/review/2026-05-02/cycle6_job1_content_length.md`
- `paper/dissertation/review/2026-05-02/cycle6_job2_method_data.md`
- `paper/dissertation/review/2026-05-02/cycle6_job3_focus_flow_calibration.md`
- `paper/dissertation/review/2026-05-02/phase4_professor_cycle5.md` (latest score 82.9/100)
- Active build manuscript

## Task: Axis 8 — Defense Readability + Q&A Robustness

Apply Q1-Q6 PLUS additional Q7-Q10 informed by J1/J2/J3 findings.

Q1. Can a committee member understand the one-sentence thesis without
   knowing MutBench internals? Verdict: yes / partly / no. Provide the
   sentence in plain English a non-specialist would understand.
Q2. Can the candidate answer "what is your main contribution?" in three
   ordered bullets (without losing committee attention)?
Q3. Can Ch4 be explained verbally using 3-5 core figures/tables?
   List which 3-5 figures/tables you would pick.
Q4. Are likely objections to Layer A, LOPO, HIV-1, and 11 pathogens
   answered in the main text?
Q5. Are terminology switches (Layer A vs A' vs A'_dms; 3-core/4-core;
   11/12 pathogen) likely to derail Q&A?
Q6. Does the dissertation provide enough "why this matters" language for
   non-specialist committee members?
Q7. Generate 5 most likely defense questions a committee will ask, based on
   J1/J2/J3 findings. For each: estimated answer length (1 sentence /
   1 minute / 5 minutes). Mark any that the user CANNOT answer in the
   estimated length.
Q8. Identify the highest-risk single sentence in the dissertation a
   hostile committee member would attack first. Quote it with file:line.
Q9. Identify the strongest sentence in the dissertation a candidate
   should lead with in the verbal opening. Quote with file:line.
Q10. If you had 2 hours to defend, what 5-page subset of the dissertation
   would you actually present?

## Output

Write report to:
  `/proj/paper/paper/dissertation/review/2026-05-02/cycle6_job4_defense_readability.md`

Structure:
1. Q1-Q10 results table (each row: verdict + 1-2 sentence rationale + cite)
2. The proposed one-sentence thesis (Q1)
3. The 5 likely defense questions (Q7) with answer-length estimates
4. The highest-risk sentence (Q8) and strongest opening sentence (Q9)
5. The 5-page defense subset (Q10) — chapter:section list
6. Recommended manuscript additions (≤80 words each, ≤5 items) that
   would lift defense readability
7. End with one-line headline:
   `RESULT_J4: readability=<strong|medium|weak> q_a_robustness=<strong|medium|weak> top_risk=<short_phrase>`

Length budget: ≤ 3000 words. Do not commit.
