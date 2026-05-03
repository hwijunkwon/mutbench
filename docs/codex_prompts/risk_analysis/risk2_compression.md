# Risk Analysis 2 — Aggressive compression candidates (Ch1–Ch5)

Execute the analysis NOW. Read-only. Do not commit.

## Context

The dissertation (215pp) will be repositioned as a **wet-lab triage tool**, not a deployable detector benchmark. Under this reframe, **detail that supports the deprecated "we tried to build a detector and failed" narrative becomes redundant** — it can collapse into ledger rows that already exist.

The compression target is now **215pp → 185–195pp (−20 to −30pp)**, not the conservative −10pp originally drafted.

## 15 candidate blocks (verify each)

For EACH block: (a) does an existing table/algorithm/ledger preserve all numerical claims? (b) what is lost? (c) verdict: safe / guarded / unsafe / keep.

### Ch1 (`chapters_en/ch1_introduction.tex`, 207 lines, ~16pp)

| # | Block | Lines | Compression target |
|---|---|---|---|
| 1 | Research Background (overlap with Ch2) | 5–55 | trim to 1–2pp by deleting Ch2-redundant prior-art prose |
| 2 | Research Objectives (long enumeration) | 76–157 | compress 6pp → 3pp by collapsing sub-objectives into 3 numbered contributions |
| 3 | Research Contributions (need reframe to triage) | 158–195 | rewrite to lead with C1=triage, similar length |

### Ch2 (`chapters_en/ch2_background.tex`, 299 lines, ~23pp)

| # | Block | Lines | Compression target |
|---|---|---|---|
| 4 | DBSCAN/HDBSCAN methods detail | 59–87 | 2.5pp → 1pp (cite only) |
| 5 | PLM survey (EVE/EVEscape/Tranception/EVEREST) | 124–166 | 3.5pp → 2pp (group, fewer per-method paragraphs) |
| 6 | Feature Importance analysis (Maher 2022 etc.) | 187–209 | 2pp → 1pp |

### Ch3 (`chapters_en/ch3_methods.tex`, 892 lines, ~68pp)

| # | Block | Lines | Compression target |
|---|---|---|---|
| 7 | Methods overview (Framework) | 78–144 | 5pp → 3pp (collapse pipeline diagrams to text) |
| 8 | **Stage 1 SARS-CoV-2 methods (now sanity check, not core)** | 338–487 | 11pp → 6pp (since Stage 1 demoted under triage reframe) |
| 9 | Statistical Design narrative (ANOVA/bootstrap setup) | 721–854 | 10pp → 7pp (keep equations, trim prose) |
| 10 | Code/Data licenses table prose | 866–892 | 2pp → 1pp |

### Ch4 (`chapters_en/ch4_results.tex`, 989 lines, ~76pp)

| # | Block | Lines | Compression target |
|---|---|---|---|
| 11 | **Single-Pathogen Stage 1 results (sanity check)** | 18–115 | 7pp → 4pp |
| 12 | Robustness/Sensitivity (H3N2 temporal + sliding-window) | 117–198 | 6pp → 3pp |
| 13 | Cross-Pathogen Structural Validation (5.92x, z=13.34) | 200–219 | 2pp → 1pp |
| 14 | Cold-Start algorithm + audit ledger prose | 706–893 | 14pp → 8pp (table+ledger preserve numerics) |
| 15 | ANOVA 5-frame triangulation prose | 485–538 | 4pp → 2pp |
| 16 | Per-pathogen biology rationale | 308–330 | 2pp → 1pp |
| 17 | Information-Type / per-feature analysis | 624–700 | 6pp → 4pp |
| 18 | **Cycle 7B six paradigms** | 863–890 | 3.5pp → 1pp (table preserves; prose to 1 sentence) |
| 19 | Subset selection 210-combo + Full-lattice + Shapley prose | 795–833 | 3.5pp → 1.5pp |

### Ch5 (`chapters_en/ch5_discussion.tex`, 340 lines, ~26pp)

| # | Block | Lines | Compression target |
|---|---|---|---|
| 20 | Cross-Pathogen Generalization (now reframed) | 63–122 | 5pp → 3pp |
| 21 | Future Research Directions (Priority 1–5) | 260–294 | 3pp → 1.5pp |

**Total potential**: ~−30pp (215pp → ~185pp). Realistic execution target with safety margin: **−20 to −25pp** (215pp → 190–195pp).

## Numbers that MUST appear somewhere after compression

- ω² = 0.296 cluster CI [0.201, 0.346]; 5-frame robustness lower bounds
- Friedman χ² = 7.69, p = 0.990
- LOPO 0/11, gap 0.265
- HBFWS p = 0.78
- Cycle 7B all 6 paradigms p ≥ 0.56
- HIV-1 7.19× (p_adj=2.5e-16, 82% disjoint), H3N2 9.36×, SARS 7.63×
- 4-core MCC 0.081 vs full-10 0.070, rank 87/1023, 3-core rank 27
- P5 0/12 callable
- Wave 4 8/12 positive p=0.368
- Wave 5 MCC −0.055, 2/10
- Stage 1 HS 0.778 / GISAID 0.383
- 8,580 evaluations = 11×20×39
- 11 pathogens / 530–5019 unique seqs / 261–1330 AA / 0.7–15.9% positive rate

## Question

For all 21 blocks above:

1. Per-block table: **lines → target lines, table preserved? what's lost? verdict (safe/guarded/unsafe/keep)**.
2. Identify any block where the compression would cause a **load-bearing** loss not absorbable by existing tables.
3. Recommend a **realistic** compression target between 185pp and 200pp; explain trade-offs.
4. Suggest the **execution order** — which blocks first (lowest risk → highest risk).
5. List blocks that should NOT be compressed at all (and why).

## Output

`paper/dissertation/review/2026-05-03/risk2_compression_analysis.md`

End with:
- Block-by-block table (21 rows)
- Total estimated savings
- Recommended execution order
- One-line: `RESULT_RISK2: safe=<n> guarded=<n> unsafe=<n> keep=<n> total_pp_savings_min=<n> total_pp_savings_max=<n> recommended_target_pp=<n>`

Length budget: ≤ 3000 words.
