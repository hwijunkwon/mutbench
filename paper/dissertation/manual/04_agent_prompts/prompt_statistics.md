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

# Phase 2 Statistics Review

Perform a formal statistical audit. Do not consult Phase 1 Blueteam, Phase 2 Redteam, CCB, or Professor outputs if present; this is an independent statistics pass.

Use active-build files plus authoritative reports. The memory concern to test is: Layer A labels can correlate strongly with `freq`; this creates a correlation/circularity risk, not automatic invalidation. Known anchor values from memory are Spearman rho 0.973 between rpb-vs-freq and freq-MCC across pathogens, and mixed Layer C correlations across four valid pathogens. Verify manuscript treatment against active files before judging.

Produce exactly ten PASS/WARN/FAIL items:

1. `omega^2` interpretation correctness, including evaluation-level 0.296 vs cell-level/lower-bound caveats.
2. Paired vs unpaired test choice, including Welch t for cross-panel comparisons and Wilcoxon/paired procedures for same-fold comparisons.
3. Multiple-comparisons control and whether family-wise claims are separated from exploratory claims.
4. Sign-stability bootstrap interpretation: whether sign stability is treated as directional reliability rather than effect-size proof.
5. MCC vs precision@20 reporting consistency and any mismatch between metric-specific claims.
6. Sample-size justification for the n=11/n=12 panel and small-cluster caveats.
7. Wave 5 cross-panel Welch t caveat enforcement: whether cross-panel comparisons are labeled as sensitivity, not definitive paired validation.
8. Permutation-null framework rigor for P1 and P6, including null choice, smoothed p-values where relevant, and global-vs-per-pathogen interpretation.
9. Callability rule pre-registration vs post-hoc adjustment, including Wave 2's 0/12 callable outcome.
10. Fairness/correlation framing: is the Layer A vs `freq` correlation/circularity risk explicitly framed in the manuscript or buried in generic limitations? Cite location and severity.

For each item, give PASS/WARN/FAIL plus 1-3 sentences and file:line evidence. End with a core-claim statistical reliability rating: high, medium, or low, with one paragraph explaining the rating.

Write the final report to:

`/proj/paper/paper/dissertation/review/2026-05-02/phase2_statistics.md`

Maximum length: 3000 words.
