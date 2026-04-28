# Ch1 Cycle 2 Review (codex + adversarial)

Source files inspected: `chapters_en/ch1_introduction.tex` (172 L), `front_en/abstract.tex`,
`chapters_en/ch4_results.tex` (lines 392, 462, 837, 956, 991, 1031, 1041), cycle 1
`summary.md`, `phase2b_ch1.md`, `phase3_ccb.md`, `phase5_codex_deep_review.md`.

## A. Cycle 1 P0 fix verification

- **G08 (two-stage → "two-stage main + Stage 3 layer")**: PARTIAL PASS.
  ch1:82 and ch1:143 now read "two-stage main experimental design with a Stage~3
  information-integration layer" — clean. BUT (i) ch1:41 still calls the bench-side
  workflow a "three-stage process" (sequence collection / computational / experimental)
  using the same Stage 1/2/3 vocabulary as the experimental design — collision with the
  fix; cycle 1 m2 flagged this and it was not addressed. (ii) TikZ subbox at ch1:111 still
  reads "2-Stage + Integration", not "2-Stage main + Stage 3 layer" — visual inconsistency
  with the prose patch.
- **G09 (novel-only Bonferroni 3.9e-9 origin)**: PASS. Now derived in
  ch4:956 ("$5.0 \times 10^{-12} \times 780 \approx 3.9 \times 10^{-9}$").
- **G10 (7.19× double-meaning at ch1:153)**: PASS. H3N2 novel 7.19× is now explicitly
  scoped to "9 novel positions" and HIV-1 full 7.19× is named.
- **G14a/b/c (figure caption fixes)**: out of Ch1 scope; not re-verified here.
- **G02b (Friedman/LOPO split)**: ch1:148 reads cleanly; PASS for Ch1.
- **G01 (ρ disambiguation)**: NOT applied to Ch1 directly. Ch1 contains no ρ value, so
  no patch was needed; however the abstract and Ch1 share scope and a single sentence
  "feature-feature ρ ≠ ground-truth ρ" is still absent from the introduction-level reader
  view. Low priority for Ch1 (kept at P2).

## B. New adversarial findings

### Critical
- **[C-01] ch1:82 vs ch1:150 — 11 vs 12 pathogen conflict (cycle 1 P1 G24 still open).**
  L82 Objective 1: "Stage~3 for multi-source feature integration with information-type
  analysis across all 11 pathogens"; L150 Contribution 3a: "nested-LOPO on the
  12-pathogen Stage~3 panel". Same chapter, opposite counts. Ch4:837 confirms the
  nested-LOPO is on 12 (Zika added). This was logged in cycle 1 as M8/G24 P1 and never
  fixed — escalate to P0 for Ch1 internal consistency. Fix at L82: "across the
  11-pathogen panel (extended to 12 with Zika for the feature-ablation/nested-LOPO
  analysis; see Section~\\ref{subsec:feature_ablation})".

- **[C-02] ch1:152 — "operationally equivalent" overclaim under wide non-inferiority CI.**
  Paired delta CI is $[-0.018, +0.042]$ MCC, p=0.61. This excludes inferiority larger
  than 0.018 MCC and superiority larger than 0.042 — a non-inferiority margin of about
  half of the LOPO mean MCC (0.081). Calling this "operationally equivalent to the full
  10-feature ensemble" promotes a non-rejection of $H_0$ to an equivalence claim without
  a pre-specified equivalence margin. Codex IV&V P5-01 (SERIOUS) already flags an
  upstream protocol mismatch on the same claim; Ch1 wording compounds it.
  Fix: "statistically indistinguishable from the full 10-feature ensemble within a
  $\\pm$0.04 MCC bound under nested-LOPO" and drop "operationally equivalent" here
  (also at L143 if present).

### Major
- **[M-01] ch1:117 (TikZ) — full-set 7.19× listed first contradicts "primary anchor =
  novel-only" framing.** TikZ subbox reads "HIV-1 vaccine-escape enrichment (full set
  7.19$\\times$; novel-only 7.16--8.24$\\times$)". Caption at L131 (cycle-1-corrected) and
  abstract:11 frame novel-only as the primary anchor. The figure body still leads with
  full-set. Reorder: "novel-only 7.16--8.24$\\times$ (37 Layer-A-disjoint positions);
  full-set 7.19$\\times$ shown for completeness". Cycle 1 M6 raised this; not patched.

