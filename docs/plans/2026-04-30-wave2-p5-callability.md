# Wave 2 P5 — Callability / Abstention Rule Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement task-by-task.

**Goal:** Pre-register and execute the P5 callability/abstention rule specified in `codex_p1_hardstop_consultation.md` §3. For each LOPO fold, decide whether Algorithm~1 (3-core primary, 4-core secondary) is "callable" on the held-out pathogen using ONLY training-fold information, then evaluate Algorithm~1 strictly on the callable subset. Abstentions count as no-deployment, not as failures.

**Architecture:** Reuse the Wave 1 sign-fitting + nested LOPO machinery. Add four diagnostics computed on the 11-pathogen training set per fold + a sparse-label red flag on the held-out + an inversion guardrail. Default thresholds are fixed per codex's spec; an inner LOO sensitivity sweep stress-tests them. Results land in `results/mutbench/codex_wave2/p5_*` and feed a single new `\subsubsection` in ch4_results.tex.

**Tech Stack:** Python 3, numpy, pandas, scipy, sklearn (already installed). No GPU. Compute budget: ~1 CPU-hour total (10k iid perms × 11 training pathogens × 12 outer folds × 2 methods + 200 perturbations × 11 × 12 × 2).

**Documentation cadence:** Each task ends with a NOTES.md bullet, a per-task standalone Markdown report under `paper/dissertation/review/2026-04-30/wave2/p5_*.md`, and a git commit (v187+).

**Spec source:** `paper/dissertation/review/2026-04-30/codex_p1_hardstop_consultation.md` §3 + §4

**Codex review of plan:** PENDING (this plan file is consulted before execution).

**Out of scope (Wave 3 plans):** P6 biological-realistic local nulls (extends P1), Tier 2 features-only LOPO at n=30, Tier 3 EVE/PLM site-effect, pilot 3 Layer A literature curation.

---

## Pre-registered Decision Rule (per codex §3)

A fold (held-out pathogen) is **callable** for a candidate method (3-core primary, 4-core secondary) if **all four** diagnostics pass AND the inversion guardrail holds.

### Diagnostics (computed on the 11 training pathogens of the fold)

| Tag | Operational definition | Default threshold |
|---|---|---|
| **D1: top-decile separation** | For each training pathogen, top-decile minus bottom-decile Layer A prevalence with 1{,}000-resample bootstrap CI. Method passes if **the lower CI bound > 0.02 AND the point estimate > 0.05** for ≥7/11 training pathogens. (Inner LOO sweep tests sensitivity to the 7/11 quorum.) | lower CI > 0.02; point > 0.05; quorum ≥ 7/11 |
| **D2: null-adjusted enrichment** | For each training pathogen, observed top-decile enrichment ÷ mean null top-decile enrichment under 10{,}000 iid prevalence-preserving permutations. 1{,}000-resample bootstrap over training pathogens of this ratio. Method passes if **lower 95% bootstrap bound > 1.10**. | bootstrap lower > 1.10 |
| **D3: perturbation stability** | For each training pathogen, 200 perturbations: (a) jitter feature z-scores by per-feature SD × 0.10 as a **fixed stability stress perturbation** (replace with empirical measurement variance only if available before execution; we do not have such estimates so the stress magnitude is treated as predeclared), (b) re-fit signs on bootstrap of training pathogens. **Both** components are applied jointly per perturbation to capture rank and sign uncertainty. Compute Jaccard overlap of top-10% callsets across pairs of perturbations. Method passes if **median Jaccard ≥ 0.60 AND 10th percentile ≥ 0.40** aggregated over the 11 training pathogens. | median ≥ 0.60; 10th pct ≥ 0.40 |
| **D4: sparse-label red flag (held-out annotation-density metadata only)** | The held-out pathogen has at least **10 Layer A positives**, at least **200 rankable positions**, and Layer A prevalence between **1% and 20%**. **Uses only held-out annotation-density metadata: positive count, rankable-site count, and prevalence; no held-out scores, ranks, MCC, enrichment, or p-values.** | ≥10 pos, ≥200 pos, prev ∈ [1%, 20%] |

### Inversion guardrail (per-method)

