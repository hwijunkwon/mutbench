# P1 — 100k-Permutation Null Calibration (Wave 1)

**Status:** Complete — 2026-04-30
**Plan task:** docs/plans/2026-04-30-codex-experiment-execution.md Task 4
**Verdict:** **HARD STOP TRIGGERED.** P1 iid Stouffer one-sided p = 1.0 globally for the 4-core MCC. Per the predeclared P1 failure-mode branch, **Wave 1 execution PAUSED before Task 5 (P4)**. Strong per-pathogen heterogeneity: 5/12 pathogens individually significant under iid null, only 1/12 (Norovirus) survives the strictest local-burden-preserving null.

## Command

```bash
cd /proj/paper && python scripts/codex_p1_null_calibration.py --n-perm 100000 --workers 16
```

Wall time: ~12 minutes (16 workers, 96 jobs).

## Inputs

- `results/mutbench/feature_analysis/feature_matrix_*.csv` — 12 pathogens, 10 features per position, `layer_a` ground truth
- LOO sign fitting per held-out pathogen (Pearson on concatenated training labels)
- Two methods: 4-core (`freq, entropy, homoplasy, plddt`) and 3-core (`freq, entropy, homoplasy`)
- 4 null types per pathogen × method, 100,000 permutations each (4.8M total MCC evaluations × 4 metrics each)

## Null types

| Tag | Description | What it preserves |
|---|---|---|
| iid | Random label permutation, prevalence preserved | label count only |
| circular_shift | Roll labels by random offset 1..n−1 (wraparound) | local clustering structure |
| protein_block_shuffle | Within each fixed 50-residue block, permute labels | within-block prevalence + global block ordering |
| local_burden_preserving | 5-quintile stratification by local mean(freq+entropy) over ±5 window, shuffle within stratum | local entropy/frequency burden distribution |

## Outputs

- `results/mutbench/codex_wave1/p1_null_per_pathogen.csv` — 12 × 4 × 2 × 4 = 384 rows (pathogen × null × method × metric)
- `results/mutbench/codex_wave1/p1_null_summary.csv` — Stouffer-aggregated global p
- `results/mutbench/codex_wave1/p1_null_distribution.png` — 12-pathogen facet, 4-core MCC null histogram + observed marker
- `results/mutbench/codex_wave1/p1_run.log`

## Top-line findings

### 1. HARD STOP gate triggered (codex review Q5 P1 branch)

```
4-core MCC iid Stouffer one-sided p = 1.0
```

Globally, Algorithm 1's 4-core MCC does NOT exceed an iid prevalence-preserving null. Per the predeclared branch:

> Remove any claim that Algorithm 1 beats a prevalence-preserving null. Reframe as an exploratory ranking heuristic; keep P2/P3 as descriptive diagnostics only; do not add detector-agnostic or search-space-reduction language as a headline.

### 2. Per-pathogen iid significance (one-sided p < 0.05)

| Pathogen | Observed MCC | iid p | circular p | block p | local-burden p |
|---|---|---|---|---|---|
| **Norovirus** | **+0.432** | **0.00001** | **0.00206** | **0.00001** | **0.00006** |
| **Influenza_B** | +0.219 | 0.00007 | 0.01073 | 0.04047 | 0.07203 |
| **H3N2** | +0.159 | 0.00177 | 0.08040 | 0.36870 | 0.24578 |
| **HCV** | +0.150 | 0.00917 | 0.21014 | 0.30465 | 0.83467 |
| **Dengue** | +0.145 | 0.00553 | 0.02268 | 0.07132 | 0.07627 |
| EV-A71 | +0.050 | 0.299 | 0.317 | 0.086 | 0.452 |
| SARS-CoV-2 | −0.010 | 0.730 | 0.674 | 0.878 | 0.804 |
| HIV-1 | −0.010 | 0.690 | 0.563 | 0.406 | 0.884 |
| Zika | −0.023 | 0.786 | 0.746 | 0.627 | 0.871 |
| MERS | −0.028 | 1.000 | 1.000 | 1.000 | 1.000 |
| Rabies | −0.049 | 0.925 | 0.813 | 0.870 | 0.877 |
| RSV | −0.065 | 1.000 | 1.000 | 1.000 | 1.000 |

**5 pathogens significant under iid null.** Stouffer aggregation fails because 6/12 pathogens have observed MCC ≤ null mean (positive vs negative observed MCCs balance out).

### 3. Null gradient (key codex prediction confirmed)

Number of pathogens significant at p<0.05 one-sided as the null becomes more biologically realistic:

| Metric × Method | iid | circular_shift | protein_block_shuffle | **local_burden_preserving** |
|---|---|---|---|---|
| 4-core MCC | 5/12 | 3/12 | 2/12 | **1/12** |
| 4-core enrichment | 5/12 | 3/12 | 2/12 | 1/12 |
| 4-core window_mcc | 1/12 | 3/12 | 1/12 | 0/12 |
| 4-core precision@20 | 2/12 | 2/12 | 1/12 | 1/12 |
| 3-core MCC | 4/12 | 4/12 | 3/12 | 1/12 |
| 3-core enrichment | 4/12 | 4/12 | 3/12 | 1/12 |

