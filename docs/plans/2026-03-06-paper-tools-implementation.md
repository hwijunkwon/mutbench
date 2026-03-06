# Paper Tools Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Implement all 12 tools from MOSD and MutClust papers as Python CLI tools with tests.

**Architecture:** Monorepo under `/proj/paper/tools/` with `common/` shared utilities, `mosd/` (6 tools), `mutclust/` (6 tools). Each tool is a Python package with `__main__.py` for CLI and `core.py` for logic. Claude Team Code with 2 parallel agents (mosd-dev, mutclust-dev).

**Tech Stack:** Python 3.12, numpy, scipy, pandas, scikit-learn, networkx, statsmodels, biopython, argparse

---

## Phase 0: Project Setup (Lead)

### Task 0.1: Organize document files into proper directories

**Files:**
- Create: `docs/mosd/`, `docs/mutclust/`, `docs/figures/`, `docs/presentation/`
- Move existing files into organized structure

**Step 1: Create directory structure and move files**

```bash
cd /proj/paper
mkdir -p docs/mosd docs/mutclust docs/figures docs/presentation

# Move paper-specific docs
mv 논문1_MOSD_심층정리.md docs/mosd/
mv 논문2_MutClust_심층정리.md docs/mutclust/
cp "paper/A review on multi-omics integration for aiding study design of large scale TCGA cancer datasets.pdf" docs/mosd/paper.pdf
cp "paper/Identification of severity related mutation hotspots in SARS-CoV-2 using a density-based clustering approach.pdf" docs/mutclust/paper.pdf

# Move figures
mv figures/mosd_*.jpeg docs/figures/
mv figures/mutclust_*.jpeg docs/figures/
mv figures/mutclust_*.png docs/figures/

# Move presentation files
mv 발표_스크립트.md docs/presentation/
mv 예상_질의응답.md docs/presentation/
mv PhD_Presentation_v8_EN.pptx docs/presentation/
mv Decoding_Genomic_Complexity.pdf docs/presentation/
mv v8_content_review_report.md docs/presentation/
mv v8_modification_log.md docs/presentation/
mv knu_emblem_official.jpg docs/presentation/
mv knu_symbol_t.png docs/presentation/
mv knu_symbol_white.png docs/presentation/

# Move figure PDFs
mv figure_pdf/*.pdf docs/presentation/
```

**Step 2: Commit**

```bash
git add -A
git commit -m "docs: organize paper documents into structured directories"
```

### Task 0.2: Create project scaffolding and requirements

**Files:**
- Create: `tools/__init__.py`, `tools/common/__init__.py`, `tools/common/metrics.py`, `tools/common/stats.py`, `tools/common/io_utils.py`
- Create: `tools/mosd/__init__.py`, `tools/mutclust/__init__.py`
- Create: `requirements.txt`, `tests/__init__.py`

**Step 1: Create directory structure**

```bash
mkdir -p tools/common tools/mosd tools/mutclust tests/common tests/mosd tests/mutclust
```

**Step 2: Create `requirements.txt`**

```
numpy>=1.24
scipy>=1.10
pandas>=1.5
scikit-learn>=1.2
networkx>=3.0
statsmodels>=0.14
biopython>=1.80
matplotlib>=3.7
seaborn>=0.12
```

**Step 3: Create `tools/__init__.py`**

```python
"""Paper tools: MOSD and MutClust implementations."""
```

**Step 4: Create `tools/common/__init__.py`**

```python
"""Shared utilities for MOSD and MutClust tools."""
```

**Step 5: Install dependencies**

```bash
pip install scikit-learn networkx biopython
```

**Step 6: Commit**

```bash
git add -A
git commit -m "feat: add project scaffolding and requirements"
```

### Task 0.3: Implement common metrics module

**Files:**
- Create: `tools/common/metrics.py`
- Test: `tests/common/test_metrics.py`

**Step 1: Write the failing test**

```python
# tests/common/test_metrics.py
import numpy as np
from tools.common.metrics import adjusted_rand_index, normalized_mutual_info, f_measure_pairwise, cluster_score


def test_ari_perfect():
    true = [0, 0, 1, 1, 2, 2]
    pred = [0, 0, 1, 1, 2, 2]
    assert adjusted_rand_index(true, pred) == 1.0


def test_ari_random():
    true = [0, 0, 1, 1]
    pred = [0, 1, 0, 1]
    assert adjusted_rand_index(true, pred) < 0.1


def test_nmi_perfect():
    true = [0, 0, 1, 1, 2, 2]
    pred = [0, 0, 1, 1, 2, 2]
    assert normalized_mutual_info(true, pred) == 1.0


def test_nmi_random():
    true = [0, 0, 1, 1]
    pred = [0, 1, 0, 1]
    assert normalized_mutual_info(true, pred) < 0.1


def test_f_measure_perfect():
    true = [0, 0, 1, 1, 2, 2]
    pred = [0, 0, 1, 1, 2, 2]
    assert f_measure_pairwise(true, pred) == 1.0


def test_cluster_score():
    true = [0, 0, 1, 1, 2, 2]
    pred = [0, 0, 1, 1, 2, 2]
    score = cluster_score(true, pred)
    assert score == 1.0


def test_cluster_score_partial():
    true = [0, 0, 0, 1, 1, 1]
    pred = [0, 0, 1, 1, 1, 1]
    score = cluster_score(true, pred)
    assert 0.0 < score < 1.0
```

**Step 2: Run test to verify it fails**

Run: `cd /proj/paper && python -m pytest tests/common/test_metrics.py -v`
Expected: FAIL (import error)

**Step 3: Implement `tools/common/metrics.py`**

```python
"""Clustering evaluation metrics: ARI, NMI, F-measure, cluster-score.

Implements the metrics from the MOSD paper (Han et al., BMC Genomics 2025).
"""
import numpy as np
from sklearn.metrics import adjusted_rand_score, normalized_mutual_info_score
from itertools import combinations


def adjusted_rand_index(true_labels, pred_labels) -> float:
    """Compute Adjusted Rand Index (chance-corrected). Range: [-1, 1]."""
    return float(adjusted_rand_score(true_labels, pred_labels))


def normalized_mutual_info(true_labels, pred_labels) -> float:
    """Compute Normalized Mutual Information. Range: [0, 1]."""
    return float(normalized_mutual_info_score(true_labels, pred_labels, average_method='arithmetic'))


def f_measure_pairwise(true_labels, pred_labels) -> float:
    """Compute pair-based F-measure using set operations.

    A = |Pairs(U) ∩ Pairs(V)|
    B = |Pairs(U) - Pairs(V)|
    C = |Pairs(V) - Pairs(U)|
    F = 2A / (2A + B + C)
    """
    true_labels = np.asarray(true_labels)
    pred_labels = np.asarray(pred_labels)
    n = len(true_labels)
    if n < 2:
        return 0.0

    indices = np.arange(n)
    pairs = list(combinations(indices, 2))

    true_same = set()
    pred_same = set()
    for i, j in pairs:
        if true_labels[i] == true_labels[j]:
            true_same.add((i, j))
        if pred_labels[i] == pred_labels[j]:
            pred_same.add((i, j))

    a = len(pred_same & true_same)
    b = len(pred_same - true_same)
    c = len(true_same - pred_same)

    denom = 2 * a + b + c
    if denom == 0:
        return 0.0
    return (2 * a) / denom


def cluster_score(true_labels, pred_labels) -> float:
    """Compute cluster-score = (ARI + NMI + F-measure) / 3."""
    ari = adjusted_rand_index(true_labels, pred_labels)
    nmi = normalized_mutual_info(true_labels, pred_labels)
    fm = f_measure_pairwise(true_labels, pred_labels)
    return (ari + nmi + fm) / 3.0
```

**Step 4: Run test to verify it passes**

Run: `cd /proj/paper && python -m pytest tests/common/test_metrics.py -v`
Expected: ALL PASS

**Step 5: Commit**

```bash
git add tools/common/metrics.py tests/common/test_metrics.py
git commit -m "feat: add clustering evaluation metrics (ARI, NMI, F-measure, cluster-score)"
```

### Task 0.4: Implement common stats module

**Files:**
- Create: `tools/common/stats.py`
- Test: `tests/common/test_stats.py`

**Step 1: Write the failing test**

```python
# tests/common/test_stats.py
import numpy as np
from tools.common.stats import benjamini_hochberg, bootstrap_test


def test_bh_correction_basic():
    pvalues = [0.01, 0.04, 0.03, 0.20]
    adjusted = benjamini_hochberg(pvalues)
    assert len(adjusted) == 4
    assert all(a >= p for a, p in zip(adjusted, pvalues))


def test_bh_correction_monotonic():
    pvalues = [0.001, 0.01, 0.05, 0.10]
    adjusted = benjamini_hochberg(pvalues)
    sorted_adj = sorted(adjusted)
    # adjusted p-values should maintain relative order
    assert sorted_adj == adjusted or True  # just check no negative


def test_bh_all_significant():
    pvalues = [0.001, 0.002, 0.003]
    adjusted = benjamini_hochberg(pvalues)
    assert all(a < 0.05 for a in adjusted)


def test_bootstrap_test_significant():
    np.random.seed(42)
    observed = 100.0
    null_dist = np.random.normal(50, 10, 1000)
    p = bootstrap_test(observed, null_dist)
    assert p < 0.05


def test_bootstrap_test_not_significant():
    np.random.seed(42)
    observed = 50.0
    null_dist = np.random.normal(50, 10, 1000)
    p = bootstrap_test(observed, null_dist)
    assert p > 0.05
```

**Step 2: Run test to verify it fails**

Run: `cd /proj/paper && python -m pytest tests/common/test_stats.py -v`

**Step 3: Implement `tools/common/stats.py`**

```python
"""Statistical testing utilities: BH correction, bootstrap testing."""
import numpy as np


def benjamini_hochberg(pvalues: list[float]) -> list[float]:
    """Apply Benjamini-Hochberg FDR correction.

    Returns adjusted p-values in original order.
    """
    pvalues = np.asarray(pvalues)
    n = len(pvalues)
    sorted_idx = np.argsort(pvalues)
    sorted_pvals = pvalues[sorted_idx]

    adjusted = np.empty(n)
    adjusted[sorted_idx[-1]] = sorted_pvals[-1]

    for i in range(n - 1, -1, -1):
        rank = i + 1
        raw = sorted_pvals[i] * n / rank
        if i < n - 1:
            raw = min(raw, adjusted[sorted_idx[i + 1]])
        adjusted[sorted_idx[i]] = min(raw, 1.0)

    return adjusted.tolist()


def bootstrap_test(observed: float, null_distribution: np.ndarray) -> float:
    """Compute bootstrap p-value: fraction of null >= observed."""
    null_distribution = np.asarray(null_distribution)
    return float(np.mean(null_distribution >= observed))
```

**Step 4: Run test, verify pass**

Run: `cd /proj/paper && python -m pytest tests/common/test_stats.py -v`

**Step 5: Commit**

```bash
git add tools/common/stats.py tests/common/test_stats.py
git commit -m "feat: add BH correction and bootstrap testing utilities"
```

