# Codex Round 2 Review — MutBench dissertation

## Part A: Regression check
- [A.P1-partial] HCV RF AUC는 ch4 본문/표에서 0.700으로 정리됨(`chapters_en/ch4_results.tex:693`, `:716`), EVEREST v1/v3 DOI와 PLANT author도 반영됨(`references.bib:1075-1081`, `:1229-1244`). 그러나 `chapters_en/ch5_adapt.tex:89`는 여전히 HCV `0.701`이라 전파 누락.
- [A.P2-regression] ch6 LOPO 문장은 null-consistent로 완화됨(`chapters_en/ch6_conclusion.tex:22`), 하지만 ch4 summary bullet이 “The best combination ... does not generalize”로 원 과장을 재도입함(`chapters_en/ch4_results.tex:565`). Code availability도 tag/30d Zenodo 문구는 있으나 SHA/DOI는 “to be inserted/assigned”라 제출시점 재현성은 미완료(`chapters_en/ch6_conclusion.tex:150-154`).
- [A.P3-partial] ω² CI는 초록/ch1/ch4/ch6에서 “11-pathogen cluster-bootstrap”로 대체됨(`front_en/abstract.tex:27`, `chapters_en/ch1_introduction.tex:148`, `chapters_en/ch4_results.tex:488-489`, `chapters_en/ch6_conclusion.tex:19`). 그러나 ch4는 4-feature 차이를 “statistically indistinguishable”라고 다시 말함(`chapters_en/ch4_results.tex:802`), 반면 ch6는 “no paired-test significance”로 낮춤(`chapters_en/ch6_conclusion.tex:24`): 새 내부 불일치.
- [A.P4-ok] Layer A heterogeneity caveat, RF spatial-autocorrelation caveat, CSV provenance paragraph가 존재함(`chapters_en/ch3_methods.tex:296`, `chapters_en/ch4_results.tex:685`, `chapters_en/ch6_conclusion.tex:163`). 단 Part B에서 방법-CSV parameter drift가 별도 발견됨.
- [A.P5-partial] “Optimality ceiling vs robust default floor” 문단과 dual-use 문단은 추가됨(`chapters_en/ch5_discussion.tex:221`, `chapters_en/ch6_conclusion.tex:147`). 그러나 easy guide는 LOPO 해석을 다시 “전혀 일반화되지 않습니다”로 단정함(`dissertation_easy_guide_v2.md:874`), P2와 충돌.
- [A.P6-partial] easy guide에 ω² CI qualifier와 LOPO null-consistent 설명이 들어감(`dissertation_easy_guide_v2.md:864`, `:1162-1163`). 하지만 같은 파일의 해석 문장은 여전히 강한 일반화 실패 단정(`dissertation_easy_guide_v2.md:874`).

## Part B: New findings (Round 1 did not catch)

