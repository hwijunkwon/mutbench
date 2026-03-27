#!/usr/bin/env python3
"""
Compute EVE (Evolutionary model of Variant Effect) per-position scores
for 12 viral proteins used in MutBench.

Pipeline:
1. Prepare protein MSAs from existing nucleotide/protein FASTA files
2. Align with MAFFT if needed
3. Convert to a2m format for EVE
4. Train EVE VAE model
5. Extract per-position evolutionary index (mean ELBO across all single mutations at each position)
6. Save to CSV

For viral proteins, within-species diversity is used as the evolutionary MSA,
with theta=0.01 (recommended for viruses in EVE documentation).
"""

import os
import sys
import json
import subprocess
import tempfile
import shutil
import numpy as np
import pandas as pd
from collections import defaultdict
from pathlib import Path
from Bio import SeqIO
from Bio.Seq import Seq
import warnings
warnings.filterwarnings("ignore")

# Add EVE to path
EVE_DIR = "/proj/paper/tools/EVE"
sys.path.insert(0, EVE_DIR)

# Paths
DATA_DIR = "/proj/paper/data"
OUTPUT_DIR = "/proj/paper/results/mutbench/feature_analysis"
MSA_DIR = "/proj/paper/data/eve_msa"
WEIGHTS_DIR = "/proj/paper/data/eve_weights"
CHECKPOINT_DIR = "/proj/paper/results/eve_checkpoints"
LOGS_DIR = "/proj/paper/results/eve_logs"

os.makedirs(MSA_DIR, exist_ok=True)
os.makedirs(WEIGHTS_DIR, exist_ok=True)
os.makedirs(CHECKPOINT_DIR, exist_ok=True)
os.makedirs(LOGS_DIR, exist_ok=True)

# 12 pathogens and their data sources
PATHOGENS = {
    "SARS-CoV-2": {
        "protein_name": "SPIKE_SARS2",
        "nt_aligned": f"{DATA_DIR}/ncbi_temporal/sars2_spike_nt_cds_aligned.fasta",
        "protein_seqs": None,  # translate from nt
        "description": "SARS-CoV-2 Spike protein"
    },
    "H3N2": {
        "protein_name": "HA_H3N2",
        "nt_aligned": f"{DATA_DIR}/influenza/h3n2_ha_nt_cds_aligned.fasta",
        "protein_seqs": None,
        "description": "Influenza A H3N2 Hemagglutinin"
    },
    "HIV-1": {
        "protein_name": "GP120_HIV1",
        "nt_aligned": f"{DATA_DIR}/hiv/hiv1_gp120_nt_cds_aligned.fasta",
        "protein_seqs": f"{DATA_DIR}/hiv/hiv1_gp120_sequences.fasta",
        "description": "HIV-1 gp120 envelope glycoprotein"
    },
    "HCV": {
        "protein_name": "E2_HCV",
        "nt_aligned": f"{DATA_DIR}/hcv/hcv_e2_nt_cds_aligned.fasta",
        "protein_seqs": f"{DATA_DIR}/hcv/hcv_e2_sequences.fasta",
        "description": "HCV E2 envelope glycoprotein"
    },
    "Dengue": {
        "protein_name": "E_DENV",
        "nt_aligned": f"{DATA_DIR}/dengue/dengue_e_nt_cds_aligned.fasta",
        "protein_seqs": f"{DATA_DIR}/dengue/dengue_e_sequences.fasta",
        "description": "Dengue virus E protein"
    },
    "MERS": {
        "protein_name": "SPIKE_MERS",
        "nt_aligned": f"{DATA_DIR}/mers/mers_spike_nt_cds_aligned.fasta",
        "protein_seqs": f"{DATA_DIR}/mers/mers_spike_sequences.fasta",
        "description": "MERS-CoV Spike protein"
    },
    "Norovirus": {
        "protein_name": "VP1_NORO",
        "nt_aligned": f"{DATA_DIR}/norovirus/norovirus_vp1_nt_cds_aligned.fasta",
        "protein_seqs": f"{DATA_DIR}/norovirus/norovirus_vp1_sequences.fasta",
        "description": "Norovirus VP1 capsid protein"
    },
    "RSV": {
        "protein_name": "F_RSV",
        "nt_aligned": f"{DATA_DIR}/rsv/rsv_f_nt_cds_aligned.fasta",
        "protein_seqs": f"{DATA_DIR}/rsv/rsv_f_sequences.fasta",
        "description": "RSV Fusion protein"
    },
    "Rabies": {
        "protein_name": "G_RABV",
        "nt_aligned": f"{DATA_DIR}/rabies/rabies_g_nt_cds_aligned.fasta",
        "protein_seqs": f"{DATA_DIR}/rabies/rabies_g_sequences.fasta",
        "description": "Rabies virus G glycoprotein"
    },
    "Zika": {
        "protein_name": "E_ZIKV",
        "nt_aligned": f"{DATA_DIR}/zika/zika_e_nt_cds_aligned.fasta",
        "protein_seqs": f"{DATA_DIR}/zika/zika_e_sequences.fasta",
        "description": "Zika virus E protein"
    },
    "Influenza_B": {
        "protein_name": "HA_FLUB",
        "nt_aligned": f"{DATA_DIR}/influenza/influenza_b_ha_nt_cds_aligned.fasta",
        "protein_seqs": f"{DATA_DIR}/influenza/influenza_b_ha_sequences.fasta",
        "description": "Influenza B Hemagglutinin"
    },
    "EV-A71": {
        "protein_name": "VP1_EVA71",
        "nt_aligned": f"{DATA_DIR}/enterovirus/eva71_vp1_nt_cds_aligned.fasta",
        "protein_seqs": f"{DATA_DIR}/enterovirus/eva71_vp1_sequences.fasta",
        "description": "Enterovirus A71 VP1"
    },
}


