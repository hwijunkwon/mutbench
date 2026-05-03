# Cycle 6 Job 3 -- Argument Focus, Flow, and Claim-Evidence Calibration

## 1. Axis 4 Results -- Argument Focus

| ID | Verdict | Evidence | Rationale |
|---|---|---|---|
| F1 | PASS | Abstract line 2 states MutBench scope, 8,580 evaluations, the scoring x pathogen interaction, Layer A caveat, and HIV-1 anchor. Ch1 also states the problem and objectives before the roadmap (`ch1_introduction.tex:33-49`, `:79-94`). | A reader can stop after page 1/abstract and state the thesis: MutBench benchmarks region-level hotspot detection and finds pathogen-dependent information-source utility, with HIV-1 as the strongest practical anchor. |
| F2 | PASS | Ch1 explicitly lists the three contributions and then says they form a hierarchy (`ch1_introduction.tex:145-158`). | The thesis can be one sentence without dropping any contribution: benchmark infrastructure -> pathogen-dependent information-source evidence -> retrospective practical validation. The sentence is long but coherent. |
| F3 | WARN | Stage 1 is labelled a SARS-CoV-2 sanity check (`ch4_results.tex:114`), Stage 2 is the primary evidence (`ch4_results.tex:244`), and Waves 1-5 are boundary audits (`ch5_discussion.tex:273-285`). | Major sections mostly serve one thesis, but the Wave 1-5 and Cycle 7/7B blocks still read partly like a second project on adaptive deployment, especially in Ch4 paragraphs `para:p5_callability` to `para:cycle7b_comparison`. |
| F4 | PASS | Ch1 subordinates Contribution 3 to external validation and treats 4-core as a methodological sanity check (`ch1_introduction.tex:91`, `:154-158`). Ch4 calls HIV-1 the load-bearing external anchor (`ch4_results.tex:943-945`). | Practical search-space reduction is framed as consequence/anchor, not as the central adaptive-method thesis. |
| F5 | PASS | Abstract assigns Stage 1 as sanity check, HIV-1 as primary anchor, H3N2 as self-consistency, SARS-CoV-2 as exploratory (`abstract.tex:10-11`). Ch4 repeats the same tiering (`ch4_results.tex:939-949`). | Pathogen roles are stable enough for defense: SARS-CoV-2 sanity/exploratory, Stage 2 main panel, HIV-1 external anchor, H3N2 self-consistency. |
| F6 | WARN | The manuscript distinguishes main 11, Stage 3 12 with Zika, 3-core/4-core, and Layer A/A' (`ch1_introduction.tex:82-91`; `ch4_results.tex:630`, `:657`, `:818-820`; `ch5_discussion.tex:275-285`). | The distinctions are usually correct but fragment attention. The 3-core superiority, historical 4-core, and Layer A' negative sensitivity require too much local memory. |

## 2. Axis 5 Results -- Flow

| ID | Verdict | Evidence | Rationale |
|---|---|---|---|
| W1 | PASS | Ch1 moves from motivation to objectives; Ch3 defines MutBench; Ch4 reports Stage 1/2/3 evidence; Ch5 interprets, limits, and concludes. | The chapter sequence matches motivation -> benchmark design -> evidence -> interpretation. |
| W2 | WARN | Ch1 roadmap says Ch4 has five sections including Cross-Pathogen Validation before the large-scale benchmark (`ch1_introduction.tex:169`). Ch4 actually opens with a Key Results box and includes late audit blocks through Cycle 7B (`ch4_results.tex:9-14`, `:822-857`). | The roadmap is directionally correct but underspecifies the large late-cycle audit load. |
| W3 | PASS | Ch3 predefines Layer A/B/C, ANOVA, LOPO, nested-LOPO, vaccine-escape Fisher tests, Bonferroni denominator, and Stage 3 scope (`ch3_methods.tex:197-230`, `:809-858`, `:903-912`). | Compared with Cycle 4, Ch3 now prepares nearly every major Ch4 analysis; remaining audit density is more presentation than missing-method failure. |
| W4 | PASS | Ch4 begins with key results, then SARS-CoV-2 sanity checks, robustness, cross-pathogen benchmark, feature/integration analyses, and practical validation (`ch4_results.tex:9-14`, `:18`, `:117`, `:222`, `:620`, `:898`). | Results now flow from central evidence to supporting and practical evidence. Some audit blocks remain dense but no longer obscure the primary Stage 2 finding. |
| W5 | PASS | Ch5 discusses circularity, small-n inference, curation heterogeneity, temporal/prospective limits, and then summarizes limitations (`ch5_discussion.tex:17-23`, `:176-213`, `:246-285`). | Limitations generally appear after the relevant result has been established and do not preempt the reader before the evidence. |
| W6 | WARN | Waves form an arc: null/rank/callability/P6, Wave 4 feature expansion, Wave 5 Layer A' negative provenance test (`ch5_discussion.tex:273-285`). | The arc is integrated conceptually, but the prose still carries scripts, branch decisions, and many numbers. It reads as an audit log more than a distilled robustness narrative. |
| W7 | PASS | Conclusion restates scope, interaction, HIV-1 anchor, H3N2/SARS-CoV-2 tiers, 4-core as bounded, and no universal predictor (`ch5_discussion.tex:328-329`). | The conclusion closes the argument without introducing new scientific claims. Dual-use and code availability are release-governance additions, not new evidentiary claims. |

