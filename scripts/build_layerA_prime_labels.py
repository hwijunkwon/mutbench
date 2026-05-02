#!/usr/bin/env python3
"""
Build Layer A' label CSVs from curated UniProt accessions.

Pipeline:
1. Read curated accession map (from build_curated_accession_map.py).
2. Fetch each UniProt entry directly (one per target).
3. For each feature, apply:
   - Type filter: keep Site / Binding site / Active site / Motif / Region
   - Region description filter (drop structural-only)
   - Coordinate guards (1 <= start_mature, end_mature <= csv_length, delta <= 6)
4. Output:
   - results/mutbench/layer_a_prime/{target}_layer_a_prime.csv  (position, layer_a_prime, evidence_basis, description)
   - results/mutbench/layerA_prime_inventory.csv (per-target summary with raw v2 + refined classification)
"""
import csv
import json
import time
import urllib.request
from pathlib import Path

ROOT = Path("/proj/paper")
ACC_MAP = ROOT / "results" / "mutbench" / "layerA_curated_accession_map.json"
OUT_DIR = ROOT / "results" / "mutbench" / "layer_a_prime"
INVENTORY = ROOT / "results" / "mutbench" / "layerA_prime_inventory.csv"

# Region descriptions to drop (case-insensitive substring match against feature description)
REGION_DROP_PATTERNS = [
    "disordered",
    "mucin-like",
    "stalk",
    "head",
    "heptad repeat",
    "transient transmembrane",
    "signal peptide",
    "propeptide",
    "necessary for nucleocapsid",
    "transmembrane domain",
    "cytoplasmic",
    "stem",
    "spacer",
    "linker",
    "polybasic cleavage",
]

# Region descriptions to keep with explicit functional description
REGION_KEEP_PATTERNS = [
    "fusion peptide",
    "fusion loop",
    "receptor",
    "binding",
    "interaction",
    "antigenic",
    "epitope",
    "active site",
    "catalytic",
    "neuraminidase activity",
    "membrane fusion",
    "host receptor",
    "rbd",
    "receptor-binding",
]

# Site/Binding site keep regardless of description; drop if description names cleavage at chain boundary
SITE_DROP_PATTERNS = [
    "cleavage; by host signal peptidase",
]

KEEP_TYPES = {"Site", "Binding site", "Active site", "Motif", "Region"}

# Length-mismatch acceptance threshold (delta in residues)
MAX_LENGTH_DELTA = 6


def fetch(acc: str) -> dict:
    url = f"https://rest.uniprot.org/uniprotkb/{acc}.json"
    req = urllib.request.Request(url, headers={"User-Agent": "mb-la-prime/0.1"})
    with urllib.request.urlopen(req, timeout=20) as r:
        return json.loads(r.read().decode("utf-8"))


def keep_region(desc: str) -> bool:
    d = desc.lower()
    for pat in REGION_KEEP_PATTERNS:
        if pat in d:
            return True
    for pat in REGION_DROP_PATTERNS:
        if pat in d:
            return False
    # Default: drop unknown Region descriptions to be conservative
    return False


def keep_site(desc: str) -> bool:
    d = desc.lower()
    for pat in SITE_DROP_PATTERNS:
        if pat in d:
            return False
    return True