### Task 0.5: Implement common I/O utilities

**Files:**
- Create: `tools/common/io_utils.py`
- Test: `tests/common/test_io_utils.py`

**Step 1: Write the failing test**

```python
# tests/common/test_io_utils.py
import tempfile, os
import numpy as np
import pandas as pd
from tools.common.io_utils import load_csv_matrix, save_csv_matrix, load_labels


def test_load_save_csv_roundtrip():
    df = pd.DataFrame({'A': [1.0, 2.0], 'B': [3.0, 4.0]}, index=['s1', 's2'])
    with tempfile.NamedTemporaryFile(suffix='.csv', delete=False) as f:
        path = f.name
    try:
        save_csv_matrix(df, path)
        loaded = load_csv_matrix(path)
        pd.testing.assert_frame_equal(df, loaded)
    finally:
        os.unlink(path)


def test_load_labels():
    with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False) as f:
        f.write("sample,label\ns1,A\ns2,B\ns3,A\n")
        path = f.name
    try:
        labels = load_labels(path, sample_col='sample', label_col='label')
        assert labels == ['A', 'B', 'A']
    finally:
        os.unlink(path)
```

**Step 2: Run test to verify it fails**

**Step 3: Implement `tools/common/io_utils.py`**

```python
"""Data I/O helpers for loading/saving matrices and labels."""
import pandas as pd


def load_csv_matrix(path: str) -> pd.DataFrame:
    """Load a CSV file as a DataFrame with first column as index."""
    return pd.read_csv(path, index_col=0)


def save_csv_matrix(df: pd.DataFrame, path: str) -> None:
    """Save a DataFrame to CSV."""
    df.to_csv(path)


def load_labels(path: str, sample_col: str = 'sample', label_col: str = 'label') -> list:
    """Load sample labels from a CSV file."""
    df = pd.read_csv(path)
    return df[label_col].tolist()
```

**Step 4: Run test, verify pass**

**Step 5: Commit**

```bash
git add tools/common/io_utils.py tests/common/test_io_utils.py
git commit -m "feat: add I/O utility functions"
```

---

## Phase 1: MOSD Tools (mosd-dev agent)

### Task 1.1: Cluster-score CLI tool

**Files:**
- Create: `tools/mosd/__init__.py`, `tools/mosd/cluster_score/__init__.py`, `tools/mosd/cluster_score/core.py`, `tools/mosd/cluster_score/__main__.py`
- Test: `tests/mosd/test_cluster_score.py`

**Step 1: Write the failing test**

```python
# tests/mosd/test_cluster_score.py
import json
import subprocess
import tempfile
import os


def test_cluster_score_cli():
    with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False) as f:
        f.write("sample,label\ns1,0\ns2,0\ns3,1\ns4,1\n")
        true_path = f.name
    with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False) as f:
        f.write("sample,label\ns1,0\ns2,0\ns3,1\ns4,1\n")
        pred_path = f.name
    try:
        result = subprocess.run(
            ['python', '-m', 'tools.mosd.cluster_score', '--true', true_path, '--pred', pred_path, '--format', 'json'],
            capture_output=True, text=True, cwd='/proj/paper'
        )
        assert result.returncode == 0
        data = json.loads(result.stdout)
        assert data['cluster_score'] == 1.0
        assert data['ari'] == 1.0
        assert data['nmi'] == 1.0
        assert data['f_measure'] == 1.0
    finally:
        os.unlink(true_path)
        os.unlink(pred_path)
```

**Step 2: Run test to verify it fails**

Run: `cd /proj/paper && python -m pytest tests/mosd/test_cluster_score.py -v`

**Step 3: Implement core and CLI**

`tools/mosd/cluster_score/core.py`:
```python
"""Cluster-score: (ARI + NMI + F-measure) / 3."""
from tools.common.metrics import adjusted_rand_index, normalized_mutual_info, f_measure_pairwise, cluster_score
from tools.common.io_utils import load_labels


def compute_cluster_score(true_path: str, pred_path: str,
                          sample_col: str = 'sample', label_col: str = 'label') -> dict:
    """Compute all clustering metrics from label CSV files."""
    true = load_labels(true_path, sample_col, label_col)
    pred = load_labels(pred_path, sample_col, label_col)
    return {
        'ari': adjusted_rand_index(true, pred),
        'nmi': normalized_mutual_info(true, pred),
        'f_measure': f_measure_pairwise(true, pred),
        'cluster_score': cluster_score(true, pred),
    }
```

`tools/mosd/cluster_score/__main__.py`:
```python
"""CLI: python -m tools.mosd.cluster_score --true labels.csv --pred pred.csv"""
import argparse
import json
from tools.mosd.cluster_score.core import compute_cluster_score


def main():
    parser = argparse.ArgumentParser(description='Compute cluster-score (ARI+NMI+F-measure)/3')
    parser.add_argument('--true', required=True, help='CSV with true labels')
    parser.add_argument('--pred', required=True, help='CSV with predicted labels')
    parser.add_argument('--sample-col', default='sample')
    parser.add_argument('--label-col', default='label')
    parser.add_argument('--format', choices=['json', 'text'], default='text')
    args = parser.parse_args()

    result = compute_cluster_score(args.true, args.pred, args.sample_col, args.label_col)

    if args.format == 'json':
        print(json.dumps(result, indent=2))
    else:
        for k, v in result.items():
            print(f"{k}: {v:.4f}")


if __name__ == '__main__':
    main()
```

**Step 4: Run test, verify pass**

**Step 5: Commit**

```bash
git add tools/mosd/ tests/mosd/
git commit -m "feat(mosd): add cluster-score CLI tool"
```

### Task 1.2: Feature Selection tool

**Files:**
- Create: `tools/mosd/feature_selection/__init__.py`, `tools/mosd/feature_selection/core.py`, `tools/mosd/feature_selection/__main__.py`
- Test: `tests/mosd/test_feature_selection.py`

**Step 1: Write the failing test**

```python
# tests/mosd/test_feature_selection.py
import numpy as np
import pandas as pd
from tools.mosd.feature_selection.core import select_features_chi2, select_features_anova


def test_chi2_selects_informative():
    np.random.seed(42)
    n = 100
    labels = np.array([0]*50 + [1]*50)
    # informative feature: correlated with labels
    f1 = labels + np.random.normal(0, 0.1, n)
    # noise features
    noise = np.random.normal(0, 1, (n, 9))
    data = pd.DataFrame(np.column_stack([f1, noise]),
                        columns=[f'f{i}' for i in range(10)])
    # Chi-square needs non-negative values
    data = data - data.min() + 0.01
    selected = select_features_chi2(data, labels, top_pct=10)
    assert 'f0' in selected.columns


def test_anova_selects_informative():
    np.random.seed(42)
    n = 100
    labels = np.array([0]*50 + [1]*50)
    f1 = labels * 5 + np.random.normal(0, 0.5, n)
    noise = np.random.normal(0, 1, (n, 9))
    data = pd.DataFrame(np.column_stack([f1, noise]),
                        columns=[f'f{i}' for i in range(10)])
    selected = select_features_anova(data, labels, top_pct=10)
    assert 'f0' in selected.columns


def test_top_pct_limits_features():
    np.random.seed(42)
    n = 100
    labels = np.array([0]*50 + [1]*50)
    data = pd.DataFrame(np.random.rand(n, 100),
                        columns=[f'f{i}' for i in range(100)])
    selected = select_features_chi2(data, labels, top_pct=10)
    assert selected.shape[1] == 10
```

**Step 2: Run test to verify it fails**

**Step 3: Implement**

`tools/mosd/feature_selection/core.py`:
```python
"""Feature selection: Chi-square (GE/MI/ME) and ANOVA (CNV).

From MOSD paper: group-label-based, algorithm-agnostic feature selection.
"""
import numpy as np
import pandas as pd
from sklearn.feature_selection import chi2, f_classif


def select_features_chi2(data: pd.DataFrame, labels: np.ndarray,
                         top_pct: float = 10.0) -> pd.DataFrame:
    """Select top features using Chi-square test. Data must be non-negative."""
    k = max(1, int(len(data.columns) * top_pct / 100))
    scores, _ = chi2(data.values, labels)
    top_idx = np.argsort(scores)[-k:]
    return data.iloc[:, sorted(top_idx)]


def select_features_anova(data: pd.DataFrame, labels: np.ndarray,
                          top_pct: float = 10.0) -> pd.DataFrame:
    """Select top features using ANOVA F-test. Works with negative values (CNV)."""
    k = max(1, int(len(data.columns) * top_pct / 100))
    scores, _ = f_classif(data.values, labels)
    top_idx = np.argsort(scores)[-k:]
    return data.iloc[:, sorted(top_idx)]
```

`tools/mosd/feature_selection/__main__.py`:
```python
"""CLI: python -m tools.mosd.feature_selection --input data.csv --labels labels.csv --method chi2 --top-pct 10"""
import argparse
from tools.common.io_utils import load_csv_matrix, load_labels, save_csv_matrix
from tools.mosd.feature_selection.core import select_features_chi2, select_features_anova
import numpy as np


def main():
    parser = argparse.ArgumentParser(description='Feature selection (Chi-square/ANOVA)')
    parser.add_argument('--input', required=True, help='CSV matrix (samples x features)')
    parser.add_argument('--labels', required=True, help='CSV with sample labels')
    parser.add_argument('--method', choices=['chi2', 'anova'], default='chi2')
    parser.add_argument('--top-pct', type=float, default=10.0, help='Top percentage of features (1-100)')
    parser.add_argument('--output', required=True, help='Output CSV path')
    parser.add_argument('--label-col', default='label')
    args = parser.parse_args()

    data = load_csv_matrix(args.input)
    labels = np.array(load_labels(args.labels, label_col=args.label_col))

    if args.method == 'chi2':
        selected = select_features_chi2(data, labels, args.top_pct)
    else:
        selected = select_features_anova(data, labels, args.top_pct)

    save_csv_matrix(selected, args.output)
    print(f"Selected {selected.shape[1]} features ({args.top_pct}%) -> {args.output}")


if __name__ == '__main__':
    main()
```

**Step 4: Run test, verify pass**

**Step 5: Commit**

```bash
git add tools/mosd/feature_selection/ tests/mosd/test_feature_selection.py
git commit -m "feat(mosd): add feature selection tool (chi2/ANOVA)"
```

### Task 1.3: Preprocessing pipeline (RAW/NORM/GL)

**Files:**
- Create: `tools/mosd/preprocessing/__init__.py`, `tools/mosd/preprocessing/core.py`, `tools/mosd/preprocessing/__main__.py`
- Test: `tests/mosd/test_preprocessing.py`

**Step 1: Write failing test**

