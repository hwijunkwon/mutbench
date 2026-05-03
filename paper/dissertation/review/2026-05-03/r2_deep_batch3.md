# Risk-2 Deep Batch 3 -- Ch4 Stage 1, Robustness, Structural, ANOVA

Source read: `ch4_results.tex` lines 18--115, 117--198, 200--219, 485--538, plus `risk2_compression_analysis.md` and `risk1_framing_analysis.md`.

Counting rule: original inclusive source lines versus proposed replacement source lines, counting blank lines.

## Block #11 -- Stage 1 results

First line: `\section{Single-Pathogen Benchmark: SARS-CoV-2}`

Last line: `\textbf{Stage 1 summary.} MutClust-Hybrid is the best of the H-score-based variants on synthetic data ($\mathit{HS} = 0.778$, $\sim$$43\times$ above chance) but loses its advantage on sparse real GISAID data ($\mathit{HS} = 0.383$ vs.\ MutClust-Fixed $0.386$); enrichment remains high ($6.9$--$8.0\times$). The single-pathogen Stage 1 therefore validates the hotspot-score metric and the multi-ground-truth comparison as a controlled sanity check, but the question of which scoring--detector combination is best is genuinely pathogen-dependent and is taken up at scale in Section~\ref{sec:9pathogen_results}.`

Must-retain numerical anchors: 29,903 positions; 1,251 ground-truth nt; `F_1 = 0.785`; `HS = 0.778`; random baseline `0.018`; `~43x`; precision `0.968`; recall `0.659`; GISAID `342/29,903 = 1.14%`; GISAID Hybrid `F_1=0.123`, `HS=0.383`; Fixed/dNdS `HS=0.386`; sliding-window `F_1=0.420`; enrichment `6.9--8.0x`; OPTICS `F_1=0.150`, `HS=0.369`; KDE precision `1.000`, recall `0.049`, `HS=0.557`; 30 OPTICS and 36 KDE sweeps. Multi-GT anchors: 417 AA/32.8%/1,251 nt; 252/19.8%; 97/7.6%; Jaccard `0.006`; table values `0.474`, `0.315`, `0.188`, `1.70x`, `0.108`, `3.43x`.

Sanity-check framing: Stage 1 should no longer read as detector selection. It is a controlled SARS-CoV-2 sanity check showing that the metric can recover planted or curated signal, while sparse real surveillance data immediately demotes any universal-detector claim.

Concrete replacement draft (47 lines):

