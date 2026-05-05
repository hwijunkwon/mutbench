# Easy Guide Audit p1-5

## 1. 정확성 (numbers)
| Statement | Page | dissertation source | Match? |
|---|---:|---|---|
| 11개 RNA 바이러스에서 8,580번 비교 | 1 | `front_en/abstract.tex:2`, `chapters_en/ch3_methods.tex:764-765` = 20 scoring formulas x 39 variants x 11 pathogens | Yes |
| 정보 유형 x 바이러스 효과가 가장 큰 요인, omega^2=0.296 | 1, 3 | `front_en/abstract.tex:19`, `chapters_en/ch1_introduction.tex:132-135`; CI [0.201, 0.346] exists in source but is omitted here | Yes, but page 1/3 omit CI |
| HIV-1 백신 회피 위치 7.19배 enrichment | 1, 3 | `front_en/abstract.tex:2`, `front_en/abstract.tex:17` = 7.19x, p_adj=2.5e-16, 82% Layer-A-disjoint, 37/45 novel | Partial: headline value matches, supporting qualifiers omitted |
| RNA virus mutation rate 약 1e-5~1e-3/site/year | 1 | General background claim; not part of provided v229 anchor set | Not independently checked in this audit |
| SARS-CoV-2 Spike 484, D614G examples | 1-2 | Consistent with dissertation framing: adaptive hotspot vs founder effect distinction | Yes |
| 2020/2022 Omicron timing example | 2 | Used as explanatory example, not headline evidence | Yes |
| 평가 예시 5,000 vs 2,000 sequences | 2 | Illustrative hypothetical comparison | Acceptable, but mark as example if reader may read as dataset fact |
| HIV는 코로나의 10배, HCV 340AA vs MERS 1,330AA | 2 | `chapters_en/ch3_methods.tex:744-745`, `chapters_en/ch3_methods.tex:757` include 340-1,330 AA and positive-rate ranges; 10x mutation-rate claim not spot-verified here | Partial |
| 3층 정답 기준: Layer A/B/C | 2, 4-5 | `front_en/abstract.tex:4`; Layer C is functional validation, computed only for 6 pathogens (`chapters_en/ch3_methods.tex:739`) | Mostly yes; wording on p2 overstates “결합한 정답 기준” unless Layer C availability is immediately bounded |
| 11 x 20 scoring types (6 categories) x 14 families (5 categories, 39 variants) = 8,580 | 3-4 | `front_en/abstract.tex:18`, `chapters_en/ch1_introduction.tex:128-130` | Yes |
| “10가지 정보 유형과 14개 탐지 방법” | 3 | Source distinguishes 10 information types, 20 scoring formulas, 14 detection families, 39 variants | Minor ambiguity: “방법” should be “패밀리” or “계열” |
| Core 4 features: homoplasy, pLDDT, entropy, freq | 3 | `chapters_en/ch1_introduction.tex:152` | Yes |
| DMS available for 6 pathogens / Layer C independent validation | 5 | `front_en/abstract.tex:17`, `chapters_en/ch3_methods.tex:739` | Yes, but should be elevated earlier |
| ViroGym 13 viruses/79 DMS/552k, EVEREST 45 DMS, ProteinGym 217 DMS/90+ models | 5 | Easy-guide markdown lines 167-172; external-currentness not checked due read-only/local scope | Locally consistent |

## 2. 명확성 (clarity)
- Issues:
- p1 한줄 요약이 너무 압축되어 비전공 독자에게는 “정보 유형 x 바이러스 효과”, omega^2, PAHD-R, Core/Augmented/Review가 한 문장 안에서 한꺼번에 들어옵니다. 쉬운 뜻 문단은 좋지만, omega^2를 “성능 차이 중 이 요인이 차지하는 비중” 정도로 풀어 주면 좋습니다.
- p1 Table 1의 MCC 정의가 “-1~+1”만 있어, 0이 무작위 수준이라는 핵심 해석이 빠졌습니다.
- p2 “ground truth”가 괄호 안 영어로만 제시됩니다. “정답처럼 삼아 평가하는 기준”이라고 풀면 easy-guide 성격에 더 맞습니다.
- p3 “Per-feature AUC”, “Random Forest”, “Feature ablation”, “Vaccine escape enrichment”가 쉬운 설명 없이 연속 등장합니다. 각 용어는 한글 설명을 붙이는 편이 좋습니다.
- p4 scoring/detection 단계 설명은 구조가 좋지만, FUBAR x3, stability x2, EVEscape composite는 독자가 왜 여러 변형인지 이해하기 어렵습니다.
- p5 VEP와 hotspot detection의 학생/반 비유는 효과적입니다. 다만 “성적이 낮은 학생”은 생물학적 나쁨/좋음과 반대로 오해될 수 있어 “특정 특징을 가진 학생이 몰린 반”이 더 중립적입니다.

