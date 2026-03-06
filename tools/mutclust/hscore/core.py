"""H-score: mutation importance metric combining frequency and diversity.

H_i = log2(P_i * |E_i| * 100 + 1)
From MutClust paper (Youn et al., BioData Mining 2025).
"""
import numpy as np
from math import log2

NUCLEOTIDES = ['A', 'T', 'G', 'C']

def compute_nucleotide_ratios(counts: dict[str, int]) -> dict[str, float]:
    total = sum(counts.values())
    if total == 0:
        return {n: 0.0 for n in NUCLEOTIDES}
    return {n: counts.get(n, 0) / total for n in NUCLEOTIDES}

def compute_mutation_ratio(ratios: dict[str, float], ref: str) -> float:
    return sum(r for n, r in ratios.items() if n != ref)

def compute_mutation_entropy(ratios: dict[str, float], ref: str) -> float:
    P = compute_mutation_ratio(ratios, ref)
    if P == 0:
        return 0.0
    entropy = 0.0
    for n in NUCLEOTIDES:
        if n == ref:
            continue
        r = ratios[n]
        if r > 0:
            cond_prob = r / P
            entropy += cond_prob * log2(cond_prob)
    return entropy

def compute_hscore(P: float, E: float) -> float:
    val = P * abs(E) * 100 + 1
    return log2(val)

def compute_hscores_from_counts(counts_per_position: list[dict[str, int]], reference: list[str]) -> list[float]:
    hscores = []
    for counts, ref in zip(counts_per_position, reference):
        ratios = compute_nucleotide_ratios(counts)
        P = compute_mutation_ratio(ratios, ref)
        E = compute_mutation_entropy(ratios, ref)
        H = compute_hscore(P, E)
        hscores.append(H)
    return hscores

def compute_hscores_from_alignment(alignment: list[str], reference: str) -> list[float]:
    seq_len = len(reference)
    hscores = []
    for pos in range(seq_len):
        counts = {n: 0 for n in NUCLEOTIDES}
        for seq in alignment:
            nuc = seq[pos].upper()
            if nuc in counts:
                counts[nuc] += 1
        ref_nuc = reference[pos].upper()
        ratios = compute_nucleotide_ratios(counts)
        P = compute_mutation_ratio(ratios, ref_nuc)
        E = compute_mutation_entropy(ratios, ref_nuc)
        H = compute_hscore(P, E)
        hscores.append(H)
    return hscores
