# Codex Audit Plan Review

## 1. Verification

### `ls -d /proj/paper/paper/dissertation/manual/ 2>&1 | head -2`

```text
ls: cannot access '/proj/paper/paper/dissertation/manual/': No such file or directory
```

Claim match: matches lines 38-42: "`manual/` directory" and "**None of these files exist in the repo**".

### `grep "\\input" /proj/paper/paper/dissertation/thesis_en.tex 2>&1`

```text
%%   Digital submission: xelatex "\def\printmode{0}\input{thesis_en}"
%%   Print version:      xelatex "\def\printmode{1}\input{thesis_en}"
  \input{front_en/abstract}
\input{chapters_en/ch1_introduction}
%% \input{chapters_en/ch2_background}  % merged into ch1 in v170 (M1 macro cut)
\input{chapters_en/ch3_methods}
\input{chapters_en/ch4_results}
%\input{chapters_en/ch5_adapt}  % merged into ch4_results
\input{chapters_en/ch5_discussion}
%% \input{chapters_en/ch6_conclusion}  % merged into ch5 in v168 (M4 macro cut)
  \input{front/abstract_kr}
```

Claim match: mostly matches line 53, but note that the command output includes `front/abstract_kr`; the plan's "4 chapters input by thesis_en.tex" is correct only for `chapters_en`.

### `ls /proj/paper/paper/dissertation/chapters_en/ 2>&1`

```text
ch1_introduction.tex
ch2_background.tex
ch3_methods.tex
ch4_results.tex
ch5_adapt.tex
ch5_discussion.tex
```

Claim match: matches lines 30 and 53: active English build uses ch1/ch3/ch4/ch5_discussion, while `ch2_background` and `ch5_adapt` exist as orphan/non-input files.

### `ls /proj/paper/paper/dissertation/verify_dissertation.py 2>&1`

```text
/proj/paper/paper/dissertation/verify_dissertation.py
```

Claim match: matches line 29.

### `cd /proj/paper/paper/dissertation && python3 verify_dissertation.py 2>&1 | tail -25`

```text
      Either: 20 lines (2.1%)
  [PASS] ch4_results.tex: MOSD/MutClust mentions = 2.1% (<= 15%)

    ch5_adapt.tex (312 lines):
      MOSD: 0 lines
      MutClust: 0 lines
      Either: 0 lines (0.0%)
  [PASS] ch5_adapt.tex: MOSD/MutClust mentions = 0.0% (<= 15%)

    ch5_discussion.tex (333 lines):
      MOSD: 0 lines
      MutClust: 2 lines
      Either: 2 lines (0.6%)
  [PASS] ch5_discussion.tex: MOSD/MutClust mentions = 0.6% (<= 15%)

======================================================================
SUMMARY
======================================================================
  [PASS] 129
  [FAIL] 4
  [WARN] 6
  Total checks: 139
======================================================================

  4 FAILURE(s) detected — review required.
```

Claim match: contradicts treating Phase 0 as a likely quick pass. Line 89 says pass condition is "**0 FAILs**"; actual output has "`[FAIL] 4`" and "`4 FAILURE(s) detected — review required.`"

### `git -C /proj/paper log --oneline -3`

```text
7204571 Revert "feat: v204 — Wave 5 Task 1 (PubMed search, 911 unique PMIDs)"
addb7f3 Revert "feat: v205 — Wave 5 Task 2 (evidence sheet + curation worksheets)"
c49ee27 feat: v207 — Wave 5 substitution (Layer A' UniProt sensitivity, Branch C)
```

Claim match: does not verify line 13's "`master @ v207+v208`"; the last three commits show v207 and two reverts, not v208.

## 2. Verdict

**PROCEED WITH MODIFICATIONS.** The pipeline shape is sound, but M1 should not be a hard prerequisite for cycle 1, Phase 0 must block on the current 4 FAILs, and Phase 4 should use one calibrated pass criterion.

## 3. Per-question answers

### 1. Phase order: is M1 the right first move?

Not as a hard first move. The plan says "the skill cannot proceed without them" and makes M1 generate `paper/dissertation/manual/`. That is useful for repeatability, but the current cycle can bootstrap Phase 1/2/Stats from inline prompts using `agent_review_structure.md`, `professor_evaluation_skill.md`, the plan itself, and the three recent reports as factual context.

