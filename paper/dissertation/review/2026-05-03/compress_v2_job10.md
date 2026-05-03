# Compression-Check v2 Job 10 -- ch4:701-989

Scope reviewed: `paper/dissertation/chapters_en/ch4_results.tex` lines 701-989. The Ch4 audit-ledger table itself is already applied, so I did not re-recommend the ledger conversion or deletion of its now-summarized audit rows as a standalone candidate.

## Candidate 1 -- Cold-Start baseline progression prose/table duplication

1. **Type:** consolidate-duplicate / trim-verbose
2. **Current length:** ~260 prose words + table caption/minipage note; ~0.5 pp
3. **What it currently does:** Lines 760-793 argue that the 4-core ensemble beats single-feature and cumulative top-K baselines, then the table and minipage restate the same comparisons.
4. **Compression strategy:** Let the table carry the numeric progression and replace the three-takeaway prose plus minipage with one lead sentence and one interpretive sentence. Example after-state: "Table X shows that the fixed 4-core beats top-1 through top-5 cumulative baselines and trails the oracle 4-of-210 subset by only +0.014 MCC; the ensemble is therefore useful but not label-optimized."
5. **Expected page saving:** 0.3-0.4 pp
6. **Expected score impact:** lift. The defense improves because the table becomes the evidence and the text stops re-litigating every row.
7. **Risk:** low

## Candidate 2 -- 210-subset paragraph plus full-lattice paragraph overlap

1. **Type:** merge-paragraphs / trim-verbose
2. **Current length:** ~260-word subset paragraph + table note + ~110-word full-lattice paragraph; ~0.6 pp
3. **What it currently does:** Lines 795-833 separately explain the 210 fixed-size subset audit and the 1023 full-lattice audit, with repeated claims that the 4-core is near-top-decile but not optimal.
4. **Compression strategy:** Merge the interpretive prose into a compact "subset/lattice robustness" paragraph before the top-10 table; move script/CSV paths and distribution IQR into the table caption or appendix. Example after-state: "Across both audits, homoplasy/frequency/entropy dominate; the historical 4-core ranks 13/210 and 87/1023, while the 3-core is the stronger compact descriptive variant."
5. **Expected page saving:** 0.3-0.5 pp
6. **Expected score impact:** lift. It preserves the key adverse finding ("not optimum") while reducing audit fatigue.
7. **Risk:** low-medium

## Candidate 3 -- Ground-truth heterogeneity setup and conclusion

1. **Type:** trim-verbose / merge-paragraphs
2. **Current length:** ~115 prose words + long caption; ~0.25 pp
3. **What it currently does:** Lines 896-928 introduce the Layer A definition-type audit, show a table, and then restate that feature heterogeneity persists despite mostly immune-escape labels.
4. **Compression strategy:** Collapse the three-sentence setup and two-sentence conclusion into one sentence before the table and one sentence after it; move the "11 main + Zika" scope and HIV-1 count caveat into the caption only. Example after-state: "Layer A composition does not explain away method-pathogen dependence: all pathogens are >=71% immune_escape, yet five best-feature classes emerge and 10/12 immune-only restrictions preserve the best feature."
5. **Expected page saving:** 0.1-0.2 pp
6. **Expected score impact:** neutral-to-lift. The causal boundary becomes sharper, but the saving is modest.
7. **Risk:** low

## Candidate 4 -- EqualWeight protocol exposition in search-space reduction

1. **Type:** move-detail-to-footnote / table-ize-prose
2. **Current length:** ~230-word method paragraph; ~0.4 pp
3. **What it currently does:** Lines 934-940 re-explain production EqualWeight, nested-LOPO sign fitting, scripts, normalization, and why adaptive weighting was rejected.
4. **Compression strategy:** Replace the prose with a two-row protocol table or a one-sentence main-text contrast plus footnote for scripts and formula. Example after-state: "Production EqualWeight uses pre-defined orientations and 1/10 min-max averaging; nested-LOPO adds training-fold sign fitting and z-scoring. Their mean MCC differs by <=0.013, so sign fitting is not load-bearing."
5. **Expected page saving:** 0.2-0.4 pp
6. **Expected score impact:** lift. The distinction remains examiner-visible without burying the search-space result under implementation detail.
7. **Risk:** medium

## Candidate 5 -- Vaccine-escape validation table note, key findings, and circularity prose

1. **Type:** table-ize-prose / consolidate-duplicate / move-detail-to-footnote
2. **Current length:** ~590 words after the equation plus a dense table note; ~1.1 pp
3. **What it currently does:** Lines 948-987 present the enrichment table, Bonferroni/provenance notes, key findings, H3N2 self-consistency details, data-availability exclusions, Layer A circularity audit, and final search-space claim.
4. **Compression strategy:** Add compact columns or a small follow-on ledger with rows for HIV-1, H3N2, SARS-CoV-2, and "8 unavailable pathogens": role, circularity, corrected status, boundary. Move Bonferroni denominator arithmetic, pipeline filenames, and H3N2 site list to footnote/appendix. Example after-state: "HIV-1 is the external anchor; H3N2 is mainly self-consistency; SARS-CoV-2 is exploratory; the other eight pathogens lack comparable residue-level escape labels."
5. **Expected page saving:** 0.6-0.9 pp
6. **Expected score impact:** lift. This is the closest analogue to the audit-ledger win: it makes independence/circularity boundaries more legible while saving space.
7. **Risk:** medium

RESULT_COMPRESS_V2_J10: candidates=5 total_pages_saved=1.5-2.4 total_score_impact=+0.3
