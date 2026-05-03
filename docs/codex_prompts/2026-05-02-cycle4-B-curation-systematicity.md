# Cycle 4 Perspective B — Layer A curation systematicity audit

Execute the audit task NOW. Read-only. Write only the final report.

You are an independent reviewer applying ground-truth-curation reproducibility
standards to a PhD dissertation. Active English build files are at:
`/proj/paper/paper/dissertation/chapters_en/{ch1, ch3, ch4, ch5_discussion}.tex`
plus `/proj/paper/paper/dissertation/front_en/abstract.tex`. Layer A tags table
is at `/proj/paper/results/mutbench/layer_a_tags.csv` (309 rows, 12 pathogens).

Use neutral terminology. Reference Layer A tags as "the literature-curated
position-level annotation table" rather than re-quoting biology.

## Task

Apply the 17 ground-truth reproducibility checks from
[Are Ground Truth Labels Reproducible? (ICLR submission)](https://ml-eval.github.io/assets/pdf/GroundTruthReproducibilityICLRSubmitted.pdf)
adapted to a literature-curation setting. The 17 checks include:

1. Annotator agreement quantification (kappa, alpha)
2. Annotation protocol documentation
3. Annotator background and expertise
4. Quality control mechanisms
5. Disagreement resolution
6. Label noise / uncertainty quantification
7. Curation criteria explicitness (inclusion/exclusion)
8. Reproducibility of annotation process
9. Temporal stability
10. Bias and fairness
11. Error analysis / failure cases
12. Annotation data accessibility (source -> label traceability)
13. Validation against independent test sets
14. Conflict of interest
15. Statistical confidence bounds on labeling accuracy
16. Scalability and generalization assessment
17. Deprecated / outdated label audits

ALSO check IEDB curation criteria adapted:

- Original experimental data only (vs review/secondary citations)
- Position-level definedness (minimal/optimal vs region-level approximation)
- 3-concept structure (reference / position-structure / assay context)

## Inputs

- `/proj/paper/results/mutbench/layer_a_tags.csv` (per-position citation table)
- Active build manuscript files
- `/home/hwijun/.claude/projects/-proj-paper/memory/fairness_issue.md`
  (Layer A vs freq correlation context)
- `/proj/paper/paper/dissertation/chapters_en/ch3_methods.tex` Layer A definition

## Output

Write report to:
  `/proj/paper/paper/dissertation/review/2026-05-02/cycle4_B_curation.md`

Structure:
1. Per-check matrix (17 + 3 = 20 rows) with PASS / WARN / FAIL / MISSING +
   1-2 sentence justification + file:line evidence where applicable
2. Top 3 highest-risk gaps with concrete prose suggestions
3. Cherry-pick risk: if you replaced 1-3 of the cited source papers with
   alternative same-topic papers, would the 309 positions plausibly change?
   Reasoned answer (do not run new analysis).
4. Verdict: green / yellow / red on Layer A curation defensibility
5. End with a one-line headline:
   `RESULT_B: pass=<n> warn=<n> fail=<n> missing=<n> verdict=<green|yellow|red>`

Length budget: ≤ 2800 words. Do not commit.
