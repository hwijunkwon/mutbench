# Ch3 Methods — Cycle 2 Adversarial Review

Target: `/proj/paper/paper/dissertation/chapters_en/ch3_methods.tex` (973 lines)
Reviewer: codex-style adversarial agent, cycle 2
Date: 2026-04-28

---

## A. Cycle 1 fix verification

| Cycle 1 ID | Fix expected | Status in current ch3 | Verdict |
|------------|--------------|----------------------|---------|
| C1 cutoff date | per-pathogen YYYY-MM-DD | still "December 2024" only (L131) | **NOT FIXED** |
| C2 MAFFT non-determinism | per-pathogen algorithm table | self-disclosure only (L132–133), no per-pathogen log | **NOT FIXED** |
| C3 preregistration | SOP freeze date | absent | **NOT FIXED** |
| C4 repo URL | direct in ch3 | still forward-ref to ch6 (L967) | **NOT FIXED** |
| C5 ANOVA family pre-spec | preregistered hypothesis | L890 still "exploratory rather than confirmatory" | **NOT FIXED** |
| C6 Layer C 6-pathogen sweep | Rabies/EV-A71 sweep | L317 still 4-pathogen only | **NOT FIXED** |
| Tranception/ESM-2 channel (P1) | per-pathogen ρ table | **FIXED** — Table tab:tranception_esm_correlation L657–684 added (HIV-1 ρ=0.04 disclosed) |
| Structure source (P1) | per-pathogen mapping | **FIXED** — Table tab:structure_sources L624–651 |
| 4-feature 97.6% paired-test (P1) | nested-LOPO | **DEFERRED** to ch4 (L843–864 nested-LOPO present); ch3 L922–926 still uses retrospective `\Delta` MCC framing |
| HIV-1 23/26 reconciliation | dual column | **PARTIAL** — text reconciliation at L391, but Table tab:gt_positions still single column |

**Net**: 6 of 6 Cycle 1 Critical items remain open. Two Cycle 1 P1 items (Tranception channel separation, structure source) were addressed.

---

## B. New adversarial findings (Cycle 2)

### Critical (defense-stopper)

- **B-C1 EqualWeight directional sign leakage (carry-over of Cycle-1 M8, escalated)**. L695 says signs are fit on "training pathogens" but the term is undefined inside ch3. Stage~3 nested-LOPO (ch4 L843) refits signs per fold, but the **Stage~2 EqualWeight** scoring vector that contributes to the headline ω²=0.296 uses *all 11 pathogens'* Layer~A correlations — i.e., the EqualWeight column of the 8,580 grid is fit on the same labels it is later evaluated against. This is label leakage into one of the 20 scoring channels and inflates the scoring×pathogen interaction. Severity: Critical.

