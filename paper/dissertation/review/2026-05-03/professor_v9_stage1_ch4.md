# Chapter Deep Eval: ch4_results

## In-scope rubric items
- C
- D
- E
- F
- G

## Per-item evidence

### C
**Strongest evidence**:
- Stage 2 methods are concretely enumerated: "20 scoring types ... combined with 14 detection method families ... 39 parameter variants ... across 11 pathogens, totaling ... 8,580 evaluations" (lines 206-209).
- The metric choice is justified rather than assumed: "Stage~2 uses MCC rather than hotspot-score because the stability component ... has not been cross-validated across all 11 pathogens" and MCC is "robust to class imbalance" (line 213).
- Statistical method triangulation is detailed: three-way ANOVA, LOPO, Friedman/Nemenyi, BCa bootstrap, permutation nulls, cluster/wild/phylogenetic block robustness frames, and DMS/escape audits are all reported with parameters and archives (lines 329-439, 459-508, 543-570, 906-949).

**Weakest evidence / gaps**:
- Several analyses reuse the same 8,580-row data; the chapter admits "The three lenses are consistency checks on the same data, not independent replications" (line 371) and later "only the ANOVA ... provides positive evidence" (line 586). Methodological breadth is high, but independence is limited.
- ANOVA assumptions fail: "Shapiro-Wilk ... p<10^{-29}; Levene significant for all factors" and effective independence is "closer to ... 3,080 unique cells" (line 461). The chapter handles this, but it weakens any literal variance-decomposition reading.

**Hidden issues for panel awareness**:
- A source-level micro-inconsistency: Table `stage2_best` claims "all 11 pathogens exhibit unique best combinations" (line 238), but the footnote says Influenza B and MERS share both freq and KDE p=85, so "only 10 of the 11 best-combinations are unique tuples" (line 262). The headline box also says "All 11 pathogens have unique best combinations" (line 12). Panel should score the corrected footnote, but note the headline slip.
- Scope changes are easy to miss: the main benchmark is 11 pathogens, but feature ablation and cold-start use "12 pathogens including Zika" (lines 608, 612, 637-660, 862-867). This is defensible but should not be conflated with the 11-pathogen Stage 2 evidence.

**Suggested score range**: 8.0--8.8

### D
**Strongest evidence**:
- Scale is explicit and broad: "8,580 evaluations (20 scoring formulas x 39 detection parameter variants ... x 11 pathogens)" (line 223).
- Breadth spans "six information categories" including frequency, MSA-derived, phylogenetic, structural, AI-based, and composite channels (line 224), with 10 underlying biological features (lines 209-211, 598-603).
- Validation breadth includes DMS for 6 pathogens (line 226), prospective temporal splits "Across 73 temporal splits in 11 pathogens" (line 164), and vaccine/antibody escape for 3 pathogens with "2,340 enrichment evaluations" (lines 906-907).

**Weakest evidence / gaps**:
- External escape validation is narrow and convenience-selected: "feasible for only 3 of 11 pathogens" and should be read as a "data-availability convenience sample rather than a balanced subset" (line 946).
- The nominally large row count partly overstates independent sample size because 39 variants share inputs; the chapter says independent scale is closer to 3,080 cells than 8,580 rows (line 461), and pathogen clusters are only 11.

**Hidden issues for panel awareness**:
- The opening says Stage 2 extends to "11 RNA viruses" (line 7), but several later claims use "12-pathogen feature panel (core 11 + Zika)" (line 608). The extra Zika improves some cold-start diagnostics but is outside the main 11-pathogen result.
- Panel size is biologically broad but statistically small for cluster inference; the chapter cites G=11 cluster frames (lines 463-477) and future 20-30+ pathogen stability targets (line 670). This helps maturity but caps scale scoring.

**Suggested score range**: 8.0--8.7

### E
**Strongest evidence**:
- The results reading is carefully tempered: uniqueness is not overclaimed because "probability of all 11 being unique by chance ... approximately 93%" and the real finding is the "mean MCC gap = 0.265" (lines 266-269).
- The ANOVA headline is bounded: "largest source" is explicitly narrowed to "largest modeled component"; residual omega is "comparable in magnitude" (line 367).
- LOPO/Friedman are correctly framed as weak corroborations: "LOPO is therefore reported as corroboration ... rather than as independent positive evidence" (line 582), and "only the ANOVA ... provides positive evidence" (line 586).

**Weakest evidence / gaps**:
- Some interpretive language still overshoots locally. The worst-end paragraph says the negative-MCC fraction is "exactly what pathogen-dependent optimality predicts" (line 273), which is rhetorically stronger than the data require; bad cells also follow from noisy detectors, weak labels, and class imbalance.
- The DMS section says "In all 6 pathogens, the best scoring type differs ... confirming their independence" in the table caption (line 553), but the prose later backs off to "non-identical aspects" and notes RSV positive agreement (line 570). The caption is too strong.

