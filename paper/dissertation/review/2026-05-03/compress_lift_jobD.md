# Compression-with-lift review -- Job D: ch5_discussion

Scope: `paper/dissertation/chapters_en/ch5_discussion.tex` post-compression state.

## Candidates

1. **Future-work programme / Wave 2-5 repetition**
   - File:lines 300-312 and 338-340.
   - Current function: Lines 300-312 set the claim boundary for Algorithm 1 using Wave 1-5 audits; lines 338-340 restate adaptive-selection, callability, Wave 4, and Wave 5 again inside Future Research Directions.
   - Compression strategy: Keep the detailed audit block once, then make Future Research Directions a forward-looking synthesis: one sentence for the adaptive null, one sentence for the expansion requirement, and a compact roadmap table with statuses ("done negative", "engineering feasible", "future"). Remove repeated D1 quorum, 32-config sensitivity sweep, Wave 4, and Wave 5 numerics from line 340 because they already appear at 302-308.
   - Expected page saving: 0.9-1.2 pages.
   - Expected score impact: lift. The defense line becomes easier: "all deployment gates failed; next work is expanded external labels."
   - Risk level: Low-medium. Must preserve the exact 0/12 callable and Layer A' negative result somewhere; they already remain in lines 302-308.

2. **Limitations prose plus limitations table consolidation**
   - File:lines 184-258, 273-298.
   - Current function: Separate limitation subsections cover phylogeny, GISAID, ESM leakage, Tranception/ESM collinearity, Simpson's-paradox, winner's curse, Bolker/small-n, reproduction, technical covariates, Layer A heterogeneity, sub-lineage pooling, scope, PLM/data, prospective validation, DURC, and MAFFT. A summary table then repeats only a subset.
   - Compression strategy: Expand `tab:limitations_summary` into a "defense limitations matrix" with columns: limitation, empirical bound, mitigation, future test. Keep only short lead-in paragraphs for the highest-risk issues: Layer A heterogeneity, prospective/time-forward failure, and dual-use. Move MAFFT, ESM leakage, GISAID, Bolker, sub-lineage pooling, winner's curse, and reproduction into table rows.
   - Expected page saving: 1.0-1.5 pages.
   - Expected score impact: lift. A table is more examiner-friendly and reduces the impression of accumulating caveats.
   - Risk level: Medium. Some nuance may be lost unless the table includes the key numeric bounds: ESM collinearity 11/12, 0/12 callable, grand mean forward AUROC 0.539, Bolker 20-30, and Layer A subset omega values.

3. **Code/data availability and numerical artifact listing**
   - File:lines 375-390.
   - Current function: Licenses, archive location, upstream license caveat, runtime, environment, no-redistribution policy, and CSV-to-table provenance list.
   - Compression strategy: Convert to a 4-row table: repository/release, licenses, redistributed artifacts, reproducibility/provenance. Move the long CSV bullet list into one sentence pointing to the provenance manifest, naming only the three load-bearing CSVs (`stage3_full_results.csv`, `vaccine_escape_stage3.csv`, `feature_ablation_nested_lopo_summary.csv`).
   - Expected page saving: 0.3-0.5 pages.
   - Expected score impact: neutral to lift. Prose becomes less administrative while retaining auditability.
   - Risk level: Low, if the manifest truly contains row-to-table provenance.

4. **Take-home message and concluding remarks overlap**
   - File:lines 349-373.
   - Current function: The conclusion paragraph, defense map, and take-home message all repeat the same central claim: information-source choice dominates detector choice, with bounded deployment.
   - Compression strategy: Delete the standalone take-home message at line 371 or fold it into the first sentence of line 352. Let `tab:defense_map` carry the oral wording.
   - Expected page saving: 0.1 page.
   - Expected score impact: neutral to lift. Removes a visible echo immediately after the defense map.
   - Risk level: Very low.

5. **Dual-use duplication**
   - File:lines 249-253 and 373.
   - Current function: DURC/ethics subsection gives policy classification and mitigations; final dual-use paragraph repeats the same mitigations in broader responsible-stewardship language.
   - Compression strategy: Keep the detailed DURC/ethics subsection where limitations are discussed. Replace the final dual-use paragraph with a 2-sentence cross-reference: outputs are dual-use because they prioritize immune-escape-relevant regions; release mitigations and IBC/P3CO boundaries are specified in Section `sec:durc_ethics`.
   - Expected page saving: 0.25-0.4 pages.
   - Expected score impact: lift. Keeps stewardship signaling without sounding defensive twice.
   - Risk level: Low.