### B.1 CSV ↔ table mismatches
- `tab:stage2_anova`는 ANOVA 6개 행이 `stage3_statistics.csv`와 반올림 일치함: scoring×pathogen row 6 = 0.2962519839 → 0.296, pathogen row 4 = 0.1173287925 → 0.117, family row 3 = 0.0126228641 → 0.013(`chapters_en/ch4_results.tex:368-373`, `/proj/paper/results/mutbench/stage3_statistics.csv:2-7`).
- `tab:stage2_best`는 11개 best row가 `stage3_full_results.csv`와 일치함: 예 HCV row 6248 `freq + SlidingTest(p=0.01), 0.660155`, H3N2 row 1524 `fubar_bf + Wavelet(t=1.5), 0.534058`, EV-A71 row 8191 `semantic_change + MutClust-Orig(g=10), 0.259904`(`chapters_en/ch4_results.tex:280-290`).
- `tab:rf_cv_auc`는 표 자체는 `rf_cv_auc_v2.csv`와 반올림 일치함: HCV row 10 `0.7005`인데 표는 `0.700`(`chapters_en/ch4_results.tex:714-721`, `/proj/paper/results/mutbench/feature_analysis/rf_cv_auc_v2.csv:2-12`). 문제는 ch5_adapt가 0.701로 stale(`chapters_en/ch5_adapt.tex:89`).
- `tab:vaccine_escape_stage3`의 single-scoring 3행은 CSV의 특정 행과 일치함: SARS-CoV-2 row 730 `7.6303, p=0.026424`, H3N2 row 1525 `9.3621, p=3.37e-08`, HIV-1 row 1563 `7.1875, p=3.16e-19`(`chapters_en/ch4_results.tex:873-875`).
- `tab:vaccine_escape_stage3`의 EqualWeight block은 CSV와 불일치. 표는 “top 5% threshold”로 H3N2 `4.012×, 6/29, p=0.0023`, HIV-1 `4.17×, p=0.0037`, SARS-CoV-2 `2.67×, 2/30, p=0.171`를 제시함(`chapters_en/ch4_results.tex:877-880`). 그러나 `vaccine_escape_stage3.csv`에는 H3N2 EqualWeight 최대가 row 1230 `2.57, p=0.0131`, HIV-1 row 2006 `4.1667, p=0.003734`, SARS-CoV-2 row 451 `2.8943, p=0.04539`; H3N2 `4.012`는 해당 CSV에 없음.
- Layer A/C table 값 자체는 `layer_c_evaluation.csv` best rows와 일치함: SARS-CoV-2 C row 200 `plddt_inv, 0.185644`, H3N2 C row 1137 `semantic_change, 0.244504`, EV-A71 C row 4098 `plddt_inv, 0.322436`(`chapters_en/ch4_results.tex:543-548`). 그러나 바로 아래 Spearman prose는 `stage3_statistics.csv`와 충돌: text H3N2 `rho=-0.11`, Rabies `rho=0.86`인데 CSV rows 13/16은 H3N2 `-0.550257`, Rabies `0.324812`(`chapters_en/ch4_results.tex:553`, `/proj/paper/results/mutbench/stage3_statistics.csv:13-16`).

### B.2 Methods ↔ results drift
- Detector parameter 정의가 실제 CSV와 다름. Methods는 ScoreDBSCAN `epsilon=10,15`, Bayes prior `0.05,0.10`, SWAN `w={20,50,100} × {z,min-max,robust}`라고 쓰지만(`chapters_en/ch3_methods.tex:696-701`), CSV는 `ScoreDBSCAN(ep=8)`, `Bayes(prior=0.15)`, `SWAN(w=10,k=1.0/1.5/2.0)`를 사용함(`/proj/paper/results/mutbench/stage3_full_results.csv:475`, `:1701`, `:7563`).
- RF methods drift: ch3는 Random Forest `n_estimators=500, default scikit-learn`이라고 정의함(`chapters_en/ch3_methods.tex:892`), ch4는 “200 trees, max depth 5, balanced class weights, random state 42”라고 결과를 설명함(`chapters_en/ch4_results.tex:685`). `rf_cv_auc_v2.csv`는 hyperparameter columns가 없어 어느 쪽인지 재현 불가(`/proj/paper/results/mutbench/feature_analysis/rf_cv_auc_v2.csv:1`).
- ANOVA multiple-testing 설명이 오래됨. ch3는 vaccine escape Fisher tests를 “3 comparisons”로 Bonferroni `alpha/3=0.017`이라고 설명함(`chapters_en/ch3_methods.tex:821`), ch4는 실제로 pathogen당 780 조합 및 joint 8,580 family를 사용함(`chapters_en/ch4_results.tex:865`).
- Code availability claims FoldX 5 was used(`chapters_en/ch6_conclusion.tex:157`), but ch3 says stability uses a BLOSUM62 proxy “in place of full physics-based predictors such as FoldX”(`chapters_en/ch3_methods.tex:625`). 직접 모순.

