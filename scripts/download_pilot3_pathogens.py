#!/usr/bin/env python3
"""Download surface-glycoprotein sequences for pilot 3 pathogens:

  - Yellow Fever virus (envelope E)
  - Lassa virus (glycoprotein precursor GPC)
  - West Nile virus (envelope E)

Mirrors the NCBI Entrez pattern in data/download_ncbi_sequences.py.
"""

import time
from io import StringIO
from Bio import Entrez, SeqIO

Entrez.email = "mutbench@example.com"

VIRUSES = [
    {
        "name": "Yellow Fever virus E protein",
        "search_term": 'txid11089[Organism] AND (envelope OR "E protein" OR polyprotein)',
        "output": "/proj/paper/data/yfv/yfv_e_sequences.fasta",
        "min_len": 480,
        "max_len": 510,
    },
    {
        "name": "Lassa virus GPC",
        "search_term": 'txid11620[Organism] AND (glycoprotein OR GPC OR "preglycoprotein")',
        "output": "/proj/paper/data/lassa/lassa_gpc_sequences.fasta",
        "min_len": 480,
        "max_len": 530,
    },
    {
        "name": "West Nile virus E protein",
        "search_term": 'txid11082[Organism] AND (envelope OR "E protein" OR polyprotein)',
        "output": "/proj/paper/data/wnv/wnv_e_sequences.fasta",
        "min_len": 490,
        "max_len": 510,
    },
]

BATCH_SIZE = 500
MAX_SEQS = 5000


def download_virus(virus):
    name = virus["name"]
    print(f"\n{'=' * 60}\n{name}\n{'=' * 60}")
    handle = Entrez.esearch(
        db="protein", term=virus["search_term"], retmax=MAX_SEQS, usehistory="y"
    )
    results = Entrez.read(handle)
    handle.close()
    total = int(results["Count"])
    print(f"  Found {total} candidates; downloading up to {MAX_SEQS}")
    if total == 0:
        print("  No hits.")
        return

    webenv = results["WebEnv"]
    query_key = results["QueryKey"]
    records = []
    for start in range(0, min(total, MAX_SEQS), BATCH_SIZE):
        attempts = 0
        while attempts < 3:
            try:
                fetch = Entrez.efetch(
                    db="protein",
                    rettype="fasta",
                    retmode="text",
                    retstart=start,
                    retmax=BATCH_SIZE,
                    webenv=webenv,
                    query_key=query_key,
                )
                data = fetch.read()
                fetch.close()
                batch = list(SeqIO.parse(StringIO(data), "fasta"))
                records.extend(batch)
                print(f"    fetched {start}..{start + len(batch)}")
                break
            except Exception as e:
                attempts += 1
                print(f"    retry {attempts}: {e}")
                time.sleep(5)
        time.sleep(0.5)

    print(f"  Total fetched: {len(records)}")
    keep = [
        r
        for r in records
        if virus["min_len"] <= len(r.seq) <= virus["max_len"]
        and "X" not in str(r.seq)
    ]
    print(f"  Length-filtered ({virus['min_len']}-{virus['max_len']}): {len(keep)}")

    import os

    os.makedirs(os.path.dirname(virus["output"]), exist_ok=True)
    with open(virus["output"], "w") as f:
        SeqIO.write(keep, f, "fasta")
    print(f"  Wrote {virus['output']}")


def main():
    for v in VIRUSES:
        try:
            download_virus(v)
        except Exception as e:
            print(f"  FAILED: {e}")
        time.sleep(1)


if __name__ == "__main__":
    main()
