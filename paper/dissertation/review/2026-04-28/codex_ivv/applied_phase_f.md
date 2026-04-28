# Phase F: C4 P0+P1 8건 패치 보고

작성일: 2026-04-28
대상: codex_C4_new_attacks.md (P0/P1 8건) + codex_C5_defense_rehearsal.md (Q1 답변 노트)

---

## 1. M1 라이선스 명시 (Critical)

### 추가 위치
- **`chapters_en/ch3_methods.tex` §Code, Data, and Reproducibility (subsec:code_data_availability, line 1013부터)**: 기존 "open-source license" 단독 표현을 "MIT License (MutBench's own implementation code) + CC-BY-NC 4.0 (dissertation text and figures)"로 명시. 또한 §3.x에 새 단락 `Software and data licenses (external resources)` (label `para:external_licenses`) 추가.
- **`chapters_en/ch6_conclusion.tex` §Code and data availability (sec:code_availability, line 101 부근)**: 한 줄 추가하여 MIT/CC-BY-NC 라이선스 명시 + ch3 §Software-and-data-licenses 단락에 cross-reference.

### 명시한 자원 list (ch3 §external_licenses)
- **Sequence alignment / homology**: MAFFT (BSD-style, `katoh2013mafft`), CD-HIT (open-source, `fu2012cdhit`), MMseqs2 (MIT-style, `steinegger2017mmseqs2`)
- **Phylogenetic / selection**: IQ-TREE 2 (GPL-2.0), HyPhy/FUBAR (3-clause BSD)
- **PLM**: ESM-2 (MIT, `lin2023esm2`), ESM-3 (Cambrian non-commercial — *not used in headline*), Tranception (MIT, `notin2022tranception`), EVE/EVEscape (academic-only, `frazer2021eve` + `thadani2023evescape`)
- **Variant-effect benchmarks (citation only)**: EVEREST v3 (CC-BY 4.0, `gurev2026everest_v3`), ProteinGym (open, `notin2025proteingym_v13`), ViroGym (`virogym2026`)
- **Structures**: AlphaFold-DB (CC-BY 4.0, DeepMind/EBI), ESMFold (MIT)
- **Sequence repos**: NCBI GenBank (U.S. public domain)
- **DMS data (Layer C)**: Bloom-lab Greaney 2021/2022 (CC-BY, `greaney2021RBD/spike`), Haddox 2018 HIV-1 (CC-BY via Dryad, `haddox2018hiv1dms`), Lee 2018 / Dadonaite 2024 / Simonich 2026 / Aditham 2025 / Bakhache 2025 (academic-research terms)

라이선스 호환성 명시: MutBench 헤드라인 8,580 grid는 MIT/BSD/GPL/CC-BY 호환 입력만 사용; non-commercial 라이선스 (ESM-3, EVE) 도구는 헤드라인에 *없음*. ESM-3/EVE를 사용하려는 후속 사용자는 별도 라이선스 취득 의무 명시.

`% TODO: confirm exact license version` 주석 2건 (라이선스 확정 시 제거).

---

## 2. M2 GenBank query 명시 (Major)

### 추가 위치
- **`chapters_en/ch3_methods.tex` §Materials > FASTA collection 단락 (line 131 부근)**

### 추가 내용
- SARS-CoV-2 Spike의 *전체 query 문자열* 본문 inline (예시):
  > `(``Severe acute respiratory syndrome coronavirus 2''[Organism] OR txid2697049[Organism]) AND spike[Gene Name] AND ``complete cds''[Properties] NOT (partial[Title] OR laboratory[Title])` with length filter 3,500–4,000 nt; 실행일 2024-12-09.
- 11 pathogen 모두의 query는 `results/mutbench/provenance/genbank_queries.csv`에 archive (이미 ch3 line 132 footnote에 언급됨, 본 단락에서 강화).

---

## 3. M3 worst-MCC 공개 (Major)

### 추가 위치
- **`chapters_en/ch4_results.tex` §Per-Pathogen Best Method Analysis (line 338 직후)**: 새 paragraph `Worst-end disclosure (negative-MCC and degenerate combinations)` (label `para:stage2_worst_mcc`)

