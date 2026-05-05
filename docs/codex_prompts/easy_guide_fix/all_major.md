# Easy Guide v2 — Apply All Major Fixes (28 from 9 chunked audits)

Execute the editing task NOW. Workspace-write OK. Do NOT commit.

## Read all 9 audit reports first

- `paper/dissertation/review/2026-05-04/easy_guide_audit_p1-5.md`
- `paper/dissertation/review/2026-05-04/easy_guide_audit_p6-10.md`
- `paper/dissertation/review/2026-05-04/easy_guide_audit_p11-15.md`
- `paper/dissertation/review/2026-05-04/easy_guide_audit_p16-20.md`
- `paper/dissertation/review/2026-05-04/easy_guide_audit_p21-25.md`
- `paper/dissertation/review/2026-05-04/easy_guide_audit_p26-30.md`
- `paper/dissertation/review/2026-05-04/easy_guide_audit_p31-35.md`
- `paper/dissertation/review/2026-05-04/easy_guide_audit_p36-40.md`
- `paper/dissertation/review/2026-05-04/easy_guide_audit_p41-42.md`

## Target file

`paper/dissertation/dissertation_easy_guide_v2.md` (~1355 lines, Korean PhD dissertation summary)

## Reference state (master v229)

- Manuscript: 197pp, Phase 4 prof v9 = 83.31/100 PASS
- Wet-lab triage reframe (deployment refused; Layer C 6/11 + HIV-1 7.19× = anchors)
- Authoritative anchors:
  - ω²(scoring × pathogen) = 0.296 (cluster-bootstrap CI **[0.201, 0.346]**)
  - HIV-1 full anchor: 7.19× (p_adj = 2.5×10⁻¹⁶, 82% Layer-A-disjoint, 37 of 45 novel)
  - H3N2 9.36×; SARS-CoV-2 7.63× exploratory (Bonferroni-fail)
  - Layer C: 6/11 pathogens, 650 positions, best MCC 0.139–0.322 (EV-A71 0.322 strongest, H3N2 0.245)
  - LOPO 0/11; Friedman p = 0.990; HBFWS p = 0.78; Cycle 7B 6/6 fail (smallest p = 0.56)
  - Wave 5 Layer A' MCC = −0.055

## Task: apply ALL 28 Major fixes from the 9 audit reports

Synthesize the per-chunk recommendations into edits on `dissertation_easy_guide_v2.md`. Do **all 28 Major** items; skip Minor unless trivially fixable in passing. Ignore visual-only issues that require LaTeX rebuild engineering — but fix emoji incompatibility if mentioned.

Common patterns to standardize (apply uniformly):

1. **Layer C anchor**: add a one-sentence anchor "Layer C DMS: 6/11 pathogens (650 positions, best MCC 0.139–0.322; EV-A71 0.322, H3N2 0.245 가장 강함)" near every place where wet-lab/practical evidence is introduced. Recommended insertion points: p1 summary, p11 Layer C section, p19 DMS introduction, p29 Layer A vs Layer C result, Ch 5/6 conclusions.

2. **HIV-1 full anchor**: every standalone "7.19×" mention should be expanded to "7.19× (p_adj=2.5×10⁻¹⁶, 82% Layer-A-disjoint, 37/45 novel)" or referenced from a single anchor sentence. Avoid repeating the full citation 6+ times.

3. **ω² CI**: any remaining `[0.195, 0.333]` → `[0.201, 0.346]`. Verify all occurrences.

4. **Wet-lab triage framing**: replace "실용적 검증" / "실용 가능성" wording with "wet-lab 실험 우선순위 축소" or "실험 후보 prioritization" (Korean) where it appears as practical-value framing.

5. **Cross-reference numbering**: fix any "Table 24" → "Table 30" type mismatches noted in p36-40 audit.

6. **Emoji fix**: replace ✅ 🟢 (and similar) in the v229 appendix with text equivalents (PASS, OK, GREEN as plain text).

7. **Internal consistency**: if a numerical claim in the easy guide does not match dissertation v229 (per audit reports), update to match v229.

## Constraints

- Preserve Korean writing style (this is the easy-Korean guide)
- Do NOT add new sections; modify existing prose, captions, tables only
- Preserve all citation references and figure paths
- After all edits, rebuild PDF: `cd paper/dissertation && pandoc dissertation_easy_guide_v2.md -o dissertation_easy_guide_v2.pdf --pdf-engine=xelatex -V CJKmainfont="Noto Serif CJK KR" -V mainfont="Noto Serif CJK KR" -V geometry:margin=1in`

## Output

- Save modified `paper/dissertation/dissertation_easy_guide_v2.md`
- Rebuild `dissertation_easy_guide_v2.pdf`
- Write change log to `paper/dissertation/review/2026-05-04/easy_guide_fix_all_major_changelog.md`:
  - Per-chunk: which Major items addressed (chunk 1-5, 6-10, ...)
  - Total fixes applied
  - Any deviations (Major items skipped because they require dissertation source change instead)
  - PDF rebuild status
- Print one-line: `RESULT_EASY_GUIDE_FIX_ALL: major_applied=<n>/28 minor_applied=<n>/55 visual_applied=<n>/23 pdf_pages=<N> pdf_status=<built|failed>`

Length budget for changelog: ≤ 3000 words.
