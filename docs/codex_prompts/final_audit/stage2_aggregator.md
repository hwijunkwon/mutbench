# Final Audit Stage 2 — Cross-Cutting Consistency Aggregator

Execute the audit NOW. Read-only. Do not commit. Do not ask for confirmation.

You are the **cross-cutting consistency aggregator** for the pre-defense final audit on master v227 (197pp post-triage-reframe).

## Task

1. Read all 5 Stage 1 chapter audit reports:
   - `paper/dissertation/review/2026-05-03/final_audit_stage1_abs_ch1.md`
   - `paper/dissertation/review/2026-05-03/final_audit_stage1_ch2.md`
   - `paper/dissertation/review/2026-05-03/final_audit_stage1_ch3.md`
   - `paper/dissertation/review/2026-05-03/final_audit_stage1_ch4.md`
   - `paper/dissertation/review/2026-05-03/final_audit_stage1_ch5.md`

2. Cross-chapter numerical consistency: verify EACH key anchor appears with the SAME value across all chapters where it occurs.

   Key anchors to track:
   - omega^2 = 0.296 (cluster-bootstrap CI [0.201, 0.346])
   - 5-frame omega CIs: standard [0.201, 0.346], wild [0.201, 0.303], phylo block [0.202, 0.346], mixed-effects 0.340 lower 0.188, Bayesian HDI [0.242, 0.388]
   - Friedman chi^2 = 7.69, p = 0.990
   - LOPO 0/11
   - HIV-1 vaccine escape: 7.19x, p_adj=2.5e-16, 82% Layer-A-disjoint, 37 of 45 novel
   - H3N2: 9.36x; SARS-CoV-2: 7.63x exploratory
   - HBFWS p = 0.78
   - Cycle 7B 6 paradigms, smallest p = 0.56
   - Wave 4: 8/12 positive, p = 0.368
   - Wave 5 Layer A': mean MCC = -0.055
   - 4-core: MCC 0.0809 vs full-10 0.0698, paired delta +0.011, p = 0.61
   - Subset rank 13/210, full lattice 87/1023, 3-core rank 27
   - P1 null: 6/12 (iid/circular), 4/12 (block), 7/12 (local-burden)
   - P2 decision curve: random 41 at budget 50; 4-core 66, 3-core 68
   - P5 0/12 callable
   - P6 nulls: 5/12 (sasa, plddt), 4/12 (joint)
   - Layer C 6 pathogens (SARS 247, H3N2 112, HIV-1 48, RSV 101, Rabies 87, EV-A71 55), best MCC range 0.139-0.322

3. Bibliography orphan analysis:
   - Open `paper/dissertation/references.bib`, list all bib entry keys
   - Search active build (front_en/abstract.tex, chapters_en/ch1-ch5) for `\cite{...}` usage
   - Identify: (a) bib keys defined but never cited; (b) `\cite{}` keys cited but missing from bib

4. Triage framing global verdict:
   - Aggregate Stage 1 D-section findings
   - Final list of remaining "deployable/operational/phase-transition" stragglers if any
   - Verdict: framing CONSISTENT / NEEDS_FIX

5. Cross-reference orphan check:
   - Aggregate Stage 1 C-section findings
   - List any `\label{}` defined but never referenced
   - List any `\ref{}` to a non-existent label

6. Defense readiness checklist:
   - Phase 4 gate: PASS (83.63)
   - Numerical consistency: PASS / FAIL
   - Citation integrity: PASS / FAIL
   - Triage framing: PASS / FAIL
   - Defense readiness: GREEN / YELLOW / RED

## Output

`paper/dissertation/review/2026-05-03/final_audit_aggregate.md`

Structure:

```
# Final Audit Aggregate (master v227, 197pp)

## 1. Stage 1 summary
{per-chapter critical/major/minor counts}

## 2. Cross-chapter numerical consistency
{table: anchor | ch where appears | values | match status}

## 3. Bibliography orphan analysis
{lists of orphan bib keys + missing cite keys}

## 4. Triage framing global verdict
{aggregated D-section findings + verdict}

## 5. Cross-reference orphans
{aggregated C-section findings}

## 6. Defense readiness checklist
{green/yellow/red verdict per category + overall}

## 7. Recommended fixes
{prioritized fix list if any issues found}

RESULT_FINAL_AUDIT_AGGREGATE: critical=<n> major=<n> minor=<n> consistency=<PASS|FAIL> citation=<PASS|FAIL> framing=<PASS|FAIL> defense_readiness=<GREEN|YELLOW|RED>
```

Length budget: <= 3000 words.
