# Compression-check v2 Job 2 -- Chapter 1 lines 101--207

Scope reviewed: `paper/dissertation/chapters_en/ch1_introduction.tex:101-207`.

Already-applied items skipped: the panel-scope summary box/table at lines 90--105 is already present, so it is not re-recommended. The external-validation ledger at lines 175--190 is also treated as already implemented in this chunk, not as a new table-ization candidate.

## Candidate 1 -- Research-overview prose duplicates the figure and caption

1. **Type:** consolidate-duplicate / trim-verbose
2. **Current length:** ~170 words across the lead sentence, TikZ node text, and caption; ~0.25--0.35 pp including caption footprint.
3. **What it currently does:** It states the same four-step logic three times: frequency/entropy limitation, MutBench comparison, pathogen-dependent optimum, and HIV-1 vaccine-escape validation.
4. **Compression strategy:** Keep the figure nodes as the visual summary, reduce the lead-in and caption to functional text. Example after-state: "Figure~\ref{fig:research_overview} maps the study from the information-source gap to MutBench, the pathogen-dependent interaction result, and HIV-1 external validation."
5. **Expected page saving:** 0.1--0.2 pp.
6. **Expected score impact:** lift: the figure will feel less like repeated prose and more like a guidepost; no evidence is removed.
7. **Risk:** low.

## Candidate 2 -- Contribution 1 is a methods catalog in prose

1. **Type:** table-ize-prose / trim-verbose
2. **Current length:** ~190--220 words; ~0.4 pp.
3. **What it currently does:** It combines novelty claim, scale, comparator boundary, scoring taxonomy, ground-truth layers, hotspot-score metric, and three experimental stages in two long paragraphs.
4. **Compression strategy:** Replace the second paragraph with a compact component ledger: component, scope, role. Example after-state: "MutBench has four components: 20 formulas across 6 information categories; three-layer ground truth; hotspot-score; Stage 1/2 main benchmark plus Stage 3 integration."
5. **Expected page saving:** 0.2--0.3 pp.
6. **Expected score impact:** lift: the architecture becomes easier to inspect, and the broadest-benchmark claim remains separate from implementation inventory.
7. **Risk:** low.

## Candidate 3 -- Contribution 2 stacks result, examples, and caveats

1. **Type:** move-detail-to-footnote / merge-paragraphs
2. **Current length:** ~170--200 words; ~0.35--0.45 pp.
3. **What it currently does:** It reports the interaction result, 9 best scoring types, examples, Friedman null, LOPO 0/11, cluster-bootstrap CI, 6-category lower bound, small-cluster warning, and evidentiary hierarchy.
4. **Compression strategy:** Keep the hierarchy in the main text and move the Bolker rule-of-thumb detail to a footnote or limitations cross-reference. Example after-state: "The primary evidence is the scoring-by-pathogen interaction; Friedman and 9 distinct optima support no universal winner, while LOPO 0/11 is treated only as null-consistent corroboration."
5. **Expected page saving:** 0.2--0.3 pp.
6. **Expected score impact:** lift: reduces caveat overload while preserving the defensible claim boundary around LOPO.
7. **Risk:** medium, because the small-cluster caution is defense-relevant and must remain accessible.

## Candidate 4 -- Objective tail repeats scope and robustness boundaries

1. **Type:** consolidate-duplicate
2. **Current length:** ~90--120 words in lines 105--109; ~0.15--0.25 pp.
3. **What it currently does:** It repeats the 11-pathogen headline-scope rule immediately after the panel-scope ledger and embeds the 4-feature robustness check inside the third objective.
4. **Compression strategy:** Move "headline claims belong to the 11-pathogen main panel" into the table note/caption and shorten the third objective to the external validation aim. Example after-state: "Externally validate search-space reduction on independently curated vaccine-escape positions, prioritising Layer-A-disjoint sites."
5. **Expected page saving:** 0.1--0.2 pp.
6. **Expected score impact:** neutral to lift: removes repetition created by the new panel ledger; the robustness check still appears in Contribution 3 and Chapter 4.
7. **Risk:** low.

## Candidate 5 -- Dissertation organization is an inventory, not a reader map

1. **Type:** table-ize-prose / trim-verbose
2. **Current length:** ~210--240 words; ~0.45--0.55 pp.
3. **What it currently does:** It lists each chapter and then enumerates many internal sections and analysis types that the table of contents already supplies.
4. **Compression strategy:** Convert to a four-row organization table with columns: unit, purpose, main evidence. Example after-state: "Chapter 3 reports validation, robustness, cross-pathogen benchmark, and information-type analyses; Chapter 4 interprets limits and future work."
5. **Expected page saving:** 0.25--0.35 pp.
6. **Expected score impact:** neutral to lift: lowers end-of-introduction fatigue with little evidentiary downside.
7. **Risk:** low.

## Total

Estimated total saving if all five are applied conservatively: **0.9--1.35 pages**. Expected score impact is a modest **+0.3**, mostly from readability and better claim hierarchy rather than new evidence.

RESULT_COMPRESS_V2_J2: candidates=5 total_pages_saved=1.1 total_score_impact=+0.3
