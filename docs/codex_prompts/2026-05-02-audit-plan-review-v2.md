# Codex review — Audit pipeline plan (v2, sanitized)

You are an independent reviewer for a draft pipeline plan. **Read-only.** Do
not modify files except your final report. Do not commit.

## Task

Evaluate the pipeline plan and return a verdict + concrete edits.

Plan: `/proj/paper/docs/plans/2026-05-02-dissertation-audit-plan.md`

## Verify these factual claims

Run these commands and record their actual outputs in your report.

```bash
ls -d /proj/paper/paper/dissertation/manual/ 2>&1 | head -2
grep "\\\\input" /proj/paper/paper/dissertation/thesis_en.tex 2>&1
ls /proj/paper/paper/dissertation/chapters_en/ 2>&1
ls /proj/paper/paper/dissertation/verify_dissertation.py 2>&1
cd /proj/paper/paper/dissertation && python3 verify_dissertation.py 2>&1 | tail -25
git -C /proj/paper log --oneline -3
```

Report whether each plan claim matches the actual output.

## Read these for context

- Plan: `/proj/paper/docs/plans/2026-05-02-dissertation-audit-plan.md`
- Memory: `/home/hwijun/.claude/projects/-proj-paper/memory/agent_review_structure.md`
- Memory: `/home/hwijun/.claude/projects/-proj-paper/memory/professor_evaluation_skill.md`
- Recent reports: `/proj/paper/paper/dissertation/review/2026-05-02/` (three review files
  from today; treat them as facts, do not re-quote technical content from them)

## Adversarial questions to answer

For each, give a direct answer with evidence. Stay at the meta-pipeline level —
do not re-quote technical content from the dissertation.

1. **Phase order — is M1 (manual generation) the right first move?** The plan
   says the manual is required before Phase 1, but is it possible to bootstrap
   the audit with inline prompts (skipping the manual) for cycle 1, and only
   formalise the manual after cycle 1 results are in hand? Pros/cons either way.

2. **IV&V parallelism vs sequential.** The plan runs Phase 1, Phase 2, and the
   Statistics phase in parallel without sharing outputs (independent verification
   and validation). Could running them sequentially (Statistics first, then
   Blueteam, then Redteam, each seeded with the prior outputs) catch more
   issues at the cost of independence? Where do you stand?

3. **Pass criterion calibration.** The skill defines mean ≥ 7, individual ≥ 5.
   The memory protocol defines total ≥ 80 with min ≥ 6. The plan says we run
   BOTH and require BOTH. Is this over-strict, under-strict, or right? Recommend
   a single criterion.

4. **What does the plan miss?** Specifically:
   - Phase 0 checks the plan should add (build artefacts, .aux file consistency,
     table cross-refs, page-number consistency between chapters).
   - Korean-chapter divergence (is it Phase 0 WARN or full skip?).
   - Any pre-existing fairness concern from memory that Phase 2 Statistics
     should weaponise (do not re-quote technical detail; just say "the issue
     in `fairness_issue.md` should be addressed in stage X step Y").

5. **What is the minimum viable cycle?** If the user only has 60 minutes,
   which phases are non-negotiable and which can be cut without making the
   audit useless?

## Output

Write your report to:

  `/proj/paper/paper/dissertation/review/2026-05-02/codex_audit_plan_review.md`

Structure:

1. **Verification section** — exact command outputs verifying the factual
   claims above.
2. **Verdict** — PROCEED / PROCEED WITH MODIFICATIONS / REVISE.
3. **Per-question answers** — concrete answers to the 5 questions, each ≤ 250 words.
4. **Edit list** — exact line-level edits to the plan, in unified-diff
   format if practical, or "replace section X with Y" if line-numbers are
   awkward. Each edit must have a one-line rationale.
5. **Minimum viable subset** — if user requests a 60-min audit, which
   phases survive and which prompts do they use.
6. **Hard blockers (if any)** — anything the plan must fix before any M1
   codex job runs.

Length: ≤ 2500 words. Cite file paths and exact phrases; do not paraphrase.
Do not re-quote dissertation technical content; treat the audit pipeline as
the only review subject.
