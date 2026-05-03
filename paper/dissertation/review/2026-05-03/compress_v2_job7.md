# Compression-check v2 Job 7 -- ch3:601-892

Scope reviewed: `paper/dissertation/chapters_en/ch3_methods.tex:601-892`.

Already-applied skip: the ANOVA robustness/BCa/wild-cluster/Bayesian area around lines 764-814 contains additional compressible prose, but it overlaps the already-done "ANOVA diagnostics 5-frame consolidation" and is not re-recommended here.

## 1. EqualWeight variant explanation as leakage-audit table

1. **Type:** table-ize-prose
2. **Current length:** ~260 words; ~0.4 pp.
3. **What it currently does:** Separates production EqualWeight from nested-LOPO EqualWeight to prevent a label-leakage misunderstanding.
4. **Compression strategy:** Replace the two long bullets plus follow-up paragraph with a 2-row table: `Variant | code path | normalization/orientation | label use | where used | claim boundary`.
   Example after-state: "Production EqualWeight uses hard-coded domain orientations, min-max scaling, and uniform 1/10 weights; it enters headline Stage 2. Nested-LOPO fits signs only on training pathogens; it is used only for the 4-core retention sensitivity."
5. **Expected page saving:** 0.3 pp.
6. **Expected score impact:** lift. The content is defense-critical, but a table makes the leakage boundary easier to inspect and less dependent on dense prose.
7. **Risk:** low.

## 2. Detector-family design rationale after the variant table

1. **Type:** move-detail-to-footnote
2. **Current length:** ~190 words beyond the table; ~0.3 pp.
3. **What it currently does:** Explains excluded supervised ML, minor detector-family variance, family-level ANOVA, and Stage 1 MutClust cross-reference after the detector table.
4. **Compression strategy:** Keep the table and move the rationale into a compact table note or one footnote; the main text only needs the design decision.
   Example after-state: "The ANOVA uses 14 families rather than 39 variants because variant counts differ by family; supervised classifiers were excluded because 9--54 positives per pathogen cannot support generalizable position-level training."
5. **Expected page saving:** 0.2 pp.
6. **Expected score impact:** neutral to lift. It removes narration after an already-informative table while preserving the fairness rationale.
7. **Risk:** low.

## 3. Experimental-design heterogeneity and mitigation paragraph

1. **Type:** consolidate-duplicate
2. **Current length:** ~180 words plus a table caption already carrying key caveats; ~0.35 pp.
3. **What it currently does:** Restates table ranges, labels pathogen as a composite factor, and lists three mitigations for uncontrolled cross-pathogen heterogeneity.
4. **Compression strategy:** Let Table `design_characteristics` carry the ranges, then use a single "limitation + mitigation" sentence or a 3-row mini-table (`confound | mitigation | residual limit`).
   Example after-state: "Because pathogen conflates biology and data availability, inference focuses on within-pathogen scoring contrasts; subsampling shows sequence count is not dominant, and minimum-size equalization would lose power without removing length or temporal confounds."
5. **Expected page saving:** 0.25 pp.
6. **Expected score impact:** lift. It sharpens the causal limitation rather than repeating the table, which should improve examiner trust.
7. **Risk:** low.

## 4. MCC rationale repeated across metric list and headline-metric paragraph

1. **Type:** consolidate-duplicate
2. **Current length:** ~420 words plus equation; ~0.7 pp.
3. **What it currently does:** Defines metrics, explains Stage 1 vs Stage 2 metric choice, defines MCC, then repeats why MCC is the headline metric and where F1/AUROC are archived.
4. **Compression strategy:** Keep the metric list, equation, and one consolidated MCC-choice paragraph; remove duplicate all-four-cells/base-rate/Chicco-Jurman language.
   Example after-state: "Stage 2 uses MCC because the 0.7--15.9% positive-rate range makes base-rate-stable, all-four-cell evaluation preferable to F1; F1, precision, recall, AUROC, and `n_detected` remain archived as supplementary metrics."
5. **Expected page saving:** 0.35 pp.
6. **Expected score impact:** lift. The metric choice becomes more decisive and less defensive without deleting the formal definition.
7. **Risk:** low.

## 5. External-license prose and bullet list

1. **Type:** move-detail-to-footnote
2. **Current length:** ~520 words; ~0.9 pp.
3. **What it currently does:** States repository/data licensing, then gives a human-readable external-resource license inventory that duplicates the machine-readable matrix.
4. **Compression strategy:** Keep the dual-license statement, repository/Zenodo pointer, and one sentence that the external-resource license matrix is authoritative; move the category-by-category inventory to appendix or supplementary provenance.
   Example after-state: "MutBench code is MIT-licensed and dissertation text/figures are CC-BY-NC 4.0. External-resource licenses are version-frozen in `external_resource_licenses.csv`; no model weights, upstream FASTA bundles, or raw third-party DMS tables are redistributed."
5. **Expected page saving:** 0.6 pp.
6. **Expected score impact:** neutral to lift. Reproducibility remains auditable through the matrix, and the main methods chapter stops reading like a license appendix.
7. **Risk:** medium. The ESM-3/EVE non-commercial boundary is useful defense material, so the compressed main text must retain the "headline grid does not depend on restricted resources" sentence.

RESULT_COMPRESS_V2_J7: candidates=5 total_pages_saved=1.7 total_score_impact=+0.2
