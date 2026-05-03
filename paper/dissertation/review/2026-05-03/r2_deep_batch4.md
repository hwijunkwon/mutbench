# Risk-2 Deep Batch 4 -- Cold-Start + Cycle 7B + Subset/Lattice

Scope: Ch4 lines 706--893 only. This is a read-only line-level compression plan; no source edits made.

## Block #14: Cold-Start algorithm + audit ledger prose

**Original span:** lines 706--893 = 188 lines.  
**Guarded target:** 105--112 lines (<=60%).  
**Recommended replacement:** 111 lines.  
**Exact savings:** 188 - 111 = **77 lines**.

### Existing ledger/table preservation

Existing `tab:audit_ledger` already preserves: P1 null calibration, P2 rank reliability, P3 full lattice + Shapley, P5 `0/12` callable, P6 structural nulls, Wave 4, Wave 5, HBFWS `p=0.78`, and Cycle 7B `p=0.56`.

Existing non-ledger tables preserve: `tab:cold_start_baseline_progression` for Algorithm 1, 4-core `0.0809`, full-10 `0.0698`, and oracle `0.0950`; `tab:subset_selection_top10` for 4-of-210 rank `13/210`; `tab:nested_lopo_4core` for nested-LOPO CIs/deltas.

Add one audit-ledger row so the opening Cold-Start prose can shrink without losing the operational anchor:

```tex
\textbf{Cold-Start baseline} & fixed 4-core vs simpler/full/oracle ensembles & Algorithm~\ref{alg:mutbench_coldstart}: MCC $0.081$ vs full-10 $0.070$; 13/210 4-of-10 rank; oracle gap $+0.014$ & retrospective wet-lab triage heuristic, not deployable detector & \ref{para:cold_start_baseline_progression} \\
```

Modify existing P1/P2 ledger cells rather than adding rows: P1 should include at-or-below-null counts `6/12`, `4/12`, `7/12`; P2 should include the decision-curve random baseline `41`. Keep P3 row as-is but ensure it still says `1023`, `87/1023`, `27/1023`, pLDDT `-0.0015`, ESM-2 `-0.0144`.

### Narrative content that must remain

Keep these boundary statements: Tier 1 is exploratory retrospective prioritization, not prospectively callable deployment; Tier 2 is provisional and family-prior only; the `omega^2 = 0.296` interaction with cluster CI `[0.202, 0.346]` supports pathogen-dependent information utility, not a prescriptive selector; current failures are at `n=11` under tested labels/features/validation.

Do not let LOPO `0/11` appear alone; when mentioned, pair it with `omega^2=0.296`, Friedman `p=0.990`, HBFWS `p=0.78`, and Cycle 7B failures.

### Concrete replacement draft

Target layout: keep Algorithm 1 at lines 710--733 unchanged (24 lines), keep `tab:audit_ledger` but add the one Cold-Start row and tighten typography if needed (about 25 lines), keep `tab:cold_start_baseline_progression` (about 30 lines), then replace the surrounding prose with these 32 TeX lines:

