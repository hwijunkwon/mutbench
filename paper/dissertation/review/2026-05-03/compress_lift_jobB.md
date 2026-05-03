# Compression-with-lift review -- Job B: ch2_background + ch3_methods

## 1. Candidates

### 1) ANOVA robustness and diagnostic tests block
- **File:line range:** `paper/dissertation/chapters_en/ch3_methods.tex:820-825`, `855-862`
- **What it currently does:** Gives Bayesian, Levene, Kruskal-Wallis, ART, multiple-testing, BCa, wild-cluster, phylogenetic-block, mixed-effects, jackknife, and Mantel/Procrustes details as long prose.
- **Compression strategy:** Convert to one compact "robustness frame / question / result / inference / archive" table, keep 3-4 sentences of prose for the load-bearing conclusion, and move "not performed" items to a limitations sentence or footnote.
- **Expected page saving:** 0.7-1.0 pages.
- **Expected score impact:** **lift** -- committee can grade the inferential defense faster; it also removes duplicated numerics already tabulated in `ch4_results.tex:481-493`.
- **Risk level:** Low-medium; preserve exact lower bounds and distinguish evaluation-level vs cell-level models.

### 2) Layer A heterogeneity repeated in prose and table note
- **File:line range:** `paper/dissertation/chapters_en/ch3_methods.tex:190-207`, `272-313`
- **What it currently does:** Defines Layer A/B/C, then repeats Layer A's heterogeneous criteria in the identification paragraph and again in the `tab:gt_positions` minipage note.
- **Compression strategy:** Add an "Evidence role / positive label / audit role / key limitation" mini-table for Layers A-C, then reduce the Layer A paragraph to a single operational definition plus a forward reference; delete the second heterogeneity note or make it a one-line table footnote.
- **Expected page saving:** 0.5-0.8 pages.
- **Expected score impact:** **lift** -- makes the ground-truth contract more findable and reduces the appearance of apologetic repetition.
- **Risk level:** Low; the content is already duplicated and can be consolidated without changing claims.

### 3) Detector families and parameter variants double table + prose restatement
- **File:line range:** `paper/dissertation/chapters_en/ch3_methods.tex:622-728`
- **What it currently does:** Provides one table for 14 families, one table for 39 parameter variants, then restates five category groupings in prose.
- **Compression strategy:** Merge family, category, variants, and parameter values into one table; trim category prose to one sentence explaining why detection family is modeled rather than variant.
- **Expected page saving:** 0.8-1.2 pages.
- **Expected score impact:** **lift** -- the reader can inspect the full detector grid in one place and the ANOVA factor choice becomes clearer.
- **Risk level:** Medium; merged table may be wide, so use `tabularx`/small font or split into two blocks inside one table.

### 4) PLM channel correlation prose after table
- **File:line range:** `paper/dissertation/chapters_en/ch3_methods.tex:571-604`
- **What it currently does:** Explains ESM-2/Tranception proxy status, reports correlation ranges and HIV-1 exception, then the table caption/minipage repeats backbone, archive, and sensitivity caveats.
- **Compression strategy:** Keep a 2-sentence prose lead and let the table carry correlation evidence; move archive/script names to the table footnote and cut duplicate "near-equivalent for 11 of 12" phrasing.
- **Expected page saving:** 0.3-0.5 pages.
- **Expected score impact:** **lift** -- preserves the collinearity caveat while reducing a defensive tone.
- **Risk level:** Low; table already contains the evidence.

### 5) Per-pathogen biological context as a dense 11-pathogen paragraph
- **File:line range:** `paper/dissertation/chapters_en/ch3_methods.tex:21-35`
- **What it currently does:** Lists all pathogens by transmission class, then adds a long paragraph of five biological rationales plus DMS/Zika notes.
- **Compression strategy:** Add 2-3 columns to `tab:pathogen_data` or a short "panel rationale" table with pathogen group, biological stressor, and benchmark implication; reduce prose to "The panel was selected to span X/Y/Z."
- **Expected page saving:** 0.4-0.7 pages.
- **Expected score impact:** **lift** -- committee members can map pathogen choice to benchmark rationale without parsing a 110-word sentence.
- **Risk level:** Low-medium; avoid overloading the already-wide sequence table.

### 6) Reproducibility/license procedural detail in main text
- **File:line range:** `paper/dissertation/chapters_en/ch3_methods.tex:914-935`
- **What it currently does:** Mixes code availability, seeds, library versions, license compatibility, and external-resource license summaries in the main chapter flow.
- **Compression strategy:** Keep one reproducibility paragraph plus a compact license/resource table; push library versions and exact provenance paths to footnote/supplement because `environment.yml`, `requirements-pinned.txt`, and provenance CSVs are the authoritative records.
- **Expected page saving:** 0.5-0.9 pages.
- **Expected score impact:** **neutral to lift** -- defense quality improves if the main text stops reading like a release manifest, but legal/license claims must remain auditable.
- **Risk level:** Medium; license statements are sensitive, so do not delete the no-redistribution and non-commercial-resource boundaries.

