# Task: Adversarial verification of MutBench dissertation — Round 2 (deep)

You are an independent external reviewer. This is the **second** independent review of this dissertation. Round 1 (report at `review/2026-04-17/codex_verification_report.md`) found 3 Critical, 9 Major, 5 Minor, and 5 out-of-frame issues; Claude applied ~15 patches in response. Your job is (A) verify those patches are complete and did not introduce regressions, (B) dig into areas Round 1 could not reach, and (C) run a mock defense with three reviewer personas. Be adversarial, not agreeable.

## Access

Working directory: `/proj/paper/paper/dissertation/`
Additional read-only dir: `/proj/paper/results/` (Stage 2/3 CSVs — Round 1 could NOT access these; you CAN)

Key files (same as Round 1):
- `front_en/abstract.tex`, `back/abstract_en.tex`
- `chapters_en/ch1_introduction.tex` through `ch6_conclusion.tex`
- `dissertation_easy_guide_v2.md`
- `references.bib`
- `review/2026-04-17/codex_verification_report.md` (Round 1 findings — READ ONCE, do not repeat)

Patches Round 1 triggered (summary, verify via `git log --oneline -10` or `git diff HEAD~N`):
- **P1 (m1/m2/m5/M9)**: HCV 0.701→0.700; EVEREST v1/v3 versioned DOIs; `tab:9pathogen_*` → `tab:stage2_*`; PLANT author list replaced with Ito et al.
- **P2 (C3/M5/M8)**: ch6:22 LOPO "does not generalize" → null-consistent corroboration; "vaccine-escape cross-validation" → "single-anchor audit (HIV-1 primary)"; Code Availability added dissertation-v1 tag + 30d Zenodo timeline
- **P3 (M1/M3/M4)**: ω² CI → "11-pathogen cluster-bootstrap 95% interval" (6 sites); 4-feature 97.6% qualified (12-pathogen Stage 3 EqualWeight LOPO top-10%, numerical not statistical)
- **P4 (M6/M7/C2)**: Layer A curation-protocol heterogeneity caveat at ch4:490; RF 5-fold CV spatial autocorrelation footnote at ch4:685; CSV provenance manifest paragraph in ch6 Code Availability
- **P5 (o3/o4/o5)**: ch5 "Optimality ceiling vs robust default floor" paragraph; ch2 DCA single-position biological-realism caveat; ch6 Dual-use considerations paragraph
- **P6**: easy-guide synced on LOPO framing + ω² CI qualifier (5 sites)

## Three-part mission

### Part A: Regression check (did the patches hold?)

For each patch category above:
1. Verify the replacement text is present, coherent, and propagated everywhere it needed to go
2. Flag any **new** internal contradictions the patches introduced (e.g., did the "cluster-bootstrap 95% interval" phrasing end up inconsistent between abstract, ch1, ch4, and ch6?)
3. Flag any **incomplete** propagation (e.g., if Claude fixed ch6:22 but left the same overclaim in ch5 or an unchanged easy-guide line)
4. Flag any **new** overclaim, under-claim, or awkward phrasing introduced by the patch language itself

Output format under `## Part A: Regression check`:
- `[A.P1-ok]` / `[A.P1-partial]` / `[A.P1-regression]` — one line per patch family, with file:line evidence.

### Part B: Depth areas Round 1 could not reach

Do NOT re-report Round 1 findings. Report only what is new in these categories.

**B.1 CSV ↔ table cell verification.** Pick at least the following tables and cross-check every cell against the listed CSV in `/proj/paper/results/`:
- `tab:stage2_anova` (ch4 §subsec:9pathogen_anova, now renamed) ↔ appropriate stage3_statistics CSV
- `tab:stage2_best` (11 pathogen best combos) ↔ `stage3_full_results.csv`
- `tab:rf_cv_auc` (11 pathogen Random Forest CV AUC) ↔ `feature_analysis/rf_cv_auc_v2.csv`
- `tab:vaccine_escape_stage3` ↔ `vaccine_escape_stage3.csv`
- Layer C / DMS subgroup tables ↔ `layer_c_evaluation.csv`
- Any other table whose caption explicitly cites a CSV filename

Report: mismatches (exact), rounding inconsistencies, off-by-one rows, missing columns, CSV entries that contradict the prose.

**B.2 Methods ↔ results reproducibility trace.** For a randomly-selected subset of Stage 2 and Stage 3 claims in ch4/ch5_adapt, trace the claim back to the methods definition in ch3. Flag:
- Parameter drift (e.g., ch3 says "5-fold CV, seed=42"; ch4 uses different value)
- Definitions used inconsistently across chapters (e.g., MCC computed differently in Stage 1 vs Stage 2)
- Any claim that ch3 does not cover at all (implicit methodology)

