# Compression execution — Tasks 1 + 2 (no appendix)

Execute the editing task NOW. Workspace-write OK. Do not commit.

## Constraints

- **No appendix is allowed.** All evidence must remain in main text (chapters_en/).
- **Preserve every negative result and every numerical value** verbatim (e.g.,
  `0/12 callable`, `p=0.78`, `Branch C`, `MCC=-0.055`, `1/12 (Norovirus)`,
  Shapley values, percentages).
- **Preserve all `\label{}` declarations and `\ref{}`/`\cite{}` cross-references** —
  do not break the build.
- Build must remain `0 errors / 0 undefined refs / 0 multiply-defined`.
- Length budget: target -7 to -10 pages from current 241 pages (i.e., 231-234
  pages). Hard ceiling: do not exceed the 7-paragraph trim scope listed
  below.

## Task 1 — Audit ledger table + trim 9 audit paragraphs

### Step 1.1 — Add new summary table

Insert a new `table` environment titled
`\caption{Robustness audit ledger: pre-registered audits, key results, and
boundaries imposed.}` with `\label{tab:audit_ledger}` immediately AFTER
the existing `\begin{algorithm}` block (around `chapters_en/ch4_results.tex:715`).

Table columns: `Audit` | `Question / null` | `Headline result` | `Boundary imposed` | `Section`

Table rows (one per audit, ≤2 lines each in the source LaTeX):
1. **P1 null calibration** — 100k-perm × 4 nulls / does scoring beat null? — 5/12 iid sig → 1/12 under strict local-burden (Norovirus only); Stouffer global $p=1.0$ — Algorithm 1 reframed as exploratory, callable subset only — `\ref{para:null_calibration}`
2. **P2 rank reliability** — top-vs-bottom decile bootstrap / is rank reliable? — 3-core +0.084, 4-core +0.063, full-10 +0.043 vs random +0.011; Rabies inverts — operational claim = ranked screening-budget allocator, not calibrated probability — `\ref{para:rank_reliability}`
3. **P3 full lattice + Shapley** — 1023 subsets / is 4-core best? — 4-core rank 87/1023; 3-core (freq, entropy, homoplasy) dominates at rank 27; pLDDT Shapley $-0.0015$, ESM-2 $-0.0144$ — 4-core characterized as historical, not optimal — `\ref{para:full_lattice_shapley}`
4. **P5 callability + abstention** — D1-D4 conjunction, 32-config sensitivity sweep / can we deploy? — $\mathbf{0/12}$ callable across all sweep configs at quorum $\geq 6/11$ — formal abstention; deployment refused on current panel — `\ref{para:p5_callability}`
5. **P6 biological-realistic nulls** — 4 structural nulls, 100k perms each / signal vs structural clustering? — 5/12 (sasa, plddt), 4/12 (joint) for 4-core; Norovirus passes all 4 + P1 strict — descriptive signal under structural conditioning, not deploy claim — `\ref{para:p6_biological_nulls}`
6. **Wave 4 Tier 2 features-only LOPO** — labeled 12-fold + 28-target stability / does $n\approx30$ dissolve panel-size limit? — 0/3 hscore harmonized → 2-core fallback; mean MCC $0.077$, $8/12$ positive, $p=0.368$ vs 4-core; D1=0/12; 1/28 stable; 16/16 envelope-compatible — panel-size limit not relaxed; Layer A curation rate-limiting — `\ref{para:w4_tier2_lopo}`
7. **Wave 5 Layer A$'$ UniProt sensitivity** — 10 UniProt-feature targets / is label provenance interchangeable? — mean MCC $-0.055$, $2/10$ positive, sign **negative** opposite to 12-panel; cross-panel Welch $p=0.0089$; Branch C — Layer A and Layer A$'$ not interchangeable; not panel extension — `\ref{para:w5_layer_a_prime}`
8. **HBFWS Bayesian shrinkage** — hierarchical pooling vs EqualWeight-4core / does adaptive beat baseline? — $\Delta = -0.020$, paired Wilcoxon $p=0.78$ — pre-registered hypothesis rejected at $n=11$ — `\ref{para:hbfws_check}` (or paragraph if no label)
9. **Cycle 7B six paradigms** — XGBoost / RF / LR / 1-NN / phylo HBFWS / rank agg / does any adaptive method beat EqualWeight? — all six fail nested-LOPO Wilcoxon (smallest $p=0.56$) — convergent failure across paradigms; constraint = panel size, not algorithm — `\ref{para:cycle7b_comparison}` (or paragraph if no label)

Make the table compact with `\small` and 5 columns; one row per audit.

### Step 1.2 — Trim each of the 9 paragraphs to ≤ 50% of current length

For each of P1, P2, P3, P5, P6, W4, W5, HBFWS, Cycle 7B paragraphs in
ch4_results.tex:

**KEEP** (do not cut):
- Headline numerical results (every percentage, every $p$-value, every MCC)
- Boundary statements (e.g., "Algorithm 1 reframed as...", "abstention...")
- Per-pathogen significance counts (5/12, 1/12, etc.)
- Branch fired (Branch C, etc.)
- Pre-registered prior probabilities

**CUT or COMPRESS**:
- Method detail (replace with "as described in Section X" cross-ref)
- Implementation specifics (chains, accept rate, sampler settings)
- Script and CSV path lists (replace with "(see Table~\ref{tab:audit_ledger})")
- Repeated cross-references already in the table
- Verbose connectors and rephrasing

Each compressed paragraph should END with: "(see Table~\ref{tab:audit_ledger})"
or similar pointer if not already cross-referenced.

## Task 2 — Statistical robustness detail consolidation

### Step 2.1 — Identify the 5-frame description across 3 locations

Three locations describe the same 5 inferential frames (cluster bootstrap /
wild bootstrap / phylogenetic block / mixed-effects / Bayesian factor):

- `chapters_en/ch3_methods.tex` Section "ANOVA Diagnostic Tests" around line 805-825 (method spec)
- `chapters_en/ch4_results.tex` "ANOVA Diagnostic Tests" around line 475-498 (result + 5-frame summary)
- `chapters_en/ch5_discussion.tex` Bolker small-cluster paragraph around line 182 (limitation + 5-frame restatement)

### Step 2.2 — Designate Ch3 as primary; trim Ch4 and Ch5

- **Ch3 (METHOD)**: keep all 5-frame implementation detail (pyMC version, $\hat{R}$,
  chains, hyperpriors, etc.). This is the canonical method description.
- **Ch4 (RESULT)**: replace 5-frame implementation detail with one sentence:
  "Five inferential frames were re-estimated under the implementations described
  in Chapter~\ref{ch:mutbench} Section~\ref{subsec:anova_diagnostics}." Keep
  the numerical bounds (`[0.195, 0.333]`, `[0.201, 0.303]`, etc.) and the
  Cohen-threshold conclusion. Remove repeated PyMC version, sampler settings,
  $\hat{R}$ values, ESS values, hyperprior names, sampler names.
- **Ch5 (LIMITATION)**: cite the same Section X cross-reference; keep only the
  conclusion that all 5 lower bounds exceed 0.14. Remove restatement of
  bounds and frame names.

## Output

After all edits:
1. Run `bash paper/dissertation/build.sh digital` and report:
   - Final page count
   - Pages saved (target 231-234)
   - 0 errors / 0 undefined / 0 multiply-defined
2. Print a one-line summary:
   `RESULT_COMPRESS: pages_before=241 pages_after=<N> saved=<N> errors=<N>`

Do not commit. Do not modify other chapters or front matter.
