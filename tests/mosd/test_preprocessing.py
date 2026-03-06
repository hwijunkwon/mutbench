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
    data = pd.DataFrame({'probe1': [1.0, 2.0], 'probe2': [3.0, 4.0], 'probe3': [5.0, 6.0]})
    gene_map = {'probe1': 'BRCA1', 'probe2': 'BRCA1', 'probe3': 'TP53'}
    result = preprocess_gl(data, gene_map)
    assert 'BRCA1' in result.columns
    assert 'TP53' in result.columns
    assert result.loc[0, 'BRCA1'] == 2.0
