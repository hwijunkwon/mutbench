# Risk Analysis 2 -- Aggressive Compression Candidates (Ch1--Ch5)

## Executive Verdict

Aggressive compression is feasible, but only as **ledger compression**, not deletion. The wet-lab triage reframe makes the old "detector benchmark failed" narrative redundant, yet the negative results remain defense-critical because they prove the boundary: MutBench is retrospective prioritization, not a deployable cross-pathogen detector.

The safest realistic target is **190--195 pages**. A hard 185-page target is possible only by moving too much robustness/audit evidence out of the main text; that would expose the thesis to "you hid the failures" and "you overfit then compressed the caveats" objections.

All mandatory numbers can survive if the main text keeps one consolidated evidence ledger containing: omega cluster CI, Friedman, LOPO gap, HBFWS, Cycle 7B, vaccine-escape enrichments, 4-core/full-10/lattice ranks, P5, Wave 4/5, Stage 1 HS/GISAID, 8,580 evaluations, and panel ranges.

## Load-Bearing Losses

Compression becomes unsafe if any of these are removed rather than ledgered:

- **Statistical backbone**: `omega^2 = 0.296` with CI `[0.201, 0.346]`, five-frame lower bounds, Friedman `chi^2 = 7.69, p = 0.990`, LOPO `0/11`, gap `0.265`.
- **Non-deployability audits**: HBFWS `p = 0.78`, Cycle 7B six paradigms `p >= 0.56`, P5 `0/12` callable, Wave 4 `8/12` positive `p=0.368`, Wave 5 `MCC=-0.055`, `2/10`.
- **Wet-lab triage anchor**: HIV-1 `7.19x`, `p_adj=2.5e-16`, `82%` disjoint; H3N2 `9.36x`; SARS `7.63x`.
- **Feature-minimality/search-space boundary**: 4-core `MCC 0.081` vs full-10 `0.070`, rank `87/1023`, 3-core rank `27`.
- **Scope and sanity checks**: Stage 1 `HS 0.778 / GISAID 0.383`; `8,580 = 11 x 20 x 39`; `11 pathogens`, `530--5019` unique seqs, `261--1330` AA, `0.7--15.9%` positive rate.

## Recommended Target

Recommended target: **192 pages**.

This assumes **20--25 pages** of savings from the listed blocks. It preserves the main evidentiary spine while replacing repeated prose with tables. Targeting **185 pages** would require compressing Ch4 cold-start/audit material and Ch3 statistical design to the point where readers may miss why the dissertation refuses deployment claims. Targeting **198--200 pages** is safer but leaves obvious redundancy and weakens the requested repositioning.

## Blocks Not To Compress

No block must remain entirely untouched, but three should not be aggressively compressed:

- **#3 Research Contributions**: rewrite to triage, but do not shrink materially. It is the contract for the whole reframe.
- **#9 Statistical Design**: trim prose, but keep equations, units of resampling, and the distinction between cell-level and pathogen-cluster evidence.
- **#14 Cold-start audit ledger prose**: compress to a ledger, but do not remove any negative audit row.

## Block-by-Block Table

