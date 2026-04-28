# Codex C2: LaTeX 라벨/cross-ref Hygiene Audit

Auditor: codex IV&V Step 2
Date: 2026-04-28
Build target: `/proj/paper/paper/dissertation/thesis_en.tex` (xelatex + bibtex + xelatex × 2)

## 1. 신규 \label 정의 검증

| Label (cycle 2-3 신규) | 정의 위치 | 호출 위치 | 상태 |
|---|---|---|---|
| `tab:gt_positions` | ch3_methods.tex:370 (Table 3.3) | ch2:109, ch3:135, ch3:300 (×2), ch3:365, ch3:842, ch4:888, ch5:309 | OK (8 calls) |
| `subsubsec:cell_level_omega` | ch3_methods.tex:917 (`\phantomsection\label{...}`) | (정의만, 본문 \ref 없음 — 섹션 anchor 역할) | OK-anchor |
| `subsec:feature_correlation` | ch4_results.tex:765 | ch5:33 (1 call) | OK |
| `para:pahd_r_redesign_audit` | ch4_results.tex:1013 (`\phantomsection\label{...}`) | ch5:200 (1 call) | OK |
| `sec:esm2_leakage` | ch5_discussion.tex:271 | ch3:678 (1 forward-ref call) | OK |
| `sec:prospective_validation_gap` | ch5_discussion.tex:338 | (없음) | **ORPHAN** |
| `sec:mafft_auto_artifact` | ch5_discussion.tex:345 | (없음) | **ORPHAN** |

**주의 1**: 작업 컨텍스트는 `sec:cell_level_omega`로 명시했으나 실제 구현은 `subsubsec:cell_level_omega`. 둘 다 \ref로 호출되지 않으므로 빌드는 무사하나, 컨텍스트와 구현의 prefix 불일치는 기록.

**주의 2**: `sec:prospective_validation_gap`, `sec:mafft_auto_artifact` 두 라벨은 cycle 2 applied_ch5.md (line 57-58, 117-118) 가 abstract.tex / ch3 forward-ref를 예고했으나 **실제 cross-ref이 누락**. 정의된 \subsection은 정상 (TOC + hyperref bookmark는 작동), 그러나 본문에서 forward/back-ref가 없어 "anchor만 있는 라벨"이 됨. dangling 빌드 에러는 아님.

## 2. \ref / \cref 호출 resolve 검증

- 총 chapter 차원 \ref 호출 (`ch:introduction`-`ch:conclusion`, `ch:mutbench`): **67건 모두 resolve**
- 신규 라벨에 대한 호출: **12건 (tab:gt_positions 8 + 나머지 4) 모두 resolve**
- 미정의(undefined) \ref: **0건**
- `LaTeX Warning: Reference ... undefined`: **0건** (thesis_en.log)
- `LaTeX Warning: Citation ... undefined`: **0건**
- PDF 내 `??` 패턴 (`pdftotext | grep "??"`): **0건**

## 3. multiply-defined labels

`thesis_en.aux`의 모든 `\newlabel{...}` 항목을 sort | uniq -c 로 검증:
- 중복 정의된 라벨: **0건**
- `Label \`...' multiply defined` warning: **0건**

## 4. Bibliography (신규 11개)

`references.bib` (총 135 entries, BibTeX 0 errors/warnings):

| key | bib | cite | bbl |
|---|---|---|---|
| murrell2012meme | 1 | 1 | 1 |
| kosakovskypond2005fel | 1 | 1 | 1 |
| murrell2015busted | 1 | 1 | 1 |
| hayes2024esm3 | 1 | 1 | 1 |
| su2024saprot | 1 | 1 | 1 |
| greaney2021RBD | 1 | 1 | 1 |
| greaney2022spike | 1 | 1 | 1 |
| luksza2014predictive | 1 | 1 | 1 |
| huddleston2020integrating | 1 | 1 | 1 |
| moore2015williamson | 1 | 1 | 1 |
| lee2018h3n2dms | 1 | 4 | 1 |

11/11 모두 references.bib 정의 + 본문 인용 + .bbl 등재 (123 entries cited via bibtex). `thesis_en.blg`: 0 warnings, 0 errors.

## 5. LaTeX 빌드 결과

- `xelatex thesis_en.tex` (1차) — exit 0, 238 pages
- `bibtex thesis_en` — exit 0, 123 cited / 135 total entries, **0 warnings**
- `xelatex thesis_en.tex` (2차) — exit 0
- `xelatex thesis_en.tex` (3차) — exit 0, 238 pages, 6,604,588 bytes
- 잔존 warning: LaTeX Font Warning (cmm/cmsy/rsfs/cmr at <5.5pt, 자동 size substitution) — **본문 가독성 무영향, 라벨/ref와 무관**
- "There were undefined references" 메시지: **없음**
- "Label multiply defined" 메시지: **없음**
- chapter cross-ref (`ch:introduction`, `ch:background`, `ch:mutbench`, `ch:results`, `ch:discussion`, `ch:conclusion`) 모두 aux에 등록, 페이지 매핑 정상 (1, 13, 38, 92, 155, 188).

## 6. 발견된 문제

1. **[Minor] orphan-label 2건**: `sec:prospective_validation_gap`, `sec:mafft_auto_artifact`는 정의됐으나 본문 \ref 호출이 없음. cycle 2 plan은 `front_en/abstract.tex` retrospective caveat과 `ch3:131-135` MAFFT 자인 문장에서 forward-ref하기로 예고했으나 실제로 누락. 빌드 무영향이므로 P2-급 hygiene 잔재. 2건 추가 \ref 한 줄씩이면 닫힘.
2. **[Minor] prefix 불일치**: 컨텍스트는 `sec:cell_level_omega`로 표기했으나 실제 라벨은 `subsubsec:cell_level_omega` (ch3:917, `\phantomsection`로 정의). \ref 호출이 없어 빌드 영향 없음. 향후 컨텍스트/리뷰 문서와 코드의 prefix 통일이 바람직.
3. 그 외 dangling, multiply-defined, 미정의 cite, undefined ref **0건**.

## 종합 판정

- **LaTeX hygiene: PASS** (build clean, 0 undefined refs, 0 multiply-defined, 0 bibtex warnings, 238 pages)
- 두 orphan label은 빌드 차원에서는 무해하며, 단지 plan-vs-implementation 정합성 측면의 minor cosmetic 잔재로 분류. submission blocker 아님.
