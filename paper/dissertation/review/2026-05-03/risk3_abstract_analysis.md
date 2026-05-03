# Risk 3 Abstract Reframe Analysis

## 1. Anchor preservation table

| Anchor | In current abstract | In new draft | Verdict |
|---|---:|---:|---|
| 11 pathogens, 20 scoring x 14 detection x 39 variants = 8,580 evaluations | Yes: opening sentence and evidence ledger context. | Partial: says panel size n=11, but drops the full benchmark grid and 8,580 count. | Not preserved as a numerical anchor. |
| omega^2 = 0.296, CI [0.201, 0.346] | Yes: ledger and later text. | Yes: exact value and CI retained. | Preserved. |
| HIV-1 7.19x, p_adj = 2.5 x 10^-16 | Yes: ledger and body text. | Partial: 7.19x retained, p_adj omitted. | Not fully preserved. |
| 82% Layer-A-disjoint | Yes. | Yes: "HIV-1 82% Layer-A-disjoint". | Preserved. |
| Friedman p = 0.990 | Yes: ledger row for no universal best combination. | No. | Dropped. |
| LOPO 0/11 | Yes. | Yes. | Preserved. |
| HBFWS p = 0.78 | Not in current abstract, but present in Ch4/Ch5 audit body. | Yes. | Newly added, body-supported. |
| Wave 5 Layer A' MCC -0.055 | Yes: current abstract line on UniProt-derived Layer A' sensitivity. | No. | Dropped. |

Strict count against the requested anchor list: 4/8 fully preserved. If partial retention is allowed, 6/8 are at least mentioned.

## 2. Concept gap list

- Benchmark identity is weakened: the new draft no longer says MutBench is a region-level, single-position, gap-aware hotspot-detection benchmark for RNA-virus surface glycoproteins with substitutions-only ground-truth labels.
- The 10 biological information types / 20 scoring formulas / 14 detection families / 39 variants / 8,580 evaluation scale is missing. This is load-bearing because it establishes breadth before arguing non-learnability.
- The three-layer ground truth architecture is dropped: Layer A curated positives, Layer B purifying-selection negatives, Layer C DMS validation. This should stay in at least one compressed clause.
- The hotspot-score composite metric is dropped. It is less important than the triage anchor, but it defines the benchmark's original evaluation surface.
- Stage structure is dropped: Stage 1 SARS-CoV-2 sanity check, Stage 2 cross-pathogen comparison, Stage 3 integration. A shortened form is enough.
- The "no universal best combination" evidence loses Friedman p=0.990 and the 0.265 oracle-vs-generalized MCC gap. The draft keeps LOPO but omits the statistic that prevents LOPO from being read alone.
- The label-provenance negative control is lost: Wave 5 Layer A' mean MCC = -0.055, precision@20 = 0.005. This is important because it prevents a simplistic "just add UniProt labels" fix.
- The 10-feature / 4-feature cold-start framing is mostly absent except via audits. If the abstract keeps "wet-lab triage," it should say whether this is from optimal scoring-detection combinations, EqualWeight integration, or the cold-start 4-core.

## 3. Body-claim consistency check

Supported:

- Search-space reduction from about 1,000 positions to 10-50 candidate sites with 7-9x escape enrichment is supported by Ch5 conclusion and Ch4 search-space-reduction section. Ch4 gives the concrete three-anchor range as 11-32 detected positions.
- H3N2 9.36x, SARS-CoV-2 7.63x, HIV-1 7.19x, and HIV-1 as the primary external anchor are supported by Ch4 Table `tab:vaccine_escape_stage3` and Ch5 conclusion.
- "Not a deployable per-position detector" is supported by the callability, null-calibration, and prospective-validation caveats: P5 0/12 callable, Layer A' failure, HBFWS failure, Cycle 7B adaptive failures, and the prospective validation gap.
- HBFWS p=0.78 and Cycle 7B adaptive paradigms all fail are supported in Ch4. Note that Ch4 says six additional paradigms plus HBFWS, i.e. seven adaptive-weighting failures in total; the draft's "Cycle 7B six adaptive paradigms" is okay if HBFWS is listed separately.

