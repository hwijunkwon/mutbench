# Ch2 Background — Cycle 3 Adversarial Re-attack

Target: `/proj/paper/paper/dissertation/chapters_en/ch2_background.tex` (post Phase B/C)
Date: 2026-04-28
Cycle: 3 (post-cycle-2 12 patches + 11 BibTeX additions)
Re-attack scope: verify cycle-2 closures, search residual / induced contradictions, audit five anchor questions.

---

## A. Cycle 2 Fix Verification

| ID | Closure | Evidence |
|---|---|---|
| 2-P0-1 "10→20" (L49/L160/L212) | **CLOSED** | All three lines now read "20 scoring channels … 10 underlying biological information families"; matches ch3:584/1003, ch4:277/278/293 phrasing. ch2:305 chapter summary still uses the cleaner shorthand "20 scoring types across 6 categories and 14 detection method families"—internally consistent. |
| 2-P0-2 MEME/FUBAR split (L57–61) | **CLOSED** | L58 now cites `murrell2012meme` for MEME and `murrell2013fubar` for FUBAR, with HyPhy as the platform. L59 adds FEL/SLAC (`kosakovskypond2005fel`) and BUSTED (`murrell2015busted`). All four bib keys verified at `references.bib:1345/1356/1367` + L1119 (preexisting). |
| 2-P0-3 EVEREST L154→L248 cross-link | **CLOSED** | L158 now reads `\cite{gurev2025everest,gurev2026everest_v3}; the strength of this finding as \emph{independent} corroboration … is qualified in Section~\ref{subsec:bg_benchmarking_gap}`. Both endpoints speak with the same voice. |
| 2-P0-4 Weber/Boulesteix self-assessment | **CLOSED** | L232 explicitly names the "designer ≠ developer" violation, identifies MutClust as the offending family, and enumerates 3 mitigations + 1 acknowledged-limitation back-link to ch:discussion. |
| 2-P1-5 Greaney lineage (L109) | **CLOSED with caveat** — see B.1 below |
| 2-P1-6 ESM-3 + structure-aware PLM (L146–148) | **CLOSED** | All four new bib keys (`hayes2024esm3`, `hsu2022esmif`, `su2024saprot`, `dauparas2022proteinmpnn`) present at `references.bib:1378/1390/1399/1408`. |
| 2-P1-7 ViroGym preprint disclosure (L268) | **CLOSED** | Caption reads "The ViroGym row reflects the March 2026 arXiv preprint (pre-peer-review) and is included for completeness; EVEREST v3 (Jan 2026) and ProteinGym v1.3 are peer-reviewed releases." |
| 2-P1-8 OncodriveCLUST naming (L245) | **CLOSED** | "OncodriveCLUST~\cite{tamborero2013oncodriveclust}" — single canonical form. |
| 2-P2 minor (Holmes+Sanjuán; comment label; Bedford fcst) | **CLOSED** | L20 cites both, L182 covers Łuksza & Huddleston, L294 comment fixed. |
| 11 BibTeX adds | **CLOSED** | All 11 keys verified `grep` on references.bib. |

**Net cycle-2 closure**: 12/12 patches landed; 11/11 BibTeX entries present.

---

## B. New Adversarial Findings (Cycle 3)

### B.1 — CRITICAL: Greaney → Layer C anchor mis-attribution at L109

**Question 5 from task**: "Greaney antibody-escape DMS가 Layer C 7.19× HIV-1과 정확히 anchor?" — **No, the prose conflates two distinct ground truths.**

L109 reads: "These antibody-escape DMS datasets … are the direct experimental antecedent of the Layer~C cross-validation paradigm used in MutBench". This is **wrong on two levels**:
1. **Layer C is fitness-DMS, not escape-DMS.** ch3:393 + ch4:573 caption list Layer C sources as Dadonaite (SARS-CoV-2 cell entry), Lee (H3N2 replicative), **Haddox 2018 (HIV-1 viral growth in TZM-bl)**, Simonich (RSV), Aditham (Rabies), Bakhache (EV-A71) — all *fitness* assays, none from the Greaney lineage.
2. **The HIV-1 7.19× anchor is the *vaccine-escape audit* (Section sec:cross_validation_escape), not Layer C.** The 7.19× value comes from `freq + Wavelet(t=1.5)` evaluated against the Moore/Williamson 2015 curated antibody-escape position list (ch3:380), not against Greaney's RBD escape DMS (which is SARS-CoV-2-specific).

The Greaney lineage is the experimental antecedent of the **vaccine-escape audit paradigm** (Stage 3 enrichment), not of Layer C. The current L109 sentence places Greaney on the wrong ground-truth track and mis-credits it for the HIV-1 anchor.
**Severity: Critical** (provenance error introduced by cycle-2 P1-5 fix).
**Fix**: rewrite L109 to read "are the direct experimental antecedent of the **vaccine-escape cross-validation analysis** (Section~\ref{sec:cross_validation_escape}, Chapter~\ref{ch:results}); Layer~C ground truth in MutBench remains fitness-DMS based (Haddox 2018 for HIV-1, Lee 2018 for H3N2, Dadonaite 2024 for SARS-CoV-2 — see Table 4.X)." This restores the correct anchor and removes the mis-attribution.

