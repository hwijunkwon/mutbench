# Task: Adversarial verification of MutBench PhD dissertation

You are an independent external reviewer. Your job is to find problems I (and another AI, Claude) may have missed after 11 cycles of self-review. Be adversarial, not agreeable.

## Access
Working directory: /proj/paper/paper/dissertation/
Key files:
- front_en/abstract.tex              — English abstract (6 paragraphs)
- front/abstract_kr.tex               — Korean abstract
- chapters_en/ch1–ch6.tex            — English chapters (main body)
- chapters/ch1–ch6.tex                — Korean chapters (MAY BE STALE — see below)
- references.bib                      — ~260 entries after MOSD cleanup
- results/*.csv, results/*.json       — numerical outputs
- review/2026-04-17/*.md              — prior cycle reports (DO NOT just trust these)

Build: bash build.sh (xelatex 3-pass) — optional, do not modify.

## Core claims to verify (headline numbers)

1. 8,580 evaluations = 20 scoring × 39 detector × 11 pathogens
2. scoring×pathogen interaction ω²_modeled = 0.296 (CI 0.195–0.333); residual ω² ≈ 0.39
3. Friedman χ² = 7.69, p = 0.990 (no universally best combination)
4. LOPO 0/11 exact matches, oracle-vs-generalized MCC gap = 0.265
5. HIV-1 novel-only Fisher enrichment 7.16–8.24× on 37 Layer-A-disjoint positions (worst-case p = 5e-12)
6. H3N2 vaccine escape 4.012×, p = 0.0023 (but 69% Layer A overlap — self-consistency only)
7. SARS-CoV-2 7.63× enrichment (exploratory, post-Bonferroni)
8. 4-feature core captures ~98% (97.6%) of 10-feature ensemble
9. MutClust-Hybrid hotspot-score = 0.778 on SARS-CoV-2

## Required checks (Critical / Major / Minor — each with file:line evidence)

### A. Statistical validity
- Does the ω² interpretation correctly separate modeled vs residual variance? Is 0.296 the right denominator?
- Is LOPO 0/11 a meaningful negative result, or null-consistent under permutation? The paper claims the conclusion rests on interaction + HIV-1 audit, not LOPO alone — is that defensible?
- Bonferroni across how many tests? Is the family-wise correction applied consistently?
- Cluster bootstrap CI: are the clusters defined at the correct level (pathogen? scoring? replicate)?

### B. External literature coverage
Check whether these are cited AND correctly characterized:
- ViroGym (arXiv:2603.06740, Mar 2026) — concurrent fitness-regression benchmark
- EVEREST v3 — DMS benchmark
- ProteinGym v1.3 — 217 DMS, 70+ models
- PLANT (2025) — protein language model
- AlphaMissense — Google DeepMind pathogenicity predictor
- DCA (Direct Coupling Analysis) — coevolution baseline
- EVEscape — antibody escape prediction
- Weber 2019 — hotspot definitions

If present: is the framing correct (competitor vs complementary)? If absent: is that defensible or a gap?

### C. Bibkey and citation accuracy (spot-check 30+ bibkeys)
Prior cycle flagged:
- tong2024eva71 → should be Bakhache 2025 (VERIFY)
- simonich year (VERIFY)
- dadonaite2024h5 — correct?
- covfit2025 DOI — resolves?

Go beyond this list. Scan references.bib and grep `\cite{` — report any bibkey used in text but wrong author/year/venue.

### D. Korean-English consistency
The Korean chapters (chapters/ch*.tex) are suspected stale from before Cycle 6 reframing. Cross-check:
- Do Korean abstracts/chapters still say ω²=0.285 (old) vs 0.296 (new)?
- LOPO 0/9 (old) vs 0/11 (new)?
- "9 pathogens" (old) vs "11 pathogens" (new)?
- HIV-1 primary framing present in Korean too?

### E. Tables and figures
- Table 4.3, 4.9, 4.13 — do numbers match the CSVs in results/?
- Figure 1.1 — caption vs content consistency
- Any table with implausibly narrow or wide ranges?
- Figure captions vs in-text references — mismatches?

### F. Overclaiming and selective reporting
- HIV-1 framing: is "primary anchor" defensible given only 3/11 pathogens have vaccine-escape audits? Or is this post-hoc selection?
- "≈98% of 10-feature ensemble" — what metric? On what split? Is the gap statistically non-significant or just numerically small?
- Any headline number without a confidence interval or significance test where one is warranted?
- Negative results properly reported, or only wins highlighted?

### G. Logical gaps
- Contribution 3 (multi-source integration): is the causal claim "integration → better hotspot detection" supported, or merely correlational?
- Layer B (negative controls under purifying selection) — is the null properly defined?
- Does the paper distinguish "pathogen-dependent optimality" (interesting) from "no method generalizes" (trivial)?

### H. Reproducibility
- Are seeds documented?
- Are data splits (train/test/LOPO folds) specified?
- Code availability statement present?
- DMS data source citations complete?

### I. Out-of-frame analysis (MOST IMPORTANT)

The checks A–H above are categories *I* defined. Your highest-value contribution is
finding problems that fall OUTSIDE these categories. Explicitly consider:

1. **Framing / problem formulation**
   - Is "region-level hotspot detection" the right problem to benchmark, or is it a contrived framing that avoids the harder per-variant prediction task?
   - Does the three-layer ground truth (convergent / conserved / DMS) have internal contradictions the author didn't notice?
   - Is the dichotomy "information source × detector" the right decomposition, or does it hide confounds (e.g., scoring scale vs detector threshold)?

2. **Discipline-specific red flags I may not know**
   - Virology / molecular evolution norms: what would a reviewer from Nat. Methods or Virus Evolution flag that a CS-trained reviewer would miss?
   - Statistical genetics norms: multiple-testing conventions, effect-size reporting standards, fairness-of-comparison expectations.
   - Benchmark paper conventions: leakage audits, held-out pathogens, baseline selection, hyperparameter tuning fairness.

3. **Omissions (what is NOT in the paper but should be)**
   - Missing baselines (random predictor? frequency-only?)
   - Missing ablations
   - Missing failure mode analysis — which pathogens / scorings failed and why?
   - Missing limitations section depth
   - Missing ethics / dual-use considerations for pathogen research
   - Missing compute cost / accessibility discussion

4. **Meta-claim integrity**
   - Does the paper's narrative arc (problem → gap → contribution → evidence) have a weak link that Cycle 11 self-review couldn't see from inside?
   - Are any of the three contributions actually restatements of the same finding? (i.e., are they genuinely three?)
   - Is "pathogen-dependent optimality" a discovery or a tautology given the way ground truth is constructed?

5. **Adversarial reading — imagine a hostile reviewer**
   - If reviewer #2 wanted to reject this paper, what would they attack first?
   - What single experiment, if it failed, would collapse the main claim?
   - Is there a way to read the paper where contribution 3 undermines contribution 2 (or vice versa)?

6. **Anything else that strikes you as wrong, weak, or worth flagging** — including things you cannot neatly categorize. Use a "Misc" section if needed. Do not suppress a concern just because it does not fit a heading.

Report these findings under a dedicated section:
## Out-of-frame findings (things Claude's review structure could not have caught)

## Output format

Produce a single Markdown report:

# Codex Independent Review — MutBench dissertation

## Critical (fix before submission)
- [C1] <title> — file:line — <finding> — <evidence> — <suggested fix>
- ...

## Major (should fix)
- [M1] ...

## Minor (polish)
- [m1] ...

## Out-of-frame findings (things Claude's review structure could not have caught)
- ...

## What Claude's Cycle 11 review missed (your unique findings)
- ...

## Confidence assessment
- Per-contribution (1, 2, 3a, 3b): defensible / needs revision / overclaimed
- Overall: ready to defend / needs 1-week revision / needs 1-month revision

## Meta
- Files read: <count>
- Numbers spot-checked against CSVs: <count>
- Bibkeys verified: <count>
- Time spent: <rough estimate>

## Language
Write the report in Korean. Preserve English technical terms, citations, and quoted passages verbatim.

## Ground rules
- Evidence before assertion. No "seems", "appears", "might be" without a specific file:line reference.
- Do not trust prior cycle reports (review/2026-04-17/*.md) — treat them as hypotheses to verify, not facts.
- If you cannot verify a claim from the files alone, say so explicitly — do not fabricate.
- Adversarial posture: your job is to find problems, not to validate. If the paper is solid, the report should be short. If it's shaky, be specific about where.
- Treat the category list (A–I) as a floor, not a ceiling. If a problem doesn't fit any category, create a new one — do not force-fit or skip it.

## Final deliverable
Write your full report to: /proj/paper/paper/dissertation/review/2026-04-17/codex_verification_report.md
Then echo the filepath as your final line.
