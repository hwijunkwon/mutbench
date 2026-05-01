# Codex task — Wave 4 prose insertion (ch4 + ch5, English mirror)

You are editing `/proj/paper/paper/dissertation/chapters_en/ch4_results.tex` and
`/proj/paper/paper/dissertation/chapters_en/ch5_discussion.tex`. Three edits total.
All other files are read-only.

## Context

Wave 4 = Tier 2 features-only LOPO + expanded-target stability diagnostics. Result
report: `/proj/paper/paper/dissertation/review/2026-04-30/wave4/w4_tier2_features_lopo.md`
(read this first). Output CSVs live under `results/mutbench/codex_wave4/` and
`results/mutbench/codex_wave4/w4_summary_figure.png`.

Branch: `experiments/waves`. Wave 1/2/3 prose already lives in the English mirror
(`chapters_en/`); this insertion extends the same audit thread.

## Headline numbers (from the report — do not paraphrase away the bounding qualifiers)

- hscore overlap audit on Dengue:dengue_e, HIV-1:hiv1_gp120, Norovirus:norovirus_vp1
  — 0/3 PASS at the predeclared threshold (median Spearman ρ ≥ 0.70 AND top-10 Jaccard ≥ 0.50).
  Branch 5 fired → 2-core (`freq, entropy`) fallback.
- Labeled 12-fold 2-core LOPO: mean MCC = 0.077 (sd 0.136), 8/12 positive folds,
  paired Wilcoxon greater vs recomputed 4-core comparator p = 0.368
  (i.e., 2-core ≈ 4-core, statistically indistinguishable).
- D1 callability recheck: 0/12 — matches Wave 2 P5 failure mode; the rate-limiting
  gate is unchanged after fallback.
- Expanded 28-target stability: 1/28 stable, same-target quorum 0, union quorum 16,
  quorum_pass = False; sign-fitting bootstrap (1,000 resamples of training pathogens
  with replacement, seed 42) preserves the full-sample sign in 81.6% (freq) and
  94.4% (entropy) of bootstraps.
- All 16 unlabeled targets fall **inside** the labeled feature envelope — feature-space
  compatibility holds, so Layer A curation can proceed for the next wave.
- Predeclared interpretive branch after fallback: closest to Branch 2 of the plan
  (preserve labeled-panel signal, conclude features-only expansion is too schema-shifted
  for stable transfer; next step is Layer A pilot + feature augmentation, not expanded
  callability).
- Wave 5 ordering (pilot 3 Layer A curation for YFV/Lassa/WNV) preserved because
  labeled 2-core was bounded positive.

## Edit 1 — ch4_results.tex: new paragraph after `para:p6_biological_nulls`

**Location:** insert immediately after the long `\paragraph{Biologically-realistic null calibration (P6).}` body that ends with `... 8 edits applied (\texttt{paper/dissertation/review/2026-04-30/codex\_wave3\_plan\_review.md}).` and before the existing `\paragraph{Hierarchical Bayesian adaptive-weighting robustness check.}` paragraph.

**New `\paragraph` heading + label:**
```
\paragraph{Tier 2 features-only LOPO and expanded-target stability (W4).}
\label{para:w4_tier2_lopo}
```

**Body requirements** (one paragraph, ~200–280 words, English to match the surrounding ch4_en style):

- Frame this as the Wave 4 expansion of the audit programme on the `experiments/waves`
  branch only — a features-only Tier 2 LOPO pre-registered to test whether the
  panel-size limit identified in Waves 1–3 dissolves at $n \approx 30$.
- Begin with the hscore harmonization audit failure (0/3 PASS on
  Dengue/HIV-1/Norovirus; cite Spearman ρ ≥ 0.70 AND top-10 Jaccard ≥ 0.50 threshold).
  State that Branch 5 fired and the analysis used the 2-core fallback `freq, entropy`.
- Report labeled-only 12-fold LOPO results: mean 2-core MCC = 0.077 (sd 0.136),
  8/12 positive folds, paired Wilcoxon $H_1$: 2-core $>$ recomputed 4-core
  $p = 0.368$ — i.e., bounded positive but statistically indistinguishable from the
  recomputed 4-core comparator at this sample size.
- Note D1 callability recheck = 0/12 (matches Wave 2 P5; the rate-limiting gate is
  not relaxed by the fallback). Reference `\ref{para:p5_callability}`.
- Report expanded 28-target stability: 1/28 stable, union quorum 16, quorum_pass =
  False; bootstrap-sign agreement with full-sample sign 81.6% (freq) / 94.4%
  (entropy). Make explicit that this is sign-fitting instability of the 2-core under
  pathogen-resampling, not a claim that the 16 new targets are biologically poor.
