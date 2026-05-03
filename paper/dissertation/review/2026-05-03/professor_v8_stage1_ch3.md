# Chapter Deep Eval: ch3_methods

## In-scope rubric items
- C
- D
- H

## Per-item evidence

### C
**Strongest evidence**:
- Clear end-to-end methodological contract: "ground truth construction from three independent biological evidence sources", "systematic scoring and detection via 20 scoring types and 14 detection method families", and "multi-metric evaluation with factorial statistical analysis" (lines 81--82).
- Strong label/metric separation: Layer A "defines true positives for MCC", Layer B "defines constrained negatives for constrained FPR", and Layer C "provides experimental validation" (lines 186--187; table roles lines 201--205). The A/C conflict rule is unusually mature: "no single universal `hotspot' label is asserted" and each operationalization is evaluated independently (lines 277--282).
- The statistical design is specific and auditable: the ANOVA grid and thresholds were "frozen in the project SOP" before Stage 1, with "No post-hoc adjustment" after observing Stage 2 MCC results (line 221); the ANOVA also distinguishes the 8,580-row evaluation panel from the 3,080-cell family grid and explains residual dependence (lines 764--768).

**Weakest evidence / gaps**:
- Some method descriptions are still over-compressed relative to their importance. For example, "Random subsamples at 25%, 50%, 75%, and 100% of MSA sequences are drawn" gives no replicate count, stratification rule, or whether alignments/scoring are recomputed from scratch (line 818).
- Several important choices are acknowledged but not fully ablated in this chapter: MAFFT `--auto` effects were "not separately ablated" (line 39), Rabies/EV-A71 DMS threshold sweeps are deferred (line 242), Tranception/ESM-2 merged-channel sensitivity is deferred (line 586), and Foldseek/DALI structural QC is deferred (line 552).

**Hidden issues for panel awareness**:
- A subtle anchor-preservation issue remains around deployability framing. The chapter mostly supports retrospective benchmarking, but line 435 says the Stage 1 stability metric reflects "the practical requirement that methods in viral surveillance should produce consistent results", and line 485 says the H3N2 pilot was raised in connection with "benchmark deployability." These phrases may nudge readers toward detector/deployment expectations even though the revised dissertation frames MutBench as wet-lab triage.
- The "Tranception" channel is not actually Tranception: it is an "ESM-2 masked-marginal pseudo-perplexity" proxy (lines 583--586). The caveat is transparent, but panelists may treat the 20 scoring types as more independent than they are; the chapter itself says variance is partly double-counted for 11 of 12 pathogens (line 586).
- The Method chapter reports result-like quantities inside methods, e.g., MutClust-Hybrid "achieves the highest hotspot-score" (line 423), detection family contributes only omega^2 = 0.013 (line 678), and several ANOVA/robustness outcomes (lines 768--775, 809--810). This helps rigor, but it blurs methods/results boundaries.

**Suggested score range**: 8.0--8.8

### D
**Strongest evidence**:
- The scale is explicit and substantial: "11 RNA viruses", "20 scoring types", "14 detection method families", "39 parameter variants", and "3-layer ground truth" (lines 5--7). Stage 2 is quantified as "20 scoring types x 39 detection parameter variants x 11 pathogens = 8,580 combinations" (lines 491--492).
- Breadth is biologically diverse rather than only computational: the chapter covers respiratory, blood-borne/STI, enteric, arthropod-borne, and neurotropic viruses, with alignment lengths from 261 to 1,330 AA and substitution-rate/evolutionary-regime diversity (lines 21--29).
- The table-level evidence is strong: sequence counts range from 1,311 to 5,325 total sequences and 530 to 5,019 unique sequences (Table, lines 52--64); Layer A/B/C counts are enumerated for all pathogens, including six with all three layers (lines 286--326).

**Weakest evidence / gaps**:
- The pathogen panel is broad but not exhaustive, and the chapter admits this: "diverse but non-exhaustive range of RNA-virus surface-glycoprotein evolutionary regimes" (line 29). It is still one protein class/regime, not a whole-virus or all-viral-protein benchmark.
- Ground-truth depth is uneven. Five pathogens lack DMS Layer C (lines 320--323), HCV has effective Layer B = 0 because coordinate mapping was not high-confidence (lines 304, 314), and Layer A positive rates range from 0.7% to 15.9% (lines 712--713), making "scale" heterogeneous in label quality.

