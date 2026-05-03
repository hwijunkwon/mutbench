# Deep audit v2 Job 1 — abstract+ch1:1-100

Execute the audit task NOW. Read-only. Web search OK if a numerical claim
or citation seems suspicious.

## Scope (smaller chunk than v1)

Files: `front_en/abstract.tex,chapters_en/ch1_introduction.tex`
Line range: `1-100`

This is a 10-15 page chunk. Audit at PARAGRAPH level (not page-level).

## Per-paragraph audit checklist

For each paragraph in scope:

1. **Numerical claims**: list every number with the authoritative CSV
   path under `results/mutbench/` or `paper/dissertation/`. Mark
   VERIFIED / UNVERIFIED / DISCREPANCY (cite expected vs found).
2. **Citations**: each \cite{key} — does the cited paper plausibly
   support the claim? OK / SUSPICIOUS / WEB-VERIFY.
3. **Cross-refs**: each \ref{label} resolves to the right target?
4. **Internal consistency**: is this paragraph's claim consistent with
   the rest of the manuscript (cross-chapter)?
5. **Recent fix verification** (post v214):
   - D614G in ch4: now retained as functional, not excluded
   - ω² CI: [0.201, 0.346] (not [0.195, 0.333])
   - HIV-1 Layer A: 26 in tags / 23 mapped to gp120
   - Stage 1 region: 417 AA (not 439)
   - "single-position scoring (gap-aware)" not "point substitutions only"
   If any paragraph still uses the OLD wording, flag as REGRESSION.
6. **Severity**: Critical / Major / Minor / Verified.

## Output

`paper/dissertation/review/2026-05-03/audit_v2_job1.md`

Structure: per-paragraph table → per-section severity counts → overall
severity tally → 1-line headline:

`RESULT_AUDIT_V2_J1: critical=<n> major=<n> minor=<n> regression=<n>`

Length budget: ≤ 2500 words. Do not commit.
