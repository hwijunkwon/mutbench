# Tier A 12 P2/P3 + 5 minor 패치 보고

작성: 2026-04-28
대상: codex C4 P2/P3 12건 (S1, S2, S3, D2, D4, E2, E3, G2, G3, C2, C3, C4) + C6 minor 5건
빌드 baseline: v152 (Phase F) — 245 페이지, verify 90/0/0

---

## 항목별 적용

| ID | 위치 (file:line) | before | after |
|----|-----------------|--------|-------|
| **S1** Mantel test 부재 명시 | `chapters_en/ch3_methods.tex` §wild_cluster_future 직후 (`subsubsec:mantel_acknowledgement`, line 967 부근) | 없음 (cycle 1~3 미점검) | 신규 단락: Mantel/Procrustes alternate distance-matrix test was not performed; phylogenetic non-independence is controlled via family-pair sensitivity / cluster bootstrap / LOPO / Friedman; queued as follow-up. `\cite{mantel1967nonparametric}` |
| **S2** F1·AUROC 헤드라인 비교 | `chapters_en/ch3_methods.tex` §subsec:9pathogen_metrics MCC 정당화 단락 직후 (`subsubsec:headline_metric_choice`, line 911 부근) | Chicco \& Jurman 인용 1줄 (MCC ≫ F1 in imbalance) | 추가 단락: F1·AUROC가 \texttt{stage3\_full\_results.csv}에 archived 됨; MCC 헤드라인 3 reasons (positive-rate 0.7--15.9\% spread, Chicco \& Jurman, 4-cell biological cost); supplementary F1/AUROC tables queued |
| **S3** Jackknife 미수행 acknowledge | ch3:wild_cluster_future 직후 (`subsubsec:jackknife_acknowledgement`) | 없음 | 신규 1단락: delete-one jackknife not performed; BCa는 scipy 표준; jackknife-acceleration re-fit queued |
| **D2** HIV-1 group M/O 분리 | ch5 §sublineage_pooling (line 321) | (Phase F에서 처리) | acknowledge-only (Phase F 320--321 paragraph) — Tier A 추가 변경 없음 |
| **D4** HCV genotype 1/3 분리 | ch5 §sublineage_pooling (line 321) | (Phase F에서 처리) | acknowledge-only (Phase F 320--321 paragraph) — Tier A 추가 변경 없음 |
| **E2** DMS 데이터 사용 약관 명시 | ch3 §external_licenses Layer~C 항목 (line 1031) | "academic-research terms" 일괄 표현 | 강화: Bloom-lab Greaney/Haddox = CC-BY 4.0 (Dryad/Zenodo); IRB consent 적용 안 됨 (protein-level fitness, 인체-피험자 식별자 없음); MutBench는 derived top-20\% indicator vectors만 redistribute |
| **E3** 한국 IBC 검토 명시 | ch5 §durc_ethics (line 353) | KNU IBC 명시 + TODO | TODO 그대로 유지 (Phase F 처리). `% TODO: confirm KNU IBC review tag/letter ID` 명확화 |
| **G2** Severity Medium → High | ch6:36 (Table~\ref{tab:limitations_summary} ``Scope constraints'' 행) | "Medium / RNA viruses and surface proteins only" | "**High** / RNA viruses and surface glycoproteins only; point substitutions only; coding region only (5$'$/3$'$ UTR and non-coding selection out of scope) / DNA viruses, multi-protein, indel-aware scoring, UTR/non-coding extension" |
| **G3** UTR / coding region only | ch3:133 (FASTA collection 단락) | "complete coding sequences" filter 한 줄 | 추가: "single-position regime within the coding region of the surface glycoprotein only; 5$'$/3$'$ UTRs, IRES, polyprotein-cleavage junctions outside assayed protein boundary, pseudogenes, non-coding selection are explicitly out of scope"; HCV polyprotein scope 한정 한 줄 |
| **C2** Foldseek 인용 / 미사용 명시 | ch3:651 (structural scores SASA paragraph 끝) | 없음 | 추가 1줄: "Foldseek~\cite{vankempen2024foldseek} and DALI-style structure-alignment tools were \emph{not} used; AlphaFold-DB SARS-CoV-2 vs.\ PDB~6VSB anchored by direct accession reference (Table~\ref{tab:structure_sources}) without explicit RMSD/Z-score readout; queued as follow-up" |
| **C3** AlphaFold-Multimer 미사용 명시 | ch3:649 (structural scores 단락 헤드) | "AlphaFold DB or ESMFold-derived" 단순 인용 | 추가: "AlphaFold~2 monomer mode" 명시 + "AlphaFold-Multimer~\cite{evans2021af2multimer} was \emph{not} used"; HIV-1 gp120 / RSV F / Influenza HA trimers, Dengue/Zika E dimers — monomer SASA over-estimates oligomeric interface exposure; cross-reference ch5 §plm_data_limitations |
| **C4** HMMER 미사용 / 정당화 | ch3:133 (dedup paragraph) | CD-HIT/MMseqs2 인용만 (Phase F) | 강화: 100\%-identity equivalence 정당화 (arithmetic identity, dependency 회피); HMMER~\cite{eddy2011hmmer} \texttt{phmmer}/\texttt{hmmsearch} \emph{not applied}; GenBank query + post-MAFFT min-length truncation으로 frame-shift 부분-domain mis-annotation 경계화; HMMER profile-screen pass queued |
| **Minor 13** TODO 주석 명확화 | ch3:1023, ch3:1033, ch5:354 | TODO 3건 (라이선스 버전 / ESM-3 license / KNU IBC tag) | 그대로 유지 (placeholder 보존, 사용자 confirm 시점 명시) |
| **Minor 14** Vic/Yam acknowledge polish | ch3:71, ch5:321 | (Phase F 처리) | 변경 없음 |
| **Minor 15** ESM-3 cross-chapter 일관성 | ch2:146 | "not benchmarked directly in this dissertation" (애매) | 명확화: "\emph{not} used as a scoring channel in MutBench's headline 8{,}580-evaluation grid because EvolutionaryScale Cambrian non-commercial license, MIT-redistribution requirement과 incompatible (Chapter~\ref{ch:mutbench}, §\ref{para:external_licenses})" — ch3 §external_licenses와 cross-reference로 일관성 확립 |
| **Minor 16** CD-HIT "functionally equivalent" 정당화 | ch3:133 | "functionally equivalent" 1줄 | "arithmetically identical at 100\%-identity setting (no partial-match scoring), avoids additional dependency in reproducibility environment" — C6 review의 minor 잔존 봉쇄 |
| **Minor 17** C0/A1 polish | — | — | 신규 polish 없음 |

