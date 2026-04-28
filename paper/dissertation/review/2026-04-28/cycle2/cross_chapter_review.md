# Cycle 2 Cross-Chapter Consistency Review (2026-04-28)

Scope: abstract, ch1, ch3, ch4, ch5, ch6 (English). No per-chapter deep review. Line numbers are absolute.

---

## A. Master Numerical Claims Table

| Number | Abstract | Ch1 | Ch3 | Ch4 | Ch5 | Ch6 | Status |
|---|---|---|---|---|---|---|---|
| 8,580 evals | L4, L11 | L82, L142 | L6, L562, L972 | L7, L292, L1040 | L283 (verifies via 8,580 obs) | L105 | **CONSISTENT** |
| 11 pathogens / 11 RNA viruses | L2, L4, L10–11 | L78, L82, L142 | L6, L28, L140, L171 (and ~30 more) | L277, L292, L303, etc. | many (L82, L84, L319, …) | L11 | **CONSISTENT** |
| 20 scoring types | L2, L11 | L82, L142–143 | L6, L171, L562, L700 | L11, L277, L293 | L281, L295 | implied L11 | **CONSISTENT** |
| 39 detectors / 14 families | abstract L2 (39); L4 implied | L82 (39 from 14), L143 (4 of 6 cat.) | L6 (14 fam, 39 var), L191, L700, L706 | L7 (14 fam / 39 var), L277 | L298 (14 fam) | L11 (39) | **CONSISTENT** — no "41 detectors / 15 families" in any chapter |
| ω² = 0.296 | L2, L10 | L114, L145, L148 | L839 | L11, L338, L396, L403, L421, L425, L429, L431, L598, L912, L1030, L1040 | L70, L82, L93, L155, L283, L290, L320 | L12, L89 | **CONSISTENT** |
| CI [0.195, 0.333] | L2, L10 | L148 | L176, L523 | L429, L598, L1040 | L285 (cluster lower 0.195) | — | **CONSISTENT** |
| Within-cell residual ω² ≈ 0.39 | L10 | — | — | L396, L421, L425, L431, L598, L1040 | L279 (0.39) | — | **CONSISTENT** as "within-cell residual"; ch5 L279 calls it 0.39 (not 0.234). 0.234 is "cell-level baseline" in ch5 L290 (ANCOVA), distinct quantity. |
| LOPO 0/11 | L10 | L145–146, L148 | — | L12, L13, L245, L336, L446, L458, L462, L478, L599, L600, L1040 | L155, L319, L321 | L13 | **CONSISTENT**, all caveat-tagged "null-consistent" |
| Friedman p = 0.990 | L10 | L147 | — | L429, L466, L469, L473, L601 | L319 | L13 | **CONSISTENT** |
| HIV-1 7.19× full-set | L2, L11, L14 | L117 (TikZ), L150, L153 | — | L13, L943, L961, L991, L1041 | L93, L155, L161 | L15, L90 | **CONSISTENT** |
| HIV-1 novel-only 7.16–8.24× | L11, L14 | L117, L150, L153 | — | L956, (implied 1041 via "novel-only enrichment") | L176 | L15 | **CONSISTENT** |
| Worst-case Fisher p = 5×10⁻¹² | L11 | L150, L153 | — | L956 | — (referenced indirectly L176) | L15 (5.0×10⁻¹²) | **CONSISTENT**; ch5 omits the explicit number but cites the equivalent worst-case test (L176) |
| Bonferroni p_adj = 3.9×10⁻⁹ | — | L150 | — | L956 | — | — | **PARTIAL** — only ch1 + ch4. **Drift**: not in abstract / ch5 / ch6 (only the unadjusted 5×10⁻¹² appears). Acceptable since 5×10⁻¹² is the worst-case nominal; 3.9×10⁻⁹ is the corresponding Bonferroni and survives. |
| 4-feature 97.6% retention | L11 (paired delta primary; 97.6 not stated) | L150 (97.6% within-pathogen, demoted) | — | L839 (97.6% retained as ablation descriptor) | L192, L244 (98% numerical, "no paired-sample test") | L14 (paired delta primary, no "97.6") | **CONSISTENT but uneven**: ch5 L192 says "retained 97.6%", ch5 L244 says "98%". Both flag the protocol but the 97.6/98 alternation is minor cosmetic drift. |
| 9 distinct optimal types | L13 | L145, L146 | — | L307 caption, L481, L599, L784 | — | L12 (9 distinct), L89 (nine distinct) | **CONSISTENT** |

