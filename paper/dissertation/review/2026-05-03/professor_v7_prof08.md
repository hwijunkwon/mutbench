# Professor 8: Practice/field user (strictness=high)

## Scores
A: 8.0
B: 7.5
C: 7.0
D: 8.0
E: 8.0
F: 7.5
G: 6.0
H: 6.5
I: 9.0
J: 7.0
total: 74.5/100

## Rationale (<=3 sentences each item)
A: The problem is well framed around a real practice gap: field users need residue-level triage, not another retrospective lineage tracker or per-variant fitness benchmark. The dissertation is strongest when it states the practical contract as search-space reduction under a single-position RNA-virus surface-glycoprotein regime. The deduction is that the problem statement still oscillates between benchmark science, adaptive method selection, and cold-start deployment, so a field reader must work to identify the actual use case.

B: The related-work coverage is broad and current, spanning surveillance platforms, cancer hotspot methods, DMS, PLMs, VEP benchmarks, and algorithm-selection theory. It usefully distinguishes MutBench from ProteinGym, EVEREST, ViroGym, Nextstrain, PANGO, and MutClust. The deduction is that the review is sometimes encyclopedic rather than decision-oriented, and coupling-aware/epistatic methods remain mostly scoped out rather than evaluated against the practical task.

C: The methodology is ambitious and mostly reproducible: 3-layer ground truth, 20 scoring formulas, 14 detection families, MCC, omega-squared ANOVA, LOPO, Friedman, escape enrichment, and multiple robustness audits are all explicitly specified. However, Layer A is a heterogeneous literature union, several channels are proxies or highly collinear, MAFFT/structure/input quality are pathogen-confounded, and the effective independent unit is closer to 3,080 cells or 11 pathogen clusters than 8,580 rows. From a field-user standpoint, the method is credible as a retrospective benchmark, but not yet as a deployable operational protocol.

D: The 11-pathogen, 8,580-evaluation scale is substantial for a region-level viral hotspot benchmark, and the panel covers useful diversity in surface proteins, sequence depth, and evolutionary regimes. The practical validation scope is much narrower: vaccine-escape enrichment is available for only 3/11 pathogens, with HIV-1 as the only clean external anchor. Prospective evidence is especially limited because the 73-window backtest is near chance overall and the callability rule refuses all folds.

E: The interpretation is unusually careful: LOPO 0/11 and Friedman p=0.990 are correctly downgraded to null-consistent corroboration, while the omega-squared interaction and HIV-1 escape audit carry the main positive evidence. The manuscript also distinguishes H3N2 self-consistency from HIV-1 external validation and treats SARS-CoV-2 as exploratory. The deduction is that some headline language still risks sounding stronger than the evidence, especially around "practical workflow" and family-level scoring priors.

F: The benchmark contribution is novel in the region-level hotspot-detection niche, especially the pathogen-by-information interaction analysis and the explicit audit ledger. The strongest original element is not a new detector but a disciplined demonstration that information-source utility varies by pathogen under a standardized grid. Novelty is reduced by reliance on existing feature families, proxy implementations, and a retrospective validation regime.

G: Practical value is real but bounded: HIV-1 7.19x enrichment and Layer-A-disjoint novel-only significance show that MutBench can reduce candidate lists for wet-lab triage. For field use, the major blockers are that prospective performance is weak, adaptive selection is not learnable at n=11, external escape validation covers only 3 pathogens, and the predeclared abstention rule gives 0/12 callable folds. The current output is a research triage aid, not an operational surveillance or vaccine-strain decision tool.

H: The manuscript is transparent but hard to use: it contains many ledgers, caveats, repeated numeric distinctions, and version/cycle audit terminology that obscure the field-facing takeaway. The abstract and discussion are much clearer than the middle chapters, but a practitioner would still need a short "what to run, when to abstain, what not to claim" page. Clarity is penalized because the document often protects against objections instead of guiding adoption.

I: Limitations awareness is excellent. The dissertation openly names label heterogeneity, circularity, winner's curse, small-cluster inference, PLM/proxy collinearity, prospective failure, dual-use risk, MAFFT artifacts, and failed adaptive weighting attempts. The only deduction is that some limitations are so numerous and distributed that they weaken rather than sharpen the actionable boundary.

J: Overall maturity is solid for a dissertation benchmark: the work is numerically rich, internally audited, and careful about not overclaiming deployability. It is not yet mature as a field product because the label system needs independent recuration, the prospective protocol needs external expansion, and the recommended cold-start recipe is explicitly historical rather than optimal. The final state is defense-ready as a bounded retrospective benchmark, but not field-deployment-ready.

## Critical concerns (if any item < 6)
None.

## Strongest single deduction
G: Practical value is capped because the strongest result is retrospective HIV-1 triage, while prospective backtests, adaptive selection, and callability audits currently fail; fix by adding an externally curated 20-30+ pathogen time-forward validation panel with predeclared abstention and independent label recuration.

RESULT_PROF_V7_08: total=74.5/100 min_item=6.0(G) max_item=9.0(I)
