# Codex feasibility check — alternative Layer A sources for panel expansion

You are a feasibility analyst. **Read-only by default.** You may make small
network calls (UniProt API, IEDB API, NCBI E-utilities) but do not modify the
working tree except the report and a tiny inventory CSV. Do not commit.

## Background

The user's dissertation has a 12-pathogen panel with manually curated Layer A
positions (literature-based, 1–3 papers per pathogen, captured in
`results/mutbench/layer_a_tags.csv`). Wave 5 was supposed to extend this panel
with YFV E / Lassa GPC / WNV E via a 911-PMID PubMed scrape + manual curation,
but the human curation step is infeasible in the defense window. The user
wants to know whether **alternative pre-existing Layer A sources** can extend
the panel **without manual curation**.

The 12-panel was originally built from named papers — same approach should
work for new pathogens if their named papers exist (they do; see
`scripts/pathogen_scaling_targets.json` Tier 1 entries).

19 cross-pathogen feature-only targets exist at
`data/cross_pathogen/*_position_scores.csv` (Wave 4 16/16 envelope targets).

## The two paths to evaluate

### Path 2 — Named-paper extraction for the 3 Wave 5 pilot targets

Sources predeclared in `scripts/pathogen_scaling_targets.json`:

- **YFV E (taxid 11089)** — `Rey 2017` neutralizing-epitope literature
- **Lassa GPC (taxid 11620)** — `Robinson 2016` escape mAb panel
- **WNV E (taxid 11082)** — `Beasley 2002` / `Oliphant 2005` epitope mapping

For each, determine: is the paper accessible? Does it report residue-level
epitope/escape positions (in main text, table, or supplement)? Could a
**focused parser** extract the position list from the abstract + tables in
under one hour each? Or does it require the same kind of manual paper-reading
as Wave 5 Task 3?

You can use `efetch` against PubMed/PMC if needed. Do not run multi-hour
scrapes. Cite each source by PMID/DOI.

### Path 3 — Public-DB harvest (IEDB / UniProt) for the 19 Wave 4 cross_pathogen targets

For each target listed in `data/cross_pathogen/` (excluding 12-panel members
that already have Layer A: `dengue_e`, `hiv1_gp120`, `norovirus_vp1`):

- `chikungunya_virus_e2`
- `eastern_equine_encephalitis_virus_e2`
- `hcov-229e_spike`
- `hcov-nl63_spike`
- `hendra_virus_g`
- `japanese_encephalitis_virus_e`
- `lassa_gpc`
- `marburg_virus_gp`
- `measles_virus_h`
- `mumps_virus_hn`
- `nipah_virus_g`
- `tick-borne_encephalitis_virus_e`
- `venezuelan_equine_encephalitis_virus_e2`
- `western_equine_encephalitis_virus_e2`
- `wnv_e`
- `yfv_e`

(That's 16 genuinely-new targets after subtracting the 3 already labeled.)

For each, determine:

1. **IEDB** — does the IEDB API return per-residue epitope data for this
   pathogen/protein? Approximate epitope position count? Use the IEDB query
   API (`https://query-api.iedb.org` or the older `iedb.org` API). At minimum,
   try a search by organism+antigen. Cite the API endpoint used.
2. **UniProt** — does the canonical UniProt entry for this protein have
   structured antigenic-site / disulfide / propeptide / epitope features?
   Fetch via REST: `https://rest.uniprot.org/uniprotkb/search?query=...`.
3. **Bloom-lab DMS catalog / Dms-view / DMSurl** — any DMS escape data exists?

For each target, classify into:

- **A: Strong candidate** — IEDB ≥10 mapped residues OR UniProt has explicit
  antigenic-site features OR DMS catalog with reliable escape thresholds.
- **B: Marginal** — IEDB has 1–9 residues OR partial UniProt annotation; would
  need light human review.
- **C: Insufficient** — no structured public data; would still need manual
  literature curation.

Coordinate-system risk: flag any candidate where IEDB/UniProt position
indexing differs from the position scores CSV reference frame. This was a
predeclared concern for Lassa GPC (signal peptide / GP1 / GP2 cleavage) and
YFV/WNV (polyprotein vs mature E numbering).

## Honest constraints

- IEDB API may rate-limit. Stop after 60 seconds per target if responses are
  slow; record `api_timeout=true`.
- UniProt search may return multiple isoforms; pick the longest reviewed entry
  matching the target accession in `results/mutbench/pilot_accession_manifest.csv`
  if available. Otherwise prefer the canonical UniProtKB entry.
- Do not invent data. If an API returns nothing, say so.
- Do not pursue NCBI text mining (that was Wave 5; user has explicitly
  declared that path infeasible).

## Output

Write a single report to:

  `/proj/paper/paper/dissertation/review/2026-05-02/codex_layerA_alternative_sources.md`

Structure:

1. **Path 2 verdict** — for each of 3 Wave 5 pilot targets:
   - PMID/DOI, accessibility status, position-list-in-paper status, automation
     feasibility (can a focused parser extract positions, or does it need a
     human reading the whole paper?). One paragraph each.

2. **Path 3 inventory** — table with one row per target × source (IEDB, UniProt,
   DMS), columns: target, source, n_mapped_residues_or_features,
   coordinate_system, classification (A/B/C), API endpoint cited.

3. **Coverage summary** — how many of the 16 new targets reach Class A or B?
   What is the realistic n for an expanded labeled panel without manual
   curation? Compare to the Wave 4 quorum threshold (7+ stable per current
   Layer A behavior).

4. **Recommendation** — one of:
   - **Expand to N targets via Path 3** (specify which N), abandon Wave 5 PubMed
     pipeline, replace ch4/ch5 Wave 5 prose with public-DB framing.
   - **Path 2 only for 3 pilot targets** (specify which papers parse cleanly),
     skip Path 3.
   - **Both paths viable** — staged rollout.
   - **Neither viable** — recommend reverting to 12-panel scope and removing
     all Wave 5 prose mentions from thesis.

5. **Concrete next steps** — exact files/scripts to create, exact lines of
   thesis prose to add or remove. Do not commit; produce a diff plan.

Also produce a tiny inventory CSV at:

  `/proj/paper/results/mutbench/layerA_alternative_sources_inventory.csv`

Schema: `target,source,n_residues,classification,coordinate_system,api_endpoint,notes`

Length budget for the report: ≤3500 words.

If the network is unavailable for any API, record that explicitly and keep
going with the remaining sources. Partial coverage is acceptable; fabricated
coverage is not.
