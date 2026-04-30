# MutBench dissertation full-rigor experiment slate

Assumption: time is no longer the primary constraint, but the central scientific constraint remains unchanged: at the current \(n=11\) pathogen panel, adaptive weighting is underidentified. A journal-grade method claim should therefore avoid "one more adaptive learner" on the same panel and instead strengthen Algorithm 1 through calibrated reporting, falsification-resistant audits, and panel expansion with new Layer A labels.

## Tier 1 - Method core

### 1. Full null-calibrated Algorithm 1 callability and abstention

**Hypothesis:** Algorithm 1 is a useful cold-start prioritizer only in measurable callable regimes, and a predeclared abstention layer can improve mean reliability without pretending that all pathogens are predictable.

**Protocol:** Extend P1, P2, and P5 into one formal calibration study on the 11/12-pathogen feature-ablation panel. For every pathogen and temporal window where available, compute Algorithm 1's 4-core scores, top-k callsets, rank deciles, score-margin diagnostics, label prevalence, sequence depth, alignment length, entropy dispersion, homoplasy dispersion, duplicate rate, and Layer A density. Build null distributions with 100,000 label permutations per pathogen, including iid fixed-prevalence, circular coordinate shifts, protein-block shuffles, and local-burden-preserving shuffles. Define a callable status using training-fold-only diagnostics under nested leave-one-pathogen-out: for example, require top-decile score separation, null-adjusted enrichment lower bound above 1.0, perturbation Jaccard above a threshold, and no sparse-label red flag. Evaluate coverage, exact MCC, +/-10 MCC, precision@20, enrichment, constrained FPR, and abstention rate; report both all-pathogen and callable-only performance. The comparison is fixed 4-core versus full-10 EqualWeight, best single feature, random rank, and oracle 4-of-10 as an unattainable ceiling.

**Expected outcome:** My prior is that 5-7 of 11 pathogens become callable or review-only, while MERS/RSV-like sparse or weak-signal cases remain diagnostic-only. Callable-only metrics should improve materially, but abstention will be substantial. Failure mode: the diagnostics may not separate success from failure; then Algorithm 1 remains a ranked heuristic without a calibrated deployment rule.

**Defense question pre-empted:** "If MCC is small and prospective evidence is uneven, when should anyone trust the method?"

**Compute/time budget:** 200-800 CPU-hours for 100,000-permutation nulls and bootstrap intervals; 1-2 wall-clock weeks including analysis and figure production.

**What this adds to the dissertation:** New Chapter 4 subsection "Null-Calibrated Callability of Algorithm 1"; one reliability-curve figure, one callable-status table, and one methods paragraph defining abstention.

**Risk if it fails:** The dissertation honestly improves via disclosure. A failed callability rule blocks deployment language but strengthens the claim discipline.

### 2. Exhaustive fixed-core subset, Shapley, and stability decomposition

**Hypothesis:** The 4-feature cold-start core is not an arbitrary post hoc choice; it is close to the best label-free compact subset and each retained channel contributes a defensible marginal role.

**Protocol:** Extend P3 from the 15 subsets of the 4-core to the full 2^10 - 1 subset lattice over the 10 available features, with no learned pathogen-specific weights. For each subset, evaluate fixed EqualWeight scoring under nested-LOPO normalization, top-10% and top-20% thresholds, KDE/Wavelet/default detector variants, exact MCC, +/-10 MCC, enrichment, precision@20, constrained FPR, and rank stability under sequence resampling. Compute Shapley-style marginal contributions across all subsets for each metric and per-pathogen win counts. Compare the chosen 4-core against best 1-, 2-, 3-, 4-, and all-feature subsets, with multiplicity-aware bootstrap intervals rather than treating the best subset as a clean discovery.

**Expected outcome:** Frequency, entropy, and homoplasy likely carry most average signal; pLDDT is probably weaker but may improve constrained-FPR or structural-regime robustness. I expect the 4-core to remain near the Pareto frontier rather than uniquely best. Failure mode: a 3-core may dominate, in which case Algorithm 1 should be simplified or pLDDT should be marked optional.

**Defense question pre-empted:** "Why these four features instead of frequency plus entropy or an arbitrary cherry-picked subset?"

**Compute/time budget:** 50-200 CPU-hours if feature matrices are already present; 1 wall-clock week including Shapley summaries and plotting.

**What this adds to the dissertation:** New table ranking subset frontiers; new Shapley/ablation figure; revised Algorithm 1 note if the 3-core is cleaner.

