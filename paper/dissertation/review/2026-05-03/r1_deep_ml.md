# Risk-1 Deep ML / VEP-PLM Rebuttal Script

## Opening question

**ML expert:** "The negative result may simply show that your labels/features/models are weak, not that cross-pathogen detection is unlearnable. Also, EqualWeight and 4-core heuristics are not modern adaptive learning."

**Why hard.** This is the strongest attack because it targets the causal interpretation of the thesis: a negative LOPO result can be explained by label noise, weak features, underpowered models, poor representation, or a real cross-pathogen barrier. The reviewer also knows that EqualWeight is a baseline, not a modern learner, and will resist any rhetoric that treats a failed heuristic as proof of impossibility.

**Best rebuttal.** I would not claim "unlearnable in principle." The bounded claim is that a deployable cross-pathogen detector is not supported at the current panel size under this audited region-level label, feature, and validation regime: 10 information types, 20 scoring formulas, 39 detector variants, the full 1023-subset lattice, HBFWS hierarchical Bayesian weighting, and six Cycle 7B adaptive paradigms all fail to produce a reliable held-out-pathogen rule. The positive result is therefore a benchmarked boundary result: there is real within-pathogen and oracle signal, but the information type needed is pathogen-dependent and label-provenance dependent.

## Follow-up questions

### 1. Meta-learning / fine-tuning

**Quote.** "Did you try meta-learning or fine-tuning across pathogens?"

**Why hard.** A VEP/PLM reviewer will see the benchmark as a natural few-shot or meta-learning problem: train across pathogens, adapt to a new pathogen, and use shared protein-language representations. If the answer is merely "no," the negative result sounds like a methods gap.

**Best rebuttal.** The benchmark did test the model-class boundary that is feasible for this label geometry: HBFWS hierarchical Bayesian shrinkage plus Cycle 7B XGBoost, Random Forest, sparse logistic regression, 1-NN algorithm selection, phylogenetic HBFWS, and rank aggregation under nested LOPO. All failed to beat EqualWeight-4core, with the best adaptive Wilcoxon result still non-significant, so the limiting factor is not just lack of a flexible weighting rule. True neural meta-learning is outside the dissertation's scope because the supervision is per-position region-level, not dense per-variant DMS labels; with 11 pathogens and 9--54 positives each, it would be more likely to learn label provenance and protein-family artifacts than a deployable cross-pathogen decision rule.

### 2. ESM-2 fine-tuning

**Quote.** "Why not use ESM-2 fine-tuning on Layer A pooled across pathogens?"

**Why hard.** ESM-2 is a modern representation, and pooled fine-tuning sounds like the obvious fix for a weak hand-engineered feature set. The reviewer may view masked-marginal ESM-2 and semantic-change features as too shallow compared with end-to-end adaptation.

**Best rebuttal.** The thesis deliberately evaluates region-level hotspot detection, whereas ESM-style VEP fine-tuning is strongest when labels are variant-level and densely assayed. Pooling Layer A across pathogens would mix different proteins, lengths, prevalence rates, curation standards, and biological mechanisms, so a fine-tuned model could optimize the training labels while worsening the held-out-pathogen problem the dissertation is testing. Within the audited representation space, ESM-2 masked marginal scores and semantic-change embeddings were included, and the full-lattice/Shapley audit found ESM-2 LLR negative on average under cold-start LOPO; that does not falsify future PLM fine-tuning, but it does show that adding PLM signal did not dissolve the region-level cross-pathogen barrier here.

### 3. Multicollinearity / feature-ablation artifacts

**Quote.** "Cycle 7B failures could be feature-ablation artifacts -- did you control for multicollinearity?"

**Why hard.** The feature table explicitly contains correlated channels: frequency, entropy, and dN/dS are highly correlated, and the Tranception proxy is highly correlated with ESM-2 for most pathogens. A reviewer can argue that adaptive learners failed because redundant or collinear inputs destabilized selection.