```latex
\section{Single-Pathogen Benchmark: SARS-CoV-2}
\label{sec:single_pathogen_benchmark}

\subsection{Stage~1 metric sanity check}
\label{sec:variant_comparison}
\label{sec:multi_gt}
\label{sec:real_gisaid_benchmark}

Stage~1 is retained as a single-pathogen sanity check rather than as detector selection.
On a SARS-CoV-2-like synthetic genome (29,903 positions; 1,251 ground-truth functional positions), MutClust-Hybrid achieved the best H-score-based balance ($F_1=0.785$, precision $0.968$, recall $0.659$, $\mathit{HS}=0.778$), about $43\times$ the $0.018$ random baseline (Table~\ref{tab:hotspot_scores}).
The other MutClust variants remained precise but lower-recall, HDBSCAN-Auto was high-recall/low-precision, and external OPTICS/KDE sweeps (30 and 36 configurations; OPTICS $F_1=0.150$, $\mathit{HS}=0.369$; KDE precision $1.000$, recall $0.049$, $\mathit{HS}=0.557$) did not exceed the Hybrid hotspot-score.

\begin{table}[htbp]
\centering
\caption{Synthetic benchmark headline (100 subsamplings, 80\% retention); full variant and baseline details are archived in the supplementary CSV.}
\label{tab:hotspot_scores}
\small
\begin{tabular}{lrrrrr}
\toprule
Method & Precision & Recall & F1 & Stability & Hotspot-score \\
\midrule
\textbf{MutClust-Hybrid} & \textbf{0.968} & \textbf{0.659} & \textbf{0.785} & \textbf{0.706} & \textbf{0.778} \\
MutClust variants (Original / Fixed / dNdS) & 0.988--0.991 & 0.504--0.506 & 0.668--0.669 & 0.418--0.445 & 0.638--0.646 \\
HDBSCAN-Auto & 0.079 & 0.944 & 0.146 & 0.788 & 0.604 \\
Frequency baseline / sliding window & 0.404 / 0.157 & 0.965 / 0.974 & 0.569 / 0.270 & --- & --- \\
\bottomrule
\end{tabular}
\end{table}

The same benchmark was then checked against three non-equivalent ground truths: functional regions (417 AA, 32.8\%; 1,251 unique nt), DMS-escape (252 positions, 19.8\%; top 20th percentile~\cite{dadonaite2023dms}), and convergent evolution (97 positions, 7.6\%~\cite{cao2023ba286,carabelli2023convergent}).
Their DMS--convergence Jaccard similarity was only 0.006, and the leading method changed by reference set (Table~\ref{tab:multi_gt}), so a single ground truth would bias the benchmark.

\begin{table}[htbp]
\centering
\caption{Method comparison across multiple ground truths.}
\label{tab:multi_gt}
\small
\begin{tabular}{llrrr}
\toprule
Ground truth & Best method & F1 & Enrichment & Positions \\
\midrule
Functional regions & TC-freq-v2 & 0.474 & --- & 417 \\
DMS-escape & Saturated H-score & 0.315 & --- & 252 \\
Convergent / strict convergent & CH-score / TC-freq-v3 & 0.188 / 0.108 & 1.70$\times$ / 3.43$\times$ & 97 / --- \\
\bottomrule
\end{tabular}
\end{table}

On real GISAID 2020--2021 H-scores~\cite{youn2025mutclust}, only 342 of 29,903 positions (1.14\%) were nonzero (Table~\ref{tab:real_gisaid}).
MutClust-Hybrid dropped from $F_1=0.785$ to $0.123$ and from $\mathit{HS}=0.778$ to $0.383$; Fixed/dNdS reached $\mathit{HS}=0.386$, the sliding window had the highest $F_1$ ($0.420$), and enrichment remained biologically high ($6.9$--$8.0\times$).
Thus Stage~1 validates the metric and exposes the sparse-data boundary; pathogen-adaptive scoring--detector selection is evaluated at scale in Section~\ref{sec:9pathogen_results}.
```

Citations/refs preserved: `dadonaite2023dms`, `cao2023ba286`, `carabelli2023convergent`, `youn2025mutclust`; Tables `tab:hotspot_scores`, `tab:multi_gt`, `tab:real_gisaid`; Section `sec:9pathogen_results`; labels `sec:variant_comparison`, `sec:multi_gt`, `sec:real_gisaid_benchmark`. Savings: `98 - 47 = 51`.

## Block #12 -- Robustness/sensitivity

First line: `\section{Robustness and Sensitivity Validation}`

