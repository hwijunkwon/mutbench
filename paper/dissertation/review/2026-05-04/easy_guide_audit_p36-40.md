# Easy Guide Audit p36-40

## 1. 정확성 (numbers)
| Statement | Page | dissertation source | Match? |
|---|---:|---|---|
| Table 29 region-relaxed MCC values: HCV 0.660/0.588/0.519, H3N2 0.534/0.639/0.548, HIV-1 0.275/0.406/0.343, SARS-CoV-2 0.211/0.480/0.497, mean 0.341/0.472/0.454 | 36 | easy guide md 1132-1143 | Yes, table matches source. |
| Narrative says Exact MCC 0.289 -> +/-5 0.638 -> +/-10 0.712, and p37 repeats +/-10 MCC 0.712 | 37 | easy guide md 1126, 1187; Table 29 mean is 0.341/0.472/0.454 | Major mismatch/ambiguity. The narrative and table appear to use different denominators or datasets without explanation. If Table 29 is the supporting table, 0.712 is not supported. |
| Homoplasy AUC: HIV-1 0.71, HCV 0.39 | 36 | easy guide md 1151 | Yes. |
| LOPO 0/11 | 36 | easy guide md 545, 842-844; v229 reference LOPO 0/11 | Yes numerically, but interpretation is too strong because source says 0/11 is null-consistent and should be corroborative, not standalone. |
| MutBench unique contribution: omega^2=0.296; 6-category lower bound 0.103; residual omega^2 approx 0.39; HIV-1 7.19x, 82% Layer-A-disjoint, Bonferroni p=2.5e-16 | 37 | easy guide md 1173; v229 reference | Yes. Missing 37/45 novel, but numbers stated are correct. |
| Stage 1 vaccine escape table: SARS-CoV-2 34, 25/34, 4.90x, p<0.0001; H3N2 25, 6/25, 2.10x, p=0.054; HIV-1 45, 3/45, 0.35x, p=0.997 | 37 | easy guide md 1197-1199 | Matches source, but it is older Stage 1 context and can distract from v229 anchor. |
| Stage 2 HIV-1 7.19x improvement | 37 | easy guide md 1203; v229 reference | Yes, but should include p_adj=2.5e-16 and 37/45 novel / 82% disjoint when used as anchor. |
| "v98 ... Layer A optimal = escape optimal ... 2,340 evaluations" | 37 | easy guide md 1209; md 964-968 qualifies HIV-1 as clean, H3N2 self-consistency, SARS exploratory | Major stale/overstated claim. It conflicts with v229 caveat hierarchy. |
| Chapter 6 summary: 11 viruses, 20 scoring types, 14 detector families, 39 variants, 3 layers, 8,580 evaluations | 39 | easy guide md 1245-1248; v229 reference | Yes. |
| Chapter 6 summary: omega^2=0.296; HIV-1 7.19x | 39-40 | easy guide md 1253-1254, 1298; v229 reference | Yes, but incomplete anchor wording because p_adj, 82%, 37/45 are omitted in the final take-home. |
| EqualWeight H3N2 4.012x p=0.0023; HIV-1 4.17x p=0.0037; 97.6% | 39 | easy guide md 1259 | Matches source. |
| Limitations: DMS data 6/11 | 39 | easy guide md 1267; v229 reference | Yes, but v229 says Layer C 6/11 should be a primary practical evidence anchor, not only a limitation. |
| Bayesian partial-pooling omega^2=0.252, 95% HDI [0.188, 0.314], Pr(>0.14)=99.6%; ART omega^2=0.277, p=8.6e-141 | 40 | easy guide md 1275 | Matches source. |

## 2. 명확성 (clarity)
- Issues: Page 37 has a severe clarity problem around relaxed MCC. It says +/-10 MCC becomes 0.712 immediately after a table whose +/-10 mean is 0.454, without explaining whether 0.712 is from PAHD-R, another aggregation, or a separate analysis.
- Issues: Page 36 uses LOPO, oracle, MCC, precision, homoplasy, and parsimony saturation in dense paragraphs. MCC and homoplasy were defined earlier, but this chunk itself is not easy-guide friendly; at minimum "oracle" and "parsimony saturation" need one plain Korean apposition.
- Issues: Page 37 "primary external validation", "Layer A-disjoint", "Bonferroni" are technically correct but not explained in easy Korean. Add a short phrase: "기존 정답과 겹치지 않는 위치에서도..." and "여러 번 검정한 것을 보정한 p값".
- Issues: Page 39-40 limitation table is too dense for non-specialists. The ANCOVA/Bayesian/ART cell reads like dissertation notes, not a summary guide.