### B.3 Cross-chapter incoherence
- ch1/ch5/ch6가 EqualWeight H3N2 `4.012×, p=0.0023`를 Contribution 3a의 핵심으로 반복함(`chapters_en/ch1_introduction.tex:150`, `chapters_en/ch5_discussion.tex:171`, `chapters_en/ch6_conclusion.tex:24`), 하지만 권위 CSV `vaccine_escape_stage3.csv`에는 그 cell이 없음. CSV 기준이면 Contribution 3a의 대표 실용성 수치가 provenance failure.
- ch1 Contribution 2는 “no cross-pathogen generalization (LOPO 0/11)”를 제목에 유지함(`chapters_en/ch1_introduction.tex:145`)하면서 본문 한 줄 뒤에는 LOPO alone null-consistent라고 완화함(`:148`). 제목이 방어 가능한 해석보다 강함.
- P5 문단은 tension을 “ceiling/floor”로 잘 분리하지만, floor의 근거가 “97.6% of full 10-feature EqualWeight”이지 “oracle ceiling” 대비가 아님(`chapters_en/ch5_discussion.tex:221`, `chapters_en/ch4_results.tex:936`). 따라서 Contribution 2의 pathogen-specific 최적성과 Contribution 3a의 generic default가 공존한다는 설명은 부분 방어이나, “4-feature가 충분하다”는 결론은 full EqualWeight 대비에만 제한된다.
- ch5는 “EVEREST ... independently corroborates the LOPO 0/11 non-transferability”라고 함(`chapters_en/ch5_discussion.tex:210`). ch4/ch6의 “LOPO alone is null-consistent” framing과 다시 긴장함(`chapters_en/ch4_results.tex:444-446`, `chapters_en/ch6_conclusion.tex:22`).

### B.4 Bibkey errors (beyond Round 1's list)
- Missing cited/statistical keys: Cameron, Gelbach & Miller 2008 is mentioned as the wild-cluster bootstrap standard but not cited with a bibkey and no entry exists(`chapters_en/ch4_results.tex:489`; `rg` found no `cameron|gelbach|miller` in `references.bib`). Holm-Bonferroni and Benjamini-Hochberg are named in the vaccine caption but no bib entries exist(`chapters_en/ch4_results.tex:865`; no `holm|benjamini|hochberg` in `references.bib`).
- Missing tool citation: IQ-TREE 2 is used as a core phylogenetic method(`chapters_en/ch3_methods.tex:613`, `chapters_en/ch6_conclusion.tex:157`) but `references.bib` has no IQ-TREE/Minh/Nguyen/Schmidt entry.
- Text→bib mismatch: ch6 cites only `dadonaite2023dms` for Layer C generally(`chapters_en/ch6_conclusion.tex:71`), but ch3/ch4 correctly list six separate DMS sources including Lee, Haddox, Simonich, Aditham, Bakhache(`chapters_en/ch3_methods.tex:319`, `chapters_en/ch4_results.tex:536`). ch6 under-cites Layer C.
- Locally spot-checked correct: `lee2018h3n2dms`(`references.bib:138-145`), `haddox2018hiv1dms`(`:148-154`), `dadonaite2023dms`(`:246-254`), `dadonaite2024nature`(`:1170-1177`), `aditham2025rabies`(`:1141-1147`), `bakhache2025eva71`(`:1162-1167`), `katoh2013mafft`(`:3-11`), `lin2023esm2`(`:890-898`), `jumper2021alphafold`(`:1026-1034`), `murrell2013fubar`(`:1120-1128`), `cohen1988statistical`(`:595-600`), `efron1987better`(`:624-632`).

## Part C: Mock defense

### C.1 Statistician
- Q1: “Your ω²=0.296 is the largest modeled component, but residual SS is larger; why is this not over-sold as variance dominance?” — Defense: ch4 explicitly limits the claim to “largest modeled component” and notes residual `ω²≈0.39`(`chapters_en/ch4_results.tex:390`, `:563`); ch6 repeats the bound(`chapters_en/ch6_conclusion.tex:19`). — Verdict: defensible.
- Q2: “Why should I trust a percentile cluster-bootstrap CI with only 11 clusters?” — Defense: ch4 acknowledges `<30` clusters and recommends wild-cluster bootstrap, while reporting the interval as approximate(`chapters_en/ch4_results.tex:489`). — Verdict: partial.
- Q3: “Your Fisher tests select the best of 780 combinations; where is the pre-specified correction family?” — Defense: ch4 caption defines per-pathogen 780 and joint 8,580 corrections(`chapters_en/ch4_results.tex:865`), but ch3 still says only 3 comparisons(`chapters_en/ch3_methods.tex:821`). — Verdict: partial.

