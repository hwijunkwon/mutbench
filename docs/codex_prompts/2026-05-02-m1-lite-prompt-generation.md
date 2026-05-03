# Codex task — M1-lite: generate 4 agent prompt files for dissertation audit

You are authoring four agent-prompt markdown files. **Workspace-write OK.
Do not commit.** No external tooling — pure file authoring from existing
memory protocols + the audit plan.

## Inputs

Read first:

- `/proj/paper/docs/plans/2026-05-02-dissertation-audit-plan.md` (v2 plan — your
  source of truth for scope, gates, and expected outputs)
- `/home/hwijun/.claude/projects/-proj-paper/memory/agent_review_structure.md`
  (5-stage pipeline, 10 evaluation items A–J)
- `/home/hwijun/.claude/projects/-proj-paper/memory/professor_evaluation_skill.md`
  (10-professor protocol, 9-item rubric, scoring criteria)
- `/home/hwijun/.claude/projects/-proj-paper/memory/fairness_issue.md`
  (the Layer A vs freq correlation concern that Statistics step 10 must address)
- `/home/hwijun/.claude/projects/-proj-paper/memory/source_of_truth.md`
  (which files are authoritative for numbers)
- `/home/hwijun/.claude/projects/-proj-paper/memory/required_citations.md`
  (citation expectations)

## Outputs

Create exactly four files:

1. `/proj/paper/paper/dissertation/manual/04_agent_prompts/prompt_blueteam.md`
2. `/proj/paper/paper/dissertation/manual/04_agent_prompts/prompt_redteam.md`
3. `/proj/paper/paper/dissertation/manual/04_agent_prompts/prompt_statistics.md`
4. `/proj/paper/paper/dissertation/manual/04_agent_prompts/prompt_professor.md`

Each prompt is self-contained: a downstream codex agent should be able to
execute the prompt without further context from this conversation.

## Author each prompt to these specs

### Common preamble (include verbatim in every prompt)

```
You are an independent reviewer for a PhD dissertation. **Read-only mode.**
Do not modify the manuscript or any data. Write only your final report
to the path specified at the bottom.

The dissertation is at /proj/paper/paper/dissertation/. The active build
inputs are:
  - chapters_en/ch1_introduction.tex
  - chapters_en/ch3_methods.tex
  - chapters_en/ch4_results.tex
  - chapters_en/ch5_discussion.tex
  - front_en/abstract.tex

Orphan files (NOT in build) are: ch2_background.tex, ch5_adapt.tex,
ch6_conclusion.tex. Do not cite them as evidence.

Authoritative supporting reports under paper/dissertation/review/:
  - 2026-04-30/wave1/, wave2/, wave3/, wave4/ — codex per-task reports
  - 2026-05-02/wave5_replacement/lap_lopo_report.md — Wave 5 Layer A' result
  - 2026-05-02/codex_layerA_uniprot_review.md — codex review of Layer A' inventory
  - 2026-05-02/codex_wave5_disposition_review.md — earlier disposition review

Use neutral, scope-appropriate terminology. Do not re-quote biological
detail beyond what is required for the specific finding you are reporting.
```

### prompt_blueteam.md (argument-map task)

