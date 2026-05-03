# Cycle 6 deeper re-analysis — entire dissertation, all 8 axes, more rigorous

Execute the deep audit task NOW. Read-only. Write only the final report.

You are running a deeper re-analysis of the dissertation from the same 8 axes
covered in Cycle 6 Jobs 1-4, but applied to the WHOLE manuscript with stricter
rigor than the original cycle-6 round. The user has now applied 5 J4 defense
readability fixes (defense map table, panel-scope box, "establishes practical
relevance" softened, LOPO spoken-answer, Layer A provenance summary), so the
manuscript is at 243 pages.

Active English build files at /proj/paper/paper/dissertation/chapters_en/
plus front_en/abstract.tex.

## Required reading

- All cycle 6 J1-J4 reports under paper/dissertation/review/2026-05-02/
- Phase 4 cycle 5 score 82.9/100 with H 7.8 residual
- All cycle 4 perspectives reports (cycle4_*.md)
- Active manuscript

## Deeper-rigor differences from original cycle 6

1. **Whole-paper cross-cutting**: do not silo per-axis; identify findings
   that span multiple axes (e.g., a single missing sentence that lifts
   content + flow + readability simultaneously).
2. **PhD-thesis-grade benchmark**: judge against published RNA-virus
   benchmarks and equivalent computational-biology dissertations, not
   only against internal logic.
3. **Verify the 5 just-applied fixes**: read the new defense map table,
   panel-scope box, softened sentence, LOPO spoken-answer, and Layer A
   provenance summary table. Verdict: did each fix actually lift the
   intended axis? PASS / partial / regression.
4. **Identify second-order risks**: what new gaps did the 5 fixes create
   or expose? (e.g., new tables increase length; verbal-fluency sentence
   may conflict with later prose.)
5. **Per-axis re-grade with finer resolution**: instead of strong/medium/weak,
   give numeric 1-10 grades with sub-component scores.

## Per-axis deeper re-analysis

For each of the 8 axes, produce:

### Per-axis output

```
### Axis N — <name>
- Original cycle-6 verdict: <strong/medium/weak>
- Cycle-6-deeper grade: X.X / 10
- Sub-components: ...
- New findings (not in original cycle 6): ...
- Verification of the 5 J4 fixes that touch this axis: ...
- Top remaining gap, post-fix: ...
- Smallest additional fix to lift to grade 9.0+: ...
```

8 axes:
1. Content appropriateness
2. Length appropriateness (re-evaluate with new tables, 243 pages)
3. Method appropriateness
4. Argument focus
5. Flow
6. Data appropriateness
7. Claim-evidence calibration
8. Defense readability + Q&A robustness

## Cross-axis synthesis

After per-axis sections, produce:

1. **Top 5 cross-cutting findings** that span 2+ axes (each ≤80 words)
2. **The 5 sentences in the dissertation that most need rewording** (cite file:line, propose replacement, rationale)
3. **The single biggest defendability gap** that the 5 fixes did NOT close
4. **Stretch goals**: 3 enhancements that would lift the dissertation from
   "defensible at 83/100" to "exemplary at 90+/100" (each ≤120 words);
   evaluate effort vs lift ratio

## Output

Write report to:
  /proj/paper/paper/dissertation/review/2026-05-02/cycle6_deeper_rerun.md

End with one-line headline:
   `RESULT_C6D: avg_grade=<x.x>/10 top_gap=<short> stretch_lift_potential=<x.x>`

Length budget: ≤ 4000 words. Do not commit.
