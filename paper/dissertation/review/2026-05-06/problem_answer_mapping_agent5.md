# Problem-Answer Mapping Audit

## Problem 1: Standardized framework
**Where answered**: Ch3 framework overview and 3-layer ground truth define the infrastructure; Ch4 Stage 2 applies it at scale; Ch5 explicitly bounds standardization. Key locations: `ch3_methods.tex` framework overview; `ch3_methods.tex:186-219`; `ch4_results.tex:225-226`, `331-373`; `ch5_discussion.tex:121`, `193`, `217`.

**Quoted answer**: Ch3 states that "Layer~A (literature-curated adaptive/diversifying positions) defines true positives for MCC computation, Layer~B (purifying selection) defines constrained negatives for constrained FPR, and Layer~C (DMS fitness) provides experimental validation" (`ch3_methods.tex:186`). It also states that Layer A's "operational contract is therefore evidence-based rather than algorithmic" (`ch3_methods.tex:216`) and that the Layer A union is "a limitation rather than a single computational construct" (`ch3_methods.tex:219`). Ch4 applies the standardized grid: "8,580 evaluations (20 scoring formulas x 39 detection parameter variants from 14 families x 11 pathogens)" (`ch4_results.tex:225` context). Ch5 summarizes: the framework is "designed for standardised use, pending external benchmarking by independent teams" (`ch5_discussion.tex:121`).

**Strength**: Partial. The dissertation establishes a standardized *benchmark procedure* (fixed scoring grid, detector grid, metrics, three-layer roles, preregistered thresholds), but not a fully standardized biological ground-truth instrument. The strongest internal caveat is Ch5: "Layer~A is intentionally heterogeneous across pathogens... the interaction claim is therefore a claim about relative method rankings under real curation heterogeneity" (`ch5_discussion.tex:193`). The prior curation audits sharpen this: Agent 1 estimates 55-65% of the interaction may be curation-protocol-dependent; Agent 3 estimates a 46% curation share and shows homogeneous-curation subset omega values (0.160 weighted estimate) below the 0.296 headline.

**Strict-reviewer counter-argument**: "You standardized the computation, not the target. HCV region labels, HIV variable-loop labels, antigenic-site labels, VOC point labels, and immune-escape lists are not one measurement system. A framework whose primary positives are 46-60% protocol-dependent cannot be claimed as a standardized biological evaluation framework without stronger scoping."

**Recommended action**: C. Keep the broad motivation, but add a Ch1 scope-bounding paragraph. Suggested text:

> MutBench standardizes the computational evaluation contract--input features, detector grid, metrics, and reporting--while deliberately treating Layer A as a literature-curated operational hotspot definition rather than a single homogeneous biological assay. Thus, the framework answers the standardization gap at the benchmark-procedure level, but its biological labels remain bounded by pathogen-specific curation conventions that are audited in Chapters 4-5.

## Problem 2: Independent ground truth
**Where answered**: Ch3 defines Layer A/B/C and explicitly says Layer C is experimental; Ch4 shows multiple ground truths change method ranking and reports vaccine-escape overlap; Ch5 discusses circularity, Layer A provenance, curation reproducibility, DMS/vaccine validation. Key locations: `ch3_methods.tex:190-242`; `ch4_results.tex:46-58`, `906-949`; `ch5_discussion.tex:16-19`, `48-49`, `127`, `137-145`.

**Quoted answer**: Ch3 says the layers capture "literature-supported adaptation, structural constraint, and direct experimental fitness effect" (`ch3_methods.tex:190-191`), with Layer C as "direct experimental measurements" (`ch3_methods.tex:240-242`). Ch4 shows why a single ground truth is inadequate: "DMS--convergence Jaccard similarity was only 0.006, and the leading method changed by reference set... so a single ground truth would bias the benchmark" (`ch4_results.tex:46`). Ch5 states the strongest defense and limitation: "Layer~C (DMS experimental fitness) is used where available (6 of 11 pathogens), and the vaccine escape enrichment analysis... provides partial external cross-validation" (`ch5_discussion.tex:19`). It also concedes no "duplicate independent recuration subset, inter-annotator agreement statistic, or adjudicated disagreement log" (`ch5_discussion.tex:49`).

**Strength**: Partial. The dissertation provides independent *evidence axes*, especially DMS Layer C and HIV-1 vaccine escape, but Layer A itself is not independent in the strict sense. It is a single-team literature synthesis, dominated by immune-escape tags, with region-derived labels for some pathogens. Ch4's vaccine-escape audit is strong for HIV-1 (82% Layer-A-disjoint, novel-only significant), but H3N2 is self-consistency and SARS-CoV-2 exploratory (`ch4_results.tex:937-949`). Layer C covers 6/11 pathogens, not the full benchmark panel.

**Strict-reviewer counter-argument**: "Your primary MCC ground truth is Layer A, and Layer A is not independently curated by another team or generated by a uniform assay. Layer C and HIV-1 escape validate parts of the story, but they do not convert the main 11-pathogen Layer A benchmark into an independent ground truth framework."

