## 1. C11 Scores

| Axis | C10 | C11 | Rationale |
|---|---:|---:|---|
| Methodology rigor | 8.8 | 8.95 | The C10 blocker fixes materially improve defensibility: public-data IBC exemption is now explicit, the region-overlap provenance is no longer "pending," and the DOI placeholder is framed as final-submission minting. The HBFWS Cycle 7 negative result strengthens rigor because it tests, rejects, and correctly demotes an adaptive-weighting hypothesis rather than burying it. Remaining penalty: small-protocol inconsistencies around EqualWeight normalization and prospective-window counts. |
| Statistical power | 7.9 | 8.05 | The HBFWS negative result does not add power, but it clarifies what the current 11-pathogen panel cannot learn. The manuscript is now more honest about small-cluster limits, LOPO null-consistency, and adaptive-selection underidentification. Power remains bounded by 11 pathogens, 3 escape-validation pathogens, and heterogeneous Layer A definitions. |
| Novelty | 7.7 | 7.8 | The work's novelty remains the systematic region-level benchmark and pathogen-information interaction. HBFWS failure slightly weakens any claim of an adaptive method contribution, but the text now properly treats adaptive selection as future work, preserving novelty in the benchmark rather than overclaiming an algorithm. |
| Writing | 7.8 | 8.15 | v172's H8/H9 polish improves readability: the vaccine-escape table now separates the load-bearing HIV-1 single-scoring anchor from complementary EqualWeight checks, and "queued" language is gone. Some stale transitional prose remains, and a few numerical/protocol inconsistencies still interrupt trust. |
| External validity | 8.0 | 8.15 | HIV-1 is now correctly foregrounded as the clean external anchor, with H3N2 and SARS-CoV-2 discounted for circularity. The multi-pathogen prospective backtest, including mostly negative results, improves the external-validity story by bounding deployment claims. Generalization is still limited by only 3/11 escape validations and the RNA-virus/surface-glycoprotein scope. |
| Reproducibility | 8.3 | 8.45 | Provenance language is much improved: archived CSVs, stage3_full_results derivation, seed/version notes, and Zenodo timing are clearer. Remaining reproducibility risk is mostly internal consistency, not missing artifacts. |
| Defense readiness | 7.9 | 8.35 | The dissertation is substantially more defensible because it now anticipates the obvious committee attacks: ethics, circularity, mixed vaccine pipelines, LOPO overinterpretation, and failed adaptive learning. The remaining issues are fixable before defense and do not require new experiments. |

**Mean: 8.27/10.** This is a real improvement over C10's 8.06. The main gain is not higher performance; it is better claim discipline.

## 2. Remaining Actionable Issues Before Defense (all addressed in v173)

1. **Polish/high: ch5_discussion.tex:21 -- EqualWeight normalization statement was misleading.**
   Resolution: Replaced with min-max for production EqualWeight column; z-scoring restricted to nested-LOPO ablation protocol cross-reference.

2. **Polish/high: ch4_results.tex:186 vs ch5_discussion.tex:217 -- prospective backtest count mismatch (219 vs 73).**
   Resolution: ch4 now reads "73 temporal split windows ... yielding 219 top-k evaluations across k in {20, 30, 50}".

3. **Polish/medium: ch4_results.tex:826 -- H3N2 novel-only "7.19x" collided with HIV-1 headline 7.19x.**
   Resolution: Replaced with explicit "1 of 21 Layer-A-disjoint H3N2 escape positions" novel-only count plus disclaimer that this is not the HIV-1 external anchor.

4. **Polish/medium: ch5_discussion.tex:295 -- "oracle ceiling" was ambiguous.**
   Resolution: Renamed to "per-pathogen adaptive-weight oracle ceiling" with explicit cross-reference to per-combination oracle MCC 0.341 to disambiguate.

5. **Polish/low: ch3_methods.tex:938-940 -- stale chapter-transition wording.**
   Resolution: "Chapter summary"/"The following chapter" -> "Materials and methods summary"/"Chapter~\ref{ch:results} applies".

No remaining blocker.

## 3. Verdict

**Defense-ready.**

At C11, the dissertation clears the >8.0 threshold. The HBFWS negative result strengthens the thesis because it supports the central "not yet learnable from n=11" claim and prevents an overfit adaptive-method story. The C10 blocker fixes remove the main administrative/provenance risks, and v172 correctly separates the HIV-1 external anchor from mixed-pipeline EqualWeight evidence. v173 closed all five C11 polish items.

These were not new experiments; they were consistency repairs that prevent examiners from spending time on avoidable wording/provenance confusion.
