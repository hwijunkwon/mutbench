# Final Audit Stage 1: ch2_background

## A. Numerical consistency

Scope file audited: `paper/dissertation/chapters_en/ch2_background.tex` (229 lines). MutBench numerical claims in ch2 were checked against the requested CSV sources.

- PASS: `8{,}580` headline grid at line 108 is consistent with `stage3_full_results.csv`: 8,580 data rows = 11 pathogens x 20 scoring channels x 39 detector variants.
- PASS: line 108 says ESM-3 is excluded from the headline grid; ESM-3 is not present among the 20 `scoring` values in `stage3_full_results.csv`.
- PASS: line 138 says 20 scoring channels, 10 biological information families, 11 pathogens; the 20 scoring channels and 11 pathogens are confirmed in `stage3_full_results.csv`. The 10-family claim is methodological and consistent with the chapter's wording that 20 channels are expanded from 10 families.
- PASS: line 158 says 14 detection families; `stage3_full_results.csv` has 14 distinct `family` values and 39 detector variants.
- PASS: line 184 says scoring x pathogen interaction `omega^2 = 0.296`; `stage3_statistics.csv` gives `scoring×pathogen = 0.29625198394914415`.
- PASS: line 186 says 11-pathogen cluster-bootstrap interval `[0.201, 0.346]`; `cluster_bootstrap_omega_summary.csv` gives `ci_lo=0.2008358030`, `ci_hi=0.3455024399`, rounding to `[0.201, 0.346]`.
- PASS: line 186 says within-cell residual `omega^2 approx 0.39`; from `stage3_statistics.csv`, residual SS 37.2076 over total modeled-plus-residual SS 97.5133 gives 0.382, which supports the approximate 0.39 statement.
- PASS: line 187 says HIV-1 `7.19x`, Bonferroni-corrected `p = 2.5e-16`, 82% Layer-A-disjoint. `vaccine_escape_stage3.csv` has HIV-1 `freq + Wavelet(t=1.5)`, enrichment `7.1875`, raw `p=3.1602957833854608e-19`; multiplied by 780 gives `2.46e-16`. The 82% disjoint value is supported by the Chapter 4 audit table footnote (37/45 novel), not directly by the CSV columns.
- PASS: line 187 says H3N2 `9.36x`; `vaccine_escape_stage3.csv` has H3N2 `fubar_bf + Wavelet(t=2.0)`, enrichment `9.3621`.
- PASS: line 178 says MutBench LOPO 0/11 is null-consistent under permutation; `stage3_statistics.csv` gives LOPO match rate `0.0` over 11 folds and Friedman `p=0.9895444533`, consistent with null-non-rejection.
- PASS: line 166 ProteinGym v1.3 `217 DMS assays` and `90+ baseline models`, line 167 ViroGym `13 viruses`, `79 DMS assays`, `552,937 sequences`, and line 178 EVEREST v3 `45 viral DMS datasets`, `31 forecasting clades`, `4 viruses`, `40 WHO priority RNA viruses`, `16 families` are cited to local BibTeX keys. These are literature-scope numbers and are not represented in the requested MutBench CSVs.
- NOT ASSERTED IN CH2: auxiliary audit values from `feature_ablation_nested_lopo_summary.csv`, `p1_null_per_pathogen.csv`, `p2_decision_curve.csv`, `p3_full_lattice_1023.csv`, `p5_callable_decisions.csv`, `p6_null_summary.csv`, `w4_labeled_lopo_summary.csv`, `codex_layerA_prime/lopo_summary.csv`, `adaptive_weighting_comparison.csv`, and `hbfws_lopo_results.csv` are not claimed in ch2. No ch2 inconsistency found against them.

## B. Citation integrity

PASS: all citations resolve. Parsed 91 `\cite...{}` key uses, 72 unique keys. Every key exists in `paper/dissertation/references.bib`.

Missing cite keys: none.

## C. Cross-reference integrity

PASS: all references resolve. Parsed 36 `\ref`/`Chapter~\ref`/`Section~\ref` targets, 15 unique labels. Every target label exists in the active build set (`front_en`, `ch1`--`ch5`).

Wrong-target scan: no evidence of wrong target for ch2 refs. Examples checked: `sec:information_analysis` -> ch4 results, `sec:scoring_detection` -> ch3 methods, `tab:vaccine_escape_stage3` -> ch4 results, `tab:gt_positions` -> ch3 methods, `sec:future_work` -> ch5 discussion, and local `tab:benchmark_comparison` -> ch2.

Orphan refs/equation/table/figure refs in ch2: none found.

## D. Triage framing consistency

PASS: no unqualified claim that MutBench/Algorithm 1 is deployable, deployed, a calibrated detector, or a prospective detector appears in ch2.

Keyword scan:

- `deployable` / `deployment` / `prospective detector`: no ch2 hits.
- `operational`: two hits, both generic background usage about surveillance platforms providing operational context, not MutBench deployment.
- `phase transition`, `20-30`, `20--30`: no ch2 hits.
- `Algorithm 1`: no ch2 hits.
- `LOPO 0/11`: one conceptual hit at line 178, explicitly qualified as "null-consistent under permutation" and not used as standalone proof.

Framing inconsistencies: 0.

## E. Layer C / HIV-1 anchor

Layer C: ch2 correctly distinguishes antibody-escape DMS from fitness-DMS Layer C and names the six Layer C pathogens/datasets at line 84. However, ch2 does not state the current practical-anchor numerics: 6 pathogens, 650 Layer C positions, per-pathogen counts (SARS-CoV-2 247, H3N2 112, HIV-1 48, RSV 101, Rabies 87, EV-A71 55), or best Layer C MCC range 0.139--0.322. These values are supported by `layer_c_evaluation.csv` and appear in ch5, but not in ch2.

HIV-1: ch2 states the load-bearing HIV-1 escape anchor as `7.19x`, Bonferroni `p = 2.5e-16`, and 82% Layer-A-disjoint. These match `vaccine_escape_stage3.csv` plus the ch4 circularity audit. ch2 does not explicitly include "37 of 45 novel"; it only gives the equivalent 82% disjoint value.

## F. Compression regression check

- Bolker rule-of-thumb: DEVIATION. ch2 does not cite or mention the Bolker 20--30 stable-random-effects rule as a design target. This may be intentional because the point is covered in ch4/ch5, but the mandatory ch2 compression check fails literally.
- "Not learnable" paired with "at n=11": PASS by absence. ch2 does not make a "not learnable" claim; no unpaired overstatement found.
- "20--30+ pathogens will suffice" / phase transition: PASS. No such claim in ch2.
- LOPO 0/11 standalone: PASS. The only ch2 LOPO statement is paired with null consistency.
- Algorithm 1 calibrated detector: PASS. No Algorithm 1 claim in ch2.
- Orphaned equation/table/figure refs: PASS. No orphaned refs found.

## Issue list

- Critical: none.
- Major: ch2 fails the mandatory Bolker retention check literally; no Bolker 20--30 rule-of-thumb citation or design-target framing is present in the chapter.
- Minor: ch2 does not carry the full Layer C practical-anchor numerics (six pathogen counts and 0.139--0.322 MCC range) and does not spell out HIV-1 "37 of 45 novel," although the equivalent 82% disjoint statement is present and correct.

RESULT_FINAL_AUDIT_STAGE1_ch2: critical=0 major=1 minor=1 framing_inconsistencies=0 orphan_refs=0
