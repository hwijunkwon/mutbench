# Easy Guide Audit p41-42

## 1. 정확성 (numbers)
| Statement | Page | dissertation source | Match? |
|---|---:|---|---|
| v229, 2026-05-04 final-state appendix | 41 | `dissertation_easy_guide_v2.md:1304` | Match |
| P5 abstention 0/12 callable | 41 | `results/mutbench/codex_wave3/README.md:7` reports Wave 2 pre-registered abstention 0/12 callable | Match, but needs scope note because adjacent text says `n=11` panel |
| Protein ~1,000 positions -> 10-50 candidates; 7-9x escape enrichment | 41 | Easy-guide anchors include HIV-1 7.19x, H3N2 9.36x, SARS-CoV-2 7.63x (`dissertation_easy_guide_v2.md:941-943`) | Match as rounded range, but underspecified |
| Generalization algorithm not learnable from n=11 panel | 41 | LOPO 0/11 and oracle-vs-generalized gap discussed at `dissertation_easy_guide_v2.md:842-844` | Match framing |
| Phase 4 v6: 215pp, 77.52, conditional | 41 | `professor_v6_aggregate.md:37,122`; source table `dissertation_easy_guide_v2.md:1318` | Match |
| Phase 4 v8: 197pp, 83.63 PASS | 41 | `professor_v8_aggregate.md:45,97`; source table `dissertation_easy_guide_v2.md:1319` | Match |
| Phase 4 v9: 197pp, 83.31 PASS current | 41 | `professor_v9_aggregate.md:37,79`; source table `dissertation_easy_guide_v2.md:1320` | Match |
| Gate thresholds: total >=80, item mean >=6, skill mean >=7, individual >=5 | 41 | `dissertation_easy_guide_v2.md:1322`; `professor_v9_aggregate.md:59-64` | Match |
| Layer C DMS 6/11 pathogens | 41 | `dissertation_easy_guide_v2.md:382,386,1326`; `layer_c_evaluation.csv` has six pathogens | Match |
| SARS-CoV-2 Layer C: n=247, plddt_inv + KDE(p=75), MCC 0.186 | 41 | `results/mutbench/layer_c_evaluation.csv`: best mcc_layer_c 0.185644 | Match rounded |
| H3N2 Layer C: n=112, semantic_change + KDE(p=80), MCC 0.245 | 41 | `layer_c_evaluation.csv`: best 0.244504 | Match rounded |
| HIV-1 Layer C: n=48, fubar + Wavelet(t=2.0), MCC 0.139 | 41 | `layer_c_evaluation.csv`: best 0.138527 | Match rounded |
| RSV Layer C: n=101, EVEscape_composite + KDE(p=75), MCC 0.180 | 41 | `layer_c_evaluation.csv`: best 0.180434 | Match rounded |
| Rabies Layer C: n=87, homoplasy + ScoreDBSCAN(ep=8), MCC 0.182 | 41 | `layer_c_evaluation.csv`: best 0.181990 | Match rounded |
| EV-A71 Layer C: n=55, plddt_inv + Wavelet(t=1.5), MCC 0.322 | 41 | `layer_c_evaluation.csv`: best 0.322436 | Match rounded |
| Layer C total positions implied by table: 650 | 41 | Sum of n_gt_c in `layer_c_evaluation.csv`: 247+112+48+101+87+55=650 | Match, but not stated |
| 6/6 Layer A optimum != Layer C optimum | 41 | Source states this at `dissertation_easy_guide_v2.md:1337`; detailed table at `dissertation_easy_guide_v2.md:848-861` | Match |
| flow-improve: 197pp 83.31; 158pp 81.85 (-1.46); 153pp 80.86 (-0.99) | 41 | `dissertation_easy_guide_v2.md:1341-1346` | Match |
| Master v229 commit aa13920, 197pp, 83.31 PASS | 41 | `dissertation_easy_guide_v2.md:1350`; v9 aggregate 83.31 | Match |
| Hidden issues 49; 0 framing inconsistencies; 0 orphan refs | 42 | `professor_v9_aggregate.md:79`; final-audit aggregate reports 0 framing inconsistencies | Match |
| Visual layout sample 6 pages; defense-ready GREEN | 42 | `dissertation_easy_guide_v2.md:1353-1354`; `professor_v9_aggregate.md:64` | Match |

