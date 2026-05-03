# R3 Deep Anchor: HIV-1 Anchor Preservation

Scope: `abstract.tex`, `ch1_introduction.tex`, `ch4_results.tex`, and `ch5_discussion.tex`, checked against `results/mutbench/vaccine_escape_stage3.csv`.

## Source-of-truth row

CSV row 1563:

`HIV-1,freq,Wavelet(t=1.5),Wavelet,32,45,23,7.1875,3.1602957833854608e-19`

This supports the rounded manuscript row: HIV-1, `freq`, `Wavelet(t=1.5)`, enrichment `7.19x`, overlap `23/45`, with Bonferroni-adjusted `p_adj = 3.1603e-19 * 780 = 2.47e-16`, rounded as `2.5 x 10^-16`. The Layer A circularity numbers are manuscript-side audit values: `8/45` overlap with Layer A, therefore `37/45` disjoint (`82%`), novel-only enrichment `7.16--8.24x`, worst-case `p = 5.0e-12`, adjusted `p_adj ~= 3.9e-9`.

## Occurrences and Wording

### Abstract

1. Line 2: "HIV-1 vaccine-escape enrichment provides the primary retrospective external anchor." This preserves role but not numeric anchor.
2. Line 24: "HIV-1 full-set Fisher enrichment $7.19\times$ ($p_{\text{adj}} = 2.5 \times 10^{-16}$, $82\%$ Layer-A-disjoint); novel-only $7.16\text{--}8.24\times$ on 37 Layer-A-disjoint positions (worst-case $p = 5 \times 10^{-12}$; Bonferroni $p_{\text{adj}} \approx 3.9 \times 10^{-9}$ across 780 combinations)". This is the strongest full preservation.
3. Line 31: "The external practical anchor for downstream search-space reduction remains HIV-1, where the Layer-A-disjoint escape subset supports $7.16$--$8.24\times$ enrichment under the novel-only audit." Preserves novel-only result but omits full-set `7.19x`, `23/45`, and full-set `p_adj`.

### Chapter 1

1. Line 109: "Externally validate the benchmark on independently-curated vaccine-escape positions, prioritising the Layer-A-disjoint subset..." This implies the anchor without naming HIV-1 or giving values.
2. Line 112: "...culminating in external vaccine-escape validation on HIV-1 as the primary anchor for practical impact." Role preserved, values omitted.
3. Figure node line 139: "Practical Impact: HIV-1 vaccine-escape enrichment $7.19\times$ (full panel) and $7.16$--$8.24\times$ (novel-only, Bonferroni-significant) --- primary external anchor". Preserves headline and novel-only range, but omits full-set `p_adj`, `82%`, `37/45`, and `23/45`.
4. Caption line 153: "...external vaccine-escape validation on a Layer~A-disjoint subset (HIV-1, Bonferroni-significant) as the primary anchor for practical impact." Implied only.
5. Box row line 184: "Layer-A-disjoint subset of HIV-1 escape positions (37 of 45) yields direct novel-only enrichment $7.16\text{--}8.24\times$ (worst-case nominal Fisher $p = 5.0 \times 10^{-12}$; Bonferroni-adjusted $p_{\text{adj}} \approx 3.9 \times 10^{-9}$ across 780 combinations)". Strong novel-only preservation, but omits full-set `7.19x`, full-set `p_adj`, and `23/45`.

### Chapter 4

1. Line 13: "Vaccine-escape: HIV-1 \textbf{7.19$\times$} (primary anchor, $p_{\text{adj}} = 2.5 \times 10^{-16}$)..." Preserves full-set value/significance but omits `82%` and novel-only.
2. Line 451: "the HIV-1 anchor of the vaccine-escape audit..." Role only.
3. Lines 607 and 616: "single-anchor vaccine-escape enrichment audit (HIV-1 as primary external anchor...)" and "The HIV-1 vaccine-escape audit provides a separate external positive line." Role only.
4. Line 942: "HIV-1 (45 Env gp120 antibody escape sites)." Preserves `n_escape=45`.
5. Table line 959: "HIV-1 & freq & Frequency & Wavelet($t$=1.5) & \textbf{7.19}$\times$ & 23/45 & $< 0.0001$ & $***$ & external anchor". Directly matches source row after rounding.
6. Footnote line 972: "HIV-1 $p_{\text{adj}} \approx 2.5 \times 10^{-16}$ ... Layer~A overlap ... 8/45 ... HIV-1 retains 37/45 Layer-A-disjoint positions (82\%), novel-only enrichment 7.16--8.24$\times$ ... novel-only $p_{\text{adj}} ... \approx 3.9 \times 10^{-9}$." Full preservation except the footnote is separated from the table row.
7. Line 977: "The load-bearing external anchor is the single-scoring HIV-1 7.19$\times$ enrichment row (82\% Layer~A-disjoint escape set, novel-only $p_{\text{adj}} \approx 3.9 \times 10^{-9}$)..." Strong, but omits `23/45`, full-set `p_adj`, and novel-only range.
8. Lines 979 and 984 contrast H3N2/SARS-CoV-2 with "the HIV-1 external anchor" and "why HIV-1 is the least circular external validation." Role/circularity only.

