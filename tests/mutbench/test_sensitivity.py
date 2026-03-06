import numpy as np
from tools.mutbench.sensitivity.sweep import ParameterSweep


def test_param_combinations():
    sweep = ParameterSweep()
    combos = sweep.get_param_combinations()
    assert len(combos) == 4 * 4 * 4  # 64 combinations


def test_sweep_runs():
    np.random.seed(42)
    hscores = np.zeros(500)
    hscores[100:120] = np.random.uniform(0.1, 0.5, 20)
    hscores[110] = 1.0

    def mock_evaluate(clusters):
        n_pos = sum(len(c['positions']) for c in clusters)
        return {'n_positions': n_pos, 'n_clusters': len(clusters)}

    sweep = ParameterSweep(
        gamma_values=[5, 10],
        d_values=[2, 3],
        minpts_values=[3, 5],
    )
    results = sweep.run(hscores, mock_evaluate)
    assert len(results) == 2 * 2 * 2  # 8 combinations
    assert 'gamma' in results[0]
    assert 'n_positions' in results[0]


def test_results_to_dataframe():
    results = [
        {'gamma': 10, 'd': 3, 'minpts': 5, 'f1': 0.5},
        {'gamma': 15, 'd': 3, 'minpts': 5, 'f1': 0.6},
    ]
    sweep = ParameterSweep()
    df = sweep.results_to_dataframe(results)
    assert len(df) == 2
    assert 'gamma' in df.columns