- **[M-02] ch1:41 "three-stage process" lexical collision with Stage 1/2/3 design.**
  L41-50 introduces the bench-side workflow as Stage 1 sequence collection / Stage 2
  computational analysis / Stage 3 experimental validation, then L82/143 redefine
  Stage~1/2/3 as the experimental-design phases (SARS-CoV-2 / cross-pathogen /
  integration). A reader who only sees Ch1 cannot tell which "Stage~3" L150 refers to.
  Fix: rename L41 workflow to "three-step pipeline" with steps "(i) sequence collection,
  (ii) computational analysis, (iii) experimental validation" and stop using the word
  Stage in §1.1. Cycle 1 m2 (Minor) — escalate to Major because cycle-1 G08 fix
  introduced "Stage~3" prose in §1.3/§1.4, raising the collision risk.

- **[M-03] Objectives ↔ Contributions still 1:1 mapping with no surprise (cycle 1 M2
  unaddressed).** Objective 2 = "quantify variance components"; Contribution 2 just
  fills in $\\omega^2=0.296$. The interaction-dominates-detector finding is the actual
  novelty but is never previewed as a question in §1.3. Same for Contribution 3a's
  4-feature core. Reframe Objective 2 as "Determine which factor — scoring, detector, or
  pathogen — dominates variance" and Objective 3 as "Test whether a small information
  core suffices and whether multi-source integration externally validates on
  vaccine-escape sets", so Contributions become non-trivial answers.

- **[M-04] ch1:142 "broadest" claim references 8,580 evals + 11-pathogen panel only,
  but Contribution 3 evidence comes from a 12-pathogen Stage 3 panel.** A hostile
  reader reads L142 as the headline scope and is later told L150 evaluates a different
  panel. Either restate Contribution 1 scope as "11-pathogen main panel + 12-pathogen
  feature-integration extension" or footnote the discrepancy.

- **[M-05] ch1:148 cluster-bootstrap CI [0.195, 0.333] without n_clusters=11
  caveat.** Codex / Ch5 acknowledge that 11 clusters is below the Bolker
  rule-of-thumb (~20–30) and only marginally above the (5–6) lower threshold. Ch1 cites
  the CI as if it carried full asymptotic warrant. One-clause caveat: "(11 pathogen
  clusters, near the small-cluster regime; see Section~\\ref{sec:limitations})".

### Minor
- **[m-01] ch1:106 TikZ "10 information types across 11 pathogens" — same 11/12
  ambiguity as C-01.** Update once C-01 is fixed.
- **[m-02] ch1:151 "ESM-2 for SARS-CoV-2" (per-feature AUC) vs ch1:146 "protein
  language model scores for SARS-CoV-2 and RSV" (MCC).** Two different metric
  framings, both consistent in spirit but the metric labels are absent at L151.
  Add "(per-feature AUC)" parenthetical to L151 and "(MCC-best)" at L146.
- **[m-03] ch1:150 "(0.081 of 0.083 mean MCC)" never explicitly relates to the
  abstract's "97.6%" wording — readers must compute themselves. Cycle 1 m6 unaddressed.
- **[m-04] ch1:11 self-cite `youn2025mutclust` for "core task" (cycle 1 M3 P2)**
  remains. Replace with `harvey2021tracking` or `carabelli2023convergent`.
- **[m-05] ch1:33 missing EVEscape (`thadani2023evescape`) and Livesey & Marsh
  (`livesey2020using`)** — cycle 1 P2 G26 unaddressed.

## C. P1/P2 follow-up status (cycle 1)

| Cycle 1 ID | Item | Ch1 status |
|------------|------|-----------|
| G24 (P1) | Information-type panel 11 vs 12 conflict | OPEN — escalated to C-01 |
| G27 (P2) | youn2025mutclust core-task self-cite | OPEN (m-04) |
| G25 (P2) | Cancer benchmark cite thin (bailey2018 only) | OPEN |
| G26 (P2) | EVEscape / Livesey & Marsh missing | OPEN (m-05) |
| Cycle1 M2 | Objectives ↔ Contributions surprise | OPEN (M-03) |
| Cycle1 M5 | Strawman risk in §1.2 problems | OPEN, low impact |
| Cycle1 M6 | Figure body novel-only ordering | OPEN (M-01) |
| Cycle1 m2 | three-stage / Stage~3 vocabulary | OPEN (M-02) |
| Defense Q3 (n_clusters=11) | Bolker caveat in Ch1 | OPEN (M-05) |

## D. Number/claim consistency check (Ch1 only)

