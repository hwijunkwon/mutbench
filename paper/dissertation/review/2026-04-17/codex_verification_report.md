# Codex Independent Review — MutBench dissertation

## Critical (fix before submission)

- [C1] 한국어 본문이 정본과 충돌 — `chapters/ch1_introduction.tex:44`, `chapters/ch1_introduction.tex:61`, `chapters/ch4_results.tex:695`, `chapters/ch4_results.tex:770`, `chapters/ch4_results.tex:809`, `chapters/ch5_discussion.tex:142` — 한국어판은 여전히 9 pathogens, 3,159 evaluations, LOPO 0/9, `family × pathogen ω²=0.285`, Friedman `p=0.0015`를 본문 결론으로 서술한다. 영어판/초록의 정본은 11 pathogens, 8,580 evaluations, LOPO 0/11, `scoring × pathogen ω²=0.296`, Friedman `p=0.990`이다. `chapters/ch4_results.tex:5`의 판본 안내만으로는 학위논문 본문 충돌을 해결하지 못한다. 한국어 장 전체를 동기화하거나 한국어 본문을 제출본에서 제외해야 한다.

- [C2] 결과 CSV/JSON 부재로 표 검증 불가능 — `chapters_en/ch4_results.tex:707`, `chapters_en/ch6_conclusion.tex:106` — 본문은 `rf_cv_auc_v2.csv` 및 “CSV-row-to-table-cell provenance manifest”를 전제로 하지만, 작업 디렉터리에는 `results/` 디렉터리도 CSV도 없다. 따라서 Table 4.3/4.9/4.13 및 headline numbers를 원자료에 대해 독립 검산할 수 없다. 제출 전 `results/*.csv`, `results/*.json`, provenance manifest를 포함하거나 본문에서 재현 가능성 주장을 낮춰야 한다.

- [C3] LOPO 해석이 장별로 다시 과장됨 — `chapters_en/ch4_results.tex:442-446`는 0/11 exact match와 0.265 gap이 permutation null에서 유의하지 않다고 명시하지만, `chapters_en/ch6_conclusion.tex:22`는 “showing that the optimal information source for one pathogen does not generalize to others”라고 단정한다. 같은 장 `chapters_en/ch6_conclusion.tex:60`은 `P≈0.96`을 인정한다. “LOPO는 null-consistent corroboration일 뿐”으로 결론 문장을 고쳐야 한다.

## Major (should fix)

- [M1] `ω²=0.296` 해석은 개선됐지만 CI 신뢰도는 약함 — `chapters_en/ch4_results.tex:361-390`, `chapters_en/ch4_results.tex:483-489` — modeled vs residual 분리는 올바르게 적고 있으나, cluster bootstrap은 11 pathogen clusters뿐이고 본문도 `≥30` rule-of-thumb 미달 및 anticonservative 가능성을 인정한다. headline CI `[0.195, 0.333]`는 “확정적 95% CI”보다 “11-cluster percentile bootstrap interval”로 낮춰야 한다.

- [M2] Bonferroni family 정의가 방어적이지만 표 caption에 과부하 — `chapters_en/ch4_results.tex:865` — per-pathogen 780, joint 8,580, Holm, BH, winner’s curse, α-sensitivity, novel-only audit가 한 caption에 모두 들어가 표 자체가 해석 문단이 되었다. 논리 자체는 대체로 방어 가능하지만, family-wise correction의 primary denominator를 methods에 분리해 사전 정의하고 caption은 숫자만 남겨야 한다.

- [M3] “4-feature core captures 97.6%”의 metric/split 설명이 headline보다 약함 — `front_en/abstract.tex:11`, `chapters_en/ch1_introduction.tex:150`, `chapters_en/ch4_results.tex:760-775`, `chapters_en/ch4_results.tex:948` — 97.6%는 EqualWeight mean MCC의 비율로 보이나, 12 pathogens including Zika와 core-11 restriction이 섞인다. CI나 paired test가 없다. “statistically indistinguishable”이 아니라 “numerically retains 97.6% under this LOPO/top-10% setup”으로 고쳐야 한다.