```tex
\paragraph{MutBench Cold-Start algorithm: retrospective triage, not deployment.}
\label{para:mutbench_algorithm}
The evidence above operationalises into a two-tier search-space-reduction heuristic for wet-lab triage. Tier~1 is the label-free default: compute homoplasy, pLDDT, entropy, and frequency; orient each feature by the training-fold sign or predefined domain orientation; average within-pathogen $z$-scores; and threshold the top 10\% of positions (Algorithm~\ref{alg:mutbench_coldstart}). It is not a prospectively callable detector under the P5 abstention rule.
The empirical anchor is compact: the fixed 4-core has nested-LOPO mean MCC $0.081$ versus full-10 $0.070$ (Table~\ref{tab:nested_lopo_4core}; baseline progression in Table~\ref{tab:cold_start_baseline_progression}) and ranks 13/210 among 4-of-10 subsets (Table~\ref{tab:subset_selection_top10}). On the triage task it reduces roughly 1,000 positions to 20--80 candidates, enough for screening-budget allocation rather than calibrated probability.
Tier~2 optionally swaps the 4-core for the family-prior single-best category in Table~\ref{tab:scoring_recommendation}. This is justified only as a provisional prior from the scoring~$\times$~pathogen interaction ($\omega^2=0.296$; family-cluster bootstrap [0.202, 0.346]), not as a held-out-family rule. If the family is absent, or if deployment callability is required, default back to Tier~1 and the audit ledger boundaries in Table~\ref{tab:audit_ledger}.

\paragraph{Cold-Start baseline progression.}
\label{para:cold_start_baseline_progression}
Table~\ref{tab:cold_start_baseline_progression} asks whether Algorithm~\ref{alg:mutbench_coldstart} is redundant with simpler baselines. It is not: the single-feature mean is $0.0147$, cumulative top-$K$ peaks at $K=5$ with MCC $0.0724$, and the fixed 4-core reaches $0.0809$ without held-out labels. The oracle best 4-of-210 subset reaches $0.0950$, only $+0.0141$ above the 4-core and within the 4-core paired-bootstrap uncertainty (Table~\ref{tab:nested_lopo_4core}).

\paragraph{Audit ledger reading guide.}
Table~\ref{tab:audit_ledger} should be read as the boundary contract for Algorithm~\ref{alg:mutbench_coldstart}: P1/P6 show partial pathogen-specific signal but no global null-calibrated detector; P2 supports ranked budget allocation with 66--68 expected true positives versus 41 random at 50 sites/pathogen; P3 shows the 4-core is historical rather than optimal; P5 refuses deployment with 0/12 callable folds; Wave 4/5 show label/provenance limits; HBFWS and Cycle 7B show adaptive weighting does not beat the fixed baseline at $n=11$.
```

### Reference verification

Preserved explicitly: Algorithm~`\ref{alg:mutbench_coldstart}`, `tab:audit_ledger`, `tab:cold_start_baseline_progression`, `tab:nested_lopo_4core`, `tab:subset_selection_top10`. Critical numbers preserved: `omega^2=0.296` cluster CI `[0.202,0.346]`, 4-core `0.081` vs full-10 `0.070`, P2 random baseline `41`, P1 at-or-below counts via ledger modification, P5 `0/12`, HBFWS `p=0.78`, Cycle 7B `p>=0.56`.

## Block #18: Cycle 7B six paradigms

**Original span:** lines 863--890 = 28 lines.  
**Guarded target:** <=8 lines.  
**Recommended replacement:** 8 lines.  
**Exact savings:** 28 - 8 = **20 lines**.

### Existing ledger/table preservation

Existing audit row: `Cycle 7B six paradigms` preserves the six methods and smallest `p=0.56`. Existing `tab:adaptive_weighting_comparison` preserves all method means, deltas, and Wilcoxon p-values, but the table can move to appendix if the ledger row keeps `p>=0.56` and the main text names the six paradigms.

### Narrative content that must remain

Keep the interpretation: six additional adaptive methods plus HBFWS fail at `n=11`; this supports a finite-panel/label-regime boundary, not a proof of universal non-learnability. Keep LOPO/Friedman/gap only as paired corroboration, never standalone.

### Concrete replacement draft

```tex
\paragraph{Cycle 7B: six additional adaptive-weighting failures.}
\label{para:cycle7b_comparison}
Cycle 7B tested XGBoost, Random Forest, Logistic L1, 1-NN algorithm selection, phylogenetic HBFWS, and rank aggregation against EqualWeight-4core under the same nested-LOPO folds as Table~\ref{tab:nested_lopo_4core}. None beat the baseline by one-sided Wilcoxon test (smallest $p=0.56$; method-level values archived in Table~\ref{tab:adaptive_weighting_comparison} or appendix).
Together with HBFWS ($p=0.78$), LOPO 0/11, Friedman $p=0.990$, and the oracle-vs-generalised gap, this is a bounded negative result: adaptive selection is not supported at $n=11$ under the tested feature, label, and validation regime (Table~\ref{tab:audit_ledger}).
```

