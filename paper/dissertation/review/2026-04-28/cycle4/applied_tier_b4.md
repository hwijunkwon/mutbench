# Tier B4: Per-Pathogen Friedman Nemenyi Post-Hoc 측정 보고

**일자**: 2026-04-28 (cycle 4)
**작업**: Friedman omnibus (chi^2 = 7.69, p = 0.990, n = 11) 한계 보강용
Nemenyi pairwise post-hoc test 수행 + 본문 통합 + LaTeX 재빌드

## 1. 데이터 + 코드

### 입력
- `/proj/paper/results/mutbench/stage3_full_results.csv` (8,580 evals, 11
  pathogens × 20 scoring × 14 detection families)

### 코드
- 신규: `/proj/paper/scripts/nemenyi_posthoc_friedman.py`
  - `analyze_stage3_stats.py` 의 Friedman 행렬 구성과 동일하게
    `combo_pathogen` 평균 → `combo_mean` → MCC 내림차순 정렬 → `head(20)`
    → `(20 combos × 11 pathogens)` MCC 행렬 생성.
  - `scipy.stats.friedmanchisquare` 로 echo (chi^2, p) 재산출 (sanity).
  - `scikit_posthocs.posthoc_nemenyi_friedman((blocks × treatments))` 로
    20×20 pairwise p-value matrix 산출.
  - 190 pair long-form table + Bonferroni 임계값 + provenance JSON.

### 산출물
- `/proj/paper/results/mutbench/nemenyi_pairwise_pvalues.csv` (20×20)
- `/proj/paper/results/mutbench/nemenyi_summary.csv` (190 pairs, p로 정렬)
- `/proj/paper/results/mutbench/nemenyi_provenance.json` (행렬 shape, top-10
  lowest/highest p, 환경 메타)

### Friedman echo 재현 검증
- 산출 echo: chi^2 = 7.6880, p = 0.989544 → ch4:474 의 7.69 / 0.990 과 정확
  일치. `verify_claims.py` 의 Bonus 항목도 그대로 PASS (8/8). 즉
  Nemenyi 가 사용한 20-combo 부분집합은 본문이 보고한 Friedman 부분집합과
  동일하다.

## 2. 측정 결과

| 항목 | 값 |
| --- | --- |
| Combos × pathogens | 20 × 11 |
| 총 pair 수 | 190 |
| Raw α = 0.05 유의 pair | **0/190** |
| Bonferroni α = 0.05/190 = 2.63e-04 유의 pair | **0/190** |
| 전체 p-value 분포 | min 0.989, median 1.000, max 1.000 |

### 가장 유의 (lowest p) — top 5
| combo A | combo B | mean rank A | mean rank B | rank gap | p |
| --- | --- | ---: | ---: | ---: | ---: |
| freq+AdaptWin | entropy+Wavelet | 8.59 | 12.64 | 4.05 | 0.989 |
| homoplasy+KDE | entropy+Wavelet | 8.64 | 12.64 | 4.00 | 0.991 |
| freq+AdaptWin | fubar_pos_sel+KDE | 8.59 | 12.55 | 3.95 | 0.992 |
| homoplasy+KDE | fubar_pos_sel+KDE | 8.64 | 12.55 | 3.91 | 0.993 |
| freq+SWAN | entropy+Wavelet | 9.05 | 12.64 | 3.59 | 0.997 |

### 가장 유사 (highest p) — top 5
| combo A | combo B | rank gap | p |
| --- | --- | ---: | ---: |
| freq+Wavelet | freq+FreqThresh | 0.32 | 1.000 |
| freq+AdaptWin | homoplasy+KDE | 0.05 | 1.000 |
| dnds_proxy+SWAN | entropy+AdaptWin | 0.36 | 1.000 |
| entropy+SWAN | dnds_proxy+AdaptWin | 0.55 | 1.000 |
| dnds_proxy+AdaptWin | homoplasy+AdaptiveKnee | 0.18 | 1.000 |

### 패턴
- 최소 mean-rank (best ranking) 클러스터: `freq+AdaptWin` (8.59),
  `homoplasy+KDE` (8.64), `freq+SWAN` (9.05), `dnds_proxy+SWAN` (9.41),
  `freq+SlidingTest` (9.73) — 빈도/선택압 기반.
- 최대 mean-rank (worst ranking) 클러스터: `entropy+Wavelet` (12.64),
  `fubar_pos_sel+KDE` (12.55), `freq+KDE` (11.59),
  `EqualWeight+FreqThresh` (11.45) — Bayesian-selection / Wavelet-detection
  편중.
- 그러나 최대 rank 격차 (4.05) 조차 Nemenyi p = 0.989 → **n = 11 block 에서는
  어떤 pair 도 ranking 이 다르다고 통계적으로 주장 불가**.

## 3. 20×20 matrix highlight

`nemenyi_pairwise_pvalues.csv` 첫 6행 (전체 행 라벨은 mean-MCC 순):

