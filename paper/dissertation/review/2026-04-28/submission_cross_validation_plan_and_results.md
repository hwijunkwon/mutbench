# Submission Cross-Validation Plan and Results

Date: 2026-04-28
Target: `/proj/paper/paper/dissertation`
Scope: dissertation source, digital PDF, print PDF, tables, figures, references, and deadline-readiness packaging.

## Cross-Validation Plan

| Track | Reviewer role | Purpose | Check method | Pass criterion |
|---|---|---|---|---|
| A. Build reproducibility | Primary Codex | Confirm that the thesis builds from source | `./build.sh both` | digital and print PDFs regenerate without fatal error |
| B. Independent structural audit | Codex cross-check | Re-check claims, labels, citations, and prior P0 repairs independently from the writing pass | `verify_dissertation.py`, existing codex IV&V notes | 0 FAIL / 0 WARN for automated dissertation checks |
| C. Submission-format audit | Mechanical gatekeeper | Confirm page counts, PDF metadata, figure files, labels, captions, and unresolved references | `scripts/audit_dissertation_submission_readiness.py` | all gates PASS |
| D. Figure/table audit | Visual-integrity gatekeeper | Confirm included image files exist and every float has a caption/label | source scan + PDF image listing | no missing images; no unlabeled floats; captions equal floats |
| E. Deadline-readiness audit | Final red team | Detect stale placeholders, unresolved PDF markers, severe overfull boxes, and outdated build outputs | log scan, `pdftotext`, `rg` | no TODO/FIXME; no `??`; no severe overfull >= 25pt |

## Execution Summary

### A. Build Reproducibility

Command:

```bash
cd /proj/paper/paper/dissertation
./build.sh both
```

Result: PASS.

Generated files:

| File | Pages | Created |
|---|---:|---|
| `thesis_digital.pdf` | 211 | 2026-04-28 11:06 KST |
| `thesis_print.pdf` | 212 | 2026-04-28 11:07 KST |

The print PDF has one additional page, consistent with print-mode spine/front-matter behavior.

### B. Dissertation Verification

Command:

```bash
python paper/dissertation/verify_dissertation.py
```

Result: PASS.

Summary:

| Metric | Count |
|---|---:|
| PASS | 86 |
| FAIL | 0 |
| WARN | 0 |

Covered categories include forbidden-pattern scan, key-statistic consistency, CSV-vs-table checks, LaTeX label/citation integrity, scoring formula/code consistency, permutation-test formula consistency, and MOSD/MutClust weighting.

### C. Submission Readiness Audit

Command:

```bash
python scripts/audit_dissertation_submission_readiness.py
```

Result: PASS.

Key output:

| Gate | Result |
|---|---|
| digital pages | 211 |
| print pages | 212 |
| expected print extra page | true |
| included raster figures | 18 / 18 found |
| labels | 187 |
| refs | 228 total / 107 unique |
| missing refs | 0 |
| duplicate labels | 0 |
| floats | 54 |
| captions | 54 |
| floats without label | 0 |
| fatal reference/citation log hits | 0 |
| unresolved `??` in PDF text | 0 |
| severe overfull boxes >= 25pt | 0 |

### D. Figure and Table Status

Automated source/PDF checks found:

- 18 external `\includegraphics` files, all present under the dissertation figure paths.
- 54 total floats with 54 captions.
- 0 unlabeled figure/table floats.
- PDF image extraction lists embedded raster images at expected result-figure pages.

### E. Final Adversarial Claim Audit

Command:

```bash
python scripts/audit_final_adversarial_claims.py
```

Result: PASS.

Output report: `/proj/paper/docs/final_adversarial_audit_2026-04-27.md`

## Corrections Applied During This Audit

One deadline-readiness issue was found before the final pass:

- `thesis_digital.pdf` and `thesis_print.pdf` were initially out of sync in creation time and page count because only the digital PDF had been regenerated after the latest source state.

Resolution:

- Re-ran `./build.sh both`.
- Confirmed synchronized output timestamps and expected digital/print page relationship.

One formatting quality issue was also improved:

- Three severe overfull boxes in Chapter 3 were caused by long code-like terms and formulas in method descriptions.

Resolution:

- Shortened and split the affected Chapter 3 method paragraphs without changing the methodological meaning.
- Rebuilt both PDFs.
- Confirmed severe overfull boxes dropped from 3 to 0.

## Final Verdict

Submission readiness: PASS.

Remaining non-blocking issues:

- Ordinary LaTeX overfull/underfull warnings remain, mostly from long technical terms, tables, list-of-table/list-of-figure entries, and bibliography lines.
- These are not fatal, do not indicate missing references or figures, and no severe overfull box remains under the >= 25pt threshold used for this audit.
