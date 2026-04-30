# Codex consultation — Wave 1 execution plan review

## Context

You previously authored two slates of experiments for the MutBench dissertation:
- `paper/dissertation/review/2026-04-30/codex_experiment_proposals.md` (P1–P5, ≤24-hr-each constrained)
- `paper/dissertation/review/2026-04-30/codex_full_rigor_experiment_slate.md` (Tier 1–3, time relaxed)

The candidate has now drafted a **Wave 1 execution plan** to run the four
Tier-1 method-core experiments first (P1 null calibration, P2 rank
reliability, P3 full 2^10 lattice + Shapley, P4 detector consensus). Wave
2 (P5 callability/abstention) and Wave 3 (pilot 3 Layer A curation, Tier
2 features-only LOPO at n=30, Tier 3 EVE/PLM site-effect) are deferred to
later plans.

**Plan file:** `docs/plans/2026-04-30-codex-experiment-execution.md`

## Existing infrastructure on disk (already collected)

- `results/mutbench/feature_analysis/feature_matrix_*.csv` — 12 pathogens, 10 features per position, ground_truth (Layer A) column
- `results/mutbench/feature_analysis/feature_ablation_nested_lopo.csv` — 4-core vs full-10 nested-LOPO MCC (12 folds)
- `results/mutbench/feature_analysis/subset_selection_robustness_210combos.csv` — 4-of-10 subsets only (210 rows)
- `results/mutbench/stage3_full_results.csv` — 8580 rows = 20 scoring × 39 detector × 11 pathogens, columns: pathogen, scoring, detector, family, mcc, precision, recall, f1, n_detected
  - **NB**: detector callset *positions* are NOT persisted in this CSV; only summary metrics. Reconstruction may require re-running `run_stage3_full_detectors.py` with a `--save-positions` flag.
- `data/cross_pathogen/*_position_scores.csv` — 19 new pathogens (pilot 3 yfv/lassa/wnv + Tier 2 16 species), but **ground_truth column is placeholder (-1) — Layer A not yet curated**.
- `tools/eve_container/` — PyTorch 2.1.2 EVE container, smoke-tested on RTX 4090 sm_89, ready but not used in Wave 1.

## Wave 1 plan summary

**Task 1**: scaffold `results/mutbench/codex_wave1/` + README
**Task 2 (P3)**: enumerate all 1023 non-empty subsets of the 10 features, same nested-LOPO + top-10% + MCC protocol as `feature_ablation_nested_lopo.py`. Compute Shapley as mean marginal v(S∪{f}) − v(S) over subsets not containing f.
**Task 3 (P2)**: per-pathogen decile/ventile prevalence, Layer A enrichment with bootstrap 95% CI, isotonic calibration on training pathogens, ECE + Brier on held-out, decision curves at budgets {20, 50, 80}. Compare 4-core vs full-10 vs each single feature vs random rank.
**Task 4 (P1)**: 100k permutations × 4 null types per pathogen = 4.8M MCC evals (multiprocessing pool of 8 → ~17 min). Null types:
1. iid prevalence-preserving (label shuffle)
2. circular shift within sequence
3. protein-block shuffle (50-residue blocks as proxy when domain annotation absent)
4. local-burden-preserving (5-bin entropy/frequency strata match)

**Task 5 (P4)**: pairwise Jaccard + Spearman + family-consensus from `stage3_full_results.csv`. Consensus thresholds 25/50/75% of detectors. Will likely require persisting detector callset positions first.
**Task 6**: insert 4 subsubsections in ch4_results.tex + Limitations paragraph in ch5_discussion.tex with concrete numbers.
**Task 7**: write `~/.claude/projects/-proj-paper/memory/codex_wave1_results.md` and update MEMORY.md index.

Each task ends with a NOTES.md bullet and a git commit (v181 → v187).

## Specific questions for you

### Q1. Scope and ordering
Is **P3 → P2 → P1 → P4** the right order for Wave 1? P3 is cheapest and stress-tests Algorithm 1's "non-arbitrary 4-core" claim. P1 is highest-stakes (100k-permutation null) — should it move first to fail-fast? Or is the current "build prose foundation first, then null-stress-test it" order defensible?