**Risk if it fails:** The dissertation stays the same or improves. Finding a smaller robust core is a method improvement, not a fatal contradiction.

### 3. Detector-agnostic consensus and search-space reduction guarantee

**Hypothesis:** Algorithm 1's practical value is driven by biological scoring signal rather than a fragile detector setting, and consensus across detector families yields a smaller high-confidence candidate set.

**Protocol:** Extend P4 across the full 20 scoring x 39 detector x 11 pathogen Stage 3 grid and the 4-core/full-10 scores. For each pathogen, compute pairwise Jaccard overlap, Spearman rank correlation, call frequency, and detector-family agreement among Wavelet, KDE, HDBSCAN/MutClust, threshold, and window methods. Construct consensus callsets at >=25%, >=50%, and >=75% detector agreement, keeping thresholds fixed before evaluation. Test whether consensus positions are enriched for Layer A and vaccine-escape sites relative to detector-specific top-k lists and coordinate-preserving nulls. Report recall loss, precision gain, and candidate-list size.

**Expected outcome:** Consensus should increase precision/enrichment and reduce recall; high-agreement calls will likely be few but defensible. Failure mode: detector agreement may be too low outside H3N2/HIV-1/SARS-CoV-2, supporting the existing "detector choice matters" claim but not a guarantee.

**Defense question pre-empted:** "Are the results an artifact of one detector hyperparameter or family?"

**Compute/time budget:** 20-80 CPU-hours if callsets are materialized; 1 wall-clock week.

**What this adds to the dissertation:** New consensus-stability figure and a supplemental detector-overlap matrix; optional Algorithm 1 Tier 1b "review consensus" output.

**Risk if it fails:** The dissertation honestly improves via disclosure. It would prevent overclaiming detector-agnostic performance but not weaken the benchmark contribution.

### 4. Formal rank calibration and top-k decision curves

**Hypothesis:** Even when binary MCC is modest, Algorithm 1 scores encode useful rank information: top-ranked positions have higher empirical Layer A and escape-site density than lower-ranked positions.

**Protocol:** Extend P2 with full reliability analysis. Bin per-position Algorithm 1 scores into pathogen-normalized deciles and ventiles, then estimate empirical Layer A prevalence, +/-10-window prevalence, escape-site prevalence, enrichment, and bootstrap confidence bands. Fit a simple nonparametric calibration curve using only training pathogens in nested-LOPO, then evaluate calibration slope, expected calibration error, Brier score for top-k membership, and decision curves showing expected true positives per wet-lab screening budget of 20, 50, and 80 sites. Compare against frequency-only, entropy-only, homoplasy-only, full-10 EqualWeight, and random rank.

**Expected outcome:** Strong top-versus-bottom separation is plausible; strict monotonic decile calibration is less likely. The most defensible result is "rank-prioritized screening, not calibrated pathogenic probability."

**Defense question pre-empted:** "If the score is not a probability, what operational decision does it support?"

**Compute/time budget:** 20-60 CPU-hours; less than 1 wall-clock week.

**What this adds to the dissertation:** New calibration/decision-curve figure and a concise interpretation of Algorithm 1 as a screening-budget allocator.

**Risk if it fails:** Low to moderate. It weakens probability-like language but improves method honesty.

## Tier 2 - Robustness / honest disclosure

### 5. Biologically realistic local nulls for clustered labels and clustered calls

**Hypothesis:** Algorithm 1's apparent enrichment is not explained solely by local clustering of both Layer A labels and predicted hotspots.

**Protocol:** Replace simple label permutation with local null models that preserve protein-domain boundaries, local mutation burden, accessible-region masks, and Layer A cluster-size distributions. For each pathogen, simulate null callsets and null labels using block bootstrap, circular shifts within proteins/domains, and matched local entropy/frequency strata. Recompute exact MCC, +/-10 MCC, enrichment, precision@20, and constrained FPR for Algorithm 1, full-10, and best single feature. This is not a new method-selection run; it is an adversarial audit of whether coordinate clustering alone can explain the result.

**Expected outcome:** Some exact-site signals will attenuate, especially in pathogens with regionally clustered Layer A labels. HIV-1/H3N2 escape enrichment should survive better than sparse MERS/RSV cases. Failure mode: most global significance disappears under local nulls, requiring the dissertation to frame Algorithm 1 as region-prioritization only.

**Defense question pre-empted:** "Did you beat a real biological null, or only an iid coordinate shuffle?"

