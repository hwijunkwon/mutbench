# Deep audit Job 2 — ch2_background (≈23 pp, 2-3 chunks)

Execute the audit task NOW. Read-only. Web search OK.

Follow template at `docs/codex_prompts/2026-05-03-deep-audit-template.md`.

## Scope

- `paper/dissertation/chapters_en/ch2_background.tex` (~23 pp = 299 lines)

Chunk boundaries:
- Chunk 1: lines 1-150 (Mutation Hotspot Detection / Density-Based Clustering / DMS / PLM)
- Chunk 2: lines 151-299 (PLM cont., Genomic Surveillance, Feature Importance, Algorithm Selection, Benchmarking Gap)

## Specific items to verify

- All cited algorithms exist and are correctly characterised (DBSCAN, OPTICS,
  KDE, MutClust, Wavelet, BinSeg, Bayesian online change-point detection)
- All cited PLMs / VEP benchmarks exist and are correctly characterised
  (ESM-2, Tranception, ProteinGym, EVEREST, ViroGym, EVEscape)
- DMS dataset references (Bloom lab, etc.)
- Surveillance platforms (Nextstrain, GISAID)
- ICTV taxonomy claims
- Algorithm-selection literature (Rice 1976, Kerschke 2019)

## Web search guidance

For algorithms and PLMs, briefly verify they exist with the cited author
+ year. For DMS papers, verify the cited author published a viral DMS
study. For ProteinGym/EVEREST/ViroGym, verify recent publication years.

## Output

`paper/dissertation/review/2026-05-03/deep_audit_job2_ch2.md`

End with: `RESULT_DEEP_J2: critical=<n> major=<n> minor=<n>`

Length ≤ 3000 words.
