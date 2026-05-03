# Risk-3 Deep anchor 1 — HIV-1 anchor preservation across abstract+ch1+ch4+ch5

Execute the analysis NOW. Read-only. Do not commit.

## Context

Risk-3 verdict was REVISE because anchor preservation 4/8 in initial abstract draft. The HIV-1 anchor (7.19×, p_adj=2.5e-16, 82% disjoint, 37/45 novel positions, novel-only 7.16-8.24×, p_adj=3.9e-9) is the LOAD-BEARING practical-value evidence. Verify it is preserved consistently across all 4 active-build files.

## Inputs

- `paper/dissertation/front_en/abstract.tex`
- `paper/dissertation/chapters_en/ch1_introduction.tex`
- `paper/dissertation/chapters_en/ch4_results.tex` (lines 941–989 vaccine escape table + footnote)
- `paper/dissertation/chapters_en/ch5_discussion.tex`
- `results/mutbench/vaccine_escape_stage3.csv` (HIV-1 freq+Wavelet(t=1.5) row)
- `paper/dissertation/review/2026-05-03/risk3_abstract_analysis.md`

## Task

For each of the 4 manuscript files:

1. Find every place where HIV-1 anchor appears (grep for "7.19", "HIV-1", "vaccine escape", "82\\%", "Layer-A-disjoint", "novel-only").
2. List the exact wording used.
3. Verify against `vaccine_escape_stage3.csv` HIV-1 freq+Wavelet(t=1.5) row: enrichment=7.1875, n_overlap=23, n_escape=45.
4. Identify any place where the anchor is implied but not stated, or stated inconsistently across files.
5. Recommend a SINGLE canonical wording template that should appear in abstract + ch1 introduction box + ch4 table + ch5 conclusion.

## Output

`paper/dissertation/review/2026-05-03/r3_deep_anchor.md`

End with: `RESULT_R3_DEEP_ANCHOR: occurrences=<n> consistency=<consistent|partial|inconsistent> canonical_template="<one sentence>"`

Length: ≤ 1500 words.