**Compute/time budget:** 300-1,000 CPU-hours; 1-2 wall-clock weeks.

**What this adds to the dissertation:** New adversarial-null subsection and a table separating iid-null, circular-null, and local-burden-null conclusions.

**Risk if it fails:** Honestly improves disclosure, but it may force a narrower method claim.

### 6. Layer A heterogeneity and alternative ground-truth audit

**Hypothesis:** The main conclusions are stable across reasonable definitions of adaptive hotspot ground truth and are not an artifact of one Layer A curation boundary.

**Protocol:** Re-evaluate Algorithm 1 and the headline Stage 2 interaction under multiple predeclared ground-truth variants: strict Layer A only, Layer A excluding labels that overlap vaccine-escape validation, Layer A+B, convergent-evolution-only, immune-escape-only, drug-resistance-only where applicable, +/-5 and +/-10 neighborhood labels, and DMS-derived Layer C labels for pathogens with independent assays. Use the same fixed scores and detectors; do not tune thresholds per ground-truth variant. Report changes in omega-squared, rank-calibration, MCC, enrichment, and per-pathogen callable status.

**Expected outcome:** Exact values will move, but the pathogen-dependence and search-space-reduction story should survive in broad form. Failure mode: the 4-core works only for one annotation definition, which would narrow the method claim to that definition.

**Defense question pre-empted:** "Are your results just a consequence of subjective Layer A annotation?"

**Compute/time budget:** 80-200 CPU-hours plus 1 week of annotation reconciliation; 1-2 wall-clock weeks.

**What this adds to the dissertation:** Robustness table by ground-truth definition and a methods appendix clarifying which claims depend on strict Layer A.

**Risk if it fails:** Honestly improves disclosure; only harmful if the current strict Layer A is uniquely favorable.

### 7. Sequence-processing, sub-lineage, and phylogenetic split stress test

**Hypothesis:** Algorithm 1 signals are robust to plausible sequence-sampling and phylogenetic preprocessing choices, not artifacts of duplicate-heavy alignments or one dominant lineage.

**Protocol:** For each pathogen with enough sequences, create multiple sequence panels: raw, deduplicated, date-balanced, geography-balanced, lineage-balanced, downsampled to common depth, and major-sublineage holdout where metadata permits. Recompute frequency, entropy, homoplasy, and pLDDT-derived 4-core scores where needed; keep structural pLDDT fixed if the protein model is unchanged. Evaluate rank correlation, top-k Jaccard, callable status, and Layer A metrics. For H3N2, SARS-CoV-2, Dengue/HCV, and HIV-1, add sub-lineage splits to test whether calls transfer within pathogen clades.

**Expected outcome:** Frequency/entropy calls will move under sampling; homoplasy and structural channels should stabilize some positions. Failure mode: the top-k list is highly sampling-sensitive, implying Algorithm 1 needs a sequence-quality gate before deployment.

**Defense question pre-empted:** "Could your hotspots be artifacts of sampling bias or lineage overrepresentation?"

**Compute/time budget:** 500-2,000 CPU-hours if trees/homoplasy are recomputed broadly; 2-4 wall-clock weeks.

**What this adds to the dissertation:** New preprocessing robustness figure and an explicit sequence-quality checklist for Algorithm 1.

**Risk if it fails:** Honestly improves deployment guidance; it may move some pathogens from callable to diagnostic-only.

## Tier 3 - Genuinely new contributions

### 8. Curated 20+ pathogen Layer A panel for real adaptive validation

**Hypothesis:** Adaptive method selection becomes learnable only after expanding the benchmark from 11 pathogens to roughly 20-30 curated pathogens with fewer singleton families and richer family replication.

**Protocol:** Manually curate Layer A for a prioritized expansion panel where sequence/features already look feasible and literature density is credible: West Nile virus E, Japanese encephalitis virus E, Yellow fever virus E, Tick-borne encephalitis virus E, Chikungunya virus E2, Nipah virus G, Measles virus H, and Mumps virus HN. These are worth the cost because they add flavivirus replication, alphavirus representation, and paramyxovirus family structure while targeting surface glycoproteins with known antibody, receptor-binding, or adaptation literature. For each pathogen, freeze inclusion criteria, coordinate mapping, evidence tiers, and exclusion rules before scoring evaluation. After curation, rerun Stage 2/3, Algorithm 1, callability, LOPO, leave-one-family-out, and the previously failed adaptive paradigms only as a powered panel-size test. The key test is not whether a new adaptive model wins at n=11, but whether performance changes as the panel approaches 20+ pathogens and family replication improves.

