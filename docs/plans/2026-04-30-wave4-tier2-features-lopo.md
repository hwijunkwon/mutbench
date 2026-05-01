# Wave 4 Tier 2 — Features-Only LOPO at n≈30 Plan

> **Version:** v1 draft, 2026-04-30  
> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement task-by-task.

**Goal:** Pre-register the Wave 4 Tier 2 features-only expanded-panel experiment promised in Chapter 5, while resolving the central design ambiguity: the 19 `cross_pathogen` targets have frequency/entropy/h-score features but no Layer A labels. The primary experiment must therefore separate (i) true held-out Layer A evaluation, which can only occur on the existing 12 labeled `feature_matrix_*.csv` pathogens, from (ii) expanded-panel stability and quorum diagnostics over the approximately 30-target features-only panel.

**Architecture:** Use a hybrid design (Option E below). Actual nested-LOPO MCC, TP@budget, and callability endpoints remain restricted to folds with Layer A. The expanded panel is used for ranking-stability, sign-stability, feature-spread, and quorum-reachability diagnostics only. This preserves the Algorithm 1 contract while testing the bounded codex Q7 feasibility question: whether the expanded features-only panel makes a future curated quorum structurally reachable, without showing that the 12-pathogen outcome was an artifact.

**Tech Stack:** Python 3, NumPy, pandas, scipy, sklearn, matplotlib. No GPU. Compute budget: <1 CPU-hour. No new data acquisition. No Layer A curation in this wave.

**Documentation cadence:** Per task: NOTES.md bullet + standalone Markdown report under `paper/dissertation/review/2026-04-30/wave4/`. Memory written ONLY at Wave 4 closure.

**Spec source:** Wave 3 codex review §Q7 ordering, `codex_wave3_results.md` memory, Chapter 5 future-work paragraph on Tier 2 features-only sweep, and Chapter 3 nested-LOPO Algorithm 1 description.

**Critical constraint:** The 19 `data/cross_pathogen/*_position_scores.csv` files have `ground_truth=-1` and no Layer A. They must not be treated as held-out positive/negative labels. Any metric requiring true labels (MCC, F1, precision against Layer A, TP@budget, callability endpoint performance) is computed only on the original 12 labeled feature matrices.

**Out of scope (Wave 5+ plans):** Literature Layer A curation for YFV/Lassa/WNV or any other target; EVE/PLM external site-effect via `tools/eve_container/`; defense rehearsal; any claim that the 16 newly added unlabeled targets validate Algorithm 1 against Layer A.

---

## Motivation

Wave 1 showed that Algorithm 1 has descriptive signal on a subset of the 12-pathogen panel (5/12 iid-significant, but only Norovirus under the strictest P1 local-burden null), while P2/P3 bounded rank reliability and feature-set optimality. Wave 2 then applied the pre-registered callability rule and found 0/12 callable under the default 7/11 quorum, largely because the current panel has too few training pathogens with stable top-decile separation. Wave 3 P6 strengthened the descriptive subset by showing that H3N2, Norovirus, Dengue, and Influenza B survive structurally explicit SASA/pLDDT/joint nulls, with Norovirus also surviving P1 local-burden. Codex Wave 3 review §Q7 therefore ordered Wave 4 first as "Tier 2 features-only LOPO at n≈30" before pilot Layer A curation or EVE/PLM. The unresolved issue is that Layer A is missing on the expanded targets; this plan makes that limitation explicit and pre-registers a hybrid experiment that assesses future quorum feasibility without overclaiming held-out validation where no labels exist.

---

## Design Options Analysis

### Shared facts and denominators

- Existing labeled panel: 12 `results/mutbench/feature_analysis/feature_matrix_{...}.csv` files with `layer_a` and 10 features.
- Expanded features-only panel: 19 `data/cross_pathogen/*_position_scores.csv` files with `position,frequency,entropy,hscore,ground_truth`.
- Overlaps with labeled panel: `dengue_e ↔ Dengue`, `hiv1_gp120 ↔ HIV-1`, `norovirus_vp1 ↔ Norovirus`.
- Unique union: 12 labeled pathogens + 16 newly added unlabeled targets = 28 unique experimental targets. The plan uses `n≈30` as the dissertation shorthand but every output must report the exact denominator as `n_unique_targets=28`, `n_labeled_eval=12`, `n_cross_pathogen_csv=19`, `n_overlap=3`, and `n_unlabeled_expanded=16`.
- Shared features: the only universally available position-level channels are frequency, entropy, and a frequency-by-entropy h-score proxy. For labeled feature matrices, derive labeled `hscore = freq * entropy` provisionally; include hscore in expanded diagnostics only if the overlap schema-drift gate passes.

