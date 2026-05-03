# Risk-2 Deep Batch 2 -- Ch3 Stage 1 Demotion + Statistical Design

## Block #7 -- Framework Overview (lines 78--144, safe)

First prose line: "The MutBench framework follows a three-component pipeline architecture (Figure~\ref{fig:mutbench_pipeline}): (1)~ground truth construction from three independent biological evidence sources, (2)~systematic scoring and detection via 20 scoring types and 14 detection method families, and (3)~multi-metric evaluation with factorial statistical analysis."

Last prose line: "Details are presented in Section~\ref{sec:eval_stat_design}."

Load-bearing claims to keep: 3-component pipeline; 3 evidence layers; 20 scoring types, 14 detection families/39 variants; Stage 1 is SARS-CoV-2 sanity check, not core in-depth validation; Stage 2 is the 11-pathogen factorial benchmark; metrics/statistical methods include MCC, hotspot-score, ANOVA, Friedman, LOPO; Figure~\ref{fig:mutbench_pipeline} must remain.

Draft (23 lines, 34.3%):
```tex
\subsection{Framework Overview}
\label{subsec:framework_overview}
MutBench is organized as the pipeline in Figure~\ref{fig:mutbench_pipeline}: ground-truth construction, per-position scoring plus hotspot detection, and multi-metric statistical evaluation.
The design separates a SARS-CoV-2 Stage~1 sanity check from the Stage~2 11-pathogen benchmark; Stage~3 information integration is described in Section~\ref{subsec:stage3_methods}.

% keep existing Figure~\ref{fig:mutbench_pipeline} unchanged

\textbf{Ground truth.}
The 3-layer reference separates adaptive/diversifying positives (Layer~A), constrained-region false-positive audits (Layer~B), and DMS functional validation (Layer~C).
Stage~1 adds SARS-CoV-2-specific synthetic and DMS checks only to audit framework behavior before the cross-pathogen analysis.
Details are in Section~\ref{subsec:3layer_gt}.

\textbf{Scoring and detection.}
Twenty scoring types in six information categories are converted into hotspot calls by 14 detection families (39 parameter variants).
Stage~1 tests the MutClust lineage and temporal SARS-CoV-2 scores as a single-pathogen sanity check (Section~\ref{subsec:stage1}); Stage~2 evaluates the full scoring $\times$ detection $\times$ pathogen grid (Section~\ref{sec:stage2}).

\textbf{Evaluation and statistics.}
Position-level metrics include MCC, F1, enrichment ratio, constrained FPR, and DMS F1.
Stage~1 uses hotspot-score to combine recall, precision, and stability; Stage~2 uses MCC as the primary cross-pathogen metric.
Factorial ANOVA with $\omega^2$, Friedman ranking, and LOPO validation are defined in Section~\ref{sec:eval_stat_design}.
```

Stage 1 voice to shift: replace "performs in-depth analysis" and "validate the framework components" with "single-pathogen sanity check" and "audit framework behavior."

Exact line savings: 67 original - 23 replacement = **44 lines**.

## Block #8 -- Stage 1 SARS-CoV-2 Methods (lines 338--487, guarded)

First prose line: "This subsection describes the Stage~1 experimental design, which focuses on SARS-CoV-2 as the anchor pathogen."

Last prose line: "Results of this pilot are reported in Chapter~\ref{ch:results} (Section~\ref{subsec:h3n2_temporal_pilot})."

Load-bearing claims to keep: Stage~1 is SARS-CoV-2-only sanity check; DMS Dadonaite entry-fitness top 20% and codon mapping; Eq.~\ref{eq:coordinate_transform}; synthetic signal recovery setup and non-biological limitation; Table~\ref{tab:ground_truth} and Figure~\ref{fig:mutbench_hotspot_map}; MutClust H-score, entropy, adaptive DBSCAN/HDBSCAN parameters, bug boundary, and v2c/v1 Stage~2 decision; Eq.~\ref{eq:mutbench_hscore}, Eq.~\ref{eq:shannon_entropy}, Eq.~\ref{eq:hotspot_score}; 100 x 80% stability bootstrap; Table~\ref{tab:alternative_scoring}; structural/contact, coalescent, TreeTime audit-only status; H3N2 temporal pilot sample distinction, windows, thresholds, top-k, Fisher test.

