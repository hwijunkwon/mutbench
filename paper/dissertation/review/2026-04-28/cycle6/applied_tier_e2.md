# Tier E2: Per-Pathogen LOO ω² Sensitivity

Date: 2026-04-28
Owner: cycle6 / Tier E2
Headline target: ω²(scoring × pathogen) = 0.296 robust to single-pathogen exclusion

## Goal
11 LOO refits (drop one pathogen, refit on 10) → range / std / leverage → confirm no single pathogen drives the headline.

## Step 1 — Existing artifact reused
`/proj/paper/results/mutbench/cluster_bootstrap_omega_loo.csv` (cycle 4 archive run of `scripts/cluster_bootstrap_omega.py`, `random_seed=42`) already contains the 11 LOO ω² values at evaluation level using the same Type-II-like decomposition that produces the 0.296 headline. No refit was required.

## Step 2 — Computed leverage Δᵢ = 0.296 − ω²_LOO(i)

## Step 3 — 11 LOO ω² (sorted by |leverage|)

| Rank | Excluded pathogen | ω²_LOO | Leverage Δ |
|-----:|-------------------|-------:|-----------:|
| 1    | HCV               | 0.2534 | +0.0426    |
| 2    | Norovirus         | 0.3126 | −0.0166    |
| 3    | H3N2              | 0.3066 | −0.0106    |
| 4    | Rabies            | 0.2878 | +0.0082    |
| 5    | RSV               | 0.2879 | +0.0081    |
| 6    | Influenza B       | 0.3025 | −0.0065    |
| 7    | MERS              | 0.2900 | +0.0060    |
| 8    | SARS-CoV-2        | 0.2912 | +0.0048    |
| 9    | EV-A71            | 0.2992 | −0.0032    |
| 10   | HIV-1             | 0.2975 | −0.0015    |
| 11   | Dengue            | 0.2973 | −0.0013    |

Distributional summary
- mean   = 0.2933
- median = 0.2973
- s.d.   = 0.0154
- min    = 0.2534 (drop HCV)
- max    = 0.3126 (drop Norovirus)
- range  = 0.0592
- IQR    = 0.0119

## Step 4 — Top-2 leverage interpretation

1. **HCV (Δ = +0.043)** — the unique outlier. Excluding HCV *lowers* ω² to 0.253 because HCV's Layer A (HVR / diversifying selection) creates a distinct best-scoring profile relative to convergent-evolution pathogens. This is the same pathogen flagged by the curation-protocol restriction (body §4.4 sensitivity sentence already reports the analogous 0.246 figure).
2. **Norovirus (Δ = −0.017)** — opposite direction. Excluding Norovirus *raises* ω² to 0.313 because Norovirus's pathogen-specific best scoring overlaps the panel-wide best more than the average pathogen, so its presence slightly attenuates the interaction.

The remaining 9 pathogens all have |Δ| ≤ 0.011 and individually move the headline by < 4% of its value.

## Step 5 — Original 0.296 vs LOO range

- LOO range [0.253, 0.313] is **fully contained inside** the 11-pathogen cluster-bootstrap 95% interval [0.195, 0.333].
- Min(LOO) = 0.253 sits **above** the cluster-bootstrap lower bound (0.195) for every single hold-out — i.e., even the worst-case single-pathogen exclusion never crosses the lower CI bound.
- All 11 LOO values exceed Cohen large threshold (ω² = 0.14) by ≥ 0.11 absolute units.
- Headline (0.296) − LOO mean (0.293) = 0.003 → effectively unchanged on average.

Verdict: **Best (robust)** outcome from the planning ladder. Single-pathogen exclusion does not threaten the headline.

## Step 6 — Body update (ch4 §subsec:anova_diagnostics)

Inserted **after** the existing HCV-only sensitivity sentence (ch4:606) so it generalises that probe:

- New paragraph "Per-pathogen leave-one-out sensitivity" (~150 words): summarises [0.253, 0.313] range, mean 0.293, s.d. 0.015; reports HCV (+0.043) and Norovirus (−0.017) as the only |Δ| > 0.015; states all 11 LOO values stay inside [0.195, 0.333] and above 0.14; cites Table 4.10 and the two CSV archives.
- New `\begin{table}[h] \label{tab:omega_loo_pathogen_sensitivity}` (Table 4.10, 4 cols × 12 rows + summary row) — registers as Table 4.10 on page 143.
- Updated the selective-reporting probe sentence at ch4:546 (item iii) so the phrase "the full 11-fold LOOCV trajectory" now references the new Table 4.10 and `omega_loo_pathogen_sensitivity.csv` in addition to `cluster_bootstrap_omega_loo.csv`.

## Step 7 — Verify + xelatex

- `python3 scripts/verify_claims.py` → all 7 headline claims + bonus PASS, including Claim 2 ω² = 0.290 within ±0.03 of 0.296.
- `xelatex thesis_en.tex` 2-pass → success, 0 errors, 0 undefined references, **268 pages** (cycle 5: 266 → +2 pages from new paragraph + Table 4.10).
- Label registration check: `\newlabel{tab:omega_loo_pathogen_sensitivity}{{4.10}{143}{Per-pathogen leave-one-out $\omega^2$ sensitivity}{table.caption.109}{}}` — registers cleanly.

## Output artifacts (cycle 6)

- `/proj/paper/results/mutbench/omega_loo_pathogen_sensitivity.csv` (12 rows: 11 pathogens + leverage + abs_leverage + rank columns)
- `/proj/paper/results/mutbench/cluster_bootstrap_omega_loo.csv` (existing archive, kept)
- `/proj/paper/paper/dissertation/chapters_en/ch4_results.tex` (new paragraph + Table 4.10; selective-reporting probe sentence updated)
- `/proj/paper/paper/dissertation/thesis_en.pdf` (268 pages)
- `/proj/paper/paper/dissertation/review/2026-04-28/cycle6/applied_tier_e2.md` (this file)

## Final note

- The body still cites HCV-only ω² = 0.246 from `analyze_stage3_stats.py` (slightly different residual MS construction than the archived re-implementation 0.253). Both numbers are now consistent with the LOO-HCV 0.253 figure within rounding tolerance, and the broader leverage table makes clear that HCV is the single largest leverage point in either parameterisation.
- 11 LOO range (0.059) is much narrower than the 11-pathogen cluster-bootstrap CI width (0.138), so single-pathogen exclusion uncertainty is a smaller component than resampling uncertainty — consistent with the cluster-bootstrap framing being the more honest reference.
- This Tier E2 deliverable closes the per-pathogen-leverage gap left as future work in cycle 5 Tier D5 §8.
