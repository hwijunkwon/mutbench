# Codex consultation — Wave 2 P5 plan review

## Context

Wave 1 closed v186 with three completed audits (P3 v182, P2 v183, P1 v184) and prose insertions (v185). The P1 HARD STOP triggered on the predeclared rule (iid Stouffer one-sided p=1.0 globally), and you provided binding guidance in `codex_p1_hardstop_consultation.md` (Option C: skip P4, promote P5 callability rule, use the four pre-registered diagnostics + inversion guardrail you specified in §3).

The candidate has now drafted a Wave 2 plan implementing your P5 spec. **Plan file:** `docs/plans/2026-04-30-wave2-p5-callability.md`.

## What the plan does

For each of 12 LOPO folds (held-out p_k, training = 11 others) × 2 methods (3-core primary, 4-core secondary):

1. Fit signs on training (Pearson on concatenated training labels per feature).
2. Compute four diagnostics on the 11 training pathogens:
   - **D1 top-decile separation:** per training pathogen, top-bot decile prevalence delta + 1{,}000-resample bootstrap CI; method passes if lower CI > 0.02 AND point > 0.05 in **≥7/11** training pathogens.
   - **D2 null-adjusted enrichment:** per training pathogen, observed top-decile enrichment ÷ mean null enrichment under 10{,}000 iid prevalence-preserving permutations; 1{,}000-bootstrap of the ratio across 11 training pathogens; passes if **lower 95% > 1.10**.
   - **D3 perturbation stability:** 200 perturbations per training pathogen — jitter feature z-scores by 0.10 × per-feature SD AND re-fit signs on a bootstrap of training pathogens; pairwise Jaccard of top-10% callsets aggregated to median + 10th percentile; passes if **median ≥ 0.60 AND 10th pct ≥ 0.40**.
   - **D4 sparse-label red flag (held-out only):** ≥10 Layer A positives, ≥200 rankable positions, prevalence ∈ [1%, 20%]. Uses no scores or held-out labels.
3. Inversion guardrail: not callable if **≥2 training pathogens have CI upper bound < 0** OR **median Spearman ρ ≤ 0**.
4. Callable = D1 ∧ D2 ∧ D3 ∧ D4 ∧ ¬inversion.
5. If callable, deploy method on held-out and record observed MCC + TP@50.
6. Sensitivity sweep over D1 quorum ∈ {5/11, 6/11, 7/11, 8/11} × D2 lower-bound ∈ {1.05, 1.10, 1.20, 1.50} = 32 configs.
7. Endpoints:
   - Primary: mean MCC + sum TP@50 on callable; identity + count of abstained.
   - Secondary: callable fraction; coverage-performance tradeoff vs always-deploy + random-on-abstained.

Compute budget: ~1 CPU-hour total (10k iid perms × 11 training × 12 folds × 2 methods + 200 perturbations × 11 × 12 × 2 + the 32-config sweep).

## Predeclared failure-mode branches (in plan)

- 0/12 callable → not deployable; preserve descriptive role of P1/P2/P3; move to Wave 3
- 1–4/12 → report callable + abstain; do not generalise
- 5–9/12 → expected; report performance + coverage tradeoff
- 10–12/12 → revisit thresholds for over-permissiveness
- Inversion-fired ≥1 fold → report which; cross-check Rabies (P2 inversion result)

## Specific questions for you

### Q1. Implementation fidelity

Does the operationalisation of D1–D4 + inversion guardrail match your §3 spec? Specifically:
- D1 quorum ≥7/11 (your spec didn't specify a count). Is 7/11 the right default, or should it be 8/11 or "at least majority but not strict"?
- D2 bootstrap is over the 11 training pathogens of the (observed/null) ratio. Is this the right resampling unit (vs. per-pathogen lower bound averaged)?
- D3 perturbation noise scale 0.10 × per-feature SD. Is 0.10 the intended magnitude, or should it tie to a specific source (e.g., training measurement variance)?
- D3 sign re-fit on bootstrap of training pathogens (random subset with replacement). Is this the intended source of perturbation, or should signs stay fixed and noise come only from the z-score jitter?
- D4 prevalence range [1%, 20%]. Should the upper bound be tighter (e.g., 15%) given that HCV (15.9%) sits at the edge?

### Q2. Inversion guardrail scope

The guardrail is currently **per-method** (3-core / 4-core separately). Should it instead be **method-agnostic** — if the data shows inversion under any reasonable scoring on the 11 training pathogens, abstain regardless of method? Or is per-method correct because we want to allow 3-core to be callable on a fold where 4-core might not be?

### Q3. Default thresholds

You provided default thresholds explicitly. The plan keeps them as defaults and runs an inner LOO sweep around them. Is the sweep configuration ({5/11..8/11} × {1.05..1.50}) appropriate, or do you want a different range? Should the sweep also vary D3 thresholds, D4 prevalence band, or the inversion-guardrail count threshold?

### Q4. Endpoint reporting

Codex §3 spec: "MCC and TP@50 on callable held-out pathogens only, with the number and identity of abstained pathogens reported in the same table." Should we also report:
- Per-pathogen abstention reason (which of D1/D2/D3/D4/inversion failed)?
- The "always-deploy + random on abstained" baseline as a competitor?
- Calibrated decision-curve at multiple budgets (20, 50, 80) on callable?

### Q5. Cross-check against P1's 5 iid-significant pathogens

The plan calls for a qualitative cross-check: P5 callable subset should overlap meaningfully with P1's 5 iid-significant set (Norovirus, Influenza_B, H3N2, HCV, Dengue), since both detect "method has signal here." Should this be made formal (e.g., expected overlap ≥3/5)? Or is overlap a hindsight measure that should not be a pre-registered criterion?

### Q6. Plan-level concerns

Anything else in the Wave 2 plan that needs correction, addition, or removal before Task 2 executes? Particularly: data leakage paths, threshold gaming, or implicit assumptions you can spot.

### Q7. After P5 — Wave 3 ordering

Conditional on P5 success (≥1 callable), which Wave 3 experiment is highest ROI:
- (a) Pilot 3 Layer A literature curation for YFV/Lassa/WNV (multi-day human work)
- (b) Tier 2 features-only LOPO at n≈30 with the existing 19 pathogen position scores (no Layer A on most)
- (c) Tier 3 EVE/PLM site-effect via the prepared `tools/eve_container/`
- (d) P6 biological-realistic local nulls (extends P1 with domain-aware nulls) on the existing 12-pathogen panel

## Output format requested

Single review document at `paper/dissertation/review/2026-04-30/codex_wave2_plan_review.md` with:

1. **Verdict:** PROCEED AS-IS / PROCEED WITH MODIFICATIONS / REVISE BEFORE PROCEED
2. **Per-question answer** (Q1–Q7), one short paragraph each
3. **Concrete edits** to the plan if needed (filename, line, change)
4. **Wave 3 ordering recommendation** (Q7)

Keep under ~1500 words. Direct, no hedging.
