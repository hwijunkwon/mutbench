# P3 — Full 2^10 Lattice + Formal Shapley (Wave 1)

**Status:** Complete — 2026-04-30
**Plan task:** docs/plans/2026-04-30-codex-experiment-execution.md Task 2
**Verdict:** **PARTIAL FAILURE** — P3 failure-mode branch triggered (4-core lattice rank > 50/1023). Defensible finding; prose adjustment required.

## Command

```bash
cd /proj/paper && python scripts/codex_p3_full_lattice_shapley.py
```

Wall time: ~10 minutes (single core).

## Inputs

- `results/mutbench/feature_analysis/feature_matrix_*.csv` — 12 pathogens, 10 features per position, `layer_a` ground truth
- Same nested-LOPO + Pearson-fit signs + z-score-within-held-out + top-10% threshold mechanics as `feature_ablation_nested_lopo.py`

## Outputs

- `results/mutbench/codex_wave1/p3_full_lattice_1023.csv` — 1023 rows (all non-empty subsets)
- `results/mutbench/codex_wave1/p3_shapley.csv` — per-feature formal Shapley for MCC and enrichment
- `results/mutbench/codex_wave1/p3_per_pathogen_wins.csv` — 1023 × 12 = 12276 rows
- `results/mutbench/codex_wave1/p3_pareto_frontier.png` — best-of-size-k frontier with 4-core marker
- `results/mutbench/codex_wave1/p3_run.log`

## Sanity checks

| Check | Expected | Observed | Result |
|---|---|---|---|
| 4-core MCC matches `subset_selection_robustness_210combos.csv` combo_id=13 | 0.0808818486287735 | 0.0808818486287735 | **PASS (exact)** |
| Total subsets | 1023 = sum_k C(10,k) | 1023 | PASS |
| Shapley efficiency for MCC | sum(phi_f) ≈ v(N) − v(empty) = 0.069754 | 0.069754, |diff| = 0.00e+00 | **PASS (exact)** |
| Shapley efficiency for enrichment | sum(phi_f) ≈ 2.039459 | 2.039459, |diff| = 0.00e+00 | **PASS (exact)** |
| Lattice cross-check vs 210-combo CSV (all 4-of-10 rows) | identical | identical | PASS |

## Top-line findings

### 1. 4-core lattice rank: 87 / 1023 — fails the "non-arbitrary 4-core" claim

The fixed 4-core (`freq, entropy, homoplasy, plddt`) sits at rank 87 of 1023 (top 8.5%), well outside the top-50 threshold predeclared in the plan's P3 failure-mode branch. The "non-arbitrary 4-core" framing is therefore not supported by the lattice; the dissertation prose must be revised per the predeclared branch.

### 2. 3-core (`freq, entropy, homoplasy`) DOMINATES the 4-core

| Subset | MCC | Lattice rank | wins/12 vs full-10 |
|---|---|---|---|
| 3-core (`freq,entropy,homoplasy`) | **0.0866** | **27 / 1023** | 9 |
| 4-core (incl. pLDDT) | 0.0809 | 87 / 1023 | 9 |
| Delta (3-core minus 4-core) | **+0.0058** | — | — |
| Best-of-lattice (k=7, no pLDDT, no esm2_llr, no rare_freq) | 0.0968 | 1 / 1023 | 10 |
| Best 4-of-10 (`freq,entropy,homoplasy,semantic_change`) | 0.0950 | 2 / 1023 | 9 |
| Full-10 EqualWeight | 0.0698 | n/a | n/a |

The 3-core beats the 4-core by 0.006 MCC. **pLDDT addition strictly hurts.**

### 3. Formal Shapley confirms pLDDT is detrimental on average

Sorted by MCC contribution (sum = 0.069754 = v(N), efficiency exact):

| Feature | shapley_mcc | shapley_enrichment |
|---|---|---|
| homoplasy | +0.0294 | +0.555 |
| freq | +0.0220 | +0.343 |
| entropy | +0.0219 | +0.367 |
| dnds_proxy | +0.0137 | +0.233 |
| semantic_change | +0.0030 | +0.178 |
| sasa | −0.0011 | +0.175 |
| grantham | −0.0013 | +0.091 |
| **plddt** | **−0.0015** | +0.165 |
| rare_freq | −0.0019 | +0.091 |
| **esm2_llr** | **−0.0144** | **−0.158** |

Three of the ten features (esm2_llr, rare_freq, plddt) have negative or near-zero MCC contribution. esm2_llr's enrichment Shapley is also negative — the only feature that hurts both metrics.

## Failure-mode branch applied

Per `docs/plans/2026-04-30-codex-experiment-execution.md` predeclared P3 branch (rank > 50/1023):

> Replace "non-arbitrary 4-core" with "fixed historical 4-core benchmarked against the lattice." Report the best compact subset and, if a 3-core dominates, mark pLDDT optional or move to a sensitivity appendix.

**Required prose changes for Task 6 (ch4_results.tex):**
1. Drop "non-arbitrary 4-core" wording.
2. Frame the 4-core as the **fixed historical configuration** used throughout the dissertation, then benchmark it against the lattice (rank 87 / 1023, top 8.5%).
3. Report the **3-core (freq, entropy, homoplasy)** result and explicitly mark **pLDDT as optional** — the 3-core dominates the 4-core by 0.0058 MCC.
4. Report the lattice top-1 (7-feature, MCC 0.0968) as an upper bound the 4-core does not reach.
5. Show Shapley table; flag esm2_llr as a candidate for removal (negative on both MCC and enrichment).

**Required prose changes for ch5_discussion.tex Limitations:**
- pLDDT inclusion was based on prior structural-conservation literature, but the present 12-pathogen panel does not bear out a positive marginal contribution. Future work should test pLDDT on structurally diverse pathogens with high-quality predicted structures (e.g., enveloped viruses with multi-domain glycoproteins).
- Negative Shapley for esm2_llr is consistent with the v161 ESM compression and supports moving ESM-derived features to the ablation/Stage 3 sensitivity appendix rather than the headline ensemble.

## Interpretation

The result strengthens the dissertation in a non-obvious way: the failure of the "non-arbitrary 4-core" claim is offset by the discovery of a **simpler, defensible 3-core** that out-performs it. This is the type of finding the predeclared failure-mode branch was designed to handle — a negative outcome that yields a constructive scope adjustment rather than a face-saving overclaim.

**Defense narrative:** "We pre-registered a 4-core configuration based on multi-source information types. The full 1023-subset lattice (Table P3) shows a 3-core dominates by 0.006 MCC, which we report transparently. pLDDT is recommended as an optional structural extension. The 4-core remains within the top 8.5% of subsets, so its construction is not pathological — it is simply not the optimum on this 12-pathogen panel."

## Cross-references

- Lattice CSV: `results/mutbench/codex_wave1/p3_full_lattice_1023.csv`
- Shapley CSV: `results/mutbench/codex_wave1/p3_shapley.csv`
- Pareto figure: `results/mutbench/codex_wave1/p3_pareto_frontier.png`
- Existing 4-of-10 lattice (cross-check input): `results/mutbench/feature_analysis/subset_selection_robustness_210combos.csv`
- Algorithm 1 reference (v180): `paper/dissertation/chapters_en/ch4_results.tex` (alg:mutbench_coldstart, tab:cold_start_baseline_progression)
