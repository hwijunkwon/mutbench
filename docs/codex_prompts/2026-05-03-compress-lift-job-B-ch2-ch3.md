# Compression-with-lift review — Job B: ch2_background + ch3_methods

Execute the review NOW. Read-only. Write only the final report.

You are looking for compression opportunities that ALSO improve readability /
defense quality, following the recent audit-ledger pattern that lifted score
+0.6 while cutting 7 pages.

## Scope

- `paper/dissertation/chapters_en/ch2_background.tex` (active via ch1:54 input)
- `paper/dissertation/chapters_en/ch3_methods.tex`

## Pattern to find

Dense prose with parallel items → compact table + trimmed prose. Lifts score
by (a) making evidence findable, (b) reducing repeated caveats, (c)
improving committee gradeability.

Look for:

1. **Table-izable lists**: prose enumerations of N parallel items
   (scoring formulas, detector families, pathogens, evidence types, etc.)
2. **Repeated caveats**: same limit/qualifier in multiple places
3. **Long single sentences** (100+ words)
4. **Footnote-tier in main text** (file paths, library versions, procedural notes)
5. **Redundant cross-references**
6. **Tutorial-style background that overlaps the introduction**
7. **Method-spec restated in result chapters** (already partly cleaned in cycle 6)

For each candidate, give:
- File:line range
- What it currently does (1 sentence)
- Compression strategy
- Expected page saving
- Expected score impact: lift / neutral / drop (with reasoning)
- Risk level: low / medium / high

## Specific known patterns to check

- `ch3_methods.tex` ANOVA Diagnostic Tests block (line 805-825 area) was
  partially trimmed in ch5 — check if ch3 and ch4 still duplicate
- detector families table + parameter variants — long enumeration?
- ground truth Layer A/B/C definitions — how many places?
- 11-pathogen biology rationale — already partially compressed; check residue
- PLM channel correlation table prose — could it be tighter?

## Expected output

Write report to:
  `/proj/paper/paper/dissertation/review/2026-05-03/compress_lift_jobB.md`

Structure:
1. List of 5-10 candidates
2. Top 3 recommended
3. Sample compressed prose for the #1 candidate (≤ 200 words)
4. End with one-line:
   `RESULT_JOBB: candidates=<n> top3_pages_saved=<n> top3_score_impact=<+x.x|0|-x.x>`

Length budget: ≤ 2200 words. Do not commit.
