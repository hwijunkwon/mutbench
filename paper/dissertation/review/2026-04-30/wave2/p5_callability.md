# P5 — Callability / Abstention Rule (Wave 2)

**Status:** Complete — 2026-04-30
**Plan task:** docs/plans/2026-04-30-wave2-p5-callability.md Task 2
**Verdict:** **0/12 CALLABLE for both 3-core and 4-core under default thresholds.** Predeclared "0/12" failure-mode branch triggered: Algorithm 1 is not deployable on this panel under the pre-registered rule. Move to Wave 3 (expanded panel).

## Command

```bash
cd /proj/paper && python scripts/codex_p5_callability.py
```

Wall time: ~12 minutes (single core).

## Inputs

- `results/mutbench/feature_analysis/feature_matrix_*.csv` — 12 pathogens, 10 features per position, `layer_a` ground truth
- LOO sign fitting per held-out pathogen (Pearson on concatenated training labels)
- 4 codex-specified pre-registered diagnostics + inversion guardrail (codex Wave 2 review v187b)

## Outputs

- `results/mutbench/codex_wave2/p5_callable_decisions.csv` — 24 rows (12 folds × 2 methods) with full diagnostic breakdown
- `results/mutbench/codex_wave2/p5_endpoint_summary.csv` — primary + secondary endpoints per method
- `results/mutbench/codex_wave2/p5_diagnostics_per_fold.csv` — flat per-(fold, method, diagnostic) view
- `results/mutbench/codex_wave2/p5_callable_subset.png` — diagnostic-bar facet by method
- `results/mutbench/codex_wave2/p5_run.log`

## Top-line findings

### 1. Predeclared 0/12 failure-mode branch triggered

| Method | n_callable | callable subset | abstained | mean MCC if callable | sum TP@50 if callable |
|---|---|---|---|---|---|
| 3-core | 0/12 | (empty) | all 12 | n/a | 0 |
| 4-core | 0/12 | (empty) | all 12 | n/a | 0 |

Per the predeclared P5 failure-mode branch:

> 0/12 callable → Algorithm 1 is not deployable on this panel under the pre-registered rule. Report this as the headline; preserve the descriptive role of P1/P2/P3. Move to Wave 3 (expanded panel) immediately.

### 2. Per-diagnostic pass rate (across 12 folds × 2 methods = 24 evaluations)

| Diagnostic | 3-core (12 folds) | 4-core (12 folds) | What it measures |
|---|---|---|---|
| **D1 top-decile separation** (≥7/11 quorum) | **0/12 pass** | **0/12 pass** | training-set generalization |
| D2 null-adjusted enrichment (lower CI > 1.10) | 4/12 pass (RSV, MERS, Zika, Rabies) | 1/12 pass (MERS) | iid-null superiority |
| D3 perturbation stability | 11/12 pass (Norovirus fails) | 3/12 pass | sign + score robustness |
| D4 sparse-label red flag | 11/12 pass (MERS fails) | 11/12 pass (MERS fails) | held-out evaluability |
| Inversion guardrail | 12/12 pass | 11/12 pass (MERS fires) | training-set monotonicity |

**D1 is the rate-limiting diagnostic.** No fold has ≥7/11 training pathogens with both lower CI > 0.02 AND point > 0.05 on top-bot decile prevalence delta. Maximum pass rate observed: 5/11 across all folds and methods.

### 3. D1 bottleneck explained

D1 measures top-decile separation across training pathogens. Per Wave 1 P2 (per-pathogen rank reliability), only 5/12 pathogens (Norovirus, Dengue, H3N2, Influenza_B, HIV-1) have strong-positive top-vs-bottom prevalence delta with CI excluding 0 and point > 0.05. When held-out is one of these 5, training has 10 strong + the rest. Even then, training pathogens that fail D1 individually pull the quorum below 7/11.

This is **structurally consistent** with the codex's specified rule: D1 is a generalization gate, and if only 5/12 pathogens have signal, the rule correctly says no LOPO fold has enough training generalization to deploy.

### 4. D2 paradox: sparse pathogens "pass"

D2 passes for RSV, MERS, Zika, Rabies (3-core) — pathogens that observed-MCC-wise FAILED in P1 (negative or zero). This is because D2 is computed across training pathogens (not the held-out). When the held-out is RSV, the 11 training pathogens include the 5 strong-signal ones (Norovirus, Dengue, H3N2, Influenza_B, HIV-1, plus HCV), and their (observed enrichment / null enrichment) ratios are high enough to push the bootstrap lower CI > 1.10. **D2 is a property of the training set, not the held-out** — by design.

The combined gate (D1 ∧ D2 ∧ D3 ∧ D4 ∧ ¬INV) = 0/12. D1 fails universally; even folds where D2/D3/D4 all pass cannot become callable.

### 5. D3 confirms P3 finding (pLDDT is unstable)

3-core perturbation stability: 11/12 pass (median Jaccard ≥ 0.85 typical, p10 ≥ 0.49 typical).
4-core perturbation stability: 3/12 pass (median Jaccard ~0.55-0.66 typical, often below 0.60 threshold).

The 4-core's pLDDT inclusion makes the callset less stable under sign-refit perturbations — consistent with P3 Shapley showing pLDDT contributes negatively (-0.0015 to MCC).

### 6. Inversion guardrail fires for 4-core MERS

For the MERS fold under 4-core: ≥2 training pathogens have bootstrap CI upper < 0 → inversion fires. Under 3-core, no fold inverts. This is consistent with the P2 finding that 4-core has 1 inversion case (Rabies) and full-10 has 2 (Rabies + RSV) — 3-core is the most monotone variant.