Needs tightening:

- "formalising the panel-size threshold (~20-30 pathogens, Bolker rule-of-thumb) at which adaptive method selection becomes possible" is too strong. The body supports "n=11 is below Bolker's >=20-30 stable-random-effects regime" and "expansion to 20-30+ pathogens is future work." It does not prove that adaptive method selection becomes possible at that threshold.
- "falsification-resistant evidence that a deployable cross-pathogen detector is not learnable" is defensible if phrased as "not learnable from the current panel." Avoid implying a theorem of impossibility beyond the current dataset.

Unsupported new claims count: 1 overstrong claim, the "threshold at which adaptive method selection becomes possible."

## 4. Concrete suggested edits to the draft

Suggested revised opening:

> MutBench is a region-level, single-position hotspot-prioritization benchmark for 11 RNA-virus surface glycoproteins, comparing 10 biological information types (20 scoring formulas) x 14 detection families (39 variants) across 11 pathogens for 8,580 evaluations, with a three-layer ground truth. Its practical value is wet-lab triage: for a typical viral protein, optimal scoring-detection combinations narrow about 1,000 positions to roughly 10-50 candidate sites (11-32 in the three escape-enrichment anchors) with 7-9x enrichment for vaccine-escape positions.

Add the missing HIV and non-learnability anchors:

> HIV-1 provides the primary external anchor (7.19x, p_adj = 2.5 x 10^-16; 82% Layer-A-disjoint), while H3N2 is a self-consistency check (9.36x) and SARS-CoV-2 is exploratory after Bonferroni (7.63x).

Replace the overstrong threshold sentence:

> Comprehensive audits at the current panel size show that a deployable cross-pathogen selector is not learnable from n=11: Friedman p=0.990, LOPO 0/11, P5 0/12 callable, HBFWS p=0.78, and six further Cycle 7B adaptive paradigms fail. These results place adaptive method selection below the practical panel-size regime suggested by the Bolker 20-30 pathogen rule-of-thumb, rather than proving that 20-30 pathogens would be sufficient.

Add one compact negative-control clause:

> A UniProt-derived Layer A' sensitivity analysis fails in the opposite direction (Wave 5 mean MCC = -0.055), showing that label provenance is not interchangeable.

Keep the interaction final sentence, but make its role explicit:

> The headline scoring x pathogen interaction (omega^2=0.296, 95% CI [0.201, 0.346]) therefore operationalises the boundary condition: information utility is pathogen-dependent, so current MutBench should be read as a triage framework and audit-backed benchmark, not a calibrated deployable detector.

## 5. Evidence-ledger table verdict

Modify, do not remove.

The ledger is doing useful defensive work: it separates claim, statistic, boundary, and defense role. However, if the abstract is reframed around wet-lab triage, the ledger should be shortened and re-ordered so the practical triage anchor appears first. Recommended rows:

1. Wet-lab triage / search-space reduction: ~1,000 to 10-50 positions; 7-9x enrichment; HIV-1 7.19x, p_adj = 2.5 x 10^-16, 82% Layer-A-disjoint; boundary: retrospective, 3/11 pathogens only.
2. Benchmark scale and ground truth: 11 pathogens, 20 x 14 x 39 = 8,580; three-layer ground truth; boundary: RNA-virus surface glycoprotein substitutions.
3. Pathogen-dependent information utility: omega^2 = 0.296, CI [0.201, 0.346]; 6-category omega^2 = 0.103; boundary: Layer A curation heterogeneity.
4. Non-deployability at current panel size: Friedman p=0.990, LOPO 0/11, P5 0/12 callable, HBFWS p=0.78, Cycle 7B failures, Wave 5 Layer A' MCC=-0.055; boundary: not a proof that 20-30 pathogens suffice.

## 6. Result

RESULT_RISK3: anchors_preserved=4/8 concepts_dropped=8 new_claims_unsupported=1 verdict=revise
