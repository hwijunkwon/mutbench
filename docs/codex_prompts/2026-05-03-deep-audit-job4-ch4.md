# Deep audit Job 4 — ch4_results (≈76 pp, 8 chunks)

Execute the audit task NOW. Read-only. Web search OK if a numerical claim
is suspicious.

Follow template at `docs/codex_prompts/2026-05-03-deep-audit-template.md`.

## Scope

- `paper/dissertation/chapters_en/ch4_results.tex` (~76 pp = 989 lines)

Chunk boundaries:
- Chunk 1: lines 1-130 (Stage 1 SARS-CoV-2 Results)
- Chunk 2: lines 131-260 (H3N2 temporal pilot, Stage 2 best scoring per pathogen)
- Chunk 3: lines 261-380 (per-pathogen biology rationales table, scoring × detector heatmap)
- Chunk 4: lines 381-500 (ANOVA results, ω² + 5-frame triangulation, Friedman, LOPO)
- Chunk 5: lines 501-630 (Cold-Start algorithm + 4-core nested-LOPO)
- Chunk 6: lines 631-770 (Cold-Start baseline progression, lattice subset audit)
- Chunk 7: lines 771-870 (Audit ledger, P1/P2/P3, P5 callability, P6 nulls)
- Chunk 8: lines 871-989 (Wave 4/5, HBFWS, Cycle 7B, vaccine-escape validation)

## Specific items to verify (numerical fact-check)

Every numerical claim in ch4 must be cross-referenced to a CSV. Most
critical:
- ω²(scoring × pathogen) = 0.296 evaluation-level → `cluster_bootstrap_omega_summary.csv`
- ω²(cell-level) = 0.234 → `ancova_omega_summary.csv`
- Friedman χ² = 7.69, p = 0.990 → `stage3_statistics.csv`
- LOPO 0/11 → check
- 4-core LOPO mean MCC = 0.081 → `feature_ablation_nested_lopo_summary.csv`
- 4-core full-lattice rank 87/1023 → `codex_wave1/p3_full_lattice_1023.csv`
- 3-core lattice rank 27/1023 with MCC 0.0866 → same
- Shapley pLDDT -0.0015, ESM-2 -0.0144 → `codex_wave1/p3_shapley.csv`
- HIV-1 enrichment 7.19× p_adj=2.5e-16 → `vaccine_escape_stage3.csv`
- HIV-1 novel-only 7.16-8.24× → same
- Cycle 7B six methods all fail → `adaptive_weighting_comparison.csv`
- HBFWS p = 0.78 → `hbfws_lopo_results.csv`
- Wave 4 mean MCC 0.077, 8/12 positive → `codex_wave4/w4_labeled_lopo_summary.csv`
- Wave 5 Layer A' MCC -0.055, 2/10 positive → `codex_layerA_prime/lopo_summary.csv`
- Counterfactual null ω² 60× above null → `cycle4_counterfactual_null.csv`
- P1 Norovirus only under strict null → `codex_wave1/p1_null_per_pathogen.csv`
- P5 0/12 callable → `codex_wave2/p5_*.csv`
- P6 4/12 individually significant → `codex_wave3/p6_*.csv`

## Output

`paper/dissertation/review/2026-05-03/deep_audit_job4_ch4.md`

End with: `RESULT_DEEP_J4: critical=<n> major=<n> minor=<n>`

Length ≤ 4000 words.
