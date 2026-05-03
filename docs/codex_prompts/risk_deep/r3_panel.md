# Risk-3 Deep panel 2 — "panel-size threshold" wording across all chapters

Execute the analysis NOW. Read-only. Do not commit.

## Context

Risk-3 flagged "formalising the panel-size threshold (~20-30 pathogens, Bolker rule-of-thumb) at which adaptive method selection becomes possible" as overstrong (1 unsupported claim). The body supports "n=11 below Bolker >=20-30 stable random-effects regime" but does not prove "20-30 will be sufficient."

## Inputs

- `paper/dissertation/front_en/abstract.tex`
- `paper/dissertation/chapters_en/ch1_introduction.tex`
- `paper/dissertation/chapters_en/ch3_methods.tex`
- `paper/dissertation/chapters_en/ch4_results.tex`
- `paper/dissertation/chapters_en/ch5_discussion.tex`

## Task

1. Find every occurrence of "20-30", "20--30", "Bolker", "panel size", "rule of thumb", "20 to 30", "twenty", "Bolker minimum".
2. Quote each occurrence.
3. Classify each: claim is bound (n=11 < 20-30 regime) or claim is overstrong (20-30 will suffice).
4. Provide canonical wording that satisfies Risk-1 guardrails: "Always pair 'not learnable' with 'at n=11, under tested regime'" + "Treat 20-30 as design target/rule-of-thumb, not phase transition."
5. Recommend per-occurrence edits.

## Output

`paper/dissertation/review/2026-05-03/r3_deep_panel.md`

End with: `RESULT_R3_DEEP_PANEL: occurrences=<n> overstrong=<n> canonical="<one phrase>"`

Length: ≤ 1500 words.
