# Cycle 4 Perspective E — Reproducibility audit (external-team perspective)

Execute the audit task NOW. Read-only. Write only the final report.

You are an external research team trying to independently reproduce the
dissertation's headline numbers given only the public artefacts. Active
English build files at `/proj/paper/paper/dissertation/chapters_en/`. Use
neutral terminology.

## Task

Inventory whether each headline number can be re-derived from artefacts
accessible to an external team. For each headline number below, classify:

- **Reproducible**: scripts + data + seed + config all available; one
  command can re-derive the number
- **Reproducible-with-effort**: artefacts exist but rebuilding requires
  manual scripting
- **Not reproducible**: required artefact is missing, behind authentication,
  or only described in prose

## Headline numbers to audit

- $\omega^2_{\text{scoring x pathogen}} = 0.296$ + 95% CI [0.195, 0.333]
- $\omega^2_{\text{cell-level}} = 0.234$
- HIV-1 enrichment 7.19x with $p_{\text{adj}} = 2.5 \times 10^{-16}$
- Cold-start 4-core nested-LOPO mean MCC 0.081
- Cycle 7B six adaptive methods all failing (smallest p = 0.56)
- Wave 1 P1 100k-permutation null calibration outputs
- Wave 5 Layer A' LOPO mean MCC -0.055 with 2/10 positive folds
- 1023-subset Shapley with 4-core rank 87/1023 and 3-core rank 27/1023
- Friedman $p = 0.990$ on 11 pathogens

## Inputs

- Code at `/proj/paper/scripts/` (which scripts exist for which numbers?)
- Data CSVs at `/proj/paper/results/mutbench/`
- Random seed declarations in code
- Manuscript pointers (Section / Chapter mapping each number to a script or CSV)
- License + access notes in `chapters_en/ch5_discussion.tex` Section
  `\ref{sec:code_availability}` (the "MIT License + CC-BY-NC 4.0" paragraph)

## Output

Write report to:
  `/proj/paper/paper/dissertation/review/2026-05-02/cycle4_E_reproducibility.md`

Structure:
1. Per-number reproducibility table (classification + script/CSV path +
   reproducibility command if available)
2. Gaps: for each Not-reproducible item, state the smallest fix
   (publish artefact, write a one-shot script, etc.)
3. License/access concern audit (any restricted dependencies?)
4. External-team time-to-reproduce estimate (hours): best/realistic/worst
5. End with a one-line headline:
   `RESULT_E: reproducible=<n> with_effort=<n> not_reproducible=<n> total=<n>`

Length budget: ≤ 2500 words. Do not commit.
