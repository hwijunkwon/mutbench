# Cycle 3 Adversarial Re-Attack — Ch5 Discussion

Target: `/proj/paper/paper/dissertation/chapters_en/ch5_discussion.tex` (352 lines, +16 vs cycle 2 baseline 336)
Date: 2026-04-28 / Cycle 3 / Phase B (post-14-fix)
Reviewer: Claude (cycle 3 codex-style adversarial agent)

---

## A. Phase B 14-fix retention verification

| Cycle 2 ID | Target item | Loc (post-fix) | Verdict |
|------------|-------------|---------------|---------|
| N-C1 | 97.6% retention "relative to 10-feature ensemble" + no paired test | L164 (in-line), L192 (workflow), L244 (computational) | **HELD-FULL.** L164 contains the exact qualifier "relative-to-ensemble retention figure within the same protocol, not an absolute floor relative to an oracle, and no paired-sample significance test was performed". Clinical-misread risk neutralised. |
| N-C2 | Rice algorithm-selection self-contradiction | L84 | **HELD-FULL.** The exact phrase "We therefore frame Rice as a *theoretical scaffold* for the algorithm-selection problem in our setting, not as an empirical guide" is present, paired with explicit LOPO 0/11 / Friedman / 0.265 gap citations as joint null-consistent evidence. |
| N-C3a | "is standardised" forward-looking weakening | L155 | **HELD-FULL.** Now "is *designed for standardised use, pending external benchmarking* by independent teams (with the saturation caveat in Section~\ref{sec:hscore_saturation})". Saturation cross-ref inline. |
| N-C3b | "integrates with Nextstrain/GISAID" weakening | L192 | **HELD-FULL.** Now "*is designed to integrate* with ... via their public APIs ... integration testing remains future work, and no production-grade integration is claimed". |
| N-M2 (Tranception/ESM) | Per-pathogen ρ values | L279 (new bold paragraph) | **HELD-FULL with exact numbers.** Pearson 0.64–0.84 / Spearman 0.71–0.98 for 11/12 pathogens; HIV-1 dissociates (Pearson 0.04, n.s.). Located inside `sec:esm2_leakage` immediately after the leakage uniformity self-critique. |
| N-M3 (prospective gap) | New `\subsection{...sec:prospective_validation_gap}` | L337–342 | **HELD-FULL.** Two-paragraph subsection: "no *prospective*, time-forward validation has been conducted"; sliding-window explicitly distinguished from forward prediction; 2010-cutoff H3N2 pilot disclosed as queued, not part of dissertation. |
| MAFFT --auto | New `\subsection{...sec:mafft_auto_artifact}` | L344–347 | **HELD-FULL.** Confound with pathogen factor admitted; one-mode-for-all sensitivity not run; "small magnitude is hypothesis, not quantified bound". |
| C2 partial→full (HCV/Norovirus discount propagation) | L34 *Implication for per-pathogen rankings* sentence | L34 | **HELD-FULL.** Discount tagged onto Stage~2 rankings via Table~\ref{tab:stage2_best}. |
| C4 partial→full (independent-reproduction claim-by-claim) | L291 expanded | L291 | **HELD-FULL.** Maps ω²=0.296 evaluation / 0.234 cell / mean oracle 0.341 / HIV-1 7.19× / p_adj=2.5e−16 to single-team-single-snapshot label; relative-vs-absolute robustness rule stated. |
| C5 partial→full (Bolker explicit 5–6 vs 20–30) | L289 | L289 | **HELD-FULL.** "11-pathogen panel meets Bolker's minimum but is materially below the typical recommendation"; wild-cluster bootstrap (Cameron 2008) recommended. |
| C7 partial→full (circularity↔heterogeneity logical chain) | L34 trailing sentence | L34 | **HELD-FULL.** Chain explicit: "downstream consequence of the Layer~A curation heterogeneity discussed in Section~\ref{sec:gt_heterogeneity}". |
| G01 cross-ref pinning | ch5:33 | L33 | **HELD-FULL.** `Chapter~\ref{ch:results} Section~\ref{subsec:feature_correlation}` resolves; `subsec:feature_correlation` exists at `ch4_results.tex:765`. |
| Friedman uninformative (M-7) | L323 | L323 | **HELD-FULL.** "uninformative under rank-block design with $n=11$ ... null-consistent corroboration, not ... independent confirmation" present verbatim. |
| 7.19× vs 4.012× framing (M-11) | L162 | L162 | **HELD-FULL.** Winner's-curse-prone vs winner's-curse-free distinction explicit; "smaller integration number is therefore *more reliable* ... not weaker". |

**Retention rate: 14/14 (100%).** No regressions, no over-weakening, no broken cross-refs detected.

---

## B. Adversarial probes (cycle 3)

