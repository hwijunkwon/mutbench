# Phase 2 Redteam Adversarial Review

Scope: active build files only (`front_en/abstract.tex`, `chapters_en/ch1_introduction.tex`, `ch3_methods.tex`, `ch4_results.tex`, `ch5_discussion.tex`) plus the named Wave 1-5 review reports. Orphan files were not used as evidence.

## Critical Findings

No Critical finding is sustained. The active manuscript exposes most negative, null, and abstention results somewhere in Chapter 4 or Chapter 5. The residual problems are over-strong framing and uneven placement, not apparent fabrication or concealment.

## Major Findings

### 1. Algorithm 1 is still over-staked relative to the benchmark contribution

- **Severity:** Major.
- **Evidence path:** `chapters_en/ch4_results.tex:696` calls the recipe a "deployable algorithm" and "cold-start, universal" and ties it to `7--9x` search-space reduction. The same results chapter later reports that the 4-core is a historical fixed configuration, not an optimum (`chapters_en/ch4_results.tex:796`), that rank reliability is positive in only 5/12 pathogens and inverts on Rabies (`chapters_en/ch4_results.tex:800`), and that the pre-registered rule yields `0/12` callable folds (`chapters_en/ch4_results.tex:808`). The discussion repeats the deployment boundary at `chapters_en/ch5_discussion.tex:272` and `ch5_discussion.tex:301`.
- **Failure mode:** A hostile examiner could say: the dissertation's real contribution is a benchmark plus post-hoc bounded heuristics, but the "Algorithm" framing makes the cold-start recipe sound operationally validated for novel pathogens. The abstention result says it is not deployable under its own pre-registered rule.
- **Minimal prose fix:** At `chapters_en/ch4_results.tex:696`, replace "operationalises into a deployable algorithm" and "cold-start, universal" with: "operationalises into an exploratory search-space-reduction heuristic" and "cold-start default for retrospective screening; not prospectively callable under the P5 rule on the current panel."

### 2. The "not yet learnable from n=11" claim is close to insulated from contradiction

- **Severity:** Major.
- **Evidence path:** `chapters_en/ch4_results.tex:824` says the mapping is "not yet learnable from the current panel"; `chapters_en/ch4_results.tex:857` says seven failures "isolate the constraint to the panel size itself." `chapters_en/ch5_discussion.tex:299` repeats that convergence across methods isolates panel size rather than algorithm choice. But a positive single fold is also reported at `chapters_en/ch4_results.tex:857`, and LOPO/gap evidence is explicitly weak in isolation at `chapters_en/ch4_results.tex:437-441`.
- **Failure mode:** A hostile examiner could say: "panel size" has become a non-falsifiable refuge. Any failed learner is attributed to n=11, while any success is treated as "possible in principle." The claim would be stronger if phrased as "not learned by the tested model class under the tested protocols."
- **Minimal prose fix:** At `chapters_en/ch4_results.tex:857` and `chapters_en/ch5_discussion.tex:299`, replace "isolates the constraint to the panel size itself" with: "is most consistent with a panel-size constraint under the tested feature sets, model classes, and nested-LOPO protocols; alternative pathogen descriptors or external labels could still change this conclusion."

### 3. Layer A vs Layer A' provenance is informative, but the manuscript over-converts a negative transfer result into support for the original benchmark

- **Severity:** Major.
- **Evidence path:** Wave 5 reports mean MCC `-0.055`, 2/10 positive folds, and Branch C at `review/2026-05-02/wave5_replacement/lap_lopo_report.md:5`; caveats say the comparison is cross-provenance and not a clean replacement experiment at `lap_lopo_report.md:30-36`. The active manuscript says Branch C supports keeping the 12-pathogen literature-curated panel as primary at `chapters_en/ch4_results.tex:820` and `chapters_en/ch5_discussion.tex:272`. The UniProt inventory review warned that Layer A' is not label-equivalent to Layer A at `review/2026-05-02/codex_layerA_uniprot_review.md:5` and `:53`.
- **Failure mode:** A hostile examiner could say: failed transfer to Layer A' is being used asymmetrically. If Layer A' had worked, it would likely be treated as validation; because it fails, it is labelled a provenance sensitivity and used to protect the original labels. That is defensible only if the text says the result shows non-equivalence, not superiority of Layer A.
- **Minimal prose fix:** At `chapters_en/ch4_results.tex:820`, replace "supporting the 12-pathogen literature-curated panel as the dissertation's primary benchmark" with: "showing that Layer A and Layer A' are not interchangeable label provenances; the dissertation therefore retains Layer A as the pre-existing primary benchmark but does not treat the Layer A' failure as validation of Layer A."

### 4. The omega-squared headline is statistically careful but biologically under-qualified at the headline level

