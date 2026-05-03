# Phase 3 CCB Arbitration

Scope: active English build inputs only (`front_en/abstract.tex`, `chapters_en/ch1_introduction.tex`, `chapters_en/ch3_methods.tex`, `chapters_en/ch4_results.tex`, `chapters_en/ch5_discussion.tex`) plus Phase 0/1/2/Statistics and cited supporting reports. Orphan files are not used as evidence.

## Part A — Per-Finding Arbitration

### Redteam Findings

1. **Algorithm 1 over-staked relative to benchmark contribution — (b) Requires manuscript fix.**  
The active text still says the evidence "operationalises into a deployable algorithm" and "cold-start, universal" at `chapters_en/ch4_results.tex:696`, while later audits bound it as historical/non-optimal, rank-heterogeneous, and not callable (`chapters_en/ch5_discussion.tex:272`, `chapters_en/ch5_discussion.tex:301`; supporting lattice/rank evidence at `review/2026-04-30/wave1/p3_full_lattice.md:40-55`, `review/2026-04-30/wave1/p2_rank_reliability.md:35-45`).  
Suggested edit at `chapters_en/ch4_results.tex:696`: replace the opening sentence with: "The empirical evidence above operationalises into an exploratory two-tier search-space-reduction heuristic. Tier 1 is a cold-start default for retrospective screening, not a prospectively callable detector under the current P5 abstention rule."

2. **"Not yet learnable from n=11" over-causal panel-size framing — (b) Requires manuscript fix.**  
The manuscript acknowledges weak LOPO/gap evidence in isolation (`chapters_en/ch4_results.tex:437-441`) and one positive EV-A71 fold (`chapters_en/ch4_results.tex:857`), but still says failures "isolate the constraint to the panel size itself" (`chapters_en/ch4_results.tex:857`) and repeats the same causal framing in future work (`chapters_en/ch5_discussion.tex:299`).  
Suggested edit at `chapters_en/ch4_results.tex:857` and `chapters_en/ch5_discussion.tex:299`: "is most consistent with a panel-size constraint under the tested feature sets, model classes, and nested-LOPO protocols; alternative pathogen descriptors, external labels, or different model classes could still change this conclusion."

3. **Layer A vs Layer A' provenance over-converted into support for Layer A — (b) Requires manuscript fix.**  
The negative result is disclosed (`chapters_en/ch4_results.tex:820`; supporting report `review/2026-05-02/wave5_replacement/lap_lopo_report.md:5`, `:30-36`), and the active text says Layer A' is not a panel extension (`chapters_en/ch4_results.tex:820`, `chapters_en/ch5_discussion.tex:301`). However, "supports keeping" the literature-curated panel can still read as validation of Layer A rather than non-equivalence.  
Suggested edit at `chapters_en/ch4_results.tex:820`: "The result shows Layer A and Layer A' are not interchangeable label provenances; the dissertation therefore retains Layer A as the pre-existing primary benchmark but does not treat the Layer A' failure as validation of Layer A."

4. **Omega-squared headline biologically under-qualified — (b) Requires manuscript fix.**  
Statistical handling is careful: Chapter 4 says "largest modeled component" and gives conservative cell-level estimates (`chapters_en/ch4_results.tex:354`, `:383`), and methods disclose heterogeneous Layer A construction (`chapters_en/ch3_methods.tex:207`, `:306`). But the abstract headline foregrounds `omega^2 = 0.296` without the curation-protocol caveat (`front_en/abstract.tex:2`, `:10`), and the table footnote says "proportion of total variance explained" (`chapters_en/ch4_results.tex:372`).  
Suggested edit at `front_en/abstract.tex:2`: add "under literature-curated Layer A labels, which partly confound pathogen biology with curation protocol." At `chapters_en/ch4_results.tex:372`, replace "proportion of total variance explained" with "bias-corrected modeled effect-size estimate."

