#!/usr/bin/env python3
"""Compute per-position semantic change using ESM-2 embeddings for 9 pathogens.

Semantic change measures how much a mutation alters the protein's "meaning"
in the language model's representation space. For each position, we compute
the mean cosine distance between the wild-type embedding and each observed
mutant embedding at that position.

Reference: Hie et al. (2021) Science 371:284-288.
"""

import os
import sys
import numpy as np
import pandas as pd
import torch
from collections import Counter

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

BASE = os.path.join(os.path.dirname(__file__), "..")
OUT_DIR = os.path.join(BASE, "results/mutbench/feature_analysis")
os.makedirs(OUT_DIR, exist_ok=True)

PATHOGENS = {
    "SARS-CoV-2": "data/ncbi_temporal/spike_500_subsample.fasta",
    "H3N2": "data/influenza/h3n2_ha_sequences.fasta",
    "Norovirus": "data/norovirus/norovirus_vp1_sequences.fasta",
    "HIV-1": "data/hiv/hiv1_gp120_sequences.fasta",
    "Dengue": "data/dengue/dengue_e_sequences.fasta",
    "RSV": "data/rsv/rsv_f_sequences.fasta",
    "Influenza_B": "data/influenza/influenza_b_ha_sequences.fasta",
    "MERS": "data/mers/mers_spike_sequences.fasta",
    "HCV": "data/hcv/hcv_e2_sequences.fasta",
}

VALID_AA = set("ACDEFGHIKLMNPQRSTVWY")


def parse_msa(fasta_path):
    from Bio import SeqIO
    records = list(SeqIO.parse(fasta_path, "fasta"))
    lengths = [len(r.seq) for r in records]
    modal_len = max(set(lengths), key=lengths.count)
    filtered = [r for r in records if len(r.seq) == modal_len]
    return np.array([list(str(r.seq).upper()) for r in filtered])


def get_consensus(msa):
    """Get consensus sequence from MSA."""
    n_seqs, seq_len = msa.shape
    consensus = []
    for pos in range(seq_len):
        col = msa[:, pos]
        counts = Counter(c for c in col if c in VALID_AA)
        if counts:
            consensus.append(max(counts, key=counts.get))
        else:
            consensus.append("A")  # fallback
    return "".join(consensus)


def compute_semantic_change(model, alphabet, batch_converter, consensus_seq, msa, device):
    """Compute per-position semantic change.

    For each position, mutate the consensus to each observed variant,
    get ESM-2 embeddings, and compute mean cosine distance.
    """
    seq_len = len(consensus_seq)
    n_seqs = msa.shape[0]

    # Get wild-type embedding (per-position representations)
    print("    Computing wild-type embedding...")
    wt_data = [("wt", consensus_seq)]
    _, _, wt_tokens = batch_converter(wt_data)
    wt_tokens = wt_tokens.to(device)

    with torch.no_grad():
        wt_result = model(wt_tokens, repr_layers=[33])
    # Shape: [1, seq_len+2, 1280] (includes BOS/EOS tokens)
    wt_repr = wt_result["representations"][33][0, 1:-1, :].cpu()  # [seq_len, 1280]

    semantic_scores = np.zeros(seq_len)

    # For each position, compute semantic change for observed variants
    print("    Computing per-position semantic change...")
    batch_size = 20  # Process multiple mutations at once

    for pos in range(seq_len):
        col = msa[:, pos]
        counts = Counter(c for c in col if c in VALID_AA)
        wt_aa = consensus_seq[pos]

        # Get variant amino acids (excluding consensus)
        variants = {aa: count for aa, count in counts.items() if aa != wt_aa}
        if not variants:
            continue

        total_variant_count = sum(variants.values())
        total_count = sum(counts.values())

        # Compute embedding for each variant
        cosine_dists = []
        weights = []

        variant_seqs = []
        variant_weights = []

        for var_aa, count in variants.items():
            mut_seq = consensus_seq[:pos] + var_aa + consensus_seq[pos+1:]
            variant_seqs.append(("mut", mut_seq))
            variant_weights.append(count / total_count)

        if not variant_seqs:
            continue

        # Batch process variants
        for batch_start in range(0, len(variant_seqs), batch_size):
            batch = variant_seqs[batch_start:batch_start + batch_size]
            batch_w = variant_weights[batch_start:batch_start + batch_size]

            _, _, mut_tokens = batch_converter(batch)
            mut_tokens = mut_tokens.to(device)

            with torch.no_grad():
                mut_result = model(mut_tokens, repr_layers=[33])

            mut_repr = mut_result["representations"][33][:, 1:-1, :]  # [batch, seq_len, 1280]

            for j in range(len(batch)):
                # Cosine distance at this position
                wt_vec = wt_repr[pos]
                mut_vec = mut_repr[j, pos, :].cpu()

                cos_sim = torch.nn.functional.cosine_similarity(
                    wt_vec.unsqueeze(0), mut_vec.unsqueeze(0)
                ).item()
                cos_dist = 1.0 - cos_sim

                cosine_dists.append(cos_dist)
                weights.append(batch_w[j])

        # Weighted mean semantic change
        if cosine_dists:
            weights = np.array(weights)
            weights = weights / weights.sum()
            semantic_scores[pos] = np.average(cosine_dists, weights=weights)

        if (pos + 1) % 100 == 0:
            print(f"      Position {pos+1}/{seq_len}")

    return semantic_scores


