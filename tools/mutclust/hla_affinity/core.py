"""HLA-epitope binding affinity analysis."""
import numpy as np

AA_HYDROPHOBICITY = {
    'A': 1.8, 'R': -4.5, 'N': -3.5, 'D': -3.5, 'C': 2.5,
    'E': -3.5, 'Q': -3.5, 'G': -0.4, 'H': -3.2, 'I': 4.5,
    'L': 3.8, 'K': -3.9, 'M': 1.9, 'F': 2.8, 'P': -1.6,
    'S': -0.8, 'T': -0.7, 'W': -0.9, 'Y': -1.3, 'V': 4.2,
}

def generate_epitopes(sequence, min_len=8, max_len=14):
    epitopes = []
    for length in range(min_len, max_len + 1):
        for i in range(len(sequence) - length + 1):
            epitope = sequence[i:i + length]
            if all(c in AA_HYDROPHOBICITY for c in epitope):
                epitopes.append(epitope)
    return epitopes

def estimate_binding_affinity(peptide):
    if not peptide or not all(c in AA_HYDROPHOBICITY for c in peptide):
        return 50000.0
    scores = [AA_HYDROPHOBICITY.get(aa, 0) for aa in peptide]
    anchor_score = abs(scores[1]) + abs(scores[-1]) if len(scores) >= 2 else 0
    mean_hydro = np.mean(scores)
    raw_score = anchor_score * 50 + abs(mean_hydro) * 100
    return max(1.0, 500.0 - raw_score)

def compute_log_fold_change(ref_affinity, mut_affinity):
    return np.log2(mut_affinity / ref_affinity)

def analyze_hla_epitopes(ref_seq, mut_seq, min_len=8, max_len=14, affinity_threshold=500.0):
    ref_epitopes = generate_epitopes(ref_seq, min_len, max_len)
    results = []
    for i, ref_ep in enumerate(ref_epitopes):
        ref_aff = estimate_binding_affinity(ref_ep)
        if ref_aff >= affinity_threshold:
            continue
        start = i % (len(ref_seq) - len(ref_ep) + 1)
        if start + len(ref_ep) <= len(mut_seq):
            mut_ep = mut_seq[start:start + len(ref_ep)]
            mut_aff = estimate_binding_affinity(mut_ep)
            lfc = compute_log_fold_change(ref_aff, mut_aff)
            results.append({'ref_epitope': ref_ep, 'mut_epitope': mut_ep,
                           'ref_affinity': ref_aff, 'mut_affinity': mut_aff, 'log2fc': lfc})
    return results
