#!/usr/bin/env python3
"""Wave 5 Task 1 PubMed search inventory for YFV E, Lassa GPC, and WNV E."""

from __future__ import annotations

import csv
import hashlib
import json
import re
import shutil
import subprocess
import sys
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import requests


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "results" / "mutbench" / "codex_wave5"
CACHE = OUT / "cache" / "pubmed"
ABSTRACTS = OUT / "w5_abstracts"
EMAIL = "fjrzlgnlwns@gmail.com"
TOOL = "codex_w5_pilot3_search"
BASE = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils"
RETMAX = 200
SLEEP_SECONDS = 0.34
REQUEST_TIMEOUT = 30

QUERIES: dict[str, list[tuple[str, str]]] = {
    "YFV_E": [
        (
            "Y1",
            '("yellow fever virus"[Title/Abstract] OR YFV[Title/Abstract]) AND ("envelope"[Title/Abstract] OR "E protein"[Title/Abstract] OR "EDIII"[Title/Abstract] OR "fusion loop"[Title/Abstract]) AND (escape[Title/Abstract] OR neutralization[Title/Abstract] OR epitope[Title/Abstract] OR antigenic[Title/Abstract])',
        ),
        ("Y2", '("yellow fever vaccine" OR "17D") AND (mutation OR epitope) AND envelope'),
        ("Y3", '"yellow fever virus" AND "deep mutational scanning"'),
        ("Y4", '"yellow fever virus" AND ("monoclonal antibody" OR "neutralizing antibody")'),
        ("Y5", '("yellow fever virus" OR YFV) AND ("EDI" OR "EDII" OR "EDIII" OR "domain III") AND envelope'),
    ],
    "Lassa_GPC": [
        ("L1", '("Lassa virus" OR LASV OR arenavirus) AND (GPC OR "GP1" OR "GP2" OR SSP) AND (escape OR neutralization OR epitope OR antigenic)'),
        ("L2", '"Lassa virus" AND "deep mutational scanning"'),
        ("L3", '"Lassa virus" AND ("monoclonal antibody" OR "neutralizing antibody")'),
        ("L4", '("Lassa virus" OR LASV) AND (entry OR fusion OR glycan) AND glycoprotein'),
        ("L5", '"Lassa virus" AND (Josiah OR lineage) AND envelope'),
    ],
    "WNV_E": [
        ("W1", '("West Nile virus" OR WNV OR Kunjin) AND ("envelope" OR "E protein" OR "EDIII") AND (escape OR neutralization OR epitope)'),
        ("W2", '"West Nile virus" AND "deep mutational scanning"'),
        ("W3", '("West Nile virus" OR WNV) AND ("monoclonal antibody" OR "neutralizing antibody")'),
        ("W4", '"West Nile virus" AND ("EDI" OR "EDII" OR "EDIII" OR "fusion loop") AND envelope'),
        ("W5", '"West Nile virus" AND (lineage OR strain) AND antigenic AND envelope'),
    ],
}

last_call_at = 0.0


class SearchFailure(RuntimeError):
    """Raised for network or NCBI failures that should produce partial outputs."""


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def git_sha() -> str:
    try:
        return subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip()
    except Exception as exc:  # pragma: no cover - best effort provenance
        return f"unavailable:{exc.__class__.__name__}"


def stable_int_sort(pmids: list[str]) -> list[str]:
    return sorted(set(pmids), key=lambda value: int(value) if value.isdigit() else value)


def cache_key(*parts: str) -> str:
    digest = hashlib.sha256("\n".join(parts).encode("utf-8")).hexdigest()[:24]
    return digest


def ensure_dirs() -> None:
    CACHE.mkdir(parents=True, exist_ok=True)
    (CACHE / "esearch").mkdir(parents=True, exist_ok=True)
    (CACHE / "esummary").mkdir(parents=True, exist_ok=True)
    (CACHE / "abstracts").mkdir(parents=True, exist_ok=True)
    for target in QUERIES:
        (ABSTRACTS / target).mkdir(parents=True, exist_ok=True)


def rate_limited_get(url: str, params: dict[str, Any]) -> requests.Response:
    global last_call_at
    elapsed = time.monotonic() - last_call_at
    if elapsed < SLEEP_SECONDS:
        time.sleep(SLEEP_SECONDS - elapsed)
    try:
        response = requests.get(url, params=params, timeout=REQUEST_TIMEOUT)
    except requests.RequestException as exc:
        raise SearchFailure(f"network_blocked: {url} params={params} error={exc}") from exc
    last_call_at = time.monotonic()
    if response.status_code >= 400:
        raise SearchFailure(f"ncbi_error: status={response.status_code} url={response.url} body={response.text[:500]}")
    return response


