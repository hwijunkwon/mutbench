#!/usr/bin/env python3
"""
Feasibility probe — query UniProt for structured feature annotations on the
16 Wave 4 cross_pathogen targets that lack Layer A. Output an inventory CSV.

This is a non-curation feasibility check: it counts how many position-level
feature annotations (sites, disulfide bonds, chain boundaries, glycosylation,
propeptide cleavage) UniProt holds for each target, by querying the public
REST API.

NOT a Layer A label — just an audit of public-DB richness so we can decide
whether automated panel expansion is viable.
"""
import json
import sys
import time
import urllib.parse
import urllib.request
from pathlib import Path

TARGETS = [
    # (slug, taxid, protein_query, comment)
    ("chikungunya_virus_e2", "37124", "E2", "alphavirus envelope E2"),
    ("eastern_equine_encephalitis_virus_e2", "11021", "E2", "alphavirus E2"),
    ("hcov-229e_spike", "11137", "spike", "coronavirus spike"),
    ("hcov-nl63_spike", "277944", "spike", "coronavirus spike"),
    ("hendra_virus_g", "63330", "attachment glycoprotein G", "henipavirus G"),
    ("japanese_encephalitis_virus_e", "11072", "envelope", "flavivirus E"),
    ("lassa_gpc", "11620", "glycoprotein", "arenavirus GPC"),
    ("marburg_virus_gp", "11269", "glycoprotein GP", "filovirus GP"),
    ("measles_virus_h", "11234", "hemagglutinin", "morbillivirus H"),
    ("mumps_virus_hn", "1979165", "hemagglutinin neuraminidase", "rubulavirus HN"),
    ("nipah_virus_g", "121791", "attachment glycoprotein G", "henipavirus G"),
    ("tick-borne_encephalitis_virus_e", "11084", "envelope", "flavivirus E"),
    ("venezuelan_equine_encephalitis_virus_e2", "11036", "E2", "alphavirus E2"),
    ("western_equine_encephalitis_virus_e2", "11039", "E2", "alphavirus E2"),
    ("wnv_e", "11082", "envelope", "flavivirus E"),
    ("yfv_e", "11089", "envelope", "flavivirus E"),
]

# Position-level feature types we count. These are STANDARD structural / functional
# annotations in UniProt — disulfide bonds, glycosylation sites, cleavage sites,
# propeptide/chain boundaries, signal peptides, binding sites.
FEATURE_FIELDS = [
    "accession",
    "reviewed",
    "protein_name",
    "organism_name",
    "length",
    "ft_site",
    "ft_chain",
    "ft_signal",
    "ft_propep",
    "ft_disulfid",
    "ft_carbohyd",
    "ft_binding",
    "ft_region",
    "ft_topo_dom",
    "ft_transmem",
    "ft_variant",
]


def query_uniprot(taxid: str, query: str, size: int = 5) -> list[dict]:
    q = f"organism_id:{taxid} AND ({query})"
    params = {
        "query": q,
        "fields": ",".join(FEATURE_FIELDS),
        "format": "json",
        "size": str(size),
    }
    url = "https://rest.uniprot.org/uniprotkb/search?" + urllib.parse.urlencode(params)
    req = urllib.request.Request(url, headers={"User-Agent": "mutbench-feasibility/0.1"})
    try:
        with urllib.request.urlopen(req, timeout=20) as r:
            data = json.loads(r.read().decode("utf-8"))
        return data.get("results", [])
    except Exception as e:
        return [{"_error": repr(e)}]


def pick_canonical(results: list[dict], expected_len_min: int = 200) -> dict | None:
    if not results or "_error" in results[0]:
        return None
    reviewed = [r for r in results if r.get("entryType", "").lower().startswith("uniprotkb reviewed")]
    pool = reviewed if reviewed else results
    pool = [r for r in pool if not r.get("_error")]
    if not pool:
        return None
    def length_of(r):
        return r.get("sequence", {}).get("length", 0) or 0
    pool_long = [r for r in pool if length_of(r) >= expected_len_min]
    chosen_pool = pool_long if pool_long else pool
    return max(chosen_pool, key=length_of)


def count_features(entry: dict) -> dict:
    counts = {}
    if not entry:
        return counts
    for feat in entry.get("features", []) or []:
        ftype = feat.get("type", "Other")
        counts[ftype] = counts.get(ftype, 0) + 1
    return counts


