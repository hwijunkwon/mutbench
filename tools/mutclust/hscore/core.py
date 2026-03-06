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
    n_seqs = len(alignment)
    nuc_to_idx = {'A': 0, 'T': 1, 'G': 2, 'C': 3}
    ref_indices = np.array([nuc_to_idx.get(c.upper(), -1) for c in reference])
    seq_matrix = np.array([[nuc_to_idx.get(c.upper(), -1) for c in seq] for seq in alignment])
    counts = np.zeros((seq_len, 4), dtype=int)
    for idx in range(4):
        counts[:, idx] = np.sum(seq_matrix == idx, axis=0)
    totals = counts.sum(axis=1, keepdims=True)
    totals = np.where(totals == 0, 1, totals)
    ratios = counts / totals
    ref_ratios = ratios[np.arange(seq_len), ref_indices]
    P = 1.0 - ref_ratios
    E = np.zeros(seq_len)
    for nuc_idx in range(4):
        mask = (nuc_idx != ref_indices) & (ratios[:, nuc_idx] > 0) & (P > 0)
        cond_prob = np.where(mask, ratios[:, nuc_idx] / np.where(P > 0, P, 1), 0)
        E += np.where(mask, cond_prob * np.log2(np.where(cond_prob > 0, cond_prob, 1)), 0)
    H = np.log2(P * np.abs(E) * 100 + 1)
    return H.tolist()
