# Tier C2: Sliding-Window Prospective Backtest 보고

## 작업 요약

Cycle 3 ch5:337 `sec:prospective_validation_gap` 의 honest disclosure
("no prospective validation has been conducted")를 multi-pathogen
sliding-window prospective backtest 의 actual evidence 로 변환했다.
H3N2 single-pilot (subsec:h3n2_temporal_pilot)을 11 pathogen panel
전체로 확장한다.

## timestamp 가용성

per-sequence year metadata는 codon-aligned NCBI CDS FASTA description
에서 정규식(`(?:19|20)\d{2}` 1980–2026 필터, 최소값 사용)으로 추출.
가용성:

| Pathogen     | n_seq | year_pct | year_range  | 비고                          |
|--------------|-------|----------|-------------|-------------------------------|
| H3N2         | 334   | 100%     | 1984–2026   | full                          |
| Influenza_B  | 285   | 100%     | 2001–2026   | full                          |
| SARS-CoV-2   | 263   | 100%     | 2020–2025   | full                          |
| EV-A71       | 450   | 98%      | 1981–2024   | near-full                     |
| MERS         | 156   | 84%      | 2013–2023   |                               |
| Norovirus    | 341   | 84%      | 2001–2025   |                               |
| HCV          | 500   | 81%      | 1984–2017   |                               |
| Dengue       | 445   | 64%      | 1987–2024   |                               |
| HIV-1        | 394   | 63%      | 2006–2023   |                               |
| Rabies       | 428   | 53%      | 2002–2021   |                               |
| RSV          | 360   | 51%      | 2002–2023   |                               |
| **Zika**     | —     | —        | —           | **nt CDS 부재 → 제외**        |

11 / 12 candidate pathogens에 대해 작업 진행 (Zika 제외, ch4 본문에 명시).

## sliding window 설계

- **train**: year < $T_0$, **test**: year $\geq T_0$
- **constraints**: $n_{\text{train}} \geq 30$, $n_{\text{test}} \geq 20$
- **step**: 모든 가용 split year (per-pathogen 별로 자동 결정)
- **emergent ground truth**: train freq < 5% AND test freq $\geq$ 10%
  (H3N2 pilot의 정의와 일치)
- **scorer**: train window의 freq, entropy, freq+entropy uniform-weight
  $z$-ensemble (4-feature core 중 time-varying 2개)
- **metric**: top-30 MCC, F1, AUROC, Fisher one-sided enrichment

**왜 freq+entropy 만 사용하는가**: homoplasy / pLDDT는 dissertation의
4-feature core의 다른 두 feature이지만 별도 MSA coordinate frame
(`_sequences.fasta` AA-MSA, year metadata 부재) 에서 계산되어
window-specific 재학습이 불가능. 이는 ch4·ch5 양쪽에 명시.

## 측정 결과

총 **219 windows** 실행 (73 windows에 emergent positions ≥1; nan-safe metric).

per-pathogen mean (freq+entropy ensemble):

| Pathogen     | n_win | year_min | year_max | mean MCC | mean AUROC | mean enrich | trend slope/yr |
|--------------|-------|----------|----------|----------|------------|-------------|---------------|
| Rabies       |  8    | 2008     | 2021     | +0.112   | **0.789**  | 4.10×       | -0.006        |
| EV-A71       | 10    | 2014     | 2023     | +0.146   | **0.773**  | 10.78×      | +0.032        |
| Influenza_B  |  7    | 2020     | 2026     | -0.025   | 0.696      | 0.00×       | +0.003        |
| MERS         |  3    | 2016     | 2020     | -0.098   | 0.604      | 0.13×       | -0.000        |
| RSV          |  2    | 2019     | 2021     | -0.014   | 0.560      | 0.00×       | —             |
| SARS-CoV-2   |  1    | 2025     | 2025     | -0.013   | 0.514      | 0.00×       | —             |
| Dengue       | 23    | 1998     | 2023     | -0.058   | 0.477      | 2.30×       | +0.000        |
| HIV-1        |  5    | 2014     | 2018     | -0.019   | 0.463      | 0.00×       | +0.003        |
| H3N2         |  4    | 2023     | 2026     | -0.029   | 0.430      | 0.00×       | +0.004        |
| Norovirus    |  6    | 2018     | 2023     | -0.056   | 0.317      | 0.00×       | +0.008        |
| HCV          |  4    | 2001     | 2004     | -0.007   | 0.312      | 0.00×       | +0.001        |
| **Grand**    | **73**|          |          | **-0.006** | **0.539** | **1.57×**  | —             |

