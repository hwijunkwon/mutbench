# Tier B1: Tranception--ESM-LLR per-pathogen ρ measurement report

Cycle 4 / 2026-04-28 — Tier B1 ("Tranception–ESM-LLR per-pathogen ρ 실제 측정")

## 1. Data availability check

All 12 pathogens in the benchmark have BOTH a Tranception per-position score
CSV and an ESM-2 LLR `.npy` array on disk:

- Tranception per-position CSVs (12/12):
  `results/mutbench/feature_analysis/{Pathogen}_tranception.csv`
  with columns `position, tranception_score`.
- ESM-2 LLR arrays (12/12): `results/mutbench/esm_scores/{Pathogen}_esm_llr.npy`
  as 1-D `float64` arrays indexed `0..N-1`.

Length agreement (Tranception rows | ESM array length):

| Pathogen     |  TRA |  ESM | overlap (%) |
|:-------------|-----:|-----:|------------:|
| SARS-CoV-2   | 1259 | 1259 | 100.0       |
| H3N2         |  543 |  543 | 100.0       |
| Influenza_B  |  560 |  560 | 100.0       |
| HCV          |  340 |  340 | 100.0       |
| HIV-1        |  480 |  450 |  93.75      |
| RSV          |  550 |  550 | 100.0       |
| Norovirus    |  536 |  536 | 100.0       |
| Dengue       |  490 |  490 | 100.0       |
| MERS         | 1330 | 1330 | 100.0       |
| Rabies       |  490 |  524 |  93.51      |
| EV-A71       |  260 |  297 |  87.54      |
| Zika         |  451 |  504 |  89.48      |

Where lengths disagreed, the prefix of length `min(len(TRA), len(ESM))` was used
for both vectors and the truncation is recorded in the supplementary CSV's
`sample_overlap` column.

**Available pathogens: 12 / 12. No "under preparation" rows needed.**

## 2. Measurement results (re-measured this cycle)

Reproducibility script: `scripts/measure_tranception_esm_correlation_per_pathogen.py`
Output CSV: `results/mutbench/feature_analysis/tranception_esm_correlation_per_pathogen.csv`

| Pathogen     | n_positions | sample_overlap | Pearson ρ | Pearson p           | Spearman ρ | Spearman p          | status |
|:-------------|------------:|---------------:|----------:|:--------------------|-----------:|:--------------------|:-------|
| SARS-CoV-2   |        1259 |          1.000 |     0.7535 | 3.7e-231           |     0.9635 | 0.0                 | ok     |
| H3N2         |         543 |          1.000 |     0.8030 | 1.1e-123           |     0.9654 | 6.2e-318            | ok     |
| Influenza_B  |         560 |          1.000 |     0.8248 | 2.7e-140           |     0.9392 | 3.9e-261            | ok     |
| HCV          |         340 |          1.000 |     0.7375 | 1.4e-59            |     0.9805 | 9.7e-241            | ok     |
| **HIV-1**    |         450 |          0.938 |     **0.0432** | **0.361 (n.s.)** |     **0.1579** | 7.8e-04             | ok     |
| RSV          |         550 |          1.000 |     0.8046 | 4.1e-126           |     0.9674 | 0.0                 | ok     |
| Norovirus    |         536 |          1.000 |     0.8123 | 3.8e-127           |     0.9733 | 0.0                 | ok     |
| Dengue       |         490 |          1.000 |     0.8280 | 1.1e-124           |     0.9464 | 1.0e-241            | ok     |
| **MERS**     |        1330 |          1.000 |     **0.8365** | 0.0                |     0.9627 | 0.0                 | ok     |
| Rabies       |         490 |          0.935 |     0.6793 | 1.4e-67            |     0.9486 | 4.9e-246            | ok     |
| EV-A71       |         260 |          0.875 |     0.8013 | 1.7e-59            |     0.9185 | 5.9e-106            | ok     |
| Zika         |         451 |          0.895 |     0.6435 | 4.5e-54            |     0.7126 | 4.0e-71             | ok     |

Highlighted pathogens for the discussion anchor:

- **Highest Pearson ρ (most collinear)**: MERS, ρ = 0.8365, n = 1330.
- **Lowest Pearson ρ (most dissociated)**: HIV-1, ρ = 0.0432, p = 0.361 (n.s.), n = 450.
- **Lowest Spearman ρ within the collinear band** (excluding HIV-1):
  Zika, ρ = 0.7126; the 11 collinear pathogens all sit in 0.713 ≤ Spearman ρ ≤ 0.980
  and 0.643 ≤ Pearson ρ ≤ 0.836.
