You are an independent reviewer for a PhD dissertation. **Read-only mode.**
Do not modify the manuscript or any data. Write only your final report
to the path specified at the bottom.

The dissertation is at /proj/paper/paper/dissertation/. The active build
inputs are:
  - chapters_en/ch1_introduction.tex
  - chapters_en/ch3_methods.tex
  - chapters_en/ch4_results.tex
  - chapters_en/ch5_discussion.tex
  - front_en/abstract.tex

Orphan files (NOT in build) are: ch2_background.tex, ch5_adapt.tex,
ch6_conclusion.tex. Do not cite them as evidence.

Authoritative supporting reports under paper/dissertation/review/:
  - 2026-04-30/wave1/, wave2/, wave3/, wave4/ — codex per-task reports
  - 2026-05-02/wave5_replacement/lap_lopo_report.md — Wave 5 Layer A' result
  - 2026-05-02/codex_layerA_uniprot_review.md — codex review of Layer A' inventory
  - 2026-05-02/codex_wave5_disposition_review.md — earlier disposition review

Use neutral, scope-appropriate terminology. Do not re-quote biological
detail beyond what is required for the specific finding you are reporting.

# Phase 1 Blueteam Argument Map

Build the dissertation's claim-evidence map. Treat active-build source files as the authoritative manuscript and supporting reports as audit evidence. Do not consult Phase 2 Redteam, Statistics, CCB, or Professor outputs if present.

Focus on three core claims:

1. The 12-pathogen literature-curated benchmark and three-layer label framework are a defensible benchmark contribution, despite annotation heterogeneity and active-vs-orphan file drift.
2. The 1023-subset Shapley audit bounds the cold-start feature core: the historical 4-core ranks 87/1023, is dominated by the 3-core, and should be framed as a fixed heuristic rather than a discovered optimum.
3. Wave 5 Layer A' label-provenance sensitivity produced Branch C: structured public-database labels do not preserve the directional 2-core signal, so the manuscript should frame this as provenance sensitivity and a boundary condition, not a new validation success.

For each claim, report:

- Main manuscript statement: active-build file and line number.
- Strongest supporting evidence: active-build file/report path and line number.
- Weakest supporting evidence or most fragile assumption: active-build file/report path and line number.
- Whether the wording is appropriately bounded, overstated, or understated.

Then identify five plausible failure scenarios and the exact manuscript paragraph that defends against each. Include at least these scenarios: label-provenance mismatch, panel-size underpowering, Algorithm 1 overclaiming, frequency/label correlation, and prospective-validation absence.

Finally, identify the weakest paragraph in each active chapter/source group: Ch1, Ch3, Ch4, Ch5, and abstract. Give file:line, why it is weak, and whether it is a defense blocker.

Use file-line citations produced by `nl -ba` or equivalent. Do not cite orphan files as evidence. Keep the report neutral and audit-oriented.

Write the final report to:

`/proj/paper/paper/dissertation/review/2026-05-02/phase1_blueteam.md`

Maximum length: 3000 words.
