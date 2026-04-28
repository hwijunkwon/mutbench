# Ch4 Cycle 3 Re-Attack (Phase B post-mortem)

Target: `/proj/paper/paper/dissertation/chapters_en/ch4_results.tex` (1,044 lines).
Inputs: cycle 2 review (13 substantive), `applied_ch4.md` (17 fixes claimed).
Method: line-by-line verification of each claimed fix; numerical / label / cross-chapter sync probe; supplementary forward-reference reality check.

---

## A. Phase B fix verification (17 claimed)

| # | Claim | Line | Verdict |
|---|---|---|---|
| 1.1 | 4-parameterization disclosure (eval 0.296 / cell 0.234 / ANCOVA 0.264 / Bayesian 0.252-0.319) | 425 | **LANDED, ch3 sync OK** (ch3:917 cell-level, ch3:919 ANCOVA, ch3:921 Bayesian 0.252/0.319 both reported, all reconcile). |
| 1.2 | Bonferroni 780 denominator collision footnote | 958 | **LANDED**; the inline bracket distinguishes full-set 45 vs novel-only 37, "same correction family rather than same hypothesis." |
| 1.3 | EqualWeight production (0.083) vs nested-LOPO (0.070) protocol split | 922 | **LANDED**, ch3:722-724 sync OK. |
| 2.1 | 280 vs 780 footnote (M-1) | 462 | **LANDED**; body says 280 family-level, footnote disambiguates 0.341 (per-pathogen mean of best at 780) vs 0.297 (oracle at 280). |
| 2.2 | Friedman power caveat n=11, W~0.15 | 474 | **LANDED**; explicit "corroboration of, rather than disconfirmation of." |
| 2.3 | SD 0.003 vs 0.034 reconciliation footnote | 497 | **LANDED**; sqrt(11) factor + 780-combo contraction explicit. |
| 2.4 | Bonferroni-survivor mean in keybox | 13 | **LANDED**; "H3N2 ~4.7x, HIV-1 ~4-5x." |
| 2.5 | HIV-1 nA=23 vs 26 Table 4.5 caption | 307 | **LANDED**; cross-refs `tab:gt_heterogeneity` + `sec:limitations`. |
| 3.1 | Within-cell residual SS partition source | 425 | **LANDED**; "Type II ANOVA fit reported in Table tab:stage2_anova" inline. |
| 3.2 | 41-SD random baseline CSV citation | 497 | **PARTIAL**: cited `random_baseline_means.csv` **does not exist** under `/proj/paper/results/mutbench/`. See B-Critical-1 below. |
| 3.3 | 5.92x z=13.34 definition + CSV | 254 | **PARTIAL**: definition complete; cited `structural_enrichment_summary.csv` **does not exist**. |
| 3.4 | ESM-2 rho per-pathogen N | 518 | **LANDED**; HCV 340 / MERS 1330 / Norovirus 540 / HIV-1 856 explicit. |
| 4.1 | MERS framing as failure case | 561 | **LANDED**; "perfect recall ... 200 of 1,330 ... ~22% of the protein, near-indiscriminate calling." |
| 4.2 | 9-distinct unique tuples honesty | 331 | **LANDED**; "at the parameter-variant level, only 10 of the 11 best-combinations are unique tuples." |
| 4.3 | Selective-reporting probe paragraph | 483 | **PARTIAL**: forward-references `lopo_per_pathogen.csv` and `omega_loo_pathogen.csv` — **neither file exists**. See B-Critical-1. |
| 5.1 | ch4:606 four-lens calibration | 597, 606 | **LANDED**; explicit "two failures-to-reject + one positive ANOVA + HIV-1 separate external positive line." |
| 6.1 | Bonferroni rounding policy unified | 958 | **LANDED**; "$\approx 2.5\times10^{-16}$ (rounded; un-rounded 2.47e-16 in CSV)" both shown. |

**Net**: 14 of 17 fully landed; 3 (3.2, 3.3, 4.3) cite CSV files that do not exist on disk.

---

## B. New adversarial findings (cycle 3 surface)

### Critical

**Cycle3-C1. Three CSV provenance citations point to non-existent files.** ch4:497 cites `results/mutbench/random_baseline_means.csv`; ch4:254 cites `results/mutbench/structural_enrichment_summary.csv`; ch4:483 cites `lopo_per_pathogen.csv` and `omega_loo_pathogen.csv`. None exist under `/proj/paper/results/mutbench/`. The directory does contain `cluster_bootstrap_omega.csv`, `bayesian_omega_summary.csv`, `vaccine_escape_stage3.csv`, `stage3_full_results.csv`, `feature_analysis/feature_ablation_nested_lopo.csv`, but the four newly cited files are phantom references. This is the exact `supplementary forward-reference 부재` failure mode the user warned about. Phase B traded "unverifiable claim" for "phantom CSV citation" — net provenance posture is not improved for these three claims.

