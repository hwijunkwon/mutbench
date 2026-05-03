# Risk-3 Deep Consistency Check

Source note: `r3_deep_abstract_draft.md` is absent, so this check uses the fallback draft language in `risk3_abstract_analysis.md` lines 49-76.

## Canonical Triage-First Framing

The draft abstract now leads with practical value: MutBench is first a retrospective wet-lab triage/search-space-reduction framework, then a benchmark, then evidence for pathogen-dependent information utility, and finally a bounded non-deployability result at the current panel size. This is compatible with Risk-1 guardrails, but the chapters mostly still preserve the older contribution order: C1 benchmark, C2 pathogen-dependent interaction, C3 practical search-space reduction.

## Contribution Listings

| Location | Listing found | Classification | Reason |
|---|---|---|---|
| `risk3_abstract_analysis.md` 49-65, 73-76 | Triage/search-space reduction first; benchmark second; interaction third; non-deployability fourth | matches new triage-first framing | Opens with wet-lab triage, `~1,000 -> 10-50`, `11-32`, HIV-1 `7.19x`, panel-size guardrail, and "not a calibrated deployable detector." |
| `ch1_introduction.tex` 81-110 | Objectives 1/2/3: benchmark, factor dominance/pathogen interaction, external vaccine-escape validation | consistent but uses different ordering | Objective 3 is elevated in substance but not order; it says reduce experimental search space but lacks the full canonical HIV-1 and non-deployability phrasing. |
| `ch1_introduction.tex` 163-194 | Contribution 1 benchmark; Contribution 2 pathogen-dependent information source; Contribution 3 practical search-space reduction | consistent but uses different ordering | C3 is strong and near-canonical: `~1,000` to `10--50`, `11--32`, `7--9x`, HIV-1 novel-only `7.16--8.24x`, and "not prospectively callable detector" in table boundary. Still not triage-first ordering. |
| `ch5_discussion.tex` 125 | One-sentence C1/C2/C3 recap in Practical Implications | inconsistent / needs edit | C3 is reduced to "retrospective practical relevance" and lacks search-space economics (`10-50` / `11-32`), HIV-1 `7.19x`, and explicit wet-lab-triage-not-detector wording. |
| `ch5_discussion.tex` 238-243 | Summary of Research Contributions: First/Second/Third | consistent but uses different ordering | Strong C3 wording: `~1,000` to `10--50`, `11--32`, `7--9x`, HIV-1 `7.19x`, `p_adj`, `82%`, H3N2/SARS-CoV-2 tiering. Ordering remains old. |
| `ch5_discussion.tex` 308-310 | Defense map C1/C2/C3 | consistent but uses different ordering | C3 is scoped as "Retrospective" and "not a prospective deployment claim," but phrase should say wet-lab triage/search-space reduction explicitly. |
| `ch5_discussion.tex` 298 | Concluding remarks contribution summary | consistent but uses different ordering | Mentions interaction first, then HIV-1 practical validation, then 4-core; correctly rejects universal adaptive predictor, but not triage-first. |

No explicit Contribution 1/2/3 listing was found in `ch4_results.tex`; however, its top Key Results and Practical Validation subsection provide the chapter-level result headlines that feed C3.

## Phrases To Standardize

Use these near-identically in the abstract, ch1 contributions, and ch5 contribution/conclusion blocks:

1. HIV-1 7.19x template: "HIV-1 is the primary external anchor: full-set escape enrichment `7.19x` (`p_adj = 2.5 x 10^-16`), with `82%` Layer-A-disjoint escape positions and novel-only `7.16--8.24x` enrichment after Bonferroni correction."

2. Triage-not-detector qualifier: "MutBench should be read as a retrospective wet-lab triage tool / screening-budget allocator, not a calibrated deployable detector or prospective classifier."

3. Search-space economics: "For a typical viral protein, optimal scoring-detection combinations narrow roughly `~1,000` positions to `10--50` candidate sites (`11--32` detected positions in the three escape-enrichment anchors), with `7--9x` vaccine-escape enrichment."

4. Panel-size guardrail: "At the current `n=11` main panel, adaptive method selection is not learnable/deployable: Friedman `p=0.990`, LOPO `0/11`, P5 `0/12` callable, HBFWS `p=0.78`, and Cycle 7B failures; the `20--30+` pathogen target is a future design requirement/rule-of-thumb, not a proven sufficiency threshold."

## Result-Headline Alignment

`ch4_results.tex` top Key Results (9-14) correctly emphasizes HIV-1 `7.19x` as primary anchor but does not include search-space economics or triage-not-detector wording. Add one compact phrase after item 3 or in the box: "This supports retrospective wet-lab triage/search-space reduction, not deployable prospective detection."

`ch4_results.tex` Practical Validation (931-985) is mostly aligned: table and footnote contain HIV-1 `7.19x`, `p_adj`, `82%`, novel-only `7.16--8.24x`, and the H3N2/SARS-CoV-2 tiering. It should add the canonical `~1,000 -> 10--50` / `11--32` sentence at the subsection start or Key findings paragraph so C3 reads as search-space reduction rather than only enrichment.

`ch4_results.tex` Stage 2 / Stage 3 heuristic text at 708 says `~1,000` to `20--80`, while the abstract/ch1/ch5 contribution language says `10--50` and `11--32`. This is the main numerical inconsistency. Use `10--50` for optimal scoring-detection escape anchors and reserve `20--80` only for the Tier-1 4-core top-10% heuristic if both are retained.

## Deployable / Operational Conflicts

Needs edit:

- `ch5_discussion.tex` 5: "operationally equivalent to the full 10-feature ensemble" is too close to operational-use language in the opening paragraph. Prefer "statistically indistinguishable from the full 10-feature ensemble under nested-LOPO."
- `ch5_discussion.tex` 134: "making exhaustive detector comparison operationally feasible" is runtime-scoped but may blur with deployment. Prefer "computationally feasible for retrospective exhaustive detector comparison."
- `ch5_discussion.tex` 160: "MutBench's methodology operationalises through four steps" should be scoped as "for retrospective triage, MutBench's methodology proceeds through four steps."

Already adequately scoped:

- `ch4_results.tex` 708: "not a prospectively callable detector" is explicit.
- `ch4_results.tex` 845: "formally abstained from deployment" is explicit.
- `ch5_discussion.tex` 218, 224, 231, 248, 258, 284: deployable/deployment claims are guarded by panel-size, abstention, or retrospective-prioritization qualifiers.

## Edit Priority

1. Elevate C3 wording in ch5 Practical Implications line 125; it is the clearest contribution-list mismatch.
2. Add the triage-not-detector qualifier to ch4 Key Results and ch5 defense map C3.
3. Harmonize `10--50` / `11--32` against ch4 Tier-1 `20--80` by clarifying that the former is the optimal escape-anchor range and the latter is the generic 4-core top-10% heuristic.
4. Decide whether ch1/ch5 contribution ordering should remain C1/C2/C3 for dissertation structure or be reordered in all summary prose to match the abstract ledger. If ordering remains old, add a sentence before the list: "For the revised abstract, the practical C3 is presented first as the reader-facing impact claim."

RESULT_R3_DEEP_CONSIST: matched=1 needs_edit=3 conflicts=3
