# Agent 4 — Aggregator: Curation Heterogeneity Concern Final Verdict

Execute the analysis NOW. Read-only. Do not commit.

## Inputs

Read all 3 prior reports:
- `paper/dissertation/review/2026-05-06/curation_audit_agent1.md` (curation philosophy catalog)
- `paper/dissertation/review/2026-05-06/curation_defense_agent2.md` (dissertation defense audit)
- `paper/dissertation/review/2026-05-06/curation_statistics_agent3.md` (statistical re-analysis)

## User-supplied framing guidance (must reflect in recommendations)

**The user explicitly recommends a framing change**: instead of "hotspot definition is ambiguous" (defensive, limitation-flavored), reframe as:
- "hotspot is a **comprehensive AND fluid (context-dependent) concept**" (positive, contribution-flavored)
  - **Comprehensive (포괄적)**: spans multiple complementary perspectives — convergent evolution, immune escape, hypervariable region, DMS fitness
  - **Fluid (유동적)**: the operationalization naturally varies across pathogens because each pathogen's evolution mode and immune-pressure context differ
- "the benchmark covers **comprehensive and pathogen-context-dependent operationalizations of hotspot-ness**" (contribution, not limitation)
- "Layer A/B/C represent **comprehensive coverage of fluid hotspot perspectives**" (design choice, not weakness)

So the curation-heterogeneity defense should NOT just say "we acknowledge curation differs across pathogens." It should say:
- "Different curation protocols across pathogens reflect **the comprehensive and fluid nature of hotspot-ness** in viral genomics — hotspot is not a single fixed property but a context-dependent operationalization"
- "Each pathogen's Layer A captures the hotspot perspective **most relevant to its evolutionary mode and immune-pressure context** (HVR for HCV, antigenic drift for H3N2, multi-VOC convergent evolution for SARS-CoV-2, etc.)"
- "The ω²=0.296 interaction **integrates this comprehensive-and-fluid design** rather than being an artifact of inconsistent labels"
- "The fluidity is a feature, not a bug: it lets the benchmark cover the comprehensive scope of viral hotspot phenomena rather than forcing one rigid definition"

The user wants this framing applied to:
1. The 60-second oral-defense response
2. The manuscript additions to ch3/ch5
3. The recommended action (option a/b/c/d)

## Task

Produce a **final verdict** on the reviewer concern: "Is ω²=0.296 measuring pathogen biology or curation-protocol-dependence?" — using the user's multi-perspective framing.

Synthesize:

1. **Quantitative answer**: what fraction of 0.296 is plausibly biology vs curation?
2. **Defensibility verdict**: defendable / partially defendable / not defendable
3. **Best oral-defense response**: a 60-second answer the candidate can give if asked
4. **Manuscript additions needed**: specific text to add to ch3/ch4/ch5 to fully address this concern
5. **Recommended action**: 
   - (a) Manuscript already adequate — no changes needed
   - (b) Add 1-2 paragraphs + cross-reference to existing analyses
   - (c) Run new statistical analysis (homogeneous-curation subset ω²) before defense
   - (d) Larger restructuring needed

## Output

`paper/dissertation/review/2026-05-06/curation_aggregate_agent4.md`

Structure:

```
# Layer A Curation Heterogeneity — Final Verdict

## Executive summary
{1 paragraph quantitative answer + defensibility verdict}

## Quantitative breakdown
- Biology share: ~X%
- Curation share: ~Y%
- Indeterminate: ~Z%

## Defense readiness
- Existing defense strength: [from agent2]
- Gaps: [from agent2]

## Best 60-second oral-defense response
"..."

## Manuscript additions needed (specific text)

### Suggested addition to ch3:
[text with location]

### Suggested addition to ch5:
[text with location]

## Recommended action
{a/b/c/d + rationale}

RESULT_CURATION_AGGREGATE: biology_share_pct=<X> curation_share_pct=<Y> defensibility=<DEFENDABLE|PARTIAL|NOT> action=<a|b|c|d>
```

Length: ≤ 2500 words.