### 명시한 값 (extract from `/proj/paper/results/mutbench/stage3_full_results.csv`)
- Worst single cell: **HCV × stability × SWAN(w=50, k=1.0), MCC = −0.361** (precision 0.000, recall 0.000, 139 detected positions)
- Negative-MCC count: **4,171 / 8,580 (48.6%)**
- ≤0 MCC count: **4,695 / 8,580 (54.7%)**
- Worst-mean detector families: ScoreDBSCAN(ε=15) mean MCC −0.016; ScoreDBSCAN(ε=8) −0.013
- Worst-mean scoring channels: plddt_inv mean −0.017, grantham −0.008, Tranception −0.006

해석: pathogen-adaptive 헤드라인은 *bad cell의 부재*가 아니라 *ceiling vs. floor의 큰 gap* (0.196–0.660 vs. −0.361)에 anchor된다는 점을 본문에 정직히 노출.

---

## 4. D1 Influenza B Vic/Yam 분리 (Major)

### 추가 위치
- **`chapters_en/ch3_methods.tex` Influenza B paragraph (line 68–72)**: 헤더에 "Influenza B (HA, 560 AA; Victoria and Yamagata lineages, mixed)" 명시. CY018765 reference accession이 Yamagata-lineage임을 명시 + MSA가 둘 lineage 혼합이라는 사실 + 후속 sensitivity 분석은 미수행임을 honest disclosure.
- **`chapters_en/ch5_discussion.tex` §Ground Truth Heterogeneity Across Pathogens (line 317 직후)**: 새 paragraph `Sub-lineage and sub-genotype stratification (intentional pooling)` (label `para:sublineage_pooling`) 추가. Influenza B Vic/Yam, SARS-CoV-2 pre-Omicron/Omicron 시점, HIV-1 group M/O + subtype, HCV genotype 1/3 — 4개 pooling case 모두 명시 + 한계 acknowledge.

---

## 5. E1 DURC 검토 (Major)

### 추가 위치
- **`chapters_en/ch5_discussion.tex` §Dual Use Research of Concern (DURC) and Ethics Review (sec:durc_ethics, MAFFT --auto subsection 직전)**: 1 단락. NIH/HHS DURC 7 카테고리 분류 + 본 연구가 *retrospective bioinformatic analysis*이므로 strict-policy 의미에서는 해당 없음을 정직히 분류. 그럼에도 3개 mitigation (raw FASTA non-redistribution / region-level vs variant-level / institutional review on P3CO/Select Agent extension)을 ch6 §final_conclusion DUR paragraph와 일관성 있게 재명시. 한국 IBC: KDCA wet-lab 체인 외부, KNU IBC가 관할이라는 명시 + `% TODO: confirm KNU IBC review tag/letter ID at submission` 주석.
- 라이선스 cross-reference: ch3 §code_data_availability에 명시한 MIT + CC-BY-NC를 본 단락에서 다시 인용.

---

## 6. G1 RNA-virus 한정 강화 (Major)

### 수정 위치
- **`front_en/abstract.tex` 첫 줄 (line 2)**: "MutBench" 직후에 한정 절 추가 — `(currently scoped to the RNA-virus single-position regime; 11 RNA viruses, surface glycoproteins, point substitutions only)`.
- **`chapters_en/ch1_introduction.tex` line 48**: "MutBench evaluates" 직후 괄호로 RNA-virus 한정 + Chapter 6 future work cross-reference.
- **`chapters_en/ch6_conclusion.tex` Future Work `Additional Research Directions` paragraph (line 83 부근)**: extension of MutBench to DNA viruses, eukaryotic pathogens, prokaryotic systems은 *out of scope*임을 명시 + future work로 등록.

(Note: ch1:78, ch1:142, ch6:11, abstract:4 등 다른 MutBench 등장 위치는 모두 인접 문장에서 "11 RNA viruses" 명시가 이미 있어 별도 한정 추가 불필요.)