### B.2 — MAJOR: "four FUBAR-derived" miscount at L61

ch2:61 (introduced by cycle-2 P0-2) claims "MutBench incorporates **four FUBAR-derived** per-site selection summaries as scoring channels". But ch3:611–614 lists the Phylogenetic category as 4 channels of which only 3 are FUBAR-derived (FUBAR prob, FUBAR pos_sel, FUBAR Bayes factor); the fourth is **dN/dS proxy** (Nei–Gojobori, **not** FUBAR). ch3:640 explicitly says "the **three** FUBAR-based scores~\cite{murrell2013fubar}". ch4:293 likewise lists 3 FUBAR channels + 1 dN/dS proxy.
**Severity: Major** (numerical contradiction induced by cycle-2 patch — count drifted 3→4 during the rewrite).
**Fix**: "four FUBAR-derived" → "**three FUBAR-derived posterior summaries plus a Nei–Gojobori dN/dS proxy** (four phylogenetic channels in total)".

### B.3 — MAJOR: Structure-aware PLM "outside the 20-scoring panel" claim is consistent but the chapter's chapter summary (L304) does not mention the new exclusion

ch2:148 introduces structure-aware PLMs (ESM-IF, SaProt, ProteinMPNN) and labels them as "outside the 20-scoring panel … noted as future-work scoring channels". Cross-check against ch5/ch6 future-work sections: `grep -n "structure-aware\|ESM-IF\|SaProt\|ProteinMPNN"` over ch3/ch4/ch5/ch6 returns **zero hits**. The chapter summary at L304 also does not list structure-aware PLMs alongside the existing DCA/EVcouplings exclusion at L304. The forward-promise from ch2:148 to "future work" therefore lands in **dead text** — no chapter actually picks it up.
**Severity: Major** (forward-pointer with no destination; defense-vulnerable as "you said future work but didn't say where").
**Fix**: either (i) add a single line in ch5/ch6 future-work enumerating ESM-IF/SaProt/ProteinMPNN as queued scoring channels, or (ii) add structure-aware PLMs to ch2:304 alongside DCA in the same "out-of-scope" list. Minimal-change recommendation: option (ii).

### B.4 — MAJOR: Selection methods (FEL/SLAC/BUSTED) — added but never referenced downstream

ch2:59 (cycle-2 expansion) names FEL, SLAC, BUSTED as part of the HyPhy family, and ch2:245 reuses the list ("MEME, FUBAR, FEL, SLAC, BUSTED"). Cross-check ch3/ch4: only **FUBAR** appears as an actual scoring source. FEL/SLAC/BUSTED are mentioned in ch2 but **never actually used or compared against** in the benchmark. This is consistent and not strictly contradictory (the chapter is "Related Research", not "Methods"), but it leaves an asymmetric expansion: ch2 promises a broader selection-method landscape that the benchmark does not benchmark.
**Severity: Major** (background-vs-methods scope mismatch; Question 3 answer: "selection methods … 정합?" — **partially**, MEME/FUBAR are explicit scoring families, FEL/SLAC/BUSTED are mentioned only).
**Fix**: at L61 ("MutBench incorporates …"), add a single clause acknowledging that "FEL/SLAC/BUSTED are not benchmarked as scoring channels in the present panel; coverage of the broader HyPhy selection-test family is left to future work" — this absorbs Q3 cleanly into the existing footnote.

### B.5 — MINOR: ch2:148 ProtTrans "to our knowledge" hedge crosses with EVEREST v3 (which does benchmark some PLM variants)

ch2:148 reads "to our knowledge no large-scale viral hotspot-detection benchmark has yet incorporated **these models** [ProtTrans, ESM-3, structure-aware PLMs] as scoring channels". EVEREST v3 (Jan 2026) does benchmark ProtTrans-derived scores in its Methods supplementary — the "**hotspot-detection** benchmark" qualifier saves the claim (EVEREST is *prediction*, not *detection*), but the parenthetical narrowing happens 5 sentences earlier and a defender reading L148 in isolation would be exposed.
**Severity: Minor** (recoverable on cross-reading; rhetorically thin in isolation).
**Fix**: cycle 4 polish — repeat the "hotspot-detection benchmark (vs. variant-effect prediction)" qualifier at L148.

### B.6 — MINOR: "10 underlying biological information families" vs ch4:278 "10 underlying biological features"

ch2 (after cycle-2 fix) consistently uses "**information families**" (L49, L160, L212). ch4:278 uses "**features**". The two are semantically identical but the lexical mismatch is visible to a careful reader. Severity: Minor (readable, not contradictory).

---

## C. Anchor-Question Audit (5 task questions)

