#!/usr/bin/env python3
"""Broader search for YFV E and WNV E to reach >=200 sequences.

The narrow 'envelope' search finds too few hits because most YFV/WNV
GenBank entries are deposited as polyproteins. Pull polyproteins and
slice out the E domain by length-based filter.
"""

import time
from io import StringIO
from Bio import Entrez, SeqIO

Entrez.email = "mutbench@example.com"

# YFV E is positions 286-779 of polyprotein (~493 aa)
# WNV E is positions ~291-792 of polyprotein (~501 aa)
# Lookup is fragile, so we use length filtering on full polyprotein hits
# combined with a refined envelope search.

CONFIGS = [
    {
        "name": "YFV E (broader)",
        "search_terms": [
            'txid11089[Organism] AND envelope',
            'txid11089[Organism] AND "envelope protein E"',
            'txid11089[Organism] AND "structural polyprotein"',
            '"Yellow fever virus"[Organism] AND envelope',
        ],
        "output": "/proj/paper/data/yfv/yfv_e_sequences.fasta",
        "min_len": 480,
        "max_len": 510,
    },
    {
        "name": "WNV E (broader)",
        "search_terms": [
            'txid11082[Organism] AND envelope',
            'txid11082[Organism] AND "envelope protein E"',
            '"West Nile virus"[Organism] AND envelope',
            'txid11082[Organism] AND "structural polyprotein"',
        ],
        "output": "/proj/paper/data/wnv/wnv_e_sequences.fasta",
        "min_len": 490,
        "max_len": 510,
    },
]

BATCH = 500
MAX_PER_TERM = 5000


def fetch_term(term):
    handle = Entrez.esearch(db="protein", term=term, retmax=MAX_PER_TERM, usehistory="y")
    res = Entrez.read(handle)
    handle.close()
    total = int(res["Count"])
    if total == 0:
        return []
    print(f"    {term[:55]}: {total} hits")
    out = []
    for start in range(0, min(total, MAX_PER_TERM), BATCH):
        for attempt in range(3):
            try:
                fh = Entrez.efetch(
                    db="protein", rettype="fasta", retmode="text",
                    retstart=start, retmax=BATCH,
                    webenv=res["WebEnv"], query_key=res["QueryKey"],
                )
                data = fh.read()
                fh.close()
                out.extend(list(SeqIO.parse(StringIO(data), "fasta")))
                break
            except Exception as e:
                print(f"      retry {attempt + 1}: {e}")
                time.sleep(5)
        time.sleep(0.4)
    return out


def main():
    for cfg in CONFIGS:
        print(f"\n=== {cfg['name']} ===")
        seen = {}
        for term in cfg["search_terms"]:
            try:
                recs = fetch_term(term)
            except Exception as e:
                print(f"    skip ({e})")
                continue
            for r in recs:
                if r.id not in seen:
                    seen[r.id] = r
        print(f"  unique hits: {len(seen)}")

        keep = [
            r for r in seen.values()
            if cfg["min_len"] <= len(r.seq) <= cfg["max_len"]
            and "X" not in str(r.seq)
        ]
        print(f"  length-filtered ({cfg['min_len']}-{cfg['max_len']}): {len(keep)}")

        with open(cfg["output"], "w") as f:
            SeqIO.write(keep, f, "fasta")
        print(f"  wrote {cfg['output']}")
        time.sleep(1)


if __name__ == "__main__":
    main()
