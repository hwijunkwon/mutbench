# Codex deep compression strategy — dissertation length reduction

Execute the analysis NOW. Read-only. Write only the final report.

The dissertation is 241 pages, which the author considers too long. A previous
moderate-compression attempt (Option B) only achieved -2 pages because LaTeX
reflow doesn't translate word reduction into proportional page reduction.

## Required reading

- Active build files: `paper/dissertation/chapters_en/{ch1, ch3, ch4, ch5_discussion}.tex`,
  `paper/dissertation/front_en/abstract.tex`, and `chapters_en/ch2_background.tex`
  (which is `\input` from ch1:54)
- Cycle 6 deeper finding: length axis grade 7.4/10 (lowest of 8 axes); top
  remaining gap: late Ch4/Ch5 audit paragraphs read as audit logs
- Cycle 6 J1 finding: "complete but overloaded"

## Task

Produce a **deep compression strategy** that targets 215-225 pages (-15 to
-25 pages) WITHOUT removing scientific evidence. Specifically:

### 1. Page-by-page audit

Skim all chapters and identify the 10-20 highest-yield compression candidates.
For each, give:
- File:line range
- Current length (estimated words and page fraction)
- What it does (scientific role)
- Compression strategy: trim / table-ize / move-to-appendix / merge-paragraphs / delete
- Expected page saving
- Risk of evidence loss (low/medium/high)

### 2. Structural moves

Beyond per-paragraph compression, consider:
- Moving some chapters/sections to an Appendix
- Converting long prose enumerations to tables (which take less page than equivalent prose)
- Removing repeated caveats (Layer A heterogeneity, Bolker small-n, etc. that appear in 4+ places)
- Consolidating numerical-claim CSV pointers to one provenance footnote
- Merging closely-related paragraphs

### 3. Specific risk assessment

For each major compression target:
- What evidence is at risk if compressed
- What defense question becomes harder to answer if removed
- Whether the same content already exists elsewhere (potential dedup)

### 4. Recommended plan

Concrete sequence of compressions ranked by yield/risk ratio. Include:
- Target page count
- Estimated total page saving
- Wall time to apply (assume one experienced editor)
- Items to keep as-is

### 5. Aggressive compression option (if user is willing)

What additional compressions are possible if user accepts moving some
content to a single \appendix at end, accepting committee may flag
"why is this in appendix?" — name specific sections.

## Output

Write report to:
  `/proj/paper/paper/dissertation/review/2026-05-03/codex_compression_strategy.md`

Structure:
1. Page-by-page audit table (10-20 rows)
2. Structural moves analysis
3. Risk assessment
4. Recommended plan with target page count + wall time
5. Aggressive option

Length budget: ≤ 3000 words. Do not commit. Use neutral terminology.
