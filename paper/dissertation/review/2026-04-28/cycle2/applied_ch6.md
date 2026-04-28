# Cycle 2 Ch6 fix application report

Date: 2026-04-28
Target file: `/proj/paper/paper/dissertation/chapters_en/ch6_conclusion.tex`
Source matrices:
- `/proj/paper/paper/dissertation/review/2026-04-28/cycle2/integrated_fix_matrix.md` §8 (12 items, 88 min budget)
- `/proj/paper/paper/dissertation/review/2026-04-28/cycle2/ch6_review.md` §F (10 edits)
- `/proj/paper/paper/dissertation/review/2026-04-28/phase2b_ch6.md` (cycle 1 carry-over)

Cycle 1 P0 (G07, G12, G02b) status going in: G07 PASS, G12 PASS, G02b PARTIAL FAIL — addressed in this cycle.

---

## 1. Applied fixes (file:line refers to pre-edit line numbers)

| # | ID | Severity | file:line | Action |
|---|----|----------|-----------|--------|
| 1 | 6-P0-1 (C-1, G02b PARTIAL) | **P0** | ch6:13 | Friedman elevated to main statistic; LOPO 0/11 alone retained as corroborative consistency check. |
| 2 | 6-P0-5 (C-2 PAHD-R scope creep) | **P0** | ch6:16 | Recast PAHD-R as a discussion-level synthesis (Chapter ref), explicitly "not as an additional benchmark contribution." Option B chosen — minimal cross-chapter ripple. |
| 3 | 6-P0-2 (M-1 broadest + M-1 grid + m-2 Layer A def) | **P0** | ch6:11 | Restored "to our knowledge / broadest region-level, single-position hotspot-detection benchmark"; restored full grid (10 info × 14 families × 11 pathogens = 8,580); precise Layer A union definition; Layer B/C explicit; hotspot-score metric named; 2-stage main + Stage 3 layer mentioned. |
| 4 | 6-P1-3 (M-2 two-part) | P1 | ch6:14 | Contribution 3 split into 3a (integration infrastructure) and 3b (external validation, HIV-1 anchor). Header line also updated to "four results, organized as Contributions 1, 2, 3a, 3b." |
| 5 | 6-P1-4 (m-1 H3N2 p) | P1 | ch6:14 | Added `$p = 0.0023$` to 4.012-fold H3N2 enrichment. |
| 6 | 6-P1-7 (Bonferroni p_adj 3.9e-9) | P1 | ch6:15 | Added `Bonferroni $p_{\text{adj}} \approx 3.9 \times 10^{-9}$ across 780 combinations` to novel-only Fisher result; matches ch1:150 exactly. Also added 9.36× and 7.63× explicit values for H3N2 and SARS-CoV-2 (closing minor gap flagged in ch6_review §C). |
| 7 | 6-P1-6 (M-3) | P1 | ch6:91 | "confirms a feasible direction" → "is consistent with a feasible direction" (softened modal). |
| 8 | 6-m-8 (m-3 13-dim) | P2 | ch6:72 | "13-dimensional profile space" → "high-dimensional pathogen profile space" (definition source not present in ch4/ch5; soft fix applied). |
| 9 | 6-m-9 (Future work scope specificity) | P2 | ch6:83 | DNA-virus extension specified with HBV polymerase, HSV-1 glycoprotein; multi-protein expanded to "beyond surface glycoproteins"; real-time surveillance specified with Nextstrain pipelines. |
| 10 | 6-m-10 (m-4 Priority 4 prose) | P2 | ch6:81 | Added new `\textbf{Reproduction and Release.}` paragraph after Additional Research Directions, instantiating Priority 4 of `tab:future_roadmap`. Maps prose 1-1 with table. |
| 11 | 6-m-11 (m-5 take-home) | P2 | ch6:92 | "than choosing among detection algorithms" → "than the detection-algorithm main effect alone" (acknowledges the ω²=0.082 family×pathogen substantial effect). |
| 12 | 6-m-12 (m-9 self-consistency) | P2 | ch6:90 | "self-consistency evidence" → "self-consistency check" (vocabulary unified with ch6:15, abstract:11, ch1:150). |