Draft (84 lines, 56.0%):
```tex
\subsection{Stage~1: SARS-CoV-2 Sanity Check}
\label{subsec:stage1}
Stage~1 is a single-pathogen sanity check on SARS-CoV-2, chosen because it has the richest external annotations.
It audits ground-truth mapping, MutClust-family behavior, hotspot-score stability, temporal scoring, and three orthogonal validation channels before Stage~2 generalizes the benchmark to 11 pathogens.

\subsubsection{Ground Truth Generation}
\label{subsec:stage1_gt}
Ground truth is generated from DMS data, synthetic signal recovery, and annotated Spike functional regions.
\textbf{DMS-based functional sites.}\phantomsection\label{subsec:dms_ground_truth}
Dadonaite et al. Spike pseudovirus-entry fitness data~\cite{dadonaite2023dms,dadonaite2024nature} are converted to functional sites by selecting amino-acid positions in the top 20\% of mean absolute fitness effect.
Selected amino-acid positions are mapped to nucleotides by:
\begin{equation}
\text{nuc\_positions} = \{g_{\text{start}} + (p_{\text{aa}} - 1) \times 3 + k : k \in \{0, 1, 2\}\}
\label{eq:coordinate_transform}
\end{equation}
where $g_{\text{start}} = 21{,}563$ is the Spike start in Wuhan-Hu-1.
This DMS label is independent of the detectors and avoids circular validation.
\textbf{Synthetic signal recovery.}
Synthetic H-score profiles provide a controlled recovery test with known inserted signals, not a biological performance estimate.
Core Candidate Mutation seed positions AA 484, 501, 417, and 452 receive $\mathcal{U}(0.8,1.2)$ scores, positions within 50 residues receive $\mathcal{U}(0.05,0.3)$, and background receives $\mathcal{U}(0.0,0.02)$ across one 29,903-position genome per trial.
Real-data conclusions therefore rely on the DMS and convergent-evolution references, with the synthetic test serving only as a detector-behavior audit.
\textbf{Annotated functional regions.}
Spike regions from cryo-EM and NTD supersite literature~\cite{wrapp2020cryo,mccallum2021ntd} are retained in Table~\ref{tab:ground_truth}; Figure~\ref{fig:mutbench_hotspot_map} maps the seven regions to the genome.
The reference covers 1,251 unique Spike nucleotide positions after deduplicating the S2'/fusion-peptide overlap.

\subsubsection{MutClust Variant Comparison}
\label{subsec:variants}
Among the 14 Stage~2 detection families, MutClust~\cite{youn2025mutclust} is the virus-specific starting point and is audited here as a SARS-CoV-2 sanity check.
Its H-score and entropy are:
\begin{equation}
H_i = \log_2(P_i \times E_i \times 100 + 1)
\label{eq:mutbench_hscore}
\end{equation}
\begin{equation}
E_i = -\sum_{j=1}^{k} p_{ij} \log_2 p_{ij}
\label{eq:shannon_entropy}
\end{equation}
Adaptive DBSCAN uses $\varepsilon=\gamma H_i$ with fixed $\gamma=0.5$; sensitivity for $\gamma \in \{0.25,0.5,1.0\}$ is archived in \texttt{gamma\_sensitivity.csv}.
The HDBSCAN-auto settings are \texttt{min\_cluster\_size}=5, \texttt{min\_samples}=1, and EOM selection.
The tested variants are v1, v2a, v2b, v2c, and v3.
MutClust-Hybrid v2c has the best Stage~1 hotspot-score ($0.778$), but Stage~2 retains published MutClust-Orig v1 because v2c assumes H-score-like inputs and the v1 cumulative-decay bug is upstream of clustering and confined to H-score-derived rows.\phantomsection\label{subsec:improvements}

\subsubsection{Hotspot-Score Composite Metric}
\label{subsec:hotspot_score}
Stage~1 uses hotspot-score as a local reliability audit:
\begin{equation}
\text{hotspot-score} = \frac{\text{recall} + \text{precision} + \text{stability}}{3}
\label{eq:hotspot_score}
\end{equation}
Stability is mean Jaccard similarity across 100 random 80\% position-subsampling iterations.
Stage~2 switches to MCC for cross-pathogen comparability (Section~\ref{subsec:9pathogen_metrics}).

\subsubsection{Temporal Scoring Variants}
\label{subsec:alternative_scoring}
The SARS-CoV-2 temporal variants in Table~\ref{tab:alternative_scoring} are Stage~1-only scores motivated by H-score saturation.
For each score, top 5\%, 10\%, 20\%, and median thresholds generate detected sets evaluated by F1, enrichment ratio, and Cohen's $d$.

\subsubsection{Structural and phylogenetic validation (SARS-CoV-2)}
\label{subsubsec:structural_phylo_validation}
Three audit-only analyses triangulate SARS-CoV-2 linear hotspot calls.
For 3D contacts, PDB~6VSB C$\alpha$ pairs within 8~\AA{} are compared to 1,000 hotspot-label permutations, reporting enrichment and a permutation $z$ statistic.
For coalescent simulation, 100 \texttt{msprime} replicates contrast one high-frequency founder substitution with three independent convergent substitutions, using seeds 42--141.
For TreeTime, IQ-TREE plus TreeTime v0.11 provides an audit-only ML homoplasy estimate compared with the production Fitch/FastTree homoplasy feature by Spearman correlation and Layer~A AUC.

\subsubsection{Time-stratified prospective protocol (H3N2 pilot)}
\label{subsubsec:h3n2_temporal_methods}
The H3N2 temporal pilot audits frequency-only prospective signal outside the headline Stage~2 panel.
It uses the raw 9,000-sequence 2010--2025 GISAID export, not the 2,562 unique-sequence Stage~2 H3N2 panel, so frequencies reflect circulating prevalence.
Three 3,000-sequence windows (2010--2015, 2016--2020, 2021--2025) are defined by sample-date sort.
Training-window frequency is evaluated against Koel antigenic sites and newly emerging holdout positions, where training frequency is $<5\%$ and holdout frequency is $\geq10\%$.
Top-$k$ overlap for $k \in \{20,30,50\}$ is tested by one-sided Fisher's exact test on the specified $2 \times 2$ table.
Results are reported in Section~\ref{subsec:h3n2_temporal_pilot}.
```

