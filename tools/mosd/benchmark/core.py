"""Benchmark tests for multi-omics integration methods."""
import numpy as np
import pandas as pd
from sklearn.cluster import KMeans
from tools.common.metrics import cluster_score
from tools.mosd.moi_methods.core import METHODS


def _run_method(method: str, omics_list: list[pd.DataFrame], n_clusters: int) -> np.ndarray:
    """Run a clustering method and return labels."""
    return METHODS[method](omics_list, n_clusters=n_clusters)


def sample_size_test(
    data: pd.DataFrame,
    true_labels: np.ndarray,
    sizes: list[int],
    repeats: int = 5,
    method: str = 'CC',
    n_clusters: int = 3,
) -> pd.DataFrame:
    """Test clustering performance across different sample sizes.

    Args:
        data: Feature matrix (samples x features).
        true_labels: Ground-truth cluster labels (length == n_samples).
        sizes: List of sample sizes to test.
        repeats: Number of random subsampling repeats per size.
        method: MOI method name (key in METHODS).
        n_clusters: Number of clusters.

    Returns:
        DataFrame with columns [sample_size, repeat, cluster_score].
    """
    records = []
    true_labels = np.asarray(true_labels)
    for size in sizes:
        for rep in range(repeats):
            idx = np.random.choice(len(data), size=min(size, len(data)), replace=False)
            sub = data.iloc[idx].reset_index(drop=True)
            sub_true = true_labels[idx]
            # Wrap as single-omic list
            pred = _run_method(method, [sub], n_clusters=n_clusters)
            score = cluster_score(sub_true, pred)
            records.append({'sample_size': size, 'repeat': rep, 'cluster_score': score})
    return pd.DataFrame(records)


def feature_selection_test(
    data: pd.DataFrame,
    true_labels: np.ndarray,
    top_pcts: list[float] = None,
    repeats: int = 5,
    method: str = 'CC',
    n_clusters: int = 3,
) -> pd.DataFrame:
    """Test clustering performance across different feature selection percentages.

    Args:
        data: Feature matrix (samples x features).
        true_labels: Ground-truth cluster labels.
        top_pcts: List of top-percentage values for feature selection.
        repeats: Number of repeats.
        method: MOI method name.
        n_clusters: Number of clusters.

    Returns:
        DataFrame with columns [top_pct, repeat, cluster_score].
    """
    if top_pcts is None:
        top_pcts = [10, 20, 50, 100]
    from tools.mosd.feature_selection.core import select_features_chi2
    records = []
    true_labels = np.asarray(true_labels)
    # Shift data to non-negative for chi2
    data_nonneg = data - data.min() + 0.01
    for pct in top_pcts:
        for rep in range(repeats):
            selected = select_features_chi2(data_nonneg, true_labels, top_pct=pct)
            pred = _run_method(method, [selected], n_clusters=n_clusters)
            score = cluster_score(true_labels, pred)
            records.append({'top_pct': pct, 'repeat': rep, 'cluster_score': score})
    return pd.DataFrame(records)


def preprocessing_test(
    data: pd.DataFrame,
    true_labels: np.ndarray,
    strategies: list[str] = None,
    repeats: int = 5,
    method: str = 'CC',
    n_clusters: int = 3,
) -> pd.DataFrame:
    """Test clustering performance across different preprocessing strategies.

    Args:
        data: Feature matrix (samples x features), non-negative values.
        true_labels: Ground-truth cluster labels.
        strategies: List of preprocessing strategy names ('RAW', 'NORM').
        repeats: Number of repeats.
        method: MOI method name.
        n_clusters: Number of clusters.

    Returns:
        DataFrame with columns [strategy, repeat, cluster_score].
    """
    if strategies is None:
        strategies = ['RAW', 'NORM']
    from tools.mosd.preprocessing.core import preprocess_raw, preprocess_norm
    strategy_fn = {'RAW': preprocess_raw, 'NORM': preprocess_norm}
    records = []
    true_labels = np.asarray(true_labels)
    for strat in strategies:
        fn = strategy_fn[strat]
        for rep in range(repeats):
            processed = fn(data)
            pred = _run_method(method, [processed], n_clusters=n_clusters)
            score = cluster_score(true_labels, pred)
            records.append({'strategy': strat, 'repeat': rep, 'cluster_score': score})
    return pd.DataFrame(records)


