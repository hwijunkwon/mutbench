#!/usr/bin/env python3
"""
Build a curated UniProt accession map for the 16 cross_pathogen targets.

For each target, we know the position_scores.csv length. We try a list of
candidate accessions per target, fetch metadata, and pick the one whose
chain length matches the CSV length (or the smallest abs(length_delta)).
Output: results/mutbench/layerA_curated_accession_map.json
"""
import csv
import json
import time
import urllib.parse
import urllib.request
from pathlib import Path

ROOT = Path("/proj/paper")
CROSS = ROOT / "data" / "cross_pathogen"
OUT = ROOT / "results" / "mutbench" / "layerA_curated_accession_map.json"

# Curated candidates per target. Multiple per target so we can pick the one
# whose effective length matches CSV. For polyprotein entries, we record the
# chain-name we expect to find.
CANDIDATES = {
    "lassa_gpc": [("P08669", None)],  # 491 (full)
    "marburg_virus_gp": [("P35253", None), ("Q1PD50", None)],  # 681 (full)
    "measles_virus_h": [("P08362", None)],  # 617 (full, CSV 620 padding)
    "mumps_virus_hn": [("P11235", None), ("Q9WAF5", None), ("P19762", None), ("P10866", None)],  # 582 (Miyahara/RW etc.)
    "hcov-229e_spike": [("P15423", None)],  # 1173 (full)
    "hcov-nl63_spike": [("Q6Q1S2", None)],  # 1356 (full)
    # Flaviviruses — polyprotein, mature E chain
    "yfv_e": [("P03314", "Envelope protein E"), ("P19901", "Envelope protein E")],
    "wnv_e": [("P06935", "Envelope protein E")],
    "japanese_encephalitis_virus_e": [("P27395", "Envelope protein E"), ("P0DOK2", "Envelope protein E")],
    "tick-borne_encephalitis_virus_e": [("P14336", "Envelope protein E")],
    # Alphaviruses — polyprotein, mature E2 chain (called Spike glycoprotein E2 or Envelope protein E2)
    "chikungunya_virus_e2": [("Q8JUX5", None), ("Q8JUX5", "E2"), ("Q8JUX5", "Envelope protein E2"), ("Q8JUX5", "Spike glycoprotein E2")],
    "eastern_equine_encephalitis_virus_e2": [("P08768", None), ("P08768", "E2"), ("P08768", "Spike glycoprotein E2")],
    "venezuelan_equine_encephalitis_virus_e2": [("P05674", None), ("P05674", "E2"), ("P05674", "Spike glycoprotein E2")],
    "western_equine_encephalitis_virus_e2": [("P13897", None), ("P13897", "E2"), ("P13897", "Spike glycoprotein E2")],
    # Henipavirus G
    "hendra_virus_g": [("O89343", None), ("O89339", None)],
    "nipah_virus_g": [("Q9IH62", None)],
}


def csv_length(slug: str) -> int:
    p = CROSS / f"{slug}_position_scores.csv"
    if not p.exists():
        return 0
    with p.open() as f:
        reader = csv.reader(f)
        next(reader)
        return sum(1 for _ in reader)


def fetch_entry(acc: str) -> dict | None:
    url = f"https://rest.uniprot.org/uniprotkb/{acc}.json"
    req = urllib.request.Request(url, headers={"User-Agent": "mb-curated/0.1"})
    try:
        with urllib.request.urlopen(req, timeout=20) as r:
            return json.loads(r.read().decode("utf-8"))
    except Exception as e:
        return {"_error": repr(e)}


def find_chain(entry: dict, chain_query: str | None) -> tuple[int, int, str] | None:
    """Find a Chain feature whose description contains chain_query (case-insensitive
    substring), or return None for full-entry use."""
    if entry.get("_error") or not entry.get("features"):
        return None
    if chain_query is None:
        ln = entry.get("sequence", {}).get("length", 0)
        return (1, ln, "(full entry)") if ln else None
    q = chain_query.lower()
    best = None
    for f in entry["features"]:
        if f.get("type") != "Chain":
            continue
        desc = (f.get("description", "") or "")
        if q in desc.lower():
            loc = f.get("location", {}) or {}
            s = (loc.get("start") or {}).get("value")
            e = (loc.get("end") or {}).get("value")
            if isinstance(s, int) and isinstance(e, int):
                if best is None or (e - s) > (best[1] - best[0]):
                    best = (s, e, desc)
    return best


def main():
    decisions = {}
    print(f"{'target':<42} {'csv_len':>7}  {'best_acc':<10} {'chain':<25} {'chain_len':>9} {'delta':>5}  {'organism':<35}")
    print("-" * 130)
    for slug, candidates in CANDIDATES.items():
        csv_len = csv_length(slug)
        best = None
        for acc, chain_q in candidates:
            entry = fetch_entry(acc)
            time.sleep(0.4)
            if not entry or entry.get("_error"):
                continue
            chain = find_chain(entry, chain_q)
            if chain is None:
                continue
            cs, ce, cdesc = chain
            chain_len = ce - cs + 1
            delta = abs(chain_len - csv_len)
            org = entry.get("organism", {}).get("scientificName", "")
            cand = {
                "uniprot_acc": acc,
                "chain_query": chain_q or "(full entry)",
                "chain_start": cs,
                "chain_end": ce,
                "chain_length": chain_len,
                "chain_description": cdesc,
                "organism": org,
                "csv_length": csv_len,
                "length_delta": delta,
            }
            if best is None or delta < best["length_delta"]:
                best = cand
        if best is None:
            print(f"{slug:<42} {csv_len:>7}  {'-':<10} {'-':<25} {0:>9} {0:>5}  -")
            decisions[slug] = {"status": "no_candidate", "csv_length": csv_len}
            continue
        status = "match" if best["length_delta"] == 0 else ("close" if best["length_delta"] <= 5 else "mismatch")
        decisions[slug] = {**best, "status": status}
        print(f"{slug:<42} {csv_len:>7}  {best['uniprot_acc']:<10} {best['chain_query'][:25]:<25} "
              f"{best['chain_length']:>9} {best['length_delta']:>+5}  {best['organism'][:35]:<35} [{status}]")

    OUT.parent.mkdir(parents=True, exist_ok=True)
    with OUT.open("w") as f:
        json.dump(decisions, f, indent=2)
    print(f"\nWrote {OUT}")
    statuses = {}
    for slug, d in decisions.items():
        statuses[d.get("status", "none")] = statuses.get(d.get("status", "none"), 0) + 1
    print(f"Status: {statuses}")


if __name__ == "__main__":
    main()
