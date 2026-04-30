# Wave 3 P6 — Biological-Realistic Local Nulls Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement task-by-task.

**Goal:** Extend the P1 null-calibration audit (Wave 1) with biologically-realistic local nulls that preserve protein-structural and evolutionary strata while shuffling Layer A labels. Tests whether Algorithm 1's signal is reducible to obvious biological patterns ("surface positions vary more", "low-pLDDT flexible regions accumulate mutations") or whether it captures something beyond those patterns.

**Architecture:** Reuse the P1 vectorized batched-numpy MCC machinery (`scripts/codex_p1_null_calibration.py`). Add four new null types that stratify positions by biologically meaningful features (SASA, pLDDT, joint SASA×frequency, joint pLDDT×entropy) and shuffle Layer A labels within each stratum. Keep the same 100,000-permutation budget per (pathogen × null × method) as P1, with vectorized batched MCC, ±10-window MCC, top-20 precision, and enrichment metrics.

**Tech Stack:** Python 3, NumPy, pandas, scipy, multiprocessing. No GPU. Compute budget: ~30 min single-thread / ~5 min 16-core for 100k perms × 4 new nulls × 12 pathogens × 2 methods = 9.6M batched MCC evaluations.

**Documentation cadence:** Per task: NOTES.md bullet + standalone Markdown report under `paper/dissertation/review/2026-04-30/wave3/p6_*.md`. Memory written ONLY at Wave 3 closure (Task 5).

**Spec source:** `paper/dissertation/review/2026-04-30/codex_p1_hardstop_consultation.md` §4 ("biologically-realistic local nulls") + `codex_full_rigor_experiment_slate.md` Tier 2 P5 ("biologically realistic local nulls for clustered labels and clustered calls") + codex Wave 2 review §Q7 (P6 ranked first for Wave 3).

**Out of scope (Wave 4+ plans):** Tier 2 features-only LOPO at n≈30 (requires Layer A on subset of new pathogens), pilot 3 Layer A literature curation (multi-day manual), Tier 3 EVE/PLM site-effect via `tools/eve_container/`.

---

## Pre-registered null types (P6)

Each null shuffles Layer A labels within strata defined by biological structure or evolution. **Strata are computed per pathogen from the existing `feature_matrix_*.csv` columns** — no new data acquisition.

| Tag | Stratification | Rationale |
|---|---|---|
| **P6.1 SASA-stratified** | 5 quintiles of solvent-accessible surface area (column `sasa`) | Tests whether signal reduces to "surface-exposed positions tend to be Layer A". |
| **P6.2 pLDDT-stratified** | 5 quintiles of AlphaFold/ESMFold structure confidence (column `plddt`) | Tests whether signal reduces to "low-confidence/flexible regions accumulate mutations". |
| **P6.3 SASA × frequency joint** | 3×3 = 9 cells (SASA tertiles × frequency tertiles) | Tests whether the structural-evolutionary co-occurrence pattern explains signal. |
| **P6.4 pLDDT × entropy joint** | 3×3 = 9 cells (pLDDT tertiles × entropy tertiles) | Tests whether "flexible high-entropy" regions trivially explain signal. |

Each null preserves: (a) the Layer A count per stratum, (b) the strata definitions per pathogen, (c) the score and prediction (which depend on the feature matrix, not on labels). The P1 4-core / 3-core predictions are reused unchanged.

### Comparison against P1's local-burden null

P1's `local_burden_preserving` null already stratified by `mean(freq + entropy)` in a ±5 window — that captures local evolutionary burden but NOT explicit biological structure. P6.1 (SASA), P6.2 (pLDDT), and the joint nulls add explicit structural conditioning that P1 did not have.

---

## Predeclared failure-mode branches (P6)

Per the same predeclared-branch discipline as P1 and P5.

