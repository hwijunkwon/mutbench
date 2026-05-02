# Wave 5 Incomplete-Work Disposition Review

Date: 2026-05-02  
Reviewer: Codex, independent/adversarial read-only review  
Repository state checked from branch: `experiments/waves`

## 1. Verification

I verified the requested repository facts directly.

- `git log --oneline master..experiments/waves` shows `experiments/waves` contains v181 through v206, ending at `6b29864 feat: v206 -- Wave 4 prose insertion (ch4/ch5_en, thesis 232->233pp)`. The Wave 5 prep commits are exactly `c276ff0` (v203 plan), `f5fa214` (v204 PubMed search), and `38e0727` (v205 evidence sheets/worksheets). There is no Wave 5 closure commit after `38e0727`; the next commit is Wave 4 prose `6b29864`.
- `git tag -l 'backup/*'` returns `backup/master-before-split-2026-05-01`, so reversal is technically possible.
- `NOTES.md` is not neutral. Lines in the 2026-05-01 section record Wave 5 Task 1, Task 2, retry reconciliation, and status at the "Task 3 HUMAN CURATION PAUSE POINT." The strongest line says Tasks 1+2 are complete, worksheets are ready, and Tasks 4-6 are blocked until human-filled `proposed_label`/`confidence`/`notes`/`final_label`/`curator`/`curation_date`.
- `paper/dissertation/review/2026-05-01/` does not exist, despite the Wave 5 plan saying each task should write standalone reports there. There is therefore no `paper/dissertation/review/2026-05-01/wave5/` status/closure note today.
- No `paper/dissertation/review/2026-04-30/INDEX.md` or similar review index exists under `paper/dissertation/review` (`find ... -iname '*INDEX*' -o -iname 'README*'` returned nothing). There is no index entry falsely marking Wave 5 complete.
- `results/mutbench/codex_wave5/README.md` does not exist. The plan expected it, but the committed/working tree has only `results/mutbench/codex_wave5/worksheets/README.md`.
- `results/mutbench/codex_wave5/worksheets/README.md` explicitly says the worksheets are for human Layer A curation; Codex aggregated abstract-level residue evidence only and intentionally left `proposed_label`, `confidence`, and `final_label` blank. It also says not to integrate labels until human-only columns are completed and approved.
- `results/mutbench/codex_wave5/w5_evidence_summary.csv` records: YFV E 48/499 positions with evidence and 13 strong candidates; Lassa GPC 97/491 and 10; WNV E 73/501 and 23.
- `results/mutbench/codex_wave5/w5_search_summary.csv` begins with `# git_sha,c276ff...` and `# query_date_utc,2026-05-01T06:38:30Z`; `w5_search_status.txt` is `ok`.
- The Wave 5 artifact directory contains 916 abstract text files plus `w5_pmid_inventory.csv`, `w5_search_log.json`, per-target evidence CSVs, curation worksheets, and strong-candidate/excerpt files. The strong-candidate/excerpt files are currently untracked in this working tree, although they exist on disk.
- `paper/dissertation/chapters_en/ch4_results.tex` paragraph `para:w4_tier2_lopo` does not cite any Wave 5 artifact path. It cites only Wave 4 script/result/report paths and says Wave 5 pilot 3 ordering is preserved in future work.
- `paper/dissertation/chapters_en/ch5_discussion.tex` mentions Wave 5 pilot 3 twice. Both uses frame it as future work / next prospective test, not as an executed result.

## 2. Per-Option Critical Assessment

### Option A -- Reset to master / abandon all Wave work

**Defense-committee read.** Thesis-only readers see no Wave 1-4 gains and no Wave 5 inconsistency, but that comes at the cost of discarding the strongest defense-time bounded-results narrative. A committee member who later sees `experiments/waves`, the backup tag, or pushed commits can fairly ask why validated negative/bounded audit work was suppressed. This does not look like fabrication, but it can look like risk-averse erasure.

**Hidden technical debt.** Cheapest source tree, but intellectually dirty if `NOTES.md`, remote branch state, prompts, or memory files remain reachable elsewhere. If `experiments/waves` is left alive, future readers find a richer branch that contradicts the submitted master narrative.

**Reproducibility cost.** Highest. It throws away Wave 1-4 reports/prose and Wave 5 automated evidence caches. A successor can recreate PubMed search in minutes only if network/API behavior and query details are preserved; recreating 916 abstracts and evidence extraction is non-trivial.

