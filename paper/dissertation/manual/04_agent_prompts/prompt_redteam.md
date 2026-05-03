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

# Phase 2 Redteam Adversarial Review

Attack the dissertation as a hostile but fair committee member. Classify findings as Critical, Major, or Minor. Do not consult Phase 1 Blueteam, Statistics, CCB, or Professor outputs if present; this is an independent verification and validation pass.

Required attack targets. You must explicitly attempt each, even if the final severity is Minor or "not sustained":

1. Wave 5 Branch C interpretation: could the manuscript be read as hiding a negative result under the softer name "sensitivity check"?
2. Panel-size limit framing: is the "not yet learnable from n=11/n=12" claim falsifiable as written, or is it insulated from contradiction?
3. Layer A vs Layer A' provenance argument: is the asymmetry genuinely informative, or is it a post-hoc explanation for failed transfer?
4. Algorithm 1 vs benchmark separation: does the manuscript over-stake the cold-start operationalization relative to the benchmark contribution?
5. `omega^2 = 0.296` interpretation: is it described correctly given the known concern that literature-curated labels and frequency can be strongly correlated?

For each attack, provide:

- Severity: Critical, Major, Minor, or Not sustained.
- Evidence path: active-build file:line and, when useful, supporting report path:line.
- Failure mode: what a hostile examiner could say.
- Minimal prose fix: one concrete edit location and the smallest wording change that would close the issue.

Also scan for selective reporting around Waves 1-5: whether null, failure, and abstention outcomes are visible in the abstract, results, and discussion at the right strength. Treat orphan files as non-evidence.

Use file-line citations from `nl -ba` or equivalent. Keep biological detail abstract and refer to existing reports rather than re-stating technical specifics. Lead with Critical findings, then Major, then Minor.

Write the final report to:

`/proj/paper/paper/dissertation/review/2026-05-02/phase2_redteam.md`

Maximum length: 3000 words.
