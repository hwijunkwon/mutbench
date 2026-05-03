# Deep audit Job 5 — ch5_discussion (≈26 pp, 3 chunks)

Execute the audit task NOW. Read-only.

Follow template at `docs/codex_prompts/2026-05-03-deep-audit-template.md`.

## Scope

- `paper/dissertation/chapters_en/ch5_discussion.tex` (~26 pp = 340 lines)

Chunk boundaries:
- Chunk 1: lines 1-100 (Methodological Validity, Independence of GT, Layer A provenance)
- Chunk 2: lines 101-220 (Practical Implications, vaccine-escape, defense limitations matrix)
- Chunk 3: lines 221-340 (Summary contributions, Future Research, Concluding Remarks, defense map)

## Specific items to verify

- Layer A provenance summary table — 12 pathogens × n positions × dominant
  source × tag mix. Must match `layer_a_tags.csv` aggregation.
- Defense map table — 5 claim rows aligned with C1, C2, C3, Wave 5, Cycle 7B.
  Verify each "Allowed oral wording" matches the manuscript's claim
  framing in Ch1/Ch4.
- Future research roadmap table priorities/timelines.
- Layer A curation-reproducibility limitations paragraph: claims about
  "no IAA / no source-selection sensitivity / region-derived caveat" —
  factually consistent with Layer A construction described in Ch3?
- Take-home message and Concluding Remarks: do they overstate or stay within
  the bounds set by Ch3-Ch4 evidence?

## Specific cross-chapter checks

- Every `Section~\ref{...}` and `Paragraph~\ref{...}` should land on a real
  target in Ch1-Ch5.
- Every claim that says "as shown in Chapter X" should actually appear in
  that chapter.
- Every Layer A heterogeneity caveat should be consistent with Ch3 §
  Layer A construction.

## Output

`paper/dissertation/review/2026-05-03/deep_audit_job5_ch5.md`

End with: `RESULT_DEEP_J5: critical=<n> major=<n> minor=<n>`

Length ≤ 3000 words.
