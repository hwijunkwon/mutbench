# Compression-check v2 Job 4 -- ch2:151-299

Scope reviewed: `paper/dissertation/chapters_en/ch2_background.tex:151-299`.

## Candidate 1: Surveillance platform prose as role table

1. **Type:** table-ize-prose
2. **Current length:** ~185 words / ~0.35 pp (`ch2_background.tex:170-185`)
3. **What it currently does:** Explains Nextstrain, PANGO, GISAID, and outbreak.info, then repeatedly distinguishes lineage surveillance/data repositories from position-level hotspot benchmarking.
4. **Compression strategy:** Replace the prose blocks with a compact table: platform/resource, primary unit, role in surveillance, why it is not a hotspot benchmark. Example after-state: "Surveillance resources provide lineage tracking or raw prevalence data; MutBench instead evaluates position-level detection methods under shared labels and metrics."
5. **Expected page saving:** 0.25-0.40 pp
6. **Expected score impact:** lift. The table would make the operational distinction immediately inspectable and reduce repeated "not detection / not benchmarking" phrasing without weakening novelty.
7. **Risk:** low. Preserve the short-horizon Bedford forecasting caveat as a table note or parenthetical so the claim remains about primary function, not absolute exclusion.

## Candidate 2: Feature-importance prior work as evidence ledger

1. **Type:** table-ize-prose
2. **Current length:** ~310 words / ~0.55 pp (`ch2_background.tex:190-208`)
3. **What it currently does:** Summarizes Maher, Rodriguez-Rivas, Hie, and EVEscape, then states that none performs cross-pathogen feature-importance comparison.
4. **Compression strategy:** Use a 4-row ledger with columns: study, feature class, main finding, MutBench boundary. Keep one synthesis sentence after the table. Example after-state: "These studies show that epidemiological, epistatic, PLM-semantic, and integrated fitness/structure signals can matter, but each leaves cross-pathogen information-type optimality untested."
5. **Expected page saving:** 0.30-0.50 pp
6. **Expected score impact:** lift. The cited studies become easier to compare, and the final gap claim becomes more persuasive because the missing axis is explicit row by row.
7. **Risk:** low-medium. The Rodriguez-Rivas epistasis limitation is substantively important; keep the "single-position regime" boundary either as one table row note or a short follow-on sentence.

## Candidate 3: Epistasis boundary duplicated in prior-work paragraph and summary

1. **Type:** consolidate-duplicate
2. **Current length:** ~190 words / ~0.30 pp across `ch2_background.tex:198` and `ch2_background.tex:298`
3. **What it currently does:** Twice states that DCA/EVcouplings/GREMLIN-style coupling methods are outside MutBench and that Stage 2/3 conclusions apply only within a single-position scoring regime.
4. **Compression strategy:** Keep the full caveat at first mention in the feature-importance subsection, then reduce the summary to one clause. Example after-state: "As noted above, coupling-aware hotspot detection remains future work; Chapter 3 therefore presents MutBench as a single-position benchmark."
5. **Expected page saving:** 0.10-0.20 pp
6. **Expected score impact:** neutral to lift. The caveat remains visible but stops reading like a repeated defense disclaimer at the chapter close.
7. **Risk:** low. The first occurrence must retain the biological-realism boundary, because that is the load-bearing version.

## Candidate 4: Algorithm-selection and benchmarking-principles caveat block

1. **Type:** table-ize-prose
2. **Current length:** ~360 words / ~0.65 pp (`ch2_background.tex:213-228`)
3. **What it currently does:** Introduces Rice's algorithm-selection framing, No Free Lunch, meta-learning/AutoML, neutral benchmarking principles, and then a long MutClust self-assessment-bias mitigation caveat.
4. **Compression strategy:** Split into two compact tables or one two-part ledger: theory frame -> MutBench mapping; benchmarking risk -> mitigation. Example after-state: "Rice/NFL justify pathogen-specific pipeline choice; Weber/Boulesteix define the audit contract. MutBench partly violates independence through MutClust, mitigated by identical pipelines, independent labels, and frozen Stage 2 hyperparameters."
5. **Expected page saving:** 0.35-0.60 pp
6. **Expected score impact:** lift. The current paragraph has strong defense content but buries the core argument; a mitigation ledger would make the partial self-assessment exception more transparent and less apologetic.
7. **Risk:** medium. The table must preserve that the bias risk is mitigated, not eliminated, and should not overstate compliance with Weber's independence criterion.

## Candidate 5: Benchmarking-gap list absorbed into comparison table

1. **Type:** table-ize-prose
2. **Current length:** ~520 words / ~0.85 pp (`ch2_background.tex:233-260`, table at `ch2_background.tex:262-282`)
3. **What it currently does:** Lists adjacent benchmarks and tools in prose, then repeats many task/scope distinctions in `tab:benchmark_comparison`.
4. **Compression strategy:** Add a "Why insufficient for viral hotspot detection" column to the existing table and reduce the prose list to a short setup plus post-table synthesis. Example after-state: "Adjacent VEP and cancer benchmarks standardize prediction or driver discovery, but none evaluates viral per-region hotspot detectors under shared ground truth."
5. **Expected page saving:** 0.40-0.65 pp
6. **Expected score impact:** lift. This is the closest in-scope analogue to the audit-ledger pattern: it shortens the section while making novelty, task boundary, and comparator status easier to grade.
7. **Risk:** low-medium. The table is already width-constrained; adding a column may require `tabularx`, smaller phrasing, or splitting into two table blocks.

RESULT_COMPRESS_V2_J4: candidates=5 total_pages_saved=1.4-2.35 total_score_impact=+0.4
