# Risk-2 Deep Batch 1 -- Ch1+Ch2 Safe Trims

## #1 Ch1 Research Background

1. **First/last prose line**
- First: `When a new viral pandemic emerges, identifying which positions in the viral genome are mutating in functionally important ways is critical for public health response. These mutation ``hotspots'' help researchers prioritize which variants to monitor, which vaccine targets to update, and which drug resistance mutations to anticipate.`
- Last: `In practice, this means that for a virus with 1,000 amino acid positions, computational hotspot detection narrows the candidate list from 1,000 to approximately 50--100 positions (top 5--10\%), saving months of laboratory effort and enabling rapid response during emerging outbreaks.`

2. **Load-bearing claims**
- Viral mutation hotspots are public-health relevant because they inform variant monitoring, vaccine updating, and drug-resistance anticipation.
- SARS-CoV-2 re-established the importance of viral genome analysis~\cite{harvey2021tracking}.
- Hotspots are positions where mutations concentrate and are linked to transmissibility, immune evasion, and drug resistance~\cite{harvey2021tracking,carabelli2023convergent}.
- Existing hotspot practice relies heavily on frequency and entropy and cannot reliably separate biological signal from founder-effect artifacts.
- Related benchmarks cover per-variant fitness or escape, not region-level hotspot detection: ViroGym~\cite{virogym2026}, EVEREST v3~\cite{gurev2026everest_v3}, ProteinGym~\cite{notin2023proteingym,notin2025proteingym_v13}, EVEscape~\cite{thadani2023evescape}, and Livesey \& Marsh~\cite{livesey2020using}.
- Partial benchmarking precedents exist in cancer genomics~\cite{bailey2018comprehensive}.
- Prior author work, MOSD~\cite{han2025mosd} and MutClust~\cite{youn2025mutclust}, motivates the need for a quantitative benchmark.
- Nextstrain~\cite{nextstrain2018hadfield} and PANGO~\cite{rambaut2020pangolin} monitor lineages but do not evaluate region-level hotspot-detection information sources.
- The practical workflow is sequence collection, computational analysis, and experimental validation; computational ranking is valuable because wet-lab validation is expensive.
- MutBench is scoped to RNA-virus single-position region selection, with broader systems deferred to Chapter~\ref{ch:discussion}, Section~\ref{sec:future_work}.

3. **Concrete replacement draft**
```tex
\section{Research Background}
\label{sec:intro_background}

Viral mutation hotspots are genomic positions where mutations concentrate and can mark changes in transmissibility, immune escape, or drug resistance; they therefore help prioritize variant monitoring, vaccine updates, and antiviral-risk assessment~\cite{harvey2021tracking,carabelli2023convergent}.
Despite the scale of SARS-CoV-2 genomic surveillance~\cite{harvey2021tracking}, most hotspot analyses still rely on mutation frequency or Shannon entropy, which cannot by themselves distinguish functional signal from founder effects or compare against phylogenetic, structural, protein-language-model, or DMS-derived information.

Adjacent benchmarks evaluate per-variant fitness or escape rather than region-level hotspot selection: ViroGym~\cite{virogym2026}, EVEREST v3~\cite{gurev2026everest_v3}, ProteinGym~\cite{notin2023proteingym,notin2025proteingym_v13}, EVEscape~\cite{thadani2023evescape}, Livesey \& Marsh~\cite{livesey2020using}, and partial cancer-genomics precedents~\cite{bailey2018comprehensive}.
This gap also limits operational platforms such as Nextstrain~\cite{nextstrain2018hadfield} and PANGO~\cite{rambaut2020pangolin}, which track lineages but do not benchmark which information sources best identify mutation-prone positions.
The author's prior MOSD~\cite{han2025mosd} and MutClust~\cite{youn2025mutclust} work motivated MutBench as a standardized evaluation framework for the computational-analysis step between sequence collection and experimental validation.
MutBench evaluates how well computational rankings concentrate biologically meaningful positions for wet-lab triage within the RNA-virus single-position scope of Chapter~\ref{ch:mutbench}; extension to DNA viruses, eukaryotic pathogens, and prokaryotic systems remains future work (Chapter~\ref{ch:discussion}, Section~\ref{sec:future_work}).
```