### Chapter 5

1. Line 19: "HIV-1 (82\% of its escape set disjoint from Layer~A) is the cleanest external anchor..." Preserves disjointness only.
2. Line 49: "(HIV-1 82\% Layer-A-disjoint novel-only audit)..." Preserves circularity framing only.
3. Line 76: "HIV-1 vaccine-escape cross-check ($7.19\times$, 82\% Layer-A-disjoint) as the strongest external anchor." Preserves headline and disjointness, omits p-values and counts.
4. Line 125: "anchored by HIV-1 with 82\% Layer-A-disjoint novel-only enrichment". Role/disjointness only.
5. Line 131: "7.19$\times$ for HIV-1... HIV-1 ($p_{\text{adj}} = 2.5 \times 10^{-16}$) ... HIV-1 (82\% of escape set disjoint from Layer~A; external validation)". Strong full-set preservation, omits novel-only range/p.
6. Line 146: "HIV-1 passes both criteria (18\% Layer~A overlap, $p_{\text{adj}} = 2.5 \times 10^{-16}$) ... novel-only test on 37 Layer~A-disjoint positions gives $7.16\text{--}8.24\times$ enrichment..." Strong, but omits full-set `7.19x` and `23/45`.
7. Line 219: "headline values ... HIV-1 $7.19\times$, $p_{\text{adj}} = 2.5 \times 10^{-16}$". Full-set reproducibility only.
8. Line 242: "External validation is anchored by HIV-1: the escape set is largely Layer~A-disjoint (82\%) and yields full-set $7.19\times$ enrichment ($p_{\text{adj}} = 2.5 \times 10^{-16}$) plus a novel-only $7.16$--$8.24\times$ Bonferroni-significant subset..." Strongest Ch5 preservation.
9. Line 298: "The practical validation is strongest for HIV-1 escape enrichment (7.19$\times$, 82\% Layer~A-disjoint)..." Preserves headline/disjointness only.
10. Line 310: "`Retrospective practical anchor on HIV-1 with $82\%$ Layer~A-disjoint novel-only enrichment...'" Role/disjointness only.

## Consistency Assessment

The anchor is directionally consistent across all four files: HIV-1 is always treated as the primary/strongest/cleanest external practical anchor; the full-set enrichment is consistently rounded to `7.19x`; `p_adj = 2.5e-16` appears in abstract, Ch4, and Ch5; and the novel-only audit is consistently `37/45`, `82%`, `7.16--8.24x`, `p_adj ~= 3.9e-9` wherever fully stated.

The preservation is still partial, not fully consistent. Chapter 1 lacks a single full canonical sentence containing both full-set and novel-only evidence. Several Ch4/Ch5 mentions state only "HIV-1 anchor" or only `7.19x, 82%`, leaving out `23/45`, full-set `p_adj`, and/or novel-only `p_adj`. The Ch4 table row correctly reports `23/45` and `7.19x`, but its `p < 0.0001` cell depends on the footnote for the Bonferroni-adjusted value.

## Canonical Template

Recommended single sentence:

"HIV-1 is the primary retrospective external anchor: `freq + Wavelet(t=1.5)` detects 23/45 Env gp120 antibody-escape sites, giving 7.19x enrichment (`p_adj = 2.5 x 10^-16`), and because 37/45 escape sites are Layer-A-disjoint (82%), the novel-only audit remains 7.16--8.24x enriched with Bonferroni-adjusted `p_adj ~= 3.9 x 10^-9`."

Use this exact content in the abstract, the Chapter 1 introduction box, the Chapter 4 table/footnote or adjacent key-finding sentence, and the Chapter 5 conclusion. The table can keep compact columns, but the footnote/key sentence should include the same complete tuple.

RESULT_R3_DEEP_ANCHOR: occurrences=37 consistency=partial canonical_template="HIV-1 is the primary retrospective external anchor: freq + Wavelet(t=1.5) detects 23/45 Env gp120 antibody-escape sites, giving 7.19x enrichment (p_adj = 2.5 x 10^-16), and because 37/45 escape sites are Layer-A-disjoint (82%), the novel-only audit remains 7.16--8.24x enriched with Bonferroni-adjusted p_adj ~= 3.9 x 10^-9."
