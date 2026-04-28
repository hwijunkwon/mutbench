# Cycle 2 Adversarial Review — Chapter 6 (Conclusion)

Date: 2026-04-28 | Target: `chapters_en/ch6_conclusion.tex` (122 lines)
Cross-refs: `front_en/abstract.tex`, `chapters_en/ch1_introduction.tex` §1.4

---

## A. Cycle 1 P0 fix verification (ch6:13, 14, 15)

| ID | Site | Cycle 1 expectation | Cycle 2 verdict |
|----|------|---------------------|-----------------|
| G02b | ch6:13 | Friedman / LOPO 분리 표현 | **PARTIAL FAIL.** "Friedman ... shows no universally best combination across pathogens; LOPO 0/11 is null-consistent under permutation" — 분리 자체는 됨. 그러나 마지막 절 "both serve as corroborative consistency checks rather than independent evidence"가 다시 두 결과를 한 묶음으로 demote → Friedman은 main result (interaction effect와 독립 evidence)임에도 LOPO와 같은 corroborative tier로 끌려 내려감. abstract:10/ch1:147은 Friedman을 main 통계의 하나로 유지. |
| G07 | ch6:14 | 4-feature 97.6% paired-test caveat | **PASS.** "paired delta $+0.011$, 95% CI [$-0.018, +0.042$], sign-flip permutation $p=0.61$" 명시. nested-LOPO 명시. 97.6% 자체는 ch6에서 사용되지 않고 absolute MCC (0.070/0.081)만 쓰였음 — 이는 P0 의도(paired-test가 null임을 명시)와 더 강하게 정합. |
| G12 | ch6:15 | full vs novel-only 7.19× 분리 | **PASS.** "full-set 7.19-fold enrichment ($p_{\text{adj}}=2.5\times 10^{-16}$) and ... novel-only enrichment of 7.16--8.24$\times$ (worst-case Fisher $p=5.0\times 10^{-12}$)" — abstract:11과 동일 분리. |

P0 verification = 2 PASS / 1 PARTIAL (G02b). G02b 잔여 결함은 Section D Major M-1로 escalate.

---

## B. Contribution-claim alignment

| Contribution | ch1 (1.4) | abstract | ch6 §6.1 | match |
|---|---|---|---|---|
| C1 benchmark scope | "broadest *region-level* hotspot benchmark; 10 info types × 14 detection families × 11 pathogens = 8{,}580" (ch1:142) | "broadest region-level, single-position ... 8{,}580" (abs:2,4) | "20 scoring formulas, 39 detector variants, 3-layer GT" (ch6:11) | **MISS.** "broadest"/"to our knowledge" 삭제, "10 info types"/"14 families"/"8,580 evals" 누락. cycle 1 phase2b C1·M1 미수정. |
| C2 pathogen-dependent optimum | "$\omega^2{=}0.296$ CI [0.195,0.333]; 6-cat 0.103; 9 distinct; FUBAR/PLM/homoplasy 예시" (ch1:145–148) | 동일 + within-cell residual ≈0.39 (abs:10) | "0.296 / 0.103 / 9 distinct / 0.265 gap" (ch6:12) | **PARTIAL.** 핵심 ω² 일치. CI/residual/예시 누락. |
| C3a integration | "Contribution 3 (two-part) ... fixed 4-feature core ≈ full 10; H3N2 4.012× ($p{=}0.0023$)" (ch1:150) | "Contribution 3 is two-part" 명시 (abs:11) | 단일 "Third" 단락, two-part 마커 부재 (ch6:14) | **MISS.** Contribution count가 ch1/abstract = 4 (1, 2, 3a, 3b) vs ch6 = 3로 다르게 읽힘. cycle 1 phase2b C3 미수정. |
| C3b external validation | "HIV-1 primary anchor; H3N2 self-consistency; SARS-CoV-2 exploratory; 3-tier rule" (ch1:150,153) | 동일 + "2,340 evals" scope (abs:11) | "HIV-1 anchor; H3N2 self-consistency; SARS-CoV-2 exploratory" (ch6:15) | **PASS** post-G12. H3N2 9.36×와 SARS-CoV-2 7.63× 수치는 여전히 누락 (Minor). |
| PAHD-R | 부재 | 부재 | "PAHD-R redesign translates these findings into ... evidence-fusion workflow" (ch6:16); §6.3 본문 (ch6:70–74) | **DRIFT.** abstract/ch1에 없는 framework가 ch6 contribution 단락 끝에 등장. cycle 1 M4 미수정. ch5 산물임을 명시하거나 abstract에 한 줄 추가 필요. |

