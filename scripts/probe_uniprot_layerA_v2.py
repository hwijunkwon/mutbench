#!/usr/bin/env python3
"""
v2 — direct fetch of canonical reviewed UniProt entries by accession, with
polyprotein-to-mature-protein coordinate mapping for flavivirus and arenavirus
targets.

For each target: list known reviewed accessions (literature-canonical strains),
fetch features, filter to those overlapping the mature protein region, and
report. This gives a cleaner picture than the v1 keyword search.
"""
import json
import time
import urllib.parse
import urllib.request
import csv
from pathlib import Path

# Each target: list of (accession, mature_chain_label_or_None, expected_mature_length)
# accession picked from literature-standard reference strains
CANONICAL = {
    "yfv_e": [("P03314", "Envelope protein E", 493)],          # YFV 17D-204 vaccine polyprotein
    "lassa_gpc": [("P08669", None, 491)],                       # Lassa Josiah GPC (full GPC)
    "wnv_e": [("P06935", "Envelope protein E", 501)],           # WNV NY99 polyprotein
    "japanese_encephalitis_virus_e": [("P27395", "Envelope protein E", 500)],  # JEV SA-14
    "tick-borne_encephalitis_virus_e": [("P14336", "Envelope protein E", 496)],  # TBEV Neudoerfl
    "marburg_virus_gp": [("P35253", None, 681)],                # Marburg Musoke GP
    "hendra_virus_g": [("O89343", None, 604)],                  # Hendra horse-1994 G
    "nipah_virus_g": [("Q9IH62", None, 602)],                   # Nipah Malaysia G
    "measles_virus_h": [("P08362", None, 617)],                 # Measles Edmonston H
    "mumps_virus_hn": [("P30924", None, 582)],                  # Mumps Miyahara HN
    "chikungunya_virus_e2": [("Q8JUX5", "Envelope protein E2", 423)],  # CHIKV S27 polyprotein
    "eastern_equine_encephalitis_virus_e2": [("P08768", "Envelope protein E2", 423)],
    "venezuelan_equine_encephalitis_virus_e2": [("P05674", "Envelope protein E2", 423)],
    "western_equine_encephalitis_virus_e2": [("P13897", "Envelope protein E2", 423)],
    "hcov-229e_spike": [("P15423", None, 1173)],
    "hcov-nl63_spike": [("Q6Q1S2", None, 1356)],
}

FEATURE_FIELDS = [
    "accession", "reviewed", "protein_name", "organism_name", "length",
    "ft_site", "ft_chain", "ft_signal", "ft_propep", "ft_disulfid",
    "ft_carbohyd", "ft_binding", "ft_region", "ft_topo_dom", "ft_transmem",
    "ft_variant", "ft_act_site", "ft_motif",
]


def fetch_entry(acc: str) -> dict | None:
    url = f"https://rest.uniprot.org/uniprotkb/{acc}.json"
    req = urllib.request.Request(url, headers={"User-Agent": "mutbench-feasibility/0.2"})
    try:
        with urllib.request.urlopen(req, timeout=20) as r:
            return json.loads(r.read().decode("utf-8"))
    except Exception as e:
        print(f"  ERROR {acc}: {e}")
        return None


def find_chain_region(entry: dict, label: str | None) -> tuple[int, int] | None:
    """Find the (start, end) of the named chain, or return None for full-length entries."""
    if label is None:
        return None
    for feat in entry.get("features", []) or []:
        if feat.get("type") != "Chain":
            continue
        desc = feat.get("description", "") or ""
        if label.lower() in desc.lower():
            loc = feat.get("location", {}) or {}
            s = (loc.get("start") or {}).get("value")
            e = (loc.get("end") or {}).get("value")
            if s and e:
                return (int(s), int(e))
    return None


def overlaps(start: int, end: int, region: tuple[int, int] | None) -> bool:
    if region is None:
        return True
    rs, re = region
    return not (end < rs or start > re)


def map_to_mature(start: int, end: int, region: tuple[int, int] | None) -> tuple[int, int]:
    if region is None:
        return (start, end)
    rs, _ = region
    return (start - rs + 1, end - rs + 1)


def relevant_for_layer_a(ftype: str) -> bool:
    """Which UniProt feature types are plausible Layer A primary evidence?

    Layer A = literature-curated adaptive/diversifying or immune-relevant positions.
    Site / Binding site / Active site / Motif / Region (functional) → yes
    Glycosylation → marginal (could be antigenic shield)
    Disulfide bond / Chain / Topological domain / Transmembrane / Signal → no (structural)
    Natural variant → marginal (depends on annotation)
    """
    return ftype in {"Site", "Binding site", "Active site", "Motif", "Region"}