| # | Block | Lines -> target lines | Table/ledger preserves numerical claims? | What is lost | Verdict |
|---:|---|---:|---|---|---|
| 1 | Ch1 Research Background | 51 -> 20--30 | Yes; Ch2 and intro tables preserve prior-art and scope claims. | Literature texture and motivation chronology. | safe |
| 2 | Ch1 Research Objectives | 82 -> ~40 | Partial; objectives have few unique numbers, but panel/evaluation scope must remain. | Fine-grained sub-objective traceability. | guarded |
| 3 | Ch1 Research Contributions | 38 -> 35--45 | Partial; Ch4/abstract ledgers preserve stats, but C1 triage must be explicit here. | If shortened, the reframe may not land. | keep |
| 4 | Ch2 DBSCAN/HDBSCAN detail | 29 -> ~12 | Yes; method mechanics are cited and Ch3 method tables preserve variants. | Tutorial explanation of density clustering. | safe |
| 5 | Ch2 PLM survey | 43 -> ~25 | Yes; PLM comparisons and ESM results are in Ch4 tables. | Per-method history for EVE/EVEscape/Tranception/EVEREST. | safe |
| 6 | Ch2 Feature-importance survey | 23 -> ~12 | Yes; Ch4/Ch5 feature analysis preserves empirical claims. | Background on Maher-style interpretability. | safe |
| 7 | Ch3 Methods overview/framework | 67 -> ~40 | Yes; pipeline figure/table and data tables preserve scope. | Some visual redundancy and narrative walk-through. | safe |
| 8 | Ch3 Stage 1 SARS-CoV-2 methods | 150 -> 80--90 | Partial; Stage 1 tables preserve HS/GISAID numerics, but setup explains sanity-check status. | Reproducibility detail for synthetic/real-data contrast. | guarded |
| 9 | Ch3 Statistical design narrative | 134 -> 90--100 | Partial; equations preserve definitions, but prose carries cluster/unit caveats. | Defense against pseudo-replication objections if over-cut. | guarded |
| 10 | Ch3 Code/data/license prose | 27 -> ~14 | Yes; provenance/license tables preserve claims. | Implementation comfort, not scientific argument. | safe |
| 11 | Ch4 Single-pathogen Stage 1 results | 98 -> ~55 | Yes; method, hotspot-score, multi-GT, and GISAID tables preserve numbers. | Detector-development storytelling. | safe |
| 12 | Ch4 Robustness/sensitivity | 82 -> ~40 | Partial; tables preserve CIs/sensitivity, but H-score saturation and indel caveats are interpretive. | Boundary explanation for why Stage 1 is only sanity check. | guarded |
| 13 | Ch4 Structural validation | 20 -> ~10 | Yes if one sentence keeps `5.92x`, `z=13.34`. | 3D intuition and structural color. | safe |
| 14 | Ch4 Cold-start algorithm/audit ledger prose | 188 -> 105--115 | Yes only if converted to ledger with all negative rows. | Audit-transcript detail, script-path narrative. | guarded |
| 15 | Ch4 ANOVA five-frame triangulation | 54 -> ~27 | Yes if omega table/ledger keeps point estimate, CI, and lower bounds. | Statistical implementation rationale. | safe |
| 16 | Ch4 Per-pathogen biology rationale | 23 -> ~12 | Partial; best-combo table preserves outcomes but not biological plausibility. | Reader intuition for pathogen-specific winners. | guarded |
| 17 | Ch4 Information-type/per-feature analysis | 77 -> ~50 | Partial; feature tables preserve AUC/MCC, but the mechanistic explanation is not fully tabular. | Why 4-core triage is plausible, not just compact. | guarded |
| 18 | Ch4 Cycle 7B six paradigms | 28 -> ~8 | Partial; table can preserve `p >= 0.56`, but exact artefact is defense-sensitive. | Explanation of why six adaptive paradigms fail. | guarded |
| 19 | Ch4 subset selection/full-lattice/Shapley | 39 -> ~17 | Partial; lattice table preserves ranks, but search-space logic is load-bearing. | Why 4-core is a triage heuristic, not optimal feature discovery. | guarded |
| 20 | Ch5 Cross-pathogen generalization | 60 -> ~36 | Partial; Ch4 ledgers preserve numbers, Ch5 must preserve interpretation. | The philosophical bridge from benchmark to finite-panel boundary. | guarded |
| 21 | Ch5 Future directions | 35 -> ~18 | Yes; future priorities can be tabled without numeric loss. | Roadmap nuance and implementation ambition. | safe |

## Total Estimated Savings

Minimum realistic saving: **20 pages**. Maximum defensible saving: **25 pages**. Stretch saving: **30 pages**, but only with appendix migration and higher defense risk.

The best compression sources are #14, #8, #9, #11, #12, #17, #19, #20, and #21. The lowest-risk trims are #1, #4--#7, #10, #13, #15, and #21.

## Recommended Execution Order

1. **Safe background/method trims**: #4, #5, #6, #1, #10.
2. **Stage 1 demotion**: #11, #8, #12, #13.
3. **Core ledgers**: #15, #14, #18, #19.
4. **Feature/triage reframing**: #17, #16, #21.
5. **Chapter 1 contract rewrite**: #2, #3.
6. **Final synthesis**: #20, then a global mandatory-number audit.

RESULT_RISK2: safe=10 guarded=10 unsafe=0 keep=1 total_pp_savings_min=20 total_pp_savings_max=25 recommended_target_pp=192