Total: 12 / 12 items in §8 of integrated_fix_matrix applied.

---

## 2. Items NOT in fix list but addressed opportunistically

- **Headline rewrite "three results" → "four results, organized as Contributions 1, 2, 3a, 3b"**: required to make the new (3a)/(3b) split coherent at the opening of §6.1. Direct corollary of 6-P1-3.
- **9.36× and 7.63× restored in ch6:15**: the M-2 fix already touches the contiguous (3b) sentence, and ch6_review §C had marked the absent 9.36× / 7.63× values as a gap (Minor). Restored as part of the same edit to avoid revisiting the paragraph.

No items deferred or skipped within ch6 scope.

---

## 3. Cross-chapter sync verification

Performed `grep -n` against `front_en/abstract.tex` + `chapters_en/ch1_introduction.tex` + `chapters_en/ch6_conclusion.tex` for each of the load-bearing P0/P1 phrases:

| Anchor | Abstract | Ch1 | Ch6 | Verdict |
|--------|----------|-----|-----|---------|
| `to our knowledge ... broadest ... region-level, single-position` | abstract:4 ✓ | ch1:142 ✓ | ch6:11 ✓ (new) | **sync** |
| `8{,}580` grid | abstract:2,4 ✓ | ch1:82,142 ✓ | ch6:11 ✓ (new) | **sync** |
| Layer A: convergent + immune-escape + HVR union | abstract:6 ✓ | ch1:143 ✓ | ch6:11 ✓ (new, was compressed) | **sync** |
| Friedman main / LOPO corroborative split | abstract:10 ✓ | ch1:145,148 ✓ | ch6:13 ✓ (re-edit) | **sync** |
| Contribution 3 two-part marker `(3a)/(3b)` | abstract:11 ✓ | ch1:150 ✓ | ch6:14–15 ✓ (new) | **sync** |
| 4.012× p=0.0023 | abstract:11 ✓ | ch1:150,153 ✓ | ch6:14 ✓ (new) | **sync** |
| novel-only 7.16–8.24× + Bonferroni p_adj 3.9e-9 | abstract:11 (3.9e-9 still pending A-P1-5) | ch1:150 ✓ | ch6:15 ✓ (new) | **partial** — abstract A-P1-5 not yet applied (out of ch6 scope) |
| H3N2 9.36× / SARS-CoV-2 7.63× | abstract:11 ✓ | ch1:150,153 ✓ | ch6:15 ✓ (new) | **sync** |
| PAHD-R presence | absent | absent | ch6:16 (now demoted to "discussion-level synthesis") | **sync** — no scope creep |
| `self-consistency check` | abstract:11 ✓ | ch1:150 ✓ | ch6:15,94 ✓ (re-edit) | **sync** |
| `confirms` → softened modal | n/a | n/a | ch6:91/95 ✓ | landed |

Summary: 10/11 cross-chapter anchors fully synced after ch6 edits. The single residual is abstract:11 missing the explicit "Bonferroni p_adj 3.9e-9 across 780 combinations" — that is fix `A-P1-5` in §2 of the integrated matrix and belongs to the abstract agent. Ch1:150 and ch6:15 now express it identically; abstract:11 just needs the same one-clause append.

---

## 4. Cycle 1 P0 status (post cycle 2)

| Cycle 1 ID | Site | Status |
|------------|------|--------|
| G07 (4-feature paired-test caveat) | ch6:14 | PASS — already landed; not touched by this cycle (the (3a) split preserved the full caveat block including paired delta / CI / p=0.61). |
| G12 (HIV-1 full vs novel-only split) | ch6:15 | PASS — preserved and strengthened (Bonferroni p_adj 3.9e-9 added; 9.36× and 7.63× now explicit). |
| G02b (Friedman / LOPO separation) | ch6:13 | **PASS post-rewrite** — Friedman now labeled "cluster-robust main statistic, consistent with the interaction effect"; LOPO alone is the corroborative consistency check. PARTIAL FAIL closed. |