**No mismatches in headline numbers.** All headline values resolve to the same source (results/mutbench archive). Note the task brief listed "41 detector instances / 15 detector families" as a possible ch3 inconsistency — I checked and **found neither 41 nor 15 anywhere**; canonical (39, 14) is uniform.

---

## B. Two-Stage Vocabulary Audit (G08 fix)

| File | Line | Form |
|---|---|---|
| abstract.tex | 8 | "two-stage main experimental design plus a Stage~3 information-integration layer" |
| ch1 | 82 | "A two-stage main experimental design with a Stage~3 information-integration layer" |
| ch1 | 143 | "two-stage main experimental design plus a Stage~3 information-integration layer" |
| ch3 | 7 | "two-stage main design with a Stage~3 information-integration layer" |
| ch3 | 10 | "presented in two stages" — **bare "two stages"**, but local: refers to Stages 1+2 only inside the chapter sub-structure (Stage 3 introduced separately at L958). Acceptable but slightly weaker. |
| ch3 | 172 | "organized into two stages" — same local pattern (Stage 1 / Stage 2 only). |
| ch5 | — | no fresh "two-stage" claim; uses "Stage 1/2/3" individually. |
| ch6 | — | no "two-stage" wording; describes contributions individually. |

**Verdict: G08 fix is correctly applied at the load-bearing front-matter (abstract, ch1, ch3 §3.2.1).** The two ch3 internal "two stages" mentions (L10, L172) are scope-restricted to the methods sub-organization that genuinely covers only Stages 1–2 (Stage 3 is a separate later section). **Optional polish**: rephrase ch3:10 / ch3:172 as "two main stages" to remove any reader ambiguity. **Severity: Minor.**

---

## C. Contribution Alignment Table

| Component | Ch1 (L141–155) | Abstract (L4–14) | Ch6 (L11–16) |
|---|---|---|---|
| C1 — Benchmark | "MutBench: systematic hotspot-detection benchmark across 11 RNA viruses; 8,580 evaluations" | "broadest region-level, single-position hotspot-detection benchmark; 8,580 evaluations" | "benchmark for viral mutation hotspot detection across 11 RNA viruses, 20 scoring formulas, 39 detectors, 3-layer GT" |
| C2 — Pathogen-dependent optimum | "ω²=0.296; 9 distinct types; LOPO null-consistent" | "ω²=0.296 [0.195,0.333]; Friedman p=0.990; LOPO 0/11" | "ω²=0.296 (20-type) / 0.103 (6-cat); 9 distinct types; oracle-vs-generalized gap 0.265" |
| C3a — 4-feature core | "fixed 4-core indistinguishable from 10-feat under nested-LOPO; paired delta +0.011, p=0.61; H3N2 4.012× p=0.0023" | "paired delta +0.011, CI [-0.018,+0.042]; H3N2 4.012×" | "paired delta +0.011, p=0.61; H3N2 4.012-fold" |
| C3b — HIV-1 anchor | "HIV-1 novel-only 7.16–8.24×, p=5×10⁻¹², Bonferroni 3.9×10⁻⁹; H3N2 self-consistency; SARS-CoV-2 exploratory" | "HIV-1 primary anchor 7.16–8.24× novel-only; H3N2 9.36× self-consistency; SARS-CoV-2 7.63× exploratory" | "HIV-1 7.19× full-set p_adj=2.5×10⁻¹⁶; novel-only 7.16–8.24×; H3N2 self-consistency; SARS-CoV-2 exploratory" |