**Cycle3-C2. ch4:474 vs ch4:603 Friedman framing inconsistency.** Line 474 (body) says non-significance is "corroboration of, rather than disconfirmation of, pathogen-dependent optimality" (i.e., null result reframed positively). Line 603 (Summary item 4) says "a second failure-to-reject under the rank-block test, with limited power at n=11 blocks." These are not contradictory but the body sentence still tilts toward "supports interpretation (2)" at line 475 ("LOPO performance gap of 0.265 ... support interpretation (2)") whereas the Summary at 606 explicitly forbids treating LOPO/Friedman as positive evidence ("only the ANOVA ... provides positive evidence"). A hostile reviewer flags ch4:475's "support interpretation (2)" as the same overclaim Phase B was meant to remove.

### Major

**Cycle3-M1. Headline-keybox Bonferroni number does not match Table 4.10 footnote rounding policy.** Keybox at ch4:13 quotes HIV-1 `p_adj = 2.5e-16` (rounded). ch4:958 footnote keeps both 2.5e-16 and 2.47e-16. ch4:1043 chapter summary uses 2.5e-16. Internal — yes, all three reconcile. But ch1:150 says "p_adj approx 3.9e-9 across 780 combinations" (novel-only) without ever quoting the full-overlap 2.5e-16. ch6:14 also uses only the nested-LOPO 4.012× headline. Cross-chapter, the *headline* abstract/ch1 anchor is the **novel-only 3.9e-9**, but the ch4 keybox elevates the full-overlap **2.5e-16**. These are different statistical objects (cycle 2 N-C2 collision). Phase B added a footnote inside Table 4.10 but did not propagate the disambiguation to ch4:13 keybox, where 2.5e-16 still appears as the headline number.

**Cycle3-M2. ch4:600 Summary block "two primary analyses" framing vs four-lens dissection at ch4:606.** Line 597: "two primary analyses---the scoring×pathogen ω² interaction, and a single-anchor vaccine-escape enrichment audit ... plus two null-consistent corroborations (LOPO 0/11 and Friedman). The four lenses re-parameterize the same dataset." Line 606: "only the ANOVA (within the modeled subspace) provides positive evidence; the LOPO permutation test and the Friedman rank test are two failures-to-reject ... The HIV-1 vaccine-escape audit provides a separate external positive line." So 597 says "two primary + two corroborations" (four), 606 splits into "one positive + two failures + one external" (still four but realigned). The mismatch: 597 frames vaccine-escape as part of the same "re-parameterization" of the same dataset; 606 says it is a "separate external positive line." A reviewer asks: is the vaccine-escape audit the same dataset or a separate external line? It is a *separate dataset* (45 HIV-1 escape positions, distinct from the 8,580 MCC grid), so 606 is correct and 597's "re-parameterize the same dataset" is technically inaccurate for the vaccine-escape branch.

**Cycle3-M3. ch4:606 says "two failures-to-reject" but ch4:474 power caveat undermines Friedman as a failure-to-reject.** If Friedman power is ~0.15 at n=11 (ch4:474), the result is "uninformative under low power" rather than "failure to reject." Calling it a failure-to-reject in 603/606 grants statistical authority that 474 explicitly disclaimed. Mild internal tension — recommend ch4:603 say "underpowered non-rejection" or "non-informative under n=11."

### Minor

**Cycle3-Mi-1. ch4:331 footnote says "two 'shared' assignments" but lists three pathogens (HCV, Influenza B, MERS).** "the two 'shared' assignments are HCV, Influenza B, and MERS all selecting freq" — grammatically broken. "two shared assignments" should be "three shared assignments" or "the shared assignment is freq, picked by HCV, Influenza B, and MERS." The 9-distinct count (8 distinct + 1 shared = 9) is internally consistent, but the prose miscounts the shared group.

**Cycle3-Mi-2. ch4:600 keybox calls vaccine-escape "single-anchor" but ch4:1043 calls HIV-1 "primary anchor" with H3N2 self-consistency separately listed.** Same audit, two adjective regimes ("single-anchor" vs "primary anchor"). Cosmetic.

