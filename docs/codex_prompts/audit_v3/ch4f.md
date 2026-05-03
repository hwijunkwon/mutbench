# Audit v3 — finer 10pp chunk audit

Execute the audit task NOW. Read-only. Do not ask for confirmation. Do not commit.

## Scope

`paper/dissertation/chapters_en/ch4_results.tex` lines `619` to `742` (~10 manuscript pages).

## Goal

Independent post-v216 audit. Verify every numerical/factual claim in scope against:
- `results/mutbench/**/*.csv`
- `results/mutbench/codex_wave[1-5]/*.csv`
- `results/mutbench/codex_layerA_prime/*.csv`
- `results/mutbench/feature_analysis/*.csv`
- `paper/dissertation/references.bib`
- Cross-chapter labels via `\label{}` / `\ref{}`

## Recent-fix anchors (must NOT have regressed in v216)

- ω² CI = `[0.201, 0.346]` (cluster), phylogenetic-block = `[0.202, 0.346]`, wild-cluster = `[0.201, 0.303]`
- HIV-1 Layer A: `n=23` mapped to gp120 (used in MCC analysis); `n=26` in `layer_a_tags.csv` (curation tags)
- D614G is RETAINED in Layer A as a documented functional substitution per Korber 2020 (NOT excluded)
- Stage 1 functional regions: `417 AA` (= 1251 nt / 3), NOT `439`
- Single-position scoring (gap-aware), NOT "point substitutions only"
- P1 null at-or-below-mean: `6/12` under iid/circular (NOT 5/12); 4/12 protein-block; 7/12 local-burden
- Decision curve at budget 50 random baseline: `41` expected TPs (NOT ~30)

## Output

`paper/dissertation/review/2026-05-03/audit_v3_ch4f.md`

Structure:
1. Per-paragraph audit table: lines, claims, source check, citations, cross-refs, severity
2. Per-section severity counts (Critical / Major / Minor / Verified)
3. Recent-fix verification (one row per anchor above; PRESENT / NOT PRESENT / REGRESSION)
4. Compression candidates (paragraphs that could be compressed without information loss; ≥15-word reductions only)
5. Overall tally + one-line: `RESULT_AUDIT_V3_ch4f: critical=<n> major=<n> minor=<n> regression=<n>`

Length ≤ 2500 words.