4. **Citation preservation**
- Preserved: `harvey2021tracking`, `carabelli2023convergent`, `virogym2026`, `gurev2026everest_v3`, `notin2023proteingym`, `notin2025proteingym_v13`, `thadani2023evescape`, `livesey2020using`, `bailey2018comprehensive`, `han2025mosd`, `youn2025mutclust`, `nextstrain2018hadfield`, `rambaut2020pangolin`.

5. **Line savings**
- `51 -> 10`; savings `41` lines.

6. **Cross-reference side-effects**
- Preserves `sec:intro_background`, `ch:mutbench`, `ch:discussion`, and `sec:future_work`.
- Removes `tab:glossary` and the local reference to it. Local search shows no chapter-text dependency on `tab:glossary` outside this block, but glossary removal should be accepted explicitly.
- Removes the lexical-collision reference to `sec:intro_objectives`--`sec:intro_contributions`; no downstream reference depends on that sentence.

## #4 Ch2 DBSCAN/HDBSCAN Detail

1. **First/last prose line**
- First: `DBSCAN~\cite{ester1996dbscan} is a representative density-based clustering algorithm that defines high-density regions as clusters and classifies low-density regions as noise.`
- Last: `MutClust~\cite{youn2025mutclust} addressed this by replacing DBSCAN's fixed epsilon with a position-specific radius proportional to the H-score (a mutation importance metric combining frequency and entropy), thereby assigning wider neighborhoods to biologically significant positions and narrower neighborhoods elsewhere.`

2. **Load-bearing claims**
- DBSCAN defines density clusters and noise using epsilon neighborhoods and core points~\cite{ester1996dbscan}.
- DBSCAN finds arbitrary-shaped clusters without pre-specifying cluster count.
- Fixed global epsilon fails under strong density variation, including viral genomes.
- MutClust reported SARS-CoV-2 DBSCAN failure: 99.76\% merged under defaults; tuned parameters produced only 4 broad clusters~\cite{youn2025mutclust}.
- HDBSCAN adapts density through hierarchical cluster extraction~\cite{campello2013hdbscan}.
- OPTICS exposes multi-scale density via reachability plots but needs extraction choices~\cite{ankerst1999optics}.
- General density methods do not include biological importance scores; MutClust uses H-score-scaled radii~\cite{youn2025mutclust}.

3. **Concrete replacement draft**
```tex
\subsection{Density-Based Clustering}
\label{subsec:bg_density_clustering}

DBSCAN~\cite{ester1996dbscan} identifies density-connected clusters and noise from epsilon neighborhoods and core points, allowing arbitrary cluster shapes without a pre-set cluster count.
Its fixed global epsilon is poorly matched to viral genomes, where mutation density can differ sharply between immunodominant surface regions and conserved domains; in SARS-CoV-2, default DBSCAN merged 99.76\% of points into one cluster, and tuned parameters ($\varepsilon = 0.15$, MinPts $= 5$) still yielded only 4 broad clusters~\cite{youn2025mutclust}.
HDBSCAN~\cite{campello2013hdbscan} and OPTICS~\cite{ankerst1999optics} address variable density through hierarchical stability or reachability plots, but remain generic spatial algorithms.
This limitation motivated MutClust~\cite{youn2025mutclust}, which replaces a global epsilon with an H-score-scaled, position-specific radius so biologically important positions receive wider neighborhoods.
```

4. **Citation preservation**
- Preserved: `ester1996dbscan`, `youn2025mutclust`, `campello2013hdbscan`, `ankerst1999optics`.

5. **Line savings**
- `29 -> 7`; savings `22` lines.

6. **Cross-reference side-effects**
- Preserves `subsec:bg_density_clustering`.
- No `\ref{}` calls occur in the current block; none are removed.

## #5 Ch2 PLM Survey

