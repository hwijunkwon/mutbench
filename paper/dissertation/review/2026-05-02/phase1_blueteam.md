# Phase 1 Blueteam Argument Map

Scope: active-build sources only (`chapters_en/ch1_introduction.tex`, `chapters_en/ch3_methods.tex`, `chapters_en/ch4_results.tex`, `chapters_en/ch5_discussion.tex`, `front_en/abstract.tex`) plus the specified review reports. Orphan chapter files were not used as evidence.

## Claim 1: Literature-curated benchmark and three-layer labels are defensible despite heterogeneity and drift

- Main manuscript statement: `chapters_en/ch1_introduction.tex:145-147` states MutBench as an 11-RNA-virus region-level benchmark and defines Layer A/B/C; `front_en/abstract.tex:2-6` gives the same scope and three-layer summary.
- Strongest supporting evidence: `chapters_en/ch3_methods.tex:200-207` explicitly defines Layer A as a literature-curated heterogeneous union and discloses that no single computational criterion is applied uniformly. `chapters_en/ch5_discussion.tex:193` directly states that heterogeneity could inflate the interaction but reflects the real-world challenge, and warns that MCC values are not directly comparable across pathogens.
- Weakest supporting evidence or fragile assumption: `chapters_en/ch3_methods.tex:29` says the pathogen diversity is “representative,” which is broader than the evidence can prove from 11 RNA viruses. `chapters_en/ch5_discussion.tex:181` also concedes a single-team, single-codebase, single-snapshot estimate requiring independent reproduction.
- Wording assessment: appropriately bounded in the methods and discussion; mildly overstated where the introduction/abstract use broad “broadest” and “representative” language without immediately foregrounding the 11-virus, surface-glycoprotein, point-substitution restriction.

## Claim 2: The 1023-subset Shapley audit bounds the cold-start core

- Main manuscript statement: `chapters_en/ch4_results.tex:796` says the 4-core ranks 87/1023, is a historical fixed configuration rather than a non-arbitrary optimum, and is dominated by the 3-core. `chapters_en/ch5_discussion.tex:272` repeats the same boundary in limitation language.
- Strongest supporting evidence: `review/2026-04-30/wave1/p3_full_lattice.md:40-55` reports the 4-core rank 87/1023, 3-core rank 27/1023, and delta +0.0058 MCC; `review/2026-04-30/wave1/p3_full_lattice.md:57-74` reports Shapley values, including negative pLDDT. `review/2026-04-30/wave1/p2_rank_reliability.md:35-45` independently shows the 3-core ahead of 4-core on rank-reliability metrics.
- Weakest supporting evidence or fragile assumption: `chapters_en/ch4_results.tex:723-725` still frames Algorithm 1 as “a method rather than a heuristic,” which conflicts with the later audit framing. `chapters_en/ch1_introduction.tex:156` and `front_en/abstract.tex:11` still present the 4-feature core as a compact confirmed recipe without mentioning the full-lattice downgrade.
- Wording assessment: bounded in Chapter 4 and Chapter 5 audit paragraphs; overstated in abstract/intro summaries unless read together with later caveats.

## Claim 3: Wave 5 Layer A' produced Branch C, a provenance-sensitivity boundary

- Main manuscript statement: `chapters_en/ch4_results.tex:818-820` reports Layer A' as a structured-database sensitivity benchmark, not a panel extension; `chapters_en/ch5_discussion.tex:272` and `chapters_en/ch5_discussion.tex:301` say Branch C fired and that Layer A' should remain a bounded provenance-equivalence check.
- Strongest supporting evidence: `review/2026-05-02/wave5_replacement/lap_lopo_report.md:5-7` reports mean MCC = -0.055, 2/10 positive folds, precision@20 = 0.005, and Branch C. `review/2026-05-02/wave5_replacement/lap_lopo_report.md:26-36` gives the cross-panel comparison and caveats. `review/2026-05-02/codex_layerA_uniprot_review.md:47-53` explains why UniProt-derived labels are not label-equivalent to literature-curated Layer A.
- Weakest supporting evidence or fragile assumption: `review/2026-05-02/codex_wave5_disposition_review.md:128-132` warned not to call an earlier incomplete manual Wave 5 checkpoint Branch C. The active manuscript appears to have replaced that workflow with a separate Layer A' benchmark, but the report trail is potentially confusing. The Layer A' result is also small (`n=10`) and partly correlated among flavivirus targets (`lap_lopo_report.md:30-32`).
- Wording assessment: appropriately bounded if described as a sensitivity result and boundary condition. It would be overstated if called a validation success or an expanded benchmark.