## 3. 일관성 (framing consistency)
- Major: Pages 37 and 39-40 still center vaccine escape and "실제 활용 가능성" more than the v229 wet-lab triage frame. The supplied reference says Layer C 6/11 + HIV-1 7.19x are anchors, with Layer C as the primary practical evidence.
- Major: Page 37 "Layer A optimal = escape optimal" conflicts with the later/stronger framing that HIV-1 is the clean external validation, H3N2 is self-consistency, and SARS-CoV-2 is exploratory after correction.
- Minor: Page 36 LOPO text says existing best methods cannot be directly applied, but omits the v229 nuance that LOPO 0/11 alone is null-consistent and should be interpreted with the oracle-vs-generalized gap and omega^2 interaction.

## 4. 누락 (missing anchors)
- Major: Layer C wet-lab anchor is missing from pages 36-40 except as "DMS data 6/11 병원체만" in the limitations table. This chunk should reference Layer C 6/11 pathogens, 650 positions, MCC 0.139-0.322, and EV-A71 0.322 + H3N2 0.245 as functional anchors.
- Minor: HIV-1 final take-home repeats 7.19x but omits p_adj=2.5e-16, 82% Layer-A-disjoint, and 37/45 novel. At least one final anchor sentence should carry these qualifiers.
- Minor: omega^2=0.296 appears, but the CI [0.201, 0.346] is absent in this chunk. Since p40 includes robustness numbers, adding the CI would strengthen consistency with v229.

## 5. 잉여 (redundancy)
- HIV-1 7.19x appears on p37, p39, and p40. This is acceptable as a cross-chapter anchor, but the repeated versions are less useful because they omit different qualifiers. Replace repetition with one complete anchor phrase.
- Page 37 Stage 1 table plus the following standalone SARS-CoV-2 sentence repeats 25/34, 73.5%, 4.9x. The standalone sentence can be cut or merged.
- Page 39-40 limitations table could be shortened by moving detailed statistical robustness values to a compact parenthetical or appendix reference.

## 6. 시각적 (layout)
- Page 36: Table 30 spans pages 36-37 with repeated header on p37. This is readable, but the text says "Table 24" while the rendered caption is "Table 30"; caption reference mismatch.
- Page 37: Tables 31 and 32 render cleanly. No obvious overflow.
- Page 38: Table 33 renders cleanly, with large blank lower half. No functional issue.
- Page 39: Table 34 is very dense and some Korean/English mixed cells wrap awkwardly, but it remains readable.
- Page 40: Table 35 is readable. No figure/caption mismatch. The requested PNG names were zero-padded in the prompt, but actual files are p-36.png to p-40.png.

## TOP 5 fixes
1. Resolve the relaxed MCC contradiction: either explain 0.712 as a separate analysis or change the narrative to match Table 29's mean +/-10 MCC 0.454.
2. Replace the p37 "v98 Layer A optimal = escape optimal" sentence with v229 wording: HIV-1 is the clean external validation; H3N2 is supportive/self-consistency; SARS-CoV-2 is exploratory.
3. Add the Layer C wet-lab triage anchor in Chapter 6: 6/11 pathogens, 650 positions, MCC 0.139-0.322, EV-A71 0.322 + H3N2 0.245.
4. Complete the HIV-1 anchor where repeated: 7.19x, p_adj=2.5e-16, 82% Layer-A-disjoint, 37/45 novel.
5. Fix "Table 24" -> "Table 30" and add simple Korean glosses for oracle, Bonferroni, Layer-A-disjoint, and parsimony saturation.

RESULT_EASY_GUIDE_AUDIT_p36_40: critical=0 major=4 minor=8 visual_issues=2