**Recommended action**: C. Apply the user framing that hotspot is comprehensive and fluid, but only as a scoped design rationale. Suggested text:

> Layer A is intentionally comprehensive and fluid: it captures the best available pathogen-specific literature signal, including convergent evolution, immune escape, and hypervariable-region membership. This heterogeneity is a feature for operational triage, because different viruses become "hotspots" through different observable evidence streams; it is not a claim that Layer A is a uniform independent assay. Independence is supplied partially by Layer C DMS and by Layer-A-disjoint vaccine-escape audits, with HIV-1 as the strongest external anchor.

## Problem 3: Pathogen-dependence statistical evidence
**Where answered**: Ch4 ANOVA, LOPO, Friedman, heterogeneity analyses; Ch5 cross-pathogen generalization and limitations. Key locations: `ch4_results.tex:331-427`, `861-893`; `ch5_discussion.tex:68-72`, `121`, `193`, `214`, `217`, `227`.

**Quoted answer**: Ch4 reports "scoring x pathogen interaction ($\omega^2 = 0.296$) is the largest single modeled source" (`ch4_results.tex:338`, table at `345`) and notes the conservative cell-level estimate (`ch4_results.tex:367`). Ch4 also states the three lenses are "consistency checks on the same data, not independent replications" (`ch4_results.tex:371`) and that the finding provides evidence "within the 20-type/39-variant design" (`ch4_results.tex:373`). LOPO is carefully bounded: 0/11 is "not evidence against universality" alone, and the 0.265 gap has weak null separation (`ch4_results.tex:421-425`). Ch4's heterogeneity paragraph says benchmark behavior is driven by "some combination of pathogen biology, curation protocol, auxiliary input quality, and their interaction... without isolating any single component as causal" (`ch4_results.tex:893`).

**Strength**: Partial. The manuscript does quantify method-performance dependence on pathogen identity under the current benchmark labels. It does not cleanly quantify *biological pathogen-dependence* separate from curation-protocol-dependence. Agent 3's homogeneous-curation subsets materially attenuate the headline (weighted omega about 0.160 vs 0.296; curation share about 46%). Agent 2 correctly says the current best defense is "not purely HCV and not erased by immune-escape restriction," not "biology rather than curation protocol."

**Strict-reviewer counter-argument**: "$\omega^2=0.296$ is a benchmark interaction, not a clean pathogen-biology interaction. Because Layer A label logic differs by pathogen and many winners are predictable from curation philosophy, the statistic conflates biology, label provenance, input quality, and method behavior."

**Recommended action**: C, with optional body addition. Ch1 should say the dissertation quantifies pathogen/protocol-dependent benchmark performance, not pure biology. Add in Ch4/Ch5:

> The $\omega^2$ interaction should be read as pathogen-dependent information utility under the literature-curated Layer A contract. It is not a causal partition of biology versus curation protocol; homogeneous-curation and immune-escape-only sensitivity analyses bound, but do not eliminate, that confounding.

## Cross-problem coherence check
The current story is coherent if framed as: MutBench standardizes the evaluation *procedure*, uses a deliberately comprehensive and fluid literature-curated Layer A as the primary operational target, then checks that target with independent axes where available (Layer C DMS and vaccine escape), and quantifies method-pathogen dependence under that contract.

The story becomes internally overclaimed only if Ch1 is read as promising: (1) a homogeneous standardized biological ground truth, (2) fully independent validation for all pathogens, and (3) pathogen-biology-only statistical attribution. Ch3-Ch5 already contain many caveats, but Ch1's problem statements are cleaner and stronger than the body can fully satisfy.

The user-supplied "hotspot is comprehensive AND fluid" framing should be used for Problem 2, but carefully: Layer A heterogeneity is a feature for operational hotspot triage, not a defect, as long as the dissertation stops short of calling it a uniform independent assay.

## Final recommendation
- (c) Hybrid: scope-bounding paragraph + body additions.

Do not rewrite the entire Ch1 motivation downward. The three problems are real and the dissertation answers them materially. But Ch1 should add an explicit scope paragraph after the three problems or after Objectives:

> Scope of the answers. This dissertation fully standardizes the computational benchmark contract (features, detector grid, metrics, and reporting), but the biological target remains an operational literature-curated hotspot definition. Layer A is comprehensive and pathogen-specific rather than assay-homogeneous; Layer C DMS and vaccine-escape audits provide independent validation where data exist, with HIV-1 as the strongest Layer-A-disjoint external anchor. Accordingly, the reported pathogen-dependence quantifies method performance under real literature-curation heterogeneity and cannot by itself partition pathogen biology from curation protocol.

Add a short Ch4/Ch5 body sentence explicitly incorporating the Agent 3 result if it is allowed into the dissertation: homogeneous-curation subset omega estimates attenuate the headline, supporting a nontrivial curation-protocol component while preserving a residual interaction.

RESULT_PROBLEM_ANSWER_AGENT5: p1_strength=P p2_strength=P p3_strength=P recommended_action=c ch1_rewrite_needed=yes