6. **Pathogen-aware adaptive method selection residue**
   - File:line 338.
   - Current function: Combines adaptive-oracle ceiling, seven failed paradigms, negative-test rule, next-step roadmap, Tier 1 pilot, Tier 2 pilot, cross-pathogen subset construction, accession provenance, and bottleneck diagnosis.
   - Compression strategy: Split the paragraph conceptually, not visually: one compact "result" sentence and one "scaling pilot" sentence. Move target lists and `13/19`/`3+13+3` arithmetic to a table footnote or provenance manifest.
   - Expected page saving: 0.4-0.6 pages.
   - Expected score impact: lift. The current paragraph asks the examiner to retain too many bookkeeping details before reaching the claim.
   - Risk level: Low-medium. Avoid deleting the distinction "features extension, not benchmark-validated panel expansion."

7. **Vaccine escape / multi-source integration repeated from Ch4**
   - File:lines 128-135 and 141-154.
   - Current function: Re-explains enrichment values, multiple-comparison status, Layer A overlap, integration-vs-single comparability, practical value, and task orthogonality.
   - Compression strategy: Merge the two vaccine subsections into one "External validation by vaccine-escape enrichment" subsection. Keep the three-tier evidence rule and one sentence explaining the fixed EqualWeight H3N2 number. Drop the historical Stage 1 note or move it to a parenthetical.
   - Expected page saving: 0.35-0.6 pages.
   - Expected score impact: lift. This reads as results recapitulation; Ch5 should interpret.
   - Risk level: Low.

8. **Practical workflow paragraph and scoring-prior table**
   - File:lines 157-181.
   - Current function: Provides a four-step operational workflow, runtime estimates, cold-start core, family priors, and two-regime interpretation.
   - Compression strategy: Turn line 160 into a concise numbered list or a 4-column workflow table. Keep the family-prior table only if it is used in defense; otherwise compress it into a sentence naming the strongest priors and warning they are first-pass.
   - Expected page saving: 0.25-0.4 pages.
   - Expected score impact: neutral to lift. Better scanability; small risk of losing useful operational detail.
   - Risk level: Low.

9. **Scope and future research overlap**
   - File:lines 229-235 and 344.
   - Current function: The scope section explains RNA-virus-only, DNA-virus rate gap, HBV pilot, small-n caveats, and within-family heterogeneity; future research repeats DNA-virus/multi-protein/indel/retrovirus/non-viral exclusions.
   - Compression strategy: Keep the empirical HBV sanity check in the scope section. In future research, replace the long out-of-scope paragraph with a short pointer: "Scope extensions are DNA viruses, multi-protein panels, indels/recombination, and non-coding regions; current evidence does not support claims outside RNA-virus surface-glycoprotein substitutions."
   - Expected page saving: 0.25-0.35 pages.
   - Expected score impact: lift. Removes defensive redundancy while preserving boundary clarity.
   - Risk level: Low.

## Top 3 Recommended

1. **Future-work programme / Wave 2-5 repetition** (candidate 1): ~1.0 page saved, score lift.
2. **Limitations prose plus limitations table consolidation** (candidate 2): ~1.2 pages saved, score lift.
3. **Code/data availability and numerical artifact listing** (candidate 3): ~0.4 pages saved, neutral-to-lift.

Combined top-3 expected saving: ~2.6 pages. Combined score impact: +0.3 to +0.5, mainly by making the defense boundaries easier to audit.

## Sample compressed prose for #1

```tex
\textbf{Adaptive method selection and prospective callability.}
The current panel supports adaptive selection as a direction, not as a deployable result: the adaptive-weight oracle exceeds EqualWeight in principle (MCC $0.160$ vs.\ $0.083$), but seven tested adaptive paradigms fail to beat EqualWeight under nested-LOPO, and the predeclared abstention rule calls $0/12$ folds. Wave 4 shows that the expanded-target feature pipeline is feasible but not yet label-validated (D1 remains $0/12$; expanded sign stability $1/28$), while Wave 5 shows that UniProt-derived Layer A$'$ labels are not interchangeable with literature-curated Layer A (mean LOPO MCC $=-0.055$, $2/10$ positive folds). The next test is therefore not another weighting model on the same panel, but a 20--30+ pathogen expansion with curated external labels, time-forward validation, and the same paired nested-LOPO/callability gates. Until those gates pass, Algorithm~\ref{alg:mutbench_coldstart} remains a retrospective prioritization heuristic rather than a prospective classifier.
```

RESULT_JOBD: candidates=9 top3_pages_saved=2.6 top3_score_impact=+0.4