## 3. Axis 7 Claim Register

| Headline claim | Location | Tier | Calibration note |
|---|---|---|---|
| MutBench is a broad region-level, single-position hotspot-detection benchmark: 11 RNA viruses, 20 scoring formulas, 39 variants, 8,580 evaluations. | `abstract.tex:2-4`; `ch1_introduction.tex:145-147`; `ch4_results.tex:244-248` | Proven | Directly established by the design and evaluation grid, assuming archived artefacts match the manuscript. |
| The optimal information source is pathogen-dependent; scoring x pathogen is the largest modeled component. | `abstract.tex:2`, `:10`; `ch4_results.tex:383-389`; `ch5_discussion.tex:240` | Proven | Strong direct in-sample benchmark evidence with robustness frames; best phrased as "within this panel and Layer A regime." |
| 9 distinct optimal information types occur across 11 pathogens. | `abstract.tex:13`; `ch1_introduction.tex:149-150`; `ch4_results.tex:261-285` | Retrospective | Observed on the current panel; uniqueness itself is partly expected by chance, so this supports rather than proves mechanism. |
| LOPO 0/11 and 0.265 oracle-vs-generalized gap show poor cross-pathogen transfer. | `abstract.tex:10`; `ch4_results.tex:391-441`; `ch5_discussion.tex:241` | Retrospective | Correctly bounded: LOPO 0/11 alone is null-consistent; the gap is descriptive and not a prospective deployment test. |
| Friedman test shows no universally best combination. | `abstract.tex:10`; `ch4_results.tex:422-435`; `ch5_discussion.tex:241` | Negative | A non-rejection/near-zero concordance result; should not be over-read as proof of no universal method. |
| HIV-1 vaccine-escape enrichment is the primary external practical anchor. | `abstract.tex:2`, `:11`, `:13`; `ch4_results.tex:925-945`; `ch5_discussion.tex:119-122` | Retrospective | Strong retrospective external enrichment, mostly Layer-A-disjoint, but no time-forward or newly curated prospective validation. |
| H3N2 vaccine-escape enrichment is a self-consistency check. | `abstract.tex:11`; `ch4_results.tex:947`, `:951-952`; `ch5_discussion.tex:120` | Retrospective | Bonferroni-significant but mostly overlapping Layer A; correctly not treated as independent replication. |
| SARS-CoV-2 vaccine-escape result is exploratory. | `abstract.tex:11`; `ch4_results.tex:939`, `:945`; `ch5_discussion.tex:121` | Suggestive | Nominal enrichment only; fails Bonferroni. |
| Practical search-space reduction from ~1,000 to 20-80 positions with 7-9x escape enrichment. | `abstract.tex:11`; `ch1_introduction.tex:154-155`; `ch4_results.tex:954-955`; `ch5_discussion.tex:242` | Retrospective | Supported mainly by winner-selected retrospective enrichment, strongest for HIV-1; should not imply prospective screening performance. |
| 4-feature core is statistically indistinguishable from full 10-feature EqualWeight under nested-LOPO. | `abstract.tex:11`; `ch1_introduction.tex:156`; `ch4_results.tex:657-688`; `ch5_discussion.tex:242` | Retrospective | Proper paired nested-LOPO support, but it is a heuristic equivalence claim, not proof of optimality. |
| 3-core may be stronger than historical 4-core; pLDDT optional/negative. | `abstract.tex:11`; `ch5_discussion.tex:275` | Suggestive | Full-lattice audit supports this as a sensitivity finding; the main recipe remains historically fixed 4-core. |
| No adaptive-weighting paradigm tested beats EqualWeight at current n=11. | `ch4_results.tex:822-857`; `ch5_discussion.tex:311-313` | Negative | Well reported as a panel-size constraint under tested methods, not a universal impossibility theorem. |
| Layer A and Layer A' are not interchangeable label provenances. | `abstract.tex:11`; `ch4_results.tex:818-820`; `ch5_discussion.tex:280-281` | Negative | Direct negative sensitivity result on UniProt-derived labels; correctly not used as validation of Layer A. |
| Prospective deployment/callability is not supported yet. | `abstract.tex:11`; `ch4_results.tex:808`; `ch5_discussion.tex:285`, `:319-320` | Future work | The abstention rule refuses current deployment; time-forward validation remains required. |
| Scope extension to DNA viruses, multi-protein, indels, epistasis, and real-time surveillance. | `ch5_discussion.tex:317` | Future work | Correctly deferred and bounded. |

