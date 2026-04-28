# Cycle 2 Adversarial Review — Ch5 Discussion

Target: `/proj/paper/paper/dissertation/chapters_en/ch5_discussion.tex` (336 lines)
Date: 2026-04-28 / Cycle 2 (post P0)

---

## A. Cycle 1 P0 fix verification at ch5:33

**Verdict: VERIFIED, but partially.** L33 now contains an explicit one-sentence disambiguation between (i) the per-position point-biserial $|\rho|=0.12$ (Layer A membership vs frequency) and (ii) the feature-feature Pearson $\rho \approx 0.97$ (frequency vs entropy *inputs*), with the cross-reference to `sec:information_analysis`. The conceptual distinction ("circularity between GT and signal" vs "redundancy among inputs") is now stated. **Residual gap**: the ρ=0.97 reference still points only to Section information_analysis; the *exact location in Ch4* (L696/L739) is not pinned by `\ref`/page anchor, so a reader scanning Ch4 may still confuse the two values. Severity: Minor (acceptable, but a more specific cross-ref would be ideal).

---

## B. Cycle 1 7-Critical resolution status

| Cycle1 ID | Issue | Status | Evidence |
|-----------|-------|--------|----------|
| C1 | ρ=0.12 vs ρ=0.97 disambiguation | **RESOLVED** | L33 long sentence added |
| C2 | HCV/Influenza-B/Norovirus circularity → ranking discount | **PARTIAL** | L34 acknowledges "partly structural", but the *implication for HCV-best=frequency ranking* is not propagated to Tables. Reader still sees HCV "best=freq" without inline discount tag |
| C3 | NFL "stronger evidence than abstract theorem alone" | **RESOLVED** | L84 reworded to "complementary practical evidence within a biologically meaningful problem class…NFL itself remains a statement about all possible problem distributions and is neither tested nor strengthened by 11 cases" |
| C4 | Independent reproduction discount mapping | **PARTIAL** | L287 still 1 sentence. No claim-by-claim discount table (which numbers are single-team-single-snapshot estimates: ω², oracle MCC, escape enrichment) |
| C5 | 11-cluster Bolker rule explicit | **PARTIAL** | L285 cites Bolker, L321 mentions caution; explicit "11 meets the minimum (5–6) but is below the recommended (≥20–30)" still missing |
| C6 | 97.6%/98% retention consistency | **RESOLVED** | L162, L196, L244 all carry the "numerical only / no paired test" caveat after P0 |
| C7 | Circularity ↔ Layer-A heterogeneity logical chain | **PARTIAL** | L33 mentions "ground-truth curation style", but no explicit `\ref{sec:gt_heterogeneity}` linking circularity to definition heterogeneity at L33 |

**Score: 3 fully resolved / 4 partial / 0 unresolved.** Cycle 2 P0 candidates: C2 propagation, C4 mapping, C5 explicit Bolker, C7 cross-ref.

---

## C. New adversarial findings

### Critical (cycle 2)

| # | Loc | Issue |
|---|-----|-------|
| **N-C1** | L162, L164 | "10-feature EqualWeight" and "4-feature core" both claim ≈98% retention without distinguishing that the 4-feature retention (97.6%) was measured against the *10-feature* ensemble, not against an oracle. The clinical reader sees "98% retention" as an absolute floor, not a relative-to-10-feature floor. **No paired test, no CI, no oracle gap.** |
| **N-C2** | L84 | After C3 fix, the Rice algorithm-selection framing remains. But Rice's framework requires a *meta-learner* mapping problem features → algorithm; LOPO 0/11 demonstrates the meta-learner does **not** exist for this dataset. Citing Rice while reporting a null meta-learner is borderline self-contradictory unless explicitly framed as "Rice formalism applies; the empirical mapping is not yet learnable from 11 pathogens". |
| **N-C3** | L77–93 | Forward-looking claim leak: L79 "applying a previously optimized combination to a new pathogen may not generalize" (defensible) coexists with L84 "stronger practical evidence for pathogen-adaptive selection" — but no validated pathogen-adaptive *selector* is shown. The chapter implies adaptive selection is achievable while LOPO+Friedman+0.265 gap evidence shows it is not yet learnable. |

### Major (cycle 2)

