# Wave 4: Tier-2 Feature Expansion and LOPO

Plan: `docs/plans/2026-04-30-wave4-tier2-features-lopo.md`

Codex review: `paper/dissertation/review/2026-04-30/codex_wave4_plan_review.md`

Task 1 is scaffold and input audit only. No LOPO model is fit here.

## Option E Hybrid

Option E preserves the 12 labeled Layer-A pathogens as the supervised
evaluation set while using the expanded cross-pathogen panel for feature-space
and schema-harmonization audits unless later tasks add labels.

Overlap audit bridges:
- `dengue_e`
- `hiv1_gp120`
- `norovirus_vp1`

## Predeclared Denominators

- `n_unique_targets=28`
- `n_labeled_eval=12`
- `n_cross_pathogen_csv=19`
- `n_overlap=3`
- `n_new_unlabeled=16`

## No-Layer-A Constraint

The 16 new cross-pathogen targets do not have Layer-A labels in this wave.
They cannot support MCC, precision, F1, enrichment, or callability claims
against Layer A. Treat them as unlabeled feature-audit targets only.

## hscore Harmonization Gate

For overlaps, labeled hscore is `freq * entropy` and is compared with the
cross-pathogen `hscore` column. A pair harmonizes only if Spearman rho >= 0.70
AND median top-10% Jaccard >= 0.50. If fewer than 2 of 3 pairs harmonize,
downstream tasks must use the predeclared 2-core fallback.

## Task Status

- [ ] Task 1: scaffold + input audit (in progress)
- [ ] Task 2: labeled-only LOPO implementation
- [ ] Task 3: expanded Option E implementation
- [ ] Task 4: analysis/reporting
- [ ] Task 5: dissertation integration