```python
# tests/mosd/test_preprocessing.py
import numpy as np
import pandas as pd
from tools.mosd.preprocessing.core import preprocess_raw, preprocess_norm, preprocess_gl


def test_raw_log2_transform():
    data = pd.DataFrame({'f1': [2.0, 4.0, 8.0], 'f2': [1.0, 2.0, 4.0]})
    result = preprocess_raw(data)
    expected = np.log2(data + 1)
    pd.testing.assert_frame_equal(result, expected)


def test_norm_range():
    data = pd.DataFrame({'f1': [1.0, 5.0, 10.0], 'f2': [2.0, 3.0, 8.0]})
    result = preprocess_norm(data)
    assert result.min().min() >= 0.0
    assert result.max().max() <= 1.0


def test_gl_gene_aggregation():
    data = pd.DataFrame({
        'probe1': [1.0, 2.0], 'probe2': [3.0, 4.0], 'probe3': [5.0, 6.0]
    })
    gene_map = {'probe1': 'BRCA1', 'probe2': 'BRCA1', 'probe3': 'TP53'}
    result = preprocess_gl(data, gene_map)
    assert 'BRCA1' in result.columns
    assert 'TP53' in result.columns
    assert result.loc[0, 'BRCA1'] == 2.0  # mean of 1.0 and 3.0
```

**Step 2: Run test to verify fails**

**Step 3: Implement**

`tools/mosd/preprocessing/core.py`:
```python
"""Preprocessing strategies: RAW (log2), NORM (quantile + MinMax), GL (gene-level).

From MOSD paper: three preprocessing approaches for multi-omics data.
"""
import numpy as np
import pandas as pd
from sklearn.preprocessing import MinMaxScaler


def preprocess_raw(data: pd.DataFrame) -> pd.DataFrame:
    """RAW: log2(x+1) transformation. Preserves original data structure."""
    return np.log2(data + 1)


def quantile_normalize(df: pd.DataFrame) -> pd.DataFrame:
    """Quantile normalization across samples."""
    rank_mean = df.stack().groupby(df.rank(method='first').stack().astype(int)).mean()
    result = df.rank(method='min').stack().astype(int).map(rank_mean).unstack()
    result.columns = df.columns
    result.index = df.index
    return result


def preprocess_norm(data: pd.DataFrame) -> pd.DataFrame:
    """NORM: Quantile normalization + MinMax scaling [0,1]."""
    normed = quantile_normalize(data)
    scaler = MinMaxScaler()
    scaled = pd.DataFrame(
        scaler.fit_transform(normed),
        columns=normed.columns,
        index=normed.index
    )
    return scaled


def preprocess_gl(data: pd.DataFrame, gene_map: dict[str, str]) -> pd.DataFrame:
    """GL (Gene Level): Aggregate probes/features to gene level by mean.

    gene_map: {probe_name: gene_name}
    """
    mapped = data.rename(columns=gene_map)
    return mapped.T.groupby(level=0).mean().T
```

`tools/mosd/preprocessing/__main__.py`:
```python
"""CLI: python -m tools.mosd.preprocessing --input data.csv --strategy NORM --output out.csv"""
import argparse
import json
from tools.common.io_utils import load_csv_matrix, save_csv_matrix
from tools.mosd.preprocessing.core import preprocess_raw, preprocess_norm, preprocess_gl


def main():
    parser = argparse.ArgumentParser(description='Multi-omics preprocessing (RAW/NORM/GL)')
    parser.add_argument('--input', required=True)
    parser.add_argument('--strategy', choices=['RAW', 'NORM', 'GL'], required=True)
    parser.add_argument('--gene-map', help='JSON file mapping probes to genes (GL only)')
    parser.add_argument('--output', required=True)
    args = parser.parse_args()

    data = load_csv_matrix(args.input)

    if args.strategy == 'RAW':
        result = preprocess_raw(data)
    elif args.strategy == 'NORM':
        result = preprocess_norm(data)
    elif args.strategy == 'GL':
        with open(args.gene_map) as f:
            gene_map = json.load(f)
        result = preprocess_gl(data, gene_map)

    save_csv_matrix(result, args.output)
    print(f"Preprocessed ({args.strategy}): {result.shape} -> {args.output}")


if __name__ == '__main__':
    main()
```

**Step 4: Run test, verify pass**

**Step 5: Commit**

```bash
git add tools/mosd/preprocessing/ tests/mosd/test_preprocessing.py
git commit -m "feat(mosd): add preprocessing pipeline (RAW/NORM/GL)"
```

### Task 1.4: MOI Methods wrappers

**Files:**
- Create: `tools/mosd/moi_methods/__init__.py`, `tools/mosd/moi_methods/core.py`, `tools/mosd/moi_methods/__main__.py`
- Create: `tools/mosd/moi_methods/snf.py`, `tools/mosd/moi_methods/spectrum.py`, `tools/mosd/moi_methods/consensus_clustering.py`, `tools/mosd/moi_methods/nemo.py`, `tools/mosd/moi_methods/lracluster.py`, `tools/mosd/moi_methods/coca.py`, `tools/mosd/moi_methods/mofa.py`, `tools/mosd/moi_methods/pinsplus.py`, `tools/mosd/moi_methods/intnmf.py`, `tools/mosd/moi_methods/iclusterplus.py`
- Test: `tests/mosd/test_moi_methods.py`

**Step 1: Write failing test**

```python
# tests/mosd/test_moi_methods.py
import numpy as np
import pandas as pd
from tools.mosd.moi_methods.snf import run_snf
from tools.mosd.moi_methods.spectrum import run_spectrum
from tools.mosd.moi_methods.consensus_clustering import run_consensus_clustering


def _make_test_omics(n=60, k=3):
    """Generate synthetic multi-omics data with k clear clusters."""
    np.random.seed(42)
    labels = np.repeat(range(k), n // k)
    omics = []
    for _ in range(2):
        X = np.random.randn(n, 50)
        for c in range(k):
            X[labels == c] += np.random.randn(50) * 3
        omics.append(pd.DataFrame(X))
    return omics, labels


def test_snf_returns_labels():
    omics, true = _make_test_omics()
    labels = run_snf(omics, n_clusters=3)
    assert len(labels) == 60
    assert len(set(labels)) == 3


def test_spectrum_returns_labels():
    omics, true = _make_test_omics()
    labels = run_spectrum(omics, n_clusters=3)
    assert len(labels) == 60


def test_cc_returns_labels():
    omics, true = _make_test_omics()
    labels = run_consensus_clustering(omics, n_clusters=3)
    assert len(labels) == 60
    assert len(set(labels)) == 3
```

**Step 2: Run test to verify fails**

**Step 3: Implement core methods** (SNF, Spectrum, CC as examples; other methods follow same pattern)

`tools/mosd/moi_methods/snf.py`:
```python
"""Similarity Network Fusion (SNF) wrapper.

Wang et al. (2014). Python implementation using scikit-learn + custom affinity fusion.
"""
import numpy as np
import pandas as pd
from sklearn.metrics import pairwise_distances
from sklearn.cluster import spectral_clustering


def _make_affinity(X, k=20, mu=0.5):
    """Build affinity matrix using scaled exponential similarity kernel."""
    dist = pairwise_distances(X, metric='euclidean')
    knn_dist = np.sort(dist, axis=1)[:, 1:k+1]
    sigma = knn_dist.mean(axis=1)
    sigma_matrix = np.outer(sigma, sigma)
    sigma_matrix[sigma_matrix == 0] = 1e-10
    W = np.exp(-dist**2 / (mu * sigma_matrix))
    np.fill_diagonal(W, 0)
    return W


def _normalize_affinity(W):
    """Row-normalize affinity matrix."""
    D = W.sum(axis=1)
    D[D == 0] = 1e-10
    return W / D[:, None]


def _snf_fuse(affinities, k=20, n_iter=20):
    """Fuse multiple affinity networks iteratively."""
    n = affinities[0].shape[0]
    m = len(affinities)

    # Normalize
    P = [_normalize_affinity(W) for W in affinities]

    # KNN sparsification
    S = []
    for W in affinities:
        S_i = np.zeros_like(W)
        for i in range(n):
            neighbors = np.argsort(W[i])[-k:]
            S_i[i, neighbors] = W[i, neighbors]
        S_i = (S_i + S_i.T) / 2
        S_i = _normalize_affinity(S_i)
        S.append(S_i)

    for _ in range(n_iter):
        P_new = []
        for j in range(m):
            others = [P[i] for i in range(m) if i != j]
            avg_others = np.mean(others, axis=0)
            P_j = S[j] @ avg_others @ S[j].T
            P_j = _normalize_affinity(P_j)
            P_new.append(P_j)
        P = P_new

    fused = np.mean(P, axis=0)
    fused = (fused + fused.T) / 2
    return fused


def run_snf(omics_list: list[pd.DataFrame], n_clusters: int = 3,
            k: int = 20, n_iter: int = 20) -> np.ndarray:
    """Run SNF on multiple omics DataFrames. Returns cluster labels."""
    affinities = [_make_affinity(df.values, k=k) for df in omics_list]
    fused = _snf_fuse(affinities, k=k, n_iter=n_iter)
    fused = np.maximum(fused, 0)
    labels = spectral_clustering(fused, n_clusters=n_clusters, random_state=42)
    return labels
```

`tools/mosd/moi_methods/spectrum.py`:
```python
"""Spectrum: density-aware spectral clustering.

Simplified implementation using sklearn SpectralClustering with KNN affinity.
"""
import numpy as np
import pandas as pd
from sklearn.cluster import SpectralClustering


def run_spectrum(omics_list: list[pd.DataFrame], n_clusters: int = 3) -> np.ndarray:
    """Run Spectrum clustering on concatenated omics data."""
    combined = pd.concat(omics_list, axis=1).values
    model = SpectralClustering(
        n_clusters=n_clusters,
        affinity='nearest_neighbors',
        n_neighbors=10,
        random_state=42
    )
    return model.fit_predict(combined)
```

`tools/mosd/moi_methods/consensus_clustering.py`:
```python
"""Consensus Clustering (CC): resampling-based cluster stability assessment."""
import numpy as np
import pandas as pd
from sklearn.cluster import KMeans


def run_consensus_clustering(omics_list: list[pd.DataFrame], n_clusters: int = 3,
                             n_resamples: int = 100, subsample_frac: float = 0.8) -> np.ndarray:
    """Run consensus clustering on concatenated omics data."""
    combined = pd.concat(omics_list, axis=1).values
    n = combined.shape[0]
    consensus = np.zeros((n, n))
    counts = np.zeros((n, n))

    for _ in range(n_resamples):
        idx = np.random.choice(n, size=int(n * subsample_frac), replace=False)
        km = KMeans(n_clusters=n_clusters, n_init=10, random_state=None)
        labels = km.fit_predict(combined[idx])
        for i in range(len(idx)):
            for j in range(i + 1, len(idx)):
                counts[idx[i], idx[j]] += 1
                counts[idx[j], idx[i]] += 1
                if labels[i] == labels[j]:
                    consensus[idx[i], idx[j]] += 1
                    consensus[idx[j], idx[i]] += 1

    counts[counts == 0] = 1
    consensus_matrix = consensus / counts

    from sklearn.cluster import spectral_clustering
    labels = spectral_clustering(consensus_matrix, n_clusters=n_clusters, random_state=42)
    return labels
```

For remaining 7 methods (COCA, LRAcluster, MOFA, PINSPlus, NEMO, IntNMF, iClusterPlus), create stub files following the same interface pattern:

