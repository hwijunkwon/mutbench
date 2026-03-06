import pandas as pd
import numpy as np
from tools.mutbench.ground_truth.dms_loader import (
    load_dms_fitness, dms_to_position_scores, get_functional_positions
)


def test_load_dms_fitness_columns(tmp_path):
    mock_data = pd.DataFrame({
        'gene': ['S', 'S', 'S'],
        'aa_site': [484, 484, 501],
        'mutant_aa': ['K', 'R', 'Y'],
        'fitness': [-0.5, -0.3, -1.2],
    })
    path = str(tmp_path / 'test_dms.csv')
    mock_data.to_csv(path, index=False)
    df = load_dms_fitness(path)
    assert 'gene' in df.columns
    assert 'fitness' in df.columns


def test_dms_to_position_scores():
    df = pd.DataFrame({
        'gene': ['S', 'S', 'S', 'S'],
        'aa_site': [484, 484, 501, 501],
        'mutant_aa': ['K', 'R', 'Y', 'H'],
        'fitness': [-0.5, -0.3, -1.2, -0.1],
    })
    scores = dms_to_position_scores(df, gene='S')
    assert 484 in scores
    assert 501 in scores
    assert abs(scores[484] - 0.4) < 1e-10


def test_get_functional_positions():
    scores = {100: 0.1, 200: 0.8, 300: 0.05, 400: 1.5}
    func_pos = get_functional_positions(scores, threshold_percentile=50)
    assert 400 in func_pos
    assert 200 in func_pos
    assert 100 not in func_pos