5. **Wave 5 Branch C softened as sensitivity check — (a) Already addressed.**  
The active prose gives the negative numbers and interpretation directly: mean LOPO MCC `-0.055`, `2/10` positive folds, precision@20 `0.005`, stable but negative sign, Branch C, and no panel extension (`chapters_en/ch4_results.tex:820`; `chapters_en/ch5_discussion.tex:301`). Concealment is not sustained. A wording polish could add "negative" before "sensitivity benchmark," but the requested bounding language is already present.

6. **Selective reporting uneven across abstract/results/discussion — (b) Requires manuscript fix.**  
The failures are visible in Chapter 4/5: 48.6% negative-MCC cells (`chapters_en/ch4_results.tex:294-296`), null calibration and P5 `0/12` callability (`chapters_en/ch5_discussion.tex:272`, `:301`), and Layer A' non-transfer (`chapters_en/ch4_results.tex:820`). The abstract, however, gives the search-space-reduction story without the abstention/negative-transfer boundary (`front_en/abstract.tex:11`).  
Suggested edit at `front_en/abstract.tex:11`: "Negative and abstention results bound this use: the pre-registered callability rule abstains on 0/12 folds, and the Layer A' sensitivity does not transfer."

7. **Future panel-size threshold needs decision rule — (b) Requires manuscript fix.**  
The manuscript names 20-30+ pathogens (`chapters_en/ch5_discussion.tex:291`, `:299`) and reports the current 7/11 quorum rule and `0/12` outcome (`chapters_en/ch5_discussion.tex:301`), but it does not state what future result would falsify adaptive selection.  
Suggested edit at `chapters_en/ch5_discussion.tex:299`: "A future expanded-panel test should be considered negative if the same training-fold-only callability rule fails to call at least a majority of held-out folds or if adaptive methods do not exceed EqualWeight under paired nested-LOPO."

### Statistics WARN/FAIL Findings

8. **MCC vs precision@20 reporting consistency — (b) Requires manuscript fix.**  
Metric scopes are correctly separated in methods (`chapters_en/ch3_methods.tex:790-807`) and Layer A' is correctly negative in Chapter 4 (`chapters_en/ch4_results.tex:820`). The remaining risk is first-page framing: abstract line 11 emphasizes search-space reduction without carrying Layer A' precision@20 fragility (`front_en/abstract.tex:11`).  
Suggested edit at `front_en/abstract.tex:11`: append "The UniProt-derived Layer A' sensitivity is negative (mean MCC = -0.055; precision@20 = 0.005) and is treated as label-provenance non-equivalence."

9. **Fairness/correlation framing — (a) Already addressed.**  
The manuscript explicitly distinguishes Layer A membership-vs-frequency circularity from feature-feature redundancy: mean per-pathogen point-biserial `|rho| = 0.12`, range `[-0.06,+0.33]`, and the separate frequency/entropy `rho approx 0.97` feature correlation (`chapters_en/ch5_discussion.tex:16-19`; `chapters_en/ch4_results.tex:945`). It also discounts HCV, Influenza B, and Norovirus frequency-best rankings as partly structural (`chapters_en/ch5_discussion.tex:18`). The warning's concern is materially bounded by active text.

### Blueteam Weakest-Paragraph Items

10. **Abstract 4-feature core "confirms" compactness — (b) Requires manuscript fix.**  
The abstract reports the fixed 4-core as confirming compactness (`front_en/abstract.tex:11`) but omits the full-lattice downgrade and 3-core dominance later disclosed (`chapters_en/ch5_discussion.tex:272`; `review/2026-04-30/wave1/p3_full_lattice.md:40-55`).  
Suggested edit at `front_en/abstract.tex:11`: replace "confirms the compact core" with "bounds the historical 4-core as a compact retrospective heuristic; a full-lattice audit ranks it 87/1023 and finds a slightly better 3-core."

11. **Ch1 contribution overstates practical cold-start recipe — (b) Requires manuscript fix.**  
Contribution 3 says the compact 4-feature core provides a practical cold-start recipe (`chapters_en/ch1_introduction.tex:154-156`) without the later audit caveat.  
Suggested edit at `chapters_en/ch1_introduction.tex:156`: add "This is a retrospective, fixed historical recipe rather than a lattice-optimal or prospectively callable detector; Chapter 4/5 report the full-lattice and abstention-rule boundaries."