## 3. 일관성 (framing consistency)
- Wet-lab triage reframe은 대체로 유지됩니다. p1은 “후보 위치를 고르는 세 가지 사용 모드”, p5는 “실험 검증의 우선순위”라고 말해 deployable detector claim으로 가지 않습니다.
- 다만 p1 “실용 가능성도 확인”은 약간 강합니다. v229의 핵심은 prospective deployment가 아니라 retrospective wet-lab triage/search-space reduction이므로 “실험 우선순위를 줄이는 실용성”으로 좁히는 편이 안전합니다.
- HIV-1 anchor는 p1/p3에서 7.19배로 일관됩니다. 하지만 p_adj, 82% Layer-A-disjoint, 37/45 novel이 빠져 “깨끗한 외부 anchor”의 이유가 충분히 전달되지 않습니다.
- Layer C는 p5에서만 명시적으로 “6개 병원체”로 나오며, p1 opening에는 없습니다. v229 reference state에서는 Layer C 6/11 + HIV-1 7.19x가 practical evidence의 두 축이므로 첫 페이지에서 함께 보여야 합니다.

## 4. 누락 (missing anchors)
- Major: p1 opening summary should mention Layer C directly: “Layer C DMS는 6/11 병원체, 650 positions에서 best MCC 0.139-0.322” 정도의 짧은 문구가 필요합니다.
- Major: omega^2=0.296 appears, but CI [0.201, 0.346] is omitted. Since stale CI was a known risk, include the current CI at first technical mention or in a parenthetical note.
- Major: HIV-1 7.19x appears, but p_adj=2.5e-16, 82% Layer-A-disjoint, 37/45 novel are absent in this chunk. These are important because they explain why HIV-1 is the clean external anchor.
- Minor: non-deployability anchors (LOPO 0/11, Friedman p=0.990, HBFWS p=0.78, Cycle 7B failures) are not expected in detail yet, but p1’s PAHD-R sentence would be stronger if it explicitly says “현재 n=11에서는 자동 선택기는 학습되지 않았다” when previewing limits.

## 5. 잉여 (redundancy)
- p1 and p3 both repeat 8,580 / omega^2 / HIV-1 7.19x. This is acceptable for summary plus objectives, but p3 can shorten by referring back to the opening if page budget is tight.
- p2 limitation 1 bullets are clear but long. The DMS bullet especially can be split or shortened because DMS is defined again in Table 1 and p4.
- p4 repeats “본 연구에서는 ... 8,580회 평가” after p3. Keep both only if p4 is meant to stand alone; otherwise shorten p4 to “위 조합으로 총 8,580회”.
- p5 Table 2 is dense for an easy guide; it tries to encode task distinction, scale comparison, and claim-boundary policy in one table.

## 6. 시각적 (layout)
- Visual issue: requested filenames are `p-001.png` ... `p-005.png`, but available files are `p-01.png` ... `p-05.png`. Audit used available snapshots.
- p1-p2 Table 1 splits across pages with header repeated on p2; rendering is readable and caption matches.
- Visual issue: p4 heading “2.1.1 ... 방법론” and the following sentence appear on the same line, making the section start look cramped.
- Visual issue: p5 Table 2 is readable but crowded; multi-line study names and mixed Korean/English wrapping create uneven rows. No caption mismatch observed.
- No obvious figure/caption mismatch in pages 1-5; no figures present.
- No severe page-break failure observed.

## TOP 5 fixes
1. Add Layer C practical anchor to p1 summary: 6/11 pathogens, 650 positions, MCC 0.139-0.322.
2. Add current omega^2 CI [0.201, 0.346] at first occurrence to prevent stale-CI regression.
3. Expand HIV-1 anchor once with p_adj=2.5e-16, 82% Layer-A-disjoint, 37/45 novel.
4. Replace p1 “실용 가능성” with “실험 우선순위 축소 가능성” or equivalent wet-lab triage wording.
5. Fix p4 heading run-in and consider reducing p5 Table 2 density.

RESULT_EASY_GUIDE_AUDIT_p1_5: critical=0 major=3 minor=8 visual_issues=3