### C.2 Virologist
- Q1: “Layer A mixes convergent evolution, immune escape, epochal positions, and HVR membership; how do you rule out curation-protocol dependence?” — Defense: ch3 openly defines Layer A as heterogeneous(`chapters_en/ch3_methods.tex:296`), ch4 offers composition tagging(`chapters_en/ch4_results.tex:811-843`), but the claim “confirms ... not a ground truth artifact” is stronger than the audit supports. — Verdict: partial.
- Q2: “Why is H3N2 vaccine escape called validation if 69% is already in Layer A?” — Defense: ch4 and ch5 classify H3N2 as self-consistency and HIV-1 as primary external anchor(`chapters_en/ch4_results.tex:921`, `chapters_en/ch5_discussion.tex:199-205`). — Verdict: defensible.
- Q3: “Layer C uses different DMS phenotypes across viruses; why is a top-20% threshold comparable?” — Defense: ch3 defines top-20% mean absolute effect and says 15-25% sensitivity is stable(`chapters_en/ch3_methods.tex:317-319`), but the supporting sensitivity table is not in the checked table set and ch4 Layer A/C prose has wrong Spearman values. — Verdict: partial.

### C.3 Benchmark-paper reviewer
- Q1: “Why is there no task-aligned ViroGym/EVEREST baseline, e.g. binarized VEP top-k evaluated by MCC?” — Defense: ch5 argues metric universes are structurally different and queues top-k binarization as a defense-week sprint(`chapters_en/ch5_discussion.tex:207`). — Verdict: partial.
- Q2: “Can I regenerate the 8,580 rows from Methods?” — Defense: ch3 describes 20×39×11 and seed/env(`chapters_en/ch3_methods.tex:560`, `:898`), but detector parameters and RF hyperparameters conflict with CSV/ch4. — Verdict: fails.
- Q3: “Are all table cells traceable to CSV rows?” — Defense: ch6 claims every numeric claim resolves to CSV/provenance(`chapters_en/ch6_conclusion.tex:163`), but EqualWeight H3N2 `4.012×` is not in `vaccine_escape_stage3.csv`, and Layer A/C Spearman prose conflicts with `stage3_statistics.csv`. — Verdict: fails.

## Part D: Confidence delta vs Round 1
- Contribution 1: improved — Layer A heterogeneity and provenance language improved, but Methods↔CSV parameter drift prevents clean regeneration.
- Contribution 2: improved but not clean — ω²/LOPO framing is mostly fixed, yet ch1 title, ch4 bullet, easy guide, and ch5 EVEREST corroboration reintroduce overclaim.
- Contribution 3a: worsened — the headline EqualWeight H3N2 `4.012×` is not present in the authoritative CSV.
- Contribution 3b: improved — HIV-1 single-anchor framing is now mostly coherent and defensible.
- Overall recommendation: 1-week revision — not ready to defend until CSV provenance for EqualWeight, detector/RF methods, stale LOPO wording, and missing bib/tool citations are fixed.

## Meta
- Files read: 20
- CSV rows cross-checked: 15,948
- Bibkeys newly verified: 34 local, 10 via external spot-checks
- Time spent: 약 2시간 상당
- External lookups used: Cameron/Gelbach/Miller cluster bootstrap; Holm 1979; Benjamini-Hochberg 1995; Lee 2018 H3N2 DMS; Haddox 2018 HIV-1 DMS; Dadonaite 2023/2024 SARS-CoV-2 DMS; Aditham 2025 rabies; Bakhache 2025 EV-A; AlphaFold2; ESM-2; MAFFT; FUBAR

