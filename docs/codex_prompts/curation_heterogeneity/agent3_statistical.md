# Agent 3 — Statistical Re-analysis: ω² within homogeneous-curation subsets

Execute the analysis NOW. Workspace-write OK. Do NOT commit.

## Reviewer concern

"If pathogen-by-pathogen Layer A curation differs (region-based vs position-based vs antigenic-site), then ω²(scoring × pathogen)=0.296 is partly measuring curation-protocol-dependence, not pathogen biology."

## Task

Compute or critically review the following subset analyses:

### A. Existing archived subsets
Verify these from `results/mutbench/`:
- HCV-excluded ω² (from `cluster_bootstrap_omega_summary.csv` HCV-excluded body)
- Immune-escape-only Layer A subsets (n=10/9/4) ω²=0.199/0.187/0.137 (Ch4 line ~453)
- Per-pathogen LOO ω² range [0.253, 0.313] (Table tab:omega_loo_pathogen_sensitivity)

### B. New subset categorization (curation philosophy)
Group 12 pathogens by curation method:
- **Region-based** (auto-include all positions in a region): HCV (HVR1/HVR2), HIV-1 (V1-V5)
- **Position-based** (per-position literature evidence): SARS-CoV-2, Rabies
- **Antigenic-site-derived** (defined by single seminal paper): H3N2 (Koel 2013), Norovirus (Lindesmith), Influenza_B (Ni 2013), RSV (Mas 2018)
- **DMS-anchored** (escape-DMS literature): partial — EV-A71 (Bakhache 2025), Zika (Sourisseau 2019), Rabies (Aditham 2025)

For each subset, decide whether ω² can be **estimated or bounded** without re-running the full ANOVA pipeline:
- Use `results/mutbench/stage3_full_results.csv` (8580 rows, 11 pathogens × 20 scoring × 39 detector)
- For each subset, retrofit the data to estimate scoring×pathogen ω² within that subset

### C. Critical ratio
The decisive number: if ω²_within_homogeneous_curation < ω²_across_all = 0.296 by a substantial margin (e.g., 0.296 → 0.15), then a meaningful fraction is curation-driven. If it stays near 0.296, the effect is robust to curation philosophy.

### D. Counter-pathology check
For HCV (region-based) and HIV-1 (region-based), independently confirm that the reported "best scoring" is mechanically determined by curation:
- HCV best = freq → does `feature_matrix_HCV.csv` show that "all HVR positions have the highest frequency in the protein"?
- HIV-1 best = entropy → does `feature_matrix_HIV-1.csv` show that "all V-loop positions have the highest entropy in the protein"?
- If yes, these results are tautological, not biological.

## Output

`paper/dissertation/review/2026-05-06/curation_statistics_agent3.md`

Structure:

```
# Statistical Re-analysis

## A. Archived subsets (verify)
| Subset | n | ω²_LOO or subset | source |

## B. New curation-philosophy subsets
| Curation type | pathogens | n_unique | est. ω² | method |

## C. Critical ratio
- Original ω²: 0.296
- Within homogeneous-curation subsets: [estimated values]
- Within Layer A-immune-only intersection: 0.199/0.187/0.137 (archived)
- **Verdict**: 어느 정도 curation-protocol-dependent? (quantitative estimate)

## D. HCV/HIV-1 tautology check
- HCV: HVR positions vs non-HVR position-level freq distribution
- HIV-1: V-loop positions vs non-V-loop position-level entropy distribution
- Tautology score: ...

RESULT_CURATION_AGENT3: archived_omega_min=<x.xxx> homogeneous_subset_omega_est=<x.xxx> tautology_count=<n> curation_share_estimate=<xx>%
```

Length: ≤ 3000 words.
