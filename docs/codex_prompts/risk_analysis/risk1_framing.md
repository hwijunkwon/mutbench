# Risk Analysis 1 — "Generalization is impossible" framing acceptability

Execute the analysis NOW. Read-only. Do not commit.

## Context

The dissertation (215pp post-v220, branch `experiments/triage-reframe`) is being repositioned:

**Old framing**: MutBench is a benchmark for cross-pathogen hotspot detection algorithms; LOPO 0/11, HBFWS p=0.78, Cycle 7B six-paradigm failures are reported as **null findings to be tempered**.

**New framing**: MutBench is a **wet-lab experimental triage tool** that narrows ~1,000 protein positions to 10–50 candidates with 7–9× escape enrichment. The negative audits (LOPO 0/11, HBFWS p=0.78, Cycle 7B all-fail, Wave 4/5) are reframed as **falsification-resistant evidence that a deployable cross-pathogen detector is not learnable at panel size n=11**. The panel-size threshold (~20–30 pathogens, Bolker rule-of-thumb) at which adaptive selection becomes possible is now positioned as a **contribution** of the dissertation.

## Question

Will a PhD defense committee accept the reframe? Specifically:

1. Is "we proved a detector cannot be built at this panel size" a **defensible contribution** or a **face-saving narrative**?
2. Does reducing the headline to "wet-lab triage" make the dissertation feel like an **engineering tool report rather than a research thesis**?
3. Are there committee archetypes (statistics-strict, biology-strict, ML-strict) who would specifically push back on this reframe? If so, what should the rebuttal anchor be?
4. Comparable dissertations / papers that use the same framing successfully (or unsuccessfully) — search literature/web if needed.
5. Net verdict: **defensible** / **defensible with specific guardrails** / **not defensible** / **needs different framing**.

## Read first

- `paper/dissertation/front_en/abstract.tex`
- `paper/dissertation/chapters_en/ch1_introduction.tex`
- `paper/dissertation/chapters_en/ch5_discussion.tex`
- `paper/dissertation/review/2026-05-03/professor_v6_aggregate.md` (10-prof scores; G=6.80 lowest)

## Output

`paper/dissertation/review/2026-05-03/risk1_framing_analysis.md`

Structure:
1. Defensibility verdict (one paragraph, lead with the verdict)
2. Three strongest committee pushbacks (statistician, biologist, ML expert) with anticipated wording + best rebuttal
3. Two comparable theses/papers that did this reframe successfully + one that failed (with citations if web search used)
4. Specific text-level guardrails (e.g., "always pair X with Y", "never claim Z without W")
5. One-line: `RESULT_RISK1: verdict=<defensible|guarded|not_defensible> primary_concern="<one sentence>"`

Length budget: ≤ 1500 words.