def read_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, payload: dict[str, Any]) -> None:
    path.write_text(json.dumps(payload, indent=2, sort_keys=True), encoding="utf-8")


def esearch(target: str, query_id: str, query: str) -> tuple[int, list[str], bool]:
    path = CACHE / "esearch" / f"{target}_{query_id}_{cache_key(query)}.json"
    if path.exists():
        payload = read_json(path)
    else:
        params = {
            "db": "pubmed",
            "term": query,
            "retmode": "json",
            "retmax": RETMAX,
            "email": EMAIL,
            "tool": TOOL,
        }
        print(f"[{utc_now()}] ESearch {target} {query_id}")
        response = rate_limited_get(f"{BASE}/esearch.fcgi", params)
        payload = response.json()
        write_json(path, payload)
    result = payload.get("esearchresult", {})
    count = int(result.get("count", 0))
    pmids = stable_int_sort([str(pmid) for pmid in result.get("idlist", [])])
    return count, pmids, len(pmids) >= RETMAX


def esummary(target: str, query_id: str, pmids: list[str]) -> dict[str, dict[str, Any]]:
    if not pmids:
        return {}
    path = CACHE / "esummary" / f"{target}_{query_id}_{cache_key(','.join(pmids))}.json"
    if path.exists():
        payload = read_json(path)
    else:
        params = {
            "db": "pubmed",
            "id": ",".join(pmids),
            "retmode": "json",
            "email": EMAIL,
            "tool": TOOL,
        }
        print(f"[{utc_now()}] ESummary {target} {query_id} n={len(pmids)}")
        response = rate_limited_get(f"{BASE}/esummary.fcgi", params)
        payload = response.json()
        write_json(path, payload)
    result = payload.get("result", {})
    return {pmid: result.get(pmid, {}) for pmid in pmids}


def publication_year(record: dict[str, Any]) -> str:
    for field in ("pubdate", "epubdate", "sortpubdate"):
        value = str(record.get(field, ""))
        match = re.search(r"(18|19|20)\d{2}", value)
        if match:
            return match.group(0)
    return ""


def fetch_abstract(target: str, pmid: str) -> None:
    target_path = ABSTRACTS / target / f"{pmid}.txt"
    if target_path.exists():
        return
    cache_path = CACHE / "abstracts" / f"{pmid}.txt"
    if cache_path.exists():
        shutil.copyfile(cache_path, target_path)
        return
    params = {
        "db": "pubmed",
        "id": pmid,
        "rettype": "abstract",
        "retmode": "text",
        "email": EMAIL,
        "tool": TOOL,
    }
    print(f"[{utc_now()}] EFetch abstract {target} PMID={pmid}")
    response = rate_limited_get(f"{BASE}/efetch.fcgi", params)
    text = response.text
    cache_path.write_text(text, encoding="utf-8")
    target_path.write_text(text, encoding="utf-8")