def classify(counts: dict) -> str:
    site = counts.get("Site", 0)
    binding = counts.get("Binding site", 0)
    disulfid = counts.get("Disulfide bond", 0)
    glyco = counts.get("Glycosylation", 0)
    chain = counts.get("Chain", 0)
    propep = counts.get("Propeptide", 0)
    region = counts.get("Region", 0)
    variant = counts.get("Natural variant", 0)
    structural = disulfid + glyco + chain + propep
    annotated = site + binding + region
    score = annotated * 2 + structural + variant // 5
    if annotated >= 5 or score >= 15:
        return "A"
    if annotated >= 1 or score >= 5:
        return "B"
    return "C"


def main():
    out_csv = Path("/proj/paper/results/mutbench/layerA_alternative_sources_inventory.csv")
    out_csv.parent.mkdir(parents=True, exist_ok=True)
    rows = []
    detail_rows = []
    print(f"{'target':<42} {'acc':<10} {'reviewed':<10} {'len':>5}  {'site':>4} {'bind':>4} {'reg':>4} {'ds':>4} {'gly':>4} {'ch':>3} {'pp':>3} {'var':>4}  cls")
    print("-" * 120)
    for slug, taxid, q, comment in TARGETS:
        results = query_uniprot(taxid, q, size=10)
        time.sleep(0.5)
        entry = pick_canonical(results)
        if entry is None:
            row = {
                "target": slug,
                "taxid": taxid,
                "uniprot_acc": "",
                "reviewed": "",
                "length": 0,
                "site": 0, "binding": 0, "region": 0, "disulfid": 0,
                "glyco": 0, "chain": 0, "propep": 0, "variant": 0,
                "classification": "C",
                "notes": "no_uniprot_match",
            }
            print(f"{slug:<42} {'-':<10} {'-':<10} {0:>5}  {0:>4} {0:>4} {0:>4} {0:>4} {0:>4} {0:>3} {0:>3} {0:>4}  C")
            rows.append(row)
            continue
        counts = count_features(entry)
        acc = entry.get("primaryAccession", "")
        reviewed = entry.get("entryType", "").replace("UniProtKB ", "")
        length = entry.get("sequence", {}).get("length", 0)
        cls = classify(counts)
        row = {
            "target": slug,
            "taxid": taxid,
            "uniprot_acc": acc,
            "reviewed": reviewed,
            "length": length,
            "site": counts.get("Site", 0),
            "binding": counts.get("Binding site", 0),
            "region": counts.get("Region", 0),
            "disulfid": counts.get("Disulfide bond", 0),
            "glyco": counts.get("Glycosylation", 0),
            "chain": counts.get("Chain", 0),
            "propep": counts.get("Propeptide", 0),
            "variant": counts.get("Natural variant", 0),
            "classification": cls,
            "notes": comment,
        }
        rows.append(row)
        print(f"{slug:<42} {acc:<10} {reviewed:<10} {length:>5}  "
              f"{row['site']:>4} {row['binding']:>4} {row['region']:>4} "
              f"{row['disulfid']:>4} {row['glyco']:>4} {row['chain']:>3} "
              f"{row['propep']:>3} {row['variant']:>4}  {cls}")
        for feat in entry.get("features", []) or []:
            loc = feat.get("location", {}) or {}
            start = (loc.get("start") or {}).get("value")
            end = (loc.get("end") or {}).get("value")
            detail_rows.append({
                "target": slug,
                "uniprot_acc": acc,
                "feature_type": feat.get("type", ""),
                "start": start,
                "end": end,
                "description": (feat.get("description", "") or "")[:200],
            })

    import csv
    cols = ["target", "taxid", "uniprot_acc", "reviewed", "length",
            "site", "binding", "region", "disulfid", "glyco",
            "chain", "propep", "variant", "classification", "notes"]
    with out_csv.open("w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=cols)
        w.writeheader()
        for r in rows:
            w.writerow(r)
    detail_csv = out_csv.with_name("layerA_alternative_sources_features.csv")
    with detail_csv.open("w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=["target", "uniprot_acc", "feature_type", "start", "end", "description"])
        w.writeheader()
        for r in detail_rows:
            w.writerow(r)

    cls_counts = {"A": 0, "B": 0, "C": 0}
    for r in rows:
        cls_counts[r["classification"]] += 1
    print()
    print(f"Wrote {out_csv}  ({len(rows)} rows)")
    print(f"Wrote {detail_csv}  ({len(detail_rows)} feature rows)")
    print(f"Class A (rich): {cls_counts['A']}  Class B (marginal): {cls_counts['B']}  Class C (sparse): {cls_counts['C']}")


if __name__ == "__main__":
    main()
