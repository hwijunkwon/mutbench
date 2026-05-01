#!/usr/bin/env python3
"""Wave 5 Task 2: position-level abstract evidence and curation worksheets.

This script intentionally performs only mechanical evidence aggregation. It
does not assign, propose, or copy Layer A labels.
"""

from __future__ import annotations

import csv
import re
from collections import Counter, defaultdict
from dataclasses import dataclass
from pathlib import Path

import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "results" / "mutbench" / "codex_wave5"
ABSTRACTS = OUT / "w5_abstracts"
WORKSHEETS = OUT / "worksheets"

AA_POS_RE = re.compile(r"\b([ACDEFGHIKLMNPQRSTVWY])(\d{1,4})\b")
MUTATION_RE = re.compile(r"\b([ACDEFGHIKLMNPQRSTVWY])(\d{1,4})([ACDEFGHIKLMNPQRSTVWY])\b")
POSITION_ONLY_RE = re.compile(r"(?:residue|position|amino acid)\s+(\d{1,4})", re.IGNORECASE)

KEYWORDS = [
    "escape",
    "neutralization",
    "antibody",
    "epitope",
    "antigenic",
    "fusion",
    "glycan",
    "EDI",
    "EDII",
    "EDIII",
    "GP1",
    "GP2",
    "SSP",
    "domain",
]
KEYWORD_RE = {
    keyword: re.compile(rf"\b{re.escape(keyword)}\b", re.IGNORECASE)
    for keyword in KEYWORDS
}


@dataclass(frozen=True)
class TargetConfig:
    slug: str
    abstract_dir: str
    score_csv: Path
    domain_order: tuple[str, ...]
    domain_ranges: dict[str, tuple[tuple[int, int], ...]]


TARGETS = [
    TargetConfig(
        slug="yfv_e",
        abstract_dir="YFV_E",
        score_csv=ROOT / "data" / "cross_pathogen" / "yfv_e_position_scores.csv",
        domain_order=("EDI", "EDII", "EDIII", "stem-anchor"),
        domain_ranges={
            "EDI": ((1, 51), (137, 189), (294, 310)),
            "EDII": ((52, 136), (190, 293)),
            "EDIII": ((296, 394),),
            "stem-anchor": ((395, 495),),
        },
    ),
    TargetConfig(
        slug="lassa_gpc",
        abstract_dir="Lassa_GPC",
        score_csv=ROOT / "data" / "cross_pathogen" / "lassa_gpc_position_scores.csv",
        domain_order=("SSP", "GP1", "GP2"),
        domain_ranges={
            "SSP": ((1, 58),),
            "GP1": ((59, 259),),
            "GP2": ((260, 491),),
        },
    ),
    TargetConfig(
        slug="wnv_e",
        abstract_dir="WNV_E",
        score_csv=ROOT / "data" / "cross_pathogen" / "wnv_e_position_scores.csv",
        domain_order=("EDI", "EDII", "EDIII", "stem-anchor"),
        domain_ranges={
            "EDI": ((1, 51), (137, 189), (294, 310)),
            "EDII": ((52, 136), (190, 293)),
            "EDIII": ((296, 394),),
            "stem-anchor": ((395, 501),),
        },
    ),
]

EVIDENCE_COLUMNS = [
    "position",
    "wt_aa_from_score_csv",
    "n_abstract_mentions",
    "pmid_list",
    "evidence_categories",
    "domain_assignment",
    "raw_extracts",
]
WORKSHEET_COLUMNS = [
    "position",
    "wt_aa",
    "evidence_count",
    "evidence_sources",
    "evidence_summary",
    "proposed_label",
    "confidence",
    "notes",
    "final_label",
    "curator",
    "curation_date",
]
VALIDATION_NOTE = (
    "# DO NOT AUTO-FILL final_label, proposed_label, or confidence "
    "\u2014 human curator only"
)


def normalize_text(text: str) -> str:
    return re.sub(r"\s+", " ", text).strip()


def stable_pmid_sort(pmids: set[str]) -> list[str]:
    return sorted(pmids, key=lambda value: int(value) if value.isdigit() else value)


def domain_assignment(config: TargetConfig, position: int) -> str:
    for domain in config.domain_order:
        for start, end in config.domain_ranges[domain]:
            if start <= position <= end:
                return domain
    return ""