---

## 7. C1 CD-HIT / MMseqs2 인용 (Major)

### references.bib 추가 (2건)
- `fu2012cdhit`: Fu, L. et al. 2012. CD-HIT: accelerated for clustering the next-generation sequencing data. Bioinformatics 28(23):3150–3152. DOI 10.1093/bioinformatics/bts565
- `steinegger2017mmseqs2`: Steinegger, M. & Söding, J. 2017. MMseqs2 enables sensitive protein sequence searching for the analysis of massive data sets. Nature Biotechnology 35(11):1026–1028. DOI 10.1038/nbt.3988

### 인용 추가
- **`chapters_en/ch3_methods.tex` line 131 부근 (FASTA collection 단락)**: dedup 절차를 자체 Python SHA-256 hash로 명시 + "functionally equivalent to running CD-HIT~\cite{fu2012cdhit} or MMseqs2~\cite{steinegger2017mmseqs2} at a 100% identity threshold" 명시 + clustering at <100%는 *적용하지 않았다*는 정직한 disclosure (per-position freq/entropy 정확도 보존 위함).
- **`chapters_en/ch3_methods.tex` §external_licenses paragraph**: CD-HIT, MMseqs2 라이선스 명시.

---

## 8. Q1 defense answer note

### 작성 파일
- **`/proj/paper/paper/dissertation/review/2026-04-28/codex_ivv/defense_q1_answer_note.md`**

### 구성
- Q1 verbatim 인용 + 4-step 답변 (총 ~150 단어, 60–90초)
  - Step 1: Honest disclosure 인정 (15초)
  - Step 2: H3N2 pilot framing (frequency single-feature pilot, multi-source 미평가) (20초)
  - Step 3: 본 논문 contribution 경계 (retrospective benchmark + retrospective external anchor) (20초)
  - Step 4: Future work 등록 명시 (10초)
- 후속 질문 대비 3건 (Q1a "Why call it MutBench?" / Q1b "3a/3b도 retrospective뿐?" / Q1c "지금 학생이 해결한 문제는?")
- 답변에서 *피해야 할* 표현 3건
- 외워야 할 verbatim anchor 4건 (ch5:337, ch5:342, abstract:2, ch4:201)
- 발표 슬라이드 권고 (마지막 limitation slide 한 줄)

---

## 9. verify_dissertation.py 결과

**전체: PASS 90 / FAIL 0 / WARN 0** (회귀 0건)

7개 카테고리 모두 통과:
1. Forbidden Pattern Scan: PASS
2. Key Statistics Consistency (omega², Friedman, MCC, etc.): PASS
3. CSV Data vs Table Verification: PASS
4. LaTeX Structure Integrity: PASS
5. Scoring Formula vs Code Verification: PASS
6. Permutation Test Formula Check: PASS
7. MOSD/MutClust Weight Analysis: PASS (ch1 2.3%, ch3 1.8%, ch4 2.4%, ch5 0.8%, ch6 0.0% — 모두 ≤15% threshold)

---

## 10. xelatex 빌드 결과

**Build sequence**: `xelatex → bibtex → xelatex → xelatex` (3 passes)
- **Pages**: **245** (Phase E v151 245 pages 대비 0p 변동 — 추가 단락 분량이 페이지 경계를 침범하지 않음)
- **Errors (`!` or `LaTeX Error`)**: **0**
- **Undefined citations**: **0** (`grep "Citation .* undefined" thesis_en.log` empty — bib 신규 2건 (`fu2012cdhit`, `steinegger2017mmseqs2`)이 정상 resolution됨)
- **Warnings**: 통상적인 underfull \hbox 경고 (Korean 폰트 hyphenation, 기존 thesis 동일 빈도) + Font Size substitution ≤0.5pt — 모두 사전 baseline과 동일
- **bibtex pass**: cleanly resolved without missing key error

---

## 11. 잠재적 잔존 (P2/P3 outstanding)