### Option table

| Option | Experimental definition | Researcher degrees-of-freedom control | Does it answer codex Q7? | Cost | Overclaim risk | Algorithm 1 contract match | Verdict |
|---|---|---|---|---|---|---|---|
| **A. Training-fold-only stability** | Skip held-out evaluation on all unlabeled targets. Fit signs on labeled 12 only; report sign stability, top-decile spread, rank dispersion, and whether expanded meta-features make a future curated quorum structurally reachable. | Strong if thresholds and summaries are predeclared; no synthetic labels. | Partial. It tests panel diversity and stability but not held-out Layer A performance. | Low. | Low, because no validation claim is made. | Medium. Uses Algorithm 1 sign-fitting but omits held-out evaluation. | Useful baseline, insufficient as primary because "LOPO" becomes mostly absent. |
| **B. Surrogate Layer A from features** | Create weak positives on 19 targets from top-decile h-score, then run pseudo-LOPO against those labels. | Weak. The labels are derived from the same features being evaluated; many arbitrary choices (top 5/10/20%, h-score formula, tie handling). | Poor. It mostly tests whether a score recovers itself, not whether small-panel heterogeneity is real. | Low-medium. | High. It could be mistaken for validation despite circular labels. | Poor. Algorithm 1 is defined against externally curated Layer A, not feature-derived positives. | Reject except as an explicitly labeled negative-control/circularity demonstration. |
| **C. Train on 12 Layer A, evaluate cross_pathogen by unsupervised ranking concordance** | Fit signs/feature orientations using the 12 labeled panel; score 19 cross-pathogen targets; compare top-k rankings with feature-only h-score or training-fold sign predictions. | Medium if concordance endpoint is fixed; still has design freedom in the concordance target. | Partial. It tests transfer of rankings to diverse feature distributions, but no Layer A outcome. | Low. | Medium. "Concordance" can sound like validation even when it is unsupervised. | Medium-low. The training side matches Algorithm 1; evaluation lacks Layer A. | Use as a secondary diagnostic inside the hybrid track, not as the headline. |
| **D. Labeled-panel subsampling simulation** | Use the 12 labeled pathogens only. Repeatedly subsample training panels of size 6-11, run nested LOPO/callability diagnostics, and extrapolate how quorum behavior changes with panel size. | Strong if subsampling grid and seeds are fixed. No synthetic labels. | Moderate. It directly tests small-panel sensitivity, but cannot actually reach 20-30 labeled pathogens. | Medium. | Low-medium. Extrapolation beyond 12 must be described carefully. | Strong for labeled folds. | Valuable secondary simulation, but it does not use the 19 features-only targets promised in Chapter 5. |
| **E. Hybrid labeled evaluation + expanded ranking-stability transfer** | Primary actual MCC/TP/callability stays on 12 labeled folds using the shared 3-feature subset. Expanded 28-target panel is used for training-set/meta-feature stability, top-k ranking stability, and quorum-reachability diagnostics; no unlabeled target contributes to MCC. | Strongest. It predeclares which endpoints are labeled vs unlabeled and forbids synthetic positives. | Best available. It tests whether the expanded features-only panel could support a future curated-panel quorum test while preserving true evaluation only where labels exist. | Medium. | Low if prose keeps "stability/quorum diagnostic" separate from "Layer A validation." | Strongest compatible match. Nested-LOPO remains label-aware on the 12; unlabeled transfer is explicitly outside evaluation. | **Recommended primary track.** |

### Recommendation

**Recommend Option E: Hybrid labeled evaluation + expanded ranking-stability transfer.**