| Outcome | Predefined response |
|---|---|
| **All four P6 nulls show 0/12 individually significant** for both methods | Algorithm 1's signal is fully reducible to local biological patterns. Reframe in ch4/ch5 explicitly; reduce the descriptive callable set claim if no pathogen survives. |
| **1–4 pathogens individually significant** under any P6 null | Honest disclosure: signal partially survives biological-realistic nulls in this subset; report identities. |
| **5+ pathogens individually significant** under at least one P6 null | Signal is not fully reducible to obvious biological strata; preserve current callable-subset framing. |
| **Norovirus survives ALL four P6 nulls at p<0.05** | Strongly defensible: Norovirus signal is structurally non-trivial; the dissertation's Tier 1 cold-start claim is bounded but real. |
| **Norovirus fails all four P6 nulls** | Surprising; the dissertation's strongest signal becomes a candidate for "the most clustering-explicable case" rather than the strongest. Re-examine v176 Norovirus VP1 layer-A construction. |
| **D-stratum collapse for any pathogen** (e.g., MERS has too few positives in some cells of the 9-cell joint null) | Skip that pathogen for that null type and report it as a no-result; do not impute. |

---

## File Structure

**New scripts (created in `scripts/`):**
- `codex_p6_biological_nulls.py` — implements all 4 P6 null types using the same batched-numpy MCC framework as P1

**New result subdir:** `results/mutbench/codex_wave3/`
- `p6_null_per_pathogen.csv` — 12 × 4 × 2 × 4 = 384 rows (pathogen × null × method × metric)
- `p6_null_summary.csv` — Stouffer-aggregated global p across 12
- `p6_null_distribution.png` — 12-pathogen facet, 4-core MCC null histograms + observed marker
- `p6_p1_p6_gradient.csv` — combined P1 (4 nulls) + P6 (4 nulls) per-pathogen significance table for the unified gradient figure
- `p6_p1_p6_gradient.png` — single figure showing the per-pathogen significance gradient across all 8 nulls (P1 iid → circular → block → local-burden → P6 SASA → pLDDT → SASA×freq → pLDDT×ent)

**Documentation updates:**
- `NOTES.md` — bullets per task
- `paper/dissertation/review/2026-04-30/wave3/p6_biological_nulls.md` — per-task standalone report
- `paper/dissertation/chapters_en/ch4_results.tex` — extend `para:null_calibration` with a new sub-block, OR add `\paragraph{Biologically-realistic null calibration (P6).}` right after it (decision in Task 4 based on result strength)
- `paper/dissertation/chapters_en/ch5_discussion.tex` — extend `para:wave1_codex_audits` to cite P6 as additional confirmation
- `~/.claude/projects/-proj-paper/memory/codex_wave3_results.md` (new) — Wave 3 outcome row

---

## Task 1: Wave 3 scaffold + plan commit

**Files:**
- Create: `results/mutbench/codex_wave3/README.md`
- Create: `paper/dissertation/review/2026-04-30/wave3/` (empty dir)

- [ ] **Step 1: Create directories**

```bash
mkdir -p /proj/paper/results/mutbench/codex_wave3 /proj/paper/paper/dissertation/review/2026-04-30/wave3
```

- [ ] **Step 2: Write README**

```markdown
# Codex Wave 3 Results — P6 Biological-Realistic Local Nulls

- **Spec:** codex P1 hard-stop consultation §4, codex_full_rigor_experiment_slate Tier 2 P5, codex Wave 2 review §Q7
- **Plan:** docs/plans/2026-04-30-wave3-p6-biological-nulls.md
- **Started:** 2026-04-30
- **Wave 1 + Wave 2 outcome:** Algorithm 1 has descriptive signal on 5 callable pathogens; pre-registered abstention rule yields 0/12 callable; defense bounded.

## Null types

| Tag | Stratification | Rationale |
|---|---|---|
| P6.1 SASA-stratified | 5 SASA quintiles | "surface-exposed positions" reducibility |
| P6.2 pLDDT-stratified | 5 pLDDT quintiles | "flexible regions" reducibility |
| P6.3 SASA × freq joint | 3×3 cells | structural-evolutionary co-occurrence |
| P6.4 pLDDT × ent joint | 3×3 cells | flexible-high-entropy reducibility |

## Status

- [x] Task 1 — Scaffold (this README)
- [ ] Task 2 — P6 implementation (4 null types × 100k perms)
- [ ] Task 3 — Per-task report + P1+P6 unified gradient figure
- [ ] Task 4 — Ch4 + Ch5 prose insertion
- [ ] Task 5 — Memory + closure

Updated as tasks complete.
```