### 7) ch2 benchmarking-gap prose duplicates its comparison table
- **File:line range:** `paper/dissertation/chapters_en/ch2_background.tex:233-260`, `262-282`
- **What it currently does:** Lists ProteinGym, ViroGym, ConDor, Pons, SARS-CoV-2 studies, then follows with a cross-benchmark table that partially repeats task/scope distinctions.
- **Compression strategy:** Expand `tab:benchmark_comparison` by one "Why not sufficient for hotspot detection" column and reduce the preceding prose list to 3 sentences.
- **Expected page saving:** 0.4-0.6 pages.
- **Expected score impact:** **lift** -- the benchmarking gap becomes easier to grade because the table shows exactly why adjacent benchmarks do not answer the dissertation's task.
- **Risk level:** Low.

### 8) ch2 PLM/tutorial background overlaps method-specific PLM caveats
- **File:line range:** `paper/dissertation/chapters_en/ch2_background.tex:127-156`, plus method-specific echo at `ch3_methods.tex:571-574`
- **What it currently does:** Teaches ESM-2, Tranception, ProtTrans/ESM-3, EVEscape, AlphaMissense, then later repeats implementation caveats in methods.
- **Compression strategy:** Keep ch2 at literature-landscape level; move implementation caveats (ESM-3 license exclusion, EVEscape proxy, Tranception proxy) to ch3 only or summarize them in a compact "Used in MutBench?" table.
- **Expected page saving:** 0.3-0.5 pages.
- **Expected score impact:** **neutral to lift** -- background becomes less tutorial-like and methods remains the source of implementation truth.
- **Risk level:** Low-medium; ESM-3 exclusion is a defense point, so retain it somewhere.

### 9) Stage 3 information-integration method paragraph
- **File:line range:** `paper/dissertation/chapters_en/ch3_methods.tex:903-912`
- **What it currently does:** Packs 10 features, EqualWeight variants, three ablations, RF settings, 11-vs-12 pathogen distinction, and vaccine-escape validation into one dense paragraph/list.
- **Compression strategy:** Convert to a small "analysis / input / output / reported in" table and push RF hyperparameters to a footnote or parenthetical in the results table caption.
- **Expected page saving:** 0.2-0.4 pages.
- **Expected score impact:** **lift** -- makes Stage 3 scope and outputs easier to locate.
- **Risk level:** Low.

## 2. Top 3 recommended

1. **ANOVA robustness and diagnostic tests block (`ch3_methods.tex:820-825`, `855-862`)** -- best compression-with-lift target because it is dense, table-shaped, and partly duplicated by the results diagnostics table.
2. **Detector families + parameter variants (`ch3_methods.tex:622-728`)** -- largest clean page saving; one merged table would improve the reader's understanding of the 14-family/39-variant design.
3. **Layer A/B/C definitions and Layer A heterogeneity (`ch3_methods.tex:190-207`, `272-313`)** -- high defense payoff because the ground-truth contract is central and currently dispersed/repeated.

Estimated top-3 page saving: **2.0-3.0 pages**. Expected score impact: **+0.2 to +0.3** if edited carefully, because the cuts improve gradeability rather than merely shortening.

## 3. Sample compressed prose for #1 candidate

Replace the diagnostic prose with:

> The headline scoring-by-pathogen interaction was stress-tested under five inferential frames, summarized in Table X. All frames keep the lower bound or point estimate above Cohen's large-effect threshold ($\omega^2 > 0.14$): cluster bootstrap $[0.195,0.333]$, wild-cluster $[0.201,0.303]$, phylogenetic block $[0.202,0.346]$, mixed-effects pseudo-$\omega^2=0.340$, and Bayesian factor analysis mean $0.316$ with HDI $[0.242,0.388]$. Levene and Shapiro diagnostics reject ideal ANOVA assumptions, so the parametric ANOVA is interpreted through these cluster-aware and distribution-robust checks rather than through naive row-level independence. Kruskal-Wallis and ART checks support the same direction but are secondary because Kruskal-Wallis does not test the interaction directly and ART is rank-scale. No ANOVA family-wise correction is applied because the model decomposes pre-specified variance components; Fisher tests in the vaccine-escape audit use the separate 780-combination Bonferroni denominator.

RESULT_JOBB: candidates=9 top3_pages_saved=2.5 top3_score_impact=+0.3
