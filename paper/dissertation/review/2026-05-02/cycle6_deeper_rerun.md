# Cycle 6 Deeper Re-analysis -- Whole Dissertation, 8 Axes

Scope: active English build inputs only: `front_en/abstract.tex`, `chapters_en/ch1_introduction.tex` including `ch2_background.tex`, `ch3_methods.tex`, `ch4_results.tex`, and `ch5_discussion.tex`. `ch5_adapt.tex` is not included by `thesis_en.tex` and is treated as orphan evidence. Required prior evidence consumed: Cycle 6 Jobs 1--4, Phase 4 Cycle 5 score 82.9/100 with H=7.8 residual, and Cycle 4 A--I perspective reports.

## Fix Verification Summary

1. Defense map table: **PASS**. The table at `ch5_discussion.tex:356-372` directly maps claim, evidence tier, boundary, and allowed oral wording. It lifts readability/Q&A, but its citations are slightly odd: C1 points to a wave-audit paragraph rather than the benchmark-design paragraph.
2. Panel-scope box: **PASS**. `ch1_introduction.tex:89` now separates the 11-pathogen main panel, 12-pathogen Stage 3 panel, and Wave panels. It materially reduces denominator confusion.
3. Softened practical-relevance sentence: **PASS**. `ch5_discussion.tex:125` replaces "establishes" with "supports retrospective practical relevance" and integrates the LOPO oral boundary.
4. LOPO spoken-answer sentence: **PASS**. `ch5_discussion.tex:125` now states LOPO is an operational failure mode, not standalone proof; this aligns with `abstract.tex:10` and `ch4_results.tex:290-292`.
5. Layer A provenance summary: **partial PASS**. `ch5_discussion.tex:21-49` adds a useful one-row-per-pathogen provenance table plus recuration limitations. It improves defense clarity, but the tag mix remains too coarse: most rows collapse to `immune_escape`, and the table does not yet provide PMID/coordinate/extraction-level provenance.

## Per-Axis Re-analysis

### Axis 1 -- Content appropriateness
- Original cycle-6 verdict: strong
- Cycle-6-deeper grade: 8.6 / 10
- Sub-components: PhD-scale gap 9.0; contribution hierarchy 8.7; related-work benchmark positioning 8.4; limitations maturity 9.0; originality vs adjacent VEP/DMS benchmarks 8.0.
- New findings (not in original cycle 6): Against current RNA-virus benchmarks, the dissertation is strongest as a region-level benchmark, not a VEP competitor. The EVEREST/ViroGym/ProteinGym distinction is explicit (`ch2_background.tex:248-254`; `ch5_discussion.tex:151-154`), but the title-level contribution still depends on readers accepting region-level hotspot detection as a distinct task rather than a simplified binarization of variant-effect prediction.
- Verification of the 5 J4 fixes that touch this axis: panel-scope PASS; defense map PASS; Layer A provenance partial PASS. These make the content hierarchy more defensible without changing the scientific core.
- Top remaining gap, post-fix: Contribution 3 still rests on one clean external anchor, HIV-1, despite broad practical language in `abstract.tex:11` and `ch5_discussion.tex:269`.
- Smallest additional fix to lift to grade 9.0+: retitle Contribution 3 everywhere as "retrospective HIV-1-anchored search-space reduction" and add a one-row benchmark-comparison table: MutBench vs ViroGym/EVEREST/ProteinGym by task, target unit, labels, and output.