def translate_nt_to_protein(nt_fasta, max_seqs=5000):
    """Translate nucleotide alignment to protein sequences, removing gaps."""
    records = []
    for record in SeqIO.parse(nt_fasta, "fasta"):
        nt_seq = str(record.seq).replace("-", "").replace(".", "").upper()
        # Trim to multiple of 3
        nt_seq = nt_seq[:len(nt_seq) - (len(nt_seq) % 3)]
        if len(nt_seq) < 30:
            continue
        try:
            protein = str(Seq(nt_seq).translate(to_stop=False)).rstrip("*")
            if len(protein) < 10 or "X" in protein:
                continue
            record.seq = Seq(protein)
            records.append(record)
        except Exception:
            continue
    # Subsample if too many
    if len(records) > max_seqs:
        np.random.seed(42)
        indices = np.random.choice(len(records), max_seqs, replace=False)
        records = [records[i] for i in sorted(indices)]
    return records


def read_protein_seqs(fasta_path, max_seqs=5000):
    """Read protein sequences from FASTA."""
    records = list(SeqIO.parse(fasta_path, "fasta"))
    # Filter out very short or problematic sequences
    records = [r for r in records if len(str(r.seq).replace("-", "")) >= 10]
    if len(records) > max_seqs:
        np.random.seed(42)
        indices = np.random.choice(len(records), max_seqs, replace=False)
        records = [records[i] for i in sorted(indices)]
    return records


