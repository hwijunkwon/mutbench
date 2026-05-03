# Risk-3 Deep — Cross-file claim consistency check

Execute the analysis NOW. Read-only. Do not commit.

## Context

Risk-3 revised abstract draft introduces some new framing language. Verify that ch1 motivation, ch4 results headlines, and ch5 contributions/conclusions use the SAME canonical phrasing for the new triage-first framing.

## Inputs

- `paper/dissertation/review/2026-05-03/r3_deep_abstract_draft.md` (the revised abstract draft, if available; otherwise use risk3_abstract_analysis.md draft)
- `paper/dissertation/chapters_en/ch1_introduction.tex` (Research Motivation, Contributions, Organization)
- `paper/dissertation/chapters_en/ch4_results.tex` (Key findings box at top, Stage 2 summary, Practical Validation section at line 931)
- `paper/dissertation/chapters_en/ch5_discussion.tex` (Practical Implications, Summary of Research Contributions, Concluding Remarks)
- `paper/dissertation/review/2026-05-03/risk1_framing_analysis.md` (10 guardrails)

## Task

1. Identify every "Contribution 1 / 2 / 3" listing across files. Currently the contributions are framed around (1) benchmark, (2) pathogen-dependent interaction, (3) practical search-space reduction. Under triage reframe, C3 (search-space reduction) should be elevated.

2. For each contribution listing in each file, classify:
   - matches new triage-first framing
   - is consistent but uses different ordering
   - is inconsistent / needs edit

3. List specific phrases that should appear identically (or near-identically) in abstract / ch1 contributions / ch5 contributions:
   - HIV-1 7.19× wording template
   - "wet-lab triage tool, not deployable detector" qualifier
   - "10-50 candidate sites" or "11-32 in the three escape-enrichment anchors"
   - Panel-size guardrail wording

4. Identify conflicts where chapter prose still says "deployable" or "operational" without scope qualifier.

## Output

`paper/dissertation/review/2026-05-03/r3_deep_consistency.md`

End with: `RESULT_R3_DEEP_CONSIST: matched=<n> needs_edit=<n> conflicts=<n>`

Length: ≤ 2000 words.