- **B-C2 ω² 0.296 vs cell-level 0.234 selectivity**. L885 reports ω²=0.296 on the full 8,580-row panel and acknowledges the "effective independent unit is closer to 3,080" but the headline number reported throughout is still the cell-aggregation–inflated 0.296. Ch5 L290 (ANCOVA paragraph) gives the cell-level baseline 0.234, but ch3 itself never states the cell-level value — readers reading methods alone cannot reconstruct the demotion. Selective reporting at the methods level. Severity: Critical (cycle-1 defense risk #3).

- **B-C3 Wild-cluster bootstrap absence**. L915 reports 1,000 cluster-bootstrap resamples on n=11 clusters. ch4 L524 explicitly admits "11-cluster regime is below rule-of-thumb ≥30 … wild-cluster bootstrap … recommended for any future cycle". ch3 should disclose this in the *methods* description of CI computation, not only in ch4 sensitivity. Severity: Critical for methods honesty.

### Major

- **B-M1 Tranception channel collapse (Cycle 1 P1 audit)**. New table at L657 confirms 11 of 12 pathogens have Pearson ρ=0.64–0.84 and Spearman ρ=0.71–0.98 between "Tranception" and ESM-2 LLR. The text at L655 calls them "near-equivalent for 11 of 12 pathogens" yet both remain as separate channels in the ω² model and in Stage~3 ablation. This double-counts the same information signal; ω² for the AI-based category is mechanically inflated. The methodologically honest fix is to merge them or to re-run ω² with a single PLM channel as a sensitivity. Currently disclosed but not corrected.

- **B-M2 Time-stratified holdout missing in methods**. ch4 L198 introduces an "H3N2 time-stratified prospective sanity check" (2010–2015 train, 2016–2025 test) with prospective enrichment of zero. This is a *method* (temporal split protocol, freq cutoffs <5%/≥10%, Fisher one-sided) but ch3 nowhere defines it. A reader of ch3 cannot reproduce the prospective experiment.

- **B-M3 Bayesian hierarchical / partial-pooling method missing in ch3**. ch5 L285 reports a PyMC 5.28 partial-pooling model with explicit priors (half-Cauchy / half-Normal σ=0.2), 2 chains × 800 / 4 chains × 2,000 draws, and posteriors 0.252 / 0.319. None of this is described in ch3 — yet it is one of the four pillars used to defend the headline ω². Methods chapter omits a load-bearing inferential procedure.

- **B-M4 ANCOVA methodology missing in ch3**. ch5 L290 reports an ANCOVA fit (statsmodels Type II OLS, log(length) and Layer-A positive rate as covariates) showing 0.234 → 0.264. ch3 §3.2.5.1 (the ANOVA section) does not describe ANCOVA at all. This is an undisclosed methodological pivot used to defend the interaction.

- **B-M5 Nested-LOPO procedure description missing in ch3**. ch4 L837–839 describe a nested-LOPO with paired bootstrap (1,000 resamples, 12 folds) and sign-flip permutation (5,000 iterations) for the 4-feature core test. ch3 L922–926 only describes the in-sample leave-one-feature-out ablation; the nested-LOPO that supplies the load-bearing p=0.61 paired-delta evidence is absent from methods.

- **B-M6 Sensitivity sweep on γ=0.5 unverifiable**. L499 says γ ∈ {0.25, 0.5, 1.0} shifts MCC ±0.01 "across 11 pathogens" but no CSV path, no per-pathogen breakdown — only a one-line numeric claim with no provenance pointer (compare L682 Tranception correlation, which cites `tranception_esm_correlation.csv`).

### Minor

- **B-m1 Stability bootstrap seed sequence**: L519 says 100 iterations; L968 pins seed=42 globally, but the per-iteration seed advancement (e.g., 42…141 vs counter via default RNG) is unstated. (carry-over Cycle 1 m5)
- **B-m2 IQ-TREE / HyPhy / ESM-2 patch versions**: L615 IQ-TREE 2 (no minor), L619 HyPhy v2.5 (no minor), L688 ESM-2 checkpoint named but no HF revision SHA. (carry-over m5–m7)
- **B-m3 Permutation N for circular permutation**: L949 says "rotated by random offset k" but no N (compare label-shuffle 1,000 at L948). (carry-over m12)
- **B-m4 Levene F statistic missing**: L887 reports only "p<0.05" — no F, df. (carry-over Cycle 1 m9)
- **B-m5 BCa coverage simulation**: L914 admits coverage <95% at n=11 but does not provide simulated actual coverage. (carry-over m13)

---

## C. Reproducibility scoring (0–10 per section)

| Section | Random seed | Library version | Hyperparameters | I/O spec | Score |
|---------|-------------|-----------------|-----------------|---------|-------|
| Preprocessing (MSA, dedup, truncation) L131–135 | n/a | MAFFT v7.505 | `--auto` (non-deterministic) | partial (no per-pathogen log) | **5/10** |
| Ground truth construction L287–402 | n/a | n/a | Layer A heterogeneous; Layer B 0.5; Layer C 20% | partial (HCV caveat L389) | **6/10** |
| Scoring (20 types) L564–695 | seed=42 | ESM-2 t33_650M, no SHA; IQ-TREE 2.x, HyPhy v2.5 | FUBAR threshold 0.9 only; grid/branches missing | partial (Tranception proxy disclosed, EqualWeight sign leakage) | **6/10** |
| Detection (39 variants) L697–777 | partial (RF 42; others unstated) | n/a | Table tab:detection_variants exhaustive | good | **7/10** |
| ANOVA / ω² L881–897 | n/a | manual + statsmodels parallel | non-partial ω², Type II–like | good (script paths cited) | **7/10** |
| LOPO L899–905 | n/a | n/a | "best" = highest mean MCC across n−1 | concordance definition implicit | **6/10** |
| Friedman L906–910 | n/a | n/a | n=11 blocks, k=20 | adequate | **7/10** |
| BCa / cluster bootstrap L912–916 | seed=42 | n/a | 10,000 / 1,000 resamples | wild-cluster absence not disclosed in methods | **6/10** |
| Permutation L946–951 | n/a | n/a | label-shuffle N=1,000; circular N missing; pseudo-count missing | partial | **5/10** |
| Stage 3 RF L962 | seed=42 | sklearn (no version) | full hyperparams listed | good | **8/10** |
| Code/data L966–968 | seed=42 | Python 3.10, NumPy 1.24, SciPy 1.11 pinned | env file unnamed | URL forwarded to ch6 | **6/10** |

**Average: 6.3/10.** Detection table and Stage 3 RF are strongest; preprocessing and permutation are weakest.

---

## D. Statistical method honesty audit

1. **ω² interpretation (L885–897)**: PASS for `largest *modeled* component` framing; **FAIL on cell-level demotion** — ch3 never reports the cell-level 0.234 baseline that ch5 ANCOVA uses (B-C2).
2. **LOPO design (L899–905)**: concordance defined informally as "training-best vs test-best"; does not state whether ties are broken or how the 0.36% chance level treats family-level vs variant-level matches. Mild selective framing.
3. **Friedman test (L906–910)**: methodology adequate (n=11, k=20). Note: Demšar 2006 cited but post-hoc Nemenyi/Conover not reported despite top-20 ranking; consistent with ch4's "no reliably superior" claim, so no honesty issue, but listed for completeness.
4. **Permutation test (L946–951)**: label-shuffle N=1,000 stated; circular permutation N omitted; pseudo-count rule omitted.
5. **Bonferroni (L890)**: family of 780 (=20×39) is *post-hoc justified* — readers cannot tell whether the family was specified before observing HIV-1's 7.19×. Cycle 1 C5 finding stands.
6. **Wild-cluster bootstrap absence (B-C3)**: disclosed in ch4 but not in ch3 methods description.
7. **EqualWeight directional sign leakage (B-C1)**: undisclosed across-fold leakage for the Stage 2 EqualWeight column.

---

## E. Method coverage gaps (referenced in ch4/ch5, missing in ch3)

| Method (ch4/ch5 location) | Description ch3 | Gap |
|---------------------------|-----------------|-----|
| H3N2 time-stratified pilot (ch4 L198–225) | absent | full protocol missing |
| Bayesian partial-pooling (ch5 L285) | absent | priors, chains, draws all missing |
| ANCOVA with covariates (ch5 L290) | absent | covariate list, OLS type, formula missing |
| Nested-LOPO with sign-flip permutation (ch4 L837) | absent | sign-flip iterations, paired bootstrap N, fold definition missing |
| Region-level BCa for Stage 1 (ch3 L943–945) | present | placement issue: lives inside §3.2.5 (Stage 2 evaluation), should be tagged "Stage 1 only" (Cycle 1 M13) |
| 5.92× spatial contact enrichment (ch4 L254) | absent | C-α distance threshold, permutation N, z-statistic computation missing |
| Coalescent simulation 100 replicates (ch4 L261) | absent | simulator, parameters, replicate seeds missing |
| TreeTime ML validation (ch4 L262) | absent | TreeTime version, settings missing |
| External comparison (OPTICS, KDE) (ch5 L36) | partial — KDE in detection table; OPTICS not described | OPTICS hyperparams missing |

**At least 7 ch4/ch5 methods are not described in ch3.**

---

## F. Recommended cycle 2 edits (file:line, current → proposed, severity)

| # | File:line | Current | Proposed | Severity |
|---|-----------|---------|----------|----------|
| F1 | ch3:131 | "all available sequences as of December 2024 were downloaded" | Add a per-pathogen "Query date" column to Table tab:pathogen_data and append the GenBank query strings to a supplementary table | Critical |
| F2 | ch3:131–135 | `MAFFT v7.505 … --auto` | Append per-pathogen log of which `--auto` algorithm was actually selected (FFT-NS-2 vs L-INS-i vs G-INS-i); cite Katoh & Standley 2013 §2 for selection logic | Critical |
| F3 | ch3:885 | "ω² = 0.296" headline | Add: "Cell-level aggregation (3,080 unique scoring×family×pathogen cells) yields ω²=0.234; the evaluation-level 0.296 reflects within-cell residual contraction. The cell-level value is the more conservative reference." | Critical |
| F4 | ch3:912–916 | BCa 10,000 + cluster 1,000 | Add explicit one-sentence acknowledgement that the 11-cluster percentile bootstrap is anti-conservative for G≤30 and that wild-cluster bootstrap (Cameron 2008) is the recommended sharper alternative — currently only in ch4 | Critical |
| F5 | ch3:695 | "training pathogens" (EqualWeight sign rule) | Specify: signs are fit on (a) all 11 pathogens for the Stage 2 EqualWeight column (declared as a label-aware feature), or (b) refit per fold inside nested-LOPO (Stage 3); clarify that (a) is a leakage-aware design choice and is excluded from the LOPO-style generalization claim | Critical |
| F6 | ch3:317 | Layer C sweep "4 pathogens" | Either run sweep on all 6 DMS pathogens, or move sentence to: "Threshold robustness verified on 4/6 DMS pathogens; Rabies/EV-A71 sweep deferred to future work" | Major |
| F7 | ch3:899–905 (after) | LOPO subsection | Insert new subsubsection "Nested-LOPO 4-feature evaluation" describing: 12-fold structure, sign refit per training-pathogen set, paired bootstrap 1,000 resamples, sign-flip permutation 5,000 iterations | Major |
| F8 | ch3:881 (after) | ANOVA subsection | Insert new paragraph describing ANCOVA fit (statsmodels Type II OLS, log(length) + Layer-A positive rate as covariates, cell-level grid, 0.234 → 0.264 result); pull from ch5 L290 | Major |
| F9 | ch3:881 (after) | ANOVA subsection | Insert new paragraph "Bayesian partial-pooling cross-check" describing PyMC 5.28 priors, chain count, draw count, R-hat, and the dual posteriors (0.252 / 0.319) | Major |
| F10 | ch3:202 (after Stage 1 intro) | — | Insert new subsubsection "Time-stratified prospective protocol (H3N2 pilot)" defining the 2010–2015/2016–2020/2021–2025 split, freq<5%/≥10% emergent definition, and Fisher one-sided test | Major |
| F11 | ch3:655 | "near-equivalent for 11 of 12 pathogens" | Append: "Sensitivity ω² with Tranception channel removed (single-PLM model): ω²_{scoring×pathogen} = X.XXX. The two channels are retained in the headline model for completeness; the merged-channel sensitivity is the more conservative reference." | Major |
| F12 | ch3:499 | "shifts per-pathogen MCC by ±0.01 on average" | Add provenance: "(`results/mutbench/gamma_sensitivity.csv`, mean ± SD across 11 pathogens)" | Major |
| F13 | ch3:967 (Code & Data) | forward ref to ch6 | Inline the repository URL, commit hash, Zenodo DOI, and `environment.yml` filename directly in ch3 | Major |
| F14 | ch3:946–951 | permutation methods | Add circular permutation N (e.g., 200) and pseudo-count rule "p = (count+1)/(N+1)" | Minor |
| F15 | ch3:319 (Table dms_preprocessing) | "Mean across 2 replicates" for all 6 | Verify against original publications; H3N2 (Lee 2018) and HIV-1 (Haddox 2018) likely have ≥3 replicates | Minor |
| F16 | ch3:615, 619, 688 | IQ-TREE 2 / HyPhy v2.5 / ESM-2 | Pin patch versions (e.g., IQ-TREE 2.2.0, HyPhy 2.5.46) and ESM-2 HF revision SHA | Minor |
| F17 | ch3:887 | "Levene's test … p<0.05" | Report F statistic and df explicitly | Minor |
| F18 | ch3:914 | BCa caveat at n=11 | Cite a simulated coverage value (e.g., "≈ 88% nominal-95% under the present effect size") | Minor |
| F19 | ch3:296 | Layer A heterogeneity discussed in ch5 | One-line numeric forward-disclosure here: "Stage 2 sensitivity (ch5 §X) shows ω² = 0.234–0.296 across Layer-A normalisations" | Minor |
| F20 | ch3:943 (region-level BCa) | inside §3.2.5 (Stage 2) | Add header "(Stage 1 only)" — region-level BCa does not apply to the 11-pathogen cross-pathogen design | Minor |

---

## G. Severity summary

| Severity | Cycle 1 carryover (still open) | New in Cycle 2 | Total |
|----------|------------------------------|----------------|-------|
| Critical | 6 (C1 cutoff date, C2 MAFFT, C3 preregistration, C4 repo URL, C5 multiple-testing, C6 6-pathogen sweep) | 3 (B-C1 EqualWeight leakage, B-C2 cell-level demotion, B-C3 wild-cluster) | **9** |
| Major | 6 (M1 GISAID, M3 DMS DOI, M5 stability seed, M6 IQ-TREE bootstrap detail, M8 sign rule, M11 RF/ML boundary) | 6 (B-M1 channel merge, B-M2 time-stratified, B-M3 Bayesian, B-M4 ANCOVA, B-M5 nested-LOPO, B-M6 γ provenance) | **12** |
| Minor | ~10 carryover | 5 (B-m1–m5) | **15** |
| **Total ch3 issues identified** | | | **36** |

**Headline**: Cycle 1 produced no Critical fixes in ch3 itself; only two P1 items (Tranception channel separation table, structure source mapping) landed. The methods chapter still has nine open Critical items, dominated by reproducibility (cutoff date, MAFFT non-determinism, repo URL inline) and statistical-honesty gaps (cell-level demotion, EqualWeight leakage, wild-cluster bootstrap). The biggest *new* finding in cycle 2 is **B-C1 EqualWeight directional-sign leakage**: the Stage 2 EqualWeight column is fit on Layer-A correlations across all 11 pathogens, then evaluated against the same labels — this is undisclosed leakage into one of the 20 channels that feeds the headline ω². Recommended cycle 2 priority: F3, F5, F8, F9 (the four items that close the methodological-honesty gap between ch3 description and ch4/ch5 sensitivity analyses).
