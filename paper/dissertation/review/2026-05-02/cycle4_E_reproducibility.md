# Cycle 4 Perspective E - Reproducibility Audit

Scope: external-team audit of active English build files in `paper/dissertation/chapters_en/`, public scripts under `scripts/`, and result artefacts under `results/mutbench/`. Classification uses the requested definitions and asks whether the exact headline value can be re-derived, not merely found in prose.

## 1. Per-number reproducibility table

| Headline number | Classification | Script / CSV evidence | Reproducibility command if available | Notes |
|---|---|---|---|---|
| `omega^2_scoring x pathogen = 0.296` + 95% CI `[0.195, 0.333]` | Not reproducible | `scripts/cluster_bootstrap_omega.py`; `results/mutbench/cluster_bootstrap_omega_summary.csv`; `results/mutbench/stage3_statistics.csv`; manuscript: `ch1_introduction.tex`, `ch3_methods.tex`, `ch5_discussion.tex` | `python scripts/cluster_bootstrap_omega.py` | The point estimate is reproducible (`0.2962519839` in `stage3_statistics.csv` / bootstrap summary), but the current one-command cluster bootstrap yields CI `[0.2008, 0.3455]`, while the manuscript headline reports `[0.195, 0.333]`. The archived summary even records the body target as `[0.195, 0.333]` while storing different CI columns. Exact headline CI cannot be independently re-derived from the available artefacts. |
| `omega^2_cell-level = 0.234` | Reproducible-with-effort | `scripts/ancova_omega.py`; `results/mutbench/ancova_omega_summary.csv`; manuscript: `ch3_methods.tex` Section `cell_level_omega` | `python scripts/ancova_omega.py` | The available script recomputes the cell-level baseline on the 3,080-cell grid, but the stored value is `0.232509...`, which rounds to `0.233`, not `0.234`. The artefacts support the calculation conceptually; exact headline rounding/version requires manual reconciliation or a pinned output table for the manuscript value. |
| HIV-1 enrichment `7.19x` with `p_adj = 2.5e-16` | Reproducible-with-effort | `results/mutbench/vaccine_escape_stage3.csv`; manuscript: `ch1_introduction.tex`, `ch5_discussion.tex` Section `Vaccine Escape Position Validation` | No one-shot exact command found. Manual check: load CSV, filter HIV-1, compute `p_adj = min(1, 780*p_value)`. | The CSV contains HIV-1 rows with enrichment `7.1875` and `p_value = 3.160296e-19`; multiplying by 780 gives `2.465e-16`, reported as `2.5e-16`. The Bonferroni adjustment is described in methods prose but not stored as a column. |
| Cold-start 4-core nested-LOPO mean MCC `0.081` | Reproducible | `scripts/feature_ablation_nested_lopo.py`; `results/mutbench/feature_analysis/feature_ablation_nested_lopo_summary.csv`; manuscript: `ch1_introduction.tex`, `ch3_methods.tex`, `ch4_results.tex`, `ch5_discussion.tex` | `python scripts/feature_ablation_nested_lopo.py` | Data, seed (`RANDOM_SEED = 42`), protocol, and output are present. Stored fixed-4 mean is `0.080882`, rounded to `0.081`; paired delta and CI are also present. |
| Cycle 7B six adaptive methods all failing, smallest `p = 0.56` | Not reproducible | Closest artefacts: `scripts/cycle8b_fixed_prevalence.py`; `results/mutbench/cycle8b_fixed_prevalence_summary.txt`; related PAHD-R bootstrap markdowns | No matching command found. | No exact `Cycle 7B` script/result with six adaptive methods and smallest `p = 0.56` was found. The closest six-detector comparison is Cycle 8B, but its paired Wilcoxon p-values include `0.297`, `0.476`, `0.694`, `0.845`, `0.711`, and `nan`, not a smallest p of `0.56`. |
| Wave 1 P1 100k-permutation null calibration outputs | Reproducible-with-effort | `scripts/codex_p1_null_calibration.py`; `results/mutbench/codex_wave1/p1_null_summary.csv`; `p1_null_per_pathogen.csv`; `p1_null_distribution.png`; `results/mutbench/codex_wave1/README.md`; manuscript: `ch5_discussion.tex` paragraphs `null_calibration` / `p5_callability` | `python scripts/codex_p1_null_calibration.py --n-perm 100000 --workers 1` | The script and outputs exist, and the nominal seed is `42`. However worker seeds use Python's process-dependent `hash((p, method, null_type, RANDOM_SEED))`; without a pinned `PYTHONHASHSEED`, exact bitwise regeneration is not guaranteed. An external team can reproduce the analysis design, but may not recover identical p-values. |
| Wave 5 Layer A' LOPO mean MCC `-0.055` with `2/10` positive folds | Reproducible-with-effort | `results/mutbench/codex_layerA_prime/lopo_summary.csv`; `lopo_per_fold.csv`; `per_target.csv`; `paper/dissertation/review/2026-05-02/wave5_replacement/lap_lopo_report.md`; manuscript: `ch5_discussion.tex` Paragraph `w5_layer_a_prime` | No one-shot LOPO command found. | Output CSVs are present and include `mean_mcc=-0.0554876`, `n_positive_folds=2`, `n_total_folds=10`, `random_seed=42`. Scripts exist for building Layer A' labels/features (`build_layerA_prime_labels.py`, `build_layerA_prime_feature_matrices.py`), but I did not find the public script that regenerates the LOPO summary from those matrices. |
| 1023-subset Shapley with 4-core rank `87/1023` and 3-core rank `27/1023` | Reproducible | `scripts/codex_p3_full_lattice_shapley.py`; `results/mutbench/codex_wave1/p3_full_lattice_1023.csv`; `p3_shapley.csv`; manuscript: `ch5_discussion.tex` Wave 1/P3 discussion | `python scripts/codex_p3_full_lattice_shapley.py` | Script, data, fixed features, and seed (`42`) are present. The CSV has 1,023 rows; sorting by `mean_mcc` gives 4-core rank 87 and 3-core rank 27. |
| Friedman `p = 0.990` on 11 pathogens | Reproducible | `scripts/analyze_stage3_stats.py`; `scripts/nemenyi_posthoc_friedman.py`; `results/mutbench/stage3_statistics.csv`; `results/mutbench/nemenyi_provenance.json`; manuscript: `ch1_introduction.tex`, `ch3_methods.tex`, `ch5_discussion.tex` | `python scripts/analyze_stage3_stats.py` or `python scripts/nemenyi_posthoc_friedman.py` | The archived p-value is `0.989544...`, reported as `0.990`, with 20 combos x 11 pathogens in `nemenyi_provenance.json`. |

