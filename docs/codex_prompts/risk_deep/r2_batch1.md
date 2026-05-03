# Risk-2 Deep batch 1 — Ch1+Ch2 safe trims (blocks #1, #4, #5, #6)

Execute the analysis NOW. Read-only. Do not commit.

## Context

Risk-2 (`paper/dissertation/review/2026-05-03/risk2_compression_analysis.md`) flagged 21 compression candidates; this deep analysis covers blocks #1, #4, #5, #6 (Ch1 background + Ch2 DBSCAN/PLM/feature survey). All are verdict=safe.

## Input files (read fully)

- `paper/dissertation/chapters_en/ch1_introduction.tex` (lines 5–55)
- `paper/dissertation/chapters_en/ch2_background.tex` (lines 59–87, 124–166, 187–209)
- `paper/dissertation/review/2026-05-03/risk2_compression_analysis.md` (overall plan)
- `paper/dissertation/review/2026-05-03/risk1_framing_analysis.md` (guardrails)

## Task: produce a LINE-LEVEL compression plan for each of the 4 blocks

For EACH block:

1. Quote the current first/last line of the prose block (verbatim).
2. List every load-bearing claim the prose currently makes (citations preserved).
3. Provide a **concrete replacement draft** (≤ 1/3 of the original word count).
4. Confirm every citation key (\cite{...}) is preserved.
5. Compute exact line savings (current_lines → new_lines).
6. Flag any side-effects on cross-references (\ref{}, \label{}).

## Output

`paper/dissertation/review/2026-05-03/r2_deep_batch1.md`

Structure: 4 sections (#1, #4, #5, #6) each with the 6 fields above.

End with: `RESULT_R2_DEEP_BATCH1: blocks=4 line_savings=<n>`

Length budget: ≤ 2500 words.