Reasoning: Option E is the only design that satisfies all three constraints simultaneously: it preserves the dissertation's Algorithm 1 contract for any metric that uses Layer A, it uses the 19 features-only targets for the Wave 4 small-panel question, and it minimizes researcher degrees of freedom by refusing to manufacture labels. It can answer codex Q7 in the bounded form that is actually possible before Layer A curation: "Is the expanded feature space large and stable enough to justify later Layer A curation for a real quorum test?"

Options B and pure C are rejected as primary definitions because they would turn feature-derived quantities into apparent outcomes. Option D is scientifically clean but would ignore the newly computed 19-target Tier 2 panel. Option A is a defensible fallback if implementation time is short, but it is too weak to carry the phrase "features-only LOPO" without the labeled 12-fold component.

### Predeclared terminology

- **Actual LOPO evaluation:** Only the 12 labeled feature matrices; metrics include MCC, ±10-window MCC, precision@20/50/80, enrichment, and callability endpoint summaries.
- **Expanded-panel transfer diagnostic:** The 28 unique target union; metrics include feature-spread coverage, sign stability, rank stability, top-decile overlap, and training-quorum reachability proxies. These are not Layer A validation metrics.
- **Features-only 3-core:** `freq`, `entropy`, `hscore`, where `hscore = freq * entropy` on labeled feature matrices and the existing `hscore` column is used in `cross_pathogen` CSVs. If the overlap drift gate fails, expanded-panel diagnostics fall back to the 2-core `freq, entropy`; labeled 3-core LOPO remains a labeled-panel sensitivity only.
- **Historical 4-core comparison:** Optional labeled-panel comparator only, using `freq, entropy, homoplasy, plddt` where available. It must not be evaluated on unlabeled cross_pathogen targets because homoplasy and pLDDT are absent there.

---

## Predeclared Scope

### Primary track (Option E)

Run a Wave 4 hybrid experiment with two linked components:

1. **Labeled 12-fold shared-feature LOPO.**
   - Input: 12 `feature_matrix_*.csv` files.
   - Feature set: features-only 3-core `freq`, `entropy`, `hscore=freq*entropy`.
   - Ground truth: `layer_a`.
   - Protocol: nested LOPO matching Algorithm 1's sign-fitting contract: for each held-out labeled pathogen, fit per-feature directional signs on the 11 labeled training pathogens; within-pathogen z-score each feature on training pathogens, compute Pearson correlation with `layer_a` within each training pathogen, aggregate signs by median correlation across the 11 training pathogens; zero/NA correlations are recorded as neutral and excluded from the sign vote unless all are zero/NA, in which case the feature is dropped for that fold; uniformly average signed z-scores; threshold at top 10%; evaluate on held-out Layer A.
   - Endpoints: MCC, ±10-window MCC, precision@20/50/80, enrichment, top-vs-bottom decile Layer A prevalence, training-fold callability diagnostics D1-D3 and held-out annotation-density D4 on labeled folds only; no expanded target receives a callability endpoint.
   - Comparator: historical 4-core on the same 12 folds only, loaded from or recomputed consistently with Wave 1/Wave 2 scripts.

2. **Expanded 28-target features-only transfer/stability diagnostic.**
   - Input: the 19 `cross_pathogen` CSVs plus the 9 labeled-panel targets not represented in `cross_pathogen`, harmonized to unique target slugs.
   - Denominator: report `n_unique_targets=28`, `n_labeled_eval=12`, `n_cross_pathogen_csv=19`, `n_overlap=3`, `n_unlabeled_expanded=16`.
   - Feature set: `frequency/freq`, `entropy`, `hscore`.
   - Ground truth: only `layer_a` for the 12 labeled targets; `ground_truth=-1` on cross_pathogen must remain ignored for evaluation. For overlap CSVs, `ground_truth=0` is also ignored; overlap files are audit-only and never treated as negatives.
   - Diagnostics:
     - Feature-spread coverage: compare 12 labeled vs 16 unlabeled expanded targets vs all 28 on eight predeclared meta-features: `n_positions`, mean frequency, std frequency, mean entropy, std entropy, mean hscore, variable-position fraction, and top-decile hscore density.
     - Sign stability: signs learned from labeled folds; assess whether signs are stable across bootstrap resamples of labeled pathogens and whether the expanded targets fall inside or outside the labeled feature-distribution envelope.
     - Ranking stability: for each target, compute top-10% positions under bootstrapped sign fits and report median pairwise Jaccard, 10th percentile Jaccard, and rank correlation across bootstraps. Use `random_seed=42`; compute Jaccard over top-10% callsets with deterministic tie-breaking by position; report constant-score targets as `no_result_constant_rank` for Spearman.
     - Quorum reachability proxy: a feature-space feasibility diagnostic only; pass requires `n_usable_targets >= 20`, at least 7 targets with median top-10% Jaccard >=0.60 and 10th percentile >=0.40, and at least 7 targets inside the labeled envelope on >=5/8 predeclared meta-features. This does not make any target callable.
     - Overlap audit: for `Dengue`, `HIV-1`, and `Norovirus`, compare rankings from labeled `feature_matrix_*` derived hscore vs cross_pathogen hscore to quantify schema drift. Declare hscore non-harmonizable if median overlap Spearman rho <0.70, median top-10% Jaccard <0.50, or at least two of three overlaps fail either threshold.

