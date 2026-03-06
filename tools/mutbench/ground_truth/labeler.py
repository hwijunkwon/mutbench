"""Ground truth labeler from DMS and known functional sites."""
import numpy as np
from dataclasses import dataclass, field


@dataclass
class GroundTruthSource:
    name: str
    positions: set[int] = field(default_factory=set)

    def merge(self, other: 'GroundTruthSource') -> 'GroundTruthSource':
        return GroundTruthSource(
            name=f"{self.name}+{other.name}",
            positions=self.positions | other.positions,
        )


def create_ground_truth_labels(genome_length: int,
                                functional_nuc_positions: set[int]) -> np.ndarray:
    labels = np.zeros(genome_length, dtype=int)
    for pos in functional_nuc_positions:
        if 0 <= pos < genome_length:
            labels[pos] = 1
    return labels
