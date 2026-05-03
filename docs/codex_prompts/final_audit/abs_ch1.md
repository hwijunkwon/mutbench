# Final Audit — Chapter-Deep Pre-Defense Check

Execute the audit NOW. Read-only. Do not commit. Do not ask for confirmation.

## Scope

`paper/dissertation/front_en/abstract.tex + paper/dissertation/chapters_en/ch1_introduction.tex` (~17 pp) on `master` v227 (197pp post-triage-reframe).

## Recent state

- 215pp -> 197pp (-18pp via 6-step risk-managed compression)
- Wet-lab triage repositioning (deployment refused; Layer C 6/11 pathogens elevated as primary practical-value anchor)
- ANOVA 5-frame narrative restored (Cameron 2008 wild-cluster justification)
- Phase 4 Prof v8 (2-stage hybrid): 83.63/100 PASS

## Mandatory checks (verify EACH item; flag any deviation)

### A. Numerical consistency

Verify every numerical claim in scope against authoritative sources:
- `results/mutbench/stage3_full_results.csv` (8580 rows)
- `results/mutbench/stage3_statistics.csv` (Friedman, omega^2, LOPO)
- `results/mutbench/cluster_bootstrap_omega_summary.csv` ([0.201, 0.346])
- `results/mutbench/omega_robustness_5way.csv` (5-frame)
- `results/mutbench/vaccine_escape_stage3.csv` (HIV-1 7.19x, H3N2 9.36x, SARS 7.63x)
- `results/mutbench/escape_validation_adapt.csv` (top-5 fixed protocol)
- `results/mutbench/layer_c_evaluation.csv` (Layer C 6 pathogens)
- `results/mutbench/feature_analysis/feature_ablation_nested_lopo_summary.csv` (4-core 0.0809 vs full-10 0.0698)
- `results/mutbench/codex_wave1/p1_null_per_pathogen.csv` (P1 6/12)
- `results/mutbench/codex_wave1/p2_decision_curve.csv` (random 41 at budget 50)
- `results/mutbench/codex_wave1/p3_full_lattice_1023.csv` (4-core rank 87)
- `results/mutbench/codex_wave2/p5_callable_decisions.csv` (0/12 callable)
- `results/mutbench/codex_wave3/p6_null_summary.csv` (4 nulls)
- `results/mutbench/codex_wave4/w4_labeled_lopo_summary.csv` (8/12 positive p=0.368)
- `results/mutbench/codex_layerA_prime/lopo_summary.csv` (W5 -0.055)
- `results/mutbench/adaptive_weighting_comparison.csv` (Cycle 7B p=0.56)
- `results/mutbench/hbfws_lopo_results.csv` (HBFWS p=0.78)

### B. Citation integrity

For every `\cite{key}` in scope:
- Confirm `key` exists in `paper/dissertation/references.bib`
- Flag any `\cite{key}` that fails to resolve

### C. Cross-reference integrity

For every `\ref{key}` in scope:
- Confirm `\label{key}` exists somewhere in active build (front_en, ch1-ch5)
- Flag any `\ref` that points to wrong target

### D. Triage framing consistency

Check the chapter for stray wording inconsistent with the wet-lab triage reframe:
- Any `deployable` / `deployment` / `operational` / `prospective detector` claims WITHOUT scope qualifier ("at n=11, under tested regime" or "retrospective triage only")?
- Any "20-30+ pathogens will suffice" / "phase transition" overstrong claim?
- Any LOPO 0/11 standalone (must be paired with omega^2 0.296 + Friedman + adaptive failures)?
- Any "Algorithm 1 is a calibrated detector" claim (must be "retrospective triage heuristic")?

### E. Layer C / HIV-1 anchor consistency

- Layer C: 6 pathogens (SARS-CoV-2 247, H3N2 112, HIV-1 48, RSV 101, Rabies 87, EV-A71 55), best MCC range 0.139-0.322 — appears correctly cited?
- HIV-1 vaccine escape: 7.19x, p_adj=2.5e-16, 82% Layer-A-disjoint, 37 of 45 novel — appears correctly cited?

### F. Compression-specific regression check

Did the 18pp compression accidentally remove any load-bearing claim? Specifically:
- Does the chapter still cite Bolker rule-of-thumb appropriately (design target, NOT phase transition)?
- Does the chapter still pair "not learnable" with "at n=11"?
- Did any equation, table, or figure reference get orphaned?

## Output

`paper/dissertation/review/2026-05-03/final_audit_stage1_abs_ch1.md`

Structure:

```
# Final Audit Stage 1: abstract+ch1

## A. Numerical consistency
{per-claim verification}

## B. Citation integrity
{cite key audit}

## C. Cross-reference integrity
{ref/label audit}

## D. Triage framing consistency
{deployable/operational keyword audit}

## E. Layer C / HIV-1 anchor
{anchor consistency check}

## F. Compression regression check
{load-bearing claim retention}

## Issue list
- Critical: ...
- Major: ...
- Minor: ...

RESULT_FINAL_AUDIT_STAGE1_abs_ch1: critical=<n> major=<n> minor=<n> framing_inconsistencies=<n> orphan_refs=<n>
```

Length budget: <= 2500 words.
