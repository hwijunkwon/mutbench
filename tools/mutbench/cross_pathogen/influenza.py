"""Cross-pathogen stub for Influenza H3N2 HA segment analysis."""
import numpy as np
from tools.mutclust.hscore.core import compute_hscores_from_alignment
from tools.mutclust.mutclust_algo.core import mutclust


# Influenza A H3N2 HA segment is ~1701 nucleotides
HA_SEGMENT_LENGTH = 1701

# Known antigenic sites in HA (amino acid positions, H3 numbering)
ANTIGENIC_SITES = {
    'A': list(range(122, 147)),   # Site A
    'B': list(range(187, 198)),   # Site B
    'C': list(range(50, 54)) + [275, 276],  # Site C
    'D': list(range(201, 213)),   # Site D
    'E': list(range(62, 65)) + list(range(81, 83)),  # Site E
}


def get_antigenic_positions_nuc() -> set[int]:
    """Convert antigenic AA positions to nucleotide positions (0-indexed)."""
    positions = set()
    for site_positions in ANTIGENIC_SITES.values():
        for aa_pos in site_positions:
            base = (aa_pos - 1) * 3
            positions.update([base, base + 1, base + 2])
    return positions


def analyze_influenza(alignment: list[str], reference: str,
                       gamma: int = 10, d: int = 3, minpts: int = 5) -> dict:
    """Run MutClust analysis on Influenza HA sequences.

    Returns dict with hscores, clusters, and antigenic overlap info.
    """
    hscores = compute_hscores_from_alignment(alignment, reference)
    clusters = mutclust(np.array(hscores), gamma=gamma, d=d, minpts=minpts)

    antigenic = get_antigenic_positions_nuc()
    detected = set()
    for c in clusters:
        detected.update(c.positions)

    overlap = detected & antigenic

    return {
        'hscores': hscores,
        'n_clusters': len(clusters),
        'n_detected_positions': len(detected),
        'n_antigenic_overlap': len(overlap),
        'clusters': [{'start': c.start, 'end': c.end, 'positions': list(c.positions)} for c in clusters],
    }