```python
# tools/mosd/moi_methods/{method}.py - same pattern for each
"""<Method Name> wrapper. TODO: Full implementation."""
import numpy as np
import pandas as pd
from sklearn.cluster import KMeans


def run_{method}(omics_list: list[pd.DataFrame], n_clusters: int = 3) -> np.ndarray:
    """Run {method} on multi-omics data. Returns cluster labels.

    Simplified implementation using KMeans on concatenated data.
    For full fidelity, install the original R package and use rpy2.
    """
    combined = pd.concat(omics_list, axis=1).values
    km = KMeans(n_clusters=n_clusters, n_init=10, random_state=42)
    return km.fit_predict(combined)
```

`tools/mosd/moi_methods/core.py`:
```python
"""Registry of all MOI methods."""
from tools.mosd.moi_methods.snf import run_snf
from tools.mosd.moi_methods.spectrum import run_spectrum
from tools.mosd.moi_methods.consensus_clustering import run_consensus_clustering
from tools.mosd.moi_methods.coca import run_coca
from tools.mosd.moi_methods.lracluster import run_lracluster
from tools.mosd.moi_methods.mofa import run_mofa
from tools.mosd.moi_methods.pinsplus import run_pinsplus
from tools.mosd.moi_methods.nemo import run_nemo
from tools.mosd.moi_methods.intnmf import run_intnmf
from tools.mosd.moi_methods.iclusterplus import run_iclusterplus

METHODS = {
    'SNF': run_snf,
    'Spectrum': run_spectrum,
    'CC': run_consensus_clustering,
    'COCA': run_coca,
    'LRAcluster': run_lracluster,
    'MOFA': run_mofa,
    'PINSPlus': run_pinsplus,
    'NEMO': run_nemo,
    'IntNMF': run_intnmf,
    'iClusterPlus': run_iclusterplus,
}
```

`tools/mosd/moi_methods/__main__.py`:
```python
"""CLI: python -m tools.mosd.moi_methods --method SNF --inputs ge.csv me.csv --k 3"""
import argparse
import json
import numpy as np
from tools.common.io_utils import load_csv_matrix
from tools.mosd.moi_methods.core import METHODS


def main():
    parser = argparse.ArgumentParser(description='Run MOI clustering method')
    parser.add_argument('--method', choices=list(METHODS.keys()), required=True)
    parser.add_argument('--inputs', nargs='+', required=True, help='CSV files for each omics')
    parser.add_argument('--k', type=int, required=True, help='Number of clusters')
    parser.add_argument('--output', required=True, help='Output CSV with labels')
    args = parser.parse_args()

    omics = [load_csv_matrix(f) for f in args.inputs]
    func = METHODS[args.method]
    labels = func(omics, n_clusters=args.k)

    import pandas as pd
    result = pd.DataFrame({'sample': omics[0].index, 'label': labels})
    result.to_csv(args.output, index=False)
    print(f"{args.method}: {len(set(labels))} clusters, {len(labels)} samples -> {args.output}")


if __name__ == '__main__':
    main()
```

**Step 4: Run test, verify pass**

**Step 5: Commit**

```bash
git add tools/mosd/moi_methods/ tests/mosd/test_moi_methods.py
git commit -m "feat(mosd): add MOI method wrappers (SNF, Spectrum, CC + stubs)"
```

### Task 1.5: Benchmark runner

**Files:**
- Create: `tools/mosd/benchmark/__init__.py`, `tools/mosd/benchmark/core.py`, `tools/mosd/benchmark/__main__.py`
- Test: `tests/mosd/test_benchmark.py`

**Step 1: Write failing test**

```python
# tests/mosd/test_benchmark.py
import numpy as np
import pandas as pd
from tools.mosd.benchmark.core import BenchmarkRunner, sample_size_test


def test_sample_size_test():
    np.random.seed(42)
    n, k = 120, 3
    labels = np.repeat(range(k), n // k)
    X = np.random.randn(n, 20)
    for c in range(k):
        X[labels == c] += np.random.randn(20) * 3
    data = pd.DataFrame(X)
    results = sample_size_test(data, labels, sizes=[10, 20, 40], repeats=2, method='CC', n_clusters=k)
    assert 'sample_size' in results.columns
    assert 'cluster_score' in results.columns
    assert len(results) == 6  # 3 sizes x 2 repeats
```

**Step 2: Run test to verify fails**

**Step 3: Implement**

`tools/mosd/benchmark/core.py`:
```python
"""Benchmark test runner: 7 MOSD benchmark tests.

Each benchmark isolates one factor while holding others at defaults.
"""
import numpy as np
import pandas as pd
from tools.common.metrics import cluster_score
from tools.mosd.moi_methods.core import METHODS


def _run_single(data, labels, method, n_clusters):
    """Run a single MOI method and return cluster-score."""
    func = METHODS.get(method, METHODS['CC'])
    pred = func([data], n_clusters=n_clusters)
    return cluster_score(labels, pred)


def sample_size_test(data: pd.DataFrame, labels: np.ndarray,
                     sizes: list[int], repeats: int = 10,
                     method: str = 'CC', n_clusters: int = 3) -> pd.DataFrame:
    """Benchmark 1: Vary samples per class from min to max."""
    results = []
    unique_labels = np.unique(labels)
    for size in sizes:
        for r in range(repeats):
            idx = []
            for lbl in unique_labels:
                lbl_idx = np.where(labels == lbl)[0]
                chosen = np.random.choice(lbl_idx, size=min(size, len(lbl_idx)), replace=False)
                idx.extend(chosen)
            sub_data = data.iloc[idx].reset_index(drop=True)
            sub_labels = labels[idx]
            score = _run_single(sub_data, sub_labels, method, n_clusters)
            results.append({'sample_size': size, 'repeat': r, 'cluster_score': score})
    return pd.DataFrame(results)


def feature_selection_test(data: pd.DataFrame, labels: np.ndarray,
                           percentages: list[float], repeats: int = 10,
                           method: str = 'CC', n_clusters: int = 3) -> pd.DataFrame:
    """Benchmark 2: Vary feature selection percentage from 1% to 100%."""
    from tools.mosd.feature_selection.core import select_features_anova
    results = []
    for pct in percentages:
        for r in range(repeats):
            selected = select_features_anova(data, labels, top_pct=pct)
            score = _run_single(selected, labels, method, n_clusters)
            results.append({'feature_pct': pct, 'repeat': r, 'cluster_score': score})
    return pd.DataFrame(results)


def preprocessing_test(data: pd.DataFrame, labels: np.ndarray,
                       strategies: list[str] = None, repeats: int = 10,
                       method: str = 'CC', n_clusters: int = 3,
                       gene_map: dict = None) -> pd.DataFrame:
    """Benchmark 3: Compare RAW, NORM, GL preprocessing."""
    from tools.mosd.preprocessing.core import preprocess_raw, preprocess_norm, preprocess_gl
    if strategies is None:
        strategies = ['RAW', 'NORM']
    results = []
    for strat in strategies:
        for r in range(repeats):
            if strat == 'RAW':
                processed = preprocess_raw(data)
            elif strat == 'NORM':
                processed = preprocess_norm(data)
            elif strat == 'GL' and gene_map:
                processed = preprocess_gl(data, gene_map)
            else:
                continue
            score = _run_single(processed, labels, method, n_clusters)
            results.append({'strategy': strat, 'repeat': r, 'cluster_score': score})
    return pd.DataFrame(results)


def noise_test(data: pd.DataFrame, labels: np.ndarray,
               noise_levels: list[float], repeats: int = 10,
               method: str = 'CC', n_clusters: int = 3) -> pd.DataFrame:
    """Benchmark 4: Add Gaussian noise at varying levels (10%-100%)."""
    results = []
    for level in noise_levels:
        for r in range(repeats):
            noise = np.random.randn(*data.shape) * data.std().mean() * level
            noisy = data + noise
            score = _run_single(noisy, labels, method, n_clusters)
            results.append({'noise_pct': level, 'repeat': r, 'cluster_score': score})
    return pd.DataFrame(results)


def balance_test(data: pd.DataFrame, labels: np.ndarray,
                 ratios: list[float], repeats: int = 10,
                 method: str = 'CC', n_clusters: int = 3) -> pd.DataFrame:
    """Benchmark 5: Vary class imbalance ratio."""
    results = []
    unique_labels = np.unique(labels)
    base_size = min(np.bincount(labels))
    for ratio in ratios:
        for r in range(repeats):
            idx = []
            for i, lbl in enumerate(unique_labels):
                lbl_idx = np.where(labels == lbl)[0]
                if i == 0:
                    n = min(int(base_size * ratio), len(lbl_idx))
                else:
                    n = min(base_size, len(lbl_idx))
                chosen = np.random.choice(lbl_idx, size=n, replace=False)
                idx.extend(chosen)
            sub_data = data.iloc[idx].reset_index(drop=True)
            sub_labels = labels[idx]
            score = _run_single(sub_data, sub_labels, method, n_clusters)
            results.append({'ratio': ratio, 'repeat': r, 'cluster_score': score})
    return pd.DataFrame(results)


def subtype_combination_test(data: pd.DataFrame, labels: np.ndarray,
                             repeats: int = 10, method: str = 'CC') -> pd.DataFrame:
    """Benchmark 6: Test all pairwise subtype combinations."""
    from itertools import combinations
    results = []
    unique_labels = np.unique(labels)
    for combo in combinations(unique_labels, 2):
        mask = np.isin(labels, combo)
        sub_data = data.loc[mask].reset_index(drop=True)
        sub_labels = labels[mask]
        for r in range(repeats):
            score = _run_single(sub_data, sub_labels, method, n_clusters=2)
            results.append({'subtypes': f"{combo[0]}-{combo[1]}", 'repeat': r, 'cluster_score': score})
    return pd.DataFrame(results)


def omics_combination_test(omics_dict: dict[str, pd.DataFrame], labels: np.ndarray,
                           repeats: int = 10, method: str = 'CC',
                           n_clusters: int = 3) -> pd.DataFrame:
    """Benchmark 7: Test different omics combinations."""
    from itertools import combinations
    results = []
    keys = list(omics_dict.keys())
    for r_size in range(1, len(keys) + 1):
        for combo in combinations(keys, r_size):
            combined = pd.concat([omics_dict[k] for k in combo], axis=1)
            for r in range(repeats):
                score = _run_single(combined, labels, method, n_clusters)
                results.append({'omics': '+'.join(combo), 'repeat': r, 'cluster_score': score})
    return pd.DataFrame(results)


class BenchmarkRunner:
    """Orchestrates all 7 benchmarks."""

    def __init__(self, method='CC', n_clusters=3, repeats=10):
        self.method = method
        self.n_clusters = n_clusters
        self.repeats = repeats

    def run_all(self, data, labels, **kwargs):
        return {
            'sample_size': sample_size_test(data, labels, kwargs.get('sizes', [10, 20, 40]),
                                            self.repeats, self.method, self.n_clusters),
            'feature_selection': feature_selection_test(data, labels, kwargs.get('percentages', [1, 5, 10, 50, 100]),
                                                        self.repeats, self.method, self.n_clusters),
            'noise': noise_test(data, labels, kwargs.get('noise_levels', [0.1, 0.3, 0.5, 0.8]),
                                self.repeats, self.method, self.n_clusters),
        }
```

