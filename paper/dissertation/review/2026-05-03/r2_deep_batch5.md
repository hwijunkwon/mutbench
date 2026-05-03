# Risk-2 Deep Batch 5 -- Triage-Sensitive Blocks

Scope: Ch4 blocks #16/#17, Ch5 blocks #20/#21, and Ch1 blocks #2/#3. Read-only analysis; no dissertation source edits.

## Block #16 -- Ch4 Biology Rationale Table

Source: `ch4_results.tex` lines 308--330. Original length: 23 lines.

Survives:
- Keep all 11 pathogen-specific biological rationales, but shorten the table from explanatory prose to triage logic.
- Preserve high-value anchors: Norovirus homoplasy AUC `0.944` vs frequency `0.760`; SARS-CoV-2 shallow `~2019` phylogeny and CoVFit citation; MERS `530` deduplicated spike sequences and provenance path.
- Preserve the non-uniform best channels: H3N2 phylogenetic selection, Norovirus homoplasy, SARS-CoV-2/RSV PLM, Rabies stability, EV-A71 semantic change, HCV/HIV/Dengue diversity channels, MERS/Influenza B frequency.

Replacement draft, proposed 12 lines:

```latex
\begin{table}[htbp]\centering\small
\caption{Pathogen-specific rationale for wet-lab triage channel choice.}
\label{tab:stage2_biology_rationales}
\begin{tabular}{p{0.16\textwidth}p{0.22\textwidth}p{0.54\textwidth}}\toprule
Pathogen & Triage channel & Rationale \\\midrule
H3N2 & FUBAR BF & Deep HA history supports phylogenetic selection at antigenic sites. \\
Norovirus & homoplasy, AUC 0.944 & Epochal GII.4 replacement creates convergent antigenic changes; frequency AUC 0.760 is more founder-effect-prone. \\
SARS-CoV-2 / RSV & PLM channels & Shallow pandemic/strain diversity weakens MSA and phylogeny; PLM constraints supply the usable triage signal, consistent with CoVFit~\cite{covfit2025}. \\
Rabies / EV-A71 & stability / semantic change & Entry conformational change and VP1 canyon-rim immune pressure make structure/embedding shifts more informative than recurrence alone. \\
HCV / HIV-1 / Dengue & diversity channels & Quasispecies, serotype, entropy, frequency, and indel-aware diversity identify candidate immune-pressure regions when single-frequency summaries saturate. \\
MERS / Influenza~B & frequency & Sparse episodic sampling (MERS: 530 deduplicated spikes; \texttt{provenance/genbank\_queries.csv}) or lineage co-circulation makes recurrent position frequency the most practical triage signal. \\
\bottomrule\end{tabular}
\end{table}
```

Reframe note: This should not read as "the detector works because biology says so." It should read as "biology explains why the useful input channel changes by pathogen, so MutBench allocates experimental follow-up rather than claiming a universal classifier."

Line savings: `23 - 12 = 11`.

## Block #17 -- Ch4 Information-Type Analysis

Source: `ch4_results.tex` lines 624--700. Original length: 77 lines.

Survives:
- Keep the section/subsection labels, because downstream refs likely depend on them.
- Preserve the feature taxonomy: `10` biological features, `6` categories, `20` formulas.
- Preserve the interaction anchor: `omega^2_scoring x pathogen = 0.296`.
- Preserve key univariate AUC anchors: Norovirus homoplasy `0.944`; H3N2 pLDDT `0.787`; SARS-CoV-2 ESM-2 `0.586`; MERS ESM-2 `0.695`; HIV-1 entropy `0.730`; HCV dN/dS proxy `0.680`; RSV/MERS inverse associations.
- Preserve RF caveat: position-level 5-fold CV, mean AUC `0.742`, range `0.585--0.899`, spatial-autocorrelation leakage, illustrative not out-of-sample.
- Preserve correlation anchors: `rho_freq--entropy = 0.97`, `rho_freq--dN/dS = 0.87`, SASA vs pLDDT `rho=-0.19`, homoplasy decorrelated `|rho| <= 0.233`.
- Preserve ablation anchors: EqualWeight baseline `0.083` on 12-pathogen panel, core-11 `0.093`; homoplasy delta `-0.028`; entropy `-0.015`; freq `-0.012`; rare_freq `-0.010`; ESM-2 `+0.004`; SASA `+0.003`.
- Preserve nested-LOPO anchors: full-10 `0.070` CI `[0.017,0.130]`; fixed-4 `0.081` CI `[0.008,0.166]`; delta `+0.011`, CI `[-0.018,+0.042]`, permutation `p=0.61`.

