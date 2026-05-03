# Triage Reframe Progress (branch: `experiments/triage-reframe`)

Goal: reposition MutBench as **wet-lab experimental triage tool**, not deployable detector. Generalisation framed as bounded finite-panel non-deployability rather than methodological failure.

Target: **215pp → 192pp** (~−23pp). Phase 4 prof v6 score 77.52 → expected 80+.

## Risk analyses (codex)

| Analysis | Verdict | Output |
|---|---|---|
| risk1 framing | **GUARDED** — defensible if scoped to finite-panel, anchor=HIV-1 wet-lab triage | `review/2026-05-03/risk1_framing_analysis.md` |
| risk2 compression | 21 blocks: 10 safe / 10 guarded / 1 keep; recommended target 192pp | `review/2026-05-03/risk2_compression_analysis.md` |
| risk3 abstract | **REVISE** — 4/8 anchors preserved in initial draft; concrete fix provided | `review/2026-05-03/risk3_abstract_analysis.md` |
| r1_deep (3 archetypes) | Statistician 7.2 / Biologist 7.2 / ML 7.4 expected scores | `review/2026-05-03/r1_deep_*.md` |
| r2_deep (5 batches, 21 blocks) | Line-level plans, total 687 lines saveable | `review/2026-05-03/r2_deep_batch{1-5}.md` |
| r3_deep (4 sub-analyses) | Anchor 37 occ partial / Panel 16 occ 1 overstrong / Draft 13/13 anchors / Consist 3 conflicts | `review/2026-05-03/r3_deep_*.md` |

## Sequence (option C, step-by-step)

| Step | Block(s) | Files | Lines saved | Pages | Status |
|---|---|---|---|---|---|
| 1 | Batch 1 — Ch1 BG #1 + Ch2 #4 #5 #6 | ch1_intro, ch2_bg | −114 | −9pp (215→206) | ✅ done |
| 2 | Batch 3 — Ch4 Stage1 #11 + Robust #12 + Structural #13 + ANOVA #15 | ch4_results | −134 | ~−10pp | pending |
| 3 | Batch 4 — Cold-Start #14 + Cycle 7B #18 + lattice #19 | ch4_results | −119 + 1 ledger row | ~−9pp | pending |
| 4 | Batch 5 — Info #17 + Biology #16 + Ch5 gen #20 + Future #21 + Ch1 contrib #2 #3 | ch1, ch4, ch5 | −138 | ~−10pp | pending |
| 5 | Batch 2 (safe parts only) — Ch3 #7 #10 (skip risky #8 #9) | ch3_methods | ~−50 | ~−4pp | pending |
| 6 | Abstract rewrite (r3_deep_abstract_draft) | abstract | −4 | 0 | pending |
| 7 | Build + Phase 4 prof v7 (10-prof distributed re-run) | — | — | — | pending |

## Guardrails (from risk1)

- Always pair "not learnable" with "at n=11, under tested regime"
- Pair LOPO 0/11 with ω²=0.296 + Friedman p=0.990 + adaptive failures
- Anchor practical value in HIV-1 wet-lab triage (7.19×, 82% disjoint, 37/45 novel)
- Treat 20–30 panel size as design target, not phase transition
- Replace "falsification-resistant" with "convergent negative audits" for statisticians
- Keep "MutBench benchmark" as Contribution 1, "pathogen-dependent info utility" as C2, "triage tool" as C3

## Per-step commits (will append as we go)

- (commit pending) Step 1 Batch 1 applied: Ch1 BG + Ch2 #4 #5 #6 → 215pp → 206pp