**Expected outcome:** I expect Algorithm 1 to remain a defensible cold-start floor and adaptive selection to improve but not become magic. A modest adaptive gain with calibrated abstention would be a real method contribution. Failure mode: adaptive learning still fails at 19-20 pathogens, implying the needed panel is larger or the meta-features are insufficient.

**New contribution:** A true benchmark expansion that can support or falsify pathogen-aware method selection rather than treating n=11 as enough.

**Compute/time budget:** 2,000-5,000 CPU-hours; 10-16 wall-clock weeks dominated by 1-2 weeks of Layer A curation per pathogen, partly parallelizable across curators.

**What this adds to the dissertation:** Potential new chapter or major Chapter 4 expansion: "Expanded MutBench Panel"; new pathogen table, new Stage 2 interaction analysis, new adaptive-validation table.

**Risk if it fails:** The dissertation still improves as the strongest possible negative result: adaptive weighting is not merely underpowered at n=11, but remains hard after targeted expansion.

### 9. Genuine prospective backtest with frozen historical windows

**Hypothesis:** Algorithm 1 can prospectively prioritize later adaptive/escape sites for at least a subset of pathogens when trained only on sequences and annotations available before the cutoff date.

**Protocol:** Build frozen historical snapshots for pathogens with sufficient dated sequences and post-cutoff literature: SARS-CoV-2 Spike, H3N2 HA, Influenza B HA, HIV-1 Env, Dengue E, HCV E2, EV-A71 VP1, RSV F, and WNV/JEV if curated in Experiment 8. For each cutoff, use only pre-cutoff sequences and pre-cutoff Layer A labels for any calibration or callable-status assignment. Evaluate against post-cutoff Layer A additions, post-cutoff DMS/escape publications, surveillance-defined substitutions, and known antigenic drift or receptor-binding updates. Use rolling cutoffs, blocked bootstrap by year, and a locked screening budget of 20/50/80 positions. Compare Algorithm 1 against frequency-only, entropy-only, pre-cutoff known-site neighborhood, and random baselines.

**Expected outcome:** I expect selective success, not universal success. H3N2/SARS-CoV-2 may be difficult because preexisting annotations are dense and circularity is hard; HIV-1/HCV/Dengue/EV-A71 may give cleaner novel-site tests if post-cutoff label additions are available. Failure mode: post-cutoff labels are too sparse or too biased toward already-studied regions.

**New contribution:** The first genuinely prospective/time-forward MutBench validation with frozen inputs.

**Compute/time budget:** 1,000-3,000 CPU-hours; 6-10 wall-clock weeks including date-stamped data reconstruction and literature cutoff auditing.

**What this adds to the dissertation:** New prospective-validation chapter section; one timeline figure, one frozen-window performance table, and one circularity audit.

**Risk if it fails:** The dissertation honestly improves via disclosure, but a clean null would block any prospective-method claim.

### 10. Self-supervised VAE/EVE or PLM site-effect layer with an explicit OOM workaround

**Hypothesis:** A self-supervised evolutionary model can add orthogonal site-level constraint/effect information to Algorithm 1 without using Layer A labels, but only if the training path is modernized and benchmarked against simpler PLM/EVmutation baselines.

**Protocol:** Do not rerun the abandoned old EVE code under PyTorch 2.5. Use a reproducible workaround: either run the original EVE environment in a pinned container compatible with its code path, or port training to a maintained VAE implementation with minibatched MSA sampling, mixed precision, gradient checkpointing, reduced latent dimension, and sequence subsampling. Start with proteins where EVE already completed or is feasible (HCV E2, Dengue E), then add SARS-CoV-2 Spike RBD/S1, HIV-1 Env/gp120, H3N2 HA1, RSV F, and WNV/JEV E after curation. Compare VAE-derived site intolerance or mutation-effect aggregates against ESM-2 LLR, Tranception, EVmutation/direct coupling scores, frequency/entropy, and the existing 4-core. Evaluate only as a label-free feature addition or replacement in Algorithm 1; no pathogen-specific supervised weights unless Experiment 8 expands the panel.

**Expected outcome:** My prior is mixed. VAE features may help HCV/Dengue-like proteins with deep diverse MSAs and hurt sparse or heavily biased proteins. The likely successful contribution is not "VAE beats all," but "self-supervised evolutionary effect features are useful in specific callable regimes." Failure mode: training remains unstable or the feature is redundant with entropy/homoplasy.