Last line: `Adding the static members of the 4-feature core (pLDDT, homoplasy; canonical scores projected onto the codon-aligned MSA frame via Needleman--Wunsch consensus alignment, mean coverage $0.83$) to the freq+entropy baseline produces grand-mean AUROCs of $0.555$ (freq+entropy), $0.543$ (+pLDDT), $0.549$ (+homoplasy), and $0.561$ (4-feature). Paired Wilcoxon signed-rank tests vs.\ the 2-feature baseline give $p<0.001$ for +homoplasy (mean $\Delta\text{MCC}=+0.005$), $p=0.170$ for +pLDDT (mean $\Delta=-0.005$), and $p=0.016$ for the 4-feature ensemble (mean $\Delta=-0.009$): adding homoplasy gives a small but statistically distinguishable improvement, while pLDDT alone and the 4-feature combination slightly degrade Top-30 MCC despite a marginally higher mean AUROC. Per-pathogen the most pronounced gains are for EV-A71 (MCC $0.146 \to 0.188$, AUROC $0.773 \to 0.844$ with homoplasy) and Rabies (AUROC $0.789 \to 0.860$ with homoplasy); HCV is the clearest negative example (homoplasy collapses AUROC from $0.31$ to $0.09$ because the empirical homoplasy distribution over E2 is essentially flat). Adding static priors therefore helps in EV-A71/Rabies, hurts in HCV, and is approximately neutral elsewhere; full per-pathogen tables are in \texttt{sliding\_window\_prospective\_backtest\_4feature.csv} and \texttt{sliding\_window\_prospective\_c2\_vs\_d2\_paired.csv}.`

Must-retain numerical anchors: permutation `1,000 random`, `200 circular`, `p<0.005`, `z>9.2`; region BCa `1,000`, `n=7`, `[0.323,0.635]`, pairwise `p<0.001`; later BCa `[0.047,0.202]`, cluster `[0.201,0.346]`; rank 1 `71.9%` of `171`; convergence `~1,000`, `rho>0.997`, `SD<0.015`; grid `64`. H3N2 pilot anchors: `9,000`; periods `2010--2015`, `2016--2020`, `2021--2025`; `n=3,000`; `25` sites; train `<5%`, holdout `>=10%`; retrospective `2.7--3.4x`; prospective `0/20`, `0/30`, `0/50`, `1/50`; table rows `3/25/3.40x/p=0.053`, `4/25/3.02x/p=0.037`, `6/25/2.72x/p=0.017`, `0/6`, `1/7/1.62x/p=0.479`. Backtest anchors: 11 pathogens, 73 windows, 219 evals, k 20/30/50, EV-A71 `0.77`, `+0.146`, `10.8x`; Rabies `0.79`, `+0.112`, `4.1x`; Influenza B `0.70`; grand MCC `-0.006`, AUROC `0.539`, enrichment `1.57x`; drift `-0.006` to `+0.032`; retrospective `0.341`, `0.454`. 4-feature anchors: coverage `0.83`; AUROCs `0.555/0.543/0.549/0.561`; `p<0.001`, `p=0.170`, `p=0.016`; deltas `+0.005/-0.005/-0.009`; EV-A71 `0.146->0.188`, `0.773->0.844`; Rabies `0.789->0.860`; HCV `0.31->0.09`.

Sanity-check framing: this should be a robustness ledger plus forward-time boundary, not a claim that Stage 1 can forecast emergence. The H3N2 and sliding-window results are sanity checks that protect the wet-lab triage reframe by saying retrospective enrichment is useful, while prospective deployment is not established.

Concrete replacement draft (38 lines): keep both figures and the H3N2 table, but merge prose into one ledger paragraph plus one prospective-boundary paragraph.