For the 11 training pathogens, compute top-vs-bottom decile delta + bootstrap 95% CI per pathogen and median Spearman ρ across decile prevalence. **If ≥2 training pathogens have CI upper bound < 0 OR median Spearman ρ ≤ 0**, the candidate method is **not callable for this fold-method pair** regardless of D1–D4. The guardrail is applied separately to 3-core and 4-core (a 3-core rule is not forced to abstain merely because the historical 4-core inverts on the same fold). **Also record an interpretive `any_method_inversion` flag for the fold** (1 if either method fired the guardrail) for analysis only — this flag does NOT affect callability.

### Endpoints

- **Primary:** mean MCC and **sum TP@budget=50** on callable held-out pathogens, with the count and identity of abstained pathogens reported in the same table.
- **Secondary:**
  - Decision curves at budgets {**TP@20, TP@50, TP@80**} on callable pathogens (TP@50 primary; TP@20 and TP@80 show whether the conclusion depends on one arbitrary review budget).
  - Coverage-performance tradeoff — callable fraction (n_callable / 12), MCC on callable, TP@{20,50,80} on callable.
  - **Policy baseline (not a competing model):** "always-deploy on all 12 + random allocation on abstained" — labelled clearly as a deployment policy comparison, not as model evidence.
  - **Per-pathogen abstention reason** (which of D1, D2, D3, D4, inversion failed) reported in the per-pathogen CSV.

---

## File Structure

**New scripts (created in `scripts/`):**
- `codex_p5_callability.py` — implements all four diagnostics + inversion guardrail + outer LOPO + endpoint reporting
- `codex_p5_inner_loo_sweep.py` — sensitivity sweep over the D1 quorum (5/11, 6/11, 7/11, 8/11) and D2 lower-bound (1.05, 1.10, 1.20, 1.50) using inner LOO

**New result subdir (created):** `results/mutbench/codex_wave2/`
- `p5_diagnostics_per_fold.csv` — 12 folds × 2 methods × 4 diagnostics + guardrail (24 rows × ~20 columns)
- `p5_callable_decisions.csv` — 24 rows: pathogen, method, **d1_pass, d2_pass, d3_pass, d4_pass, inversion_pass** (boolean), **d1_fail, d2_fail, d3_fail, d4_fail, inversion_fail** (boolean negations for clarity), **abstention_reason** (compact string listing failed criteria), callable status, observed MCC, observed_tp20, observed_tp50, observed_tp80, **any_method_inversion** (interpretive flag)
- `p5_endpoint_summary.csv` — primary + secondary endpoints per method
- `p5_inner_loo_sweep.csv` — sensitivity sweep (rows: quorum × lower-bound × method, columns: callable count, mean MCC, etc.)
- `p5_callable_subset.png` — figure: per-fold diagnostic bars + callable status

**Documentation updates:**
- `NOTES.md` — bullets per task
- `paper/dissertation/review/2026-04-30/wave2/p5_callability.md` — per-task standalone report
- `paper/dissertation/chapters_en/ch4_results.tex` — single new `\paragraph{Prospective callability rule}` insertion (placed after the existing `para:null_calibration` block)
- `paper/dissertation/chapters_en/ch5_discussion.tex` — Future Work "Prospective Callability and Abstention Rule" paragraph upgraded from "this is the protocol" to "this is the result"
- `~/.claude/projects/-proj-paper/memory/codex_wave1_results.md` — append Wave 2 outcome row (single line)
- New plan file `docs/plans/2026-04-30-wave3-expanded-panel.md` (if user proceeds to Wave 3)

---

## Predeclared failure-mode branches (P5)

These are fixed BEFORE the P5 results exist. Prose in the new ch4 paragraph follows the matching branch.

| Outcome | Predefined response |
|---|---|
| **0/12 callable** | Algorithm 1 is not deployable on this panel under the pre-registered rule. Report this as the headline; preserve the descriptive role of P1/P2/P3. Move to Wave 3 (expanded panel) immediately. |
| **1–4/12 callable** | Report the callable subset, mean MCC + TP@50 on callable. Abstain on the rest. Do NOT generalise. |
| **5–9/12 callable** | This is the expected range given P1's 5/12 iid significance. Report callable performance + coverage tradeoff. State that the rule is operationally meaningful but not universal. |
| **10–12/12 callable** | Surprising; revisit thresholds for hidden over-permissiveness. Compare against the inversion guardrail and the inner LOO sweep before declaring success. |
| **Inversion guardrail fires for ≥1 fold** | Report which fold(s); if Rabies is the held-out pathogen of an inversion-guardrail-fired fold, this is a confirmation of the P2 finding. |

