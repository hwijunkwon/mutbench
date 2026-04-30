# MutBench dissertation — additional-experiment proposals (defense prep)

You are reviewing a near-final PhD dissertation (225 pages, defense within weeks). The
candidate's biggest concern is that the dissertation lacks a "plausible method"
(novelty in the algorithmic contribution). Your task is to propose **additional
experiments to run** that would strengthen the method/defense, ranked by ROI.

## Repository state (read these before proposing)

- Build: `/proj/paper/paper/dissertation/thesis_en.pdf` (225 pp, post-v180)
- Chapters: `/proj/paper/paper/dissertation/chapters_en/{ch1_introduction,ch2_background,ch3_methods,ch4_results,ch5_discussion}.tex`
- Bib: `/proj/paper/paper/dissertation/references.bib`
- Result CSVs: `/proj/paper/results/mutbench/*.csv` (8,580 Stage 3 evals; feature ablation; HBFWS; Cycle 7B; 30-pathogen pilot)
- Scripts: `/proj/paper/scripts/*.py`

## Method contribution (current state)

- **Contribution 3**: search-space reduction (~1000 alignment positions → 20–80;
  7–9× enrichment for escape sites; primary anchor = HIV-1 7.19× Bonferroni
  p=2.5e-16; H3N2 9.36× and SARS-CoV-2 7.63× as secondary).
- **Algorithm 1 (newly added v180)**: 2-tier MutBench Cold-Start.
  - Tier 1 (universal, ~10 min CPU): 4-feature uniform z-score ensemble
    (homoplasy + pLDDT + entropy + frequency) with directional sign + top-10% threshold.
    Formal pseudocode at `chapters_en/ch4_results.tex` §`para:mutbench_algorithm`,
    Algorithm `alg:mutbench_coldstart`.
  - Tier 2 (provisional, requires ICTV family annotation): family-prior single-best
    scoring substitution; not yet validated on held-out families.
- **Baseline progression (Table 3.14, newly added v180)**: single feature MCC=0.015
  (≈ noise floor), Cold-Start 4-core 0.0809, full-10 0.0698, oracle best 4-of-210
  (label-selected) 0.0950. Cold-Start sits +0.011 above full-10 and only -0.014
  below oracle without using held-out labels.

## Negative-result evidence (already in dissertation, do NOT propose to repeat)

1. LOPO 0/11 with Friedman χ²=7.69, p=0.990.
2. HBFWS Cycle 7 (PyMC hierarchical Bayesian shrinkage, 4 chains): paired
   Δ = -0.020, Wilcoxon p=0.78. Pre-registered hypothesis rejected.
3. Cycle 7B: six additional paradigms (XGBoost, Random Forest, Logistic L1,
   Algorithm Selection 1-NN, HBFWS-phylo, Rank Aggregation) all fail vs.
   EqualWeight-4core. Smallest p = 0.56.
4. Conclusion in dissertation: "f mapping pathogen features to optimal scoring
   weights is not yet learnable from n=11 with 5/8 singleton families."

## Constraints

- **Adaptive learning at n=11 is provably hard**: 7-paradigm convergence rules
  out further "let me try yet another adaptive method" experiments.
- **30-pathogen pilot is features-only**: Layer A annotation requires manual
  literature curation per pathogen (scaling bottleneck), so YFV/Lassa/WNV CSVs
  carry `ground_truth=-1`.
- **Defense imminent**: each proposed experiment must be ≤1 day of single-CPU
  compute on existing infrastructure (no new sequencing, no new MSA building,
  no new VAE training).
- **Existing assets**: 8,580 Stage 3 evals (20 scoring × 39 detectors × 11
  pathogens) + 12-pathogen feature-ablation per-fold MCCs + Cycle 7B
  comparison CSV + 30-pathogen feature CSVs.

## Biggest remaining defense risk (per codex C5 rehearsal Q1)

> "Prospective time-forward validation is absent. The student themselves
> wrote in `ch5:337` that the H3N2 2010-cutoff pilot is a 0/20 (or 1/50)
> negative result. So this is not pre-existing prospective evidence."

The student has no time for prospective backtesting beyond what's already
in `chapters_en/ch4_results.tex` §`subsec:temporal_validation` (73 windows,
219 top-k evaluations, all already in the manuscript).

## Your task

Propose **3–5 additional experiments**, ranked by ROI for strengthening the
method/defense before submission. For each:

1. **Hypothesis** (1 sentence — what would it claim if it succeeded).
2. **Protocol** (1 paragraph — what data, what analysis, what comparison).
3. **Expected outcome** (qualitative or quantitative — give a guess based on
   the negative-result evidence above).
4. **Defense question pre-empted** (which examiner question it would close,
   if any).
5. **Compute budget** (CPU-hours estimate; must be ≤24 hrs).
6. **Risk if it fails** (would it weaken the dissertation if the result is
   null or contradicts existing claims).

Constraints on your proposals:
- Do NOT propose another adaptive-weighting method (proven dead at n=11).
- Do NOT propose 30-pathogen Layer A curation (manual, multi-week).
- Do NOT propose new ML model training that needs >24 hrs.
- DO consider: alternative validation lenses on existing 8,580 evals;
  alternative significance tests; alternative null distributions; alternative
  effect-size decompositions; alternative feature-importance audits;
  cross-pathogen calibration / coverage / reliability diagnostics; held-out
  protein-family analyses; structural-conservation overlays; inter-detector
  agreement audits; bias diagnostics; etc.

End with a **prioritised order** (P1, P2, P3, ...) and one sentence on which
proposal you would skip if defense were tomorrow.