**New contribution:** A principled AI/PLM extension tested under strict label-free rules, with a documented workaround for the prior EVE OOM failure.

**Compute/time budget:** 2,000-10,000 GPU-hours depending on protein count and model; 6-12 wall-clock weeks with containerization and failed-run allowance.

**What this adds to the dissertation:** Optional new methods/results section on self-supervised evolutionary features; otherwise a future-work appendix documenting infeasibility and redundancy.

**Risk if it fails:** Mostly stays the same if framed as exploratory. It gets worse only if the dissertation overcommits to VAE/AI novelty before the audit passes.

### 11. Expanded-panel hierarchical benchmark model with phylogenetic partial pooling

**Hypothesis:** Once Layer A panel size increases, a joint hierarchical model can estimate pathogen, family, feature, detector, and ground-truth effects with honest uncertainty and can replace ad hoc ranking tables with posterior decision support.

**Protocol:** After Experiment 8 produces 20+ curated pathogens, fit a Bayesian hierarchical model over evaluation cells: metric ~ feature-category + detector-family + pathogen random effect + family random effect + feature x family interaction + technical covariates + ground-truth-type effect. Include phylogenetic covariance among pathogens using a viral-family tree or distance matrix where defensible; otherwise compare family random effects, Gaussian-process phylogenetic prior, and no-phylogeny models by posterior predictive checks and leave-one-family-out expected log predictive density. The target is not a new adaptive weight optimizer at n=11; it is a full uncertainty model for method comparison and for producing prediction intervals around Algorithm 1's expected performance on a new pathogen.

**Expected outcome:** With 20+ pathogens, family-level shrinkage may become estimable but still broad. I expect useful uncertainty intervals and better-calibrated recommendation tables, not large point-estimate gains. Failure mode: posterior intervals remain too wide, proving that even 20 pathogens are not enough for fine-grained adaptive selection.

**New contribution:** A statistically coherent benchmark meta-analysis and decision-support layer for MutBench.

**Compute/time budget:** 5,000-20,000 CPU-hours for MCMC/model comparison; 4-8 wall-clock weeks after expanded-panel data are ready.

**What this adds to the dissertation:** New statistical-model subsection, posterior forest plots, and a replacement for informal family-prior recommendations.

**Risk if it fails:** Honestly improves disclosure. Wide posteriors support the current panel-size caution and prevent false precision.

## Prioritized sequential execution order

1. Experiment 1 - Full null-calibrated callability and abstention. Highest immediate ROI for the "plausible method" claim.
2. Experiment 2 - Exhaustive subset/Shapley decomposition. Establishes whether Algorithm 1's 4-core is justified or should be simplified.
3. Experiment 4 - Rank calibration and decision curves. Converts low-MCC skepticism into screening-budget language.
4. Experiment 5 - Biologically realistic local nulls. Hardens the method against the strongest null-model critique.
5. Experiment 3 - Detector consensus. Adds operational confidence and a smaller high-confidence review mode if it works.
6. Experiment 6 - Ground-truth heterogeneity. Closes annotation-subjectivity questions before adding new pathogens.
7. Experiment 7 - Sequence/sub-lineage stress. Important before any prospective or deployment claim.
8. Experiment 8 - Curated 20+ pathogen panel. This is the real route to adaptive validation, but it is annotation-limited.
9. Experiment 9 - Frozen prospective backtest. Run after or alongside curation so future-window labels are cleaner.
10. Experiment 11 - Expanded-panel hierarchical model. Only meaningful after the curated panel exists.
11. Experiment 10 - VAE/EVE/PLM layer. High upside but lower certainty and GPU-heavy; keep exploratory until it passes redundancy and null audits.

Parallelization: Experiments 1, 2, 4, and 5 can run as compute jobs while a curator starts Experiment 6 annotation reconciliation. Experiment 8 should begin as soon as the first audits are queued; multiple curators can split pathogens. Experiment 7 can run in parallel with Experiment 8 for original-panel pathogens. Experiment 9 depends on frozen historical reconstruction and benefits from Experiment 8 labels, but its SARS-CoV-2/H3N2/HIV-1/HCV portions can start earlier. Experiment 11 should wait for Experiment 8. Experiment 10 can run independently on HCV/Dengue/SARS-CoV-2 once the containerized workaround is validated.
