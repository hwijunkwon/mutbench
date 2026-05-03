# Compression-with-lift review -- Job C: ch4_results

Scope: `paper/dissertation/chapters_en/ch4_results.tex` post-compression state.

## 1. Candidates

### C1. Per-pathogen biological rationales after `tab:stage2_best`

- File: `paper/dissertation/chapters_en/ch4_results.tex:305-325`
- Current role: Explains the biological rationale for each pathogen's best scoring type in 11 prose bullets, then adds detector-family and low-tier MCC observations.
- Compression strategy: Replace the 11-item paragraph list with a compact table: pathogen, best scoring, biological signal, one-line caveat. Keep 2-3 prose sentences before/after. This mirrors the audit-ledger pattern: parallel biological rationales become evidence findable at a glance. It can also remove repetition with `tab:stage2_best`, `fig:scoring_detection_heatmap`, and later feature-AUC discussion.
- Expected page saving: 0.8-1.1 pages.
- Expected score impact: lift. Improves defense quality because examiners can see all pathogen-specific rationales in one aligned object instead of searching a long list.
- Risk level: Medium. Some nuance, especially Norovirus, Dengue, MERS, and Influenza B, needs preservation in the table's caveat column or a short follow-up sentence.

### C2. ANOVA diagnostic prose duplicated around robustness table

- File: `paper/dissertation/chapters_en/ch4_results.tex:475-526`
- Current role: Reports assumption checks, effective-N caveat, cluster bootstrap provenance, naive bootstrap sensitivity, five inferential frames, the five-way table, HCV exclusion, 11-pathogen LOO sensitivity table, and Kruskal-Wallis.
- Compression strategy: Let `tab:omega_robustness_5way` carry the five inferential frames and let `tab:omega_loo_pathogen_sensitivity` carry the leave-one-out values. Reduce prose to: assumptions rejected but residual non-normality mild; cluster/bootstrap frames keep all lower bounds above 0.14; LOO range [0.253, 0.313], HCV largest leverage but not decisive; ground-truth heterogeneity caveat remains. Move script/CSV provenance to captions or one appendix-style provenance sentence.
- Expected page saving: 0.6-0.9 pages.
- Expected score impact: lift. It keeps all five lower bounds while making the logic easier to defend.
- Risk level: Low-Medium. Avoid deleting the effective-N warning; that is defense-critical.

### C3. Vaccine-escape validation caption plus follow-on narrative

- File: `paper/dissertation/chapters_en/ch4_results.tex:929-973`
- Current role: Defines enrichment and Fisher test, presents table, then a very long table footnote with Bonferroni/provenance/circularity details, followed by key findings, H3N2 self-consistency details, availability exclusions, and a circularity audit.
- Compression strategy: Split information into a compact `escape audit` table or extend the existing table with columns for `Bonferroni tier`, `Layer-A overlap`, and `role` (external anchor / self-consistency / exploratory). Then shorten caption and prose. Keep formula only if not already defined elsewhere; otherwise cite definition. Denominator arithmetic can be a one-sentence footnote: "Bonferroni uses 780 tests per pathogen; 8,580-test correction does not change tier assignment."
- Expected page saving: 0.6-0.8 pages.
- Expected score impact: lift. The current version is defensible but hard to parse; a role/tier table makes the HIV-1 anchor and H3N2/SARS-CoV-2 limits immediately visible.
- Risk level: Medium. This is a high-scrutiny result, so retain HIV-1 novel-only adjusted p-value and the H3N2/SARS-CoV-2 circularity warnings.

### C4. Cold-start algorithm intro and algorithm box

- File: `paper/dissertation/chapters_en/ch4_results.tex:694-721`
- Current role: Presents Tier 1 and Tier 2 cold-start recipe, empirical anchors, complexity claims, caveats, and formal pseudocode.
- Compression strategy: Shorten the prose before Algorithm 1 to three parts: purpose, Tier 1 recipe/evidence, Tier 2 caveat. In the algorithm box, collapse Step 1 into a single vectorized row or use `\ForEach{$f$ ...}` with feature definitions moved to text/caption. Remove per-line complexity comments inside the algorithm and report complexity once in prose.
- Expected page saving: 0.4-0.6 pages.
- Expected score impact: lift/neutral. The algorithm becomes less intimidating and easier to cite; risk is losing operational clarity if over-compressed.
- Risk level: Low-Medium.

### C5. Information-type analysis opening duplicates itself