### Axis 2 -- Length appropriateness
- Original cycle-6 verdict: medium
- Cycle-6-deeper grade: 7.4 / 10
- Sub-components: total page count 8.0; chapter balance 7.5; table/figure yield 7.2; local density 6.7; audit placement 6.8.
- New findings (not in original cycle 6): At 243 pages, the manuscript is still within a normal computational-biology PhD range, but the five fixes add front/back matter density rather than replacing text. The defense map helps oral use, but the Layer A provenance table and long future-work/audit blocks compound the "complete but overloaded" H=7.8 issue from Phase 4 Cycle 5.
- Verification of the 5 J4 fixes that touch this axis: defense map partial PASS for length because it is high-yield; Layer A provenance partial PASS because it adds necessary caveat mass; panel-scope PASS because one paragraph prevents many repeated clarifications.
- Top remaining gap, post-fix: late Ch4/Ch5 audit paragraphs still read like a running audit log with scripts, branches, and CSV paths (`ch4_results.tex:796-857`; `ch5_discussion.tex:302-340`).
- Smallest additional fix to lift to grade 9.0+: compress Waves/Cycle 7B into one main-text synthesis table and move script paths plus branch mechanics to appendix/provenance.

### Axis 3 -- Method appropriateness
- Original cycle-6 verdict: medium-to-strong
- Cycle-6-deeper grade: 8.3 / 10
- Sub-components: primary estimand fit 8.4; small-cluster robustness 8.2; null/counterfactual coverage 8.1; LOPO/Friedman use 8.6; method hierarchy clarity 7.6.
- New findings (not in original cycle 6): The method stack now meets dissertation-grade robustness for the retrospective claim: ANOVA/cell-level/ANCOVA/Bayesian/wild/phylogenetic frames plus counterfactual-null reporting. The remaining methodological gap is not another model; it is the absence of a formally independent curation/label-resampling study that treats Layer A as uncertain data rather than fixed truth.
- Verification of the 5 J4 fixes that touch this axis: LOPO spoken-answer PASS; defense map PASS; Layer A provenance partial PASS. They improve interpretation but do not add new method evidence.
- Top remaining gap, post-fix: Layer A label uncertainty is disclosed but not modeled; no duplicate recuration, agreement statistic, source-selection sensitivity, or per-label uncertainty interval exists (`ch5_discussion.tex:49`).
- Smallest additional fix to lift to grade 9.0+: independently recurate 10-20% of Layer A positions and report agreement, coordinate-error rate, and a sensitivity rerun using only high-confidence residue-level labels.

### Axis 4 -- Argument focus
- Original cycle-6 verdict: medium
- Cycle-6-deeper grade: 8.1 / 10
- Sub-components: one-sentence thesis 8.6; contribution ordering 8.5; Stage 1/2/3 role stability 8.0; audit subordination 7.3; terminology burden 7.4.
- New findings (not in original cycle 6): The new panel-scope box solves one major focus problem, but a second focus problem remains: "pathogen-dependent optimal information source" and "4-feature/3-core cold-start recipe" pull in opposite rhetorical directions. The manuscript explains ceiling vs floor (`ch5_discussion.tex:181`), but readers must retain too much local context.
- Verification of the 5 J4 fixes that touch this axis: panel-scope PASS; defense map PASS; softened sentence PASS.
- Top remaining gap, post-fix: the cold-start recipe can still look like a second dissertation about adaptive deployment, especially after seven adaptive-weighting failures (`ch4_results.tex:857`; `ch5_discussion.tex:338-340`).
- Smallest additional fix to lift to grade 9.0+: add one sentence after the contribution hierarchy: "The cold-start analyses are boundary audits of Contribution 3, not a fourth contribution."

### Axis 5 -- Flow
- Original cycle-6 verdict: medium
- Cycle-6-deeper grade: 7.8 / 10
- Sub-components: chapter arc 8.4; method-before-result ordering 7.7; Ch4 readability 7.2; Ch5 synthesis 8.0; future-work separation 7.0.
- New findings (not in original cycle 6): Whole-paper flow is good at macro scale but less good at "reader memory" scale. The manuscript now defines scope early (`ch1_introduction.tex:89`) and closes with a defense map (`ch5_discussion.tex:356-372`), but the path between them requires tracking 11, 12, 16, 19, 28, Layer A, Layer A', 3-core, 4-core, and EqualWeight variants.
- Verification of the 5 J4 fixes that touch this axis: panel-scope PASS; LOPO spoken-answer PASS; defense map PASS. The fixes improve entry and exit flow, not the dense middle.
- Top remaining gap, post-fix: Ch4 still interleaves core results, robustness audits, feature-ablation lattice results, callability failures, Wave 4/5, and adaptive-weighting failures before returning to practical validation.
- Smallest additional fix to lift to grade 9.0+: insert a one-paragraph "Reader route through Chapter 4" before Stage 2: core evidence first, then boundary audits, then practical validation.