---

## C. Headline-number cross-check

| Number | ch6 | abstract | ch4/ch1 | verdict |
|---|---|---|---|---|
| ω² scoring×pathogen (20-type) | 0.296 (l.12, l.89) | 0.296 (l.2,10) | 0.296 (ch4:386,394) | match (CI 누락) |
| ω² (6-cat) | 0.103 (l.12) | 0.103 (l.10) | 0.103 (ch5:281) | match |
| Friedman χ²/p | "7.69, 0.990" (l.13) | "7.69, 0.990" (l.10) | "7.69, 0.990" (ch4:394) | match |
| LOPO 0/11 | l.13 | l.10 | ch4:423 | match (G02b 표현 잔존) |
| oracle gap | 0.265 (l.12) | 0.265 (l.10) | 0.265 (ch4:301) | match |
| oracle ceiling | 0.160 (l.72) | — | 0.160 (ch4:936) | match |
| EqualWeight | 0.083 (l.72) | "0.081/0.083" (l.11) | 0.083 (ch4:801) | match |
| 4-feature LOPO | 0.081 / 0.070 / Δ+0.011 / p=0.61 (l.14) | 동일 (l.11) | ch1:150, ch4:nested_lopo_4core | match |
| H3N2 4.012× | 4.012 (l.14, p 누락) | 4.012, p=0.0023 (l.11) | 4.012, p=0.0023 (ch4:878) | **partial** — p-value 누락 (Minor m2 잔존) |
| HIV-1 full 7.19× | 7.19, p_adj=2.5e-16 (l.15) | 동일 (l.2,11) | 동일 (ch4:874,891) | match (G12 PASS) |
| HIV-1 novel-only 7.16–8.24× | 7.16–8.24, p=5e-12 (l.15) | 동일 (l.11) | 동일 (ch4:886) | match (G12 PASS) |
| HIV-1 Layer A-disjoint % | 82% (l.15, 90) | 82% (l.11) | 82% (ch4:891) | match |
| H3N2 9.36× / overlap 69% | 69% only (l.15); 9.36× 부재 | 9.36×, 69% (l.11) | 9.36×, 69% (ch4:873,891) | **gap** (Minor) |
| SARS-CoV-2 7.63× | 부재 ("exploratory" only) | 7.63× (l.11) | 7.63× (ch4:921) | gap (intentional?) |
| simulation ρ | −0.876 (l.78) | — | ch5:254 | match |
| real GISAID ρ | −0.107 (l.78) | — | ch5:254 | match |

수치 일관성: 핵심 값 모두 일치. **CI / p-value / 보조 enrichment 수치의 체계적 누락**이 결론의 inflation 위험.

---

## D. New adversarial findings

### Critical
- **C-1 (ch6:13, G02b 잔재).** "both serve as corroborative consistency checks rather than independent evidence" — Friedman을 LOPO와 한 tier로 demote. Friedman은 abstract에서 main 통계로 보고됨 (independent evidence). 표현이 abstract claim을 약화시켜 reviewer가 "Friedman도 null-consistent corroboration?"으로 오독 가능.
- **C-2 (ch6:11 + 16, scope creep).** Contribution 단락 마지막 문장이 PAHD-R를 contribution-like framework로 도입 — abstract/ch1 어디에도 없음. 결론에서 새 contribution 등장은 박사 심사위원에게 "scope drift" 신호.