- Task: build the dissertation's claim-evidence map for the 3 main contributions
  (the 12-pathogen literature-curated benchmark, the 1023-subset Shapley audit
  finding the 4-core is rank 87/1023 + dominated by 3-core, and the Wave 5
  Layer A' label-provenance Branch C result).
- For each claim: cite (file, line) for the strongest evidence + the
  weakest evidence + the chapter that holds the claim's main statement.
- 5 failure scenarios + which prose paragraph defends against each.
- Per-chapter weakest paragraph identification (Ch1, Ch3, Ch4, Ch5).
- Output: `/proj/paper/paper/dissertation/review/2026-05-02/phase1_blueteam.md`,
  ≤ 3000 words.

### prompt_redteam.md (adversarial attack task)

- Task: attack the dissertation in the spirit of a hostile committee member.
  Output Critical / Major / Minor.
- **Required attack targets** (the agent must explicitly attempt each):
  1. Wave 5 Branch C interpretation — could it be read as "negative result
     hidden as sensitivity check"?
  2. Panel-size limit framing — is it falsifiable as currently worded?
  3. Layer A vs Layer A' provenance argument — is the asymmetry genuinely
     informative or post-hoc?
  4. Algorithm 1 vs benchmark separation — does the manuscript over-stake
     the cold-start operationalisation?
  5. ω² = 0.296 interpretation — is it described correctly given the
     known concern in `fairness_issue.md`?
- For each attack: severity + evidence path + minimal prose fix.
- IV&V principle: do NOT consult Phase 1 or Statistics output.
- Output: `/proj/paper/paper/dissertation/review/2026-05-02/phase2_redteam.md`,
  ≤ 3000 words.

### prompt_statistics.md (formal statistics review)

- Task: 10-item PASS / WARN / FAIL. The 10 items must include:
  1. ω² interpretation correctness
  2. paired vs unpaired test choice (e.g., Welch t for cross-panel,
     Wilcoxon paired for same-fold comparisons)
  3. multiple-comparisons control
  4. sign-stability bootstrap interpretation
  5. MCC vs precision@20 reporting consistency
  6. sample-size justification for n=12 panel
  7. Wave 5 cross-panel Welch t caveat enforcement
  8. permutation-null framework rigor (P1, P6 nulls)
  9. callability rule pre-registration vs post-hoc adjustment
  10. **fairness_issue.md** explicit framing — is the Layer A vs `freq`
      correlation framed as correlation/circularity risk in the
      manuscript, or buried in generic limitations? Cite location and
      severity.
- Per item: PASS / WARN / FAIL + 1-3 sentence justification.
- Final: core-claim statistical reliability rating (high / medium / low).
- IV&V principle: do NOT consult Phase 1 or Phase 2 output.
- Output: `/proj/paper/paper/dissertation/review/2026-05-02/phase2_statistics.md`,
  ≤ 3000 words.

### prompt_professor.md (10-professor 9-item rubric)

- Task: simulate the 10-professor committee from
  `professor_evaluation_skill.md` and score the dissertation on the 9-item
  rubric (A through I, J).
  Items: A. 문제 정의, B. 관련 연구, C. 방법론, D. 실험 규모, E. 결과 해석,
  F. 기여 독창성, G. 실용 가치, H. 서술 명확성, I. 한계 인식, J. 완성도.

  Note: there are 10 letter labels but the memory file calls it a "9-item"
  rubric. Treat A–J as 10 distinct items (the discrepancy is a memory-file
  numbering issue; do not lose any item). Maximum total = 100 (10 × 10).
- 10 professors with mixed strictness levels per the memory file.
- Each professor scores each item 0–10. Output the 10×10 matrix.
- Pass criterion: **total ≥ 80/100, no single item < 6, and no unresolved
  Critical from Phase 3** (Phase 3 Critical list will be supplied as
  input at execution time).
- Diagnostic appendix: also report skill-defined mean ≥ 7 / individual
  ≥ 5 result, but it is NOT a gate.
- Output: `/proj/paper/paper/dissertation/review/2026-05-02/phase4_professor.md`,
  ≤ 3500 words.

## Quality requirements for the four files

- Each prompt is self-contained — downstream codex run does not need this
  conversation.
- Each prompt names its output path explicitly.
- Each prompt cites the active-build files only (no orphan citations).
- Each prompt uses neutral terminology and does not re-quote biological
  technical detail unnecessarily; reference review-report paths for
  technical content rather than embedding it.
- Each prompt obeys the IV&V principle for cycle 1 (Phase 1, 2, Stats do
  not see each other; Phase 4 may consume Phase 3 summary only).
- Length budget per prompt: ≤ 800 words.

## Final action

After writing the 4 files, print a 5-line summary:

```
M1-LITE COMPLETE
- prompt_blueteam.md: <wordcount> words
- prompt_redteam.md: <wordcount> words
- prompt_statistics.md: <wordcount> words
- prompt_professor.md: <wordcount> words
```

Do not commit.
