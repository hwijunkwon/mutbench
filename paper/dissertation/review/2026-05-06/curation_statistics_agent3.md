# Statistical Re-analysis

## A. Archived subsets (verify)

| Subset | n | omega2_LOO or subset | source |
|---|---:|---:|---|
| Full panel, evaluation level | 11 | 0.296 | `results/mutbench/cluster_bootstrap_omega_summary.csv`, `headline_full_panel_evaluation_level` |
| HCV-excluded, evaluation level | 10 | 0.253 archived; manuscript body target 0.246 | `cluster_bootstrap_omega_summary.csv`, `HCV_excluded_evaluation_level`. The CSV value is 0.253410, while the stored `body_target` column says 0.246. |
| HCV-excluded, cell level | 10 | 0.221 archived; manuscript body target 0.199 | `cluster_bootstrap_omega_summary.csv`, `HCV_excluded_cell_level`. This is the likely source of the Ch4/Ch5 0.199 body number, but the current CSV point estimate is higher. |
| HCV + Norovirus excluded, cell level | 9 | 0.212 archived; manuscript body target 0.187 | `cluster_bootstrap_omega_summary.csv`, `HCV_Noro_excluded_cell_level`. |
| 4-pathogen restricted, cell level | 4 | 0.159 archived; manuscript body target 0.137 | `cluster_bootstrap_omega_summary.csv`, `phylo_only_4pathogen_cell_level`. |
| 4-pathogen restricted, evaluation level | 4 | 0.187 | `cluster_bootstrap_omega_summary.csv`, `phylo_only_4pathogen_evaluation_level`; not directly body-reported. |
| Per-pathogen LOO range | 10 each | [0.253, 0.313] | `results/mutbench/omega_loo_pathogen_sensitivity.csv`; min HCV-excluded 0.2534, max Norovirus-excluded 0.3126, mean 0.2933, median 0.2973, SD 0.0154. |

Critical verification note: the archived files support the direction of the manuscript claims, but the exact body values 0.199/0.187/0.137 are stored as `body_target`, not as the current `omega2_mean` values. The current CSV estimates are 0.221/0.212/0.159 for those three cell-level rows.

## B. New curation-philosophy subsets

Method: I reused the archived `scripts/cluster_bootstrap_omega.py` estimator on `results/mutbench/stage3_full_results.csv` without re-running detectors. It computes scoring x pathogen omega2 from the 20 scoring x pathogen grid, with residual MS from scoring x pathogen x detector-family cells. Reported estimates are evaluation-level; cell-level estimates from pathogen x scoring x family means are in parentheses as a dependence-conservative check.

| Curation type | pathogens | n_unique | est. omega2 | method |
|---|---|---:|---:|---|
| Region-based | HCV, HIV-1 | 2 | 0.199 (cell 0.180) | Direct subset refit on 1,560 rows. Estimable but very small-n. |
| Position-based | SARS-CoV-2, Rabies | 2 | 0.110 (cell 0.096) | Direct subset refit on 1,560 rows. Rabies also has DMS-anchored evidence, so this is not fully disjoint. |
| Antigenic-site-derived | H3N2, Norovirus, Influenza_B, RSV | 4 | 0.221 (cell 0.189) | Direct subset refit on 3,120 rows. This is the most interpretable homogeneous subset because n=4 and all are stage3 pathogens. |
| DMS-anchored, stage3-available | EV-A71, Rabies | 2 | 0.047 (cell 0.052) | Direct subset refit on 1,560 rows. Zika is absent from `stage3_full_results.csv`; strict non-overlap DMS-only is EV-A71 alone and cannot estimate pathogen interaction. |

Influenza is named `Influenza_B` in the CSV. Zika is present in feature-analysis files but not in the 8,580-row stage3 grid, so no stage3 omega2 can be estimated for any subset requiring Zika.

## C. Critical ratio

- Original omega2: 0.296.
- Within homogeneous-curation subsets: region 0.199, position 0.110, antigenic-site 0.221, DMS-stage3 0.047.
- Within Layer A immune-only/intersection archive: manuscript body targets 0.199/0.187/0.137, but current archived cell-level CSV values are 0.221/0.212/0.159.
- Weighted mean across the four estimable homogeneous subset fits, weighting by subset pathogen count and allowing the Rabies overlap, is 0.160. Excluding the partial DMS category gives 0.188. Unweighted means are 0.144 and 0.177, respectively.
- Relative drop from 0.296 is therefore about 36% to 51%, depending on whether the partial DMS pair is included; the all-estimable weighted estimate gives (0.296 - 0.160) / 0.296 = 46%.

**Verdict**: 어느 정도 curation-protocol-dependent? Yes, materially. The all-panel 0.296 is not reproduced inside any homogeneous-curation subset; the strongest homogeneous subset is antigenic-site-derived at 0.221, still 25% below the headline. The region-based subset is 0.199, close to the manuscript's immune-only body number, and the position/DMS subsets are much lower. This does not prove that the entire interaction is an annotation artifact, because small-n subset omega2 is noisy and curation type is confounded with pathogen biology. But the quantitative estimate supports a nontrivial curation-protocol share, roughly one-third to one-half of the headline interaction scale.

## D. HCV/HIV-1 tautology check

- HCV: `feature_matrix_HCV.csv`, using `layer_a==1` as the HVR/HVR-derived Layer A proxy and `freq` as the tested feature. Layer A n=54, non-Layer A n=286. Strict tautology test fails: min Layer A freq = 0.0040, max non-Layer A freq = 0.7851, so not all HVR/Layer A positions have the highest frequency in the protein. Layer A is enriched: median freq 0.1235 vs 0.0120 non-Layer A; AUC P(LayerA > non) = 0.677; top-54 frequency positions contain 23/54 Layer A positions.
- HIV-1: `feature_matrix_HIV-1.csv`, using `layer_a==1` as the V-loop Layer A proxy and `entropy` as the tested feature. Layer A n=23, non-Layer A n=427. Strict tautology test fails: min Layer A entropy = 1.216, max non-Layer A entropy = 3.141. Layer A is enriched: median entropy 2.402 vs 2.000 non-Layer A; AUC = 0.730; top-23 entropy positions contain only 1/23 Layer A positions.
- Tautology score: 0/2 strict tautologies. Both reported best-feature choices are feature-enriched and partly circular in interpretation, but the feature matrices do not support the stronger claim that the results are mechanically predetermined by "all curated positions are the top feature values."

RESULT_CURATION_AGENT3: archived_omega_min=0.137 homogeneous_subset_omega_est=0.160 tautology_count=0 curation_share_estimate=46%
