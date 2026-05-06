# Agent 5 — Ch1 Motivation Problems 1-3 vs Manuscript Answers Audit

Execute the audit task NOW. Read-only. Do not commit.

## Reviewer concern (user-driven)

The user asks: "Ch1 Research Motivation states three specific problems (Problem 1: standardized framework lacking; Problem 2: independent ground truth absent; Problem 3: pathogen-dependence statistical evidence missing). Does the dissertation actually answer these three problems sufficiently in chapters 3-6?"

**If yes** → Research Objectives wording is fine, no changes needed.
**If no** → either:
- (a) Rewrite Ch1 motivation to scope the problems more honestly
- (b) Add manuscript content to address the gaps

## Read first

- `paper/dissertation/chapters_en/ch1_introduction.tex` (Research Motivation, lines 21-39; Research Contributions, lines 123-159)
- `paper/dissertation/chapters_en/ch3_methods.tex` (3-layer ground truth, scoring, detection design)
- `paper/dissertation/chapters_en/ch4_results.tex` (Stage 1+2 results, Layer C, vaccine escape, ANOVA, LOPO)
- `paper/dissertation/chapters_en/ch5_discussion.tex` (Methodological Validity, Limitations, Conclusions)
- `paper/dissertation/review/2026-05-06/curation_audit_agent1.md`, `curation_defense_agent2.md`, `curation_statistics_agent3.md` (recent curation analysis)

## The three problems (verbatim from Ch1)

**Problem 1**: "Lack of a standardized evaluation framework"
- Existing methods (incl. MutClust) report on their own datasets / criteria
- Bootstrap test is self-referential; cannot verify biological meaning

**Problem 2**: "Absence of validation based on independent ground truth"
- No ground truth framework for viral mutation hotspot detection
- Convergent evolution / purifying selection / DMS available but not integrated

**Problem 3**: "Lack of statistical evidence on the pathogen-dependence of best-performing methods"
- Methods tuned for single pathogens, generalizability not quantified
- Algorithm selection problem (Rice 1976) — unanswered

## Task: per-problem answer audit

For EACH of the three problems:

### A. Where in the manuscript is this problem answered?
Quote specific sections / paragraphs / tables that constitute the answer.

### B. Strength of answer
- Strong (problem fully resolved)
- Partial (answer addresses some but not all aspects)
- Weak (answer present but acknowledges fundamental gaps)
- Missing (problem not addressed in body)

Specifically check:
- **Problem 1 answer**: does the manuscript actually establish a "standardized framework"? Or does it acknowledge that the framework still depends on Layer A curation heterogeneity (which Agents 1-3 found is 46-60% curation-protocol-dependent)?
- **Problem 2 answer**: does the 3-layer ground truth provide "independent" ground truth? Or is Layer A literature-curated (single-team synthesis, region-based for some pathogens) — i.e., not truly independent of any specific theoretical framework?
- **Problem 3 answer**: does ω²=0.296 actually quantify "pathogen-dependence" cleanly? Or does it conflate biology with curation-protocol-dependence (per Agent 3, 46% may be curation-driven)?

### C. Defendability at oral defense
For each problem, can the candidate convincingly answer "yes, my dissertation solves this"? Identify the strongest counter-argument a strict reviewer would raise.

### D. Recommended action
For each problem:
- Option A: keep current Ch1 motivation wording, add manuscript content to strengthen answer
- Option B: rewrite Ch1 motivation to scope the problem more modestly (e.g., "we provide a benchmark *bound by* literature-curated Layer A, acknowledging curation heterogeneity as part of the design")
- Option C: hybrid — keep Ch1 broad framing but add an explicit "scope-bounding" paragraph in Ch1 stating what each problem is partially vs fully answered

## Output

`paper/dissertation/review/2026-05-06/problem_answer_mapping_agent5.md`

Structure:

```
# Problem-Answer Mapping Audit

## Problem 1: Standardized framework
**Where answered**: ...
**Quoted answer**: ...
**Strength**: Strong / Partial / Weak / Missing
**Strict-reviewer counter-argument**: ...
**Recommended action**: A / B / C with specific text suggestion

## Problem 2: Independent ground truth
{same structure}

## Problem 3: Pathogen-dependence statistical evidence
{same structure}

## Cross-problem coherence check
Does the manuscript's answers to P1+P2+P3 form a coherent story, or do they contradict each other?

## Final recommendation
- (a) Keep Ch1 motivation as-is, body answers are adequate
- (b) Rewrite Ch1 motivation
- (c) Hybrid: scope-bounding paragraph + body additions

User-supplied framing context: hotspot is comprehensive AND fluid — should this framing be applied to the Problem 2 answer (Layer A heterogeneity is feature, not bug)?

RESULT_PROBLEM_ANSWER_AGENT5: p1_strength=<S|P|W|M> p2_strength=<S|P|W|M> p3_strength=<S|P|W|M> recommended_action=<a|b|c> ch1_rewrite_needed=<yes|no>
```

Length: ≤ 2500 words.
