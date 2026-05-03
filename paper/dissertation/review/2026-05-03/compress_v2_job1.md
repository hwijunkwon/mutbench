# Compression-check v2 Job 1 -- abstract + ch1:1-100

Scope reviewed: `paper/dissertation/front_en/abstract.tex:1-34` and `paper/dissertation/chapters_en/ch1_introduction.tex:1-100`.

Already-applied items skipped: the abstract evidence ledger (`abstract.tex:10-27`) and the Ch1 panel-scope summary box (`ch1_introduction.tex:89-100`) match the do-not-recommend list.

## Candidate 1 -- Abstract component list

1. **Type**: consolidate-duplicate / trim-verbose
2. **Current length**: ~170 words; ~0.30 pp.
3. **What it currently does**: Defines the three MutBench components: Layer A/B/C ground truth, hotspot-score, and Stage 1/2/3 design.
4. **Compression strategy**: Retain the three components but remove parenthetical over-specification that is repeated in Ch1 Objective 1 and later chapters. Example after-state: "MutBench combines three elements: layered ground truth (literature positives, purifying-selection negatives, DMS validation), a recall-precision-stability hotspot-score, and a staged design covering SARS-CoV-2 depth, 11-pathogen breadth, and multi-source integration."
5. **Expected page saving**: 0.15-0.25 pp.
6. **Expected score impact**: neutral to lift. It preserves the defense architecture while reducing abstract density; the detailed Layer A composition remains available elsewhere.
7. **Risk**: low-medium. Layer A heterogeneity is a recurring examiner concern, so the compressed form should still signal that positives are literature-curated rather than homogeneous.

## Candidate 2 -- Abstract post-ledger result paragraphs

1. **Type**: consolidate-duplicate / move-detail-to-footnote
2. **Current length**: ~245 words; ~0.45 pp.
3. **What it currently does**: Adds feature-ablation, Layer A' sensitivity, H3N2/SARS-CoV-2 escape notes, 9 optimal information types, PLM collinearity, and the HIV-1 anchor after the main evidence ledger.
4. **Compression strategy**: Keep one synthesis paragraph after the ledger and move secondary statistics to chapter cross-references or footnotes. Example after-state: "Secondary audits bound deployment: the historical 4-feature core is statistically indistinguishable from the full ensemble, Layer A' sensitivity is negative, and non-HIV escape checks are secondary or exploratory. Across pathogens, nine scoring types become optimal, reinforcing pathogen-specific information choice."
5. **Expected page saving**: 0.25-0.40 pp.
6. **Expected score impact**: lift. The ledger already performs the main defense role; compressing the post-ledger audit trail makes the abstract read less like a results appendix while retaining the negative boundaries.
7. **Risk**: medium. The abstract uses these caveats to prevent overclaiming; do not delete the negative Layer A' and callability-adjacent boundary, only shorten it.

## Candidate 3 -- Ch1 background gap paragraphs

1. **Type**: consolidate-duplicate / merge-paragraphs
2. **Current length**: ~310 words; ~0.55 pp.
3. **What it currently does**: Explains frequency/entropy dominance, concurrent per-variant benchmarks, absence of region-level hotspot benchmarks, and surveillance platforms that do not evaluate information-source choice.
4. **Compression strategy**: Merge `ch1_introduction.tex:33-39` into one gap paragraph plus one compact comparator clause. Example after-state: "Hotspot methods still default to frequency or entropy, while contemporary resources such as ViroGym, EVEREST, ProteinGym, and EVEscape benchmark per-variant fitness or escape rather than region selection. Thus, no standard framework tests which biological information source works best for each pathogen."
5. **Expected page saving**: 0.25-0.40 pp.
6. **Expected score impact**: lift. This is the same argument repeated across three adjacent paragraphs; consolidation should sharpen novelty and reduce examiner fatigue.
7. **Risk**: low-medium. The named comparator list is useful for novelty, so keep the citations even if dataset counts move to a footnote.

## Candidate 4 -- Ch1 three-step pipeline exposition

1. **Type**: table-ize-prose / trim-verbose
2. **Current length**: ~255 words; ~0.45 pp.
3. **What it currently does**: Walks through sequence collection, computational analysis, experimental validation, validation cost, and the prioritization value of top-ranked hotspot candidates.
4. **Compression strategy**: Convert `ch1_introduction.tex:41-49` into a 3-row workflow table or compact list: step, role, relevance to MutBench. Example after-state: "Sequence collection produces MSAs; computational analysis ranks hotspot candidates; experimental validation tests selected positions. MutBench evaluates whether the computational filter concentrates biologically meaningful positions before costly laboratory validation."
5. **Expected page saving**: 0.25-0.35 pp.
6. **Expected score impact**: neutral to lift. The pipeline is helpful for non-specialists, but the current prose spends main-text space on database examples and sequencing-volume detail that are not central to the thesis claim.
7. **Risk**: low.

## Candidate 5 -- Ch1 problem-definition triad

1. **Type**: table-ize-prose / trim-verbose
2. **Current length**: ~245 words; ~0.40 pp.
3. **What it currently does**: States three problems: no standardized evaluation framework, no independent ground truth, and no statistical evidence for pathogen-dependent method choice.
4. **Compression strategy**: Replace `ch1_introduction.tex:59-73` with a compact problem table: problem, current limitation, MutBench response. Example after-state: "The gap is threefold: methods lack shared metrics, ground truth has not integrated independent evidence layers, and pathogen-specific algorithm selection has not been quantified."
5. **Expected page saving**: 0.20-0.35 pp.
6. **Expected score impact**: lift. A table would align the problems directly with the later objectives and reduce repeated definitions already covered by the glossary and background.
7. **Risk**: low-medium. Keep the algorithm-selection citation and at least one sentence explaining why pathogen-dependence is not merely parameter tuning.

## Triage note

Highest value in this chunk: Candidate 3 and Candidate 4. Candidate 3 improves novelty framing; Candidate 4 saves space without touching core evidence. Candidate 2 has the largest abstract saving but needs the most care because it carries anti-overclaiming caveats.

RESULT_COMPRESS_V2_J1: candidates=5 total_pages_saved=1.1-1.75 total_score_impact=+0.2