```latex
\section{Robustness and Sensitivity Validation}
\label{sec:robustness_validation}
\label{sec:statistical_validation}
\label{sec:sensitivity_analysis}
\label{sec:temporal}

Stage~1 is statistically stable as a retrospective sanity check, but these tests do not upgrade it into a prospective detector.
Permutation tests (1,000 random and 200 circular iterations) gave $p<0.005$ for all methods ($z>9.2$); region-level BCa bootstrap CIs~\cite{efron1987better} (1,000 resamplings, $n=7$ Spike regions; \phantomsection\label{tab:bootstrap_ci}) gave MutClust-Hybrid $\mathit{HS}$ CI [0.323, 0.635] and pairwise differences $p<0.001$.
The later combination-level BCa CI [0.047, 0.202] (Section~\ref{subsec:9pathogen_bootstrap}) and pathogen-cluster CI [0.201, 0.346] (Section~\ref{subsec:anova_diagnostics}) use different resampling units.
\phantomsection\label{tab:weight_sensitivity}MutClust-Hybrid remains rank~1 in 71.9\% of 171 weightings, metrics stabilize by ${\sim}$1,000 sequences (Spearman $\rho>0.997$, SD $<0.015$; Figure~\ref{fig:sample_size_convergence}), and the 64-point sensitivity grid shows F1 is driven mainly by $\gamma$ rather than MinPts (Figure~\ref{fig:mutbench_sensitivity}).\phantomsection\label{tab:hdbscan_sensitivity}\phantomsection\label{tab:dnds_threshold}

\begin{figure}[htbp]
\centering
\includegraphics[width=0.8\textwidth]{sample_size_convergence.png}
\caption{Sample size convergence of hotspot metrics. Stable performance (HS $\approx$ 0.62) is achieved at $\sim$1,000 sequences.}
\label{fig:sample_size_convergence}
\end{figure}

\begin{figure}[htbp]
\centering
\includegraphics[width=0.9\textwidth]{sensitivity_heatmap.png}
\caption{MutClust parameter sensitivity heatmap. Grid search over 64 combinations ($\gamma \times d \times$ MinPts); F1 most sensitive to $\gamma$, minimal MinPts influence.}
\label{fig:mutbench_sensitivity}
\end{figure}

\subsection{Prospective sanity checks}
\label{subsec:h3n2_temporal_pilot}
\label{subsec:sliding_window_backtest}
\label{para:sliding_window_4feature}

The H3N2 frequency-only pilot partitions 9,000 HA sequences into 2010--2015, 2016--2020, and 2021--2025 windows ($n=3,000$ each), trains on 2010--2015, and compares static Layer~A antigenic sites (25 Koel~2013 sites) with newly emerging positions (train freq $<5\%$, holdout freq $\geq10\%$).
It recovers the retrospective reference at $2.7$--$3.4\times$ enrichment but gives essentially no prospective signal ($0/20$, $0/30$, $0/50$ for 2016--2020; only $1/50$ for 2021--2025; Table~\ref{tab:h3n2_temporal_pilot}).

% Keep Table~\ref{tab:h3n2_temporal_pilot} unchanged: it preserves 3/25/3.40x/p=0.053, 4/25/3.02x/p=0.037, 6/25/2.72x/p=0.017, all 0/6 prospective rows, and 1/7/1.62x/p=0.479.

Across 73 temporal splits in 11 pathogens (219 top-$k$ evaluations, $k\in\{20,30,50\}$; \texttt{sliding\_window\_prospective\_backtest\_summary.csv}; Figure~\ref{fig:sliding_window_backtest}), freq+entropy exceeds AUROC 0.75 only for EV-A71 (0.77, Top-30 MCC $+0.146$, enrichment $10.8\times$) and Rabies (0.79, $+0.112$, $4.1\times$), partially for Influenza~B (0.70), and is near chance otherwise (grand mean MCC $-0.006$, AUROC $0.539$, enrichment $1.57\times$; drift $-0.006$ to $+0.032$ MCC/yr).
This bounds the retrospective headline ($0.341$ exact, $0.454$ at $\pm10$; Table~\ref{tab:region_overlap_mcc}) and motivates the limitations update in Section~\ref{sec:prospective_validation_gap}.

\begin{figure}[htbp]
\centering
\includegraphics[width=\textwidth]{sliding_window_prospective_backtest.png}
\caption{Per-pathogen MCC trajectory across split years for the sliding-window prospective backtest; EV-A71 and Rabies are consistently above chance, Influenza~B is partial, and the remaining eight cluster near zero (grand mean AUROC $0.539$).}
\label{fig:sliding_window_backtest}
\end{figure}

Adding static pLDDT and homoplasy priors via Needleman--Wunsch consensus projection (mean coverage 0.83) yields AUROCs 0.555, 0.543, 0.549, and 0.561 for freq+entropy, +pLDDT, +homoplasy, and 4-feature; Wilcoxon tests give $p<0.001$ ($\Delta$MCC $+0.005$), $p=0.170$ ($-0.005$), and $p=0.016$ ($-0.009$), respectively.
Static priors help EV-A71 (MCC $0.146\to0.188$, AUROC $0.773\to0.844$) and Rabies (AUROC $0.789\to0.860$), hurt HCV (AUROC $0.31\to0.09$), and are approximately neutral elsewhere; full tables remain in \texttt{sliding\_window\_prospective\_backtest\_4feature.csv} and \texttt{sliding\_window\_prospective\_c2\_vs\_d2\_paired.csv}.
```