**Best rebuttal.** The dissertation treats that as an audit target, not an afterthought. It reports the feature correlation structure, separates the production EqualWeight column from nested-LOPO sign fitting, tests leave-one-feature-out, 4-of-10 exhaustive subsets, the full 1023-subset lattice, and Shapley values; the result is not "all features are equally useful," but that homoplasy, frequency, and entropy are the stable positive contributors while PLM and some structural channels are noise on average. Cycle 7B then tests multiple model classes on this same region-level problem; their convergent failure is therefore not explained by a single collinear ablation design.

### 4. ProteinGym / VEP transfer

**Quote.** "ProteinGym shows VEP works at protein level. Why doesn't your benchmark inherit that?"

**Why hard.** ProteinGym, EVE, EVEscape, Tranception, and ESM-based VEP have strong reputations. The reviewer may infer that if VEP works on proteins, then a poor MutBench result indicts the benchmark rather than the feasibility of learning.

**Best rebuttal.** ProteinGym primarily evaluates per-variant effect prediction against protein-specific experimental measurements; MutBench asks whether sparse, literature-curated, per-position region labels can be detected across unrelated viral pathogens. Those are different supervision regimes. The dissertation does inherit VEP information as ESM-2, semantic-change, and EVEscape-style channels, but the tested endpoint is not "does a mutation disrupt a protein" -- it is "does a position belong to an externally curated hotspot region under a held-out-pathogen protocol." The negative result says that VEP success at protein level does not automatically transfer to cross-pathogen region-level deployability.

## Trap questions

### 1. Multi-task PLM neural net

**Quote.** "Have you tried protein-language-model embeddings as inputs to a multi-task neural net trained on all 11 pathogens jointly?"

**Honest answer.** No. That is a reasonable future experiment, but it is outside the defended claim because the current labels are sparse per-position region annotations across only 11 pathogens, not dense per-variant labels suitable for neural multi-task learning. The dissertation's claim is narrower: among the audited region-level representations and adaptive paradigms feasible for this panel, including ESM-2 and semantic embedding channels, no method met the held-out-pathogen callability bar.

**Scope guardrail.** I would explicitly frame a multi-task PLM as a next-generation benchmark once the panel reaches roughly 20--30 independent pathogen targets and label provenance is harmonized. At the present size, it would be an exploratory model, not evidence that the current negative result is wrong.

### 2. Wave 5 label-provenance challenge

**Quote.** "How does Wave 5 Layer A' negative result not just show your feature pipeline is wrong, not that labels are non-interchangeable?"

**Honest answer.** Wave 5 cannot prove the feature pipeline is universally correct. What makes it informative is the controlled direction of failure: the same feature-compatible pipeline on reviewed UniProt-derived Layer A' targets produced mean MCC = -0.055, only 2/10 positive folds, and a sign for freq/entropy that was stable but opposite to the literature-curated Layer A panel, with a cross-panel Welch p = 0.0089. A random feature-pipeline failure would more likely produce noisy collapse; the sign-flipped MCC points to label provenance as the bottleneck.

**Scope guardrail.** The claim is not that UniProt annotations are wrong. The claim is that Layer A and Layer A' are not interchangeable supervision targets for this benchmark: one encodes literature-curated hotspot evidence, the other encodes structured database feature annotations, and swapping them changes the learned direction of association.

## Strongest deduction

**Most likely deduction: F, novelty.** Prof 06 is likely to say the thesis does not introduce a modern ML method and that EqualWeight/4-core are heuristics. A secondary deduction could hit D, scale, because 11 pathogens is small for cross-pathogen supervised learning, family-level random effects, and meta-learning.

**Rebuttal anchor.** The anchor that converts this from "should not pass" to "pass with caveats" is: **audited finite-panel boundary result**.

That phrase shifts the evaluation criterion away from "new universal VEP learner" and toward a defensible empirical contribution: MutBench tests a broad representation and detector lattice, shows that oracle signal exists, shows that adaptive weighting fails under nested held-out-pathogen validation, and identifies label provenance plus panel size as the current blockers. The thesis should concede that it is not a PLM fine-tuning paper and not a proof of biological impossibility; it is a benchmarked non-deployability result with practical retrospective triage value.

`RESULT_R1_DEEP_ML: anticipated_score=7.4/10 most_at_risk_item=F rebuttal_anchor="audited finite-panel boundary result"`