def main():
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    with ACC_MAP.open() as f:
        acc_map = json.load(f)

    summary = []
    print(f"{'target':<42} {'acc':<10} {'csv_len':>7} {'chain_len':>9} {'delta':>5} {'raw_la_relevant':>15} {'kept':>5} {'class':>5}")
    print("-" * 110)

    for slug, info in acc_map.items():
        if info.get("status") in ("no_candidate", "mismatch") and info.get("length_delta", 999) > MAX_LENGTH_DELTA:
            summary.append({
                "target": slug, "uniprot_acc": info.get("uniprot_acc", ""),
                "csv_length": info.get("csv_length", 0), "chain_length": info.get("chain_length", 0),
                "length_delta": info.get("length_delta", 0), "status": info.get("status", "skipped"),
                "n_layer_a_prime_positions": 0, "raw_la_relevant": 0, "refined_class": "C",
                "reason": f"length mismatch >{MAX_LENGTH_DELTA}",
            })
            print(f"{slug:<42} {info.get('uniprot_acc',''):<10} {info.get('csv_length',0):>7} {info.get('chain_length',0):>9} {info.get('length_delta',0):>+5}  {0:>14} {0:>5}    C  [skip]")
            continue

        acc = info["uniprot_acc"]
        chain_start = info.get("chain_start", 1)
        chain_end = info.get("chain_end", info.get("chain_length", 0))
        csv_len = info["csv_length"]
        delta = info["length_delta"]

        try:
            entry = fetch(acc)
        except Exception as e:
            print(f"{slug:<42} {acc:<10} fetch_error: {e}")
            continue
        time.sleep(0.4)

        is_full_entry = info.get("chain_query") == "(full entry)"
        chain_offset = 0 if is_full_entry else (chain_start - 1)

        rows = []
        n_raw_la = 0
        for feat in entry.get("features", []) or []:
            ftype = feat.get("type", "")
            if ftype not in KEEP_TYPES:
                continue
            loc = feat.get("location", {}) or {}
            s = (loc.get("start") or {}).get("value")
            e = (loc.get("end") or {}).get("value")
            if not (isinstance(s, int) and isinstance(e, int)):
                continue
            # Restrict to the chain region (or full entry)
            if not is_full_entry:
                if e < chain_start or s > chain_end:
                    continue
            n_raw_la += 1
            desc = (feat.get("description", "") or "")
            # Apply description filters
            if ftype == "Region":
                if not keep_region(desc):
                    continue
            elif ftype in ("Site", "Binding site", "Active site"):
                if not keep_site(desc):
                    continue
            mature_s = s - chain_offset
            mature_e = e - chain_offset
            # Coordinate guards: must lie within mature CSV positions
            if mature_s < 1 or mature_e > csv_len:
                continue
            for pos in range(mature_s, mature_e + 1):
                rows.append({
                    "position": pos,
                    "layer_a_prime": 1,
                    "feature_type": ftype,
                    "evidence_basis": "uniprot_curated_feature",
                    "uniprot_acc": acc,
                    "description": desc[:200],
                })

        # Deduplicate by position (keep first row per position)
        seen = set()
        rows_dedup = []
        for r in rows:
            if r["position"] in seen:
                continue
            seen.add(r["position"])
            rows_dedup.append(r)

        out_csv = OUT_DIR / f"{slug}_layer_a_prime.csv"
        with out_csv.open("w", newline="") as f:
            w = csv.DictWriter(f, fieldnames=["position", "layer_a_prime", "feature_type", "evidence_basis", "uniprot_acc", "description"])
            w.writeheader()
            for r in rows_dedup:
                w.writerow(r)

        n_pos = len(rows_dedup)
        cls = "A" if n_pos >= 8 else ("B" if n_pos >= 3 else "C")
        summary.append({
            "target": slug, "uniprot_acc": acc, "csv_length": csv_len,
            "chain_length": info.get("chain_length", 0), "length_delta": delta,
            "status": info.get("status", ""),
            "n_layer_a_prime_positions": n_pos, "raw_la_relevant": n_raw_la,
            "refined_class": cls, "reason": "",
        })
        print(f"{slug:<42} {acc:<10} {csv_len:>7} {info.get('chain_length',0):>9} {delta:>+5} {n_raw_la:>15} {n_pos:>5}    {cls}")

    cols = ["target", "uniprot_acc", "csv_length", "chain_length", "length_delta",
            "status", "n_layer_a_prime_positions", "raw_la_relevant", "refined_class", "reason"]
    with INVENTORY.open("w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=cols)
        w.writeheader()
        for r in summary:
            w.writerow(r)

    cls_counts = {"A": 0, "B": 0, "C": 0}
    for r in summary:
        cls_counts[r["refined_class"]] += 1
    print()
    print(f"Wrote {INVENTORY}")
    print(f"Refined class counts: A={cls_counts['A']}  B={cls_counts['B']}  C={cls_counts['C']}")
    print(f"Layer A' files in {OUT_DIR}/")


if __name__ == "__main__":
    main()