- [ ] **Step 3: NOTES.md append**

```markdown
- Wave 3 (P6 biological-realistic local nulls) execution started. Plan: `docs/plans/2026-04-30-wave3-p6-biological-nulls.md`. Subdirs: `results/mutbench/codex_wave3/`, `paper/dissertation/review/2026-04-30/wave3/`. Builds on P1 infrastructure (`scripts/codex_p1_null_calibration.py`); 4 new biological null types stratifying by SASA/pLDDT and their joint cells.
```

- [ ] **Step 4: Commit**

```bash
git -C /proj/paper add docs/plans/2026-04-30-wave3-p6-biological-nulls.md results/mutbench/codex_wave3/README.md NOTES.md && \
git -C /proj/paper commit -m "plan: v192 — Wave 3 P6 biological-realistic local nulls scaffold"
```

---

## Task 2: P6 implementation (4 null types × 100k perms)

**Files:**
- Create: `scripts/codex_p6_biological_nulls.py`
- Output: `results/mutbench/codex_wave3/p6_null_per_pathogen.csv`, `p6_null_summary.csv`, `p6_null_distribution.png`

- [ ] **Step 1: Write the script**

The script reuses P1's vectorized batched-numpy MCC, ±10-window MCC, top-20 precision, and enrichment helpers verbatim (import or duplicate from `codex_p1_null_calibration.py`). Adds four new shuffle functions:

```python
"""P6: biological-realistic local nulls — 4 new null types extending P1.

Reuses everything from codex_p1_null_calibration.py except the
shuffling primitives. Same 100k-perm budget, same 4 metrics
(MCC@top-10%, +/-10-window MCC, top-20 precision, enrichment),
same one-sided primary p + Stouffer aggregation, same per-pathogen
+ summary CSVs, same multiprocessing pool.

NEW shuffle functions:
  shuffle_sasa_stratified(y, sasa_quintiles, n_perm, rng):
      labels shuffled within each of 5 SASA quintile cells.
  shuffle_plddt_stratified(y, plddt_quintiles, n_perm, rng):
      labels shuffled within each of 5 pLDDT quintile cells.
  shuffle_joint(y, strata_2d, n_perm, rng):
      labels shuffled within each cell of a 2D stratification (e.g.,
      3 SASA tertiles x 3 frequency tertiles = 9 cells, or
      3 pLDDT tertiles x 3 entropy tertiles).

Strata computed per pathogen from feature_matrix_*.csv columns.
Cells with <2 positions or 0 positives are flagged and omitted from
the shuffle for that perm (no imputation).

Outputs (under results/mutbench/codex_wave3/):
  p6_null_per_pathogen.csv  (12 × 4 × 2 × 4 = 384 rows)
  p6_null_summary.csv       (Stouffer-aggregated)
  p6_null_distribution.png  (12-facet histograms)
"""
# Implementation: ~250 lines. Sign-fitting, score, prediction, MCC
# helpers reused from codex_p1_null_calibration.py via import or copy.
# Stratum-shuffle replaces shuffle_iid / shuffle_block for each null.
# Random seed 42. Multiprocessing via Pool(16).
```

(Full implementation written when this task executes.)

- [ ] **Step 2: Smoke test on Dengue 1k perms**

```bash
cd /proj/paper && python scripts/codex_p6_biological_nulls.py --pathogen Dengue --smoke 2>&1 | tail -25
```

Expected: <1 min, 4 nulls × 1000 perms × Dengue × 2 methods = 8000 MCC evals; prints per-null one-sided p; no exceptions.

- [ ] **Step 3: Full run**

```bash
cd /proj/paper && python scripts/codex_p6_biological_nulls.py --n-perm 100000 --workers 16 2>&1 | tee results/mutbench/codex_wave3/p6_run.log | tail -40
```

Expected: ~5–10 min (16 workers, 96 jobs); 96 rows of (pathogen, null, method, metric) summaries.

- [ ] **Step 4: Sanity-check**

