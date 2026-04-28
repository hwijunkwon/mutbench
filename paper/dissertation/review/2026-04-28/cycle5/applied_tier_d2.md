# Tier D2: 4-Feature Core Full Prospective Extension

## 작업 요약

Cycle 4 Tier C2가 한계로 명시한 "homoplasy/pLDDT는 별도 MSA coordinate
frame이라 window-specific 재학습 불가"를 우회하는 3/4-feature ensemble을
구현했다. C2의 219 windows를 그대로 사용하되, 각 window의 freq/entropy에
**static prior로서의 pLDDT/homoplasy**를 추가했다.

## 데이터 가용성

| Feature   | 위치                                                       | Type            | 상태 |
|-----------|------------------------------------------------------------|-----------------|------|
| freq      | CDS-aln from `data/*/*_nt_cds_aligned.fasta`              | Window-trained  | OK   |
| entropy   | CDS-aln (same)                                            | Window-trained  | OK   |
| pLDDT     | `results/mutbench/structural_features/*_plddt.csv`         | Sequence-static | OK (canonical-protein frame) |
| homoplasy | `results/mutbench/homoplasy_scores/*_homoplasy.csv`        | Panel-static    | OK (canonical-protein frame) |

pLDDT/homoplasy는 모두 canonical protein-MSA frame에 저장되어 있고
authoritative copy가 `feature_matrix_*.csv`에 동일 값으로 들어 있다
(직접 검증: H3N2 plddt 543/543 row-match, homoplasy index-shifted 1).

## Coordinate frame 우회 방법

C2 frame (codon-aln translated, frame=0)의 column index와
feature_matrix frame의 row index를 매핑:

1. CDS-frame consensus + canonical protein consensus 각각 산출
2. ungapped 부분을 Needleman--Wunsch 정렬 (Bio.pairwise2 globalms 2/-1/-10/-0.5)
3. 매칭된 residue pair만 `{cds_col -> fm_row}` mapping에 등록
4. 매핑되지 않은 CDS column은 mapped 값들의 mean으로 채움 (z-score 후
   ensemble에서 중립)

**pLDDT는 sequence-static**(window-invariant by construction).
**homoplasy는 panel-static**(per-window TreeTime 재추정 불가, single
TreeTime 결과를 모든 window에 prior로 적용; 본문에 explicit 명시).

### Per-pathogen mapping coverage

| Pathogen     | L_cds | L_target | mapped | coverage |
|--------------|-------|----------|--------|----------|
| H3N2         |  587  |   543    |  472   |  0.80    |
| Influenza_B  |  629  |   560    |  566   |  0.90    |
| Dengue       |  795  |   490    |  497   |  0.62    |
| RSV          |  575  |   550    |  535   |  0.93    |
| HCV          |  869  |   340    |  209   |  0.24    |
| Norovirus    |  910  |   536    |  497   |  0.55    |
| EV-A71       |  429  |   261    |  297   |  0.69    |
| Rabies       |  525  |   491    |  514   |  0.98    |
| HIV-1        | 1768  |   450    |  519   |  0.29    |
| MERS         | 1687  |  1330    | 1246   |  0.74    |
| SARS-CoV-2   | 1294  |  1259    | 1222   |  0.94    |

HCV/HIV-1/Norovirus는 CDS aln이 protein MSA보다 훨씬 길어 매핑률이 낮음
(본문 limitation으로 표시 — 향후 frame-2 translate + region trimming으로
개선 여지). Rabies/SARS-CoV-2/Influenza_B는 0.9 이상으로 매핑이 높음.

## Frame=0 사용 이유 (paired 비교를 위한 동일 윈도우 보장)

C2와 D2의 freq/entropy 계산이 **완전히 동일한 column set**에서 일어나도록
frame=0을 강제. 이로써 paired 통계 비교 시 windows match이 보장됨.
(frame 자동탐지로 향상되는 freq/entropy 신호의 부수적 추가 이득은
미래 작업으로 분리.)

## 측정 결과

### Grand mean by score variant (n=73 windows)

| Score                        | mean MCC  | mean AUROC | mean enrichment |
|------------------------------|-----------|------------|-----------------|
| freq+entropy (C2 baseline)   | -0.0009   |   0.555    |     2.66×       |
| freq+entropy+pLDDT           | -0.0060   |   0.543    |     1.36×       |
| freq+entropy+homoplasy       | +0.0042   |   0.549    |     1.66×       |
| freq+entropy+pLDDT+homoplasy | -0.0097   |   0.561    |     0.92×       |

### Paired comparison vs C2 baseline (per-window MCC)

| Variant                     | n  | mean Δ MCC | Wilcoxon p | better/worse/tied |
|-----------------------------|----|------------|------------|-------------------|
| +pLDDT                      | 73 | -0.0052    | 0.170      | 38 / 14 / 21     |
| +homoplasy                  | 73 | +0.0051    | **<0.001** | 44 /  5 / 24     |
| +pLDDT+homoplasy (4-feat)   | 73 | -0.0088    | 0.016      | 44 / 10 / 19     |

Mid-result with structure: homoplasy가 단독 추가될 때만 통계적으로 신호
있지만(p<0.001), Top-30 MCC 평균 개선은 +0.005에 불과. 4-feature 합성은
sign이 mixed(better/worse 모두 증가, mean negative).