Stage 1 voice to shift: title and purpose should drop "In-Depth Analysis," "anchor pathogen," "validating framework components," and "establish the detection baseline." Use "sanity check," "audit," and "Stage~1-only."

Exact line savings: 150 original - 84 replacement = **66 lines**.

## Block #9 -- Evaluation and Statistical Design (lines 721--854, guarded)

First prose line: "The following evaluation metrics are used in the 11-pathogen benchmark."

Last prose line: "A paired bootstrap design that evaluates two methods simultaneously on the same bootstrap resample, testing the statistical significance of hotspot-score differences between methods."

Load-bearing claims to keep: MCC definition and confusion-matrix treatment of Layers A/B; F1/precision/recall/enrichment/constrained FPR/DMS F1; Stage~1 hotspot-score vs Stage~2 MCC rationale; Eq.~\ref{eq:mcc}, Eq.~\ref{eq:omega_squared}, Eq.~\ref{eq:weighted_hotspot_score}; 8,580 rows, 20 x 14 x 11 cells, detector-variant residual, residual df 7,970; evaluation-level $\omega^2=0.296$ and cell-level 0.234; cluster bootstrap CI [0.201,0.346]; ANCOVA and Bayesian cross-check; Levene/Kruskal/ART caveats; LOPO definition and 280-cell random baseline; nested-LOPO leakage prevention; Friedman 11 pathogen blocks; BCa small-n warning plus five robustness frames; explicit not-performed jackknife/Mantel acknowledgements; subsample robustness; feature ablation; Stage~1-only bootstrap/permutation/pairwise methods.

