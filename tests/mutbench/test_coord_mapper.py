from tools.mutbench.ground_truth.coord_mapper import CoordinateMapper


def test_aa_to_nuc():
    mapper = CoordinateMapper(gene_start=21563, gene_end=25384)
    nuc_positions = mapper.aa_to_nuc(484)
    assert len(nuc_positions) == 3
    assert nuc_positions[0] == 21563 + (484 - 1) * 3


def test_nuc_to_aa():
    mapper = CoordinateMapper(gene_start=21563, gene_end=25384)
    aa_pos = mapper.nuc_to_aa(21563 + (484 - 1) * 3)
    assert aa_pos == 484


def test_batch_mapping():
    mapper = CoordinateMapper(gene_start=0, gene_end=299)
    aa_positions = {10, 20, 50}
    nuc_set = mapper.aa_set_to_nuc_set(aa_positions)
    assert len(nuc_set) == 9
