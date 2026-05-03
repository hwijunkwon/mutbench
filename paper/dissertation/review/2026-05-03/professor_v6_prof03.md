# Professor 3: Statistics/ML (strictness=high)

## Scores
A: 8.0
B: 8.0
C: 7.0
D: 8.0
E: 7.0
F: 8.0
G: 7.0
H: 8.0
I: 9.0
J: 7.0
total: 77.0/100

## Rationale (≤3 sentences each item)
A: The problem is sharply framed as region-level, single-position hotspot detection rather than per-variant fitness prediction, and the dissertation consistently distinguishes this scope from ViroGym/EVEREST/ProteinGym-style tasks. The statement is strongest where it ties the benchmark gap to algorithm selection and practical search-space reduction. The main deduction is that "hotspot" remains an operationally plural construct, so the problem definition depends heavily on accepting Layer A/C/B as separate proxies rather than one target.

B: The related-work section is broad and current, covering viral surveillance, density clustering, HyPhy selection methods, DMS, VEP benchmarks, and benchmark-bias methodology. It correctly positions MutBench as complementary to variant-effect benchmarks and does not overstate direct comparability. The deduction is for density and occasional overextension: some references are used more as positioning scaffolds than as a rigorous competing-method taxonomy.

C: The methodology is ambitious and unusually well-audited: 20 scoring formulas, 39 detector variants, three ground-truth layers, MCC-based Stage 2 analysis, cluster-bootstrap intervals, counterfactual nulls, LOPO, Friedman/Nemenyi, feature-ablation, and multiple negative audits. However, the core statistical design is still constrained by 11 pathogen clusters, heterogeneous Layer A construction, one-team curation, correlated scoring channels, retrospective top-pick selection over 780 combinations, and input-quality confounding across pathogens. The work is defensible as a within-panel benchmark, but not yet strong enough methodologically for deployable adaptive selection or causal claims about pathogen biology versus label/input provenance.

D: The experimental grid is large for the stated task: 8,580 evaluations across 11 RNA-virus surface glycoproteins, plus Stage 3 and wave-style robustness analyses. The scale is meaningful in evaluation-cell count and feature breadth, but the true independent unit for cross-pathogen inference is small. The active scope is also bounded to surface-glycoprotein substitutions and cannot support claims about noncoding regions, indels, recombination, DNA viruses, or general pathogen systems.

E: The interpretation is generally careful: LOPO 0/11 is explicitly called null-consistent, Friedman p=0.990 is not oversold, SARS-CoV-2 escape is exploratory, H3N2 is self-consistency, and HIV-1 is correctly made the primary external anchor. Still, the narrative sometimes leans on top-1 enrichment and "practical search-space reduction" language more strongly than the broader negative evidence warrants, especially given 3/11 escape-validation availability, 0/12 callability, and grand-mean prospective AUROC near chance. The best interpretation is retrospective prioritization within this panel, not a general predictive detector.

F: The contribution is novel in benchmark framing: a region-level viral hotspot-detection benchmark decomposing biological information source by pathogen is a clear contribution distinct from fitness-regression benchmarks. The scoring-by-pathogen interaction, external escape audit hierarchy, and explicit negative gates add originality beyond simply running many algorithms. The deduction is that several algorithmic components are conventional, and the strongest novelty is infrastructural/evaluative rather than a new statistically validated predictor.

G: Practical value is real but bounded: the HIV-1 Layer-A-disjoint escape enrichment is a credible retrospective anchor, and a ranked short list can reduce experimental screening burden. The cold-start and adaptive-selection claims are appropriately restrained by the 0/12 callability result, seven adaptive-weighting failures, and weak prospective transfer. Therefore the practical value is useful for retrospective triage and hypothesis generation, not for operational surveillance deployment.

H: The dissertation is unusually explicit about panels, denominators, Bonferroni scopes, provenance files, and which statistics are load-bearing. The clarity benefits from evidence ledgers and limitations matrices, but the manuscript is dense and sometimes repeats the same caveats across abstract, results, and discussion. Some readers may struggle to track shifting panels (11 main, 12 Stage 3, 28 Wave 4, 10 Layer A') and protocol differences unless they read very carefully.

I: Limitations awareness is the strongest dimension. The dissertation directly names label heterogeneity, circularity, winner's curse, small-cluster inference, prospective-validation failure, MAFFT/input heterogeneity, PLM leakage, sublineage pooling, dual-use risk, and external reproduction limits. It also reports negative results rather than hiding them, including HBFWS p=0.78, Cycle 7B failures, Wave 4 p=0.368, and Layer A' MCC=-0.055.

J: Overall maturity is solid for a dissertation benchmark but not excellent under a strict Statistics/ML standard. The work has a mature audit culture and careful claim calibration, yet its central inferential unit remains a small, heterogeneous pathogen panel with non-independent labels and retrospective validation. It is ready as a rigorous within-panel benchmark contribution, but the next maturity step is independent recuration/reproduction and a larger time-forward external panel.

## Critical concerns (if any item < 6)
None.

## Strongest single deduction
C: methodology is limited by only 11 independent pathogen clusters plus heterogeneous Layer A label provenance; fix by adding an independently rec-curated 20-30+ pathogen panel with time-forward validation and the same predeclared callability gates.

RESULT_PROF_V6_03: total=77.0/100 min_item=7.0(C,E,G,J) max_item=9.0(I)
