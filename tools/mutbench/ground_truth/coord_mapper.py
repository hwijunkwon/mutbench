"""Coordinate mapping between amino acid and nucleotide positions."""


class CoordinateMapper:
    def __init__(self, gene_start: int, gene_end: int):
        self.gene_start = gene_start
        self.gene_end = gene_end

    def aa_to_nuc(self, aa_pos: int) -> list[int]:
        base = self.gene_start + (aa_pos - 1) * 3
        return [base, base + 1, base + 2]

    def nuc_to_aa(self, nuc_pos: int) -> int:
        offset = nuc_pos - self.gene_start
        return offset // 3 + 1

    def aa_set_to_nuc_set(self, aa_positions: set[int]) -> set[int]:
        result = set()
        for aa in aa_positions:
            result.update(self.aa_to_nuc(aa))
        return result
