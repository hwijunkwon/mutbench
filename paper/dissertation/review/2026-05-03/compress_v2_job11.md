# Compression-check v2 Job 11 -- ch5:1-150

Scope: `paper/dissertation/chapters_en/ch5_discussion.tex` lines 1--150.

Skipped as already-applied: lines 21--49 (`tab:layer_a_provenance` and Layer A curation-reproducibility limitations) overlap the listed "Layer A provenance summary table" and "Layer A curation-reproducibility limitations paragraph in ch5" items.

## Candidate 1 -- circularity audit prose into compact audit row

1. **Type:** table-ize-prose
2. **Current length:** ~330 words; ~0.6--0.8 pp
3. **What it currently does:** Lines 17--19 distinguish ground-truth circularity from feature-feature redundancy, list pathogen-specific correlations, add D614G/476 examples, and state the interpretive discount for frequency-best pathogens.
4. **Compression strategy:** Convert the long audit explanation into a 4-column mini-table: audit, result, affected pathogens, interpretation. Example after-state: "Layer A--frequency audit: mean $|\rho|=0.12$; moderate coupling only in HCV, Influenza B, Norovirus; frequency-best claims for those pathogens carry a structural discount; HIV-1 escape remains the cleanest external anchor."
5. **Expected page saving:** 0.3--0.5 pp
6. **Expected score impact:** lift. The current text is defensively useful but hard to scan; an audit-row format preserves the caveat and makes the circularity discount more examiner-visible.
7. **Risk:** low-medium. Must preserve the distinction between Layer A-vs-frequency circularity and frequency-vs-entropy feature redundancy.

## Candidate 2 -- H-score saturation and homoplasy alternative consolidation

1. **Type:** merge-paragraphs
2. **Current length:** ~210 words; ~0.4--0.5 pp
3. **What it currently does:** Lines 58--60 explain H-score saturation, TC-freq as a temporal-contrast alternative, DMS-vs-convergent mismatch, and homoplasy's founder-bias correction with pathogen-specific failures.
4. **Compression strategy:** Merge into one "metric alternatives" paragraph with three clauses: saturation problem, two alternatives, boundary. Example after-state: "Late-pandemic H-scores saturate, motivating TC-freq and homoplasy as complements: TC-freq retains $3.43\times$ enrichment, while homoplasy separates D614G-like founder events from independent origins. Neither is universal; HCV parsimony saturation mirrors the scoring-by-pathogen interaction."
5. **Expected page saving:** 0.1--0.2 pp
6. **Expected score impact:** neutral to slight lift. It reduces narrative repetition without weakening the methodological boundary.
7. **Risk:** low. The exact HIV-1/H3N2/HCV AUC details can be retained in Ch4 or a supporting table if needed.

## Candidate 3 -- cross-pathogen implications into one theorem/evidence paragraph

1. **Type:** trim-verbose
2. **Current length:** ~270 words; ~0.5--0.7 pp
3. **What it currently does:** Lines 69--76 restate no universal method, give two pathogen examples, quantify the scoring-vs-detector asymmetry, invoke Rice/No-Free-Lunch, cite LOPO/Friedman/oracle-gap nulls, add ESM-2 examples, and position against EVEREST/ProteinGym.
4. **Compression strategy:** Keep the variance-component result as the load-bearing sentence, then fold theory and prior-work positioning into one sentence. Example after-state: "The key result is not that detectors are useless, but that scoring choice dominates detector choice: detector-family $\omega^2=0.013$ versus scoring$\times$pathogen $\omega^2=0.296$. This realizes an algorithm-selection/No-Free-Lunch setting at too-small $n=11$, distinct from per-variant fitness benchmarks."
5. **Expected page saving:** 0.2--0.4 pp
6. **Expected score impact:** lift. The after-state would sharpen the contribution and reduce the feeling that Ch5 re-argues Ch4.
7. **Risk:** low. Keep at least one concrete pathogen example or the ESM-2 cross-paradigm sentence if the examiner needs biological grounding.

## Candidate 4 -- recall analysis as "miss class / implication" table

1. **Type:** table-ize-prose
2. **Current length:** ~190 words; ~0.4--0.5 pp
3. **What it currently does:** Line 120 compresses mean recall, three interpretive observations, H3N2 and SARS-CoV-2 examples, region-window rescue, and EV-A71/Rabies residual risk into one dense paragraph.
4. **Compression strategy:** Use a 3-row table: missed-position class, evidence, operational implication. Example after-state: "Low-recall positions cluster in minimum-lineage or epistatic sites; integration recovers some single-feature misses; windowed MCC shows most misses are local. EV-A71/Rabies remain subset-prioritization cases because short alignments limit power."
5. **Expected page saving:** 0.2--0.3 pp
6. **Expected score impact:** lift. This is a strong defense answer currently hidden in a single long sentence; table form improves readability while retaining caveats.
7. **Risk:** low-medium. Avoid implying region-window MCC is the same estimand as exact-position recall.

## Candidate 5 -- merge duplicate vaccine-escape validation blocks

1. **Type:** consolidate-duplicate
2. **Current length:** ~430 words; ~0.8--1.0 pp
3. **What it currently does:** Lines 131--135 summarize vaccine-escape enrichment, Bonferroni survival, HIV-1/H3N2/SARS-CoV-2 independence, EqualWeight-vs-single comparability, practical search-space value, and Stage 1 historical status; lines 141--149 then repeat the independence tiering.
4. **Compression strategy:** Replace both blocks with one concise evidence-tier table plus a short note on EqualWeight comparability. Example after-state: "Escape validation is partial: HIV-1 is the external anchor, H3N2 is self-consistency, SARS-CoV-2 exploratory. EqualWeight H3N2 $4.012\times$ is a fixed-protocol search-space estimate, not directly comparable to Stage 2 winners."
5. **Expected page saving:** 0.4--0.7 pp
6. **Expected score impact:** lift. This preserves Contribution 3 while removing repeated caveat prose; it should improve the defense posture because the independence hierarchy becomes visually explicit.
7. **Risk:** medium. The HIV-1 anchor, H3N2 overlap caveat, SARS-CoV-2 correction failure, and winner's-curse distinction must all survive.

RESULT_COMPRESS_V2_J11: candidates=5 total_pages_saved=1.2 total_score_impact=+0.3