def main():
    print("=" * 60)
    print("Computing per-position semantic change (ESM-2) for 9 pathogens")
    print("=" * 60)

    # Load ESM-2 model
    print("\nLoading ESM-2 model (esm2_t33_650M_UR50D)...")
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    print(f"  Device: {device}")

    import esm
    model, alphabet = esm.pretrained.esm2_t33_650M_UR50D()
    batch_converter = alphabet.get_batch_converter()
    model = model.to(device)
    model.eval()
    print("  Model loaded!")

    all_results = []

    for pathogen, fasta_rel in PATHOGENS.items():
        print(f"\n{'='*40}")
        print(f"  {pathogen}")
        print(f"{'='*40}")

        # Check if already computed
        out_path = os.path.join(OUT_DIR, f"{pathogen}_semantic_change.csv")
        if os.path.exists(out_path):
            print(f"    Already computed: {out_path}")
            df = pd.read_csv(out_path)
            all_results.append({
                "pathogen": pathogen,
                "n_positions": len(df),
                "mean_semantic": round(df["semantic_change"].mean(), 4),
                "max_semantic": round(df["semantic_change"].max(), 4),
            })
            continue

        fasta_path = os.path.join(BASE, fasta_rel)
        msa = parse_msa(fasta_path)
        print(f"    MSA shape: {msa.shape}")

        consensus = get_consensus(msa)
        print(f"    Consensus length: {len(consensus)}")

        # Compute semantic change
        scores = compute_semantic_change(
            model, alphabet, batch_converter, consensus, msa, device
        )

        # Save
        df = pd.DataFrame({
            "position": np.arange(len(scores)),
            "semantic_change": np.round(scores, 6),
        })
        df.to_csv(out_path, index=False)
        print(f"    Saved: {out_path}")

        nonzero = np.sum(scores > 0)
        print(f"    Mean={scores.mean():.4f}, Max={scores.max():.4f}, Nonzero={nonzero}/{len(scores)}")

        all_results.append({
            "pathogen": pathogen,
            "n_positions": len(scores),
            "mean_semantic": round(scores.mean(), 4),
            "max_semantic": round(scores.max(), 4),
        })

    summary = pd.DataFrame(all_results)
    summary.to_csv(os.path.join(OUT_DIR, "semantic_change_summary.csv"), index=False)
    print(f"\n\nSummary:\n{summary.to_string(index=False)}")
    print("\nDone!")


if __name__ == "__main__":
    main()
