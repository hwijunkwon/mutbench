# Compression-check v2 Job 12 -- ch5:151-340

Scope reviewed: `paper/dissertation/chapters_en/ch5_discussion.tex` lines 151-340.

Already-applied items were screened out, especially the Ch5 defense map, Layer A provenance work, Wave 1-3 / 4 / 5 paragraph split, Bolker trim, Layer A limitations paragraph, and Ch4 audit-ledger pattern. The candidates below are new opportunities still visible in this smaller slice.

## 1. Practical Workflow Dense Paragraph

1. **Type:** table-ize-prose / trim-verbose
2. **Current length:** ~250 words plus adjacent 6-row scoring-prior table; ~0.6-0.8 pp.
3. **What it currently does:** Lines 160-181 give a four-step workflow, feature runtime ladder, detector defaults, total runtime, cold-start fallback, live-deployment caveat, and then a family-prior table.
4. **Compression strategy:** Convert the workflow paragraph into a compact 4-row table with columns `Step`, `Default`, `Runtime / constraint`, and `Boundary`; keep the family-prior table only as a narrow “starting prior” companion or fold its strongest priors into the workflow table.

   Example after-state: “For new pathogens, MutBench is a four-step retrospective workflow: collect $\geq200$ diverse sequences, compute low-cost MSA/tree features first, select a family-level scoring prior, then run KDE/Wavelet defaults and report abstention status.”
5. **Expected page saving:** 0.3-0.5 pp.
6. **Expected score impact:** lift. The same operational content becomes examiner-scannable and looks like a usable protocol rather than a compressed methods recap.
7. **Risk:** low. Preserve the 4-feature cold-start caveat and the “not live deployment” sentence.

## 2. Contribution Summary Restates Earlier Evidence

1. **Type:** consolidate-duplicate / table-ize-prose
2. **Current length:** ~390 words; ~0.7 pp.
3. **What it currently does:** Lines 238-243 restate all three contributions with many headline numbers already present in the abstract, Ch4 results, practical-value discussion, and defense map.
4. **Compression strategy:** Replace with a 3-row “contribution / evidence anchor / boundary” ledger or three short bullets. Keep only one numeric anchor per contribution and cross-reference the defense map for oral wording.

   Example after-state: “Contribution 2: pathogen-dependent information choice. Evidence: scoring $\times$ pathogen $\omega^2=0.296$ and oracle-generalized gap 0.265. Boundary: LOPO 0/11 is corroborative, not independent evidence.”
5. **Expected page saving:** 0.25-0.45 pp.
6. **Expected score impact:** neutral to lift. It reduces result-recitation fatigue while preserving the thesis claims immediately before the audit boundary.
7. **Risk:** low-medium. Do not delete the HIV-1 external-validation hierarchy, because that is the practical-value anchor.

## 3. Limitation Matrix Cells Are Still Prose-Heavy

1. **Type:** trim-verbose
2. **Current length:** ~650 words across the longtable body; ~1.1-1.3 pp.
3. **What it currently does:** Lines 213-226 provide the already-consolidated limitations matrix, but many cells remain full explanatory sentences with multiple statistics.
4. **Compression strategy:** Keep the matrix, but convert cells to clause fragments and one numeric bound per row. Move secondary numerics to the cited section or footnote. This is not a new limitations consolidation; it is a table-cell tightening pass.

   Example after-state: “PLM leakage/proxy collinearity | ESM-2 contains targets; Tranception near-equivalent in 11/12 pathogens | Treat PLM as region signal; HIV-1 dissociates | Table X.”
5. **Expected page saving:** 0.4-0.7 pp.
6. **Expected score impact:** lift. The matrix becomes a defense aid instead of another dense prose block embedded inside a table.
7. **Risk:** medium. The table is load-bearing for examiner risk management; keep the key bounds: AUROC 0.539, 0/12 callable, $\omega^2$ subset values, Bolker 20-30, and no raw GISAID FASTA.

## 4. Future Roadmap Table Duplicates Following Paragraphs

1. **Type:** consolidate-duplicate / merge-paragraphs
2. **Current length:** table plus ~210 words; ~0.6-0.8 pp.
3. **What it currently does:** Lines 263-292 first summarize four future-work priorities in a table, then restate adaptive selection, expanded-panel engineering, phylogenetic correction, scope extension, and release in prose.
4. **Compression strategy:** Make `tab:future_roadmap` carry the gate/impact details and reduce the prose to two bridging paragraphs: one for “negative gates already closed” and one for “true future validation requires 20-30+ externally labeled pathogens.”

   Example after-state: “The roadmap separates completed negative gates from future validation. The next decisive experiment is not another same-panel weighting model, but a 20-30+ pathogen panel with curated labels, time-forward validation, and paired nested-LOPO/callability gates.”
5. **Expected page saving:** 0.45-0.75 pp.
6. **Expected score impact:** lift. The current version makes future work feel longer than the conclusion; compression sharpens the research agenda.
7. **Risk:** low. Keep the distinction that feature expansion is feasible but label provenance remains the bottleneck.

## 5. Concluding Claim Echoes the Take-Home Line

1. **Type:** merge-paragraphs / trim-verbose
2. **Current length:** ~115 words across line 298 and line 317; ~0.15-0.2 pp.
3. **What it currently does:** The concluding paragraph and the standalone take-home message both say that pathogen-information-source fit explains more variation than detector choice, with bounded deployment.
4. **Compression strategy:** Fold the take-home sentence into the first sentence of the concluding paragraph and delete the standalone line after the defense map.

   Example after-state: “MutBench’s take-home result is that viral hotspot detection is driven more by pathogen-specific biological information source than by detector choice alone.”
5. **Expected page saving:** 0.1-0.2 pp.
6. **Expected score impact:** neutral to lift. Small saving, but it removes a visible echo after a major table.
7. **Risk:** low.

## Not Re-Recommended

- Lines 246-254 still contain compressible Wave audit detail, but the Wave 1-3 / 4 / 5 split is explicitly already done. A further audit-ledger conversion would overlap that prior recommendation, so it is skipped.
- Lines 299-315 are the already-done defense map and are not re-recommended.
- Lines 321-340 already reflect the code/data availability table compression pattern; only marginal row tightening remains, so it is below the candidate threshold for this job.

RESULT_COMPRESS_V2_J12: candidates=5 total_pages_saved=2.0 total_score_impact=+0.2