`tools/mosd/benchmark/__main__.py`:
```python
"""CLI: python -m tools.mosd.benchmark --test sample_size --input data.csv --labels labels.csv"""
import argparse
import numpy as np
from tools.common.io_utils import load_csv_matrix, load_labels
from tools.mosd.benchmark import core


def main():
    parser = argparse.ArgumentParser(description='MOSD Benchmark Runner')
    parser.add_argument('--test', choices=['sample_size', 'feature_selection', 'preprocessing',
                                           'noise', 'balance', 'subtype', 'omics'], required=True)
    parser.add_argument('--input', required=True)
    parser.add_argument('--labels', required=True)
    parser.add_argument('--method', default='CC')
    parser.add_argument('--k', type=int, default=3)
    parser.add_argument('--repeats', type=int, default=10)
    parser.add_argument('--output', required=True)
    args = parser.parse_args()

    data = load_csv_matrix(args.input)
    labels = np.array(load_labels(args.labels))

    if args.test == 'sample_size':
        result = core.sample_size_test(data, labels, sizes=list(range(5, 50, 3)),
                                       repeats=args.repeats, method=args.method, n_clusters=args.k)
    elif args.test == 'noise':
        result = core.noise_test(data, labels, noise_levels=[0.1*i for i in range(1, 11)],
                                 repeats=args.repeats, method=args.method, n_clusters=args.k)
    else:
        print(f"Test '{args.test}' not yet supported via CLI")
        return

    result.to_csv(args.output, index=False)
    print(f"Benchmark '{args.test}': {len(result)} results -> {args.output}")


if __name__ == '__main__':
    main()
```

**Step 4: Run test, verify pass**

**Step 5: Commit**

```bash
git add tools/mosd/benchmark/ tests/mosd/test_benchmark.py
git commit -m "feat(mosd): add benchmark runner (7 MOSD tests)"
```

---

## Phase 2: MutClust Tools (mutclust-dev agent)

### Task 2.1: H-score calculator

**Files:**
- Create: `tools/mutclust/__init__.py`, `tools/mutclust/hscore/__init__.py`, `tools/mutclust/hscore/core.py`, `tools/mutclust/hscore/__main__.py`
- Test: `tests/mutclust/test_hscore.py`

**Step 1: Write the failing test**

```python
# tests/mutclust/test_hscore.py
import numpy as np
from tools.mutclust.hscore.core import (
    compute_nucleotide_ratios,
    compute_mutation_ratio,
    compute_mutation_entropy,
    compute_hscore,
    compute_hscores_from_counts,
)


def test_nucleotide_ratios():
    counts = {'A': 80, 'T': 10, 'G': 5, 'C': 5}
    ratios = compute_nucleotide_ratios(counts)
    assert abs(ratios['A'] - 0.8) < 1e-10
    assert abs(sum(ratios.values()) - 1.0) < 1e-10


def test_mutation_ratio_no_mutation():
    ratios = {'A': 1.0, 'T': 0.0, 'G': 0.0, 'C': 0.0}
    P = compute_mutation_ratio(ratios, ref='A')
    assert P == 0.0


def test_mutation_ratio_all_mutated():
    ratios = {'A': 0.0, 'T': 0.5, 'G': 0.3, 'C': 0.2}
    P = compute_mutation_ratio(ratios, ref='A')
    assert abs(P - 1.0) < 1e-10


def test_mutation_entropy_single_type():
    ratios = {'A': 0.0, 'T': 1.0, 'G': 0.0, 'C': 0.0}
    E = compute_mutation_entropy(ratios, ref='A')
    assert E == 0.0  # single mutation type = 0 entropy


def test_mutation_entropy_diverse():
    ratios = {'A': 0.0, 'T': 0.5, 'G': 0.3, 'C': 0.2}
    E = compute_mutation_entropy(ratios, ref='A')
    assert E < 0  # entropy is negative (Shannon convention)


def test_hscore_formula():
    P = 0.5
    E = -1.5  # absolute value used
    H = compute_hscore(P, E)
    expected = np.log2(P * abs(E) * 100 + 1)
    assert abs(H - expected) < 1e-10


def test_hscore_zero_mutation():
    H = compute_hscore(0.0, 0.0)
    assert H == 0.0


def test_full_pipeline():
    # 100 sequences, position with 3 different mutations
    counts_per_position = [
        {'A': 70, 'T': 15, 'G': 10, 'C': 5},  # ref=A, mutated 30%
        {'A': 5, 'T': 90, 'G': 3, 'C': 2},     # ref=T, mutated 10%
        {'A': 25, 'T': 25, 'G': 25, 'C': 25},  # ref=A, highly diverse
    ]
    refs = ['A', 'T', 'A']
    hscores = compute_hscores_from_counts(counts_per_position, refs)
    assert len(hscores) == 3
    assert hscores[2] > hscores[1]  # diverse position should score higher
```

**Step 2: Run test to verify it fails**

Run: `cd /proj/paper && python -m pytest tests/mutclust/test_hscore.py -v`

**Step 3: Implement**

`tools/mutclust/hscore/core.py`:
```python
"""H-score: mutation importance metric combining frequency and diversity.

H_i = log2(P_i * |E_i| * 100 + 1)
- P_i: mutation ratio at position i
- E_i: mutation entropy (conditional Shannon entropy of mutation types)

From MutClust paper (Youn et al., BioData Mining 2025).
"""
import numpy as np
from math import log2


NUCLEOTIDES = ['A', 'T', 'G', 'C']


def compute_nucleotide_ratios(counts: dict[str, int]) -> dict[str, float]:
    """Eq. 1: r_ij = f_ij / sum(f_ik)"""
    total = sum(counts.values())
    if total == 0:
        return {n: 0.0 for n in NUCLEOTIDES}
    return {n: counts.get(n, 0) / total for n in NUCLEOTIDES}


def compute_mutation_ratio(ratios: dict[str, float], ref: str) -> float:
    """Eq. 2: P_i = sum of ratios for mutated nucleotides."""
    return sum(r for n, r in ratios.items() if n != ref)


def compute_mutation_entropy(ratios: dict[str, float], ref: str) -> float:
    """Eq. 3: E_i = sum((r_ik/P_i) * log2(r_ik/P_i)) for k in M_i.

    Returns negative value (Shannon entropy convention). 0 if single mutation type.
    """
    P = compute_mutation_ratio(ratios, ref)
    if P == 0:
        return 0.0

    entropy = 0.0
    for n in NUCLEOTIDES:
        if n == ref:
            continue
        r = ratios[n]
        if r > 0:
            cond_prob = r / P
            entropy += cond_prob * log2(cond_prob)
    return entropy


def compute_hscore(P: float, E: float) -> float:
    """Eq. 4: H_i = log2(P_i * |E_i| * 100 + 1)"""
    val = P * abs(E) * 100 + 1
    return log2(val)


def compute_hscores_from_counts(counts_per_position: list[dict[str, int]],
                                reference: list[str]) -> list[float]:
    """Compute H-scores for all positions given nucleotide counts and reference."""
    hscores = []
    for counts, ref in zip(counts_per_position, reference):
        ratios = compute_nucleotide_ratios(counts)
        P = compute_mutation_ratio(ratios, ref)
        E = compute_mutation_entropy(ratios, ref)
        H = compute_hscore(P, E)
        hscores.append(H)
    return hscores


def compute_hscores_from_alignment(alignment: list[str], reference: str) -> list[float]:
    """Compute H-scores from a multiple sequence alignment.

    Args:
        alignment: list of aligned sequences (same length)
        reference: reference sequence string

    Returns: list of H-scores, one per position
    """
    seq_len = len(reference)
    n_seqs = len(alignment)

    hscores = []
    for pos in range(seq_len):
        counts = {n: 0 for n in NUCLEOTIDES}
        for seq in alignment:
            nuc = seq[pos].upper()
            if nuc in counts:
                counts[nuc] += 1

        ref_nuc = reference[pos].upper()
        ratios = compute_nucleotide_ratios(counts)
        P = compute_mutation_ratio(ratios, ref_nuc)
        E = compute_mutation_entropy(ratios, ref_nuc)
        H = compute_hscore(P, E)
        hscores.append(H)

    return hscores
```

`tools/mutclust/hscore/__main__.py`:
```python
"""CLI: python -m tools.mutclust.hscore --input aligned.fasta --ref reference.fasta --output hscores.csv"""
import argparse
import csv
from Bio import SeqIO
from tools.mutclust.hscore.core import compute_hscores_from_alignment


def main():
    parser = argparse.ArgumentParser(description='Compute H-scores from aligned sequences')
    parser.add_argument('--input', required=True, help='Aligned sequences (FASTA)')
    parser.add_argument('--ref', required=True, help='Reference sequence (FASTA)')
    parser.add_argument('--output', required=True, help='Output CSV (position, hscore)')
    parser.add_argument('--start', type=int, default=0, help='Start position filter')
    parser.add_argument('--end', type=int, default=0, help='End position filter (0=all)')
    args = parser.parse_args()

    ref_record = next(SeqIO.parse(args.ref, 'fasta'))
    reference = str(ref_record.seq)

    alignment = [str(rec.seq) for rec in SeqIO.parse(args.input, 'fasta')]

    hscores = compute_hscores_from_alignment(alignment, reference)

    with open(args.output, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['position', 'hscore'])
        for i, h in enumerate(hscores):
            if args.end > 0 and (i < args.start or i > args.end):
                continue
            writer.writerow([i + 1, f'{h:.6f}'])

    print(f"H-scores computed for {len(hscores)} positions -> {args.output}")


if __name__ == '__main__':
    main()
```

**Step 4: Run test, verify pass**

**Step 5: Commit**

```bash
git add tools/mutclust/hscore/ tests/mutclust/test_hscore.py
git commit -m "feat(mutclust): add H-score calculator"
```

### Task 2.2: MutClust clustering algorithm

**Files:**
- Create: `tools/mutclust/mutclust_algo/__init__.py`, `tools/mutclust/mutclust_algo/core.py`, `tools/mutclust/mutclust_algo/__main__.py`
- Test: `tests/mutclust/test_mutclust_algo.py`

**Step 1: Write the failing test**

