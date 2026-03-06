# MutBench / MutClust v2 API 레퍼런스

---

## tools.mutbench.config

### BenchmarkConfig

```python
from tools.mutbench.config import BenchmarkConfig

cfg = BenchmarkConfig(
    seed=42,           # 랜덤 시드
    n_bootstrap=1000,  # 부트스트랩 반복 횟수
    fdr=0.05,          # FDR 임계값
    gamma=10,          # MutClust gamma 파라미터
    d=3,               # MutClust d 파라미터
    minpts=5,          # MutClust minpts 파라미터
    ccm_hscore_min=0.03,
    ccm_mean_min=0.01,
    ccm_sum_min=0.05,
)

rng = cfg.get_rng()  # numpy Generator (재현 가능)
```

---

## tools.mutbench.ground_truth

### dms_loader

```python
from tools.mutbench.ground_truth.dms_loader import (
    load_dms_fitness,        # CSV → DataFrame
    dms_to_position_scores,  # DataFrame → {aa_pos: mean_abs_fitness}
    get_functional_positions # scores → set of functional positions
)

df = load_dms_fitness('data/mutbench/aamut_fitness_all.csv')
scores = dms_to_position_scores(df, gene='S')
functional_aa = get_functional_positions(scores, threshold_percentile=80)
```

### coord_mapper

```python
from tools.mutbench.ground_truth.coord_mapper import CoordinateMapper

mapper = CoordinateMapper(gene_start=21563, gene_end=25384)

nuc_positions = mapper.aa_to_nuc(484)       # [22,012, 22,013, 22,014]
aa_pos = mapper.nuc_to_aa(22012)            # 484
nuc_set = mapper.aa_set_to_nuc_set({484, 501})  # set of 6 nuc positions
```

### labeler

```python
from tools.mutbench.ground_truth.labeler import (
    create_ground_truth_labels,  # → list[int] (0/1)
    GroundTruthSource,           # name + positions 데이터클래스
)

labels = create_ground_truth_labels(genome_length=29903, functional_positions={100, 101, 102})
# → [0, 0, ..., 1, 1, 1, ..., 0, 0]

src1 = GroundTruthSource(name='dms', positions={100, 200})
src2 = GroundTruthSource(name='known', positions={200, 300})
merged = src1.merge(src2)  # positions = {100, 200, 300}
```

---

## tools.mutbench.baselines

모든 베이스라인은 동일한 인터페이스:

```python
def detect_hotspots(...) -> list[dict]:
    # Returns: [{'start': int, 'end': int, 'positions': list[int]}, ...]
```

```python
from tools.mutbench.baselines.shannon_entropy import detect_hotspots as entropy_detect
from tools.mutbench.baselines.frequency_based import detect_hotspots as freq_detect
from tools.mutbench.baselines.sliding_window import detect_hotspots as window_detect

# Shannon entropy (뉴클레오타이드 카운트 필요)
clusters = entropy_detect(counts_per_position, threshold_pct=10, gap=2)

# 빈도 기반 (H-score 배열 사용)
clusters = freq_detect(hscores, threshold_pct=10, gap=2)

# 슬라이딩 윈도우
clusters = window_detect(hscores, window_size=20, threshold_pct=10, gap=2)
```

---

## tools.mutbench.variants.registry

```python
from tools.mutbench.variants.registry import list_variants, get_variant

list_variants()  # ['v1-original', 'v2a-bugfix', 'v2b-bugfix+dnds', 'v2c-full']

detect_fn = get_variant('v2a-bugfix')
clusters = detect_fn(hscores, gamma=10, d=3, minpts=5)
# → [{'start': int, 'end': int, 'positions': list[int]}, ...]
```

---

## tools.mutbench.evaluation.metrics

```python
from tools.mutbench.evaluation.metrics import evaluate_method

metrics = evaluate_method(clusters, ground_truth_positions, genome_length)
# Returns: {
#   'precision': float,
#   'recall': float,
#   'f1': float,
#   'enrichment_ratio': float,
#   'n_detected': int,
#   'n_clusters': int,
# }
```

---

## tools.mutbench.sensitivity.sweep

```python
from tools.mutbench.sensitivity.sweep import ParameterSweep

sweep = ParameterSweep(
    gammas=[5, 10, 15, 20],
    ds=[2, 3, 4, 5],
    minpts_list=[3, 5, 7, 10],
)

results = sweep.run(hscores, eval_fn)
# eval_fn: clusters → metrics dict
# returns: list of dicts (64 combinations)
```

---

## tools.mutbench.runner

```python
from tools.mutbench.runner import run_benchmark

results = run_benchmark(
    hscores,                           # np.array
    ground_truth_positions,            # set[int]
    genome_length,                     # int
    config=BenchmarkConfig(seed=42),
    counts_per_position=None,          # optional, for entropy baseline
)

method_df = results['method_results']       # pd.DataFrame
sensitivity_df = results['sensitivity_results']  # pd.DataFrame
```

---

## tools.mutclust.dnds_annotation.core

```python
from tools.mutclust.dnds_annotation.core import (
    classify_mutation,    # (ref_codon, mut_codon, pos) → 'synonymous'/'nonsynonymous'
    compute_cluster_dnds, # (nonsyn, syn, codons) → float (dN/dS)
    annotate_clusters,    # (clusters, ref_seq, mutations) → annotated clusters
)

annotated = annotate_clusters(
    clusters,        # list[dict] with 'positions' key
    reference_seq,   # str (nucleotide sequence)
    mutations,       # dict[int, str] (position → mutant nucleotide)
)
# Each cluster gets: 'syn_count', 'nonsyn_count', 'dnds' keys added
```

---

## tools.mutbench.visualization.plots

```python
from tools.mutbench.visualization.plots import (
    plot_method_comparison,    # 방법별 비교 막대 그래프
    plot_genome_hotspot_map,   # 게놈 위치별 H-score 맵
    plot_sensitivity_heatmap,  # 파라미터 민감도 히트맵
    plot_dnds_enrichment,      # dN/dS 분포 그래프
)

plot_method_comparison(method_df, 'output.png')
plot_genome_hotspot_map(hscores, detected_pos, gt_pos, 'output.png')
plot_sensitivity_heatmap(sensitivity_df, metric='f1', output_path='output.png')
plot_dnds_enrichment(annotated_clusters, 'output.png')
```