1. **First/last prose line**
- First: `Protein language models (PLMs) trained on large-scale protein sequence databases have emerged as a complementary computational approach to variant effect prediction.`
- Last: `These distinctions make ProteinGym and MutBench complementary rather than competing: ProteinGym establishes which PLMs best predict individual mutation effects, while MutBench establishes which information types (including but not limited to PLM-derived scores) best identify mutation-enriched genomic regions across diverse pathogens.`

2. **Load-bearing claims**
- PLMs infer evolutionary plausibility from amino-acid co-occurrence and can score mutations without structures or experimental fitness data.
- ESM-2 uses masked LLR scoring and may be less reliable for viral proteins because UniRef is dominated by cellular proteins~\cite{lin2023esm2,rives2021biological}.
- Tranception is autoregressive and can use retrieval-augmented homologs~\cite{notin2022tranception}.
- ProtTrans, ESM-3, ESM-IF, SaProt, and ProteinMPNN represent broader PLM/structure-aware advances~\cite{elnaggar2022prottrans,hayes2024esm3,hsu2022esmif,su2024saprot,dauparas2022proteinmpnn}.
- ESM-3 and structure-aware PLMs are outside the headline MutBench panel for license/scope reasons.
- EVEscape combines generative fitness, accessibility, and physicochemical dissimilarity; MutBench uses an EVEscape-style ESM-2 proxy, not original EVEscape~\cite{thadani2023evescape}.
- AlphaMissense is human-centered and not directly transferable to viral variant effect prediction~\cite{cheng2023alphamissense}.
- EVEREST reports viral PLM underperformance versus alignment methods, a cross-study parallel rather than independent proof~\cite{gurev2025everest,gurev2026everest_v3}.
- ProteinGym benchmarks per-mutation fitness prediction, while MutBench benchmarks per-region hotspot detection~\cite{notin2023proteingym}.

3. **Concrete replacement draft**
```tex
\subsection{Protein Language Models for Variant Effect Prediction}
\label{subsec:bg_plm}

Protein language models score mutations from evolutionary plausibility learned over large sequence corpora, offering structure- and assay-free features for variant-effect prediction.
ESM-2~\cite{lin2023esm2,rives2021biological} uses masked log-likelihood ratios, whereas Tranception~\cite{notin2022tranception} is autoregressive and can retrieve homologous context; both are relevant to MutBench because viral proteins may be underrepresented in cellular-protein-heavy training corpora.
Broader PLM and structure-aware systems include ProtTrans~\cite{elnaggar2022prottrans}, ESM-3~\cite{hayes2024esm3}, ESM-IF~\cite{hsu2022esmif}, SaProt~\cite{su2024saprot}, and ProteinMPNN~\cite{dauparas2022proteinmpnn}; ESM-3 is excluded from the headline 8{,}580-evaluation grid because its Cambrian non-commercial license conflicts with the MIT-redistribution requirement (Chapter~\ref{ch:mutbench}, Section~\ref{para:external_licenses}), and structure-aware channels are deferred as future work.
EVEscape~\cite{thadani2023evescape} shows that generative fitness, accessibility, and residue dissimilarity can be productively combined; MutBench adopts only an EVEscape-style composite that substitutes ESM-2 mutation surprise for the EVE term (Section~\ref{sec:scoring_detection}).
AlphaMissense~\cite{cheng2023alphamissense} is important but human-variant-centered, while EVEREST~\cite{gurev2025everest,gurev2026everest_v3} reports PLM underperformance on viral proteins as a cross-study parallel, not independent confirmation of MutBench's pathogen-dependence result (Section~\ref{subsec:bg_benchmarking_gap}).
ProteinGym~\cite{notin2023proteingym} ranks predictors for per-mutation fitness regression over DMS assays; MutBench instead asks which information types, including ESM-2 masked-marginal and semantic-change scores, identify mutation-enriched regions across pathogens (Section~\ref{sec:information_analysis}).
```

