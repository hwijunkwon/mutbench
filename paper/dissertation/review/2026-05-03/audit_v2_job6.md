# Audit v2 Job 6 -- ch3_methods.tex lines 301-600

Scope file actually audited: `paper/dissertation/chapters/ch3_methods.tex` lines 301-600 (the prompt path `chapters_en/ch3_methods.tex` is not present).

## Per-Paragraph Audit Table

| Lines | Numerical claims | Citations | Cross-refs | Consistency / recent-fix check | Severity |
|---|---|---|---|---|---|
| 301-311 | Formula constants `log2`, `100`, `+1`: method definition, no CSV expected. | None. | `eq:mutbench_hscore`, `eq:shannon_entropy` resolve locally. | Internally OK. | Verified |
| 313-319 | Decay formula and symbols only; no CSV expected. | None. | `eq:expand_cluster` resolves locally. | Internally OK. | Verified |
| 321-325 | `71--95%` range-loss and `641 vs. 637` detections are UNVERIFIED: not found in current CSVs; Ch4 table has `637/641` but no CSV provenance located. | None. | `subsec:improvements` resolves locally. | Historical Stage-1 claim plausible but lacks authoritative CSV path. | Minor |
| 327-334 | dN/dS `>1.0`, `<10 codons`: method thresholds, no result CSV expected. | `nei1986simple` is unresolved in `references.bib`; citation cannot compile/support. | None. | Methodologically plausible. | Major |
| 336-340 | `nt 21,563--25,384`, `3,822 nt`, `1,273 AA + stop`, `AA 319--541`, `3 codon positions`, `5'/3'-UTR`: genomic definitions, not in result CSV; consistent with SARS-CoV-2 Spike coordinates. | None. | None. | Internally OK. | Verified |
| 342-345 | `ins214EPE`, `69--70`, `Y144`: examples; no CSV expected. | None. | None. | **REGRESSION:** says H-score targets only single-nucleotide substitutions and indels are not processed. This conflicts with the requested post-v214 wording direction: "single-position scoring (gap-aware)", not broad "point/substitution-only" framing. | Major |
| 347-348 | dN/dS `<1`, `>1.0`: method interpretation, no CSV expected. | None. | None. | Internally OK. | Verified |
| 350-351 | `rho = 0.996` for Jukes-Cantor validation is UNVERIFIED; no authoritative CSV located. | None. | None. | Claim needs provenance. | Minor |
| 353-364 | `2D` feature space, `[0,Hmax]`: method definition; no CSV expected. | `campello2013hdbscan` exists and supports HDBSCAN. | None. | Internally OK. | Verified |
| 366-372 | Complexity `O(NM)`, `O(M log M)`, `O(k^2)`, `k≈800`, `M=3,822`, `N=10,000`, `~2 sec`: complexity formulas are definitional; runtime/`k` are UNVERIFIED (no runtime CSV/log path identified). | None. | None. | Runtime claim should cite benchmark log or be softened. | Minor |
| 374-378 | `min_cluster_size=5`, `min_samples=3`, median threshold: method parameters, no result CSV expected. | None. | None. | Internally OK. | Verified |
| 380-400 | `3` components; `100` subsamples; `80%` keep / `20%` zeroing; HDBSCAN-Auto `F1=0.146`, recall `0.944`, stability `0.788`: result numbers UNVERIFIED in current CSVs. Ch4 table has HDBSCAN-Auto F1 `0.146`, recall `0.944`, stability `0.788`, but no source CSV found under `results/mutbench/`. | None. | `eq:hotspot_score` resolves locally. | Historical Stage-1 values consistent with Ch4 but missing CSV provenance. | Minor |
| 402-422 | **DISCREPANCY:** says `9` scoring formulas. Current authoritative `results/mutbench/stage3_full_results.csv` has `20` scoring types; front abstract states `20`. Formula list also omits current features. | None. | `subsec:9pathogen_scoring` resolves locally; `eq:mutbench_hscore` resolves. | **REGRESSION / stale Korean text:** old 9-score framework. | Major |
| 424-457 | Alternative methods include `2024--2025`, `5%/10%/20%/median`, `epsilon=10^-6`, `F1`, enrichment, Cohen's d: method definitions. Current Stage 3 CSV does not contain these exact legacy methods as headline scoring set. | None. | `sec:temporal` resolves to Ch4 temporal section. | Mostly historical, but phrasing is stale relative to current 20-scoring Stage 3 design. | Minor |
| 459-464 | **DISCREPANCY:** says `14` families, `39` methods, and excludes `2` ensemble variants. Current `results/mutbench/stage3_full_results.csv` verifies `14` families and `39` detectors; older `combined_10scoring_results.csv` has `15` families including Ensemble and `39` detectors. Exclusion statement is stale/ambiguous. | None. | `subsec:9pathogen_detection` resolves locally. | Current headline should cite Stage 3 CSV and remove legacy ensemble explanation unless explicitly historical. | Major |
| 466-496 | Table totals `14` families, `39` variants are VERIFIED against `results/mutbench/stage3_full_results.csv`; parameter values partly DISCREPANT: table has ScoreDBSCAN eps `10,15`, Bayes prior `0.05,0.10`, SWAN `3x3` including `w=100`; current CSV uses ScoreDBSCAN `ep=8,15`, Bayes `0.15` appears, and current detector set differs. | None. | `tab:detection_families` resolves locally. | Caption says `9-pathogen`; current benchmark is `11` pathogens. **REGRESSION.** | Major |
| 498-500 | `39`, `14`, Wavelet `3` thresholds, FreqThresh `4` cuts are broadly VERIFIED by `stage3_full_results.csv` detector counts; `tab:detection_variants` resolves. | None. | `tab:detection_variants` resolves. | Old "single operating point" rationale OK, but tied to stale table. | Minor |
| 502-531 | Total `39` variants VERIFIED against `stage3_full_results.csv`; several parameter values DISCREPANT as above; table omits current scoring dimension (`20`). | None. | `tab:detection_variants` resolves. | Needs regeneration from current detector inventory. | Major |
| 533-563 | Prior-application table has no numeric results. | Several citation keys are unresolved in `references.bib`: `zhang2008chipseq`, `olshen2004cnv`, `sonesson2003cusum`, `satopaa2011kneedle`, `picard2011genomicseg`; existing keys `anastassiou2001genomic`, `tajima1989statistical`, `tokheim2016hotmaps`, `lawrence2013mutsigcv`, `mercatelli2020geographic`, `youn2025mutclust` plausibly support their rows. | `tab:detection_prior_apps` resolves. | Missing bibkeys are compile/provenance defects. | Major |
| 565-580 | `14` families into `5` categories: `14` and category count align with text; no CSV needed beyond detector inventory. | `youn2025mutclust` OK. | None. | Category descriptions plausible, but inherited stale parameter details from prior tables. | Minor |
| 582-600 | **DISCREPANCY / REGRESSION:** says "9-pathogen benchmark"; current `stage3_full_results.csv` has `11` pathogens and `8,580` evaluations. DMS `4` pathogens conflicts with current `layer_c_evaluation.csv`, which has `6` pathogens with Layer C rows. | None. | `sec:eval_stat_design_kr`, `subsec:9pathogen_metrics`, and `eq:mcc` resolve. | Metrics definitions are fine; scope/counts are stale. | Major |

## Per-Section Severity Counts

| Section | Critical | Major | Minor | Verified |
|---|---:|---:|---:|---:|
| MutClust definitions / variants, 301-378 | 0 | 2 | 3 | 6 |
| Hotspot-score, 380-400 | 0 | 0 | 1 | 0 |
| Scoring / detection methods, 402-580 | 0 | 6 | 3 | 0 |
| Evaluation metrics, 582-600 | 0 | 1 | 0 | 0 |

## Overall Severity Tally

Critical: 0  
Major: 9  
Minor: 7  
Verified: 6  
Regressions: 4

## Recent Fix Verification

In-scope regressions: line 342-345 uses old substitution-only framing; lines 409, 468, and 589 retain old 9-score / 9-pathogen framing. No in-scope paragraph mentions the old omega CI, HIV-1 Layer A `26/23`, Stage 1 `439` vs `417`, or D614G. Cross-scope scan still finds old D614G exclusion wording in Ch4 and old omega CI in `back/abstract_en.tex`, but those are outside this line-range audit.

RESULT_AUDIT_V2_J6: critical=0 major=9 minor=7 regression=4
