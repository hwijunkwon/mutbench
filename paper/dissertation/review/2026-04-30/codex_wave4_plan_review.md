# Codex Wave 4 Plan Review

## Verdict

**PROCEED WITH MODIFICATIONS.** Option E is the right primary design after the PI/student decision: true performance evaluation stays on the 12 labeled folds, while the expanded 28-target union is diagnostic only. The plan needs targeted fixes before Task 2, mainly to predeclare the h-score harmonization gate, pin bootstrap/quorum degrees of freedom, and narrow the Q7 claim from "artifact answered" to "future quorum feasibility assessed."

## Q1. Design choice

Keep Option E as primary. The labeled-evaluation versus unlabeled-diagnostic boundary is mostly drawn correctly: MCC, TP@budget, enrichment against Layer A, and callability endpoint performance are limited to the original 12 labeled feature matrices, while the 16 new targets contribute only feature-spread, rank-stability, sign-stability, and reachability diagnostics. I would not move any unlabeled component into the labeled track. The one component that needs tightening is "quorum reachability": it should remain an expanded-panel feasibility diagnostic, not a callability analogue. Also, the historical 4-core comparator belongs only in the 12-fold labeled evaluation and should not be used as a target for expanded-panel success.

## Q2. Degrees of freedom

The plan is directionally predeclared, but several operational fields remain loose enough to invite post hoc selection. Pin the exact seed, resampling unit, envelope rule, target quality gates, tie handling, and branch thresholds before implementation. In particular, the report should not be able to choose between Jaccard, Spearman, rank correlation, top-k overlap, or feature-spread criteria after seeing which looks favorable.

Fields to pin:

- `random_seed=42` for all bootstraps, perturbations, and tie-breaking.
- `n_bootstrap=1000`; bootstrap unit is labeled pathogen, sampled with replacement from the 12 labeled matrices.
- Sign aggregation rule under a bootstrap: per-feature sign is the sign of the training-label Pearson correlation after within-pathogen z-scoring; ties or zero/NA correlations map to a predeclared neutral/exclusion rule.
- Top-k definition: primary `top_fraction=0.10`; fixed candidate budgets `{20,50,80}` for labeled endpoints only; tie handling at the cutoff.
- Jaccard computation: pairwise over bootstrap top-10% callsets per target, with exact aggregation as median and 10th percentile over all bootstrap pairs or a predeclared sampled pair set.
- Rank stability: specify Spearman over all rankable positions; constant-score targets report `no_result_constant_rank`, not an imputed correlation.
- Labeled envelope rule: define the eight meta-features and whether "inside" means within labeled min-max, 5th-95th percentile, or median +/- IQR.
- Feature-quality gates: exact `n_positions`, missingness, constant/all-zero frequency/entropy/hscore, and usable-target denominator rules.
- Quorum proxy thresholds: `n_usable_targets >= 20`, `>=7` stable targets, `>=7` envelope-inside targets, and whether those must be the same seven targets.
- Schema-drift gate for `hscore`: exact Spearman/Jaccard thresholds and the action if the gate fails.

## Q3. Algorithm 1 contract

The labeled 12-fold shared-feature LOPO can preserve Algorithm 1 if implemented exactly as line 75 says: for each held-out labeled pathogen, fit directional signs using only the other 11 labeled pathogens, then score and evaluate the held-out fold. There is no necessary leakage in the design. The main leakage risk is implementation ambiguity: overlap CSVs for Dengue/HIV-1/Norovirus must never substitute for the labeled matrices inside the 12-fold evaluation, and any hscore drift observed in overlap files must not be used to tune labeled-fold signs or thresholds. The 3-core scope reduction is acceptable as a Wave 4 shared-feature experiment, but it must be described as a harmonized-feature reduction, not as the same biological 4-core claim from Wave 1-3. Direct comparison to the historical 4-core is useful only as a labeled-panel sensitivity comparator; failure of the 3-core cannot be rescued by expanded unlabeled stability.

## Q4. No-label boundary

The non-claims list is strong, but it still has wording loopholes. "Transfer," "quorum reachability," "7/11-like quorum," and "callability diagnostics" could be misread as unlabeled validation unless the plan explicitly says no expanded target is callable, successful, true-positive-enriched, or Layer-A validated in Wave 4. The plan should replace any "deployment," "validation," or "small-panel artifact" phrasing in the expanded component with "feature-space feasibility," "diagnostic," or "hypothesis-generating." Also add a guard that `ground_truth=0` in the three overlap cross_pathogen CSVs is ignored just like `ground_truth=-1`; those overlap files are schema-audit inputs, not additional labels.

## Q5. Q7 answerability