- [M4] Feature-ablation scope가 11-pathogen main claim에 Zika를 끼워 넣음 — `chapters_en/ch4_results.tex:760`, `chapters_en/ch4_results.tex:764-775`, `chapters_en/ch4_results.tex:817-842` — main benchmark는 11 pathogens인데 ablation/GT heterogeneity는 “12 pathogens including Zika”로 claim support에 사용된다. Zika 추가는 power 보강이 아니라 scope drift로 읽힌다. headline contribution에는 core-11 수치를 기본값으로 제시해야 한다.

- [M5] External validation은 사실상 HIV-1 n=1 anchor — `chapters_en/ch4_results.tex:895-918`, `chapters_en/ch4_results.tex:920-921`, `chapters_en/ch6_conclusion.tex:27` — H3N2는 69% Layer A overlap, SARS-CoV-2는 Bonferroni 실패 및 60% overlap이다. 본문이 이를 인정하는 점은 좋지만, “vaccine-escape cross-validation”이라는 복수형 framing은 과장이다. “single clean external anchor plus two auxiliary checks”로 고쳐야 한다.

- [M6] Layer A 정의가 contribution 2를 부분적으로 구성함 — `chapters_en/ch3_methods.tex:296`, `chapters_en/ch4_results.tex:490`, `chapters_en/ch4_results.tex:608-610` — Layer A가 convergent evolution, immune escape, HVR membership의 union이면 `scoring × pathogen` interaction은 생물학적 pathogen-dependence와 curation-protocol-dependence가 섞인다. HCV 제외만으로는 충분하지 않다. 동일 curation protocol subset에서 `ω²` 재계산이 필요하다.

- [M7] RF feature importance는 leakage-prone evaluation — `chapters_en/ch4_results.tex:685-696` — position-level 5-fold CV는 같은 pathogen 안의 인접/상관 positions를 train/test로 나누므로 spatial autocorrelation leakage 가능성이 크다. RF AUC는 “feature complementarity illustration”로 낮추고, blocked-by-region CV 또는 protein-domain block split을 추가해야 한다.

- [M8] Code availability가 미래형 — `chapters_en/ch6_conclusion.tex:150-153` — “will be made available”, “upon request”, “will be made public”은 제출 시점 재현성 기준으로 약하다. 방어 전 public archive/commit hash/Zenodo DOI를 제공해야 한다.

- [M9] PLANT bib author가 부정확 — `references.bib:1237-1243` — 본문은 PLANT를 인용하지만 bib author가 `{PLANT Consortium}`으로 되어 있다. 공개 정보상 PLANT preprint는 Ito, Kawakubo, Unno, Strange, Lytras, Okumura, Lilley, Harvey, Lewis, Sato 등 구체 저자 목록이 있다. bibkey는 유지해도 author 필드는 실제 저자로 바꿔야 한다.

## Minor (polish)

- [m1] Table label 이름이 구판 흔적 — `chapters_en/ch1_introduction.tex:148`, `chapters_en/ch4_results.tex:362` — `tab:9pathogen_anova`가 11-pathogen 결과를 가리킨다. `tab:stage2_anova` 등으로 바꾸는 편이 낫다.

- [m2] RF CV AUC 소수점 불일치 — `chapters_en/ch4_results.tex:692-693`, `chapters_en/ch4_results.tex:716` — 본문은 HCV `0.701`, 표는 `0.700`.

- [m3] Figure 1.1 내용/캡션은 대체로 일치하지만 node가 과밀 — `chapters_en/ch1_introduction.tex:90`, `chapters_en/ch1_introduction.tex:114-117`, `chapters_en/ch1_introduction.tex:131` — figure node에 headline numbers가 많아 abstract와 중복된다. 캡션은 괜찮지만 그림 안 숫자는 최소화 가능하다.

- [m4] Weber 2019는 “hotspot definitions”가 아니라 benchmarking guideline으로 사용됨 — `chapters_en/ch2_background.tex:225-228`, `references.bib:294-301` — 인용 자체는 정확하나, hotspot definition literature로 기대한다면 맞지 않는다. hotspot/region definition 근거는 별도 문헌으로 보강해야 한다.

