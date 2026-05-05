# Easy Guide v2 Major Fix Changelog

Target: `paper/dissertation/dissertation_easy_guide_v2.md`  
PDF: `paper/dissertation/dissertation_easy_guide_v2.pdf`  
Date: 2026-05-05

## Summary

Applied all 28 Major fixes from the 9 chunked audits. Main changes:

- Standardized Layer C as the primary wet-lab functional anchor: 6/11 pathogens, 650 positions, best MCC 0.139-0.322; EV-A71 0.322 and H3N2 0.245 strongest.
- Standardized HIV-1 vaccine-escape external anchor: 7.19x, p_adj=2.5e-16, 82% Layer-A-disjoint, 37/45 novel.
- Standardized omega-squared anchor: scoring x pathogen omega^2=0.296, 95% CI [0.201, 0.346].
- Reframed practical-value language toward wet-lab experiment prioritization/search-space reduction.
- Corrected stale/internal numerical claims and fragile figure/table cross-references.
- Replaced emoji status markers with PDF-safe text.

## Per-Chunk Major Fixes

### p1-5

Addressed 3/3 Major:

- Added Layer C DMS anchor to the opening summary and early DMS discussion.
- Added omega^2 CI [0.201, 0.346] at first technical mentions.
- Expanded the HIV-1 7.19x anchor with p_adj=2.5e-16, 82% Layer-A-disjoint, 37/45 novel.
- Also replaced "실용 가능성" style wording with wet-lab candidate-prioritization framing and added MCC=0 random-level explanation.

### p6-10

Addressed 1/1 Major:

- Replaced "실용적 검증" table language with wet-lab experiment-prioritization evidence and added the Layer C 6/11, 650-position anchor.
- Also clarified Layer C availability in the overview figure caption.

### p11-15

Addressed 3/3 Major:

- Updated Table 9 Layer C counts to current v229/CSV values: SARS-CoV-2 247, H3N2 112, HIV-1 48, RSV 101, Rabies 87, EV-A71 55, total 650.
- Replaced the SARS-CoV-2 "only pathogen with all three GT layers" claim with "most data-rich/well-validated reference pathogen."
- Added Layer C practical wet-lab anchor near the Layer C definition and Table 9.
- Also revised Figure 2 caption to include orange Layer C and softened "생물학적 사실" to experimental-condition functional evidence.

### p16-20

Addressed 3/3 Major:

- Fixed Stage 1 count mismatch from 5 to 6 experiments.
- Fixed method-count mismatch by describing the displayed set as 5 representative detection methods.
- Added omega^2 CI [0.201, 0.346] near ANOVA explanation and Layer C anchor near DMS F1.

### p21-25

Addressed 4/4 Major:

- Corrected false "all sequence counts exceed 1,000" statement; now notes EV-A71/MERS low-sample exceptions and separates total vs unique ranges.
- Corrected "11/11 unique optimal combinations" to 10/11, noting Flu-B and MERS share freq + KDE(p=85).
- Replaced fragile Table/Figure numbering references with "아래 표/그림" where numbering drifted.
- Added Layer C anchor near DMS/practical validation material.

### p26-30

Addressed 4/4 Major:

- Corrected the Layer A vs Layer C comparison prose from 5/6 to 6/6 differing optima and added the Layer C 650-position wet-lab anchor.
- Recomputed/relabelled the FUBAR BF table against current `stage3_full_results.csv` as best-detector-per-FUBAR performance; updated MCC/rank values.
- Replaced fragile figure/table number references with unnumbered wording.
- Added full HIV-1 anchor context in the Stage 2 summary and vaccine-escape section.
- Simplified the robustness paragraph by keeping the current valid citation text and removing stale broken-reference risk from the audit target.

### p31-35

Addressed 4/4 Major:

- Added Layer C DMS as the primary wet-lab anchor at the start of the practical validation section.
- Fixed the Stage 2 MCC vs Stage 1 hotspot-score wording: bootstrap CI [0.323, 0.635] is now clearly labelled Stage 1 MutClust-Hybrid hotspot-score.
- Clarified region-window numbers: Chapter 5 now uses the Table 29 11-pathogen oracle means (0.341 -> 0.472 -> 0.454), not unsupported 0.712.
- Reformatted the PAHD-R mode table to reduce right-margin clipping by dropping Coverage/status columns from the table and moving them to prose.

### p36-40

Addressed 4/4 Major:

- Resolved relaxed-MCC contradiction by aligning narrative to Table 29 mean +/-10 MCC 0.454.
- Replaced stale v98 "Layer A optimal = escape optimal" claim with v229 hierarchy: HIV-1 clean external validation, H3N2 self-consistency, SARS-CoV-2 exploratory.
- Added Layer C wet-lab triage anchor in Chapter 6/conclusion material.
- Completed HIV-1 anchor wherever it functions as the final take-home.
- Fixed "Table 24" to "Table 30."

### p41-42

Addressed 2/2 Major:

- Added final-state omega^2 anchor with CI [0.201, 0.346].
- Replaced generic "7-9x escape" with bounded HIV-1 primary external anchor plus H3N2/SARS caveat.
- Also clarified 0/12 callable vs n=11 scope and made Layer C total 650 positions explicit.

## Minor / Visual Fixes Applied

- Minor fixes applied: 8/55, limited to low-risk edits adjacent to major fixes.
- Visual fixes applied: 4/23, limited to text/caption/table-source fixes that do not require LaTeX rebuild engineering.
- Emoji/glyph fix: replaced PASS/GREEN emoji markers with ASCII text and changed p_adj notation to `2.5e-16` after XeLaTeX warned about missing superscript glyphs in the selected font.

## Deviations

- No Major item was skipped.
- Visual-only page-flow issues that require LaTeX/table-engineering rebuild work were not pursued beyond source-text/table simplifications, per instruction.
- Pandoc still warns that several pre-existing figure paths under `figures/` are missing and are replaced by descriptions. This is unchanged from source assets and not caused by the major-fix edits.

## PDF Rebuild Status

- Command run from `paper/dissertation`:
  `pandoc dissertation_easy_guide_v2.md -o dissertation_easy_guide_v2.pdf --pdf-engine=xelatex -V CJKmainfont="Noto Serif CJK KR" -V mainfont="Noto Serif CJK KR" -V geometry:margin=1in`
- Status: built
- Pages: 43
