# Compression-check v2 Job 3 -- ch2:1-150

Scope reviewed: `paper/dissertation/chapters_en/ch2_background.tex:1-150`.

## 1. Opening hotspot-definition paragraph

- **Type:** trim-verbose
- **Current length:** ~165 words; ~0.30--0.40 pp.
- **What it currently does:** Defines viral mutation hotspots, explains non-uniform mutation accumulation, gives RNA-virus mutation rates, and lists three applications.
- **Compression strategy:** Keep one definition sentence plus a compressed application clause; remove the second general restatement of non-uniformity. Example after-state: "Mutation hotspots are non-uniform genomic regions where recurrent mutations concentrate under structural, immunological, or host-adaptation pressure. For RNA viruses, high mutation supply makes such clusters useful for variant-emergence monitoring, vaccine-target selection, and therapeutics aimed at constrained sites."
- **Expected page saving:** 0.10--0.20 pp.
- **Expected score impact:** neutral to lift: no evidence is lost, and the section reaches the methods taxonomy faster.
- **Risk:** low

## 2. Hotspot-method family catalog

- **Type:** table-ize-prose
- **Current length:** ~920 words; ~1.8--2.2 pp.
- **What it currently does:** Reviews frequency, entropy, cancer-genomics, phylogeny/homoplasy, and selection-based approaches, then repeatedly states why each does not solve MutBench's benchmark problem.
- **Compression strategy:** Convert lines 20--57 into a compact method ledger: family, representative tools/studies, signal captured, limitation for viral region-level benchmarking, MutBench relationship. Example after-state: "Table X summarizes prior hotspot signals: frequency is simple but lineage-biased; entropy captures diversity but not mutation-conditioned diversity; homoplasy handles ancestry but not spatial clustering; selection tests identify sites, not regions."
- **Expected page saving:** 0.65--0.90 pp.
- **Expected score impact:** lift: this mirrors the successful audit-ledger pattern, makes the novelty boundary easier to inspect, and reduces tutorial prose without deleting citations.
- **Risk:** low-medium

## 3. HyPhy selection-test inventory

- **Type:** move-detail-to-footnote
- **Current length:** ~230 words inside the larger method-family block; ~0.45--0.55 pp.
- **What it currently does:** Defines MEME, FUBAR, FEL, SLAC, and BUSTED, then clarifies which selection-pressure channels MutBench actually benchmarks.
- **Compression strategy:** Keep MEME/FUBAR in the main sentence because FUBAR feeds MutBench channels; move FEL/SLAC/BUSTED expansion to a footnote or one table row. Example after-state: "HyPhy selection tests such as MEME and FUBAR estimate site-level positive selection; MutBench benchmarks FUBAR-derived summaries plus a Nei--Gojobori proxy, while other HyPhy tests remain future-work comparators."
- **Expected page saving:** 0.20--0.35 pp.
- **Expected score impact:** lift: it preserves the channel boundary while reducing the impression that unbenchmarked tests are central.
- **Risk:** low

## 4. Density-clustering tutorial block

- **Type:** table-ize-prose
- **Current length:** ~520 words; ~1.0--1.2 pp.
- **What it currently does:** Explains DBSCAN, its fixed-epsilon failure mode, HDBSCAN, OPTICS, and MutClust's adaptive-radius response.
- **Compression strategy:** Replace the algorithm tutorial with a four-row comparison table: DBSCAN, HDBSCAN, OPTICS, MutClust; columns for density assumption, operational advantage, viral-genomics failure/boundary, role in this dissertation. Example after-state: "Density methods differ mainly in whether the neighborhood scale is fixed, hierarchical, visualized across scales, or biologically weighted; MutClust motivates the adaptive-scoring premise used here."
- **Expected page saving:** 0.40--0.60 pp.
- **Expected score impact:** lift: committee readers get the method distinction faster, and the SARS-CoV-2 99.76% failure statistic becomes more salient as a table cell.
- **Risk:** low

## 5. Antibody-escape DMS cross-validation paragraph

- **Type:** consolidate-duplicate
- **Current length:** ~330 words; ~0.70--0.85 pp.
- **What it currently does:** Distinguishes antibody-escape DMS from fitness-DMS, names SARS-CoV-2 antecedents, previews the vaccine-escape audit, lists Layer C sources, and states the orthogonality of the two ground-truth tracks.
- **Compression strategy:** Split into one main-text distinction plus a small ground-truth-track ledger or footnote for dataset names. Example after-state: "Antibody-escape DMS and fitness-DMS provide orthogonal signals: escape-DMS supports the Chapter 5 vaccine-escape audit, whereas fitness-DMS supplies Layer C for pathogens with available assays (Table X)."
- **Expected page saving:** 0.35--0.50 pp.
- **Expected score impact:** lift: the main conceptual distinction becomes clearer, while source-level provenance can be retained in a table/footnote.
- **Risk:** medium

## Summary

Best order: candidate 2, candidate 4, candidate 5, then the smaller trims. None overlap the already-applied compression list. The combined opportunity is mainly structural: turn related-work inventories into inspection tables that preserve citations and novelty boundaries while reducing tutorial density.

RESULT_COMPRESS_V2_J3: candidates=5 total_pages_saved=1.7-2.6 total_score_impact=+0.4
