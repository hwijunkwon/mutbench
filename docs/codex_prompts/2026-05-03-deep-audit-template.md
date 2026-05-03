# Deep audit template — to be customised per chapter

## Goal

10-page-chunk audit of the active manuscript with fact-check against
internal CSVs and (where needed) external web search.

## Constraints

- Read-only on manuscript and source CSVs.
- Web search OK (e.g., for verifying citation accuracy or claim plausibility).
- Output a structured findings list, not edits.

## For each ~10-page chunk

1. **Numerical claim audit**: list every numerical claim in the chunk with
   the authoritative source (CSV file path under `results/mutbench/` or
   `paper/dissertation/`). Mark VERIFIED / UNVERIFIED / DISCREPANCY.
2. **Citation accuracy**: for each `\cite{key}` in the chunk, briefly state
   what claim it supports and whether the cited paper plausibly supports
   that claim (use general knowledge; only do web search for
   borderline cases).
3. **Cross-reference check**: every `\ref{label}` should land on the right
   target.
4. **Logical consistency**: any sentence that contradicts another sentence
   elsewhere in the manuscript? List with locations.
5. **Outdated content**: any leftover phrasing referencing earlier panels
   (e.g., "9 pathogens", "12-pathogen Stage 2", "PAHD") that no longer matches
   the current state?
6. **Severity tier per finding**:
   - Critical: would fail a defense if asked
   - Major: would lower score by 1+ on at least one rubric item
   - Minor: cosmetic / phrasing
   - Verified: no issue

## Output structure (per chunk)

```
### Chunk N (lines L1-L2, pages P1-P2)

#### Numerical claims
- Claim X: VERIFIED / [source]
- Claim Y: DISCREPANCY / [expected Z, found W in manuscript]

#### Citations
- \cite{key1}: supports [...] / OK
- \cite{key2}: supports [...] / SUSPICIOUS — actual paper is about [...]

#### Cross-refs
- \ref{labelA}: → table 4.5 (correct)

#### Logical consistency
- Line L1 says X; line L1' says X' (inconsistent? acceptable?)

#### Outdated content
- (none) or [list]

#### Severity
- 0 Critical / 1 Major / 3 Minor (example)
```

End with one-line:
`RESULT_DEEP_<chapter>: critical=<n> major=<n> minor=<n> verified_chunks=<n>/<total>`
