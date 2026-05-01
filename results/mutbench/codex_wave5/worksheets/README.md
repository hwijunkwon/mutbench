# Wave 5 Task 2 Curation Worksheets

These worksheets are for human Layer A curation. Codex aggregated abstract-level residue evidence only and intentionally left `proposed_label`, `confidence`, and `final_label` blank.

## Decision Rules

- Strong evidence: >=2 independent papers OR DMS escape >X-fold -> `final_label=1`.
- Weak evidence: 1 paper or a narrow assay -> `final_label=1`, `confidence=low`, only if the curator accepts the biological relevance.
- No evidence -> `final_label=0`.
- Conflicting evidence -> flag for re-check in `notes`; default to `final_label=0` unless resolved.
- Conserved positions, especially in the YFV 17D vaccine context, should be interpreted with conservation context rather than treated as sufficient evidence alone.
- Use `curator` for your initials and `curation_date` in `YYYY-MM-DD` format.

## Columns

- Codex-filled: `position`, `wt_aa`, `evidence_count`, `evidence_sources`, `evidence_summary`.
- Human-only: `proposed_label`, `confidence`, `notes`, `final_label`, `curator`, `curation_date`.

Do not integrate Layer A labels until the human-only columns have been completed and approved in the Wave 5 human checkpoint.
