# Cycle 4 Perspective G — External anchor cherry-pick risk

Execute the audit task NOW. Read-only. Write only the final report.

You are a reviewer attacking the practical-anchor claim of a PhD
dissertation. Active English build files at
`/proj/paper/paper/dissertation/chapters_en/`. Use neutral terminology.

## Context

The dissertation reports retrospective enrichment for vaccine-escape /
antibody-escape positions on three of the eleven panel pathogens:

- HIV-1: 7.19x enrichment with $p_{\text{adj}} = 2.5 \times 10^{-16}$
  (primary anchor; 82% Layer-A-disjoint; novel-only enrichment 7.16-8.24x)
- H3N2: 9.36x enrichment (self-consistency check, 69% Layer-A overlap)
- SARS-CoV-2: 7.63x enrichment (exploratory after Bonferroni)

Manuscript framing: "Validation is restricted to 3/11 pathogens by curated
antibody-escape annotation availability, not by panel design"
(`front_en/abstract.tex:11`).

## Task

Evaluate the cherry-pick attack:

1. **Availability claim test**: is the "by annotation availability"
   defense actually true? List the 8 NOT-validated pathogens and state for
   each whether external escape annotations exist (you may use general
   knowledge; do not run web searches).
2. **Selection bias test**: among the 3 validated, would a different
   choice (e.g., HIV-1 + H3N2 only, or all 4 with reasonable annotations)
   give qualitatively different conclusions?
3. **Layer-A-disjoint defense**: HIV-1 reports a novel-only enrichment on
   37 Layer-A-disjoint positions. Is this defense (Layer-A overlap < 33%
   gate) actually applicable to the other two pathogens?
4. **Bonferroni discount**: SARS-CoV-2 is "exploratory after Bonferroni".
   Does the manuscript clearly state which results survive vs are
   discounted?
5. **Generalisation reach**: does the manuscript over-generalise from
   3-anchor evidence to all-11-panel deployability?

## Output

Write report to:
  `/proj/paper/paper/dissertation/review/2026-05-02/cycle4_G_anchor_cherry_pick.md`

Structure:
1. Per-attack table (5 attacks above): sustained / partial / not-sustained
   + 2-3 sentence justification + file:line evidence
2. Strongest counter-attack the user should expect at defense, and the
   manuscript's current best response (cite location)
3. Recommended manuscript additions (≤ 80 words each, ≤ 3 items)
4. Verdict: how vulnerable is Contribution 3 to a cherry-pick attack
   (low / medium / high)?
5. End with a one-line headline:
   `RESULT_G: attacks_sustained=<n>/5 vulnerability=<low|medium|high>`

Length budget: ≤ 2500 words. Do not commit.
