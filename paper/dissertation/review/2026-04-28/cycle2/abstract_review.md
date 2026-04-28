# Cycle 2 Codex-Style Review — Abstract & Front Matter (2026-04-28)

Targets: `front_en/abstract.tex`, `front/abstract_kr.tex`. Sync references: `chapters_en/ch1_introduction.tex`, `chapters_en/ch6_conclusion.tex`.

## A. Cycle 1 P0 Fix Verification

| ID | Location | Required Fix | Verified |
|----|----------|--------------|----------|
| G08 | abstract:8 | "two-stage" → "two-stage main + Stage~3 layer" | LANDED — `"a two-stage main experimental design plus a Stage~3 information-integration layer"` |
| G07 | abstract:11 | 4-feature paired-test caveat (nested-LOPO) | LANDED — paired delta +0.011, CI [-0.018,+0.042], permutation p=0.61 explicitly shown |
| G07 | abstract:14 | Same caveat in second mention | LANDED — same nested-LOPO numerals reused; HIV-1 7.16–8.24× anchor follows |

All three cycle-1 P0 fixes are present and self-consistent.

## B. Korean ↔ English Sync (10 numerical claims)

| # | English claim (en line) | Korean (kr line) | Drift |
|---|------------------------|------------------|-------|
| 1 | 8,580 evaluations (en:2,4) | 8,580회 (kr:6) | OK |
| 2 | 11 RNA viruses (en:2,4) | 11개 RNA 바이러스 (kr:6) | OK |
| 3 | 20 scoring formulas (en:2) | 20개 점수화 공식 (kr:6) | OK |
| 4 | 14 detection families / 39 variants (en:2) | 14개 탐지 방법군/39개 변형 (kr:6) | OK |
| 5 | ω²=0.296, CI [0.195, 0.333] (en:2,10) | ω²=0.296, CI [0.195, 0.333] (kr:16) | OK |
| 6 | 6-cat ω²=0.103 lower bound (en:10) | 6-카테고리 ω²=0.103 하한 (kr:16) | OK |
| 7 | Friedman χ²=7.69, p=0.990 (en:10) | χ²=7.69, p=0.990 (kr:17) | OK |
| 8 | LOPO 0/11, oracle gap 0.265 (en:10) | LOPO 0/11, MCC 격차 0.265 (kr:17) | OK |
| 9 | HIV-1 7.19× full, p=2.5e-16 (en:2) | 7.19배, p=2.5×10⁻¹⁶ (kr:19) | OK |
| 10 | Novel-only 7.16–8.24×, worst-case p=5e-12 (en:11,14) | **MISSING** in kr (only "novel-only 7.19배, Fisher p=0.132" for H3N2; HIV-1 novel-only band absent) | **DRIFT — P1** |

Additional drift: en:11 explicitly states **"3/11 pathogens (2,340 evaluations)"** for validation scope; kr:19 says "3개 병원체(2,340회 평가)" — OK. But en:11 carries the **nested-LOPO 4-feature equivalence numerals**; kr:22 still says **"4개 핵심 특징… 전체 앙상블 성능의 98%를 달성"** — this is the **deprecated 97.6% retention claim** that cycle-1 G07 was meant to demote. **P0-equivalent drift in Korean abstract.**

Also: kr abstract makes no mention of **Stage 3** in the design overview (kr:12 says "2단계 실험 설계" — contradicts en:8 G08 fix). **P0-equivalent drift.**

## C. Self-Defense Audit (caveats matching body honesty)

| Body caveat | Present in en abstract? | Present in kr abstract? |
|-------------|------------------------|--------------------------|
| Single-position scoring regime | YES (en:2, 10, 14 — "20-type single-position scoring regime") | PARTIAL — implicit only |
| 11 RNA viruses (scope bound) | YES | YES |
| 20-type granularity (vs 6-category) | YES (en:10 lower bound) | YES (kr:16) |
| Retrospective only / no time-forward | NO — neither abstract states this | NO |
| LOPO null-consistent corroboration | YES (en:10) | YES (kr:17, parenthetical P≈0.96) |
| HIV-1 single-anchor for 3b | YES (en:11, "primary anchor") | PARTIAL (kr:19 implies but not labeled "primary anchor") |
| 4-feature paired-test caveat | YES (en:11,14 nested-LOPO) | NO (kr:22 still says 98%) |

