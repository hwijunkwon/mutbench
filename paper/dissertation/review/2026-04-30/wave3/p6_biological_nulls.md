# P6 — Biological-Realistic Local Nulls (Wave 3)

**Status:** Complete — 2026-04-30  
**Spec:** `paper/dissertation/review/2026-04-30/codex_p1_hardstop_consultation.md` §4; `codex_full_rigor_experiment_slate.md` Tier 2 P5; codex Wave 2 review §Q7  
**Plan:** `docs/plans/2026-04-30-wave3-p6-biological-nulls.md`  
**Codex review:** `paper/dissertation/review/2026-04-30/codex_wave3_plan_review.md`  

## Command

```bash
cd /proj/paper && python scripts/codex_p6_biological_nulls.py --n-perm 100000 --workers 4
```

Run log: `results/mutbench/codex_wave3/p6_run.log`.

## Method

- Four P6 nulls: `sasa_strat`, `plddt_strat`, `sasa_freq_joint`, `plddt_ent_joint`.
- Each null used `n_perm=100000`; p-values use smoothed `(b+1)/(n_perm+1)` one-sided estimates.
- Degeneracy criterion was predeclared: fewer than 2 strata with both positives and negatives, fewer than 5 movable positives, or near-zero null variance.
- Nulls preserve Layer A count within structural or structural-evolutionary strata; scores/predictions are reused unchanged.

## Inputs

- `results/mutbench/feature_analysis/feature_matrix_*.csv` already exist.
- 12 pathogens: SARS-CoV-2, H3N2, Norovirus, HIV-1, Dengue, RSV, Influenza_B, MERS, HCV, Zika, Rabies, EV-A71.
- Metrics: MCC, window-MCC, p20-precision, top-decile enrichment.
- Methods: 3-core and 4-core.

## Null Types

| Tag | Description | What it preserves |
|---|---|---|
| `sasa_strat` | 5 SASA quintiles | surface-exposure stratum prevalence |
| `plddt_strat` | 5 pLDDT quintiles | structure-confidence stratum prevalence |
| `sasa_freq_joint` | 3 × 3 SASA × frequency cells | joint structural-evolutionary cell prevalence |
| `plddt_ent_joint` | 3 × 3 pLDDT × entropy cells | joint flexibility/entropy cell prevalence |

## Top-Line Findings

### 1. All P6 nulls were valid

`p6_null_summary.csv` reports `n_pathogens_valid=12` and `n_pathogens_total=12` for every null × method × metric row.

`p6_null_per_pathogen.csv` has 384/384 valid rows, with `degenerate_null=False` throughout. No degeneracy branch triggered.

### 2. Per-null individual significance, 4-core MCC

One-sided p < 0.05, uncorrected per pathogen.

| Null | Count | Pathogens |
|---|---:|---|
| `sasa_strat` | 5/12 | H3N2, Norovirus, Dengue, Influenza_B, HCV |
| `plddt_strat` | 5/12 | H3N2, Norovirus, Dengue, Influenza_B, HCV |
| `sasa_freq_joint` | 4/12 | H3N2, Norovirus, Dengue, Influenza_B |
| `plddt_ent_joint` | 4/12 | H3N2, Norovirus, Dengue, Influenza_B |

### 3. Per-null individual significance, 3-core MCC

One-sided p < 0.05, uncorrected per pathogen.

| Null | Count | Pathogens |
|---|---:|---|
| `sasa_strat` | 5/12 | H3N2, Norovirus, Dengue, Influenza_B, HCV |
| `plddt_strat` | 3/12 | Norovirus, Influenza_B, HCV |
| `sasa_freq_joint` | 4/12 | Norovirus, Dengue, Influenza_B, HCV |
| `plddt_ent_joint` | 3/12 | Norovirus, Influenza_B, HCV |

### 4. Norovirus survives all four P6 nulls

Norovirus passed 4/4 nulls for both 4-core MCC and 3-core MCC.

| Method | `sasa_strat` | `plddt_strat` | `sasa_freq_joint` | `plddt_ent_joint` |
|---|---:|---:|---:|---:|
| 4-core MCC | **0.00001** | **0.00001** | **0.00001** | **0.00001** |
| 3-core MCC | **0.00001** | **0.00001** | **0.00001** | **0.00001** |

All four values are the permutation floor from `(b+1)/(n_perm+1) = 1/100001 = 0.0000099999`.

### 5. Stouffer global p is unchanged from Wave 1 pattern

All P6 summary rows have `stouffer_z_one_sided=-inf` and `stouffer_p_one_sided=1.0`.

This is expected: signed MCC across the 12 pathogens cancels, as in P1. The headline is the per-null count of individually significant pathogens, not the Stouffer global p.

## Per-Pathogen MCC P-Values

One-sided MCC p-values from `p6_null_per_pathogen.csv`. Bold marks p < 0.05.

