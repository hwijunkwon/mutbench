#!/usr/bin/env python3
"""Compute all 10 features for 3 new viruses: Zika, Rabies, EV-A71.

Features:
  1. freq: mutation frequency at each position
  2. entropy: Shannon entropy
  3. rare_freq: rare variant frequency (allele freq < 0.01)
  4. homoplasy: Fitch parsimony on FastTree phylogeny
  5. esm2_llr: ESM-2 log-likelihood ratio
  6. plddt: ESMFold predicted pLDDT
  7. sasa: Solvent Accessible Surface Area (RSA via ESMFold + ShrakeRupley)
  8. grantham: mean Grantham distance from consensus
  9. dnds_proxy: protein-level evolutionary rate / codon degeneracy
  10. semantic_change: ESM-2 embedding cosine distance

Output:
  - feature_matrix_{pathogen}.csv per pathogen
  - Individual feature CSVs per pathogen
  - per_feature_auc_v2.csv updated with new viruses
"""

import os
import sys
import time
import subprocess
import tempfile
import hashlib
import warnings
import gc
from collections import Counter, OrderedDict

import numpy as np
import pandas as pd
from scipy.stats import spearmanr
from sklearn.metrics import roc_auc_score

warnings.filterwarnings("ignore")

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, PROJECT_ROOT)

from tools.mutbench.ground_truth.multilayer_gt import get_gt_adaptive
from tools.mutbench.scoring.homoplasy import fitch_parsimony_count, load_tree

# ── Configuration ────────────────────────────────────────────────────────
NEW_PATHOGENS = {
    "Zika": {
        "fasta": "data/zika/zika_e_sequences.fasta",
        "struct_name": "zika",
    },
    "Rabies": {
        "fasta": "data/rabies/rabies_g_sequences.fasta",
        "struct_name": "rabies",
    },
    "EV-A71": {
        "fasta": "data/enterovirus/eva71_vp1_sequences.fasta",
        "struct_name": "eva71",
    },
}

FEATURE_DIR = os.path.join(PROJECT_ROOT, "results/mutbench/feature_analysis")
HOMOPLASY_DIR = os.path.join(PROJECT_ROOT, "results/mutbench/homoplasy_scores")
ESM_DIR = os.path.join(PROJECT_ROOT, "results/mutbench/esm_scores")
STRUCT_DIR = os.path.join(PROJECT_ROOT, "results/mutbench/structural_features")
PDB_DIR = os.path.join(STRUCT_DIR, "pdb_structures")

for d in [FEATURE_DIR, HOMOPLASY_DIR, ESM_DIR, STRUCT_DIR, PDB_DIR]:
    os.makedirs(d, exist_ok=True)

VALID_AA = set("ACDEFGHIKLMNPQRSTVWY")

# ── Grantham distance matrix ────────────────────────────────────────────
GRANTHAM = {
    ('A','R'):112,('A','N'):111,('A','D'):126,('A','C'):195,('A','Q'):91,('A','E'):107,
    ('A','G'):60,('A','H'):86,('A','I'):94,('A','L'):96,('A','K'):106,('A','M'):84,
    ('A','F'):113,('A','P'):27,('A','S'):99,('A','T'):58,('A','W'):148,('A','Y'):112,('A','V'):64,
    ('R','N'):86,('R','D'):96,('R','C'):180,('R','Q'):43,('R','E'):54,('R','G'):125,
    ('R','H'):29,('R','I'):97,('R','L'):102,('R','K'):26,('R','M'):91,('R','F'):97,
    ('R','P'):103,('R','S'):110,('R','T'):71,('R','W'):101,('R','Y'):77,('R','V'):96,
    ('N','D'):23,('N','C'):139,('N','Q'):46,('N','E'):42,('N','G'):80,('N','H'):68,
    ('N','I'):149,('N','L'):153,('N','K'):94,('N','M'):142,('N','F'):158,('N','P'):91,
    ('N','S'):46,('N','T'):65,('N','W'):174,('N','Y'):143,('N','V'):133,
    ('D','C'):154,('D','Q'):61,('D','E'):45,('D','G'):94,('D','H'):81,('D','I'):168,
    ('D','L'):172,('D','K'):101,('D','M'):160,('D','F'):177,('D','P'):108,('D','S'):65,
    ('D','T'):85,('D','W'):181,('D','Y'):160,('D','V'):152,
    ('C','Q'):154,('C','E'):170,('C','G'):159,('C','H'):174,('C','I'):198,('C','L'):198,
    ('C','K'):202,('C','M'):196,('C','F'):205,('C','P'):169,('C','S'):112,('C','T'):149,
    ('C','W'):215,('C','Y'):194,('C','V'):192,
    ('Q','E'):29,('Q','G'):87,('Q','H'):24,('Q','I'):109,('Q','L'):113,('Q','K'):53,
    ('Q','M'):101,('Q','F'):116,('Q','P'):76,('Q','S'):68,('Q','T'):42,('Q','W'):130,
    ('Q','Y'):99,('Q','V'):96,
    ('E','G'):98,('E','H'):40,('E','I'):134,('E','L'):138,('E','K'):56,('E','M'):126,
    ('E','F'):140,('E','P'):93,('E','S'):80,('E','T'):65,('E','W'):152,('E','Y'):122,('E','V'):121,
    ('G','H'):98,('G','I'):135,('G','L'):138,('G','K'):127,('G','M'):127,('G','F'):153,
    ('G','P'):42,('G','S'):56,('G','T'):59,('G','W'):184,('G','Y'):147,('G','V'):109,
    ('H','I'):94,('H','L'):99,('H','K'):32,('H','M'):87,('H','F'):100,('H','P'):77,
    ('H','S'):89,('H','T'):47,('H','W'):115,('H','Y'):83,('H','V'):84,
    ('I','L'):5,('I','K'):102,('I','M'):10,('I','F'):21,('I','P'):95,('I','S'):142,
    ('I','T'):89,('I','W'):61,('I','Y'):33,('I','V'):29,
    ('L','K'):107,('L','M'):15,('L','F'):22,('L','P'):98,('L','S'):145,('L','T'):92,
    ('L','W'):61,('L','Y'):36,('L','V'):32,
    ('K','M'):95,('K','F'):102,('K','P'):103,('K','S'):121,('K','T'):78,('K','W'):110,
    ('K','Y'):85,('K','V'):97,
    ('M','F'):28,('M','P'):87,('M','S'):135,('M','T'):81,('M','W'):67,('M','Y'):36,('M','V'):21,
    ('F','P'):114,('F','S'):155,('F','T'):103,('F','W'):40,('F','Y'):22,('F','V'):50,
    ('P','S'):74,('P','T'):38,('P','W'):147,('P','Y'):110,('P','V'):68,
    ('S','T'):58,('S','W'):177,('S','Y'):144,('S','V'):124,
    ('T','W'):128,('T','Y'):92,('T','V'):69,
    ('W','Y'):37,('W','V'):88,
    ('Y','V'):55,
}

