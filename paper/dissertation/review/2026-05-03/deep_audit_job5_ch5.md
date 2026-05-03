# Deep Audit Job 5: Ch5 Discussion

Scope: `paper/dissertation/chapters_en/ch5_discussion.tex` lines 1-340. Read-only audit against Ch1/Ch3/Ch4 and archived CSVs.

### Chunk 1 (lines 1-100)

#### Numerical Claims
- Lines 5, 51: 4-core nested-LOPO delta `+0.011`, `p=0.61`, min-max vs z-scoring distinction: VERIFIED against Ch3 lines 627-632, 795 and Ch4 lines 669-693; `feature_ablation_nested_lopo_summary.csv` gives full-10 `0.06975`, fixed-4 `0.08088`, paired delta `0.01113`, CI `[-0.01775, 0.04239]`.
- Lines 10, 58-60: Stage-1/SARS-CoV-2 H-score saturation, synthetic-real gap, DMS/convergent Jaccard, founder-bias homoplasy examples: internally plausible and cross-referenced to Ch4/Ch5 anchors, but not fully re-derived in this audit because their source CSVs were outside the specific requested checks.
- Lines 17-19: circularity audit (`mean |rho|=0.12`, range `[-0.06,+0.33]`, D614G homoplasy 2 vs position 476 homoplasy 53, Layer C available for 6/11): internally consistent with the stated caveat framing; source file for the point-biserial audit was not identified in the requested artifact list, so mark UNVERIFIED rather than discrepant.
- Lines 21-43, Layer A provenance table: DISCREPANCY. `results/mutbench/layer_a_tags.csv` has 308 data rows across 12 pathogens, and the tag counts match the table, but the “dominant source” logic only matches if sources are collapsed to first-author/year before the semicolon. The caption says “most-cited paper string in `layer_a_tags.csv`”; by literal full string, Rabies is `Lafon 1983; antigenic site II` (10 rows), not `Aditham 2025`; Zika is `Sourisseau 2019; DIII ABCD sheet epitope` (4 rows), not `Long 2019`; SARS-CoV-2 has several top full strings at 3/1 rows, not `Cao 2023`. If collapsed to first-author/year, the table is mostly correct: Rabies is tied `Lafon 1983`/`Aditham 2025` at 12 each, so selecting only Aditham is under-specified.
- Line 43: “Total 308” and immune-escape `~90%`: VERIFIED. CSV tag total is 278/308 immune_escape = 90.3%.
- Line 49: “309 positions across 12 pathogens”: DISCREPANCY. `wc -l` is 309 including header; CSV data rows/positions are 308, consistent with the table total.
- Line 49: no IAA / no source-selection sensitivity / region-derived caveat: VERIFIED as a limitation framing. Ch3 Layer A construction describes heterogeneous literature-curated sources (Ch3 lines 214-219) and does not report IAA, sensitivity swapping, or per-position assay-grade audit trail. The “1-3 anchor publications per pathogen” phrase is too narrow if read against the CSV’s per-row evidence strings, but broadly matches the Ch3 table’s compact source listing.

#### Citations
- `nextstrain2018hadfield`: supports real-time pathogen-evolution surveillance context; OK.
- `rice1976algorithm`, `wolpert1997nfl`: support algorithm-selection/no-free-lunch framing; OK.
- `gurev2025everest`, `notin2023proteingym`: support comparison to variant-effect/fitness benchmarks; OK, though EVEREST is a 2025 bioRxiv per the bib, so “related work” should remain cautious.
- `weirauch2013evaluation`: supports the claim that low/moderate predictive metrics can be meaningful in difficult biological sequence tasks; OK as analogy, not direct viral-hotspot evidence.

#### Cross-Refs
- All explicit Ch5 `\ref{...}` labels resolve when Ch1-Ch5 are included.
- Semantic issue: several labels are phantoms placed inside Ch5’s limitations matrix, not real sections/paragraphs (`sec:gt_heterogeneity`, `sec:durc_ethics`, `para:sublineage_pooling`, `para:hbv_pilot`, etc.). References technically compile, but “Section~\ref{sec:gt_heterogeneity}” and “Paragraph~\ref{para:hbv_pilot}” do not land on an actual heading/paragraph with substantive text.