### Explicit non-claims

- Do not claim MCC, precision, recall, F1, enrichment against Layer A, or callability success on the 16 new unlabeled targets.
- Do not call feature-derived h-score top-decile positions "positives."
- Do not revise Algorithm 1 thresholds after seeing results.
- Do not add new features, new sequences, new Entrez queries, or new Layer A labels in this wave.
- Do not pool overlap targets twice; overlap CSVs are used for schema-drift auditing, not for increasing the unique target count.
- Do not describe expanded stability, overlap concordance, or quorum reachability as validation, held-out performance, callability success, or evidence that the 12-pathogen failure was an artifact.

---

## Predeclared Failure-Mode Branches

These responses are fixed before the Wave 4 results exist. Task 4 prose must follow the matching branch.

| Outcome | Predefined response |
|---|---|
| **Branch 1: Labeled 3-core LOPO is positive and expanded stability is high** | If the shared 3-core has labeled-panel mean MCC within 0.01 of historical 4-core and ≥4/12 labeled pathogens have positive top-vs-bottom decile deltas, while expanded-panel median top-decile Jaccard ≥0.60 and 10th percentile ≥0.40, conclude that the features-only path is technically viable and the features-only expansion plausibly motivates Layer A curation to test the small-panel/quorum-artifact hypothesis. Still state that Layer A curation is required before any deployment claim. |
| **Branch 2: Labeled 3-core is positive but expanded stability is weak** | Preserve the descriptive labeled-panel signal, but conclude that the 19 features-only targets are too heterogeneous or schema-shifted for stable transfer without additional feature harmonization. Next step becomes Layer A pilot plus feature augmentation, not expanded callability. |
| **Branch 3: Labeled 3-core is weak but expanded stability is high** | Conclude that frequency/entropy/h-score are stable engineering outputs but insufficient as Layer A predictors under the Algorithm 1 contract. Expanded stability alone cannot soften a weak labeled 3-core result; dissertation prose must state that stability is engineering reproducibility, not Layer A predictiveness. This supports the need for homoplasy/structure/PLM features or curated Layer A before any expanded LOPO claim. |
| **Branch 4: Both labeled 3-core and expanded stability are weak** | Treat the Tier 2 features-only sweep as a reproducible data-generation pilot only. Do not use it to defend Algorithm 1. Prioritize pilot Layer A curation and/or richer feature generation before any further LOPO experiments. |
| **Branch 5: Overlap schema drift is large** | If Dengue/HIV-1/Norovirus feature_matrix-derived hscore rankings and cross_pathogen hscore rankings have median Spearman ρ <0.70 or top-10% Jaccard <0.50, exclude hscore from expanded diagnostics and rerun/report a 2-core `freq, entropy` sensitivity, or stop at the input-audit stage if the 2-core rerun is not performed. The expanded transfer diagnostic is not interpretable until schema drift is explained. |
| **Branch 6: Quorum remains structurally unreachable** | If after de-duplication there are <20 unique usable targets or >25% fail basic feature-quality gates (`n_positions < 100`, all-zero frequency/entropy, or missing hscore), conclude that Wave 4 cannot assess future quorum feasibility. Report the engineering blocker and move to accession/feature repair, not inference. |
| **Branch 7: Apparent expanded success depends only on surrogate labels** | If any analysis path accidentally uses `ground_truth=-1` or top-decile hscore as positives for unlabeled targets, discard that result and rerun. Synthetic-label outcomes are not part of the primary or secondary evidence. |