Draft (80 lines, 59.7%):
```tex
\subsection{Evaluation and Statistical Design}
\label{sec:eval_stat_design}
\subsubsection{Evaluation Metrics}
\label{subsec:9pathogen_metrics}
The 11-pathogen benchmark reports MCC, F1, precision, recall, enrichment ratio, constrained FPR, and DMS F1.
MCC is computed with Layer~A as the positive class; Layer~B positions remain in the ordinary non-Layer-A pool and are additionally audited by constrained FPR.
Enrichment uses one-sided Fisher tests for hotspot enrichment over non-hotspot positions.
Stage~1 uses hotspot-score (Eq.~\ref{eq:hotspot_score}) as a SARS-CoV-2 reliability audit, whereas Stage~2 uses MCC because stability under position masking is not comparable across pathogen lengths and MSA sizes.
\begin{equation}
\text{MCC} = \frac{TP \times TN - FP \times FN}{\sqrt{(TP+FP)(TP+FN)(TN+FP)(TN+FN)}}
\label{eq:mcc}
\end{equation}
MCC is set to 0 when the denominator is zero and is the headline metric because it uses all four confusion-matrix cells under severe class imbalance~\cite{chicco2020mcc}.
\textbf{Headline-metric choice.}\phantomsection\label{subsubsec:headline_metric_choice}
For all 8,580 evaluation cells, MCC, F1, precision, recall, and detection count are archived in \texttt{results/mutbench/stage3\_full\_results.csv}.
F1 is retained for auditability; AUROC is not precomputed because the headline detectors produce fixed-threshold calls, but can be recomputed from archived per-position scores.

\subsubsection{Three-way ANOVA ($\omega^2$)}
\label{subsec:9pathogen_statistics}
A three-way fixed-effect ANOVA uses scoring type (20), detection family (14), and pathogen (11), with all main effects and two-way interactions.
The 8,580 evaluation rows retain detector-variant differences in the residual term rather than modeling a full three-way interaction; residual df is 7,970 in \texttt{stage3\_statistics.csv}.
Because detector variants within a scoring--family--pathogen cell share inputs and labels, the effective unit is closer to the $20 \times 14 \times 11=3,080$ cell grid than to 8,580 independent observations.
Accordingly, inference is interpreted through pathogen-cluster robustness checks rather than naive row-level independence.
Omega-squared is computed in non-partial form:
\begin{equation}
\omega^2 = \frac{SS_{\text{effect}} - df_{\text{effect}} \times MS_{\text{error}}}{SS_{\text{total}} + MS_{\text{error}}}
\label{eq:omega_squared}
\end{equation}
The manual Type-II-like implementation and a statsmodels Type-II cross-check both give headline $\omega^2_{\text{scoring}\times\text{pathogen}}=0.296$ on the 8,580-row panel.
\textbf{Cell-level vs.\ evaluation-level $\omega^2$.}\phantomsection\label{subsubsec:cell_level_omega}
Aggregating detector variants within each scoring--family--pathogen cell gives the more conservative cell-level $\omega^2_{\text{scoring}\times\text{pathogen}}=0.234$.
The evaluation-level 0.296 is retained because it matches the archived headline grid and cluster-bootstrap CI [0.201,0.346], while the cell-level value guards against within-cell residual contraction.
\textbf{ANCOVA with technical covariates.}\phantomsection\label{subsubsec:ancova_methods}
On the cell grid, replacing the pathogen main effect with $\log(\text{alignment length})$ and Layer~A positive rate raises the scoring $\times$ pathogen interaction from 0.234 to 0.274 ($p<10^{-167}$), so the interaction is not explained away by these two technical covariates.
\textbf{Bayesian partial-pooling cross-check.}\phantomsection\label{subsubsec:bayesian_methods}
The Bayesian checks report posterior interaction estimates above Cohen's large-effect threshold: exploratory half-Cauchy mean 0.252, HDI [0.188,0.314], and archived half-Normal mean 0.319, HDI [0.246,0.396].
Levene, Kruskal--Wallis, and ART diagnostics are reported because variances are heterogeneous; the ART interaction estimates remain large in both exploratory and archived implementations.
No family-wise correction is applied to the ANOVA variance decomposition; vaccine-escape Fisher tests use their separate Bonferroni denominators.

\subsubsection{LOPO Cross-Validation (Leave-One-Pathogen-Out)}
LOPO selects the best scoring $\times$ family pair on 10 pathogens and evaluates it on the held-out pathogen.
Concordance is exact equality between the training-best and held-out-best family-level cells on the 280-cell grid; the random concordance baseline is about 0.36\%.

\subsubsection{Nested-LOPO 4-feature evaluation}
\label{subsubsec:nested_lopo_methods}
The 4-feature retention test is run on the 12-pathogen feature-ablation panel and re-fits per-feature signs and rankings inside each training fold only.
Held-out evaluation z-scores within the held-out pathogen, averages the selected features, thresholds the top 10\%, and evaluates MCC.
Paired bootstrap and sign-flip permutation test the 4-core minus full-10 delta.

\subsubsection{Friedman Test}
The Friedman test compares the top $k=20$ scoring $\times$ family combinations using the 11 pathogens as repeated-measures blocks, with Kendall's $W$ interpreted following Dem\v{s}ar~\cite{demsar2006statistical}.

\subsubsection{Pathogen-level BCa Bootstrap Confidence Intervals}
\phantomsection\label{subsec:wild_cluster_future}
BCa intervals over 11 pathogens are approximate and treated as small-cluster diagnostics, not definitive row-level inference.
The robustness ledger includes standard cluster CI [0.201,0.346], wild-cluster bootstrap [0.201,0.303], phylogenetic block bootstrap [0.202,0.346], mixed-effects pseudo-$\omega^2_{\text{int}}=0.340$, and Bayesian factor-analysis mean 0.316, all above or supporting the large-effect threshold.
\textbf{Delete-one jackknife (not performed).}\phantomsection\label{subsubsec:jackknife_acknowledgement}
A delete-one pathogen jackknife was not performed.
\textbf{Mantel/Procrustes distance-matrix tests (not performed).}\phantomsection\label{subsubsec:mantel_acknowledgement}
Phylogenetic non-independence is handled by family-pair sensitivity discussion, pathogen-cluster bootstrap, LOPO, and Friedman blocks rather than Mantel or Procrustes tests.

\subsubsection{Subsample Robustness Analysis}
MSA subsamples at 25\%, 50\%, 75\%, and 100\% test MCC stability as a function of sample size.
\subsubsection{Feature Ablation Analysis}
Leave-one-feature-out and nested subset analyses quantify how each of the 10 information types contributes to the EqualWeight ensemble.
\textbf{Weight Sensitivity Analysis.}
\label{subsec:weight_sensitivity_methods}
\begin{equation}
\text{hotspot-score}_w = w_r \cdot \text{recall} + w_p \cdot \text{precision} + w_s \cdot \text{stability}
\label{eq:weighted_hotspot_score}
\end{equation}
Stage~1 ranks the five MutClust variants across 171 hotspot-score weight combinations.
\textbf{Statistical Validation Methods.}
\label{subsec:statistical_methods}
Stage~1-only validation uses region-level bootstrap over seven Spike functional regions, random-label and circular permutation tests with pseudo-count $p=(\text{count}+1)/(N_{\text{perm}}+1)$, and paired bootstrap comparisons.
```

