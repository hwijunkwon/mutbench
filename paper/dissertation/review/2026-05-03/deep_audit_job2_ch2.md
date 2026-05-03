# Deep audit Job 2: `ch2_background.tex`

Scope: `paper/dissertation/chapters_en/ch2_background.tex` lines 1-299. Read-only audit of manuscript/source context; web checks used for citation/status claims on recent benchmarks and platform papers.

### Chunk 1 (lines 1-150, Mutation Hotspot Detection / Density-Based Clustering / DMS / PLM)

#### Numerical claims
- RNA-virus mutation rate `10^-3` to `10^-5` substitutions/site/replication cycle (line 16): VERIFIED / consistent with Holmes 2009 and Sanjuan 2010 as broad RNA-virus ranges.
- MutBench internal scope: 10 information families, 20 scoring channels (line 45): VERIFIED internally / matches repeated Chapter 3/4 framing and Chapter 1 abstract.
- DBSCAN comparison: 99.76% in one cluster; `epsilon=0.15`, `MinPts=5`, four clusters (line 71): VERIFIED / Youn 2025 full text reports DBSCAN with MinPts 5, epsilon 0.15, Cluster0 29,831 positions (99.76%), four total clusters, and 37 noise points.
- HDBSCAN “single parameter, min_cluster_size” (line 76): MINOR CAVEAT / HDBSCAN can be run with `min_cluster_size` as the primary required parameter, but implementations commonly expose `min_samples` and other settings. Characterization is acceptable for conceptual background if phrased as “can be used with”.
- DMS “all possible single amino-acid substitutions” and “thousands” (lines 91-96): VERIFIED as standard DMS description / no discrepancy.
- EVEREST v3 covers 45 viral DMS datasets (line 111): VERIFIED externally / EVEREST abstract reports 45 proteins/DMS datasets with >340,000 variants.
- ESM-2 650M parameters and approximately 250M UniRef sequences (line 131): VERIFIED / describes the common ESM-2 650M model family/training scale.
- ProtTrans “over 2 billion protein sequences” (line 141): VERIFIED / aligns with ProtTrans BFD+UniRef scale.
- ESM-3 exclusion from 8,580-evaluation grid due to non-commercial license (line 142): VERIFIED internally / cross-ref lands on Chapter 3 license paragraph; license rationale is plausible.

#### Citations
- `holmes2009evolution`, `sanjuan2010viral`: support broad RNA-virus mutation-rate range / OK.
- `mullick2021entropy`: supports Shannon entropy + K-means SARS-CoV-2 Spike hotspot detection / OK.
- `koyama2020variant`, `obermeyer2022analysis`: support SARS-CoV-2 mutation/frequency/fitness analyses / OK.
- Cancer hotspot methods: `lawrence2013mutsigcv`, `tamborero2013oncodriveclust`, `tokheim2016hotmaps`, `munoz2020mutspot` / OK.
- Phylogeny/selection tools: `felsenstein1985phylogenies`, `sagulenko2018treetime`, `suchard2018beast`, `kosakovsky2020hyphy`, `turakhia2020ultrafast`, `crispell2019homoplasyfinder`, `morel2024condor`, `murrell2012meme`, `murrell2013fubar`, `kosakovskypond2005fel`, `murrell2015busted` / OK.
- Density algorithms: `ester1996dbscan`, `campello2013hdbscan`, `ankerst1999optics` / OK. Author/year and characterization match the original methods.
- `youn2025mutclust`: supports MutClust existence, H-score-based adaptive density radius, and DBSCAN failure comparison / OK.
- DMS studies: `fowler2014dms`, `starr2020dms`, `dadonaite2023dms`, `lee2018h3n2dms`, `bloom2023fitness` / OK. Bloom/Neher is correctly described as sequence-phylogeny inferred fitness, not direct DMS.
- `greaney2021RBD`: OK for SARS-CoV-2 RBD antibody-escape DMS.
- `greaney2022spike`: MAJOR / line 105 says Greaney et al. extended antibody-escape DMS “to the full Spike with polyclonal sera.” The cited bib entry is *An Antibody-Escape Estimator for Mutations to the SARS-CoV-2 Receptor-Binding Domain* (Virus Evolution 2022), i.e. RBD, not full Spike. The note points to a companion PLoS Pathogens paper, but that paper also focuses on Delta-elicited RBD antibody response, not a full-Spike polyclonal-sera DMS extension. Full-length Spike DMS is Dadonaite 2023/2024, not this Greaney citation.
- Layer C source list in line 105: mostly OK but partially uncited in this sentence. The corresponding Chapter 3 table cites Dadonaite 2024, Haddox 2018, Simonich 2026, Aditham 2025, and Bakhache 2025. In this chapter sentence, only Dadonaite 2023/Greaney/Lee are directly cited; acceptable if the cross-reference to Table 3 is retained, but direct citations would be cleaner.
- PLM/VEP citations: `riesselman2018deep`, `frazer2021eve`, `lin2023esm2`, `rives2021biological`, `notin2022tranception`, `elnaggar2022prottrans`, `hayes2024esm3`, `hsu2022esmif`, `su2024saprot`, `dauparas2022proteinmpnn`, `thadani2023evescape`, `cheng2023alphamissense` / OK. EVEscape is accurately separated from generic PLMs.