1. **Label-collision probe.** New labels `sec:prospective_validation_gap` (L338) and `sec:mafft_auto_artifact` (L345) are unique within `chapters_en/`; no duplicate definitions found. **PASS.**
2. **Build-success probe.** `thesis_en.pdf` exists (134 pp, regenerated). The three remaining build errors are pre-existing in `ch4_results.tex:483` (`\texttt{omega_loo_pathogen.csv}` underscore in `\texttt{}` — needs `\_`); these are **not introduced by ch5 cycle 2 fixes**. **PASS.**
3. **Conclusion-weakening probe.** Limitation additions (L279 Tranception, L289 Bolker, L291 reproduction, L337 prospective, L344 MAFFT) sum to ≈30 lines of caveat text. The "Optimality ceiling vs robust default floor" paragraph (L194–197) and PAHD-R bounded-synthesis paragraph (L199–203) act as positive counterweights, retaining the three-contribution scaffold (L155). Balance is intact: critical claims (ω²=0.296, HIV-1 7.19×, 4-feature 97.6%) survive but each carries an in-line discount. **No anti-balance.**
4. **"Non-rejection of inferiority" location probe.** The exact phrase "non-rejection of the inferiority hypothesis" appears at `ch1_introduction.tex:152` only; ch5 cites the same nested-LOPO numbers (paired Δ +0.011, 95% CI [−0.018, +0.042], p=0.61) at L192 but uses "numerical retention only ... formal nested-LOPO non-inferiority result ... is reported in Chapter~\ref{ch:results} Table~\ref{tab:nested_lopo_4core}". **Cross-chapter wording is consistent but ch5 itself defers the formal NI vocabulary to ch1/ch4 — acceptable.**
5. **PAHD-R definition anchor probe.** `ch6:16` cross-refs Chapter~\ref{ch:discussion}. ch5 contains a paragraph-level use at L199–203 ("three global modes: Core ... Augmented ... Review") and at L155-onward as bounded synthesis. The full algorithmic definition lives at `ch4_results.tex:1012-1023` (PAHD-R redesign audit). **ch5 functions as the *interpretive* anchor; the *definitional* anchor remains in ch4 as expected.** N-M1 is therefore NOT a content gap — it is a cross-ref hygiene item only.

---

## C. Residual / new-cycle findings

| Sev | Loc | Issue |
|-----|-----|-------|
| Minor | ch5:199–203 (PAHD-R) | No `\ref{}` to `ch4_results.tex:1012` PAHD-R-redesign-audit paragraph from L199. A reader entering ch5 from the abstract sees the three-mode synopsis with no anchor back to the ch4 definition. **Recommendation:** add `(see Chapter~\ref{ch:results}, PAHD-R redesign audit)` at L199. |
| Minor | ch5:48 | "appropriate temporal resolution remains a future challenge" still un-pinned to `sec:practical_surveillance` 4-week minimum — cycle 2 m-13 ack'd-but-not-applied. |
| Minor | ch5:325-328 | "consistent with MutBench's central finding" tone vs CoVFit — cycle 2 m-14 ack'd-but-not-applied. |
| Minor | ch5:17 | ORF1ab/N-protein expansion sentence still no target sample size or CI half-width — cycle 2 m-1 not applied. |
| Minor | ch5:267 | "feature discriminative power changes substantially" — "substantially" still un-quantified despite multi-cycle flag. (10-fold entropy rise IS quantified at L267 same sentence — re-reading: actually quantified inline. Downgrade to **already-resolved**.) |

---

## D. Severity comparison cycle2→cycle3

| Tier | Cycle 2 open (pre-fix) | Cycle 3 (post-fix re-attack) |
|------|------------------------|------------------------------|
| Critical | 7 (4 partial + 3 new) | **0** |
| Major | ~10 | **1** (PAHD-R cross-ref to ch4:1012; cosmetic only) |
| Minor | ~12 | **3** (m-1 ORF1ab CI, m-13 4-week pin, m-14 CoVFit tone) |

Net delta: −7 Critical, −9 Major, −9 Minor. Total open ≈4 substantive (1 cosmetic Major + 3 Minor polish).

---

## E. Verdict

**PASS for ch5 at cycle 3.** All 14 cycle 2 fixes held with full verbatim retention; clinical-misread risk on 97.6% (N-C1), Rice self-contradiction (N-C2), forward-looking leak (N-C3a/b), Tranception/ESM channel-redundancy (N-M2), prospective-validation absence (N-M3), and MAFFT --auto confound are all neutralised. Two new dedicated limitation subsections (`sec:prospective_validation_gap`, `sec:mafft_auto_artifact`) integrate cleanly with no label collision; build status unchanged (the three pre-existing ch4:483 underscore errors are out-of-scope). PAHD-R is interpretively anchored at ch5:199–203 with definition deferred to ch4:1012, satisfying the ch6:16 cross-ref chain. Conclusion balance retained: positive scaffold (L155 three contributions, L194 ceiling-vs-floor, L199 PAHD-R) and limitation scaffold (L279/L289/L291/L337/L344) are weighted symmetrically. The remaining 3 Minor polish items (m-1, m-13, m-14) are P2-tier cycle-3 polish — not blocking.

Recommendation: proceed to cycle 3 cross-chapter probe; ch5 individually requires no further P0/P1 action.

---

Stored: `/proj/paper/paper/dissertation/review/2026-04-28/cycle3/ch5_re_attack.md`