---

## Implementation Tasks

## Task 1: Wave 4 scaffold + input audit

**Why:** Establishes the result directory, exact denominators, and schema harmonization before any inferential code runs.

**Files:**
- Create: `results/mutbench/codex_wave4/README.md`
- Create: `paper/dissertation/review/2026-04-30/wave4/`
- Create: `results/mutbench/codex_wave4/w4_input_inventory.csv`
- Create: `results/mutbench/codex_wave4/w4_feature_schema_audit.csv`

- [ ] Create `results/mutbench/codex_wave4/` and `paper/dissertation/review/2026-04-30/wave4/`.
- [ ] Write a README stating the Option E hybrid design, the no-Layer-A constraint, and denominators: 12 labeled, 19 cross_pathogen CSVs, 3 overlaps, 28 unique targets.
- [ ] Implement `scripts/codex_w4_features_lopo.py --audit-only`.
- [ ] Emit `w4_input_inventory.csv` with `slug,pathogen_label,source_type,is_labeled,is_overlap,audit_only,unique_target_inclusion,n_positions,has_freq,has_entropy,has_hscore,has_layer_a,ground_truth_values`; invariant: rows with `unique_target_inclusion=true` sum to 28 and rows with `audit_only=true` sum to 3.
- [ ] Emit `w4_feature_schema_audit.csv` for Dengue/HIV-1/Norovirus overlap drift: Spearman ρ and top-10% Jaccard between feature-matrix hscore and cross_pathogen hscore.
- [ ] Append one NOTES.md bullet. Do not commit unless explicitly requested.

---

## Task 2: Labeled 12-fold shared-feature LOPO

**Files:**
- Create: `scripts/codex_w4_features_lopo.py`
- Output: `results/mutbench/codex_wave4/w4_labeled_lopo_per_fold.csv`
- Output: `results/mutbench/codex_wave4/w4_labeled_lopo_summary.csv`
- Output: `results/mutbench/codex_wave4/w4_labeled_callability_recheck.csv`

- [ ] Implement shared-feature scoring: `freq`, `entropy`, `hscore=freq*entropy`.
- [ ] For each held-out labeled pathogen, fit Pearson signs on the other 11 labeled pathogens only using the predeclared median-correlation sign rule, z-score within pathogen, average signed z-scores, call top 10%, and evaluate against held-out `layer_a`.
- [ ] Per fold, emit `pathogen,n_positions,n_layer_a_pos,layer_a_prev,sign_freq,sign_entropy,sign_hscore,mcc_top10,mcc_window10,precision_at_20,tp_at_20,tp_at_50,tp_at_80,enrichment_top10,top_bottom_decile_delta,spearman_decile_rho,callability_d1_pass,callability_like_notes`.
- [ ] Include labeled-panel-only historical 4-core comparator columns: `historical_4core_mcc_top10,delta_3core_minus_4core,historical_4core_source`.
- [ ] Smoke test: `python scripts/codex_w4_features_lopo.py --labeled-only --smoke`.
- [ ] Full run: `python scripts/codex_w4_features_lopo.py --labeled-only | tee results/mutbench/codex_wave4/w4_labeled_lopo.log`.

---

## Task 3: Expanded 28-target transfer/stability diagnostics

**Files:**
- Output: `results/mutbench/codex_wave4/w4_expanded_target_scores.csv`
- Output: `results/mutbench/codex_wave4/w4_expanded_stability_per_target.csv`
- Output: `results/mutbench/codex_wave4/w4_expanded_feature_spread.csv`
- Output: `results/mutbench/codex_wave4/w4_expanded_quorum_reachability.csv`
- Output: `results/mutbench/codex_wave4/w4_overlap_schema_drift.csv`

