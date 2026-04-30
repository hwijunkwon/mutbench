# Codex consultation — Wave 3 P6 plan review

## Context

Wave 1 closed v186 (P1+P2+P3 done; P4 skipped per HARD STOP). Wave 2 closed v191 (P5 callability rule executed; 0/12 callable under default + sweep robust). Cumulative defense narrative: Algorithm 1 has descriptive signal on 5 callable pathogens, formally bounded by pre-registered abstention rule. Defense risk: medium per your prior Wave 2 review.

Per your prior recommendations:
- `codex_p1_hardstop_consultation.md` §4: "biologically-realistic local nulls" recommended for expanded panel
- `codex_full_rigor_experiment_slate.md` Tier 2 P5: "biologically realistic local nulls for clustered labels and clustered calls"
- `codex_wave2_plan_review.md` §Q7: P6 biological-realistic local nulls is the **#1 Wave 3 priority** (highest ROI for defense; addresses the largest remaining concern that callable signal might be domain-clustering artifact)

The candidate has now drafted the Wave 3 plan. **Plan file:** `docs/plans/2026-04-30-wave3-p6-biological-nulls.md`.

## What the plan does

Run four new biologically-realistic local nulls on the existing 12-pathogen panel using the P1 vectorized batched-numpy infrastructure. Each null shuffles Layer A labels within strata defined by biological structure or evolution:

- **P6.1 SASA-stratified:** 5 quintiles of solvent-accessible surface area
- **P6.2 pLDDT-stratified:** 5 quintiles of AlphaFold/ESMFold structure confidence
- **P6.3 SASA × frequency joint:** 3×3 = 9 cells (SASA tertiles × frequency tertiles)
- **P6.4 pLDDT × entropy joint:** 3×3 = 9 cells (pLDDT tertiles × entropy tertiles)

Strata computed per pathogen from existing `feature_matrix_*.csv` columns (`sasa`, `plddt`, `freq`, `entropy`). 100,000 permutations per (pathogen × null × method), same metrics as P1 (MCC@top-10%, ±10-window MCC, top-20 precision, enrichment), one-sided primary p + Stouffer aggregation.

Compute budget: ~5–10 min on 16 cores (96 jobs, batched numpy reuse from P1).

## Predeclared failure-mode branches (in plan)

- **0/12 individually significant under all four P6 nulls** → signal fully reducible to biological patterns; reframe.
- **1–4/12** → honest disclosure on subset.
- **5+/12** → preserve current callable-subset framing.
- **Norovirus survives all four** → strongly defensible.
- **Norovirus fails all four** → re-examine v176 Norovirus VP1 layer-A construction.
- **Stratum collapse** (e.g., MERS too few positives in 9-cell joint null) → skip pathogen for that null; do not impute.

## Specific questions for you

### Q1. Null type selection

You previously suggested "biologically realistic local nulls" generically. Are SASA-stratified, pLDDT-stratified, and the two joint-strata nulls the right four operationalisations? Should we add or remove any:
- **Add**: dN/dS-stratified? Secondary-structure-stratified (helix/sheet/loop)? Within-protein-domain shuffles (would require domain annotations per pathogen)?
- **Remove**: Is the joint pLDDT × entropy too redundant with P1's local-burden null (which used freq+entropy)?

### Q2. Quintile vs. tertile binning

The plan uses 5 quintiles for the marginal nulls (P6.1, P6.2) and 3 tertiles for the joint nulls (P6.3, P6.4) so the joint cells have ≥1 SASA pos per cell. Is this granularity correct, or do you prefer:
- 5×5 = 25 cells for the joint nulls (riskier — many empty cells, especially for sparse-Layer A pathogens like MERS)
- 4 quartiles uniformly (compromise)
- continuous-stratified shuffles via local rank-binning

### Q3. Stratum collapse handling

For pathogens with sparse Layer A (e.g., MERS has 9 positives, 0.7% prevalence), some 9-cell joint strata may have 0 positives → no labels to permute. The plan's predeclared rule: "skip that pathogen for that null type and report as no-result; do not impute." Is this correct, or should we:
- (a) Pool sparse cells into adjacent cells (loses some stratification specificity)
- (b) Drop the joint null entirely for sparse pathogens (consistent with current plan)
- (c) Use 2×2 reduced binning for sparse pathogens (introduces pathogen-specific binning, which is post hoc)

### Q4. Comparison against P1 local-burden null

P1's `local_burden_preserving` already stratified by local mean(freq+entropy) in a ±5 window. P6.4 (pLDDT × entropy joint) and P6.3 (SASA × frequency joint) overlap with this conceptually. Should we:
- (a) Keep all four P6 nulls as planned, noting overlap with P1 local-burden in the report
- (b) Drop P6.4 (least independent from P1 local-burden) and add a different null (e.g., domain-stratified)
- (c) Reframe P6 as "structurally-explicit nulls" to differentiate from P1's evolution-only stratification

### Q5. Headline statistic

P1's headline was the per-pathogen iid → local-burden gradient (5/12 → 1/12). For P6, what's the analogous headline? Options:
- (a) "How many pathogens individually significant under each P6 null?"
- (b) "Does Norovirus (the only P1 local-burden survivor) also survive all four P6 nulls?"
- (c) "Combined P1+P6 8-null gradient: at the strictest null, how many pathogens survive?"

The plan currently does (c) via the unified gradient figure. Is this the right framing?

### Q6. Wave 3 scope

The plan restricts Wave 3 to P6 only (excludes Tier 2 features-only LOPO at n≈30, pilot 3 Layer A curation, EVE/PLM Tier 3). Is P6-only the right Wave 3 scope, or should it be combined with:
- Tier 2 features-only LOPO using the 19 untracked position score CSVs (no Layer A on most, but possible self-consistency / detector stability checks)
- A small subset of pilot 3 Layer A literature curation (just YFV E or just Lassa GPC, ~1 day each)?

### Q7. After P6 — Wave 4 ordering

Conditional on P6 success (≥1 pathogen survives), what's the Wave 4 priority?
- (a) Tier 2 features-only LOPO at n≈30 (cheap, tests panel-size hypothesis)
- (b) Pilot 3 Layer A curation YFV/Lassa/WNV (multi-day manual)
- (c) Tier 3 EVE/PLM site-effect via prepared container
- (d) Defense rehearsal / 6-agent review of the cumulative dissertation

### Q8. Plan-level concerns

Anything else in the Wave 3 plan that needs correction, addition, or removal before Task 2 executes? Particularly: data leakage paths, post hoc null selection, or implicit assumptions you can spot.

## Output format requested

Single review document at `paper/dissertation/review/2026-04-30/codex_wave3_plan_review.md` with:

1. **Verdict:** PROCEED AS-IS / PROCEED WITH MODIFICATIONS / REVISE BEFORE PROCEED
2. **Per-question answer** (Q1–Q8), one short paragraph each
3. **Concrete edits** to the plan if needed (filename, line, change)
4. **Wave 4 ordering recommendation** (Q7)
5. **Defense-readiness risk re-scoring** (low / medium / high)

Keep under ~1500 words. Direct, no hedging.