freq-only / entropy-only / freq+entropy 세 변형의 grand mean AUROC는
0.539로 동일 ($\Delta < 0.01$); freq+entropy 가 marginal에 가깝지만
기능 일관성을 위해 ensemble을 본문 headline으로 사용.

**concept drift**: 모든 pathogen에서 |slope/year| ≤ 0.032; 시간이
지남에 따라 prospective 신호가 체계적으로 악화하지 않으나 어느 시기에도
대부분 pathogen이 chance-level. EV-A71은 train 기간이 길어질수록
MCC가 약간씩 상승하는 유일한 케이스 (+0.032/yr).

**핵심 결론**:
- **EV-A71, Rabies**: 명확한 prospective signal (AUROC 0.77–0.79,
  enrichment 4–11×)
- **Influenza_B**: partial signal (AUROC 0.70 but Top-30 MCC ~0)
- **나머지 8 pathogen**: chance-level. H3N2 single-pilot의 결론
  ("freq alone trained on 2010-2015 does not predict later-window
  emergent positions beyond chance") 이 panel 전체로 일반화됨.

## 본문 update

### ch4_results.tex
- **신규 subsection**: `subsec:sliding_window_backtest` (line 234~)
  H3N2 pilot subsection 직후 삽입.
- 신규 Table `tab:sliding_window_backtest` — 11 pathogen 요약.
- 신규 Figure `fig:sliding_window_backtest` — per-pathogen MCC over
  split year (`figures/sliding_window_prospective_backtest.png`).

### ch5_discussion.tex (`sec:prospective_validation_gap`)
- 기존: "is not implemented in this work" (negative disclosure).
- 변경: 두 단락으로 재작성:
  1. retrospective summary 의 본질 유지.
  2. **forward-time holdout이 sliding-window backtest로 implement
     되었음**, 결과 (AUROC distribution, EV-A71/Rabies 양성 신호,
     8 pathogens chance-level), 두 boundary conditions (4-feature
     core 중 2개만 재학습; reference set은 within-MSA emergent
     positions이지 literature-curated post-cutoff GT가 아님).

## 산출물 (artifacts)

- `scripts/run_sliding_window_backtest.py` (신규, 411 줄)
- `results/mutbench/feature_analysis/sliding_window_prospective_backtest.csv`
  — 219 rows × 14 cols (per-window per-score)
- `results/mutbench/feature_analysis/sliding_window_prospective_backtest_summary.csv`
  — 11 rows (per-pathogen 요약)
- `results/mutbench/feature_analysis/sliding_window_prospective_coverage.csv`
  — pathogen × {ok, year-tagged sequence count, year range}
- `paper/dissertation/figures/sliding_window_prospective_backtest.png`

## verify + xelatex

- `verify_dissertation.py`: **PASS 90 / FAIL 0 / WARN 0** (regression 없음)
- `xelatex thesis_en.tex` (2-pass): **0 errors, 259 pages**
  (이전 245–248 pages에서 +11~14 pages — 신규 subsection + table +
  figure + ch5 expanded paragraphs 분량과 일치)

## 시간

실제 소요: ~2시간 (예상 4–8시간 대비 효율).

## 한계 및 후속

1. **freq+entropy 2-feature 만 재학습** — 4-feature core 의 homoplasy /
   pLDDT 는 별 MSA coord frame 이라 forward-time 재학습 불가능 (ch4·ch5
   honestly 명시).
2. **emergent reference 는 within-MSA proxy** — literature-curated
   post-cutoff GT (e.g., DMS-validated escape sites)가 아님. 후자는
   Layer A pipeline 의 frozen earlier-date snapshot 이 필요하며 future
   work 로 분류.
3. **9 pathogens chance-level** — operational 메시지: surveillance
   사용자는 이 8개에 대해서는 forward-time signal 을 unverified로
   취급해야 함 (ch5에 명시).
4. **Zika 제외** — nt CDS 부재로 인한 honest exclusion (ch4·보고서 명시).