12. **Ch3 "representative range" overgeneralizes from 11 viruses — (b) Requires manuscript fix.**  
The methods line says the selected pathogens cover a "representative range" (`chapters_en/ch3_methods.tex:29`), while the actual scope is 11 RNA-virus surface glycoproteins, point substitutions only (`front_en/abstract.tex:2`; `chapters_en/ch3_methods.tex:37`).  
Suggested edit at `chapters_en/ch3_methods.tex:29`: replace "representative range of viral evolutionary regimes" with "deliberately diverse but non-exhaustive range of RNA-virus surface-glycoprotein evolutionary regimes."

13. **Ch4 "method rather than heuristic" conflicts with audit framing — (b) Requires manuscript fix.**  
The baseline paragraph says the takeaways defend the algorithm as "a method rather than a heuristic" (`chapters_en/ch4_results.tex:725`), but Wave 1 and P5 later reduce the claim to an exploratory prioritization heuristic (`chapters_en/ch5_discussion.tex:272`, `:301`).  
Suggested edit at `chapters_en/ch4_results.tex:725`: replace "defend the algorithm as a method rather than a heuristic" with "show why the heuristic is nontrivial relative to simpler baselines, while leaving deployability to the abstention-rule audits."

14. **Ch5 Wave 1-5 audit paragraph too dense — (b) Requires manuscript fix.**  
The paragraph at `chapters_en/ch5_discussion.tex:272` contains useful bounding language but combines full lattice, rank reliability, null calibration, callability, P6, Wave 4, and Wave 5 in one long paragraph. The content is bounded, but the density makes the defense logic fragile.  
Suggested edit at `chapters_en/ch5_discussion.tex:272`: split into three paragraphs: Wave 1-3 algorithm-boundary audits; Wave 4 expanded-feature feasibility and callability failure; Wave 5 Layer A' negative provenance-sensitivity result.

## Severity Disputes

- Statistics WARN #10 should be treated as **already addressed / low residual risk**, not a required statistical correction. The active text already separates the `|rho|=0.12` Layer A circularity audit from the `rho approx 0.97` feature-feature redundancy and propagates the caveat to frequency-best pathogens.
- Redteam Major #4 is sustained only as a **framing** issue, not as a formal statistical error. This aligns with the Statistics PASS on omega-squared interpretation (`phase2_statistics.md:3`).

## Part B — Seeded Reconciliation

The Redteam and Statistics findings partially invalidate Blueteam Claim 2 as phrased in the abstract/intro: the evidence map remains correct for Chapter 4/5 caveats, but the first-page claim that the 4-core "confirms" compactness is not supported without the 1023-subset downgrade and 3-core dominance. Redteam's Algorithm 1 and P5 callability findings also narrow Blueteam's "cold-start core" claim to retrospective search-space reduction, not deployable prediction. Redteam/Statistics do not invalidate Blueteam Claim 1 or Claim 3; they reinforce the same provenance and heterogeneity boundaries. The Blueteam map exposes one missing statistics-side check: a concise first-page consistency check tying abstract search-space-reduction language to P5 `0/12` callability and Layer A' precision@20 fragility. Otherwise, Statistics covered the main formal checks, including omega-squared, paired/unpaired tests, multiple comparisons, sign stability, small clusters, and fairness/circularity.

## Part C — Andon Code

Critical findings unresolved: **0**. Redteam self-reported 0 Critical findings (`phase2_redteam.md:5-7`), and this CCB does not elevate any Major to Critical because the adverse evidence is disclosed in active Chapter 4/5 and the remaining issues are prose-framing fixes rather than fabrication, concealment, or active-build invalidity.

Phase 4 entry verdict: **PASS**. Proceed to Phase 4 with Major/Minor prose fixes recorded for revision, but no Critical blocker.