- **Severity:** Major.
- **Evidence path:** The abstract foregrounds `omega^2 = 0.296` as the largest modeled variance component at `front_en/abstract.tex:2` and `:10`. Chapter 4 correctly calls it the largest modeled component and notes residual variance at `chapters_en/ch4_results.tex:383`, but Table wording describes omega-squared as a proportion of total variance at `chapters_en/ch4_results.tex:372`. The manuscript later admits Layer A confounds biological pathogen-dependence with curation-protocol-dependence at `chapters_en/ch4_results.tex:499`; Layer A heterogeneity is also explicit in methods at `chapters_en/ch3_methods.tex:207` and `:306`.
- **Failure mode:** A hostile examiner could say: because literature-curated labels and frequency-like signals can be strongly correlated, `omega^2 = 0.296` may partly measure label-provenance and curation-density differences, not pathogen biology. The caveat exists but is not attached to the headline strongly enough.
- **Minimal prose fix:** At `front_en/abstract.tex:2` and `chapters_en/ch4_results.tex:383`, add a short qualifier: "under the literature-curated Layer A labels, which partly confound pathogen biology with curation protocol." At `chapters_en/ch4_results.tex:372`, replace "proportion of total variance explained" with "bias-corrected modeled effect-size estimate."

## Minor Findings

### 5. Wave 5 Branch C could be read as a negative result softened under "sensitivity check," but concealment is not sustained

- **Severity:** Minor.
- **Evidence path:** The negative Wave 5 result is explicit in the active manuscript: `mean LOPO MCC = -0.055`, `2/10` positive folds, negative sign, Branch C at `chapters_en/ch4_results.tex:820` and `chapters_en/ch5_discussion.tex:301`. The supporting report states the same at `review/2026-05-02/wave5_replacement/lap_lopo_report.md:5`. However, the abstract does not mention Wave 5 or the negative Layer A' sensitivity (`front_en/abstract.tex:2-13`).
- **Failure mode:** A hostile examiner could say the manuscript uses "sensitivity benchmark" to avoid saying "failed transfer to structured-database labels." This is partly mitigated by the explicit negative numbers in Chapter 4/5.
- **Minimal prose fix:** At `chapters_en/ch4_results.tex:820`, change "sensitivity benchmark" to "negative label-provenance sensitivity benchmark." If space permits, add one abstract clause after `front_en/abstract.tex:11`: "A UniProt-derived Layer A' sensitivity was negative and is treated as label-provenance non-equivalence, not panel extension."

### 6. Selective reporting around null, failure, and abstention outcomes is mostly visible, but not evenly weighted across abstract/results/discussion

- **Severity:** Minor.
- **Evidence path:** The abstract reports LOPO null-consistency (`front_en/abstract.tex:10`) and SARS-CoV-2 exploratory status (`front_en/abstract.tex:11`), but not the 48.6% negative-MCC grid fraction (`chapters_en/ch4_results.tex:294-296`), global null-calibration failure (`chapters_en/ch4_results.tex:804`), 0/12 callability (`chapters_en/ch4_results.tex:808`), or Layer A' negative transfer (`chapters_en/ch4_results.tex:820`). The discussion does disclose these at `chapters_en/ch5_discussion.tex:272` and `:301`.
- **Failure mode:** A hostile examiner could say the abstract gives the committee the successful story, while the failure inventory lives deep in later chapters.
- **Minimal prose fix:** In `front_en/abstract.tex:11`, add one sentence: "Negative and abstention results bound this use: the pre-registered callability rule abstains on 0/12 folds, and the Layer A' sensitivity does not transfer."

### 7. Panel-size limit framing is partly falsifiable, but the future threshold needs a concrete decision rule

- **Severity:** Minor.
- **Evidence path:** Future work names 20-30+ pathogens at `chapters_en/ch5_discussion.tex:291` and `:299`; P5 gives a concrete 7/11 quorum rule at `chapters_en/ch4_results.tex:808` and `chapters_en/ch5_discussion.tex:301`.
- **Failure mode:** A hostile examiner could ask: what result at 20-30 pathogens would make the author abandon adaptive selection rather than ask for still more pathogens?
- **Minimal prose fix:** At `chapters_en/ch5_discussion.tex:299`, add: "A future expanded-panel test should be considered negative if the same training-fold-only callability rule fails to call at least a majority of held-out folds or if adaptive methods do not exceed EqualWeight under paired nested-LOPO."

## Attack Target Disposition Summary

- **Wave 5 Branch C interpretation:** Minor sustained. It is disclosed, but the phrase "sensitivity" should be paired with "negative."
- **Panel-size limit framing:** Major sustained. The claim is plausible but over-causal.
- **Layer A vs Layer A' provenance:** Major sustained. Non-equivalence is informative; it should not be written as validation of Layer A.
- **Algorithm 1 vs benchmark separation:** Major sustained. "Deployable" and "universal" conflict with 0/12 callability and rank-reliability limits.
- **`omega^2 = 0.296` interpretation:** Major sustained. Statistically careful in Chapter 4, but the headline needs the Layer A curation/frequency-correlation caveat attached.

## Overall Judgment

The dissertation is not hiding the adverse evidence; it has unusually extensive null and failure disclosure. The main adversarial vulnerability is that summary claims still read more operational and causal than the evidence permits. The fastest defense-safe revision is to move one compact failure sentence into the abstract, demote Algorithm 1 from deployable algorithm to exploratory prioritization heuristic, and state that Layer A' failure establishes label-provenance non-equivalence rather than positive support for Layer A.