def noise_test(
    data: pd.DataFrame,
    true_labels: np.ndarray,
    noise_levels: list[float] = None,
    repeats: int = 5,
    method: str = 'CC',
    n_clusters: int = 3,
) -> pd.DataFrame:
    """Test clustering robustness to Gaussian noise injection.

    Args:
        data: Feature matrix (samples x features).
        true_labels: Ground-truth cluster labels.
        noise_levels: List of noise standard deviations.
        repeats: Number of repeats per noise level.
        method: MOI method name.
        n_clusters: Number of clusters.

    Returns:
        DataFrame with columns [noise_level, repeat, cluster_score].
    """
    if noise_levels is None:
        noise_levels = [0.0, 0.1, 0.5, 1.0]
    records = []
    true_labels = np.asarray(true_labels)
    for noise in noise_levels:
        for rep in range(repeats):
            noisy = data + np.random.normal(0, noise, data.shape)
            noisy = pd.DataFrame(noisy, columns=data.columns, index=data.index)
            pred = _run_method(method, [noisy], n_clusters=n_clusters)
            score = cluster_score(true_labels, pred)
            records.append({'noise_level': noise, 'repeat': rep, 'cluster_score': score})
    return pd.DataFrame(records)


def balance_test(
    data: pd.DataFrame,
    true_labels: np.ndarray,
    imbalance_ratios: list[float] = None,
    repeats: int = 5,
    method: str = 'CC',
    n_clusters: int = 3,
) -> pd.DataFrame:
    """Test clustering performance across different class imbalance ratios.

    The ratio is the proportion of the minority class relative to the majority class.
    ratio=1.0 means balanced; ratio=0.1 means 10% minority vs 90% majority.

    Args:
        data: Feature matrix (samples x features).
        true_labels: Ground-truth cluster labels.
        imbalance_ratios: List of minority/majority size ratios.
        repeats: Number of repeats.
        method: MOI method name.
        n_clusters: Number of clusters.

    Returns:
        DataFrame with columns [imbalance_ratio, repeat, cluster_score].
    """
    if imbalance_ratios is None:
        imbalance_ratios = [1.0, 0.5, 0.25, 0.1]
    records = []
    true_labels = np.asarray(true_labels)
    classes = np.unique(true_labels)
    for ratio in imbalance_ratios:
        for rep in range(repeats):
            # Build imbalanced dataset
            indices = []
            class_sizes = []
            max_count = max(np.sum(true_labels == c) for c in classes)
            for i, c in enumerate(classes):
                class_idx = np.where(true_labels == c)[0]
                if i == 0:
                    # Majority class: keep all
                    size = len(class_idx)
                else:
                    # Minority classes: reduce by ratio
                    size = max(1, int(len(class_idx) * ratio))
                chosen = np.random.choice(class_idx, size=min(size, len(class_idx)), replace=False)
                indices.extend(chosen.tolist())
                class_sizes.append(len(chosen))
            indices = np.array(indices)
            sub = data.iloc[indices].reset_index(drop=True)
            sub_true = true_labels[indices]
            pred = _run_method(method, [sub], n_clusters=n_clusters)
            score = cluster_score(sub_true, pred)
            records.append({'imbalance_ratio': ratio, 'repeat': rep, 'cluster_score': score})
    return pd.DataFrame(records)


def subtype_combination_test(
    data: pd.DataFrame,
    true_labels: np.ndarray,
    k_values: list[int] = None,
    repeats: int = 5,
    method: str = 'CC',
) -> pd.DataFrame:
    """Test clustering performance across different numbers of subtypes (k).

    Args:
        data: Feature matrix (samples x features).
        true_labels: Ground-truth cluster labels (used for scoring; k values are varied).
        k_values: List of k (number of clusters) to test.
        repeats: Number of repeats per k.
        method: MOI method name.

    Returns:
        DataFrame with columns [k, repeat, cluster_score].
    """
    if k_values is None:
        k_values = [2, 3, 4, 5]
    records = []
    true_labels = np.asarray(true_labels)
    for k in k_values:
        for rep in range(repeats):
            pred = _run_method(method, [data], n_clusters=k)
            # Score against true labels with the true number of clusters
            score = cluster_score(true_labels, pred)
            records.append({'k': k, 'repeat': rep, 'cluster_score': score})
    return pd.DataFrame(records)


