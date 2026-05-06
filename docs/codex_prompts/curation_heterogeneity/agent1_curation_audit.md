# Agent 1 — Layer A Curation Philosophy Audit

Execute the analysis NOW. Read-only. Do not commit.

## Question

Reviewer concern: "ω²(scoring × pathogen)=0.296 may not measure pathogen biology — it may be measuring **Layer A curation-protocol-dependence**. Each pathogen's Layer A was built by different research groups, with different goals, different evidence types, and different definitions of 'hotspot'."

## Task

Audit `results/mutbench/layer_a_tags.csv` and produce a comprehensive **per-pathogen curation philosophy catalog**. For each of the 12 pathogens:

1. **Curation method**: region-based (e.g., HCV HVR), position-by-position (e.g., SARS-CoV-2 multi-VOC), antigenic-site-based (e.g., H3N2 Koel 2013), DMS-derived, or hybrid
2. **Source diversity**: single-paper vs multi-paper; year span (e.g., Rabies 1983-2025)
3. **Evidence-type composition**: immune_escape vs convergent vs functional ratio
4. **Granularity**: are positions chosen one-by-one with literature evidence, or are they defined by region inclusion (entire HVR, V-loops, antigenic sites)?
5. **Implicit feature bias**: does the curation method automatically privilege certain feature types?
   - HCV HVR-based → automatically high-frequency region → freq-scoring "wins" by construction
   - HIV-1 V-loop-based → automatically high-entropy region → entropy-scoring "wins" by construction
   - H3N2 single-paper antigenic sites → high overlap with already-known epitopes → FUBAR phylogenetic selection finds them
   - SARS-CoV-2 position-by-position multi-VOC → genuinely literature-curated, less feature-biased

## Output

`paper/dissertation/review/2026-05-06/curation_audit_agent1.md`

Structure:

```
# Layer A Curation Philosophy Catalog

## Summary table (12 pathogens)
| Pathogen | n | sources | curation method | year span | evidence types | implicit feature bias |

## Per-pathogen detail

### HCV (n=54)
**Curation method**: ...
**Sources**: ...
**Implicit bias**: ...
**Effect on Stage 2 best scoring**: ...

(repeat for all 12)

## Cross-pathogen patterns

- **Region-based curation** (HCV, HIV-1): ...
- **Position-based curation** (SARS-CoV-2, Rabies): ...
- **Antigenic-site definition** (H3N2, RSV, Influenza_B): ...
- **DMS-supplemented** (EV-A71, Rabies, Zika): ...

## Implicit feature bias assessment

For each pathogen, predict the "expected best feature" from curation method alone (without measuring MCC). Then compare to observed Stage 2 winners (Table 4.1 / tab:stage2_best). How many match?

## Risk verdict

What fraction of ω²=0.296 is plausibly attributable to curation-protocol-dependence rather than pathogen biology? Quantitative estimate.

RESULT_CURATION_AGENT1: region_based=<n>/12 position_based=<n>/12 single_paper=<n>/12 evidence_homogeneous=<n>/12 expected_protocol_omega_share=<x.x>%
```

Length: ≤ 3000 words.