- File: `paper/dissertation/chapters_en/ch4_results.tex:616-624`
- Current role: Introduces 20 scoring formulas/10 features twice, then gives a dense all-in-one paragraph with feature categories, per-pathogen AUC winners, RF CV, correlation structure, leakage caveat, and mechanistic conclusion.
- Compression strategy: Delete one of the two introductory restatements. Convert the dense AUC/correlation material into a small table with `Feature family`, `where it wins`, `diagnostic caveat`, or fold the per-pathogen AUC winners into the same table proposed in C1. Keep RF/leakage caveat in one sentence.
- Expected page saving: 0.3-0.5 pages.
- Expected score impact: lift. Reduces method restatement and improves connection between Stage 2 result and mechanism.
- Risk level: Low.

### C6. Worst-end disclosure paragraph

- File: `paper/dissertation/chapters_en/ch4_results.tex:294-296`
- Current role: Provides transparency on the worst cell, negative-MCC fraction, worst detector/scoring families, and interpretation of the cell-level floor.
- Compression strategy: Replace with a small four-row "floor audit" table: worst cell, negative-MCC fraction, worst detector families, worst scoring channels. Follow with one sentence connecting the floor to pathogen-adaptive selection.
- Expected page saving: 0.3-0.45 pages.
- Expected score impact: lift. The transparency remains, but the current single paragraph is too long to audit quickly.
- Risk level: Low.

### C7. Search-space reduction protocol restatement

- File: `paper/dissertation/chapters_en/ch4_results.tex:922-928`
- Current role: Re-explains EqualWeight production versus nested-LOPO protocols and repeats top-10% threshold/MCC results already developed in feature ablation.
- Compression strategy: Reduce to two sentences: "Search-space reduction is evaluated using the EqualWeight production protocol and the nested-LOPO sign-fit protocol described above; their means differ by <=0.013 MCC, so sign fitting is not load-bearing. At top 10%, EqualWeight mean MCC is 0.083 on 12 pathogens versus 0.075 for frequency-only and ~0 for random." Full protocol details can stay in Chapter 3/MutBench methods.
- Expected page saving: 0.25-0.35 pages.
- Expected score impact: neutral/lift. Removes method restatement in results.
- Risk level: Low.

### C8. Adaptive-weighting comparison prose after table

- File: `paper/dissertation/chapters_en/ch4_results.tex:847-878`
- Current role: HBFWS paragraph and Cycle 7B table/prose establish seven adaptive-weighting failures at n=11.
- Compression strategy: Since `tab:audit_ledger` and `tab:adaptive_weighting_comparison` already hold the facts, shrink HBFWS to a bridge sentence and shrink the post-table prose to one conclusion sentence. Keep the single positive EV-A71 fold only if needed as a caveat in the table caption or a note.
- Expected page saving: 0.25-0.4 pages.
- Expected score impact: neutral/lift. Avoids re-arguing a conclusion already made by the table.
- Risk level: Low.

## 2. Top 3 recommended

1. C1, per-pathogen rationales table: best compression/readability tradeoff; saves about 0.8-1.1 pages and makes the biological defense more inspectable.
2. C2, ANOVA diagnostics prose: saves about 0.6-0.9 pages while preserving all five lower bounds and the LOO sensitivity table.
3. C3, vaccine-escape validation consolidation: saves about 0.6-0.8 pages and clarifies which evidence is external versus self-consistency/exploratory.

Combined top-3 expected saving: about 2.0-2.8 pages. Expected score impact: +0.3, mainly from readability and defense traceability rather than new evidence.

## 3. Sample compressed prose for C1

After Table~\ref{tab:stage2_best}, replace the 11 bullets with:

> The biological interpretation is summarized in Table~X. The winning scores are not arbitrary detector artifacts: they track the dominant usable signal in each pathogen, including phylogenetic selection in H3N2, homoplasy in Norovirus, PLM-derived constraints in SARS-CoV-2/RSV, structural tolerance in Rabies, entropy in HIV-1, and frequency in HCV/MERS/Influenza~B. The important point is not that every rationale is independently proven by this benchmark, but that the observed winners map onto plausible, pathogen-specific information channels rather than a single universal scoring family. Detector choice also varies (KDE 4, Wavelet 3, SlidingTest/Bayes/MutClust/SWAN 1 each), but the larger modeled effect is the scoring-by-pathogen interaction. The lowest best-MCC tier remains SARS-CoV-2, RSV, and MERS, where shallow phylogeny, sparse positives, or broad calling limits achievable MCC.

The companion table should have columns: `Pathogen`, `Best scoring`, `Dominant biological signal`, `Defense caveat`.

RESULT_JOBC: candidates=8 top3_pages_saved=2.4 top3_score_impact=+0.3
