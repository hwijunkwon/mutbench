# Compression-with-lift review — Job D: ch5_discussion

Execute the review NOW. Read-only. Write only the final report.

You are looking for compression opportunities that ALSO improve readability /
defense quality. Ch5 was already partially compressed (Bolker 5-frame
restatement collapsed; Wave 1-3/4/5 paragraph split; defense map added)
— find what's LEFT to compress beyond that.

## Scope

- `paper/dissertation/chapters_en/ch5_discussion.tex` (post-compression state)

## Already done (do not re-recommend)

- Wave 1-3 / Wave 4 / Wave 5 paragraph split
- Bolker 5-frame restatement → 1 sentence cross-reference
- "establishes practical relevance" softened
- LOPO spoken-answer integrated
- Layer A provenance summary table added (`tab:layer_a_provenance`)
- Defense map table added (`tab:defense_map`)
- Falsification criteria paragraph removed
- Reproduction-tolerance 2 sentences removed
- v176 pilot Tier 1/2 detail compressed
- Layer A curation-reproducibility limitations paragraph added

## Pattern to find

Same compression-with-lift pattern. Look for:

1. **Future-work programme section** — long Tier 1/Tier 2/Tier 3 / Wave 4/5
   discussion + roadmap table; could narrative be tighter?
2. **Limitations subsections** — Layer A heterogeneity, Bolker, ESM leakage,
   GISAID, MAFFT, sliding-window are spread across multiple subsections;
   could they consolidate to a single limitations table?
3. **Code/data availability + numerical artifacts** sections (post line ~340) —
   long prose listings
4. **Dual-use considerations** — could it be tighter without losing
   responsible-stewardship signaling?
5. **Take-home message + Concluding Remarks** — overlapping content?
6. **Pathogen-aware adaptive method selection** — long paragraph with v176
   pilot + Wave 4/5 + future-test rule. Already partly compressed;
   check residue.
7. **Multi-source feature integration** subsections that overlap with
   Ch4 results

For each candidate:
- File:line range
- What it currently does
- Compression strategy
- Expected page saving
- Expected score impact: lift / neutral / drop
- Risk level

## Expected output

Write report to:
  `/proj/paper/paper/dissertation/review/2026-05-03/compress_lift_jobD.md`

Structure:
1. List of 5-10 candidates
2. Top 3 recommended
3. Sample compressed prose for the #1 candidate (≤ 200 words)
4. End with one-line:
   `RESULT_JOBD: candidates=<n> top3_pages_saved=<n> top3_score_impact=<+x.x|0|-x.x>`

Length budget: ≤ 2200 words. Do not commit.