#### Logical Consistency
- Layer A heterogeneity caveat is consistent with Ch3’s construction: Ch3 explicitly states Layer A is a heterogeneous union of convergent evolution, immune escape, and HVR membership.

#### Outdated Content
- No “9 pathogens” or “PAHD” residue in this chunk. The 11-vs-12 distinction is mostly explicit, but line 49’s 309/308 mismatch is a stale count.

#### Severity
- Critical: 0
- Major: 2 (Layer A provenance caption/dominant-source mismatch; phantom cross-reference anchors presented as real sections/paragraphs)
- Minor: 1 (309 vs 308 data-row count)

### Chunk 2 (lines 101-220)

#### Numerical Claims
- Lines 101-110, region-overlap table: DISCREPANCY. Caption says the upper 9 rows reproduce directly from `region_overlap_mcc.csv`, but the CSV gives different values. Examples: SARS-CoV-2 CSV exact/window5/window10 = `0.2271/0.7118/0.8611`, table = `0.211/0.480/0.497`; H3N2 CSV = `0.5209/0.8513/0.9638`, table = `0.534/0.639/0.548`; Norovirus CSV = `0.3554/0.9254/0.9254`, table = `0.510/0.335/0.275`. The table exact column largely matches per-pathogen best MCC from `stage3_full_results.csv`, not the cited CSV. This is a provenance failure for a table used in Ch4/Ch5 argumentation.
- Line 120: mean oracle recall `0.552`, EV-A71 recall `0.185`, Rabies `0.308`: VERIFIED against `stage3_full_results.csv` best-per-pathogen rows and Ch4 precision table. The `precision_at_k_analysis.csv` does not include EV-A71/Rabies, so the stated source `Table~\ref{tab:precision_at_k}` depends on manuscript values, not that CSV alone.
- Lines 125, 181, 197, 218: `omega^2=0.296`, cell-level `0.234`, LOPO `0/11`, `0.265` gap, `n=11` panel constraint: VERIFIED against Ch1 lines 167-170 and Ch4 lines 393-451.
- Lines 131-148: vaccine escape values `9.36x`, `7.19x`, `7.63x`, Bonferroni framing, HIV-1 82% disjoint, H3N2 69% overlap: VERIFIED against Ch4 Table `tab:vaccine_escape_stage3` text (Ch4 lines 958-979), but not mechanically reproduced by simply taking minima/maxima from `vaccine_escape_stage3.csv`; the CSV contains additional rows with stronger raw p-values/enrichments. The manuscript table is therefore a curated evidence-tier table, and the source/provenance should make that selection rule explicit.
- Line 132: H3N2 EqualWeight top-5 `4.012x`, `p=0.0023`: VERIFIED against `results/mutbench/escape_validation_adapt.csv`.
- Line 134: 4-core retains 97.6% and ranks 13/210: VERIFIED against Ch4 subset-selection text; correctly marked as within-protocol descriptor rather than headline inference.
- Line 160: runtimes and `>=200` sequences: partly UNVERIFIED from the requested CSVs. The `8,580` grid and `~25s` headline appear in Ch3/Ch5 release text, but runtime is environment-dependent and should not be treated as a biological result.

#### Citations
- `katoh2013mafft`: supports MAFFT use; OK.
- `nextstrain2018hadfield`, `shu2017gisaid`: support future live surveillance integration via Nextstrain/GISAID; OK.

#### Cross-Refs
- Compile-level labels resolve.
- Major semantic problem continues in the limitations matrix: rightmost “Where addressed” entries frequently point to phantom labels declared immediately before the table rather than to actual explanatory sections. For defense use, this will frustrate an examiner trying to navigate to the supporting discussion.

#### Logical Consistency
- Defense limitations matrix is largely consistent with Ch1/Ch3/Ch4 boundaries: it repeatedly frames retrospective value, small-panel adaptive limits, Layer A heterogeneity, and dual-use constraints. No overstatement detected here.

#### Outdated Content
- Line 226 “MAFFT `--auto` artifact” references Ch3; consistent with Ch3’s MAFFT description.