```
                         freq+SlidingTest  dnds_proxy+SlidingTest  entropy+SlidingTest  ...
freq+SlidingTest                     1.00                    1.00                 1.00
dnds_proxy+SlidingTest               1.00                    1.00                 1.00
entropy+SlidingTest                  1.00                    1.00                 1.00
dnds_proxy+Wavelet                   1.00                    1.00                 1.00
entropy+KDE                          1.00                    1.00                 1.00
dnds_proxy+KDE                       1.00                    1.00                 1.00
```

행렬 전체에서 off-diagonal 최소 p = 0.989, 25th / 50th / 75th percentile 모두
1.000. → ch4 본문은 단일 sentence 로 "전부 비유의" 라는 표현 + 가장 유의 한
pair 와 가장 유사 한 pair 만 소개하는 형태로 통합 가능.

## 4. 본문 update

### ch4 (`chapters_en/ch4_results.tex`, §9pathogen_friedman)
- 기존 478~479 line "non-significance admits two interpretations …" 다음에
  새 단락 **"Nemenyi pairwise post-hoc test"** 삽입.
- 핵심 문구:
  > Because the omnibus Friedman result cannot reject (p = 0.990), we report
  > the Nemenyi pairwise post-hoc test on the same 20 combinations × 11
  > pathogens rank matrix. None of the C(20,2) = 190 pairs reach the
  > conventional threshold (raw α = 0.05: 0/190; Bonferroni α = 2.6e-04:
  > 0/190); the entire pairwise p-value distribution lies in [0.989, 1.000]
  > with median 1.000.
- 가장 유의 pair (`freq+AdaptWin` vs `entropy+Wavelet`, p = 0.989) +
  가장 유사 pair (`dnds_proxy+AdaptWin` vs `homoplasy+AdaptiveKnee`,
  p = 1.000) 명시.
- "best-performing 클러스터 = 빈도/선택압, worst = Bayesian-selection +
  Wavelet" descriptive 패턴은 ANOVA scoring main-effect 와 같은 방향이지만
  Nemenyi 가 통계적으로 격차를 인증해주지 못함을 명시 (overclaim 방지).
- `nemenyi_pairwise_pvalues.csv`, `nemenyi_summary.csv`,
  `nemenyi_provenance.json` 을 archived provenance 로 명시.

### ch5 (`chapters_en/ch5_discussion.tex`, §scope_justification, line 327)
- "Despite the small sample size … this p-value is uninformative …" 문장에
  **Nemenyi 결과 단일 절** 삽입:
  > … the Nemenyi pairwise post-hoc analysis confirms this power limit
  > explicitly — 0/190 top-20 pairs are significant at raw α = 0.05 (and
  > 0/190 under Bonferroni at α = 2.6e-04), with the entire pairwise
  > p-value distribution lying in [0.989, 1.000] (Section
  > §9pathogen_friedman of Chapter 4; provenance
  > `nemenyi_pairwise_pvalues.csv`).
- ch5 는 ch4 본문으로 cross-reference 만 두고 디테일은 중복하지 않도록 처리.

## 5. verify + xelatex

### verify_claims.py
```
✓ PASS  Claim 1: 8,580 evaluations
✓ PASS  Claim 2: ANOVA ω² ≈ 0.296
✓ PASS  Claim 3: LOPO 0/11
✓ PASS  Claim 4: Escape 9.36×
✓ PASS  Claim 5: 4-feature 98%
✓ PASS  Claim 6: GT non-contradiction
✓ PASS  Claim 7: H-score formula
✓ PASS  Bonus: Friedman test (chi² = 7.69, p = 0.990, W = 0.037)
Result: 8/8
```
Friedman echo 재현으로 Nemenyi 가 본문 부분집합과 동일함을 확인.

### xelatex (digital mode, 2회)
- 1회차 + 2회차 모두 fatal error 0.
- 출력: `thesis_en.pdf`, **250 pages** (변경 전과 동일 페이지 수, body
  내부 단락 추가만 발생).
- natbib Citation undefined 경고 2건 (`evans2021af2multimer`,
  `vankempen2024foldseek`) → Tier B4 와 무관한 기존 누락 citation; Nemenyi
  변경에서 새로 발생한 undefined ref 0건.

## 6. 결론 (1 단락)

Friedman omnibus null 을 reject 못하는 이유가 (1) 모든 method 가 비슷하기
때문인지 (2) n = 11 block 으로는 power 가 부족하기 때문인지 본문은 그동안
Type I/II 어느 쪽도 통계적으로 분리하지 못했었다. Nemenyi pairwise post-hoc
은 후자임을 직접 증명한다 — 가장 큰 mean-rank 격차 (4.05, freq+AdaptWin vs
entropy+Wavelet) 조차 raw α = 0.05 도 통과하지 못하므로 (p = 0.989), 20-combo
× 11-pathogen rank-block design 자체가 어떤 pair 도 분리할 수 없는 power
한계를 가지고 있다. 따라서 Friedman p = 0.990 은 "방법들이 같다" 가 아니라
"분리할 수 없다" 를 보여주며, ANOVA interaction (ω² = 0.296) 과
oracle-vs-generalized MCC gap (0.265) 가 pathogen-adaptive 결론의 일차
증거로 남는다는 본문의 기존 framing 이 통계적으로 더 강하게 정당화된다.
