"""MutClust: adaptive density-based clustering for mutation hotspot detection."""
import numpy as np
from math import ceil
from dataclasses import dataclass, field

CCM_HSCORE_MIN = 0.03
CCM_MEAN_MIN = 0.01
CCM_SUM_MIN = 0.05

@dataclass
class Cluster:
    seed: int
    positions: list[int] = field(default_factory=list)
    @property
    def start(self): return min(self.positions) if self.positions else self.seed
    @property
    def end(self): return max(self.positions) if self.positions else self.seed
    @property
    def size(self): return len(self.positions)

def compute_deps(hscore: float, gamma: int = 10) -> int:
    return ceil(gamma * hscore)

def _get_neighborhood(pos, hscores, deps):
    start = max(0, pos - deps)
    end = min(len(hscores), pos + deps + 1)
    return hscores[start:end]

def is_ccm(pos, hscores, gamma=10, minpts=5):
    h = hscores[pos]
    if h <= CCM_HSCORE_MIN:
        return False
    deps = compute_deps(h, gamma)
    neighborhood = _get_neighborhood(pos, hscores, deps)
    mutant_scores = neighborhood[neighborhood > 0]
    if len(mutant_scores) == 0 or mutant_scores.mean() <= CCM_MEAN_MIN:
        return False
    if mutant_scores.sum() <= CCM_SUM_MIN:
        return False
    if len(mutant_scores) < minpts:
        return False
    return True

def _expand_cluster(seed, hscores, gamma, d, minpts):
    cluster = Cluster(seed=seed, positions=[seed])
    deps_ccm = compute_deps(hscores[seed], gamma)
    for direction in [-1, 1]:
        current_deps = deps_ccm
        distance = 0
        while True:
            distance += 1
            next_pos = seed + direction * distance
            if next_pos < 0 or next_pos >= len(hscores):
                break
            current_deps = deps_ccm - distance / d
            if distance > current_deps:
                break
            if hscores[next_pos] > 0:
                cluster.positions.append(next_pos)
    cluster.positions.sort()
    return cluster

def _merge_overlapping(clusters):
    if not clusters:
        return []
    clusters.sort(key=lambda c: c.start)
    merged = [clusters[0]]
    for cluster in clusters[1:]:
        if cluster.start <= merged[-1].end + 1:
            all_pos = set(merged[-1].positions) | set(cluster.positions)
            merged[-1].positions = sorted(all_pos)
        else:
            merged.append(cluster)
    return merged

def mutclust(hscores, gamma=10, d=3, minpts=5):
    hscores = np.asarray(hscores, dtype=float)
    n = len(hscores)
    ccms = [i for i in range(n) if is_ccm(i, hscores, gamma, minpts)]
    if not ccms:
        return []
    clusters = []
    assigned = set()
    for ccm in ccms:
        if ccm in assigned:
            continue
        cluster = _expand_cluster(ccm, hscores, gamma, d, minpts)
        if cluster.size >= minpts:
            clusters.append(cluster)
            assigned.update(cluster.positions)
    return _merge_overlapping(clusters)