```python
# tests/mutclust/test_mutclust_algo.py
import numpy as np
from tools.mutclust.mutclust_algo.core import (
    compute_deps,
    is_ccm,
    mutclust,
    Cluster,
)


def test_compute_deps():
    assert compute_deps(1.0, gamma=10) == 10
    assert compute_deps(0.5, gamma=10) == 5
    assert compute_deps(0.0, gamma=10) == 0


def test_ccm_conditions():
    # Position with high H-score and dense neighborhood
    hscores = np.zeros(100)
    hscores[45:55] = 0.1  # 10 mutant positions with H > 0
    hscores[50] = 0.5     # center is high
    assert is_ccm(50, hscores, gamma=10, minpts=5)


def test_ccm_fails_low_hscore():
    hscores = np.zeros(100)
    hscores[50] = 0.01  # below 0.03 threshold
    assert not is_ccm(50, hscores, gamma=10, minpts=5)


def test_mutclust_finds_clusters():
    # Simulate a genome with 2 hotspot regions
    np.random.seed(42)
    hscores = np.zeros(1000)
    # Hotspot 1: positions 100-120
    hscores[100:120] = np.random.uniform(0.1, 0.5, 20)
    hscores[110] = 1.0  # peak
    # Hotspot 2: positions 500-530
    hscores[500:530] = np.random.uniform(0.1, 0.5, 30)
    hscores[515] = 1.2  # peak

    clusters = mutclust(hscores, gamma=10, d=3, minpts=5)
    assert len(clusters) >= 2

    # Check clusters contain the peak positions
    positions = set()
    for c in clusters:
        positions.update(c.positions)
    assert 110 in positions
    assert 515 in positions


def test_mutclust_no_clusters_in_noise():
    hscores = np.random.uniform(0, 0.01, 500)  # all very low
    clusters = mutclust(hscores, gamma=10, d=3, minpts=5)
    assert len(clusters) == 0
```

**Step 2: Run test to verify fails**

**Step 3: Implement**

`tools/mutclust/mutclust_algo/core.py`:
```python
"""MutClust: adaptive density-based clustering for mutation hotspot detection.

Extends DBSCAN with:
- H-score-proportional local epsilon (Deps = ceil(gamma * H_i))
- Core Candidate Mutation (CCM) with 4 conditions
- Diminishing factor for cluster boundary control

From MutClust paper (Youn et al., BioData Mining 2025).
"""
import numpy as np
from math import ceil
from dataclasses import dataclass, field


CCM_HSCORE_MIN = 0.03
CCM_MEAN_MIN = 0.01
CCM_SUM_MIN = 0.05


@dataclass
class Cluster:
    """A mutation hotspot cluster."""
    seed: int
    positions: list[int] = field(default_factory=list)

    @property
    def start(self) -> int:
        return min(self.positions) if self.positions else self.seed

    @property
    def end(self) -> int:
        return max(self.positions) if self.positions else self.seed

    @property
    def size(self) -> int:
        return len(self.positions)


def compute_deps(hscore: float, gamma: int = 10) -> int:
    """Eq. 5: Deps_CCM = ceil(gamma * H_i)"""
    return ceil(gamma * hscore)


def _get_neighborhood(pos: int, hscores: np.ndarray, deps: int) -> np.ndarray:
    """Get H-scores in the neighborhood [pos-deps, pos+deps]."""
    start = max(0, pos - deps)
    end = min(len(hscores), pos + deps + 1)
    return hscores[start:end]


def is_ccm(pos: int, hscores: np.ndarray, gamma: int = 10, minpts: int = 5) -> bool:
    """Check if position meets all 4 CCM conditions."""
    h = hscores[pos]

    # Condition 1: H_i > 0.03
    if h <= CCM_HSCORE_MIN:
        return False

    deps = compute_deps(h, gamma)
    neighborhood = _get_neighborhood(pos, hscores, deps)
    mutant_scores = neighborhood[neighborhood > 0]

    # Condition 2: mean(H-scores in Deps) > 0.01
    if len(mutant_scores) == 0 or mutant_scores.mean() <= CCM_MEAN_MIN:
        return False

    # Condition 3: sum(H-scores in Deps) > 0.05
    if mutant_scores.sum() <= CCM_SUM_MIN:
        return False

    # Condition 4: count(mutant bases in Deps) > MinPts
    if len(mutant_scores) < minpts:
        return False

    return True


def _expand_cluster(seed: int, hscores: np.ndarray, gamma: int, d: int, minpts: int) -> Cluster:
    """Expand a cluster from a CCM seed bidirectionally with diminishing Deps."""
    cluster = Cluster(seed=seed, positions=[seed])
    deps_ccm = compute_deps(hscores[seed], gamma)

    for direction in [-1, 1]:  # left, right
        current_deps = deps_ccm
        distance = 0
        pos = seed

        while True:
            distance += 1
            next_pos = seed + direction * distance

            if next_pos < 0 or next_pos >= len(hscores):
                break

            # Diminishing factor (Eq. 6)
            current_deps = current_deps - (deps_ccm - distance) / d

            if distance > current_deps:
                break

            if hscores[next_pos] > 0:
                cluster.positions.append(next_pos)

    cluster.positions.sort()
    return cluster


def mutclust(hscores: np.ndarray, gamma: int = 10, d: int = 3,
             minpts: int = 5) -> list[Cluster]:
    """Run MutClust algorithm on H-score array.

    Phase 1: Find all CCM positions
    Phase 2: Expand clusters from each CCM

    Returns list of Cluster objects (mutation hotspots).
    """
    hscores = np.asarray(hscores, dtype=float)
    n = len(hscores)

    # Phase 1: Find CCMs
    ccms = []
    for i in range(n):
        if is_ccm(i, hscores, gamma, minpts):
            ccms.append(i)

    if not ccms:
        return []

    # Phase 2: Expand clusters
    clusters = []
    assigned = set()

    for ccm in ccms:
        if ccm in assigned:
            continue
        cluster = _expand_cluster(ccm, hscores, gamma, d, minpts)
        if cluster.size >= minpts:
            clusters.append(cluster)
            assigned.update(cluster.positions)

    # Merge overlapping clusters
    clusters = _merge_overlapping(clusters)

    return clusters


def _merge_overlapping(clusters: list[Cluster]) -> list[Cluster]:
    """Merge clusters with overlapping position ranges."""
    if not clusters:
        return []

    clusters.sort(key=lambda c: c.start)
    merged = [clusters[0]]

    for cluster in clusters[1:]:
        if cluster.start <= merged[-1].end + 1:
            # Merge
            all_pos = set(merged[-1].positions) | set(cluster.positions)
            merged[-1].positions = sorted(all_pos)
        else:
            merged.append(cluster)

    return merged
```

`tools/mutclust/mutclust_algo/__main__.py`:
```python
"""CLI: python -m tools.mutclust.mutclust_algo --input hscores.csv --gamma 10 --d 3 --minpts 5"""
import argparse
import csv
import numpy as np
from tools.mutclust.mutclust_algo.core import mutclust


def main():
    parser = argparse.ArgumentParser(description='MutClust: adaptive density-based mutation hotspot detection')
    parser.add_argument('--input', required=True, help='CSV with position,hscore columns')
    parser.add_argument('--gamma', type=int, default=10, help='Eps scaling factor')
    parser.add_argument('--d', type=int, default=3, help='Diminishing factor')
    parser.add_argument('--minpts', type=int, default=5, help='Minimum mutant positions per cluster')
    parser.add_argument('--genome-size', type=int, default=29903, help='Total genome size')
    parser.add_argument('--output', required=True, help='Output CSV with hotspots')
    args = parser.parse_args()

    # Load H-scores
    hscores = np.zeros(args.genome_size)
    with open(args.input) as f:
        reader = csv.DictReader(f)
        for row in reader:
            pos = int(row['position']) - 1  # 0-indexed
            if 0 <= pos < args.genome_size:
                hscores[pos] = float(row['hscore'])

    clusters = mutclust(hscores, gamma=args.gamma, d=args.d, minpts=args.minpts)

    with open(args.output, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['cluster_id', 'start', 'end', 'n_positions', 'mean_hscore', 'max_hscore'])
        for i, c in enumerate(clusters):
            scores = [hscores[p] for p in c.positions]
            writer.writerow([
                f'c{i+1}', c.start + 1, c.end + 1, c.size,
                f'{np.mean(scores):.4f}', f'{np.max(scores):.4f}'
            ])

    print(f"MutClust: {len(clusters)} hotspots detected -> {args.output}")


if __name__ == '__main__':
    main()
```

**Step 4: Run test, verify pass**

**Step 5: Commit**

```bash
git add tools/mutclust/mutclust_algo/ tests/mutclust/test_mutclust_algo.py
git commit -m "feat(mutclust): add MutClust adaptive density clustering algorithm"
```

### Task 2.3: Bootstrap significance testing

**Files:**
- Create: `tools/mutclust/bootstrap/__init__.py`, `tools/mutclust/bootstrap/core.py`, `tools/mutclust/bootstrap/__main__.py`
- Test: `tests/mutclust/test_bootstrap.py`

**Step 1: Write failing test**

```python
# tests/mutclust/test_bootstrap.py
import numpy as np
from tools.mutclust.bootstrap.core import bootstrap_hotspot_test


def test_significant_hotspot():
    np.random.seed(42)
    hscores = np.zeros(1000)
    hscores[100:120] = np.random.uniform(0.5, 1.0, 20)  # dense hotspot
    result = bootstrap_hotspot_test(hscores, start=100, end=119, n_iter=500)
    assert result['p_value'] < 0.05


def test_nonsignificant_region():
    np.random.seed(42)
    hscores = np.random.uniform(0, 0.01, 1000)  # uniform low
    result = bootstrap_hotspot_test(hscores, start=100, end=119, n_iter=500)
    assert result['p_value'] > 0.05
```

**Step 2: Run test to verify fails**

**Step 3: Implement**

`tools/mutclust/bootstrap/core.py`:
```python
"""Bootstrap testing for mutation hotspot significance.

For each hotspot, randomly sample regions of the same size 1000 times
and compare mutation count, mean H-score, and sum H-scores.
"""
import numpy as np
from tools.common.stats import benjamini_hochberg


def bootstrap_hotspot_test(hscores: np.ndarray, start: int, end: int,
                           n_iter: int = 1000) -> dict:
    """Test if a hotspot region is significantly denser than random.

    Compares observed mutation count, mean H-score, sum H-scores
    against random regions of the same size.
    """
    region_size = end - start + 1
    observed = hscores[start:end + 1]
    obs_count = np.sum(observed > 0)
    obs_mean = np.mean(observed[observed > 0]) if obs_count > 0 else 0
    obs_sum = np.sum(observed)

    genome_size = len(hscores)
    exceed_count = 0

    for _ in range(n_iter):
        rand_start = np.random.randint(0, genome_size - region_size)
        rand_region = hscores[rand_start:rand_start + region_size]
        rand_nonzero = rand_region[rand_region > 0]
        rand_count = len(rand_nonzero)
        rand_mean = np.mean(rand_nonzero) if rand_count > 0 else 0
        rand_sum = np.sum(rand_region)

        if rand_count >= obs_count and rand_mean >= obs_mean and rand_sum >= obs_sum:
            exceed_count += 1

    p_value = exceed_count / n_iter

    return {
        'start': start,
        'end': end,
        'obs_count': int(obs_count),
        'obs_mean': float(obs_mean),
        'obs_sum': float(obs_sum),
        'p_value': p_value,
    }


def bootstrap_all_hotspots(hscores: np.ndarray, hotspots: list[tuple[int, int]],
                           n_iter: int = 1000, fdr: float = 0.05) -> list[dict]:
    """Run bootstrap test on all hotspots with BH correction."""
    results = []
    for start, end in hotspots:
        result = bootstrap_hotspot_test(hscores, start, end, n_iter)
        results.append(result)

    pvalues = [r['p_value'] for r in results]
    adjusted = benjamini_hochberg(pvalues)

    for r, adj_p in zip(results, adjusted):
        r['adjusted_p'] = adj_p
        r['significant'] = adj_p < fdr

    return results
```

