"""Three-layer ground truth framework for MutBench.

Layer A (Adaptive): Positions under positive/diversifying selection.
  - Convergent evolution sites (documented independent emergence)
  - Sites with dN/dS > 1 from published analyses
  - TRUE POSITIVES for hotspot detection

Layer B (Constrained): Positions under strong purifying selection.
  - Conserved functional residues (fusion peptides, structural cysteines)
  - TRUE NEGATIVES — should NOT be detected as hotspots

Layer C (DMS-functional): Experimentally validated functional sites.
  - Deep mutational scanning fitness effects
  - Independent of sequence-based detection methods

References per pathogen are documented inline.
"""

import numpy as np


def get_gt_adaptive(pathogen: str, max_len: int) -> set[int]:
    """Layer A: Positions with evidence of positive selection (0-based)."""
    if pathogen == "SARS-CoV-2":
        # Convergent evolution across independent VOC lineages
        # Carabelli et al. 2023 Nat Rev Microbiol; Cao et al. 2023 Nature
        sites = {
            484, 501, 452, 346, 417, 681,  # High-confidence convergent
            478, 614, 655, 156, 18, 19, 20,  # Recurrent across lineages
            371, 373, 375, 376, 405, 408,  # Omicron RBD convergent
            440, 446, 460, 490, 493, 498,  # BA.2/BA.5/XBB convergent
        }
    elif pathogen == "H3N2":
        # Koel et al. 2013 Science cluster-transition + antigenic drift
        sites = {
            145, 155, 156, 158, 159, 189, 193,
            137, 142, 144, 186, 190, 192, 196,
            131, 135, 138, 140, 147, 148,
            157, 160, 163, 164, 165,
        }
    elif pathogen == "Norovirus":
        # Lindesmith et al. 2012, 2013 GII.4 epochal variant positions
        sites = {
            297, 298, 310, 333, 340, 345, 356, 357, 368,
            372, 373, 376, 394, 395, 397,
        }
    elif pathogen == "HIV-1":
        # Moore & Williamson 2015; Pond & Frost FUBAR/FEL
        sites = {
            132, 138, 141, 152, 155, 160, 165, 167, 169, 171,
            301, 305, 308, 315, 317, 319, 321, 323, 325,
            385, 392, 395, 396, 460, 462, 463,
        }
    elif pathogen == "Dengue":
        # Twiddy et al. 2002; Holmes 2003 serotype-defining positions
        sites = {
            305, 307, 310, 312, 329, 330, 332, 335,
            337, 339, 340, 360, 361, 364, 380, 383, 384,
            52, 71, 83, 120, 155, 157, 161,
        }
    elif pathogen == "RSV":
        # Mas et al. 2018; Sullender 2000 escape mutations
        sites = {
            255, 256, 259, 260, 262, 268, 272, 275, 276,
            148, 152, 155, 159, 163, 173, 174,
            422, 425, 427, 429,
        }
    elif pathogen == "Influenza_B":
        # Ni et al. 2013; Wang et al. 2008 antigenic drift
        sites = {
            122, 127, 129, 141, 147, 150, 151, 162, 163,
            164, 165, 175, 177, 179, 194, 196, 197,
        }
    elif pathogen == "MERS":
        # Kim et al. 2016 RBD escape; Tang et al. 2014 positive selection
        sites = {484, 506, 510, 511, 530, 534, 537, 539, 542}
    elif pathogen == "HCV":
        # HVR1 + HVR2: genuinely hypervariable regions
        sites = set(range(1, 28)) | set(range(77, 104))
    else:
        sites = set()

    return {p for p in sites if p < max_len}


