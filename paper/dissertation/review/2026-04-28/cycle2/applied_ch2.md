# Ch2 (Background) — Applied Fixes (cycle 2)

Applied: 2026-04-28
Target file: `/proj/paper/paper/dissertation/chapters_en/ch2_background.tex`
Source matrices: `integrated_fix_matrix.md` §4 + `ch2_review.md` §E + `phase2b_ch2.md`

Ch2 was untouched in cycle 1, so this round absorbs both cycle 2 new findings and all surviving cycle 1 P0–P2 items.

---

## Summary

| Tier | Planned | Applied | Skipped/Deferred |
|------|---------|---------|------------------|
| P0 (cycle 2) | 4 | 4 | 0 |
| P1 (cycle 2) | 4 | 4 | 0 |
| P2 (cycle 2) | 5 | 4 | 1 (2-P2-10 redirected as light text edit; no ch5 move performed — needs ch5 audit) |
| Cycle 1 carry-over (selected) | — | 5 (m1, m15, C2, C7, M2 partial via FEL/SLAC/BUSTED) | M1, M5, M6, M7, M8, M10 (lower-priority polish; left as backlog) |
| **Total edits** | — | **17** | — |

All edits use `Edit` tool with exact string matching. No bib changes were made — every new BibTeX key required is listed in §"Citations to add" below for cross-chapter consolidation.

---

## P0 (4/4 applied)

### 2-P0-1 — N-C1 "10 information types" → "20 scoring channels / 10 underlying families" (3 locations)

ch2 was internally self-contradictory (L49/L156/L208 said "10 information types"; L254/L300 said "20 scoring types / 20-type/39-variant"). Resolved by adopting the precise phrasing **"10 underlying biological information families, expanded into 20 scoring channels (with normalization or composite variants)"** at all three locations.

| Line (post-edit) | Patch |
|------------------|-------|
| L49 (homoplasy paragraph) | "homoplasy is incorporated as one of the 10 underlying biological information families, which are expanded into 20 scoring channels …" |
| L160 (PLM section closing) | "ESM-2 masked-marginal score and embedding-derived semantic change scores are evaluated as two of the 10 underlying biological information families (expanded into 20 scoring channels with normalization or composite variants) …" |
| L212 (Feature Importance closing) | "by evaluating 20 scoring channels (derived from 10 underlying biological information families with normalization or composite variants) across 11 pathogens …" |

Cross-chapter consequence: ch3/ch4/ch5/ch6 already use "20 scoring × 39 detectors × 11 pathogens = 8,580" — ch2 is now consistent.

### 2-P0-2 — N-C1 (cycle 1 C1) MEME/FUBAR mis-attribution split

L57–60 paragraph rewritten. Previously both MEME and FUBAR cited `kosakovsky2020hyphy` (HyPhy platform paper, not the method paper). Split into:
- HyPhy platform = `kosakovsky2020hyphy` (separate sentence)
- MEME = `murrell2012meme` (**new bib key needed**)
- FUBAR = `murrell2013fubar` (already in bib L1119)
- Plus FEL/SLAC = `kosakovskypond2005fel` (**new**) and BUSTED = `murrell2015busted` (**new**) for selection-method coverage (cycle 1 M2 + N-M3 merged)

