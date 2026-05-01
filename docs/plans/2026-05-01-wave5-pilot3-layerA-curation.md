# Wave 5 Pilot 3 — Layer A Curation for YFV E, Lassa GPC, and WNV E
> **Version:** v1 draft, 2026-05-01  
> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement task-by-task.
**Goal:** Convert three Wave 4 feature-compatible but unlabeled targets into curated Layer A feature matrices: Yellow fever virus envelope (YFV E), Lassa virus glycoprotein complex (Lassa GPC), and West Nile virus envelope (WNV E). This is a mixed automated + manual wave: Codex may search, download, normalize, cross-tabulate, and integrate evidence, but the final per-position Layer A labels require human researcher's domain judgment.
**Architecture:** Build a reproducible evidence-to-label pipeline with a hard human checkpoint. Automated tasks produce per-target literature/DMS evidence inventories and position-level worksheets. The human curator reviews evidence and enters final labels. Only after that checkpoint may Codex integrate `layer_a` into target feature matrices and rerun the Wave 4 labeled and expanded diagnostics with up to three existing Wave 4 targets changed from unlabeled to curated-labeled status.
**Tech Stack:** Python 3, pandas, Biopython optional, NCBI E-utilities, PubMed XML/JSON, bioRxiv API/RSS, static DMS/escape catalogs where available. No GPU. Network required only for Task 1 evidence discovery. Compute budget after curation: <1 CPU-hour.
**Documentation cadence:** Per task: standalone report under `paper/dissertation/review/2026-05-01/wave5/`. Memory written ONLY at Wave 5 closure. No manuscript prose edits in this plan unless separately requested after results.
**Spec source:** Wave 4 closure and result review, `codex_wave4_results.md` memory, Chapter 3 Layer A definition, Wave 4 plan format, existing v176 pilot accession/feature scaffold.
**Critical constraint:** Codex must not infer final Layer A labels automatically. Automated evidence summaries may propose labels for reviewer attention, but `final_label` is human-authored. Any validation result using machine-proposed labels before human review is invalid and must be discarded. Task 4 must also require an explicit human approval manifest; populated worksheet cells alone are not sufficient if they could have been produced by Task 2 automation.
**Out of scope (Wave 6+ plans):** Adding a fourth target; EVE/PLM site-effect generation; manuscript ch4/ch5 prose insertion; defense rehearsal; broad all-16-target curation; automatic literature-derived labeling without human review.
---
## Motivation
Wave 4 ended with a **POSITIVE-BOUNDED** verdict. The shared `freq+entropy` feature core preserved bounded labeled-panel signal on the 12 existing feature matrices, but the expanded panel remained unlabeled and unstable: **16/16** newly added unlabeled targets were inside the labeled feature envelope, while only **1/28** targets passed the expanded stability proxy. This separates two facts that must not be conflated. The v176 pilot targets are technically feature-compatible, but the missing Layer A labels are now the rate-limiting step.
Pilot 3 is therefore the correct Wave 5 move. It does not claim that Wave 4 already validated the expanded panel or that the 12-pathogen failure was a small-panel artifact. Instead, it tests whether manual labels reduce the most obvious Wave 4 bottleneck by changing up to three existing Wave 4 targets from unlabeled to curated-labeled status and asking whether labeled LOPO, quorum, and stability diagnostics move in the right direction. This is pilot evidence for whether curation is worth scaling, not resolution of Q7.
The three targets are intentionally small enough for manual review while covering distinct viral families and curation regimes: YFV and WNV are flavivirus envelope proteins with neutralization/epitope literature, and Lassa GPC is an arenavirus glycoprotein with a different antibody and receptor-binding evidence structure. This is a pilot, not an all-target curation campaign.
---
## Predeclared Scope
### Fixed target set
Do not add a fourth target during this wave.
| Target slug | Pathogen | Surface protein | Taxid | Existing feature input | Existing provenance |
|---|---|---|---:|---|---|
| `yfv_e` | Yellow fever virus | Envelope / E protein | 11089 | `data/cross_pathogen/yfv_e_position_scores.csv` | `results/mutbench/pilot_accession_manifest.csv` |
| `lassa_gpc` | Lassa virus | Glycoprotein complex / GPC | 11620 | `data/cross_pathogen/lassa_gpc_position_scores.csv` | `results/mutbench/pilot_accession_manifest.csv` |
| `wnv_e` | West Nile virus | Envelope / E protein | 11082 | `data/cross_pathogen/wnv_e_position_scores.csv` | `results/mutbench/pilot_accession_manifest.csv` |
### What counts as Layer A
Use the Chapter 3 definition: Layer A positions are literature-curated adaptive or diversifying positions treated as hotspot positives. Evidence can include immune escape, neutralization escape, receptor/adaptation mutations, recurrent lineage-level emergence, antigenic-site membership, or diversifying-selection literature, depending on the pathogen and source study. DMS-only evidence is not primary Layer A by default because Chapter 3 treats DMS as Layer C unless the curator explicitly upgrades it based on literature relevance and assay context.
No single computational criterion is imposed uniformly across the three targets. The operational definition remains: **Layer A is the union of literature-curated positive/diversifying-selection positions per target**, with evidence basis, mapping confidence, and label confidence explicitly recorded.
### What does not count
- A high `frequency`, `entropy`, or `hscore` value alone is not Layer A evidence.
- A Codex-generated proposed label is not a final label.
- A broad protein domain, epitope region, or antibody footprint is not automatically converted to every residue as positive unless the cited study supports residue-level annotation or the human curator explicitly accepts a region-to-position mapping.
- DMS escape is evidence for review, but it is not auto-thresholded into final labels without the human curator accepting the threshold and coordinate mapping. DMS-only positions default to `layer_a_dms_sensitivity`, not `layer_a_primary`.
- Coordinates that cannot be mapped to the existing position index are not integrated as positives.
---
## Mixed Automation Matrix
| Step | Automatable? | Tool/Method |
|---|:---:|---|
| 1. PubMed search per target | ✅ codex | E-utilities, predeclared keyword set |
| 2. Pre-print mining (bioRxiv) | ✅ codex | RSS / API |
| 3. DMS escape catalog lookup | ✅ codex | Static URLs / CSV downloads |
| 4. Per-position evidence sheet generation | ✅ codex | Position × evidence cross-table |
| 5. **Layer A label decision per position** | ❌ HUMAN | Domain judgment + literature review |
| 6. **Inter-position consistency check** | ⚠️ HUMAN-led | Heuristic flags from script |
| 7. Layer A CSV → feature_matrix integration | ✅ codex | Schema alignment |
| 8. Validation: `12->15 labeled within 28 unique targets` rerun | ✅ codex | `scripts/codex_w4_features_lopo.py` extended |
### Automation boundary
Codex may fill `proposed_label` to accelerate review, but these values are advisory and must be ignored by downstream validation until the human has populated `final_label`, `label_confidence`, `curator`, and `curation_date`, and supplied the explicit approval manifest.
### Manual boundary
The human curator must decide whether each position is Layer A positive (`1`) or non-positive/unsupported (`0`) after reviewing evidence summaries and, when needed, the source papers. The curator also resolves conflicts between papers, decides whether region-level evidence is precise enough, and confirms coordinate-system mappings.
---
## Predeclared Search Keywords
These keyword sets are locked before running searches to avoid post-hoc keyword cherry-picking. Task 1 may add exact query syntax required by PubMed, but it must not add new biological concepts after seeing favorable results. Allowed pre-execution expansion is limited to synonyms and coordinate/domain terms listed in this plan; after Task 1 begins, no new biological concept may be added without marking it as post hoc sensitivity search.
### YFV E (`yfv_e`, taxid 11089)
- `"yellow fever virus" AND ("envelope" OR "E protein") AND ("escape" OR "neutralization" OR "epitope" OR "antigenic")`
- `"yellow fever vaccine" AND ("17D" OR "WHO") AND "mutation"`
- `"deep mutational scanning" AND "yellow fever"`
- `"yellow fever virus" AND "envelope" AND ("monoclonal antibody" OR "neutralizing antibody")`
- `"yellow fever virus" AND ("adaptive" OR "positive selection" OR "diversifying selection") AND "envelope"`
- Locked expansion terms: `"YFV"`, `"yellow fever"`, `"17D-204"`, `"Asibi"`, `"E domain I"`, `"E domain II"`, `"E domain III"`, `"EDIII"`, `"fusion loop"`, `"escape mutant"`, `"resistant mutant"`, `"antibody footprint"`, `"glycan"`
### Lassa GPC (`lassa_gpc`, taxid 11620)
- `"Lassa virus" AND ("glycoprotein" OR "GPC" OR "GP1" OR "GP2") AND ("escape" OR "neutralization" OR "epitope" OR "antigenic")`
- `"Lassa virus" AND ("monoclonal antibody" OR "neutralizing antibody") AND ("GPC" OR "glycoprotein")`
- `"Lassa virus" AND ("receptor binding" OR "alpha-dystroglycan" OR "LAMP1") AND "mutation"`
- `"deep mutational scanning" AND "Lassa"`
- `"Lassa virus" AND ("adaptive" OR "positive selection" OR "diversifying selection") AND ("GPC" OR "glycoprotein")`
- Locked expansion terms: `"LASV"`, `"arenavirus"`, `"GP-C"`, `"GPC-C"`, `"stable signal peptide"`, `"SSP"`, `"glycan shield"`, `"entry"`, `"fusion"`, `"escape mutant"`, `"resistant mutant"`, `"antibody footprint"`
### WNV E (`wnv_e`, taxid 11082)
- `"West Nile virus" AND ("envelope" OR "E protein") AND ("escape" OR "neutralization" OR "epitope" OR "antigenic")`
- `"West Nile virus" AND ("monoclonal antibody" OR "neutralizing antibody") AND "envelope"`
- `"West Nile virus" AND ("vaccine" OR "attenuation") AND "mutation"`
- `"deep mutational scanning" AND "West Nile virus"`
- `"West Nile virus" AND ("adaptive" OR "positive selection" OR "diversifying selection") AND "envelope"`
- Locked expansion terms: `"WNV"`, `"West Nile"`, `"flavivirus"`, `"E domain I"`, `"E domain II"`, `"E domain III"`, `"EDIII"`, `"fusion loop"`, `"escape mutant"`, `"resistant mutant"`, `"antibody footprint"`, `"glycan"`
Record zero-hit queries and do not delete them from `w5_search_queries.csv`.
### Fixed search metadata
For every query, record:
- `target_slug`
- `query_string`
- `database`
- `run_date`
- `n_hits`
- `hit_ids`
- `api_url_or_command`
- `notes`
If searches fail because network is unavailable, Task 1 stops with `blocked_network=true` and records the exact failed commands. Do not substitute ad hoc memory-based paper lists.
---
## Worksheet Schema
Codex creates one CSV per target:
- `results/mutbench/codex_wave5/worksheets/yfv_e_layerA_worksheet.csv`
- `results/mutbench/codex_wave5/worksheets/lassa_gpc_layerA_worksheet.csv`
- `results/mutbench/codex_wave5/worksheets/wnv_e_layerA_worksheet.csv`
Schema:
```text
position,wt_aa,evidence_count,evidence_sources,evidence_summary,evidence_basis,mapping_confidence,proposed_label,label_confidence,notes,final_label,curator,curation_date
```
Column ownership:
| Column | Owner | Rule |
|---|---|---|
| `position` | codex | Existing feature-matrix/cross-pathogen position index |
| `wt_aa` | codex | Reference amino acid if recoverable; blank if unavailable |
| `evidence_count` | codex | Count of distinct evidence records mapped to the position |
| `evidence_sources` | codex | Compact PMID/DOI/preprint/catalog IDs |
| `evidence_summary` | codex | Short source-grounded summary; no unsupported inference |
| `evidence_basis` | codex | Advisory evidence basis: `literature_primary`, `literature_plus_dms`, `dms_only`, `region_only`, or `coordinate_uncertain` |
| `mapping_confidence` | codex | Advisory coordinate confidence: `high`, `medium`, `low`, or `unresolved` |
| `proposed_label` | codex | Advisory only: `0`, `1`, or `needs_review` |
| `label_confidence` | HUMAN | `high`, `medium`, `low`, or `uncertain`; biology/label confidence, separate from mapping confidence |
| `notes` | HUMAN | Free-text rationale, coordinate caveats, conflict notes |
| `final_label` | HUMAN | Required before integration: `0` or `1`; remains blank until human approval |
| `curator` | HUMAN | Initials or name |
| `curation_date` | HUMAN | ISO date |
Format choice: CSV is canonical. Optional `.xlsx` copies may be generated for convenience, but CSV remains the authoritative source for integration.
---
## Predeclared Decision Rules
These rules are guidance for the human curation step, not automatic code paths.
| Evidence pattern | Suggested human decision |
|---|---|
| Strong evidence: ≥2 independent papers support the same position as immune escape, neutralization escape, antigenic, adaptive, or diversifying | `final_label=1`, usually `label_confidence=high` |
| Strong DMS evidence: reproducible escape/fitness signal above predeclared per-study threshold, with reliable coordinate mapping | Include in `layer_a_dms_sensitivity` by default; upgrade to primary Layer A only if the human curator documents assay relevance, coordinate reliability, and why the evidence satisfies the Chapter 3 literature-curated adaptive/diversifying definition. |
| Weak evidence: 1 paper, narrow antibody, single strain, limited assay, or broad region with plausible residue mapping | `final_label=1` only if curator accepts biological relevance; otherwise `0` with note |
| No evidence | `final_label=0` |
| Conflicting evidence | Flag for re-check; default `final_label=0` with `label_confidence=uncertain` unless curator resolves conflict |
| YFV 17D vaccine conserved or attenuation-associated position | Treat conservation/attenuation as additional context, not sufficient alone for Layer A |
| Region-level epitope only | Convert to positive positions only when the source provides residue-level boundary precise enough for the target index |
| Non-envelope or non-GPC evidence | Exclude unless coordinate mapping unambiguously falls inside the evaluated protein |
### DMS threshold placeholder
If a DMS escape catalog is found, Task 1 must record the study's native scale and a proposed threshold before seeing target-level validation results. The plan-level default is: "DMS escape above the study-recommended high-escape cutoff." If the study provides no recommended cutoff, top 5% may be used only for sensitivity labels and must not enter primary validation without curator attestation. The human curator must approve or revise the threshold in the worksheet notes before those positions become final positives.
---
## Coordinate and Schema Rules
- Preserve the existing `position` index in `data/cross_pathogen/*_position_scores.csv`.
- Record all external source coordinate systems explicitly: mature protein, polyprotein, precursor, signal-peptide-inclusive numbering, strain-specific numbering, PDB residue numbering, or alignment column.
- Do not silently shift coordinates. Every non-identity mapping requires a `coordinate_mapping_notes` entry in the evidence table. The evidence table must include `source_position`, `source_residue`, `target_position`, `target_residue`, `mapping_basis`, `offset`, and `reference_accession` for every non-identity mapping.
- If wild-type amino acid conflicts with the source residue, flag `aa_mismatch=true` and require human review.
- If a source reports GP1/GP2 coordinates for Lassa GPC, map to the evaluated GPC position index only after confirming whether the signal peptide and cleavage site are included. For Lassa, explicitly record whether positions are pre-GPC, signal-peptide-inclusive GPC, mature GP1, mature GP2, SSP, or alignment coordinates; GP1/GP2 coordinates require a documented cleavage-site offset before integration.
- If YFV or WNV envelope evidence is reported in polyprotein numbering, map to E-protein numbering before worksheet integration. For YFV/WNV, record whether the source uses full polyprotein, prM/E precursor, mature E, domain/PDB, or alignment numbering and record the exact offset used to reach the evaluated E index.
- For each mapped evidence row, require `source_position`, `source_residue`, `target_position`, `target_residue`, `mapping_basis`, `offset`, `aa_mismatch`, `mapping_confidence`, and `reference_accession`.
- If mapping confidence is low or unresolved, leave `proposed_label=needs_review`; do not auto-fill `final_label`, and keep the row out of both primary and sensitivity labels until human approval.
---
## Predeclared Failure-Mode Branches
| Outcome | Predefined response |
|---|---|
| **Branch A: ≥2 of 3 targets get ≥10 high-confidence literature-primary or literature-plus-DMS positives** | Proceed to Task 5 validation. Report pilot as successful enough to test whether new Layer A labels improve quorum behavior. DMS-only positives do not satisfy Branch A unless explicitly curator-upgraded. |
| **Branch B: 1/3 targets gets ≥10 high-confidence literature-primary or curator-upgraded positives** | Proceed with the 1 successful target; include lower-confidence or DMS-only targets only in clearly labeled sensitivity tables, not the headline labeled-LOPO summary. Report as partial pilot, not full quorum test. |
| **Branch C: 0/3 targets get ≥10 high-confidence literature-primary or curator-upgraded positives** | Reframe as "pilot 3 attempted, demonstrating Layer A bottleneck is real." Do not run headline validation; write evidence-sparsity report. |
| **Branch D: coordinate mapping unresolved for any target** | Exclude unresolved positions from integration. If >25% of candidate positives are unresolved, pause for human coordinate review before validation. |
| **Branch E: evidence dominated by DMS only** | Run literature-primary validation as the headline if any literature-primary labels exist; run DMS-inclusive validation only as sensitivity and label the branch `DMS-dominated`. |
| **Branch F: evidence is broad region-level only** | Human curator decides whether region boundaries are precise enough. If not, target remains unlabeled for validation. |
| **Branch G: validation worsens or quorum still fails** | Report that labels alone did not resolve the Wave 4 stability bottleneck; next step becomes richer feature generation or broader curation, not overclaiming. |
| **Branch H: sparse mixed success** | Do not describe "1 successful target plus two weak targets" as a three-target pilot success; report the number of primary-gated targets explicitly. |
---
## Implementation Tasks
## Task 1: Wave 5 scaffold + automated PubMed/DMS search (auto)
**Why:** Establishes a reproducible evidence inventory before any manual label decisions are made.
**Automatable:** Yes. Codex/general scripts may execute this task.
**Files:**
- Create: `results/mutbench/codex_wave5/README.md`
- Create: `paper/dissertation/review/2026-05-01/wave5/`
- Create: `results/mutbench/codex_wave5/w5_search_queries.csv`
- Create: `results/mutbench/codex_wave5/w5_pubmed_hits.csv`
- Create: `results/mutbench/codex_wave5/w5_biorxiv_hits.csv`
- Create: `results/mutbench/codex_wave5/w5_dms_catalog_hits.csv`
- Create: `results/mutbench/codex_wave5/w5_source_inventory.csv`
- Create: `scripts/codex_w5_layerA_curation.py`
- [ ] Create `results/mutbench/codex_wave5/`, `results/mutbench/codex_wave5/worksheets/`, and `paper/dissertation/review/2026-05-01/wave5/`.
- [ ] Write README stating fixed target set, manual label boundary, and Wave 4 motivation.
- [ ] Implement `scripts/codex_w5_layerA_curation.py --search-only`.
- [ ] Run PubMed E-utilities using only the locked keyword sets above.
- [ ] Run bioRxiv search/API/RSS mining using the same biological concepts.
- [ ] Query or download relevant DMS/escape catalogs if stable URLs are available; otherwise record `catalog_unavailable`.
- [ ] Emit `w5_search_queries.csv` with exact query strings, dates, hit counts, and retained zero-hit queries.
- [ ] Emit source inventories with PMID/DOI/preprint ID, title, year, target, evidence type, and abstract/snippet if available.
- [ ] Write `paper/dissertation/review/2026-05-01/wave5/w5_task1_search_inventory.md`.
**Stop condition:** If network access or APIs fail, record the failure and stop. Do not continue using remembered literature.
---
## Task 2: Per-position evidence aggregation + worksheet generation (auto)
**Why:** Converts paper/catalog-level evidence into a position-indexed worksheet that the human curator can review efficiently.
**Automatable:** Yes. Codex/general scripts may execute this task, but only through `proposed_label`.
**Files:**
- Output: `results/mutbench/codex_wave5/w5_position_evidence_long.csv`
- Output: `results/mutbench/codex_wave5/w5_coordinate_mapping_audit.csv`
- Output: `results/mutbench/codex_wave5/worksheets/yfv_e_layerA_worksheet.csv`
- Output: `results/mutbench/codex_wave5/worksheets/lassa_gpc_layerA_worksheet.csv`
- Output: `results/mutbench/codex_wave5/worksheets/wnv_e_layerA_worksheet.csv`
- Output: `paper/dissertation/review/2026-05-01/wave5/w5_task2_worksheet_generation.md`
- [ ] Load `data/cross_pathogen/yfv_e_position_scores.csv`, `lassa_gpc_position_scores.csv`, and `wnv_e_position_scores.csv`.
- [ ] Load `results/mutbench/pilot_accession_manifest.csv` and record `n_seq_filtered`, `query_date`, accession-list path, and FASTA SHA-256 for each target.
- [ ] Extract candidate residue positions from titles, abstracts, DMS tables, supplementary tables, and catalog records.
- [ ] Build `w5_position_evidence_long.csv` with one row per `(target, position, source, evidence_type)` and evidence-basis fields needed to distinguish primary literature from DMS sensitivity evidence.
- [ ] Build `w5_coordinate_mapping_audit.csv` with `source_position`, `source_residue`, `target_position`, `target_residue`, `mapping_basis`, `offset`, `aa_mismatch`, `mapping_confidence`, `reference_accession`, source coordinate system, target coordinate system, mapping method, AA match status, reference protein lengths, inferred offsets, cleavage-site assumptions, and source-to-target coordinate equation.
- [ ] Generate one worksheet per target using the required schema.
- [ ] Fill `proposed_label` only as advisory: `1` for strong mapped evidence, `0` for no evidence, `needs_review` for weak/conflicting/mapping-sensitive evidence.
- [ ] Leave `label_confidence`, `notes`, `final_label`, `curator`, and `curation_date` blank; Task 2 must never copy `proposed_label` into any human-owned column.
- [ ] Write a worksheet-generation report with counts by target: candidate evidence sources, mapped positions, `needs_review`, and mapping conflicts.
**Hard boundary:** Do not create feature matrices with `layer_a` in Task 2.
---
## Task 3: HUMAN curation pause point — deliver worksheets to user
**Why:** This is the Layer A decision step. It is the scientific bottleneck Wave 4 identified.
**Automatable:** No. This task requires the human researcher's domain judgment.
**Files requiring human completion:**
- `results/mutbench/codex_wave5/worksheets/yfv_e_layerA_worksheet.csv`
- `results/mutbench/codex_wave5/worksheets/lassa_gpc_layerA_worksheet.csv`
- `results/mutbench/codex_wave5/worksheets/wnv_e_layerA_worksheet.csv`
- `results/mutbench/codex_wave5/worksheets/human_curation_approval.csv`
- [ ] Human reviews evidence summaries and original sources as needed.
- [ ] Human resolves coordinate mapping concerns and AA mismatches.
- [ ] Human fills `label_confidence`, `notes`, `final_label`, `curator`, and `curation_date`.
- [ ] Human confirms whether weak evidence and DMS-only evidence should be included in primary or sensitivity labels.
- [ ] Human confirms target-level branch: A, B, C, D, E, F, G, or H.
**Checkpoint:** Stop here and wait for human input. This is not auto-resumable. Codex must not proceed to integration or validation until the user explicitly provides completed worksheets or instructs Codex where to read them. Resume requires a separate `results/mutbench/codex_wave5/worksheets/human_curation_approval.csv` containing target_slug, curator, curation_date, reviewed_source_files, and `approved_for_integration=true`.
---
## Task 4: Resume — Layer A CSV integration + feature_matrix update (auto)
**Why:** Converts human-reviewed worksheets into benchmark-compatible feature matrices.
**Automatable:** Yes, after human checkpoint only.
**Files:**
- Output: `results/mutbench/codex_wave5/layerA/yfv_e_layerA.csv`
- Output: `results/mutbench/codex_wave5/layerA/lassa_gpc_layerA.csv`
- Output: `results/mutbench/codex_wave5/layerA/wnv_e_layerA.csv`
- Output: `results/mutbench/codex_wave5/feature_matrix_YFV.csv`
- Output: `results/mutbench/codex_wave5/feature_matrix_Lassa.csv`
- Output: `results/mutbench/codex_wave5/feature_matrix_WNV.csv`
- Output: `results/mutbench/codex_wave5/w5_layerA_integration_audit.csv`
- Output: `paper/dissertation/review/2026-05-01/wave5/w5_task4_layerA_integration.md`
- [ ] Validate all worksheet rows have `final_label ∈ {0,1}`, `curator`, and `curation_date`. Also validate that `human_curation_approval.csv` exists and covers every target being integrated.
- [ ] Fail closed if any `final_label` is missing or non-binary.
- [ ] Fail closed if `final_label` exactly equals `proposed_label` for all non-empty evidence rows without explicit curator attestation in `human_curation_approval.csv`.
- [ ] Export target-specific Layer A CSVs with `position,layer_a_primary,layer_a_dms_sensitivity,evidence_basis,label_confidence,mapping_confidence,evidence_sources,curator,curation_date`.
- [ ] Align the three existing `position,frequency,entropy,hscore,ground_truth` inputs to the 12-panel schema pattern in `results/mutbench/feature_analysis/feature_matrix_Norovirus.csv`.
- [ ] Create feature matrices with at minimum `position,freq,entropy,layer_a`, where headline `layer_a` is derived from `layer_a_primary`; include `hscore` only as auxiliary metadata unless the validation script explicitly uses it.
- [ ] Preserve unavailable 10-feature columns as absent rather than fabricating values.
- [ ] Emit integration audit with `n_positions`, `n_layer_a_primary_pos`, `n_layer_a_dms_sensitivity_pos`, `layer_a_prev`, `n_high_label_confidence_primary_pos`, `n_low_label_confidence_primary_pos`, evidence-basis counts, and branch status.
**Validation gate:** If any target has fewer than 10 total positives or fewer than 10 high-confidence literature-primary or curator-upgraded literature-plus-DMS positives for headline validation, mark it as `curation_sparse=true` and apply the predeclared failure branch before Task 5.
---
## Task 5: Validation — `12->15 labeled within 28 unique targets` rerun + report (auto)
**Why:** Tests whether changing up to three existing Wave 4 targets from unlabeled to curated-labeled status changes the Wave 4 conclusion from "feature-compatible but unlabeled" toward a bounded labeled-fold test.
**Automatable:** Yes, after Task 4 only.
**Files:**
- Modify or extend: `scripts/codex_w4_features_lopo.py` or create `scripts/codex_w5_layerA_validation.py`
- Output: `results/mutbench/codex_wave5/w5_28target_15labeled_input_inventory.csv`
- Output: `results/mutbench/codex_wave5/w5_labeled_lopo_per_fold.csv`
- Output: `results/mutbench/codex_wave5/w5_labeled_lopo_summary.csv`
- Output: `results/mutbench/codex_wave5/w5_expanded_stability_per_target.csv`
- Output: `results/mutbench/codex_wave5/w5_quorum_reachability.csv`
- Output: `results/mutbench/codex_wave5/w5_validation_summary.png`
- Output: `paper/dissertation/review/2026-05-01/wave5/w5_task5_validation.md`
- [ ] Expand the Wave 4 labeled set from 12 to up to 15 labeled targets, depending on Task 3 branch.
- [ ] Report `n_labeled_eval=12+k`, where `k` is the number of targets passing the primary curation gate, and `n_unique_targets=28` in every validation table.
- [ ] Preserve the Wave 4 no-leakage rule: signs are fit on training labeled pathogens only.
- [ ] Keep unlabeled targets out of MCC, precision, F1, enrichment, and callability endpoint performance.
- [ ] Use high/medium `label_confidence` literature-primary or curator-upgraded literature-plus-DMS positions for primary validation; report DMS-only and broad-region-only labels only as sensitivity unless explicitly curator-upgraded.
- [ ] Recompute labeled shared-feature LOPO on the labeled set using `freq+entropy` primary; do not reintroduce non-harmonized hscore as a primary feature.
- [ ] Recompute expanded stability across the unique target set: the same 28 Wave 4 unique targets, with YFV/Lassa/WNV label status changed only for targets passing Task 3/4 gates. Report exact denominators rather than relying on "n≈30".
- [ ] Report whether D1 quorum changes when the training pool includes the curated targets.
- [ ] Compare against Wave 4 baselines: labeled mean MCC=0.077, 8/12 positive folds, D1 0/12, expanded stability 1/28, 16/16 unlabeled inside envelope.
- [ ] Select and document the applicable failure-mode branch.
**Permitted claims:** Curated primary labels enable a bounded labeled-fold test for the newly curated targets that pass the manual and evidence-basis gates.  
**Forbidden claims:** The entire 28-target expanded panel is validated, or the method is deployable, unless the predeclared callability rule passes.
---
## Task 6: Codex review of validation results + memory closure (auto)
**Why:** Forces an independent bounded-claim review before results enter dissertation narrative or future plans.
**Automatable:** Yes.
**Files:**
- Create: `paper/dissertation/review/2026-05-01/codex_wave5_plan_review_prompt.md`
- Create after execution: `paper/dissertation/review/2026-05-01/codex_wave5_results_review.md`
- Create after execution: `/home/hwijun/.claude/projects/-proj-paper/memory/codex_wave5_results.md`
- Modify after execution only if user requests: `NOTES.md`
- [ ] Draft a plan review prompt using the eight questions below before Task 1 execution if external review is desired.
- [ ] After validation, draft a results review prompt focusing on label leakage, human/manual boundary, coordinate mapping, branch correctness, and claim discipline.
- [ ] Write result review with verdict: `POSITIVE`, `POSITIVE-BOUNDED`, `PARTIAL`, or `NEGATIVE`.
- [ ] Write memory only at closure with target-level curation counts, branch outcome, validation denominators, and next-step ordering.
- [ ] Do not commit unless explicitly requested.
---
## Deliverables
### Plan
- `docs/plans/2026-05-01-wave5-pilot3-layerA-curation.md`
### Scripts
- `scripts/codex_w5_layerA_curation.py`
- Optional: `scripts/codex_w5_layerA_validation.py`
- Optional extension: `scripts/codex_w4_features_lopo.py`
### Search and evidence inventories
- `results/mutbench/codex_wave5/README.md`
- `results/mutbench/codex_wave5/w5_search_queries.csv`
- `results/mutbench/codex_wave5/w5_pubmed_hits.csv`
- `results/mutbench/codex_wave5/w5_biorxiv_hits.csv`
- `results/mutbench/codex_wave5/w5_dms_catalog_hits.csv`
- `results/mutbench/codex_wave5/w5_source_inventory.csv`
- `results/mutbench/codex_wave5/w5_position_evidence_long.csv`
- `results/mutbench/codex_wave5/w5_coordinate_mapping_audit.csv`
### Human worksheets
- `results/mutbench/codex_wave5/worksheets/yfv_e_layerA_worksheet.csv`
- `results/mutbench/codex_wave5/worksheets/lassa_gpc_layerA_worksheet.csv`
- `results/mutbench/codex_wave5/worksheets/wnv_e_layerA_worksheet.csv`
- `results/mutbench/codex_wave5/worksheets/human_curation_approval.csv`
### Integrated labels and feature matrices
- `results/mutbench/codex_wave5/layerA/yfv_e_layerA.csv`
- `results/mutbench/codex_wave5/layerA/lassa_gpc_layerA.csv`
- `results/mutbench/codex_wave5/layerA/wnv_e_layerA.csv`
- `results/mutbench/codex_wave5/feature_matrix_YFV.csv`
- `results/mutbench/codex_wave5/feature_matrix_Lassa.csv`
- `results/mutbench/codex_wave5/feature_matrix_WNV.csv`
- `results/mutbench/codex_wave5/w5_layerA_integration_audit.csv`
### Validation outputs
- `results/mutbench/codex_wave5/w5_28target_15labeled_input_inventory.csv`
- `results/mutbench/codex_wave5/w5_labeled_lopo_per_fold.csv`
- `results/mutbench/codex_wave5/w5_labeled_lopo_summary.csv`
- `results/mutbench/codex_wave5/w5_expanded_stability_per_target.csv`
- `results/mutbench/codex_wave5/w5_quorum_reachability.csv`
- `results/mutbench/codex_wave5/w5_validation_summary.png`
### Reports and review
- `paper/dissertation/review/2026-05-01/wave5/w5_task1_search_inventory.md`
- `paper/dissertation/review/2026-05-01/wave5/w5_task2_worksheet_generation.md`
- `paper/dissertation/review/2026-05-01/wave5/w5_task4_layerA_integration.md`
- `paper/dissertation/review/2026-05-01/wave5/w5_task5_validation.md`
- `paper/dissertation/review/2026-05-01/codex_wave5_plan_review_prompt.md`
- `paper/dissertation/review/2026-05-01/codex_wave5_results_review.md`
### Memory
- `/home/hwijun/.claude/projects/-proj-paper/memory/codex_wave5_results.md`
---
## Codex Review Section
Ask codex for concrete edits, not a general thumbs-up. The eight review questions are:
1. **Automation boundary:** Is the plan strict enough that Codex can collect and propose evidence but cannot create final Layer A labels?
2. **Target scope:** Is the fixed YFV/Lassa/WNV pilot defensible after Wave 4's 16/16 envelope and 1/28 stability result, or should any of the three targets be deferred before searches begin?
3. **Search preregistration:** Are the locked keyword sets broad enough to avoid missing obvious immune-escape/adaptive evidence while narrow enough to avoid post-hoc cherry-picking?
4. **Layer A contract:** Does the worksheet and decision-rule design preserve Chapter 3's Layer A definition as literature-curated adaptive/diversifying positives?
5. **Coordinate risk:** Are the coordinate-mapping safeguards sufficient for YFV/WNV polyprotein numbering and Lassa GPC GP1/GP2/signal-peptide ambiguity?
6. **DMS handling:** Is the DMS threshold placeholder acceptable, or should DMS evidence be separated into a sensitivity label set rather than included in primary Layer A?
7. **Validation denominator:** After adding labels for three existing Wave 4 targets, should validation be described as `12->15 labeled within 28 unique targets` rather than "30-target" except as shorthand?
8. **Failure branches:** Are Branches A/B/C strong enough to prevent overclaiming if literature is sparse or only one target curates cleanly?
Expected review output:
- `PROCEED`, `PROCEED WITH MODIFICATIONS`, or `REVISE BEFORE PROCEED`
- concrete line-level edits to this plan
- explicit answer to whether Task 3 must remain a hard human checkpoint
---
## References
- Wave 4 plan: `docs/plans/2026-04-30-wave4-tier2-features-lopo.md`
- Wave 3 plan format: `docs/plans/2026-04-30-wave3-p6-biological-nulls.md`
- Wave 4 result review: `paper/dissertation/review/2026-04-30/codex_wave4_results_review.md`
- Wave 4 memory: `/home/hwijun/.claude/projects/-proj-paper/memory/codex_wave4_results.md`
- Layer A definition: `paper/dissertation/chapters_en/ch3_methods.tex`, Section `Layer A: Adaptive Positive Selection`
- Existing pilot manifest: `results/mutbench/pilot_accession_manifest.csv`
- Existing target features: `data/cross_pathogen/yfv_e_position_scores.csv`, `data/cross_pathogen/lassa_gpc_position_scores.csv`, `data/cross_pathogen/wnv_e_position_scores.csv`
- Existing 12-panel schema reference: `results/mutbench/feature_analysis/feature_matrix_Norovirus.csv`
---
## Self-Review Checklist
- [ ] The plan title, date, and version are present.
- [ ] Motivation explicitly cites Wave 4: 16/16 feature-compatible, 1/28 stable, Layer A required.
- [ ] Scope is fixed to YFV E, Lassa GPC, and WNV E with taxids 11089, 11620, and 11082.
- [ ] The plan does not add a fourth target.
- [ ] Mixed automation matrix distinguishes Codex/script tasks from human judgment.
- [ ] Search keywords are predeclared per target before searches run.
- [ ] Worksheet schema matches `position,wt_aa,evidence_count,evidence_sources,evidence_summary,evidence_basis,mapping_confidence,proposed_label,label_confidence,notes,final_label,curator,curation_date`.
- [ ] Codex-filled advisory columns and human-owned columns are explicitly separated.
- [ ] Decision rules are framed as human guidance, not automatic labeling.
- [ ] Failure-mode branches A/B/C are explicit.
- [ ] Task 3 is a hard checkpoint and not auto-resumable.
- [ ] Task 4 cannot run until completed human worksheets exist.
- [ ] Validation keeps unlabeled targets out of label-based metrics.
- [ ] Deliverables list exact paths.
- [ ] Codex review includes eight targeted questions.
- [ ] No manuscript edits, commits, or unrelated file changes are included in this plan.