---

## Task 1: Wave 2 scaffold + Wave 1 codex consultation closure

**Why:** Establishes Wave 2 result subdir + per-task report dir, re-uses the Wave 1 README pattern.

**Files:**
- Create: `results/mutbench/codex_wave2/README.md`
- Create: `paper/dissertation/review/2026-04-30/wave2/` (empty dir)

- [ ] **Step 1: Create directories**

```bash
mkdir -p /proj/paper/results/mutbench/codex_wave2 /proj/paper/paper/dissertation/review/2026-04-30/wave2
```

- [ ] **Step 2: Write README**

```markdown
# Codex Wave 2 Results — P5 Callability / Abstention Rule

- **Spec:** `paper/dissertation/review/2026-04-30/codex_p1_hardstop_consultation.md` §3 (4 pre-registered diagnostics + inversion guardrail)
- **Plan:** `docs/plans/2026-04-30-wave2-p5-callability.md`
- **Started:** 2026-04-30
- **Wave 1 outcome:** P1+P2+P3 done v182-v185; HARD STOP triggered for Algorithm 1 global claim; P5 is the codex-specified next experiment.

## Diagnostics per fold (training-fold-only; no held-out leakage)

| Tag | Threshold |
|---|---|
| D1 top-decile separation | lower CI > 0.02, point > 0.05, ≥7/11 quorum |
| D2 null-adjusted enrichment | bootstrap lower > 1.10 |
| D3 perturbation stability | median Jaccard ≥ 0.60, 10th pct ≥ 0.40 |
| D4 sparse-label red flag | ≥10 pos, ≥200 pos, prev 1-20% |
| Inversion guardrail | not callable if ≥2 training pathogens have CI upper < 0 OR median ρ ≤ 0 |

## Endpoints

Primary: mean MCC + sum TP@50 on callable held-out pathogens.
Secondary: callable fraction + coverage-performance tradeoff.

## Status

- [ ] Task 1 — Scaffold
- [ ] Task 2 — Implement P5 (codex_p5_callability.py)
- [ ] Task 3 — Sensitivity sweep (codex_p5_inner_loo_sweep.py)
- [ ] Task 4 — Ch4 prose insertion
- [ ] Task 5 — Memory + closure commit
```

- [ ] **Step 3: NOTES.md append**

```markdown
- Wave 2 (P5 callability) execution started. Plan: `docs/plans/2026-04-30-wave2-p5-callability.md`. Subdirs: `results/mutbench/codex_wave2/` and `paper/dissertation/review/2026-04-30/wave2/`.
```

- [ ] **Step 4: Commit**

```bash
git -C /proj/paper add docs/plans/2026-04-30-wave2-p5-callability.md results/mutbench/codex_wave2/README.md NOTES.md && \
git -C /proj/paper commit -m "plan: v187 — Wave 2 P5 callability plan + scaffold"
```

---

## Task 2: Implement P5 (full diagnostic suite + outer LOPO + endpoints)

**Files:**
- Create: `scripts/codex_p5_callability.py`
- Output: `results/mutbench/codex_wave2/p5_diagnostics_per_fold.csv`, `p5_callable_decisions.csv`, `p5_endpoint_summary.csv`, `p5_callable_subset.png`

- [ ] **Step 1: Write the script**

The script reuses Wave 1 sign-fitting and scoring. Pseudocode:

