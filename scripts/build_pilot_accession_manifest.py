#!/usr/bin/env python3
"""Build a deterministic accession manifest for the v176 Tier 1 + Tier 2 pilots.

The download scripts (download_pilot3_pathogens.py, download_tier2_features.py)
issue Entrez search-and-fetch queries that depend on live NCBI state. To make
the pilots externally reproducible we extract the actual NCBI accessions from
the FASTAs that v176 fetched and emit a per-pathogen manifest with:

  - slug (matches data/cross_pathogen/<slug>_position_scores.csv)
  - n_seq_raw, n_seq_modal_kept (matches tier2_summary.json)
  - sha256 of the modal-length FASTA
  - sorted accession list (NCBI version IDs)

A third party can replay the pilot by `efetch`-ing the listed accessions and
checking the FASTA sha256 instead of re-issuing the original Entrez search.

Output:
  results/mutbench/pilot_accession_manifest.csv  (slug, n_seq_raw, n_seq_modal,
                                                  sha256_modal, query_date)
  results/mutbench/pilot_accessions/<slug>.txt   (one accession per line)
"""

import csv
import hashlib
import json
from collections import Counter
from pathlib import Path

from Bio import SeqIO

ROOT = Path("/proj/paper/data")
OUT_CSV = Path("/proj/paper/results/mutbench/pilot_accession_manifest.csv")
OUT_DIR = Path("/proj/paper/results/mutbench/pilot_accessions")
OUT_DIR.mkdir(exist_ok=True, parents=True)

QUERY_DATE = "2026-04-29"  # v176 build date (commit 5d68c42)

# (slug, raw FASTA path) — the raw FASTA is the post-length-filter, pre-modal
# file written by the download scripts. Tier 1 raw FASTAs sit in their
# pathogen subdir; Tier 2 raw FASTAs sit under data/tier2/.
SOURCES = [
    # Tier 1
    ("yfv_e",    ROOT / "yfv/yfv_e_sequences.fasta"),
    ("lassa_gpc", ROOT / "lassa/lassa_gpc_sequences.fasta"),
    ("wnv_e",    ROOT / "wnv/wnv_e_sequences.fasta"),
    # Tier 2 (only the 13 that actually built; the other 6 had n<30 and are
    # listed in tier2_summary.json with status=low_n)
    ("chikungunya_virus_e2",                    ROOT / "tier2/chikungunya_virus_e2.fasta"),
    ("japanese_encephalitis_virus_e",           ROOT / "tier2/japanese_encephalitis_virus_e.fasta"),
    ("tick-borne_encephalitis_virus_e",         ROOT / "tier2/tick-borne_encephalitis_virus_e.fasta"),
    ("eastern_equine_encephalitis_virus_e2",    ROOT / "tier2/eastern_equine_encephalitis_virus_e2.fasta"),
    ("venezuelan_equine_encephalitis_virus_e2", ROOT / "tier2/venezuelan_equine_encephalitis_virus_e2.fasta"),
    ("western_equine_encephalitis_virus_e2",    ROOT / "tier2/western_equine_encephalitis_virus_e2.fasta"),
    ("mumps_virus_hn",                          ROOT / "tier2/mumps_virus_hn.fasta"),
    ("measles_virus_h",                         ROOT / "tier2/measles_virus_h.fasta"),
    ("nipah_virus_g",                           ROOT / "tier2/nipah_virus_g.fasta"),
    ("hendra_virus_g",                          ROOT / "tier2/hendra_virus_g.fasta"),
    ("marburg_virus_gp",                        ROOT / "tier2/marburg_virus_gp.fasta"),
    ("hcov-nl63_spike",                         ROOT / "tier2/hcov-nl63_spike.fasta"),
    ("hcov-229e_spike",                         ROOT / "tier2/hcov-229e_spike.fasta"),
]


def fasta_sha256(records):
    h = hashlib.sha256()
    for r in sorted(records, key=lambda x: x.id):
        h.update(f">{r.id}\n{str(r.seq).upper()}\n".encode())
    return h.hexdigest()


def main():
    rows = []
    for slug, path in SOURCES:
        if not path.exists():
            print(f"  MISSING {path}")
            continue
        # Records here are the post-length-filter, pre-alignment FASTA
        # written by the download script; this is the deterministic reference
        # state a third party should regenerate via efetch on the listed
        # accessions and check via sha256.
        records = list(SeqIO.parse(path, "fasta"))
        accessions = sorted(r.id for r in records)

        per_target = OUT_DIR / f"{slug}.txt"
        per_target.write_text("\n".join(accessions) + ("\n" if accessions else ""))

        sha = fasta_sha256(records)
        rows.append({
            "slug": slug,
            "n_seq_filtered": len(records),
            "sha256_filtered_fasta": sha,
            "query_date": QUERY_DATE,
            "accession_list": str(per_target.relative_to(Path("/proj/paper"))),
        })
        print(f"  {slug:42s} n={len(records):>4d}  sha={sha[:12]}...")

    fields = ["slug", "n_seq_filtered", "sha256_filtered_fasta",
              "query_date", "accession_list"]
    with open(OUT_CSV, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=fields)
        w.writeheader()
        for r in rows:
            w.writerow(r)
    print(f"\nWrote {OUT_CSV} ({len(rows)} rows)")
    print(f"Per-target accession lists in {OUT_DIR}")


if __name__ == "__main__":
    main()