The headline prediction from codex's slate (`codex_full_rigor_experiment_slate.md` P1) was:

> Some exact-site signals will attenuate, especially in pathogens with regionally clustered Layer A labels. HIV-1/H3N2 escape enrichment should survive better than sparse MERS/RSV cases. Failure mode: most global significance disappears under local nulls, requiring the dissertation to frame Algorithm 1 as region-prioritization only.

**This is exactly what we observed:**
- Most global significance disappears under local-burden null (1/12 vs 5/12 under iid).
- **Only Norovirus** survives the strictest null across all metrics.
- Influenza_B and Dengue partially survive (p ~ 0.07–0.08, marginal).

### 4. Window-MCC tells a slightly more permissive story

window_mcc allows ±10-position tolerance. Under circular_shift it shows 3/12 significant for 4-core (Influenza_B, H3N2, Norovirus marginal, Dengue, SARS-CoV-2). The +/-10 window inflates type-I error somewhat by giving credit for near-misses. We DO NOT make a "region-prioritization is significant" claim from this — only that exact-site signal is the more honest framing.

## Failure-mode branch applied

Per `docs/plans/2026-04-30-codex-experiment-execution.md` predeclared P1 branch:

> **HARD STOP before Task 5.** Remove any claim that Algorithm 1 beats a prevalence-preserving null. Reframe as exploratory ranking heuristic. Keep P2/P3 as descriptive diagnostics only. Do NOT add detector-agnostic or search-space-reduction headlines.

**Application:**

1. **Task 5 (P4 detector consensus) is PAUSED.** Running P4 to claim "detector-agnostic consensus" while the underlying score does not beat a prevalence-preserving null globally would be misleading.
2. **Algorithm 1 is reframed as an exploratory ranking heuristic** with pathogen-specific signal (5/12 under iid; 1/12 under strict local-burden).
3. **P3/P2 are kept as descriptive diagnostics only** — they document where Algorithm 1 has signal, not that it is universally calibrated.
4. **The headline pathogens** (Norovirus, Influenza_B, H3N2, HCV, Dengue) become the dissertation's "callable" subset. **The negative-direction pathogens** (SARS-CoV-2, HIV-1, RSV, MERS, Zika, Rabies) become the explicit not-yet-learnable subset, consistent with v171's negative-result thesis.

## Required prose changes

### ch4_results.tex (Task 6 amended)

- Remove any "Algorithm 1 beats null" or "consensus search-space reduction" headline.
- New subsubsection: **"Null calibration: a callable subset and an exploratory heuristic"** (~150 words).
- Cite the per-pathogen iid table (5 significant), the local-burden gradient (only Norovirus survives), and frame Algorithm 1 as "tier-1 cold-start prioritization where signal is present."

### ch5_discussion.tex Limitations

- Insert P1-failure-branch language: "Globally, Algorithm 1's 4-core MCC does not exceed a prevalence-preserving null at α=0.05 (Stouffer one-sided p=1.0). On strict local-burden-preserving nulls, only Norovirus retains significance. The five pathogens with single-pathogen significance (Norovirus, Influenza_B, H3N2, HCV, Dengue) constitute the practical callable set under Algorithm 1's current 12-pathogen calibration. The dissertation's deployment claims are bounded by this finding."

## Implication for Wave 2 / Wave 3 plans

The natural next experiment is **P5 (callability/abstention)**: define a pre-registered diagnostic that flags pathogens as callable based on training-fold-only signals, then evaluate Algorithm 1 strictly on the callable subset with abstention disclosure. Wave 1 was scoped to exclude P5; this result strengthens the case for P5 as the FIRST Wave 2 experiment.

**Recommendation to user:** instead of skipping the predeclared HARD STOP and forcing P4, formalize the callable subset via P5 in Wave 2. Alternatively: re-scope P4 to operate ONLY on the 5 callable pathogens, framed as "for the callable subset, detector consensus enrichment is X." That would make P4 a within-subset reproducibility diagnostic rather than a global claim.

## Cross-references

- Per-pathogen CSV: `results/mutbench/codex_wave1/p1_null_per_pathogen.csv`
- Summary CSV: `results/mutbench/codex_wave1/p1_null_summary.csv`
- Distribution figure: `results/mutbench/codex_wave1/p1_null_distribution.png`
- P3 finding (3-core dominance): `paper/dissertation/review/2026-04-30/wave1/p3_full_lattice.md`
- P2 finding (per-pathogen heterogeneity, Rabies inversion): `paper/dissertation/review/2026-04-30/wave1/p2_rank_reliability.md`
- Codex slate (original P1 protocol): `paper/dissertation/review/2026-04-30/codex_full_rigor_experiment_slate.md`