#### Cross-refs
- `\ref{sec:information_analysis}` -> Chapter 4 information analysis / correct.
- `\ref{ch:mutbench}` -> Chapter 3 / correct.
- `\ref{sec:scoring_detection}` -> Chapter 3 scoring/detection section / correct.
- `\ref{sec:future_work}` -> Chapter 5 future work / correct.
- `\ref{ch:discussion}`, `\ref{sec:cross_validation_escape}`, `\ref{ch:results}`, `\ref{tab:vaccine_escape_stage3}`, `\ref{tab:gt_positions}` -> correct targets.
- `\ref{subsec:bg_dms}` in line 105 points to the current subsection. MINOR / self-reference is technically valid but awkward; if the intended pointer is the present subsection, use “this subsection” rather than a numbered self-reference.

#### Logical consistency
- No contradiction found between lines 1-150 and the rest of the manuscript on 11 pathogens, 20 scoring channels, or single-position scorer scope.
- The text correctly separates antibody-escape DMS from fitness-DMS Layer C, but the Greaney 2022 full-Spike claim weakens that separation.

#### Outdated content
- No “9 pathogens”, “12-pathogen Stage 2”, or “PAHD” stale phrasing in this chunk.
- Specific requested algorithms `BinSeg` and Bayesian online change-point detection are not cited or characterized in this chapter chunk; no direct claim to verify here.

#### Severity
- 0 Critical / 1 Major / 2 Minor

### Chunk 2 (lines 151-299, PLM cont., Genomic Surveillance, Feature Importance, Algorithm Selection, Benchmarking Gap)

#### Numerical claims
- ProteinGym 2023: 217 DMS assays and 2.7M substitution variants; over 70 predictors (line 159): VERIFIED / matches ProteinGym 2023 scale.
- MutBench scope: 20 scoring channels / 10 information families / 11 pathogens (lines 156, 208, 299): VERIFIED internally.
- Rice framing: Stage 1 hotspot-score and Stage 2 MCC (line 215): VERIFIED internally / cross-ref to metrics section lands correctly.
- Benchmarking methods: 14 detection families (line 228), 780 combinations and 8,580 grid cells (lines 276, 142): VERIFIED internally from design arithmetic (20 scoring channels x 39 detector variants x 11 pathogens = 8,580; 20 x 39 = 780 per pathogen).
- Bailey 2018: 26 tools, 9,423 tumor exomes (line 233): VERIFIED / consistent with PanCancer Atlas driver analysis.
- ProteinGym v1.3: 217 DMS assays and 90+ baselines (line 236): VERIFIED as current release-style claim from local bib/web.
- ViroGym: 13 viruses, 79 DMS assays, 552,937 sequences, 7 phenotypic categories (line 237): VERIFIED externally / arXiv abstract reports these exact counts plus 21 influenza neutralization tasks and SARS-CoV-2 real-world prediction.
- EVEREST v3: 45 viral DMS datasets, 31 forecasting clades across 4 viruses, 40 WHO-priority viruses, 16 viral families (line 248): VERIFIED externally for the first three; 16-family taxonomy claim is attributed to EVEREST. No separate ICTV citation appears in ch2, so taxonomy-source verification is indirect.
- ANOVA `omega^2=0.296`, CI [0.195, 0.333], residual ~0.39, enrichment statistics (lines 254-258): UNVERIFIED against CSV in this job / internally consistent with Chapter 4, but no `results/mutbench/` CSV was read or available in this scoped audit pass.

