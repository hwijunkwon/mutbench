#!/usr/bin/env python3
"""Stage additional temporal metadata for PAHD-R follow-up experiments.

The script keeps new data separate from thesis claims. It first parses local
FASTA headers for accessions and dates. With --fetch-ncbi, it also attempts to
retrieve accession-level GenBank XML metadata from NCBI Protein and extracts
collection_date/country when available.
"""

from __future__ import annotations

import argparse
import csv
from pathlib import Path
import re
import time
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET

import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parent.parent
OUT_DIR = PROJECT_ROOT / "data" / "additional" / "pahd_r_temporal_metadata"
RESULTS_DIR = PROJECT_ROOT / "results" / "mutbench"

FASTAS = {
    "HIV-1": PROJECT_ROOT / "data" / "hiv" / "hiv1_gp120_sequences.fasta",
    "MERS": PROJECT_ROOT / "data" / "mers" / "mers_spike_sequences.fasta",
}

ACCESSION_RE = re.compile(r"^([A-Z]{1,4}_?\d+(?:\.\d+)?)\b")
YEAR_RE = re.compile(r"(?<![A-Za-z0-9])((?:19|20)\d{2})(?![A-Za-z0-9])")
EMAIL = "mutbench@example.com"


def read_fasta_headers(path: Path) -> list[str]:
    headers = []
    for line in path.read_text(encoding="utf-8").splitlines():
        if line.startswith(">"):
            headers.append(line[1:].strip())
    return headers


def accession_from_header(header: str) -> str:
    match = ACCESSION_RE.search(header)
    return match.group(1) if match else ""


def year_from_text(text: str) -> str:
    match = YEAR_RE.search(text)
    return match.group(1) if match else ""


def fetch_genbank_xml(accessions: list[str], batch_size: int = 100, delay: float = 0.34) -> dict[str, dict[str, str]]:
    fetched: dict[str, dict[str, str]] = {}
    base = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi"
    for start in range(0, len(accessions), batch_size):
        batch = accessions[start:start + batch_size]
        params = {
            "db": "protein",
            "id": ",".join(batch),
            "rettype": "gb",
            "retmode": "xml",
            "email": EMAIL,
        }
        url = base + "?" + urllib.parse.urlencode(params)
        with urllib.request.urlopen(url, timeout=60) as handle:
            payload = handle.read()
        root = ET.fromstring(payload)
        for seq in root.findall(".//GBSeq"):
            accession = seq.findtext("GBSeq_accession-version") or seq.findtext("GBSeq_primary-accession") or ""
            create_date = seq.findtext("GBSeq_create-date") or ""
            update_date = seq.findtext("GBSeq_update-date") or ""
            organism = seq.findtext("GBSeq_organism") or ""
            source = seq.findtext("GBSeq_source") or ""
            collection_date = ""
            country = ""
            isolate = ""
            for feature in seq.findall(".//GBFeature"):
                key = feature.findtext("GBFeature_key") or ""
                if key.lower() not in {"source", "protein"}:
                    continue
                for qual in feature.findall(".//GBQualifier"):
                    name = qual.findtext("GBQualifier_name") or ""
                    value = qual.findtext("GBQualifier_value") or ""
                    if name == "collection_date":
                        collection_date = value
                    elif name == "country":
                        country = value
                    elif name == "isolate":
                        isolate = value
            fetched[accession] = {
                "ncbi_create_date": create_date,
                "ncbi_update_date": update_date,
                "organism": organism,
                "source": source,
                "collection_date": collection_date,
                "country": country,
                "isolate": isolate,
                "ncbi_year": year_from_text(collection_date) or year_from_text(create_date),
                "fetch_status": "ok",
            }
        time.sleep(delay)
    for accession in accessions:
        fetched.setdefault(accession, {"fetch_status": "missing_in_ncbi_response"})
    return fetched


def build_local_table(pathogen: str, path: Path) -> pd.DataFrame:
    rows = []
    for header in read_fasta_headers(path):
        accession = accession_from_header(header)
        rows.append({
            "pathogen": pathogen,
            "accession": accession,
            "header": header,
            "header_year": year_from_text(header),
        })
    return pd.DataFrame(rows)