### Major
- **M-1 (ch6:11).** "broadest"/"to our knowledge" 삭제. cycle 1 phase2b C1 미수정. abstract:2/ch1:142와 강도 불일치.
- **M-2 (ch6:14).** Contribution 3가 단일 "Third" 단락 — abstract/ch1의 "two-part" 구조 (3a/3b) 미반영. Contribution count 시각적 mismatch (abstract 4 / ch6 3).
- **M-3 (ch6:91).** "the dissertation **confirms** a feasible direction for adaptive evidence fusion" — "confirms"는 강한 단정. ch4:936은 oracle gap만 evidence로 보고 → "evidences"/"supports"가 안전.

### Minor
- **m-1 (ch6:14).** 4.012× H3N2 enrichment에 p=0.0023 누락.
- **m-2 (ch6:11).** Layer A 정의가 "literature-curated adaptive positives"로 압축 — abstract:6 "convergent + immune-escape + HVR union"과 mapping 약함.
- **m-3 (ch6:72).** "13-dimensional profile space" — ch5/ch4에서 정의 출처 불명. "high-dimensional" 또는 명시적 정의 필요.
- **m-4 (ch6:81–83).** §6.3 본문이 Table:future_roadmap의 Priority 4 (Reproduction/release) 단락을 누락. 표/본문 1-1 mapping 깨짐.
- **m-5 (ch6:92).** Take-home "explains more performance variance than choosing among detection algorithms" — ch4:392의 family×pathogen ω²=0.082는 substantial. "than the detection-algorithm main effect alone" 한정 필요.

---

## E. Future-work specificity audit

| Roadmap item | Concrete? | 근거 |
|---|---|---|
| Phylogenetic/time correction | **High.** TreeTime/UShER + temporal metadata 명시, founder-bias 표적 (SARS-CoV-2) 명시 (ch6:78–79) | concrete tool/data prerequisites |
| Adaptive method selection | **Medium.** "20–30+ pathogens", meta-learning/algorithm-selection 인용 (rice1976, kerschke2019) — 그러나 numerical target (e.g., MCC 0.10 → 0.13) 부재 | tool은 명시, success criterion 부재 |
| Scope extension | **Low.** "DNA viruses, multi-protein, indel-aware scoring" — single-sentence dump (ch6:83). 어떤 DNA virus/어떤 multi-protein인지 specifics 없음 | vague |
| Reproduction & release | **Medium.** Zenodo tag/SHA은 명시; **본문 단락에서 빠짐** (m-4). 표에만 등장 | partial |

전반적으로 (1)은 strong, (2)는 actionable, (3)은 vague (가장 약함), (4)는 표만. 박사논문 "Future Work"는 보통 5년 horizon로 written — (3)에 적어도 한 specific DNA target (e.g., HBV polymerase) 추가 권장.

---

## F. Recommended cycle 2 edits

