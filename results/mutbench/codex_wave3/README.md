# Codex Wave 3 Results — P6 Biological-Realistic Local Nulls

- **Spec:** codex P1 hard-stop consultation §4 + codex_full_rigor_experiment_slate Tier 2 P5 + codex Wave 2 review §Q7
- **Plan:** docs/plans/2026-04-30-wave3-p6-biological-nulls.md
- **Codex review of plan:** paper/dissertation/review/2026-04-30/codex_wave3_plan_review.md (verdict: PROCEED WITH MODIFICATIONS, 8 edits applied in v192b)
- **Started:** 2026-04-30
- **Wave 1+2 outcome:** Algorithm 1 has descriptive signal on 5 callable pathogens (Wave 1); pre-registered abstention rule yields 0/12 callable (Wave 2); defense risk medium.

## Null types (structurally explicit, not strictness ladder beyond P1)

| Tag | Stratification | Rationale |
|---|---|---|
| P6.1 SASA-stratified | 5 quintiles of solvent-accessible surface area | "surface-exposed positions" reducibility |
| P6.2 pLDDT-stratified | 5 quintiles of structure confidence | "flexible regions" reducibility |
| P6.3 SASA × freq joint | 3×3 = 9 cells | structural-evolutionary co-occurrence |
| P6.4 pLDDT × ent joint | 3×3 = 9 cells | flexible-high-entropy reducibility |

Strata computed per pathogen from existing feature_matrix CSV columns. Zero-positive cells are NOT failures — they are exactly what stratum-preserving shuffling preserves.

## Degeneracy criterion (per-pathogen, per-null)

A (pathogen, null) pair is **degenerate** (and reported as `no_result_degenerate_null`) iff at least one of:
- (a) <2 strata contain BOTH positives AND negatives (no movable labels)
- (b) <5 total movable positives
- (c) near-zero null variance (numerical degeneracy)

Otherwise compute the null normally with `(b+1)/(n_perm+1)` smoothed p-values.

## Status

- [x] Task 1 — Scaffold + plan + codex review (v192a, v192b, v192)
- [ ] Task 2 — P6 implementation (4 null types × 100k perms)
- [ ] Task 3 — P1+P6 comparative robustness figure
- [ ] Task 4 — Ch4 + Ch5 prose insertions
- [ ] Task 5 — Memory + closure

Updated as tasks complete.