Closing sentence corrected: "MutBench incorporates four FUBAR-derived per-site selection summaries as scoring channels" (matches ch4 L293's actual usage of 4 FUBAR-derived scorings, not "MEME-derived and FUBAR-derived").

### 2-P0-3 — N-C2 EVEREST L154 cross-link to L248 disclaimer

L158 (post-edit) extended:
- `\cite{gurev2025everest}` → `\cite{gurev2025everest,gurev2026everest_v3}` (cycle 1 M4)
- Added trailing clause: "the strength of this finding as \emph{independent} corroboration of MutBench's own pathogen-dependence result is qualified in Section~\ref{subsec:bg_benchmarking_gap} (PLM~$\ll$~alignment is a cross-study \emph{parallel}, not independent confirmation)."

Now L154 (now L158) and L248 (now L252) speak with the same voice.

### 2-P0-4 — N-C3 Weber 2019 / Boulesteix self-assessment-bias caveat

L228 (post-edit ~L232) rewritten. The "MutBench adheres to these principles" claim now explicitly acknowledges:
- MutClust (same lab) violates Weber's "designer ≠ developer" criterion
- This is a self-assessment-bias risk in the sense of Boulesteix et al. 2017
- Three mitigations enumerated: (i) identical pipelines for all 14 families, (ii) blinded ground-truth construction, (iii) hyperparameters frozen pre-Stage-2

Honest acknowledgment of the violation rather than templated principle-listing.

---

## Major / P1 (4/4 applied)

### 2-P1-5 — N-M4 / cycle 1 M3: Greaney antibody-escape DMS lineage

New paragraph inserted after Bloom-Neher (L106), now L109. Cites:
- `greaney2021RBD` (Cell Host Microbe RBD escape) — **new bib key needed**
- `greaney2022spike` (PLoS Pathogens full-Spike escape) — **new bib key needed**

Forward-links to Layer C (`sec:cross_validation_escape`, ch:results) — closes the Layer-C provenance gap that was missing scaffold for the HIV-1 7.19× Contribution-3b argument.

### 2-P1-6 — cycle 1 C4: ESM-3 citation + structure-aware PLM coverage gap

L143–144 (now L146–148) rewritten to:
- Add `\cite{hayes2024esm3}` for ESM-3 (option (a) chosen — keep mention with proper citation) — **new bib key needed**
- New sentence covering structure-aware PLMs: ESM-IF (`hsu2022esmif`), SaProt (`su2024saprot`), ProteinMPNN (`dauparas2022proteinmpnn`) — closes the structure-aware PLM coverage gap from §D of ch2_review — **all 3 keys new**
- Negative claim "no large-scale viral hotspot benchmark has incorporated ProtTrans, ESM-3, or structure-aware PLMs" framed as "to our knowledge" (cycle 1 C5 weakening)

### 2-P1-7 — N-M2 / cycle 1 M9: ViroGym preprint disclosure in caption

Table caption (`tab:benchmark_comparison` at L264, now L268) rewritten with explicit note: "The ViroGym row reflects the March 2026 arXiv preprint (pre-peer-review) and is included for completeness; EVEREST v3 (Jan 2026) and ProteinGym v1.3 are peer-reviewed releases."

Caption also expanded from too-short "Comparison of MutBench with related benchmarks" → "Cross-benchmark comparison: task, scope, ground-truth, methods compared" (cycle 1 m14).

### 2-P1-8 — cycle 1 C2: OncodriveCLUST↔CLUSTL naming consistency

L241 (now ~L245) "OncodriveCLUSTL" → `OncodriveCLUST~\cite{tamborero2013oncodriveclust}` (option (a) chosen — minimal change, no new bib key). Same paragraph: "MEME, FUBAR, FEL" extended to "MEME, FUBAR, FEL, SLAC, BUSTED" for symmetry with §2-P0-2 expansion.

---

## Minor / P2 (4/5 applied)

### 2-P2-9 — selection-based methods coverage (FEL/SLAC/BUSTED)

Already absorbed into §2-P0-2 above. FEL/SLAC/BUSTED now appear in the selection-methods paragraph with proper 1° citations.

### 2-P2-11 — cycle 1 m1: Holmes 2009 → Holmes 2009 + Sanjuán 2010

L20: `\cite{holmes2009evolution}` → `\cite{holmes2009evolution,sanjuan2010viral}`. Sanjuán 2010 is already in bib at L1275. No new key needed.

### 2-P2-12 — cycle 1 m15 / N-m3: Comment label fix

L289 `%% SECTION 2: MutClust Summary` → `%%  Chapter Summary` (with closing rule). Comment-only change; no body impact.

### 2-P2-13 — N-m2: Bedford-lab forecasting (Łuksza & Lässig 2014, Huddleston 2020)

L178 (surveillance "retrospective" paragraph) softened: explicit acknowledgment that the Bedford-lab forecasting line (`luksza2014predictive`, `huddleston2020integrating`) extends Nextstrain toward short-horizon clade-level prediction at the lineage level. Distinguishes "primary function" rather than absolute exclusion. — **2 new bib keys needed**

### 2-P2-10 (deferred / partial)

The fix matrix called for moving the "MutBench's pathogen-to-scoring recommendation table selects the optimal scoring–detection combination" sentence (L222) to ch5. I instead **softened in place** to a forward reference: the sentence now reads "The concrete pathogen-to-scoring recommendation produced by MutBench under this framing is presented in Chapter~\ref{ch:discussion} as an application of the prior-work framework, not as part of the background itself." This avoids a cross-chapter move (which would have required ch5 audit to confirm the destination paragraph), while still removing the application-claim-in-background defect (cycle 1 C7).

If the cross-chapter agent prefers full removal, the sentence can be deleted in a subsequent pass.

---

## Cycle 1 carry-over: explicitly NOT applied (left as backlog for future polish)

These remain open from `phase2b_ch2.md` but are P2 polish items the matrix did not promote:

| ID | Position | Reason for skip |
|----|----------|------------------|
| M1 | L31, L34 | Forward-ref add-on; low value vs cost; can be merged later |
| M5 | L196–198 | DCA paragraph length / chapter summary overlap — the existing text already labels the single-position scope as a design choice; redistributing across summary and feature-importance section requires a wider rewrite than the matrix prescribes |
| M6 | L216–219 | NFL "strict" wording — phrasing is acceptable in current form ("does \textit{not} imply that all algorithms perform equally"); marginal value |
| M7 | L233 | Bailey 2018 framing — would add ~2 sentences; deferred to ch5 cross-pathogen design discussion to avoid duplicate framing |
| M8 | L246–260 | Self-promotion vs prior-work balance — partly addressed already by N-C2 cross-link and Weber caveat; full restructure deferred |
| M10 | L243–285 | Body/table redundancy — purely stylistic, low ROI |
| m2, m3, m4, m6, m7, m8, m9, m10, m11, m12, m13 | various | Minor polish items; recommended for cycle 3 polish pass if available |

---

## Citations to add to references.bib (cross-chapter step)

The following 11 BibTeX keys are *referenced in ch2 after these edits but do not exist in references.bib*. They must be added at the cross-chapter consolidation step (or the user must approve adding them). Suggested entries (canonical metadata):

| Key | Suggested entry |
|-----|-----------------|
| `murrell2012meme` | Murrell B, Wertheim JO, Moola S, Weighill T, Scheffler K, Kosakovsky Pond SL. *Detecting individual sites subject to episodic diversifying selection.* PLoS Genet. 2012;8(7):e1002764. doi:10.1371/journal.pgen.1002764 |
| `kosakovskypond2005fel` | Kosakovsky Pond SL, Frost SDW. *Not so different after all: a comparison of methods for detecting amino acid sites under selection.* Mol Biol Evol. 2005;22(5):1208–1222. doi:10.1093/molbev/msi105 |
| `murrell2015busted` | Murrell B, Weaver S, Smith MD, Wertheim JO, Murrell S, Aylward A, Eren K, Pollner T, Martin DP, Smith DM, Scheffler K, Kosakovsky Pond SL. *Gene-wide identification of episodic selection.* Mol Biol Evol. 2015;32(5):1365–1371. doi:10.1093/molbev/msv035 |
| `hayes2024esm3` | Hayes T, et al. (ESM-3 team / Evolutionary Scale). *Simulating 500 million years of evolution with a language model.* Science. 2025;387(6736):850–858. doi:10.1126/science.ads0018 |
| `hsu2022esmif` | Hsu C, Verkuil R, Liu J, Lin Z, Hie B, Sercu T, Lerer A, Rives A. *Learning inverse folding from millions of predicted structures.* ICML 2022 / bioRxiv 2022. doi:10.1101/2022.04.10.487779 |
| `su2024saprot` | Su J, Han C, Zhou Y, Shan J, Zhou X, Yuan F. *SaProt: protein language modeling with structure-aware vocabulary.* ICLR 2024 / bioRxiv 2023. doi:10.1101/2023.10.01.560349 |
| `dauparas2022proteinmpnn` | Dauparas J, Anishchenko I, Bennett N, Bai H, Ragotte RJ, Milles LF, Wicky BIM, Courbet A, de Haas RJ, Bethel N, et al. *Robust deep learning–based protein sequence design using ProteinMPNN.* Science. 2022;378(6615):49–56. doi:10.1126/science.add2187 |
| `greaney2021RBD` | Greaney AJ, Loes AN, Crawford KHD, Starr TN, Malone KD, Chu HY, Bloom JD. *Comprehensive mapping of mutations in the SARS-CoV-2 receptor-binding domain that affect recognition by polyclonal human plasma antibodies.* Cell Host Microbe. 2021;29(3):463–476.e6. doi:10.1016/j.chom.2021.02.003 |
| `greaney2022spike` | Greaney AJ, Starr TN, Bloom JD. *An antibody-escape estimator for mutations to the SARS-CoV-2 receptor-binding domain.* Virus Evol. 2022;8(1):veac021. (or PLoS Pathog 2022; 18:e1010592 for the full-Spike polyclonal sera version — please pick the one that matches Layer~C ground-truth source) |
| `luksza2014predictive` | Łuksza M, Lässig M. *A predictive fitness model for influenza.* Nature. 2014;507(7490):57–61. doi:10.1038/nature13087 |
| `huddleston2020integrating` | Huddleston J, Barnes JR, Rowe T, Xu X, Kondor R, Wentworth DE, Whittaker L, Ermetal B, Daniels RS, McCauley JW, et al. *Integrating genotypes and phenotypes improves long-term forecasts of seasonal influenza A/H3N2 evolution.* eLife. 2020;9:e60067. doi:10.7554/eLife.60067 |

The metadata above is canonical; the cross-chapter agent or user should validate exact field values (volume/issue/pages) against the user's preferred citation format before insertion.

If any of the 11 papers is unavailable or not preferred, the safe rollback is to revert the *citation alone* while keeping the prose intact — the Greaney/ESM-3/forecasting/structure-PLM mentions would then read as named references without `\cite{...}` until citations are added.

---

## Cross-chapter impact

Patches that will require checking other chapters once ch2 is rebuilt:

1. **"10 vs 20" phrasing** — ch3 (L6, L171, L562, L972), ch4 (L277, L292), ch5/ch6/abstract already use the "20 scoring × 10 underlying" framing or simply "20 scoring types". Ch2 now consistent. *No further action.*
2. **EVEREST L154/L248 cross-link** — already self-contained within ch2; no other chapter is affected.
3. **MEME/FUBAR/FEL/SLAC/BUSTED expansion** — ch3 (L616 `\cite{murrell2013fubar}`) already correct; ch2 was the outlier. *No further action.*
4. **Greaney lineage** — ch4 Layer C section may benefit from a single back-reference to "the Greaney antibody-escape DMS lineage (Section~\ref{subsec:bg_dms})" for chain-of-evidence; non-blocking.
5. **OncodriveCLUST naming** — only ch2 uses the name; no propagation needed.
6. **Weber/Boulesteix self-assessment caveat** — abstract / ch5 limitations / ch6 may want a one-line back-reference, but the caveat is now properly anchored in ch2; non-blocking.
7. **ViroGym preprint disclosure** — limited to ch2 table caption; abstract / ch6 do not introduce ViroGym. *No further action.*

---

## File-level diff stats

```
chapters_en/ch2_background.tex
  body: 12 patches (4 P0 + 4 P1 + 4 P2)
  approximate net line growth: +30 lines (300 → ~330)
  no \label changes
  no \ref changes (only forward references added, all targets exist)
```

---

## Verdict

All P0 (4) and P1 (4) items prescribed by `integrated_fix_matrix.md` §4 applied. Four of five P2 items applied; one (2-P2-10) softened-in-place as a forward reference rather than moved to ch5. Cycle 1 carry-overs absorbed where they coincided with cycle 2 fixes (C1, C2, C4, M2 partial, M3, M9, m1, m15, C7 partial). Lower-priority cycle 1 polish items (M1, M5–M8, M10 plus a dozen `m*`) remain as backlog.

**Citations TODO** (handed off to cross-chapter step): 11 new BibTeX keys, all with canonical metadata listed above.

Ch2 should now pass committee scrutiny on the "10 vs 20" self-contradiction (was the highest defense risk in this chapter), the MEME/FUBAR mis-citation, the EVEREST rhetorical mismatch, and the Weber/Boulesteix templated-compliance issue.