| ID | 카테고리 | 결함 | 본 패치에서 처리? | 잔존 사유 |
|----|---------|------|------------------|----------|
| S1 | 통계 | Mantel test / Procrustes 부재 | **No** (P2) | scipy/skbio 5분 cost로 가능하나 본 round 8건 scope 밖 |
| S2 | 통계 | F1 / AUROC 헤드라인 병기 | **No** (P1, deferred) | `stage3_full_results.csv`에 F1 컬럼 존재 확인됨 (header: `pathogen,scoring,detector,family,mcc,precision,recall,f1,n_detected`) — 다음 round에 ch4 Table 옆에 F1 컬럼 1개 추가 1단계 cost |
| S3 | 통계 | Jackknife 미시도 | **No** (Minor) | n=11 ≤1분 cost, 향후 round |
| D2 | 도메인 | HIV-1 group M/O subtype 분리 | **부분 Yes** | ch5 §sublineage_pooling paragraph에 명시적 acknowledge 포함 (Vic/Yam, Omicron 시점, HIV-1 group/subtype, HCV genotype 4건 묶음) |
| D3 | 도메인 | SARS-CoV-2 Omicron 시점 분리 | **부분 Yes** (D2와 동일 paragraph) | 시점 stratification은 sensitivity로 *queued*만 명시; 실제 시점별 re-run 미수행 |
| D4 | 도메인 | HCV genotype 1/3 분리 | **부분 Yes** (D2와 동일 paragraph) | 동상 |
| E2 | 윤리 | DMS data use agreement 명시 | **부분 Yes** (Minor) | ch3 §external_licenses에서 Bloom-lab DMS = CC-BY (Dryad/Zenodo)로 명시; Lee/Dadonaite/Simonich/Aditham/Bakhache는 "academic-research terms"로 일괄 표현 |
| E3 | 윤리 | 한국 KCDC / IBC framework | **부분 Yes** | ch5 §durc_ethics에서 KDCA가 wet-lab 체인 외부, KNU IBC 관할 명시; review tag/letter ID는 `% TODO` |
| G2 | 범위 | RNA-virus-only severity Medium → High | **No** (Minor) | ch6:39 표 ``Severity'' 컬럼이 Medium으로 유지 (다음 round에서 검토) |
| G3 | 범위 | UTR/pseudogene/readthrough out-of-scope | **No** (Minor) | 다음 round |
| C2 | 인용 | Foldseek/DALI 미인용 | **No** (Minor) | 다음 round |
| C3 | 인용 | AlphaFold-Multimer 미인용 → monomer SASA 한계 | **No** (Major within structural biology view) | 다음 round; ch5에 1줄 acknowledge 권장 |
| C4 | 인용 | HMMER homology filter | **No** (Minor) | 다음 round |

`% TODO` 주석 2건 (라이선스 정확 버전 확정 / KNU IBC review tag) — submission 단계에서 confirm 후 제거 예정.

---

## 종합

본 Phase F 패치는 codex C4가 식별한 신규 결함 20건 중 **P0+P1 8건**을 처리했다. 처리 단위는 (1) abstract / ch1 / ch3 / ch4 / ch5 / ch6 본문 패치 7건, (2) references.bib 신규 BibTeX 2건, (3) defense Q1 answer note 1건. 

`verify_dissertation.py` 90 checks 전부 PASS 유지 (회귀 0건); xelatex+bibtex+xelatex×2 빌드 245 pages 0 errors 0 undefined citations로 통과. 

P2/P3 13건 (S1/S3, G2, G3, C2/C3/C4 등 minor 11건 + S2 P1 deferred 1건 + 시점 re-run 미수행 acknowledge-only)은 본 round 시간 scope 밖으로 명시 보류; 본 패치만으로 codex_C5 §Phase 4의 "조건부 PASS 84–88%" 추정에서 fail trigger 거리는 완화되었다고 판단된다.

본 패치 적용 직후 commit 권고 단위: `fix: v152 — Phase F codex C4 P0/P1 (license + GenBank query + worst-MCC + Vic/Yam + DURC + RNA-virus scope + CD-HIT/MMseqs2)`.
