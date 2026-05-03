# Compression-Check v2 Job 9: `chapters_en/ch4_results.tex` lines 331--700

Scope note: requested path resolves in this repo as `paper/dissertation/chapters_en/ch4_results.tex`. I skipped the listed already-done items, especially the counterfactual-null paragraph and the ANOVA diagnostics 5-frame consolidation.

## Candidate 1: Nemenyi Post-Hoc Paragraph

1. **Type**: table-ize-prose
2. **Current length**: ~190 words / ~0.35 pp
3. **What it currently does**: Lines 445 report all Nemenyi null results, extreme pair examples, rank-cluster interpretation, and archive provenance in one dense paragraph.
4. **Compression strategy**: Convert to a compact post-hoc summary table plus one interpretive sentence. Example after-state: "Nemenyi post-hoc testing found no distinguishable top-20 pair: 0/190 raw-significant pairs, median p=1.000, and minimum p=0.989; the descriptive rank ordering is therefore exploratory only."
5. **Expected page saving**: 0.2 pp
6. **Expected score impact**: lift. The present paragraph is defensible but hard to parse; a small table preserves auditability and makes the null result look deliberate rather than buried.
7. **Risk**: low

## Candidate 2: LOPO Interpretation Repetition

1. **Type**: consolidate-duplicate
2. **Current length**: ~230 words / ~0.4 pp across lines 430, 447--451, and summary lines 612--616
3. **What it currently does**: Repeats that LOPO 0/11 and the 0.265 gap are null-consistent, weaker than ANOVA, and should be read as corroboration rather than independent evidence.
4. **Compression strategy**: Keep the LOPO table and a single caveat block after the permutation null; shorten the later summary bullet to one clause. Example after-state: "LOPO supports the interaction descriptively: 0/11 exact matches is null-expected, and the 0.265 gap is not permutation-significant (p≈0.25--0.28), so LOPO is corroborative rather than independent positive evidence."
5. **Expected page saving**: 0.3 pp
6. **Expected score impact**: lift. It improves pacing while retaining the statistical humility that likely helped the blind score.
7. **Risk**: low

## Candidate 3: BCa Bootstrap Explanation And SD Footnote

1. **Type**: move-detail-to-footnote
2. **Current length**: ~230 words / ~0.35 pp at lines 455--467, including a long explanatory footnote on SD definitions.
3. **What it currently does**: Reports the best fixed combination, compares it to the oracle, frames MCC=0.124 as nontrivial, and explains why two random-baseline SDs differ.
4. **Compression strategy**: Keep the three-item result list and one sentence of interpretation; move the random-baseline mechanics and SD distinction to supplement/provenance note. Example after-state: "The best fixed combination (P*E+Wavelet, MCC=0.124, BCa CI [0.047,0.202]) is above random but only 36% of the pathogen-specific oracle (0.341), so fixed selection remains materially inferior."
5. **Expected page saving**: 0.2 pp
6. **Expected score impact**: neutral to lift. The key caveat remains; the detailed SD reconciliation is mostly defensive bookkeeping and can distract from the main result.
7. **Risk**: medium

## Candidate 4: DMS Layer-A-vs-C Interpretation

1. **Type**: trim-verbose
2. **Current length**: ~210 words / ~0.35 pp at lines 576--601, after Table `tab:layer_a_vs_c`
3. **What it currently does**: States DMS/evolution correlations, threshold sensitivity, table setup, rank-correlation details, post-hoc rationale check, and practical objective-dependent recommendation.
4. **Compression strategy**: Let the table carry the six pathogen winners and replace the long rank-correlation paragraph with a 2--3 sentence synthesis. Example after-state: "Layer A and C choose different best scoring types in all six DMS pathogens. Rank agreement is mixed (RSV positive, H3N2 negative, four nonsignificant), so the two layers are non-identical rather than fully independent validation axes."
5. **Expected page saving**: 0.3 pp
6. **Expected score impact**: lift. The current paragraph over-explains an already strong table; trimming sharpens the methodological boundary without weakening the claim.
7. **Risk**: low

## Candidate 5: Information-Type Analysis Opening

1. **Type**: merge-paragraphs
2. **Current length**: ~300 words / ~0.45 pp across lines 628--636
3. **What it currently does**: Introduces the 10 features, gives per-pathogen AUC exemplars, summarizes RF AUC, feature correlations, leakage caveat, and the mechanistic conclusion.
4. **Compression strategy**: Merge the two introductory paragraphs and table-ize the feature evidence into "best feature examples / RF / correlation / caveat" rows, or cut the duplicated "why the interaction arises" setup. Example after-state: "Feature-level analyses explain the interaction: best univariate AUCs shift by pathogen, RF AUC averages 0.742, and the frequency/entropy/dN/dS cluster contrasts with decorrelated homoplasy."
5. **Expected page saving**: 0.3 pp
6. **Expected score impact**: neutral to lift. It preserves the mechanism but reduces a paragraph that currently functions like a mini-results section before the ablation table.
7. **Risk**: medium

RESULT_COMPRESS_V2_J9: candidates=5 total_pages_saved=1.3 total_score_impact=+0.3
