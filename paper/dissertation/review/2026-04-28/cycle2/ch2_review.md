# Ch2 Background — Cycle 2 Adversarial Review (codex-style)

Target: `/proj/paper/paper/dissertation/chapters_en/ch2_background.tex` (300 lines)
Date: 2026-04-28
Cycle: 2 (post-cycle 1 fixes)

---

## A. Cycle 1 Fix Verification

Cycle 1 P0 list (summary.md G01–G14c) targeted ch1/4/5/6 — **no ch2 P0 items were included**, so ch2 cycle-1 issues (phase2b_ch2.md C1–C7, M1–M10, m1–m15) **remain unfixed in current ch2 source**. Spot-check:

- **C1 MEME/FUBAR mis-citation** still present at L57 (`\cite{kosakovsky2020hyphy}` for both MEME and FUBAR; `murrell2013fubar` exists in bib L1119 but is unused in ch2; `murrell2012meme` not in bib).
- **C2 OncodriveCLUST↔CLUSTL** still inconsistent: L39 (`tamborero2013oncodriveclust`) vs L241 ("OncodriveCLUSTL" with no separate citation; `arnedopac2019` absent from bib).
- **C4 ESM-3 named without citation** at L143 still present.
- **M3 Greaney 2021/2022 escape-DMS** still missing — confirmed by `grep "greaney"` returning 0 hits in references.bib.

Cycle 1 ch2 verdict ("CONDITIONAL PASS, 5 priority fixes") was not actioned. All cycle-1 ch2 findings carry forward to cycle 2.

---

## B. New Adversarial Findings (Cycle 2)

### CRITICAL

**N-C1 — Cross-chapter count contradiction "10 information types" vs "20 scoring types".**
Ch2 L49, L156, L208 say MutBench evaluates **10 information types**. Ch3 L6, L171, L562, L972 and Ch4 L277, L292 consistently say **20 scoring types** (= 10 underlying features × variants/composites). Ch4 L278 reconciles: "20 scoring types are derived from 10 underlying biological features." Ch2's repeated unqualified "10 information types" claim contradicts the headline design statement "20 scoring × 39 detectors × 11 pathogens = 8,580" and undercuts the `ω² = 0.296 (20-type model)` framing introduced at ch2 L254 within the same chapter. Self-inconsistent within ch2.
**Severity: Critical** (factual count drift, defense-vulnerable).

**N-C2 — EVEREST cited as competing source for "PLM ≪ alignment" while ch2 itself disclaims independence.**
Ch2 L154 cites EVEREST v1 only (`gurev2025everest`) for the "PLMs underperform alignment-based methods" claim. Ch2 L248 then states: "Because MutBench's LOPO 0/11 match rate is itself null-consistent under permutation … we describe this as a cross-study *parallel* … rather than as independent corroboration." This honest disclaimer at L248 directly weakens the rhetorical use of EVEREST at L154 to motivate the PLM-section investigation, but L154 is not cross-linked to L248. A defender reading L154 in isolation would interpret EVEREST as independent corroboration.
**Severity: Critical** (rhetorical inconsistency between section claims and chapter-level disclaimer).

**N-C3 — Required citation Weber 2019 cited but not discussed.**
Required-citations.md mandates Weber 2019 be cited in proper context. Ch2 L226 cites `weber2019benchmarking` with three principles (independent evaluation, multiple metrics, controlled design). The wording is templated — there is no discussion of *which* Weber criterion MutBench arguably violates (e.g., "independent evaluation": MutBench design and execution are by the same author group). Compliance is asserted (L228 "MutBench adheres to these principles") without acknowledging that Weber's "independent evaluation" requires designer ≠ method-developer, which is partially violated whenever MutClust (`youn2025mutclust`, same lab) is included as a benchmarked method.
**Severity: Critical** (Weber citation present but mis-applied; Boulesteix 2017 self-assessment-bias citation L227 makes this contradiction worse).

### MAJOR

**N-M1 — "First / largest / broadest" claim vulnerability.**
Ch2 L254–260 lists three "capabilities absent in EVEREST and other VEP benchmarks." Item (1) "scoring × pathogen interaction via three-way ANOVA" — vulnerable because ProteinGym v1.3 supplementary materials do report per-protein × per-method variance decompositions; the differentiation rests on ω² being *headline* in MutBench vs *supplementary* in ProteinGym, not on absence. Item (3) "concrete pathogen-to-scoring recommendation table" — this is a deliverable choice, not a methodological capability. Of the three claimed novelties, only (2) "vaccine-escape circularity audit" is robustly differentiating. The phrasing "absent in EVEREST" is a **strong negative claim** that requires having actually checked EVEREST v3 supplementary tables.
**Severity: Major** (defensible only if scope of "absent" is narrowed).

