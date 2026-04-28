# Cycle 3 Adversarial Re-attack — Chapter 6 (Conclusion)

Date: 2026-04-28 | Target: `chapters_en/ch6_conclusion.tex` (126 lines, post-cycle-2)
Cross-refs: `front_en/abstract.tex`, `chapters_en/ch1_introduction.tex` §1.4
Phase B applied: 12 fixes (see `cycle2/applied_ch6.md`)

---

## A. Phase B verification (cycle 2 — 12 items)

| ID | Site | Status | Evidence |
|----|------|--------|----------|
| G02b → PASS | ch6:13 | **PASS** | "Friedman $\chi^2=7.69$, $p=0.990$ (cluster-robust main statistic) … consistent with the interaction effect; LOPO 0/11 is null-consistent under permutation and is reported as a corroborative consistency check rather than independent evidence." Friedman elevated, LOPO alone demoted — correct asymmetry. |
| C-2 PAHD-R scope creep | ch6:16 | **PASS** | "presented as a discussion-level synthesis, not as an additional benchmark contribution." Demotion phrasing exact. |
| Contribution 3a/3b split | ch6:14–15 | **PASS** | `\textbf{Third (two-part).} \textit{(3a) … } … \textit{(3b) External validation, anchored by HIV-1}:` markers present. |
| M-1 broadest / grid / Layer A | ch6:11 | **PASS** | "to our knowledge, MutBench is the broadest \emph{region-level, single-position} hotspot-detection benchmark"; full grid 10×14(39)×11=8,580; Layer A union (convergent + immune-escape + HVR, "with immune-escape positions dominating") restored. |
| M-3 confirms → softened | ch6:95 | **PASS** | "is consistent with a feasible direction for adaptive evidence fusion, not a universal adaptive predictor." |
| Minor: p=0.0023 | ch6:14 | **PASS** | "$p = 0.0023$" inline. |
| Minor: 13-dim → high-dim | ch6:72 | **PASS** | "high-dimensional pathogen profile space". |
| Minor: future-work specificity | ch6:83 | **PASS** | "HBV polymerase, HSV-1 glycoprotein", "Nextstrain pipelines". |
| Minor: take-home qualifier | ch6:96 | **PASS** | "than the detection-algorithm main effect alone". |
| Minor: Reproduction prose | ch6:85–87 | **PASS** | new paragraph added; instantiates Priority 4. |
| Minor: 9.36× / 7.63× restored | ch6:15 | **PASS** | both numerals now explicit. |
| Minor: self-consistency check | ch6:15, 94 | **PASS** | vocabulary unified. |

**12/12 land verified.** Cycle 1 G02b PARTIAL → cycle 3 PASS.

---

## B. Cross-chapter sync (abstract / ch1 / ch6)

| Anchor | abstract | ch1 | ch6 | Verdict |
|---|---|---|---|---|
| broadest / to our knowledge / single-position | abs:4 | ch1:142 | ch6:11 | **sync** |
| 10×14(39)×11=8,580 grid | abs:2,4 | ch1:142 | ch6:11 | **sync** |
| Layer A union (3 evidence types, immune-escape dominating) | abs:6 | ch1:143 | ch6:11 | **sync** |
| ω²=0.296 (20-type) / 0.103 (6-cat) | abs:2,10 | ch1:148 | ch6:12, 93 | **sync** (ch6 still omits 95% CI [0.195, 0.333] — minor) |
| Friedman main / LOPO corroborative | abs:10 | ch1:148 | ch6:13 | **sync** |
| 4-feature LOPO (Δ+0.011, p=0.61) | abs:11,14 | ch1:150,152 | ch6:14 | **sync** |
| H3N2 4.012× p=0.0023 | abs:11 | ch1:150,153 | ch6:14 | **sync** |
| HIV-1 7.19× / novel 7.16–8.24× / Bonferroni 3.9e-9 / 780 combos | abs:11 | ch1:150,153 | ch6:15 | **sync** (abstract A-P1-5 also landed) |
| H3N2 9.36× 69% / SARS-CoV-2 7.63× exploratory | abs:11 | ch1:150,153 | ch6:15 | **sync** |
| PAHD-R | absent | absent | ch6:16 (demoted) | **no creep** |

