# Compression-check v2 Job 5 -- ch3:1-300

Scope audited: `paper/dissertation/chapters_en/ch3_methods.tex` lines 1-300. I did not re-recommend the already-applied Ch3 five-biological-points enumeration trim or any listed Ch4/Ch5 audit-ledger compressions.

## 1. Opening chapter roadmap duplicates later framework overview

1. **Type:** trim-verbose / consolidate-duplicate
2. **Current length:** ~210 words; ~0.35 pp (`ch3_methods.tex:5-11`)
3. **What it currently does:** Introduces MutBench scale, Stage 1/2/3 design, and then lists the chapter sections before the same architecture is restated in the framework overview.
4. **Compression strategy:** Keep one scale sentence and one organization sentence; move the stage explanations to the framework overview where they are already developed. Example after-state: "MutBench evaluates 20 scoring types and 14 detector families across 11 RNA-virus surface-protein MSAs against a three-layer ground truth. This chapter defines the pathogen panel, ground-truth layers, scoring/detection grid, and evaluation design."
5. **Expected page saving:** 0.15-0.25 pp
6. **Expected score impact:** lift. The chapter starts more cleanly and avoids making the examiner reconcile two near-identical stage summaries.
7. **Risk:** low

## 2. GenBank retrieval, deduplication, HMMER non-use, and MSA preprocessing block

1. **Type:** table-ize-prose / move-detail-to-footnote
2. **Current length:** ~390 words; ~0.75 pp (`ch3_methods.tex:37-42`)
3. **What it currently does:** Documents GenBank search criteria, one full SARS-CoV-2 query, query-date provenance, ambiguity filtering, exact-duplicate hashing, why CD-HIT/MMseqs2/HMMER were not used, MAFFT, scoring vectors, and truncation.
4. **Compression strategy:** Replace most procedural prose with a compact curation ledger: step, rule, rationale, provenance. Keep the exact SARS-CoV-2 query and SHA-256-vs-CD-HIT equivalence in a footnote or provenance appendix. Example after-state: "Sequence curation used complete-CDS GenBank queries, >5% ambiguity removal, exact 100% deduplication by SHA-256 hash, MAFFT v7.505 `--auto`, and minimum-length truncation; full query strings and logs are archived in the provenance CSVs."
5. **Expected page saving:** 0.4-0.6 pp
6. **Expected score impact:** lift. The reproducibility contract becomes more inspectable; details remain available without turning the methods narrative into a manifest.
7. **Risk:** medium. The exact query and "no near-duplicate clustering" choices are defense-relevant, so they should remain in a footnote or appendix rather than disappear.

## 3. MAFFT mode explanation repeats table columns and minipage note

1. **Type:** consolidate-duplicate / trim-verbose
2. **Current length:** ~170 words plus table-note space; ~0.25-0.35 pp (`ch3_methods.tex:38-40`, `46`, `70`)
3. **What it currently does:** Explains MAFFT `--auto`, reports that 10/11 pathogens used FFT-NS-2, says the table log is authoritative, then the table caption/minipage repeats the MAFFT mode rationale and EV-A71 exception.
4. **Compression strategy:** Let `tab:pathogen_data` carry the MAFFT mode and one footnote carry the EV-A71 exception; remove the separate prose paragraph about FFT-NS-2 dominance. Example after-state: "MAFFT `--auto` mode is reported per pathogen in Table X; EV-A71 selected L-INS-i because its smaller N x L product stayed below the heuristic cutoff."
5. **Expected page saving:** 0.15-0.3 pp
6. **Expected score impact:** neutral to lift. The same information becomes easier to find in one place; no evidence is lost.
7. **Risk:** low

## 4. Framework figure plus component prose repeats pipeline facts

1. **Type:** merge-paragraphs / table-ize-prose
2. **Current length:** ~260 words plus figure/caption; ~0.4-0.6 pp (`ch3_methods.tex:81-142`)
3. **What it currently does:** States the three-component pipeline, shows it in Figure 3.x, then repeats each component in three bold paragraphs with mostly the same counts and cross-references.
4. **Compression strategy:** Keep the figure and replace the three bold component paragraphs with a 3-row component ledger: component, input/output, metric/result role, section. Example after-state: "The framework has three components: ground truth construction, score-to-call generation, and multi-metric statistical evaluation (Table X/Figure X)."
5. **Expected page saving:** 0.3-0.5 pp
6. **Expected score impact:** lift. The audit-ledger pattern would make the methods architecture more gradeable and reduce repeated 20/14/39/stage language.
7. **Risk:** low-medium. Preserve the distinction that Stage 1 uses hotspot-score while Stage 2 uses MCC.

## 5. DMS Layer C prose duplicates the preprocessing table

1. **Type:** table-ize-prose / move-detail-to-footnote
2. **Current length:** ~260 words plus table caption/minipage; ~0.45-0.65 pp (`ch3_methods.tex:240-268`)
3. **What it currently does:** Explains DMS conceptually, lists six pathogens and phenotypes, gives the top-20% rule and partial threshold sweep, then repeats phenotype/source/replicate/preprocessing details in `tab:dms_preprocessing`.
4. **Compression strategy:** Keep a short conceptual definition and let the table carry phenotype, assay, replicate, score, threshold, and source. Move the 10/20/30% sweep caveat to a single table note. Example after-state: "Layer C uses per-position mean absolute DMS fitness effect; top-20% positions define DMS positives for six pathogens. Threshold robustness was checked at 10/20/30% for four sources and did not alter winning Layer-C-aligned scores."
5. **Expected page saving:** 0.25-0.45 pp
6. **Expected score impact:** lift. The current version is accurate but reads as both a tutorial and a table; compression would preserve the boundary while reducing fatigue.
7. **Risk:** medium. Do not remove the Rabies/EV-A71 missing-sweep caveat, because it prevents overclaiming threshold robustness.

RESULT_COMPRESS_V2_J5: candidates=5 total_pages_saved=1.3-2.1 total_score_impact=+0.2