## 2. 명확성 (clarity)
- Issues: `0/12 callable` and `n=11 panel` appear in adjacent bullets without explaining that the 12-pathogen abstention scope differs from the 11-pathogen benchmark panel. This is easy to misread as a denominator error.
- Issues: `P5 abstention`, `callable`, `prospective`, `panel-size threshold`, `2-stage hybrid`, `Layer C DMS`, `MCC`, `KDE`, `Wavelet`, `ScoreDBSCAN`, and `functional anchor` are used in an appendix summary without plain Korean definitions. The page is more an expert audit memo than an easy guide.
- Issues: The Layer C table is numerically sound, but non-specialist readers need one sentence: "MCC는 -1~1 점수이고 0보다 클수록 실험 데이터와 더 잘 맞는다."
- Issues: The flow-improve paragraph is dense in the PDF because the three markdown bullets render inline after a colon.

## 3. 일관성 (framing consistency)
- Strong: The chunk explicitly rejects `deployable detector` and frames MutBench as a wet-lab experiment prioritization tool. This matches the v229 triage reframe.
- Strong: Layer C is presented as the main practical anchor, not a side note.
- Minor issue: The phrase `7-9x escape 농축` invokes the vaccine-escape anchor but does not name HIV-1 7.19x as the clean external validation. Elsewhere the guide treats H3N2/SARS more cautiously, so the appendix should avoid sounding like all three are equally strong.

## 4. 누락 (missing anchors)
- Major: The appendix does not restate `ω²=0.296` or its CI `[0.201, 0.346]`, even though it summarizes the final dissertation state and mentions n=11 generalization failure. Add the core "정보 유형 x 바이러스" effect anchor.
- Major: The HIV-1 primary external anchor is missing in numeric form: `7.19x`, `p_adj=2.5e-16`, `82% Layer-A-disjoint`, `37/45 novel`. The current `7-9x` range is too generic for a final-state summary.
- Minor: The Layer C table implies the 650-position anchor but does not state it. Add "6개 병원체, 650 positions" to make the anchor explicit.
- No missing Layer C anchor: `6/11 pathogens` and all six MCC rows are present.

## 5. 잉여 (redundancy)
- Low redundancy. The chunk repeats `197pp` and `83.31` several times, but this is acceptable in a final-state appendix.
- The sentence about tables/figures affecting reviewer trust can be shortened; it is meta-process commentary and less useful than one more sentence defining Layer C/MCC.
- `Defense readiness` duplicates the Phase 4 gate table. Consider retaining only the master line plus hidden/layout status.

## 6. 시각적 (layout)
- Table rendering: Layer C table aligns correctly and values are readable on p41.
- Visual issue: The check-mark emoji in the Phase 4 table and p42 final status renders as a boxed/missing glyph, not a clean check/green marker. Replace emoji with ASCII `PASS`/`GREEN` or a LaTeX-safe symbol.
- Visual issue: The flow-improve bullet list collapses into one paragraph with inline hyphen bullets, reducing readability.
- Visual issue: p42 is an orphan continuation page with only three bullets at the top and large blank space. Pull those bullets back to p41 if possible or force a cleaner appendix page break.
- Minor visual issue: The prompt references `p-041.png`/`p-042.png`, but the actual files are `p-41.png`/`p-42.png`; audit used the existing snapshots.

## TOP 5 fixes
1. Add one compact anchor sentence under "정체성 재정의" or before Defense readiness: `핵심 통계 근거는 정보 유형 x 바이러스 상호작용 ω²=0.296, 95% CI [0.201, 0.346]입니다.`
2. Replace `7-9x escape 농축` with a bounded version: `HIV-1 7.19x (p_adj=2.5e-16; 82% Layer-A-disjoint; 37/45 novel)을 primary external anchor로, H3N2 9.36x/SARS-CoV-2 7.63x는 보조/탐색 근거로 둠`.
3. Explain denominator scope: `0/12 callable은 P5 prospective/callability 확장 스코프, n=11은 본 벤치마크 패널`.
4. Replace emoji check/green markers with PDF-safe `PASS`, `OK`, or LaTeX check symbols; verify p41/p42 after rebuild.
5. Convert the flow-improve inline paragraph back to true bullets and avoid orphaning the final three Defense readiness bullets on p42.

RESULT_EASY_GUIDE_AUDIT_p41_42: critical=0 major=2 minor=6 visual_issues=3