CODON_DEGENERACY = {
    'A': 4, 'R': 6, 'N': 2, 'D': 2, 'C': 2,
    'Q': 2, 'E': 2, 'G': 4, 'H': 2, 'I': 3,
    'L': 6, 'K': 2, 'M': 1, 'F': 2, 'P': 4,
    'S': 6, 'T': 4, 'W': 1, 'Y': 2, 'V': 4,
    '*': 3,
}

MAX_ASA = {
    'A': 129, 'R': 274, 'N': 195, 'D': 193, 'C': 167,
    'E': 223, 'Q': 225, 'G': 104, 'H': 224, 'I': 197,
    'L': 201, 'K': 236, 'M': 224, 'F': 240, 'P': 159,
    'S': 155, 'T': 172, 'W': 285, 'Y': 263, 'V': 174,
}


# ── MSA parsing ─────────────────────────────────────────────────────────
def parse_msa(fasta_path):
    """Parse FASTA into 2D character array (n_seqs x seq_len).
    Keeps only sequences matching the modal length."""
    from Bio import SeqIO
    records = list(SeqIO.parse(fasta_path, "fasta"))
    lengths = [len(r.seq) for r in records]
    modal_len = max(set(lengths), key=lengths.count)
    filtered = [r for r in records if len(r.seq) == modal_len]
    n_dropped = len(records) - len(filtered)
    if n_dropped > 0:
        print(f"    Kept {len(filtered)}/{len(records)} seqs with modal length {modal_len} "
              f"(dropped {n_dropped})")
    else:
        print(f"    All {len(filtered)} seqs have length {modal_len}")
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
            consensus.append("A")
    return "".join(consensus)


def get_reference_sequence(fasta_path):
    """Get first sequence from FASTA as reference (for structural features)."""
    from Bio import SeqIO
    rec = next(SeqIO.parse(fasta_path, "fasta"))
    return str(rec.seq).replace("-", "").replace("X", "A")


# ── Feature 1-3: freq, entropy, rare_freq ────────────────────────────────
def compute_freq_entropy(msa):
    n_seqs, seq_len = msa.shape
    freq = np.zeros(seq_len)
    entropy = np.zeros(seq_len)
    rare_freq = np.zeros(seq_len)

    for pos in range(seq_len):
        col = msa[:, pos]
        counts = Counter(col)
        total = sum(v for k, v in counts.items() if k not in ("-", "X", "."))
        if total == 0:
            continue
        non_gap = {k: v for k, v in counts.items() if k not in ("-", "X", ".")}
        if not non_gap:
            continue
        consensus_aa = max(non_gap, key=non_gap.get)
        consensus_freq = non_gap[consensus_aa] / total
        freq[pos] = 1.0 - consensus_freq
        probs = np.array([v / total for v in non_gap.values()])
        probs = probs[probs > 0]
        entropy[pos] = -np.sum(probs * np.log2(probs))
        rare_sum = sum(v / total for v in non_gap.values() if v / total < 0.01)
        rare_freq[pos] = rare_sum

    return freq, entropy, rare_freq


# ── Feature 4: homoplasy ────────────────────────────────────────────────
MAX_SEQS = 500
SEED = 42

def read_fasta_dict(filepath):
    sequences = OrderedDict()
    current_name = None
    current_seq = []
    with open(filepath) as f:
        for line in f:
            line = line.strip()
            if line.startswith('>'):
                if current_name is not None:
                    sequences[current_name] = ''.join(current_seq)
                current_name = line[1:].split()[0]
                current_seq = []
            else:
                current_seq.append(line)
    if current_name is not None:
        sequences[current_name] = ''.join(current_seq)
    return sequences


def clean_sequence(seq):
    cleaned = []
    for c in seq.upper():
        if c in VALID_AA:
            cleaned.append(c)
        elif c == '-' or c == '.':
            continue
        else:
            cleaned.append('X')
    return ''.join(cleaned)


