# Codex consultation — How to dispose of incomplete Wave 5 work

You are an independent reviewer. **Read-only mode. Do not modify any file.** Your
task is adversarial deep analysis of a strategic decision and a recommendation
delivered as a markdown report at the end.

## The strategic question

Human Layer A curation (Task 3 of Wave 5) is **infeasible** for the dissertation
defense window — the user has explicitly declared this. Tasks 1–2 of Wave 5
(automated PubMed search + per-position evidence aggregation + worksheet
generation) are already committed to the `experiments/waves` branch. Tasks 3–6
cannot proceed. **What should we do?**

User's framing: "미완인데 어떻게 포함하는가" — i.e., if Wave 5 is incomplete, how
do we honestly reconcile (a) the worksheets sitting on disk, (b) the thesis
prose that already names "Wave 5 pilot 3" twice in `chapters_en/`, and (c) the
defense narrative.

This is a single-shot decision; I want your independent judgment, not a
hand-waved "depends on context" answer.

## Repository state (verified at 2026-05-02)

- Two branches, divergence preserved by `backup/master-before-split-2026-05-01`
  tag and pushed to `origin`:
  - `master` at v180 (d87df85): pre-Wave-1 state, `thesis_en.pdf` 232 pp, no
    Wave content in chapters or `results/`. Sync target is `pahd_r_easy_guide.md`.
  - `experiments/waves` at v206 (6b29864): contains Wave 1–4 (validated, prose
    inserted) and Wave 5 prep commits v203–v205. `thesis_en.pdf` 233 pp.
- Commit chain on `experiments/waves` past master:
  - v181–v186 = Wave 1 (P1+P2+P3 + prose v185 + closure v186)
  - v187–v191 = Wave 2 (P5 callability + prose v190 + closure v191)
  - v192–v196 = Wave 3 (P6 biological nulls + prose v195 + closure v196)
  - v197–v202 + v206 = Wave 4 (Tier 2 LOPO + prose v206 + closure v202)
  - v203 = Wave 5 plan + codex review (`docs/plans/2026-05-01-wave5-pilot3-layerA-curation.md`)
  - v204 = Wave 5 Task 1: PubMed search, 911 unique PMIDs, 916 abstracts
  - v205 = Wave 5 Task 2: per-position evidence aggregation + worksheets
- Wave 5 closure commit (v206-equivalent for Wave 5) **does not exist**.
- Wave 5 prose insertion in chapters **does not exist**.

## What Wave 5 prep actually delivered (v204 + v205)

Files on disk under `results/mutbench/codex_wave5/`:

- `w5_evidence_summary.csv` — per-target counts:
  - YFV E: 499 positions, 48 with any evidence (9.6%), 13 strong-evidence candidates
  - Lassa GPC: 491 positions, 97 with any evidence (19.8%), 10 strong candidates
  - WNV E: 501 positions, 73 with any evidence (14.6%), 23 strong candidates
- `w5_{target}_evidence.csv` — per-position evidence rows (1491 rows total)
- `w5_abstracts/{target}/<PMID>.txt` — 916 abstract text files
- `worksheets/w5_{target}_curation.csv` — empty `final_label/curator/curation_date`
  columns; `proposed_label/confidence` also empty (codex correctly refused to
  auto-fill these per plan §"Hard boundary"). Top-line banner reads:
  `# DO NOT AUTO-FILL final_label, proposed_label, or confidence — human curator only`
- `worksheets/w5_{target}_strong_candidates.csv` — extracted strong candidates
  for human curator priority review (10–23 per target)
- `worksheets/w5_{target}_strong_excerpts.md` — quoted abstract excerpts
- `scripts/codex_w5_pilot3_evidence.py` — the evidence aggregation script

Plus v203 plan (`docs/plans/2026-05-01-wave5-pilot3-layerA-curation.md`, 359 lines)
and v203 codex plan review (`paper/dissertation/review/2026-04-30/codex_wave5_plan_review.md`,
78 lines).