---

## references.bib 신규 4건 추가

위치: line 36 부근 (CD-HIT/MMseqs2 그룹 직후), 신규 4 entry block

1. `eddy2011hmmer` — Eddy 2011 "Accelerated profile HMM searches" (PLoS Comp Bio 7(10):e1002195, doi 10.1371/journal.pcbi.1002195)
2. `vankempen2024foldseek` — van Kempen et al. 2024 "Fast and accurate protein structure search with Foldseek" (Nat Biotechnol 42(2):243--246, doi 10.1038/s41587-023-01773-0)
3. `evans2021af2multimer` — Evans et al. 2021 "Protein complex prediction with AlphaFold-Multimer" (bioRxiv 2021.10.04.463034, doi 10.1101/2021.10.04.463034)
4. `mantel1967nonparametric` — Mantel 1967 "The detection of disease clustering and a generalized regression approach" (Cancer Research 27(2 Part 1):209--220)

신규 4건 모두 인용 위치 1+ 처에 정상 resolve. bibtex pass에서 missing-key 0건 발생 안 함.

---

## verify + xelatex 결과

- `python3 verify_dissertation.py`: **PASS 90 / FAIL 0 / WARN 0** (회귀 0건)
- xelatex pass 1 → bibtex → xelatex pass 2 → xelatex pass 3:
  - **Pages**: 253 (v152 245p 대비 +8p; 신규 7단락 + Minor 5건 분량)
  - **Errors (`!`/LaTeX Error)**: **0**
  - **Undefined citations**: **0** (`grep "Citation .* undefined" thesis_en.log` empty; 신규 4 bib key 정상 resolution)
  - **Warnings**: 통상적인 underfull \hbox (한국어 폰트 hyphenation, 기존 baseline 동일 빈도) + Font size substitution ≤0.5pt — 모두 baseline 동일

---

## 잔여

| 잔여 | 사유 |
|-----|-----|
| TODO 주석 3건 (ch3:1023, ch3:1033, ch5:354) | submission 시점에 사용자 confirm 후 제거 — placeholder 의도 보존 |
| 시점-stratified Omicron re-run 본문 미수행 (D3) | Phase F의 acknowledge-only 정공법 유지 (재실험 0 건 원칙) |
| HIV-1 group/subtype re-run 본문 미수행 (D2) | 동상 |
| HCV genotype 1/3 re-run 본문 미수행 (D4) | 동상 |
| Influenza B Vic/Yam re-run 본문 미수행 (D1) | Phase F 처리 (sensitivity로 queued) |
| Mantel correlation $r$/$p$ 수치 부재 | acknowledge-only (Tier A 신규 단락에서 명시); follow-up cycle |
| Foldseek RMSD readout 부재 | acknowledge-only; follow-up |
| AlphaFold-Multimer SASA re-fit 부재 | acknowledge-only; follow-up |

모두 acknowledge-only 정공법으로 closing. Re-run 0건. 시간 cost ≈ 60분 (목표 60--90분 범위 내).

---

## commit 권고 단위

`fix: v153 — Tier A codex C4 P2/P3 (12) + C6 minor (5) acknowledge-only patches`

신규 bib 4건 (`mantel1967nonparametric`, `vankempen2024foldseek`, `evans2021af2multimer`, `eddy2011hmmer`) + 본문 7단락 신규/강화 + 1 표 셀 변경 (severity Medium → High).
