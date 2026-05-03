# Phase 4 Stage 1 — Chapter-Deep Evaluator

Execute the evaluation NOW. Read-only. Do not commit. Do not ask for confirmation.

You are a **chapter-deep evaluator** for the wet-lab triage MutBench dissertation.
Your job: read **only your assigned chapter** carefully and produce evidence for the 10-item rubric (A-J) so the Stage 2 professor panel can score with detail-aware input.

## Assigned chapter

`paper/dissertation/front_en/abstract.tex + paper/dissertation/chapters_en/ch1_introduction.tex` (~17 pp)

## Rubric (10 items)

- A. problem statement
- B. related work
- C. methodology
- D. scale (panel size, breadth)
- E. interpretation (results reading)
- F. novelty/contribution
- G. practical value (wet-lab triage utility)
- H. clarity (writing)
- I. limitations awareness
- J. overall maturity

## In-scope items for this chapter

A B F H J

## Recent state

Manuscript reframed v220 -> v226 as **wet-lab triage tool, not deployable detector**:
- 215pp -> 197pp (-18pp compression)
- Abstract evidence ledger added Layer C (DMS) 6/11 pathogens, 650 positions, MCC 0.139-0.322
- ch5 sec:vaccine_escape retitled "Wet-Lab Validation: Layer C DMS and Vaccine Escape"
- ANOVA 5-frame narrative restored (Cameron 2008 wild-cluster justification)
- Cold-Start algorithm reframed as "retrospective triage, not deployment"
- Cycle 7B / HBFWS / LOPO 0/11 paired with "at n=11, under tested regime" guardrail
- ω² = 0.296 cluster-bootstrap CI [0.201, 0.346]; HIV-1 7.19x with 82% Layer-A-disjoint

## Task

1. Read the assigned chapter carefully (full text, all tables, all figure captions).
2. For each in-scope rubric item:
   - List 2-3 strongest evidence points (quote exact phrases; cite line numbers if possible)
   - List 1-2 weakest evidence points (gaps, weak claims, unsupported phrasing)
   - Identify any **hidden issues** that a bulk-read 10-prof panel would miss (subtle framing slips, anchor-preservation failures, micro-inconsistencies)
3. Suggest a chapter-specific **score range** for each in-scope item (e.g., "B: 7.5-8.5 depending on prof strictness; weak on per-method history but strong on benchmark gap framing")
4. Flag any item where the chapter actively HELPS or HURTS panel-level interpretation.

## Output

`paper/dissertation/review/2026-05-03/professor_v8_stage1_abstract_ch1.md`

Structure:

```
# Chapter Deep Eval: abstract+ch1

## In-scope rubric items
- A
- B
- F
- H
- J

## Per-item evidence

### A (or applicable items)
**Strongest evidence**:
- <quote / line ref>
- <quote / line ref>

**Weakest evidence / gaps**:
- ...

**Hidden issues for panel awareness**:
- ...

**Suggested score range**: <x.x>--<x.x>

(Repeat for each in-scope item)

## Cross-cutting observations

- (subtle issues affecting multiple items)

## Bottom line for Stage 2 panel

One paragraph: what should the panel notice that bulk-read would miss?
```

Length budget: ≤ 2500 words.

End with: `RESULT_PROF_V8_STAGE1_abstract_ch1: in_scope_items=<n> hidden_issues=<n> recommended_score_floor=<x.x> recommended_score_ceiling=<x.x>`