**Honesty calibration.** Weak. For a user sensitive to adversarial completeness, this looks cosmetic: "we made the problem disappear by reverting to a cleaner story."

**Branch hygiene.** Only clean if `experiments/waves` is explicitly archived/renamed/deleted after preserving a tag. Otherwise it invites the exact six-month confusion the question warns about.

### Option B -- Merge `experiments/waves` to master, keep Wave 5 prep as-is

**Defense-committee read.** Thesis-only readers are mostly safe: Wave 5 remains future work. Repo-browsing readers find v204/v205 worksheets, `NOTES.md` pause-point entries, and no closure note. The hostile read is: "You did a partial Wave 5, left it unreported in the thesis, and never closed the loop." This is not overclaiming, but it is vulnerable to incompleteness and paper-trail sloppiness.

**Hidden technical debt.** Significant. The plan promised `results/mutbench/codex_wave5/README.md` and per-task reports under `paper/dissertation/review/2026-05-01/wave5/`; neither exists. `NOTES.md` states the true pause point, but no durable review note explains why Tasks 3-6 stopped. `worksheets/README.md` is honest, but buried.

**Reproducibility cost.** Low. It preserves the useful search and evidence artifacts. The cost is interpretive: successors must infer from `NOTES.md` and worksheet README that the pipeline stopped deliberately at the human checkpoint.

**Honesty calibration.** Medium. Keeping the artifacts is honest, but not adding an explicit disposition note is a passive ambiguity. Under probing review, "unmentioned infrastructure" is weaker than "declared frozen at Task 2."

**Branch hygiene.** Better than A/C only if master is fast-forwarded and the branch is retired. If `experiments/waves` remains active after merge, people may continue from a branch whose last commit is misleadingly Wave 4 prose after Wave 5 prep.

### Option C -- Merge Wave 1-4 only, drop v203-v205

**Defense-committee read.** Thesis-only readers are clean: Wave 5 is future work and no artifacts contradict it. But repo readers who know the branch/tag history can see that v203-v205 existed and were selectively removed. A hostile member can call this hiding incomplete work, especially because `NOTES.md` currently records Wave 5 progress. It is defensible only if framed as "not part of the submitted artifact," but it will still look curated.

**Hidden technical debt.** More than it first appears. Cherry-picking v181-v202 plus v206 is not clean because `6b29864` modifies `NOTES.md` after the Wave 5 notes existed; careless cherry-pick can carry Wave 5 `NOTES.md` entries while dropping the files. Reverting v203-v205 on branch preserves deletion commits that advertise the omission. Either way, the history remains explanatory burden.

**Reproducibility cost.** Medium-high. It discards the plan, search inventory, abstracts, evidence aggregation script, and worksheets from the main line. The backup tag may preserve them, but a successor lab will not naturally find or trust them.

**Honesty calibration.** Weak. This is the most cosmetic option: the thesis says future work, and the repo is made to match by deleting prep evidence. That solves surface consistency by reducing transparency.

**Branch hygiene.** Operationally fussy. Revert/cherry-pick paths are error-prone, especially around `NOTES.md` and `thesis_en.pdf`. The stale branch still needs retirement or it remains a competing source of truth.

### Option D -- Merge all and add a Wave 5 closure/status commit

**Defense-committee read.** Thesis-only readers still see Wave 5 as future work, which is accurate. Repo-browsing readers see v204/v205 plus a direct status note saying Tasks 1-2 were infrastructure, Task 3 is deferred by human infeasibility, and Tasks 4-6 are blocked. The hostile question becomes answerable: "We did not claim Wave 5 results; we preserved reusable prep and documented the stop condition."

**Hidden technical debt.** Lowest if the closure commit also fixes the existing documentation hole: create `paper/dissertation/review/2026-05-01/wave5/w5_status.md`, update `NOTES.md`, and ideally add `results/mutbench/codex_wave5/README.md` that points to the worksheet README and status note. It should also decide whether to track or delete the untracked strong-candidate/excerpt files; leaving them untracked is future confusion.

**Reproducibility cost.** Lowest. It preserves the PubMed inventory, abstract cache, evidence CSVs, scripts, and worksheet schema while freezing the interpretation before any validation claim.