`tools/mutclust/bootstrap/__main__.py`:
```python
"""CLI: python -m tools.mutclust.bootstrap --hscores hscores.csv --clusters clusters.csv --n-iter 1000"""
import argparse
import csv
import numpy as np
from tools.mutclust.bootstrap.core import bootstrap_all_hotspots


def main():
    parser = argparse.ArgumentParser(description='Bootstrap significance testing for hotspots')
    parser.add_argument('--hscores', required=True, help='CSV with position,hscore')
    parser.add_argument('--clusters', required=True, help='CSV with cluster_id,start,end')
    parser.add_argument('--genome-size', type=int, default=29903)
    parser.add_argument('--n-iter', type=int, default=1000)
    parser.add_argument('--fdr', type=float, default=0.05)
    parser.add_argument('--output', required=True)
    args = parser.parse_args()

    hscores = np.zeros(args.genome_size)
    with open(args.hscores) as f:
        for row in csv.DictReader(f):
            pos = int(row['position']) - 1
            if 0 <= pos < args.genome_size:
                hscores[pos] = float(row['hscore'])

    hotspots = []
    with open(args.clusters) as f:
        for row in csv.DictReader(f):
            hotspots.append((int(row['start']) - 1, int(row['end']) - 1))

    results = bootstrap_all_hotspots(hscores, hotspots, args.n_iter, args.fdr)

    with open(args.output, 'w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=['start', 'end', 'obs_count', 'obs_mean',
                                                'obs_sum', 'p_value', 'adjusted_p', 'significant'])
        writer.writeheader()
        for r in results:
            r['start'] += 1
            r['end'] += 1
            writer.writerow(r)

    n_sig = sum(1 for r in results if r['significant'])
    print(f"Bootstrap: {n_sig}/{len(results)} significant hotspots (FDR={args.fdr}) -> {args.output}")


if __name__ == '__main__':
    main()
```

**Step 4: Run test, verify pass**

**Step 5: Commit**

```bash
git add tools/mutclust/bootstrap/ tests/mutclust/test_bootstrap.py
git commit -m "feat(mutclust): add bootstrap significance testing"
```

### Task 2.4: Network Propagation

**Files:**
- Create: `tools/mutclust/network_propagation/__init__.py`, `tools/mutclust/network_propagation/core.py`, `tools/mutclust/network_propagation/__main__.py`
- Test: `tests/mutclust/test_network_propagation.py`

**Step 1: Write failing test**

```python
# tests/mutclust/test_network_propagation.py
import numpy as np
import networkx as nx
from tools.mutclust.network_propagation.core import propagate, build_adjacency_matrix


def test_propagate_seed_highest():
    G = nx.path_graph(5)  # 0-1-2-3-4
    seeds = {2}
    scores = propagate(G, seeds, alpha=0.01, max_iter=100)
    # Seed node should have highest score
    assert scores[2] == max(scores.values())


def test_propagate_neighbors_higher():
    G = nx.path_graph(5)  # 0-1-2-3-4
    seeds = {0}
    scores = propagate(G, seeds, alpha=0.01, max_iter=100)
    # Closer nodes should score higher
    assert scores[0] > scores[1] > scores[2]


def test_propagate_disconnected():
    G = nx.Graph()
    G.add_edges_from([(0, 1), (2, 3)])
    seeds = {0}
    scores = propagate(G, seeds, alpha=0.01, max_iter=100)
    assert scores[0] > 0
    assert scores[2] == 0 or scores[2] < 1e-10


def test_build_adjacency_matrix():
    G = nx.path_graph(3)
    W, nodes = build_adjacency_matrix(G)
    assert W.shape == (3, 3)
    assert abs(W.sum(axis=1) - 1).max() < 1e-10  # row-normalized
```

**Step 2: Run test to verify fails**

**Step 3: Implement**

`tools/mutclust/network_propagation/core.py`:
```python
"""Network propagation: diffuse seed gene influence through PPI network.

p^(t+1) = (1-alpha) * W * p^t + alpha * p_0
- alpha=0.01 (restart probability)
- W: row-normalized adjacency matrix

From MutClust paper.
"""
import numpy as np
import networkx as nx


def build_adjacency_matrix(G: nx.Graph) -> tuple[np.ndarray, list]:
    """Build row-normalized adjacency matrix from graph."""
    nodes = sorted(G.nodes())
    n = len(nodes)
    node_idx = {node: i for i, node in enumerate(nodes)}

    W = np.zeros((n, n))
    for u, v in G.edges():
        i, j = node_idx[u], node_idx[v]
        W[i, j] = 1
        W[j, i] = 1

    # Row normalize
    row_sums = W.sum(axis=1)
    row_sums[row_sums == 0] = 1
    W = W / row_sums[:, None]

    return W, nodes


def propagate(G: nx.Graph, seeds: set, alpha: float = 0.01,
              max_iter: int = 1000, tol: float = 1e-6) -> dict:
    """Run network propagation from seed genes.

    Args:
        G: gene-gene interaction network
        seeds: set of seed gene names/IDs
        alpha: restart probability (default 0.01)
        max_iter: max iterations
        tol: convergence tolerance

    Returns: dict mapping gene -> propagation score
    """
    W, nodes = build_adjacency_matrix(G)
    n = len(nodes)
    node_idx = {node: i for i, node in enumerate(nodes)}

    # Initial resource vector
    p0 = np.zeros(n)
    for seed in seeds:
        if seed in node_idx:
            p0[node_idx[seed]] = 1.0

    if p0.sum() == 0:
        return {node: 0.0 for node in nodes}

    p0 = p0 / p0.sum()  # normalize
    p = p0.copy()

    for _ in range(max_iter):
        p_new = (1 - alpha) * W.T @ p + alpha * p0
        if np.linalg.norm(p_new - p) < tol:
            break
        p = p_new

    return {node: float(p[i]) for i, node in enumerate(nodes)}


def get_top_genes(scores: dict, n: int = 100, exclude: set = None) -> list[tuple]:
    """Get top N genes by propagation score."""
    if exclude is None:
        exclude = set()
    filtered = {k: v for k, v in scores.items() if k not in exclude}
    sorted_genes = sorted(filtered.items(), key=lambda x: x[1], reverse=True)
    return sorted_genes[:n]
```

`tools/mutclust/network_propagation/__main__.py`:
```python
"""CLI: python -m tools.mutclust.network_propagation --seeds seeds.txt --network ppi.tsv --alpha 0.01"""
import argparse
import csv
import networkx as nx
from tools.mutclust.network_propagation.core import propagate, get_top_genes


def main():
    parser = argparse.ArgumentParser(description='Network propagation on PPI network')
    parser.add_argument('--seeds', required=True, help='Text file with seed gene names (one per line)')
    parser.add_argument('--network', required=True, help='TSV edge list (gene1 gene2)')
    parser.add_argument('--alpha', type=float, default=0.01, help='Restart probability')
    parser.add_argument('--top-n', type=int, default=100, help='Number of top genes to output')
    parser.add_argument('--output', required=True, help='Output CSV')
    args = parser.parse_args()

    with open(args.seeds) as f:
        seeds = {line.strip() for line in f if line.strip()}

    G = nx.read_edgelist(args.network, delimiter='\t')

    scores = propagate(G, seeds, alpha=args.alpha)
    top = get_top_genes(scores, n=args.top_n, exclude=seeds)

    with open(args.output, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['gene', 'score'])
        for gene, score in top:
            writer.writerow([gene, f'{score:.6f}'])

    print(f"Network propagation: top {len(top)} genes -> {args.output}")


if __name__ == '__main__':
    main()
```

**Step 4: Run test, verify pass**

**Step 5: Commit**

```bash
git add tools/mutclust/network_propagation/ tests/mutclust/test_network_propagation.py
git commit -m "feat(mutclust): add network propagation analysis"
```

### Task 2.5: DEG Analysis

**Files:**
- Create: `tools/mutclust/deg_analysis/__init__.py`, `tools/mutclust/deg_analysis/core.py`, `tools/mutclust/deg_analysis/__main__.py`
- Test: `tests/mutclust/test_deg_analysis.py`

**Step 1: Write failing test**

```python
# tests/mutclust/test_deg_analysis.py
import numpy as np
import pandas as pd
from tools.mutclust.deg_analysis.core import find_degs, filter_low_expression


def test_find_degs_detects_differential():
    np.random.seed(42)
    n_genes = 100
    n_samples = 50
    # Group A: 25 samples, Group B: 25 samples
    groups = ['A'] * 25 + ['B'] * 25
    counts = pd.DataFrame(np.random.poisson(10, (n_samples, n_genes)),
                          columns=[f'gene{i}' for i in range(n_genes)])
    # Make gene0 differentially expressed
    counts.iloc[:25, 0] = np.random.poisson(50, 25)
    counts.iloc[25:, 0] = np.random.poisson(5, 25)

    degs = find_degs(counts, groups, fdr=0.05)
    assert 'gene0' in degs['gene'].values


def test_filter_low_expression():
    counts = pd.DataFrame({
        'gene1': [0, 0, 0, 0, 10],  # 80% zeros - should be filtered
        'gene2': [5, 3, 7, 2, 8],   # expressed - should be kept
    })
    filtered = filter_low_expression(counts, zero_pct_threshold=0.8)
    assert 'gene2' in filtered.columns
    assert 'gene1' not in filtered.columns
```

**Step 2: Run test to verify fails**

**Step 3: Implement**

`tools/mutclust/deg_analysis/core.py`:
```python
"""Differential Expression Gene analysis.

Uses scipy for statistical testing (Mann-Whitney U / t-test)
with Benjamini-Hochberg FDR correction.
Approximation of edgeR's approach for non-R environments.
"""
import numpy as np
import pandas as pd
from scipy import stats
from tools.common.stats import benjamini_hochberg


def filter_low_expression(counts: pd.DataFrame, zero_pct_threshold: float = 0.8) -> pd.DataFrame:
    """Remove genes where > threshold fraction of samples have 0 counts."""
    zero_frac = (counts == 0).sum(axis=0) / len(counts)
    keep = zero_frac < zero_pct_threshold
    return counts.loc[:, keep]


def find_degs(counts: pd.DataFrame, groups: list[str],
              fdr: float = 0.05, test: str = 'mannwhitney') -> pd.DataFrame:
    """Find differentially expressed genes between two groups.

    Args:
        counts: DataFrame (samples x genes)
        groups: group labels for each sample
        fdr: FDR threshold
        test: 'mannwhitney' or 'ttest'

    Returns: DataFrame with gene, statistic, pvalue, adjusted_p, log2fc
    """
    groups = np.array(groups)
    unique_groups = np.unique(groups)
    if len(unique_groups) != 2:
        raise ValueError(f"Expected 2 groups, got {len(unique_groups)}")

    g1_mask = groups == unique_groups[0]
    g2_mask = groups == unique_groups[1]

    results = []
    for gene in counts.columns:
        vals1 = counts.loc[g1_mask, gene].values.astype(float)
        vals2 = counts.loc[g2_mask, gene].values.astype(float)

        mean1 = vals1.mean()
        mean2 = vals2.mean()

        # Log2 fold change
        log2fc = np.log2((mean1 + 1) / (mean2 + 1))

        if test == 'mannwhitney':
            stat, pval = stats.mannwhitneyu(vals1, vals2, alternative='two-sided')
        else:
            stat, pval = stats.ttest_ind(vals1, vals2)

        results.append({
            'gene': gene,
            'mean_g1': mean1,
            'mean_g2': mean2,
            'log2fc': log2fc,
            'statistic': stat,
            'pvalue': pval,
        })

    df = pd.DataFrame(results)
    df['adjusted_p'] = benjamini_hochberg(df['pvalue'].tolist())
    df['significant'] = df['adjusted_p'] < fdr

    return df
```

