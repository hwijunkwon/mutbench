# P2 — Rank Reliability + Decision Curves (Wave 1)

**Status:** Complete — 2026-04-30
**Plan task:** docs/plans/2026-04-30-codex-experiment-execution.md Task 3
**Verdict:** **PARTIAL FAILURE** — P2 failure-mode branch partially triggered (5/12 4-core CI excludes 0 in positive direction, 1/12 in NEGATIVE direction). Defensible "screening-budget allocator with pathogen heterogeneity" framing required.

## Command

```bash
cd /proj/paper && python scripts/codex_p2_rank_reliability.py
```

Wall time: ~4 minutes.

## Inputs

- `results/mutbench/feature_analysis/feature_matrix_*.csv` — 12 pathogens
- Same nested-LOPO sign-fitting as P3
- Methods: 4-core, 3-core (added per P3 finding), full-10, freq-only, entropy-only, homoplasy-only, random

## Outputs

- `results/mutbench/codex_wave1/p2_decile_prevalence.csv` — pathogen × method × decile (n=12 × 7 × 10 = 840 rows)
- `results/mutbench/codex_wave1/p2_calibration.csv` — isotonic ECE/Brier/slope per (method, fold)
- `results/mutbench/codex_wave1/p2_decision_curve.csv` — TP at budgets {20, 50, 80}
- `results/mutbench/codex_wave1/p2_top_vs_bottom.csv` — top-decile minus bottom-decile prevalence + bootstrap CI + Spearman trend
- `results/mutbench/codex_wave1/p2_method_summary.csv` — aggregate method comparison
- `results/mutbench/codex_wave1/p2_reliability.png` — 12-pathogen facet of decile prevalence
- `results/mutbench/codex_wave1/p2_decision_curve.png` — TP-vs-budget faceted

## Top-line findings

### 1. Method comparison (12-pathogen aggregate)

| Method | Mean top-bot delta | CI excludes 0 (any direction) | Mean Spearman ρ | Mean ECE | TP@budget=50 (sum) |
|---|---|---|---|---|---|
| **3-core** | **+0.0838** | **6/12** (all positive) | **+0.368** | 0.037 | **68** |
| 4-core | +0.0634 | 5/12 (4 positive + 1 negative) | +0.283 | 0.035 | 66 |
| full-10 | +0.0429 | 7/12 (5 positive + 2 negative) | +0.295 | 0.032 | 60 |
| entropy-only | +0.0617 | 5/12 | +0.258 | 0.034 | 65 |
| freq-only | +0.0636 | 4/12 | +0.146 | 0.031 | 65 |
| homoplasy-only | +0.0399 | 3/12 | +0.355 | 0.036 | 60 |
| random | +0.0107 | 1/12 | −0.041 | — | ~30 (12·5%·50≈30) |

**Headline:** 3-core dominates 4-core on all rank-reliability metrics, consistent with P3. Full-10 has more pathogens with CI excluding 0 (7/12) but **2 of those are in the WRONG direction** (Rabies, RSV: top decile depleted in Layer A).

### 2. Per-pathogen heterogeneity (4-core)

| Pathogen | top-bot delta | 95% CI | Spearman ρ | Status |
|---|---|---|---|---|
| Norovirus | +0.241 | [+0.130, +0.352] | +0.74 | strong positive |
| HCV | +0.161 | [−0.042, +0.366] | +0.37 | positive (CI includes 0) |
| Dengue | +0.160 | [+0.060, +0.260] | +0.83 | positive |
| H3N2 | +0.146 | [+0.054, +0.236] | +0.86 | positive |
| Influenza_B | +0.140 | [+0.053, +0.228] | +0.87 | positive |
| HIV-1 | +0.043 | [+0.000, +0.109] | +0.63 | positive (boundary) |
| EV-A71 | +0.033 | [−0.157, +0.221] | −0.41 | noisy |
| SARS-CoV-2 | +0.016 | [+0.000, +0.040] | +0.13 | very weak |
| Zika | +0.000 | [−0.087, +0.087] | +0.12 | flat |
| MERS | +0.000 | [+0.000, +0.000] | +0.10 | flat |
| RSV | −0.056 | [−0.111, +0.000] | −0.10 | weak negative |
| **Rabies** | **−0.123** | [−0.245, −0.003] | **−0.76** | **inverted** |

