# Codex review — public-database annotation coverage for panel expansion

You are an independent reviewer. **Read-only mode.** Do not modify the working
tree except the report file. Do not commit.

## Background

The user maintains a benchmark of position-level scores for 12 reference
organisms and wants to extend it to 16 additional organisms whose feature
matrices already exist at `data/cross_pathogen/*_position_scores.csv`. Existing
12-target labels were originally curated from 1–3 named publications per
target; a separate 911-document literature scrape attempt was abandoned after
hitting a manual-review bottleneck.

To replace the abandoned scrape with a **public-database-driven** approach, we
queried UniProtKB for the 16 candidate targets using canonical reviewed
accessions and counted **structured functional annotations** that the database
itself flags (Site, Binding site, Active site, Region, Motif). For polyprotein
entries, features were re-mapped to the mature protein region via the Chain
annotation.

## Your inputs

- Inventory CSV: `results/mutbench/layerA_alternative_sources_inventory_v2.csv`
  Columns: target, uniprot_acc, length, chain_label, chain_start, chain_end,
  n_features_in_chain, n_layer_a_relevant, feature_breakdown, classification.
- Per-feature CSV: `results/mutbench/layerA_alternative_sources_features_v2.csv`
  Columns: target, uniprot_acc, feature_type, start_full, end_full,
  start_mature, end_mature, layer_a_relevant, description.
- Probe scripts: `scripts/probe_uniprot_layerA.py` (v1, deprecated),
  `scripts/probe_uniprot_layerA_v2.py` (current).
- 12-target reference label table: `results/mutbench/layer_a_tags.csv` (309
  rows, three tag categories: immune_escape, functional, convergent).
- 12-target feature matrices: `results/mutbench/feature_analysis/feature_matrix_*.csv`.
- Position-score CSVs for the 16 candidate targets: `data/cross_pathogen/`.
- Wave 4 closure note in memory: `codex_wave4_results.md` (16/16 envelope-pass
  but 1/28 stability, panel-size limit not relaxed by features-only fallback).

## What I want from you

A critical review with these explicit checks. Use the v2 inventory and feature
CSVs as ground truth; do not re-query UniProtKB.

### 1. Classification audit

The current rule classes a target as A if `n_layer_a_relevant >= 5`, B if
1–4, C if 0. v2 result: A=10, B=5, C=1.

- Spot-check 4 Class A targets and 2 Class B targets. Read their feature
  descriptions in the per-feature CSV. Are these features the right kind to
  treat as positive labels? Specifically, distinguish:
  - **Functional residues** (binding sites, catalytic residues, host-receptor
    interaction sites, fusion-peptide loop) — strong positive-label candidates
  - **Structural-only regions** (large "Disordered" stretches, full-length
    "Stalk"/"Head" regions, signal-peptide cleavage sites, mucin-like regions)
    — weak or non-positive
- Recommend whether the auto-classifier should subset the `Region` rows by
  description text so that "Disordered", "Mucin-like region", and full-length
  domain bands are excluded.

### 2. Coordinate-frame check

Position scores in `data/cross_pathogen/*_position_scores.csv` use mature
protein indexing. UniProt features for polyproteins were mapped via the
detected Chain region. Spot-check three flavivirus targets (yfv_e, wnv_e,
japanese_encephalitis_virus_e) by:

- Reading the first 5 rows of the corresponding `data/cross_pathogen/*_position_scores.csv`
- Comparing the position range to the v2 inventory's `chain_end - chain_start + 1`
- Flagging any frame mismatch (off-by-one, signal-peptide-included vs
  -excluded, alternative reference strain).

### 3. Comparability to existing 12-target labels

- Compare per-target n_layer_a_relevant from v2 to per-target row counts in
  `layer_a_tags.csv` for the 12-target panel. If the 12 targets average ~26
  positions/target and the new 16 average ~10 (rough estimate from v2
  totals), discuss whether the labels are comparable enough to mix in a
  single benchmark fold or whether they should run as a sensitivity panel.
- Also examine whether the 12-target labels would themselves classify as A
  under the same UniProt-feature criterion, by sampling SARS-CoV-2 and
  Norovirus UniProt entries' feature counts via the `accession`/`organism`
  fields you already have. (You may use offline reasoning if API access
  fails; do not block on the network.)

### 4. Honest framing for the dissertation

If we expand to 12 + N targets where the new N use UniProt-feature-derived
labels (not literature-curated immune-relevance labels), the framing must
be different. Recommend the most defensible language:

- "Public-database functional-annotation labels (Layer A')" treated as a
  separate label provenance from literature-curated labels.
- Or "extended panel" with explicit asterisk / sensitivity-only treatment.
- Or do not mix; run two parallel evaluations.

### 5. Final recommendation

Pick one:

- **R1 — Adopt full extension to 12 + 10 Class-A targets** (using the v2
  pipeline + a description-text refinement to drop disordered/structural rows).
  State exactly which 10 targets and what label-construction script we should
  write next.
- **R2 — Limit to a smaller subset** (e.g., 5–7 targets where v2 features
  clearly include functional sites). State exactly which.
- **R3 — Reject UniProt-only labels as too different from literature-curated
  labels**, and recommend reverting the dissertation scope to the 12-target
  panel and removing all forward references to the abandoned scrape from
  `chapters_en/ch4_results.tex` and `chapters_en/ch5_discussion.tex`.
- **R4 — Hybrid** that keeps the 12-target labeled benchmark as the headline,
  adds the new 12+N as a clearly-labelled sensitivity panel, and writes a
  concrete prose paragraph for `chapters_en/ch5_discussion.tex` future-work
  section that replaces the current "pilot 3" reference.

State your reasoning. Cite at least 5 specific (target, feature_type,
start_mature, end_mature, description) tuples from the per-feature CSV.

## Output

Single report at:

  `paper/dissertation/review/2026-05-02/codex_layerA_uniprot_review.md`

Length: ≤3500 words. End with a numbered next-step list (≤8 items) that we
could execute as a single subsequent commit, including any prose snippets
ready to paste into `chapters_en/ch5_discussion.tex`.