def compute_homoplasy(pathogen, fasta_path):
    """Compute homoplasy scores via Fitch parsimony on a FastTree phylogeny."""
    out_path = os.path.join(HOMOPLASY_DIR, f"{pathogen}_homoplasy.csv")
    if os.path.exists(out_path):
        print(f"    Homoplasy already computed: {out_path}")
        return pd.read_csv(out_path)

    # Load and clean sequences
    raw_seqs = read_fasta_dict(fasta_path)
    cleaned = OrderedDict()
    for name, seq in raw_seqs.items():
        c = clean_sequence(seq)
        if len(c) >= 50:
            cleaned[name] = c

    # Truncate to min length
    if not cleaned:
        print(f"    ERROR: No sequences after cleaning")
        return None
    min_len = min(len(seq) for seq in cleaned.values())
    truncated = OrderedDict((n, s[:min_len]) for n, s in cleaned.items())
    seq_len = min_len
    print(f"    Homoplasy: {len(truncated)} seqs, truncated to {seq_len}")

    # Deduplicate
    seen = set()
    unique = OrderedDict()
    for name, seq in truncated.items():
        h = hashlib.md5(seq.encode()).hexdigest()
        if h not in seen:
            seen.add(h)
            unique[name] = seq
    print(f"    After dedup: {len(unique)} unique")

    # Subsample
    if len(unique) > MAX_SEQS:
        rng = np.random.default_rng(SEED)
        names = list(unique.keys())
        chosen = set(rng.choice(names, size=MAX_SEQS, replace=False))
        sampled = OrderedDict((n, unique[n]) for n in names if n in chosen)
    else:
        sampled = unique
    print(f"    Using {len(sampled)} sequences for tree")

    # Build tree with FastTree
    with tempfile.TemporaryDirectory() as tmpdir:
        aligned_path = os.path.join(tmpdir, 'aligned.fasta')
        tree_path = os.path.join(tmpdir, 'tree.nwk')

        with open(aligned_path, 'w') as f:
            for name, seq in sampled.items():
                f.write(f'>{name}\n')
                for i in range(0, len(seq), 60):
                    f.write(seq[i:i+60] + '\n')

        print(f"    Building tree with FastTree...")
        cmd = f'fasttree -quiet < {aligned_path} > {tree_path}'
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        if result.returncode != 0:
            print(f"    FastTree failed: {result.stderr}")
            return None

        tree = load_tree(tree_path)
        print(f"    Tree: {len(tree.get_terminals())} terminals")

        print(f"    Running Fitch parsimony ({seq_len} positions)...")
        counts = fitch_parsimony_count(tree, sampled, seq_len)

    max_count = counts.max()
    normalized = counts / max_count if max_count > 0 else counts.astype(float)

    df = pd.DataFrame({
        'position': np.arange(1, seq_len + 1),
        'raw_count': counts,
        'normalized_score': np.round(normalized, 6),
    })
    df.to_csv(out_path, index=False)
    nonzero = counts[counts > 0]
    print(f"    Saved: {out_path}")
    print(f"    Positions with changes: {len(nonzero)}/{seq_len}, max={max_count}")
    return df


# ── Feature 5: ESM-2 LLR ────────────────────────────────────────────────
ESM_MAX_LEN = 1022
ESM_OVERLAP = 256

def compute_esm_llr(pathogen, consensus_seq, model, alphabet, batch_converter, device):
    """Compute ESM-2 LLR scores."""
    import torch

    out_path = os.path.join(ESM_DIR, f"{pathogen}_esm_llr.npy")
    if os.path.exists(out_path):
        print(f"    ESM-2 LLR already computed: {out_path}")
        return np.load(out_path)

    seq_len = len(consensus_seq)
    print(f"    Computing ESM-2 LLR ({seq_len}aa)...")

    def compute_single(sequence):
        data = [("protein", sequence)]
        _, _, batch_tokens = batch_converter(data)
        batch_tokens = batch_tokens.to(device)
        with torch.no_grad():
            results = model(batch_tokens, repr_layers=[], return_contacts=False)
            logits = results["logits"]
        log_probs = torch.log_softmax(logits, dim=-1)
        llr = np.zeros(len(sequence))
        for i, aa in enumerate(sequence):
            token_idx = alphabet.get_idx(aa)
            llr[i] = -log_probs[0, i + 1, token_idx].item()
        return llr

    if seq_len <= ESM_MAX_LEN:
        llr = compute_single(consensus_seq)
    else:
        # Sliding window
        scores_sum = np.zeros(seq_len)
        counts = np.zeros(seq_len)
        step = ESM_MAX_LEN - ESM_OVERLAP
        starts = list(range(0, seq_len - ESM_MAX_LEN + 1, step))
        if starts[-1] + ESM_MAX_LEN < seq_len:
            starts.append(seq_len - ESM_MAX_LEN)
        print(f"    Using {len(starts)} sliding windows")
        for si, start in enumerate(starts):
            end = start + ESM_MAX_LEN
            window_llr = compute_single(consensus_seq[start:end])
            scores_sum[start:end] += window_llr
            counts[start:end] += 1
            print(f"      Window {si+1}/{len(starts)} done")
        counts[counts == 0] = 1
        llr = scores_sum / counts

    np.save(out_path, llr)
    print(f"    Saved: {out_path}")
    print(f"    Stats: mean={llr.mean():.4f}, std={llr.std():.4f}")

    torch.cuda.empty_cache()
    gc.collect()
    return llr


