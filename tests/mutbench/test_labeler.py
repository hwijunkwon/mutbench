import numpy as np
from tools.mutbench.ground_truth.labeler import (
    create_ground_truth_labels, GroundTruthSource
)


def test_create_labels_from_dms():
    genome_length = 1000
    functional_nuc_positions = {100, 101, 102, 200, 201, 202}
    labels = create_ground_truth_labels(genome_length, functional_nuc_positions)
    assert len(labels) == 1000
    assert labels[100] == 1
    assert labels[0] == 0
    assert sum(labels) == 6


def test_ground_truth_source_merge():
    src1 = GroundTruthSource(name='dms', positions={100, 200, 300})
    src2 = GroundTruthSource(name='known_sites', positions={200, 400})
    merged = src1.merge(src2)
    assert merged.positions == {100, 200, 300, 400}