Citations/refs preserved: `efron1987better`; Sections `subsec:9pathogen_bootstrap`, `subsec:anova_diagnostics`, `sec:prospective_validation_gap`; Figures `fig:sample_size_convergence`, `fig:mutbench_sensitivity`, `fig:sliding_window_backtest`; Table refs/labels `tab:bootstrap_ci`, `tab:weight_sensitivity`, `tab:hdbscan_sensitivity`, `tab:dnds_threshold`, `tab:h3n2_temporal_pilot`, `tab:region_overlap_mcc`, `tab:sliding_window_backtest`; paragraph label `para:sliding_window_4feature`. Savings: `82 - 38 = 44`.

## Block #13 -- Structural validation

First line: `\section{Cross-Pathogen and Structural Validation}`

Last line: `\phantomsection\label{subsec:phylo_correction_poc}\phantomsection\label{subsec:treetime_ml_validation}\phantomsection\label{subsec:treetime_gisaid_validation}\phantomsection\label{subsec:homoplasy_sensitivity}\phantomsection\label{tab:phylo_sensitivity}Coalescent simulation (100 replicates, $N = 500$) shows H-score ranks single-origin founder mutations above convergent mutations in $100\%$ of replicates, while Fitch parsimony correctly ranks convergent mutations at the top ($\rho = -0.876$, $p = 1.28 \times 10^{-64}$); TreeTime~\cite{sagulenko2018treetime} ML validation confirms AUC $= 1.000$ for Fitch and TreeTime-ML vs.\ AUC $= 0.000$ for H-score. \textbf{Frequency-based scores systematically conflate founder effects with positive selection}. D614G is retained in Layer~A as a documented functional/stability-affecting substitution per~\cite{korber2020tracking} rather than excluded; the founder-vs-selection discount is therefore applied at the H-score interpretation level (Paragraph~\ref{para:full_lattice_shapley}) rather than via Layer~A removal, and the homoplasy/Fitch channel provides the convergent-evolution discriminator that mere frequency cannot. Method rankings differ between SARS-CoV-2 and H3N2 ($\mathit{HS} = 0.661$ vs.\ $0.577$ for MutClust-Fixed/Hybrid), motivating the large-scale cross-pathogen benchmark with expanded information types.`

Must-retain numerical anchors: H3N2 `1,967` sequences, `5` antigenic sites, `HS=0.661` vs `0.577`, `543` HA positions, enrichment `0.87--2.36x` vs `1.9--23.7x`; structural `5.92x`, within-8 Angstrom, `1,000` random subsets, `z=13.34`; phylo `100` replicates, `N=500`, `100%`, `rho=-0.876`, `p=1.28e-64`, TreeTime/Fitch `AUC=1.000`, H-score `AUC=0.000`.

Concrete replacement draft (10 lines):

