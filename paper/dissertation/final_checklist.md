# 논문 마감 체크리스트

## A. 수치 일관성 검증

### A1. 핵심 수치 (전 챕터에서 동일해야 함)
- [ ] 평가 수: 8,580 (20 × 39 × 11)
- [ ] Scoring 수: 20 types, 6 categories
- [ ] Detector 수: 39 variants, 14 families
- [ ] Pathogen 수: 11 (benchmark), 12 (feature analysis with Zika)
- [ ] ANOVA: scoring×pathogen ω²=0.296 (최대)
- [ ] ANOVA: family ω²=0.013
- [ ] Friedman: χ²=7.69, p=0.990
- [ ] LOPO: 0/11 match, mean gap=0.265
- [ ] Unique best combos: 11/11 (9 distinct scoring types)
- [ ] Stage 1 hotspot-score: 0.778 (MutClust-Hybrid)
- [ ] Vaccine escape: SARS-CoV-2 4.90×, H3N2 4.012×

### A2. 체크 대상 파일
- front_en/abstract.tex
- front/abstract_kr.tex
- back/abstract_en.tex (있다면)
- ch1_introduction.tex
- ch3_methods.tex
- ch4_results.tex
- ch5_discussion.tex
- ch6_conclusion.tex

## B. 그림 검증

### B1. Stage 3 그림 9개
- [ ] stage3_scoring_pathogen_heatmap.png — 20 scoring × 11 pathogen 맞는지
- [ ] stage3_scoring_category_bar.png — 6개 카테고리 맞는지
- [ ] stage3_anova_decomposition.png — scoring×pathogen=0.296 맞는지
- [ ] stage3_best_per_pathogen.png — 11개 병원체 맞는지
- [ ] stage3_detector_comparison.png — 14 families 맞는지
- [ ] stage3_fairness_scatter.png — rho=0.973 맞는지
- [ ] stage3_layer_a_vs_c.png — 4개 DMS 병원체 맞는지
- [ ] stage3_lopo_crossval.png — 0/11 match 맞는지
- [ ] stage3_fubar_spotlight.png — H3N2 ★ 표시 맞는지

### B2. 그림-본문 일치
- [ ] 각 그림이 본문에서 \includegraphics로 참조됨
- [ ] 각 그림의 캡션이 최신 수치와 일치
- [ ] Figure 번호가 순차적

## C. 참조 무결성

### C1. Cross-reference
- [ ] \ref{ch:adapt} — ch4_results.tex의 information-type 섹션으로 resolve
- [ ] \ref{subsec:pahd_prototype} — phantom label 존재 확인
- [ ] \ref{sec:information_analysis} — 올바른 섹션 가리킴
- [ ] PAHD 관련 \ref 깨진 것 없는지

### C2. 인용
- [ ] EVEREST (Gurev 2025) 인용됨
- [ ] EVE (Frazer 2021) 인용됨
- [ ] EVEscape (Thadani 2023) 인용됨
- [ ] ProteinGym (Notin 2023) 인용됨
- [ ] AlphaMissense (Cheng 2023) 인용됨
- [ ] Demsar 2006 인용됨
- [ ] Weber 2019 인용됨
- [ ] Bailey 2018 인용됨

## D. PAHD 완전 제거

- [ ] ch1: 0건
- [ ] ch2: 0건
- [ ] ch3: 0건
- [ ] ch4: 0건 (phantom label만 허용)
- [ ] ch5_discussion: 0건
- [ ] ch6: 0건
- [ ] front_en/abstract: 0건
- [ ] front/abstract_kr: 0건
- [ ] back/abstract_en: 0건

## E. LaTeX 빌드

- [ ] xelatex 에러 없음
- [ ] bibtex 에러 없음
- [ ] undefined references 없음
- [ ] 페이지 수 확인 (목표: ~165p)
- [ ] List of Tables, List of Figures 정상

## F. 데이터 파일

- [ ] results/mutbench/stage3_full_results.csv: 8,580 rows
- [ ] results/mutbench/stage3_statistics.csv: 올바른 수치
- [ ] results/mutbench/layer_c_evaluation.csv: 4 pathogens
- [ ] 그림 PNG 파일: paper/figure/ 와 paper/dissertation/figures/ 동기화
