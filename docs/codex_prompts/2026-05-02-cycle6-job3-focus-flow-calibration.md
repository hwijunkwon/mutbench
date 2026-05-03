# Cycle 6 Job 3 — Argument Focus + Flow + Claim-Evidence Calibration

Execute the audit task NOW. Read-only. Write only the final report.

You are a narrative-coherence and claim-calibration reviewer. Active English
build files at `/proj/paper/paper/dissertation/chapters_en/`. Use neutral
terminology.

This Job covers axes 4 (Focus), 5 (Flow), 7 (Claim-Evidence Calibration) of
the cycle 6 design.

**IMPORTANT**: Do NOT duplicate cycle 4 I (content flow) — extend it with
the focus/calibration angle. Cycle 4 I established structure grade = B
with 11 PASS / 5 WARN / 1 FAIL.

## Task: Axis 4 — Argument Focus

Apply F1-F6. Verdict + evidence + rationale.

F1. Is the central thesis visible on page 1/abstract?
   I.e., can a reader stop after page 1 and state the thesis in one sentence?
F2. Can the thesis be stated as one sentence without losing the three contributions?
F3. Do all major sections serve the same thesis rather than separate project identities?
   (Example test: are Wave 1-5 audits part of THE main thesis, or do they read
   as a different project layered on top?)
F4. Is the practical contribution (HIV-1 search-space reduction) subordinate
   to the benchmark/pathogen-dependence thesis?
F5. Are pathogen case studies assigned stable roles: sanity check, main panel,
   external anchor, exploratory?
F6. Are 11/12 pathogen, 3-core/4-core, and Layer A/A' distinctions handled
   without fragmenting the argument?

## Task: Axis 5 — Flow

Apply W1-W7. Verdict + evidence + rationale.

W1. Does the chapter sequence match motivation -> benchmark design -> evidence -> interpretation?
W2. Does Ch1's roadmap match the actual current chapter contents?
W3. Does Ch3 prepare every major Ch4 analysis before results appear?
W4. Does Ch4 order results from central to supporting evidence?
W5. Does Ch5 discuss limitations after the relevant result has been established?
W6. Are Wave 1-5 presented as an integrated robustness arc?
W7. Does the conclusion close the argument without introducing new claims?

## Task: Axis 7 — Claim-Evidence Calibration

Build a defense-facing claim register. For each headline claim found in
abstract / Ch1 contributions / Ch4 key findings / Ch5 conclusion, classify
into one of:
- **Proven**: established by direct test on the manuscript's panel with
  appropriate statistical evidence
- **Retrospective**: tested but only on the in-sample evaluation; no
  prospective time-forward generalisation
- **Suggestive**: weakly supported / single-case / pilot
- **Negative**: a result that fired against the original hypothesis,
  reported transparently
- **Future work**: deferred, acknowledged as not yet established

Apply E1-E6.

E1. Are all abstract headline claims classified as proven, retrospective,
   suggestive, negative, or future work?
E2. Does every "demonstrates/shows/confirms" verb match the evidence tier?
E3. Are retrospective benchmark findings distinguished from prospective
   deployment claims?
E4. Are null/negative results included in the claim register?
E5. Are confidence intervals and p-values used only where the inferential
   unit supports them?
E6. Does the conclusion avoid upgrading suggestive evidence into established fact?

## Output

Write report to:
  `/proj/paper/paper/dissertation/review/2026-05-02/cycle6_job3_focus_flow_calibration.md`

Structure:
1. Axis 4 results table (6 rows)
2. Axis 5 results table (7 rows)
3. Axis 7 claim register table (one row per headline claim with tier classification)
4. Axis 7 results table (E1-E6)
5. Top 3 cross-axis gaps with concrete prose suggestions
6. The one-sentence thesis you would propose if F2 currently fails (≤30 words)
7. Verdict summary
8. End with one-line headline:
   `RESULT_J3: focus=<strong|medium|weak> flow=<strong|medium|weak> calibration=<strong|medium|weak> top_gap=<short_phrase>`

Length budget: ≤ 3000 words. Do not commit.
