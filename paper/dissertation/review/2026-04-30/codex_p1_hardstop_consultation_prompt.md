# Codex consultation — P1 HARD STOP triggered, next-step decision

## Context

Wave 1 of your full-rigor experiment slate has executed P3 (full lattice + Shapley), P2 (rank reliability), and P1 (100k-permutation null × 4 null types × 12 pathogens × 2 methods). All three commits landed (v182–v184). Per the plan you reviewed (`codex_wave1_plan_review.md`), the predeclared P1 failure-mode branch was:

> P1 iid Stouffer p > 0.05 globally → HARD STOP before Task 5. Remove any claim that Algorithm 1 beats a prevalence-preserving null. Reframe as exploratory ranking heuristic; keep P2/P3 as descriptive diagnostics only; do not add detector-agnostic or search-space-reduction language as a headline.

That gate triggered. We need your guidance on the next step.

## P1 result summary

**Headline:** 4-core MCC iid Stouffer one-sided p = 1.0 globally. 5/12 pathogens individually significant under iid; only 1/12 (Norovirus) survives the strictest local-burden-preserving null.

| Pathogen | Observed MCC (4-core) | iid p (one-sided) | local-burden p |
|---|---|---|---|
| Norovirus | +0.432 | 0.00001 | 0.00006 |
| Influenza_B | +0.219 | 0.00007 | 0.07203 |
| H3N2 | +0.159 | 0.00177 | 0.24578 |
| HCV | +0.150 | 0.00917 | 0.83467 |
| Dengue | +0.145 | 0.00553 | 0.07627 |
| EV-A71 | +0.050 | 0.299 | 0.452 |
| SARS-CoV-2 | −0.010 | 0.730 | 0.804 |
| HIV-1 | −0.010 | 0.690 | 0.884 |
| Zika | −0.023 | 0.786 | 0.871 |
| MERS | −0.028 | 1.000 | 1.000 |
| Rabies | −0.049 | 0.925 | 0.877 |
| RSV | −0.065 | 1.000 | 1.000 |

Null gradient (4-core MCC, # significant of 12 at p<0.05 one-sided):
- iid: 5/12
- circular_shift: 3/12
- protein_block_shuffle: 2/12
- **local_burden_preserving: 1/12 (Norovirus only)**

This matches your prior P1 prediction exactly: "Some exact-site signals will attenuate, especially in pathogens with regionally clustered Layer A labels. … Failure mode: most global significance disappears under local nulls."

**P3 finding (already committed v182):** 4-core lattice rank 87/1023; 3-core (`freq+entropy+homoplasy`) dominates 4-core (MCC 0.087 vs 0.081, rank 27 vs 87). Formal Shapley: pLDDT contribution slightly negative (−0.0015), esm2_llr strongly negative (−0.0144).

**P2 finding (already committed v183):** 4-core 5/12 with positive top-vs-bottom CI excluding 0; Rabies inverts (delta −0.123, CI excludes 0 in negative direction); TP@budget=50 = 66 vs random ~30.

The three results triangulate to: **Algorithm 1 has signal on a callable subset of 5 pathogens** (Norovirus, Influenza_B, H3N2, HCV, Dengue), is **flat or anti-monotone** on the other 7, and **most "above-null" signal is explained by local clustering** of Layer A labels.

This is consistent with v171 not-yet-learnable thesis (HBFWS Bayesian shrinkage failed at n=11).

## Decision needed

We've identified four options, ranked by adversarial-defense value:

### Option A. Honor HARD STOP, skip P4, proceed directly to Task 6 prose insertions

Apply the P1 failure-mode branch as written. Insert prose under all four sub-sections (P3, P2, P1, no-P4). Frame as "exploratory cold-start prioritization for a 5-pathogen callable subset." Wave 1 ends without P4. Wave 2 plan begins with P5 callability rule.

### Option B. Re-scope P4 to the callable subset only

Run P4 (detector consensus) restricted to the 5 callable pathogens (Norovirus, Influenza_B, H3N2, HCV, Dengue). Frame as "for the callable subset, ≥50% detector consensus enriches Layer A by X." Disclose that this is a within-subset reproducibility diagnostic, not a global detector-agnostic claim. **Risk:** sub-selection by P1 outcome could be cherry-picked; we would disclose this prominently.

### Option C. Skip P4 in Wave 1; promote P5 callability rule from Wave 2 to immediately follow P1

The P1 result IS the trigger for P5: define a pre-registered diagnostic that flags pathogens as callable using training-fold-only signals (not the P1 outcome itself), then evaluate Algorithm 1 strictly on the callable set. Wave 1 redefined as P1+P2+P3+P5 (no P4). Wave 2 begins with biological-realistic local nulls (your P6).

### Option D. Re-run P1 with paired-bootstrap or sign-flip aggregation instead of Stouffer

The Stouffer global p = 1.0 is partially an artifact of mixed-direction observations (5 positive, 6 near-zero, 1 negative observed MCC). A paired bootstrap of the 12 (observed − null_mean) deltas would treat the MCC as a directional signed signal across the panel, which is arguably more honest given the heterogeneity. **Risk:** reframing the test post hoc to get a more favorable global p is exactly the kind of move the predeclared branch was designed to prevent.

## Specific questions for you

### Q1. Is HARD STOP correctly triggered?

The Stouffer one-sided p was the predeclared global statistic. It is 1.0. That's unambiguously > 0.05. Should we treat this as the binding outcome, or do you accept that Stouffer with mixed-direction observed values is a degenerate case where a pre-registered alternative (like a global signed-rank test) would have been better?

### Q2. Which of Options A–D do you recommend?

If A: confirm the prose plan. If B: spell out the cherry-pick disclosure. If C: spell out a P5 protocol that uses ONLY training-fold-only diagnostics to predeclare callable status (not the P1 outcome). If D: provide the alternative test specification.

### Q3. What pre-registered diagnostics define "callable" without leaking the P1 outcome?

If we go with Option C (or any future P5), we need diagnostics that are computed from training pathogens only (per nested-LOPO fold). Candidates from your slate were "top-decile score separation, null-adjusted enrichment lower bound above 1.0, perturbation Jaccard above a threshold, no sparse-label red flag." Please specify the threshold values and operationalization.

### Q4. Should P4 ever be run on the 12-pathogen panel as-is?

If P1 says Algorithm 1 doesn't beat null globally, does a "detector-agnostic consensus" claim ever become defensible on this panel? Or should P4 be deferred until the panel expands (Tier 1 pilot 3 + Tier 2 features-only at n=30) and re-tested with new Layer A?

### Q5. Defense-readiness implications

Given P1+P2+P3 outcomes, what is the new defense risk score? You scored Wave 1 "medium" pre-execution and "low-medium" with edits. With these results, where does it land?

## Output format requested

Single review document at `paper/dissertation/review/2026-04-30/codex_p1_hardstop_consultation.md`:

1. **Verdict** for each option (A, B, C, D): RECOMMEND / ACCEPTABLE / REJECT, with one-sentence reason
2. **Single recommended path forward** (one of the four, or a hybrid)
3. **Pre-registered callability diagnostics** if Option C is recommended (concrete thresholds)
4. **P4 disposition** — defer to expanded panel, run on subset, or skip permanently
5. **Defense-readiness risk re-scoring** (low / medium / high)

Keep under ~1200 words. Direct, no hedging. The candidate is asking for binding guidance.