| # | Loc | Issue |
|---|-----|-------|
| **N-M1** | L194–203 (PAHD-R) | Cycle 1 M7 flagged this as "new system in Discussion = anti-pattern". Status: still in Ch5 with no `\ref` to a Results section. Either Ch4 defines PAHD-R modes (verify) or this paragraph belongs in Ch6. |
| **N-M2** | L271–277 | ESM-2 leakage "uniform across pathogens" assumption still un-quantified (cycle1 M10). Cycle 2 finds an additional asymmetry: **Tranception is also UniRef-trained**, and L93/L277 treat Tranception and ESM-2 as if independent channels even though the cycle-1 phase4 TOP-3 risk identifies them as plausibly redundant. No per-pathogen ρ(Tranception, ESM-LLR) reported in Ch5. |
| **N-M3** | L266–268 | Time-forward validation is described as a "future direction" in 1 sentence. Phase 4 professor 8 (역학 실무자, 6.8) flagged this as one of TOP-3 risks. Ch5 does not contain a single prospective sanity check (e.g., 2010-cutoff H3N2 holdout). |
| **N-M4** | L155 | Contribution recap omits the saturation caveat (Section hscore_saturation, L46–48) — the same Contribution 1 (hotspot-score metric) is acknowledged elsewhere as saturating in 2024–2025 data. Logical inconsistency within the chapter. |
| **N-M5** | L161–162 | Stage-2 single-feature 7.19× (winner-curse-prone) and integration 4.012× (winner-curse-free) are juxtaposed without telling the reader that the smaller integration number is *more reliable*, not weaker. Risk of misreading "integration is worse than single feature". |
| **N-M6** | L319 (Friedman p=0.990) | "p=0.990 indicating no method reliably distinguishable" can be misread as strong evidence FOR null. Should clarify Friedman is *uninformative* under the rank-block design with n=11, not a confirmation. |

### Minor (cycle 2)

| # | Loc | Issue |
|---|-----|-------|
| **N-m1** | L17 | "expand by including ORF1ab, N protein" — still no target sample size or CI half-width gain. |
| **N-m2** | L48 vs L190 | "appropriate temporal resolution remains future challenge" (L48) still inconsistent with L190 "minimum 4-week window required". |
| **N-m3** | L267 | "feature discriminative power changes substantially" — "substantially" still un-quantified despite cycle 1 m10 flag. |
| **N-m4** | L315–323 (Scope) | MAFFT --auto mode artifact concern not raised; only "input quality varies" wraps it. Phase 1 blueteam noted this as residual risk. |
| **N-m5** | L292 | n=4 phylo-only ω²=0.137 still has no CI half-width; cycle 1 m12 flag still unaddressed. |

---

## D. Limitation honesty table

| Limitation | Discussed? | Location | Gap level |
|-----------|------------|----------|-----------|
| Prospective/time-forward validation absence | NO (only post-hoc temporal AUC change) | L266–268 | **Critical gap** |
| 11 RNA virus single-position regime restriction | Partial | L315–319 | Medium — "single-position" qualifier missing in headline |
| Tranception–ESM-LLR proxy collinearity | NO | (absent) | **Critical gap** (phase4 TOP-1 risk) |
| 4-feature 97.6% paired-test absence | YES | L162, L196, L244 | Resolved |
| HIV-1 single anchor for 7.19× | Partial | L179, L184 | Medium — "single anchor" framed as "primary" not as "vulnerability" |
| Structure source per-pathogen variability | Partial | L295, L329 | Medium — no per-pathogen mapping |
| MAFFT --auto mode artifact possibility | NO | (absent) | **Major gap** |
| External independent reproduction | Partial (1 sentence) | L287 | Major gap (no claim-by-claim discount) |
| Layer A definitional heterogeneity | YES (full subsection) | L300–308 | Resolved |
| ESM-2 viral leakage | Partial | L271–277 | Medium — "uniform" assumption unverified |
| Winner's curse | YES (with mitigation) | L283 | Resolved |
| Bolker n≥5–6 vs ≥20–30 | Partial | L285 | Medium |

---

## E. Forward-looking claim audit

| Loc | Claim | Evidence | Verdict |
|-----|-------|----------|---------|
| L84 | "stronger practical evidence for pathogen-adaptive selection" (post-C3 fix wording: "complementary practical evidence within a problem class") | LOPO 0/11, Friedman p=0.990, gap 0.265 (all null/weak) | **Now defensible** after cycle 1 fix |
| L82 | "the choice of input information matters far more than the choice of detection algorithm" | $\omega^2_{scoring} \gg \omega^2_{family}$ (modeled main effects only) | Defensible — already caveat'd at L279 |
| L155 | Contribution 1 = "standardised evaluation framework provided by 3-layer GT and hotspot-score metric" | Saturation at L46–48 contradicts unqualified "standardised" | **Overclaims — N-M4** |
| L162 | "achieves 4.012× H3N2 escape enrichment without requiring pathogen-specific optimization" | Single-pathogen demonstration | Borderline — extrapolates from 1 pathogen to "without optimization" |
| L84 | "consistent with the No Free Lunch theorem" | NFL is universal, claim is empirical | Defensible after C3 fix |
| L192 | "This workflow integrates with existing surveillance platforms such as Nextstrain and GISAID" | No deployment instance shown | **Forward-looking — needs "is designed to integrate" softening** |
| L268 | "Standardizing the analysis time window … is an important future direction" | Honest future-work framing | OK |

---

## F. Recommended cycle 2 edits