def get_gt_constrained(pathogen: str, max_len: int) -> set[int]:
    """Layer B: Positions under strong purifying selection (0-based).

    TRUE NEGATIVES — good methods should NOT detect these.
    """
    sites = set()

    if pathogen == "SARS-CoV-2":
        # Fusion peptide, HR1, HR2: highly conserved structural elements
        for start, end in [(816, 833), (912, 984), (1163, 1213)]:
            sites.update(range(start, min(end + 1, max_len)))
        # Structural cysteines (invariant disulfide bonds)
        sites.update({15, 136, 166, 291, 301, 336, 361, 379, 391, 432, 480, 488})
    elif pathogen == "H3N2":
        # Receptor binding site core (conserved for sialic acid binding)
        sites = {98, 134, 136, 153, 183, 194, 195, 225, 226, 228}
    elif pathogen == "Norovirus":
        # Shell domain (highly conserved)
        sites = set(range(1, 230))
    elif pathogen == "HIV-1":
        # Conserved CD4 binding site contact residues
        sites = {
            124, 125, 126, 196, 198, 279, 280, 281, 282, 283,
            365, 366, 367, 368, 370, 425, 426, 427, 428, 429,
            430, 431, 432, 455, 456, 457, 458, 459, 469, 471,
            473, 474, 476,
        }
    elif pathogen == "Dengue":
        # Fusion loop: extremely conserved across all flaviviruses
        sites = set(range(98, 111))
        # Structural disulfides
        sites.update({3, 30, 60, 74, 92, 105, 116, 121, 137, 166, 176, 189})
    elif pathogen == "RSV":
        # Fusion peptide: highly conserved
        sites = set(range(137, 155))
    elif pathogen == "Influenza_B":
        # Receptor binding site core
        sites = {95, 141, 159, 190, 193, 194, 195, 225, 226, 228}
    elif pathogen == "MERS":
        # Fusion peptide + HR1
        sites = set(range(888, 912)) | set(range(974, 1060))
    elif pathogen == "HCV":
        # CD81 binding site: functionally constrained contact residues
        sites = {
            418, 420, 422, 424, 436, 438, 441, 442,
            503, 506, 528, 529, 530, 535,
        }

    return {p for p in sites if p < max_len}


def get_gt_dms(dms_scores: dict[int, float],
               threshold_percentile: float = 80) -> set[int]:
    """Layer C: DMS-derived functional positions.

    Positions where mutations have high phenotypic effect.
    """
    if not dms_scores:
        return set()
    values = list(dms_scores.values())
    threshold = np.percentile(values, threshold_percentile)
    return {pos for pos, val in dms_scores.items() if val >= threshold}


def get_all_gt_layers(
    pathogen: str, max_len: int, dms_scores: dict[int, float] | None = None
) -> dict[str, set[int]]:
    """Get all three GT layers for a pathogen."""
    return {
        "adaptive": get_gt_adaptive(pathogen, max_len),
        "constrained": get_gt_constrained(pathogen, max_len),
        "dms": get_gt_dms(dms_scores) if dms_scores else set(),
    }


def load_bloom_preferences(filepath: str) -> dict[int, float]:
    """Load Bloom lab amino acid preference CSV.

    Returns dict mapping 0-based position to preference entropy
    (high = tolerant of mutations = potential hotspot).
    """
    import pandas as pd

    df = pd.read_csv(filepath)
    aa_cols = [c for c in df.columns if c != "site" and len(c) == 1]
    position_scores = {}
    for _, row in df.iterrows():
        pos = int(row["site"]) - 1  # Convert to 0-based
        prefs = np.array([row[aa] for aa in aa_cols])
        prefs = prefs / (prefs.sum() + 1e-10)
        entropy = -np.sum(prefs * np.log2(prefs + 1e-10))
        position_scores[pos] = entropy
    return position_scores


def load_sars2_fitness(filepath: str) -> dict[int, float]:
    """Load SARS-CoV-2 Bloom fitness data (aamut_fitness_all.csv).

    Returns dict mapping 0-based Spike AA position to mean |fitness|.
    """
    import pandas as pd

    df = pd.read_csv(filepath)
    site_fitness = (
        df.groupby("site")["fitness"]
        .apply(lambda x: np.mean(np.abs(x)))
        .to_dict()
    )
    return {int(pos) - 1: val for pos, val in site_fitness.items()}