## Plausible Failure Scenarios and Defenses

1. Label-provenance mismatch: defended by `chapters_en/ch4_results.tex:820`, which separates Layer A' from literature-curated Layer A and says the signal does not transfer; also by `review/2026-05-02/codex_layerA_uniprot_review.md:53`, which warns against mixing label provenance.

2. Panel-size underpowering: defended by `chapters_en/ch4_results.tex:808`, where the pre-registered callability rule yields 0/12 callable folds; reinforced by `chapters_en/ch5_discussion.tex:205`, which explicitly treats the 11-pathogen panel as small-n and lists caveats.

3. Algorithm 1 overclaiming: defended by `chapters_en/ch4_results.tex:796`, `chapters_en/ch4_results.tex:800`, and `chapters_en/ch4_results.tex:804`, which reframe the 4-core as historical, rank-prioritization only, and not globally calibrated.

4. Frequency/label correlation: defended by `chapters_en/ch5_discussion.tex:16-19`, which reports the Layer A membership-vs-frequency audit and warns that some pathogen rankings are partly structural.

5. Prospective-validation absence: defended by `front_en/abstract.tex:2`, which explicitly states retrospective enrichment and no prospective time-forward validation; `chapters_en/ch5_discussion.tex:181` and `chapters_en/ch5_discussion.tex:301` reserve reproduction and expanded-panel deployment for future work.

## Weakest Paragraph by Active Source Group

- Abstract: `front_en/abstract.tex:11`. Weakness: it says the 4-feature core “confirms” compactness while omitting the later 1023-subset downgrade and 3-core dominance. Defense blocker: not fatal, but should be softened in oral defense.

- Ch1: `chapters_en/ch1_introduction.tex:154-156`. Weakness: Contribution 3 still presents the 4-feature core as a practical cold-start recipe without the full-lattice caveat. Defense blocker: moderate, because it is the front-door claim.

- Ch3: `chapters_en/ch3_methods.tex:28-30`. Weakness: “representative range” overgeneralizes from the specific 11-virus surface-protein panel. Defense blocker: low if paired with the scope limitations in Chapter 5.

- Ch4: `chapters_en/ch4_results.tex:723-725`. Weakness: “method rather than heuristic” is too strong relative to the later null-calibration and callability results. Defense blocker: moderate unless the later audit paragraphs are emphasized.

- Ch5: `chapters_en/ch5_discussion.tex:272`. Weakness: it compresses Waves 1-5 into one very long paragraph, combining negative audits, callable subsets, Wave 4, and Layer A' Branch C. The content is useful, but the density makes the defense logic hard to inspect. Defense blocker: low-to-moderate; the claims are bounded, but the paragraph is rhetorically fragile.

## Overall Blueteam Read

The defensible dissertation story is not “MutBench discovers a universal predictor.” It is: MutBench provides a scoped, literature-curated RNA-virus hotspot benchmark; the scoring-by-pathogen interaction is the central benchmark finding; the cold-start 4-core is a historical fixed heuristic bounded by a full-lattice audit; and Layer A' is a negative provenance-sensitivity result showing that structured public-database labels are not interchangeable with literature-curated Layer A. The active manuscript mostly supports that bounded story, with the main remaining risk concentrated in abstract/intro compression and the confusing Wave 5 report history.
