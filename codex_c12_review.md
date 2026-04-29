**C12 Scores**

| Axis | C11 → C12 | Rationale |
|---|---:|---|
| Methodology rigor | 8.95 → **8.90** | v176 improves claim discipline by reporting the executed Tier 1/Tier 2 pilot, including YFV/WNV low-n limits and Layer A bottleneck in [ch5_discussion.tex](/proj/paper/paper/dissertation/chapters_en/ch5_discussion.tex:295). Small regression: “27-pathogen scaffold” is not fully represented by the cited meta-feature artefact, which has 19 rows, not 27. |
| Statistical power | 8.05 → **8.05** | No real validation power is added because the new pathogens are mostly features-only with `ground_truth=-1`; the pilot supports feasibility, not inferential performance. Cycle 7B still carries the adaptive-null argument in [ch4_results.tex](/proj/paper/paper/dissertation/chapters_en/ch4_results.tex:738). |
| Novelty | 7.80 → **7.85** | The two-tier scaling roadmap and executed cross-pathogen scaffold add a useful dissertation-deadline contribution: it shows how MutBench could scale beyond the 11-pathogen validated panel without pretending the labels exist yet. |
| Writing | 8.15 → **8.05** | The new paragraph is honest but too dense and slightly over-compressed. It correctly discloses Tier 1 counts, Tier 2 success/failure, and the meta-feature ranges, but the “27-pathogen scaffold” plus 19-row CSV reference invites examiner confusion. |
| External validity | 8.15 → **8.25** | External-validity posture improves modestly: v176 shows the frequency/entropy/h-score feature path runs across additional flavivirus, alphavirus, paramyxovirus, filovirus, and coronavirus targets. Because Layer A is absent, this is breadth of feature extraction, not breadth of validated benchmark performance. |
| Reproducibility | 8.45 → **8.20** | The committed CSVs and `tier2_summary.json` help, but the download scripts depend on live Entrez search results without accession manifests, query dates, stable sorting, or committed raw FASTA snapshots for most targets. A third party may not regenerate identical FASTAs. |
| Defense readiness | 8.35 → **8.30** | Still defense-ready, but C12 adds a few avoidable examiner hooks: reproducibility of Entrez-derived FASTAs, “full-pipeline” wording despite missing Layer A annotations, and the 27-vs-19 meta-feature artefact mismatch. |

**Mean**

C12 mean: **8.23/10**  
Δ vs C11 mean 8.27: **-0.04**

**New Actionable Issues**

| Severity | Location | Issue | Resolution |
|---|---|---|---|
| **High** | [ch5_discussion.tex:295](/proj/paper/paper/dissertation/chapters_en/ch5_discussion.tex:295), [expanded_panel_metafeatures.csv:1](/proj/paper/results/mutbench/expanded_panel_metafeatures.csv:1) | Text says the 27-pathogen scaffold has the cited “panel-level meta-feature spread,” but the CSV has only 19 pathogen rows and omits 8 original-panel pathogens. | Either regenerate the CSV with all 27 pathogens or reword as “19 CSV-available scaffold/meta-feature subset.” |
| **Medium** | [download_pilot3_pathogens.py:48](/proj/paper/scripts/download_pilot3_pathogens.py:48), [download_tier2_features.py:64](/proj/paper/scripts/download_tier2_features.py:64) | Entrez downloads are not fully reproducible: no accession lockfile, no query-date manifest, no stable accession list fetch, and live NCBI contents can change. | Commit accession manifests plus checksums/query dates, and make scripts fetch by accession IDs. |
| **Medium** | [expanded_panel_metafeatures.py:2](/proj/paper/scripts/expanded_panel_metafeatures.py:2), [expanded_panel_metafeatures.py:20](/proj/paper/scripts/expanded_panel_metafeatures.py:20) | Script docstring says “expanded 27-pathogen panel,” but it only scans `data/cross_pathogen/`; the `EXISTING_11` set contains only 3 pathogens and is unused. | Make the script explicitly assemble all 27 inputs or rename it to describe the actual 19-row input set. |
| **Low** | [download_tier2_features.py:160](/proj/paper/scripts/download_tier2_features.py:160) | Cached CSVs return `n=None, L=None` but are counted as successful, so rerunning can overwrite `tier2_summary.json` with less informative counts. | On cache hit, recompute `n/L` from cached FASTA/alignment/CSV or preserve the previous summary entry. |
| **Polish** | [ch5_discussion.tex:295](/proj/paper/paper/dissertation/chapters_en/ch5_discussion.tex:295) | “Full-pipeline Tier 1” overstates the state of YFV/Lassa/WNV because position-score CSVs have `ground_truth=-1` and Layer A is still deferred. | Call it “Tier 1 sequence/features pilot” until Layer A annotations are actually curated. |

**Specific Concern Checks**

1. Numerical consistency: Tier 1 counts match modal FASTAs: YFV 27, Lassa 454, WNV 74. Tier 2 13/19 and 40-791 match `tier2_summary.json`. Meta-feature ranges match the CSV, but the CSV is 19-row, not 27-row.
2. Features-only scaffold is defensible if explicitly labeled as such. It does not invalidate the “current 11-pathogen RNA-virus form” claim, but the 27-scaffold wording needs tighter separation from validated benchmark scope.
3. Reproducibility is the weakest C12 addition: Entrez scripts are not deterministic enough for examiner-grade regeneration.
4. Yes, YFV/WNV are honestly disclosed as below the canonical `>=200` threshold.
5. The pilot modestly strengthens “panel size is the constraint, not algorithm” operationally, but not statistically; it shows scaling is feasible, not that adaptive selection now works.
6. The `expanded_panel_metafeatures.csv` reference path is correct and committed, but the file does not contain all 27 pathogens.

**Verdict**

**Defense-ready: yes**, at **8.23/10**, with one high-priority wording/artefact consistency fix recommended before submission.