def write_empty_outputs(query_date: str, status: str, detail: str) -> None:
    write_json(OUT / "w5_search_log.json", [])
    with (OUT / "w5_pmid_inventory.csv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.writer(handle)
        writer.writerow(["target", "query_id", "query", "pmid", "publication_year", "journal", "title", "query_date_utc", "truncated"])
    with (OUT / "w5_search_summary.csv").open("w", newline="", encoding="utf-8") as handle:
        handle.write(f"# git_sha,{git_sha()}\n")
        handle.write(f"# query_date_utc,{query_date}\n")
        writer = csv.writer(handle)
        writer.writerow(["target", "query_id", "n_hits", "n_unique_pmids_after_dedupe", "n_zero_hit_flag", "query_date_utc", "truncated"])
    (OUT / "w5_search_status.txt").write_text(f"{status}\n{detail}\n", encoding="utf-8")


def write_outputs(
    search_log: list[dict[str, Any]],
    inventory_rows: list[dict[str, Any]],
    summary_rows: list[dict[str, Any]],
    query_date: str,
) -> None:
    write_json(OUT / "w5_search_log.json", {"git_sha": git_sha(), "query_date_utc": query_date, "queries": search_log})
    with (OUT / "w5_pmid_inventory.csv").open("w", newline="", encoding="utf-8") as handle:
        fieldnames = ["target", "query_id", "query", "pmid", "publication_year", "journal", "title", "query_date_utc", "truncated"]
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(inventory_rows)
    with (OUT / "w5_search_summary.csv").open("w", newline="", encoding="utf-8") as handle:
        handle.write(f"# git_sha,{git_sha()}\n")
        handle.write(f"# query_date_utc,{query_date}\n")
        fieldnames = ["target", "query_id", "n_hits", "n_unique_pmids_after_dedupe", "n_zero_hit_flag", "query_date_utc", "truncated"]
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(summary_rows)
    (OUT / "w5_search_status.txt").write_text("ok\n", encoding="utf-8")


def run() -> int:
    ensure_dirs()
    query_date = utc_now()
    print(f"[{query_date}] Wave 5 Task 1 PubMed search start")
    print(f"[{utc_now()}] git_sha={git_sha()}")
    search_log: list[dict[str, Any]] = []
    inventory_rows: list[dict[str, Any]] = []
    summary_rows: list[dict[str, Any]] = []
    pmids_by_target: dict[str, set[str]] = {target: set() for target in QUERIES}

    try:
        for target, target_queries in QUERIES.items():
            seen_for_target: set[str] = set()
            for query_id, query in target_queries:
                started = time.monotonic()
                count, pmids, truncated = esearch(target, query_id, query)
                metadata = esummary(target, query_id, pmids)
                for pmid in pmids:
                    record = metadata.get(pmid, {})
                    inventory_rows.append(
                        {
                            "target": target,
                            "query_id": query_id,
                            "query": query,
                            "pmid": pmid,
                            "publication_year": publication_year(record),
                            "journal": record.get("fulljournalname") or record.get("source", ""),
                            "title": record.get("title", ""),
                            "query_date_utc": query_date,
                            "truncated": int(truncated),
                        }
                    )
                seen_for_target.update(pmids)
                pmids_by_target[target].update(pmids)
                elapsed = time.monotonic() - started
                search_log.append(
                    {
                        "target": target,
                        "query_id": query_id,
                        "query": query,
                        "esearch_count": count,
                        "pmids": pmids,
                        "query_date_utc": query_date,
                        "truncated": truncated,
                        "elapsed_seconds": round(elapsed, 3),
                    }
                )
                summary_rows.append(
                    {
                        "target": target,
                        "query_id": query_id,
                        "n_hits": count,
                        "n_unique_pmids_after_dedupe": len(seen_for_target),
                        "n_zero_hit_flag": int(count == 0),
                        "query_date_utc": query_date,
                        "truncated": int(truncated),
                    }
                )
                print(
                    f"[{utc_now()}] {target} {query_id}: hits={count} retained={len(pmids)} "
                    f"target_unique={len(seen_for_target)} truncated={int(truncated)} elapsed={elapsed:.1f}s"
                )

        inventory_rows.sort(key=lambda row: (row["target"], row["query_id"], int(row["pmid"])))
        summary_rows.sort(key=lambda row: (row["target"], row["query_id"]))
        search_log.sort(key=lambda row: (row["target"], row["query_id"]))

        for target in sorted(pmids_by_target):
            for pmid in stable_int_sort(list(pmids_by_target[target])):
                fetch_abstract(target, pmid)

        write_outputs(search_log, inventory_rows, summary_rows, query_date)
        totals = {target: len(pmids) for target, pmids in pmids_by_target.items()}
        zero_hit = [f"{row['target']}:{row['query_id']}" for row in summary_rows if row["n_zero_hit_flag"]]
        print(f"[{utc_now()}] unique PubMed totals: {totals}")
        print(f"[{utc_now()}] zero-hit queries: {', '.join(zero_hit) if zero_hit else 'none'}")
        print("TASK 1 DONE")
        return 0
    except SearchFailure as exc:
        detail = str(exc)
        status = "network_blocked" if detail.startswith("network_blocked") else "ncbi_error"
        print(f"[{utc_now()}] {status}: {detail}", file=sys.stderr)
        write_empty_outputs(query_date, status, detail)
        print("TASK 1 PARTIAL")
        return 0
    except Exception as exc:
        detail = f"ncbi_error: unexpected {exc.__class__.__name__}: {exc}"
        print(f"[{utc_now()}] {detail}", file=sys.stderr)
        write_empty_outputs(query_date, "ncbi_error", detail)
        print("TASK 1 PARTIAL")
        return 0


if __name__ == "__main__":
    raise SystemExit(run())