Replacement draft, proposed 46 lines:

```latex
\section{Information-Type Analysis}
\label{sec:information_analysis}
\label{ch:adapt}

The benchmark's 20 scoring formulas reduce to 10 biological features across 6 information categories. This section explains the wet-lab triage implication of the Stage~2 interaction: the useful input information changes by pathogen ($\omega^2_{\text{scoring}\times\text{pathogen}} = 0.296$), so the output should be read as pathogen-specific candidate prioritization rather than as a universal detector.

\subsection{Per-Feature Discriminative Power and Multivariate Importance}
\phantomsection\label{subsec:per_feature_auc}\phantomsection\label{subsec:rf_importance}\phantomsection\label{subsec:feature_correlation}\phantomsection\label{subsec:info_type_implications}

Univariate Layer~A AUCs show why no single feature should be promoted globally: Norovirus is best separated by homoplasy (AUC $0.944$), H3N2 by pLDDT ($0.787$), SARS-CoV-2 and MERS by ESM-2 masked-marginal score ($0.586$ and $0.695$), HIV-1 by entropy ($0.730$), and HCV by the dN/dS proxy ($0.680$). RSV and MERS also show inverse associations for several channels ($\mathrm{AUC}<0.5$), demonstrating that the same feature can help one pathogen while misleading another.

A Random Forest summary (200 trees, max depth 5, 5-fold stratified CV; \texttt{scripts/rf_feature_importance.py}) reaches mean AUC $0.742$ across 11 pathogens (range $0.585$--$0.899$; \texttt{rf_cv_auc_v2.csv}), but this is a feature-complementarity diagnostic, not a prospective generalisation estimate, because position-level CV can leak spatially autocorrelated signal. Feature correlations clarify the triage rule: frequency, entropy, and dN/dS are redundant ($\rho_{\text{freq--entropy}}=0.97$, $\rho_{\text{freq--dN/dS}}=0.87$), SASA is not a pLDDT duplicate ($\rho=-0.19$), and homoplasy is the most decorrelated channel ($|\rho|\leq0.233$). Thus non-uniform ESM/SASA usefulness is not a failure of those features; it is evidence that wet-lab prioritization should choose channels conditional on pathogen biology.

\subsection{Feature Ablation Analysis}
\label{subsec:feature_ablation}

Under EqualWeight LOPO at a top-10\% budget, leave-one-feature-out ablation on the 12-pathogen feature panel (core 11 + Zika; core-only baseline $0.083\to0.093$) identifies homoplasy as the largest average contributor ($\Delta=-0.028$), followed by entropy ($-0.015$), frequency ($-0.012$), and rare-variant frequency ($-0.010$). Removing ESM-2 masked marginal ($+0.004$) or SASA ($+0.003$) slightly improves the uniform ensemble, which means these channels are noisy under one-size-fits-all weighting even though they remain useful for specific pathogens.

\begin{table}[htbp]
\centering\footnotesize
\caption{Triage interpretation of EqualWeight leave-one-feature-out ablation. Negative $\Delta$ means the feature helps the uniform ensemble; positive $\Delta$ means noise on average across pathogens.}
\label{tab:feature_ablation}
\begin{tabular}{lrl}\toprule
Feature group & $\Delta$MCC & Triage interpretation \\\midrule
homoplasy & $-$0.028 & strongest broad contributor; convergent-evolution channel \\
entropy / freq / rare\_freq & $-$0.015 / $-$0.012 / $-$0.010 & diversity and recurrence channels; partly redundant \\
dnds\_proxy / plddt / grantham / semantic\_change & $-$0.006 to $-$0.001 & conditional or weak average contribution \\
sasa / esm2\_llr & $+$0.003 / $+$0.004 & not globally useful under uniform weights; keep as pathogen-conditional triage channels \\
\bottomrule\end{tabular}
\end{table}

Nested-LOPO keeps the conclusion bounded. The full 10-feature ensemble has mean MCC $0.070$ (95\% CI [$0.017$, $0.130$]) and the fixed 4-feature core (homoplasy, pLDDT, entropy, frequency) has mean MCC $0.081$ (95\% CI [$0.008$, $0.166$]); the paired delta is $+0.011$ (95\% CI [$-0.018$, $+0.042$], sign-flip $p=0.61$). Therefore the compact 4-core is operationally equivalent under this retrospective LOPO audit, but not a prospectively callable detector.
```

