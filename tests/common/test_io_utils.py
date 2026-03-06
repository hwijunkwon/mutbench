import tempfile, os
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
