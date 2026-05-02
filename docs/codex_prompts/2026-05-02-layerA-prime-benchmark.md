# Codex task — Layer A' sensitivity benchmark for the cross-panel sensitivity test

You are implementing a Python benchmark script and executing it. The goal is to
produce structured-database-derived sensitivity-panel results that mirror Wave 4
LOPO's machinery. **Workspace-write OK. Do not commit.**

## Inputs (already prepared)

- 10 augmented feature matrices at `results/mutbench/feature_matrix_layerA_prime/{slug}.csv`,
  schema `position, freq, entropy, layer_a_prime`.
- Per-target inventory: `results/mutbench/layerA_prime_inventory.csv` (refined classification, prevalence).
- 12-panel reference at `results/mutbench/feature_analysis/feature_matrix_{Pathogen}.csv`,
  schema `position, freq, entropy, ..., layer_a, ...`.
- Wave 4 reference machinery at `scripts/codex_w4_features_lopo.py` — read for
  pearson sign, signed-zscore averaging, MCC, decile, paired Wilcoxon helpers.

## Context

The 10 Layer A' targets are: lassa_gpc, measles_virus_h, mumps_virus_hn,
hcov-229e_spike, hcov-nl63_spike, yfv_e, wnv_e, japanese_encephalitis_virus_e,
tick-borne_encephalitis_virus_e, eastern_equine_encephalitis_virus_e2.

Layer A' density per target (from inventory): lassa=10, measles=90, mumps=14,
hcov-229e=157, hcov-nl63=157, yfv=14, wnv=14, jev=14, tbe=14, eee=10. Per-target
prevalence range 2.0–14.5%. Note: yfv/wnv/jev/tbe share the same fusion-peptide
region annotation (98-111), so labels are correlated across the four
flaviviruses; treat this as a known confound.

## Task

Write `scripts/codex_layerA_prime_lopo.py` and run it. The script must:

### Stage 1 — Per-target sanity

For each of the 10 targets, compute:

- n_positions, n_layer_a_prime, prevalence
- raw Pearson(freq, layer_a_prime), raw Pearson(entropy, layer_a_prime)
- per-target signed-2-core score (`signs={freq:+1, entropy:+1}`-default; the
  primary is the **median Pearson sign across the OTHER 9 targets**)
- per-target MCC at the top-10% predicted threshold

Output: `results/mutbench/codex_layerA_prime/per_target.csv`

### Stage 2 — Labeled-only LOPO (10-fold)

Run leave-one-target-out:

- Training pool = 9 targets. Compute median Pearson sign per feature across the
  9 (replicate `fit_median_signs` from the Wave 4 script).
- Test target = held-out target. Score positions = signed z-score average of
  freq and entropy. Predict positives at the top 10% by score.
- Compute MCC, precision@20, top-vs-bottom decile delta + bootstrap 95% CI.

Output: `results/mutbench/codex_layerA_prime/lopo_per_fold.csv` and
`lopo_summary.csv` with mean/median MCC, sd, n_positive_folds, n_total_folds.

### Stage 3 — Sign stability bootstrap

For 1000 resamples of the 10 training targets with replacement (seed=42),
recompute median sign per feature; report what fraction of bootstraps preserve
the full-sample sign for freq and for entropy.

Output: `results/mutbench/codex_layerA_prime/sign_bootstrap.csv`

### Stage 4 — Cross-provenance comparison

Compare the Layer A' LOPO summary to the Wave 4 labeled (12-target) baseline:
- Wave 4 baseline: MCC mean=0.077, sd=0.136, 8/12 positive folds.
- Layer A' panel: report your computed MCC mean, sd, positive folds.
- Paired Wilcoxon is NOT applicable (different targets); report unpaired
  Welch t-test instead, with explicit caveat that the panels differ in
  provenance (literature-curated vs UniProt-curated) and target identity.

Output: `results/mutbench/codex_layerA_prime/cross_panel_comparison.csv`

### Stage 5 — Composite figure (optional but preferred)

4-panel PNG at `results/mutbench/codex_layerA_prime/summary_figure.png`,
14×10 in, 200dpi:
- A: per-fold MCC bars for the 10-target Layer A' LOPO
- B: prevalence vs MCC scatter (each target a dot)
- C: sign bootstrap stability bars for freq and entropy
- D: cross-panel comparison (Wave 4 vs Layer A' MCC distributions, boxplot or violin)

### Stage 6 — Per-task report

Write `paper/dissertation/review/2026-05-02/wave5_replacement/lap_lopo_report.md`
(create the directory). ≤2500 words. Include:

- Headline numbers
- Per-target table (prevalence, MCC)
- Honest caveats: (a) flavivirus label correlation, (b) small panel n=10,
  (c) UniProt feature-density bias, (d) provenance difference from 12-panel.
- Predeclared interpretive branches:
  - **Branch A**: Layer A' MCC mean ≥ 0.05 AND ≥6/10 positive folds → "Layer A'
    sensitivity panel preserves the bounded directional signal under different
    label provenance."
  - **Branch B**: 0.0 ≤ MCC mean < 0.05 OR 4–5/10 positive folds → "weak
    signal preservation; sensitivity analysis bounded but inconclusive."
  - **Branch C**: MCC mean < 0.0 OR ≤3/10 positive folds → "Layer A' label
    provenance does not preserve the signal — supports keeping 12-panel as
    primary and not extending."
- Recommendation for ch5 prose framing.

## Constraints

- Use only stdlib + pandas + numpy + scipy + matplotlib.
- Random seed 42 everywhere.
- Do not modify any file outside `scripts/codex_layerA_prime_lopo.py`,
  `results/mutbench/codex_layerA_prime/`, and the report directory.
- Do not commit.
- Sandbox network is fine to be off; you do not need any API access.

## Final reporting

Print a one-line headline at end of stdout: `RESULT: Branch=<A|B|C> MCC_mean=<x> n_positive=<n>/10`.
