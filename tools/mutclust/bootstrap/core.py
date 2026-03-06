"""Bootstrap testing for mutation hotspot significance."""
import numpy as np
from tools.common.stats import benjamini_hochberg

def bootstrap_hotspot_test(hscores, start, end, n_iter=1000, seed=None):
    rng = np.random.default_rng(seed)
    region_size = end - start + 1
    observed = hscores[start:end + 1]
    obs_count = int(np.sum(observed > 0))
    obs_mean = float(np.mean(observed[observed > 0])) if obs_count > 0 else 0.0
    obs_sum = float(np.sum(observed))
    genome_size = len(hscores)
    rand_starts = rng.integers(0, genome_size - region_size, size=n_iter)
    exceed_count = 0
    for rs in rand_starts:
        rand_region = hscores[rs:rs + region_size]
        rand_nonzero = rand_region[rand_region > 0]
        rand_count = len(rand_nonzero)
        rand_mean = float(np.mean(rand_nonzero)) if rand_count > 0 else 0.0
        rand_sum = float(np.sum(rand_region))
        if rand_count >= obs_count and rand_mean >= obs_mean and rand_sum >= obs_sum:
            exceed_count += 1
    return {'start': start, 'end': end, 'obs_count': obs_count,
            'obs_mean': obs_mean, 'obs_sum': obs_sum,
            'p_value': exceed_count / n_iter}

def bootstrap_all_hotspots(hscores, hotspots, n_iter=1000, fdr=0.05, seed=None):
    results = [bootstrap_hotspot_test(hscores, s, e, n_iter, seed=seed) for s, e in hotspots]
    pvalues = [r['p_value'] for r in results]
    adjusted = benjamini_hochberg(pvalues)
    for r, adj_p in zip(results, adjusted):
        r['adjusted_p'] = adj_p
        r['significant'] = adj_p < fdr
    return results