- [ ] Harmonize one unique target table: 12 labeled feature matrices converted to `freq,entropy,hscore`, plus 19 cross_pathogen CSVs with overlap targets marked but not double-counted.
- [ ] Keep `Dengue`, `HIV-1`, and `Norovirus` labeled rows as evaluation rows; use `dengue_e`, `hiv1_gp120`, and `norovirus_vp1` only for schema-drift audit.
- [ ] Run 1,000 bootstrap sign fits with `random_seed=42`, resampling labeled pathogens with replacement; unlabeled targets are never sampled into sign fitting. Score all 28 unique targets under each fit.
- [ ] Per target, compute top-10% Jaccard across bootstraps, rank Spearman across scores, and sign-vote entropy.
- [ ] Compare the eight predeclared feature-spread meta-features for labeled 12, `n_unlabeled_expanded=16`, cross_pathogen 19, and all unique 28.
- [ ] Apply the structural quorum proxy: `n_usable_targets >= 20`, at least the same 7 targets with median top-10% Jaccard ≥0.60 and 10th percentile ≥0.40, inside the labeled envelope on ≥5/8 meta-features, and not dominated by all-zero frequency/entropy.
- [ ] Full run: `python scripts/codex_w4_features_lopo.py --expanded-stability --n-bootstrap 1000 | tee results/mutbench/codex_wave4/w4_expanded_stability.log`.

---

## Task 4: Figure, report, and dissertation prose

**Files:**
- Output: `results/mutbench/codex_wave4/w4_features_lopo_summary.png`
- Output: `paper/dissertation/review/2026-04-30/wave4/w4_tier2_features_lopo.md`
- Modify: `paper/dissertation/chapters_en/ch5_discussion.tex` only if results are interpretable and user approves prose insertion.

- [ ] Create `w4_features_lopo_summary.png` with four panels: labeled 3-core vs 4-core MCC; expanded feature-spread heatmap/PCA; per-target stability Jaccard; quorum proxy bars with exact denominators.
- [ ] Write `w4_tier2_features_lopo.md` with command provenance, denominators, overlap handling, no-Layer-A reminder, labeled endpoints, expanded stability endpoints, selected branch, and permitted/non-permitted claims.
- [ ] If the user requests manuscript edits, update Chapter 5 with the exact 28/12/16 denominator and keep the claim bounded to feasibility/stability.
- [ ] If prose is edited, build the PDF with `cd /proj/paper/paper/dissertation && bash build.sh`.

---

## Task 5: Codex review + memory closure

**Files:**
- Create: `paper/dissertation/review/2026-04-30/codex_wave4_plan_review_prompt.md`
- Create after execution: `/home/hwijun/.claude/projects/-proj-paper/memory/codex_wave4_results.md`
- Modify after execution: `NOTES.md`

- [ ] Draft `codex_wave4_plan_review_prompt.md` asking specifically about label leakage, circular surrogate labels, Option E, denominator handling, and the structural quorum proxy.
- [ ] Incorporate codex edits before Task 2 if verdict is `PROCEED WITH MODIFICATIONS`; stop and revise if `REVISE BEFORE PROCEED`.
- [ ] At completion only, write `codex_wave4_results.md` with denominators, labeled LOPO results, expanded stability results, failure-mode branch, and next steps.
- [ ] Append final NOTES.md closure bullet.

---

## Deliverables

### Plan and review

- `docs/plans/2026-04-30-wave4-tier2-features-lopo.md`
- `paper/dissertation/review/2026-04-30/codex_wave4_plan_review_prompt.md`

### Scripts

- `scripts/codex_w4_features_lopo.py`

### Result directory

- `results/mutbench/codex_wave4/README.md`
- `results/mutbench/codex_wave4/w4_input_inventory.csv`
- `results/mutbench/codex_wave4/w4_feature_schema_audit.csv`
- `results/mutbench/codex_wave4/w4_labeled_lopo_per_fold.csv`
- `results/mutbench/codex_wave4/w4_labeled_lopo_summary.csv`
- `results/mutbench/codex_wave4/w4_labeled_callability_recheck.csv`
- `results/mutbench/codex_wave4/w4_labeled_lopo.log`
- `results/mutbench/codex_wave4/w4_expanded_target_scores.csv`
- `results/mutbench/codex_wave4/w4_expanded_stability_per_target.csv`
- `results/mutbench/codex_wave4/w4_expanded_feature_spread.csv`
- `results/mutbench/codex_wave4/w4_expanded_quorum_reachability.csv`
- `results/mutbench/codex_wave4/w4_overlap_schema_drift.csv`
- `results/mutbench/codex_wave4/w4_expanded_stability.log`
- `results/mutbench/codex_wave4/w4_features_lopo_summary.png`

