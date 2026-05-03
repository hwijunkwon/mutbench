# Deep audit Job 3 — ch3_methods (≈70 pp, 7 chunks)

Execute the audit task NOW. Read-only. Web search OK.

Follow template at `docs/codex_prompts/2026-05-03-deep-audit-template.md`.

## Scope

- `paper/dissertation/chapters_en/ch3_methods.tex` (~70 pp = 892 lines)

Chunk boundaries:
- Chunk 1: lines 1-150 (Materials, Target Pathogens, Data)
- Chunk 2: lines 151-300 (Methods overview, Framework, Layer A construction)
- Chunk 3: lines 301-450 (Layer A continued, Layer B, Layer C, hotspot-score)
- Chunk 4: lines 451-600 (Stage 1 SARS-CoV-2 in-depth, MutClust variants)
- Chunk 5: lines 601-750 (Stage 2 cross-pathogen, scoring formulas, detection families)
- Chunk 6: lines 751-892 (Evaluation/statistical design, ANOVA Diagnostic Tests)

## Specific items to verify

- 11 pathogens × surface glycoproteins × subtypes / lengths in Table 3.1 area
- 8580 evaluation = 20 scoring × 39 detector variants × 11 pathogens
- 14 detection families × 39 parameter variants
- Layer A/B/C definitions consistent with usage in ch4
- Layer A counts per pathogen (HCV 54, Rabies 39, Zika 27, EV-A71 27,
  HIV-1 26, SARS-CoV-2 25, H3N2 25, Dengue 24, RSV 20, Influenza B 17,
  Norovirus 15, MERS 9 — total 308 or 309)
- DMS Layer C availability: SARS-CoV-2, H3N2, HIV-1, RSV, Rabies, EV-A71 (6 pathogens)
- Stage 1 SARS-CoV-2 specific numbers
- ANOVA fixed-effect design rationale
- 5-frame robustness diagnostics references

## Internal data sources

Same as Job 1, plus:
- `results/mutbench/feature_analysis/feature_matrix_*.csv` — per-pathogen feature data
- `data/cross_pathogen/*_position_scores.csv` — additional 19 cross-pathogen targets

## Output

`paper/dissertation/review/2026-05-03/deep_audit_job3_ch3.md`

End with: `RESULT_DEEP_J3: critical=<n> major=<n> minor=<n>`

Length ≤ 4000 words.