The structural quorum-reachability proxy does not fully answer whether 12-pathogen heterogeneity is a small-panel artifact, because it has no Layer A on the 16 new targets. It can answer a narrower and still useful question: whether the expanded features-only panel contains enough non-duplicated, non-degenerate, feature-diverse targets that a future curated-panel callability test would be structurally possible. The dissertation-safe conclusion is "Wave 4 assesses feasibility of escaping the 12-panel quorum bottleneck," not "Wave 4 shows the 12-panel failure was a small-panel artifact."

## Q6. Feature harmonization

`hscore=freq*entropy` on labeled matrices is a reasonable provisional harmonization only if the overlap audit shows that the labeled-derived and cross_pathogen hscore rankings agree. The sampled cross_pathogen rows do not look numerically equal to `frequency * entropy`, so raw formula equivalence should not be assumed. Use the overlap drift gate to decide whether hscore enters expanded-panel diagnostics. I recommend the plan declare hscore non-harmonizable if the median across Dengue/HIV-1/Norovirus is Spearman rho < 0.70 or top-10% Jaccard < 0.50, or if at least two of the three overlaps fail either threshold. If non-harmonizable, keep labeled 3-core LOPO as planned but report expanded diagnostics as a 2-core `freq, entropy` sensitivity plus a failed hscore audit.

## Q7. Denominator handling

The 28 unique target denominator is correct given the files listed: 12 labeled feature matrices plus 19 cross_pathogen CSVs minus 3 overlaps equals 28 unique targets, with 16 newly added unlabeled targets. The reporting schema should include all of `n_unique_targets=28`, `n_labeled_eval=12`, `n_cross_pathogen_csv=19`, `n_overlap=3`, and `n_unlabeled_expanded=16` or `n_new_unlabeled=16`; pick one name and use it consistently. Double-counting is mostly protected by lines 80-81 and 164-165, but add a machine-checkable invariant: unique-target tables must have 28 rows, overlap-audit tables must have 3 rows, and any expanded diagnostic that includes `source_type=cross_pathogen_overlap` must mark those rows as `audit_only` and exclude them from unique-target counts.

## Q8. Failure branches

The branches are useful and mostly strong enough. Branch 3 is the key defense guardrail: if labeled 3-core performance is weak but expanded stability is high, the conclusion must be negative for Algorithm 1 prediction, not "stable transfer." I would strengthen Branch 1 and Branch 3 to require labeled evidence before any small-panel-artifact prose. Branch 1 should say "plausibly motivates curated expansion" rather than "plausibly a small-panel/quorum artifact." Branch 5 should be promoted from a reporting caution to an execution gate for expanded hscore analyses: if overlap drift is large, hscore-based expanded diagnostics become uninterpretable and the branch must either rerun with 2-core features or stop at input-audit results.

## Concrete Edits