10/10 load-bearing anchors sync. Only residual minor: ch6:12 omits the 95% cluster-bootstrap CI [0.195, 0.333] that abstract:2 / abstract:10 / ch1:148 carry.

---

## C. Adversarial re-attack — does conclusion overclaim?

1. **Stronger than abstract?** No. Conclusion HIV-1 phrasing ("strongest for HIV-1 escape enrichment", ch6:94) is weaker than abstract's "primary external anchor" (abs:2). Adaptive claim ("not a universal adaptive predictor", ch6:95) matches abstract's silence on adaptivity. **Pass.**
2. **Future-work over-promise?** ch6:62 "Adaptive method selection" expects "20–30+ pathogens + external labels" with impact "Validates selection for unseen pathogens" — borderline aspirational but explicitly conditioned on prerequisites, not promised as deliverable. ch6:74 names rice1976/kerschke2019 as the methodological frame. **Acceptable for a 5-year roadmap.**
3. **Contribution-count match across files?** **Residual minor mismatch.** ch6:10 says "four results, organized as Contributions 1, 2, 3a, 3b" while abstract:11 / ch1:150 say "Contribution 3 is two-part" (= 3 contributions) and ch1:155 explicitly states "These three contributions form a logical hierarchy." Numerically equivalent (3a+3b ≡ split-C3) but the *count word* differs (4 vs 3). A skeptical examiner could flag this as a counting-convention drift; both forms are defensible but should be unified in one direction.

---

## D. New residual findings (cycle 3)

### Major
- **M3-1 (ch6:10 vs ch1:155 / abstract:11).** Counting convention mismatch: ch6 uses "four results" while ch1/abstract use "three contributions, the third in two parts". Recommend unifying to *"three contributions, with Contribution 3 reported in two parts (3a, 3b)"* in ch6:10 to match the upstream convention; (3a)/(3b) markers downstream stay intact. Cost: 1 sentence rewrite, no ripple.

### Minor
- **m3-1 (ch6:12).** ω²=0.296 lacks the 95% cluster-bootstrap CI [0.195, 0.333] that abstract/ch1 carry. One-clause append closes it.
- **m3-2 (ch6:73).** §6.3 PAHD-R paragraph still uses positive framing ("auditable intermediate synthesis") — formally consistent with the ch6:16 demotion, but a reader who skims §6.3 alone could re-elevate it. Minor; defensible as written.
- **m3-3 (ch6:62 Future-work table).** Priority 2 "Expected impact: Validates selection for unseen pathogens" — phrasing is closer to a guarantee than to an aspiration. Soften to "Tests whether selection generalizes to unseen pathogens".
- **m3-4 (ch6:96 take-home).** "MutBench quantifies that asymmetry" — verbally strong; abstract has no analogous take-home. Acceptable as conclusion-only flourish; flagged for awareness only.

---

## E. Verdict

| Category | Count | IDs |
|---|---|---|
| Critical | 0 | — |
| Major | 1 | M3-1 (contribution count word: 4 vs 3) |
| Minor | 4 | m3-1 (CI), m3-2 (PAHD-R prose), m3-3 (Priority 2 phrasing), m3-4 (take-home strength) |

**Cycle 2 12/12 verified PASS.** All P0/P1 critical findings closed. Single residual Major (M3-1) is a counting-convention unification, not a substantive claim drift. Conclusion does not overclaim relative to abstract; PAHD-R demotion holds; future-work specificity is acceptable for dissertation horizon. **Recommend M3-1 fix before defense; m3-1…m3-4 are polish-tier.**

P0 verification trajectory: cycle 1 G02b PARTIAL → cycle 2 applied → cycle 3 confirmed PASS.