def omics_combination_test(
    omics_list: list[pd.DataFrame],
    true_labels: np.ndarray,
    repeats: int = 5,
    method: str = 'CC',
    n_clusters: int = 3,
) -> pd.DataFrame:
    """Test clustering performance across different combinations of omics data.

    Tests each single omic and all combinations up to the full set.

    Args:
        omics_list: List of DataFrames, each representing one omic type.
        true_labels: Ground-truth cluster labels.
        repeats: Number of repeats per combination.
        method: MOI method name.
        n_clusters: Number of clusters.

    Returns:
        DataFrame with columns [n_omics, omics_indices, repeat, cluster_score].
    """
    from itertools import combinations as itercombs
    records = []
    true_labels = np.asarray(true_labels)
    n = len(omics_list)
    for r in range(1, n + 1):
        for combo in itercombs(range(n), r):
            subset = [omics_list[i] for i in combo]
            for rep in range(repeats):
                pred = _run_method(method, subset, n_clusters=n_clusters)
                score = cluster_score(true_labels, pred)
                records.append({
                    'n_omics': r,
                    'omics_indices': str(list(combo)),
                    'repeat': rep,
                    'cluster_score': score,
                })
    return pd.DataFrame(records)


class BenchmarkRunner:
    """Runner that executes all benchmark tests and collects results.

    Args:
        method: MOI method name (key in METHODS).
        n_clusters: Number of clusters.
        repeats: Number of repeats per test condition.
    """

    def __init__(self, method: str = 'CC', n_clusters: int = 3, repeats: int = 5):
        self.method = method
        self.n_clusters = n_clusters
        self.repeats = repeats
        self.results = {}

    def run_sample_size(self, data: pd.DataFrame, true_labels: np.ndarray,
                        sizes: list[int] = None) -> pd.DataFrame:
        if sizes is None:
            sizes = [20, 40, 60, 80, 100]
        df = sample_size_test(data, true_labels, sizes=sizes, repeats=self.repeats,
                              method=self.method, n_clusters=self.n_clusters)
        self.results['sample_size'] = df
        return df

    def run_feature_selection(self, data: pd.DataFrame, true_labels: np.ndarray,
                              top_pcts: list[float] = None) -> pd.DataFrame:
        df = feature_selection_test(data, true_labels, top_pcts=top_pcts,
                                    repeats=self.repeats, method=self.method,
                                    n_clusters=self.n_clusters)
        self.results['feature_selection'] = df
        return df

    def run_preprocessing(self, data: pd.DataFrame, true_labels: np.ndarray,
                          strategies: list[str] = None) -> pd.DataFrame:
        df = preprocessing_test(data, true_labels, strategies=strategies,
                                repeats=self.repeats, method=self.method,
                                n_clusters=self.n_clusters)
        self.results['preprocessing'] = df
        return df

    def run_noise(self, data: pd.DataFrame, true_labels: np.ndarray,
                  noise_levels: list[float] = None) -> pd.DataFrame:
        df = noise_test(data, true_labels, noise_levels=noise_levels,
                        repeats=self.repeats, method=self.method,
                        n_clusters=self.n_clusters)
        self.results['noise'] = df
        return df

    def run_balance(self, data: pd.DataFrame, true_labels: np.ndarray,
                    imbalance_ratios: list[float] = None) -> pd.DataFrame:
        df = balance_test(data, true_labels, imbalance_ratios=imbalance_ratios,
                          repeats=self.repeats, method=self.method,
                          n_clusters=self.n_clusters)
        self.results['balance'] = df
        return df

    def run_subtype_combination(self, data: pd.DataFrame, true_labels: np.ndarray,
                                k_values: list[int] = None) -> pd.DataFrame:
        df = subtype_combination_test(data, true_labels, k_values=k_values,
                                      repeats=self.repeats, method=self.method)
        self.results['subtype_combination'] = df
        return df

    def run_omics_combination(self, omics_list: list[pd.DataFrame],
                              true_labels: np.ndarray) -> pd.DataFrame:
        df = omics_combination_test(omics_list, true_labels, repeats=self.repeats,
                                    method=self.method, n_clusters=self.n_clusters)
        self.results['omics_combination'] = df
        return df

    def summary(self) -> pd.DataFrame:
        """Return a summary DataFrame with mean cluster_score per test."""
        rows = []
        for test_name, df in self.results.items():
            rows.append({
                'test': test_name,
                'mean_cluster_score': df['cluster_score'].mean(),
                'std_cluster_score': df['cluster_score'].std(),
            })
        return pd.DataFrame(rows)