# ── Feature 6: pLDDT ────────────────────────────────────────────────────
def extract_plddt_from_pdb(pdb_text):
    positions = []
    plddts = []
    for line in pdb_text.split("\n"):
        if line.startswith("ATOM") and line[12:16].strip() == "CA":
            resnum = int(line[22:26].strip())
            bfactor = float(line[60:66].strip())
            positions.append(resnum)
            plddts.append(bfactor)
    return positions, plddts


def esmfold_api_chunk(sequence, chunk_size=400, overlap=50, max_retries=3):
    """ESMFold API with chunking. Returns pLDDT on 0-100 scale."""
    import requests

    seq_len = len(sequence)
    if seq_len <= chunk_size:
        chunks = [(0, seq_len)]
    else:
        chunks = []
        start = 0
        while start < seq_len:
            end = min(start + chunk_size, seq_len)
            chunks.append((start, end))
            if end == seq_len:
                break
            start = end - overlap

    print(f"    ESMFold: {len(chunks)} chunk(s) for {seq_len}aa")

    plddt_sum = np.zeros(seq_len)
    plddt_count = np.zeros(seq_len)

    for i, (start, end) in enumerate(chunks):
        chunk_seq = sequence[start:end]
        print(f"      Chunk {i+1}/{len(chunks)}: pos {start+1}-{end} ({len(chunk_seq)}aa)", end="")

        success = False
        for attempt in range(max_retries):
            try:
                r = requests.post(
                    "https://api.esmatlas.com/foldSequence/v1/pdb/",
                    data=chunk_seq,
                    timeout=300,
                )
                if r.status_code == 200:
                    _, chunk_plddts = extract_plddt_from_pdb(r.text)
                    for j, plddt in enumerate(chunk_plddts):
                        pos = start + j
                        if pos < seq_len:
                            plddt_sum[pos] += plddt
                            plddt_count[pos] += 1
                    print(f" -> OK")
                    success = True
                    break
                else:
                    print(f" -> HTTP {r.status_code}", end="")
                    if attempt < max_retries - 1:
                        wait = 15 * (attempt + 1)
                        print(f", retry in {wait}s", end="")
                        time.sleep(wait)
            except Exception as e:
                print(f" -> {e}", end="")
                if attempt < max_retries - 1:
                    wait = 15 * (attempt + 1)
                    print(f", retry in {wait}s", end="")
                    time.sleep(wait)

        if not success:
            print(f" FAILED")
            return None, None

        if i < len(chunks) - 1:
            time.sleep(3)

    valid = plddt_count > 0
    plddt_avg = np.where(valid, plddt_sum / plddt_count, 0)
    # ESMFold B-factors may be on 0-1 scale
    if np.max(plddt_avg) <= 1.0:
        plddt_avg = plddt_avg * 100.0

    return list(range(1, seq_len + 1)), list(plddt_avg)


def compute_plddt(pathogen, struct_name, ref_seq):
    """Compute pLDDT via ESMFold API."""
    out_path = os.path.join(STRUCT_DIR, f"{struct_name}_plddt.csv")
    if os.path.exists(out_path):
        print(f"    pLDDT already computed: {out_path}")
        return pd.read_csv(out_path)

    print(f"    Computing pLDDT for {pathogen} ({len(ref_seq)}aa)...")
    positions, plddts = esmfold_api_chunk(ref_seq)
    if positions is None:
        print(f"    FAILED to get pLDDT")
        return None

    df = pd.DataFrame({
        "position": positions,
        "pLDDT": [round(p, 2) for p in plddts],
    })
    df.to_csv(out_path, index=False)
    print(f"    Saved: {out_path}, mean={np.mean(plddts):.1f}")
    return df