## Failure-mode branch applied

Per `docs/plans/2026-04-30-wave2-p5-callability.md` predeclared 0/12 branch:

> Algorithm 1 is not deployable on this panel under the pre-registered rule. Report this as the headline; preserve the descriptive role of P1/P2/P3. Move to Wave 3 (expanded panel) immediately.

**Implication:** The Cold-Start Algorithm 1 cannot be operationalised as a one-size-fits-all detector on the current 12-pathogen panel using a pre-registered abstention rule. This is **not a contradiction** with the dissertation's existing claim — Algorithm 1 was always framed as a Tier-1 cold-start prioritization heuristic, and Wave 1 showed signal exists on 5 callable pathogens; Wave 2 P5 shows that signal cannot be reliably predicted-in-advance with a 7/11-quorum LOPO callability rule on 12 pathogens.

The next step is Wave 3 P6 (biological-realistic local nulls, codex's recommended ordering) — testing whether the callable subset survives more credible nulls — followed by Tier 2 features-only LOPO at n≈30, where the larger training panel might satisfy a 7/30 or 9/30 quorum.

## Required prose changes (Task 4)

### ch4_results.tex

Insert new `\paragraph{Pre-registered callability rule (P5)}` after `para:null_calibration`:
- Cite all 4 pre-registered diagnostics + inversion guardrail with default thresholds
- Headline: 0/12 callable for both methods under defaults
- D1 is the rate-limiting gate (max 5/11 quorum observed)
- D3 confirms 3-core > 4-core perturbation stability (Shapley pLDDT negative)
- Frame as "the pre-registered abstention rule says 'do not deploy', preserving the descriptive role of P1/P2/P3"

### ch5_discussion.tex

Update the existing "Prospective Callability and Abstention Rule" subsection from "this is the protocol" to "this is the result":
- Wave 2 P5 with default thresholds yields 0/12 callable
- The rule is ROBUST in the sense that it correctly refuses to deploy when training generalization is insufficient
- Sensitivity sweep (Task 3) reports performance under threshold relaxation
- Wave 3 P6 (biological local nulls) and Tier 2 LOPO at n≈30 are the natural next experiments

## Caveats

- 3-core SARS-CoV-2 D1 returns NaN (n_total=10/11) — degenerate decile due to score ties. Inherits the P2 caveat. Does not change the headline (n_pass=4/10 < 7/11 either way).
- D4 prevalence band [1%, 20%] excludes MERS (0.7%). HCV (15.9%) is at the upper edge but passes. No edits to the band post hoc.

## Predeclared threshold sensitivity sweep (Task 3)

Per codex Wave 2 review §Q3 — sweep D1 quorum and D2 lower bound only (not D3, D4, or inversion). Results in `results/mutbench/codex_wave2/p5_threshold_sensitivity_sweep.csv`:

| Method | D1 quorum | n_callable across {D2 lower in 1.05, 1.10, 1.20, 1.50} |
|---|---|---|
| 3-core | 5/11 | **3, 2, 1, 0** |
| 3-core | 6/11 | 0, 0, 0, 0 |
| 3-core | 7/11 (default) | 0, 0, 0, 0 |
| 3-core | 8/11 | 0, 0, 0, 0 |
| 4-core | 5/11 | 1, 1, 1, 0 |
| 4-core | 6/11 | 0, 0, 0, 0 |
| 4-core | 7/11 (default) | 0, 0, 0, 0 |
| 4-core | 8/11 | 0, 0, 0, 0 |

**At any D1 quorum ≥ 6/11, regardless of D2 lower bound, the callable count is 0/12 for both methods.** The 0/12 outcome is robust to the predeclared sensitivity range.

### Pathology revealed by the most-permissive corner (quorum 5/11, D2 ≥ 1.05)

When the rule is relaxed to its most-permissive predeclared corner:
- 3-core selects callable = {SARS-CoV-2, RSV, Zika}, **mean MCC = −0.027** (callable subset performs WORSE than zero)
- 4-core selects callable = {Rabies}, **mean MCC = −0.049**

These are precisely the P1-negative pathogens (observed MCC ≤ 0). The combined gate selects sparse-/unstable-signal pathogens because D2's (observed enrichment / null enrichment) ratio can be inflated when the null is also small (sparse Layer A → both observed precision and null mean are tiny, but the ratio looks above 1.05). The rule does NOT identify the 5 P1-positive pathogens (Norovirus, Influenza_B, H3N2, HCV, Dengue) as callable at any swept configuration — those folds always fail D1 because the training set has at most ~4 P1-positive pathogens, never reaching the quorum.

**This is a feature, not a bug, of the codex-specified rule:** D1 is a generalisation gate that requires the method to work on the majority of training pathogens, not on the held-out itself. With only 5/12 strong-signal pathogens, no LOPO training set has 7+ strong-signal members, so D1 cannot pass at the predeclared default. Relaxation reveals the pathology of D2 alone — confirming that the conjunction of all five criteria (especially D1) is the safety-relevant gate.

## Cross-references

- Plan: `docs/plans/2026-04-30-wave2-p5-callability.md`
- Codex review (8 edits applied): `paper/dissertation/review/2026-04-30/codex_wave2_plan_review.md`
- Codex P1 hard-stop consultation (P5 spec source): `paper/dissertation/review/2026-04-30/codex_p1_hardstop_consultation.md`
- Wave 1 reports: `paper/dissertation/review/2026-04-30/wave1/{p1,p2,p3}_*.md`
- Diagnostic figure: `results/mutbench/codex_wave2/p5_callable_subset.png`
