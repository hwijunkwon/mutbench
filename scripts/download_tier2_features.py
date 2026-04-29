#!/usr/bin/env python3
"""Tier 2 features-only download: 19 surface-glycoprotein targets.

Reads scripts/pathogen_scaling_targets.json, downloads protein FASTAs from
NCBI Entrez, length-filters, runs MAFFT alignment, and writes
data/cross_pathogen/<slug>_position_scores.csv with the same schema as the
canonical 11-pathogen panel.

Layer A is intentionally not curated for Tier 2 — the goal is to expose the
features pipeline at n=30 and let downstream Cycle 7B test the panel-size
hypothesis without the manual-curation bottleneck.

Robust to NCBI rate limits via per-batch retries and a 2-minute soft timeout.
"""

import json
import math
import os
import signal
import subprocess
import sys
import time
from collections import Counter
from io import StringIO
from pathlib import Path

from Bio import Entrez, SeqIO

Entrez.email = "mutbench@example.com"

REGISTRY = Path("/proj/paper/scripts/pathogen_scaling_targets.json")
OUT_DIR = Path("/proj/paper/data/cross_pathogen")
OUT_DIR.mkdir(exist_ok=True, parents=True)
WORK_DIR = Path("/proj/paper/data/tier2")
WORK_DIR.mkdir(exist_ok=True, parents=True)

AA20 = list("ACDEFGHIKLMNPQRSTVWY")
PER_TERM_CAP = 800           # cap per Entrez term — stay under rate limits
BATCH = 200
PER_TARGET_TIMEOUT = 120     # seconds


class Timeout(Exception):
    pass


def _alarm(_signum, _frame):
    raise Timeout()


def slug(name):
    return (
        name.lower()
        .replace(" ", "_")
        .replace("(", "")
        .replace(")", "")
        .replace("/", "_")
        .replace(",", "")
    )


def fetch_protein(taxid, expected_len):
    """Pull up to PER_TERM_CAP hits, length-filter, dedupe."""
    terms = [
        f'txid{taxid}[Organism] AND envelope',
        f'txid{taxid}[Organism] AND glycoprotein',
        f'txid{taxid}[Organism] AND haemagglutinin',
        f'txid{taxid}[Organism] AND spike',
        f'txid{taxid}[Organism] AND capsid',
    ]
    seen = {}
    for term in terms:
        try:
            h = Entrez.esearch(db="protein", term=term, retmax=PER_TERM_CAP, usehistory="y")
            r = Entrez.read(h)
            h.close()
            total = int(r["Count"])
            if total == 0:
                continue
            cap = min(total, PER_TERM_CAP)
            for start in range(0, cap, BATCH):
                for attempt in range(3):
                    try:
                        f = Entrez.efetch(
                            db="protein", rettype="fasta", retmode="text",
                            retstart=start, retmax=BATCH,
                            webenv=r["WebEnv"], query_key=r["QueryKey"],
                        )
                        data = f.read()
                        f.close()
                        for rec in SeqIO.parse(StringIO(data), "fasta"):
                            if rec.id not in seen:
                                seen[rec.id] = rec
                        break
                    except Exception as e:
                        print(f"      retry {attempt + 1}: {e}")
                        time.sleep(3)
                time.sleep(0.4)
        except Exception as e:
            print(f"    term failed ({term[:40]}): {e}")
            continue
    keep = [
        rec for rec in seen.values()
        if expected_len[0] <= len(rec.seq) <= expected_len[1]
        and "X" not in str(rec.seq)
    ]
    return keep


def shannon_entropy(counts, total):
    if total == 0:
        return 0.0
    H = 0.0
    for v in counts.values():
        if v > 0:
            p = v / total
            H -= p * math.log2(p)
    return H


def mafft(in_path, out_path):
    with open(out_path, "w") as fo:
        subprocess.run(
            ["mafft", "--auto", "--thread", "4", "--quiet", str(in_path)],
            stdout=fo, check=True,
        )


def per_position(msa_file):
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
        freq = (n_aa - c_aa.get(consensus, 0)) / n_aa
        H = shannon_entropy(c_aa, n_aa)
        hscore = H * freq * 10.0
        rows.append((i + 1, round(freq, 6), round(H, 6), round(hscore, 6), -1))
    return rows, n, L


def process_one(target):
    name = target["name"]
    taxid = target["taxid"]
    expected_len = target["expected_len"]
    s = slug(name)
    fasta = WORK_DIR / f"{s}.fasta"
    aligned = WORK_DIR / f"{s}_aligned.fasta"
    csv_out = OUT_DIR / f"{s}_position_scores.csv"
    if csv_out.exists():
        print(f"  CACHED {csv_out.name}")
        # Re-derive n,L from cached aligned FASTA so reruns do not lose the
        # informative summary numbers from the first build.
        n_cached = L_cached = None
        if aligned.exists():
            seqs_cached = list(SeqIO.parse(aligned, "fasta"))
            if seqs_cached:
                n_cached = len(seqs_cached)
                L_cached = len(seqs_cached[0].seq)
        return {"slug": s, "status": "cached", "n": n_cached, "L": L_cached}

    signal.signal(signal.SIGALRM, _alarm)
    signal.alarm(PER_TARGET_TIMEOUT)
    try:
        records = fetch_protein(taxid, expected_len)
    except Timeout:
        print(f"  TIMEOUT fetching {name}")
        return {"slug": s, "status": "timeout"}
    except Exception as e:
        print(f"  FETCH failed ({name}): {e}")
        return {"slug": s, "status": "fetch_error"}
    finally:
        signal.alarm(0)

    print(f"  {name}: {len(records)} length-filtered records")
    if len(records) < 30:
        print(f"  SKIP {name} — too few sequences ({len(records)} < 30)")
        SeqIO.write(records, fasta, "fasta")
        return {"slug": s, "status": "low_n", "n_raw": len(records)}

    SeqIO.write(records, fasta, "fasta")
    try:
        mafft(fasta, aligned)
    except Exception as e:
        print(f"  MAFFT failed ({name}): {e}")
        return {"slug": s, "status": "mafft_error"}

    rows, n, L = per_position(aligned)
    if rows is None:
        return {"slug": s, "status": "score_error"}

    with open(csv_out, "w") as fo:
        fo.write("position,frequency,entropy,hscore,ground_truth\n")
        for r in rows:
            fo.write(",".join(str(x) for x in r) + "\n")
    print(f"  WROTE {csv_out.name} (n={n}, L={L})")
    return {"slug": s, "status": "ok", "n": n, "L": L}


def main():
    reg = json.loads(REGISTRY.read_text())
    targets = reg["tier2_features_only"]
    summary = []
    print(f"Processing {len(targets)} Tier 2 targets...")
    for t in targets:
        print(f"\n=== {t['name']} (taxid {t['taxid']}) ===")
        result = process_one(t)
        result["name"] = t["name"]
        summary.append(result)
        time.sleep(1)

    print("\n=== Tier 2 summary ===")
    ok = sum(1 for r in summary if r["status"] in ("ok", "cached"))
    print(f"  Successful: {ok}/{len(summary)}")
    for r in summary:
        line = f"  {r['name']:40s} {r['status']:>14s}"
        if r.get("n") is not None:
            line += f"  n={r['n']:>5d}  L={r['L']:>4d}"
        print(line)

    summary_path = WORK_DIR / "tier2_summary.json"
    summary_path.write_text(json.dumps(summary, indent=2))
    print(f"\nWrote {summary_path}")


if __name__ == "__main__":
    main()
