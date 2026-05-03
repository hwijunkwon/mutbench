# Risk-1 Deep archetype 3 — ML / VEP-PLM expert committee member rebuttal expansion

Execute the analysis NOW. Read-only. Do not commit.

## Context

The ML/PLM expert is the highest-strictness reviewer (Prof 06 in v6 panel scored 73.5, lowest). They will probe whether the negative result is a labeling/feature/learning failure rather than an actual cross-pathogen barrier.

## Inputs

- `paper/dissertation/review/2026-05-03/risk1_framing_analysis.md`
- `paper/dissertation/chapters_en/ch3_methods.tex` scoring/detection sections (lines 488–720)
- `paper/dissertation/chapters_en/ch4_results.tex` feature-ablation + adaptive-weighting sections (lines 624–700, 706–893)
- `paper/dissertation/chapters_en/ch5_discussion.tex` lines 121–125 (cross-pathogen and Rice/NFL framing)

## ML expert role

Specialty: VEP, PLM (ESM-2, EVE, EVEscape, Tranception, ProteinGym), MSA-based methods, supervised/few-shot learning, label-noise theory, meta-learning. Strict on: are baselines adequate? did you try modern adaptive paradigms? is the negative result a labeling/feature/model issue or a fundamental cross-pathogen barrier?

## Task: defense-script

### 1. Opening question
ML expert: "The negative result may simply show that your labels/features/models are weak, not that cross-pathogen detection is unlearnable. Also, EqualWeight and 4-core heuristics are not modern adaptive learning."

### 2. Three follow-up questions

Cover these variants:
- "Did you try meta-learning or fine-tuning across pathogens?"
- "Why not use ESM-2 fine-tuning on Layer A pooled across pathogens?"
- "Cycle 7B failures could be feature-ablation artifacts — did you control for multicollinearity?"
- "ProteinGym shows VEP works at protein level. Why doesn't your benchmark inherit that?"

For each:
- Quote
- Why hard
- Best 2-3 sentence rebuttal citing the scope: per-position region-level vs per-variant; 10 information types + 20 scoring formulas + 39 detector variants exhaust the audited representation space; HBFWS hierarchical Bayesian + 6 Cycle 7B paradigms span model-class boundary.

### 3. Two trap questions

- "Have you tried protein-language-model embeddings as inputs to a multi-task neural net trained on all 11 pathogens jointly?"
- "How does Wave 5 Layer A' negative result not just show your feature pipeline is wrong, not that labels are non-interchangeable?"

For each: honest scope-narrowing answer. Note that Wave 5's sign-flipped MCC is genuinely informative because it shows label-provenance, not feature, is the bottleneck.

### 4. Strongest deduction

What item(s) would Prof 06 most likely deduct? F (novelty) or D (scale)? Identify the rebuttal anchor that converts the deduction from "this should not pass" to "this should pass with caveats."

## Output

`paper/dissertation/review/2026-05-03/r1_deep_ml.md`

End with: `RESULT_R1_DEEP_ML: anticipated_score=<x.x>/10 most_at_risk_item=<letter> rebuttal_anchor="<one phrase>"`

Length: ≤ 2000 words.
