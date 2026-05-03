# Cycle 4 Perspective F — Statistical model alternatives stress test

Execute the audit task NOW. Read-only. Write only the final report.

You are a hostile statistician reviewing a PhD dissertation. Active English
build files at `/proj/paper/paper/dissertation/chapters_en/`. Use neutral
terminology.

## Task

The headline interaction effect $\omega^2 = 0.296$ was derived under a
fixed-effect three-way ANOVA on (scoring x detector x pathogen). The
manuscript already triangulates with FIVE inferential frames:

1. Pathogen-level cluster bootstrap (95% CI [0.195, 0.333])
2. Wild-cluster Rademacher bootstrap ([0.201, 0.303])
3. Phylogenetic block bootstrap at ICTV-family level ([0.202, 0.346])
4. Frequentist linear mixed-effects model (pseudo-$\omega^2 = 0.340$)
5. Bayesian two-way random-effects factor analysis (posterior mean 0.316)

Read `chapters_en/ch3_methods.tex` Section `subsec:anova_diagnostics` and
`chapters_en/ch4_results.tex` Section `subsec:anova_diagnostics` for full
context.

Identify model alternatives NOT yet tried, and estimate plausibility that
the conclusion would change under each:

- **A. Logistic/binomial model on per-cell binary success indicator**
  (instead of continuous MCC ANOVA)
- **B. Generalised linear mixed model with pathogen-specific random
  intercepts AND random slopes** (vs the current random-intercept frame)
- **C. Permutation ANOVA preserving block structure (pathogen-blocked
  permutation)** instead of the residual permutation implicit in bootstrap
- **D. Robust/M-estimator regression** (handles outlier pathogens differently)
- **E. Rank-based non-parametric two-way analysis (e.g., aligned-rank
  transform)** instead of parametric ANOVA
- **F. Bayesian model averaging across {Beta-Binomial, Normal, Skew-Normal}**
  outcome distributions

For each, give:
- Why it might give a different answer
- Plausibility that conclusion changes (low/medium/high)
- Approximate effort to add (hours)

Also flag any statistical claim in the manuscript that is fragile to
distributional or independence assumptions (e.g., normality of MCC, IID
within-pathogen).

## Output

Write report to:
  `/proj/paper/paper/dissertation/review/2026-05-02/cycle4_F_stat_alternatives.md`

Structure:
1. Per-alternative table: name, why-different, plausibility, effort
2. Identified fragile assumptions in current statistical claims
3. Recommended addition: at most ONE alternative the user should add
   before defense (smallest impact / largest robustness gain ratio)
4. End with a one-line headline:
   `RESULT_F: alternatives=<n> high_risk=<n> recommended_addition=<name|none>`

Length budget: ≤ 2500 words. Do not commit.
