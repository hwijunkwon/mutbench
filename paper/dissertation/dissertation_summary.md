# MutBench: A Systematic Benchmark Framework for Viral Mutation Hotspot Detection

**Author:** Hwijun Han, Department of Computer Science

---

## One-Paragraph Summary

This dissertation presents MutBench, the first systematic benchmark framework for evaluating methods that detect mutation hotspots in viral genomes. By evaluating 9 scoring methods combined with 39 detection algorithms across 9 RNA viruses (3,159 total evaluations, 161 pages, 16 figures, ~32 tables, 76 references), the study provides statistical proof that no single detection method works best for all pathogens: all 9 viruses required different optimal method combinations, and the interaction between method and pathogen was the largest source of performance variance. Based on this finding, the author proposes PAHD (Pathogen-Adaptive Hotspot Detection), a proof-of-concept framework that selects detection strategies based on each pathogen's genomic profile. The work fills a gap in viral genomics where, unlike cancer genomics or machine learning, no standardized benchmark existed for comparing hotspot detection approaches.

---

## Dissertation Structure (v50, 161 pages, 16 figures, ~32 tables, 76 references)

- **Ch1:** Introduction
- **Ch2:** Related Work
- **Ch3:** Methodology — 4 sections: (1) Materials, (2) Benchmark Framework Design, (3) Scoring and Detection Methods, (4) Evaluation and Statistical Design
- **Ch4:** Results — 4 sections: (1) Single-Pathogen Analysis, (2) Robustness Analysis, (3) Cross-Pathogen Analysis, (4) 9-Pathogen Analysis
- **Ch5:** Discussion
- **Ch6:** Conclusion
- **39 detection methods** (from 14 algorithm families), **9 scoring methods**, **9 pathogens**
- **Contributions: exactly 2** (MutBench framework; statistical demonstration of pathogen-adaptive necessity)

---

## Background for CS Audience

### What is a virus genome?

A virus genome is a sequence of nucleotide bases (A, C, G, T/U) that encodes all the information the virus needs to replicate. SARS-CoV-2, for example, has approximately 30,000 bases. This sequence encodes multiple proteins, including the Spike protein (roughly 3,800 bases), which the virus uses to enter human cells.

### What is a mutation?

When a virus replicates, errors occur in copying the genome, changing one base to another at some position. RNA viruses like SARS-CoV-2, HIV, and influenza mutate at rates of 10^-3 to 10^-5 substitutions per site per year, which is fast enough that new variants emerge within months.

### What is a mutation hotspot?

A mutation hotspot is a genomic position or region where mutations accumulate far more frequently than expected by chance. These hotspots often correspond to sites under evolutionary pressure, such as positions where the virus is adapting to evade the human immune system or improve its ability to infect cells. Not all highly mutated positions are hotspots in a meaningful sense: some positions appear highly mutated simply because one lineage carrying that mutation became dominant (a "founder effect"), not because the mutation was independently advantageous.

### Why does it matter?

Accurately identifying hotspots has direct implications for vaccine design (which regions to target), antiviral drug development (which regions to avoid due to escape risk), and real-time surveillance (early detection of emerging variants). During COVID-19, positions like E484K and N501Y in the Spike protein were recognized as hotspots associated with immune evasion and increased transmissibility.

### What tools existed before MutBench?

Several approaches existed for scoring and detecting hotspots: frequency-based methods (counting how often each position mutates), entropy-based methods (measuring the diversity of mutation types), density-based clustering (DBSCAN, HDBSCAN), sliding windows, wavelet transforms, and kernel density estimation. Cancer genomics had well-established benchmarks comparing 26 detection methods against independent ground truth. Viral genomics had nothing comparable: each method was evaluated using its own data and criteria, making fair comparison impossible.

### The CS analogy

The situation before MutBench is analogous to evaluating machine learning classifiers without a standard dataset (like MNIST or ImageNet), without agreed-upon metrics (like accuracy, F1, or AUC), and without knowing whether a model trained on one data distribution will transfer to another. Researchers proposed new detection methods and claimed they worked, but there was no way to objectively compare them or predict which would work for a given pathogen. MutBench provides the equivalent of a standardized benchmark suite with defined ground truth, composite metrics, and cross-domain generalization testing.

