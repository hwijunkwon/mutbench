"""dN/dS annotation layer for mutation hotspot clusters.

Post-processing annotation that classifies mutations as synonymous/nonsynonymous
and computes per-cluster dN/dS ratio to indicate selection pressure.
"""
from Bio.Data.CodonTable import standard_dna_table

CODON_TABLE = standard_dna_table.forward_table
STOP_CODONS = standard_dna_table.stop_codons


def translate_codon(codon: str) -> str:
    """Translate a DNA codon to its amino acid (single letter).

    Returns '*' for stop codons and 'X' for unknown codons.
    """
    codon = codon.upper()
    if codon in STOP_CODONS:
        return '*'
    return CODON_TABLE.get(codon, 'X')


def classify_mutation(ref_codon: str, mut_codon: str, codon_pos: int) -> str:
    """Classify a single-nucleotide mutation as synonymous or nonsynonymous.

    Parameters
    ----------
    ref_codon : str
        Reference codon (3 nucleotides).
    mut_codon : str
        Mutant codon (3 nucleotides).
    codon_pos : int
        Position within the codon where the mutation occurs (0, 1, or 2).

    Returns
    -------
    str
        'synonymous' if the amino acid is unchanged, 'nonsynonymous' otherwise.
    """
    ref_aa = translate_codon(ref_codon)
    mut_aa = translate_codon(mut_codon)
    if ref_aa == mut_aa:
        return 'synonymous'
    return 'nonsynonymous'


def compute_cluster_dnds(nonsyn_count: int, syn_count: int,
                         seq_length_codons: int) -> float:
    """Compute the dN/dS ratio for a cluster.

    Uses a simplified Nei-Gojobori-style calculation where ~75% of possible
    mutations are nonsynonymous and ~25% are synonymous.

    Parameters
    ----------
    nonsyn_count : int
        Number of observed nonsynonymous mutations.
    syn_count : int
        Number of observed synonymous mutations.
    seq_length_codons : int
        Length of the cluster region in codons.

    Returns
    -------
    float
        dN/dS ratio. Returns inf if dS is zero with dN > 0, or 0.0 if both
        are zero.
    """
    possible_n = seq_length_codons * 3 * 0.75
    possible_s = seq_length_codons * 3 * 0.25
    if syn_count == 0 or possible_s == 0:
        return float('inf') if nonsyn_count > 0 else 0.0
    dn = nonsyn_count / possible_n
    ds = syn_count / possible_s
    if ds == 0:
        return float('inf') if dn > 0 else 0.0
    return dn / ds


def annotate_clusters(clusters, reference_seq, mutations):
    """Annotate detected clusters with dN/dS information.

    For each cluster, classifies every mutated position as synonymous or
    nonsynonymous, then computes the per-cluster dN/dS ratio.

    Parameters
    ----------
    clusters : list of dict
        Each dict must have 'start', 'end', and 'positions' keys.
    reference_seq : str
        The reference DNA sequence.
    mutations : dict
        Mapping from position (int) to mutant nucleotide (str).

    Returns
    -------
    list of dict
        Copies of the input cluster dicts augmented with 'syn_count',
        'nonsyn_count', and 'dnds' keys.
    """
    results = []
    for cluster in clusters:
        syn_count = 0
        nonsyn_count = 0
        for pos in cluster['positions']:
            if pos not in mutations:
                continue
            codon_start = (pos // 3) * 3
            if codon_start + 3 > len(reference_seq):
                continue
            ref_codon = reference_seq[codon_start:codon_start + 3]
            mut_codon = list(ref_codon)
            codon_pos = pos % 3
            mut_codon[codon_pos] = mutations[pos]
            mut_codon = ''.join(mut_codon)
            classification = classify_mutation(ref_codon, mut_codon, codon_pos)
            if classification == 'synonymous':
                syn_count += 1
            else:
                nonsyn_count += 1
        cluster_len_codons = max(1, (cluster['end'] - cluster['start'] + 1) // 3)
        dnds = compute_cluster_dnds(nonsyn_count, syn_count, cluster_len_codons)
        result = {**cluster, 'syn_count': syn_count, 'nonsyn_count': nonsyn_count, 'dnds': dnds}
        results.append(result)
    return results
