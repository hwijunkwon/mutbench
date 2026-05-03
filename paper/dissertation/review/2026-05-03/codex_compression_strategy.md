# Deep Compression Strategy: 241 pages to 215--225 pages

Assumption: one technical page is roughly 400--500 prose words, but LaTeX floats, captions, algorithms, and table notes dominate several target ranges. Savings below are therefore page-footprint estimates, not proportional word-count estimates. The safest target is 222 pages: about 19 pages saved while keeping all scientific evidence in the main thesis or appendix.

## 1. Page-by-page audit table

| # | File:line range | Current length | Scientific role | Compression strategy | Expected saving | Evidence-loss risk |
|---|---:|---:|---|---|---:|---|
| 1 | `chapters_en/ch4_results.tex:723-857` | ~2,300 words + 2 tables + algorithm; ~6--7 pp | Cold-start, subset lattice, nulls, callability, Wave 4/5, adaptive-weighting failures | Replace audit-log paragraphs with one "audit ledger" table: question, result, boundary, provenance. Move script paths, branch names, long null details, and Cycle 7B method prose to appendix. | 4.0--5.0 pp | Medium |
| 2 | `chapters_en/ch5_discussion.tex:338-340` | ~1,100 words; ~2.0--2.5 pp | Future roadmap for adaptive selection, expanded panel, Wave 4/5 linkage | Split into: 1 short future-work paragraph + appendix "expanded-panel audit details." Keep only panel-size conclusion and Layer A bottleneck. | 1.5--2.0 pp | Low-medium |
| 3 | `chapters_en/ch4_results.tex:475-526` | ~720 words + 2 tables; ~2.0--2.5 pp | Five-way robustness of $\omega^2$ and LOO sensitivity | Keep Table 4.9 and 3-sentence interpretation; move per-frame implementation details, LOO leverage prose, scripts/CSV paths to appendix/provenance note. | 1.2--1.8 pp | Medium |
| 4 | `chapters_en/ch3_methods.tex:805-825` plus `:846-862` | ~1,500 words; ~3 pp | Statistical design, cell-level/ANCOVA/Bayesian/ART/Mantel caveats | Convert to methods table: test, purpose, implementation, where result appears. Move non-performed Mantel/jackknife detail to limitations appendix. | 1.2--1.6 pp | Medium |
| 5 | `chapters_en/ch4_results.tex:305-325` | ~800 words; ~1.5 pp | Biological rationale for 11 per-pathogen winners | Table-ize rationales into 11 compact rows or move full biological rationales to appendix, leaving 3 examples in main text. | 0.8--1.2 pp | Low-medium |
| 6 | `chapters_en/ch3_methods.tex:539-604` | ~930 words + correlation table; ~2 pp | Structural/PLM source caveats; Tranception--ESM collinearity | Keep scoring table and one PLM caveat; move per-pathogen correlation table and Foldseek/AlphaFold-Multimer notes to appendix. | 0.8--1.2 pp | Medium |
| 7 | `chapters_en/ch5_discussion.tex:187-209` | ~730 words; ~1.5 pp | GISAID bias, ESM leakage, proxy collinearity, small-n inference | Merge repeated caveats with Ch3/Ch4 versions; keep only one "data/PLM/statistical limits" paragraph plus references to tables. | 0.8--1.0 pp | Low |
| 8 | `chapters_en/ch4_results.tex:435-443` | ~560 words; ~1 pp | Nemenyi and LOPO permutation tempering | Keep one sentence: Nemenyi finds no significant top-20 pair; LOPO gap is null-consistent. Move p-value distributions and CSV names. | 0.6--0.8 pp | Low |
| 9 | `chapters_en/ch5_discussion.tex:300-308` | ~270 words but dense; ~0.7 pp | Falsification-resistant audit summary and Wave 4/5 limitation | Merge into the same Ch4 audit ledger; retain boundary conclusion only in Ch5. | 0.5--0.7 pp | Low |
| 10 | `chapters_en/ch5_discussion.tex:352-390` | ~730 words + defense table; ~2 pp | Final claim map, dual-use, code/data provenance | Keep defense map. Compress dual-use and code/provenance into one availability paragraph + one provenance footnote. | 0.6--1.0 pp | Low-medium |
| 11 | `chapters_en/ch2_background.tex:230-285` | ~1,000 words + comparison table; ~2 pp | Benchmarking gap and VEP benchmark positioning | Keep comparison table; cut repeated prose after table. One paragraph before and one after table is sufficient. | 0.6--0.9 pp | Low |
| 12 | `chapters_en/ch3_methods.tex:622-728` | ~1,050 words + 2 tables; ~2.5 pp | Detection families and parameter variants | Merge family and parameter tables or move parameter table to appendix. Main text can cite 39 variants and explain why family-level ANOVA is used. | 0.8--1.3 pp | Medium |
| 13 | `chapters_en/ch3_methods.tex:197-212`, `:259-313` | ~900 words + GT table notes; ~2 pp | Layer A/B/C criteria and overlap handling | Keep table, move HIV count reconciliation and long HCV coordinate caveat to footnote/appendix. Avoid repeating Layer A heterogeneity. | 0.5--0.9 pp | Medium |
| 14 | `chapters_en/ch5_discussion.tex:240-258` | ~650 words; ~1.2 pp | PLM/data limits, prospective validation gap, DURC, MAFFT artifact | Convert to limitation table rows or merge with existing limitations table. Keep prospective gap paragraph intact. | 0.5--0.8 pp | Low-medium |
| 15 | `chapters_en/ch4_results.tex:937-955` | ~570 words + long table note before it; ~1.5 pp | Vaccine-escape provenance and search-space conclusion | Keep HIV-1 anchor, H3N2 self-consistency, SARS-CoV-2 exploratory status. Move pipeline provenance and denominator arithmetic to one global provenance note. | 0.5--0.8 pp | Medium |
| 16 | `chapters_en/ch2_background.tex:88-123` and `:124-166` | ~2,000 words; ~4 pp | DMS and PLM/VEP background | Trim tutorial material; keep only what motivates Layer C and task distinction. | 0.8--1.2 pp | Low |

