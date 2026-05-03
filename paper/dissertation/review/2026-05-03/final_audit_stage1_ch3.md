# Final Audit Stage 1: ch3_methods

Scope audited: `paper/dissertation/chapters_en/ch3_methods.tex` on checked-out `master` commit `746549a`. Prompt provenance says `master` v227, but the local checkout does not expose that identifier; this audit uses the current workspace state.

## A. Numerical consistency

Verified against the requested archives:

- Stage-2 grid: Chapter 3 states 20 scoring types x 39 detector variants x 11 pathogens = 8,580 evaluations; `stage3_full_results.csv` has 8,580 rows, 11 pathogens, 20 scoring types, 39 detector strings, and 14 families.
- ANOVA: Chapter 3 reports residual df 7,970 and headline scoring x pathogen omega^2 = 0.296; `stage3_statistics.csv` gives `scoring×pathogen = 0.29625198394914415`, residual df 7,970, family omega^2 = 0.012622864, scoring omega^2 = 0.063008596, pathogen omega^2 = 0.117328792.
- Friedman/LOPO design: Chapter 3 describes 11 blocks, top k=20 combinations, and 280-cell random concordance 1/280 = 0.36%; `stage3_statistics.csv` gives Friedman chi^2 = 7.6879666, df = 19, and LOPO match_rate = 0.0. No standalone “LOPO 0/11 proves not learnable” claim appears in Chapter 3.
- Bootstrap omega: Chapter 3 reports standard cluster CI [0.201, 0.346]; `cluster_bootstrap_omega_summary.csv` gives [0.2008358, 0.3455024]. Rounded match.
- 5-frame robustness: Chapter 3 reports wild-cluster [0.201, 0.303], phylogenetic block [0.202, 0.346], mixed pseudo-omega 0.340, Bayesian mean 0.316 HDI [0.242, 0.388], P(>0.14)=0.9998; `omega_robustness_5way.csv` matches rounded values.
- Vaccine-escape methods: Chapter 3 reports 3/11 pathogens and 2,340 enrichment evaluations; `vaccine_escape_stage3.csv` has 2,340 rows over H3N2, HIV-1, SARS-CoV-2. The headline enrichment values are not asserted in Chapter 3.
- Fixed top-5 protocol: Chapter 3 does not quote the top-5 enrichment values; `escape_validation_adapt.csv` contains the expected top5 rows.
- Layer C: Chapter 3 gives six DMS pathogens and counts SARS-CoV-2 247, H3N2 112, HIV-1 48, RSV 101, Rabies 87, EV-A71 55; `layer_c_evaluation.csv` matches exactly. Per-pathogen best Layer-C MCC range from archive is 0.138527-0.322436, consistent with the dissertation-level 0.139-0.322 anchor.
- Nested LOPO 4-core: Chapter 3 says 4-feature core vs full-10 uses the nested-LOPO protocol; `feature_ablation_nested_lopo_summary.csv` gives fixed-4 = 0.08088185 and full-10 = 0.06975433. No mismatch.
- Wave/Cycle archives: Chapter 3 only defines methods, but requested values verified: P1 iid 4-core significance is 5/12 and “at/below null mean” framing in active Chapter 4 accounts for 6/12; P2 random budget-50 total = 41; P3 4-core rank = 87/1023; P5 callable = 0/24 method-fold rows across 12 pathogens; P6 has 4 null types; Wave 4 8/12 positive, Wilcoxon p = 0.367658; W5 mean MCC = -0.0554876; HBFWS one-sided greater p = 0.7793659.

Deviation: line 34 says “HCV-only ANOVA sensitivity analysis (omega^2 = 0.246)”. In `cluster_bootstrap_omega_summary.csv`, the current HCV-excluded evaluation-level value is 0.2534097 and the file’s `body_target` is 0.246. This looks like a stale rounded manuscript target or ambiguous wording (“HCV-only” vs “HCV-excluded”). Minor numerical issue.

## B. Citation integrity

Parsed all `\cite...{}` instances in Chapter 3. Result: 84 citation instances, 59 unique keys, 0 missing from `paper/dissertation/references.bib`.

No unresolved citation keys found.

## C. Cross-reference integrity

Parsed all `\ref`, `\eqref`, `\autoref`, and `\pageref` keys in Chapter 3 and compared against labels in active `front_en` and `chapters_en` files. Result: 127 ref instances, 65 unique keys, 0 missing labels, 0 duplicate labels in the active label set.

Spot-checked target semantics for high-risk refs: `tab:pathogen_data`, `tab:gt_positions`, `subsec:9pathogen_statistics`, `tab:omega_robustness_5way`, `tab:nested_lopo_4core`, `sec:future_work`, `sec:esm2_leakage`, `sec:cross_validation_escape`, and `alg:mutbench_coldstart` resolve to the intended active chapters/tables/algorithm. No orphaned equation, table, or figure refs found.

## D. Triage framing consistency

Keyword audit in Chapter 3:

- `deployable`: none.
- `deployment`: none.
- `prospective detector`: none.
- `calibrated detector`: none.
- `phase transition`, `20--30`, `20-30`, `not learnable`, `Algorithm 1`: none.
- `operational`: three uses. Lines 216 and 282 refer to metric/ground-truth operationalization, not deployment. Line 627 distinguishes EqualWeight code paths. These are scoped and not inconsistent with wet-lab triage framing.
- `deployability`: line 485 says “a question raised in connection with benchmark deployability” but immediately limits the analysis to a single-pathogen H3N2 time-stratified frequency-only pilot, notes the retrospective Layer-A reference, and reserves full prospective work for future study. No overclaim.

No unqualified deployment/prospective-detector claim found in Chapter 3. No LOPO 0/11 standalone proof claim found.

## E. Layer C / HIV-1 anchor

Layer C is correctly represented in Chapter 3: six pathogens are listed with counts SARS-CoV-2 247, H3N2 112, HIV-1 48, RSV 101, Rabies 87, EV-A71 55, matching `layer_c_evaluation.csv`. The best-MCC range 0.139-0.322 is not directly quoted in Chapter 3 but is supported by the archive.

HIV-1 vaccine escape headline values (7.19x, p_adj = 2.5e-16, 82% Layer-A-disjoint, 37/45 novel) are not quoted in Chapter 3; Chapter 3 only defines the vaccine-escape cross-validation method and the 3/11 pathogen availability. No inconsistency in scope.

## F. Compression regression check

- Bolker rule-of-thumb is not cited in Chapter 3. It remains present in active front matter/Chapter 1/Chapter 5 as a design target and stable-random-effects rule-of-thumb, not a phase transition.
- “Not learnable” does not appear in Chapter 3. Active front matter pairs it with “at n=11, under the tested regime”; Chapter 3 does not introduce an unqualified version.
- No equation, table, or figure reference was orphaned after compression.
- Load-bearing ANOVA 5-frame narrative remains in Chapter 3 and includes Cameron 2008 wild-cluster justification.
- Compression did not remove the Layer C availability/count table or the EqualWeight variant distinction.

## Issue list

- Critical: none.
- Major: none.
- Minor: Chapter 3 line 34 has a stale/ambiguous HCV sensitivity number: manuscript says omega^2 = 0.246, while the current audit archive gives HCV-excluded evaluation-level omega^2 = 0.2534097 and only preserves 0.246 as `body_target`.
- Minor: Local checkout provenance is `master` commit `746549a`, not an explicit v227 identifier; audit could not confirm the prompt’s v227 state from git metadata.

RESULT_FINAL_AUDIT_STAGE1_ch3: critical=0 major=0 minor=2 framing_inconsistencies=0 orphan_refs=0
