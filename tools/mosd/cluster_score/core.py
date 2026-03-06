"""Cluster-score: (ARI + NMI + F-measure) / 3."""
from tools.common.metrics import adjusted_rand_index, normalized_mutual_info, f_measure_pairwise, cluster_score
from tools.common.io_utils import load_labels


def compute_cluster_score(true_path: str, pred_path: str,
                          sample_col: str = 'sample', label_col: str = 'label') -> dict:
    true = load_labels(true_path, sample_col, label_col)
    pred = load_labels(pred_path, sample_col, label_col)
    return {
        'ari': adjusted_rand_index(true, pred),
        'nmi': normalized_mutual_info(true, pred),
        'f_measure': f_measure_pairwise(true, pred),
        'cluster_score': cluster_score(true, pred),
    }