**B.3 Cross-chapter narrative coherence.** Read ch1 contributions → ch4 results → ch5 discussion → ch6 conclusion as a single arc. Flag:
- A finding in ch4 that ch5 doesn't discuss OR discusses with a different value
- A ch6 claim that ch5 does not support
- A ch1 promise that ch4 does not actually deliver
- "Optimality ceiling vs robust default floor" (new P5 paragraph) — does it actually resolve the Contribution 2 vs 3 tension, or did Claude just relabel the problem?

**B.4 Additional bibkey spot-check (30+ NEW keys, different from Round 1's).** Focus on:
- DMS data source citations (Lee 2018, Haddox 2018, Dadonaite 2023/2024, Bakhache 2025, Bloom lab 2026, Aditham 2025)
- Statistics methodology (Cameron/Gelbach/Miller 2008 cluster bootstrap; BCa bootstrap; Cohen 1988; Holm, Benjamini-Hochberg)
- Structural/PLM tools (AlphaFold2 Jumper 2021; ESM-2 Lin 2023; MAFFT Katoh; IQ-TREE; HyPhy FUBAR Murrell)

Report wrong year, wrong venue, wrong author list, or bibkey→text mismatches.

### Part C: Mock defense (three reviewer personas)

For each of the three hostile-but-fair reviewers below, list **exactly three opening questions** they would ask at defense, and for each question indicate whether the dissertation already answers it (citing file:line) or leaves it exposed.

**C.1 Statistician reviewer** (expects rigor on: variance decomposition, multiple testing, effect size, CI coverage)
- Example seed: "Your ω² = 0.296 is larger than any modeled main effect, but your residual is 0.39 — what prevents me from reading this as the interaction being *smaller* than unmodeled noise?"

**C.2 Virologist reviewer** (expects rigor on: biological validity, DMS data handling, escape vs drift distinction, ground truth construction)
- Example seed: "Your Layer A mixes convergent evolution, immune escape, and HVR membership. When you claim 'pathogen-dependent optimality,' how do we rule out that this is just curation-protocol-dependence?"

**C.3 Benchmark-paper reviewer** (expects rigor on: baseline selection, leakage audits, held-out splits, comparison fairness)
- Example seed: "You position against ViroGym/EVEREST as 'complementary task' — but you have no per-variant VEP baseline at all. Why isn't a binarized VEP top-k a fairer competitor?"

For each question:
- Quoted question (one sentence)
- Dissertation's defense (file:line + summary) OR "exposed — no direct answer"
- Your verdict: "defensible / partial / fails"

### Part D: Confidence delta

Round 1 concluded:
- Contribution 1: needs revision
- Contribution 2: defensible with revision
- Contribution 3a: needs revision
- Contribution 3b: needs revision
- Overall: needs 1-week revision

Your Round 2 verdict: state per-contribution change (improved / unchanged / worsened), and overall recommendation (ready to defend / 3-day polish / 1-week revision / >1-week revision).

## Output format

```
# Codex Round 2 Review — MutBench dissertation

## Part A: Regression check
- [A.P1-...] ...
- [A.P2-...] ...
...

## Part B: New findings (Round 1 did not catch)
### B.1 CSV ↔ table mismatches
### B.2 Methods ↔ results drift
### B.3 Cross-chapter incoherence
### B.4 Bibkey errors (beyond Round 1's list)

## Part C: Mock defense
### C.1 Statistician
- Q1: ... — Defense: ... — Verdict: ...
- Q2: ...
- Q3: ...
### C.2 Virologist
### C.3 Benchmark-paper reviewer

## Part D: Confidence delta vs Round 1
- Contribution 1: improved / unchanged / worsened (why, one line)
- Contribution 2: ...
- Contribution 3a: ...
- Contribution 3b: ...
- Overall recommendation: ready / 3-day / 1-week / >1-week

## Meta
- Files read: <count>
- CSV rows cross-checked: <count>
- Bibkeys newly verified: <count>
- Time spent: <rough>
- External lookups used: <list>
```

## Language
Write the report in Korean. Preserve English technical terms, citations, and quoted passages verbatim.

## Ground rules

- **Do not repeat Round 1 findings.** Read `review/2026-04-17/codex_verification_report.md` once to know what is already reported; then write only what is genuinely new.
- **Evidence before assertion.** Every claim needs a file:line or CSV:row reference.
- **No "seems / appears / might be"** without a specific citation.
- **If you can't verify, say so explicitly** — do not fabricate.
- **Adversarial posture.** Your job is to find remaining problems, not to validate. If the paper is now solid, the report should be short. If there are still shaky spots, be specific.
- **CSV is authoritative for Stage 2/3 numerics.** If prose and CSV disagree, CSV wins.
- Treat Parts A/B/C as a floor, not a ceiling. New categories are welcome — add them under Part B with a clear heading.

## Final deliverable

Write your full report to: `/proj/paper/paper/dissertation/review/2026-04-17/codex_round2_report.md`
(If the sandbox is read-only, reply with the full report as your final message — the runner will capture it via `-o`.)
Then echo the intended filepath as your last line.