**Cycle3-Mi-3. ch4:425 uses Bayesian range "0.252-0.319 (95% HDI [0.188, 0.396])" but ch3:921 reports two separate Bayesian fits — original 0.252 [0.188, 0.314] and re-implementation 0.319 [0.246, 0.396].** ch4 collapses into one range "0.252-0.319" with HDI "[0.188, 0.396]" (lower-of-original, upper-of-reimplementation). This synthetic union HDI is not the HDI of either fit individually. Reviewers may parse 0.252-0.319 as a single posterior range when it is actually two separate posterior means.

---

## C. Headline number internal consistency (ch4 only)

| Number | Locations | Verdict |
|---|---|---|
| ω² = 0.296 (eval-level) | 11, 338, 396, 421, 425, 600, 1042 | OK |
| ω² = 0.234 (cell-level) | 425 only | OK; not propagated to keybox or summary, but disclosure depth at 425 is adequate |
| 7.19× HIV-1 | 13, 945, 963, 1043 | OK |
| novel-only 7.16-8.24× HIV-1 | 958, 1043 (ch1:150) | OK |
| 9.36× H3N2 | 13, 944, 965, 993, 1043 | OK |
| novel-only 7.19× **H3N2** | 965, 1043 | **POTENTIAL CONFUSION**: H3N2 novel-only enrichment 7.19× shares the numerical value with HIV-1 full enrichment 7.19×; not a typo (both are 7.19×) but readers may conflate. ch4:13 carries HIV-1 7.19× headline; ch4:1043 carries both ("HIV-1 7.19×" and "novel-only enrichment 7.19×" for H3N2) in adjacent sentences. |
| p_adj = 2.5×10⁻¹⁶ | 13, 958, 1043 | OK; rounding consistent |
| p_adj = 3.9×10⁻⁹ | 958 (cycle 1 G09) | OK |
| Bonferroni-survivor 4.7× / 4-5× | 13, 958 | OK |
| 0.265 gap | 336, 449, 462, 480, 600, 1042 | OK |
| LOPO 0/11 | 12, 446 | OK |
| 4-feature 97.6% | 836 (descriptor only); 0.011/0.61 in 1033, 1043 | OK |

**Internal**: numerically consistent; the only soft confusion is the H3N2-novel 7.19× / HIV-1-full 7.19× collision (Mi-4 grade).

---

## D. Cross-chapter sync (ch3 / ch5 / ch6 / abstract)

| Item | ch4 | ch3 | ch5 | ch6 / abstract |
|---|---|---|---|---|
| Cell-level 0.234 | 425 | 917 (subsubsec:cell_level_omega) | 298 (sec:scoring_input_heterogeneity) | abstract not yet checked here |
| ANCOVA 0.264 | 425 | 919 | (forward) | — |
| Bayesian 0.252-0.319 | 425 | 921 | — | — |
| EqualWeight (a) production / (b) nested-LOPO | 922 | 722-724 | 192 (97.6% with caveat) | 14 |
| Bonferroni 780 + 3.9e-9 | 958 | — | — | ch1:150, ch6:14 (1.2 footnote not propagated) |

ch3 ↔ ch4 sync on cell-level / ANCOVA / Bayesian / EqualWeight protocols is **complete**. Bonferroni-collision footnote is **not** propagated to ch1 / ch6 (they cite 3.9e-9 without the "different statistical objects" disclaimer). Recommend cross-chapter Phase C for abstract / ch1 / ch6.

---

## E. Severity summary and recommendation

| Tier | Count | Items |
|---|---|---|
| Critical | 1 | C1 (3 phantom CSV citations) |
| Major | 3 | M1 (keybox 2.5e-16 vs ch1 3.9e-9 disambiguation not propagated), M2 (597 "same dataset" vs 606 "separate external" inconsistency), M3 (Friedman power caveat undercuts "failure-to-reject" label) |
| Minor | 4 | Mi-1 (two/three shared count typo at 331), Mi-2 (single vs primary anchor), Mi-3 (synthetic Bayesian HDI), 7.19× collision (H3N2 novel vs HIV-1 full) |

**Verdict**: Phase B applied 17 fixes; 14 fully landed and 3 (3.2, 3.3, 4.3) introduced phantom-CSV regressions. The cell-level/Bonferroni-collision/EqualWeight P0 trio (1.1, 1.2, 1.3) — the three highest-priority cycle 2 demands — all landed cleanly with ch3 sync verified. Cycle 3 P0 priority: create the four missing CSVs OR replace those provenance citations with files that do exist (`stage3_full_results.csv`, `cluster_bootstrap_omega.csv`, `bayesian_omega_summary.csv`).

End of cycle 3 ch4 re-attack.
