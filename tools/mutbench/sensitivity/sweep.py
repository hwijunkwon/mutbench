"""Parameter sensitivity sweep for MutClust benchmark."""
import numpy as np
from itertools import product
from tools.mutclust.mutclust_algo.core import mutclust


class ParameterSweep:
    def __init__(self,
                 gamma_values=None,
                 d_values=None,
                 minpts_values=None):
        self.gamma_values = gamma_values or [5, 10, 15, 20]
        self.d_values = d_values or [2, 3, 4, 5]
        self.minpts_values = minpts_values or [3, 5, 7, 10]

    def get_param_combinations(self):
        return list(product(self.gamma_values, self.d_values, self.minpts_values))

    def run(self, hscores, evaluate_fn):
        """Run sweep over all parameter combinations.

        Args:
            hscores: array of H-scores
            evaluate_fn: callable(detected_clusters) -> dict of metrics

        Returns:
            list of dicts with params and metrics
        """
        hscores = np.asarray(hscores, dtype=float)
        results = []
        for gamma, d, minpts in self.get_param_combinations():
            clusters = mutclust(hscores, gamma=gamma, d=d, minpts=minpts)
            detected = [{'start': c.start, 'end': c.end, 'positions': list(c.positions)}
                       for c in clusters]
            metrics = evaluate_fn(detected)
            results.append({
                'gamma': gamma,
                'd': d,
                'minpts': minpts,
                **metrics,
            })
        return results

    def results_to_dataframe(self, results):
        """Convert results list to pandas DataFrame."""
        import pandas as pd
        return pd.DataFrame(results)