#### Citations
- Surveillance: `nextstrain2018hadfield` and `shu2017gisaid` / OK. Nextstrain is correctly described as real-time phylogenetic/geotemporal tracking; GISAID as a genome-sequence repository/data source. `rambaut2020pangolin` is OK for SARS-CoV-2 lineage nomenclature, though “taxonomic organization” is informal rather than ICTV taxonomy.
- Forecasting caveat: `luksza2014predictive`, `huddleston2020integrating` / OK for clade-level forecasting context.
- Feature-importance studies: `maher2022predicting`, `rodriguez2022epistatic`, `hie2021learning`, `thadani2023evescape` / OK.
- Algorithm-selection literature: `rice1976algorithm`, `kerschke2019algorithm`, `bischl2016aslib`, `feurer2015automl`, `kotthoff2016algorithm` / OK. Rice’s problem/feature/algorithm/performance mapping is correctly characterized; Kerschke 2019 is the correct survey.
- Benchmarking literature: `weber2019benchmarking`, `mangul2019systematic`, `boulesteix2017towards` / OK for neutral benchmarking and self-assessment bias.
- Benchmarking gap citations: `notin2023proteingym`, `notin2025proteingym_v13`, `virogym2026`, `morel2024condor`, `pons2020computational`, `harvey2021tracking`, `bailey2018comprehensive` / OK for task/scope distinction.
- MAJOR / line 264 says “EVEREST v3 (Jan 2026) and ProteinGym v1.3 are peer-reviewed releases.” The local bib marks EVEREST v3 as bioRxiv and ViroGym as arXiv; web metadata likewise shows EVEREST as a Jan 12, 2026 preprint/article page, not peer-reviewed. ProteinGym 2023 is peer-reviewed NeurIPS Datasets and Benchmarks, but `notin2025proteingym_v13` is a website/release entry, not itself a peer-reviewed publication. Caption should distinguish “ProteinGym 2023 peer-reviewed; v1.3 release; EVEREST v3 preprint/update.”
- `plant2025antigenic`, `shah2024h3n2ml`, `smith2004antigenic`, `cheng2023alphamissense` / OK for adjacent VEP/antigenic cartography context.

#### Cross-refs
- `\ref{ch:results}` -> Chapter 4 / correct.
- `\ref{subsec:9pathogen_metrics}` -> Chapter 3 metrics section / correct, but MINOR: label name is stale (`9pathogen`) while text is 11-pathogen.
- `\ref{sec:cross_validation_escape}` -> Chapter 5 vaccine escape section / correct.
- `\ref{tab:benchmark_comparison}` -> local table / correct.
- `\ref{ch:mutbench}` -> Chapter 3 / correct.

#### Logical consistency
- The PLM/VEP benchmarks are consistently framed as per-variant prediction benchmarks, not region-level hotspot detection benchmarks. This supports the claimed MutBench gap.
- The text appropriately qualifies EVEREST as a “parallel” rather than independent proof of MutBench non-transferability.
- PANGO is described as “taxonomic organization” (line 174). MINOR / PANGO is lineage nomenclature/classification for SARS-CoV-2, not ICTV taxonomy; avoid “taxonomic” if the dissertation also discusses formal ICTV taxonomy elsewhere.

#### Outdated content
- No “9 pathogens” prose in this chunk, but the cross-reference label `subsec:9pathogen_metrics` is stale.
- No PAHD mention.
- ICTV-specific taxonomy claims requested for this job are absent from active ch2 text; only the EVEREST “16 viral families” claim appears, sourced to EVEREST rather than ICTV.

#### Sources spot-checked
- Youn 2025 MutClust/DBSCAN comparison: https://biodatamining.biomedcentral.com/articles/10.1186/s13040-025-00476-3
- EVEREST v3 metadata/abstract: https://labs.sciety.org/articles/by?article_doi=10.1101%2F2025.08.04.668549
- ViroGym arXiv metadata/abstract: https://papers.cool/arxiv/2603.06740
- Greaney/Bloom RBD escape estimator: https://jbloomlab.org/papers/2022_greaney_c.html
- Greaney 2022 PLoS Pathogens Delta/RBD antibody response: https://journals.plos.org/plospathogens/article?id=10.1371%2Fjournal.ppat.1010592
- Nextstrain paper/docs: https://academic.oup.com/bioinformatics/article/34/23/4121/5001388 and https://docs.nextstrain.org/en/latest/learn/pathogens/index.html
- GISAID 2017 paper: https://www.gisaid.org/fileadmin/c/gisaid/files/pdfs/Eurosurveillance_From_Vision-to-Reality.pdf
- ICTV current taxonomy release context: https://cms.ictv.global/news/taxonomy_2024

#### Severity
- 0 Critical / 1 Major / 2 Minor

RESULT_DEEP_J2: critical=0 major=2 minor=4