- **SARS-CoV-2 (the headline-claim pathogen)**: Pearson ρ = 0.7535,
  Spearman ρ = 0.9635, n = 1259 — sits squarely in the collinear band.

## 3. ch5:279 paragraph update

**Before** (placeholder, range only, single dissociation example):

> Per-pathogen correlations between this proxy channel and the standalone
> ESM-2 LLR channel are high for 11 of 12 pathogens (Pearson ρ = 0.64–0.84,
> Spearman ρ = 0.71–0.98) and only HIV-1 dissociates the two
> (Pearson ρ = 0.04, n.s.).

**After** (actual measured values, named extremes, supplementary CSV cited):

> The actual per-pathogen correlations between this proxy channel and the
> standalone ESM-2 LLR channel were re-measured at the position level for
> the cycle-4 audit
> (`scripts/measure_tranception_esm_correlation_per_pathogen.py`;
> reproducible CSV:
> `results/mutbench/feature_analysis/tranception_esm_correlation_per_pathogen.csv`,
> with full `n_positions`, `sample_overlap`, p-value, and `status` columns)
> and exhibit the following structure: 11 of 12 pathogens are operationally
> near-equivalent (Pearson ρ = 0.643–0.836, Spearman ρ = 0.713–0.980, all
> p < 10⁻⁵⁰), with **MERS most collinear (Pearson ρ = 0.836, n = 1330)** and
> **Zika lowest within the collinear band (Pearson ρ = 0.643, n = 451)**.
> **HIV-1 is the lone dissociating case (Pearson ρ = 0.043, p = 0.36 n.s.;
> Spearman ρ = 0.158, p = 7.8 × 10⁻⁴, n = 450).** The headline
> "SARS-CoV-2 best = Tranception" result (SARS-CoV-2 itself: Pearson ρ = 0.753,
> Spearman ρ = 0.963, n = 1259) therefore lives within a regime where the two
> PLM channels are operationally near-equivalent.

The placeholder ranges have been replaced with measured values to three
decimal places, the most-collinear and most-dissociated pathogens are now
explicitly named, the SARS-CoV-2 anchor value is quoted in line, and the
supplementary CSV is cited as the load-bearing record.

## 4. ch3:678 sensitivity reference

A new line was added to the footnote of `Table~\ref{tab:tranception_esm_correlation}`
in `chapters_en/ch3_methods.tex` (just after line 708) explicitly citing the new
cycle-4 supplementary CSV and its column structure (`n_positions`,
`sample_overlap`, p-value, `status`), and pointing to the channel-redundancy
discussion in Chapter 5 (Section `sec:esm2_leakage`).

## 5. Supplementary CSV

- **Path**: `/proj/paper/results/mutbench/feature_analysis/tranception_esm_correlation_per_pathogen.csv`
- **Columns**: `pathogen, n_positions, sample_overlap, pearson_rho, pearson_p, spearman_rho, spearman_p, len_tranception, len_esm_llr, status`
- **Rows**: 12 pathogens, all `status = ok`.
- **Reproducibility**: `python3 scripts/measure_tranception_esm_correlation_per_pathogen.py`
  re-creates the CSV byte-identically; numerical values agree with the
  pre-existing rounded `tranception_esm_correlation.csv` to within float64
  rounding.

## 6. Verify + xelatex check

- `python3 paper/dissertation/verify_dissertation.py`
  → 90 PASS, 0 FAIL, 0 WARN.
- `bash paper/dissertation/build.sh digital`
  → `xelatex` completed (3 passes incl. bibtex), output 248 pages,
  no LaTeX errors, no undefined references, no undefined citations.
  PDF: `paper/dissertation/thesis_digital.pdf` (6.4 MB, 2026-04-28 15:45).

## 7. Files touched

Edited:
- `/proj/paper/paper/dissertation/chapters_en/ch5_discussion.tex` — paragraph at line 279 updated to actual measured values.
- `/proj/paper/paper/dissertation/chapters_en/ch3_methods.tex` — table footnote at line 708 extended with cycle-4 supplementary CSV reference.

Created:
- `/proj/paper/scripts/measure_tranception_esm_correlation_per_pathogen.py` — reproducible measurement driver.
- `/proj/paper/results/mutbench/feature_analysis/tranception_esm_correlation_per_pathogen.csv` — Tier B1 supplementary table.
- `/proj/paper/paper/dissertation/review/2026-04-28/cycle4/applied_tier_b1.md` — this report.

Pre-existing (unchanged, retained as the rounded LaTeX-table source):
- `/proj/paper/results/mutbench/feature_analysis/tranception_esm_correlation.csv`
- `chapters_en/ch3_methods.tex` Table `tab:tranception_esm_correlation`
  (the rounded numbers matched the new high-precision CSV; no change needed).