### Axis 6 -- Data appropriateness
- Original cycle-6 verdict: medium
- Cycle-6-deeper grade: 7.9 / 10
- Sub-components: 11-pathogen panel fitness 8.0; sequence provenance 8.2; Layer A suitability 7.2; Layer B/C separation 8.4; external validation data 7.2; scope ledger 7.0.
- New findings (not in original cycle 6): The manuscript now benchmarks well against comparable computational-biology dissertations in transparency, but less so against curated immunology resources such as IEDB-grade evidence trails. The Layer A provenance table (`ch5_discussion.tex:21-49`) is a clear improvement, yet it also exposes the dominance of a few sources and the lack of residue-level extraction metadata.
- Verification of the 5 J4 fixes that touch this axis: Layer A provenance partial PASS; panel-scope PASS. The fixes lift defendability, not data completeness.
- Top remaining gap, post-fix: no candidate-exclusion ledger for the RNA-virus target universe; omitted surface proteins and non-HIV retroviral scope remain only partially documented.
- Smallest additional fix to lift to grade 9.0+: add a supplementary target ledger with included, Stage 3-only, features-only, skipped, and not-attempted targets; include sequence count, label feasibility, escape/DMS availability, and exclusion reason.

### Axis 7 -- Claim-evidence calibration
- Original cycle-6 verdict: strong
- Cycle-6-deeper grade: 8.4 / 10
- Sub-components: headline scope 8.6; retrospective/prospective separation 8.4; negative-result visibility 8.8; verb calibration 7.8; uncertainty language 8.3.
- New findings (not in original cycle 6): Calibration is unusually mature, but a few strong verbs remain. `ch4_results.tex:290` says the LOPO gap "demonstrates" correct choice matters; `ch4_results.tex:301` says the heatmap "confirms" no single scoring type dominates; `ch5_discussion.tex:269` says the 4-feature core "confirms" a practical recipe. These are mostly defensible, but "supports/quantifies/is consistent with" would be safer.
- Verification of the 5 J4 fixes that touch this axis: softened practical-relevance PASS; LOPO spoken-answer PASS; defense map PASS. These directly lift the axis.
- Top remaining gap, post-fix: "validated on independently-curated vaccine-escape positions" remains broader than the actual evidence, where HIV-1 is the clean independent anchor and 3/11 availability is a convenience sample (`ch4_results.tex:949-952`).
- Smallest additional fix to lift to grade 9.0+: replace remaining "validated/confirm/demonstrates" verbs for retrospective, winner-selected, or null-consistent claims with "supports/quantifies/is consistent with."

### Axis 8 -- Defense readability + Q&A robustness
- Original cycle-6 verdict: medium
- Cycle-6-deeper grade: 8.2 / 10
- Sub-components: one-minute thesis 8.5; likely objections answered 8.4; terminology control 7.8; oral claim map 8.8; Q&A residual risk 7.5.
- New findings (not in original cycle 6): The five fixes materially lift the prior H=7.8 clarity residual. A committee member can now find allowed oral wording in one table. The remaining Q&A risk is no longer "what do you claim?" but "why should I trust the labels and prospective usefulness beyond HIV-1?"
- Verification of the 5 J4 fixes that touch this axis: all five touch this axis. Defense map PASS; panel-scope PASS; softened sentence PASS; LOPO spoken-answer PASS; Layer A provenance partial PASS.
- Top remaining gap, post-fix: The strongest hostile question remains: "If prospective signal is weak for 8/11 pathogens (`ch5_discussion.tex:247`) and callability is 0/12, what exactly can a field user do tomorrow?"
- Smallest additional fix to lift to grade 9.0+: add a "recommended user report card" checklist: panel match, label provenance, abstention status, retrospective/prospective status, and whether output is a ranked prioritization list or a deployable detector.