- [m5] EVEREST v3와 EVEREST 2025가 같은 DOI — `references.bib:1075-1080`, `references.bib:1228-1234` — 버전 구분 note는 있으나 같은 DOI를 두 bibkey로 분리했다. LaTeX/bib style에서 중복 reference로 보일 수 있다.

## Out-of-frame findings (things Claude's review structure could not have caught)

- Region-level hotspot detection framing 자체가 방어 포인트다 — `chapters_en/ch2_background.tex:233-242`, `chapters_en/ch5_discussion.tex:207` — ViroGym/EVEREST/ProteinGym과 task가 다르다는 주장은 맞지만, hostile reviewer는 “harder per-variant prediction을 피하고 region binary MCC로 문제를 쉽게 만든 것”이라고 공격할 수 있다. 공유 pathogen에서 top-k binarized VEP baseline 하나라도 넣는 것이 가장 강한 방어다.

- “Pathogen-dependent optimality”가 ground truth construction의 tautology로 읽힐 수 있다 — `chapters_en/ch3_methods.tex:296`, `chapters_en/ch4_results.tex:842-843` — pathogen마다 Layer A 정의가 다르면 pathogen-specific winner가 나오는 것은 발견이 아니라 설계 귀결이라는 공격이 가능하다. 동일 evidence-type subset 분석이 필요하다.

- Contribution 3가 Contribution 2를 약화시킨다 — `chapters_en/ch4_results.tex:853-855`, `chapters_en/ch4_results.tex:930-938` — Contribution 2는 pathogen-specific 최적성을 말하지만, Contribution 3는 EqualWeight generic ensemble의 실용성을 말한다. 둘은 공존 가능하지만 narrative상 “최적 정보원은 병원체별로 다르다”와 “4-feature generic core면 98% 충분하다”가 긴장한다. “optimality vs robust default”로 명시 분리해야 한다.

- DCA/epistasis exclusion은 단순 future work 이상이다 — `chapters_en/ch2_background.tex:196-198` — viral escape와 compensatory mutations에서 epistasis는 핵심이다. 단일-position scorer로 ANOVA decomposition을 깨끗하게 만들었지만, 그 선택이 biological realism을 낮춘다.

- Dual-use/ethics 논의가 약하다 — `chapters_en/ch6_conclusion.tex:148-159` — pathogen hotspot/immune escape prioritization 도구인데 ethics, misuse, release granularity, GISAID compliance 외 dual-use mitigation이 보이지 않는다. 방어/제출용으로 별도 문단이 필요하다.

## What Claude's Cycle 11 review missed (your unique findings)

- CSV/results artifact가 실제 작업 디렉터리에 없어서 required table verification 자체가 불가능하다.
- Korean abstract는 동기화됐지만 Korean chapters는 대량 stale 상태라 bilingual submission 위험이 남아 있다.
- PLANT bib author가 placeholder `{PLANT Consortium}`으로 남아 있다.
- RF feature importance의 position-level CV leakage 가능성이 explicit하게 다뤄지지 않았다.
- Contribution 2와 3의 narrative tension이 아직 결론에서 충분히 분리되지 않았다.

## Confidence assessment

- Contribution 1: needs revision — framework는 명확하지만 Layer A heterogeneity와 Layer B true-negative 정의가 더 엄격해야 한다.
- Contribution 2: defensible with revision — `ω²=0.296` modeled-component 주장은 방어 가능하나 LOPO/Friedman은 보조 증거로만 써야 한다.
- Contribution 3a: needs revision — 4-feature core는 promising하지만 metric/scope/CI가 불충분하다.
- Contribution 3b: needs revision — HIV-1 anchor는 강하지만 n=1 clean external validation이다.
- Overall: needs 1-week revision — 영어 본문은 방어 가능한 수준에 가까우나, 한국어 본문 동기화와 source artifact/provenance 보강은 submission blocker다.

## Meta

- Files read: 16
- Numbers spot-checked against CSVs: 0 — CSV/results directory absent in workspace
- Bibkeys verified: 40+ local, 6 external spot checks
- Time spent: 약 70분 상당
- External checks used: ViroGym arXiv metadata, EVEREST Sciety/bioRxiv metadata, ProteinGym official/PyPI/GitHub summaries, PLANT Sciety/HuggingFace metadata.