## 2. Gaps and smallest fixes

For the omega CI headline, publish the exact bootstrap artefact that generated `[0.195, 0.333]` or update the manuscript to the current reproducible CI `[0.2008, 0.3455]`. If `[0.195, 0.333]` came from an older algorithm/version, archive that script, seed, environment, and input hash.

For the Cycle 7B six-method claim, add the missing `Cycle 7B` script and result CSV/MD, or rename the manuscript claim to the available Cycle 8B result and update the p-values. The smallest adequate artefact is a CSV with method, fold-level deltas, test used, p-value, seed, and command.

For cell-level `0.234`, either update the rounded number to match `ancova_omega_summary.csv` (`0.2325`, i.e. `0.233`) or add the exact cell-level script/output version that yields `0.234`.

For HIV-1 enrichment, add `p_adj` and correction-family columns to `vaccine_escape_stage3.csv`, or provide a one-shot `make_vaccine_escape_table.py` that emits the manuscript table directly.

For P1 null calibration, replace Python `hash()`-derived worker seeds with stable seeds, for example `hashlib.sha256(...).digest()` plus `RANDOM_SEED=42`, and document `PYTHONHASHSEED` for legacy reproduction.

For Wave 5 Layer A', publish the LOPO runner that creates `codex_layerA_prime/lopo_summary.csv` from `feature_matrix_layerA_prime/*.csv`, or add a Makefile target wrapping the current internal command.

## 3. License/access concern audit

`ch5_discussion.tex` Section `sec:code_availability` states that source code, scripts, ground truth definitions, and configuration files are archived at GitHub tag `dissertation-v1`; code is MIT, dissertation text/figures are CC-BY-NC 4.0, stochastic analyses use seed 42, and raw GISAID sequences are not redistributed.

Access concerns remain for full external reconstruction from raw data: raw GISAID FASTA bundles are explicitly not redistributed and remain under provider access controls; external model weights and upstream resources are governed by their own licenses; ESM-2/AlphaFold/HyPhy/IQ-TREE/MAFFT dependencies may require installation outside the archive. For the audited headline numbers, most reproduction depends on precomputed CSVs rather than raw FASTA, so authentication is not a blocker except for rebuilding the entire pipeline from raw sequence snapshots.

The manuscript says a Zenodo DOI "will be minted"; if still absent at release, that is an archival gap rather than a code-license conflict.

## 4. External-team time-to-reproduce estimate

Best case: 6-8 hours. This assumes a Python environment with scientific packages already installed, no full raw-feature regeneration, and reproduction from archived CSVs plus the one-shot scripts.

Realistic case: 18-30 hours. Time is spent reconciling manuscript-vs-CSV mismatches, recreating adjusted p-values, checking ranks, stabilizing P1 seed behavior, and writing small helper scripts for Layer A' and vaccine-escape table regeneration.

Worst case: 60-100+ hours. This applies if the external team attempts raw end-to-end regeneration from sequence sources, has to obtain GISAID access, install phylogenetic/PLM dependencies, and resolve stale headline values without author-side provenance.

RESULT_E: reproducible=3 with_effort=4 not_reproducible=2 total=9