Line count note: 4 nonblank TeX lines plus paragraph spacing; budgeted as 8 source lines if wrapped for readability.

### Reference verification

Preserved explicitly: `tab:nested_lopo_4core`, `tab:adaptive_weighting_comparison`, `tab:audit_ledger`. Critical numbers preserved: HBFWS `p=0.78`, Cycle 7B six paradigms `p>=0.56`, LOPO `0/11` guarded with Friedman and oracle gap.

## Block #19: subset/lattice/Shapley

**Original span:** lines 795--833 = 39 lines.  
**Guarded target:** <=19 lines.  
**Recommended replacement:** 17 lines.  
**Exact savings:** 39 - 17 = **22 lines**.

### Existing ledger/table preservation

Existing audit row: `P3 full lattice + Shapley` already preserves `1023` subsets, 4-core rank `87/1023`, 3-core rank `27`, pLDDT `-0.0015`, ESM-2 `-0.0144`, and the boundary "4-core historical, not optimal." `tab:subset_selection_top10` preserves the 210-subset top-10 and core rank `13/210`.

### Narrative content that must remain

Keep the distinction between two audits: the 210-combination 4-of-10 sweep says the a priori 4-core is competitive; the 1023-subset lattice says it is not optimal and pLDDT is optional. Preserve the interpretation that 3-core is the stronger compact descriptive variant, while Algorithm 1 remains the historical fixed triage recipe.

### Concrete replacement draft

```tex
\paragraph{Subset and lattice audits: competitive, not optimal.}
\label{para:subset_selection_robustness}
The a priori 4-core was not chosen by LOPO tuning. In the exhaustive 4-of-10 sweep, it reaches MCC $0.0809$ and ranks 13/210, above the full-10 ensemble ($0.0698$) but below the best 4-feature subset, \texttt{freq, entropy, homoplasy, semantic\_change}, at $0.0950$ (Table~\ref{tab:subset_selection_top10}). The $+0.0141$ oracle gap is small relative to paired-bootstrap uncertainty, so the 4-core is defensible as a fixed cold-start recipe rather than a discovered optimum.

\paragraph{Full-lattice subset audit and per-feature Shapley.}
\label{para:full_lattice_shapley}
The full lattice confirms the boundary. Across all $2^{10}-1=1023$ non-empty subsets, the 4-core ranks 87/1023, while the 3-core \texttt{freq, entropy, homoplasy} ranks 27/1023 and slightly dominates the 4-core (MCC $0.0866$ vs.\ $0.0809$). Shapley values keep homoplasy, frequency, and entropy positive, but pLDDT is slightly negative ($-0.0015$) and ESM-2 more negative ($-0.0144$). Thus Algorithm~\ref{alg:mutbench_coldstart} remains a historical wet-lab triage heuristic; the compact descriptive optimum is closer to the 3-core (Table~\ref{tab:audit_ledger}).
```

### Reference verification

Preserved explicitly: Algorithm~`\ref{alg:mutbench_coldstart}`, `tab:subset_selection_top10`, `tab:audit_ledger`. Preserved through block #14 baseline draft: `tab:nested_lopo_4core`, `tab:cold_start_baseline_progression`. Critical numbers preserved: 4-core `0.081` vs full-10 `0.070`, `1023`, rank `87`, 3-core rank `27`, pLDDT `-0.0015`, ESM-2 `-0.0144`.

## Summary

| Block | Original lines | Replacement lines | Savings |
|---:|---:|---:|---:|
| #14 | 188 | 111 | 77 |
| #18 | 28 | 8 | 20 |
| #19 | 39 | 17 | 22 |
| **Total** | **255** | **136** | **119** |

Ledger work: add 1 new Cold-Start baseline row; modify existing P1/P2/P3/Cycle 7B cells as noted, with no new rows required for those.

RESULT_R2_DEEP_BATCH4: blocks=3 line_savings=119 ledger_rows_added=1
