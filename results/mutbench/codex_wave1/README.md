# Codex Wave 1 Results — Tier 1 Method Core

- **Spec:** `paper/dissertation/review/2026-04-30/codex_full_rigor_experiment_slate.md`
- **Plan:** `docs/plans/2026-04-30-codex-experiment-execution.md`
- **Codex review of plan:** `paper/dissertation/review/2026-04-30/codex_wave1_plan_review.md`
- **Per-task reports:** `paper/dissertation/review/2026-04-30/wave1/`
- **Started:** 2026-04-30

## Experiments

| Tag | Hypothesis tested | Files |
|-----|-------------------|-------|
| **P1** | Algorithm 1 above null (4 null types: iid / circular / protein-block / local-burden), 100k permutations each | `p1_null_*.csv`, `p1_null_distribution.png` |
| **P2** | 4-core score ranks Layer A monotonically across deciles; usable as screening-budget allocator | `p2_decile_*.csv`, `p2_calibration.csv`, `p2_decision_curve.csv`, `p2_*.png` |
| **P3** | 4-core sits on Pareto frontier of full 1023-subset lattice; formal Shapley justifies each feature | `p3_full_lattice_1023.csv`, `p3_shapley.csv`, `p3_per_pathogen_wins.csv`, `p3_pareto_frontier.png` |
| **P4** | Detector-agnostic consensus (≥50% of 39 detectors) enriches Layer A above matched-size detector mean, across 5 scorings (4-core, full-10, freq, entropy, homoplasy) | `p4_consensus_*.csv`, `p4_family_agreement.csv`, `p4_consensus_stability.png` |

## Provenance (no new data collection in Wave 1)

- 12-pathogen feature matrices: `results/mutbench/feature_analysis/feature_matrix_*.csv`
- 4-core / full-10 LOPO baseline: `results/mutbench/feature_analysis/feature_ablation_nested_lopo.csv`
- 4-of-10 subset lattice (will be cross-checked exactly): `results/mutbench/feature_analysis/subset_selection_robustness_210combos.csv`
- Stage 3 detector summary: `results/mutbench/stage3_full_results.csv` (8580 rows)
  - **Note:** detector callset positions are NOT in this CSV; P4 re-runs `run_stage3_full_detectors.py` with `--save-positions` for 5 scorings.

## Predeclared failure-mode branches

See top of `docs/plans/2026-04-30-codex-experiment-execution.md`. Prose insertions in Task 6 follow the matching branch — no post-hoc framing.

## Status

- [ ] Task 1 — Scaffold (this README)
- [ ] Task 2 — P3 full lattice + formal Shapley
- [ ] Task 3 — P2 rank reliability + decision curves
- [ ] Task 4 — P1 null calibration (HARD STOP gate before Task 5)
- [ ] Task 5 — P4 detector consensus
- [ ] Task 6 — Ch4/Ch5 prose insertions
- [ ] Task 7 — Memory + index update

Updated as tasks complete.