# ── Feature 7: SASA ─────────────────────────────────────────────────────
def compute_sasa(pathogen, struct_name, ref_seq):
    """Compute per-residue SASA/RSA via ESMFold + BioPython ShrakeRupley."""
    import requests
    from Bio.PDB import PDBParser
    from Bio.PDB.SASA import ShrakeRupley
    from Bio.Data.IUPACData import protein_letters_3to1

    out_path = os.path.join(STRUCT_DIR, f"{struct_name}_sasa.csv")
    if os.path.exists(out_path):
        print(f"    SASA already computed: {out_path}")
        return pd.read_csv(out_path)

    pdb_path = os.path.join(PDB_DIR, f"{struct_name}.pdb")
    seq_len = len(ref_seq)

    # Get PDB structure via ESMFold
    if not os.path.exists(pdb_path):
        print(f"    Folding with ESMFold for SASA ({seq_len}aa)...")
        chunk_size = 400
        overlap = 50

        if seq_len <= chunk_size:
            # Single call
            for attempt in range(3):
                try:
                    r = requests.post(
                        "https://api.esmatlas.com/foldSequence/v1/pdb/",
                        data=ref_seq,
                        timeout=300,
                    )
                    if r.status_code == 200:
                        with open(pdb_path, "w") as f:
                            f.write(r.text)
                        print(f"    Folded OK: {seq_len}aa")
                        break
                    else:
                        print(f"    HTTP {r.status_code}, attempt {attempt+1}/3")
                        time.sleep(15 * (attempt + 1))
                except Exception as e:
                    print(f"    Error: {e}, attempt {attempt+1}/3")
                    time.sleep(15 * (attempt + 1))
            else:
                print(f"    FAILED to fold for SASA")
                return None
        else:
            # Chunked folding
            chunks = []
            start = 0
            while start < seq_len:
                end = min(start + chunk_size, seq_len)
                chunks.append((start, end))
                if end == seq_len:
                    break
                start = end - overlap

            all_pdb_lines = []
            atom_counter = 0
            for i, (start, end) in enumerate(chunks):
                chunk_seq = ref_seq[start:end]
                print(f"      SASA Chunk {i+1}/{len(chunks)}: pos {start+1}-{end}", end="")
                success = False
                for attempt in range(3):
                    try:
                        r = requests.post(
                            "https://api.esmatlas.com/foldSequence/v1/pdb/",
                            data=chunk_seq,
                            timeout=300,
                        )
                        if r.status_code == 200:
                            for line in r.text.split("\n"):
                                if line.startswith("ATOM"):
                                    resnum = int(line[22:26].strip())
                                    if i > 0 and resnum <= overlap:
                                        continue
                                    new_resnum = resnum + start
                                    atom_counter += 1
                                    new_line = (
                                        line[:6] + f"{atom_counter:5d}" +
                                        line[11:22] + f"{new_resnum:4d}" + line[26:]
                                    )
                                    all_pdb_lines.append(new_line)
                            print(f" -> OK")
                            success = True
                            break
                        else:
                            print(f" -> {r.status_code}", end="")
                            time.sleep(15 * (attempt + 1))
                    except Exception as e:
                        print(f" -> {e}", end="")
                        time.sleep(15 * (attempt + 1))
                if not success:
                    print(f" FAILED")
                    return None
                if i < len(chunks) - 1:
                    time.sleep(3)

            with open(pdb_path, "w") as f:
                f.write("\n".join(all_pdb_lines) + "\nEND\n")

    # Compute SASA from PDB
    parser = PDBParser(QUIET=True)
    structure = parser.get_structure("protein", pdb_path)
    model = structure[0]
    sr = ShrakeRupley()
    sr.compute(model, level="R")

    positions = []
    sasa_values = []
    rsa_values = []

    for chain in model:
        for residue in chain:
            if residue.id[0] != ' ':
                continue
            resname = residue.get_resname()
            try:
                aa1 = protein_letters_3to1.get(resname.capitalize(), 'X')
            except:
                aa1 = 'X'

            resnum = residue.id[1]
            sasa = residue.sasa
            max_asa = MAX_ASA.get(aa1.upper(), 200)
            rsa = min(sasa / max_asa, 1.0) if max_asa > 0 else 0.0

            positions.append(resnum)
            sasa_values.append(round(sasa, 2))
            rsa_values.append(round(rsa, 4))

    df = pd.DataFrame({"position": positions, "SASA": sasa_values, "RSA": rsa_values})
    df.to_csv(out_path, index=False)
    print(f"    Saved SASA: {out_path} ({len(df)} residues), mean RSA={df['RSA'].mean():.3f}")
    return df


# ── Feature 8: Grantham ─────────────────────────────────────────────────
def get_grantham(aa1, aa2):
    if aa1 == aa2:
        return 0
    key = (aa1, aa2)
    if key in GRANTHAM:
        return GRANTHAM[key]
    key = (aa2, aa1)
    if key in GRANTHAM:
        return GRANTHAM[key]
    return np.nan


def compute_grantham(pathogen, msa):
    out_path = os.path.join(FEATURE_DIR, f"{pathogen}_grantham.csv")
    if os.path.exists(out_path):
        print(f"    Grantham already computed: {out_path}")
        return pd.read_csv(out_path)

    n_seqs, seq_len = msa.shape
    scores = np.zeros(seq_len)

    for pos in range(seq_len):
        col = msa[:, pos]
        counts = Counter(c for c in col if c in VALID_AA)
        if not counts:
            continue
        consensus = max(counts, key=counts.get)
        weighted_sum = 0.0
        weight_total = 0.0
        for aa, count in counts.items():
            if aa == consensus:
                continue
            g = get_grantham(consensus, aa)
            if not np.isnan(g):
                weighted_sum += g * count
                weight_total += count
        if weight_total > 0:
            scores[pos] = weighted_sum / weight_total

    df = pd.DataFrame({"position": np.arange(len(scores)), "grantham": scores})
    df.to_csv(out_path, index=False)
    print(f"    Saved Grantham: {out_path}, mean={scores.mean():.2f}, max={scores.max():.1f}")
    return df


