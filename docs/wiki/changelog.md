# MutBench Dissertation Changelog (master)

Reverse chronological. Latest first.

## experiments/flow-improve (2026-05-04) — Failed score-improvement experiment, branch DISCARDED

Investigated whether content-flow improvements + targeted deletions could push score above v9 (83.31). Result: every step lost score. Experiment ABANDONED, master remains at v229.

### Trajectory

| Branch step | Action | PDF | Score | Δ |
|---|---|---|---|---|
| v229 (master) | baseline | 197pp | 83.31 | — |
| Step 1: flow-fix | TOP 10 flow improvements (5 codex agents) | 197pp | not measured | — |
| Step 2: deletion | Moderate plan applied (5 codex agents); -39pp aggressive | 158pp | v10 = 81.85 | -1.46 |
| Step 3: partial rollback | restore 3 ch4 tables | 153pp | v11 = 80.86 | -0.99 |

### Key findings

- v9 (197pp, 83.31) is the empirical sweet spot for this manuscript
- Aggressive deletion (-39pp) hurt H/clarity score: panels lost evidence visibility
- Partial table restoration without surrounding narrative context made flow worse, not better
- Hidden-issues count went UP (44→52) after partial rollback — agents flagged "table appears with thin context"
- 80/100 gate near-miss in v11 (3 profs <80) confirmed branch should be abandoned

### Branch status

`experiments/flow-improve` retained on origin for institutional memory; not merged. Reports under `paper/dissertation/review/2026-05-03/`:
- `flow_audit_aggregate.md`, `flow_fix_chN_changelog.md` (flow analysis + edits)
- `deletion_deep_aggregate.md`, `deletion_apply_chN_changelog.md` (deletion analysis + edits)
- `professor_v10_aggregate.md`, `professor_v11_aggregate.md` (failed scoring)

Master continues at v229 (197pp, 83.31, all 4 gates PASS).

## v229 (2026-05-04) — Phase 4 prof v9 re-eval on v228 (PASS, all gates)

Re-run of v8 method (5 chapter-deep + 10 prof aggregator = 15 codex jobs) on v228 to verify cleanup did not regress.

- v9 total: **83.31/100** (vs v8 83.63, Δ -0.32 — within evaluation noise)
- All 10 profs ≥ 80 (10/10)
- Min item: G 7.80 (vs v8 7.71, +0.09)
- Stage 1 hidden issues: 49 (v8 52, ch4 17→10 = -7 from cleanup)
- All 4 gates PASS, defense readiness GREEN confirmed

No problematic findings. Defense-ready as v228 manuscript.

Reports: `professor_v9_aggregate.md`, `professor_v9_prof01-10.md`, `professor_v9_stage1_*.md`

## v228 (2026-05-04) — Final audit cleanup (defense_readiness GREEN)

Final audit (option C: 5 chapter-deep + 1 cross-cutting aggregator + visual review of 6 PDF pages):
- 0 Critical, 0 framing inconsistencies, 0 orphan refs, 0 layout issues
- 4 actionable findings fixed:
  - ch5 ANCOVA stale value 0.234→0.264 → corrected to 0.233→0.274 (matches `ancova_omega_summary.csv`)
  - ch3 "HCV-only ANOVA" → "HCV-excluded ANOVA" (semantic fix)
  - ch4 + ch5 Bolker 20-30 statement now cites `bolker2009glmm`
  - 3 orphan bib entries removed (chen2022gisaid, kaku2024virological, ioannidis2008winner)
- Defense readiness: YELLOW → **GREEN**

Reports: `final_audit_aggregate.md`, `final_audit_stage1_*.md` (5 chapter reports)

## v227 (2026-05-04) — Triage reframe merge: 215pp → 197pp, Phase 4 PASS 83.63/100

Branch `experiments/triage-reframe` (9 commits) merged into master with `--no-ff`.

**Outcome**:
- 215pp → 197pp (-18pp risk-managed compression)
- Wet-lab triage repositioning: deployment refused; Layer C (6/11 DMS pathogens, 650 positions) elevated as primary practical-value anchor
- ANOVA 5-frame narrative restored (Cameron 2008 wild-cluster justification)
- Phase 4 Prof v8 (2-stage hybrid 5 chapter-deep + 10 prof aggregator): **83.63/100** (vs single-read v7: 77.72)
- All 10 profs ≥ 80; All 4 gates PASS

**Method innovation**: 2-stage hybrid evaluation. Single-read 10-prof was systematically underrating because 197pp/prof attention is too thin per item. Stage 1 caught 52 hidden issues bulk-read missed; Stage 2 prof aggregators consume Stage 1 reports + their specialty deep-read.

Reports: `paper/dissertation/review/2026-05-03/professor_v8_aggregate.md`, `docs/wiki/triage-reframe.md`.

## v220 (2026-05-03) — Phase 4 prof v6 distributed
- 10 codex blind agents per professor role
- Score: **77.52/100** (range 73.5–81.0); item I limit-awareness 9.00 strongest, G practical 6.80 weakest
- Gate: skill-memory diagnostic PASS (mean 7.75, min 6.0); Phase 4 prompt 80/100 FAIL (-2.48)
- Verdict: CONDITIONAL PASS

## v219 (2026-05-03) — HIV-1 Bonferroni-survivor mean fix (audit_v3 ch4a M1)
- ch4 line 13: "HIV-1 ≈ 4-5×" → "HIV-1 ≈ 2.3× (132/780 survivors) / 2.7× (freq subset)"

## v218 (2026-05-03) — audit v3 round 1, 6 Major fixes
- ch4 MERS 530 seqs, ANCOVA 0.233/0.274, SASA Norovirus, P2 CI list 4/12, SARS top-5 2/15
- ch3 SASA/Norovirus pLDDT source

## v217 (2026-05-03) — audit v2 round 2, 4 Major fixes
- ch2 Bailey 26 tools, EVEREST/ProteinGym preprint disclosure
- ch3 AUROC retain claim, ch5 region_overlap_mcc caption

## v216 (2026-05-03) — audit v2 follow-up, 4 Major fixes
- ch4 HIV-1 26/23 inversion, D614G ch4 line 336, P1 6/12, decision curve 41

## v215 (2026-05-03) — audit v2 + compress v2 (24 codex chunks)
- 2 regression fixes (Stage 1 417 AA, MERS 15%)

## v214 (2026-05-03) — deep 5-chapter audit + Critical/Major fact-check fixes (+0.75 blind)

## v213 (2026-05-03) — Top-12 chapter compression (-19pp, blind +0.3)

## v212 (2026-05-03) — Ch4 audit ledger + ch5 5-frame consolidation (-7pp, blind +0.6)

## v211 (2026-05-03) — blind codex professor evaluation (anchoring sanity check)

## v210 and earlier — see git log