**N-M2 — ViroGym 2026 admitted as comparable benchmark with weak provenance.**
L237 introduces ViroGym (`virogym2026`) as a peer comparator in Table~\ref{tab:benchmark_comparison}. Cycle 1 phase2b_ch2 M9 flagged this as arXiv-only / pre-peer-review. Currently ch2 L237 says "(Mar 2026)" but the comparison table treats ViroGym alongside ProteinGym and EVEREST without preprint-status disclosure in the table itself or its caption. A reviewer accessing the table independently would not know ViroGym is unrefereed.
**Severity: Major.**

**N-M3 — Selection-based methods coverage is asymmetric.**
Selection-based methods (L56–60) cover MEME and FUBAR but omit **FEL, SLAC, BUSTED, aBSREL, RELAX** — the rest of the HyPhy selection-test family. dN/dS-aware hotspot detection has a 20+ year history (Yang & Nielsen 2002, PAML; Murrell et al. 2015 BUSTED). The chapter's selection-method paragraph is one paragraph long versus three full paragraphs on PLMs (L125–156) and is the weakest argued subsection given that MutBench's own benchmark *uses FUBAR-derived scores* in 4 of 20 scoring formulas (ch4 L293).
**Severity: Major** (under-coverage of a method family that ch3 actually uses).

**N-M4 — Antibody escape DMS as Layer C ground-truth lineage missing.**
Phase2b_ch2 M3 already flagged this. Greaney et al. 2021 (Cell Host Microbe), 2022 (PLoS Pathog), and the Bloom lab antibody-escape DMS series are the **direct experimental antecedent** of Layer C / vaccine-escape positions used in ch4. Ch2 L102–106 lists Starr 2020, Dadonaite 2023, Lee 2018, Bloom-Neher 2023, but the *escape* DMS lineage is absent. The entire Contribution-3b argument (HIV-1 7.19× vaccine escape) lacks its background-chapter scaffold.
**Severity: Major** (Layer C provenance gap).

### MINOR

**N-m1 — "Holmes 2009" mutation rate citation (L20)** is a textbook secondary source; Sanjuán et al. 2010 (`sanjuan2010viral`) is in bib at L1275 and is the primary 1° source. Use both.

**N-m2 — Surveillance section omits Bedford-lab forecasting** (L172–180). Nextstrain has a `forecasts` module (Łuksza & Lässig 2014; Huddleston 2020). The "surveillance is retrospective" claim is overstated.

**N-m3 — Chapter Summary mislabel (L289–290).** Comment block reads `%% SECTION 2: MutClust Summary` but content is actually the chapter summary (cycle-1 m15, still uncorrected).

---

## C. Required Citation Audit Table

| Required citation | Bib key | In ch2? | Context quality | Issue |
|---|---|---|---|---|
| EVEREST | `gurev2025everest`, `gurev2026everest_v3` | L112, L154, L248, L250, L270 (table) | **Discussed** | Honest L248 disclaimer not back-linked to L154 (N-C2) |
| EVEscape | `thadani2023evescape` | L146–148, L203 | **Discussed twice** (PLM section + feature-importance section) | OK; minor concern that EVE→ESM2 substitution caveat noted but content-impact not quantified (cycle 1 C6) |
| Weber 2019 | `weber2019benchmarking` | L226 | **Cited, weakly applied** | Weber's "independent evaluation" criterion contradicts MutClust self-inclusion (N-C3) |
| Livesey & Marsh 2023 | `livesey2020using` | L115, L117 | **Discussed** | OK |
| Bailey 2018 | `bailey2018comprehensive` | L233, L270 (table) | **Cited, uncritical** | Limitations not surfaced (cycle 1 M7) |
| ProteinGym | `notin2023proteingym`, `notin2025proteingym_v13` | L159, L236, L246, L270 (table) | **Discussed extensively** | OK |
| Rice 1976 | `rice1976algorithm` | L213, L214, subsection title | **Discussed** | Background-vs-application boundary blurred (cycle 1 C7); NFL "strict" claim overreaches (cycle 1 M6) |

**Verdict**: All 7 required citations are cited; **2 (Weber, Bailey) are contextually weak**, **1 (EVEREST L154) is rhetorically over-leveraged** vs the chapter's own L248 disclaimer.

---

## D. Coverage Gap Analysis

| Subfield | Ch2 coverage | Gap severity |
|---|---|---|
| Frequency-based methods | L24–28 | OK |
| Entropy-based methods | L30–34 | OK |
| Cancer-genomics hotspot detection | L36–41, L233 | OK |
| Phylogeny-aware (homoplasy, treetime, BEAST) | L43–49 | OK |
| Selection-based dN/dS (MEME/FUBAR/FEL/SLAC/BUSTED) | L56–60 | **WEAK** — only MEME/FUBAR, mis-cited (N-M3, cycle-1 C1) |
| Density-based clustering | L65–89 | OK |
| DMS for protein fitness | L94–122 | OK |
| **Antibody-escape DMS (Greaney, Bloom-lab)** | — | **MISSING** (N-M4) |
| PLM landscape | L125–156 | OK; ESM-3 named but uncited (cycle-1 C4) |
| Coupling-aware / DCA / EVcouplings | L196–198, L299 | Acknowledged as out-of-scope; OK |
| Structure-aware PLM (ESM-IF, SaProt, ProteinMPNN) | — | **MISSING** (cycle 1 fairness section) |
| Surveillance platforms (Nextstrain, PANGO, GISAID) | L170–185 | OK; forecasting module overlooked (N-m2) |
| Antigenic cartography (Smith 2004; PLANT; Łuksza-Lässig) | L249 | Brief; under-developed |
| Algorithm selection / NFL / meta-learning | L213–223 | OK; NFL strict claim slightly overreaches |
| Benchmarking guidelines (Weber, Mangul, Boulesteix) | L226–227 | Cited, weakly applied (N-C3) |

