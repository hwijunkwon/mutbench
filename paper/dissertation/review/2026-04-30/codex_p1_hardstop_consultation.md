# Codex P1 Hard-Stop Consultation

## 1. Option Verdicts

| Option | Verdict | Reason |
|---|---|---|
| A. Honor HARD STOP, skip P4, proceed to Task 6 prose insertions | **ACCEPTABLE** | This is the cleanest literal reading of the predeclared branch and immediately prevents overclaiming, but it leaves the callable-subset problem informal. |
| B. Re-scope P4 to the callable subset only | **REJECT** | Restricting P4 to the five pathogens selected by the P1 result is post hoc outcome conditioning; disclosure would reduce but not remove the cherry-pick risk. |
| C. Skip P4 in Wave 1; promote P5 callability rule to immediately follow P1 | **RECOMMEND** | This honors the HARD STOP while converting the observed heterogeneity into a prospective abstention protocol that can be evaluated without leaking P1 outcomes. |
| D. Re-run P1 with paired-bootstrap or sign-flip aggregation instead of Stouffer | **REJECT** | The Stouffer statistic was the binding global test; changing the global test after p=1.0 would read as post hoc rescue even if a signed-rank test would have been preferable ex ante. |

## 2. Single Recommended Path Forward

Choose **Option C with an A-style prose stop now**.

Treat the HARD STOP as binding. The iid Stouffer one-sided p=1.0 is not a technical degeneracy to reinterpret; it is exactly the predeclared global gate. The correct statement is: Algorithm 1 does not beat a prevalence-preserving null globally on the 12-pathogen panel. P2 and P3 remain valuable descriptive diagnostics, but not evidence for a global detector-agnostic or search-space-reduction claim.

Do **not** run P4 in Wave 1. Instead, close Wave 1 with Task 6 prose insertions that state:

- The 4-core is a historical benchmark, not a non-arbitrary optimum.
- The 3-core (`freq, entropy, homoplasy`) is the stronger compact descriptive comparator.
- Rank reliability is pathogen-specific: clear positive signal in a callable minority, flat or inverted behavior elsewhere.
- Null calibration removes the global claim: 5/12 pass iid locally, only Norovirus passes the strict local-burden null.
- Algorithm 1 is now framed as an exploratory cold-start prioritization heuristic pending a prospective abstention rule.

Then make the next experiment **P5: nested callability/abstention**, not P4.

## 3. Pre-Registered Callability Diagnostics

P5 must assign callable status inside each held-out-pathogen fold using **training pathogens only**. The held-out pathogen's P1 p-values, held-out observed MCC, held-out top-decile delta, or held-out null-adjusted enrichment must not be used to set thresholds or decide callability.

Use this protocol:

1. For each LOPO fold, fit the scoring signs on the 11 training pathogens exactly as in P1/P2/P3.
2. Within the 11 training pathogens, compute four diagnostics for the candidate method, preferably the 3-core and secondarily the historical 4-core.
3. Select thresholds from training pathogens only using leave-one-training-pathogen-out inner resampling. The thresholds below are fixed defaults unless the inner loop chooses stricter thresholds.
4. Apply the resulting rule once to the held-out pathogen.
5. Report performance separately for callable and abstained pathogens; abstentions count as no deployment, not as failures or successes.

Pre-register a pathogen as **callable** only if all four criteria pass:

| Diagnostic | Operational definition | Threshold |
|---|---|---|
| Top-decile score separation | Bootstrap 95% CI for Layer A prevalence in top score decile minus bottom score decile, computed on training-style resamples using the fold's fitted score | Lower CI bound **> 0.02** and point estimate **> 0.05** |
| Null-adjusted enrichment | Top-decile Layer A enrichment divided by the mean top-decile enrichment under an iid prevalence-preserving null, using 10,000 training-only permutations | Lower 95% bootstrap bound **> 1.10** |
| Perturbation stability | Jaccard overlap of top-10% ranked positions across 200 perturbations that jitter feature z-scores by training-estimated measurement noise and refit signs on bootstrap training pathogens | Median Jaccard **>= 0.60** and 10th percentile **>= 0.40** |
| Sparse-label red flag | Held-out pathogen has enough positive labels and rankable sites for decile and MCC estimates to be meaningful; this uses label count and sequence length only, not performance | At least **10 Layer A positives**, at least **200 rankable positions**, and Layer A prevalence between **1% and 20%** |

Add one guardrail: if the training panel shows evidence of inversion for the candidate rule, abstain. Operationally, if at least two training pathogens have top-vs-bottom bootstrap upper CI bound < 0, or the training median Spearman trend is <= 0, the method is declared **not callable for that fold family**.

Primary P5 endpoint:

- MCC and TP@50 on callable held-out pathogens only, with the number and identity of abstained pathogens reported in the same table.

Secondary P5 endpoint:

- Coverage-performance tradeoff: callable fraction, TP@50 among callable pathogens, and TP@50 if abstained pathogens receive random allocation.

This makes callability a deployment policy, not a retrospective label for the five P1-positive pathogens.

## 4. P4 Disposition

**Defer P4 to an expanded panel.**

Do not run P4 on the 12-pathogen panel as a headline claim. A detector-consensus result cannot rescue a method that failed the predeclared global null calibration. On this panel, P4 would be defensible only as a clearly labeled exploratory appendix, and even then it should not be restricted to the five P1-positive pathogens.

The defensible future P4 is:

- Run after P5 defines callability prospectively.
- Run on an expanded panel, ideally Tier 1 pilot plus Tier 2 features-only expansion toward n≈30.
- State the claim as conditional: "among prospectively callable pathogens, independent detector consensus enriches Layer A relative to matched nulls."

Current disposition: **skip P4 in Wave 1; defer to expanded-panel validation after P5**.

## 5. Defense-Readiness Risk Re-Scoring

New risk score: **medium-high** if the dissertation retains any global Algorithm 1 claim; **medium** if the HARD STOP language is adopted cleanly.

The risk increased from pre-execution because P1 invalidates the broadest claim: the 4-core does not beat even iid prevalence-preserving nulls globally, and the strict local-burden null leaves only Norovirus significant. P3 also weakens the fixed 4-core rationale, and P2 exposes one clear inversion case.

The risk is controllable because the negative result is coherent and predeclared. With the recommended edits, the defensible defense narrative becomes:

> Algorithm 1 is not a globally calibrated detector on the current 12-pathogen panel. It is an exploratory cold-start ranking heuristic with measurable signal in a prospectively definable callable subset, and the dissertation reports both the signal and the abstention problem transparently.

That is a defendable thesis. The unsafe thesis is any version of "Algorithm 1 is detector-agnostic, globally above null, or broadly reduces search space across pathogens."
