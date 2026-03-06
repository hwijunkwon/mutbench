"""MutBench benchmark configuration."""
from dataclasses import dataclass
import numpy as np

@dataclass
class BenchmarkConfig:
    seed: int = 42
    n_bootstrap: int = 1000
    fdr: float = 0.05
    # MutClust defaults
    gamma: int = 10
    d: int = 3
    minpts: int = 5
    ccm_hscore_min: float = 0.03
    ccm_mean_min: float = 0.01
    ccm_sum_min: float = 0.05

    def get_rng(self) -> np.random.Generator:
        return np.random.default_rng(self.seed)
