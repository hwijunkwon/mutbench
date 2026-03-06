from tools.mutbench.config import BenchmarkConfig

def test_config_defaults():
    cfg = BenchmarkConfig()
    assert cfg.seed == 42
    assert cfg.n_bootstrap == 1000
    assert cfg.gamma == 10
    assert cfg.d == 3
    assert cfg.minpts == 5

def test_config_custom():
    cfg = BenchmarkConfig(seed=123, gamma=15)
    assert cfg.seed == 123
    assert cfg.gamma == 15

def test_config_reproducibility():
    cfg = BenchmarkConfig(seed=42)
    rng1 = cfg.get_rng()
    rng2 = cfg.get_rng()
    assert rng1.integers(0, 1000) == rng2.integers(0, 1000)
