# Compression-check v2 Job 6 — ch3:301-600

Scope reviewed: `chapters_en/ch3_methods.tex`, lines 301-600. Already-done items were checked conceptually; none of the candidates below re-recommend the listed completed compressions.

## Candidate 1 — Ground-truth caveat block after Table 3.x

1. **Type**: table-ize-prose
2. **Current length**: ~185 words / ~0.35 pp (lines 314-325)
3. **What it currently does**: Explains three separate caveats after the 3-layer ground-truth table: HCV coordinate handling, HIV-1 Layer A count reconciliation, and inclusion of pathogens lacking Layer C.
4. **Compression strategy**: Convert the prose block into a compact "Ground-truth caveats and operational handling" table with columns `Issue`, `Operational choice`, `Where sensitivity/limitation is handled`.
   Example after-state: "HCV Layer B: HVR1/HVR2 mapped; CD81 regions not high-confidence in E2 alignment, so Layer B=0; HCV-exclusion sensitivity reported in Chapter 4."
5. **Expected page saving**: 0.25-0.35 pp
6. **Expected score impact**: lift. A ledger-style table should improve examiner confidence because the operational consequences become auditable instead of buried in footnote prose.
7. **Risk**: low

## Candidate 2 — Synthetic benchmark protocol prose

1. **Type**: trim-verbose
2. **Current length**: ~145 words / ~0.25 pp (lines 361-367)
3. **What it currently does**: Defines the Stage 1 synthetic signal-recovery test, including score ranges, seed positions, genome size, and the caveat that biological validation still comes from DMS and convergent evolution.
4. **Compression strategy**: Keep the design essentials in one compact paragraph and move the exact uniform distributions into a parenthetical or short protocol sentence.
   Example after-state: "Synthetic H-scores were generated on one 29,903-position genome per trial, with high scores at CCM seeds (484/501/417/452), moderate scores within +/-50 AA, and low background noise. Because truth is injected by design, this tests signal recovery, not biological validity; DMS and convergent-evolution references provide the real-data checks."
5. **Expected page saving**: 0.10-0.20 pp
6. **Expected score impact**: neutral to slight lift. No methodological content is lost, and the limitation remains explicit.
7. **Risk**: low

## Candidate 3 — MutClust formula and variant paragraph

1. **Type**: consolidate-duplicate
2. **Current length**: ~190 words plus two displayed equations / ~0.45 pp (lines 412-423)
3. **What it currently does**: Introduces MutClust, restates H-score and entropy inline, gives DBSCAN/HDBSCAN parameters, then repeats H-score and entropy as displayed equations before describing five variants and Stage 2 retention of v1.
4. **Compression strategy**: Remove inline formula duplication and separate "scoring definition" from "variant disposition" in two shorter paragraphs; keep the displayed equations as the authoritative definitions.
   Example after-state: "MutClust is the only virus-specific hotspot tool in the benchmark. We use its H-score and entropy definitions in Eqs. X-Y, followed by adaptive DBSCAN with gamma=0.5; sensitivity over gamma in {0.25,0.5,1.0} changed MCC by +/-0.01."
5. **Expected page saving**: 0.20-0.35 pp
6. **Expected score impact**: lift. The current sentence is overloaded and visually hard to parse; reducing duplication should improve method readability while preserving reproducibility details.
7. **Risk**: low

## Candidate 4 — Orthogonal SARS-CoV-2 validation protocols

1. **Type**: table-ize-prose
2. **Current length**: ~285 words / ~0.55 pp (lines 474-480)
3. **What it currently does**: Describes three validation analyses: 3D contact enrichment, coalescent founder-vs-convergence simulation, and TreeTime ML homoplasy audit.
4. **Compression strategy**: Replace the three dense paragraphs with a protocol table: `Validation`, `Input`, `Null/comparator`, `Reported statistic`, `Scope`.
   Example after-state: "3D contact enrichment | PDB 6VSB C-alpha contacts <=8 A | 1,000 shuffled hotspot labels | observed/expected contact ratio and z statistic | SARS-CoV-2 only."
5. **Expected page saving**: 0.40-0.60 pp
6. **Expected score impact**: lift. The table would make the orthogonal validation design easier to audit and parallels the successful audit-ledger pattern without duplicating prior ch4/ch5 compressions.
7. **Risk**: medium. Some implementation parameters, especially TreeTime flags, may need a concise footnote or supplementary-method pointer to avoid perceived loss of reproducibility.

## Candidate 5 — H3N2 prospective pilot mega-paragraph

1. **Type**: table-ize-prose
2. **Current length**: ~250 words / ~0.50 pp (line 485)
3. **What it currently does**: Defines the H3N2 time-stratified pilot: raw 9,000-sequence input, three 5-year windows, frequency-only training, retrospective and prospective references, emergence thresholds, top-k overlap, and Fisher exact testing.
4. **Compression strategy**: Convert the single paragraph into a compact protocol box/table with fields `Dataset`, `Windows`, `Training signal`, `Reference sets`, `Emergence rule`, `Evaluation`, `Interpretation`.
   Example after-state: "Emergence rule: a position is prospective if training frequency <5% and holdout frequency >=10%. Evaluation: top-k overlap for k=20/30/50; one-sided Fisher exact test on detected vs reference positions."
5. **Expected page saving**: 0.35-0.55 pp
6. **Expected score impact**: lift. The current paragraph hides the design logic; a protocol table would read as a deliberate audit rather than an appended caveat.
7. **Risk**: low to medium. The raw-vs-deduplicated distinction must remain explicit because it defends the pilot's prevalence interpretation.

## Total

Estimated non-overlapping saving: **1.3-2.1 pp**. Conservative planning estimate: **1.7 pp**.

Expected aggregate score impact: **+0.3**. The largest likely benefit is readability and examiner trust: caveats and audit protocols become inspectable without weakening the methodological record.

RESULT_COMPRESS_V2_J6: candidates=5 total_pages_saved=1.7 total_score_impact=+0.3
