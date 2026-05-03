# Risk-3 Deep — Concrete revised abstract draft

Execute the writing task NOW. Read-only on the source files. Output a draft only (do not edit `abstract.tex`).

## Context

Risk-3 provided suggested edits but not a clean unified replacement. Synthesize one final draft.

## Inputs

- `paper/dissertation/front_en/abstract.tex` (current)
- `paper/dissertation/review/2026-05-03/risk3_abstract_analysis.md` (suggested edits + 4-row ledger)
- `paper/dissertation/review/2026-05-03/risk1_framing_analysis.md` (10 guardrails)

## Task

Produce a complete replacement abstract that:

1. Leads with wet-lab triage value (search-space reduction quantified).
2. Has the 4-row evidence ledger as suggested by Risk-3.
3. Preserves every numerical anchor from Risk-3 anchor list (HIV-1 7.19× / p_adj=2.5e-16 / 82% disjoint / 37 of 45 novel; H3N2 9.36×; SARS 7.63× exploratory; ω²=0.296 CI [0.201, 0.346]; LOPO 0/11; HBFWS p=0.78; Cycle 7B 6 paradigms; Wave 5 MCC=-0.055; 8,580 evaluations; 11 pathogens).
4. Avoids the "20-30 will suffice" overstrong claim.
5. Pairs all "not learnable" claims with "at n=11, under tested regime."
6. Includes Bolker rule-of-thumb as design target, not phase transition.
7. Stays within current abstract length budget (~34 lines body + ledger).

## Output

`paper/dissertation/review/2026-05-03/r3_deep_abstract_draft.md`

Structure:
1. The complete replacement abstract.tex content (LaTeX-ready, including `\begin{table}` ledger).
2. Word-by-word audit confirming all required anchors are present.
3. Length comparison (current vs new).

End with: `RESULT_R3_DEEP_DRAFT: anchors=<n>/<n> length_change=<+/-N lines> ledger_rows=4`

Length: ≤ 2500 words.