# ── Feature 9: dN/dS proxy ──────────────────────────────────────────────
def compute_dnds(pathogen, msa):
    out_path = os.path.join(FEATURE_DIR, f"{pathogen}_dnds.csv")
    if os.path.exists(out_path):
        print(f"    dN/dS already computed: {out_path}")
        return pd.read_csv(out_path)

    n_seqs, seq_len = msa.shape
    sub_rates = np.zeros(seq_len)
    syn_capacity = np.zeros(seq_len)

    for pos in range(seq_len):
        col = msa[:, pos]
        counts = Counter(c for c in col if c in VALID_AA)
        if not counts:
            continue
        total = sum(counts.values())
        consensus = max(counts, key=counts.get)
        consensus_freq = counts[consensus] / total
        sub_rates[pos] = 1.0 - consensus_freq
        syn_capacity[pos] = CODON_DEGENERACY.get(consensus, 1)

    mean_rate = sub_rates[sub_rates > 0].mean() if np.any(sub_rates > 0) else 1.0
    dnds_proxy = np.zeros(seq_len)

    for pos in range(seq_len):
        if sub_rates[pos] == 0:
            continue
        n_codons = syn_capacity[pos]
        nonsyn_fraction = 1.0 - (n_codons - 1) / 9.0
        expected = mean_rate * nonsyn_fraction
        if expected > 0:
            dnds_proxy[pos] = sub_rates[pos] / expected
        else:
            dnds_proxy[pos] = sub_rates[pos] / mean_rate if mean_rate > 0 else 0

    df = pd.DataFrame({
        "position": np.arange(len(dnds_proxy)),
        "dnds_proxy": np.round(dnds_proxy, 4),
    })
    df.to_csv(out_path, index=False)
    above1 = np.sum(dnds_proxy > 1.0)
    print(f"    Saved dN/dS: {out_path}, mean={dnds_proxy.mean():.3f}, dN/dS>1: {above1}/{seq_len}")
    return df


# ── Feature 10: semantic change ──────────────────────────────────────────
def compute_semantic(pathogen, msa, consensus_seq, model, alphabet, batch_converter, device):
    """Compute per-position semantic change using ESM-2 embeddings."""
    import torch

    out_path = os.path.join(FEATURE_DIR, f"{pathogen}_semantic_change.csv")
    if os.path.exists(out_path):
        print(f"    Semantic change already computed: {out_path}")
        return pd.read_csv(out_path)

    seq_len = len(consensus_seq)
    print(f"    Computing semantic change ({seq_len} positions)...")

    # Get wild-type embedding
    wt_data = [("wt", consensus_seq)]
    _, _, wt_tokens = batch_converter(wt_data)
    wt_tokens = wt_tokens.to(device)
    with torch.no_grad():
        wt_result = model(wt_tokens, repr_layers=[33])
    wt_repr = wt_result["representations"][33][0, 1:-1, :].cpu()

    semantic_scores = np.zeros(seq_len)
    batch_size = 20

    for pos in range(seq_len):
        col = msa[:, pos]
        counts = Counter(c for c in col if c in VALID_AA)
        wt_aa = consensus_seq[pos]
        variants = {aa: count for aa, count in counts.items() if aa != wt_aa}
        if not variants:
            continue

        total_count = sum(counts.values())
        variant_seqs = []
        variant_weights = []
        for var_aa, count in variants.items():
            mut_seq = consensus_seq[:pos] + var_aa + consensus_seq[pos+1:]
            variant_seqs.append(("mut", mut_seq))
            variant_weights.append(count / total_count)

        cosine_dists = []
        weights = []

        for batch_start in range(0, len(variant_seqs), batch_size):
            batch = variant_seqs[batch_start:batch_start + batch_size]
            batch_w = variant_weights[batch_start:batch_start + batch_size]
            _, _, mut_tokens = batch_converter(batch)
            mut_tokens = mut_tokens.to(device)
            with torch.no_grad():
                mut_result = model(mut_tokens, repr_layers=[33])
            mut_repr = mut_result["representations"][33][:, 1:-1, :]
            for j in range(len(batch)):
                wt_vec = wt_repr[pos]
                mut_vec = mut_repr[j, pos, :].cpu()
                cos_sim = torch.nn.functional.cosine_similarity(
                    wt_vec.unsqueeze(0), mut_vec.unsqueeze(0)
                ).item()
                cosine_dists.append(1.0 - cos_sim)
                weights.append(batch_w[j])

        if cosine_dists:
            w = np.array(weights)
            w = w / w.sum()
            semantic_scores[pos] = np.average(cosine_dists, weights=w)

        if (pos + 1) % 100 == 0:
            print(f"      Position {pos+1}/{seq_len}")

    df = pd.DataFrame({
        "position": np.arange(len(semantic_scores)),
        "semantic_change": np.round(semantic_scores, 6),
    })
    df.to_csv(out_path, index=False)
    nonzero = np.sum(semantic_scores > 0)
    print(f"    Saved semantic: {out_path}, mean={semantic_scores.mean():.4f}, nonzero={nonzero}/{seq_len}")

    torch.cuda.empty_cache()
    gc.collect()
    return df


# ── Build feature matrix and compute AUC ─────────────────────────────────
def load_homoplasy_arr(path):
    df = pd.read_csv(path)
    max_pos = df["position"].max() + 1
    arr = np.zeros(max_pos)
    arr[df["position"].values] = df["normalized_score"].values
    return arr


def load_plddt_arr(path):
    df = pd.read_csv(path)
    min_pos = df["position"].min()
    if min_pos >= 1:
        positions = df["position"].values - 1
    else:
        positions = df["position"].values
    max_pos = positions.max() + 1
    arr = np.full(max_pos, np.nan)
    arr[positions] = df["pLDDT"].values
    return arr


def load_sasa_arr(path):
    df = pd.read_csv(path)
    min_pos = df["position"].min()
    if min_pos >= 1:
        positions = df["position"].values - 1
    else:
        positions = df["position"].values
    max_pos = positions.max() + 1
    arr = np.full(max_pos, np.nan)
    arr[positions] = df["RSA"].values
    return arr