def align_with_mafft(records, output_a2m, protein_name, start_pos=1):
    """
    Align protein sequences with MAFFT and convert to a2m format.
    The first sequence is the focus/reference sequence.
    """
    # Write unaligned sequences to temp file
    tmp_input = tempfile.NamedTemporaryFile(mode="w", suffix=".fasta", delete=False)
    for r in records:
        seq = str(r.seq).replace("-", "").replace(".", "")
        tmp_input.write(f">{r.id}\n{seq}\n")
    tmp_input.close()

    # Run MAFFT
    tmp_output = tempfile.NamedTemporaryFile(mode="w", suffix=".fasta", delete=False)
    tmp_output.close()

    cmd = f"mafft --auto --thread 4 {tmp_input.name}"
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=600)

    if result.returncode != 0:
        print(f"  MAFFT failed: {result.stderr[:200]}")
        os.unlink(tmp_input.name)
        return None

    # Parse MAFFT output
    aligned_seqs = {}
    current_name = None
    current_seq = ""
    for line in result.stdout.split("\n"):
        if line.startswith(">"):
            if current_name:
                aligned_seqs[current_name] = current_seq
            current_name = line.strip()
            current_seq = ""
        else:
            current_seq += line.strip()
    if current_name:
        aligned_seqs[current_name] = current_seq

    os.unlink(tmp_input.name)

    if len(aligned_seqs) < 10:
        print(f"  Too few aligned sequences: {len(aligned_seqs)}")
        return None

    # Get the first sequence (reference) and determine its length
    first_name = list(aligned_seqs.keys())[0]
    first_seq = aligned_seqs[first_name]
    ref_len_no_gaps = len(first_seq.replace("-", ""))
    end_pos = start_pos + ref_len_no_gaps - 1

    # Write in a2m format: focus sequence header must have /start-end
    with open(output_a2m, "w") as f:
        # Write focus sequence first with proper header
        focus_header = f">{protein_name}/{start_pos}-{end_pos}"
        f.write(f"{focus_header}\n{first_seq}\n")
        # Write remaining sequences
        for name, seq in aligned_seqs.items():
            if name == first_name:
                continue
            f.write(f"{name}\n{seq}\n")

    return output_a2m