Line savings: `77 - 46 = 31`.

## Block #20 -- Ch5 Cross-Pathogen Generalization

Source: `ch5_discussion.tex` lines 63--122. Original length: 60 lines.

Survives:
- Keep the core asymmetry: detection family main effect `omega^2=0.013`, about `23x` smaller than scoring-by-pathogen `omega^2=0.296`.
- Keep Rice algorithm-selection and No-Free-Lunch citations, but as framing, not proof.
- Keep bounded evidence set: `n=11`, LOPO `0/11`, Friedman `p=0.990`, oracle-vs-generalized gap `0.265`.
- Keep ESM-2 example: SARS-CoV-2 topped by ESM-LLR but Norovirus dominated by homoplasy, AUC `0.763` vs `0.944`.
- Keep comparison to EVEREST/ProteinGym as different task: per-variant fitness/escape vs per-region hotspot triage.
- Keep HIV-1 external anchor: `7.19x`, `82%` Layer-A-disjoint.
- Keep oracle ceiling and region-window anchors if section is retained here: exact mean `0.341`, range `0.196--0.660`, random baseline `0.001`, `113` SDs, `+/-5` mean `0.472`, `+/-10` mean `0.454`, Influenza B `0.894/0.924`.
- Keep recall caveat only in compressed form: mean recall `0.552`; EV-A71 `0.185`, Rabies `0.308`; triage subset not exhaustive list.

Replacement draft, proposed 25 lines:

```latex
\section{Cross-Pathogen Generalization}

\subsection{Implications of Cross-Pathogen Generalization}
\label{sec:cross_pathogen_implications}

The main cross-pathogen result is not that MutBench ``tried to generalize and failed,'' but that the 11-pathogen panel is below the size needed to learn an adaptive method-selection rule. Detection-family choice contributes little variance ($\omega^2=0.013$), about 23 times less than the scoring~$\times$~pathogen interaction ($\omega^2=0.296$). The operational implication is wet-lab triage: choose the information source that matches the pathogen's signal landscape before optimizing detector details.

This is Rice's algorithm-selection problem~\cite{rice1976algorithm}, with the No-Free-Lunch theorem~\cite{wolpert1997nfl} as intuition rather than proof. At $n=11$, the empirical mapping from pathogen properties to optimal scoring is not yet learnable under the tested labels and features: LOPO gives 0/11 exact matches, Friedman gives $p=0.990$, and the oracle-vs-generalised gap is $0.265$. The ESM-2 validation illustrates the same boundary: ESM-LLR is strongest for SARS-CoV-2 but is dominated by homoplasy on Norovirus (AUC $0.763$ vs.\ $0.944$).

This differs from EVEREST~\cite{gurev2025everest} and ProteinGym~\cite{notin2023proteingym}, which target per-variant fitness or escape prediction. MutBench evaluates region-level hotspot prioritization and contributes a quantified pathogen-dependent information-utility result ($\omega^2=0.296$ at 20-type granularity; $0.103$ at 6-category granularity), with HIV-1 vaccine-escape enrichment ($7.19\times$, 82\% Layer-A-disjoint) as the strongest external triage anchor.

\subsection{Upper Bound and Recall Boundaries}
\label{sec:oracle_mcc_ceiling}

The oracle ceiling is modest but non-random: mean exact MCC is $0.341$ across 11 pathogens (range $0.196$--$0.660$), against a random baseline near $0.001$ and 113 standard deviations above that baseline. Position-level exact matching, class imbalance ($0.7\%$--$15.9\%$ positives), and stringent labels explain much of the ceiling. Region-window scoring is more aligned with wet-lab follow-up: mean MCC rises to $0.472$ under $\pm5$ positions and $0.454$ under $\pm10$ positions, with Influenza~B reaching $0.894$ and $0.924$.

Mean oracle recall is $0.552$. Missed sites are not interpreted as random detector errors: they often reflect minimum-evidence Layer~A entries, epistatic escape, or short alignments. EV-A71 (recall $0.185$) and Rabies ($0.308$) mark the practical boundary: MutBench detections should be treated as prioritized subsets for DMS, neutralization assays, or epitope mapping, not exhaustive maps of adaptive positions.
```