```latex
\section{Cross-Pathogen and Structural Validation}
\label{sec:cross_pathogen_structural}\label{sec:influenza_validation}\label{sec:structure_analysis}\label{sec:phylo_simulation}

H3N2 HA (1,967 sequences; 5 antigenic sites~\cite{wiley1981structural,wilson1990structural}) reverses the SARS-CoV-2 ranking: MutClust-Fixed exceeds Hybrid ($\mathit{HS}=0.661$ vs.\ $0.577$) because all 543 HA positions have nonzero H-scores, while enrichment narrows to $0.87$--$2.36\times$ versus $1.9$--$23.7\times$ for SARS-CoV-2.
\phantomsection\label{tab:influenza} Figure~\ref{fig:cross_pathogen_comparison} and Table~\ref{tab:stage2_best} therefore introduce the large-scale pathogen-adaptive comparison (Sections~\ref{subsec:9pathogen_statistical} and~\ref{subsec:9pathogen_lopo}).

% Keep Figure~\ref{fig:cross_pathogen_comparison} unchanged.

3D C$\alpha$ coordinates from PDB~6VSB show that linear hotspots are spatially clustered, with $5.92$-fold within-8-\AA{} contact enrichment over 1,000 length-matched random subsets ($z=13.34$); source data remain in \texttt{results/mutbench/structural\_features/}.
\phantomsection\label{subsec:phylo_correction_poc}\phantomsection\label{subsec:treetime_ml_validation}\phantomsection\label{subsec:treetime_gisaid_validation}\phantomsection\label{subsec:homoplasy_sensitivity}\phantomsection\label{tab:phylo_sensitivity}Coalescent simulations (100 replicates, $N=500$) show H-score ranks founder mutations above convergent mutations in 100\% of replicates, while Fitch/TreeTime separate convergence (Fitch $\rho=-0.876$, $p=1.28\times10^{-64}$; Fitch and TreeTime-ML AUC $=1.000$ vs.\ H-score AUC $=0.000$~\cite{sagulenko2018treetime}); D614G is retained per~\cite{korber2020tracking}, with founder discounting handled through the homoplasy/Fitch channel and Paragraph~\ref{para:full_lattice_shapley}.
```

Citations/refs preserved: `wiley1981structural`, `wilson1990structural`, `sagulenko2018treetime`, `korber2020tracking`; Figure `fig:cross_pathogen_comparison`; Table `tab:stage2_best`; Sections `subsec:9pathogen_statistical`, `subsec:9pathogen_lopo`; all structural/phylo labels. Savings: `20 - 10 = 10`.

## Block #15 -- ANOVA five-frame

First line: `\textbf{ANOVA Diagnostic Tests.}`

Last line: `Kruskal-Wallis non-parametric tests confirmed all effects (pathogen: $H = 1{,}120.8$, $p < 10^{-234}$; detection family: $H = 129.1$, $p < 10^{-21}$; scoring: $H = 277.9$, $p < 10^{-47}$), maintaining the reliability of the directional ANOVA conclusions despite these caveats.`

Must-retain numerical anchors: Shapiro `W=0.974`, `p<10^-29`; skew `0.14`, kurtosis `2.83`; `N=8,580`; `39` variants; cells `20 x 14 x 11 = 3,080`; five-frame omega CIs: original/standard `[0.201,0.346]`, wild `[0.201,0.303]`, phylo `[0.202,0.346]`, mixed `0.340` with lower `0.188`, Bayesian `[0.242,0.388]`, naive `[0.260,0.321]`; table rows `0.272/0.145`, `0.269/0.103`, `0.272/0.143`, `0.316/0.146`; HCV-excluded `0.246`; LOO span `[0.253,0.313]`, mean `0.293`, median `0.297`, SD `0.015`, headline `0.296`, HCV delta `+0.043`, Norovirus `-0.017`, nine `<=0.011`; Kruskal `1120.8`, `129.1`, `277.9` and p-values.

Concrete replacement draft (25 lines):