Conservative total from the top 12 items: 14--19 pages. Adding items 13--16 reaches 18--24 pages.

## 2. Structural moves analysis

The best compression is structural, not sentence-level. The manuscript currently spends many pages proving that weaknesses were audited. That evidence should remain, but the main text should report the audit answer, not the audit transcript.

Recommended appendix structure:

1. `Appendix A: Robustness and Provenance Audits`
2. `A.1 Statistical robustness implementation details` for cluster/wild/phylogenetic/Bayesian frames, jackknife/Mantel non-performed notes, and LOO leverage table.
3. `A.2 Cold-start and adaptive-weighting audit ledger` for full-lattice Shapley, P1/P5/P6, Wave 4/5, HBFWS, Cycle 7B.
4. `A.3 CSV-to-table provenance` for script names, CSV filenames, row-index claims, Bonferroni denominators, and pipeline differences.
5. `A.4 Extended method catalog` for detector-parameter table, PLM channel-correlation table, structure-source caveats, and external-license matrix.

Tables should replace prose in three places: Ch4 audit block, Ch5 future-work expansion block, and Ch3 statistical-method implementation detail. The most efficient table columns are "question", "result", "boundary imposed", and "where archived." This preserves defense readiness while removing branch-log style text from the main narrative.

Repeated caveats should be consolidated. Layer A heterogeneity appears in Ch3 ground truth, Ch4 ground-truth heterogeneity, Ch5 circularity/limitations, and the defense map. Keep the operational definition in Ch3, the quantitative sensitivity in Ch4, and a single limitation statement in Ch5. Similarly, Bolker/small-cluster caveats should appear once in Ch3 methods and once in Ch5 limitations, not in every robustness paragraph.

CSV pointers should be centralized. Replace repeated `script:` and `CSV:` clauses with one footnote: "All script-to-CSV provenance for Tables X--Y is listed in Appendix A.3." Keep only load-bearing table source names when a table would be unverifiable without them.

## 3. Risk assessment

