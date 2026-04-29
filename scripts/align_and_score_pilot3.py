#!/usr/bin/env python3
"""Align pilot 3 pathogen sequences and compute basic position-level scores.

Outputs (per pathogen):
  data/<name>/<protein>_aligned.fasta         (MAFFT --auto, modal length keep)
  data/cross_pathogen/<protein>_position_scores.csv  (position, frequency, entropy, hscore)

The CSV schema matches data/cross_pathogen/dengue_e_position_scores.csv so
downstream stage3 / feature-ablation pipelines work without modification.
The 'ground_truth' column is filled with -1 (unknown) until Layer A is curated.
"""

import math
import subprocess
from collections import Counter
from pathlib import Path

from Bio import SeqIO

PILOTS = [
    ("yfv", "yfv_e", "/proj/paper/data/yfv/yfv_e_sequences.fasta"),
    ("lassa", "lassa_gpc", "/proj/paper/data/lassa/lassa_gpc_sequences.fasta"),
    ("wnv", "wnv_e", "/proj/paper/data/wnv/wnv_e_sequences.fasta"),
]

OUT_CROSS = Path("/proj/paper/data/cross_pathogen")
OUT_CROSS.mkdir(exist_ok=True, parents=True)

AA20 = list("ACDEFGHIKLMNPQRSTVWY")
GAP = "-"


def shannon_entropy(counts, total):
    if total == 0:
        return 0.0
    H = 0.0
    for v in counts.values():
        if v > 0:
            p = v / total
            H -= p * math.log2(p)
    return H


def mafft_align(in_fasta, out_fasta):
    print(f"  aligning -> {out_fasta}")
    with open(out_fasta, "w") as fo:
        subprocess.run(
            ["mafft", "--auto", "--thread", "4", "--quiet", str(in_fasta)],
            stdout=fo, check=True,
        )


def keep_modal_length(records):
    lengths = [len(r.seq) for r in records]
    if not lengths:
        return []
    modal = max(set(lengths), key=lengths.count)
    keep = [r for r in records if len(r.seq) == modal]
    return keep


def per_position_scores(msa_file):
    seqs = [str(r.seq).upper() for r in SeqIO.parse(msa_file, "fasta")]
    n = len(seqs)
    if n == 0:
        return None, 0, 0
    L = len(seqs[0])
    rows = []
    for i in range(L):
        col = [s[i] for s in seqs]
        c_all = Counter(col)
        c_aa = {a: c_all.get(a, 0) for a in AA20 if c_all.get(a, 0) > 0}
        n_aa = sum(c_aa.values())
        if n_aa == 0:
            rows.append((i + 1, 0.0, 0.0, 0.0, -1))
            continue
        consensus = max(c_aa.items(), key=lambda kv: kv[1])[0]
        n_non_consensus = n_aa - c_aa.get(consensus, 0)
        freq = n_non_consensus / n_aa
        H = shannon_entropy(c_aa, n_aa)
        # H-score proxy: entropy * non-consensus frequency * 10 (scales similarly to existing CSVs)
        hscore = H * freq * 10.0
        rows.append((i + 1, round(freq, 6), round(H, 6), round(hscore, 6), -1))
    return rows, n, L


def main():
    print(f"=== Pilot 3 alignment + scoring ===\n")
    summary_lines = []
    for short, slug, fasta in PILOTS:
        print(f"\n--- {slug} ---")
        records = list(SeqIO.parse(fasta, "fasta"))
        kept = keep_modal_length(records)
        print(f"  raw: {len(records)} sequences; modal-length kept: {len(kept)}")
        modal_in = Path(f"/proj/paper/data/{short}/{slug}_modal.fasta")
        modal_in.parent.mkdir(exist_ok=True, parents=True)
        SeqIO.write(kept, modal_in, "fasta")

        aln = Path(f"/proj/paper/data/{short}/{slug}_aligned.fasta")
        if not aln.exists() or aln.stat().st_size == 0:
            mafft_align(modal_in, aln)
        else:
            print(f"  alignment cached: {aln}")

        rows, n, L = per_position_scores(aln)
        if rows is None:
            summary_lines.append(f"{slug}: SKIPPED (0 sequences)")
            continue
        out = OUT_CROSS / f"{slug}_position_scores.csv"
        with open(out, "w") as fo:
            fo.write("position,frequency,entropy,hscore,ground_truth\n")
            for r in rows:
                fo.write(",".join(str(x) for x in r) + "\n")
        print(f"  wrote {out} ({L} positions)")
        summary_lines.append(f"{slug}: n_seq={n}, L={L}, csv={out.name}")

    print("\n=== Summary ===")
    for s in summary_lines:
        print("  " + s)


if __name__ == "__main__":
    main()