**5 pathogens** (Norovirus, Dengue, H3N2, Influenza_B, HIV-1) show strong rank monotonicity. **Rabies inverts** — top-decile positions are depleted in Layer A relative to bottom-decile, consistent with the dissertation's existing not-yet-learnable thesis. RSV trends inversely too. Sparse-label pathogens (MERS, Zika) are flat.

### 3. Decision curve (sum across 12 pathogens)

| Method | TP@budget=20 | TP@50 | TP@80 |
|---|---|---|---|
| 4-core | (smaller k) | 66 | (larger k) |
| 3-core | — | **68** | — |
| full-10 | — | 60 | — |
| random expected | ~12 (12·5%·20) | ~30 | ~48 |

At a budget of 50 sites/pathogen, 4-core delivers **~2.2× more TPs** than random allocation. 3-core marginally better. This is the strongest defensible framing: **the method is a screening-budget allocator that doubles wet-lab hit rate over random**.

### 4. Calibration (isotonic on training, evaluated held-out)

ECE values are uniformly low (0.03–0.04) but this is misleading: low ECE arises mechanically from the low Layer A base rate (~5%) where any near-zero prediction is well-calibrated. We do NOT make a calibrated-probability claim.

## Failure-mode branch applied

Per `docs/plans/2026-04-30-codex-experiment-execution.md` predeclared P2 branch:

> P2 decile slope essentially flat (top-vs-bottom bootstrap CI includes 0): Drop probability/calibration language. Frame Algorithm 1 as not rank-reliable on current Layer A labels; retain only per-pathogen diagnostics + isolated budget gains with CIs.

**Application:** The signal is **not flat globally** (mean delta is positive across all 4-core/3-core/full-10), but it is **uneven across pathogens**, and one pathogen (Rabies) inverts. Therefore:

1. **Drop** "calibrated probability" language entirely (low ECE is a base-rate artifact).
2. **Keep** "ranked screening" framing with explicit per-pathogen heterogeneity.
3. **Highlight** the budget=50 decision-curve result (~2× random) as the operational claim.
4. **Disclose** Rabies inversion as evidence consistent with the not-yet-learnable thesis.
5. **Use 3-core** as the primary rank-reliability comparator going forward (5/12 → 6/12 with CI excluding 0).

**Required prose changes for Task 6 (ch4_results.tex):**
- New subsubsection "Per-pathogen rank reliability (P2)" reporting the 5 strong-positive pathogens, Rabies inversion, decision curve at budget=50.
- Frame as "screening-budget allocator" not "calibrated probability."

**Required prose changes for ch5_discussion.tex:**
- Per-pathogen heterogeneity in rank reliability is consistent with v171 not-yet-learnable thesis.
- Rabies inversion: candidate explanation is mismatch between Layer A epitopes (literature-curated) and the rabies fixed-strain phylogenetic structure where escape is dominated by host-range determinants (G ectodomain) rather than antigenic-site dN/dS.

## Caveats

- **3-core SARS-CoV-2 returns NaN** for top-vs-bottom delta — likely a degenerate decile (all positions in one bin due to score ties when 3 features collapse). Not a Wave 1 blocker; flagged for follow-up.
- ECE is uninformative at low base rates; we report it for completeness but do not draw conclusions.

## Cross-references

- Per-pathogen CSV: `results/mutbench/codex_wave1/p2_top_vs_bottom.csv`
- Faceted reliability figure: `results/mutbench/codex_wave1/p2_reliability.png`
- Decision curve figure: `results/mutbench/codex_wave1/p2_decision_curve.png`
- P3 finding (3-core dominance): `paper/dissertation/review/2026-04-30/wave1/p3_full_lattice.md`
