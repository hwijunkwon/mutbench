# Ch1 Cycle 3 적대 재공격

대상: `chapters_en/ch1_introduction.tex` (172 L, post-cycle-2)
검증 출처: cycle 2 `applied_ch1.md` (12 fixes), cycle 2 `ch1_review.md` (defects).

## A. Cycle 2 결함 해소 검증 (12건)

| ID | 결함 | 해소 | 증거 (현재 ch1) |
|----|------|------|-----------------|
| 1-P0-4 (C-01) | L82 11/12 panel 모순 | YES | L82: "11-pathogen main panel, extended to 12 pathogens by adding Zika...Section~\ref{subsec:feature_ablation}" |
| 1-P0-9 (m-01) | L106 TikZ panel 11/12 | YES | L106: "(extended to 12 with Zika for feature ablation)" |
| 1-P0-6 (M-01) | L117 TikZ full-set first | YES | L117: novel-only $7.16$–$8.24\times$ leads, full-set $7.19\times$ "for completeness" |
| 1-P0-7 (M-05) | L148 Bolker n=11 caveat 누락 | YES | L148: "11 pathogen clusters places the design near the small-cluster regime---above the Bolker rule-of-thumb minimum of 5--6 but below the typical recommendation of 20--30" + cross-ref `sec:limitations` |
| 1-P0-8 (C-02) | L152 "operationally equivalent" overclaim | PARTIAL | L152 OK ("statistically indistinguishable...non-inferiority bound...not as a pre-specified equivalence claim") **BUT** L150 still reads "the operational claim of equivalence is anchored on the nested-LOPO test" — same paragraph self-contradicts |
| 1-P1-3 (M-02) | L41 "three-stage" lexical collision | YES | L41: "three-step pipeline...uses the term ``step'' for the bench-side workflow"; `grep three-stage` → 0 |
| 1-P1-5 (G08 partial) | L111 TikZ "2-Stage + Integration" | YES | L111: "2-Stage main + Stage~3 layer" |
| 1-P2-1 (m-04) | L11 self-cite `youn2025mutclust` for "core task" | YES | L11: `\cite{harvey2021tracking,carabelli2023convergent}` |
| 1-P2-2 (m-05) | L33 EVEscape/Livesey 누락 | YES | L33: `thadani2023evescape`, `livesey2020using` 추가됨 |
| 1-P2-10 (m-02) | L146 metric label 누락 | YES | L146: "9 distinct MCC-best scoring types...(MCC-best at the scoring--detector cell)"; L151 "(per-feature AUC)" 그대로 |
| 1-P2-11 (M-03) | Objectives↔Contributions 1:1 surprise 결여 | YES | L85–87: Obj 2 = "Determine which factor...dominates the variance"; Obj 3 = "Test whether a small information core is sufficient...two open questions: (i)...(ii)..." |
| 1-P2-12 (M-04) | L142 "broadest" 11-pathogen 단독 | YES | L142: "11-pathogen main panel, with the Stage~3 feature-integration analysis extended to a 12-pathogen panel by adding Zika" |

**합계: 11/12 PASS, 1 PARTIAL (1-P0-8).**

## B. Phase B 수정 부작용

- **[B-1] L150 vs L152 자체-모순 (1-P0-8 잔존).** L152는 "not a pre-specified equivalence claim" 명시했으나 L150 같은 단락이 "the operational claim of equivalence is anchored on the nested-LOPO test"로 끝남. cycle 2 매트릭스가 L152만 약화하고 L150 retention-figure 단락의 "operational claim of equivalence" 어구를 놓침. **Major** — 위원회 원샷 식별 가능.
- **[B-2] L41 안내 문장 self-referential.** "to avoid lexical collision with the Stage~1/2/3 experimental design...the present chapter uses the term ``step''" 자체가 본문에 노출 — 일반적으로 이런 메타-안내는 footnote가 깔끔. 본문 의미 손상 없음 → **Minor (스타일)**.
- **[B-3] TikZ subbox L111 길이 변화.** "2-Stage main + Stage~3 layer"가 기존 "2-Stage + Integration"보다 약 11자 김. `subbox`는 `minimum width=3cm`만 지정 — overflow 시 가시적 깨짐 가능. 컴파일 미수행이라 시각 검증 불가 → **Minor, 빌드 시 점검 필요**.
- **[B-4] L117 TikZ 정보 밀도 폭증.** Bonferroni `$p_{\text{adj}}{\approx}3.9{\times}10^{-9}$, 780 combinations`가 mainbox(`minimum width=10cm`) 한 줄에 압축. 의미 손상은 없으나 가독성 저하 → **Minor**.