```python
#!/usr/bin/env python3
"""P5: Callability / abstention rule (codex P1 hard-stop consultation §3).

For each LOPO fold (held-out p_k, training = 11 others):
  - signs = fit_signs(training, FEATURES)  # Pearson sign per feature, training only
  - For method in [3-core, 4-core]:
      - Score every position in every training pathogen and held-out (using signs)
      - D1: per training pathogen, top-bot decile delta + 1000-bootstrap CI
            (lower > 0.02 AND point > 0.05 in >=7/11)
      - D2: per training pathogen, observed top-decile enrichment / mean null
            enrichment under 10000 iid perms; 1000-bootstrap of ratio across
            11 training pathogens (lower 95% > 1.10)
      - D3: per training pathogen, 200 perturbations:
              jitter z-scores by 0.10 * per-feature SD, re-fit signs on
              random-bootstrap training pathogens; Jaccard of top-10% across
              all 200 callsets per pathogen, then aggregate over training set
              (median >= 0.60 AND 10th-percentile >= 0.40)
      - D4 (held-out only): n_pos >= 10 AND n_rankable >= 200 AND
            prev in [0.01, 0.20]
      - Inversion guardrail: count of training pathogens with bootstrap
            CI upper < 0; median Spearman trend across training (>=2 with
            upper<0 OR median <= 0 -> not callable)
      - Callable = D1 AND D2 AND D3 AND D4 AND NOT(inversion)
      - If callable: deploy method on held-out; record observed MCC,
            TP@20, TP@50, TP@80 (decision curve at three budgets), and
            per-pathogen enrichment.
        If abstained: record D-failure cause via `abstention_reason`;
            DO NOT short-circuit early — emit ALL diagnostic component
            values even when an early criterion fails (no hidden
            short-circuit behavior).
Aggregate:
  - Primary: mean MCC + sum TP@50 on callable; identity + count on abstained.
  - Secondary: callable fraction; "always-deploy + random on abstained" baseline.

Outputs:
  results/mutbench/codex_wave2/p5_diagnostics_per_fold.csv
  results/mutbench/codex_wave2/p5_callable_decisions.csv
  results/mutbench/codex_wave2/p5_endpoint_summary.csv
  results/mutbench/codex_wave2/p5_callable_subset.png
"""
# Implementation: ~400 lines. Sign-fitting, equalweight_score, MCC/TP@K
# helpers reused verbatim from scripts/codex_p2_rank_reliability.py (no
# changes to scoring mechanics). New code is the 4 diagnostics + the
# guardrail. Random seed 42 throughout. Multiprocessing optional for
# the 200-perturbation D3 (12 folds × 11 training × 200 = 26400 callset
# computations × 2 methods; vectorisable to <5 minutes single-thread).
```

(Full implementation written when this task executes.)

- [ ] **Step 2: Smoke test on one fold**

```bash
cd /proj/paper && python scripts/codex_p5_callability.py --fold Dengue --smoke 2>&1 | tail -30
```

Expected: <1 min, prints D1/D2/D3/D4/inversion status for the Dengue fold under both methods, no exceptions.

- [ ] **Step 3: Full run**

```bash
cd /proj/paper && python scripts/codex_p5_callability.py 2>&1 | tee results/mutbench/codex_wave2/p5_run.log | tail -40
```

Expected: ~30 min wall (the 10k null perms × 11 training × 12 outer × 2 methods is the bottleneck — 2.6M MCC evals via batched numpy). 24 rows in `p5_callable_decisions.csv`.

- [ ] **Step 4: Sanity-check**

```bash
head -3 /proj/paper/results/mutbench/codex_wave2/p5_callable_decisions.csv
python -c "
import pandas as pd
df = pd.read_csv('results/mutbench/codex_wave2/p5_callable_decisions.csv')
for m in ['3-core', '4-core']:
    sub = df[df['method'] == m]
    n_call = sub['callable'].sum()
    if n_call > 0:
        callable_subset = sub[sub['callable']]
        print(f'{m}: {n_call}/12 callable. Mean MCC={callable_subset[\"observed_mcc\"].mean():.4f}, '
              f'sum TP@50={callable_subset[\"observed_tp50\"].sum():.0f}')
        print(f'  callable: {list(callable_subset[\"pathogen\"])}')
        print(f'  abstained: {list(sub[~sub[\"callable\"]][\"pathogen\"])}')
    else:
        print(f'{m}: 0/12 callable.')
"
```

Cross-check against P1 — **qualitative implementation sanity check only; this is NOT a pass/fail criterion**. The callable set may overlap with P1's 5 iid-significant pathogens (Norovirus, Influenza_B, H3N2, HCV, Dengue), but P5 uses a different operationalisation (callability via training-set diagnostics; P1 used per-pathogen one-sided null tests). If overlap is 0/5, inspect for coding errors or diagnostic mismatch; if the implementation is correct, report the divergence transparently rather than retrofitting thresholds.