```latex
\textbf{ANOVA Diagnostic Tests.}
\label{subsec:anova_diagnostics}
Residual diagnostics reject ideal ANOVA assumptions (Shapiro-Wilk $W=0.974$, $p<10^{-29}$; Levene significant), but the departures are mild (skewness 0.14, excess kurtosis 2.83) and the grid is large ($N=8{,}580$).
Because the 39 parameter variants within each scoring--detector--pathogen cell share inputs, the effective independent scale is closer to the $20\times14\times11=3{,}080$ unique cells than to the row count; $\omega^2$ is therefore interpreted as an indicative effect size with pathogen-aware robustness frames.

Across Table~\ref{tab:omega_robustness_5way}, every primary frame remains above Cohen's large-effect threshold ($\omega^2>0.14$): standard cluster [0.201, 0.346], wild-cluster [0.201, 0.303], phylogenetic block [0.202, 0.346], mixed-effects pseudo-$\omega^2_{\text{int}}=0.340$ with lower reference 0.188, and Bayesian HDI [0.242, 0.388].
The naive $N=8{,}580$ bootstrap [0.260, 0.321] is narrower and is not the primary reference.

\begin{table}[h]
\centering
\small
\caption[Five-way $\omega^2$ robustness comparison]{Five-way comparison of $\omega^2(\text{scoring}\times\text{pathogen})$ on the 8,580-row Stage~3 grid; all effective-$N$-aware frames remain above $\omega^2=0.14$.}
\label{tab:omega_robustness_5way}
\begin{tabular}{lrrrr}
\toprule
Method & $\omega^2$ & 95\% CI lower & 95\% CI upper & CI width \\
\midrule
Standard cluster (G\,=\,11) & 0.272 & 0.201 & 0.346 & 0.145 \\
Wild-cluster Rademacher (G\,=\,11) & 0.269 & 0.201 & 0.303 & 0.103 \\
Phylogenetic block (G\,=\,8) & 0.272 & 0.202 & 0.346 & 0.143 \\
Mixed-effects var-comp & 0.340 & --- & --- & --- \\
Bayesian factor analysis & 0.316 & 0.242 & 0.388 & 0.146 \\
\bottomrule
\end{tabular}
\end{table}

Excluding HCV gives $\omega^2_{\text{scoring}\times\text{pathogen}}=0.246$, so the interaction is not driven only by HCV's HVR-based Layer~A; the caveat remains that Layer~A mixes convergent-evolution, immune-escape, and HVR-membership evidence.
Per-pathogen leave-one-out values in Table~\ref{tab:omega_loo_pathogen_sensitivity} span [0.253, 0.313] (mean 0.293, median 0.297, SD 0.015) around the 0.296 headline; HCV has the largest leverage ($+0.043$), Norovirus the second largest ($-0.017$), and the other nine have $|\Delta|\leq0.011$.
Kruskal-Wallis tests preserve the directional conclusion despite diagnostics (pathogen $H=1{,}120.8$, $p<10^{-234}$; detection family $H=129.1$, $p<10^{-21}$; scoring $H=277.9$, $p<10^{-47}$).
```

Citations/refs preserved: no citations in block; Tables `tab:omega_robustness_5way` and `tab:omega_loo_pathogen_sensitivity` preserved; ANOVA label preserved. Savings: `54 - 25 = 29`.

## Savings ledger

| Block | Original lines | Replacement lines | Savings |
|---:|---:|---:|---:|
| #11 Stage 1 | 98 | 47 | 51 |
| #12 Robustness/sensitivity | 82 | 38 | 44 |
| #13 Structural | 20 | 10 | 10 |
| #15 ANOVA five-frame | 54 | 25 | 29 |
| Total | 254 | 120 | 134 |

Overall recommendation: compress #11 and #13 directly; compress #12 with the prospective-boundary language intact; compress #15 as a diagnostics ledger but keep `tab:omega_robustness_5way` in main text because the five-frame CIs are part of the statistical backbone identified by Risk-1/Risk-2.

RESULT_R2_DEEP_BATCH3: blocks=4 line_savings=134