| # | file:line | severity | current | proposed |
|---|---|---|---|---|
| 1 | ch6:13 | **Critical** | "Friedman ... shows no universally best combination across pathogens; LOPO 0/11 is null-consistent under permutation; both serve as corroborative consistency checks rather than independent evidence." | "Friedman $\chi^2{=}7.69$, $p{=}0.990$ shows no universally best combination across pathogens (consistent with the interaction effect); LOPO 0/11 is null-consistent under permutation and is reported as corroborative rather than independent evidence." |
| 2 | ch6:11 | **Critical** + Major M-1, m-2 | "MutBench provides a benchmark for viral mutation hotspot detection across 11 RNA viruses, combining 20 scoring formulas, 39 detector variants, and a three-layer ground truth (literature-curated adaptive positives, constrained negatives, and DMS fitness where available)." | "To our knowledge, MutBench is the broadest region-level, single-position hotspot-detection benchmark to date for RNA viruses, combining 10 biological information types (20 scoring formulas) $\times$ 14 detection families (39 variants) $\times$ 11 pathogens = 8{,}580 evaluations, a three-layer ground truth (Layer~A union of convergent-evolution, immune-escape, and HVR evidence; Layer~B purifying-selection negatives; Layer~C DMS where available), and the hotspot-score composite metric." |
| 3 | ch6:14 | **Major M-2** + m-1 | "\textbf{Third}, multi-source integration supplies a practical cold-start floor: under nested-LOPO ..." | "\textbf{Third (two-part).} \textit{(3a) Multi-source integration infrastructure}: under nested-LOPO ... (full-10 LOPO mean MCC 0.070, fixed-4 LOPO mean MCC 0.081, paired delta $+0.011$, 95\% CI [$-0.018$, $+0.042$], sign-flip permutation $p=0.61$), and the H3N2 integration case yields 4.012-fold escape enrichment ($p=0.0023$)." |
| 4 | ch6:15 | **Major M-2** | (current opens "External validation is anchored ...") | Prepend "\textit{(3b) External validation, anchored by HIV-1}:" to mark two-part structure. |
| 5 | ch6:16 | **Critical C-2** | "The PAHD-R redesign translates these findings into a conservative evidence-fusion workflow, confirming the feasibility and audit boundaries of adaptive extension without claiming a completed universal adaptive predictor." | "Building on these three contributions, the PAHD-R synthesis (Chapter~\ref{ch:discussion}) demonstrates the feasibility and audit boundaries of an adaptive evidence-fusion workflow without claiming a universal adaptive predictor; PAHD-R is presented as a discussion-level synthesis, not as an additional benchmark contribution." |
| 6 | ch6:91 | **Major M-3** | "the dissertation confirms a feasible direction for adaptive evidence fusion" | "the dissertation evidences a feasible direction for adaptive evidence fusion" |
| 7 | ch6:72 | minor m-3 | "13-dimensional profile space" | "high-dimensional pathogen profile space" (or define 13 dims explicitly with ref) |
| 8 | ch6:83 | minor (Future-work specificity) | "Additional directions are DNA-virus extension, multi-protein evaluation, indel-aware scoring, virus-tuned PLM features, and real-time surveillance integration." | "Additional directions are: DNA-virus extension (e.g., HBV polymerase, HSV glycoprotein), multi-protein evaluation beyond surface glycoproteins, indel-aware scoring, virus-tuned PLM features, and real-time surveillance integration via Nextstrain pipelines." |
| 9 | ch6:81 | minor m-4 | (no Reproduction paragraph in §6.3 prose) | Add 1-sentence paragraph aligning with Priority 4: "**Reproduction and Release.** The archived CSVs, provenance manifest, and Zenodo tag (Section~\ref{sec:code_availability}) close the reproducibility gap as a defense-time deliverable." |
| 10 | ch6:92 | minor m-5 | "explains more performance variance than choosing among detection algorithms" | "explains more performance variance than the detection-algorithm main effect alone" |

---

## G. Adversarial committee questions (post-conclusion only)

1. **"What is the *single* strongest external evidence for your benchmark, and is it in the conclusion?"** — Answer present (HIV-1 7.19× / novel-only 7.16–8.24×, ch6:15) ✓.
2. **"Your conclusion lists three contributions but your abstract lists four (C3 two-part). Which is correct?"** — **Not answered** (M-2). Edit #3 fixes.
3. **"Where in your conclusion do you state the *limit* of your adaptive claim?"** — Answered: ch6:91 "not a universal adaptive predictor" + Limitations table (ch6:24–43) ✓.

Two of three answered without edits; question 2 surfaces an alignment gap that edit #3 closes.

---

## H. Severity summary

| Severity | Count | IDs |
|---|---|---|
| Critical | 2 | C-1 (Friedman demotion), C-2 (PAHD-R scope creep) |
| Major | 3 | M-1 (broadest 누락), M-2 (two-part 마커), M-3 (confirms→evidences) |
| Minor | 5 | m-1 (p=0.0023), m-2 (Layer A def), m-3 (13-dim), m-4 (Priority 4 누락), m-5 (main-effect 한정) |

P0 fix landing: G07 ✓, G12 ✓, G02b ◐ (PARTIAL — re-edit #1 권장).
Cycle 1 phase2b 미수정 항목: C1·C3·M4 → 본 cycle edits #2, #3, #5로 해결.
Total substantive issues found: **10** (target ≥5 satisfied).

Recommendation: **Apply edits #1, #2, #3, #5 (Critical/Major) before defense**; #4, #6 권장; #7–#10는 polish.