- [ ] **Step 5: Document**

Append NOTES.md:
```markdown
- P5 callability (2026-04-30): 3-core N/12 callable, 4-core M/12 callable. Mean MCC on callable: X.XXX (3-core), Y.YYY (4-core). Sum TP@50: ___ vs always-deploy random ~30. Inversion guardrail fired for ___ fold(s). See `paper/dissertation/review/2026-04-30/wave2/p5_callability.md`.
```

Write standalone report `paper/dissertation/review/2026-04-30/wave2/p5_callability.md` (~2 pages: command, inputs, primary/secondary endpoints, callable identities, abstention reasons, branch outcome from the failure-mode table).

- [ ] **Step 6: Commit**

```bash
git -C /proj/paper add scripts/codex_p5_callability.py results/mutbench/codex_wave2/p5_*.csv results/mutbench/codex_wave2/p5_*.png results/mutbench/codex_wave2/p5_run.log paper/dissertation/review/2026-04-30/wave2/p5_callability.md NOTES.md && \
git -C /proj/paper commit -m "feat: v188 — Wave 2 P5 callability/abstention rule (codex spec)"
```

- [ ] **Step 7: CHECKPOINT** — Apply the P5 failure-mode branch (top of plan) matching the observed callable count. If 0/12 callable, stop and notify user before Task 4 prose. If ≥1 callable, proceed.

---

## Task 3: Predeclared threshold sensitivity sweep (D1 quorum × D2 lower bound)

**Why:** The 4-of-4 default thresholds are predeclared. This task runs a **predeclared sensitivity sweep** (NOT inner LOO threshold selection — we do not choose stricter thresholds adaptively from inner training data) to report robustness of the callable count + MCC across reasonable threshold neighborhoods. **Per codex Wave 2 review §Q3:** D3 thresholds, D4 prevalence band, and inversion count are NOT swept (would multiply researcher degrees of freedom). Default thresholds are NOT replaced after seeing outer callable performance.

**Files:**
- Create: `scripts/codex_p5_inner_loo_sweep.py`
- Output: `results/mutbench/codex_wave2/p5_inner_loo_sweep.csv`

- [ ] **Step 1: Write the sweep script**

For (quorum ∈ {5/11, 6/11, 7/11, 8/11}) × (lower-bound ∈ {1.05, 1.10, 1.20, 1.50}) × (method ∈ {3-core, 4-core}) = 32 configurations. Each configuration re-runs the outer LOPO with the new thresholds. Record callable count, mean MCC on callable, sum TP@50, identity of callable subset.

- [ ] **Step 2: Run**

```bash
cd /proj/paper && python scripts/codex_p5_inner_loo_sweep.py 2>&1 | tee -a results/mutbench/codex_wave2/p5_run.log | tail -40
```

- [ ] **Step 3: Sanity-check**

Verify: at default (7/11, 1.10) the result matches Task 2. At looser thresholds (5/11, 1.05) the callable count grows monotonically. At stricter (8/11, 1.50) it shrinks monotonically. If non-monotone, investigate.

- [ ] **Step 4: Append report**

Add a "Sensitivity sweep" section to `wave2/p5_callability.md` with the 32-row table abstracted to: at default → N callable; at loosest → M callable; at strictest → K callable. Conclusion: rule is/is not robust to threshold choice.

- [ ] **Step 5: Commit**

```bash
git -C /proj/paper add scripts/codex_p5_inner_loo_sweep.py results/mutbench/codex_wave2/p5_inner_loo_sweep.csv paper/dissertation/review/2026-04-30/wave2/p5_callability.md NOTES.md && \
git -C /proj/paper commit -m "feat: v189 — P5 inner LOO sensitivity sweep over D1 quorum + D2 lower bound"
```

---

## Task 4: Ch4 prose insertion

**Files:**
- Modify: `paper/dissertation/chapters_en/ch4_results.tex` (insert after `para:null_calibration`)
- Modify: `paper/dissertation/chapters_en/ch5_discussion.tex` (upgrade Future Work `\textbf{Prospective Callability and Abstention Rule}` from "this is the protocol" to "this is the result")

