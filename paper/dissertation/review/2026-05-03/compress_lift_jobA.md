# Compression-with-lift review -- Job A: abstract + Chapter 1

## 1. Candidates

### 1. Abstract results block as an evidence ledger
- **File:line range:** `paper/dissertation/front_en/abstract.tex:10-13`
- **What it currently does:** Reports Stage 1, Stage 2, LOPO, vaccine-escape enrichment, feature-ablation, negative abstention, and information-type examples as dense prose.
- **Compression strategy:** **Table-ize** into a 4-row "main evidence ledger" with columns: claim, statistic, boundary/limitation, defense role; keep one lead sentence before and one synthesis sentence after.
- **Expected page saving:** 0.45--0.65 pages.
- **Expected score impact:** **lift**: evidence becomes findable, caveats are attached to the claims they qualify, and the abstract reads less like an audit transcript.
- **Risk level:** Low-medium. The abstract is high-stakes, so the table must preserve HIV-1 as primary anchor, LOPO's null-consistent status, and the retrospective/no-prospective boundary.

### 2. Abstract opening sentence overload
- **File:line range:** `paper/dissertation/front_en/abstract.tex:2`
- **What it currently does:** Defines MutBench, scope, benchmark lattice, headline interaction, Layer A caveat, and HIV-1 validation in one very long opening paragraph.
- **Compression strategy:** **Split/trim** into: one sentence defining scope and scale; one sentence stating the headline interaction and external anchor; remove one repeated "single-position/RNA-virus/panel" phrase.
- **Expected page saving:** 0.10--0.15 pages.
- **Expected score impact:** **lift**: improves first-impression clarity without removing evidence.
- **Risk level:** Low.

### 3. Chapter 1 problem/benchmark comparison paragraph
- **File:line range:** `paper/dissertation/chapters_en/ch1_introduction.tex:33-39`
- **What it currently does:** Contrasts frequency/entropy hotspot detection with five concurrent benchmarks, then repeats the region-level/per-variant distinction across adjacent paragraphs.
- **Compression strategy:** **Table-ize/trim** the benchmark comparison into a compact comparison table or 3-column inline table: benchmark, target, why not region-level hotspot detection; reduce prose to one pre-table and one post-table sentence.
- **Expected page saving:** 0.35--0.55 pages.
- **Expected score impact:** **lift**: committee readers can verify novelty faster, and the ViroGym/EVEREST/ProteinGym distinction becomes more defensible.
- **Risk level:** Low. Keep citations and the "region-level detection, not per-variant fitness" boundary.

### 4. Bench-side pipeline narrative
- **File:line range:** `paper/dissertation/chapters_en/ch1_introduction.tex:41-49`
- **What it currently does:** Explains sequence collection, computational analysis, experimental validation, lexical collision with stages, and practical candidate reduction.
- **Compression strategy:** **Table-ize** the three steps: input/activity/output/role in dissertation; move the "step vs stage" lexical note to a footnote or parenthetical.
- **Expected page saving:** 0.25--0.40 pages.
- **Expected score impact:** **lift**: the pipeline becomes scannable and the "computational filter" argument is easier to grade.
- **Risk level:** Low.

### 5. Objectives plus panel-scope summary
- **File:line range:** `paper/dissertation/chapters_en/ch1_introduction.tex:81-94`
- **What it currently does:** Gives three objectives, then inserts a dense panel-scope summary with 11-pathogen, 12-pathogen, and Wave 4--5 panels.
- **Compression strategy:** **Consolidate/table-ize** the panel-scope material into a small "panel ledger" with columns: panel, used for, not used for; keep the objectives shorter and avoid repeating Stage 3/Zika details inside Objective 1 and the panel summary.
- **Expected page saving:** 0.35--0.50 pages.
- **Expected score impact:** **lift**: protects against panel-expansion confusion while reducing repeated caveats.
- **Risk level:** Low-medium. Must preserve that headline claims belong to the 11-pathogen main panel.

### 6. Research overview text duplicates figure content
- **File:line range:** `paper/dissertation/chapters_en/ch1_introduction.tex:96-137`
- **What it currently does:** The lead-in sentence, TikZ nodes, and caption all repeat the same problem-to-MutBench-to-pathogen-dependence-to-HIV-1 sequence.
- **Compression strategy:** **Trim** either the lead-in or caption to a single functional sentence; keep the figure, but remove repeated "culminating in external vaccine-escape validation..." language from one location.
- **Expected page saving:** 0.10--0.20 pages.
- **Expected score impact:** **neutral to lift**: less repetition around an already visual summary.
- **Risk level:** Low.

### 7. Contribution 1 as methods catalog
- **File:line range:** `paper/dissertation/chapters_en/ch1_introduction.tex:147-149`
- **What it currently does:** Packs novelty claim, benchmark scale, concurrent benchmark contrast, 10/20/6 taxonomy, three-layer ground truth, hotspot-score, and three stages into two long paragraphs.
- **Compression strategy:** **Table-ize** Contribution 1 into a component ledger: scope/scale, ground truth, metric, experimental design, comparator boundary. The prose can then state only the novelty and purpose.
- **Expected page saving:** 0.30--0.45 pages.
- **Expected score impact:** **lift**: makes the framework architecture easier to inspect and reduces overlap with Objectives.
- **Risk level:** Low.

