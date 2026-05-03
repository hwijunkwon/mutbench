# Deep audit Job 1 — abstract + ch1 (≈25 pp, 3 chunks of ~10pp each)

Execute the audit task NOW. Read-only on manuscript. Workspace-write OK
for the report file. Web search OK if needed.

Follow the template at `docs/codex_prompts/2026-05-03-deep-audit-template.md`.

## Scope

- `paper/dissertation/front_en/abstract.tex` (~3 pp)
- `paper/dissertation/chapters_en/ch1_introduction.tex` (~22 pp = 207 lines)

Chunk boundaries (approximate page counts):
- Chunk 1: abstract + ch1 lines 1-105 (~10 pp)
- Chunk 2: ch1 lines 106-207 (~12 pp)

## Internal data sources for fact-check

- `results/mutbench/stage3_full_results.csv` — 8580 evaluation grid
- `results/mutbench/cluster_bootstrap_omega_summary.csv` — ω² CIs
- `results/mutbench/feature_analysis/feature_ablation_nested_lopo_summary.csv` — 4-core LOPO
- `results/mutbench/codex_wave1/p3_full_lattice_1023.csv` — Shapley + lattice
- `results/mutbench/cycle4_counterfactual_null.csv` — counterfactual null
- `results/mutbench/codex_layerA_prime/lopo_summary.csv` — Layer A' Branch C
- `results/mutbench/vaccine_escape_stage3.csv` — HIV-1 + H3N2 + SARS-CoV-2 enrichment
- `results/mutbench/layer_a_tags.csv` — 309 Layer A positions
- `paper/dissertation/references.bib` — 126 citations

## Specific items to verify in this chapter

- The abstract's evidence-ledger numerical entries (Stage~1 0.778; ω²=0.296;
  HIV-1 7.19×; etc.)
- Contribution 3 framing: 7-9× enrichment, 20-80 positions per protein,
  ~1000 to 20-80 reduction
- The "11 RNA viruses, surface glycoproteins, point substitutions only"
  scope statement
- ch1 contribution hierarchy: are Contribution 1, 2, 3 statements
  consistent with what Ch3-5 actually deliver?
- The panel-scope summary box (~line 87 area): 11 main / 12 Stage 3 /
  Wave 4-5 — does this match active Ch3 panel definition?

## Output

Write report to:
  `paper/dissertation/review/2026-05-03/deep_audit_job1_abstract_ch1.md`

Length budget: ≤ 3000 words.

End with: `RESULT_DEEP_J1: critical=<n> major=<n> minor=<n>`
