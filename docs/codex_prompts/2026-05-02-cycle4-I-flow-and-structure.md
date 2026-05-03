# Cycle 4 Perspective I — Content flow + good-paper structure audit

Execute the audit task NOW. Read-only. Write only the final report.

You are a reviewer evaluating the narrative coherence and structural
soundness of a PhD dissertation. Active English build files at
`/proj/paper/paper/dissertation/chapters_en/{ch1, ch3, ch4, ch5_discussion}.tex`
plus `/proj/paper/paper/dissertation/front_en/abstract.tex`. Use neutral
terminology.

## Task

Apply the components-of-a-good-paper checklist to the active build:

### Part 1 — Motivation arc

1. **Problem statement clarity**: does Ch1 introduce the problem with a
   concrete real-world stake?
2. **Gap identification**: does Ch1 explicitly state what existing work
   does NOT do that this dissertation does?
3. **Contribution preview**: does Ch1 list contributions in a form
   directly resolvable to Chapter 4 results?

### Part 2 — Method-result coupling

4. **Method completeness**: does Ch3 describe every method needed to
   reproduce every Ch4 result, without forward references that don't
   resolve?
5. **Result-claim alignment**: does every Ch4 numerical claim map to a
   Ch3 method described in advance? Find any Ch4 number that requires
   reading the Ch3 \ref{} target backward.
6. **Forward-reference hygiene**: does any Ch3 method reference a Ch4
   result that doesn't actually appear there?

### Part 3 — Abstract coherence

7. **Abstract-to-paper match**: does the abstract list claims that all
   appear in main text with consistent numbers?
8. **Abstract caveat density**: are abstract bounding qualifiers
   proportionate to the bounding language inside the manuscript? Or are
   the strongest qualifiers buried 200 pages away?

### Part 4 — Discussion / limitations

9. **Limitation engagement**: does Ch5 limitations section actually
   engage each limitation, or just list them?
10. **Future-work feasibility**: does the future-work programme name
    concrete next steps, with feasibility realism (vs aspiration)?

### Part 5 — Narrative arc across Waves 1-5

11. **Wave 1-5 narrative integration**: do the audit programme paragraphs
    read as a coherent prosecution of one hypothesis, or as 5 separate
    appendices?
12. **Wave 1-5 single-sentence summary**: can each wave be summarised in
    one sentence in the final synthesis paragraph? Or does the summary
    require reader memory?

### Part 6 — Cross-references and consistency

13. **Internal cross-reference resolution**: spot-check 5 random
    `\ref{}` calls; do they land on the intended target?
14. **Tone / terminology consistency**: does the manuscript use the same
    term for the same thing across chapters? (e.g., "Layer A" vs
    "literature-curated label" vs "primary annotation")
15. **Figure/table integration**: are Ch4 figures and tables introduced
    BEFORE the prose that interprets them, or after with backward
    reference? Find any orphan figures (not cited from prose).

### Part 7 — Closing arc

16. **Conclusion strength**: does Ch5 (which absorbs ch6 conclusion per
    the v168 macro cut) close with a single, defensible "what was learned"
    statement?
17. **Defense one-pager**: distill the dissertation to a single paragraph
    a committee could read in 30 seconds. Does it stand on its own?

## Output

Write report to:
  `/proj/paper/paper/dissertation/review/2026-05-02/cycle4_I_flow_structure.md`

Structure:
1. Per-question matrix (17 items): PASS / WARN / FAIL with 1-2 sentence
   justification + file:line evidence
2. Top 5 structural weaknesses, ranked by defense impact
3. The 30-second one-pager you produced for question 17 (≤ 200 words)
4. Recommended structural fixes (≤ 80 words each, ≤ 5 items)
5. Verdict: structure-grade (A / B / C / D)
6. End with a one-line headline:
   `RESULT_I: pass=<n> warn=<n> fail=<n> structure_grade=<A|B|C|D>`

Length budget: ≤ 3000 words. Do not commit.