4. **Citation preservation**
- Preserved: `lin2023esm2`, `rives2021biological`, `notin2022tranception`, `elnaggar2022prottrans`, `hayes2024esm3`, `hsu2022esmif`, `su2024saprot`, `dauparas2022proteinmpnn`, `thadani2023evescape`, `cheng2023alphamissense`, `gurev2025everest`, `gurev2026everest_v3`, `notin2023proteingym`.

5. **Line savings**
- `43 -> 9`; savings `34` lines.

6. **Cross-reference side-effects**
- Preserves `subsec:bg_plm`, `ch:mutbench`, `para:external_licenses`, `sec:scoring_detection`, `subsec:bg_benchmarking_gap`, and `sec:information_analysis`.
- No labels are removed.

## #6 Ch2 Feature-Importance Survey

1. **First/last prose line**
- First: `Several recent studies have analyzed which biological features predict viral mutation patterns, providing context for the multi-source information analysis in this dissertation (Section~\ref{sec:information_analysis}).`
- Last: `This is the gap that the present study addresses: by evaluating 20 scoring channels (derived from 10 underlying biological information families with normalization or composite variants) across 11 pathogens, MutBench quantifies the pathogen-specificity of feature importance and provides concrete recommendations for which information source to prioritize for each virus (Section~\ref{sec:information_analysis}).`

2. **Load-bearing claims**
- Prior feature-importance studies motivate MutBench's multi-source analysis.
- Maher et al. found epidemiological features dominated sequence features for SARS-CoV-2 VOC prediction, but the result is single-pathogen~\cite{maher2022predicting}.
- Rodriguez-Rivas et al. found DCA epistatic models outperformed independent-site models for SARS-CoV-2 escape prediction (AUC 0.76 vs 0.63)~\cite{rodriguez2022epistatic}.
- Coupling-aware methods are excluded from MutBench's 20-scoring panel, so the Chapter~\ref{ch:results} interaction result is bounded to single-position scorers.
- Hie et al. showed PLM semantic change can capture antigenic novelty~\cite{hie2021learning}.
- EVEscape supports multi-source integration of fitness, accessibility, and residue dissimilarity~\cite{thadani2023evescape}.
- The gap is cross-pathogen feature importance; MutBench evaluates 20 scoring channels from 10 information families across 11 pathogens.

3. **Concrete replacement draft**
```tex
\subsection{Feature Importance Analysis in Viral Mutation Prediction}
\label{subsec:bg_feature_importance}

Prior feature-importance studies motivate MutBench's multi-source analysis but remain mostly single-pathogen: Maher et al.~\cite{maher2022predicting} found epidemiological features dominated sequence features for SARS-CoV-2 variant emergence, Rodriguez-Rivas et al.~\cite{rodriguez2022epistatic} showed epistatic DCA models improved escape prediction (AUC 0.76 vs.\ 0.63), Hie et al.~\cite{hie2021learning} linked PLM semantic change to antigenic novelty, and EVEscape~\cite{thadani2023evescape} combined fitness, accessibility, and residue dissimilarity.
Coupling-aware methods such as DCA, EVcouplings, and GREMLIN remain outside MutBench's 20-scoring panel (Section~\ref{sec:scoring_detection}), so the scoring~$\times$~pathogen interaction in Chapter~\ref{ch:results} is an information-type contrast within a single-position regime, not an upper bound on epistasis-aware methods.
MutBench addresses the remaining gap by evaluating 20 scoring channels from 10 biological information families across 11 pathogens and reporting pathogen-specific feature recommendations (Section~\ref{sec:information_analysis}).
```

4. **Citation preservation**
- Preserved: `maher2022predicting`, `rodriguez2022epistatic`, `hie2021learning`, `thadani2023evescape`.

5. **Line savings**
- `23 -> 6`; savings `17` lines.

6. **Cross-reference side-effects**
- Preserves `subsec:bg_feature_importance`, `sec:information_analysis`, `sec:scoring_detection`, and `ch:results`.
- Removes the explicit future-work cross-reference to `ch:discussion`; if the future-work pointer is desired here rather than only in Ch5, add it to the second replacement sentence.

RESULT_R2_DEEP_BATCH1: blocks=4 line_savings=114
