# Easy Guide Audit p21-25

## 1. 정확성 (numbers)
| Statement | Page | dissertation source | Match? |
|---|---:|---|---|
| DMS 기준 Saturated H-score F1=0.315, 기능 영역 TC-freq-v2 F1=0.474 | 21 | easy guide md 641; multi-GT table md 618-625 | Match |
| Cohen's d d≈0.25, 전반 d<0.3 | 21 | easy guide md 643 | Match, but source provenance not independently available in workspace |
| GT 간 Jaccard 비대각선 0.006 | 21 | easy guide md 633 | Match |
| 실제 GISAID: 29,903 positions, 342 H-score>0, 1.14%, F1 0.785→0.123 | 21 | easy guide md 657; discussion md 1102 | Match |
| GISAID table: Hybrid 0.305/0.077/0.123/7.28x; Fixed 0.295/0.079/0.125/7.04x; Sliding 0.323/0.600/0.420/7.73x | 21 | easy guide md 663-668 | Match to md, but caption/cross-ref mismatch: text says Table 14 while rendered caption says Table 15 |
| "6.9~8.0배 유지" | 21 | easy guide md 659, 672 | Probably match, but table shown only reaches 7.73x; if 8.0 comes from unshown method, add note |
| 표본 수 50~5,000, 약 1,000부터 안정화, benchmark sequence count 662~5,325 all above convergence point | 22 | easy guide md 680, 692; authoritative English ch3 says total 1,311~5,325 except EV-A71 total/unique 662, unique range 530~5,019 | **Mismatch/logic error**: 662 is below ~1,000, so "모두 이 수렴점 이상" is false. If using total sequences, min is 662; if unique sequences, min is 530. |
| Figure 4 caption/text says 50~5,000 but plotted x-axis includes 10,000 and appears to start at 100 | 22 | rendered p22 figure | **Mismatch** between text/caption and figure |
| 171 weight combinations; MutClust-Hybrid 71.9% rank-1 | 22-23 | easy guide md 680, 693 | Match |
| Bootstrap CI [0.323, 0.635] | 22 | easy guide md 694 | Match to md; not one of v229 headline CIs |
| H3N2 HS 0.661 vs 0.577 | 24 | easy guide md 700 | Match to md |
| Table 16 top-3 mean MCC values | 24 | easy guide md 704-718 | Match to md; no CSV available for independent recalculation |
| 5.92x spatial contact enrichment, z=13.34; D614G rank 2 vs 1,134; rho=-0.876 | 24 | easy guide md 720-722 | Match |
| 20 scoring x 14 families (39 variants) x 11 pathogens = 8,580; per pathogen 780 | 24 | easy guide md 726-730; v229 reference state | Match |
| "11/11 고유 최적 조합" | 24-25 | rendered Table 17; English ch4 footnote notes Flu-B and MERS share freq + KDE(p=85) | **Mismatch**: Table 17 itself has Flu-B = freq + KDE(p=85) and MERS = freq + KDE(p=85). The claim should be "10/11 unique parameter tuples" or reword to "all pathogens have pathogen-specific MCC optima, with 9 distinct scoring types." |
| Table 17 MCC values HCV 0.660, H3N2 0.534, Norovirus 0.510, Flu-B 0.392, HIV-1 0.275, Dengue 0.274, EV-A71 0.260, Rabies 0.248, SARS-CoV-2 0.211, RSV/MERS 0.196 | 24-25 | easy guide md 736-750; English ch4 table | Match |

## 2. 명확성 (clarity)
- Issues: Page 21 says DMS vs 기능 영역 difference proves "Layer A와 Layer C" independence. 기능 영역 is not Layer A as defined elsewhere; either mention 수렴 진화 Layer A explicitly or say "DMS와 문헌 기반 GT는 독립적 평가 차원."
- Page 21 defines Cohen's d and enrichment well enough for non-specialists.
- Page 24-25 biological rationale paragraph is too dense: 11 pathogens are compressed into one long wrapped paragraph after PDF rendering. Convert to bullets or a compact table.
- Page 24 uses HDBSCAN, H-score, founder effect, homoplasy, rho without local redefinition. Some were defined earlier, but for an "easy guide" this page would benefit from a parenthetical reminder for homoplasy/rho.