## What thesis prose currently says about Wave 5

In `paper/dissertation/chapters_en/ch4_results.tex` (Wave 4 paragraph
`para:w4_tier2_lopo`, inserted by v206):

> "...the Wave 5 pilot 3 ordering for YFV/Lassa/WNV is preserved in
> Section~\ref{sec:future_work}."

In `paper/dissertation/chapters_en/ch5_discussion.tex` (Wave 4 paragraph,
inserted by v206):

> "Wave 4 has now executed the Tier 2 features-only LOPO at the available
> expanded scope (Paragraph~\ref{para:w4_tier2_lopo}); the 2-core fallback was
> bounded positive, but D1 remained 0/12 and only 1/28 targets were stable,
> confirming the panel-size limit and making Layer A curation in Wave 5 pilot 3
> the rate-limiting next step rather than an optional add-on."

In `paper/dissertation/chapters_en/ch5_discussion.tex` (`Prospective
Callability and Abstention Rule (Wave 2 result)`, inserted by v190):

> "The remaining experiments in this future-work programme — Tier 2 features-only
> LOPO at $n \approx 30$, pilot~3 Layer~A literature curation for YFV/Lassa/WNV,
> and Tier 3 EVE/PLM site-effect via the prepared container — are reserved for
> an expanded panel where the 7/11 quorum is structurally reachable and the
> deployment claim can be tested rather than refused."

So thesis prose treats Wave 5 pilot 3 as **future work**, NOT executed. The
worksheets on disk are infrastructure preparation, not results.

## Wave 4 closure context (memory: codex_wave4_results.md)

Per Wave 4 plan §branch outcome:

> "The 16/16 envelope gives concrete reason to proceed with curation rather than
> treating Wave 4 as dead end."

Wave 4 result review verdict was **POSITIVE-BOUNDED**. Wave 5 pilot 3 was
declared the next rate-limiting step.

## Wave 5 plan §branches (predeclared, in `docs/plans/2026-05-01-wave5-pilot3-layerA-curation.md`)

- **Branch C**: 0/3 targets get ≥10 high-confidence positives → "pilot 3
  attempted, demonstrating Layer A bottleneck is real" (no validation run).
- **Branch G**: validation worsens or quorum still fails → "labels alone did
  not resolve the Wave 4 stability bottleneck; next step becomes richer feature
  generation or broader curation, not overclaiming."

The plan **predeclared** that 0/3 success counts as a defensible outcome
("Layer A bottleneck is real"), parallel to a non-execution outcome.

## The four candidate dispositions

### Option A — Reset to master (abandon all Wave work)

Hard reset `experiments/waves` to master (or just stop using the branch). Lose
Wave 1–4 prose (30 lines), 1647 lines of supplementary review docs, and the
Norovirus 4-null robust + P1+P6 unified + Tier 2 LOPO defense narrative.
Thesis returns to 232 pp.

### Option B — Merge experiments/waves to master, keep Wave 5 prep as-is

Squash- or fast-forward-merge the branch. Wave 1–4 prose stays. v203–v205
commits travel to master, including 911 PMIDs + worksheets. Thesis prose still
calls Wave 5 "future work" — the worksheets are unmentioned infrastructure.

### Option C — Merge Wave 1–4 only, drop v203–v205

Either revert v203/v204/v205 on the branch then merge, or cherry-pick
v181–v202 + v206 onto master. Wave 5 plan, PubMed data, worksheets, and the
Wave 5 codex plan review all disappear from history (or only remain in the
backup tag). Thesis prose still calls Wave 5 "future work" — but now the repo
contains zero infrastructure proving any prep was done.

### Option D — Merge everything and add a Wave 5 closure commit

Merge experiments/waves to master AND add a new commit (e.g., v207) that:
- Writes a `paper/dissertation/review/2026-05-01/wave5/w5_status.md` note saying
  Tasks 1–2 done, Task 3 deferred at human checkpoint per plan, Tasks 4–6
  blocked. Update `NOTES.md` accordingly.
