# Risk-1 Deep archetype 2 — Biologist / wet-lab user committee member rebuttal expansion

Execute the analysis NOW. Read-only. Do not commit.

## Context

The wet-lab triage reframe is most relevant to the biologist committee archetype. They will probe the practical-value claim hardest. Risk-1 gave a sketch; expand to defense-script.

## Inputs

- `paper/dissertation/review/2026-05-03/risk1_framing_analysis.md`
- `paper/dissertation/chapters_en/ch4_results.tex` vaccine-escape + search-space sections (lines 941–989, 931–989)
- `paper/dissertation/chapters_en/ch5_discussion.tex` Practical Implications section (lines 123–233)
- `results/mutbench/vaccine_escape_stage3.csv` and `escape_validation_adapt.csv`

## Biologist role

Specialty: virology, vaccine immunology, structural biology of viral envelope glycoproteins. Strict on: false discovery vs operational deployment, retrospective vs prospective validation, dual-use risks, biological interpretability, lab-economics costs.

## Task: defense-script

### 1. Opening question
Biologist: "If 0/12 folds are callable and you cannot deploy this prospectively, why should a wet-lab group invest pipette time on MutBench predictions?"

### 2. Three follow-up questions

For each:
- Quote
- Why hard
- Best 2-3 sentence rebuttal anchored in HIV-1 anchor (7.19×, 82% Layer-A-disjoint, 37/45 novel positions, p_adj 3.9e-9) and search-space economics
- Cite ch4/ch5 line numbers

### 3. Two trap questions

Examples to cover (or substitute equivalents):
- "H3N2 has 69% Layer-A overlap — isn't that just rediscovering known antigenic sites?"
- "If MutBench prioritizes positions, isn't DMS already the gold-standard prioritization?"
- "Most viral hotspot 'discoveries' are sites already known from immune-evasion literature."

For each: quote, why weak, scope-narrowing honest response.

### 4. Strongest deduction

One-line on what the biologist most likely deducts and why. Identify the specific anchor that needs to lead the discussion (HIV-1 novel-only enrichment, not H3N2).

## Output

`paper/dissertation/review/2026-05-03/r1_deep_biologist.md`

End with: `RESULT_R1_DEEP_BIO: anticipated_score=<x.x>/10 anchor_to_lead="<HIV-1 ...>" trap_count=<n>`

Length: ≤ 2000 words.
