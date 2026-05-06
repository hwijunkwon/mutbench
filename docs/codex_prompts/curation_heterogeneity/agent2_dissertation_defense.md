# Agent 2 — Dissertation Defense Audit (Layer A heterogeneity concern)

Execute the analysis NOW. Read-only. Do not commit.

## Reviewer concern

"ω²=0.296 may be measuring Layer A curation-protocol-dependence, not pathogen biology. Each pathogen's Layer A was built by different researchers with different definitions and goals."

## Task

Audit how the dissertation v229 (197pp master) currently defends against this concern. Read carefully:

- `paper/dissertation/chapters_en/ch3_methods.tex` (Layer A construction, source heterogeneity disclosure)
- `paper/dissertation/chapters_en/ch4_results.tex` (HCV-excluded sensitivity, immune-escape-only subsets)
- `paper/dissertation/chapters_en/ch5_discussion.tex` (Layer A heterogeneity limitations matrix, curation reproducibility limits)

Identify:

1. **Existing defenses**: which sections/sentences address this concern? Quote them.
2. **Strength of each defense**: how convincing is each?
   - HCV-excluded ω²=0.246 (strong: shows the effect is not all HCV)
   - Layer A immune-escape-only subsets (ω²=0.199/0.187/0.137 for n=10/9/4) — partially address
   - Layer A provenance summary table (12 pathogens × dominant source) — descriptive only
   - Layer A curation-reproducibility limitations paragraph — disclosure
3. **Gaps**: which aspects of the concern are NOT addressed?
   - Region-based vs position-based curation philosophy distinction?
   - "Same curation philosophy subset" ω² recalculation?
   - Direct test: does ω²(scoring × pathogen) drop substantially within homogeneous-curation subsets?
4. **Defense readiness**: if a strict reviewer asks this question at oral defense, can the candidate point to a specific paragraph + number that answers it?

## Output

`paper/dissertation/review/2026-05-06/curation_defense_agent2.md`

Structure:

```
# Dissertation Defense Audit: Layer A Curation Heterogeneity

## 1. Existing defenses (quoted from manuscript)

### Defense 1: HCV-excluded sensitivity
**Location**: ...
**Quote**: ...
**Strength**: HIGH/MEDIUM/LOW because ...

### Defense 2: ...

(repeat for each existing defense)

## 2. Defense gaps

What's NOT in the manuscript:
- ...

## 3. Defense readiness verdict

If asked: "Is your ω²=0.296 measuring biology or curation protocol?"
**Current best answer (from manuscript)**: [quote the strongest existing passage]
**Adequacy**: ADEQUATE / PARTIAL / WEAK

## 4. Suggested manuscript additions

To convert PARTIAL/WEAK to ADEQUATE, add:
- [specific text suggestion]
- [where to insert]

RESULT_CURATION_AGENT2: existing_defenses=<n> gap_count=<n> adequacy=<ADEQUATE|PARTIAL|WEAK> suggested_additions=<n>
```

Length: ≤ 2500 words.