- Optionally add 1–3 sentences in `chapters_en/ch5_discussion.tex` future-work
  section acknowledging that worksheets exist and are awaiting curation —
  framing the prep as evidence the bottleneck is operational not absent.
- Optionally write a `codex_wave5_partial.md` memory file noting "Wave 5 frozen
  at Task 2; resume requires human curator."

This is the most paper-trail-honest disposition.

## Adversarial questions I want you to answer

For EACH of A/B/C/D give a critical assessment, NOT a sales pitch. Specifically:

1. **Defense-committee read.** What would a hostile committee member say if
   they (a) read the thesis prose only, (b) browsed the repo and saw v204/v205
   commits, or (c) ran `git log` and saw the gap between Wave 4 closure and
   nothing for Wave 5? Where is each option vulnerable to "you over-promised /
   you hid work / you fabricated future-work language"?

2. **Hidden technical debt.** Are there scripts, CI hooks, NOTES.md entries,
   memory files, or `paper/dissertation/review/` index entries that would be
   internally inconsistent under each option (e.g., Wave 5 plan exists but
   no closure exists, or NOTES.md trail mentions Wave 5 work but git history
   doesn't, or the README under `results/mutbench/codex_wave5/` advertises a
   pipeline that nobody can finish)?

3. **Reproducibility cost.** If a future curator (or a successor lab) wants to
   pick up Wave 5, what does each option cost them? PubMed search alone is ~5
   min API time but downloading 916 abstracts + the evidence-extraction step
   are non-trivial to recreate.

4. **Honesty calibration.** Per the user's working style memory entry, the
   user is sensitive to "probing completeness" and adversarial multi-agent
   review. Which option survives that lens? Which one risks looking like a
   cosmetic move?

5. **Branch hygiene.** What is the cheapest way to leave the repo in a state
   that does not invite future confusion — e.g., a stale `experiments/waves`
   that someone might accidentally branch off in 6 months?

## Specific things to verify, not infer

- Run `git log --oneline master..experiments/waves` to confirm the v181–v206
  commit chain.
- Read `NOTES.md` and check whether it mentions Wave 5 progress in a way that
  would be inconsistent with any disposition.
- Look at `paper/dissertation/review/2026-05-01/wave5/` directory if it exists
  — what's there?
- Check `results/mutbench/codex_wave5/README.md` to see what the published
  pipeline description claims about completion state.
- Check whether the Wave 4 paragraph `para:w4_tier2_lopo` cites any Wave 5
  artefact path (it should not, but verify).
- Check the index file `paper/dissertation/review/2026-04-30/INDEX.md` (or
  similar) to see whether Wave 5 is listed anywhere as completed or pending.
- Confirm `backup/master-before-split-2026-05-01` tag actually exists via
  `git tag -l 'backup/*'` so we know reversal is genuinely possible.

## Output

Write your report to:

  `/proj/paper/paper/dissertation/review/2026-05-02/codex_wave5_disposition_review.md`

(Create the directory if it does not exist. Do not commit.)

Structure:

1. **Verification section** — what you actually found in the repo (cite paths
   and exact file contents you read).
2. **Per-option critical assessment** — A, B, C, D, each with the 5 adversarial
   questions answered concretely.
3. **Recommendation** — pick ONE option with reasoning. If your recommendation
   is a hybrid or modification of A–D, state it as a new Option E with explicit
   diff from the closest existing option.
4. **Concrete next-step sequence** — exact git/file operations to execute the
   recommended option, in order. Include any prose snippet you recommend
   inserting (full LaTeX, ready to paste).
5. **What you would NOT do, and why** — explicitly call out moves that look
   tempting but you reject (e.g., "do not silently delete v204/v205 because…").

Length budget: ≤4000 words. Cite specific files and commit hashes; do not
hand-wave.