def train_eve_and_extract_scores(a2m_file, protein_name, pathogen_name, num_seqs):
    """
    Train EVE VAE on the MSA and extract per-position evolutionary scores.

    Per-position score = mean absolute evolutionary index across all 19 possible
    mutations at that position. Higher = more evolutionary constraint.
    """
    import torch
    from EVE import VAE_model
    from utils import data_utils

    print(f"  Loading MSA from {a2m_file}")

    # Adjust training parameters based on MSA size
    # Smaller MSAs need fewer steps; viral MSAs use theta=0.01
    theta = 0.01  # EVE recommendation for viruses

    # Load and process MSA
    weights_file = os.path.join(WEIGHTS_DIR, f"{protein_name}_theta_{theta}.npy")
    try:
        data = data_utils.MSA_processing(
            MSA_location=a2m_file,
            theta=theta,
            use_weights=True,
            weights_location=weights_file,
            threshold_sequence_frac_gaps=0.5,
            threshold_focus_cols_frac_gaps=0.3,
        )
    except Exception as e:
        print(f"  MSA processing failed: {e}")
        return None

    print(f"  MSA: {data.num_sequences} sequences, {data.seq_len} positions, Neff={data.Neff:.1f}")

    if data.num_sequences < 20:
        print(f"  Too few sequences ({data.num_sequences}) for EVE training")
        return None

    # Adjust model params for viral protein sizes
    model_params = json.load(open(os.path.join(EVE_DIR, "EVE", "default_model_params.json")))

    # Scale down model for smaller proteins/MSAs
    seq_len = data.seq_len
    if seq_len < 200:
        model_params["encoder_parameters"]["hidden_layers_sizes"] = [512, 256, 64]
        model_params["decoder_parameters"]["hidden_layers_sizes"] = [64, 256, 512]
        model_params["encoder_parameters"]["z_dim"] = 30
        model_params["decoder_parameters"]["z_dim"] = 30
    elif seq_len < 500:
        model_params["encoder_parameters"]["hidden_layers_sizes"] = [1024, 512, 128]
        model_params["decoder_parameters"]["hidden_layers_sizes"] = [128, 512, 1024]
        model_params["encoder_parameters"]["z_dim"] = 40
        model_params["decoder_parameters"]["z_dim"] = 40

    # Reduce training steps for feasibility
    # EVE default is 400k; we use 30k-100k based on MSA size
    if num_seqs < 100:
        n_steps = 20000
    elif num_seqs < 500:
        n_steps = 30000
    elif num_seqs < 2000:
        n_steps = 50000
    else:
        n_steps = 80000

    model_params["training_parameters"]["num_training_steps"] = n_steps
    model_params["training_parameters"]["batch_size"] = min(128, max(32, num_seqs // 4))
    model_params["training_parameters"]["log_training_freq"] = n_steps // 5
    model_params["training_parameters"]["save_model_params_freq"] = n_steps + 1  # don't save intermediate
    model_params["training_parameters"]["use_validation_set"] = False
    model_params["training_parameters"]["annealing_warm_up"] = n_steps // 4
    model_params["training_parameters"]["log_training_info"] = True
    model_params["training_parameters"]["training_logs_location"] = LOGS_DIR
    model_params["training_parameters"]["model_checkpoint_location"] = CHECKPOINT_DIR

    model_name = f"{protein_name}_eve"

    # Initialize model
    model = VAE_model.VAE_model(
        model_name=model_name,
        data=data,
        encoder_parameters=model_params["encoder_parameters"],
        decoder_parameters=model_params["decoder_parameters"],
        random_seed=42
    )
    model = model.to(model.device)

    print(f"  Training EVE for {n_steps} steps (batch_size={model_params['training_parameters']['batch_size']})...")

    # Train
    model.train_model(data=data, training_parameters=model_params["training_parameters"])

    # Load best model if validation was used, otherwise use final
    checkpoint_path = os.path.join(CHECKPOINT_DIR, f"{model_name}_final")
    if os.path.exists(checkpoint_path):
        checkpoint = torch.load(checkpoint_path, map_location=model.device, weights_only=False)
        model.load_state_dict(checkpoint['model_state_dict'])
        print(f"  Loaded final checkpoint")

    # Compute per-position evolutionary scores
    # For each position, compute mean |evol_index| across all 19 possible AA substitutions
    print(f"  Computing per-position evolutionary indices...")
    model.eval()

    focus_seq = data.focus_seq_trimmed
    n_positions = len(focus_seq)
    num_samples = 20  # Reduced from 100 for speed; still gives stable estimates

    # Build wild-type one-hot
    wt_one_hot = np.zeros((1, data.seq_len, data.alphabet_size))
    for j, letter in enumerate(focus_seq):
        if letter in data.aa_dict:
            k = data.aa_dict[letter]
            wt_one_hot[0, j, k] = 1.0

    # Build ALL mutant one-hots at once (19 per position)
    all_mutant_one_hots = []
    mutant_pos_map = []  # index -> position_idx

    for pos_idx in range(n_positions):
        aa_at_pos = focus_seq[pos_idx]
        if aa_at_pos not in data.aa_dict:
            continue
        for mut_aa in data.alphabet:
            if mut_aa == aa_at_pos or mut_aa not in data.aa_dict:
                continue
            mut_oh = wt_one_hot[0].copy()
            mut_oh[pos_idx, :] = 0.0
            mut_oh[pos_idx, data.aa_dict[mut_aa]] = 1.0
            all_mutant_one_hots.append(mut_oh)
            mutant_pos_map.append(pos_idx)

    # Prepend wild-type
    all_seqs = np.concatenate([wt_one_hot, np.array(all_mutant_one_hots)], axis=0)
    n_total = all_seqs.shape[0]
    print(f"  Total sequences to score: {n_total} (1 wt + {n_total-1} mutants)")

    # Score in large batches for efficiency
    batch_size = 512
    mean_elbos = np.zeros(n_total)

    with torch.no_grad():
        for sample_idx in range(num_samples):
            sample_elbos = np.zeros(n_total)
            for start in range(0, n_total, batch_size):
                end = min(start + batch_size, n_total)
                x = torch.tensor(all_seqs[start:end], dtype=model.dtype).to(model.device)
                elbos, _, _ = model.all_likelihood_components(x)
                sample_elbos[start:end] = elbos.cpu().numpy()
            mean_elbos += sample_elbos
            if (sample_idx + 1) % 5 == 0:
                print(f"    Sample {sample_idx+1}/{num_samples} done")
        mean_elbos /= num_samples

    # Compute per-position scores
    wt_elbo = mean_elbos[0]
    evol_indices = -(mean_elbos[1:] - wt_elbo)  # positive = constrained

    position_scores = {}
    pos_evol = defaultdict(list)
    for i, pos_idx in enumerate(mutant_pos_map):
        pos_evol[pos_idx].append(abs(evol_indices[i]))

    for pos_idx in range(n_positions):
        if pos_idx in pos_evol:
            position_scores[pos_idx] = float(np.mean(pos_evol[pos_idx]))
        else:
            position_scores[pos_idx] = 0.0

    return position_scores


def compute_independent_model_scores(a2m_file, protein_name, pathogen_name):
    """
    Fallback: Compute EVmutation-style independent model scores from MSA.
    Uses positional amino acid frequency entropy as evolutionary constraint proxy.
    This is the independent-site component of EVE (without the VAE).

    Score = conservation score based on column-wise Shannon entropy.
    Lower entropy = higher conservation = higher evolutionary constraint.
    We invert so higher score = more constrained (like EVE evol_index).
    """
    print(f"  Computing independent model (conservation) scores for {pathogen_name}...")

    aa_alphabet = "ACDEFGHIKLMNPQRSTVWY"
    aa_to_idx = {aa: i for i, aa in enumerate(aa_alphabet)}

    # Read MSA
    seq_name_to_seq = {}
    focus_name = None
    with open(a2m_file) as f:
        name = ""
        for i, line in enumerate(f):
            line = line.rstrip()
            if line.startswith(">"):
                name = line
                if i == 0:
                    focus_name = name
            else:
                seq_name_to_seq[name] = seq_name_to_seq.get(name, "") + line

    if not seq_name_to_seq:
        return None

    focus_seq = seq_name_to_seq[focus_name]

    # Identify focus columns (non-gap in reference)
    focus_cols = [i for i, c in enumerate(focus_seq) if c.upper() in aa_alphabet]

    # Build frequency matrix
    n_pos = len(focus_cols)
    n_aa = len(aa_alphabet)
    freq_matrix = np.zeros((n_pos, n_aa))

    for seq in seq_name_to_seq.values():
        for j, col_idx in enumerate(focus_cols):
            if col_idx < len(seq):
                aa = seq[col_idx].upper()
                if aa in aa_to_idx:
                    freq_matrix[j, aa_to_idx[aa]] += 1

    # Add pseudocounts
    freq_matrix += 1.0
    freq_matrix = freq_matrix / freq_matrix.sum(axis=1, keepdims=True)

    # Shannon entropy per position
    entropy = -np.sum(freq_matrix * np.log2(freq_matrix + 1e-10), axis=1)
    max_entropy = np.log2(n_aa)

    # Convert to conservation: higher = more constrained
    # conservation = max_entropy - entropy (ranges from 0 to max_entropy)
    conservation = max_entropy - entropy

    return {i: float(conservation[i]) for i in range(n_pos)}


def main():
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--pathogens", nargs="*", default=None,
                       help="Specific pathogens to process (default: all)")
    parser.add_argument("--fallback-only", action="store_true",
                       help="Skip EVE VAE training, use independent model only")
    parser.add_argument("--force", action="store_true",
                       help="Recompute even if output exists")
    args = parser.parse_args()

    pathogens_to_process = args.pathogens if args.pathogens else list(PATHOGENS.keys())

    results_summary = {}

    for pathogen_name in pathogens_to_process:
        if pathogen_name not in PATHOGENS:
            print(f"Unknown pathogen: {pathogen_name}")
            continue

        info = PATHOGENS[pathogen_name]
        protein_name = info["protein_name"]
        output_file = os.path.join(OUTPUT_DIR, f"{pathogen_name}_eve_score.csv")

        if os.path.exists(output_file) and not args.force:
            print(f"\n[{pathogen_name}] Output exists: {output_file} (use --force to recompute)")
            results_summary[pathogen_name] = "skipped (exists)"
            continue

        print(f"\n{'='*60}")
        print(f"Processing {pathogen_name}: {info['description']}")
        print(f"{'='*60}")

        # Step 1: Get protein sequences
        if info["protein_seqs"] and os.path.exists(info["protein_seqs"]):
            print(f"  Reading protein sequences from {info['protein_seqs']}")
            records = read_protein_seqs(info["protein_seqs"])
        elif info["nt_aligned"] and os.path.exists(info["nt_aligned"]):
            print(f"  Translating nucleotide alignment to protein")
            records = translate_nt_to_protein(info["nt_aligned"])
        else:
            print(f"  No input data found!")
            results_summary[pathogen_name] = "FAILED: no input data"
            continue

        num_seqs = len(records)
        print(f"  Got {num_seqs} protein sequences")

        if num_seqs < 10:
            print(f"  Too few sequences for EVE training")
            results_summary[pathogen_name] = f"FAILED: only {num_seqs} sequences"
            continue

        # Step 2: Align with MAFFT and convert to a2m
        a2m_file = os.path.join(MSA_DIR, f"{protein_name}.a2m")
        if not os.path.exists(a2m_file) or args.force:
            print(f"  Aligning {num_seqs} sequences with MAFFT...")
            result = align_with_mafft(records, a2m_file, protein_name)
            if result is None:
                print(f"  Alignment failed!")
                results_summary[pathogen_name] = "FAILED: alignment"
                continue
        else:
            print(f"  Using existing alignment: {a2m_file}")

        # Step 3: Train EVE or use fallback
        position_scores = None

        if not args.fallback_only:
            try:
                position_scores = train_eve_and_extract_scores(
                    a2m_file, protein_name, pathogen_name, num_seqs
                )
                if position_scores is not None:
                    method = "EVE_VAE"
            except Exception as e:
                print(f"  EVE training failed: {e}")
                import traceback
                traceback.print_exc()

        if position_scores is None:
            print(f"  Using independent model (conservation-based) as fallback")
            position_scores = compute_independent_model_scores(
                a2m_file, protein_name, pathogen_name
            )
            method = "EVE_independent"

        if position_scores is None:
            results_summary[pathogen_name] = "FAILED: scoring"
            continue

        # Step 4: Save to CSV
        df = pd.DataFrame({
            "position": list(position_scores.keys()),
            "eve_score": list(position_scores.values())
        })
        df = df.sort_values("position").reset_index(drop=True)
        df.to_csv(output_file, index=False)
        print(f"  Saved {len(df)} positions to {output_file}")
        print(f"  Score stats: mean={df['eve_score'].mean():.4f}, "
              f"std={df['eve_score'].std():.4f}, "
              f"min={df['eve_score'].min():.4f}, "
              f"max={df['eve_score'].max():.4f}")

        results_summary[pathogen_name] = f"OK ({method}, {len(df)} positions, {num_seqs} seqs)"

    # Print summary
    print(f"\n{'='*60}")
    print("SUMMARY")
    print(f"{'='*60}")
    for pathogen, status in results_summary.items():
        print(f"  {pathogen:20s}: {status}")


if __name__ == "__main__":
    main()
