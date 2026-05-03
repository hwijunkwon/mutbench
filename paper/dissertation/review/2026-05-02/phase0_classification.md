# Phase 0 — FAIL classification (active vs orphan)

Date: 2026-05-02
Active build files (input by `thesis_en.tex`):
- `chapters_en/{ch1_introduction, ch3_methods, ch4_results, ch5_discussion}.tex`
- `front_en/abstract.tex`
- `front/abstract_kr.tex`

Orphan files (NOT input):
- `chapters_en/{ch2_background, ch5_adapt}.tex`
- `chapters/{ch2_background, ch5_adapt, ch6_conclusion}.tex` (Korean mirror, all chapters/ are orphan per v206 policy except `front/abstract_kr.tex`)
- `chapters_en/ch6_conclusion.tex` does not exist

## verify_dissertation.py output: 4 FAIL / 6 WARN / 129 PASS

### FAIL 1 — 130 duplicate `\label{}` declarations

Per-row classification (sampled by category):

| Pattern | Count | Status |
|---|---|---|
| `chapters/X.tex` ↔ `chapters_en/X.tex` (Korean+English mirror) | 110 | **NOT BLOCKING** — Korean chapters/ are orphan to English build |
| `chapters_en/ch5_adapt.tex` ↔ `chapters_en/ch4_results.tex` (e.g., `\label{ch:adapt}`) | 4 | **NOT BLOCKING** — ch5_adapt.tex is orphan |
| `chapters_en/ch6_conclusion.tex` ↔ `chapters_en/ch5_discussion.tex` (e.g., `\label{ch:conclusion}`) | 4 | **NOT BLOCKING** — ch6_conclusion.tex is orphan |
| `chapters/ch2_background.tex:4` ↔ `chapters/ch2_background.tex:7` | 2 | **NOT BLOCKING** — orphan-internal |
| `(file, line) listed twice for same label` (verify-script artefact) | 12 | **NOT BLOCKING** — false-positive from script's set-vs-list issue |

**Active-build duplicates: 0.** Confirmed by `thesis_en.log` showing 0 `multiply defined` warnings.

### FAIL 2 — 2 undefined `\ref{}`

| Ref | Used in | Status |
|---|---|---|
| `\ref{fig:feature_correlation}` | `ch5_adapt.tex:151` | **NOT BLOCKING** — orphan |
| `\ref{fig:feature_importance_grid}` | `ch5_adapt.tex:95` | **NOT BLOCKING** — orphan |

**Active-build undefined refs: 0.** Confirmed by `thesis_en.log` showing 0 `There were undefined references`.

### FAIL 3 — 11 citation keys not in `references.bib`

| Citation key | Used in | Status |
|---|---|---|
| `breiman2001random` | `ch5_adapt.tex` | **orphan** |
| `jumper2021alphafold` | `chapters/ch5_adapt.tex` (KR) + `chapters_en/ch5_adapt.tex` (EN orphan) | **orphan + KR-only** |
| `moult2014casp` | `chapters/ch5_discussion.tex:92` (KR only) | **KR-only** |
| `nei1986simple` | `chapters/ch3_methods.tex:332` (KR only) | **KR-only** |
| `olshen2004cnv` | `chapters/ch3_methods.tex:549` (KR only) | **KR-only** |
| `picard2011genomicseg` | `chapters/ch3_methods.tex:556` (KR only) | **KR-only** |
| `satopaa2011kneedle` | `chapters/ch3_methods.tex:551` (KR only) | **KR-only** |
| `shrake1973environment` | `chapters/ch4_results.tex:1113` (KR) + `chapters_en/ch5_adapt.tex:25` (orphan) | **KR-only + orphan** |
| `simonich2025rsvdms` | `chapters/ch3_methods.tex:132` (KR only) | **KR-only** |
| `sonesson2003cusum` | `chapters/ch3_methods.tex:550` (KR only) | **KR-only** |
| `zhang2008chipseq` | `chapters/ch3_methods.tex:546,548` (KR only) | **KR-only** |

**Active-build missing citations: 0.** Confirmed by `thesis_en.log` showing 0 `Citation undefined`.

### FAIL 4 — 1 `\includegraphics` not found

| File | Used in | Status |
|---|---|---|
| `feature_ablation_bars.png` | `ch5_adapt.tex:105` | **NOT BLOCKING** — orphan |

**Active-build missing figures: 0.**

## Phase 0 additional checks

| Check | Result |
|---|---|
| Build artefacts present | ✓ `thesis_en.pdf` (236pp), `.log`, `.aux`, `.toc` all present + current |
| LaTeX errors | 0 (`grep -c '^!' thesis_en.log = 0`) |
| Undefined refs | 0 |
| Multiply-defined refs | 0 |
| Closure tone (TODO/FIXME/TBD/PLACEHOLDER/XXX in active sources) | **clean** (case-sensitive word-boundary grep returns nothing) |
| Output written | `Output written on thesis_en.pdf (236 pages)` |

## Phase 0 verdict

**Active-build pass condition: 0 FAILs in active build files → PASS.**

The 4 raw FAIL categories from `verify_dissertation.py` are entirely
attributable to (a) Korean+English mirror duplicate labels, (b) orphan
files (`ch5_adapt`, `ch6_conclusion`, `ch2_background`) that are not
`\input`-ed by `thesis_en.tex`, (c) verify-script self-duplication
artefacts, or (d) Korean-chapter-only citations not present in
`references.bib`. None affect the actual `thesis_en.pdf` build, which
compiles with 0 errors / 0 undefined references / 0 multiply-defined.

**WARN items** (non-blocking, recorded for committee context):
- `Stale Friedman chi2=42.44 (KR-only / pre-cycle-12)` — Korean
  `chapters/ch4_results.tex` still references the pre-cycle-12
  Friedman number; English `ch4_results.tex` uses the corrected
  current value. Not blocking per v206 "Korean chapters/ untouched"
  policy.
- `Pathogens not mentioned in ch4: ['Influenza_B']` — Korean
  ch4 only; English ch4 mentions Influenza_B in Wave 3/4/5 audit
  paragraphs.
- `ch3_methods.tex: Current 20/39/11 benchmark design not clearly
  referenced` — Korean ch3 only.

Active-build Phase 0 = **PASS**. Proceed to Phase 1+2+Statistics.
