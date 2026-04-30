# /proj/paper NOTES

Incremental research notes. Append-only unless correcting a factual error.

**Scope**: Session-to-session findings worth keeping that do not yet warrant a dedicated memory file. Graduate a note to `~/.claude/projects/-proj-paper/memory/` when it is referenced in 2+ future sessions.

**Source of truth**: see `~/.claude/projects/-proj-paper/memory/source_of_truth.md` — never treat this file as authoritative for citations, chapter content, or final results.

**Format**: `## YYYY-MM-DD` section per day, bullet points. Include file:line references when pointing at code or chapter text.

---

## 2026-04-17
- NOTES.md created as minimal increment layer (Red Team review rejected full Karpathy wiki adoption; this is the reduced alternative).

## 2026-04-30
- Codex Wave 1 (Tier 1 method-core P1–P4) execution started. Plan: `docs/plans/2026-04-30-codex-experiment-execution.md`. Codex consultation review: `paper/dissertation/review/2026-04-30/codex_wave1_plan_review.md` — 11 edits incorporated (formal Shapley, multi-metric, hard-stop gate, 5-scoring P4 panel, predeclared failure branches, per-task reports). Result subdir: `results/mutbench/codex_wave1/`. Per-task reports: `paper/dissertation/review/2026-04-30/wave1/`.
- P3 full lattice (2026-04-30): 1023 subsets enumerated. **4-core (freq+entropy+homoplasy+plddt) MCC = 0.0809, lattice rank 87/1023** — triggers P3 failure-mode branch (rank > 50). 4-core MCC matches existing 210-combo CSV exactly (|diff|=0). **3-core (freq+entropy+homoplasy) dominates 4-core: MCC 0.0866, rank 27/1023, +0.0058 vs 4-core.** Formal Shapley efficiency exact (sum=v(N)=0.0698). Top Shapley_MCC: homoplasy (+0.029), freq (+0.022), entropy (+0.022). pLDDT Shapley = -0.0015 (negative); esm2_llr = -0.014 (negative for both MCC + enrichment). Best lattice subset is 7-feature (k=7, MCC=0.0968, no pLDDT/esm2_llr/rare_freq). See `paper/dissertation/review/2026-04-30/wave1/p3_full_lattice.md`.