Cycle 1 phase2b ch6 issues (C1, C3, M1, M2, M3, M4, m1, m3, m8, m9): all addressed in this round. C4 caveat (no paired-test significance for 97.6%) was already retained inside the (3a) block by virtue of preserving the existing paired-delta wording.

---

## 5. Defense-question coverage check (§G of ch6_review)

1. *"What is the single strongest external evidence?"* — answered: HIV-1 7.19× full-set + 7.16–8.24× novel-only (ch6:15). PASS.
2. *"Three contributions vs four — which is correct?"* — now answered: ch6:10 declares "four results, organized as Contributions 1, 2, 3a, 3b." PASS (was unanswered pre-edit).
3. *"Where is the limit of the adaptive claim stated?"* — answered: ch6:91/95 "is consistent with a feasible direction ... not a universal adaptive predictor" + Limitations table (ch6:24–43). PASS.

---

## 6. File-level diff summary

Lines changed in `chapters_en/ch6_conclusion.tex`:
- §6.1 contribution paragraph (lines 10–16): full rewrite.
- §6.3 Future Research Directions: "13-dimensional" softened (line 72); DNA-virus / HBV / HSV-1 / Nextstrain specified (line 83); new **Reproduction and Release** paragraph appended (post line 83).
- §6.4 Concluding Remarks (lines 91–94): "confirms" → "is consistent with"; "self-consistency evidence" → "self-consistency check"; take-home main-effect qualifier.

No additions to bibliography, figures, or tables. No new `\label` introduced. `\ref{ch:discussion}` is reused from the existing PAHD-R reference; `\ref{sec:code_availability}` and `\ref{tab:future_roadmap}` are pre-existing labels.

---

## 7. Risks / residuals

- **Abstract A-P1-5 still pending**: the explicit Bonferroni p_adj 3.9e-9 clause is in ch1:150 and ch6:15 but not yet in abstract:11. The abstract agent (run separately) is responsible for that propagation.
- **PAHD-R framing**: option B (demote to discussion synthesis) was applied. If the committee asks "why introduce a named framework only in Discussion/Conclusion?", the response is now anchored on the new ch6:16 wording — PAHD-R is *not* counted as a fifth contribution. Should the user later prefer option A (add PAHD-R to abstract + ch1), the ch6:16 demotion would need to be reverted; current state assumes option B is final.
- **Headline rewording** "three results" → "four results, organized as Contributions 1, 2, 3a, 3b": this is consistent with abstract:11's "Contribution 3 is two-part" but is a counting convention. Some committees prefer "three contributions, with Contribution 3 in two parts." If that softer phrasing is preferred, ch6:10 can be reverted to "three contributions" while keeping the (3a)/(3b) split downstream — neither variant breaks alignment with abstract / ch1.

---

## 8. Verification checklist

- [x] All 12 §8 fix-matrix items applied.
- [x] Cycle 1 G02b PARTIAL → PASS.
- [x] PAHD-R confined to ch6 (no abstract / ch1 ripple).
- [x] Friedman / LOPO sync with abstract:10 + ch1:145/148.
- [x] Two-part Contribution 3 marker present in ch6:14–15.
- [x] H3N2 4.012×, p=0.0023 + Bonferroni p_adj 3.9e-9 + 9.36× + 7.63× now in ch6:14–15.
- [x] "broadest / to our knowledge / 8,580" restored in ch6:11.
- [x] "13-dimensional" softened to "high-dimensional".
- [x] §6.3 prose now maps 1-1 with `tab:future_roadmap` (Priority 4 added).
- [x] Take-home qualifier: "main effect alone" present.
- [x] "self-consistency check" used in both ch6:15 and ch6:94.
- [x] No new `\label`; no broken `\ref`; cross-references all resolve to pre-existing labels.

Result: ch6 cycle 2 patch landed. Estimated reading time of patched §6.1 unchanged (~120 s); LaTeX compile risk: low (no math envs altered, no new packages).