## 4. Axis 7 Results -- Claim-Evidence Calibration

| ID | Verdict | Evidence | Rationale |
|---|---|---|---|
| E1 | PASS | Abstract explicitly tiers the major claims: retrospective, no prospective validation, HIV-1 primary anchor, H3N2 self-consistency, SARS-CoV-2 exploratory, Layer A' negative (`abstract.tex:2`, `:10-13`). | All abstract headline claims can be classified. |
| E2 | WARN | Most strong verbs are bounded, but Ch4 still says "demonstrates" for correct choice mattering (`ch4_results.tex:290`) and Ch5 says vaccine escape "establishes practical relevance" (`ch5_discussion.tex:98`). | Replace some "demonstrates/establishes/confirms" with "supports/quantifies/is consistent with" where evidence is retrospective or same-panel. |
| E3 | PASS | Abstract states "retrospective enrichment; no prospective time-forward validation" (`abstract.tex:2`). Ch5 says recommended use is retrospective only (`ch5_discussion.tex:285`). | Retrospective benchmark claims are consistently separated from deployment. |
| E4 | PASS | Negative results include LOPO null-consistency, Friedman/Nemenyi non-rejection, callability 0/12, Wave 5 Layer A' failure, HBFWS/Cycle 7B failures (`ch4_results.tex:437-441`, `:808`, `:820`, `:824-857`). | Null and negative results are not hidden. |
| E5 | PASS | Cluster/bootstrap intervals are tied to pathogen clusters and small-n caveats (`ch4_results.tex:480-485`); Fisher p-values use explicit 2x2 tables and Bonferroni denominator (`ch4_results.tex:909-939`); Stage 1 region bootstrap is bounded to SARS-CoV-2 (`ch3_methods.tex:890-893`). | Inferential units are mostly stated and p-values/CIs are not used as generic decoration. |
| E6 | WARN | Final conclusion is well bounded (`ch5_discussion.tex:328`), but Ch5 contribution recap says the 4-core "confirms" a practical recipe and that vaccine validation "establishes" relevance (`ch5_discussion.tex:98`, `:242`). | Conclusion avoids major upgrading, but recap language should be softened for suggestive/retrospective claims. |

## 5. Top 3 Cross-Axis Gaps and Prose Suggestions

1. **Audit arc still competes with the main thesis.** Suggestion: "The Wave audits do not add a second contribution; they bound the deployment interpretation of the same benchmark. In summary, they show that the current panel supports retrospective prioritization but refuses prospective callability."

2. **Strong verbs occasionally outrun evidence tier.** Suggestion: change "cross-validation against vaccine-escape positions establishes practical relevance" to "retrospective vaccine-escape enrichment supports practical relevance, anchored by HIV-1 and not yet prospectively validated."

3. **Core-recipe identity remains cognitively expensive.** Suggestion: "The fixed 4-core is retained as the historical cold-start recipe; the 3-core is a stronger descriptive sensitivity variant, and pLDDT should be treated as an optional structural extension."

## 6. Proposed One-Sentence Thesis if Needed

F2 does not currently fail.

## 7. Verdict Summary

Focus is medium-to-strong: the main thesis is visible and hierarchical, but the Wave/adaptive material still risks looking like a layered second project. Flow is medium-to-strong: chapter order is coherent and Ch3 now covers most major Ch4 analyses, but the robustness arc remains too log-like. Calibration is strong with minor verb-level tightening: the manuscript now distinguishes proven, retrospective, suggestive, negative, and future-work claims unusually well for a dissertation draft.

RESULT_J3: focus=medium flow=medium calibration=strong top_gap=audit_arc_competes