## 3. 일관성 (framing consistency)
- No "deployable detector" overclaim appears in this chunk.
- Stage 2 framing mostly matches "pathogen-specific information choice," but page 24-25 overstates uniqueness ("11/11 고유 최적 조합") beyond the table.
- HIV-1 anchor is not discussed in this chunk except as one row in Table 17. That is acceptable if vaccine-escape validation follows later, but the p25 HIV-1 row should not be left as the practical anchor.
- Layer C is treated as independent validation on p21, but the chunk does not yet present the v229 primary practical Layer C anchor (6/11 pathogens, 650 positions, MCC 0.139-0.322).

## 4. 누락 (missing anchors)
- Missing where relevant: p21 DMS validation discusses only SARS-CoV-2-style DMS figures and does not foreshadow the dissertation-level Layer C DMS anchor: 6/11 pathogens, 650 positions, MCC 0.139-0.322.
- Missing where relevant: p24-25 introduces the 8,580 benchmark and "no universal method," but does not yet state the quantitative ANOVA anchor, omega^2=0.296 with CI [0.201, 0.346]. If this appears immediately after p25, this is a local foreshadowing issue, not a global omission.
- HIV-1 7.19x, p_adj=2.5e-16, 82% Layer-A-disjoint, 37/45 novel is absent from p21-25. It is not strictly required in these pages, but p25's HIV-1 best-method row should not be mistaken for the external-validation anchor.

## 5. 잉여 (redundancy)
- Pages 22-23 repeat stability content: 4.1.6 says two validations, then 4.2 immediately repeats sample-size and weight-sensitivity plus adds Bootstrap CI. Merge 4.1.6 and 4.2 or make 4.1.6 a short transition.
- Page 24 repeats 8,580 three times within a short block. Keep the formula once and use "이 전체 격자" afterward.
- Page 25 repeats "만능 방법이 있었다면 한 열이 전부 진한 색" in both lead-in and caption. One occurrence is enough.

## 6. 시각적 (layout)
- Page 21: text says "Table 14" but rendered caption says "Table 15." This is a visible cross-reference/caption error.
- Page 22: Figure 4 is readable, but caption says 50~5,000 while plot includes 10,000; text also says all benchmark sequence counts exceed ~1,000 despite 662.
- Page 23: Figure 5 floats alone with excessive top whitespace. Not wrong, but visually inefficient.
- Page 24-25: Table 17 splits across pages. The continued table on p25 has no "continued" marker; acceptable but could be clearer.
- Page 25: Lead-in says Figure 9, rendered caption says Figure 6. This is a visible caption mismatch.
- Page 25 heatmap is legible at page scale, though small labels are dense.

## TOP 5 fixes
1. Fix the false "all sequence counts exceed ~1,000" statement: distinguish total vs unique counts and note EV-A71/MERS exceptions as needed.
2. Correct "11/11 고유 최적 조합"; Table 17 contains a duplicate freq + KDE(p=85) for Flu-B and MERS.
3. Repair rendered numbering/cross-references: Table 14/15 on p21 and Figure 9/Figure 6 on p25.
4. Add a one-sentence Layer C anchor near p21 or p24: "전체 논문에서는 Layer C DMS가 6/11 병원체, 650 positions에서 별도 검증 축으로 쓰인다."
5. Reduce p22-23 repetition by merging 4.1.6/4.2 and making the stability validations a single concise block.

RESULT_EASY_GUIDE_AUDIT_p21_25: critical=0 major=4 minor=6 visual_issues=5