def build_feature_matrix_and_auc(pathogen, cfg, msa_len):
    """Build feature matrix and compute per-feature AUC."""
    struct_name = cfg["struct_name"]

    # Load all features
    freq_path = None  # computed inline from MSA
    hom_path = os.path.join(HOMOPLASY_DIR, f"{pathogen}_homoplasy.csv")
    esm_path = os.path.join(ESM_DIR, f"{pathogen}_esm_llr.npy")
    plddt_path = os.path.join(STRUCT_DIR, f"{struct_name}_plddt.csv")
    sasa_path = os.path.join(STRUCT_DIR, f"{struct_name}_sasa.csv")
    grantham_path = os.path.join(FEATURE_DIR, f"{pathogen}_grantham.csv")
    dnds_path = os.path.join(FEATURE_DIR, f"{pathogen}_dnds.csv")
    semantic_path = os.path.join(FEATURE_DIR, f"{pathogen}_semantic_change.csv")

    fasta_path = os.path.join(PROJECT_ROOT, cfg["fasta"])
    msa = parse_msa(fasta_path)
    seq_len = msa.shape[1]
    freq, entropy, rare_freq = compute_freq_entropy(msa)

    lengths = {"msa": seq_len}

    # Load homoplasy
    homoplasy = None
    if os.path.exists(hom_path):
        homoplasy = load_homoplasy_arr(hom_path)
        lengths["homoplasy"] = len(homoplasy)

    # Load ESM
    esm_arr = None
    if os.path.exists(esm_path):
        esm_arr = np.load(esm_path)
        lengths["esm"] = len(esm_arr)

    # Load pLDDT
    plddt = None
    if os.path.exists(plddt_path):
        plddt = load_plddt_arr(plddt_path)
        lengths["plddt"] = len(plddt)

    # Load SASA
    sasa = None
    if os.path.exists(sasa_path):
        sasa = load_sasa_arr(sasa_path)
        lengths["sasa"] = len(sasa)

    # Load grantham
    grantham = None
    if os.path.exists(grantham_path):
        gdf = pd.read_csv(grantham_path)
        grantham = gdf["grantham"].values
        lengths["grantham"] = len(grantham)

    # Load dnds
    dnds = None
    if os.path.exists(dnds_path):
        ddf = pd.read_csv(dnds_path)
        dnds = ddf["dnds_proxy"].values
        lengths["dnds"] = len(dnds)

    # Load semantic
    semantic = None
    if os.path.exists(semantic_path):
        sdf = pd.read_csv(semantic_path)
        semantic = sdf["semantic_change"].values
        lengths["semantic"] = len(semantic)

    min_len = min(lengths.values())
    print(f"  Lengths: {lengths} -> using min_len={min_len}")

    # Get Layer A ground truth
    layer_a_set = get_gt_adaptive(pathogen, min_len)
    layer_a = np.zeros(min_len, dtype=int)
    for p in layer_a_set:
        if p < min_len:
            layer_a[p] = 1

    # Build DataFrame
    df = pd.DataFrame({
        "position": np.arange(min_len),
        "freq": freq[:min_len],
        "entropy": entropy[:min_len],
        "rare_freq": rare_freq[:min_len],
    })

    if homoplasy is not None:
        df["homoplasy"] = homoplasy[:min_len]
    if esm_arr is not None:
        df["esm2_llr"] = esm_arr[:min_len]
    if plddt is not None:
        df["plddt"] = plddt[:min_len]
    if sasa is not None:
        df["sasa"] = sasa[:min_len]
    if grantham is not None:
        df["grantham"] = grantham[:min_len]
    if dnds is not None:
        df["dnds_proxy"] = dnds[:min_len]
    if semantic is not None:
        df["semantic_change"] = semantic[:min_len]

    df["layer_a"] = layer_a

    # Save feature matrix
    out_path = os.path.join(FEATURE_DIR, f"feature_matrix_{pathogen}.csv")
    df.to_csv(out_path, index=False)
    print(f"  Saved feature matrix: {out_path} ({len(df)} positions, {int(layer_a.sum())} Layer A)")

    # Compute AUC
    features = [c for c in df.columns if c not in ("position", "layer_a")]
    y = df["layer_a"].values
    n_pos = int(y.sum())

    auc_results = []
    if n_pos > 0 and n_pos < len(y):
        for feat in features:
            x = df[feat].values
            mask = ~np.isnan(x)
            x_clean = x[mask]
            y_clean = y[mask]
            if len(np.unique(y_clean)) < 2:
                continue
            try:
                auc = roc_auc_score(y_clean, x_clean)
            except ValueError:
                auc = np.nan
            rho, p_val = spearmanr(x_clean, y_clean)
            auc_results.append({
                "pathogen": pathogen,
                "feature": feat,
                "auc": round(auc, 4),
                "spearman_rho": round(rho, 4),
                "p_value": round(p_val, 6) if p_val is not None else np.nan,
                "n_positions": len(y_clean),
                "n_layer_a": int(y_clean.sum()),
            })

    return df, auc_results