```bash
python -c "
import pandas as pd
df = pd.read_csv('results/mutbench/codex_wave3/p6_null_per_pathogen.csv')
print('=== 4-core MCC: per-pathogen one-sided p across 4 P6 nulls ===')
sub = df[(df['method']=='4-core') & (df['metric']=='mcc')].copy()
piv = sub.pivot_table(index='pathogen', columns='null_type', values='p_one_sided_primary')
piv['observed'] = sub.groupby('pathogen')['observed'].first()
print(piv.sort_values('observed', ascending=False).to_string())
"
```

Verify: Norovirus should remain strongly significant (was p<1e-5 under P1 iid). If Norovirus fails ALL FOUR P6 nulls, surface immediately — that triggers a strong predeclared failure-mode branch.

- [ ] **Step 5: Document**

Append NOTES.md:
```markdown
- P6 biological nulls (2026-04-30): SASA p=___, pLDDT p=___, SASA×freq p=___, pLDDT×ent p=___ for Norovirus 4-core. Per-pathogen counts at p<0.05 under each null: SASA N/12, pLDDT M/12, joint K/12, joint L/12. See `paper/dissertation/review/2026-04-30/wave3/p6_biological_nulls.md`.
```

Write standalone report `paper/dissertation/review/2026-04-30/wave3/p6_biological_nulls.md` (~2 pages: command, inputs, primary outcomes, per-pathogen significance table, branch outcome from failure-mode table, comparison against P1's 4 nulls).

- [ ] **Step 6: Commit**

```bash
git -C /proj/paper add scripts/codex_p6_biological_nulls.py results/mutbench/codex_wave3/p6_*.csv results/mutbench/codex_wave3/p6_*.png results/mutbench/codex_wave3/p6_run.log paper/dissertation/review/2026-04-30/wave3/p6_biological_nulls.md NOTES.md && \
git -C /proj/paper commit -m "feat: v193 — Wave 3 P6 biological-realistic local nulls (4 new null types)"
```

- [ ] **Step 7: CHECKPOINT** — Apply matching failure-mode branch. If "all four P6 nulls show 0/12 individually significant" for both methods, stop and notify user before Task 4 prose; the descriptive callable set claim must be reconsidered.

---

## Task 3: P1 + P6 unified gradient figure + report

**Files:**
- Create: `results/mutbench/codex_wave3/p6_p1_p6_gradient.csv`, `p6_p1_p6_gradient.png`

- [ ] **Step 1: Combine P1 and P6 per-pathogen one-sided p values**

```python
"""Build a unified per-pathogen significance gradient table:
8 columns (P1 iid → P1 circular → P1 protein-block → P1 local-burden →
           P6 SASA → P6 pLDDT → P6 SASA×freq → P6 pLDDT×ent)
12 rows × 2 methods = 24 row groups
For each cell: one-sided p value (or asterisk if p<0.05).
"""
```

- [ ] **Step 2: Plot gradient figure**

12-facet figure (one panel per pathogen), x-axis = 8 nulls in increasing strictness, y-axis = -log10(one-sided p). Highlight p<0.05 threshold line. Color: 4-core (red), 3-core (blue).

- [ ] **Step 3: Append gradient summary to wave3 report**

Add a "P1+P6 unified gradient" section to `paper/dissertation/review/2026-04-30/wave3/p6_biological_nulls.md`. Cite the 8-null gradient: how many pathogens individually significant at each null tier?

- [ ] **Step 4: Commit**

```bash
git -C /proj/paper add results/mutbench/codex_wave3/p6_p1_p6_gradient.csv results/mutbench/codex_wave3/p6_p1_p6_gradient.png paper/dissertation/review/2026-04-30/wave3/p6_biological_nulls.md NOTES.md && \
git -C /proj/paper commit -m "feat: v194 — P1+P6 unified per-pathogen significance gradient (8 nulls)"
```

---

## Task 4: Ch4 + Ch5 prose insertion

**Files:**
- Modify: `paper/dissertation/chapters_en/ch4_results.tex` (extend `para:null_calibration` with P6 sub-block, OR add `\paragraph{Biologically-realistic null calibration (P6).}` immediately after it)
- Modify: `paper/dissertation/chapters_en/ch5_discussion.tex` (extend `para:wave1_codex_audits` to cite P6)

- [ ] **Step 1: Insert ch4 paragraph**

Insert `\paragraph{Biologically-realistic null calibration (P6).}` right after `\label{para:null_calibration}` block (i.e., before `\paragraph{Pre-registered callability and abstention rule (P5).}`). ~150 words. Cite:
- 4 new null types (SASA quintile, pLDDT quintile, SASA×freq joint, pLDDT×ent joint)
- 100k perms each, same MCC + window-MCC + precision + enrichment metrics
- Per-pathogen significance counts (n_sig at each null type)
- Norovirus survival across all four (or not)
- Headline conclusion: signal is/is not reducible to local biological patterns

- [ ] **Step 2: Extend ch5 limitations summary paragraph**

Add a sentence to `para:wave1_codex_audits` (in `sec:limitations`): "P6 biologically-realistic local nulls (Paragraph~\ref{para:p6_biological_nulls}) further bound the signal: under SASA-stratified, pLDDT-stratified, and joint structural-evolutionary nulls, ___ of 12 pathogens retain individual significance for the 4-core MCC, with Norovirus ___ surviving all four nulls."

- [ ] **Step 3: Build PDF**

```bash
cd /proj/paper/paper/dissertation && bash build.sh 2>&1 | tail -10
```

Expected: 0 errors, page count 232 → ~234, no undefined refs.

- [ ] **Step 4: Commit**

```bash
git -C /proj/paper add paper/dissertation/chapters_en/ch4_results.tex paper/dissertation/chapters_en/ch5_discussion.tex paper/dissertation/thesis_en.pdf && \
git -C /proj/paper commit -m "fix: v195 — Wave 3 P6 prose insertion (ch4 + ch5 limitations extension)"
```

---

## Task 5: Memory + closure commit

- [ ] **Step 1: Write `codex_wave3_results.md` memory**

```markdown
---
name: Codex Wave 3 Results
description: P6 biological-realistic local nulls outcomes (2026-04-30); ___ of 12 pathogens retain significance under structural-evolutionary nulls; defense ___
type: project
---

[per-pathogen significance counts under each P6 null + headline + Wave 4+ priorities]
```

Append the row to MEMORY.md index.

- [ ] **Step 2: Optional codex follow-up consultation**

If Norovirus fails all four P6 nulls, draft `codex_p6_followup_consultation_prompt.md` and consult before closure. Otherwise proceed.

- [ ] **Step 3: Final NOTES.md closure entry**

```markdown
- Wave 3 closure (2026-04-30 or later): P6 done v192-v196. Memory written. Wave 4+ reserved for Tier 2 features-only LOPO (n≈30), pilot 3 Layer A curation, EVE/PLM site-effect.
```

- [ ] **Step 4: Commit**

```bash
git -C /proj/paper add NOTES.md && \
git -C /proj/paper commit -m "docs: v196 — Wave 3 P6 closure"
```

---

## Self-review checklist

- ✅ All 4 P6 null types specified with operational stratification (SASA, pLDDT, joint cells)
- ✅ Predeclared failure-mode branches at top of plan (covering 0/12, 1-4/12, 5+/12, Norovirus survival cases)
- ✅ Strata computed per pathogen from existing feature_matrix CSVs (no new data)
- ✅ Reuse P1 vectorized MCC, window-MCC, top-K precision, enrichment helpers
- ✅ Per-task standalone reports under `wave3/`
- ✅ Memory written ONLY at Wave 3 closure
- ✅ Out-of-scope explicitly listed (Wave 4+ for Tier 2 LOPO, pilot 3 curation, EVE)
- ⚠️ P6 implementation (~250 lines) is sketched, not full code — written when Task 2 executes
- ⚠️ Joint-null cells with too few positives will be flagged + skipped (not imputed) — exact behavior verified at Task 2

## Codex consultation step (before Task 2)

This plan should be reviewed by codex BEFORE Task 2 executes, matching the v181a / v187a pattern. Prompt at `paper/dissertation/review/2026-04-30/codex_wave3_plan_review_prompt.md`. If codex returns "PROCEED WITH MODIFICATIONS", incorporate edits. If "REVISE BEFORE PROCEED", iterate.