- Report that 16/16 unlabeled targets fall inside the labeled feature envelope — so
  feature-space compatibility for Layer A curation is established even though
  callability is not. State this is a feasibility claim only.
- Close with the predeclared interpretive branch: features-only expansion is too
  schema-shifted to dissolve the panel-size limit by itself; Layer A curation
  remains the rate-limiting next step. Cross-reference Wave 5 pilot 3 ordering
  (YFV/Lassa/WNV) preserved in `\ref{sec:future_work}`.
- Include script + CSV references inline:
  `scripts/codex_w4_features_lopo.py`,
  `scripts/codex_w4_task4_summary.py`,
  `results/mutbench/codex_wave4/w4_labeled_lopo_summary.csv`,
  `results/mutbench/codex_wave4/w4_expanded_stability_per_target.csv`,
  `results/mutbench/codex_wave4/w4_summary_figure.png`,
  and the report
  `paper/dissertation/review/2026-04-30/wave4/w4_tier2_features_lopo.md`.
- Style: match Paragraphs `para:p5_callability` and `para:p6_biological_nulls` —
  same passive academic voice, `\texttt{}` for filenames, `\emph{}` for the rhetorical
  beats ("First", "Second", "Third" or equivalent), bold only for the headline
  fail/pass counts (e.g. `$\mathbf{0/12}$`, `$\mathbf{16/16}$`).
- Do NOT claim the 4-core is dominated, NOT claim Wave 4 validates Algorithm 1,
  NOT claim Layer A curation is complete. Bounded interpretation only.

## Edit 2 — ch5_discussion.tex: extend `para:wave1_codex_audits`

**Location:** the paragraph `\paragraph{Falsification-resistant audits and the boundary of Algorithm 1's claim.}` (label `para:wave1_codex_audits`) currently ends with the sentence `The expanded-panel work above remains the natural prospective test.` Append (do NOT replace the existing body; just append one sentence after it, inside the same paragraph) ~50–80 words covering:

- Wave 4 (Paragraph `\ref{para:w4_tier2_lopo}`) tested the features-only expansion
  on the `experiments/waves` branch: hscore did not harmonize (0/3 PASS), so a 2-core
  (`freq, entropy`) fallback was used.
- Labeled 12-fold 2-core LOPO is bounded positive but indistinguishable from the
  recomputed 4-core (mean MCC 0.077, 8/12 positive, paired Wilcoxon p = 0.368);
  D1 callability remains 0/12 and expanded 28-target sign stability is 1/28.
- The 16/16 unlabeled-target envelope establishes feature-space feasibility for
  Layer A curation but does not by itself relax the panel-size limit.
- Conclude: features-only expansion does not dissolve the bound; Layer A curation
  is the next prospective test (forward reference to Wave 5 pilot 3).

## Edit 3 — ch5_discussion.tex: extend the "Prospective Callability and Abstention Rule (Wave 2 result)" subsection

**Location:** the `\textbf{Prospective Callability and Abstention Rule (Wave 2 result).}` paragraph (around line 301) currently ends with `... and the deployment claim can be tested rather than refused.` Append one sentence (50–80 words) at the end of that same paragraph covering:

- Wave 4 has now executed the Tier 2 features-only LOPO at the available expanded
  scope (`\ref{para:w4_tier2_lopo}`); the 2-core fallback bounded positive but
  D1 = 0/12 and 1/28 stable, so the panel-size limit is confirmed and Layer A
  curation (Wave 5 pilot 3) is the rate-limiting next step rather than an
  optional add-on.
- Keep the Wave 2/3 cross-references intact.

## Style + safety constraints

- Both files are LaTeX. Preserve all existing labels, citations, and `\texttt{}`
  formatting. Do not introduce new bib entries.
- Do not change pre-existing prose. Only add the three insertions above.
- Use $n \approx 30$ rather than committing to a specific labeled count.
- Do not use the word "novel" or "we propose"; this is a results extension.
- Do not edit `chapters/` (the Korean chapters); only `chapters_en/`.
- Do not rebuild the PDF; that step is owned by the parent agent.
- Do not commit.

## Deliverable

After both files are edited, print:

```
=== W4 PROSE INSERTED ===
ch4 line ranges: <start>-<end>
ch5 edit 1 (para:wave1_codex_audits) line ranges: <start>-<end>
ch5 edit 2 (Prospective Callability) line ranges: <start>-<end>
approx wordcount delta: ch4=<n>, ch5=<n>
```

Then `git diff --stat` for the two files.