Line savings: `60 - 25 = 35`.

## Block #21 -- Ch5 Future Directions

Source: `ch5_discussion.tex` lines 260--294. Original length: 35 lines.

Survives:
- Keep roadmap statuses: done negative, engineering feasible, future validation, scope/reproduction.
- Keep adaptive-oracle vs EqualWeight `0.160` vs `0.083`, seven paradigms fail, abstention `0/12`.
- Keep 20--30+ pathogen expansion as design target/rule-of-thumb, not a proven threshold.
- Keep label-provenance bottleneck and Wave 4/5 conclusion, but compress.
- Keep TreeTime/UShER citations and homoplasy distinctness anchors: simulation `rho=-0.876`, real GISAID `rho=-0.107`.
- Keep scope boundaries: DNA viruses, multi-protein, indels/recombination, virus-tuned PLMs, Nextstrain, non-coding; current evidence limited to RNA-virus surface-glycoprotein substitutions.

Replacement draft, proposed 17 lines:

```latex
\section{Future Research Directions}
\label{sec:future_work}

Table~\ref{tab:future_roadmap} separates completed negative gates from extensions that could convert retrospective triage into prospective callability.

\begin{table}[htbp]\centering\small
\caption{Prioritized future research roadmap with current status}
\label{tab:future_roadmap}
\begin{tabular}{llll}\toprule
Priority & Status & Direction & Gate / expected impact \\\midrule
1 & Done negative & Adaptive selection at current size & Oracle $0.160$ vs EqualWeight $0.083$, but seven paradigms fail and abstention calls 0/12 \\
2 & Engineering feasible & Expanded feature pipeline & Feature automation scales; curated external labels remain bottleneck \\
3 & Future & 20--30+ pathogen validation & Time-forward labels plus paired nested-LOPO/callability gates \\
4 & Future & Scope and release & DNA viruses, multi-protein targets, indels, reproduction, Zenodo provenance \\
\bottomrule\end{tabular}
\end{table}

The next study should not tune another weighting model on the same panel. It should expand to 20--30+ curated pathogens, treat that number as a stability rule-of-thumb rather than a guaranteed phase transition, and require time-forward validation plus predeclared callability. Feature engineering can scale, but Wave~4/5 show that label provenance is the limiting factor. Phylogenetic correction remains a targeted extension because homoplasy is distinct from frequency (simulation $\rho=-0.876$; real GISAID $\rho=-0.107$) and can be integrated through TreeTime~\cite{sagulenko2018treetime} or UShER~\cite{turakhia2020ultrafast}. Scope expansion should remain explicitly bounded beyond RNA-virus surface-glycoprotein substitutions.
```

Line savings: `35 - 17 = 18`.

## Block #2 -- Ch1 Research Objectives

Source: `ch1_introduction.tex` lines 76--157. Original length: 82 lines.

Survives:
- Keep three objectives, but make Objective 3 explicitly wet-lab triage and move the practical search-space economics into the objective language.
- Keep MutBench identity: 11 RNA viruses, 10 information types, 20 scoring formulas, 39 detector variants from 14 families, 8,580 evaluations.
- Keep three-layer ground truth and hotspot-score metric, but compress the ledger.
- Keep panel-scope table: 11 main, 12 Stage 3 with Zika, Wave 4/5 features-only panels.
- Keep figure concept if source figure remains, but rewrite the intro sentence and figure caption to triage-first.