## Cross-Axis Synthesis

### Top 5 cross-cutting findings
1. The dissertation is defensible as a retrospective, region-level benchmark, not as a deployable predictor. This affects content, method, data, calibration, and defense. The manuscript states this, but repeated "practical recipe" language keeps inviting deployment questions.
2. The five fixes lift clarity more than validity. They reduce denominator confusion, oral overclaiming, and Layer A opacity, but they do not add external labels, recuration agreement, or prospective validation.
3. Layer A is the central residual scientific risk. It is transparent and bounded, but heterogeneous curation affects data appropriateness, method interpretation, claim calibration, and Q&A.
4. Late audit density is now the main readability tax. The audit programme is scientifically valuable, but Ch4/Ch5 still read partly as provenance logs, affecting length, flow, and defense fluency.
5. The benchmark-positioning claim is strong if task boundaries stay explicit. MutBench complements EVEREST/ViroGym/ProteinGym; it should not imply superiority on per-variant fitness prediction or PLM family benchmarking.

### The 5 sentences that most need rewording
1. `front_en/abstract.tex:11`: "Contribution 3, practical search-space reduction validated on HIV-1 vaccine-escape..."
   Replacement: "Contribution 3 is retrospective search-space reduction, with HIV-1 vaccine escape as the primary external anchor..."
   Rationale: avoids making one anchor sound like broad validation.
2. `ch1_introduction.tex:156`: "Practical search-space reduction validated on independently-curated vaccine-escape positions."
   Replacement: "Retrospective search-space reduction anchored by independently curated HIV-1 vaccine-escape positions."
   Rationale: aligns title with evidence tier.
3. `ch4_results.tex:290`: "...which demonstrates that the correct choice of combination matters materially..."
   Replacement: "...which quantifies the material cost of using a generalized rather than pathogen-specific combination..."
   Rationale: LOPO gap is descriptive/null-consistent, not a standalone proof.
4. `ch4_results.tex:301`: "The heterogeneous pattern confirms that no single scoring type dominates across all pathogens."
   Replacement: "The heterogeneous pattern is consistent with the absence of a single dominant scoring type across this panel."
   Rationale: heatmap visual evidence should not overstate confirmation.
5. `ch5_discussion.tex:269`: "...confirms the compact 4-feature core... provides a practical cold-start recipe..."
   Replacement: "...supports treating the compact 4-feature core as a retrospective cold-start heuristic..."
   Rationale: the 4-core is historically fixed, not lattice-optimal or prospectively callable.

### Single biggest defendability gap not closed
Matched external/prospective validation remains the biggest gap. The five fixes make the boundaries much easier to say, but they do not change the fact that practical value is cleanly anchored by HIV-1, prospective signal is weak for most pathogens, and the abstention rule refuses deployment on 0/12 folds. This is acceptable for an 83/100 defensible dissertation, but it is the main barrier to a 90+ exemplary thesis.

### Stretch goals
1. Independent Layer A recuration/audit. Effort: medium-high; lift: very high. Recurate 10-20% of positions with a second curator, report agreement, coordinate mismaps, source-disagreement examples, and rerun headline omega on high-confidence residue-level labels. This directly improves data, method, calibration, and defense.
2. Compact audit restructuring. Effort: low-medium; lift: high. Convert Wave/Cycle 7B prose into a table plus one synthesis paragraph, moving script paths to provenance. This would raise length, flow, and readability without new experiments.
3. One additional clean external anchor or time-forward test. Effort: high; lift: very high. A second Layer-A-disjoint escape/DMS-derived validation set, or a frozen pre/post time-forward Layer A rerun, would move Contribution 3 from HIV-1-anchored retrospective support toward exemplary practical validation.

RESULT_C6D: avg_grade=8.1/10 top_gap=matched_external_prospective_validation stretch_lift_potential=1.2