### Q2. Protocol fidelity to your slate
The plan implements:
- **P1 null types** as four separate runs rather than nested. Acceptable or should they be combined (e.g., run only the strongest local null, since iid + circular are widely known to be too easy)?
- **P3 Shapley** as **mean marginal v(S∪{f}) − v(S)** over subsets, NOT the formal Shapley with binomial weights `1 / C(n−1, |S|)`. Justification: full Shapley needs all 2^9 = 512 subsets per feature (the lattice gives this for free), and the simplified mean is monotonically ranked the same way 95%+ of the time. Is the simplification acceptable or should we compute the formal weighted Shapley?
- **P2 calibration** uses isotonic regression on training pathogens. Your slate says "simple nonparametric calibration curve" — isotonic is the obvious choice, but should we additionally report Platt or beta-calibration for sensitivity?

### Q3. P4 detector-consensus — re-run required?
`stage3_full_results.csv` has summary metrics only, not callset positions. To compute Jaccard / consensus we need the actual position lists. Two options:
- (a) Re-run `run_stage3_full_detectors.py` with a `--save-positions` flag for the 4-core and full-10 scorings only (not all 20 scorings, ~30 min).
- (b) Restrict P4 to a smaller subset of (scoring × detector) cells where positions are already available somewhere in the repo.

Is (a) acceptable, or does it bias the consensus claim by including only the two scorings the author already favors? Should we include a few control scorings (e.g., frequency-only, entropy-only) for fairness?

### Q4. Out-of-scope items
Wave 1 does **not** include:
- pilot 3 Layer A curation (multi-day manual literature work for YFV/Lassa/WNV)
- Tier 2 features-only LOPO (n=30) — needs Layer A on at least some of the 19 new pathogens, otherwise we can only compute distributional / consensus stability, no MCC
- EVE Tier 3 site-effect (container ready but not run)

Is deferring these to Wave 2/3 correct, or does any of them belong in Wave 1 because it interacts with one of P1–P4?

### Q5. Failure-mode handling
What is the predefined response if:
- (i) P1 iid Stouffer p > 0.05 globally? (Would invalidate the headline method claim.)
- (ii) P3 4-core ranks > 50/1023? (Would invalidate "non-arbitrary 4-core.")
- (iii) P2 calibration slope is essentially flat across deciles? (Would force "ranked screening only" framing.)
- (iv) P4 detector consensus enrichment ≤ detector-mean? (Would invalidate "detector-agnostic" framing.)

Should the plan include explicit "if X then revise prose to Y" branches, or is it acceptable to handle these reactively?

### Q6. Documentation cadence
The plan documents at three levels:
- **NOTES.md** (one bullet per task, lightweight)
- **`results/mutbench/codex_wave1/`** (CSVs + figures + run logs)
- **`~/.claude/projects/-proj-paper/memory/codex_wave1_results.md`** (memory file at end)
- **dissertation prose** (4 subsubsections inserted only after all 4 results stable)

Is this appropriate, or should there also be a per-task standalone `.md` report under `paper/dissertation/review/2026-04-30/wave1/` (matching the codex_ivv/cycle pattern)?

### Q7. What would you add or remove?
Anything you'd cut, add, reorder, or strengthen. Particularly: are there cheap audits (CPU-hours small) that the plan misses and that would meaningfully improve defense readiness?

## Output format requested

Please produce a single review document at `paper/dissertation/review/2026-04-30/codex_wave1_plan_review.md` with:

1. **Verdict**: PROCEED AS-IS / PROCEED WITH MODIFICATIONS / REVISE BEFORE PROCEED
2. **Per-question answer** (Q1–Q7), one short paragraph each
3. **Concrete edits** to the plan if needed (filename, line, change)
4. **Pre-defined failure-mode responses** (Q5) as a small table
5. **Time-to-defense risk score** (low/medium/high) given the plan as-is

Keep it under ~1500 words. Direct, no hedging — you've already provided the slate, this is a fidelity check.