Replacement draft, proposed 40 lines:

```latex
\section{Research Objectives}
\label{sec:intro_objectives}

This study treats computational hotspot detection as wet-lab triage: the goal is to prioritize a small, biologically plausible set of positions for follow-up experiments, not to claim a deployable cross-pathogen classifier. The objectives are:

\begin{enumerate}[label=\textbf{Objective \arabic*.}]
\item \textbf{Build MutBench, a standardized benchmark for comparing biological information sources across 11 RNA viruses.}
MutBench combines a three-layer ground truth (Layer~A literature-curated positives, Layer~B purifying-selection negatives, Layer~C DMS fitness validation), the hotspot-score metric, and 8{,}580 Stage~2 evaluations (20 scoring formulas $\times$ 39 detector variants from 14 families $\times$ 11 pathogens), with Stage~3 feature integration on the 11-pathogen panel plus Zika.

\begin{table}[htbp]
\centering\small
\caption{Panel-scope ledger for MutBench claims}
\label{tab:intro_panel_scope}
\begin{tabularx}{\textwidth}{p{0.25\textwidth}XX}\toprule
Panel & Used for & Not used for \\\midrule
11-pathogen main panel & Headline interaction, Friedman, LOPO 0/11, and escape enrichment & Not replaced by Stage~3 or Wave panels \\
12-pathogen Stage~3 panel & Feature ablation and nested-LOPO robustness (11 main + Zika) & Not a benchmark expansion \\
Wave 4--5 features-only panels & Feature-scaling and Layer~A$'$ sensitivity & Bounded sensitivity analyses only \\
\bottomrule\end{tabularx}
\end{table}

All headline claims belong to the 11-pathogen main panel unless stated otherwise.

\item \textbf{Quantify whether hotspot prioritization is driven mainly by scoring information, detector family, pathogen, or their interaction.}
This objective tests whether a universal scoring--detector recipe exists using ANOVA, Friedman testing, and LOPO validation. The expected interpretation is bounded: failure to learn a universal recipe at $n=11$ is evidence of current-panel non-deployability, not proof that future larger panels cannot support adaptive selection.

\item \textbf{Validate practical triage on independently curated vaccine-escape positions.}
The primary practical test is whether MutBench reduces a protein-scale search space from roughly 1{,}000 positions to a top-decile candidate set of about 10--50 positions while enriching for experimentally relevant escape sites, prioritizing Layer-A-disjoint HIV-1 evidence. The compact 4-feature core is reported as a retrospective cold-start sanity check, not as a prospectively callable detector.
\end{enumerate}

Figure~\ref{fig:research_overview} summarizes the research flow: MutBench compares information types, the main analysis shows pathogen-dependent information utility, and the external validation asks whether the resulting candidates are useful for wet-lab prioritization.
```

Line savings: `82 - 40 = 42`.

## Block #3 -- Ch1 Research Contributions

Source: `ch1_introduction.tex` lines 158--195. Original length: 38 lines. This block should stay similar length, but Contribution 1 should become the triage headline.

Survives:
- Keep three-contribution hierarchy.
- Reframe C1 from "benchmark as broadest hotspot detector" to "wet-lab triage benchmark and search-space reducer"; still preserve breadth numerics and benchmark identity.
- Keep C2 as pathogen-dependent information utility with `omega^2=0.296`, CI `[0.201,0.346]`, lower-bound `0.103`, 9 optimal types, LOPO `0/11`, Friedman `p=0.990`, and small-cluster boundary.
- Keep C3 as external validation, but make it the evidence ledger for triage: HIV-1 primary anchor, H3N2 self-consistency, SARS-CoV-2 exploratory, 4-core retrospective recipe.
- Preserve comparable-benchmark citations: ViroGym, EVEREST v3, ProteinGym v1.3.

Replacement draft, proposed 37 lines:

