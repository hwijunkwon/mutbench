# Cycle 4 Perspective H — Generalisation scope (RNA virus -> beyond)

Execute the audit task NOW. Read-only. Write only the final report.

You are a reviewer challenging the dissertation's claim of practical
applicability. Active English build files at
`/proj/paper/paper/dissertation/chapters_en/`. Use neutral terminology.

## Context

The dissertation is explicitly scoped to 11 RNA-virus surface
glycoproteins, point substitutions only (`front_en/abstract.tex:2`). The
discussion includes one DNA-virus pilot (HBV polymerase, $n=708$
sequences, drug-resistance Layer A test $p=0.354$ global, $p=0.136$
RT-domain restricted; `chapters_en/ch5_discussion.tex` Section
`\ref{para:hbv_pilot}`).

## Task

Evaluate the generalisation scope and its boundary documentation:

1. **In-scope completeness**: does the manuscript clearly document why
   each of the eight excluded RNA-virus surface proteins (e.g., other
   alphavirus E2, additional bunyavirus G, etc.) was OR was not in the
   panel?
2. **Out-of-scope discipline**: does the manuscript transparently state
   that DNA viruses, retroviruses (already partly covered by HIV-1?),
   bacteria, and eukaryotic pathogens are explicitly excluded?
3. **Pilot extrapolation**: HBV pilot returns negative. Does the
   manuscript treat this as "scope confirmation" or accidentally as
   "method failure"?
4. **DMS / fitness vs detection**: the paper distinguishes its
   region-level detection task from per-variant fitness-regression
   benchmarks. Does it document where the boundary is, and whether the
   boundary defence is valid?
5. **Substitution-rate scope**: substitution rates from 1e-3 (HIV-1) to
   1e-4 (Rabies). Outside this band, does the manuscript explicitly say
   the conclusions do NOT apply?
6. **Indels and multi-position events**: explicitly out-of-scope; is the
   exclusion documented and defended?

## Output

Write report to:
  `/proj/paper/paper/dissertation/review/2026-05-02/cycle4_H_generalisation.md`

Structure:
1. Per-question table (6 questions above): documented? bounded? defended?
   with file:line evidence
2. Top 3 generalisation-attack vectors a defense committee might use
3. Recommended manuscript additions (≤ 80 words each, ≤ 3 items)
4. Verdict: scope discipline (high / medium / low)
5. End with a one-line headline:
   `RESULT_H: questions_pass=<n>/6 discipline=<high|medium|low>`

Length budget: ≤ 2500 words. Do not commit.