**Drift assessment**: zero contradictions. Three notes:
1. Ch6 L12 emphasizes the 6-category lower bound 0.103 in the C2 statement; abstract's C2 statement only mentions 0.103 once (L10). Minor asymmetry, no contradiction.
2. Ch6 omits the explicit Bonferroni p_adj=3.9×10⁻⁹ for HIV-1 novel-only — only the full-set 2.5×10⁻¹⁶ and the worst-case 5×10⁻¹² appear. Slight under-statement, not drift.
3. Abstract L13 frames C2 evidence around "9 distinct optimal information types" with a different example list (FUBAR/PLM/homoplasy) than ch1 L146 (same examples). Consistent.

---

## D. ρ Disambiguation Check (G01 fix)

ch5:33 explicitly contrasts:
- **|ρ|=0.12** = per-position membership-vs-frequency point-biserial (circularity audit; range [-0.06, +0.33]).
- **ρ≈0.97** = feature–feature Pearson between *frequency* and *entropy* scoring inputs.

Cross-references in ch4:
- ch4:731 — "entropy and frequency are highly correlated (ρ = 0.97)" → matches ch5 referent (feature-feature).
- ch4:774 — "ρ_freq–entropy = 0.97" — same referent.
- ch4:961 — "both frequency-derived and correlated at ρ ≈ 0.97, Section 7.5" — same referent.

**No occurrence of |ρ|=0.12 outside ch5:33** (it is a unique audit number). G01 disambiguation is internally consistent and correctly anchored. **Severity: clean.**

---

## E. Caveat Consistency 5×5 Grid

| Caveat | Abstract | Ch1 | Ch4 (Results) | Ch5 (Discussion) | Ch6 (Conclusion) |
|---|---|---|---|---|---|
| LOPO 0/11 null-consistent | YES (L10) | YES (L145, L148) | YES (L12, L336, L338, L458, L478–481, L600) | YES (L155, L319, L321) | YES (L13) |
| ω² range (0.103 / 0.296 / 0.39 residual) | YES (L10: full range) | YES (L148: 0.103 lower bound) | YES (L425, L431, L598, L1040) | YES (L70, L93, L279, L281, L290) | YES (L12: 0.296+0.103) |
| Novel-only Bonferroni | PARTIAL (L11: 5×10⁻¹² worst-case stated, no "Bonferroni 3.9e-9") | YES (L150: 5×10⁻¹² + 3.9×10⁻⁹) | YES (L956 footnote: explicit 3.9×10⁻⁹) | PARTIAL (L176: novel-only worst-case noted; explicit 3.9×10⁻⁹ absent) | PARTIAL (L15: 5×10⁻¹² stated; 3.9×10⁻⁹ omitted) |
| HIV-1 single anchor | YES (L11: "HIV-1 is the primary anchor"; L14) | YES (L117 figure, L131 fig caption, L150, L153) | YES (L13, L595 "single-anchor", L961, L991) | YES (L93, L155, L161, L179) | YES (L15, L90) |
| 4-feature paired-test absent (in-sample 97.6% demotion) | YES (L11: paired delta + permutation now headline; 97.6 not used) | YES (L150: explicitly demotes 97.6 to "in-sample only") | YES (L839: explicit demotion) | PARTIAL (L192 still says "retained 97.6%" without protocol caveat in-line; L244 adds "no paired-sample test" but only in resource-constrained workflow) | YES (L14: paired delta primary; no 97.6 used) |

**Two soft gaps**:
1. **Novel-only Bonferroni 3.9×10⁻⁹**: present only in ch1 and ch4 footnote. Abstract / ch5 / ch6 cite 5×10⁻¹² (nominal worst-case) but do not propagate the survival-after-Bonferroni number. Recommend a one-clause add to abstract L11 and ch6 L15.
2. **97.6% protocol caveat in ch5 §6**: ch5:192 retains the "97.6%" wording without an inline reminder that the figure is in-sample (the demotion is performed at ch4:839 and ch1:150, but a reader landing on ch5:192 first would not see it). Recommend rewording ch5:192 to match ch5:244's framing ("numerical retention; no paired-sample test was performed").

