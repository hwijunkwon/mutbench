# 논문 검증 결과 (cycle 1, 2026-05-02)

대상: master @ `7204571` (Wave 5 Layer A' substitution + revert v204/v205), `thesis_en.pdf` 236pp.
스킬: `paper-plan` 4-Phase 적대적 검증.
플랜: `docs/plans/2026-05-02-dissertation-audit-plan.md` (v2, codex review PROCEED WITH MODIFICATIONS).

## Phase 0: 자동 검증

- PASS: 129 / FAIL: 4 (raw) / WARN: 6
- **활성 빌드 기준 PASS**: 4건 FAIL 모두 orphan 파일 (`ch5_adapt`, `ch6_conclusion`, `ch2_background`) + Korean+English mirror 중복 + Korean-only 인용에서 발생. 활성 빌드(`thesis_en.pdf` 236pp)는 0 errors / 0 undefined refs / 0 multiply-defined.
- 분류 보고서: `phase0_classification.md`
- 추가 점검: 빌드 산출물 4종 존재, 마감 어조 깨끗, 페이지 일관성 OK

## Phase 1: 블루팀 논증 지도

- 핵심 주장 3개 모두 evidence 매핑 완료
  - 1: 12-pathogen literature-curated benchmark
  - 2: 1023-subset Shapley audit (4-core rank 87/1023, 3-core dominates)
  - 3: Wave 5 Layer A' Branch C
- 실패 시나리오 5개 + 방어 paragraph 매핑
- **챕터별 최약 지점**:
  - Abstract: 4-core "confirms" compactness — full-lattice downgrade 미언급
  - Ch1: Contribution 3 → 4-core practical recipe 과장
  - Ch4: para `:725` "method rather than heuristic" — 후속 audit framing과 충돌
  - Ch5: `:272` Wave 1-5 audit 단락 너무 dense

## Phase 2: 레드팀 공격 보고서

- **Critical: 0** / Major: 4 / Minor: 3
- 주요 공격 TOP 4 (모두 Major sustained):
  1. Algorithm 1 over-staked vs benchmark
  2. "not yet learnable from n=11" causally over-stated
  3. Layer A vs Layer A' provenance argument over-converted to Layer A validation
  4. ω²=0.296 headline biologically under-qualified

## Phase 2 통계 검증

- PASS: 8 / WARN: 2 / FAIL: 0
- WARN: (5) MCC vs precision@20 abstract 일관성, (10) fairness 표현은 explicit이지만 강도 보강 가능
- **Core-claim statistical reliability: medium** (retrospective benchmark 강함, operational/prospective 보통)

## Phase 3: CCB 중재

- 14건 중재
  - 해소 (a): 2건 — Wave 5 Branch C 표현, fairness 프레이밍
  - 수정 필요 (b): **12건** — 모두 prose-framing fix (구체 edit 제시됨)
  - 반박 (c): 0건
- 심각도 분쟁: Statistics WARN 10 → "이미 해결, 잔여 위험 낮음"으로 다운그레이드
- Seeded reconciliation: Blueteam Claim 2 (4-core compact) abstract/intro 표현은 Phase 2/Stats 발견에 부분 무효화 → 첫 페이지 caveat 필요
- **미해소 Critical: 0**
- **Phase 4 entry: PASS**

## Phase 4: 교수 시뮬레이션

- 평균 답 완성도: **80.5 / 100** (A− grade, 최저 7.5 = H 서술 명확성)
- 항목별 평균: A 8.4 / B 8.1 / C 8.5 / D 8.3 / E 7.8 / F 7.8 / G 8.0 / H 7.5 / I 7.9 / J 8.2
- 가장 취약한 항목 TOP 3: **H 서술 명확성 (7.5), E 결과 해석 (7.8), F 기여 독창성 (7.8)**
- 게이트:
  - Total ≥ 80/100: **PASS**
  - No item < 6: **PASS** (min 7.5)
  - No unresolved Critical: **PASS** (0건)

## 최종 판정: **통과 (조건부)** — A− grade, 12 prose-framing 수정 권고

- **판정 근거**: Phase 0/3/4 모든 게이트 통과. Critical 0건. Major 4건은 모두 prose-framing이며 fabrication/concealment 아님. CCB가 수정 시 H/F/I/E 상승 예상 → 총점 mid-80s.
- **다음 액션**:
  1. (권장) **CCB 12건 수정 적용** 후 Phase 4만 재실행 (cycle 2). 예상 작업: prose 30-60분 + Phase 4 재실행 25분 = 약 1.5시간. 예상 결과: 85+ 가능.
  2. (대안) 현재 80.5 / A− 상태로 **submit-as-is**. 디펜스 시 12건이 심사위원 공격 표면이 될 수 있음.
  3. 사용자 결정 필요: (1) vs (2).

## 산출물

- `phase0_verify.txt`, `phase0_classification.md`
- `phase1_blueteam.md` (896 words)
- `phase2_redteam.md` (1364 words)
- `phase2_statistics.md` (756 words)
- `phase3_ccb.md` (12 fix-required, 14 findings)
- `phase4_professor.md` (1504 words, 10×10 매트릭스)
- 본 summary

## 비용 실측

| 단계 | 토큰 | 시간 |
|---|---:|---|
| 코덱스 plan review | 22k | ~3min |
| M1-lite (4 prompts) | 62k | ~2min |
| Phase 0 (claude) | — | ~5min |
| Phase 1+2+Stats 병렬 | ~150k | ~5min (병렬) |
| Phase 3 CCB | 85k | ~3min |
| Phase 4 Professor | 67k | ~3min |
| **총** | **~386k** | **~25min wall** |

플랜 예상(~390k / 2h)과 일치. 병렬 실행 효과로 wall time 25분.