**Two material gaps**: antibody-escape DMS lineage and structure-aware PLM family.

---

## E. Recommended Cycle 2 Edits (priority order)

| Pri | File:line | Current | Proposed fix | Severity |
|---|---|---|---|---|
| P0 | ch2 L49, L156, L208 | "10 information types" | Replace with "20 scoring types derived from 10 underlying biological features" (matches ch3/ch4 phrasing) | Critical |
| P0 | ch2 L57 | `MEME … FUBAR … \cite{kosakovsky2020hyphy}` | Split: `MEME~\cite{murrell2012meme}` (add to bib) + `FUBAR~\cite{murrell2013fubar}` (already in bib L1119); keep HyPhy citation in a separate sentence as the platform | Critical |
| P0 | ch2 L154 | `\cite{gurev2025everest}` | Add v3 + cross-link to L248 disclaimer: `\cite{gurev2025everest,gurev2026everest_v3}; the strength of this as independent corroboration is qualified in the discussion of Section~\ref{subsec:bg_benchmarking_gap}` | Critical |
| P0 | ch2 L228 | "MutBench adheres to these principles…" | Add: "with the partial exception that MutClust~\cite{youn2025mutclust}, developed in the same lab, is one of the 14 evaluated detection families; this is mitigated by … [identical conditions / blinded ground truth]" | Critical |
| P1 | ch2 L106 (after Bloom-Neher) | — | Insert new paragraph citing Greaney 2021 (`greaney2021RBD`) and Greaney 2022 (`greaney2022spike`); state "these escape DMS datasets directly inform the Layer C cross-validation paradigm (Section~\ref{sec:cross_validation_escape})" | Major |
| P1 | ch2 L143–144 | "the ESM-3 generation … (no formal citation key …)" | Either cite Hayes et al. 2024 (Science 387:850) or remove the ESM-3 mention | Major |
| P1 | ch2 L237 table caption | (no preprint status) | Add to table caption: "ViroGym row reflects the March 2026 arXiv preprint (pre-peer-review)." | Major |
| P1 | ch2 L57 / L241 | OncodriveCLUST vs OncodriveCLUSTL | Pick one: either change L241 to "OncodriveCLUST" (uses existing `tamborero2013oncodriveclust`) or add `arnedopac2019` to bib | Major |
| P2 | ch2 L56–60 | Selection-based one paragraph | Add 1–2 sentences listing FEL/SLAC/BUSTED with `kosakovskypond2005fel` (new bib entry) | Major |
| P2 | ch2 L222 | "MutBench's pathogen-to-scoring recommendation table selects…" | Move to ch5 discussion or rewrite as forward-reference only | Minor |
| P2 | ch2 L20 | `\cite{holmes2009evolution}` | `\cite{holmes2009evolution,sanjuan2010viral}` | Minor |
| P2 | ch2 L289 | `%% SECTION 2: MutClust Summary` | Comment label `%% Chapter Summary` | Minor |

---

## F. Severity Summary

| Tier | Count | Notes |
|---|---|---|
| **Critical (cycle 2 new)** | 3 (N-C1, N-C2, N-C3) | + cycle 1 carry-over: C1, C2, C4 → **6 total open Critical** |
| **Major (cycle 2 new)** | 4 (N-M1, N-M2, N-M3, N-M4) | + cycle 1 carry-over: M1–M10 mostly open → **~12 total open Major** |
| **Minor (cycle 2 new)** | 3 (N-m1, N-m2, N-m3) | + cycle 1 m1–m15 mostly open |
| **Required citations missing/weakly placed** | 2 weakly applied (Weber, Bailey), 0 missing | — |
| **Coverage gaps** | 2 (antibody-escape DMS; structure-aware PLM) | — |

**Verdict**: Ch2 was not touched during cycle 1 P0 fixes; all cycle 1 findings remain. Cycle 2 adds **3 new Critical issues** dominated by the **"10 vs 20" count contradiction (N-C1)** which is internally self-inconsistent within ch2 itself, and the **EVEREST L154/L248 rhetorical mismatch (N-C2)**. Recommend P0 fixes (4 items) before defense; P1 fixes resolve the antibody-escape DMS gap and ESM-3 citation hygiene.

Total substantive issues found in cycle 2: **10** (3 Critical + 4 Major + 3 Minor) + carry-over.