def snippet(text: str, start: int, end: int, width: int = 80) -> str:
    half_context = max((width - (end - start)) // 2, 0)
    left = max(start - half_context, 0)
    right = min(end + half_context, len(text))
    raw = text[left:right].strip()
    if left > 0:
        raw = "..." + raw
    if right < len(text):
        raw = raw + "..."
    return raw[:width]


def abstract_keywords(text: str) -> set[str]:
    return {keyword for keyword, pattern in KEYWORD_RE.items() if pattern.search(text)}


def extract_mentions(text: str) -> dict[int, list[str]]:
    mentions: dict[int, list[str]] = defaultdict(list)
    for pattern in (MUTATION_RE, AA_POS_RE, POSITION_ONLY_RE):
        for match in pattern.finditer(text):
            position_text = match.group(2) if pattern is not POSITION_ONLY_RE else match.group(1)
            position = int(position_text)
            mentions[position].append(snippet(text, match.start(), match.end()))
    return mentions


def read_score_positions(path: Path) -> tuple[pd.DataFrame, str]:
    df = pd.read_csv(path)
    if "position" not in df.columns:
        raise ValueError(f"Missing position column in {path}")
    wt_col = ""
    for candidate in ("wt_aa", "wt", "ref_aa", "reference_aa", "aa"):
        if candidate in df.columns:
            wt_col = candidate
            break
    return df, wt_col


def aggregate_target(config: TargetConfig) -> tuple[pd.DataFrame, pd.DataFrame, dict[str, int | float]]:
    score_df, wt_col = read_score_positions(config.score_csv)
    valid_positions = set(int(pos) for pos in score_df["position"].tolist())
    position_pmids: dict[int, set[str]] = defaultdict(set)
    position_keywords: dict[int, Counter[str]] = defaultdict(Counter)
    position_snippets: dict[int, list[str]] = defaultdict(list)

    abstract_dir = ABSTRACTS / config.abstract_dir
    for path in sorted(abstract_dir.glob("*.txt"), key=lambda p: int(p.stem) if p.stem.isdigit() else p.stem):
        pmid = path.stem
        text = normalize_text(path.read_text(encoding="utf-8", errors="replace"))
        if not text:
            continue
        keywords = abstract_keywords(text)
        mentions = extract_mentions(text)
        for position, raw_snippets in mentions.items():
            if position not in valid_positions:
                continue
            position_pmids[position].add(pmid)
            for keyword in keywords:
                position_keywords[position][keyword] += 1
            for raw in raw_snippets:
                if len(position_snippets[position]) < 5:
                    position_snippets[position].append(raw)

    evidence_rows: list[dict[str, object]] = []
    worksheet_rows: list[dict[str, object]] = []
    for _, score_row in score_df.sort_values("position").iterrows():
        position = int(score_row["position"])
        pmids = stable_pmid_sort(position_pmids.get(position, set()))
        keyword_counts = position_keywords.get(position, Counter())
        categories = [keyword for keyword in KEYWORDS if keyword_counts.get(keyword, 0) > 0]
        domain = domain_assignment(config, position)
        wt_aa = str(score_row[wt_col]) if wt_col else ""
        if wt_aa == "nan":
            wt_aa = ""
        evidence_rows.append(
            {
                "position": position,
                "wt_aa_from_score_csv": wt_aa,
                "n_abstract_mentions": len(pmids),
                "pmid_list": ",".join(pmids[:20]),
                "evidence_categories": ";".join(categories),
                "domain_assignment": domain,
                "raw_extracts": "||".join(position_snippets.get(position, [])[:5]),
            }
        )
        worksheet_rows.append(
            {
                "position": position,
                "wt_aa": wt_aa,
                "evidence_count": len(pmids),
                "evidence_sources": ",".join(pmids[:10]),
                "evidence_summary": format_evidence_summary(domain, keyword_counts, pmids),
                "proposed_label": "",
                "confidence": "",
                "notes": "",
                "final_label": "",
                "curator": "",
                "curation_date": "",
            }
        )

    evidence_df = pd.DataFrame(evidence_rows, columns=EVIDENCE_COLUMNS)
    worksheet_df = pd.DataFrame(worksheet_rows, columns=WORKSHEET_COLUMNS)
    n_positions = len(evidence_df)
    n_with_any = int((evidence_df["n_abstract_mentions"] > 0).sum())
    strong = int(
        sum(
            1
            for row in evidence_rows
            if int(row["n_abstract_mentions"]) >= 2
            and (
                "escape" in str(row["evidence_categories"]).split(";")
                or "antibody" in str(row["evidence_categories"]).split(";")
            )
        )
    )
    stats = {
        "target": config.slug,
        "n_positions": n_positions,
        "n_with_any_evidence": n_with_any,
        "n_strong_evidence_candidate": strong,
        "n_zero_evidence": n_positions - n_with_any,
        "p_with_evidence": round(n_with_any / n_positions, 6) if n_positions else 0.0,
    }
    return evidence_df, worksheet_df, stats


def format_evidence_summary(domain: str, keyword_counts: Counter[str], pmids: list[str]) -> str:
    parts: list[str] = []
    if domain:
        parts.append(domain)
    category_parts = [
        f"{keyword}x{keyword_counts[keyword]}"
        for keyword in KEYWORDS
        if keyword_counts.get(keyword, 0) > 0
    ]
    if category_parts:
        parts.append(", ".join(category_parts))
    if pmids:
        parts.append(f"PMIDs {', '.join(pmids[:3])}")
    return "; ".join(parts)


def write_commented_csv(path: Path, df: pd.DataFrame) -> None:
    with path.open("w", newline="", encoding="utf-8") as handle:
        handle.write(VALIDATION_NOTE + "\n")
        writer = csv.DictWriter(handle, fieldnames=WORKSHEET_COLUMNS)
        writer.writeheader()
        for row in df.to_dict("records"):
            writer.writerow(row)


def validate_worksheets(paths: list[Path]) -> None:
    for path in paths:
        with path.open(encoding="utf-8", newline="") as handle:
            note = handle.readline().rstrip("\n")
            if note != VALIDATION_NOTE:
                raise ValueError(f"Missing validation note in {path}")
            reader = csv.DictReader(handle)
            if reader.fieldnames != WORKSHEET_COLUMNS:
                raise ValueError(f"Unexpected worksheet columns in {path}: {reader.fieldnames}")
            for row_number, row in enumerate(reader, start=2):
                for column in ("proposed_label", "confidence", "final_label"):
                    if row.get(column, "") != "":
                        raise ValueError(f"{path}:{row_number} has nonblank {column}")


def write_readme(path: Path) -> None:
    text = """# Wave 5 Task 2 Curation Worksheets

These worksheets are for human Layer A curation. Codex aggregated abstract-level residue evidence only and intentionally left `proposed_label`, `confidence`, and `final_label` blank.

## Decision Rules

- Strong evidence: >=2 independent papers OR DMS escape >X-fold -> `final_label=1`.
- Weak evidence: 1 paper or a narrow assay -> `final_label=1`, `confidence=low`, only if the curator accepts the biological relevance.
- No evidence -> `final_label=0`.
- Conflicting evidence -> flag for re-check in `notes`; default to `final_label=0` unless resolved.
- Conserved positions, especially in the YFV 17D vaccine context, should be interpreted with conservation context rather than treated as sufficient evidence alone.
- Use `curator` for your initials and `curation_date` in `YYYY-MM-DD` format.

## Columns

- Codex-filled: `position`, `wt_aa`, `evidence_count`, `evidence_sources`, `evidence_summary`.
- Human-only: `proposed_label`, `confidence`, `notes`, `final_label`, `curator`, `curation_date`.

Do not integrate Layer A labels until the human-only columns have been completed and approved in the Wave 5 human checkpoint.
"""
    path.write_text(text, encoding="utf-8")


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    WORKSHEETS.mkdir(parents=True, exist_ok=True)

    summary_rows: list[dict[str, int | float | str]] = []
    worksheet_paths: list[Path] = []
    for config in TARGETS:
        evidence_df, worksheet_df, stats = aggregate_target(config)
        evidence_path = OUT / f"w5_{config.slug}_evidence.csv"
        worksheet_path = WORKSHEETS / f"w5_{config.slug}_curation.csv"
        evidence_df.to_csv(evidence_path, index=False)
        write_commented_csv(worksheet_path, worksheet_df)
        summary_rows.append(stats)
        worksheet_paths.append(worksheet_path)

    summary_df = pd.DataFrame(
        summary_rows,
        columns=[
            "target",
            "n_positions",
            "n_with_any_evidence",
            "n_strong_evidence_candidate",
            "n_zero_evidence",
            "p_with_evidence",
        ],
    )
    summary_path = OUT / "w5_evidence_summary.csv"
    summary_df.to_csv(summary_path, index=False)
    readme_path = WORKSHEETS / "README.md"
    write_readme(readme_path)
    validate_worksheets(worksheet_paths)

    print("Per-target evidence counts:")
    for row in summary_df.to_dict("records"):
        print(
            f"- {row['target']}: any evidence "
            f"{row['n_with_any_evidence']}/{row['n_positions']}; "
            f"strong-evidence candidates {row['n_strong_evidence_candidate']}"
        )
    print("Worksheet paths:")
    for path in worksheet_paths:
        print(f"- {path.relative_to(ROOT)}")
    print(f"Worksheet README: {readme_path.relative_to(ROOT)}")
    print("TASK 2 DONE")


if __name__ == "__main__":
    main()