### Per-pathogen highlights

| Pathogen   | C2 MCC | +homoplasy MCC | +homoplasy AUROC | 4-feat AUROC | 변화 패턴 |
|------------|--------|----------------|------------------|--------------|----------|
| EV-A71     | 0.146  | **0.188**      | 0.773 → **0.844**| 0.825        | homoplasy 추가가 best |
| Rabies     | 0.112  | 0.067          | 0.789 → **0.860**| 0.800        | AUROC 개선/MCC 약화 |
| RSV        | -0.014 | -0.012         | 0.560 → 0.910    | **0.922**    | 4-feat 최강 (n=2) |
| Influenza_B| -0.025 | -0.023         | 0.696 → 0.732    | 0.650        | 부분 개선 |
| HCV        | -0.007 | -0.007         | 0.312 → **0.085**| 0.590        | homoplasy 파괴적 |
| Norovirus  | -0.056 | -0.041         | 0.317 → 0.232    | 0.220        | 추가 정보가 noise |

핵심 패턴: pathogen-specific. EV-A71/Rabies/RSV에는 homoplasy 추가가
도움이 되고, HCV에는 파괴적임 (HCV homoplasy 분포가 거의 flat이라 noise만 추가).

## ch4/ch5 본문 update

### ch4_results.tex (line 281-290 근처, 신규 paragraph + figure)

`\paragraph{4-feature core extension (3-/4-feature ensembles).}` 신설,
`label{para:sliding_window_4feature}`. C2의 fig:sliding_window_backtest
직후에 삽입. Grand mean MCC/AUROC, paired Wilcoxon p, per-pathogen
하이라이트, HCV negative example을 honest 보고. 신규 그림
`sliding_window_prospective_backtest_4feature.png` 삽입.

### ch5_discussion.tex (line 351, sec:prospective_validation_gap 두 번째 단락)

C2의 단락("Two boundary conditions are explicit. First, ...")을 확장:
- 4-feature ensemble의 honest 보고 ("not a free lunch in the prospective regime")
- EV-A71/Rabies 강화, HCV 파괴 패턴 명시
- Retrospective MCC headline (0.341)과 prospective gap의 reaffirmation

## 산출물 (artifacts)

- `scripts/run_sliding_window_backtest_4feature.py` (신규, 466 줄)
- `results/mutbench/feature_analysis/sliding_window_prospective_backtest_4feature.csv`
  — 292 rows × 13 cols (73 windows × 4 score variants)
- `results/mutbench/feature_analysis/sliding_window_prospective_backtest_4feature_summary.csv`
  — 44 rows (per-pathogen × per-score-variant)
- `results/mutbench/feature_analysis/sliding_window_prospective_c2_vs_d2_paired.csv`
  — 3 rows (paired Wilcoxon/t-test results)
- `results/mutbench/feature_analysis/sliding_window_prospective_4feature_diagnostics.csv`
  — 11 rows (per-pathogen frame, lengths, mapping coverage)
- `paper/dissertation/figures/sliding_window_prospective_backtest_4feature.png`
  — 11-panel grid (2-feat vs 4-feat MCC trajectory)

## verify + xelatex

- `verify_dissertation.py`: **PASS 90 / FAIL 0 / WARN 0** (regression 없음)
- `xelatex thesis_en.tex` (2-pass): **0 errors, 263 pages**
  (C2 baseline 259 → 263, +4 pages: 1 paragraph + 1 figure + ch5 expansion)

## 결과 분류

**Mid-result**: 4-feature가 명확히 더 좋지도, 더 나쁘지도 않음.
- AUROC 측면: marginal improvement (0.555 → 0.561, +0.6%pt)
- MCC 측면: marginal regression (-0.001 → -0.010)
- Statistical: +homoplasy만 paired Wilcoxon p<0.001, but Δ=+0.005

이 결과는 dissertation의 retrospective LOPO 0/11 finding ("no single
feature wins across all pathogens")과 **일관**됨: prospective regime에서도
pathogen-specific. EV-A71/Rabies/RSV에는 homoplasy 추가가 도움, HCV에는
파괴, 나머지에는 neutral.

## 시간

실제 소요: ~1.5시간 (예상 2-6시간 대비 효율).

## 한계 및 후속

1. **Frame=0 강제** — paired 비교 우선이라 best-frame 선택의
   freq/entropy 향상은 별도 작업으로 분리. 후속에서 best-frame 사용 시
   2-feature baseline 자체가 향상될 가능성.
2. **Homoplasy panel-static** — per-window TreeTime ML 재추정은
   ~11 pathogen × 219 window = 2400 trees로 intractable. 본문에
   "documented limitation, not a covert leakage"로 explicit 명시.
3. **Mapping coverage low** for HCV (0.24), HIV-1 (0.29) — CDS-aln이
   canonical protein보다 훨씬 길 때 alignment가 불완전. 후속에서
   per-pathogen reference protein-aln 사전 정렬 또는 frame-2 translate를
   재시도.
4. **HCV homoplasy 파괴** — homoplasy 분포가 평탄한 pathogen에서는
   prior로 사용 시 신호 더 흐림. 본문에 명시.