**Hidden issues for panel awareness**:
- The chapter often rescues claims in footnotes or later caveats. A bulk reader may remember "0/11" and "all unique" as strong independent evidence; the actual careful reading says both are null-consistent (lines 267, 400, 421-425, 582).
- MERS is explicitly a failure case despite perfect recall: precision 0.045, 200/1,330 positions flagged, "not a basis for claiming successful generalization" (line 541). This is an important guardrail for interpretation.

**Suggested score range**: 8.2--9.0

### F
**Strongest evidence**:
- The chapter states a concrete contribution: "statistical demonstration that the most predictive biological information source is pathogen-dependent" (line 221).
- It quantifies novelty beyond the intuitive "different pathogens differ" claim: interaction omega 0.296, scoring main effect 0.063, detection-family main effect 0.013, and oracle-vs-generalized gap 0.265 (lines 269, 336-369, 379-404).
- The result is biologically interpreted per pathogen, with 9 distinct scoring types and rationales spanning phylogenetic, PLM, homoplasy, entropy, stability, semantic change, and frequency (lines 246-263, 282-309).

**Weakest evidence / gaps**:
- The contribution is benchmark/triage evidence, not a new deployable detector; the chapter repeatedly says "retrospective triage, not deployment" (lines 672-674, 809-811). Novelty should be scored as empirical framing and benchmark synthesis, not operational ML breakthrough.
- Some novelty depends on internal benchmark construction. Independent disjoint pathogen-panel replication is "deferred to future work" (line 371), limiting how definitive the contribution can be.

**Hidden issues for panel awareness**:
- "Information type dominates detection algorithm" is strong within this grid, but residual/unmodeled variance is large and family x pathogen remains medium (lines 338-350, 367). The novelty is not that detectors are irrelevant; it is that scoring x pathogen is the largest modeled component.
- The chapter’s own adaptive-weighting failures (HBFWS, Cycle 7B) make the contribution more negative and mature: "adaptive selection is not supported at n=11 under the tested feature, label, and validation regime" (line 831). This helps novelty as a bounded negative result.

**Suggested score range**: 8.0--8.8

### G
**Strongest evidence**:
- Practical triage is directly operationalized: Cold-Start computes homoplasy, pLDDT, entropy, frequency, averages within-pathogen z-scores, and thresholds top 10% (lines 672-699).
- The claimed utility is concrete search-space reduction: "narrows roughly 1,000 positions to 20--80 candidates with 7--9x escape enrichment" (line 674) and for 500 positions to "approximately 10--50 positions" (lines 951-952).
- External/practical anchor is strongest for HIV-1: "7.19x enrichment," "82% Layer-A-disjoint," "novel-only p_adj approx 3.9 x 10^{-9}" (lines 923-937, 941-942).

**Weakest evidence / gaps**:
- Deployment is refused: "0/12 folds are callable" and "formally abstained from deployment" (lines 809-811). This is correct for safety, but it limits practical value to ranking/screening-budget allocation.
- Prospective transfer is weak: H3N2 frequency pilot has "essentially no prospective signal" (line 131), and multi-pathogen backtest grand mean is "MCC -0.006, AUROC 0.539" (line 164). Retrospective triage value does not yet equal forward surveillance value.

**Hidden issues for panel awareness**:
- The strongest practical escape validation is HIV-1 single-scoring freq+Wavelet, while EqualWeight HIV-1 uses a different pipeline and lacks fixed-threshold integration (lines 930-937, 941). Bulk readers may over-merge these as one unified practical pipeline.
- H3N2 escape enrichment is mostly circular/self-consistency: "8 of those 9 are already in Layer A" and novel-only Fisher p=0.132 (line 944). HIV-1 is the main practical external anchor, not H3N2.

**Suggested score range**: 7.3--8.2

## Cross-cutting observations

- The v228 wet-lab triage reframing is mostly preserved. The strongest lines explicitly say "candidate prioritization rather than a universal detector" (line 598), "not a prospectively callable detector" (line 635), "deployment refused" (line 716), and "ranked screening-budget allocator, not a calibrated-probability model" (line 803).
- Hidden consistency risk: the headline/key-results and table caption still contain stronger "all 11 unique" phrasing than the corrected footnote supports (lines 12, 238, 262).
- The chapter is unusually transparent about failed or negative results: prospective backtests, MERS saturation, DMS divergence, null calibration, Layer A' failure, and adaptive-weighting failures all constrain claims rather than inflate them.
- Panel-level scoring should separate strong retrospective benchmark maturity from weaker prospective/deployment maturity.

## Bottom line for Stage 2 panel

Chapter 4 is strongest as a mature, detail-aware retrospective benchmark showing that biological scoring information is pathogen-dependent within a broad 20 x 39 x 11 design. The panel should notice that the load-bearing evidence is the scoring x pathogen interaction with cluster-aware robustness plus the HIV-1 escape anchor; LOPO 0/11, "unique best combinations," and Friedman are explicitly weak/null-consistent corroborations. Practical value is real for wet-lab candidate triage, but the chapter itself refuses deployable-detector framing after poor prospective/callability audits.

RESULT_PROF_V9_STAGE1_ch4: in_scope_items=5 hidden_issues=10 recommended_score_floor=7.3 recommended_score_ceiling=9.0