Pros of M1 first: reusable prompts; lower drift across agents; easier user approval at Gate 2; better defense against hallucinated task scope. Cons: it burns 30-40 minutes before any audit signal, and manual authorship may encode premature assumptions before seeing cycle 1 failures.

My recommendation: split M1 into **M1-lite before cycle 1** and **M1-full after cycle 1**. M1-lite creates only `prompt_blueteam.md`, `prompt_redteam.md`, `prompt_statistics.md`, and `prompt_professor.md` or inline equivalents. Defer chapter guides and taxonomy polish until after Phase 3 reveals real failure modes.

### 2. IV&V parallelism vs sequential

Keep the first pass parallel. The plan's phrase "**none receives the others' output**" is correct for independent verification: it prevents Redteam and Statistics from anchoring on Blueteam's framing. That matters because the audit target is overclaiming and selective reporting; independence is itself a test.

Sequential seeded review can catch second-order issues: Statistics-first might identify quantitative weaknesses that Blueteam maps to claims, and Redteam seeded with both can attack the strongest integrated defense. But that is no longer IV&V; it is adversarial synthesis.

My position: run **parallel first, seeded second**. Keep Phase 1, Phase 2, and Statistics independent. Then make Phase 3 CCB do a short seeded reconciliation: ask whether any Redteam/Statistics issue invalidates a Blueteam evidence map, and whether Blueteam's claim map exposes any missing statistical check. This preserves independence while adding the main benefit of sequencing.

### 3. Pass criterion calibration

Requiring both gates is over-strict and partly incoherent. The plan combines "10 mandatory questions x answer-completeness" with the memory's committee rubric. Those measure different things, so an "either gate fails" rule can fail a defensible dissertation twice for overlapping reasons while providing no single interpretable committee verdict.

Use a single criterion: **memory-defined 10-professor rubric, total >= 80/100, no item below 6, and no unresolved Critical from Phase 3.** The skill-defined mean >= 7 / individual >= 5 can be retained as a diagnostic appendix, not a gate.

Rationale: the memory protocol is closer to the actual defense simulation and names the same 10-professor structure the plan wants. The skill-defined threshold is too permissive at the floor (minimum 5) and too vague about item identity. A total >= 80 with min >= 6 is stricter where it matters and easier to explain.

### 4. What does the plan miss?

Add Phase 0 checks for build artifacts and consistency: confirm `thesis_en.pdf`, `thesis_en.log`, `thesis_en.aux`, and `thesis_en.toc` exist; extract the last "Output written" line; compare `.aux` labels/citations against source after a fresh build or timestamp check; verify all table `\label{}` references resolve; and check page-number consistency between chapter starts in `.toc`, `.aux`, and the PDF page count.

Korean divergence should be **Phase 0 WARN, not full skip**. The plan can audit English only, but `front/abstract_kr` is actively input by `thesis_en.tex`, so Korean material is not completely out of scope. WARN should say English chapters are authoritative for this cycle; Korean synchronization is deferred unless it affects active front matter or build correctness.

Fairness: the issue in `fairness_issue.md` should be addressed in **Statistics step 10 and Phase 3 CCB arbitration**. Do not bury it in general limitations; Statistics should explicitly test whether the manuscript frames the concern as correlation/circularity risk, and CCB should decide whether any remaining phrasing requires a manuscript fix.

### 5. Minimum viable cycle

For 60 minutes, keep: Phase 0, Phase 2 Redteam, Statistics, and a compressed Phase 4. Cut M1-full, full Blueteam, and formal Phase 3 unless a Critical appears.

Non-negotiable prompts: `verify_dissertation.py` plus added Phase 0 checks; Redteam prompt focused on Critical/Major overclaiming; Statistics prompt focused on numeric consistency, test choice, small-panel caveats, provenance separation, and the fairness concern; Professor prompt using the single 10-professor rubric gate.

Optional if time remains: a 10-minute Blueteam claim map for only the three main contributions. Do not spend the first 30 minutes writing a polished manual in the 60-minute scenario.

## 4. Edit list