#### Severity
- Critical: 0
- Major: 2 (region-overlap table provenance/numerical mismatch; vaccine-stage evidence table needs explicit curated-row selection rule rather than implying direct CSV extrema)
- Minor: 1 (runtime claims are not anchored to stable CSV evidence)

### Chunk 3 (lines 221-340)

#### Numerical Claims
- Lines 238-242: contribution summary values (`8,580`, three-layer ground truth, 20 scoring formulas, 39 variants, 11 pathogens, `omega^2=0.296`, CI `[0.195,0.333]`, 9 information types, `0.265` gap, HIV-1/H3N2/SARS-CoV-2 enrichment, 4-core delta): VERIFIED against Ch1 and Ch4, with the same vaccine curated-row caveat above.
- Lines 248-254: Wave 1/2/3/4/5 and Cycle audit values: VERIFIED against Ch4 paragraphs `para:full_lattice_shapley`, `para:rank_reliability`, `para:null_calibration`, `para:p5_callability`, `para:p6_biological_nulls`, `para:w4_tier2_lopo`, `para:w5_layer_a_prime`.
- Line 284: adaptive oracle `0.160` vs EqualWeight `0.083`, seven adaptive failures, `0/12` callability: VERIFIED against Ch4 lines 704, 861-890 and `adaptive_weighting_comparison.csv`.
- Lines 265-282, future roadmap: CONSISTENT with Ch4/Ch5 evidence. Priorities are defensible: adaptive selection is already negative, feature pipeline is engineering-feasible, and 20-30+ curated pathogen validation remains the next scientific gate. No timeline is actually present despite the user’s prompt mentioning priorities/timelines; if the manuscript intends timelines, the table lacks them.
- Lines 298, 317: concluding remarks/take-home message stay within evidence. They say information-source fit matters more than detector choice “within modeled terms” and keep HIV-1 as strongest practical validation. No overstatement found.

#### Citations
- `sagulenko2018treetime`: supports TreeTime as a maximum-likelihood phylodynamic/ancestral reconstruction tool; OK.
- `turakhia2020ultrafast`: supports UShER scalable phylogenetic placement; OK.

#### Cross-Refs
- Defense map rows resolve, but row C2 cites `Paragraph~\ref{para:full_lattice_shapley}` for the `omega^2=0.296` interaction. That paragraph is about 4-core subset/Shapley robustness, not the original interaction result. The correct evidentiary anchor is Ch4 `tab:stage2_anova` / `subsec:anova_diagnostics` / Ch4 lines 393-397.
- Defense map row C1 points to `para:wave1_codex_audits`, a Ch5 paragraph about Algorithm 1 audits, not the Ch1/Ch3 benchmark artifact construction. The wording itself matches Ch1 Contribution 1, but the row’s anchor is misleading.
- C3, Wave 5, and adaptive rows align with the manuscript’s bounded framing.

#### Logical Consistency
- Minor tension: Ch5 line 298 calls the 4-feature core a “compact starting recipe for new pathogens,” while lines 248 and 258 correctly demote Algorithm 1 to an exploratory heuristic with `0/12` callability. The final sentence’s “but adaptive deployment remains bounded” mostly contains this, but the phrase “for new pathogens” should be read as retrospective prioritization, not prospective prediction.

#### Outdated Content
- No major stale “9 pathogen”/“PAHD” phrasing found. Mixed 11-pathogen and 12-pathogen language is mostly explicit and consistent with main-panel vs feature-ablation scope.

#### Severity
- Critical: 0
- Major: 2 (defense map C1/C2 misleading evidence anchors; future roadmap caption/prompt expectation mentions timelines but table has none if timelines are required)
- Minor: 1 (“new pathogens” phrasing could be misread as stronger than the bounded heuristic claim)

### Overall Assessment

Ch5 is mostly conservative in claim framing: the take-home message and concluding remarks do not overstate Ch3-Ch4 evidence, and the Layer A reproducibility limitations are factually aligned with Ch3’s heterogeneous construction. The main defects are provenance/navigation defects rather than inflated conclusions: the Layer A provenance table caption does not match the literal CSV aggregation rule; the region-overlap table does not reproduce from its cited CSV; and several defense-facing references land on phantom or mismatched anchors.

RESULT_DEEP_J5: critical=0 major=6 minor=3