**Honesty calibration.** Strongest. It does not hide incomplete work and does not inflate it into a result. It matches the user's "미완인데 어떻게 포함하는가" concern: include it as incomplete infrastructure with an explicit stop condition, not as dissertation evidence.

**Branch hygiene.** Good if followed by merge hygiene: fast-forward/squash according to project policy, tag the merge/freeze point, delete or lock `experiments/waves` after master contains the status commit, and stop using the branch name as a live work target.

## 3. Recommendation

Choose **Option D, with one mandatory modification**: the Wave 5 closure/status commit must be a "freeze at human checkpoint" commit, not a results-review commit. Do not call it `codex_wave5_results.md`; call it `w5_status.md` or `codex_wave5_partial.md`. The status should say Wave 5 Tasks 1-2 are reusable infrastructure, Task 3 is infeasible for the defense window, and no Task 4-6 integration/validation/prose-result step occurred.

I would also add a small `results/mutbench/codex_wave5/README.md`. The plan expected one, the root directory currently lacks one, and a future reader entering through `results/` should not have to discover the stop condition through `NOTES.md`.

I would not add Wave 5 as a result in Chapter 4. A short future-work sentence in Chapter 5 is acceptable only if it says the worksheets exist and await human curation. The thesis currently does not overclaim; the repo needs closure more than the prose needs expansion.

## 4. Concrete Next-Step Sequence

Recommended operations after accepting this review:

```bash
git switch experiments/waves
git status --short
```

Decide the untracked strong-candidate/excerpt files under `results/mutbench/codex_wave5/worksheets/`: either add them to the Wave 5 freeze commit because they are useful curator aids, or remove them from the working tree before merge if they were scratch. Do not leave them untracked.

Create:

```text
paper/dissertation/review/2026-05-01/wave5/w5_status.md
results/mutbench/codex_wave5/README.md
```

Add to `NOTES.md` under 2026-05-01 or 2026-05-02:

```text
- Wave 5 freeze (2026-05-02): Wave 5 is frozen at Task 2. Tasks 1-2 produced PubMed/evidence/worksheet infrastructure for YFV E, Lassa GPC, and WNV E; Task 3 human Layer A curation is infeasible for the defense window; Tasks 4-6 were not run. No Wave 5 validation result or manuscript result claim exists. Resume requires human-completed worksheets plus explicit approval manifest.
```

If adding thesis prose, paste only this sentence at the end of the Wave 5 paragraph in `chapters_en/ch5_discussion.tex` future work:

```latex
For Wave 5 pilot 3, the automated PubMed inventory and per-position worksheet infrastructure for YFV E, Lassa GPC, and WNV E have been prepared as reproducibility artefacts, but the human Layer~A curation checkpoint remains incomplete; no curated labels, integration run, or validation claim is included in this dissertation.
```

Then:

```bash
git add NOTES.md paper/dissertation/review/2026-05-01/wave5/w5_status.md results/mutbench/codex_wave5/README.md
git add results/mutbench/codex_wave5/worksheets/w5_*_strong_candidates.csv results/mutbench/codex_wave5/worksheets/w5_*_strong_excerpts.md   # only if keeping curator aids
git commit -m "docs: freeze Wave 5 at human curation checkpoint"
git switch master
git merge --ff-only experiments/waves
git tag backup/experiments-waves-merged-2026-05-02
git branch -d experiments/waves
git push origin master backup/experiments-waves-merged-2026-05-02
git push origin --delete experiments/waves   # only after confirming remote policy
```

If `--ff-only` fails because master moved, stop and inspect; do not resolve by rewriting history.

## 5. What I Would Not Do

- Do not silently delete v204/v205. The artifacts exist, `NOTES.md` records them, and the backup tag preserves the trail. Deleting them now looks more like concealment than rigor.
- Do not write Wave 5 as a result paragraph in Chapter 4. There are no human labels, no integration, no LOPO rerun, and no closure review.
- Do not call Branch C as if it fired. Branch C requires attempted human curation yielding 0/3 targets with enough high-confidence positives. Here Task 3 did not occur; the honest branch is "stopped at human checkpoint."
- Do not leave only Option B's implicit state. It is technically accurate but too easy to misread as abandoned partial execution.
- Do not keep `experiments/waves` as a live branch after merging the chosen disposition. The branch name will otherwise remain a tempting but stale base for future work.