```diff
@@ line 13 @@
-defense-state dissertation (master @ v207+v208, thesis_en.pdf 236pp). The
+defense-state dissertation (current git HEAD verified before execution; record `git log --oneline -3` and `thesis_en.log` page count in Phase 0). The
+Rationale: required verification did not show v208, so the plan should not name an unverified revision.

@@ lines 38-47 @@
-The `paper-plan` skill expects a `manual/` directory ...
-... Codex authors them; we review before use.
+Cycle 1 may run from inline prompts derived from `agent_review_structure.md`, `professor_evaluation_skill.md`, and this plan. Generate `manual/` before repeated cycles or before committing the audit protocol as reusable infrastructure.
+Rationale: M1-full is useful, but not required to obtain first audit signal.

@@ lines 87-93 @@
 Run `verify_dissertation.py`, redirect to
 `paper/dissertation/review/2026-05-02/phase0_verify.txt`. Pass condition:
 **0 FAILs**.
+Current pre-check output is `[FAIL] 4`; Phase 1/2/Stats may run for diagnosis, but no clean audit verdict or Phase 4 pass may be issued until these FAILs are classified and blocking FAILs are fixed.
 Rationale: the actual verification output already fails the stated gate.

@@ lines 95-102 @@
 - DMS reference consistency (4/11 vs 6/11 deprecation)
+- build artefacts: `thesis_en.pdf`, `thesis_en.log`, `thesis_en.aux`, and `thesis_en.toc` exist and are current
+- `.aux` consistency: labels, citations, and table references match source after build
+- page-number consistency: chapter starts and total pages agree across `.toc`, `.aux`, log, and PDF
+- table cross-refs: every table `\label{}` is referenced intentionally or listed as intentionally unreferenced
+- Korean divergence: WARN for inactive Korean chapter drift; FAIL only if active `front/abstract_kr` or build inputs are stale/broken
+Rationale: these are defense-submission risks not covered by the current Phase 0 list.

@@ lines 124-131 @@
 - core-claim statistical reliability rating
+- explicit fairness check: address the issue in `fairness_issue.md` as the final Statistics checklist item
+Rationale: a known fairness concern should be actively tested, not left to generic Redteam review.

@@ lines 140-150 @@
 Inputs: phase1 + phase2 + statistics outputs ...
+Phase 3 also performs seeded reconciliation: test whether Redteam/Statistics findings invalidate any Blueteam claim map, and whether Blueteam exposes any missing statistical check.
+Rationale: preserves IV&V first pass while gaining the benefit of sequential synthesis.

@@ lines 162-172 @@
-Two flavours combined:
-...
-If either gate fails, list the failing item(s) ...
+Gate: use the memory-defined `professor_evaluation_skill.md` 10-professor rubric only. Pass requires total >= 80/100, no item < 6, and no unresolved Critical from Phase 3. The skill-defined mean >= 7 / individual >= 5 output may be reported as a diagnostic appendix, not a pass gate.
+Rationale: one calibrated criterion is more interpretable and avoids double-counting.

@@ lines 186-197 @@
 | M1 manual generation | codex | 20-30 min | 60k |
+| M1-lite inline prompt extraction | codex/claude | 10 min | 10k |
+Rationale: add a fast path for the 60-minute audit.

@@ lines 229-235 @@
 - Korean `chapters/` synchronization (P1 deferred per v206 policy)
+- Full Korean `chapters/` synchronization (P1 deferred); active Korean front matter remains in Phase 0 scope
+Rationale: `front/abstract_kr` is actively input by `thesis_en.tex`.
```

## 5. Minimum viable subset

60-minute audit:

1. Phase 0 hard preflight: run the required verification commands, `verify_dissertation.py`, LaTeX log checks, build artifact checks, `.aux`/`.toc` sanity, figure existence, and table-reference scan.
2. Phase 2 Redteam inline prompt: use line 117 scope plus the plan's line 121 attack targets; output only Critical/Major/Minor with evidence paths.
3. Statistics inline prompt: use lines 124-131 plus `fairness_issue.md`; require PASS/WARN/FAIL for statistical framing and known fairness risk.
4. Compressed Professor simulation: use only `professor_evaluation_skill.md` rubric; require total >= 80/100, no item < 6, and no unresolved Critical.

Cut for 60 minutes: M1-full manual generation, full Phase 1 Blueteam, formal Phase 3 CCB, final commit. If Redteam or Statistics finds a Critical, spend remaining time on CCB for that Critical only.

## 6. Hard blockers

Hard blocker before any clean M1-to-audit execution: `verify_dissertation.py` currently reports "`[FAIL] 4`". At minimum, classify the four FAIL categories before launching professor scoring. If any are numeric inconsistency, undefined reference, missing citation, or missing figure in active build paths, fix them before Phase 4.

Second blocker: line 13's "`v207+v208`" is not verified by `git -C /proj/paper log --oneline -3`. Replace it with a current-HEAD record.
