# Cycle 4 Perspective C — Negative-result framing trap

Execute the audit task NOW. Read-only. Write only the final report.

You are an independent reviewer evaluating whether negative or null results
in a PhD dissertation are framed honestly versus rebranded into apparent
strengths. Active English build files at
`/proj/paper/paper/dissertation/chapters_en/{ch1, ch3, ch4, ch5_discussion}.tex`
plus `/proj/paper/paper/dissertation/front_en/abstract.tex`. Use neutral
terminology.

## Task

Identify every negative or abstention or null result in the manuscript.
For each, score:

1. **Disclosure**: is the negative result reported with its original
   negative framing, or rebranded?
2. **Boundary**: is the bounding language adjacent to the claim, or is it
   in a different chapter that requires a determined reader to find?
3. **Contradiction risk**: does any later prose use the same evidence to
   support a positive narrative without re-declaring the negative?
4. **Honest synthesis**: does the dissertation acknowledge what would be
   different if the negative result were instead positive?

## Negative results to evaluate (at minimum)

- Wave 5 Layer A' Branch C (mean MCC -0.055, 2/10 positive folds)
- Wave 4 callability rule 0/12 abstention
- Wave 1 P1 four-null gradient (5/12 -> 1/12 under strict null)
- Wave 1 P1 HARD STOP (P4 not run)
- HBFWS pre-registered failure (p=0.78)
- Cycle 7B six adaptive-method failures
- LOPO 0/11 exact-match failure
- Friedman p=0.990 (no universally best combination)
- Sliding-window forward-time enrichment ~chance for most pathogens
- HBV polymerase pilot non-significant (p=0.354 global, p=0.136 RT-domain)

## Output

Write report to:
  `/proj/paper/paper/dissertation/review/2026-05-02/cycle4_C_negative_framing.md`

Structure:
1. Per-result table: result, disclosure score (good/borderline/poor),
   boundary score, contradiction risk, file:line of strongest framing
   and weakest framing
2. Top 3 framing risks with concrete prose suggestions
3. "Defense honesty" verdict: high / medium / low
4. End with a one-line headline:
   `RESULT_C: results=<n> good=<n> borderline=<n> poor=<n> verdict=<high|medium|low>`

Length budget: ≤ 2500 words. Do not commit.