Stage 1 voice to shift: make all hotspot-score, weight-sensitivity, region-bootstrap, permutation, and pairwise-comparison text explicitly "Stage~1-only" or "SARS-CoV-2 reliability audit."

Pseudo-replication/cluster defense risk: **medium if compressed as above, high if further reduced.** The replacement must preserve the 8,580-row vs 3,080-cell distinction, detector variants in the residual, residual df 7,970, cell-level 0.234, cluster CI [0.201,0.346], and small-$G$ caveat. Removing any two of these would materially weaken the response to row-level pseudo-replication objections.

Exact line savings: 134 original - 80 replacement = **54 lines**.

## Block #10 -- Code/Data/License Prose (lines 866--892, safe)

First prose line: "The full source code, configuration files, scoring scripts, detection-family implementations, ground-truth tables, statistical-analysis notebooks, and the 8{,}580-evaluation result archive are released under the MIT License (MutBench's own implementation code) with the dissertation text and figures additionally distributed under the Creative Commons Attribution--NonCommercial 4.0 International license (CC-BY-NC 4.0) for documentation reuse.%"

Last prose line: "Chapter~\ref{ch:results} applies this framework to report experimental results: Stage~1 provides a controlled SARS-CoV-2 sanity check, Stage~2 extends the evaluation to all 11 pathogens to identify the dominant factors influencing hotspot detection performance, and Stage~3 decomposes the resulting performance by information type via per-feature AUC, ablation, and Random Forest analyses."