### Reports and optional manuscript edits

- `paper/dissertation/review/2026-04-30/wave4/w4_tier2_features_lopo.md`
- Optional, only with user approval after results: `paper/dissertation/chapters_en/ch5_discussion.tex`
- Optional, only if prose edited: `paper/dissertation/thesis_en.pdf`

### Memory

- `/home/hwijun/.claude/projects/-proj-paper/memory/codex_wave4_results.md`

---

## Codex Review Section

Ask codex for concrete edits, not a general thumbs-up. The eight review questions are:

1. **Design choice:** Is Option E the most defensible definition of "Tier 2 features-only LOPO at n≈30" given that 16 new targets have no Layer A, or should the plan choose a stricter Option A/D fallback?
2. **Degrees of freedom:** Are the expanded-panel diagnostics predeclared tightly enough to avoid post hoc selection of favorable stability metrics?
3. **Algorithm 1 contract:** Does the labeled 12-fold shared-feature LOPO preserve the Chapter 3 Algorithm 1 contract, especially Pearson sign-fitting on training labels only?
4. **No-label boundary:** Is the plan sufficiently explicit that the expanded 16 unlabeled targets cannot contribute MCC, precision, F1, enrichment against Layer A, TP@budget, or callability endpoint performance?
5. **Q7 answerability:** Does the structural quorum-reachability proxy actually answer "is 12-pathogen heterogeneity a small-panel artifact?", or should the plan limit itself to a narrower feasibility claim?
6. **Feature harmonization:** Is `hscore=freq*entropy` on labeled feature matrices a defensible harmonization with the cross_pathogen `hscore`, or should overlap drift determine whether hscore is included at all?
7. **Denominator handling:** Is the 28 unique target denominator correct and sufficiently protected against double-counting Dengue/HIV-1/Norovirus overlaps?
8. **Failure branches:** Are the predeclared branches strong enough to prevent overclaiming if expanded stability looks good but labeled 3-core performance is weak?

Expected review output:

- `PROCEED`, `PROCEED WITH MODIFICATIONS`, or `REVISE BEFORE PROCEED`
- concrete line-level edits to this plan
- explicit answer to whether Option E should remain primary

---

## References

- Wave 1 plan: `docs/plans/2026-04-30-codex-experiment-execution.md`
- Wave 2 plan: `docs/plans/2026-04-30-wave2-p5-callability.md`
- Wave 3 plan: `docs/plans/2026-04-30-wave3-p6-biological-nulls.md`
- Wave 3 memory: `/home/hwijun/.claude/projects/-proj-paper/memory/codex_wave3_results.md`
- Wave 3 codex review §Q7: `paper/dissertation/review/2026-04-30/codex_wave3_plan_review.md`
- Chapter 3 Algorithm 1 / nested-LOPO description: `paper/dissertation/chapters_en/ch3_methods.tex`
- Chapter 5 future-work promise: `paper/dissertation/chapters_en/ch5_discussion.tex`
- Existing labeled feature matrices: `results/mutbench/feature_analysis/feature_matrix_*.csv`
- Expanded cross_pathogen CSVs: `data/cross_pathogen/*_position_scores.csv`
- Expanded meta-features: `results/mutbench/expanded_panel_metafeatures.csv`
- Pilot accession manifest: `results/mutbench/pilot_accession_manifest.csv`

---

## Self-Review Checklist

- [x] Enumerates five concrete definitions (A-E)
- [x] Recommends exactly one primary option (E)
- [x] Explains why rejected options are weaker
- [x] Separates actual Layer A evaluation from unlabeled expanded diagnostics
- [x] Handles overlap denominator explicitly (`n_unique_targets=28`, `n_labeled_eval=12`, `n_cross_pathogen_csv=19`, `n_overlap=3`, `n_unlabeled_expanded=16`)
- [x] Includes predeclared failure-mode branches before results exist
- [x] Mirrors Wave 3 format: header, motivation, scope, design choices, deliverables, failure branches, codex review section, references
- [x] Does not request new data acquisition, Layer A curation, or commit