### 8. Contribution 2 caveat stack
- **File:line range:** `paper/dissertation/chapters_en/ch1_introduction.tex:151-154`
- **What it currently does:** States pathogen-dependent optimality, lists examples, reports Friedman/ANOVA/CI/lower-bound/small-cluster caveat, and explains LOPO's evidentiary status.
- **Compression strategy:** **Consolidate** into an evidence row or short paragraph: primary evidence = interaction; corroborating evidence = Friedman/no universal winner and 9 types; boundary = LOPO null-consistent and small-cluster caution. Move Bolker rule-of-thumb detail to limitations/methods cross-reference.
- **Expected page saving:** 0.25--0.35 pages.
- **Expected score impact:** **lift**: prevents caveat overload while keeping the defensible hierarchy of evidence.
- **Risk level:** Medium. Do not delete the LOPO null-consistency warning.

### 9. Contribution 3 validation/feature-ablation block
- **File:line range:** `paper/dissertation/chapters_en/ch1_introduction.tex:156-158`
- **What it currently does:** Combines search-space reduction, HIV-1 novel-only enrichment, H3N2/SARS-CoV-2 status, EqualWeight integration, per-feature examples, 4-core non-inferiority, and lattice/callability boundaries.
- **Compression strategy:** **Table-ize** as an external-validation ledger: HIV-1 primary anchor, H3N2 self-consistency, SARS-CoV-2 exploratory, 4-core robustness boundary. Move exact full-10/fixed-4 LOPO means and sign-flip detail to Chapter 4 cross-reference.
- **Expected page saving:** 0.40--0.60 pages.
- **Expected score impact:** **lift**: mirrors the successful audit-ledger pattern and makes the primary/secondary/exploratory hierarchy harder to miss.
- **Risk level:** Medium. Keep direct novel-only HIV-1 enrichment and Bonferroni survival in main text.

### 10. Dissertation organization catalog
- **File:line range:** `paper/dissertation/chapters_en/ch1_introduction.tex:165-173`
- **What it currently does:** Lists chapters with long inventories of every section and analysis type.
- **Compression strategy:** **Trim/table-ize** to one compact table: chapter, purpose, main evidence; remove subtopic inventories that the table of contents already provides.
- **Expected page saving:** 0.25--0.40 pages.
- **Expected score impact:** **neutral to lift**: lowers end-of-chapter fatigue with minimal evidentiary risk.
- **Risk level:** Low.

## 2. Top 3 recommended

1. **Candidate 1: Abstract evidence ledger** -- best lift/risk ratio because it compresses the densest prose while improving the abstract's defense map. Estimated saving: 0.45--0.65 pages; expected score impact: +0.2.
2. **Candidate 9: Contribution 3 validation ledger** -- high-value because it preserves the HIV-1/H3N2/SARS-CoV-2 hierarchy and turns repeated caveats into gradeable rows. Estimated saving: 0.40--0.60 pages; expected score impact: +0.2.
3. **Candidate 5: Panel-scope ledger** -- reduces repeated 11/12/Wave caveats while making the scope boundary more defensible. Estimated saving: 0.35--0.50 pages; expected score impact: +0.1.

Combined top-3 saving estimate: **1.2--1.75 pages**. Combined expected score impact: **+0.5**, mostly from readability and reduced ambiguity rather than new evidence.

## 3. Sample compressed prose for candidate #1

MutBench evaluates region-level, single-position hotspot detection across 11 RNA viruses using 20 scoring formulas and 39 detector variants (8,580 evaluation cells). Its main evidence is summarized below.

| Claim | Main result | Boundary |
|---|---|---|
| Framework sanity check | Stage 1 SARS-CoV-2 MutClust-Hybrid hotspot-score = 0.778 | Controlled single-pathogen check |
| Pathogen-dependent information utility | Stage 2 scoring x pathogen interaction is the largest modeled component, $\omega^2=0.296$ (95% cluster-bootstrap CI [0.195, 0.333]); 6-category lower bound $\omega^2=0.103$ | Layer A labels partly confound biology with curation protocol |
| No universal best combination | Friedman $p=0.990$; LOPO 0/11 exact matches with 0.265 oracle-vs-generalized MCC gap | LOPO 0/11 is null-consistent alone; inference rests on interaction plus external audit |
| Practical external anchor | HIV-1 escape enrichment $7.19\times$ full-set and $7.16$--$8.24\times$ novel-only | Retrospective; no prospective time-forward validation |

Feature-ablation and negative sensitivity analyses bound the practical use: the historical 4-feature core is statistically indistinguishable from the 10-feature EqualWeight ensemble, while UniProt-derived Layer A' does not transfer.

RESULT_JOBA: candidates=10 top3_pages_saved=1.2-1.75 top3_score_impact=+0.5