- [ ] **Step 1: Insert ch4 paragraph**

Insert a new `\paragraph{Pre-registered callability and abstention rule.}` (~200 words) after the existing `\label{para:null_calibration}` block in ch4_results.tex. Cite:
- The 4 diagnostics + inversion guardrail with default thresholds (1 sentence each)
- N callable / 12 (under default thresholds)
- Identity of callable subset; identity of abstained subset
- Mean MCC on callable, sum TP@50 on callable, vs always-deploy baseline
- Sensitivity sweep summary (1 sentence)
- Failure-mode branch outcome (1 sentence per the table)

- [ ] **Step 2: Upgrade ch5 Future Work paragraph**

Change "Prospective Callability and Abstention Rule" subsection from a protocol-only statement to a result-statement paragraph: "The Wave 2 application of this rule yielded N callable / 12 with mean MCC X on callable. The remaining M abstained pathogens are reserved for future-work expansion to the Tier 1 pilot 3 + Tier 2 features-only n=30 panel with new Layer A annotations."

- [ ] **Step 3: Build PDF**

```bash
cd /proj/paper/paper/dissertation && bash build.sh 2>&1 | tail -10
```

Expected: 0 errors, page count 231 → ~233, no undefined refs.

- [ ] **Step 4: Commit**

```bash
git -C /proj/paper add paper/dissertation/chapters_en/ch4_results.tex paper/dissertation/chapters_en/ch5_discussion.tex paper/dissertation/thesis_en.pdf && \
git -C /proj/paper commit -m "fix: v190 — Wave 2 P5 prose insertion (ch4 + ch5 future work upgrade)"
```

---

## Task 5: Memory + closure commit

- [ ] **Step 1: Update memory**

Append a "Wave 2 outcome" row to `~/.claude/projects/-proj-paper/memory/codex_wave1_results.md` (rename it to `codex_waves_results.md` if growing too large; for now just append). Update MEMORY.md index entry's one-liner.

- [ ] **Step 2: Optional codex follow-up consultation**

If the result is unexpected (0/12 callable or >9/12 callable), draft a `codex_p5_followup_consultation_prompt.md` similar to the P1 hard-stop consultation and ask for the next-step recommendation. Otherwise proceed to closure.

- [ ] **Step 3: Final NOTES.md closure entry**

```markdown
- Wave 2 (P5) closure (2026-04-30 or later): N/12 callable for 3-core, M/12 for 4-core; sensitivity sweep robust/not robust; ch4+ch5 prose updated; PDF 231→XXX pp. v187-v191 commit chain.
```

- [ ] **Step 4: Commit**

```bash
git -C /proj/paper add NOTES.md && \
git -C /proj/paper commit -m "docs: v191 — Wave 2 P5 closure"
```

---

## Self-review checklist

- ✅ All 4 codex-specified diagnostics + inversion guardrail present with default thresholds
- ✅ Sensitivity sweep over D1 quorum and D2 lower bound (32 configs)
- ✅ No held-out information used in callable decision (D4 uses counts + length only)
- ✅ Predeclared failure-mode branches at top of plan covering 0/12, 1-4/12, 5-9/12, 10-12/12, inversion-fired cases
- ✅ Per-task standalone reports under `wave2/`
- ✅ Memory written only at Wave 2 completion (Task 5)
- ✅ Out-of-scope explicitly listed (P6 local nulls, Tier 2 LOPO, Tier 3 EVE, pilot 3 Layer A)
- ⚠️ P5 implementation (~400 lines) is sketched, not full code — written when Task 2 executes
- ⚠️ Sensitivity sweep (~150 lines) is sketched, written when Task 3 executes
- ⚠️ Cross-validation against P1's 5 iid-significant pathogens is qualitative only (no formal expected-overlap test)

## Codex consultation step (before Task 2)

This plan should be reviewed by codex BEFORE Task 2 executes, matching the v181a pattern. Prompt at `paper/dissertation/review/2026-04-30/codex_wave2_plan_review_prompt.md` (created in Task 1.5). If codex returns "PROCEED WITH MODIFICATIONS", incorporate edits and proceed. If "REVISE BEFORE PROCEED", iterate.
