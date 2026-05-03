# Risk-2 Deep batch 5 — Information-type + Biology rationale + Ch5 generalization + Future (blocks #16, #17, #20, #21) + Ch1 rewrite (blocks #2, #3)

Execute the analysis NOW. Read-only. Do not commit.

## Context

Final batch: feature/triage analysis (#16 biology rationale, #17 information-type), Ch5 reframe (#20 cross-pathogen generalization, #21 future directions), and Ch1 rewrite (#2 objectives, #3 contributions — #3 is "keep" but needs reframe to triage).

These are the most reframe-sensitive blocks because they carry the new "wet-lab triage as primary contribution" message.

## Input files (read fully)

- `paper/dissertation/chapters_en/ch4_results.tex` (lines 308–330 biology rationale, 624–700 info-type analysis)
- `paper/dissertation/chapters_en/ch5_discussion.tex` (lines 63–122 cross-pathogen generalization, 260–294 future directions)
- `paper/dissertation/chapters_en/ch1_introduction.tex` (lines 76–157 objectives, 158–195 contributions)
- `paper/dissertation/review/2026-05-03/risk1_framing_analysis.md` (guardrails)
- `paper/dissertation/review/2026-05-03/risk3_abstract_analysis.md` (revised abstract reflects new framing)

## Task: 6 block-level plans

For each block:

1. Identify content that should survive (anchor numerics, key arguments, citations).
2. Provide reframe-aware replacement draft (≤ 60% of original for guarded; #3 contributions stays similar length but with C1=triage as headline).
3. For #20 (Ch5 cross-pathogen generalization): convert "we tried to generalize and failed" tone to "n=11 is below the panel-size threshold for adaptive selection".
4. For #16/#17: connect to wet-lab triage (which features matter for which pathogen, why ESM/SASA non-uniform usefulness supports triage rather than detector).
5. For Ch1 #2/#3: produce a triage-anchored Research Contributions paragraph as the new core.
6. Compute line savings per block.

## Output

`paper/dissertation/review/2026-05-03/r2_deep_batch5.md`

End with: `RESULT_R2_DEEP_BATCH5: blocks=6 line_savings=<n>`

Length budget: ≤ 3500 words.