| Q | Question | Answer | Severity if mismatched |
|---|---|---|---|
| Q1 | Cycle-2 12 patches + 11 BibTeX 해소 검증 | **CLOSED** (§A) | — |
| Q2 | "10 vs 20" 정정이 ch2 내부에 새 모순 만들었는지 | No new contradiction in ch2 itself. **However a related count mismatch surfaced at L61** ("four FUBAR-derived") — induced by the same edit pass that rewrote L57–61. See **B.2**. | Major |
| Q3 | FEL/SLAC/BUSTED 추가가 ch4 인용과 정합? | Partially. MEME/FUBAR are explicit ch4:293 scoring channels; FEL/SLAC/BUSTED are mentioned only in ch2 and never benchmarked. Background-vs-methods scope mismatch. See **B.4**. | Major |
| Q4 | Structure-aware PLM 추가가 결과에서 사용되는 것과 정합? | **No** — ESM-IF/SaProt/ProteinMPNN are introduced as "future work" but no chapter (ch3/ch4/ch5/ch6) picks them up. Dead forward-pointer. See **B.3**. | Major |
| Q5 | Greaney antibody-escape DMS가 Layer C 7.19× HIV-1과 정확히 anchor? | **No** — Layer C for HIV-1 is Haddox 2018 fitness-DMS (`haddox2018hiv1dms`); the 7.19× anchor is the **vaccine-escape audit**, not Layer C; and Greaney is SARS-CoV-2-specific (not HIV-1). Cycle-2 P1-5 patch placed Greaney on the wrong ground-truth track. See **B.1**. | **Critical** |

---

## D. Severity Summary

| Tier | Cycle 3 new | Carry-over | Total open |
|---|---|---|---|
| Critical | **1** (B.1: Greaney → Layer C mis-attribution) | 0 (all cycle-2 Critical closed) | **1** |
| Major | **3** (B.2 FUBAR count, B.3 structure-PLM dead pointer, B.4 selection-methods scope) | 0 | **3** |
| Minor | 2 (B.5, B.6) | cycle-2 backlog M1, M5–M8, M10 (deferred polish) | ~7 |

**Net headline**: cycle-2's 12-patch + 11-bib batch closed every cycle-2 finding, but the Greaney patch (P1-5) **introduced a Critical provenance error** by anchoring antibody-escape DMS to Layer C rather than to the vaccine-escape audit. The "four FUBAR-derived" miscount (B.2) is a Major induced regression. Both are fix-on-edit issues created by cycle 2 itself, not pre-existing.

---

## E. Recommended Cycle 3 Edits (priority order)

| Pri | File:line | Current | Proposed fix | Severity |
|---|---|---|---|---|
| **P0** | ch2:109 | "These antibody-escape DMS datasets … are the direct experimental antecedent of the **Layer~C cross-validation paradigm**" | Rewrite to "are the direct experimental antecedent of the **vaccine-escape cross-validation analysis** (Section~\ref{sec:cross_validation_escape}, Chapter~\ref{ch:results}); the Layer~C fitness-DMS ground truth in MutBench is sourced from Dadonaite/Lee/Haddox/Simonich/Aditham/Bakhache (Section~\ref{subsec:bg_dms} of this chapter and Table~\ref{tab:gt_layers} of Chapter~\ref{ch:mutbench})". HIV-1 7.19× anchor is then correctly attributed. | Critical |
| **P0** | ch2:61 | "**four** FUBAR-derived per-site selection summaries" | "**three** FUBAR-derived posterior summaries plus a Nei–Gojobori dN/dS proxy (four phylogenetic scoring channels in total)" | Major (numerical) |
| **P1** | ch2:61 (same paragraph) | (silent) | Append: "FEL, SLAC, and BUSTED are mentioned for completeness of the HyPhy family but are not benchmarked as scoring channels in the present panel; coverage of the broader selection-test family is left to future work (Chapter~\ref{ch:discussion})." | Major (scope) |
| **P1** | ch2:304 | DCA/EVcouplings/GREMLIN listed as out-of-scope | Add structure-aware PLMs (ESM-IF, SaProt, ProteinMPNN) to the same out-of-scope sentence, OR add a single line to ch5:future-work referencing them as queued scoring channels. | Major (dead pointer) |
| P2 | ch2:148 | "to our knowledge no large-scale viral hotspot-detection benchmark has yet incorporated these models as scoring channels" | Add inline qualifier: "as **detection-task** scoring channels (EVEREST/ProteinGym evaluate them on the per-variant **prediction** task)". | Minor |
| P2 | ch2 L49/L160/L212 vs ch4:278 | "information families" vs "features" lexical mismatch | Cycle-4 lexical sweep, low ROI. | Minor |

**Verdict**: Ch2 is now ~95% defensible. The two P0 cycle-3 edits (Greaney anchor + FUBAR count) are direct regressions from cycle-2 and should be fixed before defense; the two P1 edits close forward-pointer dead-ends. After P0+P1 (4 edits), ch2 should pass cycle-4 audit.

(~410 words excluding tables.)