def summarize(df: pd.DataFrame) -> dict[str, object]:
    n = len(df)
    with_accession = int((df["accession"].astype(str) != "").sum()) if n else 0
    header_year = int((df["header_year"].astype(str) != "").sum()) if n else 0
    ncbi_year = int((df.get("ncbi_year", pd.Series([""] * n)).astype(str) != "").sum()) if n else 0
    collection_date = int((df.get("collection_date", pd.Series([""] * n)).astype(str) != "").sum()) if n else 0
    return {
        "pathogen": df["pathogen"].iloc[0] if n else "",
        "n_records": n,
        "n_with_accession": with_accession,
        "accession_coverage": with_accession / n if n else 0.0,
        "n_header_year": header_year,
        "header_year_coverage": header_year / n if n else 0.0,
        "n_ncbi_year": ncbi_year,
        "ncbi_year_coverage": ncbi_year / n if n else 0.0,
        "n_collection_date": collection_date,
        "collection_date_coverage": collection_date / n if n else 0.0,
    }


def run(fetch_ncbi: bool) -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    all_tables = []
    summaries = []
    for pathogen, path in FASTAS.items():
        table = build_local_table(pathogen, path)
        if fetch_ncbi:
            accessions = sorted(set(a for a in table["accession"].astype(str) if a))
            fetched = fetch_genbank_xml(accessions)
            fetched_df = pd.DataFrame([
                {"accession": accession, **metadata}
                for accession, metadata in fetched.items()
            ])
            table = table.merge(fetched_df, on="accession", how="left")
        out_path = OUT_DIR / f"{pathogen.replace('-', '_').lower()}_temporal_metadata.csv"
        table.to_csv(out_path, index=False, quoting=csv.QUOTE_MINIMAL)
        all_tables.append(table)
        summaries.append(summarize(table))

    combined = pd.concat(all_tables, ignore_index=True)
    summary = pd.DataFrame(summaries)
    combined_path = OUT_DIR / "combined_temporal_metadata.csv"
    summary_path = RESULTS_DIR / "pahd_r_additional_temporal_metadata_summary.csv"
    report_path = RESULTS_DIR / "pahd_r_additional_data_staging_report.md"
    combined.to_csv(combined_path, index=False)
    summary.to_csv(summary_path, index=False)

    lines = [
        "# PAHD-R Additional Data Staging Report",
        "",
        "Date: 2026-04-27 KST",
        "",
        "## Scope",
        "",
        (
            "This staging report collects HIV-1/MERS accession and temporal metadata "
            "for follow-up experiments only. It is not incorporated into thesis "
            "performance claims."
        ),
        "",
        "## Fetch Mode",
        "",
        f"NCBI metadata fetch: {'enabled' if fetch_ncbi else 'disabled'}",
        "",
        "## Summary",
        "",
        "| " + " | ".join(summary.columns) + " |",
        "| " + " | ".join(["---"] * len(summary.columns)) + " |",
    ]
    for _, row in summary.iterrows():
        vals = []
        for col in summary.columns:
            val = row[col]
            vals.append(f"{val:.4f}" if isinstance(val, float) else str(val))
        lines.append("| " + " | ".join(vals) + " |")
    lines.extend([
        "",
        "## Staged Files",
        "",
        f"- `{combined_path.relative_to(PROJECT_ROOT)}`",
        f"- `{(OUT_DIR / 'hiv_1_temporal_metadata.csv').relative_to(PROJECT_ROOT)}`",
        f"- `{(OUT_DIR / 'mers_temporal_metadata.csv').relative_to(PROJECT_ROOT)}`",
        f"- `{summary_path.relative_to(PROJECT_ROOT)}`",
        "",
        "## Interpretation",
        "",
        (
            "If collection-date coverage remains low after NCBI fetch, the next step "
            "is a curated temporal MSA or accession table rather than another PAHD-R "
            "weight/preprocessing sweep."
        ),
        "",
    ])
    report_path.write_text("\n".join(lines), encoding="utf-8")
    print(report_path)
    print(summary.round(4).to_string(index=False))


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--fetch-ncbi", action="store_true", help="Fetch GenBank XML metadata from NCBI Protein.")
    args = parser.parse_args()
    run(fetch_ncbi=args.fetch_ncbi)


if __name__ == "__main__":
    main()