def main():
    out_csv = Path("/proj/paper/results/mutbench/layerA_alternative_sources_inventory_v2.csv")
    feat_csv = Path("/proj/paper/results/mutbench/layerA_alternative_sources_features_v2.csv")
    summary_rows = []
    feature_rows = []

    print(f"{'target':<42} {'acc':<10} {'len':>5} {'chain':<13} {'features_in_chain':>17} {'layer_a_relevant':>16}  cls")
    print("-" * 120)

    for slug, accs in CANONICAL.items():
        for acc, chain_label, expected_len in accs:
            entry = fetch_entry(acc)
            time.sleep(0.5)
            if entry is None:
                summary_rows.append({
                    "target": slug, "uniprot_acc": acc, "length": 0,
                    "chain_label": chain_label or "", "chain_start": "", "chain_end": "",
                    "n_features_in_chain": 0, "n_layer_a_relevant": 0,
                    "feature_breakdown": "fetch_failed", "classification": "C",
                })
                continue
            full_len = entry.get("sequence", {}).get("length", 0)
            chain_region = find_chain_region(entry, chain_label) if chain_label else None
            chain_str = f"{chain_region[0]}-{chain_region[1]}" if chain_region else "(full entry)"

            n_in_chain = 0
            n_la_relevant = 0
            type_counts = {}
            for feat in entry.get("features", []) or []:
                ftype = feat.get("type", "")
                loc = feat.get("location", {}) or {}
                s = (loc.get("start") or {}).get("value")
                e = (loc.get("end") or {}).get("value")
                if not (isinstance(s, int) and isinstance(e, int)):
                    continue
                if not overlaps(s, e, chain_region):
                    continue
                n_in_chain += 1
                type_counts[ftype] = type_counts.get(ftype, 0) + 1
                ms, me = map_to_mature(s, e, chain_region)
                is_la = relevant_for_layer_a(ftype)
                if is_la:
                    n_la_relevant += 1
                feature_rows.append({
                    "target": slug, "uniprot_acc": acc,
                    "feature_type": ftype, "start_full": s, "end_full": e,
                    "start_mature": ms, "end_mature": me,
                    "layer_a_relevant": "yes" if is_la else "no",
                    "description": (feat.get("description", "") or "")[:200],
                })
            cls = "A" if n_la_relevant >= 5 else ("B" if n_la_relevant >= 1 else "C")
            breakdown = ", ".join(f"{k}={v}" for k, v in sorted(type_counts.items()))
            print(f"{slug:<42} {acc:<10} {full_len:>5} {chain_str:<13} {n_in_chain:>17} {n_la_relevant:>16}  {cls}")
            summary_rows.append({
                "target": slug, "uniprot_acc": acc, "length": full_len,
                "chain_label": chain_label or "",
                "chain_start": chain_region[0] if chain_region else "",
                "chain_end": chain_region[1] if chain_region else "",
                "n_features_in_chain": n_in_chain,
                "n_layer_a_relevant": n_la_relevant,
                "feature_breakdown": breakdown,
                "classification": cls,
            })

    cols = ["target", "uniprot_acc", "length", "chain_label", "chain_start",
            "chain_end", "n_features_in_chain", "n_layer_a_relevant",
            "feature_breakdown", "classification"]
    with out_csv.open("w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=cols)
        w.writeheader()
        for r in summary_rows:
            w.writerow(r)
    with feat_csv.open("w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=["target", "uniprot_acc", "feature_type",
                                           "start_full", "end_full", "start_mature",
                                           "end_mature", "layer_a_relevant", "description"])
        w.writeheader()
        for r in feature_rows:
            w.writerow(r)

    cls_counts = {"A": 0, "B": 0, "C": 0}
    for r in summary_rows:
        cls_counts[r["classification"]] += 1
    print()
    print(f"Wrote {out_csv} ({len(summary_rows)} rows)")
    print(f"Wrote {feat_csv} ({len(feature_rows)} rows)")
    print(f"Class A (≥5 layer-a-relevant features): {cls_counts['A']}")
    print(f"Class B (1-4 features): {cls_counts['B']}")
    print(f"Class C (none): {cls_counts['C']}")


if __name__ == "__main__":
    main()
