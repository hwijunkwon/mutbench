# MutBench dissertation — FULL experiment slate (relaxed time constraint)

## Context update

Earlier you proposed 5 experiments (P1–P5) under a ≤24-hr-each constraint
(see `paper/dissertation/review/2026-04-30/codex_experiment_proposals.md`).
The candidate now wants a **full-rigor experiment slate** — time is no longer
a binding constraint (weeks–months acceptable). Update your proposals.

## What this changes

You may now propose:

1. **Full versions of P1–P5** (deeper bootstrap counts, larger MCMC, more
   strata, more pathogens, finer-grained diagnostics — whatever you'd want
   for a journal-grade method paper, not just defense survival).
2. **Experiments you previously excluded due to time** that are now in scope:
   - Multi-week manual Layer A curation for selected new pathogens
   - VAE/EVE training (was abandoned in 2026-04 due to OOM with old EVE code
     on PyTorch 2.5; only E2_HCV and E_DENV completed; do NOT propose unless
     you have a workaround)
   - >24-hr ML training (XGBoost/RF stacking already failed, but consider:
     pathogen-aware multi-task learning, graph neural networks on phylogeny,
     transformer over MSA columns, etc.)
   - Larger Bayesian models (joint hierarchical with more levels, GP priors
     over phylogeny, Dirichlet-process partitions)
   - Cross-domain extensions (DMS independent evaluation expansion beyond
     current ProteinGym subset; structural-conservation overlay across
     more pathogens; etc.)
3. **Experiments outside the original 5** that are now ROI-positive given
   weeks of compute (e.g., genuine prospective backtesting with held-out
   future windows; re-running Cycle 7B with 10× more bootstrap iterations;
   exhaustive subset selection beyond 4-of-10; alternative ground-truth
   sources beyond Layer A).

## Constraints that still hold

- **n=11 panel-size constraint**: 7-paradigm convergence on adaptive
  weighting is a real result. Proposing a new adaptive method that "might
  work this time" needs strong justification for why it'd escape the
  panel-size bottleneck.
- **Layer A annotation cost**: each new pathogen ≈ 1–2 weeks of literature
  curation. Propose specific pathogens worth that cost.
- **Method-defensibility**: the candidate's biggest worry remains "no
  plausible method." Proposals must materially help that, not just add
  more analyses.
- **Negative results**: HBFWS p=0.78, Cycle 7B all 6 fail, LOPO 0/11 are
  archived. Do not propose to re-run these unless with a concrete
  improvement (e.g., new pathogens added).

## Your task

Produce **a comprehensive ranked experiment slate** organized in three tiers:

### Tier 1 — Method core (highest ROI for "plausible method" claim)
Experiments that directly strengthen Algorithm 1's empirical case or extend
it into a richer method (e.g., calibrated callability, panel-conditional
abstention, multi-source aggregation with formal guarantees).

### Tier 2 — Robustness / honest disclosure
Permutation nulls, Shapley audits, sub-lineage splits, alternative GT
sources, alternative tests — things that close defense questions without
adding new claims.

### Tier 3 — Genuinely new contributions
Experiments that, if successful, add a new contribution to the dissertation
(e.g., panel-scale Layer A curation enabling a real adaptive validation;
prospective backtest with proper held-out future window; cross-pathogen
transfer learning; calibration-aware ensemble).

For **every** experiment provide:

1. **Hypothesis** (1 sentence).
2. **Protocol** (1 paragraph — be specific about data, comparison, test).
3. **Expected outcome** (your honest prior, including failure modes).
4. **Defense question pre-empted** (or "new contribution" if Tier 3).
5. **Compute/time budget** (CPU-hours and wall-clock weeks).
6. **What this adds to the dissertation** (new subsection? new figure?
   new table? new chapter?).
7. **Risk if it fails** (does the dissertation get worse, stay same, or
   honestly improve via disclosure).

End with a **prioritized execution order** assuming sequential execution,
plus a flag on which experiments could be parallelised (e.g., independent
data curation in week 1 while compute jobs run in week 2).

Aim for 8–12 total experiments. Do not pad.