**Hidden issues for panel awareness**:
- There is a micro-inconsistency in temporal coverage: Table 3 design characteristics lists SARS-CoV-2 and MERS at "~5 yr" (lines 697, 704), but the prose says temporal coverage is "~2--50 years" (line 712). This is small but visible to a detail reader.
- The chapter has legacy labels `sec:9pathogen_benchmark`, `subsec:9pathogen_data`, and `subsec:9pathogen_metrics` even though the text now says 11 pathogens (lines 12, 19, 725). These do not affect results but are anchor-preservation artifacts that can make the revision look mechanically patched.
- Zika is excluded from Stage 2 but appears repeatedly in Stage 3/structure contexts (lines 30, 574, 579, 863). The text is transparent, but a bulk reader may overcount the headline benchmark as 12 pathogens unless they track which analysis is 11 vs 12.

**Suggested score range**: 8.2--9.0

### H
**Strongest evidence**:
- The chapter is well organized: the opening roadmap names Materials, Methods, framework overview, ground truth, Stage 1, Stage 2, and evaluation/statistical design in order (lines 5--11). Sectioning is easy to follow despite the dense content.
- Tables and captions do real work. The dataset table caption explains query date and MAFFT mode (lines 44--70), DMS preprocessing records phenotype/assay/replicates/source (lines 246--268), and detector families list categories and parameter values with reproduction anchors (lines 641--674).
- The writing often anticipates reviewer confusion: it distinguishes Layer A/B/C conflicts (lines 271--282), production vs nested-LOPO EqualWeight variants (lines 627--632), pLDDT vs SASA structure sources (lines 551--556), and evaluation-level vs cell-level omega^2 (line 768).

**Weakest evidence / gaps**:
- Density is high. Some lines are paragraph-sized method ledgers, especially GenBank/MAFFT/deduplication (line 37), Layer A preregistration (line 221), structural-source caveats (lines 551--552), and EqualWeight variants (lines 627--632). Detail is valuable, but readability suffers.
- Some language is too strong or too absolute for a methods chapter. Examples: "arithmetically identical" SHA-256 vs CD-HIT/MMseqs2 at 100% identity (line 37), "every possible single amino acid substitution" for DMS (line 241), and "any mutation here is lethal or severely deleterious" for Layer B (line 228). These are directionally understandable but vulnerable to nitpicking.

**Hidden issues for panel awareness**:
- The chapter title is "Materials and Method" (line 2), singular "Method"; most dissertations use "Materials and Methods." Minor, but it is a first-page polish issue.
- A table cross-reference appears mismatched: the H3N2 pilot cites "Table~\\ref{tab:design_characteristics}" for the 2,562 unique-sequence Stage 2 panel (line 485), but that table is introduced later (lines 688--710). LaTeX can resolve it, yet reading flow is slightly backward.
- Several phrases still carry legacy "hotspot detection" and "surveillance" language (lines 5, 435, 755), while the recent global framing is "wet-lab triage tool, not deployable detector." This chapter helps the triage framing through MCC/false-positive cost language, but it does not consistently use the new frame.

**Suggested score range**: 7.6--8.5

## Cross-cutting observations

- The chapter actively HELPS panel-level interpretation for C and D because it makes the benchmark contract auditable: frozen thresholds/grid, explicit layer roles, full panel dimensions, and several robustness caveats are present in-method rather than hidden in later chapters.
- The chapter slightly HURTS panel-level interpretation for H if professors expect clean narrative separation. It has many result values embedded in the methods chapter and several long caveat paragraphs that read like audit memos rather than dissertation prose.
- The most important subtle methodological risk is not a missing method, but over-independence: detector variants are dependent within family, PLM channels are correlated, pathogens are only 11 clusters, and label definitions differ by pathogen. The chapter generally acknowledges all four, which should raise rather than lower confidence, but the panel should score strictness based on whether acknowledgement plus deferred sensitivity is enough.

## Bottom line for Stage 2 panel

Bulk-read panelists may remember Chapter 3 as simply "large benchmark methods." The detail-aware reading is stronger and more nuanced: the chapter has a genuinely mature methodological scaffold, with preregistered thresholds, explicit layer separation, a broad 8,580-cell panel, and unusually candid dependence/caveat handling. The hidden weaknesses are revision-polish and interpretation risks: legacy 9-pathogen labels, a few deployability/surveillance phrases, result-heavy methods prose, uneven Layer C/B coverage, and partially redundant AI scoring channels. These should not erase the chapter's methodological strength, but they should keep C/H below a perfect score.

RESULT_PROF_V8_STAGE1_ch3: in_scope_items=3 hidden_issues=9 recommended_score_floor=7.6 recommended_score_ceiling=9.0