```latex
\section{Research Contributions}
\label{sec:intro_contributions}

The research contributions of this study are as follows.

\textbf{Contribution 1. MutBench as a wet-lab triage benchmark for RNA-virus hotspot prioritization.}
MutBench evaluates whether computational scores can reduce protein-scale experimental search spaces to candidate regions for follow-up assays. It is, to our knowledge, the broadest region-level, single-position hotspot-prioritization benchmark for RNA viruses: 8{,}580 evaluation cells across 20 scoring formulas, 39 detector variants from 14 families, and the 11-pathogen main panel, with Stage~3 feature integration extended to a 12-pathogen panel by adding Zika. Unlike concurrent fitness-regression benchmarks such as ViroGym~\cite{virogym2026}, EVEREST~v3~\cite{gurev2026everest_v3}, and ProteinGym v1.3~\cite{notin2025proteingym_v13}, MutBench asks which biological information source best prioritizes candidate hotspot regions for each pathogen. It organizes 10 information types into 6 categories, defines a three-layer ground truth, and uses the hotspot-score metric plus the Stage~1/Stage~2/Stage~3 design to support bounded triage claims rather than deployable surveillance claims.

\textbf{Contribution 2. Evidence that biological information utility is pathogen-dependent.}
The largest modeled component is the scoring~$\times$~pathogen interaction ($\omega^2=0.296$, 95\% cluster-bootstrap CI [0.201, 0.346]); 6-category aggregation gives $\omega^2=0.103$ as a collinearity-robust lower bound. The 11 pathogens show 9 distinct MCC-best scoring types, including FUBAR selection for H3N2, PLM scores for SARS-CoV-2 and RSV, and homoplasy for Norovirus. LOPO gives 0/11 exact matches and Friedman gives $p=0.990$, but these are treated as null-consistent corroboration of the interaction, not as standalone proof. With 11 pathogen clusters, the result is a finite-panel boundary: adaptive cross-pathogen method selection is not supported under the tested labels, features, and validation regime, while larger 20--30+ pathogen panels remain future work.

\textbf{Contribution 3. External evidence that MutBench can reduce wet-lab search space.}
The practical claim is retrospective prioritization: optimal scoring--detection combinations narrow roughly 1{,}000 alignment positions to about 10--50 candidates (11--32 in the three escape-enrichment anchors) with $7$--$9\times$ vaccine-escape enrichment. The validation hierarchy is:

\begin{table}[htbp]\centering\small
\caption{External-validation ledger for practical search-space reduction}
\label{tab:intro_external_validation_ledger}
\begin{tabularx}{\textwidth}{p{0.18\textwidth}p{0.32\textwidth}p{0.24\textwidth}X}\toprule
Anchor & Main result & Boundary & Role \\\midrule
HIV-1 primary & Layer-A-disjoint escape subset (37/45) yields $7.16$--$8.24\times$ novel-only enrichment; worst nominal Fisher $p=5.0\times10^{-12}$, Bonferroni $p_{\text{adj}}\approx3.9\times10^{-9}$ & Layer~A overlap $<33\%$ & Primary external triage validation \\
H3N2 & $9.36\times$ enrichment; EqualWeight $4.012\times$ ($p=0.0023$) & 69\% Layer~A overlap & Self-consistency support \\
SARS-CoV-2 & Escape enrichment survives multiple-comparison correction & Exploratory & Bounded external check \\
4-core & Full-10 MCC $0.070$ vs fixed-4 MCC $0.081$; delta $+0.011$, CI [$-0.018$,$+0.042$], $p=0.61$ & Retrospective only & Cold-start heuristic \\
\bottomrule\end{tabularx}
\end{table}

Together, the contributions establish MutBench as triage infrastructure, show why the relevant information source differs by pathogen, and validate practical search-space reduction without claiming a calibrated prospective detector.
```

Line savings: `38 - 37 = 1`.

## Savings Summary

| Block | Original lines | Proposed lines | Savings |
|---|---:|---:|---:|
| #16 biology rationale | 23 | 12 | 11 |
| #17 information-type analysis | 77 | 46 | 31 |
| #20 cross-pathogen generalization | 60 | 25 | 35 |
| #21 future directions | 35 | 17 | 18 |
| #2 research objectives | 82 | 40 | 42 |
| #3 research contributions | 38 | 37 | 1 |
| **Total** | **315** | **177** | **138** |

RESULT_R2_DEEP_BATCH5: blocks=6 line_savings=138