## C. 새 발견

### Critical
- 없음.

### Major
- **[C-Maj-1] L150 "operational claim of equivalence" 어구.** B-1과 동일 — Ch1 같은 단락 내부 모순. **권고**: "the operational claim of equivalence is anchored on the nested-LOPO test" → "the operational non-inferiority claim is anchored on the nested-LOPO test (per the bound stated below)."

### Minor
- **[C-Min-1] L82 Objective 1 enumerated bullet 길이.** Stage~3 항목이 60+ 단어 단일 bullet — 가독성 저하. 분리 권장이지만 의미 정확.
- **[C-Min-2] L143 Contribution 1 본문에 Stage~1/2/3 panel 명시 vs L142 헤드라인 panel 명시 중복.** 완전한 모순은 아니나 같은 정보를 두 번 — 한 번은 footnote 권장.
- **[C-Min-3] L146 "FUBAR phylogenetic selection scores for H3N2"에 metric label 미부여.** 옆에 있는 RSV/SARS-CoV-2는 "(MCC-best at the scoring--detector cell)"로 묶였으나 H3N2 FUBAR와 Norovirus homoplasy는 metric label 없음. 같은 줄이라 묶음으로 해석 가능 → **Trivial**.
- **[C-Min-4] L11 `harvey2021tracking,carabelli2023convergent` 두 인용.** carabelli2023convergent는 "convergent evolution" 강조 문헌 — "core task in vaccine design" 일반 anchor로는 약간 specific. 그래도 cycle 2 권고 그대로이므로 PASS.
- **[C-Min-5] L36 self-cite (`han2025mosd`, `youn2025mutclust`)은 motivational context로 정당함** — 새 결함 아님.

## D. Defense readiness (Ch1만)

- **위원회 즉식별 결함: 1건 (B-1/C-Maj-1).** L150 "operational claim of equivalence" vs L152 "not a pre-specified equivalence claim" — 한 단락 내 자체-모순으로 적대적 심사위원이 즉시 지적할 수준. 단, 두 문장 모두 nested-LOPO 결과를 동일하게 인용하므로 의도는 명확 — **블로커는 아님**.
- **Stage~1/2/3 vocabulary 충돌**: L41 메타-안내로 명시 해소 → 위원회 식별 위험 사라짐.
- **11/12 panel 모순**: 5곳 모두 일관 (L82/L106/L142/L143/L150) → PASS.
- **숫자 정합** (8,580 / 7.19× / 9.36× / ω²=0.296 / Bonferroni 3.9e-9 / 4-core delta CI): cycle 2 매트릭스 D 표 그대로 일관 — 변동 없음.

**권고: 추가 수정 권장 (1줄 fix).** B-1 외에는 차단 위험 없음. 다음 cycle에서 단일 sed 패치로 닫힘.

## E. 잔존 cycle 3 권고

| 우선 | 위치 | 패치 |
|------|------|------|
| P1 | L150 | `the operational claim of equivalence is anchored on the nested-LOPO test` → `the non-inferiority claim is anchored on the nested-LOPO test (within the $\pm 0.04$~MCC bound stated below)` |
| P2 | L41 | "to avoid lexical collision...uses the term ``step''" 메타-문장을 footnote로 이동 (스타일) |
| P2 | TikZ L111/L117 | LaTeX 컴파일로 subbox/mainbox overflow 시각 검증 |

**합계**: Critical 0 / Major 1 (B-1) / Minor 4. Cycle 2 12-fix 중 11건 PASS, 1건 PARTIAL.