Severity: Minor (low risk; no contradiction, only completeness drift).

---

## F. Bibliography ↔ Text Spot Check

10 random body citations → all in `references.bib` (124 entries):
`harvey2021tracking`, `notin2025proteingym_v13`, `cohen1988statistical`, `bolker2009glmm`, `gurev2026everest_v3`, `virogym2026`, `lin2023esm2`, `chicco2020mcc`, `rice1976algorithm`, `cameron2008bootstrap` — **10/10 PRESENT.**

5 random bib entries → all cited in body:
`dadonaite2024nature` (2 files), `aditham2025rabies` (2), `covfit2025` (2), `efron1987better` (1: ch4 region-level BCa), `wolpert1997nfl` (2) — **5/5 CITED.**

Full diff-set comparison (124 bib entries vs every `\cite{...}` key across the 6 files): zero undefined keys, 12 uncited bib entries (e.g., `benjamini1995controlling`, `holm1979sequential`, `nei1986simple`, `zhang2008chipseq`, …) — these appear to be reserved/legacy keys. Not a defect; not blocking.

**Severity: clean.**

---

## G. Recommended Cycle 2 Edits (Priority)

| Pri | Target | Edit | Rationale |
|---|---|---|---|
| P1 | ch5:192 | Rewrite the workflow note to read "...retained ≈98% of the full 10-feature ensemble's mean MCC under the specific uniform-weight LOPO top-10% protocol (numerical retention only; the formal nested-LOPO equivalence test is reported in ch4 Table 4.X)." | Aligns ch5 §6 with the demotion installed at ch1:150 / ch4:839 / abstract; closes the only remaining "97.6%" mention that lacks an inline protocol caveat. |
| P1 | ch6:15, abstract:11 | Add the Bonferroni-adjusted novel-only p_adj ≈ 3.9×10⁻⁹ once each, e.g., "...worst-case Fisher p = 5.0×10⁻¹² (Bonferroni p_adj ≈ 3.9×10⁻⁹ across 780 combinations)". | Propagates G09 fix uniformly to summary venues. |
| P2 | ch3:10, ch3:172 | "two stages" → "two main stages" (or explicit "Stages 1 and 2"). | Remove residual ambiguity vs. the "two-stage main + Stage 3 layer" wording at ch3:7. |
| P2 | ch6 §contrib | Add the 0.265 oracle-vs-generalized gap explicitly as the C2 quantitative anchor (already at ch6:12, but redundancy-tag with "rather than the LOPO 0/11 rate alone"). | Strengthens null-consistency framing parity with ch4:336/L600. |

No P0 cross-chapter defects identified.

---

## H. Severity Summary

| Item | Severity | Status |
|---|---|---|
| Master numerical claims (12 numbers) | — | All consistent |
| Two-stage vocabulary | Minor | G08 effectively applied; ch3 has 2 scope-local "two stages" mentions worth polishing |
| Contribution alignment | — | No drift between ch1/abstract/ch6 |
| ρ disambiguation | — | G01 fix holds; no leak of 0.12 / 0.97 confusion |
| Caveat propagation | Minor | 2 soft gaps: (a) novel-only 3.9×10⁻⁹ missing from abstract/ch5/ch6; (b) ch5:192 keeps "97.6%" without inline protocol caveat |
| Bib ↔ text | — | 10/10 cite→bib, 5/5 bib→cite; 12 uncited reserved entries (non-blocking) |

**Overall**: cycle 2 is in good shape. No P0 cross-chapter defects. Two P1 polish edits (ch5:192 protocol caveat; abstract+ch6 novel-only Bonferroni number) close the last consistency gaps; two P2 cosmetic edits clean residual "two stages" wording.

(~780 words excluding tables.)