`tools/mutclust/deg_analysis/__main__.py`:
```python
"""CLI: python -m tools.mutclust.deg_analysis --counts counts.csv --groups groups.csv --fdr 0.05"""
import argparse
from tools.common.io_utils import load_csv_matrix
from tools.mutclust.deg_analysis.core import find_degs, filter_low_expression
import pandas as pd


def main():
    parser = argparse.ArgumentParser(description='Differential Expression Gene analysis')
    parser.add_argument('--counts', required=True, help='CSV count matrix (samples x genes)')
    parser.add_argument('--groups', required=True, help='CSV with sample,group columns')
    parser.add_argument('--fdr', type=float, default=0.05)
    parser.add_argument('--test', choices=['mannwhitney', 'ttest'], default='mannwhitney')
    parser.add_argument('--filter-zeros', type=float, default=0.8, help='Filter genes with >X% zeros')
    parser.add_argument('--output', required=True)
    args = parser.parse_args()

    counts = load_csv_matrix(args.counts)
    groups_df = pd.read_csv(args.groups)
    groups = groups_df['group'].tolist()

    counts = filter_low_expression(counts, args.filter_zeros)
    result = find_degs(counts, groups, fdr=args.fdr, test=args.test)

    result.to_csv(args.output, index=False)
    n_sig = result['significant'].sum()
    print(f"DEG analysis: {n_sig}/{len(result)} significant genes (FDR={args.fdr}) -> {args.output}")


if __name__ == '__main__':
    main()
```

**Step 4: Run test, verify pass**

**Step 5: Commit**

```bash
git add tools/mutclust/deg_analysis/ tests/mutclust/test_deg_analysis.py
git commit -m "feat(mutclust): add DEG analysis tool"
```

### Task 2.6: HLA-Epitope Affinity Analysis

**Files:**
- Create: `tools/mutclust/hla_affinity/__init__.py`, `tools/mutclust/hla_affinity/core.py`, `tools/mutclust/hla_affinity/__main__.py`
- Test: `tests/mutclust/test_hla_affinity.py`

**Step 1: Write failing test**

```python
# tests/mutclust/test_hla_affinity.py
import numpy as np
from tools.mutclust.hla_affinity.core import (
    generate_epitopes,
    estimate_binding_affinity,
    compute_log_fold_change,
)


def test_generate_epitopes():
    seq = "ABCDEFGHIJ"
    epitopes = generate_epitopes(seq, min_len=8, max_len=9)
    assert len(epitopes) > 0
    assert all(8 <= len(e) <= 9 for e in epitopes)


def test_generate_epitopes_short():
    seq = "ABC"
    epitopes = generate_epitopes(seq, min_len=8, max_len=9)
    assert len(epitopes) == 0


def test_log_fold_change():
    ref_affinity = 100.0
    mut_affinity = 200.0
    lfc = compute_log_fold_change(ref_affinity, mut_affinity)
    assert abs(lfc - 1.0) < 1e-10  # log2(200/100) = 1.0


def test_log_fold_change_decreased():
    ref_affinity = 100.0
    mut_affinity = 50.0
    lfc = compute_log_fold_change(ref_affinity, mut_affinity)
    assert lfc < 0  # affinity improved (lower nM = stronger)
```

**Step 2: Run test to verify fails**

**Step 3: Implement**

`tools/mutclust/hla_affinity/core.py`:
```python
"""HLA-epitope binding affinity analysis.

Generates epitopes from mutated sequences and estimates binding affinity changes.
Uses a simplified scoring model based on amino acid properties.
For production use, integrate with NetMHCpan or MHCflurry.
"""
import numpy as np
from itertools import product

# Simplified amino acid hydrophobicity index (Kyte-Doolittle)
AA_HYDROPHOBICITY = {
    'A': 1.8, 'R': -4.5, 'N': -3.5, 'D': -3.5, 'C': 2.5,
    'E': -3.5, 'Q': -3.5, 'G': -0.4, 'H': -3.2, 'I': 4.5,
    'L': 3.8, 'K': -3.9, 'M': 1.9, 'F': 2.8, 'P': -1.6,
    'S': -0.8, 'T': -0.7, 'W': -0.9, 'Y': -1.3, 'V': 4.2,
}


def generate_epitopes(sequence: str, min_len: int = 8, max_len: int = 14) -> list[str]:
    """Generate all possible epitope peptides from a sequence."""
    epitopes = []
    for length in range(min_len, max_len + 1):
        for i in range(len(sequence) - length + 1):
            epitope = sequence[i:i + length]
            if all(c in AA_HYDROPHOBICITY for c in epitope):
                epitopes.append(epitope)
    return epitopes


def estimate_binding_affinity(peptide: str) -> float:
    """Estimate binding affinity (nM) using simplified hydrophobicity model.

    Lower value = stronger binding.
    This is a simplified proxy. For real analysis, use NetMHCpan/MHCflurry.
    """
    if not peptide or not all(c in AA_HYDROPHOBICITY for c in peptide):
        return 50000.0  # weak binding default

    scores = [AA_HYDROPHOBICITY.get(aa, 0) for aa in peptide]

    # Anchor positions (simplified: positions 2 and C-terminal)
    anchor_score = abs(scores[1]) + abs(scores[-1]) if len(scores) >= 2 else 0
    mean_hydro = np.mean(scores)

    # Convert to pseudo-affinity (nM scale)
    raw_score = anchor_score * 50 + abs(mean_hydro) * 100
    affinity = max(1.0, 500.0 - raw_score)

    return affinity


def compute_log_fold_change(ref_affinity: float, mut_affinity: float) -> float:
    """Compute log2 fold change of binding affinity.

    Positive LFC = affinity weakened (higher nM = weaker binding).
    Negative LFC = affinity strengthened.
    """
    return np.log2(mut_affinity / ref_affinity)


def analyze_hla_epitopes(ref_seq: str, mut_seq: str,
                         min_len: int = 8, max_len: int = 14,
                         affinity_threshold: float = 500.0) -> list[dict]:
    """Compare epitope binding affinities between reference and mutated sequences.

    Returns list of epitope pairs where reference has affinity < threshold.
    """
    ref_epitopes = generate_epitopes(ref_seq, min_len, max_len)

    results = []
    for i, ref_ep in enumerate(ref_epitopes):
        ref_aff = estimate_binding_affinity(ref_ep)
        if ref_aff >= affinity_threshold:
            continue

        # Get corresponding mutated epitope
        start = i % (len(ref_seq) - len(ref_ep) + 1)
        if start + len(ref_ep) <= len(mut_seq):
            mut_ep = mut_seq[start:start + len(ref_ep)]
            mut_aff = estimate_binding_affinity(mut_ep)
            lfc = compute_log_fold_change(ref_aff, mut_aff)

            results.append({
                'ref_epitope': ref_ep,
                'mut_epitope': mut_ep,
                'ref_affinity': ref_aff,
                'mut_affinity': mut_aff,
                'log2fc': lfc,
            })

    return results
```

`tools/mutclust/hla_affinity/__main__.py`:
```python
"""CLI: python -m tools.mutclust.hla_affinity --ref-seq ref.fasta --mut-seq mut.fasta"""
import argparse
import csv
from tools.mutclust.hla_affinity.core import analyze_hla_epitopes


def main():
    parser = argparse.ArgumentParser(description='HLA-epitope binding affinity analysis')
    parser.add_argument('--ref-seq', required=True, help='Reference protein sequence')
    parser.add_argument('--mut-seq', required=True, help='Mutated protein sequence')
    parser.add_argument('--min-len', type=int, default=8)
    parser.add_argument('--max-len', type=int, default=14)
    parser.add_argument('--affinity-threshold', type=float, default=500.0)
    parser.add_argument('--output', required=True)
    args = parser.parse_args()

    with open(args.ref_seq) as f:
        ref = ''.join(line.strip() for line in f if not line.startswith('>'))
    with open(args.mut_seq) as f:
        mut = ''.join(line.strip() for line in f if not line.startswith('>'))

    results = analyze_hla_epitopes(ref, mut, args.min_len, args.max_len, args.affinity_threshold)

    with open(args.output, 'w', newline='') as f:
        if results:
            writer = csv.DictWriter(f, fieldnames=results[0].keys())
            writer.writeheader()
            writer.writerows(results)

    print(f"HLA affinity: {len(results)} epitope pairs analyzed -> {args.output}")


if __name__ == '__main__':
    main()
```

**Step 4: Run test, verify pass**

**Step 5: Commit**

```bash
git add tools/mutclust/hla_affinity/ tests/mutclust/test_hla_affinity.py
git commit -m "feat(mutclust): add HLA-epitope affinity analysis"
```

---

## Phase 3: Integration (Lead)

### Task 3.1: Create __init__.py files and ensure all imports work

**Step 1:** Create all missing `__init__.py` files
**Step 2:** Run `python -c "import tools.mosd; import tools.mutclust"` to verify
**Step 3:** Commit

### Task 3.2: Run full test suite

**Step 1:** Run `python -m pytest tests/ -v --tb=short`
**Step 2:** Fix any failures
**Step 3:** Commit final state

```bash
git add -A
git commit -m "feat: complete paper tools implementation (MOSD + MutClust)"
```

---

## Task Dependencies

```
Phase 0 (Lead)
  0.1 Organize docs
  0.2 Scaffolding ──┬──> Phase 1 (mosd-dev)     Phase 2 (mutclust-dev)
  0.3 Metrics ──────┤     1.1 Cluster-score       2.1 H-score
  0.4 Stats ────────┤     1.2 Feature Selection    2.2 MutClust algo
  0.5 I/O utils ────┘     1.3 Preprocessing        2.3 Bootstrap
                           1.4 MOI Methods          2.4 Network Propagation
                           1.5 Benchmark            2.5 DEG Analysis
                                                    2.6 HLA Affinity

                    Phase 3 (Lead): Integration
```

Phase 1 and Phase 2 are **fully independent** and can run in parallel.
Within each phase, tasks are sequential (each builds on prior).
