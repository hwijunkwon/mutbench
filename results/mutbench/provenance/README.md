# MutBench Provenance Bundle

This directory provides verifiable provenance for the dissertation
"MutBench: A Reproducible Benchmark for Single-Position Variant-Effect Scoring
across 11 Surface Glycoproteins" (KNU, 2026).

It is the canonical record referenced from `chapters_en/ch3_methods.tex`
(Sections "9-pathogen data", "External resource licenses", and
"Reproducibility envelope") and `chapters_en/ch6_conclusion.tex`
(Section `code_availability`).

## Files

| File | Purpose | Referenced from |
|------|---------|-----------------|
| `genbank_queries.csv` | Per-pathogen NCBI Entrez queries (taxon ID, gene/product filter, length window, exclusion clauses) for all 11 pathogens, with query date and post-deduplication unique counts that match Table~\ref{tab:pathogen_data}. | ch3:133, ch3:134, ch3:166 |
| `dms_sources.csv` | DMS (deep mutational scanning) dataset sources for the 7 Layer-C-evaluable pathogen/protein pairs, including DOI, license, source repository, and access date. Replicate counts reflect the discrepancy between published replicates and the 2-replicate aggregated tables consumed by the pipeline. | ch3:350 |
| `tool_versions.txt` | Frozen versions of every load-bearing software/library/model: Python stack, MAFFT, IQ-TREE, HyPhy, TreeTime, ESM-2, ARTool, PyMC, msprime, plus xelatex. Patch-level versions for IQ-TREE/HyPhy are the canonical reference for ch3:1024. | ch3:1024 |
| `external_resource_licenses.csv` | Per-resource license matrix (license name, URL, redistributable flag, headline-grid usage flag, citation key). Replaces the bullet list in ch3 §external_licenses for machine-readable license auditing. | ch3:1027-1041 |
| `commit.txt` | Git commit hash of the dissertation snapshot (filled in at submission). | ch3:1024, ch6:103 |

## Reproduction Instructions

1. Clone the canonical repository: `git clone https://github.com/kksuhj/mutbench`
2. Check out the dissertation tag: `git checkout dissertation-v1`
3. Recreate the environment: `conda env create -f environment.yml` (or `pip install -r requirements-pinned.txt`).
4. Re-download the FASTA inputs using the queries in `genbank_queries.csv`.
   Note: GenBank is a live database; the unique-sequence counts will drift slightly after
   the per-pathogen query date. The `total_hits` and `unique_after_dedup` columns
   document the snapshot consumed by this dissertation.
5. Re-run the alignment, scoring, and detection pipelines. The pinned random seed
   (`seed=42`) governs all bootstrap, subsampling, and permutation analyses.
6. Cross-check the 8,580-evaluation grid against the released
   `combined_10scoring_results.csv` and the per-stage CSVs in `results/mutbench/`.

## License

- Code (MutBench's own implementation): MIT (see `LICENSE-CODE` at repo root)
- Dissertation text and figures: Creative Commons Attribution-NonCommercial 4.0
  International (CC-BY-NC 4.0; see `LICENSE-DATA` at repo root)
- Derived per-position scores and Layer-C indicator vectors are released under
  the same CC-BY-NC 4.0 terms; raw upstream FASTA bundles, model weights,
  and DMS fitness tables are NOT redistributed.

## License compatibility audit

Every load-bearing 8,580-evaluation cell uses inputs from MIT-, BSD-, GPL-,
or CC-BY-class licenses (see `external_resource_licenses.csv` column
`used_in_headline_grid`). Resources with academic-only or non-commercial
restrictions (ESM-3 Cambrian, EVE, EVEscape) are NOT load-bearing in the
headline grid; they are cited or used only as proxy implementations
(EVEscape_composite is an ESM-2 x SASA x Grantham product, not the original
EVEscape model).

## Citation

```bibtex
@phdthesis{kim2026mutbench,
  author = {Kim, Hwijun},
  title  = {MutBench: A Reproducible Benchmark for Single-Position
            Variant-Effect Scoring across 11 Surface Glycoproteins},
  school = {Kyungpook National University},
  year   = {2026},
  note   = {Zenodo DOI: 10.5281/zenodo.MUTBENCH-DISS (placeholder; assigned at submission)}
}
```