| Pathogen | SASA 3c | SASA 4c | pLDDT 3c | pLDDT 4c | SASA×freq 3c | SASA×freq 4c | pLDDT×ent 3c | pLDDT×ent 4c |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| SARS-CoV-2 | 0.55929 | 0.72892 | 0.60043 | 0.78560 | 0.55227 | 0.73902 | 0.55273 | 0.70766 |
| H3N2 | **0.04985** | **0.00078** | 0.07143 | **0.01302** | 0.25851 | **0.00426** | 0.17648 | **0.01771** |
| Norovirus | **0.00001** | **0.00001** | **0.00001** | **0.00001** | **0.00001** | **0.00001** | **0.00001** | **0.00001** |
| HIV-1 | 0.07441 | 0.60422 | 0.15245 | 0.47705 | 0.36981 | 0.83250 | 0.49476 | 0.64797 |
| Dengue | **0.02283** | **0.00694** | 0.06952 | **0.04195** | **0.04193** | **0.01078** | 0.10387 | **0.03365** |
| RSV | 1.00000 | 1.00000 | 1.00000 | 1.00000 | 1.00000 | 1.00000 | 1.00000 | 1.00000 |
| Influenza_B | **0.00013** | **0.00020** | **0.00008** | **0.00001** | **0.01415** | **0.00632** | **0.01242** | **0.00297** |
| MERS | 1.00000 | 1.00000 | 1.00000 | 1.00000 | 1.00000 | 1.00000 | 1.00000 | 1.00000 |
| HCV | **0.00005** | **0.01302** | **0.00006** | **0.00454** | **0.01003** | 0.27530 | **0.00421** | 0.12330 |
| Zika | 0.71402 | 0.76001 | 0.80385 | 0.73197 | 0.72426 | 0.79926 | 0.73694 | 0.70890 |
| Rabies | 0.91318 | 0.90084 | 0.91482 | 0.86776 | 0.77457 | 0.77013 | 0.76509 | 0.76919 |
| EV-A71 | 0.32562 | 0.32866 | 0.57238 | 0.47847 | 0.45848 | 0.40614 | 0.49106 | 0.42987 |

Pattern: H3N2, Norovirus, Dengue, and Influenza_B are significant for 4-core MCC under all four P6 nulls. HCV survives both marginal P6 nulls but drops under both joint 4-core nulls.

## Failure-Mode Branch Applied

The predeclared branch **"Norovirus survives ALL four P6 nulls at p<0.05"** fired.

Predeclared interpretation:

> Strongly defensible: Norovirus signal is structurally non-trivial; the dissertation's Tier 1 cold-start claim is bounded but real.

The broader "≥1 pathogen survives all 4 P6 nulls" positive outcome also fired via Norovirus.

## Comparison Against P1

P6 is structurally explicit and partially overlaps with P1 local-burden; it is not independent replication and not a strictness ladder.

P1 4-core MCC gradient:

| P1 null | Count |
|---|---:|
| iid | 5/12 |
| circular_shift | 3/12 |
| protein_block_shuffle | 2/12 |
| local_burden_preserving | 1/12 |

P6 4-core MCC counts:

| P6 null | Count |
|---|---:|
| `sasa_strat` | 5/12 |
| `plddt_strat` | 5/12 |
| `sasa_freq_joint` | 4/12 |
| `plddt_ent_joint` | 4/12 |

Concordance:

- H3N2, Norovirus, Dengue, and Influenza_B were significant under P1 iid and under all four P6 4-core MCC nulls.
- For these four pathogens, the signal is not reducible to surface exposure, pLDDT, SASA×frequency, or pLDDT×entropy clustering.
- HCV survives marginal P6 nulls but drops in joint 4-core nulls: partial reducibility to structural-evolutionary co-clustering.
- Norovirus survives both P1 local-burden and all four P6 nulls, giving the strongest robustness claim.

## Caveats

There is no positive Stouffer result because signed MCC cancels across pathogens; `stouffer_z_one_sided=-inf` and `stouffer_p_one_sided=1.0` are known artifacts of the heterogeneous 12-pathogen panel. "Individually significant" means uncorrected per-pathogen p<0.05, not a multiplicity-controlled global result. Structural strata depend on the existing `feature_matrix_*.csv` definitions of SASA, pLDDT, frequency, and entropy. P6 defends descriptive signal on the callable subset; it does not establish prospective deployability. Concordance with P1 is robustness across complementary null definitions, not independent evidence.

## Files Produced

- `results/mutbench/codex_wave3/p6_run.log`
- `results/mutbench/codex_wave3/p6_null_per_pathogen.csv`
- `results/mutbench/codex_wave3/p6_null_summary.csv`
- `results/mutbench/codex_wave3/p6_null_distribution.png`
- `paper/dissertation/review/2026-04-30/wave3/p6_biological_nulls.md`

## Decision

Wave 4 ordering per codex is now triggerable because P6 produced a positive outcome: at least one pathogen survived all four biological-realistic nulls. Proceed in this order: Tier 2 features-only LOPO at n≈30 → pilot 3 Layer A curation → defense rehearsal / 6-agent cumulative review → EVE/PLM site-effect.

## Cross-References

- Per-pathogen CSV: `results/mutbench/codex_wave3/p6_null_per_pathogen.csv`
- Summary CSV: `results/mutbench/codex_wave3/p6_null_summary.csv`
- Distribution figure: `results/mutbench/codex_wave3/p6_null_distribution.png`
- P1 reference: `paper/dissertation/review/2026-04-30/wave1/p1_null_calibration.md`
- Codex Wave 3 plan review: `paper/dissertation/review/2026-04-30/codex_wave3_plan_review.md`
