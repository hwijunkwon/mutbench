# Codex review — Dissertation audit + professor evaluation plan

You are an independent reviewer for a draft audit plan. **Read-only.** Do not
modify anything except the report file. Do not commit.

## Your task

Evaluate the audit plan and return a verdict + concrete edits.

Plan: `/proj/paper/docs/plans/2026-05-02-dissertation-audit-plan.md`

## Required reading

- The plan itself (~10 min)
- Skill description: the 4-phase pipeline summarised in the plan §1, §5
- Memory protocols: `agent_review_structure.md` and
  `professor_evaluation_skill.md` (cited via the plan)
- Repository facts the plan claims:
  - `paper/dissertation/verify_dissertation.py` exists
  - `paper/dissertation/manual/` does NOT exist (gap)
  - `paper/dissertation/chapters_en/` has `ch1, ch2, ch3, ch4, ch5_adapt, ch5_discussion`
  - `thesis_en.tex` `\input`s only `ch1, ch3, ch4, ch5_discussion`
  - master at v207+v208, `thesis_en.pdf` 236 pp, 0 errors
  - prior reviews live under `paper/dissertation/review/`
- Recent project memory:
  - `codex_wave5_substitution.md` (today, 2026-05-02) — Wave 5 = Layer A'
    Branch C, MCC=-0.055, 2/10 positive folds, sign opposite to 12-panel
  - `codex_wave4_results.md` — Tier 2 features-only LOPO, 2-core fallback,
    panel-size limit
  - `feedback_verify_existing_data_first.md` — verification rule that
    saved this audit programme

## Verify these specific claims in the plan before accepting it

1. The plan says the manual files do not exist. Spot-check this:
   `ls -d paper/dissertation/manual/ 2>&1` should fail.
2. The plan says `thesis_en.tex` only inputs 4 chapters. Confirm with
   `grep "\\\\input" paper/dissertation/thesis_en.tex`.
3. The plan claims the codex biosafety filter triggered twice on
   2026-05-02. Inspect `docs/codex_prompts/2026-05-02-wave5-alternative-feasibility.md`
   for the original prompt and find the biology-trigger keywords.
4. The plan claims Phase 0 should pass cleanly today; do a dry sanity
   pass: `cd /proj/paper/paper/dissertation && python3 verify_dissertation.py 2>&1 | tail -20`.
   Report any [FAIL] or warning that would block Phase 1.
5. The plan claims a 9-item rubric. Confirm by reading
   `professor_evaluation_skill.md` §"평가 항목 (9개)". Report any
   discrepancy with the items A–J listed there (note: A–J is 10 letters
   for 9 items? — verify and flag).

## Adversarial questions to answer

For each, give a direct answer with evidence:

1. **Is M1 (manual generation) the right first move?** The skill says the
   manual is required before Phase 1, but is it possible to bootstrap the
   audit with inline prompts (skipping the manual) for cycle 1, and only
   formalise the manual after cycle 1 results are in hand?

2. **Is parallel Phase 1+2+Statistics IV&V worth the complexity?** Could
   running them sequentially (Statistics first, then Blueteam, then
   Redteam, each seeded with the prior outputs) catch more issues at
   the cost of independence? Where do you stand on this trade-off given
   the dissertation has only ~2 hours of audit time?

3. **Is the professor pass criterion calibrated correctly?** The skill
   defines mean≥7, individual≥5. The memory protocol defines total ≥80
   with min ≥6. The plan says we run BOTH and require BOTH. Is this
   over-strict? Under-strict? Recommend a single criterion.

4. **What does the plan miss?** Specifically:
   - any Phase 0 check the plan should add (build artefacts, .aux file
     consistency, table cross-refs)
   - any Wave 5 specific risk (Branch C interpretation could read as
     "negative result hidden as sensitivity check") that Phase 2 Redteam
     should pre-load with
   - Korean-chapter divergence — should it be Phase 0 WARN or full skip?
   - the Layer A' fairness concern (per memory `fairness_issue.md`,
     Layer A vs freq correlation already known) — should Phase 2
     Statistics weaponize this?

5. **Codex biosafety filter risk**. The plan says use "neutral
   terminology". Be specific: list 8–10 terms that are likely to trigger
   and their safe replacements. This is operational guidance Claude will
   need before sending Phase 1/2/Stats prompts.

6. **What is the minimum viable cycle?** If the user only has 60 minutes,
   which phases are non-negotiable and which can be cut?

## Output

Write your verdict report to:

  `/proj/paper/paper/dissertation/review/2026-05-02/codex_audit_plan_review.md`

Structure:

1. **Verification section** — exact command outputs verifying the 5
   factual claims listed above.
2. **Verdict** — PROCEED / PROCEED WITH MODIFICATIONS / REVISE.
3. **Per-question answers** — concrete answers to the 6 adversarial
   questions, each ≤ 250 words.
4. **Edit list** — exact line-level edits to the plan, in unified-diff
   format if practical, or "replace section X with Y" if line-numbers
   are awkward. Each edit must have a one-line rationale.
5. **Minimum viable subset** — if user requests a 60-min audit, which
   phases survive and which prompts do they use.
6. **Hard blockers (if any)** — anything the plan must fix before any
   M1 codex job runs.

Length: ≤ 3000 words. Cite file paths and exact phrases; do not paraphrase.