- `/proj/paper/docs/plans/2026-04-30-wave4-tier2-features-lopo.md:8`: Replace "testing the codex Q7 question: whether the 12-pathogen heterogeneity and Wave 2's 0/12 callable outcome are artifacts of too small a reference panel" with "testing the bounded codex Q7 feasibility question: whether the expanded features-only panel makes a future curated quorum structurally reachable, without showing that the 12-pathogen outcome was an artifact."
- `/proj/paper/docs/plans/2026-04-30-wave4-tier2-features-lopo.md:35`: Add `n_cross_pathogen_csv=19` and `n_overlap=3` to the required denominator string, and use one consistent name for the 16 new targets: `n_unlabeled_expanded=16`.
- `/proj/paper/docs/plans/2026-04-30-wave4-tier2-features-lopo.md:36`: Replace "define `hscore = freq * entropy` unless..." with "derive labeled `hscore = freq * entropy` provisionally; include hscore in expanded diagnostics only if the overlap schema-drift gate passes."
- `/proj/paper/docs/plans/2026-04-30-wave4-tier2-features-lopo.md:52`: Replace "whether the 12-panel heterogeneity remain even in the expanded feature space" with "whether the expanded feature space is large and stable enough to justify later Layer A curation for a real quorum test."
- `/proj/paper/docs/plans/2026-04-30-wave4-tier2-features-lopo.md:60`: Append "If the overlap drift gate fails, expanded-panel diagnostics fall back to the 2-core `freq, entropy`; labeled 3-core LOPO remains a labeled-panel sensitivity only."
- `/proj/paper/docs/plans/2026-04-30-wave4-tier2-features-lopo.md:75`: After "fit per-feature directional signs" add the exact estimator: "within-pathogen z-score each feature on training pathogens, compute Pearson correlation with `layer_a` within each training pathogen, aggregate signs by median correlation across the 11 training pathogens; zero/NA correlations are recorded as neutral and excluded from the sign vote unless all are zero/NA, in which case the feature is dropped for that fold."
- `/proj/paper/docs/plans/2026-04-30-wave4-tier2-features-lopo.md:76`: Replace "callability diagnostics D1-D4 where applicable" with "training-fold callability diagnostics D1-D3 and held-out annotation-density D4 on labeled folds only; no expanded target receives a callability endpoint."
- `/proj/paper/docs/plans/2026-04-30-wave4-tier2-features-lopo.md:81`: Change `n_new_unlabeled=16` to `n_unlabeled_expanded=16` or add an alias line saying the two names are identical; do not alternate names across outputs.
- `/proj/paper/docs/plans/2026-04-30-wave4-tier2-features-lopo.md:83`: Append "For overlap CSVs, `ground_truth=0` is also ignored; overlap files are audit-only and never treated as negatives."
- `/proj/paper/docs/plans/2026-04-30-wave4-tier2-features-lopo.md:87`: Add "Use `random_seed=42`; compute Jaccard over top-10% callsets with deterministic tie-breaking by position; report constant-score targets as `no_result_constant_rank` for Spearman."
- `/proj/paper/docs/plans/2026-04-30-wave4-tier2-features-lopo.md:88`: Replace the current quorum sentence with "Quorum reachability proxy: a feature-space feasibility diagnostic only; pass requires `n_usable_targets >= 20`, at least 7 targets with median top-10% Jaccard >=0.60 and 10th percentile >=0.40, and at least 7 targets inside the labeled envelope on >=5/8 predeclared meta-features. This does not make any target callable."
- `/proj/paper/docs/plans/2026-04-30-wave4-tier2-features-lopo.md:89`: Append "Declare hscore non-harmonizable if median overlap Spearman rho <0.70, median top-10% Jaccard <0.50, or at least two of three overlaps fail either threshold."
- `/proj/paper/docs/plans/2026-04-30-wave4-tier2-features-lopo.md:91-98`: Add a non-claim bullet: "Do not describe expanded stability, overlap concordance, or quorum reachability as validation, held-out performance, callability success, or evidence that the 12-pathogen failure was an artifact."
- `/proj/paper/docs/plans/2026-04-30-wave4-tier2-features-lopo.md:107`: Replace "the 12-panel callability failure is plausibly a small-panel/quorum artifact" with "the features-only expansion plausibly motivates Layer A curation to test the small-panel/quorum-artifact hypothesis."
- `/proj/paper/docs/plans/2026-04-30-wave4-tier2-features-lopo.md:109`: Append "Expanded stability alone cannot soften a weak labeled 3-core result; dissertation prose must state that stability is engineering reproducibility, not Layer A predictiveness."
- `/proj/paper/docs/plans/2026-04-30-wave4-tier2-features-lopo.md:111`: Replace "stop before dissertation prose insertion and audit preprocessing differences" with "exclude hscore from expanded diagnostics and rerun/report a 2-core `freq, entropy` sensitivity, or stop at the input-audit stage if the 2-core rerun is not performed."
- `/proj/paper/docs/plans/2026-04-30-wave4-tier2-features-lopo.md:132`: Add `audit_only` and `unique_target_inclusion` columns to `w4_input_inventory.csv`, with an invariant that unique-target rows sum to 28 and overlap-audit rows sum to 3.
- `/proj/paper/docs/plans/2026-04-30-wave4-tier2-features-lopo.md:166`: Replace "Run 1,000 labeled-pathogen bootstrap sign fits" with "Run 1,000 bootstrap sign fits with `random_seed=42`, resampling labeled pathogens with replacement; unlabeled targets are never sampled into sign fitting."
- `/proj/paper/docs/plans/2026-04-30-wave4-tier2-features-lopo.md:169`: Clarify whether the 7 stable targets and 7 envelope-inside targets must be the same targets. I recommend requiring the same >=7 targets to pass both stability and envelope criteria for a stronger feasibility claim.

## Wave 5 Ordering Recommendation

After Wave 4, the next step should be conditional. If labeled 3-core performance is not clearly positive, Wave 5 should not be pilot Layer A expansion; it should be feature augmentation or a manuscript-negative-results cleanup. If labeled 3-core is acceptable and the expanded panel passes feature-quality plus hscore/2-core stability gates, proceed to the planned pilot Layer A curation for YFV/Lassa/WNV, selected from targets that pass the Wave 4 quality and diversity filters. Only after that should defense rehearsal or EVE/PLM site-effect work be prioritized.

## Defense-Readiness Risk Re-Scoring

**Medium-High.** Option E prevents the biggest overclaiming failure, but risk remains above medium until the plan narrows the Q7 claim and handles hscore schema drift. Without those edits, a committee could reasonably object that the expanded-panel result is an unlabeled stability diagnostic being presented as evidence about Layer A performance.