| Sev | File:line | Current → Proposed |
|-----|----------|--------------------|
| **C** | ch5:155 | "the standardised evaluation framework is provided by the three-layer ground truth and hotspot-score metric" → add "(with the saturation caveat in Section~\ref{sec:hscore_saturation})" |
| **C** | ch5:84 | After Rice citation, add: "though the empirical mapping $f$ is not yet learnable from this 11-pathogen panel (LOPO 0/11; Section~\ref{sec:cross_pathogen_implications})." |
| **C** | ch5:162, ch5:164 | "the 4-feature core (homoplasy, pLDDT, entropy, frequency) retained 97.6% of the full 10-feature ensemble's mean MCC" → add "*relative to the 10-feature ensemble, not relative to an oracle*; no paired-sample significance test, see Section~\ref{sec:practical_workflow}" |
| **C** | ch5:271–277 (new sentence) | After "ESM-2 was trained on UniRef…", add: "Tranception (Notin 2022) was also trained on UniRef variants; per-pathogen ρ(Tranception, ESM-LLR) is not reported in this work, so the SARS-CoV-2 best=Tranception result should be interpreted with channel-redundancy uncertainty." |
| **C** | ch5:266–268 (new sentence) | Add: "No prospective time-forward validation has been conducted; all reported enrichments and MCC values are retrospective on a 2024-12 GenBank snapshot. A pilot 2010-cutoff H3N2 holdout is queued (Section~\ref{ch:conclusion})." |
| **M** | ch5:194–203 (PAHD-R) | If `\label{...}` for PAHD-R modes does not exist in Ch4, move this paragraph to Ch6 §future_work; otherwise add `\ref{}` to the Ch4 definition |
| **M** | ch5:319 | "$p = 0.990$, indicating that no single method can be reliably distinguished" → "$p = 0.990$; under the Friedman rank-block design with $n = 11$ blocks the test is uninformative rather than confirming a null, and pathogen-specific optimality remains the more parsimonious interpretation given the ANOVA interaction and oracle-vs-generalized gap" |
| **M** | ch5:287 (independent reproduction) | Expand to: "Specifically, the headline interaction ($\omega^2 = 0.296$), oracle MCC means (0.341), and HIV-1 7.19× enrichment are single-team-single-snapshot estimates; relative orderings are more robust than absolute magnitudes." |
| **M** | ch5:34 (HCV/Influenza-B/Norovirus circularity) | Append: "Implication: HCV's freq-best ranking and Norovirus's epochal-Layer-A coupling should be read as partly structural; per-pathogen rankings in Tables~\ref{tab:stage2_best} carry this discount implicitly." |
| **M** | ch5:285 | Append: "11 pathogens meets Bolker et al.'s minimum ($\geq$5–6) for fixed-effect ANOVA blocks but is below the typical recommendation ($\geq$20–30) for stable random-effects estimation." |
| **m** | ch5:33 (cross-ref) | Append `\ref{sec:gt_heterogeneity}` after "ground-truth curation style" |
| **m** | ch5:48 | "appropriate temporal resolution remains a future challenge" → "appropriate temporal resolution beyond the 4-week minimum (Section~\ref{sec:practical_surveillance}) remains a future challenge" |
| **m** | ch5:325–328 | "consistent with MutBench's central finding" → "as a parallel observation, not as confirmation, of the pathogen-dependent information principle" |
| **m** | ch5:319 (scope) | Add MAFFT --auto sentence: "MSA construction used MAFFT --auto across all pathogens; per-pathogen mode (FFT-NS-2 / L-INS-i) was not held constant, which may contribute marginally to the input-quality component of the interaction." |

---

## G. Severity summary

| Tier | Cycle 1 status | Cycle 2 new | Total open |
|------|----------------|-------------|-----------|
| Critical | 3 of 7 resolved, 4 partial | 3 (N-C1, N-C2, N-C3) | **7 open** |
| Major | (cycle 1 majors largely partial) | 6 (N-M1..N-M6) | ~10 open |
| Minor | (cycle 1 minors largely open) | 5 (N-m1..N-m5) | ~12 open |

**Verdict: CONDITIONAL PASS at cycle 2.** Cycle 1 P0 G01 is verified. Cycle 1 7-Critical resolution is 3 fully + 4 partial — the partial set requires 4 small text edits to close. The 3 new cycle-2 Critical findings (relative-to-10feature framing of 97.6%, Rice formalism without learnable mapping, Tranception/ESM-2 channel redundancy in limitations) are all addressable by single-paragraph additions; none requires re-experiment. Phase 4 G (실용적 6.7) and C (방법론 6.9) lift will come from N-M3 (prospective pilot), N-M2 (Tranception ρ), and the L155 saturation caveat.

Total substantive issues: **C1 partials (4) + N-C (3) + N-M (6) = 13 substantive findings**, exceeding the 7-issue floor.

---

Reviewer: Claude (cycle 2 codex-style adversarial agent)
Stored: `/proj/paper/paper/dissertation/review/2026-04-28/cycle2/ch5_review.md`
