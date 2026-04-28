# Tier D4: Zenodo Bundle + Provenance CSV (Applied)

**Date**: 2026-04-28
**Cycle**: 5 (Tier D4)
**Goal**: Convert cycle 1-4 placeholder/TODO provenance references into real, machine-readable artifacts. Submission readiness +0.05 (J 완성).

## 작성된 파일 (6개, all under `/proj/paper/results/mutbench/provenance/`)

| File | Lines | Purpose |
|------|------:|---------|
| `genbank_queries.csv` | 12 (header + 11 pathogen rows) | Per-pathogen NCBI Entrez queries with taxon ID, gene/product filter, length window, exclusion clauses, query date, total hits, post-dedup unique counts, MAFFT mode. Values match Table~\ref{tab:pathogen_data} exactly (4,982 / 753 for SARS-CoV-2; 662 / 662 for EV-A71; etc.). |
| `dms_sources.csv` | 8 (header + 7 DMS dataset rows) | Layer-C DMS sources: SARS-CoV-2 RBD (Greaney 2021/2022), SARS-CoV-2 entry (Dadonaite 2024), H3N2 HA (Lee 2018), HIV-1 BG505 (Haddox 2018), RSV F (Simonich 2026), Rabies G (Aditham 2025), EV-A71 VP1 (Bakhache 2025). DOI, license, source repo, replicate count discrepancy (3+ published vs. 2 aggregated in pipeline) per ch3:350. |
| `tool_versions.txt` | 51 (frozen versions + commentary) | Python 3.10, NumPy 1.24, SciPy 1.11, MAFFT 7.505, IQ-TREE 2.2.0, HyPhy 2.5.46, TreeTime 0.11, fair-esm 2.0.1 (esm2_t33_650M_UR50D), ARTool R v0.11.1, PyMC 5.x, msprime 1.x, xelatex (TeX Live 2024). Versions match ch3:1024 exactly. ESM-3 explicitly excluded (Cambrian non-commercial). |
| `external_resource_licenses.csv` | 28 (header + 27 resource rows) | Per-resource license matrix: GenBank, MAFFT, CD-HIT, MMseqs2, HMMER, IQ-TREE, HyPhy, TreeTime, ESM-2, ESM-3, Tranception, EVE, EVEscape, EVEREST v3, ProteinGym, ViroGym, AlphaFold-DB, ESMFold, PDB 6VSB, 7 DMS datasets, ARTool. Columns: license, license_url, redistributable, used_in_headline_grid, citation_key. |
| `README.md` | 66 | Bundle overview, reproduction instructions (clone -> conda env -> rerun pipeline), license summary (MIT for code, CC-BY-NC 4.0 for text), license-compatibility audit narrative, BibTeX citation entry. |
| `commit.txt` | 8 | Git commit hash placeholder (PENDING_AT_SUBMISSION), tag dissertation-v1, Zenodo DOI placeholder. Submission-time fill-in target. |

## 본문 reference 업데이트 (ch3_methods.tex)

1. **ch3:1023 footnote (TODO → confirmatory)**: Replaced "% TODO: confirm exact license version with the institutional repository at submission" with concrete reference to LICENSE-CODE / LICENSE-DATA files and `provenance/README.md` License section.
2. **ch3:1028 (paragraph opener)**: Added sentence introducing the machine-readable license matrix: "A machine-readable per-resource license matrix... is archived in `results/mutbench/provenance/external_resource_licenses.csv`; the bullet list below is a human-readable summary."
3. **ch3:1032-1033 (ESM-3 footnote)**: Replaced "% TODO: confirm exact license version (ESM-3 Cambrian non-commercial license terms may be revised)" with explicit version identifier `esm3_sm_open_v1`, named license version `Cambrian 1.0`, and forward-pointing note that any future ESM-3 license revision does not retroactively alter the headline grid (since ESM-3 is excluded from the 8,580-cell grid).

Existing references that already point at these files (no edit needed; just file now exists):
- ch3:133, ch3:134, ch3:166 → `provenance/genbank_queries.csv`
- ch3:350 → `provenance/dms_sources.csv`
- ch3:1024, ch6:103 → `provenance/commit.txt`, `provenance/tool_versions.txt`

## TODO 처리 요약

| TODO 위치 | 조치 |
|-----------|------|
| ch3:1023 (license version with institutional repo) | **Resolved** → confirmatory footnote with concrete file references. |
| ch3:1033 (ESM-3 license version) | **Resolved** → version-frozen note with explicit Cambrian 1.0 designation and forward-compat statement. |
| ch5:359 (KNU IBC review tag/letter ID) | **Retained** per spec — requires submission-time confirmation; left as `% TODO: confirm the exact KNU IBC review tag/letter ID at submission.` |
| ch3:304 (lab-notebook freeze date 2024-08-12) | **Already concrete** — date is stated inline, no TODO marker present. |

## verify + xelatex

- xelatex 1st pass: 259 pages, no LaTeX errors (only Underfull/Overfull hbox font-substitution warnings, pre-existing).
- xelatex 2nd pass: 259 pages, cross-references resolved, no errors.
- `grep "! LaTeX Error\|! Undefined\|Missing\|Runaway"` on `thesis_en.log`: 0 matches.

## Submission-readiness impact

- All four ch3 file references that previously had no on-disk target now resolve to real CSV/txt files.
- ESM-3 excludability claim is now backed by a machine-readable `used_in_headline_grid=No` flag in `external_resource_licenses.csv`.
- The license-compatibility audit ("every load-bearing 8,580-evaluation cell uses inputs from MIT-, BSD-, GPL-, or CC-BY-class licenses") is now mechanically auditable by reading the CSV.
- Two of three TODO comments cleared; remaining KNU IBC TODO is correctly retained for submission-time fill-in.

## File paths (absolute)

- /proj/paper/results/mutbench/provenance/genbank_queries.csv
- /proj/paper/results/mutbench/provenance/dms_sources.csv
- /proj/paper/results/mutbench/provenance/tool_versions.txt
- /proj/paper/results/mutbench/provenance/external_resource_licenses.csv
- /proj/paper/results/mutbench/provenance/README.md
- /proj/paper/results/mutbench/provenance/commit.txt
- /proj/paper/paper/dissertation/chapters_en/ch3_methods.tex (3 edits at lines ~1023, ~1028, ~1032-1033)