**Gap**: "Retrospective benchmark, no prospective validation" — absent from both abstracts. Defense risk Q2 (epi practitioner) is unmitigated at abstract level.

## D. Headline-Claim Attack Matrix

| Claim | Committee objection | Qualified in abstract? |
|-------|--------------------|-----------------------|
| "broadest region-level single-position hotspot benchmark" (en:2,4) | Concurrent benchmarks (ViroGym, EVEREST v3, ProteinGym v1.3) cover more pathogens / variants | YES — distinguishes "region-level single-position" vs "per-variant fitness regression" (en:4) |
| ω²=0.296 largest variance | Cell-level residual ω²≈0.39 is larger; selective headline | YES — en:10 reports residual ω²≈0.39 in same sentence; "**modeled** variance component" wording |
| LOPO 0/11 | Null-consistent under permutation (P≈0.96) | YES — en:10 explicit "null-consistent under permutation" |
| HIV-1 7.19× | 82% Layer A overlap risk → circular | YES — Layer-A-disjoint subset 37 positions, novel-only 7.16–8.24× (en:11) |
| H3N2 9.36× | 69% Layer A overlap | YES — labeled "self-consistency check" (en:11) |
| 4-feature equivalent to 10 | Wide CI; underpowered | YES — paired CI [-0.018,+0.042], permutation p=0.61 stated (en:11,14) |
| 9 distinct optimal types | Tranception/ESM-2 channel collinearity not separated | NO — abstract does not mention proxy/collinearity caveat (Defense Q1 unmitigated) |
| EqualWeight H3N2 4.012× | Single-pathogen integration result inflated to general claim | PARTIAL — abstract calls it "case study" (en:14) but headline figure stays |

## E. Recommended Edits

| # | File:line | Current | Proposed | Severity |
|---|-----------|---------|----------|----------|
| E1 | abstract_kr.tex:12 | "2단계 실험 설계" | "2단계 주 실험 설계 + Stage~3 정보 통합 레이어" (mirror G08) | **P0** |
| E2 | abstract_kr.tex:22 | "4개 핵심 특징…전체 앙상블 성능의 98%를 달성" | "4개 핵심 특징(homoplasy, pLDDT, entropy, freq)이 nested-LOPO 하에서 10-feature 앙상블과 운영적으로 동등(paired Δ +0.011, 95% CI [−0.018, +0.042], 부호 치환 p=0.61)" (mirror G07) | **P0** |
| E3 | abstract_kr.tex:19 | (no novel-only HIV-1 band) | Add "Layer~A-disjoint 37개 위치 novel-only 7.16–8.24배(worst-case Fisher p=5×10⁻¹²)" | P1 |
| E4 | abstract.tex:2 (headline) | "primary external anchor" | (keep) but append "(retrospective enrichment; no prospective time-forward validation)" | P1 |
| E5 | abstract.tex:13 + abstract_kr.tex:21 | "9 distinct optimal information types" | Add 1-clause caveat: "Tranception/ESM-2 channel collinearity not separated at headline granularity (see Ch3)" | P1 |
| E6 | abstract.tex:11 ("Validation is restricted to 3/11 pathogens") | (keep) | Append "by curated antibody-escape annotation availability — not by panel design" (clarity) | P2 |
| E7 | abstract_kr.tex:1–26 | Length OK | No padding; no shortening needed | — |

## F. Severity Summary

- **P0 (Korean ↔ English drift, must fix before defense): 2** — E1 (Stage~3 missing in kr), E2 (kr still uses retired 98% retention claim).
- **P1 (recommended): 3** — E3 (kr novel-only band), E4 (retrospective caveat), E5 (PLM proxy caveat).
- **P2: 1** — E6 (annotation-availability clarification).
- Cycle-1 P0 fixes (G07, G08) **landed correctly in English** but **were not propagated to Korean**. This is the headline finding of cycle 2.
- Length/density: English 17 lines, Korean 26 lines — both appropriate; no padding detected. English denser; Korean slightly more narrative but within thesis-abstract norm.
