# Risk Analysis 1 -- Generalization-Impossibility Reframe

## 1. Defensibility verdict

**Verdict: defensible with specific guardrails.** A committee can accept the reframe if the thesis says: "MutBench is a retrospective wet-lab triage benchmark, and its negative audits show that a deployable cross-pathogen adaptive detector is not supported at the current panel size (`n=11`) under the tested feature, label, and validation regime." That is a defensible negative contribution because it converts repeated failures (LOPO 0/11, Friedman `p=0.990`, HBFWS `p=0.78`, Cycle 7B all-fail, Wave 4/5, `0/12` callable) into a bounded impossibility/boundary result. It becomes face-saving if stated as "we proved generalization is impossible" without the scope qualifiers. The current dissertation is close to the acceptable version: it anchors Contribution 2 in the scoring-by-pathogen interaction (`omega^2=0.296`, lower-bound category aggregation `0.103`) and treats LOPO as corroborative, not standalone proof. The weakest committee risk is practical value: the v6 aggregate already shows `G=6.80`, with field/practice reviewers penalizing the gap between retrospective enrichment and deployable callability.

## 2. Three strongest committee pushbacks

**Statistician pushback.** "You have 11 pathogen clusters. You cannot prove non-learnability or a panel-size threshold from 11 units; the cluster bootstrap and random-effects interpretation are underpowered or anti-conservative."

**Best rebuttal.** Agree with the statistical boundary, then narrow the claim: "Correct; this is not a theorem over all future panels. The contribution is an audited finite-panel boundary: five inferential frames identify pathogen-dependent information utility, while seven adaptive paradigms and the predeclared callability rule fail at `n=11`. The 20--30 pathogen target is therefore a design requirement for the next study, consistent with mixed-model guidance that random-effect variance estimation becomes unstable with few levels and is more credible around 20--30 levels." Cite Bolker's GLMM guidance as a rule-of-thumb, not a formal threshold: <https://bbolker.github.io/stat4c03/notes/glmm.html>.

**Biologist pushback.** "This sounds like a computational exercise. If `0/12` folds are callable, why should a wet-lab group care?"

**Best rebuttal.** Do not defend deployment. Defend prioritization economics: "MutBench is not a replacement for DMS, neutralization assays, or epitope mapping. It is a screening-budget allocator. In HIV-1, the Layer-A-disjoint escape audit narrows roughly 1,000 positions to 10--50 candidates with `7.16--8.24x` enrichment after Bonferroni correction. That is a legitimate wet-lab triage outcome even when calibrated prospective detection is not yet supported." Keep H3N2 as self-consistency and SARS-CoV-2 as exploratory; make HIV-1 the only primary external-practical anchor.

**ML expert pushback.** "The negative result may simply show that your labels/features/models are weak, not that cross-pathogen detection is unlearnable. Also, EqualWeight and 4-core heuristics are not modern adaptive learning."

**Best rebuttal.** Separate "unlearnable in principle" from "not learnable from this panel with these audited representations": "The claim is not that no representation can ever work. The dissertation tested a broad region-level lattice: 10 information types, 20 scoring formulas, 39 detector variants, full-lattice subset audit, HBFWS, Cycle 7B, and Wave 4/5 sensitivity. The consistent failure of adaptive selection despite detectable within-panel oracle signal establishes a sample-size and label-provenance bottleneck. The positive ML contribution is benchmarked algorithm-selection evidence, not a new universal learner." Anchor in Rice's algorithm-selection framing and No-Free-Lunch intuition only as explanatory theory, not as proof of the empirical claim.

## 3. Comparable theses/papers

**Successful comparable 1: No-Free-Lunch / algorithm-selection work.** Wolpert and Macready's No Free Lunch theorem and follow-on benchmark work are accepted contributions because they formalize when universal optimizer claims fail rather than proposing a better optimizer. MutBench can borrow this rhetorical shape, but must stay empirical and scoped: pathogen-specific signal landscapes, no universal scoring-detector winner, and a larger-panel requirement. Useful citations: Wolpert & Macready, 1997, "No Free Lunch Theorems for Optimization"; Duenyez-Guzman and Vose, 2013, "No Free Lunch and Benchmarks," *Evolutionary Computation*, DOI `10.1162/EVCO_a_00077` (<https://direct.mit.edu/evco/article/21/2/293/984/No-Free-Lunch-and-Benchmarks>).

**Successful comparable 2: negative-data infrastructure in computational biology.** Youngs et al. built NoGO around the absence and importance of negative examples for protein function prediction. The contribution is not a high-performing predictor; it is an enabling benchmark/data resource that clarifies why supervised learning is limited without the right labels. MutBench is analogous if framed as benchmark plus label/provenance boundary plus triage utility. Citation: Youngs, Penfold-Brown, Bonneau, and Shasha, 2014, "Negative Example Selection for Protein Function Prediction: The NoGO Database," *PLOS Computational Biology*, DOI `10.1371/journal.pcbi.1003644` (<https://journals.plos.org/ploscompbiol/article?id=10.1371/journal.pcbi.1003644>).

**Failed cautionary comparable: Google Flu Trends as overclaimed deployment.** Google Flu Trends is the cautionary example because a promising predictive tool was treated as operational surveillance despite opacity, drift, and overfitting; Lazer et al. report large avoidable errors and frame it as "big data hubris." MutBench avoids this failure only if it refuses deployable-detector language until time-forward/callability gates pass. Citation: Lazer, Kennedy, King, and Vespignani, 2014, "The Parable of Google Flu: Traps in Big Data Analysis," *Science* 343:1203--1205, DOI `10.1126/science.1248506` (<https://gking.harvard.edu/publications/parable-google-flu%C2%A0traps-big-data-analysis>).

## 4. Specific text-level guardrails

- Always pair "not learnable" with "at `n=11`, under the tested labels/features/validation regime."
- Always pair "cross-pathogen detector" with "deployable/adaptive/prospective"; otherwise readers may think the dissertation denies retrospective pathogen-dependent signal.
- Never say "proved generalization is impossible"; say "the current evidence falsifies a deployable universal detector claim at this panel size."
- Never let LOPO 0/11 stand alone. Pair it with `omega^2_scoring x pathogen = 0.296`, Friedman `p=0.990`, oracle-vs-generalized MCC gap, and adaptive-audit failures.
- Always pair "wet-lab triage" with the quantitative search-space economics: `~1,000 -> 10--50` candidates and HIV-1 `7.16--8.24x` Layer-A-disjoint escape enrichment.
- Keep "MutBench benchmark" as Contribution 1 and "pathogen-dependent information utility" as Contribution 2; "triage tool" should be practical impact, not the whole thesis.
- Treat the 20--30 pathogen threshold as a design target/rule-of-thumb, not an empirically estimated phase transition.
- Keep H3N2 and SARS-CoV-2 secondary: H3N2 has high Layer-A overlap; SARS-CoV-2 is exploratory. Do not distribute the HIV-1 strength across all pathogens.
- Replace "falsification-resistant evidence" with "convergent negative audits" when speaking to statisticians; the former can sound rhetorical.
- Use "retrospective prioritization heuristic" for Algorithm 1 unless the abstention rule calls on an externally validated expanded panel.

## 5. Net result

`RESULT_RISK1: verdict=guarded primary_concern="The reframe is acceptable only if impossibility is stated as a bounded finite-panel non-deployability result, while practical value is anchored in HIV-1 wet-lab triage enrichment rather than prospective detector callability."`
