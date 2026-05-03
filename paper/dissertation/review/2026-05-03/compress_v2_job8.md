# Compression-check v2 Job 8 -- ch4:1-330

Scope: `paper/dissertation/chapters_en/ch4_results.tex:1-330`

Skipped as already-applied/overlap: the per-pathogen biology rationale table at lines 305-330 and the LOPO/null-consistency paragraph at lines 289-292 overlap items explicitly listed as already done.

## 1. Chapter key-results box

- **Type:** table-ize-prose
- **Current length:** ~95 words / ~0.15 pp
- **What it currently does:** The opening box lists three headline findings but packs interaction variance, LOPO status, and vaccine-escape anchors into one dense prose run.
- **Compression strategy:** Convert to a 3-row ledger with columns `Claim`, `Statistic`, `Interpretation boundary`. Example after-state: "Pathogen dependence | scoring x pathogen omega2 = 0.296 | primary modeled effect. LOPO | 0/11 match | null-consistent, corroborative only. Escape | HIV-1 7.19x | primary external anchor."
- **Expected page saving:** 0.1-0.2 pp
- **Expected score impact:** lift; it mirrors the successful audit-ledger style and makes the evidence hierarchy visible before the chapter begins.
- **Risk:** low; preserve the HIV-1 primary-anchor wording and the Bonferroni-survivor means caveat.

## 2. Stage 1 synthetic benchmark lead paragraph

- **Type:** trim-verbose
- **Current length:** ~135 words / ~0.20 pp
- **What it currently does:** Lines 25-26 introduce the synthetic SARS-CoV-2 benchmark, report MutClust-Hybrid's main numbers, summarize all comparator behavior, and pre-interpret the later real-GISAID drop.
- **Compression strategy:** Let Table `tab:hotspot_scores` carry comparator ranges and keep only the claim plus boundary. Example after-state: "On the controlled SARS-CoV-2-like synthetic benchmark, MutClust-Hybrid was the only method combining high precision with moderate recall (F1 0.785; HS 0.778, ~43x chance). This validates discriminative ability under dense simulated signal, not real-GISAID generalization."
- **Expected page saving:** 0.1-0.2 pp
- **Expected score impact:** neutral to lift; the paragraph becomes less table-duplicative while retaining the synthetic-only caveat.
- **Risk:** low; do not remove the real-GISAID boundary because it prevents overclaiming.

## 3. Multi-ground-truth setup details

- **Type:** move-detail-to-footnote
- **Current length:** ~105 words / ~0.15 pp
- **What it currently does:** Lines 49-52 define three ground truths with position counts, percentages, domain examples, citations, overlap statistic, and the conclusion that no single method dominates.
- **Compression strategy:** Keep one sentence naming the three ground truths and the low-overlap conclusion; move domain examples and exact percentage denominators into the table footnote/caption. Example after-state: "The three ground truths represent functional annotation, DMS escape, and convergent evolution; their low overlap (DMS vs convergent Jaccard 0.006) makes method ranking ground-truth-dependent."
- **Expected page saving:** 0.1-0.2 pp
- **Expected score impact:** lift; the conceptual point becomes clearer and exact counts remain auditable in/under Table `tab:multi_gt`.
- **Risk:** low-medium; the functional-region definition must remain precise enough to explain the 417 AA / 1,251 nt mapping.

## 4. Real-GISAID/external-method paragraph plus Stage 1 summary

- **Type:** merge-paragraphs
- **Current length:** ~160 words / ~0.25 pp
- **What it currently does:** Lines 112 and 114 separately explain the synthetic-to-real drop, sliding-window reversal, enrichment retention, external OPTICS/KDE comparison, and Stage 1 take-home.
- **Compression strategy:** Merge into one compact Stage 1 closeout and move OPTICS/KDE sweep counts to a parenthetical or footnote. Example after-state: "Real GISAID reverses the synthetic headline: sparse nonzero H-scores lower MutClust-Hybrid to HS 0.383, while enrichment remains 6.9-8.0x and sliding-window F1 is highest. Stage 1 therefore validates the metric and exposes pathogen/data-regime dependence."
- **Expected page saving:** 0.15-0.3 pp
- **Expected score impact:** lift; it removes repeated "controlled sanity check" language and makes the transition to Stage 2 sharper.
- **Risk:** low-medium; retain the external OPTICS/KDE result somewhere if it is needed as a superiority check for MutClust-Hybrid.

## 5. Stage 2 setup and benchmark-scale repetition

- **Type:** consolidate-duplicate
- **Current length:** ~230 words / ~0.35 pp
- **What it currently does:** Lines 229-238 introduce Stage 2 scale, scoring/detection counts, 10-feature derivation, MCC rationale, and section order; lines 244-250 repeat the benchmark scale, scoring categories, metrics, DMS subset, and accession provenance.
- **Compression strategy:** Replace both blocks with one setup paragraph plus a compact scale ledger. Example after-state: "Stage 2 contains 8,580 evaluations: 20 scoring formulas from 10 biological features x 39 detector variants from 14 families x 11 pathogens. MCC is primary because hotspot-score stability was not cross-validated across all pathogen-specific alignments."
- **Expected page saving:** 0.3-0.5 pp
- **Expected score impact:** lift; this is the cleanest new version of the audit-ledger pattern in the scoped chunk and removes visible duplicate bookkeeping.
- **Risk:** low; keep the v1 MutClust rationale cross-reference and the DMS Layer C six-pathogen boundary.

## 6. Prospective backtest narrative and 4-feature extension

- **Type:** table-ize-prose
- **Current length:** ~300 words / ~0.45 pp
- **What it currently does:** Lines 184-197 define the sliding-window prospective protocol, summarize 73 windows and 219 top-k evaluations, then reports 2-feature, 3-feature, and 4-feature outcomes with per-pathogen positives and HCV failure.
- **Compression strategy:** Convert the result portion to a small table: `Model`, `Grand mean AUROC/MCC`, `Where it helps`, `Where it fails`, `Inference`. Example after-state: "Freq+entropy is mostly chance (AUROC 0.539); homoplasy helps EV-A71/Rabies but collapses HCV; 4-feature slightly raises AUROC while degrading Top-30 MCC."
- **Expected page saving:** 0.4-0.7 pp
- **Expected score impact:** lift; the current text is defensible but hard to scan, and a table makes the prospective/non-prospective boundary much clearer.
- **Risk:** medium; the temporal-split definition must stay in prose before the table so the negative result remains interpretable.

## Summary

Top opportunities: Stage 2 setup consolidation (#5), prospective backtest table (#6), and Real-GISAID/Stage 1 closeout merge (#4). Together these save roughly 0.85-1.5 pages while improving evidence traceability. Including the smaller local trims, the scoped chunk has about 1.15-2.1 pages of plausible additional compression without touching already-applied candidates.

RESULT_COMPRESS_V2_J8: candidates=6 total_pages_saved=1.6 total_score_impact=+0.3