---

## The Problem

This dissertation addresses three specific gaps.

**Gap 1: No standardized evaluation framework.** Existing methods reported performance using their own datasets and evaluation criteria. For example, MutClust (a prior work by the author's group) validated its results using bootstrap tests, which only confirm internal statistical significance but cannot verify whether detected clusters correspond to biologically meaningful regions.

**Gap 2: No independent ground truth.** Objectively evaluating detection results requires a ground-truth standard that is independent of the detection algorithm. In viral genomics, independently verifiable evidence sources existed (convergent evolution sites, structurally conserved regions, Deep Mutational Scanning experimental data), but no one had integrated them into a systematic ground truth framework.

**Gap 3: Unknown generalizability across pathogens.** All existing methods were tuned and tested on a single pathogen. Whether the best method for SARS-CoV-2 would also be the best for influenza, HIV, or norovirus had never been tested. This is a specific instance of the algorithm selection problem (Rice, 1976): given a pathogen with particular characteristics, which detection method should be applied?

---

## MutBench Framework

### 3-Layer Ground Truth

MutBench defines ground truth using three independent biological evidence layers, mitigating single-source bias:

- **Layer A (Positive selection sites):** Genomic positions where mutations arose repeatedly and independently in multiple lineages, indicating functional advantage. These are "True Positives" that detection methods should find. Sources: published convergent evolution studies for each pathogen. Example: E484K (glutamic acid to lysine at position 484) in SARS-CoV-2 arose independently in Alpha, Beta, Gamma, and Omicron lineages. (9--54 positions per pathogen.)

- **Layer B (Constrained sites):** Structurally essential positions under purifying selection, where mutations are removed because they destroy protein function. These are "True Negatives" that detection methods should not flag. Example: heptad repeat regions in the Spike protein that are critical for membrane fusion. (0--229 positions per pathogen.)

- **Layer C (DMS experimental fitness):** Positions where laboratory experiments (Deep Mutational Scanning) measured the functional impact of every possible amino acid substitution. Positions in the top 20th percentile of fitness effect are classified as functionally important. Available for 4 of 9 pathogens.

Three layers are needed because they capture fundamentally different aspects of mutational importance: Layer A captures evolutionary pattern, Layer B captures structural constraint, and Layer C captures functional effect. The Jaccard similarity between DMS-escape sites and convergent evolution sites is only 0.006, confirming near-complete independence.

### Hotspot-score Metric

The composite evaluation metric is defined as:

    hotspot-score = (recall + precision + stability) / 3

where stability is the mean Jaccard similarity between the full-data detection and 100 subsampling runs (80% position retention). This design reflects the practical requirement that a method with high accuracy but unstable results under data perturbation is less useful than a moderately accurate but reproducible method.

### Two-Stage Experimental Design

- **Stage 1 (Deep, single pathogen):** In-depth analysis on SARS-CoV-2 comparing 5 MutClust variants and 2 baselines using synthetic benchmark, real GISAID data, temporal generalization, parameter sensitivity, and multi-ground-truth evaluation. Primary metric: hotspot-score.

- **Stage 2 (Broad, 9 pathogens):** Large-scale evaluation of 9 scoring formulas combined with 39 detection methods from 14 algorithm families, applied to 9 RNA viruses (SARS-CoV-2, H3N2, Norovirus, HIV-1, Dengue, RSV, Influenza B, MERS, HCV) selected to cover diverse mutation rates, genome sizes, and evolutionary strategies. Total: 3,159 evaluations. Primary metric: Matthews Correlation Coefficient (MCC), which is robust to the extreme class imbalance inherent in hotspot detection (positive rates of 1--16%). A parameter variants table documents all detection method configurations, and a prior applications table summarizes existing literature for each method.

### Statistical Validation

Three-way ANOVA (omega-squared effect sizes, including residual omega-squared = 0.307), Friedman nonparametric test, Leave-One-Pathogen-Out (LOPO) cross-validation, BCa bootstrap confidence intervals, and permutation tests. SWAN artifact in LOPO is discussed.

---

## Key Results

### Stage 1: SARS-CoV-2 deep analysis

MutClust-Hybrid achieved the highest hotspot-score of **0.778** on synthetic data (precision 0.968, recall 0.659, stability 0.706), confirming that combining domain-specific seed detection with data-driven (HDBSCAN) boundary determination outperforms both pure domain-knowledge approaches (MutClust-Original: 0.638) and pure data-driven approaches (HDBSCAN-Auto: 0.604).

On real GISAID 2020--2021 data, a substantial performance gap appeared (MutClust-Hybrid F1 dropped from 0.785 to 0.123) due to sparse H-score distributions, though enrichment ratios remained 7-fold above random, confirming biological validity.

### Stage 1 to Stage 2: Rankings reverse

The best method on SARS-CoV-2 (MutClust-Hybrid) was outperformed on H3N2 by MutClust-Fixed (hotspot-score 0.661 vs. 0.577), demonstrating that method rankings are not stable across pathogens.

### ANOVA: Interaction is the dominant factor

Three-way ANOVA on 2,418 valid evaluations:

| Factor | omega-squared |
|---|---|
| detection family x pathogen | **0.285** (largest) |
| pathogen (main effect) | 0.260 |
| scoring x pathogen | 0.083 |
| scoring (main effect) | 0.027 |
| detection family (main effect) | 0.025 |

The interaction between detection method family and pathogen explains 28.5% of total variance, exceeding all main effects. By Cohen's benchmarks, omega-squared above 0.14 is a "large" effect. This means which method works best depends fundamentally on which pathogen you are analyzing.

### All 9 pathogens have different optimal combinations

No two pathogens share the same best scoring-detection combination. For example: SARS-CoV-2 prefers E*rare + CUSUM, H3N2 prefers E_only + SlidingTest, HCV prefers E_only + CUSUM (same scoring but different detection parameters), and so on. Oracle MCC ranges from 0.088 (MERS) to 0.549 (H3N2).

### Friedman test: Performance differences are significant

Friedman chi-squared = 42.44, p = 0.0015 (top 20 combinations across 9 pathogens as blocks). This rejects the null hypothesis that all top combinations are interchangeable.

### LOPO: Zero generalization

Leave-One-Pathogen-Out cross-validation: combination match rate **0/9**. The best combination selected from 8 training pathogens was never the best for the held-out pathogen. Mean generalization ratio: only 4.9% of oracle performance.

### ESM-2: Protein language model confirms the pattern

ESM-2 (a 650M-parameter protein language model) log-likelihood ratios ranked 1st for SARS-CoV-2 and MERS but 10th (last) for Norovirus and HIV-1. This confirms that even a fundamentally different scoring paradigm (deep learning on protein sequences vs. MSA-based statistics) does not escape the pathogen-dependence problem.

---

## PAHD Prototype

Pathogen-Adaptive Hotspot Detection (PAHD) is a proof-of-concept framework motivated by the 9-pathogen benchmark results. It formalizes the problem as an instance of Rice's algorithm selection framework: given a pathogen profile (alignment length, diversity ratio, ground truth density, etc.), predict the best detection strategy.

Two profile versions were tested: a v1 profile (8 genomic features) and a v2 profile (85 MSA-derived features). Using a Family-first strategy (first predict the best detection algorithm family, then select the best combination within that family), v1 achieved 5/9 positive MCC values (mean = 0.005, median = 0.014). The v2 profile improved mean MCC to 0.017 by eliminating pathological negative transfers, though with fewer positive cases (4/9). At coarser prediction granularity, family-level prediction recovered 48.3% of oracle performance, and scoring-level prediction recovered 57.7%.

**Honest assessment:** The knowledge base of n=9 pathogens is too small for reliable combination-level prediction (exact match rate: 0/9). Scaling to 20+ pathogens and transitioning to meta-learning regression models are necessary next steps.

---

## Additional Analyses

- **Phylogenetic correction:** Coalescent simulations demonstrated that H-score systematically conflates founder effects with positive selection (Spearman rho = -0.876 between H-score and independent mutational origins). TreeTime ML ancestral reconstruction achieved AUC = 1.000 for discriminating convergent from founder mutations. Validation on real GISAID sequences confirmed that H-score and homoplasy scores capture fundamentally different signals (rho = -0.107, p = 1.36 x 10^-4). A temporal mismatch was discovered: 2020-H1 sequences predate the convergent evolution ground truth, causing near-zero detection performance with homoplasy-based scoring on early pandemic data.

- **Region-overlap MCC:** Under position-exact evaluation, mean oracle MCC = 0.289. Relaxing to a +/-5 window increased this to 0.638, and +/-10 window (approximately one antigenic epitope) to 0.712. H3N2 reached MCC = 0.964 under +/-10, confirming that detections are spatially proximate to known functional sites even when not exactly overlapping.

- **Weight sensitivity:** MutClust-Hybrid maintained rank 1 in 71.9% (123/171) of all possible hotspot-score weight combinations, switching to HDBSCAN-Auto only in extreme recall-oriented regions (recall weight >= 0.60, precision weight <= 0.20).

- **H-score saturation:** By 2024--2025, all 1,273 Spike amino acid positions had nonzero H-scores (standard deviation only 0.098), eliminating discriminative power. This reveals that reference-based mutation scoring has a limited shelf life as viral populations diverge from the reference.

---

## Contributions

The dissertation presents exactly two research contributions:

1. **Contribution 1: MutBench Benchmark Framework.** MutBench introduced the first systematic benchmark framework for viral mutation hotspot detection, comprising a three-layer ground truth (Layers A/B/C), the hotspot-score composite metric, and a two-stage experimental design combining synthetic data analysis (Stage 1) with large-scale comparison across 9 RNA viruses (Stage 2).

2. **Contribution 2: Statistical Demonstration of the Necessity of Pathogen-Adaptive Method Selection.** Statistical analysis of the large-scale benchmark results established, through four independent lines of evidence, that no single best-performing method exists: (1) the detection family x pathogen interaction was the largest source of variance in ANOVA (omega-squared = 0.285), (2) all 9 pathogens exhibited unique best scoring-detection combinations, (3) the Friedman test confirmed that performance rankings systematically vary across pathogens (chi-squared = 42.44, p = 0.0015), and (4) LOPO cross-validation yielded 0/9 agreement. As a proof-of-concept application of these findings, the PAHD prototype demonstrated that genomic profile similarity can partially predict detection family preferences (v1: 5/9 positive MCC; coarser-granularity prediction recovered up to 57.7% of oracle performance). ESM-2 cross-paradigm validation further confirmed the pathogen-dependence finding from an entirely independent methodology (ranking 1st for SARS-CoV-2/MERS, last for Norovirus/HIV-1).

---

## Limitations and Future Work

- **Ground truth relies on published literature.** Full 3-layer ground truth (including DMS) is available for only 4 of 9 pathogens. Layer A construction criteria vary across pathogens (convergent evolution for some, hypervariable regions for others).
- **RNA viruses only.** The 9 pathogens cover major RNA virus families, but DNA viruses (HPV, HBV) with fundamentally different mutation rates and mechanisms have not been tested.
- **Phylogenetic non-independence not fully corrected.** Proof-of-concept simulations and TreeTime validation were conducted, but full integration of phylogenetic correction into the benchmark pipeline remains future work.
- **Synthetic-to-real performance gap.** Synthetic benchmarks overestimate absolute performance due to continuous background noise vs. real data sparsity (342 of 29,903 positions nonzero).
- **Position-exact evaluation is strict.** A detection one position away from ground truth counts as a false positive. Region-overlap analysis (MCC: 0.289 to 0.712 at +/-10 window) quantifies this conservativeness.
- **PAHD knowledge base too small.** n=9 pathogens is insufficient for reliable method prediction. Scaling to 20+ pathogens is the critical next step.
- **Indels excluded.** H-score captures only point mutations; insertions and deletions (e.g., del69-70 in Alpha) are invisible to the current framework.
- **GISAID sampling bias.** Geographic overrepresentation of high-income countries and temporal sequencing imbalances affect frequency-based scores.

---

## Key Takeaway

Before MutBench, researchers deploying viral hotspot detection had no quantitative basis for choosing among available methods. MutBench provides this basis and reveals a critical finding: the best detection method is not a property of the method itself but of the method-pathogen combination (28.5% of variance explained by their interaction). This means that applying a single fixed method across all pathogens, which is current standard practice, systematically underperforms. The path forward is pathogen-adaptive method selection, for which MutBench serves as both the evidence base and the evaluation platform.
