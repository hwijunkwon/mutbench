# Risk-3 Deep Abstract Draft

## 1. Complete replacement `abstract.tex` content

```latex
% Abstract
MutBench is a region-level, single-position hotspot-prioritization benchmark for 11 RNA-virus surface glycoproteins, designed for retrospective wet-lab triage rather than prospective deployment. Its practical value is search-space reduction: for a typical viral protein, optimal scoring--detection combinations narrow roughly 1{,}000 positions to about 10--50 candidate sites, with the primary HIV-1 external anchor showing $7.19\times$ escape enrichment ($p_{\text{adj}} = 2.5 \times 10^{-16}$), $82\%$ Layer-A-disjoint support, and 37 of 45 novel prioritized sites. Across 10 biological information types (20 scoring formulas), 14 detection families (39 variants), and 11 pathogens, MutBench contains 8{,}580 evaluations under gap-aware single-position scoring with substitutions only as ground-truth labels.

The benchmark uses a three-layer ground-truth system: Layer~A literature-curated positive markers combining convergent evolution, immune escape, and hypervariable-region evidence; Layer~B conserved structural regions under purifying selection as negative controls; and Layer~C deep-mutational-scanning fitness data as functional validation. Stage~1 checks the framework on SARS-CoV-2, Stage~2 performs the cross-pathogen comparison, and Stage~3 evaluates multi-source integration. The composite hotspot score averages recall, precision, and stability, while MCC and enrichment analyses provide the main interpretive anchors.

The main evidence is summarized below.

\begin{table}[htbp]
\centering
\caption{Main evidence ledger for MutBench}
\label{tab:abstract_evidence_ledger}
\small
\begin{tabularx}{\textwidth}{p{0.22\textwidth}p{0.32\textwidth}p{0.22\textwidth}X}
\toprule
\textbf{Claim} & \textbf{Statistic} & \textbf{Boundary} & \textbf{Defense role} \\
\midrule
Wet-lab triage value & Search space reduced from $\sim$1{,}000 positions to $\sim$10--50 candidates; HIV-1 $7.19\times$ ($p_{\text{adj}} = 2.5 \times 10^{-16}$), $82\%$ Layer-A-disjoint, 37 of 45 novel; H3N2 $9.36\times$; SARS-CoV-2 $7.63\times$ exploratory & Retrospective; external escape-enrichment annotation available for 3/11 pathogens; H3N2 is a self-consistency check and SARS-CoV-2 is exploratory after Bonferroni & Shows practical prioritization economics without claiming prospective detector readiness \\
Benchmark scale and scope & 10 information types (20 scoring formulas) $\times$ 14 detection families (39 variants) $\times$ 11 pathogens = 8{,}580 evaluations; three-layer ground truth & RNA-virus surface glycoproteins; region-level, single-position, gap-aware scoring; substitution labels only & Establishes the benchmark contribution and the tested regime \\
Pathogen-dependent information utility & $\omega^2_{\text{scoring}\times\text{pathogen}} = 0.296$ with 11-pathogen cluster-bootstrap 95\% CI [0.201, 0.346]; 6-category aggregation $\omega^2 = 0.103$ & Layer~A partly couples pathogen biology to curation protocol & Primary statistical evidence that information choice is pathogen-specific \\
Non-deployability at current panel size & Friedman $p = 0.990$; LOPO 0/11 exact matches; HBFWS $p = 0.78$; six further Cycle~7B adaptive paradigms fail; Wave~5 Layer~A$'$ mean MCC $= -0.055$ & Not learnable at $n=11$, under the tested labels, features, detectors, and validation regime; Bolker 20--30 pathogen guidance is a design target, not a phase transition & Converts adaptive-selection failures into a bounded finite-panel non-deployability result \\
\bottomrule
\end{tabularx}
\end{table}

The headline result is therefore not a universal detector claim. MutBench finds strong retrospective signal, but the optimal information source is pathogen-dependent: FUBAR-like phylogenetic selection is strongest for H3N2, protein-language-model channels dominate for SARS-CoV-2 and RSV, and homoplasy is strongest for Norovirus. At $n=11$, under the tested regime, a deployable cross-pathogen adaptive selector is not learnable: LOPO 0/11, HBFWS $p = 0.78$, and the six Cycle~7B adaptive paradigms all fail despite detectable oracle signal. The Bolker 20--30 pathogen rule-of-thumb is used only as a future design target for more stable random-effect and adaptive-selection estimates, not as evidence that 20--30 pathogens will suffice.

Thus, MutBench contributes a broad RNA-virus hotspot benchmark, a quantified pathogen-by-information interaction, and a guarded wet-lab triage result. The practical anchor is HIV-1 Layer-A-disjoint escape enrichment, supported secondarily by H3N2 self-consistency and SARS-CoV-2 exploratory enrichment, while the negative audits delimit what the present panel cannot support: at $n=11$, under the tested regime, a calibrated prospective cross-pathogen detector is not learnable.

\vspace{1em}
\noindent\textbf{Keywords}: mutation hotspot detection, MutBench, biological information types, viral genomics, wet-lab triage, pathogen-dependent optimality, vaccine escape, Deep Mutational Scanning
```

## 2. Word-by-word anchor audit

All required anchors are present in the replacement text:

1. `HIV-1 7.19×`: present as `HIV-1 $7.19\times$`.
2. `p_adj=2.5e-16`: present as `$p_{\text{adj}} = 2.5 \times 10^{-16}$`.
3. `82% disjoint`: present as `$82\%$ Layer-A-disjoint`.
4. `37 of 45 novel`: present exactly as `37 of 45 novel`.
5. `H3N2 9.36×`: present as `H3N2 $9.36\times$`.
6. `SARS 7.63× exploratory`: present as `SARS-CoV-2 $7.63\times$ exploratory`.
7. `ω²=0.296 CI [0.201, 0.346]`: present as `$\omega^2_{\text{scoring}\times\text{pathogen}} = 0.296$ ... 95\% CI [0.201, 0.346]`.
8. `LOPO 0/11`: present as `LOPO 0/11`.
9. `HBFWS p=0.78`: present as `HBFWS $p = 0.78$`.
10. `Cycle 7B 6 paradigms`: present as `six further Cycle~7B adaptive paradigms fail`.
11. `Wave 5 MCC=-0.055`: present as `Wave~5 Layer~A$'$ mean MCC $= -0.055$`.
12. `8,580 evaluations`: present as `8{,}580 evaluations`.
13. `11 pathogens`: present in the opening and ledger as `11 pathogens`.

Additional guardrail audit:

- Wet-lab triage leads the abstract and is quantified as `~1,000 -> ~10--50`.
- No claim says `20--30 will suffice`; the draft says Bolker 20--30 pathogen guidance is a design target, not a phase transition.
- Both `not learnable` claims are paired with `at n=11, under the tested regime`.
- The ledger has exactly 4 rows.

## 3. Length comparison

- Current `abstract.tex`: 34 lines.
- Replacement abstract content above: 30 lines inside the LaTeX block, counting `% Abstract`, blank lines, and table lines.
- Length change: -4 lines.

RESULT_R3_DEEP_DRAFT: anchors=13/13 length_change=-4 lines ledger_rows=4