The largest risk is weakening the defense against "you overfit and then hid the failed audits." For Ch4 `723-857`, do not delete the negative results. Compress them into an audit ledger that explicitly says: 4-core not lattice-optimal, callability 0/12, Wave 4 features-only expansion does not solve panel size, Layer A$'$ is negative, seven adaptive paradigms fail. The defense question at risk is "what prevents this from being a deployable predictor?" The same content exists again in Ch5 `300-312` and future work `338-340`, so deduplication is safe if the ledger remains.

For statistical robustness (`ch4:475-526`, `ch3:805-825`), the evidence at risk is the claim that $\omega^2$ survives small-cluster objections. The defense question is "is $N=8,580$ pseudo-replication?" Keep the five lower bounds and cell-level value in main text; move implementation details and scripts. This is partially duplicated across Ch3 methods, Ch4 results, and Ch5 small-n limitations.

For PLM/proxy caveats (`ch3:539-604`, `ch5:194-205`), the risk is overclaiming PLM family superiority. Keep the fact that Tranception is an ESM-2 proxy and near-collinear for 11/12 pathogens. The full correlation table can move because the conclusion is repeated in Ch5.

For vaccine escape (`ch4:937-955`, `ch5:128-149`), the risk is weakening Contribution 3. Keep HIV-1 as primary external anchor, H3N2 as self-consistency, SARS-CoV-2 exploratory, and 3/11 availability. Move pipeline notes and denominator arithmetic. The defense question is "is this independent validation?" The answer already appears in both Ch4 and Ch5, so one concise version is enough.

For related work (`ch2:230-285`), the risk is losing task-boundary protection against ViroGym/EVEREST/ProteinGym. Keep the comparison table and one paragraph stating region-level detection is distinct from per-variant VEP. Delete repeated uniqueness prose after the table.

## 4. Recommended plan

Target: 222 pages, acceptable range 215--225. Estimated saving: 18--22 pages. Wall time for one experienced editor: 2.5--4 working days, plus one build/reflow pass.

Sequence by yield/risk:

1. Convert Ch4 `723-857` and Ch5 `300-312`, `338-340` into one main audit ledger plus appendix detail. Save 6--8 pages.
2. Consolidate statistical robustness detail across Ch3 `805-825`, Ch4 `475-526`, and Ch5 `207-211`. Save 2.5--4 pages.
3. Compress Ch3 method catalogs: detector variants, PLM correlation/structure caveats, external licenses. Save 2--3.5 pages.
4. Table-ize per-pathogen biological rationales in Ch4 `305-325`. Save ~1 page.
5. Consolidate vaccine-escape provenance and CSV pointers across Ch4/Ch5. Save 1--1.5 pages.
6. Trim related-work tutorial/background sections while preserving the benchmark comparison table. Save 1.5--2 pages.
7. Merge limitations paragraphs into the existing limitations table; keep prospective gap, Layer A heterogeneity, and DURC. Save 1--1.5 pages.

Keep as-is: abstract length, Ch1 contribution hierarchy, headline Ch4 tables/figures (`stage2_best`, ANOVA decomposition, LOPO, feature ablation, vaccine escape), Ch5 defense map, and the prospective/time-forward limitation paragraph. These carry high defense value per page.

## 5. Aggressive option

If the author accepts a single appendix that may draw "why is this in appendix?" questions, target 215--218 pages by moving the following wholesale:

- Ch4 `806-857`: P5/P6, Wave 4/5, HBFWS, Cycle 7B implementation details; keep only the audit ledger in main text.
- Ch3 `669-702`: detector-parameter variants table.
- Ch3 `576-604`: Tranception--ESM correlation table.
- Ch4 `501-525`: per-pathogen leave-one-out leverage table.
- Ch5 `378-390`: numerical artifact CSV list.
- Ch3 `920-935`: external-resource license bullet list.

Additional saving: 5--8 pages beyond the recommended plan. Risk: medium. The committee may ask why robustness evidence is not in the main chapter, so the main-text ledger must cite the appendix explicitly and preserve every negative result in one-line form.
