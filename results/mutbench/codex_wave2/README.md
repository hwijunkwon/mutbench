# Codex Wave 2 Results — P5 Callability / Abstention Rule

- **Spec:** `paper/dissertation/review/2026-04-30/codex_p1_hardstop_consultation.md` §3 (4 pre-registered diagnostics + inversion guardrail)
- **Plan:** `docs/plans/2026-04-30-wave2-p5-callability.md`
- **Codex review of plan:** `paper/dissertation/review/2026-04-30/codex_wave2_plan_review.md` (verdict: PROCEED WITH MODIFICATIONS, 8 edits applied in v187b)
- **Started:** 2026-04-30
- **Wave 1 outcome:** P1+P2+P3 done v182-v185; HARD STOP triggered for Algorithm 1 global claim; P5 is the codex-specified next experiment.

## Diagnostics per fold (training-fold-only; held-out leakage limited to D4 annotation-density metadata)

| Tag | Operational definition | Default threshold |
|---|---|---|
| D1 top-decile separation | Per training pathogen, top-bot decile prevalence delta + 1k-bootstrap CI; method passes if lower CI > 0.02 AND point > 0.05 in ≥7/11 | 7/11 quorum |
| D2 null-adjusted enrichment | Per training pathogen, observed top-decile enrichment ÷ mean null enrichment under 10k iid perms; 1k-bootstrap of ratio across 11 training | lower 95% > 1.10 |
| D3 perturbation stability | 200 perturbations (0.10×SD jitter + sign re-fit on bootstrap training); Jaccard of top-10% callsets across pairs | median ≥ 0.60, 10th pct ≥ 0.40 |
| D4 sparse-label red flag | Held-out annotation-density metadata only: positive count, rankable-site count, prevalence | ≥10 pos, ≥200 pos, prev 1-20% |
| Inversion guardrail (per-method) | Not callable if ≥2 training pathogens have CI upper < 0 OR median ρ ≤ 0 | per fold-method pair |

## Endpoints

- **Primary:** mean MCC + sum TP@50 on callable held-out pathogens.
- **Secondary:** TP@20 + TP@80 (decision curves), callable fraction, coverage-performance tradeoff vs always-deploy + random policy.
- **Per-pathogen abstention reason** explicit in CSV (d1_fail, d2_fail, d3_fail, d4_fail, inversion_fail, abstention_reason).
- **Interpretive flag:** any_method_inversion (does NOT affect callability).

## Predeclared failure-mode branches

- 0/12 callable → not deployable; preserve descriptive role of P1/P2/P3; Wave 3 immediately
- 1–4/12 → report callable + abstain; do not generalise
- 5–9/12 → expected range; report performance + coverage tradeoff
- 10–12/12 → revisit thresholds for over-permissiveness
- Inversion-fired ≥1 fold → report; cross-check Rabies (P2 inversion result)

## Status

- [x] Task 1 — Scaffold + plan + codex review (v187, v187a, v187b)
- [ ] Task 2 — P5 implementation + outer LOPO + endpoints
- [ ] Task 3 — Predeclared threshold sensitivity sweep
- [ ] Task 4 — Ch4 + Ch5 prose insertions
- [ ] Task 5 — Memory + closure

Updated as tasks complete.
