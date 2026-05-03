# Codex design review — Cycle 6 user-intent-aligned content review

Execute the design-review task NOW. Read-only. Write only the final design report.

You are designing a content-focused dissertation review with the user. The user's
intent (Korean): "내용의 적절성, 분량의 적절성, 방법의 적절성, 그리고 주장하는
내용이 산만하지 않고 하나로 집중되는지, 흐름은 적절한지, 데이터들은 적절한지와
관련된 확인". Translation: "appropriateness of content, length, method, whether
the argument is one focused thesis vs scattered, whether flow is appropriate,
whether data is appropriate".

Cycles 1-4 already covered these adversarial perspectives, with separate reports
under `paper/dissertation/review/2026-05-02/`:
- cycle 1-3: 4-phase paper-plan (blueteam, redteam, statistics, professor)
- cycle 4: A falsifiability, B Layer A curation, C negative framing,
  D counterfactual null, E reproducibility, F stat alternatives,
  G HIV-1 cherry-pick, H generalisation scope, I content flow

The current draft 6 axes:

1. **Content appropriateness** — PhD-level depth, contribution scope,
   engineering-vs-science balance, chapter content fit
2. **Length appropriateness** — 242 pages, chapter balance, bloat/thin
   sections, figure/table/equation density
3. **Method appropriateness** — ANOVA, Friedman, LOPO, bootstrap, cluster-bootstrap,
   Bayesian frames — right choice? simpler alternatives?
4. **Argument focus** — one central thesis vs scattered claims, orphan
   sections, page-1-clear thesis statement
5. **Flow** — motivation → method → result → discussion progression,
   Wave 1-5 as add-on vs integral
6. **Data appropriateness** — 11/12 pathogen panel, sequence sources,
   ground truth choices, alternative datasets

## Your task

Produce a design-review report at:

  `/proj/paper/paper/dissertation/review/2026-05-02/cycle6_design_review.md`

Structure:

### 1. Coverage assessment (per axis)

For each of the 6 axes:
- Is the axis well-defined? Specific enough to execute?
- Does it overlap meaningfully with cycle 1-4 perspectives? If yes,
  what's the differentiating angle worth running?
- What concrete check items would you propose? (List 4-8 per axis.)
- Is this axis useful for the user's stated intent, or does it duplicate
  earlier work?

### 2. Missing axes

The user's intent spans content/length/method/focus/flow/data. Are there
related axes the user implicitly wants but didn't list? Examples to consider:
- thesis-claim-vs-evidence calibration (proven/retrospective/deferred)
- defendability under verbal Q&A (vs cycle 1-4 written reviews)
- contribution distinctness (each contribution is genuinely separate?)
- editorial polish (no orphan footnotes, no broken anaphora, no
  inconsistent terms)
- chapter-self-sufficiency (could a committee read just ch4 and follow?)

Recommend 1-3 ADDITIONAL axes if you find genuinely missing ones.

### 3. Check-item refinement

Propose specific check items per axis (4-8 each). Each check item must be:
- Concrete: a specific question with a yes/no or tier answer
- Verifiable: file:line evidence available
- Useful: answer changes a defense decision

Format example:
```
### Axis 2 — Length appropriateness

Check items:
- L1. Total page count vs Korean university PhD norm (target 150-300pp,
  current 242pp). Verdict: appropriate / over / under.
- L2. Chapter 4 page count proportion (current XX/242 = XX%). Cohen's
  rule of thumb: results 30-40% of total. Verdict.
- L3. ...
```

### 4. Execution plan recommendation

Given that 6 axes (or 6+N) require codex jobs:
- Which can be combined into one codex job (overlapping perspectives)?
- Which must remain separate (independent axes)?
- Suggest the minimum codex job count and optimal grouping.

### 5. User confirmation prompt

Draft the question(s) to present to the user before launch:
- Confirm 6 axes are right
- Confirm any added axes
- Confirm execution plan (parallel jobs / sequential)

Length budget: ≤ 2500 words. Use neutral terminology. Cite specific
manuscript or review-report locations only when necessary.