Load-bearing claims to keep: MIT code license; CC-BY-NC dissertation/figures license; canonical repo/commit/Zenodo DOI placeholder; seed 42 and seeds 42--141 for Stage~1 stability; pinned environment files; external resources not redistributed; license matrix path; headline grid excludes ESM-3/EVE restricted resources; summary of 11 viruses, 3 layers, 20 scores, 14 families, Stage~3; Stage~1 sanity-check phrasing.

Draft (9 lines, 33.3%):
```tex
\subsection{Code, Data, and Reproducibility}
\label{subsec:code_data_availability}
MutBench code, configuration, scoring/detection scripts, ground-truth tables, notebooks, and the 8,580-evaluation archive are released under MIT; dissertation text and figures use CC-BY-NC 4.0.\footnote{The code and data/documentation license split is recorded in \texttt{LICENSE-CODE}, \texttt{LICENSE-DATA}, and \texttt{results/mutbench/provenance/README.md}.}
The canonical repository is \url{https://github.com/kksuhj/mutbench}; the commit hash is recorded in \texttt{provenance/commit.txt}, with the final Zenodo DOI inserted at submission.
Randomized analyses use \texttt{seed}=42, with Stage~1 stability seeds 42--141, and software versions are pinned in \texttt{environment.yml}, \texttt{requirements-pinned.txt}, and \texttt{provenance/tool\_versions.txt}.
\paragraph{Software and data licenses (external resources).}
\label{para:external_licenses}
External tools, models, structures, sequence repositories, and DMS datasets are governed by their upstream licenses and summarized in \texttt{results/mutbench/provenance/external\_resource\_licenses.csv}; MutBench redistributes only derived per-position scores, labels, calls, and summary statistics, not model weights, upstream FASTA bundles, or raw third-party DMS tables.
The headline 8,580-cell grid excludes non-commercial-gated ESM-3/EVE resources, preserving reproducibility of the MIT-licensed code release. This chapter defined the 11-virus, 3-layer, 20-score, 14-family MutBench framework: Stage~1 is a SARS-CoV-2 sanity check, Stage~2 is the cross-pathogen benchmark, and Stage~3 analyzes multi-source integration.
```

Stage 1 voice to shift: final summary should say "SARS-CoV-2 sanity check," not "controlled" if "controlled" implies stronger validation than intended.

Exact line savings: 27 original - 9 replacement = **18 lines**.

## Aggregate

Total proposed replacement lines: 23 + 84 + 80 + 9 = 196.
Total original lines: 67 + 150 + 134 + 27 = 378.
Exact line savings: 378 - 196 = **182 lines**.

Risk flags: #8_stage1_demoted_but_method_audit_must_remain; #9_medium_pseudoreplication_defense_if_kept_at_80_lines; #9_high_risk_if_cell_level_or_cluster_CI_removed; #10_license_matrix_must_remain_auditable.

RESULT_R2_DEEP_BATCH2: blocks=4 line_savings=182 risk_flags=[#8_stage1_demoted_but_method_audit_must_remain,#9_medium_pseudoreplication_defense_if_kept_at_80_lines,#9_high_risk_if_cell_level_or_cluster_CI_removed,#10_license_matrix_must_remain_auditable]