| Claim | Locations | Status |
|-------|-----------|--------|
| 8,580 evaluations | L33 (implicit), L82, L142 | consistent |
| 20 scoring × 39 detector × 11 pathogen | L82 | consistent with ch4:277 |
| 14 detection families | L82, L165 | consistent |
| 10 information types | L33, L90, L106, L143, L151 | consistent |
| Pathogen count 11 vs 12 | L78, L82, L106, L142, L145 (=11) vs L150 (=12) | **INCONSISTENT** (C-01) |
| HIV-1 full 7.19× p=2.5e-16 | L153 | consistent w/ abstract |
| HIV-1 novel 7.16–8.24× | L117, L150, L153 | consistent |
| HIV-1 novel Bonferroni 3.9e-9 | L150 | now sourced (ch4:956) |
| H3N2 9.36× full / 7.19× novel p=0.132 | L150, L153 | consistent w/ ch4:991 |
| ω²=0.296 CI [0.195, 0.333] | L114 (TikZ), L148 | consistent w/ abstract |
| 6-cat lower bound 0.103 | L148 | consistent |
| 9 distinct optimal types | L114, L145, L146 | consistent |
| LOPO 0/11 null-consistent | L145, L148 | consistent |
| 4-feature core delta +0.011 CI [-0.018, +0.042] | L150, L152 | consistent (but C-02 wording overclaim) |

## E. Recommended cycle 2 edits (priority order)

1. **[P0] ch1:82** — `across all 11 pathogens` → `on the 11-pathogen main panel
   (extended to 12 with Zika for feature ablation; Section~\\ref{subsec:feature_ablation})`.
   Also update TikZ box at ch1:106 in lockstep.
2. **[P0] ch1:152 and ch1:150** — drop "operationally equivalent" / replace with
   "statistically indistinguishable within a $\\pm$0.04 MCC non-inferiority bound under
   nested-LOPO". Aligns Ch1 with the codex P5-01 caveat language already in Ch4/Ch6.
3. **[P0] ch1:117 (TikZ)** — reorder to lead with novel-only 7.16–8.24× as the primary
   anchor and demote full-set 7.19× to parenthetical, matching caption at L131.
4. **[P1] ch1:41** — rename "three-stage process" → "three-step pipeline (sequence
   collection → computational analysis → experimental validation)"; remove the word
   "Stage" from §1.1. Eliminates collision with §1.3/§1.4 Stage 1/2/3.
5. **[P1] ch1:111 (TikZ)** — `2-Stage + Integration` → `2-Stage main + Stage 3 layer`
   to match the prose patch.
6. **[P1] ch1:148** — append `; 11 pathogen clusters, near the small-cluster
   regime; see Section~\\ref{sec:limitations}` to the cluster-bootstrap CI.
7. **[P2] ch1:77–88** — rephrase Objectives 2 and 3 as open questions to give
   Contributions 2/3 surprise value (M-03).
8. **[P2] ch1:11** — replace `youn2025mutclust` with `harvey2021tracking` or
   `carabelli2023convergent` for the "core task" anchor (m-04).
9. **[P2] ch1:33** — add `thadani2023evescape` (EVEscape) and `livesey2020using`
   (Livesey & Marsh) to the concurrent-benchmark list (m-05).
10. **[P2] ch1:151** — add metric labels: "(per-feature AUC)" at L151 and "(MCC-best)"
    at L146.

## F. Severity summary

- Critical: **2** (C-01 11/12 pathogen conflict; C-02 "operationally equivalent" overclaim)
- Major: **5** (M-01..M-05)
- Minor: **5** (m-01..m-05)
- P0 escalations from cycle 1: **2** (G24 → C-01; codex P5-01 wording collateral → C-02)
- Cycle 1 P0 verification: 4/5 PASS (G09, G10, G02b, G01-not-applicable), 1 PARTIAL
  (G08 — prose patched, TikZ subbox + §1.1 vocabulary not aligned).

Codex IV&V style stance per finding:
- C-01: AGREE (numeric inconsistency, mechanical fix).
- C-02: AGREE — wording overclaim, equivalence-margin missing.
- M-01: AGREE — figure/abstract framing mismatch.
- M-02: MODIFY — Major in this cycle because cycle 1 G08 patch made the collision
  worse; codex would likely call it Moderate.
- M-03: MODIFY — structural, not a defect of fact; codex would call it stylistic.
- M-04: AGREE — scope-claim drift between L142 and L150.
- M-05: AGREE — small-cluster caveat already exists in Ch5; surfacing in Ch1 is cheap.