# ── Main ─────────────────────────────────────────────────────────────────
def main():
    import torch

    print("=" * 70)
    print("Computing all 10 features for 3 new viruses")
    print("=" * 70)

    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    print(f"Device: {device}")
    if device.type == "cuda":
        print(f"  GPU: {torch.cuda.get_device_name(0)}")
        print(f"  Memory: {torch.cuda.get_device_properties(0).total_mem / 1e9:.1f} GB"
              if hasattr(torch.cuda.get_device_properties(0), 'total_mem')
              else f"  Memory: {torch.cuda.get_device_properties(0).total_memory / 1e9:.1f} GB")

    # ── Phase 1: MSA-based features (freq, entropy, rare_freq, grantham, dnds) ──
    print("\n" + "=" * 70)
    print("PHASE 1: MSA-based features")
    print("=" * 70)

    msa_data = {}
    consensus_data = {}

    for pathogen, cfg in NEW_PATHOGENS.items():
        print(f"\n--- {pathogen} ---")
        fasta_path = os.path.join(PROJECT_ROOT, cfg["fasta"])
        msa = parse_msa(fasta_path)
        msa_data[pathogen] = msa
        consensus = get_consensus(msa)
        consensus_data[pathogen] = consensus
        print(f"    MSA shape: {msa.shape}, consensus: {len(consensus)}aa")

        # Compute MSA-based features
        compute_grantham(pathogen, msa)
        compute_dnds(pathogen, msa)

    # ── Phase 2: Homoplasy ──
    print("\n" + "=" * 70)
    print("PHASE 2: Homoplasy (Fitch parsimony)")
    print("=" * 70)

    for pathogen, cfg in NEW_PATHOGENS.items():
        print(f"\n--- {pathogen} ---")
        fasta_path = os.path.join(PROJECT_ROOT, cfg["fasta"])
        compute_homoplasy(pathogen, fasta_path)

    # ── Phase 3: ESM-2 features (LLR + semantic change) ──
    print("\n" + "=" * 70)
    print("PHASE 3: ESM-2 features (LLR + semantic change)")
    print("=" * 70)

    print("\nLoading ESM-2 model (esm2_t33_650M_UR50D)...")
    import esm
    esm_model, esm_alphabet = esm.pretrained.esm2_t33_650M_UR50D()
    esm_batch_converter = esm_alphabet.get_batch_converter()
    esm_model = esm_model.to(device)
    esm_model.eval()
    print("  Model loaded!")

    for pathogen, cfg in NEW_PATHOGENS.items():
        print(f"\n--- {pathogen} ---")
        consensus = consensus_data[pathogen]
        msa = msa_data[pathogen]

        # ESM-2 LLR
        compute_esm_llr(pathogen, consensus, esm_model, esm_alphabet, esm_batch_converter, device)

        # Semantic change
        compute_semantic(pathogen, msa, consensus, esm_model, esm_alphabet, esm_batch_converter, device)

    # Free ESM model memory
    del esm_model
    torch.cuda.empty_cache()
    gc.collect()
    print("\n  ESM-2 model freed from GPU memory")

    # ── Phase 4: Structural features (pLDDT, SASA via ESMFold API) ──
    print("\n" + "=" * 70)
    print("PHASE 4: Structural features (pLDDT, SASA)")
    print("=" * 70)

    for pathogen, cfg in NEW_PATHOGENS.items():
        print(f"\n--- {pathogen} ---")
        fasta_path = os.path.join(PROJECT_ROOT, cfg["fasta"])
        ref_seq = get_reference_sequence(fasta_path)
        struct_name = cfg["struct_name"]

        compute_plddt(pathogen, struct_name, ref_seq)
        time.sleep(2)
        compute_sasa(pathogen, struct_name, ref_seq)
        time.sleep(2)

    # ── Phase 5: Build feature matrices and compute AUC ──
    print("\n" + "=" * 70)
    print("PHASE 5: Building feature matrices and computing AUC")
    print("=" * 70)

    all_auc_results = []

    for pathogen, cfg in NEW_PATHOGENS.items():
        print(f"\n--- {pathogen} ---")
        msa = msa_data[pathogen]
        df, auc_results = build_feature_matrix_and_auc(pathogen, cfg, msa.shape[1])
        all_auc_results.extend(auc_results)

    # Save AUC results
    if all_auc_results:
        new_auc_df = pd.DataFrame(all_auc_results)
        print(f"\n  New AUC results ({len(new_auc_df)} rows):")
        print(new_auc_df.to_string(index=False))

        # Append to existing per_feature_auc_v2.csv
        auc_v2_path = os.path.join(FEATURE_DIR, "per_feature_auc_v2.csv")
        if os.path.exists(auc_v2_path):
            existing_auc = pd.read_csv(auc_v2_path)
            # Remove any existing entries for these pathogens
            existing_auc = existing_auc[~existing_auc["pathogen"].isin(NEW_PATHOGENS.keys())]
            combined = pd.concat([existing_auc, new_auc_df], ignore_index=True)
        else:
            combined = new_auc_df
        combined.to_csv(auc_v2_path, index=False)
        print(f"\n  Updated: {auc_v2_path} ({len(combined)} total rows)")

        # Print summary pivot
        pivot = new_auc_df.pivot_table(index="pathogen", columns="feature", values="auc")
        feat_order = ["freq", "entropy", "rare_freq", "homoplasy", "esm2_llr",
                       "plddt", "sasa", "grantham", "dnds_proxy", "semantic_change"]
        feat_order = [f for f in feat_order if f in pivot.columns]
        pivot = pivot[feat_order]
        print(f"\n  AUC Summary:")
        print(pivot.to_string(float_format=lambda x: f"{x:.3f}"))

    print("\n" + "=" * 70)
    print("ALL DONE!")
    print("=" * 70)


if __name__ == "__main__":
    main()
